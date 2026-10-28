---
module_id: API-047
program: API & Service Engineering
level: 1
module_number: 47
title: Mass Assignment and Overposting
status: complete
last_verified: 2026-09-01
---

# Mass Assignment and Overposting

## One-Page Review

### Governing question

How should an API translate untrusted structured input into a narrowly authorized domain command without letting convenience binding expose new or sensitive object properties as write authority?

### Essential definitions

- **Mass assignment** is automatic copying of request fields into object properties, often by a framework binder, serializer, ORM, or generic map/update operation.
- **Overposting** is a client submitting fields beyond the operation's intended writable contract; it becomes exploitable when those fields influence protected state.
- A **request DTO/input model** is a transport-specific closed representation containing only fields accepted by one operation/version.
- A **command** names an intended domain action with explicit parameters; it is not a serialized persistence entity.
- A **server-owned field** is derived or controlled by trusted server logic, such as tenant, owner, role, price, balance, approval, state, timestamps, or version.
- A **write allowlist** is the exact set of properties or patch paths this actor/action/state may change.
- An **unknown property policy** defines whether undeclared input is rejected, ignored, or preserved; command APIs normally reject it.
- **Transition authorization** decides whether the current object may become the proposed new state, beyond validating individual field types.

### Central model, mechanism, or theorem

For context $c$, operation $a$, current object $x$, payload $p$, and writable path set $W(c,a,x)$, accept only when

$$
\operatorname{accept}(c,a,x,p)=V_{schema}(p)\land paths(p)\subseteq W(c,a,x)\land A(c,a,x,x')\land I(x'),
$$

where $x'=T_{a}(x,p,c)$ is produced by an explicit operation mapper, $A$ authorizes the transition, and $I$ checks domain invariants. The mapper takes server-owned values from $c$ or authoritative data, not from similarly named payload fields.

The subset test is necessary but insufficient: an allowed `quantity` can still be negative, an allowed destination can name another tenant, and two individually valid fields can form an invalid transition.

### Critical invariants

External request types are not domain/persistence entities. Each create, replace, patch, transition, administrative, and bulk operation has its own closed writable contract. Allowlist beats a blacklist because future internal fields remain non-writable by default. Unknown properties and aliases are handled deterministically before domain mutation. Server-owned identity, tenant, ownership, privilege, lifecycle, money, audit, concurrency, and derived fields never come from ordinary input. Nested paths, collection members, relationship connect/disconnect operations, JSON Patch `path` and `from`, and merge-patch deletion receive the same property authorization. Missing, explicit `null`, default, empty, and remove remain distinct. The final proposed state is validated and authorized atomically against the current version. Persistence writes explicit columns/effects. Response schemas independently prevent excessive exposure. Tests prove every new domain field is denied until deliberately added to an operation contract.

### Common failures

Deserializing JSON directly into an ORM/domain entity; spreading `request.body` into a model; calling generic `update(payload)`; relying on the UI to omit `is_admin`; blacklisting today’s sensitive names; sharing a read model as the write model; using one DTO for create and update; ignoring unknown fields silently; assuming validation means authorization; accepting client tenant/owner/price/state/version/timestamps; allowing nested relationship IDs or `_destroy`; treating PATCH missing and null alike; authorizing a JSON Patch destination but not its source; letting a binder accept case/alias variants; saving a detached full entity with defaulted excluded fields; and adding an internal property that silently becomes writable.

### Compact example

A profile endpoint intends to accept `display_name` and `locale`. An attacker adds `role: "admin"` and `tenant_id: "victim"`. The closed input schema rejects both unknown fields before any entity is built. The mapper constructs `UpdateProfile(display_name, locale, expected_version)` and takes subject/tenant from validated context. The domain object changes only those two properties under a version check. **Conclusion:** the safe boundary grants exactly one command vocabulary, not generic write access to whatever the model happens to contain.

### Connections

[Object-Level Authorization](046-object-level-authorization.md) decides whether the caller may act on the target object, [Request Parsing and Validation](032-request-parsing-and-validation.md) validates the declared input shape, and [Concurrency Control at the API Boundary](038-concurrency-control-at-the-api-boundary.md) binds changes to a current version. [Enumeration and Data Exposure](../ROADMAP.md) next secures what can be inferred or returned.

## Governing Question

When frameworks can automatically populate rich objects from arbitrary client input, how does the service ensure that the writable API surface is an intentional, action-specific subset of the internal state model now and after the model evolves?

## Why This Matters

Automatic binding removes repetitive code: deserialize a body, populate properties with matching names, and save. The same convenience can erase the security boundary. Internal models often contain fields that were never shown in the UI—`role`, `approved`, `owner_id`, `tenant_id`, `price`, `balance`, `status`, `deleted_at`, `risk_score`, `email_verified`, or relationship collections. A caller can inspect responses, schema, client code, error messages, source, naming conventions, or simply fuzz likely names.

