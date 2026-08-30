---
module_id: DSE-077
program: Data Structures Engineering
level: 2
module_number: 77
title: SSTables and Sorted Runs
status: complete
last_verified: 2026-08-30
---

# SSTables and Sorted Runs

## One-Page Review

### Governing question

How should an immutable sorted-run format encode, locate, validate, and iterate versioned entries so it remains correct across compression, corruption, format evolution, and LSM publication?

### Essential definitions

- An **SSTable/sorted run** is an immutable file or component set whose internal entries are ordered by the engine's complete comparator.
- An **internal key** combines user key with sequence/version and kind so versions of one user key occur in the resolution order required by reads and compaction.
- A **data block** stores a contiguous key interval and is independently located, decompressed, and integrity-checked.
- **Prefix compression** stores a key as shared-prefix length plus unshared suffix relative to a prior key.
- A **restart point** stores a full key periodically, bounding reconstruction work and enabling binary search among restart intervals.
- A **block handle** records checked offset and encoded length; it is untrusted until bounds and arithmetic are validated against file size and trailer.
- An **index block** maps routing separators to data-block handles; a **metaindex** discovers optional named metadata such as filters.
- A **footer** at a fixed location carries format/magic and top-level handles so a reader can bootstrap from file size.

### Central model, mechanism, or theorem

If internal entries are globally ordered and partitioned into ordered blocks, a two-level index can find a candidate data block in `O(log D + log R + scan_interval)` comparisons for D data blocks and R restart points, subject to the concrete search implementation. A range seek finds the first candidate block, reconstructs from a restart, then iterates entries and subsequent blocks until its endpoint.

Prefix compression reduces repeated-key bytes but creates a dependency chain. Restart interval r bounds sequential reconstruction after a restart to at most roughly r entries; smaller r improves seek/recovery locality but increases full-key and restart-array space. Block size similarly trades index/metadata and compression efficiency against read/decompression amplification, cache granularity, corruption blast radius, and compaction memory.

An SSTable becomes serving state only after all blocks, trailers, footer, checksums, and required durability are complete and its manifest/version edit is installed. File immutability simplifies readers and caching but does not prove correct bytes, comparator compatibility, no stale/misplaced block, or safe deletion.

### Critical invariants

1. Entries are strictly ordered by internal comparator, with a deterministic duplicate/version/kind contract.
2. Each decoded prefix record is valid relative to its predecessor; restart entries have zero shared prefix and offsets/indexes are ordered and in bounds.
3. Data-block intervals are ordered and agree with every index separator and file min/max property.
4. Handles use checked arithmetic and point wholly inside permitted file regions without illegal overlap.
5. Compression type, checksum algorithm/scope, format version, comparator/filter identities, and encryption context are authenticated/validated before use.
6. Point/range iteration returns no entry outside the decoded ordered stream and reports corruption rather than treating it as absence.
7. Only a complete, verified, durable file is manifest-visible; obsolete files remain until all pinned readers/recovery users release them.

### Common failures

- Sorting user keys but not sequence/kind, causing nondeterministic version resolution.
- Trusting restart counts, offsets, shared lengths, varints, decompressed lengths, or handles from disk.
- Seeking directly into a prefix chain rather than reconstructing from a valid restart.
- Using a separator that is below the previous block's last key or above the next block's first key.
- Checking compressed bytes but not decoded length/type/context, or accepting checksum failure as a miss.
- Letting a filter false negative or corrupt index silently skip the data block.
- Changing comparator/normalization while reading old files without versioned compatibility.
- Publishing the filename before footer/checksum/durability, or deleting obsolete input while readers remain.

### Compact example

Keys `apple, application, apricot, banana, band, bandana, carrot` with restart interval three have shared-prefix lengths `0,4,2,0,3,4,0`; restart entries are 0,3,6. Partitioning three entries per block gives first keys `apple,banana,carrot` and right-lower-bound separators `banana,carrot`. Inclusive scan `[apricot,bandana]` returns four keys across the first two blocks.

### Connections

DSE-071 provides page/byte validation, DSE-074 sorted construction/ranges, DSE-076 LSM lifecycle, DSE-078 Bloom filters, and DSE-079 compaction. Database and Data Engineering consume immutable files in local stores, lake tables, stream checkpoints, distributed exchange, backups, and replication.

