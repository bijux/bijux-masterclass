---
module_id: DSE-023
program: Data Structures Engineering
level: 1
module_number: 23
title: Linear Probing
status: complete
last_verified: 2026-08-29
---

# Linear Probing

## One-Page Review

### Governing question

How can one contiguous table resolve collisions by unit-step probing while preserving termination, reachability, duplicate prevention, deletion, load, clustering, resizing, object lifetime, and hostile-input contracts?

### Essential definitions

- **open addressing** stores entries inside the primary slot array; a probe sequence examines candidate slots.
- **linear probing** uses `p_j=(home+j) mod m` for `j=0,...,m-1`.
- A slot is **EMPTY**, **OCCUPIED**, or **DELETED/tombstone** under tombstone deletion.
- The **home** slot is the initial reduced full hash.
- **probe distance/displacement** is the cyclic distance from home to current slot.
- A **cluster/run** is a maximal cyclic sequence of non-EMPTY slots.
- **primary clustering** is the growth/merging of contiguous occupied runs because any insertion entering a run extends it at the same exit.
- **live load** is `α=n/m`; **used/fill load** includes tombstones when they consume search/insertion structure.
- **backward-shift deletion** moves eligible following entries toward home to close a hole without tombstones.
- A **probe bound** stops after at most m distinct slots, preventing infinite loops in full/corrupt tables.

### Central model, mechanism, or theorem

For capacity `m>0` and home `q`, linear probe order is

\[
p_j=(q+j)\bmod m,\quad 0\le j<m.
\]

This visits every slot exactly once because `p_a=p_b` implies `a≡b (mod m)`, and `|a-b|<m`. Search may stop unsuccessfully at the first EMPTY because an insertion following the same sequence could not have placed the key beyond an always-empty slot. It may not stop at DELETED, which may have held an earlier link in reachability.

Under the ideal uniform-home model and limiting assumptions for large tables, classic approximations are successful probes about `1/2(1+1/(1-α))` and unsuccessful/insertion probes about `1/2(1+1/(1-α)^2)`. These describe pure linear probing under that model, not arbitrary hash families, tombstone histories, or modern grouped tables.

### Critical invariants

1. Every live key appears once and is reachable from home before an EMPTY terminator.
2. EMPTY, DELETED, and OCCUPIED metadata agree with object initialization and live/used counts.
3. Lookup compares equality for candidates, crosses tombstones, and terminates within m probes.
4. Unique insertion scans far enough to find an existing equal key before committing into the earliest reusable tombstone.
5. Deletion preserves reachability by tombstone or a proved backward-shift transformation.
6. At least one terminating EMPTY exists whenever algorithms rely on finding one rather than an explicit m-probe bound.
7. Resize/rebuild inserts every live entry exactly once and removes tombstones under the new placement.
8. Iterator/reference, allocation, failure, concurrency, and security policies match relocation and slot lifetime.

### Common failures

- Treating DELETED as EMPTY and making later cluster entries unreachable.
- Inserting immediately into the first tombstone without searching for an existing equal key.
- Omitting a full-cycle bound when no EMPTY remains.
- Counting only live load while tombstones make nearly every slot non-EMPTY.
- Clearing a removed payload but forgetting to mark metadata, or marking reusable before destruction is safe.
- Backward-shifting every following entry without checking whether the hole lies on its cyclic home-to-position path.
- Rehashing by copying physical slots rather than reinserting from full hashes.
- Applying idealized probe formulas to poor hashes, finite high load, deletions, or non-linear group probes.
- Assuming contiguous layout guarantees good locality despite long clusters, large values, or separate payload storage.
- Calling CPython/Rust/Swiss tables “linear probing” when their current documented probe schemes differ.

### Compact example

In seven slots with identity hashes, keys 0,7,14 occupy slots 0,1,2. Deleting 7 leaves a tombstone at 1; lookup 14 crosses it. Key 21 must remember slot 1 but continue through 14 until EMPTY slot 3 proves 21 absent, then reuse 1. A missing key 28 probes slots 0,1,2,3 and stops at EMPTY after four comparisons of metadata. The executable trace also includes key 3 at slot 3, so its miss stops at slot 4 after five probes.

