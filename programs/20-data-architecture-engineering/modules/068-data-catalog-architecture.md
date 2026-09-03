---
module_id: DARCH-068
program: Data Architecture Engineering
level: 2
module_number: 68
title: Data Catalog Architecture
status: complete
last_verified: 2026-09-03
---

# Data Catalog Architecture

## One-Page Review

### Governing question

How should an organization identify, ingest, reconcile, describe, connect, search, govern, operate, and retire metadata about data resources so people and machines can discover suitable assets and evaluate their fitness without confusing catalog claims with the resources themselves?

### Essential definitions

- A **data catalog** is a governed metadata system that represents resources, distributions, services, schemas, terms, people, policies, quality, lineage, usage, and lifecycle for discovery and action.
- A **cataloged resource** is the thing described, such as a dataset, stream, API, dashboard, model, report, file collection, or data product.
- A **catalog record** is the catalog's attributable description of a resource. Its creation and modification times can differ from the resource's own lifecycle.
- A **dataset** is a conceptual collection of data; a **distribution** is one accessible representation of it; a **data service** exposes operations that provide or process data.
- **Descriptive metadata** supports identification and discovery; **structural metadata** describes organization and schema; **administrative metadata** supports management, rights, and lifecycle.
- **Operational metadata** records observed runs, access, freshness, volume, incidents, and other changing system behavior.
- **Business metadata** connects resources to terms, purposes, domains, owners, rules, and decision context.
- A **metadata assertion** is a claim about an entity or relation with source, observation or effective time, confidence, authority, and lifecycle.
- A **metadata graph** represents catalog entities and typed relations such as ownership, containment, derivation, use, implementation, classification, and meaning.
- A **connector** extracts, receives, maps, checkpoints, and publishes metadata from a source into a catalog ingestion boundary.
- **Reconciliation** compares source, catalog, search, graph, and downstream projections to detect absence, conflict, duplication, dangling relations, and stale state.
- A **catalog profile** is a bounded application of a metadata model and vocabulary for a community, resource class, or exchange.
- **Discovery** finds candidate resources; **evaluation** assesses fitness for a stated purpose; **access** authorizes and delivers data. A catalog can support all three without collapsing them.
- **Active metadata** is metadata delivered into operational workflows or used to trigger policy and automation, not merely displayed on a catalog page.

### Central model, mechanism, or theorem

Represent a catalog capability as:

`K = (I, E, A, G, V, P, X, Q, W, S, O, L)`

where `I` is identity, `E` entities, `A` attributable assertions, `G` the relation graph, `V` vocabularies and profiles, `P` provenance and precedence, `X` ingestion and exchange, `Q` search and fitness signals, `W` stewardship workflows, `S` security and policy, `O` operation and reconciliation, and `L` lifecycle closure. A catalog answer is trustworthy only relative to a named resource identity, assertion sources, observation times, authority rules, projection versions, user context, and intended decision. Search relevance is not truth, popularity is not quality, and presence in the catalog is not permission to access or use data.

### Critical invariants

- Resource identity, catalog-record identity, source-system identity, distribution identity, service identity, and mutable names remain distinct.
- Every consequential assertion records source, authority, observation or effective time, ingestion event, and supersession behavior.
- Source connectors cannot silently overwrite human stewardship, policy decisions, or another authoritative source without explicit field-level precedence.
- The canonical metadata store is authoritative for accepted catalog state; graph and search indexes are rebuildable, versioned projections.
- A resource is not declared deleted because one crawler temporarily failed to observe it; absence progresses through bounded suspicion and reconciliation.
- Search authorization filters apply before disclosure and ranking, including counts, snippets, suggestions, relations, and timing behavior.
- Quality, popularity, certification, freshness, ownership, documentation, and semantic fit remain separate signals with visible denominators and times.
- Lineage edges retain their observation type, granularity, producer, run or design context, and confidence; reachability is not causality.
- Federated catalogs preserve source authority, stable cross-catalog identity, profile conformance, and conflict evidence.
- Metadata changes are idempotent, ordered or conflict-resolved, replayable, auditable, and reconciled across projections.
- Catalog availability never authorizes otherwise forbidden data access, and data access does not imply catalog disclosure.
- Retirement closes ingestion, aliases, search results, relations, automation, access requests, caches, exports, backups, and recovery while preserving required historical evidence.

### Common failures

Common failures include cataloging physical tables but not conceptual datasets; treating names as durable identity; merging identical-looking assets; making the search index the system of record; accepting last-write-wins across unequal sources; deleting on first missing crawl; calling graph reachability lineage; ranking popularity as trust; displaying quality without metric or time; inferring ownership from recent queries; exposing sensitive names through autocomplete; collecting query text without privacy controls; letting unbounded connectors overwhelm the store; refreshing everything through full scans; producing duplicate entities after renames; synchronizing taxonomies without stable concept IDs; claiming federation while copying metadata into one authority; turning tags directly into access policy; automating from stale metadata; measuring record count instead of discovery success; and retiring pages while active ingestion recreates them.

### Compact example

A toy catalog contains six assets and four lineage relations. Five assets are active, all six documented, five owned, one stale, and one orphaned. One relation points to an unknown target. A search for `order` produces three lexical candidates, but freshness, lifecycle, and ownership eligibility leave two results; `orders` ranks first. Executable evidence proves only those invented records, filters, and scores. It does not prove useful relevance, correct identity, complete metadata, real lineage, safe authorization, quality, semantic fit, or production scalability.

### Connections

[DARCH-016](016-canonical-models-and-their-trade-offs.md), [DARCH-019](019-model-versioning.md), [DARCH-027](027-producer-and-consumer-contracts.md), [DARCH-061](061-metadata-architecture.md), [DARCH-062](062-metadata-harvesting-and-synchronization.md), [DARCH-063](063-business-glossaries-and-term-governance.md), [DARCH-064](064-lineage-architecture.md), [DARCH-066](066-semantic-interoperability.md), and [DARCH-067](067-schema-registries.md) establish the catalog's model, ingestion, semantic, lineage, and schema foundations. [DARCH-069](../ROADMAP.md) next develops metadata APIs and eventing.

## Governing Question

An organization can possess thousands of tables, streams, files, APIs, dashboards, models, and reports yet still be unable to answer which resource is authoritative, what it means, who owns it, whether it is current, how it was produced, which policy applies, or how to obtain access. A spreadsheet inventory decays because resources and relationships change continuously. A crawler-only catalog is comprehensive only for what its credentials and adapters happen to observe. A socially curated portal is useful only while people can keep its technical claims synchronized.

The governing question is how to build a durable metadata control plane that combines machine observations and human assertions without erasing their origins. The architecture must support discovery, evaluation, governance, automation, and exchange, while keeping the catalog record distinct from the resource, relevance distinct from fitness, and metadata visibility distinct from data authorization.

## Why This Matters

