---
module_id: DSE-038
program: Data Structures Engineering
level: 1
module_number: 38
title: Binary and d-Ary Heaps
status: complete
last_verified: 2026-08-30
---

# Binary and d-Ary Heaps

## One-Page Review

### Governing question

How can an engineer derive, implement, and validate an array-backed binary or d-ary heap whose ordering, stability, mutation, failure, and performance contracts are explicit?

### Essential definitions

- A **priority queue** is an abstract data type that retrieves an item of extremal priority; a heap is one possible representation.
- A **d-ary heap** is a complete rooted tree with at most `d` children per node and heap order between every parent and child.
- In a zero-based array, `parent(i)=floor((i-1)/d)` for `i>0`, and child `j` of `i` is `d*i+j` for `1<=j<=d` when that index is below the logical length.
- A **min-heap** satisfies `key(parent)<=key(child)`; a max-heap reverses the relation.
- **sift up** repairs one possible parent violation after append or priority decrease in a min-heap.
- **sift down** repairs one possible child violation after root replacement, arbitrary removal, or bottom-up construction.
- **heapify** applies sift down to internal nodes from right to left and builds a heap in `O(n)` time.
- A **stable priority policy** returns equal-priority items in arrival order, commonly by comparing `(priority, sequence)`.
- A **handle** identifies a live entry so its priority can be changed or the entry removed without an `O(n)` search.

### Central model, mechanism, or theorem

The array length enforces complete-tree shape; only local heap order must be maintained. Appending creates one possible upward violation, so sift up follows one ancestor path. Removing the root moves the last entry to index zero, creating one possible downward violation, so sift down repeatedly selects the best child. These operations visit `O(log_d n)` levels, but a straightforward sift down may compare up to `d` children per level and therefore costs `O(d log_d n)` comparisons.

Bottom-up heapify is linear, not `O(n log n)`: most nodes are near the leaves and can descend only a few levels. Bounding the number of nodes of height at least `h` by `n/d^h` gives a work sum proportional to `n * sum(h/d^h)`, which converges for fixed `d>=2`.

### Critical invariants

1. `d>=2`, logical length and capacity are valid, and index arithmetic cannot overflow.
2. Array positions `0..n)` form the unique complete-tree shape with no holes.
3. Every nonroot entry has a valid parent whose key is no worse under the declared strict ordering.
4. Sift up/down move the hole or displaced entry along one path; all off-path edges remain ordered.
5. Equal-key policy is explicit; stability requires a unique, nonwrapping tie-break key or a defined renumbering scheme.
6. A mutable heap maintains both directions of its mapping: `position[handle]` points to the entry, and the entry at that index carries that handle.
7. Mutating an ordering field outside the heap API is forbidden or detected before subsequent results are trusted.
8. Publication, cancellation, ownership, exception safety, and concurrency semantics cover the whole logical operation, not individual swaps.

### Common failures

- Treating the backing array or its iterator as sorted.
- Calling bottom-up heapify `O(n log n)` because each isolated sift has that upper bound.
- Increasing `d` and counting only reduced height while ignoring child scans.
- Reversing a comparator twice and returning the wrong extremum.
- Expecting equal priorities to be stable without a sequence key.
- Changing a key in place without repair, or repairing in the wrong direction.
- Keeping an index as a durable handle while swaps and reallocations move entries.
- Implementing `push-pop` and `replace-root` as if they had identical boundary semantics.
- Assuming standard-library priority queues expose ordered iteration or thread safety.
- Using a successful small trace as proof that one arity wins on all workloads.

### Compact example

Nine arrivals with priorities `5,3,7,1,3,2,6,1,4` heapify to `D` at the root for both `d=2` and `d=4`. Comparing `(priority,arrival_sequence)` makes the extraction order `D,H,F,B,E,I,A,G,C`. The binary representation has four occupied levels and the 4-ary representation three; the finite trace uses 14 versus 8 comparisons to heapify, but that instance does not prove a general winner.

### Connections

[DSE-004](004-time-space-and-allocation-cost.md), [DSE-006](006-memory-locality-and-cache-behavior.md), and [DSE-009](009-property-based-testing-of-data-structures.md) supply cost, locality, and evidence models. [DSE-037](037-fenwick-interval-and-segment-trees.md) contrasts another family of implicit array trees. The [program roadmap](../ROADMAP.md) continues with indexed and meldable priority queues, skip lists, tries, and disjoint sets.

## Governing Question

Which abstract priority semantics, array mapping, local repair proof, arity, tie policy, handle design, numeric boundary, ownership rule, and workload evidence justify a binary or d-ary heap in a real system?

## Why This Matters

Priority queues sit inside schedulers, shortest-path and graph-search algorithms, event simulation, top-k analytics, timer systems, merge pipelines, memory managers, compression, external sorting, and storage engines. The textbook heap is small, yet production behavior depends on choices textbooks often suppress: whether a lower number means higher urgency, whether ties are stable, whether keys may change, what a handle owns, how cancellation works, which failures leave the object usable, and whether one global root becomes a concurrency bottleneck.

A heap is not synonymous with a priority queue. The abstract data type promises operations and observable ordering; the heap is a representation that exploits a partial order. A sorted array, balanced tree, calendar queue, bucket structure, skip list, pairing heap, or concurrent relaxed queue can implement a related interface with different guarantees. Conversely, the same array heap can support a scheduler, heapsort, selection, or a bounded top-k filter under different policies.

