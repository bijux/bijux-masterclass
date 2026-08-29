---
module_id: DSE-024
program: Data Structures Engineering
level: 1
module_number: 24
title: Quadratic Probing and Double Hashing
status: complete
last_verified: 2026-08-30
---

# Quadratic Probing and Double Hashing

## One-Page Review

### Governing question

How should an open-addressed table choose non-linear probe sequences that reduce linear probing's clustering without sacrificing coverage, termination, reachability, deletion correctness, or honest performance claims?

### Essential definitions

- A **probe policy** maps a key and probe number to a candidate slot.
- **Quadratic probing** uses a key-independent offset such as `c1*i+c2*i^2`, or a related recurrence, from the key's home slot.
- **Triangular probing** uses offsets `T_i=i(i+1)/2`; modulo a power of two these offsets form a full permutation.
- **Secondary clustering** occurs when keys with the same home follow the same later probes.
- **Double hashing** uses `p_i=(h1(k)+i*h2(k)) mod m`; the second hash selects the stride.
- A **full-cycle** probe sequence visits every table slot exactly once before repeating.
- The double-hash **cycle length** is `m/gcd(h2(k),m)`; full coverage therefore requires `gcd(h2(k),m)=1`.
- **EMPTY**, **OCCUPIED**, and **DELETED** retain the meanings established for linear probing.
- **Live load** is `alpha=n/m`; **fill load** includes tombstones that cannot terminate search.
- A **probe group** is a metadata/payload group inspected as one step in modern grouped tables; it is not necessarily one logical slot.

### Central model, mechanism, or theorem

For triangular offsets and `m=2^r`, `p_i=(h1(k)+i(i+1)/2) mod m`, `0<=i<m`, visits every slot. If two offsets were equal, `2^(r+1)` would divide `(j-i)(i+j+1)`. These two factors have opposite parity, so the even factor alone would need all `r+1` powers of two; within the stated index range it is positive and smaller than `2^(r+1)`, a contradiction.

For double hashing, repeated addition of stride `s=h2(k)` reaches exactly `m/gcd(s,m)` residues. Full coverage is equivalent to `gcd(s,m)=1`. Prime `m` with `1<=s<m`, or power-of-two `m` with odd `s`, are sufficient policies. Neither “quadratic” nor “two hashes” alone establishes coverage: coefficients, capacity family, reduction, and bounds are one correctness contract.

### Critical invariants

1. Each key's probe generator is deterministic while the key is indexed and emits no invalid slot.
2. The capacity policy and probe formula provide the documented coverage before insertion relies on it.
3. Lookup stops at EMPTY, crosses DELETED, confirms equality, and never exceeds the proved probe bound.
4. Unique insertion remembers reusable tombstones but searches far enough to exclude an existing equal key.
5. Slot states agree with payload lifetime, live/fill counts, and reachability from each key's probe sequence.
6. Resize recomputes both home and stride/offset under the new capacity and reinserts every live entry once.
7. Hash mixing, seed, capacity, group width, and probe arithmetic are versioned parts of the physical representation, not serialized logical semantics.
8. Expected-time, cache, security, concurrency, and invalidation claims name their assumptions and evidence.

### Common failures

- Using `i^2 mod p` and assuming it visits all `p` slots; it visits only the quadratic residues plus the initial offset.
- Choosing an even stride for a power-of-two table and making most slots unreachable.
- Allowing double-hash stride zero after reduction.
- Reusing a tombstone before checking the rest of the probe sequence for a duplicate.
- Changing capacity without recomputing the second hash or probe policy.
- Confusing reduced primary and secondary values derived from one mixed hash with statistically independent hashes.
- Claiming quadratic probing eliminates all clustering; equal-home keys still share a sequence in the basic design.
- Applying uniform-hashing expected bounds to arbitrary hashes, finite tables, tombstones, or hostile keys.
- Assuming a source-described grouped quadratic table probes one payload slot per step.
- Omitting overflow-safe arithmetic and an explicit maximum probe count.

### Compact example

With `m=8`, home 3, triangular offsets `0,1,3,6,10,15,21,28` produce slots `3,4,6,1,5,2,0,7`: a full permutation. With `m=11`, start 2 and stride 5 produce all eleven slots. With `m=12`, start 1 and stride 4 produce only `1,5,9` before repeating because `gcd(4,12)=4`. The executable trace verifies these three cases and tombstone-safe operations.

### Connections

[DSE-021](021-hash-functions-and-distribution.md) owns mixing and reduction; [DSE-023](023-linear-probing.md) supplies the open-addressing state machine and clustering baseline. The [program roadmap](../ROADMAP.md) next studies Robin Hood, cuckoo, and hopscotch policies before treating resize and hash-flooding as dedicated topics.

