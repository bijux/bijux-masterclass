---
module_id: DSE-054
program: Data Structures Engineering
level: 2
module_number: 54
title: Persistent Balanced Trees
status: complete
last_verified: 2026-08-30
---

# Persistent Balanced Trees

## One-Page Review

### Governing question

How can an immutable ordered map preserve every old root while insertion, replacement, deletion, rotations, recoloring, cached metadata, bulk operations, reclamation, concurrency, and storage retain both search-order and balance guarantees?

### Essential definitions

- A **persistent balanced search tree** is an immutable ordered set/map whose updates return balanced new roots while previous roots remain queryable.
- **path copying** rebuilds every node whose child, payload, color, height, size, or aggregate changes and reuses untouched subtrees.
- A **rotation** is a local shape transformation preserving in-order key sequence; a persistent rotation constructs replacement nodes.
- An **AVL tree** requires every node's child heights to differ by at most one and stores/recomputes height.
- A **red-black tree** constrains node colors and equal black heights so its height remains logarithmic.
- A **weight-balanced tree** constrains subtree sizes and uses size-guided rotations.
- A **smart constructor** computes metadata and performs the balancing cases rather than exposing raw node construction.
- `join(L,k,v,R)` combines ordered trees when every key in `L` is below `k` and every key in `R` is above it.
- `split(T,k)` partitions a tree around `k`; join/split support union, intersection, difference, and range surgery.
- A **changed frontier** is the connected set of nodes rebuilt because an update or repair changes their outgoing edges or metadata.

### Central model, mechanism, or theorem

An ordered immutable update descends from a chosen old root. It returns either the same subtree for a no-op or a new subtree whose changed child is the recursive result and whose untouched child is reused by identity. On the way up, a balancing constructor recomputes metadata and applies rotations/recoloring by allocating the new local shape. No published node is mutated.

Correctness composes three obligations. The abstraction proof shows in-order traversal represents the intended map. The balance proof shows every constructor/repair restores AVL, red-black, weight, or other chosen invariant. The persistence proof shows old reachable nodes are unchanged and sufficiently live. If height is `O(log n)`, point lookup/update takes `O(log n)` comparisons/work and allocates `O(log n)` nodes, with constant-factor extra nodes for local repair. Deletion and bulk join/split need their own proofs.

Persistent algorithms must be analyzed in their functional form. An imperative rotation's assignment count does not predict immutable allocation. A red-black recolor can require rebuilding nodes; an AVL rotation constructs a complete local replacement; cached sizes/hashes/aggregates must be recomputed from replacement children. Identity sharing is an optimization promise, not ordered-map semantics.

### Critical invariants

1. Comparator order is total and stable for every retained key; no key mutates in a way that changes ordering.
2. Each root satisfies strict BST bounds and the chosen duplicate/replacement policy.
3. Every stored height, size, color, black height, weight, hash, and aggregate agrees with reachable children.
4. The chosen balance predicate holds at every node, including after deletion and bulk operations.
5. Updates never mutate a node/payload reachable from an old root; untouched subtrees may be reused safely.
6. Rotations preserve in-order sequence and rebuild every node whose children or metadata change.
7. Root publication occurs only after the private new tree is complete and validated; failure preserves old roots.
8. Readers, iterators, caches, version registries, and storage manifests protect lifetime; reclamation follows all retained roots.
9. Complexity claims state tree family, operation, comparator/value cost, branch/history, node/byte allocation, and runtime model.

### Common failures

- Copying the search path but rotating or recoloring an old shared node in place.
- Reusing stale height, size, hash, or aggregate after a child changes.
- Proving insertion while silently assuming deletion follows automatically.
- Accepting nontransitive, stateful, locale-changing, or mutable-key comparison.
- Translating an imperative fix-up that depends on parent pointers without rebuilding its full context.
- Returning raw node pointers as stable entries across versions, rotations, compaction, or restart.
- Claiming `O(log n)` without validating balance after every version/operation.
- Measuring only current-root nodes and overlooking old roots, iterators, caches, and allocator retention.
- Equating pointer inequality with logical map inequality.
- Publishing a durable root before all new nodes/pages and metadata are recoverable.

### Compact example

Insert `30,20,10` into an immutable AVL map. The third insertion constructs a left-left imbalance and a persistent right rotation, yielding root `20` with children `10` and `30`; earlier roots still denote `[30]` and `[20,30]`. Insert `25` into that root: rebuild `30` and `20`, but reuse node `10`. Independently insert `5` into the three-key root: rebuild the left path and reuse node `30`. The executable validates both branches, exact metadata, ordering, balance, replacement isolation, and selected sharing.

### Connections

[DSE-032](032-avl-trees.md), [DSE-033](033-red-black-trees.md), and [DSE-034](034-treaps.md) supply ephemeral balance families. [DSE-051](051-path-copying.md) supplies version construction/lifetime, and [DSE-052](052-structural-sharing.md) supplies DAG accounting. [DSE-053](053-persistent-lists-and-queues.md) shows why cost proofs must match persistent traces. The [program roadmap](../ROADMAP.md) continues with HAMTs, finger trees, persistent vectors, snapshots, concurrency, and verified structures.

## Governing Question

Which ordered-map semantics, balancing family, immutable repair algorithm, metadata discipline, lifetime model, publication protocol, and evidence jointly establish logarithmic behavior without corrupting any retained version?

## Why This Matters

