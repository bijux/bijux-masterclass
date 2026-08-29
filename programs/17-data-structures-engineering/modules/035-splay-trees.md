---
module_id: DSE-035
program: Data Structures Engineering
level: 1
module_number: 35
title: Splay Trees
status: complete
last_verified: 2026-08-30
---

# Splay Trees

## One-Page Review

### Governing question

How can a binary search tree reorganize on every access, offer strong sequence-sensitive amortized guarantees without balance metadata, and still expose its latency, mutation, identity, concurrency, and proof boundaries honestly?

### Essential definitions

- A **splay tree** is a BST that moves an accessed node to the root through a prescribed sequence of rotations.
- **splaying** is that rootward restructuring operation.
- **zig** is the final single rotation when the accessed node has a parent but no grandparent.
- **zig-zig** handles two edges in the same direction by rotating the parent over the grandparent, then the accessed node over the parent.
- **zig-zag** handles opposite directions by rotating the accessed node over its parent and then over its grandparent.
- **bottom-up splaying** requires parent/ancestor access; **top-down splaying** partitions and assembles while descending.
- **amortized cost** bounds total cost across every legal sequence, not each operation separately and not an average over random inputs.
- A **weight** `w(x)>0`, **subtree weight** `s(x)`, **rank** `r(x)=log2 s(x)`, and **potential** `Phi=sum r(x)` form the standard access-lemma analysis.
- **static optimality**, **working-set**, **static-finger**, **dynamic-finger**, and **sequential-access** are distinct sequence-sensitive properties.
- **dynamic optimality** asks for constant competitiveness with the best offline dynamic BST; it remains conjectural for splay trees.

### Central model, mechanism, or theorem

Splaying preserves BST order by rotations but maintains no height/color/priority invariant. The double-rotation order matters: zig-zig first rotates the parent, unlike merely rotating the accessed node twice through arbitrary ancestors. With positive item weights, the Access Lemma bounds the amortized cost of splaying `x` by a constant times `r(root)-r(x)` plus a constant. Unit weights give `O(log n)` amortized access; insertion, deletion, split, and join inherit logarithmic amortized bounds when built from a constant number of splays and BST operations.

The guarantee is sequence-wide. One access may traverse and rotate a chain of length `n`. Its high actual cost is paid partly by a potential decrease that benefits later operations. A tree can remain linearly tall without being invalid.

Splaying also adapts to locality. Suitable weight choices yield static-optimality, static-finger, and working-set consequences; stronger separate analyses establish dynamic-finger and sequential-access results. As of August 2026, constant-factor dynamic optimality remains unproved. A July 2026 preprint establishes an `O(log log n * log^2 log log n)` competitive factor, up to an additive term and its stated sequence regime—not constant competitiveness.

### Critical invariants

1. Global comparator bounds, exact reachability, ownership, and payload association hold before and after every rotation.
2. Parent/root links and the transferred middle subtree are correct for each primitive rotation.
3. Zig, zig-zig, and zig-zag choose orientation and rotation order from the live ancestry after each rewrite.
4. Every augmentation is recomputed in child-dependency order on all changed nodes.
5. Successful access splays the declared node; unsuccessful access follows a documented policy, commonly splaying the last visited node.
6. Split/join/delete preconditions preserve exact, disjoint ordered content and physical identity policy.
7. Potential arguments account for both actual work and potential change across the entire sequence.
8. Reader synchronization, iterator validity, mutation failure, and reclamation are explicit because even reads restructure the tree.

### Common failures

- Saying “balanced” when no height invariant exists.
- Treating amortized `O(log n)` as worst-case `O(log n)` latency.
- Moving a node to root with repeated zig rotations and assuming the Access Lemma still applies.
- Reversing the zig-zig rotation order.
- Splaying only successful searches without reflecting miss policy in bounds/API behavior.
- Forgetting that `get`, lower-bound, and sometimes iteration helpers mutate topology.
- Losing the middle subtree, root, parent, or augmentation during rotation.
- Joining trees whose key domains overlap or are reversed.
- Using splay access under a read lock or exposing it through a logically `const` concurrent API.
- Calling dynamic optimality proved, or ignoring the assumptions/additive term of newer competitiveness work.

### Compact example

Inserting `5,3,7,2,4,6,8` and splaying each new key leaves root 8 and height 6 after 15 rotations: validity does not imply height balance. Accesses to 2, 7, and 6 move each to root using 4, 1, and 3 rotations. Repeating access to 6 costs no rotations. A miss for 9 splays last-visited 8. Deleting 5 splays it, joins the separated children, and produces sorted keys `2,3,4,6,7,8`, root 4, height 3, and exact size 6. An independent checker validates global bounds, parents, reachability, sizes, and count.

### Connections

[DSE-031](031-binary-search-trees.md) supplies BST contracts, [DSE-032](032-avl-trees.md) supplies rotation/augmentation proofs, [DSE-033](033-red-black-trees.md) supplies deterministic worst-case balance, and [DSE-034](034-treaps.md) supplies split/join and expected-versus-deterministic distinctions. The [program roadmap](../ROADMAP.md) continues with order-statistic and interval/segment structures.

## Governing Question

Which splaying policy, amortized proof, access/miss/update contract, augmentation scheme, worst-case latency guard, and synchronization model make a self-adjusting tree correct and useful for a real workload?

## Why This Matters

Balanced trees optimize a structural surrogate: keep all root-to-leaf paths short. Splay trees optimize reactively: make the item just used maximally accessible and reorganize its search path in a way whose total cost is provably controlled. No height, color, or random priority is stored. This can exploit skew, recency, locality, sequential scans, and split/join workloads that a fixed balanced shape does not express.

