---
module_id: DSE-072
program: Data Structures Engineering
level: 2
module_number: 72
title: B-Trees
status: complete
last_verified: 2026-08-30
---

# B-Trees

## One-Page Review

### Governing question

How can a high-fan-out balanced search tree maintain ordered records in a bounded number of page transfers while preserving occupancy, separator, durability, and concurrency invariants through splits, merges, and root changes?

### Essential definitions

- A **B-tree of minimum degree t >= 2** is a rooted multiway search tree in which each node holds at most `2t-1` ordered keys and at most `2t` children.
- Every nonroot node holds at least `t-1` keys; an internal nonroot node therefore has at least `t` children. A nonempty root has at least one key and, if internal, at least two children.
- For internal node keys `k[0..m-1]` and children `c[0..m]`, every key in `c[i]` lies between its adjacent separators under the tree's duplicate-key policy.
- All leaves have the same depth. This is the balance invariant, not a statistical expectation.
- A **split** promotes a median key and partitions one full child into two legal nodes before descent in the top-down insertion algorithm.
- A **borrow/rotation** transfers a separator through the parent from a sufficiently occupied sibling. A **merge** combines two minimally occupied siblings with their parent separator.
- The classic B-tree can store a key's satellite record in any node. A B+ tree normally keeps data entries at leaves; DSE-073 treats that distinct contract.
- **Fan-out** is determined by encoded bytes, not an abstract key count, when keys and records are variable length.

### Central model, mechanism, or theorem

For height h measured in edges and minimum degree t, the minimum number of keys in a nonempty B-tree of height h is

`n_min(h) = 1` when `h=0`, and `n_min(h)=2t^h-1` when `h>=1`.

The maximum is `n_max(h)=(2t)^(h+1)-1`. Consequently, for n >= 1,

`h <= floor(log_t((n+1)/2))`,

and search uses `h+1 = O(log_t n)` node visits. With a page-sized node and high effective t, height and external transfers stay small. CPU comparisons within a node, cache behavior, variable encodings, buffer hits, concurrency restarts, and recovery writes remain separate costs.

Top-down insertion never descends into a full child: split it first, compare against the promoted median, and descend into a nonfull result. Top-down deletion never descends into a child with only `t-1` keys: borrow from a sibling with at least t keys or merge before descent. These strengthened preconditions localize repair, but a durable concurrent implementation must additionally log structural changes, control latches, publish sibling/root identities safely, and recover allocation state.

### Critical invariants

1. Keys within every node are strictly ordered, or ordered by an explicit duplicate/tie-break policy.
2. An internal node with m keys has exactly `m+1` valid child references.
3. Child key ranges agree with every parent separator; no key is lost or appears twice unless duplicates are intentional records.
4. Every leaf has the same depth.
5. Nonroot occupancy is `[t-1,2t-1]`; root exceptions are explicit.
6. A split, rotation, merge, and root contraction conserve the logical ordered multiset.
7. Page identifiers, generations, latches, pins, WAL records, and allocation ownership remain valid across structural modification.

### Common failures

- Calling every database ordered index a B-tree while silently assuming B+ leaf-only records.
- Computing degree from nominal page bytes while ignoring headers, slots, child IDs, record payloads, prefixes, alignment, or worst-case encodings.
- Descending into a full child during insertion or a minimal child during deletion, forcing awkward upward repair.
- Promoting/copying the wrong boundary key and leaving child ranges inconsistent.
- Treating deletion as “remove the key”; internal replacement, borrow, merge, and root contraction are essential.
- Holding latches in an order that deadlocks, releasing a parent before a child is structurally safe, or following recycled page IDs.
- Logging individual page images without a recoverable contract for the multi-page structural change and allocator.
- Claiming logarithmic CPU time from a page-I/O height bound or production correctness from a bounded in-memory model.

### Compact example

With t=2, nodes hold one through three keys except for the root. Inserting `10,20,5,6,12,30,7,17` by preemptive splitting produces root `[10,20]` and three leaves `[5,6,7]`, `[12,17]`, `[30]`. Every leaf is at depth one; an in-order walk returns the inserted set. This exact finite case exercises root split, child split, median promotion, and two search outcomes.

### Connections

B-trees combine comparison search (DSE-021), multiway-tree invariants (DSE-033), external-memory/page design (DSE-071), and transactional storage. DSE-073 changes record placement and leaf traversal for B+ trees; DSE-074 builds trees in bulk; DSE-075 changes mutation publication with copy-on-write. Database Engineering later adds index semantics, transactions, MVCC, WAL, and query planning.

