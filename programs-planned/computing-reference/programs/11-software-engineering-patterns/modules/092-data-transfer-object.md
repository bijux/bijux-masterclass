---
module_id: SEPAT-092
program: Software Engineering: Patterns
level: 2
module_number: 92
title: Data Transfer Object
status: complete
last_verified: 2026-08-29
---

# Data Transfer Object

## One-Page Review

### Governing question

When data crosses an expensive or independently evolving process/layer boundary, how can one explicit carrier shape reduce calls and decouple contracts without leaking domain behavior, persistence representation, authority, secrets or ambiguous presence semantics?

### Essential definitions

- A **Data Transfer Object (DTO)** is a boundary-specific data carrier, classically used to move a coarse-grained data set between processes and reduce remote calls.
- An **assembler/mapper** converts between domain/application models and DTOs; mapping is policy, not mechanical copying.
- A **request DTO** describes caller-supplied input; a **response DTO** describes server-observable output. They often differ.
- A **domain entity** owns identity/behavior/invariants; a DTO carries serialized data and does not become authoritative merely by deserialization.
- A **persistence record/model** represents storage concerns; it is not automatically a public contract.
- A **command** expresses application intent after boundary validation/authorization; it is distinct from raw transport DTO.
- A **domain/integration event** states a past fact under event semantics; it is not just any DTO.
- **field presence** distinguishes omitted, explicitly null, default-valued and set values where the contract requires it.
- **over-posting/mass assignment** occurs when untrusted fields are automatically bound to privileged/internal properties.
- A **compatibility policy** defines how readers/writers handle added, removed, renamed, unknown and differently interpreted fields.

### Central model, mechanism, or theorem

Let domain state be $M$, wire/request/response DTO shapes be $D_{in},D_{out}$, and explicit mappings be

$$
parse: bytes\rightarrow D_{in},\quad validate/authorize/map:D_{in}\rightarrow Command,
$$

$$
execute:Command\times M\rightarrow Result,\quad assemble:Result\rightarrow D_{out}\rightarrow bytes.
$$

Correctness depends on preserving only declared meaning at each arrow. There is rarely a bijection: server-owned fields are not writable; secrets/internal states are not readable; absence differs from null/default; domain value objects flatten or format; compatibility may accept several input versions while emitting one output version. A general reflection copier cannot prove these policies.

### Critical invariants

- Every DTO has one named boundary, direction, audience, owner, schema/version and semantic purpose.
- Input mapping allow-lists writable fields; client identity, tenant, role, price, status, revision and audit fields are server-derived unless explicitly delegated.
- Structural parsing/validation precedes application use, but domain/business invariants are enforced by the domain/application transaction.
- Omitted, null, empty, zero, false and default have explicit distinct/equivalent semantics.
- Response mapping exposes only authorized/classified data and stable public states; no secrets or ORM/lazy proxies leak.
- Domain values have canonical wire representations for money, time, identifiers, enums, precision and locale.
- Mapping failures are path-specific, stable and do not echo sensitive payloads.
- Additive/evolution rules are tested against old readers/writers; unknown-field behavior is intentional.
- DTO size/depth/count and deserialization work are bounded before expensive allocation/use.
- Generated schema/code and handwritten mapping have named authority; round-trip tests do not assume lossy mappings are inverses.

### Common failures

Common failures include using one class for request, response, domain and database; auto-mapping every matching property; accepting `role`, `tenant_id`, `price` or `status`; treating missing as null; exposing password hash/internal fraud state; serializing lazy ORM graphs/cycles; binary floats for money; locale-dependent dates; timezone-less timestamps; unstable enum ordinals; accepting unknown fields silently where typos are dangerous; rejecting all unknown response fields and breaking forward compatibility; unbounded nested collections; “version” fields with no compatibility policy; DTO-per-layer ceremony inside one process; mapping libraries that hide ownership; and tests that compare only happy-path JSON snapshots.

### Compact example

