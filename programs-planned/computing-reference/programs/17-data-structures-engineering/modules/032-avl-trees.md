---
module_id: DSE-032
program: Data Structures Engineering
level: 1
module_number: 32
title: AVL Trees
status: complete
last_verified: 2026-08-30
---

# AVL Trees

## One-Page Review

### Governing question

How can a binary search tree maintain a logarithmic worst-case height through local rotations while preserving global order, exact height metadata, payload identity, deletion correctness, and production failure/lifetime contracts?

### Essential definitions

- An **AVL tree** is a BST in which every node's child-subtree heights differ by at most one.
- This module uses node-height `height(null)=0`, `height(leaf)=1`.
- A node's **balance factor** is `bf(x)=height(x.left)-height(x.right)`; valid values are `-1,0,1`.
- A **rotation** is a constant-size link transformation that preserves in-order key order.
- **LL** and **RR** describe outer-heavy imbalance repaired by one right or left rotation.
- **LR** and **RL** describe inner-heavy imbalance repaired by two rotations.
- **height augmentation** stores `1+max(left.height,right.height)` at each node.
- **rebalance** recomputes height, classifies imbalance, rotates, and returns the new subtree root.
- **repair path** is the ancestor chain whose subtree height may have changed after insertion/deletion.
- `N(h)` is the minimum number of nodes in an AVL tree of node-height `h`.

### Central model, mechanism, or theorem

The AVL invariant adds `|bf(x)|<=1` to the global BST invariant. The sparsest height-`h` AVL root has child heights `h-1` and `h-2`, so

`N(0)=0`, `N(1)=1`, and `N(h)=1+N(h-1)+N(h-2)`.

Thus `N(h)` grows like Fibonacci numbers and exponentially in `h`; equivalently `h=O(log n)`. Search remains ordinary BST search and is worst-case `O(log n)`.

A rotation preserves order by repartitioning three ordered regions. For right rotation at `y` with `x=y.left` and middle subtree `B=x.right`, the order is `A < x < B < y < C`; afterward `x.left=A`, `x.right=y`, `y.left=B`, so the same in-order sequence remains. Update the lower node's height before the new root's height. Insertion repairs the ancestor path and needs at most a constant number of rotations around its first violated ancestor in the classical algorithm; deletion can reduce repaired-subtree height and therefore may require repair at multiple ancestors, still `O(log n)` total.

### Critical invariants

1. Global strict BST bounds and declared comparator equivalence hold at every node.
2. Stored height equals `1+max(height(left),height(right))`, with null height zero.
3. Every node has balance factor in `{-1,0,1}` after a public operation completes.
4. Rotations preserve every node/association exactly once, all middle subtrees, root/parent ownership, and in-order sequence.
5. Insert/update/delete preserve size and payload lifetime; rebalancing changes shape, not logical content.
6. Height/other augmentations are recomputed bottom-up in dependency order after every changed link.
7. Iterators, references, node handles, and concurrent readers follow an explicit rotation/mutation contract.
8. Allocation/comparator/payload failure cannot publish a partially rewired or metadata-inconsistent tree.

### Common failures

- Mixing null-height `-1` and zero conventions in balance/rotation code.
- Recomputing height recursively during every repair, turning logarithmic updates into larger work.
- Selecting LL/LR/RR/RL from inserted key direction alone, which fails for deletion and generic comparators.
- Dropping the middle subtree during rotation.
- Updating the new root before its demoted child, storing a stale height.
- Repairing only the first deletion imbalance although subtree height may keep decreasing upward.
- Assuming a rotation invalidates references when nodes are relinked—or assuming stability when associations are copied/moved.
- Updating balance but forgetting size/order/interval augmentations.
- Claiming perfect balance; AVL permits child heights to differ by one.
- Publishing intermediate rotation links to unsynchronized readers.

### Compact example

Insertions `30,20,10`, `10,20,30`, `30,10,20`, and `10,30,20` independently force LL, RR, LR, and RL repairs; every final root is 20, while double cases use two primitive rotations. A separate tree built from `9,5,10,0,6,11,-1,1,2` has root 9 and height four. Deleting 10 promotes 11, makes the root left-heavy, and a right rotation produces root 1 while height remains four. The final keys are `-1,0,1,2,5,6,9,11`; all stored heights, bounds, balance factors, count, and three cumulative rotations validate.

### Connections

[DSE-031](031-binary-search-trees.md) supplies ordered-map semantics and deletion. [DSE-009](009-property-based-testing-of-data-structures.md) supplies invariant testing, while [DSE-006](006-memory-locality-and-cache-behavior.md) and [DSE-007](007-genericity-and-type-constraints.md) govern node layout and comparators. The [program roadmap](../ROADMAP.md) next compares red-black, randomized, adaptive, and augmented ordered trees.