## Governing Question

Which quadratic or double-hash probe construction, capacity family, deletion state machine, load policy, and evidence make a non-linear open-addressed table correct for every reachable state—not merely faster on one friendly benchmark?

## Why This Matters

Linear probing's sequential locality is powerful, but its unit stride lets occupied runs attract and merge. Non-linear probing tries to spread collisions: quadratic offsets move progressively farther, while double hashing gives each key a key-dependent stride. Both can reduce primary clustering. Both can also make empty slots unreachable if their arithmetic is chosen casually.

That failure is semantic, not a small slowdown. An insertion can report “full” while free slots exist; a miss can loop; deletion can hide a key; resize can silently change reachability. A production design therefore treats probe formula and capacity policy as a coupled theorem. It additionally manages tombstones, object lifetime, exceptions, iterators, adversarial hashes, arithmetic overflow, and concurrent publication.

Modern implementations complicate names further. Current Abseil and Go sources describe quadratic probing over groups with compact control metadata; current Rust documentation describes quadratic probing with SIMD lookup. Their group geometry, fingerprints, load policy, and implementation invariants are not interchangeable with a textbook slot-at-a-time formula. This chapter develops the mathematics first, then uses those implementations as carefully scoped engineering evidence.

## Prerequisites and Retrieval

Retrieve abstraction, representation, and operation contracts from [DSE-001](001-abstract-data-types-and-concrete-representations.md), [DSE-002](002-representation-invariants.md), and [DSE-003](003-operation-contracts.md); cost, layout, cache, genericity, iteration, testing, and benchmarking from [DSE-004](004-time-space-and-allocation-cost.md) through [DSE-010](010-benchmarking-a-structure-without-misleading-results.md); hash-family and reduction assumptions from [DSE-021](021-hash-functions-and-distribution.md); collision-layout contrast from [DSE-022](022-separate-chaining.md); and EMPTY/DELETED reachability, duplicate-safe insertion, load, rebuild, lifetime, security, and concurrency rules from [DSE-023](023-linear-probing.md).

## Learning Objectives

After completing this module, you should be able to:

1. derive and audit quadratic and double-hash probe generators;
2. prove triangular probing permutes a power-of-two table;
3. compute a double-hash cycle length using a greatest common divisor;
4. distinguish primary from secondary clustering and uniform-hashing assumptions;
5. integrate EMPTY/OCCUPIED/DELETED behavior with a non-linear probe sequence;
6. design capacity, stride, load, rebuild, and checked-arithmetic policies together;
7. preserve failure, lifetime, iterator/reference, and resize contracts;
8. scope grouped quadratic implementations without copying private details into an abstract guarantee;
9. test coverage, reachability, duplicates, deletion churn, resize, and adversarial hashes;
10. benchmark full operation cost and tail behavior under representative histories.

## Core Exposition

**Start with a probe generator, not a slogan.** Let `m>0`, let `h1(k)` be the reduced home slot, and let `p_i(k)` be the slot examined on probe `i`. A correct generator must define a deterministic finite sequence for every legal key/table state. It must keep indices in `[0,m)`, avoid arithmetic undefined behavior, and provide enough distinct candidates for the load policy. Lookup and insertion must use exactly the same generator for the same key and capacity.

A full permutation is the simplest coverage contract: `p_0,...,p_(m-1)` contains every slot once. A design may intentionally cover less, but then it must maintain occupancy below a proved limit for each reachable probe subset and grow before that premise fails. “There is an EMPTY somewhere” is insufficient unless the current key can reach it.

**Quadratic probing is a family.** A common form is

\[
p_i(k)=(h_1(k)+c_1 i+c_2 i^2)\bmod m.
\]

The coefficients, arithmetic domain, capacity, and index range determine coverage. For prime `p`, the simple offsets `i^2 mod p` contain only `(p+1)/2` distinct values for `i=0,...,p-1`: nonzero `i` and `p-i` have the same square. If fewer than `(p+1)/2` table slots are occupied, every such probe set must include an EMPTY, so a sub-half load policy can still guarantee insertion. It does not justify probing `p` times as though every slot were covered.

Different coefficients can have different guarantees. Never transplant “prime capacity” from one formula or “load below one-half” from one theorem into another without redoing the proof. A test over several capacities is useful, but finite enumeration is not a universal proof.

**Triangular offsets give a clean power-of-two construction.** Define `T_i=i(i+1)/2` and let `m=2^r`. The sequence

\[
p_i(k)=(h_1(k)+T_i)\bmod 2^r
\]

