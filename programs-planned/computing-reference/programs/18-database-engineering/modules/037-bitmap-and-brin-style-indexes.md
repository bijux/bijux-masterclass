---
module_id: DBE-037
program: Database Engineering
level: 1
module_number: 37
title: Bitmap and BRIN-Style Indexes
status: complete
last_verified: 2026-08-30
---

# Bitmap and BRIN-Style Indexes

## One-Page Review

### Governing question

How can a database represent candidate row sets or coarse page-range summaries compactly enough to skip work, while guaranteeing that lossiness, stale summaries, visibility, and physical layout never create false negatives?

### Essential definitions

A **persistent bitmap index** stores bit vectors or compressed row sets associated with values/ranges. A **transient bitmap scan** constructs an execution-time candidate set from one or more ordinary index scans and combines it with bitwise AND/OR; it is a plan representation, not necessarily a persistent bitmap access method. An **exact bitmap** identifies candidate tuple locations individually. A **lossy bitmap** identifies a containing page/range when memory pressure or access-method semantics cannot retain exact locations, so every tuple there must be rechecked. A **BRIN-style summarizing index** stores conservative metadata—such as min/max, bounding set, bloom signature, or multiple intervals—for a physical block range. A summary is **consistent** with a predicate when the range might contain a match; inconsistency safely excludes it. **Physical correlation** measures how well indexed values cluster/order with table location. An **unsummarized range** lacks a usable summary and must not be silently excluded.

### Central model, mechanism, or theorem

Exact bitmaps compute set operations directly: bits for `A AND B` are `bitmap(A) & bitmap(B)`, while OR uses union. Lossy candidates must be base-rechecked. A BRIN min/max summary `(lo_r,hi_r)` can reject query interval `[a,b]` only when `hi_r<a` or `lo_r>b`; overlap means “possible,” not “match.” If every value in range `r` lies within its conservative summary, rejection cannot remove a true result. Effectiveness—not correctness—depends on correlation, range granularity, outliers, and up-to-date/unsummarized handling.

### Critical invariants

- Bit positions/tuple identifiers bind to the correct relation and row/page incarnation; updates and reuse cannot retarget stale bits.
- Exact bitmap set operations preserve every qualifying candidate under the declared predicate logic.
- Every lossy page/range is rechecked against the original condition, visibility, and any partial-index predicate.
- BRIN summaries conservatively contain all indexed values in their ranges; shrink only after proving removed extremes are no longer required.
- An unsummarized, stale, or invalid range is treated conservatively—normally scanned—not skipped.
- Summary-to-range mapping, metapage/reverse map, pages-per-range, operator class, and index version agree.
- NULL/all-null/no-null/empty-range states are represented according to the operator class rather than guessed from min/max.
- Bitmap AND/OR observes compatible snapshots, TID domains, and predicate meanings; it does not promise output order.
- Concurrency, WAL, vacuum/cleanup, summarization, desummarization, and page reuse preserve no-false-negative behavior.
- Plan value is judged by heap pages/tuples rechecked, memory/spill, correlation, and output—not index size alone.

### Common failures

Failures include calling PostgreSQL Bitmap Index Scan a persistent bitmap index; assuming a bitmap heap scan preserves index order; returning lossy candidates without recheck; treating min/max overlap as proof every row matches; using current min/max after deleting an extreme without safe resummarization; skipping unsummarized ranges; selecting BRIN only because a column has low cardinality; ignoring one outlier that widens a range; using huge ranges that select most pages; using tiny ranges that bloat maintenance/index size; confusing Bloom false positives with false negatives; combining bitmaps from incompatible snapshots/incarnations; and reading a low BRIN size as a performance guarantee.

### Compact example

Four physical ranges have values `P0=(1,3,5)`, `P1=(90,100,110)`, `P2=(111,120,140)`, `P3=(200,210,220)`. Query `[105,115]` rejects P0/P3 by min/max and visits P1/P2. Six rows are rechecked; only 110 and 111 match. The false positives are expected and safe. Separately, exact row bitmaps `ready={1,3,4,7}` and `tenant7={1,2,4,5}` yield AND `{1,4}` and OR `{1,2,3,4,5,7}` but no ordering guarantee.

