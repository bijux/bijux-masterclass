---
module_id: DARCH-085
program: Data Architecture Engineering
level: 2
module_number: 85
title: Data Fabric Concepts
status: complete
last_verified: 2026-09-03
---

# Data Fabric Concepts

## One-Page Review

### Governing question

How should an enterprise connect heterogeneous, distributed data products and systems through shared metadata, semantics, integration, access, governance, and automation capabilities without pretending that one vendor suite, catalog, graph, virtual query layer, or physical copy can become universal truth?

### Essential definitions

- A **data fabric** is an architectural pattern of interoperable data-management capabilities that uses governed metadata and automation to connect distributed data across technologies, locations, and lifecycle stages.
- A **fabric endpoint** is a source, store, stream, pipeline, service, catalog, model, application, or consumer that participates through an identified contract and adapter.
- A **fabric capability** is a reusable service for discovery, metadata, semantics, integration, access, quality, lineage, policy, observability, orchestration, or lifecycle.
- The **data plane** stores, moves, transforms, queries, serves, or consumes data.
- The **metadata plane** collects and connects technical, operational, business, social, policy, quality, and usage observations about data and operations.
- The **control plane** converts authorized intent and metadata into plans, policies, actions, status, and evidence across participating systems.
- A **knowledge graph** represents identified entities and typed relationships with provenance; it is one implementation for connected metadata, not proof of truth or intelligence.
- **Active metadata** is observed metadata used within bounded workflows to recommend, trigger, constrain, or verify action rather than remaining a passive catalog description.
- A **data product** is an owned, versioned, discoverable, addressable, trustworthy, interoperable, secure, and supported data capability for named consumers and purposes.
- A **fabric service contract** defines capability inputs, outputs, identity, semantics, service, policy, evidence, cost, compatibility, and lifecycle.
- A **connector** or **adapter** translates between a fabric contract and an endpoint's protocol, identity, model, capabilities, and failure behavior.
- **Logical access** exposes data through federation or virtualization without requiring every byte to be copied first.
- **Physical integration** moves or materializes data through batch, replication, change capture, streaming, or transformation.
- **Orchestration** coordinates dependent work; **reconciliation** repeatedly drives observed state toward declared intent.
- **Automation authority** defines which metadata-supported actions may be suggested, approved, executed, reversed, or prohibited and by whom.
- **Closure** removes active routes, copies, caches, credentials, policies, metadata assertions, costs, and recovery paths while preserving required evidence and tombstones.

### Central model, mechanism, or theorem

Represent a data fabric as:

`F = (E, M, K, S, I, A, G, O, X, L)`

where `E` is endpoints and identities, `M` metadata collection and synchronization, `K` knowledge and semantic relationships, `S` service and product contracts, `I` integration and orchestration, `A` access and delivery, `G` governance and protection, `O` observation and bounded automation, `X` user experience and economics, and `L` lifecycle, recovery, and closure. A fabric is defensible when these capabilities improve end-to-end user outcomes across heterogeneous endpoints while preserving source authority, explicit contracts, observable effects, and reversibility. Product branding or a connected diagram is insufficient.

### Critical invariants

- Endpoint, asset, product, distribution, schema, term, owner, policy, job, run, decision, observation, recommendation, action, and outcome have separate stable identities.
- Every metadata assertion names source, issuer, collection method, valid time, observation time, confidence where relevant, version, and lineage.
- A shared graph connects qualified assertions; it does not erase conflicting meanings, ownership, uncertainty, or temporal scope.
- Data products and service contracts remain the consumer boundary; internal tables, connector schemas, and graph nodes do not silently become public APIs.
- Integration style follows semantics, latency, consistency, sovereignty, cost, and failure requirements rather than a mandate to move or virtualize everything.
- Control actions require explicit authority, preview, scope, idempotency, rate limits, evidence, failure handling, and reversal or compensation.
- Policy decisions and enforcement effects remain distinct; metadata tags alone do not protect data.
- Unknown endpoints, unsupported capabilities, stale metadata, broken lineage, policy conflicts, and partial actions remain visible.
- Cross-tenant identity, data, metadata, control state, credentials, logs, caches, backups, and recovery are isolated.
- Measures distinguish inventory coverage, metadata freshness, interoperability, automation activity, user success, reliability, cost, risk, and outcomes.
- Recovery restores identity, contracts, policy, current metadata, deletion and hold state, and control authority before automation resumes.
- Retirement closes data- and control-plane effects across all endpoints instead of deleting only a catalog node.

### Common failures

Common failures include buying a product and declaring a fabric; centralizing all data; equating a catalog with integration; equating a graph with truth; ingesting every metadata field without purpose; hiding conflicts through last-write-wins; exposing internal schemas as product contracts; forcing virtualization on operationally unsuitable sources; copying everything into a lake; making connectors privileged permanent backdoors; letting recommendations execute without authority; calling rules or machine learning intelligent; measuring scanned assets instead of useful outcomes; ignoring control-plane outages and metadata poisoning; and retiring a connector while copies, credentials, routes, metadata, and restores remain active.

### Compact example

Ten invented fabric use cases are evaluated against six declared requirements. Four qualify; one each lacks source identity, metadata, a contract, policy, observation, or supported automation. Seven domains, nine endpoints, four integration styles, ten metadata events, and ten decisions are counted. Executable evidence confirms only those declarations and counts. It proves no real metadata accuracy, interoperability, governance, automation safety, performance, value, or beneficial outcome.

### Connections

[DARCH-061](061-metadata-architecture.md), [DARCH-064](064-lineage-architecture.md), [DARCH-066](066-semantic-interoperability.md), [DARCH-068](068-data-catalog-architecture.md), [DARCH-069](069-metadata-apis-and-eventing.md), [DARCH-081](081-data-mesh-principles.md), [DARCH-083](083-self-serve-data-platform-capabilities.md), and [DARCH-084](084-federated-computational-governance.md) establish metadata, provenance, semantics, discovery, eventing, mesh, platform, and policy foundations. [DARCH-086](../ROADMAP.md) next develops active metadata.

