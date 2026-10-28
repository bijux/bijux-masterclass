---
module_id: API-052
program: API & Service Engineering
level: 2
module_number: 52
title: Protocol Buffers and Schema Evolution
status: complete
last_verified: 2026-09-02
---

# Protocol Buffers and Schema Evolution

## One-Page Review

### Governing question

How can a Protocol Buffers message evolve while old and new producers, consumers, stored bytes, relays, JSON gateways, and generated runtimes coexist without corrupting meaning or losing data?

### Essential definitions

- A **schema** assigns stable field numbers, types, names, presence, cardinality, enums, and message structure.
- A **tag** encodes a field number and wire type as $(field\_number\ll3)\mathbin{|}wire\_type$.
- A **wire type** tells a parser how to skip or decode a payload; it is not the full declared type.
- An **unknown field** is a well-formed field absent from the reader's schema; binary runtimes normally retain it for reserialization.
- **Wire-safe** evolution preserves correct old/new binary exchange; **wire-compatible** evolution parses but may lose or reinterpret data; **wire-unsafe** evolution can corrupt or reject data.
- **Presence** distinguishes “not supplied” from a supplied default value where the schema supports it.
- A **reserved** number/name prevents accidental reuse after deletion.
- **version skew** means producers, consumers, schemas, generated code, and runtimes run different supported versions.
- **semantic compatibility** preserves business meaning, which wire decoding alone cannot guarantee.

### Central model, mechanism, or theorem

For field number $n$ and wire type $w$,

$$
tag=(n\ll3)\mathbin{|}w,\qquad n=tag\gg3,\qquad w=tag\mathbin{\&}7.
$$

The wire carries $n$, $w$, and payload—not the field name or complete declared type. Therefore field-number identity is permanent. A safe rolling change must satisfy both binary interpretation and domain meaning for every supported writer/reader pair:

$$
\forall (W_i,R_j)\in S:\ decode_{R_j}(encode_{W_i}(m))\text{ preserves required meaning}.
$$

Adding an optional field with a fresh number is usually binary-safe because old readers skip/retain it. Reusing a number, changing incompatible type/cardinality, or altering an existing field's meaning is unsafe even if new code compiles.

### Critical invariants

Never reuse a field number; reserve deleted numbers and names. Treat package/message/field identity as a governed API. Add rather than reinterpret. Model presence deliberately. Put an unspecified zero enum value first and handle unknown numeric values. Preserve unknown fields through binary parse/serialize and message-aware copy paths. Do not assume field order or default serialization bytes are stable. Bound message size, nesting, repeated counts, strings/bytes, and decompression before expensive work. Separate RPC messages from durable storage schemas when lifecycles differ. Test old writer/new reader, new writer/old reader, old/new relay, JSON/text gateways, all supported languages, generated-code/runtime combinations, rollback, and stored-data replay. Deploy readers before writers when new data needs tolerant readers; observe unknown/default/validation behavior. Wire compatibility does not authorize a behavior change.

### Common failures

Changing or recycling tag numbers; renaming without considering JSON/TextFormat; changing type because it shares a wire type; scalar↔repeated or singular↔map changes; adding required semantics that old writers cannot supply; using zero as a meaningful enum default; assuming closed enums reject future values uniformly; collapsing absent into default; field-by-field copying that drops unknowns; binary→JSON→binary relay loss; signing/hashing nondeterministic serialization; relying on field order; using one schema for API and database forever; changing units or identifier meaning; mixing unsupported generated code/runtime versions; accepting huge nested messages; deploying writers before readers; and testing only new/new.

### Compact example

Version 1 has `string display_name = 1`. Version 2 adds `optional string locale = 2`. A new writer sends fields 1 and 2; an old binary reader understands field 1 and retains field 2 as unknown. If it reserializes the same message through a message-aware binary API, a new reader recovers `locale`. If the old relay converts to JSON, unknown field 2 is lost. **Conclusion:** adding field 2 is binary-safe, but the end-to-end path is safe only if intermediaries preserve unknown data and old behavior tolerates the missing semantic.

### Connections

[Remote Procedure Call Semantics](051-remote-procedure-call-semantics.md) defines the operation contract, [API Contracts and Behavioral Guarantees](021-api-contracts-and-behavioral-guarantees.md) frames semantic compatibility, and [Contract-First and Code-First Workflows](028-contract-first-and-code-first-workflows.md) governs schema change. [Unary and Streaming gRPC](../ROADMAP.md) next composes protobuf messages with concrete call shapes.

