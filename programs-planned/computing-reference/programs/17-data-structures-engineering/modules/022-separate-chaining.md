---
module_id: DSE-022
program: Data Structures Engineering
level: 1
module_number: 22
title: Separate Chaining
status: complete
last_verified: 2026-08-29
---

# Separate Chaining

## One-Page Review

### Governing question

How can a hash table preserve exact map/set semantics when many keys select the same bucket, while keeping chain layout, ownership, load, resizing, iteration, failure, hostile inputs, and concurrency contracts explicit?

### Essential definitions

- **Separate chaining** stores each bucket's colliding entries in a separate container.
- A **bucket index** is `b=reduce(h(key),m)` for bucket count `m>0`.
- A **chain** is the bucket container; it may be a linked list, array, tree, or hybrid.
- **chain length** `Li` is the entry count in bucket i; `sum Li=n`.
- **load factor** is `α=n/m`, the average chain length for n entries and m buckets.
- A **full hash** is the hash before bucket reduction; caching it can avoid recomputation and reject some nonmatches.
- **rehashing** builds or activates placement under a new bucket count and possibly a new hash seed/function.
- **incremental rehashing** migrates bounded old-table work while operations continue.
- **treeification** replaces a long list-like bin with a balanced search structure under extra ordering/tie rules.
- **ownership policy** defines who allocates, retains, moves, destroys, and exposes keys, values, nodes, and bucket memory.

### Central model, mechanism, or theorem

Let table `T=<B0,...,B(m-1)>`. Its abstraction is the disjoint logical union of entries in all buckets, subject to the map's key-equivalence rule. Representation requires every entry e to occur exactly once in

\[
B_{reduce(h(e.key),m)}.
\]

Also `n=sum Li` and no two entries have equivalent keys for a unique-key map. Under simple uniform hashing, the expected chain length is `E[Li]=α`; an unsuccessful lookup inspects expected O(α) candidates plus hashing/bucket work. A successful bound depends on insertion/order/query assumptions. Worst-case lookup remains O(max Li), which can be O(n).

### Critical invariants

1. Every live entry appears in exactly one bucket selected by its current key/hash/count.
2. Equality, not hash equality, decides whether an entry matches.
3. Unique maps contain at most one representative per key-equivalence class; multi-maps define duplicate ordering and removal precisely.
4. `n`, every `Li`, ownership metadata, links/arrays/tree state, and cached hashes agree.
5. Insert/update/delete are failure-safe and destroy each owned resource exactly once.
6. Resize exposes either a coherent old table or a coherent migration state with no lost/duplicated logical entries.
7. Iterators/references and iteration order follow documented invalidation/stability rules.
8. Concurrent readers/writers, if supported, obey bucket/table synchronization and reclamation protocols.

### Common failures

- Returning the first equal hash without running key equality.
- Adding a duplicate node when unique-map insertion should update/reject.
- Losing the bucket head when deleting its first node, or dereferencing a freed predecessor.
- Updating size before an allocation/key-copy that can fail and not rolling back.
- Rehashing by old bucket number instead of reducing the full hash for the new capacity.
- Looking only in the new table during incremental migration, or inserting duplicates across both tables.
- Assuming load factor must stay below one; chaining permits `α>1`, though cost grows.
- Calling expected O(1) a worst-case guarantee under hash flooding.
- Treating a linked chain as cache-friendly because bucket lookup itself is constant-time.
- Depending on bucket/iteration order that changes after head insertion, resize, seed, or treeification.

### Compact example

With five buckets and identity hashes, keys 0,5,10 all select bucket zero while key 2 selects bucket two, so lengths are `3,0,1,0,0`. Updating key 5 changes its value without changing size. Rehashing to eleven buckets places all four keys separately. Deleting 10 leaves keys 0,2,5, size three, and consistent placement. This finite trace proves exact operations only.

### Connections

[DSE-021](021-hash-functions-and-distribution.md) supplies equality, hashing, reduction, and threat assumptions. [DSE-015](015-doubly-and-intrusive-linked-lists.md) supplies link/ownership reasoning. The [program roadmap](../ROADMAP.md) next compares open-addressed linear, quadratic, and double-hash probing.

