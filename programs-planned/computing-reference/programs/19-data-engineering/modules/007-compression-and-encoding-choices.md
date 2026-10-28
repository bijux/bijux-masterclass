---
module_id: DE-007
program: Data Engineering
level: 1
module_number: 7
title: Compression and Encoding Choices
status: complete
last_verified: 2026-09-02
---

# Compression and Encoding Choices

## One-Page Review

### Governing question

How should a data engineer choose value encodings, compression codecs, frames, dictionaries and block sizes so that a pipeline reduces bytes without sacrificing interoperability, latency, resource safety, random access or reproducibility?

### Essential definitions

- **Value encoding** maps typed values or structural metadata to bytes using a representation such as plain, dictionary, delta, run-length, bit-packed or variable-length integer encoding.
- **Compression** maps a byte sequence losslessly to a usually smaller byte sequence by exploiting redundancy; decompression must recover the exact input bytes.
- A **codec** is a defined compression/decompression algorithm and format profile, including parameters required for interoperable decoding.
- A **frame** wraps compressed blocks with boundaries and metadata such as magic, sizes, flags, dictionary ID or checksums.
- A **block** is an independently bounded compression unit; block dependency determines whether later blocks can decode without earlier history.
- A **compression level** selects a codec-specific time, memory and ratio tradeoff. Equal numbers across codecs have no common meaning.
- A **compression dictionary** is shared context used to improve short or patterned inputs; the decoder needs the exact compatible dictionary.
- **Compression ratio** is uncompressed bytes divided by compressed bytes. **Space saving** is one minus compressed/uncompressed size.
- **Splittability** is the ability to locate independent decode boundaries for parallel or partial reads using an enclosing index or framed structure.
- A **checksum** detects some accidental corruption; an authenticated construction is required for adversarial integrity.
- **Decompression amplification** is the ratio of decoded output or allocated work to compressed input and must be bounded.
- **Corpus** is the governed representative set used to evaluate codecs, encodings, parameters and workload behavior.

### Central model, mechanism, or theorem

For typed input $X$, choose value encoding $E$, compression configuration $Z$, block plan $K$ and envelope $F$:

$$
b=frame_F(compress_{Z,K}(encode_E(X))).
$$

Correctness requires inverse recovery plus schema/domain invariants. Selection minimizes a workload-relative cost, not compressed size alone:

$$
J=w_sB_c+w_nT_{net}+w_wT_{enc}+w_rT_{dec}+w_mM_{peak}+w_lL_{tail}+w_oO,
$$

subject to exact recovery, consumer support, latency objectives, random/parallel access, bounded amplification, dictionary availability, and failure isolation. A codec “wins” only for a declared corpus, hardware, implementation, concurrency and access pattern.

### Critical invariants

- `decode_E(decompress_Z(unframe_F(b)))` recovers values exactly under the declared schema and equivalence.
- Format/envelope names are exact: raw DEFLATE, zlib, gzip, raw LZ4 blocks and LZ4 frames are not interchangeable.
- Every decoder supports the emitted codec, frame flags, encoding, level-independent features and dictionary identity.
- Chunk/block boundaries preserve records or carry enough framing/index metadata to reconstruct them.
- Declared compressed/uncompressed sizes, windows, blocks, dictionaries, nesting and total output obey limits before allocation.
- Checksums are verified where required but never misrepresented as authentication.
- Dictionaries are versioned, authenticated, retained and distributed for as long as encoded data.
- Benchmarks include encode/decode CPU, end-to-end bytes, peak memory, concurrency and tail latency on representative data.
- Secrets are not compressed in a context where attacker-controlled input and observable lengths create a confidentiality oracle.
- Adaptive choices remain explicit in metadata and never emit a representation a required reader cannot decode.

### Common failures

Calling serialization “compression”; calling dictionary value encoding a codec dictionary; applying generic compression before structural encoding; comparing only file size; using synthetic repeated text as the only corpus; reporting throughput without hardware or concurrency; measuring warm-cache decompression but cold production reads; assuming gzip means raw DEFLATE; using raw blocks without lengths/checksums; expecting one frame to provide random access; compressing tiny messages with more header than savings; using one huge block that defeats recovery and pruning; forgetting dictionary distribution; retraining dictionaries without preserving old versions; double-compressing already compressed media; trusting advertised output sizes; disabling checksums without alternative integrity; and compressing secrets beside attacker-controlled guesses.

### Compact example

One million source bytes compress to 250,000, giving ratio 4.0 and 75% saving. At 5 MB/s transport, raw transfer takes 0.20 seconds. If compression takes 0.04 seconds, compressed transfer 0.05 and decompression 0.01, the compressed path takes 0.10 seconds and wins for that path. At a 1 GB/s local-memory boundary the same codec may lose. The decision also tests peak memory, tail latency, frame overhead, decode support, corrupted blocks and limits. Separately, sorted integers use delta/bit packing before page compression, while repeated strings may use dictionary indices; those type-aware encodings change the codec's input.

### Connections

[DE-006](006-parquet-and-columnar-files.md) applies encodings and codecs per page. [DE-005](005-arrow-and-in-memory-columnar-representation.md) shows when compressed storage must materialize into in-memory buffers. Network content coding connects to [Network Engineering](../../24-network-engineering/ROADMAP.md); resource and oracle threats connect to [Security Engineering](../../25-security-engineering/ROADMAP.md).

## Governing Question

Which transformation reduces total system cost for the actual data and workload while retaining exact, safe and supported recovery?

