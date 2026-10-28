---
module_id: DSE-040
program: Data Structures Engineering
level: 1
module_number: 40
title: Skip Lists
status: complete
last_verified: 2026-08-30
---

# Skip Lists

## One-Page Review

### Governing question

How can a layered ordered linked structure use randomized heights to obtain logarithmic expected search and update while preserving exact ordering, range, memory, concurrency, and evidence contracts?

### Essential definitions

- A **skip list** is a sorted base linked list plus progressively sparser forward-link levels over the same nodes.
- A node's **height** is the number of levels in which it participates; every node has height at least one.
- A **tower** is the collection of one node's forward links across its levels.
- A **promotion probability** `p` independently continues a tower to the next level, normally until failure or a configured maximum.
- A **header/sentinel** precedes every legal key and carries links for all configured levels.
- A **search path** moves right while the next key remains before the target, then moves down one level.
- The **update/predecessor array** records the last node before a target at every level and is reused for insertion or deletion.
- An **indexable skip list** stores spans or widths on links so rank and select can skip known counts.
- A **linearization point** is the instant a concurrent operation takes effect in its abstract history.
- **safe reclamation** prevents a removed node from being freed while a reader could still dereference it.

### Central model, mechanism, or theorem

With independent promotion probability `0<p<1`, a node reaches level `k` with probability approximately `p^(k-1)`. The expected number of forward links per node is `1/(1-p)`, and the highest occupied level is logarithmic with high probability. Search reverses the construction: at each level it moves across a geometrically spaced sample, then descends. Expected search, insertion, and deletion take `O(log n)` comparisons for fixed `p`, while ordered range output costs `O(log n+k)` for `k` results.

These are randomized bounds, not deterministic worst-case guarantees. A realized or adversarially influenced height pattern can degenerate to a linked list. Correctness never depends on good randomness: base order and cross-level subsequence invariants prove answers. Randomness controls performance only.

### Critical invariants

1. Level zero contains every live node in strict total key order under the declared duplicate policy.
2. Each higher level is an ordered subsequence of the level below, and a link at level `i` targets a node of height greater than `i`.
3. Header links above the current top level are empty; configured maximum and node height are in range.
4. Search never skips a key that could satisfy the target because it moves right only while the next key is strictly before the boundary.
5. Insert/delete update every affected level exactly once and maintain size, top-level, backward/tail, or span metadata when present.
6. Random-level generation has specified probability, entropy source, cap, reproducibility hooks, and adversarial model.
7. Concurrent publication initializes immutable fields before release-linking reachability; deletion separates logical marking, physical unlinking, and reclamation.
8. Serialization, persistence, and recovery validate ordering and bounds or rebuild from logical entries.

### Common failures

- Treating expected logarithmic time as deterministic worst-case time.
- Off-by-one confusion between height count and zero-based highest level.
- Moving right on `<=target` when searching for the first key `>=target`.
- Allowing duplicate keys without a composite ordering or explicit multimap policy.
- Updating only the base link during deletion and leaving higher dangling links.
- Forgetting to lower the current top after its final node is removed.
- Choosing a maximum level too small, too large, or with unchecked allocation arithmetic.
- Using predictable/adversarially controllable promotion bits when performance is security-sensitive.
- Adding spans without updating every crossed width on insert/delete.
- Freeing an unlinked concurrent node before all possible readers have quiesced.

### Compact example

A deterministic seven-node layout uses heights `4,1,2,3,1,2,3` for keys `10,20,25,30,35,40,50`. Its level populations are `7,5,3,1`. Search finds 25, lower-bound 26 returns 30, and range `[20,40)` returns `20,25,30,35`. Deleting 30 updates three levels, yielding populations `6,4,2,1`; a validator checks base order and every higher-level subsequence.

### Connections

[DSE-007](007-genericity-and-type-constraints.md), [DSE-009](009-property-based-testing-of-data-structures.md), and [DSE-010](010-benchmarking-a-structure-without-misleading-results.md) supply comparator and evidence disciplines. [DSE-031](031-binary-search-trees.md) through [DSE-035](035-splay-trees.md) provide ordered-tree alternatives. The [program roadmap](../ROADMAP.md) continues with graph layouts, adjacency engineering, tries, suffix structures, and disjoint sets.

## Governing Question

Which ordering, height distribution, maximum level, duplicate/range policy, memory layout, publication protocol, reclamation scheme, persistence boundary, and workload evidence justify a sequential, concurrent, or storage-engine skip list?

## Why This Matters

Skip lists implement ordered maps and sets, lower/upper bounds, range scans, predecessor/successor queries, and sometimes rank/select. Their algorithms are visually close to linked-list traversal and local splicing, yet their expected performance competes with balanced trees under suitable randomness. They appear in in-memory database structures, storage-engine memtables, concurrent navigable maps, sorted sets, schedulers, and indexing layers.

Their apparent simplicity can mislead. The probabilistic proof requires independent height choices and a fixed promotion model. Duplicate keys and composite comparators can silently break navigation. Variable-size towers complicate allocation. Rank spans create a second arithmetic invariant. Concurrent insertion must publish multiple links coherently enough for readers; deletion must not reclaim nodes prematurely. Storage-engine implementations may deliberately never delete individual nodes and reclaim the whole arena later, which changes the concurrency proof.

