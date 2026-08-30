---
module_id: DBE-035
program: Database Engineering
level: 1
module_number: 35
title: Composite and Covering Indexes
status: complete
last_verified: 2026-08-30
---

# Composite and Covering Indexes

## One-Page Review

### Governing question

How should one physical index order its search keys and optional payload so that a declared query workload gets selective bounds, useful output order, and fewer base-row visits without imposing unjustified write, space, and maintenance cost?

### Essential definitions

A **composite/multicolumn index** orders entries by a tuple of key parts. Its **leftmost prefix** is any initial sequence of those parts. An **equality prefix** fixes consecutive leading key parts; the next range part usually bounds a contiguous interval. A **residual index condition** filters entries visited inside a wider interval but does not necessarily reduce the interval. **Skip scan** is an optimizer/access technique that performs repeated probes over possible missing leading values when estimated profitable. A **covering index** contains every value needed by a query. A **key column** participates in navigation/order/uniqueness; an **included/payload column** is stored for return/recheck but does not guide navigation. An **index-only scan** returns data from index entries without fetching base rows only when the engine can also establish visibility/version validity.

### Central model, mechanism, or theorem

An index on `(k1,k2,...,km)` is sorted lexicographically under declared direction, NULL, collation, and tie-breaker semantics. Equality on `k1...kq`, followed by a bound on `k(q+1)`, usually forms one narrow interval. Constraints on later parts can reject candidates but do not generally make one contiguous interval when an earlier part is unconstrained. Output order follows the remaining physical key order after fixed prefixes. Coverage is a separate property: query-required values must be representable in the entry, and an engine-specific visibility mechanism must permit base-row avoidance.

### Critical invariants

- Key-part encoding/comparison exactly matches query equality, ordering, collation, direction, NULL, and type semantics.
- Navigation uses the complete lexicographic physical key, including implicit row-locator tie-breakers.
- Claimed scan bounds are derived from a contiguous interval or explicit set of intervals; residual filtering is not called selectivity.
- A claimed ordering matches forward/backward direction for every unfixed key part and survives plan operators.
- Uniqueness applies only to declared key columns; payload columns do not silently change it.
- Coverage includes predicates, projection, join, grouping/order, recheck, and expression/visibility needs—not merely `SELECT` columns.
- Index-only claims distinguish stored values from all-visible/version evidence and report actual base fetches.
- Updates maintain every changed key/payload value under transaction and recovery rules.
- Entry/page size, fan-out, height, splits, cache, WAL, replication, and build/rebuild cost are budgeted.
- Redundant prefix indexes are removed only after workload, constraint, capability, and rollback review.

### Common failures

Failures include “put the most selective column first” as a universal rule; treating separate single-column indexes as equivalent to one composite order; assuming every mentioned column narrows the scan; using a range before a later ordering requirement; forgetting mixed ASC/DESC and NULL placement; omitting a deterministic pagination tie-breaker; confusing payload with a search key; assuming coverage guarantees zero heap/base reads; including wide volatile values; changing uniqueness by appending payload as a key; ignoring implicit primary-key locators; retaining redundant indexes without write-cost evidence; and trusting one `EXPLAIN` estimate without actual candidate/base-fetch measurements.

### Compact example

For query `tenant=7 AND status='ready' AND created BETWEEN 100 AND 200 ORDER BY created,id`, key `(tenant,status,created,id)` makes one ordered interval and examines only ready entries in the time range. Key `(tenant,created,status,id)` also bounds tenant/time but scans every status in that interval before residual status filtering. Adding payload `total` can cover projection `(id,total)`, but in PostgreSQL heap avoidance additionally depends on the visibility map; on a churned heap, an index-only plan can still perform heap fetches.

### Connections

This module uses DBE-031–033's physical comparator, scan, and mutation model. DBE-036 adds partial/expression indexing; DBE-037–039 add specialized indexes, selectivity/statistics, and maintenance amplification. Query optimization later decides among these access paths.

## Governing Question

Column order is not a trivia rule. It is a workload contract among predicate shapes, ordering/grouping, projection, data distribution, write patterns, engine capabilities, and resource budgets. The design question is: which important query families map to narrow lexicographic intervals and useful output order, what must remain residual, which values merit duplication as payload, and what evidence justifies the ongoing cost?

Do not design from one SQL string alone. Bind parameter distributions, `LIMIT`, join role, snapshot/visibility, result width, update frequency, cache, tenant skew, and competing plans. A structurally usable index can still lose to a sequential, bitmap, hash, or different composite scan.

