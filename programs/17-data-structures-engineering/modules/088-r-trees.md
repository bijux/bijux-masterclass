---
module_id: DSE-088
program: Data Structures Engineering
level: 2
module_number: 88
title: R-Trees
status: complete
last_verified: 2026-08-30
---

# R-Trees

## One-Page Review

### Governing question

How can a balanced, page-oriented hierarchy of bounding rectangles index extended spatial objects while controlling overlap, occupancy, mutation, concurrency, and false-positive rechecks?

### Essential definitions

An **R-tree** stores entries ((B,	ext{pointer})), where (B) is a minimum bounding rectangle (MBR). Leaf entries bound data objects; internal entries bound every rectangle in their child. Unlike a k-d split, sibling MBRs may overlap, so a query can descend multiple branches.

For rectangle (B=[l_x,u_x]\times[l_y,u_y]),

\[
\operatorname{area}(B)=(u_x-l_x)(u_y-l_y).
\]

Insertion usually chooses a child minimizing required area enlargement, with tie rules based on area or occupancy. Overflow splits entries into nodes subject to maximum capacity (M) and minimum fill (m). Search visits every child MBR intersecting the query, then rechecks candidate objects using exact geometry when MBRs are lossy.

### Central model, mechanism, or theorem

Correctness follows from enclosure: if every child object is contained by each ancestral MBR, then a subtree whose MBR is disjoint from the query cannot contain an intersecting object. Performance depends on tree height, page occupancy, MBR area, margin, overlap, dead space, and object/query distribution. R*-tree policies add forced reinsertion and optimize combinations of area, margin, and overlap.

### Critical invariants

- Every stored rectangle is normalized and finite: lower coordinate never exceeds upper.
- Every internal MBR encloses all child MBRs exactly or conservatively.
- Non-root nodes respect declared occupancy after committed structural changes.
- All leaves remain at the same depth in a balanced R-tree.
- Search follows every intersecting MBR; overlap means multiple branches may be required.
- Lossy bounding tests produce candidates, not final exact geometry answers.
- Page splits, parent updates, root changes, and recovery are atomic under the storage protocol.

### Common failures

Failures include treating siblings as disjoint, omitting an intersecting branch, storing stale parent MBRs, confusing containment with intersection, reversing min/max coordinates, ignoring floating-point outward rounding, optimizing only height, splitting into underfull pages, forgetting exact recheck, losing entries during reinsertion, exposing half a root split, and promising logarithmic search regardless of overlap.

### Compact example

A static packed teaching index groups 12 rectangles into four leaves of capacity three. The root MBR is ((0,0,16,10)); leaf MBR area totals 166 and pairwise overlap area totals 24. An inclusive query rectangle ((5,3,10,7)) intersects two leaf MBRs and returns objects C, D, F, and K, exactly matching a scan.

### Connections

[DSE-087](087-k-d-trees.md) supplies region-pruning proofs, metric discipline, and immutable rebuild patterns. The roadmap successor is [DSE-089, “Locality-Sensitive Hashing”](../ROADMAP.md), which trades exact spatial intersection for probabilistic similarity candidates. Database storage, geospatial systems, transaction recovery, and concurrency determine whether the page index remains durable and useful.

## Governing Question

How should an R-tree be represented, searched, updated, split, bulk-loaded, persisted, and measured so that bounding-box pruning is correct and overlap does not erase its I/O advantage?

## Why This Matters

Points are not enough for roads, parcels, trajectories, time intervals, CAD objects, or bounding boxes. Their spatial extent can cross partitions. R-trees group nearby rectangles into disk-sized balanced nodes and bound groups recursively, allowing intersection, containment, point-stabbing, spatial join, and nearest-style searches.

R-tree correctness is simple to state but demanding to maintain. One missed parent enlargement creates false negatives. One overlarge MBR preserves correctness but increases false positives and page reads. Split and reinsertion heuristics are workload-sensitive. Database implementations must additionally handle locks, write-ahead logging, page splits, crash recovery, vacuum, and exact predicate rechecks.

## Prerequisites and Retrieval

Retrieve:

