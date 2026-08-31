---
module_id: DSE-087
program: Data Structures Engineering
level: 2
module_number: 87
title: k-d Trees
status: complete
last_verified: 2026-08-30
---

# k-d Trees

## One-Page Review

### Governing question

How can recursive axis-aligned partitions accelerate multidimensional range and nearest-neighbor queries while keeping geometry, pruning, balance, mutation, and dimensional limits correct?

### Essential definitions

A **k-d tree** indexes points (x\in\mathbb{R}^k) by recursively choosing an axis (a), a split value (s), and two subregions. A common balanced construction selects the median point on axis (a=\text{depth}\bmod k). The left subtree contains points ordered before the split and the right contains points after it under a declared tie rule.

An orthogonal range query reports points inside an axis-aligned box. A nearest-neighbor query maintains the best distance found, explores the query-side child first, then explores the other child only if its region can beat the incumbent. For a splitting plane under Euclidean distance, the lower bound is ((q_a-s)^2). Bounding boxes give stronger lower bounds:

$$
d^2(q,B)=\sum_i
\begin{cases}
(\ell_i-q_i)^2,&q_i<\ell_i,\\
(q_i-u_i)^2,&q_i>u_i,\\
0,&\ell_i\le q_i\le u_i.
\end{cases}
$$

### Central model, mechanism, or theorem

Correct pruning is branch-and-bound. A subtree may be skipped only when a proven lower bound on every point in its region exceeds the current admissible best distance. Median construction controls height; spatial separation controls pruning. A balanced tree can still visit most points in high dimension or adversarial geometry.

### Critical invariants

- Every node's subtree respects all ancestral half-space constraints.
- Axis, comparator, tie, duplicate, and numeric-domain rules are stable.
- Stored bounding boxes enclose every descendant and are refreshed after mutation.
- Distance lower bounds use the same metric and transformed coordinate space as exact distance.
- Exact search prunes only on a non-improvable bound; approximate search states its relaxation.
- Returned neighbors and ranges are checked against deterministic tie semantics.
- Source point storage remains immutable or changes through index-owned updates.

### Common failures

Common failures include promising (O(\log n)) worst-case queries, building an unbalanced insertion tree, pruning with distance instead of squared distance, using Euclidean plane bounds for a different metric, ignoring equal-axis points, mutating aliased coordinates, keeping stale boxes after deletion, treating NaN as ordered, and expecting low-dimensional pruning to survive hundreds of dimensions.

### Compact example

A median-built two-dimensional fixture contains 15 points, height 4, and root ((6,5)). For query ((9,4)), exact branch-and-bound visits 8 nodes and returns ((10,3)) at squared distance 2, matching exhaustive search. An inclusive box from ((7,1)) through ((10,4)) visits 8 nodes and reports exactly ((7,2),(8,1),(10,3)).

### Connections

[DSE-086](086-quantile-sketches.md) supplies ordered summaries, comparator discipline, and empirical-versus-formal evidence. The roadmap successor is [DSE-088, “R-Trees”](../ROADMAP.md), which indexes extended spatial objects and disk-oriented bounding hierarchies. Vector search, databases, graphics, robotics, and scientific computing reuse the same metric and pruning obligations.

## Governing Question

How should a k-d tree be constructed, queried, mutated, persisted, and benchmarked so that geometric pruning remains correct and its performance claims survive real data?

## Why This Matters

Many systems ask which points fall in a box, which observation is closest to a query, or which (k) candidates lie within a radius. Exhaustive scanning is simple and robust but costs (O(nk)) coordinate work per query. A k-d tree reuses spatial partitions across queries and can avoid examining large regions.

The structure is not a universal nearest-neighbor oracle. Its performance depends on dimension, distribution, metric, balance, leaf size, bounding boxes, and query workload. Correctness depends on subtle relationships between region bounds and distance. Mutable or externally owned arrays can invalidate partitions silently. Graduate-level engineering means proving pruning and measuring visited work, not quoting an average logarithmic slogan.

