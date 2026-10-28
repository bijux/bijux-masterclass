---
module_id: LSDS-008
program: Large-Scale Data Systems Engineering
level: 1
module_number: 8
title: Serialization Across Workers
status: complete
last_verified: 2026-09-03
---

# Serialization Across Workers

## One-Page Review

### Governing question

How should a distributed data system turn values, code, and state into bounded byte sequences that heterogeneous workers can exchange, validate, evolve, and recover without silently changing meaning?

### Essential definitions

- **Serialization** maps a value or object graph to bytes; **deserialization** reconstructs an interpreted value from bytes.
- A **wire format** defines the byte-level representation of primitive and composite values.
- A **schema** defines field identities, types, cardinality, defaults, logical meanings, and compatibility rules.
- **Framing** delimits messages or batches and carries envelope metadata such as length, version, schema identity, flags, and integrity data.
- **Writer schema** describes bytes emitted; **reader schema** describes the value a consumer expects.
- **Backward compatibility** lets a new reader consume old data; **forward compatibility** lets an old reader consume new data under stated rules.
- **Deterministic encoding** produces a prescribed byte representation under a defined scope; semantic equality alone does not imply byte equality.
- A **deserialization trust boundary** is any point where bytes can be supplied or modified by a less-trusted principal or failure domain.

### Central model, mechanism, or theorem

Treat a transferable unit as `F=(magic, envelope_version, codec, schema_id, flags, payload_length, payload, integrity)`. Acceptance requires a supported envelope and codec, a compatible writer/reader schema pair, bounded lengths and nesting, complete bytes, validated integrity as required, successful decoding, and application-level invariants.

The round-trip obligation is semantic: for supported values `x`, `decode_reader(encode_writer(x))` must equal the documented projection or evolution of `x`. Byte determinism is a separate obligation needed for content addressing, signatures, stable hashing, or binary identity. A checksum detects accidental corruption; it does not authenticate an attacker.

### Critical invariants

- Every byte stream has an unambiguous framing and schema-identification rule.
- Lengths, counts, nesting, allocations, and decompression expansion are bounded before use.
- Field identity is stable across producer and consumer versions.
- Required semantic changes use explicit migrations, not hopeful decoder coercion.
- Unknown, missing, null, and default values have deliberate distinct behavior.
- Keys and partition fields retain stable cross-language meaning and encoding.
- Untrusted bytes never enter an unsafe object-instantiation decoder.
- Checksums, authentication, encryption, and transport reliability are not interchangeable.
- Benchmarks include encode/decode CPU, bytes, allocations, batching, compression, and tails.

### Common failures

Frequent failures are shipping language-native objects as a durable protocol, omitting record framing, reusing field numbers, confusing absent with null or zero, hashing nondeterministic bytes, changing time/decimal units, permitting unbounded lengths or recursion, deserializing attacker-controlled object graphs, accepting partial frames, treating checksums as signatures, enabling compression without expansion limits, and benchmarking only average payload size.

### Compact example

A worker frame uses a fixed header with magic, envelope version, flags, payload length, and a truncated digest, followed by tag-length-value bytes. An old reader ignores the new `currency` field; a new reader supplies documented `USD` for an old message. Reordered map insertion yields identical bytes under the fixture's field ordering. One flipped byte fails the checksum comparison, and an advertised length above the configured maximum is rejected before allocation.

### Connections

[LSDS-007](007-narrow-and-wide-transformations.md) determines which bytes move. [LSDS-009](../ROADMAP.md) develops the failures that can interrupt or corrupt transfer. Later shuffle, state, checkpoint, query, and performance modules revisit serializer choice for distinct lifetimes and workloads.

## Governing Question

Inside one process, a value can be pointers, headers, language-specific collections, and runtime metadata. Another process cannot interpret those addresses. Across a worker boundary, the system needs bytes plus enough contract to reconstruct meaning. Across languages, runtime versions, rolling upgrades, retries, checkpoints, and retained shuffle files, implicit assumptions become protocol decisions.

“Serialize the object” hides several questions. Which fields exist and what do they mean? How are signed integers, strings, maps, timestamps, decimals, nulls, and unknown fields represented? Where does one message end? How is its schema found? Can old and new workers overlap? Is byte identity stable? What happens to a truncated, corrupted, oversized, malicious, or compressed payload?

The governing question is therefore how to define a byte contract appropriate to the lifetime and trust of the data. Ephemeral records exchanged within one application attempt can use a tighter engine-native format than durable state restored after an upgrade. External events require interoperable, governed schemas. Code and closures have different safety and versioning risks from plain data. One serializer should not be assumed suitable for every boundary.

## Why This Matters

Serialization lies on every remote data path: task launch, shuffle, broadcast, RPC, stream input, state snapshot, checkpoint, cache spill, and sink output. A wide transformation can encode billions of records. A few extra bytes per record become storage and network cost; a few extra allocations become garbage-collection pressure; a slow decoder can gate every downstream task.

Correctness depends on meaning surviving. A timestamp interpreted as seconds instead of milliseconds moves an event by orders of magnitude. A decimal converted through binary floating point changes money. A missing field treated as false can reverse a policy decision. A changed hash encoding can send equal keys to different partitions. A decoder that drops unknown fields can destroy information when it later reserializes a message.

Availability depends on bounded work. A forged length can request impossible memory. Deep nesting can exhaust the stack. Highly compressed input can expand far beyond its wire size. Malformed maps can trigger pathological behavior. An object serializer may instantiate classes or execute code during decode. Workers process data at scale, so a small per-message vulnerability can become a cluster-wide resource event.

