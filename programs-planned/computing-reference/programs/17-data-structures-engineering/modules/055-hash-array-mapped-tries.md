---
module_id: DSE-055
program: Data Structures Engineering
level: 2
module_number: 55
title: Hash Array Mapped Tries
status: complete
last_verified: 2026-08-30
---

# Hash Array Mapped Tries

## One-Page Review

### Governing question

How can an immutable hash map consume fixed-width hash fragments through a compact trie while preserving exact key equality, collision correctness, path-copy isolation, deletion normalization, transient ownership, bounded depth, and honest memory and security evidence?

### Essential definitions

- A **hash array mapped trie** (HAMT) is a trie over successive fixed-width fragments of a key hash.
- The **branching factor** is `B=2^w`, where `w` hash bits select one logical child per level.
- A **bitmap-indexed node** stores a `B`-bit occupancy bitmap and a compact array containing only present branches.
- The **logical slot** is the fragment value; the **physical index** is the number of set bitmap bits below that slot.
- An **array node** stores a dense `B`-entry child array when occupancy makes bitmap compaction less attractive.
- A **payload entry** stores key, value, and usually its original/improved hash at or within a trie node.
- A **hash-collision node** stores distinct keys with identical full hashes and resolves them by key equality.
- **path copying** replaces nodes along the accessed hash path and shares all untouched branches.
- **CHAMP** is a compressed HAMT organization separating payload and child-node bitmaps for denser layouts and canonical forms under its rules.
- A **transient** is a temporarily editable, uniquely authorized view that freezes back into an immutable persistent map.

### Central model, mechanism, or theorem

Given a `b`-bit hash and fragment width `w`, level `d` selects `(hash >> (dw)) & (B-1)`. A bitmap node tests bit `1 << slot`. If absent, lookup misses. If present, `popcount(bitmap & (bit-1))` maps the sparse logical slot to its compact-array index. Traversal continues until a payload/collision node confirms full hash and key equality.

Immutable insertion copies the nodes on that fragment path, inserts or replaces the terminal payload, and shares every untouched child. Two hashes with equal early fragments create deeper bitmap nodes until they diverge. Two distinct keys with the same entire hash enter an explicit collision node; the trie must never treat hash equality as key equality. Removal deletes the entry, collapses collision/singleton nodes only under valid normalization rules, and copies the affected path.

For a fixed-width well-distributed hash, depth is bounded by `ceil(b/w)` before the collision representation, so the structural height is a small constant for fixed `b`; in a parameterized model it is `O(log_B U)` over hash universe `U`, not a universal worst-case `O(1)` for adversarial equality/collision buckets. Node array copying, hash/equality cost, allocation, cache locality, and collision policy determine real performance.

### Critical invariants

1. Equal keys produce equal hashes for their entire residence; key equality and hashes are stable.
2. Every entry is reachable through exactly the fragments of its stored/recomputed full hash.
3. Each bitmap's set-bit count equals the compact-array arity and its rank calculation maps slots exactly.
4. Node/payload maps, array partitions, and tags agree with the concrete layout; no slot is represented twice.
5. A collision node contains at least the required number of distinct equal-hash keys and resolves by equality.
6. Insert, replacement, and removal never mutate any node/key/value reachable from an old root.
7. Removal normalization preserves all remaining entries and the valid parent-depth interpretation.
8. Stored count, cached hashes, and optional subtree metadata equal independent recomputation.
9. Transient edit authorization is exclusive; shared source nodes copy before mutation; freeze revokes edit capability.
10. Complexity/security claims include hash quality, collision bucket behavior, resource quotas, runtime layout, and workload.

### Common failures

- Using a hash match as proof of key equality.
- Failing to represent distinct keys whose complete hashes collide.
- Computing compact index from the wrong bitmap or bit range.
- Mixing payload and child ordering conventions during update or iteration.
- Mutating an array/node still reachable from a persistent source or sibling version.
- Collapsing a remaining internal node to a level where its fragments are interpreted incorrectly.
- Leaving empty, singleton, or over/underfull nodes in a shape forbidden by the implementation contract.
- Allowing key hash/equality to change after insertion.
- Claiming constant worst-case behavior despite unbounded equality work in a collision node.
- Benchmarking random integer keys only and ignoring node bytes, allocation, hashing, collisions, removals, and retained versions.

### Compact example

With `w=2`, hashes `0` and `4` share root fragment `0` but diverge at the next fragment (`0` versus `1`), so insertion creates one deeper bitmap. Hash `1` occupies root fragment `1`. Two distinct keys with hash `42` share every fragment and therefore occupy a collision node at root fragment `2`. Replacing the value for the hash-`4` key copies root fragment `0` but shares the collision branch. Removing the hash-`1` key copies the root and shares fragments `0` and `2`.

### Connections

[DSE-021](021-hash-functions-and-distribution.md), [DSE-022](022-separate-chaining.md), and [DSE-029](029-hash-flooding-resistance.md) supply hash/equality/collision threats. [DSE-044](044-tries.md) and [DSE-045](045-compressed-and-radix-tries.md) supply trie/rank concepts. [DSE-051](051-path-copying.md) and [DSE-052](052-structural-sharing.md) supply version, sharing, lifetime, and evidence models. The [program roadmap](../ROADMAP.md) continues with finger trees, persistent vectors, snapshots, concurrency, and verification.

## Governing Question

Which hash contract, fragment width, node repertoire, bitmap/rank layout, collision policy, immutable update/removal normalization, transient protocol, lifetime model, and evidence make a HAMT a correct and production-worthy persistent map?

## Why This Matters

Persistent hash maps are foundational values in functional programs, compilers, build systems, immutable application state, snapshot services, rule engines, and concurrent read-mostly systems. A HAMT avoids copying an entire flat hash table per update. Its high branching factor gives shallow paths, while bitmaps avoid allocating a full sparse array at every node.

The idea sounds like “use chunks of the hash as trie digits,” but correctness lives in the compression details. A logical slot does not equal a compact-array position. Payloads and child nodes may have different packed regions. Full-hash collisions do occur. Removal must normalize without forgetting the depth at which remaining branches are interpreted. Mutable builder optimizations must distinguish newly owned arrays from shared persistent arrays.

HAMTs also expose the boundary between asymptotic notation and machines. A 32-way node copies compact arrays, invokes popcount, allocates headers, follows pointers, and stresses caches and collectors. Dense array nodes trade space for indexing. CHAMP-like layouts improve locality and iteration but add layout invariants. Small-map specializations can beat a trie until a promotion threshold.

