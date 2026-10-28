---
module_id: DSE-034
program: Data Structures Engineering
level: 1
module_number: 34
title: Treaps
status: complete
last_verified: 2026-08-30
---

# Treaps

## One-Page Review

### Governing question

How can an ordered map obtain a random-BST shape from independent priorities while keeping its invariants, probability assumptions, split/merge algebra, implementation behavior, and adversarial limits explicit?

### Essential definitions

- A **treap** is simultaneously a binary search tree by key and a heap by priority.
- This module uses a **min-heap convention**: every parent priority is smaller than each child priority.
- A **randomized treap** assigns priorities independently from one common distribution; plain treap means only the two structural invariants.
- A **Cartesian tree** is the unique tree determined by distinct ordered keys and distinct priorities under the BST and heap constraints.
- **split(T,k)** returns treaps containing keys `<k` and `>=k`.
- **merge(L,R)** returns one treap, under the precondition that every key in `L` is smaller than every key in `R`.
- A **rotation formulation** inserts by ordinary BST placement and rotates a priority violation upward.
- A **split/merge formulation** treats those two operations as primitives from which insert and delete can be composed.
- An **implicit treap** uses in-order position, usually subtree size, instead of an explicitly stored search key.
- An **augmentation** is cached subtree information, such as size, aggregate, or interval maximum.

### Central model, mechanism, or theorem

For distinct keys and priorities, the minimum-priority item must be the root. Items with smaller keys must recursively form its left treap and larger keys its right treap. This proves existence and uniqueness by induction. The same shape is produced by inserting keys into an ordinary BST in increasing-priority order.

If priorities are independent, identically distributed, and continuous, their relative order is a uniformly random permutation independent of key order. A randomized treap therefore has the distribution of a random BST. Search, insert, delete, split, and merge have expected `O(log n)` path length; any particular realized tree can still have height `n`, so these are not per-operation worst-case guarantees.

Split follows one search path: when `root.key<k`, keep the root in the left result and split its right child; otherwise keep it in the right result and split its left child. Merge compares root priorities, chooses the heap-eligible root, and recursively merges only one boundary child. Both preserve key partitions, heap order, reachability, and augmentations when their preconditions hold.

### Critical invariants

1. Every node satisfies global comparator bounds, not merely parent-child key order.
2. Every parent precedes each child under the declared priority order and tie-break rule.
3. Each live node is reachable exactly once; the root owns the full set and no cycle exists.
4. Subtree size and every other augmentation equal a recomputation from children and payload.
5. Split produces disjoint, exhaustive key partitions; merge is called only on ordered domains.
6. A node's balancing priority is immutable while linked, or a priority change is implemented as removal and reinsertion.
7. Randomized bounds require priorities whose relative order is sufficiently uniform and independent of key order.
8. Publication, iterator identity, failure rollback, and reclamation are representation-specific contracts, not consequences of balance.

### Common failures

- Calling every heap-ordered BST “randomized” without stating how priorities were generated.
- Claiming worst-case logarithmic time from an expected random-shape theorem.
- Using a small priority domain without a deterministic collision rule.
- Letting clients choose priorities and then treating hostile shapes as impossible.
- Implementing only local parent-child BST checks, which miss deep bound violations.
- Merging interleaved key ranges or reversing the merge precondition.
- Losing the middle subtree in rotation or the boundary subtree in split/merge.
- Updating a priority in place and silently breaking heap order.
- Reusing a predictable seed as though it were adversarial protection.
- Publishing recursive rewrites to unsynchronized readers or reclaiming old nodes too soon.

### Compact example

Keys `2..8` have fixed priorities `40,20,30,10,25,15,35`. Regardless of whether those pairs are inserted in order `2,8,4,6,3,7,5` or reverse key order, uniqueness forces root 5 and the same Cartesian-tree shape. Splitting at 6 yields `{2,3,4,5}` and `{6,7,8}`; merging restores the exact original shape. Deleting root 5 merges its left and right children and leaves root 7. An independent checker validates bounds, min-heap order, unique priorities/reachability, sizes, and count after every stage.

### Connections

[DSE-031](031-binary-search-trees.md) supplies ordered-map semantics, [DSE-032](032-avl-trees.md) supplies rotation and augmentation proofs, and [DSE-033](033-red-black-trees.md) supplies the deterministic-balance comparison. The [program roadmap](../ROADMAP.md) continues with adaptive splay trees and augmented ordered structures.

## Governing Question

Which priority model, update formulation, split/merge contract, randomness policy, augmentation discipline, failure semantics, and evidence make a treap a trustworthy ordered structure rather than a probabilistic slogan?

## Why This Matters

Treaps separate two concerns unusually cleanly. Key order supplies dictionary semantics; priority order supplies shape. Once priorities are fixed, there is no balancing case table: the structure is the unique Cartesian tree for the item set. This makes split, merge, persistence, bulk set operations, interval augmentation, and proofs concise.

The simplicity can hide a serious qualification. A treap is not balanced merely because nodes have priorities. Expected logarithmic depth comes from a probability model: the relative priority order must behave like a random permutation independent of key order. A deterministic, exposed, biased, colliding, or adversarial priority source changes the guarantee. Production review must distinguish a deterministic invariant from a probabilistic performance claim.