Evolution depends on explicit compatibility. Rolling deployments create producer/consumer version matrices. Shuffle output and checkpoints can outlive the worker binary that wrote them. If serializer registration IDs or class layouts change, a retry may fail only after a worker is replaced. Durable schema identity and compatibility tests turn that implicit coupling into evidence.

## Prerequisites and Retrieval

Recall from [LSDS-003](003-range-hash-and-consistent-partitioning.md) that partition keys require stable equality and routing semantics. Recall from [LSDS-006](006-stages-tasks-and-dependencies.md) that attempts and accepted outputs are separate identities. Recall from [LSDS-007](007-narrow-and-wide-transformations.md) that exchange blocks belong to a graph and partitioner generation.

You should understand bytes, integers, floating point, Unicode, records, arrays, maps, checksums, hashes, compression, schemas, compatibility, authentication, memory allocation, and percentiles. Retrieve the distinction between corruption detection and adversarial authenticity.

## Learning Objectives

After completing this module, you should be able to:

- separate in-memory values, wire encoding, framing, transport, and application semantics;
- specify an envelope with version, schema identity, length, flags, payload, and integrity;
- choose between engine-native, row-oriented, schema-based, and columnar formats;
- reason about writer/reader schema compatibility in rolling upgrades and recovery;
- distinguish missing, null, default, unknown, and invalid fields;
- preserve key, timestamp, decimal, string, map, and floating-point semantics;
- explain semantic round trips and deterministic byte encoding;
- reject truncated, corrupted, unsupported, oversized, or malicious frames safely;
- distinguish checksum, MAC/signature, encryption, and transport protection;
- evaluate batching, compression, zero-copy, allocation, and garbage-collection trade-offs;
- define metrics, compatibility matrices, golden fixtures, and failure tests; and
- specify consequence-appropriate review for serialized data.

## Core Exposition

### Values, bytes, and protocols

An in-memory value belongs to a runtime data model. It may contain pointers, aliases, cycles, class metadata, lazy fields, platform-sized integers, or unordered containers. Serialization selects an abstract data model and maps it to bytes. Deserialization parses bytes and constructs a reader-side value. Neither direction is inherently lossless across different models.

A protocol includes more than a codec. It specifies message types, field semantics, schemas, framing, sequencing, error behavior, limits, compatibility, integrity, and sometimes authentication or encryption. JSON, Avro, Protocol Buffers, Arrow IPC, and a language object stream each solve different portions of that contract.

Separate the layers. The application defines meaning. A schema defines the logical record. The wire format encodes it. Framing delimits it. Compression transforms payload bytes. Integrity detects changes. Authentication establishes origin/integrity under a key or signature. Encryption protects confidentiality. The transport moves bytes and supplies its own delivery semantics.

Two processes can share a codec and still disagree on meaning. Both may decode integer `1000`, while one reads milliseconds and the other seconds. Both may decode a string, while one normalizes Unicode before key comparison. Type success is not semantic compatibility.

### Boundary and lifetime classes

Classify each serialization boundary by audience, lifetime, replay horizon, trust, and upgrade independence. An intra-task buffer may live milliseconds inside one binary. A shuffle block may survive executor replacement within one application. A checkpoint may be restored months later under new code. A stream event may be consumed by many teams and languages. A published file may be governed for years.

Engine-native serializers optimize for application-local values and speed. Spark's serializer API explicitly does not require wire compatibility across Spark versions and scopes its use to a single application. Such a serializer can be suitable for shuffle records while being unsuitable as a durable external format.

Durable state needs stored serializer/schema metadata and migration support. Flink snapshots serializer configuration and checks compatibility when restoring state; supported evolution depends on the serializer and state shape. External data needs a stable format specification, schema governance, and independent producer/consumer conformance.

Code and closures deserve a separate boundary. A task closure may capture far more state than intended, include unavailable classes, or reference nonserializable resources. Shipping executable object graphs also increases trust risk. Prefer explicit code artifacts and small declarative task parameters where the engine supports them.

### Envelope and framing

A decoder must know where bytes begin and end. Fixed-size records, length prefixes, sentinel delimiters, chunked framing, and self-delimiting formats are alternatives. Delimiters require escaping or grammar-aware parsing. Length prefixes permit efficient allocation but are dangerous if trusted before limits. Chunking supports streaming large values but needs total-size and sequence rules.

A robust frame commonly includes magic bytes, envelope version, codec/schema identity, flags, payload length, payload, and checksum or authenticated integrity data. It may add message type, compression algorithm, uncompressed length, partition/exchange identity, attempt, sequence number, or trace context. Specify byte order and exact integer widths.

Validate the header before allocating from it. Require supported magic, version, flags, and codec; enforce maximum compressed and uncompressed lengths; detect arithmetic overflow; require the exact declared payload; then verify integrity before expensive or effectful application handling. Streaming decoders also enforce chunk count, total size, and completion.

Framing and schema identity can be per record, batch, partition, connection, or file. Per-record metadata is flexible but expensive. Batch-level schemas amortize overhead but make mixed-schema records harder. Connection-negotiated schemas reduce bytes yet complicate reconnect and retained artifacts. Persisted blocks should remain independently interpretable under their recovery contract.

### Primitive semantic choices

