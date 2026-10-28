---
module_id: DBE-067
program: Database Engineering
level: 2
module_number: 67
title: Access-Path Selection
status: complete
last_verified: 2026-08-30
---

# Access-Path Selection

## One-Page Review

### Governing question

How should an optimizer enumerate, prove legal, cost, and select the physical route from a logical relation to qualifying visible row occurrences while preserving required order, parameterization, snapshot semantics, and resource limits?

### Essential definitions

An **access path** is a physical plan for obtaining a relation's required rows/properties: sequential/column scan, direct row identifier, index/range/skip scan, index-only/covering scan, bitmap/index-merge scan, partition/file/block pruning, synopsis-assisted scan, remote pushdown, or parameterized lookup. An **access predicate** constrains navigation; an **index condition** may be evaluated within the index; a **residual/recheck predicate** is evaluated afterward. A **covering** path can provide required columns from its access structure, subject to visibility/version rules. **Sargability** means a predicate can be mapped to an access method's supported search operation without changing semantics. **Clustering/correlation** describes relation between access-key order and physical placement. **Lossy pruning** admits false positives but no false negatives. A **parameterized path** depends on values produced by another plan node.

### Central model, mechanism, or theorem

For bound relation R and required properties p, derive every supported candidate `a` with exact navigation bounds, residual predicates, delivered properties, parameter dependencies, visibility/recheck obligations, and cost/resource/uncertainty estimates. Reject semantically invalid or unavailable candidates. Retain non-dominated candidates per property/parameter class, because a locally dearer ordered, covering, partition-local, or parameterized path can make the full plan cheaper. Selection is `arg min` over feasible candidates under the declared objective—not “use an index when selective.”

### Critical invariants

- Predicate-to-access matching respects type, collation, operator family/class, null/NaN semantics, casts, expressions, volatility, partial-index implication, tenant/security predicates, and snapshot.
- Access bounds are necessary supersets of qualifying rows; residual/recheck evaluation recovers exact SQL semantics.
- Partition/file/block pruning removes a region only by a sound proof or synopsis contract; stale/lossy summaries may add reads but never remove possible matches.
- Covering/index-only eligibility distinguishes stored/reconstructible values from row-version visibility and payload freshness.
- Ordering includes key sequence, direction, equality-fixed prefixes, collation, null placement, uniqueness/ties, partition concatenation, and required global versus local order.
- Cost separates startup, examined entries, fetched pages/bytes, emitted rows, rechecks, random/sequential locality, repeated probes, caching, memory, sort avoidance, and row goal.
- Candidate traces bind schema/index generation, statistics, parameters, snapshot, configuration, engine/model versions, and fallback.

### Common failures

Failures include rewriting an expression to look indexable while changing semantics; treating a broad range as an exact predicate; assuming composite-index suffixes narrow the scan; assuming INCLUDE guarantees heap-free execution; losing required order through bitmap combination; equating matching row count with heap pages; ignoring duplicates across OR branches; pruning on an unenforced constraint or stale unsound metadata; using compile-time parameters for a generic plan; selecting a cheap parameterized path outside its producer; forcing an index from one benchmark; or evaluating estimated path cost without candidate execution and workload consequences.

### Compact example

Under normalized costs, a 1,000-page/100,000-row sequential scan costs 2,250. A point B-tree path fetching eight scattered heap pages costs 37.14. At 5,000 rows, a plain index path costs 3,339.50 while bitmap batching costs 422.50. At 60,000 rows, the index costs 5,352 and the scan wins. An ordered covering path serving LIMIT 20 costs 4.15 and avoids sort; a bitmap would lose index order. Partition pruning selects one 100-page partition for 225, and a lossy BRIN-like summary selects four ten-page ranges for 52 with mandatory recheck. The executable verifies only these finite equations.

### Connections

Retrieve [Sequential and Index Scans](052-sequential-and-index-scans.md), [Composite and Covering Indexes](035-composite-and-covering-indexes.md), [Cost Models](065-cost-models.md), and [Join Ordering](066-join-ordering.md). Continue through [the roadmap](../ROADMAP.md) to parameter sensitivity, adaptive query processing, and plan diagnosis.

## Governing Question

A logical scan means “produce visible occurrences of R satisfying predicate q with columns c and properties p.” It does not say whether to traverse every row, seek a B-tree, combine bitmaps, read only an index, prune partitions/files/ranges, perform parameterized probes, or push work to a remote source. How should the optimizer enumerate all semantically sound routes, expose what each route actually guarantees, and choose the best whole-plan contribution under uncertain data and runtime conditions?

Access-path selection is a proof problem before it is a cost problem. The optimizer must show that its navigation bounds cannot omit a qualifying row under SQL types, nulls, collations, casts, functions, operator semantics, row versions, and policies. A path may intentionally admit extra rows, but then its residual/recheck is part of correctness. Only after establishing this contract can cost, ordering, covering, locality, memory, and parameterization rank candidates.

