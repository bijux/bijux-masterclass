---
module_id: LSDS-093
program: Large-Scale Data Systems Engineering
level: 2
module_number: 93
title: Serialization and Compression Trade-Offs
status: complete
last_verified: 2026-09-04
---

# Serialization and Compression Trade-Offs

## One-Page Review

### Governing question

How should an engineer choose and evolve representations, serialization encodings, compression codecs, block boundaries, and settings so distributed data remains correct and interoperable while minimizing end-to-end CPU, memory, network, storage, latency, and recovery cost?

### Essential definitions

- **representation** is the in-memory logical/physical layout presented to computation, such as row objects or columnar arrays.
- **serialization** maps values and schema context into bytes; **deserialization** reconstructs values under a reader contract.
- An **encoding** maps typed values to byte patterns, for example varints, dictionary indices, delta values, or bit-packed runs.
- A **compression codec** transforms a byte stream losslessly or lossily according to an explicit contract; this module assumes lossless data codecs unless stated.
- **compression ratio** is $r=U/V$, where $U$ is encoded bytes before compression and $V$ is compressed bytes; larger $r$ means fewer output bytes.
- A **frame, page, block, or batch** is an independently delimited unit for parsing, compression, checksums, seeking, retry, or parallelism.
- **schema resolution** applies writer and reader schemas to decide how fields/types/defaults evolve.
- **canonicalization** defines one stable byte representation when equality by bytes, hashing, signing, or deduplication requires it.
- A **compression dictionary** is shared prior data/model state needed to encode or decode efficiently.
- **codec amplification** includes temporary buffers, copies, decompressed expansion, and CPU beyond nominal output size.

### Central model, mechanism, or theorem

Separate the pipeline:

$$values\xrightarrow{representation/encoding}U\xrightarrow{codec}V\xrightarrow{framing}wire/storage,$$

with $r=U/V$. For a non-overlapped path of bandwidth $b$, a candidate's approximate service time is:

$$T=t_{ser}+t_{comp}+V/b+t_{decomp}+t_{deser}.$$

Real pipelines overlap stages, share CPU/cache/memory bandwidth, and incur queueing, so benchmark the executed topology rather than treating this sum as a universal latency formula. Compression is beneficial for elapsed time only when avoided I/O and downstream effects exceed codec CPU, buffering, and operational cost. Encoding often changes compressibility first; column projection, dictionary/delta/RLE encoding, and block size can matter more than codec brand.

Choose per boundary: in-memory cache, shuffle, RPC/event, checkpoint, and analytical file have different lifetime, schema, seek, splittability, and compatibility requirements. Optimize only among candidates that preserve semantic round trips, evolution, corruption detection, resource bounds, and every consumer's codec/format support.

### Critical invariants

- Decode under the declared writer/reader schema preserves the required values, nullability, ordering, precision, and logical types.
- Format, schema, codec, level, dictionary, checksum, encryption, and framing identifiers are sufficient for independent recovery.
- Blocks are bounded for allocation, decompression, retry loss, seek, and parallel decode.
- Split boundaries never begin inside undecodable codec state unless an index or preceding context is supplied.
- Byte equality is never used as semantic equality unless canonical serialization is explicitly guaranteed.
- Unknown fields, defaults, removed identifiers, and type conversions follow tested evolution rules across all supported versions/languages.
- Compression and decompression resource limits defend against malformed lengths, excessive ratios, deep nesting, and crafted CPU/memory consumption.
- Checksums cover the intended compressed or uncompressed domain, and corruption is never silently accepted as valid records.
- Metrics distinguish logical values, encoded bytes, compressed bytes, physical transferred/stored bytes, and decompressed working memory.
- Benchmarks pin data distribution, hardware, libraries, warm-up, concurrency, block size, codec level, schema, and correctness oracle.

### Common failures

Common failures include choosing the smallest sample output; comparing codecs at different levels or block sizes; compressing already compressed/encrypted bytes; double-compressing; using one format for shuffle and century-scale storage; forgetting decompression CPU; measuring producer throughput while consumers regress; ignoring memory/copy amplification; making a whole file one unsplittable frame; training a dictionary that decoders cannot identify; reusing removed field numbers; assuming default serialization is deterministic; hashing noncanonical bytes; changing key serialization across state restore; accepting corrupt/truncated frames as partial success; trusting claimed ratios without representative data; and benchmarking only warm, homogeneous, low-concurrency input.

