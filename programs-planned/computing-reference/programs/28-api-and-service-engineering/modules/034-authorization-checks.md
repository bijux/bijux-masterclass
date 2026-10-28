---
module_id: API-034
program: API & Service Engineering
level: 1
module_number: 34
title: Authorization Checks
status: complete
last_verified: 2026-09-01
---

# Authorization Checks

## One-Page Review

### Governing question

How should an API decide and enforce whether an authenticated actor may perform one action on one resource, relationship, field set, and current state without leaking hidden objects or racing the effect it protects?

### Essential definitions

- **authorization** evaluates whether a subject may perform an action on an object under policy and context.
- A **policy decision point** evaluates authorization; a **policy enforcement point** prevents the operation unless the decision permits it.
- **object-level authorization** binds the decision to the exact resource selected by caller-controlled identity.
- **function-level authorization** controls access to an operation or administrative capability.
- **field-level authorization** governs which input fields may be set and which output fields may be observed.
- **relationship-based authorization** derives access from relationships such as owner, member, parent, delegate, or group.
- **concealment** deliberately makes an inaccessible object observationally similar to an absent object.
- **indeterminate** means the decision cannot be established safely because evidence or policy evaluation failed.

### Central model, mechanism, or theorem

Model a decision as:

$$
D_P(s,a,o,e,t)\in\{\text{permit},\text{deny},\text{indeterminate}\},
$$

where policy $P$ evaluates subject/context $s$, action $a$, object and relationships $o$, environmental facts $e$, and evaluation time/version $t$. The enforcement invariant is that effect $E$ occurs only if a current permit covers the same action, object, tenant, fields, and state used by $E$. Authentication, route access, possession of an opaque ID, or schema validity never substitutes for this decision.

### Critical invariants

Default is deny. Every externally supplied object identifier triggers an object-level check. Tenant and parent scope are part of object identity. Function permission and object permission are both required where applicable. Writes allowlist fields before mutation; reads project fields after authorization. Collection filtering uses the same policy as individual reads and does not leak hidden counts. Checks and effects share a consistency boundary or guarded precondition. Downstream and asynchronous execution re-establish authorization appropriate to execution time. Policy errors are not permits. Denial responses, timing, caches, logs, and audit obey disclosure policy.

### Common failures

Checking only that the caller is authenticated; trusting an unguessable UUID; authorizing a route but not its object; loading by ID without tenant scope; comparing one token user ID to one request field; allowing administrators by URL naming; mass assigning forbidden fields; filtering results after pagination/counting; checking parent but not child; authorizing before a state change then acting on newer state; caching permits beyond revocation; treating policy-engine outage as allow; forwarding a permit decision to another audience; and returning different errors that enumerate concealed resources.

### Compact example

`DELETE /tenants/t-1/orders/o-9` arrives from authenticated buyer `u-7`. The service verifies tenant membership, loads `o-9` within `t-1`, checks `order.delete` on that exact object and current state, and requires the expected version. It commits deletion only while the authorized version remains current. For absent, wrong-tenant, or concealed objects it returns the same public `404`; audit retains safe internal distinctions. **Conclusion:** permission is bound to the exact effect, not merely the route or identity.

### Connections

[Authentication Context Propagation](033-authentication-context-propagation.md) supplies verified identity evidence. [Transport, Application, and Domain Boundaries](031-transport-application-and-domain-boundaries.md) places enforcement around the use case. [Error Translation](../ROADMAP.md) next maps denial and concealment safely; later modules on object-level authorization, overposting, and enumeration deepen attack-specific cases.

## Governing Question

Which authorization model, data retrieval pattern, consistency rule, enforcement placement, field projection, and disclosure behavior makes every API operation least-privileged and resistant to object, function, tenant, relationship, and timing bypasses?

## Why This Matters

Authentication answers who or what presented acceptable evidence. It does not say which order that principal may see, whether a support agent may refund it, whether a workload may act for the user, or which fields may appear. APIs expose object identifiers repeatedly in paths, queries, headers, and bodies, so attackers can substitute identifiers at high speed. OWASP's API Security Top 10 2023 identifies broken object-level authorization as its first risk category.

Authorization bugs survive apparently sound controls. UUIDs make guessing harder but are not permissions. OAuth scopes can permit the `orders:read` function without granting every order. A repository query scoped to tenant can still expose another member's private object. A correct decision can become stale before a mutation commits. A filtered list can hide rows yet leak their count.

