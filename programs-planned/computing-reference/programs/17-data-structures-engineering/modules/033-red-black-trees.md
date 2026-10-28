---
module_id: DSE-033
program: Data Structures Engineering
level: 1
module_number: 33
title: Red-Black Trees
status: complete
last_verified: 2026-08-30
---

# Red-Black Trees

## One-Page Review

### Governing question

How can one color bit per node constrain every search path enough to guarantee logarithmic ordered-map operations, while insertion, deletion, rotations, recoloring, augmentation, identity, and concurrency remain correct?

### Essential definitions

- A **red-black tree** is a BST augmented with red/black color and path constraints.
- **NIL leaves** are conceptual black sentinels replacing null child positions.
- A node's **black-height** is the number of black nodes on any path from that node (under a stated endpoint convention) to descendant NIL; equality makes it well-defined.
- A **red-red violation** is a red node with a red parent/child.
- A **black deficit** or **double black** is bookkeeping for the missing black contribution after deleting/moving a black node.
- **rotation** preserves BST in-order order while changing local shape.
- **recoloring** changes the encoded multiway structure without changing links.
- **uncle** is the parent's sibling during insertion repair; **sibling**, **near child**, and **far child** classify deletion repair relative to the deficit side.
- A **2–3–4 correspondence** contracts red-linked nodes into multi-key nodes; black links/levels encode multiway depth.
- A **left-leaning red-black tree (LLRB)** is a stricter variant encoding red links in one orientation, usually corresponding to 2–3 or 2–3–4 trees depending on the algorithm.

### Central model, mechanism, or theorem

Under a standard classical convention:

1. every internal node is red or black;
2. the root is black;
3. every NIL leaf is black;
4. no red node has a red child;
5. every path from a node to descendant NIL contains the same number of black nodes.

If a subtree has black-height `b`, it contains at least `2^b-1` internal nodes. Because red nodes cannot be consecutive, a root-to-NIL path has length at most twice its black-node count. Hence tree height `h <= 2 log2(n+1)`, and BST path operations are worst-case `O(log n)`.

Insertion creates a red leaf so equal black-height is initially preserved; repair eliminates a possible red-red edge by recoloring when the uncle is red or by triangle/line rotations and recoloring when the uncle is black. Deletion physically removes a node with at most one non-NIL child. Removing a black contribution creates a deficit repaired through sibling-color/child-color cases until it is absorbed, propagated to the root, or resolved by rotation/recoloring. Exact cases depend on sentinel, parent, top-down/bottom-up, classical/LLRB, and identity choices; variants must not be spliced together casually.

### Critical invariants

1. Global BST bounds and comparator-equivalence policy hold independently of colors.
2. The root and every conceptual/explicit NIL leaf are black under the chosen representation.
3. A red node has only black children; all descendant NIL paths from each node have equal black-height.
4. Each node/link is owned exactly once; rotations preserve the middle subtree, root/parent links, and exact content.
5. Color changes and rotations preserve the chosen 2–3/2–3–4 encoding and terminate repair.
6. `size`, parent links, subtree augmentations, sentinels, modification versions, and payload lifetime remain consistent.
7. Insert/delete failure cannot expose partially published links/colors or ambiguous authority.
8. Iterator/reference/node-handle/concurrent-reader behavior is explicit across rotations, association replacement, erase, and reclamation.

### Common failures

- Omitting conceptual NIL leaves from black-height reasoning.
- Checking only root color and absence of adjacent red nodes, but not equal black-height.
- Treating all red-black formulations as interchangeable with LLRB code.
- Rotating without transferring the middle subtree or reconnecting the grandparent/root.
- Recoloring a null child or using null where a deletion algorithm requires a parent-aware sentinel.
- Deleting a two-child association and repairing from the target rather than the physical removal site.
- Confusing sibling near/far children after the deficit side changes through a rotation.
- Forgetting root-black normalization or subtree-size recomputation.
- Assuming rotations move payload objects—or promising stable handles while association-copy deletion changes identity.
- Publishing multi-link/color intermediate states to unsynchronized readers.

### Compact example

A left-leaning red-black ordered map inserts keys `5,3,7,2,4,6,8,1,9`. Its sorted keys are `1..9`, root 5, size nine, and it has used nine primitive rotations plus four color flips. Top-down deletion first removes minimum leaf 1, then internal key 7, then root association 5. The final keys are `2,3,4,6,8,9`, root 6, size six, with fourteen cumulative rotations and ten flips. An independent checker verifies global bounds, black root, no right-leaning red link, no consecutive red nodes, equal black-height, subtree sizes, unique reachability, and exact count.

### Connections

