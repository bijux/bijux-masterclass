---
module_id: DBE-032
program: Database Engineering
level: 1
module_number: 32
title: B+ Tree Search and Range Scan
status: complete
last_verified: 2026-08-30
---

# B+ Tree Search and Range Scan

## One-Page Review

### Governing question

How does a B+ tree position an equality or range query at the correct leaf and enumerate exactly the qualifying ordered entries despite duplicates, composite keys, visibility, caching, and concurrent structural change?

### Essential definitions

**Descent** chooses one child per internal level from separators and the complete index comparator. **Lower bound** is the first entry not less than a search key; **upper bound** is the first entry greater than it. A **point probe** positions by the complete physical key or scans an equal logical-key run. A **range scan** positions once at its lower endpoint, then walks leaf entries/siblings until the upper endpoint fails. A **scan key** encodes comparison attributes, inclusivity, omitted suffix semantics, collation, directions, and NULL rules. A **residual predicate/recheck** tests conditions not fully proven by the index entry. A **covering/index-only scan** can return required columns from the index only when visibility and representation rules permit. A **B-link correction** follows a right sibling when a high key shows that a stale parent descent landed left of the target range.

### Central model, mechanism, or theorem

Under DBE-031's right-child-minimum convention, internal descent selects child index equal to the number of separators `<= target`. At the leaf, binary lower-bound finds the first key `>= lower` for an inclusive start or upper-bound finds first `> lower` for an exclusive start. A half-open scan `[low,high)` emits entries while `key<high`, advances through validated ordered leaf links, and stops at the first `key>=high`. For height `h`, point positioning costs `O(h)` page visits plus within-page comparisons; returning `k` adjacent entries adds approximately the leaf pages covering them. Correctness additionally requires comparator consistency, structural validity, snapshot/visibility, and concurrency protocol.

### Critical invariants

- Every internal child choice matches the exact separator convention and full physical comparator.
- Binary search maintains explicit low/high invariants and terminates at the declared lower/upper bound.
- The start position is the earliest qualifying physical entry, including duplicate tie-breakers and endpoint inclusivity.
- Leaf traversal follows validated monotone links without skip, loop, stale incarnation, or unbounded corrupt chain.
- The stop predicate is evaluated before emission and is correct for forward/backward direction and composite bounds.
- Index qualification is distinguished from base-row visibility, lossy/prefix/expression recheck, and concurrent version state.
- Locks/latches/pins protect only documented intervals; high-key/right-link validation or restart closes split races.
- Ordering claims match index column directions, NULL placement, collation/operator class, scan direction, and planner contract.

### Common failures

Failures include using lower-bound when an exclusive endpoint needs upper-bound; routing equality to the wrong separator side; stopping at a leaf boundary; returning only one duplicate; comparing a composite prefix as a complete key; applying SQL three-valued NULL logic as raw comparator logic; claiming prefix-index equality without recheck; assuming an index locator is a visible row; calling an index-only scan heap-free without visibility evidence; losing order through bitmap combination; following a stale sibling after page reuse; holding a root-to-leaf latch chain unnecessarily; ignoring high keys during concurrent splits; and equating logarithmic comparison count with storage latency.

### Compact example

With root separators `(15,30)` and leaves `L0=(5,10)`, `L1=(15,20,25)`, `L2=(30,40)`, point 25 counts one separator `<=25`, descends to L1, and finds value `e`; point 26 descends to L1 but lower-bound lands after 25, so it is absent. Range `[10,31)` begins at L0 key 10, follows L1 and L2, emits `(10,15,20,25,30)`, and stops before 40. If a stale parent sends key 35 to L1 whose high key is 30, the search follows L1's right link to L2 before positioning.

### Connections

This module depends on [DBE-031](031-b-tree-structure.md)'s exact separator, comparator, leaf, and right-link invariants and DBE-021–030's page/buffer/integrity context. DBE-033 supplies mutations that create concurrent split states; DBE-035 covers composite/covering index design; later query-processing modules choose among scans and enforce visibility/predicates.

## Governing Question

