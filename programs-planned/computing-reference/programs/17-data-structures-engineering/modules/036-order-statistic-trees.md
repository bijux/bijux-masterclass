---
module_id: DSE-036
program: Data Structures Engineering
level: 1
module_number: 36
title: Order-Statistic Trees
status: complete
last_verified: 2026-08-30
---

# Order-Statistic Trees

## One-Page Review

### Governing question

How can a balanced ordered tree answer rank, selection, and range-count queries in logarithmic time while subtree counts, duplicate semantics, rotations, deletion, overflow, identity, and concurrency remain correct?

### Essential definitions

- An **order-statistic tree** is an ordered tree augmented with subtree cardinality or weight.
- `size(null)=0` and `size(x)=1+size(x.left)+size(x.right)` for a unique-key map.
- `rank(k)` in this module is the number of stored keys strictly less than `k`; it is defined even when `k` is absent.
- `select(i)` returns the key of zero-based rank `i`, with `0<=i<size(root)`.
- A **lower-bound rank** is exactly the insertion position of a key among sorted distinct keys.
- `count([lo,hi))=rank(hi)-rank(lo)` under the module's half-open convention.
- A **weighted order-statistic tree** stores a nonnegative multiplicity/weight sum rather than physical-node count.
- An **augmentation** is locally maintainable when a node summary is computable from its payload and child summaries in bounded time.
- An **augmentation callback** propagates, copies, or recomputes metadata when the balancing implementation changes links.
- **rank consistency** includes `rank(select(i))=i` for every legal index and `select(rank(k))=k` for every stored unique key.

### Central model, mechanism, or theorem

At node `x`, let `left_size=size(x.left)`. For `select(i)`, descend left if `i<left_size`, return `x` if equal, otherwise descend right with `i-left_size-1`. For `rank(k)`, descend left when `k<=x.key`; when `k>x.key`, add `left_size+1` and descend right. Both follow one root-to-leaf path.

If the base tree has height `h`, rank/select cost is `O(h)`. A red-black, AVL, B-tree, or suitably randomized base supplies logarithmic height under its own guarantee. The size field does not balance an unbalanced BST by itself.

Local mutation changes counts only on affected ancestor paths and rotation neighborhoods. A rotation preserves the promoted subtree's total membership; recompute the demoted node from its new children before the promoted node. Insertion, deletion, split, join, bulk loading, copy/transplant, and persistence must all preserve exact summaries.

### Critical invariants

1. Global comparator bounds and duplicate/equivalence policy define one unambiguous sorted sequence.
2. Every node is reachable exactly once and `size(x)` equals an independent subtree count.
3. The base tree's balance invariant holds independently of size augmentation.
4. Every rotation/link change updates summaries in child-dependency order and reconnects the correct root/parent.
5. Rank and select use the same zero/one-based, strict/inclusive, node/multiplicity convention.
6. Counters cannot overflow for any representable legal container state; arithmetic is checked or the capacity is bounded.
7. Range endpoints and empty/reversed intervals have explicit semantics.
8. Readers never combine links and counts from different mutation states; publication and reclamation follow the concurrency contract.

### Common failures

- Calling a tree order-statistic without storing or efficiently deriving subtree totals.
- Mixing zero-based `select` with one-based rank formulas.
- Defining rank only for present keys, then misusing it for range counts or insertion positions.
- Updating only the inserted/deleted node, not every changed ancestor.
- Recomputing a promoted node before its demoted child after rotation.
- Copying a successor key/value but leaving the target's count/weight semantics inconsistent.
- Counting physical nodes when duplicates/multiplicities require logical occurrences.
- Using `rank(hi)-rank(lo)` while claiming a closed interval.
- Letting a narrow counter wrap and direct selection down the wrong branch.
- Reading count and child pointers without synchronization during mutation.

### Compact example

An AVL order-statistic map inserts keys `1..9`. It ends with root 4, height 4, five rotations, and exact in-order sequence. `select` produces every key in order. Ranks of `0,1,4,5,9,10` are `0,0,3,4,8,9`; absent endpoints work as lower-bound positions. `[3,8)` contains five keys. Deleting key 4 returns its payload and leaves `1,2,3,5,6,7,8,9`, root 5, exact size 8; `select(4)=6`, `rank(6)=4`, and the same range now has four keys.

### Connections

[DSE-031](031-binary-search-trees.md) defines ordered queries, [DSE-032](032-avl-trees.md) supplies the executable balance/rotation base, [DSE-033](033-red-black-trees.md) supplies another deterministic base, and [DSE-034](034-treaps.md) plus [DSE-035](035-splay-trees.md) supply split/join and adaptive alternatives. The [program roadmap](../ROADMAP.md) next develops Fenwick, interval, and segment trees.

