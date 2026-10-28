---
module_id: DBE-034
program: Database Engineering
level: 1
module_number: 34
title: Hash Indexes
status: complete
last_verified: 2026-08-30
---

# Hash Indexes

## One-Page Review

### Governing question

When does mapping an equality key to a bucket produce a correct, durable, and predictably efficient database access path, and how must the structure grow when collisions and skew make one bucket too large?

### Essential definitions

A **hash function** maps a normalized index key to a fixed-width hash code. A **bucket function** maps that code and current table metadata to a logical bucket. A **collision** occurs when unequal keys share a code or bucket; correctness requires equality recheck. A bucket has a **primary page** and possibly **overflow pages**. **Load factor** relates occupied capacity to allocated bucket capacity, but does not describe skew or chain tails. **Extendible hashing** uses a directory of hash-bit prefixes, a global depth, and per-bucket local depths; it doubles the directory only when splitting a bucket whose local depth equals global depth. **Linear hashing** grows without a full directory by maintaining a level and split pointer, splitting buckets in a deterministic round. A **split state** names old/new buckets and tuple-movement status so reads and recovery remain correct while redistribution is incomplete.

### Central model, mechanism, or theorem

Normalize the lookup key exactly as insertion did, compute stable `H(k)`, derive bucket `b=f(H(k),metadata)`, validate/scan every page belonging to that bucket, and accept only entries whose full indexed value satisfies the equality semantics. Expected constant-time access requires assumptions about hash distribution, bounded load, metadata access, overflow, cache, concurrency, and adversarial input; the worst case is linear in entries concentrated in one bucket. Dynamic schemes split incrementally: extendible hashing refines one directory prefix; linear hashing splits the bucket named by a moving split pointer, not necessarily the bucket that overflowed.

### Critical invariants

- Insertion and lookup use the same type normalization, collation/equality, hash function version, seed, and bucket metadata generation.
- Equality-compatible keys hash compatibly; hash equality never proves value equality unless the representation explicitly guarantees it.
- Every live entry is in the bucket(s) the current or declared split-state mapping tells a reader to inspect.
- Collision and duplicate runs are scanned without prematurely returning absent or only one match.
- Extendible directory references agree with local-depth prefixes; each local depth is at most global depth.
- Linear-hashing level/split-pointer arithmetic assigns every code to exactly one current bucket.
- Overflow chains are acyclic, incarnation-checked, bounded by corruption defenses, and safely reclaimed.
- Split publication, tuple movement, cleanup, WAL, and metadata changes define readable crash states.
- Logical deletion, physical tuple cleanup, overflow unlink, and page reuse remain distinct.
- Optimizer capability and cost claims match the actual engine/index/operator class, not the word “hash.”

### Common failures

Failures include assuming `hash(a)=hash(b)` implies `a=b`; hashing raw bytes while equality uses normalized values; changing seed/function/collation without rebuild; using a hash index for range/order/prefix operations; trusting average load while one bucket has a long chain; confusing extendible with linear split selection; doubling an extendible directory unnecessarily; publishing new metadata before buckets are readable; losing/duplicating tuples during concurrent split; stopping at the primary page; reclaiming an overflow page still pinned; treating expected `O(1)` as a latency guarantee; and exposing a denial-of-service collision path.

### Compact example

With two-entry buckets and one directory bit, keys use low bits of identity hash. Bucket A receives 0 and 2. Insert 4 overflows A; because A's local depth equals global depth 1, double the directory to depth 2 and split A: directory `(A,B,C,B)`, A has `(0,4)`, C has `(2)`. Later depth is 3 and B still has local depth 1; overflowing B splits it to local depth 2 without doubling the directory. Directory entries sharing B's refined prefix are redirected to E. This is extendible hashing—not linear hashing's split-pointer rule.

### Connections

This module contrasts DBE-031–033's ordered B+ tree with equality-oriented hashing. DBE-035 treats multicolumn/payload design; DBE-037–039 address selectivity, statistics, and maintenance cost. Storage, buffers, WAL, and integrity come from DBE-021–030.

## Governing Question

