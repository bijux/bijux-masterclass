---
module_id: API-056
program: API & Service Engineering
level: 2
module_number: 56
title: GraphQL Execution, Resolvers, and Batching
status: complete
last_verified: 2026-09-02
---

# GraphQL Execution, Resolvers, and Batching

## One-Page Review

### Governing question

How should a GraphQL service turn one validated operation into bounded, correct field work while preserving response-path semantics, preventing N+1 amplification, isolating request/authentication state, and reporting partial execution failure honestly?

### Essential definitions

- **execution** recursively resolves and completes the selected response positions of one validated operation against a schema.
- A **collected field set** groups selections with the same response name after fragments and directives are considered.
- A **resolver** is an implementation function that derives one field value from its parent/source value, coerced arguments, request context, and field/execution information.
- **value completion** turns a resolver result into the field's declared scalar, enum, object, list, or non-null response shape.
- A **response path** identifies one result position with aliased response names and zero-based list indices.
- The **N+1 pattern** occurs when resolving a parent collection causes one backend request plus one or more child requests per parent.
- A **batch loader** coalesces key requests and returns one result/error slot per requested key in the original key order.
- **request-scoped memoization** reuses one load result only within a request and an equivalent visibility/consistency context.
- A **batch window** is the scheduling interval during which compatible pending keys may be coalesced; widening it can improve batch size while adding latency.

### Central model, mechanism, or theorem

For parent count $n$, naive relationship resolution can require

$$
R_{naive}=1+n
$$

backend round trips at one level. A compatible loader partitions $u$ unique keys into batches of maximum size $b$, giving

$$
R_{batch}=1+\left\lceil\frac{u}{b}\right\rceil,
$$

subject to scheduler, dependency-level, backend, and cache semantics. This is not a whole-query bound: deeper sequential dependency layers add rounds, independent fields may fan out concurrently, and one batch can still be expensive.

For input keys $K=[k_0,\ldots,k_{m-1}]$, the batch contract requires output $Y$ with $|Y|=|K|$ and $Y_i$ corresponding to $k_i$—including explicit missing/error slots. Backend return order is irrelevant.

### Critical invariants

Only a selected, parsed, validated operation with successfully coerced variables executes. Query fields and non-root mutation fields are side-effect-free and idempotent because normal execution may reorder/parallelize them; top-level mutation fields execute serially, but their nested fields do not become a transaction. Every resolver has a single field semantic owner, validates domain assumptions, uses immutable/bounded request context, and returns a value compatible with the declared type. Context never becomes a global service locator or cross-request cache. Loader instances are scoped to one request or an explicitly equivalent principal/tenant/policy/snapshot boundary. Batch keys include every fact affecting value visibility/meaning. Batch output preserves length and input order, represents per-key absence/error, bounds key count, and shares the same deadline/cancellation. Memoized values are treated as immutable; mutations clear/prime affected keys after commit according to one consistency policy. Execution errors preserve response path and are redacted; null propagation follows schema wrappers. Instrumentation measures field/batch/dependency behavior without labels derived from arbitrary aliases/arguments.

### Common failures

Doing work before validation; resolving the same collected field twice because fragments duplicate it; placing side effects in query/nested fields; assuming query sibling order; assuming top-level mutation serialization is transactional; resolver business logic scattered across types; creating network/database clients per field; mutable global context; passing raw request objects everywhere; one loader shared across users/tenants; cache keys that omit tenant, locale, policy version, projection, or consistency mode; using request memoization as a shared cache; failing to clear after mutation; caching transient authorization/dependency errors; batch output in backend order; omitting missing rows; disabling cache without handling duplicate keys; unlimited batches; long batch windows; awaiting each load before sibling loads are enqueued; batching incompatible authorization scopes; loading full rows for tiny fields; hidden N+1 below helper layers; serializing all fields to make tests deterministic; swallowing errors into null; leaking exception messages; unbounded per-field spans/labels; and optimizing round-trip count while increasing bytes, locks, tail latency, or dependency saturation.

### Compact example

A query selects 100 orders and each order's customer. A naive resolver issues one order query plus 100 customer lookups. A request-scoped loader receives customer IDs, deduplicates 60 unique keys, and sends batches capped at 25: one order query plus three customer batches. The backend returns rows out of order and omits an inaccessible ID; the batch function maps rows back to every input slot and returns a policy-consistent absence/error. **Conclusion:** correct batching reduces calls from 101 to 4 here, but order alignment, visibility, bounds, and error semantics are part of correctness.

### Connections

[GraphQL Schema Design](055-graphql-schema-design.md) defines the field and nullability promises execution must uphold. [Request-Scoped Transaction Boundaries](036-request-scoped-transaction-boundaries.md) and [Deadlines, Cancellation, and Metadata](054-deadlines-cancellation-and-metadata.md) constrain context and effects. Pagination/incremental delivery and authorization/cost controls follow in the next two modules.