Authorization must therefore be modeled as a decision about subject, action, exact resource, relationships, fields, state, environment, and time. Enforcement must protect the actual observation or effect. The public response must also implement disclosure policy: even a denied operation can leak object existence, tenant membership, workflow state, or sensitive field names.

## Prerequisites and Retrieval

Retrieve authenticated principal, client, workload, tenant, delegation, and assurance context; API resource and operation semantics; domain ownership and lifecycle; request and response field ownership; least privilege, fail-safe defaults, RBAC, ABAC, ACLs, and relationship models; HTTP `401`, `403`, and concealment with `404`; database transactions and concurrency; caching; bulk and asynchronous operations; audit; and threat modeling.

Before implementing a check, retrieve the action vocabulary, exact object identity and tenant, subject and workload identities, relevant relationships and attributes, field set, current state, policy version, consistency requirement, disclosure policy, failure behavior, cache/revocation bounds, audit purpose, and human break-glass process.

## Learning Objectives

By the end of this module, you should be able to:

1. separate authentication, function, object, relationship, field, and state authorization;
2. model authorization decisions with explicit subject, action, resource, environment, and policy;
3. place enforcement so a permit protects the exact read or effect;
4. design authorized collections, expansions, bulk operations, and asynchronous work;
5. preserve concealment across errors, timing, caches, totals, and logs;
6. handle policy consistency, caching, outages, and revocation safely; and
7. test denial, bypass, race, and cross-tenant cases systematically.

## Core Exposition

### Name the authorization tuple

Every check should make these inputs explicit:

- **subject:** issuer-scoped principal, client, workload, and delegation chain;
- **action:** a domain/API verb such as `order.read`, `order.cancel`, or `refund.approve`;
- **object:** exact type, stable ID, tenant, parent, owner, classification, and current state;
- **environment:** time, network/channel assurance, purpose, device or risk facts where governed; and
- **policy:** versioned rules and relationship data used for the decision.

Avoid generic `canAccess(user, object)`. Read, update, delete, share, approve, export, and administer have different risk. An action name should remain stable across routes that implement the same capability, while still distinguishing materially different effects.

Authorization result needs at least permit, deny, and indeterminate. Indeterminate covers policy-engine timeout, missing required attributes, stale relationship evidence beyond policy, or evaluation error. Under fail-safe defaults, indeterminate does not become permit. The public API may group deny and indeterminate, but operations and incident response need the distinction.

### Enforce function and object permission

Function-level policy determines whether the actor may attempt a capability at all. Object-level policy determines whether it may act on this instance. Both can be necessary.

An `orders:cancel` scope might allow the endpoint, while ownership or tenant relationship selects which orders. An administrator role might expose an administrative function, while region, separation-of-duty, or case assignment restricts objects. Checking only one side creates a bypass.

Do not infer function permission from HTTP method or route naming. `DELETE /users/{id}` is not safe because it sits under `/admin`. Route registration, documentation visibility, and UI hiding are not enforcement.

Put a coarse function check early when it cheaply rejects impossible calls, then run exact object and state checks after safe loading. Keep one authoritative policy so coarse and exact checks cannot contradict silently.

### Treat every caller-controlled identifier as a target

Object IDs appear beyond path parameters:

- body references and foreign keys;
- query filters and cursor contents;
- parent IDs in nested routes;
- file, attachment, and image keys;
- webhook and callback registrations;
- batch item IDs;
- export selections;
- GraphQL node IDs; and
- relationship expansion parameters.

Each can select protected data or cause an effect. Validate shape first, then bind the exact resolved object to the actor and action. Do not authorize the path order but trust a different body `paymentId` or callback owner.

Opaque random identifiers reduce enumeration efficiency and accidental collision; they do not establish permission. Assume an identifier can leak through logs, links, browser history, screenshots, events, referrers, or another authorized user.

### Bind tenant into identity and lookup

In multi-tenant systems, `object_id` alone may not uniquely or safely identify the target. Use a compound identity or tenant-scoped repository operation such as `find_visible_order(tenant, order_id, subject)` where appropriate.

Verified tenant context and requested path tenant must agree under policy. Never let a body tenant override authentication context. Database row-level policy or tenant predicates can provide defense in depth, but application semantics still own the action and disclosure decision.

