---
module_id: DARCH-038
program: Data Architecture Engineering
level: 1
module_number: 38
title: Federation and Virtualization
status: complete
last_verified: 2026-09-03
---

# Federation and Virtualization

## One-Page Review

### Governing question

When should consumers query data across autonomous sources through a federated or virtual layer, and how can architects preserve meaning, time, protection, source safety, predictable service, provenance, and ownership when planning and execution span systems with different models and guarantees?

### Essential definitions

- **Data federation** presents governed access across multiple autonomous data sources while those sources retain their own storage, operation, and authority.
- **Data virtualization** supplies logical views or interfaces that hide selected physical-source differences and may execute queries across them without requiring a permanent centralized copy as the primary product.
- A **virtual dataset** is a governed logical representation computed from one or more sources at query time or from explicitly managed caches.
- A **connector or adapter** translates a virtual engine's operations, types, identity, metadata, and errors to a source capability.
- **Query pushdown** delegates filters, projections, aggregations, joins, limits, or other operations to a source rather than moving all input to the federation layer.
- **data movement** is the transfer of source rows, columns, intermediate results, or cached data across a boundary during planning and execution.
- A **federated join** combines inputs whose storage, clocks, transactions, availability, authorization, and schemas may differ.
- **capability discovery** identifies which operations, types, statistics, and guarantees a connector and source can safely execute.
- **semantic mediation** maps source meanings into a declared logical contract; structural alignment alone does not establish equivalence.
- **identity delegation** carries an authorized user or workload context to a source; **service identity** executes under shared technical authority and requires compensating controls.
- **source protection** bounds query concurrency, bytes, time, scans, locks, memory, and priority so virtual access cannot destabilize operational systems.
- **materialization** persists a result or intermediate state; it may be a cache, acceleration, snapshot, or durable product with its own lifecycle.

### Central model, mechanism, or theorem

Represent a virtual product as:

`V = (sources, connectors, logical_model, mappings, planner, execution, time, service, protection, observability, ownership, cache, change, lifecycle)`

Federation trades copy latency and duplicated storage for runtime dependency and cross-source uncertainty. Pushdown can reduce movement and use source indexes, while central execution can provide consistent operators across weak connectors. Neither is automatically better. A justified design makes semantic mappings, query plans, data movement, time consistency, identity, source limits, partial failure, caching, cost, and consumer fitness observable and governable.

### Critical invariants

- Every virtual dataset names source products, assertion authority, keys, grain, mappings, time boundaries, quality, limitations, consumers, and owner.
- Connectors declare supported types, operators, pushdown, transactions, identity, errors, statistics, and version compatibility; unsupported behavior is not guessed.
- Query plans preserve semantics when moving predicates, projections, aggregations, joins, and limits across different null, collation, timezone, precision, and error rules.
- Cross-source results disclose whether they represent one snapshot, independent read times, bounded staleness, or live mixed state.
- Authorization, purpose, minimization, row and field controls, residency, licensing, retention, deletion, and audit hold across sources, intermediates, spills, caches, results, logs, and exports.
- Query admission, budgets, concurrency, timeouts, cancellation, workload isolation, and source-specific limits protect operational systems.
- End-to-end service accounts for virtual layer, connectors, networks, sources, identity, caches, planning, execution, and consumer-visible freshness and correctness.
- Lineage and runtime evidence expose sources, versions, mappings, plans, pushdown, movement, cache use, failures, and output consumers.
- Schema, source, connector, policy, and semantic changes use impact analysis, compatibility testing, versioning, communication, and rollback.
- Retirement closes views, catalogs, connectors, credentials, policies, caches, spills, exports, query history, alerts, contracts, and source grants after consumer validation.

### Common failures

Common failures are calling a catalog of links a semantic layer; joining same-named keys with different identity rules; claiming zero-copy while caches and spills persist data; pushing predicates whose null or collation behavior differs; assuming all sources share one snapshot; hiding stale replicas behind live views; running unrestricted analytical scans on operational databases; using one privileged connector identity for every consumer; enforcing policy only after protected rows moved; ignoring error and cancellation propagation; estimating cost from query count rather than bytes and source work; changing source schemas without consumer impact evidence; treating cached results as harmless acceleration; and removing a view while grants, exports, credentials, and source load remain.

### Compact example

A virtual Customer Revenue dataset joins CRM customer assertions with ledger revenue. The contract preserves separate source authority, maps stable business keys, states that sources are read independently within a five-minute window, and excludes transactionally consistent point-in-time claims. Region and active-status filters push to each source under verified semantics; a small result joins centrally. Per-source quotas protect operations, purpose-aware policies apply before movement, and lineage records plan and versions. A daily materialized snapshot serves large repeat analytics.

### Connections