Security is not inherited from the word “trie.” Attackers who control hashes or equality cost can force large collision nodes, deep work within fixed hash width, expensive comparisons, memory amplification, or retained version floods. Seeded hashing, collision trees, quotas, and bounded diagnostics are policies that must match the threat model.

## Prerequisites and Retrieval

Retrieve hash/equality requirements and avalanche/distribution from [DSE-021](021-hash-functions-and-distribution.md), collision handling from [DSE-022](022-separate-chaining.md), resizing/cost accounting from [DSE-028](028-resizing-and-incremental-rehashing.md), and adversarial hashing from [DSE-029](029-hash-flooding-resistance.md). Retrieve trie paths/compression from [DSE-044](044-tries.md) and [DSE-045](045-compressed-and-radix-tries.md).

Retrieve persistent update/failure/lifetime from [DSE-051](051-path-copying.md), canonical versus opportunistic sharing and physical-DAG accounting from [DSE-052](052-structural-sharing.md), and immutable collection/transient lessons from [DSE-053](053-persistent-lists-and-queues.md). You should be able to trace bits, prove a recursive abstraction invariant, distinguish logical and physical size, and test all retained roots.

## Learning Objectives

After completing this module, you can:

1. derive HAMT traversal from hash fragments, bitmap membership, and rank;
2. specify bitmap, array, payload, and collision node invariants;
3. trace persistent lookup, insert, replacement, and removal with exact sharing;
4. explain deep-prefix divergence and complete-hash collision handling;
5. prove path-copy isolation and valid removal normalization;
6. compare classic HAMT, CHAMP, small-map, collision, and dense-node layouts;
7. design transients with edit-token/ownership/freeze guarantees;
8. specify concurrency, serialization, migration, and failure contracts;
9. validate every version plus global sharing and retention properties; and
10. benchmark hashing, equality, allocation, node bytes, locality, collisions, transients, and tail behavior.

## Core Exposition

**Begin with unordered-map semantics.** A map associates at most one value with each key according to equality `eq`. `get`, `contains`, `associate`, `remove`, size, iteration, fold, union/intersection/difference, equality, hashing, and transient construction are separate API operations. Iteration order may be unspecified, stable for a given seed/build, or deliberately defined; never promise insertion order unless the representation supports it.

The hash contract is one-way: if `eq(a,b)` then `hash(a)=hash(b)`. Unequal keys may share a hash. Both equality and hash must remain stable while a key is retained. A mutable key whose hash changes becomes unreachable through its stored path. A stateful or asymmetric equality function can make replacement, collision lookup, and map equality incoherent.

Decide whether a map retains the original equal key or replaces it on association, whether equal values return the identical root, how null/nil keys are represented, and whether hashes are cached. A reserved null slot outside the trie is an implementation choice requiring count/equality/iteration coverage.

Persistent semantics mean `associate(root,k,v)` and `remove(root,k)` return roots without changing any previous root. Any retained version can branch. Deep snapshot semantics also require immutable/copy-owned keys and values; otherwise only the HAMT spine is persistent.

**Partition the hash into trie digits.** Let hash width be `b` and consume `w` low-to-high or high-to-low bits per level according to one fixed convention. `B=2^w`, `mask=B-1`, and at shift `s`, `slot=(h >> s) & mask`. For `w=5`, logical slots range 0–31. A fixed 32-bit hash needs at most seven fragments when the final fragment has fewer effective bits; 64-bit policies differ.

A naïve array-mapped trie stores `B` child pointers in every internal node. It offers direct `children[slot]` but wastes space when occupancy is low. Bitmap compression stores a `B`-bit occupancy word and an array only for occupied slots. For `bit=1<<slot`, absence is `(bitmap & bit)==0`. Presence maps to physical index

`index = popcount(bitmap & (bit - 1))`.

Bits below the target correspond exactly to occupied logical slots with smaller indices. The compact child array is therefore ordered by logical slot. Insertion of an absent slot sets the bit and inserts at `index`; removal clears the bit and removes at `index`. Using `popcount(bitmap)` or `popcount(bitmap & bit)` is wrong.

Bitmap width, integer signedness, shift masking, and popcount primitives are language-specific. In a 32-bit signed integer, bit 31 may look negative yet still be a valid bit pattern. Avoid undefined shifts in C/C++; use unsigned types and exact bounds. A final partial fragment must not read beyond the hash model.

**Node layout is part of the proof.** A simple design has `BitmapNode(bitmap,children)`, `ArrayNode(count,children[B])`, `Leaf(hash,key,value)`, and `Collision(hash,entries)`. Other designs store key/value payloads inline in bitmap nodes and distinguish payload positions from child positions. CHAMP-style nodes use separate data and node maps and pack payloads/nodes into arranged array regions.

For a two-bitmap node, require `dataMap & nodeMap == 0`, popcounts match payload/node counts, occupied slots equal their union, physical indexing uses the corresponding bitmap, and packed positions follow the implementation's direction. Store size/cached hash only if every update recomputes it. Type tags and null encodings must be unambiguous.

Dense array nodes reduce rank and compact-array insertion costs at high occupancy but allocate `B` slots. Define promotion threshold bitmap→array and demotion threshold array→bitmap with hysteresis if oscillation matters. Conversion must preserve each logical slot, count, node kind, and metadata. Thresholds are performance policy, not universal constants.

Small maps often use a flat immutable array of key/value pairs, promoting to HAMT after a threshold. This improves locality and header cost for tiny collections. Promotion/demotion changes iteration order and identity unless contract says otherwise; equality remains map equality.

**Lookup ends with equality, not hash.** At an internal node, compute slot and compact index, then recurse with `shift+w`. At a leaf, compare stored full hash as a fast rejection and then compare key equality. A full-hash match is only a candidate. At a collision node, confirm matching stored hash and search entries by equality.

If hash computation is expensive, caching can help, but cached hashes require key immutability and include seed/improvement policy. A map moved across a process with another randomized seed cannot reuse path hashes blindly. Hash improvement/mixing is part of the representation version.

Missing branches terminate quickly. A malicious equality function may throw, recurse, allocate, or take unbounded time; constrain key types or treat failures as operation failures that preserve old roots. Hash/equality exceptions during lookup do not mutate the map; during private update they must release partial allocations.

