---
module_id: LSDS-069
program: Large-Scale Data Systems Engineering
level: 2
module_number: 69
title: Federated Query
status: complete
last_verified: 2026-09-04
---

# Federated Query

## One-Page Review

### Governing question

How should a query engine plan and execute one logical read across autonomous heterogeneous sources so pushed operations preserve semantics, cross-source movement is bounded, each source's consistency and authorization are explicit, failures are attributable, and the result is not presented as more globally consistent than it is?

### Essential definitions

- A **federated query** evaluates one logical query using data or computation from multiple independently managed sources without first requiring all data to be copied into one store.
- A **connector** or **wrapper** maps source metadata, types, capabilities, credentials, splits, statistics, queries, and results into the federation engine's contracts.
- **source autonomy** means a source controls its schema, dialect, availability, quotas, transactions, policies, and evolution independently.
- **capability negotiation** establishes which predicates, projections, aggregates, joins, limits, functions, and partitions a source can execute with equivalent semantics.
- **pushdown** delegates an operation to a source; a **residual** operation remains in the federation engine to complete the logical predicate or computation.
- A **pass-through query** is source-native query text executed primarily under the remote dialect and security contract rather than decomposed by the federation optimizer.
- **query decomposition** divides a global logical plan into source subplans, exchanges, and central or delegated combination operators.
- A **snapshot vector** $(\sigma_1,\ldots,\sigma_n)$ identifies the source-local snapshots observed by a query; it is not automatically one global instant.
- **data shipping** moves source rows to compute; **query shipping** moves computation to a source; hybrid plans combine both.
- A **semi-join reduction** sends distinct join keys or a conservative filter to reduce rows returned from another source before the final exact join.

### Central model, mechanism, or theorem

For global expression $Q$ over sources $S_1,\ldots,S_n$, the coordinator constructs source subplans $q_i$ plus an engine remainder $R$. The decomposition is correct only if

$$R(q_1(S_1,\sigma_1),\ldots,q_n(S_n,\sigma_n))=Q(S_1@\sigma_1,\ldots,S_n@\sigma_n)$$

under declared type, null, comparison, collation, time-zone, function, duplicate, ordering, and error semantics. Pushdown is safe when the connector proves an operation equivalent or returns the unhandled residual. Cost must include remote startup/work/load, requests, transferred bytes, network latency/bandwidth, local compute, throttling, retries, and uncertainty. The result's consistency is the declared snapshot vector and acquisition protocol; federation alone does not create a distributed transaction or globally simultaneous snapshot.

### Critical invariants

- Every referenced object resolves to a source/catalog, schema mapping, source object/version, type mapping, authorization context, and metadata epoch.
- A connector advertises only operations it can implement with equivalent semantics and returns every unhandled predicate or expression as residual.
- Parameter values use typed binding or a rigorously escaped source API; user text is not concatenated into remote SQL.
- Source-local snapshot/isolation, acquisition time, transaction scope, and retry behavior are recorded for each scan.
- Cross-source plans preserve row multiplicity, null behavior, comparison/collation/time semantics, function behavior, and required order.
- Statistics and costs carry provenance, freshness, units, confidence, and source-load/network assumptions.
- Connections, requests, bytes, remote concurrency, local memory, result size, retries, and wall time are bounded per query/tenant/source.
- Retry does not silently read a newer remote snapshot unless the query contract permits it and records the change.
- Partial, stale, unauthorized, or mixed-snapshot results are not labeled complete globally consistent answers.
- Logs and plans redact credentials and sensitive literals while retaining source, subplan, capability, timing, and failure attribution.

### Common failures

Common failures include pushing case-sensitive comparison into a case-insensitive source; dropping the residual after partial pushdown; comparing timestamps under different zones; assuming `NULL`, NaN, decimal, JSON, or string semantics match; planning from stale remote statistics; pulling billions of rows for a tiny cross-source join; overloading an operational database with analytical fan-out; retrying only one source against newer data; treating separate source snapshots as one instant; accepting duplicate pages after connector retry; embedding credentials or literals in native query text; exposing row-policy-protected data through a coordinator; and returning successful partial results without an explicit partial contract.

### Compact example

A remote table has 10 million rows averaging 120 bytes, or 1.2 GB. A safe pushed predicate retains 2%, so 24 MB crosses the network. At 100 MB/s, transfer time falls from roughly 12 seconds to 0.24 seconds before startup and compute. The optimizer must still verify predicate semantics, source load, statistics confidence, and residual handling. If a local table is read at snapshot $\sigma_L$ and the remote source at $\sigma_R$, the result represents $(\sigma_L,\sigma_R)$ unless an external protocol establishes a common cut.

### Connections

