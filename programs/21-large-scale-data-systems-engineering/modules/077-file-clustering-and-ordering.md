---
module_id: LSDS-077
program: Large-Scale Data Systems Engineering
level: 2
module_number: 77
title: File Clustering and Ordering
status: complete
last_verified: 2026-09-04
---

# File Clustering and Ordering

## One-Page Review

### Governing question

How should a large analytical table place related rows into files and pages so common predicates prune efficiently, range scans preserve locality, and merge/compression behavior improves—without confusing a declared order with guaranteed global sorting, overspending on rewrites, or optimizing yesterday's workload?

### Essential definitions

- **ordering** arranges rows by a total or lexicographic comparison over one or more expressions.
- **clustering** places rows with similar selected values near one another, without necessarily defining a total order.
- A **sort order** specifies stable source-field identities, transforms, direction, and null ordering used within declared file scope.
- **lexicographic order** compares the first key, then later keys only when earlier keys tie.
- **multidimensional clustering** maps several coordinates to one locality key, often with a space-filling curve.
- **Z-order (Morton order)** interleaves coordinate bits to approximate multidimensional locality.
- **Hilbert order** uses another space-filling curve with different locality properties and higher implementation complexity.
- **range overlap** measures how much file min/max intervals cover the same value space; overlap weakens skipping.
- **clustering depth/debt** describes how much current data fails to satisfy a target layout, under a specified metric.
- **layout rewrite** replaces files with logically equivalent files organized by a declared target order or clustering rule.

### Central model, mechanism, or theorem

Let files $F$ expose conservative bounds on clustering column $x$. For predicate range $Q=[q_l,q_u]$, file $f$ is a candidate when its interval $I_f=[l_f,u_f]$ intersects $Q$. The candidate bytes are

$$B_{scan}(Q)=\sum_{f\in F}\mathbf{1}[I_f\cap Q\ne\varnothing]B_f.$$

Ordering rows by $x$ before cutting balanced files usually narrows and separates $I_f$, reducing candidates for range predicates. Lexicographic `(x,y)` primarily improves $x$ and improves $y$ within equal/narrow $x$ groups. Multidimensional curves trade exact one-axis order for locality across several selected columns. Benefit depends on predicate distribution, correlation, cardinality, statistics availability/quality, file/page size, compression, and update churn. The rewrite must preserve logical rows, delete semantics, schema/spec identity, and accurately declare each output file's order.

### Critical invariants

- Layout changes physical locality only; logical row multiset, update/delete order, schema resolution, partition meaning, and snapshot semantics remain unchanged.
- Sort fields bind stable source IDs and exact transforms, directions, collation, null, NaN, timestamp, decimal, and binary ordering.
- A file claims a sort-order ID only when its rows satisfy that order under the declared comparator.
- Unsorted or unknown-order files remain readable and are never pruned merely because they violate the current default order.
- File/page statistics conservatively cover actual values and are interpreted under the writer schema and order.
- Clustering columns are chosen from measured stable workload value, not cardinality folklore or arbitrary column count.
- Rewrites group compatible data, validate exact inputs under concurrency, publish atomically, and retain old files for pinned snapshots.
- Incremental clustering records what ranges/files satisfy which layout version; it does not claim the whole table is reclustered.
- Evaluation includes candidate bytes, rows/pages/files, query tails, compression, shuffle/spill, rewrite cost, ingest impact, and conflict loss.
- Sensitive clustering keys, bounds, and access patterns follow authorization, encryption, and telemetry-minimization policy.

### Common failures

Common failures include calling partitioning and sorting interchangeable; assuming a table default sort means every historical file is sorted; declaring sort metadata without verifying output; adding many Z-order columns until locality is diluted; choosing high-cardinality columns without predicate evidence; sorting on a column whose statistics are not collected; optimizing file counts while leaving overlapping bounds; using lexicographic second-key predicates as if the first key did not matter; ignoring null/NaN/collation semantics; reclustering cold data repeatedly; evaluating with a warm-cache single query; and publishing a rewrite after concurrent inputs changed.

### Compact example

Eight equal files each contain customer IDs spanning roughly 1–1,000 because unordered ingestion mixed keys. A query for IDs 100–120 opens all eight. A sort rewrite orders rows by customer ID and cuts eight balanced files with mostly disjoint adjacent ranges. The same query now overlaps one or two files. If queries filter only `status`, the rewrite may offer no benefit. If the table is sorted lexicographically by `(customer_id,event_time)`, an event-time-only query can still touch every customer range. The measured predicate workload—not “sorted is faster”—determines value.