is a permutation for `0<=i<2^r`. Suppose `T_i=T_j mod 2^r`, with `0<=i<j<2^r`. Multiplying by two gives divisibility of `(j-i)(i+j+1)` by `2^(r+1)`. The factors have opposite parity because their sum is `2j+1`. The odd factor contributes no factor two; the even factor would have to be divisible by `2^(r+1)`, but both positive factors are smaller than that. Contradiction. Adding home merely rotates the permutation.

Compute this sequence by a recurrence when appropriate: start at home, then add `1,2,3,...` modulo capacity. Checked/wrapping arithmetic must match the proof. Unsigned machine wrap at word width is not automatically the same as modulo table capacity unless masking and capacity constraints make it so.

Basic quadratic probing avoids the primary clustering mechanism of one shared unit-step run: keys arriving near a run do not all walk to the same adjacent exit. However, two keys with the same home and the same coefficient policy follow exactly the same sequence. This **secondary clustering** shares collision history even if their full hashes differ.

**Double hashing makes the stride key-dependent.** Define

\[
p_i(k)=(h_1(k)+i h_2(k))\bmod m.
\]

For fixed key, this is repeated addition on integers modulo `m`. Let `s=h2(k)` and `d=gcd(s,m)`. The sequence repeats when `(i-j)s=0 mod m`. The least positive period is `m/d`, so it visits exactly that many residues. It covers all slots if and only if `s` and `m` are coprime.

This yields two durable policies. With prime capacity `m`, restrict the stride to `1,...,m-1`. With `m=2^r`, force the stride odd. More general capacities require selecting from their units modulo `m`; merely mapping into `1,...,m-1` is not enough. Stride zero is always invalid for `m>1` because the probe never leaves home.

The second hash should spread keys across allowed strides and should not be a weak restatement of the primary reduction. Deriving `h1` and `h2` from disjoint portions or domain-separated mixes of one high-quality full hash can avoid hashing large keys twice, but does not magically make them probabilistically independent. State precisely what the hash-family analysis assumes and what the implementation supplies.

Double hashing reduces both primary clustering and the equal-home shared-sequence behavior when colliding keys obtain different strides. If two keys have the same home and stride, they still share a sequence. There are at most `m*phi(m)` start/allowed-stride pairs, far fewer than `m!` possible permutations; double hashing is not literal uniform probing. The cited research discusses asymptotic relationships to fully random behavior under defined models, not guarantees for arbitrary user hashes.

**The open-addressing state machine remains.** Each slot is EMPTY, OCCUPIED, or DELETED. Lookup follows the selected sequence: EMPTY proves absence, DELETED preserves continuation, and OCCUPIED requires hash/fingerprint filtering followed by equality. It stops after the proved coverage bound even if corruption, a full table, or policy error removes all terminators.

Unique insertion remembers the first DELETED slot but continues until equality, EMPTY, or full-cycle exhaustion. Equality updates/rejects without changing counts. On EMPTY, commit into the remembered tombstone or this EMPTY. Into EMPTY increments live and used counts; into DELETED increments live only. A completed sequence with no EMPTY may reuse a remembered tombstone, otherwise the policy must grow or report capacity exhaustion.

Deleting by writing EMPTY can hide later keys regardless of whether the sequence is linear, quadratic, or double-hashed. Tombstones are the general repair. Linear probing's simple local backward-shift rule does not transfer directly: later physical neighbors may not be successors in the deleted key's or moved key's non-linear sequence. A deletion algorithm that relocates entries must prove reachability for each policy; otherwise use tombstones and periodic rebuild.

**Load has two dimensions.** Track live `n`, non-EMPTY/used `u`, capacity `m`, `alpha=n/m`, and fill `phi=u/m`. A mathematical guarantee may constrain live occupancy, while termination and measured misses depend on non-EMPTY history. Repeated deletion can leave `alpha` small and `phi` near one. Same-size rebuild removes tombstones; growth creates live headroom; shrink needs hysteresis.

For `i^2 mod p`, a policy that relies on the `(p+1)/2` candidate-set argument must grow before an insertion can encounter too many occupied positions. Tombstones count as non-terminating for lookup and often as consumed candidates for insertion search. For a full-cycle triangular or coprime double-hash sequence, coverage remains, but performance still deteriorates sharply near full and the implementation should preserve at least one EMPTY if its control flow depends on one.

Under the ideal uniform-hashing model, an unsuccessful search at load `alpha` has expected probes at most about `1/(1-alpha)`, and a successful search obtained by averaging insertion costs is about `(1/alpha) ln(1/(1-alpha))`. These familiar bounds are model results. Double hashing can approximate uniform probing under stronger random assumptions, as the cited research analyzes, but no chapter equation proves a particular hash implementation, deletion history, finite capacity, cache, or hostile input meets those assumptions.

