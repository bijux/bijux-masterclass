---
module_id: DE-006
program: Data Engineering
level: 1
module_number: 6
title: Parquet and Columnar Files
status: complete
last_verified: 2026-09-02
---

# Parquet and Columnar Files

## One-Page Review

### Governing question

How should a data engineer design, write, validate and operate Parquet files so that column projection and metadata pruning improve analytical reads without corrupting schema, nulls, nesting, statistics, security or reproducibility?

### Essential definitions

- A **Parquet file** is an immutable column-oriented file whose data precedes a Thrift-serialized footer and whose beginning and end use `PAR1` framing in the ordinary unencrypted-footer layout.
- A **row group** is a horizontal partition of rows. Each row group contains one column chunk for every leaf column.
- A **column chunk** is the data for one leaf column within one row group, stored as a sequence of pages.
- A **page** is an independently encoded and usually compressed unit within a column chunk; page headers describe its representation.
- A **physical type** is a minimal storage primitive such as `INT32`, `INT64`, `BYTE_ARRAY` or `FIXED_LEN_BYTE_ARRAY`.
- A **logical type** annotates a physical type with interpretation such as string, decimal, date, timestamp, list or map.
- A **definition level** records how far an optional path is defined; null values do not occupy value-encoding slots.
- A **repetition level** records where repeated nested paths continue or restart, allowing a leaf stream to reconstruct lists and records.
- **Column projection** reads only requested leaf column chunks while reconstructing the selected logical fields.
- **Predicate pruning** uses trustworthy metadata to prove that a row group or page cannot satisfy a predicate, avoiding its data read.
- A **page index** contains optional column and offset indexes for page-level value and row-position navigation.
- A **Bloom filter** is a probabilistic membership structure: a negative result can exclude a value under the governed algorithm, while a positive result remains only a candidate.

### Central model, mechanism, or theorem

Represent a file as

$$
F=(S,G_1,\ldots,G_m,M),\qquad G_i=(C_{i1},\ldots,C_{ik}),
$$

where $S$ is the full logical/physical schema, each row group $G_i$ covers one ordered interval of rows, $C_{ij}$ is leaf column $j$'s chunk for that same interval, and footer metadata $M$ locates chunks and optional indexes/statistics. For query predicate $P$ and projection $Q$, a reader may prune unit $u$ only when metadata proves $\forall r\in u:\neg P(r)$. Otherwise it must treat the unit as a candidate and evaluate $P$ on decoded values. Optimization metadata may reduce I/O; it must never invent query truth.

### Critical invariants

- File framing, footer length, metadata offsets and every page/chunk range stay within the immutable object's byte bounds.
- Every row group has one aligned column chunk per leaf path and reconstructs the declared number and order of logical rows.
- Physical type, logical annotation, precision, scale, unit, signedness and field identity remain compatible with the dataset contract.
- Definition and repetition levels remain within schema-derived maxima and consume exactly the correct number of encoded values.
- Compression and value encodings match page metadata and remain within reader support and resource limits.
- Statistics, page indexes and Bloom filters are used only under their defined type ordering, truncation, null and trust rules.
- Pruning is conservative: uncertain, absent, unsupported, corrupt or unauthorized metadata causes a read, not a false exclusion.
- Files are published atomically and treated as immutable; dataset snapshots name exact objects and schema/partition state.
- Encryption and key authorization cover sensitive data plus revealing metadata such as statistics and Bloom filters.
- File count, file size, row-group size and page size are selected from measured workload and storage behavior, not folklore.

### Common failures

Calling Parquet “compressed CSV”; confusing row groups with files or partitions; expecting row-oriented point updates; reading the head instead of the footer first; trusting extension alone; assuming all columns are adjacent globally; treating physical types as domain types; writing decimal or timestamp annotations inconsistently; losing null versus empty in nested lists; decoding definition levels as values; misaligning leaf streams; selecting unsupported encodings; believing dictionary encoding is always smaller; double-compressing blindly; pruning with corrupt, incorrectly ordered, truncated or NaN statistics; treating Bloom positives as matches; requiring indexes for correctness; producing millions of tiny files; creating huge row groups that exceed writer memory; overwriting published objects; and assuming encryption of data pages hides plaintext footer metadata.

### Compact example

A file has three 100-row row groups for integer `order_id` ranges `[1,10]`, `[11,20]` and `[21,30]`. Query `18 <= order_id <= 23` can safely prune the first group because its maximum is below 18; the other two remain candidates and rows still require evaluation. Projection requests `order_id` and `amount` but not a large payload column, so only relevant column chunks are fetched. Optional `discount` uses definition levels: level zero contributes null with no encoded value, while maximum level consumes the next encoded integer. The reader validates footer and chunk bounds before range reads and reconciles decoded row counts across columns.

### Connections

[DE-005](005-arrow-and-in-memory-columnar-representation.md) develops in-memory arrays and record batches; Parquet readers commonly materialize selected pages into Arrow arrays, but layouts are not identical. [DE-004](004-avro-protocol-buffers-and-schema-aware-serialization.md) supplies schema-evolution concepts. Dataset layout connects to [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) and object-store behavior to [Cloud & Infrastructure Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md).

## Governing Question

What conditions let a reader avoid bytes while still returning exactly the rows and fields required by an analytical query?