Treaps also expose a reusable structural algebra. Split divides an ordered domain without scanning all items; merge joins already separated domains without ordinary per-key insertion. These primitives later support persistent sequences, parallel set union/intersection/difference, interval structures, and range transformations. Their elegance is valuable only when boundary ownership, augmentation, stack depth, random-source policy, and failure behavior remain explicit.

## Prerequisites and Retrieval

Retrieve global BST bounds, comparator equivalence, search/range semantics, three deletion topologies, identity, and ownership from [DSE-031](031-binary-search-trees.md). Retrieve rotations, returned subtree roots, middle-subtree conservation, augmentation order, and independent invariant checking from [DSE-032](032-avl-trees.md). Retrieve cost reasoning, adversarial testing, and benchmark discipline from [DSE-004](004-time-space-and-allocation-cost.md), [DSE-009](009-property-based-testing-of-data-structures.md), and [DSE-010](010-benchmarking-a-structure-without-misleading-results.md). Review representation and operation contracts in [DSE-002](002-representation-invariants.md) and [DSE-003](003-operation-contracts.md).

## Learning Objectives

After completing this module, you should be able to:

1. state and independently validate the global BST, priority-heap, reachability, and augmentation invariants;
2. prove uniqueness of a treap for fixed distinct key-priority pairs;
3. derive the equivalence between a randomized treap and a BST built from a random insertion permutation;
4. distinguish deterministic correctness from expected, high-probability, empirical, and worst-case claims;
5. implement insertion/deletion using rotations and using split/merge, preserving exact content;
6. prove split and merge from partition, ordering, heap, and termination invariants;
7. specify collision, duplicate-key, comparator, priority-update, and random-source policies;
8. maintain subtree size and other augmentations in ephemeral and persistent implementations;
9. design model, invariant, exhaustive, statistical, fault, lifetime, and concurrency tests;
10. choose among treap, AVL, red-black, splay, skip-list, B-tree, sorted-vector, and hash structures from workload evidence.

## Core Exposition

**Start with a deterministic object.** An item is `(key, priority, value)`. Under this module's convention, keys form a strict BST and priorities form a min-heap. Randomness is not part of the definition of a treap; it is one method for choosing priorities. This distinction lets us prove structural correctness for a fixed finite input before reasoning about distributions.

For every node `x`, all keys in `x.left` compare less than `x.key`, all keys in `x.right` compare greater, and `x.priority` is smaller than each child priority. Parent-child key checks are insufficient: a key can be on the correct side of its parent but on the wrong side of an ancestor. Validation therefore carries lower and upper key bounds through recursion.

Distinctness needs a policy. A map may reject comparator-equivalent duplicate keys or update the existing association without changing its priority. Priority collisions can be rejected, regenerated, or ordered by a stable secondary field such as a unique insertion ID or a deterministic key fingerprint. The theorem then applies to the resulting total priority order. Silently using `<=` on both children does not restore uniqueness and can make shape depend on insertion history.

**Uniqueness is recursive.** In a nonempty set of distinct pairs, the minimum-priority item must be the root; otherwise its ancestor would have a larger priority and violate min-heap order. The key invariant uniquely partitions every other item into smaller-key and larger-key sets. Apply the same reasoning recursively to both sets. The empty case is unique, so induction proves one treap for the entire set.

This theorem has an engineering consequence: two replicas with identical key-priority pairs and identical total ordering produce the same logical shape, independent of update order. It does not imply identical addresses, allocator layout, serialization bytes, augmentation bugs, or concurrent histories. Shape determinism also fails if replicas use different comparators, collation versions, floating-point NaN policy, priority collision rules, or key encodings.

**The random-BST equivalence supplies expected balance.** Imagine inserting all items into an ordinary unbalanced BST in increasing priority order. The first item is the minimum-priority root; recursively, the earliest priority within each key interval becomes that subtree's root. This is exactly the uniqueness construction.

If priorities are i.i.d. from a continuous distribution, every relative priority ordering is equally likely and ties have probability zero. Thus the induced shape has the same distribution as a BST built from a uniformly random key insertion permutation. For sorted ranks `1..n`, item `j` is an ancestor of item `i` exactly when it has minimum priority in the rank interval between them. The probability is the reciprocal of that interval length. Summing those indicator probabilities gives expected depth bounded by harmonic sums, hence `O(log n)`.

Expectation is over priority choices, not a promise about every realized tree. Priorities increasing with keys yield a chain. Search on that instance costs `Theta(n)` and recursive operations can overflow the call stack. Random treaps have logarithmic expected height and stronger tail results under stated models, but latency-critical systems may still require a deterministic height limit, an iterative algorithm, rebuild policy, or an AVL/red-black/B-tree alternative.

Do not confuse expected depth, expected height, and expected rotations. A randomly selected node's expected depth is logarithmic; maximum height is a different random variable. Seidel and Aragon analyze expected access/update behavior and rotation counts under their randomized-search-tree scheme. A finite benchmark can estimate a particular implementation/distribution; it cannot prove the theorem or guarantee a future tail.

