---
module_id: API-045
program: API & Service Engineering
level: 1
module_number: 45
title: Scope and Permission Design
status: complete
last_verified: 2026-09-01
---

# Scope and Permission Design

## One-Page Review

### Governing question

How should an API define, grant, encode, communicate, enforce, evolve, and audit scopes and permissions so that access tokens carry the minimum useful authority without pretending coarse grants decide every resource action?

### Essential definitions

- A **scope** is an OAuth string naming requested/granted access under authorization-server and resource-server policy.
- A **permission** is a normalized action or capability that local authorization policy can evaluate.
- An **audience/resource indicator** identifies the resource server where a token may be used; it is distinct from what the token may do.
- A **grant** is the authority approved for a client/subject relationship; a token is one bounded projection of that grant.
- **Effective permissions** are the intersection of requested, client-eligible, actor-authorized, consent/policy-approved, resource-relevant, and current restrictions.
- A **composite scope** expands to a documented set of atomic permissions; a **wildcard** represents an open-ended family and is hazardous when its future expansion is unclear.
- **Rich authorization details** are typed JSON authorization structures (RFC 9396) for transaction/resource/action detail that flat scope strings express poorly.
- **Object-level authorization** checks whether the authenticated context may perform an action on this specific object now; scope alone is insufficient.

### Central model, mechanism, or theorem

For request $q$, client $c$, actor $u$, resource server $r$, grant/consent $g$, and current restrictions $p$, mint only

$$
E=Q(q)\cap C(c)\cap U(u)\cap R(r)\cap G(g)\cap P(p).
$$

The resource server then decides request $x$ on object $o$ in state $s$:

$$
\operatorname{allow}(x,o)=V_{token}\land action(x)\in E\land A(subject,client,tenant,action,o,s,environment).
$$

The first intersection bounds portable token authority; $A$ supplies current object, relationship, state, and environmental policy. Neither substitutes for the other.

### Critical invariants

Each token is audience-restricted to one resource server or a small justified set. Scope names have documented semantics, owners, eligible clients/actors, consent text, risk, and tests. No requested scope bypasses client registration, user authority, or policy. Defaults are minimal and explicit; omission does not mean all access. Composite scopes expand through a versioned governed mapping. New API actions do not silently join existing wildcards or broad write scopes. Tokens do not encode unbounded object identifiers as ad hoc scope strings when rich/local authorization is needed. Machine tokens do not inherit user permissions, and user delegation preserves client identity. The resource server validates audience and token state, maps grants through its owned vocabulary, and performs object/action authorization on every path. Revocation and policy-change staleness are bounded and observable.

### Common failures

Using `read`/`write` globally across unrelated APIs; treating audience as scope; granting every registered scope by default; assuming requested equals granted; defining `admin` or `*` without stable expansion; letting `write` automatically include future destructive actions; packing object IDs into millions of scopes; copying identity-provider groups directly into API permissions; interpreting missing scope as legacy full access; issuing multi-audience bearer tokens; using negative scopes whose conflict order is unclear; checking permissions only at the gateway; treating consent as object authorization; returning all internal permissions in errors; and changing scope meaning without inventory, migration, or token-lifetime analysis.

### Compact example

A web client requests resource `orders-api` with `orders.read orders.cancel orders.refund`. Registration permits read/cancel, the user may read/cancel/refund, consent grants read/cancel, and current tenant policy allows both. The token receives only read/cancel and the `orders-api` audience. When cancelling order 7, the API still checks tenant membership, `orders.cancel`, object visibility/ownership, order state, `If-Match`, and rate/risk policy. **Conclusion:** the scope intersection prevents over-issuance; local authorization prevents over-use.

### Connections

[Applying OpenID Connect at API Boundaries](044-applying-openid-connect-at-api-boundaries.md) supplies stable actor identity, [OAuth Authorization Flows](043-oauth-authorization-flows.md) obtains grants, and [Credential and Token Handling](042-credential-and-token-handling.md) bounds tokens. [Object-Level Authorization](../ROADMAP.md) next deepens the local predicate that scopes intentionally cannot express.

## Governing Question

Which stable capabilities should an authorization server be able to grant to which clients/actors for which resource audiences, and which decisions must remain current, contextual, and object-specific inside the resource server?

## Why This Matters

Scope design becomes a public security vocabulary. Clients request it, authorization servers grant it, users/administrators see it, access tokens carry it, APIs enforce it, audits record it, and migrations depend on it. A vague scope can outlive the implementation that gave it meaning. A broad `write` issued years ago may accidentally authorize a newly added irreversible refund endpoint.

