---
module_id: DSE-039
program: Data Structures Engineering
level: 1
module_number: 39
title: Indexed and Meldable Priority Queues
status: complete
last_verified: 2026-08-30
---

# Indexed and Meldable Priority Queues

## One-Page Review

### Governing question

How should a priority queue represent stable identity and efficient union when clients need direct key updates, arbitrary cancellation, or frequent melding rather than only root access?

### Essential definitions

- An **indexed priority queue** maps each live handle to the entry's current position, making key change and arbitrary removal possible without a linear search.
- A **handle** is opaque stable identity; an array index is only a transient location.
- A **position invariant** is bidirectional: `position[handle]=i` and `heap[i].handle=handle` must agree for every live entry.
- **meld** combines two priority queues while preserving their observable ordering contract.
- A **destructive meld** consumes or empties at least one input; a **persistent meld** returns a result while retaining previous versions.
- A **leftist heap** is a heap-ordered binary tree whose left null-path rank is at least its right rank; the right spine is logarithmic.
- A **binomial heap** is a forest containing at most one heap-ordered binomial tree of each rank; melding resembles binary addition with carries.
- A **Fibonacci heap** defers consolidation and uses cuts plus marking to obtain strong amortized bounds.
- A **pairing heap** is a self-adjusting multiway heap with a simple link operation and variant-dependent delete-min/decrease-key analysis.
- **amortized time** bounds the total over every operation sequence; it is not an average over random inputs and does not bound each latency.

### Central model, mechanism, or theorem

Indexing and melding solve different access problems. An indexed array heap adds a dictionary or inverse array and updates it on every swap. Direct lookup is expected `O(1)` with hashing or worst-case `O(1)` for bounded dense IDs; repair remains `O(log n)`. A stale or half-updated position map invalidates the whole abstraction even if parent-child order still holds.

Meldable heaps make union structural. A leftist heap recursively links roots and repairs right-spine rank, giving `O(log n)` worst-case meld. Binomial heaps combine equal-rank trees like carries and give logarithmic worst-case union. Fibonacci heaps leave many roots unconsolidated, pay during delete-min, and use a potential such as roots plus twice marked nodes to obtain `O(1)` amortized insert, meld, and decrease-key with `O(log n)` amortized delete-min. These guarantees rely on exact structural and amortization invariants, not the word “heap.”

### Critical invariants

1. Heap order, stable tie policy, comparator identity, and empty behavior are explicit.
2. Every live handle names exactly one entry, every entry has one live handle, and every physical move updates the inverse mapping.
3. Removed handles are invalidated and cannot alias later entries; generation and counter exhaustion have policies.
4. Key change chooses repair direction from old/new order or local relations; it never silently accepts a forbidden increase/decrease.
5. Meld defines ownership of source queues, nodes, handles, allocators, comparators, stability counters, and failures.
6. Leftist ranks, binomial ranks/uniqueness, Fibonacci degrees/marks, and pairing sibling structure are locally and globally valid.
7. Amortized claims name the potential/accounting argument and do not become per-operation latency claims.
8. Cancellation, serialization, concurrency, and reclamation preserve both logical membership and structural reachability.

### Common failures

- Updating the heap array but not the position map during one swap.
- Using caller-visible array indices as stable handles.
- Allowing a removed handle to target a newly allocated entry.
- Implementing arbitrary removal with sift down only.
- Reinsert-on-update without bounding stale entries and pop cleanup.
- Calling array concatenation plus heapify constant-time meld.
- Melding queues with incompatible comparators or stability epochs.
- Keeping donor handles alive without defining their new owner.
- Quoting Fibonacci amortized bounds as worst-case latency.
- Treating every pairing-heap variant as having the same proven decrease-key bound.

### Compact example

An indexed min-heap inserts `A..F`, decreases `C` from 7 to 0, removes `B` by handle, increases `D` to 8, and adds `G` tied at priority 3. Bidirectional map repair yields `C,F,E,G,A,D`. Separately, two leftist heaps destructively meld to six entries and extract `C,D,B,A,F,E`; the donor is empty and rank/order validation passes.

### Connections

[DSE-038](038-binary-and-d-ary-heaps.md) supplies array shape, sift proofs, arity, stability, and failure foundations. [DSE-023](023-linear-probing.md) and [DSE-028](028-resizing-and-incremental-rehashing.md) inform hashed position maps. [DSE-035](035-splay-trees.md) supplies self-adjusting analysis. The [program roadmap](../ROADMAP.md) continues with skip lists, graph representations, tries, and disjoint-set union.

## Governing Question

Which identity model, inverse mapping, meld semantics, structural invariant, amortized proof, ownership boundary, and measured workload justify an indexed binary/d-ary heap, lazy reinsertion, leftist/skew heap, binomial heap, Fibonacci heap, or pairing heap?

## Why This Matters

The basic heap interface answers “what is best now?” Many important clients also ask “make this particular item better,” “cancel this exact item,” or “combine the work accumulated by two producers.” Dijkstra's shortest-path algorithm, Prim's minimum-spanning-tree algorithm, discrete-event simulation, incremental schedulers, external merge systems, and work-stealing runtimes expose these operations directly.

Without identity, changing a known item's key requires an `O(n)` scan or reinserting a new version and leaving a stale copy behind. Without structural meld, combining two array heaps means repeated insertion or concatenation plus heapify. Those may be correct choices, but their space, latency, ownership, and cleanup contracts differ from an indexed or meldable queue.

This topic also disciplines performance reasoning. Fibonacci heaps are famous because amortized analysis changes graph-algorithm bounds. That theorem does not say they are universally faster, simpler, more cache-friendly, or lower-latency. Pairing heaps are famous for simple self-adjustment and subtle analyses. Array heaps remain compelling because contiguous storage and small constants often dominate. A production decision must preserve the mathematical assumptions while measuring the actual operation mix.