`CreateUserRequestV1` accepts `display_name` and optional `nickname` with explicit presence. It cannot carry server `id`, tenant, role, password hash, status or revision. The boundary validates size/Unicode shape, derives tenant/principal from authenticated context, maps to `CreateUser` command, and the domain enforces uniqueness. `UserResponseV1` exposes id, display name and revision; internal risk flags are omitted. PATCH distinguishes nickname absent (no change), null (clear) and value (set).

### Connections

[SEPAT-025](025-facade.md) and [SEPAT-063](063-message-translator.md) help define coarse/translated boundaries, [SEPAT-052](052-domain-model.md), [SEPAT-057](057-data-mapper.md) and [SEPAT-091](091-repository.md) show models that DTOs must not replace or leak. The successor [Change Data Capture Pattern](../ROADMAP.md) exposes durable database changes and requires an even sharper distinction between physical row shape and governed integration contract.

## Governing Question

How should engineers design, map, validate, evolve and secure boundary data shapes so they optimize communication and protect model ownership without duplicating types pointlessly?

The original DTO pattern addressed expensive remote calls: rather than many fine-grained calls on remote objects, transfer a coarse data carrier. Modern APIs and messaging routinely use serialized request/response/event shapes. The durable lesson is boundary-specific representation. The pattern is not “all objects without methods are DTOs” and not a requirement to clone every type between adjacent local functions.

## Why This Matters

Directly serializing domain or ORM objects looks efficient at first. It couples public compatibility to private refactoring, exposes fields accidentally, invites mass assignment, triggers lazy queries/cycles, and confuses client input with server state. A database column rename becomes an API break; a new sensitive property may appear automatically; client-supplied role can overwrite authority.

DTOs make contracts reviewable and independently evolvable. They also impose mapping code, duplication, allocation and drift risk. The right question is whether a real boundary has different ownership, trust, performance or evolution forces. Across a network/process, durable queue, plugin/FFI, public API or independently versioned package, the answer is often yes. Between every service and helper in one process, local DTO layers can become ceremony.

DTO design intersects compatibility, security and semantics. A JSON field absent versus `null`, proto scalar presence, timezone precision, enum evolution or partial update can change business behavior. Schemas validate shape, but they cannot decide whether the caller may set a role or whether an amount is legal in current domain state.

## Prerequisites and Retrieval

Learners should retrieve:

- remote facade, serialization, network call cost and coarse-grained APIs;
- domain entities/value objects/aggregates and application commands/results;
- persistence records, Repository and Data Mapper;
- JSON/object-schema and binary protocol presence/evolution semantics;
- authentication, authorization, tenant derivation and data classification;
- validation layers, error contracts and Unicode/numeric/time representations;
- backward/forward compatibility, consumer/provider contract tests;
- memory/CPU limits, recursive/nested payload attacks and observability privacy.

Before continuing, explain why accepting a deserialized `User` domain object from an HTTP request can simultaneously create a compatibility problem and an authorization vulnerability.

## Learning Objectives

After this module, learners can:

1. state the original DTO forces and distinguish useful boundaries from local ceremony;
2. distinguish DTO, domain entity/value, persistence record, command, event and view model;
3. design separate input/output/update shapes with explicit ownership;
4. specify omitted/null/default/empty presence semantics;
5. map allow-listed fields and derive authoritative values from trusted context;
6. choose canonical money/time/ID/enum/numeric representations;
7. evolve schemas using tested reader/writer compatibility policy;
8. bound deserialization, nesting, collections and sensitive telemetry;
9. test mapping, compatibility, security and lossy/asymmetric behavior;
10. decide when generated mapping or direct local types are more appropriate.

## Core Exposition

### Recover the original pattern forces

In Fowler's distribution pattern, remote calls are expensive. Fine-grained domain objects encourage chatty calls and proxy illusions. A DTO aggregates required data into one serializable object; an assembler maps between it and domain objects. The DTO has fields/accessors but little behavior because its job is transfer.

Today HTTP/gRPC/message boundaries already encourage coarse messages, but the same forces remain: latency, serialization, failure, trust and independent deployment. A DTO can also stabilize a public contract while domain/storage models evolve. Do not reinterpret that as “a DTO between every method.” Fowler later warned about local DTO use without a remote/boundary need.

