---
module_id: DSE-027
program: Data Structures Engineering
level: 1
module_number: 27
title: Hopscotch Hashing
status: complete
last_verified: 2026-08-30
---

# Hopscotch Hashing

## One-Page Review

### Governing question

How can an open-addressed map keep every key inside a small contiguous neighborhood of its home while using farther empty slots and local relocations for high-load insertion, bounded lookup, and concurrent validation?

### Essential definitions

- A key's **home bucket** is its reduced hash position.
- A home bucket's **neighborhood** contains that bucket and the next `H-1` cyclic slots.
- The **neighborhood invariant** requires every live key to lie within forward distance `<H` of home.
- A **hop-information bitmap** at home marks offsets whose slots contain keys belonging to that home.
- A **physical slot** owns at most one payload; overlapping neighborhoods describe logical membership, not duplicated storage.
- **linear vacancy search** scans forward for an EMPTY slot; lookup does not perform that scan.
- A **hop/relocation** moves a resident from one legal neighborhood offset to another, bringing the empty slot closer to the new key's home.
- A **relocation chain** repeats legal hops until the vacancy enters the new key's neighborhood or no move is available.
- A **segment/version** is synchronization metadata used by concurrent variants to lock or validate affected buckets.
- **resize/rehash** rebuilds every neighborhood and bitmap under a new capacity/hash configuration.

### Central model, mechanism, or theorem

For capacity `m>0`, neighborhood width `1<=H<=m`, and cyclic distance

\[
dist(a,b)=(b-a)\bmod m,
\]

key `k` with home `h(k)` may occupy slot `j` only when `dist(h(k),j)<H`. Bitmap bit `d` at home `h` is set exactly when slot `(h+d) mod m` holds a live key whose home is `h`.

Lookup reads the home bitmap and examines only marked offsets, then confirms equality. Insertion may find an EMPTY outside the neighborhood. To move that vacancy backward, choose a candidate home `c` before the vacancy and one of its residents at offset `r` such that `r<dist(c,empty)<H`; moving the resident to `empty` remains legal and makes its old slot the new vacancy. Each successful hop preserves neighborhood membership and bitmap/payload agreement. If no chain brings the vacancy within distance `<H` of the new home, the implementation must rebuild, grow, or report failure.

### Critical invariants

1. Every live key appears once and its slot is within its home neighborhood.
2. Every hop bit names a live slot belonging to that home, and every live slot has exactly one matching bit.
3. Lookup enumerates the complete marked neighborhood, filters by hash/fingerprint, and confirms equality.
4. Unique insertion checks the home neighborhood for an equivalent key before publishing another copy.
5. A relocation source and destination both belong to the moved key's neighborhood; its old bit is cleared and new bit set with payload ownership transferred safely.
6. A relocation chain is bounded and either commits a complete valid state or preserves/recoverably exposes the prior state.
7. Deletion clears exactly the payload and matching home bit, with correct size and lifetime ordering.
8. Capacity, neighborhood width, bitmap representation, hash, resize, concurrency, and iterator/reference contracts agree.

### Common failures

- Treating the `H` physical slots after home as a private bucket; neighborhoods overlap.
- Scanning `H` payloads but ignoring the bitmap, losing the intended lookup filtering and concurrency protocol.
- Setting a hop bit before the destination payload is safely initialized.
- Moving an arbitrary nearby resident to the vacancy even though the vacancy lies outside that resident's neighborhood.
- Updating destination metadata but not clearing the source bit, creating two apparent copies.
- Publishing intermediate moves that let a concurrent reader miss the key at both source and destination.
- Declaring the whole table full when one relocation attempt fails.
- Claiming lookup is one cache access for arbitrary `H`, slot size, wrap, fingerprints, or hardware.
- Repeating the original paper's high-load benchmark as a universal guarantee.
- Assuming one bitmap machine word makes the entire map atomic or lock-free.

### Compact example

With `m=12,H=4`, occupy slots 0 through 5 with homes arranged so slot 4 belongs to home 3 and slot 2 belongs to home 1. A new home-zero key finds EMPTY slot 6, outside offsets 0–3. Move the home-three resident from 4 to 6, then the home-one resident from 2 to 4; vacancy 2 is now legal for home zero. Both moves keep offset three within their respective neighborhoods and update the corresponding bitmaps.

### Connections

[DSE-023](023-linear-probing.md) supplies cyclic layout and vacancy search; [DSE-025](025-robin-hood-hashing.md) supplies local relocation/lifetime concerns; [DSE-026](026-cuckoo-hashing.md) supplies augmenting-path and transactional-failure contrasts. The [program roadmap](../ROADMAP.md) next owns resizing, hash-flooding resistance, and an integrated memory-efficient map.