The legacy corpus contains an earlier indexed-queue chapter with useful motivation and a position-map model. It was reviewed as background, not copied: its concrete benchmark is machine-specific, and its arbitrary deletion repairs only downward, which is incorrect when the replacement must rise. The new module retains the durable identity insight, corrects the repair boundary, and integrates meld, ownership, amortization, and verification.

## Prerequisites and Retrieval

Retrieve ADT/representation separation and validator design from [DSE-001](001-abstract-data-types-and-concrete-representations.md) and [DSE-002](002-representation-invariants.md). Retrieve expected/worst/amortized costs from [DSE-004](004-time-space-and-allocation-cost.md), contiguous versus linked locality from [DSE-005](005-contiguous-and-linked-layouts.md) and [DSE-006](006-memory-locality-and-cache-behavior.md), and ordering/genericity from [DSE-007](007-genericity-and-type-constraints.md). Retrieve property evidence and workload measurement from [DSE-009](009-property-based-testing-of-data-structures.md) and [DSE-010](010-benchmarking-a-structure-without-misleading-results.md). Retrieve complete array heaps, stability, arbitrary repair, and concurrency limits from [DSE-038](038-binary-and-d-ary-heaps.md).

## Learning Objectives

After completing this module, you should be able to:

1. specify handle identity, validity, ownership, and stale-handle behavior;
2. implement and validate a bidirectional position map for an indexed binary or d-ary heap;
3. distinguish direct update, arbitrary replacement, lazy reinsertion, and tombstone cancellation;
4. specify destructive, nondestructive, and persistent meld with comparator/allocator compatibility;
5. derive leftist-heap logarithmic right-spine and meld bounds;
6. derive binomial-forest structure and union as rank-wise carry propagation;
7. explain Fibonacci-heap lazy consolidation, cuts, marks, degree bounds, and potential accounting;
8. describe pairing-heap linking and two-pass delete-min without overstating variant-specific theory;
9. choose a queue from operation frequencies, memory/locality, worst-case latency, and implementation risk;
10. design invariant, oracle, exhaustive, fault, handle-lifetime, meld, concurrency, and benchmark evidence.

## Core Exposition

**Define the operation vector before choosing a heap.** A useful priority-queue contract may include `make`, `is_empty`, `size`, `peek`, `insert`, `extract`, `change_key`, `decrease_key`, `increase_key`, `remove(handle)`, and `meld`. State min or max direction. State stable ties, duplicate values, duplicate keys, and iteration semantics. State which calls return handles and which operations preserve them.

Complexity is a vector too. A binary heap gives constant-time peek and logarithmic insertion/extraction; an indexed variant adds logarithmic direct update/removal. An unsorted meld can be constant only by deferring work somewhere else. A binomial or leftist heap supports structural meld efficiently. A Fibonacci heap moves work from insertion/meld/decrease into later consolidation while retaining a bound over the sequence. There is no single scalar “best heap.”

Separate **actual**, **worst-case**, **amortized**, and **expected** cost. Fibonacci insert can link a root into a list in actual constant time, while delete-min may consolidate many roots; potential pays for that accumulated disorder. A hash map used for handle lookup may be expected constant time under its hash assumptions. A concurrent relaxed queue may improve throughput by weakening exact-min behavior. Each qualifier changes what a client can rely on.

**An indexed heap adds an inverse representation.** Store entries in an ordinary binary or d-ary array heap. Each entry carries an opaque handle. A map stores `position[handle]=array_index`. For dense stable IDs drawn from `0..U)`, the map can be an inverse array with a sentinel for absence. For sparse or external IDs, use a hash table or ordered map and include its complexity and attack model.

The invariant is bijective over live entries. Array length equals the number of live handles. Every array entry's handle maps back to its exact index. Every map item names an in-range array position containing the same handle. Handles are unique. Heap order holds independently. A complete validator checks both directions; checking only that each entry appears in the map misses extra or aliased map entries.

`insert` allocates or accepts a valid new handle, appends the entry, installs the mapping, and sifts upward. Every swap is a representation primitive: swap entries, then set both handles' positions. Centralize it rather than duplicating two-array writes throughout repair code. `peek` reads root without changing identity. `extract` removes the root handle, moves the last entry, updates its position, and sifts down.

`remove(handle)` looks up the index in expected or worst-case map time, invalidates membership, moves the last entry into the hole, then chooses repair direction. If the replacement precedes its parent, sift up; otherwise sift down. The old entry must not remain reachable from the map. When removing the last entry, no replacement or repair occurs. When removing from an empty or stale handle, return a defined error without touching structure.

`decrease_key` in a min-heap checks that the new key does not follow the old key, writes it, and sifts up. `increase_key` sifts down. A general `change_key` can compare old and new or inspect the parent after replacement and select a direction. Comparator equivalence needs policy: a stable queue usually preserves the original sequence when priority changes, while a scheduler may treat reprioritization as a new arrival. Name that choice.

Strong exception safety is difficult when map insertion, array growth, comparator execution, or element moves fail. One design reserves capacity and creates map state before publishing the entry; another uses rollback guards. The required guarantee may be “unchanged on failure” or merely “valid, membership explicitly reported.” A half-installed handle or map/array disagreement is never an acceptable basic guarantee.

**Handles are capabilities with lifetimes.** An integer array position is not a handle because sifting changes it. A pointer into a dynamic array is invalidated by reallocation and still moves with entries. A payload value may not be unique. Use an opaque token carrying a slot identity and generation, or a stable node object referenced from both heap and registry.