**Insertion handles three distinct collision cases.** An absent branch inserts a payload and copies each ancestor. An existing equal key applies replacement/no-op policy. Unequal full hashes that share current fragment create/deepen bitmap nodes until a fragment differs. Distinct keys with identical complete hashes enter a collision node.

Deep-prefix collision is not a full collision. For `w=5`, two 32-bit hashes may share several low fragments, producing a chain of single-child internal nodes before diverging. Correctness follows because both entries remain under their shared prefix, then occupy distinct next slots. Implementations may compress paths, but compressed prefixes require explicit prefix/length validation.

A full collision cannot be resolved by consuming more bits: none remain and every fragment is equal. Store a collision bucket/list/array/tree. Every operation compares equality within it. Replacing one key preserves other entries. Inserting a third distinct equal-hash key extends the bucket. Removing to one entry can convert to a leaf, subject to parent normalization.

Path copying allocates a new terminal node and new ancestors. At each ancestor, the compact child array normally must be copied with one changed element/insert/delete, even though sibling child objects share. Thus “copies only `O(depth)` nodes” hides copied array slots/bytes. Branch factor trades shallow depth against per-node array copying and sparsity.

If an update discovers identical key and equal value, returning the same root maximizes sharing, but value equality may be expensive or user-defined. Version-event systems may still record a new logical commit even when the map root is identical. Keep structural root and version/provenance record separate.

**Removal is more subtle than lookup.** Traverse using hash fragments and equality. If absent, return the original node/root. Remove a leaf, or remove one collision entry. Then reconstruct ancestors. A bitmap node with no children becomes empty. A collision with one entry can become a leaf. A singleton bitmap may sometimes collapse its sole leaf/collision child upward because such terminal nodes re-check full hash; collapsing an internal bitmap can be invalid if it changes which shift interprets its descendants.

Normalization rules depend on node repertoire. CHAMP payloads inline at their correct level; migrating a singleton payload or child must obey canonical layout. Dense nodes may demote when occupancy falls below threshold. Counts, cached hashes, data/node maps, and arrays update atomically in the new node.

Canonical representation is valuable for equality and memory but must be proven. If insertion order can produce different permitted shapes, pointer inequality cannot reject map equality. Even canonical shape under fixed hashes does not mean roots are pointer-identical without hash-consing; structural equality can compare node layouts faster when canonical rules hold.

Test removal after every insertion pattern: absent key, equal-hash bucket head/middle/tail, bucket 2→1, deep-prefix branch 2→1, root last entry, bitmap/dense threshold, inline payload/child migration, and branches retaining the pre-removal root. Historical versions must not observe array compaction.

**Complexity needs the hash universe and bucket bound.** With `b` fixed hash bits and `w` per level, internal depth is bounded by `ceil(b/w)`. For machine-sized hashes this is a small constant, which motivates “effectively constant” descriptions. In an asymptotic universe model, expected or structural lookup is `O(log_B U)` plus terminal equality work.

If `c` unequal keys share a full hash and the collision representation is linear, lookup/update/remove is `O(c)` key comparisons. An adversary can make `c=n` when hashes are controlled. A balanced collision tree can give logarithmic bucket operations but needs a stable secondary order or another trusted discriminator. Seeded keyed hashing makes chosen collisions harder but is not proof against all denial-of-service or expensive equality.

Allocation for a point update is proportional to path depth in nodes, but bytes include compact arrays copied at each level, payload tuples, collision arrays, headers, alignment, allocator classes, refcounts, and garbage. Iteration visits all entries/nodes and is `Theta(n)` logical work; locality depends on layout. Map equality/hashing may be `Theta(n)` even with shallow lookup.

Hash computation cost may be `Theta(key length)` and dominate trie traversal. Caching hashes shifts cost to insertion/memory and relies on immutable key content. Report hash, equality, popcount/rank, allocation, and traversal separately when possible.

**CHAMP optimizes layout and bulk behavior.** Compressed Hash-Array Mapped Prefix-trees distinguish in-node payloads from child nodes using separate bitmaps, remove wrapper indirections, and arrange arrays to improve cache locality and iteration. Under specified normalization they can provide a canonical structural form for fixed hashes/equality.

This changes invariants, not abstract map semantics. Data and node ranks use different bitmaps. Payloads may occupy paired array cells while child nodes occupy another region. Insert/remove can migrate between inline payload and subnode. Equality and iteration optimizations rely on exact layout. Port the full algorithm and tests; do not mix one paper's indexing equation with another implementation's packing convention.

Bulk union/intersection/difference can align trie fragments and recurse only where bitmaps overlap. Disjoint slots share whole subtrees. Colliding payloads require conflict/equality policy. Complexity depends on structural overlap, hash distribution, and exact algorithm. Parallel recursion is possible at independent branches, but allocation and cutoff overhead matter.

HHAMT-style specialization can encode heterogeneous payload categories with additional bitmaps, reducing nested collection overhead for multimaps. It expands node layout states and verification surface. Use only when workload evidence justifies the complexity.

**Transients optimize batches through controlled mutation.** Repeated persistent inserts copy an ancestor array on every operation even when successive updates touch the same private path. A transient attaches an edit token/owner to editable nodes. On access, a node with matching owner may update its private array in place; a shared/different-owner node is copied and marked with the current owner. Freeze publishes an immutable root and revokes editing.

The invariants are exclusive edit authority, no persistent reader sees mutation, copy-on-first-touch for shared nodes, correct bitmap/layout after each transient operation, no use after freeze, and safe failure/cancellation. “The caller promises not to alias” is too weak unless the API/type/runtime enforces or detects it according to contract.

Thread confinement is a common policy but not the only possible enforcement. If a runtime relaxes thread identity checks, single-path/nonconcurrent use remains an obligation. An edit token does not make concurrent mutation safe. Freeze requires a release/publication barrier where the memory model needs it; later persistent updates must not mutate transient arrays.

Bulk builders may instead sort/group by hash fragments and construct nodes bottom-up, reducing repeated copies. Compare transients, bulk construction, and persistent folds by input size, duplicates/collisions, locality, peak memory, failure cleanup, and final validation. Speedup is empirical.

**Lifetime and failure follow the version DAG.** Every persistent root, iterator, cache, transient source, active transient, latest-root handle, and serialized manifest can retain subtrees. Tracing GC handles fan-in/cycles introduced by payloads/caches. Reference counting gives prompt reclamation for acyclic HAMT nodes but adds counter traffic and recursive/deferred destruction. Arenas can amplify retention across shared generations.

