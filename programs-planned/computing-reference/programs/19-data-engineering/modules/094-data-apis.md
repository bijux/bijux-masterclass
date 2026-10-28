---
module_id: DE-094
program: Data Engineering
level: 2
module_number: 94
title: Data APIs
status: complete
last_verified: 2026-09-03
---

# Data APIs

## One-Page Review

### Governing question

How can a team expose governed records, metrics, datasets, and analytical results through an API whose identity, schema, authorization, snapshot, query cost, pagination, freshness, provenance, and lifecycle are explicit—without turning a warehouse into an unbounded remote SQL endpoint or returning plausible but semantically inconsistent data?

### Essential definitions

- A **data API** is a programmatic contract for retrieving or operating on governed data products, records, metrics, query results, or extracts.
- A **logical data product** is the stable consumer-facing meaning; a **physical source** is one implementation used to serve it.
- A **dataset identity** names the governed collection and its owner, grain, key, semantics, classification, and lifecycle.
- A **contract version** identifies request, response, behavior, and semantic guarantees; a **schema version** identifies fields and types.
- A **snapshot** is the immutable logical boundary against which a request or multi-page traversal is evaluated.
- A **query capability** is an allowed filter, projection, grouping, ordering, or aggregation expressed through a bounded grammar or named template.
- A **cursor** is opaque continuation state bound to the query, authorization, ordering, contract, and snapshot.
- A **query budget** bounds work using dimensions such as bytes scanned, rows, partitions, cardinality, execution time, memory, concurrency, and result size.
- An **asynchronous query resource** gives long work a stable identity and lifecycle separate from the initiating request.
- **Freshness** is age relative to an authoritative source boundary; **consistency** describes which mutually compatible state a response may observe.
- **provenance** records the product, source boundary, transformation, schema, policy, query, execution, and artifact identities behind a result.
- **inference risk** is disclosure derived from permitted answers, differences, counts, timing, errors, or repeated queries rather than a directly returned forbidden field.

### Central model, mechanism, or theorem

Treat every accepted request as a bound execution claim

$$
R=(u,p,d,c,s,q,o,b),
$$

where principal $u$ acts for purpose $p$ on data product $d$, contract/schema generation $c$, snapshot $s$, normalized query $q$, deterministic order $o$, and budget $b$. Authorization and minimization produce an allowed projection $A(u,p,d,q,s)$; execution is valid only when the returned rows and fields are a subset of $A$, the work remains within $b$, and the receipt records the same bindings.

For keyset pagination, order by a unique total key $K(r)$. Page $i+1$ is

$$
P_{i+1}=first_n\{r\in D_s:Q(r)\land K(r)>K(last(P_i))\}.
$$

If snapshot $s$, normalized query, authorization generation, order, and cursor integrity stay fixed, pages neither repeat nor skip members of that snapshot. Offset pagination over changing state does not have this property.

### Critical invariants

- Every surface resolves to one owned data product with declared grain, stable key, field meanings, units, time semantics, classification, quality, freshness, and retirement policy.
- Authentication is not authorization. Every request is authorized at product, tenant, row, column, operation, purpose, and output level before release.
- Clients choose only documented capabilities. Raw SQL, arbitrary expressions, joins, functions, paths, or sort keys are denied unless an intentionally sandboxed query product governs them.
- Query text and cursor state cannot override tenant or policy predicates; security predicates are composed server-side and remain non-bypassable.
- Pagination uses deterministic unique ordering and a cursor bound to query, snapshot, identity, policy, contract, expiry, and page constraints.
- Response schema distinguishes absence, null, redaction, unknown, zero, empty, and unavailable; numeric precision, units, timezone, timestamp, and interval conventions are explicit.
- Admission occurs before expensive planning or execution. Every query, job, export, and stream has bounded work, output, duration, concurrency, and retention.
- Request success, job acceptance, job completion, result publication, download completion, and consumer use are distinct states.
- Caches include every representation and authorization dimension or store only safely reusable material; revocation and deletion have bounded invalidation paths.
- Responses and artifacts carry stable request/job IDs, product and schema versions, snapshot/freshness evidence, pagination state, and safe provenance.

### Common failures

Wrapping arbitrary SQL in JSON; authorizing the endpoint but not the referenced rows or fields; trusting a client-supplied tenant filter; leaking hidden columns through sorting, grouping, counts, errors, timing, or metadata; using sequential object IDs as authorization; returning database types without an API type contract; silently rounding decimals; mixing local times; changing null meaning; paginating mutable data with offset; omitting a unique tie-breaker; putting raw filters or secrets in cursors; letting a cursor outlive revocation; counting only response bytes while scans explode; waiting synchronously for warehouse work; treating `202 Accepted` as completed; caching across principals; excluding policy from cache keys; exporting presigned URLs with excessive lifetime; exposing internal table names and plans; logging sensitive query values; changing metric definitions without contract evolution; and deleting the endpoint while old exports, jobs, cursors, or SDKs remain active.

### Compact example

An orders API supports `status`, `created_after`, and `region` filters; a fixed projection set; and ordering by `(created_at, order_id)`. A request is normalized, tenant and row policy are injected server-side, estimated scan is checked against a 2 GiB budget, and snapshot `S184` is selected. The first 100 rows and an HMAC-protected cursor bind tenant, policy generation, normalized query hash, snapshot, order, last key, page size, and expiry. An order inserted later cannot shift the traversal because it is outside `S184`; a revoked principal cannot use the old cursor because authorization is rechecked. **Conclusion:** the continuation token represents the same governed query, not merely a place in a table.

### Connections

[DE-076](076-data-contracts.md) supplies product contracts, [DE-086](086-access-control-for-analytical-data.md) supplies analytical authorization, [DE-089](089-auditability-and-provenance.md) supplies evidence, and [DE-091](091-warehouses-query-engines-and-serving-stores.md) supplies workload placement. [API-021](../../28-api-and-service-engineering/modules/021-api-contracts-and-behavioral-guarantees.md), [API-017](../../28-api-and-service-engineering/modules/017-filtering-sorting-and-pagination.md), and [API-090](../../28-api-and-service-engineering/modules/090-evolving-an-api-without-coordinated-consumer-releases.md) provide general API semantics that this module specializes for governed data.

## Governing Question

For a particular data consumer and decision, what named data product, semantic version, authoritative boundary, permissible query language, authorization policy, consistency/freshness class, resource budget, result representation, and lifecycle make every response interpretable and every expensive or sensitive action bounded?

## Why This Matters

Data access often begins as a direct warehouse query, shared view, notebook, or file. These interfaces are flexible for exploration but make stable application integration difficult. Credentials are broad, physical schemas leak, queries compete unpredictably, consumers infer undocumented semantics, and definition changes arrive without negotiation. A data API can create a narrower and more durable boundary—if it governs data meaning and execution rather than merely translating HTTP into SQL.