## Governing Question

Which rank/select convention, multiplicity model, base-tree guarantee, augmentation update protocol, overflow policy, and evidence yield trustworthy dynamic order statistics rather than plausible but stale counters?

## Why This Matters

Ordered maps answer membership and neighbor queries, but many systems also ask positional questions: the median, kth task by priority, percentile boundary, number of keys below a threshold, page at offset, or count in a range. Recomputing a subtree's cardinality by traversal makes one decision linear. One cached summary per node turns the decision into constant work at each tree level.

The idea is broader than size. A locally composable summary transforms an ordered tree into an index for aggregates, intervals, sequences, hashes, and application-specific measures. Order statistics are the cleanest case because the algebra is addition and the independent oracle is an in-order list. They teach the engineering obligations that harder augmentations inherit.

The main risk is stale metadata. Ordinary search may still find keys when a size is wrong, while rank/select silently return plausible incorrect results. Corruption can persist far from the mutation that caused it. Correctness therefore combines base-tree invariants, summary equations, query inversion laws, failure/lifetime behavior, and independent recomputation.

## Prerequisites and Retrieval

Retrieve comparator equivalence, global bounds, lower/upper bounds, range semantics, deletion topology, identity, and serialization from [DSE-031](031-binary-search-trees.md). Retrieve rotations, demoted-before-promoted recomputation, AVL height repair, deletion cascades, and invariant testing from [DSE-032](032-avl-trees.md). Contrast red-black callbacks in [DSE-033](033-red-black-trees.md), split/merge augmentation in [DSE-034](034-treaps.md), and access-driven rewrites in [DSE-035](035-splay-trees.md). Retrieve integer/space cost and benchmarking from [DSE-004](004-time-space-and-allocation-cost.md) and [DSE-010](010-benchmarking-a-structure-without-misleading-results.md).

## Learning Objectives

After completing this module, you should be able to:

1. specify zero/one-based rank/select and strict/inclusive range semantics precisely;
2. derive rank and select from subtree counts and prove their path invariants;
3. explain why query complexity follows base-tree height rather than augmentation alone;
4. maintain size through insertion, update, deletion, rotation, split/join, and bulk build;
5. generalize physical-node counts to duplicates, multiplicities, and nonnegative weights;
6. design counter-width, overflow, capacity, and serialization policies;
7. preserve identity, iterators, exception safety, and publication across metadata changes;
8. validate counts independently and test rank/select inversion plus range identities;
9. compare pointer trees with Fenwick/segment trees, B-trees, sorted arrays, and database counts;
10. benchmark rank-heavy systems using representative updates, offsets, locality, and concurrency.

## Core Exposition

**Define the sequence before the metadata.** This module models a unique-key ordered map. Comparator-equivalent keys identify one association; updating its value does not change cardinality. In-order traversal defines a sequence of length `n`. `select(i)` uses zero-based position. `rank(k)` counts keys strictly smaller than `k`, whether or not `k` is stored.

Other conventions are legitimate. Texts may use one-based selection or rank as the count `<=k`. Multisets may rank occurrences or distinct keys. Weighted trees may select by cumulative mass. APIs must state one convention; formulas, tests, persistence formats, and callers must not infer it from the word “rank.”

The strict lower-bound rank is especially compositional. It is the sorted insertion index. `rank(hi)-rank(lo)` counts `[lo,hi)` without testing whether either endpoint exists. A closed interval `[lo,hi]` instead needs `upper_rank(hi)-lower_rank(lo)`, where upper rank counts keys `<=hi`, or an explicit membership adjustment. When `lo>=hi`, a half-open count is zero by policy rather than a negative unsigned subtraction.

**Store subtree cardinality.** For unique physical nodes, set `size(null)=0` and `size(x)=1+size(x.left)+size(x.right)`. The root gives total logical entries. A leaf has size one. The field can store full subtree size, or a representation may store only left-subtree count; full size usually simplifies rotations, root size, validation, split/join, and other augmentations.

The summary is locally computable in constant time from children. This is the augmentation criterion: if mutation changes a bounded set of links plus their ancestor paths, recompute affected summaries without traversing unaffected subtrees. The base structure determines how many nodes change and its height bound.

Adding size to an ordinary unbalanced BST does not make operations logarithmic. Rank/select follow height `h`, so they are `O(h)` and can be `Theta(n)` on a chain. AVL/red-black give worst-case `O(log n)`. Treaps give expected logarithmic paths under priority assumptions. Splay trees give amortized access guarantees and mutate during rank/select if those searches splay. B-trees store child counts across higher fanout.

**Select maintains a residual rank.** At node `x`, let `l=size(x.left)`. Exactly `l` subtree keys precede `x`. If requested `i<l`, the desired item lies left with unchanged index. If `i=l`, return `x`. If `i>l`, skip the entire left subtree and `x`, descend right with `i-l-1`.