## Governing Question

Which aspects of a protobuf definition are permanent wire identity, which changes merely remain parseable, and what evidence proves a rolling ecosystem preserves both bytes and business meaning?

## Why This Matters

Protocol Buffers gives a compact language-neutral binary representation and generated APIs. Its key-value wire records let a parser skip fields it does not know, enabling additive change. That mechanism is powerful but narrower than “schemas are automatically backward compatible.” The wire stores field numbers and coarse wire types, not field names, validation rules, units, permissions, or intent. Two schemas may parse the same bytes and disagree completely about what they mean.

Distributed deployments guarantee skew. Mobile clients may remain old for months. Jobs and event logs preserve old bytes. A server rollback reintroduces an older reader. A relay can parse and reserialize a message. Languages differ in generated APIs and enum/presence treatment. JSON gateways use names and string representations that have different compatibility rules. A change must therefore be evaluated against a matrix of writers, readers, paths, runtimes, and stored data—not only whether the latest compiler accepts it.

The worst mistakes are durable. Reusing field 7 after deleting it can cause old stored values to be interpreted as a new field years later. Changing `int64 amount_cents` into a concept with dollars keeps the same bytes and silently multiplies value. A field-by-field relay compiled from an old schema can erase new information. These failures may not crash; they corrupt meaning.

Good evolution treats a `.proto` file as a long-lived protocol. Field numbers are never recycled, semantics expand conservatively, unknown data survives, deployment order is planned, and compatibility gates run in CI. Editions change language defaults and generated APIs without changing the foundational binary wire contract; teams pin toolchains and migrate deliberately rather than cargo-culting feature settings.

## Prerequisites and Retrieval

Retrieve binary/varint and ZigZag encoding, bit shifts/masks, length prefixes, schemas and generated code, optional/repeated/map/oneof/enum/message fields, default values and presence, RPC/version skew, rolling deployment/rollback, compatibility testing, unknown-field retention, JSON/text encodings, integer range/overflow, UTF-8, resource limits, and supply-chain/toolchain pinning.

Before changing a schema, retrieve every producer, consumer, relay, gateway, storage/log/archive, language runtime, compiler/plugin, supported deployment/rollback path, descriptor registry, validation policy, message size/nesting limit, field ownership, current field-number/name reservations, JSON/TextFormat use, signing/hashing behavior, stored retention horizon, and semantic invariants such as units, identity, authorization, ordering, and required combinations.

## Learning Objectives

By the end of this module, you should be able to:

1. decode protobuf tags and explain how wire types permit unknown-field skipping;
2. distinguish wire-safe, conditionally compatible, wire-unsafe, source, runtime, JSON, and semantic compatibility;
3. evolve field numbers, presence, enums, oneofs, repeated fields, maps, and nested messages conservatively;
4. preserve unknown data and identify transformations that discard it;
5. plan reader/writer rollout, rollback, migration, and stored-data replay;
6. govern compiler, generated-code, runtime, descriptors, and schema checks; and
7. design a cross-version evidence matrix that tests meaning rather than parse success alone.

## Core Exposition

### Understand what the binary wire actually records

A protobuf message is a sequence of records. Each begins with a varint tag combining a positive field number and one of six wire-type codes. Wire type 0 carries varints; 1 carries 64-bit fixed-width data; 2 carries a length-delimited payload such as string, bytes, embedded message, or packed repeated scalars; 3/4 delimit deprecated groups; 5 carries 32-bit fixed-width data.

The tag formula explains why field numbers 1–15 are compact: shifting them by three still produces a one-byte tag for common wire types. More importantly, field number is the identity. Names exist in schemas and some textual encodings but not ordinary binary records. Renaming a binary field may be safe for binary traffic and breaking for generated source, JSON, TextFormat, reflection, field masks, analytics, or policy configured by name.

Wire type is too coarse to establish declared type. `int32`, `int64`, `uint32`, `uint64`, `bool`, enums, and ZigZag integers use varint records with different interpretation. Strings, bytes, embedded messages, and packed repeated fields are all length-delimited. Changing between them because the record remains skippable can produce overflow, invalid UTF-8, changed sign, lost repetitions, or arbitrary reinterpretation.