## Governing Question

Given a validated GraphQL operation and authenticated request context, what work graph may the executor create, how must each resolver and batch preserve type/trust/ordering/error invariants, and what evidence shows that optimization has reduced amplification without changing results?

## Why This Matters

GraphQL's field-local programming model is productive because each field can be understood independently. It is dangerous for the same reason: a harmless-looking relationship resolver may run hundreds of times, multiple sibling branches can concurrently saturate one dependency, and a cache placed at the wrong scope can disclose one user's data to another. The schema reveals selection shape but not the actual number, cost, or scheduling of backend calls.

Execution is also a correctness mechanism. It collects fields across fragments, coerces values, resolves abstract types, completes lists and non-null wrappers, attaches error paths, and may return partial data. A hand-built approximation that ignores alias merging, null propagation, or mutation ordering is not GraphQL execution.

Batching is not merely a performance trick. The batch function establishes a positional contract, a visibility scope, missing/error semantics, and consistency within a request. A loader that returns results in database order can silently attach the wrong customer to an order. A process-global loader can be fast and catastrophically wrong.

This module focuses on execution mechanics, resolver boundaries, N+1 diagnosis, request-scoped batching/memoization, and evidence. API-057 owns connection pagination and incremental response delivery. API-058 owns authorization placement and query-cost admission. Those concerns touch execution, but keeping their policy mechanisms distinct prevents a loader from being mistaken for an authorization or resource-control system.

## Prerequisites and Retrieval

Retrieve [GraphQL Schema Design](055-graphql-schema-design.md), [Transport, Application, and Domain Boundaries](031-transport-application-and-domain-boundaries.md), [Request-Scoped Transaction Boundaries](036-request-scoped-transaction-boundaries.md), [Concurrency Control at the API Boundary](038-concurrency-control-at-the-api-boundary.md), and [Deadlines, Cancellation, and Metadata](054-deadlines-cancellation-and-metadata.md). Be able to distinguish request errors from execution errors, schema coordinates from response paths, memoization from shared caching, and backend transaction scope from GraphQL operation scope.

## Learning Objectives

After completing this module, you can:

1. trace an operation through selection collection, field resolution, value completion, and response construction;
2. state which fields may execute normally and which top-level mutation fields execute serially;
3. design resolver interfaces with explicit parent, arguments, context, and execution information;
4. detect and quantify N+1 and deeper fan-out patterns from traces and dependency evidence;
5. implement the key-order, cardinality, missing-value, error, and size invariants of a batch loader;
6. choose safe request-scoped memoization keys and mutation invalidation behavior;
7. reason about async scheduling, dependency waves, cancellation, and concurrency limits;
8. preserve partial-data and non-null error semantics while redacting internal failure detail; and
9. verify semantic equivalence and performance under representative/adversarial operations.

## Core Exposition

### Enter execution only after request validation

A GraphQL request must be parsed, identify one operation when necessary, validate against the schema, and coerce variables before ordinary execution. A request error produces no response data. Reject invalid operations before opening transactions or calling domain dependencies; otherwise malformed traffic consumes capacity and may cause effects.

The executor begins with the operation root type, root value, coerced variables, request context, and selection set. Directives such as `@skip` and `@include`, fragments, type conditions, and aliases affect the selected work. Implement the current specification through a maintained library rather than duplicating its algorithms in application code.

Request preparation can be cached for trusted persisted operations, but cache keys must bind schema version/identity, operation text/hash, operation name, and any validation rules that change acceptance. Never treat a caller-supplied hash as proof that arbitrary text was previously approved.

### Collect fields by response name

GraphQL first turns a selection set into a collected fields map. Selections with the same response name—including compatible selections reached through fragments—are grouped. The response name is the alias when present, otherwise the field name. A resolver should not run independently for each duplicate syntactic occurrence.

Field collection prevents duplicated work and establishes response order. It also means observability must distinguish schema coordinate (`Order.customer`) from response path (`["recent", 3, "buyer"]`). Aliases are caller-controlled and high-cardinality; never use raw path or argument values as an unbounded metric label.

Fragments can make the executed field graph much larger or smaller than the surface operation suggests. Instrument the normalized operation and collected coordinates, not naive line counting. Runtime type conditions determine which abstract-type selections apply.

### Understand normal and serial execution

For query root fields and nested fields, collected fields execute normally: an implementation may choose order and normally permits parallelism. The specification relies on non-top-level-mutation field resolution being side-effect-free and idempotent so order cannot change results. Parent resolution precedes its child selection because the child needs a parent value; independent siblings can overlap.