## Governing Question

An enterprise may own a warehouse, lakehouse, operational databases, streams, SaaS applications, a catalog, integration tools, policy engines, and semantic models. Adding them to one diagram does not create a fabric. The endpoints can still disagree about identity, meaning, ownership, freshness, policy, and lifecycle while every connector reports green.

The governing question is how to create useful connective tissue without inventing universal control or truth. A durable fabric identifies endpoints and authorities, gathers qualified metadata, exposes stable products and services, chooses integration per workload, embeds governance, observes real effects, and automates only within explicit authority and recovery boundaries.

## Why This Matters

IBM's current [What Is a Data Fabric?](https://www.ibm.com/think/topics/data-fabric) describes data fabric as an architectural approach rather than one piece of software and emphasizes metadata, integration, governance, self-service, and lifecycle across heterogeneous and hybrid environments. The page is vendor-authored, so claimed benefits require independent local evidence.

IBM's [Data and Analytics Data Fabric architecture guide](https://www.ibm.com/think/architectures/patterns/data-fabric) organizes a reference architecture around metadata import, enrichment, cataloging, curation and transformation, and consumption. It illustrates capability decomposition. Its product mappings are options, not universal architecture requirements.

Zhamak Dehghani's [Data Mesh Principles and Logical Architecture](https://martinfowler.com/articles/data-mesh-principles.html) defines mesh as an organizational and architectural operating model based on domain ownership, products, self-service, and federated computational governance. A fabric can provide connective capabilities to a mesh, but it cannot substitute for domain authority, accountable products, or governance legitimacy.

W3C [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/) represents catalogs, datasets, data services, distributions, series, versions, relationships, rights, and qualified attributions. It supports interoperable discovery across catalogs while allowing multiple distributions and publishers. DCAT descriptions do not establish fitness, truth, or operational support.