W3C [Data Catalog Vocabulary 3](https://www.w3.org/TR/vocab-dcat-3/) defines an interoperable RDF vocabulary for catalogs. It distinguishes catalogs, cataloged resources, datasets, distributions, data services, dataset series, and catalog records. A conceptual dataset can have several distributions and be provided through services; the catalog record can separately capture registration provenance. DCAT also provides versioning, relationships, rights, policy, themes, temporal and spatial coverage, and catalog composition. These distinctions prevent a download URL or warehouse table from becoming the only model of a dataset.

W3C [Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/) models quality dimensions, metrics, measurements, annotations, certificates, policies, and user feedback. It deliberately does not declare one universal meaning of quality. Catalog architecture should preserve who measured what, using which metric, for which resource or distribution, at what time, rather than flattening evidence into an unexplained green badge.

W3C [PROV-O](https://www.w3.org/TR/prov-o/) encodes provenance concepts including entities, activities, agents, generation, use, derivation, attribution, association, delegation, and qualified relations. A catalog can use provenance to distinguish a resource's production history from the catalog record's ingestion history and from a curator's later assertion.

W3C [SKOS](https://www.w3.org/TR/skos-reference/) distinguishes concepts from preferred, alternative, and hidden labels and models broader, narrower, related, and mapping relations. Catalog themes and business terms benefit from stable concept identity and multilingual labels. Search synonyms should not become assertions that two concepts are semantically exact.

The [DCMI Metadata Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/) define reusable properties and classes for identifiers, titles, descriptions, creators, publishers, subjects, coverage, formats, rights, licenses, provenance, versions, relations, and other metadata. Their use in application profiles illustrates how a catalog can adopt shared semantics while adding bounded local requirements.

W3C [SHACL](https://www.w3.org/TR/shacl/) defines shapes, targets, constraints, severities, validation results, and conformance for RDF graphs. A DCAT exchange or internal graph can be checked against a profile, but conformance to a shape does not prove the truth, currency, authority, or business fitness of asserted metadata.

The [OpenLineage object model](https://openlineage.io/docs/spec/object-model/) identifies jobs and datasets by namespace and name, distinguishes a job from its runs, and carries extensible facets on jobs, runs, inputs, outputs, and datasets. It supports runtime run events plus design-time job and dataset metadata events. This separation helps a catalog retain what was designed, what executed, and what changed instead of converting every observation into one timeless lineage edge.

[Apache Atlas](https://atlas.apache.org/2.0.0/index.html) presents a typed metadata repository with entities and relationships, classifications, lineage, search, REST APIs, hooks and bridges, notifications, authorization integration, high availability, and import/export. It demonstrates a graph-oriented governance implementation in which type system, ingestion, search, security, and operational architecture are inseparable.

The [OpenMetadata architecture documentation](https://docs.open-metadata.org/latest/developers/architecture) describes JSON Schemas for metadata models, REST APIs, a relational metadata store, and a separate search index. That decomposition illustrates why a catalog needs a transactional source of accepted metadata and rebuildable retrieval projections rather than treating a search engine as canonical storage.

The [DataHub architecture overview](https://github.com/datahub-project/datahub/blob/master/docs/architecture/architecture.md) describes schema-first metadata modeling, REST, GraphQL, and stream-based metadata APIs, real-time change propagation, and federated metadata serving connected to central search and graph capabilities. It supplies a concrete example of catalog metadata as an eventful platform that downstream automation can subscribe to.

These sources show that a catalog is neither a list nor a single database product. It is a sociotechnical system joining identifiers, models, connectors, assertions, graphs, indexes, workflows, policies, interfaces, and operations. If those pieces disagree, an attractive search page can confidently direct users to the wrong asset or trigger unsafe automation.

## Prerequisites and Retrieval

You should understand metadata, data modeling, identifiers, graphs, taxonomies, ontologies, lineage, quality, schemas, contracts, search and ranking, APIs, events, connectors, distributed systems, authorization, privacy, provenance, versioning, observability, disaster recovery, migration, and governance.

Retrieve catalog, cataloged resource, catalog record, dataset, distribution, data service, dataset series, metadata assertion, source authority, observation time, effective time, provenance, connector, harvester, push, event, checkpoint, reconciliation, tombstone, search index, metadata graph, projection, taxonomy, glossary, profile, validation, quality dimension, metric, measurement, annotation, certification, lineage, usage, popularity, ownership, stewardship, data product, federation, active metadata, access workflow, deprecation, retirement, and historical interpretation.

As a retrieval test, inspect a search result called `customer_360`. Ask whether it denotes a conceptual dataset, table, view, stream, dashboard, data product, or catalog page; which environment and authority issue its identity; whether aliases point to a renamed predecessor; which distribution or service provides access; when technical and business metadata were observed; who asserted ownership and meaning; what quality measurement applies; whether displayed lineage was declared or observed; whether the viewer may know it exists; and whether access is separately authorized. The label alone answers none of these questions.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish resources, datasets, distributions, services, products, catalog records, assertions, and projections;
2. design stable identity, alias, merge, split, rename, environment, and cross-catalog resolution;
3. model technical, operational, business, governance, quality, lineage, usage, and social metadata with provenance;
4. choose pull, push, event, query-log, static, and human curation ingestion by authority and latency;
5. reconcile duplicates, conflicts, missing observations, stale state, dangling relations, and projection drift;
6. build authorization-aware lexical, faceted, semantic, and graph discovery with explainable ranking;
7. integrate glossaries, profiles, quality, lineage, schema registries, contracts, access, and stewardship without collapsing their ownership;
8. compare centralized, federated, domain-owned, embedded, graph-first, and search-first catalog designs;
9. operate catalog APIs, events, SLOs, privacy, security, scalability, recovery, migration, and economics; and
10. deprecate and retire cataloged resources while preserving required provenance and historical interpretation.

## Core Exposition

**Begin with discovery decisions.** Identify users, tasks, resources, consequences, and actions. An analyst finding a trustworthy revenue table, an engineer assessing blast radius, a privacy reviewer locating personal fields, and an automated access controller need different metadata, freshness, recall, precision, and authorization.

Do not optimize a catalog for page count before defining successful decisions. Measure whether qualified users find and correctly evaluate suitable resources, not merely whether ingestion created records.

**Separate resource from record.** The resource exists in a source authority. The catalog record describes it. A record can be created after a dataset, updated by ingestion without changing the dataset, or retained after a resource is retired.

Use separate identities and timestamps. `resource.modified_at` should not be overwritten by `catalog_record.harvested_at`, and a changed description should not falsely imply the data was refreshed.

**Separate conceptual dataset from delivery.** A conceptual dataset can have warehouse, file, API, stream, language, resolution, or historical distributions. A data service can provide access to several datasets or perform selection and transformation.

Model access URLs and physical stores as distributions or services rather than equating one location with the dataset. This supports migration and multi-format publication without changing conceptual identity.

**Define the catalog scope.** State included resource types, environments, authorities, domains, regions, lifecycle states, metadata classes, users, automation, retention, and exclusions. Define whether ephemeral tables, temporary jobs, personal workspaces, development assets, external shares, and deleted resources belong.

Scope affects cost, privacy, ranking, and completeness claims. Publish coverage denominators by source and type rather than saying “the enterprise is cataloged.”

**Design stable resource identity.** A durable key often includes source authority, platform instance, environment, resource type, and source-native stable identifier. Human paths and display names become attributes and aliases.

Normalize only what the source contract says is equivalent. Case-folding a case-sensitive identifier or removing environment can merge distinct resources. Never infer identity from matching schema alone.

**Model rename, move, merge, split, and recreation.** A rename can preserve identity in one platform; a drop-and-create with the same name can create a new resource. A dataset can split into successors or merge into a replacement.

Record source-native events, old aliases, effective times, identity decisions, and evidence. Search redirects can guide users without rewriting historical lineage to the new resource.

**Use typed entities and relations.** Common entity types include datasets, distributions, services, streams, schemas, fields, jobs, runs, dashboards, charts, reports, models, features, metrics, terms, policies, people, teams, domains, products, quality checks, incidents, and access requests.

Relations name meaning: contains, provides, implements, derives from, consumes, produces, visualizes, trains on, owns, stewards, classifies, conforms to, supersedes, serves, or depends on. Avoid a generic edge that leaves direction and semantics to UI guesswork.

**Make assertions first-class.** One resource can have a technical description harvested from a database, a business description written by a steward, an inferred classification, and a disputed owner imported from a directory.

Represent value, subject, predicate, source, agent, observation time, effective interval, confidence, method, authority class, ingestion event, and supersession. The resolved view can choose one display value while preserving disagreements and their origins.

**Define field-level precedence.** Source systems usually own physical schema and location. Domain stewards may own business description and terms. Security policy can own classification. Observability systems own measurements they produce. Identity directories own active people and teams.

Precedence depends on field, source, scope, and time—not one global source priority. A manual correction to harvested technical metadata needs a durable override strategy or a route back to the source, not silent permanent conflict.

**Distinguish declared, observed, inferred, and reviewed metadata.** A producer declares an owner; a query log observes use; a classifier infers sensitive data; a steward reviews the classification. Each has different authority and confidence.

Render these differences and constrain automation. An inferred tag can create a review task, while a verified policy classification may block access.

**Choose ingestion mode by source behavior.** Pull connectors crawl systems that expose current state. Push APIs accept metadata from producers and CI. Event ingestion observes changes or runs. Static manifests declare intended state. Query parsing infers usage and lineage. Human workflows add contextual assertions.

Combine modes without pretending they are interchangeable. A full crawl can detect existing objects missed before; events reduce latency; reconciliation repairs loss; human review supplies meaning machines cannot safely infer.

**Treat connectors as production software.** A connector has source version, credentials, scopes, extraction contract, mapping version, checkpoint, idempotency, rate limit, backoff, pagination, deletion semantics, schema evolution, error classes, observability, and ownership.

Test incomplete permissions, source throttling, pagination mutation, renamed objects, timeouts after writes, duplicates, clocks, malformed metadata, large schemas, unsupported types, and source upgrades. Connector success means more than process exit zero.

**Use source snapshots and change events together.** Snapshot ingestion gives a point-in-time inventory; events give low-latency deltas. Associate both with source authority and watermark.

Reconcile event-applied state against periodic snapshots. Do not let an old snapshot overwrite newer events; compare source versions, observation times, and monotonic tokens where available.

**Make ingestion idempotent.** A retried metadata proposal with the same source event identity and content should produce the same accepted state. Store deduplication identity long enough for the retry and replay horizon.

Avoid generating new catalog IDs for each observation. Separate assertion event identity from resource identity and content identity.

**Model time explicitly.** At minimum distinguish source event time, observation time, ingestion time, effective time, processing time, catalog acceptance time, and projection time.

Late observations can describe an earlier state. A search index updated now may expose metadata effective yesterday. Preserve temporal semantics so replay and conflict resolution do not rely on arrival order alone.

**Handle absence cautiously.** A missing resource in one crawl can mean deletion, permission loss, connector filter change, partial page, source outage, rename, or transient error.

Progress through states such as observed, missing-suspected, missing-confirmed, deprecated, and retired. Require repeated complete observations, explicit source tombstones, or authoritative deletion events before destructive transitions.

**Represent tombstones.** A tombstone identifies the resource, source, deletion or retirement event, time, reason, replacement, retention, and propagation state. It prevents stale replay from recreating a removed resource without evidence.

Do not erase the identity immediately. Historical lineage, audit, saved searches, incident analysis, and retained data may still refer to it.

**Separate canonical store from projections.** The accepted metadata store preserves identities, assertions, relations, versions, and audit. Search indexes, graph traversals, analytics aggregates, recommendations, and UI materializations are projections.

Give every projection a schema and build version, source offset, rebuild procedure, lag metric, and reconciliation. A projection can be eventually consistent without becoming an alternate authority.

**Choose storage by access patterns.** Relational storage supports transactional constraints and familiar operations. Graph stores support typed relationship traversal. Search engines support lexical retrieval, faceting, highlighting, and ranking. Object storage can retain raw harvests and replay logs.

One engine can serve several roles at modest scale, but name which invariants it owns. Polyglot storage adds synchronization and recovery obligations; a fashionable graph database does not automatically create sound lineage.

**Design the metadata graph semantically.** Edge type, direction, endpoints, source, time, scope, granularity, confidence, and lifecycle matter. Containment, semantic mapping, transformation, and observed co-use should not share one `related_to` relation.

Represent hyperedges or process nodes when an activity transforms many inputs into many outputs. Inferring every input-to-output pair can create false Cartesian lineage.

**Separate design and runtime lineage.** Design lineage states intended dependencies from code or models. Runtime lineage reports what a particular run read and wrote. Query-derived lineage is an observation based on parsing. Manual lineage is an attributed assertion.

Preserve them independently. A declared dependency not observed recently can indicate inactive code, sampling, instrumentation gaps, or a failure—not automatically a false edge.

**Integrate schema metadata by identity.** Link catalog resources and distributions to immutable schema-registry versions or source schema observations. Preserve field identity through rename and type evolution where the source can justify it.

Do not copy `latest` schema text into the catalog without the version and authority. Catalog enrichment should not become a second mutable schema registry.

**Connect business terms carefully.** A resource or field can be classified by a stable glossary concept under an explicit relationship: implements, represents, approximates, derived from, or governed by.

Do not map by label alone. Preserve concept scheme, version, scope, mapping authority, effective time, confidence, and review. Search synonyms are retrieval aids and do not prove semantic equivalence.

**Use application profiles.** A profile states required and recommended metadata for a community or resource class, controlled vocabularies, cardinalities, value forms, validation rules, severities, and extensions.

Validate machine conformance and report focus entity, path, offending value, rule, severity, and source. A complete record can still be wrong; profile validation is one evidence layer.

**Model quality evidence, not a universal score.** A quality measurement identifies resource or distribution, metric definition and version, dimension, value and unit, computation, data interval, observation time, producer, coverage, result, and limitations.

Certification, user feedback, incidents, and automated measurements remain distinct. A weighted score hides trade-offs and can be gamed. Let consumers select dimensions relevant to their purpose.

**Model freshness with several clocks.** Source data freshness, schema freshness, catalog observation freshness, quality-measurement freshness, lineage freshness, and steward-review freshness are different.

Display the relevant clock and service expectation. “Updated two minutes ago” must say whether the data, catalog page, connector, index, or quality check changed.

**Treat ownership as an accountable relation.** Distinguish producer, accountable domain owner, technical operator, steward, subject-matter expert, support contact, platform owner, and approver.

Query frequency and repository commits can suggest contacts but should not silently assign accountability. Define transfer, absence, team deletion, escalation, and periodic attestation.

**Design search as a pipeline.** Typical stages include authorization-aware corpus selection, query parsing, normalization, lexical retrieval, semantic or graph candidate generation, filtering, ranking, diversification, explanation, and feedback.

Index titles, aliases, descriptions, terms, fields, owners, domains, classifications, and resource types with field-aware analyzers. Keep stable identity outside language-specific tokenization.

**Secure before ranking.** Apply visibility and field-level disclosure before candidate counts, facets, autocomplete, spelling suggestions, snippets, embeddings, related assets, lineage, and rankings are exposed.

Post-filtering an unrestricted result set can leak existence through counts, timing, or suggestions. Build authorization-aware indexes or query filters with tested noninterference appropriate to consequence.

**Make ranking explainable.** Signals can include lexical match, concept match, endorsed status, documentation, ownership, recency, fit profile, quality evidence, usage by peers, lineage proximity, support, and lifecycle.

Avoid one opaque popularity score. Show why an item appeared and let users filter or re-rank by purpose. A certified but rarely used source can be better than a popular obsolete extract.

**Control popularity feedback loops.** High-ranked assets receive more clicks and queries, which can make them rank higher. New or specialized assets become invisible.

Normalize usage by eligible population and time, damp repeats and automation, preserve privacy, diversify results, allocate exploration, and evaluate relevance with counterfactual or curated judgments.

**Use semantic retrieval conservatively.** Embeddings can improve recall for natural-language queries and multilingual descriptions. They can expose sensitive text, drift with model versions, reproduce bias, and produce inexplicable near-neighbors.

Record embedding model, input fields, time, authorization boundary, index version, and deletion propagation. Use semantic similarity to retrieve candidates, not to assert term equivalence or fitness.

**Support graph discovery.** Users may explore upstream and downstream lineage, dashboards using a dataset, terms applied to fields, owners of related resources, or products that provide a distribution.

Bound traversal by edge type, direction, confidence, time, lifecycle, authorization, and depth. Avoid presenting every reachable node as caused by or dependent on the starting node.

**Separate discovery, evaluation, and access.** Discovery identifies candidates. Evaluation examines meaning, provenance, quality, freshness, contract, examples, support, and limitations. Access applies policy and provisions credentials or delivery.

The catalog can link the workflow, but a search result or owner approval does not itself grant data access. Conversely, secret resources may be usable through a service without broad catalog discoverability.

**Design asset pages for decisions.** A page should state durable identity, type, environment, description, purpose, owner, support, terms, schema, distributions and services, classifications, policy, quality, freshness, lineage, usage context, incidents, lifecycle, version, and provenance.

Show conflicts and stale sections rather than smoothing them into false certainty. Distinguish human assertions, source observations, and inferred suggestions visually and through APIs.

**Create stewardship workflows.** Useful workflows include claim ownership, request description, propose term, review classification, resolve duplicate, attest metadata, certify fit, handle issue, approve exception, deprecate, and retire.

Each workflow needs state, role, evidence, due date, escalation, comments, immutable history, notifications, and closure criteria. Avoid turning the catalog into an unaudited comment stream.

**Bring work to owners.** Integrate review and alert tasks with systems where owners work, while retaining the catalog as the authoritative workflow record. Use idempotent external-message keys and reconcile delivery and response.

Notification volume needs prioritization, digesting, routing, quiet periods, deduplication, and escalation. An ignored flood makes a technically complete workflow operationally empty.

**Treat certification as scoped.** A certification names resource version or identity, intended purpose, consumer population, evidence, checks, reviewer, policy, effective interval, and revocation conditions.

A generic `certified` badge is dangerous. Certification for exploratory analytics may not cover finance reporting, model training, or individual decisions.

**Represent data products explicitly.** A data product can group datasets, distributions, services, documentation, contracts, quality objectives, policies, support, consumers, and lifecycle under accountable ownership.

Do not treat a tag named `product` as enough. Model membership, offered interfaces, service objectives, versioning, dependencies, costs, and closure.

**Enable active metadata through governed events.** Metadata events can trigger access review, pipeline warnings, classification propagation, contract tests, impact analysis, or owner tasks.

Subscribers need event schema, identity, before and after state or retrievable version, source, time, ordering, idempotency, authorization, replay, and tombstones. Automation should state acceptable staleness and compensation for false triggers.

**Avoid policy-by-tag shortcuts.** Tags are often collaborative labels with weak authority. Policy classifications require controlled identity, issuing authority, scope, review, provenance, effective time, and conflict behavior.

An inferred `PII` suggestion can start a security workflow. It should not silently declassify or override a verified restriction when absent from a later crawl.

**Design catalog APIs around stable concepts.** Provide identity resolution, typed entity and relation retrieval, assertion provenance, version or temporal views, search, graph traversal, profile validation, workflow actions, bulk export, change feed, and health.

Use idempotent writes, optimistic concurrency, pagination with stable cursors, field masks, bounded traversal, consistent errors, rate limits, and explicit projection freshness. Separate administrative, ingestion, user, and high-volume automation interfaces.

**Expose metadata change events.** Events represent proposals, accepted changes, projection updates, lifecycle transitions, and perhaps workflow decisions. Do not call a proposal authoritative before validation and conflict resolution.

Partition by stable identity where ordering matters. Include event ID, entity ID, assertion or version ID, operation, source, actor, effective and processing times, schema, trace, and replay semantics.

**Federate authority, not merely deployment.** In federation, domains or platforms retain authority for designated entities or assertions while shared protocols enable global identity, search, graph, and exchange.

Define minimum profile, namespace allocation, resolution, provenance, conflict, indexing, availability, latency, deletion, security, and exit. A central crawler copying everything remains centralized even if sources are distributed.

**Choose federation topology.** A central index can query or ingest domain metadata. A distributed query can fan out to domain catalogs. A hybrid can replicate discovery fields centrally while resolving detailed metadata at source.

Central indexes improve latency and consistent ranking but add staleness and disclosure. Distributed query preserves current authority but creates tail latency and partial-result semantics. Declare which result is complete enough for each use.

**Validate metadata exchange.** Use profiles and shape validation for required identity, labels, ownership, rights, distributions, services, versions, and relations. Preserve extensions in namespaces and reject collisions.

Exchange conformance does not establish that the source claims are true or that the receiving catalog applies the same business meaning. Record provenance and profile version and reconcile round trips.

**Protect metadata as sensitive data.** Catalogs reveal system names, schemas, personal fields, security classifications, vulnerabilities, business initiatives, users, query text, lineage, and access patterns.

Classify metadata itself. Apply least privilege, tenant isolation, field redaction, secure search, encryption, audit, retention, legal review, and controlled export. Avoid making public metadata about secret resources unless a deliberate opaque reference is required.

**Protect behavioral metadata.** Query logs, popularity, followers, favorites, and search history can reveal employee behavior, investigations, health or finance interests, and sensitive projects.

Minimize collection, aggregate thresholds, separate operational from personalization purpose, constrain retention, support subject rights where applicable, and prevent ranking telemetry from becoming a surveillance system.

**Secure connectors and parsers.** Connectors often hold broad read credentials and process attacker-controlled names, schemas, comments, and API responses. Isolate execution, minimize scopes, rotate secrets, validate certificates, bound payloads, scan dependencies, and redact logs.

Treat rich descriptions and embedded markup as untrusted content. Sanitize UI output and exports to prevent injection.

**Scale ingestion by change.** Prefer incremental checkpoints, source events, hashes, partitioned scans, and priority queues over repeated full extraction. Separate raw acquisition from normalization, identity resolution, assertion acceptance, and projection.

Backpressure by source and cost. A huge schema or flapping source should not starve critical lifecycle and security changes.

**Scale search and graphs deliberately.** Define document size, nested field, shard, analyzer, facet, embedding, traversal depth, fan-out, and relation cardinality limits. Precompute selected neighborhoods and use asynchronous exploration for expensive paths.

Pagination must remain stable enough for a session, and graph APIs must defend against degree explosions. Test high-degree owners, terms, shared fields, and universal source tables.

**Observe end-to-end freshness.** Measure source event to accepted store, accepted store to search, accepted store to graph, workflow creation, notification delivery, and automation action separately.

Track connector coverage, success, partial completion, checkpoint age, records read, accepted, rejected, deduplicated, conflicted, missing-suspected, and deleted. A green connector with zero authorized objects is not healthy.

**Measure discovery outcomes.** Useful indicators include search success, reformulation, zero-result rate, time to qualified selection, result diversity, stale selection, access completion, user correction, owner response, and downstream incident.

Segment by role, task, domain, language, sensitivity, and new versus expert user. Click-through alone rewards attractive or already popular pages.

**Measure metadata health with denominators.** Report coverage of active in-scope resources, not raw counts. Separate identity, owner, description, term, schema, contract, quality, lineage, freshness, support, policy, and lifecycle coverage.

Time-bound every metric. A description written five years ago can satisfy non-null coverage and still be misleading.

**Set service objectives by path.** Search, entity lookup, graph traversal, ingestion acceptance, projection freshness, workflow, change event, bulk export, and recovery have different latency and availability needs.

Define partial-result behavior in federation and degraded mode. Search can serve a labeled stale snapshot during ingestion outage; policy automation may require fresher verified metadata.

**Reconcile every projection.** Periodically compare canonical entity and relation versions to search and graph projection offsets, counts, hashes, and sampled content. Detect dangling edges, missing documents, duplicates, stale tombstones, unauthorized fields, and ranking-feature drift.

Repair from the accepted event log or store, not by declaring the projection authoritative. Verify repair with user-visible queries and authorization cases.

**Design backup and recovery for identity.** Back up resource and record identities, assertions, provenance, relations, vocabularies, profiles, raw observations, accepted events, workflows, policies, aliases, tombstones, audit, and configuration.

Rebuild projections from a known checkpoint, compare counts and content digests, validate high-consequence resources, test search and graph authorization, resume connectors without duplicate or destructive absence, and reconcile before automation restarts.

**Plan migration and portability.** Export canonical and source-native identities, original assertions, provenance, history, relations, controlled vocabularies, profiles, quality evidence, lineage types, workflows, policies, aliases, and tombstones—not only current pages.

Map target semantics explicitly. Shadow ingestion and search, compare identity and relation graphs, dual-publish events, test authorization, canary users and automation, and retain rollback. Product feature parity does not prove metadata equivalence.

**Manage catalog economics.** Cost includes connectors, source queries, event transport, storage, search and graph indexes, embeddings, backups, support, stewardship time, access integration, security, and migration.

Allocate cost by durable drivers such as resources, fields, change rate, query volume, retention, graph density, service objective, and connector complexity. Never incentivize domains to hide sensitive or low-usage resources merely to reduce record count.

**Deprecate visibly.** A deprecated resource records reason, replacement, owner, affected consumers, support end, access behavior, migration, and effective time. Search can demote it while preserving explicit discovery and historical links.

Do not redirect silently when semantics differ. Consumers need to compare contracts and activate deliberately.

**Retire the full relationship.** Stop source production or delivery as authorized, disable new access, close consumers, terminate connector observations, remove mutable aliases, suppress normal search, close workflows and automation, update lineage and products, revoke credentials, and update recovery.

Preserve catalog records, tombstones, provenance, schema identities, quality and incident evidence, and historical relations for the required period. Test that replay or restore does not republish a retired resource as active.

## Definitions and Notation

Let `r` denote a cataloged resource and `c(r)` its catalog record. Let `D(r)` be distributions of `r` and `S(r)` data services that provide or process it. Resource identity and record identity are separate even when one page presents both.

Let an assertion be `a = (r, p, v, s, g, t_o, t_e, q, m, z)`, where `p` is predicate, `v` value, `s` source, `g` asserting agent, `t_o` observation time, `t_e` effective interval, `q` confidence or qualification, `m` method, and `z` lifecycle or supersession state.

Let `A(r, p, t)` be all non-retired assertions for resource `r` and predicate `p` applicable at time `t`. Let precedence function `Π(p, context, A)` choose a resolved display value or conflict set. Precedence is predicate- and context-specific.

Let metadata graph `G_t = (V_t, E_t)` contain typed, time-qualified entities and relations known at catalog time `t`. An edge `e = (u, relation, v, source, observation, scope, confidence)` is more informative than untyped adjacency.

Let `H_s` be the set of resources authoritatively observed in a complete source snapshot `s`, and `C_s` the active catalog identities expected for that source. Missing candidates are `M_s = C_s − H_s`. They become deletion evidence only under a stated completeness and confirmation policy.

Let accepted metadata log offset be `o_a`, search projection offset `o_x`, and graph projection offset `o_g`. Projection lag can be measured in offsets and time: `lag_x = o_a − o_x`; zero offset lag does not prove content correctness, so reconciliation also compares identities and digests.

For query `q` and viewer `u`, define authorized candidate set `C(q, u)` before ranking. Let feature vector `φ(q, r, u, t)` include lexical, concept, lifecycle, documentation, ownership, freshness, quality, and usage signals. Ranking score `score = w · φ` is a policy output, not truth.

Let `Eligible(r, u, purpose, t)` express visibility plus required lifecycle, freshness, ownership, profile, policy, and perhaps quality gates. Search relevance and eligibility remain separate; a highly relevant result can be ineligible.

For required metadata predicate set `P` and in-scope active resources `R`, field coverage is `coverage(p) = |{r ∈ R : valid_current(r,p)}| / |R|`. Overall non-null cell count is not a substitute for per-predicate denominators.

Let quality measurement `qm = (r, d, metric, value, unit, window, observed, producer, coverage, result)`, with dimension `d`. Comparing measurements requires compatible metric versions, units, windows, populations, and result semantics.

Let catalog freshness for assertion `a` at time `t` be `F(a,t) = t − t_o`; source-data freshness requires a different timestamp. Service objectives specify which clock and population they govern.

Let `Resolve(id, authority, t)` return the resource identity valid under authority at time `t`, including alias and tombstone evidence. A bare name does not define this function.

Let `Fit(r, purpose, u, t)` be a conjunctive or explicitly scored decision over meaning, authority, quality, freshness, policy, access, support, and consumer requirements. Catalog presence and search rank alone do not imply `Fit`.

## Mechanisms, Invariants, or Proof Structure

Use the following gates to design and review data catalog architecture.

**Decision gate.** Name users, discovery and governance decisions, resource types, consequences, actions, required evidence, latency, and success measures.

**Scope gate.** Declare authorities, environments, domains, regions, lifecycle states, temporary resources, external resources, metadata classes, and coverage denominators.

**Identity gate.** Govern source-native key, authority, type, environment, catalog record, alias, rename, move, recreation, merge, split, version, distribution, service, and non-reuse.

**Model gate.** Define typed entities, relations, fields, assertions, extensions, cardinalities, time, profiles, compatibility, and model evolution.

**Authority gate.** Assign field-level ownership, source precedence, manual override, inferred suggestion, review, conflict, transfer, and supersession.

**Ingestion gate.** Specify pull, push, event, static, query, and human sources; credentials, mapping, checkpoint, ordering, idempotency, pagination, quotas, errors, and replay.

**Absence gate.** Distinguish source deletion, rename, permission loss, partial crawl, filter change, outage, missing suspicion, confirmation, tombstone, and historical retention.

**Graph gate.** Type direction, source, time, granularity, confidence, design or runtime status, hyperedge behavior, traversal bounds, and authorization.

**Vocabulary gate.** Govern terms, concept schemes, labels, language, mapping strength, profile requirements, validation, and local extensions.

**Quality gate.** Preserve dimensions, metric definitions, measurements, windows, producers, coverage, certificates, feedback, incidents, limitations, and purpose.

**Projection gate.** Version search, graph, analytics, recommendation, and UI projections; record offsets, rebuild, lag, authorization, and reconciliation.

**Discovery gate.** Apply authorized corpus selection, query parsing, candidate generation, filtering, ranking, diversity, explanation, feedback, and evaluation tests.

**Workflow gate.** Define stewardship state, role, evidence, deadline, notification, escalation, concurrency, audit, exception, and closure.

**Automation gate.** Consume accepted versioned metadata events with authorization, idempotency, staleness, compensation, rate limits, and human review by consequence.

**Protection gate.** Classify metadata and behavioral telemetry; enforce least privilege, field redaction, secure search, tenant isolation, secret handling, retention, audit, and safe export.

**Operations gate.** Measure coverage, freshness, conflicts, connector health, projection lag, discovery outcomes, workflow, SLOs, saturation, cost, and incidents with denominators.

**Recovery gate.** Restore identities, assertions, provenance, events, relations, vocabularies, profiles, policies, workflows, tombstones, and audit; rebuild and reconcile projections before automation.

**Closure gate.** End production, access, ingestion, aliases, search, workflows, automation, credentials, replication, and recovery while preserving required historical interpretation.

### Executable evidence: catalog reconciliation and search eligibility

This Python example inspects six invented catalog records, four relation edges, and a lexical search. It applies simple freshness, lifecycle, and ownership eligibility before ranking.

<!-- bijux-verify: {"id":"catalog-reconciliation-and-search-eligibility","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"catalog_assets=6\nactive_assets=5\ndocumented_assets=6\nowned_assets=5\nstale_assets=1\norphaned_assets=1\nlineage_edges=4\ndangling_edges=1\nsearch_candidates=3\neligible_results=2\ntop_result=orders\n","stderr":""}} -->
```python
assets = {
    "orders": {
        "title": "Orders",
        "description": "Authoritative commerce order records",
        "owner": "commerce",
        "active": True,
        "days_since_observed": 1,
    },
    "payments": {
        "title": "Payments",
        "description": "Settled payment records",
        "owner": "finance",
        "active": True,
        "days_since_observed": 2,
    },
    "customers": {
        "title": "Customers",
        "description": "Customer account records",
        "owner": "customer-platform",
        "active": True,
        "days_since_observed": 3,
    },
    "order_dashboard": {
        "title": "Order Performance",
        "description": "Dashboard for order volume and status",
        "owner": "analytics",
        "active": True,
        "days_since_observed": 4,
    },
    "shipment_events": {
        "title": "Shipment Events",
        "description": "Carrier shipment status events",
        "owner": None,
        "active": True,
        "days_since_observed": 1,
    },
    "legacy_orders": {
        "title": "Legacy Orders",
        "description": "Retired order extract retained for audit",
        "owner": "commerce",
        "active": False,
        "days_since_observed": 90,
    },
}

lineage = [
    ("orders", "customers"),
    ("orders", "payments"),
    ("order_dashboard", "orders"),
    ("legacy_orders", "unknown_archive"),
]

freshness_limit = 30
stale = {
    asset_id
    for asset_id, asset in assets.items()
    if asset["days_since_observed"] > freshness_limit
}
orphaned = {asset_id for asset_id, asset in assets.items() if asset["owner"] is None}
dangling = [(source, target) for source, target in lineage if target not in assets]

query = "order"
candidates = {
    asset_id: asset
    for asset_id, asset in assets.items()
    if query in (asset["title"] + " " + asset["description"]).lower()
}
eligible = {
    asset_id: asset
    for asset_id, asset in candidates.items()
    if asset["active"]
    and asset["owner"] is not None
    and asset["days_since_observed"] <= freshness_limit
}


def rank(asset_id, asset):
    title = asset["title"].lower()
    description = asset["description"].lower()
    exact_identity = asset_id == query + "s"
    return (4 * exact_identity + 2 * title.startswith(query) + int(query in description), asset_id)


ranked = sorted(eligible, key=lambda key: rank(key, eligible[key]), reverse=True)

print(f"catalog_assets={len(assets)}")
print(f"active_assets={sum(asset['active'] for asset in assets.values())}")
print(f"documented_assets={sum(bool(asset['description']) for asset in assets.values())}")
print(f"owned_assets={sum(asset['owner'] is not None for asset in assets.values())}")
print(f"stale_assets={len(stale)}")
print(f"orphaned_assets={len(orphaned)}")
print(f"lineage_edges={len(lineage)}")
print(f"dangling_edges={len(dangling)}")
print(f"search_candidates={len(candidates)}")
print(f"eligible_results={len(eligible)}")
print(f"top_result={ranked[0]}")
```

The expected output reports `catalog_assets=6`, `active_assets=5`, `documented_assets=6`, `owned_assets=5`, `stale_assets=1`, `orphaned_assets=1`, `lineage_edges=4`, `dangling_edges=1`, `search_candidates=3`, `eligible_results=2`, and `top_result=orders` on separate lines.

The evidence is intentionally narrow. The dictionaries do not establish durable identity or assertion provenance. Nonempty descriptions and owners do not prove correctness or current accountability. One fixed freshness threshold does not suit every metadata class. Tuple pairs are asserted as lineage without process, source, time, granularity, or confidence. A missing target can be a permission or ingestion problem rather than a nonexistent resource. The search performs substring matching over unrestricted invented text; production search needs authorization before retrieval, language-aware analysis, stable ranking, privacy, evaluation, and projection reconciliation. The ranking formula contains no real quality or semantic fitness. Production assurance requires source reconciliation, profile validation, authority rules, temporal assertions, protected indexes, curated relevance judgments, adversarial tests, connector failure injection, workflow evidence, projection rebuilds, recovery exercises, and user-outcome measurement.

## Alternatives and Trade-Offs

**Centralized catalog.** A single authority can standardize identity, profiles, search, graph, workflows, and operations. It can become a bottleneck, high-value target, slow path for domain changes, and false owner of local semantics.

**Federated catalog.** Domains retain metadata authority and can evolve locally. Global identity, minimum profiles, cross-domain search, graph resolution, latency, conflicts, security, and exit become harder.

**Hybrid central discovery.** Domains publish governed metadata while a central index stores selected discovery projections. It balances autonomy and fast search but needs explicit staleness, disclosure, and conflict semantics.

**Distributed query.** Search fans out to authoritative domain catalogs. It can return current source views and minimize replication, but tail latency, partial results, inconsistent ranking, and authorization coordination complicate experience.

**Crawler-first ingestion.** Connectors quickly inventory existing systems without application changes. They lag between scans, depend on broad credentials, struggle with intent and semantics, and can mistake permission loss for deletion.

**Producer-push ingestion.** CI or application systems publish intended metadata with context and low latency. Producers can omit, misstate, or stop sending, so periodic inventory and reconciliation remain necessary.

**Event-driven ingestion.** Change and run events support active metadata and near-real-time projection. Event loss, duplication, ordering, schema evolution, and replay require durable design.

**Human curation.** Stewards supply purpose, meaning, ownership, certification, and dispute resolution. Manual work does not scale for technical drift and needs routed workflows, evidence, and attestation.

**Relational canonical store.** Transactions, constraints, temporal tables, and operational familiarity are strengths. Deep graph traversal and flexible entity types may require derived structures or additional engines.

**Graph canonical store.** Relationships are direct and traversals expressive. Transactional history, high-degree performance, indexing, migration, and operational skill can be demanding.

**Search-first storage.** Flexible documents and retrieval make prototypes fast. Search engines are weak authorities for precise constraints, history, concurrency, and complex updates; rebuildable projection is safer.

**Event-log canonical model.** An append-only log supports replay, temporal audit, projections, and subscriptions. Correct snapshots, compaction, privacy deletion, schema evolution, ordering, and operator tooling add complexity.

**Strongly typed metadata model.** It provides stable APIs, validation, discoverability, and tool interoperability. Model evolution and long-tail resource types can be slow.

**Property graph flexibility.** New entities and relations can be added quickly. Without profiles and ownership, inconsistent labels, edge meanings, and attributes produce an unqueryable graph.

**Shared standards and profiles.** DCAT, DCMI, PROV, SKOS, DQV, SHACL, and OpenLineage improve exchange and common semantics. Local platforms still need mappings, profiles, extensions, implementation rules, and evidence about conformance.

**One global taxonomy.** It aids global navigation and policy. It can erase domain nuance and create a central maintenance bottleneck; layered schemes and qualified mappings often preserve more meaning.

**Lexical search.** It is fast, explainable, and predictable for known names and terms. Vocabulary mismatch and multilingual queries reduce recall.

**Semantic vector search.** It improves conceptual recall and natural-language use. It adds model drift, privacy, explainability, cost, authorization, deletion, and relevance-evaluation risk.

**Graph recommendations.** Related resources can be found through lineage, ownership, terms, and co-use. Dense or erroneous graphs amplify noise, popularity, and unauthorized inference.

**Popularity ranking.** Usage can expose operationally proven assets. Feedback loops, bots, dominant teams, stale extracts, and sensitive telemetry make raw counts unsafe proxies for fitness.

**Certification gates.** Review can reduce consequential misuse. Generic badges, slow queues, expiring evidence, and purpose mismatch can create false confidence.

**Policy automation.** Active metadata can reduce response time and consistent enforcement. Stale or inferred metadata can trigger harmful actions, so authority, freshness, compensation, and review thresholds matter.

**Catalog-integrated access.** Users get one discovery-to-request workflow and traceable context. The catalog becomes coupled to identity, policy, provisioning, and revocation systems and must not itself become the final access authority accidentally.

**Open-source platform.** It offers extensibility, source visibility, and ecosystem integrations. Operation, upgrade, security, connector maintenance, and migration remain organizational responsibilities.

**Managed product.** It reduces platform operation and can accelerate connectors and search. Metadata residency, vendor semantics, export completeness, pricing, API limits, identity portability, and exit require evidence.

**Broad metadata retention.** It supports history, impact analysis, audit, and model training. It increases sensitive disclosure, behavioral surveillance, storage, legal, and deletion obligations.

**Minimal current-state catalog.** It reduces cost and exposure. It weakens replay, provenance, dispute resolution, trend analysis, and reconstruction of decisions based on earlier metadata.

## Failure Modes and Misconceptions

**“A catalog is an inventory.”** Inventory is one capability. Discovery, provenance, quality, lineage, meaning, workflows, exchange, active metadata, and lifecycle require a broader architecture.

**“The catalog page is the dataset.”** It is a record about a resource. Confusing them corrupts timestamps, ownership, deletion, access, and provenance.

**“One table equals one dataset.”** Conceptual datasets can span partitions and distributions; one table can contain several governed domains; services and streams complicate the mapping.

**“Name and path are identity.”** Renames, moves, case rules, environment collisions, and recreation make names insufficient without source authority and stable keys.

**“Matching schema means duplicate.”** Two resources with identical fields can have different populations, time, authority, policy, quality, and purpose.

**“The latest crawl is truth.”** Crawls are observations under credentials, filters, pagination, and source availability. Preserve source state and completeness evidence.

**“Missing once means deleted.”** Permission loss, partial scans, failures, filters, or renames can cause absence. Require authoritative events or confirmation.

**“Manual metadata should always win.”** Humans can be stale or unauthorized for technical fields. Precedence must be predicate-specific and evidence-backed.

**“Source metadata should always win.”** Sources rarely own business terms, certification, policy decisions, or steward explanations. Preserve layered assertions.

**“Last write wins resolves conflict.”** Arrival time does not establish authority or effective time. It can let an old retry erase a reviewed assertion.

**“A graph edge is lineage.”** Containment, co-use, similarity, ownership, semantic mapping, and derivation have different meanings. Even derivation needs source and context.

**“Reachability proves impact.”** A path can include inactive, low-confidence, historical, design-only, or false edges. Impact analysis filters and verifies.

**“Column lineage is always more precise.”** Parser approximations, dynamic SQL, wildcards, user functions, and field renames can produce confident-looking false precision.

**“All green quality checks mean good data.”** Checks cover selected dimensions, intervals, and populations. Their absence or success does not prove fitness for every purpose.

**“One quality score is objective.”** Weighting dimensions embeds consumer priorities and can conceal failure. Preserve measurements and purpose.

**“Fresh catalog means fresh data.”** Connector, index, schema, lineage, quality, and data freshness use different clocks.

**“Nonempty owner means accountability.”** A deleted team, inferred frequent user, or generic platform group may not accept support or decision responsibility.

**“Tags are policies.”** Collaborative tags often lack controlled identity, authority, provenance, review, and conflict behavior required for enforcement.

**“Glossary labels provide semantics.”** Meaning belongs to stable concepts and qualified mappings, not matching display strings.

**“Search rank means recommended.”** Ranking optimizes a retrieval objective under available signals. It does not establish certification or fitness.

**“More clicks means better.”** Position bias and feedback loops amplify incumbent assets; automation and curiosity distort counts.

**“Semantic search understands the business.”** Vector similarity is model-dependent statistical proximity. It can retrieve candidates but does not prove equivalence.

**“Filter unauthorized results afterward.”** Counts, timing, autocomplete, snippets, embeddings, relations, and facets can leak hidden resources before filtering.

**“Metadata is not sensitive.”** Names, schemas, lineage, classifications, users, query text, and incidents can expose highly consequential information.

**“The catalog grants access.”** Discovery and workflow context do not replace policy evaluation and provisioning in authoritative access systems.

**“Federation means many connectors.”** Central harvesting is still centralized authority. Federation allocates ownership and supports governed interoperability.

**“Standards remove local modeling.”** Shared vocabularies require application profiles, identity mappings, extensions, validation, and operational rules.

**“Search index is a sufficient backup.”** It can omit history, provenance, workflows, hidden fields, relations, and canonical identity and can contain stale projections.

**“Reindexing fixes metadata.”** It fixes projection derivation only if canonical state and transformations are correct. Source conflicts and bad identity remain.

**“Connector success means coverage.”** A process can succeed after reading zero objects or skipping unauthorized fields. Track expected denominators and partiality.

**“Events eliminate reconciliation.”** Loss, duplication, mapping bugs, policy changes, and projection failures make periodic comparison essential.

**“A central catalog guarantees consistency.”** Separate stores, indexes, graphs, connectors, workflows, caches, and clients can diverge inside one deployment.

**“More assets means more value.”** Duplicate, stale, hidden, unowned, and irrelevant records can increase count while degrading discovery.

**“Clicks are the success metric.”** Users can click wrong results, abandon later, or repeatedly reopen poor pages. Measure qualified selection and outcomes.

**“Deprecation is a banner.”** Producers, access, consumers, aliases, ranking, automation, support, and recovery must change.

**“Deletion should erase every trace.”** Some contexts require restricted provenance or tombstones to interpret history; privacy and legal policy decide what may remain.

**“No searches means safe retirement.”** APIs, saved queries, scheduled jobs, embeddings, exported metadata, and hidden consumers may bypass recorded UI search.

## Worked Examples

### Example 1

A sales dataset is published as a warehouse view, daily Parquet files, and a query API. The catalog gives the conceptual dataset one durable identity, represents three distributions or services, and records distinct freshness, formats, licenses, and access routes. Search finds the dataset; evaluation chooses the appropriate delivery rather than presenting three unexplained duplicates.

### Example 2

A source table disappears from one nightly crawl after a permission change. The connector marks the observation incomplete and advances no deletion watermark. The catalog retains the asset as `missing-suspected`, alerts the connector owner, and confirms the resource through a source administrator before any tombstone or search demotion.

### Example 3

A warehouse renames `finance.rev_daily` to `finance.revenue_daily` while preserving a stable object ID. The catalog keeps resource identity, adds the old path as a time-bounded alias, updates the display name, and preserves historical query and lineage observations under their original timestamps. It does not create a duplicate and merge later by schema similarity.

### Example 4

A steward describes a field as “net booked revenue,” while a crawler supplies the technical comment “amount.” Field-level precedence presents the steward description and preserves the source comment as technical evidence. When the crawler reruns, it updates its assertion without overwriting the steward's separately owned claim.

### Example 5

A quality badge once summarized six checks. The redesigned catalog shows metric identity, computation version, data interval, result time, coverage, owner, and purpose-specific certification. A user sees that completeness passed yesterday but reconciliation failed for one region, avoiding an unjustified global green judgment.

### Example 6

A query event names two input tables and two outputs. Instead of inferring all four input-output pairs, the lineage producer reports the exact process relationships it can justify. The catalog marks parser-inferred field edges separately from observed run datasets and design declarations, allowing impact analysis to filter by confidence and time.

### Example 7

A search for “customer retention” first applies the viewer's metadata visibility policy, then retrieves lexical, glossary, and semantic candidates. Ranking explains endorsed purpose match, current owner, freshness, and quality evidence. A popular deprecated extract is demoted but remains explicitly discoverable for historical migration.

### Example 8

A classifier infers that a new field may contain personal data. The accepted assertion carries model version, confidence, sample policy, and observation time and triggers a review. Until review, it can conservatively restrict exposure under established policy, but it cannot silently remove an existing verified classification when a later inference is absent.

### Example 9

Three domains operate authoritative catalogs and publish a common profile into a central discovery index. Global identity includes domain authority; central search stores approved discovery fields and projection offsets; detailed metadata resolves at the domain. A partial-result marker appears when one domain is unavailable, and policy automation does not treat the result as complete.

### Example 10

A catalog platform migration exports resources, records, assertions, provenance, graph edges, terms, profiles, quality history, workflows, aliases, and tombstones. Shadow ingestion compares identities, search judgments, and authorization. The old catalog remains read-only for rollback until new projections rebuild and historical links resolve; only then are connectors, credentials, events, and recovery paths retired.

## Cross-Program Connections

**Data Engineering.** Catalog connectors observe warehouses, lakes, streams, orchestrators, transformation tools, quality systems, BI, and model platforms. Late data, replay, partitions, CDC, and source migrations determine metadata identity and freshness.

**API and Service Engineering.** Catalog REST, GraphQL, bulk, search, traversal, access, and event interfaces need durable resource models, pagination, conditional mutation, idempotency, errors, rate limits, compatibility, and support windows.

**Platform Engineering.** A catalog is an internal platform with golden paths, self-service, tenancy, paved connectors, ownership boundaries, SLOs, cost allocation, upgrades, and exit. Adoption depends on reducing work inside existing engineering and stewardship flows.

**Information Retrieval.** Tokenization, fields, facets, synonyms, embeddings, candidate generation, learning to rank, relevance judgments, feedback bias, diversity, evaluation, and explanations shape catalog discovery.

**Distributed Systems Engineering.** Connector checkpoints, events, deduplication, ordering, projections, caches, replication, federation, partial results, conflict resolution, failover, and reconciliation are distributed state-management problems.

**Security Engineering.** Metadata enumeration, search leakage, connector privilege, parser exploits, tag-based automation, behavioral telemetry, tenant isolation, audit, and backups create a large protection surface.

**Software Engineering Patterns.** Adapters isolate source APIs, anti-corruption layers preserve local semantics, event sourcing supports replay, materialized views support retrieval, and state machines govern workflows and lifecycle.

**Knowledge Representation.** Typed relations, controlled vocabularies, concept schemes, profiles, provenance, validation, and mappings determine whether the metadata graph supports defensible reasoning instead of visual adjacency.

**Site Reliability Engineering.** Source-to-search latency, projection drift, connector saturation, zero-object success, stale caches, search tail latency, restore, and automation restart need explicit objectives and exercises.

**Governance, Risk, and Compliance.** Catalogs help inventory regulated resources, rights, classifications, owners, quality, lineage, access, and retention. They also create new sensitive aggregations and cannot substitute for accountable policy decisions.

**Human-Computer Interaction.** Search explanations, stale warnings, conflict displays, comparison, workflow burden, accessibility, multilingual labels, feedback, and progressive disclosure affect whether catalog evidence changes decisions.

**Economics and Organization.** Stewardship capacity, connector ownership, domain incentives, platform funding, chargeback, support, and migration cost determine whether catalog completeness is sustainable rather than a short campaign.

## References

1. W3C, [“Data Catalog Vocabulary (DCAT), Version 3”](https://www.w3.org/TR/vocab-dcat-3/), 2024. Retrieved 2026-09-03.
2. W3C, [“Data on the Web Best Practices: Data Quality Vocabulary”](https://www.w3.org/TR/vocab-dqv/), 2016. Retrieved 2026-09-03.
3. W3C, [“PROV-O: The PROV Ontology”](https://www.w3.org/TR/prov-o/), 2013. Retrieved 2026-09-03.
4. W3C, [“SKOS Simple Knowledge Organization System Reference”](https://www.w3.org/TR/skos-reference/), 2009. Retrieved 2026-09-03.
5. Dublin Core Metadata Initiative, [“DCMI Metadata Terms”](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/), 2020. Retrieved 2026-09-03.
6. W3C, [“Shapes Constraint Language (SHACL)”](https://www.w3.org/TR/shacl/), 2017. Retrieved 2026-09-03.
7. OpenLineage, [“Object Model”](https://openlineage.io/docs/spec/object-model/), current specification documentation. Retrieved 2026-09-03.
8. Apache Software Foundation, [“Apache Atlas 2.0.0”](https://atlas.apache.org/2.0.0/index.html), 2019. Retrieved 2026-09-03.
9. OpenMetadata, [“OpenMetadata System Architecture”](https://docs.open-metadata.org/latest/developers/architecture), current documentation. Retrieved 2026-09-03.
10. DataHub Project, [“DataHub Architecture Overview”](https://github.com/datahub-project/datahub/blob/master/docs/architecture/architecture.md), current documentation. Retrieved 2026-09-03.

## Exercises

### Exercise 1

Design a catalog for warehouse tables, streams, object-store collections, APIs, dashboards, models, and data products across five domains. Specify resource identity, catalog records, distributions, services, entities, relations, assertion provenance, profiles, and ownership.

### Exercise 2

The catalog ingests nightly crawls, source events, OpenLineage run events, query logs, CI manifests, and human edits. Design checkpoints, idempotency, ordering, temporal fields, precedence, absence detection, conflict, reconciliation, and replay.

### Exercise 3

Design authorization-aware search and evaluation for analysts, engineers, privacy reviewers, and external partners. Include lexical, semantic, graph, quality, popularity, lifecycle, explanation, feedback, privacy, and relevance evaluation.

### Exercise 4

Three domains want federated catalog authority with global discovery and active-metadata automation. Design identity, profiles, central and local stores, query topology, events, partial results, security, SLOs, conflicts, recovery, and exit.

### Exercise 5

A company must replace its catalog in six months while preserving 400 connectors, two million resources, field lineage, glossaries, quality history, access workflows, automation, and audit. Design inventory, export, mapping, shadowing, migration, rollback, and retirement.

## Answers to the Exercises

### Answer 1

Define a catalog authority and source authorities. Give every resource a key containing source instance, environment, type, and stable native ID; treat paths as time-bounded aliases. Separate conceptual datasets from warehouse, file, stream, and API distributions or services. Give catalog records their own identity and ingestion timestamps. Represent dashboards, charts, models, features, jobs, runs, schemas, fields, metrics, terms, policies, people, teams, domains, products, checks, incidents, and access requests as typed entities.

Type relations such as contains, provides, derives from, consumes, produces, visualizes, trains on, implements, classifies, owns, stewards, conforms to, serves, and supersedes. Every consequential assertion carries source, agent, observation and effective times, method, confidence, authority, and lifecycle. Use profiles per resource class for required identity, description, owner, support, classification, contract, schema, quality, lineage, distribution, and retirement metadata. Domains own meaning and product promises; source systems own physical state; the platform owns catalog operation; policy authorities own verified classifications; consumers supply feedback without gaining authority over source facts.

Model rename, recreation, merge, split, and migration explicitly. Link schema registry versions by immutable authority-qualified identity, glossary terms by stable concept, quality by metric and window, and lineage by design or runtime evidence. Preserve conflict rather than selecting a silent last writer. Measure in-scope coverage by source and field, freshness by metadata class, owner attestation, dangling relations, search success, and user outcomes.

### Answer 2

Create a source-specific ingestion envelope with event ID, source identity, connector and mapping version, checkpoint, source event time, observation time, effective interval, ingestion time, completeness, content digest, trace, and operation. Nightly snapshots establish observed sets and reconcile missed events. Source events provide low latency. OpenLineage preserves job, run, dataset, and facet context. Query logs create observed-use or inferred-lineage assertions. CI manifests declare intended metadata. Human edits create attributed reviewed assertions.

Deduplicate by durable source event or snapshot identity and make accepted changes idempotent. Partition ordered events by stable resource identity where possible; compare source versions and effective times rather than arrival time. Define field-level precedence: physical schema from the source, business description from the steward, verified classification from policy, run facts from lineage instrumentation, observed usage from telemetry. Preserve competing assertions and surface unresolved conflicts. A manual technical override either expires, routes correction upstream, or remains a visible exception.

Mark a resource missing only from a declared complete snapshot. Progress from suspected to confirmed after repeated observations or authoritative tombstone; distinguish permission and connector failures. Reconcile source sets, accepted canonical state, event offsets, search, graph, and automation. Retain raw observations for bounded replay, apply model and mapping versions deterministically, rebuild projections, verify digests and authorization, and prevent old snapshots from overwriting later source events.

### Answer 3

Define visibility separately for resource existence, fields, schema, description, owners, terms, classification, quality, lineage, usage, and access route. Select an authorized corpus before counts, facets, autocomplete, lexical or vector retrieval, related nodes, snippets, and ranking. Test nonmembers, tenant boundaries, renamed and deleted resources, high-degree graphs, embeddings, timing, caches, and exports. External partners receive a separate disclosure profile and index where needed.

Generate candidates through fielded lexical search, controlled-term expansion, semantic retrieval, and bounded typed graph neighborhoods. Filter lifecycle, environment, required ownership, freshness, applicable certification, and access possibility by task. Rank with explainable components rather than one hidden score: title and term match, endorsed purpose, current owner, documentation, quality evidence, support, recency, and usage among a comparable eligible population. Demote but do not conceal deprecated resources needed for migration. Diversify domains and allocate exploration so popularity does not lock out new resources.

The evaluation view exposes meaning, provenance, schema, distributions, services, quality metric and time, design and runtime lineage, policy, incidents, support, and stale or conflicting assertions. Access remains a separate authoritative workflow. Protect search and usage telemetry through minimization, aggregation, retention, purpose limitation, and audit. Evaluate with curated judgments and task completion by role and language, zero results, reformulation, time to qualified selection, stale or wrong selection, access completion, correction, and downstream incidents—not clicks alone.

### Answer 4

Allocate domain authority namespaces and globally resolvable resource identities. Domains own designated resource and semantic assertions; central policy owns minimum classification and exchange controls; the shared platform owns profiles, discovery projection, identity resolution, and interoperability. Each domain validates a versioned common profile, preserves extensions in its namespace, publishes assertion provenance and tombstones, and exposes support and SLOs.

Use a hybrid topology: domain canonical stores and workflows publish accepted change events; a central index and selected graph projection hold authorized discovery fields with source offsets. Detailed or sensitive metadata resolves at the domain. Search reports missing domains and projection staleness. For high-consequence automation, incomplete federation or stale classifications fail according to an explicit safety policy rather than masquerading as a complete absence. Define conflict rules per predicate, retain both assertions, and route disputes to accountable authorities.

Secure service-to-service exchange, end-user delegation, field disclosure, tenant isolation, bulk export, behavioral telemetry, and cross-domain graph traversal. Events include stable identity, version, source, times, operation, schema, ordering key, authorization context, and replay. Set SLOs for domain publication, central projection, query fan-out, partial-result rate, identity resolution, event delivery, and recovery. Back up local canonical state and shared namespace/profile configuration; rebuild central projections and reconcile. Exit requires portable history, assertions, provenance, relations, workflows, aliases, and tombstones plus removal of events, credentials, caches, and recovery dependencies.

### Answer 5

Inventory source authorities, connectors and versions, schedules and checkpoints, entities, identities, aliases, record history, assertions and precedence, fields, schemas, relations and lineage confidence, terms and mappings, profiles, quality metrics and results, policies, workflows, access integrations, search features, embeddings, events, automation subscribers, users, permissions, SLOs, backups, and retention. Classify which old-product behaviors have no target equivalent and decide transformation, preserved extension, or accepted loss before export.

Export original source-native identity, canonical identity, resource and catalog-record history, assertion provenance, typed relations, controlled concepts, quality evidence, workflow state and audit, aliases, tombstones, and raw observations—not only current display pages. Build deterministic mappings and verify counts, referential integrity, content digests, high-degree nodes, time, language, and authorization. Re-run profile validation and keep old decision evidence where engines differ.

Shadow every connector into the new ingestion boundary without granting automation authority. Compare accepted state, absence candidates, search relevance judgments, graph neighborhoods, quality displays, access workflows, events, and privacy. Dual-publish change events with idempotent subscriber handling. Canary domains and roles, record activation, preserve routing rollback, and reconcile projections. Freeze old mutation only after source coverage and workflows move. Then stop old connectors, aliases, notifications, events, automation, credentials, exports, backups, and recovery startup; retain a restricted historical resolver for the governed period and test that disaster recovery cannot reactivate the old catalog.
