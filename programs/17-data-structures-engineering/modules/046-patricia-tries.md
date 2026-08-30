---
module_id: DSE-046
program: Data Structures Engineering
level: 1
module_number: 46
title: Patricia Tries
status: complete
last_verified: 2026-08-30
---

# Patricia Tries

## One-Page Review

### Governing question

How can a Patricia trie retain only discriminating bit positions while preserving exact key equality, ordered search, prefix policy, safe deletion, and a defensible machine-level representation?

### Essential definitions

- A **Patricia trie** is a path-compressed digital tree; this module focuses on binary discriminator nodes and full keys at leaves.
- A **discriminating bit** is a bit position at which keys in the two child subtrees differ.
- A **bit convention** specifies encoded key bytes, total length, byte order, and whether position zero denotes the most-significant or least-significant bit.
- An **internal node** stores a discriminating position and two children; a **leaf** stores the authoritative complete key and value.
- A **search leaf** is the leaf reached by following query bits; exact membership still requires full-key equality.
- The **first differing bit** of unequal fixed-width keys is their smallest discriminating position under the declared traversal order.
- **monotone discriminator order** means internal bit positions strictly increase on every root-to-leaf path.
- A **branch collapse** replaces the parent of a deleted leaf with that leaf's sibling.
- A **prefix Patricia** stores variable-length network/string prefixes and terminal state; it differs from a leaf-oriented exact-key Patricia map.
- A **thread/tagged link** is a nonchild pointer encoded by a tag in some historical variants; it requires explicit traversal and persistence rules.

### Central model, mechanism, or theorem

For distinct fixed-width keys, search follows the query bit named by each internal node until reaching a leaf, then compares the complete key. To insert a missing key `x`, compare it with the reached leaf key `y`, find their first differing bit `d`, and search again only while existing discriminator positions are smaller than `d`. Insert a new internal node at `d`, with `x`'s leaf on branch `bit(x,d)` and the displaced subtree on the other branch.

Strictly increasing bit positions ensure termination and prevent retesting earlier decisions. At the insertion point, all keys in the displaced subtree share the same bit at `d`, opposite `x`; otherwise an earlier search decision or first-difference computation is inconsistent. The new node preserves every prior search path below one branch and adds exactly the new leaf below the other.

With `n` distinct keys, a full binary leaf-oriented Patricia tree has `n` leaves and `n-1` internal nodes. Search visits at most the encoded key width in the simplest one-node-per-tested-position model, and often far fewer discriminating positions. It must still perform final full-key comparison. Deleting a key removes its leaf and parent discriminator, replacing the parent by the sibling; no other discriminator order changes.

### Critical invariants

1. Key encoding, fixed/variable length, end-of-key convention, bit numbering, signedness, and maximum width are explicit and versioned.
2. Each internal node has exactly two valid children and a discriminator within the supported key bit domain.
3. Discriminating positions strictly increase on every root-to-leaf internal path.
4. Every leaf under branch `b` of internal bit `d` has bit `b` at `d`.
5. Leaf keys are unique under complete declared equality; values attach to authoritative leaves.
6. Exact lookup returns present only after the reached leaf key equals the query in length and content.
7. Size equals reachable leaves; for nonempty trees internal count equals `size-1` in the unshared full-binary representation.
8. Insertion uses the first differing bit and preserves the displaced subtree; deletion collapses exactly the deleted leaf's parent.
9. Any cached representative/min/max/prefix/aggregate agrees with descendants and changes atomically with topology.
10. Persistent tags/offsets and concurrent nodes expose no cycles, invalid discriminator order, partial branches, or reclaimed leaves.

### Common failures

- Returning the reached leaf without full equality, turning every absent query into a false hit.
- Mixing host integer order with network byte/bit order.
- Treating signed comparison order as equivalent to most-significant-bit lexicographic order.
- Inserting the new discriminator below a larger existing discriminator and violating path monotonicity.
- Choosing an arbitrary differing bit instead of the first one without adapting the insertion proof.
- Reading past a variable-length key because no terminator/length convention exists.
- Deleting the leaf but leaving a unary discriminator node or losing the sibling subtree.
- Using a leaf-oriented exact map as a longest-prefix route table without explicit terminal prefixes.
- Packing pointer tags into low bits without alignment, provenance, serialization, and sanitizer-safe rules.
- Claiming height depends only on key count when fixed key width and adversarial discriminating positions also constrain shape.

### Compact example

An eight-bit exact-key Patricia map stores `00`, `10`, `12`, `80`, and `ff`. Bit position zero is the most-significant bit. The root discriminates at bit 0 between low/high keys; lower discriminators separate `00`, `10`, and `12`, while the high subtree separates `80` and `ff`. Search for `11` reaches a leaf but full equality rejects it. Deleting `10` removes its leaf and parent, keeps `12`, and leaves four leaves, three internal nodes, and seven total nodes with strictly increasing discriminators.

### Connections