The governing question is not merely whether binary search appears in the code. It asks what ordered domain is searched, which boundary is desired, what tree snapshot/concurrent protocol is observed, what an index entry proves, and when a returned base row satisfies SQL semantics. One off-by-one comparison or omitted suffix can silently miss/duplicate rows.

A production scan contract declares key encoding/comparator, separator convention, duplicate tie-breaker, endpoint normalization, direction, leaf-link/high-key semantics, latching/restart policy, visibility responsibility, residual predicates, output ordering, cancellation, and resource bounds.

## Why This Matters

B+ trees matter because one root-to-leaf positioning phase can feed many adjacent results. Equality lookup and selective ranges exploit small height; ordered scans can also satisfy `ORDER BY`, `MIN/MAX`, prefix groups, merge joins, and pagination. Covering leaves may avoid base-row I/O. But broad ranges can become more expensive than sequential/bitmap plans.

Index order is physical and complete. SQL predicates may be partial, three-valued, collation-sensitive, type-coerced, or expression-based. A multicolumn tree sorts lexicographically: constraints on leading columns usually define contiguous intervals; conditions only on later columns may not. Modern optimizers can use skip-scan-like strategies in bounded cases, but “leftmost prefix” remains a reasoning baseline, not an absolute product claim.

Concurrency adds correctness work. Searches cannot assume a parent observed after a split already points to every child. Right links/high keys or version-validation/restart protocols ensure a search that descends stale does not miss moved-right keys. Memory/buffer reclamation must prevent a page ID from becoming another object while referenced.

## Prerequisites and Retrieval

Retrieve exact order-4 structure, right-child-minimum separators, full physical comparator, duplicates, occupancy, links/high keys, and stable/concurrent states from [DBE-031](031-b-tree-structure.md). Retrieve buffer pins/latches/generations from [DBE-026](026-buffer-pools.md), integrity from [DBE-029](029-checksums-and-page-corruption.md), and row/visibility context from earlier modules.

Before continuing, implement lower-bound and upper-bound on a sorted array using half-open search interval `[lo,hi)` and state the loop invariant. Explain why point lookup of a non-unique logical key is a range over physical `(logical_key,tie_breaker)` entries, and why an index hit may still reference an invisible/dead/version-mismatched row.

## Learning Objectives

After completing this module, you should be able to:

1. derive internal child selection from a declared separator convention;
2. implement/prove leaf lower-bound and upper-bound positioning without off-by-one errors;
3. normalize inclusive/exclusive, unbounded, forward, and backward ranges;
4. scan siblings and stop exactly while defending against corrupt/stale links;
5. reason about duplicates, composite prefixes, NULLs, collations, descending keys, expressions, and prefix indexes;
6. separate index qualification, residual recheck, base lookup, visibility, and covering evidence;
7. explain high-key/right-link correction and restart under concurrent splits/deletions;
8. model comparison, page-I/O, cache, prefetch, output, and random base-fetch costs; and
9. design correctness, performance, fault, and observability tests.

## Core Exposition

Normalize the predicate into physical key intervals. Equality on complete key is `[k,k_successor)` conceptually, but discrete successor may not exist; implementations carry inclusive/exclusive flags or sentinel suffixes. `a<=x<b` maps directly to `[a,b)`. `a<x<=b` needs upper-bound at `a` and inclusive stop after `b`. Unbounded endpoints use minus/plus-infinity sentinels defined by the comparator.

Internal descent under the chapter convention chooses the first separator strictly greater than target; if none, choose rightmost child. Equivalently count separators `<=target`. This is an upper-bound operation on pivots. A different parent convention changes the comparison. Truncated pivots and omitted scan-key suffixes require engine comparison rules, not padding guessed by an application.

Within a leaf, binary lower-bound uses `[lo,hi)` with invariant: entries before `lo` are `<target`; entries at/after `hi` are `>=target`. Choose `mid=lo+floor((hi-lo)/2)`; if entry `<target`, set `lo=mid+1`, else `hi=mid`. Termination at `lo=hi` returns first `>=target`. Upper-bound changes the left invariant to `<=target` and advances when `entry<=target`.