The loop invariant is: the original requested item is the current subtree's residual-index item, and all skipped items are known smaller. Each step descends one level. Reject `i<0` or `i>=size(root)` before descent. In languages with unsigned indices, prevent a negative caller from converting to a huge value and ensure subtraction occurs only after `i>l`.

**Rank accumulates skipped prefixes.** Maintain `answer`, initially zero. At node `x`, if `k<=x.key`, no node at `x` or to its right is strictly smaller; descend left. If `k>x.key`, all `size(x.left)+1` items in the left subtree plus `x` are smaller; add them and descend right. On null, return the accumulated lower-bound position.

For a stored `k`, traversal reaches its node and returns accumulated prefix plus its left size. For an absent key, null termination yields the number of keys before its insertion point. Comparator equivalence rather than object equality decides the branch. A mutable or inconsistent comparator invalidates both search and rank.

`rank(select(i))=i` follows because selection's skipped prefix equals rank's accumulated prefix on the same ordered path. For every stored `k`, `select(rank(k))` is comparator-equivalent to `k`. These are powerful metamorphic tests but depend on exact size and a unique-key convention.

**Insertion repairs all affected summaries.** Ordinary insertion creates a leaf of size one. Every ancestor on the search path gains one, unless an equivalent key merely updates a value and count semantics ignore values. A recursive implementation recomputes while returning; an iterative parent-pointer implementation walks upward.

If the base tree rotates, link rewrites change subtree membership of the demoted and promoted nodes. For a left rotation with old root `x` and promoted `y=x.right`, update `x` after attaching the middle subtree, then `y` after attaching `x`. The promoted subtree's total should equal the old total, but general recomputation is easier to audit than clever copying. Red-black frameworks may expose copy/rotate/propagate callbacks; follow their preconditions exactly.

AVL insertion can stop height propagation after its first rebalance, but size still changed for every higher ancestor. Do not incorrectly stop all augmentation updates because balance height stabilized. Either recompute size on the full return path or maintain separate height-change and content-change signals.

**Deletion follows the physical removal site.** A leaf/one-child removal decreases every ancestor count on its old path. Two-child deletion often copies successor association into the target and physically removes the successor. Cardinality falls along the successor-removal path, not merely at the requested key's original position. The target's size may change through that path even though its address remains.

Physical transplant moves the successor node and rewires two neighborhoods. Preserve its association identity, then recompute both affected paths and all rotation neighborhoods. Base-tree deletion repair can rotate repeatedly. A callback contract may copy the old subtree summary to a replacement root and recompute the demoted node; hand-coded variants must prove equivalent behavior.

Deletion returning early when a child is null still requires ancestors to recompute. An absent deletion must not alter counts; a splay-based miss may alter shape but must preserve every size. Destruction/reclamation happens after structural authority changes and after concurrent readers/handles release the removed node.

**Duplicates require choosing what rank measures.** A multiset can represent each occurrence as a physical node ordered by `(key,unique_id)`, in which case size counts occurrences. Or one node stores `(key,multiplicity)` and summary `weight(x)=multiplicity(x)+weight(left)+weight(right)`. Rank by occurrence adds multiplicities; select returns the key whose cumulative interval covers the index.

Distinct-key rank and occurrence rank are different APIs. Zero multiplicity usually means remove the node; negative multiplicity is invalid. Large client weights may overflow even when node count fits. If weights are arbitrary measures, require nonnegative values for monotone selection. With signed sums, `select by cumulative weight` cannot safely decide from left totals because later negative values can reverse order.

Weighted selection finds the first position whose cumulative weight crosses a target. Define whether targets are integer occurrence indices, real thresholds, and whether equality selects the current node or next. A node with zero weight occupies a key position but no weighted interval. These boundary rules need examples and inverse properties suited to the measure.

**Counter representation is correctness, not an optimization footnote.** A 32-bit subtree size can wrap in a long-lived or multiplicity-weighted tree. Wrapped left size sends select into the wrong branch; wrapped range subtraction can produce a plausible number. Choose a type capable of representing the maximum legal total, reject capacity before mutation, and use checked addition.

The maximum node count may be bounded by address space, but compressed/on-disk structures, large weights, or remote aggregates can exceed local pointer counts. Serialization must version counter width and reject inconsistent/out-of-range values. Rebuilding counts from bounded logical records is safer than trusting serialized caches.

Counts also affect memory layout. Adding eight bytes can cross allocator/cache-line size classes, reducing locality. Packed or narrow counters save space only with proven bounds. Saturating counts preserve a “large” signal but cannot support exact selection above saturation and must not masquerade as exact rank.

