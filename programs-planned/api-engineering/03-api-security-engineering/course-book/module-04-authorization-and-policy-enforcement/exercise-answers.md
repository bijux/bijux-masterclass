# Worked Answers — Module 04: Authorization and Policy Enforcement

Use these solutions to audit your reasoning for **Authorization and Policy Enforcement**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why is a scope not object authorization?

It states delegated capability for an operation class, not the caller’s relationship to a specific project, dataset, run, or artifact.

The chapter’s decisive distinction is this: Implement the full API 1.2 policy matrix and run cross-tenant object, list, mutation, artifact, and support-context tests. Plant one missing owner predicate in artifact retrieval and prove the shared attack vector detects it.

**Evidence.** Exercise missing scope, correct scope/wrong owner, wrong tenant, stale support context, field restrictions, and successful ownership while checking that denied requests perform no protected source I/O.

## 2. Where should tenant filtering occur?

In the authoritative query or transaction so foreign rows are not loaded and later filtered by application convenience.

In the cumulative capstone, the rule becomes concrete: Collection authorization is not “load everything, then filter the response.” The repository query must include tenant and relationship constraints so foreign rows do not enter application memory, counts, pagination boundaries, caches, or timing-sensitive branches. The same principle applies to nested identifiers: a dataset ID must be constrained through its project ownership rather than trusted because the URL also contains a project ID.

## 3. What does default deny mean for a new endpoint?

Until an explicit policy row and enforcement mapping exist, the endpoint is inaccessible.

A useful way to reason about the boundary is: Support and administrative access should be more constrained, not exempt. Require a named role, explicit operation, reason, stronger assurance, recent authentication, bounded delegation, and an audit event. “Admin bypass” is not a policy because it erases resource, action, and incident accountability.

**Evidence.** Remove the central guard in a planted variant and require the negative security suite to detect the exact unauthorized or leaked outcome.

## 4. When use 403 versus concealed 404?

Use policy-defined behavior: 403 when revealing existence is acceptable and actionable; concealed 404 when foreign-object existence is sensitive.

The implementation consequence is: A time-of-check/time-of-use defect occurs when ownership or state changes between the authorization read and the mutation. Prefer one owner-constrained update or a transaction that locks and verifies the relevant version. Caching allow decisions is dangerous unless the cache key includes principal, operation, resource identity and version, tenant, policy revision, and any freshness conditions—and even then invalidation must be explicit.

## 5. Why is authorization after lookup risky?

The lookup may disclose data, timing, or existence and may be reused by code paths that forget the later check.

The important nuance is: Authentication produces a principal. Authorization evaluates whether that principal may perform one operation on one resource under current policy and context. A scope such as artifacts:read is therefore necessary information, not a complete decision. The caller may hold the scope for tenant A and still be forbidden from reading tenant B.

## 6. What is an obligation?

A condition attached to allow, such as redact a field, require audit, constrain query tenant, or enforce recent authentication.

Under concurrency or failure, the distinction becomes: Field-level policy applies in both directions. Input models must not allow a caller to assign ownerId, tenant, role, lifecycle state, or server-generated version. Output projection must remove fields the principal is not entitled to see. Serialization models help, but the policy still needs a test that plants a sensitive internal field and proves it cannot cross the boundary.

## 7. How should support impersonation be modeled?

As explicit time-bounded delegated context with reason, actor and effective principal, restricted actions, audit, and revocation.

The design remains honest only if: The decisive proof matrix crosses credential validity, scope, role, tenant, ownership, state, assurance, and freshness. Include combinations where exactly one dimension is wrong. Happy-path tests with one all-powerful fixture principal do not test authorization.

**Evidence.** Remove the central guard in a planted variant and require the negative security suite to detect the exact unauthorized or leaked outcome.

## 8. Why protect output fields?

A caller may be allowed to read a resource but not internal owner, diagnostic, or security metadata.

The consumer-facing consequence is: Field-level policy applies in both directions. Input models must not allow a caller to assign ownerId, tenant, role, lifecycle state, or server-generated version. Output projection must remove fields the principal is not entitled to see. Serialization models help, but the policy still needs a test that plants a sensitive internal field and proves it cannot cross the boundary.

## 9. How does ETag mutation interact with authorization?

The transaction must constrain owner/tenant and expected version atomically; a prechecked policy cannot authorize a later changed resource blindly.

The operational consequence is: A time-of-check/time-of-use defect occurs when ownership or state changes between the authorization read and the mutation. Prefer one owner-constrained update or a transaction that locks and verifies the relevant version. Caching allow decisions is dangerous unless the cache key includes principal, operation, resource identity and version, tenant, policy revision, and any freshness conditions—and even then invalidation must be explicit.

## 10. What proves list isolation?

Create interleaved resources for two tenants and assert pages, counts, cursors, and errors reveal only the caller’s permitted set.

The strongest engineering interpretation is: Implement the full API 1.2 policy matrix and run cross-tenant object, list, mutation, artifact, and support-context tests. Plant one missing owner predicate in artifact retrieval and prove the shared attack vector detects it.

**Evidence.** Remove the central guard in a planted variant and require the negative security suite to detect the exact unauthorized or leaked outcome.

## 11. Trace default-deny resource authorization in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_security/authorization.py` and `capstone/tracks/typescript-fastify/src/security/authorization.ts`. The required invariant is that scope, role, tenant, relationship, assurance, freshness, and concealment are evaluated for the exact operation and resource.

The defect-oriented view is: Authentication produces a principal. Authorization evaluates whether that principal may perform one operation on one resource under current policy and context. A scope such as artifacts:read is therefore necessary information, not a complete decision. The caller may hold the scope for tenant A and still be forbidden from reading tenant B.

## 12. Compare default-deny resource authorization across Python and TypeScript

Both tracks must preserve this invariant: scope, role, tenant, relationship, assurance, freshness, and concealment are evaluated for the exact operation and resource. The intentional difference is that policy representation differs; an unknown operation and a cross-owner request must both deny.

Across the Python and TypeScript tracks, the invariant is: The decisive proof matrix crosses credential validity, scope, role, tenant, ownership, state, assurance, and freshness. Include combinations where exactly one dimension is wrong. Happy-path tests with one all-powerful fixture principal do not test authorization.