Too little granularity forces clients to receive excess authority. Too much granularity creates an unmanageable catalogue, unusable consent, enormous tokens, and brittle client configuration. Encoding object IDs, field filters, amounts, and workflow constraints into flat strings quickly turns the vocabulary into an unbounded policy language without a parser or governance model.

Scope is only one dimension. An access token also needs the correct resource audience, actor/client/tenant, lifetime, sender constraint, and current status. At the API, a scope still cannot answer whether the caller owns order 7, whether the order is cancellable, whether delegation covers this tenant, or whether a high-risk action needs fresh authentication.

A good design therefore separates portable capability from local policy. The authorization server intersects what was requested with what every authority source permits. The resource server validates that bounded token and applies current action/object/state rules. This creates defense in depth without duplicating the same unclear policy in two places.

## Prerequisites and Retrieval

Retrieve set intersection, least privilege, OAuth authorization requests/grants/tokens, scopes, resource indicators/audience, bearer and sender-constrained tokens, consent, client registration, user/service/tenant authority, RBAC and ABAC, claims/groups/roles, JWT/introspection, token exchange, rich authorization requests, object-level authorization, policy decision/enforcement points, deny/default rules, revocation/staleness, audit, and versioning.

Before defining scopes, retrieve consumer tasks and client types, resource servers/audiences, API operation inventory, action risk, object/tenant model, user and service authority sources, delegation, client eligibility, consent/administrator grant model, existing scopes/tokens/clients, composite/wildcard behavior, token formats/size, lifetime/revocation, step-up/transaction needs, rich authorization support, policy ownership, enforcement locations, public documentation/errors, telemetry/audit, emergency controls, and migration/compatibility constraints.

## Learning Objectives

By the end of this module, you should be able to:

1. distinguish resources/audiences, scopes, permissions, roles/groups, claims, and object policy;
2. derive a stable capability vocabulary from consumer tasks and domain actions;
3. compute effective token permissions as an intersection of independent authority bounds;
4. choose atomic, composite, resource-specific, and rich authorization representations;
5. enforce scope and local object/action policy at the owning resource server;
6. version, migrate, revoke, observe, and govern permission semantics; and
7. test over-grant, under-grant, confused deputy, stale policy, and every enforcement path.

## Core Exposition

### Separate four layers of authorization meaning

Use four named layers:

1. **Resource/audience:** Which API/resource server may receive the token? Examples: `https://api.example/orders` or a stable logical audience.
2. **Capability/permission:** What class of action may be attempted? Examples: `orders.read`, `orders.cancel`, `orders.refund`.
3. **Actor/client/tenant grant:** Which user/service/client delegation currently holds that capability and under which tenant/relationship?
4. **Object/action/state policy:** May this exact actor/client perform the capability on this target now?

OAuth `scope` often carries the capability layer, but deployments sometimes use structured claims or entitlement identifiers. The representation matters less than having one documented semantic map. Do not overload scope with audience: a token with `orders.read` but audience `billing-api` is still unusable at orders. Do not overload identity-provider group with API capability: `Finance-Team` is organizational data whose mapping and lifecycle must be governed.

The resource server owns the final decision because it knows route/action, target, tenant, state, relationships, preconditions, and often current risk. The authorization server owns grant issuance policy and can prevent a client/user from ever receiving capabilities they are ineligible for. Keep the boundary explicit.

### Derive permissions from consumer and domain actions

Start with meaningful tasks and domain commands/queries, not database CRUD or HTTP verbs alone. `orders.write` hides important differences among create, amend address, cancel, approve exception, mark shipped, and refund. Some are reversible and low risk; others move money or defeat controls.

Create an operation-permission matrix with:

- stable permission ID and human description;
- API audience and owning team;
- operations/routes/events covered;
- actor types and eligible client classes;
- object/tenant relationship required;
- domain-state and assurance/freshness requirements;
- data/property visibility or mutation bounds;
- consent/admin display and risk class;
- audit/monitoring and emergency-disable behavior; and
- introduction/deprecation/version history.

Prefer action names that survive transport refactoring. `orders.cancel` remains clear if a route changes from `POST ...:cancel` to a command endpoint. Avoid names tied to implementation tables or temporary versions. Use a consistent namespace owned by the resource server, such as `orders.read`, not a global `read` that every API interprets differently.

Do not make every route its own permission automatically. Several read routes may share one capability if data sensitivity and relationships are equivalent. Split when risk, data, client eligibility, user understanding, audit, or independent revocation differs. The goal is minimum useful authority, not maximum string count.

### Compute grants by intersection, never union-by-accident

At authorization/token issuance, requested authority is only an upper request. Compute effective permissions from independent bounds:

- permissions the client registration is eligible to request;
- authority the resource owner/user/service actually holds;
- permissions approved by user/admin/organizational grant;
- permissions relevant to the selected resource audience;
- current security/product policy, risk, tenant, and grant status; and
- the subset requested for this token/transaction.

Every source narrows. No single client parameter or directory claim expands beyond another authority boundary. Record which principal/client/grant/resource produced the result. If an authorization server cannot satisfy a request, reject or return a clearly documented reduced grant according to protocol/client expectations; never silently add scopes.

For a service acting as itself, omit user authority/consent and intersect service registration, workload identity, organization/tenant allocation, resource policy, and request. Do not populate a user ID from input. For delegated user access, preserve both client and subject/effective actor; a privileged client should not amplify an unprivileged user, nor should a privileged user make an untrusted client eligible for every permission.

Downscoping at refresh or token exchange can produce a subset of an existing grant, never recover removed/ungranted authority. Bind audience and sender again. Chained services should receive an audience- and purpose-specific token rather than forwarding one broad upstream token everywhere.

### Design atomic permissions and composites deliberately

An **atomic permission** has one stable independently reviewable capability. A **composite scope** is a convenience bundle expanded by the authorization server/resource policy, such as `orders.manage` expanding to create/read/update/cancel under a versioned contract.

Composites improve client configuration and consent readability but create future-expansion risk. If `orders.manage` later includes `orders.refund`, every existing grant may silently gain money movement. Safer choices are:

- freeze composite membership for its lifetime/version;
- require new consent/admin approval for expansion;
- introduce a new composite; or
- keep high-risk permissions explicitly separate.

Document whether tokens carry the composite string or expanded atomic set. Resource servers should enforce one canonical expansion source and version, not each service team's informal guess. Audit should make effective atomic authority explainable.

Avoid wildcards such as `orders.*` in externally issued tokens unless the set is closed and immutable under an exact version. Wildcards turn future feature deployment into privilege escalation. Internal policy languages may use patterns with governed evaluation, but minting them to long-lived external clients carries the same expansion risk.

### Keep defaults minimal and semantics monotone

If `scope` is omitted, RFC 6749 lets an authorization server use a documented default or reject. Choose a minimal explicit default; never interpret omission as every registered permission for legacy convenience. Return the actually granted scope when it differs from requested as the protocol requires.

Permission sets should be easy to reason about. Adding a permission to a request must not remove unrelated authority through hidden conflict unless a documented policy says so. Avoid negative scope strings like `orders.read !orders.sensitive`: merging allow/deny across grants, tokens, and services becomes order-dependent. Keep deny/constraints in the policy layer with explicit precedence and current data.

Define implication only where unavoidable. If `orders.cancel` implies `orders.read`, state and test it; alternatively mint both atomic permissions. Do not infer that write always includes read: write-only ingestion is legitimate, and read may disclose more data. Do not infer that admin bypasses tenant, object, state, or audit rules.

Permission names are opaque protocol strings; case, separators, and comparison rules must be exact. Normalize at registration/authoring, not inconsistently at runtime. Unknown permissions are rejected or ignored only under a documented profile; they never become true by substring/prefix matching.

### Restrict each token to a resource audience

RFC 9700 recommends minimum privileges and audience restriction to a resource server or small justified set. RFC 8707 `resource` lets a client identify target protected resources so the authorization server can mint appropriately restricted tokens. The resource server validates audience on every request.

Prefer one access token per resource server. A token accepted by orders, billing, admin, and analytics increases theft blast radius and lets a compromised/counterfeit resource replay it elsewhere. Separate audiences also let each API use its own token format, claims, lifetime, sender binding, and privacy minimization.

Scope namespaces alone are not adequate audience restriction. `orders.read` in a token accepted by billing is a configuration failure even if billing ignores it today. Conversely, audience `orders-api` does not confer any action. Require both audience and permission.

Resource identifiers may include tenant path when the resource topology and standard profile require tenant-specific audience separation, as RFC 8707 discusses. Balance that against token proliferation/privacy. At minimum, API local tenant policy must remain authoritative.

At token refresh/exchange, the requested resource and scope must stay within the original grant and current policy. A token for resource A must not be exchanged into resource B merely because the client asks, unless an explicit grant/policy authorizes the transition.

### Use rich authorization details for structured transactions

Flat scope strings are poor at expressing “initiate one payment of EUR 125 to beneficiary 9 from account 7.” Encoding it as `payment:account7:beneficiary9:EUR:125` creates unbounded names, escaping/canonicalization problems, unreadable consent, and brittle policy.

RFC 9396 defines `authorization_details`, an array of typed JSON objects. A type-specific profile can express actions, locations/resources, amounts, identifiers, and other details with defined schema/semantics. Use it when transaction-specific authorization is material and ecosystem participants implement the profile.