That adaptation changes the engineering contract. A lookup is a structural write. A single operation may be linear. Iterators and parent paths can change after any access. Read-mostly concurrency loses the usual separation between readers and writers. Persistence and logging pay for path rewrites. A system with a hard per-request latency budget may prefer AVL, red-black, B-tree, or a hybrid even when splay wins total comparison count.

Splay trees are also a premier case study in amortized analysis. Their shape can look terrible at an arbitrary instant, so pointwise inspection does not establish performance. The potential method relates work to a stored analytical resource across a sequence. That discipline transfers to dynamic arrays, disjoint sets, Fibonacci heaps, link-cut trees, caches, and online algorithms.

## Prerequisites and Retrieval

Retrieve strict global BST bounds, comparator equivalence, search/miss behavior, deletion identity, ordered iteration, and serialization from [DSE-031](031-binary-search-trees.md). Retrieve rotation regions, returned subtree roots, parent/root repair, demoted-first augmentation, fault injection, and handle semantics from [DSE-032](032-avl-trees.md). Contrast red-black worst-case balance in [DSE-033](033-red-black-trees.md), and retrieve split/join domain proofs plus expected-versus-worst-case language from [DSE-034](034-treaps.md). Review cost and benchmark discipline in [DSE-004](004-time-space-and-allocation-cost.md) and [DSE-010](010-benchmarking-a-structure-without-misleading-results.md).

## Learning Objectives

After completing this module, you should be able to:

1. state the splay-tree representation and operation contracts without inventing a height invariant;
2. trace and implement zig, zig-zig, and zig-zag with correct rotation order;
3. derive the Access Lemma using weights, ranks, potential, and local case inequalities;
4. distinguish actual, amortized, expected, worst-case, competitive, and empirical performance;
5. derive search, miss, insertion, deletion, split, and join from splaying;
6. explain static-optimality, working-set, finger, sequential-access, and dynamic-optimality claims at the right strength;
7. maintain parent links, subtree augmentations, payload identity, and failure safety across access mutation;
8. specify iterator, `const`, cache, serialization, and concurrency semantics for a self-adjusting map;
9. build reference-model, invariant, exhaustive, adversarial-sequence, fault, lifetime, and benchmark evidence;
10. choose splay versus deterministic balanced, randomized, high-fanout, contiguous, and hashed alternatives from workload and SLOs.

## Core Exposition

**A splay tree has ordinary BST validity and unusual operation semantics.** Every left-descendant key is smaller than its ancestor and every right-descendant key larger under one strict comparator policy. All nodes are reachable exactly once; ownership, parent links, size, and other augmentations remain consistent. There is deliberately no constraint on height, subtree-size ratio, color, or priority.

After locating an existing key, splay that node to the root. A miss must also have a contract. The common rule splays the last non-null node visited, which is the predecessor or successor boundary where the search terminated. This improves locality around the missing key and is convenient for split. Another implementation may leave misses unchanged, but then its exact operation analysis, mutation behavior, and interoperability differ.

Map updates of a comparator-equivalent key normally replace the value and splay the existing node. Insertion places a leaf and splays it. Deletion splays the target, detaches its left and right subtrees, then joins them. Thus the root often records the most recent access boundary, not a balance-selected median.

**Rotations preserve order, but the schedule creates the theorem.** Let accessed node `x`, parent `p`, and grandparent `g`. When `p` is root, zig rotates `x` over `p` once. If `x` and `p` are both left children, zig-zig right-rotates `p` over `g`, then `x` over `p`; the both-right case uses two left rotations. If their directions differ, zig-zag rotates `x` over `p`, then `x` over `g` in the opposite direction.

The first zig-zig rotation promotes the parent, not `x`. Repeatedly rotating `x` over its current parent also reaches the root and preserves BST order, but it is a different heuristic (“move to root”) and does not inherit the splay access lemma. The double-step reshapes not only the requested path but the ranks of side subtrees, creating the potential drop required by analysis.

Each primitive rotation transfers a middle subtree. A left rotation at `p` promotes `x=p.right`, assigns `p.right=x.left`, reconnects that middle child's parent, attaches `p` as `x.left`, and reconnects `x` to the old grandparent/root. Right rotation is symmetric. Read orientation from current links because the first rotation changes ancestry for the second.

For subtree augmentation, recompute the demoted node before the promoted node. In zig-zig, the first pair is updated before the second rotation consumes it; a general rotation primitive can do this locally. At the end, the splayed node's augmentation summarizes the whole tree. Interval maximum, sum, sequence hash, and lazy tags add their own combination/push rules.

**Amortized analysis is deterministic sequence analysis.** Let actual cost count visited nodes or a constant per rotation/search step. Choose positive weights `w(v)`, let `s(v)` be total weight in `v`'s current subtree, define rank `r(v)=log2 s(v)`, and potential `Phi(T)=sum_v r(v)`. Potential is analytical; it need not be stored.

For an operation changing tree `T` to `T'`, amortized cost is `actual + Phi(T')-Phi(T)`. Summing over operations telescopes: total actual cost equals total amortized cost minus final potential plus initial potential. With fixed positive weights, potential is bounded, so a sequence-wide amortized bound converts to a total actual bound plus an initial/final term.

The **Access Lemma** states, under a conventional cost model, that splaying `x` has amortized cost at most `3(r'(x)-r(x))+1`; constants shift with whether cost counts rotations or visited nodes and with log base. Since after splaying `x` its subtree is the whole tree, `r'(x)=r(root before)`. Unit weights give at most `O(log n)` amortized cost.