Scope caches, idempotency records, cursors, background jobs, and authorization decisions by tenant. A cache keyed only by `order_id` can replay one tenant's result or permit into another context.

Tenant administrators are not automatically global administrators, and workload identity does not automatically inherit every tenant. Model delegated administrative boundaries explicitly.

### Choose an authorization model by policy shape

**Role-based access control (RBAC)** assigns permissions to roles and subjects to roles. It fits stable job functions but can explode into roles for every object and exception.

**Attribute-based access control (ABAC)** evaluates subject, object, action, and environment attributes against policy. NIST SP 800-162 frames ABAC in these terms. It expresses classification, region, time, assurance, or purpose, but attribute provenance and freshness are critical.

**Access-control lists (ACLs)** attach principals or groups to object permissions. They are intuitive for sharing but can be costly to traverse and govern at scale.

**Relationship-based access control (ReBAC)** derives permission from graph relationships such as member-of, owns, parent-of, or shared-with. It supports nested groups and resource hierarchies but introduces graph consistency, cycles, depth, and latency concerns.

**Capability-based authority** uses an unforgeable, intentionally delegated capability to represent permission. A signed URL can be a bounded capability, not merely an identifier, if its scope, expiry, audience, action, and replay properties are designed correctly.

Most APIs combine models: role permits support work; relationship binds a case; attributes require region and assurance; object state forbids a transition. Make conjunction and precedence explicit rather than scattering `if` statements.

### Separate policy decision and enforcement

A policy decision point (PDP) evaluates policy. A policy enforcement point (PEP) prevents reads or effects without a permit. They may be in one process or separate services.

The application use case is usually the primary PEP because it knows action, object, transaction, and outcome. Gateways can enforce coarse audience, scope, and route policy but lack current object relationships and state. Database row-level security can enforce tenant and row visibility but may not know domain action or downstream effects.

Use layered enforcement as defense in depth with one semantic owner. Do not assume several partial checks compose safely. Document which layer is authoritative and test discrepancies.

A remote PDP centralizes policy and relationship evaluation. Its request must contain authenticated subject/workload, exact action/object, attributes with provenance, policy version or consistency requirement, and a correlation identity. Protect the PDP channel and treat its result as sensitive. The PDP does not perform the effect; the PEP still binds decision to it.

### Place the check near the effect

Authorization too early can become a time-of-check/time-of-use bug. Suppose an order is editable only while assigned to team A. The service checks assignment, another transaction reassigns it, and the first request updates afterward.

Bind check and effect through one of:

- transaction isolation over relationship and object state;
- optimistic version/precondition checked at write;
- database statement whose predicate encodes authorized scope and current state;
- authorization snapshot/consistency token respected by the data write; or
- durable workflow that rechecks at execution.

Do not hold a remote authorization call and database transaction open blindly; latency can increase contention. Instead retrieve a policy decision with a freshness/consistency contract, then guard the write with the exact object version and policy-relevant facts. If they changed, re-evaluate or return a conflict/precondition outcome.

For destructive or financial effects, authorize every stage that can independently commit an effect. A preflight endpoint does not authorize the later execution request.

### Secure reads before projection

Load only data needed to decide safely, then authorize, then construct an allowed representation. Avoid loading a full secret-rich aggregate into generic serialization before field policy.

Field-level read policy can depend on subject, action, object, purpose, and state. A support agent may see shipping address but not payment instrument; an owner may see their own email; a public viewer sees neither.

Define named projections rather than deleting fields ad hoc from a generic map. Nested relationships and expansions require authorization at every edge. A parent permit does not imply every child, attachment, audit log, or linked user is visible.

Redaction can itself reveal that a field exists. Decide whether to omit, return null, provide a state marker, or reject the requested projection. Keep the rule consistent with schema and caching.

### Authorize writes before mapping effects

Request schema validity does not make every field writable. Maintain an allowlist per action and actor context. Reject or deliberately ignore unauthorized fields under the contract before they reach domain or persistence models.

Separate permissions such as `profile.update_own`, `profile.update_role`, and `profile.verify_email`. A generic `profile.update` plus mass assignment invites privilege escalation. Read permission does not imply write permission, and create permission does not imply control over server-derived owner, tenant, status, totals, or audit fields.

For patch documents, inspect every targeted path or operation. JSON Patch can touch deeply nested or array-selected data; JSON Merge Patch can use null to remove. Authorize the resulting intended transition, not only top-level field names.