Name the cost it addresses: fewer calls, controlled shape, trust boundary, versioned compatibility, language neutrality or restricted data exposure. If none applies and the models are semantically identical under one owner/version, direct types may be clearer.

### Distinguish neighboring representations

**Domain entity.** Has stable identity, encapsulated behavior/invariants, and relationships within aggregate rules. It may contain private state not serializable.

**Value object.** Represents a domain concept through values/equality/behavior (Money, DateRange). It is not the historical “Transfer Object” synonym.

**Persistence record.** Encodes columns/keys/nullability/normalization/tracking. It may flatten or split domain concepts and include internal metadata.

**Request DTO.** Untrusted candidate data with presence and syntactic constraints. It does not carry authenticated authority merely because fields are named `tenant_id` or `role`.

**Command.** Trusted-enough application intent assembled after structural validation and contextual authorization/derivation. Domain execution can still reject it.

**Response DTO.** Authorized public projection of a result, often tailored to use case and media/version.

**Event.** Immutable past-fact contract with identity/time/source/replay/evolution semantics. Its envelope/payload are data carriers, but calling it DTO can obscure those semantics.

**View model.** Data/behavior tailored to a UI rendering/interaction. It may overlap response DTO but ownership/audience differ.

Reuse only when semantics, trust, presence and evolution are genuinely identical—not because property names match today.

### Make direction and authority explicit

Separate create/update/response DTOs. A response might contain `id`, `status`, `revision`, computed totals and links that requests must not write. A PATCH/update DTO needs field presence; a create DTO may require values; a replace DTO may define full resource semantics.

Mapping is an allow-list:

- accept only documented writable fields;
- derive principal/tenant/scopes from authenticated context;
- derive server time, IDs, revision and audit source internally;
- load authoritative price/rate/permissions from trusted systems;
- ignore or reject read-only fields according to a documented contract;
- never reflection-copy arbitrary input onto domain/persistence objects.

Rejecting unknown input fields can catch typos/security probes, but may impede forward-compatible clients/proxies. Ignoring unknown fields supports additive evolution but can hide misspellings. Choose per boundary/version and record/observe safely. Do not accept a known forbidden field just because unknowns are ignored.

The assembler belongs at the boundary/application translation edge. Domain code should not know JSON/OpenAPI/protobuf annotations; persistence mapper should not decide public exposure. Avoid a single omniscient mapper that translates every representation bidirectionally.

### Layer validation correctly

DTO/schema validation handles representation:

- parse correctness, type, required/presence;
- length/count/depth/range/format bounds;
- known enum/discriminator/version;
- cross-field constraints intrinsic to request shape;
- canonical encoding where required.

Application/domain validation handles current truth:

- authorization and tenant relationship;
- uniqueness/current state/version;
- credit/stock/policy/business rules;
- aggregate invariants under transaction;
- external authority/revocation.

Do not duplicate domain rules into generated DTO validators and assume they remain synchronized. Early boundary bounds protect resources; authoritative rules still run transactionally. Error responses distinguish syntactic path errors, authorization concealment, conflict/version and domain rejection without exposing internals.

### Field presence is semantic

For updates, these can differ:

- field omitted: leave unchanged;
- field present with null: clear value;
- empty string/list: set empty (or invalid by contract);
- zero/false: set legitimate default-valued value;
- field present with value: set value.

Language defaults can erase distinctions. JSON object membership preserves missing versus explicit null if the parser/model does. Protocol Buffers has implicit versus explicit presence disciplines; current official guidance recommends explicit `optional` for proto3 basic types when presence matters. OpenAPI/JSON Schema `required`, type including null and directional annotations must be interpreted carefully.

Do not use sentinel magic values such as `0 means absent` if zero is valid. Represent a patch as typed operations/presence wrappers and test every combination. Replacing versus merging collections needs explicit semantics.

### Canonical scalar and structured representations

**Money.** Use decimal string or integer minor units plus ISO currency under explicit scale/rounding; binary floating point can alter value.

**Time.** Use RFC 3339/ISO 8601 profile with timezone/offset and declared precision; distinguish instant, local date/time and duration. Preserve occurrence versus processing time.

