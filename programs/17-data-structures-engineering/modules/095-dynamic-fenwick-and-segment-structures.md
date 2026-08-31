---
module_id: DSE-095
program: Data Structures Engineering
level: 2
module_number: 95
title: Dynamic Fenwick and Segment Structures
status: complete
last_verified: 2026-08-30
---

# Dynamic Fenwick and Segment Structures

## One-Page Review

### Governing question

How should an engineering team choose, specify, implement, persist, and validate Fenwick and segment-tree families for changing range data without confusing algebraic preconditions, coordinates, lazy composition, versioning, or concurrency guarantees?

### Essential definitions

A **Fenwick tree** stores partial aggregates over intervals determined by the least significant set bit. Point update and prefix aggregation visit (O(log n)) cells in a compact array. An arbitrary range sum is the difference of two prefixes; more generally, this subtraction requires a group inverse and is not available for every associative operation.

A **segment tree** stores an aggregate for each node interval. Its operation must be associative with an identity: a monoid. Point updates and range queries touch (O(log n)) canonical nodes. A **lazy segment tree** stores deferred range actions. Actions compose and must distribute over the stored aggregate, often requiring interval length in the node value.

“Dynamic” can mean changing values, inserting coordinates, allocating nodes on demand over a huge universe, preserving versions, or serving concurrent readers. These are different designs and costs.

### Central model, mechanism, or theorem

Fenwick cell (i) in one-based indexing owns ((i-lowbit(i),i]). A prefix query repeatedly clears the least significant set bit; an update repeatedly adds it. The visited intervals partition the prefix, which proves correctness and logarithmic work.

A segment-tree query decomposes ([l,r)) into disjoint canonical intervals. Associativity permits combining their aggregates, but noncommutative operations require left-to-right order. Lazy propagation maintains the invariant that each node aggregate already reflects its deferred action; before descending, the action is composed into children in the declared chronological order.

### Critical invariants

- Length, coordinate domain, half-open interval convention, numeric type, overflow policy, and algebra are explicit.
- Fenwick cells equal aggregates of their declared lowbit intervals; prefix selection requires monotone cumulative values.
- Segment nodes equal the ordered aggregate of their interval after accounting for their lazy tag.
- Identity, associativity, action identity, composition order, distributivity, and interval-length effects are tested.
- Empty ranges return identity; invalid ranges fail before access; padding leaves remain identity.
- Versions, snapshots, serialized roots/nodes, and coordinate maps never mix generations.
- Concurrency claims identify synchronization, linearization points, memory reclamation, and snapshot semantics.

### Common failures

Failures include mixing zero- and one-based formulas, changing ([l,r)) into inclusive endpoints, using prefix subtraction without an inverse, performing Fenwick selection with negative values, reversing lazy-action composition, forgetting segment length for range assignment/sum, reading children before pushing, corrupting padding, overflowing midpoint or aggregate arithmetic, claiming (O(log U)) memory for an implicit tree, retaining unbounded persistent versions, and calling unsynchronized readers “lock-free.”

### Compact example

For `[3,1,4,1,5,9,2,6]`, a Fenwick tree reports prefix `[0,5)` as 14 and range `[2,7)` as 21. Adding 4 at index 3 changes that range to 25; the first zero-based index whose inclusive cumulative sum reaches 15 is 4. A lazy sum tree adds 3 to `[1,6)`, making total 46 and `[2,7)` equal 33. Plain-array oracles reproduce each result.

### Connections

Earlier DSE chapters establish arrays, trees, monoids, persistence, and cache behavior. [DSE-091](091-bit-vectors-with-rank-and-select.md) uses prefix summaries for rank/select. The roadmap successor is [DSE-096, “Merkle Trees”](../ROADMAP.md). Databases, streaming, computational geometry, numerical systems, and concurrency engineering own snapshots, coordinate compression, event time, numeric policy, and multi-reader publication.

## Governing Question

Which algebraic, coordinate, update, query, memory, persistence, and concurrency contracts make a Fenwick or segment structure correct for its production workload, and what evidence distinguishes those contracts from one successful fixture?

## Why This Matters

Range aggregation appears in ledgers, telemetry windows, schedulers, geometric sweeps, ranking, inventory, and online analytics. Recomputing each query from raw values is too slow; rebuilding a static prefix table after every update is also too slow. Fenwick and segment structures occupy useful points between those extremes.