OWASP API3:2023 unifies unauthorized property reading and writing as Broken Object Property Level Authorization. Mass assignment is the write-side failure: the server has authorized access to an object or function but has not authorized each property transition. It can escalate privilege, cross tenants, bypass payment/approval, change ownership, suppress moderation, or corrupt audit and lifecycle state.

The hazard grows over time. A blacklist may block `is_admin` today, then a migration adds `role`, `account_type`, or nested `permissions`. Generic binding makes the new field writable without an API design decision. An allowlisted request DTO makes the opposite default: new internal fields do nothing at the external boundary until a developer intentionally specifies parsing, validation, authorization, mapping, documentation, tests, and migration behavior.

This is not merely serializer configuration. A field can be syntactically valid but unauthorized for this actor or state. Several allowed fields can produce an illegal transition. PATCH formats introduce deletion, array, pointer, ordering, and missing/null semantics. Persistence tools can overwrite excluded fields with defaults. Durable protection is a pipeline from closed transport schema to explicit command to authorized domain transition to explicit persistence effect.

## Prerequisites and Retrieval

Retrieve JSON/object parsing, request validation, DTOs/view models, domain entities, command methods, object/property authorization, least privilege, allowlist versus blocklist, create/PUT/PATCH semantics, JSON Merge Patch and JSON Patch, null/missing/default, JSON Pointer, nested relationships, optimistic concurrency, database constraints, ORM change tracking, schema evolution, API error semantics, audit, and fuzz/property testing.

Before designing an input, retrieve every internal field and relationship, server- versus client-owned provenance, per-action writable fields, actor/client/state differences, type/range/format validation, cross-field/domain invariants, create/update/replace/patch behavior, unknown/duplicate/alias/case policy, content types and parser configuration, nested/collection limits, relationship authorization, version/precondition source, response model, serializer/binder/ORM defaults, generated clients, old consumers, audit/redaction, and tests that detect contract drift.

## Learning Objectives

By the end of this module, you should be able to:

1. distinguish mass assignment mechanics from overposting attacks and property authorization;
2. separate transport DTOs, commands, domain objects, persistence models, and response representations;
3. derive per-operation writable-path allowlists and trusted server-owned values;
4. implement safe create, PUT, merge-patch, JSON Patch, nested, relationship, and bulk semantics;
5. validate and authorize the entire proposed state under concurrency;
6. use framework protections without depending on fragile binder or ORM defaults; and
7. test unknown fields, aliases, nested paths, lifecycle drift, and dangerous new model properties.

## Core Exposition

### See the binding pipeline as a security boundary

Input passes through several mechanisms: HTTP body parsing, media-type selection, JSON decoding, name/alias normalization, type coercion, model binding, validation, mapping, domain behavior, ORM change tracking, and persistence. Any stage that copies arbitrary keys toward mutable state can create mass assignment.

Common dangerous shapes include `Entity(**body)`, object spread/merge, reflection setters, generic mapper libraries, ORM `create(body)`/`update(body)`, and “patch every non-null property.” The issue is not that automation exists; it is that the set of client-controlled targets is inferred from internal structure rather than declared by the API operation.

Draw four separate types even if the implementation language makes them concise:

1. **Request DTO:** external names/types/presence for this operation and version.
2. **Command:** canonical domain intent and explicit validated parameters.
3. **Domain object:** complete state and methods enforcing transitions/invariants.
4. **Persistence model:** storage representation, keys, metadata, and change tracking.

A fifth response DTO controls readable properties. Reusing any one type for all five roles couples public writable/readable surfaces to internal evolution. Code generation does not change the boundaries; generate different request and response types from different schemas.

### Derive a per-operation writable contract

Start from a domain action, not the entity's property list. Registration may accept email, display name, locale, and password while deriving user ID, tenant invitation, role, verification, and timestamps. Profile update may accept display name and locale but not email. Email change is a separate command with reauthentication and verification. Administrative suspension is another command with reason and audit.

For each operation record:

- external field/path and exact type/presence/null/default semantics;
- business meaning and domain command parameter;
- actor/client/tenant/state eligibility;
- validation, normalization, and authoritative lookup;
- whether the value is client-proposed, server-derived, or immutable;
- cross-field and resulting-state invariants;
- version/precondition and idempotency behavior;
- audit/redaction and response projection; and
- introduction/deprecation/compatibility history.

The allowlist can be static for most operations and further narrowed dynamically. An owner might edit `display_name`; a verified enterprise administrator might also set a governed classification, while neither may set `tenant_id`. Dynamic authorization should narrow a known schema, not let policy invent arbitrary internal property names supplied by a client.

Choose action-shaped endpoints when fields represent lifecycle transitions: `POST /orders/{id}:cancel` with a reason is clearer than `PATCH {"status":"cancelled"}`. Commands centralize prerequisites, side effects, audit, and allowed state transitions. Generic CRUD is appropriate only when the resource truly is client-owned data with documented replacement semantics.

### Prefer closed allowlists and request DTOs over blacklists

