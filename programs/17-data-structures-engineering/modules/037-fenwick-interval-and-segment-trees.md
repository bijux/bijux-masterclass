---
module_id: DSE-037
program: Data Structures Engineering
level: 1
module_number: 37
title: Fenwick, Interval, and Segment Trees
status: complete
last_verified: 2026-08-30
---

# Fenwick, Interval, and Segment Trees

## One-Page Review

### Governing question

How should an engineer choose and prove a Fenwick tree, array segment tree, lazy segment tree, or interval-search tree when the workload mixes prefix aggregates, range aggregates, range updates, and geometric interval overlap?

### Essential definitions

- A **Fenwick tree** (binary indexed tree) stores a decomposition of array prefixes in one indexed array.
- `lowbit(i)=i&(-i)` for positive two's-complement integer `i`; Fenwick cell `i` summarizes `(i-lowbit(i),i]` in one-based coordinates.
- A **prefix query** aggregates `[0,r)`; an invertible group operation can derive `[l,r)` from two prefixes.
- An **array segment tree** stores an associative aggregate for canonical subranges in a binary hierarchy.
- A **monoid** is a set with an associative operation and identity; it need not have inverses or be commutative.
- **lazy propagation** stores a deferred range action at a node and pushes it only before children must be distinguished.
- A **monoid action** maps aggregates compatibly with combination; action composition order is part of the contract.
- An **interval-search tree** is an ordered tree keyed by interval start and augmented with maximum endpoint in each subtree.
- Two half-open intervals `[a,b)` and `[c,d)` overlap iff `a<d` and `c<b`.
- A **canonical cover** partitions a query interval into `O(log n)` segment-tree nodes under the standard fixed-index layout.

### Central model, mechanism, or theorem

A Fenwick tree moves through implicit ancestors by clearing the least-significant set bit during prefix query and adding that bit during point update. It uses `O(n)` words and `O(log n)` update/query time with small constants. Arbitrary range queries from two prefixes require an inverse, such as subtraction for sums; min has no such inverse.

A segment tree stores `aggregate(node)=op(left,right)` over a fixed index range. Associativity makes decomposition independent of parenthesization; identity handles empty pieces. Point update and range query touch `O(log n)` nodes in a balanced layout. Lazy range updates require an action that can transform a whole-node aggregate from the tag and segment length, plus associative, correctly ordered tag composition.

An interval tree solves a different problem: dynamic interval objects, not array positions. Ordered starts guide search, while `max_high` proves when a subtree cannot overlap a query. A balanced base gives `O(log n)` insertion/deletion and `O(log n+k)` reporting under the usual interval-tree algorithm, where `k` results are emitted.

### Critical invariants

1. Index base, endpoint inclusivity, empty ranges, and domain bounds are declared once and used everywhere.
2. Fenwick cell `i` equals the aggregate of its exact lowbit-defined responsibility interval.
3. Segment-tree internal aggregates equal ordered combination of children; padding leaves carry the identity.
4. Lazy tags describe exactly the deferred action on a node range; composition order matches chronological application.
5. Interval-tree global key order and base balance hold independently of `max_high`.
6. `max_high(x)=max(x.high,max_high(left),max_high(right))` under a declared empty identity.
7. Arithmetic, endpoint, size, allocation, and index computations cannot overflow or escape capacity.
8. Readers observe links, aggregates, and lazy tags from one coherent version; update publication and reclamation are explicit.

### Common failures

- Confusing interval trees with segment trees because both contain the word “interval.”
- Mixing zero-based external indices with one-based Fenwick internals.
- Calling `add(0,...)` in a one-based loop and never advancing.
- Deriving arbitrary range min/max from two prefix minima.
- Assuming a segment operation may be nonassociative or reordering a noncommutative operation.
- Forgetting identity-filled padding leaves or returning a numeric sentinel that is not a true identity.
- Applying a lazy tag to a sum without multiplying by segment length.
- Composing “set” and “add,” affine, or reversal tags in the wrong temporal order.
- Using closed-interval overlap tests for half-open intervals, creating boundary false positives.
- Pruning an interval subtree from a stale `max_high` value.

### Compact example

For values `2,1,3,4,2,5,1,6`, a Fenwick tree reports prefix `[0,5)=12`, range `[2,7)=15`, and first prefix reaching 18 at index 6. Adding 6 at index 3 changes those to 18, 21, and index 4. A lazy sum segment tree independently applies `+3` to `[2,6)`, producing `[2,7)=27`, total 36, and exact point values. An interval tree over six half-open intervals reports `B,C,D` overlapping `[6,11)` and none overlapping `[8,9)`; its validator checks global low-order and every `max_high`.

### Connections

[DSE-036](036-order-statistic-trees.md) supplies augmentation and prefix-count reasoning. [DSE-004](004-time-space-and-allocation-cost.md) and [DSE-006](006-memory-locality-and-cache-behavior.md) supply cost/layout models. The [program roadmap](../ROADMAP.md) continues with heaps, meldable priority queues, skip lists, tries, and union-find.

## Governing Question

Which algebra, coordinate model, update/query pattern, layout, endpoint policy, overflow boundary, and concurrency contract justify each range structure and its claimed complexity?

## Why This Matters