The implementations look short, which makes contract errors dangerous. A loop can pass ordinary sums while mishandling index zero. A lazy tree can return correct full-range totals but stale subranges. A persistent tree can preserve values yet leak every abandoned version. Production readiness therefore joins algebraic proof, boundary testing, numeric policy, memory ownership, and recovery.

## Prerequisites and Retrieval

Retrieve:

- arrays, one- and zero-based indexing, binary representation, least significant set bit, and half-open intervals;
- monoids, groups, identities, associativity, inverses, function composition, and distributive actions;
- recursion/iteration, complete binary-tree layouts, coordinate compression, checked arithmetic, and cache locality;
- point/range update, prefix/range query, order statistics, difference arrays, persistence, and snapshots;
- locks, atomics, linearizability, immutable publication, epochs/hazards, serialization, checksums, and differential testing.

This chapter treats aggregate values as mathematical integers unless a concrete type is named. A real implementation must specify modular, wrapping, saturating, checked, arbitrary-precision, or domain-bounded behavior.

## Learning Objectives

After this chapter, you should be able to:

1. derive Fenwick update/query paths from lowbit interval ownership;
2. state when two-prefix range queries and prefix selection are valid;
3. derive iterative or recursive segment queries from canonical decomposition;
4. specify and test a lazy monoid action, including composition order and segment length;
5. choose dense, implicit, coordinate-compressed, persistent, or concurrent variants by workload;
6. design safe serialization, publication, reclamation, and rebuild behavior;
7. validate results, invariants, asymptotic claims, and full memory/latency curves against plain oracles.

## Core Exposition

### Fenwick interval ownership

Use one-based internal index $i$ and $lowbit(i)=i\mathbin{\&}(-i)$. Cell `tree[i]` owns source interval $(i-lowbit(i),i]$. A prefix query for the first $i$ values accumulates `tree[i]` and assigns $i\leftarrow i-lowbit(i)$ until zero. Each step clears one set bit, so there are at most $\lfloor\log_2n\rfloor+1$ steps; owned intervals are adjacent and disjoint, exactly partitioning the prefix.

A point addition at one-based position (i) updates (tree[i]) and assigns $i\leftarrow i+lowbit(i)$. These are precisely the ancestor intervals containing that position. Linear construction can propagate each initialized cell to its next owner, but a simple repeated-add build costs $O(n\log n)$; the API and benchmark must state which is used.

External zero-based index (p) maps to internal (p+1). Prefix API names should reveal whether the end is exclusive. This chapter uses (prefix(r)=aggregate([0,r))) and (range(l,r)=prefix(r)-prefix(l)) for sums. Empty ([l,l)) returns zero; (r=n) is valid even though point index (n) is not.

### Algebraic limits and prefix selection

Fenwick point updates work for a commutative group in the familiar single-array form; prefix accumulation uses the stored operation. Deriving arbitrary ranges from two prefixes requires an inverse. For sums, subtract; for XOR, XOR again. Minimum lacks an inverse, so general point replacement plus arbitrary range minimum does not follow from the same interface. Specialized monotone-update Fenwick variants exist but have narrower contracts.

Binary lifting over Fenwick cells can find the smallest prefix reaching a target in (O(log n)) without repeated binary-search queries. It relies on cumulative monotonicity, normally nonnegative frequencies. If updates make values negative, a larger prefix can have a smaller sum, invalidating the selection predicate even though ordinary prefix sums remain correct. Define whether the result is an index, prefix length, insertion point, or not-found sentinel.

Range-add/point-query uses a Fenwick tree over a difference array. Range-add/range-sum can use two Fenwick trees and an algebraic formula. These variants change stored meaning and numeric bounds; naming both simply `FenwickTree` invites misuse.

### Segment monoids and canonical decomposition

Let (S) be node-value type, $op:S\times S\to S$ associative, and (e) its identity. Leaves represent elements; internal node value is (op(left,right)). A range query selects disjoint nodes whose intervals cover ([l,r)) and combines them in source order. Commutativity is unnecessary: string concatenation and matrix multiplication work if left/right accumulators preserve order.

A flat iterative tree rounds capacity to a power of two, stores leaves in the second half, and parents above. It offers dense memory, predictable traversal, and easy rebuild. A pointer tree supports sparse allocation or persistence but pays allocation, pointer, metadata, and locality costs. Report logical (n), padded capacity, node count, element size, and allocator overhead.