## Why This Matters

Composite indexes can replace repeated filtering/sorting and turn keyset pagination into a stable ordered seek. Covering can avoid expensive random base-row fetches. Conversely, every extra key/payload byte reduces fan-out, increases cache footprint and split/WAL cost, duplicates table data, and makes writes more expensive. An attractive read plan for one endpoint can tax every insert and update.

These indexes also enforce semantics. Composite unique constraints encode business keys; ordering and NULL behavior affect which tuples conflict. Included columns ordinarily must not participate in uniqueness. Confusing these roles can either reject valid data or permit invalid duplicates.

## Prerequisites and Retrieval

Retrieve SQL duplicate/NULL and constraint semantics from DBE-011–020. Retrieve B+ tree physical keys and pivots from [DBE-031](031-b-tree-structure.md), bounds/order/visibility from [DBE-032](032-b-tree-search-and-range-scan.md), and write amplification from [DBE-033](033-b-tree-insertion-splitting-and-deletion.md). Contrast equality-only [DBE-034](034-hash-indexes.md).

Before continuing, sort tuples `(tenant,status,created,id)` lexicographically and identify which predicates form one contiguous slice. Explain why `(a,b)` order supports grouping by `a` then `b`, but does not globally sort all `b` values independently of `a`.

## Learning Objectives

After completing this module, you should be able to:

1. derive composite scan intervals from lexicographic key order;
2. distinguish boundary constraints from residual index conditions and base rechecks;
3. design column order for equality, range, order, grouping, join, and pagination needs;
4. reason about missing leading columns and bounded skip-scan alternatives;
5. handle directions, NULLs, collations, expressions, duplicates, and row-locator tie-breakers;
6. distinguish key columns, included payload, coverage, and true index-only execution;
7. preserve intended uniqueness while adding payload;
8. estimate fan-out, height, cache, WAL, split, update, and rebuild consequences;
9. identify safe redundancy/consolidation opportunities; and
10. validate designs with actual plans, results, counters, and workload experiments.

## Core Exposition

Let key be `(k1,...,km)` with lexicographic comparison: compare `k1`; only if equal compare `k2`; continue until a difference, then use an implicit locator if necessary. Directions and NULL placement are part of each comparison. The tree contains one total order, not an independent lookup structure per column.

Suppose `(tenant,status,created,id)`. Equality `tenant=7,status='ready'` selects a contiguous prefix group. Bounds on `created` select a subinterval; `id` orders ties and enables an exclusive keyset continuation. Within that interval, a later predicate on `id` can filter, but an arbitrary `id` range does not necessarily shorten the created-time interval unless expressed as a lexicographic row bound the engine can use.

The baseline bound rule for a B-tree is leading equalities, then the first inequality/range. Later columns can still be checked inside the index, reduce base fetches, satisfy projection, or affect ordering. They should not be advertised as reducing pages/entries scanned without plan evidence. Current PostgreSQL documentation also describes skip scan/dynamic equality strategies, so “leftmost prefix” is a reasoning baseline, not a universal impossibility theorem.

With a missing leading key, qualifying later values are distributed among each leading-key group. Skip scan can enumerate a small estimated set of leading values and perform repeated probes. It is attractive when distinct leading values are few and later predicates selective; it degrades when enumeration/probes approach a broad scan. Capability and costing are engine/version/data dependent.

Column order balances several objectives. Equality columns before a range often create a narrow interval, but ordering among equality columns can affect compression, skew, alternate query prefixes, and skip scans. A query that always fixes both equality columns gets the same logical interval either way; choose based on other workload needs, not “most selective first.” A column needed alone by frequent queries may need to lead another index.

Ordering works after fixed prefixes. Index `(tenant,status,created DESC,id ASC)` with tenant/status fixed can emit `created DESC,id ASC`. A backward scan reverses both remaining directions together; it cannot make only one reverse. If `status` is not fixed, rows group by status before created and do not satisfy global created order. Bitmap combination usually loses index order.

Keyset pagination needs a total continuation key matching order, for example `(created,id) < (last_created,last_id)` in descending semantics. Using created alone repeats/skips tied rows. Offset pagination has different stability/cost. Concurrent inserts and snapshot behavior remain transaction concerns, not cured by the index.

