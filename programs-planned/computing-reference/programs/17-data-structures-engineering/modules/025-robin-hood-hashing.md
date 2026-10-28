---
module_id: DSE-025
program: Data Structures Engineering
level: 1
module_number: 25
title: Robin Hood Hashing
status: complete
last_verified: 2026-08-30
---

# Robin Hood Hashing

## One-Page Review

### Governing question

How can an open-addressed table reduce displacement inequality by letting a farther-displaced incoming entry evict a nearer-home resident while preserving lookup termination, deletion, failure safety, and evidence boundaries?

### Essential definitions

- **Robin Hood hashing** resolves a collision in favor of the entry farther from its home: it “steals” the slot from the less-displaced resident.
- **home** is the first position in a key's probe sequence.
- **DIB/DFB/PSL** is distance to initial/home bucket, or probe-sequence length before the current position; this chapter uses **DIB**.
- An entry's **age** is its DIB; the poorer/older entry has probed farther.
- **linear Robin Hood hashing** combines this swap discipline with unit-step cyclic probing.
- A **Robin Hood swap** places the higher-DIB incoming entry in the current slot and continues insertion with the evicted lower-DIB entry.
- **early unsuccessful termination** occurs when search distance exceeds the resident DIB in a valid tombstone-free linear Robin Hood table.
- **backward-shift deletion** closes a hole by shifting following positive-DIB entries one slot toward home until EMPTY or DIB zero.
- **displacement distribution** records how live entries' DIB values vary; Robin Hood's objective is lower variance/tails, not a universal reduction in all costs.
- **probe bound** and **distance-width limit** prevent infinite loops and metadata overflow.

### Central model, mechanism, or theorem

For unit-step probing with capacity `m`, entry `x` at slot `j` has

$$
DIB(x,j)=(j-home(x))\bmod m.
$$

An insertion carries an entry with current distance `d`. At an occupied slot with resident distance `r`, equality handles update; if `r<d`, swap the carried entry and resident, then continue with the evicted entry at its next distance. Otherwise continue with the incoming entry. EMPTY commits.

For tombstone-free linear Robin Hood hashing, lookup for key `k` at distance `d` may return absent on EMPTY or when the resident has DIB `<d`. If `k` had survived insertion to this position, it would have displaced a less-displaced resident. Backward-shift deletion preserves this order witness by moving successive entries while DIB is positive and decrementing each moved DIB; it stops before moving an entry already at home.

### Critical invariants

1. Every live entry is stored once, with immutable key/hash and correct home/DIB metadata.
2. Lookup follows the same probe sequence as insertion, checks equality before early-stop logic, and is bounded by capacity.
3. A carried insertion entry's DIB matches the current candidate slot; a swap preserves the resident placed there and advances the evicted entry correctly.
4. No EMPTY lies before a live key on its search path; in the tombstone-free linear variant, no lower-DIB resident may falsely precede a sought entry at a greater search distance.
5. Backward-shift deletion moves only positive-DIB successors, decrements distance exactly once, and leaves one EMPTY at the final hole.
6. Live count, initialized payloads, cached hashes/fingerprints, and distance metadata agree after every commit.
7. Resize reinserts each live entry from its full hash with DIB reset and recomputed; physical order is not copied.
8. Load, maximum distance, failure, invalidation, concurrency, security, and measurement policies are explicit.

### Common failures

- Treating Robin Hood as a hash function rather than a collision-resolution discipline.
- Swapping keys/values but not their full hash, DIB, or ownership metadata.
- Incrementing the wrong entry's distance after a swap.
- Checking `resident_DIB<search_DIB` before equality under inconsistent metadata.
- Assuming DIB values are globally nondecreasing across a cluster; a key at home can create a decrease.
- Applying early termination unchanged across ordinary tombstones or arbitrary deletion schemes.
- Backward-shifting past an entry with DIB zero and making it unreachable from home.
- Letting a narrow distance field wrap instead of growing, reseeding, widening, or reporting failure.
- Claiming Robin Hood lowers the mean search cost; its defining effect redistributes displacement and reduces variance under scoped models.
- Applying classic random-probing constants to a practical linear-probing implementation.

### Compact example

In eight slots with identity homes, insert keys 0,1,8,16. Key 8 reaches slot 1 with DIB 1 and evicts key 1 at DIB 0; key 1 continues. Key 16 later evicts key 1 at slot 2. Physical keys become `0,8,16,1` with DIBs `0,1,2,2`. A missing home-zero key stops when its search distance 3 encounters resident DIB 2. Deleting 8 shifts 16 and 1 backward, producing `0,16,1` with DIBs `0,1,1`.

