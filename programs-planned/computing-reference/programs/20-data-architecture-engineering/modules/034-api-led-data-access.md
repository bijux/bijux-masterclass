---
module_id: DARCH-034
program: Data Architecture Engineering
level: 1
module_number: 34
title: API-Led Data Access
status: complete
last_verified: 2026-09-03
---

# API-Led Data Access

## One-Page Review

### Governing question

When should an organization expose data through governed APIs, and how can it preserve domain authority, consumer fitness, time semantics, protection, reliability, discoverability, changeability, and lifecycle without turning operational services into accidental bulk-export systems or an API gateway into the owner of data meaning?

### Essential definitions

- An **application programming interface (API)** is a governed interaction boundary through which a provider offers operations and representations to authorized consumers under an explicit contract.
- **API-led data access** makes an API the supported access path for named data products, queries, commands, or derived views rather than permitting consumers to depend on private storage structures.
- A **resource** is an identified conceptual target whose representations can be transferred; it is not synonymous with a database row.
- A **representation** is a versioned encoding of resource state or an operation result for a declared media type and context.
- A **system-facing API** contains endpoint-specific or source-system concerns; a **domain or process API** expresses governed business capabilities; a **consumer-facing API** shapes access for a bounded use. These are responsibilities, not mandatory layers.
- **Projection** selects a bounded subset or view of fields; **filtering** selects qualifying members; **pagination** divides a result sequence into retrievable pages under declared ordering and consistency.
- A **snapshot contract** states which effective point or interval a multi-request read represents and how concurrent changes affect it.
- **Conditional request** semantics allow a client to act on validators such as entity tags or modification dates and avoid unnecessary transfer or lost updates.
- **Rate limiting** bounds admitted work; **quota** allocates permitted work over a declared scope and period. Neither substitutes for capacity engineering or consumer prioritization.
- **API retirement** closes operations, versions, clients, credentials, gateway rules, caches, copies, telemetry, documentation, and support after evidence of safe migration.

### Central model, mechanism, or theorem

Represent an API data boundary as:

`A = (product, resources, operations, representations, semantics, time, contract, service, protection, observability, ownership, change, lifecycle)`

An API is appropriate when consumers need bounded, governed interaction with current or explicitly historical state and the provider can support the resulting workload and lifecycle. It is not automatically appropriate for bulk extraction, complete history, high-volume event propagation, offline analytics, or cross-source computation. The protocol exposes an access mechanism; the data architecture must still define authority, grain, keys, time, quality, correction, permitted use, and consumer outcome.

### Critical invariants

- Every operation identifies its provider, product, purpose, resource or action semantics, authority, consumers, versions, service, protection, and owner.
- Resources express durable domain concepts and capabilities rather than leaking private tables, joins, storage keys, or deployment topology.
- Representations declare keys, grain, units, codes, nulls, classification, provenance, schema, examples, and information omitted or derived.
- Collection reads define filtering, ordering, pagination, snapshot or drift behavior, limits, and deletion or late-arrival effects.
- Time semantics distinguish business-effective, observed, transaction, publication, cache, and request time; “current” has a declared boundary.
- Errors, validation, idempotency, concurrency, retries, rate limits, quotas, and degraded behavior are machine-readable and operationally tested.
- End-to-end objectives cover consumer-visible availability, latency, freshness, completeness, correctness, recovery, correction, and support—not gateway uptime alone.
- Authentication, authorization, purpose, minimization, field and row access, logging, caching, retention, residency, and deletion apply to every response and copy.
- Compatibility decisions consider semantic and behavioral change as well as additive schema syntax, with consumer evidence and bounded deprecation.
- Bulk, event, file, query, or product alternatives remain available when API access cannot responsibly satisfy workload, history, latency, or consistency needs.

### Common failures

Common failures are wrapping database tables and calling them resources; making the gateway own domain semantics; returning every field by default; using offset pagination over a changing collection without declaring drift; confusing response time with data freshness; promising “real time” without an observation boundary; using HTTP 200 for application failures; retrying non-idempotent requests; publishing schemas without examples or meaning; breaking clients through changed defaults; treating authentication as purpose authorization; logging protected payloads; allowing bulk clients to exhaust transactional capacity; using one API for current state and complete history without explicit temporal design; and removing documentation while unknown clients, credentials, caches, and exports remain.

### Compact example

A Customer domain replaces direct reporting queries against its operational tables with a source-aligned Customer API. Stable customer identifiers, effective status time, field classifications, conditional reads, cursor pagination, error details, per-purpose authorization, and freshness objectives become explicit. The API offers bounded current-state queries; a governed snapshot product serves nightly analytics, and events notify subscribers of changes. Consumers stop coupling to tables without forcing every access pattern through synchronous calls.

### Connections

[DARCH-027](027-producer-and-consumer-contracts.md) defines provider-consumer obligations, while [DARCH-031](031-point-to-point-integration-and-its-costs.md), [DARCH-032](032-hub-and-spoke-integration.md), and [DARCH-033](033-enterprise-service-bus.md) establish direct and mediated alternatives. This module precedes [DARCH-035](../ROADMAP.md) on event-driven integration, [DARCH-037](../ROADMAP.md) on batch and file exchange, and [DARCH-040](../ROADMAP.md) on choosing from semantics and latency.