### Connections

[DSE-021](021-hash-functions-and-distribution.md) supplies hash/reduction assumptions and [DSE-022](022-separate-chaining.md) provides the collision-layout contrast. The [program roadmap](../ROADMAP.md) next changes probe sequences with quadratic probing and double hashing, then studies Robin Hood displacement.

## Governing Question

Which slot-state machine, probe termination proof, deletion method, load/rebuild policy, and evidence make pure linear probing correct and predictable for its actual keys and workload?

## Why This Matters

Linear probing replaces node chains with a compact array and sequential access. Metadata and entries can fit cache lines; allocation can be one block; traversal is simple. For friendly hashes and moderate load, these properties can make it exceptionally fast.

The same unit-step rule couples neighboring keys. A run attracts every insertion whose home lies in or immediately before it, then grows and merges. Deletion cannot simply create EMPTY in the middle because searches use EMPTY as proof of absence. High live load or accumulated tombstones makes misses expensive. Entries move on resize and sometimes deletion, affecting addresses and iterators.

Production tables often adapt these ideas with control bytes, fingerprints, groups, quadratic/group probing, Robin Hood policies, or separate dense entries. This module deliberately studies pure linear probing so later variations have a precise baseline. Current runtime observations are contrasts, not evidence for the baseline algorithm.

## Prerequisites and Retrieval

Retrieve ADT/invariant/failure tools from [DSE-001](001-abstract-data-types-and-concrete-representations.md), [DSE-002](002-representation-invariants.md), and [DSE-003](003-operation-contracts.md); cost/layout/locality tools from [DSE-004](004-time-space-and-allocation-cost.md), [DSE-005](005-contiguous-and-linked-layouts.md), and [DSE-006](006-memory-locality-and-cache-behavior.md); generic lifetime, iteration, testing, and benchmarking from [DSE-007](007-genericity-and-type-constraints.md), [DSE-008](008-iterators-and-traversal-protocols.md), [DSE-009](009-property-based-testing-of-data-structures.md), and [DSE-010](010-benchmarking-a-structure-without-misleading-results.md); and hash/distribution plus chaining from [DSE-021](021-hash-functions-and-distribution.md) and [DSE-022](022-separate-chaining.md).

## Learning Objectives

After completing this module, you should be able to:

1. prove the unit-step probe visits every slot and terminates;
2. derive lookup and unique insertion across EMPTY/OCCUPIED/DELETED states;
3. explain primary clustering and load-sensitive probe growth;
4. distinguish live size, used/fill count, capacity, tombstones, and growth-left;
5. implement tombstone deletion without losing reachability or creating duplicates;
6. derive the condition for backward-shift deletion on a cyclic table;
7. design resize/rebuild, exception/lifetime, and invalidation behavior;
8. contrast pure linear probing with grouped, quadratic, perturbation, Robin Hood, and chained designs;
9. test probe histories, wrap, full tables, deletion churn, and hostile hashes;
10. benchmark probe distributions and complete operation costs rather than throughput alone.

## Core Exposition

**Model slots as a state machine.** A basic table has m slots, each EMPTY, OCCUPIED(key,value,optional full hash), or DELETED. Empty storage contains no live key/value. Deleted storage contains no live payload but records that the probe path may continue. Occupied storage owns exactly one initialized entry.

Maintain `0<=n<=u<=m`, where n is occupied count and u is non-EMPTY count (occupied plus tombstones) for a simple tombstone design. Some implementations count growth capacity differently, but names and update rules must remain exact. Live load is n/m; fill load is u/m.

For unique maps, equality/hash/key immutability rules from DSE-021 remain. A hash match/fingerprint only filters; equality confirms. Mutating an indexed key can change home and make it unreachable.