Skip lists are also an excellent case study in separating correctness from performance. Even a height-one degeneration remains a correct sorted list if its links are valid. Randomization proves likely path length, not answer validity. This separation makes tests clearer: structural and model checks establish correctness; distribution tests and benchmarks provide bounded evidence about performance assumptions.

## Prerequisites and Retrieval

Retrieve representation invariants and corruption diagnosis from [DSE-002](002-representation-invariants.md), probability-sensitive cost language from [DSE-004](004-time-space-and-allocation-cost.md), and linked layout/cache behavior from [DSE-005](005-contiguous-and-linked-layouts.md) and [DSE-006](006-memory-locality-and-cache-behavior.md). Retrieve strict comparator requirements from [DSE-007](007-genericity-and-type-constraints.md), property/model checking from [DSE-009](009-property-based-testing-of-data-structures.md), and benchmark design from [DSE-010](010-benchmarking-a-structure-without-misleading-results.md). Retrieve ordered-map semantics from [DSE-031](031-binary-search-trees.md), randomized-priority reasoning from [DSE-034](034-treaps.md), and concurrency/ownership cautions from [DSE-039](039-indexed-and-meldable-priority-queues.md).

## Learning Objectives

After completing this module, you should be able to:

1. define a skip-list ordered-map contract including bounds, duplicates, ranges, and iteration;
2. derive search, insertion, and deletion from the predecessor path;
3. state and prove base-order and higher-level subsequence invariants;
4. derive expected tower space and logarithmic expected search for fixed promotion probability;
5. distinguish expectation, high-probability behavior, and deterministic worst-case degeneration;
6. select promotion probability and maximum level from space/comparison/cache trade-offs;
7. extend links with spans for rank/select and state the additional update proof;
8. explain current Redis, RocksDB, LevelDB, and Java skip-list choices without assuming identical contracts;
9. specify concurrent logical/physical deletion, memory ordering, ABA defense, and safe reclamation;
10. design deterministic structural, statistical, fault, concurrency, persistence, and production benchmark evidence.

## Core Exposition

**Start with the ordered dictionary.** Let keys be governed by a strict total order or a strict weak order plus a tie policy that yields total placement. Decide whether the structure is a set, unique-key map, or multimap. Define `find`, `lower_bound` (first key not less than target), `upper_bound` (first key greater than target), predecessor, successor, insertion/update, deletion, and half-open range `[low,high)`.

Iteration normally follows level zero and therefore has sorted order. An iterator's mutation guarantees—fail-fast, snapshot, weakly consistent, or externally synchronized—are separate. Empty bounds, unbounded endpoints, reverse iteration, and comparator-equivalent but unequal keys need explicit behavior. A result range costs at least the number `k` of emitted entries.

**The representation is a hierarchy of samples.** Every node appears in level zero. A height-two node additionally appears in level one; height `h` supplies forward pointers indexed `0..h-1`. The header has the configured maximum height and a conceptual key before all legal keys. Some implementations also keep a tail and base-level backward pointers for reverse traversal.

At each higher level, fewer nodes remain. Think of an express transit line: traverse long gaps at a high level, descend near the target, and finish on the complete local line. Unlike a balanced tree, the skip list does not rotate or store child subtrees. It maintains several linked subsequences over identical ordered nodes.

Choose one vocabulary and stick to it. This module calls a one-pointer node height 1 and its highest level 0. A four-pointer node has height 4 and highest level 3. Some papers and code call the highest index the “level,” producing an off-by-one shift. Translate at the boundary, especially when allocating flexible arrays or configuring a maximum.

**Search is monotone right then down.** Begin at the header's highest occupied level. While the next node at this level has key strictly less than the target, move right. Otherwise descend. After level zero, `current.forward[0]` is the first node whose key is at least the target, or null. Equality decides `find`; returning the candidate implements lower bound.

Why is it correct? At every level, `current.key<target` (or current is header), and the next link is absent or not less than target. Moving right preserves the first condition because the tested key is still below target. Descending cannot reveal an omitted qualifying node before current: higher levels are subsequences of the ordered base, and current's base position is already known to precede target. At level zero, no unvisited node lies between current and candidate.

For upper bound, advance while the next key is less than or equivalent to target under the declared key equality. For composite duplicate ordering, lower/upper search should use synthetic minimum/maximum tie components or explicit comparator functions rather than scattering equality exceptions through loops.

**Insertion reuses the search path.** During top-down search, record `update[i]`, the last node at level `i` whose key is before the insertion point. Check the level-zero successor for duplicate policy. Generate the new node's height. If it exceeds the current occupied height, set new `update` entries to the header and raise the current height.

For every node level `i`, set `new.forward[i]=update[i].forward[i]`, then `update[i].forward[i]=new`. This two-link splice preserves the ordered subsequence because the predecessor is before the new key and the old successor follows it. Levels above the node height remain unchanged. Increment logical size only after successful publication under the sequential contract.

If duplicates are forbidden, reject comparator equality or replace the value without changing tower height according to policy. If duplicates are allowed, order by `(user_key,stable_sequence)` or another unique secondary key. Searching by user key then uses lower/upper sentinels for the secondary field. A linked collection of equal values is another design, with different range and deletion costs.

Allocating a variable-height node can use a flexible trailing pointer array, one allocation for header plus levels, or a fixed maximum array per node. Flexible nodes save expected pointer space but require checked size arithmetic and alignment. Fixed arrays waste memory but simplify ownership. Separate tower objects add indirection. Store large values indirectly when copying/moving them through lifecycle operations is expensive.

