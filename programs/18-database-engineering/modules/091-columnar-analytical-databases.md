---
module_id: DBE-091
program: Database Engineering
level: 2
module_number: 91
title: Columnar Analytical Databases
status: complete
last_verified: 2026-09-05
---

# Columnar Analytical Databases

## One-Page Review

### Governing question

How do columnar analytical databases turn projection-heavy scans into efficient I/O and CPU pipelines, and what ingestion, mutation, reconstruction, metadata, and operational costs accompany that advantage?

### Essential definitions

A **row store** colocates the attributes of one tuple; a **column store** colocates values from one attribute across many tuples. A **row group** or **segment** is a horizontal batch whose columns are stored separately, bounding reconstruction and metadata. **Projection pruning** reads only referenced columns. **Data skipping** uses metadata such as min/max zone maps, dictionaries, or bloom filters to reject segments without decoding rows. An **encoding** transforms values using structure—run length, dictionary, delta, frame-of-reference, bit packing—before or alongside a general **compression codec**. **Late materialization** keeps intermediate results as column vectors and row/selection identifiers until tuple reconstruction is necessary. **Vectorized execution** applies an operator to a batch, amortizing interpretation and improving cache/SIMD use. A **selection vector** identifies qualifying positions without copying every value. A **sort/cluster key** controls physical order and therefore compression and skipping. An immutable **part** is a sorted/encoded batch later compacted or merged. **Write amplification** is total physical rewriting per logical change.

### Central model, mechanism, or theorem

For N rows, a fixed-width row of W bytes, and projected columns S with widths $w_j$, an uncompressed scan lower-bound model is

$$B_{row}\approx NW,\qquad B_{col}\approx N\sum_{j\in S}w_j.$$

If compression ratios $c_j\ge1$ and only fraction $g_j$ of segments survive metadata pruning, the column bytes become approximately

$$B_{col}\approx N\sum_{j\in S}\frac{g_jw_j}{c_j},$$

plus metadata, identifiers, decompression, and reconstruction. This is a cost model, not a universal theorem: point lookups, wide projections, poorly clustered predicates, frequent small updates, tiny tables, or reconstruction-heavy queries can erase the advantage.

### Critical invariants

- Every column segment in a row group uses one row-position/visibility domain, or carries an exact mapping.
- Null bitmaps, dictionaries, offsets, and nested repetition/definition metadata decode without changing SQL null and row boundaries.
- Segment pruning has no false negatives for the predicate, collation, type, and snapshot.
- Encoded operations preserve the same comparison, overflow, decimal, timezone, and collation semantics as decoded SQL.
- Selection vectors refer only to live positions at the correct MVCC snapshot and remain aligned across projected columns.
- Sort/cluster metadata describes actual stored order; background merge cannot silently violate it.
- Immutable-part replacement is atomic and recoverable; old parts remain until no reader needs them.
- Updates/deletes and deduplication rules have an explicit visibility point rather than “eventual cleanup” semantics.
- Spill, exchange, cache, and temporary column data retain type, encryption, ownership, and row identity.
- Benchmarks include ingestion, merge/compaction, concurrency, recovery, and correctness—not scan throughput alone.

### Common failures

Failures include calling a file columnar because fields are listed separately; reading every column despite projection pruning; using min/max metadata with incompatible collation; applying dictionary IDs from different dictionaries as values; losing nulls during vector operations; averaging partition averages; reconstructing wide rows too early; choosing a sort key from one demonstration query; creating too many tiny parts; forcing compaction during peak load; treating merge-time deduplication as immediate uniqueness; performing point updates that rewrite large segments; benchmarking hot compressed data only; ignoring spill/network bytes; and assuming compression ratio predicts query latency.

### Compact example

A billion-row fact table has eight 8-byte columns. A query reads two columns. The simplified row-store scan is 64 GB; column projection is 16 GB before compression. If each chosen column compresses 4:1 and zone maps skip 75% of segments, the estimate is 1 GB plus metadata/decompression. But `SELECT *` removes projection benefit, random point lookup may need segment location and reconstruction, and an update can rewrite an immutable block much larger than one row.

### Connections

Retrieve [Vectorized and Pipeline Execution](059-vectorized-and-pipeline-execution.md), [External Sorting and Spilling](057-external-sorting-and-spilling.md), and [Sharding and Data Placement](086-sharding-and-data-placement.md). Continue through [the program roadmap](../ROADMAP.md) to LSM key-value stores and other specialized engines.

## Governing Question