[DSE-031](031-binary-search-trees.md) supplies ordered-map deletion and [DSE-032](032-avl-trees.md) supplies rotation/augmentation proof discipline. [DSE-007](007-genericity-and-type-constraints.md) owns comparator semantics and [DSE-009](009-property-based-testing-of-data-structures.md) owns invariant testing. The [program roadmap](../ROADMAP.md) continues with randomized treaps, adaptive splay trees, and augmented ordered structures.

## Governing Question

Which red-black formulation, sentinel/color encoding, insertion and deletion repair protocol, augmentation order, identity policy, and validation evidence yield a maintainable worst-case-logarithmic ordered map rather than a collection of memorized cases?

## Why This Matters

Red-black trees are a central production ordered-map design because they guarantee logarithmic height with one color bit and comparatively permissive balance. Implementations appear in language libraries, intrusive systems code, and container internals. Their sorted iteration and bound/range operations are deterministic, unlike hash placement.

The difficulty is deletion. A diagram may hide NIL sentinels, parent ownership, physical removal location, color transfer, payload assignment, augmentation, and reader lifetime. Case labels differ across texts. An implementation that mixes bottom-up classical insertion with top-down LLRB deletion without proving shared invariants can pass simple tests and fail on rare histories.

The durable mental model is multiway encoding plus local conservation. Red links fuse binary nodes into logical 3/4-nodes; black-height is the uniform multiway level count. Recoloring splits/merges encoded nodes, while rotations change encoding orientation without changing key order. This model explains both the height theorem and repair intent.

## Prerequisites and Retrieval

Retrieve global BST bounds, comparator equivalence, bounds/ranges, in-order traversal, all deletion topologies, association-copy versus physical transplant, ownership, recursion, and concurrency from [DSE-031](031-binary-search-trees.md). Retrieve rotation algebra, returned subtree roots, augmentation order, identity, exhaustive deletion testing, and balanced-tree benchmarking from [DSE-032](032-avl-trees.md). Retrieve representation/operation contracts from [DSE-002](002-representation-invariants.md) and [DSE-003](003-operation-contracts.md).

## Learning Objectives

After completing this module, you should be able to:

1. state classical red-black invariants including conceptual NIL leaves;
2. derive the `2 log2(n+1)` height bound from black-height;
3. explain the 2–3/2–3–4 correspondence and distinguish classical from LLRB variants;
4. prove rotations/recolorings preserve BST order, reachability, and encoded structure;
5. derive insertion repair from parent/uncle orientation and color;
6. derive deletion repair from deficit side, sibling color, and near/far child colors;
7. implement and validate top-down LLRB insertion/deletion as one coherent variant;
8. maintain parent links, subtree augmentations, sentinels, versions, and payload lifetime;
9. test every color/rotation/physical-removal case with independent black-height recomputation;
10. compare red-black with AVL, B-tree, treap, skip-list, sorted-vector, and hash alternatives empirically.

## Core Exposition

**Choose one formulation before writing code.** Classical red-black trees usually describe black NIL sentinels, arbitrary red-link orientation, parent pointers, and bottom-up fix-up. Left-leaning red-black trees orient red links left and use concise recursive/top-down transformations. Some LLRB algorithms encode 2–3 trees, others admit temporary 4-nodes. Linux, OpenJDK, Boost, and Princeton source differ in representation and repair details.

Document color ownership. Many implementations store a node color that conceptually colors the parent link; the root has no parent link but is normalized black. Null pointers may be interpreted black without allocated sentinel nodes, yet deletion code may require the parent of a missing child. Options include one shared NIL with carefully maintained parent context, explicit parent parameters, link references, or top-down avoidance of a bottom-up null deficit.

State black-height endpoints. Whether the starting node or NIL is counted changes the integer but not equality/height proof. A validator must use one convention consistently. This module's executable checker returns one for a null leaf, then adds one for each black internal node; it compares left/right results rather than publishing the absolute number.

**The height proof has two lemmas.** First, a node of black-height `b` roots at least `2^b-1` internal nodes (adjust indices for endpoint convention). Induct: each child has black-height at least `b-1`, so two minimum child subtrees plus the root establish the bound.

Second, no red-red edge means at least half the internal nodes along any downward path are black; red nodes can occur only between black nodes. Therefore height is at most twice black-height. Combining `n>=2^b-1` with `h<=2b` yields `h<=2log2(n+1)`. Search, min/max, bounds, and traversal start are `O(log n)`; reporting `k` range items adds `O(k)`.

The root-black rule simplifies statements but recoloring a red root black changes every root-to-leaf black count equally. Some theoretical definitions omit it without losing asymptotic height. Production code should still normalize and validate its chosen rule.

**The multiway correspondence explains colors.** Contract each red node/link with its black parent. A black node alone represents a 2-node; one red child can encode a 3-node; two red children can encode a 4-node in a 2–3–4 formulation. Equal black-height corresponds to all multiway leaves at one level. Red-red chains would overfill an encoded node.