**Deletion must unlink every level where the node appears.** Search and record predecessors. Let `target=update[0].forward[0]`. If it is absent or unequal, report not found. For each level of the target, if the predecessor points to it, bypass it. Higher levels cannot point to a shorter node. Then lower the current occupied height while the header's top link is null, decrement size, update tail/backward/span metadata, and reclaim only under the applicable lifetime protocol.

A sequential implementation may free immediately when no iterators or handles borrow the node. A fail-fast iterator can use a modification counter. A stable iterator may require refcounted nodes, copy-on-write versions, or a documented restriction. Deleting only at level zero leaves reachable nodes at upper levels; searches can return freed memory or keys absent from iteration.

**Random height supplies balance statistically.** A common generator starts at height one and promotes while independent Bernoulli trials succeed, capped by `max_height`. With promotion probability `p`, `Pr[height>=h]=p^(h-1)` before capping. Therefore expected pointers per uncapped node are `sum_{h>=1}Pr[height>=h]=1/(1-p)`. At `p=1/2`, the expectation is two forward pointers; at `p=1/4`, it is `4/3`.

Expected population at level index `i` is `n*p^i`. The level where this becomes constant is about `log_{1/p} n`. The maximum height exceeds `c log_{1/p} n` with probability bounded by a union bound over nodes: `n*p^(c log_{1/p} n)=n^(1-c)` up to indexing/cap constants. This supplies a high-probability height bound for `c>1`.

Search analysis can run backward from the target. At a level, the expected number of horizontal steps before encountering a tower that rises is geometric, roughly `1/p`; the expected number of levels is logarithmic. For fixed `p` away from zero and one, expected search is `O(log n)`. Precise constants depend on the model, maximum level, and boundary effects. The original analysis gives sharper bounds.

Worst case is still `O(n)`: every node may receive height one, or an unfortunate sparse arrangement may force a long base scan. Randomization makes that unlikely under independent private choices. It does not turn the worst case logarithmic. A deterministic skip list or balanced tree is appropriate when hard worst-case bounds are required, though deterministic variants have different update rules.

**Promotion probability trades levels against width.** With smaller `p`, towers use fewer pointers and levels, but horizontal gaps widen. With larger `p`, searches make fewer horizontal moves per level but traverse more levels and allocate more links. The comparison-cost approximation includes both `1/p`-like horizontal work and `log_{1/p} n` vertical work; cache misses and pointer bytes alter the optimum.

Pugh discussed values such as one-half and one-quarter; current systems make their own trade-offs. RocksDB's inline skip list exposes a branching factor and maximum height, stores keys inline for locality, and documents its concurrency constraints. Redis uses a capped random level and also stores spans/backward links for sorted-set rank and reverse traversal. Do not copy constants without measuring node/key sizes and workload.

Choose `max_height` so the expected population at the top is comfortably below one for the maximum supported `n`, while bounding header/node allocation and loops. A cap that is too low makes the top level dense at scale and worsens searches. A huge cap enlarges header/update arrays and exposes arithmetic/stack limits without benefit. Treat capacity growth beyond the design maximum as an explicit error, rebuild, or accepted degradation.

**Randomness is part of the performance contract.** State the generator, seeding, independence approximation, and whether tests can inject heights. A deterministic seed makes failures reproducible but may let an attacker learn future heights. Key insertion order and random height should be independent; deriving height from a weak public function of the key can permit constructed degeneration.

For untrusted workloads, use a keyed pseudorandom mapping or protected generator if probabilistic performance is security-relevant, rotate keys only with a rebuild policy, and cap all work/memory regardless. A cryptographic generator may be unnecessary overhead for trusted local data; the threat model decides. Statistical tests cannot prove independence, but they can detect gross bias, cap errors, or broken seeds.

Deterministic tests should inject explicit heights so every topology and deletion boundary is reproducible. Separately test the production generator over fixed recorded seeds and large samples: population ratios, mean height, cap frequency, and confidence intervals. Never make structural correctness tests probabilistically flaky.

**Indexable skip lists add distance algebra.** Store with each forward link a span: the number of level-zero nodes crossed by that link under one declared convention. During search, accumulating spans yields rank. Select by rank moves right only when adding the next span does not overshoot. Redis's sorted-set skip list maintains spans for rank operations.

Insertion records both predecessors and cumulative ranks. Splitting a predecessor link divides its old span between predecessor-to-new and new-to-successor; untouched higher levels crossing the insertion point increment by one. Deletion joins spans around the removed node and decrements crossing spans. An off-by-one convention can return plausible ranks while corrupting boundary results, so define whether spans count destination, edges, or intervening base nodes.

Span validation independently walks level zero to assign true positions, then recomputes every link's distance. Span addition and total length can overflow fixed counters. Rank/select adds space and mutation writes; omit spans when only ordered lookup/range scan is needed.

**Split, concatenate, and bulk build are not automatically cheap.** A search path can identify a split boundary, but every crossing level must be rewired and ownership defined. Concatenation is valid only when all left keys precede all right keys under compatible comparators; finding tail/predecessors and reconciling top levels costs work. Random heights can be retained if nodes move unchanged, but headers, arenas, and concurrency metadata complicate transfer.

Bulk building from sorted entries can generate heights then maintain a tail pointer per level, linking each node once for expected linear work. Validate strict order and duplicates first. If building an indexable variant, compute spans from known base positions. This can be more deterministic and cache-friendly than repeated insertion.