## Governing Question

Which neighborhood definition, membership index, vacancy-relocation proof, bounded failure policy, and synchronization protocol make hopscotch hashing correct under deletion, resize, exceptions, contention, and hostile keys?

## Why This Matters

Linear probing keeps memory accesses contiguous but lets negative lookups cross long clusters. Cuckoo hashing bounds candidate buckets but may relocate along nonlocal paths and fail on graph structure. Hopscotch hashing combines a local lookup neighborhood with a farther linear vacancy search and carefully chosen moves that “hop” the vacancy back toward home.

The bitmap makes lookup proportional to marked residents rather than to the potentially long vacancy-search region. Overlapping neighborhoods allow high physical utilization while keeping a key near home. The same representation gives concurrent readers a compact membership summary to validate.

The price is coupled metadata. A slot can be physically close to many home buckets but belongs logically to exactly one. A move changes payload location and two bitmap positions. Insertion can fail while empties remain if no legal relocation chain exists. Concurrent movement, deletion, and resize require more than atomic bit operations. High-load results from a specific historical implementation/hardware do not substitute for current workload evidence.

## Prerequisites and Retrieval

Retrieve abstraction, invariants, operation contracts, cost, layout, cache, genericity, iteration, testing, and benchmarking from [DSE-001](001-abstract-data-types-and-concrete-representations.md) through [DSE-010](010-benchmarking-a-structure-without-misleading-results.md). Retrieve hashing/reduction from [DSE-021](021-hash-functions-and-distribution.md), chaining contrast from [DSE-022](022-separate-chaining.md), open-addressing state/load from [DSE-023](023-linear-probing.md), probe variants from [DSE-024](024-quadratic-probing-and-double-hashing.md), relocation/lifetime from [DSE-025](025-robin-hood-hashing.md), and bounded relocation/fallback from [DSE-026](026-cuckoo-hashing.md).

## Learning Objectives

After completing this module, you should be able to:

1. define cyclic home neighborhoods and exact hop-bitmap semantics;
2. implement bounded bitmap-directed lookup and duplicate-safe update;
3. derive legal vacancy moves and relocation-chain termination;
4. implement deletion without tombstones while preserving membership metadata;
5. distinguish local relocation failure from physical fullness;
6. design transactional/no-throw payload and bitmap publication;
7. specify resize, wrap, bitmap width, load, and invalidation behavior;
8. explain concurrent validation, locking/versioning, and reclamation obligations;
9. test bitmap/payload agreement, relocation histories, failure, and adversarial homes;
10. benchmark lookup locality against insert movement, contention, and memory overhead.

## Core Exposition

**A neighborhood is a logical index over shared slots.** Let the table contain `m` slots in a ring and choose width `H`. Home `h` owns a virtual neighborhood at offsets `0,...,H-1`. Physical slot `j` may hold one entry whose stored/recomputed home `h` satisfies `dist(h,j)<H`. The neighborhoods of adjacent homes overlap heavily; they do not reserve `H` cells apiece.

Store at each home a bitmap `hop[h]` with `H` meaningful bits. Bit `d` means slot `(h+d) mod m` contains a live key whose home is exactly `h`. It does not merely mean the slot is occupied. Therefore:

\[
bit(h,d)=1\iff slot[(h+d)\bmod m]=OCCUPIED(k,v)\land home(k)=h.
\]

This biconditional is the representation invariant. Cached full hashes or home metadata help validate it and avoid rehashing during relocation. If metadata uses fingerprints, equality remains authoritative.

**Lookup follows membership, not vacancy history.** Compute home, snapshot/read its hop information under the representation's synchronization rule, and enumerate set offsets. For each, inspect the corresponding slot, validate that it is a stable live entry for this home/version, filter by full hash/fingerprint, and compare equality. If no candidate equals the key, it is absent.

Unlike linear probing, lookup does not scan until EMPTY and does not depend on tombstones. Cost is bounded by neighborhood representation: up to `H` bits/slots in a simple version, often only the set bits. “One machine word” describes bitmap storage when `H` fits; payload accesses, wrap, cache-line count, equality, and validation retries remain.

Unique insertion must run the same logical candidate search first. If it finds equality, update/reject without changing size or membership. Two equal keys cannot be allowed at different offsets. Key hash/equality state remains stable while indexed.