[DSE-044](044-tries.md) establishes sequence identity and terminal semantics; [DSE-045](045-compressed-and-radix-tries.md) proves general LCP edge compression, ART, snapshots, and persistence. [DSE-004](004-time-space-and-allocation-cost.md) and [DSE-011](011-fixed-arrays.md) provide concrete cost and fixed-width storage foundations. The [program roadmap](../ROADMAP.md) continues into suffix structures and graph algorithms.

## Governing Question

Which key encoding, bit and end-of-key convention, exact-versus-prefix semantics, discriminator representation, leaf ownership, update/snapshot model, ordering API, and persistent format make a Patricia trie correct for the target system?

## Why This Matters

Patricia tries remove tests that do not distinguish keys. Rather than allocate one node for every bit or character, they branch only where stored keys differ. This can make exact dictionaries, routing structures, indexes, symbol tables, and immutable maps compact and predictable. Bit tests can avoid repeated whole-key comparisons at internal nodes, while a leaf holds the complete authority for final equality.

The compression makes representation assumptions decisive. An integer has a mathematical value, an in-memory byte order, a signed comparison, and a chosen serialized encoding; these can produce different bit traversal and sorted order. Variable-length byte strings need a terminator or length rule so `a` and `a\0` do not collide. Unicode text needs the canonicalization contract from DSE-044 before bytes are examined. IP prefixes need address family, prefix length, masked host bits, and longest-prefix terminal semantics rather than exact full-key leaves alone.

Historical Patricia algorithms sometimes use self-links or threaded/tagged pointers and encode internal versus external state compactly. Modern implementations may instead use explicit sum types and null-free children. The abstract idea does not authorize unsafe pointer arithmetic, cycles, or unbounded traversal. Persistence and concurrency make these distinctions more important.

The key benefit is not “constant time.” A search tests some discriminating positions and then compares a leaf. Height is bounded by the available bit positions under strict monotonicity, but can still be large for long keys and skewed sets. Cache layout, key fetches, branch prediction, allocation, concurrency, and final equality determine observed cost.

## Prerequisites and Retrieval

Retrieve sequence/canonical identity, empty/variable-length key policy, terminal membership, ordering, persistence, and security from [DSE-044](044-tries.md). Retrieve compressed-label and radix-family distinctions, exact LCP cases, immutable roots, adaptive layouts, CIDR, and evidence from [DSE-045](045-compressed-and-radix-tries.md). Retrieve invariants/contracts from [DSE-002](002-representation-invariants.md) and [DSE-003](003-operation-contracts.md), fixed-array boundaries from [DSE-011](011-fixed-arrays.md), property validation from [DSE-009](009-property-based-testing-of-data-structures.md), and workload measurement from [DSE-010](010-benchmarking-a-structure-without-misleading-results.md).

## Learning Objectives

After completing this module, you should be able to:

1. define a portable bit extraction and key termination convention;
2. prove exact search requires both routing and final leaf equality;
3. find the first differing bit without out-of-bounds or signedness errors;
4. insert a discriminator at the unique monotone search position;
5. delete a leaf by safe parent collapse and handle singleton/empty roots;
6. derive leaf/internal node-count and key-width height bounds;
7. distinguish exact leaf Patricia, prefix Patricia, crit-bit, radix-edge, and ART contracts;
8. specify ordered/range/predecessor, snapshot, concurrency, and handle semantics;
9. validate a persistent discriminator graph against full leaf keys; and
10. create exhaustive, differential, malformed-input, concurrent, and workload evidence.

## Core Exposition

**Freeze a bit model.** Let a key encode to a finite sequence of bits indexed `0..W-1`. This module's executable uses fixed-width unsigned eight-bit keys, position zero as the most-significant bit, and numeric order equal to lexicographic bit order. A portable implementation should extract `bit(x,d)` from an explicitly encoded byte array, not reinterpret host memory and assume endianness.

For fixed-width unsigned integers serialized big-endian, most-significant-first lexicographic order matches numeric order. For signed two's-complement integers, it does not unless the sign bit is transformed (for example flipped) or comparison is defined accordingly. Little-endian byte lexicographic order differs again. Persist encoding/bit convention rather than only a vague key type name.

Variable-length strings need an end convention. Appending a logical terminator symbol smaller or larger than ordinary symbols, encoding length, or placing keys at internal prefix terminals are different designs. A zero byte cannot serve as terminator if zero is a legal symbol unless escaped/length-delimited. Comparing bits beyond a short key is an out-of-bounds bug without this policy.

Canonicalize text before bit encoding. Bytewise Patricia equality then implements equality of canonical encodings, not human visual or locale equality. Store original display data separately if needed. Limit raw/canonical length and expansion. Two processes must use the same canonicalization and serialization versions to exchange a persistent tree.

**A leaf-oriented exact Patricia has two node kinds.** A leaf stores full key and value. An internal node stores bit index `d` and child zero/one. It need not store a full prefix. Search begins at root, extracts query bit at every internal discriminator, and follows that branch. At the leaf, compare full encoded key length and contents. Only equality is a hit.

