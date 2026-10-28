---
module_id: DARCH-087
program: Data Architecture Engineering
level: 2
module_number: 87
title: Federated Query and Data Virtualization
status: complete
last_verified: 2026-09-03
---

# Federated Query and Data Virtualization

## One-Page Review

### Governing question

How should an enterprise expose governed queries across autonomous, heterogeneous data systems while preserving source authority, semantic and temporal correctness, policy, workload isolation, observable plans, reproducibility, cost, and graceful failure—and when should it materialize a supported data product instead?

### Essential definitions

- A **federated query** executes one logical request across two or more independently operated data sources or query engines.
- **Data virtualization** presents distributed data through a logical access layer without requiring every result to be physically consolidated before the request.
- A **federation coordinator** authenticates requests, resolves logical objects, plans distributed work, invokes connectors, combines results, and reports status and evidence.
- A **connector** translates catalog, schema, type, expression, planning, execution, security, cancellation, and error contracts for one source class.
- A **virtual object** is a governed logical table, view, graph, or service whose contract maps to one or more source objects and transformations.
- A **capability matrix** records which types, expressions, predicates, aggregates, joins, limits, ordering, transactions, statistics, policies, and operations an endpoint actually supports.
- **Pushdown** moves an operation such as projection, predicate, aggregation, limit, or join toward a source when semantics and capability permit.
- **Residual evaluation** executes the part of a query that a source cannot safely or efficiently perform.
- A **distributed snapshot contract** defines which source versions or time boundaries a result represents and which inconsistencies remain possible.
- A **semantic mapping** translates types, nulls, collation, time zones, identifiers, units, code sets, functions, and business meaning across boundaries.
- A **query plan receipt** records logical query identity, sources and versions, policy decisions, pushdowns, exchanges, transformations, limits, costs, effects, status, and lineage.
- **Source protection** constrains concurrency, scanned data, rows, time, memory, network, spill, egress, and priority imposed on each participating system.
- **Result reproducibility** means the system can identify or reconstruct the relevant query, contracts, policy, source versions, plan, and nondeterministic context—not necessarily that mutable live sources return identical rows later.
- A **materialized data product** is a persisted, owned distribution with explicit refresh, quality, lineage, policy, service, cost, and lifecycle.
- **Partial result** is an explicitly modeled incomplete answer with missing sources and limitations; it is not a successful complete result.
- **Closure** removes virtual routes, mappings, credentials, caches, materializations, policies, consumers, costs, and recovery activation while preserving required evidence.

### Central model, mechanism, or theorem

Represent federated query as:

`Q = (U, C, S, M, P, E, G, O, R, L)`

where `U` is users and decisions, `C` logical contracts and catalogs, `S` source and connector capabilities, `M` semantic and temporal mappings, `P` planning, pushdown, and exchange, `E` execution and source protection, `G` identity, policy, and governance, `O` observation, lineage, cost, and outcomes, `R` resilience, reproducibility, and recovery, and `L` lifecycle and closure. Virtualization is justified only when an end-to-end contract can be met more safely and economically than a materialized product or direct source interface.

### Critical invariants

- User, request, logical object, source object, connector, schema, mapping, policy decision, plan, fragment, result, receipt, cache, and materialization have separate stable identities.
- Every virtual object names an accountable owner, consumers, semantics, source authority, supported operations, service expectations, policy, cost, and lifecycle.
- Type and expression translation preserves declared semantics or reports loss; syntactic acceptance is not equivalence.
- Pushdown is capability- and invocation-specific, appears in the inspected plan, and cannot weaken row filters, column masks, purpose, or other obligations.
- Results state source versions, snapshot limits, time zones, collation, nondeterminism, missing sources, and partial-result policy.
- Identity and purpose remain attributable across coordinator and sources; shared connector credentials do not erase the requesting principal.
- Admission, quotas, timeouts, cancellation, backpressure, and workload isolation protect every source and the federation itself.
- Query completion, source success, result delivery, consumer use, and beneficial decision outcomes remain distinct.
- Unknown capabilities, stale statistics, policy conflicts, semantic loss, incomplete lineage, partial failure, and uncertain cost remain visible.
- Metrics distinguish planning, pushdown, source work, exchanges, spill, cache, reliability, cost, policy, user success, and outcomes.
- Recovery restores trusted catalogs, mappings, policies, credentials, source state, caches, tombstones, and clocks before serving queries.
- Retirement prevents stale clients, prepared statements, caches, credentials, and restored coordinators from using closed virtual objects.

### Common failures

Common failures include calling a cross-database join transparent; exposing source tables without product contracts; treating identical SQL types as identical semantics; ignoring null, collation, time-zone, and decimal differences; promising a global snapshot without coordination; trusting connector capability labels without plan inspection; pushing policy expressions into sources with different semantics; using one powerful source credential; allowing analytical queries to overload operational systems; retrying a non-repeatable query and merging results; labeling missing-source output complete; caching results without source, policy, purpose, or expiry keys; measuring coordinator uptime rather than user decisions; and retiring views while credentials, caches, clients, and recovery configurations remain.

### Compact example

Ten invented federated-query candidates are evaluated against six declared requirements. Four qualify; one each lacks a contract, loses type semantics, has a policy gap, lacks a coherent snapshot, imposes unbounded source load, or lacks lineage. Seven source systems, six connector types, four join strategies, ten evidence receipts, and ten decisions are counted. Executable evidence confirms only those declarations and counts. It proves no real query correctness, policy enforcement, isolation, performance, reproducibility, cost efficiency, or beneficial outcome.

### Connections

[DARCH-034](034-api-led-data-access.md), [DARCH-038](038-federation-and-virtualization.md), [DARCH-040](040-choosing-an-integration-style-from-semantics-and-latency.md), [DARCH-045](045-semantic-and-metrics-layers.md), [DARCH-064](064-lineage-architecture.md), [DARCH-072](072-policy-as-code-for-data.md), [DARCH-085](085-data-fabric-concepts.md), and [DARCH-086](086-active-metadata.md) establish access, integration, semantics, lineage, policy, fabric, and metadata foundations. [DARCH-088](../ROADMAP.md) next develops data sharing across organizations.