The word “data” changes the risk profile of otherwise familiar API design. Results may contain thousands of rows and hundreds of megabytes. One short filter expression may scan petabytes or create a high-cardinality join. A request can be syntactically read-only while exposing a sensitive cohort, exhausting shared compute, or reconstructing protected facts through repeated counts. Analytical state also changes while clients paginate, cache, or retry, so a set of individually correct responses can form an impossible whole.

Data APIs span several shapes. Record APIs fetch known entities. Dataset APIs enumerate governed collections. Metric APIs return centrally defined measures over dimensions and time. Query APIs accept bounded analytical expressions or named templates. Export APIs publish immutable bulk artifacts. Streaming APIs transfer columnar batches or incremental changes. Each has a different latency, cost, consistency, and authorization envelope; one endpoint should not pretend they are interchangeable.

The durable abstraction is a logical product contract. Consumers should depend on `recognized_revenue` with a declared grain, currency, recognition rule, effective time, and version—not on warehouse table `finance_mart_v17`. Physical warehouses, serving stores, indexes, materialized views, and engines can then change behind the boundary. The API is valuable when it narrows choices, preserves meaning, meters work, and supplies evidence.

## Prerequisites and Retrieval

Retrieve the consumer decision, application workflow, latency/throughput needs, interactive or batch shape, expected cardinality, required fields, permissible staleness, consistency need, retry behavior, SDK/runtime constraints, and failure consequences. Identify whether a human exploration tool, governed query service, record API, metric API, export, event stream, or replicated serving store is actually appropriate.

Retrieve product semantics: owner, purpose, grain, primary/business keys, dimensions, measures, aggregation rules, units/currency, event/effective/processing time, timezone/calendar, null/unknown/redacted meaning, slowly changing dimensions, corrections, deletion, schema and definition versions, source-of-truth boundary, lineage, quality checks, freshness SLO, classification, retention, and deprecation.

Retrieve interface behavior: operations, identifiers, filter/projection/order grammar, defaults, pagination, maximum pages, field masks, expansions, aggregations, format negotiation, compression, conditional requests, idempotency, errors, quotas, deadlines, cancellation, asynchronous states, callbacks or polling, result expiration, partial results, and SDK compatibility.

Retrieve execution facts: logical-to-physical resolution, materializations and indexes, optimizer and statistics behavior, bytes/partitions/rows scanned, intermediate cardinality, memory/spill, concurrency pools, tenant fairness, cache layers, cold starts, warehouse reservations, cost attribution, result storage, and downstream bandwidth.

Retrieve security and governance: principal/workload identity, tenant/account, delegated actor, purpose, product/row/column/cell policy, consent, region, legal holds, export approval, aggregation thresholds, differential privacy where justified, rate and query-history controls, credential scope, encryption, audit, incident response, and revocation latency.

Retrieve lifecycle evidence: active consumers and versions, contract tests, schema registry, usage telemetry, cursor/job/export populations, migration and rollback, old representations, cache invalidation, historical snapshots, retained artifacts, deletion propagation, owner/on-call, dependency inventory, and retirement criteria.

Distinguish logical product from physical relation; record identity from row position; schema version from data snapshot; freshness from request latency; consistency from recency; filter from authorization; projection from redaction; query success from semantic validity; estimate from hard execution limit; request completion from job completion; job completion from result retrieval; page cursor from authorization grant; cache validity from policy validity; and operational reliability from consumer decision correctness.

Write a data API contract:

| Concern | Required decision and evidence |
|---|---|
| Product | Owner, purpose, grain, key, semantics, classification and lifecycle |
| Contract | Operations, schema/definition versions, types, errors and compatibility |
| Query | Named capability grammar, allowed fields/functions, normalized form and limits |
| State | Snapshot, freshness, consistency, correction and deletion behavior |
| Security | Principal, tenant, purpose, row/column policy, inference controls and revocation |
| Resources | Estimate, admission, scan/cardinality/output/deadline/concurrency budgets and cost |
| Delivery | Pagination, async job, export/stream, compression, integrity and expiry |
| Evidence | Request/job identity, provenance, metrics, audit, reconciliation and consumer tests |

Write a falsifiable claim: “API surface A version C exposes product D at one row per `(tenant,order_id)` using schema S and policy P; accepts only named filters F and order O; resolves each traversal to snapshot B; admits work below measured budgets Q; emits decimals as strings with declared currency and timestamps as UTC instants; rechecks row/column authorization on each page and download; records receipt R; completes within the interactive SLO or transitions to bounded job J; and deprecates only after usage, artifact, cursor, and consumer evidence meet retirement rule E.”

## Learning Objectives

After completing this module, you should be able to:

1. distinguish record, dataset, metric, query, export, and streaming data APIs and choose among them;
2. define logical product identity, grain, keys, measures, units, time, null, schema, definition, snapshot, and provenance semantics;
3. design bounded filters, projections, expansions, aggregations, ordering, parameterized templates, and safe physical resolution;
4. implement snapshot-bound keyset pagination and explain why mutable offset traversal can duplicate or omit rows;
5. enforce product-, tenant-, row-, column-, purpose-, operation-, and output-level authorization without trusting client predicates;
6. assess inference, enumeration, query-history, metadata, error, timing, cache, log, and export disclosure;
7. estimate and enforce scan, cardinality, memory, duration, concurrency, output, storage, and monetary budgets;
8. design synchronous responses, asynchronous query resources, bulk artifacts, and columnar streams with honest state transitions;
9. evolve data/API semantics, schemas, jobs, cursors, caches, and consumers through compatible migrations; and
10. measure semantic correctness, freshness, security, cost, reliability, and consumer outcomes independently.

## Core Exposition

### Choose the narrowest honest API shape

Start from a decision and workload. A service rendering one account needs a record lookup with predictable point latency. A dashboard needs a small set of governed metrics. A partner integration may need a daily immutable export. A data-science client transferring millions of typed values may need a columnar stream. A bounded analytical application may need an asynchronous query resource. Giving every use case arbitrary SQL maximizes apparent flexibility while transferring semantic, security, and resource governance to every consumer.

A record API exposes domain entities and usually supports known identifiers plus constrained collection navigation. A dataset API exposes rows at a declared grain and supports bounded selection. A metric API owns aggregation semantics and dimensional eligibility; it must not let each client redefine numerator, denominator, attribution, or calendar. A query API accepts either named query templates with typed parameters or a deliberately limited language. An export API creates an immutable artifact with manifest, checksum, expiry, policy, and receipt. A streaming data API moves batches efficiently but still requires schema, authentication, flow control, deadlines, and cancellation.

Keep commands separate from reads. Creating an export or query job is a state-changing operation even when the underlying query is read-only: it consumes compute, stores a result, may trigger billing, and can create a sensitive artifact. Give it idempotency, ownership, quotas, cancellation, retention, and audit behavior. Do not overload `GET` with hidden expensive job creation whose effects intermediaries may repeat.

### Define product identity above storage