The governing question has three parts. **Semantic correctness:** do insertion and lookup agree on equality and normalization? **Structural correctness:** can every current or splitting bucket be found exactly as the protocol declares? **Performance fitness:** does the workload actually consist of selective equality probes with a controlled collision/overflow distribution?

A hash index is not “a dictionary, but on disk.” Disk pages, MVCC versions, duplicate locators, variable-width encodings, metadata caching, incremental growth, WAL, concurrent scans, deletion, and hostile keys turn a one-line array formula into a storage protocol. The right design states which layer provides each guarantee.

## Why This Matters

Equality lookup is common: primary identifiers, session tokens, exact device IDs, deduplication keys, and join/build tables. Hashing can avoid comparator-driven tree descent and store compact codes. But a B+ tree already supports equality while also supporting ranges and order. A persistent hash index earns its write/space/recovery cost only when measured equality behavior, key width, cache, concurrency, and engine capabilities justify it.

Hash structures also teach a general systems lesson: expected complexity is conditional. Uniform independent codes plus controlled load can yield short bucket access; skewed equivalence classes or attacker-chosen collisions create long scans and hot locks. Production design therefore connects mathematical distribution assumptions to instrumentation, resource bounds, seed/version policy, and rebuild procedures.

## Prerequisites and Retrieval

Retrieve exact equality, NULL, collation, and duplicate semantics from DBE-011–020. Retrieve slotted pages and overflow risks from [DBE-023](023-slotted-pages.md), pins/latches/identity from [DBE-026](026-buffer-pools.md), write-ahead recovery from [DBE-028](028-dirty-pages-and-writeback.md), and validation from [DBE-029](029-checksums-and-page-corruption.md). Compare ordered navigation in [DBE-032](032-b-tree-search-and-range-scan.md) and multi-page mutation in [DBE-033](033-b-tree-insertion-splitting-and-deletion.md).

Before continuing, distinguish hash code, bucket number, and physical page number. Explain the pigeonhole principle: a fixed-width code over a larger key domain must permit collisions. Recall that SQL equality, an index operator class's equality, and raw byte identity need not be the same relation.

## Learning Objectives

After completing this module, you should be able to:

1. derive a correct equality probe from normalization through full recheck;
2. distinguish code collisions, bucket collisions, duplicate keys, and MVCC versions;
3. analyze static buckets and overflow-chain behavior beyond average load;
4. trace extendible directory doubling, local-depth split, lookup, and optional merge;
5. trace linear-hashing level/split-pointer addressing and incremental expansion;
6. separate logical buckets from primary, overflow, bitmap, and metadata pages;
7. design concurrent split/read/cleanup and WAL/recovery states;
8. reason about hash stability, adversarial inputs, NULL/collation/composite semantics;
9. compare hash and B+ tree access paths for real query shapes; and
10. construct differential, structural, crash, concurrency, and workload evidence.

## Core Exposition

Start with an equality relation `~` defined by the index operator semantics. A valid hash support function obeys `a~b => H(a)=H(b)`. The converse normally fails. Case-insensitive equality, canonical Unicode, numeric representations, signed zero, NULL policy, composite-field delimiters, and collation versions must be handled consistently. If a hash function distinguishes values the equality operator considers equal, a lookup can miss a valid row and the index is unsound.

Insertion encodes/normalizes key `k`, computes fixed-width `h=H(k)`, derives logical bucket `b=f(h,M)` from metadata `M`, and inserts a locator or entry into that bucket's page set. Lookup repeats those exact steps, scans candidate entries with matching stored code where available, then rechecks full equality against the indexed/base value. An index that stores only code and locator cannot prove equality or answer an index-only query by itself.

There are two collision layers. A **hash-code collision** gives the same full code to unequal keys. A **bucket collision** gives a shared bucket to different codes because the table currently uses only some bits/modulus. Duplicate logical keys are neither: they intentionally compare equal and may have several row locators/versions. Correct lookup searches the entire relevant run/chain and applies visibility and residual checks to each candidate.

A static hash file has `B` primary buckets and often chooses `h mod B` or selected bits. It is simple when cardinality is known and stable. Growth without reorganization raises load and overflow. A global resize can allocate a new table and redistribute all entries—clean and cache-friendly after completion, but expensive, space-hungry, and coordination-heavy for a large persistent index.