**The probe is a cyclic permutation.** Starting at home q, examine q,q+1,... modulo m. For j in `[0,m)`, no position repeats. An explicit loop bound m is therefore sufficient to distinguish absent/full/corrupt rather than spin forever. If the design maintains at least one EMPTY and loops until EMPTY, prove all insert/resize/deletion policies preserve that reserve.

Lookup behavior by state:

- EMPTY: the key is absent; stop.
- DELETED: continue; there may be a live equal key later.
- OCCUPIED: compare stored hash if used, then equality; return on match, otherwise continue.

Why can EMPTY stop? Any insertion of the target following the same probe would have used that slot when it was first EMPTY, unless later deletion incorrectly changed a necessary predecessor to EMPTY. This historical reachability fact is the heart of deletion.

**Insertion has a remembered tombstone.** Probe from home and remember the first DELETED index, but continue. If an equivalent OCCUPIED key appears, update/reject it. At the first EMPTY, commit into the remembered tombstone if any, otherwise the EMPTY slot. If the full cycle has no match/EMPTY, reuse a remembered tombstone or report/grow; if none exists, the table is full.

Stopping at the first tombstone and inserting can create duplicate equivalent keys when the original lies later. That breaks size, lookup/update, and erase semantics. Construction/allocation should happen before slot publication; metadata changes to OCCUPIED only after payload initialization. On failure, the original tombstone/empty state remains.

When inserting into EMPTY, increment n and u. When reusing DELETED, increment n but not u. Updating an existing value changes neither. These distinctions drive rebuild/growth policy.

**Deletion with tombstones is simple but accumulative.** Find the exact entry, destroy/move out the value and key under the language's lifetime rules, mark DELETED, decrement n, and leave u unchanged. Metadata must not announce DELETED before concurrent/exceptional readers are excluded and payload cleanup is safely sequenced.

Tombstones preserve reachability but make misses and insert searches cross dead history. Repeated insert/delete churn can leave n small and u near m. Trigger a same-size rebuild based on used count, tombstone ratio, or measured probes; growth based on prospective live/fill capacity; shrink under hysteresis. One threshold does not suit all layouts.

**Backward-shift deletion removes tombstones.** After creating a hole at d, scan forward until EMPTY. For an occupied entry at position s with home h, move it backward into the hole only if the hole lies on its cyclic probe interval from h to s. Then s becomes the new hole and scanning continues.

Define cyclic distance `dist(a,b)=(b-a) mod m`. Entry at s may move to d when `dist(h,d)<dist(h,s)`: d is an earlier position it would have probed. Moving an entry whose home occurs after the hole in cyclic order can place it before its search starts and make it unreachable. Wrap-aware distance avoids brittle non-cyclic comparisons.

Stop at EMPTY because later entries belong to another cluster. Moves require safe payload relocation, cached hash preservation, iterator/reference invalidation, and exception strategy. For types whose move can fail, a table may prefer tombstones or indirection. Variants such as Robin Hood backward-shift deletion add displacement-order assumptions and belong in DSE-025.

**Primary clustering is self-reinforcing.** A cluster is a maximal cyclic interval containing no EMPTY. Any key whose probe enters the cluster exits at the same first EMPTY, extending it. Two growing clusters merge when the gap fills. Thus probe costs grow faster than the independent-slot intuition as α approaches one.

Under an idealized uniform independent home model, classic large-table approximations show successful probes increasing roughly with `1/(1-α)` and unsuccessful probes with `1/(1-α)^2`. At α=0.5 they predict about 1.5 successful and 2.5 unsuccessful probes; at α=0.9, about 5.5 and 50.5. These are analytical warnings, not promises or measurements.

Finite capacity, hash independence, unsuccessful key distribution, tombstones, resizing, and cache groups change results. Research on k-independence shows linear probing's expected performance needs stronger assumptions than pairwise-universal intuition; Thorup's notes review expected constant time with 5-independent hashing and known lower-independence failures.

**Layout trades locality against movement.** AoS slots colocate key/value/metadata but scanning large values wastes bandwidth. Separate control bytes let probes inspect compact metadata/fingerprints before touching payloads. SoA or indirection can reduce scan traffic and preserve value addresses at pointer/allocation cost.