Name a stable product and owning team. Define one row/observation grain, stable keys, field dictionary, dimensions, measures, units, allowed aggregations, update cadence, classification, quality, retention, and consumers. A response schema alone cannot express that `revenue` is net recognized USD at invoice-line grain under policy version 4. Semantic definitions and examples are contract artifacts.

Resolve the logical product to a physical view, materialization, index, serving store, or engine behind an internal adapter. Record the resolution generation in provenance, but do not expose physical table names as durable client identity. This allows migration and workload routing while the external meaning remains stable. When the meaning changes, evolve the definition honestly even if the JSON shape does not.

Distinguish three identities: contract version describes API behavior; schema/definition version describes types and meaning; snapshot identifies data state. A consumer may request contract `v2`, receive schema `orders-7`, and traverse snapshot `S184`. Never label a new snapshot as a new schema version merely because values changed.

### Specify types and semantic edges

Map storage types into an explicit wire model. JSON numbers do not preserve every decimal or 64-bit integer through every runtime. Represent money and other exact decimals using a declared decimal string or a typed binary format; include currency or unit. Define scale, rounding mode, overflow, NaN/infinity policy, and whether zero differs from missing. Test generated SDK behavior.

Timestamps need an instant representation, timezone/offset rules, precision, leap-second stance, and inclusive/exclusive interval conventions. Dates are not midnight timestamps. Local business periods require a calendar and zone. Distinguish event time, effective time, ingestion time, processing time, and snapshot/as-of time in names and metadata.

For every field, define absent, null, unknown, not applicable, withheld/redacted, not yet computed, and deleted. A redacted property should not masquerade as a genuine null if consumers make different decisions. Collections distinguish empty from omitted and may be partial only when marked. Enumerations require unknown-value behavior. Maps and open objects need key/value constraints; otherwise they become uncontrolled schema escape hatches.

JSON Schema can validate structural constraints, but semantic units, authority, aggregation, policy, freshness, and cross-field meaning require additional contract and tests. A `format` annotation should not be assumed to prove real-world identity or deliverability. Validate at the boundary, preserve exact rejected-path evidence safely, and avoid echoing secrets or forbidden values in errors.

### Design a bounded query language

Prefer named filters and typed query templates. Publish allowed fields, operators, combinations, maximum list sizes, range widths, nesting, expansion depth, group dimensions, aggregations, sort keys, and output columns. Parse into an abstract syntax tree, validate against the product contract, normalize to a canonical representation, authorize referenced concepts, estimate cost, then compile with bound parameters.

Never concatenate client strings into SQL. Parameterization protects values but not arbitrary identifiers, operators, table names, functions, or query structure; those require allowlists and grammar validation. Security predicates such as tenant, residency, purpose, and row policy are injected from trusted server context, not accepted as client-provided filters. The compiled physical plan must preserve them through joins, views, caching, and materialization.

Bound pathological shapes before execution: giant `IN` lists, unanchored patterns, deep Boolean trees, broad date ranges, high-cardinality grouping, Cartesian joins, recursive paths, expensive functions, arbitrary regular expressions, and large expansions. Reject unsupported operators rather than silently ignore them. Return a stable machine-readable problem type, safe field/path detail, retryability, and request ID.

OData demonstrates a standardized family of query options, but implementing a syntax does not require supporting every option; unsupported capabilities must be rejected. Likewise, GraphQL selection does not itself bound resolver fan-out. Capability discovery should state the implemented subset and its cost/authorization rules.

### Bind pagination to a stable query

Offset pagination is understandable but unstable under concurrent insertion and deletion and increasingly expensive on many stores. If a row is inserted before offset 100 between requests, the original row 100 can repeat; if a row is deleted, another can be skipped. Offset may remain acceptable for small immutable sets or approximate human browsing when its limitations are explicit.

For stable traversal, establish snapshot $s$ and unique total order $K$. Append a stable unique key to any nonunique client sort. The cursor contains—or refers server-side to—contract/schema generation, normalized query hash, product, snapshot, order, last key, tenant/principal or authorization context, page size policy, issued time, expiry, and nonce. Sign or encrypt it as appropriate, treat it as opaque, and limit its size.

Reauthorize every continuation. A signed cursor proves server issuance and integrity, not current permission. If policy or product changes incompatibly, return an explicit expired/invalid continuation problem instead of silently switching snapshots or filters. Prevent a client from increasing page size, changing projection, or replaying a cursor across tenants. Do not place sensitive raw filters or credentials in readable tokens.

Define whether the snapshot is transaction, materialization generation, commit sequence, or bounded as-of watermark. If the backend cannot retain it for cursor lifetime, shorten expiry, materialize results, or disclose weaker semantics. Releasing a snapshot between pages while claiming stable traversal is a correctness bug.

### Govern authorization and inference

Authenticate human or workload identity and preserve delegation. Authorize operation, product, tenant, object/row, column/property, purpose, region, and output. A user who may see one account is not authorized merely because the endpoint accepts account IDs. Random IDs reduce guessability but never replace object-level authorization.

Compose row predicates from server-side policy and verify them at the final serving boundary. Column policy applies not only to projection: forbidden fields can leak through filtering, ordering, grouping, distinct counts, joins, errors, and timing. A principal unable to read `diagnosis` may still infer it by comparing `count(*)` with and without a hidden predicate. Metadata—field names, partitions, distinct values, plans, statistics, and job history—also needs policy.

For aggregate interfaces, consider minimum cohort thresholds, suppression of complementary cells, query-history budgets, approved dimensions, rounding/noise, and differential privacy where its assumptions and utility are formally owned. A threshold on each query alone is insufficient when differences between overlapping permitted queries isolate one person. Record canonical queries and policy decisions for abuse analysis without logging unnecessary sensitive literals.

Enforce minimization after authorization and before serialization. Avoid generic object serialization that exposes newly added internal fields. Contract tests assert exact allowed output properties per role and purpose. Treat data export as privilege amplification because the provider loses online enforcement after release; bind recipients, purpose, watermarking where appropriate, expiry, encryption, and deletion obligations.

### Admit by work, not request count alone

A requests-per-second limit cannot distinguish a cached point lookup from a broad aggregation. Estimate scan bytes/partitions, candidate rows, join/group cardinality, memory, shuffle, execution time, result rows/bytes, storage, egress, and monetary cost. Estimates are uncertain; combine preflight gates with hard engine limits and runtime cancellation.

Use separate pools and budgets for interactive, batch, administrative, and urgent policy work. Fairness should account for tenant and cost, not only arrival order. Bound concurrent queries, queued jobs, per-principal work, daily export bytes, result retention, and outstanding downloads. Backfills should not starve interactive reads; one tenant should not consume a global warehouse reservation.

Admission happens before expensive parse/planning/execution where possible. A dry run or optimizer estimate is evidence, not a guarantee: statistics may be stale and intermediate explosion may appear only at runtime. Instrument actual versus estimated work and improve guards. If a limit is exceeded, cancel promptly, release resources, classify partial artifacts as unusable unless explicitly supported, and return safe retry or narrowing guidance.