Composite uniqueness applies to the declared key tuple under product NULL semantics. Appending `id` as a key can make every tuple unique and thereby destroy enforcement of unique `(tenant,email)`. In systems with `INCLUDE`, store output payload outside uniqueness/navigation. If no such feature exists, understand how trailing columns affect uniqueness and upper-level representation.

A covering index contains every value the physical plan needs: search and residual predicates, projection, join/group/order operations, and sometimes base-row identity or expression inputs. Coverage is query-specific. `SELECT *`, large JSON/blob values, or frequently changing payload usually makes poor coverage. Lossy prefix/expression representations may still require base recheck.

“Covering” and “index-only” are not synonyms in every engine. PostgreSQL indexes do not themselves contain MVCC visibility for heap tuples; an index-only scan checks a much smaller visibility map. If the heap page is not all-visible, it visits the heap. Thus stored payload makes index-only execution possible, while visibility state determines avoided heap fetches. Other engines with clustered/versioned layouts have different rules.

PostgreSQL `INCLUDE` columns are non-key payload: they do not affect search or uniqueness and are removed from upper B-tree levels. They still occupy leaf tuples, face tuple-size limits, and are maintained on relevant updates. Current PostgreSQL documentation recommends conservatism, especially for wide data and frequently changing tables where heap visits remain likely.

Secondary indexes may implicitly store a row locator or clustered primary key. This can make a projection appear covered and makes wide primary keys multiply across secondary indexes. The exact entry layout is engine-specific; verify it rather than adding duplicate columns blindly.

Index consolidation requires caution. `(a,b)` often serves queries on `a`, potentially making `(a)` redundant. But the shorter index may be shallower/smaller, support a different uniqueness/constraint/foreign-key role, have different included columns/collation/order, or materially improve a hot workload. Observe plans and write benefit, test invisibility/drop in a safe environment, retain rollback, then remove.

Write cost includes entry encoding, tree traversal, dirty leaf/internal pages, splits, WAL/redo, replication, vacuum/cleanup, cache displacement, backup, build/rebuild, and lock duration. Updating an included column can force index maintenance even when search keys are unchanged; engine optimizations such as PostgreSQL HOT may be prevented when indexed values change. Wider entries reduce leaf density and can raise height.

Statistics matter. Optimizers estimate prefix/range selectivity, correlation, distinct groups, NULLs, and combinations. Independent per-column estimates can badly miss correlated `(country,postal_code)` or `(tenant,status)` distributions; extended/multicolumn statistics may help if supported. DBE-038 treats this in depth. Index design and statistics are complementary.

The executable model compares two stable in-memory lexicographic layouts for one query. All rows are declared visible. The good order examines exactly two in-range ready entries and covers `(id,total)`; placing time before status examines four time-range entries then filters two. This is finite evidence, not an optimizer or I/O benchmark.