Swiss-table designs use control metadata, hash fragments, SIMD/group candidate scans, and a non-unit group probe. They preserve the EMPTY-versus-DELETED insight but are not pure linear probing. Current Rust `HashMap` describes quadratic probing plus SIMD lookup. Current CPython dict source describes a perturbation recurrence; current CPython set source combines bounded linear runs with perturbation. The legacy archive's blanket “production open addressing is linear probing/Robin Hood/SipHash perturbation” claims are therefore not retained.

OpenJDK's current `IdentityHashMap` is a useful scoped pure-linear example with alternating key/value array cells and reference equality. Its identity semantics are deliberately not a general `Map` equality substitute. Its documentation/source, not an analogy, governs null markers, close deletion, resizing, iteration, and synchronization.

**Resize is full reinsertion.** Before an insertion would violate the live/fill/EMPTY policy, choose new m using checked arithmetic and maximums, allocate storage, then insert every live entry according to full hash and new reduction. Tombstones do not transfer. Commit the new table only when all entries are represented exactly once.

Copying physical positions is incorrect because homes and clusters depend on m. If hashing callbacks or moves can fail, preserve the old table or provide a documented basic guarantee with recoverable state. Node-indirected payloads can reduce move failure but still relocate slot metadata/pointers.

Rebuild at the same m cleans tombstones but can rearrange clusters and iteration. Grow/shrink invalidates physical references/iterators under most flat layouts. `reserve` should account for target load and checked rounding, while actual capacity policy can be implementation-specific. Never serialize raw slots/tombstones as an unversioned logical map format.

**Iteration scans capacity.** A flat iterator visits occupied slots and skips empty/deleted, making full traversal O(m), not merely O(n). Over-reserving or deletion churn can hurt iteration even when lookups seem fine. Insertion, deletion shifts, rebuild, resize, or seed changes can reorder entries; order is not a promise unless maintained separately.

Returning references can be valid until an operation relocates/destroys the slot under the exact API. Entry handles that retain an index become stale after resize or backward shift. Generational versions or exclusive borrows can enforce validity.

**Concurrency is not obtained from atomic states alone.** Concurrent insertion can claim the same slot; lookup can see OCCUPIED before payload initialization; deletion can destroy while a reader compares; backward shift moves a sequence under readers; resize replaces the array. A lock, sharded table, or purpose-built concurrent protocol must define linearization and reclamation.

Lock-free open-addressing often uses atomic metadata plus immutable/indirected payloads, helping descriptors, or version tags. Memory ordering, ABA, resize cooperation, cancellation after reservation, and reclamation remain algorithm-specific. A sequential linear-probe implementation should not be advertised thread-safe because slot words are atomic.

**Hash flooding and resource exhaustion remain.** Poor/attacker-chosen homes form long clusters. Secret/randomized hashing, capacity/load limits, request limits, time budgets, alternative structures, and telemetry layer defenses. Unit-step locality does not prevent worst-case O(n) probes or aggregate O(n^2) construction.

Track probes per hit/miss/insert/delete, maximum/percentiles, cluster lengths, live/fill/tombstone loads, rebuild/grow/shrink counts and latency, equality calls, bytes hashed, and allocation/memory. An average alone hides latency-critical clusters.

**Testing uses a reference map and structural oracle.** Generate unique put/update/get/delete/reserve/rebuild operations. After each, compare logical contents and inspect slot counts, duplicate absence, payload initialization, and reachability: from every key's home, its slot must appear before any EMPTY. Probe every absent key in a bounded domain and ensure termination.

Force m=1/small, empty, exactly one EMPTY, full, home at last slot, wrap clusters, deletion at cluster head/middle/tail, tombstone before duplicate, all tombstones, same-size cleanup, grow/shrink, maximum arithmetic, constant hash, and failure during construction/rehash. For backward shift, enumerate small tables and compare every moved state to a model.