Point replacement updates one leaf and recomputes ancestors. Point addition is replacement by (old+delta), not a universal segment-tree primitive. Query APIs can also implement boundary searches such as maximum right endpoint satisfying a monotone predicate; the predicate must accept identity and remain monotone under extension.

### Lazy range actions

For range updates, define action type (F), identity (id), mapping $f:S\to S$, and composition. Actions must be closed under composition and compatible with aggregation: applying (f) to a parent aggregate must equal aggregating its effects on children. For range-add/range-sum, node value includes sum and length, and mapping is $(sum,len)\mapsto(sum+delta\cdot len,len)$.

Composition order is semantic. If stored tag (g) represents older pending work and new action (f) arrives, a convention might store $f\circ g$, meaning apply (g) then (f). Assignment followed by addition differs from addition followed by assignment; tests using only additions cannot detect reversal because addition commutes.

When a fully covered node receives an action, update its aggregate immediately and compose its tag. Before partial descent, push the parent tag to both children and reset it to identity. After recursion, pull the parent aggregate from children. The root is always current; descendants may be stale only in the precisely represented way described by ancestor tags.

### Dynamic domains, coordinates, and versions

If coordinates are known offline, sort/deduplicate them and map to dense ranks. This changes interval semantics: a geometric length aggregate needs coordinate gaps, not merely rank counts. If the universe is huge and points arrive online, an implicit segment tree allocates nodes only on visited paths. Time is (O(log U)) for universe size (U), but memory is proportional to allocated nodes, potentially $O(q\log U)$ before sharing or pruning.

Path copying creates a new root and copies (O(log n)) nodes per point update, preserving old roots. This is partial persistence when only the newest version is updated and full persistence when any version can branch. Lazy persistent range updates need careful copying before push/mutation. Version IDs, roots, coordinate maps, and node arenas must publish consistently; retention and garbage collection are part of the design.

### Concurrency and durability

An in-place update touches multiple cells/nodes, so atomic element writes alone do not give an atomic range query. Options include a coarse read/write lock, striped protocols with documented consistency, copy-on-write immutable roots, seqlocks with retry, or specialized concurrent algorithms. State the linearization point and whether queries observe one version or may combine updates.

Immutable roots simplify readers, but old nodes cannot be reclaimed while readers hold them. Reference counting, epochs, hazard pointers, or managed runtimes supply different progress and latency properties. Persistence for historical queries is not the same as safe memory reclamation for concurrent snapshots.

Durable images record schema, algebra/action identifier, numeric policy, (n), capacity/universe, coordinate map digest, node/cell sections, roots/version table, checksums, and generation. Validate lengths, indices, tree shape, padding identity, root aggregates, tag encodings, and checked offset arithmetic before use. Publish a validated immutable generation atomically and never combine its roots with another generation's arena.

### Evaluation and bounded executable evidence

Test empty/singleton/power-of-two/non-power-of-two sizes; every boundary interval; negative and extreme updates; noncommutative operations; noncommuting lazy actions; invalid coordinates; padding; overflow; corrupt tags; allocation exhaustion; abandoned versions; and concurrent publication. Differential randomized sequences compare every operation with a plain array, while structural checks recompute cell ownership and node aggregates.

Benchmark operation mixes and interval lengths, hot/cold locality, selection targets, update skew, sample versions, reader counts, construction, rebuild, allocation, reclamation, serialization, and recovery. Report latency distributions and total owned bytes, not only theoretical nodes.

The finite model below implements sum-specific Fenwick point addition and lazy segment range addition. It demonstrates coordinate and lazy-sum invariants, not a generic library, persistence, concurrency, serialization, overflow control, or production performance.