Protobuf messages are not self-delimiting: an enclosing transport/file must frame message length. Serialization order is not guaranteed, and default serialization is not a canonical byte representation. Do not compare serialized bytes for semantic equality or sign/hash them without a separately specified canonicalization/profile.

### Derive forward and backward compatibility

Call a change **backward readable** when the new reader can consume old-writer bytes, and **forward readable** when the old reader can consume new-writer bytes. Full rolling compatibility needs both for all supported paths. Parse success is only the first check; required meaning must survive.

Adding an optional field at a fresh number is generally binary wire-safe. New readers see absence in old messages and apply presence/default policy. Old readers see a well-formed unknown record and skip it. If they retain unknowns, a binary relay can round-trip it. But old business logic cannot act on the new field. If `risk_override=ALLOW` changes authorization, an old server ignoring it is not semantically compatible.

Deleting a field from the schema is binary-safe only if its number is never reused and remaining behavior tolerates old writers still sending it. Reserve the number; reserve the name when JSON/TextFormat/name reuse matters. Data does not disappear from old stored bytes merely because the declaration is gone.

A useful review classifies changes:

- **wire-safe:** fresh optional/repeated field, reserved deletion, new enum value with consumers designed for unknown values;
- **conditionally compatible:** certain numeric widening/type changes or packed/unpacked transitions may parse but can lose/overflow data and require controlled rollout;
- **wire-unsafe:** field-number reuse/change, incompatible wire-type change, many cardinality/oneof/map restructures;
- **wire-safe but semantically breaking:** changed units, meaning, validation, authorization, default behavior, identifier namespace, or side effects;
- **binary-safe but JSON/source breaking:** rename or representation change that name-based consumers observe.

Prefer additive replacement: add a fresh field with new semantics, dual-read/dual-write under explicit precedence, migrate producers/data, observe, stop writing old, and eventually reserve old identity.

### Treat presence as information

For a scalar, the value zero/empty/false can mean “caller explicitly chose the default” or “writer did not know/supply the field.” Implicit-presence APIs may collapse these states. Explicit presence (`optional` in modern proto3/editions feature policy, message fields, or oneof) preserves the distinction.

Presence matters for patches, validation, inheritance, policy, and migrations. `retry_count=0` may deliberately disable retries; absence may request a service default. If a new reader interprets absent `currency` as USD, old writers silently choose USD. That can be acceptable only as an explicit semantic compatibility decision.

Avoid adding a logically required field to an established message. Old writers cannot populate it. Instead define tolerant behavior for absence, negotiate a capability/version, or introduce a new operation/message when the invariant cannot coexist. “Required” comments/validators can document a new contract but do not make old bytes contain data.

### Evolve enums for open-world readers

Use a zero-valued `*_UNSPECIFIED` first entry so absence/unknown fallback is not mistaken for a meaningful state. Additive enum values are wire-safe, but old generated APIs may expose unknown numeric values differently. Business code must have an explicit unknown-value policy: preserve and pass through, reject at a trust boundary, map to safe fallback, or stop with an actionable error.

Never use a default branch that grants privileges or triggers an irreversible action for unknown values. Do not exhaustively assume today's values are the universe across a distributed rollout. Renaming an enum symbol may preserve binary numeric representation while breaking JSON strings, source references, dashboards, or configurations. Reusing enum numbers corrupts old data just like field-number reuse.

### Preserve unknown fields end to end

When a new writer sends field 9 to an old binary runtime, the parser normally stores it in an unknown-field set and writes it back. This permits a read-modify-write intermediary to retain future data it does not understand. Preservation is an implementation/path property, not magic.

Unknown fields can be lost when converting to ProtoJSON, copying known fields one by one into a new message, rebuilding from reflection incorrectly, clearing/merging selectively, passing through a runtime/API that discards them, or applying redaction/transformation. TextFormat may print unknown field numbers but is not a safe server interchange format.

Test relays explicitly: new writer → old relay → new reader. Assert unknown bytes/semantic field survive. When a relay intentionally sanitizes messages, decide whether dropping unknowns is a security boundary or compatibility bug. Blind preservation can also forward unvalidated data; trust boundaries may need descriptor-aware allowlists and explicit versioning rather than an accidental proxy.

### Handle repeated, packed, maps, and oneofs carefully

