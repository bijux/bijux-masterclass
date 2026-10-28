---
module_id: DSE-051
program: Data Structures Engineering
level: 2
module_number: 51
title: Path Copying
status: complete
last_verified: 2026-08-30
---

# Path Copying

## One-Page Review

### Governing question

How can an update create a new version by copying only the search path while preserving every old version, sharing untouched substructure safely, and accounting for identity, memory reclamation, concurrency, persistence, and evidence?

### Essential definitions

- A **persistent data structure** preserves access to earlier versions after updates.
- **partial persistence** permits queries of all versions but updates only the newest; **full persistence** permits updates from any version; **confluent persistence** can combine versions.
- **path copying** allocates new nodes along the root-to-update path and reuses untouched subtrees.
- **structural sharing** means multiple immutable versions reference the same node/subtree.
- A **version root** identifies the entry point for one logical snapshot.
- A **fat node** stores several field values with version annotations as an alternative persistence technique.
- A **version DAG** records derivation/ownership among version roots; full persistence branches rather than forming one line.
- A **transient/ephemeral builder** temporarily allows controlled mutation under unique ownership before freezing an immutable value.
- **logical size** counts entries in one version; **physical live nodes** count unique allocated nodes reachable across retained versions.
- **retention amplification** is memory kept alive because old roots/readers reference shared generations.

### Central model, mechanism, or theorem

In an immutable binary search tree, searching for key `x` visits one root-to-leaf path. An insertion recursively constructs a new node at the change and, while returning, constructs one replacement for each ancestor with one new child and one original untouched child. Every node outside the path is shared. If tree height is `h`, update allocates `O(h)` nodes and query remains `O(h)`. A balanced tree gives logarithmic allocation/work; an unbalanced tree can copy linearly many nodes.

Correctness follows from immutability and reconstruction. Old nodes are never changed, so old roots preserve their maps. Each new ancestor copies its old key/value and the untouched child exactly; only the recursive child contains the specified update. BST/order/aggregate invariants are restored at each constructed node. A branch updated from an older root is isolated from later versions because it shares only immutable nodes.

Sharing changes the resource model. Summing logical sizes double-counts shared nodes; counting allocated nodes ignores reclaimed versions; reachable unique nodes depend on retained roots. Reference counting, tracing GC, epochs, arenas, or explicit ownership must reclaim nodes without freeing a subtree still shared by another root or reader.

### Critical invariants

1. Published nodes and referenced keys/values are immutable, or their interior mutability is excluded/versioned by contract.
2. Every version root reaches a structurally valid instance of the abstract data type and is associated with stable version metadata.
3. An update allocates all changed-path nodes and never rewires an old node reachable from another version.
4. Untouched subtrees may be shared only when their node/value lifetime outlives every referencing root/reader.
5. Per-node cached size, height, hash, balance, bounds, or aggregates are recomputed from the new children and valid in every version.
6. Failure before new-root publication leaves all existing versions unchanged; private partial nodes are safely destroyed.
7. Logical equality, object identity, entry identity, node address, and version identity are separate concepts.
8. Reference counts/GC roots/epochs/arena ownership cannot reclaim live shared nodes or leak abandoned version DAGs without declared retention.
9. Serialization preserves logical versions and sharing only under a versioned acyclic graph format with validated references.

### Common failures

- Copying only the leaf and mutating an old parent to point to it.
- Sharing mutable values or child containers while calling only nodes immutable.
- Recomputing balance/size/hash from old rather than new children.
- Assuming `O(log n)` copied nodes without a height/balance guarantee.
- Treating pointer equality as logical equality or stable entry identity.
- Refcounting parent-to-child links but forgetting retained roots/readers.
- Creating cycles through parent pointers, caches, or confluence and leaking under reference counting.
- Holding one tiny old root that retains a massive shared generation unexpectedly.
- Serializing each version independently and losing sharing/space, or serializing raw pointers and losing portability.
- Using path copying for a high-churn workload without measuring allocator, cache, and reclamation amplification.

### Compact example

Six updates create seven roots including empty. Version 4 contains keys `1,2,4,6`; a branch from version 2 creates version 5 with `2,3,4`, isolated from later keys. Version 6 updates value at key 6 from version 4, copying the root and right path while sharing the whole left subtree. Across nonempty roots there are 17 logical node occurrences but only 13 unique node objects; four objects are referenced from multiple versions. Every old lookup and BST invariant remains unchanged.

### Connections

