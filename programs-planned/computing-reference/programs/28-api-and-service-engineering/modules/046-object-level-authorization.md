---
module_id: API-046
program: API & Service Engineering
level: 1
module_number: 46
title: Object-Level Authorization
status: complete
last_verified: 2026-09-01
---

# Object-Level Authorization

## One-Page Review

### Governing question

How can an API ensure that an authenticated caller with permission to invoke an operation may act only on the exact objects, fields, relationships, states, and tenants that current policy allows?

### Essential definitions

- **Object-level authorization** decides whether a subject, acting through a client, may perform one action on one object in the current context.
- **Broken object-level authorization (BOLA)** occurs when an API accepts an attacker-controlled object reference without enforcing the required subject–action–object policy.
- An **object reference** is a path, query, header, body, cursor, global ID, storage key, or indirect handle that selects an object; it is not evidence of authority.
- A **relationship** is a governed edge such as owner, member, editor, parent, delegate, or approver between subjects and objects.
- An **authorization context** contains trusted subject, client, tenant, grant, action, object attributes, state, environment, and policy-version inputs.
- **Authorized retrieval** constrains lookup by policy, so an inaccessible object is not loaded as an ordinary application result.
- A **policy decision point (PDP)** evaluates policy; a **policy enforcement point (PEP)** prevents the operation unless the decision permits it.
- **TOCTOU** is a time-of-check/time-of-use race in which the facts authorized earlier differ when the protected effect occurs.

### Central model, mechanism, or theorem

For trusted context $c$, action $a$, object $o$, and current state $s$, define

$$
\operatorname{allow}(c,a,o,s)=V(c)\land C(c,a)\land R(c,a,o)\land A(c,a,o,s)\land E(c,a,o,s).
$$

$V$ validates the security context, $C$ checks coarse capability, $R$ checks tenant/ownership/delegation relationships, $A$ checks subject/object/action attributes and state, and $E$ checks current environmental constraints. Each term is necessary. An identifier never appears as a sufficient term.

For retrieval, use the authorized set

$$
O_{c,a}=\{o\in O\mid \operatorname{allow}(c,a,o,state(o))\}.
$$

Resolve a client-supplied identifier only inside $O_{c,a}$; for a mutation, re-evaluate the relevant predicate atomically with the state change.

### Critical invariants

Authentication, route access, token scope, identifier secrecy, and possession of a URL do not imply object authority. Subject, client, and tenant come from validated server context rather than ordinary request fields. Every object reference and every action—including nested, batch, search, export, GraphQL, job, event, storage, and support paths—has a PEP. Policy denies by default and fails closed when required facts are unavailable. Reads filter before projection; writes constrain both the old row and permitted new state. Every member of a batch is authorized under an explicit all-or-nothing or partial-result contract. Cache keys and artifacts preserve authorization boundaries. High-risk decisions use current data or a bounded, declared snapshot. The protected effect cannot race past the decision unnoticed. Denials disclose no more existence or policy detail than the API contract permits. Decisions are explainable and auditable without logging secrets.

### Common failures

Loading by raw ID and checking only authentication; comparing a user ID to a request-body owner ID; trusting tenant headers; assuming a UUID is authorization; checking list endpoints but not detail/export/download paths; testing “has role” without object relationship; permitting reads through nested expansions or counts; authorizing the first batch item only; updating by ID after a separate stale check; allowing clients to change ownership/tenant fields; caching an authorized representation under an object-only key; issuing a long-lived signed URL after revocation; running async work as an omnipotent service; bypassing policy in support/admin/direct-database paths; using 403/404 inconsistently; and deploying new routes with no authorization mapping.

### Compact example

Alice has `orders.cancel` and owns open order 7 in tenant north. Mallory has the same scope and can guess order 7's UUID. The API executes a conditional mutation whose predicate includes order ID, tenant from Mallory's trusted context, required owner relationship, current `open` state, and version. It affects zero rows and returns the same concealed not-found response used for an absent object. Alice's equivalent request affects one row and is audited. **Conclusion:** permission permits attempting cancellation; only the current subject–tenant–object–state predicate permits this cancellation.

### Connections

[Scope and Permission Design](045-scope-and-permission-design.md) bounds which actions a token may attempt, [Request-Scoped Transaction Boundaries](036-request-scoped-transaction-boundaries.md) makes a checked mutation atomic, and [Concurrency Control at the API Boundary](038-concurrency-control-at-the-api-boundary.md) supplies version/precondition reasoning. [Mass Assignment and Overposting](../ROADMAP.md) next secures the proposed new object state.

## Governing Question

Given an untrusted object reference and a valid caller, how does the service derive a complete current policy decision and bind that decision to the exact read, mutation, transfer, export, or delegated effect?

## Why This Matters

Most useful callers legitimately access an endpoint and some objects of its type. That makes object authorization different from merely hiding an endpoint. A customer may read their own invoices but not a neighbor's; an editor may change document content but not transfer ownership; an operator may inspect one tenant but not another; a service may process assigned jobs but not arbitrary records. The dangerous request often looks syntactically normal and carries a valid token with the right broad permission.