## Prerequisites and Retrieval

Retrieve:

- binary-search-tree ordering, selection/median construction, recursion, and height;
- vectors, axis-aligned hyperrectangles, Euclidean and Minkowski distance;
- branch-and-bound lower bounds, exact versus approximate answers, and tie breaking;
- floating-point total-order concerns, immutable index keys, and concurrent publication;
- exact rank/comparator discipline from [DSE-086](086-quantile-sketches.md).

Use squared Euclidean distance for comparisons to avoid unnecessary square roots:

$$
d^2(x,q)=\sum_{i=0}^{k-1}(x_i-q_i)^2.
$$

This monotone transformation preserves nearest ordering only because all distances are nonnegative and the square root is monotone.

## Learning Objectives

After this chapter, you should be able to:

1. derive k-d tree partition and region invariants;
2. construct a balanced tree with explicit axis and tie rules;
3. trace exact orthogonal range and nearest-neighbor pruning;
4. adapt lower bounds to bounding boxes, Minkowski metrics, and approximation;
5. evaluate dimension, leaf size, layout, rebuild, and alternative-index trade-offs;
6. diagnose degeneracy, duplicates, stale geometry, floating point, concurrency, and persistence failures;
7. verify results against brute force and benchmark visited nodes across declared workloads.

## Core Exposition

### Recursive spatial partition

At a node with split axis (a) and split coordinate (s), the left and right children inherit the parent's region intersected with (x_a\le s) and (x_a\ge s), adjusted by the implementation's strict/equal convention. Cycling axes is simple; choosing the axis of greatest spread can adapt to anisotropic data; sliding-midpoint rules can avoid empty cells. These policies produce different shapes but must preserve a provable region for each subtree.

A node may store one point, a bucket of points, or only a split with points in leaves. A leaf size greater than one shortens the tree and improves contiguous brute-force work. Pointer nodes are easy to mutate but incur allocation and cache misses. Flat arrays permit cache-friendly traversal and stable serialization. These are representation choices, not different meanings of k-d partitioning.

### Balanced construction

Repeated insertion follows a multidimensional comparison and can degenerate to height (n) for ordered data. Offline construction selects a median on the chosen axis and recursively partitions the halves. Full sorting at every level gives a clear (O(n\log^2 n)) implementation; linear-time selection at each level can achieve (O(n\log n)) expected or controlled construction, and presorted strategies offer other bounds and trade-offs.

Balance by point count controls height, not spatial quality. A median split may cut through a dense cluster or create elongated cells. Midpoint splitting may produce empty or badly imbalanced children. Modern implementations combine median or sliding-midpoint policies, leaf buckets, and compact bounding boxes. Benchmarks must report build time, memory, height, region aspect, and visited leaves.

Duplicates need a total tie key. Comparing only coordinate (a) leaves equal-axis points unordered. A deterministic build can compare ((x_a,x_0,\ldots,x_{a-1},x_{a+1},\ldots,	ext{id})). If identical points are distinct records, preserve identifiers or multiplicity. If they represent a set, canonicalize before build. The query API must specify ties among equally distant points.

### Orthogonal range search

For inclusive query box (Q=[l_0,u_0]\times\cdots\times[l_{k-1},u_{k-1}]), test each visited point against all dimensions. At a split on axis (a), the left child can intersect only if (l_a\le s); the right can intersect only if (s\le u_a), subject to the tree's equality convention. With stored subtree boxes, skip a child if its box is disjoint from (Q), and report or scan a compact subtree when its box is fully contained.

The output itself may be large, so range-query complexity includes (z), the number of reported records. For balanced, well-behaved low-dimensional trees, pruning is effective, but worst-case boxes can intersect many cells. Never advertise a query bound without output size and distribution/dimension premises.

### Exact nearest-neighbor search