Analytical queries often scan many rows while touching few attributes: group revenue by region, filter timestamps and status, aggregate a measure. A row layout fetches unrelated attributes with each qualifying tuple. A column layout can read only needed streams, encode similar adjacent values densely, and evaluate predicates over CPU-friendly batches.

The design is not “transpose the table.” A usable analytical engine must preserve tuple identity, null/nested semantics, snapshots, joins, ordering, mutation visibility, and recovery while data is split into segments, encoded, compacted, and processed without reconstructing rows. The physical design moves cost from reads into ingestion, metadata, background rewriting, and difficult point mutation.

## Why This Matters

Columnar storage underlies data warehouses, MPP analytical databases, lakehouse file formats, embedded analytics, and column indexes inside hybrid systems. Its wins come from a chain: projection and segment pruning reduce bytes; encoding improves compression; vectorized/compiled execution reduces per-value overhead; late materialization delays copying; parallel fragments use partitions.

Breaking any link can dominate. Poor sort keys prevent skipping, high-cardinality strings defeat naive dictionaries, tiny parts inflate metadata and seeks, skew leaves one worker slow, and update/delete semantics force expensive merges. Engineers must measure the real workload rather than infer “OLAP means columnar.”

C-Store, MonetDB/X100, modern column-store research, Dremel, Parquet, Snowflake, and production engines demonstrate different choices. Current DuckDB execution-format and ClickHouse MergeTree/storage documentation were checked on 2026-09-05. Their mutable defaults and implementation details are examples, not universal column-store laws.

## Prerequisites and Retrieval

Retrieve these ideas:

- relational results use rows and SQL semantics even when physical data is columnar;
- pages, blocks, buffers, compression, checksums, and writeback define physical evidence;
- projection pruning and predicate pushdown must follow equivalence rules;
- vectorized pipelines balance batch overhead, cache locality, branch behavior, and blocking operators;
- external sort, hash aggregation, and join can spill;
- MVCC snapshots require version visibility and garbage-collection horizons;
- sort order and partitioning affect zone-map selectivity and distributed locality;
- immutable files/parts simplify readers but move work to compaction and replacement;
- statistics and cardinality estimates choose scan/join/exchange strategies;
- durability and backup require a recoverable catalog-to-data cut.

This chapter focuses on analytical relational engines. It does not claim all columnar systems share one storage format, transaction model, or update policy.

## Learning Objectives

After completing this module, you should be able to:

1. compare row, pure-column, and row-group/hybrid layouts from workload evidence;
2. derive projection, compression, and segment-skipping cost estimates;
3. explain dictionary, run-length, delta, bit-packed, and general compression trade-offs;
4. trace vectorized predicate, selection, aggregation, and late materialization paths;
5. preserve row identity, null, nested, collation, numeric, and snapshot semantics;
6. design sort keys, row groups, parts, ingestion, mutation, and compaction policies;
7. diagnose skew, tiny parts, wide reconstruction, spill, and background-work interference;
8. validate an analytical engine with semantic oracles and complete production workloads.

## Core Exposition

**Start with access shape.** Row layout is strong when operations fetch or update most attributes of a few tuples: primary-key OLTP, short record writes, and locality within one row. Column layout is strong when operations scan many tuples, reference a small subset of attributes, aggregate, and benefit from repeated/sorted values. Hybrid systems use row groups: tuples are partitioned horizontally, then each group's attributes are column streams. This bounds metadata, parallel tasks, seeks, and reconstruction.

Physical design is workload-specific. Count projected bytes, predicate columns, selectivity, point access, joins, concurrency, ingestion order, mutation rate, retention, and service-level tails. A narrow table offers little projection savings. A query selecting most columns can turn column storage into many streams plus reconstruction.

**Preserve row identity.** Columns from one row group normally align by ordinal position. Position 17 in each live column belongs to the same logical row. Deletes, updates, dictionary changes, and late materialization must not shift one stream independently. Systems use delete bitmaps, row IDs, version columns, position lists, or replacement parts while preserving a mapping.

Variable-length values need offsets and payload buffers; nulls need validity metadata distinct from empty/zero. Nested values require repetition/definition levels or offset/validity structures that reconstruct lists and structs exactly. Predicate evaluation over child streams must retain parent row boundaries.

**Prune columns and segments.** The planner resolves all columns needed for predicates, joins, grouping, ordering, projection, visibility, and expression evaluation. Only then can it prune unused physical streams. A column used only by a filter is still needed until the selection is known; it need not be carried afterward.