## Governing Question

Which height convention, balance invariant, rotation primitive, repair rule, deletion propagation, augmentation order, and API/lifetime contract make an AVL ordered map both provably logarithmic and implementable without hidden corruption?

## Why This Matters

The plain BST makes ordered search depend on height but does not control height. Sorted or adversarial insertion can create a chain, making operations linear and recursive depth unsafe. AVL trees add one local invariant whose global consequence is logarithmic height.

That guarantee is not free. Every mutation maintains height metadata, classifies four orientation cases, and changes multiple links. Deletion can trigger repair repeatedly toward the root. Iterators and parent pointers observe shape changes even though sorted content remains identical. Generic comparators, throwing payload operations, intrusive nodes, and concurrent readers turn a textbook diagram into a systems problem.

AVL is also a model for augmented structures. The same bottom-up dependency discipline later maintains subtree sizes, interval maxima, priorities, and cached aggregates. Rotations are not memorized pictures; they are local algebra over ordered regions and derived metadata.

## Prerequisites and Retrieval

Retrieve the global BST invariant, comparator equivalence, search, bounds, traversal, all deletion cases, association-copy versus node transplant, ownership, and height-sensitive analysis from [DSE-031](031-binary-search-trees.md). Retrieve representation invariants and operation contracts from [DSE-002](002-representation-invariants.md) and [DSE-003](003-operation-contracts.md), locality and genericity from [DSE-006](006-memory-locality-and-cache-behavior.md) and [DSE-007](007-genericity-and-type-constraints.md), testing from [DSE-009](009-property-based-testing-of-data-structures.md), and measurement from [DSE-010](010-benchmarking-a-structure-without-misleading-results.md).

## Learning Objectives

After completing this module, you should be able to:

1. state the BST, stored-height, and AVL balance invariants under one height convention;
2. derive logarithmic height from the minimum-node recurrence;
3. prove left/right rotations preserve order, reachability, and exact content;
4. implement LL, RR, LR, and RL classification from subtree balance factors;
5. repair insertion bottom-up and explain its constant primitive-rotation bound;
6. repair deletion through every affected ancestor and explain cascading rotations;
7. update height and arbitrary subtree augmentations in dependency order;
8. specify reference, iterator, node-identity, failure, recursion, and concurrency behavior;
9. test every rotation/deletion topology using independent recomputation and a reference map;
10. compare AVL with red-black trees, sorted vectors, B-trees, and hash maps by workload evidence.

## Core Exposition

**Add height balance to the BST contract.** An AVL node still partitions all keys by the comparator; rotation never weakens that global order. It additionally stores or derives subtree height and requires the two child heights to differ by at most one. Pick one height convention and make it repository-wide. Here null is zero and a new leaf is one. Literature using null `-1` and leaf zero is equivalent only if every formula shifts consistently.

The balance factor sign is also conventional. This module uses left minus right. Positive two means left-heavy; negative two means right-heavy. Mixing a source's opposite sign can silently select the wrong rotation. Tests should construct named shapes rather than trust comments like “RR case.”

The strongest checker ignores stored heights initially. It recursively/iteratively validates ancestor bounds, computes true child heights, requires stored height equal to the result, requires absolute difference at most one, checks unique reachability/count, and returns the true height. Comparing a field with itself or using stored child heights to validate stored parent height can let consistent-but-wrong metadata pass.

**The height bound is a recurrence proof.** Let `N(h)` be the fewest nodes possible at node-height `h`. For `h>=2`, a minimum tree must have one child of height `h-1`; balance permits the other to be no shorter than `h-2`. Choosing exactly those heights and minimum subtrees yields `N(h)=1+N(h-1)+N(h-2)`, with `N(0)=0,N(1)=1`.

The sequence is Fibonacci-shifted: `N(2)=2,N(3)=4,N(4)=7,N(5)=12`. It grows at least exponentially—for example `N(h)>=2*N(h-2)`—so `h<=2 log2(n+1)+O(1)` is already enough for `O(log n)`. A tighter Fibonacci/golden-ratio expression gives a better constant but does not change the algorithmic conclusion.

The theorem assumes every node is balanced and height describes the reachable tree. A stale field or one unbalanced descendant invalidates the premise. Logging root height alone is useful telemetry, not proof.

**A rotation is an order-preserving subtree replacement.** For left rotation at `x`, require `y=x.right`; save middle `B=y.left`; set `x.right=B`; set `y.left=x`; then repair parent/root links and return `y`. Before rotation, ordered regions satisfy `A<x<B<y<C`; afterward the in-order sequence remains `A,x,B,y,C`.