[DSE-002](002-representation-invariants.md), [DSE-003](003-operation-contracts.md), and [DSE-008](008-iterators-and-traversal-protocols.md) supply invariants, failure, and lifetime contracts. [DSE-031](031-binary-search-trees.md) through [DSE-036](036-order-statistic-trees.md) provide tree/search/balance/augmentation contexts. [DSE-043](043-disjoint-set-forests.md) contrasts destructive path compression with persistence/rollback. [DSE-045](045-compressed-and-radix-tries.md) and [DSE-050](050-choosing-representations-for-large-graphs-and-text.md) use immutable roots and generation publication. The [program roadmap](../ROADMAP.md) continues with persistent balanced trees, HAMTs, vectors, and versioned systems.

## Governing Question

Which updates affect bounded paths, which node/value fields can be immutable, what version branching and identity semantics are required, how are roots/readers retained and reclaimed, and when is path copying preferable to fat nodes, logs, snapshots, or transient mutation?

## Why This Matters

Path copying is the bridge from ephemeral pointer structures to persistent values. It underlies functional maps/sets, compiler syntax and symbol environments, transactional snapshots, undo/history, immutable configuration, copy-on-write indexes, MVCC-like roots, and concurrent read-mostly structures. The mechanism is locally simple: copy ancestors and share untouched children.

The production consequences are not simple. One update allocates several objects and increases reference/GC work. Old roots can retain most of a structure. Values inside nodes can remain mutable and violate snapshot semantics. Balance rotations copy more than the search path. Parent pointers create backward edges. Cached hashes or sizes must describe the new children. Version roots need ownership, publication, persistence, and observability.

Full persistence changes history from a line into a DAG: users may update any old version. Confluent merges can create more sharing and difficult identity/complexity questions. A filesystem or database “copy-on-write” page tree follows similar reasoning at page granularity but adds crashes, reference accounting, checksums, and storage reclamation.

This module begins Level II by treating persistence as an abstract version contract plus a memory/lifecycle system. The code trace proves finite structural sharing; the chapter makes clear what it does not prove.

## Prerequisites and Retrieval

Retrieve abstract/concrete representations and invariants from [DSE-001](001-abstract-data-types-and-concrete-representations.md) and [DSE-002](002-representation-invariants.md), operation/failure contracts from [DSE-003](003-operation-contracts.md), allocation costs from [DSE-004](004-time-space-and-allocation-cost.md), locality from [DSE-006](006-memory-locality-and-cache-behavior.md), generic identity/values from [DSE-007](007-genericity-and-type-constraints.md), iterators/lifetime from [DSE-008](008-iterators-and-traversal-protocols.md), and evidence from [DSE-009](009-property-based-testing-of-data-structures.md) and [DSE-010](010-benchmarking-a-structure-without-misleading-results.md). Retrieve BST invariants from [DSE-031](031-binary-search-trees.md).

## Learning Objectives

After completing this module, you should be able to:

1. distinguish ephemeral, partial, full, and confluent persistence;
2. derive path-copying query, update, allocation, and sharing costs from height and update footprint;
3. implement fully persistent insertion/update without mutating old nodes;
4. extend reconstruction proofs to deletion, rotations, tries, vectors, and augmented nodes;
5. specify logical, version, entry, node, iterator, and value identity;
6. choose reference counting, GC, epochs, arenas, or explicit ownership for shared lifetime;
7. design transient builders with uniqueness/token/freeze guarantees;
8. publish and serialize immutable version DAGs safely;
9. validate old-version isolation, sharing, failure, reclamation, and concurrency; and
10. benchmark allocated/reclaimed/retained nodes and tail behavior rather than only operation time.

## Core Exposition

**Define persistence independently from immutability syntax.** An ephemeral structure exposes one current state; update destroys/replaces it. A persistent structure preserves previous logical versions. An API returning a new object is not truly persistent if it mutates shared internals. Conversely, an implementation may mutate private unshared construction buffers yet publish persistent immutable values.

Partial persistence allows queries on all versions but updates only the newest. Full persistence allows `update(version,x)` for any retained version, creating a branch. Confluent persistence combines two or more versions; naïve confluence can make version ancestry and node sharing exponentially complex. Retroactivity changes past operations and is another model.

State what versions mean. They may be immutable values with no global numbering, monotone commits, branch IDs, content hashes, timestamps, or opaque roots. Equal maps built differently can have different roots. A version root is not an element handle. Persist metadata such as parent version(s), operation/provenance, schema/comparator, generation, and durability state according to needs.

Snapshot semantics include values. If node points to a mutable list/object and later code mutates it, old tree roots observe the change. Require immutable/deeply persistent values, copy on insertion/update, defensive ownership, or explicitly weak shallow snapshots. Hash/comparator keys must not mutate while indexed.

**Copy exactly the affected root path.** In a BST insertion, compare at root. If key is smaller, recursively insert into left and create `Node(old.key,old.value,new_left,old.right)`. If larger, create corresponding right replacement. On equality, create a replacement value node with old children, unless policy returns the same root for an equal unchanged value. Empty insertion creates one leaf.