Parquet arranges each row group's leaf columns into independently addressable chunks and records their locations in footer metadata. A reader can fetch the footer, choose row groups, choose columns and decode only relevant pages. Encodings and compression exploit local value patterns.

These mechanisms are not a database optimizer and do not guarantee fast queries. Selectivity depends on file clustering, row-group ranges, metadata quality, object-store request behavior and reader implementation. A filter on an unsorted high-cardinality column may overlap every row group.

The current Apache [Parquet file-format documentation](https://parquet.apache.org/docs/file-format/) and authoritative [parquet-format specification](https://github.com/apache/parquet-format/blob/master/README.md) define the footer, Thrift metadata, physical/logical types, nested levels, pages, encodings and extensions. Data engineers must combine those byte rules with immutable dataset publication, domain schema and representative measurement.

## Why This Matters

Analytical datasets often retain billions of rows while queries need a few fields and time ranges. Column projection avoids reading irrelevant fields. Row-group and page pruning can avoid regions whose metadata proves they cannot match. Encodings and compression reduce storage and transfer.

Write decisions determine later read options. Sorting or clustering a timestamp may create disjoint min/max ranges; random ordering can make every range overlap. Row-group size governs sequential I/O, pruning granularity, footer size, writer buffering and parallelism. Page size governs encoding locality and page-index precision.

Schema errors can survive unnoticed. A byte array annotated as UTF-8 may contain invalid text. Decimal precision or scale can differ across files. Legacy timestamp encodings and timezone assumptions can yield plausible wrong instants. A dataset directory can contain individually valid Parquet files with mutually incompatible schemas.

Nested data adds reconstruction state. Parquet flattens leaf values and carries definition/repetition levels. Missing list, empty list, null element and present scalar can occupy different levels while some states emit no value bytes. A reader that counts only encoded values loses logical rows.

Optimization metadata is untrusted input at many boundaries. A malformed footer can point outside the object. Decompression can expand aggressively. Incorrect min/max statistics can cause false pruning and silent wrong answers. A robust reader validates structure and degrades uncertain optimization into extra reading.

File operations are dataset operations. Object stores typically make whole objects immutable in practice; rewriting one logical field creates new files. Without a snapshot/manifest protocol, readers can observe mixtures of old and new objects, duplicates or gaps.

## Prerequisites and Retrieval

Retrieve the domain grain and schema; all physical/logical Parquet types; field IDs where used; required/optional/repeated structure; decimal precision/scale and temporal unit/timezone policy; writer/reader libraries and supported format features; data-page version and encodings; codec and level; row-group/page targets; dictionary fallback behavior; sort order and clustering; column-chunk, page and file statistics configuration; page indexes and Bloom filters; checksum and encryption settings; footer/key policy; object-store consistency and range-read behavior; file naming and immutable snapshot manifest; partition values and source provenance; expected row counts and null distributions; target projections/predicates; memory and concurrency limits; repair/quarantine policy; and representative files from every writer/version.

Distinguish dataset partition from file; file from row group; row group from column chunk; column chunk from page; logical column from nested leaf path; schema field from partition directory; physical type from logical annotation; encoding from compression; dictionary encoding from a database dictionary; null from absent encoded value; null list from empty list and null element; row-group statistics from page index; Bloom negative from positive candidate; sortedness metadata from actual order; pruning from filtering; projection from row selection; file metadata from external catalog; format release from file metadata version; immutable rewrite from in-place update; encryption at rest from Parquet modular encryption; checksum from authenticity; and Arrow materialization from Parquet storage.

## Learning Objectives

After completing this module, you should be able to:

1. trace a Parquet file from framing and footer to row groups, column chunks and pages;
2. distinguish physical types, logical annotations, value encodings and compression;
3. reconstruct optional and repeated nested values from definition/repetition levels;
4. reason conservatively about projection, statistics, page indexes and Bloom filters;
5. select file, row-group and page sizes using measured workload evidence;
6. validate footer, range, page, codec and allocation boundaries before decoding;
7. preserve schema, row alignment, nulls and field identity across files and readers;
8. design atomic immutable dataset publication and compaction;
9. protect sensitive data and metadata using appropriate encryption/key policies; and
10. verify cross-reader compatibility and query equality against a non-pruned baseline.

## Core Exposition

### Read the file from its footer

An ordinary Parquet file starts with four-byte magic `PAR1`. Data column chunks follow. Near the end are Thrift-serialized file metadata, a four-byte little-endian footer length and trailing `PAR1`.

A reader normally range-reads the tail, validates the trailing magic and footer length, then retrieves metadata to locate desired column chunks. It does not discover the schema by scanning every page.

Validate all arithmetic and byte ranges against immutable object length before following them.

### Understand row groups

A row group is a horizontal slice of the logical table. All leaf column chunks in one row group cover the same logical rows.

Row groups are the common unit of coarse pruning and parallel work. Larger groups improve sequential I/O and compression opportunities but reduce pruning granularity and require more write/read buffering.

Target bytes as well as rows because variable-width data changes group size dramatically.

### Understand column chunks

For every leaf column path, a row group has one column chunk. The chunk contains its pages back to back and carries metadata for type, encodings, codec, counts, sizes, offsets and optional statistics/indexes.

Projection selects leaf chunks needed to reconstruct requested fields and evaluate filters. Nested parent fields can require multiple leaf paths and levels.

Column chunks for a column are not necessarily contiguous across all row groups.

### Understand pages

Pages are the encoded/compressed units inside a column chunk. A dictionary page, if used, precedes data pages in that chunk. Data pages carry repetition levels, definition levels and encoded values according to page version and schema.

Page headers are Thrift structures stored inline. Optional page indexes near the footer allow navigation without first reading every page header.

Treat declared compressed and uncompressed sizes as untrusted until bounded and reconciled.

### Separate physical and logical types

Parquet deliberately has few physical types: Boolean, 32/64-bit integers, floating point, byte arrays and fixed-length byte arrays, plus legacy `INT96`.

Logical annotations specify string, integer widths/signedness, decimal, date/time, timestamp, UUID, JSON, list, map and other meanings over those primitives.

Validate both layers. `INT64` milliseconds and microseconds are physically alike but semantically different.

### Govern decimal representation

Decimal encodes an unscaled integer plus declared scale and precision over permitted physical types. The interpreted value is `unscaled × 10^{-scale}`.

Across files, require compatible precision, scale and physical representation or perform an explicit safe conversion. Check extrema, negative two's-complement bytes, sign extension, overflow and rounding.

Do not infer monetary unit from scale; currency remains domain metadata.

### Govern temporal representation

Date, time and timestamp logical types specify units and adjusted-to-UTC semantics where applicable. Legacy `INT96` timestamps have inconsistent ecosystem history.

Choose one governed representation, record timezone semantics and test across languages. Treat local civil time and instant as different types.

Schema merge must not silently coerce milliseconds to microseconds or attach a timezone.

### Separate encoding from compression

Encoding transforms values into a structured representation: plain, dictionary, delta, RLE/bit-packed hybrid, delta byte array or byte-stream split. Compression then applies a codec to page data.

Encoding effectiveness depends on distribution. Dictionary favors repeated vocabulary; delta favors correlated sequences; byte-stream split can help floating-point compression.

Reader support determines compatibility. Plain is a baseline; newer encodings can make a file unreadable to older readers.

### Use dictionary encoding by evidence

A dictionary page stores distinct values, and data pages store encoded indices. When cardinality or dictionary size grows, writers may fall back to plain encoding within the same column chunk.

Readers must support mixed encodings declared in metadata. A dictionary is scoped to its column chunk, not globally to a dataset.

Measure encoded bytes and decode cost. High-cardinality identifiers may gain little.

### Choose compression deliberately

Codec choice trades compressed bytes, CPU, implementation support and latency. Value encoding changes codec input and can matter as much as codec name.

Benchmark full write and representative projected/filter reads. Include object transfer, decompression, vector materialization and concurrency.

Cap decompressed size before allocation and compare actual output with declared page size.

### Encode nulls with definition levels

Definition level indicates how many optional nodes on a leaf path are present. At maximum level, a value is encoded; below maximum, a particular ancestor or leaf is null/absent and no physical value is consumed.

For a flat optional scalar with max definition level one, levels `(1,0,1)` plus encoded values `(7,8)` reconstruct `(7,null,8)`.

Logical count follows levels, not number of encoded values.

### Encode repetition with repetition levels

Repetition levels indicate at which repeated ancestor a new value continues. Together with definition levels they distinguish new parent records, repeated elements, empty collections, null collections and null elements.

Max levels derive from schema paths. Validate each level within range and ensure value consumption matches maximum definitions.

Test nested lists/maps across independent implementations; visual tables can hide ambiguity.

### Write standard list and map structures

Current logical-type guidance defines three-level LIST and MAP structures. Historical writers emitted variants that readers may interpret through compatibility rules.

New writers should emit the standard form. Readers supporting archives need targeted fixtures for legacy structures rather than broad guessing.

Preserve distinctions among null list, empty list, list containing null and list containing empty value.

### Project columns correctly

Projection avoids reading unneeded leaf chunks. It does not by itself reduce logical rows, and filters may require columns not returned in final output.

For nested fields, identify all leaves and levels needed to reconstruct the requested logical value. A list of structs is not one flat byte range.

Reconcile row positions across decoded columns before building batches.

### Prune row groups conservatively

For predicate `x >= a`, a row group is safely excluded when trustworthy maximum is below `a`. If statistics overlap, are absent, truncated ambiguously, unsupported or invalid, read the group.

Statistics are bounds, not evidence that every interior value exists. After pruning, evaluate predicates on decoded rows.

Compare pruned results with a scan that ignores statistics during validation.

### Interpret statistics by type order

Min/max bytes require the logical/physical type's defined sort order. Signed versus unsigned integers, byte arrays, decimals, floating NaN and legacy timestamps need specific handling.

Writers may truncate large byte-array bounds. A valid truncated bound can remain conservative under specified rules; arbitrary truncation can cause false exclusion.

Null counts describe nullity but do not turn min/max into a domain constraint.

### Use page indexes optionally

The ColumnIndex stores per-page null/bound information; OffsetIndex maps pages to locations and row positions. Together they support selective page reads and alignment across projected columns.

Indexes are optional. Readers must return correct answers without them. Corrupt or unsupported indexes degrade to reading pages.

They are not secondary indexes sorted independently of file data.

### Use Bloom filters as membership hints

A Bloom filter can rule out equality membership when it returns negative under the exact hashing/type rules. A positive result may be a false positive and still requires data evaluation.

Validate header, algorithm, bitset bounds and column association. Do not use a malformed filter to exclude data.

Bloom filters reveal possible membership and may require encryption for sensitive columns.

### Preserve sort and clustering evidence

Sorting a common predicate column can make row-group/page ranges selective. Store sorting-column metadata where supported, but validate writer behavior and do not infer global order from filenames.

Multiple sort keys help lexicographically; later keys prune well only within constrained earlier-key ranges.

Compaction can improve clustering or destroy it. Measure after rewrite.

### Govern schema evolution across files

A Parquet file has one schema; a dataset can contain many. Adding an optional field may read as null in old files, but field identity, name matching and reader behavior must be explicit.

Never reuse a field ID for changed meaning. Avoid type, scale, unit, repetition or grain changes in place. Test the exact dataset reader's merge behavior.

For incompatible change, write a new field or dataset and migrate with reconciliation.

### Understand format compatibility

The official [format-versions guidance](https://parquet.apache.org/docs/file-format/versions/) distinguishes format-spec releases, the historically inconsistent `FileMetaData.version` field and feature compatibility.

Optional metadata such as Bloom filters may be ignorable by old readers. New encodings or Data Page V2 require actual reader support.

Inventory features written, not merely a nominal “Parquet version.”

### Treat files as immutable

Footer offsets and statistics summarize written bytes. In-place edits risk invalidating them and are poorly matched to object storage.

Write a complete new object, validate it, then atomically publish a snapshot/manifest reference. Retain old snapshots for rollback under policy.

Readers should bind to one snapshot rather than listing a mutating prefix mid-query.

### Control the small-files problem

Many tiny files multiply listings, footer range requests, task scheduling, opens and metadata memory. They also prevent useful row-group sizing.

Compact immutable inputs into larger outputs under one transaction-like publication. Preserve partition/domain boundaries, validate schemas, reconcile rows/digests and avoid duplicate visibility.

Do not create giant files solely to minimize count; parallelism and rewrite cost still matter.

### Size files, groups and pages empirically

Official configuration guidance gives historical workload-oriented starting points, not universal laws. Object stores, modern engines and variable rows differ.

Set targets in bytes, bound writer memory, and observe actual distributions. Balance footer overhead, range requests, parallel tasks, pruning, sequential I/O and retry units.

Retune when schemas, compression, clustering or workloads change.

### Validate checksums and corruption

Page checksums, when present and supported, can detect accidental corruption of page bytes. Object digests and storage checks provide broader evidence.

A checksum is not authentication against an attacker who can replace both content and checksum. Use authenticated storage or Parquet modular encryption for that threat.

Quarantine corrupt files; do not silently skip them and report a partial dataset as complete.

### Use modular encryption deliberately

Parquet modular encryption can protect/authenticate footer and column modules with different keys while preserving selective reads for authorized clients.

Key management, rotation, identities and authorization are external operational responsibilities. Protect indexes, statistics and Bloom filters because they can reveal sensitive properties.

Test partial-encryption behavior across every reader; unsupported readers must fail safely.

### Secure untrusted reads

Validate object size and footer framing before allocating metadata. Bound Thrift nesting/collections, page sizes, levels, dictionary size, decompression and concurrent row groups.

Verify every offset/length with overflow-safe arithmetic and ensure chunks do not claim bytes outside the file. Reject overlapping ranges where the format/profile disallows them.

Run parsers with patched libraries and isolate high-risk ingestion boundaries.

### Contrast Parquet with Arrow

Parquet optimizes durable columnar storage through encodings, compression, row groups, pages and footer metadata. Arrow specifies directly addressable in-memory arrays and IPC.

Reading Parquet commonly decodes selected values/levels into Arrow buffers; this usually involves decompression and materialization. It is not a byte-identical zero-copy mapping in general.

Choose based on boundary: storage/retrieval versus in-memory computation/interchange.

### Observe production datasets

Measure file, row-group and page sizes; rows; compression ratio; encodings; dictionary fallback; schema variants; nulls; statistics availability; pruning ratios; projected bytes; footer requests; read amplification; decode failures; checksum/encryption failures; and snapshot age.

Track candidate units separately from matched rows. High pruning does not prove correct pruning, so run periodic non-pruned comparisons on governed samples.

Alert on tiny-file growth, incompatible writers, impossible offsets, missing snapshots and row-count reconciliation failures.

## Definitions and Notation

Let file $F=(S,G_1,\ldots,G_m,M)$ contain schema $S$, row groups $G_i$ and metadata $M$. If schema has $k$ leaf paths, $G_i=(C_{i1},\ldots,C_{ik})$, and every chunk covers row interval $I_i=[a_i,b_i)$ with $|I_i|=N_i$. Alignment requires all $C_{ij}$ reconstruct exactly $N_i$ logical positions in the same order.

Each column chunk $C$ contains pages $P_1,\ldots,P_p$. Page representation is governed by physical/logical type $T$, value encoding $E$, codec $Z$, maximum definition/repetition levels $d_{max},r_{max}$ and metadata ranges.

For one leaf stream of $L$ level pairs $(r_\ell,d_\ell)$ and encoded-value sequence $V$, require

$$
0\le r_\ell\le r_{max},\quad0\le d_\ell\le d_{max},\quad |V|=|\{\ell:d_\ell=d_{max}\}|.
$$

For unit $u$ with trustworthy bounds $[min_u,max_u]$ and query predicate $P$, define `exclude(u,P)` only when the bounds prove $\forall x\in u:\neg P(x)$. Candidate set is $U_P=\{u:\neg exclude(u,P)\}$. Correctness requires every matching row's unit remain in $U_P$; false-positive candidates affect cost only.

For projection $Q$ and candidate row groups $U_P$, approximate compressed bytes scheduled as $B(Q,U_P)=\sum_{i\in U_P}\sum_{j\in leaves(Q\cup fields(P))} size(C_{ij})$, plus metadata/index requests. Actual bytes depend on page pruning, request coalescing and reader behavior.

## Mechanisms, Invariants, or Proof Structure

### Sixteen-step Parquet lifecycle

1. Define grain, schema, field identity, nulls, units, time and compatibility.
2. Choose supported physical/logical types, page version, encodings and codecs.
3. Cluster data for important predicates without inventing global order.
4. Select byte-bounded file, row-group and page targets from measurements.
5. Encode nested definition/repetition levels and leaf values consistently.
6. Write column chunks/pages with bounded dictionaries and compression.
7. Emit conservative statistics, indexes, filters and checksums as supported.
8. Protect sensitive data and metadata with governed encryption/key access.
9. Finish footer/framing before making the object visible.
10. Reopen with independent readers and validate full schema and structure.
11. Reconcile rows, nulls, extrema and domain aggregates to source evidence.
12. Compare projected/pruned queries with an unpruned baseline.
13. Publish immutable objects through one atomic dataset snapshot.
14. Serve range reads under allocation, decompression and concurrency limits.
15. Observe layout, pruning, read amplification, failures and schema drift.
16. Compact/migrate by writing new snapshots with rollback and reconciliation.

### Byte-range invariant

Magic, footer length, metadata, indexes, Bloom filters, chunks and pages refer only to validated non-overflowing ranges inside the exact immutable object.

### Row-alignment invariant

Every leaf chunk in a row group reconstructs exactly the declared row count and positions align across all projected/filter columns.

### Level-consumption invariant

All definition/repetition levels lie within schema maxima, and a physical value is consumed exactly when the leaf is maximally defined.

### Type-fidelity invariant

Physical type plus logical annotation, precision, scale, unit, timezone, repetition and field identity preserve the dataset contract across every file.

### Conservative-pruning invariant

Only proof of impossibility excludes a unit. Missing or doubtful metadata expands candidates rather than dropping possible matches.

### Publication invariant

Readers see one immutable manifest of complete validated files; compaction or migration never exposes both replaced and replacement rows in the same snapshot.

### Resource invariant

Footer, page, dictionary, level, decompression, row-group and concurrency work remain within enforced limits before allocation and decode.

### Security invariant

Authorization and cryptographic policy protect sensitive pages plus metadata leakage, and integrity evidence is appropriate to accidental versus adversarial threats.

### Proof sketch: overlapping statistics cannot prove a match

Let a unit have exact minimum 1 and maximum 10, and predicate `x=5`. Dataset A contains values `{1,5,10}`; dataset B contains `{1,10}`. Both have identical min/max bounds, but A contains a match and B does not. Therefore overlapping bounds cannot prove membership. They can only prevent exclusion. A reader must decode candidate data or use another sound structure; treating overlap as a match yields false positives.

### Executable pruning and levels audit

The synthetic audit performs conservative range pruning, calculates projected compressed bytes, and reconstructs optional values from definition levels. It models finite metadata rules rather than parsing a real Parquet file or benchmarking storage.

<!-- bijux-verify: {"id":"parquet-pruning-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"selected_groups=2,3\nrows_candidate=200 rows_total=300\nprojected_bytes=800 full_bytes=4500\ndefinition_levels=(1, 0, 1, 0)\nencoded_values=(7, 8)\nreconstructed=(7, None, 8, None)\n","stderr":""}} -->
```python
row_groups = (
    {"id": 1, "min": 1, "max": 10, "rows": 100, "bytes": {"id": 100, "amount": 400, "payload": 1000}},
    {"id": 2, "min": 11, "max": 20, "rows": 100, "bytes": {"id": 100, "amount": 400, "payload": 1000}},
    {"id": 3, "min": 21, "max": 30, "rows": 100, "bytes": {"id": 100, "amount": 400, "payload": 1000}},
)
lower, upper = 18, 23
selected = tuple(
    group for group in row_groups
    if not (group["max"] < lower or group["min"] > upper)
)
projected_bytes = sum(group["bytes"]["amount"] for group in selected)
full_bytes = sum(sum(group["bytes"].values()) for group in row_groups)

definition_levels = (1, 0, 1, 0)
encoded_values = (7, 8)
cursor, reconstructed = 0, []
for level in definition_levels:
    if level == 1:
        reconstructed.append(encoded_values[cursor])
        cursor += 1
    else:
        reconstructed.append(None)
if cursor != len(encoded_values):
    raise ValueError("definition levels and values disagree")

print(f"selected_groups={','.join(str(group['id']) for group in selected)}")
print(f"rows_candidate={sum(group['rows'] for group in selected)} rows_total={sum(group['rows'] for group in row_groups)}")
print(f"projected_bytes={projected_bytes} full_bytes={full_bytes}")
print(f"definition_levels={definition_levels}")
print(f"encoded_values={encoded_values}")
print(f"reconstructed={tuple(reconstructed)}")
```

### Verification strategy

Read footer ranges manually; corrupt magic, footer length and chunk/page offsets; test empty files/groups/pages; compare declared and reconstructed row/value counts; populate all physical/logical types at extrema; cross-check decimals and timestamps across languages; exhaust null/empty/nested list/map states; mutate definition/repetition levels; force dictionary fallback and mixed encodings; truncate compressed pages and exceed expansion limits; create NaN, signed/unsigned and truncated string statistics; delete/corrupt page indexes and Bloom filters; compare every pruned result with disabled-pruning scans; vary sorting, row-group/page sizes and codecs on representative workloads; simulate partial writes and mixed snapshot listings; compact with duplicate/gap detection; rotate encryption keys; deny metadata keys; and read every feature with the oldest supported implementation.

## Alternatives and Trade-Offs

- **Parquet versus CSV/JSON:** Parquet supplies typed column chunks and metadata pruning; text formats are more directly inspectable and broadly streamable.
- **Parquet versus Arrow IPC:** Parquet optimizes durable encoded/compressed storage; Arrow IPC optimizes reconstructing in-memory arrays.
- **One file versus many:** fewer large files amortize metadata; more files add parallelism and independent replacement but can overwhelm planning/listing.
- **Large versus small row groups:** large groups improve sequential I/O/compression; small groups improve pruning and lower memory/retry units.
- **Large versus small pages:** large pages reduce header overhead; small pages improve page-index granularity and bound decode units.
- **Row count versus byte targets:** row targets are simple; byte targets better handle variable-width and nested data.
- **Sorted versus unsorted writes:** sorting improves range pruning/compression; it costs shuffle, memory and write latency.
- **Single versus multiple sort keys:** one key gives predictable ranges; multiple keys support compound workloads but weaken later-key global pruning.
- **Plain versus dictionary encoding:** plain is universal/predictable; dictionary benefits repeated values but may fall back at high cardinality.
- **Delta versus plain integers:** delta compresses correlated sequences well; arbitrary values may add decode complexity without gain.
- **Byte-stream split versus plain floating point:** split can improve codec results; it requires reader feature support.
- **Fast versus dense codec:** fast codecs reduce CPU/latency; denser codecs reduce storage/transfer. Measure the complete path.
- **Data Page V1 versus V2:** V2 separates levels and has different compression/header behavior; older readers may lack support.
- **Row-group statistics versus page index:** group stats are coarse and common; page indexes enable finer reads with metadata cost and variable support.
- **Bloom filter versus min/max:** Bloom filters aid equality on non-clustered values; min/max aids ordered ranges and costs less for favorable clustering.
- **Full versus truncated string statistics:** full bounds improve pruning but enlarge metadata/leak values; sound truncation bounds size but reduce precision.
- **Partition directory versus in-file pruning:** partitions skip whole files via catalog paths; in-file metadata refines within selected files.
- **Schema merge versus normalized rewrite:** merge supports evolution quickly; rewrite enforces one representation at compute/storage cost.
- **Flat versus nested schema:** flat leaves simplify some engines; nested data preserves hierarchy and avoids duplicated parents but complicates levels.
- **Checksums versus encryption:** checksums detect accidental damage; authenticated encryption adds adversarial integrity/confidentiality with key complexity.

## Failure Modes and Misconceptions

1. “Parquet is compressed CSV” ignores typed schema, nested levels, chunks, pages and footer metadata.
2. “Columnar means one file per column” confuses logical organization with ordinary file layout.
3. “A row group is a dataset partition” conflates internal horizontal unit and directory/catalog partition.
4. “A column chunk spans the file” ignores row-group scope.
5. “A page is an I/O request” confuses encoding unit with reader request coalescing.
6. “The schema is at the front” ignores footer-first discovery.
7. “The `.parquet` suffix validates bytes” trusts naming over framing/metadata.
8. “Footer length can be allocated directly” accepts untrusted sizes.
9. “Physical `INT64` identifies timestamps” omits logical annotation.
10. “Decimal scale is formatting” changes numerical value.
11. “Every reader interprets `INT96` alike” ignores legacy ambiguity.
12. “Encoding and compression are synonyms” collapses two transformations.
13. “Dictionary encoding applies to a dataset” ignores column-chunk scope.
14. “Dictionary encoding never falls back” rejects valid mixed-encoding chunks.
15. “Highest compression is fastest” ignores CPU and latency.
16. “Nulls occupy placeholder values” ignores definition-level value consumption.
17. “Encoded value count equals logical row count” fails on nulls/nesting.
18. “Definition levels alone reconstruct lists” omits repetition levels.
19. “Empty list equals null list” loses definition distinctions.
20. “A repeated leaf defines row grain” ignores ancestor structure.
21. “Projection needs only displayed columns” forgets predicate and nested reconstruction leaves.
22. “Statistics prove rows match” confuses candidate overlap with membership.
23. “Statistics are always exact and safe” ignores writer defects, truncation and ordering.
24. “NaN has ordinary min/max behavior” ignores floating edge rules.
25. “A Bloom positive proves membership” ignores false positives.
26. “A Bloom negative is safe regardless of hash/type” ignores compatibility and corruption.
27. “Page indexes are required” makes an optimization part of correctness.
28. “Page index is a secondary index” overstates its structure.
29. “Sorted metadata proves actual ordering” trusts annotation without validation.
30. “Latest-only schema merge protects archives” ignores historical files/readers.
31. “Adding a field changes old files” confuses reader projection with immutable bytes.
32. “Parquet supports updates in place” conflicts with footer/layout and object publication.
33. “Renaming an object atomically publishes a dataset everywhere” assumes storage semantics.
34. “Listing a prefix is a snapshot” can mix generations.
35. “Tiny files only waste storage” ignores planning, ranges, tasks and memory.
36. “One-gigabyte row groups are universal” mistakes a historical recommendation for evidence.
37. “File metadata version states every feature” ignores documented inconsistent use.
38. “A newer spec minor release is always forward compatible” conflicts with feature-level compatibility.
39. “Checksums authenticate data” ignores malicious replacement.
40. “Encrypting pages hides statistics” ignores footer/index/filter leakage and key mode.
41. “Arrow reads Parquet zero-copy” ignores encoded/compressed storage and materialization.
42. “Skipping corrupt files is graceful degradation” silently changes dataset truth.

## Worked Examples

### Example 1

A time-sorted file has hourly row groups. A one-hour query prunes most groups by timestamp min/max and projects three of eighty fields. The team verifies equal results with pruning disabled and measures range requests, not only decoded bytes.

### Example 2

Randomly ordered customer IDs yield min/max ranges covering nearly the entire domain in every group. Bloom filters help point lookups if cardinality/size is reasonable, but positive candidates still scan. Re-clustering is evaluated against write-shuffle cost.

### Example 3

An optional integer stream has levels `(1,0,1,0)` and values `(7,8)`. The reader produces four logical positions and consumes two integers. Attempting to consume one value per level overruns the page and shifts following data.

### Example 4

A nullable list of nullable strings distinguishes null list, empty list, `[null]` and `['']`. Cross-language fixtures verify standard three-level LIST schema plus exact definition/repetition sequences. A legacy two-level archive gets a separate compatibility fixture.

### Example 5

One writer emits decimal `(12,2)` and another `(18,6)` under the same column name. Directory-level schema merge is rejected. A migration writes a new field with explicit conversion/rounding policy and reconciles unscaled totals.

### Example 6

A high-cardinality UUID column begins dictionary encoded then falls back to plain. The reader accepts both encodings within the chunk. Measurement shows dictionary/page overhead exceeds savings, so future files disable it for that field only.

### Example 7

Ten million tiny hourly files create millions of footer requests. Compaction writes larger, date-clustered files to a new snapshot, checks row IDs/counts and query equality, then atomically changes the manifest. Old objects remain for rollback before governed deletion.

### Example 8

A page index contains an out-of-file offset after object truncation. The reader refuses the index and then rejects the structurally incomplete file rather than guessing. The snapshot remains failed/quarantined; it does not silently omit the file.

### Example 9

Sensitive health-code values have Bloom filters. Because membership metadata leaks possible diagnoses, modular encryption uses the column key for pages, indexes and Bloom structures, while authorized projections of nonsensitive columns remain possible under the chosen footer mode.

### Example 10

A new writer enables byte-stream split and Data Page V2. The nominal file metadata version still looks familiar, but the oldest production reader cannot decode. Feature-matrix tests catch it, and the writer stays on the common profile until the reader fleet upgrades.

## Cross-Program Connections

**Data Architecture Engineering:** partitioning, snapshots, contracts and ownership determine which files form one trustworthy dataset.

**Large-Scale Data Systems Engineering:** distributed scans exploit row-group/file parallelism, predicate pruning and projection while coordinating retries and skew.

**Database Engineering:** statistics and zone-map-like bounds aid pruning, but Parquet lacks transactional indexes and update machinery by itself.

**Cloud & Infrastructure Engineering:** range requests, object immutability, listings, request pricing and multipart upload shape effective layouts.

**Security Engineering:** untrusted metadata, decompression, parser libraries, key management and revealing optimization metadata require threat-specific controls.

**Programming Languages:** unsigned order, decimals, timestamps and nested collections map differently across runtimes and need fixtures.

**Performance Engineering:** workload traces, end-to-end bytes, CPU, memory, pruning and task overhead guide encoding and sizing decisions.

**Formal Methods:** conservative pruning is a soundness obligation: optimization may admit extra candidates but must never exclude a possible result.

## References

1. Apache Parquet, [File Format](https://parquet.apache.org/docs/file-format/), current documentation.
2. Apache Parquet, [parquet-format Specification](https://github.com/apache/parquet-format/blob/master/README.md), current authoritative repository.
3. Apache Parquet, [Metadata](https://parquet.apache.org/docs/file-format/metadata/), current documentation.
4. Apache Parquet, [Physical and Logical Types](https://parquet.apache.org/docs/file-format/types/), current documentation.
5. Apache Parquet, [Logical Types](https://parquet.apache.org/docs/file-format/types/logicaltypes/), current specification.
6. Apache Parquet, [Nested Encoding](https://parquet.apache.org/docs/file-format/nestedencoding/), current documentation.
7. Apache Parquet, [Nulls](https://parquet.apache.org/docs/file-format/nulls/), current documentation.
8. Apache Parquet, [Data Pages](https://parquet.apache.org/docs/file-format/data-pages/), current documentation.
9. Apache Parquet, [Column Chunks](https://parquet.apache.org/docs/file-format/data-pages/columnchunks/), current documentation.
10. Apache Parquet, [Encodings](https://parquet.apache.org/docs/file-format/data-pages/encodings/), current specification.
11. Apache Parquet, [Page Index](https://parquet.apache.org/docs/file-format/pageindex/), current specification.
12. Apache Parquet, [Bloom Filter](https://parquet.apache.org/docs/file-format/bloomfilter/), current specification.
13. Apache Parquet, [Modular Encryption](https://parquet.apache.org/docs/file-format/data-pages/encryption/), current specification.
14. Apache Parquet, [Format Versions](https://parquet.apache.org/docs/file-format/versions/), current documentation.
15. Apache Parquet, [Implementation Status](https://parquet.apache.org/docs/file-format/implementationstatus/), current documentation.
16. Apache Parquet, [Configurations](https://parquet.apache.org/docs/file-format/configurations/), current documentation.

## Exercises

### Exercise 1

Given four row groups with trusted integer bounds `[0,9]`, `[10,19]`, `[20,29]`, `[30,39]`, identify candidates for predicate `x > 17 and x <= 31`. Explain why candidate groups are not matching rows.

### Exercise 2

Reconstruct a flat optional integer column from definition levels `(0,1,1,0,1)` and encoded values `(4,5,6)`. State and check the consumption invariant.

### Exercise 3

Design Parquet schema/evidence for nullable `List<nullable String>` and enumerate null list, empty list, one null element and one empty-string element.

### Exercise 4

Design a file/row-group/page sizing experiment for a cloud object-store dataset with time-range filters, five projected columns out of 120, skewed payload widths and a two-minute freshness objective.

### Exercise 5

Design an atomic compaction and schema migration from millions of files containing decimal `(12,2)` to a new `(18,6)` field while preserving rollback and proving no gaps or duplicates.

## Answers to the Exercises

### Answer 1

Group `[0,9]` is excluded because its maximum is not greater than 17. Groups `[10,19]`, `[20,29]` and `[30,39]` overlap the predicate's possible range `(17,31]`, so they are candidates. The last group may contain 30 or 31 even though its maximum extends to 39.

Bounds say only that values fall between minima and maxima. The second group might contain `{10,19}` and no 18; the fourth might contain `{30,39}` and one matching 30 or none if 30 is only a lower conservative bound. Decode and evaluate rows. Validate results against pruning-disabled execution.

### Answer 2

Max definition level is one. Traverse levels: zero emits null and consumes nothing; the next two ones consume 4 and 5; zero emits null; final one consumes 6. The logical result is `(null,4,5,null,6)`.

The consumption invariant is number of encoded values equals count of levels at maximum: three equals three. The value cursor must finish exactly at length three. Too few values means truncation; extras mean levels/schema/page metadata disagree.

### Answer 3

Use the standard three-level LIST annotation: optional outer list group, repeated middle `list` group and optional UTF-8 `element`. The outer optionality distinguishes null list; repetition plus levels distinguishes an empty present list; optional element distinguishes a null element; UTF-8 byte-array length zero represents present empty string.

Create four independent records containing null, `[]`, `[null]` and `['']`. Record expected definition/repetition level sequences from a trusted writer, inspect them, and cross-read with every supported implementation. Compare logical states, leaf value consumption, row counts and round trips; do not rely on printed output that might display null/empty similarly.

### Answer 4

Collect representative width, null, cardinality and time-order distributions. Hold schema/codec constant while varying byte-targeted file, row-group and page sizes across a matrix. Generate at least ordered and realistically late/skewed inputs. Run full scans, common two-minute-window queries, wider ranges and point-like queries with five-field projection.

Measure write buffering/latency, object count, footer and range requests, request cost, compressed bytes, candidate/read bytes, page/row-group pruning, decode CPU, peak memory, parallel task balance and end-to-end freshness. Compare page indexes on/off and likely codecs/encodings. Repeat under concurrency and cold caches. Choose a Pareto point meeting two-minute publication while avoiding tiny files; document hardware, library versions and confidence ranges.

### Answer 5

Never mutate old files or reinterpret their existing decimal. Add a new semantically named `(18,6)` field and define exact conversion from unscaled `(12,2)`: multiply by `10^4` only when the unit is truly unchanged. Reject overflow and any case requiring unapproved rounding; retain provenance and old value.

Read one immutable source snapshot, write byte-bounded sorted outputs to a new hidden generation, and give every source row a stable identity. Validate files with independent readers, schemas, level/value counts and non-pruned query baselines. Reconcile input/output row IDs, counts, partition counts, nulls, sums using exact decimals and duplicate/gap sets. Publish one manifest pointer atomically only after all checks pass. Keep old snapshot and object mapping for rollback, prevent readers from listing both generations, observe queries, then retire old objects under retention policy.