Range queries appear in telemetry, schedulers, finance, editors, games, databases, geometry, memory managers, compression, and analytics. A static prefix array answers range sums quickly but updates poorly. A balanced ordered tree handles dynamic keys but may waste locality for dense indices. Fenwick and segment trees exploit a fixed or coordinate-compressed index universe; interval trees exploit ordered endpoints and subtree pruning.

These structures are often taught as memorized loops. Production failures instead occur at their contracts: half-open versus closed endpoints, integer overflow, nonassociative operators, incorrect tag composition, stale augmentation after rotation, non-power-of-two padding, concurrent mixed versions, or claims that omit output size. The durable skill is deriving the structure from its algebra and workload.

The combined chapter is intentional because selection requires distinguishing three similarly named tools. It does not collapse them into one implementation. Fenwick trees represent prefix decompositions, segment trees represent canonical array ranges, and interval-search trees index interval objects for overlap. Their proofs, memory behavior, update powers, and failure modes differ.

## Prerequisites and Retrieval

Retrieve array indexing, capacity, checked arithmetic, and layout from [DSE-011](011-fixed-arrays.md) and [DSE-012](012-dynamic-arrays-and-geometric-growth.md). Retrieve global BST order, rotations, deletion, and handles from [DSE-031](031-binary-search-trees.md), [DSE-032](032-avl-trees.md), and [DSE-033](033-red-black-trees.md). Retrieve augmentation equations, inverses, counter width, persistence, and validation from [DSE-036](036-order-statistic-trees.md). Retrieve property testing and benchmark discipline from [DSE-009](009-property-based-testing-of-data-structures.md) and [DSE-010](010-benchmarking-a-structure-without-misleading-results.md).

## Learning Objectives

After completing this module, you should be able to:

1. derive Fenwick responsibility intervals and prove prefix/update traversals;
2. state when two prefix aggregates can and cannot produce an arbitrary range;
3. derive segment-tree construction, point update, and ordered range decomposition from a monoid;
4. specify and prove a lazy action, aggregate mapping, and tag-composition order;
5. distinguish array segment trees from geometric interval-search trees;
6. prove interval overlap pruning using ordered starts and subtree maximum endpoints;
7. choose recursive/iterative, compact/padded, dynamic/static, ephemeral/persistent layouts;
8. define endpoints, empty ranges, coordinate compression, duplicates, overflow, and serialization;
9. design independent invariant, oracle, exhaustive, adversarial, fault, concurrency, and benchmark evidence;
10. select a range structure from update/query algebra, density, output size, locality, and latency requirements.

## Core Exposition

**Begin with the abstract operations.** Let an array contain `a[0..n)`. Decide whether updates replace a point, add a delta, add/assign/transform a range, insert coordinates dynamically, or change interval objects. Decide whether queries ask prefix sum, arbitrary aggregate, first prefix satisfying a monotone predicate, interval overlap existence, or all overlaps.

The answer determines algebra. Prefix sums use addition and subtraction. Range minimum uses associative `min` and identity `+infinity`, but no inverse. String concatenation is associative and noncommutative, so left-to-right order matters. Range-add/range-sum lazy propagation needs a tag action that increases a segment sum by `delta*length`. Interval overlap uses ordered endpoints and maximum-high augmentation, not a monoid decomposition of array cells.

Use half-open array ranges `[l,r)` unless an external protocol dictates otherwise. They compose without double counting, allow empty `l=r`, and make length `r-l`. Interval objects may be closed in a domain such as integer reservations; then overlap and adjacent-boundary rules differ. Convert once at the boundary rather than scattering `+1` adjustments.

**Fenwick cells are implicit binary suffix blocks.** Externally expose zero-based positions; internally map position `p` to `i=p+1`. For positive `i`, `lowbit(i)=i&-i` isolates its least-significant set bit in two's-complement arithmetic. Cell `bit[i]` stores the sum over one-based indices `i-lowbit(i)+1..i`, equivalently external half-open range `[i-lowbit(i),i)`.

For example, `bit[12]` has `lowbit=4` and covers external `[8,12)`. `bit[8]` covers `[0,8)`. These aligned blocks overlap across the whole array, but the blocks chosen for any prefix partition it exactly.

To compute prefix `[0,r)`, start at internal `i=r`. Add `bit[i]`, then set `i-=lowbit(i)`, clearing its least-significant set bit. Each block ends where the remaining prefix currently ends; clearing bits strictly decreases `i`. At most the number of index bits are visited.

To add delta at external position `p`, start `i=p+1`. Every Fenwick cell whose responsibility interval contains that position is found by `i+=lowbit(i)`. The changed bit pattern moves to the next implicit ancestor until `i>n`. Starting at internal zero is invalid because `lowbit(0)=0` and the loop cannot advance.

The invariant proof has two parts. Construction/update maintains each cell as its exact responsibility aggregate. Query indices select disjoint responsibility intervals whose union is the requested prefix. Addition is commutative, but generalized Fenwick variants require care: update direction and prefix decomposition may demand commutativity or inverses depending on the operation/API.

**Arbitrary Fenwick ranges need algebraic cancellation.** For an additive group, `sum([l,r))=prefix(r)-prefix(l)`. XOR similarly self-inverts. Prefix minimum does not contain enough information to subtract the contribution of `[0,l)`; two identical prefix minima can arise from different suffix minima. Use a segment tree, a restricted monotone-update Fenwick variant with carefully proved semantics, or another structure.