### Connections

This module contrasts exact ordered/scalar indexes from DBE-031–036 with candidate-set and physical-summary designs. DBE-038 covers inverted/full-text posting sets; DBE-039 covers maintenance/write amplification; later optimizer modules cost bitmap combinations and rechecks.

## Governing Question

The governing question is not “is the index small?” It is whether the structure can safely rule out work, what candidates it returns, which original conditions must be rechecked, and whether the workload/layout makes exclusion selective enough to beat a sequential or ordinary index scan.

Three objects are often conflated. A persistent bitmap index materializes value-to-row bitsets. An execution bitmap is temporary state produced by one or more access paths. BRIN stores summaries per physical range and commonly emits a lossy page bitmap. Their compression, maintenance, concurrency, and optimizer contracts differ even when all eventually manipulate bits.

## Why This Matters

Analytical predicates often combine several moderately selective conditions. Repeated random row fetches from independent indexes can be expensive; bitmap AND/OR can first accumulate candidates, order heap-page visits, and fetch each page efficiently. Persistent compressed bitmaps can evaluate low/moderate-cardinality predicates with fast word operations.

Very large append-correlated tables may not need one entry per row. A tiny BRIN summary can exclude most history for a time range. But disorder, backfills, updates, or outliers widen summaries until most ranges become candidates. The same structure remains correct and small while becoming useless, so physical-layout health and recheck rate are first-class evidence.

## Prerequisites and Retrieval

Retrieve SQL predicate/NULL/visibility semantics from DBE-011–020, pages/TIDs from DBE-021–026, integrity/writeback from DBE-028–030, range scans from [DBE-032](032-b-tree-search-and-range-scan.md), and partial predicate rechecks from [DBE-036](036-partial-and-expression-indexes.md).

Before continuing, represent finite sets as bit vectors and compute AND/OR/NOT with a declared universe. Prove the interval-disjointness test. Explain why a physical page identifier needs relation/incarnation protection and why a candidate set is not a result set.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish persistent bitmap indexes, transient bitmap scans, and BRIN summaries;
2. derive exact AND/OR/NOT candidate sets and their snapshot/universe assumptions;
3. explain exact versus lossy bitmap memory behavior and mandatory rechecks;
4. prove min/max range exclusion has no false negatives under conservative summaries;
5. reason about pages-per-range, correlation, outliers, clustering, and recheck amplification;
6. compare minmax, multi-minmax, inclusion, and Bloom-style summaries;
7. trace inserts, updates, deletion, vacuum, summarization, desummarization, and page reuse;
8. design WAL/concurrency/validation for summary and bitmap state;
9. compare bitmap/BRIN with B+ tree, hash, sequential, partition pruning, and columnar designs; and
10. build correctness, disorder, memory, crash, and workload experiments.

## Core Exposition

A bit vector over universe `U={0,...,n-1}` represents set membership: bit `i=1` means row/TID `i` is a candidate. Equality bitmap per distinct value makes `x=a OR x=b` a wordwise OR and conjunction across columns an AND. NOT requires a declared live-row universe; complementing arbitrary allocated positions can invent candidates. MVCC versions and deletes complicate what “row i” means.

Compression changes the low-cardinality slogan. Uncompressed bitmap cost is roughly rows times distinct values; word-aligned/run-length/Roaring-like schemes exploit runs or sparse/dense containers. Row order affects compressibility. Cardinality alone does not decide size/performance: distribution, runs, encoding, query operations, updates, and concurrency matter. High-cardinality bitmap variants can be useful with compression/bit slicing, while a randomly alternating binary column can compress poorly.