## Governing Question

Which bucket representation, operation semantics, allocation policy, load threshold, migration protocol, and evidence make a separately chained table correct and predictable for its real keys and runtime?

## Why This Matters

Collisions are inevitable. Separate chaining makes them explicit by giving every bucket a secondary container. Unlike open addressing, entries need not occupy the primary bucket array, and the table can hold more entries than buckets. Deletion can be direct because it removes a bucket-container entry rather than preserving a probe path.

The apparent simplicity hides systems choices. A linked node costs pointers, allocations, and cache misses. An array bucket shifts entries. A tree bin needs ordering and more metadata. Resizing can pause the world or maintain two tables. Iterator/reference stability depends on whether nodes move. Allocators, callback failures, duplicate policy, concurrency, and hostile chain growth can dominate the textbook hash computation.

This module therefore treats “chain” as an owned bucket container with a contract, not automatically a singly linked list. It separates semantic correctness—which must survive a constant hash—from distribution-dependent performance and attack resistance.

## Prerequisites and Retrieval

Before continuing, retrieve:

- ADT, representation, and failure contracts from [DSE-001](001-abstract-data-types-and-concrete-representations.md), [DSE-002](002-representation-invariants.md), and [DSE-003](003-operation-contracts.md);
- cost, allocation, layout, and cache models from [DSE-004](004-time-space-and-allocation-cost.md), [DSE-005](005-contiguous-and-linked-layouts.md), and [DSE-006](006-memory-locality-and-cache-behavior.md);
- generic key/value, iterator, testing, and measurement discipline from [DSE-007](007-genericity-and-type-constraints.md), [DSE-008](008-iterators-and-traversal-protocols.md), [DSE-009](009-property-based-testing-of-data-structures.md), and [DSE-010](010-benchmarking-a-structure-without-misleading-results.md);
- linked-node lifetime/deletion from [DSE-014](014-singly-linked-lists.md) and [DSE-015](015-doubly-and-intrusive-linked-lists.md);
- equality, canonical encoding, distribution, universal hashing, reduction, and HashDoS from [DSE-021](021-hash-functions-and-distribution.md).

## Learning Objectives

After completing this module, you should be able to:

1. define the abstraction and representation invariants of a separately chained map;
2. derive lookup, unique insert/update, multi-insert, deletion, and clear operations;
3. analyze expected chain work from load while preserving worst-case bounds;
4. compare linked, contiguous, small-vector, tree, and intrusive bucket containers;
5. design stop-the-world and incremental resize protocols with failure safety;
6. specify allocation, key/value ownership, cached hash, and callback behavior;
7. state iteration, reference, duplicate, ordering, and serialization contracts;
8. separate chain hardening, hash randomization, resource limits, and worst-case alternatives;
9. design safe synchronization/reclamation for supported concurrency topologies;
10. test and benchmark semantic, distribution, lifecycle, migration, and hostile cases.

## Core Exposition

**Begin with the map abstraction.** A unique map is a finite mapping from key-equivalence classes to values. `find(k)` returns the value whose stored key is equivalent to k; `insert(k,v)` either adds, rejects, or returns existing state; `insert_or_assign` adds or replaces; `erase(k)` removes at most one; and `clear` removes all. A multimap permits multiple values per class and must define range/order/erase-one/erase-all behavior.

The table owns an array of m bucket roots or descriptors. When m is zero under lazy allocation, operations must initialize or report empty before reducing modulo m. For m>0, a key's bucket is derived from the full hash using the current reduction. Every candidate still needs equality: full-hash or fingerprint mismatch can reject early, but equality confirms a hit.

Storing a cached full hash in each node can help expensive keys, rehashing, and equality filtering. It costs bytes and must reflect the immutable key and active hash function/seed. If a rehash changes only m, reduce the cached hash again. If it changes hashing, recompute from the key.

**Lookup scans one bucket container.** Compute/canonicalize/hash k, reduce to i, then search Bi. For a linked list, compare cached hash if present and equality for surviving candidates. Return not-found only after the entire relevant bucket has been examined. Under migration, “relevant” may include old and new tables.