### Compact example

One 1,000-MiB encoded batch crosses a 50-MiB/s bottleneck. With 2 seconds each for serialization/deserialization, uncompressed service time is 24 seconds. A fast codec produces 500 MiB with 4-second compression and 3-second decompression, totaling 21 seconds. A denser codec produces 300 MiB but spends 12 and 8 seconds in codec work, totaling 30 seconds. The densest result loses this latency objective; it could still win storage-at-rest cost if reads are rare and compatibility is proven.

### Connections

[LSDS-063](063-exchange-operators.md) supplies shuffle boundaries, [LSDS-066](066-vectorized-execution-at-cluster-scale.md) supplies columnar representation, [LSDS-074](074-schema-evolution-at-scale.md) supplies table evolution, [LSDS-089](089-schema-and-code-changes-during-reprocessing.md) supplies replay compatibility, [LSDS-091](091-partition-count-and-task-granularity.md) supplies block/task granularity, and [LSDS-092](092-memory-pressure-spill-and-garbage-collection.md) supplies buffer and expansion accounting.

## Governing Question

Distributed systems cross many byte boundaries: closures sent to workers, shuffle records, cached partitions, event logs, RPC messages, checkpoint state, spill runs, table pages, manifests, and results. Each boundary has different priorities. A shuffle may value decode speed and short lifetime; an archive may value ratio and decades of readable schemas; an event needs independent framing and mixed-version evolution; a columnar file needs projection and skipping.

The governing question is how to decompose the choice, quantify the complete path, preserve semantics across versions and languages, and keep recovery possible when a block is truncated, corrupt, unavailable, too large, or written by older code.

## Why This Matters

Bytes influence every large-scale resource. Smaller payloads can reduce network, disk, cache, object requests, and retry time, but stronger compression consumes CPU, memory bandwidth, buffers, and latency. Compact serialized state may reduce garbage collection yet make each access decode. Larger blocks improve ratio and amortize metadata but enlarge buffers and lost work, weaken seeking, and reduce parallelism.

Correctness risks are less visible than performance. A field renumbering can reinterpret old bytes. A default may change business meaning. A noncanonical encoding can produce distinct byte strings for equal values. A state-key serializer change can move logical keys. Missing codec/dictionary support can make a durable dataset unreadable. These are protocol and lifecycle decisions, not local micro-optimizations.

## Prerequisites and Retrieval

Review exchange operators in [LSDS-063](063-exchange-operators.md), vectorized execution in [LSDS-066](066-vectorized-execution-at-cluster-scale.md), schema evolution in [LSDS-074](074-schema-evolution-at-scale.md), reprocessing compatibility in [LSDS-089](089-schema-and-code-changes-during-reprocessing.md), partition granularity in [LSDS-091](091-partition-count-and-task-granularity.md), and memory/spill behavior in [LSDS-092](092-memory-pressure-spill-and-garbage-collection.md).

You should understand schemas, logical/physical types, byte order, varints, dictionaries, RLE/delta/bit packing, checksums, framing, row/column layouts, projection, random access, shuffle, state snapshots, cache locality, CPU and memory bandwidth, percentiles, and backward/forward compatibility.

For evaluation retain format/schema/codec/dictionary identifiers and versions; field/type/null/default metadata; block/page/batch sizes; record counts/distributions/cardinality/order; logical/encoded/compressed/physical bytes; serialize/compress/transfer/decompress/deserialize CPU and elapsed time; temporary/peak memory; copies; cache misses; network/disk throughput; seek/projection bytes; corruption failures; retries; cross-language/version matrix; worker shape; concurrency; and cost.

## Learning Objectives

After this module, you should be able to:

1. separate representation, value encoding, compression, framing, and schema resolution;
2. compute ratio and a transparent service-time estimate without overclaiming pipeline behavior;
3. explain how data distribution and encodings influence compressibility;
4. choose block boundaries for ratio, memory, seek, parallelism, and retry trade-offs;
5. preserve semantic and schema compatibility across versions and languages;
6. distinguish semantic determinism from byte-level canonicalization;
7. design bounded, corruption-aware, independently recoverable frames;
8. benchmark producer and consumer paths with representative data and complete resource metrics;
9. choose different policies for shuffle, events, cache, state, and archival files; and
10. roll out format/codec changes with dual-read evidence and rollback.