A blacklist must name every field that is or will become sensitive. It loses when a model gains `superuser`, `credit_limit`, `moderation_state`, a naming alias, or nested relationship. An allowlist needs only the stable intended input vocabulary; new internal fields are denied by default.

OWASP recommends allowlisting bindable non-sensitive fields and using DTOs. Rails Strong Parameters requires explicit permission before Active Model mass assignment. Microsoft's ASP.NET Core documentation recommends view models for overposting protection and warns that some binding attributes affect form model binding but not JSON/XML input formatters. These framework details illustrate a general rule: verify the exact parser/binder path used by the endpoint; an annotation on the wrong path is no protection.

Request DTOs are necessary architecture, not magic. A DTO that includes `is_admin` “for reuse” remains dangerous. A mapper that reflects every DTO property into an entity recreates coupling. A loose `metadata: object` field can hide arbitrary privileged subkeys. Define closed nested schemas and explicit mapping.

Blocklists can add defense in depth around especially dangerous fields, and persistence/database rules should reject impossible privilege changes. They are not the primary boundary. If an allowlist and blocklist disagree, deny and treat the mismatch as a configuration error.

### Reject unknown, ambiguous, and duplicate properties deliberately

For command/write payloads, rejecting undeclared properties is usually safer than silently ignoring them. It catches attacker probes, client typos, stale names, and server/client contract drift. Ignoring `is_admin` may be secure today, but tells a buggy client its request succeeded when part did nothing; after a later schema change, the same field may start working unexpectedly.

Strictness has a compatibility cost. A new client sending a new optional field to an old server will fail, so version negotiation, capability discovery, or coordinated rollout may be needed. “Tolerant reader” guidance fits descriptive event/data formats better than authority-changing commands. When unknown preservation is a real requirement, isolate it in a namespaced extension map with size/type limits and guarantee it cannot affect routing, policy, queries, templates, or domain behavior without separate validation.

Define duplicate-member behavior before binding. JSON parsers differ on first-wins, last-wins, or rejection; a security layer and application can interpret different values. Reject duplicates where the stack permits or ensure one canonical parse is shared. Define case sensitivity, Unicode normalization, snake/camel aliases, prefix/nested syntax, and form/query/body precedence. Attackers try `isAdmin`, `is_admin`, `IsAdmin`, nested equivalents, and duplicate aliases.

Validate the exact `Content-Type`; otherwise an endpoint protected for form binding may accept JSON through a different input formatter. Bound object depth, member count, string/array size, numeric range, and parser work so schema validation does not become resource exhaustion.

### Keep server-owned values out of ordinary payloads

Server-owned fields include identifiers, subject, tenant, creator/owner, roles/permissions, lifecycle/approval/moderation state, prices/totals/balances, risk/verification, timestamps, audit actor, row version, deletion flags, and derived aggregates. The client may sometimes propose a related value, but that uses a distinct authorized operation.

Take trusted context values directly from the validated request/session and authoritative records. Do not accept `owner_id` and compare it to the same client-supplied `user_id`. Compute price from the current catalogue, total from validated lines, tenant from membership/grant, and status through domain transition methods. Store audit actor from security context, not `updated_by` in JSON.

Concurrency versions are usually supplied through a defined precondition such as `If-Match` or an explicit command field, but the client cannot choose the new version. Validate the expected version against the current object and let persistence advance it. Timestamps may be client domain facts only when the API names them as such (for example, `observed_at`); they are not substitutes for server `created_at`/`updated_at`.

Immutability needs enforcement beyond omission. A raw SQL/ORM path, import, admin tool, or migration can still alter tenant/owner. Use domain encapsulation, explicit repository effects, database constraints/triggers where appropriate, separated privileges, and audit. Define rare recovery/transfer commands instead of making protected fields generally mutable.

### Separate type validation, property authorization, and transition invariants

Schema validation answers whether submitted data has allowed names, types, formats, presence, and bounds. Property authorization answers whether this context may propose each property/action. Object authorization answers whether it may affect this object. Domain validation answers whether the complete transition is legal. All are required.

An allowed `quantity` with integer type can be zero or exceed stock. An allowed `destination_account_id` can identify another tenant. Start/end times can each be valid while ordered incorrectly. `discount` and `coupon` may be mutually exclusive. A role administrator may assign some roles but not one equal/higher than their own. Validate authoritative references and the resulting object, not just independent input fields.

Apply changes to a candidate or call a domain method without persisting, then authorize/check invariants against current and proposed state. Persist atomically with the expected version. Do not partially mutate an ORM entity, trigger observers, or send side effects before the whole input and transition succeeds. On failure, no protected field or side effect remains changed.

Errors should identify safe client-correctable schema problems without echoing secrets or advertising hidden fields. For an unknown ordinary field, a JSON Pointer/name is often useful. For a guessed privileged field, the same generic unknown-property response avoids confirming internal state. Internally log a bounded reason and request/schema version; never log passwords, tokens, full payment data, or arbitrary payloads.