On removal, mark the generation dead before a slot can be reused. A stale operation returns an error; it must not mutate the new occupant. Generation wrap is not impossible merely because the type is wide: reject reuse, widen the generation, or prove a lifetime bound. If handles cross threads, processes, restarts, or tenants, include owner and epoch identity so an otherwise valid number cannot target the wrong queue.

Borrowed handles must not outlive the queue. Owning handles complicate destruction because dropping a handle might or might not cancel its entry. Weak handles may observe absence. Serialization may intentionally invalidate all pre-restart handles or persist globally unique IDs and rebuild a registry. These are API semantics, not implementation trivia.

**Lazy reinsertion is a different design point.** When an item's key improves, push a new `(key,version,id)` entry and record the authoritative version in a separate table. During extraction, discard entries whose versions are stale. This uses an ordinary heap and avoids position maintenance. It is often excellent when updates are rare or library constraints forbid handles.

The logical queue can contain `n` live items while the physical heap contains `n+s` entries after `s` updates/cancellations. Worst-case pop may discard many stale roots. Memory can grow without bound unless a policy rebuilds when physical/live ratio, dead bytes, or latency crosses a threshold. Rebuild must snapshot authoritative entries and heapify; concurrent updates need version coordination. Complexity claims must include stale cleanup and compaction, not call each update simply logarithmic and stop there.

Indexed and lazy designs can both support Dijkstra correctly. Indexed storage keeps at most one live heap entry per vertex and performs direct decreases. Lazy storage pushes improved distances and ignores a pop whose distance no longer equals the authoritative best. Their asymptotic graph bound may match in common formulations while memory, map operations, constants, and peak latency differ. Measure graph density, successful relaxation rate, duplicates, key type, and cache regime.

**Meld needs a semantic contract before a data structure.** Given queues `A` and `B`, the result represents their multiset union under one ordering. Does `meld(A,B)` mutate `A` and empty `B`, consume both and return a new queue, copy entries, or preserve persistent versions? Are handles from `B` valid afterward, and if so which queue owns them? What happens if the same handle appears in both?

Comparators must be compatible. Two function objects can have the same type but different captured state. A min-heap cannot safely meld with a max-heap by concatenating nodes. Stable sequences may have overlapping counters; prepend an origin epoch, reserve disjoint counter ranges, or renumber according to a declared cross-queue order. Allocator/resource compatibility matters when nodes allocated by `B` become owned and later freed by `A`.

Destructive meld can be constant or logarithmic because it transfers nodes. Copying meld must at least account for copied elements. Persistent meld shares immutable nodes and therefore needs path-copy structure plus lifetime management. A concurrency-safe meld often must lock two queues in global identity order to prevent deadlock, then atomically transfer ownership. Self-meld should be rejected or a no-op by specification; blindly linking a root to itself creates a cycle.

**Leftist heaps make one spine short.** A leftist min-heap is a heap-ordered binary tree. Define null-path rank `rank(empty)=0` and `rank(node)=1+min(rank(left),rank(right))`. Enforce `rank(left)>=rank(right)`, so `rank(node)=rank(right)+1`. Because a rank-`r` node contains at least `2^r-1` nodes, the right spine has length at most `floor(log2(n+1))`.

To meld roots `x` and `y`, return the nonempty one if either is empty. Otherwise ensure `x` has the smaller root, recursively meld `x.right` with `y`, swap children if left rank is smaller, and recompute `x.rank` from the right. The recursion follows right spines, so worst-case time is logarithmic in total size. Insert melds with a singleton. Extract-min melds the root's left and right subheaps. No parent pointer is required for those operations.

The proof has three layers. Root selection preserves heap order because the smaller root precedes both inputs. Recursive induction returns a valid melded right subtree. Child swap and rank recomputation restore the leftist invariant without changing membership or order. The rank-size lemma bounds recursion depth. A **skew heap** drops stored ranks and always swaps children after recursive meld; it is simpler and self-adjusting, with amortized rather than leftist worst-case meld bounds.

Leftist/skew heaps are node-based. They pay allocations, pointers, poorer spatial locality, allocator metadata, and reclamation complexity relative to arrays. They become attractive when meld frequency and node transfer outweigh those costs. Intrusive nodes can reduce allocation but expose ownership and aliasing hazards. Recursive implementations need a stack-depth argument or iterative transformation.

**Binomial heaps encode size in ranks.** A binomial tree `B_0` is one node. Link two `B_k` trees by making the larger root a child of the smaller root, producing `B_{k+1}`. `B_k` has `2^k` nodes, root degree `k`, and binomially distributed nodes by depth. A binomial heap stores at most one tree of each rank, so an `n`-entry heap has at most `floor(log2 n)+1` roots; occupied ranks correspond to set bits in `n`.

Meld merges root lists ordered by rank. At each rank, zero, one, two, or three trees may appear when including a carry. One tree is emitted; two are linked into a carry; three emit one and link two according to a defined case table. This is binary addition. Each link preserves heap order, rank increases by one, and uniqueness is restored. The number of ranks is logarithmic, yielding worst-case `O(log(n+m))` union in a standard representation.

Finding minimum may scan the logarithmic root list unless a minimum pointer is maintained. Insert is meld with `B_0`; eager carry can be logarithmic worst-case and constant amortized under bit-flip accounting. Extract-min removes the minimum root, reverses or reorders its children into rank order, then melds that forest with the remainder. Handles for decrease-key often swap keys/payloads upward, but that can violate stable node identity: if a handle promises one logical item, moving only key/value changes which node it denotes. Either swap full logical entries and repair handle-node associations or structurally cut under a different heap design.