Design each authorization-detail type with:

- registered/stable `type` and owning specification;
- closed schema, canonical identifiers/types/limits;
- allowed actions and their relationship to scopes;
- resource/audience binding;
- client/user eligibility and consent display;
- subset/downscope/refresh rules;
- token/response representation and privacy;
- resource-server validation and replay/transaction binding; and
- errors, versioning, and audit.

Rich authorization is not a license to accept arbitrary client JSON as policy. The authorization server validates against client/grant/user/resource policy and may grant a subset. The resource server compares the authorized details with the actual request/domain object using canonical semantics. For high-integrity flows, pushed or signed authorization requests may protect request confidentiality/integrity under their specifications.

Use object-level authorization instead when the decision is ordinary local ownership/relationship across many objects. Do not mint a new token for every row merely to avoid writing repository scoping. Rich details fit explicit transaction authorization whose exact parameters matter to consent/approval.

### Treat roles, groups, and claims as inputs, not permissions by accident

Roles aggregate responsibilities; groups aggregate membership; claims convey issuer assertions; scopes/permissions describe token capability. They can map, but they are not interchangeable.

Define a policy mapping such as `tenant-billing-operator` role → eligible `invoices.read` and `invoices.adjust` for that tenant, subject to client eligibility and object rules. Store mapping ownership/version and deprovisioning. Do not let an identity-provider group named `admin` automatically become a global API admin permission across every environment.

Claims have provenance and staleness. Token-embedded groups may remain after removal until expiry. Local policy lookup is fresher but adds dependency/latency. State the maximum staleness and critical-action strategy. Ensure directory administrators who can change groups are understood as authorization administrators and audited accordingly.

Roles should not explode combinatorially for every context. Attribute/relationship-based policy can evaluate subject, object, operation, and environment, as NIST's ABAC model describes. Keep token inputs minimal and stable; fetch current resource relationships locally.

### Place enforcement at every owned entry path

At the resource server:

1. validate token type, issuer, key/introspection, audience, time, sender/status;
2. construct immutable subject/client/tenant context;
3. map token scope/authorization details through the API-owned canonical vocabulary;
4. map route/method/domain command to required permission(s);
5. load/identify the target in authoritative tenant scope;
6. evaluate object, relationship, state, assurance, delegation, and environmental policy;
7. execute inside required concurrency/transaction boundary; and
8. audit the decision/effect with safe identifiers.

Do this for REST routes, GraphQL fields/resolvers, RPC methods, batch elements, bulk filters, async job submission/execution/download, WebSocket establishment/messages, event consumers, admin/support tools, and internal direct calls. A gateway check is defense in depth, not proof every backend path enforces correctly.

Map operations to permissions centrally enough to review but close enough to code to avoid drift. Fail closed when no mapping exists. Tests enumerate all registered operations and prove each has an authorization rule. Generated annotations alone are insufficient if alternate methods/routes bypass them.

Batch/bulk operations require per-element or query-scope authorization; `orders.read` does not let a caller supply arbitrary tenant IDs. Field/property access may need separate permissions or serializer/mutation policies. Later modules deepen these boundaries.

### Return errors without turning policy into reconnaissance

If a token is absent/invalid, use the authentication failure contract. If authenticated but missing a required token permission, a `403`/OAuth insufficient-scope challenge may be appropriate; disclose required scopes only when safe and useful. If object existence is concealed, the local policy can return `404` without revealing whether scope or ownership failed.

Do not return the caller's entire effective permission set, internal role/group names, policy source, another tenant's data, or privileged alternative scopes in public errors. Stable problem types can distinguish recoverable missing grant from non-recoverable object denial without explaining sensitive topology.

Clients do not blindly request every scope named by an error. They initiate an explicit authorization/consent upgrade only for a feature the user selected, preserving original action context and anti-CSRF/step-up rules. APIs do not redirect to authorization servers themselves.

### Govern lifecycle and semantic changes

Maintain a permission registry with owner, audience, description, risk, atomic/composite expansion, operations, eligible clients/actors, consent/admin text, introduced/deprecated dates, replacement, token/grant population, and verification links. Reconcile it with API contracts/routes, authorization-server configuration, clients, and observed tokens.

Adding an endpoint requires explicit permission mapping. Adding a destructive action to an existing broad permission is a security change needing threat/risk/compatibility review. Renaming or splitting a permission requires client registration, consent/grant, token lifetime, refresh, policy, documentation, SDK, and monitoring migration.