**Resize changes every arithmetic premise.** Growing from `m` to `m'` changes primary reduction, quadratic modulus, and double-hash allowed stride. Allocate a new legal capacity, recompute home and stride/offset from the full stored/recomputed hash, and reinsert every live entry exactly once. Do not copy physical indices, tombstones, or old strides blindly.

Capacity selection affects memory rounding, division versus masking, SIMD/group geometry, maximum arithmetic, and growth granularity. Prime-capacity double hashing needs a checked next-prime or governed capacity table. Power-of-two policies need checked shifts and a defined maximum. `reserve(x)` must translate requested live capacity through maximum load without overflow. A failed allocation/hash/move/equality must leave the documented prior or recoverable state; publish new metadata only after payload construction succeeds.

**Layout and probe unit matter.** A slot-at-a-time quadratic sequence can jump among cache lines, trading linear locality for less clustering. Separate control bytes let a probe inspect many state/fingerprint bytes before touching keys. Grouped designs apply the sequence to groups, then compare a vector of fingerprints inside a group. Their “probe count” may mean groups, metadata bytes, candidate equalities, or payload accesses; measurements must name the unit.

Current Abseil `raw_hash_set` source describes an open-addressed, quadratic-probed low-level table with separate control bytes, H2 fingerprints, groups, EMPTY/DELETED states, and implementation-specific load behavior. Current Go runtime source states that its built-in map design is based on Swiss tables and walks power-of-two groups using quadratic probing, with an EMPTY group termination invariant. Current Rust `HashMap` documentation describes quadratic probing with SIMD lookup. These are current scoped examples, not a portable promise that all releases or languages share coefficients, group width, deletion optimization, or invalidation.

Current CPython dictionary source uses a perturbation recurrence rather than calling its scheme quadratic or double hashing. This contrast prevents a common category error: any non-unit open-addressing scheme is not automatically one of the two formulas in this chapter. The ISO C++ unordered-container requirements specify observable hash/equality, complexity, load, rehash, and invalidation behavior without mandating a physical probe scheme.

**Security remains a hash-family and resource question.** A secret seed can make collision patterns harder to predict but does not repair a coverage bug. Two derived hashes can share structural weaknesses. An attacker who induces equal start/stride pairs or costly equality can still create long probes. Worst-case open addressing remains linear per operation and repeated insertions can be quadratic in total work.

Defenses combine keyed or randomized hashing where appropriate, input and capacity limits, time budgets, collision/probe telemetry, alternate structures, and operational controls. Record maximum and percentile groups/probes per hit, miss, insert, and delete; tombstones; rebuilds/resizes; equality calls; bytes hashed; and rejected capacity requests. Do not expose seeds through deterministic physical-order serialization.

**Iteration and concurrency require separate contracts.** Flat iteration scans capacity and skips non-live slots, so it is `O(m)` even when `n` is small. Rebuild/resize changes order; insertion and deletion may do so too. References, indices, and entry handles can be invalidated by relocation. State those rules rather than inheriting them from another library.

Atomic control bytes alone do not make probing concurrent. Readers must not observe OCCUPIED before payload publication or race destruction; writers can claim the same slot; resize replaces probe arithmetic and storage; tombstone reuse creates ABA-like state reuse. A concurrent table needs a linearization, memory-order, migration, iterator/snapshot, and reclamation design. A sequential implementation needs external synchronization if shared.

**Testing must audit arithmetic before workload behavior.** For every supported capacity, enumerate every home and probe index for small tables and assert range, determinism, distinct-count, period, and termination. For double hashing enumerate allowed strides and compare observed period with `m/gcd(s,m)`. Include forbidden zero/noncoprime strides as negative tests. For quadratic policies test the exact coefficients and capacity family, not a generic label.

Then model-test put/update/get/delete/reserve/rebuild against a reference map. After each operation check counts, slot/payload state, uniqueness, and reachability along the exact key sequence before EMPTY. Force wrap, same-home keys, same and different double-hash strides, tombstones before duplicates, all tombstones, one EMPTY, maximum load, resize across capacity families, constant/structured hashes, mutable keys, arithmetic boundaries, and injected allocation/hash/equality/move failures.

Benchmark realistic and adversarial keys across live/fill load sweeps, hit/miss mixes, churn, resize/rebuild boundaries, value sizes, metadata layouts, cache and branch behavior, division/multiplication cost, vector width, memory, throughput, and p50/p95/p99/max latency. Compare linear, quadratic, double, chaining, and grouped designs under identical semantics and memory budgets. Report toolchains, hardware, seeds, distributions, warmup, repetitions, uncertainty, and raw artifacts.

The finite executable oracle below checks two positive coverage theorems, one noncoprime counterexample, tombstone continuation/reuse, duplicate prevention, counts, and reachability. It is not a production hash table or performance experiment.