**Identifiers.** Use opaque stable strings with format/length bounds; clients do not infer database type or authorization from ID.

**Enums.** Use stable symbolic values, reserve/handle unknowns and never expose ordinal positions. Removing/reinterpreting values is breaking.

**Numbers.** JSON consumers may not preserve arbitrary integer/decimal precision. Define ranges/string encodings where cross-language loss matters.

**Text.** Define Unicode normalization/case/length in code points/bytes/graphemes only where domain/security requires; bound encoded bytes too.

**Collections.** Define maximum, ordering, duplicates, paging and partial/complete semantics. Avoid recursive unbounded graphs; use IDs/links/pages.

### Deterministic asymmetric mapping model

The following pure model constructs a response allow-list, demonstrates absent/null/value presence, and ignores a client-supplied role rather than mapping it to authority.

<!-- bijux-verify: {"id":"sepat-092-dto-boundary","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"response-fields=display_name,id,revision\nsecret-exposed=no\nnickname-states=absent,null,value:\noverpost-role=ignored\n","stderr":""}} -->
```python
domain_user = {
    "id": "u-17",
    "display_name": "Ada",
    "revision": 4,
    "password_hash": "internal",
    "risk_flag": "review",
}
response_fields = ["id", "display_name", "revision"]
response = {name: domain_user[name] for name in response_fields}

def nickname_state(payload):
    if "nickname" not in payload:
        return "absent"
    if payload["nickname"] is None:
        return "null"
    return "value:" + payload["nickname"]


payloads = [{}, {"nickname": None}, {"nickname": ""}]
untrusted_create = {"display_name": "Ada", "role": "administrator"}
writable = {"display_name"}

print("response-fields=" + ",".join(sorted(response)))
print("secret-exposed=" + ("yes" if "password_hash" in response else "no"))
print("nickname-states=" + ",".join(nickname_state(item) for item in payloads))
print("overpost-role=" + ("accepted" if "role" in writable else "ignored"))
```

This execution proves fixed dictionary allow-list and presence branches only. It performs no serialization, schema validation, authentication, authorization, domain transaction, Unicode/numeric/time mapping, compatibility negotiation, allocation limit or sensitive-data analysis.

### Serialization and assembler ownership

Serialization turns DTO to bytes/media and back. Keep serializer concerns—field names, wire tags, codecs—at boundary packages. A DTO can be generated from an authoritative schema, handwritten and checked against schema, or schema generated from code; select one source of truth and detect drift.

Mapping is often asymmetric and lossy:

- domain Money maps to `{amount,currency}` but input cannot reconstruct exchange policy;
- internal state maps several values to one public state;
- response omits secret/tenant internals;
- input display name maps through normalization but output returns canonical form;
- links/permissions depend on viewer context, not entity alone.

Therefore `fromDto(toDto(x)) == x` is not a universal oracle. Test declared round trips for lossless value subsets, and explicit projections/omissions for lossy mappings. Mapping code should be reviewable; generated/reflection mappers require allow-lists and golden/contract tests.

### Evolution and compatibility

Define a reader/writer matrix. Typical tolerant-reader/additive rules:

- old readers ignore new optional response/event fields if their parser permits;
- new readers accept old payloads and supply semantic defaults only when valid;
- writers do not change meaning/type of an existing field;
- rename is add-new + dual-read/write/migration/deprecation, not silent replacement;
- required input additions are breaking unless negotiated/defaultable;
- enum additions require unknown-value behavior;
- numeric range/precision tightening can break existing values;
- field reuse after removal is forbidden in tagged binary protocols and hazardous elsewhere.

Version only when needed and define negotiation/media/topic/package. A `version: 2` field without supported versions/transition policy is decoration. Prefer additive compatible evolution where semantics allow; create a new endpoint/message type when meaning changes.

Contract tests include old client fixtures against new provider and new client/reader against old payload fixtures. Preserve serialized golden fixtures, not only generated classes. Test absent/null/default and unknown fields across languages/toolchains.

### Performance and resource safety

DTO coarse-graining reduces round trips but can overfetch. One enormous graph increases latency/memory, privacy exposure and retry cost. Shape by use case, page/stream large collections, compress only with bomb/ratio limits, and bound:

- body bytes before buffering;
- nesting depth, fields/object and collection counts;
- string/decoded bytes and number ranges;
- decompressed size/work;
- parse/map/validation time;
- response bytes and fan-out/source work.

Batch DTOs need per-item identity/result, maximum size and atomicity semantics. Partial failure must not be hidden by one success status. Avoid fine-grained remote DTO methods; the carrier should remain inert/serializable.

### Security and privacy

Mass assignment is prevented structurally by separate input type and allow-listed mapping, then authorization. Deny-listing `password_hash` fails when new sensitive fields appear. Responses use allow-lists/data classification/viewer policy. Beware indirect exposure through nested objects, error echo, logs/traces, generated `toString`, schema examples and caches.

Treat deserialization as hostile input. Avoid polymorphic type instantiation from untrusted class names. Validate discriminators against an allow-list. Prevent prototype/object injection in applicable languages, duplicate-key ambiguity, billion-laughs/entity expansion in relevant formats and parser differentials. Authenticate/sign exact canonical bytes only with a specified canonicalization.

DTOs do not authorize themselves. A field called `is_admin` remains untrusted. Server attaches principal/tenant and current policy outside the payload. Redact/minimize regulated data and define retention/erasure for captured payload evidence.

### Testing and evidence

Tests should cover:

- exact schema/wire fixtures and generated-code drift;
- every required/optional/absent/null/default/empty combination;
- allow-listed input, server-owned over-post and nested injection;
- secret/internal omission under every response variant/viewer;
- domain value precision/rounding/timezone/Unicode/enum unknowns;
- old/new reader-writer compatibility and version negotiation;
- size/depth/count/decompression/parser limits;
- deterministic mapping and path-specific errors;
- concurrency/version fields and idempotency fingerprint stability;
- fuzz/property tests plus cross-language golden vectors;
- batch partial results and pagination order/cursors.

Schema validation proves conformance to the tested schema, not business authorization, domain correctness or absence of all sensitive inference. Named domain/security/privacy/legal reviewers are required for high-stakes exposure decisions.

## Definitions and Notation

Let input/output DTO schemas be $D_{in}^v,D_{out}^v$, wire bytes $B$, parse/serialize $P_v,S_v$, boundary mapping $m_{in}:D_{in}\times Context\to Command$, result projection $m_{out}:Result\times Viewer\to D_{out}$, presence state $\pi_f\in\{absent,null,default,value\}$, and reader/writer versions $R_i,W_j$.

Let classified field set $F$, writable allow-list $A_w\subset F$, visible set $A_r(viewer)\subset F$. Correct mapping is generally partial/asymmetric: $m_{out}$ need not be invertible and $m_{in}$ must not accept $F\setminus A_w$.

## Mechanisms, Invariants, or Proof Structure

**Call reduction.** A coarse DTO transfers needed data in one remote call rather than multiple fine-grained calls, at the cost of larger payload/overfetch. Measurement selects granularity.

**Mass-assignment safety.** Separate input DTO plus allow-list means fields outside $A_w$ cannot reach command/domain mutation through the mapper. Reflection/unknown alternate paths invalidate the argument.

**Exposure safety.** Allow-listed contextual projection exposes only $A_r(viewer)$; adding a new domain/persistence field does not automatically add output. Derived/inference risks still require review.

**Presence correctness.** Preserving $\pi_f$ lets PATCH distinguish no-change, clear and set-default/value. A language/model that collapses presence breaks this contract.

**Compatibility.** If old reader ignores unknown optional fields and new writer preserves old field meaning, an additive field is backward compatible for that pair. Required/type/meaning changes need separate proof/migration.

**Mapping ownership.** Explicit arrows isolate wire/domain/storage change. One shared class collapses arrows and couples all owners/releases.

**Bounded parsing.** Enforced byte/depth/count limits cap named resource dimensions; they do not prove constant CPU or eliminate parser vulnerabilities.

## Alternatives and Trade-Offs

| Alternative | Prefer when | Limitation or cost |
|---|---|---|
| direct domain/value type | same-process owner and semantics/trust/evolution match | leaks when boundary diverges |
| dedicated request/response DTOs | remote/trust/compatibility/exposure differ | mapping/duplication/drift |
| generated schema-first types | multi-language governed wire contract | generator/runtime coupling and custom mapping remains |
| code-first schema generation | one-language domain team and tooling control | accidental code annotations can define public API |
| dynamic map/document | highly dynamic extension data is required | weak discoverability/validation/compatibility |
| persistence record as DTO | internal controlled CRUD with intentionally shared schema | couples database evolution and exposes internals |
| domain event contract | immutable fact/replay semantics are required | not interchangeable with request/response carrier |
| pagination/stream | large result sets | protocol/state/backpressure complexity |
| local DTO layer | truly independent local module/version/trust boundary | otherwise ceremony and mapping drift |

## Failure Modes and Misconceptions

- **DTO means any object with fields.** Purpose is boundary transfer; context matters.
- **DTO is a domain Value Object.** Value Objects have domain equality/behavior; terms differ.
- **One model reduces duplication safely.** It couples trust, storage, domain and public evolution.
- **Schema validation enforces business rules.** Current invariants/authorization require domain/application context.
- **AutoMapper removes mapping decisions.** Matching names do not prove authority/semantics.
- **Unknown fields should always be ignored/rejected.** Compatibility/security policy decides by direction.
- **Missing and null are equal.** PATCH and presence-sensitive protocols often differ.
- **Zero means absent.** Zero/false may be valid values.
- **Response DTO can be reused as request.** Server-owned/read-only fields invite over-posting.
- **Enums can use ordinals.** Reordering/additions break meaning.
- **ISO-looking time is enough.** Offset, precision and instant/local semantics matter.
- **DTOs eliminate chatty design.** Poorly shaped endpoints can remain chatty or overfetch.
- **Generated types eliminate compatibility testing.** Old/new cross-version behavior still needs fixtures.
- **Round-trip equality proves mapping.** Many safe projections are intentionally lossy/asymmetric.
- **Local DTOs always improve architecture.** Without a real boundary they can be empty ceremony.

## Worked Examples

### Example 1

A remote album UI calls once per album, artist and track. A coarse `AlbumDetailsResponse` includes the needed summary and bounded track page in one call. Payload/call measurements choose granularity; it does not expose mutable domain objects. This is the original remote-call DTO force.

### Example 2

An HTTP create endpoint deserializes an ORM `User` including `role`, `tenant_id`, `status` and `password_hash`. Auto-save grants admin. A dedicated request accepts display name/email only; mapper derives tenant/principal, server assigns role/status/hash/revision, and domain enforces uniqueness.

### Example 3

PATCH `{}` should leave nickname, `{"nickname":null}` clears it, and `{"nickname":""}` sets empty only if allowed. A generated model collapses all to null. Enabling explicit presence/wrapper and mapping three typed operations restores semantics; tests cover each.

### Example 4

Domain Money €12.345 under currency scale/rounding is serialized as binary `12.345`; another language observes a different value. Contract uses decimal string plus currency and declared rounding/scale validation. The domain constructs Money only after syntactic checks.

### Example 5

A response serializes ORM order with lazy customer/lines/payments, producing N+1 queries, a cycle and internal fraud flag. An explicit assembler selects a bounded authorized projection in one designed query, omits risk state and emits links/IDs instead of recursive graphs.

### Example 6

Provider adds optional `middle_name`; old tolerant readers ignore it and new readers accept old absence. Renaming `name` to `display_name` directly breaks readers. Migration adds new field, continues old meaning, dual-reads/writes under policy, measures adoption, then versions/removes only through published process.

### Example 7

An enum adds `SUSPENDED`. Old mobile code crashes on exhaustive unknown. Contract defines unknown fallback that does not grant access; generated client fixtures verify it. Security-critical state defaults closed/explicit, while UI can label unsupported state without inventing normal.

### Example 8

A batch request accepts 100,000 nested items and decompresses gigabytes before validation. Boundary caps compressed/decompressed bytes, nesting, items and per-string sizes before expensive mapping; batch returns per-item identities/results with declared partial atomicity.

### Example 9

An internal helper maps `Customer` to an identical `CustomerDto` and back solely to satisfy a layer rule. Both modules deploy together; no trust/evolution/call boundary exists. Removing the DTO reduces drift. A public API keeps dedicated DTO because exposure and compatibility genuinely differ.

### Example 10

A clinical response omits diagnosis code but exposes medication/clinic/time combinations that infer it. Field allow-list alone is insufficient. Privacy/domain reviewers perform inference/threat analysis, minimize/coarsen data by audience and verify access/audit. Automated schema tests confirm mechanics, not clinical/privacy adequacy.

## Cross-Program Connections

- [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md): DTOs protect aggregate/value/domain semantics from boundary representation.
- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md): remote facades, dependency direction and independent evolution.
- [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md): contract, golden, fuzz, property and cross-version tests.
- [Compilers and Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md): parsing, AST/IR separation, code generation and schema evolution analogies.
- [Security Engineering](../../25-security-engineering/ROADMAP.md): mass assignment, parser attacks, authorization, classification and inference/privacy.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md): OpenAPI/protobuf, pagination, error, media/version and compatibility contracts.

