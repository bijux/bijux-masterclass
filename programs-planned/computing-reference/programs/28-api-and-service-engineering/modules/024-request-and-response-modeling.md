---
module_id: API-024
program: API & Service Engineering
level: 1
module_number: 24
title: Request and Response Modeling
status: complete
last_verified: 2026-09-01
---

# Request and Response Modeling

## One-Page Review

### Governing question

How should an API model what a consumer may ask for and what a service may reveal so ownership, lifecycle, authority, omission, errors, and evolution remain explicit in both directions?

### Essential definitions

- A **request model** describes consumer-supplied intent for one operation, not a writable copy of stored state.
- A **response model** describes an authorized representation of an outcome or resource observation, not an object-memory dump.
- **field ownership** identifies which party may originate or change a value and which party merely observes it.
- A **projection** is a representation selected for a consumer decision, role, or interaction rather than every available fact.
- A **derived field** is computed or asserted by the service from trusted state and is not directly writable by the caller.
- **overposting** or **mass assignment** occurs when untrusted input is bound to fields the caller did not legitimately control.
- A **problem model** describes stable machine-readable details of a failed HTTP interaction while preserving status semantics.

### Central model, mechanism, or theorem

For operation $o$, model request fields $Q_o$ and response fields $P_o$ as projections from different authority sets. Admission requires every supplied field to belong to the caller-writable set $W_o$ and the effective request to satisfy structural and domain constraints. Disclosure requires every emitted field to belong to the visible set $V(o,a,t,s)$ for operation $o$, actor $a$, target $t$, and state $s$. In general $Q_o\ne P_o$, and neither should be inferred from a persistence record.

### Critical invariants

Every request field has an owner and operation-specific purpose. Service-derived identity, tenant, price, role, audit, lifecycle, and authorization results are never trusted from request content. Missing, null, empty, defaulted, unchanged, and removed have distinct declared meanings. Response fields are authorized before serialization, including nested objects, counts, links, and errors. Status, headers, content type, and body describe one coherent outcome. Create, replace, patch, command, success, list, detail, and problem models are distinct where their semantics differ. Unknown request fields follow an explicit rejection policy; consumers tolerate documented response evolution.

### Common failures

Reusing one database entity as every request and response; making every field optional to support every operation; trusting `readOnly` or serializer settings as authorization; binding requests directly into domain or persistence objects; accepting client-supplied tenant, owner, total, status, or audit fields; returning secrets because they existed in memory; using null for hidden, missing, unknown, and cleared; wrapping every response in `data`; returning `200` with an error body; using one universal error string; exposing internal enum or timestamp meaning; and adding response fields without consumer evidence.

### Compact example

`CreateInvoiceRequest` accepts customer reference, currency, and lines. It does not accept invoice ID, tenant, computed tax, total, status, approver, creation time, or version. `InvoiceResponse` can return authorized identity, totals, state, timestamps, links, and a validator, but never a payment credential or internal risk note. **Conclusion:** request and response models may describe the same domain concept while having deliberately different fields and authority.

### Connections

[Designing an API from Consumer Tasks Rather Than Database Tables](020-designing-an-api-from-consumer-tasks-rather-than-database-tables.md) supplies consumer intent. [JSON Schema](022-json-schema.md) supplies structural expression, and [OpenAPI Structure](023-openapi-structure.md) places models into operations and media types. [Validation Constraints](../ROADMAP.md) deepens field and cross-field admissibility; later security modules enforce authority.

## Governing Question

Which directional models let a producer accept only legitimate intent and reveal only legitimate observations while remaining precise under HTTP, domain, security, and evolution constraints?

## Why This Matters

Requests and responses cross an independent trust boundary. A request is not a friendly constructor call. It is an untrusted claim about desired action, supplied through a network that can replay, truncate, transform, or deliver it after state changes. A response is not a debugging view. It is a durable disclosure that clients, logs, caches, generated code, analytics, and downstream services may retain.

The fastest way to create a vulnerability is to serialize a persistence or domain object in both directions. A model containing `tenant_id`, `role`, `approved`, `price`, `balance`, `risk_score`, `deleted_at`, and `password_hash` may be convenient internally. Making those properties writable enables mass assignment; making them readable enables excessive data exposure. Hiding fields in a UI changes neither risk.

