# Worked answers — Demand Control, Persisted Operations, and Caching

Compare the decision rule and evidence, not just wording.

## 1. Why does depth limiting alone fail?

A shallow query can repeat expensive fields through aliases or request broad lists. Depth measures only one dimension.

**Decisive evidence.** Construct a shallow operation with hundreds of aliases or a large list multiplier. It must exceed budget despite low depth, proving depth alone is insufficient.

## 2. Why count aliases as executed occurrences?

Each alias creates a separate response entry and can invoke the resolver again with distinct arguments.

**Decisive evidence.** Alias one expensive nested field repeatedly. The analyzer must count each executed occurrence rather than one schema coordinate.

## 3. How do fragments affect cost?

Their selections are expanded at each executed spread. Cycles are rejected and repeated spreads contribute repeated cost.

**Decisive evidence.** Place expensive selections behind reused and nested fragments. Expanded occurrence, depth, cycle, and cardinality reports must match the executable selection set.

## 4. Why multiply nested cost by list cardinality?

Each parent item can execute the nested selection. Without a multiplier, one field appears cheap while producing hundreds of resolutions.

**Decisive evidence.** Compare cost for `first=1`, `20`, and `100`, then nest a second list. The model must reflect the product of possible parent and child executions.

## 5. What remains dynamic after a persisted operation is approved?

Variables, principal, tenant, source state, deadline, and page size. Runtime validation and budgets still apply.

**Decisive evidence.** Change list variables, filters, optional branches, client identity, and current concurrency. Registration fixes document bytes, not all runtime demand.

## 6. Why is APQ not necessarily an allowlist?

It can accept and cache arbitrary documents presented by clients. Its primary purpose is request-size reduction unless policy restricts registration.

**Decisive evidence.** Enable automatic persisted-query registration in a scratch profile and submit a new digest. Unless a separate allowlist gate exists, APQ learns arbitrary documents and is not trusted-document admission.

## 7. What identifies a trusted operation?

The SHA-256 of the exact registered UTF-8 document plus its governed name, client owner, version, and status.

**Decisive evidence.** Verify the registry binding among exact UTF-8 digest, operation name, client releases, owner, schema release, status, and reviewed cost. A name alone is insufficient.

## 8. Why include client identity in concurrency budgets?

Different clients have different traffic and risk. Operation-only limits let one client starve others.

**Decisive evidence.** Run equal-cost operations from two clients with different concurrency agreements. Admission must enforce the correct client partition and prevent one client from consuming another budget.

## 9. What must a response-cache key include?

Operation hash, normalized variables, authorization partition, schema version, representation variants, and source-version policy.

**Decisive evidence.** Vary operation digest, canonical variables, tenant/audience, schema release, representation, source versions, and completeness state. Any dimension that changes the result must change or invalidate the cache entry.

## 10. Why is DataLoader caching not response caching?

It lasts one request and deduplicates source keys; it does not reuse a completed GraphQL response across requests.

**Decisive evidence.** Run two requests for the same node. Request-scoped loader caching disappears between them; response caching intentionally survives only under a separate consistency and identity policy.

## 11. What does a budget rejection return?

A stable admission error before execution. It must not drop selected fields or call downstream services.

**Decisive evidence.** Inspect rejection data and source traces. The client receives a stable budget code and bounded metadata, while downstream call count remains zero.

## 12. How should new operations enter production?

Register, validate, estimate, run against fixtures, assign owner and client version, then release through the operation registry.

**Decisive evidence.** Require source-controlled document, owner, client catalogue entry, schema validation, budget report, authorization review, release approval, and retirement policy before activating the digest.