## Core Exposition

### Decompose the byte pipeline

Do not call every transformation “serialization.” In-memory layout controls locality and object overhead. Serialization defines typed bytes and schema context. Encodings exploit value structure. Compression exploits byte redundancy. Framing creates boundaries and metadata. Encryption usually destroys compressibility and belongs after compression.

Measure each stage separately and together. Changing a column encoding can reduce input to the codec, change its ratio, and lower decode work. Removing copies can improve latency without changing byte count. The decomposition makes causal comparisons possible.

### Begin with the contract lifetime

Ask who reads the bytes, for how long, in which languages and versions, with what failure/recovery behavior. Ephemeral shuffle bytes can be regenerated by the same job version. Checkpoints must restore compatible state across upgrades. Event logs may have mixed writers/readers. Table files outlive engines and organizations.

Longer-lived boundaries need open, stable specifications, embedded or resolvable schema/codec metadata, compatibility policy, test corpora, and migration/retention plans. A faster private serializer is a liability if the only decoder disappears.

### Match representation to access

Row-oriented layouts favor reconstructing whole records and transactional access. Columnar layouts favor projection, vectorized scans, compression by homogeneous type, and statistics-based skipping. Nested data complicates both with definition/presence structure and irregular access.

Avoid converting row to column to row at every operator boundary. Count conversions, copies, and materialized columns. Zero-copy claims require compatible ownership, alignment, lifetime, byte order, and representation; metadata-only reconstruction is not universally zero cost.

### Use value encodings deliberately

Small nonnegative integers benefit from varints; signed values may need zigzag mapping. Repeated low-cardinality values can use dictionaries and integer indices. Runs benefit from RLE, monotonic values from delta encoding, and bounded integers from bit packing. Byte-stream splitting can make numeric byte lanes easier for a general codec to compress.

Encodings can regress on high cardinality, random data, negative-number choices, tiny batches, or frequent dictionary fallback. Record per-column decisions and fallback rates. Encoding must remain interoperable with the format specification and reader implementations.

### Understand codec trade-offs

Fast codecs often target low CPU and moderate ratio; stronger codecs may spend more CPU/memory for smaller output. Levels move along a codec-specific curve. Hardware acceleration, implementation version, vector instructions, dictionary use, and threading change that curve.

Do not rank codecs by name. Measure compression and decompression separately because write-once/read-many data weights decode heavily, while archival data may weight encode less. A network-bound shuffle and CPU-bound query can choose differently.

### Choose block and frame boundaries

Larger blocks expose more redundancy and amortize headers/checksums, often improving ratio. They also require larger buffers, increase latency to the first record, enlarge corruption/retry scope, reduce independent parallelism, and can make selective reads decompress irrelevant data.

Smaller blocks improve seek, streaming, memory bounds, and fault isolation but add metadata and may reduce ratio. Align pages/row groups/batches with expected projection, predicate skipping, transport messages, object range reads, and task sizes. Keep explicit maximum compressed and decompressed lengths.

### Preserve splittability and random access

A splittable container provides indexes or independent frames so workers can begin at safe boundaries. A stream whose block depends on all prior codec state cannot be divided arbitrarily. File-level compression around an already blocked columnar format can destroy its native seeking and parallelism.

Validate range reads, footer/index discovery, truncated tails, concatenated frames, and partial corruption. Plan how metadata itself is replicated, checksummed, or reconstructed.

### Design schema evolution

Store or resolve the writer schema and apply explicit reader-schema rules. Adding a nullable/defaulted field may be compatible in one format but not semantically safe for every consumer. Widening types can lose precision in another language. Renames may look like delete-plus-add without stable identifiers.

Never reuse retired field numbers/IDs where the wire format attaches meaning to them. Preserve unknown fields when round-tripping requires it. Test old-writer/new-reader, new-writer/old-reader, mixed-version pipelines, defaults, nulls, enums, unions, maps, nested values, and reserialization.

### Distinguish determinism and canonical bytes

Correct decoders may accept field orders or representations that encode the same semantic value. A deterministic option may be stable only for one binary/version and still not define a cross-language canonical form. Therefore do not use ordinary serialized bytes as a content hash, signature input, ordering key, or deduplication identity.

If byte identity matters, define and test canonical field order, map ordering, numeric forms, Unicode handling, defaults, unknown fields, floating-point edge cases, and schema version. Alternatively hash a deliberately normalized semantic projection.