The engineering lesson is unusually transferable. The array formulas illustrate representation derivation. Sift operations illustrate local invariant restoration. Bottom-up construction illustrates aggregate analysis: assigning the worst cost to every item gives the wrong bound. Arity illustrates that asymptotic height alone does not predict comparisons, cache behavior, or tail latency. Stable ties and mutable handles illustrate how an apparently small API promise changes representation and proof obligations.

## Prerequisites and Retrieval

Retrieve abstract/concrete representation distinctions from [DSE-001](001-abstract-data-types-and-concrete-representations.md), invariants and validators from [DSE-002](002-representation-invariants.md), and time/space/allocation models from [DSE-004](004-time-space-and-allocation-cost.md). Retrieve contiguous layout and cache effects from [DSE-005](005-contiguous-and-linked-layouts.md) and [DSE-006](006-memory-locality-and-cache-behavior.md), generic ordering contracts from [DSE-007](007-genericity-and-type-constraints.md), and testing/benchmark discipline from [DSE-009](009-property-based-testing-of-data-structures.md) and [DSE-010](010-benchmarking-a-structure-without-misleading-results.md). Dynamic arrays in [DSE-012](012-dynamic-arrays-and-geometric-growth.md) supply capacity, reallocation, and failure boundaries.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish a priority-queue contract, a heap representation, and the heapsort client;
2. derive zero- and one-based parent/child formulas for arbitrary fixed arity;
3. state complete-tree shape and local heap-order invariants precisely;
4. prove sift-up and sift-down correctness using a path-local violation argument;
5. prove fixed-arity bottom-up heap construction takes linear time;
6. analyze arity using height, comparisons, swaps, locality, key updates, and workload mix;
7. specify equal-priority stability and comparator requirements without accidental payload comparison;
8. design arbitrary removal and priority mutation with validated, lifetime-safe handles;
9. compare current Python, C++, Rust, Java, Go, and Boost heap contracts without assuming semantic parity;
10. create oracle, invariant, exhaustive, fault, concurrency, security, and benchmark evidence without overstating a finite experiment.

## Core Exposition

**Start with the abstract contract.** Let an entry contain a payload, a priority key, and possibly metadata. A min-priority queue returns an entry whose key is minimal under a declared ordering; a max-priority queue returns a maximal key. `peek` observes that entry, `push` inserts, and `pop` removes and returns it. Define behavior on empty queues. Define whether duplicates are permitted, whether equal keys have an observable order, and whether iteration promises priority order. Define whether clients may remove arbitrary entries or change priorities.

The word “priority” is a policy name, not a mathematical direction. A scheduler may assign priority 100 to urgent work while a shortest-path algorithm treats distance 0 as best. Avoid ambiguous comparator prose such as “returns true if higher.” State an ordering relation and root condition: for a min-heap, `less(a,b)` means `a` precedes `b`, and no child precedes its parent. A comparator must behave as a strict weak ordering: irreflexive, transitive, and transitive in its induced equivalence. Time-dependent, random, stateful, or inconsistent comparison destroys the proof.

**A d-ary heap has two independent invariants.** Shape says the conceptual tree is complete: every level before the last is full, and the last is filled left to right. Order says every parent is at least as preferred as each child. A contiguous array makes shape implicit. Positions `0..n)` exist and no others do; append and removal of the last position preserve completeness. The implementation therefore repairs only order.

For zero-based index `i>0`, derive the parent by observing that the children of parent `p` occupy `d*p+1` through `d*p+d`. Solving `d*p+1<=i<=d*p+d` gives `p=floor((i-1)/d)`. Child number `j` in `1..d` is `d*i+j`, provided it is less than `n`. A node is a leaf when its first child `d*i+1` is outside the array. For nonempty `n`, the last internal node is `floor((n-2)/d)`.

One-based arrays use different formulas. With root 1, child `j` can be written `d*(i-1)+j+1`, and the parent requires corresponding adjustment. Mixing a one-based parent formula with a zero-based child formula may pass tiny cases and fail near arity boundaries. Derive formulas from the chosen coordinate system and test around `d*k`, `d*k+1`, and the final partial sibling group.

Index arithmetic is part of correctness. Computing `d*i+j` can overflow a fixed unsigned type and wrap into a valid-looking smaller position. Test `i>(MAX-j)/d` or structure loops so `first<n` is established using checked arithmetic. Capacity growth, byte multiplication, and iterator differences need the same care. An addressable array also imposes a practical maximum below the integer maximum.

**Sift up repairs the append boundary.** Append a new entry at index `n`. The old heap remains valid. The new leaf has no children, so the only possible violation is its edge to the parent. Compare it with the parent. If it does not precede the parent, the heap is valid. Otherwise swap them and repeat at the parent position.

The loop invariant is that every edge is ordered except possibly the edge from the moving entry to its current parent. Before a swap, the moving entry precedes the parent. After the swap, the demoted parent remains no worse than the moving entry's former children: those children were previously below that parent, and the moving entry was a leaf or had inherited a subtree whose roots were no better than the old parent. Off-path subtrees never change. Reaching the root or an ordered parent terminates after at most the heap height.

An efficient implementation may use a **hole** rather than swapping at every level: save the inserted entry, copy parents downward while they are worse, then write the saved entry once. This reduces element moves for large records. It changes exception and ownership analysis because partially moved elements exist during repair. Store indirect pointers or compact records when payload moves are expensive, but count the extra indirection and allocation.

