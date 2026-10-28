---
module_id: DE-004
program: Data Engineering
level: 1
module_number: 4
title: Avro, Protocol Buffers, and Schema-Aware Serialization
status: complete
last_verified: 2026-09-02
---

# Avro, Protocol Buffers, and Schema-Aware Serialization

## One-Page Review

### Governing question

How should a data engineer choose, evolve, identify and operate schema-aware binary records so that independently deployed writers and readers preserve meaning rather than merely decode bytes?

### Essential definitions

- A **schema** declares the named structure, physical types and constraints needed to interpret serialized values; it is not the entire domain contract.
- A **writer schema** is the schema used to encode a datum. A **reader schema** is the schema a consumer expects while decoding it.
- **Schema resolution** maps a writer representation into a reader representation under format-specific matching, promotion, default and alias rules.
- A **field identity** is the durable wire identity of a field: normally a field name in Avro record resolution and a field number in Protobuf binary encoding.
- A **wire type** tells a Protobuf parser how to skip or decode a payload class; it does not identify the declared application type by itself.
- An **unknown field** is a well-formed field not recognized by the reader's schema. Preservation depends on format, runtime and transformation path.
- **Presence** distinguishes an explicitly set field from an unset field. It is separate from a field's returned default value.
- A **logical type** adds a semantic interpretation, such as decimal or timestamp, to an Avro primitive representation.
- A **schema subject** or equivalent governed lineage identifies which schemas may evolve together under one compatibility policy.
- **Backward compatibility** asks whether a new reader can consume old data; **forward compatibility** asks whether an old reader can consume new data.
- **Transitive compatibility** checks a proposed schema against every relevant historical version, not only its immediate predecessor.
- A **schema fingerprint or identifier** is an indirect reference to schema content. It needs a collision, availability, authorization and retention policy.

### Central model, mechanism, or theorem

Represent a boundary by

$$
M=(F,S_w,S_r,E,R,C,D,O),
$$

where $F$ is the format/profile, $S_w$ the writer schema, $S_r$ the reader schema, $E$ the encoder/runtime, $R$ the resolver/runtime, $C$ the compatibility policy and history, $D$ the domain contract, and $O$ the operational envelope. Successful decoding proves only that one implementation found a syntactically permitted interpretation. Trustworthy evolution additionally requires field-identity continuity, directional schema resolution, preserved presence and unknown data, domain-safe values, mixed-version rollout evidence, and reproducible schema lookup.

### Critical invariants

- Every payload can be bound to the exact writer schema or an authenticated, durable identifier for it.
- A field number or Avro field name is never silently reused for a different meaning.
- Compatibility is stated with direction, historical scope, data population, format profile and consumer set.
- Defaults supply a reader value; they do not prove that a writer observed or transmitted that value.
- Missing, null, default-valued and unknown fields remain distinct whenever the domain requires the distinction.
- Unknown fields are preserved across old-reader round trips when forward evolution relies on them.
- Logical types retain precision, scale, unit, epoch and timezone semantics across every target implementation.
- Binary payload framing, size, recursion, decompression and allocation are bounded independently of schema validity.
- Generated code, runtime, compiler, registry client and schema versions stay within documented compatibility guarantees.
- Registry acceptance never substitutes for mixed-version tests, domain invariants, migration planning or observation.

### Common failures

Embedding no usable writer-schema identity; decoding Avro binary with a guessed schema; reusing Protobuf tags; renaming Avro fields without aliases and history tests; treating a wire type as a domain type; adding a reader-required Avro field without a usable default; confusing reader defaults with producer facts; losing Protobuf unknown fields through JSON or field-by-field copying; relying on unstable serialization bytes for hashing; changing numeric representations because their wire types happen to match; changing presence or repeatedness without rollout analysis; using `null` unions carelessly; evolving enum values without unknown-value policy; ignoring logical-type precision; checking only the latest schema; applying the wrong subject strategy; deleting registry history; accepting unbounded messages; and assuming a green compatibility check proves application safety.

### Compact example

An order event is written with Avro schema `OrderCreated` version 1 containing `order_id` and `amount_minor`. Version 2 adds optional `currency` with reader default `"USD"`. A version-2 reader can read version-1 data and obtain `USD`, but the old writer never asserted that currency; the default is an interpretation rule. Separately, a Protobuf message adds `string currency = 3`. An old binary reader can skip and normally preserve field 3, but a JSON conversion or field-by-field reconstruction can discard it. The rollout therefore registers schemas under the correct lineage, tests old/new writer-reader pairs with real values, keeps tag 3 reserved forever if removed, validates currency against business rules, and observes unknown-field loss.

### Connections

[DE-003](003-csv-json-and-line-oriented-formats.md) separates byte decoding, framing, parsing and semantic validation. DE-005 and DE-006 develop Arrow and Parquet, where schema and physical layout interact differently. Schema-aware service messages connect to [API & Service Engineering](../../28-api-and-service-engineering/ROADMAP.md); persistence evolution connects to [Database Engineering](../../18-database-engineering/ROADMAP.md).

## Governing Question

When a producer and consumer use different schema versions, what evidence shows that the decoded value still represents the same business fact?

Binary serialization reduces repeated names and can make boundaries typed, compact and fast. It also relocates meaning outside the payload. Avro binary traverses a writer schema without encoding record field names. Protobuf binary encodes field numbers and wire types, while declared names and application types live in the message definition. Bytes that parse with the wrong schema can therefore yield plausible but false values.