**Insertion has two equivalent formulations.** In the rotation formulation, search by key and attach a new leaf exactly as in a BST. The key invariant now holds globally, but the new priority may precede its parent's. Rotate the new node upward across each violating parent. A right rotation promotes a left child; a left rotation promotes a right child. Each rotation preserves in-order key order, and promotion repairs one heap edge without invalidating heap order inside untouched subtrees.

Recursive insertion can perform the same work while unwinding. Insert into one child, compare that child's root priority with the current root, rotate if needed, recompute augmentation, and return the possibly new root. Allocation, key/value construction, and priority acquisition should occur before publication when they can fail. Comparator failure during descent leaves an unmodified tree; failures after linking require rollback or a documented nonthrowing repair path.

In the split/merge formulation, split the current tree around the new key, create one node, and merge the pieces in key order. A common recursive variant compares the new priority with the current root: when the new node should be above it, split the old tree around the key and attach the two results as children. Otherwise recurse into the correct child. The invariant proof is the same Cartesian-tree uniqueness expressed without explicit rotations.

Updating an existing map key should normally replace only the value, leaving its priority unchanged. Drawing a new priority for every value update changes shape, iterator behavior, write amplification, and reproducibility for no dictionary-semantic reason. If priority encodes an intentional weight that changes, remove the node and reinsert it under the new total order; prove identity and failure behavior.

**Deletion joins around the removed association.** In the rotation formulation, find the target and rotate it downward. When it has two children, promote the child with earlier heap priority; this keeps the promoted child above the other boundary. Continue until the target has at most one child, then unlink it. The number of rotations follows the target's descent.

In the merge formulation, deletion is smaller: replace the target subtree by `merge(target.left,target.right)`. The key-domain precondition holds because every left key is below the deleted key and every right key above it. Merge chooses the smaller-priority root. If it chooses the left root, recursively merge `left.right` with the right tree; if it chooses the right root, recursively merge the left tree with `right.left`. Only one boundary spine changes.

Map identity still matters. Directly merging children physically removes the requested node and preserves every other node association. An implementation that copies a successor association into the target instead has different reference/node-handle semantics. Values, priorities, destructor ownership, parent links, versions, and augmentations must follow the declared representation.

**Split is a search-path partition.** Define `split(T,k)=(L,R)` with all `L` keys `<k` and all `R` keys `>=k`. If `T.root.key<k`, the root belongs in `L`; its left subtree already belongs there, and only its right subtree can straddle the boundary. Split that right subtree, attach its left result back as `root.right`, and return root with the other result. The symmetric case places the root in `R` and splits its left child.

The proof maintains four facts: partition membership, disjoint/exhaustive content, heap order, and valid augmentations. Reattached children were already descendants of the same root, so their priority cannot precede it. Recursion descends one level and terminates at null. Work is proportional to the traversed height, expected `O(log n)` under the random model but worst-case `O(n)`.

Inclusive/exclusive semantics must be named. A split defined as `<=k`/`>k` is equally valid but not interchangeable. Comparator-equivalent keys, multiset occurrence ordering, and range endpoints require a consistent total order. Returning mutable roots transfers ownership: the original root must no longer be used as if it still represented the complete tree.

**Merge has a non-negotiable domain precondition.** For `merge(L,R)`, every key in `L` must be less than every key in `R`. If either is empty, return the other. Otherwise the earlier-priority root must become root to preserve heap order. If `L.root` wins, its left child is untouched and its right child becomes `merge(L.root.right,R)`; if `R.root` wins, its right child is untouched and its left child becomes `merge(L,R.root.left)`.

Why is the recursive call legal? In the first case, all keys in `L.root.right` remain below every key in `R`; in the second, every key in `L` remains below all keys in `R.root.left`. The chosen root precedes both existing child roots, so heap order holds. Content is the disjoint union. A production API should enforce, prove by construction, or debug-check the boundary precondition; an arbitrary merge of interleaved ranges can preserve local heap order while corrupting search semantics.

**Augmentations follow the rewritten spine.** The executable tree stores `size=1+size(left)+size(right)`. A rotation recomputes the demoted node before the promoted node. Split recomputes the root after replacing one child. Merge recomputes the selected root after recursive attachment. An independent validator must calculate true sizes rather than trust cached child sizes blindly.

Other decomposable subtree summaries work the same way: sum, min/max, interval maximum endpoint, hash, lazy sequence aggregate, or application-specific monoid. Each needs an identity value, combination order, overflow/error policy, and proof that local recomputation reflects logical content. Noncommutative sequence aggregates must preserve in-order direction.

An implicit treap removes explicit search keys and interprets a node's rank as `size(left)`. Split by position descends according to subtree sizes; merge preserves concatenation order. Lazy reversal or range-update tags can make sequence editing powerful, but tag composition/push order becomes part of the invariant. This module introduces that transfer only; a production implicit treap needs its own contract and exhaustive evidence.

**Persistence changes mutation into path copying.** Purely functional split and merge allocate new nodes along changed spines and share untouched subtrees. The old root remains a valid version, so readers can obtain snapshot semantics. This makes versions, rollback, and parallel divide-and-conquer attractive.

