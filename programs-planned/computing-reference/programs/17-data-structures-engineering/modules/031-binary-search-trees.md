---
module_id: DSE-031
program: Data Structures Engineering
level: 1
module_number: 31
title: Binary Search Trees
status: complete
last_verified: 2026-08-30
---

# Binary Search Trees

## One-Page Review

### Governing question

How can a binary search tree implement an ordered map correctly—including search, update, bounds, traversal, and all deletion cases—while making its comparator, height, node identity, lifetime, and degeneration limits explicit?

### Essential definitions

- A **binary tree** has at most a left and right child per node; a **binary search tree (BST)** adds an ordering invariant.
- For a unique-key map under comparator `<`, every key in node `x`'s left subtree is strictly less than `x.key`, and every key in its right subtree is strictly greater.
- **comparator equivalence** means neither `a<b` nor `b<a`; the map must decide whether that denotes one logical key.
- **height** `h` is the number of nodes on the longest root-to-leaf path here; an empty tree has height zero.
- **search path** is the root-to-null/node sequence selected by repeated comparison.
- **successor** is the least key greater than a key/node; **predecessor** is the greatest smaller key/node.
- **lower bound** is the first key not less than a query; **upper bound** is the first key greater.
- **transplant/splice** replaces one subtree link while preserving parent/root ownership.
- **Hibbard deletion** replaces a two-child node using its in-order successor (or symmetrically predecessor) and removes that successor from its old location.
- An **in-order traversal** visits left subtree, node, then right subtree and therefore yields sorted keys when the invariant holds.

### Central model, mechanism, or theorem

Search compares query `q` with each visited node: go left if `q<x.key`, right if `x.key<q`, and treat the remaining comparator-equivalent case according to the duplicate policy. The BST invariant proves the discarded subtree cannot contain `q`. Search, insert, delete, min/max, predecessor/successor, and bounds use `O(h)` comparisons/pointer steps; traversal is `Theta(n)` plus `O(h)` auxiliary stack without parent links.

Deletion has three structural cases. A leaf becomes null. A one-child node is replaced by its child. For two children, let `s=min(x.right)`. Then every key in `x.left` is `<x.key<s.key`, and no key in `x.right` is between `x.key` and `s.key`; removing `s` from the right subtree and placing its key/value (or node) at `x` preserves order. The proof must also preserve root/parent links, count, payload lifetime, exception behavior, and any promised node identity.

Nothing in the plain invariant bounds height. Sorted insertion can form a chain with `h=n`, making operations linear and recursive implementations vulnerable to call-stack exhaustion. Balanced trees in later modules strengthen the representation so `h=O(log n)` under their own proofs.

### Critical invariants

1. The root is null or owned exactly once; every reachable non-root node has exactly one parent/link and there are no cycles or shared subtrees.
2. Every key lies strictly within the lower/upper bounds inherited from all ancestors, not merely its immediate parent.
3. Comparator equivalence implements the declared duplicate/update policy consistently across insert, lookup, erase, bounds, and serialization.
4. `size` equals the number of reachable initialized nodes; each key/value is constructed and destroyed exactly once.
5. Child/parent links, cached sizes/heights if any, minimum caches, and iterator state agree after every transplant.
6. Search and traversal terminate even for degenerate height; iterative paths or explicit limits protect untrusted depth.
7. Mutations provide the promised iterator/reference/node-handle invalidation and failure guarantee.
8. Complexity claims use measured/derived height rather than assuming balance.

### Common failures

- Checking only `left.key < node.key < right.key` instead of bounds over entire subtrees.
- Using equality inconsistent with comparator equivalence, creating duplicate or unreachable logical keys.
- Sending comparator-equivalent keys arbitrarily left/right without a documented multimap policy.
- Losing a subtree, parent pointer, or root update during one/two-child deletion.
- Copying successor payload into a node while promising stable identity for key-associated handles.
- Detaching the successor but forgetting its right child.
- Updating `size` twice or not at all across recursive deletion returns.
- Calling every operation `O(log n)` although an unbalanced BST only guarantees `O(h)` and worst-case `O(n)`.
- Recursing through attacker-created sorted input until stack overflow.
- Traversing with a live stack while concurrent mutation frees or rotates nodes without a contract.

### Compact example

Insert `8,3,10,1,6,14,4,7,13`. In-order traversal is `1,3,4,6,7,8,10,13,14`, and height is four. Update key 6 without changing size. Delete leaf 7; delete one-child node 14 by promoting 13; delete two-child node 3 by detaching successor 4 from its right subtree and copying that association into node 3's position. The final sorted keys are `1,4,6,8,10,13`, size six, height three, and the executable checker verifies global bounds and exact count.