## References

1. Fowler, Martin. “Data Transfer Object.” *Patterns of Enterprise Application Architecture* catalog. <https://martinfowler.com/eaaCatalog/dataTransferObject.html>
2. Fowler, Martin. *Patterns of Enterprise Application Architecture*. Addison-Wesley, 2003.
3. Fowler, Martin. “Local DTO.” 2004. <https://martinfowler.com/bliki/LocalDTO.html>
4. Alur, Deepak, John Crupi, and Dan Malks. *Core J2EE Patterns*, 2nd ed. Prentice Hall, 2003.
5. Bray, Tim. “The JavaScript Object Notation (JSON) Data Interchange Format.” RFC 8259. <https://www.rfc-editor.org/rfc/rfc8259>
6. OpenAPI Initiative. “OpenAPI Specification 3.1.1.” 2024-10-24. <https://spec.openapis.org/oas/v3.1.1.html>
7. JSON Schema Authors. “JSON Schema Validation Draft 2020-12.” <https://json-schema.org/draft/2020-12/json-schema-validation>
8. Protocol Buffers Authors. “Application Note: Field Presence.” <https://protobuf.dev/programming-guides/field_presence/>
9. Protocol Buffers Authors. “Updating a Message Type.” <https://protobuf.dev/programming-guides/proto3/#updating>
10. OWASP Foundation. “API6:2019 Mass Assignment.” <https://owasp.org/API-Security/editions/2019/en/0xa6-mass-assignment/>
11. Nottingham, Mark, and Roy Fielding. “HTTP Semantics.” RFC 9110. <https://www.rfc-editor.org/rfc/rfc9110>
12. Unicode Consortium. “Unicode Standard Annex #15: Unicode Normalization Forms.” <https://unicode.org/reports/tr15/>

