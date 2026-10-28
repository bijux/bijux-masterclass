---
module_id: DBE-052
program: Database Engineering
level: 2
module_number: 52
title: Sequential and Index Scans
status: complete
last_verified: 2026-08-30
---

# Sequential and Index Scans

## One-Page Review

### Governing question

When should an execution engine read a relation in physical sequence, navigate an index, or combine both, and what must each path prove about candidates, visibility, predicates, order, and resource cost?

### Essential definitions

A **sequential scan** visits the relation's eligible physical units and tests tuples in scan order. An **index scan** navigates an auxiliary search structure to obtain candidate tuple locators or stored values, then applies visibility and residual conditions. An **index-only scan** can return referenced values from the index when it contains every needed value and the engine can establish row visibility without an ordinary base-row visit. **Sargability** means a predicate has a form that an access method can use to delimit or probe its search space. **Selectivity** is the expected qualifying fraction. **Clustering/correlation** describes how closely index-key order agrees with base-row location. A **residual predicate** is a condition not fully discharged by navigation and therefore rechecked on candidates.

### Central model, mechanism, or theorem

Access-path choice is a proof-and-cost decision. First prove that the path cannot omit a qualifying visible row and cannot emit a nonqualifying row after required rechecks. Then estimate startup, index traversal, leaf work, distinct base pages, visibility/version work, predicate CPU, prefetch, caching, parallelism, ordering, and early-stop behavior. A scan is not good or bad by name: sequential access often wins broad or poorly clustered retrieval; index access often wins selective or order-and-limit retrieval; covering access can change the crossover by removing base fetches.

### Critical invariants

- Every visible tuple satisfying the logical predicate appears with the correct multiplicity, and no other tuple survives.
- Index conditions delimit candidates only where the operator class, collation, type, and predicate semantics justify them.
- Candidate locators are revalidated against snapshot/version state and every residual condition.
- Lossy summaries or pages are rechecked; absence is concluded only from conservative metadata.
- Physical scan order is not promised as SQL result order unless an applicable ordered path satisfies the complete `ORDER BY` contract.
- Early termination is legal only when the parent no longer needs rows or ordering makes the remaining range irrelevant.
- Cost estimates never weaken correctness, locking, isolation, cancellation, or resource-accounting obligations.
- Plan evidence is bound to data distribution/layout, statistics, parameters, cache, concurrency, engine/build, and settings.

### Common failures

Common failures are treating every sequential scan as defective; assuming an index lookup returns a visible final row; confusing an index condition with a residual filter; applying a function or coercion that prevents useful navigation; ignoring leading-column and range boundaries; expecting a covering index to avoid all base visits under MVCC; claiming index order without matching direction/null/collation semantics; estimating heap visits as returned rows despite scatter and dead versions; forcing a path from a tiny fixture; benchmarking only a warm cache; and adding wide or overlapping indexes without pricing write amplification.

### Compact example

For 96 rows stored eight per page, a sequential scan reads 12 data pages. An ordered range of 24 keys touches three heap pages when clustered but all 12 under a deterministic scattered layout. With one root and three modeled leaf pages, the clustered index path touches seven pages while the scattered path touches sixteen. The same predicate and index can therefore be cheaper or dearer than sequential access solely because physical locality changes. This finite page-touch model explains a mechanism; it is not a hardware or optimizer benchmark.

### Connections

Retrieve [B+ Tree Search and Range Scan](032-b-tree-search-and-range-scan.md), [Composite and Covering Indexes](035-composite-and-covering-indexes.md), [Bitmap and BRIN-Style Indexes](037-bitmap-and-brin-style-indexes.md), [Snapshot Visibility](047-snapshot-visibility.md), and [Logical and Physical Plans](051-logical-and-physical-plans.md). Continue through the Database Engineering [roadmap](../ROADMAP.md) to join, aggregation, sort, vectorized, and parallel operators.

## Governing Question

How can a database choose and execute sequential, index, and index-only access paths without mistaking candidate discovery for SQL correctness or a simplified cost estimate for measured performance?

## Why This Matters

Scans sit at the leaves of most query plans. Their output cardinality, latency, order, and locality determine how much work every parent join, aggregate, sort, or exchange performs. A poor estimate can turn one leaf decision into millions of unexpected random fetches or parameterized probes. An incorrect scan can silently lose data, violate snapshot semantics, or return values from the wrong row version.