Do not assert that each access traverses `O(log n)` nodes. If the tree is a chain and the deep endpoint is accessed, actual cost is linear. That splay can greatly lower potential and rearrange the entire path, paying forward. Conversely, a zero-rotation access at root can increase no potential and is actually constant.

**The Access Lemma is local-to-global accounting.** For a zig, only two local subtree ranks change; the leftover `+1` covers the final single rotation. A double step costs two rotations. In zig-zig and zig-zag, compare the before/after subtree weights of `x,p,g`; all nodes outside this local region keep their rank.

The logarithm's concavity converts sums of child/subregion weights into bounded rank differences. For zig-zag, the two former sides of `x` become separated under `p` and `g`; for zig-zig, one must use the fact that the old `x` subtree and the new sibling-side region are disjoint portions of the new `x` subtree. The standard inequalities bound actual double-step cost plus local potential change by three times `x`'s rank increase. Summing steps telescopes `x`'s successive ranks.

This is a proof pattern, not a magic potential. Positive weights and a consistent subtree definition matter. Logs of zero are invalid, so null children contribute no node rank rather than weight zero nodes. If insertions/deletions change the universe/weights, account for their potential changes separately or reduce the operation to access plus controlled structural work.

**Standard operations use a constant number of splays.** Search descends by comparator and splays the found or last node. Insert can search/splay first, then create a root whose left/right children partition the former root, or perform ordinary leaf insertion and splay the new node. Duplicate-map insertion updates the association according to policy.

To delete key `k`, access it. If absent, the miss policy may already have changed shape but logical contents stay unchanged. If present, `k` becomes root. Detach `L=root.left` and `R=root.right`. If `L` is empty, publish `R`. Otherwise make `L` the working tree, access/splay its maximum; that maximum has no right child, so attach `R` there and recompute. Every key in `L` precedes every key in `R`, establishing join's domain precondition.

Split at `k` accesses `k` or the last boundary node. With an exact key at root, detach one side according to `<k`/`>=k` or `<=k`/`>k` semantics. With a miss, root is the predecessor or successor; one rotation/partition rule separates the boundary. Define whether split consumes an ephemeral tree or returns persistent versions, and define treatment of comparator-equivalent keys/multiset occurrences.

Join requires `max(L)<min(R)`. Splay `max(L)` to the root of `L`; its right link is null, so attach `R`. Calling this on interleaved domains silently corrupts global search order even though local parent-child comparisons near the root can appear plausible. Enforce or prove the boundary at the API.

**Access-sensitive theorems are not interchangeable.** With unit weights, the balance consequence gives logarithmic amortized operations. Assigning weights proportional to fixed access frequencies and applying the Access Lemma yields static optimality: over a sufficiently long sequence, total access cost is within a constant factor/additive term of the best fixed BST for those frequencies.

Choosing weights by distance from a fixed finger yields a static-finger bound. Varying analytical weights across time carefully yields the working-set theorem: recently accessed items can cost logarithmic in the number of distinct items accessed since their previous access. The dynamic-finger theorem relates access cost to rank distance from the preceding access, but it required a separate deeper proof; it should not be presented as an immediate one-line consequence of the basic lemma.

The sequential-access theorem says accessing all keys in sorted order from any initial splay tree takes linear total time. This is much stronger than applying `O(log n)` amortized access independently. Similar specialized results and conjectures concern traversal and deque sequences. Each has its own model: access-only versus updates, initial-tree/additive costs, successful keys, and unit-cost BST operations.

These bounds describe total abstract BST work, not automatic wall-clock superiority. Rotations write pointers and dirty cache lines; pointer layouts may miss caches; comparators and payloads vary; allocators and branches matter. A red-black or B-tree may win a uniform workload; a hash table may win exact lookup; a sorted vector may win immutable scans.

**Dynamic optimality is an online-competitiveness question.** Fix an access sequence. Compare splay's BST-model cost with the minimum cost of an offline dynamic BST allowed to know the whole sequence and rotate/restructure within the model. The dynamic-optimality conjecture asks whether splay is within a constant factor, with appropriate additive/initial terms, for every sequence.

It is incorrect to infer dynamic optimality from static optimality, the working-set bound, dynamic finger, or many successful benchmarks; those cover important but incomplete sequence families. It is also incorrect to say no progress has occurred since 1985.

As of the chapter's verification date, the July 2026 preprint *Splay trees are almost dynamically optimal* reports an `O(log log n * log^2 log log n)` competitive ratio, plus the paper's additive term, for sufficiently long sequences in its stated model. This is the first reported sublogarithmic ratio for splay trees and is major evidence, but the constant-factor conjecture remains open. The work is cited as a primary preprint, not described as settled peer-reviewed consensus; future revisions may change constants, conditions, or status.

**Top-down and bottom-up implementations are related but not textually interchangeable.** Bottom-up splaying follows parent pointers and directly matches zig case descriptions. Top-down splaying descends once while building temporary left and right trees, performing local rotations when two consecutive directions align, then assembles around the accessed/boundary node. It can avoid parent pointers and a second upward pass.

A top-down variant must prove that partition trees contain the right key ranges, boundary tails are maintained, middle subtrees are not lost, and final assembly restores reachability. Its exact rotation count and miss shape can differ from bottom-up code. Do not test one against an expected shape produced by the other unless the contract promises that shape.

Semi-splaying, conditional splaying, and thresholded access may reduce writes. They are different algorithms with different theoretical properties. “Splay only on insert/delete” turns ordinary lookup into nonadjusting BST search and can leave a chain permanently expensive. If a workload policy deliberately does this, benchmark and specify it rather than borrowing full-splay bounds.