A point lookup then checks equality at the returned position. For unique complete physical key it returns zero/one entry. For non-unique logical keys, physical entries include tie-breakers; find the lower sentinel `(logical,-infinity)` and scan until logical key changes, applying visibility/recheck. Posting/deduplicated lists require a nested ordered search/iteration.

A forward range positions once. It visits entries from the start slot, evaluates the upper stop before emitting, skips index entries that fail index-local conditions, returns/rechecks candidates as required, and follows the right leaf link when the page ends. It releases/reacquires pins/latches under the engine protocol and validates next-page identity/range. It stops as soon as monotonic ordering proves no future entry can qualify.

Backward scanning is not “reverse the output afterward.” Position at the last allowed entry using upper/lower bound appropriate to the upper endpoint, iterate entries leftward, follow validated left links (or engine alternative), and stop below the lower endpoint. Mixed ASC/DESC columns and NULL placement determine whether forward/backward scan produces the requested SQL order.

Composite keys are lexicographic. Index `(tenant,status,created_at,id)` makes `tenant=T,status=S,created_at in [a,b)` one contiguous interval using sentinel suffixes. With only `status=S`, qualifying entries are spread across tenant groups. With `tenant=T,created_at>=a` but no status restriction, the scan may cover all statuses within tenant and recheck time, or use skip-scan/product-specific strategies. Exact planner capability must be verified.

NULL is an ordered index datum according to index definition, while SQL `NULL = NULL` is unknown. The access method uses sortable NULL flags for navigation, and predicate semantics decide which NULL entries qualify. Collation/operator class and type coercion must match index semantics; an incompatible collation change can make navigation wrong even with valid checksums.

Expression, partial, and prefix indexes have implication/recheck boundaries. A prefix string index can locate a candidate range but may conflate longer values and require full-column recheck. A partial index contains only rows satisfying its predicate when maintained correctly; the planner must prove query implication. Expression values must be computed consistently. These designs are expanded in DBE-036.

An index entry may store a heap locator, clustered primary key, or complete row/payload. A heap/clustered lookup can be random and may find an invisible version; MVCC visibility and residual predicates are usually outside the basic tree navigation. PostgreSQL access-method documentation separates returning index entries from fetching parent-table tuples and visibility. Index-only operation still needs engine-specific visibility evidence; stale included values/version rules matter.

Output order follows the complete index comparator and scan direction only while the plan preserves it. A forward scan of a suitable B-tree can satisfy matching `ORDER BY`; backward reverses every key direction/NULL ordering together. Bitmap combination typically discards index order. Parallel scans/merges, deduplication, rechecks, and base fetches need an explicit order contract.

Under a B-link split, a parent can route to an old left page. After latching/validating it, compare target with page high key. If target belongs to the right, follow the right link and repeat because multiple splits may have occurred. A dead/ignored page also moves according to protocol. Optimistic/versioned trees instead validate node versions and restart. Neither permits following unvalidated arbitrary links.

Range scans face concurrent inserts/deletes and snapshot semantics. Whether a scan sees a newly inserted key depends on isolation, latch protocol, cursor state, predicate locking/serialization, and implementation. Avoid duplicates/skips by maintaining a stable resume key/physical tie-breaker and engine cursor protocol, not by retaining a raw slot across page compaction/split. Pagination by `OFFSET` is different from keyset continuation.

Cost decomposes into internal/leaf positioning comparisons, page misses/hits, sibling leaf pages, result processing, base-row random fetches, visibility/rechecks, locks/latches, prefetch, and output. Approximate `O(h+ceil(k/entries_per_leaf))` page visits assumes contiguous qualifying entries and ignores base fetch/cache. A broad unclustered secondary range can perform many random heap/clustered lookups; a sequential or bitmap plan may win.

Cache and prefetch change observed latency. Upper levels are frequently hot; leaves may be cold. Sibling scans offer sequential/logical prefetch but physical pages may not be adjacent. Read-ahead too far wastes I/O on cancellation/limit/selectivity errors. Limit pushdown can stop early only if order/predicate semantics ensure correctness.

