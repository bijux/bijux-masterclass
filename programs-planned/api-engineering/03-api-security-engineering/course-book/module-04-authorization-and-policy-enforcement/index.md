# Module 04 — Authorization and Policy Enforcement

> **Program stage:** Course 3 of 10 — Defend the promise.

> **Central question:** How are scopes, roles, ownership, tenant membership, relationships, assurance, and freshness combined under default deny?

## Where this module fits

Module 03 produced **Implement issuer, audience, algorithm, key, lifetime, revocation, subject, tenant, and scope validation**. This module extends that result by asking: **How are scopes, roles, ownership, tenant membership, relationships, assurance, and freshness combined under default deny?**

The new capstone increment is **Build explicit authorization decisions for collections, individual resources, fields, support access, and administration**. It becomes the prerequisite for **Hostile Input and File Handling**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Separate authentication from authorization.
- Model operation policy explicitly.
- Constrain collection queries before loading data.
- Apply field-level input and output policy.
- Prevent existence leaks and stale authorization decisions.

## Capstone increment

Build explicit authorization decisions for collections, individual resources, fields, support access, and administration.

## Core security model

### Driving question

> How does a verified principal receive only the operations, resource instances, and fields allowed in the current context?

Authorization is a default-deny decision over principal, action, resource, relationship, tenant, request fields, assurance, and time. Scopes alone are necessary metadata, not complete object authorization.

### 1. Policy decision point

A deterministic service evaluates policy inputs and returns allow/deny plus reason and obligations.

The transport or application boundary refuses to execute unless a valid allow decision applies to the exact action and resource.

Missing policy, unknown operation, absent attribute, or evaluation error denies rather than falls through.

Tenant membership constrains all collection and object queries before data leaves persistence.

Owner, project member, support delegate, or administrator relationships are explicit and time-bounded.

Allowed input fields and output projections can vary by principal and operation.

For selected foreign resources, return the same not-found behavior as absent resources to avoid existence disclosure.

Authorization facts used for mutation must remain valid at the durable decision point or be rechecked atomically.

### Synthesis

Draw the capstone data flow and annotate where each concept is owned. Any concept with no owner becomes a Module 04 defect.

## Authorization is a decision over an action and a resource

Authentication produces a principal. Authorization evaluates whether that principal may perform one operation on one resource under current policy and context. A scope such as `artifacts:read` is therefore necessary information, not a complete decision. The caller may hold the scope for tenant A and still be forbidden from reading tenant B.

Model the decision as a tuple:

```text
(operation, principal, resource facts, relationship, request context, policy revision)
    -> allow | deny | conceal | step-up
```

The operation must be the stable contract operation ID, not a route-function name. Resource facts should contain only the data needed for policy: tenant, owner, membership, state, sensitivity, and version. Request context can include authentication assurance, authentication age, support delegation, and an explicitly approved reason. Unknown operations default to deny.

### Constrain queries before materialization

Collection authorization is not “load everything, then filter the response.” The repository query must include tenant and relationship constraints so foreign rows do not enter application memory, counts, pagination boundaries, caches, or timing-sensitive branches. The same principle applies to nested identifiers: a dataset ID must be constrained through its project ownership rather than trusted because the URL also contains a project ID.

Existence concealment is a deliberate response policy. For selected tenant-owned resources, a wrong-owner request can return the same not-found problem as an absent identifier. That choice must be consistent across detail, update, artifact content, list counts, and diagnostic events. Concealment is not achieved if the status matches but latency, ETag, or error extensions reveal the foreign object.

Field-level policy applies in both directions. Input models must not allow a caller to assign `ownerId`, tenant, role, lifecycle state, or server-generated version. Output projection must remove fields the principal is not entitled to see. Serialization models help, but the policy still needs a test that plants a sensitive internal field and proves it cannot cross the boundary.

### Avoid stale decisions

A time-of-check/time-of-use defect occurs when ownership or state changes between the authorization read and the mutation. Prefer one owner-constrained update or a transaction that locks and verifies the relevant version. Caching allow decisions is dangerous unless the cache key includes principal, operation, resource identity and version, tenant, policy revision, and any freshness conditions—and even then invalidation must be explicit.

Support and administrative access should be more constrained, not exempt. Require a named role, explicit operation, reason, stronger assurance, recent authentication, bounded delegation, and an audit event. “Admin bypass” is not a policy because it erases resource, action, and incident accountability.

The decisive proof matrix crosses credential validity, scope, role, tenant, ownership, state, assurance, and freshness. Include combinations where exactly one dimension is wrong. Happy-path tests with one all-powerful fixture principal do not test authorization.

## Security requirements and standards

The course profile turns the mental model into enforceable requirements. `MUST` denotes a non-compensable course invariant; `SHOULD` requires a recorded exception.