[DARCH-020](020-reconciling-conflicting-models-across-systems.md) covers semantic reconciliation, [DARCH-027](027-producer-and-consumer-contracts.md) establishes obligations, and [DARCH-028](028-cross-domain-dependencies.md) supplies graph reasoning. [DARCH-034](034-api-led-data-access.md) and [DARCH-037](037-batch-and-file-exchange.md) provide access and materialization alternatives; this module prepares [DARCH-040](../ROADMAP.md) on integration-style selection.

## Governing Question

Federation can give consumers one query surface without first copying every source into a warehouse. It can also make one user query an unbounded distributed program whose semantics, authorization, latency, and failures depend on systems operated for other purposes.

The governing question is not “Can the engine connect to these systems?” It is “Can a logical product across autonomous sources offer defensible meaning, time, protection, service, and cost while respecting the capacity and authority of each source?”

## Why This Matters

Centralizing every dataset creates latency, storage, duplication, synchronization, and governance work. Querying sources in place can provide current access and reduce unnecessary copies. The apparent absence of pipelines does not eliminate integration: mappings, connectors, planning, movement, security, caching, operations, and consumer contracts still exist.

The SQL/MED concepts exposed through PostgreSQL's [Foreign Data Wrappers](https://www.postgresql.org/docs/current/postgres-fdw.html) show how foreign tables can map remote data into a local query surface. Trino's [Connector documentation](https://trino.io/docs/current/connector.html) illustrates a connector-based engine spanning heterogeneous sources. Product capabilities and guarantees remain source- and version-specific.

The W3C [SPARQL 1.1 Federated Query](https://www.w3.org/TR/sparql11-federated-query/) recommendation defines a mechanism for directing parts of a query to remote SPARQL services. The W3C [Data on the Web Best Practices](https://www.w3.org/TR/dwbp/) addresses identifiers, metadata, access, versions, quality, provenance, and reuse. These reinforce that federation needs both execution and product metadata.

W3C [PROV-O](https://www.w3.org/TR/prov-o/) supplies derivation concepts. Google's [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/) informs overload controls. NIST [SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final) describes zero-trust architecture principles, and NIST [SP 800-160 Volume 1 Revision 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) frames trustworthy security across system lifecycles.

## Prerequisites and Retrieval

You should understand relational queries, joins, query planning, indexes, statistics, transactions, isolation, schemas, APIs, data products, domains, authorization, distributed failure, caching, lineage, provenance, service objectives, privacy, and lifecycle.

Retrieve federation, virtualization, virtual view, connector, catalog, logical model, mapping, capability, predicate, projection, aggregation, join, pushdown, pruning, statistics, cardinality, intermediate, spill, cache, materialization, delegation, impersonation, snapshot, staleness, admission, cancellation, source protection, and retirement.

As a retrieval test, inspect “The virtual layer provides one live Customer view across CRM and Billing.” Ask which assertions each owns, how identities and grain align, which read times apply, where filters and joins execute, what moves, whose authorization reaches each source, which caches exist, how source failure appears, and who corrects the result. The phrase is not yet a contract.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish federation, virtualization, catalogs, semantic layers, replication, caching, materialized views, and data products;
2. model sources, connectors, logical contracts, mappings, planners, execution, time, service, protection, ownership, cache, and lifecycle;
3. reconcile keys, grain, units, codes, nulls, time, identity, authority, and quality across autonomous sources;
4. explain predicate, projection, aggregation, join, and limit pushdown and the conditions required for semantic equivalence;
5. reason about cardinality, statistics, join placement, intermediate movement, spills, source work, and query cost;
6. define cross-source snapshot, mixed-time, staleness, caching, and transaction limitations precisely;
7. engineer identity delegation, purpose-aware policies, minimization, source-side enforcement, audit, residency, and result-copy governance;
8. protect sources through admission, quotas, workload classes, timeouts, cancellation, concurrency, and resource budgets;
9. observe logical and physical plans, movement, cache use, source service, failures, quality, lineage, and consumer outcomes;
10. decide when to federate, materialize, replicate, publish an API, exchange files, or build an aggregate product.

## Core Exposition

**Begin with the consumer question.** Record purpose, assertions, population, keys, grain, history, freshness, consistency, latency, volume, concurrency, protection, and decision consequence. A one-off discovery query differs from a critical dashboard or transaction.

Federation is attractive when data should remain under source control and query demand is bounded. Repeated large scans or stable derived facts often deserve a materialized product.

**Name source products.** A connector reaches a system, but a virtual dataset should depend on governed products or explicit source boundaries. Record each source's authority, quality, service, protection, and lifecycle.

Do not infer authority from physical location. CRM may store billing fields copied from Ledger. The virtual contract must identify which source owns each assertion.

**Define the logical product.** State result grain, keys, relationships, fields, definitions, units, codes, nulls, time, classifications, quality, provenance, limitations, and owner.

A view definition is implementation, not sufficient documentation. Consumers need to know what the result claims and under which evidence.

**Reconcile identity.** Same-named customer IDs can come from different namespaces; different IDs can refer to one subject. Joins require declared identity mappings and confidence.

Do not embed probabilistic matching invisibly in a connector. Publish identity resolution as a governed mapping or product with ownership, versions, errors, and correction.

**Reconcile grain.** Joining customer rows to invoice lines multiplies records. A consumer expecting one row per customer may double-count balances.

Declare input and output grain and join cardinality. Aggregate at an accountable boundary. Test one-to-many, missing, duplicate, and temporal relationships.

**Reconcile meaning.** `active`, `revenue`, `country`, or `date` can differ across sources. Map definitions, units, code sets, null semantics, and effective intervals.

Semantic mediation creates new claims and needs an owner. Avoid selecting the convenient non-null value without a survivorship or precedence rule.

**Model time.** Each source read has transaction, observation, publication, replica, cache, and response time. A federated result may combine states that never coexisted.

State whether the query uses independent live reads, source snapshots, as-of parameters, bounded staleness, or a coordinated snapshot. Do not label mixed-time results point-in-time.

**Understand connector capabilities.** A connector maps catalogs, schemas, types, predicates, functions, statistics, transactions, identity, and errors. Capabilities can vary by source and version.

Maintain a tested capability matrix. Unsupported pushdown should fall back safely or reject clearly. Silent semantic approximation is dangerous.

**Map data types explicitly.** Decimal precision, timestamps, timezones, strings, collation, binary data, arrays, nested values, and nulls differ. A type conversion can overflow, truncate, round, or reorder.

Specify mapping and error behavior. Include extreme values and historical schemas in tests. Avoid converting protected identifiers to floating-point numbers or local times.

**Reason about predicate pushdown.** Sending `region='SE'` to a source can reduce rows moved and use indexes. It is valid only if source and virtual comparison semantics agree for type, collation, case, nulls, timezone, and errors.

When equivalence is uncertain, evaluate centrally or apply a conservative source predicate plus exact central filter. Record plan behavior and movement.

**Reason about projection pushdown.** Requesting only needed columns reduces bytes and exposure. The source may still require hidden keys or fields to evaluate policies and joins.

Minimize before movement where possible. Ensure pushed projections do not omit fields needed for correct null, duplicate, provenance, or authorization behavior.

**Reason about aggregation pushdown.** Source-side sums or counts can dramatically reduce movement and use local execution. Results can differ through precision, overflow, null, collation, grouping, or approximate algorithms.

State exactness and types. For sensitive populations, aggregate pushdown can also reduce row exposure, but small groups may create inference risk.

**Reason about join pushdown.** A source can efficiently join tables it owns under one transaction and optimizer. Cross-source join pushdown may be impossible or supported only through one source's foreign-access mechanism.

Choose join placement from capabilities, movement, source work, semantics, protection, service, and failure. Lowest estimated byte movement is not always the safest plan.

**Use statistics carefully.** Planners estimate cardinality from source statistics, metadata, sampling, or cached observations. Stale or absent statistics can choose catastrophic join order.

Record statistics age and confidence. Apply plan limits and adaptive controls. Protected distributions may not be safe to expose broadly.

**Measure data movement.** Track rows and bytes read at sources, transferred, shuffled, spilled, cached, and returned. Query text or result size alone hides intermediate cost.

Compression, serialization, and network locality affect cost. Use observed plans and workload distributions rather than a single benchmark.

**Protect operational sources.** Federated analytical queries can hold transactions, consume connections, scan indexes, evict caches, or compete with application work.

Use read replicas, workload groups, concurrency limits, statement timeouts, scan and byte budgets, priorities, maintenance windows, and circuit breakers. Source owners define safe envelopes.

**Design admission control.** Authenticate the consumer, classify workload and purpose, estimate cost, check source health and budgets, then admit, queue, degrade, or reject.

Cost estimation is uncertain. Enforce runtime limits and cancellation. Prevent a flood of individually cheap queries from exhausting shared sources.

**Propagate cancellation.** When a consumer disconnects or a deadline expires, cancel remote work and release resources where connectors support it.

Orphan queries can continue burdening sources after the virtual layer reports failure. Observe cancellation confirmation and provide cleanup for connectors with weak support.

**Bound retries.** Retrying a distributed query can repeat expensive scans and duplicate temporary data. Use deadlines, backoff, jitter, maximum attempts, and query budgets.

Retry only when semantics permit. A second execution may observe different source state. Label restarted results rather than pretending continuation of one snapshot.

**Handle partial failure.** One source can return rows before another fails. Decide whether the entire result fails, partial data is explicitly labeled, or a prior cache is used.

Never silently omit a failed source. A degraded result needs authorized policy, visible completeness, source status, age, and consumer acceptance.

**Compose service objectives.** End-to-end availability and latency depend on planner, connectors, networks, identity, every required source, caches, and consumer path.

Define objectives by virtual product and workload class. Include data freshness, semantic correctness, completeness, cancellation, recovery, correction, and support—not just engine uptime.

**Avoid naive availability multiplication.** Component availability values may be dependent, workload-specific, or measured at different boundaries. Optional sources and caches change paths.

Model scenarios and fault trees. Validate through observed queries and failure tests. Declare which degraded paths still meet product meaning.

**Choose identity propagation.** End-user or workload delegation lets sources enforce native policy and audit consumers but requires compatible identity, token exchange, and trust.

A service identity simplifies connectivity but concentrates privilege and moves fine-grained enforcement to the virtual layer. Use source-scoped credentials, purpose-aware policy, and attributable audit.

**Enforce policy before movement.** Row and field restrictions should apply as close to the authoritative source as feasible so unauthorized data does not enter intermediates.

Defense in depth can repeat checks centrally. Verify equivalence and fail closed. Policy pushdown itself is a semantic transformation requiring testing and evidence.

**Prevent inference.** Joins, counts, filters, errors, timing, and repeated queries can reveal protected facts even when fields are hidden.

Use minimum group sizes, query-shape restrictions, budgets, result review, or purpose-specific products where needed. Rate limits alone do not prove privacy.

**Govern metadata.** Catalogs expose names, schemas, classifications, statistics, owners, and relationships. Metadata can reveal sensitive systems and populations.

Offer role-appropriate discovery, protect connector configuration and credentials, and track metadata freshness. A discoverable dataset is not automatically authorized.

**Treat intermediates as copies.** Exchange buffers, worker memory, local disks, spills, result caches, history, logs, traces, notebooks, and exports may persist source data.

Apply encryption, access, residency, retention, deletion, records, provider, and incident rules. “Zero copy” should mean no intended durable central product, not literally no bytes copied.

**Design caching explicitly.** Caches improve latency, resilience, and source protection. They introduce staleness, invalidation, key variation, authorization, storage, correction, and deletion obligations.

Name cache scope, key, contents, freshness, source version, purpose, consumers, eviction, and fallback. Do not serve one tenant's result to another through an incomplete key.

**Distinguish cache from materialized product.** A transparent cache accelerates the same contract within bounded staleness. A durable reusable result with independent consumers and service is a product and needs ownership.

Promote recurring high-value queries deliberately rather than letting accidental caches become shadow warehouses.

**Control result size.** Require limits, pagination, aggregation, sampling, asynchronous export, or materialization for large results. A client-side limit may not prevent full source scans.

Define row, byte, time, and intermediate limits. Avoid truncating silently; return explicit incomplete status or reject before misleading consumers.

**Support reproducibility honestly.** A query text alone cannot reproduce results when sources, schemas, data, policies, connectors, plans, or clocks change.

Record source versions or snapshots, query and parameters, mappings, policy, connector and engine versions, plan, time, cache, and result digest where consequence warrants.

**Maintain lineage and provenance.** Link virtual fields and results to source products, fields, mappings, queries, transformations, executions, agents, and times.

Dynamic lineage can record actual plans and sources. Static lineage describes possibilities. Preserve both and disclose gaps caused by opaque connectors or source functions.

**Observe planning and execution.** Track logical and physical plans, pushdown decisions, source calls, rows, bytes, scans, joins, shuffles, spills, cache hits, retries, cancellation, errors, and result size.

Correlate with source service and consumer outcomes. Protect query text and literals, which may contain personal or secret values.

**Allocate cost.** Include engine compute, connector operation, source work, network, spill, cache, catalog, observability, support, incidents, change, and source opportunity cost.

Query count is weak allocation. Use workload classes and measured work without creating incentives to bypass governance. Make uncertainty explicit.

**Govern schema change.** Source column rename, type change, table move, permission change, connector upgrade, or policy revision can break virtual products.

Use impact analysis, contracts, compatibility fixtures, versioned views, notices, parallel operation, rollback, and consumer migration. Do not bind durable names to physical locations unnecessarily.

**Govern semantic change.** A source can keep the same schema while changing definition or authority. Virtual mappings must carry effective time and version.

Correct derived outputs and notify affected consumers. A view recompiling successfully is not evidence of semantic compatibility.

**Assign ownership.** Source teams own source products and safe query envelopes. Platform teams own engine and connectors. Virtual product owners own cross-source meaning and service. Consumers own fitness and downstream effects.

Name incident coordination, change approval, source protection, correction, cache decisions, and retirement. Federation does not dissolve organizational boundaries.

**Choose federation for selective composition.** It fits bounded queries across sources when copying is undesirable, source interfaces are stable, and runtime dependency is acceptable.

It is weak for repeated large scans, strict global snapshots, unpredictable low latency, fragile operational sources, or complex reusable transformations.

**Choose materialization when evidence favors it.** Recurring joins, large movement, expensive source work, historical reproducibility, stable derived meaning, or strict service may justify an aggregate product.

Materialization adds freshness, storage, synchronization, and copy governance. Compare lifecycle outcomes rather than ideological “zero-copy” claims.

**Combine federation and products.** Federate for discovery and low-volume exploration, then promote validated recurring logic to governed materializations. Use virtual views over products rather than raw sources where possible.

Keep semantics consistent across both. A cache or snapshot used for acceleration must expose its time and provenance.

**Plan migration.** Inventory queries, consumers, sources, mappings, policies, workloads, caches, reports, decisions, and unknown use. Establish contracts, budgets, identity, lineage, and telemetry before redirecting traffic.

Validate old and new results across keys, grain, values, nulls, time, security, completeness, performance, and decisions. Use bounded cohorts and rollback.

**Retire completely.** Remove views, catalogs, connectors, credentials, network grants, source permissions, caches, spills, result stores, scheduled queries, exports, alerts, dashboards, docs, and support.

Update lineage and consumer records. Preserve required audit, provenance, retention, holds, and correction evidence. Verify source load and access cease.

**Measure value.** Track governed product coverage, source safety, pushdown correctness, rows and bytes moved, query and source latency, freshness, failures, cancellations, cache staleness, policy decisions, incidents, cost, and retirement.

Connected-source count is not value. Federation succeeds when consumers receive defensible cross-source answers without unacceptable copies, source harm, semantic ambiguity, or runtime fragility.

## Definitions and Notation

Represent virtual product $V=(S,C,L,M,P,E,T,Q,Z,O,K,G,R)$, where $S$ is source products, $C$ connectors and capabilities, $L$ logical model, $M$ semantic mappings, $P$ planner and pushdown, $E$ execution and movement, $T$ temporal model, $Q$ service and source budgets, $Z$ protection, $O$ observability and provenance, $K$ caching or materialization, $G$ ownership and change, and $R$ retirement.

For source relations $i$, let selected rows be $n_i$, average transferred row bytes $b_i$, and intermediate shuffle bytes $h$. A simple movement estimate is $D=\sum_i n_i b_i+h$. It omits compression, protocol overhead, source reads, scans discarded by filters, spills, retries, and result transfer.

Let $t_i$ be the effective read boundary of source $i$. Cross-source temporal skew is $\Delta_t=\max_i(t_i)-\min_i(t_i)$ under compatible time meanings and clocks. Small skew does not prove a distributed snapshot or semantic consistency.

For source $i$, admitted work $w_i$ must remain within a reviewed budget $q_i$ for the workload class and interval. $w_i\leq q_i$ is necessary but not sufficient for safety because locks, skew, tail latency, cache eviction, and correlated demand remain.

Define `JustifiedVirtualization(V,t)` as a review predicate requiring coherent cross-source meaning, explicit time, capable connectors, semantically safe plans, bounded movement and source work, effective protection, observable service, accountable ownership, compared materialization alternatives, and funded lifecycle at time $t$.

## Mechanisms, Invariants, or Proof Structure

Use ten gates for every material virtual product.

**1. Need gate.** Define consumers, questions, sources, assertions, history, freshness, consistency, volume, concurrency, consequence, protection, and alternatives.

**2. Semantic gate.** Reconcile authority, keys, identity, grain, relationships, fields, units, codes, nulls, time, quality, provenance, and limitations.

**3. Connector gate.** Test types, predicates, functions, statistics, transactions, identity, authorization, cancellation, errors, versions, and failure behavior.

**4. Plan gate.** Validate projection, predicate, aggregation, join, limit, sorting, pushdown, cardinality, placement, movement, spills, and semantic equivalence.

**5. Time gate.** Declare source read boundaries, snapshots, replicas, staleness, caches, skew, retries, partial results, and reproducibility evidence.

**6. Protection gate.** Apply delegation, least privilege, purpose, minimization, row and field policy, inference controls, residency, copies, retention, deletion, audit, and incidents.

**7. Source-safety gate.** Govern admission, workload classes, budgets, concurrency, timeouts, cancellation, retries, isolation, source health, and escalation.

**8. Service gate.** Define availability, latency, freshness, completeness, correctness, capacity, degraded behavior, recovery, correction, support, and cost.

**9. Evidence gate.** Observe plans, pushdown, sources, versions, rows, bytes, scans, joins, spills, caches, identities, policies, errors, lineage, and consumer outcomes.

**10. Lifecycle gate.** Discover, authorize, publish, query, cache, correct, revise, materialize, migrate, revoke, remove, archive, retire, and verify closure.

The executable example compares estimated input movement with and without source filter and projection pushdown.

<!-- bijux-verify: {"id":"federated-query-movement-estimate","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"full_scan_bytes=184000000\npushed_input_bytes=9200000\nnominal_bytes_avoided=174800000\npushed_to_full_ratio=0.0500\n","stderr":""}} -->
```python
left_rows, left_row_bytes = 1_000_000, 160
right_rows, right_row_bytes = 200_000, 120
left_selected, right_selected = 50_000, 10_000

full_scan_bytes = left_rows * left_row_bytes + right_rows * right_row_bytes
pushed_input_bytes = (
    left_selected * left_row_bytes + right_selected * right_row_bytes
)
nominal_bytes_avoided = full_scan_bytes - pushed_input_bytes
pushed_to_full_ratio = pushed_input_bytes / full_scan_bytes

print(f"full_scan_bytes={full_scan_bytes}")
print(f"pushed_input_bytes={pushed_input_bytes}")
print(f"nominal_bytes_avoided={nominal_bytes_avoided}")
print(f"pushed_to_full_ratio={pushed_to_full_ratio:.4f}")
```

The arithmetic proves only an input-byte estimate under declared row counts, average widths, and perfectly selective pushdown: 9.2 MB instead of 184 MB. It does not prove actual source scans, network bytes, compression, join correctness, predicate equivalence, result size, source cost, latency, protection, or planner choice. Production decisions require observed plans, source metrics, semantic tests, workload distributions, and accountable review.

## Alternatives and Trade-Offs

**Federation versus materialization.** Federation avoids planned durable copies and can expose current source state but adds runtime dependency and source load. Materialization stabilizes service and history while adding synchronization and storage.

**Virtual view versus source API.** A view enables relational composition and planner optimization. An API constrains supported operations and source work but can make cross-source composition more explicit and application-oriented.

**Pushdown versus central execution.** Pushdown reduces movement and uses source engines but risks semantic differences and source contention. Central execution standardizes operators while moving more protected data.

**Delegated identity versus service identity.** Delegation preserves source policy and attribution but requires compatible trust. Service identities simplify connections while concentrating privilege and enforcement.

**Live mixed reads versus coordinated snapshots.** Live reads reduce staleness and coordination but can combine impossible states. Snapshots improve consistency while increasing storage, latency, or source constraints.

**Transparent cache versus governed product.** Caches accelerate the same logical contract within a freshness bound. Reusable durable results need product ownership, semantics, service, protection, and lifecycle.

**One federation layer versus domain layers.** One layer centralizes operations and discovery but concentrates failure and semantic work. Domain-aligned layers preserve context while requiring interoperable metadata and cross-layer planning.

**Flexible query versus curated views.** Flexibility supports exploration but creates unpredictable workload and inference. Curated products bound meaning, protection, and capacity at the cost of additional design.

**Partial result versus all-or-nothing failure.** Explicit partial results may aid exploration during source failure. Consequential decisions often require complete failure to prevent misleading use.

**Zero-copy aspiration versus minimal-copy evidence.** Avoiding unnecessary durable replication reduces exposure. Runtime transfer, spill, caches, and results still create copies that must be governed.

## Failure Modes and Misconceptions

1. **A connected catalog provides semantic integration.** Meaning and authority still require mappings.
2. **Same field names mean same concepts.** Identity, grain, units, time, and definitions can differ.
3. **Virtualization means no copies.** Buffers, shuffles, spills, caches, results, and exports copy data.
4. **Pushdown is always faster.** Source load, indexes, selectivity, and network paths vary.
5. **Pushdown preserves semantics automatically.** Null, collation, precision, timezone, and error rules can differ.
6. **One query sees one point in time.** Autonomous sources usually have independent read boundaries.
7. **Current access means fresh data.** Replicas and caches can be stale.
8. **Result size equals query cost.** Sources may scan and shuffle far more data.
9. **A service identity is equivalent to delegation.** Attribution and native policy are lost or shifted.
10. **Central filtering protects source data.** Unauthorized rows may already have moved.
11. **Rate limits protect every source.** Query complexity, concurrency, locks, and skew matter.
12. **Cancellation ends remote work.** Weak connectors can leave orphan queries running.
13. **Retry returns the same answer.** Sources can change between executions.
14. **Cache fallback is harmless.** Staleness, authorization, and incomplete sources affect meaning.
15. **A compiling view is compatible.** Definitions and authority can change without syntax failure.
16. **Engine uptime is product availability.** Connectors, sources, identity, and correctness remain.
17. **Dropping a view retires federation.** Grants, connectors, caches, exports, credentials, and source load remain.

## Worked Examples

### Example 1

CRM and Billing both expose `customer_id`, but one is tenant-local and the other enterprise-wide. Direct equality joins unrelated customers. A governed crosswalk includes namespace, confidence, effective time, owner, and correction. **Conclusion:** structural key equality is not identity equivalence.

### Example 2

A customer-to-invoice join returns one row per invoice while a dashboard sums customer credit limit on every row. Declared grains and pre-aggregation prevent multiplication. **Conclusion:** federated joins must preserve output grain explicitly.

### Example 3

Source A treats text comparison case-insensitively; the virtual engine is case-sensitive. Pushing `status='active'` changes membership. Compatibility tests disable that pushdown and evaluate centrally. **Conclusion:** predicate movement is a semantic transformation.

### Example 4

Filters reduce estimated input from 184 MB to 9.2 MB. Source metrics show the remote database still scans the full table because no index supports the predicate. **Conclusion:** reduced network movement does not prove reduced source work.

### Example 5

A query reads Inventory at 10:00 and Orders at 10:04. It reports negative available stock that never existed at one instant. The product labels four-minute skew and uses a materialized coordinated snapshot for financial decisions. **Conclusion:** cross-source time needs a contract.

### Example 6

A consumer cancels a query after timeout, but the connector does not propagate cancellation. The source continues a forty-minute scan. Runtime observation and a source-side statement timeout close the gap. **Conclusion:** client cancellation is not evidence of remote resource release.

### Example 7

One shared connector identity can read every patient row; central policies filter results. A spill file contains the unfiltered join input. Source-side purpose policy, delegated context, encrypted spills, and minimized projection reduce exposure. **Conclusion:** protection must apply before and during movement.

### Example 8

A cache serves during a source outage but is twelve hours old and lacks new deletions. The virtual product exposes source status and age and refuses a consequential eligibility decision while allowing labeled exploration. **Conclusion:** degraded data requires use-specific policy.

### Example 9

A recurring weekly query scans three sources and repeatedly spills two terabytes. A governed aggregate product cuts source load and supplies reproducible history. **Conclusion:** repeated federation can be evidence that materialization has better lifecycle economics.

### Example 10

After a view is dropped, scheduled notebooks still use its service credential directly against sources and cached exports remain. Retirement revokes grants and credentials, removes caches and jobs, updates lineage, and verifies load cessation. **Conclusion:** logical-object deletion is only one closure action.

## Cross-Program Connections

- **Database engineering:** query planning, statistics, joins, transactions, snapshots, indexes, isolation, foreign tables, and source protection underlie federation.
- **Distributed systems:** partial failure, deadlines, retries, cancellation, clocks, consistency, caches, and fault propagation shape runtime behavior.
- **Data engineering:** connectors, query engines, transformations, materialization, lineage, quality, and serving implement virtual products.
- **Platform engineering:** catalogs, identity, workload classes, quotas, observability, connector lifecycles, self-service, and cost controls sustain the layer.
- **Cybersecurity and privacy:** delegation, least privilege, purpose, row and field policy, inference, spills, caches, residency, deletion, and audit constrain queries.
- **Software architecture:** bounded contexts, anti-corruption mappings, facades, dependency direction, ownership, and product boundaries locate semantics.
- **API and service engineering:** source APIs, contracts, rate limits, errors, compatibility, and service objectives provide constrained federation endpoints.
- **Systems engineering:** interface assurance, capability matrices, fault analysis, trade studies, configuration, verification, and lifecycle govern the whole system.

## References

1. PostgreSQL Global Development Group, *postgres_fdw*, PostgreSQL Documentation. <https://www.postgresql.org/docs/current/postgres-fdw.html>
2. Trino Software Foundation, *Connector Documentation*. <https://trino.io/docs/current/connector.html>
3. W3C, *SPARQL 1.1 Federated Query*, W3C Recommendation, 2013. <https://www.w3.org/TR/sparql11-federated-query/>
4. W3C, *Data on the Web Best Practices*, W3C Recommendation, 2017. <https://www.w3.org/TR/dwbp/>
5. W3C, *PROV-O: The PROV Ontology*, W3C Recommendation, 2013. <https://www.w3.org/TR/prov-o/>
6. Beyer, B., Jones, C., Petoff, J., and Murphy, N. R., eds., *Site Reliability Engineering: Addressing Cascading Failures*, Google, 2016. <https://sre.google/sre-book/addressing-cascading-failures/>
7. NIST, *Zero Trust Architecture*, SP 800-207, 2020. <https://csrc.nist.gov/pubs/sp/800/207/final>
8. NIST, *Systems Security Engineering: Considerations for a Multidisciplinary Approach in the Engineering of Trustworthy Secure Systems*, SP 800-160 Volume 1 Revision 1, 2022. <https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final>

## Exercises

### Exercise 1

Define a virtual Customer Revenue product across CRM and Ledger, including authority, keys, grain, time, mappings, service, protection, evidence, and lifecycle.

### Exercise 2

Analyze a federated join with one million 160-byte left rows and 200,000 120-byte right rows. Compare full movement with selective pushdown and state limitations.

### Exercise 3

Design source protection for interactive exploration and scheduled analytical workloads sharing three operational sources. Include admission, quotas, cancellation, retries, and observability.

### Exercise 4

Compare delegation and service identity for a protected cross-source view, including row and field policy, inference, audit, caches, spills, and providers.

### Exercise 5

Decide which of twenty recurring federated queries should remain virtual and which should become materialized products. Define evidence, migration, rollback, and retirement.

## Answers to the Exercises

### Answer 1

Name CRM Customer assertions and Ledger revenue postings separately, with each source product, owner, service, schema, quality, and classification. Define a governed identity crosswalk with namespaces, confidence, effective interval, errors, and correction. Output grain is one customer per declared revenue interval; revenue definition, currency conversion, exclusions, nulls, refunds, late postings, and customer status are explicit. Preserve field-level source authority and transformation provenance.

State whether source reads are independent, snapshot-based, or as-of; record each read boundary, replica and cache age, maximum skew, and prohibition on point-in-time claims when appropriate. Specify connector types and capabilities, pushed filters, join placement, data movement, workload limits, failure and partial-result policy, availability, latency, freshness, completeness, correction, and support. Propagate identity or apply source-scoped service credentials plus purpose-aware row and field policy before movement. Protect intermediates, spills, caches, logs, and exports. Observe plans, versions, source calls, bytes, policy decisions, lineage, and consumers. Govern schema and semantic changes, materialization thresholds, deprecation, credential revocation, cache disposal, and verified closure.

### Answer 2

Full input movement is $1{,}000{,}000\times160+200{,}000\times120=184{,}000{,}000$ bytes. If verified source predicates reduce inputs to 50,000 and 10,000 rows at the same widths, movement is $50{,}000\times160+10{,}000\times120=9{,}200{,}000$ bytes. Nominal avoided movement is 174,800,000 bytes and the ratio is 0.05.

This excludes compression, protocol overhead, result and shuffle bytes, serialization, spills, retries, and source scans. The source may scan full tables despite returning fewer rows. Predicate semantics can differ through nulls, collation, timezone, types, or errors. Authorization may require source-side filtering, and pushdown can burden an operational source. Use observed physical plans, source metrics, network telemetry, semantic fixtures, workload distributions, and consumer outcomes before choosing placement.

### Answer 3

Classify interactive and scheduled workloads by consumer, purpose, source, expected rows and bytes, complexity, concurrency, freshness, priority, and consequence. Authenticate before planning. Maintain per-source capability and safety envelopes from source owners. Admit interactive queries under low row, byte, time, and concurrency limits; use curated views and result pagination. Put scheduled analytics in separate workload groups and windows, with scan, join, spill, and source budgets. Route heavy recurring work to replicas or materialized products.

Set end-to-end deadlines and propagate cancellation; add source-side statement timeouts when connectors cannot confirm it. Use bounded retries with backoff, jitter, maximum attempts, and shared budgets, recognizing that retry may see new data. Circuit-break sources under stress and reject or queue work explicitly. Observe logical and physical plans, estimates versus actuals, connections, locks, scans, rows, bytes, source latency, shuffles, spills, cache, retry, cancellation confirmation, failures, and source health. One consumer cannot borrow critical source capacity without authorized exception. Test skew, missing statistics, source failure, orphan queries, and recovery.

### Answer 4

Delegation carries attributable user or workload context to each source, allowing native row and field policies and source audit. It requires compatible identity, audience, token exchange, trust, revocation, and consistent purpose semantics. A service identity simplifies connection pooling and heterogeneous sources, but it concentrates broad privilege and moves enforcement and attribution to the virtual layer. Use separate source- and product-scoped identities rather than one universal account.

In either model, authorize consumer, purpose, subject relationship, fields, rows, region, time, and query shape before movement. Minimize projections and push filters only after semantic tests. Defend against inference through joins, counts, errors, timing, and repeated queries. Encrypt and restrict shuffles, spills, caches, logs, and exports; include identity and purpose in cache keys; apply residency, retention, deletion, provider, and incident rules. Record policy version, source decisions, virtual-layer decisions, actual sources and fields, and consumer outcome. Fail closed on delegation or policy mismatch.

### Answer 5

For each query record consumers, purpose, frequency, parameters, source products, meanings, keys, grain, time, source and result bytes, scans, joins, spills, cache, latency, freshness, failures, source impact, protection, reproducibility, change, and cost. Keep virtual queries that are selective, variable, low-volume, tolerant of runtime dependency and mixed-time semantics, and safe for sources. Materialize recurring large joins, expensive scans, reusable derived meaning, historical results, strict service, or workloads that repeatedly threaten sources.

Define each materialized product's owner, source authority, transformation, grain, time, refresh, quality, service, protection, correction, and lifecycle. Run old virtual and new materialized results in parallel, comparing keys, values, nulls, aggregates, time, completeness, policy, performance, and decisions. Explain intended freshness differences and preserve rollback. Redirect consumer cohorts and monitor use. Retire virtual paths by removing views, grants, connector access, service identities, scheduled queries, caches, spills, exports, alerts, and documentation, updating lineage and preserving required audit and provenance. Verify source load and access have ceased.