**Memory behavior differs from balanced trees.** Expected forward-pointer count is linear, but each allocation carries headers, alignment, allocator metadata, key/value, optional backward pointer, spans, marks, and concurrency fields. Tall variable nodes fragment size classes. Pointer chasing across separately allocated nodes is often cache-unfriendly compared with sorted vectors or B-tree pages.

Arena allocation can pack nodes and make destruction constant-time for the whole arena. It also means individual deletes may only mark/unlink, not return memory. RocksDB's documented design keeps nodes until the skip list is destroyed, greatly simplifying lock-free reads and reclamation but matching its append-oriented memtable lifecycle. A general mutable map cannot assume that lifecycle.

Inline keys save one pointer and improve locality but require size/alignment calculation and immutable key bytes after publication. Prefix compression is harder than in page structures because forward links target independent nodes. NUMA placement, allocator contention, and pointer width matter at large scale.

**Current production examples intentionally differ.** Redis sorted sets combine a dictionary for member lookup with a skip list ordered by score and member. Duplicate scores are allowed but members are unique through the surrounding dictionary; composite comparison supplies total placement. Forward spans support rank, and backward/tail links support reverse traversal. The skip list is one component of the zset contract, not a standalone universal map.

LevelDB uses a skip list for its memtable and relies on an arena-like lifetime and external synchronization assumptions. RocksDB's evolved inline skip list documents nonconcurrent `Insert`, concurrent insertion routes, release publication, immutable node contents after linking, and no node deletion until whole-list destruction. Those choices are tied to an LSM memtable that becomes immutable and flushes.

Java's `ConcurrentSkipListMap` implements a concurrent navigable map. Its current API documents expected average logarithmic operations, weakly consistent iterators, ascending views faster than descending ones, and nonconstant size under concurrency. It forbids null keys/values and defines atomic concurrent-map operations. A sequential pointer splice does not reproduce these semantics.

**Concurrency multiplies the proof surface.** A coarse mutex around search/update is the baseline: simple linearization and immediate reclamation after no readers, with contention. Fine-grained locks may lock predecessor/successor links by a global order and validate that the recorded window remains adjacent. Optimistic/lazy algorithms find a window, lock or CAS relevant nodes, validate marks/links, publish, and retry on interference.

Insertion commonly initializes the new node fully, links level zero at its linearization point, then installs higher-level index links. A reader that misses a new upper link can still descend and find the node at level zero; an upper link must never expose uninitialized lower state. Release/acquire ordering and immutable keys make this argument concrete. Other algorithms choose different publication order and must prove their own abstract point.

Deletion often marks a node logically absent, then physically unlinks its tower. Searches that encounter marked nodes help bypass them or retry. Marking the base link/value may be the linearization point. Higher links are routing aids; leaving them temporarily reachable is acceptable only when traversals detect the mark and never return the deleted entry.

Atomic pointers do not solve memory reclamation. A reader can load a pointer just before unlink and dereference after another thread frees/reuses it. Use hazard pointers, epochs/RCU, reference counting with a correct acquisition protocol, tracing GC, or arena lifetime. Tagged pointers/generations address ABA but not reader lifetime alone. Each scheme has progress, memory, and shutdown costs.

Lock-free means system-wide progress, not wait-free per operation. CAS loops can starve. Random level generation, allocation, and comparator calls may block even if link manipulation is lock-free. Range iteration may be weakly consistent rather than a snapshot; it can observe concurrent insertions/deletions according to the algorithm's contract. Linearizability testing must target point operations and separately validate iterator semantics.

**Persistence and crash recovery need ordering beyond CPU memory.** A durable skip list must persist node contents, links, membership state, and allocator metadata in an order that recovery can interpret. Flushing a higher link before its node contents creates a durable dangling pointer. In-place multi-level deletion can leave partially unlinked states after a crash.

Common durable designs log logical operations and rebuild, use copy-on-write/path-like metadata, or define recoverable marking/link protocols with persistent-memory fences. Absolute pointers are invalid across remapping unless the format guarantees stable addresses; use offsets or object IDs. Validate all offsets, heights, cycles, ordering, and sizes on recovery. For many storage engines, the skip-list memtable is deliberately volatile because a write-ahead log is the durability source.

Serialization of a sequential logical map should usually write sorted entries plus comparator/version and regenerate towers on load. Persisting the exact random topology is useful only for exact replay or startup latency and makes the format more fragile. Rebuild also removes accumulated fragmentation and stale index links.

**Numerics and comparators remain dangerous.** Floating keys require a total NaN/negative-zero policy. Redis rejects NaN scores in relevant skip-list paths and uses a member tie-break. Locale-dependent or version-changing string comparison can make stored order invalid after upgrade. Persist comparator identity/version and rebuild when semantics change.

Node allocation computes base bytes plus `height*link_record_size`; use checked multiplication/addition. Size, spans, rank, and version counters can overflow. Maximum height and loop indices must use signedness carefully when descending from zero. A loop like unsigned `for(level=top; level>=0; --level)` never terminates.

Expensive or inconsistent user comparators amplify search work and can violate every ordering proof. Restrict comparator purity, precompute bounded keys, or execute untrusted logic outside the structure's privileged core. Limit range output and traversal time to resist amplification.