### Connections

[DSE-023](023-linear-probing.md) supplies clustering, tombstones, and cyclic distance; [DSE-024](024-quadratic-probing-and-double-hashing.md) separates probe generation from collision discipline. The [program roadmap](../ROADMAP.md) next studies cuckoo and hopscotch relocation, then resizing and flooding resistance.

## Governing Question

Which displacement definition, swap loop, early-stop theorem, deletion transformation, distance representation, failure contract, and evidence make Robin Hood hashing a correct engineered data structure rather than a compelling metaphor?

## Why This Matters

Open addressing distributes collision cost unevenly. First-come-first-served placement lets early keys remain near home while unlucky later keys travel far. Robin Hood insertion deliberately transfers some advantage from low-displacement residents to higher-displacement arrivals. The intended outcome is a tighter search-cost distribution and better tail behavior.

That redistribution adds movement and state. Insertion may relocate several existing key/value objects before finding EMPTY. Lookup's powerful early-stop rule depends on a preserved displacement invariant. Deletion must repair the table or represent history carefully. A distance counter can overflow. Resize, references, iterators, exceptions, concurrency, and hostile hashes become more subtle than in a simple insert-only diagram.

The name also spans different algorithms. Celis's original work and later mathematical analyses use random probe-sequence models. Many contemporary “Robin Hood” maps instead use linear probing and backward-shift deletion. Some store payloads inline; others store indices into a dense vector. Results from one model do not automatically establish latency or memory behavior in another. This module makes those boundaries explicit.

## Prerequisites and Retrieval

Retrieve ADT, representation, operation, cost, layout, genericity, iteration, testing, and benchmarking tools from [DSE-001](001-abstract-data-types-and-concrete-representations.md) through [DSE-010](010-benchmarking-a-structure-without-misleading-results.md). Retrieve full-hash and reduction contracts from [DSE-021](021-hash-functions-and-distribution.md), the separate-layout contrast from [DSE-022](022-separate-chaining.md), and open-addressing state/deletion/load rules from [DSE-023](023-linear-probing.md). [DSE-024](024-quadratic-probing-and-double-hashing.md) establishes that a collision discipline and a probe generator are separate design choices.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish Robin Hood collision resolution from hashing and probe generation;
2. derive DIB under cyclic linear probing and maintain it through swaps;
3. implement duplicate-safe insertion with correct carried-entry state;
4. prove early unsuccessful termination for the stated table variant;
5. implement and justify backward-shift deletion;
6. separate mean, variance, maximum, and tail claims under random versus linear probing;
7. design distance-width, load, resize, lifetime, failure, and invalidation policies;
8. assess flat, node-indirected, and dense-payload layouts;
9. test structural histories, metadata overflow, failure, and hostile hashes;
10. benchmark distributional behavior and complete costs without a universal-winner claim.

## Core Exposition

**Robin Hood is an arbitration rule.** A hash function and probe generator produce candidate slots. When the carried entry collides with a resident, the policy compares how far each has traveled. If the carried entry has traveled farther, it takes the slot and the resident becomes the carried entry. If not, the carried entry continues. Ties commonly leave the resident in place, giving deterministic behavior without affecting the strict inequality invariant.

The policy can be described for abstract probe sequences, as in classic random-probing analysis. This chapter's executable design uses cyclic linear probing because it supports compact DIB arithmetic, early termination, and local backward-shift deletion. Whenever a statement depends on linearity, it says so.

Let `m>0`, `home(k)=reduce(hash(k),m)`, and position `j`. Under unit-step probing, `DIB(k,j)=(j-home(k)) mod m`, interpreted along a search bounded to fewer than `m` steps. Store DIB explicitly or recompute it from a cached full hash/home and index. Explicit fields speed comparison but consume metadata and require overflow handling. Recalculation reduces metadata but adds arithmetic and requires stable hash information.

**Insertion carries a complete entry.** Construct or otherwise prepare `(key,value,full_hash,DIB=0)` under the language's lifetime rules. At each candidate:

1. EMPTY: publish the carried payload and metadata, increment size, finish.
2. Equivalent resident: update/reject according to map semantics, finish without size change.
3. Resident DIB lower than carried DIB: exchange the entire logical entries, including cached hash/fingerprint, value ownership, and distance; the evicted resident continues.
4. Otherwise: the same carried entry continues.

After either nonterminal case, advance one slot cyclically and increment the carried entry's DIB. A common bug swaps distance fields, then increments the new resident rather than the evicted carried entry. Expressing the loop around a single “carried entry” object makes ownership and distance easier to audit.