**Sift down repairs root replacement.** To pop, save the root, remove the last entry, place that entry at root if any remain, and repair downward. At a node, find the most preferred existing child. If the displaced entry is no worse than that child, all its child edges are ordered and repair stops. Otherwise promote the best child and continue in that child's former position.

The choice of best child is essential. Swapping with merely the first violating child can leave a better sibling below a worse parent. The loop invariant says all off-path edges are ordered, the displaced entry may violate only edges to its children, and the promoted child's subtree remains ordered. When repair stops, every edge is valid. In a d-ary heap, finding the best child takes up to `d-1` comparisons and comparing it with the displaced entry takes another; the number of levels is about `log_d n`.

Arbitrary removal at index `i` replaces that entry with the last. The replacement may be better than its parent or worse than one of its children. Compare with the parent first: if it precedes the parent, sift up; otherwise sift down. Always sifting down silently fails when the last entry must rise. Priority decrease in a min-heap normally sifts up; priority increase normally sifts down. If the API accepts an arbitrary replacement key, choose direction from local relations rather than trusting the caller's label.

**Bottom-up heapify exploits heterogeneous heights.** Every leaf is already a heap. Starting at the last internal node and moving backward, sift each entry down. When index `i` is processed, all child subtrees begin at larger indices and have already been heapified. Sift down makes the subtree rooted at `i` a heap without disturbing their internal order. Induction moving toward index zero proves the whole array.

Calling each sift `O(log n)` gives a valid but loose `O(n log n)` upper bound. A tight bound charges work by height. At most `n/d^h` nodes have height at least `h`. For constant arity, the total number of level descents is bounded by `n * sum_{h>=1}(1/d^h)=O(n)`; counting per-height work more precisely uses `sum(h/d^h)`, also convergent. Each d-ary level scans at most `d` children, so fixed `d` still gives `O(n)` comparisons. If `d` itself grows with `n`, retain the `d` factor rather than hiding it as a constant.

Top-down construction inserts entries one at a time and costs `O(n log n)` in the worst case. It is appropriate for an online stream. Bottom-up construction requires all entries but is asymptotically and usually practically better for a batch. This distinction descends from the original heapsort/treesort development and remains visible in standard libraries that expose linear-time `heapify`, `make_heap`, `Init`, or vector conversion.

**Arity is a workload and machine parameter.** Increasing `d` lowers height: a complete d-ary heap has `Theta(log_d n)` levels. That can reduce swaps and can help operations dominated by upward motion, such as `decrease-key` in a min-heap. Downward motion must inspect more children. A simple pop therefore performs roughly `d*log_d n` key comparisons; this expression is not monotonically improved by large `d`.

Contiguous siblings may share cache lines and allow branchless or vectorized minimum selection. A smaller height reduces dependent loads. Conversely, large keys or indirect comparators make a wide sibling scan expensive; a high arity can pull more cache lines, and a comparator with unpredictable branches can dominate. The best `d` differs for push-heavy, pop-heavy, decrease-key-heavy, and batch-heapify workloads. Binary and 4-ary heaps are common design points, not universal optima.

Measure comparison count, element bytes moved, allocations, cache misses, branch misses, and latency distribution separately. Benchmark realistic priority distributions: random keys, monotone arrivals, many ties, nearly ordered inputs, adversarial alternation, and graph-derived updates. Vary `n` across cache and capacity boundaries. Warm-up, compiler optimization, allocator state, and frequency scaling belong in the record. Do not tune `d` on the test set and report the same data as independent evidence.

**Heap order is partial, not sorted order.** The root is extremal because every root-to-node path is ordered. Siblings and nodes in different subtrees have no required relation. Iterating the backing array exposes a valid heap layout, not extraction order. Finding an arbitrary value can require scanning all `n` entries. Sorting a copied heap array is a separate operation.

Heapsort builds a max-heap, repeatedly swaps the root with the last unsorted position, shrinks the heap boundary, and sifts down. It sorts in place with `O(n log n)` comparisons and `O(1)` auxiliary element storage under an array implementation. Ordinary heapsort is not stable: root/end swaps can reverse equal keys. A min-heap analog naturally emits ascending items by repeated extraction into separate output, but that is no longer the same in-place arrangement.

**Equal priorities require policy.** A plain heap may return any representative among comparator-equivalent entries. Stability is an additional contract. Store `(priority,sequence,payload)` and compare only the first two fields. A monotonically increasing sequence preserves arrival order for a min-heap; reverse or adjusted direction is needed for a max-heap depending on the comparator.

The sequence is not “just an integer.” Its width, wrap behavior, persistence, and reuse define correctness. Wrap can make a newer entry appear older or create duplicate comparison keys. Options include rejecting insertion at exhaustion, using a wider counter with a proved lifetime bound, or pausing to renumber all live entries in current stable order. Distributed producers need a global policy; local counters alone do not define cross-producer arrival order. Never fall through to payload comparison merely because two priorities tie: payloads may be unorderable, expensive, secret-dependent, or semantically irrelevant.

**Mutable priorities require identity.** If a client presents only a payload, finding it is `O(n)` unless a separate map exists. An indexed heap associates each live entry with a unique handle and maintains a position map. Every swap must update both affected handle positions. Validation checks `position[entry.handle]==index` for every entry and `entries[position[h]].handle==h` for every live handle.

Raw array indices are not durable handles because every repair moves entries. Direct pointers into a dynamic array are invalidated by reallocation and still do not identify the current index after swaps. Use opaque IDs with generations, stable entry objects referenced from the array, or another lifetime-safe scheme. On removal, invalidate the handle before it can alias a later entry. A generation counter also needs an exhaustion policy.