The folk rule “indexes are fast” omits the actual comparison. Sequential access has low setup, predictable page progression, prefetch opportunities, compact per-tuple loops, and effective parallel partitioning. An index adds root-to-leaf navigation and leaf examination; unless it covers the query, it may cause one base-row fetch per candidate in an order hostile to storage and cache. When many candidates land on the same pages, clustering or batching amortizes that cost. When few are needed—or a matching index can stop after a small `LIMIT`—the index avoids most relation pages.

Correctness is subtler than cost. An index entry commonly denotes a candidate row location, not a final logical row. The executor must establish visibility for the statement's snapshot, follow engine-specific version/location rules, acquire required locks, and apply residual or lossy rechecks. A predicate that is mathematically equivalent over simple integers may not be interchangeable under SQL nulls, collations, floating values, time zones, nondeterministic functions, implicit casts, or expression-index definitions.

Modern systems also broaden “scan.” Row stores expose sequential, ordered index, bitmap-plus-heap, and index-only paths. Columnar and analytical engines scan vectors while skipping row groups through conservative min/max metadata; remote engines push projections/predicates into file or service readers; distributed systems prune partitions and schedule parallel fragments. The durable questions remain: what space is searched, what can be excluded soundly, what must be rechecked, which physical properties are delivered, and what resources are consumed?

## Prerequisites and Retrieval

You should understand relations and bags, three-valued predicates, pages and tuple locators, buffer pools, B+ trees, composite/covering/partial indexes, MVCC snapshots, cardinality/selectivity, physical ordering, and plan estimates versus measurements. Retrieve candidate set, key range, operator class, collation, residual/recheck, covering payload, visibility map or equivalent summary, correlation, startup cost, total cost, prefetch, vector batch, partition pruning, and early stop.

DBE-051 separated logical requirements from physical implementations. Here the logical operator is a relation scan with predicate and projection. We refine it into physical alternatives and prove their result/property contracts before comparing costs. Bitmap and summarizing access were introduced in Level I; this module uses them as comparison points rather than re-deriving their internal structures.

## Learning Objectives

After this module, you can:

1. specify sequential, index, and index-only scan contracts independently of one product's node names;
2. trace page, tuple, index-entry, visibility, predicate, projection, and cancellation work;
3. separate access conditions, residual filters, lossy rechecks, and partition/row-group pruning;
4. derive B+ tree equality/range boundaries for composite keys and identify sargability barriers;
5. estimate scan crossover from selectivity, distinct page touches, clustering, cache, row width, and early stopping;
6. reason about delivered ordering, direction, null placement, collation, and `LIMIT`;
7. explain why covering data is necessary but not always sufficient for index-only execution;
8. diagnose estimate-versus-actual and scan-plan regressions without plan-shape dogma;
9. design differential, adversarial, and operational tests for scan correctness and performance; and
10. evaluate scan/index changes as read-write-storage-reliability trade-offs.

## Core Exposition

**Begin with the logical contract.** For relation state (D), snapshot (S), predicate (P), and projection (E), a scan must produce the bag of (E(t)) for every tuple version (t) visible under (S) where (P(t)) evaluates TRUE. FALSE and UNKNOWN do not qualify. Multiplicity follows visible input versions and SQL operators above the scan. Required row locks, predicate/range protection, or DML target identity extend this result contract.

The physical access method may produce a superset of candidates. Soundness after recheck requires every emitted row to be visible and satisfy (P). Completeness requires every visible tuple satisfying (P) to be reached. A conservative zone map or bitmap is allowed false positives, never false negatives. A stale, lossy, or approximate structure is safe only when its maintenance and recheck protocol preserves these properties.

**A sequential scan is a physical traversal, not a promise of logical order.** A row-store implementation typically initializes a relation/snapshot, obtains a page or extent range, pins or reads pages through the buffer manager, identifies candidate line pointers/versions, checks visibility, evaluates predicates, projects columns, and yields rows or batches. It releases pins/latches according to lifecycle rules and responds to cancellation. Read-ahead, large I/O, ring/admission policy, vectorized predicates, late materialization, parallel ranges, and storage-zone pruning can alter mechanics without altering semantics.