## Governing Question

How do we refine “sorted immutable file” into a durable binary interface whose readers can prove ordering and integrity without loading the whole run?

## Why This Matters

SSTables sit on the correctness path of every LSM read, flush, compaction, backup, and recovery. They must serve point lookups with a small number of block reads and stream ranges efficiently, while compressing repeated prefixes and values. Immutability allows lock-free sharing, stable cache keys, and checksums; a compactor can construct a new file privately and publish it through a manifest.

Yet immutable corruption is still corruption. One unchecked offset can expose arbitrary memory or create resource exhaustion. One false-negative filter can hide data. A comparator change can make a previously sorted file semantically unordered. A truncated footer can redirect the index. A checksum stored without file/block identity can accept a misplaced block. A repair tool that guesses around bad bytes can emit plausible but wrong records.

The format is therefore a protocol among builder, reader, cache, compactor, manifest, migration tools, and operators. It needs canonical encodings, explicit limits, compatibility identities, independent verification, and failure taxonomy. Performance evidence is secondary to a reader that reliably distinguishes found, absent, corrupt, unsupported, unavailable, and I/O failure.

## Prerequisites and Retrieval

Retrieve:

- total internal-key order, snapshots, tombstones, merge resolution, and range endpoints;
- varints/fixed-width endian encoding, checked arithmetic, prefix compression, checksums, and decompression limits;
- external sorting, block indexes, binary search, iterators, cache keys, and readahead;
- immutable-file publication, manifest generations, file reference pinning, WAL/flush recovery, and safe deletion;
- fuzzing, golden fixtures, property oracles, corruption injection, format migration, and benchmark design.

Diagnostic retrieval: if record says shared length 8 but the previous decoded key has 5 bytes, reject the block. Clamping to 5 changes the key and can break order/routing while hiding corruption.

## Learning Objectives

After this module, you can:

1. specify internal entry, comparator, version/kind, data block, restart, index, metadata, trailer, and footer contracts;
2. encode/decode prefix-compressed blocks with bounded reconstruction and hostile-input validation;
3. derive valid separators and route point/range seeks through index and restart intervals;
4. define checksum, compression, encryption, cache, and file-identity scopes;
5. build, finalize, verify, durably publish, pin, retire, and delete immutable files safely;
6. handle comparator/filter/format evolution, downgrade, migration, repair, and salvage;
7. design property, mutation, fuzz, crash, compatibility, and independent-reader evidence;
8. measure index/filter/cache/block-size/compression effects without confusing speed with correctness.

## Core Exposition

**Freeze comparator identity.** Internal ordering might be `(user_key ascending, sequence descending, kind descending)`. User comparison can include collation, normalization, timestamp encoding, tenant prefix, or custom operator. Store a stable comparator/definition identity in properties/manifest. A reader must reject unsupported identity rather than apply its current default to old bytes.

**Encode canonical entries.** Each record carries shared-key length, unshared length, value length, suffix bytes, and value bytes using bounded canonical integers. Validate integer termination/overflow, length sum, previous-key availability, shared <= previous length, record inside block, key/value maxima, and remaining bytes before allocation/copy. Restart records use shared=0.

**Place restart metadata at block tail.** A data block commonly contains entry stream, fixed-width restart offsets, and restart count. Validate minimum trailer space, count limit, multiplication/addition, monotonically increasing offsets, each offset inside entry region and on an actual record, first restart policy, and zero-shared record at every restart. Do not trust an offset merely because it is in range.

**Search in two stages.** Binary-search restart full keys to choose the last restart whose key is below/equal target under the seek rule, then decode forward until key >= target or interval ends. An index first chooses the candidate data block. Range iteration preserves decoder state across entries, then reads the next indexed block. Reverse iteration usually needs additional restart/backtracking logic; specify it separately.

**Derive safe separators.** Between data blocks with last key a and next first key b, choose separator s satisfying `a <= s < b` or the concrete index convention that routes every target correctly. A shortening routine can emit a compact distinguishing prefix only if comparator semantics prove it. Otherwise store b or a full boundary. Validate the complete ordered block sequence during build and independent audit.