<!-- bijux-verify: {"id":"composite-covering-scan","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"key_order=('tenant', 'status', 'created', 'id')\nmatching_ids=(2, 3)\nentries_examined_good=2\nentries_examined_range_before_status=4\nheap_fetches_covering=0\nheap_fetches_noncovering=2\norder_satisfied=True\n","stderr":""}} -->
```python
rows = (
    {"tenant": 7, "status": "ready", "created": 90, "id": 1, "total": 10},
    {"tenant": 7, "status": "ready", "created": 110, "id": 2, "total": 20},
    {"tenant": 7, "status": "pending", "created": 120, "id": 5, "total": 50},
    {"tenant": 7, "status": "ready", "created": 150, "id": 3, "total": 30},
    {"tenant": 7, "status": "failed", "created": 160, "id": 6, "total": 60},
    {"tenant": 7, "status": "ready", "created": 210, "id": 4, "total": 40},
    {"tenant": 8, "status": "ready", "created": 130, "id": 7, "total": 70},
)
good_order = ("tenant", "status", "created", "id")
alternate_order = ("tenant", "created", "status", "id")


def ordered(key_parts: tuple[str, ...]) -> tuple[dict[str, object], ...]:
    return tuple(sorted(rows, key=lambda row: tuple(row[part] for part in key_parts)))


def good_candidates() -> tuple[dict[str, object], ...]:
    return tuple(
        row
        for row in ordered(good_order)
        if row["tenant"] == 7
        and row["status"] == "ready"
        and 100 <= row["created"] <= 200
    )


def alternate_candidates() -> tuple[dict[str, object], ...]:
    return tuple(
        row
        for row in ordered(alternate_order)
        if row["tenant"] == 7 and 100 <= row["created"] <= 200
    )


good = good_candidates()
alternate = alternate_candidates()
matches = tuple(row for row in alternate if row["status"] == "ready")
available = set(good_order) | {"total"}
required = {"tenant", "status", "created", "id", "total"}
all_visible = True
heap_fetches_covering = 0 if required <= available and all_visible else len(good)

print(f"key_order={good_order}")
print(f"matching_ids={tuple(row['id'] for row in matches)}")
print(f"entries_examined_good={len(good)}")
print(f"entries_examined_range_before_status={len(alternate)}")
print(f"heap_fetches_covering={heap_fetches_covering}")
print(f"heap_fetches_noncovering={len(good)}")
print(f"order_satisfied={tuple(row['id'] for row in good) == (2, 3)}")
```

## Definitions and Notation

Let physical key `K=(k1,...,km,t)` include explicit parts and tie-breaker `t`; compare lexicographically under per-part direction/NULL/collation. Let query-required values be `R`, values reconstructable from the index be `I`, and visibility evidence be `V`. Coverage means `R subset I`; base-row avoidance additionally requires an engine-specific predicate such as `V=true`.

Let scanned index entries be `s`, qualifying candidates `c`, returned rows `r`, base fetches `b`, entry width `w`, fan-out `F(w)`, height `h`, and maintained indexes `j`. A better design reduces end-to-end pages/CPU/latency subject to write/storage budgets; it does not merely maximize the number of predicate columns appearing in an index.

## Mechanisms, Invariants, or Proof Structure

A defensible design workflow is:

1. Group important queries by normalized predicate, join, order/group, projection, limit, and consistency shape.
2. Bind equality/NULL/collation/direction semantics and parameter/data distributions.
3. Derive candidate lexicographic intervals; mark boundary, residual-index, base-recheck, and visibility conditions separately.
4. Verify output order and deterministic tie-breaker after fixed prefixes and plan transformations.
5. Add only payload needed for high-value coverage; preserve uniqueness key boundaries.
6. Estimate encoded width, fan-out/height, tuple limits, writes, WAL, cache, maintenance, and build/rebuild resources.
7. Compare composite, single/combined, partial/expression, specialized, sequential, and no-new-index alternatives.
8. Test actual plans/results across representative parameters, skew, cache, visibility, concurrency, and writes.
9. Canary/invisibly evaluate where supported; observe regressions and keep rollback.
10. Periodically audit usage, redundancy, bloat, validity, statistics, and changed workload assumptions.

Lexicographic interval correctness follows because all tuples sharing a fixed prefix are contiguous; within that group, the next key part is ordered, so its range is contiguous. A constraint on a later part with an unconstrained earlier part appears in multiple earlier-part groups and is not generally one interval. This is a structural proof for the order, not a proof that an optimizer will choose or that the plan will be fastest.

## Alternatives and Trade-Offs

One composite index provides joint order and can satisfy search plus sorting; separate indexes offer independent prefixes and may be bitmap/intersected, but combination often loses order and adds merge work. A wider “one index for everything” reduces apparent count while bloating every access. Several narrower indexes increase write paths but can better match distinct query families.

Key payload supports navigation/order but affects uniqueness and upper levels. Included payload preserves key semantics and often upper-level fan-out, yet widens leaves and updates. Base fetch avoids duplication but may be random/visibility-heavy. Materialized/denormalized projections, caches, and column stores solve different workloads with larger consistency/operational costs.

## Failure Modes and Misconceptions

- “Most selective first” ignores equality combinations, ordering, other query prefixes, compression, and workload.
- “A range stops all later usefulness” is too broad; later parts can filter/cover/order within constraints, though not necessarily narrow bounds.
- “Leftmost prefix is absolute” ignores current skip-scan and optimizer-specific repeated probes.
- “Two single indexes equal `(a,b)`” ignores joint order, interval shape, bitmap cost, and ordering loss.
- “All WHERE columns are search keys” confuses boundary, residual, and recheck.
- “Covering means `SELECT` columns only” omits predicates, joins, order/group, expressions, and visibility.
- “INCLUDE makes uniqueness include payload.” In PostgreSQL it does not.
- “Index-only means zero heap reads.” Visibility/version evidence decides actual fetches.
- “Wider is always faster for reads.” Fan-out, cache, I/O, tuple limits, and scans can worsen.
- “A prefix index is redundant.” Constraint, size, order, capability, and hot-plan evidence may preserve it.
- “One plan proves design.” Parameters, skew, statistics, cache, visibility, and concurrency change choices.
- “No sort node proves correct order.” Verify full key directions, NULLs, collation, and plan preservation.

## Worked Examples

### Example 1

Index `(tenant,status,created,id)` and predicates fixing tenant/status plus created range form one interval. Swapping status after created scans all statuses inside the time interval. Conclusion: both indexes are usable, but examined-entry counts differ.

### Example 2

Queries always fix `(tenant,email)`. Choosing email first because it is globally selective sacrifices tenant-only administration queries; within full equality, either order locates the same logical row. Conclusion: order is workload-wide, not a selectivity slogan.

### Example 3

Index `(region,device_id)` receives only `device_id=42`. Qualifiers exist in every region group. A skip scan may probe a small region set; with thousands of regions it may lose. Conclusion: missing-leading support is costed repeated search, not free direct lookup.

### Example 4

Index `(tenant,created DESC,id ASC)` with tenant fixed satisfies that order. Backward gives created ASC,id DESC, not created ASC,id ASC. Conclusion: scan reversal flips all unfixed directions.

### Example 5

Pagination ordered by created alone sees ten ties. Continuing after only created can skip/repeat them; `(created,id)` supplies a total exclusive continuation. Conclusion: deterministic order needs a tie-breaker.

### Example 6

Unique key should enforce `(tenant,email)`. Defining unique `(tenant,email,last_seen)` permits two rows with same tenant/email when timestamps differ. `INCLUDE(last_seen)` preserves intended uniqueness where supported. Conclusion: key and payload roles are semantic.

### Example 7

An index stores `(tenant,status,created,id)` plus total, covering a query's values. On an all-visible PostgreSQL heap page it avoids heap access; after churn clears the bit it fetches heap tuples for visibility. Conclusion: coverage enables but does not guarantee base avoidance.

### Example 8

Including a 20 KiB document exceeds an index tuple limit or destroys density. Keeping a small summary/version in the index and fetching rare documents is cheaper. Conclusion: payload width is a hard and economic constraint.

### Example 9

Indexes `(a)` and `(a,b)` coexist. The shorter one is unused after workload replay and has no constraint role; hiding/dropping it reduces write/WAL cost. If it is a hot compact path, retain it. Conclusion: redundancy is evidence-based.

### Example 10

Planner estimates tenant/status independence, but one tenant owns nearly all ready rows. Actual scan returns 100 times the estimate. Extended statistics or a different/partial design may help. Conclusion: index order cannot repair missing joint-distribution knowledge alone.

## Cross-Program Connections

- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies lexicographic order and multidimensional-key reasoning.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies interval proofs and output-sensitive cost models.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) supplies workload shapes, clustering, and analytical access trade-offs.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) supplies keyset pagination and endpoint query contracts.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies observability, workload replay, canaries, and capacity budgets.