**Split, join, persistence, and bulk build broaden update paths.** A key split partitions one search path and recomputes summaries on both returned spines. An index split uses left counts to divide by position. Join requires ordered domains and recomputes the boundary spine. The new root total must equal the checked sum of inputs.

Persistent path copying creates fresh nodes on changed paths; each fresh node computes size from immutable children. Shared untouched subtrees retain valid summaries. Publication of one new root supplies a coherent version, but allocation rollback and shared reclamation remain required.

Bulk build from sorted keys can choose balanced roots and compute size bottom-up in linear time. Repeated insertion is simpler but `O(n log n)` for a balanced implementation. Bulk-loading a B-tree must calculate per-child/subtree counts consistently across pages and account for partial final nodes.

**Higher fanout uses prefix child counts.** In a B-tree node with keys and children, selection must decide among child ranges and separator keys. Store child subtree counts and optionally prefix sums within the node. Search within a node may be linear in fanout, binary, or SIMD-accelerated. Total cost depends on height plus in-node work.

Updating a leaf propagates count deltas to ancestors; splits/merges redistribute keys/children and recompute local prefix counts. Page-level concurrency and crash recovery must publish keys, pointers, and counts consistently. A stale count can direct an offset query to the wrong page even when ordinary key lookup works.

Database `OFFSET k` over an ordered index is not automatically order-statistic selection. Many B-tree indexes do not store exact visible-row counts per subtree, and MVCC visibility varies by snapshot. Dead tuples, predicates, permissions, and concurrent versions make “row rank” query-specific. Exact rank indexes trade update/write complexity for positional queries.

**Concurrency must bind metadata to structure.** A reader at `x` needs a mutually consistent `x.left` and its size. During rotation, reading a new child with an old count can skip the wrong number. Atomic fields individually do not make the composite traversal linearizable.

Use an external lock, path locks with a proven order, immutable root snapshots, or optimistic version validation that restarts when any observed node changes. The operation's linearization point and iterator snapshot/weak/locked semantics must be documented. Epoch/hazard/GC lifetime protects nodes but not count consistency.

Maintaining a global exact rank under concurrent inserts may create contention along upper paths. Sharded approximate quantiles or relaxed counters may scale better, but then the API is not an exact order-statistic tree. State error/confidence/staleness instead of silently weakening exactness.

**Testing combines a list oracle with independent structural checks.** Maintain a sorted reference list/map. After every insertion, update, deletion, split, join, or version publication, compare in-order contents and total size. Recompute every subtree size from scratch, validate global bounds, base balance, reachability, parents, and lifetimes.

For all `i`, assert `select(i)==reference[i]` and `rank(select(i))==i`. For stored keys, assert inverse selection; for absent probes around/between/extreme keys, compare rank with binary-search insertion position. Test every half-open range against a reference slice/count, including equal and reversed endpoints under policy.

Exhaust small insertion/deletion permutations to cover rotations, immediate/deep successors, root replacement, cascading balance repair, and empty/singleton states. Force counter limits, checked overflow, duplicate/multiplicity transitions, zero weights, serialization corruption, and allocator/comparator/value failures. Under concurrency pause around link/count publication and reclamation, then check histories/races/restarts.

Benchmark against unaugmented ordered traversal, sorted vector, Fenwick/segment tree on dense coordinates, B-tree, skip list with spans, database indexes, and approximate sketches as relevant. Report size, height/fanout, rank/select/update mix, comparisons, rotations, metadata writes, allocations/bytes, cache/TLB/branches, contention/retries, throughput/tails, hardware/toolchain, repetitions, uncertainty, and raw artifacts.

The executable evidence implements a unique-integer AVL map with height and subtree-size augmentation, zero-based select, strict lower-bound rank, half-open range count, insertion, association-copy deletion, and an independent validator. It demonstrates only the finite trace below under successful allocation and Python exact integers—not generic overflow, duplicate weights, stable handles, concurrency, database visibility, or production performance.