If chain length is L, bucket scanning is O(L) comparisons plus key/hash work. Under simple uniform hashing, expected L for an arbitrary bucket is α=n/m. An unsuccessful query independent of stored keys therefore sees expected α entries. Successful-search constants depend on how entries are ordered, insertion timing, query frequencies, and whether a match is promoted; do not memorize `1+α/2` without its assumptions.

Worst case is max chain length n. Randomized hashing gives expected protection under a declared adversary model, not semantic correctness or an absolute latency bound. Tree bins, balanced fallback structures, or globally ordered maps can improve collision worst cases subject to their comparison contracts.

**Unique insertion is lookup plus a transaction.** First search for an equivalent key. If found, reject or update according to the named operation; do not allocate a duplicate. If absent, allocate/construct owned key/value/node, then link it and increment n at a commit point. If hash/equality/allocation/key-copy/value construction can fail, specify which calls occur and how partial resources are destroyed.

Head insertion into a singly linked bucket is constant link work: new.next=old_head, then bucket=new. It reverses per-bucket admission order and can improve access to recent inserts, but neither is a portable map promise. Tail insertion preserves bucket insertion order at extra traversal or tail metadata. Self-referential keys/values and reentrant callbacks can invalidate naive transaction reasoning; libraries commonly constrain callback behavior.

`insert_or_assign` must decide key retention: keep the existing stored key and replace only value, or replace both under a specified API. Value construction before destructive replacement can provide a stronger guarantee. If replacement itself can throw/fail, document basic versus strong failure guarantees.