At most `m` distinct slots may be examined. A production table grows before becoming full, but an explicit bound turns a violated reserve, corrupt metadata, or maximum-capacity condition into a controlled error. Distance metadata must represent every permitted DIB. If a stored eight-bit or truncated value approaches its sentinel/limit, grow, rebuild with a different seed/capacity, widen metadata, or fail; wrapping destroys search correctness.

**Swaps redistribute, not conjure capacity.** Under linear probing, insertion still ends at an EMPTY in the cluster it reaches; swaps decide which key owns intervening slots. Robin Hood aims to reduce disparity between keys' displacements. It can increase one formerly fortunate key's cost while decreasing the incoming key's prospective cost. It adds move/swap traffic and may touch large payloads.

Do not say it unconditionally reduces average successful probes. The cited random-probing analysis explicitly notes that expected search cost can be independent of collision discipline while variance changes dramatically. For a linear implementation, occupancy patterns, clustering, cache locality, hash quality, deletion history, and load determine measured means and tails. Report the distribution actually observed.

**Lookup has an extra absence witness.** Search key `k` from home with current distance `d=0,1,...`. At each slot:

- EMPTY proves absence.
- An equal live key proves presence.
- In a valid tombstone-free linear Robin Hood table, resident DIB `<d` proves absence.
- Otherwise continue, bounded by `m`.

Why does the distance comparison work? Consider the sought key's hypothetical insertion path. On reaching this slot with distance `d`, it would have displaced a resident whose DIB was smaller. Later valid Robin Hood insertions cannot leave that lower-age barrier in front of an existing higher-age copy of the sought key. The invariant is about the relationship between a search's current distance and the encountered resident; it is not the false claim that DIBs never decrease anywhere in a cluster. Slots with homes inside an existing occupied run can contain DIB zero after positive-DIB entries.

Equality must use the full contract. A fingerprint or cached hash only filters. Equivalent keys must have compatible hashes, and an indexed key's hash/equality state must not mutate. Lookup checks equality for plausible candidates before concluding from later slots. Metadata corruption must not become memory-unsafe traversal.

**Ordinary tombstones complicate early stop.** A DELETED slot has no resident DIB to compare, yet may hide a later live key. Treating it as EMPTY is wrong; giving it an arbitrary small DIB can cause false absence; giving it a large sentinel preserves continuation but can degrade searches and insertion ordering. Research analyzes specific lazy-deletion models, but their results and algorithms must be implemented exactly.

For a practical linear Robin Hood table whose values can be safely moved, backward-shift deletion avoids tombstones. Locate the key under the normal search theorem, destroy or move out its payload, and make its index the hole. Inspect the next cyclic slot:

- EMPTY: stop and leave the hole EMPTY.
- OCCUPIED with DIB zero: stop; moving it backward would put it before its home.
- OCCUPIED with DIB positive: move it into the hole, decrement its DIB, make its old slot the new hole, and continue.

Each move preserves the entry's linear probe path because the new slot is exactly one step closer to home. Stopping at DIB zero preserves that entry and separates the repair boundary. The final operation reduces live size once and creates no tombstone. It may relocate many entries and invalidate references/iterators to each moved payload.

**Failure safety is a first-class cost.** Robin Hood insertion may mutate multiple resident slots before discovering EMPTY. If key/value swap or move can throw/fail, a half-completed eviction chain can lose entries, duplicate ownership, or mismatch metadata. Strong safety can require no-throw move/swap types, node indirection, precomputed hashes, a relocation log with rollback, copy-on-write storage, or a more conservative algorithm.

Pre-grow before beginning the chain so allocation is not discovered at its end. Construct the new payload before publishing it. If equality/hash callbacks can fail, define which operations invoke them and whether prior swaps are possible. Many generic C++ implementations condition their strong guarantee on no-throw movement; a custom container must document an equally precise condition.

Backward-shift deletion has similar concerns. Moving entry `i+1` into hole `i` must not destroy the only valid copy before construction succeeds. Trivially relocatable payloads make this cheap; nontrivial types require ordered move/destroy and an exception policy. Node-indirected variants move pointers/indices rather than values, trading allocation and indirection for stable payload addresses and simpler relocation.

**Layout determines what a swap costs.** A flat array can store `(metadata,key,value)` together, but probing and relocation move/inspect large values. Separate metadata stores DIB plus fingerprints compactly; candidate equality then accesses payload. A node layout keeps values stable but pays pointer and allocation costs. A dense-payload layout stores `(key,value)` in a vector and keeps bucket-to-vector indices with DIB/fingerprint; iteration is dense, but erase may move the last payload and update its bucket index.