[LSDS-025](025-lazy-evaluation-and-plan-construction.md) builds deferred plans, [LSDS-031](031-shuffle-architecture.md) moves cross-source data, [LSDS-057](057-memory-cpu-and-i-o-isolation.md) bounds shared resources, [LSDS-061](061-distributed-logical-and-physical-plans.md) decomposes physical work, [LSDS-062](062-coordinator-and-worker-architecture.md) owns connector control, [LSDS-063](063-exchange-operators.md) transports results, [LSDS-064](064-distributed-hash-and-merge-joins.md) combines sources, [LSDS-067](067-runtime-filtering-and-dynamic-pruning.md) reduces remote reads, and [LSDS-068](068-adaptive-query-execution.md) reacts to source behavior.

## Governing Question

Enterprises rarely keep all useful information in one engine. Operational databases, warehouses, object stores, search systems, metrics services, and partner APIs differ in data model, SQL dialect, functions, indexes, consistency, security, availability, cost, and operational ownership. Federation offers one logical query surface while leaving sources autonomous.

That convenience creates a boundary problem. The global engine must know what each source can do, which meanings agree, where to execute each operation, how much data will move, whose credentials apply, which snapshots were observed, and what a failure means. A connector that merely turns rows into pages is insufficient; it participates in planning, semantics, isolation, resource control, and audit.

The governing question is how to gain source-local filtering and computation without inventing false equivalence, false global consistency, unbounded cross-source movement, or authority broader than the user possesses.

## Why This Matters

Federation can answer questions before an ingestion pipeline exists, combine data that policy forbids copying permanently, retain source-specific indexes or functions, reduce duplication, and support gradual migration. It can also isolate the analytical engine from source implementation details through stable connector contracts.

The same architecture is exposed to wide-area latency, source outages, quota changes, stale schemas, dialect differences, and remote load. A plan that is cheap centrally may be dangerous for a production database. A filter that is correct locally may change meaning under another collation. A retry may observe a different remote transaction. A result joining two individually consistent snapshots may never have existed at any one moment.

Performance failures are often movement failures. Pulling a large remote relation through one connection can dominate everything. Overaggressive pushdown can be worse when the source lacks indexes, is heavily loaded, or returns an enormous intermediate. Reliable federation therefore combines semantic proof, capability negotiation, network-aware costing, source protection, and explicit consistency.

## Prerequisites and Retrieval

Review lazy plan construction in [LSDS-025](025-lazy-evaluation-and-plan-construction.md), shuffle architecture in [LSDS-031](031-shuffle-architecture.md), resource isolation in [LSDS-057](057-memory-cpu-and-i-o-isolation.md), multi-tenant queues in [LSDS-058](058-multi-tenant-queueing.md), physical plans in [LSDS-061](061-distributed-logical-and-physical-plans.md), coordinator/worker roles in [LSDS-062](062-coordinator-and-worker-architecture.md), exchange in [LSDS-063](063-exchange-operators.md), joins in [LSDS-064](064-distributed-hash-and-merge-joins.md), runtime filters in [LSDS-067](067-runtime-filtering-and-dynamic-pruning.md), and adaptation in [LSDS-068](068-adaptive-query-execution.md).

You should understand relational algebra, schemas and types, three-valued logic, collations, transactions and isolation, query optimization, join algorithms, statistics, authentication/authorization, network cost, backpressure, retries, and observability.

## Learning Objectives

After this module, you should be able to:

1. distinguish federation from replication, ingestion, external tables, virtualization, and pass-through queries;
2. define connector contracts for metadata, capabilities, types, statistics, splits, security, transactions, and errors;
3. prove safe full or partial pushdown while preserving residual expressions;
4. decompose a global query into source-local subplans and cross-source operators;
5. compare query shipping, data shipping, bind joins, semi-joins, and central joins using full cost;
6. specify snapshot vectors, consistency guarantees, retries, and partial-result behavior;
7. protect autonomous sources with quotas, concurrency, timeouts, backpressure, and cancellation;
8. manage credential delegation, row/column policies, native query text, audit, and data residency;
9. instrument remote planning/work, requests, bytes, waits, throttling, retries, and source load; and
10. validate semantics, failure, security, performance, and connector evolution before rollout.

## Core Exposition

### Distinguish federation from neighboring architectures

Federation evaluates against live or source-managed data through a common engine. Ingestion copies data into an owned analytical store. Replication maintains additional copies. External tables expose remote files or services through table abstractions. Virtualization is a broader product/architecture label that may use federation, caches, materialization, or semantic views.

A pass-through query sends source-native text and returns a relation. It exposes specialized features quickly but moves semantic validation and often security checks toward the source. A decomposed federated query lets the global optimizer reason about expressions and combine multiple sources. State which contract applies per subplan.

### Define the global catalog and mappings