The original DTO material and current OpenAPI 3.1.1, JSON Schema 2020-12 and Protocol Buffers presence guidance were checked on 2026-08-29. Generator/parser/unknown-field/presence behavior is language/runtime/version specific and must be verified with actual toolchains and fixtures.

## Exercises

### Exercise 1

Design create, patch and response DTOs for a user resource. Classify every field by source/authority/presence/exposure and define mapping arrows.

### Exercise 2

Derive compatibility outcomes when v2 adds optional `nickname`, adds required request `country`, extends enum status, and changes integer cents to decimal-string amount.

### Exercise 3

Diagnose an API that uses one ORM entity for request/response, reflection mapping, nullable PATCH, float money, local timestamps, ordinal enums, lazy graphs and unbounded arrays. Redesign and specify evidence.

### Exercise 4

Decide whether DTOs are justified between: public API/domain; domain/repository; two functions in one package; service/message broker; independently versioned plugin/host; query projection/UI. Explain mapping ownership.

### Exercise 5

Design DTOs for a regulated high-stakes decision result, including inference risk, authorization, precision, explanations, versioning, redaction, audit and named review.

## Answers to the Exercises

### Answer 1

`CreateUserRequestV1`: display name and email required; nickname optional with create semantics; no id/tenant/role/status/revision/hash/risk. `PatchUserRequestV1`: presence-aware display name/email/nickname operations; omitted=no change, nickname null=clear if policy permits, empty validated separately. `UserResponseV1`: public ID, canonical display/email per viewer policy, nickname, public status, revision and links; never hash/risk/internal tenant policy.