Current Tessil `robin-map` describes open-addressed linear Robin Hood hashing with backward-shift deletion and offers power-of-two and prime growth policies. Its source records a distance field and explicitly conditions strong exception guarantees on nothrow-swappable/move-constructible values. Current `ankerl::unordered_dense` describes a dense payload array plus bucket metadata containing distance, fingerprint, and payload index. These are scoped implementations, not proof that one layout or threshold is universally best.

Current Abseil/Go/Rust tables are useful non-Robin-Hood contrasts. In particular, a 2018 concurrency paper states that Rust had adopted Robin Hood, but current Rust `HashMap` documentation says quadratic probing and SIMD lookup. Historical observations must not be silently promoted to current API facts.

**Resize rebuilds displacement from zero.** Select a legal new capacity with checked arithmetic, allocate and initialize the new representation, and reinsert every live entry using its full hash. Each entry starts DIB zero in the new table; copying an old DIB or physical slot is invalid because home and cluster shape change. Publish only after exact-once construction succeeds.

Growth triggers should consider prospective live load, measured DIB maximum/percentiles, metadata distance limit, memory budget, and EMPTY reserve. A long displacement at low load may indicate a poor hash or adversarial input; blindly doubling can waste memory without repairing distribution. A seed change or prime growth policy may be appropriate only under an explicit hash/security contract. Shrink needs hysteresis to avoid relocation oscillation.

Iteration over a flat bucket array is `O(m)`, not `O(n)`, and skips EMPTY. Dense-payload variants can iterate `O(n)` but define different erase order/invalidation. Insertion swaps, deletion shifts, resize, and seed change can move entries. Stable references require node indirection or a documented operation-specific guarantee. Never serialize raw buckets, DIBs, seeds, fingerprints, or iteration order as an unversioned logical map.

**The classic theory is powerful and narrow.** Celis's thesis introduces the displacement-balancing rule and analyzes random probe sequences. Later work derives bounded-variance results and mean-centered search under asymptotic random-probing models. The expected successful search cost in one cited insertion-only random-probing model is `(1/alpha) ln(1/(1-alpha))`, independent of the compared collision disciplines, while Robin Hood concentrates its distribution. Deletion analyses specify particular random insert/delete and tombstone models.

Those results do not certify linear probing, finite capacities, a particular hash family, backward-shift deletion, grouped metadata, cache behavior, user equality, or hostile inputs. “Less than 2.6 probes near full” belongs to a particular original search/model construction, not a default production prediction. Preserve theorem assumptions next to every quantitative claim.

**Concurrency multiplies the relocation problem.** An insertion can swap a chain, deletion can shift a chain, and resize changes all homes. A reader may see metadata from one entry and payload from another. Per-slot atomic writes do not make a multi-slot transformation linearizable or safe for object lifetime.

The cited concurrent Robin Hood research uses a specific multiword-update construction and analyzes its progress/synchronization model. A production design must define linearization points, versioning/validation, helping or locks, memory order, ABA defense, resize cooperation, iteration/snapshot semantics, cancellation, and reclamation. Do not label a sequential Robin Hood map concurrent because its distance byte is atomic.

**Hostile hashes defeat fairness.** If all keys share a home, Robin Hood can equalize their displacements but must still build a long cluster. Per-operation worst case remains linear; repeated construction can be quadratic. A narrow distance limit may become an attacker-controlled failure path. Random/keyed hashing, input and time limits, collision/DIB telemetry, alternate structures, capacity ceilings, and operational defenses are complementary.

Test with a reference map plus structural oracle. Generate put/update/get/delete/reserve/rebuild sequences and compare contents. After each operation check size, initialized payloads, key uniqueness, correct home/DIB, bounded lookup of every live and sampled absent key, no premature early stop, and no distance overflow. Enumerate small tables and all insertion orders where feasible.

Force empty/singleton, home at the last slot, wrap, equal homes, alternating homes, ties, repeated swaps, duplicate during an eviction chain, early-stop miss, delete head/middle/tail, next entry DIB zero, shift across wrap, nearly full/full, resize, maximum distance, constant/structured hashes, mutable keys, and allocation/hash/equality/move/destructor failures. Use sanitizers or language lifetime tools for nontrivial payloads.