## Governing Question

How do we move from the mathematical B-tree—a perfectly balanced multiway search tree—to a page-resident, crash-recoverable, concurrent ordered index without confusing the proof obligations of one layer with evidence about another?

## Why This Matters

A binary search tree spends one pointer traversal per comparison level. On external or remote storage, the expensive unit is often a page request, so a node should use one transfer to discriminate among many ranges. A B-tree turns page capacity into fan-out while bounding every root-to-leaf path to the same height. It supports exact lookup, ordered traversal, insertion, and deletion without periodically rebuilding the whole index.

That compact description hides the engineering. A page may fit different numbers of variable-length keys. Separator semantics differ among variants. Duplicate keys need a total order or posting representation. A split mutates a child, parent, allocator, and sometimes root. Concurrent readers must not miss a key while those pages change. A crash between writes must recover either a valid earlier or valid later logical tree. An online checker must distinguish transient structural states protected by latches from published corruption.

The durable skill is therefore not memorizing split diagrams. It is defining the exact tree variant, deriving occupancy and height, implementing conservative transformations, and attaching each correctness claim to appropriate evidence: proof for abstract invariants, exact executable traces for bounded algorithms, byte/fuzz tests for formats, schedule exploration for concurrency, crash injection for recovery, and workload measurements for performance.

## Prerequisites and Retrieval

Retrieve before continuing:

- comparison ordering, lower/upper bound, stable tie-breakers, and in-order traversal;
- rooted-tree depth, height, subtree range, and inductive invariants;
- external-memory parameters N, M, B and the difference between I/O and CPU cost;
- page IDs, slotted pages, encoded-byte validation, pin/latch/dirty state, WAL, and torn writes;
- atomicity, linearizability, lock/latch ordering, generations, and safe reclamation;
- checked arithmetic, corruption handling, property tests, model checking, and fault injection.

Diagnostic retrieval: for t=3, state nonroot key bounds, maximum children, and the minimum key count at height two. The answers are 2 through 5 keys, 6 children, and `2*3^2-1=17` keys. If those are not immediate, review the one-page derivation before implementing transformations.

## Learning Objectives

After this module, you can:

1. specify classic B-tree node, ordering, occupancy, balance, duplicate, and root contracts;
2. derive minimum/maximum population, height, search transfers, and byte-based fan-out bounds;
3. trace search and top-down insertion with median promotion and root growth;
4. implement deletion through leaf removal, predecessor/successor substitution, borrow, merge, and root contraction;
5. distinguish classic B-trees from B+ trees and other ordered storage variants;
6. map nodes to hostile-input-validated pages with stable identity and allocation ownership;
7. design latch, publication, WAL, recovery, verification, migration, and observability contracts;
8. evaluate correctness and performance without overgeneralizing bounded tests or asymptotic I/O results.

## Core Exposition

**Specify the variant first.** Let minimum degree t be at least two. A node stores an ordered sequence of key-record entries and, if internal, one more child than keys. Classic B-tree lookup may terminate at an internal node because satellite records may live there. If duplicates are allowed, compare a composite such as `(user_key,record_id)` or define a duplicate container; “equal goes right” alone is insufficient across split, delete, and recovery unless universally enforced.

**Ordering partitions the universe.** With keys `k0 < ... < k(m-1)`, child c0 contains values below k0, child ci contains values between `k(i-1)` and ki, and cm contains values above the last key. Boundary inclusion follows the duplicate policy. Search performs lower-bound within the node: return on equality; otherwise descend through the corresponding gap. A malformed child count or separator invalidates this reasoning.

**Occupancy creates logarithmic height.** Each nonroot node has at least t-1 and at most 2t-1 keys. At height h>=1, the root has at least two children; each successive internal nonroot level multiplies node count by at least t. Summing the minimum keys gives one root key plus `(t-1)` keys per nonroot node: `1 + 2(t-1)(1+t+...+t^(h-1)) = 2t^h-1`. Solving yields the height bound. Maximum population follows a full 2t-ary tree. The result assumes fixed count capacity; page implementations must derive conservative effective capacity from bytes or use byte-occupancy rules whose proof differs.

**Search has two cost axes.** A root-to-leaf search reads at most h+1 nodes. If each node is a page and the buffer misses, that is h+1 page transfers. Within-node linear search costs O(t) comparisons; binary search costs O(log t), but branch prediction, prefix compression, SIMD, cache lines, and key decoding can dominate. Root and upper levels are often cached. Report logical page visits, physical reads, buffer hits, comparisons, decoded bytes, and latency separately.