Overflow pages let a bucket grow locally. They avoid immediate global rebuild and handle transient skew, but every link adds page access, latch/pin work, corruption surface, fragmentation, and tail latency. Average load factor can look healthy while one hot bucket has a hundred pages. Track chain-length distribution and maximum, not merely total entries divided by primary capacity.

Extendible hashing interprets hash bits as a directory index. Global depth `g` means `2^g` directory entries. A bucket's local depth `d<=g` says how many low or high bits—choose and document one—identify its prefix. A bucket with depth `d` is referenced by `2^(g-d)` directory slots. Lookup reads the `g` selected bits and follows one slot.

On overflow, if `d<g`, allocate a sibling, increase the old/new local depth to `d+1`, redirect half of directory references according to the new distinguishing bit, and redistribute using `d+1` bits. The directory size does not change. If `d=g`, first double the directory by duplicating references, increment `g`, then perform the same local split. Only the overflowing bucket's entries move.

Deletion may permit buddy merge when both buckets have the same local depth, share all but the distinguishing bit, and combined contents fit. Directory references collapse to one bucket and local depth decreases; if no bucket needs global depth `g`, the directory can halve. Many systems delay or omit shrinking to avoid oscillation and synchronization. Merge is policy, not part of equality correctness.

Linear hashing avoids an exponential directory. Let a base bucket count be `N`, level `i`, split pointer `p`, `h_i(x)=H(x) mod (N*2^i)`, and `h_(i+1)` double that modulus. Compute `b=h_i(x)`; if `b<p`, recompute with `h_(i+1)` because that earlier bucket has already split this round. Growth splits bucket `p`, creates bucket `p+N*2^i`, redistributes with `h_(i+1)`, increments `p`, and when `p=N*2^i`, resets `p=0` and increments `i`.

This yields gradual expansion without a full directory. Crucially, the bucket split next is selected by `p`, not necessarily the one that overflowed. Overflow pages absorb imbalance until its turn. A load-triggered implementation may initiate one or several controlled splits. Linear hashing therefore trades directory memory for arithmetic metadata and potentially longer temporary chains.

PostgreSQL's current hash implementation is a concrete linear-style disk design, not the executable extendible model below. Its metadata maps bucket numbers to physical locations despite interspersed overflow/bitmap pages. It may cache metadata and revalidate against bucket state. It uses primary bucket, overflow, bitmap, and metapages; index pages sort entries by hash code for local search. Its current documentation states that hash indexes support equality and can use overflow pages when a bucket fills.

SQL query capability is narrower than physical code lookup. Hash order has no useful relationship to `<`, `>`, `BETWEEN`, prefix order, `ORDER BY`, `MIN/MAX`, merge join, or adjacent-key pagination. A set of `IN` equalities can issue multiple probes, but a numeric range cannot be scanned by walking neighboring buckets. Composite equality can hash an entire tuple; omitting a component generally changes the indexed expression and cannot use that composite hash directly.

NULL behavior is engine/operator specific. A query predicate `x=NULL` is not SQL equality; `IS NULL` may or may not be supported by a hash operator class. Unique indexes often allow multiple NULLs depending on product semantics. Never infer NULL behavior from the hash formula. The same applies to nondeterministic collations and types with multiple representations that compare equal.

The hash algorithm must be stable for the lifetime/version of the index unless every entry is rebuilt. Process-randomized language hashes are usually unsuitable for persistent layouts without persisted seed and version. Changing collation/equality or hash support code can invalidate bucket placement. Upgrade paths need compatibility declarations, catalog versioning, validation, `REINDEX`/rebuild, and rollback.

Adversarial collision resistance and fast database hashing are related but not identical goals. A public attacker who can choose keys may target known weak functions, exhausting CPU/I/O or a bucket latch. A secret per-index/process seed can frustrate precomputed collisions, but persistence/replication and recovery must reproduce it. Strong cryptographic hashing costs more and still cannot fix a genuinely skewed logical key with millions of duplicates. Bound chain scans, rate-limit, monitor, and choose a design from the threat model.