OWASP API1:2023 calls this class Broken Object Level Authorization and notes that identifiers appear not only in paths but also query parameters, headers, and bodies. Sequential numbers make enumeration convenient, but UUIDs, opaque global IDs, and signed-looking references remain attacker-controlled selectors. If the server can retrieve an object by the selector, it must independently decide whether this caller may perform this action on it.

The decision is rarely ownership alone. Real policy includes tenant, membership, delegation, client, object classification, parent relationship, action, field, state, time, assurance, separation of duties, legal hold, and emergency restrictions. These facts change. Copying a user ID from a token into one comparison covers only the simplest model and can even compare against attacker-controlled data.

Object authorization is also an architecture property. A perfect policy function offers no protection when one controller, resolver, export job, cache, or storage download bypasses it. Conversely, scattering hand-written checks across handlers produces drift. A durable design gives every path a consistent enforcement obligation, locates trusted facts, makes decisions testable, and binds authorization to data access and mutation concurrency.

## Prerequisites and Retrieval

Retrieve authentication versus authorization, OAuth audiences/scopes, least privilege, deny by default, tenant isolation, domain actions and invariants, RBAC/ABAC/ReBAC, database predicates and transactions, optimistic concurrency, TOCTOU, GraphQL resolution, batch/async semantics, caches, object storage, HTTP 401/403/404 semantics, audit logging, policy distribution, and revocation/staleness.

Before implementing a policy, retrieve the object and relationship model, all identifiers and entry paths, action/field/state matrix, actor and client types, tenant source, source-of-truth attributes, delegation and sharing rules, public-object behavior, parent/child inheritance, list/search/export semantics, batch atomicity, mutation concurrency, cache/artifact lifetimes, background execution identity, policy ownership/version, denial disclosure contract, audit requirements, and emergency/recovery paths.

## Learning Objectives

By the end of this module, you should be able to:

1. distinguish object references, coarse permissions, and object-level authority;
2. model decisions over trusted subject, client, tenant, action, relationship, object, state, and environment;
3. choose authorized retrieval, centralized policy, relationship graphs, or database row policy deliberately;
4. secure reads, lists, nested data, batches, creates, mutations, transfers, jobs, caches, and artifacts;
5. bind authorization to a protected effect without a TOCTOU gap;
6. design concealed yet diagnosable denial, audit, and observability behavior; and
7. test coverage and adversarial cross-object, cross-tenant, stale-state, and alternate-path cases.

## Core Exposition

### Treat identifiers as selectors, never capabilities by accident

A route such as `GET /orders/{id}` receives a claim from the client: “select the order named by this value.” It does not receive proof that the caller owns, may see, or may mutate that order. The same is true when the ID is a UUID, hash, slug, cursor, GraphQL global ID, foreign key, object-store key, or encrypted-looking blob.

Unpredictable IDs are still useful. They reduce opportunistic enumeration, prevent leakage of business volume, and can make accidental cross-object access less likely. They are defense in depth, not the authorization mechanism. A reference can leak through logs, links, browser history, analytics, referrers, screenshots, notifications, support tickets, shared clients, or another API. OWASP explicitly recommends authorization on each function that uses client input to access a record even when random identifiers are used.

Some systems intentionally create capability URLs whose unforgeable token conveys limited authority. That is a different declared security model: the capability needs entropy, scope, expiry, revocation/attenuation, leakage analysis, secure transport/storage, and action binding. Do not accidentally convert every UUID into a bearer capability merely because it is hard to guess.

Inventory selectors beyond the obvious path. Examine query filters, body arrays, nested relation IDs, destination IDs, headers, pagination cursors, webhook subscription targets, filenames, signed download parameters, GraphQL nodes, RPC messages, events, and retry/idempotency records. The policy applies to the object reached, not to the syntax used to name it.

### Build a trusted authorization context

The decision begins with trusted facts. Derive authenticated subject and token/client from validated security context. Derive tenant from the subject's active membership/grant or an independently validated tenant selection—not merely `X-Tenant-ID` or a body field. Map the endpoint/resolver/command to a canonical action owned by the service. Load object attributes and relationships from authoritative storage.

A useful context records:

- real actor, effective/delegated subject, client/workload, and authentication assurance;
- selected tenant/organization and the grant that permits acting there;
- canonical action and sensitive properties involved;
- target object type/ID, parent/container, owner, classification, and current state/version;
- relationships such as owner, editor, member, approver, beneficiary, or assigned worker;
- environment such as time, network/device risk, purpose, emergency mode, and policy revision; and
- provenance/freshness for every security-relevant fact.

Request fields may identify which tenant or owner the caller wants to target, but the service must validate that target against trusted authority. Never replace the authenticated subject with a submitted `user_id`, accept `role=admin`, or use an unvalidated tenant claim as a database partition key. For delegated/support actions, preserve both actor and effective subject so policy and audit can distinguish “Alice acting for Bob” from Bob.

### Express subject–action–object policy explicitly

NIST SP 800-162 models ABAC as evaluating subject, object, requested-operation, and sometimes environment attributes against policy, rules, or relationships. Relationship-based access control makes edges such as `document:7#editor@user:alice` first-class and supports inherited relations through folders, teams, or organizations. Role-based access remains useful for coarse responsibility. Most APIs combine them.

Write policy using domain predicates, not controller accidents. For example, cancelling an order may require all of:

- authenticated context valid for the orders audience;
- coarse `orders.cancel` capability;
- active membership in the object's tenant;
- owner relationship, or explicit support delegation with approval;
- order state `open` and no legal/fraud hold;
- client eligible for cancellation and fresh assurance for high risk; and
- no emergency restriction.

The conjunction matters. `owner OR admin` is unsafe if “admin” accidentally bypasses tenant, state, legal hold, or separation of duties. Define precisely which predicates a privileged path may override and which invariants no role bypasses. Keep an explicit default deny when no rule applies or an input is unknown.

Policies need stable action and object schemas. Type-check or validate policy input so missing tenant or misspelled action does not become truthy, fall through to broad defaults, or select the wrong rule. Record policy owner, version, tests, rollout, and removal of deprecated decisions.

### Constrain retrieval to the authorized set

The safest common read pattern asks storage for “object with this ID visible to this context,” not “object with this ID, then perhaps check it.” A tenant/relationship predicate is part of the query or repository operation:

- `find_visible_order(context, id, action)` returns an authorized object or no result;
- `list_visible_orders(context, filters)` applies the same policy before pagination/counting;
- `update_cancellable_order(context, id, version, change)` constrains the affected row.

This reduces accidental disclosure and naturally supports concealed 404 behavior. It also makes an insecure raw lookup conspicuous in review. Repository APIs should require authorization context or expose raw access only inside narrow trusted domain/policy components. Avoid returning an unrestricted ORM query that later layers can widen or evaluate without policy.

Filtering is not enough when policy needs complex or remote facts. A PDP may make the decision after loading a minimal object, or return a query constraint/authorized ID set. The invariant is that no representation or effect escapes before authorization. Do not fetch a secret body merely to decide whether its public metadata is visible if a minimal policy projection suffices.

Lists, searches, counts, facets, aggregates, and pagination require the same authorized set. Filter before `COUNT`, sorting, cursor generation, aggregation, and response projection; otherwise even excluded rows leak existence, values, distribution, or timing. A client-supplied filter can narrow the authorized set, never widen it. Avoid “get all then filter in application” because it risks leaks, unstable pages, excess memory, and inconsistent counts.

### Authorize every graph edge, nested projection, and batch member

An authorized parent does not automatically authorize every child, attachment, owner profile, internal note, or linked payment. Define whether access inherits across each relationship and in which direction. Expansion parameters such as `include=customer,payment` are additional reads. GraphQL field/resolver authorization must cover node lookups, nested fields, aliases, fragments, connections, global IDs, subscriptions, and federation/entity resolvers.

For a batch, authorize every target and every action. Never authorize the first item and assume the rest share its tenant/owner. Choose semantics explicitly:

- **atomic:** reject or roll back the whole batch when any member is unauthorized;
- **filtered read:** return only authorized items when the contract makes omission safe;
- **per-item result:** report outcomes without leaking forbidden object existence; or
- **bounded job:** authorize the query/filter at submission and again or under a governed snapshot at execution.

Cap batch size and computational fan-out. A BOLA probe sent as a thousand-ID array is still an enumeration attack. Preserve input/output correlation without revealing which guessed IDs exist if concealment is required.

### Secure creation, mutation, transfer, and deletion

Creation has no existing target row, but it still has objects: the parent/container, proposed tenant/owner, linked resources, and new object's attributes. Authorize `create` on the container and every referenced object. Stamp tenant, creator, and immutable ownership from trusted context unless a separately authorized assignment action permits another value. Module 047 addresses the complementary danger of binding unapproved fields.

For updates, decide against both the existing object and proposed transition. An editor allowed to change `title` may not change `tenant_id`, `owner_id`, `classification`, approval state, or payment destination. Map request fields to a canonical command and explicit writable-field policy. Revalidate referenced objects such as destination accounts.

Transfers and relationship changes are security operations. Authorize the actor, source object, destination tenant/owner, target subject eligibility, and resulting invariants. Prevent the last owner from disappearing where policy requires one. Separation of duties may require a different approver; the initiator cannot satisfy both roles merely because both have broad permissions.

Deletion must cover soft-deleted rows, undelete, purge, tombstones, versions/history, attachments, search indexes, derived exports, and cascade effects. A hidden/deleted object is not public. A caller allowed to delete a parent may or may not be allowed to read every child or purge regulated history.

### Bind the decision to the protected effect

The common sequence “load, authorize, wait, update by ID” has a TOCTOU gap. Ownership, tenant, state, hold, delegation, or version can change between check and use. For a mutation, keep decision and write in one transaction and encode stable policy predicates in conditional data access where practical. Require the expected version and inspect affected-row count.

For example, cancellation can update only where ID, tenant, owner/delegation constraint, `state='open'`, and expected version still match. Zero rows means absent, concealed, stale, or no longer eligible according to the public error contract. If policy depends on an external relationship service, use a bounded consistency token/snapshot, recheck before commit, or design a domain command whose authoritative owner serializes both facts.

Authorization does not replace domain concurrency. Two individually authorized actions can conflict. Use optimistic versions, locks, serializable invariants, or idempotent commands as the domain demands. For high-risk external effects, bind approved transaction details to execution and revalidate immediately before dispatch.