The engineering problem is not “Avro or Protobuf?” It is how the system distributes writer schemas, identifies fields durably, resolves old and new views, tests populated values, handles unknowns and presence, frames messages, constrains resources, and recovers when a change cannot be made compatible.

Apache Avro's [1.12.0 specification](https://avro.apache.org/docs/1.12.0/specification/) defines schemas, binary and JSON encodings, schema resolution, object container files, single-object encoding, canonical form and fingerprints. Protocol Buffers' official [encoding guide](https://protobuf.dev/programming-guides/encoding/) defines numbered tags, wire types, varints and length-delimited values. These mechanisms enable evolution, but neither format knows that `amount=500` means five dollars, five euros or five hundred units.

## Why This Matters

Schema-aware records often become durable organizational memory. They cross service deployments, message brokers, object stores, data lakes, replication systems and language runtimes. A record written today may be replayed after the producer is retired.

Deployment is asynchronous. A new producer can meet an old consumer; a rolled-back service can meet a new message; a batch backfill can combine five historical schemas; a disaster-recovery environment can lack the registry cache used in production. Compatibility must describe all required encounters, not an idealized synchronized release.

Wire compatibility is narrower than application compatibility. Protobuf permits parsers to skip unknown fields because a tag includes a wire type, but an old application may still reject an unknown enum concept or make a wrong decision without a newly added field. Avro resolution may supply a default, yet that default may invent a fact the producer did not know.

Format transitions expose loss. Binary Protobuf normally retains unknown fields in message objects, but the official [proto3 guide](https://protobuf.dev/programming-guides/proto3/) warns that converting to JSON or copying known fields one by one can lose them. ProtoJSON also has different evolution properties because names appear on the wire and unknown fields are generally not propagated.

Registries improve control by storing versioned schemas and enforcing configured checks. Their decision is only as sound as subject identity, policy direction, history scope, reference resolution and format implementation. A registry cannot infer consumer inventories, business invariants, rollout order or whether historical data contains values at a newly dangerous boundary.

Security and reliability remain separate layers. A tiny payload can declare a huge length, nest deeply, expand through decompression, trigger expensive allocation or reference a schema the reader cannot retrieve. Authentication of the transport does not authenticate a public registry response; a valid schema does not authorize access to the data it describes.

## Prerequisites and Retrieval

Retrieve the producer and consumer inventories; exact Avro schemas or `.proto` descriptors; schema lineage/subject naming rules; registry IDs, versions, references and compatibility configuration; representative historical payloads; writer, reader, compiler, code-generator and runtime versions; binary envelope and framing; compression; generated-code options; logical-type adapters; unknown-field behavior; presence discipline; default values; aliases and reserved tags/names; enum handling; maximum message, collection, string, bytes and recursion sizes; retry and replay semantics; data retention; registry backup and availability design; authentication and authorization; language mappings; domain grain, identity, units, nulls and time; migration/backfill plans; rollback windows; and observability for decode, resolution and validation failures.

Distinguish schema syntax from domain contract; writer schema from reader schema; field name from field identity; wire type from declared type; omitted from default-valued; null from unknown; reader default from producer observation; schema version from schema ID; canonical form from original documentation; fingerprint from collision-free identity; backward from forward compatibility; pairwise from transitive checks; wire-safe from source/API-safe and domain-safe; unknown-field parsing from preservation; deterministic serialization within one implementation from canonical bytes across implementations; datum encoding from stream framing; payload schema from envelope schema; generated code from runtime; and migration from ordinary compatible evolution.

## Learning Objectives

After completing this module, you should be able to:

1. explain what schema-aware serialization does and does not prove;
2. trace Avro binary encoding from writer schema through reader-schema resolution;
3. explain Protobuf tags, wire types, varints, length-delimited values and unknown fields;
4. preserve durable field identity and presence semantics during evolution;
5. classify compatibility by direction, transitivity, format and domain effect;
6. govern defaults, aliases, unions, enums and logical types without inventing facts;
7. design a schema-registry lineage, lookup envelope and outage strategy;
8. test mixed writer-reader versions, generated code and runtimes with populated boundaries;
9. bound framing, allocation, recursion, decompression and schema retrieval; and
10. plan explicit migration when a change cannot be made safely in place.

## Core Exposition

### Begin with the domain contract

A serialization schema describes representable structure. Start earlier: define the record grain, business identity, field meaning, units, null and missing states, temporal semantics, privacy class and invariants.

Map that contract into Avro or Protobuf deliberately. A `long` can carry cents, milliseconds, a counter or an identifier. Correct binary decoding cannot distinguish them.

Keep stable domain documentation and conformance tests beside the wire schema. Generated types improve ergonomics; they do not replace meaning.

### Understand Avro's schema dependency

Avro binary encoding follows the writer schema depth-first and left-to-right. Record field names, primitive type markers and separators are not repeated in each datum.

The decoder therefore needs the writer schema. An Avro object container file stores it in file metadata. Single-object encoding prefixes a schema fingerprint. Other envelopes or registries may carry an identifier.

Never decode raw Avro binary from “latest schema.” Latest is not evidence of which schema wrote historical bytes.

### Separate Avro writer and reader schemas

Avro resolution compares the writer schema used for bytes with the reader schema requested by the application. Matching records are resolved by name; fields are matched by name, with aliases available for evolution.

Writer fields absent from the reader are ignored. Reader fields absent from the writer need a reader default or resolution fails. Some numeric promotions are defined.

Test resolution in both required directions. A new reader reading old data and an old reader reading new data are different claims.

### Treat Avro defaults as read rules

An Avro field default is used when the reader has a field that the writer schema lacks. It is not a value automatically written whenever the field happens to equal the default.

Defaults must conform to the field schema. For unions, default and branch ordering require careful specification-level review and implementation tests.

Label default provenance. `currency="USD"` supplied by reader version 2 is derived interpretation, not producer testimony from version 1.

### Govern Avro names and aliases

Named records, enums and fixed types have full names based on name and namespace. Record field matching uses names; aliases can map a writer name to a reader name during resolution.

Renaming without a tested alias can break resolution. Reusing an old name for a new concept can be worse: it may resolve while changing meaning.

Keep a lineage ledger for retired names, aliases and semantic changes. Test against every retained writer schema.

### Use Avro unions deliberately

An Avro union is a JSON array of possible schemas and encodes a branch index before the branch value. `null` plus another type is commonly used for optionality.

Branch order is wire-significant because the index is encoded. Reordering branches changes interpretation. Ambiguous named or promoted branches can surprise readers.

Keep unions narrow, stable and tested. Model domain variants with named records when meaning matters more than primitive convenience.

### Respect Avro logical types

Logical types annotate an underlying primitive or complex representation. Examples include decimal on bytes/fixed and temporal interpretations over integers.

Compatibility of physical primitives does not prove logical compatibility. Decimal scale and precision, timestamp precision, local versus instant semantics, and implementation support must align.

Test each target language with boundary values, negative values, epochs, leap boundaries where relevant, maximum precision, rounding and unsupported annotations.

### Choose the Avro envelope

An object container file includes a header, schema metadata, codec and synchronization marker, followed by blocks. Sync markers enable splitting at block boundaries rather than arbitrary datum bytes.

Single-object encoding prefixes a marker and 64-bit schema fingerprint for one object. Registry ecosystems may use their own magic byte and schema ID envelope.

These are distinct protocols. Record the exact envelope, compression, framing and schema lookup, not merely media type “Avro.”

### Understand Protobuf field keys

A Protobuf binary message is a sequence of tag-value records. The tag is `(field_number << 3) | wire_type`, encoded as a varint.

Field number is durable identity. Wire type groups encodings such as varint, fixed 32-bit, fixed 64-bit and length-delimited. The `.proto` or descriptor supplies the declared name and application type.

Field order on the wire is not semantic. Parsers must accept fields in any order and repeated occurrences according to the format rules.

### Encode integers deliberately

Unsigned and ordinary signed integer fields use varints; small nonnegative values are compact. Negative `int32` or `int64` values are inefficient in ordinary varint form.

`sint32` and `sint64` apply ZigZag before varint so small-magnitude negative and positive values remain compact. Fixed-width types trade constant size and direct layout for space on small values.

Changing among types because they share a wire type can still change signedness, range, generated APIs and meaning. Treat official wire-compatible cases as migration candidates, not automatic approval.

### Parse length-delimited fields safely

Strings, bytes, embedded messages and packed repeated scalars use the length-delimited wire type. The wire type alone does not reveal which one was declared.

Validate the length before allocation and against remaining bytes. Apply limits recursively to embedded messages and independently to collections and strings.

Framing around the message is still required. Concatenating two Protobuf messages without lengths or an external container does not preserve their boundary.

### Never reuse a Protobuf tag

Once deployed, a field number may survive in logs, backups, delayed messages and old binaries. Reusing it for a different field can cause old bytes to populate a new meaning.

Delete by reserving both number and, when useful, name. Reserve removed enum numbers too. The official [Proto Best Practices](https://protobuf.dev/best-practices/dos-donts/) treats tag reuse as categorically unsafe.

Renaming a field while preserving its number is binary-wire compatible, but can break JSON, reflection, generated APIs and operational queries. Compatibility has multiple surfaces.

### Preserve unknown Protobuf fields

An old binary reader can skip fields whose numbers it does not know because their wire types provide parsing boundaries. Current proto3 runtimes preserve unknown fields in normal parse/serialize paths.

Preservation can fail through ProtoJSON, reflection filters, hand-built copies or gateways that reconstruct only known fields. Test the actual path: new writer to old intermediary to new reader.

Unknown preservation protects wire information. It does not make the old application's decision correct without the new concept.

### Model presence explicitly

Presence asks whether a singular field was set, not merely what its getter returns. Under implicit presence, a basic field's default value is generally omitted and cannot be distinguished from unset in the generated API.

Proto3 `optional` and Editions' default explicit presence retain that distinction for singular basic fields. Repeated and map fields do not distinguish absent from empty.

The official [field-presence note](https://protobuf.dev/programming-guides/field_presence/) recommends explicit presence for proto3 basic types. Treat presence changes as semantic changes and test merge, patch and JSON behavior.

### Evolve enums defensively

Give a Protobuf enum a zero-valued `UNSPECIFIED` or `UNKNOWN` member. Callers then have a stable default and a branch for values they do not understand.

Adding a number can be binary-wire safe while breaking exhaustive application switches. Removing or reusing a number is dangerous; reserve deleted values.

Avro enums resolve by named symbol, with reader defaults available under the specification. Test old readers against new symbols and define quarantine, passthrough or fallback semantics.

### Distinguish binary Protobuf from ProtoJSON

ProtoJSON maps message definitions to JSON names and representations. It is not the same wire protocol with prettier bytes.

The official [ProtoJSON guide](https://protobuf.dev/programming-guides/json/) notes that unknown fields are generally not propagated and names enter the representation, changing evolution safety. JSON parsers can reject new fields that old binary readers would skip.

Assess binary, JSON and text-format boundaries independently. Do not cite binary compatibility as evidence for a JSON gateway.

### Do not hash ordinary serialized Protobuf bytes

Known and unknown fields need not be emitted in stable order. Deterministic serialization may stabilize bytes only for a particular binary and does not establish canonical output across versions or languages.

For semantic identity, hash a governed canonical representation or explicit business key. For evidence identity, hash the original received bytes and retain the exact envelope.

Separate semantic equality, message equality and byte equality in tests.

### Define compatibility direction

Let schema versions be $S_1,\ldots,S_n$. Backward compatibility for proposed $S_n$ means its reader can consume data written under required older schemas. Forward compatibility means required older readers can consume data written under $S_n$.

Full compatibility demands both directions. Transitive policy compares against all governed historical versions rather than only $S_{n-1}$.

State whether the check applies to schema structure, all legal values, currently populated values, application code, JSON forms, generated APIs or domain behavior.

### Govern the schema registry

A registry provides versioned storage, references, IDs and compatibility enforcement. Define subject lineage from data ownership, not an accidental topic or class name.

Confluent's [schema-evolution documentation](https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html) distinguishes backward, forward, full and transitive modes. Confirm the deployed product/version and configuration rather than assuming defaults.

Protect write access, authenticate reads, back up schema content and references, retain historical schemas as long as payloads, and cache safely for outages. An ID without registry scope is not globally meaningful.

### Bind payloads to schemas

The envelope may carry a full schema, canonical fingerprint, registry ID, content type plus version, or another authenticated reference. Document byte order, identifier width, collision handling and lookup namespace.

Avro fingerprints identify parsing canonical form, which intentionally strips non-parsing attributes. They do not retain documentation, custom semantics or every governance annotation.

Reject unknown or unauthorized IDs predictably. Do not silently fall back to latest schema.

### Test a mixed-version matrix

For every required writer $W_i$ and reader $R_j$, encode with the real writer toolchain and decode with the real reader toolchain. Populate new fields, old fields, defaults, nulls, every union branch, enums, numeric boundaries and unknown fields.

Exercise old intermediaries, JSON gateways, storage round trips, registry outages, rollback versions and language-specific logical types. Compare domain values and presence, not just decode success.

Archive fixtures with schema content, compiler/runtime versions and expected interpretations.

### Control compiler and runtime skew

Generated code and runtime libraries form a coupled implementation. A schema compatible on paper can fail when code generation, runtime and plugin versions fall outside supported combinations.

Protocol Buffers publishes a [cross-version runtime guarantee](https://protobuf.dev/support/cross-version-runtime-guarantee/) with language-specific limits. Pin and verify each language's actual window.

Record Avro library behavior too, especially logical types, aliases, defaults, union selection and canonical fingerprinting.

### Migrate incompatible changes explicitly

Some changes should create a new field, record type, subject, topic, endpoint or dataset. Examples include changing units, changing identity, splitting one record grain, narrowing populated ranges or repurposing a field.

Use dual read/write only with one authoritative source and reconciliation. Backfill immutably, validate counts and domain invariants, shadow consumers, cut over deliberately, retain rollback evidence, then retire old paths.

Compatibility tricks are not a substitute for an honest migration when meaning changes.

### Observe the boundary

Measure payload and decoded sizes, schema IDs and versions, resolver decisions, unknown fields, default applications, enum fallbacks, decode/validation latency, failures, recursion/limit rejection, registry cache hits, lookup errors and quarantine.

Avoid logging sensitive payloads. Use stable error classes and protected samples with provenance.

Alert on unseen schema IDs, incompatible producer deployment, unknown-field spikes, default use where new writers should populate values, and old-reader traffic beyond its planned window.

## Definitions and Notation

Let a writer produce domain value $v$ under schema $S_w$ and format profile $F$:

$$
b=encode_{F,S_w}(v).
$$

A reader uses the exact writer schema plus its desired schema $S_r$:

$$
v_r=resolve_F(S_w,S_r,decode_{F,S_w}(b)).
$$

Define $B(S_a,S_b)$ when a reader using $S_b$ can consume every governed datum written under $S_a$ without violating the declared contract. A new schema $S_n$ is backward compatible with history $H$ when $B(S_i,S_n)$ for every required $S_i\in H$. It is forward compatible when $B(S_n,S_i)$ for every required old reader $S_i\in H$. Pairwise checking uses only the chosen predecessor; transitive checking quantifies over $H$.

For Protobuf field number $f$ and wire type $w$, the encoded tag value is

$$
t=(f\ll3)\;|\;w.
$$

Varint encodes an unsigned integer in seven payload bits per byte, using the high bit to signal continuation. ZigZag maps signed $n$ to an unsigned value so small magnitudes remain small: $z(n)=2n$ for $n\ge0$ and $z(n)=-2n-1$ for $n<0$.

Let $P(m,f)$ state that message $m$ explicitly contains field $f$. A getter returning its default $d_f$ does not imply $P(m,f)$. Let $U_R(m)$ be bytes for fields unknown to reader $R$. Forward-preserving round trip requires $U_R(parse_R(m))$ to remain available when reserialized, unless the boundary explicitly authorizes loss.

## Mechanisms, Invariants, or Proof Structure

### Fourteen-step schema-aware boundary mechanism

1. Define domain grain, identity, units, time, presence, nulls and invariants.
2. Choose format, encoding profile, message/file envelope, framing and compression.
3. Assign durable names or field numbers and record retired identities.
4. Store exact schema content, dependencies, compiler/runtime versions and ownership.
5. Bind each payload or immutable group to its writer schema.
6. Resolve writer and reader schemas using the format's documented algorithm.
7. Validate domain constraints after decoding and resolution.
8. Check compatibility in every required direction against the governed history.
9. Execute a populated mixed-version and language-runtime matrix.
10. Exercise unknown-field, presence, default, union, enum and logical-type behavior.
11. Bound bytes, lengths, recursion, collections, decompression and lookup work.
12. Publish atomically with schema/envelope identity and reconciliation evidence.
13. Observe resolution, defaults, unknowns, failures and version adoption.
14. Use explicit migration for changes that cannot preserve meaning in place.

### Schema-binding invariant

Every accepted payload is bound to the exact writer schema content or a durable authenticated reference whose namespace, lookup and collision behavior are known.

### Field-identity invariant

A deployed Protobuf number or Avro name/alias lineage denotes one enduring concept. Retirement prevents future reuse for a different concept.

### Resolution invariant

The interpreted value follows the declared writer-to-reader resolution. No decoder guesses a schema from latest version, extension or successful parse.

### Presence invariant

Unset, explicit default, null, empty, unknown and absent-by-old-schema remain distinguishable whenever downstream behavior depends on them.

### Unknown-preservation invariant

Any path expected to forward data it does not understand preserves well-formed unknown fields or explicitly rejects the path as lossy.

### Domain invariant

Resolution cannot change business identity, unit, scale, time meaning, legal state or authorization merely because primitive encodings match.

### History invariant

Compatibility is checked over every schema and reader still required by retained data, deployment, rollback, replay and recovery windows.

### Resource invariant

Before allocation or recursion, payload framing, declared lengths, collection counts, depth, decompressed volume and schema retrieval obey enforced limits.

### Proof sketch: pairwise compatibility is not necessarily transitive

Let $S_1$ contain field `x`; let $S_2$ remove it in a direction where unknown/extra writer fields can be ignored; let $S_3$ add a new required reader field also named `x` but with a different meaning/default policy chosen only relative to $S_2$. A checker comparing adjacent versions may accept $S_1\rightarrow S_2$ and $S_2\rightarrow S_3$ under its configured direction, while direct $S_1\rightarrow S_3$ binds the historical `x` to the new concept or otherwise violates the domain contract. Therefore adjacent acceptance does not prove compatibility across history. Transitive format checks reduce structural gaps, and domain tests must still reject semantic reuse.

### Executable wire audit

The synthetic model recomputes Protobuf tag and varint encoding, preserves an unknown raw field during an old-reader round trip, and recomputes Avro long ZigZag encoding. It validates these finite byte rules only; it does not implement either full specification.

<!-- bijux-verify: {"id":"schema-wire-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"protobuf_hex=089601120378797a\nprotobuf_field=1 wire=0 value=150\nunknown_preserved=True\navro_minus_one_hex=01\navro_64_hex=8001\nround_trip=True\n","stderr":""}} -->
```python
def encode_varint(value):
    if value < 0:
        raise ValueError("varint input must be unsigned")
    output = []
    while value >= 128:
        output.append((value & 127) | 128)
        value >>= 7
    output.append(value)
    return bytes(output)


def decode_varint(data, offset=0):
    value, shift = 0, 0
    while offset < len(data):
        byte = data[offset]
        value |= (byte & 127) << shift
        offset += 1
        if byte < 128:
            return value, offset
        shift += 7
        if shift > 63:
            raise ValueError("varint is too long")
    raise ValueError("truncated varint")


def avro_encode_long(value):
    zigzag = value << 1 if value >= 0 else ((-value) << 1) - 1
    return encode_varint(zigzag)


def avro_decode_long(data):
    zigzag, offset = decode_varint(data)
    if offset != len(data):
        raise ValueError("trailing Avro bytes")
    return zigzag // 2 if zigzag % 2 == 0 else -(zigzag // 2) - 1


known = encode_varint((1 << 3) | 0) + encode_varint(150)
unknown = encode_varint((2 << 3) | 2) + encode_varint(3) + b"xyz"
message = known + unknown
tag, cursor = decode_varint(message)
value, cursor = decode_varint(message, cursor)
old_reader_reserialized = message[:cursor] + message[cursor:]

print(f"protobuf_hex={message.hex()}")
print(f"protobuf_field={tag >> 3} wire={tag & 7} value={value}")
print(f"unknown_preserved={old_reader_reserialized == message}")
print(f"avro_minus_one_hex={avro_encode_long(-1).hex()}")
print(f"avro_64_hex={avro_encode_long(64).hex()}")
print(f"round_trip={all(avro_decode_long(avro_encode_long(n)) == n for n in (-64, -1, 0, 1, 64))}")
```

### Verification strategy

Compile schemas with every production generator; encode and decode a full old/new matrix; inspect payload tags, schema IDs and container headers; populate numeric extremes, explicit defaults, missing values, null branches, every union/oneof branch, every enum condition and logical-type boundary; pass new messages through old intermediaries; round-trip via binary and every JSON gateway; reorder fields and inject unknowns; truncate every varint and length-delimited position; declare excessive lengths; fuzz recursion and collections under limits; disable the registry and invalidate caches; remove schema authorization; test rollback and replay; compare pairwise with transitive compatibility; reconcile published counts; and validate domain meaning independently of parser success.

## Alternatives and Trade-Offs

- **Avro versus Protobuf:** Avro's writer/reader schema resolution and container files suit generic data processing; Protobuf's numbered fields and generated APIs suit service messages. Workload and ecosystem decide.
- **Generated versus generic readers:** generated code gives typed APIs and compiler feedback; generic readers support dynamic schemas but shift more validation to runtime.
- **Embedded schema versus registry ID:** embedding improves autonomous recovery but increases size; an ID is compact but adds lookup, retention and namespace dependencies.
- **Full fingerprint versus short ID:** content fingerprints are portable but collide probabilistically and may omit semantic annotations; registry IDs are centrally governed but registry-scoped.
- **Object container file versus per-message envelope:** a container amortizes schema and supports blocks; per-message identity handles heterogeneous streams at extra overhead.
- **Backward versus forward policy:** backward favors deploying readers before writers; forward favors writers before readers. Real rollback windows often require both.
- **Pairwise versus transitive checking:** pairwise permits more incremental histories; transitive better protects long-lived data and old readers at higher evolution cost.
- **Default versus explicit backfill:** a reader default is cheap but records no producer observation; backfill makes provenance explicit but costs computation and migration control.
- **Alias versus new field:** an alias can preserve a pure Avro rename; a new field is clearer when semantics or migration timing differ.
- **Union versus named variant record:** primitive unions are compact; named variants provide stable meaning and better evolution ownership.
- **Implicit versus explicit presence:** implicit presence simplifies some APIs; explicit presence preserves unset versus default and supports patch semantics.
- **Unknown preservation versus normalization:** preservation supports forward round trips; normalization can simplify output but must declare information loss.
- **Varint versus fixed width:** varints favor small magnitudes; fixed widths favor predictable size and some numeric distributions.
- **Binary Protobuf versus ProtoJSON:** binary is compact and has stronger unknown-field evolution; JSON is inspectable and web-friendly but changes name and unknown-field behavior.
- **Deterministic serializer versus semantic canonicalization:** deterministic mode may stabilize one binary; cross-system hashes need a separately governed canonical contract.
- **One subject per topic versus record type:** topic lineage is operationally simple; record-type lineage can isolate evolution but complicates heterogeneous stream lookup.
- **Strict rejection versus tolerant reader:** tolerance supports rollout and archival reads; excessive coercion hides corruption and semantic changes.
- **Online transformation versus new dataset/topic:** transformation can keep one address; a new boundary makes incompatible semantics and rollback clearer.
- **Central registry versus bundled descriptor set:** a registry centralizes policy and discovery; bundled descriptors improve offline recovery but require distribution and revocation strategy.
- **Compression versus direct observability:** compression saves storage/network; it adds resource-expansion risk and makes partial inspection harder.

## Failure Modes and Misconceptions

1. “The schema is in Avro” ignores raw datum versus object container, single-object and registry envelopes.
2. “Protobuf is self-describing” confuses tags/wire types with message names and declared field types.
3. “Latest schema can decode old data” discards the exact writer-schema requirement.
4. “A schema ID is global” ignores registry namespace and cluster scope.
5. “A fingerprint cannot collide” turns probabilistic identity into certainty.
6. “Canonical form contains the full contract” ignores stripped docs, aliases and custom semantic attributes.
7. “A default is what the producer sent” confuses reader resolution with observation.
8. “Optional means nullable everywhere” collapses format-specific presence and union rules.
9. “Missing equals zero” loses explicit presence and patch intent.
10. “Null equals unknown” collapses a known marker and an unrecognized field.
11. “Renaming is harmless” ignores Avro aliases, ProtoJSON names, generated APIs and queries.
12. “Same Protobuf wire type means safe type change” ignores range, signedness, API and domain meaning.
13. “Deleted tags are available” overlooks retained payloads and old binaries.
14. “An unknown field is always preserved” ignores JSON and reconstructing gateways.
15. “Old readers safely ignore every new concept” confuses parseability with correct decisions.
16. “Adding an enum member cannot break” ignores exhaustive switches and fallback policy.
17. “Reordering an Avro union is cosmetic” ignores its encoded branch index.
18. “Avro record field order is cosmetic” ignores binary traversal and parsing canonical form.
19. “Decimal bytes imply decimal agreement” ignores scale, precision and adapter support.
20. “Milliseconds and microseconds are compatible longs” ignores time semantics.
21. “Deterministic Protobuf is canonical” exceeds the documented implementation-level guarantee.
22. “Two messages with different bytes differ semantically” ignores permissible ordering and representation differences.
23. “A successful decode validates the domain” promotes syntax to truth.
24. “Backward means both directions” omits forward compatibility.
25. “Latest-only compatibility protects archives” ignores non-transitive history gaps.
26. “Registry green means rollout safe” ignores generated code, populated values and domain logic.
27. “One subject strategy fits every stream” ignores ownership and heterogeneous records.
28. “Registry availability is someone else's problem” makes replay dependent on an untested service.
29. “Binary records frame themselves” ignores stream/container boundaries.
30. “Length-delimited means safe allocation” trusts attacker-controlled lengths.
31. “A 2 GiB format maximum is a reasonable service limit” confuses theoretical capability with operational policy.
32. “Compression is outside serialization” ignores decompression bombs and block recovery.
33. “Generated code and runtime versions are interchangeable” ignores language-specific support windows.
34. “JSON is just a diagnostic view” fails when diagnostic paths are replayed or persisted.
35. “Dual write guarantees migration” ignores atomicity, divergence and reconciliation.
36. “Wire compatibility permits semantic reuse” confuses representability with enduring meaning.

## Worked Examples

### Example 1

An Avro v1 writer records `id` and `amount_minor`. A v2 reader adds `currency` with default `USD`. Resolution succeeds backward, but lineage marks currency as reader-derived for v1 records. Before new writers emit non-USD values, consumers are upgraded and domain validation requires ISO currency plus amount unit agreement.

### Example 2

An Avro field `customer` is renamed `customer_id` without changing meaning. The reader schema carries the historical name as an alias, fixtures cover all retained writer schemas, and registry policy remains transitive. If meaning had changed from account number to party UUID, a new field and migration would be required instead.

### Example 3

A team proposes changing union `["null","string"]` to `["string","null"]` for style. Review rejects it because Avro encodes the selected branch index. The existing order remains, and future variants use named record branches with fixtures that populate each branch.

### Example 4

A Protobuf v2 message adds `optional string region = 5`. A v1 proxy parses and reserializes binary messages, and the integration test confirms field 5 survives. A second proxy converts through ProtoJSON and loses the unknown; it is classified as a lossy boundary and upgraded before writers populate `region`.

### Example 5

Field 7, formerly `temperature_celsius`, is removed. The schema reserves number 7 and its name. A new Fahrenheit reading receives a new number and an explicit unit-bearing name. Historical bytes cannot populate the new field accidentally.

### Example 6

A signed counter frequently contains `-1`, `0` and `1`. Measurement shows `sint64` gives compact ZigZag varints, but the deployed `int64` field is not changed in place. A new field is introduced, dual-populated within range, compared, then adopted after old consumers retire.

### Example 7

A registry subject was accidentally keyed by topic even though three unrelated record types share it. Compatibility rules cross-contaminate lineages. Engineers create ownership-based subjects, publish an explicit message-type index in the envelope, migrate consumers, and retain the old ID mapping for replay.

### Example 8

An Avro decimal uses bytes with precision 18 and scale 4. Java, Python and warehouse adapters are tested with maximum magnitude, negative values, trailing zeros and rounding rejection. A proposed scale change creates a new field because primitive byte compatibility would conceal changed units.

### Example 9

A disaster-recovery test blocks registry access. Consumers decode cached known schemas, quarantine unseen IDs without guessing, and recover after authenticated lookup returns. Schema backups restore exact content, references and ID mapping before retained payloads expire.

### Example 10

An order schema changes from one record per order to one record per line item. No compatibility mode can preserve grain. The team creates a new record type and topic, backfills from immutable orders, reconciles counts and totals, shadows consumers, cuts over, and records the old-to-new lineage.

## Cross-Program Connections

**API & Service Engineering:** Protobuf messages often define RPC surfaces. Wire-safe changes can still break generated client APIs, validation, authorization and behavioral contracts.

**Database Engineering:** Adding columns, changing types and backfilling mirror schema-evolution concerns, but database transactions and storage catalogs provide different atomicity and history guarantees.

**Distributed Systems:** Asynchronous deployment, rollback, replay and registry availability turn compatibility into a coordination problem across versions.

**Programming Languages:** Generated APIs map presence, enums, unions, unsigned integers and logical types differently. Language semantics are part of boundary verification.

**Security Engineering:** Schema lookup needs authentication and authorization; parsers need allocation and recursion limits; unknown fields and logs can carry sensitive data.

**Formal Methods:** Compatibility is a directional relation over schemas and governed values. Counterexamples, quantification over history and invariant preservation sharpen review.

**Site Reliability Engineering:** Registry outages, cache behavior, decode error budgets, version adoption and rollback windows require observable operational design.

**Software Engineering Patterns:** Anti-corruption layers separate wire DTOs from domain models, preventing generated representation choices from becoming business meaning.

## References

1. Apache Avro, [Specification 1.12.0](https://avro.apache.org/docs/1.12.0/specification/), 2024.
2. Apache Avro, [Apache Avro 1.12.0 Documentation](https://avro.apache.org/docs/1.12.0/), 2024.
3. Protocol Buffers, [Encoding](https://protobuf.dev/programming-guides/encoding/), current documentation.
4. Protocol Buffers, [Language Guide (proto 3)](https://protobuf.dev/programming-guides/proto3/), current documentation.
5. Protocol Buffers, [Language Guide (editions)](https://protobuf.dev/programming-guides/editions/), current documentation.
6. Protocol Buffers, [Application Note: Field Presence](https://protobuf.dev/programming-guides/field_presence/), current documentation.
7. Protocol Buffers, [Proto Best Practices](https://protobuf.dev/best-practices/dos-donts/), current documentation.
8. Protocol Buffers, [ProtoJSON Format](https://protobuf.dev/programming-guides/json/), current documentation.
9. Protocol Buffers, [Cross-Version Runtime Guarantee](https://protobuf.dev/support/cross-version-runtime-guarantee/), current documentation.
10. Protocol Buffers, [Protobuf Editions Overview](https://protobuf.dev/editions/overview/), current documentation.
11. Confluent, [Schema Evolution and Compatibility](https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html), current documentation.
12. Confluent, [Schema Registry SerDes Overview](https://docs.confluent.io/platform/current/schema-registry/fundamentals/serdes-develop/overview.html), current documentation.
13. Confluent, [Schema Registry Data Contracts](https://docs.confluent.io/platform/current/schema-registry/fundamentals/data-contracts.html), current documentation.
14. Confluent, [Protobuf Serializer and Deserializer](https://docs.confluent.io/platform/current/schema-registry/fundamentals/serdes-develop/serdes-protobuf.html), current documentation.
15. IETF, [RFC 8949: Concise Binary Object Representation](https://www.rfc-editor.org/rfc/rfc8949.html), 2020.

## Exercises

### Exercise 1

An Avro v1 record has `order_id:string` and `amount_minor:long`. Design v2 to add currency, explain backward and forward resolution, and state what a reader default does not prove.

### Exercise 2

A deployed Protobuf field `int32 status_code = 4` is removed. A proposal later assigns `string status_text = 4`. Diagnose the failure and design the durable schema change.

### Exercise 3

Trace the bytes `08 96 01 12 03 78 79 7a` using Protobuf tags, wire types, varints and length prefixes. What can be known without the `.proto` definition?

### Exercise 4

Design a compatibility and test policy for a seven-year event archive, rolling service deployments, binary Protobuf producers, one old binary proxy and one ProtoJSON analytics gateway.

### Exercise 5

An Avro field changes from decimal precision 12, scale 2 in cents-like values to precision 18, scale 6 for fractional units. A latest-only registry check can be made to pass. Design the correct migration and evidence package.

## Answers to the Exercises

### Answer 1

Add a `currency` string field with a valid default such as `"USD"` only if that is an approved interpretation for old records. A v2 reader uses the default when reading data whose v1 writer schema lacks the field, so that establishes backward resolution. An old v1 reader generally ignores the new writer field under Avro record resolution, establishing the structural forward direction when names and record identity match.

Test both directions with exact writer schemas and populated values. The default proves only that the v2 reader supplies `USD`; it does not prove the v1 producer observed USD. Carry provenance or a derived-status flag if downstream reasoning needs that distinction. If old data can contain multiple currencies, a single default is false and the change requires enrichment or migration.

### Answer 2

Field number 4 is the durable binary identity. Old payloads encode its former integer value with wire type 0, while the proposed string uses wire type 2. Depending on parsers and paths, data may be treated as unknown, lost or misinterpreted; more importantly, one identity now means two concepts. Never reuse it.

Reserve number 4 and the retired name. Give `status_text` a new field number. Prefer an enum or named status model with an unspecified state if the domain is closed enough. During migration, new writers can populate the new field while readers understand both, with a declared conflict rule. Retire old population only after consumer and archive windows close.

### Answer 3

`08` is varint tag 8: field number `8 >> 3 = 1`, wire type `0`. The following varint bytes `96 01` decode to 150. `12` is tag 18: field number 2, wire type 2. Its next byte `03` declares three payload bytes, `78 79 7a`, which are ASCII `xyz` but could represent a UTF-8 string, arbitrary bytes, an embedded message or packed scalars depending on the schema.

Without the `.proto`, one knows field numbers, wire classes, record boundaries within this message and raw payload values. One does not know declared names, whether field 1 is an integer, Boolean or enum, what field 2 means, the containing message type, domain units, or the outer message boundary.

### Answer 4

Use an ownership-based schema lineage with full transitive checks over every retained reader/writer requirement, reserving all deleted field and enum numbers. Retain descriptors and ID mappings at least as long as the archive, back them up for recovery, authenticate lookup and reject unknown IDs without guessing.

For each change, run new and rollback writers against new, rollback and archive readers with boundary-populated fixtures. Pass new fields through the old binary proxy and confirm unknown bytes survive. Treat the ProtoJSON gateway separately: deploy schema support before producers emit new fields because JSON generally does not propagate binary unknowns, and test field/enum names plus presence. Record compiler/runtime versions, observe schema IDs, unknown fields and fallback use, and preserve original binary evidence for replay.

### Answer 5

The change alters numeric domain and representation even if a primitive or registry path accepts it. Create a new field with a new semantic name, such as `amount_units_6`, and keep the old field immutable. Specify conversion as exact decimal arithmetic, rounding rejection, unit, scale, valid range and source provenance.

Dual-read and, if authoritative conversion is possible, dual-write within a controlled window. Backfill from immutable source records into a new dataset or schema lineage, never by repeatedly mutating the archive. Test every retained writer-reader pair and each language adapter at extrema, negatives, fractional values and values not exactly representable at scale 2. Reconcile record counts and aggregate values, shadow consumers, cut over with rollback boundaries, then retire the old field without reusing its identity. Use transitive checks, but treat domain and numeric evidence—not registry acceptance—as the migration proof.