### Account for memory and copies

Compression needs input/output buffers, codec state, dictionaries, and possibly whole-block materialization. Decompression expands $V$ back toward $U$ and then may create object/vector memory. Concurrent tasks multiply peaks. JNI crossings and language workers may add copies.

Record peak resident memory and allocation failures at encode and decode, not only average byte ratio. Bound advertised uncompressed lengths before allocation. Stream where possible and use allocator ownership consistent with [LSDS-092](092-memory-pressure-spill-and-garbage-collection.md).

### Protect against hostile or corrupt input

Treat lengths, nesting, dictionary references, checksums, and codec frames as untrusted. Cap compressed/uncompressed size, ratio, nesting, records, and CPU/time per frame. Reject unsupported format/codec/schema versions explicitly. Fuzz parsers and test truncation, bit flips, duplicate fields, malformed varints, and oversized declarations.

Checksums detect corruption only for their coverage domain and algorithm. Encryption/authentication may provide integrity at a different layer. Verify before publishing decoded records; do not silently skip corrupt bytes unless the data contract explicitly permits quarantined partial recovery.

### Avoid redundant compression

Already compressed images, archives, encrypted payloads, and high-entropy identifiers may expand or waste CPU. Column encodings plus page compression can be useful; wrapping the whole file in another codec may eliminate access advantages for little gain. Transport compression around already compressed IPC buffers can do the same.

Sample per data class and allow a codec to store incompressible blocks raw when the format supports it. Observe ratio distributions, not only aggregate ratio dominated by one easy column.

### Weight the whole lifecycle

For write-once/read-many data, multiply decode and transferred bytes by expected scans, including projection and cache behavior. For shuffle, include both producer and consumer CPU and the bottleneck link. For checkpoints, include snapshot time, storage, restore, and failure frequency. For events, include broker batch compression, consumer fleet, and retention.

Storage savings can shift cost to every query. Conversely, a stronger codec may reduce scan cost if I/O is limiting and decode is vectorized. Express the objective in dollars, worker-hours, latency/SLO, energy, or capacity—not ratio alone.

### Benchmark fairly

Use representative records including cardinality, sortedness, nulls, widths, nested depth, skew, entropy, and already-compressed fields. Keep format, encoding, block size, codec level, checksum, thread count, library, hardware, and concurrency explicit. Warm up JIT/cache when appropriate and retain cold-start results when they matter.

Verify round-trip values and schema behavior for every candidate before comparing. Report distributions and confidence across producer CPU, consumer CPU, wall time, bytes, peak memory, copies, random/projection reads, and corruption handling.

### Roll out safely

Inventory every reader before writing a new codec or format feature. Canary with dual-read verification, then expand writers only after old/new consumers pass. Keep rollback able to read newly written data or stop new writes without stranding it. For durable data, backfill or retain old decoders until the final old object expires.

Tag output with exact format/codec/schema/dictionary/library policy. Monitor unsupported-codec, decode, checksum, size, latency, and fallback errors by producer and consumer version.

### Observe continuously

Dashboard logical records/bytes, encoded $U$, compressed $V$, $r$, physical transfer/store bytes, block/page/batch sizes, serialize/compress/decompress/deserialize CPU and elapsed time, queueing, peak memory, allocations/copies, projected/read bytes, cache behavior, corruption, retries, and cost.

Segment by boundary, dataset/table/topic/state/operator, field/type/column, producer/consumer language and version, format/schema/codec/level/dictionary, block size, hardware, concurrency, input distribution/entropy, percentile, cache state, and time window.

## Definitions and Notation

Let:

- $U$ be bytes after serialization/encoding but before general compression;
- $V$ be compressed payload bytes and $r=U/V$ the compression ratio;
- $B$ be effective bottleneck transfer bandwidth;
- $t_s,t_c,t_x,t_d,t_r$ be serialization, compression, transfer, decompression, and reconstruction times;
- $M_e,M_d$ be peak encode/decode working memory;
- $q$ be expected number of reads over the object's lifetime;
- $f$ be frame/block size and $n=\lceil U/f\rceil$ nominal blocks before variable effects;
- $A_w,A_r$ be physical write/read amplification relative to logical bytes; and
- $p_f$ be probability of failure requiring retransmission or recomputation of a frame.