Testing includes every endpoint combination, empty tree/range, exact separator equality, before-first/after-last, one-page and multi-level, leaf-boundary starts/stops, all duplicates, NULL/composite/direction/collation cases, corrupt/looping links, stale page generations, split/delete schedules, snapshot changes, visibility/recheck, covering fallback, cancellation, limits, and differential comparison to a sorted reference model.

Observability records index/plan, normalized bounds, direction, root/internal/leaf pages, comparisons, right-link corrections/restarts, leaf pages/entries visited, candidates/rechecks/visible rows, base fetches, buffer hits/misses/prefetch, lock/latch wait, returned rows, ordering/sort, cancellation, and p50/p99. Values must be redacted/sampled.

The executable model uses DBE-031's tiny stable tree. It demonstrates point presence/absence, half-open range traversal, an empty range, and high-key right correction from a deliberately stale parent landing. It omits duplicates, composite keys, visibility, concurrency interleavings, pages, and I/O.

<!-- bijux-verify: {"id":"bplus-search-range","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"point_25=(path=('R', 'L1'),value='e')\npoint_26=(path=('R', 'L1'),value=None)\nrange_10_31=(keys=(10, 15, 20, 25, 30),leaves=('L0', 'L1', 'L2'))\nrange_empty=()\nlower_inclusive_upper_exclusive=True\nstale_parent_35=(path=('L1', 'L2'),leaf='L2')\nleaf_links_valid=True\n","stderr":""}} -->
```python
nodes = {
    "L0": {"entries": ((5, "a"), (10, "b")), "high": 15, "next": "L1"},
    "L1": {"entries": ((15, "c"), (20, "d"), (25, "e")), "high": 30, "next": "L2"},
    "L2": {"entries": ((30, "f"), (40, "g")), "high": None, "next": None},
}
root_keys = (15, 30)
root_children = ("L0", "L1", "L2")


def child_for(key: int) -> str:
    position = 0
    while position < len(root_keys) and root_keys[position] <= key:
        position += 1
    return root_children[position]


def lower_bound(entries: tuple[tuple[int, str], ...], key: int) -> int:
    low = 0
    high = len(entries)
    while low < high:
        middle = low + (high - low) // 2
        if entries[middle][0] < key:
            low = middle + 1
        else:
            high = middle
    return low


def point(key: int) -> tuple[tuple[str, str], str | None]:
    leaf = child_for(key)
    entries = nodes[leaf]["entries"]
    position = lower_bound(entries, key)
    value = entries[position][1] if position < len(entries) and entries[position][0] == key else None
    return ("R", leaf), value


def range_scan(low_key: int, high_key: int) -> tuple[tuple[int, ...], tuple[str, ...]]:
    leaf = child_for(low_key)
    position = lower_bound(nodes[leaf]["entries"], low_key)
    keys = []
    leaves = []
    while leaf is not None:
        leaves.append(leaf)
        entries = nodes[leaf]["entries"]
        while position < len(entries):
            key = entries[position][0]
            if key >= high_key:
                return tuple(keys), tuple(leaves)
            keys.append(key)
            position += 1
        leaf = nodes[leaf]["next"]
        position = 0
    return tuple(keys), tuple(leaves)


def move_right(start: str, key: int) -> tuple[tuple[str, ...], str]:
    path = []
    leaf = start
    while True:
        path.append(leaf)
        high_key = nodes[leaf]["high"]
        if high_key is None or key < high_key:
            return tuple(path), leaf
        leaf = nodes[leaf]["next"]


point_25 = point(25)
point_26 = point(26)
range_10_31 = range_scan(10, 31)
range_empty = range_scan(26, 30)[0]
stale_path, corrected_leaf = move_right("L1", 35)
leaf_links_valid = tuple(nodes[name]["next"] for name in root_children) == ("L1", "L2", None)

print(f"point_25=(path={point_25[0]},value={point_25[1]!r})")
print(f"point_26=(path={point_26[0]},value={point_26[1]!r})")
print(f"range_10_31=(keys={range_10_31[0]},leaves={range_10_31[1]})")
print(f"range_empty={range_empty}")
print("lower_inclusive_upper_exclusive=True")
print(f"stale_parent_35=(path={stale_path},leaf={corrected_leaf!r})")
print(f"leaf_links_valid={leaf_links_valid}")
```

The range `[26,30)` is empty but touches L1 and then observes boundary 30 in L2; output reports only result keys. Production instrumentation should separately report visited pages, as the main range output does.

## Definitions and Notation

Let complete physical key comparator be `<_I`. `lower_bound(A,x)=min{i | not(A_i <_I x)}` and `upper_bound(A,x)=min{i | x <_I A_i}`, with result `|A|` if absent. A normalized range has lower `(l,inclusive_l)` and upper `(u,inclusive_u)` plus infinities.

For right-min separators `K_1...K_r`, child index is `upper_bound(K,target)`, i.e. number of separators `<=target`. Height is `h`; returned qualifying entries are `k`; visited leaves `q`; base-row fetches `b`; right corrections/restarts `r_c`. Complexity notation hides page/caching and should be accompanied by these counts.

## Mechanisms, Invariants, or Proof Structure

A defensible scan workflow is:

1. Bind snapshot, index incarnation/root, comparator/collation, scan direction, normalized physical bounds, and residual predicate.
2. Validate each internal page and choose child under the exact separator comparison; retain only required pin/latch/version evidence.
3. After descent, compare high key/version and move right or restart until target belongs to the page.
4. Binary-search the first/last qualifying leaf entry using a stated loop invariant.
5. Before each emission, validate key against stop bound and index-local predicates.
6. Follow duplicate/posting entries in complete physical order; never collapse logical equality prematurely.
7. Traverse validated sibling pages while preserving resume key and concurrency/snapshot rules.
8. Fetch/recheck base versions or establish covering/visibility evidence; apply SQL semantics.
9. Preserve promised output order or explicitly sort/merge; stop safely on limit/cancellation/error.
10. Account pages, candidates, rechecks, visible rows, I/O, corrections, and residual limitations.

Lower-bound correctness follows from the loop invariant. Initially both partitions are empty. Each comparison places `mid` and one side into the proven `<target` or `>=target` partition while shrinking `[low,high)`. At termination the first partition ends at `low` and second begins there, so it is the first not-less element. Range correctness follows by start minimality, monotonically complete leaf traversal, emission iff within bounds, and stopping once all later keys exceed the upper bound.

## Alternatives and Trade-Offs

Linear scan within a tiny/compressed page can beat binary search through cache/branch effects; binary/interpolation/SIMD/prefix-aware search trades CPU and metadata. Optimistic/versioned descent lowers latch cost but restarts; latch coupling simplifies validation but can constrain concurrency. B-link right correction avoids root restart for right splits at metadata cost.

Plain index scan preserves order but random base fetches can dominate. Covering scan enlarges/maintains index but avoids fetches when visibility permits. Bitmap scans combine predicates and batch physical visits but lose index order. Sequential scan wins broad ranges. Prefetch helps long scans but wastes bandwidth under small limits/cancellation.

## Failure Modes and Misconceptions

- “Binary search means equality.” Positioning requires lower/upper-bound semantics.
- “Separator equality goes left.” It depends on the declared parent convention.
- “A range is two point lookups.” Position once, then traverse ordered leaves until stop.
- “Duplicates are one entry.” Physical tie-breakers/posting lists form an equal-key interval.
- “The later composite column is searchable alone.” It may not define one contiguous interval.
- “NULL comparison follows SQL equality.” Navigation has a total NULL order; qualification uses SQL semantics.
- “Index hit is a returned row.” Visibility and residual predicates may reject it.
- “Covering means no heap/base access always.” Visibility/version/engine rules decide.
- “Index scan always satisfies ORDER BY.” Directions, NULLs, collation, prefixes, bitmap/parallel transformations matter.
- “Page links remain valid after unlatch.” Generation/reclamation protocols are required.
- “Concurrent split requires locking the whole path.” B-link/versioned designs can correct or restart.
- “O(log N+k) predicts p99.” Cache misses, base fetches, contention, storage, recheck, and output dominate.
- “More prefetch is faster.” Limits, selectivity errors, and shared I/O create waste.
- “A clean result proves no skipped page.” Differential/structural/concurrency evidence is still needed.

## Worked Examples

### Example 1

At separator 15 under right-min convention, target 15 goes to the right child because one separator is `<=15`. Sending equality left misses the leaf entry.

### Example 2

Leaf `(10,10,10,12)` with physical tie-breakers needs lower-bound `(10,-infinity)` and iteration through the whole logical-equal interval. One binary hit is insufficient.

### Example 3

For `(tenant,status,time,id)`, `tenant=7,status='ready',time>=t` is contiguous. `status='ready'` alone spans tenant groups and may require another plan or bounded skip scans.

### Example 4

Range `(10,30]` positions with upper-bound 10, emits 15,20,25,30, and stops after 30. Reusing `[10,30)` comparisons would wrongly include 10 and exclude 30.

### Example 5

A prefix index stores first ten characters of a URL. Two full URLs share the prefix; the index returns both candidates and the full predicate rechecks them. Prefix equality is lossy.

### Example 6

An index entry points to a heap version deleted before the reader's snapshot rules allow it. Tree navigation is correct but visibility rejects it. Candidate and returned-row counts differ.

### Example 7

A stale parent lands on page high-key 50 for target 75. The reader validates/follows right twice after consecutive splits. A bounded correction/restart rule prevents corrupt cycles from looping forever.

### Example 8

Forward scan of `(x ASC,y DESC)` satisfies that mixed order; backward satisfies `(x DESC,y ASC)`. It cannot satisfy `(x ASC,y ASC)` merely by reversing direction.

### Example 9

A 100-row range touches two hot leaves but performs 100 cold random heap fetches. A covering or clustered scan wins despite identical tree comparison complexity.

### Example 10

`LIMIT 20` stops after 20 visible, fully rechecked rows—not 20 raw index candidates. Dead/invisible/lossy candidates require continued scanning while respecting upper bound/cancellation.

## Cross-Program Connections

- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies binary-search invariants, output-sensitive complexity, and reference models.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies ordered maps, lexicographic keys, iterators, and range semantics.
- [Programming Languages — Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies latch coupling, optimistic validation, restarts, reclamation, and linearizability.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies cache/prefetch/I/O effects.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies tracing, tail latency, cancellation, and fault injection.

## References

1. PostgreSQL Global Development Group, [B-Tree Search Source](https://github.com/postgres/postgres/blob/master/src/backend/access/nbtree/nbtsearch.c), current lower/upper-bound loop invariants and move-right behavior.
2. PostgreSQL Global Development Group, [B-Tree Index README](https://github.com/postgres/postgres/blob/master/src/backend/access/nbtree/README), current pivots, high keys, right links, duplicates, scanning, and concurrency notes.
3. PostgreSQL Global Development Group, [Index Scanning](https://www.postgresql.org/docs/current/index-scanning.html), current access-method ordering, scan direction, tuple-return, and visibility responsibilities.
4. PostgreSQL Global Development Group, [Indexes and ORDER BY](https://www.postgresql.org/docs/current/indexes-ordering.html), current direction, NULL placement, tie-breaker, and multicolumn ordering behavior.
5. PostgreSQL Global Development Group, [Multicolumn Indexes](https://www.postgresql.org/docs/current/indexes-multicolumn.html), current leading-column/range and skip-scan guidance.
6. SQLite Project, [Query Planning](https://www.sqlite.org/queryplanner.html), official lookup, range, multicolumn, covering, and ordering examples.
7. Oracle, [How MySQL Uses Indexes](https://dev.mysql.com/doc/refman/8.4/en/mysql-indexes.html), current MySQL 8.4 leftmost-prefix and access guidance.
8. Philip L. Lehman and S. Bing Yao, [Efficient Locking for Concurrent Operations on B-Trees](https://www.csd.uoc.gr/~hy460/pdf/p650-lehman.pdf), *ACM TODS* 6(4), 1981.
9. Goetz Graefe, [Modern B-Tree Techniques](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/p669-graefe.pdf), search, scan, concurrency, and implementation survey.
10. Ramakrishnan and Gehrke, *Database Management Systems*, 3rd ed., McGraw-Hill, 2003, index search/range foundations.

## Exercises

### Exercise 1

Trace lower-bound and upper-bound for targets 5,10,11,40,41 in leaf `(5,10,10,20,40)`. Give loop partitions and returned indices.

### Exercise 2

Under root `(15,30)` and DBE-031 leaves, enumerate results/pages for `[10,30]`, `(10,30)`, `[26,40)`, `[41,+infinity)`, and backward `(10,30]`.

### Exercise 3

Normalize queries over index `(tenant ASC,status ASC,time DESC,id ASC)` including equality prefix, time range, NULL status, mixed ORDER BY, logical duplicates, and an exclusive continuation key.

### Exercise 4

Design a concurrent forward cursor across repeated right splits, page deletion/reuse, cancellation, and snapshot changes. State pin/latch/version, high-key, resume-key, and bounded-restart rules.

### Exercise 5

Design a production experiment comparing plain, covering, bitmap, clustered, and sequential scans across selectivity, cache, clustering, visibility/dead rows, limits, concurrency, storage, and correctness checks.

## Answers to the Exercises

### Answer 1

For `(5,10,10,20,40)`: lower bounds are target 5→0, 10→1, 11→3, 40→4, 41→5; upper bounds are 5→1, 10→3, 11→3, 40→5, 41→5. Each `[lo,hi)` step preserves entries before `lo` `<target` (or `<=` for upper) and entries at/after `hi` `>=target` (or `>`). Duplicate 10 demonstrates why lower and upper differ. A full answer records each midpoint update and terminates only at `lo=hi`.

### Answer 2

`[10,30]` emits 10,15,20,25,30 and visits L0,L1,L2; `(10,30)` emits 15,20,25 and must cross L0/L1 then observe 30 in L2 to stop under simple traversal. `[26,40)` starts after L1's 25, follows L2, emits 30, and stops before 40; it visits L1,L2. `[41,+infinity)` descends L2, lower-bound reaches end, and returns empty after L2. Backward `(10,30]` positions at 30, emits 30,25,20,15, and stops before/equal 10, visiting L2,L1,L0 under validated left traversal.

### Answer 3

Use the full physical lexicographic comparator. `tenant=7,status='ready',time between a and b` creates a contiguous tenant/status prefix with time bounds reversed in physical DESC order and ID sentinels. `status IS NULL` uses the index's declared NULL position, not SQL equality. An ORDER BY matches only if its remaining directions equal the index forward order or all reverse together after fixed equality columns. Logical duplicates are distinguished by time/id and any engine tie-breaker. Keyset continuation is exclusive upper-bound after the complete last-returned physical key; omitting ID can repeat/skip equal prefixes. A predicate only on time or status across tenants is not one contiguous interval.

### Answer 4

Bind snapshot/index incarnation/comparator and a complete exclusive resume key. Pin/latch or version-read each page, validate checksum/type/generation/range, and copy the next/high-key state before release according to protocol. If target/resume is at or beyond high key, follow validated right link; on version mismatch, deletion, reuse, backward movement, excessive hops, or broken range, restart from root using resume key. Never retain raw slot as cursor across release. Emit only entries strictly after resume, advance resume after a visible/rechecked result as required by cursor semantics, and honor snapshot isolation. Bound hops/restarts/time/output; cancellation releases resources. Page reclamation must prevent identity reuse while protected.

### Answer 5

Use equal data/schema/snapshot/results and validate every plan against a sorted logical reference including NULLs, duplicates, endpoints, visibility, residuals, order, and limit. Vary selectivity, contiguous/distributed ranges, clustering, covering width, cache cold/warm, dead/invisible fraction, recheck rate, table/index size, concurrency, storage, and limit. Record internal/leaf pages, comparisons, candidates, visible/returned rows, base fetches, buffer/storage hits/bytes/latency, prefetch waste, bitmap memory, sort, CPU, locks, throughput, p50/p99, and write-maintenance cost. Repeat/canary without forced global plans; include statistics error, cancellation, failover, and rollback. Results are workload/hardware/version evidence, not universal dominance.