Data systems use multiple layers that are casually called “encoding.” A Protobuf varint represents an integer; Parquet dictionary encoding replaces values with indices; UTF-8 represents characters; gzip compresses bytes; base64 expands bytes into text-safe symbols; TLS encrypts records. Their purposes and reversibility conditions differ.

Choose type-aware representation first, then generic compression, then framing and integrity appropriate to the boundary. Compression observes bytes, not domain values. A sorted integer delta stream gives a codec different redundancy than little-endian integers; dictionary indices differ from repeated strings.

Primary specifications matter because similar names identify different formats. [RFC 1951](https://www.rfc-editor.org/rfc/rfc1951.html) defines DEFLATE, [RFC 1952](https://www.rfc-editor.org/rfc/rfc1952.html) defines gzip wrapping, and HTTP `deflate` means the zlib format containing a DEFLATE stream under [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html). Interoperability depends on the exact layer.

## Why This Matters

Storage and network bytes cost money and time, but compression consumes CPU, memory and latency. Decompression often sits on the read-critical path and may run many more times than compression. An archival write-once/read-rarely corpus can justify expensive compression; a hot stream with strict latency may prefer a fast decoder and modest ratio.

Data shape dominates. Repetitive categorical fields, sorted counters, JSON keys, floating-point streams, encrypted blobs and high-entropy media respond differently. Small messages can grow because frames, checksums and dictionary IDs have fixed overhead.

Block structure controls access. One monolithic compressed stream is sequential even if its codec supports streaming. A columnar file with independent compressed pages and footer offsets supports selective reads. Independently compressed Kafka records allow random consumption but lose cross-record redundancy.

Failure containment matters. A corrupted dependent stream may invalidate everything after the error; independent blocks limit damage but reduce shared history. Checksums detect some corruption, while authenticated encryption provides stronger tamper evidence.

Decompression is an input-amplification boundary. A few bytes can expand into enormous output or trigger large windows, dictionaries and allocation. Nested archives multiply amplification. Limits must be enforced on cumulative decoded bytes and work, not only compressed input.

Compression can also leak secrets. If attacker-controlled guesses share compression context with secrets and the attacker can observe encoded length, ratio differences can reveal information. Disabling transport compression blindly is not the only design, but secret and attacker data must be separated with threat-model evidence.

## Prerequisites and Retrieval

Retrieve representative raw and already encoded bytes; schema, grain, ordering and value distributions; null rate, cardinality, runs, deltas and entropy indicators; current and future readers/writers; supported codecs, versions and frame profiles; compression levels and advanced parameters; block/window sizes; dictionary training corpus, ID, digest and retention; envelopes and content-type/content-encoding metadata; checksum/authentication settings; source and target byte counts; read/write frequency; projection, random-access and replay patterns; storage/network bandwidth and pricing; CPU architecture, cores and contention; memory pools and limits; concurrency and tail-latency objectives; corruption/recovery policy; maximum compressed and decoded sizes; nested archive policy; secret classification; attacker-controlled inputs; cache behavior; and observability for ratio, latency, failures and amplification.

Distinguish encoding from compression; compression from encryption; lossless from lossy transformation; physical codec from file extension; raw algorithm block from self-describing frame; DEFLATE from zlib and gzip; Snappy raw from Snappy framed; LZ4 block from LZ4 frame and Parquet `LZ4_RAW`; codec dictionary from value dictionary; block size from window size; frame concatenation from random access; compressed size from total object/envelope size; ratio from saving percentage; throughput from tail latency; encoder speed from decoder speed; single-thread from aggregate concurrency; warm cache from cold reads; checksum from authenticated integrity; bomb prevention from ordinary decompression errors; and empirical winner from universal recommendation.

## Learning Objectives

After completing this module, you should be able to:

1. separate value encoding, compression, framing, integrity and encryption layers;
2. compute compression ratio, saving, transfer time and end-to-end break-even;
3. compare gzip/DEFLATE, Snappy, LZ4, Zstandard and Brotli by measured workload;
4. select dictionary, delta, run-length, bit-pack and byte-stream encodings by value shape;
5. design blocks and frames for streaming, splitting, recovery and random access;
6. train, identify, distribute, rotate and retire compression dictionaries safely;
7. benchmark representative corpora with reproducible hardware and concurrency evidence;
8. bound output, windows, allocation, nesting and decompression work;
9. distinguish checksums from authentication and analyze compression side channels; and
10. roll out codec/profile changes across heterogeneous readers with rollback.

## Core Exposition

### Name every transformation layer

A typical path can be `domain values → type encoding → page/block compression → file framing → encryption → transport encoding`. Reverse in the required order.

Record each layer in metadata or an external contract. A decoder cannot infer whether bytes are gzip, zlib or raw DEFLATE merely because one library accepts multiple modes.

Avoid redundant layers. Compressing a Parquet file again as one gzip stream often destroys selective range access and yields little extra saving.

### Start with type-aware encodings

Value encodings exploit semantics a generic codec cannot see directly. Delta encoding replaces correlated numbers with smaller differences. Run-length encoding represents repeated runs. Bit packing uses only the required bits. Dictionary encoding replaces repeated values with compact indices.

They are reversible representations under a schema. Apply them before generic compression so repeated patterns become easier for the codec.

Measure decode cost and fallback behavior, not just encoded size.

### Use plain encoding as a baseline

Plain fixed-width values are simple, broadly supported and predictable. They can outperform elaborate encodings on high-entropy or tiny blocks.

A baseline exposes whether a chosen optimization truly helps. Compare plain uncompressed, plain compressed, specialized encoding uncompressed and specialized encoding compressed.

Do not assume “more layers” means smaller or faster.

### Apply run-length encoding to runs

RLE represents a repeated value and run length. It works well for long homogeneous sequences such as null levels, Boolean flags or sorted categories.

Alternating values add overhead. Cap run lengths and validate cumulative decoded count before expansion.

Hybrid RLE/bit-packing can handle mixtures, but the exact format matters for interoperability.

### Apply delta encoding to correlation

For ordered values $x_i$, store initial $x_0$ and differences $d_i=x_i-x_{i-1}$. Slowly changing counters and timestamps may yield small deltas.

Signed deltas often use ZigZag plus variable or bit-packed representation. Validate arithmetic overflow and exact reconstruction.

Randomly ordered identifiers can make deltas large; sorting may improve compression but changes write cost and access behavior.

### Use bit packing for bounded integers

If unsigned values lie in `[0,m]`, `ceil(log2(m+1))` bits suffice per value. Frame metadata must preserve bit width and count.

Bit packing saves space but adds extraction work and boundary complexity. SIMD-aware implementations can offset this; measure the actual reader.

Validate padding and prevent over-read at the final partial word.

### Use value dictionaries carefully

Dictionary encoding stores distinct values once and replaces occurrences with indices. It benefits low-cardinality repeated strings or larger values.

High cardinality grows the dictionary and index width; builders may fall back to plain. The dictionary is scoped to a file chunk, batch or protocol context as defined.

Do not confuse this with a codec dictionary trained from byte substrings.

### Understand generic dictionary compression

Some codecs accept a shared dictionary containing representative byte patterns. It can substantially help many small records where each input lacks enough history.

The dictionary is an external dependency unless embedded. Its ID alone does not distribute or authenticate it; RFC 8878 explicitly leaves Zstandard dictionary retrieval out of band.

Version and retain exact bytes/digest. A wrong dictionary must fail, never silently decode plausible content.

### Understand DEFLATE, zlib and gzip

DEFLATE combines LZ-style backreferences with Huffman coding in a compressed data format. The zlib wrapper adds its header/trailer semantics; gzip adds a file/member wrapper and metadata/checksum.

Names are not interchangeable. HTTP `Content-Encoding: deflate` specifies zlib-wrapped DEFLATE, while `gzip` specifies gzip coding.

Gzip has broad interoperability but benchmark its encoder CPU, decoder behavior and member support for the exact platform.

### Understand Snappy profiles

Snappy targets fast compression/decompression rather than maximum density. The core compressed format and optional framing format are distinct.

The official [framing specification](https://github.com/google/snappy/blob/main/framing_format.txt) adds chunks, a stream identifier and checksums for streaming. Parquet's SNAPPY codec applies the relevant raw page codec under its own page framing.

Record which profile is used; `.snappy` does not resolve ambiguity.

### Understand LZ4 blocks and frames

The LZ4 block format contains compressed sequences but does not supply all self-contained framing metadata. The [LZ4 frame format](https://github.com/lz4/lz4/blob/dev/doc/lz4_Frame_format.md) adds magic, descriptor, blocks, end mark and optional checksums.

Independent blocks improve recovery and parallelism; linked blocks can exploit prior history. The frame itself does not provide general random access without an external index.

Parquet's deprecated `LZ4` codec and interoperable `LZ4_RAW` are distinct; follow the Parquet specification.

### Understand Zstandard

[RFC 8878](https://www.rfc-editor.org/rfc/rfc8878.html) defines lossless Zstandard frames, independent concatenated frames, skippable frames, optional checksums and dictionaries.

Zstandard offers a wide parameter/level space and a reference benchmark tool. Higher level generally trades more compression effort/memory for density, but progress is content-dependent rather than smooth or universal.

Pin profiles required by readers and benchmark dictionary/no-dictionary cases on current data.

### Understand Brotli

[RFC 7932](https://www.rfc-editor.org/rfc/rfc7932.html) defines the Brotli compressed format. It is common in web content coding and available in Parquet ecosystems.

It may suit static content where compression effort can be amortized, but that is a hypothesis to benchmark against required codecs, levels and implementations.

Do not use browser support as evidence that every data engine supports Brotli pages.

### Use container-native compression

Formats such as Parquet compress individual pages/blocks and store uncompressed/compressed sizes in surrounding metadata. This preserves column projection and bounded units.

The current [Parquet compression specification](https://parquet.apache.org/docs/file-format/data-pages/compression/) defines supported codec profiles, including deprecated versus interoperable LZ4 variants.

Prefer the container's native units over wrapping the entire container unless the outer boundary has a justified purpose.

### Choose block boundaries deliberately

Larger blocks give the codec more history and amortize headers, often improving ratio. Smaller independent blocks bound latency, memory, corruption radius and selective reads.

Block size interacts with record framing. Never split a logical record unless the enclosing format can reconstruct it exactly.

Set both compressed and decoded byte caps per block plus cumulative caps per object/request.

### Separate block size and window size

Block size is a container or codec unit; window size controls how far backward matches can refer. They may be coupled but are not synonyms.

A decoder may need memory proportional to advertised window even before producing much output. Enforce a maximum supported window.

Large history can improve ratio while harming concurrency and random restart.

### Design for splitting and random access

A sequential compressed stream is not automatically splittable. Parallel readers need known independent frame/block boundaries and decoded position metadata.

Files such as Parquet provide indexes to compressed pages. Seekable variants or external indexes can map uncompressed ranges to frames.

Test arbitrary partition starts and corrupted prior blocks. Do not scan from byte zero and call it random access.

### Handle concatenated frames or members

Specifications can permit concatenated gzip members, Zstandard frames or LZ4 frames. Some APIs stop after the first member unless configured otherwise.

Test the actual reader with empty, multiple and trailing frames. Decide whether unknown/skippable metadata is accepted and bounded.

Reconcile total decoded size and member count to prevent hidden trailing content.

### Compute ratio and saving consistently

Let uncompressed size be $U$ and compressed size including required frame overhead be $C$. Ratio is $R=U/C$; saving is $1-C/U$.

Some tools report the inverse. Always publish raw byte counts and formula. Include dictionaries, indexes and envelopes when they are part of deployed cost.

For incompressible input, $C$ can exceed $U$.

### Model end-to-end break-even

Raw path time approximates $U/b$, where $b$ is effective bandwidth. Compressed path includes encode $T_e$, transfer $C/b$ and decode $T_d$, plus queueing and allocation.

Compression helps latency when $T_e+T_d<(U-C)/b$ under the measured path. Cached reads, distributed fan-out and read frequency alter the equation.

Tail latency and throughput under concurrency matter more than isolated mean time.

### Build representative corpora

Sample each schema, partition, producer, season and size distribution. Include already compressed/encrypted fields, null patterns, outliers, small messages and evolution versions.

Split training and evaluation data for codec dictionaries. Prevent leakage from evaluating on the exact samples used to train.

Retain immutable corpus digests and privacy controls so results are reproducible.

### Benchmark reproducibly

Record codec/library version, format/profile, parameters, dictionary digest, block size, CPU, memory, operating system, threading, warmup, repetitions and cache state.

Measure compressed bytes, encode/decode throughput, CPU time, allocations, peak memory and latency percentiles. Validate decoded digests every run.

Benchmark the enclosing application path, not only an in-memory CLI loop.

### Weight reads and writes correctly

If data is written once and read one thousand times, decoder cost dominates total compute. If intermediate spill data is written/read once, balanced encode/decode speed may dominate.

Multiply per-operation costs by expected frequency, replicas, downstream fan-out and retention. Include recompression during compaction.

Plan for peak concurrent decoders, not only aggregate daily CPU.

### Govern adaptive compression

Writers can sample a block and store it uncompressed when compression expands it, or choose among supported codecs by column/type.

Every choice must be explicit in metadata and supported by all readers. Adaptation complicates observability, reproducibility and capacity prediction.

Use bounded deterministic policy versions rather than unconstrained per-record experimentation.

### Detect already compressed or encrypted input

JPEG, video, encrypted ciphertext and compressed archives often have high entropy to a generic codec. Recompressing can waste CPU and expand bytes.

Use declared media/schema knowledge first; magic sniffing alone is not trustworthy. Sample compression can inform a bounded store-uncompressed decision.

Never skip validation simply because content seems incompressible.

### Bound decompression amplification

Before decode, cap compressed input, advertised output/window/block sizes, dictionary bytes, nested layers and concurrent memory. During decode, enforce cumulative output and CPU/deadline budgets.

Stream to bounded consumers rather than allocating an advertised whole result when possible. Abort deterministically and quarantine evidence.

Archive extraction also needs file-count, path and recursion controls beyond the codec.

### Treat checksums correctly

Frame or block checksums detect many accidental storage/transport corruptions. Verify them before accepting decoded output when the profile carries them.

Checksums are unkeyed; an attacker can replace content and recompute one. Authenticated encryption or a trusted MAC/signature is required for adversarial integrity.

Record whether a checksum covers compressed bytes, decoded content, header or only some pieces.

### Separate compression and encryption

Compress before encryption because sound ciphertext should not expose exploitable redundancy. Encryption after compression changes integrity and framing responsibilities.

Never decrypt unauthenticated bytes and then allow unbounded decompression. Verify the authenticated envelope according to protocol design.

Do not assume storage-provider encryption determines page-level compression choices.

### Analyze compression side channels

If a secret and attacker-controlled guess share compression context, matching substrings can shorten output. Observable length across adaptive requests can become an oracle.

Separate secrets from attacker-controlled content, disable shared compression contexts, add protocol defenses supported by a threat analysis, and limit repeated observations.

Random padding alone is not automatically sufficient; validate the complete attack surface.

### Roll out codec changes safely

Inventory every reader, including old recovery jobs and external partners. Write canary data with the new exact profile and exercise oldest supported readers.

Deploy readers before writers when introducing a forward-incompatible codec/encoding. Retain a rollback writer profile and do not rewrite archives until proven.

Observe unknown-codec failures, ratio, CPU, latency and memory after rollout.

### Observe production behavior

Record raw and compressed bytes, ratio distribution, frame/block sizes, codec/profile/level, dictionary ID, encode/decode CPU, latency, peak memory, checksum failures and output-limit rejections.

Segment by schema and producer. A global average hides columns or tenants that expand.

Alert on ratio drift, dictionary decay, decoder-version skew, increased tail latency, malformed frames and unexpected nested compression.

## Definitions and Notation

Let typed data $X$ encode to $Y=encode_E(X)$ with size $U=|Y|$. Compression and framing produce $b=frame_F(compress_{Z,K}(Y))$ with deployed size $C=|b|$. Correct recovery requires

$$
decode_E(decompress_{Z,K}(unframe_F(b)))\equiv_S X.
$$

Compression ratio $R=U/C$. Fraction saved $s=1-C/U$ for $U>0$. Report $U$, $C$, envelope/dictionary inclusion and formulas because “4× compression” and “75% smaller” describe the same example while inverse conventions can confuse.

For bandwidth $q$ bytes/second, raw transfer time is $U/q$. Compressed-path idealized time is $T_e+C/q+T_d$. Compression reduces this latency only if

$$
T_e+T_d<(U-C)/q.
$$

Add queueing, I/O requests, allocation and concurrency for a production model.

For delta encoding $d_0=x_0$ and $d_i=x_i-x_{i-1}$ for $i>0$. Reconstruction uses $x_0=d_0$ and $x_i=x_{i-1}+d_i$, with checked arithmetic. ZigZag maps signed $n$ to $2n$ for nonnegative and $-2n-1$ for negative.

Let amplification $A=O/I$ for decoded output $O$ and compressed input $I>0$. Resource policy also caps absolute output, window/dictionary memory, nested product amplification, CPU/deadline and concurrent decoders; ratio alone is insufficient for tiny inputs or metadata bombs.

## Mechanisms, Invariants, or Proof Structure

### Sixteen-step encoding and compression mechanism

1. Define values, schema, exact-recovery equivalence and access workload.
2. Inventory every writer/reader and its supported representation profiles.
3. Build immutable representative training and evaluation corpora.
4. Establish plain/uncompressed correctness and cost baselines.
5. Evaluate type-aware encodings against value shape.
6. Evaluate codec, level, block/window and dictionary combinations.
7. Include all frame, index and dictionary bytes in size accounting.
8. Validate decoded values/digests for every benchmark run.
9. Measure encode/decode CPU, latency percentiles, allocations and peak memory.
10. Test splitting, partial reads, concatenation, corruption and restart.
11. Enforce compressed/output/window/dictionary/nesting/concurrency limits.
12. Verify checksum coverage and threat-appropriate authentication.
13. Review secret/attacker co-compression and observable-length channels.
14. Deploy compatible readers before new writers and retain rollback.
15. Observe ratios, dictionary drift, failures, memory and tails by schema.
16. Rebenchmark when corpus, hardware, implementation or access patterns change.

### Exact-recovery invariant

Unframing, decompression and value decoding reproduce the declared values and null/ordering/schema distinctions for every accepted block.

### Profile invariant

Codec, raw/wrapped format, flags, block dependency, level-independent features and dictionary identity are explicit and supported by every required decoder.

### Boundary invariant

Blocks/frames align with enclosing record or carry enough length/index metadata to reconstruct exact boundaries and resume safely.

### Resource invariant

Compressed bytes, output, windows, dictionaries, nested layers, allocations, time and concurrent work remain within enforced limits throughout decoding.

### Integrity invariant

All required checksums are verified, and adversarial integrity relies on authenticated mechanisms rather than unkeyed checksums.

### Benchmark invariant

Every comparative claim names corpus, byte accounting, implementation, parameters, hardware, concurrency, repetitions and correctness verification.

### Dictionary invariant

Every dictionary-compressed object references exact authenticated dictionary bytes retained and available through the object's lifetime.

### Confidentiality invariant

Secrets never share an observable adaptive compression context with attacker-controlled guesses without a reviewed and tested mitigation.

### Proof sketch: the best ratio need not minimize transfer latency

Consider codecs A and B on input size $U$ and bandwidth $q$. A yields smaller $C_A<C_B$ but has encode/decode cost $T_A$; B costs $T_B$. Compressed latency is $L=C/q+T$. If $T_A-T_B>(C_B-C_A)/q$, then $L_A>L_B$ despite A's better ratio. Thus ordering codecs by compressed size does not determine latency ordering. The same counterexample extends to total cost with memory, concurrency and reads.

### Executable decision audit

The synthetic model checks RLE and delta/ZigZag recovery, then recomputes size saving and an idealized network break-even. It is an arithmetic fixture, not a codec benchmark.

<!-- bijux-verify: {"id":"compression-decision-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"runs=(('A', 3), ('B', 2), ('C', 1))\nrle_round_trip=True\ndeltas=(100, 1, 1, 0, 0, 8)\nzigzag=(200, 2, 2, 0, 0, 16)\nbytes_saved=750000 saving=75.0% ratio=4.0\nraw_seconds=0.200 compressed_path_seconds=0.100\ncompression_wins=True\n","stderr":""}} -->
```python
def run_length_encode(values):
    runs = []
    for value in values:
        if runs and runs[-1][0] == value:
            runs[-1] = (value, runs[-1][1] + 1)
        else:
            runs.append((value, 1))
    return tuple(runs)


def run_length_decode(runs):
    return tuple(value for value, count in runs for _ in range(count))


labels = ("A", "A", "A", "B", "B", "C")
runs = run_length_encode(labels)
values = (100, 101, 102, 102, 102, 110)
deltas = (values[0],) + tuple(values[index] - values[index - 1] for index in range(1, len(values)))
zigzag = tuple(delta * 2 if delta >= 0 else -delta * 2 - 1 for delta in deltas)

uncompressed, compressed = 1_000_000, 250_000
bandwidth = 5_000_000
encode_seconds, decode_seconds = 0.04, 0.01
raw_seconds = uncompressed / bandwidth
compressed_seconds = encode_seconds + compressed / bandwidth + decode_seconds

print(f"runs={runs}")
print(f"rle_round_trip={run_length_decode(runs) == labels}")
print(f"deltas={deltas}")
print(f"zigzag={zigzag}")
print(f"bytes_saved={uncompressed - compressed} saving={(1 - compressed / uncompressed) * 100:.1f}% ratio={uncompressed / compressed:.1f}")
print(f"raw_seconds={raw_seconds:.3f} compressed_path_seconds={compressed_seconds:.3f}")
print(f"compression_wins={compressed_seconds < raw_seconds}")
```

### Verification strategy

Round-trip every value/null/order boundary; compare plain and specialized encodings; use training/evaluation separation; include tiny, incompressible, already compressed, skewed and evolving samples; benchmark all supported codec profiles/levels with full envelope and dictionary bytes; verify decoded digests; repeat cold/warm and single/concurrent runs; record CPU, allocations, memory and percentiles; vary blocks/windows; begin decode at every advertised split; concatenate frames/members; truncate and flip header/body/checksum bits; substitute/miss dictionaries; declare huge windows/outputs; nest compressed inputs; enforce deadlines; compare checksums with authenticated corruption tests; exercise secret/guess length observations; test oldest readers; canary rollout/rollback; and remeasure production drift.

## Alternatives and Trade-Offs

- **Plain versus specialized encoding:** plain is simple and universal; specialized encodings exploit runs, deltas, bounds or cardinality with extra metadata and decode work.
- **RLE versus bit packing:** RLE favors long repeats; bit packing favors bounded values without long runs.
- **Delta versus original values:** delta favors correlated order; original values avoid dependency and overflow concerns.
- **Value dictionary versus plain strings:** dictionaries favor repeated vocabulary; high cardinality expands dictionary and indices.
- **Codec dictionary versus no dictionary:** a trained dictionary helps small patterned inputs; it adds lifecycle, memory and availability dependencies.
- **Raw block versus framed format:** raw blocks minimize overhead inside a container; frames provide self-description, boundaries and optional integrity.
- **Gzip versus faster codecs:** gzip maximizes broad legacy support; Snappy/LZ4/Zstd may reduce CPU or bytes depending on workload and readers.
- **LZ4 versus Snappy:** both target speed-oriented use cases; exact implementations, frames, ratios and hardware decide.
- **Zstd versus Brotli:** both offer denser options; supported levels, dictionaries, decode path and ecosystem decide rather than brand.
- **Low versus high compression level:** low levels reduce write CPU/memory; high levels may save more bytes for archival or repeated reads.
- **Small versus large blocks:** small blocks bound latency/corruption and aid selective access; large blocks amortize headers and share more history.
- **Independent versus linked blocks:** independent blocks enable restart/parallelism; linked history may improve ratio.
- **Per-record versus batch compression:** records isolate failures/random access; batches exploit cross-record redundancy and amortize frames.
- **Container-native versus whole-file compression:** native blocks preserve projection/splitting; whole-file wrappers are simple but often serialize access.
- **Static versus adaptive codec:** static policy is predictable; adaptive policy avoids expansion but complicates metadata and operations.
- **Checksum versus no checksum:** checksum detects accidental corruption at byte/CPU cost; omitting it requires other integrity evidence.
- **Checksum versus authenticated encryption:** checksum is unkeyed detection; AEAD adds confidentiality/integrity and key/nonce obligations.
- **Compression before encryption versus none:** pre-encryption compression saves redundancy; secret-mixing and length oracles may require separation/disablement.
- **Warm-cache versus cold-path tuning:** warm runs expose decoder compute; cold runs include storage/network and may change the winner.
- **Best mean versus best tail:** mean throughput favors aggregate efficiency; tail objectives penalize large blocks, queues and variable work.

## Failure Modes and Misconceptions

1. “Encoding means compression” conflates representation and redundancy removal.
2. “Compression means encryption” provides no confidentiality.
3. “Lossless means semantically correct” only proves byte recovery under the codec.
4. “gzip and DEFLATE are identical” ignores wrappers.
5. “HTTP deflate is raw DEFLATE” conflicts with HTTP's zlib coding definition.
6. “Snappy raw and framed are interchangeable” ignores chunk framing/checksums.
7. “LZ4 blocks identify their own output size” omits external framing metadata.
8. “Parquet LZ4 names are equivalent” ignores deprecated versus `LZ4_RAW` profiles.
9. “A file extension selects the decoder” trusts naming over contract/magic.
10. “Higher level always compresses proportionally better” ignores content and parameter behavior.
11. “Level 6 means the same across codecs” compares unrelated scales.
12. “Best ratio is best codec” ignores CPU, memory, latency and access.
13. “Fast encoder implies fast decoder” assumes coupled performance.
14. “One benchmark corpus represents production” ignores schema and seasonal diversity.
15. “Repeated lorem ipsum is realistic” biases toward artificial redundancy.
16. “In-memory CLI throughput is end-to-end latency” omits I/O, allocation and queues.
17. “Warm caches represent cold object reads” changes the tested system.
18. “Compressed size excludes frame/dictionary” undercounts deployed bytes.
19. “4× smaller means 400% saving” confuses ratio and percentage.
20. “Compression always shrinks” ignores incompressible input and headers.
21. “Already compressed media benefits again” often wastes CPU or expands.
22. “Dictionary encoding and codec dictionaries are the same” confuses value IDs and byte history.
23. “Dictionary ID retrieves a dictionary” omits distribution and namespace.
24. “Retraining can replace old dictionary bytes” breaks retained data.
25. “A large block is always denser” ignores data changes and capped windows.
26. “Streaming means random access” confuses incremental decode with seekability.
27. “Concatenated frames are universally consumed” ignores API behavior.
28. “Splitting at arbitrary compressed offsets works” ignores frame dependencies.
29. “Checksum authenticates content” ignores attacker recomputation.
30. “Checksum always covers headers” depends on exact frame.
31. “Compressed input size bounds output” enables amplification attacks.
32. “Advertised output size is safe to allocate” trusts hostile metadata.
33. “Per-block limit prevents nested bombs” ignores cumulative/product limits.
34. “Timeout alone bounds memory” allocation may occur first.
35. “Encryption makes compression unnecessary” ciphertext placement occurs after compression choice.
36. “Compressing secrets is always harmless” ignores observable-length oracles.
37. “Random padding automatically fixes leakage” may average out under repeated queries.
38. “Adaptive codec choice needs no metadata” makes decoding ambiguous.
39. “Every reader supports a newly listed codec” ignores versions and feature matrices.
40. “Canary decode proves archives can migrate” omits old data shapes and recovery readers.
41. “Global average ratio detects regressions” hides schema/tenant expansion.
42. “Successful decompression proves complete input” can ignore trailing members/content.

## Worked Examples

### Example 1

A local shuffle runs over 40 GB/s memory bandwidth. Zstd saves bytes but its CPU makes the stage slower; LZ4 or no compression wins. The same data crossing a 200 MB/s network selects Zstd. Both results are correct for their named paths.

### Example 2

Sorted millisecond timestamps have small deltas. Delta encoding plus bit packing shrinks the intermediate representation before Zstd. Randomly permuting rows erases this benefit, demonstrating that order and access design affect compression.

### Example 3

Ten thousand short JSON events share keys but are compressed independently. A trained Zstd dictionary improves size. The pipeline embeds dictionary ID plus authenticated digest, distributes exact bytes before writer rollout and retains every version through event expiration.

### Example 4

High-cardinality encrypted payload fields expand under page compression while status fields compress well. Column-specific Parquet metrics lead to disabling compression for ciphertext and retaining a fast codec for other columns.

### Example 5

A producer labels data `deflate` but emits raw RFC 1951 streams. HTTP clients expect RFC 9110's zlib wrapper and fail. The producer changes the content coding or adds the correct wrapper after dual-client conformance tests.

### Example 6

One giant gzip member wraps a 500 GB CSV. Parallel consumers must decode from the start. A migration creates independently framed, indexed, record-aligned objects; count/digest reconciliation proves the new splits preserve logical records.

### Example 7

A 2 KB API response becomes 2.1 KB after frame/header overhead and consumes 2 ms CPU. Adaptive policy stores it uncompressed under an explicit envelope flag. Larger repetitive responses remain compressed.

### Example 8

A 10 KB archive expands to 50 GB across nested members. The ingress service enforces per-layer and cumulative output, entry count, depth, path and CPU limits, aborts before disk exhaustion and quarantines the source digest.

### Example 9

A response compresses a CSRF token beside an attacker-reflected parameter, and response length is observable. The design separates the secret from compressed attacker content and validates that repeated guesses no longer change secret-dependent length.

### Example 10

A new Zstd level/dictionary lowers average size 12% but raises p99 decode memory under 200 concurrent readers beyond the service limit. A lower level or smaller window wins the constrained objective despite a weaker ratio.

## Cross-Program Connections

**Information Theory:** entropy and redundancy bound what lossless compression can exploit, while real codecs trade optimality for compute and memory.

**Algorithms:** Huffman codes, Lempel–Ziv matches, RLE, delta, bit packing and dictionary lookup are distinct composable algorithms.

**Computer Architecture:** memory bandwidth, cache, SIMD, branches and cores determine codec throughput beyond asymptotic analysis.

**Network Engineering:** bandwidth, content negotiation, framing, partial transfer and latency influence break-even decisions.

**Operating Systems:** page cache, memory mapping, pipes, file descriptors and process limits affect benchmark and production behavior.

**Security Engineering:** decompression amplification, parser defects, checksum/authentication distinctions and length oracles require threat models.

**Distributed Systems:** codec rollouts must accommodate version skew, replay, retries, recovery readers and heterogeneous workers.

**Performance Engineering:** representative corpora, controlled experiments, percentiles and end-to-end resource accounting turn preferences into evidence.

## References

1. IETF, [RFC 1951: DEFLATE Compressed Data Format](https://www.rfc-editor.org/rfc/rfc1951.html), 1996.
2. IETF, [RFC 1952: GZIP File Format](https://www.rfc-editor.org/rfc/rfc1952.html), 1996.
3. IETF, [RFC 8878: Zstandard Compression Format](https://www.rfc-editor.org/rfc/rfc8878.html), 2021.
4. IETF, [RFC 7932: Brotli Compressed Data Format](https://www.rfc-editor.org/rfc/rfc7932.html), 2016.
5. IETF, [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html), 2022.
6. Google, [Snappy Compressed Format](https://github.com/google/snappy/blob/main/format_description.txt), current specification.
7. Google, [Snappy Framing Format](https://github.com/google/snappy/blob/main/framing_format.txt), current specification.
8. LZ4 Project, [LZ4 Block Format](https://github.com/lz4/lz4/blob/dev/doc/lz4_Block_format.md), current specification.
9. LZ4 Project, [LZ4 Frame Format](https://github.com/lz4/lz4/blob/dev/doc/lz4_Frame_format.md), version 1.6.4.
10. Zstandard Project, [Reference Implementation](https://github.com/facebook/zstd), current project repository.
11. Zstandard Project, [CLI and Benchmark Manual](https://github.com/facebook/zstd/blob/dev/programs/zstd.1.md), current documentation.
12. Zstandard Project, [Dictionary Builder API Guidance](https://github.com/facebook/zstd/blob/dev/lib/zdict.h), current documentation.
13. Apache Parquet, [Compression](https://parquet.apache.org/docs/file-format/data-pages/compression/), current specification.
14. Apache Parquet, [Encodings](https://parquet.apache.org/docs/file-format/data-pages/encodings/), current specification.
15. Apache Parquet, [Implementation Status](https://parquet.apache.org/docs/file-format/implementationstatus/), current documentation.
16. NIST, [SP 800-38D: Galois/Counter Mode](https://csrc.nist.gov/pubs/sp/800/38/d/final), 2007.

## Exercises

### Exercise 1

Compute ratio, saving and idealized latency for 800 MB input compressed to 200 MB over 100 MB/s bandwidth with 1.5 seconds encode and 0.7 seconds decode. Should compression be selected for this one-way path?

### Exercise 2

For integer sequence `(1000,1001,1003,1003,999)`, compute deltas and ZigZag mappings. State the reconstruction and overflow checks.

### Exercise 3

Design a reproducible comparison of Snappy, LZ4, Zstd and gzip for Parquet pages serving a read-heavy analytical workload.

### Exercise 4

Design a lifecycle for trained dictionaries used by millions of small events across rolling producers, consumers, archives and disaster recovery.

### Exercise 5

Threat-model a service that accepts nested compressed uploads, extracts records and returns a compressed response containing account data plus an attacker-controlled label.

## Answers to the Exercises

### Answer 1

Ratio is `800/200 = 4.0`. Saving is `1-200/800 = 0.75`, or 75%. Raw transfer is `800/100 = 8` seconds. Compressed transfer is 2 seconds; adding 1.5 encode and 0.7 decode gives 4.2 seconds, so idealized saving is 3.8 seconds and compression wins for this one-way scenario.

The decision is incomplete until sizes include frame/dictionary overhead and measurements include contention, allocations, p99, implementation support and whether data is encoded once/read many times. At bandwidth above `(800-200)/(1.5+0.7) ≈ 272.7 MB/s`, the simple transfer inequality reverses.

### Answer 2

Using the first value as initial delta, deltas are `(1000,1,2,0,-4)`. ZigZag gives `(2000,2,4,0,7)`: nonnegative maps to twice itself, while `-4` maps to `8-1=7`.

Reconstruct `x_0=d_0`; then cumulative addition yields 1001, 1003, 1003 and 999. Encoding and decoding must use a declared signed width, reject subtraction/addition overflow, validate count and reject truncated variable/bit-packed values. Sorting to improve deltas would need separate row-order preservation.

### Answer 3

Select files/columns spanning cardinality, nulls, sorted deltas, strings, floating values, nested fields, tiny and large pages, already compressed payloads and historical schemas. Freeze training/evaluation inputs by digest. For each reader-supported exact Parquet codec profile, vary meaningful levels and page sizes while holding other settings controlled; include plain/uncompressed baseline.

Measure full file bytes and per-column/page sizes, write CPU/time/memory, cold and warm projected/filter read bytes, decode CPU, p50/p95/p99, peak memory and concurrency scaling. Verify row/value digests and pruning-disabled equality. Record hardware, OS, libraries, threads, caches and repetitions. Weight write once against measured read frequency and choose a Pareto option meeting memory/tail constraints, then canary on oldest readers.

### Answer 4

Train only on privacy-approved representative samples and evaluate on held-out data. Assign each immutable dictionary a scoped ID plus cryptographic digest, schema/corpus/version metadata, codec parameters and creation evidence. Store it in authenticated durable distribution with access control, backup and disaster-recovery replication.

Deploy consumers and caches before producers emit the ID. Payloads carry the exact ID/digest; unknown dictionaries fail/quarantine without fallback. Retain old bytes through the maximum payload/archive/replay/rollback lifetime. Observe ratio drift and retrain to a new ID, never replace existing bytes. Test new/old producer-consumer matrices, missing/corrupt dictionaries, cache eviction and registry outage. Decommission only after authoritative evidence shows no retained references.

### Answer 5

For uploads, cap compressed input, members, entries, nesting, paths, dictionary/window/block sizes, per-layer and cumulative decoded bytes, ratio, CPU/deadline, disk and concurrency. Stream to bounded storage, reject traversal/symlinks, verify checksums/authentication as applicable, patch/isolate decoders and quarantine any partial failure rather than returning incomplete records.

For responses, account data is secret and the label attacker-controlled. Do not place both in a shared adaptive compression context whose length the attacker can repeatedly observe. Separate response components/contexts or disable compression for the secret-bearing response under a reviewed protocol; rate/authorization controls supplement but do not replace separation. Encrypt with authenticated transport, remembering TLS does not hide total ciphertext length. Test repeated guesses and variable padding statistically rather than assuming padding cures the oracle.