Only top-level mutation fields in one mutation operation execute serially in textual order. Nested selections of each mutation payload execute normally. Serial does not mean atomic: the first mutation may commit and the second fail. It does not serialize concurrent HTTP requests. A transaction spanning several root mutation fields is an explicit application contract with serious locking/failure implications, not an automatic GraphQL property.

Do not introduce side effects in `Query.invoice.viewCount`, lazy relationship getters, telemetry writes that affect domain state, or default resolvers. If a read must update an audit record, separate a best-effort operational signal from domain state or expose an intentional command.

### Give resolvers narrow, explicit inputs

Most implementations present a resolver with four conceptual inputs:

- parent/source value produced by the enclosing field;
- coerced named arguments for the selected field;
- per-request context such as authenticated principal, deadline/cancellation, loaders, trace linkage, locale, and scoped domain ports;
- execution information such as schema field, return type, fragments, operation, and response path.

Framework names vary; the semantics matter. Parent objects should be stable domain/view values, not raw ORM sessions whose lazy properties issue invisible queries. Arguments are typed by GraphQL but still require domain validation such as range, state, and authorization. Context is created once per request and passed down; keep it bounded, immutable where practical, and explicit enough to test.

Execution information is useful for logging, lookahead, and path-aware errors. Parsing arbitrary selection trees inside every resolver creates tight coupling and can mis-handle fragments/directives/aliases. Prefer planned data access at owned boundaries, framework-supported lookahead, or loaders unless projection demonstrably matters.

The common default resolver reads a property or calls a similarly named method from the parent. It is convenient for pure already-loaded values. Do not let it trigger ORM lazy I/O, expose unintended properties, or invoke methods with side effects.

### Separate field adaptation from domain work

A resolver should translate GraphQL inputs/context to a domain query/command, call an owned application boundary, then adapt the result to the declared field value. Business invariants belong in domain/application services that can be reused outside GraphQL. Transport error mapping and response paths remain at the GraphQL boundary.

Thin does not mean no responsibility. A resolver owns field-specific argument semantics, authorization invocation, deadline propagation, selection-independent result meaning, null/error mapping, and instrumentation. Avoid a universal resolver helper that takes strings and dynamically reaches any repository; it destroys coordinate ownership and static review.

Use request-scoped dependencies rather than constructing clients/pools per field. Pools are application-scoped; transactions, identity, deadlines, loaders, and units of work are request/operation scoped. Ensure cleanup happens when the request completes or cancels, even if sibling resolvers are still pending.

### Complete values according to the declared type

After resolution, the executor completes the value. Scalars/enums serialize under their defined rules. Objects execute the selected child fields with the resolved value as parent. Lists complete each item and preserve list order. Interfaces/unions determine a valid runtime object type before child selections. Non-null wrappers reject null and propagate the execution error upward.

An asynchronous resolver can return an awaitable/promise supported by its runtime. Completion waits appropriately while allowing sibling work. Never return a live database cursor or lazy object whose lifetime ends before child completion. Materialize/bind resource ownership explicitly, and cap collections even when pagination policy is addressed elsewhere.

Execution errors attach to response positions. A nullable failed field becomes null and siblings attempt to continue; the response can contain both data and errors. A non-null failure propagates to the nearest nullable ancestor and may make `data` null. Do not catch every exception and silently return null: that erases the distinction between legitimate absence and service fault and may violate non-null.

### Recognize N+1 as a work-graph property

Suppose `Query.orders` performs one query and `Order.customer` independently loads a customer. For $n$ orders, the simplest execution makes $1+n$ backend calls. If each customer then loads an organization independently, a second fan-out may add up to $n$ more or reflect unique organization count. Nested lists can multiply work.

N+1 is not limited to SQL. It occurs with HTTP/gRPC calls, object storage, policy checks, cache misses, feature services, and filesystem reads. It can hide under ORM lazy loading or domain helpers. Count dependency operations by normalized coordinate/path level and request, then inspect key cardinality, batch size, concurrency, latency, and bytes.

A database join or eager load can solve a known access pattern efficiently. It may overfetch for other selections, duplicate rows, complicate authorization, or explode across several lists. A loader preserves field modularity and coalesces same-resource keys. A query planner can optimize globally but adds sophisticated ownership. Choose from evidence, and allow different fields to use different mechanisms.

### Enforce the batch function contract

A loader presents individual-key loads while scheduling one batch function for compatible pending keys. The batch receives an ordered key list. Backends commonly return rows in arbitrary order and omit missing keys. The batch function must index results, then return exactly one value, absence marker, or error for every original key in original order.

If input is `[9, 2, 9, 6]`, cache-enabled loaders may deduplicate to `[9, 2, 6]`; cache-disabled loaders may pass duplicates. Library behavior must be verified. Never return `values(result_map)`. Explicit alignment prevents identity corruption.