- axis-aligned boxes, intersection, containment, area, perimeter/margin, and minimum distance;
- balanced multiway search trees, page occupancy, split propagation, and root growth;
- [DSE-087](087-k-d-trees.md) on region lower bounds and exact rechecking;
- write-ahead logging, latches versus transactional locks, copy-on-write publication, and checksums;
- floating-point outward rounding and total-order/domain validation.

Two closed rectangles intersect exactly when their intervals overlap on every dimension:

\[
l_i^A\le u_i^B\quad\land\quad l_i^B\le u_i^A
\]

for each axis (i). Touching at an edge counts as intersection under this convention; another API may choose interior-only semantics.

## Learning Objectives

After this chapter, you should be able to:

1. derive MBR enclosure and disjoint-pruning correctness;
2. trace intersection, containment, insertion choice, overflow split, and deletion condensation;
3. compare linear/quadratic splits, R*-tree reinsertion, and bulk-loading policies;
4. quantify occupancy, area, margin, overlap, dead space, and page visits;
5. specify exact recheck, numeric rounding, concurrency, WAL, and recovery obligations;
6. diagnose stale MBRs, underfill, overlap explosion, high-dimensional collapse, and corrupt pages;
7. verify structural invariants and query answers against exhaustive geometry.

## Core Exposition

### Hierarchy of bounding rectangles

An R-tree node corresponds naturally to a storage page. A leaf entry contains an object's MBR plus record identifier or payload pointer. An internal entry contains a child-page pointer plus an MBR enclosing that child's entries. A node normally holds at most (M) entries and, except for root cases, at least (m).

All leaves have equal depth, so height grows and shrinks through root changes as in B-tree families. The keys are not a nonoverlapping scalar partition. Sibling MBRs can overlap, and one object may intersect several siblings even though it is stored in one leaf. Search is therefore a branching traversal.

The minimal enclosing rectangle of rectangles (B_1,\ldots,B_t) has each lower coordinate equal to the minimum child lower coordinate and each upper coordinate equal to the maximum child upper coordinate. Parent MBRs may conservatively exceed this minimum and remain correct, but looser boxes cause extra visits. Under-approximating a child is incorrect.

### Intersection and containment search

For an intersection query (Q), visit an internal entry exactly when (B_i\cap Q\ne\varnothing). At leaves, apply the MBR predicate to produce candidates. If indexed objects are themselves rectangles and the requested predicate is rectangle intersection, this may be exact. For polygons, curves, geography, compressed keys, or other lossy representations, fetch the object and recheck the true predicate.

Containment predicates have different direction. “Objects contained by Q,” “objects containing Q,” and “objects intersecting Q” use different tests. An operator class or query planner must bind the correct consistent function. A permissive bounding predicate may return extra candidates; it must never exclude a possible exact match.

Nearest-neighbor traversal orders nodes by a lower bound such as minimum distance from the query to an MBR. A priority queue explores the smallest bound first and stops when remaining bounds cannot beat the result frontier. The lower bound and exact distance must use compatible geometry, coordinate reference system, and periodic/geodesic semantics.

### Choosing a subtree

To insert rectangle (E), descend from the root. Guttman's area-enlargement heuristic chooses the child minimizing

\[
\Delta A=\operatorname{area}(\operatorname{MBR}(B,E))-\operatorname{area}(B),
\]

breaking ties by smaller area and then deterministic policy. Near the leaf level, R*-tree variants emphasize overlap enlargement because leaf overlap directly multiplies query paths. Every chosen ancestor must expand to enclose (E).

Local minimum enlargement is a heuristic, not a global optimum. Different insertion orders create different trees. Bulk workloads should not be evaluated only under friendly order. Record the split/choose policy and benchmark sorted, reverse, clustered, diagonal, overlapping, and random streams.

### Overflow and split

When a node exceeds (M), divide its (M+1) entries into two groups, each meeting minimum occupancy. The **linear split** cheaply selects separated seeds; the **quadratic split** seeks a pair that would waste large area if grouped and repeatedly assigns entries by enlargement difference. Both are heuristics.