Benchmark realistic keys and structured/adversarial homes over α/fill sweeps, hits/misses, updates, churn, cluster distributions, rebuild boundaries, iteration, element size/layout, cache behavior, memory, throughput, and latency percentiles. Compare chaining and later probing variants under identical semantics; do not import legacy machine timings.

The executable trace below verifies tombstone continuation, duplicate-safe reuse, wrap-capable bounded lookup, and rebuilding-independent invariants on finite integer keys.

<!-- bijux-verify: {"id":"linear-probing-tombstone-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"lookup_after_tombstone=FOURTEEN\nreused_tombstone_index=1\nstates=O,O,O,O,E,E,E\nvalues=ZERO,TWENTY_ONE,FOURTEEN,THREE\nmiss_probes=5\nsize=4\ninvariant=True\nevidence=finite_linear_probing_trace\n","stderr":""}} -->
```python
EMPTY = object()
DELETED = object()


class LinearMap:
    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.slots = [EMPTY] * capacity
        self.size = 0
        self.used = 0

    def _locate(self, key, for_insert=False):
        first_deleted = None
        for probes in range(1, len(self.slots) + 1):
            index = (hash(key) + probes - 1) % len(self.slots)
            slot = self.slots[index]
            if slot is EMPTY:
                target = first_deleted if first_deleted is not None else index
                return False, target, probes
            if slot is DELETED:
                if first_deleted is None:
                    first_deleted = index
                continue
            if slot[0] == key:
                return True, index, probes
        if for_insert and first_deleted is not None:
            return False, first_deleted, len(self.slots)
        return False, None, len(self.slots)

    def put(self, key, value):
        found, index, _ = self._locate(key, for_insert=True)
        if found:
            self.slots[index] = (key, value)
            return False, index
        if index is None:
            raise OverflowError("table full")
        if self.slots[index] is EMPTY:
            self.used += 1
        self.slots[index] = (key, value)
        self.size += 1
        return True, index

    def get_with_probes(self, key):
        found, index, probes = self._locate(key)
        if not found:
            return None, probes
        return self.slots[index][1], probes

    def delete(self, key):
        found, index, _ = self._locate(key)
        if not found:
            raise KeyError(key)
        value = self.slots[index][1]
        self.slots[index] = DELETED
        self.size -= 1
        return value

    def invariant(self):
        occupied = [(i, slot) for i, slot in enumerate(self.slots)
                    if slot is not EMPTY and slot is not DELETED]
        if len(occupied) != self.size:
            return False
        if sum(slot is not EMPTY for slot in self.slots) != self.used:
            return False
        keys = [slot[0] for _, slot in occupied]
        if len(keys) != len(set(keys)):
            return False
        for index, (key, _) in occupied:
            for distance in range(len(self.slots)):
                probe = (hash(key) + distance) % len(self.slots)
                if self.slots[probe] is EMPTY:
                    return False
                if probe == index:
                    break
            else:
                return False
        return True


table = LinearMap(7)
for key, value in ((0, "ZERO"), (7, "SEVEN"), (14, "FOURTEEN"), (3, "THREE")):
    assert table.put(key, value)[0]
assert table.delete(7) == "SEVEN"
print(f"lookup_after_tombstone={table.get_with_probes(14)[0]}")
inserted, reused = table.put(21, "TWENTY_ONE")
assert inserted
assert not table.put(14, "FOURTEEN")[0]
labels = ["E" if slot is EMPTY else "D" if slot is DELETED else "O"
          for slot in table.slots]
values = [slot[1] for slot in table.slots if slot not in (EMPTY, DELETED)]
print(f"reused_tombstone_index={reused}")
print("states=" + ",".join(labels))
print("values=" + ",".join(values))
_, miss_probes = table.get_with_probes(28)
print(f"miss_probes={miss_probes}")
print(f"size={table.size}")
print(f"invariant={table.invariant()}")
print("evidence=finite_linear_probing_trace")
```

## Definitions and Notation

- `m`: positive physical slot count.
- `n`: OCCUPIED/live count; `u`: non-EMPTY/used count for tombstone design.
- `α=n/m`: live load; `φ=u/m`: fill load.
- `home(k)=reduce(h(k),m)`: first probe position.
- `p_j(k)=(home(k)+j) mod m`: j-th unit-step probe, `0<=j<m`.
- `dist(a,b)=(b-a) mod m`: forward cyclic distance.
- **cluster/run**: maximal cyclic non-EMPTY interval.
- **tombstone**: non-live marker that preserves continuation but is reusable after duplicate search.
- **reachability**: an entry is encountered from home before any EMPTY.
- **backward shift**: deletion repair moving later reachable entries into earlier holes.

## Mechanisms, Invariants, or Proof Structure

Probe-permutation proof establishes bounded coverage. Search correctness uses the insertion history: OCCUPIED candidates require equality, DELETED preserves the path, and EMPTY proves absence. Unique insertion remembers reuse but continues to equality/EMPTY/full-cycle, preventing duplicates.

Tombstone deletion proves logical removal plus continued reachability; counts update `n--` and leave u. Backward-shift deletion instead maintains a moving hole and relocates an entry only when `dist(home,hole)<dist(home,current)`, preserving that entry's search prefix.

Resize/rebuild proves a bijection from old OCCUPIED entries to new OCCUPIED entries under new homes, no transfer of EMPTY/DELETED, correct counts, and publication after complete successful construction. Complexity claims state hash independence, load, deletion history, and table/probe variant.

## Alternatives and Trade-Offs

| Design | Strength | Cost or obligation |
|---|---|---|
| Pure linear probing | simple, sequential locality | primary clustering, relocation, load sensitivity |
| Tombstone deletion | simple removal and stable remaining slots | dead fill and rebuild pressure |
| Backward-shift deletion | removes dead fill | move cost, wrap proof, invalidation/failure |
| Separate metadata/payload | compact scans/fingerprints | more layout/index/lifetime state |
| Quadratic/double hashing | reduces primary clustering patterns | coverage/step proofs, less sequential locality |
| Robin Hood | controls displacement variance | swaps, distance metadata, deletion rules |
| Swiss-style groups | SIMD candidate filtering/high density | not pure unit probing; complex metadata |
| Separate chaining | easy deletion/stable nodes possible | pointers, allocation, cache misses |

## Failure Modes and Misconceptions

- **“Empty and deleted are both vacant.”** Both accept insertion, but only EMPTY terminates lookup.
- **“First tombstone wins immediately.”** Search must still exclude a duplicate.
- **“A full table eventually finds empty.”** It does not; bound m and grow/report.
- **“Low live load means short probes.”** Tombstones can make fill nearly one.
- **“Linear probing is uniform hashing.”** contiguous probes create correlated clusters.
- **“Classic formulas are exact guarantees.”** They are model-dependent asymptotic approximations.
- **“Backward shift moves every successor.”** Only entries whose probe interval crosses the hole may move.
- **“Prime capacity fixes clustering.”** unit steps still merge clusters; hash distribution remains decisive.
- **“Contiguous means zero cache misses.”** long probes and large payloads still cost bandwidth/cache.
- **“All modern open-addressed maps are linear.”** many use quadratic, perturbation, grouped, or hybrid probes.
- **“Atomic slot metadata is thread safety.”** payload publication, movement, resize, and reclamation remain.
- **“Tombstones are only a memory issue.”** they directly extend negative/insert probes.

## Worked Examples

### Example 1

For m=7 and home 5, probes are 5,6,0,1,2,3,4. Every slot appears once. Conclusion: unit-step modulo probing covers the table and must be bounded at seven.

### Example 2

Keys 0,7,14 occupy 0,1,2. Lookup 14 compares through the cluster. Conclusion: distinct homes equal modulo m form a contiguous run.

### Example 3

Deleting key 7 by marking slot 1 EMPTY makes lookup 14 stop there falsely. DELETED preserves continuation. Conclusion: deletion state carries historical reachability.

### Example 4

After that deletion, insertion of key 14 that commits at tombstone 1 before checking slot 2 creates a duplicate. Conclusion: remember reuse, continue search.

### Example 5

At n=4,u=9,m=10, live load is 0.4 but fill is 0.9. Misses can cross nearly the whole table. Conclusion: tombstone policy tracks both counts.

### Example 6

At α=0.5, ideal formulas give 1.5 successful and 2.5 unsuccessful probes; at 0.9 they give 5.5 and 50.5. Conclusion: negative probes deteriorate sharply near full under the model.

### Example 7

With hole 6, current slot 0, and entry home 5 in m=8, `dist(5,6)=1<dist(5,0)=3`, so shifting to 6 preserves reachability across wrap. Conclusion: cyclic distance handles boundary cases.

### Example 8

An entry at current 1 with home 1 must not move backward into hole 7: its search begins at 1. Conclusion: physical adjacency alone is not the shift condition.

### Example 9

Rebuilding m=8 to m=16 changes key hash 13's home from 5 to13 and removes tombstones. Conclusion: rebuild reinserts logical entries, not slot bytes.

### Example 10

A reader sees OCCUPIED before a producer finishes constructing the value, while a deleter shifts that slot. Conclusion: sequential state invariants need a separate concurrent publication/movement proof.

## Cross-Program Connections

- [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) owns atomic slot protocols, linearizability, helping, resize, and reclamation.
- [Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) connects uninitialized storage, relocation, destructors, SIMD metadata, overflow, and allocators.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) connects clustering analysis, k-independence, probe distributions, and empirical cost.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) connects hash indexes/joins, tombstones, rebuild, skew, and spill.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) connects cache lines, SIMD groups, bandwidth, branch prediction, and prefetching.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns HashDoS, randomized hashes, resource limits, hostile equality, and telemetry.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) connects cooperative resize/migration and versioned placement.