Integer encoding must specify signedness, width, overflow, and representation. Variable-length integers save space for small magnitudes but have data-dependent size and parsing. Fixed widths simplify random access and vectorization. Never silently wrap a larger writer value into a smaller reader type.

Floating point needs IEEE representation assumptions, byte order, NaN, infinity, signed zero, and comparison rules. Multiple NaN bit patterns and map ordering can defeat byte determinism. Financial or measured quantities may need scaled integers or decimal logical types with explicit precision, scale, and rounding.

Time requires instant versus civil time, unit, epoch, time zone, calendar, precision, leap-second policy, and ambiguity behavior. Store instants in an agreed epoch/unit and retain zone identifiers when civil interpretation matters. A bare integer named `timestamp` is not a sufficient contract.

Strings require an encoding such as UTF-8, normalization policy, invalid-byte behavior, and length unit. Byte length differs from Unicode code-point or user-perceived character count. If strings form keys, all languages must implement identical canonicalization and equality.

Maps and sets need duplicate-key, key-type, ordering, and canonicalization rules. Many formats permit semantically unordered maps, while an implementation emits insertion order. Hashing raw bytes of such output is unsafe unless the protocol defines deterministic encoding. Arrays preserve order and therefore carry different meaning.

### Schema identity and resolution

Compact binary formats often omit field names or types from each record, so readers require the writer schema. Carry the schema directly, include a stable fingerprint/ID resolved from a registry, bind it at the batch/connection level, or use stable numeric field tags. Each method has availability and collision risks.

A schema ID must identify immutable content, not a mutable “latest” name. Registry access should not become an unbounded task-start dependency; cache verified schemas and define outage behavior. A content digest needs canonical schema bytes and collision-resistant comparison appropriate to the system.

Reader/writer resolution maps writer fields and types into reader expectations. The compatibility policy must state which additions, removals, promotions, aliases, defaults, and unknown fields are accepted. Avro makes writer and reader schemas explicit. Protocol Buffers uses stable field numbers and permits unknown-field skipping; removed numbers and names should be reserved rather than reused.

Schema compatibility is not semantic compatibility. Renaming `gross_cents` to `net_cents` while keeping the field identity decodes successfully but changes meaning. Changing a unit or identity rule usually requires a new field plus migration, dual-read/write period, or explicit versioned message type.

### Missing, null, default, and unknown

Missing means the writer did not encode a field. Null is an encoded absence when the schema permits it. A default is a reader-side value or schema behavior, not proof the writer observed that value. Zero, empty string, empty collection, and false are ordinary values unless the domain says otherwise.

Conflating these states breaks evolution. An old message missing `consent` must not automatically mean the person declined, consented, or was ineligible. The schema can represent `unknown`, `not_applicable`, and evidence-bearing decisions explicitly.

Unknown fields let old readers tolerate newer writers, but preservation policy matters. A decode-modify-reencode proxy that discards unknown fields can erase new data. Some libraries preserve unknown wire fields; conversions through JSON or generic objects may not. Test the full path, not only direct decoding.

Required-field additions usually break old data unless the reader has a valid default or migration. Field removal can break readers and reusing its tag can reinterpret retained bytes. Type promotion may preserve range but change equality, precision, or application logic. Compatibility rules are directional and workload-specific.

### Semantic round trips and determinism

For a single schema and supported domain `D`, a basic obligation is `decode(encode(x)) = x` for every `x in D`, where equality is the documented semantic equality. Under evolution, use `decode_R(encode_W(x)) = project_(W->R)(x)`. The projection accounts for defaults, ignored unknowns, aliases, and deliberate conversions.

This is not generally a byte round trip. A decoder may reorder map entries, normalize values, select a different valid integer width, or preserve logical content while re-encoding differently. Protocol Buffers documentation warns that default serialization order is not guaranteed and that deterministic mode has a limited binary/version scope.

Byte determinism is required when bytes themselves feed a digest, signature, cache key, deduplication ID, Merkle tree, or partitioner. Define one canonical representation including field/map order, integer widths, floating values, Unicode, unknown fields, and schema version. Alternatively hash a stable semantic projection rather than incidental serializer output.

Determinism does not imply correctness or security. A deterministic encoder can deterministically encode the wrong unit. A collision-resistant digest over canonical bytes detects identity changes but does not establish authorization. A signature requires key and verification policy.

### Compatibility across rolling workers

A rolling upgrade can run old writers with new readers, new writers with old readers, and new readers over retained old shuffle/checkpoint bytes. Build the matrix explicitly. Backward-only compatibility does not cover a new writer feeding an old worker during overlap.

Test adjacent versions and every still-supported retained version. Use golden bytes produced by real language implementations; decode them with other languages/versions and re-evaluate semantics. Include unknown fields, missing fields, extremes, invalid encodings, Unicode, time, decimal, and large collections.

Registration-based serializers need stable class-to-ID mappings. Independent registration order can assign different IDs. Class names, constructors, field layout, runtime libraries, and custom serializer versions may also drift. Freeze and validate registration manifests or avoid implicit IDs for recoverable boundaries.

For state migration, preserve the old decoder long enough to read old bytes and produce new bytes. Migration should be resumable, idempotent, measured, and reversible through retained source/checkpoint copies where required. Do not learn incompatibility only during disaster recovery.

### Integrity, authenticity, and confidentiality

A checksum such as CRC efficiently detects many accidental bit errors and truncation patterns. It is not designed to resist an attacker who can modify both payload and checksum. A cryptographic digest detects changes when the expected digest is obtained through a trusted path, but an unauthenticated digest traveling with the payload can also be replaced.