## References

1. PostgreSQL Global Development Group, [Multicolumn Indexes](https://www.postgresql.org/docs/current/indexes-multicolumn.html), current leading constraints and skip-scan guidance.
2. PostgreSQL Global Development Group, [Index-Only Scans and Covering Indexes](https://www.postgresql.org/docs/current/indexes-index-only-scans.html), current visibility-map and `INCLUDE` semantics.
3. PostgreSQL Global Development Group, [Indexes and ORDER BY](https://www.postgresql.org/docs/current/indexes-ordering.html), current direction, NULL placement, and multicolumn ordering.
4. PostgreSQL Global Development Group, [Index Scanning](https://www.postgresql.org/docs/current/index-scanning.html), access-method, visibility, bitmap, and index-only boundaries.
5. SQLite Project, [Query Planning](https://www.sqlite.org/queryplanner.html), official multicolumn, covering, search, and sort examples.
6. Oracle, [MySQL 8.4 Multiple-Column Indexes](https://dev.mysql.com/doc/refman/8.4/en/multiple-column-indexes.html), current leftmost-prefix and index-merge guidance.
7. Oracle, [How MySQL Uses Indexes](https://dev.mysql.com/doc/refman/8.4/en/mysql-indexes.html), current covering, ordering, and selectivity guidance.
8. Goetz Graefe, [Modern B-Tree Techniques](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/p669-graefe.pdf), composite keys, included columns, compression, and physical design context.
9. Surajit Chaudhuri and Vivek Narasayya, [An Efficient, Cost-Driven Index Selection Tool for Microsoft SQL Server](https://www.microsoft.com/en-us/research/wp-content/uploads/1997/05/vldb97.pdf), *VLDB*, 1997.
10. Ramakrishnan and Gehrke, *Database Management Systems*, 3rd ed., McGraw-Hill, 2003, composite-index and access-path foundations.

## Exercises

### Exercise 1

For index `(tenant ASC,status ASC,created DESC,id ASC)`, derive intervals/residuals/order for five query shapes: full equality prefix plus time range; tenant plus time; status alone; tenant/status plus exclusive pagination; and tenant with global created ASC,id ASC output.

### Exercise 2

Compare `(tenant,status,created,id)` with `(tenant,created,status,id)` on the executable rows. Enumerate ordered entries examined and explain what changes under status skew and a small `LIMIT`.

### Exercise 3

Design a unique `(tenant,email)` index covering `display_name,last_seen`. State key/payload, equality/collation/NULL rules, visibility requirements, update effects, tuple-width limits, and why adding payload to the unique key is wrong.

### Exercise 4

Given indexes `(a)`, `(a,b) INCLUDE(c)`, `(b,a)`, and workload/plans, devise a safe consolidation experiment including constraints, statistics, plan capture, invisible/canary behavior, write measurements, rollback, and decision thresholds.

### Exercise 5

Design a production experiment for a feed query with tenant, status, descending time, keyset pagination, projection, heavy churn, and skew. Compare composite/covering alternatives and state correctness/performance evidence.

## Answers to the Exercises

### Answer 1

Full tenant/status equality plus created range is one interval; id orders ties. Tenant plus created range spans status groups, so created is not one contiguous next-part bound and may require broader scan/skip strategy with created residual. Status alone misses tenant prefix and similarly needs repeated/broad/other access. Exclusive pagination after complete `(created,id)` becomes a lexicographic bound inside fixed tenant/status. With only tenant fixed, forward order groups by status then created DESC/id ASC; backward reverses status and both later directions, so neither yields global created ASC,id ASC unless status is fixed or a sort/different index is used.

### Answer 2

The good order visits ready rows at created 110 and 150: two interval entries, IDs 2,3. The alternate tenant/time interval visits created 110 ready, 120 pending, 150 ready, 160 failed: four entries, then status filters to 2,3. More non-ready rows increase residual work; if ready dominates, the difference shrinks. A small `LIMIT` can stop the good ordered interval after enough qualifying rows, while the alternate may inspect many residual failures and its ordering includes status between time and id. Actual planner/page/cache effects still require measurement.

### Answer 3

Use key `(tenant,normalized_email)` and payload `display_name,last_seen` through non-key inclusion where supported. Declare case/collation and NULL uniqueness semantics exactly; do not assume ordinary SQL equality. Coverage includes all query needs, but PostgreSQL-like heap avoidance requires all-visible evidence and should record heap fetches. Updates to display/last-seen maintain wider leaf entries, may increase WAL/splits and inhibit engine update optimizations; enforce tuple-size limits and exclude overly wide values. Making payload key parts changes uniqueness to the four-column tuple and permits duplicate tenant/email pairs when payload differs.

### Answer 4

Inventory uniqueness, foreign-key/constraint, order/collation/direction, payload, validity, and engine capability before calling anything redundant. Capture parameterized actual plans and usage over a representative window; refresh relevant statistics. Hide an index where supported or canary schema replicas, replay reads/writes, and compare results plus p50/p99, pages, sorts, base fetches, cache, WAL, locks, space, and maintenance. `(a,b) INCLUDE(c)` may cover `(a)` queries but be larger; `(b,a)` serves a different prefix. Remove `(a)` only if no semantic role and measured read regression stays below threshold while write/storage benefit meets threshold. Retain a rapid recreate/rollback plan and monitor after rollout.

### Answer 5

Define exact snapshot, tenant/status predicates, `(created DESC,id ASC)` total order, exclusive continuation, projection, visibility, and result oracle. Compare keys such as `(tenant,status,created DESC,id)` and `(tenant,created DESC,id,status)` with narrow payload variants and a noncovering baseline. Vary tenant/status skew, page depth, limit, cache, all-visible fraction/churn, update rate, concurrency, and history width. Verify no duplicate/skip across ties and compare actual bounds/residuals, entries/pages, returned rows, heap fetches, sort, cache/I/O, WAL, splits, size, write throughput, and p50/p99. Choose only if benefits hold across declared distributions and write budgets; canary with rollback and re-evaluate as visibility/statistics/workload drift.