OWASP API Security Top 10 2023 groups excessive property exposure and mass assignment under broken object property-level authorization. The durable lesson is not one framework setting: inspect and authorize every property that a caller can modify or receive. Object-level authorization and property-level authorization are complementary. A caller may legitimately access an invoice while lacking permission to change its approval or see its fraud notes.

HTTP adds another modeling layer. RFC 9110 defines a representation as information intended to reflect a past, current, or desired resource state. Request content can be a representation, command, patch document, query encoding, or upload. Response content can represent the target, an operation, a collection page, or a problem occurrence. Status and metadata remain part of the meaning. An identical JSON object under `201`, `202`, `409`, or `422` does not communicate the same outcome.

## Prerequisites and Retrieval

Retrieve resources and representations, consumer-task design, HTTP method and status semantics, JSON data types, JSON Schema, OpenAPI content maps, authentication, authorization, domain invariants, persistence boundaries, partial updates, concurrency validators, content negotiation, pagination, and Problem Details.

Before modeling an operation, retrieve its actor, purpose, preconditions, input ownership, observable success, failure recovery, confidentiality, consistency, and evolution policy. A field list without those decisions is premature.

## Learning Objectives

By the end of this module, you should be able to:

1. derive request and response models from consumer intent and field authority;
2. separate create, replacement, patch, command, detail, summary, and problem shapes;
3. define omission, null, default, derivation, redaction, and conditional presence;
4. model identifiers, money, time, enums, links, collections, and nested data safely;
5. map transport models through an explicit application boundary;
6. prevent overposting and excessive disclosure with structural and authorization controls; and
7. evolve directional models using provider and consumer evidence.

## Core Exposition

### Begin with one operation and one decision

Name the consumer, the decision or intent, and the operation outcome before listing fields. “Customer model” is usually too broad. `CreateCustomerRequest`, `ReplaceCustomerProfileRequest`, `CustomerSummary`, `CustomerDetail`, and `CustomerCreated` each serve different interactions. Their overlap does not make them the same contract.

For each request field, ask:

- why must the caller supply it now?
- is it intent, evidence, a reference, a precondition, or presentation preference?
- who is authoritative for the value?
- what does absence mean?
- can it be null, empty, defaulted, or repeated?
- is its value stable enough to become public contract?
- which actor and target state permit it?

For each response field, ask which consumer decision it supports, its authority and freshness, whether its absence discloses protected information, and whether clients can rely on it across versions. A field is not free merely because the server already computed it.

### Build an authority matrix

Classify fields by operation, not only by entity. A useful authority matrix records input acceptance, source of truth, output visibility, mutability, sensitivity, and derivation. The same field can be writable during creation, immutable during replacement, and visible only to administrators in detail responses.

<!-- bijux-verify: {"id":"field-authority-matrix","mode":"data","language":"text","toolchain":"none","reason":"Review table showing operation-specific ownership and disclosure decisions; it is declarative rather than executable."} -->
```text
field          create input   update input   ordinary output   source
customer_ref   required       forbidden      visible           caller at creation
tenant_id      forbidden      forbidden      hidden            auth context
currency       required       forbidden      visible           caller, then immutable
subtotal       forbidden      forbidden      visible           service computation
status         forbidden      forbidden      visible           domain transition
risk_note      forbidden      forbidden      hidden            restricted service evidence
```

“Forbidden” is stronger than “ignored.” Rejecting unknown or prohibited request fields catches stale clients and attacks. Quietly discarding `role: "admin"` prevents one effect but can convince the caller the value was accepted. For compatibility-sensitive APIs, distinguish unknown extension fields from known forbidden fields explicitly.

Identity deserves separate treatment. A client can supply an idempotency key or a client-selected resource identifier under one contract without controlling internal row IDs, tenant identity, owner identity, audit principal, or authorization subject. Derive trusted context from authenticated transport and server state, not body fields that repeat it.

### Separate transport, application, domain, and persistence models