Cache only after normalizing the full semantic key: product, definition/schema, snapshot or freshness class, normalized query, projection, representation/media type, locale/timezone, tenant, policy generation, and any principal dimension that affects results. Shared caches are unsafe when authorization differs. Conditional HTTP requests and validators can reduce transfer, but a validator identifies a representation; it does not authorize a now-revoked reader.

### Separate interactive requests from query jobs

Keep synchronous operations within a tested latency and output envelope. For longer work, create an asynchronous query resource with stable job ID, owner, normalized request, contract/schema/policy versions, snapshot choice, estimate/budget, idempotency key, state, timestamps, progress semantics, result reference, expiry, and terminal error. Return `202 Accepted` only as acceptance, never as completion.

A useful state machine distinguishes `accepted`, `admitted`, `planning`, `running`, `publishing`, `succeeded`, `failed`, `cancel_requested`, `cancelled`, `expired`, and possibly `unknown`. Define transitions and terminality. Cancellation is a request until the engine and publication path confirm it; a job can race to success. Retry job creation with the same idempotency identity and parameters, and do not duplicate work or artifacts.

Polling uses bounded backoff and validators or change tokens where useful. Webhooks need authentication, replay resistance, idempotent consumers, and a polling recovery path. Progress may be unknown and must not be fabricated from elapsed time. BigQuery's query method, for example, distinguishes an incomplete response with `jobComplete=false` from a completed result and supports dry-run statistics; treat such vendor behavior as a specific implementation, not a universal guarantee.

Publish result artifacts atomically only after schema, row count, checksum, policy, and completion metadata are ready. Presigned or delegated download URLs should be short-lived, scoped, revocable where feasible, and reauthorized before issuance. Result expiration removes both data and discoverable metadata according to policy. A completed job whose result expired has a different state from a failed job.

### Stream and export large results deliberately

For bulk transfer, prefer compressed, typed, splittable formats with an explicit manifest over a giant JSON array. Record schema fingerprint, product/definition version, snapshot, partitions/files, row and byte counts, checksums, compression, encryption, classification, created/expiry times, and producer. Consumers verify manifest and object integrity before publication or use.

For online columnar exchange, Arrow Flight defines operations such as schema discovery and `DoGet` streams identified by tickets; Flight SQL layers database/query metadata and result retrieval. Efficient transport does not supply product semantics, authorization, query budgets, or lifecycle automatically. Tickets remain capabilities that require scope, expiry, protection, and authorization appropriate to the implementation.

Apply backpressure and bounded batches. Track compressed and decoded bytes, because compression and nested values can expand dramatically. Define cancellation, resume, partition ordering, duplicates, checksums, partial download, and retry. A resumed export must address the same immutable artifact; a resumed live query without snapshot can silently change contents.

### Make evidence part of the response lifecycle

Return or make discoverable a stable request/job ID, product and contract/schema versions, snapshot/as-of boundary, generated time, freshness age or source boundary, pagination cursor, partial/complete marker, units/timezone, and safe warnings. Not every client needs full lineage in each row; provide a protected provenance endpoint or receipt keyed by request/job.

Record principal/workload and delegated actor, tenant, purpose, policy decision/generation, canonical query hash, allowed projection, product resolution generation, snapshot, estimate and actual resources, cache decision, status transitions, row/byte counts, result artifact and checksum, errors, and deletion/expiry. Protect logs because query parameters, identifiers, filters, samples, and plans can be more sensitive than ordinary application metadata.

Reconcile across boundaries. Compare response/job counts and checksums to the selected product snapshot where feasible; verify that policy-filtered counts plus excluded classifications account for the execution population; track accepted jobs with no terminal state, successful jobs with missing artifacts, expired data with lingering links, and cursors referencing unavailable snapshots. Audit evidence is useful only if identities and boundaries join.

### Evolve semantics and retire safely

Classify changes across syntax, schema, definition, authorization, consistency, freshness, ordering, pagination, limits, errors, cost, and artifacts. Adding a nullable field can expose sensitive data, break exact decoders, enlarge payloads, or change wildcard projections. Changing a metric formula with the same field name is a semantic break even when every type remains compatible.

Use expansion and coexistence. Add a new field/definition or contract version, dual-compute against the same snapshots, compare results with explained differences, migrate explicit consumers, and retain rollback until new writes/artifacts are readable by the old path where required. Bind cursors and jobs to their originating generation so deployment does not reinterpret them mid-flight.

Retirement requires more than endpoint traffic reaching zero. Inventory SDKs, scheduled jobs, cached responses, active query resources, downloadable artifacts, cursors, service accounts, dashboards, and downstream copies. Stop new creation, allow or explicitly invalidate bounded in-flight work, revoke credentials/links, expire results, remove policy and physical resolution, preserve required audit, and verify consumers migrated. Deprecation dates without usage and artifact evidence are aspirations.

## Definitions and Notation

Let $D$ be a logical data product and $D_s$ its state at snapshot $s$. Let $u$ be the authenticated principal, $a$ a delegated actor, $t$ the tenant, $p$ the declared purpose, $c$ the contract/schema/definition generation, and $P_g$ policy generation $g$.

Let a normalized query be $q=(f,\pi,gq,agg,o)$: filter $f$, projection $\pi$, grouping $gq$, aggregations $agg$, and unique total order $o$. The server constructs trusted predicate $\phi(u,a,t,p,P_g)$ independently of client input. Eligible rows and fields are

$$
E=authorize_{P_g}(u,a,t,p,D_s),\qquad Result=project_{allowed}(execute(D_s,f\land\phi,q)).
$$

Let budget vector $b=(B_{scan},N_{rows},C_{group},M,T,N_{out},B_{out},J)$ cover scan bytes, candidate rows, group cardinality, memory, duration, output rows/bytes, and concurrent jobs. Admission requires estimate $\hat w\preceq b$; runtime also enforces actual $w$ because $\hat w$ may be wrong.

Let $K(r)$ be a unique total ordering tuple and cursor

$$
z=protect(hash(q),D,c,s,P_g,u/t,K(last),n,expiry,nonce).
$$

Protection means authenticated integrity and, if contents are sensitive, confidentiality or an opaque server-side handle. It does not replace authorization. Let source boundary time be $T_s$, result publication time $T_p$, and observation time $T_o$; freshness age is $T_o-T_s$, whereas service latency is $T_p-T_{request}$. They answer different questions.

For an asynchronous job $j$, let state $X_j$ follow an explicit transition relation, and let receipt $R_j$ join request, policy, product, snapshot, execution, artifact, and terminal outcome identities. “Succeeded” is valid only after the complete artifact/result and receipt are atomically discoverable under the contract.

## Mechanisms, Invariants, or Proof Structure

### End-to-end request mechanism