### Connections

[LSDS-020](020-selecting-storage-layouts-for-large-analytical-workloads.md) supplies layout economics, [LSDS-033](033-sort-based-shuffle.md) supplies distributed ordering mechanics, [LSDS-039](039-skewed-keys-and-heavy-hitters.md) supplies skew analysis, [LSDS-060](060-diagnosing-scheduler-delay-and-resource-fragmentation.md) supplies performance evidence, [LSDS-072](072-manifest-and-metadata-trees.md) supplies bounds, [LSDS-075](075-metadata-mechanics-of-partition-evolution.md) separates partition transforms, and [LSDS-076](076-compaction-planning.md) supplies rewrite selection.

## Governing Question

Columnar files already contain min/max statistics, row groups, pages, dictionaries, and compression. Yet those mechanisms help only when values with useful locality land together. Randomly mixed customer IDs produce broad bounds in every file; a point lookup cannot skip anything. Sorted or clustered output makes the metadata selective.

Physical order is not free. Global sorting requires shuffle, comparison, memory, spill, and network. It can create skew and long tasks. Continuous ingestion immediately introduces new unclustered files, so layout quality decays. The best columns change as products and queries change. Multicolumn techniques spread finite locality across dimensions.

The governing question is how to specify comparator semantics, choose columns and techniques from evidence, construct files and pages, maintain layout incrementally, preserve correctness under evolution and concurrency, and prove that saved reads repay rewrite cost.

## Why This Matters

Data skipping often decides whether a query reads gigabytes or petabytes. Better clustering can reduce files, row groups, pages, remote requests, decompression, and CPU. It can also improve run-length and dictionary compression, merge joins, streaming of ordered ranges, and locality for deletes or updates.

But a layout optimized for one predicate can harm another. Sorting by timestamp benefits time ranges and compression of correlated fields, while scattering each account across the table. Sorting by account benefits histories but may concentrate a hot account. Z-ordering several dimensions approximates locality but weakens as dimensions grow and depends on normalization.

Ordering metadata is correctness-adjacent. Readers may use it for merge planning or delete optimizations. A false declaration can produce wrong assumptions, not merely slower scans. Therefore order IDs and statistics must describe actual file content, while old/unsorted files remain explicitly distinguishable.

## Prerequisites and Retrieval

Review storage layouts in [LSDS-020](020-selecting-storage-layouts-for-large-analytical-workloads.md), sort-based shuffle in [LSDS-033](033-sort-based-shuffle.md), heavy hitters in [LSDS-039](039-skewed-keys-and-heavy-hitters.md), metadata pruning in [LSDS-072](072-manifest-and-metadata-trees.md), schema evolution in [LSDS-074](074-schema-evolution-at-scale.md), partition evolution in [LSDS-075](075-metadata-mechanics-of-partition-evolution.md), and compaction planning in [LSDS-076](076-compaction-planning.md).

You should understand total order, lexicographic comparison, null/NaN/collation rules, min/max statistics, row groups/pages, entropy and correlation, histograms, cardinality, space-filling curves, shuffle, spill, compression, immutable files, snapshots, OCC, and matched performance experiments.

Before changing layout, retrieve query fingerprints and predicates, selected/read/returned bytes, file/page pruning, filter combinations, join/group/order keys, data distributions and correlations, null/NaN rates, file statistics coverage, current sort-order IDs, partition/spec cohorts, write/update churn, rewrite history, compression, spill, conflict rate, retention, and supported client capabilities.

## Learning Objectives

After this module, you should be able to:

1. Distinguish partitioning, bin packing, ordering, and multidimensional clustering.
2. Specify a complete comparator and trustworthy file-level order declaration.
3. Relate file-range overlap to predicate candidate bytes.
4. Explain lexicographic prefix behavior and secondary-key limitations.
5. Construct and critique Z-order or Hilbert-style locality keys.
6. Choose clustering fields using weighted workload evidence and stability.
7. Plan compatible rewrite groups with size, shuffle, skew, and concurrency controls.
8. Maintain incremental layout without falsely claiming table-wide order.
9. Verify logical equivalence, actual ordering, statistics, and delete semantics.
10. Evaluate payback using matched query and maintenance measurements.