Decode a request into a transport-specific input model. Validate syntax and structure. Map accepted fields into an application command or query together with trusted identity, target, preconditions, and request metadata. Let the domain evaluate invariants and transitions. Map the outcome into an authorized response model. Persistence records stay behind adapters.

This boundary prevents framework binding from becoming policy. An ORM entity can contain relationships, lazy loaders, internal flags, version columns, soft-delete markers, and secrets. A domain aggregate can expose methods and invariants irrelevant to serialization. A request DTO can express only the caller's legitimate intent. A response DTO can be constructed after field-level visibility decisions.

Do not rely on “ignore unknown JSON properties” as the only boundary. A later internal field addition could silently become writable if generic binding or reflection changes. Use allowlisted operation-specific constructors or mapping functions. Test that every prohibited field remains rejected or inert under the documented policy.

### Model create requests around caller intent

A create request normally contains facts the caller is authorized to originate and references it may select. The service derives stable identity, tenant, ownership from authenticated context, timestamps, initial lifecycle state, totals, policy decisions, audit facts, and version validators unless the contract explicitly assigns one to the caller.

Required-at-creation does not imply mutable forever. Currency can be mandatory and then immutable. A customer reference may be accepted only if the caller can use that customer. Lines can carry SKU and quantity while authoritative price, tax, discount, and total come from a quote or server calculation.

Defaulting must be visible. If omitted `locale` selects a tenant policy at request time, document that policy and whether the resolved value is returned. A JSON Schema `default` annotation does not perform the selection. Store or report enough resolved state that later policy changes do not rewrite the meaning of an earlier request invisibly.

Creation success should model the actual completion point. `201` can include the resource URI, representation, and validator. `202` should model an accepted operation with identity, observation link, state, and terminal outcomes rather than pretending the final resource exists.

### Distinguish replacement, partial change, and command models

A PUT representation expresses complete desired state of the target under its media type. It may omit server-derived fields by contract, but caller-owned fields omitted from a complete representation cannot ambiguously mean “leave unchanged.” Use validators to protect against overwriting a newer state.

PATCH content is an instruction document whose media type defines absence, null, path, and array behavior. A partial object with every property optional is not self-explanatory. JSON Merge Patch uses null for removal and replaces arrays; JSON Patch uses operations and JSON Pointer. A custom field-update document needs its own precise semantics.

Domain commands such as approve, cancel, rotate, refund, or publish deserve intent models when document editing would hide transition meaning. `ApproveExpenseRequest` may contain a decision comment and expected version; it must not accept `approvedBy`, `approvedAt`, or final status. Those come from the authenticated actor, authoritative clock, and state transition.

Sharing one all-optional “Update” schema across replacement, patch, and commands erases guarantees. Separate models increase artifact count but make authority, requirement, and evolution review tractable.

### Give omission, null, and empty distinct meanings

For each field and operation, define the state space. In a create request, omission may select a default; explicit null may be prohibited or may mean known absence. In a merge-style update, omission often means unchanged while null may remove. In a response, omission may mean not requested, not applicable, unauthorized, unknown, or unavailable. Those meanings are not interchangeable.

Avoid using null as universal uncertainty. If a value has meaningful provenance or availability, a tagged object can be clearer: `{ "state": "pending" }`, `{ "state": "known", "value": 42 }`, or `{ "state": "not_applicable" }`. Do not expose `{ "state": "forbidden" }` if revealing that the fact exists would violate non-disclosure policy.

Empty string, empty array, and empty object are present values. Decide whether each is meaningful. A list of zero line items can be structurally well typed but invalid for order creation. An empty patch can be a no-op or error according to the media type and API contract. Normalization such as trimming whitespace happens at a named stage and must not change signed or idempotency-fingerprinted content silently.

### Use Schema annotations as documentation, not enforcement

JSON Schema Draft 2020-12 defines `readOnly` and `writeOnly` as annotations. OpenAPI 3.2.0 explains that direction-aware tooling may validate them, but JSON Schema itself does not know whether an instance is being read or written. An owning authority may ignore a supplied read-only property or treat it as an error under the applicable contract.