Per-segment metadata may include min/max, null count, distinct estimates, dictionaries, bloom filters, and sort position. To skip a segment, the metadata must prove no row can satisfy the predicate. For `x=7`, min=10 can safely skip under compatible numeric semantics. For locale-sensitive strings, truncated bounds, NaN, timestamps, casts, or functions, the proof is more subtle. False positives cost reads; false negatives lose correct results and are forbidden.

**Choose row-group size deliberately.** Large groups improve compression, sequential I/O, and metadata amortization but make selective reads and mutation rewrites coarser. Small groups improve pruning/task granularity but create metadata, seek, scheduling, and tiny-file/part overhead. Align group decisions with storage latency, object-store range requests, cache, vector size, partition keys, and common predicates.

A row group is not a transaction boundary by default. Multiple groups may form one part/file, and one query snapshot may span many versions. Do not infer atomic visibility from physical grouping.

**Encode before general compression.** Run-length encoding stores `(value,count)` and excels on long runs created by sorting. Dictionary encoding maps repeated values to compact IDs; local dictionaries bound size but IDs from different segments are not comparable unless dictionaries/order mappings are reconciled. Delta/frame-of-reference encoding stores differences from previous/minimum values, useful for ordered timestamps or clustered integers. Bit packing uses only the width required by a bounded range. Boolean/null streams can use bitmaps.

General codecs exploit byte patterns after encoding. Compression saves I/O, cache, and network but costs CPU and can impede random access. Seek points/block indexes bound how much must be decompressed. Select codecs and levels from end-to-end latency and resource budgets, not compression ratio alone.

**Operate on encoded data when safe.** Equality against a dictionary can translate the literal once to an ID; run-length aggregation can multiply by run count; frame-of-reference comparisons can adjust the predicate. This avoids full decode. The operation is valid only when encoding preserves relevant semantics. Segment-local dictionary ID 3 does not globally sort before ID 4; dictionary order, collation, nulls, and unknown literals matter.

Encoded execution has combinatorial complexity. Engines often expose a unified vector abstraction or decode selected blocks to a canonical vector. Measure specialization benefit against code paths, branch cost, and correctness surface.

**Vectorize execution.** Tuple-at-a-time interpretation invokes operator logic per row and often incurs branches, virtual calls, and poor instruction locality. Vectorized execution processes batches of homogeneous values, amortizes dispatch, uses tight loops, enables SIMD/autovectorization, and improves prefetch/cache behavior. Batch size balances overhead against cache footprint, latency, and selection density.

A vector carries data, validity, type, and sometimes representation (flat, constant, dictionary, sequence). A selection vector lists qualifying row positions. Downstream operators process selected positions without copying every column. Dense filters may use bitmasks; sparse filters may favor index arrays. Null masks participate in SQL three-valued logic.

**Materialize late.** Evaluate selective predicates on narrow columns, propagate row/position IDs, then fetch payload columns for survivors. This reduces memory traffic and copying. But repeated random fetches from many columns can destroy locality, and joins can require stable tuple identifiers across reordered intermediates. Early materialization can win for wide outputs, high selectivity, or operators optimized for contiguous tuples.

Materialization is a plan choice. Track bytes and cache misses at each boundary instead of declaring late universally superior.

**Exploit physical order.** Sorting/clustering adjacent rows by common filter/group/join keys increases run-length/delta compression and makes min/max pruning selective. A compound key helps predicates on its leading order; later columns gain within-prefix clustering. Low-cardinality first keys can create long runs but poor pruning for other filters. High-cardinality timestamps can support range pruning but concentrate ingestion.

No one order serves every workload. C-Store-style projections, materialized views, secondary indexes, partitioning, or redundant clustering trade storage/refresh cost for access paths. Choose from query frequency, bytes saved, freshness, and maintenance budget.

**Design ingestion and parts.** Batch ingestion can sort, encode, and write immutable parts atomically, with catalog metadata published after durable data. Streaming micro-batches reduce freshness delay but can create thousands of tiny parts. Buffer or compact them while bounding visibility latency and crash loss.

Background merge reads parts, resolves engine-specific version/delete rules, re-sorts, re-encodes, and atomically replaces inputs. It consumes disk bandwidth, CPU, memory, cache, and temporary space. Rate-limit and admission-control merges without starving them; unchecked part accumulation eventually harms queries and ingestion.

**Make mutation semantics explicit.** In-place point update of one value can break compression and require rewriting a segment. Designs append a new version/delta, mark delete, maintain a write-optimized store, or rewrite affected parts. Readers merge base and delta under a snapshot. Deletes remain as tombstones/bitmaps until safe compaction.