After domain policy computes effects, ensure no authorized input creates an unauthorized indirect effect—for example, changing a parent relationship to gain access to children.

### Build authorized collections correctly

Collection authorization is not “query all, then remove forbidden rows” when pagination, limits, counts, timing, or cost expose the hidden set. Integrate visibility into selection or use an authorization-aware index.

Let business membership be $M(o)$ and visibility policy be $V(s,a,o)$. The authorized set is:

$$
R_s=\{o\mid M(o)\land V(s,a,o)=\text{permit}\}.
$$

Filtering, sorting, pagination, totals, facets, and aggregations operate over $R_s$, not the unfiltered set. Otherwise a page can contain fewer items, a total can reveal hidden membership, or a cursor can encode a secret object.

Be cautious with centralized per-object checks after a broad database query; it can create N+1 latency and denial-of-service risk. Push safely expressible predicates into the data layer, precompute authorized indexes, batch PDP checks, or use relationship-aware lookup. Verify equivalence with the authoritative policy.

Search, autocomplete, export, analytics, and existence endpoints need the same visibility policy as individual GET. A `HEAD`, count, timing difference, or validation suggestion can enumerate objects without returning their bodies.

### Protect parent-child and graph relationships

Nested URI `/projects/p/files/f` asserts a relationship that must be verified, not inferred from path syntax. Load `f` under parent `p` and authorized tenant; do not load `f` globally after authorizing only `p`.

Inherited permission needs clear semantics: does folder access include all descendants, future children, shared links, deleted objects, and audit history? Relationship graphs need cycle handling, maximum depth, consistency, and revocation behavior.

Zanzibar's published design demonstrates relationship-based permission checks with consistency requirements across access-control and object changes. Its production scale numbers are evidence for that system, not a guarantee for every Zanzibar-inspired implementation.

When a relationship changes, cached permits and derived memberships must not authorize a later read against newer object state. Carry a consistency token or invalidate/recheck under a defined staleness bound.

### Handle concealment deliberately

RFC 9110 permits an origin server to hide the existence of a forbidden target by responding `404` instead of `403`. Decide per resource and threat model.

Concealment requires more than status equality. Align body type and size where practical, cache behavior, headers, validation precedence, links, timing, logs visible to callers, list totals, and side channels. Do not return “invalid state” for a hidden object or validate a secret child field before checking visibility.

`401` concerns missing or invalid authentication and normally carries a challenge. `403` means the server understood the authenticated request but refuses it. Concealed `404` intentionally avoids acknowledging the target. Use stable internal categories for operations while preserving the public equivalence.

Absolute timing equality is rarely possible, but avoid obvious distinctions such as remote policy calls only for existing objects. Threat-model high-risk enumeration and add uniform lookup patterns, bounded jitter only if justified, and rate/abuse controls.

### Handle bulk and batch operations per item

A bulk request containing 100 object IDs requires authorization for each exact action/object pair. A permit for the batch endpoint is insufficient. Validate limits first, then evaluate items under consistent policy and tenant scope.

Choose atomicity and disclosure. All-or-nothing can reject the whole batch without identifying hidden items. Per-item results improve correction but can enumerate existence. A safe contract may report only submitted client reference plus generic denied/not-processed classification.

Do not partially execute before all required authorization checks if the contract promises atomicity. If policy can change during long execution, bind a snapshot or recheck at each effect. Count and rate-limit authorization graph work as part of request cost.

### Reauthorize asynchronous and downstream work

An accepted job can execute after roles, relationships, object state, or policy change. Decide whether acceptance snapshots authority or execution requires current authority. Store the original subject, workload, tenant, action, object, delegation/impersonation facts, decision/policy version, and revocation/cancellation controls—never only `authorized=true`.

For high-risk work, re-evaluate before each irreversible effect. For a durable legally binding acceptance, snapshot authority may be correct, but the policy must define it and audit the evidence. A worker's service role cannot silently replace user authorization.

Downstream services enforce their own action/object policy from audience-bound authentication context. An upstream “permit” header is not universal authority. If a central decision is propagated, bind it cryptographically or through an authenticated channel to receiver, action, object, subject, policy, expiry, and one use where needed.

### Cache decisions with all dependencies

Authorization caching trades latency for revocation and staleness. A correct cache key can include subject and delegator, workload/client, action, object and tenant, object/policy/relationship version, relevant environment, and requested fields.