Right rotation is symmetric. A production node with parents sets `B.parent`, the demoted node's parent, the promoted node's former parent child/root, and the promoted node's parent. Intrusive membership, threaded links, min caches, subtree sizes, interval maxima, and version fields may add work.

Update derived metadata bottom-up: after left rotation, `x` is demoted and its children are final, so recompute `x`; then recompute promoted `y`. Reversing this order can calculate `y` from stale `x.height`. Generic augmentation needs a declared recompute function whose dependencies are children and local payload.

Rotations normally relink existing nodes; key/value references may remain stable if node allocations do. Iterators storing an ancestor stack can become structurally stale. Array-packed implementations may move nodes. Association-copy deletion changes identity before rotations even in a node layout. Document each handle category instead of saying merely “rotations preserve elements.”

**Rebalance from child heights, not history.** After a recursive/iterative child mutation, recompute node `z`. If `bf(z)>1`, inspect `bf(z.left)`. Nonnegative means outer/LL-or-deletion-equal case: right rotate `z`. Negative means inner/LR: left rotate `z.left`, then right rotate `z`. If `bf(z)<-1`, use symmetric rules.

The equality cases matter for deletion. Rules based solely on the newly inserted key—`key<z.left.key`, and so on—can classify insertion but do not generalize when no inserted key exists and a sibling's height decreased. Child balance factors express the actual shape.

The local proof assumes a pre-operation AVL tree and one child height changed by at most one, so a violated ancestor has magnitude two. If a checker observes magnitude three or more, earlier metadata/repair is wrong or an unsafe bulk mutation bypassed the algorithm. A defensive implementation may reject/rebuild, but one textbook rotation proof cannot simply be applied without its precondition.

**Insertion repair is bottom-up.** Perform ordinary BST insert/update. A new unique leaf has height one. On return/ascent, recompute each ancestor and rebalance. If an equivalent key only changes value and no augmentation depends on value, height/shape remain unchanged.

At the first imbalanced insertion ancestor, a single outer rotation or inner double rotation restores the subtree to its pre-insertion height in the classical AVL proof. Therefore higher ancestors do not become newly imbalanced from height growth, and insertion uses at most two primitive rotations. An implementation may still walk/update ancestors depending on its control flow/augmentations.

Recursive code naturally returns each possibly new subtree root. Iterative parent-pointer code must reconnect rotation results to grandparents/root. A common bug rebalances a local pointer but leaves the parent pointing at the demoted node, disconnecting the promoted root.

Construct/compare before publishing a leaf. If allocation or key/value construction fails, no height changes are needed. Comparator failure during descent leaves structure unchanged if comparisons have no side effects. Once rotations begin, they should be nonthrowing pointer/metadata operations; otherwise rollback becomes a transaction over multiple ancestors.

**Deletion repair can cascade.** First perform BST deletion using the identity/lifetime policy from DSE-031. The physical removal occurs at a node with at most one child (even when a successor association was copied). Its former ancestors may lose one unit of subtree height. Recompute and rebalance from the lowest changed ancestor to root.

After a deletion rotation, the repaired subtree may be one level shorter than before deletion. Its parent can therefore become imbalanced, so continue. In worst case `O(h)=O(log n)` ancestors are visited and a logarithmic number of rotations may occur. This is the key distinction from insertion's constant primitive-rotation bound.

If association-copy deletion copies successor key/value into the target and recursively deletes the successor, repair begins along the successor's old path and naturally propagates through the target/root in a recursive implementation. If physical transplant moves a node, recompute all paths whose child or augmentation changed; there may be a join between the successor-removal path and target path.

The child-balance-zero deletion case often determines whether one rotation reduces height and propagation continues. Do not reuse an insertion-only `>`/`<` classifier that excludes equality. Exhaustive small-tree generation is valuable here because deletion cases are easy to miss.

**Height storage is an engineering choice.** Storing full height makes validation/debugging and generic recomputation simple; the value is `O(log n)` and often fits in a small integer, but alignment may make a byte save invisible. Storing only balance factor uses two bits conceptually, but update logic must propagate height-change information. Packing balance bits into parent pointers requires alignment/provenance care.

Never let a narrow height field wrap. Even a valid AVL tree's height is logarithmic, but deserialized/corrupt/unbalanced input or a type-capacity mismatch can exceed the representation. Use checked conversions and validate before trusting stored metadata.

Adding subtree size enables rank/select; interval maximum enables overlap search. A rotation preserves logical entries but changes the children of the demoted and promoted nodes, so recompute all augmentations for the demoted node first, promoted node second. For nonlocal/lazy aggregates, name invalidation and propagation.