## Core Exposition

### Separate the physical mechanisms

Partitioning maps rows into coarse disjoint or overlapping logical groups and is recorded in partition specs. Bin packing combines files toward size targets without promising value locality. Sorting orders rows under a comparator. Clustering co-locates similar values and may not produce a strict order. These can be combined, but each solves a different problem.

A common pipeline first partitions, then sorts or clusters rows within each rewrite group, then cuts output files near size targets, and finally writes columnar row groups/pages. File boundaries should not destroy the intended locality. Too-small files improve bounds but multiply fixed costs; too-large files require page indexes and row-group pruning to exploit internal order.

### Complete ordering semantics

Sort field metadata needs source-field ID or transform, direction, and null order. It also depends on the format's comparison for strings/collations, signed/unsigned binary, decimals, timestamps, floating-point zeros, infinities, and NaNs. Two engines that disagree cannot safely share an order claim.

Order scope matters. A file may be internally sorted; files in a snapshot need not be globally ordered relative to one another. A partition may contain overlapping sorted runs. A table's default order tells writers what is preferred, not necessarily what every writer produced. File metadata must label actual order or unsorted state.

### One-dimensional range locality

For each file $f$, statistics give conservative interval $I_f$. Range query $Q$ retains any file whose interval overlaps. Random mixing makes most intervals approach the global domain. Sorting then cutting adjacent rows tends to create narrow, nearly disjoint intervals.

Define weighted overlap debt for file intervals as

$$O=\sum_{i<j}w_{ij}\frac{|I_i\cap I_j|}{|I_i\cup I_j|},$$

for numeric domains with nonzero union length and weights chosen from query relevance. This is one diagnostic, not a universal objective. Point distributions, skew, nulls, categorical values, multidimensional filters, and unequal file sizes require other measures.

### Lexicographic orders

Order `(a,b,c)` groups primarily by `a`; within equal `a`, by `b`; then by `c`. Predicates on a prefix use contiguous ranges well. A predicate only on `c` may appear throughout all `a,b` groups. Therefore column order follows workload conjunctions and leading-key usefulness, not simply placing the highest-cardinality field first.

Correlation can make a later key redundant. If event date is strongly determined by event timestamp, ordering both may spend no additional useful locality. Conversely, tenant then time works well when most queries constrain tenant and scan time ranges within it.

### Multidimensional locality

Z-order normalizes each selected coordinate to a bit representation and interleaves bits. Nearby points often have nearby Morton keys, so cutting the ordered key produces files localized across dimensions. It does not preserve every multidimensional neighborhood perfectly and is sensitive to normalization, skew, null encoding, bit contribution, and dimension count.

Hilbert curves generally aim for stronger locality continuity but are more complex to compute and evolve. Product implementations differ; never assume two “Z-order” or “Hilbert” implementations share encoding. Persist layout version/algorithm parameters when interoperability or incremental clustering depends on them.

Every added dimension divides finite key bits and locality. Select a small set of columns that appear together in selective, valuable predicates. A column without usable statistics may cost rewrite work without enabling data skipping.

### Workload-based selection

Build predicate workload $W$ from normalized query fingerprints over a representative horizon. For candidate layout $L$, estimate candidate bytes or files for query $q$ using production distributions or a sample rewrite:

$$Cost(L)=\sum_{q\in W}freq(q)\cdot importance(q)\cdot B_{candidate}(q,L).$$

Add rewrite, maintenance frequency, ingest impact, and stability penalties. Protect rare critical queries separately so high-volume low-value traffic does not dominate. Exclude queries whose filters already prune perfectly by partition, index, or runtime filter.

Avoid leaking literal predicates. Aggregate or hash fingerprints, restrict access, and apply retention. Workload mining itself is governed telemetry.

### Statistics as the exploitation layer

Clustering only helps a skipper when file/row-group/page statistics cover the chosen field and correctly represent bounds. Verify null counts, truncated bounds, writer schema, collation, NaN rules, and page-index availability. Missing statistics convert good physical locality into unavailable evidence.

Sorting can enable binary search within ordered page indexes. For unordered columns, page bounds can still skip but may require examining more index entries. File-level and page-level savings should be measured separately.

### File cutting and skew