Sequential scan cost is not simply table bytes. It includes eligible pages after partition/segment pruning, cache/device behavior, decompression, version/dead-row checks, predicate CPU, projection width, and parent demand. Parallel workers can reduce elapsed time but add setup, coordination, exchange, imbalance, and interference. A `LIMIT` can stop an unordered scan after enough qualifying rows only when any qualifying rows are acceptable; it cannot infer which rows are globally first for an unmatched `ORDER BY`.

**An index scan separates navigation from row reconstruction.** For a B+ tree, the executor forms legal search keys/ranges, descends internal pages, walks qualifying leaf entries, and obtains stored payload and/or a base tuple locator. It then visits the base structure when needed, resolves the visible row version under engine rules, evaluates residual conditions, and projects. Multiple disjoint ranges, `IN` probes, skip-scan-like repeated seeks, or parameterized probes can multiply root/leaf searches.

Index predicates have roles. A boundary condition narrows the leaf interval. A condition evaluable from index values can reject candidates before base fetch even if it does not narrow the interval. A base-table filter runs after fetch. A lossy operator supplies a recheck condition. Explain output should preserve these distinctions because moving work earlier may improve cost while the final predicate remains unchanged.

**Composite navigation is lexicographic and implementation-specific at its edges.** For a conventional B+ tree on `(tenant_id, created_at, id)`, equality on `tenant_id` plus a range on `created_at` defines a contiguous interval; `id` may be checked in the index yet not narrow that interval after the range dimension. A predicate only on `created_at` cannot generally jump to one contiguous range because all tenant prefixes interleave. Some engines use skip scanning when leading distinct values are few, but that is a costed repeated-search technique, not a universal leftmost-prefix repeal.

Sargability is semantic compatibility, not cosmetic syntax. `amount >= 100` can delimit a compatible ordered numeric index. `lower(email) = value` needs an engine-supported matching expression index or rewrite; a plain email index cannot assume the function preserves its order/equality rules. Implicit type conversion, collation mismatch, arithmetic around the indexed column, time-zone transformation, nondeterministic expression, and leading-wildcard pattern can block or change navigation. Rewriting must preserve overflow, precision, null, collation, and time-boundary behavior.

**Index-only access has two independent obligations.** First, all values needed for navigation, residual predicates, projection, and ordering must be available from index entries or derivable safely. Included/payload columns can cover output without changing search ordering. Second, the executor must establish visibility. PostgreSQL 18, for example, may avoid a heap visit when the corresponding all-visible map bit proves the page's tuples old enough; otherwise it still visits the heap. Other storage engines embed versions differently. “Covering” describes data availability, not a universal zero-base-I/O guarantee.

Wide covering indexes trade read locality against larger leaves, lower fanout, more pages, cache pressure, write/WAL amplification, split/compaction work, maintenance duration, and storage. Payload types may face index tuple/type restrictions. Coverage should be designed for a measured workload and reviewed after query/schema changes, not achieved by copying an entire table into each index.

**Ordering is a physical property.** A compatible ordered index can deliver key order forward or backward, subject to engine rules for mixed directions, null placement, collation, and tie-breaking. It may satisfy both search and order, making `ORDER BY ... LIMIT n` especially favorable because execution can stop after the first (n) qualifying rows. An index plus random base fetches can still lose economically to sequential scan plus sort for a broad result. Bitmap paths commonly sacrifice index order to batch base-page access.

Never expose incidental heap, row identifier, leaf, worker, or batch order as an application contract. SQL without a sufficient `ORDER BY` leaves presentation order unspecified. Even with `ORDER BY`, ties need enough keys if deterministic pagination is required. Changes in plan, vacuum/compaction, page splits, parallel scheduling, or replicas can reveal a test's false assumption.

**The cost crossover depends on distinct page visits, not selectivity alone.** A simplified model is


(C_{seq}=P_s c_{seq}+N_s c_{vis/pred}+C_{startup}),


(C_{idx}=Hc_{seek}+L_ic_{leaf}+D_hc_{heap}+N_cc_{vis/pred}+C_{startup}),


where (P_s) is scanned relation pages, (H) tree/search work, (L_i) leaf pages, (D_h) distinct heap pages reached, and (N_c) candidates. The coefficients depend on cache, storage, concurrency, prefetch, compression, and CPU. Clustering reduces (D_h); covering may reduce it toward zero; scattered matches drive it toward the relation page count. A bitmap can sort/batch locators to exchange startup and memory for locality.