It is also a global planning problem. A bitmap path may minimize local I/O but destroy order. A covering ordered index may cost more locally yet satisfy ORDER BY and LIMIT without a sort. A parameterized index lookup is valuable only inside a join order that supplies its key. A partition-local scan can enable parallelism or pruning. Therefore access paths belong in the memo/property space, not in a one-time “choose scan” prepass.

## Why This Matters

Access paths determine which bytes, pages, objects, partitions, remote requests, and row versions are touched. They control startup latency, cache behavior, prefetch, random access, visibility checks, recheck CPU, memory for bitmaps, result order, lock/pin patterns, and downstream join choices. A wrong path can turn a point query into a table scan, a broad predicate into millions of random heap reads, or an ordered LIMIT into a full scan and sort.

System R made access-path enumeration, selectivity, interesting order, and cost integral to optimization. Modern systems add composite/partial/expression/covering indexes, bitmap/index merge, skip scan, visibility metadata, partition and block pruning, column projection, remote/object stores, and runtime parameters. The durable principle remains: enumerate capabilities and properties from exact metadata, derive a sound candidate contract, then cost the work the executor will actually perform.

Current PostgreSQL 18 documentation illustrates index, bitmap, skip, index-only, partition-pruning, and BRIN behavior. Its bitmap combination loses original index order; index-only benefit depends on all-visible state; partition pruning is driven by partition bounds rather than index presence; and BRIN is lossy and requires recheck. Current MySQL 8.4 documentation distinguishes extracted range conditions from full WHERE semantics and supports range, skip scan, and index-merge variants. These product facts reinforce the same model/guarantee boundary.

Production correctness is as important as speed. Unsound pruning causes missing rows. An index-only visibility bug can expose wrong versions. Partial-index implication mistakes can violate predicates. Collation/cast mismatches can change comparison results. Security filters and tenant boundaries must not be bypassed by pushdown. Performance changes also alter cache pollution, storage traffic, replicas, remote billing, and workload interference. Verification must cover semantics, candidate completeness, path decisions, and system outcomes.

## Prerequisites and Retrieval

You should understand SQL bags/nulls/types/collations, MVCC/visibility, pages/buffer pools, B-trees/hashes/LSM-like storage, composite/covering/partial/expression indexes, logical/physical plans, cardinality, cost, join ordering, sorting, partitions, and distributed storage.

Retrieve: relation occurrence; access method/capability; search key; bound interval; equality prefix; skip scan; index/index-only/bitmap scan; index merge/intersection/union; heap fetch; visibility map; clustering correlation; residual/recheck; lossy synopsis; partition/file/block pruning; zone map/BRIN; parameterized path; interesting order; row goal; dominance; selectivity crossover; and plan regret.

## Learning Objectives

After this module, you can:

1. define an access path's semantic, property, parameter, visibility, and evidence contract;
2. derive exact/superset bounds from predicates without changing SQL semantics;
3. enumerate sequential, direct, index, covering, bitmap, pruning, and remote candidates;
4. reason about composite prefixes, skip scans, partial/expression indexes, and operator families;
5. cost index entries, heap pages, locality, caching, rechecks, repetition, memory, ordering, and row goals;
6. integrate access paths with join ordering and physical properties;
7. distinguish sound pruning, lossy filtering, and residual correctness;
8. diagnose parameter, skew, visibility, correlation, and metadata-driven path errors;
9. evaluate candidate coverage, semantic equivalence, regret, and workload effects; and
10. deploy access-path changes with reproducible traces, canaries, observability, and rollback.

## Core Exposition

**Bind the requested relation.** Record relation occurrence/alias, snapshot/time-travel version, row-level/security policy, partition/table inheritance scope, projected expressions, filter/join predicates, parameter producers, required order/distribution/locality/rewindability, row goal, and statement mode. Record schema, access structures, operator classes/families, collation, statistics/summaries, physical placement, model/configuration generation, and resource class. Without these bindings, “index applicable” is not reviewable.

**Discover capabilities, not names.** An access structure declares which strategy operators it supports; key and included columns; expression definitions; partial predicate; sort directions/null placement/collation; whether values are returnable; bitmap/plain/backward capabilities; uniqueness; lossiness/recheck; and storage/visibility behavior. A B-tree, GIN, GiST, BRIN, column zonemap, remote secondary index, and materialized projection have different contracts. Do not encode “all indexes can equality/range/order/cover” as a catch-all rule.

**Classify predicates.** Normalize only through semantics-preserving rules. Bind types before comparing expression shape. Separate:

- navigation predicates that define exact or conservative key intervals;
- index conditions evaluated while scanning entries;
- partition/file/block constraints used to prune regions;
- residual predicates evaluated on reconstructed/current rows;
- security/visibility predicates that remain mandatory at the authorized layer.

For `x >= 10 AND x < 20`, a compatible ordered key yields one half-open interval. For `x=1 OR x=9`, use multiple ranges, bitmap union, or equivalent disjunction machinery. A prefix `LIKE 'abc%'` can map to a collation/type-specific range only with correct upper-bound and residual semantics; `LIKE '%abc'` ordinarily cannot navigate a leading B-tree. MySQL 8.4 explicitly documents extracting a less restrictive range condition and applying the full WHERE afterward.

**Composite indexes.** For B-tree `(a,b,c)`, leading equalities plus a range on the first non-equality key normally bound the contiguous scan. Later conditions can reject index entries or rows without reducing the scanned interval. Equality on `a`, range on `b`, and equality on `c` does not generally make c part of one contiguous bound. Skip scan can synthesize searches over distinct missing-prefix values when their count and repositioning cost are favorable; PostgreSQL 18 and MySQL 8.4 document current variants. This is a costed candidate, not a declaration that column order no longer matters.

Expression indexes require the bound expression to match through supported equivalences, including type/collation/function semantics. Partial indexes require proof that the query predicate implies the index predicate for the actual parameter knowledge; similarity or likely truth is insufficient. Unique indexes can provide cardinality/stop guarantees only for matching key/null semantics and valid constraints.

**Sequential and direct paths.** A sequential/column scan is the universal baseline when the source supports it. It can exploit asynchronous/sequential I/O, vectorized predicates, column projection, compression, zone/block pruning, and parallelism; it is not “no optimization.” Direct RID/TID/primary-key/row-key paths require valid identifiers and generation/snapshot semantics. Full index scans may be attractive for covering/order even without selective bounds.

**Ordinary versus covering access.** A secondary-index path usually traverses entries then fetches base rows for visibility and missing columns. Heap/page visits depend on clustering, correlation, duplicate RIDs, batching, caching, and selected row locations—not selected count alone. A covering/index-only candidate requires all needed values to be stored or reconstructible, but MVCC may still require base visibility checks. PostgreSQL 18 documents that index-only benefit depends on all-visible page state; INCLUDE expands payload but does not make visibility disappear.

**Bitmap and index merge.** Scan one or more indexes to produce row/page identifiers, combine them with AND/OR, deduplicate, then visit base pages in physical order and recheck. This can trade random heap access for bitmap creation and more ordered page visits. Memory pressure can make representations lossy, increasing recheck. PostgreSQL 18 documents that bitmap combination loses original index ordering; MySQL 8.4 documents intersection, union, and sort-union variants. Compare a composite index, one selective index plus residual, and bitmap combination rather than assuming “use every available index.”

The executable evaluates deliberately normalized candidates. Its equations are evidence for crossovers and properties, not a model of any named engine.