The global catalog maps a stable logical name to connector, remote object identifier, metadata version, columns, logical/remote types, nullability, keys when trustworthy, partitioning, policy, and owner. Avoid using display names as durable identity. Record whether metadata is authoritative, cached, or inferred and when it expires.

Schema drift can rename, remove, or reinterpret remote fields. A query should bind a metadata epoch during planning and validate compatible handles at execution. If the source changes incompatibly, fail with source/object attribution rather than silently shifting columns.

Mappings may expose views that combine or rename remote structures. Lineage must trace global fields and predicates back to remote objects for authorization, debugging, and governance.

### Make capabilities precise and invocation-specific

A connector can advertise supported scans, partitions, predicate domains, projections, aggregates, functions, limits, top-N, joins, and table functions. Capability is not merely a boolean by operator kind. It may depend on type, collation, expression form, join type, source version, index, session setting, transaction, or query size.

Optimization methods may be invoked repeatedly. Return “not applied” when a call makes no further change; otherwise an optimizer can loop. Return a new immutable source handle describing applied operations, plus residual expressions and guarantees such as whether a limit is exact.

Version capability contracts. A connector binary, remote server upgrade, or configuration change can invalidate cached plans. Include relevant capability and semantic versions in plan-cache keys.

### Normalize types without erasing source meaning

Map remote physical/logical types into a global type system with explicit range, precision, scale, encoding, time zone, collation, and null behavior. Reject or require explicit casts for values the global type cannot represent. Do not silently truncate wide decimals, timestamps, strings, arrays, or identifiers.

Round-trip conversion matters when values are sent back as join keys or predicates. A global decimal converted to remote floating point may not preserve equality. Timestamp-with-zone converted to local timestamp can shift instants. Text normalization and case rules can alter comparisons.

Surface provenance for lossy conversions. If no safe common type exists, keep the comparison in one semantic domain or refuse it.

### Prove pushdown and preserve residuals

For expression $p$, a full pushdown requires remote result equivalence to the global engine under the mapped input. For partial pushdown, split into remote $p_r$ and residual $p_g$ so

$$p(x)=p_g(x)\land p_r(x)$$

under the engine's three-valued semantics, or use another formally justified decomposition. The connector returns what remains; the optimizer must not infer that “some filter applied” means the whole predicate was enforced.

Projection, aggregation, join, limit, top-N, sampling, and function pushdown have analogous guarantees. `LIMIT` without order may return any qualifying rows, while top-N needs compatible order, null placement, and collation. Aggregate pushdown must match overflow, decimal, null, distinct, approximate, and empty-input behavior.

Keep an engine-side check when the connector's result is conservative but not exact. A remote filter may return a superset; it must not omit qualifying rows.

### Decompose by source ownership and physical boundaries

Start with global relational algebra. Group maximal semantically pushable subgraphs by connector and source transaction. Insert exchange/scan nodes at their outputs. The remaining plan performs cross-source joins, aggregates, sorting, and final projection.

Two catalogs using the same connector are not necessarily one source capable of a remote join. Conversely, several schemas in one remote database may be joined there if authorization and transaction scope permit. Let the connector identify execution affinity rather than guessing from names.

Subplans should be typed parameterized representations when possible. Native SQL generation requires a dialect-aware renderer for identifiers, literals, placeholders, functions, and limits—not string concatenation.

### Cost the whole federated path

For source $i$, a simple model is

$$C_i=C_{startup,i}+C_{remote,i}+N_{req,i}L_i+\frac{B_{wire,i}}{BW_i}+C_{decode,i}+C_{local,i},$$

augmented by queueing, concurrency, egress price, throttling probability, failure/retry cost, and uncertainty. Latency matters for serial round trips; bandwidth matters for large transfers. Source CPU may be more valuable than federation-cluster CPU.

Statistics need provenance and freshness. Local cached statistics avoid remote planning calls but age. Remote estimates may cost a round trip and still use different cost units. Convert only comparable quantities, keep uncertainty, and favor robust plans near cliffs.

Never treat a source's arbitrary optimizer cost unit as seconds without calibration. Capture observed rows/bytes/time by subplan to improve bounded future estimates.

### Choose query shipping, data shipping, or hybrid execution

Query shipping pushes filters, projections, aggregates, and sometimes joins to a capable source, reducing movement and exploiting indexes. It can overload the source, encounter dialect differences, or obscure work.

Data shipping pulls rows into the federation engine for uniform semantics and cross-source computation. It consumes network, local memory, and time. Use it when operations cannot be safely delegated or when the analytical engine is better suited.

Hybrid execution pushes only safe reductions, then combines centrally. A common plan pushes filters/projections and partial aggregates at each source, ships compact results, and finalizes globally. Partial states must be mergeable and version compatible.

### Place cross-source joins deliberately