Concurrency needs stable metadata and bucket ownership. A reader may cache `M`, compute a bucket, latch/pin it, and discover that a split made the cache stale. The protocol must let it revalidate/recompute or inspect both old/new buckets. A writer serializes the affected bucket transformation, publishes initialized pages and split state, moves or copies entries under defined flags, updates metadata, and completes cleanup. Latches need a global order; cleanup must respect active pins/scans.

PostgreSQL's source design illustrates explicit split states: old bucket being split, new bucket being populated, moved-by-split tuples, and a later split-cleanup condition. A reader can inspect both buckets according to flags, and a partial split can be completed later. This is one implementation protocol, not a universal recipe. Extendible, linear, copy-on-write, and in-memory concurrent hash tables have different publication/linearization proofs.

WAL treats allocation, entry insertion/movement, split-state transitions, metadata updates, overflow linking/unlinking, and cleanup as recoverable actions. Dirty pages need not persist together. Every crash boundary must retain a mapping under which reads know where candidates can exist, and redo must be idempotent by page identity/LSN. Space allocated before metadata commit may be a recoverable orphan/reservation, not silently reusable.

Deletion first obeys transaction visibility. Removing a row version does not necessarily permit immediate index entry removal. Later garbage collection deletes known-dead entries, compacts pages, squeezes overflow chains, updates counts, and retires pages. Reuse requires pin/epoch/generation safety. Some implementations grow bucket count but do not shrink it; do not promise a merge merely because a textbook variant defines one.

Cost decomposes into hash computation, metadata/directory access, primary page access, within-page code scan, overflow pages, candidate equality/visibility/base fetches, cache/storage misses, latches/retries, and output. Expected `O(1)` suppresses distribution/load assumptions and constant factors; worst-case lookup is `O(n)` candidates. A B+ tree of small height with hot upper pages may beat a hash index, so benchmark the actual engine and query mix.

Observability records operator/index version, normalized predicate shape, hash function/seed version (not secret value), bucket generation, primary/overflow pages visited, candidates and equality rechecks, visible/returned rows, chain-length histogram/max, load and byte occupancy distribution, splits and split lag, directory/global/local depths or linear level/pointer, metadata refresh/retries, latch waits, WAL/dirty bytes, garbage/reclamation debt, and p50/p99. Hash codes and keys may be sensitive; aggregate or redact.

Testing uses a reference multimap keyed by the exact equality relation. Differentially compare inserts, deletes, updates, equality probes, duplicates, NULL/type/collation boundaries, and missing keys. Force every directory/local-depth or level/split-pointer boundary. Inject colliding codes, skew, maximum encodings, corrupt/looping chains, stale metadata, interrupted split, crash at each WAL action, concurrent scans/cleanup, and page reuse. Audit all bucket/directory/allocation metadata for exact reachability, no cycles, and permitted transient duplication only.

The executable model is a single-threaded in-memory extendible hash set with identity integer hash, low-bit directory, two-entry buckets, and no deletion. It demonstrates directory doubling, splitting, lookup, a later split without directory doubling, and stable invariants. It does not model linear hashing, overflow pages, duplicate values, SQL equality/NULL, MVCC, concurrency, WAL, disk pages, attacks, or production performance.