## Governing Question

A logical query can join live orders in PostgreSQL, product metadata in a lakehouse, customer risk in a service, and reference codes in a graph. The SQL may succeed while combining different valid times, truncating decimals, comparing text under different collations, bypassing source policy, exhausting the order database, and producing a result nobody can reproduce.

The governing question is not how to hide heterogeneity. It is which differences may be abstracted, which must remain visible, and when query-time coupling is appropriate. A durable architecture publishes supported logical products, maps semantics explicitly, plans from observed capabilities, enforces policy end to end, protects sources, records evidence, and materializes when repeated live federation cannot meet the contract.

## Why This Matters

Trino's [pushdown documentation](https://trino.io/docs/current/optimizer/pushdown.html) describes predicate, projection, dereference, aggregation, join, and other operations that can be delegated to a connected source. It emphasizes that support depends on the connector and source and that the effective plan reveals whether pushdown occurred. Pushdown is an observed plan property, not a generic connector promise.

Trino's [connector development documentation](https://trino.io/docs/current/develop/connectors.html) exposes capability methods for filters, projections, limits, top-N, aggregation, joins, table functions, and redirection and requires connectors to report when a transformation had no effect. This illustrates why connector contracts must be invocation-specific and optimizer-safe.

Trino's [security overview](https://trino.io/docs/current/security/overview.html) describes authentication, user and group mapping, system and catalog access control, row filtering, column masking, and auditing options. It also documents permissive defaults that require deliberate configuration. A federation must verify identity and controls across all participating layers.

Apache Calcite's [Adapters](https://calcite.apache.org/docs/adapter) documentation describes schema adapters, relational expressions, calling conventions, converters, planner rules, cost-based plan selection, and fallback execution. It demonstrates that heterogeneous federation is a negotiation among logical algebra, source capabilities, conversion, and cost.

PostgreSQL's [Foreign Data](https://www.postgresql.org/docs/current/ddl-foreign-data.html) documentation describes foreign servers, foreign tables, user mappings, and wrappers that fetch or transmit external data. The model makes connector identity and credential mapping explicit. Transaction, optimization, and compatibility behavior remain wrapper-specific.

PostgreSQL's [postgres_fdw](https://www.postgresql.org/docs/current/postgres-fdw.html) documentation covers connection, transaction management, remote optimization, execution environment, compatibility, and diagnostics for remote PostgreSQL sources. Even similar engines require careful control of estimates, pushdown, sessions, transactions, and version behavior.