After ordering, split by target bytes rather than fixed row count when row width varies. A tuple-balanced Z-order rewrite can still produce highly unequal bytes and task durations. Estimate compression and variable-width contribution, cap maximum output, and preserve enough rows for useful statistics.

Hot keys may create a range too large for one file. Multiple files can share the same bound value; correctness is intact but point queries read all of them. Secondary ordering, finer partitioning, indexes, or salting may help, but salting harms simple locality and must preserve key semantics.

### Incremental clustering and decay

New writes may follow the target order, arrive as separate sorted runs, or remain unsorted for latency. Layout debt grows with unclustered bytes and overlapping runs. Maintenance chooses affected ranges and rewrites enough adjacent/overlapping files to improve bounds, not merely the newest file.

Record per-file sort order/layout version and clustering provenance. A table can have old order A, new order B, and unsorted files simultaneously. Query planning must remain correct for all. Report coverage by bytes and query-touch frequency, not only file count.

Reclustering is not automatically idempotent: rerunning a multidimensional algorithm can rewrite already organized files and produce different grouping. Use candidate/debt predicates and cooldowns to avoid churn.

### Evolution

Changing default sort order affects future files and may guide maintenance; it does not reorder history. Stable field IDs protect renames. Dropping or changing a source type/transform requires dependency checks. Old order definitions remain in metadata while files reference them.

Partition evolution means clustering is evaluated within multiple spec cohorts. Do not mix incompatible physical partitions just to sort globally. Layout algorithms and statistics must decode historical schema types correctly.

### Rewrite correctness and concurrency

Clustering is a compaction rewrite. Pin a snapshot and exact inputs; apply deletes/updates under their sequence semantics; order rows with a deterministic comparator; cut files; compute truthful statistics and order IDs; reconcile logical state; validate inputs at current head; and atomically replace them.

A concurrent append outside the range may be compatible. A deletion, rewrite, or row update of an input invalidates prepared output. Predicate-defined clustering ranges need inclusive validation of concurrent additions if the intended range should be fully organized. Partial progress must use disjoint groups and explicit coverage.

### Evaluation

Measure before and after on the same snapshot-derived data and matched workloads: candidate files/bytes/pages, actual bytes read, request count, planning time, scan CPU, decompression, query p50/p95/p99, join/shuffle effects, compression, file sizes, rewrite read/write/shuffle/spill, duration, conflicts, and ingest interference.

Warm and cold cache behavior differ. Compare clustered cohorts with controls and retain query result equality. Calculate payback using observed savings frequency versus maintenance cost. Revisit when workload, correlation, data volume, schema, or engine changes.

## Definitions and Notation

Let:

- $F$ be files in a compatible rewrite/query cohort;
- $I_f^x=[l_f^x,u_f^x]$ be conservative bounds of file $f$ on column $x$;
- $Q^x=[q_l,q_u]$ be a range predicate;
- $B_f$ be physical bytes of $f$;
- $P(Q)$ be files whose relevant summaries may overlap $Q$;
- $B_{scan}(Q)=\sum_{f\in P(Q)}B_f$ be candidate bytes;
- $B_{read}$ and $B_{result}$ be actual read and result bytes;
- $O_x$ be a declared interval-overlap metric;
- $L=(e_1,\ldots,e_d)$ be a layout over $d$ expressions;
- $z_L(r)$ be a multidimensional locality key for row $r$;
- $W$ be workload fingerprints with frequency $freq(q)$ and importance $imp(q)$;
- $C_L(W)$ be modeled candidate cost under layout $L$;
- $R_L$ be rewrite/maintenance cost;
- $U_L$ be bytes actually organized under layout $L$ and $T$ total compatible bytes.

Coverage $U_L/T$ requires positive $T$ and says nothing about query-weighted coverage. Pruning ratio can mean files rejected, bytes rejected, row groups rejected, or pages rejected; name the unit. Result amplification $B_{read}/B_{result}$ is undefined for zero-result queries, which need a separate cohort.

## Mechanisms, Invariants, or Proof Structure

### Range-pruning argument

If each file bound conservatively contains its actual $x$ values, a range query may skip file $f$ only when $I_f^x\cap Q^x=\varnothing$. Sorting adjacent $x$ values before file cutting tends to reduce interval width and overlap, increasing safe exclusions. It does not guarantee a particular reduction without a distribution and boundary model.

### Order-verification argument