### Connections

[DSE-001](001-abstract-data-types-and-concrete-representations.md) through [DSE-009](009-property-based-testing-of-data-structures.md) provide representation, lifetime, iterator, and testing discipline. Hash maps in [DSE-021](021-hash-functions-and-distribution.md) through [DSE-030](030-engineering-a-memory-efficient-hash-map.md) trade order for expected lookup. The [program roadmap](../ROADMAP.md) next adds AVL, red-black, randomized, adaptive, augmented, and heap structures.

## Governing Question

Which ordered-map semantics, comparator law, node representation, search-path proof, deletion strategy, iterator contract, failure guarantee, and height policy make a BST correct and usable as the baseline for balanced search trees?

## Why This Matters

An ordered map supports more than exact lookup. Minimum/maximum, predecessor/successor, lower/upper bounds, sorted iteration, and range traversal emerge from one structural invariant. Hash tables do not naturally provide these operations, while a sorted array makes insertion/deletion expensive. The BST is the conceptual bridge: it turns comparison order into navigable links.

It is also a compact case study in data-structure proof. Search correctness depends on global ancestor bounds. Deletion rewires ownership in three cases and forces a choice about node versus association identity. Iteration relies on the same invariant through a different path. Complexity depends on shape, so input history becomes part of the cost model.

Plain BSTs are rarely the final general-purpose production choice because they can degenerate. Yet AVL, red-black, treap, splay, order-statistic, interval, and many intrusive kernel trees all preserve a BST order relation while adding structure. If the unbalanced baseline is vague, later rotations and augmentations cannot be proved.

## Prerequisites and Retrieval

Retrieve abstract/concrete representation, global invariants, operation contracts, cost vectors, linked layout, ownership, generic comparators, iterators, and property testing from [DSE-001](001-abstract-data-types-and-concrete-representations.md) through [DSE-009](009-property-based-testing-of-data-structures.md). Contrast sorted arrays and linked structures from [DSE-011](011-fixed-arrays.md) through [DSE-015](015-doubly-and-intrusive-linked-lists.md). Retrieve evidence discipline from [DSE-010](010-benchmarking-a-structure-without-misleading-results.md).

## Learning Objectives

After completing this module, you should be able to:

1. state the BST invariant using ancestor-derived open bounds;
2. specify a strict ordering/comparator-equivalence and duplicate/update policy;
3. derive search, insert, min/max, predecessor/successor, and lower/upper-bound algorithms;
4. implement and prove leaf, one-child, and two-child deletion;
5. choose between payload-copy and node-transplant deletion under identity/lifetime contracts;
6. implement in-order iteration using recursion, an explicit stack, or parent pointers;
7. prove operation costs in `O(h)` and construct best/degenerate shapes;
8. handle allocation/comparator/payload failure without corrupting links or counts;
9. test global order, reachability, uniqueness, size, traversal, and model equivalence;
10. decide when a plain BST, balanced tree, sorted vector, skip list, or hash map fits the workload.

## Core Exposition

**Specify an ordered-map abstraction first.** A unique-key ordered map associates one value with each comparator-equivalence class. `put(k,v)` either inserts a new class or updates the existing value. `get/erase` use the same equivalence. `lower_bound(q)` returns the least stored key `k` for which `k<q` is false; `upper_bound(q)` returns the least `k` for which `q<k` is true. A multimap needs a separate duplicate placement and stable-range policy.

The comparator must act as a strict weak ordering over all admitted keys/borrowed queries: irreflexive, asymmetric, transitive, with transitive equivalence classes. If `a` and `b` compare equivalent but the map's external equality says they are different, decide whether the ordered-map contract treats them as one key. OpenJDK's current `TreeMap` documentation explicitly warns that comparator order inconsistent with `equals` does not satisfy the general `Map` contract even though tree behavior can remain defined.

Comparators may be generic callbacks. They can throw, allocate, recurse into the map, depend on mutable locale/state, or observe keys that later mutate. A key whose order changes while stored breaks reachability. Production APIs normally require stable ordering and prohibit structural reentrancy during mutation. Test heterogeneous lookup so stored and borrowed comparators induce compatible equivalence.