At each frame, the old node remains reachable and untouched. The sibling subtree is reused by identity. The return value becomes the child of a new parent. The final returned root names the new version. If the search path contains `h` existing nodes, a new-key insertion allocates `h+1`; a value replacement allocates `h` or `h+1` under height-count convention.

Old-version correctness follows directly from immutability. New-version correctness is inductive: the recursive child represents the specified update and preserves its subtree invariant; copied key/value and untouched sibling match old facts; comparison locates update in correct side. Node metadata is recalculated. No other paths change.

If the update discovers a no-op—deleting absent key or setting equal value—returning the original root can maximize sharing. But equality may be expensive or side-effectful, and callers may expect a new version event even with equal content. Separate logical root reuse from version-record creation.

Path copying applies to tries, segment trees, B-trees/pages, radix structures, heap-like trees, and tree-shaped object graphs. The copied frontier is every node whose outgoing pointer/metadata changes, not literally one simple path in all structures. Range updates, rotations, splits/merges, or confluence copy several connected paths/nodes.

**Complexity is height and footprint dependent.** Query uses the normal structure: `O(h)`. A point update takes `O(h)` work and nodes. With AVL/red-black/treap expected/bounded height, this is logarithmic. An unbalanced BST can have `h=n`, copying the whole chain. A B-tree path is shorter but each copied page/node may be large; use copy-on-write pages and account bytes, not node count.

For `v` retained versions, worst physical nodes can be initial nodes plus sum of copied footprints. This is often `O(n+u log n)` for `u` balanced point updates, not `O(vn)`. Yet an update sequence changing disjoint paths may retain much of every generation. The actual live set is union of nodes reachable from roots, readers, caches, iterators, and logs.

Logical size per version and unique physical nodes answer different questions. A monitoring system should report version/root count, total allocations, reclaimed nodes, live unique/estimated bytes, shared fan-in, oldest retained generation, reader age, and retention by owner. Summing version sizes overstates physical memory; allocator heap alone can include garbage/unreachable nodes.

Cache locality can worsen because copied paths allocate at different times/pages and shared subtrees scatter. Immutable packed rebuilds may restore locality. Arena-per-generation is fast but sharing across arenas makes reclamation dependencies. A hybrid periodically compacts/rebuilds versions.

**Deletion and balancing expand the copied region.** BST deletion copies ancestors to target. Removing a leaf/one-child node returns the surviving child, sharing it. For two children, replace with predecessor/successor and persistently delete that key in a subtree; copy both affected paths as required. Never mutate the successor node/value in place.

AVL insertion/deletion recomputes heights/balance and performs persistent rotations. A rotation constructs new nodes for the rearranged local subtrees; untouched outer subtrees share. Red-black functional algorithms rebuild/recolor a bounded local context, but deletion cases are intricate. Validate every old/new version, not only current.

Order-statistic subtree sizes, hashes, min/max, lazy tags, and aggregates must be computed from the replacement children. Sharing an old aggregate with new child is silent corruption. Lazy propagation may conceptually mutate children; persistent implementations push/copy affected nodes or encode immutable lazy transformations.

B-tree copy-on-write may split a full page, allocate siblings/parent, and propagate to root. Crash-safe stores write new pages, then atomically publish a root pointer/manifest with checksums and free-space/reference accounting. In-memory node proof is necessary but not sufficient for storage durability.

**Identity and iterators need precision.** Logical map equality compares entries. Version identity distinguishes history/snapshot even when content equals. Node object identity exposes structural sharing but should normally remain internal. Entry identity may be stable external ID or just key/value equality. A copied ancestor gets a new address although the entry at its key is logically unchanged.

Returning raw node pointers as long-lived handles breaks across path copying, compaction, serialization, and process restart. Use key lookup, stable entry IDs, or version-tagged opaque handles. A handle into one version cannot silently query another unless API defines rebasing.

An iterator pins its root/version. Because nodes are immutable, concurrent new versions do not invalidate its path, provided lifetime is protected. It yields a consistent snapshot. Value objects must also be immutable/pinned. Iterator retention can keep the entire root/subtrees live; expose cancellation/close and track old readers.

Diff between two versions can exploit pointer equality: identical subtree pointers imply equal content under immutability, so skip them. Different pointers may still be logically equal due to independently constructed nodes. Content hashes can skip more but require collision policy and correct recomputation. Diff output is data-dependent and unbounded.

**Memory reclamation is part of correctness.** Tracing GC treats version roots/readers/caches as roots and reclaims unreachable nodes, including cycles, but pause/throughput/heap sizing matter. Reference counting increments each new shared child and root, decrements on release, recursively frees at zero, and gives prompt deterministic reclamation for acyclic graphs. It adds atomic/non-atomic counter traffic and overflow/cycle concerns.