Monitor root/version count, oldest reader, unique/live/reclaimed/allocated nodes and bytes, bitmap/array/collision-node counts, occupancy distribution, collision-bucket sizes, depth, sharing fan-in, transient-owned bytes, allocator/GC pauses, and retention owner. Summing map sizes across roots overstates shared physical entries; current-root size understates historical retention.

Build persistent updates privately. Hash/equality, allocation, array copy, collision growth, metadata, or validation can fail. Release partial nodes and preserve input roots. Publish/register the completed root last. For transients, failure policy may leave the private builder usable, poisoned, or disposable; specify it and never expose partial persistent state.

Count/bitmap arithmetic must reject overflow and invalid shifts. Hostile serialized nodes may claim impossible bitmap/array counts. Recursive destruction/validation of a corrupt deep graph can overflow the stack; use bounded iterative validation before trust.

**Concurrency separates immutable snapshots from shared updates.** Once safely published and lifetime-protected, immutable roots support lock-free read traversal in the ordinary sense of no structure mutation. Two writers starting from one root produce valid branches. A shared latest root needs a lock, atomic compare-and-swap loop, transaction, or intentional branch registry.

CAS losers retry or preserve branches and release private nodes. Hash/equality/value callbacks must be retry-safe. ABA and reclamation require managed references, generations, hazards, epochs, or locks. A successful root CAS is a map-wide linearization point; it does not make the constructor wait-free, nor guarantee per-key merge semantics.

Concurrent reads of cached map hash/lazy metadata need safe once-publication or eager immutable fields. Transients are not shared concurrent maps. Bulk parallel operations read immutable inputs safely but must publish only complete results and clean cancelled subtrees.

Long readers pin historical branches. Backpressure and root/reader leases may be necessary. Never reclaim based only on the current root.

**Serialization should prefer logical maps unless structural sharing is required.** A durable logical format stores bounded canonical key/value records, schema, hash/equality policy identifier if relevant, and count; rebuilding recomputes process-local seeded hashes. Do not persist runtime pointers, edit tokens, array headers, random seeds as portable identity, closures, or cached process-specific hashes.

Graph serialization can preserve many version roots and shared nodes. Assign stable IDs or content hashes, write node tags/bitmaps/arrays/collision entries, and bind root manifests. Validate references, acyclicity, fragment placement, bitmap/popcount/arity, data/node disjointness, collision hashes/equality uniqueness, counts, depth, reachability, and quotas before exposing lookup.

Content addressing needs canonical encoding, domain separation, child-before-parent durability, collision policy, and immutable keys/values. A HAMT's ordinary noncryptographic key hash is not a content identifier. Root publication, checksums, flushes, recovery, and garbage collection are storage protocols beyond in-memory persistence.

Hash algorithm/seed, fragment order/width, node thresholds, key encoding/equality, and layout changes can alter every path. Logical migration rebuilds a new generation and retains old roots until policy permits deletion. Cross-version diffs should compare logical entries unless structural format/version matches.

**Security starts at hashes and resources.** Seeded/keyed hash mixing mitigates attacker-chosen collision floods when the attacker cannot discover/control the seed and the function/key type is appropriate. Rotate policy carefully: changing seed requires rebuilding. Cryptographic hashing can be too expensive for ordinary maps and still leaves expensive equality/large keys.

Bound map/versions/roots, key/value bytes, hash/equality time, collision bucket length, depth, node/array count, batch/transient duration, iteration/diff/output, serialized graph, and reader age. Choose reject, secondary collision tree, reseed/rebuild, or isolate-tenant responses before overload.

Hash/equality timing, iteration order, randomized seed, structural-sharing diagnostics, object addresses, and retained histories can leak information. Do not expose internal node shapes or hashes across trust boundaries without purpose. Authorize each root/history; immutable old versions preserve deleted secrets until reclaimed.

Malformed graph formats can contain cycles, duplicate slots/keys, wrong fragments, impossible bitmaps, enormous collision counts, aliased mutable arrays, and decompression bombs. Validate within quotas before hashing/equality callbacks where possible. Fuzz parsers and invariant checkers.

**Evidence must include collisions and all versions.** Maintain an independent ordinary map snapshot per root with controlled immutable keys and known hashes. Generate associate, replace, remove, lookup, branch-from-any-version, union, transient batch, and freeze operations. Compare all old and new roots after every operation.

Use synthetic key wrappers with chosen hashes to force each fragment, deep shared prefixes, full collisions, and hash/equality edge cases. Do not rely only on runtime random strings. Exhaust small fragment widths because bitmap/layout states become enumerable. Include absent/equal key, equal value no-op, null policy, and mutable-key rejection/documentation.

Validate local nodes: tag, bitmap ranges, popcounts, compact arity, data/node disjointness, dense counts, collision hashes/unique equalities, stored metadata, and allowed normalization. Validate globally: acyclicity, each entry's complete fragment path, unique logical keys, exact count, every root's reference equality, old-node immutability, expected sharing, transient ownership, and reachability accounting.

Metamorphic relations include associate then get; remove then miss; associate equal value no-op under policy; remove absent returns equal/original root; branch isolation; batch transient result equals persistent fold; freeze prevents edits; iteration entries rebuild an equal map; union with empty; union conflict resolver; serialization round trip; and rehash migration preserves logical map.

Fault-inject hash/equality, each allocation/array copy/promotion/demotion/collision operation, transient copy/freeze, root CAS, serialization write/flush/publication, and reclamation. Concurrency tests race readers/root writers, CAS retries, release, cached hash, and prohibited transient sharing. Use memory/thread sanitizers or managed-runtime diagnostics as applicable.

Benchmarks vary size, fragment width/node thresholds, hash distribution, full collisions, key/value/hash/equality size, lookup/hit/miss/insert/replace/remove/iterate/equality/hash/union mix, batch/transient size, branch depth/fan-out, retained roots/readers, runtime/allocator/GC, threads, and serialization. Report latency quantiles, hash/equality calls, trie depth, popcounts, node/array copies and bytes, occupancy/node kinds, collision lengths, allocation/reclamation/live/retained bytes, cache/TLB/branches, GC pauses, CAS retries, and correctness validation.

The executable below uses two-bit fragments and immutable tuples for bitmap, leaf, and full-hash collision nodes. It inserts deep-prefix and complete-hash collisions, replaces and removes entries, creates a branch from an older version, checks exact paths/layout, and verifies selected identity sharing. It does not model 32-way/CHAMP/dense nodes, transients, randomized hashing, concurrency, durability, hostile parsing, or performance.