Caching `canRead(user, order)` without membership version can retain access after removal. Caching a role result can cross tenant or impersonation mode. Negative caching can delay newly granted access.

Choose TTL below the acceptable revocation window, invalidate from policy/relationship changes, or use consistency tokens. Never cache beyond authentication context expiry. Sensitive actions may require fresh evaluation.

Local caches must not turn PDP outage into indefinite permits. A still-valid cached permit may be usable only under an explicit availability policy and bounded freshness; otherwise return indeterminate/fail closed.

### Use decision obligations carefully

A PDP may return obligations such as required redaction, step-up authentication, justification, watermark, maximum amount, or audit category. Treat these as part of the permit. If the PEP cannot satisfy an obligation, it must not execute.

Keep obligations typed and versioned. Free-form policy strings are hard to enforce safely. The application verifies that all mandatory obligations are recognized and applied before effect or serialization.

Avoid making policy evaluation mutate application state. Decision should be deterministic for its declared inputs where possible; audit is a separate reliable effect. If approval consumption or one-time capability use is stateful, model it as an atomic authorization/effect transaction or a governed capability redemption.

### Fail closed without making the system unusable

Policy parse errors, missing attributes, relationship-service timeouts, stale evidence beyond bounds, unknown action, and unsupported obligation yield indeterminate or deny—not permit.

Differentiate outage from ordinary denial internally. A public `503` can be appropriate when policy infrastructure is unavailable and concealment permits revealing a temporary service problem; some operations may use a generic denial. Define this contract and retry behavior rather than returning random `403` or `500` responses.

Break-glass access is a separate high-assurance policy: named eligible actors, strong authentication, narrow scope, reason, approval or alert, short expiry, immutable audit, and retrospective review. It is not a code path that disables checks during incidents.

The executable decision model below checks function, tenant, relationship, field, and state conditions. It is not a policy engine, database consistency proof, or authorization system.