`readOnly: true` therefore does not prevent overposting. `writeOnly: true` does not redact output. `deprecated` does not remove access. `default` does not insert a value. Use separate directional schemas or disciplined composition, explicit mappers, and authorization checks. Annotations improve generated documentation and code when tools honor them, but security must survive a tool that merely carries them through.

A property that is both required and read-only creates direction-sensitive interpretation and uneven generator support. Separate request and response schemas are often clearer than one schema requiring contextual filtering. If you reuse a shared core, test the fully resolved input and output views rather than the component in isolation.

### Model response projections for decisions

Return the smallest coherent representation that supports the consumer's next decision. A collection summary might contain identity, display label, state, updated time, and link. A detail representation might add lines and history. An administrative projection may include restricted diagnostics. Do not force every consumer to receive the union of all roles and use cases.

Authorization precedes serialization. Filter the candidate resource universe before counting and paginating. Then apply field-level visibility to each selected item and nested relation. A response can leak through totals, `hasMore`, ordering gaps, links, enum states, error differences, timing, or supposedly opaque IDs even when a direct field is absent.

Partial representations need a contract. If fields are selected through a `fields` parameter, state whether omitted properties are unrequested, unauthorized, unavailable, or absent in the resource. Validators and caches must correspond to the selected representation and vary on selection inputs where required. A schema with every field optional cannot convey this alone.

Links and actions can expose discoverability, but they do not grant authority. A visible `approve` link should agree with current policy and state, yet the server must reauthorize when invoked. Representations age between read and action.

### Represent identifiers, money, time, and enums deliberately

Identifiers are opaque unless their structure is part of the contract. Use strings when numeric arithmetic is irrelevant, preserve case and normalization rules, and do not expose sequential internal IDs if enumeration increases risk. State whether IDs are stable, reusable, tenant-scoped, or globally resolvable.

Money needs currency and exact amount semantics. A decimal JSON number can lose precision in binary floating point; an integer minor-unit model depends on currency exponent; a string requires parsing rules. Choose one representation with range, rounding, scale, and currency relationship documented. Never accept a caller-computed authoritative total merely because it matches the response shape.

Time fields need event meaning, clock source, offset and zone rules, precision, and ordering limitations. `createdAt` might mean accepted, committed, persisted, or externally observable. Prefer an interoperable timestamp format while remembering lexical validity does not establish truthful or monotonic time.

Enums create closed-world pressure in generated clients. Request enums can be intentionally closed because the service accepts known commands. Response classifications often evolve; consumers need an unknown strategy or versioned changes. Do not publish internal workflow states that are not stable consumer decisions.

### Model collections as traversable representations

A collection response is more than an array. It may need a stable total ordering, cursor or page links, snapshot or freshness meaning, item projection, next-page availability, and limits. A generic envelope such as `{data, meta}` is not inherently wrong, but every layer needs a purpose. Do not wrap single resources mechanically and create two competing locations for status and errors.

Cursors should be opaque and bound to the query, sort, authorization context, and traversal semantics as required. Counts can be expensive, stale, or confidential. Mark approximation and time basis if a count is not exact. Do not include `total=0` when policy requires hiding whether matching resources exist.

Nested collections need cardinality bounds. Embedding every child can create unbounded payloads and inconsistent snapshots. Include a bounded summary and link or separate projection when the full relationship has its own pagination and authorization.

### Make success and failure models coherent with HTTP

Response modeling includes status code, headers, media type, and body together. A `201` representation can accompany `Location`; a `202` model should identify accepted work; a `204` has no content; a conditional `304` relies on validators rather than a normal response body. Do not build `{ "success": false }` under `200` to override HTTP semantics.

RFC 9457 Problem Details supplies `application/problem+json` and common members such as `type`, `title`, `status`, `detail`, and `instance`, with extension members for domain decisions. The HTTP status remains authoritative; body `status` is advisory. Problem types identify stable categories, while human `detail` text is not a machine code.

Model errors around recovery: correct fields, authenticate, obtain authority, refresh a validator, wait, observe accepted work, reconcile an unknown outcome, or stop. Field-error locations need a stable addressing convention and must not expose internal property or database names. Avoid reflecting secrets, submitted credentials, stack traces, constraint names, or hidden resource facts.