Keys must include all facts that affect the loaded representation: stable resource identity plus tenant/principal visibility boundary, authorization/policy version where applicable, locale/currency, consistency snapshot, and perhaps projection. Overly broad keys can leak or return wrong variants; overly narrow keys reduce reuse. Prefer separate loader instances for substantially different semantics rather than a giant ambiguous tuple.

The executable model below maps unordered sparse backend rows back to requested order, preserves duplicates, and emits an explicit missing marker.

<!-- bijux-verify: {"id":"batch-key-alignment","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"requested=[9, 2, 9, 6]\nbackend_order=[2, 9]\naligned=['user-9', 'user-2', 'user-9', 'MISSING']\nlength_ok=True\n","stderr":""}} -->
```python
def align(keys, rows):
    by_key = {row["id"]: row["name"] for row in rows}
    return [by_key.get(key, "MISSING") for key in keys]

requested = [9, 2, 9, 6]
backend_rows = [
    {"id": 2, "name": "user-2"},
    {"id": 9, "name": "user-9"},
]
aligned = align(requested, backend_rows)
print("requested=" + str(requested))
print("backend_order=" + str([row["id"] for row in backend_rows]))
print("aligned=" + str(aligned))
print("length_ok=" + str(len(aligned) == len(requested)))
```

In production, absence versus forbidden versus dependency error follows the schema/security policy. Returning an error in one slot permits other keys to succeed when the library supports it. A rejected whole batch usually fails every key and should represent a true batch-wide failure.

### Scope memoization to one visibility context

DataLoader-style caching is request memoization, not a replacement for Redis or an application cache. Create loaders at request entry after authentication context is established and discard them at request end. A process-global loader can reuse user A's allowed value for user B, retain stale data indefinitely, and leak memory.

Even within one request, repeated loads may occur before and after a mutation. After a committed update, clear affected keys and optionally prime them with the authoritative returned value. Do not prime before commit. If aliases or alternative keys exist, invalidate/prime all equivalent indexes or use a versioned immutable key. Define whether the request promises a snapshot, read-your-writes, or ordinary backend consistency.

Caching individual errors is library-specific and dangerous for transient or policy-sensitive failures. Distinguish stable absence from timeout, cancellation, overload, and authorization decisions. Clear retryable errors if a retry is allowed within remaining budget; never make the loader an unbounded retry loop.

Treat memoized values as immutable. If one resolver mutates a cached object, sibling results become order-dependent. Return immutable values/copies or enforce conventions with types/tests.

### Tune batch scheduling and size with evidence

The scheduler decides which pending loads coalesce. A same-turn/microtask window often batches sibling resolver requests without deliberate delay. Awaiting one load before enqueueing unrelated sibling keys creates sequential waves. Structure code to issue independent loads before awaiting them, while preserving dependency order.

Wider windows gather more keys but add latency and may violate deadlines. Manually dispatched loaders risk never dispatching on exceptional paths. Record enqueue-to-dispatch delay, batch size distribution, unique/duplicate ratio, backend latency, and queue cancellation.

Always bound maximum batch size to backend limits and measured behavior. A single SQL `IN` with thousands of keys can exceed parameter limits, ruin plans, hold locks, or create huge responses. Partition deterministically, preserve final alignment, propagate one shrinking deadline, and limit concurrent sub-batches. Fewer round trips is not success if dependency tail latency or bytes explode.

Batch only compatible requests. Do not combine keys across principals or policy/consistency modes merely because they target the same table/service. Batch authorization itself only under an API that returns per-resource decisions aligned to inputs and binds actor/action/context.

### Coordinate loaders, transactions, and cancellation

A loader must use the same request deadline and cancellation signal as the resolver. If the operation is cancelled, pending keys should be abandoned where safe and in-flight work cancelled cooperatively; cleanup remains bounded. Do not cache cancellation/timeout as stable resource absence.

Transaction-scoped reads must not escape into a loader bound to a different connection/snapshot. If a mutation writes then nested payload fields read, decide whether they use the mutation transaction, post-commit state, or returned domain value. A request-wide loader created before a transaction may violate read-your-writes unless invalidated and routed correctly.

Batch scheduling across mutation root fields can violate their required serial completion if work from the first is deferred into the second. Ensure each top-level mutation field, including value completion required for its result, reaches the implementation's serial boundary before the next begins. Never use a shared scheduler to reorder side effects.

### Handle failures without destroying partial-data semantics

Classify failures: request errors prevent execution; execution errors occur at a response position; expected domain outcomes may be typed data; transport failure may prevent delivery; cancellation/deadline does not prove absence of effects. Map internal exceptions to stable developer-safe messages/codes and retain detailed causes in protected telemetry.

Error paths use response names/aliases and list indices, while internal metrics should aggregate by schema coordinate and bounded error class. Preserve correlation without placing secrets, raw arguments, tokens, SQL, or stack traces in client `message`/`extensions`.

If a batch dependency fails wholly, each affected field position can surface an execution error under framework semantics. If only one key is missing/fails, return the corresponding per-key result so unrelated positions remain valid. Respect non-null propagation; do not insert a fabricated object to avoid null unless it is a real domain value promised by the schema.

Sibling work may already be running when non-null propagation makes its output unusable. Cancellation can reduce waste but must not create unsafe rollback assumptions. Instrument abandoned work and ensure dependency clients respect cancellation.

### Observe the execution graph safely

Record operation identity/hash/name (under policy), schema version, total duration, parse/validate/execute phases, normalized schema coordinates, resolver duration, dependency name, batch size, queue delay, cache hit/miss, error class, cancellation, and null propagation. Trace only useful boundaries; a span for every scalar field overwhelms systems.

Avoid raw query text, variables, aliases, list indices, IDs, and error messages as metric labels. Use bounded coordinate/error/dependency attributes and sampled protected traces for response paths. Distinguish resolver self-time from waiting and child dependency time; parallel siblings make sums exceed wall time.

Detect N+1 with per-request dependency-call counts correlated to parent/result cardinality. Compare calls, bytes, rows, latency percentiles, saturation, and correctness before/after batching. A call-count reduction alone can conceal giant payloads or hot-key contention.

### Verify semantics before and after optimization

Use a reference implementation or unbatched path as an oracle for representative small operations. Property-test batch alignment across arbitrary key order, duplicates, missing values, errors, and partitions. Assert output equivalence, not merely request count.

Test fragments, aliases, directives, repeated fields, interface/union types, empty/null lists, non-null propagation, async completion order, mutation-root ordering, and partial failure. Test two concurrent principals/tenants with identical raw IDs to catch cache leakage. Test mutation invalidation, snapshot/read-your-writes policy, cancellation before dispatch/in flight, deadline exhaustion, maximum batches, and dependency reordering.

Load-test realistic operation mixes and adversarial cardinalities. Inspect dependency concurrency, pool/queue depth, batch distributions, event-loop/thread saturation, memory retained per request, and tail latency. Prove loaders are released at completion. Fault-inject whole-batch and per-key failure and scan client/log/trace output for sensitive detail.

## Definitions and Notation

Let $O$ be one validated operation, $G_O=(P,E)$ its runtime response-position dependency graph, and $p\in P$ a response position identified by path. Let $f(p)$ be its schema coordinate, $r_f(parent,args,context,info)$ its resolver, and $Complete(T_f,v)$ value completion against declared type $T_f$.

Let $n$ be parent count, $K=[k_0,\ldots,k_{m-1}]$ requested batch keys, $u=|unique(K)|$, $b$ maximum batch size, and $Y$ aligned results. Batch correctness requires $|Y|=|K|$ and correspondence $Y_i\leftrightarrow k_i$. Let $q$ be scheduler queue delay, $d$ remaining deadline, and $c$ allowed dependency concurrency.

Request-scoped cache equivalence is not merely key equality: $(principal,tenant,policy,snapshot,locale,projection,k)$ must be equivalent for any reused result. Which components matter is field/domain-specific and documented.

## Mechanisms, Invariants, or Proof Structure

The N+1 arithmetic assumes one parent fetch and one child fetch for each of $n$ parents. Deduplicating to $u$ keys and partitioning into batches of size at most $b$ requires $\lceil u/b\rceil$ child calls, hence $1+\lceil u/b\rceil$. This proof does not bound deeper dependency waves, bytes, batch service time, retries, or concurrency.

Positional correctness follows by constructing an index from backend identity to authorized result and mapping over original $K$. Returning backend iteration order is correct only accidentally when it equals $K$ with identical omissions/duplicates. Explicit mapping handles reordering and creates one slot per requested occurrence.

Request isolation is necessary because memoization replaces a later computation with an earlier result. If visibility differs between two requests but a cache key does not encode that difference, there exists a resource for which the substituted result is unauthorized or semantically wrong. Per-request construction after authentication is the simplest conservative partition.

Normal execution permits sibling reordering/parallelism, so any observable domain side effect in an ordinary field can make result depend on executor scheduling. Requiring those fields to be side-effect-free and idempotent removes that ordering dependency. Serial top-level mutation fields establish order, not all-or-nothing atomicity.

## Alternatives and Trade-Offs

DataLoader-style batching preserves field-local resolvers and optimizes repeated key access. Joins/eager loading can be faster for known selections and one datastore. Selection-aware repositories reduce bytes but couple planning to GraphQL documents. A graph/federation planner can optimize across services but adds composition and execution complexity. Combine mechanisms at owned boundaries based on traces.

Request memoization gives natural isolation and consistency duration but repeats work across requests. Shared caches improve hit rate but require explicit tenant/principal-safe keys, TTL/invalidation, data classification, stampede control, and authorization at read time. They are a separate architecture, not a loader scope tweak.

Per-key errors preserve partial results; whole-batch failure is simpler when the dependency operation is atomic. Converting forbidden to absence can reduce existence leakage but reduces diagnostic distinction. The schema/security contract chooses, and telemetry retains protected detail.

Parallel resolution reduces latency for independent I/O but increases dependency concurrency and nondeterminism. Concurrency caps protect dependencies but add queues and deadline pressure. Fully serial execution is predictable but wastes independence and cannot substitute for correct side-effect rules.

Loader keys can be resource IDs only when one request already fixes all visibility/representation context. Composite keys make variants explicit but reduce deduplication and risk accidental omission. Separate loaders per semantic variant often produce clearer ownership.

## Failure Modes and Misconceptions

- **“One resolver runs for every field spelling.”** Compatible selections are collected by response name across fragments before field execution.
- **“Queries execute left to right.”** Normal execution may choose order/parallelism; only top-level mutation fields have specified serial behavior.
- **“A mutation operation is a transaction.”** Serial root execution supplies order, not rollback, isolation across requests, or atomic commit.
- **“Thin resolvers contain no policy.”** They still own field adaptation, domain validation invocation, context propagation, null/error mapping, and evidence.
- **“N+1 means SQL only.”** Any per-parent downstream operation can amplify: RPC, object store, authorization, cache, or filesystem.
- **“One batch means bounded work.”** Batch key count, bytes, backend plan, locking, time, concurrency, and response size need independent bounds.
- **“The backend will return input order.”** Many `IN`/bulk APIs reorder or omit; positional alignment is an explicit invariant.
- **“DataLoader is a shared cache.”** Its primary safe role is per-request batching/memoization; cross-request caching is a distinct system.
- **“ID alone is always a safe key.”** Visibility and representation may vary by tenant/principal/policy/snapshot/locale/projection.
- **“Memoized objects can be patched in place.”** Mutation creates order-dependent sibling results; cached values should be immutable and invalidated/primed deliberately.
- **“Returning null handles every exception.”** It erases fault/absence distinction and may violate non-null or security policy.
- **“Fewer dependency calls proves improvement.”** Measure latency, bytes, saturation, errors, correctness, and cache isolation too.

## Worked Examples

### Example 1

**Situation:** `name` appears directly and in two fragments under the same response name. **Reasoning:** field collection groups compatible selections, so resolve it once and complete the merged selection. Counting syntax nodes would overstate work. **Conclusion:** plan from collected fields, not raw occurrences.

### Example 2

**Situation:** Two query siblings increment a domain counter and read it. **Reasoning:** normal execution may reorder/overlap them, producing nondeterministic output. Replace the increment with an explicit mutation; keep queries observational. **Conclusion:** ordinary fields must not depend on execution order.

### Example 3

**Situation:** One mutation document contains `charge` then `reserve`. **Reasoning:** root fields run serially, but `charge` may commit before `reserve` fails and concurrent requests still interleave. Use a domain command/workflow if atomic business intent spans both. **Conclusion:** serial is not transactional.

### Example 4

**Situation:** 100 orders reference 60 customers and batch cap is 25. **Reasoning:** naive calls are 101; aligned deduplicated batching uses $1+\lceil60/25\rceil=4$ calls. Inspect bytes and batch latency before declaring success. **Conclusion:** quantify both amplification and optimization limits.

### Example 5

**Situation:** Backend returns customers `[9,2]` for requested `[2,9,6]`. **Reasoning:** returning rows directly swaps identities and omits a slot. Index by ID and return `[customer2, customer9, missing]` with policy-defined missing semantics. **Conclusion:** batch result order follows requested keys.

### Example 6

**Situation:** A singleton loader caches raw ID 7 from tenant A, then tenant B loads ID 7. **Reasoning:** the cache substitutes A's value under a different visibility context. Create per-request loaders after authentication and authorize resolved resources. **Conclusion:** cache scope is a security boundary.

### Example 7

**Situation:** A mutation updates user 4 after `userLoader` already memoized it. **Reasoning:** nested payload fields can see stale data. After commit, clear every equivalent key and prime from authoritative returned state, or read under a documented snapshot policy. **Conclusion:** mutation consistency requires deliberate loader invalidation.

### Example 8

**Situation:** A 50 ms custom batch window produces large batches but adds 50 ms to a 40 ms remaining deadline. **Reasoning:** work expires before dispatch. Use a small immediate scheduling window, adapt/skip batching when budget is tight, and measure queue delay. **Conclusion:** batch size trades against latency budget.

### Example 9

**Situation:** One key times out in a bulk call while 49 succeed. **Reasoning:** if dependency protocol identifies per-key results, align an error only to that key; whole-batch rejection discards valid partial work. Never cache the timeout as stable absence. **Conclusion:** failure granularity should match evidence.

### Example 10

**Situation:** Tracing creates a span and metric label for every alias/list path. **Reasoning:** caller-controlled cardinality overwhelms telemetry and may expose IDs. Aggregate metrics by schema coordinate/error class/dependency and sample protected response paths. **Conclusion:** execution observability must itself be bounded.

## Cross-Program Connections

- **Algorithms and Data Structures:** DAG traversal, maps, stable positional alignment, partitioning, and memoization implement execution and batching.
- **Concurrent Programming:** futures, structured cancellation, sibling scheduling, concurrency caps, and immutable shared values govern resolver safety.
- **Database Engineering:** joins, `IN` queries, parameter/plan limits, snapshots, transactions, and identity maps shape data loading.
- **Distributed Systems Engineering:** partial failure, deadlines, retries, consistency, and local observations constrain partial results.
- **Security Engineering:** request-context isolation, authorization-sensitive keys, redaction, and existence leakage define loader trust.
- **Observability and Performance:** operation normalization, coordinate metrics, critical paths, queueing, and tail distributions provide evidence.

## References

1. GraphQL Foundation, “GraphQL Specification, September 2025,” execution, collected fields, normal/serial execution, value completion, execution errors, response positions, and response format, verified 2026-09-02. [GraphQL specification](https://spec.graphql.org/September2025/).
2. GraphQL Foundation, “Execution,” official resolver, root, context, argument, asynchronous result, and type-resolution overview, verified 2026-09-02. [GraphQL documentation](https://graphql.org/learn/execution/).
3. GraphQL Foundation, “Response,” official data, request-error, execution-error, partial-data, path, and extensions guidance, verified 2026-09-02. [GraphQL documentation](https://graphql.org/learn/response/).
4. GraphQL Foundation, “Performance,” official N+1, batching, caching, and demand-oriented performance guidance, verified 2026-09-02. [GraphQL documentation](https://graphql.org/learn/performance/).
5. GraphQL Foundation, “DataLoader,” reference implementation documentation for batching, key/result alignment, scheduling, request memoization, errors, invalidation, duplicate keys, and batch bounds, verified 2026-09-02. [DataLoader repository](https://github.com/graphql/dataloader).
6. GraphQL Foundation, “Serving over HTTP,” official request pipeline and transport-layer placement guidance, verified 2026-09-02. [GraphQL documentation](https://graphql.org/learn/serving-over-http/).

## Exercises

### Exercise 1

Define field collection, resolver, value completion, response path, N+1, batch loader, request memoization, and batch window. Explain normal versus serial execution.

### Exercise 2

A query fetches 240 invoices referencing 83 unique accounts. The account backend accepts at most 30 keys per call. Compute naive and batched round trips at this level. State what the arithmetic does not prove.

### Exercise 3

Design a batch function for requested keys `[A, C, A, B, D]` when the backend returns `B`, `A`, and an error for `D` in arbitrary order while `C` is absent. Cover cache-enabled/disabled duplicate behavior, output alignment, per-key error, and bounds.

### Exercise 4

Diagnose a server whose singleton loader key is numeric ID, resolver context contains a mutable ORM session, query fields write audit-domain state, a mutation fails to invalidate cached values, and raw response paths label metrics. Provide a repair and verification plan.

### Exercise 5

Design execution for a multi-tenant emergency coordination query/mutation graph. It reads incidents, responders, locations, and capabilities from separate dependencies; mutations assign responders; partial dependency failure is expected; deadlines are tight. Specify resolver/context ownership, loader keys/scope/bounds/scheduling, transaction/read-after-write behavior, error/null mapping, cancellation, observability, and adversarial tests. State what API-057 and API-058 must still decide.

## Answers to the Exercises

### Answer 1

Field collection groups applicable selections by response name after fragments, directives, aliases, and runtime type conditions are considered. A resolver derives a field value from parent, coerced arguments, request context, and execution information. Value completion converts that result according to the declared scalar/enum/object/list/non-null type, recursively executing children. A response path locates a result position using aliases and list indices. N+1 is one parent operation plus repeated child work per parent. A batch loader coalesces compatible key loads and aligns one result/error per original key. Request memoization reuses equivalent loads only within one request/visibility context. A batch window is the scheduling interval that gathers keys.

Query root and nested collected fields execute normally, so order is not guaranteed and parallelism is allowed. Top-level mutation fields execute serially in textual order; their nested selections execute normally. Serial ordering does not imply transactionality or isolation from other requests.

### Answer 2

Naive relationship resolution makes one invoice call plus one account call per invoice: $1+240=241$ calls. Deduplication yields 83 account keys. With maximum 30 keys, account calls are $\lceil83/30\rceil=3$, so this level uses $1+3=4$ calls.

This does not prove whole-operation call count, latency, correctness, or capacity. Deeper dependency waves can add calls; batches may run serially or concurrently; authorization/locale/snapshot can prevent deduplication; retries add work; 30-key calls may have nonlinear cost; and bytes, rows, locks, pool saturation, scheduler delay, cache semantics, null/error behavior, and result alignment require evidence.

### Answer 3

Construct an index keyed by authorized stable identity from the backend's unordered outcomes: `A → valueA`, `B → valueB`, `D → errorD`; `C` has the policy-defined absence marker. Map over original keys to return `[valueA, absentC, valueA, valueB, errorD]`. Length is five and every index corresponds to its request key. Never return the backend iteration list.

With cache-enabled deduplication, the loader may batch unique `[A,C,B,D]` and fulfill both A promises from one memoized result. With caching disabled, the library may pass `[A,C,A,B,D]`; the batch function must return two A slots. Verify the chosen library. A per-key `D` error should reject/mark only D when supported; a thrown/rejected batch would fail every key and is reserved for batch-wide failure. Bound input count/bytes, partition if necessary while preserving final alignment, share one deadline/cancellation, authorize each resolved resource, and do not cache transient D failure as absence.

### Answer 4

Create authenticated request context once with immutable principal/tenant, deadline/cancellation, trace linkage, and scoped domain ports/loaders. Application pools remain global, but ORM unit-of-work/session and loaders are request/transaction scoped and cleaned up. Replace the singleton loader with per-request loaders or explicit equivalent visibility partitions; include every semantic variant in key/instance and authorize resources.

Move domain audit writes out of query/nested resolvers into explicit mutations or a non-domain operational signal that cannot affect query semantics. Keep ordinary fields side-effect-free/idempotent. Define mutation transaction ownership; after commit, clear/prime every loader key/alias affected or return authoritative domain values under a documented snapshot/read-your-writes policy. Cached objects are immutable.

Metrics aggregate by bounded schema coordinate, dependency, outcome/error class, and loader name; protected sampled traces can retain response path. Never label by aliases, IDs, raw arguments, or error messages. Verify with concurrent tenant A/B same-ID tests, randomized resolver order, repeated fragments, mutation read-after-write, rollback/commit, loader release, cancellation, batch alignment, null propagation, sensitive-data scans, and before/after dependency/latency/saturation measurements.

### Answer 5

Create one context after authenticating the caller: immutable actor/tenant/policy identity, one shrinking deadline and cancellation signal, trace correlation, request-scoped incident/responder/location/capability loaders, and an explicitly owned unit of work for mutations. Resolvers translate typed fields to domain queries/commands and return stable view/domain values; they do not expose clients/sessions or embed arbitrary cross-field business logic. Query and nested resolvers are side-effect-free.

Loader instances are request scoped. Keys bind tenant and stable resource ID plus policy/snapshot/locale/projection facts that affect visibility; alternatively separate loaders per invariant. Each batch function caps keys/bytes, partitions under dependency limits, aligns unordered/missing/per-key-error results to original positions, limits concurrent sub-batches, and propagates remaining deadline/cancellation. Use an immediate scheduling window measured against the tight budget; do not wait deliberately when remaining time is smaller. Treat values as immutable and discard caches at request end.

`assignResponder` is one intent mutation with an operation/idempotency identity and domain transaction/workflow. Root mutations serialize but the command owns atomic state. After commit, clear/prime incident/responder/assignment keys from authoritative state; if nested payload reads use transaction state, bind loaders to that connection/snapshot and prevent escape. Cancellation does not imply rollback after commit; expose stable outcome recovery.

Map expected unavailable responder/location states to typed domain data when the schema promises them. Map dependency faults to redacted execution errors at exact response paths; nullable fields permit useful incident data to continue, while non-null propagation follows the schema. Whole-batch failure affects its keys, while identified per-key failures preserve others. Never turn authorization failure into a cached generic miss without the graph's existence policy.

Record bounded operation identity/schema version, phase and total latency, coordinates, dependency calls/bytes, batch size/queue delay/cache outcome, concurrency, cancellation, null propagation, and safe error class. Sample protected paths; exclude patient/location details, tokens, IDs, aliases, and raw variables from labels. Test fragments/aliases, 0/1/max/over-max cardinality, unordered/duplicate/missing keys, cross-tenant same IDs, policy changes, partial and whole dependency failure, cancellation before/after dispatch/commit, tight deadlines, mutation read-after-write, concurrent assignments, non-null propagation, loader cleanup, telemetry leakage, and semantic equivalence to an unbatched oracle.

API-057 must still define connection/cursor semantics, ordering stability, and incremental response delivery. API-058 must define field/resource authorization placement, introspection policy, operation depth/complexity/admission, and abuse/cost controls. Loaders implement those decisions at data-access boundaries but do not replace them.