Benchmark realistic and adversarial workloads across live loads, hits/misses, updates/deletes, churn, resize and deletion-shift boundaries, element sizes, flat/node/dense layouts, hash cost/quality, cache/branch behavior, memory, throughput, and latency percentiles. Record probes, equality calls, swaps per insertion, shifts per deletion, DIB mean/variance/maximum/percentiles, bytes moved, and failures. Compare against linear, quadratic, double, grouped, cuckoo, and chaining designs under identical semantics and budgets.

The executable trace below verifies a finite linear Robin Hood swap chain, early-stop miss, backward-shift deletion, reinsertion, counts, DIB correctness, uniqueness, and reachability. It makes no performance or generic lifetime claim.

<!-- bijux-verify: {"id":"robin-hood-displacement-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"keys_before=0,8,16,1\ndib_before=0,1,2,2\ninsertion_swaps=2\nmiss_probes_before=4\ndeleted=EIGHT\nkeys_after=0,16,1,9\ndib_after=0,1,1,2\nlookup_one_probes=2\nsize=4\ninvariant=True\nevidence=finite_robin_hood_trace\n","stderr":""}} -->
```python
EMPTY = object()


class RobinHoodMap:
    def __init__(self, capacity):
        self.slots = [EMPTY] * capacity
        self.size = 0

    def put(self, key, value):
        capacity = len(self.slots)
        carried = [key, value, hash(key) % capacity, 0]
        index = carried[2]
        swaps = 0
        for _ in range(capacity):
            resident = self.slots[index]
            if resident is EMPTY:
                self.slots[index] = carried
                self.size += 1
                return True, swaps
            if resident[0] == key:
                resident[1] = value
                return False, swaps
            if resident[3] < carried[3]:
                self.slots[index], carried = carried, resident
                swaps += 1
            index = (index + 1) % capacity
            carried[3] += 1
        raise OverflowError("table contains no empty slot")

    def locate(self, key):
        capacity = len(self.slots)
        index = hash(key) % capacity
        distance = 0
        for probes in range(1, capacity + 1):
            resident = self.slots[index]
            if resident is EMPTY or resident[3] < distance:
                return None, probes
            if resident[0] == key:
                return index, probes
            index = (index + 1) % capacity
            distance += 1
        return None, capacity

    def get_with_probes(self, key):
        index, probes = self.locate(key)
        if index is None:
            return None, probes
        return self.slots[index][1], probes

    def delete(self, key):
        index, _ = self.locate(key)
        if index is None:
            raise KeyError(key)
        value = self.slots[index][1]
        hole = index
        capacity = len(self.slots)
        next_index = (hole + 1) % capacity
        while self.slots[next_index] is not EMPTY and self.slots[next_index][3] > 0:
            moved = self.slots[next_index]
            moved[3] -= 1
            self.slots[hole] = moved
            hole = next_index
            next_index = (next_index + 1) % capacity
        self.slots[hole] = EMPTY
        self.size -= 1
        return value

    def invariant(self):
        live = [slot for slot in self.slots if slot is not EMPTY]
        if len(live) != self.size or len({slot[0] for slot in live}) != self.size:
            return False
        capacity = len(self.slots)
        for index, slot in enumerate(self.slots):
            if slot is EMPTY:
                continue
            if slot[2] != hash(slot[0]) % capacity:
                return False
            if slot[3] != (index - slot[2]) % capacity:
                return False
            located, _ = self.locate(slot[0])
            if located != index:
                return False
        return True


table = RobinHoodMap(8)
swaps = 0
for key, value in ((0, "ZERO"), (1, "ONE"), (8, "EIGHT"), (16, "SIXTEEN")):
    inserted, operation_swaps = table.put(key, value)
    assert inserted
    swaps += operation_swaps

keys_before = [slot[0] for slot in table.slots if slot is not EMPTY]
dib_before = [slot[3] for slot in table.slots if slot is not EMPTY]
_, miss_probes = table.get_with_probes(24)
deleted = table.delete(8)
assert table.put(9, "NINE")[0]
keys_after = [slot[0] for slot in table.slots if slot is not EMPTY]
dib_after = [slot[3] for slot in table.slots if slot is not EMPTY]
one, one_probes = table.get_with_probes(1)
assert one == "ONE" and not table.put(1, "ONE")[0]

print("keys_before=" + ",".join(map(str, keys_before)))
print("dib_before=" + ",".join(map(str, dib_before)))
print(f"insertion_swaps={swaps}")
print(f"miss_probes_before={miss_probes}")
print(f"deleted={deleted}")
print("keys_after=" + ",".join(map(str, keys_after)))
print("dib_after=" + ",".join(map(str, dib_after)))
print(f"lookup_one_probes={one_probes}")
print(f"size={table.size}")
print(f"invariant={table.invariant()}")
print("evidence=finite_robin_hood_trace")
```

## Definitions and Notation

- `m`: positive slot capacity; `n`: live entry count; `alpha=n/m`.
- `home(k)`: reduced full hash at current capacity.
- `DIB(k,j)=(j-home(k)) mod m`: cyclic linear distance for key `k` stored at `j`.
- **carried entry**: incoming or evicted complete entry currently seeking a slot.
- **resident**: live entry currently owning the candidate slot.
- **Robin Hood swap**: exchange when `resident_DIB<carried_DIB`.
- **early stop**: absence conclusion when EMPTY or `resident_DIB<search_DIB` under the stated invariant.
- **backward-shift deletion**: repeated one-slot earlier relocation of positive-DIB successors.
- **DIB distribution**: mean, variance, maximum, percentiles, or tail probabilities across live keys.
- **random probing model**: each key receives a model-defined random probe sequence; distinct from linear probing with a random home.

## Mechanisms, Invariants, or Proof Structure

Insertion correctness treats the carried entry as a loop invariant: its home/hash/value/DIB describe the current candidate. A swap installs the farther-displaced entry and transfers complete ownership/state of the resident to the carried variable. Advancing increments only the carried DIB. EMPTY publication adds exactly one live entry; equality changes no membership.

Lookup correctness uses reachability plus Robin Hood ordering. EMPTY is the usual historical absence witness. In a tombstone-free linear table, a resident poorer in neither age nor distance—specifically resident DIB below current search DIB—shows the target could not have passed without taking that slot. The rule does not require globally sorted DIBs.

Deletion correctness maintains a moving hole. A following entry with positive DIB can move one step closer to home; decrementing DIB restores exact metadata. EMPTY or DIB zero terminates the shift. Resize correctness is exact-once reinsertion with DIB reset, failure-safe construction, and post-success publication.

## Alternatives and Trade-Offs

| Design | Strength | Cost or obligation |
|---|---|---|
| First-come linear probing | few insertion moves | unequal displacement and cluster tails |
| Linear Robin Hood | tighter displacement, early miss stop | swaps, shift deletion, invalidation |
| Tombstone Robin Hood | simpler physical erase | early-stop metadata and churn analysis |
| Flat payload | locality and one allocation | moves large/nontrivial values |
| Node-indirected payload | stable values/easier swaps | allocations and pointer/cache cost |
| Dense payload plus bucket indices | dense iteration and small buckets | erase index repair and order changes |
| Grouped fingerprint table | vector candidate filtering | different invariant; not automatically Robin Hood |
| Chaining/tree table | simple deletion/stable nodes possible | pointers, allocation, or comparison cost |

## Failure Modes and Misconceptions

- **“Robin Hood is a better hash.”** It is an insertion/collision discipline layered on hashing and probing.
- **“Swap only key and value.”** cached hash, fingerprint, DIB, ownership, and auxiliary metadata travel too.
- **“Increment both distances after a swap.”** only the evicted carried entry advances.
- **“DIBs are sorted across each cluster.”** a resident at its home can follow displaced entries.
- **“Any DIB decrease proves absence.”** compare resident DIB to this query's current search distance under the valid variant.
- **“Tombstones preserve every early stop.”** their distance semantics require a separate algorithm/proof.
- **“Backward shift crosses a home entry.”** DIB zero is a repair boundary.
- **“A byte of DIB is enough because loads are capped.”** bad hashes can overflow distance at low load.
- **“Robin Hood lowers average cost by definition.”** its defining action redistributes displacement; models and workloads determine means.
- **“Classic constants apply to linear maps.”** cited theory often assumes random probe sequences.
- **“Atomic metadata makes swaps concurrent.”** multi-slot publication and lifetime remain.
- **“High load is safe because variance is low.”** means, misses, movement, EMPTY reserve, and adversaries still matter.

## Worked Examples

### Example 1

In `m=8`, keys 0 and 1 occupy homes 0 and 1. Key 8 reaches slot 1 at DIB 1 while key 1 has DIB 0, so 8 steals slot 1 and 1 continues to slot 2 at DIB 1. Conclusion: the poorer key receives collision priority.

### Example 2

After keys `0,1,8`, inserting 16 reaches slot 2 at DIB 2 and evicts key 1 at DIB 1. Final DIBs are `0,1,2,2`. Conclusion: one insertion can relocate multiple logical entries.

### Example 3

Searching missing key 24 from home zero sees DIBs 0,1,2, then resident 2 at query distance 3 and stops. Conclusion: early absence can precede EMPTY.

### Example 4

Keys with homes 0,0,2 can have DIBs 0,1,0 in one occupied run. Conclusion: global nondecreasing DIB is not the lookup theorem.

### Example 5

Deleting slot 1 from DIB sequence `0,1,2,2` shifts following entries to produce `0,1,1` and stops at EMPTY. Conclusion: each moved entry becomes exactly one probe closer.

### Example 6

If the next resident after a hole has DIB zero, shifting it backward would place it before home and lookup would start after it. Conclusion: backward shift stops at zero.

### Example 7

A seven-bit distance field reaches its maximum under constant-hash input while live load is modest in a large table. Conclusion: load factor alone cannot protect metadata width.

### Example 8

Swapping a 4 KiB inline value through twelve slots moves far more bytes than swapping twelve eight-byte node pointers. Conclusion: probe count is not total insertion cost.

### Example 9

Growing from 8 to 16 changes key 9's home from 1 to 9; its old DIB and slot are meaningless. Conclusion: rebuild starts every entry at its new home/DIB zero.

### Example 10

A benchmark reports lower DIB variance but higher insertion p99 because backward shifts move large values during delete-heavy churn. Conclusion: selection requires operation- and workload-level evidence.

## Cross-Program Connections

- **Algorithms:** exchange arguments, distribution tails, random models, and adversarial bounds separate fairness from mean work.
- **Programming languages:** move/swap failure, destruction, ownership, generics, and borrow/reference rules govern relocation chains.
- **Computer architecture:** flat metadata, payload size, cache lines, branches, and bytes moved determine realized cost.
- **Software engineering:** invariants span hash, probe, metadata, resize, and failure boundaries and need model-based regression tests.
- **Database engineering:** hash-join/build skew and delete churn require tail, memory, and spill evidence, not only average lookup.
- **Concurrent programming:** insertion and deletion are multi-slot transactions requiring versioning, linearization, and reclamation.
- **Security engineering:** equal-home attacks can exhaust DIB width and CPU despite fair displacement.

## References

1. Pedro Celis, [Robin Hood Hashing](https://cs.uwaterloo.ca/research/tr/1986/CS-86-14.pdf). Primary thesis introducing the collision discipline, search, analysis, and deletion considerations under its stated model.
2. Michael Mitzenmacher, [A New Approach to Analyzing Robin Hood Hashing](https://arxiv.org/abs/1401.7616). Primary random-probing analysis for insertion-only and specified deletion processes.
3. Patricio V. Poblete and Alfredo Viola, [Robin Hood Hashing Really Has Constant Average Search Cost and Variance in Full Tables](https://arxiv.org/abs/1605.04031). Primary asymptotic random-probing variance, mean-centered search, and tombstone-deletion analysis.
4. Robert Kelly, Barak A. Pearlmutter, and Phil Maguire, [Concurrent Robin Hood Hashing](https://arxiv.org/abs/1809.04339). Primary concurrency design showing the multi-location update and validation problem.
5. Tessil, [`robin-map`](https://github.com/Tessil/robin-map). Current linear Robin Hood/backward-shift implementation documentation and growth/layout API considerations.
6. Tessil, [`robin_hash.h`](https://github.com/Tessil/robin-map/blob/master/include/tsl/robin_hash.h). Current primary implementation source for distance metadata, movement, growth, and conditional exception guarantees.
7. Martin Ankerl, [`unordered_dense`](https://github.com/martinus/unordered_dense). Current dense payload plus distance/fingerprint/index Robin Hood design and backward-shift deletion.
8. Rust Project, [`std::collections::HashMap`](https://doc.rust-lang.org/std/collections/struct.HashMap.html). Current quadratic/SIMD implementation statement used to reject stale claims that Rust currently specifies Robin Hood hashing.
9. ISO C++ working draft, [Unordered Associative Container Requirements](https://eel.is/c%2B%2Bdraft/unord.req.general). Observable equality/hash, complexity, rehash, iterator/reference, and exception requirements without a mandated collision discipline.
10. Scott A. Crosby and Dan S. Wallach, [Denial of Service via Algorithmic Complexity Attacks](https://www.usenix.org/legacy/event/sec03/tech/full_papers/crosby/crosby.pdf). Primary collision-driven resource-attack evidence.

## Exercises

### Exercise 1

Write language-neutral linear Robin Hood map pseudocode for find, insert/update, and bounded failure. State carried-entry ownership, equality order, swap rule, DIB update, metadata width, slot publication, size changes, and exception requirements.

### Exercise 2

Prove the early unsuccessful-search rule without assuming globally nondecreasing DIBs. Give a valid occupied-run example whose DIB decreases, and explain why the query-relative comparison still stops correctly.

### Exercise 3

Prove backward-shift deletion preserves lookup and DIB metadata across wraparound. Identify its stop conditions and design a failure/lifetime strategy for nontrivially movable values.

### Exercise 4

Design a flat, node-indirected, or dense-payload Robin Hood map for a workload with large values, stable-reference requirements, deletes, and untrusted keys. Justify distance width, hash storage, growth/reseed policy, iteration, serialization, and observability.

### Exercise 5

Design differential/property tests and a benchmark that distinguish mean, variance, maximum, p99, swaps, shifts, bytes moved, memory, and failure behavior. Explain how you will keep random-probing theory separate from measured linear Robin Hood results.

## Answers to the Exercises

### Answer 1

Require positive capacity, one reserved EMPTY or an explicit `m`-probe failure, stable key hash/equality, and representable DIB. Find starts at home with distance zero: EMPTY returns absent; equality returns the entry; resident DIB below query distance returns absent; otherwise advance/increment within `m`. Insert constructs a complete carried entry at DIB zero. EMPTY publishes and increments size; equality updates/rejects; lower resident DIB swaps the entire entry state, leaving the evicted resident carried; then advance and increment only carried DIB. Pre-grow and check the distance limit before destructive relocation. Strong failure safety requires no-throw swaps/moves or rollback/indirection/transactional storage; payload is never marked live before successful construction. Full-cycle exhaustion grows or reports without looping.

### Answer 2

Suppose a sought key would reach slot `j` at distance `d`, but the current resident has `r<d`. During a valid insertion of the sought key, reaching that slot would cause it to displace the lower-DIB resident; subsequent valid operations preserve the query-relative barrier. Hence the sought key cannot occur later. Global monotonicity is unnecessary: homes 0,0,2 can occupy slots 0,1,2 with DIBs 0,1,0. A query from home zero reaches slot 2 at distance two, sees resident DIB zero, and correctly stops; a query for the home-two resident starts at slot 2 and finds equality at distance zero.

### Answer 3

After removing slot `h`, inspect `s=h+1 mod m`. If `s` is EMPTY, leave `h` EMPTY. If its resident DIB is zero, leave `h` EMPTY because moving that resident would precede home. Otherwise move the complete resident to `h`, decrement DIB, make `s` the hole, and repeat. Each move replaces a key's current position with the immediately preceding position on its linear probe path, so reachability is preserved across wrap; the final EMPTY/zero boundary prevents crossing another home. Decrement size once. For nontrivial values, require no-throw relocation, move pointers/indices, use a rollback log/basic guarantee, or choose tombstones; order construction, metadata publication, and destruction so one valid owner remains.

### Answer 4

Stable references plus large values favor node indirection: buckets store pointer/index, cached hash/fingerprint, and sufficiently wide DIB; nodes own payloads. This adds allocation and pointer traffic but makes swap/shift cheap and can preserve node addresses until erase. Use keyed/randomized high-quality hashing for untrusted keys, checked power-of-two or prime growth matched to reduction, a hard DIB limit that triggers governed grow/reseed/failure, and live/probe/memory thresholds with hysteresis. State iterator and node/reference invalidation separately. Serialize logical key/value entries plus format semantics, never raw slots, seeds, or DIB. Observe load, DIB distribution, probes, equality, swaps, shifts, bytes moved, allocations, resize/reseed/failure, memory, and latency; enforce input/time/capacity limits.

### Answer 5

Generate put/update/get/delete/reserve/rebuild against a reference map and inspect size, unique keys, home/DIB, reachability, early-stop soundness, destruction, and rollback after every operation. Exhaust small capacities/insertion orders; force wrap, ties, DIB decreases, swap chains, duplicate updates, deletion boundaries, distance overflow, poor hashes, and injected failures. Benchmark identical semantics and memory budgets across realistic/adversarial hashes, load sweeps, hit/miss/churn mixes, payload layouts/sizes, resize and shift boundaries, seeds, and hardware/toolchains. Report mean/variance/max/p50/p95/p99 probes, swaps/insertion, shifts/deletion, bytes moved/hashed, equality calls, cache/branch behavior, allocations/memory, throughput, latency, repetitions, uncertainty, and raw artifacts. Cite random-probing equations only as model predictions; label linear Robin Hood numbers as measurements for the exact implementation and workload.