The W3C [SPARQL 1.1 Federated Query](https://www.w3.org/TR/sparql11-federated-query/) recommendation defines `SERVICE` for evaluating part of a query against another SPARQL endpoint and combining bindings. Its explicit endpoint form makes remote dependence visible. Availability, authorization, endpoint trust, result completeness, and cost remain deployment concerns.

Apache Arrow [Flight SQL](https://arrow.apache.org/docs/format/FlightSql.html) defines SQL metadata and execution operations over Arrow Flight and Protobuf. A common protocol can reduce client and data-transfer friction, but server capabilities, semantics, session state, authentication, authorization, and lifecycle still require contracts.

Google Cloud's [Introduction to federated queries](https://cloud.google.com/bigquery/docs/federated-queries-intro) documents query-time access to external databases, type conversion, pushdown, connection and cross-region limits, source quotas, temporary results, performance constraints, and separate encryption configuration. These explicit limits show why “query in place” is not free or transparent.

Amazon Athena's [Federated Query](https://docs.aws.amazon.com/athena/latest/ug/federated-queries.html) documentation describes connectors over relational, non-relational, object, and custom sources, parallelism, predicate pushdown, and connector-mediated access restrictions. Connector execution, spill, permissions, quotas, and provider boundaries need local assurance.

OpenLineage's [object model](https://openlineage.io/docs/spec/object-model/) represents jobs, runs, datasets, and extensible facets. Federated query receipts can emit exact source and result lineage, but query rewriting, dynamic plans, temporary data, and missing instrumentation require explicit coverage and limitations.

The OpenTelemetry [specification](https://opentelemetry.io/docs/specs/otel/) defines traces, metrics, logs, resources, context propagation, semantic conventions, and protocols. Trace context can correlate client, coordinator, fragments, connectors, sources, exchanges, and delivery while sensitive query text and data attributes require minimization.

The Open Policy Agent [Policy Language](https://www.openpolicyagent.org/docs/policy-language) supports declarative decisions over structured inputs. A federation can use shared policy decisions, but enforcement must cover catalog discovery, planning, source queries, row and column rules, temporary results, caches, exports, and derived products.

W3C [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/) represents datasets, data services, distributions, versions, relationships, rights, and qualified attributions. A logical object can be presented as a supported data service or distribution while retaining the identity and authority of its sources.

The Bitol [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/latest/) provides machine-readable product, schema, quality, service, role, support, and infrastructure sections. A virtual product still needs a contract; query-time access does not remove producer and consumer obligations.

NIST's [Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework) organizes outcomes across Govern, Identify, Protect, Detect, Respond, and Recover. Federation expands trust, credential, network, temporary-data, metadata, and availability boundaries, so security architecture must cover the full lifecycle.

Together these sources support adapter-based planning, explicit endpoint federation, foreign-data mappings, common query protocols, provider-specific limits, lineage, telemetry, policy, product contracts, and lifecycle controls. They do not prove semantic equivalence, global consistency, complete enforcement, economical performance, or user value.

## Prerequisites and Retrieval

You should understand relational algebra, SQL, query planning and optimization, distributed execution, statistics, transactions, consistency, snapshots, schemas, types, null semantics, collation, time, APIs, identity, authorization, policy, data products, contracts, lineage, observability, caching, materialization, workload management, security, privacy, cost, and recovery.

Retrieve federation, virtualization, coordinator, catalog, connector, adapter, foreign table, logical view, source authority, capability matrix, semantic mapping, type coercion, pushdown, residual, fragment, exchange, broadcast join, repartition join, dynamic filter, statistics, distributed snapshot, isolation, partial result, spill, admission, quota, cancellation, lineage, receipt, cache, materialization, reproducibility, recovery, and closure.

As a retrieval test, inspect a virtual view joining a CRM customer table with a fraud feature store. Ask which customer identity and valid time apply; how decimals, nulls, collation, and time zones map; which filters and masks execute where; what snapshot is promised; how source load is bounded; which connector and statistics versions planned the query; where temporary data travels; what happens if one source fails; how the result can be investigated; and when a materialized product is preferable. A successful `SELECT` answers none of these questions.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish federation, virtualization, foreign tables, query engines, semantic layers, caching, replication, and materialized products;
2. define logical object, source, connector, capability, semantic, temporal, policy, service, evidence, and lifecycle contracts;
3. reason about type coercion, nulls, collation, time zones, functions, identifiers, units, code sets, and semantic loss;
4. design logical planning, source discovery, statistics, pushdown, residual execution, join placement, exchange, spill, and caching;
5. state consistency, snapshot, nondeterminism, partial-result, retry, and reproducibility limits honestly;
6. propagate identity, purpose, row and column controls, obligations, lineage, and evidence across coordinator and sources;
7. protect sources with admission, quotas, priorities, timeouts, cancellation, backpressure, and workload isolation;
8. operate connector compatibility, schema drift, statistics freshness, incidents, cost, recovery, and closure;
9. choose live federation or materialization from semantic, service, risk, sovereignty, and economic evidence; and
10. migrate direct cross-system queries into supported products without creating a fragile universal database.

## Core Exposition

**Begin with the consumer decision.** Identify who needs the result, for which purpose, at what grain and time, with which correctness, latency, availability, privacy, reproducibility, and cost. “Join these systems” is an implementation request, not a product outcome.

**Distinguish federation from virtualization.** Federation distributes query evaluation across independent endpoints. Virtualization presents a logical abstraction over location and technology. A system can federate without a stable virtual product, or virtualize a single source through views and caching.

**Do not promise transparency.** Useful abstractions hide incidental syntax and transport while exposing material semantic, consistency, performance, policy, cost, and failure differences. A universal-database illusion makes unsafe assumptions easy and diagnosis difficult.

**Publish logical objects as products.** Name owner, consumers, purpose, source authority, fields, grain, keys, semantics, time, quality, service, policy, lineage, support, cost, change, and retirement. Ad hoc source catalogs are not automatically supported products.

**Separate logical and physical identity.** A logical customer view can map to several physical tables, services, partitions, or versions. Preserve product, distribution, logical field, source field, connector, mapping, and result identities so changes and evidence remain traceable.

**Build a connector capability matrix.** Record discovery, types, predicates, projections, aggregates, joins, windows, ordering, limit, functions, transactions, snapshots, prepared statements, cancellation, statistics, policy, lineage, errors, writes, and version compatibility. Test capabilities rather than trusting documentation alone.

**Negotiate per invocation.** A connector may support predicate pushdown generally but not a particular function, collation, disjunction, nested field, or parameter. Planning records the exact transformation accepted for each request and retains the residual expression.

**Model type translation explicitly.** Map integer ranges, decimal precision and scale, floating point, strings, binary, dates, times, time zones, intervals, arrays, maps, rows, JSON, identifiers, enums, and missing values. State overflow, truncation, rounding, encoding, and unsupported behavior.

**Preserve null and missing semantics.** SQL null, absent JSON fields, graph nonbinding, empty strings, sentinel values, and source-specific missing types are not interchangeable. Three-valued logic and filter placement can change results across mappings.

**Govern collation and comparison.** Case, accents, locale, normalization, padding, sort order, and equality rules affect filters, joins, grouping, distinctness, and order. A pushed comparison must be semantically equivalent or remain residual.

**Normalize time carefully.** Preserve instant, local date-time, zone, offset, calendar, precision, daylight transitions, valid time, transaction time, and source clock. Converting everything to a timestamp without zone can silently change business meaning.

**Map functions by semantics.** Same-named functions can differ in regex dialect, division, rounding, date arithmetic, casts, overflow, substring indexing, and error behavior. Function pushdown requires proven equivalence for the input domain, not spelling.

**Keep business mappings qualified.** Customer, revenue, active, exposure, and current can differ across domains. A virtual view documents transformations, authorities, versions, loss, and intended decisions rather than treating column alignment as semantic integration.

**Define catalog discovery boundaries.** Decide which sources, schemas, objects, columns, statistics, and metadata a user may discover. Metadata names and cardinalities can be sensitive. Cache discovery under identity, tenant, purpose, policy, and freshness.

**Plan from versioned metadata.** Schema, capabilities, statistics, partitions, constraints, indexes, locations, policy, and costs have observation time and version. A plan based on stale metadata is an explicit risk, not an invisible optimizer detail.

**Validate before optimizing.** Resolve names, types, permissions, functions, result schema, and semantic mappings first. Rewrites must preserve the validated meaning. An efficient query that changes null or policy semantics is incorrect.

**Push projections and predicates when safe.** Reducing columns and rows can protect sources, network, cost, and privacy. Preserve exact expression semantics, policy ordering, and error behavior. Inspect the effective plan and record residual filters.

**Push aggregates cautiously.** Count, distinct, averages, approximate functions, grouping, decimal arithmetic, and null treatment differ. Partial aggregation can be safe when merge semantics are defined; opaque source aggregates need compatibility evidence.

**Choose join placement deliberately.** Options include source-local join, coordinator join, broadcast of a small input, repartition exchange, semijoin reduction, dynamic filtering, cached dimension, or prior materialization. Evaluate data size, selectivity, skew, sovereignty, sensitivity, memory, network, and source capability.

**Do not broadcast sensitive data casually.** A small table can still contain secrets or regulated identifiers. Plan policy applies to temporary exchange, worker placement, spill, logs, retries, and cleanup, not only final output.

**Use statistics with uncertainty.** Record source, sample, time, method, confidence, and staleness for row counts, distinct values, ranges, nulls, histograms, sizes, and skew. Plan adaptively or conservatively when estimates are missing or contradicted at runtime.

**Protect operational sources.** Give each source concurrency, rate, scanned-byte, row, time, memory, connection, and priority budgets. Prefer read replicas or supported APIs when production transactions would otherwise compete with analytical scans.

**Admit before spending.** Estimate source work, network, coordinator memory, spill, egress, and monetary cost with uncertainty. Reject, queue, rewrite, sample, or require materialization when the request exceeds policy or budget.

**Apply end-to-end cancellation.** Propagate deadline and cancellation to fragments, connectors, sources, exchanges, and spill cleanup. A client disconnect must not leave an expensive source query running invisibly.

**Treat backpressure as correctness.** Bounded buffers and demand propagation prevent one slow source or consumer from exhausting memory. Spill, queue, throttle, pause, or fail under declared behavior; silent dropping is not valid for query rows.

**Specify distributed snapshot limits.** Independent sources rarely share one transaction or clock. State whether each source is read at statement start, connector start, source snapshot, named version, or unspecified live time, and whether cross-source skew is bounded.

**Avoid invented global consistency.** Two individually snapshot-consistent sources can represent different business times. If a decision requires one cutoff, use versioned source products, coordinated snapshots, temporal predicates, or materialization.

**Model nondeterminism.** Current time, random values, unstable ordering, mutable functions, source retries, approximate algorithms, and live data can change results. Bind evaluation context or label nonrepeatability in the contract and receipt.

**Use retries narrowly.** A failed read may have performed source work and observed a different snapshot on retry. Do not concatenate attempts or claim exactly-once query semantics. Retry only classified safe fragments under the result contract.

**Treat writes as a separate architecture.** Distributed writes introduce authority, transactions, partial commit, compensation, idempotency, conflict, and recovery far beyond read federation. Prefer source-owned command APIs unless a verified write contract is essential.

**Propagate attributable identity.** Preserve authenticated principal, effective user, workload, tenant, purpose, delegation, client, and trace across coordinator and source. A shared service credential needs source-side session context, restrictive policy, and trustworthy audit mapping.

**Compose policy at every boundary.** Cover discovery, logical objects, source objects, rows, columns, functions, query shape, purpose, location, exchange, temporary data, cache, result, export, and derived use. Coordinator permission cannot silently override a stricter source.

**Prove policy-preserving pushdown.** Row filters and masks can interact with joins, aggregation, outer joins, errors, inference, and function semantics. Validate rewrites and ensure policy expressions are evaluated under compatible identity and semantics.

**Control inference channels.** Counts, errors, timing, cardinality, ordering, and repeated predicates can reveal protected values even when columns are masked. Apply query-shape restrictions, thresholds, privacy mechanisms, rate limits, monitoring, and result review according to threat.

**Protect temporary state.** Exchanges, spill, caches, intermediate tables, connector staging, debug samples, and logs carry data and metadata. Apply encryption, placement, tenant isolation, access, retention, deletion, key management, and evidence.

**Design partial failure explicitly.** Source unavailable, timeout, schema drift, policy error, connector crash, worker loss, exhausted quota, corrupt page, and delivery failure have different retry and result semantics. Preserve which fragments and effects completed.

**Do not label partial output complete.** If a use case permits partial results, identify missing sources, fields, time ranges, rows, confidence, and limitations in a machine-readable result contract. Many financial, safety, and compliance decisions should fail instead.

**Emit precise lineage.** Record logical query and plan, exact source objects and versions, pushed and residual transformations, policy filters and masks, temporary materializations, and result identity. Avoid inferring a Cartesian lineage edge between every input and output.

**Create a query plan receipt.** Include request and product identity, normalized query digest, logical schema version, connector and source versions, mappings, policies, plan fragments, pushdowns, snapshots, exchanges, spill, cache, limits, costs, status, lineage, and limitations.

**Observe the full path.** Trace client, admission, planning, policy, fragments, connectors, sources, exchanges, spill, result construction, delivery, and cancellation. Separate coordinator queue time, planning, source execution, transfer, blocked time, and consumer fetch.

**Minimize telemetry.** Query text, literals, plans, errors, field names, and source metadata can expose protected information. Redact or tokenize while preserving correlation and diagnostic usefulness; apply access, retention, deletion, and legal holds.

**Cache under complete semantics.** Keys include logical contract, query, parameters, principal or policy class, purpose, source versions or freshness, mapping, policy revision, locale, time zone, nondeterminism, and result obligations. Invalidate or expire on any relevant change.

**Distinguish cache from product.** A cache optimizes a request under bounded validity. A materialized product has an owner, consumers, refresh, schema, quality, service, policy, lineage, cost, change, support, and lifecycle. Repeated shared cache use may justify promotion.

**Choose materialization from evidence.** Materialize when live sources cannot meet snapshot, isolation, latency, availability, reproducibility, sovereignty, quality, contract, or cost requirements. Keep virtualization for exploratory, low-volume, current, or heterogeneous access that meets its contract.

**Measure source externalities.** Track connections, CPU, I/O, locks, scans, throttling, replicas, incidents, tail latency, and opportunity cost at each source. A fast coordinator result can still harm operational service.

**Measure user outcomes.** Track time to governed answer, success, abandonment, retries, semantic defects, trust, decision quality, support, and avoided materialization. Do not equate query count or bytes scanned with value.

**Test connector semantics.** Use conformance suites for types, nulls, collation, time, functions, pushdowns, transactions, errors, cancellation, policy, schema evolution, and versions. Test negative, boundary, adversarial, load, and fault cases.

**Test plans, not only results.** Small fixtures can return the same rows despite unsafe full scans, missing pushdown, policy placement, or explosive joins. Assert relevant plan properties and source work under representative scale.

**Test failure and recovery.** Inject source delay, partial pages, connector restart, worker loss, stale catalogs, policy outage, spill exhaustion, cancellation, cache corruption, and coordinator failover. Verify status, cleanup, source protection, evidence, and user semantics.

**Version independently.** Logical contracts, schemas, mappings, connectors, coordinator, source engines, policies, statistics, and client protocols evolve separately. Maintain supported compatibility matrices and explicit deprecation rather than accidental lockstep.

**Migrate from direct queries incrementally.** Inventory clients, credentials, source objects, semantics, workloads, costs, policies, failures, and owners. Publish virtual products for bounded uses, compare results and plans, canary consumers, and revoke direct paths after evidence.

**Recover trusted control first.** Restore identity, catalogs, logical contracts, mappings, policies, connector configuration, secrets, source topology, tombstones, cache metadata, time, and evidence. Validate source versions and isolation before accepting queries.

**Retire end to end.** Stop new requests, drain or cancel work, close clients and prepared statements, revoke credentials, remove mappings, expire caches, delete temporary and materialized data, close policies and costs, preserve evidence, and prevent recovery reactivation.

## Definitions and Notation

Let a federated-query system be:

`Q = (U, C, S, M, P, E, G, O, R, L)`.

Represent a source contract as:

`s = (id, authority, connector, schema, capabilities, consistency, policy, limits, service, cost, lifecycle)`.

Represent a virtual object as:

`v = (id, owner, consumers, purpose, logical_schema, semantics, source_map, time_contract, policy, service, lifecycle)`.

Represent a plan fragment as:

`f = (engine, inputs, operations, pushdowns, residuals, exchange, estimates, limits, policy, output)`.

Represent a query receipt as:

`r = (request, virtual_object, query_digest, contract_version, sources, snapshots, connectors, mappings, policies, plan, costs, status, lineage, limitations)`.

Let type mapping be `T_source -> (T_logical, loss, constraints)`. A mapping is total only for its declared source domain; accepting every runtime value by truncation is not semantic totality.

Define pushdown ratio for a plan as:

`P_d = estimated_rows_removed_at_sources / estimated_rows_without_pushdown`.

It depends on uncertain estimates and does not prove semantic correctness.

Define source amplification as:

`A_s = source_rows_scanned / result_rows_delivered`.

The ratio is undefined for zero delivered rows unless a reporting convention is declared, and a high value can be necessary for valid aggregates.

Let snapshot vector `V(q) = {(source_i, version_i, observed_time_i)}`. It exposes per-source state but does not create a single global transaction.

Let `Impact(x)` contain requests, consumers, results, decisions, caches, and derived products linked to faulty connector, mapping, policy, source, or plan `x`. Missing receipts or lineage make the set incomplete.

Define `Closed(v)` to require no client, mapping, route, credential, prepared statement, cache, spill, temporary table, materialization, policy, consumer, cost, or recovery path can use retired virtual object `v`, while required evidence remains controlled.

## Mechanisms, Invariants, or Proof Structure

Use the following assurance gates.

**Outcome gate.** Define consumer, purpose, decision, grain, time, correctness, service, policy, cost, alternatives, and success.

**Product gate.** Verify logical identity, owner, consumers, semantics, source authority, contract, quality, lineage, support, change, and closure.

**Source gate.** Record endpoint, authority, environment, location, engine, version, workload, consistency, service, limits, policy, and lifecycle.

**Connector gate.** Test discovery, types, expressions, pushdown, transactions, statistics, security, errors, cancellation, versions, and failure.

**Semantic gate.** Check keys, grain, nulls, types, precision, collation, time, units, codes, functions, concepts, mappings, loss, and conflict.

**Snapshot gate.** State source versions, read boundaries, skew, nondeterminism, retries, partial-result behavior, and reproducibility.

**Plan gate.** Inspect validation, statistics, rewrites, pushdowns, residuals, join placement, exchanges, estimates, uncertainty, and adaptive changes.

**Protection gate.** Enforce admission, quota, priority, rate, concurrency, scans, connections, deadlines, cancellation, backpressure, spill, and cleanup.

**Policy gate.** Preserve principal, workload, tenant, purpose, discovery, object, row, column, function, source, exchange, cache, result, and export controls.

**Evidence gate.** Correlate request, contracts, sources, versions, mappings, policies, plan, execution, delivery, lineage, cost, and limitations.

**Resilience gate.** Define source, connector, worker, coordinator, policy, network, spill, cache, delivery, and cancellation failures and recovery.

**Economics gate.** Measure licenses, source load, network, egress, coordinator compute, memory, spill, cache, support, incidents, and alternatives.

**Materialization gate.** Compare live federation with owned persisted products on semantics, snapshot, isolation, service, policy, reproducibility, cost, and lifecycle.

**Migration gate.** Inventory direct use, publish contracts, compare results and plans, canary consumers, reconcile, revoke bypasses, and retire safely.

**Recovery gate.** Restore trusted identity, catalogs, contracts, mappings, policy, connectors, secrets, source versions, tombstones, caches, and evidence.

**Closure gate.** Remove clients, mappings, routes, credentials, statements, caches, temporary state, materializations, policies, costs, and recovery activation.

### Executable evidence: federated-query candidate evaluation

The following program classifies ten invented query candidates against six declared requirements.

<!-- bijux-verify: {"id":"federated-query-candidate-evaluation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"queries=10\nqualified=4\nmissing_contract=1\ntype_loss=1\npolicy_gap=1\nstale_snapshot=1\nunbounded_source_load=1\nmissing_lineage=1\nsource_systems=7\nconnector_types=6\njoin_strategies=4\nevidence_receipts=10\ndecision_events=10\n","stderr":""}} -->
```python
queries = [
    {"source": "orders-db", "connector": "postgres", "join": "source", "contract": True, "types": True, "policy": True, "snapshot": True, "bounded": True, "lineage": True},
    {"source": "risk-stream", "connector": "kafka", "join": "repartition", "contract": True, "types": True, "policy": True, "snapshot": True, "bounded": True, "lineage": True},
    {"source": "product-lake", "connector": "object", "join": "broadcast", "contract": True, "types": True, "policy": True, "snapshot": True, "bounded": True, "lineage": True},
    {"source": "reference-graph", "connector": "sparql", "join": "semijoin", "contract": True, "types": True, "policy": True, "snapshot": True, "bounded": True, "lineage": True},
    {"source": "campaign-api", "connector": "api", "join": "broadcast", "contract": False, "types": True, "policy": True, "snapshot": True, "bounded": True, "lineage": True},
    {"source": "finance-db", "connector": "mysql", "join": "repartition", "contract": True, "types": False, "policy": True, "snapshot": True, "bounded": True, "lineage": True},
    {"source": "orders-db", "connector": "postgres", "join": "source", "contract": True, "types": True, "policy": False, "snapshot": True, "bounded": True, "lineage": True},
    {"source": "support-db", "connector": "postgres", "join": "broadcast", "contract": True, "types": True, "policy": True, "snapshot": False, "bounded": True, "lineage": True},
    {"source": "orders-db", "connector": "postgres", "join": "repartition", "contract": True, "types": True, "policy": True, "snapshot": True, "bounded": False, "lineage": True},
    {"source": "product-lake", "connector": "object", "join": "semijoin", "contract": True, "types": True, "policy": True, "snapshot": True, "bounded": True, "lineage": False},
]

def evaluate(query):
    if not query["contract"]:
        return "missing_contract"
    if not query["types"]:
        return "type_loss"
    if not query["policy"]:
        return "policy_gap"
    if not query["snapshot"]:
        return "stale_snapshot"
    if not query["bounded"]:
        return "unbounded_source_load"
    if not query["lineage"]:
        return "missing_lineage"
    return "qualified"

results = [evaluate(query) for query in queries]
print(f"queries={len(queries)}")
for outcome in ["qualified", "missing_contract", "type_loss", "policy_gap", "stale_snapshot", "unbounded_source_load", "missing_lineage"]:
    print(f"{outcome}={results.count(outcome)}")
print(f"source_systems={len({query['source'] for query in queries})}")
print(f"connector_types={len({query['connector'] for query in queries})}")
print(f"join_strategies={len({query['join'] for query in queries})}")
print(f"evidence_receipts={len(queries)}")
print(f"decision_events={len(results)}")
```

The output reports ten candidates, four qualified and one of each declared failure, seven sources, six connector types, four join strategies, ten declared receipts, and ten decisions.

The evidence is deliberately narrow. Invented Booleans and strings do not establish contract fitness, type semantics, policy enforcement, snapshot coherence, bounded load, lineage, query correctness, performance, cost, reproducibility, or user outcome. Production assurance requires connector conformance, plan inspection, representative source tests, policy and workload evidence, snapshot records, end-to-end telemetry, lineage, incident learning, and consumer outcomes.

## Alternatives and Trade-Offs

**Direct source access.** Native capability and low coordinator complexity remain. Consumers absorb heterogeneity, credentials, policy, and change.

**Federated logical access.** Cross-source discovery and composition improve. Runtime coupling, semantic mapping, planning, and failure expand.

**Materialized product.** Isolation, snapshot, quality, reproducibility, and service improve. Freshness lag, copies, cost, retention, and deletion grow.

**Source-local pushdown.** Network and coordinator work decline. Source load and semantic or policy mismatch can increase.

**Coordinator residuals.** Semantics are controlled centrally. More data crosses trust boundaries and consumes memory, spill, and cost.

**Broadcast join.** A small side avoids repartition. Sensitivity, stale size estimates, and worker duplication can make it dangerous.

**Repartition join.** Large inputs distribute across workers. Network, skew, spill, and failure costs rise.

**Semijoin or dynamic filtering.** Source scans can shrink. Extra coordination, source capabilities, timing, and filter size constrain benefit.

**Live-source snapshots.** Currency is high. Cross-source time skew and nonrepeatability remain.

**Named-version queries.** Reproducibility improves. Sources need version support and results can be less current.

**Shared connector credentials.** Operations simplify. Attribution, least privilege, source audit, and blast radius weaken.

**Per-user delegation.** Source accountability improves. Credential exchange, scale, compatibility, and revocation become harder.

**Fail complete.** Consumers never confuse partial with whole. Availability falls when optional sources fail.

**Explicit partial results.** Exploratory use may continue. Downstream tools can ignore limitations and make unsafe decisions.

**Result caching.** Latency and source load decline. Invalidation, identity, policy, freshness, and sensitive temporary data complicate use.

**Adaptive planning.** Runtime evidence can repair bad estimates. Plan variability, policy review, reproducibility, and diagnosis become harder.

**One logical schema.** Consumer queries simplify. Domain meaning and source evolution can be flattened.

**Product-specific virtual views.** Contracts remain bounded and meaningful. More objects, mappings, owners, and lifecycle work are required.

**Read-only federation.** Distributed transaction risk stays bounded. Write workflows need source-owned APIs or separate architecture.

**Federated writes.** One interface can coordinate change. Partial commit, compensation, authority, recovery, and harm become much harder.

## Failure Modes and Misconceptions

1. **“A federated query is transparent.”** Semantics, time, policy, cost, and failure remain material.
2. **“Virtualization creates one database.”** Sources keep independent authority and behavior.
3. **“No data moves during virtual queries.”** Results, exchanges, broadcasts, spill, and temporary tables move or copy data.
4. **“Query in place has no storage.”** Buffers, caches, spill, and temporary results require lifecycle controls.
5. **“A catalog table is a data product.”** Ownership, consumers, contracts, service, and lifecycle are missing.
6. **“Same column name means same concept.”** Domain semantics and time can differ.
7. **“Same SQL type means same values.”** Ranges, precision, collation, encoding, and errors vary.
8. **“All missing values are null.”** Absent, unknown, empty, unbound, and sentinel states differ.
9. **“UTC solves time semantics.”** Local dates, zones, valid time, calendars, and business cutoffs remain.
10. **“Same function name means same function.”** Dialects differ in edge cases and errors.
11. **“Successful casts preserve meaning.”** Truncation, rounding, overflow, and lossy conversion can succeed.
12. **“A connector capability is universal.”** Support depends on expression, source, version, and invocation.
13. **“The optimizer always pushes filters.”** Plans and connector responses determine actual pushdown.
14. **“More pushdown is always better.”** Source load, policy, and semantic mismatch can worsen.
15. **“Pushdown preserves policy automatically.”** Rewrites and source semantics can change filters and masks.
16. **“Small tables are safe to broadcast.”** Sensitivity and worker placement matter beyond size.
17. **“Statistics are facts.”** They are sampled, stale, scoped observations with uncertainty.
18. **“The cheapest estimated plan is cheapest.”** Estimates, contention, egress, and provider billing can be wrong.
19. **“A global query has a global snapshot.”** Independent sources rarely share one transaction.
20. **“Two current sources represent the same time.”** Business and observation times can differ.
21. **“Read-only queries have no side effects.”** They consume connections, locks, CPU, I/O, network, and money.
22. **“Operational databases can absorb analytics.”** Unbounded scans can harm transactional service.
23. **“Timeout stops source work.”** Cancellation may not propagate or may arrive after effects.
24. **“Retry returns the same data.”** Live state, time, randomness, and partial execution can change.
25. **“Retries provide exactly-once queries.”** Attempts can observe different snapshots and consume repeated work.
26. **“A coordinator can safely merge retry output.”** Duplicates and snapshot mixing can corrupt results.
27. **“Shared credentials are merely implementation.”** They affect attribution, privilege, and audit.
28. **“Coordinator authorization covers sources.”** Source and connector paths need enforcement too.
29. **“Column masks prevent all inference.”** Counts, errors, timing, and predicates can leak information.
30. **“Temporary results need no policy.”** They contain governed data and can outlive requests.
31. **“Encryption location follows source policy.”** Exchanges and temporary stores may use different keys and regions.
32. **“A successful fragment proves a complete result.”** Other sources or delivery may fail.
33. **“Partial output is better than failure.”** Many decisions require completeness.
34. **“A missing source can be treated as empty.”** Unavailable and empty are different claims.
35. **“Query completion proves delivery.”** Clients can disconnect or fail while fetching.
36. **“Delivery proves consumer value.”** The result may be unused, misunderstood, or harmful.
37. **“Lineage can be inferred from table lists.”** Pushdowns, fields, expressions, and dynamic plans matter.
38. **“Telemetry should include full SQL.”** Literals and names can expose sensitive data.
39. **“A cache key needs only query text.”** Identity, purpose, policy, versions, locale, and time matter.
40. **“Cache invalidation follows schema change.”** Data, policy, consent, mapping, and source state also invalidate.
41. **“A shared cache is a data product.”** It lacks explicit ownership and service unless promoted.
42. **“Federation is always fresher than materialization.”** Slow sources and caches can make it stale.
43. **“Materialization is architectural failure.”** It can be the correct isolation and reproducibility choice.
44. **“Coordinator uptime measures reliability.”** Sources, connectors, policies, and delivery define the journey.
45. **“Bytes scanned measure value.”** They measure work and often cost, not outcome.
46. **“Result fixtures sufficiently test connectors.”** Plans, boundaries, load, cancellation, and failure need tests.
47. **“Federated writes are symmetric with reads.”** Authority and partial commit make them qualitatively harder.
48. **“Recovery can reuse cached catalogs safely.”** Mappings, policy, credentials, and sources may have changed.
49. **“Deleting a virtual view closes access.”** Credentials, prepared statements, caches, and direct paths can remain.
50. **“Stopping the coordinator retires federation.”** Clients, sources, temporary data, and recovery can reactivate it.

## Worked Examples

### Example 1

A virtual revenue view joins invoices and payments whose decimal scales differ. The mapping rejects values outside the logical precision and records rounding rules rather than silently casting both to a convenient floating-point type.

### Example 2

A case-insensitive source and binary-collation lake produce different customer-key matches. The join remains residual under an explicit normalized key mapping. Pushing equality to both sources would return a different set.

### Example 3

An operational orders database joins a small reference table. A broadcast would scan the full orders table, while semijoin keys allow safe predicate pushdown. Source quotas and the inspected plan—not table labels—justify the choice.

### Example 4

Risk analysis needs balances and limits at one month-end cutoff. Live federation cannot promise cross-source alignment, so each domain publishes a named snapshot and the coordinator records the source-version vector.

### Example 5

A shared connector credential queries a protected table. The federation propagates principal, workload, tenant, and purpose, the source records delegated context, and coordinator row filters remain visible in the plan and receipt.

### Example 6

One source times out after returning pages. The use case prohibits partial results, so the coordinator discards temporary state, cancels remaining fragments, reports the failed source, and does not relabel missing rows as empty.

### Example 7

A dashboard repeats the same expensive query. A cache key binds contract, parameters, purpose, policy revision, source snapshots, time zone, and freshness. A consent revocation invalidates affected entries before expiry.

### Example 8

Repeated federated fraud queries overload an operational replica and need reproducible features. Evidence supports a materialized product with stream refresh, quality checks, lineage, service objectives, retention, and independent ownership.

### Example 9

A connector upgrade changes timestamp rounding and aggregate pushdown. Compatibility tests catch result differences; plan canaries keep the old connector for affected products while a mapping revision and migration are reviewed.

### Example 10

Retiring a partner virtual product drains queries, cancels fragments, revokes connection secrets, expires prepared statements and caches, removes mappings, deletes temporary results, preserves receipts, ends charges, and tests recovery nonactivation.

## Cross-Program Connections

- [Data Engineering](../../19-data-engineering/ROADMAP.md) owns materialized products, movement, transformation, quality, lineage emission, orchestration, and refresh implementation.
- [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md) owns distributed query engines, storage, exchanges, scheduling, memory, spill, caching, scale, and isolation.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) owns types, SQL semantics, transactions, indexes, statistics, query plans, foreign-data interfaces, replication, and source protection.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) owns query-service APIs, authentication, delegation, cancellation, streaming delivery, errors, compatibility, and service objectives.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns connector lifecycle, self-service, admission, policy integration, observability, capacity, secrets, cost, and recovery.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns threat modeling, identity, least privilege, row and column controls, side channels, temporary-data protection, detection, and response.
- [Network Engineering](../../24-network-engineering/ROADMAP.md) owns connectivity, DNS, TLS, routing, bandwidth, latency, segmentation, cross-region transfer, and failure diagnosis.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies reasoning about snapshots, partial failure, clocks, retry, cancellation, consistency, and coordination.
- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) owns boundaries, adapters, contracts, dependency direction, compatibility, and evolution.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies stakeholder, trade-space, assurance, hazard, lifecycle, recovery, and emergent-risk reasoning.

## References

1. Trino, [Pushdown](https://trino.io/docs/current/optimizer/pushdown.html), connector-specific predicate, projection, aggregate, join, and other pushdowns.
2. Trino, [Connectors](https://trino.io/docs/current/develop/connectors.html), connector capabilities and optimizer integration.
3. Trino, [Security Overview](https://trino.io/docs/current/security/overview.html), authentication, identity mapping, access control, masking, and audit.
4. Apache Calcite, [Adapters](https://calcite.apache.org/docs/adapter), schemas, relational expressions, conventions, converters, planner rules, and costs.
5. PostgreSQL, [Foreign Data](https://www.postgresql.org/docs/current/ddl-foreign-data.html), wrappers, servers, tables, and user mappings.
6. PostgreSQL, [postgres_fdw](https://www.postgresql.org/docs/current/postgres-fdw.html), remote PostgreSQL planning, connections, transactions, and compatibility.
7. W3C, [SPARQL 1.1 Federated Query](https://www.w3.org/TR/sparql11-federated-query/), distributed evaluation through `SERVICE`.
8. Apache Arrow, [Flight SQL](https://arrow.apache.org/docs/format/FlightSql.html), metadata and SQL execution over Flight RPC.
9. Google Cloud, [Introduction to Federated Queries](https://cloud.google.com/bigquery/docs/federated-queries-intro), external query limits, types, pushdown, quotas, regions, and costs.
10. Amazon Web Services, [Athena Federated Query](https://docs.aws.amazon.com/athena/latest/ug/federated-queries.html), connector-based queries across heterogeneous sources.
11. OpenLineage, [Object Model](https://openlineage.io/docs/spec/object-model/), jobs, runs, datasets, events, and facets.
12. OpenTelemetry, [Specification](https://opentelemetry.io/docs/specs/otel/), traces, metrics, logs, resources, context, semantics, and protocols.
13. Open Policy Agent, [Policy Language](https://www.openpolicyagent.org/docs/policy-language), declarative decisions over structured input.
14. W3C, [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/), datasets, data services, distributions, versions, rights, and attribution.
15. Bitol, [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/latest/), machine-readable data-product contracts.
16. NIST, [Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework), Govern, Identify, Protect, Detect, Respond, and Recover outcomes.

## Exercises

### Exercise 1

Design a supported virtual product that joins an operational customer source, a lakehouse product, and a reference graph. Define consumer decision, contracts, identity, semantic mappings, source authority, snapshot, service, policy, lineage, cost, and closure.

### Exercise 2

Given heterogeneous decimals, strings, timestamps, missing values, and functions, define a logical type and expression mapping. Identify safe pushdowns, residuals, loss, rejection, boundary tests, and consumer-visible limitations.

### Exercise 3

Plan a federated join under uncertain statistics and skew. Compare source-local, broadcast, repartition, semijoin, dynamic filtering, cache, and materialization. Include source quotas, sensitive movement, spill, cancellation, observability, and cost.

### Exercise 4

Specify identity, policy, and evidence for a query spanning three security domains. Cover discovery, delegation, source access, row filters, masks, purpose, temporary state, inference, exports, receipt, partial failure, and incident response.

### Exercise 5

Plan migration from direct cross-database queries to governed virtual and materialized products. Include inventory, result and plan comparison, consumer canaries, connector compatibility, recovery, credential revocation, and retirement.

## Answers to the Exercises

### Answer 1

Name an owned logical product for a precise decision and consumer set. Bind customer identity and valid time, map lake measures and graph concepts with versions and loss, and preserve each source authority. Publish fields, grain, keys, null and time semantics, supported filters, snapshot vector, partial-result prohibition, service objectives, quality, policy, lineage, support, and cost. Test connector capabilities and protect the operational source with a replica and quotas. The receipt records exact sources, mappings, policies, plan, and limits. Closure removes mappings, secrets, caches, temporary data, consumers, and restore activation.

### Answer 2

Choose logical types only where every accepted source value has a defined mapping. Reject decimal overflow rather than silently round unless the contract authorizes rounding. Distinguish absent, null, empty, and sentinel states. Normalize strings under an explicit collation and Unicode form. Preserve instants, local date-times, zones, offsets, and precision. Compare function edge cases and error behavior. Push only expressions proven equivalent for the input domain; retain residuals otherwise. Test minimum, maximum, null, malformed, daylight transition, collation, overflow, division, regex, and unsupported cases, and expose every loss.

### Answer 3

Record estimate source, time, sample, uncertainty, cardinality, width, distinctness, selectivity, and skew. Source-local joins minimize movement when one endpoint owns both inputs and preserves semantics. Broadcast only a truly small, permitted side to approved workers. Repartition large compatible inputs with skew controls and spill bounds. Semijoin or dynamic filters can reduce source scans if key transfer is permitted. Cache stable dimensions under complete policy and version keys. Materialize when repetition, snapshot, isolation, reproducibility, or cost demands it. Admission, per-source budgets, deadlines, end-to-end cancellation, trace and plan evidence, runtime adaptive limits, and egress costs govern every choice.

### Answer 4

Preserve authenticated principal, effective workload, tenant, purpose, delegation, client, and trace. Apply discovery controls before exposing catalogs. Compose logical and source policy without weakening either; prove row-filter and mask placement through plan tests. Restrict query shapes and rates that create inference channels. Encrypt and isolate exchanges, spill, caches, and temporary results in allowed regions. Record bounded query digest, contracts, mappings, policy revisions, source snapshots, plan, enforcement, delivery, lineage, and limitations. On partial failure, follow the product's complete-or-explicit-partial rule, cancel outstanding work, clean temporary state, preserve evidence, and route security incidents to response and affected parties.

### Answer 5

Inventory clients, users, queries, credentials, source objects, meanings, snapshots, loads, policies, costs, failures, exports, and owners. Group queries by durable consumer decision and publish bounded logical contracts. Run old and new paths against representative and adversarial data; compare results, plans, source work, policy, latency, and cost. Canary consumers and maintain explicit rollback. Promote repeated high-service workloads to materialized products. Version connector and mapping compatibility independently. Restore identity, contracts, policies, secrets, source topology, and tombstones before serving after failure. Retire direct paths by revoking credentials, removing mappings and prepared statements, expiring caches, deleting temporary data, preserving receipts, and testing recovery.