## References

1. Mikkel Thorup, [Linear Probing with 5-Independent Hashing](https://arxiv.org/abs/1509.04549). Primary lecture notes deriving expected constant time under 5-independence and explaining higher-moment requirements.
2. Anna Pagh, Rasmus Pagh, and Milan Ružić, [Linear Probing with Constant Independence](https://arxiv.org/abs/cs/0612055). Primary paper on sufficient independence and pairwise-independent counterbehavior.
3. Oracle, [Java SE 25 `IdentityHashMap`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/IdentityHashMap.html). Current scoped linear-probe implementation note, identity semantics, capacity, iteration, synchronization, and ordering contract.
4. OpenJDK Project, [`IdentityHashMap.java`](https://github.com/openjdk/jdk/blob/master/src/java.base/share/classes/java/util/IdentityHashMap.java). Current primary source for alternating layout, probing, close deletion, resizing, iteration, and invariants.
5. Abseil Project, [Swiss Tables Design Notes](https://abseil.io/about/design/swisstables). Current control-byte/fingerprint/SIMD candidate and EMPTY-versus-DELETED design contrast.
6. Rust Project, [`HashMap`](https://doc.rust-lang.org/std/collections/struct.HashMap.html). Current quadratic-probing/SIMD implementation statement, randomized hash, capacity, mutation, iteration, and API behavior.
7. Python Software Foundation, [CPython `dictobject.c`](https://github.com/python/cpython/blob/main/Objects/dictobject.c). Current compact dictionary layout and perturbation recurrence; evidence that CPython dict is not pure linear probing.
8. Python Software Foundation, [CPython `setobject.c`](https://github.com/python/cpython/blob/main/Objects/setobject.c). Current bounded linear-run plus perturbation set lookup and slot-state implementation.
9. Scott A. Crosby and Dan S. Wallach, [Denial of Service via Algorithmic Complexity Attacks](https://www.usenix.org/legacy/event/sec03/tech/full_papers/crosby/crosby.pdf). Primary worst-case hash-table attack evidence and resource-threat context.
10. ISO C++ working draft, [Unordered Associative Container Requirements](https://eel.is/c%2B%2Bdraft/unord.req.general). Observable equality/hash, average/worst complexity, load, rehash, and invalidation requirements without mandating probing layout.

## Exercises

### Exercise 1

Specify lookup and unique insertion for EMPTY/OCCUPIED/DELETED slots, including full-cycle behavior, counts, equality, and failure.

### Exercise 2

Prove the probe permutation and the EMPTY termination rule; construct the minimal counterexample to clearing a middle deletion to EMPTY.

### Exercise 3

Derive backward-shift deletion using cyclic distance and trace a wraparound cluster, including move/lifetime/invalidation constraints.

### Exercise 4

Design live/fill/rebuild/grow/shrink policies for a deletion-heavy table without copying thresholds from another implementation.

### Exercise 5

Prepare a production evidence plan comparing pure linear probing, separate chaining, and a grouped-control-byte table.

## Answers to the Exercises

### Answer 1

Require m>0 and probe at most m distinct slots. On OCCUPIED, filter by stored hash then equality and return/update on match. On DELETED, save its index only if it is the first and continue. On EMPTY, absence is proved; for insert, construct key/value off-table and commit to saved tombstone or this empty slot. Into EMPTY increments n and u; into DELETED increments n only; update changes neither. If a full cycle finds a match, use it; otherwise reuse a saved tombstone or report/grow if none. Publication follows successful initialization; exceptions/failures preserve prior state. Key/hash state remains immutable while indexed.

### Answer 2

If `(q+a) mod m=(q+b) mod m` for `0<=a,b<m`, then m divides a-b, whose magnitude is below m, so a=b; m probes cover m slots. An insertion follows the same sequence and takes the first reusable EMPTY absent an earlier equal key, so a later live key implies no persistent EMPTY preceded it; lookup may stop at the first EMPTY. Minimal counterexample: m=3, keys with home0 occupy slots0 and1. Delete the first key and set slot0 EMPTY. Lookup of the second stops at0 and falsely reports absent. DELETED or correct shifting preserves the path.

### Answer 3

After removing at hole d, scan s=d+1 cyclically until EMPTY. For entry home h at s, move it to d iff `dist(h,d)<dist(h,s)`, since d occurs earlier on its legal probe path; then s becomes the hole. Example m=8: homes5 entries occupy5,6,7,0. Delete6. Entry at7 with home5 moves to6; entry at0 with home5 moves to7; stop at empty1, leaving0 empty. Each move constructs/moves into non-live storage, updates metadata only at safe commit points, destroys/clears old storage once, preserves hashes, and invalidates physical handles as documented. If moves can fail, provide rollback/basic state or use tombstones/indirection.

### Answer 4

Maintain n, u, tombstones `u-n`, capacity m, probe histograms, and memory/latency budgets. Before insertion, grow if prospective live/fill violates a target chosen from measured hit/miss/churn costs or would eliminate the required EMPTY. Same-size rebuild when tombstone load/probes exceed budget even if n is low. Shrink only when sustained live load is below a lower threshold and target capacity satisfies headroom, using hysteresis to avoid oscillation. Every size computation is checked; maximum-capacity insertion reports failure rather than looping. Rebuild reinserts live entries, resets u=n, and is failure-atomic. Tune from key sizes, hash quality, hit/miss ratio, deletes, element layout, cache, iteration, and tail latency across load sweeps.

### Answer 5

Hold equality, keys, values, hash/security profile, failure, update, and iteration requirements fixed. Model-test logical operations plus constant hashes, duplicates, wrap, full tables, delete churn, rebuild, failure, and resource lifetimes. For linear probing inspect reachability, n/u, clusters, and probe termination; for chaining inspect exact bucket membership/links; for grouped design inspect control/payload states and group coverage. Benchmark realistic/structured/adversarial keys across live/fill loads, hits/misses, updates/deletes, reserve/rebuild/resize, iteration, element size, allocator, bytes hashed, comparisons/probes/groups, cache/branch/SIMD behavior, memory, throughput, and p50/p95/p99/max latency. Add security seed/limit review and concurrency/lifetime evidence if applicable. Do not infer a winner from legacy timings or another runtime's private algorithm.