<!-- bijux-verify: {"id":"avl-order-statistic-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"before=1,2,3,4,5,6,7,8,9\nbefore_root=4\nbefore_height=4\nbefore_size=9\nrotations_before=5\nselect_all=1,2,3,4,5,6,7,8,9\nranks=0:0,1:0,4:3,5:4,9:8,10:9\nrange_3_8=5\ndeleted=FOUR\nafter=1,2,3,5,6,7,8,9\nafter_root=5\nafter_height=4\nafter_size=8\nrotations_after=6\nselect_4=6\nrank_6=4\nrange_3_8_after=4\ninvariant=True\nevidence=finite_avl_order_statistic_trace\n","stderr":""}} -->
```python
from dataclasses import dataclass


@dataclass
class Node:
    key: int
    value: str
    left: object = None
    right: object = None
    height: int = 1
    size: int = 1


class OrderStatisticAVL:
    def __init__(self):
        self.root = None
        self.rotations = 0

    @staticmethod
    def node_height(node):
        return 0 if node is None else node.height

    @staticmethod
    def node_size(node):
        return 0 if node is None else node.size

    def update(self, node):
        node.height = 1 + max(self.node_height(node.left), self.node_height(node.right))
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

    def rebalance(self, node):
        self.update(node)
        balance = self.node_height(node.left) - self.node_height(node.right)
        if balance > 1:
            if self.node_height(node.left.left) < self.node_height(node.left.right):
                node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        if balance < -1:
            if self.node_height(node.right.right) < self.node_height(node.right.left):
                node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
        return node

    def put(self, key, value):
        def insert(node):
            if node is None:
                return Node(key, value)
            if key < node.key:
                node.left = insert(node.left)
            elif key > node.key:
                node.right = insert(node.right)
            else:
                node.value = value
            return self.rebalance(node)

        self.root = insert(self.root)

    def delete(self, key):
        removed = None

        def remove_min(node):
            if node.left is None:
                return node.right
            node.left = remove_min(node.left)
            return self.rebalance(node)

        def erase(node):
            nonlocal removed
            if node is None:
                return None
            if key < node.key:
                node.left = erase(node.left)
            elif key > node.key:
                node.right = erase(node.right)
            else:
                removed = node.value
                if node.left is None:
                    return node.right
                if node.right is None:
                    return node.left
                successor = node.right
                while successor.left is not None:
                    successor = successor.left
                node.key, node.value = successor.key, successor.value
                node.right = remove_min(node.right)
            return self.rebalance(node)

        self.root = erase(self.root)
        return removed

    def rank(self, key):
        node = self.root
        answer = 0
        while node is not None:
            if key <= node.key:
                node = node.left
            else:
                answer += 1 + self.node_size(node.left)
                node = node.right
        return answer

    def select(self, index):
        if index < 0 or index >= self.node_size(self.root):
            raise IndexError("order-statistic index is outside the tree")
        node = self.root
        while node is not None:
            left_size = self.node_size(node.left)
            if index < left_size:
                node = node.left
            elif index > left_size:
                index -= left_size + 1
                node = node.right
            else:
                return node.key
        raise AssertionError("validated index must resolve")

    def range_count(self, low, high):
        return 0 if low >= high else self.rank(high) - self.rank(low)

    @staticmethod
    def keys_from(node):
        if node is None:
            return []
        return OrderStatisticAVL.keys_from(node.left) + [node.key] + OrderStatisticAVL.keys_from(node.right)

    def validate(self):
        seen = set()

        def check(node, low, high):
            if node is None:
                return 0, 0
            identity = id(node)
            if identity in seen:
                raise AssertionError("node is repeated or cyclic")
            seen.add(identity)
            if not (low < node.key < high):
                raise AssertionError("global BST bound failed")
            left_size, left_height = check(node.left, low, node.key)
            right_size, right_height = check(node.right, node.key, high)
            if node.size != 1 + left_size + right_size:
                raise AssertionError("subtree size failed")
            if node.height != 1 + max(left_height, right_height):
                raise AssertionError("stored height failed")
            if abs(left_height - right_height) > 1:
                raise AssertionError("AVL balance failed")
            return node.size, node.height

        count, _ = check(self.root, float("-inf"), float("inf"))
        for index in range(count):
            if self.rank(self.select(index)) != index:
                raise AssertionError("rank/select inversion failed")
        return count == self.node_size(self.root) == len(seen)


tree = OrderStatisticAVL()
words = {1: "ONE", 2: "TWO", 3: "THREE", 4: "FOUR", 5: "FIVE", 6: "SIX", 7: "SEVEN", 8: "EIGHT", 9: "NINE"}
for item_key in range(1, 10):
    tree.put(item_key, words[item_key])
assert tree.validate()
print("before=" + ",".join(map(str, tree.keys_from(tree.root))))
print(f"before_root={tree.root.key}")
print(f"before_height={tree.root.height}")
print(f"before_size={tree.root.size}")
print(f"rotations_before={tree.rotations}")
print("select_all=" + ",".join(str(tree.select(index)) for index in range(tree.root.size)))
probes = [0, 1, 4, 5, 9, 10]
print("ranks=" + ",".join(f"{probe}:{tree.rank(probe)}" for probe in probes))
print(f"range_3_8={tree.range_count(3, 8)}")
print(f"deleted={tree.delete(4)}")
print("after=" + ",".join(map(str, tree.keys_from(tree.root))))
print(f"after_root={tree.root.key}")
print(f"after_height={tree.root.height}")
print(f"after_size={tree.root.size}")
print(f"rotations_after={tree.rotations}")
print(f"select_4={tree.select(4)}")
print(f"rank_6={tree.rank(6)}")
print(f"range_3_8_after={tree.range_count(3, 8)}")
print(f"invariant={tree.validate()}")
print("evidence=finite_avl_order_statistic_trace")
```

## Definitions and Notation

- `S`: sorted logical sequence represented by the tree.
- `n=|S|=size(root)`: logical cardinality.
- `size(null)=0`; `size(x)=1+size(x.left)+size(x.right)` for unique nodes.
- `rank(k)=|{x in S: x<k}|`: zero-based lower-bound rank.
- `select(i)=S[i]` for `0<=i<n`.
- `upper_rank(k)=|{x in S: x<=k}|` under comparator equivalence.
- `count([lo,hi))=rank(hi)-rank(lo)` when `lo<hi`.
- `m(x)`: node multiplicity/weight in a weighted variant.
- `weight(x)=weight(left)+m(x)+weight(right)`.
- `h`: base-tree height; rank/select are `O(h)`.
- **summary monoid**: identity plus associative combination used for a general augmentation.

## Mechanisms, Invariants, or Proof Structure

The query proof partitions every subtree into its left prefix, root item/mass, and right suffix. Select carries a residual index; rank accumulates skipped prefixes. Each descends one level, so complexity follows the base tree's height. Inversion follows because both account for identical prefixes under one convention.

The update proof treats size as a locally derived summary. Link changes invalidate only changed nodes and ancestors. Insert/delete update their physical paths; rotations recompute demoted before promoted; split/join update returned spines; persistence computes new path nodes; bulk build computes bottom-up. Base balance and global BST/reachability proofs remain independent.

The systems proof adds equivalence/duplicate/multiplicity semantics, checked counter capacity, failure atomicity, identity, iterator rules, coherent publication, safe reclamation, bounded logical serialization, and snapshot-aware database meaning. Independent full recomputation plus rank/select/range identities guards against plausible stale metadata.

## Alternatives and Trade-Offs

| Design | Strength | Cost or obligation |
|---|---|---|
| Full subtree size | simple total/select/rank/validation | counter bytes per node |
| Left-subtree count only | sufficient for rank/select | root total and rotations less symmetric |
| Physical duplicate nodes | straightforward occurrence order | tie ID, extra nodes, identity policy |
| Multiplicity per key | compact repeated keys | weighted arithmetic and occurrence semantics |
| AVL/red-black base | worst-case logarithmic queries | balance metadata/repair |
| Treap base | simple split/index operations | expected rather than deterministic height |
| Splay base | adapts to positional locality | rank/select mutate; amortized latency |
| B-tree with child counts | cache/page-friendly large index | prefix-count and crash/concurrency complexity |
| Sorted vector | direct `select`, binary-search rank | linear middle updates |
| Fenwick/segment tree | fast prefix/select on dense domain | coordinate universe/compression and separate payload map |
| Approximate quantile sketch | compact/scalable estimates | no exact rank/select and explicit error |

## Failure Modes and Misconceptions

- **“Order statistic means statistical sample formula.”** here it means positional queries in a dynamic ordered set.
- **“Size augmentation balances the tree.”** it supplies navigation; the base tree supplies height guarantees.
- **“Rank is universally defined.”** strict/inclusive and zero/one-based conventions differ.
- **“Present-key tests cover rank.”** absent lower-bound probes are essential.
- **“Insertion rotation fixes every ancestor field.”** ancestors above a height-stable AVL repair still need count updates.
- **“Deleting the requested node identifies the update path.”** two-child removal updates from the physical successor site.
- **“Copying the promoted size is always safe.”** callbacks and other augmentations may require ordered recomputation.
- **“Nodes and occurrences are the same.”** multiplicity changes the summary/query algebra.
- **“Machine size types cannot overflow.”** weighted/on-disk/distributed totals need explicit capacity.
- **“Atomic counters make concurrent select safe.”** links and summaries require one coherent version.
- **“Index OFFSET is logarithmic automatically.”** storage/MVCC indexes may not retain exact visible subtree counts.
- **“Passing rank/select inversion proves the whole tree.”** duplicate conventions or mutually consistent corruptions still require independent bounds/count validation.

## Worked Examples

### Example 1

At root 40 with left size 3, `select(3)` returns 40 under zero-based indexing. Conclusion: a node's rank within its subtree equals its left size.

### Example 2

At the same root, `select(6)` descends right with residual `6-3-1=2`. Conclusion: skip the entire left prefix and root exactly once.

### Example 3

For absent key 45, rank adds four at root 40 then descends right; the final result is its sorted insertion position. Conclusion: strict rank need not require membership.

### Example 4

Keys `{1,3,5,7}` give `count([3,7))=rank(7)-rank(3)=3-1=2`. Conclusion: half-open range counting needs no endpoint membership branch.

### Example 5

A left rotation promotes `y`; recomputing `y` before demoted `x` reads x's old size. Conclusion: metadata follows the new child-dependency graph.

### Example 6

Updating the value at equivalent key 5 changes no node count. Conclusion: logical cardinality follows the map's duplicate/update policy, not every `put` call.

### Example 7

A node for key 5 has multiplicity 100. Physical size is one but occurrence weight is 100. Conclusion: name whether rank/select operates on keys, nodes, or occurrences.

### Example 8

Deleting root 4 in the executable AVL copies successor 5 then removes its physical node; every ancestor on that removal/repair path recomputes. Conclusion: two-child deletion metadata follows physical topology.

### Example 9

A 32-bit left count wraps from `2^32-1` to zero; `select(0)` incorrectly descends left or returns the root. Conclusion: counter overflow is query corruption, not a cosmetic metric error.

### Example 10

An MVCC index contains ten physical versions but a snapshot sees six rows. Structural node count cannot answer the snapshot's sixth visible row without visibility-aware summaries. Conclusion: database rank semantics include snapshot/predicate state.

## Cross-Program Connections

- **Algorithms:** augmentation, inductive summaries, prefix decomposition, inverses, monoids, and lower bounds connect representation to queries.
- **Programming languages:** generic comparators, checked integers, option/error types, persistent nodes, and callback contracts determine safe APIs.
- **Database engineering:** B-tree child counts, MVCC visibility, offset pagination, selectivity, page splits, and recovery complicate logical rank.
- **Concurrent programming:** coherent link/count versions, path locks, immutable roots, optimistic retries, and reclamation govern linearizable selection.
- **Data engineering:** exact ranks/quantiles contrast with distributed/streaming approximate sketches and their error models.
- **Security engineering:** hostile sizes, overflow, deep trees, serialized metadata, and expensive endpoints require checked resource limits.
- **Software engineering:** reference lists, full summary recomputation, inversion laws, fault injection, invalidation matrices, and telemetry make augmentation maintainable.

## References

1. MIT OpenCourseWare 6.046J, [Lecture 9: Augmentation](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/fc870caae0e6812787bb5d50ea4d5e24_MIT6_046JS15_lec09.pdf). Primary academic treatment of locally maintainable tree augmentation, order-statistic rank/select, and update costs.
2. MIT OpenCourseWare 6.046J, [Augmenting Data Structures, Dynamic Order Statistics, Interval Trees](https://ocw.mit.edu/courses/6-046j-introduction-to-algorithms-sma-5503-fall-2005/resources/lecture-11-augmenting-data-structures-dynamic-order-statistics-interval-trees/). Primary lecture for order-statistic trees and augmentation methodology.
3. Carnegie Mellon University 15-210, [Ordered Sets and Augmented BSTs](https://www.cs.cmu.edu/afs/cs/academic/class/15210-f14/www/lectures/ordered.pdf). Academic chapter deriving rank, select, split-by-index, stored size, reduce, work/span, and persistent tree interfaces.
4. Stanford CS166, [Balanced Trees](https://web.stanford.edu/class/archive/cs/cs166/cs166.1166/lectures/06/Small06.pdf). Academic source for order statistics through a general augmentation framework and rotation-local maintenance.
5. Princeton Algorithms, [`RedBlackBST.java`](https://algs4.cs.princeton.edu/code/edu/princeton/cs/algs4/RedBlackBST.java.html). Primary implementation source for subtree size, zero-based select, strict rank, range count, and independent rank/size consistency checks.
6. Princeton Algorithms, [Binary Search Trees](https://algs4.cs.princeton.edu/32bst/). Academic exercises/reference for subtree-count certification and rank/select inversion.
7. GCC Project, [`tree_policy.hpp`](https://github.com/gcc-mirror/gcc/blob/master/libstdc%2B%2B-v3/include/ext/pb_ds/tree_policy.hpp). Current primary source defining policy-based order-statistics metadata and query interfaces.
8. GCC Project, [`order_statistics_imp.hpp`](https://github.com/gcc-mirror/gcc/blob/master/libstdc%2B%2B-v3/include/ext/pb_ds/detail/tree_policy/order_statistics_imp.hpp). Current primary implementation source for order lookup, rank lookup, comparator use, and metadata recomputation.
9. Linux Kernel, [Red-black Trees—augmented rbtrees](https://docs.kernel.org/core-api/rbtree.html). Current official callback contract for propagation, copy, rotation, insertion, erase, and interval-tree augmentation.
10. ISO C++ working draft, [Associative container requirements](https://eel.is/c%2B%2Bdraft/associative.reqmts). Current ordered-container equivalence, complexity, iterator/reference, insert/erase, and node-handle requirements used as observable-contract context.

## Exercises

### Exercise 1

Derive zero-based select and strict lower-bound rank. State loop invariants, prove termination/correctness for present and absent keys, and derive half-open range count.

### Exercise 2

Prove size maintenance for a left/right rotation and extend it to AVL/red-black insertion and two-child deletion. Identify physical paths and dependency order.

### Exercise 3

Design distinct-key, multiset-node, and multiplicity-weighted APIs. Specify rank/select, duplicates, zero weights, overflow, update, serialization, and inverse properties.

### Exercise 4

Design exhaustive, property, fault, lifetime, concurrency, and corruption tests for an order-statistic tree. Include an independent oracle and failures that ordinary lookup would miss.

### Exercise 5

Choose a structure for exact positional queries over a large concurrent/MVCC dataset and compare AVL/red-black, B-tree, sorted vector, Fenwick/segment tree, and approximate quantile sketches.

## Answers to the Exercises

### Answer 1

At node x let l=size(left). Select keeps the invariant that the desired original element is residual index i in the current subtree: go left if i<l, return x if equal, otherwise skip l+1 and go right with i-l-1. Legal indices terminate at a node because each descent strictly shrinks the subtree. Rank keeps `answer` equal to the number of proven-skipped keys smaller than k: for k<=x.key go left; for k>x.key add l+1 and go right. Null returns the lower-bound insertion position, so absence is handled naturally. The two algorithms account for identical prefixes, giving `rank(select(i))=i`. For lo<hi, keys counted by rank(hi) but not rank(lo) are exactly those satisfying lo<=key<hi; otherwise the module returns zero.

### Answer 2

For left rotation partition `A<x<B<y<C`. Before, `size(x)=1+|A|+1+|B|+|C|`; after transfer, recompute demoted x as `1+|A|+|B|`, then promoted y as `1+size(x)+|C|`, equal to the old total. Right rotation is symmetric. In insertion every search ancestor gains a node; rotations recompute their local pair, and higher ancestors still recompute size even if AVL height propagation stops. In red-black, recoloring changes no size but rotations/copy/transplant do. For two-child association-copy deletion, the count decrement originates where the successor is physically removed, continues through target/root, and every deletion-repair rotation recomputes demoted then promoted. Physical transplant has both detachment and installation neighborhoods; callback/caller ownership must cover both.

### Answer 3

A distinct-key map uses one node per comparator class, update replaces value, size counts nodes, rank is strict key count, and select returns a unique association. A multiset-node design orders `(key,stable_id)`, counts occurrences, and must define first/last-key rank and erase-one/all. A multiplicity design stores positive m, summary weight, rank sums multiplicities, and select returns the key whose cumulative interval contains the occurrence index; transition to zero removes the node. Arbitrary weighted selection requires nonnegative weights and precise threshold/equality rules. Use checked wide totals and reject mutations exceeding capacity; version serialization and rebuild summaries. Tests use key inversion for distinct mode and cumulative-bound properties for multiplicity because many indices may select the same key.

### Answer 4

Use a sorted list/map oracle for contents, lower-bound rank, selection, and ranges. After every operation independently validate global bounds, base balance, unique reachability, count, parents, true heights, every subtree size, and all indices/probes. Exhaust small insertion/deletion permutations, all rotation orientations, immediate/deep successor, root/last removal, duplicate updates, every absent gap/extreme, split/join boundaries, and counter limits. Inject comparator/value/allocation/callback/serialization failures and verify atomicity/destruction. Corrupt one internal count while preserving keys to ensure validation/rank tests catch what lookup misses. Pause concurrent writers at link/count/root publication and retirement; check histories, snapshot/retry semantics, races, overflow, leaks, and use-after-free.

### Answer 5

AVL/red-black give exact worst-case logarithmic pointer-tree rank/select with per-node counts, but upper-path writes can contend and locality is modest. A B-tree with child/prefix counts reduces height and suits pages, but splits/merges, MVCC visibility, WAL/recovery, and snapshot-specific counts are complex. A sorted vector gives direct select and binary-search rank with excellent scans but linear insertion. Fenwick/segment trees give prefix/select over a dense or compressed stable coordinate universe, often paired with a payload map; dynamic new coordinates complicate them. Quantile sketches scale for approximate percentiles but cannot answer exact selection/rank and require explicit error/confidence. For MVCC, first define whether rank is physical, latest committed, or snapshot/predicate visible. Prefer a counted B-tree when exact snapshot-aware positional queries justify write/recovery complexity; otherwise use keyset pagination or an approximate sketch. Validate crash recovery, concurrent snapshots, page counts, update contention, and p99.99 latency on representative data.