1. Authenticate principal/workload and delegated actor; derive tenant, environment, purpose, and current policy context.
2. Resolve the stable product and requested contract/definition version; reject retired or unsupported generations explicitly.
3. Parse the request into a typed syntax tree; reject unknown fields, operators, duplicate parameters, excessive structure, and invalid type/unit/time values.
4. Normalize query, projection, grouping, order, representation, and defaults into one canonical form.
5. Authorize operation, product, rows, fields, purpose, metadata, and requested output; inject trusted security predicates.
6. Select or validate snapshot and consistency/freshness class; bind continuation to the same state.
7. Estimate work and output; enforce per-query, principal, tenant, workload-class, and global admission budgets.
8. Resolve logical product to approved physical plan with parameters; preserve policy predicates and record resolution generation.
9. Execute under hard scan, memory, duration, concurrency, cancellation, and output controls; isolate workloads.
10. Minimize and serialize only contract fields; verify schema, exact types, row/page bounds, and completeness markers.
11. Publish response, cursor, job, stream, or immutable artifact with version, snapshot, freshness, integrity, and expiry metadata.
12. Record actual cost, state, provenance, policy decision, cache use, errors, and terminal evidence; reconcile missing or contradictory states.

### Conditional claim: snapshot keyset traversal is complete and duplicate-free

**Claim.** Let $D_s$ be finite, $Q$ fixed, and $K$ a unique total order. Beginning below the minimum key, repeatedly return the first $n>0$ qualifying rows with $K(r)$ greater than the last returned key, always evaluated against $D_s$. The concatenated pages contain every row in $\{r\in D_s:Q(r)\}$ exactly once.

**Proof sketch.** Strict `>` makes page key ranges disjoint, so no row repeats. If an eligible row were omitted, choose the least omitted key. Every smaller eligible row is eventually returned because each nonfinal page advances to its maximum key by at most $n$ finite elements. The next page after that predecessor must include the least omitted row before any larger eligible row, a contradiction. The claim fails if order is nonunique, comparison semantics change, snapshot changes or disappears, query/policy changes, page size can be zero, or the cursor is forged/rebound.

### Conditional claim: output authorization is non-bypassable by client filters

**Claim.** Suppose trusted policy predicate $\phi$ and allowed projection $A$ are derived exclusively from authenticated server context, compilation always executes `client_filter AND phi`, output serialization can emit only $A$, and every physical/cached path is equivalent under those constraints. Then changing client filters or projections cannot directly return a row or property denied by $\phi$ or $A$.

**Proof sketch.** Conjunction cannot make a row failing $\phi$ satisfy the selection, and the serializer's codomain excludes properties outside $A$. The claim is limited to direct output. It fails with optimizer/policy bugs, unsafe joins, stale/mis-keyed cache, alternate endpoints, metadata/errors/timing, post-release copies, or inference from allowed aggregates. Those channels need separate controls and tests.

### Executable snapshot-bound cursor illustration

This deterministic fixture paginates a fixed commit boundary by `(event_time,id)`, inserts a later-version row whose sort key would disrupt an offset traversal, verifies exactly-once coverage of the original snapshot, and rejects a modified cursor. Its small keyed tag is deliberately non-cryptographic and exists only to make the binding test executable; production cursors require a standard authenticated construction plus key management, rotation, authorization, expiry, confidentiality where needed, and backend snapshot retention.