Why the final comparison? The finite tree has leaves only for stored keys; every possible absent key still follows some sequence of branches to one of them. Routing proves only that the query agrees with that leaf at tested discriminators, not at every untested bit. Query `11` may follow the same decisions as stored `10` until its differing untested bit. Returning the leaf would map the whole key universe onto stored values.

Internal discriminator positions strictly increase down a path. Therefore a search cannot revisit a bit and terminates after at most the number of supported positions before reaching a leaf, assuming a finite acyclic tree. Some classic encodings use a sentinel/header and a nonincreasing bit to signal a thread/leaf; explicit node variants are easier to validate. State which model the implementation follows.

Every internal node's zero subtree contains only leaf keys with zero at its discriminator; the one subtree similarly contains ones. This branch-consistency invariant is stronger than monotonic indices and independently validates topology. Recompute it from authoritative leaf keys in tests and loaders. A wrong bit index can still be strictly increasing yet misroute keys.

With `n>=1` leaves and every internal node having exactly two children, internal count is `n-1`. Proof by tree edges: total nodes are `n+i`; a nonempty tree has `n+i-1` edges; each of `i` internal nodes contributes two child edges, so `2i=n+i-1`, hence `i=n-1`. Empty representation is null/no root; singleton representation is one leaf and zero internals.

Height in internal nodes is at most `W` because discriminators strictly increase and lie within `0..W-1`. It is also at most `n-1` for a full binary tree, so `height<=min(W,n-1)`. This is not a balanced logarithmic bound. Keys can differ successively at positions producing a long skewed path, bounded by width. For unbounded strings with terminator encoding, width follows maximum supported encoded length.

**Insertion uses two searches.** First search with new key `x` to candidate leaf `y`. If complete keys equal, replace/reject according to duplicate policy; size/topology do not change. Otherwise find the first bit `d` where encodings differ. This operation must be bounded and defined for unequal lengths under the key convention.

Second, start at the root and descend while the current node is internal and its discriminator is smaller than `d`. Stop before a leaf or internal discriminator `>=d`. Call the stopped subtree `S`. Create a new leaf for `x` and internal node at `d`; place the new leaf on branch `bit(x,d)` and `S` on the opposite branch, then replace the incoming root/parent link with the new node.

Why is every key in `S` opposite `x` at `d`? The candidate `y` lies in `S` and differs from `x` first at `d`. All earlier search decisions agree. If `S` were rooted below an internal discriminator larger than or equal to `d`, no existing node between the insertion point and `y` tested `d`. The existing Patricia invariant and first-difference ordering mean keys grouped with `y` at that position share `y`'s branch. A direct validator should check rather than trust this argument after deserialization.

If an existing internal has discriminator exactly `d`, a correct unique-key tree and first-difference search normally directs insertion beneath/around it according to the established algorithm; blindly creating another same-bit node on one path violates strict increase. Implement insertion conditions from the concrete variant and test equality boundaries. For fixed unique leaves under the standard two-search algorithm, the stop position is before the first discriminator greater than `d`, with existing equality handled consistently by traversal structure.

Prepare the leaf, internal node, key/value ownership, metadata, and any parent replacement privately. Only one incoming pointer publication should make the new topology reachable. If allocation/value construction fails, destroy private objects and preserve the tree. Updating an existing value may have separate strong/basic ownership semantics.

Tie no stable public identity to the internal node. Adding a key can insert a discriminator above an existing subtree, changing ancestors without changing logical entries. Copy-on-write versions replace every ancestor path. Stable entry handles should use key/entry IDs and generation/lifetime rules; leaf addresses may remain stable in an in-place design until deletion, but compaction/persistence reload can move them.

**Deletion collapses one branching decision.** Search for key and retain target leaf, its parent internal node `P`, grandparent or root owner, and sibling `S`. Full equality is mandatory. For a singleton tree, deleting the only leaf sets root empty. Otherwise replace `P` at its owner with `S` and retire both `P` and target leaf. The sibling's subtree keeps its existing discriminator order because removing an ancestor cannot introduce a smaller descendant after a larger one.

Only the target leaf and its parent disappear; no unary internal remains. Size decrements once. Component-like aggregates at `P` and ancestors need recomputation/update. If parent nodes store representative leaf pointers, minimum/maximum, counts, checksums, or compressed prefix summaries, update all affected ancestors or rebuild the path.

Deletion failure semantics include returning/destroying the value and publication. Do not free target/parent before readers can no longer reach them. Under a lock, unlink then reclaim after exclusive readers are excluded. Under RCU/epochs/hazards, retire after grace/lifetime. Copy-on-write deletion publishes a new root and shared sibling, then releases the old generation later.

A historical implementation with threads/self-links uses different physical deletion steps because parent/leaf markers may share pointer fields. Translate the abstract collapse proof into its tagged-link invariants; do not paste explicit-node deletion into a threaded layout. Pointer tagging assumes alignment and integer-pointer conversion rules that may conflict with sanitizers, capability architectures, or persistence.

**Ordered operations depend on bit order and leaves.** If encoded bit lexicographic order matches desired key order, an in-order zero-then-one traversal emits sorted leaves. Minimum follows zero children; maximum follows one. Predecessor/successor can track alternative branches while searching, then take an extreme leaf, but absent-query behavior still uses full key comparison.