**Insertion strengthens the descent condition.** If the root is full, allocate a new empty root, make the old root its child, and split that child; height grows by one. At a nonfull internal node, choose child i. If it is full, split it around median key `t-1`: the median moves into the parent; left and right retain `t-1` keys; children partition similarly. Recompare with the promoted key and descend into a nonfull child. Insert into the sorted leaf. The abstract operation conserves all entries and creates legal occupancy.

**Split publication is more than array slicing.** On pages, reserve a new page and generation; decide exact split point by encoded bytes while retaining legal minimum occupancy; initialize the right page and its sibling/fence metadata if the variant has it; update the left; install the parent separator; and make allocation plus page changes recoverable. Parent overflow can propagate to the root. A failure at every boundary must have a redo/undo or copy-on-write outcome.

**Deletion has six semantic cases.** Search for key x at node u. If u is a leaf, remove x. If x occurs in internal u and the left child has at least t keys, replace x with its predecessor record and recursively delete that predecessor. Else if the right child has at least t, use its successor. Else merge both t-1-key children with x into one `2t-1`-key child and continue there.

If x is not in internal u, identify child c. Before descent, ensure c has at least t keys. Borrow through the parent from an adjacent sibling with at least t keys; otherwise merge c with an adjacent minimal sibling and the intervening parent separator. Then descend. If the root loses its last key and has one child, make that child the root and retire the old root. An empty leaf root represents an empty tree. Exact boundary indexes and duplicate identity are frequent defect sites.

**Rotation preserves order.** Borrowing from the left moves the parent's left separator into the front of c and moves the left sibling's greatest key into the parent; an internal child pointer moves with its range. Borrowing from the right is symmetric. It is not valid to copy a sibling key directly without rotating the parent separator, because the parent partitions ranges.

**Merge conserves the multiset.** Merge left child, parent separator, and right child in that order. For minimum-degree children, `(t-1)+1+(t-1)=2t-1`, exactly the maximum. Move right child pointers if internal, remove one separator and child reference from the parent, and retire the right page only when no reader or recovery path can mistake a recycled identity.

**Variable-length pages complicate minimum degree.** A count-based t assumes each entry has bounded equal cost. Real separator keys, records, child IDs, slots, prefixes, and versions vary. Options include enforcing maximum key/record sizes and a conservative t; defining byte fullness plus count/space safety; storing large records out of line; truncating internal separators under a proven routing rule; and redistributing by bytes. Never claim the textbook occupancy theorem for a representation that cannot guarantee its premises.

**Durability spans a structural modification operation.** A split/merge may touch two children, a parent, allocator metadata, sibling links, root metadata, and free-page state. Physiological WAL can log page-local changes plus structural intent; shadow paging can publish a new root after writing new paths. Define redo idempotence, undo or logical compensation, page LSN rules, allocation ownership, flush ordering, torn-page detection, and root selection. A page checksum alone cannot make a half-published tree logical.

**Concurrency needs a traversal protocol.** Basic latch coupling pins/latches the child before releasing the parent and retains ancestors when a split/merge may propagate. Optimistic traversal may read versions, descend without long parent holds, validate, and restart on change. B-link variants add high keys and right links so searches can move right across concurrent splits; that is a different, explicitly proven protocol. Logical transaction locks/MVCC protect user records and predicates; short physical latches protect page structure. Mixing them produces deadlocks and incorrect isolation.

**A bounded insertion model provides executable evidence.** The next model implements classic count-based B-tree search and preemptive insertion at t=2. It validates count, child, ordering, range, equal-depth, in-order, and membership properties for one deterministic trace.