Google's Zanzibar paper highlights causal ordering for authorization changes: a user should not remove access and then observe a later operation authorized from older relationship data. Not every service needs a global relationship system, but every service must state its consistency and staleness contract. “Eventually consistent” is incomplete unless the maximum exposure, sensitive-operation behavior, and recovery mechanism are explicit.

### Use multiple enforcement layers without confusing ownership

Application/domain policy usually has the richest action and state meaning. A central PDP can provide consistent language, versioning, decision IDs, and relationship evaluation. A gateway can validate credentials and coarse route policy. Database row-level security can constrain rows even if an application query forgets a predicate. These are complementary PEPs.

Defense in depth fails when teams assume another layer owns the decision. The service that owns the domain operation remains accountable for a complete decision. Gateway route authorization cannot see all objects or new state. Database row policy may not understand domain commands, external relationships, nested artifacts, or field transitions.

PostgreSQL row security, for example, can default-deny visible/modifiable rows when enabled and no applicable policy exists, with separate `USING` and `WITH CHECK` expressions. But superusers, `BYPASSRLS` roles, and normally table owners bypass it; `TRUNCATE` and some table operations are outside row policies. Connection pooling also requires trustworthy per-request context setup/reset. Treat RLS as a powerful governed layer, not an automatic proof of end-to-end authorization.

Central PDP calls add latency and availability dependencies. Co-located policy lowers network failure but can drift. Cached decisions need keys containing every relevant subject/client/tenant/action/object/version/policy fact and expiry bounded by revocation needs. On missing policy data, timeouts, parse failures, or unknown actions, fail closed for protected access and expose a controlled availability error rather than allow.

### Preserve authority through caches, artifacts, and asynchronous work

A representation authorized for Alice must not be cached under only `/orders/7` and served to Mallory. Use private/no-store rules where needed or vary the key by stable authorization dimensions and policy/data versions. Be wary of CDN normalization, GraphQL response caches, memoized PDP decisions, and shared process caches. Cache denial/existence cautiously to avoid stale access or enumeration differences.

Exports, reports, thumbnails, logs, snapshots, and object-store files are new protected objects. Record their tenant, creator/grant, source classification, purpose, expiry, and current download policy. A signed URL is a bearer capability: keep it narrowly scoped and short-lived, prevent it from authorizing a broader key prefix, and define revocation for sensitive data. Authorize both generation and download.

Async jobs must not become authority laundering. At submission, authorize job type, query, objects, destination, and limits. Persist immutable actor, effective subject, client, tenant, grant/policy snapshot or revision, and approved parameters—not a mutable request blob. At execution, either reauthorize under current policy or deliberately use a bounded snapshot whose semantics are documented. A service account's technical database reach must not become the user's business authority.

Events and webhooks also carry object references. Consumers authenticate the producer/channel, validate tenant and event type, then enforce their own local policy before exposing or mutating objects. A payload saying `owner_id=alice` is data, not automatically trusted authorization input.

### Design denials, audit, and observability together

RFC 9110 permits an origin server to use 404 instead of 403 to hide the existence of a forbidden target. Use a consistent contract. Return 401 for missing/invalid authentication where appropriate; use 403 when the caller may safely know the object/operation exists and different authority could help; use concealed 404 when existence is sensitive. Do not let response body, size, headers, timing, cache behavior, pagination count, or audit identifier undo concealment.

Internally distinguish absent, wrong tenant, relationship denied, state denied, stale version, and policy unavailable for safe diagnosis. Externally return stable problem types that do not enumerate policy or other principals. Do not list the exact owners, roles, or scopes an attacker needs.

Audit high-risk allows and meaningful denies with decision ID, actor/effective subject, client, tenant, canonical action, protected object pseudonymous/stable ID, result/reason class, policy revision, relevant state/version, request/trace ID, and timestamp. Minimize sensitive attributes and protect retention/access. Decision logs themselves can disclose relationship graphs and object existence.

Metrics should use bounded labels: decisions/result/reason/action/object type/policy revision, policy latency/errors, concealed denials, cross-tenant attempts, batch rejection, cache hit class, stale conflicts, and route-to-policy coverage. Never use raw tokens, user IDs, or arbitrary object IDs as metric labels. Alert on systematic ID walking, tenant switching, high denial ratios, newly unmapped actions, and privileged bypass use without treating every legitimate stale request as an attack.

### Verify policy and enforcement coverage independently

Policy-correctness tests ask whether the decision matches intended relationships, attributes, actions, states, and exceptions. Enforcement-coverage tests ask whether every route/resolver/job/event/storage path actually invokes the decision and obeys it. Both are necessary.

Generate a subject–client–tenant–action–object matrix with owner/non-owner, member/non-member, same/cross tenant, public/private, current/stale state, normal/privileged path, active/revoked relation, and allowed/forbidden field. Property tests can assert changing only an untrusted ID never crosses the authorized set; adding an unrelated role does not bypass tenant; filters never return objects outside a per-object oracle; and downscoping cannot add visibility.

Maintain a registry from OpenAPI operations, RPC methods, GraphQL fields/resolvers, job types, event handlers, storage routes, and support commands to canonical actions and PEPs. CI fails on unmapped new surfaces. Mutation tests deliberately remove/broaden checks and confirm the suite fails. Integration tests use two users in one tenant and two tenants, because single-user fixtures conceal horizontal failures.