**Evidence needs topology independence.** A reference ordered map or sorted list supplies `find`, lower/upper bound, predecessor, range, insert/update, and delete results. Generate operation histories and compare after every operation. Independently traverse base order, count size, detect cycles, then verify each higher level is a subsequence of base with sufficient node height.

Exhaust small explicit height assignments, including all height one, one maximum tower, alternating towers, removal of the only top node, duplicate boundaries, empty ranges, and min/max keys. Inject allocation and comparator failures before every splice; verify the documented unchanged/basic state. For spans, recompute every link distance from base positions. For backward/tail links, traverse both directions.

Random-generator tests use many fixed seeds and report uncertainty rather than hard-coding one exact histogram. Adversarial tests use sorted/reverse keys, equal primary keys, chosen public-hash heights, maximum-size towers, and output-heavy ranges. Benchmarks vary `p`, cap, allocator/layout, key/payload size, lookup/update/range mix, hit rate, scan length, and dataset size across caches.

Concurrent evidence combines invariant checks after quiescence, linearizability histories for point operations, weak-iterator contract tests, forced publication interleavings, reclamation sanitizers, stalled readers, thread exit, and shutdown. Persistence evidence injects crashes at each durable step and validates recovery or logical-log replay. No small sequential benchmark stands in for these obligations.

The following executable accepts explicit heights rather than generating random ones. This makes the topology reproducible and exercises search, lower bound, half-open range, unique-key rejection, multi-level deletion, top-level counts, and structural validation. It demonstrates correctness for one finite sequential layout; it does not empirically validate the height distribution, expected-time theorem, spans, allocation failures, storage durability, or concurrent publication/reclamation.