Persistent bitmap updates can touch shared words/segments and create contention or write amplification. MVCC needs version-aware membership or safe stale-bit recheck. Bulk/append analytics differ from high-churn OLTP. Product-specific bitmap indexes have distinct locking and maintenance rules; do not infer them from abstract bit operations.

A transient bitmap plan asks ordinary access methods for TIDs, combines candidate sets, then visits heap/base pages. PostgreSQL's `Bitmap Index Scan` is such a plan node, even if its input is a B-tree. `BitmapAnd` and `BitmapOr` combine multiple inputs. Because TIDs are reorganized by page, index ordering is lost; an explicit sort may follow.

An exact transient bitmap retains individual tuple offsets. Under a memory limit it may become lossy by remembering only page membership. Then every visible tuple on the page is a candidate, and the executor rechecks index conditions (and recheckable partial predicate) to eliminate false positives. A lossy bitmap must never discard a candidate merely to save memory; it coarsens location.

Bitmap plans trade startup and memory for batched heap locality. They help when a plain index scan would do many scattered fetches yet a sequential scan would read too much. For very few rows, direct index scan avoids bitmap construction. For most pages, sequential scan avoids index/recheck overhead. `LIMIT` and required order often favor a direct ordered index because a bitmap plan builds candidates and loses order.

BRIN partitions the heap's block-number space into fixed ranges and stores operator-class summaries. For min/max, insertion expands `lo=min(lo,x)` and `hi=max(hi,x)`. Query range overlaps summary if not disjoint. The summary proves absence only for disjoint ranges; overlap emits the whole block range for heap recheck. It never identifies exact rows.

No-false-negative proof: assume every non-NULL value `x` in range r satisfies `lo_r<=x<=hi_r`. If query seeks `a<=x<=b` and summary is disjoint, either `hi_r<a`, hence every `x<a`, or `lo_r>b`, hence every `x>b`; no match exists. The converse fails: overlap can be caused by values outside the query or wide gaps.

NULL needs explicit summary flags/operator semantics. A range of all NULLs has no ordinary numeric min/max, yet `IS NULL` may match all rows. A mixed range may need has-null/all-null metadata. Empty/new ranges and unsummarized ranges must be conservatively included or summarized before exclusion.

`pages_per_range` controls granularity. Smaller ranges create more summary tuples and maintenance/index reads but narrower candidate regions. Larger ranges shrink the index but widen summaries and rechecks. If values are physically ordered, even large ranges separate cleanly. If values are random, each range tends toward global min/max and nearly every query overlaps.

Correlation is workload-specific. Append timestamps correlate naturally until backfills place old timestamps in new blocks, or updates scatter values. Cluster/rewrite can restore locality at operational cost. One outlier can widen a min/max summary dramatically; minmax-multi stores several intervals to reduce gaps, while inclusion summaries store bounding representations and Bloom summaries trade configurable false positives for compact membership evidence. Operator-class semantics decide supported predicates.

BRIN maintenance is asymmetric. Expanding a summary on insert is safe. Deleting/updating an extreme does not require immediate shrinking for correctness; the stale wider summary only adds false positives. Resummarization can tighten after verifying the range. New page ranges may be unsummarized until vacuum/manual/auto summarization; PostgreSQL's current documentation says autosummarize is not enabled by default and missed request queues can leave debt.

Current PostgreSQL BRIN uses a reverse map from each heap range to its summary tuple. Index creation scans existing pages. Concurrent inserts can update/replace summaries; WAL/recovery and locks preserve mapping. An invalid, missing, or corrupt summary must fail/scan conservatively according to engine policy, never authorize silent skipping.

Combining BRIN with partition pruning stacks exclusion layers: partition metadata removes partitions, BRIN removes physical ranges, heap predicate removes rows. A B+ tree is better for selective exact probes/order; BRIN often wins for broad correlated ranges on huge data with tiny maintenance/storage budget. Zone maps in columnar/file formats share the conservative-summary idea.

