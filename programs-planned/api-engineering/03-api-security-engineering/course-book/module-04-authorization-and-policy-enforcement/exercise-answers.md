# Reference Answers — Module 04: Authorization and Policy Enforcement

Read after attempting all twelve Authorization and Policy Enforcement exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Why is a scope not object authorization?

**Answer.** It states delegated capability for an operation class, not the caller’s relationship to a specific project, dataset, run, or artifact.

## 2. Where should tenant filtering occur?

**Answer.** In the authoritative query or transaction so foreign rows are not loaded and later filtered by application convenience.

## 3. What does default deny mean for a new endpoint?

**Answer.** Until an explicit policy row and enforcement mapping exist, the endpoint is inaccessible.

## 4. When use 403 versus concealed 404?

**Answer.** Use policy-defined behavior: 403 when revealing existence is acceptable and actionable; concealed 404 when foreign-object existence is sensitive.

## 5. Why is authorization after lookup risky?

**Answer.** The lookup may disclose data, timing, or existence and may be reused by code paths that forget the later check.

## 6. What is an obligation?

**Answer.** A condition attached to allow, such as redact a field, require audit, constrain query tenant, or enforce recent authentication.

## 7. How should support impersonation be modeled?

**Answer.** As explicit time-bounded delegated context with reason, actor and effective principal, restricted actions, audit, and revocation.

## 8. Why protect output fields?

**Answer.** A caller may be allowed to read a resource but not internal owner, diagnostic, or security metadata.

## 9. How does ETag mutation interact with authorization?

**Answer.** The transaction must constrain owner/tenant and expected version atomically; a prechecked policy cannot authorize a later changed resource blindly.

## 10. What proves list isolation?

**Answer.** Create interleaved resources for two tenants and assert pages, counts, cursors, and errors reveal only the caller’s permitted set.

## 11. Trace default-deny resource authorization in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_security/authorization.py` and `capstone/tracks/typescript-fastify/src/security/authorization.ts`. The required invariant is that scope, role, tenant, relationship, assurance, freshness, and concealment are evaluated for the exact operation and resource.

## 12. Compare default-deny resource authorization across Python and TypeScript

Both tracks must preserve this invariant: scope, role, tenant, relationship, assurance, freshness, and concealment are evaluated for the exact operation and resource. The intentional difference is that policy representation differs; an unknown operation and a cross-owner request must both deny.