Parse/bound DTO, authenticate context, allow-list fields, derive tenant/principal/server time, map to `CreateUser`/`PatchUser(expected_revision)` command. Domain transaction enforces uniqueness/current version/rules. Assembler maps result plus authorized viewer to response. Errors map at boundary. Document unknown-field policy and canonical ID/time/text. Tests over-post role/tenant/status/hash, all presence states, authorization/exposure and old/new fixtures.

### Answer 2

Adding optional response `nickname` is backward compatible only if old readers tolerate unknowns; new readers must accept absence from old writers. Adding required request `country` breaks old writers unless server can supply a semantically valid default/context or new version/negotiation is used.

Adding enum status breaks old readers that assume exhaustiveness; define unknown behavior, preserve safe authority and test generated clients. Changing cents integer to decimal string changes type/unit and is breaking if done in place. Add a new field with explicit amount/currency/scale, dual-emit/read under version policy, reconcile values and deprecate the old field through measured migration. Never reinterpret existing cents silently.

### Answer 3

One ORM model leaks storage/tracking/sensitive fields and permits mass assignment. Reflection mapping hides authority. Nullable PATCH collapses missing/null. Float money loses decimal precision; local time lacks instant/zone semantics; enum ordinal is unstable; lazy graph triggers I/O/cycles/exposure; arrays exhaust resources.