Cost tracks summary/index pages, ranges selected/total, heap pages exact/lossy, tuples rechecked/removed, bitmap memory/spill/lossification, access-input searches, base cache/I/O, visibility, sort, output, parallelism, and maintenance debt. `rows removed by index recheck`, exact/lossy heap blocks, and buffers are more informative than index size alone.

Observability records index/operator-class/version, pages-per-range, summarized/unsummarized ranges, summary widths/outliers, physical correlation, selected/total ranges, exact/lossy bitmap pages, candidates/rechecks/matches, false-positive ratio, bitmap bytes/lossification/spill, heap blocks, cache/I/O, sort/order, WAL/summary updates, summarization queue/age, rebuild/cluster age, and p50/p99. Aggregate sensitive values.

Testing differentially compares every result to a full predicate scan under the same snapshot. Generate ordered, reverse, random, clustered, backfilled, outlier, duplicate, NULL, and skewed layouts. Test every range boundary and pages-per-range. Force memory lossification, bitmap AND/OR/NOT, stale/unsummarized/desummarized state, concurrent insert/update/vacuum, crash after each WAL action, corrupt mappings, reuse, cancellation, and parallel execution. Zero false negatives is non-negotiable; false positives are measured.

The executable model shows exact set bitmaps and a stable min/max summary scan. It selects two of four ranges, rechecks six values, returns 110/111, and counts four false positives. It omits compression, memory lossification, SQL NULL/MVCC, persistent pages, concurrent maintenance, WAL, and performance.