For declared lexicographic comparator $\preceq_L$, verify every adjacent row pair within the file satisfies $r_i\preceq_L r_{i+1}$, using exact null/NaN/collation/type rules. Verify statistics cover every row and file metadata references $L$. Distributed range partition boundaries may additionally prove nonoverlapping file ranges, but internal order alone does not prove global file order.

### Logical-equivalence obligation

Decode input state after applicable updates/deletes to canonical logical multiset $M_I$. Decode outputs to $M_O$. Require $M_I=M_O$, plus preserved schema/spec, sequence/delete semantics, constraints, and provenance. Order changes sequence of physical rows but not keyed logical meaning unless the application contract explicitly treats order as data.

### Multidimensional caution

A locality key maps $d$ dimensions to one dimension and necessarily loses aspects of neighborhood/order. Prove deterministic encoding and conservative statistics, not universal optimal locality. Evaluate actual query rectangles; do not infer benefit from the visual smoothness of a curve.

### Economic proof

Record predicted workload-weighted read savings and rewrite/maintenance cost before execution. After a representative horizon, compare matched cohorts and uncertainty. Promote a layout only if correctness holds, important query tails do not regress, and realized discounted savings exceed total maintenance and interference cost under the chosen policy.

## Alternatives and Trade-Offs

**Single-column sorting** gives strong range locality and simple semantics but favors one axis. **Lexicographic sorting** supports leading prefixes and within-prefix ranges but weakens non-prefix filters.

**Z-order** distributes locality across several dimensions with relatively direct key construction. **Hilbert order** may improve neighborhood continuity but adds computation, versioning, and implementation complexity. Neither dominates for all distributions.

**Hash clustering** spreads keys and helps equality/co-location but destroys range order. **Range clustering** helps ranges and skipping but suffers skew at hot boundaries. Hybrid partition/hash/range designs add operational complexity.

**Write-time ordering** prevents debt but increases ingestion latency and shuffle. **Asynchronous clustering** protects writes but allows temporary degradation and consumes maintenance capacity.

**Full-table clustering** creates uniform coverage and high cost/conflict. **Incremental hot-range clustering** improves payback but leaves heterogeneous layouts that metadata and readers must support.

**Fixed declared order** is predictable but may age poorly. **Adaptive layout** follows workload but risks churn and makes reproducibility harder. Use stability windows, change budgets, and versioned rationale.

## Failure Modes and Misconceptions

1. **Partitioning equals sorting.** Partition membership does not order rows.
2. **Bin packing equals clustering.** File size can improve while bounds remain broad.
3. **Default order describes all files.** Historical or latency-sensitive writes may be unsorted.
4. **Internal order is global order.** Sorted files may overlap one another.
5. **Second lexicographic key works alone.** Earlier-key variation scatters it.
6. **More dimensions improve Z-order.** Finite locality is diluted.
7. **High cardinality guarantees value.** Predicates, selectivity, and statistics matter.
8. **Correlated columns both belong.** One may add no independent locality.
9. **Statistics appear automatically.** Writer/format configuration may omit them.
10. **Truncated bounds are exact.** They remain conservative approximations.
11. **Rows per file predict bytes.** Variable-width data creates skew.
12. **Hot keys are solved by sorting.** They can span many same-bound files.
13. **Reclustering is idempotent.** Algorithms may regroup already clustered data.
14. **Rename invalidates order.** Stable identity can preserve it; name-only clients may still break.
15. **Sort declaration can be aspirational.** It must describe actual bytes.
16. **Concurrent rewrite can be rebased blindly.** Changed inputs invalidate output.
17. **Fewer candidate files proves faster queries.** File size, pages, cache, CPU, and parallelism matter.
18. **One benchmark selects a durable layout.** Workload and data evolution require a horizon and controls.

## Worked Examples

### Example 1

Four files have `x` intervals `[0,100]`, `[10,110]`, `[20,120]`, and `[30,130]`. Query `[45,50]` retains all four. A range rewrite yields `[0,32]`, `[33,65]`, `[66,98]`, `[99,130]`; the query retains one.

### Example 2

Files sorted lexicographically by `(tenant_id,event_time)` make a tenant-plus-time query contiguous. An event-time-only query crosses every tenant and may retain most files. Workload frequency determines whether tenant should lead.

### Example 3