<!-- bijux-verify: {"id":"finite-access-path-selection","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"seq_cost=2250.00\npoint_btree_cost=37.14\npoint_choice=btree\nmedium_plain_index_cost=3339.50\nmedium_bitmap_cost=422.50\nmedium_choice=bitmap\nbroad_index_cost=5352.00\nbroad_choice=sequential\nordered_limit_covering_cost=4.15\nordered_limit_choice=covering_btree\nbitmap_preserves_order=false\nbitmap_or_cost=270.00\nor_choice=bitmap_union\npruned_partition_scan_cost=225.00\npartition_choice=pruned_partition_scan\nbrin_range_cost=52.00\ncorrelated_range_choice=brin\nresidual_recheck=true\nevidence=deterministic_access_path_equations\n","stderr":""}} -->
```python
seq_page = 1.0
random_page = 4.0
cpu_tuple = 0.01
cpu_index_tuple = 0.005
cpu_operator = 0.0025


def seq_cost(pages, examined_rows):
    return pages * seq_page + examined_rows * (cpu_tuple + cpu_operator)


def plain_index_cost(index_pages, heap_pages, matched_rows):
    return (
        2.0
        + index_pages * seq_page
        + heap_pages * random_page
        + matched_rows * (cpu_index_tuple + cpu_tuple + cpu_operator)
    )


sequential = seq_cost(1000, 100000)
point_btree = plain_index_cost(3, 8, 8)
medium_plain = plain_index_cost(50, 800, 5000)
medium_bitmap = 10 + 50 * seq_page + 300 * seq_page + 5000 * (cpu_tuple + cpu_operator)
broad_index = plain_index_cost(300, 1000, 60000)
ordered_covering = 2 + 2 * seq_page + 20 * (cpu_index_tuple + cpu_operator)
bitmap_or = 10 + 15 + 20 + 200 * seq_page + 2000 * (cpu_tuple + cpu_operator)
partition_scan = seq_cost(100, 10000)
brin_range = 2 + 4 * 10 * seq_page + 4000 * cpu_operator

print(f"seq_cost={sequential:.2f}")
print(f"point_btree_cost={point_btree:.2f}")
print(f"point_choice={'btree' if point_btree < sequential else 'sequential'}")
print(f"medium_plain_index_cost={medium_plain:.2f}")
print(f"medium_bitmap_cost={medium_bitmap:.2f}")
print(f"medium_choice={'bitmap' if medium_bitmap < min(medium_plain, sequential) else 'other'}")
print(f"broad_index_cost={broad_index:.2f}")
print(f"broad_choice={'sequential' if sequential < broad_index else 'btree'}")
print(f"ordered_limit_covering_cost={ordered_covering:.2f}")
print("ordered_limit_choice=covering_btree")
print("bitmap_preserves_order=false")
print(f"bitmap_or_cost={bitmap_or:.2f}")
print(f"or_choice={'bitmap_union' if bitmap_or < sequential else 'sequential'}")
print(f"pruned_partition_scan_cost={partition_scan:.2f}")
print("partition_choice=pruned_partition_scan")
print(f"brin_range_cost={brin_range:.2f}")
print(f"correlated_range_choice={'brin' if brin_range < sequential else 'sequential'}")
print("residual_recheck=true")
print("evidence=deterministic_access_path_equations")
```

**Partition, file, and block pruning.** Partition bounds can prove entire children impossible. File statistics/manifests, row-group min/max, bloom filters, and zone maps can exclude storage regions under their contracts. PostgreSQL 18 stresses that partition pruning follows partition constraints, not indexes, and can occur at plan initialization or repeatedly with execution parameters. BigQuery's current clustered-table documentation describes block pruning from clustering metadata. A pruned region must be impossible for the predicate; unknown, null, truncation, collation, stale metadata, schema evolution, encryption, or unsupported functions must conservatively retain it.

BRIN-like summaries are deliberately lossy. PostgreSQL 18 describes page-range summaries that return all tuples in ranges consistent with the condition, followed by executor recheck. Correlation with physical location determines value: four qualifying ranges can be cheap; scattered values can make nearly every range a candidate. Summary granularity trades metadata size/maintenance for pruning precision.

**Ordering and row goals.** An ordered index can satisfy `ORDER BY` only when key prefix, equality constraints, directions, collation, null ordering, expression binding, and global/local partition order match. Reverse scan may invert directions subject to capability. Bitmap combination visits physical row locations and loses key order. Parallel scans/partition concatenation may deliver only local order unless merged.

For LIMIT/cursor/EXISTS, compare startup and partial demand. A covering index may stop after 20 qualifying entries; a table scan plus sort may need full input. But residual predicates can force many index entries before 20 matches, and OFFSET/keyset semantics differ. Bind the row-goal distribution and correctness of ties rather than treating LIMIT as base selectivity.

**Parameterized paths.** A path may depend on outer keys: repeated index lookup, runtime partition pruning, remote point requests, or memoized batches. Its memo identity includes required parameter relations/expressions. Cost uses outer occurrences, distinct keys, null handling, batch size, cache/memo hit rate, concurrency, and failure/retry. It is unavailable as a standalone base path. Access-path and join-order enumeration must therefore be coupled.

**Remote and columnar paths.** For foreign/object/warehouse sources, candidates may push predicates/projection/aggregation, request row groups, use materialized projections, or fetch remotely. Require capability/version negotiation and semantic compatibility for types, collation, time zones, nulls, functions, policies, and snapshot. Cost requests, bytes, decompression, serialization, network, remote concurrency/quotas, egress money, and fallback. A remote “index used” label is insufficient evidence of transferred work.

**Dominance and retention.** Candidate a dominates b only if it is no worse for the same semantics, parameter requirements, delivered properties, startup/total objective, resources, and uncertainty. Retain an ordered/covering/partition-local/low-memory/fast-start candidate even when its local scalar is higher if a parent can exploit it. Bound the frontier with explicit property relevance and safe/heuristic pruning records.

**Uncertainty and sensitivity.** Perturb cardinality, heap-page count/correlation, visibility fraction, cache, prefix NDV for skip scan, bitmap density/lossiness, partition/runtime parameter class, summary false-positive rate, row-goal hit position, remote latency, and repeated-probe distinctness. Find path crossover boundaries. A point estimate barely favoring random index fetches over a scan may not justify plan churn if plausible error crosses the boundary; choose a robust plan or preserve parameter-sensitive variants.

**Diagnose first divergence.** Freeze query bindings, parameters, snapshot, schema/index definitions, access capabilities, statistics/summaries, configuration, model version, storage/cache/concurrency, and plan trace. Ask in order: was the candidate enumerated; was predicate matching/implication legal; were bounds/residuals correct; were required properties/parameters represented; were cardinality/page/visibility/pruning estimates correct; were costs/composition correct; was the path pruned/timed out; did runtime differ by cache, skew, or interference? Forcing an index does not identify the cause.

**Evaluate in layers.** Generate finite datasets with nulls, duplicates, boundary values, collations, casts, partial predicates, expression keys, multiple versions, unsummarized/lossy regions, partitions, and parameters. Compare every path result as a bag against a trusted full scan at the same snapshot/policy. Verify intervals and residuals, no false-negative pruning, delivered ordering, covering visibility, OR deduplication, and parameter contracts. Then compare candidate costs/rankings with actual pages/bytes/rows/rechecks/startup/total/memory, execute alternatives safely, and report regret and workload outcomes.

**Productionize safely.** Version access-matching rules, capability registry, cost/cardinality models, statistics/summaries, and configuration. Shadow old/new candidates and decisive traces. Canary selected fingerprints/tenants with result hashes or stronger equivalence checks, storage/request/resource budgets, control cohort, kill switch, and rollback. Monitor planning latency, candidate/fallback rates, path churn, examined/emitted rows, heap fetches, rechecks, pruning, cache, spill, remote bytes/requests, latency tails, and workload interference. Redact literals and tenant-sensitive distribution/metadata.

## Definitions and Notation

- **R, q, c, p**: bound relation occurrence, predicate, required columns, and physical properties.
- **A(R,q,c,p)**: feasible enumerated access paths.
- **Navigation bound**: exact or conservative key/region restriction used before residual evaluation.
- **Residual/recheck**: predicate required after access to restore exact semantics.
- **Equality prefix**: consecutive leading composite keys fixed by equality-like constraints.
- **Covering path**: supplies required values without ordinary base-row payload fetch, subject to visibility/version rules.
- **Correlation/clustering**: association between access-key order/value ranges and physical row placement.
- **Lossy summary**: admits false-positive regions/rows and requires recheck but must not admit false negatives.
- **Parameterized path**: requires values from a declared outer relation set.
- **Delivered order**: exact sequence property, including direction/collation/null/global scope.
- **Crossover**: context where two path objective values are equal and preference can reverse.
- **Path regret**: realized selected-path objective minus realized reference-best feasible path.

An access condition and a residual can originate from the same SQL predicate. The split is an execution contract, not a weakening of query semantics.

## Mechanisms, Invariants, or Proof Structure

**Superset-and-recheck proof.** Let Q be rows satisfying SQL predicate q and B be rows/regions admitted by access bounds. Sound access requires `Q subseteq B`. Evaluating q exactly as residual on B returns Q. If bounds are exact, residual may be redundant only when the access method certifies identical semantics. Lossy pruning is safe when it enlarges B, never when it excludes any member of Q.

**Composite B-tree interval.** Leading equalities select one prefix range; the first following inequality supplies an interval within that prefix. Later key predicates may filter entries but do not generally create one narrower contiguous interval. Skip scan decomposes missing-prefix values into multiple searches; its correctness is union coverage, while profitability depends on prefix NDV and repositioning.

**Bitmap set algebra.** Exact identifier sets satisfy intersection for AND and union for OR; union requires deduplication under bag row identity before row production. Lossy page/range bitmaps represent supersets, so final predicate recheck is mandatory. Physical-order visitation does not imply key-order delivery.

**Pruning invariant.** A region may be removed only if metadata plus predicate semantics prove its candidate set empty. Unknown/unsupported/stale-without-safety evidence yields “keep.” For min/max range `[lo,hi]` and query `x>k`, prune only when `hi<=k` under compatible type/collation/null semantics.

**Dominance condition.** Discard b for a only when both have identical semantic/parameter obligations and a is no worse in every future-relevant property/resource/objective dimension. Lower local total cost alone cannot dominate order, covering, startup, locality, or memory differences.

**Evidence separation.** Executable arithmetic establishes only finite model decisions. Differential bags establish semantic equivalence for tested data/grammar. Path execution establishes scoped regret. Workload canaries establish scoped operational outcomes. None proves universal path optimality or safe pruning for untested metadata.

## Alternatives and Trade-Offs

**Sequential/column scans** have low setup, predictable streaming, and good broad-access locality; they examine more storage. **Plain index scans** provide selective navigation, parameterization, and order; scattered base fetches can dominate. **Covering/index-only scans** avoid payload fetches and can preserve order; wider indexes cost storage/cache/write amplification and visibility can erase the benefit.

**Composite indexes** efficiently serve common conjunction/order shapes; column order narrows reuse. **Separate indexes plus bitmap/index merge** flexibly combine predicates and OR branches; bitmap creation/recheck costs memory and loses order. **Skip scan** recovers some suffix usefulness; many prefix values make repeated seeks approach/full-scan cost.

**Partition pruning** gives exact structural exclusion when predicates align; too many partitions increase planning/metadata overhead and non-aligned predicates gain little. **BRIN/zone maps** are tiny and effective on clustered data; they are lossy and weaken with disorder. **Full secondary-index scan** can cover/order narrow rows; table/column scans may be better for broad payloads.

**Compile-time paths** are stable and cacheable; unknown/skewed parameters can mislead. **Runtime pruning/parameterized paths** exploit actual values; they add repeated work, state, and observability complexity. **Remote pushdown** reduces transfer and exploits source indexes; semantic mismatch, quotas, failures, and opacity require conservative fallback.

**Hints/forced paths** provide a diagnostic or emergency control; they freeze assumptions and can age badly. Prefer repairing predicate binding, statistics, visibility/summaries, capability enumeration, costing, or parameter strategy, then retain hint removal criteria.

## Failure Modes and Misconceptions

1. “An indexable-looking predicate is sargable” ignores types, casts, collation, expressions, and operator support.
2. “Index condition means no residual” ignores conservative bounds and lossy methods.
3. “Every composite-key predicate narrows the range” ignores equality-prefix/first-range structure.
4. “Skip scan makes column order irrelevant” ignores prefix NDV and repeated seeks.
5. “Matching 1,000 rows means 1,000 page reads” ignores clustering, duplicates, cache, and batching.
6. “INCLUDE guarantees index-only execution” ignores stored values, visibility, snapshot, and access-method support.
7. “Bitmap AND/OR preserves index order” it visits physical locations and needs separate ordering.
8. “Bitmap OR may emit duplicates” row identifiers must be deduplicated before row production.
9. “Partition pruning is index usage” it follows partition bounds/constraints independently.
10. “Lossy synopsis can skip probable nonmatches” sound pruning needs impossibility, not probability.
11. “LIMIT 20 means inspect 20 entries” residual selectivity and ties can require much more work.
12. “Parameterized index path is globally available” it requires its declared producer and invocation model.
13. “Lowest local path cost is globally best” order, covering, distribution, startup, and join use can reverse it.
14. “Forcing the faster index proves an optimizer bug” environment/parameter/cache differences and missing evidence remain.

## Worked Examples

### Example 1

**Exact range.** Compatible integer B-tree and `x>=10 AND x<20` produce `[10,20)`. Nulls do not satisfy either comparison. Conclusion: exact bounds can implement the predicate when operator semantics match.

### Example 2

**Conservative string bound.** A prefix search maps to a collation-aware candidate range but complex collation may admit false positives; residual LIKE validates them. Conclusion: range navigation and predicate truth are separate contracts.

### Example 3

**Composite suffix.** Index `(tenant,created_at,status)` with tenant equality and time range scans one tenant/time interval; status rejects entries but normally does not shorten that interval. Conclusion: later keys are not automatically navigation keys.

### Example 4

**Selectivity crossover.** The executable chooses B-tree at eight rows, bitmap at 5,000 rows, and sequential scan at 60,000. Conclusion: path choice depends on page locality and processing terms, not a universal selectivity threshold.

### Example 5

**Covering visibility.** Query needs indexed key plus included payload, but recently modified heap pages lack all-visible status. Base visibility checks remain. Conclusion: logical covering eligibility does not guarantee heap-free physical execution.

### Example 6

**Bitmap OR.** Separate predicates yield overlapping identifier sets `{1,2,3}` and `{3,4}`. Union is `{1,2,3,4}`, not five row occurrences; each base row is then evaluated once for the OR. Conclusion: identifier deduplication preserves scan semantics.

### Example 7

**Order loss.** Two B-tree scans are bitmap-ANDed, then heap pages are visited by location. `ORDER BY key LIMIT 20` needs a sort/top-N, while one less-selective ordered index might stop early. Conclusion: cost properties can outweigh local filtering.

### Example 8

**Runtime partition pruning.** Inner nested-loop key determines month per outer row. Compile time cannot choose a month, but execution-time parameter changes can prune partitions. Conclusion: parameterized access includes runtime pruning and invocation evidence.

### Example 9

**Lossy block summary.** Four BRIN ranges might contain `timestamp>k`; all rows in those ranges are read/rechecked, while 96 ranges are safely excluded. Disorder expands candidate ranges but must not hide rows. Conclusion: synopsis precision changes work, not correctness.

### Example 10

**Production regression.** New visibility estimate selects an index-only path for a hot, frequently updated table; heap fetches and p99 rise. Compare first divergence at all-visible fraction, shadow a corrected estimate, preserve ordered alternative, canary write-heavy tenants, and monitor heap fetches/cache/storage. Conclusion: repair the causal input and verify workload regret.

## Cross-Program Connections

- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md): trees, bitmaps, bloom filters, summaries, cache locality, and external-memory structures implement paths.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md): interval algebra, set operations, pruning proofs, cost crossovers, and robust choice formalize selection.
- [Data Engineering](../../19-data-engineering/ROADMAP.md): partitions, file/row-group metadata, clustering, compaction, schema evolution, and data quality determine pruning.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md): placement, serving layouts, materializations, and workload ownership shape available paths.
- [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md): remote storage, sharding, routing, replicas, and network/resource constraints extend access planning.
- [Security Engineering](../../25-security-engineering/ROADMAP.md): row policies, encryption, tenant isolation, side channels, and metadata/literal access constrain pushdown and traces.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): statistics/synopsis services, resource classes, observability, canaries, and rollback operationalize path changes.