**The invariant is global.** For each node `x`, every key in `x.left` is less than `x.key`, and every key in `x.right` is greater. A checker should pass an open lower and upper bound down the recursion/stack. Checking only immediate children accepts an invalid tree such as root 10, left child 5, and 5's right child 12: `12>5` locally, but 12 violates the root's left-subtree bound.

The ownership invariant is independent: the root owns a finite acyclic graph in which each non-root node is reached from exactly one child link. If parent pointers exist, they must be inverse to child links. `size` is the reachable node count. Cached subtree size, height, min/max, balance, interval maximum, or other augmentation adds equations later modules must update on every changed ancestor.

**Search is interval refinement.** Begin at root with bounds `(-infinity,+infinity)`. At node `x`, compare `q` and `x.key`. If `q<x.key`, the right subtree and `x` cannot contain an equivalent key; continue left and tighten upper bound to `x.key`. If `x.key<q`, continue right and tighten lower bound. Otherwise the keys are comparator-equivalent.

The path ends at the matching node or a null child where insertion belongs. With `h` nodes on the longest root-leaf path, search visits at most `h` nodes and uses `O(1)` auxiliary state iteratively. Expensive comparison/key access multiplies that count. Cache misses and pointer chasing differ from binary search over a packed array.

**Insertion reuses the failed search.** Track the last non-null node and comparison direction. Construct/allocate the new node only under a failure protocol: comparison should complete before link publication, and allocation/payload construction failure leaves the tree unchanged. Link it into the unique null position, set parent if used, then increment size/update augmentations.

If a comparator-equivalent node exists, update its value according to API semantics without allocating a duplicate node. Value assignment may fail; specify whether the old value is preserved, partially modified, or replaced through construct-then-swap. Structural modification counters should not advance for a pure value update unless the iterator contract says otherwise.

Sorted insertion `1,2,...,n` creates only right children, so `h=n`. A favorable insertion order can create height near `floor(log2 n)+1`. “Average `O(log n)`” requires a distribution over insertion orders/keys and is not a worst-case contract. Adversaries and already-sorted data invalidate casual randomness assumptions.

**Minimum, maximum, and bounds follow monotone paths.** Minimum repeatedly follows left links; maximum follows right, each `O(h)`. For lower bound, retain a candidate. If current key is not less than query, it may be the answer; record it and go left for a smaller qualifying key. Otherwise go right. Upper bound is analogous using `query<current`.

The successor of node `x` is minimum of `x.right` when it exists. Otherwise ascend parent links until leaving a left edge; that ancestor is next. Without parents, an iterator/search can retain ancestors on a stack. Predecessor is symmetric. These algorithms prove navigation without materializing all keys.

Range iteration begins at `lower_bound(lo)` and advances successor until the upper predicate fails, giving `O(h+k)` pointer/comparison work for `k` reported entries in a plain model. If keys mutate or the tree changes concurrently, saved ancestors/nodes may be stale. Document fail-fast, snapshot, lock-held, versioned, or unsupported mutation semantics.

**Deletion exposes the representation contract.** Find target `x`. With no left child, replace the parent/root link to `x` with `x.right`; with no right child, replace it with `x.left`. The replacement child's parent becomes `x.parent` when parent links exist. Only after publication/ownership transfer can `x` be destroyed.

With two children, choose successor `s=min(x.right)`. Because `s` is minimum, it has no left child. Its right child, if any, must be connected where `s` was removed. There are two main implementation families.

**Association-copy deletion** copies/moves `s.key,s.value` into `x`, then deletes `s`. It rewires fewer tree links and is the executable strategy. But a handle to node `x` now denotes a different key, a handle to `s` dies, key assignment may be forbidden/throw, and identity-sensitive intrusive/augmented state complicates copying. This is not valid if the API promises that a node object remains bound to its original association.

**Node-transplant deletion** physically moves `s` into `x`'s position. If `s.parent!=x`, first replace `s` with `s.right`, attach `s.right=x.right`, then attach `s.left=x.left` and connect `s` to `x.parent/root`. Update every parent pointer and augmentation in the right order. Node identity for `s` survives, but a handle to erased `x` still invalidates, and more links are touched.

The ordering proof is the same: all left keys are `<x.key<s.key`; after removing the minimum `s` from the original right subtree, all remaining right keys are `>s.key`. The structural/lifetime proof differs. State which one is implemented.

Some designs alternate predecessor/successor or choose randomly to reduce deletion bias, but a plain BST still has no worst-case height bound. Hibbard deletion's historical name does not create balancing. DSE-032 and DSE-033 add invariants and rotations that bound height.