<!-- bijux-verify: {"id":"quadratic-double-hashing-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"quadratic_sequence=3,4,6,1,5,2,0,7\nquadratic_unique=8\ndouble_sequence=2,7,1,6,0,5,10,4,9,3,8\ndouble_unique=11\nnoncoprime_cycle=1,5,9\nlookup_after_tombstone=True\nreused_tombstone_index=7\nsize=3\ninvariant=True\nevidence=finite_quadratic_double_hashing_trace\n","stderr":""}} -->
```python
from math import gcd

EMPTY = object()
DELETED = object()


def triangular_probe(home, capacity):
    return [
        (home + index * (index + 1) // 2) % capacity
        for index in range(capacity)
    ]


def double_probe(start, step, capacity):
    return [(start + index * step) % capacity for index in range(capacity)]


def distinct_cycle(start, step, capacity):
    result = []
    seen = set()
    index = start
    while index not in seen:
        seen.add(index)
        result.append(index)
        index = (index + step) % capacity
    return result


class DoubleHashSet:
    def __init__(self, capacity):
        self.capacity = capacity
        self.slots = [EMPTY] * capacity
        self.size = 0
        self.used = 0

    def probes(self, key):
        _, start, step = key
        assert 0 <= start < self.capacity
        assert gcd(step, self.capacity) == 1
        return double_probe(start, step, self.capacity)

    def add(self, key):
        first_deleted = None
        for index in self.probes(key):
            slot = self.slots[index]
            if slot is EMPTY:
                target = first_deleted if first_deleted is not None else index
                self.slots[target] = key
                self.size += 1
                if first_deleted is None:
                    self.used += 1
                return True, target
            if slot is DELETED:
                if first_deleted is None:
                    first_deleted = index
            elif slot == key:
                return False, index
        if first_deleted is not None:
            self.slots[first_deleted] = key
            self.size += 1
            return True, first_deleted
        raise OverflowError("probe cycle contains no reusable slot")

    def contains(self, key):
        for index in self.probes(key):
            slot = self.slots[index]
            if slot is EMPTY:
                return False
            if slot is not DELETED and slot == key:
                return True
        return False

    def delete(self, key):
        for index in self.probes(key):
            slot = self.slots[index]
            if slot is EMPTY:
                raise KeyError(key)
            if slot is not DELETED and slot == key:
                self.slots[index] = DELETED
                self.size -= 1
                return index
        raise KeyError(key)

    def invariant(self):
        live = [slot for slot in self.slots if slot is not EMPTY and slot is not DELETED]
        if len(live) != self.size or len(set(live)) != self.size:
            return False
        if sum(slot is not EMPTY for slot in self.slots) != self.used:
            return False
        for key in live:
            for index in self.probes(key):
                if self.slots[index] is EMPTY:
                    return False
                if self.slots[index] == key:
                    break
            else:
                return False
        return True


quadratic = triangular_probe(3, 8)
double = double_probe(2, 5, 11)
bad = distinct_cycle(1, 4, 12)
assert len(set(quadratic)) == 8
assert len(set(double)) == 11
assert len(bad) == 12 // gcd(4, 12)

table = DoubleHashSet(11)
a = ("A", 2, 5)
b = ("B", 2, 5)
c = ("C", 2, 5)
d = ("D", 2, 5)
for key in (a, b, c):
    assert table.add(key)[0]
assert table.delete(b) == 7
found_after_delete = table.contains(c)
inserted, reused = table.add(d)
assert inserted and not table.add(c)[0]

print("quadratic_sequence=" + ",".join(map(str, quadratic)))
print(f"quadratic_unique={len(set(quadratic))}")
print("double_sequence=" + ",".join(map(str, double)))
print(f"double_unique={len(set(double))}")
print("noncoprime_cycle=" + ",".join(map(str, bad)))
print(f"lookup_after_tombstone={found_after_delete}")
print(f"reused_tombstone_index={reused}")
print(f"size={table.size}")
print(f"invariant={table.invariant()}")
print("evidence=finite_quadratic_double_hashing_trace")
```

## Definitions and Notation

- `m`: positive slot or probe-group count governed by the specific design.
- `n`: live/OCCUPIED count; `u`: non-EMPTY count for a tombstone table.
- `alpha=n/m`, `phi=u/m`: live and fill load.
- `h1(k)`: home position after full-hash mixing and capacity reduction.
- `p_i(k)`: candidate position for probe number `i`, starting at zero.
- `c1,c2`: coefficients of a specified quadratic family.
- `T_i=i(i+1)/2`: triangular offset.
- `h2(k)=s`: double-hash stride; it must be nonzero and coprime to `m` for a full cycle.
- `gcd(s,m)`: greatest common divisor; double-hash cycle length is `m/gcd(s,m)`.
- `phi(m)`: Euler totient, the number of residue classes coprime to `m`.
- **primary clustering**: shared contiguous-run growth under unit-step probing.
- **secondary clustering**: equal-home keys sharing later probes under a home-only policy.
- **group probe**: one step that examines multiple control bytes/candidates, distinct from one payload-slot probe.

## Mechanisms, Invariants, or Proof Structure

Quadratic correctness begins with the exact offset family. For triangular offsets modulo `2^r`, the opposite-parity factor proof establishes a permutation. For square offsets modulo an odd prime, pairing `i` with `p-i` establishes only `(p+1)/2` distinct candidates and therefore motivates a stricter occupancy policy.

Double-hash correctness reduces to additive order modulo `m`: stride `s` generates a subgroup/coset of size `m/gcd(s,m)`. A full-cycle capacity/stride policy follows immediately. Search correctness then reuses the three-state history proof: equality confirms candidates, DELETED continues, EMPTY terminates, and a finite coverage bound prevents looping.

Insertion preserves uniqueness by remembering rather than immediately occupying the first tombstone. Deletion preserves reachability by retaining a tombstone unless a policy-specific relocation proof exists. Rebuild/resize is a bijection over live entries under newly computed homes and probe parameters, with publication only after successful construction.

## Alternatives and Trade-Offs

| Design | Strength | Cost or proof obligation |
|---|---|---|
| Linear probing | simplest and sequential | primary clustering and high-load miss tails |
| Square offsets modulo prime | simple non-linear pattern | partial coverage; sub-half occupancy premise |
| Triangular offsets modulo power of two | full-cycle recurrence and masking | power-of-two/correct recurrence coupling |
| Double hashing, prime capacity | any nonzero stride covers all slots | division/prime-capacity policy and second mix |
| Double hashing, power of two | odd stride covers all slots | low-bit quality and nonsequential access |
| Grouped quadratic probing | compact metadata and vector filtering | group-level invariants and implementation complexity |
| Separate chaining | no probe-coverage theorem | allocation, pointers, and cache behavior |
| Cuckoo/Robin Hood/hopscotch | different displacement objectives | movement, cycle/neighborhood, and deletion proofs |

## Failure Modes and Misconceptions

- **“Quadratic probing has one canonical formula.”** Coefficients, modulus, recurrence, and range define different algorithms.
- **“A prime table makes every quadratic full-cycle.”** `i^2 mod p` repeats paired squares.
- **“An EMPTY anywhere guarantees insertion.”** The current key must be able to reach it.
- **“Two hashes guarantee a full cycle.”** The stride must be nonzero and coprime to capacity.
- **“Double hashing samples all permutations.”** It samples start/stride arithmetic progressions, not `m!` orders.
- **“Different strides mean no clustering.”** equal start/stride pairs still share a sequence and high load still costs.
- **“Tombstones can terminate a miss.”** Only EMPTY carries that historical proof.
- **“First tombstone is safe for unique insertion.”** an equal live key may occur later.
- **“Resize only changes the mask.”** home, stride, coverage, placement, load, and iteration can all change.
- **“Grouped quadratic means one slot per probe.”** current implementations inspect control groups and candidates.
- **“Random seeding fixes arithmetic.”** it cannot make a noncoprime stride cover missing residues.
- **“Expected constant time is unconditional.”** model, hash family, load, history, and adversary matter.

## Worked Examples

### Example 1

For `m=8`, home 3, triangular offsets yield `3,4,6,1,5,2,0,7`. All eight positions are distinct. Conclusion: this formula and capacity family support a full-cycle bound of eight.

### Example 2

For prime `p=7`, square offsets from home zero are `0,1,4,2,2,4,1`: only `{0,1,2,4}`. With at most three occupied slots, one of four candidates is empty; at four occupied slots, insertion is no longer guaranteed. Conclusion: partial coverage can support only a coupled load premise.

### Example 3

In `m=11`, double hashing with start 2 and stride 5 gives `2,7,1,6,0,5,10,4,9,3,8`. Since `gcd(5,11)=1`, its period is eleven. Conclusion: coprimality proves full coverage.

### Example 4

In `m=12`, start 1 and stride 4 reaches `1,5,9` then repeats. The period is `12/gcd(4,12)=3`, leaving nine positions unreachable. Conclusion: nonzero is necessary but not sufficient.

### Example 5

For power-of-two `m=16`, every odd stride is coprime to capacity; stride 6 has gcd two and visits eight slots. Conclusion: forcing a low bit to one is a coverage rule, not a hash-quality proof.

### Example 6

Keys A, B, C share start 2 and stride 5 in eleven slots, occupying 2,7,1. Deleting B must leave DELETED at 7 so lookup C crosses it. Conclusion: non-linear probing retains the deletion-history invariant.

### Example 7

After that deletion, inserting D remembers slot 7, checks slot 1 and then EMPTY slot 6, and reuses 7. If D equals C, equality at 1 prevents a duplicate. Conclusion: reusable does not mean terminal.

### Example 8

At `n=30,u=63,m=64`, live load is about 0.469 but fill is about 0.984. A full-cycle theorem prevents unreachable empties, yet misses may cross nearly all metadata. Conclusion: coverage proves termination, not acceptable latency.

### Example 9

Growing a prime-capacity double-hash table from 11 to 23 changes `h1 mod m` and the allowed `1..m-1` stride reduction. Copying old positions or old reduced strides can break lookup. Conclusion: resize reinserts from full hash information.

### Example 10

A grouped table reports two group probes, one fingerprint match, and one equality call. Calling that “two comparisons” hides eight or sixteen metadata lanes per group and payload traffic. Conclusion: benchmark units must correspond to the actual representation.

## Cross-Program Connections

- **Algorithms:** modular arithmetic, permutations, randomized analysis, and adversarial lower bounds distinguish theorem from measurement.
- **Programming languages:** overflow semantics, object lifetime, exceptions, generics, and iterator/reference rules constrain slot publication and relocation.
- **Computer architecture:** non-linear addresses trade reduced clustering for cache/TLB behavior; grouped metadata introduces vector width and alignment.
- **Software engineering:** the probe/capacity pair is a versioned module boundary with property tests, observability, and failure contracts.
- **Database engineering:** in-memory hash joins and indexes need workload, memory, spill, skew, and adversarial analysis beyond abstract average time.
- **Security engineering:** predictable start/stride collisions create resource-exhaustion paths; seeding, quotas, and telemetry are layered defenses.
- **Concurrent programming:** atomic slot states do not solve publication, resize, linearization, ABA, or reclamation.

## References

1. MIT OpenCourseWare, [6.006 Lecture 7: Hashing III—Open Addressing](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2008/resources/lec7/). Official lecture notes on tombstones, clustering, double hashing, coprime steps, and uniform hashing.
2. Yuhao Guo, Seth Pettie, and Chengzhang Wan, [A Simple Analysis of Quadratic Probing and Other Open Addressing Schemes](https://arxiv.org/abs/2608.08013). Current primary research on what is—and is not yet—proved about expected insertion cost for fixed-offset and quadratic probing.
3. Michael Mitzenmacher, [More Analysis of Double Hashing for Balanced Allocations](https://arxiv.org/abs/1503.00658). Primary coupling analysis that defines double-hash combinations and relates fully random behavior, balanced allocation, and the earlier open-addressing result under explicit asymptotic models.
4. Abseil Project, [`raw_hash_set.h`](https://github.com/abseil/abseil-cpp/blob/master/absl/container/internal/raw_hash_set.h). Current primary source for a grouped quadratic-probing table, control bytes, fingerprints, tombstones, and scoped load behavior.
5. Go Project, [runtime maps `map.go`](https://go.dev/src/internal/runtime/maps/map.go). Current primary source describing Swiss-style groups, quadratic probing, power-of-two group count, EMPTY termination, deletion, and growth.
6. Rust Project, [`std::collections::HashMap`](https://doc.rust-lang.org/std/collections/struct.HashMap.html). Current official statement of quadratic probing, SIMD lookup, hashing defaults, capacity, iteration, and API behavior.
7. Python Software Foundation, [CPython `dictobject.c`](https://github.com/python/cpython/blob/main/Objects/dictobject.c). Current perturbation recurrence and compact-layout contrast; not evidence for quadratic or double hashing.
8. ISO C++ working draft, [Unordered Associative Container Requirements](https://eel.is/c%2B%2Bdraft/unord.req.general). Observable hash/equality, complexity, load, rehash, and invalidation requirements without a mandated probe layout.
9. Scott A. Crosby and Dan S. Wallach, [Denial of Service via Algorithmic Complexity Attacks](https://www.usenix.org/legacy/event/sec03/tech/full_papers/crosby/crosby.pdf). Primary evidence for collision-driven resource attacks and threat modeling.
10. Oracle, [Java SE 25 `IdentityHashMap`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/IdentityHashMap.html). Current linear-probe identity-map contrast demonstrating that probe policy, equality, capacity, ordering, and synchronization are separate contracts.

## Exercises

### Exercise 1

Specify production-grade lookup, insertion, update, and deletion pseudocode parameterized by a finite probe generator. State preconditions, slot transitions, counts, duplicate behavior, maximum probe bound, failure commits, and what coverage the generator must provide.

### Exercise 2

Prove triangular offsets permute a table of capacity `2^r`. Then enumerate `i^2 mod 11`, determine its distinct candidate count, and derive the strongest occupancy threshold that alone guarantees an EMPTY in every square-offset probe set.

### Exercise 3

Prove the double-hash period `m/gcd(s,m)`. For capacities 13, 16, and 18, design a stride reduction that guarantees full coverage, and give one plausible but incorrect reduction with a counterexample for each composite capacity.

### Exercise 4

Design resize/rebuild, reserve, maximum-capacity, exception/lifetime, iterator/reference, serialization, and observability contracts for a flat double-hashed map. Include live/fill hysteresis and checked arithmetic.

### Exercise 5

Design a differential test and benchmark study comparing slot-linear, triangular quadratic, double-hash, grouped quadratic, and chaining tables without making a misleading universal-winner claim. Include arithmetic, semantic, security, memory, and tail-latency evidence.

## Answers to the Exercises

### Answer 1

Require `m>0`, deterministic in-range probes, and a declared distinct-candidate bound. Lookup examines at most that bound: EMPTY returns absent, DELETED continues, OCCUPIED filters by stored hash then equality. Unique insertion remembers the first DELETED, continues to equality or EMPTY/end, updates/rejects an equal key, and commits constructed payload into remembered DELETED or EMPTY. EMPTY insertion increments `n,u`; tombstone reuse increments `n`; update changes neither. Delete destroys/moves out the exact live payload, publishes DELETED safely, and decrements `n`. If all candidates are nonreusable, grow/report rather than loop. Failures before publication preserve the old slot/table; key hash/equality state remains stable while indexed. Coverage must ensure the allowed occupancy leaves a reachable reusable slot, or supply a full permutation.

### Answer 2

For `T_i=i(i+1)/2 mod 2^r`, equality at `i<j` implies `2^(r+1)` divides `(j-i)(i+j+1)`. The factors have opposite parity; the even factor would need divisibility by `2^(r+1)`, yet each is positive and smaller, contradiction. Thus all `2^r` offsets differ. Squares modulo 11 for `i=0..10` are `0,1,4,9,5,3,3,5,9,4,1`, giving six candidates `(11+1)/2`. With at most five occupied table slots, every six-slot candidate set has an EMPTY. Once six slots may be occupied, occupancy alone cannot guarantee it. Tombstones/non-EMPTY states require a stricter operational policy when EMPTY termination is required.

### Answer 3

The sequence repeats after positive `t` when `t*s=0 mod m`; dividing by `gcd(s,m)` makes the least such `t=m/gcd(s,m)`. For prime 13, use `1+(mix mod 12)`. For 16, map to an odd stride, such as `(mix mod 16)|1`. For 18, choose from the units `{1,5,7,11,13,17}` via a governed table or rejection/reduction proven uniform enough for the requirement. Incorrect `mix mod m` permits zero everywhere; `1+(mix mod 15)` for 16 can yield even stride 2; `1+(mix mod 17)` for 18 can yield stride 6 with period three. Hash distribution remains a separate obligation from coprimality.

### Answer 4

Track `n,u,m`, tombstones, growth-left, probe distributions, and memory/latency budgets. Grow before prospective load/fill or EMPTY-reserve limits; same-size rebuild when tombstones/probes exceed budget; shrink only below a lower sustained threshold, with hysteresis. `reserve` computes required capacity with checked arithmetic and selects a legal capacity/stride family. Rebuild allocates, recomputes home and stride from full hashes, constructs every live entry once, then atomically commits; failure retains the old representation or a documented recoverable state. Maximum capacity reports failure. State relocation invalidation, iteration-order instability, serialization by logical entries rather than raw slots/seeds, allocator/lifetime order, and thread-safety. Record capacity, loads, periods/policy version, probes/groups/equalities, rebuild/resize counts and latency, failures, and resource limits.

### Answer 5

First enumerate supported small capacities/homes/strides and verify periods against proofs, including zero/noncoprime negatives. Differentially generate put/update/get/delete/reserve/rebuild and compare logical contents while checking slot states, counts, uniqueness, reachability, termination, destruction, and rollback. Include same-home/start-stride keys, constant/structured hashes, tombstone churn, wrap, one EMPTY/full, capacity transitions, arithmetic maxima, mutable keys, expensive/throwing callbacks, and concurrent tests only for claimed concurrent designs. Benchmark identical semantics and budgets on realistic plus adversarial key/history distributions across live/fill sweeps, hit/miss/update/delete mixes, resize/rebuild, iteration, element sizes, hashes, seeds, and layouts. Report hardware/toolchains, bytes hashed, probes or groups with exact units, equality calls, cache/branch/vector behavior, allocations/memory, throughput, p50/p95/p99/max latency, repetitions, uncertainty, and raw artifacts. Conclusions stay scoped to those conditions.