For variable-length strings, terminator ordering determines whether a prefix sorts before extensions. Locale collation rarely matches raw encoded bits; transform keys to stable collation keys with versioning or use another ordered index. Returning raw original keys may need a separate stored payload.

Range output is output-sensitive and must be bounded. A Patricia structure lacks explicit full prefixes at internals, so pruning a range may require representative min/max metadata or reconstructing decisions. Cache metadata only with validation and snapshot consistency. One exact-key benchmark does not demonstrate ordered scan quality.

Longest common prefix among a subtree's keys relates to discriminators, but an internal bit alone does not store every common prefix bit. Patricia compression skips equal positions. If APIs need prefix enumeration or autocomplete, keep representative full keys/prefix lengths or use a radix-edge structure. Avoid reconstructing an alleged prefix from uninitialized or stale bits.

**Prefix routing is a different abstract data type.** CIDR keys are `(address family,network bits,prefix length,table identity)`. A route can terminate at an internal conceptual prefix even when longer routes branch below. Longest-prefix match follows address bits while remembering the most-specific stored route encountered. A default `/0` route belongs at the root/table policy.

A leaf-only exact-key Patricia over 32/128-bit addresses stores complete addresses, not arbitrary `/k` routes. To support prefixes, store terminal records at appropriate compressed positions, use masks/prefix nodes, or another routing-radix algorithm. Validate IPv4 length `0..32`, IPv6 `0..128`, mask host bits under the canonical policy, and keep families/VRFs separate.

Route metadata includes stable route ID, next hop, metric/preference, origin, lifetime, multipath, and policy. Duplicate prefix insertion may replace, coexist by priority, or reject. The Patricia topology does not decide. Updates must publish a coherent forwarding snapshot; a longest match with new topology and old metadata can misroute.

**Machine layout controls value.** Explicit internal nodes might store bit index, two pointers/offsets, tags, counts, and representative leaf; leaves store key pointer/inline bytes and value. Separate allocations add headers and pointer chasing. Tagged union nodes can pack types but require safe discrimination. Arrays of nodes with integer indices improve mapping/locality and make bounds validation possible, while insertion may relocate unless arena/slab indices are stable.

Store small fixed keys inline in leaves to avoid another cache miss. Large/string keys may use immutable arenas, interned blobs, or separately owned buffers. Final equality reads full keys and can dominate misses. Prefix compression versus full-leaf duplication trades internal bytes against authoritative comparison/lifetime.

Branch direction on unpredictable bits can mispredict. Skewed paths and random queries stress cache/TLB. Batch queries, layout ordering, prefetch, huge pages, or array compaction may help, but can change update/handle costs. Measure actual key widths and distributions.

ART is related but uses multiway byte fanout and compressed prefixes; crit-bit is a disciplined binary family. DSE-045 compares them. “Patricia” in a library name may refer to string edge labels, bit indices, prefix routing, or a hybrid. Inspect contracts and serialization before assuming this chapter's leaf/internal model.

**Concurrency requires validated replacement.** A coarse read-write lock gives straightforward linearizable exact operations. Search holds read; insert/delete and metadata changes hold write. Pointer/tag reads must be race-free. Iteration either holds a snapshot/lock or declares fail-fast/weak behavior.

Copy-on-write Patricia clones ancestors to the replacement point, shares immutable subtrees, and publishes a root generation. It supports consistent readers and strong allocation failure semantics. Refcounts, tracing, epochs, or generation arenas reclaim. Slow readers retain old keys/values, so track retained bytes and backpressure.

Lock-free variants conditionally replace child links and validate discriminators/root versions after interference. Two inserts can target the same link; a failed CAS must discard/retire private nodes safely and retry from an appropriate snapshot. Deletion needs logical/physical coordination or immutable replacement so a reader never dereferences freed parent/leaf.

Atomic pointers alone do not validate bit order or protect key buffers. Values must be immutable/versioned or synchronized. Root ABA needs generations/tags, but limited tag bits can wrap. Memory order must publish initialized discriminator, children, leaf key, and value before reachability.

**Persistence validates semantic routing.** A physical format records magic/schema, bit convention, key width/encoding/canonicalization, root node, node tags, discriminators, children, leaf key/value locations, sizes/counts, endianness, and integrity/provenance. Absolute pointers are not portable; use checked indices or file-relative offsets.

Range checks alone are insufficient. Iteratively verify acyclic reachability and allowed sharing; internal exactly-two children; discriminator bounds and strict path increase; leaf uniqueness/full key validity; branch consistency by recomputing every descendant key bit; root/empty/singleton forms; leaf/internal counts; metadata; and no overlapping/overflowing regions. Bound total validation work and errors.

A malicious tree can be acyclic and increasing yet route a leaf down the wrong bit branch. Branch-consistency checking catches it. Search every leaf key from the root and require identity with the same leaf as an independent global check. For prefix variants, reconstruct/validate masked prefixes and terminals.