<!-- bijux-verify: {"id":"authorization-decision-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"owner_read=permit\nother_read=deny:relationship\ncross_tenant=deny:tenant\nforbidden_field=deny:field\nclosed_order=deny:state\nmissing_policy=indeterminate:policy\n","stderr":""}} -->
```python
def decide(subject, action, order, fields, policy_available=True):
    if not policy_available:
        return "indeterminate:policy"
    if action not in subject["actions"]:
        return "deny:function"
    if subject["tenant"] != order["tenant"]:
        return "deny:tenant"
    if subject["id"] != order["owner"]:
        return "deny:relationship"
    if not set(fields) <= subject["writable_fields"]:
        return "deny:field"
    if action == "order.update" and order["state"] != "open":
        return "deny:state"
    return "permit"

buyer = {
    "id": "u-7", "tenant": "t-1", "actions": {"order.read", "order.update"},
    "writable_fields": {"note"},
}
base = {"tenant": "t-1", "owner": "u-7", "state": "open"}
cases = {
    "owner_read": (buyer, "order.read", base, [], True),
    "other_read": (buyer, "order.read", {**base, "owner": "u-8"}, [], True),
    "cross_tenant": (buyer, "order.read", {**base, "tenant": "t-2"}, [], True),
    "forbidden_field": (buyer, "order.update", base, ["status"], True),
    "closed_order": (buyer, "order.update", {**base, "state": "closed"}, ["note"], True),
    "missing_policy": (buyer, "order.read", base, [], False),
}
for name, arguments in cases.items():
    print(f"{name}={decide(*arguments)}")
```

The example gives one deterministic order for checks. A real API may conceal relationship and tenant denial identically and must bind a permit to the version actually read or changed.

### Audit without leaking

Record subject and effective actor identifiers, workload/client, action, object reference under access controls, tenant, decision, policy/version, obligations, reason category, request identity, and effect outcome. Avoid tokens, full personal claims, secret fields, or caller-visible logs.

Denial audit can itself be abused at high volume; rate-limit and aggregate safely while retaining incident value. Audit stores need tamper resistance, retention, access review, and searchable correlation.

Decision logs prove that a component recorded a result, not that policy was correct or enforcement occurred. Link decision to transaction/effect identity and test that denied/indeterminate paths cannot commit.

### Test the negative space

For every endpoint, test anonymous, wrong issuer/audience, correct identity without function permission, wrong tenant, same tenant wrong owner, missing/changed relationship, forbidden field, wrong object state, stale policy, PDP failure, and concealed absence.

Replace every caller-controlled ID with another authorized user's ID. Test nested IDs independently. Test lists, counts, filters, search, export, expansion, batch items, files, callbacks, and background execution—not only individual GET.

Property-based tests can assert that non-permitted inputs produce no effect and no restricted field. Mutation tests remove or invert policy predicates to ensure tests fail. Differential tests compare pushed-down database filters and batch decisions with the reference evaluator.

Concurrency tests change membership, ownership, state, and policy between check and write. Verify revocation bounds and cache keys. Operational tests fail the PDP, key stores, and relationship service. Human review checks that policy matches domain intent and cannot be bypassed through another operation.

## Definitions and Notation

Let authorization request $q=(s,a,o,e,t)$ contain subject/context $s$, action $a$, object and relationships $o$, environment $e$, and evaluation time/version $t$. Decision $D_P(q)$ is permit, deny, or indeterminate under policy $P$.

Let requested effect $E(q,v)$ operate on object version $v$. Enforcement requires a permit whose decision inputs identify the same subject, action, object, tenant, relevant fields, relationships, and state version—or a consistency rule proving equivalence at effect time.

Let business collection predicate be $M(o)$ and authorization visibility be $V(s,a,o)$. Authorized result set is $R_s=\{o\mid M(o)\land V(s,a,o)=permit\}$, and pagination/counting operate on $R_s$.

An **obligation** is a mandatory condition accompanying permit. A **policy information point** supplies attributes or relationships. A **decision cache** stores results under declared dependencies and freshness. A **revocation window** bounds how long removed authority can remain effective. **TOCTOU** is a time-of-check/time-of-use gap in which decision inputs change before effect.

## Mechanisms, Invariants, or Proof Structure

1. Define stable actions and exact object/tenant identities.
2. Construct verified subject, client, workload, delegation, and tenant context.
3. Apply coarse function policy without treating it as object permission.
4. Resolve the target under safe tenant and parent scope.
5. Evaluate object, relationship, field, state, environment, and policy inputs.
6. Treat deny and indeterminate as no permit and satisfy all obligations.
7. Bind permit to the exact read projection or guarded effect.
8. Apply identical visibility to collections, totals, expansions, and batch items.
9. Re-establish authorization for downstream and asynchronous execution.
10. Audit and test negative, concealed, stale, concurrent, and failure cases.

The key safety property is non-bypass: every protected observation or effect has a permit covering its exact semantic inputs, and every non-permit path produces no protected effect. Evidence for selected tests and models does not prove arbitrary policy correctness.

## Alternatives and Trade-Offs

Embedded policy is low latency and close to domain code but can drift across services. A centralized PDP improves consistency and audit but adds network, availability, and version dependencies. Keep policy ownership clear and use local enforcement either way.

RBAC is understandable for stable functions but weak for instance sharing. ABAC expresses rich conditions but depends on attribute provenance. ACL/ReBAC maps sharing directly but requires graph consistency and scale controls. Combine only with explicit precedence and vocabulary.

Filtering in database queries is efficient and avoids hidden-row leakage. A separate PDP can express richer policy but may require batching or authorized indexes. Push down only predicates whose equivalence is verified; keep the reference decision authoritative.

Fresh checks minimize revoked access but add latency and dependency load. Cached permits improve availability but extend authority. Choose sensitivity-specific revocation windows, consistency tokens, and cache keys.

`403` is diagnostically clear for known resources. Concealed `404` reduces enumeration but complicates support and testing. Choose by resource threat model and maintain safe internal diagnostics.

Snapshot authorization makes accepted jobs predictable. Execution-time rechecks honor revocation and state change. Hybrid policies can snapshot low-risk authority while rechecking high-risk effects, but the user-facing contract must be explicit.

## Failure Modes and Misconceptions

- **“Authenticated means authorized.”** Identity evidence does not grant an action on an object.
- **“A scope grants every resource.”** Scope is usually coarse function evidence and needs object policy.
- **“UUIDs prevent object attacks.”** Leaked or obtained IDs remain usable without authorization checks.
- **“Tenant filtering is enough.”** Same-tenant ownership, relationship, field, and state rules can still deny.
- **“The route is admin-only.”** UI and route names are not enforcement.
- **“Read permission implies write permission.”** Actions and fields have different authority.
- **“Parent access implies all children.”** Inheritance must be defined and verified at each relationship.
- **“Filter after fetching.”** Counts, pagination, timing, and cost can leak hidden objects.
- **“A permit remains valid for the request.”** Policy-relevant state can change before the effect.
- **“Policy timeout should fail open for availability.”** Indeterminate is not permit.
- **“The gateway handles authorization.”** Gateways usually lack exact object and state semantics.
- **“Database row policy handles everything.”** It may protect rows but not actions, downstream effects, or fields.
- **“Cache by user and object.”** Action, tenant, fields, policy, relationships, context, and versions can matter.
- **“A worker's service role covers the user.”** Asynchronous effects need explicit delegated or durable authority.
- **“Decision logs prove enforcement.”** Link permits and denials to actual read/effect postconditions.

## Worked Examples

### Example 1

**Situation:** Buyer changes `/orders/o-7` to `/orders/o-8`, another buyer's UUID. **Reasoning:** Route scope and authentication pass, but object relationship fails. Load under tenant and evaluate `order.read` on `o-8`; return concealed denial. **Conclusion:** every caller-controlled object ID needs an exact check.

### Example 2

**Situation:** Tenant administrator calls global user-deletion endpoint. **Reasoning:** Admin role is tenant-scoped; require function permission plus target tenant relationship and forbid global action. **Conclusion:** role names do not erase scope.

### Example 3

**Situation:** Profile patch includes allowed `displayName` and forbidden `role`. **Reasoning:** Validate every patch path, reject the field before mapping, and do not rely on ignoring unknown input. **Conclusion:** field-level write policy prevents mass assignment.

### Example 4

**Situation:** List query fetches 20 rows, removes 7 hidden rows, and returns `total=83`. **Reasoning:** Both short page and total reveal hidden membership. Apply visibility before pagination and compute only authorized totals. **Conclusion:** collection authorization defines the result set.

### Example 5

**Situation:** Service authorizes update while user owns a document, then ownership transfers before write. **Reasoning:** Guard write with object/relationship version or re-evaluate under one consistency boundary. **Conclusion:** a correct stale permit can still enable an unauthorized effect.

### Example 6

**Situation:** Caller can see folder but not one confidential file under it. **Reasoning:** Verify file-parent relationship and file visibility independently; do not inherit broadly from route nesting. **Conclusion:** authorization applies at every expanded graph edge.

### Example 7

**Situation:** PDP times out and middleware defaults to allow for premium customers. **Reasoning:** Availability tier is not evidence of permission. Return indeterminate/no effect, use bounded valid cache only if policy permits, and expose safe retry semantics. **Conclusion:** policy failure never manufactures authority.

### Example 8

**Situation:** Revoked group member retains cached access for an hour. **Reasoning:** Cache lacked relationship version and exceeded revocation objective. Add invalidation/consistency token and a bounded TTL below policy tolerance. **Conclusion:** authorization cache design is part of revocation semantics.

### Example 9

**Situation:** A batch delete returns `404` for absent IDs and `403` for hidden IDs. **Reasoning:** Per-item detail enumerates resources. Use a disclosure-safe generic item outcome or reject atomically while keeping internal audit distinctions. **Conclusion:** bulk result design must preserve concealment.

### Example 10

**Situation:** Refund job executes after support agent loses case assignment. **Reasoning:** The job cannot rely on stored `authorized=true`. Recheck current assignment and object state before irreversible payment, or document and audit a valid snapshot grant. **Conclusion:** asynchronous authority needs explicit time semantics.

## Cross-Program Connections

[Security Engineering](../../25-security-engineering/ROADMAP.md) owns access-control models, least privilege, and broken-access-control threat analysis. [Database Engineering](../../18-database-engineering/ROADMAP.md) supplies row predicates, transactions, and concurrency. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies consistency, caching, and asynchronous failure reasoning. [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies negative, mutation, property, and differential testing. This API module owns enforcement at public operations, objects, fields, collections, and effects.

## References

1. V. Hu et al., [*NIST SP 800-162: Guide to Attribute Based Access Control Definition and Considerations*](https://doi.org/10.6028/NIST.SP.800-162), updated 2 August 2019. Checked 2026-09-01.
2. OWASP Foundation, [*API1:2023 Broken Object Level Authorization*](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/) and [*API5:2023 Broken Function Level Authorization*](https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization/). Checked 2026-09-01.
3. R. Fielding, M. Nottingham, and J. Reschke, [*RFC 9110: HTTP Semantics*](https://www.rfc-editor.org/rfc/rfc9110.html), especially `401`, `403`, and concealment with `404`, June 2022. Checked 2026-09-01.
4. R. Pang et al., [*Zanzibar: Google's Consistent, Global Authorization System*](https://www.usenix.org/conference/atc19/presentation/pang), USENIX ATC 2019, pp. 33–46. Checked 2026-09-01.
5. D. Ferraiolo, R. Sandhu, S. Gavrila, D. Kuhn, and R. Chandramouli, “Proposed NIST Standard for Role-Based Access Control,” *ACM Transactions on Information and System Security*, vol. 4, no. 3, 2001, pp. 224–274.
6. J. Saltzer and M. Schroeder, “The Protection of Information in Computer Systems,” *Proceedings of the IEEE*, vol. 63, no. 9, 1975, pp. 1278–1308, especially complete mediation and fail-safe defaults.

## Exercises

### Exercise 1

For `PATCH /tenants/{tenant}/projects/{project}`, identify function, tenant, object, relationship, field, state, environmental, and disclosure checks.

### Exercise 2

Trace authorization for transferring document ownership under concurrent membership revocation. Define the consistency boundary between decision and effect.

### Exercise 3

Diagnose an API that uses UUIDs, route-level roles, post-query filtering, generic DTO binding, one-hour permit caches, and fail-open PDP middleware. Prioritize repairs.

### Exercise 4

Compare embedded RBAC/ABAC policy, database row policy, and a centralized relationship-based PDP for a multi-tenant collaboration product.

### Exercise 5

Design authorization for an asynchronous bulk export with nested resources, field redaction, exact totals, user delegation, revocation, and concealment.

## Answers to the Exercises

### Answer 1

Require authenticated context and coarse `project.update`; bind verified tenant to the path; load project under that tenant; check subject membership/role and any parent organization relationship; inspect every patch field against actor-specific writable fields; verify project state permits each transition; apply assurance, purpose, or time constraints where policy uses them; and guard the write with expected object/relationship version. Wrong tenant, absent, and concealed project share the public absence outcome. Forbidden fields are rejected without revealing hidden policy beyond the public contract.

### Answer 2

The decision includes current owner, recipient membership, actor permission to transfer, document and relationship versions, tenant, and any separation-of-duty rule. Execute inside a transaction that locks or version-checks document ownership and membership, or carry a consistency token accepted by the write. If membership revokes after evaluation but before commit, the version predicate fails and the service re-evaluates or rejects. Persist transfer and authorization-relevant audit atomically. Remote PDP results alone do not prevent the race unless their consistency token is tied to relationship data used at commit.

### Answer 3

First replace fail-open with deny/indeterminate and stop generic mass assignment because they directly manufacture privilege. Add exact object/tenant checks to every caller-controlled ID and every operation; route roles remain only coarse function checks. Integrate visibility into queries before counts and pagination. Define field-level read/write projections. Replace hour-long under-keyed caches with full dependency keys, relationship/policy version or invalidation, and risk-bounded TTL. UUIDs remain defense against casual guessing, not authorization. Add negative ID-substitution, cross-tenant, outage, and concurrency tests.

### Answer 4

Embedded policy gives low latency and domain proximity but risks drift; use it for stable local action/state rules with shared tests. Database row policy strongly defends tenant and row reads/writes but cannot alone express every function, field, external effect, or workflow. A centralized relationship PDP handles sharing graphs and consistent relationship changes but adds network, cache, and availability concerns. A sound combination makes domain/API policy authoritative, uses the PDP for relationships, database policy for row/tenant defense, and the application use case as enforcement point that binds all permits and obligations to the effect.

### Answer 5

At acceptance, authorize export function, tenant, selected roots, delegation, purpose, and requested field class; validate bounded scope without exposing hidden IDs. Store actor/workload/tenant/action, selection definition, policy and relationship consistency reference, requested projection, job identity, and revocation behavior—not a raw token or Boolean permit. At execution, re-evaluate or honor a documented snapshot, traverse only authorized edges, apply field projection per object, and compute totals over the authorized set. Each chunk and external delivery requires current destination authority. Results reveal generic unavailable items where concealment requires it. Revocation cancels pending work under policy, and audit links decisions to exported artifacts and deletion/expiry.