For a strictly sequential approximation, $T=t_s+t_c+V/B+t_d+t_r$. For a fully streaming pipeline, throughput approaches the slowest saturated stage after startup, while latency includes fill/drain and queueing. Neither model substitutes for measurement. $r$ must state which pre-compression representation defines $U$.

## Mechanisms, Invariants, or Proof Structure

### Semantic round-trip argument

For every admitted value and supported writer/reader schema pair, decode(reader, metadata, encode(writer, value)) must produce the specified semantic projection, including null/default/unknown/precision rules. Test boundaries and cross-language implementations, not only one object type.

### Break-even argument

Relative to uncompressed $U/B$, compression saves $(U-V)/B$ transfer time in the simple sequential model. It wins latency only if this and other downstream savings exceed compression/decompression/buffering overhead. Pipelining, contention, projection, and caching alter the empirical break-even.

### Frame-recovery argument

Each independently recoverable frame declares bounded lengths and necessary codec/dictionary/schema identity, has verified integrity, and begins at a valid decode state. An index maps logical ranges to frames. Failure discards or retries a known unit without accepting partial records.

### Compatibility argument

Maintain a matrix of supported writer and reader versions/languages, apply the format's exact evolution rules, and prove old retained bytes remain readable throughout rollback and retention. Wire parse compatibility alone does not prove application semantic compatibility.

### Adversarial verification

Test empty/tiny/huge batches, high/low cardinality, sorted/random values, null-heavy/wide/nested rows, negative/boundary integers, Unicode, NaNs and signed zero, unknown/removed fields, incompressible/already-compressed/encrypted values, missing/wrong dictionaries, truncated/corrupt frames, malicious sizes/ratios/nesting, cross-version/language round trips, and cold/concurrent resource pressure.

## Alternatives and Trade-Offs

| Choice | Strength | Cost or limitation |
|---|---|---|
| Row/object representation | Convenient whole-record access | Object overhead, copies, weaker analytical locality |
| Columnar/vector representation | Projection, locality, type-specific encoding | Conversion and irregular mutation/nesting costs |
| Self-describing text | Inspectable and flexible tooling | More bytes, parse CPU, ambiguous canonicalization |
| Schema-driven binary | Compact and typed | Requires schema/ID governance and compatible decoders |
| Fast codec/low level | Low CPU and latency | Usually less byte reduction |
| Dense codec/high level | Lower storage/network bytes | More CPU, latency, memory, and possible fleet bottleneck |
| Large blocks | Better ratio and metadata amortization | More memory, lost work, latency, weaker selection |
| Small blocks | Seek, parallelism, bounded retry | More headers/checksums and often lower ratio |
| Shared dictionary | Strong ratio for small/repetitive messages | Distribution, identity, lifecycle, and mismatch risk |
| No compression | Minimal codec CPU and complexity | Higher I/O, storage, cache, and transfer demand |

## Failure Modes and Misconceptions

1. **Best ratio means best system.** CPU, latency, memory, projection, and consumers may lose.
2. **Serialization and compression are the same layer.** Representation and encoding alter the codec input first.
3. **One format fits every boundary.** Shuffle, event, checkpoint, and archive lifetimes differ.
4. **Codec defaults are comparable.** Levels, blocks, libraries, and hardware must be pinned.
5. **Producer throughput is enough.** Every consumer and recovery path pays decode costs.
6. **Larger blocks are always better.** Seek, buffers, corruption scope, and parallelism regress.
7. **Whole-file compression is harmless.** It can destroy native splitability and projection.
8. **Binary output is canonical.** Many valid serializers do not guarantee stable byte order.
9. **Wire-compatible means semantically safe.** Defaults, precision, enums, and application rules can break.
10. **Removed IDs may be reused.** Old bytes can acquire a new meaning.
11. **Unknown fields always survive.** Some conversions or field-by-field copies discard them.
12. **Double compression saves more.** It commonly wastes CPU and harms access for little reduction.
13. **Compressed size bounds memory.** Decode expansion and concurrent buffers determine peaks.
14. **Checksum guarantees authenticity.** Coverage and threat model determine what it proves.
15. **A sample ratio generalizes.** Entropy, order, cardinality, nulls, and widths drift.

## Worked Examples

### Example 1

A 1,000-MiB encoded batch at 50 MiB/s takes 20 seconds to transfer before serialization and reconstruction costs.

### Example 2

