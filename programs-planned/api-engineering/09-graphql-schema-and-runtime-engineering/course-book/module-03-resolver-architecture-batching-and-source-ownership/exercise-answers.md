# Worked Answers — Module 03: Resolver Architecture, Batching, and Source Ownership

Use these solutions to audit your reasoning for **Resolver Architecture, Batching, and Source Ownership**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why does N+1 appear naturally in field execution?

Nested resolvers run once per parent. Direct source calls therefore multiply with parent count unless compatible keys are batched.

**Decisive evidence.** Execute the same nested operation for one, ten, and twenty parents and plot source calls. A call count that grows linearly with parents demonstrates N+1.

The chapter’s decisive distinction is this: GraphQL executes a field for each parent value. A project with twenty runs can cause twenty artifact calls and twenty notification calls if nested resolvers call services directly. The schema looks elegant while latency, load, and failure probability multiply.

## 2. What must a DataLoader cache key contain?

Every dimension that changes the value or authorization: local ID, tenant/principal partition, locale or representation variant, and sometimes source version.

**Decisive evidence.** Construct two requests that share a local ID but differ in tenant, permission class, locale, or source version. A correct key must prevent one representation from satisfying the other.

In the cumulative capstone, the rule becomes concrete: A batch loader collapses duplicate keys and dispatches them together. The source method returns a map keyed by requested identity; the loader restores each result to its resolver. The key must include every dimension that changes authorization or representation. A run identifier alone is insufficient if two tenants can use the same local identifier or if the field has locale variants.

## 3. Why must loaders be request-scoped?

Cross-request caches can return values authorized under another principal and can serve stale source data without an explicit policy.

**Decisive evidence.** Run identical operations for two principals in sequence. The second request must perform its own authorized load; any cross-request hit is a leakage defect.

A useful way to reason about the boundary is: Both tracks implement a request-scoped BatchLoader. Python uses explicit load tokens and dispatch; TypeScript uses a generic loader. The shared invariant is one batch call per compatible key set and zero cross-request cache hits.

## 4. What does batching prove that caching alone does not?

Batching reduces source calls for distinct keys. Caching only avoids repeated identical keys and can still leave one call per parent.

**Decisive evidence.** Use repeated keys and distinct keys in one operation. One batch call with correct key-to-value association proves batching; a cache hit alone does not prove source-call collapse.

The implementation consequence is: Batching reduces call count, not source workload automatically. A batch of ten thousand keys can still overwhelm a service, which is why list size and batch size are bounded. Batches may need chunking under a remaining deadline.

## 5. How should missing batch keys be represented?

The batch function returns a keyed result; missing keys map to null/not-found according to field semantics, preserving input order at the loader boundary.

**Decisive evidence.** Ask for existing, missing, and concealed keys in one batch. The result mapping must preserve every requested key and distinguish authoritative absence from per-key failure.

The important nuance is: The batch result must preserve input-key association. Returning a positional list without checking keys is unsafe when the source omits missing records or returns a different order. The reference loader accepts a mapping and reconstructs values in requested order.

## 6. Why can one giant batch still be unsafe?

It can exceed service limits, deadlines, memory, or response size. Batch size must be bounded and may require chunking.

**Decisive evidence.** Submit a page at the maximum allowed size and one above it while recording batch bytes, latency, and source limits. Admission or chunking must keep the owner within its contract.

Under concurrency or failure, the distinction becomes: Batching does not make an unbounded query safe. A query that requests one thousand parents can still create a one-thousand-key batch. Admission bounds list cardinality; the loader bounds batch size and may split work into controlled chunks. Both controls are required.

## 7. Who should authorize artifact access?

Edge policy may reject missing permission early, but Artifact Service remains authoritative for capability and resource state.

**Decisive evidence.** Remove `ARTIFACT_READ` while leaving run visibility intact. The artifact source must receive zero keys, proving authorization happened before batching.

The design remains honest only if: A field resolver converts parent value, arguments, context, and selected information into a field value. It should not decide a business rule owned elsewhere. Mutation.startAnalysis delegates to Analysis Control. AnalysisRun.artifacts calls Artifact Service. The gateway may map service errors and identifiers, but it does not recreate run state transitions or artifact authorization.

## 8. What is wrong with a resolver opening a database connection?

It bypasses the service owner, duplicates authorization and schema knowledge, and creates hidden coupling.

**Decisive evidence.** Scan the resolver track for database drivers and execute the loopback lab. All business-field values must arrive through service clients, never cross-service SQL.

The consumer-facing consequence is: A resolver may be only ten lines and still violate every boundary if it opens a database connection to another service's tables. Conversely, a slightly longer adapter that decodes identity, checks policy, allocates a child deadline, and maps a source problem can be the correct design.

## 9. How does a graph request deadline reach resolvers?

The request context carries one absolute deadline. Each downstream call receives a child budget from the remaining time, not a fresh timeout.

**Decisive evidence.** Start an operation with a short absolute deadline and inspect child budgets. No resolver may receive a fresh full timeout or continue after cancellation.

The operational consequence is: One graph operation can call several services. Each call consumes the absolute request deadline inherited from Course 4. A resolver cannot start a fresh full timeout. The graph admission report estimates service fan-out before execution; runtime telemetry records actual calls and latency.

## 10. What telemetry identifies N+1 in production?

Operation identity, field coordinate, batch size, dispatch count, downstream call count, and parent cardinality.

**Decisive evidence.** Use operation identity, field coordinate, parent count, unique-key count, batch size, dispatch count, and source spans. These bounded dimensions must expose call amplification without object-ID metric labels.

The strongest engineering interpretation is: Dispatch timing matters. A loader that dispatches immediately still performs N calls. A loader that waits without a bound can delay the entire operation. Complete GraphQL runtimes schedule field work in waves; the dependency-light course core makes dispatch explicit so the batching invariant is visible.

## 11. Why can a global loader be correct in tests and unsafe in production?

Sequential tests may use one principal and fresh process. Concurrent tenants expose cross-request cache leakage.

**Decisive evidence.** Run a single-request unit test and then concurrent cross-tenant requests against the same process. A global cache that passes the first but leaks in the second is rejected.

The defect-oriented view is: Never place these values in process-global mutable state. GraphQL executes sibling fields concurrently in many runtimes, and one process serves many tenants. A global “current user” or global loader can leak data across requests. Async-local context can improve ergonomics, but explicit resolver context remains the ownership boundary and must be set and cleared correctly.

## 12. When can a gateway compute a field without a source call?

When the value is deterministic from already authorized parent data, such as global-ID encoding, and no business decision is duplicated.

**Decisive evidence.** Approve a computed field only when all inputs are already authorized parent/context values and no new business decision is invented. A source trace of zero calls is then expected.

Across the Python and TypeScript tracks, the invariant is: Two runs selected under one project schedule two artifact keys and two delivery keys. Each loader collapses duplicates and performs one service batch. A third occurrence of run-1 reuses the request token. A second HTTP request creates new loaders, so no authorized value leaks across principals.