Pure child-directed trees are acyclic, but parent pointers, memo caches, version ancestry, callbacks, or confluence can create cycles. Weak references or tracing/explicit cycle handling may be needed. Recursive destruction of a deep uniquely owned chain can overflow stack; iterative queues or deferred reclamation help.

Epoch/RCU reclamation is useful when versions publish through concurrent roots and readers pin epochs. Retire old roots/nodes after all earlier readers exit. Path-copied nodes can be shared by new roots, so retiring a root is not enough unless nodes use refcounts, tracing, arena dependency, or are allocated per immutable generation with correct reachability scheme.

Arenas reduce allocation overhead. If each version owns only its new nodes and references older arenas, the new arena depends on ancestors; releasing old version cannot free an arena still referenced by descendants. Track arena DAG references or compact. One old node can retain a large arena, causing coarse-grained amplification.

Explicit ownership in languages such as Rust can use atomically/shared reference-counted nodes for threads or non-atomic for single-thread scopes. Copy-on-write APIs may clone only when multiple owners. Type safety prevents some use-after-free but not retention, cycles through interior mutability, logical value mutation, or resource exhaustion.

**Failure semantics are naturally strong when publication is last.** Allocate/copy nodes bottom-up privately. If key/value copy, allocator, comparator, metadata, or rotation fails, release partial new nodes and keep every old root unchanged. Publish/store the new root only after construction/validation. This is a transactional shape.

Comparator exceptions/side effects can still make semantics strange; require pure total comparisons. Reference-count increments can fail only under extreme overflow policies but must be defined. Destructors/value ownership during partial unwind must be safe. Allocation limits should reject before unbounded version creation.

A global version registry update can fail after root construction. Treat root as an uncommitted value and release it, or return it without registry persistence under a named contract. Persistent disk publication adds writes/flushes/root swap; process crash is not handled merely because nodes were immutable in RAM.

Test failure at every allocation/copy/metadata/registry point. Compare all retained old versions and resource accounting. Sanitizers and leak detection complement logical tests.

**Transient mutation amortizes batch updates.** Repeated path-copy updates allocate `O(k log n)` nodes for `k` edits even when successive paths overlap. A transient builder claims unique ownership of a version (or uses an edit token) and mutates newly owned nodes in place, copying shared nodes on first touch. Freeze revokes mutation and publishes immutable root.

Correctness requires exclusive edit token/owner, no immutable reader seeing mutation, token recorded/checked in editable nodes if used, copied-on-write when owner differs, and no operations after freeze. Thread confinement or synchronization is explicit. A transient must not mutate nodes still reachable from its source persistent version.

Batch sorted construction or merge can be better than transients. Build a balanced tree/vector/trie from sorted entries in linear work and publish. Choose based on edit locality, batch size, memory, and API. Transient speedups are measured, not assumed.

Exception/cancellation during transient editing needs rollback or disposal. If the source remains untouched and transient is private, discarding it is safe. Freezing validates invariants and transfers ownership. Persisted formats never expose an editable token.

**Concurrency is read-friendly but publication-sensitive.** Immutable version roots can be shared across threads; queries need no structural locks after safe publication and lifetime pinning. An atomic root swap implements a latest-version pointer. Release/acquire order ensures all new nodes/values initialize before readers traverse.

Two writers loading the same root and publishing updates can lose one update. Use compare-and-swap loop, serialization, transaction conflict detection, or retain branches intentionally. CAS loser releases/retries its private path. Side effects/comparator/value creation must be retry-safe or staged.

Full persistence can expose both writer branches instead of conflict, but application semantics decide whether they may coexist. Merging maps requires a conflict resolver and is not automatically confluent persistence with bounded complexity. Version ancestry and stable logical operations support three-way merge.

ABA on root pointers arises if memory is reclaimed/reused; use reference acquisition protocols, tagged generations, hazard/epochs, or managed references. Atomic refcount acquisition from an unprotected raw pointer is unsafe if another thread can free it first. Lock-free publication is not lock-free allocation/reclamation.

Contention shifts to allocator/refcounts/root CAS/cache. False sharing on reference counters and root metadata can dominate. Benchmarks use read/write mixes, branching, long readers, retries, allocator choices, and memory limits.

**Serialization chooses logical duplication or graph sharing.** Simplest: serialize each desired version as entries and rebuild. It duplicates logical content but decouples format from node layout. A snapshot may store only latest root. A history log stores operations plus checkpoints, requiring deterministic replay and schema/comparator versions.