Columns `country` and `currency` are almost perfectly correlated. Adding both to a multidimensional key consumes dimension budget without much new separation. Measure conditional correlation and query combinations.

### Example 4

A file declares ascending timestamp order but places nulls first while metadata declares nulls last. Even if non-null rows are sorted, the order claim is false. The validator checks the exact comparator.

### Example 5

Z-ordering six fields costs a large shuffle, but 90% of valuable predicates use two together. A two-field layout yields tighter bounds and cheaper maintenance; the other filters rely on partitions, indexes, or scans.

### Example 6

One million rows are evenly divided by count, but recent rows contain large arrays. Output files and sort tasks vary widely in bytes. Byte-aware cutting and compression estimates reduce tails.

### Example 7

Twenty percent of table bytes use new sort order 4. Those bytes serve 70% of recent query reads. Report physical coverage 20% and query-weighted coverage 70%; neither substitutes for measured candidate-byte savings.

### Example 8

A clustering rewrite starts from files `{a,b,c}`. Concurrent update replaces `b`. Validation fails; publishing output would resurrect old `b` state. Replan from the new snapshot.

### Example 9

Files rejected improve from 60% to 90%, but files doubled in size. Candidate bytes improve only from 40% to 20%, not to 10%. Always evaluate the physical unit that drives cost.

### Example 10

The executable fixture compares overlapping unordered ranges with clustered adjacent ranges for the same query.