<!-- bijux-verify: {"id":"bitmap-brin-candidates","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"bitmap_and=(1, 4)\nbitmap_or=(1, 2, 3, 4, 5, 7)\nbrin_candidate_ranges=('P1', 'P2')\nbrin_rechecked=6\nbrin_matches=(110, 111)\nbrin_false_positives=4\nno_false_negatives=True\n","stderr":""}} -->
```python
ready = {1, 3, 4, 7}
tenant_7 = {1, 2, 4, 5}
ranges = {
    "P0": (1, 3, 5),
    "P1": (90, 100, 110),
    "P2": (111, 120, 140),
    "P3": (200, 210, 220),
}
low, high = 105, 115
summaries = {name: (min(values), max(values)) for name, values in ranges.items()}
candidate_names = tuple(
    name
    for name, (minimum, maximum) in summaries.items()
    if not (maximum < low or minimum > high)
)
rechecked = tuple(value for name in candidate_names for value in ranges[name])
matches = tuple(value for value in rechecked if low <= value <= high)
reference = tuple(
    value
    for values in ranges.values()
    for value in values
    if low <= value <= high
)

print(f"bitmap_and={tuple(sorted(ready & tenant_7))}")
print(f"bitmap_or={tuple(sorted(ready | tenant_7))}")
print(f"brin_candidate_ranges={candidate_names}")
print(f"brin_rechecked={len(rechecked)}")
print(f"brin_matches={matches}")
print(f"brin_false_positives={len(rechecked) - len(matches)}")
print(f"no_false_negatives={matches == reference}")
```

## Definitions and Notation

Let row/TID universe be `U`; bitmap for predicate A be `B_A subset U`. Exact AND/OR are intersection/union. Let physical ranges be `r`, summary `S_r`, query condition `Q`, and consistency function `C(S_r,Q)`. No-false-negative summary contract is: if any row in `r` satisfies Q, then `C(S_r,Q)=true`. It need not guarantee a match when true.

Let selected range fraction be `sigma`, rechecked tuples `c`, matches `m`, false positives `fp=c-m`, false-positive ratio `fp/c`, exact pages `e`, lossy pages `l`, bitmap memory `M`, and range size `g`. Performance depends on these plus I/O/cache/visibility/order, not merely asymptotic bit operations.

## Mechanisms, Invariants, or Proof Structure

A defensible workflow is:

1. Bind relation/index incarnation, snapshot, original predicates, TID universe, operator classes, and summary/bitmap version.
2. Produce exact candidates from each access path; combine only compatible domains/snapshots.
3. Under memory pressure, coarsen exact TIDs to containing pages without dropping pages.
4. For BRIN, read validated summary mappings; include unsummarized/invalid/concurrent ranges conservatively.
5. Apply consistency tests to reject only ranges proven disjoint/impossible.
6. Fetch selected pages efficiently; recheck original conditions, partial predicates, and visibility for every lossy candidate.
7. Preserve no output order unless a later sort/merge establishes it.
8. Account exact/lossy pages, summary debt, candidates/rechecks/matches, memory/I/O, and limitations.

Correctness composes: exact index inputs contain their qualifying TIDs; sound AND/OR represents predicate conjunction/disjunction; lossification replaces TIDs only by supersets of containing pages; conservative summaries emit every range containing a match; final recheck removes false positives. Therefore no qualifying visible row is lost, assuming compatible snapshot/identity and correct maintenance. This is a proof sketch, not a concurrency/recovery proof for a product.

## Alternatives and Trade-Offs

Persistent bitmaps accelerate repeated set algebra but can be update/contention heavy. Transient bitmaps reuse ordinary indexes and memory per query but add startup/lossification and lose order. BRIN is extremely small and cheap for correlated physical layouts but lossy. B+ trees provide exact ordered access; hash serves equality; sequential scans win broad/unclustered access; partition pruning removes coarse logical partitions; columnar zone maps/vector scans extend the summary approach.

Minmax is tiny/simple but outlier-sensitive. Minmax-multi models gaps at greater summary size. Bloom summaries support membership with false positives and parameterized sizing, never false negatives under correct implementation. Inclusion/bounding boxes suit containment/geometry. Choose by operator semantics and data layout, not access-method name.

## Failure Modes and Misconceptions

- “Bitmap Index Scan means bitmap index.” It may consume a B-tree into a temporary bitmap.
- “Bitmaps preserve order.” Page-oriented combination discards index key order.
- “Lossy means incorrect.” It means superset candidates plus mandatory recheck.
- “Recheck is optional if estimates are good.” Correctness requires it for lossy evidence.
- “Min/max overlap means rows match.” It only means the range cannot be excluded.
- “BRIN is for low cardinality.” Physical correlation and summary operator matter more.
- “Small index means small scan.” Wide summaries can select almost every heap page.
- “Deletes must shrink summaries now.” Wider stale summaries are safe but less selective.
- “Unsummarized means empty.” It means unknown and must be included/summarized.
- “More pages per range is always better.” It shrinks index while often increasing rechecks.
- “Bloom false positive is a false row result.” Final recheck removes it; false negatives are forbidden.
- “NOT is just bit complement.” The live snapshot universe must be declared.
- “Clustering lasts forever.” backfills/updates and append patterns can degrade correlation.
- “One fast benchmark proves fitness.” Layout, memory, cache, churn, and selectivity drift.

## Worked Examples

### Example 1

Exact bitmaps ready `{1,3,4,7}` and tenant 7 `{1,2,4,5}` yield AND `{1,4}`. Fetching only one input then residual-checking can be cheaper for tiny sets; bitmap construction is costed. Conclusion: set algebra is exact but not automatically optimal.

### Example 2

Memory lossifies exact offsets on page 9 into “page 9.” The executor checks every visible tuple there and removes 18 of 20. Conclusion: memory is bounded by increasing false positives, not dropping candidate pages.

### Example 3

Min/max `(90,110)` overlaps `[105,115]`, though only 110 matches. Conclusion: consistency proves possibility, not row qualification.

### Example 4

Summary `(1,1000000)` arose from one outlier among values 1–10. Most queries overlap. Resummarization cannot help while the outlier remains; minmax-multi or relocation may. Conclusion: one value can destroy pruning without corruption.

### Example 5

Ordered timestamps give disjoint narrow summaries at 128 pages/range; random timestamps make each range approximate global history. Same index size, different selected-page fraction. Conclusion: correlation is an effectiveness invariant.

### Example 6

A new filled range has no summary because an autosummarization request was missed. Treating it as empty loses rows; scanning it preserves correctness until vacuum/manual summarization. Conclusion: maintenance debt must be conservative and observable.

### Example 7

Deleting the minimum leaves a stale lower bound. Queries near the old minimum still scan/recheck the range but return no false row. Conclusion: conservative widening affects performance, not correctness.

### Example 8

Bitmap OR combines two predicates, then heap recheck applies a lossy partial-index predicate and MVCC visibility. Counting raw bits as returned rows overstates results. Conclusion: candidate, visible, rechecked, and returned counts differ.

### Example 9

Query requires `ORDER BY created LIMIT 10`. A B+ tree can stop after ten qualifying ordered rows; a bitmap plan gathers/reorders candidates then sorts. Conclusion: selectivity alone does not choose the access path.

### Example 10

Partition pruning removes eleven months, BRIN removes 90% of ranges in the remaining month, and row recheck returns matches. Validate each layer against a full scan. Conclusion: conservative exclusion composes when each layer has no false negatives.

## Cross-Program Connections

- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies bitsets, compressed sets, and set algebra.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies conservative filters and no-false-negative proofs.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) supplies file/partition layouts, clustering, zone maps, and scan workloads.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) supplies word/SIMD bit operations, cache, and compression effects.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies memory limits, telemetry, maintenance debt, and fault injection.