Range updates can be transformed. A difference array with point delta updates supports range addition `[l,r)` by adding `d` at `l` and `-d` at `r`, while prefix query recovers the point value. Two Fenwick trees can support range-add/range-sum using an algebraic identity over weighted differences. Derive boundary formulas under one indexing convention; copying one-based equations into zero-based code is a common off-by-one bug.

Fenwick prefix lower-bound (frequency-to-symbol search) uses binary lifting over the implicit tree. It is valid when cumulative totals are monotone, usually nonnegative frequencies. Maintain a candidate index and accumulated prefix; test power-of-two jumps without exceeding `n`. Negative values destroy monotonicity, so “first prefix at least target” cannot use that descent correctly.

**Segment trees materialize a range hierarchy.** Leaves represent elements; each internal node represents the concatenation of its two child ranges. With monoid `(S,op,e)`, store `tree[x]=op(tree[left],tree[right])`. Associativity ensures any canonical decomposition gives the same parenthesized result. Identity represents empty ranges and padding.

Commutativity is not required. An iterative range query normally keeps a left accumulator and a right accumulator. When taking a left boundary node, append it to the left accumulator; when taking a right boundary node, prepend it to the right accumulator. Finish with `op(left_acc,right_acc)`. Combining all selected nodes in discovery order corrupts string/matrix/function composition.

Build bottom-up in `O(n)` for an array-backed tree, often padding to the next power of two and allocating about `2*size`. Unused leaves store `e`. A point replacement changes one leaf and recomputes ancestors to root in `O(log n)`. A half-open query advances boundary indices upward, selecting at most a constant number of nodes per level.

Recursive `4n` layouts make segment boundaries explicit and simplify lazy propagation. Iterative `2*power_of_two` layouts improve compactness and locality for point-update/range-query monoids. Exact memory, index arithmetic, and empty-`n` behavior must be checked; expressions such as `4*n`, `2*size`, or next-power-of-two can overflow before allocation rejects them.

**Lazy propagation is an algebra, not a flag trick.** Suppose each node stores aggregate `s` over length `len`, and a tag `f` represents a deferred action on every element. A mapping computes the updated aggregate without visiting leaves. For range add/range sum, `mapping(d,(sum,len))=(sum+d*len,len)`.

Tags compose. If old pending tag `g` should happen first and new tag `f` second, the stored combined tag must represent `f∘g`. For addition, order is invisible; for assignment-plus-addition, affine maps, matrices, reversals, and timestamps it is not. Define the composition function in words, equation, and tests.

A full-cover update applies mapping to the node aggregate and composes the tag. A partial update/query first pushes the pending tag to both children, clears it at the parent, recursively visits relevant children, then recomputes parent aggregate. Pushing too late reads stale children; pushing without clearing double-applies; clearing before child application loses work.

The mapping must distribute over aggregation in the structure's representation. Adding `d` to every element maps a sum using length; applying `max(x,d)` to a sum cannot generally be derived from sum and length alone. Segment-tree-beats-style structures store richer extrema/count metadata and use separate amortized proofs; they are not ordinary lazy propagation.

Boundary-search helpers such as “maximum right endpoint while predicate holds” require a pure monotone predicate with `predicate(e)=true`, plus ordered accumulation. If values can be negative, a predicate such as prefix sum `<=T` may cease to be monotone. Document preconditions instead of returning a plausible boundary.

**Interval-search trees index objects, not array slots.** Store a valid interval `(low,high,payload)` in a balanced BST ordered by `(low,high,unique_id)` or another total duplicate policy. Augment each node with `max_high`, the maximum high endpoint in its subtree. Under half-open semantics require `low<high`; decide whether empty intervals are rejected or represented separately.

Intervals `[a,b)` and `[c,d)` overlap iff `a<d && c<b`. Touching `[0,4)` and `[4,7)` do not overlap. Closed intervals would use `a<=d && c<=b`. Endpoint representation, infinities, time zones, and overflow-safe normalization belong in the contract.

For existence search at query `[qlo,qhi)`, inspect the current interval. If it overlaps, return it. Otherwise, if the left child exists and `left.max_high>qlo`, the left subtree may overlap, so search there. If not, every left interval ends at or before `qlo`; go right. Balanced height yields `O(log n)` for one match under the standard proof.

Reporting all overlaps needs more pruning and must include output cost. A subtree with `max_high<=qlo` cannot overlap. Because nodes are ordered by low, once a node/subtree's minimum relevant low is `>=qhi`, rightward candidates cannot overlap. A correct traversal reports `k` results in output-sensitive time under the chosen structure/algorithm; it cannot be `O(log n)` independent of `k`.

`max_high` follows the same rotation/update discipline as subtree size. Insert initializes to its own high and propagates maxima. Delete follows the physical removal/replacement path. Rotation copies the old subtree maximum to the promoted root and recomputes the demoted node, or recomputes demoted then promoted generically. Stale overestimates reduce pruning performance; stale underestimates can cause false negatives and are correctness failures.