Repeated scalar fields may use packed length-delimited encoding; parsers often accept packed and unpacked forms, but cardinality changes remain risky. Repeated-to-scalar can retain only the last observed value or lose data depending on type/format. Scalar-to-repeated may be conditionally compatible in limited cases, not a general migration plan.

Map fields compile to repeated entry submessages. Changing a map to a repeated message with identical entry layout may be binary-compatible in narrow cases but generated APIs, duplicate-key behavior, ordering, and JSON representation differ. Map iteration/serialization order is not a semantic contract.

A `oneof` represents mutual exclusion and presence. Moving established fields into/out of oneofs can erase information: if an old message contains several fields that a new schema puts in one oneof, parse order may choose a winner, and serialization order is unspecified. Add a new oneof or new message and migrate rather than relying on accidental wire behavior.

Changing a field between an embedded message and bytes shares wire type 2 but changes validation and interpretation. Changing signed encoding (`int32` versus `sint32`) shares wire type yet changes negative values radically. Treat official “conditionally safe” lists as warnings requiring range/data/rollout proof, not routine refactoring permission.

### Separate API, event, and storage schemas

An RPC request represents caller intent and trust-boundary validation; a database record represents internal durable state; an event represents an immutable fact for multiple consumers. Reusing one message for all three couples independent lifecycles and may expose internal fields.

Use purpose-owned messages and explicit mappings. The cost is mapping code and potentially duplicated vocabulary; the benefit is clear ownership, validation, privacy, and migration. Preserve stable domain identifiers and semantics across mappings, but do not serialize generated API messages directly as the only database evolution strategy without a retention/migration plan.

For stored binary messages, catalog schema/edition/compiler metadata, retain descriptors as necessary, and test reading the oldest supported bytes. A schema registry or descriptor set enables lint/breaking-change checks and dynamic decoding, but governance still must decide semantic compatibility.

### Plan rolling deployment and rollback

For a fresh optional field:

1. commit the schema with a fresh number and compatibility evidence;
2. deploy tolerant readers/relays first;
3. deploy writers that populate it, often behind a capability/config gate;
4. observe unknown fields, validation failures, fallback use, and version distribution;
5. make new semantics required only after incompatible writers/readers leave the support window; and
6. preserve rollback to readers that safely ignore/retain the field.

For replacement, dual-read precedence must be deterministic when old and new are both present. New writers may write both during transition if meanings can be represented exactly. Backfills need idempotence and validation. Do not delete/reserve until every producer, consumer, archive/replay, and rollback requirement is addressed; reservation happens when declaration is removed, and persists forever.

Compatibility windows are product policy. A public mobile API differs from a tightly managed internal fleet, but “we deploy together” is not proof: rollback, queues, canaries, jobs, and disaster recovery reintroduce skew.

### Govern editions, compiler, generated code, and runtime

Proto2/proto3 syntax and Protobuf Editions configure language features; runtime release versions are separate. The official support matrix records Editions 2023, 2024, and 2026, with Edition 2026 released 20 August 2026 and requiring protoc 36.0. Editions can change default feature settings and generated APIs while the binary wire format remains stable.

Pin `protoc`, language plugins, runtime dependencies, feature settings, and generated outputs in reproducible builds. Follow each language's cross-version runtime guarantee: generated code and runtime are a coupled artifact, not freely interchangeable. Upgrade in tested combinations, regenerate, inspect source/API changes, and run cross-language golden tests.

Do not adopt an edition merely because it is newest. Inventory feature defaults, generated API changes, symbol visibility/naming, language-specific options, and migration tooling. Specify only understood overrides. A compiler-accepted file establishes syntax validity, not consumer compatibility.

### Bound parsing and validate domain rules

The wire format permits very large length-delimited values and deep nesting in principle; implementations impose limits, but application limits should be much smaller and intentional. Bound framed message bytes before allocation, recursion/nesting, repeated/map entries, string/bytes lengths, decompression ratio, and processing time. Reject malformed/truncated/overlong varints and invalid UTF-8 according to runtime/schema behavior.

Generated types validate wire shape, not business rules. Check range, required combinations, identifier syntax, authorization, canonical units, enum policy, and cross-field invariants after parsing. Unknown fields may contain sensitive future data; logs/debug JSON must not dump messages indiscriminately.

### Build a compatibility evidence matrix