<!-- bijux-verify: {"id":"extendible-hash-splits","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"after_4=(depth=2,directory=('A', 'B', 'C', 'B'),buckets=(('A', 2, (0, 4)), ('B', 1, ()), ('C', 2, (2,))))\nafter_8=(depth=3,directory=('A', 'B', 'C', 'B', 'D', 'B', 'C', 'B'),buckets=(('A', 3, (0, 8)), ('B', 1, ()), ('C', 2, (2, 6)), ('D', 3, (4,))))\nafter_5=(depth=3,directory=('A', 'B', 'C', 'E', 'D', 'B', 'C', 'E'),buckets=(('A', 3, (0, 8)), ('B', 2, (1, 5)), ('C', 2, (2, 6)), ('D', 3, (4,)), ('E', 2, (3,))))\nlookups=(0, 1, 2, 3, 4, 5, 6, 8)\ninvariants=True\n","stderr":""}} -->
```python
CAPACITY = 2
global_depth = 1
directory = ["A", "B"]
buckets = {
    "A": {"depth": 1, "keys": []},
    "B": {"depth": 1, "keys": []},
}
next_name = iter(("C", "D", "E", "F", "G"))


def index_for(key: int) -> int:
    return key & ((1 << global_depth) - 1)


def view() -> tuple[int, tuple[str, ...], tuple[tuple[str, int, tuple[int, ...]], ...]]:
    states = tuple(
        (name, buckets[name]["depth"], tuple(buckets[name]["keys"]))
        for name in sorted(buckets)
    )
    return global_depth, tuple(directory), states


def split(name: str) -> None:
    global global_depth, directory
    old_depth = buckets[name]["depth"]
    if old_depth == global_depth:
        directory = directory + directory
        global_depth += 1
    new_name = next(next_name)
    new_depth = old_depth + 1
    buckets[name]["depth"] = new_depth
    buckets[new_name] = {"depth": new_depth, "keys": []}
    split_bit = 1 << old_depth
    for slot in range(len(directory)):
        if directory[slot] == name and slot & split_bit:
            directory[slot] = new_name
    old_keys = buckets[name]["keys"]
    buckets[name]["keys"] = []
    for key in old_keys:
        target = directory[index_for(key)]
        buckets[target]["keys"] = sorted(buckets[target]["keys"] + [key])


def insert(key: int) -> None:
    while True:
        name = directory[index_for(key)]
        keys = buckets[name]["keys"]
        if key in keys:
            return
        if len(keys) < CAPACITY:
            buckets[name]["keys"] = sorted(keys + [key])
            return
        split(name)


def contains(key: int) -> bool:
    name = directory[index_for(key)]
    return key in buckets[name]["keys"]


def valid() -> bool:
    if len(directory) != 1 << global_depth:
        return False
    for name, bucket in buckets.items():
        depth = bucket["depth"]
        if depth > global_depth or len(bucket["keys"]) > CAPACITY:
            return False
        references = [slot for slot, target in enumerate(directory) if target == name]
        if len(references) != 1 << (global_depth - depth):
            return False
        signature = references[0] & ((1 << depth) - 1)
        if any(slot & ((1 << depth) - 1) != signature for slot in references):
            return False
        if any(directory[index_for(key)] != name for key in bucket["keys"]):
            return False
    return True


for value in (0, 2, 4):
    insert(value)
after_4 = view()
for value in (6, 8):
    insert(value)
after_8 = view()
for value in (1, 3, 5):
    insert(value)
after_5 = view()
lookups = tuple(value for value in range(9) if contains(value))

print(f"after_4=(depth={after_4[0]},directory={after_4[1]},buckets={after_4[2]})")
print(f"after_8=(depth={after_8[0]},directory={after_8[1]},buckets={after_8[2]})")
print(f"after_5=(depth={after_5[0]},directory={after_5[1]},buckets={after_5[2]})")
print(f"lookups={lookups}")
print(f"invariants={valid()}")
```

## Definitions and Notation

Let equality be `~`, normalized encoding be `E(k)`, fixed-width hash be `H(E(k)) in [0,2^w)`, metadata snapshot be `M`, and bucket function be `f(h,M)`. Correctness requires `a~b => H(E(a))=H(E(b))` and lookup using a metadata/split state that covers every possible current location.

Let `n` be entries, `B` primary buckets, `C` usable bucket capacity, load `alpha=n/(B*C)` in a simplified fixed-width model, chain length `L_b`, candidates `c`, pages `q`, and retries `r`. Equality cost is better described by hash/metadata plus `q`, `c`, visibility/base access, and `r` than by the slogan `O(1)`.

For extendible hashing, `g` is global depth and `d_b` bucket local depth. Directory references to `b` equal `2^(g-d_b)` in stable state. For linear hashing with base `N`, level `i`, and pointer `p`, current bucket count is `N*2^i+p`; use `h_i`, but recompute with `h_(i+1)` when the first result is below `p`.

## Mechanisms, Invariants, or Proof Structure

A defensible equality probe is:

1. Bind snapshot, index incarnation, equality/operator class, normalization, hash/seed version, and metadata generation.
2. Normalize and hash the complete indexed key; derive candidate bucket under the declared dynamic scheme.
3. Pin/latch/version-check the primary page and refresh/retry when cached metadata is stale.
4. Interpret split flags and inspect old/new bucket sets exactly as the protocol requires.
5. Traverse every validated overflow page with cycle/hop/identity bounds.
6. Compare stored code, then full indexed value/base row; apply MVCC visibility and residual semantics.
7. Return every qualifying duplicate for non-unique lookup, or enforce uniqueness under transaction rules.
8. Release resources and record pages, candidates, retries, split observations, and limitations.

Extendible stable-state correctness follows because each directory slot names one prefix class and split refines one class by the next bit. Directory doubling copies all old references, so unchanged buckets preserve membership; redirecting half the old bucket's references and redistributing all its entries preserves exact coverage. This is a proof sketch under a deterministic complete hash and stable directory. Concurrent publication, failure, visibility, and reclamation require separate proof.

Linear addressing is exhaustive because buckets below `p` have already been refined with `h_(i+1)`, while buckets at/above `p` still use `h_i`; the two cases partition the current round. When `p` reaches the old round size, every bucket uses the next modulus, so advancing `i` and resetting `p` preserves mapping.

## Alternatives and Trade-Offs

Static hashing minimizes metadata but requires planned capacity or global rebuild. Extendible hashing moves only the overflowing prefix bucket and offers direct addressing, but the directory can grow and become a shared/cache/persistence concern. Linear hashing keeps small metadata and spreads growth, but overflow on a hot bucket may persist until its split turn. Cuckoo, Robin Hood, hopscotch, and learned/concurrent in-memory tables have different relocation and persistence contracts; a DBMS index name does not imply one.

Hash indexes specialize equality and can compact wide values into codes, but require collision recheck and lack useful key order. B+ trees support equality plus range/order and provide predictable logarithmic structure. Bitmap/inverted indexes serve low-cardinality/set or token queries. An in-memory execution hash table for join/aggregation is ephemeral operator state, not automatically the same as a durable secondary hash index.

## Failure Modes and Misconceptions

- “Equal hash means equal key.” It produces candidates, not proof.
- “Different bytes mean unequal.” Collation/type normalization may define equality across representations.
- “Load factor predicts lookup.” It hides bucket skew and overflow-chain maximums.
- “Extendible hashing always doubles.” It doubles only when the split bucket's local depth equals global depth.
- “Linear hashing splits the overflowing bucket.” It normally splits the current pointer bucket.
- “Adjacent buckets mean adjacent keys.” Hash bucket order has no range semantics.
- “A composite hash supports any prefix.” Hashing the whole tuple generally requires full-tuple equality.
- “The application hash can be persisted.” Randomization/version changes may move every key.
- “A secret seed solves duplicates.” Identical logical keys still share a bucket.
- “The primary page contains the bucket.” Overflow and in-progress new/old buckets may also be required.
- “Metadata cache is harmless.” Stale depth/pointer state can route to an old bucket unless revalidated.
- “Split completion is one page write.” Publication, moves, metadata, cleanup, and WAL span actions.
- “Deleted means reusable.” Visibility, active scans, pins, and incarnation safety intervene.
- “Expected constant time guarantees p99.” Storage, chains, cache, locks, retries, and rechecks dominate.

## Worked Examples

### Example 1

Case-insensitive equality says `"Ada"~"ADA"`. Hashing raw case-sensitive bytes to different codes makes one representation unfindable through the other's probe. Normalize consistently or use an equality-compatible support function. Conclusion: hash correctness begins with semantics, not distribution.

### Example 2

Keys 7 and 23 have different full codes but both map modulo 8 to bucket 7. This is a bucket collision, so scanning code fingerprints can reject one cheaply. If their full codes also collide, only full equality distinguishes them. Conclusion: both collision layers require correct recheck boundaries.

### Example 3

One hundred buckets average 60% full, but one adversarial bucket owns 40 overflow pages. The global load appears healthy while that equality probe has terrible p99 and latch contention. Conclusion: monitor chain distributions and hottest buckets, not average load alone.

### Example 4

In the executable model, A overflows at depth `d=g=1`; the directory doubles before A splits. At global depth 3, B has local depth 1, so its split increases local depth to 2 without directory growth. Conclusion: local and global depth answer different questions.

### Example 5

Linear hashing has `N=2,i=1,p=1`, hence five buckets. For a code with `h_i=0`, bucket 0 was already split because `0<p`, so recompute modulo 8; result may be bucket 4. For `h_i=2`, use bucket 2 directly. Conclusion: the split pointer is part of every lookup mapping.

### Example 6

Query `WHERE x BETWEEN 10 AND 20` cannot walk buckets in numeric order; hashing destroys adjacency. Eleven equality probes cover only a small discrete integer domain and are not a general range algorithm. Conclusion: choose an ordered access path for interval semantics.

### Example 7

A split has copied some tuples to new bucket B while old A retains originals. Split flags tell a reader which buckets and moved markers to consider so it neither misses nor incorrectly duplicates results. Conclusion: transient duplication is safe only with an explicit read protocol.

### Example 8

Crash follows durable new-bucket allocation and some move records but precedes split completion. Redo recreates the named state; lookup consults old/new as flags require; a later writer completes cleanup. Conclusion: incomplete does not mean corrupt when replay and readers share the state machine.

### Example 9

One logical value has a million row versions/duplicates. A perfect hash sends them to the same equality bucket, whose scan remains huge. Posting compression, MVCC cleanup, partitioning, or another physical design is needed. Conclusion: distribution cannot separate values that must compare equal.

### Example 10

A B+ tree equality probe touches three hot/cached levels and one leaf; a hash probe reads cold metadata, primary page, and two overflow pages. The tree wins despite `O(log n)` versus expected `O(1)`. Conclusion: compare measured page/candidate/concurrency costs on the actual engine.

## Cross-Program Connections

- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies hashing, collision resolution, dynamic dictionaries, and adversarial analysis.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies expected/worst-case analysis, distribution assumptions, and differential testing.
- [Programming Languages — Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies publication, version validation, latches, and reclamation.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies collision denial-of-service, secret management, and threat models.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies caching, page I/O, persistence, and recovery ordering.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies consistent hashing as a related but distinct node-placement problem.

## References

1. Ronald Fagin, Jürg Nievergelt, Nicholas Pippenger, and H. Raymond Strong, [Extendible Hashing—A Fast Access Method for Dynamic Files](https://dl.acm.org/doi/10.1145/320083.320092), *ACM Transactions on Database Systems* 4(3), 1979.
2. Witold Litwin, [Linear Hashing: A New Tool for File and Table Addressing](https://www.sigmod.org/publications/dblp/db/conf/vldb/Litwin80.html), *VLDB*, 1980, pp. 212–223.
3. PostgreSQL Global Development Group, [Hash Indexes](https://www.postgresql.org/docs/current/hash-index.html), current bucket, overflow, equality, size, split, and metapage guidance.
4. PostgreSQL Global Development Group, [Hash Index README](https://github.com/postgres/postgres/blob/master/src/backend/access/hash/README), current addressing, locking, split states, garbage collection, free-space, and WAL protocol.
5. PostgreSQL Global Development Group, [Hash Index Source](https://github.com/postgres/postgres/tree/master/src/backend/access/hash), current implementation and tests.
6. PostgreSQL Global Development Group, [Index Types](https://www.postgresql.org/docs/current/indexes-types.html), current operator/access-method capability overview.
7. Oracle, [MySQL 8.4 MEMORY Storage Engine](https://dev.mysql.com/doc/refman/8.4/en/memory-storage-engine.html), current HASH/BTREE capability and workload cautions.
8. Oracle, [Comparison of B-Tree and Hash Indexes](https://dev.mysql.com/doc/refman/8.4/en/index-btree-hash.html), current MySQL equality/range capability distinctions.
9. Goetz Graefe, [Modern B-Tree Techniques](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/p669-graefe.pdf), hash-versus-tree and storage-index design context.
10. Ramakrishnan and Gehrke, *Database Management Systems*, 3rd ed., McGraw-Hill, 2003, static, extendible, and linear hashing foundations.

## Exercises

### Exercise 1

For global depth 2 and directory `(A,B,C,B)` with local depths `A=2,B=1,C=2`, verify directory-reference counts/prefixes and route codes 0 through 7 using low bits.

### Exercise 2

Trace linear hashing from `N=2,i=0,p=0` through five bucket splits. After each split, give bucket count, `i`, `p`, and routing for codes 0 through 11.

### Exercise 3

Design a persistent hash equality operator for case-insensitive composite `(tenant,email)` keys with NULL policy. Specify encoding, delimiter/length safety, collation version, seed/hash version, collision recheck, upgrade, and rebuild behavior.

### Exercise 4

Design a concurrent, crash-recoverable bucket split with overflow pages. State reader/writer metadata validation, old/new visibility, latching order, WAL actions, idempotence, cleanup, and reclamation.

### Exercise 5

Design an experiment comparing a hash index and B+ tree for equality, `IN`, range, duplicate-heavy, adversarial, and mixed read/write workloads. State correctness oracle, variables, metrics, and decision rule.

## Answers to the Exercises

### Answer 1

At `g=2`, A and C each have `d=2`, so each must have `2^(2-2)=1` directory reference: slot 0 (`00`) and slot 2 (`10`) respectively. B has `d=1`, so it has two references with low-bit signature 1: slots 1 (`01`) and 3 (`11`). Codes use their low two bits: 0→A, 1→B, 2→C, 3→B, 4→A, 5→B, 6→C, 7→B. This verifies reference counts and prefix consistency, not capacity or entry correctness.

### Answer 2

Initially two buckets, `i=0,p=0`, modulus 2. Split 0 creates bucket 2, then `p=1`; lookups whose mod-2 result is 0 recompute mod 4. Split 1 creates 3; the round completes, so `i=1,p=0`, four buckets, all use mod 4. Split 0 creates 4 and sets `p=1`; mod-4 result 0 recomputes mod 8. Split 1 creates 5, `p=2`; results 0 or 1 recompute mod 8. Split 2 creates 6, `p=3`; results 0,1,2 recompute mod 8. Thus after five splits there are seven buckets with `i=1,p=3`. For codes 0–11: 0→0,1→1,2→2,3→3,4→4,5→5,6→6,7→3,8→0,9→1,10→2,11→3. Bucket 3 has not yet split in the current round.

### Answer 3

Define whether NULL participates (`IS NOT DISTINCT FROM`-like) or is excluded; do not reuse ordinary SQL `=` implicitly. Encode tenant with fixed width or length prefix, email after equality's case/collation normalization with an unambiguous length, and include field/null tags. Persist equality/collation identifier and version plus hash algorithm and seed identifier; protect any secret seed while making recovery/replicas deterministic. Require equal normalized tuples to hash equally, but fetch/recheck both full components because collisions remain. Reject incompatible opens or mark the index invalid after collation/hash change; rebuild all entries under the new version, validate against a reference scan, and keep rollback to the prior compatible index until cutover evidence passes.

### Answer 4

Persist index/bucket generations and split identity. A writer locks under one global order, allocates/initializes and WAL-logs the new page/overflow chain, marks old/new split state, then copies/moves entries with redo-identifiable records. Publish metadata only when readers can interpret both locations; readers latch/version-check computed buckets, refresh stale metadata, and inspect old/new plus markers exactly once according to protocol. Log completion separately and defer deleting old copies until active scans cannot need them. Cleanup compacts chains, unlinks retired overflow pages, and reuse waits for pin/epoch/generation safety. Recovery replays each state idempotently by LSN/incarnation; crash tests cover every record boundary and replay twice. A concrete engine must prove its chosen linearization and deadlock order.

### Answer 5

Use identical table data, snapshots, semantics, memory/storage limits, durability, and a reference full scan/sorted multimap to verify every result including NULLs, collisions, duplicates, visibility, and order. Vary cardinality, selectivity, key width, distribution/skew, duplicate/version count, chain length, cache cold/warm, equality versus `IN` width, ranges/order, read/write ratio, concurrency, collision attacks, growth, and storage. Record plans, hash/tree/overflow pages, candidates/rechecks/base fetches, cache/I/O/CPU, splits, WAL/write amplification, size, latch waits/retries, throughput, and p50/p99. Warm up and repeat with controlled seeds; inject maintenance/recovery. Choose hash only if supported semantics and measured equality benefit outweigh range/order loss and maintenance/tail/security cost across declared thresholds. Do not generalize beyond the tested engine/version/hardware/workload.