**Augmentation complicates the self-adjusting advantage.** Subtree size supports rank/select and implicit sequences, but every rotation rewrites two cached sizes. Larger summaries—interval maxima, cryptographic hashes, materialized secondary structures—make rotations more expensive. Splay's abstract rotation bounds may not predict application cost when recomputing a subtree annotation is nonlinear or touches external state.

Require augmentation to be locally composable in bounded time for standard analysis. Push lazy tags before interpreting child order or rotating an implicit sequence. For noncommutative aggregates, preserve in-order combination exactly. Validate augmentation from payloads and children independently after each operation, including a miss that splays.

Splay trees are central inside link-cut trees, where preferred paths and auxiliary-tree splays represent a dynamic forest. That application adds path-parent semantics, lazy reversals, aggregate fields, and a different operation proof. It is not correct to paste a map splay implementation into a link-cut tree and assume dynamic-tree correctness.

**Identity and exception safety must cover reads.** Rotations normally preserve node addresses and logical key/value associations; deletion removes the requested physical node in the join formulation. Yet a stack iterator's saved ancestor path becomes stale after any access. Parent-pointer successor iteration may remain valid for live nodes if the implementation promises it, all parent links are correct, and no concurrent mutation occurs.

Comparator failure can occur while descending before splay begins, leaving topology unchanged. Once structural rewrites start, rotation and augmentation updates should be nonthrowing or transactional. A value update that throws before splaying raises a policy choice: leave shape unchanged, splay the found node anyway, or roll back both value and topology. Specify observable effects rather than relying on “lookup.”

Allocation for insertion should complete before linking. Deletion should detach exactly once, preserve all nonerased associations, and delay destruction until no iterator/reader can observe the node. Intrusive trees transfer lifetime responsibility to the caller; unlinking does not necessarily destroy payload.

**Constness and concurrency are unusually sharp.** A semantic lookup changes no key/value set but changes physical structure. In C++-like APIs, a `const find` cannot splay through ordinary object state without internal mutability or a separate nonadjusting path. Exposing both “peek” and “access” can clarify this, but only access receives splay locality/bounds.

A shared/read lock is unsafe for splaying because rotations write multiple links, parents, root, and augmentations. A coarse exclusive lock makes operations linearizable simply but serializes readers. Fine-grained splay locking is difficult: the access path changes bottom-up, rotations span child-parent-grandparent, and lock order can invert. Optimistic readers need version validation and safe lifetime.

Persistent path-copy splaying can publish one immutable root and preserve reader snapshots, but each access allocates/copies the changed path and rotation neighborhoods. Epochs, hazards, reference counting, or GC protect shared versions from reclamation; they do not by themselves define which version an operation observes. A nonadjusting read replica plus serialized adapting writer is another explicit trade-off.

**Storage, recovery, and security follow from the lack of shape validity.** Any acyclic globally ordered BST shape is structurally valid, including a chain. A deserializer therefore cannot reject pathological height merely as “not a splay tree.” It must impose independent depth/node/byte limits to protect stack, time, and memory.

Prefer serializing logical sorted associations and rebuilding under a declared policy. Persisting exact shape can preserve warmed locality but couples format to layout and may restore an adversarial chain. Validate bounds, count, parents, and augmentations; never trust pointers. An iterative decoder/traversal avoids hostile recursion.

Splaying prevents a fixed bad shape from necessarily staying bad under access, but one operation can still be linear and expensive comparators/keys remain attack surfaces. Bound key bytes, entries, comparisons, rotations, stack depth, allocation, range output, and request rate. If hard tail guarantees matter, use deterministic balance or an operation budget with typed fallback; do not call an amortized theorem a denial-of-service bound.

**Testing must inspect shape changes and total sequences.** Compare logical put/get/delete/min/max/bounds/ranges with an independent ordered model after every step. Independently verify ancestor bounds, acyclic unique reachability, exact count, parents, augmentations, root result under the access/miss policy, and physical association/lifetime rules.

Force all zig directions, four zig-zig/zig-zag orientations, root/no-rotation access, deep chains, hits, misses below/inside/above the range, duplicate update, absent delete, root/internal delete, empty-side join, and every split boundary. Exhaust small initial BST shapes and access sequences, not only insertion orders. Check that each successful access ends at root and that a declared miss splays the last visited boundary.

For amortized evidence, record per-operation search steps, rotations, height, potential under chosen weights, potential delta, and cumulative actual/amortized costs. Recompute the potential independently. A finite ledger can catch accounting/code mistakes, but it does not prove the Access Lemma for all trees. Adversarial sequences should seek high individual cost, repeated alternation, scans, working sets, locality shifts, and cases where extra writes lose to balanced alternatives.

Inject comparator/value/allocation/augmentation/serialization/cancellation failures at every boundary. For concurrency, pause at each link/root/parent publication and retirement; test histories, races, deadlocks, iterator use, and reclamation. Benchmark splay against AVL, red-black, treap, B-tree, sorted vector, skip list, and hash map with realistic key distributions and access sequences. Report comparisons, rotations/writes, depths, allocations/bytes, cache/TLB/branches, throughput/tails, warm-up, hardware/toolchain, repetitions, uncertainty, and raw artifacts.

The executable evidence implements a sequential unique-integer bottom-up splay map with parent pointers, stored sizes, last-visited miss splaying, physical target deletion, and join-by-splaying-left-maximum. It proves only the exact finite history below under successful allocation and Python exact-integer comparisons. It does not empirically establish the Access Lemma, locality theorems, competitive ratios, generic failure safety, iterator guarantees, concurrency, or production performance.