Static checks compare descriptors for field-number reuse, deletion without reservation, unsafe type/cardinality/oneof changes, and package/service breaks. Lint enforces naming/ownership. These are necessary, not sufficient.

Generate golden messages for boundaries: absent/present default, min/max integers, negative ZigZag, unknown enum, unknown fields, repeated packed/unpacked, maps, oneofs, nested/empty/max-sized data, and malformed inputs. Run every supported writer against every reader and relay path. Check semantic results, unknown preservation, reserialization, JSON names/numbers, rollback, and stored replay. Fuzz decoders and enforce resource budgets.

Canary telemetry should use bounded schema/version/outcome attributes, not message bodies. Monitor validation rejects, unknown-enum/field counters where safely available, fallback paths, relay loss, payload distributions, and rollback. A change completes only when compatibility policy and evidence agree.

## Definitions and Notation

Let $S_v$ be schema version/edition state $v$, $W_v$ a writer generated from it, $R_v$ a reader, $m$ a domain message, and $b=encode_{W_v}(m)$ its bytes. Let $N$ be allocated field numbers, $Q$ reserved numbers, $U_v(b)$ the unknown records observed by $R_v$, and $M_v(b)$ the interpreted domain meaning.

**Binary parse compatibility** means $R_j(b)$ accepts well-formed $W_i$ bytes. **Round-trip preservation** means unknown records required by the policy survive $encode_{R_j}(decode_{R_j}(b))$. **Semantic compatibility** means required facts/actions represented by $M_j(b)$ remain within the declared contract. A change is **wire-safe** when official binary rules preserve old/new exchange, **wire-compatible** when bytes parse but may be lossy, and **wire-unsafe** when an old/new pairing can misparse/reject/corrupt.

Permanent identity requires $N\cap Q=\varnothing$ and monotonically accumulating reservations for removed numbers. Field number zero is invalid; protobuf field numbers occupy the documented positive range, with 19000–19999 reserved to the implementation. Presence is modeled as $(present,value)$ rather than value alone when absence carries meaning.

## Mechanisms, Invariants, or Proof Structure

For tag byte sequence beginning with varint value $t$, the low three bits select wire type and the remaining bits select number. The executable decoder checks the canonical example bytes `08 96 01`: tag 8 yields field 1/type 0, while varint bytes `96 01` yield 150.