<!-- bijux-verify: {"id":"fenwick-segment-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"values=[3, 1, 4, 1, 5, 9, 2, 6]\nfenwick_prefix_5=14\nfenwick_range_2_7_before=21\nfenwick_update=(3, 4)\nfenwick_range_2_7_after=25\nfenwick_lower_bound_15=4\nfenwick_oracle=True\nsegment_range_2_7_before=21\nsegment_update=(1, 6, 3)\nsegment_total_after=46\nsegment_range_2_7_after=33\nsegment_root_sum=46\nsegment_oracle=True\nvalid=True\nevidence=bounded_fenwick_segment_model\n","stderr":""}} -->
```python
VALUES = [3, 1, 4, 1, 5, 9, 2, 6]


class Fenwick:
    def __init__(self, values):
        self.n = len(values)
        self.tree = [0] * (self.n + 1)
        for index, value in enumerate(values):
            self.add(index, value)

    def add(self, index, delta):
        cursor = index + 1
        while cursor <= self.n:
            self.tree[cursor] += delta
            cursor += cursor & -cursor

    def prefix(self, end):
        total = 0
        cursor = end
        while cursor:
            total += self.tree[cursor]
            cursor -= cursor & -cursor
        return total

    def range_sum(self, left, right):
        return self.prefix(right) - self.prefix(left)

    def lower_bound(self, target):
        position = 0
        accumulated = 0
        step = 1 << (self.n.bit_length() - 1)
        while step:
            candidate = position + step
            if candidate <= self.n and accumulated + self.tree[candidate] < target:
                position = candidate
                accumulated += self.tree[candidate]
            step >>= 1
        return position


class LazySumTree:
    def __init__(self, values):
        self.n = len(values)
        self.sums = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        self._build(1, 0, self.n, values)

    def _build(self, node, left, right, values):
        if right - left == 1:
            self.sums[node] = values[left]
            return
        middle = left + (right - left) // 2
        self._build(node * 2, left, middle, values)
        self._build(node * 2 + 1, middle, right, values)
        self.sums[node] = self.sums[node * 2] + self.sums[node * 2 + 1]

    def _apply(self, node, left, right, delta):
        self.sums[node] += delta * (right - left)
        self.lazy[node] += delta

    def _push(self, node, left, right):
        if self.lazy[node] == 0 or right - left == 1:
            return
        middle = left + (right - left) // 2
        self._apply(node * 2, left, middle, self.lazy[node])
        self._apply(node * 2 + 1, middle, right, self.lazy[node])
        self.lazy[node] = 0

    def add(self, query_left, query_right, delta, node=1, left=0, right=None):
        right = self.n if right is None else right
        if query_right <= left or right <= query_left:
            return
        if query_left <= left and right <= query_right:
            self._apply(node, left, right, delta)
            return
        self._push(node, left, right)
        middle = left + (right - left) // 2
        self.add(query_left, query_right, delta, node * 2, left, middle)
        self.add(query_left, query_right, delta, node * 2 + 1, middle, right)
        self.sums[node] = self.sums[node * 2] + self.sums[node * 2 + 1]

    def range_sum(self, query_left, query_right, node=1, left=0, right=None):
        right = self.n if right is None else right
        if query_right <= left or right <= query_left:
            return 0
        if query_left <= left and right <= query_right:
            return self.sums[node]
        self._push(node, left, right)
        middle = left + (right - left) // 2
        return (
            self.range_sum(query_left, query_right, node * 2, left, middle)
            + self.range_sum(query_left, query_right, node * 2 + 1, middle, right)
        )


fenwick_oracle = VALUES.copy()
fenwick = Fenwick(VALUES)
fenwick_prefix_5 = fenwick.prefix(5)
fenwick_before = fenwick.range_sum(2, 7)
fenwick.add(3, 4)
fenwick_oracle[3] += 4
fenwick_after = fenwick.range_sum(2, 7)
fenwick_valid = all(
    fenwick.range_sum(left, right) == sum(fenwick_oracle[left:right])
    for left in range(len(VALUES) + 1)
    for right in range(left, len(VALUES) + 1)
)

segment_oracle = VALUES.copy()
segment = LazySumTree(VALUES)
segment_before = segment.range_sum(2, 7)
segment.add(1, 6, 3)
for index in range(1, 6):
    segment_oracle[index] += 3
segment_after = segment.range_sum(2, 7)
segment_valid = all(
    segment.range_sum(left, right) == sum(segment_oracle[left:right])
    for left in range(len(VALUES) + 1)
    for right in range(left, len(VALUES) + 1)
)

print(f"values={VALUES}")
print(f"fenwick_prefix_5={fenwick_prefix_5}")
print(f"fenwick_range_2_7_before={fenwick_before}")
print("fenwick_update=(3, 4)")
print(f"fenwick_range_2_7_after={fenwick_after}")
print(f"fenwick_lower_bound_15={fenwick.lower_bound(15)}")
print(f"fenwick_oracle={fenwick_valid}")
print(f"segment_range_2_7_before={segment_before}")
print("segment_update=(1, 6, 3)")
print(f"segment_total_after={segment.range_sum(0, len(VALUES))}")
print(f"segment_range_2_7_after={segment_after}")
print(f"segment_root_sum={segment.sums[1]}")
print(f"segment_oracle={segment_valid}")
print(f"valid={fenwick_valid and segment_valid}")
print("evidence=bounded_fenwick_segment_model")
```

Every displayed pre-update observation is captured before mutation. The exhaustive interval comparisons run after each structure's update and establish all half-open range sums for this fixture; they do not establish a generic algebra or performance bound.

## Definitions and Notation

- (A[0..n)) is the logical value sequence; all public ranges are half-open ([l,r)).
- $lowbit(i)=i\mathbin{\&}(-i)$ for positive one-based integer (i).
- A Fenwick cell at (i) owns ((i-lowbit(i),i]) in one-based coordinates.
- (prefix(r)) aggregates (A[0..r)); a sum range is (prefix(r)-prefix(l)).
- A **monoid** ((S,op,e)) has associative operation (op) and identity (e); a **group** additionally has inverses.
- A segment-tree **canonical interval** is the source interval owned by one selected query node.
- (F) is a family of update actions with identity (id), mapping onto (S), and a declared composition order.
- A **lazy tag** represents deferred action already reflected in the node aggregate but not necessarily its descendants.
- A **dense tree** allocates a fixed array for all nodes; an **implicit tree** allocates visited universe paths on demand.
- **Ephemeral**, **partially persistent**, and **fully persistent** distinguish destroyed history, newest-only updates with historical queries, and branching updates to any version.
- A **linearization point** is the instant at which a concurrent operation takes effect in the abstract history.
- A **generation** is one immutable, mutually consistent set of cells/nodes, coordinate metadata, roots, and schema.

## Mechanisms, Invariants, or Proof Structure

### Fenwick partition proof

For positive (i), subtracting (lowbit(i)) clears its least significant set bit. The interval owned before that subtraction ends exactly where the next interval begins. The decreasing indices terminate after at most the bit width of (i), and their disjoint union is ((0,i]). Point update follows the inverse ancestor relation by adding lowbit, touching every and only owned interval containing the point.

### Segment decomposition proof

A recursive query either accepts a fully covered node, rejects a disjoint node, or divides at a midpoint. Accepted leaves of this recursion are disjoint and cover exactly ([l,r)). Folding them in source order equals folding the underlying elements because associativity permits regrouping. Identity handles rejected and empty pieces. Without associativity, tree shape can change the answer; without ordered folding, a noncommutative monoid can change it.

### Lazy action proof obligation

For every action (f) and aggregate values (x,y), mapping must satisfy (mapping(f,op(x,y))=op(mapping(f,x),mapping(f,y))) under whatever length metadata is part of (x,y). Composition must satisfy (mapping(compose(f,g),x)=mapping(f,mapping(g,x))) for the declared order. Push preserves the represented array by transferring the parent action to both child representations; pull then restores the parent aggregate.

### Persistence and publication

Path copying leaves every node reachable from an old root unchanged. A new root points to copied path nodes and shares untouched subtrees, so an update allocates tree-height nodes for a point operation. This is a semantic persistence argument, not a reclamation proof. Durable or concurrent publication additionally requires atomic root/generation visibility and lifetime protection for all nodes reachable by readers.

### Evidence ladder

The bounded model checks every interval after deterministic updates. Stronger evidence adds exhaustive small arrays/operation sequences, algebra law tests, a separately implemented oracle, property-based noncommuting actions, sanitizer runs, allocation-failure injection, corrupt-image tests, model-checked concurrent histories where feasible, and measured build/memory/latency curves. Passing sum tests cannot validate generic monoid/action parameters.

## Alternatives and Trade-Offs

**Static prefix tables.** Build in linear time, answer sums in constant time, and offer excellent locality. Any value change requires repair or rebuild, so they fit immutable batches and snapshot generations.

**Fenwick trees.** Compact, iterative, and cache-friendly for prefix/group workloads. They usually use (O(n)) cells with small constants and support point update/prefix query in (O(log n)). Their implicit hierarchy is less flexible for arbitrary monoids, range actions, and structural augmentation.

**Dense segment trees.** Support general monoids, ordered aggregation, boundary searches, and lazy range actions. They use more memory and code; flat layouts improve locality. Choose them when the needed algebra exceeds the Fenwick contract.

**Sqrt/block decomposition.** Partition values into blocks with summaries. It is often easier to update, vectorize, and tune for skewed mixes, trading query/update bounds near $O(\sqrt n)$ or workload-specific variants for smaller engineering risk.

**Balanced search trees and augmented B-trees.** When coordinates are inserted/deleted online or durable storage matters, ordered trees with subtree aggregates may match the domain better. They provide navigation and external-memory page ownership absent from dense index trees.

**Difference arrays and offline sweeps.** Batched range additions followed by one materialization can be linear and simpler. Offline coordinate compression and sweep-line event ordering may eliminate the need for an online implicit tree.

**Persistent trees.** Path copying provides cheap immutable snapshots and historical queries, at allocation and retention cost. It is attractive for MVCC-like reads but does not by itself provide durable transactions, conflict resolution, or bounded memory.

**Domain-specific structures.** Sparse tables serve immutable idempotent queries; disjoint sparse tables serve immutable associative queries; interval trees own interval stabbing; link-cut trees own dynamic forest paths; sketches own approximate streams. A segment tree is not the universal answer to every “range” problem.

## Failure Modes and Misconceptions

1. **Index-base mismatch:** zero-based external indices are passed directly into one-based lowbit loops, causing an infinite loop or skipped value.
2. **Endpoint drift:** documentation says ([l,r)) while implementation or caller uses inclusive (r).
3. **Missing inverse:** two-prefix subtraction is applied to minimum, string concatenation, or another non-group operation.
4. **Invalid selection:** Fenwick lower-bound is used after negative updates destroy prefix monotonicity.
5. **Order loss:** iterative segment query combines right fragments in reverse order for a noncommutative monoid.
6. **Wrong identity:** padding or empty ranges use zero when the operation requires infinity, one, an empty string, or another identity.
7. **Reversed composition:** new and old lazy actions are composed in the wrong chronological order.
8. **Lost length:** range-add/range-sum updates a node by delta rather than delta times segment length.
9. **Stale descent:** a query descends beneath a tagged node without pushing or carrying the deferred action.
10. **Pull corruption:** a fully covered update changes children but fails to restore the parent, or changes parent without preserving tag semantics.
11. **Midpoint overflow:** ((l+r)/2) overflows a fixed-width coordinate; use (l+(r-l)/2) with checked bounds.
12. **Padding exposure:** queries enter padded leaves or padding is initialized with a nonidentity value.
13. **Sparse-memory overclaim:** (O(log U)) update time is reported as total memory despite accumulating nodes across operations.
14. **Coordinate compression error:** rank distance is mistaken for geometric or temporal distance.
15. **Version leakage:** every persistent root remains retained without quotas, reachability accounting, or collection.
16. **Generation mixing:** a root is loaded with a different node arena, coordinate map, or algebra schema.
17. **False atomicity:** per-cell atomics are assumed to make a multi-cell update/query linearizable.
18. **Unsafe reclamation:** an immutable root is swapped while readers can still dereference freed old nodes.
19. **Space undercounting:** padding, tags, pointers, arenas, versions, maps, allocator fragmentation, and rebuild copies are omitted.
20. **Fixture generalization:** passing range-add/sum is treated as validating assignments, affine maps, matrices, or arbitrary user callbacks.

## Worked Examples

### Example 1

For one-based Fenwick index 6 (`110` in binary), (lowbit(6)=2), so cell 6 owns positions ((4,6]), corresponding to zero-based values 4 and 5. Prefix 6 visits cells 6 then 4; their intervals ((4,6]) and ((0,4]) partition the first six values.

### Example 2

Adding at zero-based index 3 starts at one-based 4. The update visits cell 4 then 8 for an eight-element array. Both owned intervals contain position 4; no other Fenwick cell needs change. Starting at external index zero correctly maps to internal one, avoiding (lowbit(0)=0).

### Example 3

With nonnegative values `[3,1,4,5,5,9,2,6]`, cumulative sums are `[3,4,8,13,18,27,29,35]`. The first inclusive cumulative sum at least 15 is zero-based index 4. If index 1 changed by -10, cumulative sums would cease to be monotone and binary lifting would no longer implement this predicate.

### Example 4

For string values `a,b,c,d,e`, a segment query ([1,4)) must return `bcd`. An iterative implementation can accumulate left fragments by appending and right fragments by *prepending*. Combining all fragments as if concatenation commuted could return `bdc` or another wrong ordering.

### Example 5

In a sum tree for eight values, ([2,7)) decomposes into canonical nodes such as ([2,4)), ([4,6)), and ([6,7)), depending on layout. Their disjoint union is exact; no source element is counted twice. Associativity makes `(4+1)+(5+9)+2` equal 21.

### Example 6

A range-add action (+3) on five elements increases the stored sum by $3\cdot5=15$, not 3. Applying it to ([1,6)) changes total 31 to 46. The node value therefore needs interval length directly or from traversal boundaries.

### Example 7

Consider actions “assign 7” and then “add 2.” Their composition produces 9 for every affected value. Reversing them produces assignment 7. A law test with only two additions cannot reveal composition reversal; a noncommuting fixture is mandatory for a generic lazy library.

### Example 8

Coordinates `{10,20,1000}` compress to ranks `{0,1,2}`. Counting points over rank intervals is valid. Computing covered geometric length as three equal leaf widths is invalid: gaps are 10 and 980. Store elementary interval lengths derived from original coordinates.

### Example 9

An implicit tree over ([0,2^60)) visits at most 60 levels per point update, but one million unrelated updates can allocate tens of millions of nodes. The universe bound controls height, not retained memory. Pruning zero subtrees may help only when update semantics permit it.

### Example 10

Path-copying a point update creates a new root and copies its root-to-leaf path. A concurrent reader holding the old root sees a consistent snapshot, provided the old arena remains alive. Atomic root exchange supplies publication; epoch or reference lifetime supplies safe reclamation. Neither implies durable recovery after a crash.

## Cross-Program Connections

- **Algorithms:** binary representation, monoids, persistence, canonical decompositions, and amortized allocation supply correctness and bounds.
- **Database Engineering:** materialized aggregates, MVCC roots, write-ahead publication, checksums, rebuilds, and recovery govern durable use.
- **Data Engineering:** event-time windows, late data, coordinate dictionaries, replay, and batch/stream consistency define update semantics.
- **Concurrent and Parallel Programming:** snapshot publication, locks, seqlocks, atomics, memory ordering, and reclamation define observable histories.
- **Computational Geometry:** sweep lines, coordinate gaps, interval coverage, and dynamic endpoints motivate augmented segment structures.
- **Numerical Computing:** overflow, floating-point nonassociativity, deterministic reduction order, and error bounds constrain the algebra.
- **Security Engineering:** input bounds, checked allocation, malicious serialized images, denial-of-service ranges, and callback isolation constrain APIs.
- **Performance Engineering:** dense locality, branch behavior, vectorization, allocator cost, NUMA placement, and operation mix determine the useful variant.

## References

1. Peter M. Fenwick, [“A New Data Structure for Cumulative Frequency Tables”](https://dblp.org/rec/journals/spe/Fenwick94.html), *Software: Practice and Experience*, 1994. Stable bibliographic record for the original binary indexed tree paper and cumulative-frequency motivation.
2. Peter M. Fenwick, [“A New Data Structure for Cumulative Probability Tables”](https://www.cs.auckland.ac.nz/~peter-f/FTPfiles/TechRep88.pdf), University of Auckland technical report. Author-hosted precursor with the binary decomposition.
3. AtCoder, [Fenwick Tree](https://atcoder.github.io/ac-library/production/document_en/fenwicktree.html), official AC Library documentation. Concrete point-add and half-open range-sum contract.
4. AtCoder, [Segtree](https://atcoder.github.io/ac-library/production/document_en/segtree.html), official AC Library documentation. Monoid requirements, queries, updates, and boundary searches.
5. AtCoder, [Lazy Segtree](https://atcoder.github.io/ac-library/production/document_en/lazysegtree.html), official AC Library documentation. Monoid action, mapping, composition, and range operations.
6. AtCoder, [AC Library Appendix](https://atcoder.github.io/ac-library/production/document_en/appendix.html), official documentation. Precise finite-representation and overflow requirements for segment structures.
7. James R. Driscoll, Neil Sarnak, Daniel D. Sleator, and Robert E. Tarjan, [“Making Data Structures Persistent”](https://www.cs.cmu.edu/~sleator/papers/making-data-structures-persistent.pdf), *Journal of Computer and System Sciences*, 1989. Primary persistence techniques and terminology.

## Exercises

### Exercise 1

For values `[2,7,1,8,2,8,1,8]`, construct the one-based Fenwick cell array by repeated point addition. Show the cells visited by (prefix(7)), compute range ([2,7)), then add 3 at zero-based index 4 and recompute that range.

### Exercise 2

Prove the Fenwick prefix partition and logarithmic step bound. Then state exact algebraic assumptions for point-add/prefix, arbitrary range from two prefixes, and prefix lower-bound selection.

### Exercise 3

Design a lazy segment algebra supporting range affine updates $x\mapsto ax+b$ and range sums. Define node type, identity, mapping, action identity, chronological composition, and law tests that catch reversed composition.

### Exercise 4

Design a partially persistent implicit segment tree over unsigned 64-bit coordinates with point additions and range sums. Specify node/path bounds, overflow checks, root/version publication, retention, reclamation, serialization, and recovery.

### Exercise 5

Design a benchmark and correctness campaign choosing among a static prefix array, two-Fenwick range-add/range-sum structure, dense lazy segment tree, and augmented persistent search tree for a telemetry service with late corrections and snapshot reads.

## Answers to the Exercises

### Answer 1

Repeated additions produce cells `[0,2,9,1,18,2,10,1,37]`, including unused cell zero. Prefix 7 visits one-based cells 7, 6, and 4, totaling (1+10+18=29). Prefix 2 is 9, so ([2,7)) is 20. Adding 3 at zero-based index 4 visits one-based cells 5, 6, and 8; cells become `[0,2,9,1,18,5,13,1,40]`. The queried range includes index 4 and becomes 23.

### Answer 2

At positive (i), lowbit is the size of the owned suffix ending at (i). Subtracting it reaches the preceding boundary, so successive owned intervals are adjacent/disjoint and terminate at zero. Each subtraction clears one set bit, bounding steps by bit width. The standard point-update/prefix representation assumes an operation compatible with accumulating and updating the stored partial aggregates, commonly a commutative group for arbitrary deltas. Deriving ([l,r)) from two prefixes requires an inverse and correct order; sums subtract and XOR self-inverts. Prefix lower-bound additionally requires a monotone predicate, normally nonnegative frequency values and a clearly defined target/not-found contract.

### Answer 3

Store node `(sum,length)` with `op((s1,n1),(s2,n2))=(s1+s2,n1+n2)` and identity `(0,0)`. Action `(a,b)` maps `(s,n)` to `(a*s+b*n,n)`; identity is `(1,0)`. If older action `(a1,b1)` runs before newer `(a2,b2)`, composition is `(a2*a1, a2*b1+b2)`. Check identity, associativity of node op, action identity, closure within numeric policy, distributivity, and mapping(composition(new,old),x)=mapping(new,mapping(old,x)). A fixture “assign-like” `(0,7)` followed by add `(1,2)` must yield 9, while reversed order yields 7, detecting composition reversal.

### Answer 4

Use root interval ([0,2^64)) represented without overflowing the right endpoint—for example, a 65-bit/big-integer bound or `(prefix,length)` representation. A point update copies/allocates at most 64 path nodes and uses checked aggregate addition; absent children represent zero. Each committed version binds ID, parent, root offset, arena generation, coordinate/numeric schema, and checksum. Append nodes and version record, validate reachable bounds/root sum, flush per durability contract, then atomically publish the version table head. Readers pin a generation/root; retention quotas preserve required versions, and reachability/epoch rules reclaim only nodes unreachable by every retained or active root. Recovery scans validated committed records and ignores incomplete tails; it never combines root offsets with another arena generation.

### Answer 5

Replay deterministic production-like traces with varied (n), correction rate, interval length, snapshot age, reader count, skew, negative/extreme values, and restart points. Compare every operation with immutable plain-array snapshots using checked or arbitrary-precision arithmetic. Measure build/rebuild, point/range update, range query, snapshot creation/read, recovery, p50/p95/p99 latency, throughput, peak/final owned bytes, allocation/reclamation, write amplification, and stale-version retention. Static prefixes win for immutable batches; two Fenwick trees for sum-specific dense corrections with no broad action algebra; dense lazy trees for frequent range updates on fixed coordinates; augmented persistent search trees when online coordinate changes and historical snapshots justify pointer/allocator costs. Select against explicit service limits and verified semantics, not asymptotic notation alone.