Graph serialization assigns node IDs, writes immutable node records once, and writes version-root IDs/metadata. Validate IDs/ranges, node type, acyclicity, ordering/balance/metadata, reachability, root list, duplicate keys, values, comparator schema, and sharing constraints. File-relative IDs replace pointers. Bound nodes/roots/depth/edges/value bytes and diagnostics.

Content-addressed nodes hash type/key/value/child hashes and naturally deduplicate equal subtrees, enabling integrity and remote storage. Hash correctness needs canonical encoding, domain separation, collision threat model, and value immutability. Hashing every update adds work. Garbage collection traces retained roots/manifests.

Crash-safe copy-on-write storage writes new nodes/pages, checksums and flushes dependencies, then durably swaps/records new root. Never publish a root before children are durable. Free-space reclamation waits for no live/rollback root and handles crash recovery. Double-write/torn pages and filesystem guarantees are explicit.

Schema/comparator/key encoding changes may make old ordering invalid. Rebuild/migrate to a new generation rather than reinterpret. Version DAG provenance and retention policy govern deletion/legal/audit requirements.

**Security and resource controls follow retention.** Untrusted clients can create many versions/branches or pin readers, retaining memory. Quotas cover roots, update rate, depth/size, live unique/estimated bytes, reader age, diff/output, serialized history, and transient duration. Backpressure/rejection/eviction must respect user data/durability policy.

Pathological insertion order can create linear BST depth and allocate/copy/recursively destroy deeply. Use balanced structures, max-depth checks, iterative algorithms, or rebuild. Comparator/key inputs can be expensive or adversarial. Values can be huge despite few nodes.

Hash/content-address and equality shortcuts have collision/timing concerns. Pointer-sharing patterns can leak history or related versions through side channels/diagnostics. Do not expose raw addresses/reference counts across tenants. Authorization applies per version and diff/history.

Persistent file graphs are hostile inputs: cycles, excessive depth/fanout, duplicate references, out-of-range IDs, forged hashes, and decompression bombs require bounded iterative validation. Authenticate provenance. Encryption at rest does not enforce root authorization in the running process.

Memory exhaustion is a correctness event. Do not continue with a partially registered root or silently evict durable versions. Define retention owners and recoverable deletion. Observability avoids logging sensitive full keys/values/history.

**Evidence must compare every retained version.** An ephemeral ordered map is a reference for each operation history. Generate linear and branching histories; after every update, compare all roots' keys/values, size/order, rank/range/aggregates, and unchanged old-version digests. Keep reference snapshots independent even if expensive.

Validate structure per root: ordering/balance, cached metadata, key/value policy, acyclicity. Validate sharing globally: no new root mutates old nodes; untouched subtrees have expected identity in white-box tests; copied nodes are not incorrectly shared; physical unique count and reference ownership agree. Logical correctness never requires maximum sharing, so sharing tests target implementation promises separately.

Exhaust tiny trees and update branches: empty, insert/update/delete absent/present/root/leaf/one/two-child, rotations, duplicate policies, min/max, sorted/reverse orders, branching from every version, and equal-content independent paths. Compare path-copy versus rebuild and serialize round trips.

Metamorphic properties include old root immutability; update then lookup; unrelated key preservation; branch isolation; update of one branch not changing sibling; diff symmetry/round trip; equivalent operation orders where ADT commutes; releasing a root not breaking descendants; and compaction preserving logical versions.

Fault-inject every node/value/metadata/refcount/registry/file allocation/write/flush/root publication. Concurrent evidence pins readers, races writers/CAS, stalls epochs, releases roots, retries, and checks linearizable latest-pointer semantics or explicit branches. Use memory/thread sanitizers and leak/refcount instrumentation.

Benchmarks vary size/height/balance, key/value size, update/query/delete/diff mix, branch factor/history depth, retained roots/readers, transient batches, allocator/refcount/GC, threads, compaction, and serialization. Measure latency quantiles, allocations/copied nodes/bytes per update, unique/live/reclaimed/retained bytes, sharing ratios, cache/TLB/branches, GC/reclamation pauses, CAS retries, reader age, build/freeze, serialize/recover, and failure cleanup.

The executable below represents immutable BST nodes as tuples and performs full-persistent insertion/value replacement. It builds a linear history, branches from an older version, shares untouched subtrees, counts logical occurrences versus unique objects, and validates every root. It does not prove balance, deletion/rotation, refcount/GC correctness, concurrency, disk durability, transients, security, or production performance.