**Model the restart contract.** The following finite model prefix-encodes seven unique strings, resets every three entries, decodes exactly, groups blocks by the same capacity, routes two seeks, and executes a bounded inclusive range.

<!-- bijux-verify: {"id":"sorted-run-restart-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"entries=7\nrestart_interval=3\nrestart_entries=0,3,6\nshared_prefixes=0,4,2,0,3,4,0\ndecoded_keys=apple,application,apricot,banana,band,bandana,carrot\ndata_blocks=apple..apricot|banana..bandana|carrot..carrot\nindex_separators=banana,carrot\nseek_band_block=1\nseek_blueberry_block=1\nrange_apricot_bandana=apricot,banana,band,bandana\nround_trip=True\norder_valid=True\nevidence=sorted_run_restart_model\n","stderr":""}} -->
```python
keys = ["apple", "application", "apricot", "banana", "band", "bandana", "carrot"]
restart_interval = 3


def common_prefix(left, right):
    length = 0
    while length < len(left) and length < len(right) and left[length] == right[length]:
        length += 1
    return length


encoded = []
previous = ""
for index, key in enumerate(keys):
    shared = 0 if index % restart_interval == 0 else common_prefix(previous, key)
    encoded.append((shared, key[shared:]))
    previous = key

decoded = []
previous = ""
for shared, suffix in encoded:
    key = previous[:shared] + suffix
    decoded.append(key)
    previous = key

blocks = [decoded[index:index + restart_interval] for index in range(0, len(decoded), restart_interval)]
separators = [block[0] for block in blocks[1:]]


def block_index(target):
    index = 0
    while index < len(separators) and target >= separators[index]:
        index += 1
    return index


def scan(low, high):
    result = []
    for block in blocks[block_index(low):]:
        for key in block:
            if low <= key <= high:
                result.append(key)
            if key > high:
                return result
    return result


restart_entries = list(range(0, len(keys), restart_interval))
block_ranges = [f"{block[0]}..{block[-1]}" for block in blocks]
print(f"entries={len(keys)}")
print(f"restart_interval={restart_interval}")
print("restart_entries=" + ",".join(str(index) for index in restart_entries))
print("shared_prefixes=" + ",".join(str(shared) for shared, _ in encoded))
print("decoded_keys=" + ",".join(decoded))
print("data_blocks=" + "|".join(block_ranges))
print("index_separators=" + ",".join(separators))
print(f"seek_band_block={block_index('band')}")
print(f"seek_blueberry_block={block_index('blueberry')}")
print("range_apricot_bandana=" + ",".join(scan("apricot", "bandana")))
print(f"round_trip={decoded == keys}")
print(f"order_valid={decoded == sorted(set(decoded))}")
print("evidence=sorted_run_restart_model")
```

The model represents restart positions as entry indexes, not byte offsets, and has no values, internal versions, varints, block trailers, compression, checksums, handles, index bytes, filters, footer, file I/O, corruption, cache, manifest, or concurrency. Its full next-block first keys are valid lower-bound separators for this lexicographic unique-key case only.

**Layer the file from leaves to footer.** Emit ordered data blocks and trailers, then optional filter/properties/dictionary/range-deletion blocks. Emit a metaindex mapping stable names to handles, then primary/top-level index. A fixed-size or self-locating footer records format/magic, top handles, checksum context, and perhaps version. File-level properties include comparator, smallest/largest internal/user keys, sequence range, entry/deletion counts, raw/compressed sizes, creation reason, and feature identities.

**Checksums need context.** Define whether checksum covers compressed bytes, compression type, trailer, block location, file identity, and footer. Verify before decompression where possible, then enforce decoded size/resource limits. Stronger parent/manifest authentication can detect misplaced blocks/files. Encryption requires authenticated nonces/associated data and key/version lifecycle. A checksum mismatch is corruption, never a negative lookup.

**Cache by immutable identity.** Cache keys include database/tenant, file number/generation or content identity, block offset/type, format, and encryption/compression context. File-number reuse without generation can return stale blocks. Admission/pinning policies for data, index, filter, and dictionaries affect memory and reads. Validate cached decoded structures or rely on a proven insertion boundary; protect against mutable aliasing.

**Builder finalization is transactional.** Write to a private unique name, check every append and short write, finalize all metadata/footer, sync file as required, independently reopen/verify, then install through durable manifest version edit. Rename alone is not the logical commit. Retain WAL/input files until serving state is recoverable. Clean partial files by ownership manifest after crash.

**Readers pin file-set versions.** A reader obtains a manifest/version and file reference. Compaction can publish replacements but cannot delete the old file until all readers, iterators, cache handles, backups, checkpoints, replicas, and recovery versions release it. File immutability eliminates content races, not lifetime races. Use generations and delayed deletion to prevent stale descriptors/async I/O from observing reused identities.

**Compatibility is bidirectional policy.** Define which readers accept each format, how unknown optional/required features behave, comparator/filter policy names, checksum/compression availability, and downgrade. Golden files from every supported version must be decoded by independent/current readers. Migration writes new files privately through compaction/rebuild, validates logical equivalence, publishes, and retains rollback-compatible state as promised.

**Repair is not ordinary reading.** Normal reads fail closed with file/block/key context. Scrub reads every block, verifies footer/handles/order/restarts/checksums/properties, and cross-checks manifest ranges. Redundant storage may replace a corrupt file/block after validating alternate identity. Salvage scans bounded byte regions and emits provenance plus gaps/uncertainty into a new generation; it never silently treats skipped bytes as complete data.

**Test bytes adversarially.** Golden exact encodings, round-trip property tests, independent builder/reader, randomized ordered internal versions, every restart interval/block boundary, separator oracle, mutation of every length/offset/count/type/checksum/magic, truncation at every byte, decompression bombs, comparator mismatch, cache identity, file replacement, and crash publication. Bound CPU, recursion, memory, output, and error detail for hostile files.

## Definitions and Notation

An internal entry is `(u,s,k,v)` for user key u, sequence s, kind k, and payload v under comparator C. Data block i has interval `[lo_i,hi_i]` under a declared inclusive/fence convention and handle `(offset_i,size_i)`. Restart interval r and restart positions `q_j` bound prefix reconstruction.

Let D be data-block count, F encoded file bytes, and `HandleEnd=offset+size+trailer` computed with checked arithmetic. `RawBytes`, `CompressedBytes`, `IndexBytes`, `FilterBytes`, `CacheBytes`, physical requests, decoded bytes, and returned payload are separate metrics. File identity is not pathname alone; include immutable number/generation/content and definition context.

## Mechanisms, Invariants, or Proof Structure

### Block proof

1. Start with globally ordered internal entries under pinned comparator.
2. Encode restart entries fully and other keys relative to validated predecessor.
3. Prove decoder reconstructs each original key and bounded lengths remain inside entry region.
4. Validate restart count/array/order/record boundaries and zero-shared restart property.
5. Prove decoded keys remain ordered and values/kinds/sequences pair with exact records.
6. Attach checksum/type/context and reject corruption before logical use.

### Routing/iteration proof

1. Partition the exact ordered stream into contiguous nonoverlapping data blocks.
2. Derive each index separator within the legal gap for its child-selection convention.
3. Validate handles and block intervals against file/footer properties.
4. Point seek selects the only possible block, restart interval, then first entry >= target.
5. Range iterator emits successive ordered entries/blocks exactly within endpoints.
6. Snapshot/version resolution above the file retains correct user-key semantics.

### Publication/lifetime proof

1. Allocate private immutable identity and write all checked blocks/index/meta/footer.
2. Complete required file/directory durability and independent reopen validation.
3. Atomically/recoverably add file through manifest/version edit.
4. Readers pin a version and immutable file identity for iterator/cache lifetime.
5. Retire obsolete file only after all reader/recovery/backup/replica references clear.
6. Reconcile partial/orphan/obsolete files after every crash prefix without losing serving state.

## Alternatives and Trade-Offs

| Choice | Strength | Cost/proof burden |
|---|---|---|
| Small data blocks | narrow reads/corruption | more index/trailers, weaker compression |
| Large data blocks | compression/sequential scans | read/decode amplification and cache waste |
| Frequent restarts | faster bounded seeks | more full keys/restart bytes |
| Sparse restarts | better compression | longer decode chains |
| Full separators | simple comparator safety | larger index |
| Shortened separators | smaller index | comparator-specific proof |
| Single-level index | simple lookup | index memory/read for huge files |
| Partitioned/two-level index | scalable metadata | extra lookup/cache complexity |
| Per-block compression | random access | weaker cross-block ratio |
| Whole-file compression | ratio | poor random access/recovery |
| Embedded filter | self-contained | format/cache coupling |
| Sidecar components | independent evolution | atomic component-set publication |

## Failure Modes and Misconceptions

- **“Sorted by user key is enough.”** Internal sequence/kind order controls version resolution.
- **“Immutable means trustworthy.”** Validate all bytes and identity on every trust boundary.
- **“In-bounds offset is a restart.”** It must point to a valid zero-shared record boundary.
- **“Prefix compression permits random decode.”** Begin from a validated restart and reconstruct forward.
- **“First key of next block is always shortest separator.”** It is safe under a convention; shortening needs proof.
- **“Filter/index says absent, so corruption is absence.”** Invalid metadata is an error.
- **“Checksum covers correctness.”** It does not prove ordering, comparator, manifest completeness, or freshness.
- **“Footer magic validates file.”** Validate every handle/block/property and compatible format.
- **“Rename publishes the SSTable.”** Manifest/version and durability define serving state.
- **“Compaction can unlink old file immediately.”** Readers and recovery versions pin lifetime.
- **“File number is a cache identity forever.”** Include generation/database/context and forbid unsafe reuse.
- **“Repair that returns some rows succeeded.”** Report gaps, provenance, uncertainty, and never claim completeness.

## Worked Examples

### Example 1

**Problem.** Encode `apple,application,apricot`.

**Derivation.** Apple restart stores full. Application shares `appl` length 4 and suffix `ication`; apricot shares `ap` length 2 and suffix `ricot`.

**Conclusion.** Prefix savings depend on local ordered similarity.

### Example 2

**Problem.** Seek apricot with restart interval three.

**Derivation.** Start at full apple, decode application then apricot; compare until first key >= target.

**Conclusion.** Restart bounds dependent reconstruction.

### Example 3

**Problem.** Shared length exceeds previous key.

**Derivation.** Reject as malformed before slicing/allocation. Clamping could forge a different ordered key.

**Conclusion.** Decoder validation is semantic integrity.

### Example 4

**Problem.** Blocks end apricot and begin banana.

**Derivation.** Full banana is a valid right-lower-bound separator; a shorter `b` may distinguish under bytewise comparator but not every custom collation.

**Conclusion.** Separator optimization is comparator-specific.

### Example 5

**Problem.** Handle offset near max integer plus size wraps.

**Derivation.** Use checked addition and compare offset, size, trailer, end against file regions before read.

**Conclusion.** Bounds checks must not themselves overflow.

### Example 6

**Problem.** Compressed block checksum passes but expands beyond configured maximum.

**Derivation.** Reject before/while bounded decompression; integrity of compressed bytes does not authorize resource exhaustion or claimed decoded length.

**Conclusion.** Resource limits are correctness/security boundaries.

### Example 7

**Problem.** Filter claims key absent but filter checksum/identity is invalid.

**Derivation.** Do not skip data. Report corruption or use a documented fallback that ignores the filter and checks the index/data.

**Conclusion.** Optimization metadata cannot turn uncertainty into absence.

### Example 8

**Problem.** Crash after full file sync but before manifest edit.

**Derivation.** File is private orphan; serving version excludes it and WAL/inputs remain. Recovery reclaims or resumes by build ownership.

**Conclusion.** Complete file is not installed file.

### Example 9

**Problem.** Old reader scans file after compaction publishes replacement.

**Derivation.** Reader's version/file reference pins old identity; deletion waits. Cache entries remain valid for that immutable file, not a reused number.

**Conclusion.** Immutability requires lifetime management.

### Example 10

**Problem.** Increasing blocks from 4 KiB to 64 KiB reduces requests but worsens p99 point reads.

**Derivation.** Measure bytes read/decompressed, cache pollution, compression ratio, storage granularity, index/filter hits, CPU, ranges, and tails.

**Conclusion.** Block size is a workload/hierarchy trade-off.

## Cross-Program Connections

- **Database Engineering:** internal keys, MVCC, tombstones, table formats, corruption recovery, backups, and online upgrades define database semantics.
- **Data Engineering:** Parquet/ORC/lake files share footer discovery, row-group indexes, checksums, statistics, immutable publication, and schema evolution concerns.
- **Security Engineering:** malicious lengths/offsets/compression, checksum substitution, cache confusion, encryption context, and salvage provenance are trust boundaries.
- **Operating Systems:** pread/mmap/direct I/O, readahead, cache, short/error reads, fsync, rename, file deletion, and descriptor lifetime shape realization.
- **Distributed Systems:** object-store multipart upload, manifests, content identity, replication, remote caches, range requests, and eventual deletion extend publication.
- **Performance Engineering:** restart/block/index/filter sizes, compression, caches, prefetch, iterator width, physical locality, and tails require controlled benchmarks.

## References

1. Google LevelDB, [“Table Format”](https://github.com/google/leveldb/blob/main/doc/table_format.md), current maintainer documentation accessed 2026-08-30. Canonical data/meta/index/footer and filter layout.
2. Google LevelDB, [`table/format.h`](https://github.com/google/leveldb/blob/main/table/format.h), current source accessed 2026-08-30. Block handles, footer length/magic, trailer, checksum-aware block read interface.
3. RocksDB Project, [“Block-Based Table Format”](https://github.com/facebook/rocksdb/wiki/Rocksdb-BlockBasedTable-Format), current maintainer documentation accessed 2026-08-30. Production data/index/filter/properties/footer and format evolution.
4. RocksDB Project, [`BlockBasedTableOptions`](https://github.com/facebook/rocksdb/blob/main/include/rocksdb/table.h), current source documentation accessed 2026-08-30. Format versions, checksum context, caches, indexes, compression, and block options.
5. Google, [“Bigtable: A Distributed Storage System for Structured Data”](https://research.google.com/archive/bigtable-osdi06.pdf), *OSDI*, 2006. Primary SSTable, tablet, memtable, compaction, locality, and distributed storage design.
6. Apache Cassandra, [“Storage Engine: SSTables”](https://cassandra.apache.org/doc/stable/cassandra/architecture/storage-engine.html), current documentation accessed 2026-08-30. Official immutable component files, indexes, filters, compression, checksums, and versions.
7. Apache Cassandra, [“SSTable Tools”](https://cassandra.apache.org/doc/latest/cassandra/managing/tools/sstable/index.html), current documentation accessed 2026-08-30. Official dump, metadata, scrub, split, upgrade, and verify operational tools.
8. RocksDB Project, [“Data Block Hash Index”](https://rocksdb.org/blog/2018/08/23/data-block-hash-index.html), maintainer engineering note, 2018. Restart-interval search and optional within-block index trade-offs.

## Exercises

### Exercise 1

Specify and prove a prefix-compressed data-block format with canonical lengths, restart tail, checksum/type trailer, hostile-input limits, seek, forward/reverse iteration, and exact golden/fuzz evidence.

### Exercise 2

For ordered keys `ant,anteater,anthem,banana,band,bandit,car`, restart interval two, and three entries per data block, compute shared prefixes, restarts, block ranges, full right-bound separators, seeks for anthem/ball/cat, and range `[anteater,bandit]`.

### Exercise 3

Design an SSTable file with internal versions/tombstones, data/index/metaindex/filter/properties/footer, checksums, compression/encryption, handles, comparator identity, cache identity, and point/range read failure taxonomy.

### Exercise 4

Design builder finalization, independent verification, manifest publication, reader pinning, compaction retirement, crash recovery, object-store variant, migration/downgrade, scrub, repair, and salvage.

### Exercise 5

Audit a reader that trusts restart offsets, uses wrapping handle arithmetic, accepts unknown comparator as bytewise, treats bad filter/checksum as absence, caches by file number only, and lets repair skip corrupt blocks while reporting success.

## Answers to the Exercises

### Answer 1

Each entry encodes bounded canonical shared/unshared/value lengths then suffix/value. Restart entries require shared zero. Tail stores fixed-width restart byte offsets and count before checksum/type trailer. Parser checks trailer space, count/multiplication/addition, ordered in-region offsets, actual record boundaries, first/restart rules, varint termination/canonicality, shared <= previous key, record remaining bytes, maximum key/value/block/decompressed sizes, and strict internal order.

Seek binary-searches decoded full restart keys, reconstructs forward to first key >= target. Forward retains predecessor; reverse locates prior restart and reconstructs a bounded interval or uses extra reverse metadata. Checksum includes declared compressed bytes plus type/location/file context; decompress only under limits. Prove encoder-decoder round trip and restart-bounded reconstruction; use exact golden bytes, every boundary/interval, random ordered entries/versions, independent decoder, truncation/mutation at every field, bombs, wrong comparator/type/checksum, and resource/time limits.

### Answer 2

Restarts at entries 0,2,4,6. Shared lengths: ant 0; anteater shares 3 (`ant`); anthem restart 0; banana shares 0 with anthem; band restart 0; bandit shares 4 (`band`); car restart 0. Blocks are `ant..anthem`, `banana..bandit`, `car..car`; full right-lower-bound separators are banana and car.

Anthem routes block 0 and succeeds. Ball is below banana, routes block 0, and misses after anthem; cat is >= car, routes block 2 and misses after car. Inclusive `[anteater,bandit]` emits `anteater,anthem,banana,band,bandit`. Exact routing equality follows the declared full lower-bound separator convention.

### Answer 3

Store internal `(user,descending sequence,kind)` plus payload in prefix-compressed independently checksummed/compressed blocks. Handles are canonical checked offset/size. Index maps proven separators to data; metaindex maps versioned names to filter/properties/dictionary/range-deletion blocks; fixed footer carries format/magic and top handles. Properties pin comparator/normalization, filter policy, sequence/ranges, counts, sizes, checksum/compression/encryption, feature and creation identities.

Reader validates footer/file size, top handles, metadata identities, then uses filter only if valid/no-false-negative compatible, index to checked candidate, trailer checksum/context before bounded decompression, restart parser and internal order, and snapshot version resolution. Cache key includes database/tenant/file generation or content, offset/type/format/crypto. Return separate found, deleted/absent, unsupported, corrupt, I/O unavailable, auth/key unavailable, and resource-limit outcomes; never map the latter to absent.

### Answer 4

Builder pins definition, writes private unique identity with checked short/error handling, finalizes blocks/metadata/footer, syncs required file/object parts, and independently reopens to validate exact source multiset/order and all structures. Durable manifest edit installs it; WAL/inputs remain until recoverable. Readers pin manifest/file/cache references; compaction publishes outputs then retires old files after all reader/backup/replica/recovery lifetimes. Crash reconciliation separates referenced, private, orphan, obsolete, and deletable identities.

Object storage uses immutable object identity, completed multipart upload/checksum/version, range-read semantics, and conditional manifest/catalog publication; listing is not authority. Migration writes/validates new generation, publishes, retains rollback-compatible readers/files, and tracks replicas. Golden files prove upgrade/downgrade. Scrub checks every byte/topology/property against manifest; repair uses verified replica/rebuild. Salvage is offline/bounded, records gaps/provenance/uncertainty, emits a new untrusted-until-validated generation, and never claims complete recovery from partial bytes.

### Answer 5

Validate restart count/offset ordering/bounds and actual zero-shared record boundaries; otherwise corrupt offsets can forge keys or exhaust resources. Use checked offset+size+trailer arithmetic before read. Comparator identity is part of persisted semantics: unknown is unsupported, not permission for bytewise interpretation. Invalid filter must be ignored with safe data lookup or fail corrupt; invalid data checksum is corruption, never absence.

File number reuse causes stale cache hits, so key by database plus immutable generation/content, block offset/type/format/crypto and delay reuse. Repair skipping bytes cannot establish missing entries or ordering; report each corrupt range and uncertainty, preserve original evidence, rebuild from trusted sources/replicas when possible, independently validate emitted generation, and label salvage partial rather than success. Add parser fuzz/mutation, cache-reuse races, comparator/format compatibility, crash publication, and corruption-oracle tests before performance claims.