“Deduplicates during merge” is not a uniqueness guarantee at insert time. Queries may need an explicit finalization path that costs more. State whether repeated keys coexist, which version wins, how ties resolve, and when every read observes the result. Frequent random updates may justify a row store or hybrid delta architecture.

**Integrate MVCC and transactions.** Analytical snapshots should see one catalog/schema/data version. Immutable parts simplify snapshot retention, but new/removed part manifests and delete/update deltas require transactional publication. Long queries retain old parts and inflate storage. Compaction cannot delete them until no snapshot, backup, follower, or recovery path needs them.

Write paths may optimize bulk atomic publish rather than row transactions. Do not assume a columnar engine provides full OLTP constraints, isolation, or immediate secondary-index maintenance. Evaluate advertised semantics directly.

**Scale through MPP execution.** Partition data across nodes, place scan fragments near parts, perform partial aggregation, repartition join keys, broadcast small dimensions, and merge final results. Columnar batches reduce network bytes and serialize efficiently, but skew can leave one partition or group dominant. Compress exchanges only when network savings exceed CPU/latency.

Distributed `ORDER BY`, window functions, exact distinct, and skewed joins are blocking or shuffle-heavy. Track exchange bytes, spill, per-worker rows, slowest task, and retry semantics. A failed fragment must not duplicate aggregate inputs or publish partial result.

**Manage memory and spill.** Scans allocate compressed input, decoded vectors, selection arrays, hash tables, and output buffers. Joins/aggregations can exceed memory despite narrow scans. Use per-query/tenant limits, partitioned spill, bounded queues, and backpressure. Spill formats preserve types, nulls, collation, encryption, checksum, and attempt ownership.

Memory accounting must include dictionaries, decompression workspaces, object-store buffers, network exchange, JIT code, and background merge. Operator reservations that ignore shared cache/background work cause process-wide failure.

**Observe physical effectiveness.** Measure bytes eligible/read/decompressed, columns projected, segments skipped by reason, compression by column/encoding, rows scanned/selected/materialized, vector utilization, CPU cycles/cache misses, exchange/spill, part count/size, merge backlog/amplification, delete/update debt, snapshot age, cache hit, object-store requests, and tail latency.

Explain why segments were not skipped: unsorted data, function-wrapped predicate, stale/missing metadata, broad range, cast/collation, or planner limitation. Compression ratio alone cannot identify the bottleneck.

**Validate correctness and performance together.** Generate tables with nulls, NaN/infinity, decimal boundaries, timezone transitions, collations, duplicates, empty/all-null/constant columns, high/low cardinality, long runs, nested empty/null containers, and variable strings. Compare results with a trusted reference engine and row layout across filters, joins, groups, windows, order/limit, updates/deletes, concurrent snapshots, and retries.

Corrupt/truncate blocks and metadata; crash before/after part/catalog publication and merge replacement; exhaust disk during rewrite; overlap backup, long snapshot, schema change, ingest, and merge. Verify checksums, atomic visibility, no lost/duplicate rows, exact aggregates, and recoverable old/new part selection. Benchmark cold/warm cache, realistic concurrency/skew, ingestion plus merges, spill, node loss, and recovery—not only one hot scan.

The finite executable example below models aligned columns, row-group zone/dictionary pruning, a selection, and aggregation. It is not a storage engine, compression codec, SQL implementation, optimizer, MVCC system, distributed executor, or performance benchmark.