1. The implementation MUST satisfy **Policy decision point**: A deterministic service evaluates policy inputs and returns allow/deny plus reason and obligations.
2. The implementation MUST satisfy **Policy enforcement point**: The transport or application boundary refuses to execute unless a valid allow decision applies to the exact action and resource.
3. The implementation MUST satisfy **Default deny**: Missing policy, unknown operation, absent attribute, or evaluation error denies rather than falls through.
4. The implementation MUST satisfy **Tenant isolation**: Tenant membership constrains all collection and object queries before data leaves persistence.
5. The implementation MUST satisfy **Relationship authorization**: Owner, project member, support delegate, or administrator relationships are explicit and time-bounded.
6. The implementation MUST satisfy **Field policy**: Allowed input fields and output projections can vary by principal and operation.
7. The implementation MUST satisfy **Concealment**: For selected foreign resources, return the same not-found behavior as absent resources to avoid existence disclosure.
8. The implementation MUST satisfy **TOCTOU resistance**: Authorization facts used for mutation must remain valid at the durable decision point or be rechecked atomically.

## Worked attacks and defenses

The Authorization and Policy Enforcement cases are bounded course fixtures. Trace the attacker-controlled value through every interpreter, then identify the policy decision and smallest rejection evidence; do not target external systems.

### Attack 1 — BOLA/ID substitution

A caller changes a path identifier to a resource owned by another tenant.

### Attack 2 — Collection leak

Object reads are protected, but list queries omit tenant predicates and reveal foreign metadata.

### Attack 3 — Scope-only admin

A token with broad scope reaches an administrative endpoint without role or assurance checks.

### Attack 4 — Mass assignment

A writer supplies server-owned fields such as `ownerId`, `tenantId`, or `status`.

### Attack 5 — Stale support delegation

A previously valid support session remains accepted after expiry or revocation.

### Attack 6 — Authorization after effect

A file or database mutation occurs before resource ownership is checked.

## Python implementation

Represent `Principal`, `Action`, `ResourceFacts`, and `Decision` as immutable types. Policies return structured denial reasons for audit but adapters translate them to the frozen public problem behavior. Repository methods accept tenant/principal constraints rather than loading globally then filtering in Python.

## TypeScript implementation

Use discriminated action types and exhaustive policy switches. Avoid optional booleans such as `isAdmin?: boolean`; model named roles and obligations. Build SQL/query filters from verified policy context, not client-supplied tenant values.

## Failure patterns

For each pattern, explain why it can look reasonable, construct the smallest counterexample, and identify the missing authoritative boundary.

### 1. Checking scope but not resource ownership.


### 2. Protecting detail endpoints while leaking list and count results.


### 3. Loading a foreign object to decide concealment and then exposing timing or metadata.


### 4. Putting policy in UI or generated documentation only.


### 5. Caching allow decisions without resource version, tenant, or policy revision.


### 6. Letting an unknown operation default to a low-privilege policy.

## What you add to the capstone

### Objective

Implement the full API 1.2 policy matrix and run cross-tenant object, list, mutation, artifact, and support-context tests. Plant one missing owner predicate in artifact retrieval and prove the shared attack vector detects it.

## Representative implementation

These are the smallest useful entry points for **Authorization and Policy Enforcement**.

### Python — `capstone/tracks/python-fastapi/src/api_security/authorization.py`

```python


@dataclass(frozen=True, slots=True)
class Policy:
    operation_id: str
    scopes: frozenset[str] = frozenset()
    roles: frozenset[str] = frozenset()
    relationship: str = "none"
    tenant_bound: bool = True
    conceal: bool = False
    required_assurance: str = "baseline"
    max_auth_age_seconds: int | None = None


def _relationship_allowed(name: str, principal: Principal, resource: ResourceFacts) -> bool:
    if name in {"none", "tenant-query", "tenant-create"}:
        return True
    if name == "owner":
        return resource.owner == principal.subject
    if name in {"owner-or-member", "project-member", "project-member-and-dataset", "project-member-completed-run"}:
        return resource.owner == principal.subject or principal.subject in resource.members
    if name in {"project-owner-or-writer", "project-owner", "tenant-owner"}:
        return resource.owner == principal.subject or "tenant-admin" in principal.roles
    if name == "project-owner-or-run-creator":
        return resource.owner == principal.subject or resource.creator == principal.subject or "tenant-admin" in principal.roles
    if name == "fresh-high-assurance":
        return "operator" in principal.roles
    return False


def authorize(
    operation_id: str,
    *,
    principal: Principal | None,
    resource: ResourceFacts,
    policies: Mapping[str, Policy],
) -> Decision:
    policy = policies.get(operation_id)
    if policy is None:
        return Decision(False, "policy.missing")
    if operation_id == "getHealth" and principal is None:
        return Decision(True, "policy.public")
    if principal is None:
        return Decision(False, "credential.required", policy.conceal)
    if not policy.scopes.issubset(principal.scopes):
        return Decision(False, "scope.insufficient", policy.conceal)
    if policy.roles and not policy.roles.intersection(principal.roles):
        return Decision(False, "role.insufficient", policy.conceal)
    if policy.tenant_bound and resource.tenant is not None and resource.tenant != principal.tenant:
        return Decision(False, "tenant.foreign", policy.conceal)
    if not _relationship_allowed(policy.relationship, principal, resource):
        return Decision(False, "relationship.denied", policy.conceal)
    if policy.required_assurance == "high" and principal.assurance != "high":
        return Decision(False, "assurance.insufficient", policy.conceal)
    if policy.max_auth_age_seconds is not None and principal.auth_age_seconds > policy.max_auth_age_seconds:
        return Decision(False, "authentication.stale", policy.conceal, ("step-up",))
    return Decision(True, "policy.allow", obligations=("audit",))
```