LLRB imposes one canonical orientation so a 3-node has a left red link. This removes symmetric binary encodings but strengthens invariants: no red right link and no two consecutive left red links (and normally no consecutive red links at all). Princeton's LLRB repair sequence—rotate left on red right, rotate right on consecutive left red, flip colors on two red children—belongs to that variant.

Do not validate a classical OpenJDK/Linux tree with “no red right links”; classical valid trees allow them. Conversely, an LLRB checker that tests only classical invariants can miss loss of left-leaning canonical form, which may break its top-down algorithms.

**Rotations conserve sorted regions.** The ordered-region proof is identical to AVL. A left rotation promotes right child `y` and moves `y.left` into the demoted node's right link, preserving `A<x<B<y<C`. Red-black rotations also transfer/reassign colors according to the repair algorithm. In LLRB left rotation, promoted node takes the demoted node's incoming color and the demoted node becomes red.

Reconnect parent/root and the middle subtree before retiring no nodes—rotation changes ownership links, not content. Recompute demoted augmentation before promoted augmentation. If subtree size is stored, the promoted node often receives the old total while the demoted node recomputes, but using one general bottom-up recompute is easier to audit.

A color flip in LLRB toggles a parent and both children during top-down transformations. Some insertion presentations set parent red/children black under a known black-parent/two-red-child precondition rather than toggle. Mixing these semantics breaks deletion, where inverse flips may be required. Name preconditions and postconditions.

**Classical insertion preserves black-height initially.** Insert a new BST leaf colored red. Its NIL children are black; adding red contributes no black node, so existing black-height equality remains. Only a red parent can violate the no-red-red rule.

Let parent `p`, grandparent `g`, and uncle `u`. If `u` is red, recolor `p,u` black and `g` red, then continue at `g`; black-height below `g` is conserved while the violation moves upward. If `u` is black, an inner triangle first rotates `p` into an outer line, then rotate `g` and recolor promoted/demoted nodes to eliminate red-red while preserving black-height. Normalize root black.

The repair ascends at most tree height and performs at most two primitive rotations in the classical insertion algorithm, though recoloring may propagate to root. Comparator/allocation failure should occur before publishing the red leaf. Once linked, fix-up operations should be nonthrowing or transactional; otherwise callers can observe a violated tree.

**Deletion tracks the color physically removed.** Ordinary BST deletion reduces two-child removal to moving/copying a successor/predecessor association and physically removing a node with at most one non-NIL child. The color that matters is the removed/moved-away position's original color, not necessarily the originally requested node's color.

Removing red changes no root-to-NIL black count. Replacing a black node with a red child can recolor that child black, absorbing the deficit. Removing a black node with black/NIL child leaves one side of its parent short by one black; bottom-up algorithms model the child/position as double black.

Repair cases are symmetric; reason with deficit on left. Let sibling `s` be right, near=`s.left`, far=`s.right`. If sibling is red, parent is black under valid preconditions: rotate parent left and exchange colors, producing a black sibling configuration without resolving the deficit. Reclassify afterward.

If sibling is black with both children black, recolor sibling red. If parent was red, color it black and finish; if parent black, the deficit moves to parent. At root it disappears because all paths lost equally. This is the propagation case.

If sibling is black, far child black, and near child red, rotate sibling toward the deficit and recolor to convert near-red into far-red. Finally, with black sibling and red far child, rotate parent away from deficit; give promoted sibling the old parent color, color parent/far child black, and discharge the deficit. Exact assignments depend on representation, but black contributions can be checked on every external path.

Null/sentinel details cause many bugs. A null deficit has no parent/sibling unless passed explicitly. A shared NIL's parent cannot safely represent multiple concurrent positions. Code must not dereference missing near/far children as real nodes. Treat null as black in color predicates while retaining the structural context separately.

**Top-down LLRB deletion prevents descent into a 2-node.** Rather than create a deficit and repair upward, it moves a red link into the child direction before descending. `move_red_left` color-flips the current encoded node and, when the right child's left link is red, performs rotations/flips so the left side is not an isolated 2-node. `move_red_right` is symmetric for the right descent.

At return, `fix_up` restores left leaning, removes consecutive red links, splits temporary 4-nodes, and recomputes size. Before deletion, a black root with two black children may temporarily become red; after deletion, a nonempty root is normalized black. This coherent algorithm uses stronger invariants than classical repair.

The executable implementation deletes minimum key 1, then key 7, then root association 5. It counts every primitive rotation and color flip. Its finite traces do not prove that every internal deletion case was reached; exhaustive/model tests remain required.

**Augmentation and identity follow physical links.** Subtree size enables rank/select and must update after recursive mutation and rotations. Interval maximum, aggregate, min/max caches, and version summaries follow the same demoted-first dependency. Color is balance metadata, not part of logical serialization.