<!-- bijux-verify: {"id":"finite-columnar-scan","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"row_groups=3\ngroups_scanned=2\ngroups_skipped=1\nrows_examined=8\nmatching_rows=3\namount_sum=490\nprojected_columns=2\nevidence=finite_columnar_scan\n","stderr":""}} -->
```python
countries = ["SE", "US", "DE", "FR", "JP", "US", "SE", "NO", "US", "BR", "IN", "ZA"]
amounts = [120, 80, 200, 50, 500, 130, 20, 170, 60, 110, 90, 140]
eu = {"SE", "DE", "FR", "NO"}
group_size = 4
groups_scanned = rows_examined = 0
selected = []

for start in range(0, len(countries), group_size):
    end = start + group_size
    country_dictionary = set(countries[start:end])
    maximum_amount = max(amounts[start:end])
    if not (country_dictionary & eu) or maximum_amount < 100:
        continue
    groups_scanned += 1
    rows_examined += end - start
    selected.extend(
        i for i in range(start, end)
        if countries[i] in eu and amounts[i] >= 100
    )

print(f"row_groups={len(countries) // group_size}")
print(f"groups_scanned={groups_scanned}")
print(f"groups_skipped={len(countries) // group_size - groups_scanned}")
print(f"rows_examined={rows_examined}")
print(f"matching_rows={len(selected)}")
print(f"amount_sum={sum(amounts[i] for i in selected)}")
print("projected_columns=2")
print("evidence=finite_columnar_scan")
```

## Definitions and Notation

- **Column segment:** one attribute's values for a bounded horizontal row range.
- **Row group:** aligned set of column segments covering the same logical row positions.
- **Part:** immutable physical batch containing one or more groups plus metadata.
- **Zone map:** conservative per-segment bounds used to prove predicate impossibility.
- **Dictionary / RLE / delta / bit packing:** repeated-value ID, run, difference, and bounded-width encodings.
- **Projection pruning:** excluding unreferenced physical columns from the scan.
- **Selection vector:** positions surviving predicates without immediate tuple copying.
- **Late materialization:** delaying payload fetch and row reconstruction until after selective work.
- **Vectorized execution:** applying operators to typed batches.
- **Cluster key:** physical order chosen for pruning, compression, and locality.
- **Merge/compaction:** background replacement of parts to restore organization or resolve deltas.
- **Write amplification:** bytes rewritten divided by logical bytes changed/ingested.

## Mechanisms, Invariants, or Proof Structure

**Projection cost derivation.** With fixed-width row W, scanning N uncompressed rows reads about NW. Reading selected column widths sums to $N\sum w_j$. Compression and pruning scale each stream by approximately $g_j/c_j$, subject to block granularity and metadata/decode overhead. The estimate predicts bytes, not latency by itself.

**Safe-pruning proof.** Let metadata interval [m,M] conservatively contain every non-null segment value under the predicate's comparison semantics. If query interval Q is disjoint from [m,M], no stored value satisfies Q, so skipping has no false negative. Incorrect/truncated bounds, casts, collation, NaN, or stale metadata can violate the premise.

**Alignment invariant.** For row group G and live position i, every projected column lookup $C_j[i]$ must refer to one logical tuple, after applying the same snapshot/delete mapping. Induction through selection-vector filtering preserves alignment because it removes positions rather than independently rearranging columns.

**Merge visibility.** If readers choose either complete old part set O or complete replacement set N through one atomic manifest/catalog version, and O remains retained for old snapshots, no reader observes a partial replacement. Deleting O before all readers release it breaks the premise.

**Encoding equivalence.** An encoded predicate/aggregate is valid only when decoding after the encoded operation yields the same SQL result as operating on decoded values, including null, collation, overflow, and type rules. Testing common values alone cannot establish equivalence.

## Alternatives and Trade-Offs

| Design | Benefit | Cost or limitation | Evidence |
| --- | --- | --- | --- |
| Row store | point access/update and full-row locality | reads unused attributes in broad scans | workload bytes/latency |
| Pure column layout | maximal projection/compression opportunity | reconstruction and many streams | scan/reconstruction tests |
| Row-group columnar | bounded parallel/pruning/reconstruction unit | size tuning and metadata | group-size sweep |
| Dictionary encoding | compact repeated strings, encoded equality | cardinality/dictionary rebuild and local IDs | distribution/cardinality |
| RLE | excellent sorted low-cardinality runs | poor on alternating/random data | run statistics |
| Delta + bit packing | compact clustered numbers/timestamps | exceptions/random access complexity | range/delta evidence |
| Late materialization | less payload copying after selective filters | scattered gathers, ID propagation | selectivity sweep |
| Immutable parts | atomic readers and bulk encoding | merge debt and update amplification | ingest/merge balance |
| Write-optimized delta | fresher small writes | read merge and compaction | mixed workload test |
| Multiple projections/orders | more query-local layouts | storage and refresh cost | workload portfolio |

## Failure Modes and Misconceptions

- **“Columnar means one file per column.”** Many engines group rows and store streams/blocks within parts/files.
- **“Column stores are always faster.”** Point access, wide projection, updates, and tiny data may favor rows.
- **“Compression ratio equals performance.”** decode CPU, skipping, cache, network, and operators determine latency.
- **“Zone maps are approximate filters.”** False positives are acceptable; false negatives are correctness bugs.
- **“Dictionary IDs are values.”** Segment-local IDs may have unrelated meaning/order.
- **“Null is an empty value.”** Validity must remain separate through every vector operation.
- **“Vectorization is SIMD.”** Batching enables but does not guarantee SIMD; it also amortizes dispatch.
- **“Late materialization always wins.”** high selectivity or scattered gathers can make early rows cheaper.
- **“Sort key is a primary-key uniqueness constraint.”** Physical order and logical uniqueness are separate.
- **“Merge-time dedup is immediate.”** duplicate visibility depends on query/finalization semantics.
- **“Small batches maximize freshness for free.”** tiny parts move cost into metadata and compaction.
- **“Immutable means no transactions.”** catalog publication and snapshots still require atomicity/isolation.
- **“Analytical queries cannot harm ingestion.”** scans, spill, and merges contend for shared resources.
- **“A TPC query proves production fitness.”** concurrency, mutations, failures, recovery, and real data shape remain.

## Worked Examples

### Example 1

**Situation.** One billion rows contain eight 8-byte columns; a scan reads two.

**Reasoning.** The simplified row bytes are $10^9\times64=64$ GB. Column projection is $10^9\times16=16$ GB before compression. At 4:1 compression and 25% surviving groups, estimated column bytes are 1 GB plus overhead.

**Conclusion.** Projection, compression, and pruning multiply, but only under their premises.

### Example 2

**Situation.** A segment has numeric min=10,max=20 and predicate `x BETWEEN 30 AND 40`.

**Reasoning.** Intervals are disjoint, so no non-null value can match; skip safely. For predicate `CAST(x AS text) LIKE '1%'`, numeric bounds do not prove impossibility.

**Conclusion.** Metadata pruning is a semantic proof for one predicate, not a hint.

### Example 3

**Situation.** Segment A dictionary maps ID 1 to `SE`; segment B maps ID 1 to `US`.

**Reasoning.** Comparing IDs across segments reports equality incorrectly. Translate literals within each dictionary or unify dictionaries with explicit remapping; sorting IDs requires order-preserving dictionary semantics.

**Conclusion.** Encoded operations must respect dictionary scope.

### Example 4

**Situation.** Values `[A,A,A,A,B,B]` use RLE versus alternating `[A,B,A,B,A,B]`.

**Reasoning.** The first needs two `(value,count)` runs; the second needs six, potentially larger than compact raw IDs. Sorting on the attribute can create runs but changes locality for other predicates.

**Conclusion.** Encoding effectiveness depends on physical order and distribution.

### Example 5

**Situation.** A predicate selects positions `[2,9,11]` from 1,024 rows and output needs a large text payload.

**Reasoning.** Carrying a selection vector and fetching three payloads avoids decoding/copying 1,021 values. If 1,000 rows survive, scattered late gathers may cost more than one contiguous early decode.

**Conclusion.** Materialization timing should respond to selectivity and layout.

### Example 6

**Situation.** Two partitions contain averages 10 over 100 rows and 100 over one row.

**Reasoning.** Averaging partial averages gives 55, which is wrong. Merge `(sum,count)` to get $1100/101\approx10.891$.

**Conclusion.** Distributed/vector partial states must be algebraically sufficient.

### Example 7

**Situation.** Streaming ingestion creates one 100-row part per second while merges can consolidate only half that byte rate.

**Reasoning.** Backlog and part count grow without bound, increasing metadata, opens, seeks, and planning. Batch or buffer inserts, raise safe merge capacity, or reduce incoming rewrite work; forcing a huge merge can worsen overload.

**Conclusion.** Sustainable ingestion requires background write capacity at least matching long-run work.

### Example 8

**Situation.** An engine appends two versions for a key and promises deduplication during merge.

**Reasoning.** Before merge, ordinary scans may see both unless read semantics select a winner. Tie/version order, snapshot visibility, and `FINAL`-like paths must be defined. Physical convergence later is not immediate uniqueness.

**Conclusion.** Merge semantics and query guarantees are different contracts.

### Example 9

**Situation.** A long snapshot reads old parts while compaction publishes replacements.

**Reasoning.** Atomically publish the new part manifest for new snapshots, keep old parts pinned for the long reader, and reclaim only after its horizon passes. Mixing half old/half new can duplicate or omit rows.

**Conclusion.** Immutable replacement needs snapshot-aware catalog atomicity.

### Example 10

**Situation.** A distributed group-by hashes one dominant customer to one worker.

**Reasoning.** Total bytes and average worker load look healthy, but the hot worker spills and determines tail latency. Use heavy-hitter detection, salted partial aggregation with a final combine, or workload-aware partitioning while preserving group semantics.

**Conclusion.** MPP columnar speed remains limited by skew and the slowest stage.

## Cross-Program Connections

- Data Engineering owns ingestion pipelines and file/table lifecycle; Database Engineering owns scan, transaction, and storage-engine semantics.
- Data Architecture Engineering owns analytical models, retention, semantic measures, and workload-derived clustering choices.
- Algorithm Engineering owns compression, hashing, sorting, joins, aggregation, SIMD-friendly loops, and skew algorithms.
- Operating Systems owns page cache, direct I/O, mmap, scheduling, NUMA, device behavior, and durability beneath parts.
- Platform Engineering owns object-store/network capacity, workload isolation, observability, and automated maintenance.
- Security Engineering owns encryption, temporary/spill confidentiality, tenant isolation, and safe metadata exposure.

## References

1. Mike Stonebraker et al. [C-Store: A Column-oriented DBMS](https://www.vldb.org/conf/2005/papers/p553-stonebraker.pdf). VLDB, 2005. Columnar projections, compression, execution, and update architecture.
2. Daniel Abadi, Samuel Madden, and Nabil Hachem. [Column-Stores vs. Row-Stores: How Different Are They Really?](https://www.cs.umd.edu/~abadi/papers/abadi-sigmod08.pdf). SIGMOD, 2008. Decomposition of column-store performance mechanisms.
3. Peter Boncz, Marcin Żukowski, and Niels Nes. [MonetDB/X100: Hyper-Pipelining Query Execution](https://www.cidrdb.org/cidr2005/papers/P19.pdf). CIDR, 2005. CPU-conscious vectorized execution.
4. Daniel Abadi, Peter Boncz, and Stavros Harizopoulos. [Column-Oriented Database Systems](https://doi.org/10.14778/1687627.1687629). PVLDB 2(2), 2009. Column-store design survey.
5. Sergey Melnik et al. [Dremel: Interactive Analysis of Web-Scale Datasets](https://research.google/pubs/dremel-interactive-analysis-of-web-scale-datasets-2/). PVLDB 3, 2010. Nested columnar representation and serving tree.
6. Apache Parquet. [File Format Specification](https://github.com/apache/parquet-format). Current encoding, row-group, page, statistics, and nested-data specification checked 2026-09-05.
7. Benoit Dageville et al. [The Snowflake Elastic Data Warehouse](https://www.snowflake.com/wp-content/uploads/2016/06/Snowflake_SIGMOD.pdf). SIGMOD, 2016. Immutable columnar storage and cloud architecture.
8. Andrew Lamb et al. [The Vertica Analytic Database: C-Store 7 Years Later](https://www.vldb.org/pvldb/vol5/p1790_andrewlamb_vldb2012.pdf). PVLDB 5(12), 2012. Production column-store evolution.
9. DuckDB. [Execution Format](https://duckdb.org/docs/current/internals/vector). Current vector/data-chunk representations checked 2026-09-05.
10. ClickHouse. [MergeTree Table Engine](https://clickhouse.com/docs/engines/table-engines/mergetree-family/mergetree). Current parts, sorting, granules, marks, merges, and storage behavior checked 2026-09-05.

## Exercises

### Exercise 1

Distinguish column projection, segment pruning, encoding, general compression, vectorization, and late materialization. Give one failure mode for each.

### Exercise 2

A 500-million-row table has fixed row width 120 bytes. A query needs columns of widths 8, 4, and 16 bytes. Their compression ratios are 4, 2, and 8, and 20% of groups survive for all three. Estimate row and column bytes under the chapter model, then list omitted costs.

### Exercise 3

An engine compares local dictionary IDs across parts, drops null masks after filtering, retries scan fragments without sequence identity, and deletes old parts immediately after compaction publication. Diagnose the correctness failures and specify minimum repairs.

### Exercise 4

Compare a row store, row-group column store with immutable parts, and hybrid row-plus-column/delta design for operational dashboards with continuous ingestion, corrections, point lookup, and hourly broad aggregation.

### Exercise 5

Design and validate a production columnar analytical table for multi-tenant events. Include schema/types, partition/sort key, row groups, encodings, ingestion, updates/deletes, MVCC, compaction, distributed execution, resource isolation, security, observability, recovery, and benchmarks.

## Answers to the Exercises

### Answer 1

**Projection pruning** avoids reading unreferenced columns; hidden expression/visibility columns can make pruning incomplete. **Segment pruning** proves a block cannot match from metadata; wrong collation, stale/truncated bounds, or NaN semantics can create false negatives. **Encoding** exploits data structure such as dictionaries/runs/deltas; local dictionary IDs can be miscompared. **General compression** exploits byte redundancy; excessive decode CPU/random-access granularity can outweigh I/O savings. **Vectorization** processes batches to amortize dispatch/cache work; bad batch size or sparse selection can waste work. **Late materialization** carries positions then fetches payloads; high selectivity or scattered gathers can make it slower and unstable IDs can join wrong columns.

### Answer 2

Row bytes are $500\times10^6\times120=60$ GB. Column bytes are

$$500\times10^6\times0.2\times(8/4+4/2+16/8)$$

$$=100\times10^6\times(2+2+2)=600\text{ MB}.$$

This decimal-byte estimate omits metadata, null/offset/index streams, block rounding, footer/object requests, unprunable visibility columns, decompression CPU/workspace, cache, network, selection vectors, reconstruction, other operators, spill, concurrency, and imperfect shared pruning. It predicts neither end-to-end latency nor update cost.

### Answer 3

Local dictionary ID 1 can mean different values or sort orders across parts, corrupting comparison/join/group results. Translate literals and comparisons inside each dictionary or remap to a global/value representation with explicit collation. Dropping null masks turns SQL unknown into arbitrary values; every vector/selection/operator must propagate validity and three-valued logic.

Unidentified fragment retry can duplicate batches, rows, and aggregate inputs or race the old attempt. Tag query/fragment/attempt plus ordered batch sequence, fence cancellation, and deduplicate or restart from a clean stage checkpoint at one snapshot. Immediate old-part deletion breaks long readers, backups, and failed installations. Publish one atomic manifest version, pin old parts through every snapshot/recovery horizon, verify the replacement, and reclaim only after reference/epoch safety. Fault-test crashes around publication and retry.

### Answer 4

A **row store** gives efficient point lookup and corrections with familiar OLTP transactions, but hourly wide-row scans read unused fields and may disturb operational buffers. It fits when dashboards are selective/indexed and aggregation volume is moderate. A **row-group immutable column store** gives projection, compression, zone-map pruning, and batch/vector execution for hourly scans and append-heavy events; continuous tiny inserts and corrections create part/merge/delete debt, and point lookup may read metadata plus several streams.

A **hybrid** keeps fresh/corrected rows in a write-optimized delta and periodically merges them into columnar base. Dashboards merge base and delta at one snapshot; point lookups consult both. It balances freshness and scan speed but adds duplicate/version resolution, two optimizers/access paths, compaction, and recovery complexity. Recommend hybrid only if measured correction/lookup needs materially hurt immutable columnar ingestion and the team can prove/read-observe base-plus-delta semantics. Otherwise batch inserts into columnar groups and provide a separate indexed serving projection for point access.

### Answer 5

Use typed tenant, event time, event ID, event kind, dimensions, numeric measures, and payload fields with exact decimal/timezone/null semantics. Partition primarily by governed time/tenant granularity for pruning, retention, and residency without tiny tenants; sort by tenant, common time range, and selected filter/group keys based on workload. Choose row-group size by object requests, pruning, compression, task parallelism, and correction rewrite experiments.

Apply dictionary/RLE to measured repeated columns, delta/bit packing to clustered time/numbers, and codecs per column from end-to-end tests. Batch/micro-batch ingestion into checksummed sorted immutable parts; publish catalog atomically. Give every event stable identity. Represent corrections/deletes as versioned deltas/tombstones with defined snapshot winner and immediate query semantics; merge them in background. Retain old parts for active MVCC snapshots, backups, replicas, and recovery.

Push projection/predicates safely, propagate selection/validity/row IDs, materialize payload late when selective, and use partial/final aggregates with sufficient state. Partition MPP fragments near data; mitigate heavy tenants with subpartitioning or salted partial aggregation. Bound query memory, exchange, spill, object requests, parts, and merge bandwidth per tenant; reserve ingestion/recovery capacity. Encrypt data, metadata, exchange, spill, and backups; enforce tenant predicates/authorization below pruning and protect trace values.

Observe eligible/read/decompressed bytes, projected columns, skipped groups/reasons, compression/encoding, rows selected/materialized, vector occupancy, cache/CPU, exchange/spill, part count/size, merge backlog/amplification, tombstone/version debt, snapshot pins, ingestion freshness, per-tenant tails, and errors. Recover catalog and parts to one verified cut; test corruption, incomplete upload, publication/merge crashes, full disk, lost node/region, restore, and version upgrade.

Compare to a trusted row/reference engine using generated null, numeric, collation, timestamp, nested, duplicate, update/delete, join, group, window, and order cases. Benchmark cold/warm scans, point reads, mixed ingestion/correction/query concurrency, key skew, high/low cardinality, tiny/large parts, compaction, spill, failure, repair, and long snapshots. Report versions, dataset/distributions, configuration, all percentiles, correctness outcomes, and finite limitations.