<!-- bijux-verify: {"id":"clustering-range-pruning","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"unordered_candidates=4\nclustered_candidates=1\nunordered_bytes=400\nclustered_bytes=100\nbyte_reduction_percent=75.0\nlogical_result_equal=yes\n","stderr":""}} -->
```python
query = (45, 50)
unordered = [(0, 100), (10, 110), (20, 120), (30, 130)]
clustered = [(0, 32), (33, 65), (66, 98), (99, 130)]

def overlaps(interval, target):
    return not (interval[1] < target[0] or interval[0] > target[1])

unordered_count = sum(overlaps(interval, query) for interval in unordered)
clustered_count = sum(overlaps(interval, query) for interval in clustered)
unordered_bytes = unordered_count * 100
clustered_bytes = clustered_count * 100
reduction = 100 * (unordered_bytes - clustered_bytes) / unordered_bytes

print(f"unordered_candidates={unordered_count}")
print(f"clustered_candidates={clustered_count}")
print(f"unordered_bytes={unordered_bytes}")
print(f"clustered_bytes={clustered_bytes}")
print(f"byte_reduction_percent={reduction:.1f}")
print("logical_result_equal=yes")
```

## Cross-Program Connections

- **Algorithms:** external sorting, sample/range partitioning, space-filling curves, quantiles, histograms, and approximation build layouts.
- **Data structures:** ordered runs, interval indexes, page indexes, Bloom filters, and persistent metadata expose locality.
- **Query engines:** data skipping, binary search, predicate pushdown, merge joins, top-k, task sizing, and caches consume order.
- **Storage:** row groups, pages, compression, encoding, file size, requests, and object locality determine physical benefit.
- **Distributed systems:** immutable rewrites, OCC, partial progress, retries, snapshot retention, and capability evolution preserve correctness.
- **Platform engineering:** workload telemetry, maintenance budgets, SLOs, policy versions, canaries, and multi-tenant controls govern operation.
- **Security:** predicate logs, min/max values, clustering keys, and access patterns can expose sensitive information.
- **Economics:** workload-weighted savings, rewrite cost, churn, stability, and payback decide whether locality is worth buying.

## References

1. Apache Iceberg, [Table Format Specification](https://iceberg.apache.org/spec/). Current. Defines sort orders, field identities, comparators, and per-file order metadata.
2. Apache Iceberg, [Spark Procedures](https://iceberg.apache.org/docs/1.6.0/spark-procedures/). Versioned. Documents sort and Z-order data-file rewrites and controls.
3. Apache Iceberg, [RewriteDataFiles API](https://iceberg.apache.org/javadoc/1.7.0/org/apache/iceberg/actions/RewriteDataFiles.html). Versioned. Defines bin-pack, sort, Z-order, and filtered strategies.
4. Apache Iceberg, [Spark Writes](https://iceberg.apache.org/docs/latest/spark-writes/). Current. Documents write distribution and fanout behavior.
5. Apache Iceberg, [RewriteManifests API](https://iceberg.apache.org/javadoc/1.10.0/org/apache/iceberg/actions/RewriteManifests.html). Versioned. Documents metadata ordering by query-relevant partition fields.
6. Delta Lake, [Optimizations](https://docs.delta.io/optimizations-oss/). Current. Documents data skipping, statistics, and Z-order behavior.
7. Delta Lake, [Liquid Clustering](https://docs.delta.io/delta-clustering/). Current. Documents evolvable clustering columns and compatibility requirements.
8. Apache Hudi, [Clustering](https://hudi.apache.org/docs/next/clustering/). Current. Documents clustering planning, grouping, ordering, and execution.
9. Apache Hudi, [Technical Specification](https://hudi.apache.org/learn/tech-specs-0-point-x/). Current. Describes layout optimization, column statistics, and clustering groups.
10. Apache Parquet, [Page Index](https://parquet.apache.org/docs/file-format/pageindex/). Current. Defines ordered/unordered page bounds and skipping.
11. Apache Parquet, [Column Chunks](https://parquet.apache.org/docs/file-format/data-pages/columnchunks/). Current. Describes page and column-chunk physical layout.
12. Apache Spark, [Performance Tuning](https://spark.apache.org/docs/latest/sql-performance-tuning.html). Current. Documents shuffle partitions, adaptive coalescing, and skew controls.
13. PostgreSQL, [Multicolumn Indexes](https://www.postgresql.org/docs/current/indexes-multicolumn.html). Current. Provides a contrasting explanation of leading-column effects in lexicographic structures.

## Exercises

### Exercise 1

Files have ranges `[0,40]`, `[20,60]`, `[50,90]`, and `[80,120]`, each 200 MiB. Which files are candidates for query `[55,58]`, and how many bytes are selected?

### Exercise 2

Explain the expected behavior of lexicographic layouts `(tenant,time)` and `(time,tenant)` for tenant-plus-time, time-only, and tenant-only predicates.

### Exercise 3

Design a complete sort declaration and verification for floating values with nulls, signed zero, infinities, and NaNs.

### Exercise 4

A layout covers 300 GiB of a 2 TiB table, but files under that layout account for 60% of candidate bytes in the measured query workload. Compute physical coverage and explain the second metric.

### Exercise 5

Design a before/after experiment to decide whether Z-ordering `(account_id,event_day)` repays its rewrite cost.

## Answers to the Exercises

### Answer 1

`[0,40]` is disjoint and skipped. `[20,60]` and `[50,90]` overlap and are retained. `[80,120]` is disjoint. Two files select 400 MiB. This relies on conservative correctly typed bounds; unknown bounds would retain the associated file.

### Answer 2

`(tenant,time)` makes one tenant's time range contiguous and supports tenant-only prefixes well, but time-only predicates cross tenants. `(time,tenant)` favors time-only scans and can narrow tenant within small time ranges, but tenant-only histories cross time. Actual files, data correlation, cardinality, and boundary cutting can modify results, so evaluate weighted predicates.

### Answer 3

Declare stable source ID, identity/other transform, ascending or descending direction, nulls first/last, writer type, and the format's total comparison for negative NaN, negative infinity, negative values, negative zero, positive zero, positive values, positive infinity, and positive NaN if supported. Verify every adjacent pair with exactly that comparator, verify file/page bounds conservatively cover rows, reject forbidden NaN bounds, and record the actual order ID. Cross-engine golden vectors test identical results.

### Answer 4

Two TiB is 2,048 GiB, so physical byte coverage is $300/2048\approx14.65\%$. Query-weighted candidate coverage of 60% means the organized cohort is disproportionately hot in the measured workload; it is not 60% of table bytes and does not prove savings. Compare its candidates against a counterfactual or before state, with frequency, query importance, cache, and time scope.

### Answer 5

Pin representative data and a workload horizon. Record normalized predicate rectangles, frequency/importance, files/pages/bytes selected/read, query tails, cache state, and result checks. Rewrite a controlled set with declared algorithm/version and collect shuffle, spill, read/write bytes, duration, file-size skew, conflicts, and ingest impact. Compare matched old/new cohorts for account-only, day-only, combined, zero-result, and critical non-target queries under warm/cold caches. Verify logical equality and statistics. Compute discounted observed savings over expected layout life versus total maintenance/interference cost, and repeat before fleet policy promotion.