**Fibonacci heaps defer organization.** Represent a collection of heap-ordered trees in a circular root list with a minimum pointer. Insert adds a singleton root. Meld concatenates root lists and selects the smaller minimum. Neither operation immediately enforces unique degrees. Delete-min removes the minimum root, promotes its children to roots, and consolidates roots of equal degree until at most one per degree remains.

Decrease-key updates a referenced node. If heap order with its parent breaks, cut the node to the root list. A nonroot node that loses its first child becomes marked; losing another child cuts it too, cascading upward until reaching an unmarked node or root. Marks bound how many children a node can lose without being detached. Fibonacci-number growth then bounds maximum degree by `O(log n)`.

A standard potential is `Phi=number_of_roots+2*number_of_marked_nonroots`. Insert and meld add only constant actual work and potential. Decrease-key may perform many cascading cuts, but each cut after the first removes a mark, releasing potential that pays for the work; amortized cost is constant. Delete-min may consolidate many roots, but potential falls as roots are linked, and the logarithmic degree bound limits survivors. It has `O(log n)` amortized cost. Delete can decrease to a distinguished minus-infinity key and delete-min only if the key domain supplies a value strictly before every legal key and handle identity is preserved; otherwise implement deletion directly.

These are amortized, comparison-model results under a faithful implementation. A single delete-min can take linear actual time after many inserts. Real-time systems cannot substitute the amortized bound for a per-operation deadline. Strict Fibonacci heaps and other variants target stronger worst-case bounds with additional machinery; they are different structures and proofs.

**Pairing heaps simplify self-adjustment.** A pairing heap is a heap-ordered multiway tree. Meld links the larger root as the first child of the smaller root. Insert melds a singleton. Decrease-key cuts the improved node and melds it with the root, subject to handle/parent-sibling maintenance. Delete-min removes the root and combines its child subheaps.

The classic two-pass delete-min first links adjacent siblings left to right, then melds the resulting heaps right to left. Other multipass, forward, auxiliary-list, or lazy variants arrange this differently. Their analyses are not interchangeable. The original paper intentionally presented a simple structure with partial analysis and a conjecture about Fibonacci-like efficiency; later work established and refined bounds for particular variants. A responsible implementation cites the exact variant and bound it uses.

Pairing heaps often have attractive code size and practical behavior, but “fast in practice” is a workload-specific empirical claim. Parent pointers or predecessor links needed for direct cuts increase memory and mutation surface. Child/sibling lists impair locality. Key distributions, decrease frequency, allocation, and compiler/runtime behavior can overwhelm asymptotics.

**Array heaps still have valid meld strategies.** To combine arrays of sizes `n` and `m`, append the smaller/second array and bottom-up heapify the total in `O(n+m)` time. Repeated insertion costs `O(m log(n+m))` in the worst case but may be good when `m` is tiny and avoids rebuilding the large heap. If queues meld rarely but push/pop constantly, contiguous arrays can win overall.

Batching offers another option: keep several immutable runs/heaps and a small heap of their roots, then consolidate under thresholds. This resembles log-structured design and shifts cost into reads/compaction. It needs explicit bounds on number of runs, stale handles, and tail latency. Calling any of these “meldable” without stating complexity and ownership hides the actual contract.

**Boost's current API makes several hidden choices visible.** Its heap concepts distinguish `is_mergable`, stability, ordered iterators, reserve support, and constant-time size. Mutable queues return handles and require `update`, `increase`, or `decrease` after value mutation; using the wrong directional repair can corrupt the structure. Generic `heap_merge` works across heap types, but efficient structural merge depends on capabilities. This is a useful model: expose semantic and complexity properties rather than pretending all priority queues are substitutable.

Go's `container/heap` exposes `Fix` and `Remove(index)` over a user-maintained interface; its example updates item indices inside `Swap`. That is an indexed heap building block, not a safe opaque-handle registry by itself. A client retaining an index across unrelated operations will be wrong. The distinction between algorithm hook and public identity should be clear in wrappers.

**Testing needs two independent oracles.** For observable order, maintain a reference map from handle to `(key,sequence,value)` and compute the minimum by a full scan or sort. For membership, compare exact live handle sets. After every generated operation, validate structure-specific invariants and compare `peek`, size, errors, and extracted results with the model.

Exhaust small histories containing insert, both-direction key changes, remove every position, pop, duplicate priorities, stale handles, and meld. Generate two queues with overlapping payloads but disjoint handles; separately test rejected handle collisions, comparator mismatch, self-meld, empty meld, and donor use after consumption. For stable meld, exercise overlapping local sequence numbers and verify the specified cross-queue order.

Leftist validators recompute rank and subtree size and check `left_rank>=right_rank`. Binomial validators check acyclicity, parent links, heap order, exact rank/degree, subtree size `2^rank`, and unique root ranks. Fibonacci validators add root/child circular-list integrity, parent pointers, degrees, marks, minimum, and a separately recomputed potential. Pairing validators check one-parent reachability, sibling links, root order, and any parent/predecessor metadata.

Fault injection targets allocation, comparator, registry insertion, each swap/link/cut, and donor transfer. Verify the promised post-failure state and absence of leaks, cycles, double ownership, or half-moved handles. Deserialization fuzzing targets sizes, cycles, rank/degree lies, duplicate handles, and comparator identifiers. Concurrency tests check linearizability or the stated relaxed semantics plus deadlock-free two-queue meld.

Benchmark operation traces, not isolated calls only. Report queue-size distribution, insert/extract/change/remove/meld ratios, meld operand sizes, tie and key distributions, success rate of decreases, stale-entry ratio, payload size, allocations, bytes, cache/branch events, lock wait, and tail latency. Include build/destruction and compaction. Compare implementations with identical semantics; a stable indexed queue and unstable unindexed heap are not equivalent baselines.