Balanced trees give deterministic ordered lookup, predecessor/successor, range traversal, rank/select, and split/join behavior. Persistence adds cheap snapshots, branching states, consistent readers, rollback, undo, speculative analysis, compiler environments, symbolic maps, configuration versions, and copy-on-write indexes. A root is a compact version handle because unchanged subtrees are shared.

The combination is not “ordinary balancing plus const.” Imperative AVL and red-black presentations update child links, colors, heights, and parent pointers in place. With shared immutable nodes, every changed field requires a replacement node; the algorithm must return reconstructed context through recursion. A local repair may touch nodes not on the initial search path, and deletion can propagate a height or black-height deficit toward the root.

Balanced-tree correctness is conjunctive. Search order without balance can degrade to linear height. Balance without correct ordering returns wrong values. Both can hold while old roots are mutated or prematurely reclaimed. Logical correctness can hold while cached subtree sizes are corrupt, breaking rank/select. A complete review must cover every retained root and every augmented field.

Real systems add comparator evolution, mutable payloads, allocation failure, concurrent root publication, iterator retention, serialization, crash recovery, hostile inputs, and performance constants. This module treats functional elegance as the start of the design, not the completion claim.

## Prerequisites and Retrieval

Retrieve BST order, search, replacement, deletion, and traversal from [DSE-031](031-binary-search-trees.md); AVL height/balance/rotations from [DSE-032](032-avl-trees.md); red-black color/black-height rules from [DSE-033](033-red-black-trees.md); and treap priority rotations from [DSE-034](034-treaps.md). Retrieve rank/select augmentation from [DSE-036](036-order-statistic-trees.md) and interval/segment aggregates from [DSE-037](037-fenwick-interval-and-segment-trees.md).

Retrieve version roots, changed frontiers, failure publication, reclamation, concurrency, and serialization from [DSE-051](051-path-copying.md). Retrieve logical versus physical identity, interning, DAG reachability, and sharing evidence from [DSE-052](052-structural-sharing.md). You should be able to prove recursive invariants and audit exact allocated nodes rather than reasoning from mutable pseudocode.

## Learning Objectives

After completing this module, you can:

1. specify persistent ordered-set/map semantics and stable comparator requirements;
2. derive functional insertion/replacement from path copying and a balancing constructor;
3. prove rotations preserve in-order order while restoring a named balance case;
4. distinguish AVL, red-black, weight-balanced, treap, and rebuild-based guarantees;
5. identify every node/metadata field rebuilt by insertion, deletion, and rotations;
6. design join/split and bulk set operations with size-sensitive bounds;
7. specify identity, iterator, diff, lifetime, failure, concurrency, and durable-root contracts;
8. validate all roots globally and sharing promises separately from map semantics;
9. construct adversarial, metamorphic, fault, and concurrent evidence; and
10. report comparisons, allocations, live/retained bytes, locality, and tail behavior honestly.

## Core Exposition

**Define the map before the tree.** An ordered map associates at most one value with each key under comparator `cmp`. `lookup`, `insert/replace`, `delete`, ordered iteration, lower/upper bound, predecessor/successor, range, rank/select, split, join, and bulk operations are separate API choices. A set is a map with unit values.

The comparator must define a stable total order over retained keys: sign consistency, antisymmetry in comparison result, transitivity, and equality compatibility. If `cmp(a,b)=0`, the map's duplicate policy decides whether to preserve the old key object, replace key/value, combine values, reject, or return the same root for equal content. Comparator exceptions and side effects complicate retry and failure safety.

Persistent update takes an explicit root and returns a root. Any retained root can be updated, creating a version branch. Equal logical maps may have different shapes and node identities. Version identity, map equality, key/entry identity, and physical node identity are distinct. A rotation changes node addresses even for logically unchanged entries.

Payloads require an ownership contract. Immutable spines with mutable keys can destroy search order in every version. Mutable values preserve key navigation but violate deep snapshot values and hashes/aggregates. Require immutable values, copying, persistent nested values, or explicitly shallow snapshots.

**Functional AVL insertion is path copying plus repair.** Use immutable node `(key,value,left,right,height,...)`. Empty insertion creates a height-one node. Descent compares the key. The recursive result replaces one child; the other child is reused. A smart constructor computes `height=1+max(height(left),height(right))` and any other metadata. If balance factor leaves `[-1,1]`, return that node.

For a left-left imbalance, let `y` be the left child of `z`. A right rotation returns new root `y`, whose right child is a newly constructed `z` with `y.right` and `z.right`; `y.left` and `z.right` remain reusable. Construct lower node first so its height/size is correct, then the new root. Left-right performs persistent left rotation of `y`, then right rotation of `z`. Symmetric cases follow.

A rotation preserves order because the relevant keys satisfy `keys(A)<y<keys(B)<z<keys(C)`. Before rotation, `z(y(A,B),C)`; afterward, `y(A,z(B,C))`. Both in-order traversals are `A,y,B,z,C`. The AVL height proof then checks the imbalance-case child heights and recomputed metadata.

Insertion or replacement visits `h` nodes, creates at most a constant number of repair nodes per affected level, and runs in `O(h)`. AVL invariants imply `h=O(log n)`. Replacement can return the identical root when both key/value policy says no logical change; otherwise it copies the path even if shape stays balanced. Value-copy/hash/aggregate costs may dominate.