Structural sharing requires immutable nodes or disciplined copy-on-write. Reference counting, tracing GC, arenas, epochs, or another lifetime system must keep shared children alive. A failed allocation must leave old versions valid and release newly created partial paths. Path-copy cost is expected logarithmic under the random model and linear in a chain. Persistent does not mean leak-free or automatically safe for concurrent reclamation.

**Random-source design is part of the performance contract.** A pseudorandom generator can provide reproducible tests and statistically suitable priorities without cryptographic security. Record algorithm/version, seed policy, priority width, collision handling, and whether snapshots clone generator state. Python documents that its default generator is deterministic and unsuitable for security; this does not make it unsuitable for nonadversarial simulation, but it matters if an attacker can infer future priorities and choose keys/operations around them.

Using `priority=hash(key)` makes shape canonical without storing a generated priority, provided the hash behaves sufficiently like a random permutation for the workload and collisions have a total rule. A public stable noncryptographic hash lets an adversary search for correlated/colliding priorities. A keyed hash hides that mapping while the secret remains protected, but key rotation changes canonical shape and rebuild policy. No phrase such as “random enough” replaces a threat model and measurements.

A finite priority domain creates birthday collisions. Regeneration must avoid unbounded loops and specify deterministic replay. Pairing random bits with a unique monotonic ID removes ambiguity but reveals insertion chronology and still leaves the random component's quality relevant. Wide priorities reduce collision probability; they do not prove independence or protect a weak generator.

**Worst-case protection is a separate policy.** Options include accepting probabilistic tails, enforcing maximum depth and rebuilding with fresh priorities, using a deterministic balanced tree, keeping an emergency operation budget, or constructing priorities with a secret pseudorandom function. Rebuild must be transactional: construct and validate a new root, atomically publish it, then reclaim the old generation after readers release it.

A depth alarm does not repair a corrupt tree and may false-trigger on a rare valid random draw. Telemetry should distinguish invariant violation from unfavorable but valid shape. Record size, actual/sample height, search depths, rotations or split/merge path lengths, collision/regeneration counts, source/seed generation, rebuilds, allocation, and latency distributions.

**Iteration and concurrency remain explicit.** In-order iteration yields sorted keys. Rotations and ephemeral split/merge normally preserve addresses of surviving nodes, but stack-based iterators cache a path whose links may change. Persistent roots support snapshot iteration if shared nodes remain alive. Define whether mutation invalidates all iterators, only erased handles, or structural cursors.

Sequential recursive code is not made thread-safe by atomic root storage. A writer changes several child and augmentation fields; an unsynchronized reader can see lost nodes, repeated nodes, stale size, or reclaimed storage. External locking is the simplest policy. Immutable path copying plus atomic root publication provides coherent roots, but safe reclamation and generator/priority publication still need memory-order and lifetime reasoning.

Parallel treap set operations exploit split/merge and independent recursive subproblems. Expected work/depth results require their published model and algorithms; they do not follow automatically from spawning a task per recursive call. Grain size, allocator contention, duplicate policy, cancellation, deterministic priority agreement, and stack/depth bounds govern a real implementation.

**Serialization stores logical state and policy.** Do not trust serialized pointers, cached sizes, or claimed heap order. Decode bounded key/value/priority records with checked lengths, reject duplicates/collisions under policy, rebuild, and independently validate. Storing explicit priorities preserves logical shape across process versions only if comparator and tie rules are stable. Regenerating priorities changes shape but may be acceptable when only map contents are contractual.

**Testing has deterministic and statistical layers.** For every operation, compare logical contents and ranges with a reference ordered map. Independently validate global key bounds, heap edges, priority uniqueness/total ordering, acyclic unique reachability, exact count, augmentation, and optional parents. Exhaust all insertion and deletion permutations for small key/priority sets, plus every split boundary and legal merge partition.

Property tests should verify `merge(*split(T,k))` restores the same content and, for fixed distinct priorities, the same shape; split results are disjoint/exhaustive; deleting absent keys is nonmutating; value updates preserve priority; and rebuilding fixed pairs in different insertion orders produces the unique shape. Inject comparator, allocation, value construction, serialization, and cancellation failures.

Statistical tests address distribution claims separately: sample independent seeds, report height/depth/rotation quantiles and confidence/uncertainty, and compare with theoretical or independently simulated baselines. Include sorted, reverse, clustered, duplicate-equivalent, collision-forced, predictable-priority, and maximum-depth inputs. A passing finite distribution test is evidence against obvious generator/integration defects, never proof of independence or asymptotic bounds.

The executable evidence below is deliberately deterministic. Fixed priorities force one known Cartesian tree. It checks two insertion orders, split/merge reconstruction, root deletion, and all structural invariants. It proves only the observed finite trace under unique integer keys/priorities, sequential ownership, successful allocation, and Python's exact integer behavior. It does not test randomness, probabilistic bounds, generic comparators, exceptions, persistence, concurrency, or production performance.