Create separate allow-listed request/patch/response DTOs and application commands. Preserve presence. Use decimal string or minor units+currency, RFC 3339 instant with precision or typed local date/time, symbolic enums with unknown policy, explicit bounded projections/IDs/pages, and server-derived authority. Keep ORM behind Data Mapper/Repository. Enforce byte/depth/count/decompression limits. Evidence includes schema/golden/cross-language fixtures, over-post/security/fuzz tests, precision/time/Unicode vectors, old/new compatibility, lazy-query count absence, authorization/redaction and real mapping integration.

### Answer 4

Public API/domain: yes—remote, trust, compatibility and exposure differ; boundary assembler owns it. Domain/repository: normally use domain aggregates/value types because Repository's purpose is reconstructing them; persistence records are mapped inside infrastructure, not called public DTOs. Same-package functions: no unless a real semantic/version boundary exists.

Service/broker: yes, but define message as command/event contract with identity/replay/evolution, not merely “DTO.” Plugin/host: yes when independently versioned/possibly different ABI/trust; use stable schema and adapters on each side. Query projection/UI: often a tailored response/view model is justified to avoid aggregate leakage/overfetch; query/application boundary assembles it. Reuse only if ownership, semantics, direction and evolution match exactly.

### Answer 5

Define separate request and result DTO versions with authenticated subject/case identity derived or constrained, decision ID, outcome from a stable symbolic vocabulary, model/policy version, evidence timestamp/validity, precision/units, bounded explanation/reason codes, uncertainty and appeal/human-review status. Do not expose internal features/secrets or accept client-selected outcome/role/model version. Viewer-specific projection minimizes fields and accounts for inference from combinations.

Use exact decimal/time/identifier encodings, explicit missing/null, signed/auditable canonical bytes where required, size limits and unknown-enum fail-safe behavior. Domain decision remains authoritative; DTO/schema validates representation only. Version additively where meaning remains, otherwise new contract with old/new fixtures and retention. Logs use IDs/classification, not payloads; audit stores authorized disclosure and policy/version.

Named domain, legal/regulatory, privacy, security, model/risk, accessibility/human-factors and operations reviewers approve semantics, explanation sufficiency, inference/redaction, appeal and migration. Automated schema/mapping/security tests prove the tested mechanism, not fairness, legality or decision adequacy.