**Red-black persistence organizes repair differently.** A functional red-black node stores color plus children. Typical insertion recursively inserts a red leaf, balances black-rooted contexts containing a red-red violation, then blackens the returned root. Pattern matching replaces parent-pointer fix-up. The proof establishes BST order, no red node with a red child, equal black height on all root-to-empty paths, and black root under the external invariant.

Recoloring is not free under immutability. Changing a node color constructs a replacement and may require replacement parents. Rules convenient imperatively are not necessarily allocation-efficient functionally; compare actual nodes built. Conversely, functional pattern matching can express four symmetric insertion violations compactly and make proof cases local.

Insertion does not settle deletion. Red-black deletion must handle removal of a black node and propagate/repair black-height deficit; AVL deletion may reduce height repeatedly toward root and trigger rotations at several levels. Treap deletion rotates/merges by priority. For every family, specify absent-key no-op, leaf/one-child/two-child replacement, predecessor/successor extraction, and metadata rebuild.

Copy the entire changed frontier. In two-child BST deletion, choosing successor changes the target entry and deletes minimum in the right subtree, so both the target path and successor-extraction path are rebuilt. A rotation/recolor may rebuild sibling/niece context. Parent pointers cannot be embedded as unique parents in shared nodes; use recursive context, external cursors, or version-specific zipper paths.

**Balance families trade strictness, metadata, and operations.** AVL trees impose tight height differences and often give excellent lookup depth, with more update rotations/height metadata. Red-black trees encode relaxed balance with one color bit and height at most a constant factor logarithmic. Weight-balanced trees store sizes and rotate according to ratios, integrating rank/select and enabling elegant join-based bulk operations, but constants/inequalities must match a proven scheme.

Treaps use BST keys and heap priorities. Deterministic priorities derived from a keyed hash give repeatable shapes but introduce collision/adversarial considerations; random priorities give expected height, not deterministic worst-case. Scapegoat/root-balanced/rebuild families allow imbalance until rebuilding; persistence can make rebuild allocation large and old versions retain both shapes.

B-trees and copy-on-write page trees reduce height and fit storage/cache blocks, but copied bytes per update can be large and split/merge durability matters. This module emphasizes binary functional mechanics; persistent page indexes require page-format, concurrency-control, WAL/copy-on-write, checksum, and crash proofs.

Choose based on operations and guarantees. Lookup-heavy small immutable maps may favor AVL. General functional maps often use weight-balanced or red-black trees. Split/join-heavy parallel set algebra benefits from join-based designs. Avoid selecting solely by textbook familiarity.

**Augmentation must be reconstructed, not inherited.** Store size for rank/select: `size(node)=1+size(left)+size(right)`. Store interval maximum, sum, min/max, Merkle hash, bloom summary, or domain aggregate as a pure function of key/value and child metadata. A smart constructor is the only normal node creation path.

Every rotation changes child ownership at two or three local nodes. Recompute bottom-up. Copying an old `height` or `size` into a node with a new child silently corrupts queries while membership may still pass. Validators independently recompute metadata; never validate a cached field using itself.

Lazy tags are difficult: an imperative range tree may push a tag into children in place. Persistent code copies tagged children or represents immutable composed transformations. Define whether aggregate includes pending tags. Hashes bind type, key/value encoding, children, balance metadata if relevant, and schema with canonical boundaries.

**Join and split make bulk operations principled.** `join(L,k,v,R)` assumes all `L` keys are below `k` and all `R` keys above. If heights/weights are close, make one root. Otherwise descend the taller/heavier side, recursively join, and repair on return. A correct family-specific join preserves order and balance with work proportional to height difference under common formulations.

`split(T,k)` recursively partitions by comparison, using join to reconstruct the opposite side. It returns keys below `k`, optional matching entry, and keys above. Set union chooses a pivot from one tree, splits the other, recursively unions corresponding ranges, then joins. Intersection/difference alter whether the pivot is retained.

Naïvely inserting all smaller into larger costs `O(m log(n+m))`; join-based algorithms can achieve stronger size-sensitive work such as `O(m log(n/m+1))` for suitable balanced trees and assumptions, while exposing divide-and-conquer parallelism. Quote only the theorem for the exact algorithm/family. Comparator and allocation costs remain.

Range deletion can split at bounds and join survivors, but releasing the removed middle obeys shared lifetime. Concatenating ordered trees is valid only when boundary keys satisfy order; otherwise it is union with conflict policy.

**Identity and iteration need version context.** Ordered iteration pins one root and uses a stack/zipper of ancestors. Immutable nodes make the traversal snapshot stable, but its path/root retains subtrees. A raw node address is not a durable entry identity: rotations, replacement, compaction, hash-consing, serialization, and restart change it.

Use key lookup, stable application entry IDs, or opaque `(version,key/generation)` handles. A cursor/zipper built for one root cannot silently edit another. Persistent zippers can reconstruct updates but add context objects and retention.

Diff can exploit pointer equality: identical immutable subtrees are equal under the node contract and can be skipped. Different pointers may still hold equal content. Cached content hashes can skip more under collision policy. Shape differences make naïve paired recursion awkward; join/split, ordered iterators, or hash-guided comparison preserve correctness. Bound output.

**Lifetime and failure are part of persistence.** Tracing GC treats version roots, iterators, caches, registries, and in-flight readers as roots. Refcounting acyclic tree edges gives prompt reclamation but adds counter traffic and recursive destruction; cycles can enter through parent/caches/payloads. Epochs protect concurrent readers but require another scheme or generation ownership to know shared-node reachability.