A message authentication code verifies integrity and origin among holders of a shared secret. A digital signature supports asymmetric verification and nonrepudiation properties only within a sound key, identity, and policy system. Encryption protects confidentiality; authenticated encryption can also protect integrity for the encrypted envelope.

Define what bytes are covered. Headers that select codec, schema, compression, or length can be security-critical. Bind relevant context such as partition, sequence, tenant, and protocol version to prevent substitution or replay. TLS protects a connection in transit but not necessarily queued, cached, spilled, or replayed artifacts after termination.

Key rotation, replay windows, nonce uniqueness, verification failure, and metadata leakage require explicit design. Compression before encryption is typical for effectiveness, but secrets mixed with attacker-controlled text can introduce side channels in interactive contexts. Apply the threat model for the actual data path.

### Defensive deserialization

Treat every cross-process decoder as a parser exposed to corruption and potentially hostile input, even on an internal network. Authenticate peers, authorize message types, and assume credentials or workers can be compromised. Avoid object serializers that can invoke constructors, callbacks, class loading, or arbitrary code for untrusted bytes. Python's `pickle` documentation explicitly warns that malicious pickle data can execute arbitrary code.

Enforce limits before and during decode: frame bytes, uncompressed bytes, field count, string/array/map elements, nesting depth, numeric magnitude, dictionary size, batch rows, cumulative stream size, and processing time. Reject duplicate or forbidden fields according to the protocol. Avoid allocating directly from an unchecked declared length.

Compression adds an expansion ratio and decompressor-state boundary. Validate both compressed and declared uncompressed sizes, stream into bounded storage, and stop after the limit even if the stream claims more. Checksums should cover the intended compressed or uncompressed representation consistently.

Parsing success is only the first gate. Validate schema constraints, cross-field invariants, identifiers, permissions, partition ownership, and domain rules before changing state. Fail closed with bounded diagnostics that do not echo secrets or enormous payloads. Quarantine or sample malformed evidence under retention and privacy policy.

### Row, columnar, and object representations

Row-oriented encoding keeps fields for one record together, suiting record-at-a-time logic, sparse messages, and small RPCs. Field tags support evolution at per-record overhead. Schema-driven row formats can omit names and compact repeated structure.

Columnar batches group values by field, enabling vectorized computation, compression, selective field access, and reduced per-value overhead. Apache Arrow IPC transmits schemas, record batches, and dictionary batches around a defined physical memory layout. It is effective for analytical batches but requires buffer alignment, offset, validity bitmap, dictionary, and lifetime correctness.

Zero-copy is conditional. A receiver may view aligned buffers without per-value reconstruction only when representation, ownership, endianness, lifetime, and device/memory placement are compatible. Validation, decompression, decryption, byte swapping, or language conversion can require copies. Retaining a small slice can pin a large backing buffer.

Language object serialization is convenient for homogenous short-lived clusters and arbitrary graphs. It couples the wire to classes/runtime, may carry reference cycles and hidden state, and can be unsafe for untrusted data. Prefer explicit schemas at long-lived or independently deployed boundaries.

### Batching, compression, and performance

Per-record framing and system calls waste bytes and CPU for tiny records. Batching amortizes headers, checksums, encryption, compression dictionaries, network calls, and scheduler overhead. Larger batches improve throughput until they harm latency, memory, fairness, failure replay, or backpressure.

Compression trades encode/decode CPU and latency for fewer network/storage bytes. Effectiveness depends on codec, level, batch size, field ordering, cardinality, and data entropy. Columnar layout often improves locality of similar values. Already compressed or encrypted inputs may expand.

Serializer performance includes encoded bytes, encode/decode throughput, allocations, copies, peak memory, garbage collection, buffer growth, branch behavior, and p50/p95/p99 latency across realistic size distributions. Benchmark cold and warm paths, schema lookup, unknown fields, compression, and concurrent workers.

Registration and reusable buffers reduce metadata and allocation, but shared serializer instances may not be thread-safe. Bound buffer growth so one giant record does not permanently inflate every worker. Track maximum-object failures separately from ordinary throughput.

### Observability and retained evidence

Tag metrics by protocol/envelope version, codec, schema ID, producer and consumer version, record type, edge, and outcome without placing sensitive values in labels. Record encoded and decoded bytes, compression ratio, batch rows, encode/decode time, allocations where measurable, limit rejections, corruption, incompatibility, unknown fields, and retry bytes.

Retain schema content/digests, compatibility decisions, registration manifests, golden fixtures, benchmark configuration/results, upgrade matrices, and decoder-limit policy. For a failed frame retain bounded safe metadata: source identity, block/message ID, sizes, versions, checksum outcome, error class, and a protected sample only when policy permits.

Compare distributions. A good average compression ratio can hide a payload class that expands. A low average decode time can hide deep or giant messages. A small average task closure can hide one captured lookup table. Tie serializer metrics to stage tails, network utilization, spill, and worker memory.

## Definitions and Notation

Let logical value domain be `D_W` under writer schema `W` and reader domain be `D_R` under schema `R`. Let encoder `e_W: D_W -> B*` emit finite byte strings and decoder `d_R: B* -> D_R union Error` accept or reject bytes.

For supported writer values, compatibility requires `d_R(e_W(x)) = pi_(W->R)(x)`, where `pi` is the documented semantic projection/migration. When `W=R` and no lossy behavior exists, `pi` is identity. This statement excludes resource-limit violations and invalid application values explicitly outside the supported domain.