**The three structures occupy different design points.** Fenwick is exceptionally compact for prefix-friendly algebra and point updates. A segment tree supports arbitrary monoids and richer range updates at more memory/code cost. An interval tree supports a dynamic set of intervals with arbitrary coordinates and overlap reporting, not aggregation over every coordinate position.

Coordinate compression can map a known finite coordinate set to dense indices for Fenwick/segment trees. Preserve ordering and distinguish points from elementary gaps; interval coverage often needs endpoints plus gap cells. New unseen coordinates may require rebuild/dynamic segment trees. Compression does not preserve physical distances unless stored separately.

A dynamic implicit segment tree allocates nodes only on visited paths across a huge coordinate universe. It avoids a dense array but adds pointer/allocation overhead, reclamation, and adversarial node-growth risk. A persistent segment tree path-copies `O(log U)` nodes per update, providing versioned queries but multiplying memory. Wavelet trees and later succinct structures address different static/rank/select trade-offs.

**Numerics and identities need domain proofs.** Sum and `delta*length` can overflow even if each element fits. Use checked/wider arithmetic or prove bounds from capacity and value limits. Min identity must compare greater than every legal value without colliding with arithmetic; represent optional aggregates when no safe sentinel exists.

Floating-point addition is not mathematically associative, so segment results can depend on tree shape and update order. If reproducibility or error bounds matter, specify fixed layout, compensated summaries, exact/fixed-point arithmetic, or accepted tolerance. NaN breaks ordinary min/max expectations unless a policy defines ordering.

Endpoint `high+1` conversion from closed to half-open can overflow at maximum representable value. Use tagged unbounded endpoints, widened types, or direct closed formulas. Validate `low<=high` before subtracting lengths. Size and allocation multiplication use checked arithmetic.

**Concurrency and persistence must publish a coherent aggregate graph.** A Fenwick update writes several cells; a concurrent prefix query can combine before/after deltas and observe no linearizable point. A segment range update writes tags and aggregates across nodes; an interval rotation changes links and maxima. Atomic words individually do not make the operation atomic.

External locks are simplest. Sharding helps only when operations' touched paths/ranges do not contend or a higher-level snapshot combines versions. Immutable persistent roots allow snapshot queries after one atomic root publication, with path-copy allocation and safe reclamation. Version counters/optimistic validation may retry queries that overlap writes.

For distributed/parallel aggregates, distinguish exact linearizable queries, snapshot queries, eventually consistent summaries, and approximate sketches. A mergeable monoid enables parallel build/reduction, but concurrent mutable range updates still require ordering. Lazy tag composition across replicas is not automatically commutative or conflict-free.

**Serialization should prefer logical state plus policy.** Fenwick cells and segment internal nodes are derived caches; serialize the bounded logical array, algebra/schema/version, then rebuild and validate. Persisting exact internal arrays can speed startup only with layout/version/checksum validation. Interval trees serialize interval records, not pointers or trusted maxima/colors.

Untrusted inputs can force huge `n`, deep dynamic-tree allocation, endpoint overflow, enormous overlap output, or expensive user operations. Bound coordinates, elements, nodes, tag depth, arithmetic, query range, output count/bytes, recursion, allocation, and time. Cancellation must not publish half-applied updates.

**Verification pairs an elementary oracle with representation invariants.** For Fenwick, independently recompute every cell responsibility interval and all prefix/range queries from the logical array. Test `n=0/1`, all indices, endpoints, powers of two and neighbors, negative deltas, total overflow, and monotonicity violations for prefix search.

For segment trees, recompute every node aggregate from logical leaves, verify padding identity and lazy meaning, and compare every small `[l,r)` query/update sequence with a plain array. Use noncommutative strings/matrices to catch ordering bugs. Exhaust overlapping/disjoint/nested range updates; force tag identities and composition order.

For interval trees, validate global `(low,high,id)` bounds, base balance, unique reachability, exact `max_high`, and payload lifetime. Compare every overlap result with a linear scan across disjoint, touching, nested, equal-low/high, extreme, duplicate, and high-output intervals. Test deletion/rotation cases and under/overestimated corruption.

Inject allocation, arithmetic, user-operation, comparator, serialization, cancellation, and publication failures. Under concurrency pause at every cell/tag/link/aggregate/root write and reclamation. Benchmark prefix/range/update/output mixes against prefix arrays, block/sqrt decomposition, balanced augmented trees, B-trees, database indexes, and sketches. Report `n`, density, algebra cost, updates, query lengths/results, bytes, cache/TLB/branches, allocations, contention/retries, throughput/tails, hardware/toolchain, repetitions, uncertainty, and raw artifacts.

The executable evidence implements three sequential finite structures: additive Fenwick with prefix lower-bound under nonnegative values, lazy range-add/range-sum segment tree, and static balanced half-open interval-search tree with exact `max_high`. It proves only its recorded integer trace—not generic algebra, dynamic interval deletion/balance, overflow/failure safety, concurrency, persistence, or production performance.