<!-- bijux-verify: {"id":"splay-access-delete-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"after_insert=2,3,4,5,6,7,8\ninsert_root=8\ninsert_height=6\ninsert_rotations=15\nget_2=TWO root=2 rotations=4\nget_7=SEVEN root=7 rotations=1\nget_6=SIX root=6 rotations=3\nrepeat_6=SIX root=6 rotations=0\nmiss_9=None root=8 rotations=2\ndeleted_5=FIVE\nafter_delete=2,3,4,6,7,8\nafter_root=4\nafter_height=3\nafter_size=6\ninvariant=True\nevidence=finite_splay_access_delete_trace\n","stderr":""}} -->
```python
from dataclasses import dataclass


@dataclass
class Node:
    key: int
    value: str
    left: object = None
    right: object = None
    parent: object = None
    size: int = 1


class SplayMap:
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
        middle = promoted.left
        parent = top.parent
        promoted.parent = parent
        if parent is None:
            self.root = promoted
        elif top is parent.left:
            parent.left = promoted
        else:
            parent.right = promoted
        promoted.left = top
        top.parent = promoted
        top.right = middle
        if middle is not None:
            middle.parent = top
        self.update(top)
        self.update(promoted)
        self.rotations += 1

    def rotate_right(self, top):
        promoted = top.left
        middle = promoted.right
        parent = top.parent
        promoted.parent = parent
        if parent is None:
            self.root = promoted
        elif top is parent.left:
            parent.left = promoted
        else:
            parent.right = promoted
        promoted.right = top
        top.parent = promoted
        top.left = middle
        if middle is not None:
            middle.parent = top
        self.update(top)
        self.update(promoted)
        self.rotations += 1

    def splay(self, node):
        while node.parent is not None:
            parent = node.parent
            grandparent = parent.parent
            if grandparent is None:
                if node is parent.left:
                    self.rotate_right(parent)
                else:
                    self.rotate_left(parent)
            elif node is parent.left and parent is grandparent.left:
                self.rotate_right(grandparent)
                self.rotate_right(parent)
            elif node is parent.right and parent is grandparent.right:
                self.rotate_left(grandparent)
                self.rotate_left(parent)
            elif node is parent.right and parent is grandparent.left:
                self.rotate_left(parent)
                self.rotate_right(grandparent)
            else:
                self.rotate_right(parent)
                self.rotate_left(grandparent)
        return node

    def put(self, key, value):
        if self.root is None:
            self.root = Node(key, value)
            return None
        node = self.root
        while True:
            if key < node.key:
                if node.left is not None:
                    node = node.left
                else:
                    node.left = Node(key, value, parent=node)
                    node = node.left
                    break
            elif key > node.key:
                if node.right is not None:
                    node = node.right
                else:
                    node.right = Node(key, value, parent=node)
                    node = node.right
                    break
            else:
                previous = node.value
                node.value = value
                self.splay(node)
                return previous
        ancestor = node.parent
        while ancestor is not None:
            self.update(ancestor)
            ancestor = ancestor.parent
        self.splay(node)
        return None

    def get(self, key):
        node = self.root
        last = None
        while node is not None:
            last = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                self.splay(node)
                return node.value
        if last is not None:
            self.splay(last)
        return None

    def delete(self, key):
        value = self.get(key)
        if self.root is None or self.root.key != key:
            return None
        removed = self.root
        left = removed.left
        right = removed.right
        if left is not None:
            left.parent = None
        if right is not None:
            right.parent = None
        removed.left = None
        removed.right = None
        removed.parent = None
        if left is None:
            self.root = right
        else:
            self.root = left
            maximum = left
            while maximum.right is not None:
                maximum = maximum.right
            self.splay(maximum)
            self.root.right = right
            if right is not None:
                right.parent = self.root
            self.update(self.root)
        return value

    @staticmethod
    def keys_from(node):
        if node is None:
            return []
        return SplayMap.keys_from(node.left) + [node.key] + SplayMap.keys_from(node.right)

    @staticmethod
    def height(node):
        if node is None:
            return 0
        return 1 + max(SplayMap.height(node.left), SplayMap.height(node.right))

    def validate(self):
        seen = set()

        def check(node, low, high, parent):
            if node is None:
                return 0
            identity = id(node)
            if identity in seen:
                raise AssertionError("node is repeated or cyclic")
            seen.add(identity)
            if node.parent is not parent:
                raise AssertionError("parent link failed")
            if not (low < node.key < high):
                raise AssertionError("global BST bound failed")
            left_size = check(node.left, low, node.key, node)
            right_size = check(node.right, node.key, high, node)
            actual_size = 1 + left_size + right_size
            if node.size != actual_size:
                raise AssertionError("cached size failed")
            return actual_size

        count = check(self.root, float("-inf"), float("inf"), None)
        return count == self.node_size(self.root) == len(seen)


tree = SplayMap()
values = {2: "TWO", 3: "THREE", 4: "FOUR", 5: "FIVE", 6: "SIX", 7: "SEVEN", 8: "EIGHT"}
for item_key in [5, 3, 7, 2, 4, 6, 8]:
    tree.put(item_key, values[item_key])
assert tree.validate()
print("after_insert=" + ",".join(map(str, tree.keys_from(tree.root))))
print(f"insert_root={tree.root.key}")
print(f"insert_height={tree.height(tree.root)}")
print(f"insert_rotations={tree.rotations}")

for item_key in [2, 7, 6]:
    before = tree.rotations
    found = tree.get(item_key)
    print(f"get_{item_key}={found} root={tree.root.key} rotations={tree.rotations - before}")
    assert tree.validate()

before = tree.rotations
print(f"repeat_6={tree.get(6)} root={tree.root.key} rotations={tree.rotations - before}")
before = tree.rotations
print(f"miss_9={tree.get(9)} root={tree.root.key} rotations={tree.rotations - before}")
print(f"deleted_5={tree.delete(5)}")
print("after_delete=" + ",".join(map(str, tree.keys_from(tree.root))))
print(f"after_root={tree.root.key}")
print(f"after_height={tree.height(tree.root)}")
print(f"after_size={tree.root.size}")
print(f"invariant={tree.validate()}")
print("evidence=finite_splay_access_delete_trace")
```

## Definitions and Notation

- `x,p,g`: accessed node, its current parent, and current grandparent.
- `w(x)>0`: fixed analytical weight of item `x` for one Access-Lemma application.
- `s(x)=sum_{y in subtree(x)} w(y)`: subtree weight.
- `r(x)=log2 s(x)`: rank.
- `Phi(T)=sum_{x in T} r(x)`: tree potential.
- `a_i`: actual cost of operation `i` in a stated unit-cost model.
- `ahat_i=a_i+Phi(T_i)-Phi(T_{i-1})`: amortized cost.
- `f_x`: frequency of key `x` in an access sequence.
- `w_i(x)`: working-set number—the distinct keys accessed since the previous access to `x`, under a stated first-access convention.
- `d(x,y)`: rank distance between ordered keys, used in finger bounds.
- `OPT(X)`: minimum cost of an allowed offline BST algorithm on sequence `X` under the specified model.
- **physical/logical mutation**: link topology changes / key-value association-set changes.

## Mechanisms, Invariants, or Proof Structure

The structural proof begins with global BST intervals and exact ownership. Each primitive rotation preserves the in-order regions, transfers the middle subtree, reconnects parent/root, and recomputes metadata demoted-first. Zig/zig-zig/zig-zag select a live local configuration and repeat until the accessed or last-visited node is root.

The performance proof assigns positive weights, subtree ranks, and logarithmic potential. For each single/double step, only local ranks change; concavity and disjoint subtree weights bound actual rotations plus potential change by the accessed node's rank increase. Summing local steps telescopes, giving the Access Lemma; summing operations telescopes global potential. Different weight choices or separate stronger analyses yield sequence-sensitive corollaries.

Operation proofs reduce insertion/deletion/split/join to bounded BST changes and splays while preserving key partitions and identity. The production proof adds miss/update semantics, exception/publication behavior, augmentation, constness, iterator invalidation, worst-case budgets, logical serialization, synchronization, and reclamation. Current competitive results are labeled by publication status, model, factor, and additive term.

## Alternatives and Trade-Offs

| Design | Strength | Cost or obligation |
|---|---|---|
| Bottom-up splay | direct cases and parent-based handles | parent bytes and upward rewrites |
| Top-down splay | one descent, no parent pointers required | partition/assembly proof and variant-specific shape |
| Splay on hit and miss | full locality around access boundary | every lookup is a write |
| Splay only successful hits | fewer miss writes | different contract/analysis and stale miss locality |
| Full splay | classical sequence guarantees | high single-operation write/path cost |
| Conditional/semi-splay | potentially fewer writes | different algorithm; classical theorems do not transfer automatically |
| Ephemeral nodes | no copy allocation, stable live addresses possible | iterator mutation and synchronization |
| Persistent path copying | snapshot roots and rollback | allocation, shared lifetime, access write amplification |
| Splay tree | adaptive amortized/locality properties | no worst-case height or operation latency |
| AVL/red-black/B-tree | deterministic logarithmic path | metadata/repair and less access adaptation |
| Treap | simple expected random shape, split/merge | randomness and linear worst-case realization |
| Sorted vector/hash map | dense range scan / expected exact lookup | linear mutation / no key-order range semantics |

## Failure Modes and Misconceptions

- **“The root is approximately the median.”** it is the last splayed access/boundary and may be an extreme.
- **“Valid splay trees have logarithmic height.”** every valid BST shape, including a chain, is possible.
- **“Amortized means average input.”** the bound controls every operation sequence's total through potential, without random-input assumptions.
- **“Every operation is logarithmic.”** one search/splay can be linear.
- **“Any move-to-root heuristic is splaying.”** zig-zig's parent-first order is essential to the classical proof.
- **“Misses are read-only.”** common implementations splay the last visited node.
- **“Const lookup can silently splay.”** physical mutation affects API, data races, locks, and observability.
- **“Address-stable nodes imply stable iterators.”** cached ancestry/cursors can become stale after rotation.
- **“Join works for any trees.”** the entire left key domain must precede the right.
- **“The Access Lemma proves every locality theorem immediately.”** some require specialized analyses.
- **“Splay is dynamically optimal.”** constant competitiveness remains conjectural as of the verification date.
- **“No progress exists on dynamic optimality.”** the 2026 preprint reports the first sublogarithmic splay competitive factor, with qualifications.
- **“Persistent splaying is read-only.”** it still allocates a new path/root and needs reclamation.
- **“Amortized bounds enforce tail SLOs or DoS resistance.”** hard per-operation budgets require separate mechanisms.

## Worked Examples

### Example 1

Node 3 is left child of root 5. One right rotation makes 3 root and transfers 3's right region to 5's left. Conclusion: zig handles the final odd edge while preserving in-order regions.

### Example 2

For path `9 ->left 6 ->left 4`, zig-zig first right-rotates 6 over 9, then 4 over 6. Conclusion: same-direction splaying rotates the parent first, not merely the target twice by an arbitrary move-to-root rule.

### Example 3

For `9 ->left 4 ->right 6`, left-rotate 6 over 4, then right-rotate 6 over 9. Conclusion: zig-zag keeps the accessed node as the promoted node in both rotations.

### Example 4

The executable insertion history ends with height 6 on seven nodes, yet all global BST, parent, reachability, and size invariants pass. Conclusion: linear height is a valid state, not structural corruption.

### Example 5

Accessing key 6 immediately after it was splayed performs zero rotations. Conclusion: self-adjustment can turn temporal locality into constant actual work without a frequency table.

### Example 6

A search for absent key 9 ends at maximum key 8 and splays 8 to root. Logical contents do not change, but topology does. Conclusion: miss behavior belongs in both API and concurrency contracts.

### Example 7

Deleting root-splayed 5 separates keys `<5` and `>5`; splaying maximum 4 in the left tree creates an empty right link for the right tree. Conclusion: deletion is exact physical removal plus a proven ordered join.

### Example 8

One deep access costs `Theta(n)` rotations, but its potential can drop by `Theta(n)` rank units across many nodes. Conclusion: actual and amortized cost differ operation-by-operation while sequence totals remain linked.

### Example 9

A reader holds a shared lock for `get`, but `get` rotates child-parent-grandparent links. A concurrent reader can observe mixed topology. Conclusion: semantic read does not justify a read lock when implementation splays.

### Example 10

A benchmark repeatedly reads one hot key and reports splay fastest, then generalizes to all ordered maps. Uniform scans, mutation-heavy mixes, and hard-tail workloads were absent. Conclusion: locality benefits are workload claims, not universal superiority.

## Cross-Program Connections

- **Algorithms:** potential functions, telescoping sums, entropy/frequency bounds, online competitiveness, and access-sequence geometry connect local rotations to global guarantees.
- **Programming languages:** logical versus physical constness, exceptions, intrusive ownership, recursive/iterative control, and persistent algebra shape safe APIs.
- **Concurrent programming:** read-as-write behavior, lock modes, root publication, optimistic validation, epochs/hazards, and linearizability govern shared use.
- **Computer architecture:** pointer chasing, rotation writes, cache/TLB/branch behavior, dirty pages, and allocator locality determine real cost.
- **Database engineering:** adaptive indexes, split/join, range order, buffer writes, persistent snapshots, and tail-latency SLOs motivate alternatives.
- **Security engineering:** linear individual paths, comparator/key cost, adversarial sequences, resource budgets, and hostile serialized shapes require defenses beyond amortization.
- **Dynamic graph algorithms:** link-cut trees use auxiliary splays, adding preferred paths, lazy reversal, path aggregates, and a separate correctness proof.
- **Software engineering:** access semantics, invalidation matrices, deterministic traces, potential ledgers, fault injection, telemetry, and representative benchmarks make self-adjustment reviewable.

## References

1. Daniel D. Sleator and Robert E. Tarjan, [Self-Adjusting Binary Search Trees](https://www.cs.cmu.edu/~sleator/papers/self-adjusting.pdf), JACM 32(3), 1985. Primary paper for splaying, the Access Lemma, amortized operations, static optimality, working-set/static-finger results, and the dynamic-optimality conjecture.
2. Daniel D. Sleator, [Self-Adjusting Binary Search Trees—author page](https://www.cs.cmu.edu/~sleator/papers/Self-Adjusting.htm). Author-maintained bibliographic page and full-text source describing the original scope and amortized meaning.
3. Carnegie Mellon University 15-451 (Fall 2025), [Algorithms lecture notes](https://www.cs.cmu.edu/~15451-f25/notes.pdf). Current academic derivation of splay cases, rank potential, the Access Lemma, and amortized analysis.
4. Carnegie Mellon University 15-750, [Kozen Lecture 12: Splay Trees](https://www.cs.cmu.edu/afs/cs/academic/class/15750-s16/Handouts/KozenLecture12.pdf). Graduate academic treatment of zig/zig-zig/zig-zag, insertion/deletion, and rank-potential proof.
5. Carnegie Mellon University 15-451, [Splay Trees](https://www.cs.cmu.edu/afs/cs.cmu.edu/academic/class/15451-f97/www/splay.html). Academic overview of amortized, static-optimality, and working-set behavior with rotation cases.
6. Boost.Intrusive, [Presenting Boost.Intrusive containers](https://www.boost.org/latest/doc/html/intrusive/presenting_containers.html). Current official documentation positioning intrusive splay containers, ownership layout, and their adaptive/caching trade-off.
7. Boost.Intrusive Project, [`splaytree_algorithms.hpp`](https://github.com/boostorg/intrusive/blob/develop/include/boost/intrusive/splaytree_algorithms.hpp). Current primary implementation source for intrusive splay, search, insertion, erase, rebalance, split/join, and node-trait behavior.
8. GCC Project, [policy-based splay tree implementation](https://github.com/gcc-mirror/gcc/blob/master/libstdc%2B%2B-v3/include/ext/pb_ds/detail/splay_tree_/splay_tree_.hpp). Current primary production source for access notification, splaying, rotation, insertion, erase, split/join, and policy integration.
9. ISO C++ working draft, [Associative container requirements](https://eel.is/c%2B%2Bdraft/associative.reqmts). Current observable ordering, key equivalence, iterator/reference, insertion, erase, and node-handle contracts used for comparison without mandating splaying.
10. Petr Chmel et al., [Splay trees are almost dynamically optimal](https://arxiv.org/abs/2607.18498), July 2026 preprint. Primary current source reporting `O(log log n * log^2 log log n)` competitiveness plus stated additive/model conditions; not a proof of constant-factor dynamic optimality.

## Exercises

### Exercise 1

Trace one left-left zig-zig and one left-right zig-zag with named ordered regions. Prove preservation of global order, reachability, parents, and subtree sizes; explain why move-to-root rotation order is analytically different.

### Exercise 2

State the weight/rank/potential definitions and derive how the Access Lemma gives `O(log n)` amortized access under unit weights. Explain telescoping and why this does not bound one operation.

### Exercise 3

Implement hit and last-visited-miss splaying plus deletion by joining children. Specify duplicate updates, absent deletion, split inclusivity, node identity, failure points, and independent invariants.

### Exercise 4

Compare splay, AVL, red-black, treap, B-tree, sorted vector, and hash map for a cache with strong recency/skew but a strict p99.99 latency SLO and concurrent readers. Recommend a design and evidence.

### Exercise 5

Audit these claims: “splay has logarithmic lookup,” “working-set proves dynamic optimality,” and “the 2026 result proves dynamic optimality.” Replace each with a precise claim, then design a sequence/potential and benchmark evidence plan.

## Answers to the Exercises

### Answer 1

Let `g` have left child `p`, and `p` left child `x`; name in-order regions `A<x<B<p<C<g<D`. Right-rotate `p` over `g`, transferring `C`; then right-rotate `x` over `p`, transferring `B`. Final order is still `A,x,B,p,C,g,D`, every node/region has one owner, parent/root links follow promoted nodes, and sizes recompute first for demoted `g`, then `p`, then promoted `x` through the two primitives. For left-right, use `A<p<B<x<C<g<D`: left-rotate `x` over `p`, transferring `B`, then right-rotate `x` over `g`, transferring `C`; recompute each demoted/promoted pair. Repeatedly rotating `x` alone in same-direction cases produces a different side-subtree arrangement and potential change. It preserves BST validity but is move-to-root, so the classical zig-zig Access-Lemma inequality cannot simply be cited.

### Answer 2

Choose `w(v)=1`, so `s(v)` is subtree node count, `r(v)=log2 s(v)`, and `Phi=sum r(v)`. The Access Lemma bounds one splay's amortized cost by at most `3(r'(x)-r(x))+1`. After splaying, `x` is root and `s'(x)=n`, so `r'(x)<=log2 n`; because `r(x)>=0`, amortized cost is at most `3log2 n+1`. Across operations, summing `actual_i + Phi_i-Phi_{i-1}` cancels intermediate potentials, linking total actual work to total amortized work plus initial minus final potential. One deep access can still cost `Theta(n)`; its large negative potential change pays part of that actual cost. Therefore the conclusion is logarithmic amortized per operation over a sequence, not worst-case latency for each operation.

### Answer 3

Search carries `last`; on hit, splay the node and return its value; on null, splay `last` and return a typed miss. Duplicate map insertion updates the existing value and splays it; document whether a throwing update occurs before topology changes. For delete, search/splay; if root key differs, return absent after the miss-induced shape change. Otherwise detach physical root, clear its links, publish right if left empty, or splay maximum(left) and attach right. Define split as `<k`/`>=k` (or its alternative consistently) and require join's entire left domain below right. Allocate/construct before insertion publication; make rotations/metadata nonthrowing or transactional. Independently check ancestor bounds, acyclic unique reachability, exact count, parents, augmentations, hit/miss root policy, sorted values, and construction/destruction identities after every operation.

### Answer 4

Splay can exploit hot recency/skew and needs no balance metadata, but a lookup writes multiple pointers and can be linear, conflicting with a hard p99.99 SLO and concurrent-reader scaling. AVL/red-black give deterministic logarithmic paths; a B-tree improves cache/page fanout; treap is expected rather than hard-bounded; sorted vector favors read-mostly scans but middle mutation is linear; hash gives expected exact lookup but no order/ranges. A practical recommendation is a deterministic B-tree/red-black/AVL primary index plus a separate bounded concurrent cache/admission policy for hot items, unless exclusive serialization and amortized tails are demonstrably acceptable. Evidence must replay real recency shifts and adversarial sequences, measure comparisons, rotations/writes, lock contention, cache misses, throughput and p50/p99/p99.99/max latency, memory, and range/update behavior under the target hardware and concurrency. Do not select solely from asymptotics.

### Answer 5

Replace the first with: “For any operation sequence on at most `n` items, full splaying supports standard BST operations in `O(log n)` amortized time under the stated unit-cost model; one lookup may be `Theta(n)`.” Replace the second with: “Working-set bounds adapt to recency but cover only one family of lower-bound behavior and do not imply constant competitiveness with the optimal offline dynamic BST.” Replace the third with: “The July 2026 preprint reports an `O(log log n * log^2 log log n)` competitive ratio with an additive term and stated sequence/model conditions; constant-factor dynamic optimality remains conjectural.” For evidence, enumerate small BST shapes/access sequences and verify roots/invariants/cumulative actual cost; independently recompute unit/custom-weight potential and local/global amortized ledgers. Benchmark repeated hot sets, scans, alternation, shifting locality, misses, updates, and adversarial chains against alternatives with raw per-operation tails and structural/write/cache counters. Finite evidence can validate implementation/accounting and workload behavior, not prove universal theorems or settle the conjecture.