Maintain incumbent ((D,p)), where (D=d^2(q,p)). At node point (x), update the incumbent using a deterministic pair such as ((d^2(q,x),x,	ext{id})). Explore the child containing (q) first, which often finds a close point early.

The opposite child lies beyond the splitting plane. Its minimum possible Euclidean squared distance is at least ((q_a-s)^2). If that lower bound is greater than (D), the child cannot improve the incumbent. If equal-distance ties must return the lexicographically smallest point, explore when the bound is equal; pruning on equality could hide a tie winner. Stored bounding boxes strengthen the test by summing per-axis outside distances.

The proof has three parts: the lower bound applies to every descendant; the incumbent is an actual point and thus an admissible upper bound; and pruning occurs only when lower bound cannot beat the required answer order. A bound from a different metric or stale box breaks the first part.

### k-nearest, radius, and approximate search

For (k)-nearest neighbors, keep a max-heap of the best (k) candidates. Until full, no finite pruning radius exists; afterward the worst retained distance is the upper bound. Radius search prunes boxes farther than (r) and reports candidates within (r). Both require deterministic duplicate/tie behavior and careful boundary comparison.

Approximate nearest-neighbor search may prune more aggressively. One common contract returns a neighbor no farther than ((1+\epsilon)) times the true distance. The pruning inequality must be derived in the same distance domain; if using squared distances, the multiplicative factor is squared. Approximation is an API contract, not a timeout that silently returns the current point.

### Metrics and transformations

Axis-aligned boxes support lower bounds for (L_p) metrics by aggregating coordinate gaps with the matching norm. Mahalanobis distance can be converted to Euclidean distance after a valid linear whitening transform, but the tree must index transformed points and queries. Cosine similarity on normalized vectors relates to Euclidean distance, yet zero vectors and normalization drift require policy.

Arbitrary non-metric dissimilarities may lack useful axis-aligned lower bounds. Even for Euclidean distance, feature scaling determines geometry: meters and millimeters, or one high-variance feature, can dominate. The coordinate schema and transform version belong to the index identity.

### The curse of dimensionality

As dimension grows, distances concentrate, bounding boxes overlap query balls in many coordinates, and plane bounds rarely exceed the incumbent. An exactly balanced tree may then visit nearly every point. Intrinsic dimension can matter more than raw dimension, but it must be measured rather than assumed.

Compare against brute force, ball trees, vantage-point trees, cover trees, inverted/product-quantization indexes, graph ANN structures, and domain-specific grids. Brute force with vectorized or GPU computation can beat tree traversal at moderate (n) or high (k). The correct index is a workload decision.

### Mutation, deletion, and rebuilding

In-place insertion is possible but gradually harms balance and region quality. Deletion is more complex than in a one-dimensional BST because replacements must preserve multidimensional ordering and boxes. Practical systems often use an immutable main tree plus a small mutable delta, tombstones, and periodic rebuild. Query both components and merge candidates.

Rebuild publication needs a generation: build from a stable snapshot, capture concurrent deltas, validate, atomically swap the root, and reclaim the old generation after readers finish. Coordinate arrays must be copied or made immutable. Official SciPy documentation warns that modifying aliased data can produce incorrect answers; an index over mutable keys is a correctness bug, not merely a cache issue.

### Persistence and validation

A serialized tree needs dimension, scalar type, endianness, comparator/tie rule, metric and transform, split policy, leaf size, point/schema version, boxes, node layout, count, generation, and checksum. Readers validate all indices, finite coordinates, child bounds, acyclicity, subtree containment, boxes, and counts before publication.

Testing uses brute force as an oracle for finite data. Generate empty, singleton, duplicate, collinear, grid, clustered, monotone, extreme-coordinate, and random cases. Verify range sets, nearest/k-nearest order, radius boundaries, and approximate ratios. Corrupt boxes and splits deliberately. Benchmark visited nodes and distance evaluations, not only wall time.