For relations $A$ and $B$ on different sources, choices include pull both centrally, ship one into the other's temporary/staging facility, issue parameterized lookups, send distinct keys as a semi-join reduction, or materialize one side in an analytical store. Each changes authority, source load, latency, movement, and cleanup.

A bind join sends batches of outer keys to a remote lookup. It can exploit an index but causes many round trips and must preserve duplicates and null semantics. Bound batch size, concurrency, parameter count, and retry identity. Never send one request per row without evidence.

A semi-join or Bloom/range filter can reduce remote rows, but the final exact join remains necessary. Keys and filters may be sensitive data crossing a governance boundary. Verify destination authorization and expiry.

### State consistency as a snapshot vector

Each source scan observes a local snapshot $\sigma_i$ under its transaction/isolation rules. The federation result is over $(\sigma_1,\ldots,\sigma_n)$. Without distributed snapshot coordination, those snapshots may correspond to different times and no globally simultaneous database state.

Acquire source transactions in a defined order and record start/first-row/last-row times, isolation, snapshot token if available, and retry policy. Long transactions can harm source vacuuming, locking, or resource use; global consistency ambitions have operational cost.

If a connector cannot pin a snapshot, say so. Retrying a scan may observe newer data. Options are restart the entire federated query, accept a refreshed snapshot under a declared “latest available” contract, or fail rather than mix versions.

### Treat writes as a separate system

Read federation does not imply atomic multi-source writes. Two-phase commit needs prepared-transaction support, durable coordination, recovery, operator procedures, and careful failure semantics across every participant. Many APIs and warehouses do not provide compatible participation.

Prefer read-only federation unless a specific write protocol is designed. For non-atomic workflows, use idempotency keys, outbox/inbox patterns, sagas/compensation, reconciliation, and explicit partial outcome reporting. Never label best-effort multi-source updates one transaction.

### Protect autonomous sources

Every connector needs per-source and per-tenant limits on connections, concurrent queries, requests, bytes, rows, remote CPU/time when exposed, parameter batches, result pages, retries, and queued work. Use admission control and source-specific priority so analytics cannot starve operational traffic.

Propagate cancellation with deadlines, but expect some sources to ignore or delay it. Drain or close safely, account work after client cancellation, and avoid retry storms. Backpressure remote fetches based on downstream capacity rather than buffering an entire result.

Circuit breakers may stop new work after overload or repeated failure. Recovery should be gradual and observable. A connector timeout is not proof the source query stopped.

### Design authentication, authorization, and policy composition

Choose credential mode explicitly: end-user delegation, service identity with impersonation, or service identity plus federation-layer policy. Delegation preserves source audit and policy but may be unavailable. A broad service credential shifts enforcement to the federation engine and increases blast radius.

Authorize global object discovery, source connection use, columns, rows, functions, and pass-through query capability. Remote and federation policies may both apply; define intersection and error behavior. Prevent inference through statistics, errors, timing, dynamic filters, caches, and temporary results.

Store credentials in managed secret systems, rotate them, scope network access, encrypt transport, redact plans/logs, and expire materialized intermediates. Native query text deserves special review because source-only functions can bypass global parsing or controls.

### Specify failure and partial-result semantics

Classify failures: authentication/authorization, metadata drift, planning/capability mismatch, remote syntax, timeout, throttling, unavailable source, conversion, corrupt page, local resource, cancellation, or consistency loss. Preserve source and subplan identity without leaking secrets.

Default exact SQL behavior is fail the query if any required source cannot provide valid input. Partial results require an explicit query/API contract that identifies missing sources, incomplete partitions, snapshot vector, and aggregates that are no longer exact. Do not quietly substitute cached stale data.

Retry only idempotent reads or requests with deduplication. Bound attempts and use backoff/jitter. Decide whether the same snapshot can be reopened; otherwise restart at a safe global boundary or fail.

### Observe the source and federation layers

Record planning/metadata calls, connection acquisition, remote queue/start/first-byte/last-byte, request count, pages, source rows/bytes, wire bytes, decoded bytes, residual rows, pushdown operators, local CPU/memory/spill, backpressure, throttling, retries, cancellations, and cleanup.

Attach query, source/catalog, connector/version, source subplan hash, snapshot/isolation (redacted as needed), plan epoch, and attempt. Separate remote time from network wait and local decode. Compare predicted to observed transfer and source load.

Expose a federated explain that shows which expressions were pushed, which remain residual, where joins execute, estimated movement, source consistency, and important capability refusals. Redact credentials and sensitive literals.

### Validate connectors as semantic components

Build a conformance suite for types, nulls, comparisons, collation, time zones, decimals, NaN, JSON, arrays, identifiers, functions, aggregates, limits/top-N, errors, and ordering. Differentially compare pushed versus engine-side evaluation on adversarial data.