**Iteration order is unchanged, iterator structure may not be.** In-order traversal yields comparator-sorted associations exactly as in a BST. A stack iterator holds a root-to-current path; rotations after creation can invalidate that path even if node addresses survive. A fail-fast version, snapshot, persistent tree, lock-held iterator, restart-by-key, or explicit no-mutation rule is needed.

Parent-pointer successor can follow the reshaped tree if the current node remains live and all parents are correct, but concurrent unsynchronized mutation still races. References to values may survive rotations in node-based designs; erase invalidates the erased node; association-copy can change the key bound to a surviving address. Provide a matrix for insert/update/rotate/delete/clear.

Sorted serialization should encode logical associations and comparator/schema identity, not stored heights/balance/tree shape unless those are a versioned physical checkpoint. Rebuilding by repeated sorted insertion into a plain AVL implementation is correct but may do avoidable rotations; a validated median build can construct a balanced tree in linear time and compute heights bottom-up.

**Recursion and memory still matter.** A valid AVL tree bounds recursion to `O(log n)`, so normal operation stack depth is safe relative to `n` under reasonable capacity. But deserialization, a corrupted root, or code that validates balance only after recursive descent can still traverse a hostile deep chain. Use iterative validation or a depth/node budget for untrusted physical input.

Each node adds height/balance and perhaps parent pointers atop BST payload/links. AVL's tighter height may improve comparison count but rotations/metadata writes add mutation cost. Node allocation and pointer chasing dominate many workloads; a B-tree or sorted vector may win cache density. Measure rather than infer from height alone.

Intrusive implementations must prevent one node from belonging to multiple trees through the same link set and require removal before object destruction. Pool allocation improves locality but complicates individual reclamation. Compact indexes/offsets change rotation links but not the ordered-region proof; validate ranges and generation/handle invalidation.

**Concurrency requires atomicity above local rotations.** A rotation writes multiple links and heights. A reader seeing `x.right` changed before `y.left` published may miss nodes or observe cycles depending on sequence. Use an external lock, path locks with a proven protocol, immutable path copying, transactional publication, or a specifically designed concurrent balanced tree.

OpenJDK's red-black `TreeMap` is externally synchronized for structural concurrency; Linux's rbtree leaves locking to its user. Those policies illustrate that balanced shape is not thread safety. Lock-free AVL algorithms require descriptors/helping/versioning and safe reclamation far beyond sequential rotations.

Optimistic readers must validate versions spanning every node/link they rely on. Epoch/hazard/GC retirement protects memory but does not alone guarantee a consistent search path. Iterators/ranges need snapshot or weak semantics. Count locks/versions/retired nodes in memory and latency evidence.

**Security and resource controls remain.** AVL blocks the sorted-key height attack when comparator and repair are correct, but does not cap total entries, key bytes, comparator cost, allocation, or request rate. A malicious comparator can be nonlinear, inconsistent, or throwing. Deserializing enormous `n` or forged heights can exhaust resources.

Apply entry/byte/depth/comparison/rotation/allocation/time/concurrency limits, stable comparator policy, checked size/height arithmetic, and typed failures. Instrument operation comparisons, path length, rotations by type, deletion rotations, height, maximum balance magnitude, allocation failures, and latency tails without scanning the tree on every operation.

If runtime checks observe a balance magnitude beyond two during ordinary sequential mutation or stored-height mismatch, treat it as invariant corruption, not a workload anomaly. Stop unsafe publication/use, retain diagnostic evidence without exposing sensitive keys, and rebuild only from validated logical content under a bounded policy.

**Testing needs both local cases and global recomputation.** Independently force LL, RR, LR, and RL insertion, including root and internal rotations. For deletion cover leaf/one/two-child physical removal, immediate/deep successor, child-balance `-1,0,1`, one/multiple ancestor rotations, root replacement, minimum/maximum, and collapse to empty.

After every mutation compare with a reference ordered map and independently recompute bounds, reachable count, actual height, stored height, and balance. Check in-order equality, get/bounds/ranges, size, parent inverses, augmentation, and exact payload destruction. Exhaustively generate all insertion/deletion sequences for small key sets and deduplicate states; random testing alone may rarely hit critical deletion shapes.

Inject allocation, comparator, value update/copy/move, and serialization failure. Pause concurrency at each link/metadata publication when applicable. Use sanitizers/race detectors/model checking appropriate to the language, but do not treat them as proof.