<!-- bijux-verify: {"id":"skip-list-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"levels=4\nlevel_counts=7,5,3,1\nfound_25=X\nmissing_26=True\nlower_bound_26=30:C\nrange_20_40=20:B,25:X,30:C,35:Y\nduplicate_rejected=True\nerased_30=C\norder_after=10:A,20:B,25:X,35:Y,40:D,50:E\nlevel_counts_after=6,4,2,1\ninvariant=True\nevidence=finite_skip_list_trace\n","stderr":""}} -->
```python
class Node:
    def __init__(self, key, value, height):
        self.key = key
        self.value = value
        self.forward = [None] * height


class SkipList:
    def __init__(self, max_height=8):
        self.max_height = max_height
        self.head = Node(None, None, max_height)
        self.levels = 1
        self.size = 0

    def _predecessors(self, key):
        update = [self.head] * self.max_height
        current = self.head
        for level in range(self.levels - 1, -1, -1):
            while (current.forward[level] is not None
                   and current.forward[level].key < key):
                current = current.forward[level]
            update[level] = current
        return update

    def insert(self, key, value, height):
        if not 1 <= height <= self.max_height:
            raise ValueError("invalid height")
        update = self._predecessors(key)
        candidate = update[0].forward[0]
        if candidate is not None and candidate.key == key:
            return False
        if height > self.levels:
            for level in range(self.levels, height):
                update[level] = self.head
            self.levels = height
        node = Node(key, value, height)
        for level in range(height):
            node.forward[level] = update[level].forward[level]
            update[level].forward[level] = node
        self.size += 1
        return True

    def get(self, key):
        candidate = self._predecessors(key)[0].forward[0]
        return None if candidate is None or candidate.key != key else candidate.value

    def lower_bound(self, key):
        return self._predecessors(key)[0].forward[0]

    def values_in(self, start, end):
        current = self.lower_bound(start)
        result = []
        while current is not None and current.key < end:
            result.append((current.key, current.value))
            current = current.forward[0]
        return result

    def erase(self, key):
        update = self._predecessors(key)
        target = update[0].forward[0]
        if target is None or target.key != key:
            return None
        for level in range(len(target.forward)):
            if update[level].forward[level] is target:
                update[level].forward[level] = target.forward[level]
        while self.levels > 1 and self.head.forward[self.levels - 1] is None:
            self.levels -= 1
        self.size -= 1
        return target.value

    def level_counts(self):
        counts = []
        for level in range(self.levels):
            count = 0
            current = self.head.forward[level]
            while current is not None:
                count += 1
                current = current.forward[level]
            counts.append(count)
        return counts

    def validate(self):
        base = []
        current = self.head.forward[0]
        while current is not None:
            base.append(current)
            current = current.forward[0]
        if len(base) != self.size:
            return False
        if any(base[index].key >= base[index + 1].key
               for index in range(len(base) - 1)):
            return False
        base_ids = {id(node) for node in base}
        for level in range(self.levels):
            previous = None
            current = self.head.forward[level]
            while current is not None:
                if id(current) not in base_ids or len(current.forward) <= level:
                    return False
                if previous is not None and previous >= current.key:
                    return False
                previous = current.key
                current = current.forward[level]
        return all(self.head.forward[level] is None
                   for level in range(self.levels, self.max_height))


skip = SkipList()
for key, value, height in [
    (40, "D", 2), (10, "A", 4), (30, "C", 3), (20, "B", 1),
    (50, "E", 3), (25, "X", 2), (35, "Y", 1),
]:
    assert skip.insert(key, value, height)
print(f"levels={skip.levels}")
print("level_counts=" + ",".join(map(str, skip.level_counts())))
print(f"found_25={skip.get(25)}")
print(f"missing_26={skip.get(26) is None}")
lower = skip.lower_bound(26)
print(f"lower_bound_26={lower.key}:{lower.value}")
print("range_20_40=" + ",".join(
    f"{key}:{value}" for key, value in skip.values_in(20, 40)
))
print(f"duplicate_rejected={not skip.insert(25, 'duplicate', 2)}")
print(f"erased_30={skip.erase(30)}")
print("order_after=" + ",".join(
    f"{key}:{value}" for key, value in skip.values_in(0, 100)
))
print("level_counts_after=" + ",".join(map(str, skip.level_counts())))
print(f"invariant={skip.validate()}")
print("evidence=finite_skip_list_trace")
```

## Definitions and Notation

- `n`: number of live level-zero nodes.
- `p`: probability that a tower continues to the next level, with `0<p<1`.
- `H`: configured maximum node height.
- `height(x)`: number of forward links in node `x`, in `1..H`.
- level `i`: zero-based subsequence containing nodes with height at least `i+1`.
- `update[i]`: predecessor of a target/insertion point at level `i`.
- `lower_bound(k)`: first node whose key is not less than `k`.
- `upper_bound(k)`: first node whose key is greater than `k`.
- `[low,high)`: half-open ordered range.
- `span(x,i)`: declared level-zero distance represented by `x`'s level-`i` link.
- **logical deletion**: abstract removal, usually a mark/state change.
- **physical unlinking**: removal of routing links to a logically deleted node.
- **reclamation**: making node storage reusable after no reader can access it.
- **with high probability**: failure probability decreases polynomially (or more strongly as stated) with `n`; not certainty.

## Mechanisms, Invariants, or Proof Structure

Sequential correctness begins with strict level-zero order and the fact that every upper level is a subsequence. Search maintains a predecessor before the target, moves right only over keys known too small, and descends without losing any possible candidate. Insertion splices one new node between recorded predecessor/successor pairs. Deletion bypasses the same target at all tower levels and restores top metadata.

Randomized performance derives `Pr[height>=h]=p^(h-1)`, expected links `1/(1-p)`, logarithmic top height with high probability, and geometric horizontal progress at each level. Correctness does not use these probabilities. Maximum-level capping and adversarial randomness alter performance constants and tails, not the base-order proof.

Indexable variants add exact span equations tied to level-zero positions. Concurrent variants add abstract state and time: immutable initialization before publication, a declared linearization point, marked logical deletion, helping/physical unlinking, memory-order edges, and safe reclamation. Storage durability adds persistent write ordering or logical replay. These layers cannot be inferred from the sequential splice alone.

## Alternatives and Trade-Offs

| Structure | Strength | Main obligation |
|---|---|---|
| Sorted vector | compact, cache-efficient search/scan | linear middle update |
| Unrolled list | improved locality and block updates | block balancing/search index |
| Skip list | simple local splice, ordered range | randomized bounds and pointers |
| Indexable skip list | rank/select plus order | span arithmetic on every mutation |
| Deterministic skip list | controlled worst-case structure | more complex promotion/rebuild rules |
| Treap | randomized binary tree | rotations/priority randomness |
| AVL/red-black tree | deterministic logarithmic bounds | rotations and balance metadata |
| B/B+ tree | page/cache/storage locality | split/merge and page concurrency |
| LSM memtable skip list | append-oriented concurrent order | arena lifetime and flush integration |
| Concurrent skip list | scalable ordered map candidate | publication, marking, helping, reclamation |
| Hash table | expected constant equality lookup | no native order/range |
| Persistent ordered tree | versioned snapshots | path copying/sharing/reclamation |

## Failure Modes and Misconceptions

- **“Randomized means answers may be wrong.”** randomness affects topology/performance; invariants determine answers.
- **“Expected logarithmic means worst-case logarithmic.”** a legal height pattern can degenerate to linear search.
- **“Height and level are interchangeable.”** zero/one-based conventions differ and cause allocation bugs.
- **“Every upper node is separate.”** levels are links in towers over the same logical node.
- **“Search can stop when it sees equality high up.”** operation/duplicate policy may require the base predecessor or first equivalent.
- **“Duplicates naturally work.”** total composite order and user-key lower/upper boundaries must be specified.
- **“Delete the base node first.”** upper links may still reach it; sequential unlink order and concurrent marking need proofs.
- **“Random seed is only a test detail.”** predictability can be a performance attack surface.
- **“One-half is always optimal.”** pointer bytes, comparisons, cache misses, cap, and workload determine `p`.
- **“Expected two pointers means two allocated words.”** object/allocator/alignment/metadata overhead can dominate.
- **“Spans are cached sizes.”** every link has a precise distance equation that mutations must preserve.
- **“Atomic next pointers make a concurrent skip list safe.”** initialization, multi-level publication, logical deletion, and reclamation remain.
- **“Unlinked means safe to free.”** readers may retain previously loaded pointers.
- **“A concurrent iterator is a snapshot.”** APIs such as Java's can be weakly consistent.
- **“A storage-engine skip list is a general map.”** arena lifetime, no individual deletion, WAL, and flush lifecycle can simplify its contract.

## Worked Examples

### Example 1

At level 3, search for 37 moves from header to key 10, cannot move to 50, and descends. At lower levels it reaches 30 then 35; level-zero successor is 40. Conclusion: lower-bound search preserves the last key strictly below the target.

### Example 2

Searching lower bound 30 with a `next.key<=target` loop moves onto 30 and finally returns its successor 35. Conclusion: lower bound moves right only while `next.key<target`; upper bound uses the inclusive comparison.

### Example 3

An inserted height-three node uses recorded predecessors at levels 0, 1, and 2. Each old predecessor-successor link is split into two ordered links; level 3 stays unchanged. Conclusion: local splices preserve every subsequence.

### Example 4

Deleting the only height-six node leaves header level five empty. If current height remains six, correctness survives but every search wastes empty descents; if a dangling pointer remains, safety fails. Conclusion: unlink all tower levels and normalize top metadata.

### Example 5

With `p=1/2`, expected links per node are `1+1/2+1/4+...=2`. With `p=1/4`, they are `1+1/4+1/16+...=4/3`. Conclusion: smaller promotion probability saves link space while widening horizontal gaps.

### Example 6

For top threshold `h=c log_{1/p} n`, a union bound gives probability at most `n^(1-c)` that any of `n` towers reaches `h` before capping. Conclusion: logarithmic maximum height is a high-probability statement under independent promotions.

### Example 7

Two members share score 8.5. Ordering only by score makes their placement equivalent and deletion ambiguous. Ordering by `(score,member)` gives a unique location while range-by-score uses synthetic tie bounds. Conclusion: duplicate primary keys need a total composite policy.

### Example 8

An indexable link from rank 4 to rank 11 has declared span 7. Inserting a node at rank 8 must split it into distances 4 and 4 under a destination-counting convention, while every higher crossing span grows by one. Conclusion: spans require a stated counting convention and independent recomputation.

### Example 9

A concurrent inserter initializes key/value and all next pointers, then release-publishes level zero. A reader missing later upper links still finds the node from the base; a reader seeing the base sees initialized content. Conclusion: publication order is part of the correctness proof.

### Example 10

A reader loads node `x`; another thread marks and unlinks `x`, frees it, and allocation reuses the address. Pointer equality can succeed on a different object. Conclusion: marking/CAS need safe reclamation and possibly ABA tagging, not immediate free.

## Cross-Program Connections

- **Algorithms:** randomized analysis, geometric variables, union bounds, lower/upper bounds, and output-sensitive ranges derive guarantees.
- **Programming languages:** flexible arrays, generics, comparator laws, nullable/sentinel representation, ownership, and iterators shape APIs.
- **Concurrent programming:** release/acquire publication, CAS, marking, helping, linearization, ABA, hazards/epochs/RCU, and progress conditions govern safety.
- **Database engineering:** sorted sets, memtables, composite internal keys, WAL recovery, arena lifetime, rank, and range scans motivate variants.
- **Data engineering:** ordered event buffers, window scans, mutable indices, and partition-local structures use the same range semantics.
- **Computer architecture:** pointer chasing, tower allocation, inline keys, cache/TLB misses, branch behavior, and NUMA placement determine constants.
- **Security engineering:** adversarial heights/keys/comparators, range amplification, malformed persistent links, and counter overflow require limits.
- **Distributed systems:** local randomized order structures do not provide global consistency; snapshot and merge semantics require separate protocols.

## References

1. William Pugh, [Skip Lists: A Probabilistic Alternative to Balanced Trees](https://g-trees.github.io/g_trees/assets/references/pugh1990skip.pdf), Communications of the ACM 33(6), 1990. Primary source for representation, algorithms, probability model, and expected bounds.
2. William Pugh, [Concurrent Maintenance of Skip Lists](https://15721.courses.cs.cmu.edu/spring2019/papers/07-oltpindexes1/pugh-concurrent-tr1990.pdf), University of Maryland Technical Report CS-TR-2222, 1989/1990. Primary source for concurrent sorted-list and skip-list maintenance.
3. MIT OpenCourseWare 6.046J, [Randomization: Skip Lists](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/14fe095781943ff9bd485e6e263b48f7_MIT6_046JS15_lec07.pdf), Spring 2015. Academic derivation of randomized topology and search analysis.
4. Redis Project, [`src/t_zset.c`](https://github.com/redis/redis/blob/unstable/src/t_zset.c). Current primary source for capped random levels, composite score/member ordering, spans, backward links, rank, ranges, insertion, and deletion.
5. RocksDB Project, [`memtable/inlineskiplist.h`](https://github.com/facebook/rocksdb/blob/main/memtable/inlineskiplist.h). Current primary source for inline allocation, branching/cap configuration, splice invariants, concurrent insert publication, validation, and arena lifetime.
6. RocksDB Project, [MemTable](https://github.com/facebook/rocksdb/wiki/MemTable). Current official lifecycle and concurrent-write context for skip-list-based memtables.
7. LevelDB Project, [`db/skiplist.h`](https://github.com/google/leveldb/blob/main/db/skiplist.h). Current primary source for arena-backed skip-list search, insertion, randomness, and synchronization assumptions.
8. Oracle, [`ConcurrentSkipListMap`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/ConcurrentSkipListMap.html), Java SE 25. Current official navigable-map, expected complexity, atomic operation, iterator, null, ordering, and concurrency contract.
9. OpenJDK Project, [`ConcurrentSkipListMap.java`](https://github.com/openjdk/jdk/blob/master/src/java.base/share/classes/java/util/concurrent/ConcurrentSkipListMap.java). Current primary implementation source for Java's base nodes, index levels, insertion, logical deletion, unlinking, and traversal.
10. Keir Fraser, [Practical Lock-Freedom](https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-579.pdf), University of Cambridge Technical Report UCAM-CL-TR-579, 2004. Primary source for lock-free ordered structures, skip-list techniques, CAS, logical deletion, and memory-management context.

## Exercises

### Exercise 1

Derive sequential unique-key skip-list search, lower/upper bound, insertion, and deletion. State height convention and prove all representation invariants.

### Exercise 2

Derive expected tower space, expected/high-probability height, and expected search behavior for general fixed `p`. Explain exactly what remains worst-case linear.

### Exercise 3

Extend a skip list with backward links and spans for rank/select. Specify counting convention, mutation equations, overflow policy, and independent validators.

### Exercise 4

Compare skip list, sorted vector, red-black tree, B+ tree, and hash table for a Redis-like sorted set, an LSM memtable, and a read-mostly in-process index. Design representative benchmarks.

### Exercise 5

Design a concurrent skip-list map with insert, find, erase, and weak range iteration. State linearization, publication, marking/helping, memory order, progress, reclamation, shutdown, and verification.

## Answers to the Exercises

### Answer 1

Use height count in `1..H`, levels `0..height-1`, a maximum-height header, strict unique-key order, and current occupied height at least one. Search descends from top, advancing while next key is strictly below target; recorded predecessors bracket the first not-less node at every level. Lower bound returns the base successor; upper bound uses the appropriate inclusive advance; find additionally tests equality. Insert rejects equality, generates bounded height, fills new upper predecessors with header, and splits predecessor-successor links at each node level. Delete finds the target, bypasses it at every tower level, decrements size, and drops empty header levels. Proof uses level-zero total order, every upper level as a base subsequence, sufficient target height for every incoming link, and local splice induction. Validate cycles, strict order, exact base size, height/link bounds, subsequence membership/order, top/header emptiness, and all operation results against a sorted map.

### Answer 2

For independent promotion, `Pr[height>=h]=p^(h-1)`. Expected links are the tail sum `sum_{h>=1}p^(h-1)=1/(1-p)` before cap, so expected total link space is linear. Expected population at zero-based level `i` is `n p^i`; solving for constant population gives height `Theta(log_{1/p} n)`. For `h=c log_{1/p} n`, union bound over nodes gives `Pr[max_height>=h]<=n p^(h-1)`, polynomially small for suitable `c` up to constants. Reversing search, horizontal steps before a promoted predecessor are geometric with constant expectation depending on `p`, across logarithmically many levels, so expected comparisons are logarithmic. All-height-one or otherwise unlucky legal topologies still take linear time, and capping below the needed scale can create long top-level scans. Independence/private randomness and fixed `p` are assumptions; correctness remains deterministic.

### Answer 3

Keep `backward` on level zero and `tail`; define a span as the number of base destinations crossed, so an adjacent base link has span one and null/header conventions are explicit. Search records predecessor `update[i]` and cumulative base rank `rank[i]`. If predecessor's old link spans `s` and insertion lies `delta=rank[0]-rank[i]` base steps after it, set predecessor-to-new span `delta+1` and new-to-successor span `s-delta`; increment untouched crossing upper spans. Deletion joins predecessor span with target's outgoing span minus one and decrements unaffected crossing spans; repair backward/tail. Rank accumulates spans while advancing; select advances while the next span stays within the target rank. Use checked counters and reject/rebuild at overflow. Independently number base nodes, verify forward/backward symmetry and tail, then for every link recompute the destination rank difference and compare with stored span; test empty, ends, only-top deletion, every rank, out-of-range select, and duplicate policy.

### Answer 4

For a Redis-like sorted set, combine member hash lookup with a composite `(score,member)` skip list when rank/range/reverse scans and local updates dominate; spans/backward links cost memory. A red-black tree is a deterministic alternative; a B+ tree may improve page locality at larger scale. For an LSM memtable, an arena-backed skip list supports ordered iteration and concurrent append-like insert while WAL supplies durability; a sorted vector has expensive updates, and a hash table cannot directly flush in order. For a read-mostly index built in batches, a sorted vector often wins memory/cache/search/range behavior. Hash tables win equality-only access. Benchmark identical semantics with real key/value sizes, duplicates, lookup/update/delete/range ratios, range lengths, build/flush, memory including allocator overhead, cache/TLB/branches, concurrency, p50/p99/p999, compaction/rebuild, and recovery. Sweep `p`, cap, block/page size, and dataset across cache boundaries; report the regime, not a universal winner.

### Answer 5

Use immutable keys/values per published node, atomic marked next links or a separate logical state, and a header tower. Find traverses while helping bypass marked nodes and returns only an unmarked matching base node. Insert allocates/initializes the full tower, finds and validates predecessor/successor windows, CAS-publishes level zero as the linearization point, then adds upper routing links with release stores; duplicate race retries or returns existing by contract. Erase CAS-marks logical membership at its linearization point, marks/unlinks other levels, and lets traversals help physical removal. Acquire loads observe initialized nodes. Use hazard pointers or epochs for reclamation, define stalled-thread memory bounds, detach thread records at exit, and drain safely at shutdown. State lock-free rather than wait-free progress if retries can starve. Weak range iteration follows base links, omits nodes observed marked, and may reflect concurrent operations without claiming a snapshot. Verify with model/linearizability histories for point operations, contract-specific iterator histories, forced interleavings around every publication/mark, ABA/address reuse, stalled readers, reclamation sanitizers, counter/cap exhaustion, allocation failure, comparator restrictions, and shutdown races.