Test partial pushdown and residual retention, repeated optimizer calls, plan-cache invalidation, schema drift, source upgrades, stale stats, empty/huge pages, malformed values, backpressure, cancellation, throttling, timeout, retry, snapshot loss, credential rotation, and policy changes.

Benchmark latency and bytes over realistic regions, bandwidth, source indexes/load, concurrency, and selectivity. Shadow new pushdown/cost rules, canary by connector/source/query risk, and provide rule/connector kill switches. Any result mismatch disables the optimization before performance analysis continues.

## Definitions and Notation

Let sources be $S_1,\ldots,S_n$, source-local snapshots be $\sigma_i$, and the vector be $\boldsymbol{\sigma}=(\sigma_1,\ldots,\sigma_n)$. A global query result is $Q(S_1@\sigma_1,\ldots,S_n@\sigma_n)$ under global semantics $G$.

Let connector capability $K_i(o,t,v,c)$ state whether source $i$ can execute operation $o$ for type/semantic contract $t$, source version $v$, and context $c$. Capability must describe exact, conservative/superset, unsupported, or pass-through behavior rather than one boolean.

For pushed predicate $p_{r,i}$ and residual $p_g$, correctness requires their composition equal global predicate $p$ under three-valued logic. Let $B_i$ be wire bytes, $N_i$ requests, $L_i$ request latency, and $BW_i$ effective bandwidth. Let $C_{remote,i}$ and $C_{local,i}$ denote measured or calibrated resource costs, not assumed common arbitrary units.

For a bind join, let $D$ be distinct outer keys, $b$ batch size, and $N=\lceil D/b\rceil$ requests before retries. Duplicate outer rows remain in the final exact join even when transmitted lookup keys are deduplicated.

## Mechanisms, Invariants, or Proof Structure

### The federated-decomposition audit

1. Bind the global logical plan, parameters, user/tenant, policy, catalog metadata epoch, and intended consistency contract.
2. Resolve each object to a connector, durable remote identity, type mapping, authority, and source execution affinity.
3. Negotiate invocation-specific capabilities and semantic versions.
4. Decompose only operations proven exact or conservatively pushable; retain all residual work.
5. Assign source transactions/snapshots and record the snapshot vector and retry rules.
6. Enumerate central, query-shipping, data-shipping, bind/semi-join, and materialized alternatives that obey policy.
7. Cost remote startup/work/load, request latency, wire bytes, bandwidth, local work, uncertainty, throttling, failure, and cleanup.
8. Enforce connection/request/byte/row/memory/time/retry and source-protection bounds.
9. Execute with typed parameters, backpressure, attempt identity, cancellation, integrity validation, and exact final operators.
10. Verify result equivalence, snapshot claims, policy/audit, cleanup, source impact, and realized cost; fall back or disable unsafe rules.

### Pushdown proof obligations

The connector documents domain and codomain mappings, remote expression, supported input subset, null/exception behavior, and exactness. The engine checks required context and retains a residual whenever exactness is not guaranteed. For a conservative remote predicate $r$, require

$$p(x)=\text{true}\Longrightarrow r(x)=\text{true},$$

so remote execution cannot discard a globally qualifying row. The engine then evaluates $p$ exactly on survivors.

Aggregation and join pushdown additionally preserve multiplicity, grouping equality, empty-input results, duplicate semantics, and join type. Top-N preserves total/preorder semantics, null placement, ties, and collation or remains local.

### Consistency claim boundary

If no protocol proves a common snapshot, the strongest default claim is evaluation over the recorded vector $\boldsymbol{\sigma}$. Source-local repeatable reads keep multiple scans within one source consistent, but they do not coordinate with other sources. Hiding this distinction converts availability timing into silent analytical inconsistency.

## Alternatives and Trade-Offs

### Ingest into one analytical store

Ingestion offers common types, statistics, locality, repeatable snapshots, mature optimization, and source isolation. Data is delayed, duplicated, governed in another place, and pipelines must handle change. Prefer it for repeated heavy joins, stable SLAs, and historical reproducibility.

### Query sources live

Live federation gives freshness and fast integration while retaining source capabilities. It inherits source load, availability, latency, consistency, and evolution. Prefer it for selective reads, operational lookups, exploratory integration, or data that cannot be copied.

### Cache or materialize selectively

Caching lowers repeated latency and protects sources. It introduces invalidation, staleness, storage, security, and snapshot lineage. Cache keys must include user/policy where results differ, and entries need explicit freshness and revocation behavior.

### Use pass-through native queries

Pass-through exposes specialized source syntax and lets expert users tune locally. The global optimizer cannot safely decompose opaque text, and global policies/parameterization may be weaker. Restrict, audit, bind parameters where supported, and return source-dialect/type behavior explicitly.