<!-- bijux-verify: {"id":"snapshot-keyset-cursor","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"page1=A,B\npage2=C,D\npage3=E\nall_ids=A,B,C,D,E\nduplicate_free=true\nsnapshot_excludes_late=true\ntamper_rejected=true\n","stderr":""}} -->
```python
secret = 7919
rows = [
    {"id": "A", "event_time": 10, "commit": 1},
    {"id": "B", "event_time": 10, "commit": 2},
    {"id": "C", "event_time": 20, "commit": 3},
    {"id": "D", "event_time": 30, "commit": 4},
    {"id": "E", "event_time": 40, "commit": 5},
]
snapshot = 5


def tag(body: tuple[object, ...]) -> int:
    return (secret + sum((index + 1) * ord(character) for index, character in enumerate(repr(body)))) % 1_000_003


def encode(last: tuple[int, str]) -> tuple[tuple[object, ...], int]:
    body = ("orders-7", "active", snapshot, last)
    return body, tag(body)


def decode(token: tuple[tuple[object, ...], int]) -> tuple[int, str]:
    body, supplied = token
    if supplied != tag(body):
        raise ValueError("invalid cursor")
    contract, query, cursor_snapshot, last = body
    assert contract == "orders-7"
    assert query == "active"
    assert cursor_snapshot == snapshot
    return last


def page(cursor: tuple[tuple[object, ...], int] | None) -> tuple[list[dict[str, int | str]], tuple[tuple[object, ...], int] | None]:
    last = decode(cursor) if cursor else (-1, "")
    eligible = sorted(
        (row for row in rows if row["commit"] <= snapshot and (row["event_time"], row["id"]) > last),
        key=lambda row: (row["event_time"], row["id"]),
    )
    selected = eligible[:2]
    next_cursor = encode((selected[-1]["event_time"], selected[-1]["id"])) if len(eligible) > 2 else None
    return selected, next_cursor


seen = []
cursor = None
page_number = 0
while True:
    selected, cursor = page(cursor)
    page_number += 1
    ids = [str(row["id"]) for row in selected]
    print(f"page{page_number}={','.join(ids)}")
    seen.extend(ids)
    if page_number == 1:
        rows.append({"id": "X", "event_time": 15, "commit": 6})
    if cursor is None:
        break

print(f"all_ids={','.join(seen)}")
print(f"duplicate_free={len(seen) == len(set(seen))}".lower())
print(f"snapshot_excludes_late={'X' not in seen}".lower())

valid = encode((10, "B"))
tampered_body = valid[0][:-1] + ((10, "Z"),)
tampered = tampered_body, valid[1]
try:
    decode(tampered)
    rejected = False
except (ValueError, AssertionError):
    rejected = True
print(f"tamper_rejected={rejected}".lower())
```

## Alternatives and Trade-Offs

- **Direct warehouse access versus data API:** direct access maximizes exploration and existing tooling; an API narrows semantics, authorization, cost, and lifecycle for operational consumers. Mature estates often need both with distinct policy.
- **Record endpoint versus flexible query:** fixed record operations are predictable and cacheable; flexible queries serve more questions but expand cost, inference, and compatibility surfaces.
- **Named template versus bounded DSL:** templates are easiest to govern and optimize; a DSL reduces endpoint proliferation but requires a real parser, capability model, cost system, and evolution policy.
- **REST/JSON versus typed RPC/columnar streaming:** JSON is widely interoperable and debuggable; typed columnar protocols preserve schema and throughput better for large analytical results but require specialized clients and governance.
- **Synchronous versus asynchronous:** synchronous calls simplify consumers within tight bounds; jobs handle long work and artifacts honestly but introduce state, polling, idempotency, expiry, and cleanup.
- **Offset versus keyset pagination:** offset supports jumping to approximate positions; snapshot-bound keyset traversal offers scalable stable continuation but cannot cheaply jump to an arbitrary page and requires cursor lifecycle.
- **Live snapshot versus materialized result:** live snapshots reduce storage and may be fresher; materialized results isolate pagination/download and preserve reproducibility at storage and expiry cost.
- **Client-selected projection versus fixed views:** projection reduces payload and supports varied needs; fixed views simplify authorization, caching, compatibility, and semantic review.
- **Fresh reads versus cached reads:** fresh reads reduce staleness but cost more and can overload sources; caches improve latency/cost only when semantic and authorization keys plus invalidation are correct.
- **Presigned artifact versus proxied download:** presigned objects scale transfer and offload servers; proxying retains online authorization and revocation but adds bandwidth and availability burden.
- **Hard rejection versus automatic rewrite:** rejection makes budgets explicit; rewriting range, aggregation, sampling, or precision may be useful only when disclosed and semantically accepted, never silently.
- **Exact aggregates versus privacy mechanisms:** exact answers maximize analytical precision; thresholds, contribution bounds, suppression, or formal noise reduce inference with domain-specific utility and composition costs.
- **Physical transparency versus abstraction:** exposing plans and tables aids expert debugging; abstraction preserves migration and can reduce information leakage. Provide protected evidence without making internals contractual.
- **Global version versus capability negotiation:** global versions are understandable but coarse; capability/field negotiation reduces duplication while making coexistence and cache keys more complex.

## Failure Modes and Misconceptions

1. **“It is read-only, so it is safe.”** Reads can disclose, infer, exhaust compute, incur cost, and create durable exports.
2. **“Authentication authorizes the row.”** Identity establishes who called; policy must decide which operation, object, row, field, purpose, and output are allowed.
3. **“The tenant ID in the filter isolates tenants.”** Client filters are untrusted. Tenant predicates come from authenticated server context and survive every physical path.
4. **“Random IDs solve object authorization.”** Unpredictability reduces discovery, not permission checks.
5. **“Parameterized SQL makes arbitrary query APIs safe.”** Parameters protect values; arbitrary identifiers, functions, joins, structure, cost, and inference still require control.
6. **“A schema defines the data contract.”** It does not fully define grain, units, metric formulas, time, quality, policy, freshness, or lifecycle.
7. **“JSON numbers preserve warehouse numerics.”** Client runtimes may round large integers and decimals; exact types need explicit encoding.
8. **“Null means missing.”** It may mean unknown, inapplicable, redacted, deleted, not computed, or intentionally cleared.
9. **“Request latency measures freshness.”** A fast response can serve old data; source-boundary age and service latency are separate.
10. **“Latest is a snapshot.”** Without an immutable boundary, pages and retries can observe incompatible states.
11. **“Offset pagination is stable if ordered.”** Concurrent changes before the offset can still duplicate or omit rows.
12. **“Ordering by timestamp is total.”** Equal timestamps require a deterministic unique tie-breaker and stable comparison semantics.
13. **“A signed cursor remains authorized.”** It proves integrity, not current identity, permission, retention, or snapshot availability.
14. **“Opaque cursors may contain anything.”** Clients can decode unsigned/base64 state; sensitive contents require confidentiality or server-side handles.
15. **“One rate limit controls cost.”** Request count ignores scan, cardinality, memory, result bytes, duration, and concurrency.
16. **“Dry-run cost is exact.”** Estimates depend on statistics and planning; runtime needs hard limits and actual accounting.
17. **“`202 Accepted` means the result exists.”** It means the request entered an asynchronous lifecycle under documented semantics.
18. **“Cancellation means cancelled.”** It can race with execution/publication and must reach a confirmed terminal state.
19. **“A completed query means a complete artifact.”** Publication, manifest, checksum, and policy can fail after computation.
20. **“Caching is harmless for reads.”** Missing tenant, policy, purpose, projection, locale, or snapshot dimensions can cross-disclose or misstate data.
21. **“Hidden columns cannot leak.”** Filters, ordering, grouping, counts, errors, timing, metadata, and repeated differences can reveal them.
22. **“Minimum group size prevents inference.”** Overlapping queries and complementary cells can isolate protected values.
23. **“Efficient transport supplies governance.”** Columnar RPC improves transfer; product meaning, authorization, budget, and lifecycle remain application duties.
24. **“Adding a field is always compatible.”** It may break strict clients, expose data, alter wildcard selections, cost, caches, or meanings.
25. **“No endpoint traffic means retirement is complete.”** Jobs, cursors, SDKs, caches, artifacts, credentials, and downstream copies may remain.

## Worked Examples

### Example 1

**Situation.** A mobile product needs the current plan tier and entitlement timestamp for one account. **Reasoning.** A fixed record endpoint resolves an immutable account ID, derives tenant from workload identity, projects only two governed fields, and serves from a low-latency store with version/freshness metadata. Arbitrary dataset query is unnecessary. **Conclusion.** Choose the narrowest interface matching the decision.

### Example 2

**Situation.** Finance wants monthly recognized revenue by region and product. **Reasoning.** A metric API owns recognition definition, currency conversion version, fiscal calendar, allowed dimensions, correction window, and snapshot. It rejects client-provided formulas and unsupported dimensional combinations. **Conclusion.** Central metric semantics prevent syntactically valid but incomparable numbers.

### Example 3

**Situation.** An orders collection sorts by `created_at`; many rows share a timestamp. **Reasoning.** The server appends `order_id`, selects a snapshot, and binds `(created_at,order_id)` plus query/policy generation into the cursor. Each page reauthorizes. **Conclusion.** Stable keyset pagination needs a unique total order and stable state.

### Example 4

**Situation.** A partner requests a two-year ungrouped export through an interactive endpoint. **Reasoning.** Preflight predicts 9 TiB scanned and 300 GiB output, exceeding interactive budgets. The API rejects with safe narrowing guidance or offers an approved asynchronous export class with quota, encryption, expiry, and cost attribution. **Conclusion.** Workload class is a contract, not an implementation accident.

### Example 5

**Situation.** A support agent may view account status but not health condition. **Reasoning.** Removing the condition from projection is insufficient if agents can filter by it and compare counts. The interface removes forbidden predicates/groupings, applies minimum cohorts and query-history analysis where aggregate access is legitimate, and tests errors/timing. **Conclusion.** Authorization covers computation and inference channels, not only serialized fields.

### Example 6

**Situation.** A query exceeds the synchronous deadline. **Reasoning.** The initial idempotent request creates job `J9`, returns accepted state and polling location, and records snapshot/budget. Polls show running then publishing; only after atomic result plus manifest does status become succeeded. **Conclusion.** Long work needs a truthful resource state machine.

### Example 7

**Situation.** An export reports decimal revenue through JSON and a JavaScript client changes `9007199254740993` to another integer. **Reasoning.** The contract encodes exact integer/decimal values as constrained strings with unit and scale, publishes typed SDK adapters, and adds boundary fixtures. **Conclusion.** Storage precision is not automatically wire or client precision.

### Example 8

**Situation.** A shared cache keys only normalized query and snapshot. **Reasoning.** Two tenants issue identical filters and the second receives the first tenant's rows. The corrected design partitions by tenant and policy/representation dimensions or caches only pre-policy safe material, then reauthorizes. **Conclusion.** Cache identity is part of security correctness.

### Example 9

**Situation.** A result artifact succeeds, but its download URL lasts seven days after an employee loses access. **Reasoning.** Issuance is reauthorized, the capability is short-lived and scoped, the underlying artifact has owner/policy/expiry, revocation blocks new URLs, and high-risk results use a proxy or revocable mechanism. **Conclusion.** Export delivery extends the authorization and retention boundary.

### Example 10

**Situation.** A metric formula changes while active jobs and cursors use the old definition. **Reasoning.** The service publishes a new definition generation, dual-computes comparison snapshots, binds old jobs/cursors to the old generation until expiry, migrates named consumers, and retires only after artifact and usage evidence. **Conclusion.** Semantic evolution must govern in-flight state, not just routes.

## Cross-Program Connections

- [DE-035](035-incremental-models.md), [DE-073](073-reconciliation-tests.md), and [DE-074](074-freshness-and-timeliness.md) provide stable changes, common-boundary comparisons, and source-to-consumer freshness.
- [DE-076](076-data-contracts.md), [DE-085](085-classification-and-sensitive-data.md), [DE-086](086-access-control-for-analytical-data.md), and [DE-089](089-auditability-and-provenance.md) supply product ownership, classification, policy, and evidence.
- [DE-091](091-warehouses-query-engines-and-serving-stores.md) and [DE-092](092-materialized-views-and-derived-tables.md) supply workload routing, snapshots, derived state, publication, and serving projections.
- [DE-093](093-reverse-etl-and-operational-activation.md) contrasts copying governed desired state into operational destinations with serving it on demand through an API.
- [API-021](../../28-api-and-service-engineering/modules/021-api-contracts-and-behavioral-guarantees.md), [API-024](../../28-api-and-service-engineering/modules/024-request-and-response-modeling.md), and [API-025](../../28-api-and-service-engineering/modules/025-validation-constraints.md) provide behavioral, wire, and validation contracts.
- [API-017](../../28-api-and-service-engineering/modules/017-filtering-sorting-and-pagination.md), [API-018](../../28-api-and-service-engineering/modules/018-long-running-operations.md), and [API-019](../../28-api-and-service-engineering/modules/019-bulk-and-batch-operations.md) provide general collection, query-job, and bulk mechanics specialized here for snapshots, policy, and cost.
- [API-037](../../28-api-and-service-engineering/modules/037-idempotency-keys.md), [API-048](../../28-api-and-service-engineering/modules/048-enumeration-and-data-exposure.md), and [API-075](../../28-api-and-service-engineering/modules/075-backpressure-across-service-boundaries.md) connect job creation, disclosure, and bounded streaming.
- [API-082](../../28-api-and-service-engineering/modules/082-additive-and-breaking-changes.md) and [API-090](../../28-api-and-service-engineering/modules/090-evolving-an-api-without-coordinated-consumer-releases.md) govern schema, semantic, job, cursor, and consumer evolution.
- [PLAT-072](../../29-platform-engineering/modules/072-namespace-account-and-cluster-isolation.md), [PLAT-073](../../29-platform-engineering/modules/073-resource-quotas.md), and [PLAT-077](../../29-platform-engineering/modules/077-admission-control.md) connect isolation, query budgets, overload control, and fairness.
- [DE-095](../ROADMAP.md) applies these contract, snapshot, policy, and provenance principles to feature and training dataset pipelines.

## References

- OpenAPI Initiative, *OpenAPI Specification 3.2.0*, current specification. <https://spec.openapis.org/oas/latest.html>
- Internet Engineering Task Force, *HTTP Semantics*, RFC 9110, 2022. <https://www.rfc-editor.org/rfc/rfc9110.html>
- Internet Engineering Task Force, *Problem Details for HTTP APIs*, RFC 9457, 2023. <https://www.rfc-editor.org/rfc/rfc9457.html>
- OASIS Open, *OData Version 4.02, Part 1: Protocol*, current committee specification. <https://docs.oasis-open.org/odata/odata/v4.02/odata-v4.02-part1-protocol.html>
- JSON Schema project, *JSON Schema Validation: A Vocabulary for Structural Validation of JSON*, Draft 2020-12. <https://json-schema.org/draft/2020-12/json-schema-validation>
- Apache Arrow project, “Arrow Flight RPC,” current format documentation. <https://arrow.apache.org/docs/format/Flight.html>
- Apache Arrow project, “Arrow Flight SQL,” current format documentation. <https://arrow.apache.org/docs/format/FlightSql.html>
- Google Cloud, “BigQuery REST API: `jobs.query`,” current reference. <https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query>
- Google, “AIP-158: Pagination,” current API Improvement Proposal. <https://google.aip.dev/158>
- OWASP Foundation, “API1:2023 Broken Object Level Authorization,” *API Security Top 10*. <https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/>
- OWASP Foundation, “API3:2023 Broken Object Property Level Authorization,” *API Security Top 10*. <https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/>

## Exercises

### Exercise 1

Classify six needs—single-account lookup, governed KPI dashboard, ad hoc analyst exploration, nightly partner delivery, million-row typed transfer, and constrained embedded analytics—into record, metric, direct analytical access, export, streaming, or query API. Give the semantic, authorization, latency, cost, and lifecycle reason for each choice.

### Exercise 2

A product contains rows `(created_at,id,commit)`: `(10,A,1)`, `(10,B,2)`, `(20,C,3)`, `(30,D,4)`, `(40,E,5)`. Page size is two at snapshot 5. After page one, `(15,X,6)` is inserted and B is updated at commit 7. Derive all keyset pages, cursor bindings, and output. Contrast offset pagination without a snapshot.

### Exercise 3

Design an asynchronous customer export API. Include request idempotency, typed filters, policy/purpose, estimate and admission, job states, cancellation races, snapshot, artifact manifest, checksums, download authorization, expiry/deletion, retries, errors, provenance, and reconciliation.

### Exercise 4

Clinicians may see patient-level diagnosis data for their assigned patients; researchers may see only approved aggregates. Design row/column/purpose policy, allowed query shapes, cohort and composition controls, metadata/errors/caches/logs, revocation, exports, audit, and tests. State what formal privacy guarantees are and are not claimed.

### Exercise 5

An estate has 180 data endpoints exposing physical tables, arbitrary filters, offset pagination, shared caches, no cost limits, inconsistent decimals/times, permanent result links, and unknown consumers. Design a risk-prioritized recovery and measurable retirement/migration criteria.

## Answers to the Exercises

### Answer 1

Use a **record API** for single-account lookup: immutable account identity, server-derived tenant, fixed minimal fields, row/property authorization, point-latency SLO, and a serving store make cost predictable. Use a **metric API** for the KPI dashboard: centrally own formulas, dimensions, units, fiscal time, correction, snapshot, and cache/freshness behavior so dashboards agree.

Keep **direct governed analytical access** for genuinely ad hoc analyst exploration in a sandbox with data policy, query limits, lineage, and review; forcing unknown questions through an operational API creates an unbounded DSL badly. Use an immutable **export API** for nightly partner delivery, with approved recipient/purpose, snapshot, schema, manifest, checksum, encryption, expiry, and deletion evidence.

Use a typed columnar **streaming API** for million-row transfer when clients support it, with schema negotiation, backpressure, batch/byte limits, cancellation, integrity, and immutable resume identity. Use a bounded **query API** for embedded analytics: named dimensions/measures or templates, server-side policy, cost admission, asynchronous fallback, and contract evolution. These are defaults conditioned on measured requirements; a tiny export could be synchronous and a record history might need streaming, but the exception must preserve the same governance.

### Answer 2

Order by unique tuple `(created_at,id)`. Page one at snapshot 5 is A, B and cursor `(product, contract/schema, query hash, policy/tenant, snapshot=5, order, last=(10,B), page policy, expiry)`. Page two selects keys greater than `(10,B)` with `commit<=5`: C, D. Its cursor ends at `(30,D)`. Page three is E and has no continuation. The complete traversal is A, B, C, D, E exactly once.

X has an earlier sort position but commit 6, so it is excluded from snapshot 5. B's commit-7 update is also excluded; snapshot semantics return its version as of commit 2. If the storage model overwrites B and cannot reconstruct the earlier version, it cannot truthfully retain snapshot 5 and must materialize the result, use versioned storage, or expire the cursor.

With live offset pages, page one A,B followed by insertion X yields current order A,B,X,C,D,E. Offset 2 then returns X,C; later deletion or reordering can shift rows again. The traversal mixes states and can omit or repeat original members. A unique order alone does not cure changing offsets; snapshot and continuation binding are required.

### Answer 3

`POST /customer-exports` accepts an idempotency key plus typed contract version, named filters, projection, format, purpose, and requested freshness class. The server authenticates principal/delegation, derives tenant, authorizes product/rows/columns/purpose/export, normalizes the query, chooses snapshot, estimates scan/output/cost, checks per-user/tenant/global concurrency and daily export bytes, and stores the idempotency key with a canonical parameter hash. Same key and parameters return the existing job; mismatch conflicts.

The job records `accepted→admitted→planning→running→publishing→succeeded` or terminal `failed/cancelled/expired`, with `cancel_requested` representing a nonterminal race. Engine cancellation and artifact cleanup must be confirmed; success can win the race and be reported honestly. Retriable internal attempts retain job and snapshot identity. Problems use stable types, safe detail, request/job IDs, retryability, and no forbidden query echo.

Publication writes encrypted immutable files, then a manifest containing product/definition/schema versions, snapshot/source boundary, normalized query hash, partitions, rows/bytes, format/compression, checksums, classification, producer, creation and expiry; it validates them before atomically marking success. Download requires current authorization and issues a short-lived scoped capability or uses an authorized proxy. Expiry deletes files, invalidates links, minimizes metadata under retention policy, and preserves required protected audit.

Reconciliation finds accepted jobs without terminal state, succeeded jobs without complete manifest/files, checksums/counts inconsistent with execution receipts, expired jobs retaining artifacts, and downloads after revocation. Provenance joins principal/purpose/policy, logical and physical resolution, snapshot, execution attempts, actual cost, artifact, downloads, and deletion evidence.

### Answer 4

Clinician identity carries organization, role, care relationship, delegated context, purpose, and current assignment. Server policy restricts patient rows to active assignments and fields to the clinical workflow; each object lookup reauthorizes, caches partition by policy context, and revocation propagates within a tested bound. Researchers use a distinct product and role with approved study/purpose, allowed dimensions/measures, time ranges, and no patient identifiers or arbitrary predicates.

Aggregate controls include contribution bounds, minimum cohorts, complementary-cell and differencing analysis, canonical query history/privacy budgets, suppression or approved noise, and review of rare dimensions. Minimum count alone is not claimed as privacy. A formal differential-privacy claim is made only if adjacency, mechanism, epsilon/delta, contribution bounds, composition ledger, trusted boundary, and implementation are specified and validated; otherwise describe controls as risk reduction, not anonymity proof.

Authorize metadata, field discovery, filters, ordering, counts, errors, timing, job history, and exports. Errors do not reveal whether a forbidden patient exists. Logs store safe query hashes and policy reasons rather than raw diagnoses. Shared caches contain only demonstrably policy-independent material; result caches bind organization, role/purpose, policy generation, query, snapshot, and representation. Exports require stronger approval, encryption, recipient binding, expiry, deletion, and audit.

Tests mutate patient IDs, organizations, assignments, roles, fields, hidden predicates, group dimensions, overlapping queries, small cohorts, cursor/job ownership, cached identities, revocation, error paths, timing classes, and download links. They verify direct non-disclosure and control behavior but cannot prove absence of every auxiliary-information inference; residual risk and governance authority remain explicit.

### Answer 5

Inventory endpoints, owners, purposes, consumers, principals, products, physical sources, classifications, fields, query grammars, policies, caches, jobs/artifacts/links, scan/output/cost, freshness, versions, logs, and dependencies. Immediately contain cross-tenant/shared-cache exposure, sensitive unrestricted filters/properties, unauthenticated or permanent export links, public credentials, and queries capable of exhausting shared compute. Freeze new arbitrary-table endpoints while preserving known safe critical service.

Create logical products with grain/key/semantics/owners and map physical tables behind adapters. Replace client tenant filters with server policy; allowlist fields/operators and parameterize values; remove forbidden computation channels; add exact wire types for decimals, units, instants, dates, null/redaction; introduce unique keyset order and snapshot-bound cursors. Add estimate plus hard scan/cardinality/time/output/concurrency limits, workload pools, asynchronous jobs for large work, artifact manifests/checksums, short-lived reauthorized downloads, protected receipts, and cache keys covering product/definition/snapshot/query/projection/tenant/policy/representation—or disable unsafe sharing.

Prioritize by sensitivity, cross-tenant blast radius, irreversible export, privilege, query cost, external exposure, and consumer criticality. Put contract and adversarial tests around each migrated surface. Measure unauthorized-path test coverage, policy/revocation latency, shared-cache partitions, bounded-query coverage, estimate error, scan/output/cost, tail latency, job terminality, stale artifacts, cursor snapshot availability, type-contract adoption, freshness, reconciliation exceptions, and owner/consumer registration.

Retire a physical endpoint only after named consumers migrate and comparison tests pass; production usage remains zero through its stated horizon; active jobs and cursors finish or expire explicitly; cached responses and artifacts are deleted under policy; permanent links and credentials are revoked; schedules/SDKs/dashboards no longer reference it; required audit remains protected; and rollback or exception ownership is closed. Endpoint shutdown without downstream-copy evidence is interface retirement, not proof of data deletion.