The following finite model makes the distinct-page term observable. It stores 96 logical keys on 12 eight-row pages. The clustered layout places adjacent keys together; the scattered layout maps keys through a permutation. Two index pages model root/leaf access. It deliberately excludes cache, concurrency, MVCC, compression, prefetch, CPU, and real device latency.

<!-- bijux-verify: {"id":"scan-page-touch-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"matches=1 seq=12 clustered_index=3 scattered_index=3 index_only=2\nmatches=8 seq=12 clustered_index=3 scattered_index=10 index_only=2\nmatches=24 seq=12 clustered_index=7 scattered_index=16 index_only=4\nmatches=48 seq=12 clustered_index=13 scattered_index=19 index_only=7\nmatches=96 seq=12 clustered_index=25 scattered_index=25 index_only=13\nevidence=finite_page_touch_model\n","stderr":""}} -->
```python
from math import ceil

ROW_COUNT = 96
ROWS_PER_PAGE = 8
TABLE_PAGES = ROW_COUNT // ROWS_PER_PAGE
INDEX_ROOT_PAGES = 1


def heap_pages(matches: int, physical_rid) -> int:
    return len({physical_rid(key) // ROWS_PER_PAGE for key in range(matches)})


for matches in (1, 8, 24, 48, 96):
    clustered = heap_pages(matches, lambda key: key)
    scattered = heap_pages(matches, lambda key: (key * 37) % ROW_COUNT)
    leaf_pages = ceil(matches / ROWS_PER_PAGE)
    print(
        f"matches={matches} seq={TABLE_PAGES} "
        f"clustered_index={INDEX_ROOT_PAGES + leaf_pages + clustered} "
        f"scattered_index={INDEX_ROOT_PAGES + leaf_pages + scattered} "
        f"index_only={INDEX_ROOT_PAGES + leaf_pages}"
    )

print("evidence=finite_page_touch_model")
```

The model counts logical page identities, not buffer misses: repeated touches may hit cache, while concurrent eviction may make one page expensive repeatedly. It also counts index pages coarsely. Its valid conclusion is comparative: locality and coverage can move the crossover even at fixed selectivity.

**Estimation determines which correct path is chosen.** Planners use relation/page counts, null fractions, distinct values, frequency lists, histograms, correlation, expression/extended statistics, parameter information, and cost configuration. Stale samples, skew, cross-column dependence, parameter-sensitive predicates, and casts can misestimate candidates or distinct heap pages. PostgreSQL documentation explicitly treats plan costs as arbitrary units influenced by parameters such as sequential/random page cost and effective cache assumptions; they are not milliseconds or portable across engines.

Diagnose estimates at each boundary: estimated versus actual rows, loops/searches, rows removed by index recheck and filter, heap/base fetches, cache reads/hits, bytes, prefetch, decompression, worker balance, and time-to-first versus time-to-last row. A parent nested loop can execute an inner index scan thousands of times, so per-loop values must be interpreted with loop counts. Early `LIMIT` termination can make a child show fewer actual rows than its completion estimate without an estimation defect.

**Correct implementations coordinate with storage and concurrency.** A scan must tolerate page splits, compaction, version chains, forwarded rows, reclamation, and concurrent index maintenance according to the engine's latch/epoch/lock protocol. Tuple locators cannot be dereferenced after their protection expires. Predicate/range protection at serializable isolation may depend on the chosen access path. DML scans must preserve target identity, avoid duplicate modification where required, and recheck qualifications after locking when the engine's semantics demand it.

Cancellation and faults are part of the lifecycle: release pins, iterator state, temporary bitmaps, prefetch requests, and worker resources; do not leak a partially initialized scan. Remote/object-store scans need retry/idempotency and snapshot/version binding. Checksums, decompression errors, missing objects, and authorization changes must fail explicitly rather than become empty input.

**Verification needs independent oracles and representative environments.** For correctness, compare sequential and candidate index paths against an independent logical evaluator across empty relations, duplicates, nulls, boundary keys, collations, updated/deleted versions, partial/expression indexes, lossy summaries, concurrent change schedules, forward/backward scans, and cancellation. Verify bags and explicit order separately. Plant stale or corrupted metadata in engine-level fault tests and demand conservative fallback or explicit failure.

For performance, sweep cardinality, selectivity, clustering, row width, coverage, cache state, device/storage, churn/dead versions, statistics, parameters, `LIMIT`, concurrency, and parallelism. Record distributions and tail latency rather than one run. Validate the result before interpreting timing. Compare total workload effects—writes, log/replication bytes, vacuum/compaction, memory, and recovery—not only the target read.

## Definitions and Notation

- (R): logical relation; (S): statement snapshot; (P(t)): three-valued predicate on tuple version (t); (E(t)): projected result.
- (Q(S,R,P,E)): required output bag of projected visible tuples for which (P) is TRUE.
- **Sequential/full scan**: traversal of eligible physical relation units, possibly after safe coarse pruning.
- **Index scan**: access through a maintained search structure, commonly followed by base-row fetch and recheck.
- **Index-only scan**: path satisfying value and visibility needs without ordinary base-row access for some or all candidates.
- **Candidate**: a location/value that might satisfy the query; candidacy alone is not final qualification.
- **Search/index condition**: condition used to navigate or reject within the access method.
- **Residual/filter/recheck**: condition evaluated after an earlier access stage did not fully decide truth.
- **Sargable**: semantically compatible with an access method's search operation and representation.
- **Selectivity** (sigma): expected qualifying rows divided by eligible input rows.
- **Correlation/clustering**: relationship between logical key order and base physical location.
- (P_s,L_i,D_h,N_c): scanned base pages, index leaf pages, distinct heap/base pages, and candidate tuples.
- **Covering payload**: stored index value usable for predicate/projection but not necessarily navigation.
- **Delivered order**: sequence property proven by the scan, including key expressions, direction, null placement, and collation.
- **Early stop**: ending an iterator because the parent demand/order proves remaining rows unnecessary.

## Mechanisms, Invariants, or Proof Structure

Prove a scan in layers. First define the visible qualifying bag (Q). For sequential access, prove the page/partition iterator covers every physical location that could contain a visible tuple in (R); safe pruning excludes only units whose conservative metadata contradicts (P). Prove version traversal selects exactly the snapshot-visible logical versions, then predicate/projection evaluation produces (Q).

For index access, let (Cand(I,P)) be candidate locators from index (I). Prove completeness: every visible (t) with (P(t)=TRUE) has a reachable, maintained candidate or is covered by an explicit fallback. Prove locator/version resolution reaches the appropriate row state. Prove soundness: visibility and residual evaluation remove every false positive. For ordered delivery, additionally prove the emitted key sequence matches the required comparator/direction/null rules after visibility and residual removal; deletions preserve subsequence order, but arbitrary batching or parallel merging may not.

Index-only execution adds a projection/predicate coverage proof and a visibility proof. Cost comparison occurs only after these proofs. Estimated cost chooses among legal operators; empirical measurements calibrate estimates but do not replace semantic reasoning.

## Alternatives and Trade-Offs

Sequential row scan offers simple lifecycle, broad-bandwidth access, prefetch/vectorization, and natural range partitioning, but reads irrelevant data and supplies no general SQL order. Ordered index scan minimizes selective work and can satisfy order/limit, but pays navigation, scattered base fetches, and repeated-search cost. Index-only scan removes many base fetches when coverage/visibility permit but enlarges and maintains the index. Bitmap-plus-base scan batches locators and combines predicates, trading startup/memory and lost order for locality. Summarizing/zone-map scans cheaply prune correlated ranges but require conservative recheck. Columnar scans read projected columns and vectorize well, while point reconstruction and updates may differ. Remote pushdown reduces transfer only when semantics/capabilities and source snapshot are trustworthy.

No alternative dominates. Choose by result/property contract and a workload envelope including read mix, write amplification, storage, memory, freshness, concurrency, recovery, and operational complexity. Prefer schema/query/statistics corrections over global path disabling; planner toggles and hints are diagnostic or narrowly governed mitigations with expiry, not permanent substitutes for evidence.

## Failure Modes and Misconceptions

1. **“Sequential scan means missing index.”** Broad, tiny, cached, or poorly clustered reads can make it optimal; compare estimated/actual work and workload needs.
2. **“Index condition means the whole WHERE is proven.”** Navigation and residual conditions differ; inspect recheck/filter evidence.
3. **“Selectivity predicts random I/O.”** Equal selectivity can touch very different page counts because clustering, coverage, and cache differ.
4. **“Covering always means no table access.”** Visibility/version semantics may still require base visits.
5. **“Composite index uses every predicate equally.”** Leading equality and first range commonly delimit traversal; later conditions may only filter, with engine-specific skip behavior.
6. **“Equivalent-looking rewrite is sargable and safe.”** Types, overflow, nulls, collation, time zones, volatility, and expression definitions constrain rewrites.
7. **“Index scan implies output order.”** Only a proven compatible ordered path satisfies a complete `ORDER BY`; bitmap/parallel/base reconstruction can change sequence.
8. **“Estimated cost is milliseconds.”** It is a model-specific unit; compare alternatives within the bound configuration and measure separately.
9. **“One warm benchmark proves the index.”** Cache, parameters, churn, concurrency, tail latency, writes, and maintenance can reverse the result.
10. **“Forcing the desired node fixes performance.”** It may hide stale statistics, skew, bad schema, or non-sargable semantics and harm other parameter values.
11. **“An index entry is a current row.”** It is a maintained candidate subject to snapshot/version/locking rules.
12. **“More indexes only improve reads.”** Every index consumes storage/cache and adds write, log, vacuum/compaction, backup, and recovery work.

## Worked Examples

### Example 1

A table has 1,000 pages and a predicate qualifies 70% of rows scattered throughout the heap. A B+ tree can find keys, but base reconstruction approaches most pages in index order and adds tree/leaf work. Sequential traversal reads each eligible page once with prefetch. Conclusion: high scattered selectivity can make sequential scan cheaper despite a usable index.

### Example 2

The same table query selects one unique key and projects a non-indexed payload. The index descends a few pages and fetches one heap page; sequential access might inspect hundreds before finding it and cannot stop safely if duplicates are possible unless uniqueness is known. Conclusion: uniqueness and tiny candidate count strongly favor an index path.

### Example 3

An index on `(tenant_id, created_at, id)` receives `tenant_id=7 AND created_at>=T AND id=99`. Equality on tenant plus the created-at range bounds a contiguous interval. The `id` condition can reject entries inside that interval but generally cannot truncate every later created-at value. Conclusion: distinguish interval bounds from index-evaluable residuals.

### Example 4

Query `WHERE created_at::date = D` has an index on the timestamp column. Blindly replacing it with a day range is unsafe until the exact type, time zone, DST boundary, inclusivity, and cast semantics are established. A matching immutable expression index or correctly derived half-open range may work. Conclusion: sargability rewrites require semantic proof, not syntax preference.

### Example 5

A covering index contains `(account_id, occurred_at)` and includes `amount`, satisfying the query's values. On frequently updated PostgreSQL heap pages, visibility-map bits are often unset, so many heap visits remain. After churn subsides and maintenance establishes all-visible pages, heap fetches fall. Conclusion: value coverage and visibility sufficiency are separate conditions.

### Example 6

`ORDER BY occurred_at DESC, id DESC LIMIT 20` has a compatible index under the same collation/null rules. Backward navigation yields the first 20 qualifying rows and stops. A sequential plan must examine the eligible set and sort/top-N unless another ordering exists. Conclusion: required order plus small limit can dominate the scan choice even beyond filter selectivity.

### Example 7

Estimated matches are 100 but actual matches are 2,000,000, and an index path performs scattered heap fetches. Evidence shows stale statistics and a parameter value in a heavy-hitter bucket. Refreshing/raising appropriate statistics or handling parameter sensitivity restores a broad scan. Conclusion: diagnose estimate provenance and parameter distribution before forcing plans.

### Example 8

A lossy page summary says a page may contain values 10–90 for predicate `x=50`. The executor cannot return all page rows; it reads the page and rechecks each tuple. If the summary says range 60–90, it may exclude the page only if maintenance makes that negative conclusion conservative. Conclusion: lossy access permits false-positive pages, never unverified false negatives.

### Example 9

A nested loop runs an inner index scan 50,000 times. Explain reports two rows per loop and modest per-loop time, but total searches and heap visits dominate. Rewriting the join/access strategy or reducing outer rows matters more than micro-optimizing one probe. Conclusion: multiply scan metrics by loops and reason about the parent pipeline.

### Example 10

A team adds a wide covering index after a warm single-query test saves 8 ms. Production shows larger cache footprint, doubled ingest log bytes, slower compaction, and unchanged p99 under concurrency. A narrower index plus batching meets the read SLO with lower total cost. Conclusion: approve indexes using representative workload and write/recovery evidence, not isolated latency.

## Cross-Program Connections

- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies B+ trees, locality, hashing, probabilistic summaries, and layout analysis.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies cost models, adversarial inputs, experiments, and crossover analysis.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) explains caches, TLBs, prefetch, SIMD, branch prediction, memory bandwidth, and storage queues.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies virtual memory, file/page cache, asynchronous I/O, scheduling, cancellation, and resource isolation.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) extends scans to columnar files, row groups, partition pruning, predicate/projection pushdown, and remote object storage.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) adds shard pruning, replica/snapshot selection, partial failure, retries, and exchange cost.