**Direct insertion uses the first available vacancy.** Search physical slots forward from home, bounded by capacity or a governed search range, for EMPTY. If vacancy distance is `<H`, construct/publish the new entry there and set the matching home bit. Payload must be initialized before readers treat the bit as live; deletion reverses that relationship under the concurrency/lifetime protocol.

The first vacancy can be farther away. Hopscotch does not store the new key there, because lookup would not search it. Instead, it tries to move other residents into that vacancy, causing the vacancy to move backward until it enters the new key's neighborhood.

**A legal hop preserves another key's neighborhood.** Suppose vacancy is `e`. Consider a candidate home `c` among the preceding `H-1` positions, so `q=dist(c,e)` satisfies `1<=q<H`. If `hop[c]` has a set bit `r<q`, its resident is at `s=c+r` and may move to `e`: the destination offset `q` is still within home `c`'s neighborhood. Clear bit `r`, set bit `q`, move the complete payload from `s` to `e`, then make `s` the new vacancy.

Why require `r<q`? The source must occur before the vacancy in the same forward neighborhood, so the vacancy moves backward from `e` to `s`. Choosing an offset after/equal to `q` does not create progress and may refer through wrap incorrectly. Cyclic distance, not ordinary integer comparison, owns the proof.

Repeat until `dist(new_home,e)<H`, then install the new entry. Bound each scan/move and detect revisited states if the relocation policy can cycle. The original algorithm searches candidate homes/bits according to a defined order. An optimized BFS or other relocation search needs its own proof and memory/failure budget.

**The relocation example exposes overlapping ownership.** Before inserting X, slots 0–5 hold A,B,C,D,E,F with homes `0,0,1,0,3,5`. X's home is zero and the first EMPTY is six. E at four belongs to home three at offset one, so it can move to six at offset three. C at two belongs to home one at offset one, so it can move to four at offset three. X then occupies two at home-zero offset two.

Final home-zero residents occupy offsets 0,1,2,3; home-one has offset 3; home-three has offset 3; home-five has offset 0. Physical slot four lies inside several virtual neighborhoods but its single resident C belongs only to home one, and only `hop[1]` marks it.

**Failure does not mean full.** Relocation can stop because no preceding home has a movable resident, a move/search budget expires, metadata distance/bitmap cannot represent the configuration, allocation or payload movement fails, a concurrent version changes, or maximum capacity policy prevents rebuild. EMPTY slots elsewhere may remain.

Fallback is explicit: try another complete relocation plan/order if governed; rebuild with new seed/capacity; grow; use a separately specified overflow structure; or return a typed failure. Never loop indefinitely or place the key outside its neighborhood. A budget hit is an operational failure, not proof of mathematical impossibility.

**Plan before mutation when failure can occur.** A relocation chain touches payload slots and multiple homes' bitmaps. If moves are no-throw and the table is exclusively locked, an in-place algorithm can preserve invariants at each ordered step. With throwing moves, callbacks, optimistic concurrency, or strong exception requirements, first discover a plan against a stable snapshot, retain all affected ownership, and commit transactionally or roll back.

The executable oracle copies immutable records and bitmap integers, performs the complete relocation on that trial state, validates progress, then publishes the two arrays together at the sequential abstraction boundary. Production implementations can use node indirection, relocation logs, double-buffered metadata, locks, versions, or restricted no-throw types. Merely copying a bitmap is not enough if payload objects have external ownership.

Publication order depends on reader protocol. Setting the destination bit before payload initialization may expose garbage. Clearing the source first may make a reader miss a key. Some concurrent algorithms mark/version buckets, move data, update hop information, then validate/retry readers. The exact linearization points and memory orders must be proved for the chosen scheme.

**Deletion is direct but synchronized.** Lookup locates the key through its home bitmap. Remove/destroy the payload and clear the exact home-offset bit under an order that prevents readers from accepting stale metadata or reclaimed storage. Decrement size once. No probe-chain tombstone is required because lookup enumerates explicit neighborhood membership.

Deletion creates an EMPTY that later insertion can use. Optional compaction is not necessary for reachability and can add relocation/invalidation cost. Concurrent deletion requires version/lock coordination and safe reclamation if payload references escape. An erased bitmap bit does not alone prove no reader holds the old value.

**Bitmap representation constrains the design.** A native word enables fast bit scans and atomic snapshots for widths within that word, but `H` is not automatically the word size. Larger neighborhoods may require multiple words, sparse/list forms, or compressed metadata; their read consistency and cache behavior change. Some implementations use overflow structures when the fixed neighborhood is saturated.