<!-- bijux-verify: {"id":"protobuf-tag-varint","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"field=1\nwire_type=0\nvalue=150\n","stderr":""}} -->
```python
def read_varint(data, start=0):
    value = 0
    shift = 0
    index = start
    while True:
        byte = data[index]
        index += 1
        value |= (byte & 0x7F) << shift
        if byte < 0x80:
            return value, index
        shift += 7
        if shift >= 70:
            raise ValueError("overlong varint")

wire = bytes.fromhex("08 96 01")
tag, next_index = read_varint(wire)
value, _ = read_varint(wire, next_index)
print("field=" + str(tag >> 3))
print("wire_type=" + str(tag & 0b111))
print("value=" + str(value))
```

Why additive unknown fields work: a reader that does not map $n$ consults $w$ to skip the correct payload extent. If it retains the raw record, later reserialization can carry it. This proof is conditional on well-formed bounded input and the relay/runtime actually preserving unknowns.

Why number reuse cannot be repaired generically: old bytes labeled $n$ contain no schema version/name. A new reader assigning different meaning to $n$ cannot distinguish old-value bytes from new-value bytes using the tag alone. Therefore reserve $n$ forever or introduce an enclosing versioned boundary/migration with external knowledge.

The compatibility gate checks:

$$
\forall(i,j,p)\in Supported:\ Parse\land Bounds\land Preserve_p\land SemanticInvariant.
$$

$p$ includes direct binary, relay, storage replay, and JSON/text routes where supported. Passing descriptor comparison proves only a subset; behavioral fixtures and deployment tests supply the rest.

## Alternatives and Trade-Offs

**Protobuf versus JSON.** Protobuf offers compact typed binary records and unknown-field evolution; JSON is human-readable and ubiquitous but has name/number/presence ambiguities and normally drops protobuf unknown fields. Gateways must honor ProtoJSON-specific rules, not assume binary safety transfers.

**Additive growth versus explicit versioned message.** Additive fields simplify rolling change. A new message/operation is clearer when invariants, units, trust, or shape fundamentally change, at the cost of parallel APIs and migration.

**Implicit versus explicit presence.** Implicit presence is compact/simple when default and absent are equivalent. Explicit presence preserves intent and enables patches, but generated APIs and compatibility policy must handle the extra state.

**Enum versus integer/string.** Enums document vocabulary and generate types but require unknown-value discipline and stable numbers/names. Integers preserve arbitrary values with weaker meaning; strings evolve openly but cost bytes and allow typos. Choose by governance and openness.

**Shared versus purpose-owned message.** Sharing reduces mapping and duplication but couples API, event, and storage lifecycles/privacy. Purpose-owned schemas add mapping work and clearer ownership.

**Binary relay versus decoded transformation.** Opaque relay best preserves unknown bytes but cannot validate/redact semantic fields. Decoded transformation enforces policy but can lose future fields. Define the trust boundary and test the chosen preservation policy.

**Tool-enforced versus reviewed semantic compatibility.** Descriptor tools reliably catch structural breaks; humans/domain tests catch unit, policy, and behavior changes. Neither replaces the other.

## Failure Modes and Misconceptions

- **“The field name is its wire identity.”** Binary identity is the number; names matter in source/JSON/text/reflection.
- **“Deleted means reusable.”** Old bytes and binaries persist; reserve number and relevant name forever.
- **“Same wire type means safe type change.”** Interpretation, ranges, sign, UTF-8, cardinality, and generated APIs differ.
- **“Parse success proves compatibility.”** Meaning can change silently.
- **“Optional additions are always safe.”** Old logic ignores them; required new semantics may fail.
- **“Unknown fields are always preserved.”** JSON and field-by-field copies commonly discard them.
- **“Deterministic serialization is canonical forever.”** Official guidance limits determinism; schema/runtime/language differences remain.
- **“Enum switches are exhaustive.”** Future numeric values can arrive; use safe unknown handling.
- **“Zero can be today's normal state.”** It conflates absence/unknown with a meaningful value.
- **“Repeated and scalar are interchangeable.”** Values can be dropped or last-one-wins.
- **“Map order is stable.”** Map/repeated entry order is not a portable semantic contract.
- **“Oneof is only generated-code sugar.”** It changes presence and winner semantics.
- **“Generated code validates the domain.”** It validates representation, not authorization or business invariants.
- **“RPC messages make good database rows.”** Their ownership, privacy, and migration horizons often differ.
- **“Newest edition should be adopted immediately.”** Feature/generated API changes require a deliberate toolchain migration.
- **“Deploying together eliminates skew.”** rollback, canaries, queues, archives, and offline clients preserve it.

## Worked Examples

### Example 1

**Situation:** Decode bytes `08 96 01`. **Reasoning:** varint tag 8 gives $8\gg3=1$ and $8\&7=0$; the next varint is $(0x16)+(0x01\ll7)=22+128=150$. **Conclusion:** field 1 contains varint 150.

### Example 2

**Situation:** Add `optional string locale = 4`. **Reasoning:** 4 is fresh, old readers can skip length-delimited field 4, and new readers distinguish absent from present empty. Old business logic still ignores locale. **Conclusion:** binary-safe; semantic rollout requires a tolerant default.

### Example 3

**Situation:** Delete field 7, then reuse 7 for `bool approved`. **Reasoning:** stored old varint field 7 may decode as a boolean; bytes carry no old name. Reserving only the name cannot stop numeric collision. **Conclusion:** reserve number 7 and add `approved` at a fresh number.

### Example 4

**Situation:** Change `int32 temperature_c = 3` to mean Fahrenheit. **Reasoning:** every byte still parses, but value 20 changes from comfortable to below freezing. **Conclusion:** wire compatibility masks semantic corruption; add `temperature_f` at a new number or retain canonical units.

### Example 5

**Situation:** A new field crosses an old binary relay. **Reasoning:** message-aware parse/serialize preserves the unknown record; converting to JSON cannot represent the unknown field and drops it. **Conclusion:** test the whole relay path, not only endpoint readers.

### Example 6

**Situation:** Add enum `PAYMENT_STATE_REVERSED=3`; old code switches over known values. **Reasoning:** the numeric value can round-trip, but a default branch that treats unknown as paid is dangerous. Map unknown to non-privileged “unrecognized/pending investigation” while preserving the number. **Conclusion:** additive enum evolution needs open-world behavior.

### Example 7

**Situation:** Move fields `email=2` and `phone=3` into one `oneof contact`. Old bytes contain both. **Reasoning:** the new parser retains only the last oneof member encountered; field order is not guaranteed. **Conclusion:** direct regrouping is unsafe; add a new oneof/message with explicit migration.

### Example 8

**Situation:** Use serialized protobuf bytes as a cache key/signature input. **Reasoning:** logically equal messages may serialize fields in different order; deterministic mode is not a universal cross-version canonical format. **Conclusion:** derive a specified semantic key or standardized canonical signing representation.

### Example 9

**Situation:** New writers require `currency`, but an old mobile client cannot send it. **Reasoning:** rejecting absence breaks forward operation; silently USD may be wrong. Introduce capability/new method or use account currency only when invariant guarantees it, then retire old clients under policy. **Conclusion:** a new logical requirement is not made compatible by an optional wire field.

### Example 10

**Situation:** Migrate API, event, and database messages together to Edition 2026. **Reasoning:** edition and runtime support do not prove generated APIs, feature defaults, plugins, storage replays, or consumers migrate uniformly. Split by owned schema, pin protoc 36.x/toolchains, run descriptor and cross-version fixtures, canary readers, then writers. **Conclusion:** editions are governed toolchain changes, not business-schema version numbers.

## Cross-Program Connections

- **Data Structures:** varints, bit fields, length prefixes, and streaming parsers explain wire efficiency and bounds.
- **Programming Languages:** code generation maps one schema into different presence, enum, ownership, and API models.
- **Distributed Systems:** version skew, rollback, replay, and partial deployment make compatibility a matrix property.
- **Database Engineering:** durable records outlive services, so schema ownership, backfills, and replay govern evolution.
- **Security Engineering:** bounded parsing, unknown data, JSON gateways, descriptors, and generated toolchains are trust boundaries.
- **Testing and Verification:** descriptor diffs, golden bytes, cross-language matrices, fuzzing, and semantic invariants provide layered evidence.

## References

1. Protocol Buffers Authors, “Encoding,” official binary wire-format guide, verified 2026-09-02. [Protocol Buffers documentation](https://protobuf.dev/programming-guides/encoding/).
2. Protocol Buffers Authors, “Language Guide (proto 3),” including field numbering, deletion/reservation, updating message types, and unknown fields, verified 2026-09-02. [Protocol Buffers documentation](https://protobuf.dev/programming-guides/proto3/).
3. Protocol Buffers Authors, “Proto Best Practices,” official schema design and evolution guidance, verified 2026-09-02. [Protocol Buffers documentation](https://protobuf.dev/best-practices/dos-donts/).
4. Protocol Buffers Authors, “Language Guide (editions)” and “Feature Settings for Editions,” verified 2026-09-02. [Editions guide](https://protobuf.dev/programming-guides/editions/) and [edition features](https://protobuf.dev/editions/features/).
5. Protocol Buffers Authors, “Version Support,” including current runtime lines and Edition 2026 release/support data, verified 2026-09-02. [Protocol Buffers documentation](https://protobuf.dev/support/version-support/).
6. Protocol Buffers Authors, “ProtoJSON Format,” official JSON mapping and compatibility rules, verified 2026-09-02. [Protocol Buffers documentation](https://protobuf.dev/programming-guides/json/).
7. Protocol Buffers Authors, “Techniques,” including framing multiple messages, verified 2026-09-02. [Protocol Buffers documentation](https://protobuf.dev/programming-guides/techniques/).

## Exercises

### Exercise 1

For tag varint decimal 42, compute field number and wire type. State what the wire type proves and what it does not prove.

### Exercise 2

Classify these changes: add `optional string note=8`; delete field 5 and reserve it; reuse field 5; change `int32 cents=2` to `int64 cents=2`; change cents to dollars without changing type; add an enum value. Distinguish binary and semantic risk.

### Exercise 3

An old enrichment service parses a new message, copies every known field into a fresh builder, and emits binary. A downstream new reader loses `risk_signal=12`. Diagnose and repair the path while considering a trust boundary that may intentionally strip unknown data.

### Exercise 4

Design a rollout replacing `string address=4` with structured `PostalAddress address_v2=17` across servers, offline clients, a queue retaining 90 days, and database snapshots. Include precedence, dual write/read, rollback, reservations, and evidence.

### Exercise 5

Design a protobuf schema/evolution policy for telemetry emitted by medical infusion pumps that can remain deployed for ten years. Gateways relay binary and JSON; future event fields may be safety-relevant. Specify identity, presence/enums, unknown handling, compatibility window, toolchains, limits/security, rollout, archives, and proof evidence.

## Answers to the Exercises

### Answer 1

$42\gg3=5$ and $42\&7=2$, so it is field 5 with length-delimited wire type. Type 2 proves only how to find the payload length and skip its bytes. Depending on schema, the payload may be string, bytes, embedded message, or packed repeated scalar. It does not prove field name, UTF-8/string meaning, embedded schema, cardinality, validation, units, or authorization.

### Answer 2

Fresh optional note 8 is binary-safe if 8 is unused/unreserved; old readers ignore it, so any required new meaning still needs fallback. Deleting and reserving 5 is binary-safe when behavior tolerates old values; the reservation is permanent. Reusing 5 is wire-unsafe because old bytes can become the new field. `int32`→`int64` shares varint encoding and is listed among conditionally compatible changes, but old readers may truncate/overflow values and rollout/range proof is required; adding a new field is safer. Cents→dollars is wire-parseable but semantically breaking. Adding an enum number is binary-safe, while old clients need safe unknown-value behavior and JSON/source naming must be considered.

### Answer 3

The parser likely retained field 12 internally, but field-by-field reconstruction copied only known fields and discarded its unknown-field set. Use a message-aware copy/merge that preserves unknowns, modify the original message, or explicitly merge unknown fields under the runtime API; add new-writer→old-enricher→new-reader golden tests. If the enricher is a sanitizing trust boundary, blindly forwarding unknown data may violate policy. Then define an allowlisted descriptor/version contract, reject unsupported newer messages, or intentionally strip while surfacing a version/error so callers never assume lossless relay. Binary preservation and security policy must be explicit, not accidental.

### Answer 4

Add field 17 without changing 4. Deploy readers that accept both and define deterministic precedence: if 17 is present and valid, use it; otherwise parse/use 4. Ensure disagreement is logged/rejected under policy rather than silently choosing attacker-controlled data. Deploy writers that populate both only when structured data maps losslessly to the legacy string; retain the same behavior during rollback. Test old/new writer-reader pairs, old relays, queue replay for at least 90 days, snapshot restore, JSON paths, presence, international/boundary addresses, and conflicting dual fields. Backfill database state idempotently and observe legacy reads. After every supported old producer, queued record, snapshot, and rollback expires, stop writing/reading 4, delete its declaration, and reserve number 4 and name `address` permanently. Do not reuse it.

### Answer 5

Give each device/event/message and field a stable governed package/name/number; never reuse numbers, and retain descriptors plus toolchains for the archive horizon. Use explicit presence for measurements/configuration where absent differs from zero, canonical units in names/docs, bounded numeric ranges, and enums beginning `*_UNSPECIFIED=0` with safe unknown handling. Binary gateways preserve unknown fields message-wise; JSON gateways cannot promise that, so they either support only negotiated schemas and reject future safety-relevant fields or carry an authenticated opaque binary envelope alongside JSON. Do not silently round-trip JSON as lossless protobuf.

Support the full ten-year device writer population or negotiate firmware capabilities; deploy tolerant clinical/backend readers before writers, retain rollback, and introduce a new event type when semantics cannot coexist. Pin/sign protoc/plugins/runtimes, store generated descriptor sets and reproducible build metadata, and follow supported generated-code/runtime combinations. Bound frames, nesting, repeated entries, strings/bytes, decompression, and CPU; authenticate devices, authorize commands separately from telemetry, validate units/ranges/cross-fields, minimize logs, and fuzz parsers.

Evidence includes descriptor breaking-change checks, reserved-number registry, golden old/new bytes across every language/runtime, binary-relay unknown preservation, explicit JSON-loss tests, unknown enum/presence cases, malformed/resource cases, archive replay and disaster restore, canary metrics, rollback drills, and clinical review of semantic defaults/units. The policy can prove compatibility only for named device versions, paths, retention, and invariants; unsupported future fields must fail visibly at safety boundaries.