### TypeScript — `capstone/tracks/typescript-fastify/src/security/authorization.ts`

```typescript
import type { Decision, Principal, ResourceFacts } from "./models.js";

export interface Policy { readonly operationId: string; readonly scopes: ReadonlySet<string>; readonly roles: ReadonlySet<string>; readonly relationship: string; readonly tenantBound: boolean; readonly conceal: boolean; readonly requiredAssurance: string; readonly maxAuthAgeSeconds?: number }

function relationshipAllowed(name: string, principal: Principal, resource: ResourceFacts): boolean {
  if (["none", "tenant-query", "tenant-create"].includes(name)) return true;
  if (name === "owner") return resource.owner === principal.subject;
  if (["owner-or-member", "project-member", "project-member-and-dataset", "project-member-completed-run"].includes(name)) return resource.owner === principal.subject || resource.members.has(principal.subject);
  if (["project-owner-or-writer", "project-owner", "tenant-owner"].includes(name)) return resource.owner === principal.subject || principal.roles.has("tenant-admin");
  if (name === "project-owner-or-run-creator") return resource.owner === principal.subject || resource.creator === principal.subject || principal.roles.has("tenant-admin");
  if (name === "fresh-high-assurance") return principal.roles.has("operator");
  return false;
}

export function authorize(operationId: string, principal: Principal | undefined, resource: ResourceFacts, policies: ReadonlyMap<string, Policy>): Decision {
  const policy = policies.get(operationId);
  if (policy === undefined) return { allowed: false, reason: "policy.missing", conceal: false, obligations: [] };
  if (operationId === "getHealth" && principal === undefined) return { allowed: true, reason: "policy.public", conceal: false, obligations: [] };
  if (principal === undefined) return { allowed: false, reason: "credential.required", conceal: policy.conceal, obligations: [] };
  if (![...policy.scopes].every((scope) => principal.scopes.has(scope))) return { allowed: false, reason: "scope.insufficient", conceal: policy.conceal, obligations: [] };
  if (policy.roles.size > 0 && ![...policy.roles].some((role) => principal.roles.has(role))) return { allowed: false, reason: "role.insufficient", conceal: policy.conceal, obligations: [] };
  if (policy.tenantBound && resource.tenant !== undefined && resource.tenant !== principal.tenant) return { allowed: false, reason: "tenant.foreign", conceal: policy.conceal, obligations: [] };
  if (!relationshipAllowed(policy.relationship, principal, resource)) return { allowed: false, reason: "relationship.denied", conceal: policy.conceal, obligations: [] };
  if (policy.requiredAssurance === "high" && principal.assurance !== "high") return { allowed: false, reason: "assurance.insufficient", conceal: policy.conceal, obligations: [] };
  if (policy.maxAuthAgeSeconds !== undefined && principal.authAgeSeconds > policy.maxAuthAgeSeconds) return { allowed: false, reason: "authentication.stale", conceal: policy.conceal, obligations: ["step-up"] };
  return { allowed: true, reason: "policy.allow", conceal: false, obligations: ["audit"] };
}
```

Compare the two tracks by this invariant: **scope, role, tenant, relationship, assurance, freshness, and concealment are evaluated for the exact operation and resource**. The intended implementation difference is: policy representation differs; an unknown operation and a cross-owner request must both deny.

## Module synthesis

You are ready to leave this module when you can **Separate authentication from authorization, Model operation policy explicitly, and Constrain collection queries before loading data** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Remove or bypass the central control and prove the predicted oracle fails** and requiring the following oracle: **Separate authentication from authorization; Model operation policy explicitly; Constrain collection queries before loading data; Apply field-level input and output policy.**

The cumulative platform now includes **Build explicit authorization decisions for collections, individual resources, fields, support access, and administration**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Hostile Input and File Handling](../module-05-hostile-input-and-file-handling/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
