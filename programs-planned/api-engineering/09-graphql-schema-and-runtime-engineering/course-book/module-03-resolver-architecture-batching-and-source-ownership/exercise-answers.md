# Worked answers — Resolver Architecture, Batching, and Source Ownership

Compare the decision rule and evidence, not just wording.

## 1. Why does N+1 appear naturally in field execution?

Nested resolvers run once per parent. Direct source calls therefore multiply with parent count unless compatible keys are batched.

**Decisive evidence.** Execute the same nested operation for one, ten, and twenty parents and plot source calls. A call count that grows linearly with parents demonstrates N+1.

## 2. What must a DataLoader cache key contain?

Every dimension that changes the value or authorization: local ID, tenant/principal partition, locale or representation variant, and sometimes source version.

**Decisive evidence.** Construct two requests that share a local ID but differ in tenant, permission class, locale, or source version. A correct key must prevent one representation from satisfying the other.

## 3. Why must loaders be request-scoped?

Cross-request caches can return values authorized under another principal and can serve stale source data without an explicit policy.

**Decisive evidence.** Run identical operations for two principals in sequence. The second request must perform its own authorized load; any cross-request hit is a leakage defect.

## 4. What does batching prove that caching alone does not?

Batching reduces source calls for distinct keys. Caching only avoids repeated identical keys and can still leave one call per parent.

**Decisive evidence.** Use repeated keys and distinct keys in one operation. One batch call with correct key-to-value association proves batching; a cache hit alone does not prove source-call collapse.

## 5. How should missing batch keys be represented?

The batch function returns a keyed result; missing keys map to null/not-found according to field semantics, preserving input order at the loader boundary.

**Decisive evidence.** Ask for existing, missing, and concealed keys in one batch. The result mapping must preserve every requested key and distinguish authoritative absence from per-key failure.

## 6. Why can one giant batch still be unsafe?

It can exceed service limits, deadlines, memory, or response size. Batch size must be bounded and may require chunking.

**Decisive evidence.** Submit a page at the maximum allowed size and one above it while recording batch bytes, latency, and source limits. Admission or chunking must keep the owner within its contract.

## 7. Who should authorize artifact access?

Edge policy may reject missing permission early, but Artifact Service remains authoritative for capability and resource state.

**Decisive evidence.** Remove `ARTIFACT_READ` while leaving run visibility intact. The artifact source must receive zero keys, proving authorization happened before batching.

## 8. What is wrong with a resolver opening a database connection?

It bypasses the service owner, duplicates authorization and schema knowledge, and creates hidden coupling.

**Decisive evidence.** Scan the resolver track for database drivers and execute the loopback lab. All business-field values must arrive through service clients, never cross-service SQL.

## 9. How does a graph request deadline reach resolvers?

The request context carries one absolute deadline. Each downstream call receives a child budget from the remaining time, not a fresh timeout.

**Decisive evidence.** Start an operation with a short absolute deadline and inspect child budgets. No resolver may receive a fresh full timeout or continue after cancellation.

## 10. What telemetry identifies N+1 in production?

Operation identity, field coordinate, batch size, dispatch count, downstream call count, and parent cardinality.

**Decisive evidence.** Use operation identity, field coordinate, parent count, unique-key count, batch size, dispatch count, and source spans. These bounded dimensions must expose call amplification without object-ID metric labels.

## 11. Why can a global loader be correct in tests and unsafe in production?

Sequential tests may use one principal and fresh process. Concurrent tenants expose cross-request cache leakage.

**Decisive evidence.** Run a single-request unit test and then concurrent cross-tenant requests against the same process. A global cache that passes the first but leaks in the second is rejected.

## 12. When can a gateway compute a field without a source call?

When the value is deterministic from already authorized parent data, such as global-ID encoding, and no business decision is duplicated.

**Decisive evidence.** Approve a computed field only when all inputs are already authorized parent/context values and no new business decision is invented. A source trace of zero calls is then expected.