## Governing Question

An API can protect an operational system from private-schema coupling and give consumers a stable, observable, authorized contract. It can also encourage synchronous fan-out, conceal stale data behind fast responses, or become an inefficient extraction path when the workload really needs events, snapshots, files, or analytical serving.

The governing question is therefore not “Can this data be exposed by API?” Almost any data can. It is “Does a governed interaction boundary fit the assertions, temporal semantics, volume, consistency, latency, consumer purpose, protection, ownership, and lifecycle of this access need?”

## Why This Matters

Database tables are implementation structures. When consumers query them directly, a provider cannot change normalization, indexes, storage engines, or internal identifiers without coordinating external users. An API can replace physical coupling with an explicit resource and operation contract. That gain exists only if the API itself has durable semantics and lifecycle governance.

[RFC 9110](https://www.rfc-editor.org/rfc/rfc9110) defines HTTP semantics, including methods, status codes, content, conditional requests, and caching concepts. The [OpenAPI Specification 3.1.1](https://spec.openapis.org/oas/v3.1.1.html) describes HTTP APIs in a machine-readable form. These support precise interface contracts but do not decide which domain assertions to expose.

[JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/json-schema-core.html) supplies a vocabulary for validating JSON structure and instances. [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457) defines problem details for HTTP APIs. Structural validation and standard error representations improve interoperability, while semantic correctness and recovery still require product-specific rules.

[OAuth 2.0, RFC 6749](https://www.rfc-editor.org/rfc/rfc6749) specifies an authorization framework. Authentication and scopes are mechanisms within a larger authorization decision that includes purpose, subject, fields, relationships, policy, and context.

The W3C [Data on the Web Best Practices](https://www.w3.org/TR/dwbp/) addresses data formats, identifiers, metadata, access, versioning, provenance, quality, preservation, and reuse. Google's [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/) explains overload propagation, retry amplification, and defensive controls. NIST [SP 800-160 Volume 1 Revision 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) frames trustworthy security as a lifecycle engineering concern.

## Prerequisites and Retrieval

You should understand data products, domains, service contracts, HTTP, schemas, identity and authorization, distributed failure, caches, consistency, pagination, quality, lineage, provenance, APIs, events, batch movement, service objectives, privacy, and lifecycle.

Retrieve resource, representation, operation, method, media type, schema, key, grain, effective time, publication time, request time, projection, filter, sort, cursor, offset, page, snapshot, validator, entity tag, conditional request, cache, idempotency, rate limit, quota, backpressure, problem details, scope, purpose, version, compatibility, deprecation, and retirement.

As a retrieval test, inspect “GET `/customers` returns customer data in real time.” Ask which customer concept, source authority, key, grain, fields, time, ordering, pagination, snapshot, filter, schema, freshness, cache, authorization, purpose, limit, error, history, quality, owner, and version apply. The route and verb alone are not a data contract.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish API-led data access from private database access, bulk transfer, event publication, and federated query;
2. model APIs through products, resources, operations, representations, semantics, time, contracts, service, protection, ownership, and lifecycle;
3. design domain-oriented resources without exposing private storage or forcing all consumers into one representation;
4. specify keys, grain, fields, projections, filters, ordering, pagination, snapshots, caching, and temporal behavior;
5. apply HTTP methods, status codes, conditional requests, media types, problem details, schemas, and examples within their actual guarantees;
6. design authentication, authorization, purpose limitation, minimization, field and row controls, logging, and response-copy governance;
7. engineer capacity, rate limits, quotas, timeouts, retries, idempotency, concurrency, isolation, and degraded behavior;
8. define consumer-visible freshness, quality, availability, latency, correction, recovery, and support evidence;
9. evolve versions and semantics with compatibility analysis, consumer tests, notice, migration, and verified retirement;
10. select APIs, events, snapshots, files, replication, and analytical products from workload and semantic evidence rather than fashion.

## Core Exposition

**Start with the access need.** Record the consumer, decision or workflow, assertions, freshness, history, volume, latency, consistency, availability, protection, and expected lifetime. Do not begin with a route name or gateway product.

An API fits bounded interactions in which a provider can answer or act within an explicit request contract. Repeated scans of millions of records for offline analysis often belong in a snapshot, file, query-serving product, or replicated analytical store.

**Identify the product boundary.** The API should expose a governed source-aligned, aggregate, or consumer-aligned product. Name which team owns meaning, quality, service, correction, and change.

A gateway may authenticate, authorize, route, meter, and observe. It does not become the source of truth. Generated API descriptions do not replace accountable product ownership.

**Model resources by durable meaning.** A resource is a conceptual target such as Customer, Order, or Account Balance under a bounded context. It need not map one-to-one to a table, object, or service instance.

Choose identifiers that remain stable across storage reorganizations. Expose relationships and actions deliberately. Avoid endpoints whose names reveal shards, internal joins, batch stages, or temporary application structure.

**Separate queries and commands.** A query retrieves a representation without requesting a domain state change. A command asks the provider to perform an action and carries validation, authorization, idempotency, outcome, and correction semantics.

HTTP method properties help clients and intermediaries, but domain effect still needs definition. A nominally idempotent method can invoke non-idempotent downstream behavior if implemented carelessly.

**Define representation grain.** State what one representation describes: one customer at a valid time, one order line, one daily balance, or one aggregate. Declare keys and relationship cardinality.

Ambiguous grain causes duplicates and invalid joins. If a collection mixes current objects and historical revisions, expose that distinction through resources, parameters, or separate products.

**Define fields as assertions.** Each material field needs meaning, source authority, type, unit, code set, null semantics, effective time, quality, classification, and limitations. A JSON property name is not a business definition.

Distinguish absent, unknown, not applicable, withheld, and empty where consequences differ. Do not infer meaning from nullable syntax alone. Publish examples that include boundaries and exceptional cases.

**Use schemas within their limits.** JSON Schema can constrain types, shapes, ranges, enumerations, and composition. OpenAPI can associate schemas with operations, parameters, responses, and security descriptions.

Structural conformance does not prove authority, timeliness, completeness, or consumer fitness. Bind schemas to glossaries, contracts, versions, examples, quality evidence, and owners.

**Offer projections deliberately.** Field selection can reduce transfer and exposure, but it increases query planning, authorization, cache, and compatibility complexity. Define allowed projections and whether derived fields carry additional cost or freshness.

Minimize default representations. Sensitive or expensive fields should require explicit authorization and request. Do not let a generic `fields=*` defeat purpose limitation or capacity controls.

**Define filtering.** Specify filterable fields, operators, case and locale behavior, null handling, time zones, precision, authorization, index support, and limits. Avoid accepting arbitrary expressions that expose internals or unbounded computation.

Filtering changes the claimed population. Include filter semantics in cache keys, telemetry, contract tests, and provenance where results feed material decisions.

**Define ordering.** Pagination requires a stable order. State sort keys, direction, collation, ties, null placement, and whether ordering is total. Add a stable unique tiebreaker where needed.

Default database order is not a contract. Concurrent inserts, updates, and deletes can create duplicates or omissions across pages even when each response is locally valid.

**Choose pagination by behavior.** Offset pagination is understandable and supports arbitrary page selection, but changes before an offset can shift results. Cursor or keyset pagination can be more stable and efficient when order keys are suitable.

Define cursor opacity, scope, expiry, authorization, sort, filters, snapshot, and error behavior. A cursor is not automatically a snapshot; it may merely continue after a key in current state.

**State collection consistency.** Decide whether pages reflect one snapshot, bounded staleness, or live changing state. A snapshot may need an identifier and retention window. Live pagination must disclose possible drift.

For complete extraction, provide a snapshot export or change token when repeated API calls cannot guarantee a coherent population. Do not make consumers reconstruct correctness from undocumented behavior.

**Define time explicitly.** Separate business-effective time, system observation time, transaction time, publication time, cache time, and request time. “Latest” and “current” depend on which timeline and source boundary apply.

Historical queries need valid intervals, version selection, corrections, and retention. If the API only provides present state, state that limitation and offer another product for history where required.

**Design freshness as a data property.** A response can arrive in ten milliseconds while containing yesterday's replicated data. Publish source observation or publication timestamps and define consumer-visible freshness objectives.

Measure age at the response boundary. Include upstream ingestion, derivation, cache, and provider delays. Avoid using server response latency as freshness evidence.

**Use caching knowingly.** HTTP caching can reduce latency and provider load. Define cacheability, validators, variation dimensions, freshness lifetime, revalidation, invalidation, private versus shared storage, and protected content constraints.

Cache keys must include every representation-affecting factor, including authorization or purpose where relevant. Prevent one user's representation from being served to another. Treat caches as governed copies with retention and deletion behavior.

**Use conditional reads.** Entity tags or modification dates can let consumers validate cached representations and avoid transfer. Define whether validators are strong or weak for the intended comparison and how variants affect them.

Validators do not reveal business-effective time by themselves. Connect them to representation versions and provenance. Do not expose internal hashes that leak protected content or unstable storage details.

**Control concurrent writes.** Lost updates occur when two consumers overwrite the same prior state. Conditional requests can require a known version or validator before mutation.

Define conflict responses, merge policy, retriable behavior, and user resolution. Some domain operations should be modeled as commands with explicit preconditions rather than generic replacement.

**Define idempotency for commands.** State the business operation, idempotency key, scope, expiry, stored outcome, duplicate response, and side effects. Request identifiers alone do not make an operation idempotent.

Test timeout after effect, partial downstream work, lost response, repeated key with different payload, and replay after retention. The effect-owning service must enforce the invariant.

**Specify errors for action.** Use HTTP status semantics consistently and a structured problem representation such as RFC 9457 where appropriate. Include stable problem type, instance correlation, human title, machine-usable details, and safe extension fields.

Separate invalid request, unauthorized purpose, forbidden field, conflict, missing resource, rate limit, dependency failure, and provider error. Never put an application failure in a nominal success response merely to simplify client code.

**Avoid leaking protected diagnostics.** Error messages can reveal existence, identifiers, internal services, policy, or personal data. Provide authorized correlation without stack traces or private configuration.

Keep detailed diagnostic evidence in protected operational systems with bounded access and retention. Test enumeration, injection, malformed input, and excessive detail.

**Authenticate workloads and users appropriately.** OAuth 2.0 defines authorization roles and token flows, but architecture must choose profiles, proof, audience, issuer, lifetime, rotation, and workload or user context safely.

Do not treat possession of any token as authorization to all data. Validate intended audience and route. Separate administrative, provider, application, delegated-user, and batch identities.

**Authorize purpose and data.** Decisions may depend on consumer, user, role, purpose, subject relationship, resource, field, region, time, device, risk, and consent. Scopes alone can be too coarse.

Apply row and field minimization before serialization. Keep policy decisions explainable and auditable. Ensure list, search, count, error, and metadata endpoints cannot bypass restrictions.

**Protect against enumeration and inference.** Predictable identifiers, unrestricted filters, precise counts, timing differences, and error distinctions can reveal protected facts. Use opaque external identifiers where appropriate, authorization before disclosure, bounded search, and response normalization.

Privacy attacks can combine multiple permitted queries. Monitor patterns and enforce purpose, rate, and aggregation controls without claiming that throttling alone guarantees privacy.

**Classify response copies.** Consumers, gateways, caches, logs, traces, client libraries, browsers, proxies, test fixtures, and support tools may retain API data. Contracts must carry protection, retention, onward-use, incident, and deletion obligations.

The provider cannot assume revoking access deletes previous responses. Design revocation, correction, notification, and downstream evidence according to consequence.

**Plan capacity from operation cost.** Requests differ in database work, fields, filters, joins, payload size, fan-out, authentication, transformations, and downstream dependencies. Count weighted work rather than requests alone.

Model rates and concurrency distributions, bursts, timeouts, cache behavior, retries, bulk jobs, and failure recovery. Reserve capacity for critical operations or isolate bulk access from transactional workloads.

**Apply rate limits and quotas transparently.** Declare scope, window, burst, cost weights, headers or metadata, exceeded behavior, reset, exceptions, and owner. Clients need enough information to pace safely without learning protected capacity details.

Fairness may be per tenant, purpose, user, operation, or workload class. Equal request counts are not equal resource use. Review limits as demand and capacity evolve.

**Bound timeouts and retries.** Set end-to-end deadlines and allocate budgets across hops. Clients should retry only safe or idempotent interactions, with backoff, jitter, maximum attempts, and budgets.

Coordinate gateway, client, and service behavior. Layered retries multiply load. Shed or reject early when work cannot finish within a useful deadline.

**Provide backpressure and degraded modes.** Return explicit overload or unavailability rather than accepting work indefinitely. Degraded modes may omit expensive optional fields, serve a declared stale representation, or pause noncritical workloads.

Authorize and label degraded data. Do not silently weaken correctness or protection. Test consumer behavior so a fallback does not become an unexamined permanent contract.

**Compose service objectives.** End-to-end availability and latency depend on gateway, provider, stores, identity, networks, derived products, and consumer path. Freshness and correctness add data-specific dimensions.

Set objectives by operation and workload class. Measure successful usable responses at consumer-relevant boundaries. Publish incidents, correction, recovery, and support expectations.

**Observe contracts and outcomes.** Capture request counts, authorized purposes, versions, status and problem types, latency, saturation, rate limiting, retries, cache outcomes, payload size, freshness, quality, dependency errors, and consumer acknowledgement where appropriate.

Minimize and protect telemetry. Query strings, resource IDs, headers, and traces can be sensitive. Use aggregation, redaction, tokenization, access control, retention, and monitored access.

**Trace provenance and correction.** Link a representation to source product, input versions, derivations, publication time, API version, and relevant transformation. For corrected data, identify affected resources, intervals, fields, and consumers.

Consumers need replay, requery, restatement, or decision-review guidance. A correct future GET does not repair reports, models, caches, exports, or decisions made from the old response.

**Publish discovery artifacts.** Provide human documentation, machine-readable descriptions, schemas, examples, changelogs, status, ownership, service tiers, classifications, and onboarding instructions. Register authorized consumer relationships.

Discovery does not mean public access. Offer metadata views appropriate to roles. Record last verification and observed use so stale documentation is visible.

**Version behavior, not only paths.** A change to definitions, defaults, ordering, pagination, error meaning, authorization, freshness, precision, or rate limits can break consumers even when schema fields are only added.

Analyze compatibility across syntax, semantics, behavior, operations, service, and protection. Use fixtures and consumer contract tests, but do not let every accidental dependency veto durable correction forever.

**Manage deprecation as a relationship.** Publish replacement, rationale, affected operations, migration guide, examples, dates, support, observed clients, and rollback. Communicate through more than documentation.

Track actual traffic and consumer acknowledgement while respecting privacy. Exceptions need owner, consequence, controls, and bounded expiry. Unknown clients require an accountable decision, not infinite support.

**Choose bulk alternatives deliberately.** A consumer needing a full daily population may be better served by a versioned snapshot with manifest, checksum, schema, publication time, and quality evidence. An API can initiate or discover the export without carrying every row synchronously.

Separate transactional and extraction capacity. Preserve consistent snapshot semantics and incremental recovery. Do not force consumers to crawl pages simply because an API already exists.

**Choose events for change notification.** Events can notify subscribers of facts or state transitions without polling. They introduce delivery, ordering, duplication, retention, replay, and consumer-lag obligations.

APIs and events often complement each other: an event signals change, and an API retrieves authorized current detail. Define races, versions, deletion, correction, and source authority across both.

**Choose analytical products for computation.** Cross-source joins, scans, aggregates, and historical analysis can overload operational APIs and yield inconsistent multi-request results. Publish governed analytical products or query-serving systems with suitable grain, time, quality, and service.

Avoid copying protected data by default. Compare virtualization, extracts, cached views, and purpose-specific aggregates using workload and governance evidence.

**Plan migration from private access.** Inventory consumers, queries, fields, joins, timing, snapshots, credentials, workload, reports, decisions, and unknown use. Separate legitimate requirements from accidental table behavior.

Create API or alternative product contracts, validate semantics and performance in parallel, and migrate cohorts. Prevent new private dependencies. Keep rollback until consumer outcomes and recovery are evidenced.

**Retire access completely.** Revoke database and API credentials, remove network paths, old versions, gateway rules, code, caches, exports, schemas, docs, alerts, and provider resources. Update catalogs, lineage, ownership, and support.

Preserve required records, history, holds, provenance, and correction capability. Observe after shutdown and verify no authorized need remains. A route returning an error while tokens and copies survive is not fully retired.

**Measure architectural value.** Track private-access reduction, contract coverage, product reuse, consumer onboarding, change lead time, freshness, quality, service, capacity, rate-limit impact, security events, correction, deprecation, and closure.

Do not use endpoint count or traffic alone. A valuable API makes governed data access safer and more changeable for intended consumers while directing unsuitable workloads to better products.

## Definitions and Notation

Represent an API boundary as $A=(P,R,O,V,M,T,K,S,Z,B,G,L)$, where $P$ is the data product, $R$ resources, $O$ operations, $V$ representations, $M$ meaning and authority, $T$ temporal semantics, $K$ contracts and versions, $S$ service and capacity, $Z$ protection, $B$ observability and provenance, $G$ ownership and governance, and $L$ lifecycle.

For a stable collection of $N$ items and page size $p>0$, the minimum request count under full pages is $Q(N,p)=\lceil N/p\rceil$. If the collection changes or authorization filters vary between requests, this arithmetic does not imply complete or duplicate-free extraction.

For workload classes $i$, a simple weighted offered-load quantity is $W=\sum_i \lambda_i c_i$, where $\lambda_i$ is request rate and $c_i$ an evidenced resource-cost weight. It is a planning abstraction, not a service guarantee; concurrency, bursts, dependencies, caches, retries, and tail distributions remain.

Let freshness age at response be $F=t_{response}-t_{source\ observation}$ under declared clocks and provenance. A small HTTP latency $t_{response}-t_{request}$ does not imply small $F$.

Let lifecycle cost be $C_A=C_{product}+C_{interface}+C_{operations}+C_{consumers}+C_{change}+C_{risk}+C_{migration}+C_{retirement}$. Compare an API with events, files, snapshots, replication, and query products under equivalent assertions, workload, time, service, protection, and horizon.

Define `JustifiedAPI(A,t)` as a review predicate requiring a bounded interaction need, explicit meaning and time, provider capacity, consumer-visible service, effective protection, observable behavior, managed change, suitable alternatives, accountable ownership, and funded lifecycle at time $t$.

## Mechanisms, Invariants, or Proof Structure

Use ten gates for every material API-led data-access decision.

**1. Need gate.** Identify consumer purpose, assertions, interaction, workload, history, latency, freshness, consistency, consequence, duration, and alternatives.

**2. Product gate.** Assign resource meaning, source or derivation authority, keys, grain, fields, time, quality, correction, owner, and limitations.

**3. Interface gate.** Define operations, methods, parameters, representations, media types, schemas, examples, errors, identifiers, and discovery.

**4. Collection gate.** Specify projection, filtering, ordering, pagination, snapshot, drift, count, change tokens, limits, and bulk extraction behavior.

**5. Interaction gate.** Define conditional requests, caching, concurrency, idempotency, correlation, timeouts, retries, rate limits, quotas, and degraded modes.

**6. Service gate.** Engineer capacity, isolation, dependencies, freshness, availability, latency, completeness, correctness, recovery, correction, support, and evidence.

**7. Protection gate.** Apply identity, authorization, purpose, minimization, field and row policy, inference controls, logging, copies, residency, retention, deletion, audit, and incidents.

**8. Change gate.** Govern syntax, semantics, behavior, versions, compatibility, tests, notice, migration, deprecation, exceptions, rollback, and client evidence.

**9. Ecosystem gate.** Relate APIs to events, snapshots, files, analytical products, gateways, catalogs, lineage, consumer workflows, costs, and platform responsibilities.

**10. Lifecycle gate.** Discover, onboard, observe, correct, revise, migrate, revoke, remove, archive, retire, and verify closure.

The executable example computes the request bound for a stable paginated collection and the last-page size.

<!-- bijux-verify: {"id":"api-pagination-request-bound","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"records=1030\npage_size=250\nminimum_requests=5\nfull_pages=4\nlast_page_records=30\nunused_last_page_slots=220\n","stderr":""}} -->
```python
records = 1030
page_size = 250

minimum_requests = (records + page_size - 1) // page_size
full_pages, last_page_records = divmod(records, page_size)
unused_last_page_slots = page_size - last_page_records

print(f"records={records}")
print(f"page_size={page_size}")
print(f"minimum_requests={minimum_requests}")
print(f"full_pages={full_pages}")
print(f"last_page_records={last_page_records}")
print(f"unused_last_page_slots={unused_last_page_slots}")
```

The computation proves only that 1,030 stable, authorized records fit into four full pages and one thirty-record page when every request can return 250 records. It does not prove that the population is stable, pages form one snapshot, ordering is total, records are not added or deleted, authorization remains constant, retries do not duplicate reads, or an API is suitable for extraction. Those conclusions require collection semantics, workload, consumer purpose, service, protection, and observed evidence.

## Alternatives and Trade-Offs

**API versus direct database access.** APIs protect storage independence and enforce contracts but add service operation and request overhead. Direct access can suit tightly governed internal engines while creating strong physical coupling and broad privilege.

**API versus snapshot or file.** APIs support selective interactive access. Versioned snapshots serve large coherent populations efficiently but add publication, storage, retention, and incremental-update concerns.

**API versus event stream.** APIs answer requests for state or actions. Events distribute changes asynchronously but require ordering, duplicates, retention, replay, lag, and consumer state management.

**API versus federated query.** APIs bound supported operations and provider capacity. Federation enables flexible composition but can expose source performance, semantic, authorization, and consistency differences at query time.

**Generic resource API versus purpose-specific view.** Generic reuse reduces endpoint count but can overexpose data and underspecify meaning. Purpose-specific views improve minimization and fitness at the cost of more product surfaces.

**Offset versus cursor pagination.** Offset supports easy navigation and counts but drifts under change and can become expensive. Cursors can stabilize continuation and performance while complicating expiry, debugging, and random access.

**Fresh reads versus caching.** Fresh reads reduce staleness but increase latency and provider load. Caches improve resilience and efficiency while adding invalidation, protection, variation, and freshness obligations.

**One version versus parallel versions.** One version simplifies operation but can force coordinated change. Parallel versions provide migration time while multiplying testing, capacity, security, and retirement cost.

**Central gateway versus service-owned policy.** Gateways reuse identity, routing, quotas, and telemetry. Services retain domain-aware authorization and effect semantics. A layered design must prevent gaps and contradictory decisions.

**Synchronous composition versus aggregate product.** Calling several APIs can return current details but compounds latency, failure, and cross-source inconsistency. A governed aggregate can offer stable semantics and service while accepting derivation and freshness cost.

## Failure Modes and Misconceptions

1. **An API makes data a product.** Ownership, meaning, quality, service, protection, and lifecycle are still required.
2. **A resource is a table.** Durable domain concepts should not expose private storage design.
3. **A schema defines semantics.** Types and shapes do not establish authority, time, grain, or fitness.
4. **Additive fields are always compatible.** Strict clients, defaults, meaning, payload size, and authorization can break.
5. **Fast responses are fresh data.** Replicas, derivations, and caches can be old.
6. **Cursor pagination guarantees a snapshot.** Continuation and consistency are separate contracts.
7. **HTTP 200 means business success.** Application validation or effects may have failed.
8. **Request IDs provide idempotency.** The effect owner needs a business key, scope, retention, and stored outcome.
9. **Authentication proves authorized use.** Purpose, subject, resource, field, context, and minimization remain.
10. **Scopes prevent all overexposure.** Search, counts, errors, relationships, and inference can leak data.
11. **Rate limits solve capacity.** Weighted work, dependencies, retries, bursts, and recovery remain.
12. **Clients should retry every failure.** Non-idempotent effects and overload can worsen.
13. **Gateway uptime is API availability.** Provider, stores, identity, networks, freshness, and usable responses matter.
14. **Payload logs are harmless diagnostics.** They create protected, retained copies.
15. **One API should serve transactions and analytics.** Bulk scans can degrade operational service and lack snapshot consistency.
16. **Publishing deprecation notices removes clients.** Runtime evidence, migration, exceptions, and closure are needed.
17. **Disabling a route retires access.** Credentials, caches, copies, schemas, docs, and obligations remain.

## Worked Examples

### Example 1

A service proposes `/customer_table` with columns and internal sequence keys. Storage may soon split across two systems. Architects instead define a Customer resource with stable domain identifier, source assertions, relationships, effective status, and versioned representations. **Conclusion:** a resource contract isolates consumers from physical restructuring while preserving durable meaning.

### Example 2

A client retrieves 1,030 records in pages of 250. Five requests suffice for a stable population, but new records sort before the second offset and cause duplicates. A snapshot identifier and stable total order fix the extraction; otherwise the contract explicitly permits drift. **Conclusion:** page arithmetic does not establish collection consistency.

### Example 3

An API responds in 20 milliseconds from a cache populated nightly. The response includes source-observed and publication timestamps; consumer-visible freshness is thirteen hours. A dashboard stops labeling the data “real time” and uses an event-plus-API pattern for urgent changes. **Conclusion:** latency and freshness are different measurements.

### Example 4

Two clients read version 12 of an Account and submit conflicting replacements. The provider requires a matching entity tag and rejects the stale mutation with a conflict or precondition response. The second client rereads and applies a domain-specific command. **Conclusion:** conditional writes prevent blind lost updates but do not choose the merge policy.

### Example 5

A payment command times out after the effect. The client retries with the same business idempotency key. The provider returns the stored outcome and rejects reuse of that key with a different amount. **Conclusion:** idempotency is enforced at the business-effect boundary, not inferred from transport retries.

### Example 6

A broad `customer.read` scope allows an application to request health flags it never uses. The API adds purpose-specific authorization, field allowlists, minimized defaults, audit evidence, and a separate approved workflow for protected attributes. **Conclusion:** token scopes are inputs to authorization, not complete purpose governance.

### Example 7

A reporting job pages through five million orders during business hours and exhausts database connections. The domain publishes a daily snapshot with manifest and checksum, plus incremental change events; the API remains for selective lookups. **Conclusion:** access patterns should choose products rather than forcing bulk extraction through transactional capacity.

### Example 8

A gateway retries twice and a client library retries three times, yielding up to nine downstream attempts for one call. End-to-end retry ownership, a shared budget, backoff, jitter, and early overload rejection replace layered defaults. **Conclusion:** independently reasonable retries can amplify failure multiplicatively.

### Example 9

Version two adds an enum value and changes empty status to `unknown`. Schema evolution appears additive, but one consumer treats unrecognized values as active. Fixtures, observed-client analysis, and a migration guide expose the risk. **Conclusion:** semantic and behavioral compatibility outrank syntactic labels.

### Example 10

After version-one traffic reaches zero, the team disables its route. Audit finds live tokens, cached payloads, client code, old schemas, alerts, and retained exports. Retirement revokes access, disposes of copies under policy, removes artifacts, preserves required evidence, and observes closure. **Conclusion:** zero ordinary traffic is evidence for retirement, not retirement itself.

## Cross-Program Connections

- **API and service engineering:** HTTP semantics, resource design, contracts, errors, identity, compatibility, reliability, gateways, and developer experience implement API surfaces.
- **Distributed systems:** timeouts, retries, idempotency, concurrency, caches, consistency, partial failure, overload, and recovery shape interaction guarantees.
- **Database engineering:** keys, transactions, snapshots, indexes, query planning, isolation, temporal data, and storage evolution sit behind API contracts.
- **Data engineering:** snapshots, change feeds, quality, lineage, backfills, analytical serving, and correction complement API access.
- **Platform engineering:** gateways, workload identity, schemas, rate limiting, observability, catalogs, paved paths, and self-service reduce repeated work.
- **Cybersecurity and privacy:** authorization, purpose, minimization, enumeration, inference, protected telemetry, retention, deletion, and incidents constrain responses.
- **Software architecture:** bounded contexts, facades, anti-corruption layers, commands, queries, coupling, cohesion, and migration seams locate responsibility.
- **Systems and reliability engineering:** interface assurance, capacity, fault propagation, service objectives, verification, configuration, and lifecycle provide evidence.

## References

1. Fielding, R., Nottingham, M., and Reschke, J., *HTTP Semantics*, RFC 9110, 2022. <https://www.rfc-editor.org/rfc/rfc9110>
2. OpenAPI Initiative, *OpenAPI Specification 3.1.1*, 2024. <https://spec.openapis.org/oas/v3.1.1.html>
3. JSON Schema, *JSON Schema Core, Draft 2020-12*, 2022. <https://json-schema.org/draft/2020-12/json-schema-core.html>
4. Nottingham, M., Wilde, E., and Dalal, S., *Problem Details for HTTP APIs*, RFC 9457, 2023. <https://www.rfc-editor.org/rfc/rfc9457>
5. Hardt, D., *The OAuth 2.0 Authorization Framework*, RFC 6749, 2012. <https://www.rfc-editor.org/rfc/rfc6749>
6. W3C, *Data on the Web Best Practices*, W3C Recommendation, 2017. <https://www.w3.org/TR/dwbp/>
7. Beyer, B., Jones, C., Petoff, J., and Murphy, N. R., eds., *Site Reliability Engineering: Addressing Cascading Failures*, Google, 2016. <https://sre.google/sre-book/addressing-cascading-failures/>
8. NIST, *Systems Security Engineering: Considerations for a Multidisciplinary Approach in the Engineering of Trustworthy Secure Systems*, SP 800-160 Volume 1 Revision 1, 2022. <https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final>

## Exercises

### Exercise 1

Define a complete API data-access contract for `GET /customers/{id}`. Include resource meaning, representation, time, service, protection, errors, ownership, change, and lifecycle.

### Exercise 2

Analyze collection access for 100,000 changing records. Compare offset, cursor, and snapshot pagination, and derive the minimum request count for page size 800 under stable assumptions.

### Exercise 3

Design a protected and reliable Order command API. Include authorization, validation, concurrency, idempotency, errors, capacity, retries, observability, correction, and deprecation.

### Exercise 4

Choose among an API, event stream, daily snapshot, and analytical product for four consumers: a mobile screen, fraud detector, regulatory archive, and quarterly analyst workload.

### Exercise 5

Plan migration from shared database access to governed products for thirty consumers with unknown queries, nightly extracts, interactive applications, and direct reports. Include discovery, seams, validation, rollback, and retirement.

## Answers to the Exercises

### Answer 1

The contract identifies the Customer source-aligned product, owner, stable identifier, bounded domain meaning, and authorized lookup purpose. The representation defines grain, source authority, fields, types, units, codes, null semantics, relationships, classifications, schema and media type, examples, omissions, and provenance. It distinguishes business-effective, observation, publication, cache, and response time and states whether history is available.

Interface behavior covers HTTP method semantics, conditional reads, cache policy, validators, version, not-found and forbidden disclosure, RFC 9457 problem types, correlation, size, timeout, and rate limits. Service covers availability, latency, freshness, quality, correction, recovery, support, and degraded representations at the consumer boundary. Protection covers workload and user identity, purpose, row and field authorization, minimization, inference, logs, caches, regions, retention, deletion, and incident duties. Change covers semantic and behavioral compatibility, fixtures, consumer evidence, notice, migration, exceptions, and rollback. Lifecycle names discovery, support, deprecation, credential revocation, copy handling, artifact removal, retained evidence, and verified retirement.

### Answer 2

For a stable population, $Q(100000,800)=\lceil100000/800\rceil=125$ requests, all full. Offset pagination is easy to navigate and count but concurrent inserts or deletes before an offset cause omissions or duplicates and large offsets may be expensive. Cursor or keyset pagination continues after a stable total-order key and often scales better, but it needs opaque scope, filters, authorization, expiry, tie-breaking, and error behavior; it does not automatically freeze data.

A snapshot binds all pages to one identified population or read point and supports coherent extraction, but the provider must create or retain snapshot state and declare expiry, late data, corrections, deletions, and cost. For a changing 100,000-record export, use a versioned snapshot or change token if completeness matters. If a live UI only needs forward browsing, cursor pagination with declared drift may suffice. Request count assumes stable authorization, page size fulfillment, no retries, no changes, and no errors; it is not proof of complete extraction.

### Answer 3

The Order command names the business intent, allowed state transitions, preconditions, input assertions, keys, units, versions, owner, and outcome. Authenticate workload and user context; authorize tenant, purpose, role, order relationship, fields, amount, region, and policy. Validate schema and domain rules before effects where possible. Use a current order version or explicit precondition for concurrency. Define a business idempotency key with scope, retention, stored outcome, and rejection of key reuse with different input.

Return consistent HTTP status and structured problem types for invalid input, forbidden purpose, conflict, duplicate, rate limit, dependency failure, and internal failure without leaking protected details. Plan weighted capacity, isolate tenants and bulk callers, publish rate and quota behavior, and bound deadlines. Only retry safe or idempotent operations with backoff, jitter, maximum attempts, and one end-to-end budget. Observe correlation, authorized purpose, validation, effect, duplicates, latency, saturation, errors, and consumer outcomes with minimized telemetry. Correction links affected orders and decisions to a rule or code version. Changes use schemas, semantic fixtures, consumer tests, notice, parallel versions where needed, rollback, and verified retirement.

### Answer 4

The mobile screen needs selective low-latency current state and commands, so use a protected API with minimized representations, caching rules, conditional reads, and consumer-visible freshness. The fraud detector needs prompt change signals and scalable asynchronous processing, so publish governed events with ordering scope, duplication, retention, replay, lag, schema, and correction; it can call an API for authorized detail after a signal.

The regulatory archive needs complete immutable or versioned evidence, manifests, checksums, provenance, retention, holds, and reproducibility. Use a snapshot or file publication rather than reconstructing history by polling. The quarterly analyst needs scans, joins, aggregates, and history; use a governed analytical product or serving system with appropriate grain, time, quality, and access. These products share source identifiers, contracts, classification, lineage, and correction. Selection follows purpose, workload, time, service, and protection rather than choosing one universal delivery mechanism.

### Answer 5

Assign stable consumer, query, report, product, table, credential, and access identifiers. Discover use from database audit, query logs, grants, network records, BI tools, ETL, schedulers, repositories, notebooks, reports, exports, incidents, and interviews. Record fields, joins, filters, grain, time, frequency, volume, latency, snapshots, purposes, decisions, owners, protection, service, and observed confidence. Unknown use receives monitored notice and accountable disposition.

Classify interactive lookups and commands for APIs, change reactions for events, coherent bulk populations for snapshots, and historical composition for analytical products. Define source authority, contracts, identifiers, time, quality, correction, service, and protection across all. Introduce views, facades, adapters, dual publication, consumer registrations, and telemetry as seams. Migrate cohorts, comparing values, nulls, keys, grain, time, history, ordering, filters, access, performance, and downstream decisions. Bound dual copies and define rollback.

Prevent new private grants. After consumer acceptance and observed inactivity, revoke credentials and network paths; remove views, queries, jobs, routes, caches, exports, schemas, alerts, and support; update catalogs and lineage; dispose of data under retention and hold rules; preserve provenance and correction evidence; and verify closure. Measure known consumers, private-access reduction, product adoption, service, incidents, semantic differences, migration, and retirement rather than counting endpoints alone.