### Define create and replacement semantics independently

Create is especially exposed because frameworks often construct an entity directly. The DTO should contain only client-proposed creation facts. The application assigns ID, tenant, creator, safe initial state, prices, timestamps, version, and defaults. Defaults are server policy, not client-overridable convenience.

Validate every referenced parent, owner candidate, product, plan, or relationship under object authorization. A caller allowed to create a child in folder A cannot submit `folder_id=B`. A public signup cannot submit an invitation-derived tenant or enterprise role without redeeming a validated one-time grant.

PUT conventionally represents replacement of the resource representation, but the public representation may contain read-only/server-owned fields. Define whether omitted writable fields reset, become null, use defaults, or invalidate the request. Never deserialize PUT into a complete persistence entity and save all columns. Construct the replacement of client-owned state while preserving/recomputing server-owned state and checking version.

If most fields are server owned and updates are action-specific, PUT may be a poor interface. Several small commands can be safer and clearer than pretending the entire domain entity is replaceable.

### Make PATCH path and presence semantics explicit

For an ordinary partial-update object, the service must distinguish absent (“leave unchanged”), explicit `null` (“set null” or “remove,” if permitted), empty values, and defaults. Languages that deserialize absent and null to the same zero value need presence wrappers, optional-field types, raw token inspection, or a patch-specific DTO.

RFC 7386 JSON Merge Patch defines null as removal and recursively merges object members; arrays are replaced as wholes, and a non-object patch replaces the whole target. The server remains responsible for authorizing changes. Compute affected canonical paths, reject unknown/protected paths, apply to a candidate client-writable projection, validate the resulting state, then map to a domain command. Do not run generic merge patch over a persistence entity containing secrets and server fields.

RFC 6902 JSON Patch sequences `add`, `remove`, `replace`, `move`, `copy`, and `test` operations over JSON Pointer paths. Validate operation type, destination `path`, source `from` for move/copy, pointer escaping/canonicalization, array indices/`-`, operation count, and intermediate/final states. A move from `/role` to `/display_name` reads/removes a protected source even if the destination is writable. Operations are ordered, so authorize each effect and validate the final domain transition; apply atomically or fail the entire document as the operation contract specifies.

Patch documents operate on a declared public writable representation, not necessarily the response or storage shape. Version the path vocabulary. If a response field is renamed, do not silently make both internal aliases writable.

### Guard nested objects, relationships, collections, and bulk input

Nested input multiplies paths. A safe parent field does not authorize every child property. Define closed schemas at every level, depth and cardinality bounds, and per-path authorization. Watch framework conventions such as nested attributes, dotted keys, bracket syntax, `_destroy`, `connect`, `disconnect`, `set`, `upsert`, or foreign-key arrays; each can create/delete relationships or objects.

Treat relationship changes as domain commands. Connecting a user to a team requires authority over the team, eligible target user, role ceiling, tenant compatibility, and resulting constraints. A submitted child ID is an object reference, not proof of authority. Server-generated collection elements need their own IDs/ownership.

For arrays and bulk updates, authorize every element and define atomic, per-item, or filtered semantics. Limit counts and reject duplicate IDs/conflicting changes. Prevent one element from changing a protected field through an alternate shape. If two updates target the same object, define ordering or reject ambiguity.

Maps/dynamic metadata require special caution. Permit only a namespaced key grammar, scalar/structured value schema, quotas, and prohibited prefixes. Never later interpolate metadata into database columns, policy attribute names, template code, object paths, or configuration without a second trusted interpretation boundary.

### Persist explicit effects and constrain secondary paths

After constructing an authorized command, persist explicit columns or invoke named domain methods. Avoid saving a client-deserialized detached entity, because absent/excluded fields may become defaults and overwrite protected state. Inspect ORM APIs: some update only tracked changes; others write every property; bulk methods may bypass hooks, validation, optimistic concurrency, or tenant filters.

Database permissions and constraints can make impossible transitions fail even if application logic regresses: separate roles for privilege tables, immutable tenant triggers, nonnegative checks, foreign keys, version predicates, and append-only audit. These complement, not replace, per-action authorization.

Imports, GraphQL mutations, gRPC field masks, admin/support panels, background consumers, replay tools, webhooks, and internal service APIs need the same request-to-command mapping. “Internal” callers can be compromised or simply buggy. A field mask itself is untrusted input: intersect paths with the operation allowlist, validate mask/value presence, aliases, nested paths, and clear semantics.

Response serialization is a separate property allowlist. A request DTO that blocks `password_hash` does not prevent a generic entity serializer from returning it. API3:2023 groups unauthorized reads and writes because both arise from exposing internal object properties without explicit property policy. Maintain independently reviewed input and output schemas.

### Make drift visible through contracts and tests

The key regression property is: adding a field to a domain/persistence model cannot make it writable. Test this structurally. Enumerate external input DTO fields per operation and compare them with an approved registry; scan controllers for direct entity binding, generic spreads/maps, and unrestricted update calls. Treat generated schema diffs that add writable properties as security-sensitive review events.