A fast codec halves bytes but adds 7 seconds of codec work; it saves 3 seconds end to end in the compact example.

### Example 3

A denser codec shrinks to 300 MiB but adds 20 seconds of codec work, totaling 30 seconds and losing the latency comparison despite its 3.33 ratio.

### Example 4

Dictionary encoding converts repeated country strings into compact indices, while unique UUID strings overflow the dictionary and fall back.

### Example 5

Wrapping an indexed columnar file in one gzip stream prevents workers from independently range-reading row groups.

### Example 6

Two valid protocol messages with reordered fields decode equally but yield different byte hashes without canonicalization.

### Example 7

An old reader preserves an unknown binary field through message-level copying but loses it after conversion to JSON and reconstruction.

### Example 8

A 64-MiB compressed frame advertises 64 TiB uncompressed; the decoder rejects it before allocating or expanding.

### Example 9

A checkpoint codec saves storage but adds four minutes to recovery, changing failure-cost economics despite normal-run savings.

### Example 10

The executable fixture compares uncompressed, fast, and dense candidates under one transparent sequential service-time model.

<!-- bijux-verify: {"id":"serialization-compression-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"bandwidth_mib_s=50.0\nuncompressed_ratio=1.00\nuncompressed_time_s=24.0\nfast_ratio=2.00\nfast_time_s=21.0\ndense_ratio=3.33\ndense_time_s=30.0\nlatency_winner=fast\n","stderr":""}} -->
```python
encoded_mib = 1000.0
bandwidth_mib_s = 50.0
serialize_s = 2.0
deserialize_s = 2.0
candidates = {
    "uncompressed": (1000.0, 0.0, 0.0),
    "fast": (500.0, 4.0, 3.0),
    "dense": (300.0, 12.0, 8.0),
}

times = {}
print(f"bandwidth_mib_s={bandwidth_mib_s:.1f}")
for name, (payload_mib, compress_s, decompress_s) in candidates.items():
    ratio = encoded_mib / payload_mib
    total = serialize_s + compress_s + payload_mib / bandwidth_mib_s + decompress_s + deserialize_s
    times[name] = total
    print(f"{name}_ratio={ratio:.2f}")
    print(f"{name}_time_s={total:.1f}")
print(f"latency_winner={min(times, key=times.get)}")
```

## Cross-Program Connections

- **Data structures:** rows, columns, dictionaries, tries, runs, bitmaps, varints, deltas, and bit packing shape bytes before compression.
- **Information theory:** entropy and redundancy bound what lossless codecs can exploit, while real implementations add finite-block overhead.
- **Computer architecture:** cache locality, SIMD, memory bandwidth, branches, copies, and accelerators determine encode/decode cost.
- **Distributed systems:** framing, checksums, retries, mixed versions, one-winner output, and recovery define the byte contract.
- **Storage:** pages, row groups, indexes, object ranges, projection, compaction, and retention determine block value over time.
- **APIs and events:** field identifiers, unknown fields, canonical forms, batching, and consumer fleets constrain evolution.
- **Security:** decompression bombs, parser bugs, integrity, encryption order, signatures, and untrusted schemas require bounded decoding.
- **Economics:** producer CPU, consumer multiplicity, storage duration, transfer, cache, migration, and failure recovery define total cost.

## References

1. Apache Spark, [Tuning](https://spark.apache.org/docs/latest/tuning.html). Current. Discusses serializer speed/size, registration, serialized caching, memory, and network trade-offs.
2. Apache Spark, [Configuration](https://spark.apache.org/docs/latest/configuration). Current. Documents serializers, buffers, internal codecs, compression controls, and levels.
3. Apache Spark, [SQL Performance Tuning](https://spark.apache.org/docs/latest/sql-performance-tuning.html). Current. Documents columnar cache compression and batch-size trade-offs.
4. Apache Parquet, [Encodings](https://parquet.apache.org/docs/file-format/data-pages/encodings/). Current. Specifies plain, dictionary, RLE/bit-pack, delta, and byte-stream-split encodings.
5. Apache Parquet, [Compression](https://parquet.apache.org/docs/file-format/data-pages/compression/). Current. Specifies supported page codecs and codec framing expectations.
6. Apache Parquet, [Configurations](https://parquet.apache.org/docs/file-format/configurations/). Current. Documents configurable page and row-group boundaries and their rationale.
7. Apache Avro, [Specification](https://avro.apache.org/docs/1.12.0/specification/). Version 1.12.0. Specifies binary encoding, object containers, schema resolution, and fingerprints.
8. Protocol Buffers, [Encoding](https://protobuf.dev/programming-guides/encoding/). Current. Defines tags, wire types, varints, field ordering, and noncanonical default serialization.
9. Protocol Buffers, [Proto3 Language Guide](https://protobuf.dev/programming-guides/proto3/). Current. Documents field-number stability, unknown fields, and message evolution rules.
10. Apache Arrow, [Columnar Format](https://arrow.apache.org/docs/format/Columnar.html). Current. Specifies memory layout, IPC framing, alignment, dictionaries, random access, and optional buffer compression.
11. Apache Flink, [Data Types and Serialization](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/serialization/). Current. Documents runtime type analysis and serializer selection.
12. Apache Flink, [State Schema Evolution](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/serialization/schema_evolution/). Current. Documents serializer compatibility and state/key evolution constraints.
13. IETF, [RFC 8878: Zstandard Compression](https://datatracker.ietf.org/doc/html/rfc8878). Informational RFC. Defines independent frames, blocks, bounded streaming memory, checksums, and media type.

## Exercises

### Exercise 1

Compare uncompressed and compressed service time for 2,000 MiB at 100 MiB/s when codec output is 800 MiB, compression costs 5 seconds, decompression costs 3 seconds, and shared serialize/deserialize cost is 4 seconds.

### Exercise 2

Design a benchmark for two codecs on null-heavy sorted telemetry, high-cardinality UUID events, and already-compressed image metadata across shuffle and archival boundaries.

### Exercise 3

Design a schema-evolution matrix for adding a field, retiring an identifier, widening an integer, adding an enum value, and preserving unknown fields across three languages.

### Exercise 4

Choose page/block boundaries for a 4-TiB analytical table that is usually read by two projected columns and occasionally fully scanned, with 8-GiB worker memory and object range reads.

### Exercise 5

Plan a safe migration to a new codec that 10% of the consumer fleet cannot yet decode and that changes decompression memory requirements.

## Answers to the Exercises

### Answer 1

Uncompressed transfer is $2000/100=20$ seconds, or 24 seconds including shared serialization/reconstruction. Compressed transfer is $800/100=8$ seconds; adding 5+3 codec seconds and 4 shared seconds gives 20 seconds. The simple sequential model saves 4 seconds. Validate pipelining, CPU contention, peak buffers, ratio distribution, and both endpoints before adopting it.

### Answer 2

Pin format, encoding, block size, levels, libraries, hardware, threads, and correctness checks. For each data class measure ratio distribution, producer and consumer CPU/elapsed time, peak memory/copies, shuffle transfer and backpressure, archival writes, projected and full reads, cold/warm cache, and corruption behavior. Already-compressed fields may be stored raw. Weight shuffle by immediate two-sided latency and archives by retention plus expected reads; do not average the three data classes into one flattering ratio.

### Answer 3

For every old/current/new writer and reader in each language, test binary round trip, reserialization, defaults/nulls, maximum/boundary values, enum handling, and unknown-field preservation. Adding a field needs defined absence semantics. Retired numeric identifiers remain reserved. Integer widening needs range and target-language precision tests. New enums need old-reader behavior. Include conversion through any JSON/text gateway because it may lose unknown fields. Record semantic compatibility separately from mere parse success.

### Answer 4

Use a splittable columnar container with per-column encodings, statistics/indexes, independently compressed pages inside row groups, and footer/index range discovery. Size row groups for worker/task parallelism and object-request economics below the 8-GiB expanded working-set budget; size pages for bounded decode and projection without excessive headers. Benchmark two-column range reads and full scans across candidate boundaries, including ratio, requests, peak memory, decompression, pruning, corruption scope, and retry. Do not wrap the entire object in one external stream.

### Answer 5

Inventory and upgrade/read-test the unsupported 10% before enabling new writes, or keep writers on the old codec. Canary dual-readable outputs, attach exact codec/version metadata, and run old/new readers with value/checksum equivalence plus peak-memory limits. Preserve rollback readers and prevent compaction/backfill from converting old data prematurely. Expand writes by cohort while monitoring unsupported-codec, OOM, latency, and corruption failures. Retire the old decoder only after every old object/checkpoint/event has expired or been verified and rewritten.