## References

1. P. Griffiths Selinger et al., [“Access Path Selection in a Relational Database Management System”](https://doi.org/10.1145/582095.582099), *SIGMOD 1979*. Primary cost-based access-path and interesting-order foundation.
2. PostgreSQL Global Development Group, [PostgreSQL 18: Using `EXPLAIN`](https://www.postgresql.org/docs/18/using-explain.html), retrieved 2026-08-30. Current scan, bitmap, index-only, skip-scan, filter, row, and cost interpretation.
3. PostgreSQL Global Development Group, [PostgreSQL 18: Index Cost Estimation Functions](https://www.postgresql.org/docs/18/index-cost-estimation.html), retrieved 2026-08-30. Current index selectivity, correlation, pages, and access-cost extension contract.
4. PostgreSQL Global Development Group, [PostgreSQL 18: Multicolumn Indexes](https://www.postgresql.org/docs/18/indexes-multicolumn.html), retrieved 2026-08-30. Current equality-prefix, range, later-key, and skip-scan behavior.
5. PostgreSQL Global Development Group, [PostgreSQL 18: Combining Multiple Indexes](https://www.postgresql.org/docs/18/indexes-bitmap-scans.html), retrieved 2026-08-30. Current bitmap AND/OR, physical visitation, ordering loss, and index-design trade-offs.
6. PostgreSQL Global Development Group, [PostgreSQL 18: Index-Only Scans and Covering Indexes](https://www.postgresql.org/docs/18/indexes-index-only-scans.html), retrieved 2026-08-30. Current returnability, required columns, visibility-map, and INCLUDE behavior.
7. PostgreSQL Global Development Group, [PostgreSQL 18: Table Partitioning](https://www.postgresql.org/docs/18/ddl-partitioning.html), retrieved 2026-08-30. Current plan/init/execution pruning and partition/index distinction.
8. PostgreSQL Global Development Group, [PostgreSQL 18: BRIN Indexes](https://www.postgresql.org/docs/18/brin.html), retrieved 2026-08-30. Current page-range summaries, correlation, granularity, lossiness, recheck, and maintenance.
9. Oracle, [MySQL 8.4: Range Optimization](https://dev.mysql.com/doc/refman/8.4/en/range-optimization.html), retrieved 2026-08-30. Current interval extraction, residual filtering, composite ranges, skip scan, and planning-memory limits.
10. Oracle, [MySQL 8.4: Index Merge Optimization](https://dev.mysql.com/doc/refman/8.4/en/index-merge-optimization.html), retrieved 2026-08-30. Current intersection, union, sort-union, cost selection, switches, and hints.
11. SQLite Project, [Query Planning](https://www.sqlite.org/queryplanner.html), retrieved 2026-08-30. Current rowid/index lookup, multiple-result handling, covering, ordering, and planner trade-offs.
12. Google Cloud, [Introduction to Clustered Tables](https://docs.cloud.google.com/bigquery/docs/clustered-tables), retrieved 2026-08-30. Current block organization/pruning and processed-byte semantics for clustered tables.

## Exercises

### Exercise 1

For B-tree `(tenant,created_at,status)` and predicates `tenant=7`, time interval, `status='open'`, derive navigation bounds, index conditions, residuals, and delivered order.

### Exercise 2

Prove the superset-and-recheck rule and apply it to lossy page summaries and bitmap OR with overlapping identifiers.

### Exercise 3

Recompute every executable cost and diagnose which assumptions would move the point/index, medium/bitmap, and broad/scan crossovers.

### Exercise 4

Design candidates for `ORDER BY created_at DESC LIMIT 20` over monthly partitions with a tenant parameter supplied by an outer join. Compare compile-time, runtime-pruned, bitmap, and covering paths.

### Exercise 5

Design an elite access-path validation and rollout system covering semantic matching, visibility, pruning soundness, properties, parameters, uncertainty, regret, privacy, canaries, and rollback.

## Answers to the Exercises

### Answer 1

The equality prefix fixes tenant 7. The first following range bounds `created_at` to the exact compatible half-open/closed interval dictated by the SQL operators. `status='open'` can be evaluated on index entries if the access method supports it, saving base-row visits, but it normally does not shorten the contiguous tenant/time interval because it follows a range key. Recheck status if index semantics/lossiness require it; also evaluate any non-index predicate, row policy, and visibility on the authorized current row. The scan delivers `(tenant,created_at,status)` index order; with tenant fixed, it can deliver created_at direction (and status as a later tie component) subject to requested direction, collation/nulls, partition/global merge, and residual effects. It does not guarantee deterministic order among equal keys unless uniqueness/tie keys provide it.

### Answer 2

Let Q be exact qualifying row identifiers and B the candidate identifiers admitted by bounds. If `Q subseteq B`, exact residual evaluation returns `{r in B | q(r)}=Q`: every Q row is present and accepted, while every false positive is rejected. A lossy page summary includes all rows in every possibly matching page range; it may include many false positives but must retain every page containing Q, then recheck q. For OR, exact sets B1/B2 combine as set union; overlapping ID 3 appears once in candidate identity set, after which the full OR predicate is checked. If a lossy bitmap marks pages rather than rows, union remains a page superset and all candidate tuples are rechecked. Any false-negative bound violates the subset premise and cannot be repaired by residual evaluation.

### Answer 3

Sequential is `1000 + 100000*(.01+.0025)=2250`. Point B-tree is `2+3+8*4+8*(.005+.01+.0025)=37.14`. Medium plain is `2+50+800*4+5000*.0175=3339.50`; bitmap is `10+50+300+5000*.0125=422.50`. Broad index is `2+300+1000*4+60000*.0175=5352`. Covering LIMIT is `2+2+20*(.005+.0025)=4.15`. Bitmap OR is `10+15+20+200+2000*.0125=270`. Partition scan is `100+10000*.0125=225`. BRIN is `2+4*10+4000*.0025=52`. Lower random-page price/cache or stronger clustering moves index crossovers broader; more heap pages, width, residual work, or stale visibility moves them narrower. Bitmap memory/setup/lossiness and candidate heap pages move its crossover. Parallel/vectorized scan lowers scan cost. Ordered LIMIT/covering changes the objective via startup and sort avoidance; parameter repetition and cache change per-probe costs. Recompute under measured distributions rather than transplanting these constants.

### Answer 4

Bind tenant parameter dependency, month predicate, DESC/null/collation/tie requirements, projected columns, snapshot, and row goal. A generic compile-time plan may retain an Append of partitions with per-partition ordered indexes and a merge/top-N, plus a robust broader scan alternative. Initialization/execution pruning can remove months once time/outer parameters are known; a parameterized tenant/time index can scan DESC and stop after 20 residual-qualified visible rows. A covering variant avoids payload fetches only when all values are returnable and visibility permits. Bitmap AND of tenant/time can reduce pages but loses order and needs top-N; it may win when many rows qualify and heap locality dominates. Compare repeated outer keys, batching/memoization, per-parameter skew, number of partitions, local-versus-global order, visibility, residual hit position, startup/total, memory, and sort/exchange. Retain parameterized path only under its producer; use runtime pruning safely; preserve a generic fallback for unknown/OOD classes.

### Answer 5

Create a capability registry with exact types, operators/families, collations, expressions, partial predicates, returnability, ordering, bitmap, lossiness, visibility, and parameter contracts. Generate finite/adversarial bags across nulls, duplicates, boundary values, casts, collations, LIKE/ranges, composite gaps, OR overlap, versions, policies, partitions, stale/unknown/unsummarized regions, and remote failures. Differentially compare every candidate with an authorized full-scan oracle at one snapshot; prove `Q subseteq B`, residual exactness, no false-negative pruning, ordering, visibility, deduplication, and parameter scope. Test candidate enumeration/dominance against brute-force small cases. Calibrate pages/bytes/entries/rechecks/startup/total/memory under cache, correlation, width, bitmap density, prefix NDV, visibility, parameter repetition, remote latency, and concurrency; report coverage, ranking, executed-alternative regret, tails, resource and workload effects. Version rules/models/statistics/summaries/configuration; least-privilege and redact literals/tenant metadata; threat-model timing/metadata leakage and poisoned summaries/feedback. Shadow old/new, then canary bounded fingerprints/tenants with result equivalence, storage/request/SLO gates, control cohort, kill switch, immutable rollback, and removal criteria for hints. Evidence supports only declared versions, grammars, snapshots, metadata and environments; it does not prove universal matching, pruning soundness, optimality, privacy, fairness, certification, or deployment fitness, and external review requires named humans.