### Check request admission and response disclosure separately

The bounded checker below turns a small authority matrix into executable admission and disclosure decisions. It does not prove object-level authorization or service correctness.

<!-- bijux-verify: {"id":"directional-field-policy","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"create_request=accepted\noverposted_request=rejected:status\nordinary_response=id,status,total\nrestricted_fields=1\nrequest_fields=2\nresponse_fields=3\nevidence=bounded_directional_policy\n","stderr":""}} -->
```python
policy = {
    "customer_ref": {"write": True, "ordinary_read": False, "restricted": False},
    "currency": {"write": True, "ordinary_read": False, "restricted": False},
    "id": {"write": False, "ordinary_read": True, "restricted": False},
    "status": {"write": False, "ordinary_read": True, "restricted": False},
    "total": {"write": False, "ordinary_read": True, "restricted": False},
    "risk_note": {"write": False, "ordinary_read": False, "restricted": True},
}

def admit(request):
    forbidden = sorted(name for name in request if not policy.get(name, {}).get("write"))
    return "accepted" if not forbidden else "rejected:" + forbidden[0]

def disclose(record):
    return sorted(name for name in record if policy.get(name, {}).get("ordinary_read"))

request = {"customer_ref": "cust-7", "currency": "SEK"}
record = {"id": "inv-9", "status": "draft", "total": "125.00", "risk_note": "review"}
print("create_request=" + admit(request))
print("overposted_request=" + admit({**request, "status": "paid"}))
print("ordinary_response=" + ",".join(disclose(record)))
print("restricted_fields=" + str(sum(rule["restricted"] for rule in policy.values())))
print("request_fields=" + str(len(request)))
print("response_fields=" + str(len(disclose(record))))
print("evidence=bounded_directional_policy")
```

Test each direction adversarially. For admission, inject known forbidden and unknown properties, other-tenant identifiers, derived totals, invalid state transitions, duplicate names, boundary values, and stale validators. For disclosure, test every role, resource state, nested object, collection count, link, error, cache path, and serializer setting. Snapshot tests alone are insufficient if the snapshot was approved without an authority oracle.

### Evolve each direction by its consumers

Request and response compatibility have different variance. Widening accepted requests can be compatible for callers but may create ambiguity or security risk. Narrowing accepted requests breaks callers that send formerly valid input. Adding response fields is often compatible for tolerant readers but breaks strict decoders, signatures, exact comparisons, and generated types. Removing or changing response fields breaks consumers that rely on them.

Separate schemas make this direction visible. Inventory producers and consumers, compare valid-instance sets, generate witness messages, compile representative clients, and test actual serialization. Treat enum additions, precision changes, nullability changes, default changes, renamed fields, and authorization-filter changes as semantic changes even when a schema diff labels them additive.

Avoid versioning internal models into public names. `CustomerV2DTO` says when a type was made, not what it means. Prefer `CustomerSummary`, `CustomerDetail`, or a media-type/version identifier with a governed compatibility policy. Preserve stable public names while implementations evolve behind explicit mappers.

## Definitions and Notation

For operation $o$, let $Q_o$ be possible request properties and $P_o$ possible response properties. Let $W(o,a,t,s)\subseteq Q_o$ be properties actor $a$ may write for target $t$ in state $s$. Let $V(o,a,t,s)\subseteq P_o$ be properties the service may disclose. If supplied request keys are $K_q$, field admission requires:

$$
K_q\subseteq W(o,a,t,s).
$$

If response keys are $K_p$, field disclosure requires:

$$
K_p\subseteq V(o,a,t,s).
$$

These are necessary, not sufficient: values must also satisfy structural predicates, domain invariants, state preconditions, and cross-object authority. Let mapping $M_o(q,c)$ construct an application command from validated request $q$ and trusted context $c$; fields such as tenant, actor, authoritative time, and policy results should originate in $c$ or domain evaluation rather than untrusted duplicates in $q$.

A **directional model** is scoped to input or output. A **summary** is a bounded collection-oriented projection. A **detail** is a richer single-resource projection. A **command model** represents transition intent. A **redaction** removes or transforms sensitive information under policy. A **field oracle** decides admissible or visible properties for a concrete context. A **witness message** demonstrates a compatibility or policy distinction.

## Mechanisms, Invariants, or Proof Structure

1. Identify the operation, actor, target, state, intent, and observable outcome.
2. Build a field authority matrix for input, source, mutability, visibility, and sensitivity.
3. Define separate directional schemas where ownership or requirement differs.
4. Parse strictly and reject known forbidden and policy-disallowed unknown fields.
5. Map only allowlisted input plus trusted context into an application command.
6. Evaluate domain, state, object, and property authorization before effects.
7. Select and authorize the response projection before serialization.
8. Make status, headers, media type, body, and failure recovery coherent.
9. Test absent, null, empty, boundary, nested, role, cache, and evolution cases.
10. Compare changes by request acceptance and response consumption direction.

The invariants are explicit field ownership, no trust in caller-supplied derived facts, no serialization before disclosure authorization, precise absence semantics, directional schema integrity, coherent HTTP outcomes, bounded collections, and compatibility evidence for both sides of the interaction.

## Alternatives and Trade-Offs

One shared resource schema reduces duplication and can aid round-trip replacement. It also produces direction-sensitive required fields, overposting risk, weak generator behavior, and accidental disclosure. Separate request and response schemas cost more names and mappings but make authority and compatibility explicit. Share only truly invariant value objects.

Rejecting unknown request fields catches mistakes and blocks unintended binding. Ignoring them can help rolling clients and extensions. A balanced policy rejects unknown fields in stable core request objects, provides an explicitly namespaced extension map when needed, and always rejects known forbidden authority fields.

Rich embedded responses reduce calls and can provide a coherent snapshot. They increase payload, authorization surface, coupling, and cardinality risk. Links and separate projections reduce those costs but can add latency and consistency questions. Model the consumer decision and bound the representation.

Null is compact for optionality but collapses different reasons for absence. Tagged availability states are more verbose but improve decisions. Use them when pending, unknown, not applicable, redacted, and failed have materially different recovery.

Mapping code looks repetitive compared with reflection-based binding. That explicitness is a security and evolution boundary. Generated mapping can be acceptable when its allowlists and directional policies are reviewed and tested; do not let generation infer authority from storage fields.

## Failure Modes and Misconceptions

- **“One entity schema avoids duplication.”** It also combines incompatible ownership, requirement, visibility, and lifecycle contracts.
- **“Optional means patchable.”** Optionality only describes presence; it does not define unchanged, removal, authority, or transition semantics.
- **“`readOnly` blocks request fields.”** It is annotation; owning code or direction-aware tooling must enforce policy.
- **“`writeOnly` keeps secrets out of responses.”** A serializer can still emit them unless output mapping and disclosure tests prevent it.
- **“The authenticated user may change every visible field.”** Observation authority and mutation authority are different.
- **“Object authorization covers all properties.”** A permitted object can still contain restricted or immutable properties.
- **“Null means no value.”** It can also be confused with unknown, cleared, hidden, pending, or not requested.
- **“Derived totals can be accepted and checked later.”** Trust authoritative inputs and compute or verify derived facts before effects.
- **“A response is whatever the handler returns.”** Status, metadata, projection, media type, and disclosure policy jointly define it.
- **“An envelope makes APIs consistent.”** A purposeless envelope can duplicate status, nesting, pagination, and error channels.
- **“Adding a response field never breaks.”** Strict decoders, signatures, equality, generated clients, and privacy policy can break.
- **“Hiding a field in the UI secures it.”** Attackers can send and inspect raw HTTP messages.
- **“Database null maps directly to JSON null.”** Persistence absence and public semantic absence need not be identical.
- **“Every timestamp is self-explanatory.”** Event, clock, precision, zone, and consistency semantics must be named.
- **“A valid response is safe to cache.”** Authorization variance and sensitive content require separate HTTP cache policy.

## Worked Examples

### Example 1

**Situation:** `CreateUserRequest` accepts `id`, `role`, and `createdAt` because the response contains them. **Reasoning:** The service owns identity, role-grant policy, and authoritative time. Remove them from input and derive them after authorization. **Conclusion:** readable fields are not automatically writable.

### Example 2

**Situation:** A request includes another tenant's `tenantId` while the token identifies the caller's tenant. **Reasoning:** Ignoring the mismatch hides an attack or client defect. Omit tenant from the schema, derive it from trusted context, and reject known forbidden input. **Conclusion:** duplicated security context must not become authority.

### Example 3

**Situation:** A profile update omits `phone`, sends `phone: null`, or sends `phone: ""`. **Reasoning:** Define omission as unchanged, null as removal only if the patch media type says so, and empty string as an invalid or real value by policy. **Conclusion:** three JSON states require three deliberate meanings.

### Example 4

**Situation:** A create-order request sends line prices and total. **Reasoning:** Accept SKU, quantity, and perhaps a quote identity; obtain authoritative price and compute totals under current policy. **Conclusion:** response calculations are not caller-owned inputs.

### Example 5

**Situation:** An ordinary user can read an account but the response includes `riskNote`. **Reasoning:** Object access does not imply visibility of every property. Construct an ordinary projection after property-level authorization. **Conclusion:** disclosure requires its own field oracle.

### Example 6

**Situation:** A list returns all projects, then filters unauthorized items after computing `total`. **Reasoning:** The total leaks the pre-authorization universe. Authorize the candidate set before count, sort, and pagination. **Conclusion:** collection metadata is also protected output.

### Example 7

**Situation:** A `202` response returns the final report schema with `status: pending`. **Reasoning:** Model an operation resource with its own states, observation link, and terminal result link. **Conclusion:** accepted work is not a premature final-resource representation.

### Example 8

**Situation:** A response adds enum value `manual_review`. **Reasoning:** The schema widening can break exhaustive clients. Provide unknown handling, consumer evidence, or a versioned semantic change. **Conclusion:** output compatibility depends on consumer decisions.

### Example 9

**Situation:** An error says `constraint users_email_key violated for alice@example.test`. **Reasoning:** Translate persistence detail into a stable safe problem type and field location without echoing sensitive values or internal names. **Conclusion:** problem models are public recovery contracts, not debug dumps.

### Example 10

**Situation:** A serializer hides `passwordHash` in normal responses but includes it in an exception object's nested `user`. **Reasoning:** Centralize authorized response construction and test success and every failure path. **Conclusion:** disclosure safety must hold across alternate serialization paths.

## Cross-Program Connections

[Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) supplies commands, value objects, aggregates, and anti-corruption boundaries. [Database Engineering](../../18-database-engineering/ROADMAP.md) supplies persistence models that must remain internal. [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies object and property authorization, least privilege, and information-flow reasoning. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies stale state and ambiguous-outcome models. [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies field oracles and adversarial test design.

## References

1. R. Fielding, M. Nottingham, and J. Reschke, [*RFC 9110: HTTP Semantics*](https://www.rfc-editor.org/rfc/rfc9110.html), especially representations, methods, and response semantics, Internet Standard, June 2022. Checked 2026-09-01.
2. OpenAPI Initiative, [*OpenAPI Specification 3.2.0*](https://spec.openapis.org/oas/v3.2.0.html), especially Schema Object `readOnly` and `writeOnly` handling and media-type content, 19 September 2025. Checked 2026-09-01.
3. A. Wright, H. Andrews, B. Hutton, and G. Dennis, [*JSON Schema Validation: A Vocabulary for Structural Validation of JSON, Draft 2020-12*](https://json-schema.org/draft/2020-12/json-schema-validation), including metadata annotations, 16 June 2022. Checked 2026-09-01.
4. OWASP Foundation, [*API3:2023 Broken Object Property Level Authorization*](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/), OWASP API Security Top 10, 2023. Checked 2026-09-01.
5. M. Nottingham, E. Wilde, and S. Dalal, [*RFC 9457: Problem Details for HTTP APIs*](https://www.rfc-editor.org/rfc/rfc9457.html), Standards Track, July 2023. Checked 2026-09-01.
6. P. Hoffman and J. Klensin, [*RFC 3339: Date and Time on the Internet: Timestamps*](https://www.rfc-editor.org/rfc/rfc3339.html), Standards Track, July 2002, with published errata considered. Checked 2026-09-01.

## Exercises

### Exercise 1

Build an authority matrix for invoice fields `id`, `tenantId`, `customerRef`, `currency`, `lines`, `subtotal`, `tax`, `total`, `status`, `approvedBy`, `createdAt`, and `riskNote` across create input, correction input, ordinary output, and auditor output.

### Exercise 2

Design separate schemas and semantics for profile creation, full replacement, Merge Patch, ordinary detail response, and administrator detail response. Explain omission and null for `displayName`, `phone`, and `verifiedAt` in each direction.

### Exercise 3

A collection handler queries all records, calculates an exact total, paginates, then removes unauthorized items and redacts nested owners. Identify every observable leak and propose a correct pipeline.

### Exercise 4

Model a successful asynchronous export request and its failures. Specify request intent, `202` operation response, terminal success, terminal failure using Problem Details, headers or links, and fields that must come from trusted context.

### Exercise 5

Assess these changes separately for requests and responses: adding an optional property, making a property nullable, adding an enum value, increasing timestamp precision, changing amount from decimal string to JSON number, and hiding a field for a role that formerly saw it. Propose evidence before release.

## Answers to the Exercises

### Answer 1

Create input admits `customerRef`, `currency`, and caller-intent `lines`; it forbids ID, tenant, calculated amounts, status, approver, time, and risk note. Correction input admits only caller-owned correctable line or customer fields under state and version checks; currency may be immutable. Ordinary output may show ID, customer reference under policy, currency, lines, totals, public status, and creation time. Auditor output may additionally show approver and risk evidence according to purpose and least privilege. Tenant usually comes from trusted context and need not be public. Every amount is service-derived; every visibility decision is still subject to object, field, and state authorization.

### Answer 2

Creation requires nonempty display name, permits phone according to explicit null policy, and forbids `verifiedAt`. Full replacement requires all caller-owned desired fields; omission does not mean unchanged. Merge Patch omission means unchanged and null removes a member, making it unsuitable if explicit null is distinct. Ordinary output returns authorized display name and phone state but may omit verification detail; administrator output can include an authoritative `verifiedAt`. The service derives verification time. Separate schemas prevent `readOnly` annotations and all-optional fields from carrying these incompatible meanings alone.

### Answer 3

The original exact total leaks unauthorized membership; page sizes and empty positions reveal filtering; ordering gaps reveal hidden records; nested redaction after selection can reveal owner existence or relationship cardinality; cursors built from the unfiltered set may leak keys and skip authorized items. Establish the authorized candidate universe first, apply query and sort under that policy, build a stable page and cursor, then select an authorized item projection and safe metadata. Decide whether any count is exact, approximate, omitted, or policy-hidden. Test all roles and pages for cross-tenant observations.

### Answer 4

The request contains export selection, format, and perhaps an idempotency identity; actor, tenant, authority, accepted time, storage destination, and retention policy come from trusted context. Return `202` with a stable operation URI, validator or retry guidance, and an operation representation containing queued state and observation link. Terminal success links an authorized export result with expiry and media type. Terminal failure exposes a stable Problem Details type and safe recovery fields, not stack traces or storage paths. Distinguish invalid selection, forbidden data, quota, dependency failure, cancellation, expiry, and unknown outcomes.

### Answer 5

An optional request property widens accepted input but needs ownership and ambiguity review; an optional response property can break strict readers. Nullability adds a new semantic state in either direction. An enum addition is newly accepted input or newly produced output and can break exhaustive consumers. Greater timestamp precision usually preserves instant meaning but can break exact strings, signatures, and parsers. Decimal string to number changes type and precision and is breaking. Role-based hiding changes disclosure and may be security-required but breaks consumers and must not be delayed for unsafe compatibility. Generate old/new witness messages, validate captured requests and outputs, compile representative clients, test precision and unknown values, exercise every role, and document migration or security exception handling.