W3C [PROV-O](https://www.w3.org/TR/prov-o/) represents entities, activities, agents, generation, use, derivation, attribution, association, and delegation. A fabric can preserve where metadata and data assertions came from, which activity transformed them, and which agent acted. Provenance enables assessment but does not make an assertion correct.

W3C [SKOS](https://www.w3.org/TR/skos-reference/) models concept schemes, concepts, labels, semantic relations, collections, and mappings. It can connect domain vocabularies without forcing one enterprise dictionary. Mapping relations express claims that require provenance and scope; similar labels do not prove conceptual identity.

W3C [Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/) represents quality dimensions, metrics, measurements, policies, annotations, and feedback. It supports comparable qualified observations across products. A fabric must still decide identity, computation, sampling, time, consumer purpose, and enforcement.

W3C [SHACL](https://www.w3.org/TR/shacl/) defines shapes for validating RDF graphs and structured validation results. A fabric can validate metadata profiles and relationship constraints. Shape conformance proves the submitted graph met selected shapes under an evaluation, not that source claims or endpoints are healthy.

OpenLineage's [object model](https://openlineage.io/docs/spec/object-model/) defines jobs, runs, datasets, events, and extensible facets. It provides a common runtime lineage envelope across engines. Fabric architecture must still govern stable identity, exact versions, event completeness, retries, corrections, retention, and sensitive facets.

The OpenTelemetry [specification](https://opentelemetry.io/docs/specs/otel/) defines traces, metrics, logs, resources, context propagation, semantic conventions, and protocols. Operational telemetry can correlate user request, fabric service, connector, policy, query, and pipeline effects. It does not replace data lineage or business semantics.

The CloudEvents [specification](https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md) defines a common event envelope with required and optional context attributes and protocol bindings. Metadata and control events benefit from consistent identity, source, type, subject, time, and data schema, while delivery guarantees and domain payload semantics remain local contracts.

The Bitol [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/latest/) provides machine-readable sections for product fundamentals, schema, quality, support, pricing, teams, roles, service levels, and infrastructure. A fabric can profile contracts for discovery and automation without treating document presence as observed product fitness.

The OpenAPI Initiative [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) describes HTTP APIs in a machine-readable form. Fabric capability APIs can publish operations and schemas across portal, CLI, SDK, and automation clients. Operational semantics, authorization, idempotency, service levels, and lifecycle require additional contracts.

The Open Policy Agent [Policy Language](https://www.openpolicyagent.org/docs/policy-language) supports declarative decisions over structured input. A fabric can evaluate shared policy consistently at integration and access points, but must govern policy authority, trusted metadata, enforcement coverage, evidence, and failure modes.

The CNCF [Platforms White Paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/) frames platforms as curated capabilities serving user needs through self-service. A fabric needs the same product discipline: stable capability contracts and paved journeys rather than a portal over disconnected tools and tickets.

NIST's [Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework) organizes outcomes across Govern, Identify, Protect, Detect, Respond, and Recover. A fabric expands connectivity and control-plane reach, so architecture must address governance, protection, detection, incident response, and recovery rather than only discovery and access.

Together these sources support an architecture of interoperable catalogs, provenance, semantics, quality, events, contracts, APIs, policy, platform capabilities, observability, and lifecycle controls. They do not prove that a proposed fabric should exist, that one graph contains truth, or that automation creates value.

## Prerequisites and Retrieval

You should understand data architecture, metadata, catalogs, lineage, semantic models, knowledge graphs, data products, contracts, integration styles, batch, streaming, change capture, APIs, federation, virtualization, identity, policy, quality, observability, distributed systems, platform engineering, automation, security, privacy, cost, incident response, and recovery.

Retrieve data fabric, data mesh, lakehouse, warehouse, endpoint, node, connector, adapter, data plane, metadata plane, control plane, catalog, graph, ontology, glossary, lineage, provenance, active metadata, product, distribution, contract, virtualization, federation, replication, orchestration, reconciliation, recommendation, automation authority, confidence, freshness, drift, evidence, compensation, closure, and tombstone.

As a retrieval test, inspect a diagram whose center is a “unified intelligent metadata graph.” Ask which user outcome it supports; which endpoints and identities are known; who owns each assertion; how conflicts and time are represented; which product contracts consumers use; how data is accessed or moved; which policies are enforced where; what action the graph may authorize; how partial failure appears; how cost and effectiveness are measured; and how deletion survives restore. A central graph answers none of these by itself.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish a data fabric from a vendor suite, catalog, lakehouse, mesh, knowledge graph, virtualization system, or connector collection;
2. define endpoint, data-plane, metadata-plane, control-plane, product, service, and user-experience boundaries;
3. model stable identities, qualified metadata assertions, semantic mappings, provenance, conflicts, freshness, and confidence;
4. select batch, streaming, change capture, replication, API, federation, virtualization, and materialization by workload requirements;
5. design interoperable product, metadata, lineage, quality, policy, telemetry, event, and capability contracts;
6. govern connectors, credentials, tenant isolation, policy enforcement, automation authority, recommendations, and actions;
7. operate topology discovery, reconciliation, drift, partial failure, capacity, service objectives, incidents, and recovery;
8. measure coverage, freshness, interoperability, self-service, automation, reliability, cost, risk, and user outcomes;
9. migrate fragmented data-management tools into a fabric without requiring a dangerous enterprise-wide replacement; and
10. recover and close fabric routes, copies, controls, metadata, credentials, evidence, and costs across heterogeneous endpoints.

## Core Exposition

**Start with outcomes and pain.** Observe how users discover a product, understand meaning, obtain access, integrate it, verify freshness and quality, investigate failure, control cost, satisfy policy, and retire use. Document waiting, duplicated work, broken handoffs, inconsistent tools, uncertainty, and harm.

**Do not begin with a fabric box.** An architectural label can hide a suite procurement, lake migration, catalog rollout, virtualization project, or integration-platform replacement. Define measurable user and operational outcomes before choosing topology and products.

**Inventory the estate as relationships.** Record sources, systems of record, stores, streams, pipelines, services, catalogs, models, products, consumers, owners, authorities, policies, locations, contracts, costs, dependencies, and lifecycle. Preserve unknown and disputed state.

**Give every endpoint stable identity.** A hostname or connector name is not durable identity. Bind endpoint identity to system, environment, tenant, authority, platform, region, interface, capabilities, versions, support, and lifecycle.

**Separate three logical planes.** The data plane handles bytes and records. The metadata plane handles observations and meaning about them. The control plane turns governed intent into plans and actions. They can share infrastructure, but their identities, privileges, failure, evidence, and recovery differ.

**Use products as the consumption boundary.** A product exposes supported distributions, contracts, meaning, quality, service, policy, cost, change, and support. The fabric may connect and automate products, but it should not expose connector tables or graph internals as accidental public interfaces.

**Define fabric capabilities as products.** Metadata search, lineage, policy evaluation, integration, virtualization, quality, and orchestration each need users, jobs, APIs, service objectives, evidence, support, cost, compatibility, and lifecycle. A shared tool without those properties remains shared infrastructure.

**Collect metadata purposefully.** For each field, name the question or action it supports, authoritative source, collector, cadence, freshness need, sensitivity, retention, and failure behavior. Unlimited harvesting increases cost, surveillance, schema coupling, and false confidence.

**Model assertions, not flattened facts.** Represent subject, predicate, object or value, issuer, source, collection method, valid time, observation time, version, confidence, and evidence. Several sources may assert different owners, classifications, schemas, or freshness.

**Preserve temporal meaning.** Current, historical, future-effective, observed, and inferred states differ. A late metadata event should not overwrite a newer state simply because it arrived last. Corrections preserve what was asserted and when.

**Keep source authority qualified.** An operational domain can authoritatively describe transaction meaning while a platform reports runtime location and a privacy authority defines classification rules. No single catalog is universally authoritative for every predicate.

**Use graph structure carefully.** Graphs help traverse product, dataset, schema, job, run, owner, policy, term, consumer, and dependency relations. Identity resolution, edge semantics, provenance, cardinality, time, uncertainty, and authorization determine whether traversal is meaningful.

**Do not infer truth from connectivity.** A highly connected node can be popular, duplicated, erroneous, or over-collected. Page-rank-like importance, similarity, and embeddings are signals with training, bias, drift, and explanation limits.

**Support semantic pluralism.** Domains can retain different meanings for customer, order, exposure, or active. Connect them through qualified mappings, transformations, context, version, loss, and consumer purpose rather than one mandatory enterprise schema.

**Publish metadata profiles.** Define minimum identity, product, contract, schema, owner, policy, quality, lineage, service, support, cost, and lifecycle fields for specific use cases. Version profiles and distinguish structural conformance from observed correctness.

**Choose integration style per need.** Batch supports bounded periodic exchange; streams support event-time change; change capture projects source changes; replication supports local copies; APIs support interaction; virtualization supports query-time composition. Each moves consistency, coupling, cost, sovereignty, and failure differently.

**Treat virtualization as one capability.** It can reduce initial copying and speed exploratory access. Source load, latency, availability, pushdown, semantic mismatch, cross-region transfer, policy, and reproducibility can make physical products preferable.

**Treat movement as a governed copy.** Every replica, cache, extract, index, feature, and materialization gets stable identity, provenance, contract, location, policy, quality, retention, deletion, cost, and owner. “Fabric-managed” does not remove copy accountability.

**Separate orchestration from reconciliation.** Orchestration sequences a bounded workflow. Reconciliation continuously compares desired and observed state and repairs drift. Long-lived connectors, contracts, policies, and routes benefit from reconciliation beyond one successful deployment.

**Design connector contracts.** Declare supported endpoint versions, authentication, discovery, read and write capability, schema mapping, incremental positions, delivery semantics, retries, rate limits, quotas, observability, policy hooks, failure, upgrades, and closure.

**Use least-privilege connector identities.** Separate discovery, metadata read, data read, data write, policy, administration, and deletion. Rotate credentials and bind them to endpoint, tenant, purpose, environment, and time. A universal scanner account is a high-value compromise path.

**Design for partial capability.** One connector may expose schema but not lineage; another lineage but no policy enforcement; another query but no deletion confirmation. Publish capability matrices and refuse unsupported promises rather than normalizing everything to a lowest common fiction.

**Expose stable service APIs.** Portals, CLIs, SDKs, Git workflows, controllers, and automation use the same versioned capability contracts. APIs name desired state, idempotency, conditions, errors, evidence, cost, and lifecycle; UI state is not the system of record.

**Use events for change, not truth.** Metadata events announce observations or lifecycle transitions with source, identity, type, subject, time, schema, sequence context, and idempotency. Consumers reconcile against authoritative state when ordering, duplication, or loss matters.

**Connect technical and business metadata.** Bind physical fields and jobs to product schemas, domain concepts, metrics, purposes, owners, consumers, policies, and decisions through versioned mappings. Avoid attaching one unqualified glossary label and claiming semantic resolution.

**Build end-to-end lineage.** Connect design and runtime lineage across batch, stream, query, API, notebook, ML, manual export, and restore. Record exact input and output versions, transformation identity, run, time, environment, and completeness limits.

**Make quality consumer-aware.** Define dimensions, metrics, units, scope, method, sample, thresholds, time, uncertainty, and consumer decisions. A global score hides whether a particular product is fit for fraud, reporting, operations, or exploration.

**Embed governance at action points.** Evaluate policy when discovering sensitive metadata, granting access, moving data, querying, exporting, deriving, retaining, deleting, and restoring. A catalog tag is an input; a separate enforcement point must control the effect and report evidence.

**Isolate tenants across all planes.** Separate data, metadata, graph queries, control state, identities, credentials, policies, logs, caches, quotas, support, backups, and recovery. Cross-tenant metadata leakage can reveal names, schemas, relationships, and business activity even without row access.

**Treat active metadata as a spectrum.** Passive display, contextual warning, recommendation, proposed plan, approval-gated action, reversible automation, and autonomous action carry increasing authority and risk. Classify each use case explicitly.

**Separate inference from decision.** A model may predict that two fields contain identifiers or that a pipeline should move. Preserve input, model and version, score, uncertainty, explanation, and evaluation. An authorized policy or person decides whether and how to act.

**Bound every automated action.** Name trigger, authority, preconditions, scope, dry run, idempotency, concurrency, rate limit, blast radius, obligations, evidence, timeout, partial-failure handling, reversal or compensation, and escalation.

**Prevent feedback loops.** A classifier changes policy, policy changes access, access changes usage, and usage retrains recommendations. Record causal edges, separate training from evaluation, use holdouts and change control, and watch for self-confirming behavior.

**Protect the metadata supply chain.** Threat-model collectors, agents, event buses, schemas, mapping code, graph loaders, model artifacts, APIs, caches, credentials, and administrative interfaces. Metadata poisoning can redirect data, relax controls, or corrupt impact analysis.

**Make conflicts first-class.** Conflicting owner, schema, classification, term mapping, lineage, or deletion state should carry participating assertions, authorities, times, and resolution status. Last-write-wins is transport behavior, not governance.

**Expose freshness honestly.** Report last observed time, expected cadence, source lag, collector lag, processing lag, and unknown state. A recent catalog timestamp can describe stale source metadata that was merely reindexed.

**Design service objectives end to end.** Measure user discovery and delivery journeys, metadata propagation, policy revocation, route provisioning, query and movement reliability, incident detection, recovery, and closure—not only catalog or connector uptime.

**Control capacity and backpressure.** Scans, lineage events, profiling, graph updates, virtual queries, replication, and automation compete with production workloads. Use quotas, prioritization, sampling, incremental collection, admission, load shedding, and bounded queues.

**Observe control effects.** Correlate request, product, endpoint, connector, plan, policy decision, data operation, metadata event, lineage, cost, and outcome. A successful orchestration run does not prove the consumer received correct governed data.

**Measure useful coverage.** Publish denominators for eligible endpoints, products, distributions, fields, jobs, operations, policies, consumers, and lifecycle states. “Ten million assets scanned” lacks a coverage denominator and a user outcome.

**Measure automation quality.** Separate suggestions, accepted suggestions, approved plans, successful actions, partial actions, reversals, overrides, false positives, false negatives, incidents, time saved, cost shifted, and outcomes. Adoption under mandate is not validation.

**Make economics visible.** Include platform engineering, licenses, connectors, scanning, storage, graph, compute, egress, support, incidents, migrations, domain labor, and opportunity cost. Relate them to reduced lead time, avoided duplication, reliability, risk, reuse, and consumer value.

**Avoid forced tool unification.** Stable identities, contracts, events, policies, and evidence can connect heterogeneous systems. Replacing every endpoint simultaneously creates migration risk and often sacrifices capabilities for superficial consistency.

**Define a canonical minimum, not a canonical universe.** Standardize envelopes and cross-domain invariants needed for interoperability. Let endpoint-specific extensions remain namespaced and typed. Preserve unsupported and loss during translation.

**Plan upgrades and schema evolution.** Version connectors, APIs, events, metadata profiles, graph models, policies, inference models, and product contracts independently. Test compatibility across supported matrices and publish deprecation, migration, rollback, and closure.

**Operate incidents across planes.** Classify data corruption, metadata poisoning, missing lineage, stale policy, credential exposure, connector loops, query overload, cross-tenant leak, wrongful automation, deletion failure, and graph outage. Preserve evidence and affected-product impact.

**Migrate incrementally.** Choose high-value journeys, establish identity and contracts, connect authoritative metadata, add observation, then automate bounded actions. Run old and new paths with reconciliation and explicit ownership until evidence supports cutover.

**Recover control before automation.** Restore endpoint identity, authority, contracts, current policy, secrets, metadata sources, graph provenance, deletion tombstones, holds, exceptions, and action history. Reconcile before enabling movement, grants, or automated repair.

**Retire end to end.** Stop routes and queries, drain work, revoke identities, remove copies and caches, apply retention and deletion, close policies and exceptions, preserve required evidence, stop costs, and ensure restore cannot recreate retired connectivity.

## Definitions and Notation

Let a data fabric be:

`F = (E, M, K, S, I, A, G, O, X, L)`.

Represent an endpoint as:

`e = (id, authority, type, environment, tenant, location, interfaces, capabilities, versions, service, lifecycle)`.

Represent a metadata assertion as:

`m = (subject, predicate, value, issuer, source, method, valid_time, observed_time, version, confidence, evidence)`.

Represent a product distribution as:

`d = (product, interface, schema, semantics, service, policy, quality, lineage, location, cost, support, lifecycle)`.

Represent an integration route as:

`r = (source, target, style, contract, semantics, consistency, latency, policy, evidence, recovery, closure)`.

Represent an automated action as:

`a = (trigger, authority, target, preconditions, plan, idempotency, bounds, obligations, evidence, compensate, status)`.

Define qualified inventory coverage as:

`C_i = endpoints_with_current_required_profile / known_eligible_endpoints`.

Define metadata propagation lag as:

`T_m = usable_observation_time - authoritative_change_time`.

Define automation precision for a reviewed decision class as:

`P_a = correct_actions / reviewed_executed_actions`.

It is undefined without reviewed outcomes and says nothing about harmful omissions. Recall, affected-party consequences, reversal, and cost remain separate.

Let `Impact(x)` contain products, consumers, decisions, policies, copies, and derived outputs linked to endpoint, metadata, connector, or action defect `x` through qualified evidence. It is incomplete when identity, telemetry, or lineage coverage is incomplete.

Define `Closed(e)` to require no active route, query, copy, cache, credential, policy, metadata assertion presented as current, automation rule, consumer, cost, or recovery path remains for retired endpoint `e`, while required history and tombstones remain controlled.

## Mechanisms, Invariants, or Proof Structure

Use the following assurance gates.

**Outcome gate.** Name users, journeys, current pain, desired outcomes, eligible denominators, alternatives, economics, and exit criteria.

**Endpoint gate.** Verify stable identity, authority, tenant, environment, location, interfaces, capabilities, versions, service, support, and lifecycle.

**Plane gate.** Separate data, metadata, control, experience, evidence, privileges, failure, ownership, and recovery.

**Assertion gate.** Preserve subject, predicate, value, issuer, source, method, valid and observation time, version, confidence, and evidence.

**Semantic gate.** Govern concepts, contexts, mappings, transformations, loss, conflicts, language, versions, consumers, and authority.

**Product gate.** Define owner, consumers, purposes, distributions, contract, service, quality, policy, lineage, cost, support, change, and closure.

**Integration gate.** Select style by semantics, latency, consistency, sovereignty, availability, scale, coupling, cost, recovery, and lifecycle.

**Connector gate.** Verify compatibility, least privilege, incremental state, retries, idempotency, rate limits, observability, upgrades, and closure.

**Governance gate.** Bind classification, purpose, access, privacy, security, residency, retention, deletion, audit, exception, and enforcement evidence.

**Automation gate.** Verify inference limits, authority, trigger, preview, preconditions, scope, idempotency, bounds, obligations, evidence, compensation, and escalation.

**Tenant gate.** Isolate data, metadata, graph, control, identities, credentials, policy, logs, caches, quotas, backups, support, and recovery.

**Operations gate.** Define service objectives, capacity, backpressure, drift, conflict, partial failure, upgrades, incidents, cost, and support.

**Evidence gate.** Correlate request, product, endpoint, plan, decision, operation, observation, lineage, cost, outcome, and limitations.

**Migration gate.** Inventory, prioritize journeys, establish identity and contracts, connect metadata, observe, automate gradually, reconcile, and retire old paths.

**Recovery gate.** Restore current authority, identity, contracts, policy, secrets, metadata, tombstones, holds, exceptions, and action history before automation.

**Closure gate.** Remove routes, copies, caches, credentials, policies, current assertions, automation, consumers, costs, and recovery activation while retaining evidence.

### Executable evidence: fabric use-case evaluation

The following program classifies ten invented fabric use cases against six declared requirements.

<!-- bijux-verify: {"id":"fabric-use-case-evaluation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"cases=10\nqualified=4\nmissing_source_identity=1\nmissing_metadata=1\nmissing_contract=1\nmissing_policy=1\nmissing_observation=1\nunsupported_automation=1\ndomains=7\nendpoints=9\nintegration_styles=4\nmetadata_events=10\ndecision_events=10\n","stderr":""}} -->
```python
cases = [
    {"domain": "orders", "endpoint": "orders-db", "style": "cdc", "source": True, "metadata": True, "contract": True, "policy": True, "observed": True, "automation": True},
    {"domain": "risk", "endpoint": "risk-stream", "style": "stream", "source": True, "metadata": True, "contract": True, "policy": True, "observed": True, "automation": True},
    {"domain": "science", "endpoint": "feature-store", "style": "batch", "source": True, "metadata": True, "contract": True, "policy": True, "observed": True, "automation": True},
    {"domain": "finance", "endpoint": "warehouse", "style": "virtual", "source": True, "metadata": True, "contract": True, "policy": True, "observed": True, "automation": True},
    {"domain": "marketing", "endpoint": "campaign-saas", "style": "batch", "source": False, "metadata": True, "contract": True, "policy": True, "observed": True, "automation": True},
    {"domain": "support", "endpoint": "case-api", "style": "virtual", "source": True, "metadata": False, "contract": True, "policy": True, "observed": True, "automation": True},
    {"domain": "orders", "endpoint": "orders-lake", "style": "batch", "source": True, "metadata": True, "contract": False, "policy": True, "observed": True, "automation": True},
    {"domain": "identity", "endpoint": "identity-db", "style": "cdc", "source": True, "metadata": True, "contract": True, "policy": False, "observed": True, "automation": True},
    {"domain": "risk", "endpoint": "warehouse", "style": "batch", "source": True, "metadata": True, "contract": True, "policy": True, "observed": False, "automation": True},
    {"domain": "science", "endpoint": "research-files", "style": "batch", "source": True, "metadata": True, "contract": True, "policy": True, "observed": True, "automation": False},
]

def evaluate(case):
    if not case["source"]:
        return "missing_source_identity"
    if not case["metadata"]:
        return "missing_metadata"
    if not case["contract"]:
        return "missing_contract"
    if not case["policy"]:
        return "missing_policy"
    if not case["observed"]:
        return "missing_observation"
    if not case["automation"]:
        return "unsupported_automation"
    return "qualified"

results = [evaluate(case) for case in cases]
print(f"cases={len(cases)}")
for outcome in ["qualified", "missing_source_identity", "missing_metadata", "missing_contract", "missing_policy", "missing_observation", "unsupported_automation"]:
    print(f"{outcome}={results.count(outcome)}")
print(f"domains={len({case['domain'] for case in cases})}")
print(f"endpoints={len({case['endpoint'] for case in cases})}")
print(f"integration_styles={len({case['style'] for case in cases})}")
print(f"metadata_events={len(cases)}")
print(f"decision_events={len(results)}")
```

The output reports ten use cases, four qualified and one of each declared failure, seven domains, nine endpoints, four integration styles, ten metadata events, and ten decisions.

The evidence is deliberately narrow. Invented Booleans and strings do not establish real identity, metadata accuracy, contracts, policy enforcement, observability, automation safety, interoperability, reliability, cost, value, or outcome. Production assurance requires authoritative assertions, endpoint tests, contract compatibility, enforcement receipts, telemetry and lineage coverage, automation review, incidents, cost evidence, and user outcomes.

## Alternatives and Trade-Offs

**Suite-centered fabric.** Integration and operations can arrive quickly. Product boundaries, lock-in, capability gaps, and vendor-wide failure become important.

**Composable fabric.** Best-fit capabilities and replacement are possible. Identity, contracts, interoperability, and operational responsibility become harder.

**Central metadata graph.** Traversal and enterprise discovery improve. Concentration, stale assertions, access control, and false truth can grow.

**Federated metadata.** Authority and local capability remain near sources. Cross-domain query, synchronization, mapping, and completeness become difficult.

**Virtual access.** Initial delivery avoids copies. Source load, latency, availability, policy, and reproducibility constrain use.

**Materialized products.** Performance, isolation, and repeatability improve. Copies, staleness, cost, retention, and deletion expand.

**Universal connector model.** Common operations simplify clients. Endpoint-specific capabilities and failure semantics can be erased.

**Capability-specific contracts.** Semantics remain honest. Clients and operators manage a larger compatibility matrix.

**Broad metadata harvesting.** Future questions may be answerable. Cost, surveillance, noise, coupling, and breach impact increase.

**Purpose-bound collection.** Risk and cost shrink. New use cases can require additional collection and history may be absent.

**Rules-based automation.** Decisions are more inspectable. Complex patterns and adaptation require manual modeling.

**Model-assisted automation.** Classification and recommendation can scale. Drift, bias, opacity, evaluation, and feedback loops require controls.

**Central orchestration.** Dependency visibility improves. The orchestrator becomes a bottleneck and shared failure domain.

**Event choreography.** Endpoints remain autonomous. Global progress, compensation, debugging, and closure become harder.

**One semantic model.** Some cross-domain queries simplify. Local meanings, change autonomy, and unavoidable conflicts are flattened.

**Qualified mappings.** Domain semantics remain explicit. Consumers bear translation, ambiguity, and mapping governance.

**Automatic repair.** Drift can close quickly. Wrong inference or stale intent can amplify harm.

**Approval-gated action.** Human authority and preview improve. Queues, fatigue, inconsistent decisions, and delay can return.

**Full-fidelity evidence.** Investigation improves. Sensitive metadata, retention, access, and cost exposure increase.

**Minimal evidence.** Risk and cost decline. Correction, replay, assurance, and accountability may become inadequate.

## Failure Modes and Misconceptions

1. **“Buying a data-fabric product creates a fabric.”** Architecture, contracts, authority, and operations remain local work.
2. **“A fabric is one storage system.”** It connects heterogeneous endpoints without requiring one store.
3. **“A fabric requires no physical movement.”** Some workloads need materialization, replication, or streaming.
4. **“A fabric moves everything centrally.”** Universal copying creates gravity, cost, and lifecycle risk.
5. **“A catalog is a fabric.”** Discovery alone does not provide integration, access, enforcement, or lifecycle.
6. **“A knowledge graph is a fabric.”** It is one representation within a broader system.
7. **“A connected graph is enterprise truth.”** Edges are qualified assertions with authority, time, and uncertainty.
8. **“More metadata is always better.”** Unbounded collection raises noise, surveillance, cost, and coupling.
9. **“A recent index is fresh metadata.”** The underlying source observation can still be stale.
10. **“Last write wins resolves conflict.”** Arrival order does not establish truth or authority.
11. **“One glossary term unifies semantics.”** Context, version, mapping, and decision purpose matter.
12. **“Similar field names identify the same concept.”** Labels are not stable semantic identity.
13. **“An ontology proves facts.”** It structures claims and relations; evidence and authority remain separate.
14. **“Lineage means a line between tables.”** Runs, versions, transformations, time, and completeness are required.
15. **“A quality score proves fitness.”** Consumers need dimensions, methods, time, thresholds, and purpose.
16. **“Every table should become a product.”** Products require ownership, consumers, contracts, service, and lifecycle.
17. **“Connector schemas are product contracts.”** They expose implementation details and can change independently.
18. **“A connector supports an endpoint completely.”** Discovery, read, write, lineage, policy, and deletion capabilities differ.
19. **“A successful connection proves correctness.”** Authentication says nothing about semantic mapping or effects.
20. **“One scanner identity is operationally convenient.”** It creates excessive privilege and blast radius.
21. **“Virtualization eliminates data gravity.”** Queries still incur source, network, latency, and availability costs.
22. **“Virtual queries are always current.”** Source snapshots, caches, transactions, and clocks define currency.
23. **“Copies are just implementation details.”** They create authority, policy, retention, deletion, and cost obligations.
24. **“Batch is obsolete in a fabric.”** Bounded periodic exchange remains appropriate for many semantics.
25. **“Streaming makes data real time.”** Event time, delay, disorder, processing, and serving determine freshness.
26. **“One integration style should be paved.”** Workloads require different trade-offs and failure models.
27. **“Orchestration eliminates distributed failure.”** Partial completion and compensation remain.
28. **“A successful workflow means desired state persists.”** Drift requires reconciliation after execution.
29. **“Metadata events are authoritative state.”** Events can be late, duplicated, lost, or superseded.
30. **“A common envelope defines payload semantics.”** Domain meaning and compatibility need separate contracts.
31. **“A policy tag enforces protection.”** Enforcement points must control actual operations.
32. **“Governance belongs only in the catalog.”** Movement, query, derivation, retention, deletion, and restore need controls.
33. **“Data isolation protects metadata.”** Names, schemas, lineage, usage, and relationships can leak separately.
34. **“A recommendation is harmless.”** It can steer users, expose sensitive facts, or become de facto policy.
35. **“Model confidence is decision authority.”** A score does not authorize an action.
36. **“Automation proves intelligence.”** Rules, heuristics, and models can automate errors.
37. **“A reversible API makes an action reversible.”** Downstream disclosures and deletions may not be undoable.
38. **“Retries make control actions reliable.”** Non-idempotent effects can duplicate or conflict.
39. **“Automatic repair is always desirable.”** Stale intent can repeatedly recreate harmful state.
40. **“More automation means a more mature fabric.”** Safe user outcomes, not autonomy level, determine value.
41. **“Connector uptime is fabric reliability.”** End-to-end products and user journeys can still fail.
42. **“Asset count measures coverage.”** Eligible denominators, required fields, freshness, and usefulness matter.
43. **“Search clicks measure adoption.”** They do not establish successful governed use.
44. **“One composite score shows fabric health.”** Reliability, quality, cost, risk, and value require separate interpretation.
45. **“Vendor neutrality eliminates lock-in.”** Contracts, graph models, APIs, skills, and operational state can still couple.
46. **“Replacing every tool ensures consistency.”** Simultaneous migration concentrates risk and can lose capabilities.
47. **“Recovery starts with reconnecting endpoints.”** Current authority, policy, deletion, and secrets must be restored first.
48. **“Restored metadata is current metadata.”** Backup time and source changes create stale assertions.
49. **“Deleting a graph node retires an endpoint.”** Routes, copies, credentials, consumers, and costs may remain.
50. **“Stopping a connector closes the fabric path.”** Caches, exports, policies, automation, and recovery can revive it.

## Worked Examples

### Example 1

Orders exposes a supported product through a stream and daily files. The fabric connects both distributions under one product identity while preserving distinct schemas, freshness, service, costs, and consumer contracts rather than merging them into one endpoint fiction.

### Example 2

Two catalogs assert different owners for a risk product. The graph keeps both assertions with issuers and valid times, marks the conflict, and routes resolution to the product authority. It does not select whichever crawler ran last.

### Example 3

A consumer needs interactive queries over current operational data. Virtualization meets latency initially, but source load and outage coupling violate service objectives. The architecture materializes a governed projection and preserves provenance to the authoritative source.

### Example 4

A source column changes classification. A metadata event triggers impact analysis and a proposed policy update. A steward reviews affected products and consumers before enforcement changes. The event is a trigger, not authority to revoke or grant access by itself.

### Example 5

A connector discovers schemas but cannot emit runtime lineage. The capability matrix exposes that limitation, and pipelines add OpenLineage instrumentation. The fabric avoids presenting inferred design relationships as complete execution evidence.

### Example 6

A model predicts that two fields are direct identifiers with scores of 0.91 and 0.63. Both assertions preserve model version and evidence; the higher-consequence product requires human confirmation before classification changes trigger masking and deletion duties.

### Example 7

A retry after timeout repeats a non-idempotent access-grant call. The first call succeeded but its receipt was delayed. A stable action identity and endpoint reconciliation detect the existing grant and prevent duplicated or broader permissions.

### Example 8

Tenant A can search only its authorized product and metadata graph partitions. Query planning, logs, caches, lineage, connector credentials, support tools, backups, and recovery are tested for isolation, not merely the data tables.

### Example 9

A fabric dashboard reports 98 percent connector uptime while consumer delivery success is 84 percent. Correlated telemetry reveals contract mismatches and policy timeouts downstream. Endpoint health had concealed the user failure.

### Example 10

Retiring a SaaS endpoint stops ingestion, drains routes, revokes discovery and data credentials, deletes governed copies, closes exceptions, removes current assertions, preserves historical provenance, ends licenses, and tests that disaster recovery cannot recreate the connector.

## Cross-Program Connections

- [Data Engineering](../../19-data-engineering/ROADMAP.md) owns implementation of movement, transformation, orchestration, quality, lineage emission, and operational data products.
- [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md) owns storage, streaming, indexing, query, graph, consistency, scale, and multi-tenant engine behavior.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) owns database access, schema, transactions, change capture, query planning, replication, backup, restore, and deletion mechanics.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) owns capability APIs, contracts, identity propagation, idempotency, pagination, errors, compatibility, and service operation.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns self-service experience, control planes, connectors as products, paved paths, observability, supply chain, capacity, and recovery.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns threat modeling, identity, secrets, least privilege, isolation, policy enforcement, detection, and incident response.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies reasoning about partial failure, clocks, delivery, convergence, idempotency, partitions, and compensation.
- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) owns service boundaries, interface stability, dependency direction, composition, evolution, and architectural fitness.
- [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns contract, integration, property, fault, compatibility, and end-to-end verification strategies.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies stakeholder, lifecycle, assurance, hazard, recovery, and emergent-risk reasoning across the entire fabric.

## References

1. IBM, [What Is a Data Fabric?](https://www.ibm.com/think/topics/data-fabric), architectural approach, metadata, integration, governance, access, and lifecycle.
2. IBM, [Data and Analytics Data Fabric](https://www.ibm.com/think/architectures/patterns/data-fabric), reference-architecture capability decomposition.
3. Zhamak Dehghani, [Data Mesh Principles and Logical Architecture](https://martinfowler.com/articles/data-mesh-principles.html), domain products, platform, and federated governance.
4. W3C, [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/), catalogs, datasets, services, distributions, versions, and attribution.
5. W3C, [PROV-O](https://www.w3.org/TR/prov-o/), provenance entities, activities, agents, and qualified relations.
6. W3C, [SKOS Reference](https://www.w3.org/TR/skos-reference/), concepts, schemes, labels, semantic relations, and mappings.
7. W3C, [Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/), quality dimensions, metrics, measurements, policies, and annotations.
8. W3C, [Shapes Constraint Language](https://www.w3.org/TR/shacl/), graph constraints and validation results.
9. OpenLineage, [Object Model](https://openlineage.io/docs/spec/object-model/), jobs, runs, datasets, events, and facets.
10. OpenTelemetry, [Specification](https://opentelemetry.io/docs/specs/otel/), telemetry signals, resources, context, semantics, and protocols.
11. CloudEvents, [Specification](https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md), common event context and protocol-neutral envelope.
12. Bitol, [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/latest/), machine-readable product contract sections.
13. OpenAPI Initiative, [OpenAPI Specification](https://spec.openapis.org/oas/latest.html), machine-readable HTTP API descriptions.
14. Open Policy Agent, [Policy Language](https://www.openpolicyagent.org/docs/policy-language), declarative decisions over structured data.
15. CNCF Application Delivery Technical Advisory Group, [Platforms White Paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/), platforms as user-centered capability collections.
16. NIST, [Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework), Govern, Identify, Protect, Detect, Respond, and Recover outcomes.

## Exercises

### Exercise 1

Define a data-fabric target architecture for an estate containing operational databases, SaaS systems, streams, a warehouse, a lakehouse, notebooks, and partner APIs. Specify outcomes, planes, endpoint identities, capabilities, products, contracts, topology, and exclusions.

### Exercise 2

Design a metadata and knowledge model for products, distributions, schemas, terms, owners, jobs, runs, policies, quality, consumers, and costs. Include authority, provenance, time, conflict, confidence, events, profiles, and access control.

### Exercise 3

Choose integration styles for four workloads: interactive operational lookup, regulated daily reporting, low-latency fraud events, and exploratory historical analysis. Compare virtualization, APIs, batch, streaming, replication, and materialization across semantics, service, policy, cost, and recovery.

### Exercise 4

Design one active-metadata automation that reacts to a classification change. Specify trigger, inference, authority, preview, policy, action, idempotency, bounds, evidence, partial failure, compensation, appeal, and effectiveness measures.

### Exercise 5

Plan migration from independent catalog, ETL, virtualization, quality, lineage, and policy tools into a coherent fabric. Include identity, contracts, interoperability, staged journeys, parallel operation, incident handling, recovery, and retirement.

## Answers to the Exercises

### Answer 1

Begin with discovery-to-use, change-impact, governed-delivery, and retirement journeys. Identify every endpoint by authority, tenant, environment, region, interface, capability, version, service, and lifecycle. Separate data, metadata, control, experience, and evidence planes. Expose owned products and reusable catalog, lineage, quality, policy, integration, access, and orchestration capabilities through stable contracts. Exclude universal storage, one enterprise schema, and automatic action without authority. Define end-to-end service, cost, recovery, and exit before selecting vendor components.

### Answer 2

Use stable identities for every entity and represent metadata as qualified assertions with issuer, source, method, valid time, observation time, version, confidence, and evidence. Type relationships such as distribution-of, produced-by, consumes, governed-by, measured-by, owned-by, maps-to, and derived-from. Preserve conflicting assertions and route them to named authorities. Publish versioned profiles and events, reconcile against authoritative sources, restrict sensitive graph paths, and distinguish declared contracts from observed runs, measurements, and effects.

### Answer 3

Use a purpose-built API or governed virtual access for operational lookup if source load and availability meet the service contract. Materialize an immutable, reproducible daily product for regulated reporting with source cutoffs, quality, lineage, retention, and replay. Use a versioned event stream for fraud with event time, ordering, deduplication, schema, backpressure, and recovery. Use governed snapshots or lakehouse products for historical exploration so exploratory load and reproducibility do not depend on every source being online. Record why each style fits and how consumers migrate.

### Answer 4

A qualified classification assertion triggers impact analysis, not immediate mutation. Preserve classifier or issuer, version, score, evidence, and affected products. An authorized policy decides required changes. Preview proposed masking, access, retention, and notification actions with blast radius. Execute under stable action identity, least privilege, rate and concurrency bounds, receipts, and per-endpoint conditions. Compensate reversible changes; escalate irreversible partial effects. Measure decision accuracy, coverage, time to protection, false blocks, reversals, incidents, appeal, cost, and affected outcomes.

### Answer 5

Inventory tools, endpoints, identities, schemas, APIs, events, policies, credentials, data copies, owners, consumers, costs, and restore paths. Define a canonical minimum for identity, product contracts, metadata assertions, events, policy decisions, telemetry, and lineage while preserving namespaced extensions. Deliver a few high-value journeys end to end, reconcile parallel representations, and expose gaps. Migrate by cohorts with compatibility tests, rollback, and incident procedures. Retire old paths only after consumers, data, metadata, credentials, licenses, policies, exceptions, and recovery activation are closed and required evidence retained.