The bounded model below builds a balanced two-dimensional tree by full sorting at each level. It checks exact nearest neighbor and inclusive range results against brute force. It has no bounding boxes, buckets, mutation, persistence, high-dimensional experiment, or approximate mode, and its pruning count is evidence only for this fixture.

<!-- bijux-verify: {"id":"kd-tree-search","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"dimensions=2\npoints=15\nheight=4\nroot=(6, 5)\ntarget=(9, 4)\nnearest=(10, 3)\nnearest_distance_squared=2\nnearest_visited=8\nnearest_matches_bruteforce=True\nrange_low=(7, 1)\nrange_high=(10, 4)\nrange_points=[(7, 2), (8, 1), (10, 3)]\nrange_visited=8\nrange_matches_bruteforce=True\nvalid=True\nevidence=kd_tree_model\n","stderr":""}} -->
```python
POINTS = (
    (2, 3), (5, 4), (9, 6), (4, 7), (8, 1),
    (7, 2), (6, 5), (1, 8), (3, 9), (10, 3),
    (11, 7), (12, 2), (0, 0), (5, 9), (9, 9),
)


def key_x(point):
    return point[0], point[1]


def key_y(point):
    return point[1], point[0]


def build(points, depth=0):
    if not points:
        return None
    axis = depth % 2
    ordered = sorted(points, key=key_x if axis == 0 else key_y)
    middle = len(ordered) // 2
    return (
        ordered[middle],
        axis,
        build(ordered[:middle], depth + 1),
        build(ordered[middle + 1:], depth + 1),
    )


def distance_squared(left, right):
    return sum(
        (left[axis] - right[axis]) ** 2
        for axis in range(2)
    )


def nearest(node, target, best, visited):
    if node is None:
        return best, visited
    point, axis, left, right = node
    visited += 1
    candidate = distance_squared(point, target), point
    if candidate < best:
        best = candidate

    difference = target[axis] - point[axis]
    near, far = (left, right) if difference <= 0 else (right, left)
    best, visited = nearest(near, target, best, visited)
    if difference * difference <= best[0]:
        best, visited = nearest(far, target, best, visited)
    return best, visited


def range_query(node, low, high, output, visited):
    if node is None:
        return output, visited
    point, axis, left, right = node
    visited += 1
    if (
        low[0] <= point[0] <= high[0]
        and low[1] <= point[1] <= high[1]
    ):
        output = output + [point]
    if low[axis] <= point[axis]:
        output, visited = range_query(left, low, high, output, visited)
    if point[axis] <= high[axis]:
        output, visited = range_query(right, low, high, output, visited)
    return output, visited


def height(node):
    if node is None:
        return 0
    return 1 + max(height(node[2]), height(node[3]))


tree = build(POINTS)
target = (9, 4)
best, nearest_visited = nearest(
    tree, target, (10 ** 18, (10 ** 9, 10 ** 9)), 0
)
brute_nearest = min(
    (distance_squared(point, target), point)
    for point in POINTS
)
low = (7, 1)
high = (10, 4)
found, range_visited = range_query(tree, low, high, [], 0)
found = sorted(found)
brute_range = sorted(
    point
    for point in POINTS
    if low[0] <= point[0] <= high[0]
    and low[1] <= point[1] <= high[1]
)
valid = best == brute_nearest and found == brute_range

print("dimensions=2")
print(f"points={len(POINTS)}")
print(f"height={height(tree)}")
print(f"root={tree[0]}")
print(f"target={target}")
print(f"nearest={best[1]}")
print(f"nearest_distance_squared={best[0]}")
print(f"nearest_visited={nearest_visited}")
print(f"nearest_matches_bruteforce={best == brute_nearest}")
print(f"range_low={low}")
print(f"range_high={high}")
print(f"range_points={found}")
print(f"range_visited={range_visited}")
print(f"range_matches_bruteforce={found == brute_range}")
print(f"valid={valid}")
print("evidence=kd_tree_model")
```

## Definitions and Notation

- (k): coordinate dimension; (n): indexed point count.
- (a,s): split axis and split coordinate.
- (B=[\ell,u]): axis-aligned subtree bounding box.
- (d), (d^2): metric distance and squared Euclidean distance.
- **Incumbent**: best admissible candidate found so far.
- **Lower bound**: minimum possible distance from the query to every point in a region.
- **Leaf size**: threshold at which traversal switches to local brute force.
- **Exact search**: returns the answer under declared metric/tie rules.
- **Approximate search**: returns an answer satisfying a stated factor or additive contract.
- **Intrinsic dimension**: effective geometric dimension of the dataset/workload, distinct from coordinate count.

## Mechanisms, Invariants, or Proof Structure

### Partition induction

The root owns all space. Each child intersects its parent's region with one side of the node's split. If construction places every child point on the permitted side and recursive children preserve their inherited regions, every descendant satisfies all ancestral constraints. Bounding boxes are valid only if they enclose the point and both child boxes.

### Pruning proof

Let (L(q,R)) be a lower bound for every point in region (R), and let (D) be the distance to an actual incumbent. If (L>D), no point in (R) can improve distance. If ties affect answer identity, equality may still require exploration. Plane and box formulas must use the indexed metric/transform.

### System invariants

- count, reachability, acyclicity, height, axes, children, and boxes validate before publication;
- point coordinates and transform metadata are immutable for a generation;
- duplicate IDs and equal-distance output order are deterministic;
- tombstone/delta/main generations do not omit or duplicate records;
- exact sampled queries match brute force;
- performance reports include visited nodes, distance calculations, dimension, distribution, (n), leaf size, and hardware.

## Alternatives and Trade-Offs

Uniform grids and quad/octrees work well with bounded, regular space but can waste cells under skew. Range trees offer stronger orthogonal-query bounds at higher memory. R-trees index rectangles and disk pages. Ball and vantage-point trees partition by metric distance and support non-axis-aligned metrics. Cover trees target general metric spaces under expansion assumptions. Graph ANN, locality-sensitive hashing, and product quantization trade exactness for high-dimensional speed. Brute-force array scans offer minimal complexity, exactness, batching, SIMD, and GPU acceleration.

Median splits favor height; midpoint/sliding-midpoint splits can improve cell geometry; largest-spread axes adapt to scale; PCA-like splits tighten geometry at more build/query cost and version complexity. Small leaves deepen traversal; large leaves increase local scan. Mutable trees offer fresh results but degrade; immutable rebuilt trees give stable read performance and cheap lock-free publication.

## Failure Modes and Misconceptions

- **Balanced height guarantees logarithmic nearest search.** Geometry can force nearly full traversal.
- **All metrics share the plane bound.** The bound must be derived for the actual metric and transform.
- **Strictly greater pruning and greater-or-equal pruning are equivalent.** Equality matters for deterministic ties.
- **Equal axis values can go anywhere.** They need a stable construction and query convention.
- **Bounding boxes are optional metadata.** Once used for pruning, stale boxes cause wrong answers.
- **External coordinate mutation is harmless.** It invalidates partitions without touching tree nodes.
- **NaN is just another coordinate.** It breaks ordering and distance comparisons.
- **Dimension alone predicts performance.** Distribution, intrinsic dimension, scaling, query location, and leaf size matter.
- **Approximate means early exit.** It requires a proved approximation criterion.
- **Insertion preserves balance.** Long-lived incremental trees need balancing or rebuild.
- **Deletion is ordinary BST deletion.** Replacements must preserve all multidimensional constraints.
- **Wall-clock speed validates correctness.** Every optimized path still needs brute-force oracle checks.

## Worked Examples

### Example 1

**Median construction.** Fifteen points produce a median root with seven points on each side and, recursively, height four. Sequential insertion could produce height fifteen. **Conclusion:** build policy controls height independently of query pruning.

### Example 2

**Plane pruning.** Query coordinate on split axis is 9, split is 6, so plane squared distance is 9. If incumbent squared distance is 2, the far subtree cannot contain a closer Euclidean point and is pruned. **Conclusion:** compare squared bound with squared incumbent.

### Example 3

**Tie boundary.** Incumbent is point ((0,1)) at squared distance one, while the far region lower bound is also one and may contain lexicographically smaller ((-1,0)). **Conclusion:** exact deterministic tie search explores equality unless the tie rule proves otherwise.

### Example 4

**Range branch.** At x-split 6, inclusive box x-range ([7,10]) cannot intersect the left region (x\le6), so only the right branch is needed. If equality ownership overlaps at 6 and lower bound were 6, both relevant equality paths must be handled. **Conclusion:** range pruning follows interval intersection and tie convention.

### Example 5

**Box lower bound.** Query ((9,4)) and box ([0,5]\times[7,10]) have gaps 4 and 3, so squared lower bound is (4^2+3^2=25). An incumbent at squared distance 10 prunes the box. **Conclusion:** box bounds dominate a single-plane bound when multiple axes separate.

### Example 6

**Metric mismatch.** Under weighted squared distance (100(x_0-q_0)^2+(x_1-q_1)^2), an x-gap of two contributes 400, not four. **Conclusion:** unweighted Euclidean pruning applied to weighted search is invalid or needlessly weak depending on direction.

### Example 7

**Duplicate points.** Three records share coordinates ((5,5)). A set index may canonicalize them; a record index stores IDs and returns all three for a point range. **Conclusion:** multiplicity and tie identity belong to the data model.

### Example 8

**High-dimensional collapse.** In 100 dimensions, many boxes have a small gap in at least one axis but remain close in aggregate, causing both children to be explored repeatedly. A vectorized scan wins the benchmark. **Conclusion:** fall back based on measured visits, not loyalty to the index.

### Example 9

**Mutable alias.** An indexed array point moves from ((2,3)) to ((200,300)) without rebuilding. It remains under ancestral splits for the old coordinate and can be pruned incorrectly. **Conclusion:** copy, freeze, or route updates through index ownership.

### Example 10

**Immutable rebuild.** Main generation G has one million points; a delta has 5,000. Build G+1 from a snapshot, replay deltas after the snapshot offset, validate against brute-force samples, atomically publish, and retire G after reader epochs drain. **Conclusion:** rebuild is a transactional publication workflow.

## Cross-Program Connections

- **Database Engineering:** multidimensional predicates, optimizer selectivity, and page-aware indexes motivate R-trees and range trees.
- **Vector Search:** exact low-dimensional trees establish the branch-and-bound baseline for approximate high-dimensional indexes.
- **Concurrent Programming:** immutable roots, epoch reclamation, delta ownership, and snapshot safety govern read-heavy indexes.
- **Scientific Computing:** coordinate scale, periodic topology, floating-point inputs, and batch queries shape implementation.
- **Robotics and Graphics:** collision, ray, and proximity queries use related spatial bounding hierarchies.
- **Security Engineering:** untrusted coordinates, NaNs, degenerate builds, and serialized corruption can cause wrong answers or denial of service.

## References

1. Jon Louis Bentley, [Multidimensional Binary Search Trees Used for Associative Searching](https://cir.nii.ac.jp/crid/1363388844208283008), *Communications of the ACM* 18(9), 1975; institutional publication record.
2. Jon Louis Bentley, [Multidimensional Binary Search Trees Used for Associative Searching](https://cs.wmich.edu/gupta/teaching/cs6310/lectureNotes_cs6310/kdtree-bentley.pdf), archival university-hosted paper copy.
3. Jerome H. Friedman, Jon Louis Bentley, and Raphael A. Finkel, [An Algorithm for Finding Best Matches in Logarithmic Expected Time](https://www.sigmod.org/publications/dblp/db/journals/toms/toms3.html), *ACM TOMS* 3(3), 1977; ACM SIGMOD bibliographic record.
4. Songrit Maneewongvatana and David M. Mount, [Analysis of Approximate Nearest Neighbor Searching with Clustered Point Sets](https://arxiv.org/abs/cs/9901013), 1999.
5. SciPy Developers, [KDTree API and Algorithm Notes](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.html), SciPy 1.18 documentation, accessed 2026-08-30.
6. SciPy Developers, [cKDTree Implementation](https://github.com/scipy/scipy/blob/main/scipy/spatial/_ckdtree.pyx), accessed 2026-08-30.
7. Russell A. Brown, [Building a Balanced k-d Tree in O(kn log n) Time](https://arxiv.org/abs/1410.5420), 2014.

## Exercises

### Exercise 1

For query ((4,9)), compute the squared distance lower bound to box ([7,10]\times[2,6]). Decide whether it can be pruned with incumbent squared distance 17 and explain the equality rule.

### Exercise 2

Prove the split-plane pruning rule for exact Euclidean nearest neighbor and state how deterministic equal-distance ties change the comparison.

### Exercise 3

A production k-d tree returns stale answers after an in-place feature-normalization deployment. Diagnose the failure and design a safe migration.

### Exercise 4

Design an immutable main-tree plus mutable-delta architecture with concurrent queries, deletion, rebuild, validation, publication, and reclamation.

### Exercise 5

You must choose an index for 20 million 128-dimensional embeddings, exact two-dimensional map points, and disk-resident rectangles. Choose per workload and define benchmark evidence.

## Answers to the Exercises

### Answer 1

The x-gap is (7-4=3), and the y-gap is (9-6=3). The squared box distance is (3^2+3^2=18). Since 18 exceeds incumbent 17, every box point is farther and exact search may prune. If the lower bound were 17, pruning would depend on the answer contract: distance-only search may prune, but lexicographic or ID tie selection must explore unless the box cannot contain a preferred tie.

### Answer 2

Every point (x) in the far half-space lies across split plane (x_a=s), so (|x_a-q_a|\ge|s-q_a|). Euclidean squared distance sums nonnegative coordinate terms, hence (d^2(x,q)\ge(s-q_a)^2). If this bound exceeds squared incumbent (D), no far point improves it. When equality is possible and the required result selects a preferred point among equal distances, equality is not enough to prune; explore or maintain an additional lower bound on the tie key.

### Answer 3

Normalization changed indexed coordinates while tree partitions, boxes, and perhaps query transforms retained the old space. Freeze the old arrays, version the transform, and rebuild every point into a new generation using the new transform. Dual-query exact sampled cases against brute force in the new space, validate boxes and counts, then atomically publish the root and transform together. Reject queries with mismatched transform versions, retain rollback, and never mutate aliased coordinates beneath a live tree.

### Answer 4

Readers pin a generation and query its immutable main tree plus a small owner-controlled delta, filtering tombstones and merging candidates by distance/tie key. Updates append to a logged delta; deletes add versioned tombstones. Rebuild captures a source offset, constructs a balanced tree from live records, computes boxes, then replays later deltas. Validation checks structure, counts, containment, checksums, and brute-force sampled range/neighbor queries. Publish root, transform, schema, and generation atomically. New writes target the new delta; old readers drain through epochs or references before memory reclamation.

### Answer 5

For 128-dimensional embeddings, benchmark graph ANN or quantization indexes against vectorized CPU/GPU brute force; a k-d tree is only a measured baseline because pruning commonly collapses. Measure recall, distance ratio, p50/p99 latency, build/update cost, memory, and filtered-query behavior. For exact two-dimensional points, a balanced k-d tree or grid is plausible; measure visited nodes, output-sensitive ranges, and brute-force correctness under clusters/duplicates. For disk-resident rectangles, choose an R-tree-family page index because points and axis splits do not model object extents or I/O grouping. Measure page reads, overlap, split quality, update cost, recovery, and exact intersection results.