Let frame `F=H || P || I`, with header `H`, payload `P`, and integrity value `I`. Header fields include at least `(magic, envelope_version, codec, schema_id, flags, payload_length)` or are bound by equivalent connection/batch context. Acceptance predicate `A(F,R,policy)` is true only if framing, versions, schema resolution, limits, completeness, integrity, decoding, and application validation pass.

Let `L_wire=|F|`, `L_payload=|P|`, and `L_value` be an application-defined uncompressed/logical size. Compression ratio must state direction; use `rho=L_value/L_payload` here. Enforce `L_wire<=M_wire`, `L_value<=M_value`, and `rho<=M_ratio` when compression is enabled.

Let batch size be `n`. Fixed overhead per record approximately changes from `n*h` under individual frames to `h+b(n)` under a shared batch, while failure/retry and latency exposure grow with `n`. Empirical measurement, not this approximation, selects the operating point.

Deterministic encoding under configuration/version `v` requires `x ==_semantic y` to imply `canon_v(x)=canon_v(y)`. Cross-version stability requires the stronger `canon_v(x)=canon_w(x)` for supported `v,w`; many “deterministic” serializer modes do not promise it.

## Mechanisms, Invariants, or Proof Structure

To design and review a worker serialization boundary:

1. Name the data, code, or state boundary and its lifetime.
2. Define logical fields, units, equality, nullability, defaults, and invariants.
3. Select a schema identity and writer/reader resolution policy.
4. Define exact framing, byte order, versions, flags, lengths, and completion.
5. Bound wire size, expanded size, collections, depth, allocation, and time.
6. Select integrity, authentication, confidentiality, and replay controls from the threat model.
7. Specify deterministic representation only where byte identity is required.
8. Build old/new and cross-language golden compatibility matrices.
9. Benchmark realistic distributions, batches, compression, concurrency, and tails.
10. Retain evidence and conduct domain-specific review.

The following executable fixture demonstrates a small bounded envelope, canonical encoding, additive-field compatibility, corruption detection, and preallocation length rejection. It is instructional, not a recommended general-purpose production protocol; its CRC is not authentication.