**Deletion rewires exactly one membership edge.** In a singly linked chain, maintain a link-to-current pointer (bucket head or predecessor's next). On match, set that link to current.next, decrement n, then destroy/release under a safe order. This handles head and interior uniformly. A two-phase unlink API can detach without destruction so callbacks run after structure coherence is restored.

Deletion from a multimap must define whether it removes first, all equivalent entries, a provided iterator, or an exact key-value pair. Returning an iterator after erase needs a traversal rule. Destroying a key/value can invoke user code in some runtimes, so internal links and counters should already describe a coherent table.

`clear` walks every bucket and destroys every entry once. Failure-throwing destructors are generally prohibited or fatal in low-level container contracts. Clearing a node chain recursively can overflow the call stack; use iteration. A partial clear after callback interruption needs an explicit state or should forbid reentrancy.

**Bucket representation determines real cost.** A singly linked node offers constant head insertion and relinking, possibly stable node addresses, and simple intrusive use. It pays one next pointer per entry, often one allocation per node, fragmentation, pointer chasing, and poor prefetching. An intrusive chain makes membership links part of client objects and separates object ownership, but duplicate membership requires distinct hooks.

A dynamic-array bucket improves density and traversal but may allocate per bucket, move/shift entries, and invalidate references. Small-vector buckets keep a few entries inline and spill when needed, trading bucket-array size and move complexity for fewer allocations. A global entry arena with per-bucket indices can improve locality but introduces index/free-list/generation lifetime rules.

Balanced-tree bins bound comparisons when a bucket grows, assuming a stable strict ordering or tie-breaker coherent enough for navigation. Hash-equivalent keys may not be naturally orderable. Current OpenJDK `HashMap` source uses ordinary linked bin nodes and can treeify under implementation-specific conditions; those thresholds/layouts are private current details, not the Java `Map` abstraction or a rule for other chained tables.

**Load factor can exceed one.** Since entries live outside the bucket array, n>m is representable. But higher α means more comparisons, larger chains, and less parallelism across buckets. A resize threshold balances bucket-array memory, node overhead, cache effects, allocation latency, and workload. Empty buckets cost roots/pointers; too many buckets can make iteration over capacity expensive.

Track not only average α but maximum chain length, percentiles/histogram, equality comparisons, bytes hashed, and hot-bucket frequency. Weighted request skew can make one modest chain dominate latency. A threshold copied from an open-addressed table or another runtime is not evidence.

**Stop-the-world resize is a commit protocol.** Choose new capacity with checked arithmetic and policy limits. Allocate/zero a new bucket array. For every old entry, compute its new bucket from the full hash and new m, then link/move it. Finally publish the new array/count and release the old bucket array.

Node-based chains can relink existing nodes without moving keys/values, preserving node addresses under a stated contract. But mutating old links during migration means allocation or callback failure after partial movement needs recovery. A robust approach performs every fallible action before destructive relinking, uses nonthrowing link operations, or records which buckets have moved. If new allocation fails, the old table should remain valid.

Iteration order usually changes because bucket number and chain order change. Iterators commonly invalidate on rehash even when entry references remain stable; use the exact library contract. Serialization should store logical key/value entries under a defined format, not raw bucket links/capacity unless those are explicitly versioned representation data.

**Incremental rehashing maintains two placements.** Allocate a new table and migration cursor/state. New inserts go to the new table. Lookup/delete/update may need both, unless the old bucket is marked migrated. A migration step detaches one old bucket and redistributes all its nodes before marking it complete. No key may be logically lost or duplicated.

If operation budgets migrate “one bucket,” a hostile bucket may contain O(n) entries and cause a long pause. Budget by entries/time or harden chain length, while ensuring eventual progress through empty regions. Current Redis dictionary source explicitly uses chaining, two tables, a rehash cursor, bounded empty-bucket visits, operation-assisted migration, and rehash pausing for iterators. It is valuable current production evidence, not a universal implementation template.

During migration, inserting a key that remains in old storage must find/update it rather than add a duplicate in new storage. Deletion must remove from whichever table owns it. Size is logical across both. Iterators/sampling require pause, versioning, duplicate suppression, or a documented weak behavior. Shrink and seed changes have distinct triggers and costs.

**Iteration and order are separate contracts.** A traversal typically visits bucket array order and then each chain. Head insertion, deletion, resize, seed randomization, treeification, allocator behavior, and migration can change it. If clients need insertion order, maintain a separate global list as `LinkedHashMap`-style metadata or select an ordered map; this adds update/erase and concurrency invariants.

Weakly consistent concurrent iteration, fail-fast bug detection, snapshot iteration, and locked iteration are different. OpenJDK documents best-effort fail-fast behavior as unsuitable for correctness. C++ unordered requirements specify observable bucket/rehash/invalidation behavior without requiring separate chaining as the private layout.

**Hash flooding needs layered defense.** A public weak hash plus linked chains permits attacker-controlled long chains and potentially quadratic aggregate insertion. Secret/keyed randomized hashes reduce predictability under their assumptions. Tree bins cap comparison depth if ordering and transformations are safe. Request/key/entry/CPU limits bound resources. Collision metrics and latency alerts provide detection.

No single layer proves safety. An adaptive attacker may learn a seed; equality can be expensive; all keys can be extremely long; allocation can exhaust memory; tree comparisons can be attacker-costly. The primary Crosby-Wallach work demonstrates algorithmic-complexity risk. Threat review names attacker control, seed disclosure, worst-case operations, limits, and fallback.

**Concurrency changes ownership.** A single table lock is simplest and makes resize atomic but serializes operations. Bucket locks improve parallelism until resize changes the array; a table-level migration lock/version or cooperative protocol must coordinate. Lock striping maps many buckets to stable locks and needs deterministic lock ordering for multi-bucket operations.

Lock-free reads over mutable linked chains require atomic publication, safe deletion, and memory reclamation such as epochs/hazards; merely making bucket heads atomic creates use-after-free and traversal races. Resizing publishes a new root while readers may hold old nodes. Use a mature concurrent map or a clearly proved topology rather than adding atomics locally.

**Evidence keeps correctness independent of distribution.** Compare against a simple language map under generated put/update/get/delete/clear/reserve/rehash sequences. Inject a constant hash, equality collisions, allocation failures, throwing callbacks where supported, and duplicate keys. Inspect all entries, exact size, per-bucket placement, link acyclicity, source ownership, cached hashes, and old/new migration state after every operation.

Force m=0/1, empty/singleton, delete head/middle/tail, all keys in one bucket, α below/at/above thresholds, maximum capacity arithmetic, grow/shrink, repeated rehash, and migration interleavings. Test iterators/references against documented invalidation and destructors with counted resources. Concurrent validation adds history checking, race/memory tools, stalled threads, resize overlap, cancellation, and reclamation delays.

Benchmarks include hits/misses, key size/cost, hash quality, α sweep, chain distributions, update ratios, deletes, reserve, stop-the-world and incremental resize, full iteration, allocator choice, memory/node bytes, comparisons, cache misses, throughput, and p50/p95/p99/max latency. Compare linked, compact bucket, open addressing, and ordered alternatives under the same semantics and workload.

The executable trace below uses Python lists as bucket chains so representation is inspectable. It provides no allocation, pointer, concurrency, or production-performance evidence.

<!-- bijux-verify: {"id":"separate-chaining-operation-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"before_lengths=3,0,1,0,0\nbefore_max_chain=3\nupdated=FIVE\nafter_rehash_max_chain=1\ndeleted=ten\nkeys=0,2,5\nsize=3\ninvariant=True\nevidence=finite_separate_chaining_trace\n","stderr":""}} -->
```python
class ChainedMap:
    def __init__(self, bucket_count):
        if bucket_count <= 0:
            raise ValueError("bucket count must be positive")
        self.buckets = [[] for _ in range(bucket_count)]
        self.size = 0

    def _index(self, key):
        return hash(key) % len(self.buckets)

    def put(self, key, value):
        bucket = self.buckets[self._index(key)]
        for index, (stored_key, _) in enumerate(bucket):
            if stored_key == key:
                bucket[index] = (stored_key, value)
                return False
        bucket.insert(0, (key, value))
        self.size += 1
        return True

    def get(self, key):
        for stored_key, value in self.buckets[self._index(key)]:
            if stored_key == key:
                return value
        raise KeyError(key)

    def delete(self, key):
        bucket = self.buckets[self._index(key)]
        for index, (stored_key, value) in enumerate(bucket):
            if stored_key == key:
                del bucket[index]
                self.size -= 1
                return value
        raise KeyError(key)

    def rehash(self, bucket_count):
        if bucket_count <= 0:
            raise ValueError("bucket count must be positive")
        entries = [entry for bucket in self.buckets for entry in bucket]
        self.buckets = [[] for _ in range(bucket_count)]
        old_size = self.size
        self.size = 0
        for key, value in entries:
            assert self.put(key, value)
        assert self.size == old_size

    def invariant(self):
        keys = []
        for index, bucket in enumerate(self.buckets):
            for key, _ in bucket:
                if self._index(key) != index:
                    return False
                keys.append(key)
        return len(keys) == self.size and len(set(keys)) == self.size


table = ChainedMap(5)
for key, value in ((0, "zero"), (5, "five"), (10, "ten"), (2, "two")):
    assert table.put(key, value)
before = [len(bucket) for bucket in table.buckets]
assert not table.put(5, "FIVE")
print("before_lengths=" + ",".join(map(str, before)))
print(f"before_max_chain={max(before)}")
print(f"updated={table.get(5)}")
table.rehash(11)
print(f"after_rehash_max_chain={max(map(len, table.buckets))}")
print(f"deleted={table.delete(10)}")
keys = sorted(key for bucket in table.buckets for key, _ in bucket)
print("keys=" + ",".join(map(str, keys)))
print(f"size={table.size}")
print(f"invariant={table.invariant()}")
print("evidence=finite_separate_chaining_trace")
```

## Definitions and Notation

- `m`: positive bucket count when reduction occurs.
- `n`: logical entry count across one or both migration tables.
- `Bi`: secondary container for bucket i; `Li=|Bi|`.
- `α=n/m`: average chain length/load factor for one active placement.
- `Lmax=max Li`: worst bucket length under list/array scanning.
- **unique map**: at most one entry per key-equivalence class.
- **multimap**: permits multiple entries per class under specified range/removal ordering.
- **bucket root/link**: ownership edge from bucket metadata or predecessor to an entry.
- **tree bin**: balanced ordered structure used within a bucket under collision pressure.
- **migration cursor/state**: indicates which old buckets are authoritative, moving, or complete.
- **rehash**: placement rebuild; may change capacity, seed/hash, or both.

## Mechanisms, Invariants, or Proof Structure

The representation proof shows every live entry occurs once, in the bucket selected by the active placement, and unique-key equality classes do not duplicate. Lookup correctness follows because it examines every candidate in the selected bucket and equality confirms the class. Insert/delete preserve the abstraction by adding/removing exactly one representative at a commit point.

Expected work derives from `sum Li=n`, so average bucket length is α; probability models from DSE-021 justify expected query-bucket length only under their assumptions. Worst-case work uses Lmax, never α alone.

Stop-the-world rehash proves a bijection between old live entries and new live entries plus correct new placement before publication. Incremental rehash strengthens this with per-bucket authority: entries are in exactly one physical table, operations search every possible authoritative location, and marking migrated happens only after all entries move.

Ownership proof covers fallible construction before linking, unlink-before-destroy, allocator pairing, cached-hash validity, iterator/reference rules, callback/reentrancy assumptions, and safe reclamation after concurrent readers.

## Alternatives and Trade-Offs

| Bucket/table design | Strength | Cost or obligation |
|---|---|---|
| Singly linked chains | simple relink/delete, stable nodes possible | allocation, next pointer, cache misses, O(L) scan |
| Contiguous bucket arrays | dense scan/locality | shifts, per-bucket allocation, invalidation |
| Inline-small bucket | common short chains avoid allocation | larger bucket array, spill/move complexity |
| Treeified long bins | logarithmic comparison depth under premises | ordering/tie rules, metadata, conversion complexity |
| Intrusive chains | no wrapper allocation; explicit membership | client layout/lifetime, hook uniqueness |
| Stop-the-world resize | simplest authority state | O(n) latency spike, failure transaction |
| Incremental resize | distributes migration latency | two-table operations, budgets, iterator complexity |
| Open addressing | compact/local for many workloads | probe/deletion/load constraints, relocation |
| Ordered tree map | deterministic order and worst-case log n | more comparisons/pointers; no expected O(1) |

## Failure Modes and Misconceptions

- **“Collision means overwrite.”** Only equivalent keys update; non-equivalent colliders coexist.
- **“Hash match means key match.”** Equality is still mandatory.
- **“Separate chaining means linked list.”** The bucket container is a design choice.
- **“Load factor above one is invalid.”** It is valid but raises average chain work.
- **“Average α proves every bucket short.”** Skew/adversaries can make Lmax=n.
- **“Head insertion preserves insertion order.”** It reverses local admission order and resize can reorder again.
- **“Rehash uses old bucket indices.”** New capacity requires reduction of full hashes.
- **“Relinking nodes cannot fail.”** allocation/hash/callback/seed changes may be fallible before links move.
- **“Incremental means constant latency.”** one old bucket can itself be huge.
- **“Stable node address means stable iterator.”** container contracts may invalidate traversal state independently.
- **“Atomic bucket heads make lock-free deletion safe.”** traversal and reclamation remain unsolved.
- **“Tree bins eliminate HashDoS.”** key cost, comparison, memory, adaptive attacks, and other operations remain.

## Worked Examples

### Example 1

With m=5, hashes 0,5,10 select bucket zero. Lookup 5 checks 10 then 5 after head insert. Conclusion: collisions coexist and equality terminates the scan.

### Example 2

A unique-map `put(5,new)` finds stored key 5 and replaces its value without adding a node or incrementing n. Conclusion: duplicate policy changes the transaction.

### Example 3

Deleting the head of `10→5→0` changes the bucket root to 5; deleting 5 changes 10's or root-current link depending on prior state. A link-to-current algorithm handles both. Conclusion: membership-edge ownership simplifies deletion.

### Example 4

For n=120,m=100, α=1.2 is valid. Under the uniform model an unsuccessful scan has expected chain work proportional to 1.2, although some chains are longer. Conclusion: chaining need not reserve empty primary slots.

### Example 5

A constant hash creates Lmax=n. Every key remains retrievable through equality, but a missing lookup scans all n. Conclusion: semantic correctness and expected performance are separable.

### Example 6

Growing from m=8 to 16, an entry with full hash 13 moves from bucket 5 to bucket 13. Copying old bucket 5 is wrong. Conclusion: rehash reduces the full hash under new capacity.

### Example 7

During incremental rehash, key K remains in an unmigrated old bucket. An insert that searches only new storage adds a duplicate. Conclusion: authority state determines lookup/update scope.

### Example 8

A migration budget of one bucket encounters a million-entry hostile chain and pauses for a million relinks. Conclusion: bucket-count budgets do not bound entry work.

### Example 9

Linked nodes use one allocation and next pointer per entry; a compact bucket array scans colliders contiguously but shifts on erase. Conclusion: identical ADT/asymptotics can have different memory behavior.

### Example 10

A reader holds node X while a writer unlinks and frees it through an atomic head update. The reader follows freed `next`. Conclusion: publication without reclamation is not a concurrent-map proof.

## Cross-Program Connections

- [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) owns striped locking, linearizability, atomic publication, and reclamation.
- [Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) connects allocators, intrusive nodes, cached hashes, callbacks, failure, and lifetime.
- [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) connects map/update/duplicate semantics and ownership boundaries.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) connects expected/worst-case chain analysis, tree bins, migration budgets, and benchmarks.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) connects hash indexes/joins, bucket overflow, partitioning, spill, and skew.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) connects hot keys, skew metrics, repartitioning, and memory budgets.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns HashDoS, keyed hashing, resource limits, hostile equality cost, and telemetry.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) connects incremental migration, dual authority, and versioned placement.