<!-- bijux-verify: {"id":"bounded-b-tree-insertion-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"minimum_degree=2\ninserted=10,20,5,6,12,30,7,17\nroot=10,20\nleaves=5,6,7|12,17|30\nheight_edges=1\nsearch_17=10,20->12,17\nsearch_15=10,20->12,17\ncontains_17=True\ncontains_15=False\ninorder=5,6,7,10,12,17,20,30\nvalid=True\nevidence=bounded_b_tree_insertion_model\n","stderr":""}} -->
```python
class Node:
    def __init__(self, leaf=True):
        self.leaf = leaf
        self.keys = []
        self.children = []


class BTree:
    def __init__(self, degree):
        self.degree = degree
        self.root = Node()

    def split_child(self, parent, index):
        degree = self.degree
        full = parent.children[index]
        right = Node(full.leaf)
        median = full.keys[degree - 1]
        right.keys = full.keys[degree:]
        full.keys = full.keys[:degree - 1]
        if not full.leaf:
            right.children = full.children[degree:]
            full.children = full.children[:degree]
        parent.keys.insert(index, median)
        parent.children.insert(index + 1, right)

    def insert_nonfull(self, node, key):
        index = len(node.keys)
        if node.leaf:
            node.keys.append(key)
            while index > 0 and node.keys[index - 1] > key:
                node.keys[index] = node.keys[index - 1]
                index -= 1
            node.keys[index] = key
            return
        while index > 0 and key < node.keys[index - 1]:
            index -= 1
        if len(node.children[index].keys) == 2 * self.degree - 1:
            self.split_child(node, index)
            if key > node.keys[index]:
                index += 1
        self.insert_nonfull(node.children[index], key)

    def insert(self, key):
        if len(self.root.keys) == 2 * self.degree - 1:
            new_root = Node(False)
            new_root.children.append(self.root)
            self.split_child(new_root, 0)
            self.root = new_root
        self.insert_nonfull(self.root, key)

    def search_path(self, key):
        node = self.root
        path = []
        while True:
            path.append(",".join(str(value) for value in node.keys))
            index = 0
            while index < len(node.keys) and key > node.keys[index]:
                index += 1
            if index < len(node.keys) and key == node.keys[index]:
                return True, "->".join(path)
            if node.leaf:
                return False, "->".join(path)
            node = node.children[index]


def walk(node):
    result = []
    for index, key in enumerate(node.keys):
        if not node.leaf:
            result.extend(walk(node.children[index]))
        result.append(key)
    if not node.leaf:
        result.extend(walk(node.children[-1]))
    return result


def validate(node, degree, is_root, low=None, high=None, depth=0):
    maximum = 2 * degree - 1
    minimum = 0 if is_root else degree - 1
    count_ok = minimum <= len(node.keys) <= maximum
    order_ok = all(node.keys[i] < node.keys[i + 1] for i in range(len(node.keys) - 1))
    range_ok = all((low is None or low < key) and (high is None or key < high) for key in node.keys)
    child_ok = node.leaf and len(node.children) == 0 or not node.leaf and len(node.children) == len(node.keys) + 1
    if not (count_ok and order_ok and range_ok and child_ok):
        return False, []
    if node.leaf:
        return True, [depth]
    depths = []
    for index, child in enumerate(node.children):
        child_low = low if index == 0 else node.keys[index - 1]
        child_high = high if index == len(node.keys) else node.keys[index]
        valid, child_depths = validate(child, degree, False, child_low, child_high, depth + 1)
        if not valid:
            return False, []
        depths.extend(child_depths)
    return len(set(depths)) == 1, depths


values = [10, 20, 5, 6, 12, 30, 7, 17]
tree = BTree(2)
for value in values:
    tree.insert(value)

found_17, path_17 = tree.search_path(17)
found_15, path_15 = tree.search_path(15)
valid, leaf_depths = validate(tree.root, tree.degree, True)
leaves = "|".join(",".join(str(value) for value in child.keys) for child in tree.root.children)
print(f"minimum_degree={tree.degree}")
print("inserted=" + ",".join(str(value) for value in values))
print("root=" + ",".join(str(value) for value in tree.root.keys))
print(f"leaves={leaves}")
print(f"height_edges={leaf_depths[0]}")
print(f"search_17={path_17}")
print(f"search_15={path_15}")
print(f"contains_17={found_17}")
print(f"contains_15={found_15}")
print("inorder=" + ",".join(str(value) for value in walk(tree.root)))
print(f"valid={valid}")
print("evidence=bounded_b_tree_insertion_model")
```

The model assumes unique integer keys, uniform count capacity, atomic in-memory mutations, no deletion, no byte encoding, and no I/O. It performs no allocation persistence, latching, logging, recovery, reclamation, corruption handling, or performance experiment. Its successful run establishes only the stated finite trace and validator predicates.

**Verification must be layered.** Unit-test every split position, root growth, search gap, duplicate policy, deletion case, rotation direction, merge edge, and root contraction. Compare random operation sequences with an ordered-map oracle. Exhaustively enumerate small trees and transformations. Validate serialized pages from arbitrary bytes using checked bounds. Model concurrent structural schedules and reclamation. Crash at every log/page/allocator/root publication boundary and reopen with an independent verifier. Benchmark only after correctness gates pass.

**Online invariants need a snapshot definition.** A verifier may traverse a quiescent tree, a consistent copy/snapshot, or pages under a documented latch/version protocol. Reading pages independently during live splits can observe a mixture that never represented one state. Record root identity/generation, page versions, traversal restarts, unreachable allocations, duplicate ownership, range violations, occupancy exceptions, and checksum failures. Repair should not guess; quarantine, reconstruct from trusted records/log/replica, or rebuild under an explicit plan.

**Production rollout treats format as an API.** Version page and metadata formats; maintain golden old-version fixtures; provide offline inspect/dump/verify/rebuild tools; define upgrade, rollback, and mixed-version behavior; canary new writers while old readers remain understood. Track height, occupancy by level, split/merge/rotation rates, root changes, page reads/hits, latch waits/restarts, WAL bytes, dirty flushes, free/retired pages, corruption detections, recovery duration, and tail latency.

## Definitions and Notation

Let t be minimum degree, h height in edges, n total key-record entries, and m a node's current key count. A nonroot node has `t-1 <= m <= 2t-1`; an internal node has `m+1` children. Root has `1 <= m <= 2t-1` when nonempty, except an empty leaf root may have zero. `K(u)` is u's ordered keys; `C(u,i)` is child i; `range(u)` is the interval permitted by ancestors.

`Search(x)` follows lower-bound gaps. `Split(p,i)` splits full `C(p,i)`. `RotateLeft/Right` borrows through the parent. `Merge(p,i)` joins children i and i+1 with separator i. `PageId` is stable logical page identity; generation distinguishes reuse. `LSN(page)` identifies the latest logged change represented. A latch protects physical structure; a transaction lock/predicate mechanism protects logical isolation.

Height bounds assume the count-based definition. `IO_search <= h+1` counts cold node-page transfers in the direct mapping; buffer hits reduce physical reads. CPU work depends on the within-node algorithm and encoding. Space utilization bounds exclude page headers and external allocator overhead unless incorporated into capacity.

## Mechanisms, Invariants, or Proof Structure

### Height proof

1. At height h>=1, the root contributes at least one key and two children.
2. Every nonroot internal node contributes at least t children and every nonroot node at least t-1 keys.
3. Level i>=1 therefore has at least `2t^(i-1)` nodes.
4. Summing minimum keys through level h gives `1 + 2(t-1) sum(i=0..h-1)t^i = 2t^h-1`.
5. Thus `t^h <= (n+1)/2`, yielding the logarithmic height bound.

### Transformation proof

1. Define the ordered multiset and subtree intervals before mutation.
2. For split, show left/median/right partition the full node and both children meet occupancy.
3. For rotation, show the parent separator mediates the transfer and all child pointers retain their intervals.
4. For merge, show two minimal children plus separator fit exactly and conserve order/membership.
5. For root growth/contraction, show every leaf depth changes uniformly or the redundant root is removed uniformly.
6. Induct on descent with the strengthened nonfull/nonminimal child precondition.

### Storage proof

1. Decode and validate page identity, version, checksum, counts, slots, keys, child IDs, and range metadata before access.
2. Pin and latch pages under one deadlock/restart protocol; distinguish logical transaction protection.
3. Make new-page allocation, structural pages, parent/root publication, and retirement one recoverable operation.
4. Validate page LSN and flush ordering; prevent stale I/O or recycled generations from publishing into a new owner.
5. Recover, then independently traverse from the selected root and reconcile reachable versus allocated pages.
6. Treat crash/fault/schedule results as empirical evidence scoped to tested histories.

## Alternatives and Trade-Offs

| Design | Strength | Cost or proof burden |
|---|---|---|
| Classic B-tree | records may be found before leaf | variable internal payload lowers fan-out |
| B+ tree | dense routing and linked-leaf ranges | duplicate separators and leaf protocol |
| Fixed count degree | clean textbook proof | unrealistic for variable encoded bytes |
| Byte-balanced node | better page utilization | split feasibility and occupancy proof harder |
| Preemptive split/delete repair | single downward abstract pass | may modify nodes unnecessarily |
| Bottom-up repair | defer structural writes | needs ancestor state/restart propagation |
| Latch coupling | direct safety argument | contention and deadlock discipline |
| Optimistic versions | short common-case holds | validation/restart and reclamation complexity |
| WAL in-place | compact updates and mature recovery | multi-page structural logging burden |
| Copy-on-write path | atomic root publication/snapshots | write amplification and reclamation |
| Eager merge | stronger utilization | write/latch amplification and churn |
| Lazy underflow cleanup | fewer foreground writes | weaker occupancy/height-space guarantees |

The correct selection follows workload, key/record distribution, page format, isolation, recovery objectives, device hierarchy, and operational capacity. Name the variant and restate its invariants; do not inherit textbook bounds after changing repair thresholds or representation.

## Failure Modes and Misconceptions

- **“B-tree means B+ tree.”** State record placement, separator, and leaf-link rules.
- **“Order m has one universal definition.”** Literature uses order for different maxima/minima; specify t and exact bounds.
- **“Balanced means half the keys on each side.”** It means equal leaf depth; occupancy has separate bounds.
- **“Binary search makes lookup O(log n) I/Os.”** Height controls page visits; within-page search controls CPU.
- **“A median split is always byte-balanced.”** Variable encodings can make count and byte balance diverge.
- **“Promote a copy and keep everything.”** Classic B-tree promotion removes the median from children; B+ rules differ.
- **“Delete from a leaf and stop.”** Internal cases, underflow prevention, and root contraction preserve structure.
- **“Borrow directly from the sibling.”** Rotate through the parent separator and move the matching child pointer.
- **“A merge may overflow.”** Two minimal children plus one separator total exactly `2t-1` in the classic model.
- **“Page checksum proves tree correctness.”** It detects selected byte corruption, not range, reachability, or atomic publication errors.
- **“Pinning is locking.”** Pin controls residency; latch protects page structure; transaction mechanisms protect logical semantics.
- **“WAL one page at a time is enough.”** Allocator, parent/root, retirement, and structural relationships need recoverable intent.
- **“Passing random inserts proves deletion.”** Each delete case and adversarial boundary requires separate evidence.
- **“High average occupancy guarantees performance.”** Height, hot contention, tails, cache state, and amplification matter.

## Worked Examples

### Example 1

**Problem.** For t=50 and height h=3, bound n.

**Derivation.** Minimum is `2*50^3-1=249,999`. Maximum is `100^4-1=99,999,999`. The broad interval reflects occupancy; it does not include headers or variable byte capacity.

**Conclusion.** High fan-out supports enormous populations at small height.

### Example 2

**Problem.** Trace insertion of the executable sequence at t=2.

**Derivation.** The full root `[5,10,20]` splits before 6 descends, promoting 10. Later full child `[12,20,30]` splits before 17 descends, promoting 20. The final three leaves satisfy one-to-three-key bounds.

**Conclusion.** Preemptive splitting makes every recursive insertion target nonfull.

### Example 3

**Problem.** A t=3 internal key is deleted; its adjacent children have 4 and 2 keys.

**Derivation.** The left has at least t keys, so replace the internal entry with its predecessor from the left subtree, then delete that exact predecessor there. Duplicate identity must include the record/tie-breaker.

**Conclusion.** Replacement preserves routing while reducing a child that can tolerate deletion.

### Example 4

**Problem.** Before deletion descent at t=3, target child has 2 keys and its right sibling has 3.

**Derivation.** Rotate left: move parent separator into target; move sibling minimum into parent; if internal, move sibling's leftmost child to target's right edge. Both children remain legal.

**Conclusion.** Borrowing is a three-party ordered transformation.

### Example 5

**Problem.** Both target and adjacent sibling have t-1 keys.

**Derivation.** Merge left keys, intervening parent separator, then right keys. The result has `2t-1` keys. Parent loses one key and child pointer; descent continues into the merged page.

**Conclusion.** Minimum occupancy makes the merged result fit exactly.

### Example 6

**Problem.** A root with one separator merges its two minimal children during deletion.

**Derivation.** The root becomes empty with one child. Promote that child as root and retire the old root under generation/recovery rules. Every leaf depth decreases by one.

**Conclusion.** Deletion is the only classic operation that contracts height.

### Example 7

**Problem.** A 4 KiB internal page has 96 bytes fixed overhead, 16-byte slots, 8-byte child IDs, and maximum encoded separator 40 bytes. Bound keys conservatively.

**Derivation.** m keys require roughly `96 + m*(16+40) + (m+1)*8 = 104 + 64m`. Thus `m <= floor((4096-104)/64)=62`. Choose a maximum no greater than 62 and a t consistent with all required states and other metadata.

**Conclusion.** Degree comes from worst-case encoded layout, not page size alone.

### Example 8

**Problem.** A concurrent reader releases the parent then follows a child while a split replaces routing.

**Derivation.** Without child latch/version validation or a proven right-link/high-key protocol, it can enter an obsolete range or recycled page. Use latch coupling or optimistic validation/restart; delay reclamation by generation/epoch rules.

**Conclusion.** The sequential range proof does not automatically survive concurrent publication.

### Example 9

**Problem.** A crash occurs after writing a new right page but before its parent separator.

**Derivation.** Recovery must know whether the new allocation is unreachable garbage to reclaim or part of a logged split to redo. Page checksums cannot decide logical ownership. WAL/structural intent and allocator reconciliation must agree.

**Conclusion.** Structural atomicity includes reachability and allocation.

### Example 10

**Problem.** An implementation reports three-page average lookup and 80% occupancy.

**Derivation.** Request cold/warm physical reads, page visits, height distribution, key decoding, latch waits/restarts, p99, split/merge and WAL bytes, crash recovery, and corrupt-page tests. Average lookup and occupancy cannot establish durability or tail objectives.

**Conclusion.** Performance evidence is multidimensional and follows correctness gates.

## Cross-Program Connections

- **Database Engineering:** ordered indexes add uniqueness, composite collation, MVCC visibility, predicate locking, optimizer statistics, WAL, vacuum, and online rebuild.
- **Operating Systems:** page cache/direct I/O, asynchronous completion, flush semantics, allocation, and device failure shape the page-transfer realization.
- **Concurrent and Parallel Programming:** latch coupling, optimistic version validation, deadlock order, B-link traversal, safe reclamation, and linearization govern live trees.
- **Security Engineering:** hostile page bytes, arithmetic overflow, decompression, stale identity, corruption repair, encryption context, and denial-of-service limits are trust boundaries.
- **Data Engineering:** sort/bulk load, partitioned indexes, range extraction, spill, and remote object layouts depend on fan-out and ordered access.
- **Formal Methods:** inductive range/occupancy/balance proofs, refinement from abstract maps, crash invariants, and bounded schedule exploration can verify separate layers.

## References

1. Rudolf Bayer and Edward M. McCreight, [“Organization and Maintenance of Large Ordered Indexes”](https://link.springer.com/article/10.1007/BF00288683), *Acta Informatica* 1, 1972. Original B-tree organization, occupancy, algorithms, analysis, and experiments.
2. David Lomet, [“Simple, Robust and Highly Concurrent B-trees with Node Deletion”](https://www.microsoft.com/en-us/research/publication/simple-robust-and-highly-concurrent-b-trees-with-node-deletion/), *IEEE ICDE*, 2004. Primary treatment of concurrent structural change, right-link safety, and node deletion.
3. Pat Morin, [“B-Trees”](https://opendatastructures.org/ods-python/14_2_B_Trees.html), *Open Data Structures*. Author-maintained formal educational treatment of external-memory multiway search trees.
4. Carnegie Mellon Database Group, [“Tree Indexes”](https://15445.courses.cs.cmu.edu/fall2024/notes/08-indexes1.pdf), 15-445/645 course notes, 2024. Authoritative educational treatment of B-tree-family invariants and implementation choices.
5. PostgreSQL Global Development Group, [“B-Tree Indexes”](https://www.postgresql.org/docs/current/btree.html), current documentation accessed 2026-08-30. Official production operator classes, behavior, implementation, deletion, and deduplication context.
6. PostgreSQL Global Development Group, [`nbtree` implementation README](https://github.com/postgres/postgres/blob/master/src/backend/access/nbtree/README), current source documentation accessed 2026-08-30. Maintainer detail on concurrency, splits, deletion, and invariants in a B-tree-family implementation.
7. SQLite Project, [“B-Tree Module”](https://sqlite.org/btreemodule.html), official module specification accessed 2026-08-30. Storage-engine interface, cursor, transaction, page, insertion, and deletion contracts.
8. SQLite Project, [`src/btree.c`](https://github.com/sqlite/sqlite/blob/master/src/btree.c), current source accessed 2026-08-30. Maintainer implementation evidence for a durable page-oriented B-tree-family storage engine.

## Exercises

### Exercise 1

For minimum degree t, state all classic B-tree invariants and derive minimum/maximum keys at height h plus the search-height bound. Separate page transfers from CPU comparisons.

### Exercise 2

At t=2, insert `8,9,10,11,15,20,17` with preemptive splitting. Draw every root/child state, search for 17 and 12, and verify occupancy, ranges, balance, and in-order contents.

### Exercise 3

Give complete top-down deletion pseudocode-level reasoning for leaf removal, internal predecessor/successor replacement, borrow from either side, merge, and root contraction. State how duplicates change identity.

### Exercise 4

Design a durable variable-length page implementation of a classic B-tree. Specify byte-capacity policy, format/parser, split/merge feasibility, page identity, latch/reclamation, WAL/recovery/allocation, verification, migration, and observability.

### Exercise 5

Audit a service that calls its index a B-tree, stores records only in linked leaves, sizes degree from average keys, releases parent before validating child, writes split pages independently, immediately recycles merged pages, and claims correctness from insert benchmarks. Diagnose each error and prescribe evidence gates.

## Answers to the Exercises

### Answer 1

Each node has ordered keys under one total duplicate policy. Internal m-key nodes have m+1 children whose ranges are partitioned by separators. Every leaf has identical depth. Nonroot keys are t-1 through 2t-1; nonroot internal children t through 2t. A nonempty root has at least one key and an internal root at least two children; empty tree is an empty leaf root.

Minimum population is 1 at h=0 and `2t^h-1` at h>=1 by one root key, two root children, branching at least t, and t-1 keys per nonroot node. Maximum is `(2t)^(h+1)-1`. Thus `h <= floor(log_t((n+1)/2))`; a mapped cold-page search visits h+1 pages. Within each page, linear search is O(t) comparisons and binary search O(log t), with encoding/cache effects outside this count.

### Answer 2

Insert 8: `[8]`; 9: `[8,9]`; 10: `[8,9,10]`. Before 11, split full root and promote 9: root `[9]`, children `[8] | [10]`, then insert 11 right: `[10,11]`. Insert 15 right: `[10,11,15]`. Before 20 descends, split that child and promote 11: root `[9,11]`, children `[8] | [10] | [15]`, then right becomes `[15,20]`. Insert 17 into right: `[15,17,20]`.

Search 17 follows root gap after 11 to `[15,17,20]` and succeeds. Search 12 follows the same gap and fails at that leaf. All leaves are depth one, each nonroot has one through three keys, ranges are `<9`, `(9,11)`, and `>11`, and in-order is `8,9,10,11,15,17,20`.

### Answer 3

At node u, if x is in leaf, remove it. If x is internal and left child has at least t keys, replace x with the maximum predecessor entry and recursively delete that exact entry; else use successor when right has at least t; else merge both minimal children with x and recurse into the merged child.

If x is absent at internal u, choose child c. Before descent ensure c has at least t keys: rotate through the parent from a sibling with at least t, moving the matching child pointer when internal; otherwise merge c with an adjacent minimal sibling and intervening separator, correcting the descent index. Afterward, if root is empty/internal, replace it with its only child; empty leaf root is allowed. Every case conserves ordered entries, ranges, equal leaf depth, and legal occupancy. Duplicate keys require exact composite identity such as `(key,record_id)` so replacement/deletion cannot remove a different equal record.

### Answer 4

Define version/endian, page type/ID/generation/LSN/checksum, key/record encoding, slots, child IDs, maximum item sizes, reserved bytes, overflow, and root metadata. Choose conservative count t from worst-case bytes or state/prove byte-based occupancy and split/merge feasibility. Parser uses checked arithmetic and validates sorted keys, child count/ranges, offsets/nonoverlap, types, checksum, and resource limits before exposure.

Use pin plus one latch/version protocol, ordered coupling or restart, and delayed generation-safe reclamation. A structural log record or documented physiological sequence covers allocation, left/right/parent/root pages, retirement, redo idempotence, undo/compensation, page LSN, WAL-before-data, torn writes, and allocator reconciliation. Independent snapshot/quiescent verifier checks reachability, ownership, cycles, ranges, occupancy, equal depths, free leaks, and page bytes after recovery.

Ship golden cross-version fixtures, random oracle comparison including all deletions, exhaustive small states, byte fuzz/mutation, bounded schedules, and crash injection at every publication/flush boundary. Provide dump/verify/rebuild, compatible readers/migration/rollback, and monitor height/occupancy, reads/hits, comparisons, splits/rotations/merges, latches/restarts, WAL/flush, allocations, corruption, recovery, and latency tails.

### Answer 5

Leaf-only records plus linked leaves describe a B+ contract, so rename/specify it and use the DSE-073 separator/range rules. Average-key degree cannot guarantee worst-case fit; bound encoded bytes or prove byte occupancy with maximum item/overflow rules. Releasing a parent without child latch or version validation makes traversal race with structural change; use coupling or a proven optimistic/right-link protocol.

Independent page writes do not make a split atomic: log/recover allocation, both children, parent or root publication, page LSN/flush order, and torn writes. Immediate page-ID reuse permits stale readers/I/O/WAL to access a new owner; use generations and safe retirement. Insert throughput tests establish only measured speed for sampled executions. Gate with abstract transformation proofs, executable operation oracles including deletion, page parser/fuzz tests, concurrency schedule checks, crash/recovery injection, independent tree/allocation audit, and then cold/warm workload/tail measurements.