<!-- bijux-verify: {"id":"persistent-hamt-version-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"m5_items=alpha:A,beta:B,collide-one:C1,collide-two:C2,gamma:G\ncollision_bucket=2\nreplacement_old=B\nreplacement_new=B2\nm5_unchanged=True\nremoved_gamma=True\nm7_shares_collision_branch=True\nbranch_items=alpha:A,beta:B,delta:D,gamma:G\nbranch_isolated=True\nm6_shares_collision_branch=True\nm8_shares_chunk_zero=True\nall_lookups=True\nall_invariants=True\nevidence=finite_persistent_hamt_version_trace\n","stderr":""}} -->
```python
EMPTY = None
BITS = 2
MASK = 3


def popcount(value):
    count = 0
    while value:
        count += value & 1
        value >>= 1
    return count


def fragment(hash_code, shift):
    return (hash_code >> shift) & MASK


def leaf(hash_code, key, value):
    return ("leaf", hash_code, key, value)


def collision(hash_code, entries):
    return ("collision", hash_code, entries)


def bitmap(bits, children):
    return ("bitmap", bits, children)


def merge_nodes(left_hash, left, right_hash, right, shift):
    left_slot = fragment(left_hash, shift)
    right_slot = fragment(right_hash, shift)
    if left_slot == right_slot:
        child = merge_nodes(left_hash, left, right_hash, right, shift + BITS)
        return bitmap(1 << left_slot, (child,))
    bits = (1 << left_slot) | (1 << right_slot)
    children = (left, right) if left_slot < right_slot else (right, left)
    return bitmap(bits, children)


def associate(tree, hash_code, key, value, shift=0):
    if tree is EMPTY:
        return leaf(hash_code, key, value)
    tag = tree[0]
    if tag == "leaf":
        if tree[1] == hash_code and tree[2] == key:
            return tree if tree[3] == value else leaf(hash_code, key, value)
        fresh = leaf(hash_code, key, value)
        if tree[1] == hash_code:
            return collision(hash_code, ((tree[2], tree[3]), (key, value)))
        return merge_nodes(tree[1], tree, hash_code, fresh, shift)
    if tag == "collision":
        if tree[1] != hash_code:
            return merge_nodes(tree[1], tree, hash_code, leaf(hash_code, key, value), shift)
        entries = []
        found = False
        unchanged = False
        for old_key, old_value in tree[2]:
            if old_key == key:
                found = True
                unchanged = old_value == value
                entries.append((old_key, value))
            else:
                entries.append((old_key, old_value))
        if found:
            return tree if unchanged else collision(hash_code, tuple(entries))
        entries.append((key, value))
        return collision(hash_code, tuple(entries))
    bits, children = tree[1], tree[2]
    slot = fragment(hash_code, shift)
    bit = 1 << slot
    index = popcount(bits & (bit - 1))
    if bits & bit == 0:
        updated = children[:index] + (leaf(hash_code, key, value),) + children[index:]
        return bitmap(bits | bit, updated)
    child = associate(children[index], hash_code, key, value, shift + BITS)
    if child is children[index]:
        return tree
    return bitmap(bits, children[:index] + (child,) + children[index + 1 :])


def lookup(tree, hash_code, key, shift=0):
    if tree is EMPTY:
        raise KeyError(key)
    tag = tree[0]
    if tag == "leaf":
        if tree[1] == hash_code and tree[2] == key:
            return tree[3]
        raise KeyError(key)
    if tag == "collision":
        if tree[1] == hash_code:
            for old_key, old_value in tree[2]:
                if old_key == key:
                    return old_value
        raise KeyError(key)
    slot = fragment(hash_code, shift)
    bit = 1 << slot
    if tree[1] & bit == 0:
        raise KeyError(key)
    index = popcount(tree[1] & (bit - 1))
    return lookup(tree[2][index], hash_code, key, shift + BITS)


def remove(tree, hash_code, key, shift=0):
    if tree is EMPTY:
        return tree
    tag = tree[0]
    if tag == "leaf":
        return EMPTY if tree[1] == hash_code and tree[2] == key else tree
    if tag == "collision":
        if tree[1] != hash_code:
            return tree
        kept = tuple((k, v) for k, v in tree[2] if k != key)
        if len(kept) == len(tree[2]):
            return tree
        if len(kept) == 1:
            return leaf(hash_code, kept[0][0], kept[0][1])
        return collision(hash_code, kept)
    bits, children = tree[1], tree[2]
    slot = fragment(hash_code, shift)
    bit = 1 << slot
    if bits & bit == 0:
        return tree
    index = popcount(bits & (bit - 1))
    child = remove(children[index], hash_code, key, shift + BITS)
    if child is children[index]:
        return tree
    if child is EMPTY:
        new_bits = bits & ~bit
        new_children = children[:index] + children[index + 1 :]
        if not new_children:
            return EMPTY
        if len(new_children) == 1 and new_children[0][0] != "bitmap":
            return new_children[0]
        return bitmap(new_bits, new_children)
    return bitmap(bits, children[:index] + (child,) + children[index + 1 :])


def entries(tree):
    if tree is EMPTY:
        return ()
    if tree[0] == "leaf":
        return ((tree[2], tree[3], tree[1]),)
    if tree[0] == "collision":
        return tuple((key, value, tree[1]) for key, value in tree[2])
    result = ()
    for child in tree[2]:
        result += entries(child)
    return result


def child_at(tree, slot):
    bit = 1 << slot
    if tree[0] != "bitmap" or tree[1] & bit == 0:
        return EMPTY
    return tree[2][popcount(tree[1] & (bit - 1))]


def hashes(tree):
    return tuple(item[2] for item in entries(tree))


def valid(tree, shift=0):
    if tree is EMPTY:
        return True
    if tree[0] == "leaf":
        return isinstance(tree[1], int)
    if tree[0] == "collision":
        keys = tuple(key for key, _ in tree[2])
        return len(keys) >= 2 and len(keys) == len(set(keys))
    bits, children = tree[1], tree[2]
    if bits == 0 or popcount(bits) != len(children):
        return False
    for slot in range(1 << BITS):
        bit = 1 << slot
        if bits & bit:
            child = children[popcount(bits & (bit - 1))]
            if any(fragment(value, shift) != slot for value in hashes(child)):
                return False
            if not valid(child, shift + BITS):
                return False
    data = entries(tree)
    keys = tuple(item[0] for item in data)
    return len(keys) == len(set(keys))


def render(tree):
    return ",".join(key + ":" + value for key, value, _ in sorted(entries(tree)))


m0 = EMPTY
m1 = associate(m0, 0, "alpha", "A")
m2 = associate(m1, 4, "beta", "B")
m3 = associate(m2, 1, "gamma", "G")
m4 = associate(m3, 42, "collide-one", "C1")
m5 = associate(m4, 42, "collide-two", "C2")
m6 = associate(m5, 4, "beta", "B2")
m7 = remove(m5, 1, "gamma")
m8 = associate(m3, 2, "delta", "D")

collision_branch = child_at(m5, 2)
versions = (m0, m1, m2, m3, m4, m5, m6, m7, m8)
all_lookups = (
    lookup(m5, 0, "alpha") == "A"
    and lookup(m5, 4, "beta") == "B"
    and lookup(m5, 42, "collide-one") == "C1"
    and lookup(m5, 42, "collide-two") == "C2"
)

print("m5_items=" + render(m5))
print("collision_bucket=" + str(len(collision_branch[2])))
print("replacement_old=" + lookup(m5, 4, "beta"))
print("replacement_new=" + lookup(m6, 4, "beta"))
print("m5_unchanged=" + str(lookup(m5, 4, "beta") == "B"))
print("removed_gamma=" + str(all(item[0] != "gamma" for item in entries(m7))))
print("m7_shares_collision_branch=" + str(child_at(m7, 2) is collision_branch))
print("branch_items=" + render(m8))
print("branch_isolated=" + str(render(m5) != render(m8)))
print("m6_shares_collision_branch=" + str(child_at(m6, 2) is collision_branch))
print("m8_shares_chunk_zero=" + str(child_at(m8, 0) is child_at(m3, 0)))
print("all_lookups=" + str(all_lookups))
print("all_invariants=" + str(all(valid(tree) for tree in versions)))
print("evidence=finite_persistent_hamt_version_trace")
```

## Definitions and Notation

- `eq(k1,k2)` is key equality; it implies equal hashes but the converse is false.
- `h(k)` is the stable full key hash after any named mixing/seed policy.
- `b` is hash width, `w` bits per level, `B=2^w` branching factor, and `mask=B-1`.
- At shift `s=dw`, `slot(h,s)=(h >> s) & mask`.
- `bit(i)=1<<i`; `rank(bitmap,i)=popcount(bitmap & (bit(i)-1))`.
- `BitmapNode(M,A)` stores occupancy bitmap `M` and compact array `A` ordered by logical slots.
- `ArrayNode(c,A_B)` stores `B` physical slots and occupied count `c`.
- `Leaf(h,k,v)` is a terminal mapping; `Collision(h,E)` stores distinct equal-hash entries.
- In CHAMP-like notation, `dataMap` marks inline payload slots and `nodeMap` child-node slots.
- `assoc(T,h,k,v)` and `remove(T,h,k)` return persistent roots.
- `shift` belongs to the traversal context; a child bitmap interprets the next `w` bits.
- `Reach(r)` is physical reachability from root `r`; retained roots form a version DAG.
- **Canonical shape** means a fixed logical map/hashes normalize to one structural layout, not necessarily one object identity.
- **Transient owner/edit token** authorizes mutation only of nodes uniquely editable for one builder.
- A **collision flood** is a workload with a large number of unequal keys sharing a full hash or otherwise degrading the collision policy.

## Mechanisms, Invariants, or Proof Structure

**Bitmap/rank lemma.** For occupied logical slot `i`, set bits below `i` correspond one-to-one and in order with compact children before `i`; their count is `rank(M,i)`. Inserting/removing at that index plus setting/clearing the bit preserves the ordering. Popcount must use the node's correct bitmap.

**Path lemma.** Induct on internal depth. Every descendant hash shares the fragments represented by ancestors; the chosen child slot equals its next fragment. A leaf/collision then checks full hash/equality. Global validation recomputes every entry's fragments rather than trusting placement.

**Association proof.** Absent branch adds exactly one mapping. Equal key applies replacement policy without changing other mappings. Unequal hashes with shared prefix recurse until a differing fragment and preserve both paths. Equal full hashes create/update a collision bucket using equality. Copied ancestors preserve sibling submaps.

**Removal proof.** Absent removal returns the old node. Present removal deletes exactly one equal key; collision 2→1 becomes a leaf; empty descendants clear parent bits. Each collapse rule must preserve lookup at the parent's shift. Reconstruction preserves siblings and recomputes count/layout.

**Persistence proof.** Every persistent node/array/key/value is immutable under the contract. Association/removal create terminal replacements and new ancestor arrays; all untouched children are reused. Induction over return frames proves every input root remains unchanged. Transients require an additional exclusive-edit proof.

**Complexity proof.** Internal traversal has at most `ceil(b/w)` fragment levels for fixed-width hashes. Each level performs fragment/bitmap/rank plus node-array access/copy. Terminal collision work is `C(c)` for bucket size `c`. Therefore a claim is `O(ceil(b/w)+C(c))` operations under constant hash/equality/array bounds, with byte allocation analyzed separately.

**Transient proof.** A node mutates only if its edit owner matches the live builder. Otherwise copy before edit. Persistent roots never contain mutable-authorized nodes visible to editing; freeze revokes the builder and safely publishes fully initialized arrays. No intermediate transient root is persistent/aliased under the contract.

**Lifetime/publication proof.** All persistent roots/readers/iterators/caches/builders/manifests are lifetime roots. Reclamation follows union reachability. In-memory publication initializes descendants before root visibility; durable publication makes descendants recoverable before committing a root manifest.

**Evidence separation.** Logical map equivalence, local layout, hash-path validity, old-version isolation, optional canonicality/sharing, transient safety, reclamation, concurrency, durability, security, and performance are separately tested/reviewed.

## Alternatives and Trade-Offs

| Design | Benefit | Cost/risk |
|---|---|---|
| Full array-mapped trie | Direct slot indexing | Severe sparsity/header cost at low occupancy |
| Bitmap-indexed HAMT | Compact sparse nodes, shallow paths | Popcount/rank and compact-array copies |
| Bitmap+dense node hybrid | Better high-occupancy access | Promotion/demotion states and thresholds |
| CHAMP | Denser payload/node layout, locality, canonical-form opportunities | More intricate two-bitmap packing invariants |
| Small flat map then HAMT | Excellent tiny-map locality | Promotion threshold and dual implementations |
| Linear collision node | Simple, compact for rare collisions | `O(c)` under collision flood |
| Ordered collision tree | Stronger large-bucket bound | Secondary order, metadata, higher constants |
| Persistent-only updates | Simple value semantics | Repeated array copying in large batches |
| Transient builder | Reuses privately owned arrays | Alias/owner/freeze/failure complexity |
| Ordered persistent tree | Deterministic range/ordering | More comparisons/depth; different API |
| Mutable flat hash table | Strong locality and in-place updates | No cheap persistent versions without another mechanism |

Choose using map size, key/hash threat, lookup/update/remove/iterate/bulk mix, branch retention, runtime object layout, and proof maturity. A library's mature HAMT/CHAMP is usually safer than a partial reimplementation.

## Failure Modes and Misconceptions

1. **Hash equals key:** distinct equal-hash keys overwrite each other.
2. **Wrong compact rank:** lookup and update access a neighbor slot.
3. **Deep prefix mistaken for full collision:** entries are bucketed too early or recursion never terminates.
4. **No full-collision terminal:** equal hashes recurse beyond hash width.
5. **Bad collapse:** removal lifts an internal node and changes fragment interpretation.
6. **Stale layout metadata:** popcount, arity, count, cached hash, or data/node maps disagree.
7. **Shared-array mutation:** transient or “optimization” changes old versions.
8. **Mutable key:** later hash/equality change makes an entry unreachable or duplicate.
9. **Universal constant-time claim:** collision equality and key hashing are omitted.
10. **Nodes equal bytes:** copied compact arrays, headers, alignment, and collector state are ignored.
11. **Immutability equals concurrency:** writers still need publication/conflict/lifetime semantics.
12. **Ordinary hash equals content address:** noncryptographic seeded path hashes are not durable object identities.

## Worked Examples

### Example 1

**Bitmap rank.** Let `M=0b10110100`, representing logical slots `2,4,5,7`. For slot `5`, `bit=0b00100000`; lower occupied bits are `M & (bit-1)=0b00010100`, whose popcount is two. Conclusion: logical slot 5 is compact array index 2, not index 5.

### Example 2

**Absent slot insertion.** In the same bitmap, insert slot `3`. Lower occupied slot count is one (only slot 2), so insert the child at compact index 1 and set bit 3. Existing child objects share; the node's compact array is copied. Conclusion: sparse logical position and physical insertion position are deliberately different.

### Example 3

**Deep-prefix divergence.** With `w=2`, hashes `0` (`00000000`) and `4` (`00000100`) both select root slot 0; at shift 2 they select slots 0 and 1. Create a root singleton bitmap whose child bitmap has both leaves. Conclusion: a shared fragment creates depth, not a full collision bucket.

### Example 4

**Complete-hash collision.** Keys `x` and `y` both have full hash 42 but are unequal. No future fragment distinguishes them. A collision node stores `(x,vx),(y,vy)` and every lookup confirms equality. Conclusion: full hash equality narrows candidates but never defines map-key equality.

### Example 5

**Persistent replacement sharing.** Root branches 0,1,2; beta lies below branch 0 and a collision node below branch 2. Replacing beta copies its leaf/path and root array, while branch-2 child identity remains unchanged. Conclusion: path copying shares subtrees, though each changed ancestor may copy a compact array.

### Example 6

**Collision removal 2→1.** Collision `(x,vx),(y,vy)` loses `x`. The terminal becomes leaf `(hash(y),y,vy)`. Parent updates its child; an allowed singleton collapse may lift that leaf because it verifies full hash. Conclusion: normalization shrinks representation without losing the remaining equality check.

### Example 7

**Invalid internal collapse.** A singleton bitmap at shift 10 contains another bitmap whose children diverge at shift 15. Lifting the child bitmap to the parent without storing skipped prefix causes lookup to interpret its bitmap using shift 10. Conclusion: internal-node collapse is illegal unless the representation records/compresses the skipped path or the lookup contract still matches.

### Example 8

**Mutable-key failure.** Key `K` hashes to 7 at insertion, then a mutable field changes its hash to 23. Lookup follows hash 23 and misses; reinsertion can create a second logically related entry. All versions share `K`. Conclusion: persistent structure does not make key objects hash-stable.

### Example 9

**Transient copy-on-first-touch.** A builder begins from root `R`. First update reaches a shared node with another owner, so it copies/marks it. Ten later updates on that owned path mutate its private array. Freeze revokes token and returns `R2`; `R` remains unchanged. Conclusion: batching saves repeated copies only when ownership enforcement is correct.

### Example 10

**Adversarial service choice.** An API accepts attacker-controlled strings and retains user-created versions. Use a per-process keyed hash, cap key/value and collision/root/reader resources, isolate tenants, and monitor bucket/depth/retention. Consider a collision tree or rejection threshold. Conclusion: a HAMT needs both collision defense and version-retention defense; shallow structural depth alone is insufficient.

## Cross-Program Connections

- Programming languages: immutable maps, transients, algebraic node types, generic hash/equality, and safe publication connect semantics to runtime representation.
- Algorithm engineering: bitmap rank, popcount, fragment width, node thresholds, bulk trie algebra, and collision bounds require exact cost models.
- Software engineering: persistent configuration/state maps enable snapshots and diffs but demand stable key/value ownership and migration contracts.
- Concurrent programming: immutable readers, atomic roots, CAS retries, edit-token confinement, reclamation, and parallel bulk operations have separate progress proofs.
- Security engineering: keyed hashing, collision buckets, expensive equality, root pinning, shape leakage, and hostile serialization require quotas and isolation.
- Database engineering: immutable root manifests, content-addressed graph storage, copy-on-write pages, snapshots, and garbage collection mirror HAMT lifecycle concerns.
- Formal methods: bitmap/popcount layout and bounded hash depth support exhaustive small-width testing and inductive refinement proofs.
- Performance engineering: compact arrays, object headers, cache locality, allocation, GC/refcount, hashing, and tail behavior decide whether the high branching factor pays.

## References

1. Phil Bagwell, “Ideal Hash Trees,” EPFL technical report, 2001. https://lampwww.epfl.ch/papers/idealhashtrees.pdf
2. Michael J. Steindorfer and Jurgen J. Vinju, “Optimizing Hash-Array Mapped Tries for Fast and Lean Immutable JVM Collections,” OOPSLA, 2015. https://michael.steindorfer.name/publications/oopsla15.pdf
3. Michael J. Steindorfer and Jurgen J. Vinju, “Fast and Lean Immutable Multi-Maps on the JVM Based on Heterogeneous Hash-Array Mapped Tries,” 2016. https://arxiv.org/abs/1608.01036
4. Clojure, `PersistentHashMap.java`, current implementation source, retrieved 2026-08-30. https://github.com/clojure/clojure/blob/master/src/jvm/clojure/lang/PersistentHashMap.java
5. Scala, immutable `HashMap.scala` (CHAMP), 2.13 branch source, retrieved 2026-08-30. https://github.com/scala/scala/blob/2.13.x/src/library/scala/collection/immutable/HashMap.scala
6. Clojure, “Transient Data Structures,” current official reference, retrieved 2026-08-30. https://clojure.org/reference/transients
7. Rust `im`, immutable HAMT `HashMap` module documentation, current docs, retrieved 2026-08-30. https://docs.rs/im/latest/im/hashmap/index.html
8. Racket `data/hamt`, “Immutable Hash Array Mapped Tries,” current official documentation, retrieved 2026-08-30. https://docs.racket-lang.org/hamt/index.html

## Exercises

### Exercise 1

**Compute bitmap positions.** For `w=4` and bitmap `M=0b1010010010010001`, determine whether logical slots `0,4,7,10,13,15` are present and give the compact index for each present slot.

### Exercise 2

**Trace a persistent association.** A two-bit HAMT contains hashes 0,4,1. Associate hash 12 with a new key. Draw the fragment path, identify new versus shared nodes, and state why this is not a full collision.

### Exercise 3

**Design removal validation.** Specify local/global checks and generated histories that would validate bitmap/array/CHAMP removal, including collision and normalization transitions.

### Exercise 4

**Choose collision and transient policies.** Design a persistent map for a multitenant service with attacker-controlled keys and large batch imports. Choose hashing, collision representation/limits, transient ownership, quotas, and evidence.

### Exercise 5

**Transfer to durable version graphs.** Design a portable, crash-safe structural format for many HAMT roots while allowing a future hash/layout migration. State what is content-addressed, what must be canonical, how roots publish, how garbage is reclaimed, and how validation avoids hostile graphs.

## Answers to the Exercises

### Answer 1

Read set bits from the supplied bitmap. Slots 0,4,7,10,13,15 correspond respectively to masks `1`, `16`, `128`, `1024`, `8192`, and `32768`. In `0b1010010010010001`, set slots are `0,4,7,10,13,15`, so all queried slots are present. Their compact indices are the number of queried/set slots below them: `0→0`, `4→1`, `7→2`, `10→3`, `13→4`, `15→5`. Formally each is `popcount(M & ((1<<slot)-1))`; a validator should compute from the actual integer rather than a visual grouping.

### Answer 2

Hashes 0 and 4 share root fragment 0 and diverge at shift 2: fragments 0 and 1. Hash 1 occupies root fragment 1. Hash 12 (`0b1100`) has root fragment 0, then fragment 3. Association copies the root and its fragment-0 child bitmap, inserting a new leaf at logical slot 3 of that child. The fragment-1 root branch containing hash 1 is reused by identity. Hash 12 is not a full collision with 0 or 4 because its full bits differ and the second fragment distinguishes it; no equality-scanned collision node is needed.

### Answer 3

For every node independently check tag, bitmap width, popcount/array arity, data/node disjointness and packed ranks, dense occupied count, thresholds/allowed hysteresis, collision minimum size/full-hash equality/distinct keys, cached count/hash, and allowed singleton/empty shapes. Globally recompute every entry's fragments at every depth, require unique equality keys, exact root count, acyclicity, bounded depth, and logical equality with an independent map.

Generate absent removal; only entry; leaf under singleton chains; deep-prefix branch 2→1; collision buckets 2→1 and larger head/middle/tail; inline-payload↔child migration; bitmap↔dense threshold transitions; null policy; equal hashes; every slot including high/sign bit; branches from every pre-removal version; remove/reinsert; and repeated random histories. Compare all retained roots after every step, assert old-node immutability and promised sibling sharing, fault-inject each allocation/copy/conversion, validate transient removal/freeze, and fuzz corrupt serialized shapes. No normalization is accepted merely because lookups in the newest root pass.

### Answer 4

Use a per-process/per-tenant keyed, reviewed hash strategy over canonical bounded key bytes; equality must be stable and bounded. Store full collisions explicitly, then reject, isolate, reseed/rebuild, or promote to a proven secondary balanced representation before buckets exceed a policy limit. Never silently drop unequal equal-hash keys. Quotas cover key/value bytes, entries, roots/branches/readers, collision length, hash/equality time, batch size/duration, live/retained bytes, iteration/diff/output, and diagnostics.

For imports, create a transient with an unforgeable owner/edit token. Copy shared nodes on first touch, mutate only matching-owned arrays, forbid concurrent/aliased interim use, handle failure by disposal or a named valid state, validate, freeze with safe publication, revoke the token, and reject later edits. Compare its result with a persistent fold. Evidence forces chosen collisions, tenant isolation, quota rejection, hash/equality faults, concurrent misuse, freeze/use-after-free, retained histories, memory/GC, and latency tails under attack and ordinary imports.

### Answer 5

Define canonical encodings for key/value records and each structural node tag, bitmap(s), ordered payloads/child IDs, collision entries, count, schema, fragment width/order, and hash-policy version. Use a cryptographic content hash with domain separation over canonical bytes and child IDs; do not reuse ordinary seeded key hashes as object IDs. Store immutable children before parents and a checksummed commit/root manifest last, with explicit flush/atomic-publication guarantees and recovery selection.

Validate IDs/hashes, byte/count/depth quotas, acyclicity, bitmap/popcount/arity, CHAMP partitions, collision key uniqueness/full hashes, every key's fragment path under the recorded policy, root counts, and reachability before serving queries. Retained commit, reader, backup, and replication roots are garbage-collection roots; mark/sweep unreachable objects only after snapshot/durability policy permits. A future hash/layout/equality change logically iterates validated old entries into a new generation and publishes a new-format root; old readers keep old code/schema until retired. Test every crash point, missing/corrupt object, malicious cycle/fan-out, migration equivalence, authorization, and garbage-collection interruption.