The executable model makes the trusted tenant, capability, relationship, and state checks explicit. It returns concealed `deny:not_found` for absent, cross-tenant, and unrelated reads; production response policy may choose differently.

<!-- bijux-verify: {"id":"object-authorization-policy","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"read_owned=allow\nread_shared=allow\nread_cross_tenant=deny:not_found\ncancel_shared=deny:relationship\ncancel_owned_open=allow\ncancel_owned_shipped=deny:state\nvisible=order-1,order-2,order-4\n","stderr":""}} -->
```python
orders = {
    "order-1": {"tenant": "north", "owner": "alice", "editors": set(), "state": "open"},
    "order-2": {"tenant": "north", "owner": "bob", "editors": {"alice"}, "state": "open"},
    "order-3": {"tenant": "south", "owner": "alice", "editors": set(), "state": "open"},
    "order-4": {"tenant": "north", "owner": "alice", "editors": set(), "state": "shipped"},
}

alice = {"subject": "alice", "tenant": "north", "permissions": {"orders.read", "orders.cancel"}}

def decide(context, action, object_id):
    order = orders.get(object_id)
    if order is None or order["tenant"] != context["tenant"]:
        return "deny:not_found"
    can_see = order["owner"] == context["subject"] or context["subject"] in order["editors"]
    if not can_see:
        return "deny:not_found"
    if action not in context["permissions"]:
        return "deny:permission"
    if action == "orders.cancel" and order["owner"] != context["subject"]:
        return "deny:relationship"
    if action == "orders.cancel" and order["state"] != "open":
        return "deny:state"
    return "allow"

print("read_owned=" + decide(alice, "orders.read", "order-1"))
print("read_shared=" + decide(alice, "orders.read", "order-2"))
print("read_cross_tenant=" + decide(alice, "orders.read", "order-3"))
print("cancel_shared=" + decide(alice, "orders.cancel", "order-2"))
print("cancel_owned_open=" + decide(alice, "orders.cancel", "order-1"))
print("cancel_owned_shipped=" + decide(alice, "orders.cancel", "order-4"))
visible = [object_id for object_id in orders if decide(alice, "orders.read", object_id) == "allow"]
print("visible=" + ",".join(visible))
```

The executable evidence checks representative outcomes, not cryptographic validation, database isolation, complete graph policy, or deployment coverage. Those need separate integration, concurrency, and security testing.

## Definitions and Notation

Let $S$ be subjects, $K$ clients/workloads, $T$ tenants, $A$ canonical actions, $O$ protected objects, and $E$ environmental states. A trusted request context $c=(s,k,t,g,q)$ contains subject $s\in S$, client $k\in K$, selected tenant $t\in T$, validated grant/token context $g$, and assurance/context facts $q$.

For object $o$, let $state(o)$ be its authoritative current state and $rel(s,o,t)$ its current relationships. The decision

$$
D(c,a,o)=\operatorname{allow}(c,a,o,state(o))\in\{\text{allow},\text{deny}\}
$$

is total: unknown or missing facts produce deny. The authorized set for an action is $O_{c,a}=\{o\in O\mid D(c,a,o)=\text{allow}\}$. A selector $i$ resolves safely only when the result lies in that set. For a list query $F\subseteq O$, the returned object set is $F\cap O_{c,a}$, never $F\cup O_{c,a}$ and never client filter $F$ alone.

A **PEP** intercepts the attempted effect and enforces a result. A **PDP** computes a result from policy and attributes. A **policy information point** supplies trusted attributes/relationships; a **policy administration point** governs rules. These logical responsibilities may be colocated, but their ownership and failure behavior remain distinct.

**Horizontal escalation** accesses another peer's object; **vertical escalation** gains a more privileged action; **cross-tenant escalation** crosses an isolation boundary; **contextual escalation** performs an otherwise permitted action in a forbidden state, field, time, purpose, or client. BOLA often combines several.

## Mechanisms, Invariants, or Proof Structure

1. Inventory every object selector and protected effect across synchronous, asynchronous, storage, cache, and support surfaces.
2. Derive subject, client, tenant, action, assurance, and delegation only from validated or independently checked context.
3. Load minimal authoritative object state, attributes, and relationships with declared freshness and provenance.
4. Evaluate a total deny-by-default policy over coarse capability plus tenant, relationship, attributes, action, fields, state, and environment.
5. Resolve reads within the authorized set before projection, counts, pagination, expansion, aggregation, caching, or artifact creation.
6. For create/update/transfer/delete, validate the parent, current object, all references, allowed fields, and resulting state.
7. Bind high-risk decisions to effects with conditional writes, versions, transactions, consistency tokens, or reauthorization.
8. Enforce on every alternate path and preserve user authority through jobs, services, events, caches, and download capabilities.
9. Conceal existence according to one external contract while retaining protected internal decision evidence.
10. Test policy truth and PEP coverage separately, including adversarial IDs, tenants, batches, races, stale facts, and bypass roles.

The set construction proves a useful safety property under assumptions: if every returned object is selected from $O_{c,a}$, then every returned object satisfies $D(c,a,o)=\text{allow}$. It does not prove that $D$ represents the intended business policy, that its inputs are trustworthy/current, that all paths use the selector, or that a mutation remains authorized after the check. Those are separate evidence obligations.

For mutation, suppose a transaction changes object $o$ from version $v$ and state $s$ only when predicate $D(c,a,o)=\text{allow}$ and version equals $v$. If the authoritative data store evaluates the predicate and version with the write, the write cannot succeed on a different stored version under that operation's isolation semantics. External facts and side effects still require a stated consistency/binding mechanism.

## Alternatives and Trade-Offs

Checking after a raw lookup is flexible and can produce precise 403/404 diagnostics, but it makes omission easy and may load secrets before authorization. Authorized repository/query methods make safe behavior the easy path and conceal existence naturally, but complex policies may be hard to translate and must not diverge from the canonical PDP.

RBAC is compact for stable job functions but becomes coarse or explodes when tenant, ownership, object state, and delegation vary. ABAC expresses current attributes and environment but depends on schema, provenance, freshness, and explainability. ReBAC naturally models sharing and inheritance but adds graph consistency, cycle, depth, and operational concerns. A layered hybrid is common: role/capability gates an action, relationship and attributes gate the object.

Central policy services improve consistency, relationship reuse, and governance but add latency, availability, privacy, and consistency dependencies. Embedded policy is fast and deploys with the service but can fragment semantics. Compiled/query-filter policy can make list enforcement efficient but needs semantic equivalence tests against per-object decisions.

Database row security gives strong proximity to data and catches missed predicates, yet privileged bypass, pool context, migrations, non-row artifacts, domain transitions, and administrative operations require careful control. Application-only enforcement understands domain actions but one forgotten path is sufficient. Use layers with explicit accountability and test each bypass.

Returning 404 conceals existence but can confuse authorized support and clients; 403 is clearer but may confirm sensitive objects. Choose by resource sensitivity and caller relationship, keep timing/cache/body behavior aligned, and provide internal decision IDs. Random IDs reduce scanning efficiency but never replace either choice.

Reauthorizing async work at execution honors current revocation but can make an accepted job fail later. Snapshot authority provides reproducibility but prolongs access after revocation. Choose per action risk, disclose semantics, bound snapshot duration, and make cancellations/retries idempotent. A sensitive export usually merits current reauthorization at generation and download.

## Failure Modes and Misconceptions

- **“The user is authenticated.”** Authentication establishes an identity/context, not authority over every object.
- **“The endpoint requires the right scope.”** A scope permits a class of actions; it does not decide owner, tenant, state, or fields.
- **“The ID is a UUID.”** Unpredictability reduces guessing but leaked or observed references remain usable selectors.
- **“We compare token subject to body user ID.”** The body is attacker controlled, and ownership may involve tenants, groups, delegation, or parents.
- **“The UI never exposes that action.”** Attackers call APIs directly and alter hidden, disabled, cached, or replayed requests.
- **“The gateway checks authorization.”** It rarely owns current object relationships and domain transition rules.
- **“Lists are filtered, so detail is safe.”** Detail, export, nested, storage, GraphQL node, history, and support paths can bypass list filters.
- **“Admins bypass everything.”** Privileged operations still need tenant, purpose, state, separation, audit, and immutable safety invariants.
- **“One policy call secures the batch.”** Each object/action and the batch outcome contract require authorization.
- **“We checked before updating.”** A later unqualified write can race, change a different version, or use altered external facts.
- **“RLS solves authorization.”** Owners/bypass roles and non-row/domain paths can evade it; configuration and context hygiene are part of the control.
- **“A signed URL is safe forever.”** It is a bearer capability whose leak, expiry, action, prefix, and revocation determine risk.
- **“The service account is trusted.”** Technical reach must be narrowed by the initiating subject's business authority.
- **“403 and 404 are cosmetic.”** Differential status, timing, sizes, counts, and caches can become an enumeration oracle.
- **“A policy unit test proves coverage.”** It says nothing about routes, jobs, or resolvers that never invoke the policy.

## Worked Examples

### Example 1

**Situation:** Mallory has `documents.read` and changes `/documents/8f...` to Alice's observed UUID. **Reasoning:** Authentication and permission validate the caller and action class. UUID form adds no relationship. The repository queries the ID inside Mallory's visible-document set; no row returns. The API emits the concealed not-found response and an internal relationship-denial reason. **Conclusion:** object selection is constrained by policy; identifier opacity is only defense in depth.

### Example 2

**Situation:** Alice belongs to tenants north and south; the request header says south, while order 7 belongs to north. **Reasoning:** The header is a selection request, not trusted context. The service validates Alice's active membership and requested grant, constructs one tenant context, and requires the object's tenant to match it. It never unions visibility across both memberships or trusts a body `tenant_id`. **Conclusion:** multi-tenant users still operate within one explicit validated tenant boundary per decision.

### Example 3

**Situation:** An editor can update document content and submits `owner_id=editor` alongside a title change. **Reasoning:** Existing-object authorization permits `document.edit`, but proposed-state authorization maps only `title` and `body` as writable. Ownership transfer is a separate action requiring current owner, eligible recipient, perhaps approval, and an atomic invariant. The unknown/protected field is rejected rather than silently persisted. **Conclusion:** object authorization must cover the resulting state, not merely access to the current row.

### Example 4

**Situation:** A batch delete contains nine owned files and one file in another tenant. **Reasoning:** The service evaluates every file under canonical `files.delete`. Its contract is atomic, so one concealed denial rejects the entire transaction; none are deleted. A per-item API would need non-enumerating outcomes and independent idempotency. Checking only the first item would let the tenth ID cross tenants. **Conclusion:** batch authorization is universal quantification over members plus an explicit outcome contract.

### Example 5

**Situation:** Alice opens an order, loses ownership, then submits cancellation using the screen's stale version. **Reasoning:** A prior UI check has no force. The mutation condition includes ID, tenant, current owner, `state=open`, and expected version. Ownership/version no longer match, so zero rows change. The service returns its concealed/stale contract and does not dispatch cancellation. **Conclusion:** a conditional transactional effect closes the ordinary stale-check gap.

### Example 6

**Situation:** A GraphQL query may read a project but expands `members { email }` and `billingAccount { number }`. **Reasoning:** Project visibility does not imply each field/edge. Resolvers require `members.read_email` with organization relationship and `billing.read` with finance relationship. Cost and batching controls prevent one query from probing thousands of nodes. Unauthorized nodes/fields follow declared nullable/error semantics without revealing hidden counts. **Conclusion:** graph authorization applies at each semantically protected edge and field.

### Example 7

**Situation:** A report job is authorized Monday, the user is removed Tuesday, and it runs Wednesday. **Reasoning:** The job record preserves actor, client, tenant, approved query, policy revision, and authority mode. Because the report contains sensitive current data, execution reauthorizes and fails after revocation; no artifact is generated. A low-risk immutable historical receipt might instead use a short bounded snapshot. **Conclusion:** async authority semantics must be intentional, persisted, and risk-specific.

### Example 8

**Situation:** Alice's authorized invoice response is stored in a shared cache under `/invoices/7`; Bob requests the same path. **Reasoning:** Origin policy never runs on a cache hit, so the cache is a PEP. An object-only key crosses subjects/tenants. The service marks the response private/no-store or keys and validates by tenant, authorization class, representation, object version, and bounded policy revision. **Conclusion:** caching can reintroduce BOLA after a correct origin decision.

### Example 9

**Situation:** A PostgreSQL-backed service enables RLS and assumes all paths are safe. A maintenance connection uses a table-owner role. **Reasoning:** PostgreSQL documents that owners normally bypass RLS and `BYPASSRLS` roles always do. If an API or job uses that connection, its unqualified query can expose every tenant. Separate runtime roles, force RLS where appropriate, lock pool context reset, retain application action policy, and test privileged paths. **Conclusion:** RLS is defense in depth whose bypass semantics must be part of the threat model.

### Example 10

**Situation:** A private photo API returns 403 for an existing forbidden ID in 8 ms and 404 for an absent ID in 2 ms. **Reasoning:** Status/body concealment is defeated by timing. The authorized lookup path, error serialization, cache behavior, and bounded work should be sufficiently uniform; rate limits and anomaly detection reduce high-volume probing. Internal logs still distinguish absence from denial under restricted access. **Conclusion:** existence concealment is an end-to-end observable behavior, not just a status-code substitution.

## Cross-Program Connections

- **Security Engineering:** reference monitoring, complete mediation, least privilege, capability leakage, confused deputy, and side channels explain why every path and observable matters.
- **Identity and Access Management:** subject lifecycle, tenant membership, delegation, role/group provenance, revocation, and assurance supply trusted policy inputs.
- **Database Engineering:** query predicates, row-level security, transactions, isolation, constraints, and versioned conditional writes bind policy to data effects.
- **Distributed Systems:** replicated relationships, caches, async work, causal consistency, retries, partial failure, and revocation latency bound decision freshness.
- **Graph Theory:** relationship-based authorization evaluates typed edges, inheritance, reachability, cycles, and depth over subject/object graphs.
- **Programming Languages:** typed policy inputs, total functions, exhaustive action matching, effect boundaries, and property tests reduce authorization ambiguity.
- **Privacy Engineering:** data minimization, purpose, object existence, counts, logs, and derived artifacts determine what denial and telemetry may reveal.
- **Systems Engineering:** authorization is an emergent property of identity, policy, storage, caches, jobs, operations, and recovery—not one middleware call.

## References

1. OWASP Foundation. [API1:2023 Broken Object Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/). OWASP API Security Top 10, 2023. Checked 2026-09-01.
2. OWASP Foundation. [Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html). OWASP Cheat Sheet Series. Checked 2026-09-01.
3. Hu, V., Ferraiolo, D., Kuhn, R., et al. [NIST SP 800-162: Guide to Attribute Based Access Control Definition and Considerations](https://csrc.nist.gov/pubs/sp/800/162/upd2/final). NIST, updated August 2019. Checked 2026-09-01.
4. Pang, R., Caceres, R., Burrows, M., et al. [Zanzibar: Google's Consistent, Global Authorization System](https://research.google/pubs/zanzibar-googles-consistent-global-authorization-system/). USENIX ATC, 2019. Checked 2026-09-01.
5. Fielding, R., Nottingham, M., and Reschke, J. [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html). IETF, June 2022. Checked 2026-09-01.
6. PostgreSQL Global Development Group. [PostgreSQL 17: Row Security Policies](https://www.postgresql.org/docs/17/ddl-rowsecurity.html). PostgreSQL documentation. Checked 2026-09-01.

## Exercises

### Exercise 1

For a shared document service, define the trusted context and allow predicate for read, edit content, share, transfer ownership, delete, restore, and purge. Include tenants, owner/editor/viewer relationships, state, legal hold, and privileged support.

### Exercise 2

Trace an authorized set for Alice when a requested list contains owned, shared, unrelated, cross-tenant, archived, and legally held objects. Then derive batch-delete behavior under atomic and per-item contracts.

### Exercise 3

Diagnose a service that loads `invoice = get(id)`, checks `invoice.tenant_id == request.tenant_id`, caches by ID, and later runs `UPDATE invoices WHERE id = ?`. Give a durable implementation and test design.

### Exercise 4

Compare embedded policy, a central relationship/attribute PDP, and PostgreSQL RLS for a multi-service collaboration platform. Propose explicit ownership, layering, consistency, failure, and rollout rules.

### Exercise 5

Design object authorization for an unfamiliar scientific instrument API where researchers schedule instrument time, delegate runs, stream live results, create derived datasets, embargo publications, and use emergency operators.

## Answers to the Exercises

### Answer 1

Context contains validated actor/effective subject, client, selected active tenant membership, assurance, purpose/support approval, action, policy revision, and current time. Objects contain tenant, owner, viewer/editor edges (possibly inherited from folder/team), classification, active/archived/deleted state, version, and legal hold. Read requires same tenant plus public/viewer/editor/owner relationship and compatible classification; edit requires editor/owner, active state, and only content fields; share requires owner or governed manager and validates recipient membership plus relationship ceiling; transfer requires current owner, eligible target, fresh assurance, no legal hold, and preserves at least one owner atomically. Delete requires owner and allowed state; restore requires deletion authority/current tombstone; purge additionally requires retention expiry and no hold. Support never becomes global implicit owner: it needs just-in-time case-bound approval, tenant/object scope, non-overridable holds, short expiry, and actor/effective-subject audit. Unknown facts deny.

### Answer 2

Let the request set be `{owned-active, shared-active, unrelated, cross-tenant, owned-archived, owned-held}`. For `read`, assuming policy permits archived and held viewing, Alice's authorized set is owned-active, shared-active, owned-archived, and owned-held; unrelated and cross-tenant are removed before sorting/count/pagination. For `delete`, suppose only owned active objects without holds qualify: only owned-active remains. Under an atomic batch delete containing all six, universal authorization fails and no object changes. Under per-item semantics, the service deletes owned-active and returns bounded results for the others without distinguishing absent from forbidden where existence is concealed; retries use item idempotency and do not turn partial completion into an enumeration oracle.

### Answer 3

The request tenant is untrusted, the raw load may disclose secrets, an ID-only cache crosses authorization contexts, and the later ID-only update has both BOLA and TOCTOU gaps. Derive tenant from validated membership/grant. Replace the repository API with an authorized minimal lookup or conditional mutation over ID, trusted tenant, subject relationship, action/state, and expected version; validate proposed fields/references; execute in one transaction and require exactly one affected row. Use private caching or a key containing tenant/authorization class/object and policy/data versions, with revocation-bounded expiry. Test two users in one tenant, two tenants, guessed/leaked UUIDs, wrong request tenant, absent/forbidden timing/status, cache orderings, stale ownership/version/state, batch/nested/export paths, and mutation tests that remove each predicate.

### Answer 4

Make the domain service accountable for canonical actions, proposed transitions, and protected effects. Use an embedded typed PEP/client library in every service so missing context/actions deny and decisions are consistently invoked. A central PDP owns cross-service subject–object relationships, inheritance, policy revisions, decision IDs, and causal/freshness semantics; clients have strict timeouts, bounded cache keys, and fail closed, with a controlled availability path. PostgreSQL RLS is a data-layer backstop for tenant/row visibility and `WITH CHECK`, using non-owner/non-`BYPASSRLS` runtime roles, forced policies where appropriate, and verified pool context reset. It does not replace field/state policy or artifacts. Roll out shadow decisions with privacy-safe mismatch logs, prove per-object/filter equivalence, canary enforcement, retain rollback to the last safe deny-aware revision, and test outages, stale relations, owner/bypass connections, migrations, jobs, and every contract operation.

### Answer 5

Model instruments, schedule slots, run plans, live streams, raw/derived datasets, projects, embargoes, and publication artifacts as separate protected objects with explicit edges: project member, principal investigator, instrument operator, delegated runner, dataset steward, and emergency operator. Schedule requires project allocation, qualified researcher, instrument compatibility, conflict-free slot, quota, and current safety training. Delegation is action/object/time bounded and preserves initiator/delegate. A run revalidates plan, slot, operator, safety state, and instrument; live stream subscriptions reauthorize over their lifetime. Derived datasets inherit classification/provenance but receive explicit ownership and sharing; embargo policy gates metadata, counts, downloads, and publication until release. Emergency access requires declared incident, just-in-time operator authority, immutable audit, narrow commands, and cannot bypass physical safety interlocks. Jobs preserve actor/project/approved inputs and reauthorize sensitive execution/download. Tests cross projects, institutions, instruments, delegation expiry, embargo boundary, cached streams, replayed capabilities, partial datasets, incident end, and concurrent schedule/ownership changes.