Arenas improve locality, yet cross-version sharing creates arena dependency DAGs. One shared node can retain a coarse arena. Periodic rebuilding/compaction can improve locality and sever history sharing at allocation cost. Monitor retained roots, reader age, unique live/reclaimed nodes/bytes, sharing fan-in, and retention owners.

Construct updates privately, bottom-up. If comparator, allocation, value ownership, hash/aggregate, rotation, or validation fails, release partial nodes and keep every old root unchanged. Publish/register the new root last. Fault-inject every construction point. Destructors and refcount increments/decrements must remain balanced during unwinding.

Length/size/height counters need overflow policy. Recursive operations on corrupt/deep trees can exhaust stack before validation. Bounds and iterative hostile-input validation matter even when a valid balanced tree would be shallow.

**Concurrency is snapshot-friendly but writer semantics remain.** Readers traverse safely after acquire publication and lifetime pinning. An atomic latest-root pointer gives consistent snapshots. Two writers loading the same root create valid branches; a plain last store loses one update. Use serialized writers, compare-and-swap retry, transactions, or explicit branching/merge.

CAS retry re-executes comparison, allocation, and value/aggregate logic unless staged; side effects must be retry-safe. A loser releases its private nodes correctly. ABA requires generation tags or safe reclamation. Managed references simplify lifetime but do not remove contention, retention, or logical lost updates.

Bulk union/intersection can run recursive subproblems in parallel because input trees are immutable, but allocator/GC bandwidth and cutoff sizes govern benefit. Determinism requires stable comparator/conflict policy. Parallel construction publishes only complete immutable results; cancellation cleans every partial branch.

An immutable tree is not automatically a linearizable concurrent map. Latest-root publication defines whole-map updates, while per-key concurrency, starvation, memory ordering, and progress need separate proofs. Long readers pin old roots and raise memory.

**Serialization can be logical or structural.** Logical format writes sorted `(key,value)` entries and rebuilds under the current validated algorithm. It avoids depending on color/height/node layout and can bulk-build a balanced tree. Record comparator/key schema and duplicate policy. Rebuilding may choose a different shape but same map.

Structural graph format writes nodes once plus root/version records to preserve sharing/history. Validate IDs, references, acyclicity, strict key bounds, balance, metadata, root set, reachable counts, and quotas. Never persist raw pointers, closures, comparator code addresses, refcounts, locks, or process-local IDs.

Content-addressed nodes bind canonical key/value, child hashes, type/schema, and perhaps balance metadata. Write children before parent and root manifest last. Crash durability additionally requires checksums, flush ordering, atomic root publication, recovery, and reachability garbage collection. An immutable in-memory root alone proves none of these.

Comparator/schema migration can invalidate ordering even when bytes decode. Rebuild into a new generation and preserve old roots until policy permits reclamation. Authorization applies per version/range/history; structure-sharing diagnostics can leak relationships across tenants.

**Evidence must validate every root and every field.** Use an independent sorted-map model for linear and branching histories. After every update, compare every retained root's ordered entries, lookup, size, bounds, rank/select/range/aggregate, and unchanged digest. Reference snapshots must not share implementation nodes.

Validate locally and globally. Per root, check strict min/max bounds, balance-family invariant, metadata recomputation, acyclicity, node type, and element policy. Across roots, check old-node immutability, expected untouched-subtree sharing, absence of wrongly shared changed nodes, physical reachability, and lifetime accounting. Maximum sharing is optional unless promised.

Exhaust tiny trees and all rotation/recolor/delete cases, duplicates/replacement/no-op, root/leaf/one/two-child deletion, min/max, sorted/reverse/alternating keys, branches from every version, join height gaps, split boundaries, union conflicts, and equal maps with different shapes. Model-check published algorithms where practical.

Metamorphic relations include insert then lookup; insert/delete restoration under the selected duplicate policy; unrelated-key preservation; in-order sorted uniqueness; branch isolation; split then join restoration; union commutativity when resolver is commutative; rank/select inverse; diff/apply round trip; serialization rebuild equality; and compaction preserving every retained map.

Fault tests cover comparisons, key/value copies, each node/metadata allocation, rotations, deletion repairs, join/split recursion, refcounts, root registry/CAS, writes/flushes/publication, and cancellation. Concurrent tests pin roots, race writers, retry, release old roots, stall readers, and validate the stated linearization/branch model.

Benchmarks vary size, key/value/comparator cost, sorted/random/adversarial order, lookup/insert/replace/delete/range/rank/join/split/union mix, branch factor/history, retained readers, tree family, allocator/collector/refcount, threads, serialization, and compaction. Report comparisons, height distribution, rotations/recolors/rebuilds, copied nodes/bytes, allocations/reclamation/retention, sharing, cache/TLB/branches, latency quantiles, CAS retries, GC pauses, and maximum observed repair—not throughput alone.

The executable uses immutable Python tuples to implement persistent AVL insertion/value replacement. It constructs linear and branching roots, performs a rotation, shares untouched subtrees, recomputes height/size, and validates every retained root. It does not implement deletion, red-black/weight balance, join/split, reclamation, concurrency, storage, hostile-input defense, or performance proof.