Fuzz every endpoint with likely fields (`admin`, `role`, `tenant`, `owner`, `status`, `price`, `balance`, `verified`, timestamps), case/alias variants, unknown nested objects, duplicate keys, null/missing/empty values, enormous/deep input, relationship directives, prototype/meta keys, and patch pointer encodings. Assert rejection or documented inert behavior and verify database/audit/side effects remain unchanged.

Use differential actor/state tests: same payload as owner, editor, admin, support, service, and wrong tenant; before/after approval, deletion, lock, or delegation expiry. Use property tests asserting persisted changed paths are a subset of $W(c,a,x)$ and server-owned fields equal derived values. Mutation tests add a dangerous field to DTO/mapping or replace explicit assignment with a generic update and require the suite/contract guard to fail.

The executable boundary below rejects unknown fields, derives tenant/role from current server state, distinguishes explicit null, and binds the update to an expected version. It is intentionally smaller than a production parser/domain model.

<!-- bijux-verify: {"id":"strict-profile-command","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"valid=allow:display_name,locale\nadmin_field=deny:unknown:role\nnested_field=deny:unknown:profile\nclear_email=allow:notification_email\nstale_version=deny:version\nserver_owned=member,north\n","stderr":""}} -->
```python
WRITABLE = {"display_name", "locale", "notification_email"}
current = {"display_name": "Alice", "locale": "en", "notification_email": "a@example.test",
           "role": "member", "tenant_id": "north", "version": 7}

def update_profile(payload, expected_version):
    unknown = sorted(set(payload) - WRITABLE)
    if unknown:
        return "deny:unknown:" + unknown[0], current
    if expected_version != current["version"]:
        return "deny:version", current
    candidate = dict(current)
    for field in WRITABLE & set(payload):
        candidate[field] = payload[field]
    changed = sorted(field for field in WRITABLE if candidate[field] != current[field])
    return "allow:" + ",".join(changed), candidate

print("valid=" + update_profile({"display_name": "Alicia", "locale": "sv"}, 7)[0])
print("admin_field=" + update_profile({"role": "admin"}, 7)[0])
print("nested_field=" + update_profile({"profile": {"is_admin": True}}, 7)[0])
print("clear_email=" + update_profile({"notification_email": None}, 7)[0])
print("stale_version=" + update_profile({"locale": "fr"}, 6)[0])
safe = update_profile({"display_name": "Alicia"}, 7)[1]
print("server_owned=" + safe["role"] + "," + safe["tenant_id"])
```

The code establishes only deterministic allowlist/version behavior. Production evidence must also cover actual decoder/binder/ORM behavior, domain authorization, atomic persistence, aliases/duplicates, every media type, and schema evolution.

## Definitions and Notation

Let $P$ be canonical input property paths, $p$ a parsed payload, and $paths(p)\subseteq P$ the complete affected paths after resolving media-type semantics and aliases. For trusted context $c$, operation $a$, and current object $x$, $W(c,a,x)\subseteq P$ is the authorized writable set. Let $T_a(x,p,c)=x'$ be the explicit command/mapping transition and $S$ be server-owned paths.

Safety requires $paths(p)\subseteq W(c,a,x)$ and $W(c,a,x)\cap S=\varnothing$ for ordinary client commands. The system also requires schema validity $V_{schema}(p)$, transition authorization $A(c,a,x,x')$, and invariants $I(x')$. The persisted changed-path set $\Delta(x,x')$ should satisfy

$$
\Delta(x,x')\subseteq W(c,a,x)\cup D_a,
$$

where $D_a$ is the documented set of server-derived effects for action $a$ (for example, `updated_at` and a new version). This permits legitimate server changes without treating them as client authority.

**Missing** means no instruction for a partial update. **Null** is an explicit JSON value whose operation-specific meaning may be set-null or removal. A **default** is a server/schema-produced value when its documented precondition holds. These states are not interchangeable.

## Mechanisms, Invariants, or Proof Structure

1. Inventory internal/domain/persistence properties, relationships, aliases, binders, mappers, serializers, bulk paths, and every input media type.
2. Derive one closed request schema from each canonical domain action, not from the full entity.
3. Mark every value as client-proposed, server-derived, immutable, or separately privileged; keep ordinary write sets disjoint from server-owned paths.
4. Parse once under explicit duplicate/name/content-type/depth/size rules and compute all affected canonical paths.
5. Reject any path outside the static schema or context/state-specific write allowlist; validate nested sources and destinations.
6. Construct an explicit command/candidate using trusted context and authoritative references, preserving missing/null/remove semantics.
7. Authorize the object and complete transition; validate types, cross-field rules, relationship targets, and domain invariants.
8. Persist named effects atomically with the expected current version; derive server fields and prevent partial side effects.
9. Independently allowlist output properties, audit safely, and map errors without revealing hidden fields.
10. Enforce drift guards so new model properties, aliases, operations, binders, or media types cannot become writable without reviewed contract changes.

Under the assumptions that canonical path extraction is complete, mapping has no undeclared side effects, and persistence changes exactly the candidate plus $D_a$, the two subset conditions imply no server-owned path is directly selected by the payload and no changed path falls outside authorized plus derived effects. This is a bounded argument, not proof that $W$, $T_a$, $A$, or $I$ represents correct business policy or that every runtime path uses it.

## Alternatives and Trade-Offs

Dedicated DTOs/commands are explicit, reviewable, and safe under model evolution but add types and mapping code. Framework field allowlists are concise but may vary by content type, create/update path, aliases, or nested input. Use framework mechanisms as enforcement helpers behind operation-specific schemas, not as the only architectural boundary.

Allowlisting is future-safe but requires deliberate updates. Blacklisting is initially convenient and sometimes useful as defense in depth, yet every new sensitive field is a possible bypass. Rejecting unknown fields detects drift but reduces forward compatibility; ignoring them eases rolling clients but can hide bugs and changes behavior when fields later become known. Prefer strict command inputs with explicit version/capability rollout.

Action endpoints make lifecycle and privilege transitions clear, narrow, and auditable. Generic PATCH reduces endpoint count and supports flexible clients but requires path-level policy, presence/null rules, transition authorization, and careful evolution. Use generic patch mainly for genuinely client-owned properties; use commands for money, privilege, approval, ownership, and state machines.

JSON Merge Patch is compact and natural for object-shaped partial changes but gives null deletion semantics and replaces arrays as wholes. JSON Patch expresses precise ordered operations and tests but exposes a larger path/source/array attack surface. A typed partial DTO is simplest when the writable set is small and stable. Whichever representation is chosen, authorize semantic effects rather than trusting syntax.

Domain encapsulation prevents arbitrary setters and centralizes invariants, but ORMs/serializers/imports can bypass it. Database constraints and separate privileges catch some unsafe states but cannot infer actor/action intent. Use explicit command methods plus narrow persistence and database backstops.

## Failure Modes and Misconceptions

- **“The form never sends that field.”** Attackers construct requests independently of the UI.
- **“Validation passed.”** Type/format validity does not grant authority or prove a legal transition.
- **“We removed the field from the response.”** Attackers guess names or inspect schemas/client/source; read and write schemas are independent.
- **“We blacklist `is_admin`.”** A future `role`, alias, nested permission, or different update path may remain writable.
- **“The DTO makes it safe.”** Not if it contains protected fields, loose maps, or a reflective mapper into the entity.
- **“Unknown fields are ignored.”** That hides drift and can turn a once-inert attack payload active after evolution.
- **“PATCH only changes supplied values.”** Null/removal, arrays, source paths, aliases, and defaulted language fields can change more.
- **“PUT is full replacement.”** Server-owned fields still are not client-owned merely because a public representation contains them.
- **“Only top-level keys matter.”** Nested attributes, relationships, collection directives, maps, and field masks are writable paths too.
- **“An admin may set every property.”** Privileged actions still need role ceilings, tenant boundaries, separation, invariants, and audit.
- **“The ORM updates dirty fields only.”** Detached entities, bulk methods, mappers, hooks, and defaults may produce different effects.
- **“Rejecting `tenant_id` is enough.”** Foreign keys, parent IDs, owner objects, relationship connects, and alternate aliases can cross tenants.
- **“Database constraints solve it.”** Many privilege or workflow states are structurally valid but unauthorized for this caller/action.
- **“Internal APIs can bind entities.”** Compromised or buggy services can overpost; business authority must remain explicit.
- **“A few attack tests cover it.”** Model/schema evolution requires structural drift tests and generated unknown-path cases.

## Worked Examples

### Example 1

**Situation:** Signup accepts email/password, and an attacker sends `role=administrator`. **Reasoning:** The signup DTO is closed to email/password/invitation token. `role` is unknown and rejected. The server validates the invitation, derives tenant and safe initial role, hashes the password, and constructs `RegisterUser`. A generic `User(**body)` never exists. **Conclusion:** creation derives privilege from a trusted grant rather than a client property.

### Example 2

**Situation:** An account update blacklists `is_admin`; a migration adds string field `role`. **Reasoning:** Generic model binding now accepts `role=admin` because the blacklist cannot anticipate it. With an allowlisted profile DTO, adding an entity column changes neither schema nor mapper; a contract drift test confirms no new writable path. **Conclusion:** blocklists are unsafe under model growth, while allowlists preserve deny-by-default.

### Example 3

**Situation:** `PATCH {"notification_email": null}` reaches a language type that maps missing and null to `None`. **Reasoning:** The server cannot know whether to preserve or clear the field. A patch presence wrapper records `absent`, `present-null`, or `present-value`; the contract defines null as clear after validation. Omitted input leaves it unchanged. **Conclusion:** safe partial updates require presence semantics, not only value types.

### Example 4

**Situation:** JSON Patch contains `{"op":"move","from":"/role","path":"/display_name"}`. **Reasoning:** Checking only destination would permit reading/removing a protected property. The service defines patch over a public writable projection where `/role` does not exist and validates both source and destination paths; the whole patch fails atomically. **Conclusion:** move/copy authority includes the source effect as well as destination.

### Example 5

**Situation:** Order creation accepts product ID, quantity, and attacker-supplied unit price `0.01`. **Reasoning:** `unit_price` is absent from the DTO. The application authorizes the product, loads current catalogue price, validates positive bounded quantity, computes total, and stores price provenance/version. Later discounting is a separate governed rule. **Conclusion:** monetary derived fields come from authoritative data, not from plausible client values.

### Example 6

**Situation:** A team update accepts nested `members: [{id, role}]`; a manager assigns a user from another tenant as owner. **Reasoning:** Closed shape alone is insufficient. Each member ID is object-authorized, tenant compatibility checked, requested role bounded below the manager's ceiling, last-owner invariant maintained, duplicates rejected, and relation changes applied atomically. Prefer explicit invite/role-change commands. **Conclusion:** nested relationship input combines property, object, and transition authorization.

### Example 7

**Situation:** An ASP.NET endpoint uses a binding attribute believed to block `Balance`, but consumes JSON. **Reasoning:** Microsoft's documentation says relevant `[Bind]` behavior applies to form model binding and not JSON/XML input formatters. Verification follows the actual JSON deserialization path. A dedicated request view model without `Balance`, closed JSON options/schema, and explicit mapping supplies the boundary. **Conclusion:** framework protection must match the real parser/binder route.

### Example 8

**Situation:** A PUT request omits `owner_id`; a detached ORM entity initializes it to null and `save` writes every column. **Reasoning:** Excluding the field from binding did not preserve it. The service loads the authorized current aggregate, constructs a replacement of documented client-owned fields, preserves/derives ownership, checks version/invariants, and updates explicit columns. **Conclusion:** safe input filtering can still fail at persistence if omitted properties are overwritten.

### Example 9

**Situation:** An API ignores unknown `moderation_state` for compatibility. A later release adds it to a reused DTO. **Reasoning:** Old attack/client payloads now become active without a new request shape. Under strict unknown rejection, old servers signal incompatibility and new writable fields require versioned schema, mapper, authorization, and tests. If tolerant rollout is mandatory, capability negotiation gates the new field. **Conclusion:** unknown-field policy is part of security evolution, not parser trivia.

### Example 10

**Situation:** A GraphQL mutation takes `UpdateUserInput` generated from the output `User` type, including `emailVerified`, `roles`, and `createdAt`. **Reasoning:** GraphQL's typed schema does not make the fields authorized. Define action-specific input types, omit server fields, apply per-field and resulting-state policy, bind actor/tenant from context, and scan schema diffs for new input fields. Resolvers call a domain command rather than generic map update. **Conclusion:** strong transport typing prevents malformed input, not overbroad writable contracts.

## Cross-Program Connections

- **Security Engineering:** least privilege, default deny, privilege escalation, confused deputy, and attack-surface drift motivate closed command vocabularies.
- **Domain-Driven Design:** commands, aggregates, value objects, invariants, and explicit lifecycle methods prevent persistence structure from defining public authority.
- **Type Systems:** separate input/output/domain types, presence types, exhaustive matching, closed records, and refinement validation encode boundaries.
- **Database Engineering:** explicit column updates, constraints, transactions, versions, foreign keys, row policy, and role separation backstop application mapping.
- **Language Processing:** parsing, duplicate names, Unicode/case normalization, aliases, JSON Pointer, and canonical paths determine what field was actually requested.
- **Distributed Systems:** retries, concurrent versions, async consumers, schema evolution, mixed deployments, and event compatibility shape strictness and rollout.
- **Testing and Formal Methods:** subset properties, mutation testing, schema diffs, fuzzing, and state-machine tests expose writable-surface regressions.
- **Privacy Engineering:** independent output allowlists, metadata containment, error redaction, and payload/audit minimization prevent property exposure.

## References

1. OWASP Foundation. [API3:2023 Broken Object Property Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/). OWASP API Security Top 10, 2023. Checked 2026-09-01.
2. OWASP Foundation. [Mass Assignment Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html). OWASP Cheat Sheet Series. Checked 2026-09-01.
3. Microsoft. [Model Binding in ASP.NET Core](https://learn.microsoft.com/en-us/aspnet/core/mvc/models/model-binding?view=aspnetcore-10.0). Microsoft Learn, .NET 10 documentation. Checked 2026-09-01.
4. Rails Core Team. [Action Controller Overview: Strong Parameters](https://guides.rubyonrails.org/action_controller_overview.html#strong-parameters). Rails Guides. Checked 2026-09-01.
5. Hoffman, P., and Snell, J. [RFC 7386: JSON Merge Patch](https://www.rfc-editor.org/rfc/rfc7386.html). IETF, October 2014. Checked 2026-09-01.
6. Bryan, P., and Nottingham, M. [RFC 6902: JavaScript Object Notation (JSON) Patch](https://www.rfc-editor.org/rfc/rfc6902.html). IETF, April 2013. Checked 2026-09-01.

## Exercises

### Exercise 1

Classify every field of a multi-tenant user record as client-proposed, server-derived, immutable, or separately privileged. Derive DTOs/commands for signup, profile edit, email change, role assignment, tenant transfer, suspension, and deletion.

### Exercise 2

Given current order state and JSON Merge Patch/JSON Patch documents containing missing, null, array, move/copy, relationship, price, status, and duplicate operations, compute canonical affected paths and decide each request.

### Exercise 3

Diagnose an endpoint that binds JSON into a shared read/write ORM entity, calls a validator, then `save(entity)`. Provide a framework-independent repair and regression tests.

### Exercise 4

Design a strict-but-deployable evolution plan for adding an optional writable field while old servers reject unknown input and mobile clients update slowly. Include capability/version negotiation and rollback.

### Exercise 5

Transfer the model to an infrastructure API that creates virtual machines from nested network, image, identity, billing, metadata, and startup configuration. Define safe writable paths and server-owned effects.

## Answers to the Exercises

### Answer 1

Client-proposed profile facts include display name, locale, and notification preferences; signup may propose email/password and an invitation token. Server-derived fields include ID, tenant from validated invitation/grant, password hash, safe initial role, verification state, created/updated time, version, audit actor, and risk signals. Immutable in ordinary operations are ID, creation provenance, and often tenant; email/owner lifecycle is separately privileged. Use distinct `RegisterUser`, `UpdateProfile`, `BeginEmailChange`, `AssignRole`, `TransferTenant`, `SuspendUser`, and `DeleteUser` inputs. Each has only necessary parameters, required assurance/actor/object policy, role ceiling or target-tenant checks, explicit state transition, version, audit reason, and server-derived effects. No generic `UpdateUser` exposes the union of all fields.

### Answer 2

First reject duplicate JSON members at parsing; they have no portable single meaning. For merge patch, absent paths are unchanged, null removes/clears only nullable/removable allowed fields, object members recurse, arrays replace as wholes, and any price/status/tenant/owner relationship path outside the operation allowlist denies the entire request. Compute paths against the public writable projection, not storage. For JSON Patch, process the ordered operations but validate before persistence: `add/remove/replace` authorize destination, `move/copy` authorize both `from` and destination plus read/removal effects, `test` must not expose protected paths, pointers are decoded/canonicalized, indices bounded, and intermediate/final state valid. Relationship IDs need object/tenant authorization. Apply atomically with expected version or no changes remain.

### Answer 3

The shared type exposes every readable/internal property to the decoder; validation may accept unauthorized but well-typed state; saving a detached entity can overwrite protected/omitted columns. Define closed operation-specific JSON DTOs with duplicate/unknown/alias/content-type rules. Parse once, validate types and presence, derive subject/tenant/server values from trusted context, load and object-authorize the current aggregate, map explicit fields into a named command, authorize every field/reference and the resulting transition, enforce invariants, then update explicit columns in one version-checked transaction. Separate response DTO. Tests fuzz sensitive/unknown/case/nested fields, null/missing/default, alternate media types, two users/tenants, stale versions, ORM dirty/full update behavior, database unchanged on every denial, schema/model-field drift, and mutations that add a DTO field or generic mapper.

### Answer 4

Give the new field stable semantics and an operation/version-specific schema. Deploy servers that understand but initially feature-gate it, advertise a capability or new media/API version only after the full fleet can parse/enforce it, then enable clients to send it only when capability/version is present. Old clients remain valid because the field is optional; new clients encountering old servers either omit it or receive a clear unsupported-version response and retain local intent. The mapper, property authorization, storage migration, response behavior, audit, and generated clients roll out before enablement. Telemetry tracks unknown-field/version rejection without payload leakage. Rollback disables capability/emission while servers continue safely parsing or rejecting; it never reuses an ignored old name whose prior payloads could suddenly activate.

### Answer 5

Create a `ProvisionMachine` DTO with client-proposed name, approved image reference, size class, bounded count, selected authorized network/subnet, narrowly typed disk requests, public-key/secret references, and namespaced inert metadata. Do not accept tenant/project, owner, cloud account, billing price, privileged service identity, security-group rules beyond an approved policy, instance state, IP/MAC, host placement, audit fields, quota usage, timestamps, or raw startup code by generic binding. Authorize every referenced image/network/key/secret within the project, validate image/size/region compatibility and quota, derive current catalogue price/billing/project/owner, compile an approved startup template, and create resources transactionally or with compensating workflow/idempotency. Nested arrays have bounds and closed item schemas; metadata cannot affect policy/config. Persist immutable actor/request provenance and derived IDs/state/version, and independently restrict response properties such as host, credentials, and internal billing data.