Capacity need not equal bitmap width. Power-of-two capacity allows masking but demands mixed low bits; prime policies use division. Wraparound means the final homes' neighborhoods cross slot zero. Allocate padding/mirrored metadata only if invariants and iteration exclude duplicate payload ownership. Checked arithmetic covers capacity, `home+offset`, reserve/load rounding, and maximum sizes.

**Load is an empirical and structural input.** Hopscotch can maintain short lookup neighborhoods at high physical load when relocation succeeds, but a home can receive more than `H` keys, making the fixed neighborhood insufficient regardless of empties elsewhere. Poor or hostile hashes can cause failure at low global load.

The original paper reported good performance above 90% density on named 2008-era systems/configurations. That is historical experimental evidence, not a load guarantee, universal threshold, or current comparison. Hash family, `H`, slot/payload size, bitmap form, relocation order/range, allocation, concurrency, workload, and hardware determine results.

Track live load, per-home population, bitmap population, initial vacancy distance, moves and homes inspected per insertion, relocation failures/reasons, rebuild/grow/reseed, hash/equality calls, bytes moved, reader retries, lock contention, memory, and latency percentiles. Averages hide rare relocation chains and resize spikes.

**Current implementations are scoped evidence.** Tessil's `hopscotch-map` documents an open-addressed C++ map/set with power-of-two and prime growth variants, cached hashes, overflow behavior, and generic API/lifetime constraints. Its source defines its own neighborhood/overflow/layout details; those must not be inferred for all hopscotch tables.

The Linux `dm-vdo` integer map source is a current in-tree, domain-specific hopscotch-style implementation and demonstrates that kernel ownership/allocation/concurrency context matters. The original and lock-free research variants use different synchronization designs. ISO C++ unordered-container requirements specify observable hash/equality, complexity, rehash, and invalidation behavior without mandating hopscotch layout.

**Iteration and references expose movement.** A flat iterator scans physical capacity and yields live slots, so traversal is `O(m)`. Relocation can move an existing payload on insertion; resize moves many; deletion destroys one. Unless values are node-indirected, references/indices/iterators may invalidate more aggressively than in chaining. State exact guarantees.

Logical serialization writes entries, not raw bitmaps, secret seed, empty layout, locks, or transient versions. A versioned physical snapshot must establish stable concurrent capture, endian/word-size format, capacity/hash compatibility, payload lifecycle, and validation before restoring.

**Concurrency requires a history proof.** Original hopscotch hashing was designed with concurrency in mind, but the sequential neighborhood idea is not itself thread-safe. A lookup may read a home bitmap, then race a relocation. Writers may choose the same vacancy or move the same resident. Locks across segments can deadlock; optimistic operations can starve; resize replaces storage and home reduction.

Define linearization points for find/insert/update/delete, lock acquisition order or nonblocking descriptors, bitmap/payload memory order, version validation, retry bounds, resize cooperation, iterator/snapshot semantics, cancellation, and reclamation. Herlihy-Wing linearizability provides the observable criterion; lock-free research supplies one specific construction and progress claim, not a reusable label for arbitrary code.

**Security remains separate from locality.** A chosen set of keys with one home can exceed neighborhood capacity and force repeated rebuilds. Attackers can target expensive equality, relocation chains, overflow structures, locks, and resize. Random/keyed hashing reduces predictability but cannot repair an implementation bug or provide independence after seed leakage.

Use input/time/capacity/retry/overflow limits, strong candidate mixing, per-home and relocation telemetry, alternate structures, backpressure, and retained old state on failure. Hash-flooding resistance is owned by DSE-029 in the [program roadmap](../ROADMAP.md); this module exposes the hopscotch-specific attack surfaces without claiming immunity.

**Testing uses two independent views.** Compare logical behavior with a reference map. Separately reconstruct expected bitmaps from physical slots and full hashes; require exact equality to stored metadata. For every live key, ensure distance `<H` and bitmap-directed lookup finds its unique slot. For every set bit, verify a correctly homed initialized payload.

Generate insert/update/get/delete/reserve/rebuild sequences. Exhaust small capacities, widths, homes, and insertion orders. Force direct placement, one/multiple hops, wrap, no legal move despite empties, saturated home, duplicate during relocation, deletion/reuse, resize, maximum arithmetic, constant/structured hashes, and injected hash/equality/allocation/move/destructor failures. For concurrency, record histories, validate linearizability, run race tools, stall at publication points, and stress resize/reclamation.

Benchmark realistic/adversarial hashes over load and `H`, hit/miss/update/delete mixes, churn, relocation and rebuild boundaries, flat/node/overflow layouts, payload sizes, bitmap forms, cache/branch/NUMA, locks/retries, memory, throughput, and p50/p95/p99/max latency. Report probes as bitmap words, set bits, payload reads, vacancy scans, homes inspected, and moves—not one ambiguous count.