<!-- bijux-verify: {"id":"persistent-avl-version-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"v5_keys=10,20,25,30,40\nv6_keys=5,10,20,30\nv3_unchanged=True\nbranch_isolated=True\nv4_shares_v3_left=True\nv6_shares_v3_right=True\nreplacement_old=thirty\nreplacement_new=THIRTY\nreplacement_shares_left=True\nv5_height=3\nall_balanced=True\nall_invariants=True\nevidence=finite_persistent_avl_version_trace\n","stderr":""}} -->
```python
EMPTY = None


def height(tree):
    return 0 if tree is EMPTY else tree[4]


def size(tree):
    return 0 if tree is EMPTY else tree[5]


def node(key, value, left, right):
    return (
        key,
        value,
        left,
        right,
        1 + max(height(left), height(right)),
        1 + size(left) + size(right),
    )


def rotate_left(tree):
    child = tree[3]
    lower = node(tree[0], tree[1], tree[2], child[2])
    return node(child[0], child[1], lower, child[3])


def rotate_right(tree):
    child = tree[2]
    lower = node(tree[0], tree[1], child[3], tree[3])
    return node(child[0], child[1], child[2], lower)


def rebalance(tree):
    factor = height(tree[2]) - height(tree[3])
    if factor > 1:
        if height(tree[2][2]) < height(tree[2][3]):
            tree = node(tree[0], tree[1], rotate_left(tree[2]), tree[3])
        return rotate_right(tree)
    if factor < -1:
        if height(tree[3][3]) < height(tree[3][2]):
            tree = node(tree[0], tree[1], tree[2], rotate_right(tree[3]))
        return rotate_left(tree)
    return tree


def insert(tree, key, value):
    if tree is EMPTY:
        return node(key, value, EMPTY, EMPTY)
    if key < tree[0]:
        return rebalance(node(tree[0], tree[1], insert(tree[2], key, value), tree[3]))
    if key > tree[0]:
        return rebalance(node(tree[0], tree[1], tree[2], insert(tree[3], key, value)))
    if value == tree[1]:
        return tree
    return node(key, value, tree[2], tree[3])


def lookup(tree, key):
    while tree is not EMPTY:
        if key < tree[0]:
            tree = tree[2]
        elif key > tree[0]:
            tree = tree[3]
        else:
            return tree[1]
    raise KeyError(key)


def keys(tree):
    if tree is EMPTY:
        return ()
    return keys(tree[2]) + (tree[0],) + keys(tree[3])


def valid(tree, lower, upper):
    if tree is EMPTY:
        return True
    key, _, left, right, stored_height, stored_size = tree
    ordered = (lower is EMPTY or lower < key) and (upper is EMPTY or key < upper)
    metadata = (
        stored_height == 1 + max(height(left), height(right))
        and stored_size == 1 + size(left) + size(right)
    )
    balanced = abs(height(left) - height(right)) <= 1
    return (
        ordered
        and metadata
        and balanced
        and valid(left, lower, key)
        and valid(right, key, upper)
    )


v0 = EMPTY
v1 = insert(v0, 30, "thirty")
v2 = insert(v1, 20, "twenty")
v3 = insert(v2, 10, "ten")
v4 = insert(v3, 25, "twenty-five")
v5 = insert(v4, 40, "forty")
v6 = insert(v3, 5, "five")
v7 = insert(v5, 30, "THIRTY")

versions = (v0, v1, v2, v3, v4, v5, v6, v7)
all_invariants = all(valid(tree, EMPTY, EMPTY) for tree in versions)
all_balanced = all(
    tree is EMPTY or abs(height(tree[2]) - height(tree[3])) <= 1
    for tree in versions
)

print("v5_keys=" + ",".join(str(key) for key in keys(v5)))
print("v6_keys=" + ",".join(str(key) for key in keys(v6)))
print("v3_unchanged=" + str(keys(v3) == (10, 20, 30)))
print("branch_isolated=" + str(lookup(v5, 40) == "forty" and keys(v6)[0] == 5))
print("v4_shares_v3_left=" + str(v4[2] is v3[2]))
print("v6_shares_v3_right=" + str(v6[3] is v3[3]))
print("replacement_old=" + lookup(v5, 30))
print("replacement_new=" + lookup(v7, 30))
print("replacement_shares_left=" + str(v7[2] is v5[2]))
print("v5_height=" + str(height(v5)))
print("all_balanced=" + str(all_balanced))
print("all_invariants=" + str(all_invariants))
print("evidence=finite_persistent_avl_version_trace")
```

## Definitions and Notation

- `T` is an immutable ordered-map root; `Empty` is the empty tree.
- `Node(k,v,L,R,m)` stores key/value, left/right roots, and metadata `m`.
- `keys(T)` is the in-order key sequence; `map(T)` is the abstract key-value mapping.
- `cmp(a,b)` is the configured comparator; `<` abbreviates a negative result.
- `h(T)` is height with `h(Empty)=0`; `s(T)` is subtree size with `s(Empty)=0`.
- AVL balance factor is `bf(T)=h(L)-h(R)` and must lie in `{-1,0,1}`.
- A red-black tree has colors `R/B`, no red-red edge, and equal black height from each node to empty leaves.
- `update(T,k,v)` returns a root and never changes `T`; retained roots form a version DAG.
- `Reach(T)` is the set of physical nodes reachable from root `T`.
- The **changed frontier** includes every replacement ancestor and local repair node.
- `join(L,k,v,R)` requires `max(keys(L))<k<min(keys(R))` when sides are nonempty.
- `split(T,k)=(A,found,B)` requires keys of `A` below `k` and keys of `B` above `k`.
- **Logical equality** compares mappings; **version identity** compares roots/history; **node identity** exposes implementation sharing.
- A **smart constructor** is a trusted creation boundary that computes metadata and restores/assumes documented balance.
- A **snapshot reader** pins one root; a **latest-root service** publishes roots through synchronization.

## Mechanisms, Invariants, or Proof Structure

**Abstraction invariant.** Every node satisfies strict lower/upper comparator bounds; recursive in-order traversal yields sorted unique keys; values follow duplicate policy. Lookup correctness follows by comparison partition. Update correctness is inductive over descent and repair.

**Persistence invariant.** Nodes/payloads reachable from an input root are immutable. Recursive update constructs private nodes; unchanged children are reused, changed children are returned replacements, and publication is last. Induction over stack frames proves all old roots remain unchanged.

**Metadata invariant.** Each height, size, hash, and aggregate equals a pure recomputation from local entry and replacement children. Smart constructors are used by insertion, deletion, rotation, join, split, bulk build, deserialization, and compaction. Independent validation ignores cached answers.

**AVL repair proof.** A recursive update changes one child height by a bounded amount under the algorithm's preconditions. For each left-left, left-right, right-right, and right-left case, establish key range order, construct the rotated local tree, recompute lower nodes before root, and prove child-height difference at each rebuilt node. Unaffected ancestors then repeat the argument.

**Red-black repair proof.** Establish BST order, no red-red edge, and equal black heights for each pattern. Recursive insertion may create one local red-red violation; balancing black context and blackening root restores the external invariant. Deletion uses a separate deficit invariant and proof.

**Complexity proof.** Count comparisons, constructors, rotations/recolors, and metadata cost along height `h`. A balance theorem yields `h=O(log n)` for AVL/red-black/valid weight schemes. Therefore point operations are `O(log n)` and new node count is `O(log n)` under constant-size metadata/value reference assumptions. Bytes and expensive aggregates are analyzed separately.

**Join/split proof.** Preconditions partition key ranges. Recursive descent reduces height/weight gap; family-specific repair restores balance. Split applies induction and joins reconstructed sides. Bulk-operation work proofs depend on pivot choice and exact join theorem.

**Lifetime/publication invariant.** All roots/readers/iterators/caches/manifests are registered or otherwise protected. Reclamation occurs only after reachability/lifetime permits. A newly constructed root becomes visible atomically after initialization; disk roots publish after durable descendants.

**Evidence separation.** Map equality, representation validity, old-version isolation, promised sharing, reclamation, linearizability, durability, hostile-input safety, and performance are distinct verdicts. A passing membership trace does not certify deletion, balance, or storage.

## Alternatives and Trade-Offs

| Family | Balance guarantee | Persistent strengths | Main costs/risks |
|---|---|---|---|
| AVL | Tight deterministic height | Fast lookup; direct height proof | Height metadata; deletion/rotations |
| Red-black | Deterministic logarithmic height | Compact color metadata; elegant functional insertion | Deletion deficit cases; recolor allocation |
| Weight-balanced | Size-ratio logarithmic balance under proven constants | Rank/select and join-based bulk algebra | Subtle valid ratios/rotation cases |
| Treap | Expected logarithmic with suitable priorities | Simple split/merge and persistence | Random/hash trust; worst-case/adversarial shape |
| Scapegoat/root-balanced | Amortized rebuild guarantee | Simple search nodes; bulk rebuild | Large copy spikes and retained duplicate shapes |
| B-tree/copy-on-write pages | Logarithmic page height | Locality/storage integration | Page-copy bytes, split/merge, crash protocol |
| Rebuild sorted array | Optimal locality/read simplicity | Excellent frozen snapshots | Update copies `Theta(n)`; no cheap branching edits |

Tree choice must include ordered/range/bulk requirements, proof maturity, runtime, key/value cost, version retention, and storage boundary. “Balanced BST” is not one interchangeable implementation.

## Failure Modes and Misconceptions

1. **Mutating during repair:** one rotation corrupts every root sharing that node.
2. **Stale metadata:** membership passes while rank, aggregate, hash, or later balance decisions fail.
3. **Insertion-only confidence:** deletion has different propagation and must be implemented/reviewed independently.
4. **Comparator drift:** mutable keys, locale/configuration change, NaN-like cases, or inconsistent equality invalidate ordering.
5. **Parent-pointer reuse:** a shared node cannot carry one authoritative parent/version.
6. **Wrong allocation model:** assignment counts from imperative algorithms do not equal immutable nodes/bytes.
7. **False identity conclusion:** different roots/pointers may represent equal maps; rotations change addresses.
8. **Root-only memory count:** readers, caches, histories, allocators, and dead-but-uncollected nodes retain space.
9. **CAS equals concurrent map:** whole-root publication still needs conflict/retry/progress and lifetime policy.
10. **Raw structural persistence:** pointers, locks, comparator code, and memo state are not durable formats.
11. **Unqualified asymptotics:** comparator, payload, hash/aggregate, page bytes, and branch retention can dominate.
12. **Validator self-reference:** trusting stored height to validate stored balance misses correlated corruption.

## Worked Examples

### Example 1

**Persistent single rotation.** Insert `30,20,10`. The old root `30(20,_)` remains. The new local result is `20(10,30)`. Construct new `30` first, then new `20`; do not recolor/repoint old nodes. In-order remains `10,20,30`, heights become one and two. Conclusion: a rotation preserves mapping but allocates a replacement local spine.

### Example 2

**Untouched-subtree sharing.** From `20(10,30)`, insert `25`. Descent visits `20,30`; new `25` becomes `30.left`; replacements are `30` and `20`. Node `10` is outside the changed frontier and can be identical across roots. Conclusion: point update allocates by changed height while safely sharing the sibling subtree.

### Example 3

**Replacement without shape change.** Replace value at key `30`. Search copies ancestors and the entry node unless values compare equal and no-op policy returns the old root. Children of `30` can be reused. Conclusion: logical update cost can be logarithmic even with no rotation; key/entry identity policy must be explicit.

### Example 4

**Stale-size corruption.** A node previously had left size 3 and right size 2, stored size 6. Persistent insertion makes left size 4 but copied parent keeps 6. Membership/order still work; selecting rank 6 or parent ancestors using weight can fail. Conclusion: every augmented field is part of correctness and must be recomputed bottom-up.

### Example 5

**Deletion frontier.** Delete a two-child key `20` using successor `25` found down the right subtree. Rebuild the successor-removal path, replace the target entry, then repair/recompute toward root. An untouched outer subtree may share; target and extraction ancestors may not. Conclusion: deletion can change a broader connected frontier than the initial lookup path.

### Example 6

**Comparator failure.** Keys are mutable records ordered by `user.name`; after insertion, a name changes. The node remains at its old position, so lookup by new name follows another path and duplicates may appear. Every version sharing the key observes mutation. Conclusion: persistent tree nodes do not compensate for unstable key ordering.

### Example 7

**Split and join.** Split keys `{1,3,5,7,9}` at `5`: result below `{1,3}`, found `(5,v)`, above `{7,9}`. Joining those with `(5,v)` must reconstruct a balanced tree equal to the original map, though shape/identity may differ. Conclusion: split/join correctness is mapping equality plus balance, not restoration of the same pointers.

### Example 8

**Two concurrent writers.** Both read root `{a}`; one builds `{a,b}`, one `{a,c}`. Both are valid persistent branches. Unconditional latest-root stores lose one. CAS makes one publication linearize and forces the other to retry/branch/merge. Conclusion: immutability gives safe candidates, not an automatic conflict policy.

### Example 9

**Reader retention.** A long iterator pins a million-node old root while writers create and publish later roots. New and old roots share most nodes, but changed historical paths and their subtrees remain live. Current-root size underreports memory. Conclusion: track reader/root age and union reachability, and bound retention according to semantics.

### Example 10

**Representation selection.** A symbolic engine needs branching maps, rank/select, large union/intersection, deterministic results, and parallel bulk work. A proven join-based weight-balanced tree can integrate sizes and divide-and-conquer operations; AVL point updates alone make bulk algebra less direct, while randomized treaps weaken determinism. Conclusion: select the proven operation family, then benchmark real keys/runtime rather than choosing by rotation folklore.

## Cross-Program Connections

- Algorithm engineering: join-based set algebra, work/span, comparator counts, and adversarial sequences connect proofs to measured algorithms.
- Programming languages: algebraic data types/pattern matching express functional repairs; ownership and GC define safety/lifetime.
- Database engineering: copy-on-write indexes, MVCC roots, range scans, root publication, and vacuum mirror version/read retention.
- Concurrent programming: snapshot reads, CAS roots, epoch/hazard lifetime, retry semantics, and parallel bulk operations require explicit progress models.
- Formal methods: red-black/AVL invariants and functional code are strong candidates for induction, refinement, proof assistants, and cost verification.
- Security: comparator attacks, root pinning, deep/corrupt graph input, timing/sharing leakage, and unbounded diffs require isolation/quotas.
- Distributed systems: immutable roots/content hashes support replication and snapshots, but consensus, authorization, and durability remain external protocols.
- Performance engineering: copied bytes, cache locality, allocator/collector behavior, branch histories, and tail latency decide production fitness.

## References

1. Chris Okasaki, *Purely Functional Data Structures*, PhD thesis, Carnegie Mellon University, 1996. https://www.cs.cmu.edu/~rwh/students/okasaki.pdf
2. Chris Okasaki, “Red-Black Trees in a Functional Setting,” *Journal of Functional Programming* 9(4), 1999. https://www.cambridge.org/core/journals/journal-of-functional-programming/article/redblack-trees-in-a-functional-setting/62BC5EA75A2C95E3F6EE95AE3DADF0E5
3. Stephen Adams, “Efficient Sets—A Balancing Act,” *Journal of Functional Programming* 3(4), 1993. https://www.cambridge.org/core/services/aop-cambridge-core/content/view/0CAA1C189B4F7C15CE9B8C02D0D4B54E/S0956796800000885a.pdf/functional-pearls-efficient-setsa-balancing-act.pdf
4. Andrew W. Appel et al., “Implementation and Proof of Red-Black Trees,” *Verified Functional Algorithms*, Princeton. https://www.cs.princeton.edu/courses/archive/spring17/cos510/vfa/Redblack.html
5. Andrew W. Appel, “Efficient Verified Red-Black Trees,” 2011. https://www.cs.princeton.edu/~appel/papers/redblack.pdf
6. Tobias Nipkow, “Root-Balanced Tree,” Archive of Formal Proofs, current proof document. https://www.isa-afp.org/browser_info/current/AFP/Root_Balanced_Tree/document.pdf
7. Clojure, `PersistentTreeMap.java`, current implementation source, retrieved 2026-08-30. https://github.com/clojure/clojure/blob/master/src/jvm/clojure/lang/PersistentTreeMap.java
8. Haskell `containers`, `Data.Map.Internal`, current implementation source, retrieved 2026-08-30. https://github.com/haskell/containers/blob/master/containers/src/Data/Map/Internal.hs

## Exercises

### Exercise 1

**Trace a persistent rotation.** Starting with immutable AVL root containing `40,20,60,10,30`, insert `5`. Identify the search path, new nodes, rotation, reusable subtrees, and final in-order sequence.

### Exercise 2

**Prove metadata reconstruction.** For a persistent right rotation `z(y(A,B),C) -> y(A,z(B,C))`, derive the correct height and size construction order and explain why copying old metadata is unsound.

### Exercise 3

**Design deletion evidence.** Specify a test/reference/validator plan strong enough to add persistent AVL deletion to the executable chapter implementation, including failure and branching cases.

### Exercise 4

**Compare tree families.** Choose among AVL, red-black, weight-balanced, treap, and rebuild-based trees for (a) lookup-heavy immutable configuration snapshots; (b) rank/select plus bulk union; and (c) content-addressed untrusted keys. State conditional choices and required evidence.

### Exercise 5

**Transfer to durable MVCC indexing.** A service wants each committed version to be a persistent balanced-tree root stored on disk and concurrently read by snapshots. Design the additional page, publication, recovery, reclamation, migration, and verification contracts beyond the in-memory proof.

## Answers to the Exercises

### Answer 1

Search path is `40 -> 20 -> 10 -> empty`; allocate `5`, then replacement `10`, replacement `20`, and initially replacement `40`. The root becomes left-left heavy, so right-rotate at `40`: construct a new lower `40` whose left is old/shared `30` and right is old/shared `60`, then new root `20` whose left is new `10(5,_)` and right is new `40(30,60)`. Reusable nodes include `30` and `60`; old roots/nodes remain unchanged. Final in-order sequence is `5,10,20,30,40,60`. Exact temporary allocation depends on whether the implementation fuses construction and rotation; count actual constructors.

### Answer 2

Let stored metadata be pure functions. First build `z' = node(z,B,C)`: `h(z')=1+max(h(B),h(C))`, `s(z')=1+s(B)+s(C)`. Then build `y'=node(y,A,z')`: `h(y')=1+max(h(A),h(z'))`, `s(y')=1+s(A)+s(z')`. Building root first would lack final child metadata. Old `z` described child `y` rather than `B`, and old `y` described right `B` rather than `z'`; copying either height/size can therefore be wrong. The order proof follows `A<y<B<z<C`, so both shapes have the same in-order sequence.

### Answer 3

Use an independent sorted map per version. Exhaust empty/absent, leaf, root, one-child, two-child, predecessor/successor, minimum/maximum, and every single/double deletion rotation, plus sequences where height decreases propagate repeatedly. Generate sorted, reverse, alternating, random, duplicate/replacement, delete/reinsert, and branch-from-every-version histories. After every operation compare all retained roots' ordered entries/lookups/sizes and old digests.

The validator independently checks strict bounds, acyclicity, exact height/size, balance factor at every node, and element policy. White-box checks assert old nodes never change, untouched siblings share when promised, and changed nodes do not incorrectly share. Fault-inject comparisons and every allocation/metadata/rotation publication point; old roots must survive and partial nodes release. Add deep/corrupt serialized inputs, length overflow, refcount/GC retention, concurrent publication/retry, sanitizers, and allocation/leak instrumentation. Only after these and a deletion proof should complexity/completion claims include deletion.

### Answer 4

For lookup-heavy snapshots, AVL is a reasonable conditional choice because of tight height, provided update cost and retention benchmarks pass; a mature red-black implementation may win through library proof/operational maturity. For rank/select and bulk union, a proven join-based weight-balanced tree integrates subtree sizes and size-sensitive divide-and-conquer algebra. Validate exact balance constants and union work/span.

For content-addressed untrusted keys, deterministic AVL/red-black/verified weight balance avoids adversarial randomized-priority ambiguity; cryptographic-priority treaps are possible only with a named threat model and collision/seed policy. In all cases require stable bounded comparators/encodings, canonical hash construction, full invariant checks, memory/root quotas, hostile-input validation, and measurements of comparisons, height, allocations, live bytes, cache/GC, and tail latency. There is no unconditional family winner.

### Answer 5

Use immutable checksummed page/node records with stable IDs, schema/comparator version, bounds, metadata, and child IDs. Copy changed pages; write children before parents; flush according to the storage contract; then atomically publish a checksummed commit/root manifest containing generation and parent/provenance. Recovery selects a fully valid committed root, rejects/tolerates torn orphan writes by policy, and never follows unvalidated IDs.

Readers pin root generations through transactions/leases; writers serialize, conflict-detect, or branch/merge. Reclamation traces every committed/reader/backup/replication root and frees pages only after snapshot and crash-safety constraints. Track oldest reader and retained bytes. Comparator/key/schema changes rebuild into a new generation; do not reinterpret old ordering. Validate page bounds, acyclicity, strict key ranges, balance, metadata, reachability, checksums, quotas, and logical equality against a reference. Fault-inject each write/flush/root swap, test crash recovery and garbage collection, authorize per snapshot/range, and benchmark page-copy bytes, amplification, recovery, compaction, and tail latency. These storage/MVCC obligations are additional to the in-memory functional tree proof.