<!-- bijux-verify: {"id":"range-structure-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"fenwick_prefix_5=12\nfenwick_range_2_7=15\nfenwick_first_prefix_18=6\nfenwick_after=2,1,3,10,2,5,1,6\nfenwick_prefix_5_after=18\nfenwick_range_2_7_after=21\nfenwick_first_prefix_18_after=4\nsegment_range_2_7=15\nsegment_range_2_7_after=27\nsegment_total_after=36\nsegment_after=2,1,6,7,5,8,1,6\ninterval_root_low=9\ninterval_root_max_high=18\ninterval_hits_6_11=B,C,D\ninterval_hits_8_9=\ninvariant=True\nevidence=finite_range_structure_trace\n","stderr":""}} -->
```python
from dataclasses import dataclass


class FenwickSum:
    def __init__(self, values):
        self.values = list(values)
        self.size = len(values)
        self.cells = [0] * (self.size + 1)
        for index, value in enumerate(values):
            internal = index + 1
            while internal <= self.size:
                self.cells[internal] += value
                internal += internal & -internal

    def add(self, index, delta):
        self.values[index] += delta
        internal = index + 1
        while internal <= self.size:
            self.cells[internal] += delta
            internal += internal & -internal

    def prefix(self, end):
        total = 0
        while end > 0:
            total += self.cells[end]
            end -= end & -end
        return total

    def range_sum(self, start, end):
        return self.prefix(end) - self.prefix(start)

    def first_prefix_at_least(self, target):
        if target <= 0:
            return 0
        index = 0
        accumulated = 0
        step = 1 << (self.size.bit_length() - 1)
        while step > 0:
            candidate = index + step
            if candidate <= self.size and accumulated + self.cells[candidate] < target:
                index = candidate
                accumulated += self.cells[candidate]
            step //= 2
        return index if index < self.size else self.size

    def validate(self):
        for internal in range(1, self.size + 1):
            lowbit = internal & -internal
            expected = sum(self.values[internal - lowbit : internal])
            if self.cells[internal] != expected:
                raise AssertionError("Fenwick responsibility interval failed")
        return True


class LazyRangeSum:
    def __init__(self, values):
        self.size = len(values)
        self.sums = [0] * (4 * self.size)
        self.lazy = [0] * (4 * self.size)
        self._build(1, 0, self.size, values)

    def _build(self, node, low, high, values):
        if high - low == 1:
            self.sums[node] = values[low]
            return
        middle = (low + high) // 2
        self._build(2 * node, low, middle, values)
        self._build(2 * node + 1, middle, high, values)
        self.sums[node] = self.sums[2 * node] + self.sums[2 * node + 1]

    def _apply(self, node, low, high, delta):
        self.sums[node] += delta * (high - low)
        self.lazy[node] += delta

    def _push(self, node, low, high):
        if self.lazy[node] == 0 or high - low == 1:
            return
        middle = (low + high) // 2
        delta = self.lazy[node]
        self._apply(2 * node, low, middle, delta)
        self._apply(2 * node + 1, middle, high, delta)
        self.lazy[node] = 0

    def range_add(self, start, end, delta):
        def update(node, low, high):
            if end <= low or high <= start:
                return
            if start <= low and high <= end:
                self._apply(node, low, high, delta)
                return
            self._push(node, low, high)
            middle = (low + high) // 2
            update(2 * node, low, middle)
            update(2 * node + 1, middle, high)
            self.sums[node] = self.sums[2 * node] + self.sums[2 * node + 1]

        update(1, 0, self.size)

    def range_sum(self, start, end):
        def query(node, low, high):
            if end <= low or high <= start:
                return 0
            if start <= low and high <= end:
                return self.sums[node]
            self._push(node, low, high)
            middle = (low + high) // 2
            return query(2 * node, low, middle) + query(2 * node + 1, middle, high)

        return query(1, 0, self.size)

    def materialize(self):
        return [self.range_sum(index, index + 1) for index in range(self.size)]


@dataclass
class IntervalNode:
    low: int
    high: int
    name: str
    left: object = None
    right: object = None
    max_high: int = 0


class StaticIntervalTree:
    def __init__(self, intervals):
        ordered = sorted(intervals)

        def build(low, high):
            if low >= high:
                return None
            middle = (low + high) // 2
            start, end, name = ordered[middle]
            node = IntervalNode(start, end, name, max_high=end)
            node.left = build(low, middle)
            node.right = build(middle + 1, high)
            node.max_high = max(
                end,
                node.left.max_high if node.left is not None else end,
                node.right.max_high if node.right is not None else end,
            )
            return node

        self.root = build(0, len(ordered))

    def overlaps(self, query_low, query_high):
        matches = []

        def visit(node):
            if node is None or node.max_high <= query_low:
                return
            visit(node.left)
            if node.low < query_high and query_low < node.high:
                matches.append(node.name)
            if node.low < query_high:
                visit(node.right)

        visit(self.root)
        return matches

    def validate(self):
        def check(node, low_bound, high_bound):
            if node is None:
                return float("-inf")
            if not (low_bound < node.low < high_bound and node.low < node.high):
                raise AssertionError("interval order or bounds failed")
            left_max = check(node.left, low_bound, node.low)
            right_max = check(node.right, node.low, high_bound)
            actual_max = max(node.high, left_max, right_max)
            if node.max_high != actual_max:
                raise AssertionError("interval maximum failed")
            return actual_max

        check(self.root, float("-inf"), float("inf"))
        return True


initial = [2, 1, 3, 4, 2, 5, 1, 6]
fenwick = FenwickSum(initial)
print(f"fenwick_prefix_5={fenwick.prefix(5)}")
print(f"fenwick_range_2_7={fenwick.range_sum(2, 7)}")
print(f"fenwick_first_prefix_18={fenwick.first_prefix_at_least(18)}")
fenwick.add(3, 6)
print("fenwick_after=" + ",".join(map(str, fenwick.values)))
print(f"fenwick_prefix_5_after={fenwick.prefix(5)}")
print(f"fenwick_range_2_7_after={fenwick.range_sum(2, 7)}")
print(f"fenwick_first_prefix_18_after={fenwick.first_prefix_at_least(18)}")

segment = LazyRangeSum(initial)
print(f"segment_range_2_7={segment.range_sum(2, 7)}")
segment.range_add(2, 6, 3)
print(f"segment_range_2_7_after={segment.range_sum(2, 7)}")
print(f"segment_total_after={segment.range_sum(0, 8)}")
print("segment_after=" + ",".join(map(str, segment.materialize())))

intervals = StaticIntervalTree(
    [(0, 4, "A"), (3, 8, "B"), (5, 7, "C"), (9, 12, "D"), (11, 15, "E"), (14, 18, "F")]
)
print(f"interval_root_low={intervals.root.low}")
print(f"interval_root_max_high={intervals.root.max_high}")
print("interval_hits_6_11=" + ",".join(intervals.overlaps(6, 11)))
print("interval_hits_8_9=" + ",".join(intervals.overlaps(8, 9)))
print(f"invariant={fenwick.validate() and intervals.validate()}")
print("evidence=finite_range_structure_trace")
```

## Definitions and Notation

- `a[0..n)`: logical dense array.
- `[l,r)`: half-open range with length `r-l`.
- `lowbit(i)=i&(-i)`: isolated least-significant set bit for `i>0`.
- `prefix(r)`: aggregate over `[0,r)`.
- `(S,op,e)`: segment aggregate monoid.
- `F`: set of lazy actions, containing identity and closed under composition.
- `mapping(f,s,len)`: action of tag `f` on aggregate `s` for a segment length.
- `compose(f,g)=f∘g`: apply old `g` first, newer `f` second.
- `max_high(x)`: maximum high endpoint in interval node x's subtree.
- `k`: number of reported overlap results.
- **coordinate compression**: order-preserving mapping from known coordinates to dense ranks.
- **canonical cover**: disjoint stored segment nodes whose union is exactly a query range.

## Mechanisms, Invariants, or Proof Structure

Fenwick correctness derives each cell's lowbit responsibility interval. Prefix traversal clears bits to choose a disjoint exact partition; point update adds lowbit to visit every containing block. Group inverses derive arbitrary ranges; prefix lower-bound additionally requires monotone cumulative aggregates.

Segment correctness derives from a monoid: leaves plus identity padding, internal ordered combination, and a canonical query cover. Point updates recompute ancestors. Lazy correctness adds an action compatible with aggregate combination, exact segment length, identity, and chronologically ordered composition; push transfers authority to children before partial descent.

Interval-tree correctness combines global start-key order, balanced-tree height, and exact subtree maximum endpoints. Overlap algebra tests a node; `max_high` and ordered lows justify pruning. Reporting includes `k`. Mutation uses the base tree's link/rotation/deletion proof plus demoted-first augmentation maintenance.

## Alternatives and Trade-Offs

| Structure | Best fit | Main obligation |
|---|---|---|
| Prefix array | static prefix/range group queries | `O(n)` rebuild/update |
| Fenwick tree | compact point-add/prefix/group ranges | indexing/inverse/monotonicity limits |
| Iterative segment tree | point update, arbitrary monoid range | identity/order/padding |
| Lazy segment tree | compatible range action and aggregate | mapping/composition/push proof |
| Dynamic segment tree | sparse huge fixed universe | allocation/depth/resource limits |
| Persistent segment tree | versioned point/range queries | path-copy memory and reclamation |
| Interval-search tree | dynamic interval objects/overlap | balanced base, max endpoint, output cost |
| Sorted endpoints/sweep | offline batch geometry | not online mutable |
| Sqrt/block decomposition | simple medium-size ranges | `O(sqrt n)` operations/tuning |
| Augmented B-tree | page-resident ranges/aggregates | splits, concurrency, recovery |
| Sketch | approximate streaming quantiles/counts | explicit error, no exact answers |

## Failure Modes and Misconceptions

- **“Fenwick is a segment tree in a smaller array.”** both decompose ranges, but representation and supported algebra/update transformations differ.
- **“Segment trees store geometric segments.”** array segment trees store aggregates over index intervals; interval trees store interval objects.
- **“`i&-i` works for zero.”** it returns zero and update loops do not progress.
- **“Every prefix structure supports arbitrary ranges.”** cancellation requires an inverse or extra structure.
- **“Associativity means commutativity.”** ordered concatenation/matrix composition must preserve direction.
- **“Any sentinel is an identity.”** it must be neutral for every legal aggregate and arithmetic path.
- **“Lazy composition order does not matter.”** it matters for nearly every non-additive action.
- **“Push is a performance detail.”** incorrect push loses or duplicates logical updates.
- **“Touching intervals overlap.”** that depends on half-open versus closed semantics.
- **“One-match interval search reports all matches.”** output-sensitive traversal is a different operation.
- **“Stale maximum only slows search.”** underestimation can prune real results.
- **“Coordinate compression preserves distance.”** it preserves order, not numeric gaps unless modeled.
- **“Atomic cells make a Fenwick update atomic.”** multi-cell operations need snapshot/synchronization semantics.
- **“Asymptotic equality decides performance.”** layout, algebra cost, range distribution, writes, and cache behavior dominate constants.

## Worked Examples

### Example 1

Fenwick internal cell 12 has lowbit 4 and represents external `[8,12)`. Conclusion: the stored block is determined mechanically from the index bits.

### Example 2

Prefix 13 selects cells 13,12,8, covering `[12,13)`, `[8,12)`, `[0,8)` exactly. Conclusion: clearing the lowest set bit partitions a prefix without overlap.

### Example 3

Prefix minima of two arrays can match at `l` and `r` while their `[l,r)` minima differ. Conclusion: no subtraction-like inverse derives arbitrary range minimum.

### Example 4

String segments `"ab"`, `"cd"`, `"ef"` aggregate by concatenation. Reversing right-boundary discovery produces the wrong string. Conclusion: iterative queries need left and right accumulators for noncommutative monoids.

### Example 5

Adding 3 to a length-four segment changes its sum by 12, not 3. Conclusion: a lazy action maps aggregates using segment length.

### Example 6

An old assignment-to-5 tag followed by add-2 means constant 7; add then assignment means constant 5. Conclusion: tag composition represents chronology and is generally noncommutative.

### Example 7

Intervals `[0,4)` and `[4,8)` touch but fail `0<8 && 4<4`. Conclusion: half-open overlap excludes boundary-only contact.

### Example 8

If an interval subtree has `max_high=6` and query low is 6, no half-open interval there can overlap. Conclusion: `max_high<=qlo` is a sound prune under this convention.

### Example 9

A query overlaps 100,000 stored intervals. Finding/reporting them cannot be logarithmic total time. Conclusion: include output `k` in complexity and enforce result budgets.

### Example 10

A concurrent Fenwick query reads one updated cell and another old cell from the same delta path. The total matches no instant. Conclusion: word atomicity does not supply operation linearizability.

## Cross-Program Connections

- **Algorithms:** binary representations, monoids/groups/actions, canonical covers, augmentation, output sensitivity, and amortization derive the structures.
- **Programming languages:** generic algebra interfaces, checked indices, ownership, recursion, optional identities, and immutable versions shape APIs.
- **Databases:** page aggregates, temporal intervals, range predicates, MVCC, spatial indexes, write-ahead recovery, and result limits govern deployment.
- **Concurrent programming:** multi-cell updates, tag/link publication, snapshots, locks, versions, epochs, and reclamation determine observable correctness.
- **Data engineering:** prefix windows, time buckets, coordinate compression, streaming summaries, and approximate sketches define scale trade-offs.
- **Computer architecture:** contiguous arrays, cache lines, false sharing, pointer interval nodes, branches, and SIMD/in-node reduction affect constants.
- **Security engineering:** overflow, huge coordinates, dynamic-node growth, recursion, expensive operators, and overlap-output amplification need limits.

## References

1. Peter M. Fenwick, [A New Data Structure for Cumulative Frequency Tables](https://static.aminer.org/pdf/PDF/001/073/976/a_new_data_structure_for_cumulative_frequency_tables.pdf), Software—Practice & Experience 24(3), 1994. Primary paper for binary indexed representation, update/query traversal, and frequency search.
2. Peter M. Fenwick, [A New Data Structure for Cumulative Probability Tables: An Improved Frequency-to-Symbol Algorithm](https://www.cs.auckland.ac.nz/~peter-f/FTPfiles/TechRep110.pdf), University of Auckland technical report, 1995. Primary follow-up for binary lifting/search over cumulative frequencies and its boundary accounting.
3. Carnegie Mellon University 15-451 (Spring 2026), [Segment Trees](https://www.cs.cmu.edu/~yangp/15-451/lecture7.pdf). Current academic derivation of range queries, point/range updates, stored summaries, and lazy propagation.
4. AtCoder Library, [Segtree](https://atcoder.github.io/ac-library/master/document_en/segtree.html). Current official monoid, identity, point-update, half-open product, and boundary-search contract.
5. AtCoder Library, [Lazy Segtree](https://atcoder.github.io/ac-library/master/document_en/lazysegtree.html). Current official monoid-action, mapping, composition, identity, update/query, and complexity contract.
6. AtCoder Library, [Precise Segtree and LazySegtree Requirements](https://atcoder.github.io/ac-library/production/document_en/appendix.html). Official clarification of closure, representable subsets, overflow, and oracle assumptions.
7. AtCoder Library Project, [`segtree.hpp`](https://github.com/atcoder/ac-library/blob/master/atcoder/segtree.hpp). Current primary implementation source for iterative build, ordered half-open query, point update, and boundary search.
8. MIT OpenCourseWare 6.046J, [Augmenting Data Structures and Interval Trees](https://ocw.mit.edu/courses/6-046j-introduction-to-algorithms-sma-5503-fall-2005/eebc00db28f8650591e3be446a31f1cf_lec11.pdf). Primary academic source for interval overlap, maximum-high augmentation, search correctness, and maintenance.
9. Linux Kernel, [Red-black Trees—Augmented and Interval Trees](https://docs.kernel.org/core-api/rbtree.html). Current official propagation/copy/rotation callback and interval-search documentation.
10. Linux Kernel, [`interval_tree_generic.h`](https://github.com/torvalds/linux/blob/master/include/linux/interval_tree_generic.h). Current primary implementation source for max-end augmentation, insert/remove, half/closed-style endpoint conditions, pruning, and overlap iteration.

## Exercises

### Exercise 1

Derive Fenwick cell intervals, prefix traversal, point update, group range query, and prefix lower-bound. State indexing and monotonicity/inverse assumptions.

### Exercise 2

Implement an iterative segment tree for a noncommutative monoid. Prove canonical coverage, accumulator order, identity padding, update complexity, and empty-range behavior.

### Exercise 3

Specify lazy range assignment plus range addition over range sums. Define tag representation, mapping, composition chronology, identity, push, overflow, and exhaustive tests.

### Exercise 4

Prove half-open interval-tree one-match and all-match pruning. Extend insertion/deletion/rotation maintenance and state duplicate, endpoint, output, and lifetime policies.

### Exercise 5

Choose among prefix array, Fenwick, segment/lazy/dynamic/persistent trees, interval tree, B-tree augmentation, and sketches for three production workloads; design benchmarks and failure/concurrency evidence.

## Answers to the Exercises

### Answer 1

Use zero-based external p and one-based internal i=p+1. Cell i covers `[i-lowbit(i),i)` externally. Prefix starts i=r, accumulates the cell ending at i, then clears its lowest set bit; selected cells are disjoint and exactly cover `[0,r)`. Update starts p+1 and adds lowbit to enumerate every containing responsibility block. Both take at most the index bit width. For a group, `[l,r)=prefix(r) inverse prefix(l)` (subtraction for sums); min lacks an inverse. Prefix lower-bound binary-lifts over powers of two while maintaining a candidate prefix strictly below target. It requires cumulative monotonicity, normally nonnegative frequencies, and returns n if the target exceeds total. Validate zero/one endpoints, n=0, powers of two, target<=0/above-total, and negative-value rejection for search.

### Answer 2

Store leaves at a power-of-two base and internal `op(left,right)`; padding leaves are e. Query `[l,r)` with left=e,right=e. When l is a right child, append its node `left=op(left,node)` and increment. When r is a right boundary, decrement then prepend `right=op(node,right)`. Move both to parents until equal, return `op(left,right)`. Selected nodes are disjoint, ordered, and form the canonical cover; associativity permits their hierarchy, while two accumulators preserve noncommutative order. Empty range selects nothing and returns e. Point replacement updates one leaf and one ancestor per level, O(log n); build is O(n). Test string concatenation or matrices, every small range, padding, non-power-of-two n, and invalid boundaries.

### Answer 3

Represent a tag as optional assignment plus additive delta. Its action on `(sum,len)` is: if assignment exists, replace sum by assignment*len; then add delta*len. To compose newer f after older g, if f assigns, it overrides all of g and retains f's add; otherwise preserve g's assignment and add `f.add` to g's delta. Identity is no assignment/add zero. Full cover maps the aggregate and stores `compose(new,old)`; partial descent pushes the parent's tag to children in that order, resets parent identity, recurses, then combines children. Use checked multiplication/addition. Exhaust sequences add/add, set/set, set/add, add/set, nested/partial/disjoint ranges, identity/empty ranges, leaves, and compare every state/query with a plain array.

### Answer 4

For `[a,b)` versus `[qlo,qhi)`, overlap is `a<qhi && qlo<b`. Ordered lows and `max_high` justify pruning a subtree when `max_high<=qlo`; rightward search stops when candidate lows reach qhi. One-match search chooses a potentially overlapping left subtree or right otherwise; all-match traversal explores every nonpruned region and costs at least k to emit k results. Insert initializes high and propagates maxima; delete follows physical removal/replacement; rotations recompute demoted then promoted or use a proven copy/rotate callback. Key by `(low,high,id)` for duplicates, reject/define empty and unbounded intervals, bound outputs, state handle ownership/reclamation, and validate results against linear scan after exhaustive touching/nested/equal/extreme mutation histories.

### Answer 5

For a mostly static numeric array, build a prefix array for constant range sums; if point deltas are frequent, use Fenwick for compact group queries or segment tree for min/noninvertible monoids. For range add plus sum/min, use a lazy segment tree only after defining a compatible action; sparse huge coordinates suggest a bounded dynamic tree and version queries a persistent tree. For dynamic reservation-overlap reporting, use a balanced interval tree and include output k; dense known coordinates with coverage aggregates may instead use compressed segment trees. A storage engine may need augmented B-tree pages for locality/recovery. Streaming percentile estimates favor sketches when exactness is unnecessary. Benchmark real query/update lengths, outputs, density, algebra cost, memory/cache, allocations, concurrency, p50/tails, rebuilds, and raw traces; test overflow, endpoints, failures, crash/publication/reclamation, adversarial coordinates, and result amplification.