## References

1. PostgreSQL Global Development Group, [BRIN Indexes](https://www.postgresql.org/docs/current/brin.html), current range, lossiness, operator-class, pages-per-range, and summarization semantics.
2. PostgreSQL Global Development Group, [BRIN Reverse Map Source](https://github.com/postgres/postgres/blob/master/src/backend/access/brin/brin_revmap.c), current range-to-summary mapping and concurrency implementation.
3. PostgreSQL Global Development Group, [Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html), current Bitmap Index/Heap Scan, recheck, exact/lossy block, and buffer evidence.
4. PostgreSQL Global Development Group, [Index Scanning](https://www.postgresql.org/docs/current/index-scanning.html), current bitmap, lossy/recheck, visibility, and ordering interface.
5. PostgreSQL Global Development Group, [BRIN Introduction Commit](https://www.postgresql.org/message-id/E1XmpRL-0001Zh-Sd%40gemulon.postgresql.org), primary implementation design record.
6. Patrick O'Neil and Dallan Quass, “Improved Query Performance with Variant Indexes,” *SIGMOD Record* 26(2), 1997, bitmap and bit-sliced index foundations.
7. Elizabeth O'Neil, Patrick O'Neil, and Kesheng Wu, [Bitmap Index Design Choices and Their Performance Implications](https://doi.org/10.1109/IDEAS.2007.4318091), *IDEAS*, 2007.
8. Kesheng Wu, Ekow Otoo, and Arie Shoshani, [Bitmap Indices for Data Warehouses](https://sdm.lbl.gov/~kewu/ps/LBNL-59952.pdf), LBNL, 2006.
9. Daniel Lemire, Owen Kaser, and Kamel Aouiche, [Sorting Improves Word-Aligned Bitmap Indexes](https://arxiv.org/abs/0901.3751), 2009, compression/layout analysis.
10. Ramakrishnan and Gehrke, *Database Management Systems*, 3rd ed., McGraw-Hill, 2003, bitmap access and query-processing foundations.

## Exercises

### Exercise 1

For universe `{0,...,9}`, compute `(A AND B) OR C`, `A AND NOT B`, and identify the required live-row universe when `A={0,2,4,6}`, `B={2,3,4,5}`, `C={8}`. Explain MVCC/reuse caveats.

### Exercise 2

Given six page-range min/max summaries and queries with inclusive/exclusive/unbounded/NULL predicates, derive candidate ranges and required rechecks. Construct one false positive and prove no false negative.

### Exercise 3

Choose `pages_per_range` and operator class for ordered timestamps with rare backfills, random UUIDs, clustered ZIP codes with outliers, and equality-heavy tags. State assumptions and adaptive evidence.

### Exercise 4

Design concurrent/crash-safe BRIN summarization and desummarization with range mapping, inserts, WAL, missing summaries, vacuum, corruption, and recovery. State conservative states.

### Exercise 5

Design an experiment comparing direct B+ tree scan, transient bitmap combination, BRIN, sequential scan, and partition pruning across layout, selectivity, cache, memory, order/limit, churn, and parallelism.

## Answers to the Exercises

### Answer 1

`A AND B={2,4}`; union C gives `{2,4,8}`. With declared universe U `{0,...,9}`, `NOT B={0,1,6,7,8,9}`, so `A AND NOT B={0,6}`. If only currently visible live rows are `{0,1,2,4,6,8}`, complement must be relative to that snapshot universe, producing live `NOT B={0,1,6,8}` but the final A result remains `{0,6}`. Persistent/transient TIDs need relation/page incarnation and MVCC recheck; complementing allocated slots can include dead/reused/unrelated locations.

### Answer 2

For ordinary inclusive `[a,b]`, choose summary `[lo,hi]` unless `hi<a` or `lo>b`; exclusive endpoints adjust equality at the boundary, and unbounded removes one disjoint test. `IS NULL` requires has-null/all-null metadata, not numeric min/max. A range `(90,110)` against `[105,115]` is selected, then values 90/100 are false positives and 110 matches. No-false-negative proof: if rejected left, every value `<=hi<a`; if rejected right, every value `>=lo>b`. This assumes conservative summary and compatible comparator. Unsummarized/invalid ranges are candidates.

### Answer 3

Ordered timestamps favor minmax and can tolerate larger ranges; measure boundary-query rechecks and backfill widening. Rare backfills may justify minmax-multi or targeted resummarization/physical rewrite. Random UUID min/max will approach global bounds, so a B+ tree/hash is usually better; BRIN Bloom might help only with measured range-local membership and false-positive trade-off. Clustered ZIP codes favor minmax/inclusion with smaller ranges around outliers or minmax-multi. Equality-heavy tags may use BRIN Bloom sized from distinct-per-range/false-positive targets if tags cluster; a B+ tree/bitmap/inverted design may win otherwise. Choose via index bytes, selected ranges/pages, rechecks, maintenance/WAL, cache, and p99 under current layout.

### Answer 4

Persist index/range generations and reverse-map identity. Missing summary means scan candidate. Build a summary by scanning a protected range under a protocol that incorporates concurrent inserts or retries; WAL summary tuple and reverse-map publication idempotently before permitting exclusion. Existing summarized ranges expand on inserts. Desummarization atomically makes mapping absent/conservative before retiring old tuple; resummarization republishes only from a complete protected scan. Vacuum/manual/auto work records debt and tolerates missed requests. Crash at every scan/publication/update boundary recovers to old conservative, missing, or new complete state—not a narrow incomplete summary. Validate checksums/types/range ownership; quarantine/scan on corruption per policy; page reuse needs generation safety. Replay twice and differential-check against full scan.

### Answer 5

Use identical snapshot/results and a full-scan oracle including NULL, visibility, partial predicates, and ordering. Vary row/table size, physical correlation, range size, selectivity, predicate AND/OR, result size, duplicates/outliers/backfills, pages-per-range/operator class, bitmap memory/lossification/spill, cache, storage, order/limit, updates/deletes/summarization debt, concurrency, and parallelism. Record plans, index/summary pages, searches, ranges selected, exact/lossy heap blocks, candidates/rechecks/removed/matches, base fetches, sort, memory/spill, buffers/I/O/CPU, WAL/maintenance, throughput, and p50/p99. Partition pruning can precede each access. Repeat with controlled layouts and plans; canary without global forcing. Choose by zero false negatives and declared latency/resource/write thresholds, not smallest index or one warm run.