R*-tree overflow treatment may remove a fraction of entries far from the node center and reinsert them at the same level before splitting, once per level per insertion. Reinsertion can improve global grouping, but it needs recursion guards, complete accounting, and a recovery story. R*-tree split selection considers axis/order margin and then overlap/area. It spends more CPU during update to reduce future I/O.

A split propagates a new child entry upward and may split ancestors; a root split creates a new root. At no visible instant may a committed record lack a reachable leaf, have a parent box that excludes it, or be reachable inconsistently under the transaction model.

### Deletion and condensation

Deletion removes a leaf entry and tightens boxes upward. If a node falls below (m), traditional condensation removes the underfull node from its parent and reinserts its remaining entries at the proper level, potentially shrinking the root. Tombstone and rebuild designs trade immediate structural work for read amplification.

Reinserting internal entries at the wrong level changes leaf depth and breaks balance. Losing an orphan list during crash recovery loses records. Deletion tests must cover cascading underflow, root with one child, empty tree, duplicate rectangles, and concurrent scans.

### Quality metrics

Height and occupancy affect page I/O but do not describe spatial quality. Measure:

- MBR area or volume;
- margin/perimeter, which correlates with shape and enlargement;
- pairwise sibling overlap area;
- dead space between child union and parent MBR;
- fanout and fill distribution;
- query page visits, candidates, exact matches, and recheck ratio;
- update, split, reinsertion, and WAL volume.

Overlap is especially harmful because a query entering an overlap follows multiple branches. High dimension makes volume and overlap behavior worse; many coordinates create broad MBRs and diminished pruning. X-trees, priority R-trees, space-filling-curve B-trees, or domain partitioning may be better.

### Bulk loading and layout

Bulk loading can outperform repeated insertion. Sort-Tile-Recursive orders rectangles by one coordinate, partitions into vertical slices sized for pages, sorts each slice by another coordinate, packs leaves, and recursively packs upper levels. Hilbert ordering maps centers to a space-filling key and packs nearby keys. Packed trees offer high fill and reproducible layout for static data.

Updates after packing gradually reduce quality. Use immutable segments plus a mutable tree, scheduled rebuild, or online maintenance. Page capacity derives from usable bytes divided by entry size, including child IDs, rectangle coordinates, transaction metadata, alignment, and checksums—not a symbolic (M) chosen in isolation.

### Numeric and geometric semantics

Validate (l_i\le u_i), dimension, coordinate reference system, and finiteness. Floating conversion can shrink a stored bound and cause false negatives. SQLite documents outward rounding concerns for floating R-tree coordinates. Conservatively round lower bounds downward and upper bounds upward where formats narrow precision.

Longitude wrap, spherical distance, dateline-crossing boxes, and projected coordinates cannot be treated as ordinary Cartesian rectangles without a stated transformation. Split wrapping objects, use a periodic representation, or adopt a geometry-aware operator class. MBRs are candidates; exact geographic predicates remain authoritative.

### Concurrency and recovery

Structural modification operations may touch a leaf, ancestors, sibling/new pages, and root. Page latches protect memory structure; transaction locks protect logical conflicts. Deadlock-free latch ordering, right-link or predicate-lock strategies, and reader restart rules are implementation-specific.

Write-ahead logging must make page allocation, entry movement, MBR updates, parent insertion, and root publication recoverable and idempotent. A crash after child split but before parent link cannot strand records. Copy-on-write trees instead publish a new root after durable child pages. Both need checksums, generation identity, reachability audits, and orphan reclamation.

### Verification strategy

Structural validation walks every page, checks level consistency, occupancy, normalized rectangles, parent enclosure, child reachability, uniqueness/expected multiplicity, and root rules. Query property tests compare intersection, containment, point, and nearest results with exhaustive geometry. Mutation histories compare the live set after inserts/deletes/reinserts and crash points.

Performance experiments report dataset/query distributions, dimension, page bytes, entry format, cache state, occupancy, overlap, page reads, candidates, rechecks, and latency. A tree passing structural checks can still be useless due to overlap; a fast tree can still be wrong if exact recheck is omitted.