**Iteration is a proof oracle.** Recursive in-order traversal is concise: traverse left, visit, traverse right. It uses `O(h)` call stack and can overflow on a degenerate tree. An explicit stack makes resource use visible: push the left spine, pop/visit, then push the right child's left spine. Parent links permit successor iteration with `O(1)` extra state and amortized linear traversal, but each node pays a parent pointer and mutations update it.

Morris traversal temporarily threads null links to obtain constant auxiliary space. It mutates representation, complicates concurrency/failure/cancellation, and must restore every link; it is rarely the default for a mutable production map. A stack is easier to audit.

Iteration yields sorted comparator order, not insertion order and not necessarily external `equals` order. Stable ordering among comparator-equivalent duplicates requires a secondary key/sequence or per-key collection. Serialization should write logical sorted associations plus comparator/schema identity where meaningful, not raw pointers or tree shape unless shape is a validated format requirement.

**Recursion is a resource decision.** Recursive search/insert/delete/check/traversal have stack depth `Theta(h)`. With untrusted sorted inserts, this is `Theta(n)` and can exceed the language stack before heap limits. Iterative search/insert are straightforward. Iterative deletion uses parent/link references; iterative post-order destruction needs an explicit stack, parent links, or a safe rotation/threading scheme.

If recursion remains, enforce a node/depth limit, balance the tree, or guarantee trusted small inputs. Tail-call optimization is not portable and two-child deletion/check/traversal are not generally a simple tail chain. Catching a recursion error after partial mutation is not failure atomicity.

**Ownership and allocation shape real cost.** A classic node contains key, value, two child pointers, optionally parent, allocator header/padding, and augmentations. Each operation pointer-chases and allocates/frees individually. Intrusive nodes embed links in domain objects, avoiding a wrapper allocation and enabling stable identity; users own lifetime and must remove nodes before destruction/reuse. The current Linux rbtree documentation illustrates embedded nodes and caller-owned comparison/locking for a balanced production tree.

Pool/arena allocation improves locality and bulk release but changes individual erase reclamation and retained memory. Compact child offsets reduce pointer width only within a checked arena span. Array-indexed trees can improve locality but relocation changes handles. These representation decisions do not change the BST theorem, but they change failure, stability, and memory.

Destroying a deep tree recursively can overflow. An arena may release bytes in bulk, but payload destructors/resources may still need visitation. Garbage collection avoids explicit node frees but cycles/retained iterators and comparator closures can retain the graph. Define ownership for keys, values, comparator, nodes, iterators, and views.

**Concurrency is not implied.** A lookup racing deletion can dereference freed nodes; insertion can publish an uninitialized child; two-child deletion changes several links; iterators can miss/repeat entries. A mutex around all operations is the simplest linearizable design. Reader/writer locks, copy-on-write persistent trees, lock coupling, optimistic validation, and lock-free BSTs each need separate proofs and reclamation.

OpenJDK's current `TreeMap` explicitly requires external synchronization for structural concurrent access and uses a modification counter for best-effort fail-fast iteration. Linux's rbtree leaves locking to callers. These are distinct contracts. Do not infer thread safety from a tree's sorted shape.

**Testing starts with a reference ordered model.** Generate put/update/get/erase/lower/upper/range operations and compare logical results with a sorted reference sequence/map. After every mutation assert global bounds, reachability/no cycles, unique equivalence classes, exact size, parent inverses, augmentation equations, and in-order strict ordering.

Force every deletion topology: root/non-root leaf; only-left/only-right; two children with successor equal to immediate right; successor deep with/without right child; minimum/maximum; singleton; missing key. Test comparator-equivalent distinct objects, inconsistent/mutating comparator rejection, allocation and value-copy failure, iterator invalidation, clear/drop, serialization, and maximum depth.

Metamorphic properties help: in-order keys equal sorted reference keys; inserting a new then erasing it restores content; updating preserves keys/size; lower/upper partition the sequence; min/max agree with endpoints; deletion removes one equivalence class; building sorted keys exposes height `n`; mirrored comparator/tree gives symmetric results.

Benchmark with measured height. Sweep random, sorted, reverse, organ-pipe, duplicate/equivalent, partially sorted, and adversarial sequences; sizes; key/value/comparator costs; hits/misses/bounds/ranges; update/delete mixes; allocator/node layout; cache/NUMA; and iteration. Report height distribution, comparisons, allocations, bytes, cache/TLB misses, throughput, p50/p95/p99/max, repetitions, uncertainty, versions, and raw artifacts. Compare balanced trees and sorted arrays rather than presenting plain BST results as an ordered-map recommendation.