<!-- bijux-verify: {"id":"path-copying-version-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"versions=7\nv0_keys=\nv4_keys=1,2,4,6\nv5_keys=2,3,4\nv4_value_6=six\nv6_value_6=SIX\nv4_unchanged=True\nbranch_isolated=True\nv4_v6_share_left=True\nlogical_nodes=17\nunique_nodes=13\nshared_objects=4\nall_invariants=True\nevidence=finite_path_copying_version_trace\n","stderr":""}} -->
```python
def node(key, value, left=None, right=None):
    return (key, value, left, right)


def insert(root, key, value):
    if root is None:
        return node(key, value)
    old_key, old_value, left, right = root
    if key < old_key:
        return node(old_key, old_value, insert(left, key, value), right)
    if key > old_key:
        return node(old_key, old_value, left, insert(right, key, value))
    return node(old_key, value, left, right)


def get(root, key):
    while root is not None:
        if key < root[0]:
            root = root[2]
        elif key > root[0]:
            root = root[3]
        else:
            return root[1]
    return None


def keys(root):
    return [] if root is None else keys(root[2]) + [root[0]] + keys(root[3])


def valid(root, low=None, high=None):
    if root is None:
        return True
    key = root[0]
    if low is not None and key <= low:
        return False
    if high is not None and key >= high:
        return False
    return valid(root[2], low, key) and valid(root[3], key, high)


v0 = None
v1 = insert(v0, 4, "four")
v2 = insert(v1, 2, "two")
v3 = insert(v2, 6, "six")
v4 = insert(v3, 1, "one")
v5 = insert(v2, 3, "three")
v6 = insert(v4, 6, "SIX")
versions = [v0, v1, v2, v3, v4, v5, v6]

references = {}
logical_nodes = 0
for root in versions:
    stack = [] if root is None else [root]
    while stack:
        current = stack.pop()
        logical_nodes += 1
        references[id(current)] = references.get(id(current), 0) + 1
        if current[2] is not None:
            stack.append(current[2])
        if current[3] is not None:
            stack.append(current[3])

print(f"versions={len(versions)}")
print("v0_keys=")
print("v4_keys=" + ",".join(map(str, keys(v4))))
print("v5_keys=" + ",".join(map(str, keys(v5))))
print(f"v4_value_6={get(v4, 6)}")
print(f"v6_value_6={get(v6, 6)}")
print(f"v4_unchanged={get(v4, 6) == 'six'}")
print(f"branch_isolated={get(v5, 1) is None and get(v5, 6) is None and get(v4, 3) is None}")
print(f"v4_v6_share_left={v4[2] is v6[2]}")
print(f"logical_nodes={logical_nodes}")
print(f"unique_nodes={len(references)}")
print(f"shared_objects={sum(count > 1 for count in references.values())}")
print(f"all_invariants={all(valid(root) for root in versions)}")
print("evidence=finite_path_copying_version_trace")
```

## Definitions and Notation

Version root `R_v` denotes logical value at version `v`. `Reach(R_v)` is its reachable node set; physical live nodes across retained roots `V` are `union_{v in V} Reach(R_v)`. Logical occurrence count sums `|Reach(R_v)|` and double-counts sharing. An update footprint `F(v,op)` is the nodes newly allocated/replaced; for simple tree point updates `|F|=O(h_v)`.

Node identity is allocation identity; logical node/entry identity is ADT-specific; content equality ignores allocation/history. A version DAG edge records derivation, not a mutable parent pointer in the data structure. A transient edit token proves/claims exclusive mutation authority until freeze.

## Mechanisms, Invariants, or Proof Structure

Old-version proof is nonmutation plus lifetime. New-version proof is induction over reconstruction: recursive changed child is valid, copied fields/untouched child preserve facts, and metadata recomputes. Complexity counts visited/copied nodes and bytes. Global memory proof traces all retained roots/readers/caches and ensures reclamation only outside their reachable union.

Concurrency adds safe root publication/acquisition, writer conflict semantics, and reclamation. Persistence adds graph IDs, schema/comparator, acyclicity, durable child-before-root ordering, and GC from retained roots. Transients add exclusivity and freeze revocation. These layers require independent evidence.

## Alternatives and Trade-Offs

| Technique | Strength | Principal cost/restriction |
|---|---|---|
| full path copying | simple immutable versions/branching | `O(h)` allocations per point update |
| fat nodes | fewer node copies for bounded changes | version lookup/modification capacity complexity |
| node copying with modification boxes | theoretical partial persistence bounds | implementation/version ordering complexity |
| operation log + replay/checkpoint | compact sequential history/audit | replay latency and deterministic migration |
| whole snapshot copy | trivial isolation | `O(n)` update bytes |
| transient builder | batch locality and fewer copies | exclusivity/token/freeze proof |
| copy-on-write pages | storage-friendly coarse paths | page amplification and crash/reference GC |
| ephemeral mutation + locks | direct updates | old versions/snapshots require other mechanism |

Choose from version model, update footprint, balance, batch locality, read/write/history, values, concurrency, persistence, memory/latency, and implementation assurance.

## Failure Modes and Misconceptions

- Immutability of node pointers does not freeze mutable keys/values/caches.
- Persistence level must state which versions can be updated/merged.
- Structural sharing is an optimization/lifetime relation, not logical equality.
- `O(h)` nodes can be `O(n)` in an unbalanced structure or large bytes in page trees.
- Old roots/readers/caches are memory roots and can retain most of the graph.
- Refcounts do not collect cycles and atomic counts do not prove safe root acquisition.
- Returning the same root for a no-op differs from recording a new equal-content version.
- Parent pointers and mutable iterators can destroy tree-only ownership assumptions.
- In-memory copy-on-write does not imply crash durability.
- Finite sharing counts do not prove allocator, reclamation, concurrency, or production efficiency.

## Worked Examples

### Example 1

Inserting 1 into version with root 4 and left child 2 copies nodes 4 and 2 and creates leaf 1; right subtree rooted at 6 is shared unchanged.

### Example 2

Updating value at key 6 copies root 4 and node 6 but shares the entire left subtree. Old version still reads `six`; new reads `SIX`.

### Example 3

Branching from version `{2,4}` to insert 3 creates `{2,3,4}` without inheriting later 1 or 6. Full persistence forms sibling branches rather than overwriting history.

### Example 4

A sorted insertion sequence into an unbalanced persistent BST copies paths of lengths 0,1,2,...; total allocations become quadratic. Persistent AVL/red-black or bulk build avoids that shape.

### Example 5

A persistent AVL rotation constructs replacement nodes for the rotated local pattern and recomputes heights; outer subtrees share. Mutating an old child/height invalidates multiple versions.

### Example 6

An iterator over version 10 remains logically stable while version 11 publishes, but it retains root 10 and shared descendants until closed/released.

### Example 7

Diffing two roots first compares identity. Shared identical subtree skips immediately; different pointers require key/content recursion because independently built equal subtrees may exist.

### Example 8

Reference counting frees a child only when node links and all version roots/readers release it. A parent-pointer cycle prevents zero counts without weak/tracing handling.

### Example 9

A transient from persistent root must copy a shared node before mutation, may mutate nodes tagged with its edit token, and rejects access after freeze. Otherwise the source version changes.

### Example 10

Disk copy-on-write writes/checksums children and new root, flushes them, then commits the root manifest. Publishing root first can make recovery follow missing/torn children.

## Cross-Program Connections

- **Functional programming:** immutable maps/vectors, algebraic APIs, laziness, transients, and equational reasoning use structural sharing.
- **Database/storage engineering:** MVCC roots, copy-on-write B-trees, snapshots, WAL/manifests, page reference GC, and crash ordering generalize the method.
- **Concurrent programming:** immutable readers, atomic roots, writer CAS/conflicts, epochs/refcounts, ABA, and stalled readers define safe publication.
- **Compilers:** persistent ASTs, scopes, type environments, IR rewrites, and speculative branches benefit from old-version isolation/diff.
- **Distributed/version-control systems:** content-addressed DAGs, branches, merges, provenance, and reachability GC add confluent/history semantics.
- **Security/reliability:** version quotas, malicious retention, graph parser validation, authenticated roots, rollback, and fault injection matter.
- **Performance engineering:** allocator/refcount/GC, copied bytes, cache locality, transient batches, compaction, and retention determine actual cost.

## References

1. [James Driscoll, Neil Sarnak, Daniel Sleator, and Robert Tarjan, *Making Data Structures Persistent*](https://www.cs.cmu.edu/~sleator/papers/making-data-structures-persistent.pdf).
2. [Chris Okasaki, *Purely Functional Data Structures* thesis](https://www.cs.cmu.edu/~rwh/students/okasaki.pdf).
3. [Chris Okasaki, *Red-Black Trees in a Functional Setting*](https://www.cs.tufts.edu/~nr/cs257/archive/chris-okasaki/redblack99.pdf).
4. [Phil Bagwell, *Ideal Hash Trees*](https://lampwww.epfl.ch/papers/idealhashtrees.pdf).
5. [Rust `im` crate documentation](https://docs.rs/im/latest/im/).
6. [Clojure, data structures reference](https://clojure.org/reference/data_structures).
7. [Clojure, maintained `PersistentVector` implementation](https://github.com/clojure/clojure/blob/master/src/jvm/clojure/lang/PersistentVector.java).
8. [Scala, concrete immutable collection classes](https://docs.scala-lang.org/overviews/collections-2.13/concrete-immutable-collection-classes.html).

## Exercises

### Exercise 1

Given a balanced BST version with keys 1 through 15, describe exact nodes copied/shared when inserting 0, replacing value at 14, and deleting leaf 9. Give asymptotic and concrete node counts for one valid shape.

### Exercise 2

Prove path-copy insertion preserves every old version and yields a valid new BST with `O(h)` work/nodes. State assumptions on comparator, keys, values, allocation, and metadata.

### Exercise 3

Design a memory-lifetime system for fully persistent trees with threads, branches, iterators, caches, and occasional parent links. Compare tracing GC, refcounts, epochs, and arena generations.

### Exercise 4

Specify a transient batch-update API that begins from a persistent map, supports inserts/deletes, freezes, and rejects misuse. Include failure, thread, sharing, iterator, and validation rules.

### Exercise 5

Design a persistent on-disk node DAG with content hashes and multiple version roots. Include canonical encoding, write/commit order, validation, crash recovery, root retention/GC, migration, authorization, and evidence.

## Answers to the Exercises

### Answer 1

Choose the perfect BST rooted 8, children 4/12, then 2/6/10/14, then odd leaves. Inserting 0 searches 8,4,2,1,null: create 0 and copies 1,2,4,8—five new nodes; every sibling subtree (3,6-side,12-side) shares. Replacing value at 14 searches 8,12,14 and copies those three nodes, sharing 14's children 13/15 and all off-path subtrees. Deleting leaf 9 searches 8,12,10,9 and returns null at 9 while copying 10,12,8—three new nodes if the deleted leaf is not copied; other subtrees share. Each operation is `O(h)` work/bytes in unit-size nodes, here paths bounded by four existing levels.

### Answer 2

Induct on the search recursion. Empty insertion returns one valid singleton and changes no old node. At old node `r`, pure total comparison chooses exactly one side. By induction recursive result is the old child map with the update and old child remains unchanged. Construct a fresh node copying `r`'s key/value, untouched sibling pointer, and new changed child; ordering follows comparison plus child invariants, and recomputed metadata follows children. Equality constructs a fresh value node or returns unchanged under policy. No published old node/value is mutated, so every old root preserves reachability/content. One node is visited/copied per height level plus optional leaf, giving `O(h)` time/nodes. Assumptions: immutable stable keys/values (or deep ownership), pure comparator, allocation/copy failures unwind private nodes, and every augmentation recomputes correctly.

### Answer 3

Tracing GC handles arbitrary cycles/parent links and treats roots, iterators, caches, and thread locals as roots; tune heap/pauses and expose retention. Per-node refcounts give prompt tree/DAG reclamation but add counter traffic/overflow and leak parent/cache cycles unless weak/broken/traced; safe concurrent root acquisition needs a protected protocol. Epochs make readers cheap and delay retired-root reclamation, but shared descendants still need refcounts/tracing or generation ownership; stalled readers retain memory. Arena generations make allocation/destruction fast, but cross-generation sharing forms dependencies and one node retains an arena; refcount arenas or compact. A practical design might use immutable nodes under tracing GC, or atomic node refcounts plus weak parent links and epoch-protected latest-root acquisition, with quotas/reader-age telemetry and iterative destruction.

### Answer 4

`transient(root)` returns an exclusive thread-confined builder with fresh unforgeable edit token and pins source. On first write to a node, mutate only if node is privately owned/tagged by this token; otherwise copy it and its needed path. Inserts/deletes maintain or temporarily track invariants under documented internal states. No persistent iterator/root can observe editable nodes; transient iterators are invalidated by mutation. `freeze()` completes/rebalances/validates, clears/revokes edit authority, publishes an immutable root, and permanently invalidates builder/mutators; repeated freeze/use raises error. Cancellation/allocation/comparator/value failure discards the private builder and leaves source untouched. Thread transfer is forbidden or explicit synchronized ownership handoff. Tests branch source concurrently, force every shared-node boundary/failure, and compare source/result/reference plus leak/alias checks.

### Answer 5

Canonically encode node type, comparator/schema version, key/value and child hashes with length prefixes/domain separation; hash bytes to content ID. Write each new child/node object once, verify hash, fsync object storage as required, then write/checksum a version record naming root and parent/provenance; durably publish a root manifest only after dependencies. Loader authenticates manifest/provenance, bounds object count/bytes/depth, verifies hashes/canonical encodings, detects cycles, validates ordering/balance/metadata and authorization. Recovery selects last complete committed manifest and ignores/quarantines incomplete objects. GC traces all retained/reader/rollback/legal roots and deletes unmarked objects only after grace/recheck; quotas stop hostile roots/history. Schema/comparator changes rebuild new DAG rather than reinterpret. Evidence includes logical reference histories, hash tampering/collision-policy tests, every crash boundary, concurrent readers, GC safety, migration/shadow diff, restore drills, and no external review claim without named records.