<!-- bijux-verify: {"id":"treap-split-merge-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"before=2,3,4,5,6,7,8\nbefore_root=5\nbefore_height=3\nrotations_first_order=15\nsplit_left=2,3,4,5\nsplit_right=6,7,8\nmerge_restored_shape=True\nsecond_order_same_shape=True\nrotations_second_order=4\ndeleted=FIVE\nafter=2,3,4,6,7,8\nafter_root=7\nafter_height=4\nafter_size=6\ninvariant=True\nevidence=finite_treap_split_merge_trace\n","stderr":""}} -->
```python
from dataclasses import dataclass


@dataclass
class Node:
    key: int
    priority: int
    value: str
    left: object = None
    right: object = None
    size: int = 1


class TreapMap:
    def __init__(self):
        self.root = None
        self.rotations = 0

    @staticmethod
    def node_size(node):
        return 0 if node is None else node.size

    def update(self, node):
        node.size = 1 + self.node_size(node.left) + self.node_size(node.right)
        return node

    def rotate_left(self, top):
        promoted = top.right
        top.right = promoted.left
        promoted.left = top
        self.update(top)
        self.update(promoted)
        self.rotations += 1
        return promoted

    def rotate_right(self, top):
        promoted = top.left
        top.left = promoted.right
        promoted.right = top
        self.update(top)
        self.update(promoted)
        self.rotations += 1
        return promoted

    def put(self, key, priority, value):
        def insert(node):
            if node is None:
                return Node(key, priority, value)
            if key < node.key:
                node.left = insert(node.left)
                if node.left.priority < node.priority:
                    node = self.rotate_right(node)
            elif key > node.key:
                node.right = insert(node.right)
                if node.right.priority < node.priority:
                    node = self.rotate_left(node)
            else:
                if priority != node.priority:
                    raise ValueError("an update cannot change priority")
                node.value = value
            return self.update(node)

        self.root = insert(self.root)

    def split(self, node, key):
        if node is None:
            return None, None
        if node.key < key:
            node.right, greater = self.split(node.right, key)
            return self.update(node), greater
        smaller, node.left = self.split(node.left, key)
        return smaller, self.update(node)

    def merge(self, smaller, greater):
        if smaller is None:
            return greater
        if greater is None:
            return smaller
        if smaller.priority < greater.priority:
            smaller.right = self.merge(smaller.right, greater)
            return self.update(smaller)
        greater.left = self.merge(smaller, greater.left)
        return self.update(greater)

    def delete(self, key):
        removed = None

        def erase(node):
            nonlocal removed
            if node is None:
                return None
            if key < node.key:
                node.left = erase(node.left)
                return self.update(node)
            if key > node.key:
                node.right = erase(node.right)
                return self.update(node)
            removed = node.value
            return self.merge(node.left, node.right)

        self.root = erase(self.root)
        return removed

    @staticmethod
    def keys_from(node):
        if node is None:
            return []
        return TreapMap.keys_from(node.left) + [node.key] + TreapMap.keys_from(node.right)

    @staticmethod
    def height(node):
        if node is None:
            return 0
        return 1 + max(TreapMap.height(node.left), TreapMap.height(node.right))

    @staticmethod
    def shape(node):
        if node is None:
            return "#"
        return (
            f"{node.key}:{node.priority}("
            f"{TreapMap.shape(node.left)},{TreapMap.shape(node.right)})"
        )

    def validate(self):
        seen_nodes = set()
        seen_priorities = set()

        def check(node, low, high, parent_priority):
            if node is None:
                return 0
            identity = id(node)
            if identity in seen_nodes:
                raise AssertionError("node is repeated or cyclic")
            seen_nodes.add(identity)
            if node.priority in seen_priorities:
                raise AssertionError("priority is not unique")
            seen_priorities.add(node.priority)
            if not (low < node.key < high):
                raise AssertionError("global BST bound failed")
            if parent_priority is not None and node.priority < parent_priority:
                raise AssertionError("min-heap order failed")
            left_size = check(node.left, low, node.key, node.priority)
            right_size = check(node.right, node.key, high, node.priority)
            actual_size = 1 + left_size + right_size
            if node.size != actual_size:
                raise AssertionError("cached size failed")
            return actual_size

        count = check(self.root, float("-inf"), float("inf"), None)
        return count == self.node_size(self.root) == len(seen_nodes)


items = {
    5: (10, "FIVE"),
    3: (20, "THREE"),
    7: (15, "SEVEN"),
    2: (40, "TWO"),
    4: (30, "FOUR"),
    6: (25, "SIX"),
    8: (35, "EIGHT"),
}

first = TreapMap()
for item_key in [2, 8, 4, 6, 3, 7, 5]:
    item_priority, item_value = items[item_key]
    first.put(item_key, item_priority, item_value)
assert first.validate()
original_shape = first.shape(first.root)
print("before=" + ",".join(map(str, first.keys_from(first.root))))
print(f"before_root={first.root.key}")
print(f"before_height={first.height(first.root)}")
print(f"rotations_first_order={first.rotations}")

left, right = first.split(first.root, 6)
print("split_left=" + ",".join(map(str, first.keys_from(left))))
print("split_right=" + ",".join(map(str, first.keys_from(right))))
first.root = first.merge(left, right)
print(f"merge_restored_shape={first.shape(first.root) == original_shape}")
assert first.validate()

second = TreapMap()
for item_key in [8, 7, 6, 5, 4, 3, 2]:
    item_priority, item_value = items[item_key]
    second.put(item_key, item_priority, item_value)
assert second.validate()
print(f"second_order_same_shape={second.shape(second.root) == original_shape}")
print(f"rotations_second_order={second.rotations}")

print(f"deleted={first.delete(5)}")
print("after=" + ",".join(map(str, first.keys_from(first.root))))
print(f"after_root={first.root.key}")
print(f"after_height={first.height(first.root)}")
print(f"after_size={first.root.size}")
print(f"invariant={first.validate()}")
print("evidence=finite_treap_split_merge_trace")
```

## Definitions and Notation

- `T=(K,P,V,E)`: a treap with keys, priorities, values, and child edges.
- `k(x)`, `p(x)`: key and priority of node `x`.
- `L(T),R(T)`: root's left and right subtreaps.
- `size(null)=0`, `size(x)=1+size(x.left)+size(x.right)`.
- `height(null)=0`, `height(x)=1+max(height(x.left),height(x.right))`.
- `split(T,k)=(A,B)`: `A` contains exactly keys `<k`; `B` exactly keys `>=k`.
- `merge(A,B)`: defined under `max-key(A)<min-key(B)` (with empty sides allowed).
- **priority rank**: a priority's position in the total ordering; treap shape depends on ranks, not numeric gaps.
- **expected `O(f(n))`**: expectation over the declared random choices for each fixed legal input/history, unless stated otherwise.
- **with high probability**: a tail statement requiring a specified probability bound; it is not synonymous with expected.
- **ephemeral/persistent**: updates destroy the previous logical version / preserve it through immutable sharing.

## Mechanisms, Invariants, or Proof Structure

The deterministic proof starts from global key bounds and a total min-priority order. The minimum priority is forced to the root; key order forces the two item partitions; induction proves uniqueness. Inserting pairs by increasing priority creates the same tree, so i.i.d. continuous priorities induce the random-BST distribution. Indicator variables over rank intervals yield harmonic expected depths.

Rotation insertion first establishes BST order and moves a priority violation upward while preserving in-order regions. Merge deletion removes one association and combines its separated children by recursively promoting the earlier-priority boundary root. Split descends one boundary path, partitions content disjointly/exhaustively, and reattaches subtrees under ancestors that already precede them in priority. Recompute augmentation after each changed child and return the possibly new root.

The production proof adds collision/duplicate/comparator policies, failure atomicity, iterator/node identity, recursion limits, random-source threat model, publication, and reclamation. Deterministic invariant tests establish finite structural behavior; statistical experiments can detect distribution defects but cannot prove independence or asymptotic claims.

## Alternatives and Trade-Offs

| Design | Strength | Cost or obligation |
|---|---|---|
| Random generated priority | simple expected balance independent of key order | generator, collision, replay, adversary policy |
| Keyed-hash priority | canonical shape per secret/key | secret rotation and hash-quality dependency |
| Public hash priority | deterministic replica shape | adversarial correlation/collision exposure |
| Rotation updates | close to familiar BST mutation | parent/reconnect and rotation bookkeeping |
| Split/merge updates | concise algebra; persistence/set operations | strict key-domain and ownership contracts |
| Ephemeral nodes | low allocation and familiar handles | mutation invalidation and synchronization |
| Persistent path copying | snapshots, rollback, parallel decomposition | allocation and shared reclamation |
| Treap | simple expected logarithmic operations | linear worst-case realized height |
| AVL/red-black tree | deterministic logarithmic height | more balance metadata/repair structure |
| Splay tree | adaptive amortized locality, no priority | access mutation and no individual worst-case bound |
| B-tree/sorted vector | cache/page density | split/merge or linear middle updates |

## Failure Modes and Misconceptions

- **“Treap means randomly balanced.”** Treap names two order invariants; randomized balance needs an explicit priority model.
- **“Expected logarithmic means no slow operation.”** A legal treap can be a chain and one operation can be linear.
- **“A seeded PRNG is secure randomness.”** Reproducibility and unpredictability are different properties.
- **“Hashing keys makes independence automatic.”** public/weak hashes may correlate with or be searched by inputs.
- **“Priority collisions are harmless.”** without a total tie policy, uniqueness and update-order independence disappear.
- **“Merge combines any two treaps.”** all left keys must precede all right keys.
- **“Split can discard the original root safely.”** ephemeral split consumes/rewires ownership unless the API promises persistence.
- **“Local BST checks prove order.”** only ancestor bounds detect all misplaced descendants.
- **“Updating priority is like updating value.”** priority determines topology and must be repaired or reinserted.
- **“Augmentation updates itself.”** every rotation/split/merge spine needs dependency-ordered recomputation.
- **“Persistent means thread-safe.”** root publication and shared-node reclamation still need a concurrency protocol.
- **“A random benchmark proves the theorem.”** finite samples neither prove asymptotics nor the generator model.

## Worked Examples

### Example 1

Pairs `(5,10),(3,20),(7,15)` under min-heap order force key 5 to the root, key 3 left, and key 7 right. No insertion history is needed. Conclusion: fixed distinct pairs determine shape recursively.

### Example 2

Insert `(3,20)` then `(5,10)`. BST insertion makes 5 the right child, violating `10>=20`; one left rotation promotes 5 and preserves order `3<5`. Conclusion: rotate the priority violation upward without changing in-order content.

### Example 3

Priorities equal key ranks `1,2,3,4` create root 1 with a right chain. Search for 4 visits four nodes. Conclusion: heap order alone gives no height bound; the random model is essential.

### Example 4

For sorted ranks 1 through 8, rank 3 is an ancestor of rank 7 exactly when its priority is minimum among ranks 3 through 7, probability `1/5`. Conclusion: ancestor probabilities are interval-minimum events that sum to harmonic expected depth.

### Example 5

Split the executable tree at 6. Root 5 belongs left, so only its right subtree straddles the boundary; recursion returns `{6,7,8}` right and reconnects the smaller part under 5. Conclusion: split changes one search path and yields disjoint exhaustive partitions.

### Example 6

Merging `{2,3,4,5}` with `{6,7,8}` compares roots 5/7 with priorities 10/15, keeps 5, and recursively fills its right boundary. Conclusion: root priority selects the merge root, while the key-domain precondition makes recursion legal.

### Example 7

Attempt to merge keys `{1,9}` with `{3,4}`. Even if root priorities heap-order locally, placing the entire second tree on a boundary cannot satisfy `1,3,4,9` BST order. Conclusion: interleaved domains require set-union logic, not plain merge.

### Example 8

Two generated 32-bit priorities collide. Regenerating on one replica but breaking ties by insertion ID on another creates different total orders and shapes. Conclusion: collision policy is part of deterministic interoperability.

### Example 9

An interval treap rotates a node but updates the promoted node before the demoted child's interval maximum. The promoted cache reads stale input. Conclusion: augmentation recomputation follows child dependencies, demoted before promoted.

### Example 10

A persistent writer path-copies split results and atomically publishes a new root while a reader retains the old root. Both views are coherent, but freeing shared nodes immediately causes use-after-free. Conclusion: immutability supplies version consistency, not reclamation safety.

## Cross-Program Connections

- **Algorithms:** random permutations, indicator variables, harmonic sums, Cartesian trees, and divide-and-conquer set operations link probability to structure.
- **Programming languages:** algebraic recursive types, persistent sharing, comparator laws, exceptions, and ownership determine implementation contracts.
- **Concurrent and parallel programming:** immutable root publication, epochs/hazards, parallel split-based union, grain size, and cancellation govern scaling.
- **Security engineering:** predictable/hash-derived priorities, adversarial inputs, entropy, collision handling, resource limits, and secret rotation shape threat models.
- **Database engineering:** ordered indexes, range partitioning, join/split, interval augmentation, serialization, and page locality connect treaps to storage structures.
- **Software engineering:** deterministic replay, independent validators, fault injection, invalidation matrices, telemetry, and statistical evidence make probabilistic code reviewable.
- **Distributed systems:** canonical priorities can converge replica shape only with identical keys, comparator, hash/seed, collision rule, and versioned policy.

## References

1. Raimund Seidel and Cecilia R. Aragon, [Randomized Search Trees (Algorithmica version)](https://faculty.washington.edu/aragon/pubs/rst96.pdf). Primary paper for treap uniqueness, random-BST equivalence, expected access/update behavior, rotations, split/join, and weighted variants.
2. Cecilia R. Aragon and Raimund G. Seidel, [Randomized Search Trees (FOCS 1989)](https://faculty.washington.edu/aragon/pubs/rst89.pdf). Original primary conference paper introducing the randomized strategy and expected update analysis.
3. Cecilia R. Aragon, [Treaps](https://faculty.washington.edu/aragon/treaps.html). Author-maintained source index distinguishing treaps from randomized search trees and linking original work and implementations.
4. Pat Morin, [Open Data Structures: Treap—A Randomized Binary Search Tree](https://opendatastructures.org/ods-java/7_2_Treap_Randomized_Binary.html). Open academic derivation of heap/BST invariants, equivalence, operations, and expected bounds.
5. Carnegie Mellon University 15-210, [Parallel and Sequential Data Structures and Algorithms](https://www.cs.cmu.edu/afs/cs/academic/class/15210-f11/www/lectures/all.pdf). Academic lecture material for uniqueness, randomized priorities, split/join, persistence, and parallel sequence/set structure.
6. Guy E. Blelloch and Margaret Reid-Miller, [Fast Set Operations Using Treaps](https://www.cs.cmu.edu/~scandal/treaps.html). Primary project/paper source for split-based parallel union, intersection, difference, and their expected work/depth model.
7. Python Software Foundation, [`random`—Generate pseudo-random numbers](https://docs.python.org/3/library/random.html). Current official documentation for deterministic generator behavior, reproducibility limits, thread considerations, and non-security warning.
8. CPython Project, [`Lib/random.py`](https://github.com/python/cpython/blob/main/Lib/random.py). Current primary implementation source illustrating generator state, seeding, integer selection, and system-random separation.
9. ISO C++ working draft, [Random number generation requirements](https://eel.is/c++draft/rand.req). Current standard requirements distinguishing engines, distributions, state, and uniform random bit generators.
10. ISO C++ working draft, [Algorithms library ordering requirements](https://eel.is/c%2B%2Bdraft/alg.sorting). Current strict-weak-order and equivalence requirements used to define generic key order and duplicates.

## Exercises

### Exercise 1

Prove that a finite set of items with distinct keys and priorities has exactly one min-heap treap. State where both distinctness assumptions enter and give a deterministic collision policy that restores the theorem.

### Exercise 2

Trace `split(T,6)` and the inverse legal merge for the executable tree. Prove partition, content, heap, size, and termination invariants rather than relying on the printed result.

### Exercise 3

Implement deletion once by rotating the target downward and once by merging its children. Compare rotation/path behavior, physical identity, augmentation order, absent-key behavior, failure, and iterator consequences.

### Exercise 4

Design a priority policy for a public multi-tenant ordered service. Compare generated PRNG priorities, public key hashes, keyed hashes, collision rules, replay, secret rotation, maximum-depth response, and deterministic alternatives.

### Exercise 5

Design evidence for an ephemeral or persistent augmented treap: reference-model, exhaustive, property, distribution, fault, lifetime, concurrency, serialization, and benchmark checks. State which claims each class cannot prove.

## Answers to the Exercises

### Answer 1

For the empty set the tree is uniquely empty. For a nonempty set, min-heap order forces the unique minimum-priority item to be root. Its unique key partitions remaining items into keys less and greater; BST order forces those sets into left and right subtrees. By induction each partition has exactly one treap, proving existence and uniqueness. Distinct keys make the partition/map association unambiguous; distinct priorities force one root in every recursive subset. Restore a total priority order by comparing `(priority,stable_unique_id)` lexicographically. Every item then has a distinct composite priority. The ID's generation, persistence, and replica agreement become contractual; merely allowing equal priorities with non-strict heap edges does not prove unique shape.

### Answer 2

At root 5, `5<6`, so 5 stays in the left result and only its right subtree is split. At root 7, `7>=6`, so 7 stays right and its left subtree is split. Node 6 also stays right; its null left returns empty partitions. Reattach the returned smaller part to 7.left (none) and the returned larger part rooted at 6 as the right result's left boundary; reattach the left-returned null/appropriate boundary to 5.right. The final sets are `{2,3,4,5}` and `{6,7,8}`. Every original node follows exactly one comparison branch, so results are disjoint and exhaustive. Reattached nodes remain descendants of ancestors that already precede them in priority, and recomputation restores exact size. Recursion descends one edge per call. Legal merge has all left keys below all right keys; priority 10 at root 5 wins, recursion merges its right boundary with root 7, and uniqueness yields the original fixed-pair shape.

### Answer 3

Rotation deletion finds the node, repeatedly promotes the earlier-priority child across it, reconnects each returned subtree root, recomputes demoted then promoted augmentations, and finally unlinks the target. Merge deletion returns `merge(target.left,target.right)` and recomputes only ancestors on the search path plus the merge boundary. Both physically erase the requested node and can preserve all other node addresses; neither preserves cached path iterators automatically. Merge expresses the child-domain proof directly and may use fewer explicit primitives, while rotation integrates naturally with parent-pointer code and exposes rotation telemetry. An absent key must return a typed miss without changing shape/version. Comparator failure before mutation is nonmodifying; allocation-free deletion should make structural rewrites nonthrowing or transactional. Destruction/reclamation occurs only after readers/handles can no longer access the erased node.

### Answer 4

A public service cannot assume tenants are nonadversarial. Generated priorities from a process PRNG are simple and replayable when seeds/state are recorded, but exposed outputs/state may make future priorities predictable; generator snapshots and restarts need policy. A public stable hash gives canonical shapes but lets attackers search offline for bad correlations/collisions. A keyed pseudorandom function hides mapping while its secret remains safe; use a wide output plus a stable unique tie field, version the key/policy, and rebuild transactionally on rotation because priorities and shape change. Monitor actual depth and operation budgets; on threshold, rate-limit/rebuild or fail safely. If tail latency must be bounded for every legal state, choose AVL/red-black/B-tree rather than claiming cryptography converts an expected bound into a deterministic one.

### Answer 5

Compare every map/sequence operation with an independent ordered/sequence model; validate global bounds or implicit ranks, total heap order, unique reachability, count, augmentations, and contents after every mutation. Exhaust all small key and priority permutations, deletion orders, split boundaries, legal merges, collision paths, and absent/update cases. Properties include insertion-order-independent shape for fixed pairs and merge/split round trips. Across independent seeds, measure height/depth/rotation/path quantiles with uncertainty and adversarial generator/hash inputs; this detects defects but does not prove independence or asymptotics. Inject comparator/allocation/value/serialization/cancellation failures and count lifetimes. For persistent/concurrent versions, pause at publication/reclamation boundaries and check snapshots, histories, races, and leaks/use-after-free. Decode hostile bounded records and independently rebuild/validate. Benchmark alternatives using realistic sizes, operations, ranges, locality, hardware/toolchain, repetitions, tails, memory/cache/branch counters, and raw artifacts. None of this alone proves generic exception safety, security, lock-free correctness, universal superiority, or external review; those require the corresponding formal contract, threat/concurrency proof, and human/system evidence.