Association-copy deletion keeps the target node address but changes its key/value; successor node is destroyed. Physical transplant preserves successor association identity but rewires more parents/augmentations and repairs from its removal path. OpenJDK `TreeMap` has concrete deletion/iterator behavior; Boost.Intrusive/Linux embed or link user nodes differently. State the implementation's contract rather than infer from “red-black.”

Node-based rotations normally preserve references to nonerased payload nodes. Stack iterators can become structurally stale; parent-pointer successor may remain navigable if all parent links are correct and no unsynchronized mutation occurs. Fail-fast modification counters are bug detection, not thread safety.

**Memory representation changes costs.** A node adds color, often parent pointer, children, payload, augmentation, allocator padding/header. Color may pack into pointer alignment bits, but language provenance, masks, sanitizers, and architecture must permit it. Intrusive layouts embed links/color in domain objects, saving wrapper allocation while making membership/lifetime caller-owned.

Shared NIL sentinels reduce branches in some code but add global/address/parent concerns. Null-as-black saves allocated sentinels but demands safe predicates. Pool/arena allocation improves locality but retains slabs and changes reclamation. B-trees/sorted vectors can beat pointer trees for cache/page workloads despite similar/asymptotic search guarantees.

Compare AVL: AVL gives a tighter height constraint and stores height/balance; red-black permits taller trees and often repairs with fewer structural changes under mutation, but constants depend on algorithm and workload. Do not turn this tendency into a universal benchmark claim.

**Concurrency is a separate algorithm.** A rotation/recolor writes multiple shared fields. Readers can observe missing nodes, cycles, or inconsistent colors if publication is unsynchronized. External mutexes are simplest. Fine-grained locks need ordering and validation around parent/sibling changes. Persistent functional trees path-copy and publish one new root but allocate/reclaim versions.

Linux rbtree documentation leaves locking to the caller; OpenJDK `TreeMap` requires external synchronization for structural concurrent access. Lock-free chromatic/red-black variants relax invariants and use helping/descriptors plus safe reclamation; classical sequential cases cannot be made lock-free by replacing assignments with atomics.

Iterator snapshot/weak/lock-held semantics and memory reclamation must be defined. Epochs/hazards/GC protect nodes from premature reuse but do not ensure a consistent search/order view. Count retired generations and synchronization metadata in performance/memory evidence.

**Security and recovery remain layered.** Logarithmic comparison count prevents shape degeneration from sorted keys when invariants hold. It does not bound comparator/key-processing cost, total entries/bytes, range-output size, allocation, serialization, or request rate. A mutable/inconsistent comparator can destroy reachability.

Apply entry/key-byte/comparison/rotation/allocation/depth/time/concurrency/range-output limits, checked size arithmetic, comparator policy, and typed failures. Validate logical sorted input and rebuild; do not trust serialized pointers, colors, NILs, subtree sizes, or physical shape. A linear build from sorted keys requires a proven coloring algorithm; repeated insertion is simpler but `O(n log n)`.

Instrumentation should record size, height sampled/recomputed offline, black-height violations, red-red/right-red (variant-specific), rotations/recolors per operation, physical deletion case, comparisons, allocation/failure, iterator conflicts, and latency tails. An invariant violation is corruption, not ordinary imbalance to ignore.

**Testing combines model, exhaustive histories, and independent invariants.** Compare every put/update/get/delete/min/max/bound/range/rank/select with a reference ordered model. After every structural mutation independently check global BST bounds, unique reachability, root black, NIL black semantics, red-child rule, equal black-height, size/augmentations/parents, and variant-specific left leaning.

Force insertion red-uncle propagation, inner/outer black-uncle cases, root normalization, and internal/root rotations. For deletion cover removed red, black with red child, black deficit; red sibling; black sibling with black children and red/black parent; near-red conversion; far-red resolution; propagation through multiple ancestors; NIL child; immediate/deep successor; root/last node. Exhaust all permutations for small sets and all deletion orders; random tests alone may miss rare cases.

Inject allocator/comparator/value-copy/move/update/serialization failure and count destruction. Under concurrency, pause at every link/color publication and retirement, then use history/race/reclamation checking. Benchmark AVL, red-black variants, B-tree, sorted vector, skip list, and hash map over realistic/adversarial keys and operation/range mixes. Report height, black-height, comparisons, rotations/recolors, allocations/bytes, cache/TLB/branches, throughput/tails, toolchain/hardware, repetitions, uncertainty, and raw artifacts.

The executable trace implements a sequential unique-integer 2–3-style LLRB map with stored subtree sizes and top-down deletion. Its checker recomputes global bounds, no cycles, black root, no red right links, no consecutive red nodes, equal black-height, and exact subtree counts. It proves only this finite implementation behavior—not classical-case coverage, generic safety, stable handles, concurrency, or production performance.