The next module develops indexed and meldable priority queues in depth. The boundary here is important: a binary or d-ary heap can support handles, but the additional map, swap callbacks, ownership, and failure modes are not free consequences of heap order.

**Operation names hide boundary differences.** A `replace-root(x)` operation removes and returns the current root, then installs `x` and repairs, keeping size constant; it requires a nonempty heap. A `push-pop(x)` conceptually inserts `x` and returns the best of the enlarged set, also keeping the original size. If `x` itself is best, push-pop may return it without changing the heap, whereas replace-root must return the old root and keep `x`. Python's `heappushpop` and `heapreplace` document this distinction. Define behavior before optimizing the combined path.

Bulk insertion can mean repeated push or append-plus-heapify. Their complexity and exception boundaries differ. Meld means combining two queues; concatenating arrays and heapifying is linear in total size and may be acceptable for occasional batches, but does not provide the asymptotic meld guarantees of binomial, Fibonacci, pairing, or specialized heaps.

**Current libraries expose materially different contracts.** Python's `heapq` treats a list as a zero-based min-heap, uses only `<`, exposes linear-time `heapify`, and documents a three-field stable priority-queue pattern plus lazy deletion for updates. Python 3.14 added public max-heap counterparts; code targeting older runtimes must not assume they exist. The list is visible, so callers can corrupt the invariant by mutation.

C++ `std::priority_queue` is a container adaptor whose default top is the largest element; its `Compare` direction is a frequent source of double reversal. Its narrow adaptor API protects the underlying heap from ordinary direct mutation but does not provide arbitrary removal or key repair. Current standard wording requires a strict weak ordering and constructs from a range using `make_heap`.

Rust `std::collections::BinaryHeap` is a max-heap by `Ord`; `Reverse` can produce min behavior. Its documentation explicitly treats changing an element's relative ordering while stored as a logic error and exposes a controlled `peek_mut` guard for root mutation. Java's `PriorityQueue` exposes the least element, breaks ties arbitrarily, does not promise iterator order, and is not synchronized; `remove(Object)` and `contains` are linear even though root operations are logarithmic.

Go's `container/heap` separates algorithms from a user-defined interface. Its example maintains indices in `Swap` so `Fix` can repair changed priorities, making the handle obligation visible. Boost.Heap exposes a configurable d-ary heap, including arity, stability, and mutable options; those configuration choices change storage and semantics. Porting code between these APIs requires an explicit semantic adapter, not merely renamed calls.

**Failure, ownership, and memory rules constrain implementation.** Empty `peek`/`pop` may return an option, error, sentinel, or throw; the choice must not confuse an absent entry with a valid value. Reserve/capacity growth can fail before insertion. Comparator execution, element move/copy, allocation, and destruction can fail or panic in some languages. Specify whether an operation offers a strong guarantee (no logical change), a basic guarantee (valid but changed state), or process termination for forbidden failures.

Hole-based repair may temporarily duplicate or vacate logical values. In manual-memory languages, use move/destruction discipline that neither leaks nor double-destroys. In tracing garbage collectors, clear removed array slots if the backing capacity remains reachable, or dead payloads may be retained. Go's official priority-queue example explicitly clears the removed slot. Indirect layouts trade payload movement for pointer chasing and object allocation.

Cancellation-by-tombstone avoids indexed removal: mark a task dead, add a replacement, and discard dead roots during pop. This simplifies mutation but causes physical size and memory to diverge from live size. Track both, compact under a documented policy, and bound adversarial cancellation. Tombstones must use unforgeable state rather than a payload sentinel that a user could supply.

Serialization must define whether array layout is canonical. Two valid heaps containing the same multiset can have different arrays, especially with ties. If the wire contract is abstract, serialize entries and rebuild. If exact replay or stable ties matter, persist sequence keys and comparator identity/version. Never deserialize an untrusted claimed heap without validating length, arity, keys, handle mappings, and every parent-child edge, or rebuilding from bounded input.

**Concurrency is not obtained from atomic array cells.** Push and pop change length and several positions. A reader that observes a mixture of versions can miss an entry, return one twice, or see a nonextremal root. A coarse mutex is often the correct baseline and supplies a clear linearization point. Sharding by producer or priority range can improve throughput but makes exact global minimum selection more expensive. Relaxed concurrent priority queues deliberately return one of several near-best entries and require a different specification.

Holding user comparator code under a lock risks reentrancy, deadlock, or unbounded critical sections. Running it outside a lock risks comparing stale entries. Production designs may restrict comparator purity/cost, precompute keys, or separate synchronization. Cancellation races need a state machine that decides whether pop or cancel wins. Blocking priority queues also need wake-up, shutdown, timeout, and spurious-wake policies; those are synchronization semantics beyond the sequential heap invariant.

**Security and resource control are first-class.** An attacker can submit priorities whose comparison is extremely expensive, inconsistent, or throws; cause tie-heavy workloads; request capacity near overflow; churn cancellation tombstones; or force worst-shaped sequences of repairs. Bound queue size, key/payload size, comparison work, and physical/live ratio. Use checked arithmetic. Treat externally supplied comparator code as privileged or prohibit it.

Priority queues can leak ordering information through timing and observation. A stable tie sequence reveals arrival order. Scheduler priorities can create starvation when urgent work arrives continuously. Aging, quotas, weighted fairness, and admission control are policy layers that intentionally change effective keys; they must update through the heap API or rebuild safely. A mathematically correct heap does not make the surrounding scheduler fair.