The executable trace below implements a sequential unique-key integer BST using association-copy deletion. It validates global open bounds and reachable count after every mutation, exercises update and all three deletion shapes, and records exact output. It does not implement parent pointers, generic failing comparators, stable node handles, balancing, concurrency, or production memory management.

<!-- bijux-verify: {"id":"bst-mutation-invariant-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"before=1,3,4,6,7,8,10,13,14\ndeleted_leaf=SEVEN\ndeleted_one_child=FOURTEEN\ndeleted_two_children=THREE\nlookup_six=SIX_UPDATED\nafter=1,4,6,8,10,13\nroot=8\nsize=6\nheight=3\ninvariant=True\nevidence=finite_bst_mutation_trace\n","stderr":""}} -->
```python
from dataclasses import dataclass


@dataclass
class Node:
    key: int
    value: str
    left: object = None
    right: object = None


class BinarySearchTree:
    def __init__(self):
        self.root = None
        self.size = 0

    def put(self, key, value):
        link = self.root
        parent = None
        while link is not None:
            parent = link
            if key < link.key:
                link = link.left
            elif link.key < key:
                link = link.right
            else:
                link.value = value
                return False
        node = Node(key, value)
        if parent is None:
            self.root = node
        elif key < parent.key:
            parent.left = node
        else:
            parent.right = node
        self.size += 1
        return True

    def get(self, key):
        node = self.root
        while node is not None:
            if key < node.key:
                node = node.left
            elif node.key < key:
                node = node.right
            else:
                return node.value
        raise KeyError(key)

    @staticmethod
    def detach_min(node):
        if node.left is None:
            return node, node.right
        minimum, node.left = BinarySearchTree.detach_min(node.left)
        return minimum, node

    def delete(self, key):
        removed = []

        def erase(node):
            if node is None:
                raise KeyError(key)
            if key < node.key:
                node.left = erase(node.left)
            elif node.key < key:
                node.right = erase(node.right)
            else:
                removed.append(node.value)
                if node.left is None:
                    return node.right
                if node.right is None:
                    return node.left
                successor, remaining = self.detach_min(node.right)
                node.key, node.value = successor.key, successor.value
                node.right = remaining
            return node

        self.root = erase(self.root)
        self.size -= 1
        return removed[0]

    def keys(self):
        result = []
        stack = []
        node = self.root
        while node is not None or stack:
            while node is not None:
                stack.append(node)
                node = node.left
            node = stack.pop()
            result.append(node.key)
            node = node.right
        return result

    def height(self):
        def visit(node):
            if node is None:
                return 0
            return 1 + max(visit(node.left), visit(node.right))
        return visit(self.root)

    def invariant(self):
        seen = set()

        def check(node, lower, upper):
            if node is None:
                return 0
            if id(node) in seen:
                raise AssertionError("cycle or shared node")
            seen.add(id(node))
            if lower is not None and not lower < node.key:
                raise AssertionError("lower bound")
            if upper is not None and not node.key < upper:
                raise AssertionError("upper bound")
            return 1 + check(node.left, lower, node.key) + check(
                node.right, node.key, upper
            )

        try:
            return check(self.root, None, None) == self.size
        except AssertionError:
            return False


tree = BinarySearchTree()
for key, value in (
    (8, "EIGHT"), (3, "THREE"), (10, "TEN"), (1, "ONE"),
    (6, "SIX"), (14, "FOURTEEN"), (4, "FOUR"), (7, "SEVEN"),
    (13, "THIRTEEN"),
):
    assert tree.put(key, value)
assert not tree.put(6, "SIX_UPDATED")
before = tree.keys()
assert tree.invariant()
deleted_leaf = tree.delete(7)
assert tree.invariant()
deleted_one_child = tree.delete(14)
assert tree.invariant()
deleted_two_children = tree.delete(3)

print("before=" + ",".join(map(str, before)))
print(f"deleted_leaf={deleted_leaf}")
print(f"deleted_one_child={deleted_one_child}")
print(f"deleted_two_children={deleted_two_children}")
print(f"lookup_six={tree.get(6)}")
print("after=" + ",".join(map(str, tree.keys())))
print(f"root={tree.root.key}")
print(f"size={tree.size}")
print(f"height={tree.height()}")
print(f"invariant={tree.invariant()}")
print("evidence=finite_bst_mutation_trace")
```

## Definitions and Notation

- `n`: reachable live nodes/unique comparator-equivalence classes.
- `h`: node-height of the tree; empty height zero, leaf height one.
- `x.left,x.right,x.parent`: child/optional parent links.
- `lower,upper`: open ancestor-derived bounds for a subtree.
- `a~b`: comparator equivalence, neither `a<b` nor `b<a`.
- **search path**: comparison-selected root-to-node/null path.
- **transplant**: replace one parent/root subtree link with another subtree.
- **association-copy deletion**: keep target node object but replace its key/value from successor/predecessor.
- **node-transplant deletion**: move successor/predecessor node object into target position.
- **structural modification**: mutation changing the reachable node/link set rather than only a value.

## Mechanisms, Invariants, or Proof Structure

Search correctness follows interval refinement: the BST invariant excludes one subtree after each strict comparison, and equivalence identifies the unique map key. Insert publishes one node at the null endpoint; update preserves structure. Bounds retain the best qualifying ancestor while descending.

Deletion is proved by cases. Null-child replacement preserves ancestor bounds because the promoted subtree already satisfied the deleted node's interval. For two children, successor is the right-subtree minimum, has no left child, lies above every left key, and below every remaining right key after detachment. Structural proof additionally covers root/parent links, count, node identity, and exact payload lifetime.

Every path operation is `O(h)`; traversal is `Theta(n)` with `O(h)` stack or parent-link successor. The plain invariant permits `h=n`, so logarithmic worst-case claims require the balancing invariants introduced later.

## Alternatives and Trade-Offs

| Design choice | Strength | Cost or obligation |
|---|---|---|
| Plain unbalanced BST | minimal mechanism; excellent proof baseline | worst-case height `n` |
| Parent pointers | successor and iterators with small state | pointer bytes and mutation updates |
| Explicit traversal stack | no per-node parent pointer | `O(h)` iterator memory/invalidation |
| Association-copy delete | fewer link rewrites | changes target association identity; copying may fail |
| Node-transplant delete | preserves successor node identity | more rewiring/augmentation repair |
| Intrusive nodes | removes wrapper allocation/indirection | caller owns lifetime/link membership/locking |
| Arena/pool nodes | locality and bulk allocation | retained slabs and reclamation policy |
| Balanced BST | logarithmic height guarantee | rotations/colors/heights and stronger proof |
| Sorted vector | compact iteration and binary search | `O(n)` middle mutation/invalidation |
| Hash map | expected fast equality lookup | no native sorted/bound/range order |

## Failure Modes and Misconceptions

- **“Children ordered means valid BST.”** descendants must obey every ancestor bound.
- **“Comparator equality equals object equality.”** the API must define and enforce the relationship.
- **“Duplicates can always go right.”** rotations/search/bounds need a durable duplicate policy.
- **“BST operations are logarithmic.”** only `O(h)` is guaranteed without balance.
- **“Two-child deletion just copies the successor.”** the successor and its right child must be detached correctly.
- **“Copying preserves handles.”** the node survives but changes which association it denotes.
- **“Recursive code is harmless.”** sorted input can create depth `n` and exhaust the stack.
- **“In-order is sorted by equality.”** it is sorted by the comparator's equivalence/order.
- **“Parent links are redundant.”** they trade per-node bytes for navigation/iterator state and require inverse-link invariants.
- **“Garbage collection solves lifetime.”** it does not define mutation races, retained iterators, or logical ownership.
- **“Fail-fast means thread-safe.”** detecting some modifications is neither synchronization nor linearizability.
- **“Hibbard deletion balances.”** it preserves order but supplies no worst-case height bound.

## Worked Examples

### Example 1

Root 10 has left child 5 whose right child is 12. Immediate parent comparisons pass at node 5, but 12 violates the inherited upper bound 10. Conclusion: validation carries ancestor bounds.

### Example 2

Searching 7 in root 8, left 3, right 6, right 7 discards the right subtree at 8 and left subtree at 3/6 by invariant. Conclusion: comparisons refine a feasible interval.

### Example 3

Inserting keys 1 through 8 yields a right chain of height eight. Conclusion: plain BST worst case is linear and recursion depth is input-controlled.

### Example 4

Updating the value at comparator-equivalent key 6 changes neither node count nor shape. Conclusion: ordered-map duplicate policy is part of insertion.

### Example 5

Deleting leaf 7 replaces its parent's right link with null and decrements size once. Conclusion: leaf deletion is the zero-child transplant.

### Example 6

Node 14 has only left child 13. Deleting 14 promotes 13 into the inherited `(10,+infinity)` interval. Conclusion: one-child promotion preserves ancestor bounds.

### Example 7

Deleting node 3 with children 1 and 6 chooses successor 4, detaches it from 6's left link, and places association 4 at node 3. Conclusion: successor can be deeper than the immediate right child.

### Example 8

For lower bound 5 in keys `4,6,7,8`, node 6 becomes candidate and search continues left; absent a closer qualifier, return 6. Conclusion: bounds retain candidates instead of exact-match-only search.

### Example 9

An iterator stack contains ancestors of node 7; another thread deletes and frees one. Conclusion: sorted traversal needs a mutation/lifetime contract, not just an algorithm.

### Example 10

Two strings compare equivalent case-insensitively but are unequal bytewise. Inserting both into a unique ordered map updates one equivalence class if that is its declared policy. Conclusion: comparator equivalence owns key identity for ordered navigation.

## Cross-Program Connections

- **Algorithms:** divide-by-order search, height-sensitive analysis, traversal, sorting, and successor deletion are foundations for balanced/augmented trees.
- **Programming languages:** generic comparator laws, exceptions, moves, ownership, intrusive links, iterators, and destructors govern implementation correctness.
- **Software engineering:** ordered-map semantics, invalidation matrices, serialization, observability, and typed failures prevent hidden contract drift.
- **Concurrent programming:** link publication, structural races, locks, versions, and reclamation are required for shared mutable trees.
- **Computer architecture:** node size, pointer chasing, allocator locality, cache/TLB behavior, and branch prediction shape real cost.
- **Database engineering:** search trees lead to B-trees/indexes; bounds and ordered scans are direct conceptual predecessors.
- **Security engineering:** adversarial sorted input, comparator/equality bombs, recursion depth, allocation, and serialized-shape validation are resource surfaces.

## References

1. MIT OpenCourseWare 6.006, [Lecture 5: Binary Search Trees, BST Sort](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/resources/lecture-5-binary-search-trees-bst-sort/). Primary academic lecture for the BST invariant, search, insertion, minimum, successor, and height-dependent operations.
2. Robert Sedgewick and Kevin Wayne, [Binary Search Trees](https://algs4.cs.princeton.edu/32bst/). Primary course text/code for ordered symbol-table operations, traversal, range queries, deletion-min, and Hibbard deletion.
3. Pat Morin, [Open Data Structures: Binary Search Trees](https://opendatastructures.org/ods-python/6_2_BinarySearchTree_Unbala.html). Open academic treatment of unbalanced BST search/add/remove/splice and height-sensitive cost.
4. Software Foundations, [Search Trees](https://softwarefoundations.cis.upenn.edu/vfa-current/SearchTree.html). Mechanized-verification-oriented treatment of BST abstraction, lookup/insert, representation invariant, and correctness.
5. ISO C++ working draft, [Algorithms library ordering requirements](https://eel.is/c%2B%2Bdraft/alg.sorting). Current strict-weak-order and induced-equivalence requirements used to scope generic comparator laws.
6. ISO C++ working draft, [Associative container requirements](https://eel.is/c%2B%2Bdraft/associative.reqmts). Current ordered associative-container key equivalence, complexity, iterator, insertion, erase, and node-handle contracts.
7. Rust Project, [`std::collections::BTreeMap`](https://doc.rust-lang.org/std/collections/struct.BTreeMap.html). Current ordered-map API for iteration, ranges, entries, allocation failure, and key-order consistency; cited as a balanced production contrast.
8. OpenJDK Project, [`TreeMap.java`](https://github.com/openjdk/jdk/blob/master/src/java.base/share/classes/java/util/TreeMap.java). Current primary source for comparator/equality caveats, navigation, deletion, fail-fast modification tracking, and external synchronization; cited as a red-black contrast.
9. Linux Kernel, [Red-black Trees](https://docs.kernel.org/core-api/rbtree.html). Current official documentation for intrusive node embedding, caller-owned comparison/locking, search, insertion, erase, and ordered iteration.
10. MIT OpenCourseWare 6.006, [Lecture 6: Balanced Binary Search Trees](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/83cdd705cd418d10d9769b741e34a2b8_MIT6_006F11_lec06.pdf). Primary academic contrast establishing why an additional balancing invariant is needed beyond the plain BST baseline.

## Exercises

### Exercise 1

Specify a unique-key ordered-map comparator contract and prove iterative search, insertion/update, lower bound, and upper bound correct using ancestor intervals.

### Exercise 2

Implement deletion using both association-copy and physical node transplant. Prove all structural cases and compare node-handle, iterator, payload-failure, parent-link, and augmentation consequences.

### Exercise 3

Implement stack-based in-order/range iteration and parent-pointer successor iteration. Derive time/space and specify behavior under value updates, structural mutation, cancellation, and concurrent access.

### Exercise 4

Design ownership, allocation, recursion-depth, failure, serialization, observability, and resource-limit policies for a BST receiving untrusted keys and comparators.

### Exercise 5

Design property, metamorphic, fault, lifetime, adversarial, concurrency, and benchmark evidence comparing a plain BST with a balanced tree, sorted vector, and hash map.

## Answers to the Exercises

### Answer 1

Require a stable strict weak order `<`; define key equivalence as `!(a<b)&&!(b<a)` and unique-map update on equivalence. Search maintains open bounds `(L,U)` containing all possible matches. At node x, `q<x` excludes x/right and tightens U; `x<q` excludes x/left and tightens L; equivalence returns x. Null proves absence. Insert links one constructed node at that null endpoint, so it satisfies inherited bounds; equivalence updates value/size unchanged. Lower bound stores x when `!(x<q)` and goes left for a smaller qualifier, otherwise right; upper bound stores x when `q<x`. On termination, discarded subtrees prove no closer qualifying key exists. Each visits at most h nodes.

### Answer 2

Leaf deletion installs null; one-child deletion installs the child into the deleted node's inherited interval. For two children, successor s is right-subtree minimum, has no left child, exceeds every left key, and is below every remaining right key after removal. Association-copy assigns s's association into x then splices s.right at s's old link; x identity survives but changes key, s identity dies, and assignment can fail. Node transplant first replaces s by s.right when non-immediate, then attaches x.right/x.left and x.parent/root to s, repairing every inverse parent and augmentation; s identity survives and x dies. Both decrement size exactly once and preserve root/order, but invalidation and failure strategies differ. Construct-then-swap or physical transplant may be required for strong guarantees/nonassignable keys.

### Answer 3

Stack iteration pushes a left spine, pops/visits, then pushes the right child's left spine. Every node is pushed/popped once: Theta(n) full traversal, O(h) state; starting at lower bound and stopping at upper gives O(h+k). Parent-pointer successor uses right minimum or ascends until leaving a left edge, O(h) worst per step but O(n) total traversal and O(1) iterator state, while every mutation maintains parents. Pure value updates can preserve node path but may change yielded values; structural mutation invalidates saved stacks/nodes unless a versioned fail-fast, lock-held, snapshot, persistent, or explicitly weak contract says otherwise. Cancellation releases stack/locks safely. Concurrent iteration needs synchronization/version/reclamation, not merely parent links.

### Answer 4

Own root and each node exactly once; define key/value/comparator ownership, parent/child inverses, exact destruction, and node-handle stability. Allocate/construct before publishing a new link; preserve old value on failed update when promising a strong guarantee; for deletion choose transplant or staged replacement according to throwing moves/assignments. Use iterative paths/traversal/destruction or a checked maximum depth/balanced representation for untrusted input. Reject mutable/inconsistent/reentrant comparators or guard callbacks. Serialize logical sorted associations plus comparator/schema identity and rebuild while validating count/order/duplicates; never trust pointers/shape/depth. Track size,height/max path, comparisons, allocations/failures, operation tails, and degeneration. Cap nodes,key bytes,comparison work,depth,allocation,request time, and concurrency; return typed failures.

### Answer 5

Generate operations against a sorted reference map; after each, assert global open bounds, acyclic unique reachability, size, parent inverses, augmentation, strict in-order equivalence classes, bounds/ranges, and exact values. Metamorphic checks include insert-erase restoration, update preserving keys/size, mirrored comparator symmetry, and in-order equals sorted model. Inject allocator/comparator/value construction/assignment failures at every boundary and count destruction. Force every root/non-root deletion shape, deep successor with right child, empty/singleton, comparator equivalence, sorted/reverse/organ-pipe inputs, maximum depth, iterator mutation, serialization corruption, and concurrent pauses at link publication/transplant/retirement. Benchmark all structures over realistic/adversarial sequences, sizes, operation/range mixes, key/value/comparator costs, allocators/layouts, and threads; report height, comparisons, allocations/bytes, cache/TLB, throughput and latency tails, repetitions, uncertainty, versions, and raw artifacts. Tests do not prove universal logarithmic height, exception safety for every type, concurrent linearizability, or workload-independent superiority.