## References

1. PostgreSQL Global Development Group, [Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html), PostgreSQL 18 current documentation, retrieved 2026-08-30; sequential, index, bitmap, index-only, order/limit, estimates, loops, and runtime evidence.
2. PostgreSQL Global Development Group, [Index-Only Scans and Covering Indexes](https://www.postgresql.org/docs/current/indexes-index-only-scans.html), PostgreSQL 18 current documentation, retrieved 2026-08-30; value coverage, included columns, visibility maps, and heap-fetch qualification.
3. PostgreSQL Global Development Group, [Multicolumn Indexes](https://www.postgresql.org/docs/current/indexes-multicolumn.html), PostgreSQL 18 current documentation, retrieved 2026-08-30; leading equality, first range, later conditions, and costed skip scanning.
4. PostgreSQL Global Development Group, [Indexes and ORDER BY](https://www.postgresql.org/docs/current/indexes-ordering.html), PostgreSQL 18 current documentation, retrieved 2026-08-30; ordered delivery, direction/null placement, broad scans, and limit interaction.
5. PostgreSQL Global Development Group, [Partial Indexes](https://www.postgresql.org/docs/current/indexes-partial.html), PostgreSQL 18 current documentation, retrieved 2026-08-30; predicate implication, parameter limitations, and partial-index design cautions.
6. PostgreSQL Global Development Group, [Query Planning Configuration](https://www.postgresql.org/docs/current/runtime-config-query.html), PostgreSQL 18 current documentation, retrieved 2026-08-30; planner method controls, page/CPU cost parameters, and cache assumptions.
7. PostgreSQL Global Development Group, [Statistics Used by the Planner](https://www.postgresql.org/docs/current/planner-stats.html), PostgreSQL 18 current documentation, retrieved 2026-08-30; sampled statistics, selectivity, correlation, and extended statistics.
8. SQLite Project, [Query Planning](https://www.sqlite.org/queryplanner.html), current official documentation, retrieved 2026-08-30; binary lookup, multi-column/covering indexes, statistics, and search-order integration.
9. Oracle, [Index Condition Pushdown Optimization](https://dev.mysql.com/doc/refman/8.4/en/index-condition-pushdown-optimization.html), MySQL 8.4 Reference Manual, retrieved 2026-08-30; separating index-tuple conditions from full-row reads.
10. DuckDB Foundation, [Indexing](https://duckdb.org/docs/current/guides/performance/indexing.html), current official documentation, retrieved 2026-08-30; zonemap pruning, layout sensitivity, ART eligibility/thresholds, and index maintenance trade-offs.

## Exercises

### Exercise 1

For a scan operator, distinguish logical predicate, search boundary, index-evaluable condition, residual base-row filter, lossy recheck, projection, and delivered order. Explain which parts determine correctness.

### Exercise 2

Derive usable intervals for index `(tenant_id, occurred_at, event_id)` under `tenant_id=4 AND occurred_at>=T1 AND occurred_at<T2 AND event_id>900`. Then analyze queries omitting `tenant_id` and queries adding a matching order/limit.

### Exercise 3

Implement or specify a differential scan test harness that compares sequential, index, and index-only candidates under bags, nulls, versions, residual predicates, forward/backward order, and cancellation. Define its oracle and failure evidence.

### Exercise 4

Diagnose a production change from sequential scan to index scan that lowered median latency but increased p99, storage reads, and serialization failures. Identify evidence and safe remedies.

### Exercise 5

Design access paths for a multi-tenant event service with point lookup, recent per-tenant pagination, broad retention analytics, heavy ingest, and object-storage history. Include correctness, cost, lifecycle, and release gates.

## Answers to the Exercises

### Answer 1

The logical predicate (P) defines which visible rows qualify. A search boundary restricts the traversed key interval and must be complete for every qualifying key. An index-evaluable condition rejects entries using stored key/payload values without necessarily narrowing traversal. A base-row residual checks conditions unavailable or not fully proven by the index. A lossy recheck repeats the original condition because coarse metadata identified only a page/range candidate. Projection constructs requested output after required values and visibility are established. Delivered order is a separate physical property including expression, direction, null placement, and collation. Correctness depends on complete candidate generation, current/snapshot-correct locator resolution, visibility, every necessary residual/recheck, correct bag multiplicity/projection, and any required order/locking contract; cost placement does not weaken these obligations.

### Answer 2

Equality on `tenant_id=4` fixes the first lexicographic dimension. The half-open occurred-at range defines one contiguous interval from `(4,T1,minimum)` through but excluding `(4,T2,minimum)` under the index comparator. `event_id>900` is generally checked within that interval; because occurred-at is already a range, event ID does not globally shorten the interval. Without tenant ID, conventional navigation may cover many tenant subranges or the whole index; an engine may cost repeated skip searches only when leading distinct tenants are few. For `ORDER BY occurred_at, event_id LIMIT n` within fixed tenant and compatible direction/null/collation, the index can deliver order and stop early. Mixed direction or a different leading order may need another index or sort. Confirm exact engine operator-class behavior rather than assuming a universal prefix rule.

### Answer 3

Build an independent logical oracle over explicit row versions: select the version visible at snapshot (S), retain predicate TRUE, project, compare bags, then sort only under the declared comparator. Generate empty inputs, duplicate keys/rows, null/UNKNOWN cases, boundary and collation values, unmatched partial-index predicates, updates/deletes, stale-looking candidates, and clustered/scattered layouts. Execute sequential and every applicable index direction/range/covering mode; compare bags, types, errors, and required order. Instrument candidate IDs, base fetches, rechecks, version decisions, resource acquisition/release, and cancellation points. Add fault tests for page split/reclamation protection and lossy metadata. A failure artifact contains seed, snapshot/version history, schema/index definition, plan/build/settings, candidate trace, expected/actual bag and order, and cleanup state. Finite passing cases are evidence, not a universal proof.

### Answer 4

Bind engine/build, SQL/parameters, snapshot/isolation, schema/indexes, statistics, plans, estimates/actual rows, loops/searches, index/heap fetches, correlation, cache reads/hits, device latency/queue, waits, locks/predicate coverage, concurrency, and result checks. The median may improve for selective/common parameters while heavy/skewed values scatter across most pages and inflate p99. The path can also change serializable predicate-tracking granularity and false-positive conflicts. Test parameter classes under cold/warm and concurrent load. Remedies include correct/extended statistics, parameter-sensitive planning, a better-ordered or narrower covering index, batching/bitmap/broad scan for heavy values, shorter transactions, or scoped concurrency control. A hint/path toggle is time-bounded. Gate unchanged result/isolation behavior, p95/p99, I/O, abort-and-retry completion, write amplification, and rollback safety.

### Answer 5

Use a unique durable identifier index for point lookup and a tenant-leading ordered index such as `(tenant_id, occurred_at DESC, event_id DESC)` for stable keyset pagination, including only measured narrow payload when visibility/storage benefits justify it. Keep the hot ingest relation partitioned or segmented by a durable time/tenant policy where pruning semantics are explicit; broad retention analytics should favor columnar sequential/vector scans with conservative row-group statistics rather than millions of random probes. Compact immutable history into versioned object-store files with manifest/snapshot binding, projection/predicate pushdown, checksums, and explicit missing-object failure. Price every hot index in log bytes, cache, compaction/vacuum, backup, recovery, and ingest tail latency. Verify bag/order/pagination under duplicate timestamps, nulls, late events, updates/deletes, concurrent ingest, tier movement, retry, and cancellation. Release gates cover correctness first, then representative point/pagination/analytic SLOs, ingest and recovery budgets, storage amplification, skew, stale statistics, and safe rollback/rebuild.