**Evidence should attack the representation and the abstraction.** An invariant checker examines every child, every handle/index pair, valid length/capacity, unique live handles, and stable sequence uniqueness. A reference model can store entries in a multiset or sort a copy after each operation and compare the next expected entry. This independently checks observable behavior rather than repeating the heap algorithm.

Exhaust all short operation histories for small `n`, multiple `d`, duplicates, and every removal position. Test sizes around complete-level boundaries: 0, 1, `d`, `d+1`, `1+d+d^2`, and neighbors. Generate inconsistent comparators as negative tests only; the API should reject or document the precondition rather than promise recovery. Inject allocator, comparison, move, cancellation, and serialization failures at every feasible point. For concurrent wrappers, use linearizability or the declared relaxed specification, not merely final item counts.

The following executable uses exact Python integers and immutable tuple keys. It compares a binary and 4-ary heap on one finite input, validates local order before destructive extraction, records comparison counts, and demonstrates stable tie-breaking plus push/pop. It does not establish universal arity performance, fixed-width safety, exception safety, mutable handles, concurrency, or production fitness.

<!-- bijux-verify: {"id":"dary-heap-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"binary_root=D\nbinary_levels=4\nbinary_heapify_comparisons=14\nquaternary_root=D\nquaternary_levels=3\nquaternary_heapify_comparisons=8\nsame_stable_order=True\nstable_order=D,H,F,B,E,I,A,G,C\nbinary_total_comparisons=37\nquaternary_total_comparisons=36\npushed_root=J\npopped_after_push=J\nafter_push_pop_order=D,H,F,B,E,K,I,A,G,C\ninvariant=True\nevidence=finite_dary_heap_trace\n","stderr":""}} -->
```python
class DAryMinHeap:
    def __init__(self, entries=(), arity=2):
        if arity < 2:
            raise ValueError("arity must be at least two")
        self.arity = arity
        self.items = list(entries)
        self.comparisons = 0
        for index in range((len(self.items) - 2) // arity, -1, -1):
            self._sift_down(index)

    def _less(self, left, right):
        self.comparisons += 1
        return self.items[left][:2] < self.items[right][:2]

    def _sift_down(self, index):
        while True:
            first = self.arity * index + 1
            if first >= len(self.items):
                return
            best = first
            for child in range(first + 1, min(first + self.arity, len(self.items))):
                if self._less(child, best):
                    best = child
            if not self._less(best, index):
                return
            self.items[index], self.items[best] = self.items[best], self.items[index]
            index = best

    def _sift_up(self, index):
        while index:
            parent = (index - 1) // self.arity
            if not self._less(index, parent):
                return
            self.items[index], self.items[parent] = self.items[parent], self.items[index]
            index = parent

    def push(self, entry):
        self.items.append(entry)
        self._sift_up(len(self.items) - 1)

    def pop(self):
        if not self.items:
            raise IndexError("pop from empty heap")
        root = self.items[0]
        last = self.items.pop()
        if self.items:
            self.items[0] = last
            self._sift_down(0)
        return root

    def validate(self):
        return all(
            self.items[(index - 1) // self.arity][:2] <= self.items[index][:2]
            for index in range(1, len(self.items))
        )


def occupied_levels(item_count, arity):
    if item_count == 0:
        return 0
    levels = 1
    last = item_count - 1
    while last:
        last = (last - 1) // arity
        levels += 1
    return levels


raw = [(5, "A"), (3, "B"), (7, "C"), (1, "D"), (3, "E"),
       (2, "F"), (6, "G"), (1, "H"), (4, "I")]
entries = [(priority, sequence, name)
           for sequence, (priority, name) in enumerate(raw)]
results = {}
for arity in (2, 4):
    heap = DAryMinHeap(entries, arity)
    build_comparisons = heap.comparisons
    root = heap.items[0][2]
    valid = heap.validate()
    order = [heap.pop()[2] for _ in range(len(heap.items))]
    results[arity] = (root, build_comparisons, heap.comparisons, order, valid)

binary = DAryMinHeap(entries, 2)
binary.push((0, len(entries), "J"))
pushed_root = binary.items[0][2]
popped = binary.pop()[2]
binary.push((3, len(entries) + 1, "K"))
after = [binary.pop()[2] for _ in range(len(binary.items))]

print(f"binary_root={results[2][0]}")
print(f"binary_levels={occupied_levels(len(entries), 2)}")
print(f"binary_heapify_comparisons={results[2][1]}")
print(f"quaternary_root={results[4][0]}")
print(f"quaternary_levels={occupied_levels(len(entries), 4)}")
print(f"quaternary_heapify_comparisons={results[4][1]}")
print(f"same_stable_order={results[2][3] == results[4][3]}")
print("stable_order=" + ",".join(results[2][3]))
print(f"binary_total_comparisons={results[2][2]}")
print(f"quaternary_total_comparisons={results[4][2]}")
print(f"pushed_root={pushed_root}")
print(f"popped_after_push={popped}")
print("after_push_pop_order=" + ",".join(after))
print(f"invariant={results[2][4] and results[4][4]}")
print("evidence=finite_dary_heap_trace")
```

## Definitions and Notation

- `n`: number of live entries; valid array positions are `0..n)`.
- `d`: fixed heap arity, an integer at least two.
- `parent(i)=floor((i-1)/d)`: zero-based parent for `i>0`.
- `child(i,j)=d*i+j`: zero-based child number `j`, where `1<=j<=d` and the result is below `n`.
- **complete tree**: every level except possibly the last is full, and the last is filled left to right.
- `less(a,b)`: strict ordering predicate meaning entry `a` should precede entry `b`.
- **min-heap invariant**: `not less(child,parent)` for every parent-child edge.
- **equivalent keys**: neither key precedes the other under the comparator.
- **sift up/down**: one-path restoration after an insertion/upward or replacement/downward violation.
- **heapify**: construct heap order over an existing array, normally bottom-up.
- **stable priority queue**: equivalent priorities are removed in a declared arrival order.
- **handle**: opaque identity used to locate a live entry independently of its changing array index.
- **physical size**: stored entries including tombstones; **live size** excludes logically removed entries.
- **linearization point**: instant at which a concurrent operation appears to take effect.

## Mechanisms, Invariants, or Proof Structure

The representation proof separates complete shape from order. Array occupancy `0..n)` proves shape. Parent/child division proves that each nonroot entry has exactly one parent and at most `d` consecutive children. Checked arithmetic proves the mapping stays within the represented domain.

Sift-up correctness starts from an old heap plus one appended leaf. Only its ancestor edge can fail. Each repair preserves off-path edges and moves the sole possible violation upward. Sift-down starts from ordered child subheaps plus one displaced root. Selecting the best child preserves promoted order and moves the sole possible violation downward. Both terminate because the index moves strictly toward a boundary.

Bottom-up heapify uses induction from the last internal node toward zero: child subtrees are heaps before their parent is repaired. Its linear bound is an aggregate height argument, not `n` copies of the root height. For fixed `d`, geometrically fewer nodes can descend many levels.

Stable order extends the comparison key with a unique sequence. Mutable priority extends the representation with handle identity and a bidirectional position invariant. These are independent additions: local heap order alone proves neither stable ties nor correct handle lookup. Concurrency, fault safety, and serialization likewise require proofs around the multi-write operation and representation lifecycle.

## Alternatives and Trade-Offs

| Representation | Strength | Main cost or obligation |
|---|---|---|
| Unsorted array/list | constant-time append | linear extremum search/removal |
| Sorted array/list | constant-time extremum access | linear insertion/movement |
| Binary heap | compact general priority queue | logarithmic repair; weak meld/search |
| d-ary heap | lower height, tunable locality | wider child scan; workload tuning |
| Indexed d-ary heap | efficient priority change/removal | handle map, swap/lifetime proof |
| Stable heap | deterministic equivalent-key order | sequence storage/exhaustion policy |
| Tombstoned heap | simple logical cancellation | physical growth and cleanup policy |
| Balanced ordered tree | ordered iteration and arbitrary lookup | pointers/rebalancing or page design |
| Binomial/Fibonacci/pairing heap | stronger meld/decrease-key goals | nodes, constants, complex contracts |
| Bucket/radix/calendar queue | excellent bounded/special key domains | domain/distribution assumptions |
| Concurrent relaxed queue | scalable approximate extremum | weaker observable priority guarantee |
| Selection/top-k array | good bounded batch result | not a general mutable queue |

## Failure Modes and Misconceptions

- **“A heap is a priority queue.”** It is a representation; the ADT may require semantics the representation does not supply by itself.
- **“The heap array is sorted.”** Only ancestor edges are ordered; iteration is generally arbitrary.
- **“Every operation is logarithmic.”** Peek is constant; arbitrary search is linear; batch heapify is linear; outputting all entries is at least linear.
- **“Heapify is `n` logarithmic sifts.”** Most sifts start near leaves; aggregate height proves `O(n)` for fixed arity.
- **“More children always means faster.”** Height falls while child selection widens; machine and workload determine the trade.
- **“Swap with any violating child.”** Sift down must select the best child to avoid leaving a sibling violation.
- **“Arbitrary remove can always sift down.”** The replacement may need to rise.
- **“Comparator direction is obvious.”** Min/max conventions and adaptor semantics differ across libraries.
- **“Equal keys imply FIFO.”** Stability needs an explicit tie key and exhaustion policy.
- **“An array index is a handle.”** Repairs move entries; reallocation can invalidate addresses too.
- **“Changing a stored priority is harmless.”** It invalidates order until repaired through a controlled API.
- **“Replace and push-pop are the same.”** Their returned element differs when the candidate outranks the old root.
- **“Atomic swaps make operations thread-safe.”** Length, root, path, and map updates form one logical transaction.
- **“Lazy deletion is free.”** Tombstones consume memory and pop work until bounded compaction.
- **“One benchmark selects the best arity.”** Input, operation mix, key cost, cache regime, and hardware can reverse results.

## Worked Examples

### Example 1

For `d=4`, index 13 has parent `floor((13-1)/4)=3`. Index 3's children are 13, 14, 15, and 16. Conclusion: parent and child formulas agree at the first child boundary.

### Example 2

A nine-entry binary heap occupies four levels: capacities by level are 1, 2, 4, then 2 used positions. The same entries in a 4-ary heap occupy three levels: 1, 4, then 4. Conclusion: larger arity reduces this instance's dependent path length but says nothing yet about comparison cost.

### Example 3

Appending priority 1 below parent priority 5 violates only that edge. Sift up swaps them; if the next parent is priority 0, repair stops. All sibling subtrees were untouched. Conclusion: insertion correctness follows a single possible-violation path.

### Example 4

After replacing a min-heap root with priority 9, its children have priorities 4, 2, and 6. Swapping with 4 because it is the first violation leaves parent 4 above child 2, still invalid. Selecting 2 is necessary. Conclusion: d-ary sift down scans all existing children for the best one.

### Example 5

Removing an interior entry replaces it with the last entry of priority 1; its parent has priority 3 and its children have priorities 7 and 8. Sifting down would do nothing while the parent edge remains wrong. Conclusion: arbitrary replacement must choose direction from local comparisons.

### Example 6

For a binary heap, roughly half the nodes are leaves and do zero descent, about one quarter can descend one level, one eighth two levels, and so on. The weighted total is bounded by a constant times `n`. Conclusion: bottom-up construction is linear despite a logarithmic worst-case root sift.

### Example 7

Tasks `D` and `H` both have priority 1 but arrival sequences 3 and 7. Comparing `(priority,sequence)` returns `D` first. If sequence wraps and a new task receives 3 again, the key is no longer unique. Conclusion: stable behavior depends on a lifecycle-safe sequence domain.

### Example 8

A mutable heap swaps handles 41 and 77 at positions 2 and 8 but updates only the array. A later decrease-key through handle 41 modifies the entry now at position 2, which is handle 77. Conclusion: every physical move must update the bidirectional position map atomically with the heap operation.

### Example 9

The heap root is priority 3 and candidate `x` is priority 1. Min-heap push-pop returns `x` and can leave the old heap unchanged; replace-root returns priority 3 and retains `x`, then repairs. Conclusion: fused operations need specifications before optimization.

### Example 10

A service benchmark with random 64-bit keys finds `d=8` fastest, but production has expensive string comparators and 70% pops. Wide child scans now dominate. Conclusion: arity evidence must reproduce key cost, operation mix, size distribution, and hardware regime.

## Cross-Program Connections

- **Algorithm engineering:** Dijkstra/A*, event simulation, k-way merge, top-k, heapsort, and selection depend on priority operations and accurate cost models.
- **Programming languages:** comparator laws, generics, option/error behavior, moves, exceptions, ownership, and guards determine usable heap APIs.
- **Concurrent programming:** linearization, locking, sharding, relaxed minima, cancellation races, shutdown, and wake-up policy extend the sequential structure.
- **Database engineering:** buffer eviction, merge scheduling, external sort, timer queues, and query operators need bounded memory and recovery semantics.
- **Data engineering:** streaming top-k, watermarks, merge pipelines, and scheduler queues expose tie, skew, and backpressure policies.
- **Computer architecture:** sibling locality, cache lines, comparison branches, element movement, indirection, and prefetching influence arity.
- **Security engineering:** adversarial comparators, size overflow, tombstone growth, starvation, and priority information leakage require controls.
- **Distributed systems:** local heaps do not define a global arrival order; sharded priority selection and stable ties require coordination semantics.

## References

1. MIT OpenCourseWare 6.006, [Lecture 8: Binary Heaps](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/40d4851e550507ca14dc778b9b2266cc_MIT6_006S20_lec8.pdf), Spring 2020. Academic derivation of array heaps, heap operations, linear build, and heapsort.
2. Robert W. Floyd, [Algorithm 245: Treesort 3](https://www.bitsavers.org/pdf/stanford/Stanford_CS_TR_Collection_2025-12-12/OCR/CS-TR-74-417-ocr.pdf), Communications of the ACM 7(12), 1964, reproduced in Stanford's collected papers. Primary historical source for bottom-up tree/heap sorting.
3. Carnegie Mellon University, [d-Ary Heap Derivations](https://www.cs.cmu.edu/~eugene/teach/algs03b/works/s6.pdf), Algorithms and Data Structures solution notes. Academic derivation of d-ary indexing, height, insert, and extract costs.
4. Python Software Foundation, [`heapq` — Heap Queue Algorithm](https://docs.python.org/3/library/heapq.html), Python 3.14 documentation. Current official min/max API, fused operations, stability, mutation, and lazy-deletion guidance.
5. CPython Project, [`Lib/heapq.py`](https://github.com/python/cpython/blob/main/Lib/heapq.py). Current primary implementation source and comparison-count rationale for Python's binary heap.
6. ISO C++ Working Draft, [Container Adaptors and `priority_queue`](https://eel.is/c%2B%2Bdraft/container.adaptors). Current standard wording for ordering, construction, underlying container, and members.
7. Rust Project, [`std::collections::BinaryHeap`](https://doc.rust-lang.org/stable/std/collections/struct.BinaryHeap.html). Current official max-heap, complexity, `Reverse`, mutation, capacity, and logic-error contract.
8. OpenJDK Project, [`java.util.PriorityQueue` Source](https://github.com/openjdk/jdk/blob/master/src/java.base/share/classes/java/util/PriorityQueue.java). Current primary implementation source for zero-based binary layout, growth, sift, and API guarantees.
9. Oracle, [`PriorityQueue` API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/PriorityQueue.html), Java SE 21. Official least-element, arbitrary-tie, iterator, complexity, and synchronization contract.
10. Boost C++ Libraries, [Heap Data Structures](https://www.boost.org/doc/libs/latest/doc/html/heap/data_structures.html). Current official binary/d-ary, stability, mutability, vector/list representation, and arity trade-off documentation.
11. Go Project, [`container/heap`](https://pkg.go.dev/container/heap). Current official interface, linear initialization, logarithmic fix/remove, and index-maintenance example.

## Exercises

### Exercise 1

Derive zero-based d-ary parent, child, leaf, last-internal-node, and height relations. State all domains and fixed-width overflow checks.

### Exercise 2

Trace bottom-up heapify and one pop on `[9,4,7,1,3,6,2]` for `d=2` and `d=3`. Count key comparisons under a clearly stated child-selection loop and validate every edge.

### Exercise 3

Design a stable indexed min-heap supporting push, peek, pop, remove(handle), and change-priority(handle,key). Specify representation, repair direction, handle lifetime, sequence exhaustion, failure safety, and invariant tests.

### Exercise 4

Choose between a binary heap, 4-ary heap, balanced ordered tree, tombstoned heap, bucket queue, and concurrent relaxed queue for three production workloads. State which measurements could reverse each choice.

### Exercise 5

Design a bounded multi-tenant work scheduler using heaps. Address fairness, admission, cancellation races, stable ties, priority aging, concurrency, overload, persistence/restart, observability, and adversarial tenants.

## Answers to the Exercises

### Answer 1

Children of zero-based parent `p` are `d*p+1..d*p+d`. Solving that interval for nonroot `i` gives `parent(i)=floor((i-1)/d)`. The first child is `d*i+1`, so `i` is a leaf exactly when that value is at least `n`; for `n>=2`, the last internal node is `floor((n-2)/d)`. Level `h` begins after `1+d+...+d^(h-1)` positions; occupied levels are `1+floor(log_d((n-1)(d-1)+1))` for `n>0`, with zero levels for `n=0`, subject to an exact-integer implementation rather than floating rounding. Require `d>=2`, `0<=i<n`, `1<=j<=d`, and check `i>(MAX-j)/d` before forming `d*i+j`. Also check capacity-to-byte multiplication and representation-specific maximum length.

### Answer 2

Use min order and count each key-to-key comparison. For each arity, start at `floor((n-2)/d)` and sift indices down to zero; at each visited parent, compare existing children to choose the minimum, then compare that child with the displaced item. Record the array after each move. After heapify, validate `A[parent(i)]<=A[i]` for every `i>0`. Pop by saving root 1, moving the last item to root, shrinking length, and applying the identical sift-down rule; validate again and confirm every remaining item is at least 1. Exact intermediate arrays and counts may differ only if the implementation explicitly uses a different but correct comparison schedule; an acceptable answer supplies that schedule, the complete trace, the same extremal result, and valid final edges. The binary and ternary counts from this seven-item instance are evidence for the trace only, not asymptotic superiority.

### Answer 3

Store array entries `(key,sequence,handle,payload)`, compare `(key,sequence)`, and map each live handle to its current index. Push allocates a never-live handle and unique sequence, appends, records the position, then sifts up. Every swap updates both map entries. Pop/remove invalidates the removed handle and replaces from the last position; choose upward repair if the replacement precedes its parent, otherwise downward repair. Change-priority records old/new order and uses the appropriate direction, while preserving sequence unless the public contract says reprioritization is a new arrival. Use generation-tagged opaque handles so stale identities cannot alias reused slots. At sequence exhaustion, reject or perform a proved stop-the-world stable renumber; silent wrap is forbidden. Define allocation/comparator/move failure guarantees and order map publication so no failed operation exposes a mismatched pair. Validate every parent edge, unique sequence/handle, both mapping directions, stale-handle rejection, sizes 0/1 and level boundaries, equal keys, every removal index, arbitrary changes, injected failures, and histories against a sorted reference model.

### Answer 4

A binary heap is a strong baseline for mixed exact root operations and cheap comparisons. A 4-ary heap is a candidate when upward updates or dependent height dominate and contiguous child scans are cheap; benchmark against binary. A balanced tree fits ordered iteration, range access, and arbitrary lookup, accepting nodes and rebalancing. Tombstones fit cancellation when updates are moderate and compaction bounds physical/live growth. A bucket queue fits bounded integer priorities or distributions that keep bucket scans bounded. A concurrent relaxed queue fits high contention only if returning a near-best entry is acceptable. Measurements include push/pop/change/remove proportions, live/physical size, tie/skew/order distributions, comparator and payload cost, allocations, cache/branch behavior, contention, cancellation churn, exactness tolerance, memory ceiling, p50/p99/p999 latency, and recovery cost. Any changed workload, key, size, machine, or semantic requirement can reverse the choice.

### Answer 5

Maintain per-tenant bounded queues and a global structure over each tenant's eligible head rather than one unbounded global heap. Admission enforces tenant/global live bytes and task counts. Effective priority combines declared priority, enqueue sequence, tenant weight, and monotone aging under a precisely defined ordering; recompute through controlled updates, never mutate stored keys invisibly. Generation-tagged task handles support cancellation. A locked state transition decides whether cancel or pop wins, and completion is idempotent. Stable sequence has a persisted width/exhaustion policy; restart reloads logical entries and heapifies rather than trusting raw layout. Shard locks where measurements justify it, define the global-selection approximation if shards relax exact priority, and avoid user callbacks under internal locks. Overload rejects, sheds, or backpressures by policy; it does not grow without bound. Persist task state and sequence before acknowledging according to the required durability level. Emit live/physical sizes, per-tenant age, starvation, cancellations, compactions, comparison latency, lock wait, queue delay, and tail service latency. Test hostile priority churn, huge payloads, tie floods, comparator/key validation, crashes at acknowledgment boundaries, stale handles, cancellation/pop races, continuous high-priority arrivals, and recovery equivalence.