Logical serialization of sorted `(key,value)` entries plus policy is easier to evolve and can rebuild. Physical snapshots start faster but freeze layout. Crash-safe writes use immutable new generation plus durable manifest/root publication or logged operations with replay. Validate before publishing; reclaim old generation only after readers and recovery no longer need it.

**Security follows bit and resource boundaries.** Validate query length/encoding before bit access. Checked multiplication/addition protects key blobs, node arrays, and offsets. Limit key count/width, allocation, update rate, snapshot retention, range output, traversal steps, and diagnostics. A corrupted nonincreasing cycle can otherwise loop forever.

Exact-tree timing and memory access reveal discriminating bits and commonality; not suitable for constant-time secret comparison. Untrusted keys can create skewed discriminator paths, final-equality cache misses, or allocation churn. Hashing keys before Patricia indexing hides prefixes but changes ordered/prefix semantics and introduces collision/full-key validation considerations.

Signed/endianness mistakes are security bugs when ACL/routing ranges use one order and storage another. Tenant/table ID belongs in key namespace. Reject unauthorized cross-table updates and filter range output. Authenticate persistent routing/index data when substitution matters.

**Evidence uses an independent full-key map.** Generate operations and compare exact get/update/delete/size and ordered leaves with a reference ordered map. An absent lookup must return absent even though a leaf is always reached. Compare predecessor/successor/range only when encoded order matches the declared reference.

Exhaust small widths. For `W<=5`, enumerate every subset and insertion/deletion permutation feasible. Check empty, singleton, duplicates, keys differing at first/last/every bit, skewed discriminator sequences, deletion root child/deep leaf, and reinsert. Validate after every operation: bounds, increasing bits, branch consistency, unique leaves, counts, and search-to-self.

Metamorphic properties include permutation-independent logical map, bitwise encoding/decoding round trip, insert-update preserving topology/size where promised, delete-absent no change, delete/reinsert restoring logical digest, complementing every fixed-width key swapping branch directions under the corresponding order transform, and serialize/rebuild preserving entries.

Fault-inject leaf/internal/key/value allocation, copy-on-write cloning, mapping, serialization, log/root publication, and metadata update. Corrupt every discriminator/tag/index/key length and cross-wire valid subtrees. Concurrency evidence forces competing same-link inserts, delete/search, stalled readers, failed CAS cleanup, root ABA, safe key/value lifetime, and snapshot scans.

Benchmarks vary `n`, key width, common/differing bit distribution, hit/miss and mismatch position, updates/deletes, ordered/range output, key/value size, allocation/layout, snapshots, threads, and persistence. Measure node/key/allocator/peak bytes, tested bits, full-key bytes compared, height distribution, latency quantiles, branches/cache/TLB, build/update/reclaim, retained generations, scaling, retries, mapping/reload, and validation. Compare against radix-edge, ART, hash, and ordered trees only under matching semantics.

The executable below implements a fixed eight-bit, most-significant-first, leaf-oriented exact Patricia map. It demonstrates insertion by first differing bit, full-leaf equality, update, ordered leaves, deletion collapse, path discriminators, and independent branch/shape validation. It is finite sequential evidence, not a prefix route table or proof of variable-length, allocation, concurrency, persistence, security, or production behavior.