The executable below provides bounded evidence for two separate mechanisms. The indexed binary heap maintains an opaque integer handle and bidirectional position map through decreases, increase, removal, insertion, and extraction. The leftist heap destructively melds two independently built queues, empties the donor, and checks heap order, rank, and size before extraction. It does not prove generic comparison laws, fixed-width or failure safety, stale-generation handling, binomial/Fibonacci/pairing invariants, concurrency, or production performance.

<!-- bijux-verify: {"id":"indexed-and-meldable-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"indexed_initial_root=D\nindexed_after_decrease=C\nindexed_removed=B\nindexed_order=C,F,E,G,A,D\nindexed_invariant=True\nmeld_root=C\nmelded_size=6\ndonor_empty=True\nmeld_invariant=True\nmeld_order=C,D,B,A,F,E\nevidence=finite_indexed_and_meld_trace\n","stderr":""}} -->
```python
from dataclasses import dataclass


class IndexedMinHeap:
    def __init__(self):
        self.items = []
        self.positions = {}
        self.next_handle = 0
        self.next_sequence = 0

    def _swap(self, left, right):
        self.items[left], self.items[right] = self.items[right], self.items[left]
        self.positions[self.items[left][2]] = left
        self.positions[self.items[right][2]] = right

    def _up(self, index):
        while index:
            parent = (index - 1) // 2
            if self.items[parent][:2] <= self.items[index][:2]:
                return
            self._swap(parent, index)
            index = parent

    def _down(self, index):
        while True:
            best = index
            for child in (2 * index + 1, 2 * index + 2):
                if child < len(self.items) and self.items[child][:2] < self.items[best][:2]:
                    best = child
            if best == index:
                return
            self._swap(index, best)
            index = best

    def push(self, key, value):
        handle = self.next_handle
        self.next_handle += 1
        entry = (key, self.next_sequence, handle, value)
        self.next_sequence += 1
        self.positions[handle] = len(self.items)
        self.items.append(entry)
        self._up(len(self.items) - 1)
        return handle

    def change_key(self, handle, key):
        index = self.positions[handle]
        old = self.items[index]
        self.items[index] = (key, old[1], handle, old[3])
        if index and self.items[index][:2] < self.items[(index - 1) // 2][:2]:
            self._up(index)
        else:
            self._down(index)

    def discard_handle(self, handle):
        index = self.positions.pop(handle)
        removed = self.items[index]
        last = self.items.pop()
        if index < len(self.items):
            self.items[index] = last
            self.positions[last[2]] = index
            if index and self.items[index][:2] < self.items[(index - 1) // 2][:2]:
                self._up(index)
            else:
                self._down(index)
        return removed[3]

    def pop(self):
        if not self.items:
            raise IndexError("pop from empty heap")
        return self.discard_handle(self.items[0][2])

    def peek(self):
        return self.items[0][3]

    def validate(self):
        if len(self.items) != len(self.positions):
            return False
        for index, item in enumerate(self.items):
            if self.positions.get(item[2]) != index:
                return False
            if index and self.items[(index - 1) // 2][:2] > item[:2]:
                return False
        return True


@dataclass
class LeftistNode:
    entry: tuple
    left: object = None
    right: object = None
    rank: int = 1


class LeftistMinHeap:
    def __init__(self):
        self.root = None
        self.size = 0

    @staticmethod
    def _rank(node):
        return 0 if node is None else node.rank

    @classmethod
    def _merge(cls, first, second):
        if first is None:
            return second
        if second is None:
            return first
        if second.entry[:2] < first.entry[:2]:
            first, second = second, first
        first.right = cls._merge(first.right, second)
        if cls._rank(first.left) < cls._rank(first.right):
            first.left, first.right = first.right, first.left
        first.rank = cls._rank(first.right) + 1
        return first

    def push(self, entry):
        self.root = self._merge(self.root, LeftistNode(entry))
        self.size += 1

    def meld(self, other):
        self.root = self._merge(self.root, other.root)
        self.size += other.size
        other.root = None
        other.size = 0

    def pop(self):
        if self.root is None:
            raise IndexError("pop from empty heap")
        entry = self.root.entry
        self.root = self._merge(self.root.left, self.root.right)
        self.size -= 1
        return entry

    def validate(self):
        def check(node):
            if node is None:
                return 0, 0
            left_rank, left_size = check(node.left)
            right_rank, right_size = check(node.right)
            for child in (node.left, node.right):
                if child is not None and child.entry[:2] < node.entry[:2]:
                    raise AssertionError("heap order")
            if left_rank < right_rank or node.rank != right_rank + 1:
                raise AssertionError("leftist rank")
            return node.rank, left_size + right_size + 1

        _, actual_size = check(self.root)
        return actual_size == self.size


indexed = IndexedMinHeap()
handles = {
    name: indexed.push(key, name)
    for key, name in [(5, "A"), (3, "B"), (7, "C"),
                      (1, "D"), (3, "E"), (2, "F")]
}
print(f"indexed_initial_root={indexed.peek()}")
indexed.change_key(handles["C"], 0)
print(f"indexed_after_decrease={indexed.peek()}")
print(f"indexed_removed={indexed.discard_handle(handles['B'])}")
indexed.change_key(handles["D"], 8)
indexed.push(3, "G")
indexed_valid = indexed.validate()
print("indexed_order=" + ",".join(indexed.pop() for _ in range(len(indexed.items))))
print(f"indexed_invariant={indexed_valid}")

first = LeftistMinHeap()
second = LeftistMinHeap()
for entry in [(5, 0, "A"), (1, 2, "C"), (7, 4, "E")]:
    first.push(entry)
for entry in [(2, 1, "B"), (1, 3, "D"), (6, 5, "F")]:
    second.push(entry)
first.meld(second)
print(f"meld_root={first.root.entry[2]}")
print(f"melded_size={first.size}")
print(f"donor_empty={second.size == 0 and second.root is None}")
print(f"meld_invariant={first.validate()}")
print("meld_order=" + ",".join(first.pop()[2] for _ in range(first.size)))
print("evidence=finite_indexed_and_meld_trace")
```

## Definitions and Notation

- `H`: a priority queue under a declared strict ordering.
- `handle`: stable opaque identity for one live logical entry.
- `position[h]`: current array index for handle `h` in an indexed heap.
- `key(h)`: ordering key of the entry named by `h`.
- `meld(A,B)`: queue union under explicitly declared ownership semantics.
- `rank(x)`: structure-specific integer summary; its meaning differs between leftist, binomial, and Fibonacci heaps.
- `B_k`: binomial tree of rank `k`, containing `2^k` nodes.
- `t(H)`: number of Fibonacci-heap roots.
- `m(H)`: number of marked nonroot nodes in a Fibonacci heap.
- `Phi(H)=t(H)+2m(H)`: standard potential used to account for deferred structure.
- **cut**: detach a node from its parent and add it to the root collection.
- **consolidation**: repeatedly link roots of equal degree/rank.
- **actual cost**: work of one execution; **amortized cost**: actual cost plus potential change.
- **stale entry**: physical heap item superseded or canceled in the logical model.
- **destructive meld**: transfers membership/ownership and invalidates or empties a donor according to contract.

## Mechanisms, Invariants, or Proof Structure

Indexed-heap correctness is the conjunction of array heap order and a bijection between live handles and physical entries. Every swap is a joint update. Insert establishes mapping before repair; change selects the direction that can contain the sole violation; removal invalidates the old handle, fills the hole, and repairs up or down. Generation identity prevents stale tokens from aliasing reuse.

Leftist meld chooses the better root, recursively melds right spines, then restores rank order. Heap order follows root choice and induction; rank recomputation plus the rank-size lemma bounds the spine logarithmically. Binomial meld links equal ranks as binary carries. Unique root ranks and `2^rank` subtree size bound root count and union work.

Fibonacci heaps deliberately permit many roots and postpone equal-degree links until delete-min. Cuts and marks prevent repeated child loss from destroying logarithmic degree. Potential `t+2m` pays for accumulated roots and cascading cuts, yielding sequence bounds rather than per-call deadlines. Pairing heaps link roots similarly but rely on a specified multipass/two-pass self-adjusting schedule whose bound must match the exact variant.

Meld correctness also includes semantic state outside tree edges: comparator equivalence, stable epochs, allocator ownership, source consumption, handle migration, failure atomicity, lock order, and reclamation. A structurally valid union can still violate the public contract if any of these are undefined.

## Alternatives and Trade-Offs

| Design | Key advantage | Main obligation |
|---|---|---|
| Unindexed binary/d-ary heap | compact, local, simple | linear arbitrary lookup |
| Indexed array heap | direct change/remove, good locality | map cost and exact swap repair |
| Lazy reinsertion | uses basic library heap | stale memory/pop tails/rebuild |
| Append plus heapify | simple batch union | linear in combined size |
| Leftist heap | logarithmic worst-case meld | nodes, ranks, right-spine proof |
| Skew heap | no rank metadata | amortized self-adjusting proof |
| Binomial heap | rank-structured logarithmic union | forest/carry and node identity |
| Fibonacci heap | strong amortized meld/decrease | complex links, marks, consolidation |
| Pairing heap | simple structural link, practical candidate | variant-specific theoretical bounds |
| Persistent meldable heap | retains versions | immutability, sharing, lifetime/memory |
| Bucket/radix queue | excellent constrained key domains | integer/range/monotonicity assumptions |
| Concurrent relaxed queue | scalable contention behavior | approximate rather than exact extremum |

## Failure Modes and Misconceptions

- **“A handle is the current index.”** Repair moves entries; stable identity must be indirect.
- **“Checking entry-to-map direction is enough.”** Extra or aliased map entries require the reverse check.
- **“Decrease-key can accept any new key.”** A worsening key needs opposite repair or rejection.
- **“Removal always sifts down.”** The last entry may violate its parent edge.
- **“Generations never wrap.”** Width and reuse rate create a finite lifecycle that needs policy.
- **“Lazy duplicates preserve O(n) space.”** physical size follows update history until compaction.
- **“Meld just connects roots.”** comparator, stability, allocator, owner, and handle contracts must match.
- **“Donor handles obviously survive.”** survival, migration, or invalidation is an API choice.
- **“Binomial rank is generic tree height.”** rank has a precise recursive shape and `2^rank` size.
- **“Fibonacci operations are worst-case constant.”** the classical results quoted here are amortized.
- **“Potential is imaginary runtime.”** it is accounting that proves sequence work, not an implementation field or deadline.
- **“Pairing heap means one algorithm.”** delete-min and decrease variants have different analyses.
- **“Minus infinity always exists.”** generic key domains may lack a safe distinguished minimum.
- **“A structural validator proves ownership.”** cycles, double frees, stale registries, and donor semantics need lifecycle evidence.
- **“Asymptotics select production code.”** locality, allocation, operation mix, latency, and implementation risk remain decisive.

## Worked Examples

### Example 1

Handles 11 and 24 occupy indices 2 and 7. A sift swaps the entries but updates only `position[11]`. Both heap order and one map lookup may appear valid, yet handle 24 now targets handle 11's entry. Conclusion: a swap atomically updates both inverse entries.

### Example 2

Removing index 3 replaces key 9 with last key 2; the parent key is 4 and children are 10 and 12. Downward repair stops immediately while `4<=2` fails. Conclusion: arbitrary replacement must test the parent and may sift upward.

### Example 3

A stale handle `(slot=5,generation=8)` survives removal. Slot 5 is reused at generation 9. Comparing both fields rejects the old handle; comparing only slot silently mutates the new item. Conclusion: identity includes a reuse epoch.

### Example 4

One live task is reprioritized 100,000 times using lazy reinsertion. Logical size is one; physical size is 100,001 until stale roots are discarded or rebuilt. Conclusion: lazy update needs physical/live telemetry and bounded compaction.

### Example 5

Two stable queues both begin sequence counters at zero. Melding their `(priority,sequence)` keys creates ties whose cross-queue order is accidental. Conclusion: stable meld requires disjoint epochs or explicit renumbering/order policy.

### Example 6

A leftist node has right rank 4. The rank-size lemma implies at least `2^5-1=31` nodes in its subtree when the node rank is 5. Conclusion: the right spine cannot exceed logarithmic length.

### Example 7

Binomial heaps with occupied ranks `{0,2,3}` and `{0,1,3}` meld. Rank 0 links into a rank-1 carry; together with the existing rank 1 it creates rank 2, and carries continue exactly like binary addition. Conclusion: union work is bounded by the number of logarithmic ranks.

### Example 8

After many Fibonacci inserts, one delete-min may scan and consolidate many roots. The earlier inserts increased root potential; consolidation reduces it and pays for links. Conclusion: constant amortized insert does not cap delete-min's actual latency.

### Example 9

A pairing heap delete-min pairs adjacent children left-to-right and folds results right-to-left. A one-pass left fold creates a different variant and may have a different proof. Conclusion: implementation schedule is part of the theorem.

### Example 10

A workload performs one meld per million pops. A node-based meldable heap saves little union work but pays pointer/allocation/cache cost on every pop; array concatenate-plus-heapify at the rare boundary wins. Conclusion: optimize the observed operation vector, not the rare operation's asymptotic column alone.

## Cross-Program Connections

- **Algorithm engineering:** shortest paths, spanning trees, event simulation, k-way merge, and selection translate graph/event operations into queue-operation vectors.
- **Programming languages:** opaque types, generations, ownership, borrowing, exceptions, allocator propagation, and comparator laws shape safe handles and meld.
- **Concurrent programming:** two-object lock ordering, linearization, donor transfer, cancellation races, relaxed minima, and reclamation extend sequential proofs.
- **Database engineering:** merge scheduling, buffer eviction, background compaction, transaction cancellation, and recovery require stable identity and bounded tails.
- **Data engineering:** partition-local queues, watermark/event scheduling, stale records, batch consolidation, and backpressure resemble meld and lazy reinsertion.
- **Computer architecture:** arrays favor cache locality; forests add pointer loads, allocation, metadata, and irregular branches.
- **Security engineering:** stale-handle confusion, cross-tenant owner collision, comparator abuse, malformed serialized cycles, and stale-entry amplification need limits.
- **Distributed systems:** merging independently ordered streams requires a global tie/epoch policy; a local structural meld does not create distributed consensus.

## References

1. Jean Vuillemin, [A Data Structure for Manipulating Priority Queues](https://www.cl.cam.ac.uk/teaching/1011/AlgorithII/1978-Vuillemin-queues.pdf), Communications of the ACM 21(4), 1978. Primary source for binomial queues, rank forests, union, and priority operations.
2. Michael L. Fredman and Robert E. Tarjan, [Fibonacci Heaps and Their Uses in Improved Network Optimization Algorithms](https://www.eecs.tufts.edu/~aloupis/comp260/lectures/fredman-tarjan-1987.pdf), Journal of the ACM 34(3), 1987. Primary source for lazy consolidation, cuts, potential analysis, and graph-algorithm bounds.
3. Michael L. Fredman, Robert Sedgewick, Daniel D. Sleator, and Robert E. Tarjan, [The Pairing Heap: A New Form of Self-Adjusting Heap](https://sedgewick.io/wp-content/themes/sedgewick/papers/1986Pairing.pdf), Algorithmica 1, 1986. Primary source for pairing, multipass variants, and the scope of the original analysis.
4. Stanford CS166, [Fibonacci Heaps](https://web.stanford.edu/class/archive/cs/cs166/cs166.1266/lectures/11/), 2026 course materials. Current academic derivation and amortization review tied to the primary paper.
5. Boost C++ Libraries, [Heap Concepts](https://www.boost.org/doc/libs/latest/doc/html/heap/concepts.html). Current official contracts for handles, update direction, stability, ordered iteration, capability flags, and generic merge.
6. Boost C++ Libraries, [`binomial_heap`](https://www.boost.org/doc/libs/latest/doc/html/doxygen/classboost_1_1heap_1_1binomial__heap.html). Current official binomial-heap operations, handles, merge, stability, and complexity contracts.
7. Boost C++ Libraries, [`fibonacci_heap`](https://www.boost.org/doc/libs/latest/doc/html/doxygen/classboost_1_1heap_1_1fibonacci__heap.html). Current official Fibonacci-heap mutation, lazy update, merge, handle, and complexity contracts.
8. Boost C++ Libraries, [`pairing_heap`](https://www.boost.org/doc/libs/latest/doc/html/doxygen/classboost_1_1heap_1_1pairing__heap.html). Current official pairing-heap interface, handles, merge, ordered iteration, and documented complexity.
9. Boost C++ Libraries, [`skew_heap`](https://www.boost.org/doc/libs/latest/doc/html/doxygen/classboost_1_1heap_1_1skew__heap.html). Current official skew-heap mutability, parent-pointer, stability, merge, and complexity options.
10. Go Project, [`container/heap`](https://pkg.go.dev/container/heap). Current official `Init`, `Fix`, `Remove`, index invariant, and swap-maintenance example for indexed array heaps.

## Exercises

### Exercise 1

Specify an indexed stable min-heap with opaque generational handles. Give representation invariants and prove insert, change-key, remove, and pop preserve them under successful execution.

### Exercise 2

Derive the leftist rank-size lemma and prove recursive meld has logarithmic worst-case time. Include empty, self-meld, ownership, and stack-depth behavior.

### Exercise 3

Trace binomial union for two explicit root-rank sets, then design validators for binomial and Fibonacci heaps that do not trust stored ranks, degrees, marks, sizes, or minimum pointers.

### Exercise 4

Compare indexed array, lazy reinsertion, leftist, binomial, Fibonacci, and pairing queues for Dijkstra, a real-time timer service, and a batch merge scheduler. Separate theorem, engineering inference, and measurement.

### Exercise 5

Design a concurrent destructive-meld API whose handles may survive transfer. Specify owner identity, lock ordering, failure atomicity, cancellation races, allocator/reclamation, serialization, and adversarial tests.

## Answers to the Exercises

### Answer 1

Store array entries `(key,sequence,slot,generation,payload)`, a slot registry containing current generation/live state/index, and monotone sequence state. Invariants are complete array shape, parent order on `(key,sequence)`, one live registry record per entry, both mapping directions, unique live `(slot,generation)`, and unique nonexhausted sequence keys. Insert reserves array/registry capacity, creates identity and sequence, appends, publishes the mapping, and uses a centralized swap that updates both positions. Change validates the complete handle, preserves sequence by policy, and sifts up if it precedes its parent, otherwise down. Remove invalidates the registry generation, fills from the last entry, repairs its mapping, and chooses direction; pop delegates to root removal. Each repair preserves the bijection because only the centralized swap moves entries. Successful completion preserves order by the one-violation proof. Define stale/missing errors and counter exhaustion. For failures, use rollback guards or state only a basic guarantee that still preserves every invariant and reports membership unambiguously.

### Answer 2

Let `rank(empty)=0`, `rank(x)=1+min(rank(left),rank(right))`, and enforce left rank at least right rank. Prove by induction that a rank-`r` node has at least `2^r-1` nodes: rank zero is empty; a rank-`r` node has both child ranks at least `r-1`, so size is at least `1+2(2^(r-1)-1)=2^r-1`. Thus rank and right-spine length are at most `log2(n+1)`. Meld returns the nonempty root at the base; otherwise choose the smaller root, recursively meld its right child with the other heap, swap children if needed, and set rank to right rank plus one. Induction preserves membership/order/rank; recursion visits two logarithmic right spines. Reject self-meld before linking, define destructive donor emptying, and either prove recursion fits maximum supported size or implement an explicit stack. Allocation-free node transfer still needs compatible ownership/reclamation.

### Answer 3

For example, union ranks `{0,2,4}` and `{0,1,4}` with a carry state. At rank 0, link two trees to carry rank 1. At rank 1, the input tree plus carry link to rank 2. At rank 2, the input tree plus carry link to rank 3. Emit rank 3; at rank 4 link the two inputs to rank 5. Result ranks are `{3,5}`, matching total size. A binomial validator traverses from roots, detects cycles/duplicate reachability, verifies parent and heap order, independently counts subtree size as `2^rank`, derives degree/rank from child ranks, and checks unique increasing root ranks and total size. A Fibonacci validator checks circular-list next/previous symmetry, unique reachability, parent pointers, heap order, child count equals degree, roots unmarked by convention, mark validity, recomputed minimum, total size, and a logarithmic-degree consequence from valid cut/mark history. Structural validation alone cannot prove historical marking discipline, so operation histories and a reference model must accompany it.

### Answer 4

Dijkstra with many successful decreases is a candidate for indexed d-ary or Fibonacci heaps: the former offers compact predictable logarithmic repair; the latter supplies the classical `O(m+n log n)` amortized bound but more complex nodes. Lazy reinsertion may be simplest and competitive when decreases are sparse, but measure peak stale size. A real-time timer service favors bounded per-operation latency and simple cancellation—often an indexed array heap or hierarchical/bucket timer under bounded timestamps—not classical Fibonacci amortization. A batch merge scheduler with frequent similarly sized unions may favor leftist, binomial, or pairing structures; rare merges may favor arrays plus heapify. Theorems provide operation bounds under models. Engineering inference predicts locality, allocation, and risk. Measurement must record real operation/operand sizes, key/tie distribution, memory, cache/branches, failures, concurrency, and p99/p999 latency. Do not claim a winner beyond the reproduced regime.

### Answer 5

Give every queue a stable owner ID and every handle `(owner,slot,generation)`. `meld(receiver,donor)` rejects self-meld and incompatible comparator/stability/allocator policies, locks queues in ascending owner-ID order, prepares any registry capacity, structurally merges, migrates donor registry entries to receiver, and either rewrites handle owner through an indirection registry or preserves a lineage table that routes old owner IDs. Only after all fallible preparation succeeds does one commit point publish the receiver root/registry and donor-empty state. Cancellation and pop under the same locks decide by live generation; exactly one wins. Nodes retain allocator provenance or use a compatible shared resource; reclamation waits for outstanding operations/handles under reference counting, epochs, or another proved scheme. Serialization records logical entries, stable keys, owner lineage, generations, and comparator version, then rebuilds and validates. Test empty/nonempty and size-skew melds, self/dead donor, owner/handle collisions, counter exhaustion, injected failure before every commit step, opposite-direction concurrent meld, cancel/pop/meld races, crash/restart boundaries, malformed cycles, stale handles, and leak/double-free detection.