Do not redefine an existing scope silently. Introduce new atomic/composite permission, dual-enforce or dual-mint under a bounded migration, update clients/grants with approval, monitor old/new use, then stop issuance and reject old authority after its token/grant window. Revocation may be required for urgent narrowing.

Emergency controls can disable a permission, client, tenant, or action even when tokens carry it. Define propagation latency, cache behavior, owner/approval, audit, rollback, and customer communication. A self-contained token cannot guarantee immediate semantic changes without state checks or short life.

### Observe least privilege and drift

Measure requested versus granted versus used permissions by bounded client/resource classes; denial reasons; unused high-risk grants; tokens with multiple audiences; wildcard/composite use; old/deprecated permission use; scope/route mapping coverage; policy latency/error; emergency denies; and revocation propagation.

Avoid raw subjects/tokens or unbounded scope sets as metric labels. Put sensitive detailed grant data in protected audit/log systems with retention and access controls. Audit grant creation/change, consent/admin approval, token issuance/downscope/exchange, policy mapping change, high-risk use, denial, and revocation.

Periodic access review asks whether clients still need permissions, whether owners exist, whether high-risk unused grants can be removed, whether group mappings remain correct, and whether object rules actually constrain broad scopes. Runtime usage informs but does not alone prove authority unnecessary; consider seasonal/emergency paths before removal.

The executable model below illustrates token intersection followed by local object/state authorization. It does not represent OAuth message validation or a production policy engine.