The executable trace below verifies exact bitmap/payload correspondence, two legal moves, transactional publication, bounded lookup, direct deletion/reuse, size, and uniqueness for a finite sequential table. It is not concurrency, failure-injection, or performance evidence.

<!-- bijux-verify: {"id":"hopscotch-neighborhood-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"keys_after=A,B,G,D,C,F,E\nhome0_bitmap=1111\nlookup_C=CHARLIE\nrelocation_moves=2\ndeleted_X=XRAY\nsize=7\ninvariant=True\nevidence=finite_hopscotch_trace\n","stderr":""}} -->
```python
EMPTY = object()


class HopscotchMap:
    def __init__(self, capacity, width):
        assert 1 <= width <= capacity
        self.capacity = capacity
        self.width = width
        self.slots = [EMPTY] * capacity
        self.hops = [0] * capacity
        self.size = 0

    def distance(self, home, slot):
        return (slot - home) % self.capacity

    def locate(self, name, home):
        bits = self.hops[home]
        for offset in range(self.width):
            if bits & (1 << offset):
                index = (home + offset) % self.capacity
                resident = self.slots[index]
                if resident is not EMPTY and resident[0] == name:
                    return index
        return None

    def put(self, name, home, value):
        home %= self.capacity
        existing = self.locate(name, home)
        if existing is not None:
            self.slots[existing] = (name, home, value)
            return False, 0

        trial_slots = list(self.slots)
        trial_hops = list(self.hops)
        free = None
        for distance in range(self.capacity):
            index = (home + distance) % self.capacity
            if trial_slots[index] is EMPTY:
                free = index
                break
        if free is None:
            return False, 0

        moves = 0
        while self.distance(home, free) >= self.width:
            moved = False
            for back in range(self.width - 1, 0, -1):
                candidate_home = (free - back) % self.capacity
                target_offset = self.distance(candidate_home, free)
                for source_offset in range(target_offset):
                    if trial_hops[candidate_home] & (1 << source_offset):
                        source = (candidate_home + source_offset) % self.capacity
                        resident = trial_slots[source]
                        assert resident is not EMPTY and resident[1] == candidate_home
                        trial_slots[free] = resident
                        trial_slots[source] = EMPTY
                        trial_hops[candidate_home] &= ~(1 << source_offset)
                        trial_hops[candidate_home] |= 1 << target_offset
                        free = source
                        moves += 1
                        moved = True
                        break
                if moved:
                    break
            if not moved:
                return False, moves

        offset = self.distance(home, free)
        trial_slots[free] = (name, home, value)
        trial_hops[home] |= 1 << offset
        self.slots = trial_slots
        self.hops = trial_hops
        self.size += 1
        return True, moves

    def get(self, name, home):
        index = self.locate(name, home % self.capacity)
        if index is None:
            raise KeyError(name)
        return self.slots[index][2]

    def delete(self, name, home):
        home %= self.capacity
        index = self.locate(name, home)
        if index is None:
            raise KeyError(name)
        value = self.slots[index][2]
        offset = self.distance(home, index)
        self.slots[index] = EMPTY
        self.hops[home] &= ~(1 << offset)
        self.size -= 1
        return value

    def invariant(self):
        expected = [0] * self.capacity
        names = []
        for index, resident in enumerate(self.slots):
            if resident is EMPTY:
                continue
            name, home, _ = resident
            offset = self.distance(home, index)
            if offset >= self.width:
                return False
            expected[home] |= 1 << offset
            names.append(name)
            if self.locate(name, home) != index:
                return False
        return expected == self.hops and len(names) == self.size and len(set(names)) == self.size


table = HopscotchMap(12, 4)
for name, home, value in (
    ("A", 0, "ALPHA"),
    ("B", 0, "BRAVO"),
    ("C", 1, "CHARLIE"),
    ("D", 0, "DELTA"),
    ("E", 3, "ECHO"),
    ("F", 5, "FOXTROT"),
):
    assert table.put(name, home, value)[0]

inserted, relocation_moves = table.put("X", 0, "XRAY")
assert inserted and relocation_moves == 2
lookup_c = table.get("C", 1)
deleted_x = table.delete("X", 0)
assert table.put("G", 0, "GOLF")[0]
assert not table.put("C", 1, "CHARLIE")[0]

keys_after = [slot[0] for slot in table.slots if slot is not EMPTY]
print("keys_after=" + ",".join(keys_after))
print("home0_bitmap=" + "".join(
    "1" if table.hops[0] & (1 << offset) else "0"
    for offset in range(table.width)
))
print(f"lookup_C={lookup_c}")
print(f"relocation_moves={relocation_moves}")
print(f"deleted_X={deleted_x}")
print(f"size={table.size}")
print(f"invariant={table.invariant()}")
print("evidence=finite_hopscotch_trace")
```

## Definitions and Notation

- `m`: positive physical slot capacity; `n`: live entry count; `alpha=n/m`.
- `H`: neighborhood width with `1<=H<=m`.
- `home(k)`: reduced hash position at current capacity.
- `dist(a,b)=(b-a) mod m`: forward cyclic distance.
- `hop[h]`: membership bitmap or equivalent metadata for keys whose home is `h`.
- **virtual neighborhood**: offsets `0,...,H-1` after a home; overlapping logical view of shared slots.
- **vacancy search**: bounded forward scan used during insertion only.
- **legal hop**: move between two offsets `<H` for the resident's home that moves the vacancy backward.
- **relocation chain**: ordered legal hops ending with vacancy inside the new key's neighborhood.
- **overflow area**: separately governed representation for entries not held under the fixed bitmap invariant.

## Mechanisms, Invariants, or Proof Structure

Lookup correctness follows the bitmap biconditional: every possible equal key is named by a set home bit, and every set bit leads to a correctly homed live payload; equality confirms. Direct insert/delete add/remove one payload and matching bit with correct size and lifetime order.

Relocation correctness uses candidate home `c`, source offset `r`, and vacancy offset `q`, with `0<=r<q<H`. Moving the resident from `c+r` to `c+q` preserves its neighborhood and moves EMPTY backward. Repeating under a bound either yields `dist(new_home,empty)<H` or a governed failure.

Transactional correctness plans/mutates isolated state, checks progress and representation invariants, and publishes only a complete state. Resize/rehash recomputes every home/bit under new capacity and publishes exact-once logical membership.

## Alternatives and Trade-Offs

| Design | Strength | Cost or obligation |
|---|---|---|
| Bitmap neighborhood | compact directed lookup | width/word bound and coupled metadata |
| List/sparse neighborhood | flexible population/width | pointers or multi-load traversal |
| In-place relocation | low planning allocation | no-throw/exclusive update requirement |
| Planned transactional relocation | clean failure boundary | snapshot/queue/log and validation cost |
| Flat payload | locality and compactness | moves and reference invalidation |
| Node/index indirection | cheap hops/stable payload option | allocation/pointer/index overhead |
| Overflow structure | handles saturated homes | extra lookup and attack surface |
| Cuckoo/Robin Hood/grouped table | different displacement/lookup bounds | different invariant and evidence |

## Failure Modes and Misconceptions

- **“Each home owns H physical slots.”** neighborhoods overlap over one shared array.
- **“Any occupied nearby slot belongs to this home.”** only the home bitmap establishes membership.
- **“Lookup scans to EMPTY.”** it enumerates marked neighborhood offsets.
- **“Any earlier key can hop into the vacancy.”** destination must remain inside that key's neighborhood.
- **“Moving data is enough.”** source/destination bitmap state must change consistently.
- **“One atomic bitmap is a concurrent map.”** payload publication, multiple homes, resize, and reclamation remain.
- **“No legal move means full.”** empties may exist but be unusable by this relocation policy.
- **“High load is guaranteed.”** hash distribution and per-home saturation can fail at low load.
- **“H equals a cache line.”** payload/metadata size, alignment, wrap, and hardware decide footprint.
- **“Original benchmark ratios are current facts.”** they belong to the named historical experiment.
- **“Deletion needs tombstones.”** explicit membership allows direct removal, subject to synchronization.
- **“Resize copies bitmaps.”** new homes require complete reinsertion/reconstruction.

## Worked Examples

### Example 1

For `m=12,H=4`, home 10 covers slots 10,11,0,1 at offsets 0,1,2,3. Conclusion: cyclic distance, not linear array comparison, defines membership.

### Example 2

If `hop[3]=0b1010` under low-bit offset notation, keys homed at 3 occupy offsets one and three. Conclusion: occupancy at other nearby slots is irrelevant to home-three lookup.

### Example 3

A new home-five key finds EMPTY slot seven at distance two and installs directly, setting bit two. Conclusion: vacancy scan and lookup neighborhood coincide only on direct success.

### Example 4

Vacancy six, candidate home three, resident offset one: destination offset three is legal and the move `4→6` frees four. Conclusion: `1<3<H` supplies legality and progress.

### Example 5

Vacancy four, candidate home one, resident offset one: move `2→4` at offset three, then a home-zero key can occupy two. Conclusion: multiple hops can carry the vacancy into the target neighborhood.

### Example 6

A proposed move of a home-three resident to slot seven with `H=4` has offset four and is illegal. Conclusion: physical closeness to the vacancy is not enough.

### Example 7

Five distinct keys share one home with `H=4` and no overflow representation. At most four can satisfy the invariant. Conclusion: global empty capacity cannot overcome local neighborhood capacity.

### Example 8

Deleting a home-zero key at offset two clears payload slot two and bit two; other home bitmaps do not change. Conclusion: deletion is direct logical-index maintenance.

### Example 9

Growing changes key 13's home from five in capacity eight to thirteen in capacity sixteen. Conclusion: copying its old bit/slot would break the neighborhood invariant.

### Example 10

Two designs both report one “probe”: one reads a 32-bit bitmap plus two payload candidates; the other scans sixteen 32-byte values. Conclusion: measurement units must expose actual traffic.

## Cross-Program Connections

- **Algorithms:** cyclic intervals, local matching/relocation, bounded search, and invariant-preserving transformations structure insertion.
- **Programming languages:** ownership, no-throw relocation, rollback, atomics, and reference lifetimes govern publication.
- **Computer architecture:** bit scans, cache-line footprint, prefetch, branches, and false sharing determine locality.
- **Software engineering:** payload and secondary membership index must be tested as two mutually consistent views.
- **Database engineering:** high-load in-memory indexes need skew, build failure, resize, and tail-latency plans.
- **Concurrent programming:** bitmap-directed optimistic lookup requires linearizability, versions/locks, memory order, and reclamation.
- **Security engineering:** chosen-home concentration can saturate neighborhoods and force rebuild/overflow denial of service.

## References

1. Maurice Herlihy, Nir Shavit, and Moran Tzafrir, [Hopscotch Hashing](https://people.csail.mit.edu/shanir/publications/disc2008_submission_98.pdf). Primary algorithm, neighborhood representations, concurrent design, resize, and historically scoped experiments.
2. Robert Kelly, Barak A. Pearlmutter, and Phil Maguire, [Lock-Free Hopscotch Hashing](https://arxiv.org/abs/1911.03028). Primary alternative synchronization/progress design and evaluation.
3. Tessil, [`hopscotch-map`](https://github.com/Tessil/hopscotch-map). Current C++ hopscotch map/set documentation, growth-policy, cached-hash, overflow, API, and test context.
4. Tessil, [`hopscotch_hash.h`](https://github.com/Tessil/hopscotch-map/blob/master/include/tsl/hopscotch_hash.h). Current primary implementation source for neighborhood metadata, insertion, overflow, erase, growth, and lifetime conditions.
5. Linux kernel, [`drivers/md/dm-vdo/int-map.c`](https://github.com/torvalds/linux/blob/master/drivers/md/dm-vdo/int-map.c). Current domain-specific in-tree hopscotch integer-map implementation and ownership context.
6. Maurice Herlihy and Jeannette M. Wing, [Linearizability: A Correctness Condition for Concurrent Objects](https://www.cs.columbia.edu/~wing/publications/HerlihyWing90.pdf). Primary observable correctness criterion for concurrent map histories.
7. ISO C++ working draft, [Unordered Associative Container Requirements](https://eel.is/c%2B%2Bdraft/unord.req.general). Observable hash/equality, complexity, rehash, invalidation, and exception requirements without a mandated layout.
8. Scott A. Crosby and Dan S. Wallach, [Denial of Service via Algorithmic Complexity Attacks](https://www.usenix.org/legacy/event/sec03/tech/full_papers/crosby/crosby.pdf). Primary collision-driven resource-attack evidence.
9. Abseil Project, [Swiss Tables Design Notes](https://abseil.io/about/design/swisstables). Current grouped-control-byte contrast showing another compact-membership approach with different probing/invariants.
10. Rust Project, [`std::collections::HashMap`](https://doc.rust-lang.org/std/collections/struct.HashMap.html). Current quadratic/SIMD map contrast, hashing default, capacity, iteration, and API behavior.

## Exercises

### Exercise 1

Specify home, cyclic neighborhood, bitmap, payload, equality, and size invariants for a generic flat map. Give bounded find/update/delete pseudocode and publication/lifetime order.

### Exercise 2

Derive the legal relocation condition `r<q<H`, prove one move preserves membership and moves the vacancy backward, and trace the two-hop example across bitmap and payload states.

### Exercise 3

Design transactional insertion that distinguishes no vacancy, no legal relocation, search-budget exhaustion, move/allocation/callback failure, concurrent invalidation, and maximum-capacity failure. Assign a safe response to each.

### Exercise 4

Design bitmap width, capacity/growth, overflow, layout, iterator/reference, serialization, security, and telemetry policies for large values and untrusted keys.

### Exercise 5

Design differential/structural/concurrent tests and a benchmark comparing hopscotch with linear, Robin Hood, cuckoo, grouped, and chained tables. Prevent high-load and cache-locality claims from becoming universal.

## Answers to the Exercises

### Answer 1

Require `m>0`, `1<=H<=m`, stable compatible hash/equality, one live payload per slot, and each live key at unique slot `j` with `dist(home,j)<H`. Bit `d` at home is set iff slot `home+d` holds a live key for that home; size equals live payloads. Find snapshots/validates the home bitmap, enumerates set bits, filters, and confirms equality within a bound. Update changes only the found value. Delete locates equality, coordinates readers, destroys/clears payload and matching bit in the protocol's safe order, and decrements size once. Payload becomes visible only with a corresponding valid bit; no bit may reference uninitialized/reclaimed storage. Iteration and invalidation follow the chosen flat/node layout.

### Answer 2

Let vacancy `e` have offset `q=dist(c,e)` from candidate home `c`, and let its resident source be `s=c+r` with set bit `r`. `q<H` makes the destination legal for that resident; `r<q` puts source earlier than vacancy in the same forward neighborhood. Move complete payload `s→e`, clear bit `r`, set bit `q`, and set vacancy to `s`; every other membership is unchanged and the moved key remains within home `c`. In the trace, E home3 moves offset1 slot4 to offset3 slot6, then C home1 moves offset1 slot2 to offset3 slot4, leaving slot2 at home-zero offset2 for X. Corresponding bit changes are `home3:1→3`, `home1:1→3`, and `home0:set2`.

### Answer 3

Check duplicates and prepare the new payload. Find EMPTY under an explicit bound. On isolated snapshot/trial state, repeatedly choose only proved legal moves, track progress/visited state, and stop when vacancy enters the target neighborhood. Validate the plan/state, commit ownership and metadata with rollback/no-throw guarantees, then increment size. No vacancy triggers grow/maximum failure. Complete no-move triggers new seed/grow/overflow/typed failure. Budget exhaustion makes no impossibility claim and uses the same bounded fallback. Allocation/hash/equality failure before commit leaves state unchanged; move failure needs no-throw types, indirection, log/rollback, or a documented recoverable basic guarantee. Concurrent version change discards/retries within a budget. Maximum capacity returns failure without looping or out-of-neighborhood placement.

### Answer 4

Choose `H` from measured lookup footprint versus relocation success; use one atomic word only if its bit width and consistency protocol suffice, otherwise a versioned multiword/sparse form. Large/stable values favor node/index indirection; flat metadata can retain cached full hash/fingerprint. Use checked legal capacities, prospective load plus per-home/relocation thresholds, hysteresis, bounded overflow/rebuild/reseed, and a maximum-capacity response. State insertion/relocation/resize invalidation and iteration `O(m)` for flat slots. Serialize logical entries/config version, never secret seed/raw bitmap/locks. For untrusted keys use keyed mixing, per-home/input/time/capacity/retry/overflow limits and alternate structure. Observe loads, home/bitmap population, vacancy distance, homes inspected, moves, failures, overflow, resize/reseed, hashes/equality, bytes moved, retries/contention, memory, throughput, and latency tails.

### Answer 5

Generate logical operations against a reference map and reconstruct expected bitmaps independently after every step. Assert unique keys, exact size, `dist<H`, bitmap biconditional, bounded lookup, lifetime, and rollback. Exhaust small `m,H`, wrap, direct/one/multi-hop insertion, no-move with empties, saturated home, duplicates, delete/reuse, resize, maxima, poor hashes, and injected failures. For concurrency, capture histories for linearizability, use race tools, stall before/after payload/bit publication, force competing moves, delete/resize, retry exhaustion, and reclamation. Benchmark identical semantics/budgets over load, `H`, realistic/adversarial hashes, operation/churn mixes, relocation/resize/overflow tails, payload layouts, cache/NUMA, locks/retries, memory, throughput, and percentiles. Report bitmap words, set bits, payload reads, vacancy scans, homes/moves, equality/hash/bytes, hardware/toolchains, seeds, repetitions, uncertainty, and raw artifacts; scope conclusions to those conditions and cite historical results only as historical evidence.