The bounded model below is a static, two-level packed rectangle hierarchy, not a dynamic R-tree implementation. It verifies normalized inputs, leaf MBR containment, occupancy, area/overlap metrics, and exact intersection results against a scan. It does not implement split, reinsertion, deletion, nearest search, pages, concurrency, or recovery.

<!-- bijux-verify: {"id":"packed-r-tree-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"rectangles=12\nleaf_capacity=3\nleaves=4\nroot_mbr=(0, 0, 16, 10)\nleaf_mbrs=[(0, 0, 4, 9), (4, 1, 9, 10), (7, 0, 12, 9), (11, 0, 16, 8)]\nleaf_occupancies=[3, 3, 3, 3]\ncontainment_valid=True\ntotal_leaf_area=166\npairwise_leaf_overlap_area=24\nquery=(5, 3, 10, 7)\nvisited_leaves=2\nmatches=['C', 'D', 'F', 'K']\nmatches_bruteforce=True\nvalid=True\nevidence=packed_r_tree_model\n","stderr":""}} -->
```python
RECTANGLES = (
    ("A", 0, 0, 2, 2), ("B", 1, 3, 3, 5),
    ("C", 4, 1, 6, 3), ("D", 5, 4, 8, 7),
    ("E", 7, 0, 9, 2), ("F", 8, 3, 10, 6),
    ("G", 11, 1, 13, 4), ("H", 12, 5, 15, 8),
    ("I", 2, 6, 4, 9), ("J", 6, 8, 9, 10),
    ("K", 10, 7, 12, 9), ("L", 14, 0, 16, 3),
)
LEAF_CAPACITY = 3


def rectangle_key(entry):
    return entry[1], entry[2], entry[0]


def bounds(entry):
    return entry[1], entry[2], entry[3], entry[4]


def mbr(entries):
    return (
        min(entry[1] for entry in entries),
        min(entry[2] for entry in entries),
        max(entry[3] for entry in entries),
        max(entry[4] for entry in entries),
    )


def intersects(left, right):
    return (
        left[0] <= right[2]
        and right[0] <= left[2]
        and left[1] <= right[3]
        and right[1] <= left[3]
    )


def contains(outer, inner):
    return (
        outer[0] <= inner[0]
        and outer[1] <= inner[1]
        and inner[2] <= outer[2]
        and inner[3] <= outer[3]
    )


def area(box):
    return (box[2] - box[0]) * (box[3] - box[1])


def overlap_area(left, right):
    width = max(0, min(left[2], right[2]) - max(left[0], right[0]))
    height = max(0, min(left[3], right[3]) - max(left[1], right[1]))
    return width * height


ordered = sorted(RECTANGLES, key=rectangle_key)
leaves = [
    ordered[start:start + LEAF_CAPACITY]
    for start in range(0, len(ordered), LEAF_CAPACITY)
]
leaf_mbrs = [mbr(leaf) for leaf in leaves]
root_mbr = (
    min(box[0] for box in leaf_mbrs),
    min(box[1] for box in leaf_mbrs),
    max(box[2] for box in leaf_mbrs),
    max(box[3] for box in leaf_mbrs),
)
containment_valid = all(
    contains(leaf_mbrs[index], bounds(entry))
    for index, leaf in enumerate(leaves)
    for entry in leaf
)
pairwise_overlap = sum(
    overlap_area(leaf_mbrs[left], leaf_mbrs[right])
    for left in range(len(leaf_mbrs))
    for right in range(left + 1, len(leaf_mbrs))
)

query = (5, 3, 10, 7)
visited_leaves = 0
matches = []
for index, leaf in enumerate(leaves):
    if intersects(leaf_mbrs[index], query):
        visited_leaves += 1
        matches = matches + [
            entry[0] for entry in leaf if intersects(bounds(entry), query)
        ]
matches = sorted(matches)
brute_force = sorted(
    entry[0] for entry in RECTANGLES if intersects(bounds(entry), query)
)
valid = containment_valid and matches == brute_force

print(f"rectangles={len(RECTANGLES)}")
print(f"leaf_capacity={LEAF_CAPACITY}")
print(f"leaves={len(leaves)}")
print(f"root_mbr={root_mbr}")
print(f"leaf_mbrs={leaf_mbrs}")
print(f"leaf_occupancies={[len(leaf) for leaf in leaves]}")
print(f"containment_valid={containment_valid}")
print(f"total_leaf_area={sum(area(box) for box in leaf_mbrs)}")
print(f"pairwise_leaf_overlap_area={pairwise_overlap}")
print(f"query={query}")
print(f"visited_leaves={visited_leaves}")
print(f"matches={matches}")
print(f"matches_bruteforce={matches == brute_force}")
print(f"valid={valid}")
print("evidence=packed_r_tree_model")
```

## Definitions and Notation

- (B=[l,u]): axis-aligned rectangle/box; **MBR**: minimum box enclosing entries.
- (M,m): maximum and minimum non-root entries per node.
- **Area enlargement**: additional MBR area needed to include an entry.
- **Margin**: sum of edge lengths or generalized perimeter measure.
- **Overlap**: measure shared by sibling MBRs.
- **Dead space**: parent MBR measure not occupied by child regions.
- **Candidate**: index result needing exact predicate recheck.
- **Forced reinsertion**: removing selected overflowing-node entries and reinserting them at the same level.
- **Condensation**: repairing underfull paths after deletion.
- **Bulk loading**: constructing packed levels from a collection rather than incremental insertion.

## Mechanisms, Invariants, or Proof Structure

### Search proof

By induction, every descendant object MBR is contained by its ancestral entry MBR. If an ancestral MBR is disjoint from query (Q), every descendant is disjoint from (Q); pruning is safe. If it intersects, search must descend because containment alone cannot exclude a match. At leaves, lossy keys require an exact recheck.

### Update proof obligations

Insertion keeps old entries, adds the new entry exactly once, preserves occupancy and equal leaf depth, and enlarges every ancestor. Split partitions all overflowing entries into two valid groups. Deletion removes exactly the target, preserves/reinserts underfull contents at their level, and tightens ancestors without under-approximation. Recovery must replay these transformations atomically.

### Systems invariants

- root reachability accounts for all committed entries and no unintended duplicates;
- pages form an acyclic equal-leaf-depth hierarchy;
- every child box is normalized and contained by its parent box;
- occupancy/root exceptions match format version;
- page LSN/checksum/generation agree with recovery state;
- query operator and exact recheck implement the declared geometry;
- performance audits track both candidate amplification and page I/O.

## Alternatives and Trade-Offs

k-d and K-D-B trees suit points and disjoint partitions; R-trees suit extended objects and paged dynamic storage. Quadtrees/grid files exploit known spatial domains. Space-filling-curve B-trees reuse mature scalar storage but approximate multidimensional locality and may duplicate intervals. BVHs prioritize ray/proximity workloads, often with immutable rebuild/refit. GiST is a framework whose consistent, union, penalty, picksplit, and distance methods can express R-tree-like operator classes while the database owns generic tree machinery.

Linear splits minimize update CPU but can create poor overlap. Quadratic splits spend more CPU for better groups. R*-tree reinsertion and overlap-aware splits improve many workloads but amplify writes and complicate recovery. Bulk packing maximizes static quality; dynamic updates preserve freshness. Wider pages increase fanout but also per-page scan and split cost. Compressed coordinates save I/O only if outward rounding preserves enclosure.

## Failure Modes and Misconceptions

- **Sibling MBRs partition space.** They may overlap extensively.
- **Balanced height guarantees logarithmic search.** Overlap can force traversal of most pages.
- **An intersecting parent proves a matching child.** It only prevents pruning.
- **MBR equality is exact geometry equality.** Nonrectangular objects need recheck.
- **Containment and intersection operators are interchangeable.** Their direction and candidate logic differ.
- **Tightening boxes is always safe.** A box smaller than any child creates false negatives.
- **Float conversion is harmless.** Inward rounding can exclude the source geometry.
- **Every split into two pages is valid.** Minimum occupancy and all-entry accounting must hold.
- **Forced reinsertion is ordinary insertion.** Level, recursion limits, and recovery lineage matter.
- **Deleting the leaf entry completes deletion.** Ancestors, underflow, root, and orphan entries remain.
- **Page latches provide transactional isolation.** Structural safety and logical concurrency are distinct.
- **A fast MBR scan validates results.** Exact geometry and exhaustive oracle comparisons are required.

## Worked Examples

### Example 1

**MBR construction.** Rectangles ((1,2,4,5)) and ((3,0,8,3)) have enclosing MBR ((1,0,8,5)) with area (7\times5=35). **Conclusion:** parent bounds use coordinatewise minima and maxima.

### Example 2

**Disjoint pruning.** Child MBR x-range is ([0,4]), while query x-range is ([5,9]). Because one dimension is disjoint, rectangles cannot intersect regardless of y. **Conclusion:** a single disjoint axis safely prunes the child.

### Example 3

**Area enlargement.** Existing MBR ((0,0,4,4)) has area 16. Adding ((3,3,6,5)) yields ((0,0,6,5)), area 30, enlargement 14. **Conclusion:** insertion penalty measures future bounding expansion, not distance between centers.

### Example 4

**Overlap cost.** Two leaf MBRs overlap on ([7,9]\times[1,9]), area (2\times8=16). Queries in that region visit both leaves. **Conclusion:** overlap converts one logical region into multiple I/Os.

### Example 5

**Lossy recheck.** A road polyline's MBR intersects a parcel MBR, but the actual line bends around the parcel. The index returns a candidate; exact geometry rejects it. **Conclusion:** false positives are permitted, false negatives are not.

### Example 6

**Outward rounding.** True lower x is 0.1 but a narrowed float rounds upward. A point exactly at the true edge may be excluded. Store a representable lower value no greater than truth and upper value no less than truth. **Conclusion:** conservative numeric encoding protects enclosure.

### Example 7

**Split accounting.** Capacity (M=4) overflows with five entries and minimum (m=2). A 1/4 partition is invalid; 2/3 is valid if both groups' boxes enclose their entries. **Conclusion:** split heuristics operate inside occupancy constraints.

### Example 8

**Root growth.** A leaf root splits into two leaves. A new internal root with two child entries raises every leaf depth from zero to one uniformly. **Conclusion:** height changes through a special atomic root transition.

### Example 9

**Condense after delete.** A non-root leaf at minimum occupancy two loses one entry. Remove the leaf, collect its remaining entry for reinsertion at leaf level, tighten ancestors, and possibly shrink a single-child root. **Conclusion:** deletion is a tree repair workflow.

### Example 10

**Crash boundary.** A split's new page is durable, but the parent pointer is not. Recovery must redo/complete the logged parent insertion or reclaim the unreachable page without losing moved records. **Conclusion:** logical split correctness depends on WAL ordering and idempotence.

## Cross-Program Connections

- **Database Engineering:** pages, GiST, query planning, selectivity, recheck, WAL, vacuum, and spatial joins own production behavior.
- **Data Engineering:** coordinate schemas, CRS transformations, batch bulk-loads, and late updates determine index identity.
- **Concurrent Programming:** latch coupling, split propagation, reader restart, and page reclamation protect structure.
- **Geospatial Engineering:** dateline, spherical distance, topology, and exact predicates exceed plain Cartesian MBRs.
- **Storage Engineering:** fill factor, page size, compression, checksums, and cache behavior shape I/O.
- **Security Engineering:** malformed boxes, NaNs, overlap attacks, corrupt pages, and expensive exact rechecks require limits.

## References

1. Antonin Guttman, [R-trees: A Dynamic Index Structure for Spatial Searching](https://sigmodrecord.org/1984/06/01/r-trees-a-dynamic-index-structure-for-spatial-searching/), *SIGMOD*, 1984; official record.
2. Antonin Guttman, [R-Trees: A Dynamic Index Structure for Spatial Searching](https://www.cs.princeton.edu/courses/archive/fall08/cos597B/papers/rtrees.pdf), university-hosted paper copy.
3. A. Guttman and Michael Stonebraker, [R-Trees Technical Report](https://digicoll.lib.berkeley.edu/record/139859), UC Berkeley, 1983; library archive record.
4. Norbert Beckmann, Hans-Peter Kriegel, Ralf Schneider, and Bernhard Seeger, [The R*-tree: An Efficient and Robust Access Method for Points and Rectangles](https://sigmodrecord.org/1990/06/06/the-r-tree-an-efficient-and-robust-access-method-for-points-and-rectangles/), *SIGMOD*, 1990.
5. SQLite Project, [The SQLite R*Tree Module](https://www.sqlite.org/rtree.html), accessed 2026-08-30.
6. PostgreSQL Global Development Group, [GiST Indexes](https://www.postgresql.org/docs/current/gist.html), PostgreSQL 18 documentation, accessed 2026-08-30.
7. PostgreSQL Global Development Group, [Indexes](https://www.postgresql.org/docs/current/indexes.html), PostgreSQL 18 documentation, accessed 2026-08-30.

## Exercises

### Exercise 1

Compute the MBR, area, and area enlargement when box ((2,1,7,5)) absorbs entry ((6,4,10,9)).

### Exercise 2

Prove disjoint-MBR pruning for intersection search and explain why an intersecting MBR cannot be accepted as an exact polygon match.

### Exercise 3

An index starts returning false negatives after converting double bounds to float. Diagnose and design a safe format migration.

### Exercise 4

Design a WAL-safe overflow split and parent propagation protocol, including crash points, reader behavior, and validation.

### Exercise 5

Choose between dynamic R*-tree insertion, STR bulk loading plus delta, and a space-filling-curve B-tree for a parcel archive with nightly batches and daytime edits. Define benchmark evidence.

## Answers to the Exercises

### Answer 1

The enclosing MBR is ((2,1,10,9)). Original area is ((7-2)(5-1)=20). New area is ((10-2)(9-1)=64). Enlargement is 44. This penalty does not account for sibling overlap or margin, so an R*-style chooser may prefer a different child after considering those objectives.

### Answer 2

Every descendant object's MBR (D) lies inside ancestor MBR (B). If (B\cap Q=\varnothing), then no subset (D\subseteq B) intersects (Q); pruning cannot lose a match. If (B\cap Q\ne\varnothing), some or no descendants may intersect, so traversal is required. A polygon can occupy only part of its MBR; intersecting boxes are a necessary but not sufficient condition for polygon intersection, requiring exact recheck.

### Answer 3

Narrowing rounded some lower bounds upward or upper bounds downward, breaking enclosure. Stop writes, identify the affected format/version, and compare stored boxes with source geometry. Define directed outward conversion, reject nonfinite/unnormalized coordinates, and rebuild from authoritative doubles rather than widening already-damaged floats. Dual-read exact scans verify no false negatives at edges. Publish format and operator version atomically, retain rollback, and add edge/next-representable property tests.

### Answer 4

Latch the overflowing page, choose a deterministic valid partition, allocate a page, and log full entry movement/new-page initialization before exposing it. Log old-page after-image or physiological changes, then latch/update the parent with tightened old and new child MBRs. Recursively split ancestors; publish a root change through a logged root-pointer record. Readers use latch coupling or restart on structural sequence changes. Recovery redo is idempotent by page LSN and completes reachable parent links; undo or orphan cleanup preserves record ownership. Validate occupancy, all-entry accounting, parent containment, equal leaf depth, reachability, checksums, and exhaustive sampled queries.

### Answer 5

Nightly archives favor STR-packed immutable segments with high fill and low overlap; daytime edits enter a small transactional R*-tree delta, queried alongside segments and folded into the next build. Fully dynamic R*-tree is preferable only if edits dominate and immediate single-index visibility outweighs fragmentation. A space-filling B-tree is attractive when scalar storage tooling, range partitioning, and replication dominate, but candidate interval amplification must be measured. Benchmark page reads, overlap, fill, candidate/recheck ratio, build/edit/WAL cost, crash recovery, storage, spatial joins, skew, large parcels, and exact scan agreement under actual query windows.