<!-- bijux-verify: {"id":"bounded-worker-frame","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"frame_bytes=41 payload_bytes=25\nold_reader_new_writer={'id': 'evt-7', 'amount_cents': 1250}\nnew_reader_old_writer={'id': 'evt-7', 'amount_cents': 1250, 'currency': 'USD'}\ncanonical_equal=True\ntampered=checksum_mismatch\noversized=length_limit\n","stderr":""}} -->
```python
import hashlib

MAGIC = b"BXS1"
VERSION = 1
MAX_PAYLOAD = 1024
HEADER_BYTES = 16
FIELD_TAGS = {"id": 1, "amount_cents": 2, "currency": 3}


def encode(record):
    payload = bytearray()
    for name in ("id", "amount_cents", "currency"):
        if name not in record:
            continue
        value = record[name]
        if name == "amount_cents":
            raw = value.to_bytes(8, "big", signed=True)
        else:
            raw = value.encode("utf-8")
        payload += (
            bytes([FIELD_TAGS[name]])
            + len(raw).to_bytes(2, "big")
            + raw
        )
    if len(payload) > MAX_PAYLOAD:
        raise ValueError("length_limit")
    digest = hashlib.sha256(payload).digest()[:8]
    return (
        MAGIC
        + bytes([VERSION, 0])
        + len(payload).to_bytes(2, "big")
        + digest
        + payload
    )


def decode(frame):
    if len(frame) < HEADER_BYTES:
        raise ValueError("truncated_header")
    if frame[:4] != MAGIC or frame[4] != VERSION or frame[5] != 0:
        raise ValueError("unsupported_envelope")
    length = int.from_bytes(frame[6:8], "big")
    if length > MAX_PAYLOAD:
        raise ValueError("length_limit")
    payload = frame[HEADER_BYTES:]
    if len(payload) != length:
        raise ValueError("length_mismatch")
    if hashlib.sha256(payload).digest()[:8] != frame[8:16]:
        raise ValueError("checksum_mismatch")
    result = {}
    offset = 0
    names = {value: key for key, value in FIELD_TAGS.items()}
    while offset < len(payload):
        if offset + 3 > len(payload):
            raise ValueError("truncated_field")
        tag = payload[offset]
        size = int.from_bytes(payload[offset + 1 : offset + 3], "big")
        offset += 3
        if offset + size > len(payload):
            raise ValueError("truncated_field")
        raw = payload[offset : offset + size]
        offset += size
        if tag in names:
            name = names[tag]
            if name == "amount_cents":
                result[name] = int.from_bytes(raw, "big", signed=True)
            else:
                result[name] = raw.decode("utf-8")
    return result


def read_v1(obj):
    return {"id": obj["id"], "amount_cents": obj["amount_cents"]}


def read_v2(obj):
    return {
        "id": obj["id"],
        "amount_cents": obj["amount_cents"],
        "currency": obj.get("currency", "USD"),
    }


old = {"id": "evt-7", "amount_cents": 1250}
new = {"currency": "EUR", "amount_cents": 1250, "id": "evt-7"}
frame = encode(new)
print(f"frame_bytes={len(frame)} payload_bytes={len(frame) - HEADER_BYTES}")
print(f"old_reader_new_writer={read_v1(decode(frame))}")
print(f"new_reader_old_writer={read_v2(decode(encode(old)))}")
print(f"canonical_equal={encode(new) == encode(dict(reversed(tuple(new.items()))))}")

tampered = bytearray(frame)
tampered[-1] ^= 1
try:
    decode(tampered)
except ValueError as error:
    print(f"tampered={error}")

oversized = (
    MAGIC
    + bytes([VERSION, 0])
    + (MAX_PAYLOAD + 1).to_bytes(2, "big")
    + bytes(8)
)
try:
    decode(oversized)
except ValueError as error:
    print(f"oversized={error}")
```

The encoder emits known fields in tag order, independent of input-map insertion order. The 16-byte header accounts for a 41-byte frame around a 25-byte payload. The old reader deliberately projects away `currency`; the new reader applies a documented default to old data. Production evolution must decide whether both behaviors preserve the domain meaning.

The decoder checks maximum payload length before slicing or decoding, then exact frame length and a truncated digest. A production design would select a full-strength integrity construction appropriate to its accidental-corruption or adversarial threat model. A streaming decoder would also bound buffering time, cumulative bytes, nesting, collections, decompression, and parser resources.

Proof evidence includes schema compatibility tests, golden byte fixtures, property-based round trips over supported domains, malformed/fuzz corpora, cross-language results, registration manifests, recovery tests against retained bytes, and benchmark distributions. Passing only a happy-path round trip is insufficient.

## Alternatives and Trade-Offs

Self-describing text such as JSON is inspectable and widely supported, but verbose, weakly typed without an external schema, and susceptible to number, duplicate-key, Unicode, and canonicalization differences. Schema-based binary formats are compact and provide field evolution rules, but require schema distribution and disciplined tag/ID governance.

Avro carries writer/reader schema resolution and supports compact binary values without per-field names. Protocol Buffers uses numeric tags and unknown fields for evolution. Their compatibility details differ; neither prevents semantic misuse. Choose using language support, evolution model, data lifetime, random access, ecosystem, and benchmark evidence.

Arrow IPC represents columnar record batches close to analytical memory layout, improving vectorized exchange and reducing conversion in compatible runtimes. It can be less suitable for tiny independent messages or highly sparse evolving events. Buffer ownership and dictionary/schema sequencing become protocol concerns.

Engine-native object serializers maximize convenience and can be efficient with class registration, but couple bytes to runtime and application versions. Spark's tuning guidance contrasts Java serialization with faster, more compact Kryo and notes buffer and registration considerations. Use native serializers inside their declared compatibility horizon, not as ungoverned durable contracts.

Fixed schemas and generated code improve speed and type checks but add deployment coordination. Dynamic schemas support heterogeneous data but shift failures to runtime. Schema registries centralize governance and compatibility checks while adding availability, cache, authorization, and identity dependencies.

Per-record compression handles large independent messages but repeats setup and leaks size per record. Batch compression improves ratio and amortization but expands retry/failure units and latency. Compressing at transport, block, column, or field level changes selective access and corruption scope.

Canonical bytes simplify signing and content addressing but cost sorting/normalization and can be fragile across implementations. A stable semantic digest over a purpose-built projection may be safer than canonicalizing an entire evolving message. Preserve the original signed bytes when verification depends on them.

## Failure Modes and Misconceptions

1. **Serialization is only a performance choice.** It also defines correctness, evolution, recovery, and attack surface.
2. **A codec is a complete protocol.** Framing, schemas, limits, sequencing, and errors remain.
3. **A successful decode preserves meaning.** Units and domain semantics can still differ.
4. **A round trip proves compatibility.** It covers one version/direction and perhaps one implementation.
5. **Backward compatibility covers rolling upgrades.** Old readers may still receive new writers.
6. **Adding any field is safe.** Requiredness, defaults, old readers, and semantics determine safety.
7. **Missing, null, zero, and false are equivalent.** They can represent distinct domain states.
8. **Removed tags may be reused.** Retained bytes can then be misinterpreted.
9. **Unknown fields are always preserved.** Intermediaries and conversions may drop them.
10. **Matching class names imply wire compatibility.** Layout, registration, libraries, and custom code drift.
11. **Matching schema IDs imply matching schemas.** Mutable registries or collisions violate the claim.
12. **Map iteration order is canonical.** Many data models treat maps as unordered.
13. **Deterministic today means stable forever.** Some modes promise only one binary/version.
14. **Semantic equality implies byte equality.** Valid encodings can differ.
15. **A checksum authenticates a producer.** An attacker can recompute an unkeyed checksum.
16. **TLS protects retained blocks.** Its protection ends at the connection endpoints.
17. **Encryption replaces application validation.** Authenticated bad data remains bad.
18. **Length prefixes make framing safe.** Unchecked lengths drive memory exhaustion and overflow.
19. **Compressed size bounds decoded size.** Expansion can be orders of magnitude larger.
20. **Internal workers are trusted.** Credentials, nodes, dependencies, and inputs can be compromised.
21. **Object deserialization is passive.** Some formats can instantiate classes or execute callbacks/code.
22. **Zero-copy means no work.** Validation, ownership, alignment, and conversion still apply.
23. **Larger batches are always faster.** They increase latency, memory, unfairness, and retry scope.
24. **Average record size is representative.** Maxima and tails determine buffers and failures.
25. **Wire correctness proves domain safety.** Domain meaning and consequences need separate review.

## Worked Examples

### Example 1

**Question:** Can workers send consecutive variable-length records without framing?

**Reasoning:** The receiver cannot reliably locate boundaries unless the codec is self-delimiting and the stream contract says how completion works.

**Conclusion:** Define framing even when the payload format is familiar.

### Example 2

**Question:** A new reader adds `currency="USD"` as a default. Is old data known to be USD?

**Reasoning:** No. The default is reader behavior. Historical records may be unknown or governed by an external invariant that must be proven.

**Conclusion:** Defaults do not create historical evidence.

### Example 3

**Question:** Can raw Protocol Buffer bytes be used directly as stable content hashes?

**Reasoning:** Default serialization order is not guaranteed, and deterministic mode has a limited scope. Define a stable canonical projection or another identity scheme.

**Conclusion:** Do not hash incidental encodings.

### Example 4

**Question:** Why might equal join keys reach different partitions after a worker-language change?

**Reasoning:** String normalization, integer width, decimal representation, hash implementation, or serialized key bytes may differ.

**Conclusion:** Partition keys require cross-language semantic and byte tests.

### Example 5

**Question:** A frame advertises a 20-GB payload to a worker with a 256-MB limit. When should it fail?

**Reasoning:** Immediately after bounded header validation, before allocating or reading the declared body.

**Conclusion:** Enforce sizes before resource commitment.

### Example 6

**Question:** Does a valid CRC prove a block came from the authorized producer?

**Reasoning:** No. CRC detects accidental corruption; anyone who changes bytes can recompute it.

**Conclusion:** Use authenticated integrity when the threat model requires origin assurance.

### Example 7

**Question:** Why can a serializer upgrade break only after executor loss?

**Reasoning:** Surviving workers use in-memory values, while replacements deserialize retained shuffle/state bytes with new classes or registrations.

**Conclusion:** Recovery is part of the compatibility matrix.

### Example 8

**Question:** A 10-KB compressed batch expands to 2 GB. Is the wire-size limit sufficient?

**Reasoning:** No. Bound uncompressed bytes and ratio while streaming decompression.

**Conclusion:** Compression creates a second resource boundary.

### Example 9

**Question:** When is Arrow-style columnar IPC preferable to record-at-a-time objects?

**Reasoning:** For analytical batches where compatible consumers operate on columns and can honor schema/buffer contracts, it amortizes metadata and enables vectorized access.

**Conclusion:** Representation should match access pattern and lifetime.

### Example 10

**Question:** Can cross-language decoding tests approve a clinical dosage message?

**Reasoning:** No. Drug identity, units, concentration, route, patient/context identity, range checks, contraindications, provenance, corrections, downtime, accessibility, and clinical consequences require named pharmacy, prescribing, nursing, clinical-informatics, medication-safety, patient-safety, privacy/security, interoperability, operations, and independent clinical-safety review. No external approval is claimed here.

**Conclusion:** Byte interoperability is only one clinical-safety obligation.

## Cross-Program Connections

[Computer Architecture](../../23-computer-architecture/ROADMAP.md) supplies byte order, alignment, memory hierarchy, SIMD, and representation. [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies buffers, virtual memory, files, sockets, and zero-copy mechanisms. [Network Engineering](../../24-network-engineering/ROADMAP.md) supplies transport framing, congestion, MTUs, TLS, and network measurement.

[Security Engineering](../../25-security-engineering/ROADMAP.md) owns parser attack surfaces, authentication, encryption, keys, fuzzing, and threat modeling. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) owns delivery, version negotiation, failure, consistency, and replay. [Database Engineering](../../18-database-engineering/ROADMAP.md) owns tuple representation, pages, logs, recovery records, and type semantics.

[Data Engineering](../../19-data-engineering/ROADMAP.md) owns event and dataset contracts. [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) owns organization-wide schema identity, semantics, and governance. This program owns high-volume runtime transfer among cluster workers and the effect on shuffle, state, scheduling, and recovery.

Protocol Buffers illustrates tagged fields, unknown values, and limited deterministic guarantees. Avro illustrates explicit writer/reader schema resolution. Arrow illustrates columnar buffers and IPC batches. Spark illustrates application-scoped serializer performance and compatibility. Flink illustrates state serializer snapshots and migration constraints. CBOR specifies deterministic encoding options and decoder resource threats. Python documents the code-execution risk of unsafe object deserialization.

## References

- Protocol Buffers Project, [*Encoding*](https://protobuf.dev/programming-guides/encoding/), checked 2026-09-03. Official wire types, field order, unknown-field, and deterministic-serialization scope.
- Protocol Buffers Project, [*Language Guide (proto3): Updating a Message Type*](https://protobuf.dev/programming-guides/proto3/#updating), checked 2026-09-03. Official field-number reservation and compatible message evolution guidance.
- Apache Avro Project, [*Specification 1.12.0*](https://avro.apache.org/docs/1.12.0/specification/), checked 2026-09-03. Official schema, binary encoding, framing, canonical form, and reader/writer resolution.
- Apache Arrow Project, [*Arrow Columnar Format: Serialization and IPC*](https://arrow.apache.org/docs/format/Columnar.html#serialization-and-interprocess-communication-ipc), checked 2026-09-03. Official schema, record-batch, dictionary-batch, buffer, stream, and file representation.
- Apache Spark Project, [*Tuning: Data Serialization*](https://spark.apache.org/docs/latest/tuning.html#data-serialization), checked 2026-09-03. Official current Java/Kryo performance, registration, and buffer guidance.
- Apache Spark Project, [*Serializer API*](https://spark.apache.org/docs/latest/api/java/org/apache/spark/serializer/Serializer.html), checked 2026-09-03. Official statement that Spark serializers are application-scoped and need not be wire-compatible across versions.
- Apache Flink Project, [*State Schema Evolution*](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/serialization/schema_evolution/), checked 2026-09-03. Official current serializer compatibility, migration, key, POJO, Avro, and Kryo constraints.
- Python Software Foundation, [*pickle — Python Object Serialization*](https://docs.python.org/3/library/pickle.html), checked 2026-09-03. Official arbitrary-code risk and trusted-input warning.
- Carsten Bormann and Paul Hoffman, [*RFC 8949: Concise Binary Object Representation*](https://www.rfc-editor.org/rfc/rfc8949.html), IETF, 2020. Standards-track encoding, deterministic representation, well-formedness, validity, and resource-exhaustion guidance.
- Tim Bray, [*RFC 8259: The JavaScript Object Notation Data Interchange Format*](https://www.rfc-editor.org/rfc/rfc8259.html), IETF, 2017. Standards-track JSON grammar, interoperability, parser limits, numbers, strings, and security considerations.

## Exercises

### Exercise 1

Design a worker frame for compressed schema-based batches. Name header fields, validation order, integrity coverage, and limits.

### Exercise 2

A version adds optional `currency`, renames `amount` semantics from cents to micros under the same field tag, and deletes `memo`. Classify each change and propose a safe evolution.

### Exercise 3

Create a rolling-upgrade compatibility matrix for old/new writers and readers plus retained checkpoint bytes. State the required tests and rollback evidence.

### Exercise 4

A workload sends 50 million 80-byte logical records. Individual encoding adds 18 bytes per record; batches of 1,000 add a 200-byte batch header and compress payload plus header to 40%. Compare approximate wire bytes before transport overhead, then name omitted costs.

### Exercise 5

A clinical dataflow exchanges medication-administration records between mixed-language workers and restores them from checkpoints. Specify semantic, framing, evolution, security, recovery, test, and named review requirements.

## Answers to the Exercises

### Answer 1

Use magic and envelope version; message/batch type; codec and immutable schema ID; compression algorithm/level flags; compressed and declared uncompressed lengths; record count; graph/exchange, producer partition/attempt, target, sequence, and completion identity where needed; payload; and checksum or authenticated tag covering every field that influences interpretation. Validate a bounded fixed header, supported versions/flags/codecs, integer arithmetic, wire/uncompressed/count/depth/ratio limits, authorization and replay context, exact frame/chunk completion, authenticated integrity, decompression limits, payload decode, schema constraints, and application invariants in that order as applicable. Define byte order and failure behavior.

### Answer 2

Adding optional `currency` can be structurally compatible if old readers ignore/preserve it and new readers have a semantically valid missing-field rule; historical currency still needs evidence. Reinterpreting `amount` from cents to micros under one tag is semantically incompatible even if the integer decodes. Add a new `amount_micros` field with explicit unit and migration, dual-write/read during transition, validate equivalence, then retire the old tag without reuse. Deleting `memo` requires checking required readers, unknown-field preservation, retention, legal/audit semantics, and reserving its identity. Compatibility is directional and must be tested through intermediaries.

### Answer 3

Test old-writer to old-reader as baseline, old-writer to new-reader for backward compatibility, new-writer to old-reader for forward compatibility during overlap/rollback, and new-writer to new-reader. Restore every supported old checkpoint with new code, and if rollback is allowed, determine whether old code can read checkpoints written after upgrade. Use real golden bytes across every language, schema and registration manifests, extremes/unknown/missing/invalid cases, state invariants, deterministic identities, partial/corrupt frames, and failure injection during migration. Retain old binaries/decoders, source checkpoint copies, migration progress/receipts, rollback criteria, and a restore drill—not only unit-test claims.

### Answer 4

Individual frames use `50,000,000*(80+18)=4,900,000,000` bytes. Batching creates 50,000 batches; before compression the bytes are `50,000,000*80 + 50,000*200 = 4,010,000,000`, and at 40% approximately `1,604,000,000` bytes. This excludes transport framing, checksums/tags not included in the stated header, indexes, retransmission, dictionary/schema traffic, encryption padding, unsuccessful compression, encode/decode CPU, buffering latency, peak memory, allocation/GC, tails, retries, and partial-batch waste. Measure them on the actual distribution.

### Answer 5

Define drug/product identity, patient/encounter, dose value, decimal precision/scale, unit, concentration, route, administration/recorded times and zones, status, provenance, corrections, missing/null semantics, and clinical invariants. Use an immutable schema ID, bounded authenticated frame, explicit byte order/framing/compression limits, reserved field identities, old/new/rollback and checkpoint migration matrix, unknown-field policy, safe data-only decoders, and encryption/access controls. Fence partition/task attempts, bind frames to checkpoint/exchange generations, preserve old decoders/source checkpoints, and test mixed languages, extremes, unit confusion, Unicode identifiers, duplicates, late correction, corruption, truncation, malicious sizes/nesting, executor loss, restore, rollback, and downtime. Named reviewers include pharmacists, prescribing clinicians, nursing/administration workflow, clinical informatics/interoperability, medication-safety and patient-safety owners, privacy/governance, cybersecurity, distributed-runtime and disaster-recovery engineers, accessibility, regulatory/legal owners, and independent clinical-safety assurance. These internal checks do not constitute external approval.