## References

1. ISO C++ working draft, [Unordered Associative Container Requirements](https://eel.is/c%2B%2Bdraft/unord.req.general). Observable equality/hash, buckets, load, rehash, complexity, and invalidation contract without mandating private chaining layout.
2. Oracle, [Java SE 25 `HashMap`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/HashMap.html). Current map semantics, capacity/load guidance, distribution assumption, ordering, synchronization, and iterator limitations.
3. OpenJDK Project, [`HashMap.java`](https://github.com/openjdk/jdk/blob/master/src/java.base/share/classes/java/util/HashMap.java). Current linked/tree bin implementation, resize, thresholds, node links, iteration, and invariants; private details are version-specific.
4. Redis Project, [`dict.h`](https://github.com/redis/redis/blob/unstable/src/dict.h). Current primary source declaring power-of-two chained tables, dictionary types, rehash state, entry links, callbacks, and specialized storage.
5. Redis Project, [`dict.c`](https://github.com/redis/redis/blob/unstable/src/dict.c). Current primary source for chained lookup/update/delete, resize arithmetic, two-table incremental migration, budgets, pause, and failure handling.
6. Linux Kernel documentation, [Linked Lists](https://docs.kernel.org/core-api/list.html). Current intrusive list/hlist structure, iteration, deletion, concurrency cautions, and hash-table-oriented hlist motivation.
7. J. Lawrence Carter and Mark N. Wegman, [Universal Classes of Hash Functions](https://citeseerx.ist.psu.edu/document?doi=d8777ef17c18609781aa889055100603b13b2986&repid=rep1&type=pdf). Primary randomized-hashing foundation for input-independent expected behavior.
8. Scott A. Crosby and Dan S. Wallach, [Denial of Service via Algorithmic Complexity Attacks](https://www.usenix.org/legacy/event/sec03/tech/full_papers/crosby/crosby.pdf). Primary hash-chain worst-case attack evidence and layered-defense motivation.
9. Rust Project, [`HashMap`](https://doc.rust-lang.org/std/collections/struct.HashMap.html). Current open-addressed alternative, randomized default, key-mutation restriction, capacity, iteration, and API contracts.
10. Abseil Project, [Swiss Tables Design Notes](https://abseil.io/about/design/swisstables). Current compact open-addressed alternative using control metadata, illustrating why node chaining is not the only collision design.

## Exercises

### Exercise 1

Specify unique-map separate chaining, including equality, full-hash caching, ownership, insert/update/delete, and failure guarantees.

### Exercise 2

Derive average chain length and expected unsuccessful lookup work, then state why successful and worst-case costs require more assumptions.

### Exercise 3

Design deletion and clear for intrusive singly linked chains with key/value destructor callbacks and reentrancy restrictions.

### Exercise 4

Design incremental grow/shrink for a chained map, including authority, operation routing, budgets, iterators, allocation failure, and completion.

### Exercise 5

Prepare a production comparison of linked chaining, treeified bins, compact bucket arrays, and open addressing under hostile and ordinary workloads.

## Answers to the Exercises

### Answer 1

Define stable equivalence and require equal keys to share the full hash. Each owned node contains immutable key, value, optional cached full hash, and membership link; bucket array and allocator own nodes unless an explicit intrusive policy says otherwise. `find` reduces the active hash and tests hash then equality across the full bucket. `insert` searches first, constructs all fallible key/value/node state off-table, links once, then increments n; failure destroys partial state and preserves the old table. `insert_or_assign` keeps the stored key and commits a safely constructed replacement value under a named strong/basic guarantee. `erase` redirects the owning link, decrements n, then runs destruction under a no-reentrancy or post-coherence rule. Cached hashes invalidate if key/hash seed changes; indexed key fields cannot mutate. Constant-hash tests prove semantics independent of distribution.

### Answer 2

Because `sum Li=n`, the arithmetic average across m buckets is α=n/m. Under an unsuccessful query whose selected bucket is uniform/independent of stored placement, expected inspected entries are `sum_i (1/m)Li=n/m=α`, plus key hashing/reduction. A successful lookup's position depends on insertion order, query distribution, temporal correlations, and bucket organization; `1+α/2` needs specific uniform/list assumptions. Worst case uses `Lmax`, which can equal n under a constant/adversarial hash. Universal/randomized assumptions give expectations over function choice, not absolute per-operation latency or cryptographic safety.

### Answer 3

Give each object a dedicated nonshared hash-membership hook or forbid simultaneous membership. Maintain a pointer/reference to the link that owns current (bucket root or predecessor next). On match, save successor and required destructor inputs, redirect the owning link, decrement logical/bucket counts, and mark/detach the hook before invoking callbacks. Then release value/key according to ownership; object memory is client-owned for a purely intrusive table. For clear, iteratively detach an entire bucket or node one at a time, restore coherent counts/roots, then invoke callbacks—never recurse through an attacker-long chain. Forbid callbacks from mutating the same table, or queue destruction after structural mutation with explicit lifetime guards. Test head/middle/tail, singleton, self-removal attempts, counted destruction, and constant-hash chains.

### Answer 4

Allocate the new bucket array before changing authority; on failure keep the old table. Record old/new arrays, capacities, logical total size, and per-old-bucket cursor/state. New inserts target new storage but first search any authoritative old bucket to prevent duplicates. Lookup/update/delete search new plus old unless that old bucket is marked complete. A step marks a bucket moving, relinks a bounded number of entries by new reduction, and marks complete only when empty; entry/time budgets prevent one long chain from violating latency and operations ensure eventual progress. Size counts entries once. Iterators either pause migration, snapshot/version, or document weak behavior and prevent duplicates. Completion atomically publishes new as sole table and frees old bucket storage only after readers/iterators are excluded. Shrink uses the same authority proof; changing hash/seed requires recomputation, not cached placement alone.

### Answer 5

Fix identical equality, key/value ownership, update semantics, security profile, and workload traces. Linked chaining favors simple stable nodes but pays allocation/pointer/cache costs. Compact buckets favor scans but move entries. Treeified bins offer logarithmic collision comparison under ordering/tie premises but add conversion/metadata. Open addressing favors density/locality but has probe, deletion, load, and relocation constraints. Model-test all with constant hashes, duplicates, deletes, failures, resize, iterators, and resource lifetimes. Benchmark realistic key sizes/skew, hits/misses, update/delete ratios, α/capacity sweeps, collision attacks, resize/migration, iteration, allocator, memory, comparisons/probes, cache misses, CPU, throughput, and latency tails. Security review covers keyed hashing, adaptive attackers, limits, equality/key cost, and fallback. Choose from end-to-end evidence and auditability; do not generalize OpenJDK/Redis/Abseil thresholds or a microbenchmark.