<!-- bijux-verify: {"id":"llrb-insert-delete-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"before=1,2,3,4,5,6,7,8,9\nbefore_root=5\nbefore_size=9\nrotations_before=9\ncolor_flips_before=4\ndeleted_min=ONE\ndeleted_internal=SEVEN\ndeleted_root=FIVE\nafter=2,3,4,6,8,9\nafter_root=6\nafter_size=6\nrotations_after=14\ncolor_flips_after=10\ninvariant=True\nevidence=finite_llrb_trace\n","stderr":""}} -->
```python
from dataclasses import dataclass


RED = True
BLACK = False


@dataclass
class Node:
    key: int
    value: str
    color: bool = RED
    left: object = None
    right: object = None
    size: int = 1


class LLRBMap:
    def __init__(self):
        self.root = None
        self.rotations = 0
        self.color_flips = 0

    @staticmethod
    def is_red(node):
        return node is not None and node.color == RED

    @staticmethod
    def node_size(node):
        return node.size if node is not None else 0

    def update(self, node):
        node.size = 1 + self.node_size(node.left) + self.node_size(node.right)
        return node

    def rotate_left(self, top):
        promoted = top.right
        top.right = promoted.left
        promoted.left = top
        promoted.color = top.color
        top.color = RED
        self.update(top)
        self.update(promoted)
        self.rotations += 1
        return promoted

    def rotate_right(self, top):
        promoted = top.left
        top.left = promoted.right
        promoted.right = top
        promoted.color = top.color
        top.color = RED
        self.update(top)
        self.update(promoted)
        self.rotations += 1
        return promoted

    def flip_colors(self, node):
        node.color = not node.color
        node.left.color = not node.left.color
        node.right.color = not node.right.color
        self.color_flips += 1

    def fix_up(self, node):
        if self.is_red(node.right):
            node = self.rotate_left(node)
        if self.is_red(node.left) and self.is_red(node.left.left):
            node = self.rotate_right(node)
        if self.is_red(node.left) and self.is_red(node.right):
            self.flip_colors(node)
        return self.update(node)

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
            return self.fix_up(node)

        self.root = add(self.root)
        self.root.color = BLACK
        return bool(inserted)

    def move_red_left(self, node):
        self.flip_colors(node)
        if node.right is not None and self.is_red(node.right.left):
            node.right = self.rotate_right(node.right)
            node = self.rotate_left(node)
            self.flip_colors(node)
        return node

    def move_red_right(self, node):
        self.flip_colors(node)
        if node.left is not None and self.is_red(node.left.left):
            node = self.rotate_right(node)
            self.flip_colors(node)
        return node

    @staticmethod
    def minimum(node):
        while node.left is not None:
            node = node.left
        return node

    def delete_min_node(self, node):
        if node.left is None:
            return None
        if not self.is_red(node.left) and not self.is_red(node.left.left):
            node = self.move_red_left(node)
        node.left = self.delete_min_node(node.left)
        return self.fix_up(node)

    def delete(self, key):
        removed = []

        def erase(node):
            if key < node.key:
                if node.left is not None:
                    if not self.is_red(node.left) and not self.is_red(node.left.left):
                        node = self.move_red_left(node)
                    node.left = erase(node.left)
            else:
                if self.is_red(node.left):
                    node = self.rotate_right(node)
                if key == node.key and node.right is None:
                    removed.append(node.value)
                    return None
                if node.right is not None:
                    if not self.is_red(node.right) and not self.is_red(node.right.left):
                        node = self.move_red_right(node)
                    if key == node.key:
                        removed.append(node.value)
                        successor = self.minimum(node.right)
                        node.key, node.value = successor.key, successor.value
                        node.right = self.delete_min_node(node.right)
                    else:
                        node.right = erase(node.right)
            return self.fix_up(node)

        if self.root is None:
            raise KeyError(key)
        if not self.is_red(self.root.left) and not self.is_red(self.root.right):
            self.root.color = RED
        self.root = erase(self.root)
        if not removed:
            raise KeyError(key)
        if self.root is not None:
            self.root.color = BLACK
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

        def check(node, lower, upper, parent_red=False):
            if node is None:
                return 1, 0
            if id(node) in seen:
                raise AssertionError("cycle or shared node")
            seen.add(id(node))
            if lower is not None and not lower < node.key:
                raise AssertionError("lower bound")
            if upper is not None and not node.key < upper:
                raise AssertionError("upper bound")
            if self.is_red(node.right):
                raise AssertionError("right-leaning red link")
            if parent_red and self.is_red(node):
                raise AssertionError("consecutive red nodes")
            left_black, left_count = check(
                node.left, lower, node.key, self.is_red(node)
            )
            right_black, right_count = check(
                node.right, node.key, upper, self.is_red(node)
            )
            if left_black != right_black:
                raise AssertionError("black height")
            expected_size = 1 + left_count + right_count
            if node.size != expected_size:
                raise AssertionError("subtree size")
            black_height = left_black + (0 if self.is_red(node) else 1)
            return black_height, expected_size

        try:
            if self.is_red(self.root):
                return False
            check(self.root, None, None)
            return True
        except AssertionError:
            return False


tree = LLRBMap()
names = {1: "ONE", 5: "FIVE", 7: "SEVEN"}
for key in (5, 3, 7, 2, 4, 6, 8, 1, 9):
    assert tree.put(key, names.get(key, str(key)))
before = tree.keys()
before_root = tree.root.key
before_size = tree.root.size
rotations_before = tree.rotations
flips_before = tree.color_flips
assert tree.invariant()
deleted_min = tree.delete(1)
assert tree.invariant()
deleted_internal = tree.delete(7)
assert tree.invariant()
deleted_root = tree.delete(5)

print("before=" + ",".join(map(str, before)))
print(f"before_root={before_root}")
print(f"before_size={before_size}")
print(f"rotations_before={rotations_before}")
print(f"color_flips_before={flips_before}")
print(f"deleted_min={deleted_min}")
print(f"deleted_internal={deleted_internal}")
print(f"deleted_root={deleted_root}")
print("after=" + ",".join(map(str, tree.keys())))
print(f"after_root={tree.root.key}")
print(f"after_size={tree.root.size}")
print(f"rotations_after={tree.rotations}")
print(f"color_flips_after={tree.color_flips}")
print(f"invariant={tree.invariant()}")
print("evidence=finite_llrb_trace")
```

## Definitions and Notation

- `n,h`: live internal nodes and binary-tree height.
- `bh(x)`: black-height under the implementation's endpoint convention.
- `NIL`: conceptual/explicit black external leaf.
- **red-red violation**: adjacent red internal nodes/links.
- **black deficit/double black**: missing black contribution after physical deletion.
- `p,g,u`: parent, grandparent, uncle during insertion repair.
- `s,near,far`: sibling and its children relative to deletion deficit.
- **LLRB**: left-leaning red-black variant with stricter orientation rules.
- **physical removal site**: node/link actually removed after successor/predecessor reduction.
- **fix-up/move-red**: bottom-up normalization or top-down deficit-prevention transformation.

## Mechanisms, Invariants, or Proof Structure

The height proof combines minimum nodes per black-height with the prohibition on consecutive red nodes. The representation proof combines global BST bounds, exact reachability/lifetime, black root/NIL, red-child rule, equal black-height, and variant-specific orientation.

Insertion adds a red leaf, preserving black-height; recoloring propagates red-red upward or rotations/recoloring resolve inner/outer cases. Classical deletion follows the color at the physical removal site and conserves black contribution through sibling cases. LLRB deletion instead moves red links downward before descent and restores canonical orientation during return.

Every rotation/color operation has explicit preconditions, preserves ordered regions and content, reconnects the returned root, and updates augmentation bottom-up. Failure and concurrency additionally require staged publication, stable comparator/payload behavior, reader exclusion/validation, and safe reclamation.

## Alternatives and Trade-Offs

| Design | Strength | Cost or obligation |
|---|---|---|
| Classical bottom-up RB | common symmetric formulation | parent/sentinel and deletion-case complexity |
| Top-down classical | avoids return-path repair in variants | transforms during unsuccessful descent |
| LLRB | concise 2–3-oriented recursive code | stronger left-leaning invariant; distinct deletion behavior |
| Explicit shared NIL | uniform color/child code | parent/context and concurrency concerns |
| Null-as-black | less sentinel storage | deletion must retain missing-child context |
| Parent pointers | fix-up/successor navigation | bytes and inverse-link maintenance |
| Intrusive nodes | stable domain identity/fewer allocations | caller-owned membership/lifetime/locking |
| AVL | tighter height | more height metadata/repair writes |
| B-tree | high fanout/cache/page efficiency | split/merge/node-search complexity |
| Sorted vector | compact search/iteration | linear middle updates |

## Failure Modes and Misconceptions

- **“Red-black means approximately balanced.”** equal black-height and red adjacency yield a precise height theorem.
- **“Null children are irrelevant.”** NIL leaves define the path invariant and deletion color.
- **“Color belongs universally to nodes.”** many models treat it as the incoming link color.
- **“LLRB is just shorter classical code.”** it enforces a stronger encoding and coherent algorithms.
- **“Recoloring never changes black-height.”** only named coordinated recolorings conserve required path counts.
- **“Requested node color drives delete repair.”** the physical removed position's color matters.
- **“Sibling cases are memorized by left/right.”** derive near/far relative to current deficit after normalization.
- **“One delete rotation is enough.”** deficit can propagate; variants have different bounds/sequences.
- **“Rotation preserves every API handle.”** node layout and association replacement determine identity.
- **“Fail-fast iteration is synchronization.”** it is best-effort detection, not a memory model.
- **“One color bit makes nodes free.”** parents, links, allocator padding, augmentation, and locality dominate.
- **“Red-black always beats AVL.”** workload and implementation evidence choose the structure.

## Worked Examples

### Example 1

A path alternates black/red and has black-height `b`; it has at most roughly `2b` internal levels. Conclusion: no-red-red converts black-height into total-height control.

### Example 2

A black-height-3 subtree contains at least `2^3-1=7` internal nodes under matching conventions. Conclusion: black-height is logarithmic in population.

### Example 3

Inserting a red leaf under a black parent preserves all black counts and needs no repair. Conclusion: red is the least disruptive insertion color.

### Example 4

Red parent and red uncle are recolored black while black grandparent becomes red. Conclusion: split an encoded 4-node and move possible violation upward.

### Example 5

Red parent, black uncle, and an inner triangle first rotate parent, then rotate/recolor grandparent. Conclusion: normalize orientation before line repair.

### Example 6

Deleting a red leaf removes no black contribution. Conclusion: physical removed color determines whether a deficit exists.

### Example 7

A black deficit has black sibling with black children and black parent. Coloring sibling red equalizes local paths but transfers deficit to parent. Conclusion: deletion can propagate to root.

### Example 8

With black sibling and red far child, rotate parent away from deficit and recolor. Conclusion: borrow black capacity from the sibling side to discharge deficit.

### Example 9

An LLRB tree temporarily color-flips before descending left so the child is not a 2-node, then fixes orientation on return. Conclusion: top-down deletion prevents rather than later models double black.

### Example 10

A classical valid tree has a right red link. A left-leaning checker rejects it although classical invariants pass. Conclusion: validation must match the selected variant.

## Cross-Program Connections

- **Algorithms:** logarithmic bounds, 2–3–4 encodings, local conservation, and case symmetry connect binary and multiway trees.
- **Programming languages:** comparator laws, parent/sentinel representation, intrusive ownership, exceptions, moves, and iterator identity shape implementation.
- **Computer architecture:** pointer-heavy nodes, color packing, allocations, cache/TLB misses, and rotations affect constants.
- **Concurrent programming:** multi-link/color publication, locks, persistent paths, relaxed chromatic invariants, helping, and reclamation are separate proofs.
- **Operating systems:** intrusive red-black trees organize ordered kernel objects while delegating locking and payload ownership.
- **Database engineering:** red-black/2–3–4 correspondence prepares B-tree split/merge and ordered index reasoning.
- **Security engineering:** logarithmic shape removes sorted-input degeneration but not comparator, volume, allocation, corruption, or range-output attacks.

## References

1. Leonidas J. Guibas and Robert Sedgewick, [A Dichromatic Framework for Balanced Trees](https://sedgewick.io/wp-content/themes/sedgewick/papers/1978Dichromatic.pdf). Primary paper introducing the red/black framework, transformations, top-down updates, analysis, and concurrency discussion.
2. Princeton Algorithms, [Balanced Search Trees](https://algs4.cs.princeton.edu/33balanced/). Primary academic treatment of 2–3 encoding, left-leaning links, rotations, color flips, deletion, height, and operation bounds.
3. Princeton Algorithms, [`RedBlackBST`](https://algs4.cs.princeton.edu/code/javadoc/edu/princeton/cs/algs4/RedBlackBST.html). Primary implementation/API documentation for an augmented LLRB ordered symbol table and complexity contracts.
4. Pat Morin, [Open Data Structures: Red-Black Trees](https://opendatastructures.org/newhtml/ods/latex/redblack.html). Open academic treatment of red-black height, add/remove, and amortized rotations.
5. Linux Kernel, [Red-black Trees](https://docs.kernel.org/core-api/rbtree.html). Current official documentation for intrusive representation, caller-owned comparison/locking, search, insertion, erase, and traversal.
6. Linux Kernel, [`lib/rbtree.c`](https://github.com/torvalds/linux/blob/master/lib/rbtree.c). Current primary implementation source for parent/color encoding, rotations, insertion, deletion, replacement, and augmentation hooks.
7. OpenJDK Project, [`TreeMap.java`](https://github.com/openjdk/jdk/blob/master/src/java.base/share/classes/java/util/TreeMap.java). Current primary source for a classical red-black ordered map, comparator contract, navigation, deletion, iterators, and synchronization caveat.
8. Boost.Intrusive Project, [`rbtree_algorithms.hpp`](https://github.com/boostorg/intrusive/blob/develop/include/boost/intrusive/rbtree_algorithms.hpp). Current primary source for generic intrusive red-black initialization, insert, erase, rebalance, replace/swap, and invariants.
9. ISO C++ working draft, [Associative container requirements](https://eel.is/c%2B%2Bdraft/associative.reqmts). Current observable key-equivalence, complexity, iterator/reference, insertion, erase, and node-handle requirements without mandating red-black layout.
10. Rust Project, [`std::collections::BTreeMap`](https://doc.rust-lang.org/std/collections/struct.BTreeMap.html). Current B-tree ordered-map API used as a production high-fanout alternative and contract comparison.

## Exercises

### Exercise 1

Prove the red-black height bound from equal black-height and no consecutive red nodes. State precisely which nodes/endpoints your black-height counts.

### Exercise 2

Derive classical insertion repair from parent/uncle colors and inner/outer orientation. Prove each recoloring/rotation preserves BST order and black-height and terminates.

### Exercise 3

Derive classical deletion repair for a left-side black deficit using red sibling, black sibling with black children, near-red conversion, and far-red resolution. Mirror it and identify the physical removal color.

### Exercise 4

Compare a coherent LLRB top-down implementation with a classical parent/sentinel implementation across invariants, code, identity, iterators, augmentation, failure, and concurrency.

### Exercise 5

Design model, exhaustive-small-history, fault, lifetime, adversarial, concurrency, and benchmark evidence comparing red-black variants with AVL, B-tree, sorted vector, skip list, treap, and hash map.

## Answers to the Exercises

### Answer 1

Take NIL leaves as black and define `bh(x)` consistently as the black contribution along any x-to-NIL path. Induct that a subtree of black-height b has at least `2^b-1` internal nodes (with index adjustment if x/NIL counting differs): each child has sufficient black-height and contributes a minimum subtree. No red node has a red child, so on any root-to-NIL path red internal nodes are separated by black nodes; total internal height is at most twice the black internal count. Thus `n>=2^b-1` gives `b<=log2(n+1)` and `h<=2b<=2log2(n+1)`. Root-black normalization only strengthens/simplifies the statement.

### Answer 2

Insert a red leaf; black-height is unchanged, so only red parent violates. With red uncle, recolor parent/uncle black and grandparent red: paths through either child exchange one red/black contribution equally, and the possible violation moves two levels upward. With black uncle, rotate an inner parent-child triangle into an outer line if necessary, then rotate grandparent toward the line and assign promoted parent black/demoted grandparent red. Ordered-region rotation preserves all keys; every local NIL path retains the prior black count and red-red disappears. Each recolor moves the focus upward; the black-uncle case terminates locally; root is blackened. Height bounds the loop and at most two primitive rotations occur.

### Answer 3

Reduce BST deletion to a physical node with at most one non-NIL child and remember its original color. Red removal finishes; black with red child blackens the child. Otherwise track a left deficit. If right sibling is red, rotate parent left and exchange parent/sibling colors to obtain a black sibling, then reclassify. If black sibling has black near/far children, color sibling red; a red parent blackens and absorbs, while a black parent inherits the deficit. If far is black and near red, rotate sibling right and recolor so far becomes red. With black sibling/red far, rotate parent left, give sibling old parent color, blacken parent/far, and finish. Mirror left/right. Check black contributions after each case, recompute augmentations, and retain parent context for NIL deficits.

### Answer 4

Classical code permits red links either side, validates black root/NIL/no-red-red/equal black-height, commonly uses parents/sentinel and bottom-up fix-up, and maps directly to symmetric sibling cases. LLRB adds no red-right/canonical 2–3 encoding, recursively rotates/flips on insertion, moves red downward before deletion descent, and fixes up on return; a null representation works because context is carried by recursion. Neither case code can be imported into the other without proving shared intermediate invariants. Node-based rotations may preserve addresses, but association-copy deletion changes target identity; stack iterators remain invalidatable. Augmentations recompute demoted-first. Failure-safe allocation/comparison precedes linking; concurrent variants need locks/immutable publication/descriptors and reclamation beyond either sequential algorithm.

### Answer 5

Run every operation against a sorted reference map and independently check bounds, comparator equivalence, acyclic reachability/count, root/NIL black, red-child rule, equal black-height, parents/augmentations, in-order results, bounds/ranges, plus variant-specific left leaning. Exhaust insertion/deletion permutations for small key sets and classify every repair/physical removal case; add sorted/reverse/partially sorted and equivalent-key histories. Inject allocation/comparator/value/serialization failure and count lifetime events. Pause concurrent implementations at link/color publication and retirement; check histories/races/reclamation. Benchmark variants and alternatives over realistic/adversarial mixes with height/black-height, comparisons, rotations/recolors, allocations/bytes, cache/TLB/branches, throughput/tails, platform/toolchain, repetitions, uncertainty, and raw artifacts. Do not infer generic exception safety, lock-free correctness, or universal performance superiority from finite tests.