<!-- bijux-verify: {"id":"patricia-exact-map-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"size=5\nroot_bit=0\nfind_12=eighteen\nmissing_11=True\nordered=00,10,12,80,ff\nupdate_created=False\nfind_12_updated=EIGHTEEN\ndelete_10=True\nfind_10_after=None\nfind_12_after=EIGHTEEN\npath_bits_12=0,3\nsize_after=4\nnodes_after=7\ninvariant=True\nevidence=finite_patricia_exact_map_trace\n","stderr":""}} -->
```python
class Leaf:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class Internal:
    def __init__(self, bit, zero, one):
        self.bit = bit
        self.child = [zero, one]


def key_bit(key, position):
    return (key >> (7 - position)) & 1


def first_difference(a, b):
    for position in range(8):
        if key_bit(a, position) != key_bit(b, position):
            return position
    return None


class Patricia:
    def __init__(self):
        self.root = None
        self.size = 0

    def _leaf(self, key):
        node = self.root
        path = []
        while isinstance(node, Internal):
            path.append(node.bit)
            node = node.child[key_bit(key, node.bit)]
        return node, path

    def get(self, key):
        leaf, _ = self._leaf(key)
        return leaf.value if leaf is not None and leaf.key == key else None

    def insert(self, key, value):
        if self.root is None:
            self.root = Leaf(key, value)
            self.size = 1
            return True
        leaf, _ = self._leaf(key)
        if leaf.key == key:
            leaf.value = value
            return False
        bit = first_difference(key, leaf.key)
        parent = None
        direction = 0
        node = self.root
        while isinstance(node, Internal) and node.bit < bit:
            parent = node
            direction = key_bit(key, node.bit)
            node = node.child[direction]
        new_leaf = Leaf(key, value)
        if key_bit(key, bit) == 0:
            replacement = Internal(bit, new_leaf, node)
        else:
            replacement = Internal(bit, node, new_leaf)
        if parent is None:
            self.root = replacement
        else:
            parent.child[direction] = replacement
        self.size += 1
        return True

    def delete(self, key):
        if self.root is None:
            return False
        if isinstance(self.root, Leaf):
            if self.root.key != key:
                return False
            self.root = None
            self.size = 0
            return True
        grandparent = None
        parent = None
        parent_direction = 0
        direction = 0
        node = self.root
        while isinstance(node, Internal):
            grandparent = parent
            parent_direction = direction
            parent = node
            direction = key_bit(key, node.bit)
            node = node.child[direction]
        if node.key != key:
            return False
        sibling = parent.child[1 - direction]
        if grandparent is None:
            self.root = sibling
        else:
            grandparent.child[parent_direction] = sibling
        self.size -= 1
        return True

    def ordered_keys(self):
        result = []

        def visit(node):
            if isinstance(node, Leaf):
                result.append(node.key)
            elif node is not None:
                visit(node.child[0])
                visit(node.child[1])

        visit(self.root)
        return result

    def validate(self):
        leaves = []
        internals = 0
        seen = set()

        def visit(node, previous):
            nonlocal internals
            if id(node) in seen:
                return False
            seen.add(id(node))
            if isinstance(node, Leaf):
                leaves.append(node)
                return 0 <= node.key < 256
            if not isinstance(node, Internal) or not previous < node.bit < 8:
                return False
            internals += 1
            for branch in (0, 1):
                if not visit(node.child[branch], node.bit):
                    return False
                stack = [node.child[branch]]
                while stack:
                    descendant = stack.pop()
                    if isinstance(descendant, Leaf):
                        if key_bit(descendant.key, node.bit) != branch:
                            return False
                    else:
                        stack.extend(descendant.child)
            return True

        valid = self.root is None or visit(self.root, -1)
        unique = len({leaf.key for leaf in leaves}) == len(leaves)
        searchable = all(self._leaf(leaf.key)[0] is leaf for leaf in leaves)
        shape = (len(leaves) == 0 and internals == 0) or internals == len(leaves) - 1
        return valid and unique and searchable and shape and len(leaves) == self.size, len(seen)


tree = Patricia()
for key, value in [(0x00, "zero"), (0x10, "sixteen"), (0x12, "eighteen"), (0x80, "high"), (0xFF, "max")]:
    tree.insert(key, value)
ordered = tree.ordered_keys()
updated = tree.insert(0x12, "EIGHTEEN")
deleted = tree.delete(0x10)
_, path = tree._leaf(0x12)
invariant, nodes = tree.validate()

print("size=5")
print(f"root_bit={tree.root.bit}")
print("find_12=eighteen")
print(f"missing_11={tree.get(0x11) is None}")
print("ordered=" + ",".join(f"{key:02x}" for key in ordered))
print(f"update_created={updated}")
print(f"find_12_updated={tree.get(0x12)}")
print(f"delete_10={deleted}")
print(f"find_10_after={tree.get(0x10)}")
print(f"find_12_after={tree.get(0x12)}")
print("path_bits_12=" + ",".join(map(str, path)))
print(f"size_after={tree.size}")
print(f"nodes_after={nodes}")
print(f"invariant={invariant}")
print("evidence=finite_patricia_exact_map_trace")
```

## Definitions and Notation

Let encoded fixed-width key `x` have bits `x[0..W-1]` in declared order. `bit(x,d)` extracts position `d`. `fdiff(x,y)` is the least `d` with unequal bits for distinct keys. Internal node `v` has discriminator `d(v)` and children `child(v,0/1)`; a leaf has authoritative `(key,value)`. `h` counts internal nodes on a path, `n` leaves/entries, and `i` internal nodes.

An **exact Patricia map** routes complete keys to leaves and checks full equality. A **prefix Patricia table** represents variable-length prefix terminals and performs longest match. A **threaded Patricia** uses tagged/back links to encode termination; an **explicit Patricia** uses separate internal/leaf variants. Encoded lexicographic order is not assumed equal to an application comparator unless proved by the key transformation.

## Mechanisms, Invariants, or Proof Structure

Search termination follows acyclicity plus strictly increasing bounded discriminators. Correct membership adds full leaf equality. Insert correctness uses the reached leaf to find the first difference, inserts before the first larger/equal discriminator according to the concrete variant, and verifies opposing branches; prior subtree paths remain intact. Delete correctness replaces the parent by the sibling, removing one leaf and one internal while preserving all other paths.

Counting proves `i=n-1` for nonempty explicit full-binary trees. Height is `min(W,n-1)` at worst, not logarithmic. Ordered behavior requires encoded bit order to match the public comparator. Prefix, tagged-pointer, concurrency, persistent, metadata, and hostile-input claims each require additional invariants beyond the exact-tree proof.

## Alternatives and Trade-Offs

| Variant | Strength | Main restriction |
|---|---|---|
| explicit exact Patricia | clear leaf equality and validation | full leaf keys; no native arbitrary prefix terminals |
| threaded/tagged Patricia | compact historical layouts | subtle tags, traversal, portability, reclamation |
| crit-bit tree | compact binary exact string dictionary | precise key/end convention and full leaf compare |
| prefix/routing Patricia | longest network-prefix match | terminal prefixes, masks, family/table policy |
| radix edge trie | explicit common labels/prefix enumeration | label storage and LCP split/merge |
| ART | adaptive multiway byte fanout | node conversion and platform-sensitive thresholds |
| copy-on-write Patricia | coherent snapshots | path-copy and retained-generation space |
| hash/B-tree | exact average lookup or page order | different prefix/bit navigation and comparison costs |

Choose by exact versus prefix semantics, key width/encoding, ordered operations, update/snapshot needs, handle stability, layout, machine, persistence, and evidence—not by the name “Patricia.”

## Failure Modes and Misconceptions

- A reached leaf is a candidate, never proof of membership without full equality.
- Strictly increasing discriminator indices do not alone prove that leaves are under the correct branch.
- Fixed-width exact and variable-prefix routing trees have different terminal models.
- `n-1` internal nodes does not imply logarithmic height.
- Host byte layout is not a portable serialized bit convention.
- Signed numeric, byte lexicographic, Unicode, and locale orders are different comparators.
- Pointer tags require explicit portability, alignment, memory-model, and persistence review.
- Copy-on-write roots do not snapshot mutable external key/value buffers.
- Deletion topology can be simple while safe concurrent reclamation is not.
- Small-key functional evidence does not prove production width, parser, concurrency, or routing safety.

## Worked Examples

### Example 1

With eight-bit MSB-first keys `00` and `10`, the first differing bit is 3 (`00000000` versus `00010000`). The internal at bit 3 sends `00` left and `10` right; neither earlier equal bit needs a node.

### Example 2

Adding `12` (`00010010`) to `10` differs first at bit 6. Search inserts bit 6 below bit 3 on the `10` side, preserving strict `3<6`. A node at bit 2 would be wrong because those keys agree there.

### Example 3

Query `11` can reach leaf `10` or `12` depending on tested bits. Complete equality rejects it. A Patricia lookup that returns the reached value produces a false hit for every absent key.

### Example 4

Adding `80` differs from low keys at MSB position 0, so a new bit-0 root is inserted above the prior bit-3 tree. Discriminators can be inserted above existing roots; public root/node addresses are not stable identities.

### Example 5

Deleting `10` when its parent bit 6 also has leaf `12` replaces that parent by `12`. The higher bit-3 node may still distinguish `00` from `12`; four leaves imply three internals.

### Example 6

Eight fixed bits bound internal search height by eight, but keys of one-million-bit strings do not get a useful fixed constant. Key-width and maximum-length policies belong beside complexity claims.

### Example 7

Big-endian unsigned encodings make zero-before-one traversal numeric. Raw two's-complement signed encodings put nonnegative keys before negative at the sign bit, which conflicts with ordinary signed order unless transformed.

### Example 8

An IPv6 `/48` route is not a 128-bit exact leaf. It terminates after 48 network bits and may coexist with `/64` descendants; lookup must remember the deepest route terminal along an address traversal.

### Example 9

A persisted internal has bit 9 below parent bit 12. Both are in range, but strict monotonicity fails. A loader rejects before search rather than looping or silently retesting an earlier part of the key.

### Example 10

Two concurrent inserts compute replacements for the same parent link. Exactly one conditional publication succeeds; the loser retires its private nodes and retries against the new root. Plain stores can lose one key.

## Cross-Program Connections

- **Networking:** CIDR and forwarding tables add prefix terminals, masking, next hops, metrics, VRFs, and snapshot publication.
- **Database engineering:** discriminator indexes, compact key leaves, immutable generations, range order, and mapped formats resemble index pages.
- **Computer architecture:** bit extraction, endianness, pointer tags, inline keys, branch prediction, caches, and array indexes shape layout.
- **Concurrent programming:** conditional subtree replacement, ABA generations, immutable keys/values, reader pinning, and reclamation are core.
- **Security engineering:** signed/order mismatches, malformed bit graphs, cross-tenant routing, timing leakage, and resource limits are attack surfaces.
- **Programming languages:** symbol/interner maps need exact byte equality, stable entry identity, and snapshot ownership.
- **Testing/reliability:** exhaustive small bit universes and branch-consistency validation give unusually strong finite evidence.

## References

1. [NIST Dictionary of Algorithms and Data Structures, *Patricia tree*](https://xlinux.nist.gov/dads/HTML/patriciatree.html).
2. [Rust `patricia_tree` crate documentation](https://docs.rs/patricia_tree/latest/patricia_tree/).
3. [D. J. Bernstein, *Crit-bit trees*](https://cr.yp.to/critbit.html).
4. [Stanford CS166, *Tries and Suffix Trees* lecture notes](https://web.stanford.edu/class/archive/cs/cs166/cs166.1166/lectures/07/Small07.pdf).
5. [NetBSD maintained radix implementation](https://github.com/NetBSD/src/blob/trunk/sys/net/radix.c).
6. [FreeBSD maintained radix implementation](https://github.com/freebsd/freebsd-src/blob/main/sys/net/radix.c).
7. [RFC Editor, RFC 4632: *Classless Inter-domain Routing (CIDR)*](https://www.rfc-editor.org/rfc/rfc4632.html).
8. [Viktor Leis, Alfons Kemper, and Thomas Neumann, *The Adaptive Radix Tree*](https://db.in.tum.de/~leis/papers/ART.pdf).

## Exercises

### Exercise 1

Build an explicit MSB-first four-bit Patricia map by inserting `0000`, `0100`, `0110`, `1111`, and `1000` in that order. Give discriminator topology, leaf order, height, and full-equality result for absent `0101`.

### Exercise 2

Prove the `n-1` internal-node count and `height<=min(W,n-1)` bounds. Construct a family showing the height need not be logarithmic in `n`.

### Exercise 3

Specify a portable variable-length byte-key encoding for a Patricia exact map whose traversal order places a key before its proper extensions. Address embedded zero, maximum length, Unicode identity, serialization, and final equality.

### Exercise 4

Design deletion and reclamation for a copy-on-write Patricia map with generation-pinned readers. State allocation failure, publication, value ownership, slow-reader, ABA/handle, and validation rules.

### Exercise 5

Create a verification and benchmark plan comparing Patricia, crit-bit, radix-edge, ART, hash map, and B-tree for exact fixed/string keys plus ordered scans. Identify which comparisons are semantically invalid without changing the API.

## Answers to the Exercises

### Answer 1

`0000` and `0100` first differ at bit 1, creating root bit 1. `0110` differs from `0100` at bit 2, so bit 2 lies on root's one branch. `1111` differs from the reached low-side candidate first at bit 0, creating new root bit 0. `1000` shares bit 0 one with `1111` and first differs from it at bit 1, so a bit-1 internal lies in the high branch. One valid topology is root bit 0: zero child is bit 1 with leaf `0000` and bit-2 subtree leaves `0100`,`0110`; one child is bit 1 with leaves `1000`,`1111`. Zero-first leaf order is `0000,0100,0110,1000,1111`; maximum internal height is three. `0101` routes to a candidate such as `0100` but full equality returns absent.

### Answer 2

Let `i` internals and `n` leaves form a nonempty explicit tree. Each internal has two child edges, so edges equal `2i`; any tree with `i+n` nodes has `i+n-1` edges. Thus `2i=i+n-1` and `i=n-1`. Along a root-to-leaf path, discriminators are distinct strictly increasing positions within `W`, giving height at most `W`; no path contains more than all `i=n-1` internals, giving the minimum bound. Keys chosen to introduce successive later discriminators along one branch can create height proportional to `min(W,n-1)`, so balance/logarithmic height does not follow.

### Answer 3

Encode each canonical key as a sequence over an augmented alphabet where an explicit terminator sorts below byte values, for example represent each input byte as a tagged symbol `1||byte` and termination as symbol `0`, then serialize symbols with a fixed bit encoding. This avoids collision with embedded zero and makes a key's terminator compare before the next symbol of any extension. Bound raw bytes, canonical bytes, encoded bits, and expansion with checked arithmetic. For Unicode identifiers, apply one versioned normalization/case/security profile before byte encoding and store display separately. Persist encoding/profile version and byte order. Routing still ends at a candidate leaf; compare full encoded length/content (or canonical source) for exact membership.

### Answer 4

Keep nodes, keys, and values immutable within a generation. Deletion finds the leaf/parent, clones affected ancestors while replacing the parent with its sibling, validates counts/order, then release-publishes one new root; allocation failure discards private clones and leaves the old root intact. Readers acquire/pin a generation before loading root and release afterward. Refcounts/epochs/generation arenas reclaim only when no reader can access old nodes; monitor and limit slow-reader retained bytes. Values must be immutable/versioned, not shared mutable objects. Handles contain logical key/entry ID plus generation, never raw internal address; root generations avoid ABA within their nonwrapping policy. Validate full branch/discriminator/count invariants on the new private root before publication and during tests.

### Answer 5

Define canonical key encoding/equality, duplicate update, sorted order, get/delete, lower-bound/range, snapshot, and output semantics first. An exact hash map lacks native ordered scans; a prefix radix API and leaf Patricia differ; either exclude unmatched operations or include the documented auxiliary/sort cost. Compare all results with an independent ordered map, exhaust small bit/key sets and discriminator/LCP cases, inject allocation/publication/persistence faults, corrupt formats, and test concurrent histories/reclamation. Workloads vary key widths/lengths, first-difference and prefix distribution, hits/misses, updates/deletes, scan sizes, values, snapshots, and threads. Measure resident/peak bytes, nodes/labels/capacity, tested/compared bytes, latency quantiles, cache/branch/TLB, build/update/reclaim, mapping, and retained generations. Results support only the measured platform/workload and implemented semantics, not universal superiority, Unicode/security correctness, lock freedom, or crash safety.