Benchmark AVL against red-black/B-tree/sorted-vector/hash alternatives over random, sorted, reverse, partially sorted, Zipfian, range-heavy, update-heavy, and delete-heavy workloads. Report `n`, height, comparisons, rotations by type, nodes/bytes/allocations, cache/TLB/branches, throughput, p50/p95/p99/max, compiler/runtime/allocator/hardware, repetitions, uncertainty, and raw artifacts. Separate search benefit from rotation/write cost and final from peak memory.

The executable trace implements a sequential unique-integer AVL map using stored node-height and association-copy deletion. It counts primitive rotations, forces all four insertion orientations, then demonstrates deletion-triggered ancestor repair. Its checker recomputes global order, true height, balance, cycles, and count. It does not prove generic comparator/failure/lifetime safety, stable handles, parent pointers, concurrency, or production performance.

<!-- bijux-verify: {"id":"avl-rotation-deletion-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"ll_root=20\nrr_root=20\nlr_root=20\nrl_root=20\nbefore=-1,0,1,2,5,6,9,10,11\nbefore_root=9\nbefore_height=4\nrotations_before_delete=2\ndeleted=TEN\nafter=-1,0,1,2,5,6,9,11\nafter_root=1\nafter_height=4\nrotations_after_delete=3\ninvariant=True\nevidence=finite_avl_rotation_trace\n","stderr":""}} -->
```python
from dataclasses import dataclass


@dataclass
class Node:
    key: int
    value: str
    left: object = None
    right: object = None
    height: int = 1


class AVLMap:
    def __init__(self):
        self.root = None
        self.size = 0
        self.rotations = 0

    @staticmethod
    def node_height(node):
        return node.height if node is not None else 0

    def update_height(self, node):
        node.height = 1 + max(
            self.node_height(node.left), self.node_height(node.right)
        )

    def balance(self, node):
        return self.node_height(node.left) - self.node_height(node.right)

    def rotate_right(self, top):
        promoted = top.left
        middle = promoted.right
        promoted.right = top
        top.left = middle
        self.update_height(top)
        self.update_height(promoted)
        self.rotations += 1
        return promoted

    def rotate_left(self, top):
        promoted = top.right
        middle = promoted.left
        promoted.left = top
        top.right = middle
        self.update_height(top)
        self.update_height(promoted)
        self.rotations += 1
        return promoted

    def rebalance(self, node):
        self.update_height(node)
        factor = self.balance(node)
        if factor > 1:
            if self.balance(node.left) < 0:
                node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        if factor < -1:
            if self.balance(node.right) > 0:
                node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
        return node

    def put(self, key, value):
        inserted = []

        def add(node):
            if node is None:
                inserted.append(True)
                return Node(key, value)
            if key < node.key:
                node.left = add(node.left)
            elif node.key < key:
                node.right = add(node.right)
            else:
                node.value = value
                return node
            return self.rebalance(node)

        self.root = add(self.root)
        if inserted:
            self.size += 1
        return bool(inserted)

    def delete(self, key):
        removed = []

        def delete_min(node):
            if node.left is None:
                return node.right
            node.left = delete_min(node.left)
            return self.rebalance(node)

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
                successor = node.right
                while successor.left is not None:
                    successor = successor.left
                node.key, node.value = successor.key, successor.value
                node.right = delete_min(node.right)
            return self.rebalance(node)

        self.root = erase(self.root)
        self.size -= 1
        return removed[0]

    def keys(self):
        result = []

        def visit(node):
            if node is not None:
                visit(node.left)
                result.append(node.key)
                visit(node.right)

        visit(self.root)
        return result

    def invariant(self):
        seen = set()

        def check(node, lower, upper):
            if node is None:
                return 0, 0
            if id(node) in seen:
                raise AssertionError("cycle or shared node")
            seen.add(id(node))
            if lower is not None and not lower < node.key:
                raise AssertionError("lower bound")
            if upper is not None and not node.key < upper:
                raise AssertionError("upper bound")
            left_height, left_count = check(node.left, lower, node.key)
            right_height, right_count = check(node.right, node.key, upper)
            actual_height = 1 + max(left_height, right_height)
            if node.height != actual_height:
                raise AssertionError("stored height")
            if abs(left_height - right_height) > 1:
                raise AssertionError("AVL balance")
            return actual_height, 1 + left_count + right_count

        try:
            _, count = check(self.root, None, None)
            return count == self.size
        except AssertionError:
            return False


def root_after(sequence):
    tree = AVLMap()
    for key in sequence:
        assert tree.put(key, str(key))
    assert tree.invariant()
    return tree.root.key


ll_root = root_after((30, 20, 10))
rr_root = root_after((10, 20, 30))
lr_root = root_after((30, 10, 20))
rl_root = root_after((10, 30, 20))

tree = AVLMap()
for key in (9, 5, 10, 0, 6, 11, -1, 1, 2):
    value = "TEN" if key == 10 else str(key)
    assert tree.put(key, value)
before = tree.keys()
before_root = tree.root.key
before_height = tree.root.height
rotations_before = tree.rotations
assert tree.invariant()
deleted = tree.delete(10)

print(f"ll_root={ll_root}")
print(f"rr_root={rr_root}")
print(f"lr_root={lr_root}")
print(f"rl_root={rl_root}")
print("before=" + ",".join(map(str, before)))
print(f"before_root={before_root}")
print(f"before_height={before_height}")
print(f"rotations_before_delete={rotations_before}")
print(f"deleted={deleted}")
print("after=" + ",".join(map(str, tree.keys())))
print(f"after_root={tree.root.key}")
print(f"after_height={tree.root.height}")
print(f"rotations_after_delete={tree.rotations}")
print(f"invariant={tree.invariant()}")
print("evidence=finite_avl_rotation_trace")
```

## Definitions and Notation

- `height(null)=0`, `height(leaf)=1`: module height convention.
- `bf(x)=height(x.left)-height(x.right)`: balance factor.
- `N(h)`: minimum live nodes in a valid node-height-`h` AVL tree.
- **demoted node**: former subtree root moved down by rotation.
- **promoted node**: child becoming new subtree root.
- **middle subtree**: subtree transferred between promoted/demoted nodes.
- **primitive rotation**: one left or right rotation; LR/RL use two.
- **repair path**: changed node's ancestors processed bottom-up.
- **augmentation**: cached function of node payload and child summaries.
- **association-copy/node-transplant deletion**: identity alternatives inherited from DSE-031.

## Mechanisms, Invariants, or Proof Structure

The global proof combines BST bounds, exact reachability/lifetime, stored-height equations, and `|bf|<=1`. The minimum-node recurrence proves height logarithmic. Rotation correctness partitions the subtree into ordered regions and shows their in-order sequence and ownership are unchanged.

Mutation first performs a valid BST change, then repairs only ancestors whose child height may have changed. Rebalance derives orientation from the node and heavy child's balance, preserves order with one/two rotations, and recomputes all augmentations demoted-first. Insertion stops height propagation after its first repair; deletion may reduce repaired height and continues to root.

Failure/concurrency proofs add publication and lifetime: allocate/construct before linking, make rotation primitives nonthrowing or transactional, reconnect returned roots, exclude/validate readers, and reclaim removed nodes only after no reference can observe them.

## Alternatives and Trade-Offs

| Design | Strength | Cost or obligation |
|---|---|---|
| Full stored height | simple recomputation and auditing | field bytes and checked width |
| Packed balance factor | minimal conceptual bits | complex height-change propagation/provenance |
| Recursive repair | naturally returns new subtree roots | stack and failure-unwind concerns |
| Parent-pointer iterative repair | explicit bounded ascent/navigation | parent bytes and reconnect correctness |
| Association-copy deletion | fewer link rewrites | node/key identity and copying failure |
| Physical transplant | preserves moved node association | multiple repair paths/links/augmentations |
| AVL tree | tighter height/search bound | more metadata/rotation writes |
| Red-black tree | looser balance, fewer update repairs in some designs | color/fix-up complexity and taller bound |
| B-tree | cache/page-friendly high fanout | node search/split/merge complexity |
| Sorted vector | dense traversal/search | linear middle mutation |

## Failure Modes and Misconceptions

- **“AVL means equal subtree sizes.”** it constrains heights, not sizes.
- **“Balance factor sign is universal.”** sources use opposite conventions; code must choose one.
- **“Any imbalance uses one rotation.”** inner-heavy LR/RL need two primitives.
- **“The inserted key selects every repair.”** deletion requires current child balances.
- **“Insertion can rotate at every ancestor.”** classical AVL insertion needs at most one single/double repair event.
- **“Deletion stops after one repair.”** reduced height may imbalance successive ancestors.
- **“Rotation is just two assignments.”** middle subtree, parent/root, metadata, and publication matter.
- **“Update heights in any order.”** promoted height depends on corrected demoted height.
- **“Stored height proves balance.”** independently recompute actual height and bounds.
- **“Rotations preserve all handles.”** representation and deletion identity determine validity.
- **“Balanced means thread-safe.”** multi-link changes need synchronization and reclamation.
- **“AVL always outperforms red-black/B-tree.”** workload, mutation, cache, payload, and implementation decide.

## Worked Examples

### Example 1

`30,20,10` makes node 30 balance `+2` with nonnegative left-child balance. Right rotation promotes 20. Conclusion: LL is an outer single rotation.

### Example 2

`10,20,30` symmetrically left-rotates 10 and promotes 20. Conclusion: RR is a single rotation under the left-minus-right convention.

### Example 3

`30,10,20` has left-heavy 30 but right-heavy child 10. Left-rotate 10, then right-rotate 30. Conclusion: LR requires two dependency-ordered rotations.

### Example 4

`10,30,20` right-rotates child 30 then left-rotates 10. Conclusion: RL is the symmetric inner case.

### Example 5

Right rotation with regions `A<x<B<y<C` moves `B` from `x.right` to `y.left`; omitting it loses keys. Conclusion: name the middle subtree in every proof/code review.

### Example 6

Minimum-node counts are `0,1,2,4,7,12` for heights `0..5`. Conclusion: AVL height grows only logarithmically with nodes.

### Example 7

Updating an equivalent key's value changes no links or height when augmentation ignores values. Conclusion: not every put is structural.

### Example 8

Deleting 10 from the executable tree reduces the right side of root 9; one right rotation promotes 1. Conclusion: deletion repair is driven by resulting child heights.

### Example 9

A stack iterator saved ancestors before a rotation. Nodes remain allocated but the saved path no longer describes successor navigation. Conclusion: address stability and iterator validity differ.

### Example 10

A node stores height 3 although independently computed children imply height 4 and balance 2. Conclusion: root-height telemetry cannot substitute for full invariant validation.

## Cross-Program Connections

- **Algorithms:** Fibonacci recurrences, logarithmic bounds, local transformations, and amortized/path arguments connect proof to operations.
- **Programming languages:** comparator laws, augmentation types, exceptions, moves, intrusive ownership, and recursion determine safe implementation.
- **Computer architecture:** node pointers, metadata writes, rotations, cache/TLB locality, and branch behavior shape practical trade-offs.
- **Concurrent programming:** atomic multi-link publication, path locks, versions, immutable copying, epochs, and hazards govern shared trees.
- **Database engineering:** AVL leads toward page-oriented B-trees and ordered indexes; balance and range traversal remain core ideas.
- **Software engineering:** independent invariant checkers, invalidation matrices, serialization schemas, telemetry, and fault injection make balancing maintainable.
- **Security engineering:** height balance removes one shape attack but comparator cost, input volume, corruption, and allocation still need limits.

## References

1. G. M. Adel'son-Vel'skii and E. M. Landis, [An algorithm for organization of information](https://www.mathnet.ru/php/archive.phtml?jrnid=dan&option_lang=eng&paperid=26964&wshow=paper). Bibliographic/full-text primary source for the original 1962 height-balanced search-tree work.
2. MIT OpenCourseWare 6.006, [Binary Trees, Part 2: AVL](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/lecture-7-binary-trees-part-2-avl/). Primary academic lecture for rotations, height balance, minimum-node proof, augmentation, and global repair.
3. MIT OpenCourseWare 6.006, [AVL Recitation Notes](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/f71168c033e4cb0bd989345e478934aa_MIT6_006F11_rec06.pdf). Primary worked source for stored heights, rotation cases, insertion, and deletion ascent.
4. Boost.Intrusive Project, [`avl_set.hpp`](https://github.com/boostorg/intrusive/blob/develop/include/boost/intrusive/avl_set.hpp). Current primary source for a production intrusive AVL container, its ownership model, options, operations, and contracts.
5. Ben Pfaff, GNU libavl, [AVL Trees](https://adtinfo.org/libavl.html/AVL-Trees.html). Literate implementation/reference for rotations, insertion, deletion, traversal, testing, and engineering cases.
6. Cornell CS 312, [AVL Trees](https://www.cs.cornell.edu/courses/cs312/2006fa/lectures/lec13.html). Academic functional formulation of height/balance, smart constructors, and rotation/rebalance reasoning.
7. OCaml Project, [`stdlib/set.ml`](https://github.com/ocaml/ocaml/blob/trunk/stdlib/set.ml). Current primary source for a production persistent height-balanced ordered set variant; its balance threshold/implementation are explicitly not presented as classical AVL identity.
8. ISO C++ working draft, [Algorithms library ordering requirements](https://eel.is/c%2B%2Bdraft/alg.sorting). Current strict-weak-order and equivalence requirements for generic ordered keys.
9. Rust Project, [`std::collections::BTreeMap`](https://doc.rust-lang.org/std/collections/struct.BTreeMap.html). Current balanced ordered-map API and range/entry/iterator/key-consistency contract, used as a production alternative.
10. OpenJDK Project, [`TreeMap.java`](https://github.com/openjdk/jdk/blob/master/src/java.base/share/classes/java/util/TreeMap.java). Current red-black ordered-map source and API commentary, used as a comparator, deletion, iterator, synchronization, and balancing-policy contrast.

## Exercises

### Exercise 1

Derive the AVL height bound from `N(h)=1+N(h-1)+N(h-2)`. State base cases and translate the exponential lower bound on nodes into a logarithmic upper bound on height.

### Exercise 2

Prove left/right rotations preserve BST order and exact reachability. Extend the proof to parent pointers, height, subtree size, and interval-maximum augmentation with correct update order.

### Exercise 3

Implement insertion repair for all four orientations using child balance factors. Prove why classical insertion needs at most one single/double repair event and test internal/root rotations.

### Exercise 4

Implement deletion with association-copy and with physical transplant. Explain repair-path differences, child-balance-zero cases, cascading rotations, failure, identity, and iterator consequences.

### Exercise 5

Design property, exhaustive-small-state, fault, lifetime, adversarial, concurrency, and benchmark evidence comparing AVL with unbalanced BST, red-black/B-tree, sorted vector, and hash map.

## Answers to the Exercises

### Answer 1

Set `N(0)=0,N(1)=1`. A height-h root needs one child height h-1; balance forces the other at least h-2, so the minimum is `1+N(h-1)+N(h-2)`. This is Fibonacci-shifted and `N(h)>=2N(h-2)`, hence after repeated substitution `N(h)>=2^(h/2)-1` up to base parity. Therefore `n>=N(h)` implies `h<=2log2(n+1)+O(1)=O(log n)`. A tighter Fibonacci/phi calculation improves the coefficient. The conclusion requires every reachable node's balance invariant and true height—not merely stored root metadata.

### Answer 2

For left rotation partition keys as `A<x<B<y<C`, where y=x.right and B=y.left. Rewire x.right=B and y.left=x, reconnect y to x's former parent/root, and set B.parent=x, x.parent=y, y.parent=old parent. The in-order sequence remains A,x,B,y,C and every region/node has one owner. Recompute demoted x first from A,B, then promoted y from corrected x,C. Subtree size is `1+size(left)+size(right)` in the same order; interval maximum is max(local interval endpoint/summary,left,right) likewise. Right rotation is symmetric. If any metadata callback can throw, compute/stage before publication or make rotation metadata recomputation nonthrowing/transactional.

### Answer 3

After ordinary insert, return/ascent recomputes z. If bf(z)>1, use right rotation when bf(z.left)>=0, else left-rotate z.left then right-rotate z. If bf(z)<-1, use left rotation when bf(z.right)<=0, else right-rotate z.right then left-rotate z. Reconnect every returned root. At the lowest insertion-imbalanced ancestor, the new leaf increased the heavy path; the appropriate single/double rotation restores balance and the subtree's pre-insertion height, so higher ancestors see no additional height increase. Force LL/RR/LR/RL at root and beneath a grandparent; independently check in-order content, true/stored heights, all balances, size, parents, and rotation counts.

### Answer 4

BST physical removal occurs at a node with at most one child; ascent from that old location recomputes and rebalances every ancestor. Association-copy replaces target association with successor then removes successor, so handles to target change key identity and copying may fail; the repair path follows successor removal through target/root. Physical transplant detaches successor, installs it at target, and repairs affected successor-removal and target ancestor paths while preserving successor-node identity. For deletion, heavy child's balance may be zero; use non-strict outer tests (`>=0`/`<=0`). A repair can reduce subtree height, so continue to root and permit multiple rotations. Iterators/stacks/versioning and parent/augmentations update across every rotation; removed nodes retire under the lifetime/concurrency scheme.

### Answer 5

Generate operations against a sorted reference map; after each independently validate ancestor bounds, comparator equivalence, acyclic unique reachability, count, true/stored height, balance, parents, augmentations, in-order keys/values, bounds, and ranges. Exhaust all small insertion/deletion permutations to cover four orientations, root/internal repair, immediate/deep successor, heavy-child balances -1/0/1, and cascading deletion; add sorted/reverse/partially sorted and comparator-equivalent inputs. Inject allocation/comparison/value/serialization failures and count construction/destruction. Pause concurrent implementations at link/metadata publication and retirement; check histories/races/reclamation. Benchmark representative/adversarial workloads with n,height,comparisons,rotations,allocations/bytes, cache/TLB/branches, throughput/tails, platform/toolchain, repetitions, uncertainty, and raw artifacts. This evidence does not prove generic exception safety, lock-free correctness, universal performance superiority, or production fitness without the corresponding design and external review.
