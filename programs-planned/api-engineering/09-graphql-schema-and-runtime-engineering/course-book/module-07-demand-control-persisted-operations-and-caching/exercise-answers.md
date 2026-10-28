# Worked Answers — Module 07: Demand Control, Persisted Operations, and Caching

Use these solutions to audit your reasoning for **Demand Control, Persisted Operations, and Caching**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why does depth limiting alone fail?

A shallow query can repeat expensive fields through aliases or request broad lists. Depth measures only one dimension.

**Decisive evidence.** Construct a shallow operation with hundreds of aliases or a large list multiplier. It must exceed budget despite low depth, proving depth alone is insufficient.

The chapter’s decisive distinction is this: A valid operation can repeat an expensive field under many aliases, expand fragments, request the maximum list size at several levels, and trigger several remote services. Demand control begins before execution with document size, token, depth, alias, root-field, cost, and fan-out budgets.

## 2. Why count aliases as executed occurrences?

Each alias creates a separate response entry and can invoke the resolver again with distinct arguments.

**Decisive evidence.** Alias one expensive nested field repeatedly. The analyzer must count each executed occurrence rather than one schema coordinate.

In the cumulative capstone, the rule becomes concrete: Aliases create distinct response entries and may execute a resolver repeatedly. Cost analysis counts each occurrence, not unique field names. Fragment spreads are expanded along executed paths; cyclic fragments are rejected. Inline fragments contribute cost when their type conditions can apply.

## 3. How do fragments affect cost?

Their selections are expanded at each executed spread. Cycles are rejected and repeated spreads contribute repeated cost.

**Decisive evidence.** Place expensive selections behind reused and nested fragments. Expanded occurrence, depth, cycle, and cardinality reports must match the executable selection set.

A useful way to reason about the boundary is: A depth limit catches pathological recursion-like shapes but misses broad expensive queries. An alias limit catches repeated sibling work but misses one huge list. A page-size limit catches one cardinality source but misses nested products. A service fan-out limit catches architecture amplification but not expensive local computation.

## 4. Why multiply nested cost by list cardinality?

Each parent item can execute the nested selection. Without a multiplier, one field appears cheap while producing hundreds of resolutions.

**Decisive evidence.** Compare cost for `first=1`, `20`, and `100`, then nest a second list. The model must reflect the product of possible parent and child executions.

The implementation consequence is: No single metric is sufficient. Depth alone misses broad alias storms. Field count ignores list cardinality. Static cost misses runtime filter selectivity. The course combines conservative admission with runtime telemetry and source-service limits.

## 5. What remains dynamic after a persisted operation is approved?

Variables, principal, tenant, source state, deadline, and page size. Runtime validation and budgets still apply.

**Decisive evidence.** Change list variables, filters, optional branches, client identity, and current concurrency. Registration fixes document bytes, not all runtime demand.

The important nuance is: Admission rejection is preferable to accepting a query that cannot complete within its deadline. The runtime returns a stable code such as QUERY BUDGET EXCEEDED; it does not silently drop selected fields. Per-client concurrency and cost budgets connect Course 5 traffic controls to GraphQL operation identity.

## 6. Why is APQ not necessarily an allowlist?

It can accept and cache arbitrary documents presented by clients. Its primary purpose is request-size reduction unless policy restricts registration.

**Decisive evidence.** Enable automatic persisted-query registration in a scratch profile and submit a new digest. Unless a separate allowlist gate exists, APQ learns arbitrary documents and is not trusted-document admission.

Under concurrency or failure, the distinction becomes: Development and privileged tools may use arbitrary documents under separate limits. Public clients use the trusted registry. This distinction preserves the interactive strengths of GraphQL without making the production endpoint accept unreviewed programs from every caller.

## 7. What identifies a trusted operation?

The SHA-256 of the exact registered UTF-8 document plus its governed name, client owner, version, and status.

**Decisive evidence.** Verify the registry binding among exact UTF-8 digest, operation name, client releases, owner, schema release, status, and reviewed cost. A name alone is insufficient.

The design remains honest only if: A trusted document registry admits only operations reviewed for schema, cost, ownership, and client lifecycle. The client sends the SHA-256 digest of the exact UTF-8 document. Runtime variables remain validated and budgeted.

## 8. Why include client identity in concurrency budgets?

Different clients have different traffic and risk. Operation-only limits let one client starve others.

**Decisive evidence.** Run equal-cost operations from two clients with different concurrency agreements. Admission must enforce the correct client partition and prevent one client from consuming another budget.

The consumer-facing consequence is: A mobile client sends a registered GetProjectOverview operation with first=20. The registry confirms client and document identity. Standard validation passes. Cost evaluation expands fragments, reads the coerced page size, counts artifact and delivery fields, and predicts two downstream services. The total fits the client's budget, so execution begins.

## 9. What must a response-cache key include?

Operation hash, normalized variables, authorization partition, schema version, representation variants, and source-version policy.

**Decisive evidence.** Vary operation digest, canonical variables, tenant/audience, schema release, representation, source versions, and completeness state. Any dimension that changes the result must change or invalidate the cache entry.

The operational consequence is: GraphQL response caching is difficult because one response may depend on several services, permissions, variables, and source versions. A cache key must include operation identity, normalized variables, principal or authorization partition, schema version, and relevant representation variants. Invalidation must follow source ownership.

## 10. Why is DataLoader caching not response caching?

It lasts one request and deduplicates source keys; it does not reuse a completed GraphQL response across requests.

**Decisive evidence.** Run two requests for the same node. Request-scoped loader caching disappears between them; response caching intentionally survives only under a separate consistency and identity policy.

The strongest engineering interpretation is: Do not cache partial errors as successful complete responses without an explicit policy. A cached artifacts: null caused by a temporary outage can outlive the failure and mislead clients. The cache record must preserve completeness and source-version semantics.

## 11. What does a budget rejection return?

A stable admission error before execution. It must not drop selected fields or call downstream services.

**Decisive evidence.** Inspect rejection data and source traces. The client receives a stable budget code and bounded metadata, while downstream call count remains zero.

The defect-oriented view is: Do not “degrade” by silently dropping selected fields or reducing page sizes. The response would no longer match the requested program. Valid degradation follows declared schema semantics: nullable remote fields may fail with path errors, a stale projection may be returned with age metadata, or the whole operation may be rejected.

## 12. How should new operations enter production?

Register, validate, estimate, run against fixtures, assign owner and client version, then release through the operation registry.

**Decisive evidence.** Require source-controlled document, owner, client catalogue entry, schema validation, budget report, authorization review, release approval, and retirement policy before activating the digest.

Across the Python and TypeScript tracks, the invariant is: GraphQL validation answers whether a document is legal for the schema. It does not answer whether the operation is affordable for this service, client, tenant, or moment. An operation can be shallow but wide, deeply nested but cheap, or use aliases and fragments to repeat an expensive field many times.