### Central join versus remote staging

Central joins avoid writing to a source and provide uniform execution, but ship data. Remote staging can exploit indexes and reduce movement, but requires write authority, cleanup, quotas, encryption, naming, transaction handling, and data residency approval. Include those costs and risks.

### Stronger consistency versus availability and source impact

Pinned long transactions or coordinated snapshots improve reproducibility but can block cleanup, consume resources, and fail across unsupported sources. A best-effort snapshot vector is more available but must be communicated. Choose the contract based on decision risk rather than hiding the trade-off.

## Failure Modes and Misconceptions

- **“One SQL surface means one SQL semantics.”** Types, functions, nulls, strings, time, errors, and ordering vary.
- **“The connector accepted the predicate, so no filter remains.”** Partial or conservative pushdown requires residual evaluation.
- **“Same connector means same remote join domain.”** Catalogs may target unrelated servers or transactions.
- **“Pushdown always reduces cost.”** Remote source load, missing indexes, startup, throttling, and bad plans can dominate.
- **“Remote optimizer cost is directly comparable.”** Cost units and models differ; calibrate with observations.
- **“A source-local transaction creates a global snapshot.”** It creates only one element of the snapshot vector.
- **“Retrying one read is harmless.”** It may mix a new snapshot or duplicate pages.
- **“Distinct bind keys remove duplicate semantics.”** Deduplication reduces requests; the final join must restore multiplicity.
- **“Read access permits staging.”** Temporary writes require separate authority, lifecycle, residency, and cleanup.
- **“Cancel acknowledged means source work stopped.”** The connector must observe and account actual termination.
- **“Partial results are better than failure.”** Without explicit missingness semantics, aggregates and decisions can be dangerously wrong.
- **“Service credentials simplify security.”** They centralize policy and enlarge blast radius.

## Worked Examples

### Example 1

**Retain a residual predicate.** A source can execute `country = 'SE'` but not the global regular expression on `email`. The remote subplan applies only country; the engine evaluates the regex on all returned rows. Marking the whole conjunction handled would leak false positives into the answer.

### Example 2

**Reject unsafe string pushdown.** The global engine compares strings case-sensitively, while the remote collation is case-insensitive. Predicate `code = 'abc'` cannot be pushed as exact equality. The connector may fetch a conservative superset and apply global equality, or leave the predicate entirely local.

### Example 3

**Express the snapshot vector.** Source A pins snapshot `a42` at 10:00:01; source B begins a repeatable read `b91` at 10:00:07. The result is over `(a42,b91)`. It is reproducible if tokens can be reopened, but it is not claimed to represent exactly 10:00:04.

### Example 4

**Batch a bind join.** A local filter yields 8,200 distinct customer keys. With 500 typed parameters per request, the connector makes $\lceil8200/500\rceil=17$ remote requests before retry. It limits four concurrent calls, deduplicates retry IDs, and joins returned rows back to all original local duplicates.

### Example 5

**Protect an operational source.** A plan proposes 200 parallel splits against a primary database. Source policy permits 12 connections and 6 concurrent analytical statements. The connector caps concurrency, queues within the query deadline, applies backpressure, and may prefer a replica or ingestion path instead of treating federation capacity as cluster capacity.

### Example 6

**Compare query and data shipping.** Pulling 1.2 GB over 100 MB/s costs at least 12 seconds of transfer. An exact remote filter returns 24 MB, about 0.24 seconds, plus 0.08 seconds startup, 0.35 seconds remote work, and 0.90 seconds local completion: 1.57 seconds estimated. Source load and semantic proof remain gates.

### Example 7

**Reject a false broadcast assumption.** A remote estimate says 5 MB but is two months old. The plan would broadcast the result to 100 workers. The optimizer chooses a bounded partitioned plan or samples under policy because a stale underestimate could multiply memory and network by the cluster width.

### Example 8

**Handle a source timeout.** Source C times out after two pages. Exact-query mode cancels siblings and fails with source/subplan attribution. It does not aggregate partial C rows. A separately designed partial API could return completeness metadata, but normal SQL success remains unavailable.

### Example 9

**Fence a changed snapshot on retry.** A remote token expires after a worker failure. The connector cannot reopen the same snapshot. Policy restarts the entire federated query and obtains a new vector rather than combining new remote pages with old local materialization.

### Example 10

**Execute a transfer-cost estimate.**