<!-- bijux-verify: {"id":"effective-permission-intersection","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"granted=orders.cancel,orders.read\ncancel_own_open=allow\ncancel_other_open=deny:object\ncancel_own_shipped=deny:state\nrefund_own=deny:permission\nwrong_audience=deny:audience\n","stderr":""}} -->
```python
requested = {"orders.read", "orders.cancel", "orders.refund"}
client_allowed = {"orders.read", "orders.cancel"}
user_allowed = {"orders.read", "orders.cancel", "orders.refund"}
consented = {"orders.read", "orders.cancel"}
resource_policy = {"orders.read", "orders.cancel", "orders.refund"}
granted = requested & client_allowed & user_allowed & consented & resource_policy

def authorize(audience, permission, owner, actor, state):
    if audience != "orders-api":
        return "deny:audience"
    if permission not in granted:
        return "deny:permission"
    if owner != actor:
        return "deny:object"
    if permission == "orders.cancel" and state != "open":
        return "deny:state"
    return "allow"

print("granted=" + ",".join(sorted(granted)))
print("cancel_own_open=" + authorize("orders-api", "orders.cancel", "u1", "u1", "open"))
print("cancel_other_open=" + authorize("orders-api", "orders.cancel", "u2", "u1", "open"))
print("cancel_own_shipped=" + authorize("orders-api", "orders.cancel", "u1", "u1", "shipped"))
print("refund_own=" + authorize("orders-api", "orders.refund", "u1", "u1", "paid"))
print("wrong_audience=" + authorize("billing-api", "orders.read", "u1", "u1", "open"))
```

The model shows why a token permission is necessary but not sufficient: cancellation still depends on the target owner and state.

### Verify grants and every enforcement path

Test the set algebra with empty, minimal, excessive, unknown, composite, wildcard, conflicting, multi-resource, user, service, delegated, refresh, exchange, and revoked inputs. Property tests can assert effective permissions are a subset of every independent authority source and never grow during downscope.

For each operation, test missing token, wrong issuer/type/audience, missing permission, correct permission/wrong object/tenant/state/client, and allowed outcome. Cover alternate routes/methods, batches, filters, expansions, fields, GraphQL aliases/fragments, RPC, streams, jobs, events, admin/support, caches, and direct internal calls. Scan the contract/route registry for unmapped operations.

Test composite expansion before/after catalogue changes, old tokens/grants, permission split/rename, new destructive endpoint, omitted scope/default, case/Unicode/prefix ambiguity, token size, policy-store/cache outage, role/group removal, revocation latency, emergency disable, error disclosure, and audit completeness. Red-team high-risk clients/scopes and simulate a leaked multi-audience/wildcard token.

## Definitions and Notation

Let requested permissions be $Q(q)$, client eligibility $C(c)$, actor authority $U(u)$, resource-relevant permissions $R(r)$, grant/consent $G(g)$, and current restrictions $P(p)$. Effective token permissions are intersection $E$ and therefore satisfy $E\subseteq Q(q)$, $E\subseteq C(c)$, $E\subseteq U(u)$, $E\subseteq R(r)$, $E\subseteq G(g)$, and $E\subseteq P(p)$.

Let local authorization function $A(subject,client,tenant,action,object,state,environment)$ use current authoritative attributes/relationships. Let $V_{token}$ include token type/issuer/audience/time/sender/status validation. Authorization requires all of token validity, membership of required action in $E$, and local $A$.

A **permission registry** is the governed canonical semantic source. A **grant** can outlive an individual token and is narrowed into token authority. A **role** groups responsibilities; an **entitlement** records granted right; an **attribute** describes subject/object/environment; a **scope** is an OAuth request/grant string. These may map but are not synonyms.

## Mechanisms, Invariants, or Proof Structure

1. Inventory consumer tasks, domain actions, resource servers, clients, actors, tenants, and current grants.
2. Separate audience/resource, capability, actor/client grant, and object/state policy.
3. Define stable atomic permissions with owners, risk, eligible callers, operations, consent, and evidence.
4. Govern composites/wildcards/defaults; prevent future actions from silently expanding old authority.
5. Compute token permission sets only by intersection and bind them to one resource audience/sender/lifetime.
6. Use rich authorization details for typed transaction specifics, not unbounded ad hoc scope strings.
7. Map roles/groups/claims through governed current policy; preserve client and subject/delegation.
8. Enforce token, permission, tenant/object/action/state rules at every resource-server path.
9. Return safe errors and record grant/use/decision evidence without policy leakage.
10. Version/migrate/revoke semantics and continuously test subset, coverage, staleness, and bypass properties.

The intersection proves only non-expansion relative to its input sets. If a source is wrong, stale, attacker-controlled, or mapped incorrectly, $E$ can still be unsafe. Local enforcement coverage and object policy require separate evidence.

## Alternatives and Trade-Offs

Coarse scopes keep consent, tokens, and client registration manageable but increase over-privilege and reliance on local policy. Fine scopes improve independent grant/revocation but create catalogue/client/consent complexity. Split by meaningful risk and task, not route count.

Atomic scopes are stable and auditable but verbose. Composites improve usability but require frozen/versioned expansion. Wildcards simplify internal administration but create future privilege; avoid them in external durable grants.

Flat scopes interoperate broadly and fit capability classes. Rich authorization details express transaction structure precisely but need shared schemas, validation, consent rendering, token representation, canonical matching, and lifecycle rules.

JWT-embedded permissions enable local availability/performance but are stale until expiry and expose claims. Opaque/introspected or policy-lookup designs improve current state but add latency/availability/privacy coupling. Combine with explicit staleness bounds for critical actions.

Central policy engines improve consistency and decision visibility but can become latency/availability bottlenecks and require correct data. Service-local policy is close to objects but can drift. Centralize semantic policy/governance where useful while enforce/load targets at the owning boundary.

One multi-audience token reduces token acquisition calls but expands leakage and confused-deputy risk. Per-resource tokens increase acquisition/cache complexity but improve least privilege, privacy, and independent format/lifetime. Prefer per-resource by default.

## Failure Modes and Misconceptions

- **“Scope is audience.”** Token destination and capability are independent checks.
- **“Requested means granted.”** Effective authority is an intersection of independent bounds.
- **“A user's admin role makes any client admin.”** Client eligibility and delegation still narrow.
- **“Client credentials can borrow user permissions.”** Machine self-authority has no invented user.
- **“Write includes every future mutation.”** New destructive actions require explicit security review/grant.
- **“Admin bypasses object/tenant/state policy.”** Define exact actions; retain isolation and invariants.
- **“Consent authorizes any object.”** It approves bounded grant, not current target relationships.
- **“Groups are scopes.”** Map governed identity attributes into permissions with lifecycle.
- **“Missing scope means legacy full access.”** Defaults are minimal or omission is rejected.
- **“Negative scopes make least privilege easy.”** Deny precedence becomes ambiguous; keep constraints in policy.
- **“Put object IDs in scope strings.”** Use local authorization or typed rich details.
- **“Gateway permission checks are enough.”** Every backend/alternate path must enforce.
- **“JWT permissions update immediately.”** Define expiry, state checks, and revocation propagation.
- **“403 should list every possible scope.”** Error detail can leak policy and encourage over-requesting.

## Worked Examples

### Example 1

**Situation:** A client requests `orders.read orders.cancel orders.refund`, but registration allows read/cancel. **Reasoning:** Client eligibility intersects the user/grant request. **Conclusion:** issue at most read/cancel and communicate the actual grant.

### Example 2

**Situation:** Token has `orders.cancel` for `orders-api`; user targets another tenant's order. **Reasoning:** Scope names capability, not target relationship. **Conclusion:** deny through tenant/object authorization without revealing existence.

### Example 3

**Situation:** Existing `orders.write` is proposed to cover refunds. **Reasoning:** Old grants would silently acquire money movement. **Conclusion:** introduce `orders.refund` with separate eligibility/consent/assurance and migration.

### Example 4

**Situation:** A token has `orders.*`, issued before a new purge action. **Reasoning:** Wildcard expansion creates future privilege. **Conclusion:** reject/freeze versioned expansion and require explicit purge authority.

### Example 5

**Situation:** A payment client needs one EUR 125 transfer. **Reasoning:** Flat scopes cannot safely express amount/account/beneficiary. **Conclusion:** use a typed RFC 9396 authorization detail and bind actual transaction parameters, plus local state checks.

### Example 6

**Situation:** Identity group `Finance-Admin` is copied as global `admin`. **Reasoning:** Issuer group semantics, tenant, client, environment, and action are lost. **Conclusion:** use an owned mapping to narrow tenant billing permissions and test deprovisioning.

### Example 7

**Situation:** One bearer token is accepted by orders and billing. **Reasoning:** Either resource compromise can replay it at the other. **Conclusion:** mint per-resource audience tokens using resource indicators and minimal claims.

### Example 8

**Situation:** A GraphQL gateway checks `orders.read`, but a direct resolver/service path omits object policy. **Reasoning:** Gateway scope is not end-to-end enforcement. **Conclusion:** enforce at resolver/service repository boundary and test aliases/batches/direct calls.

### Example 9

**Situation:** An employee loses a role while a one-hour JWT retains its permission. **Reasoning:** Offline validation has a staleness bound. **Conclusion:** shorten life or add policy-version/state checks for high-risk actions and document revocation latency.

### Example 10

**Situation:** API returns every missing internal permission in a `403`. **Reasoning:** It exposes features/roles and clients request broad access reactively. **Conclusion:** return a stable safe insufficient-authority problem and drive explicit feature authorization.

## Cross-Program Connections

- **Identity and Access Management:** roles, groups, entitlements, delegation, consent, and provisioning supply governed authority inputs.
- **Security Engineering:** least privilege, confused deputy, capability confinement, revocation, separation of duties, and defense in depth shape grants.
- **Database Engineering:** tenant/object relationships, row/property filtering, state, and transactions supply the local authorization truth.
- **Distributed Systems:** token caches, policy propagation, exchange, multi-audience replay, partial rollout, and revocation latency bound semantics.
- **Language and Type Systems:** closed permission enums, typed authorization details, exhaustive mappings, and deny-by-default reduce ambiguity.
- **Product Design:** consumer tasks, understandable consent, incremental access, and recovery determine usable permission granularity.
- **Observability and Governance:** grant registries, usage review, drift detection, audit, and emergency disable keep authority current.

## References

1. Hardt, D. [RFC 6749: The OAuth 2.0 Authorization Framework](https://www.rfc-editor.org/rfc/rfc6749.html). IETF, October 2012. Checked 2026-09-01.
2. Lodderstedt, T., Bradley, J., Labunets, A., and Fett, D. [RFC 9700: Best Current Practice for OAuth 2.0 Security](https://www.rfc-editor.org/rfc/rfc9700.html). IETF BCP 240, January 2025. Checked 2026-09-01.
3. Campbell, B., Bradley, J., and Tschofenig, H. [RFC 8707: Resource Indicators for OAuth 2.0](https://www.rfc-editor.org/rfc/rfc8707.html). IETF, February 2020. Checked 2026-09-01.
4. Lodderstedt, T., Richer, J., and Campbell, B. [RFC 9396: OAuth 2.0 Rich Authorization Requests](https://www.rfc-editor.org/rfc/rfc9396.html). IETF, May 2023. Checked 2026-09-01.
5. Bertocci, V. [RFC 9068: JSON Web Token (JWT) Profile for OAuth 2.0 Access Tokens](https://www.rfc-editor.org/rfc/rfc9068.html). IETF, October 2021. Checked 2026-09-01.
6. Hu, V., Ferraiolo, D., Kuhn, R., et al. [NIST SP 800-162: Guide to Attribute Based Access Control Definition and Considerations](https://csrc.nist.gov/pubs/sp/800/162/upd2/final). NIST, updated August 2019. Checked 2026-09-01.

## Exercises

### Exercise 1

Design an audience, atomic-permission, composite, and consent catalogue for orders, billing, analytics, and support APIs. Include actor/client eligibility, risk, object rules, assurance, and versioning.

### Exercise 2

Compute effective permissions for an employee using a third-party client in two tenants when requested, client-eligible, user-role, consent, resource, and emergency-policy sets differ. Explain every removed permission.

### Exercise 3

Design an RFC 9396 authorization-detail type for approving one refund with order, amount, currency, payment method, tenant, and expiry. Specify subset, token representation, and API comparison.

### Exercise 4

Create an enforcement and test matrix spanning REST, GraphQL, batch export, async report jobs/downloads, WebSockets, events, internal service calls, and support tools.

### Exercise 5

Plan a migration that splits broad `orders.write` into `orders.create`, `orders.amend`, `orders.cancel`, and `orders.refund` while millions of tokens/grants and multiple client versions remain active.

## Answers to the Exercises

### Answer 1

Use distinct audiences such as `orders-api`, `billing-api`, `analytics-api`, and `support-api`, normally one token each. Atomic orders capabilities include read, create, amend-address, cancel, and exception approval; billing includes invoice read/adjust and refund; analytics uses aggregate read/export; support uses case read and narrowly governed impersonation. Define composites only for stable low-risk task bundles—e.g., `orders.operator` might expand to read/create/amend but excludes cancel/refund—and freeze/version expansion. Each entry records owner, eligible first/third-party/public/confidential clients, user/service roles, tenant/object relationship, property bounds, required fresh assurance for refund/impersonation/export, consent/admin display, audit, emergency disable, and mapping tests. Never make one global admin/read/write scope. High-risk refund, sensitive export, and support impersonation remain explicit and independently revocable.

### Answer 2

Let requested be `{orders.read, orders.cancel, orders.refund, analytics.export}`; client eligibility `{orders.read, orders.cancel, analytics.export}`; employee role in tenant north `{orders.read, orders.cancel, orders.refund}` and south `{orders.read}`; consent `{orders.read, orders.cancel, analytics.export}`; selected orders resource `{orders.read, orders.cancel, orders.refund}`; emergency policy disables cancel. For a north orders token, the intersection is only `{orders.read}`: refund is removed by client eligibility/consent; export by resource; cancel by emergency policy. For south, user/tenant authority also leaves only read. A separate analytics token could contain export only if user authority for that tenant and all other sets include it. Record subject, client, tenant, audience, grant, and removal reasons; never union permissions across the two tenants/resources.

### Answer 3

Define type `urn:example:refund-approval` with closed fields: tenant ID, order/payment IDs in canonical forms, action array limited to `approve`, amount object with decimal-string amount and ISO currency, permitted payment-method reference, and approval expiry. Registration/policy binds eligible clients, refund approvers, resource `billing-api`, maximum amount/currencies, and required fresh assurance. The authorization server validates the object against current actor/client/order policy, renders exact meaningful consent/approval, and may reduce actions/amount/expiry but never expand. The token carries a stable approved-detail identifier or privacy-minimized structured detail plus audience and expiry; server storage preserves canonical approved parameters/audit. The API validates token, retrieves/verifies detail, exact tenant/order/payment/currency/method, actual amount no greater/equal as profile defines, expiry, single-use/idempotency, approver separation, current order/payment state, and transaction concurrency. Refresh cannot extend amount/action/expiry without new approval.

### Answer 4

For every entry path, list token validator/audience, operation-to-permission mapping, tenant/target loader, object/property/state predicate, failure concealment, audit, and negative tests. REST covers alternate verbs/routes and bulk IDs; GraphQL covers each resolver/field, aliases/fragments, batching, introspection policy, and cost; export validates filters and every tenant/data class before job creation. Async jobs persist immutable actor/client/grant/tenant scope, reauthorize or use bounded snapshot policy at execution, and authorize artifact downloads independently. WebSockets authorize handshake and every message/subscription over lifetime/revocation. Event consumers authenticate producer/event context and never trust payload tenant/permission. Internal service calls use audience-specific workload/delegated tokens and enforce again. Support tools require scoped just-in-time authority, actor/effective subject, approval, expiry, and audit. Coverage tests compare route/schema/job/event registries with mappings and fail on any unmapped new path.

### Answer 5

Inventory every issuer, audience, client/version, grant, refresh token, access-token lifetime, endpoint, and actual `orders.write` use. Define atomic semantics and explicitly decide the legacy expansion—freeze it to its historical actions and exclude new/high-risk refund if possible. Update resource servers first to accept legacy plus atomics with identical object policy and telemetry showing which atomic action each legacy call exercised. Update authorization-server/client registration/consent and SDKs to request/mint atomics; composites, if added, have frozen expansion. Migrate grants through administrator/user approval where authority broadens; down-map existing grants only to historically authorized actions. Bound dual issuance, refresh behavior, and last legacy token expiry; revoke high-risk ambiguous grants if necessary. Monitor old client/use/denials, contact owners, then stop new legacy grants, stop refresh issuance, wait/revoke residual tokens, reject legacy, remove mapping, and verify no alternate paths. Rollback may restore compatibility mapping temporarily but must not make refund or future actions part of legacy write.