<!-- bijux-verify: {"id":"federated-transfer-cost","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"unfiltered_bytes=1200000000\nfiltered_bytes=24000000\ntransfer_seconds=0.24\nestimated_seconds=1.57\nreduction_percent=98.0\n","stderr":""}} -->
```python
rows = 10_000_000
row_bytes = 120
selectivity = 0.02
bandwidth_bytes_per_second = 100_000_000

unfiltered_bytes = rows * row_bytes
filtered_bytes = round(unfiltered_bytes * selectivity)
transfer_seconds = filtered_bytes / bandwidth_bytes_per_second
estimated_seconds = 0.08 + 0.35 + transfer_seconds + 0.90
reduction_percent = 100 * (1 - filtered_bytes / unfiltered_bytes)

print(f"unfiltered_bytes={unfiltered_bytes}")
print(f"filtered_bytes={filtered_bytes}")
print(f"transfer_seconds={transfer_seconds:.2f}")
print(f"estimated_seconds={estimated_seconds:.2f}")
print(f"reduction_percent={reduction_percent:.1f}")
```

The estimate omits queueing, throttling, contention, retries, and uncertainty; production cost models must include them.

## Cross-Program Connections

- **Database systems:** catalogs, types, algebra, optimizers, transactions, isolation, collations, and statistics define meaning.
- **Distributed systems:** autonomy, partial failure, retries, snapshot coordination, backpressure, cancellation, and recovery define execution.
- **Data engineering:** ingestion, replication, external tables, schema drift, freshness, lineage, and materialization frame alternatives.
- **Network engineering:** round trips, bandwidth, locality, egress, connection pools, and congestion dominate movement.
- **Platform engineering:** connector lifecycle, secrets, quotas, tenant admission, observability, caches, and kill switches host federation.
- **Reliability engineering:** exact versus partial results, timeouts, circuit breakers, replay, canaries, fallback, and rollback bound failure.
- **Security and governance:** identity delegation, policy intersection, residency, temporary data, audit, inference, and redaction bound authority.
- **Performance engineering:** source startup/load, requests, wire/decoded bytes, residual work, uncertainty, tails, and fleet cost establish value.

## References

1. Trino. [Pushdown.](https://trino.io/docs/current/optimizer/pushdown.html) Current predicate, projection, dereference, aggregation, join, limit, top-N, and connector-specific pushdown behavior.
2. Trino. [Connector Development.](https://trino.io/docs/current/develop/connectors.html) Current connector metadata, split, page, statistics, pushdown, handle, residual, and semantic contracts.
3. Trino. [PostgreSQL Connector.](https://trino.io/docs/current/connector/postgresql.html) Current type mapping, statistics, cost-based join pushdown, collation safeguards, native query, and performance controls.
4. Trino. [Fault-Tolerant Execution.](https://trino.io/docs/current/admin/fault-tolerant-execution.html) Current connector retry support, exchange spooling, task retries, encryption, and resource behavior.
5. Trino. [Security.](https://trino.io/docs/current/security.html) Current authentication, authorization, access control, secrets, transport, impersonation, and connector security context.
6. PostgreSQL. [postgres_fdw.](https://www.postgresql.org/docs/current/postgres-fdw.html) Current foreign-server mapping, remote estimates, costs, fetch/batch controls, pushdown, transactions, and connection behavior.
7. Google Cloud. [Introduction to Federated Queries.](https://docs.cloud.google.com/bigquery/docs/federated-queries-intro) Current BigQuery connection, external query, type conversion, region, read-only, performance, and encryption constraints.
8. Google Cloud. [Cloud SQL Federated Queries.](https://docs.cloud.google.com/bigquery/docs/cloud-sql-federated-queries) Current connection setup, native SQL, type mappings, locations, credentials, and query execution workflow.
9. Amazon Web Services. [Use Amazon Athena Federated Query.](https://docs.aws.amazon.com/athena/latest/ug/federated-queries.html) Current connectors, in-place queries, parallelism, predicate pushdown, identity, and limitations.
10. Amazon Web Services. [Available Athena Data Source Connectors.](https://docs.aws.amazon.com/athena/latest/ug/connectors-available.html) Current connector deployment, source support, configuration, and operational boundaries.
11. Josifovski et al. [Garlic: A New Flavor of Federated Query Processing for DB2.](https://research.ibm.com/publications/garlic-a-new-flavor-of-federated-query-processing-for-db2--1) Primary account of metadata, wrapper cooperation, planning, and remote execution in heterogeneous federation.
12. Haas et al. [Optimizing Queries Across Diverse Data Sources.](https://research.ibm.com/publications/optimizing-queries-across-diverse-data-sources) Primary account of capability-aware rules and global optimization over heterogeneous sources.
13. Stonebraker et al. [Mariposa: A Wide-Area Distributed Database System.](https://www.cs.cmu.edu/~natassa/courses/15-721/papers/vldbj96.pdf) Primary account of source/site autonomy, wide-area constraints, costs, and adaptive distributed query placement.

## Exercises

### Exercise 1

Design a connector capability and semantic contract for predicates, aggregates, top-N, joins, and native pass-through. Include invocation context, residuals, types, exactness, versions, repeated optimizer calls, and plan-cache invalidation.

### Exercise 2

A source has 40 million 150-byte rows. A safe predicate retains 0.5%. Compute unfiltered/filtered bytes and transfer time at 80 MB/s. Add 150 ms startup, 1.4 s remote work, and 0.6 s local work; then state missing cost factors.

### Exercise 3

Design a cross-source join among a warehouse fact table, an operational customer database, and a search service. Compare central join, bind/semi-join reduction, remote staging, and ingestion. Cover semantics, source protection, credentials, movement, cleanup, and fallback.

### Exercise 4

Define consistency and retry semantics for a query spanning two snapshot-capable databases and one API without snapshot tokens. Explain what can and cannot be claimed and how worker/coordinator failures are handled.

### Exercise 5

Design a connector validation and rollout campaign. Include differential semantics, schema/source upgrades, policy/security, failures, source load, performance attribution, shadowing, canaries, kill switches, and rollback.

## Answers to the Exercises

### Answer 1

For each operation expose connector/source/semantic version, supported expression grammar, allowed types, null/collation/time-zone/decimal/NaN/error/order behavior, required source version/configuration/index/transaction, exact versus conservative guarantee, and produced physical properties. Each application returns an immutable handle plus unhandled residual and explicit guarantees such as exact limit or ordering. Join capability includes source execution affinity, join type/build constraints, predicates, and authorization. Native pass-through is separately authorized and typed; the global optimizer treats text as opaque. Repeated application with no new effect returns “not applied.” Plan-cache keys include connector, remote version/capability epoch, semantic settings, metadata epoch, user/policy context, and relevant session configuration; changes invalidate or revalidate the plan.

### Answer 2

Unfiltered bytes are $40{,}000{,}000\times150=6{,}000{,}000{,}000$ bytes. At 0.5%, filtered bytes are 30,000,000. Transfer at 80,000,000 bytes/s is 0.375 s. Adding 0.150 + 1.4 + 0.6 gives 2.525 s. The reduction is 99.5%, but missing factors include planning/metadata calls, queueing, request latency/count, result encoding, TLS, decode expansion/CPU, connection pooling, source contention, throttling, egress price, retries/failure probability, backpressure, cleanup, statistics uncertainty, and whether the predicate is semantically exact.

### Answer 3

Push selective fact predicates/partial aggregates into the warehouse. Extract distinct authorized customer IDs and search terms only if governance permits. A batched bind or semi-join against indexed operational customer data can avoid a full pull; cap connections, concurrency, parameters, deadline, and rows. Query the search service with bounded batches and retain exact residual scoring/filter semantics centrally. A central join provides uniform semantics but may move too much. Remote staging may reduce movement but needs write authority, encrypted temporary objects, quotas, snapshot binding, cleanup, and residency approval. Repeated heavy workloads favor ingestion/materialization into the warehouse with freshness lineage. Cost source load and failure, not just bytes. Use typed parameters and delegated identity where possible. If capability, quota, or consistency checks fail, choose a bounded central/materialized plan or fail; do not silently weaken predicates or return partial data.

### Answer 4

Open and record snapshot tokens for databases A and B under defined isolation and acquisition order. The API C contributes pages observed over an interval with request/version tokens if available. The honest result contract is vector `(a,b,c_interval)`; no one-instant global snapshot is claimed. Retries for A/B reopen the same token or restart the whole query. Idempotent API page retries use cursor/request identity, but if C cannot replay the same version, either restart all sources under a latest-available contract or fail. Worker retries deduplicate logical splits/attempts. Coordinator recovery replays source-session and snapshot metadata only when credentials/tokens and source protocols allow it; otherwise it cancels remote work, cleans up, and restarts/fails at a declared boundary. Partial API results are never reported as exact success.

### Answer 5

Create adversarial fixtures for every mapped type, null, collation, time zone, decimal, NaN, JSON/array, identifier, function, aggregate, join, limit/top-N, order, and error. Differentially compare pushdown disabled/enabled and verify residual retention. Test repeated optimizer calls, schema drift, metadata/capability cache invalidation, remote version upgrades, stale statistics, malformed/oversized pages, backpressure, cancellation, throttling, timeouts, retry/snapshot loss, coordinator/worker recovery, credential rotation, revoked policy, and temporary-data expiry. Verify least privilege, delegation, network/TLS, parameter binding, redaction, residency, and audit. Benchmark realistic latency/bandwidth/index/source-load/concurrency/selectivity cohorts and attribute planning, remote, transfer, decode, local, retry, tail, and source impact. Shadow new rules, canary read-only low-risk queries per connector/source, kill-switch on any mismatch, policy breach, cleanup failure, source overload, bound breach, or severe regression, and roll back to the previous connector/rule/capability epoch.
