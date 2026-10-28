---
module_id: DSE-030
program: Data Structures Engineering
level: 1
module_number: 30
title: Engineering a Memory-Efficient Hash Map
status: complete
last_verified: 2026-08-30
---

# Engineering a Memory-Efficient Hash Map

## One-Page Review

### Governing question

How can an engineer choose and validate a hash-map representation that minimizes owned and peak memory for a defined workload while preserving lookup, mutation, iteration, lifetime, failure, and adversarial-behavior contracts?

### Essential definitions

- **logical payload** is the abstract key/value information; **owned footprint** is memory allocated by the map representation; **retained footprint** includes objects kept alive through its keys/values; **process footprint** includes allocator/runtime effects.
- `n` is live entries, `m` is physical capacity, and `alpha=n/m` is live load; **fill** may also count deleted/tombstone slots.
- **inline storage** places key/value payloads in the slot array; **node storage** places separately allocated nodes behind buckets/slots.
- **control metadata** records EMPTY/DELETED/FULL state and often a hash fingerprint separately from payload.
- **packed-entry indexing** stores compact bucket-to-entry indices while live entries reside densely elsewhere.
- **fingerprint/tag** is a small cached portion of a full hash used to reject non-candidates before key equality.
- **slack** is reserved but unused capacity; **fragmentation** is unusable space caused by alignment, size classes, allocation history, and holes.
- **small-buffer optimization** embeds capacity for tiny maps in the map object, avoiding a heap allocation at the cost of a larger object.
- **growth peak** is simultaneously live old, new, and temporary memory during resize or reseed.
- **bytes per live entry** is a scoped ratio whose numerator and denominator must be named; it is not a portable property of a container type.

### Central model, mechanism, or theorem

Memory accounting begins with representation equations, not resident-set-size division. Simplified owned-byte models include:

- inline flat: `B_flat = H + align(C(m)) + mS`;
- compact indexed: `B_indexed = H + align(mI) + pE`, where `p>=n` is packed-entry capacity;
- node-chained: `B_node = H + align(mP) + sum_j usable(node_j)`.

`H` is header state, `C(m)` control bytes and clones/padding, `S` inline slot size including alignment, `I` index width, `E` packed entry size, and `P` pointer/offset width. Real totals also include allocation headers/rounding, allocator fragmentation, separate node/key/value allocations, retained payload graphs, runtime/GC metadata, and old-plus-new growth overlap.

Reducing one term can increase another. High load lowers slack but lengthens probes and may require stronger metadata. Inline values eliminate nodes but waste `m-n` whole payload slots and relocate values on growth. Nodes preserve references but pay pointers, allocation rounding, and cache misses. Packed entries make iteration dense and let indices widen only at capacity thresholds, but add indirection and deletion compaction/order machinery. The correct design minimizes a measured objective subject to semantic and latency constraints.

### Critical invariants

1. Every live key/value appears exactly once, every occupied slot/index points to valid initialized storage, and no empty/deleted metadata exposes uninitialized payload.
2. `size`, capacity, live load, fill, deleted count, growth budget, control bytes, and packed/free lists agree.
3. Full hash/reduction selects the probe origin; tag matches identify candidates only and never replace full equality.
4. Alignment, offset/index width, capacity arithmetic, allocation size, and sentinel encodings cannot overflow or alias valid states.
5. Insert, erase, compact, resize, shrink, clear, and failure preserve payload lifetime exactly once.
6. Iterator/reference/handle invalidation follows the chosen inline, node, or packed representation contract.
7. Memory reports name what is included, allocator/toolchain/architecture, table state, and measurement method.
8. Hash-flooding and resource limits remain enforced; compactness must not depend on unsafe hash quality.

### Common failures

- Reporting `sizeof(map)` as the map's memory or RSS delta as exact owned bytes.
- Dividing capacity bytes by live entries without stating load, tombstones, small-table state, or payload inclusion.
- Counting keys/values both as inline bytes and again as transitive retained objects.
- Ignoring alignment padding, allocator size classes, node headers, control clones, and index-width transitions.
- Choosing high load solely for memory and then losing lookup latency, EMPTY termination, or attack resilience.
- Storing a tag and accepting it as equality.
- Compressing pointers/indices without checked representable ranges and reserved sentinel values.
- Claiming node storage is always larger or flat storage is always smaller regardless of payload size and slack.
- Measuring only the final table while growth briefly holds two tables and temporary move state.
- Shrinking automatically after every deletion and creating latency/allocation oscillation.

### Compact example

An explicit model compares 80 live `(8-byte key, 8-byte value)` entries at capacity 128. A flat design with a 48-byte header, `m+16` control bytes, and 16-byte inline slots owns 2,240 modeled bytes. An indexed design with one-byte indices and 24-byte packed entries owns 2,096. A chained design with 128 eight-byte bucket pointers and 80 32-byte rounded nodes owns 3,632. Flat growth to capacity 256 peaks at old plus new, 6,656 modeled bytes. These numbers prove the arithmetic under named assumptions only; allocator metadata and transitive payloads are explicitly excluded.

### Connections

[DSE-021](021-hash-functions-and-distribution.md) through [DSE-029](029-hash-flooding-resistance.md) supply placement, collision, resize, and security invariants. Earlier modules on [layout](005-contiguous-and-linked-layouts.md), [cache behavior](006-memory-locality-and-cache-behavior.md), [generic payloads](007-genericity-and-type-constraints.md), [testing](009-property-based-testing-of-data-structures.md), and [benchmarking](010-benchmarking-a-structure-without-misleading-results.md) define the evidence discipline. The [program roadmap](../ROADMAP.md) next begins ordered trees.

## Governing Question

Which ownership boundary, layout family, metadata encoding, capacity policy, payload strategy, invalidation contract, failure protocol, and measurement method yield the best memory/latency trade-off for the target keys, values, operations, and platform?

## Why This Matters

Maps can dominate a service's heap even when each logical association is tiny. A 16-byte key/value pair may occupy a control byte plus an empty-slot share, alignment padding, cached hash, pointer, node header, allocator rounding, and retained external objects. At millions of entries, a few bytes per slot become megabytes; an avoidable pointer per entry becomes cache and translation pressure as well as capacity.

Memory efficiency also changes speed and reliability. Dense metadata lets a lookup reject several slots using one cache line or vector operation. Packed iteration streams through live entries. Fewer allocations reduce allocator contention and fragmentation. Conversely, aggressive packing can increase moves, complicate deletion, invalidate references, raise probe tails, or require width-changing rebuilds. Low final memory can coexist with a dangerous resize peak.

Production designs make different choices because their contracts differ. Abseil Swiss tables separate compact control bytes from flat or node payload storage. Current Go maps use eight-slot groups and capped subtables to meet language iteration and growth requirements. CPython dictionaries use variable-width indices into a dense insertion-ordered entry array and also support shared-key split tables. Folly F14 exposes value, node, and vector policies across the size/stability spectrum. LLVM provides dense and inline-small variants for its workloads. The lesson is not a winner; it is how to derive and verify a layout.

## Prerequisites and Retrieval

Retrieve the abstraction/representation distinction and cost vectors from [DSE-001](001-abstract-data-types-and-concrete-representations.md) through [DSE-004](004-time-space-and-allocation-cost.md), layout/cache/alignment from [DSE-005](005-contiguous-and-linked-layouts.md) and [DSE-006](006-memory-locality-and-cache-behavior.md), ownership and type constraints from [DSE-007](007-genericity-and-type-constraints.md), iteration from [DSE-008](008-iterators-and-traversal-protocols.md), testing and benchmarking from [DSE-009](009-property-based-testing-of-data-structures.md) and [DSE-010](010-benchmarking-a-structure-without-misleading-results.md), and every hashing/collision/resize/security mechanism from [DSE-021](021-hash-functions-and-distribution.md) through [DSE-029](029-hash-flooding-resistance.md).

## Learning Objectives

After completing this module, you should be able to:

1. define logical, owned, retained, allocator, peak, and process memory scopes;
2. derive byte equations for inline, indexed-packed, vector-indexed, and node-based maps;
3. account for control/tag bytes, sentinel clones, alignment, slack, tombstones, index widths, and allocation rounding;
4. select load/growth/shrink policies by joint memory, probe, latency, and attack constraints;
5. choose inline, node, or packed payload storage from payload size, lifetime, stability, and iteration requirements;
6. design tiny-map and empty-map representation without imposing unjustified object-wide overhead;
7. implement checked capacity/index/offset encodings and exact payload lifetime transitions;
8. measure final and peak memory with both representation accounting and allocator/process tools;
9. validate correctness under deletion, compaction, width changes, failures, hostile hashes, and concurrency;
10. present an engineering recommendation with scoped evidence and explicit non-claims.

## Core Exposition

**Define the numerator before optimizing it.** A map object may own its header and backing allocation but merely reference key/value objects owned elsewhere. A node map may own nodes whose string fields own separate buffers. A garbage-collected runtime may retain objects through the table and add mark bits, spans, and allocator arenas. Copy-on-write pages and shared-key tables further blur process measurements.

Use at least four ledgers. Logical payload counts the information required by the abstract association. Direct owned bytes count the map object, buckets/control/indices, nodes, and directly owned payload buffers. Retained bytes include the transitive object graph kept reachable by entries. Process cost includes allocator arenas, fragmentation, runtime metadata, resident/committed pages, and shared pages according to a named tool.

There is no universal “bytes per entry” unless the numerator, `n`, capacity, fill, key/value representation, allocator, architecture, and state are fixed. Empty maps make the denominator zero. Tiny maps are dominated by headers/minimum allocations. Sparse post-deletion maps have a different ratio from freshly reserved maps with the same `n`. Report curves and state transitions, not one decorative number.

**Write a representation equation.** For a flat table, inventory the object header, allocation pointer/mask/size/growth fields, seed/hasher state, control bytes, mirrored control tail or sentinel region, alignment gap, and `m` slots of `sizeof(slot)`. `sizeof(pair<K,V>)` may exceed `sizeof(K)+sizeof(V)` because value alignment inserts padding. The allocation may round the total to an allocator size class.

For compact indexing, inventory `m` indices at width `I`, dense entry capacity `p` at size `E`, insertion/deletion order state, and possibly separate values. CPython's current source documents signed index widths that grow with table size and sentinel values for EMPTY and DUMMY. This saves index memory at small/medium capacities while dense entries make iteration proportional to entry history/live layout rather than scanning every hash slot.

For node chaining, add `m` bucket pointers/offsets, each node's next link, cached hash if present, key/value, alignment, allocator usable size, and allocator metadata/fragmentation. Separate allocations can preserve addresses and avoid reserving large inline payload slots for empties, so a node design can beat a flat design for sufficiently large payloads or low load even while losing locality.

Vector-indexed designs store compact indexes/tags in the hash structure and densely pack values in another array. Folly's current F14 description scopes this as one of several policies. It can reduce slack for large entries and improve iteration, but insertion/erase may move values and invalidate references. Stable handles require indirection, generations, tombstones/free lists, or node storage.

**Metadata is active search structure.** A separate control array lets lookup examine states and fingerprints without loading large keys/values. Abseil's Swiss-table design note describes one byte per slot: state plus seven hash bits. Current Go uses a 64-bit control word for eight slots. Candidate masks filter most slots before full equality; EMPTY states terminate a probe according to the algorithm, while DELETED states preserve reachability.

A tag is not identity. Multiple keys share seven or eight bits; every candidate still needs full hash/key equality as required. The expected number of false candidates depends on tag width, group occupancy, hash quality, and probe length. Correlated or hostile hashes invalidate a naive `occupancy/128` intuition. [DSE-029](029-hash-flooding-resistance.md) remains part of the design.

Control storage is not exactly `m` in many implementations. Vector loads may require cloned tail bytes, sentinel bytes, group rounding, and alignment. Tiny capacity can still allocate a full control group. Account from actual source/layout or allocation instrumentation rather than marketing shorthand.

Metadata choice affects deletion. Tombstones cost no payload slot in a separated layout once the value is destroyed, but they still consume probe history and fill budget. Backward-shift or tombstone-free deletion can reduce state bytes or cleanup rebuilds but must preserve reachability and may move entries. A packed occupancy bitmap, as current LLVM DenseMap source documents, has different vector/filter and deletion trade-offs from byte tags.

**Load factor trades slot slack for work.** With inline slot size `S`, unused-slot bytes are roughly `(m-n)S`; increasing `alpha` can save substantial memory for large `S`. Yet probes rise nonlinearly near full occupancy, unsuccessful lookup suffers first, and deletion needs a policy that preserves an EMPTY terminator or equivalent invariant. Collision defenses and tail-latency budgets set a maximum before raw memory minimization does.

The configured maximum load may not equal observed live load. Capacity quantization, growth hysteresis, `reserve`, deletion, tombstones, and shrink policy produce a distribution over states. A table that doubles at a threshold is sparsest immediately after growth. Model minimum, typical, maximum, post-reserve, post-delete, and during-migration states.

Reserve can reduce repeated allocations and peaks over a known build, but over-reserving retains slack. Exact-fit policies can trigger more frequent growth if estimates are low. Checked ceiling arithmetic must translate requested entries through the permitted fill/load and legal capacity. Reject addition, multiplication, shift, byte-size, index-width, and allocator-limit overflow before allocating.

Shrink is not free memory. It rehashes/moves entries, temporarily allocates a destination, invalidates according to contract, and may return pages only according to allocator behavior. Use explicit `shrink_to_fit`, lower-watermark hysteresis, sustained evidence, or domain-specific release points. Rust's current `HashMap` documentation explicitly allows internal rules to leave space after shrink requests and exposes fallible reserve for capacity/allocator failure.

**Payload size chooses between flat and indirect storage.** For tiny trivially movable keys/values, inline slots often minimize bytes and cache misses. As slot size or alignment grows, every empty flat slot wastes more, and growth copies/moves more bytes. A node or vector-indexed design keeps the probe/control structure small and touches payload only for candidates.

Node storage provides stable addresses across rehash in designs that promise it and can reuse nodes while replacing bucket arrays. Costs include one or more pointers/offsets, allocator rounding/header, fragmentation, allocation latency, pointer chasing, and more TLB/cache misses. Pool/slab allocation can amortize headers and improve locality but introduces ownership, empty-slab retention, concurrency, and reclamation policy.

Caching a full hash avoids recomputation during resize and rejects unequal colliders before expensive equality. It costs four/eight or more bytes, perhaps padding the entry further. It pays more for long strings, expensive generic hashers, node movement, or hash-flood detection; it may lose for cheap integers. A short control fingerprint captures only candidate filtering, not the full rehash benefit.

Indirect keys—string views, intern IDs, arena offsets, compressed handles—can shrink slots, but ownership moves elsewhere. A 32-bit arena offset is valid only if the arena span and sentinel reservation are checked. Views require source lifetime and immutability. Interning can save duplicate payloads while adding a global table, synchronization, retained lifetime, and its own attack surface. Count the whole system when making the claim.

**Packed entries change iteration and deletion.** A dense live-entry array makes iteration cache-friendly and can preserve insertion order naturally. Hash slots store narrow indices into it. Deleting an entry can leave a hole, maintain a free list, compact by moving the last entry, or periodically rebuild. Each choice changes stable order, iterator invalidation, reverse mapping, and memory.

If compaction moves entry `j` into hole `i`, the hash index that referred to `j` must be found and updated. A reverse slot index costs bytes; reprobe by cached full hash costs work; indirection/handles cost another field. Stable insertion order cannot use arbitrary swap-remove. CPython's actual deletion/order rules are source-specific and should not be guessed from the abstract layout.

Variable-width indices create thresholds. An encoding needs negative or reserved EMPTY/DELETED values, so the largest valid entry index may be smaller than the unsigned width suggests. Widening from one to two bytes doubles the index array and normally requires reallocation/rebuild. Test exact values around every threshold and ensure deserialization does not accept an out-of-range encoding.

**Tiny maps require a separate objective.** Programs often allocate many empty or one-element maps. A minimum heap table wastes an allocation and a whole group; an embedded small buffer avoids that but enlarges every map object, even large ones, and makes moves/copies more complex. Lazy allocation keeps empty maps cheap but adds a branch/state. Shared immutable empty storage saves allocation but requires safe first-write detachment.

LLVM's current `SmallDenseMap` is an example of explicit inline buckets. Folly F14 documents fractional small capacities within one metadata chunk and a compact empty object target. These are implementation observations, not portable sizes. Select inline capacity from a measured map-size distribution and object placement: adding 64 bytes to a million mostly-large map objects can lose more than it saves for a few tiny maps.

A tiny linear representation can be better than hashing: store two to eight key/value pairs inline and scan them, then promote to a table. That eliminates hash metadata and may use fewer branches/cache lines. Promotion must be failure-atomic, preserve order/equality/lifetime, and have hysteresis or one-way policy to avoid oscillation.

**Growth peak is a first-class memory constraint.** Stop-the-world resize commonly holds old and new arrays simultaneously. With inline values, both reserve capacity, and moving/copying may temporarily create two payload instances. Incremental rehash holds both longer and adds migration state. Node reuse can avoid duplicating payload nodes but still allocates new bucket/control storage.

The peak equation is not merely `B(old)+B(new)`: add allocator rounding, temporary construction/callback state, old generations awaiting readers, snapshots/iterators, failed destinations retained until cleanup, and concurrent builders. An out-of-memory failure near the final steady-state limit occurs because peak headroom was absent. Capacity admission must evaluate peak, not only destination size.

Growth factors trade peaks against frequency and slack. Doubling gives amortized movement but large post-growth slack and peak. Smaller factors reduce one jump yet rebuild more often and may interact badly with power-of-two/group constraints. Directory/subtable splitting, as current Go maps use, bounds an individual growth unit while adding directory/table headers and fragmentation across subtables. Measure the size distribution, not just a monolithic formula.

**Failure and lifetime rules constrain packing.** A flat resize may move nontrivial C++ objects; exceptions or throwing moves can require source retention/rollback. Rust unsafe internals must preserve initialization, aliasing, drop exactly once, allocation layout, and provenance. Garbage collection prevents manual frees but not stale logical references or retention leaks. A memory-efficient design that double-destroys, leaks on partial insertion, or reads uninitialized slots is invalid.

Define states for EMPTY, DELETED, FULL, and MOVING if migration is incremental. Publish payload before FULL metadata and remove visibility before destruction under the concurrency model. On insert failure, restore growth count and metadata. On erase, destroy exactly once and preserve probe reachability. On clear/drop, visit only initialized payloads and release each owned allocation once.

Pointer/reference/iterator stability must be explicit. Flat rehash moves values. Node rehash may preserve node addresses but deletion still invalidates the erased element. Packed compaction can move unrelated entries. Heterogeneous lookup may avoid temporary key allocation but requires compatible hash/equality across borrowed and stored forms. Memory savings do not justify silent contract changes.

**Concurrency adds metadata and fragmentation.** Locks, version words, control-state transitions, epochs, hazard records, per-thread caches, and deferred retired tables all count. Sharding reduces contention but duplicates headers, minimum capacities, slack, and skew. A 64-shard map with one entry can be far larger than one table. Hot shards grow while cold shards retain minimum storage.

Lock-free or read-optimized designs may keep multiple generations until grace periods, making instantaneous retained bytes workload-dependent. Report current, retired, and reclaimable memory separately. Compaction/growth must publish payload/control with correct memory ordering; a reader cannot treat a matching tag as proof that construction is complete.

NUMA placement, huge pages, cache coloring, and allocator arenas can dominate large maps. Compact control metadata may fit in cache while payload lives remotely. Pooling nodes by NUMA domain improves locality but changes balancing/migration. These are empirical platform decisions, not consequences of asymptotic load factor.

**Security and resource control remain non-negotiable.** A high maximum load or narrow tag assumes a competent, possibly keyed hash and defined untrusted-key policy. Hostile collisions increase probes/candidates/equality and can trigger repeated cleanup/growth. Compressed lengths and offsets invite integer overflow. Deserializing physical capacity or index metadata from untrusted bytes can request huge allocations or forge out-of-range references.

Apply checked entry/byte/capacity arithmetic, keyed/default hash policy, maximum probe/relocation/rebuild work, request/tenant quotas, allocation/peak budgets, and typed failure. Validate logical serialized entries into a fresh representation; do not trust serialized control bytes, seeds, pointers, padding, or allocator sizes. Zero or protect secrets on retirement according to the security model.

**Measurement needs two independent views.** First, instrument the implementation's exact requested allocation sizes and states: header, control/index, slots, nodes, packed capacity, tombstones, free lists, old/new generations, and temporary buffers. This verifies the representation equation. Second, use allocator/runtime/process tools to measure usable/allocated/resident/committed bytes and fragmentation. Differences are evidence, not noise to hide.

Measure at empty, tiny, threshold-minus/plus, pre-growth, post-growth, high load, post-delete, post-shrink, and migration states. Sweep key/value size/alignment, inline versus indirect ownership, hash/equality cost, hit/miss ratio, insert/delete mix, reserve accuracy, hostile distributions, shard skew, thread count, and memory pressure. Record allocator, ABI, architecture, compiler/runtime, sanitizers, CPU affinity, page state, warmup, repetitions, uncertainty, and raw artifacts.

Report memory together with performance: requested/usable/resident/peak bytes, bytes per live entry under named scope, allocations, moved/copied bytes, probes/groups/candidates/equality, throughput, p50/p95/p99/max latency, iteration bandwidth, cache/TLB misses, branch behavior, growth frequency/duration, and reclamation age. Sanitizers and debug allocators alter layout; measure them for correctness evidence but not as release-size claims.

The executable model below compares three simplified layouts using exact declared constants. It uses a 16-byte round-up for selected metadata/bucket arrays, treats node size as already allocator-rounded, and assumes the indexed entry array contains exactly `n` entries. It deliberately excludes allocator headers/arena fragmentation and transitive payloads. It verifies arithmetic and growth overlap, not any named implementation's footprint.

<!-- bijux-verify: {"id":"hash-map-layout-accounting","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"entries=80\nflat_owned_bytes=2240\nindexed_owned_bytes=2096\nnode_owned_bytes=3632\nflat_bytes_per_live=28.00\nindexed_bytes_per_live=26.20\nnode_bytes_per_live=45.40\nflat_growth_peak_bytes=6656\nexcluded=allocator_metadata_and_transitive_payloads\nevidence=finite_layout_accounting_model\n","stderr":""}} -->
```python
from dataclasses import dataclass


def round_up(value, alignment=16):
    return ((value + alignment - 1) // alignment) * alignment


@dataclass(frozen=True)
class Layout:
    header: int
    metadata_per_capacity: int = 0
    metadata_tail: int = 0
    slot_per_capacity: int = 0
    packed_per_live: int = 0
    bucket_pointer: int = 0
    rounded_node: int = 0

    def owned_bytes(self, live, capacity):
        if self.rounded_node:
            buckets = round_up(capacity * self.bucket_pointer)
            return self.header + buckets + live * self.rounded_node
        metadata = round_up(
            capacity * self.metadata_per_capacity + self.metadata_tail
        )
        return (
            self.header
            + metadata
            + capacity * self.slot_per_capacity
            + live * self.packed_per_live
        )


flat = Layout(header=48, metadata_per_capacity=1, metadata_tail=16,
              slot_per_capacity=16)
indexed = Layout(header=48, metadata_per_capacity=1, packed_per_live=24)
node = Layout(header=48, bucket_pointer=8, rounded_node=32)
live = 80
old_capacity = 128
new_capacity = 256

flat_bytes = flat.owned_bytes(live, old_capacity)
indexed_bytes = indexed.owned_bytes(live, old_capacity)
node_bytes = node.owned_bytes(live, old_capacity)
flat_peak = flat_bytes + flat.owned_bytes(live, new_capacity)

print(f"entries={live}")
print(f"flat_owned_bytes={flat_bytes}")
print(f"indexed_owned_bytes={indexed_bytes}")
print(f"node_owned_bytes={node_bytes}")
print(f"flat_bytes_per_live={flat_bytes / live:.2f}")
print(f"indexed_bytes_per_live={indexed_bytes / live:.2f}")
print(f"node_bytes_per_live={node_bytes / live:.2f}")
print(f"flat_growth_peak_bytes={flat_peak}")
print("excluded=allocator_metadata_and_transitive_payloads")
print("evidence=finite_layout_accounting_model")
```

## Definitions and Notation

- `n`: live logical entries.
- `m`: physical table/bucket capacity.
- `alpha=n/m`: live load factor; fill may additionally include deleted states.
- `H`: map/table header and scalar state bytes.
- `C(m)`: control/state/tag bytes including required tail/sentinel/padding.
- `S`: aligned inline slot bytes.
- `I`: encoded bucket-to-entry index bytes.
- `p`: packed-entry capacity, which may exceed `n`.
- `E`: aligned packed entry bytes.
- `P`: bucket pointer or offset bytes.
- `usable(node)`: allocator-usable/rounded node allocation size under a named allocator.
- **owned/retained/process/peak**: distinct memory scopes that must not be conflated.
- **candidate**: slot whose short tag matches and therefore requires full key verification.
- **width transition**: capacity/entry threshold at which index/offset encoding widens.

## Mechanisms, Invariants, or Proof Structure

The memory proof inventories every direct representation field and allocation, applies actual alignment and capacity rules, and sums each owned region exactly once. It then separately identifies excluded transitive/runtime/allocator costs. State-specific equations cover empty, loaded, deleted, growing, and retired generations.

Correctness couples metadata to lifetime: FULL identifies one initialized logical entry; EMPTY/DELETED never exposes a live payload; counts and growth budget agree; tags only filter candidates; indices/offsets are representable and reference the correct dense entry. Every mutation, compaction, width change, and rebuild preserves exact content and destroys each payload once.

The engineering selection is constrained optimization: minimize a scoped memory metric or peak subject to lookup/mutation/iteration tails, stability/order, failure, concurrency, and adversarial limits. Benchmark evidence calibrates constants; it cannot replace the representation proof or generalize across allocators, ABIs, payloads, and workloads.

## Alternatives and Trade-Offs

| Layout/policy | Memory advantage | Cost or contract obligation |
|---|---|---|
| Flat inline slots | no per-node allocation/link; strong locality | empty-slot payload slack, relocation/invalidation |
| Separate control bytes | compact hot search metadata and candidate filtering | tail/alignment bytes and tag-correctness rules |
| Variable-width indices + packed entries | narrow sparse index; dense/order-friendly iteration | indirection, width rebuild, deletion/order machinery |
| Node storage | avoids empty large payload slots; stable addresses possible | pointers, allocator overhead/fragmentation, cache misses |
| Vector-indexed packed values | dense values and small hash slots | moving erase/rehash and handle invalidation |
| Cached full hash | cheaper reject/rehash for expensive hashes | per-entry bytes/padding and secret-handling scope |
| Embedded tiny representation | avoids allocation for common tiny maps | larger object and promotion complexity |
| Lazy/shared empty state | cheap empty maps | first-write branch/detachment and concurrency |
| High maximum load | less slot slack | longer tails, deletion/EMPTY/security constraints |
| Conservative shrink | avoids oscillation and rebuild cost | retained slack after workload contraction |
| Sharding | contention isolation | duplicated headers/minima and skewed slack |

## Failure Modes and Misconceptions

- **“`sizeof` is footprint.”** it usually omits backing allocations and retained payloads.
- **“RSS delta is owned bytes.”** allocator arenas, page state, sharing, GC, and unrelated activity intervene.
- **“One control byte means one overhead byte per live entry.”** capacity slack, tails, padding, and other fields remain.
- **“Flat always uses least memory.”** large aligned payloads waste whole empty slots.
- **“Nodes always use most memory.”** they can avoid large slack and preserve payload addresses, depending on size/load/allocator.
- **“Maximum load equals actual load.”** growth quantization, reserve, delete, and shrink history change it.
- **“Fingerprint match is key match.”** short tags only select candidates.
- **“Narrow index is just a cast.”** sentinels, overflow, widening, and corrupted input need proofs.
- **“Final bytes are the limit.”** resize, snapshots, readers, and failure cleanup determine peak.
- **“Shrink returns memory now.”** table and allocator policies may retain capacity/pages.
- **“Compact means fast.”** movement, indirection, high probes, and decompression can dominate.
- **“A benchmark proves a universal winner.”** payload, operation mix, platform, allocator, and contract select the result.

## Worked Examples

### Example 1

An empty map has a 48-byte header and no allocation. “Bytes per live entry” is undefined, not zero or 48. Conclusion: report absolute footprint for empty state.

### Example 2

At `n=80,m=128`, 16-byte flat slots reserve 2,048 payload-slot bytes; 768 of those bytes belong to 48 currently empty slots. Conclusion: payload size magnifies slack.

### Example 3

The flat model adds 144 control bytes (`m+16`) and a 48-byte header, totaling 2,240 bytes. Conclusion: “one byte per slot” is only one equation term.

### Example 4

One-byte indices plus 80 packed 24-byte entries and a 48-byte header total `128+1,920+48=2,096`. Conclusion: packed indexing wins this model but assumes exact packed capacity and movable/managed entries.

### Example 5

The node model uses `128*8=1,024` bucket bytes plus `80*32=2,560` rounded nodes and a 48-byte header, totaling 3,632. Conclusion: allocator-rounded node cost must be named.

### Example 6

Growing the flat model from 128 to 256 while both tables exist uses `2,240+4,416=6,656` bytes before temporary/allocator costs. Conclusion: admission based on final 4,416 bytes can fail at peak.

### Example 7

A 7-bit tag matches a candidate, but two unequal strings share it. Full equality rejects the slot. Conclusion: tag storage saves payload accesses without changing map semantics.

### Example 8

An index encoding reserves `-1` and `-2` for EMPTY/DELETED. Capacity crosses its signed-width limit and the array widens. Conclusion: width thresholds depend on sentinels, not only nominal unsigned maximum.

### Example 9

A vector-packed map erases entry 10 by moving entry 79 into its hole and updating the corresponding hash index. A saved pointer to entry 79 is now stale. Conclusion: compaction and stability are inseparable.

### Example 10

A 64-shard map duplicates headers and minimum groups while 60 shards remain nearly empty. Conclusion: concurrency partitioning can dominate memory at small or skewed cardinality.

## Cross-Program Connections

- **Computer architecture:** cache/TLB lines, SIMD/tag filtering, alignment, prefetch, NUMA, pages, and bandwidth determine the value of compactness.
- **Programming languages:** object layout, provenance, moves, exceptions, GC, drop/destructors, borrowed lookup, and ABI define safe encodings.
- **Algorithms:** load/probe models, amortized growth, adversarial hashing, width thresholds, and packed-compaction costs bound behavior.
- **Operating systems:** virtual/resident/committed memory, page faults, copy-on-write, huge pages, and allocator arenas affect process evidence.
- **Concurrent programming:** shards, locks, epochs, retired generations, publication, and reclamation add state and delayed memory.
- **Database/data engineering:** dictionaries, hash joins/aggregation, encoding widths, arenas, partition skew, spill, and peak admission use the same accounting.
- **Software engineering:** stable contracts, instrumentation, raw artifacts, typed capacity failure, and migration compatibility keep optimization reviewable.
- **Security engineering:** seed policy, collision work, integer overflow, deserialization, quotas, and peak-memory denial of service constrain packing.

## References

1. Abseil Project, [Swiss Tables Design Notes](https://abseil.io/about/design/swisstables). Official design explanation of separate one-byte control metadata, hash splitting, candidate filtering, allocation-aware emplacement, and flat/node variants.
2. Abseil Project, [`raw_hash_set.h`](https://github.com/abseil/abseil-cpp/blob/master/absl/container/internal/raw_hash_set.h). Current primary implementation source for control layout, capacity, growth, probing, storage policy, and allocation details.
3. Go Project, [Faster Go Maps with Swiss Tables](https://go.dev/blog/swisstable). Official engineering explanation of eight-slot groups, control words, candidate filtering, load factor, runtime constraints, and measured rollout scope.
4. Go Project, [runtime maps `map.go`](https://go.dev/src/internal/runtime/maps/map.go). Current primary representation source for groups, directory/tables, capped growth units, seed, counts, and iteration obligations.
5. CPython Project, [`Objects/dictobject.c`](https://github.com/python/cpython/blob/main/Objects/dictobject.c). Current primary source for variable-width indices, EMPTY/DUMMY encodings, dense general/Unicode entries, combined/split forms, and insertion-order representation.
6. Folly Project, [F14 Hash Table](https://github.com/facebook/folly/blob/main/folly/container/F14.md). Primary design source comparing node, inline-value, vector-indexed, and adaptive storage policies, small capacities, reserve behavior, iteration, and reference stability.
7. Rust Project, [`std::collections::HashMap`](https://doc.rust-lang.org/std/collections/struct.HashMap.html). Current API contract for capacity, reserve/try_reserve failure, shrink behavior, iteration, hashing, and borrowed lookup.
8. Rust `hashbrown` Project, [repository and implementation](https://github.com/rust-lang/hashbrown). Current primary Swiss-table implementation lineage and source for control/data allocation, capacity, probing, allocation layout, and Rust lifetime/drop obligations.
9. LLVM Project, [`DenseMap.h`](https://llvm.org/doxygen/DenseMap_8h_source.html). Current primary source for packed occupancy, allocation-size arithmetic, power-of-two capacity, load policy, dense buckets, and `SmallDenseMap` inline optimization.
10. ISO C++ working draft, [Unordered Associative Container Requirements](https://eel.is/c%2B%2Bdraft/unord.req.general). Current observable hash/equality, capacity/load, reserve/rehash, complexity, iteration, and invalidation requirements without mandating a physical layout.

## Exercises

### Exercise 1

Create exact owned/retained/peak equations for a flat-control map, compact-indexed map, and node map storing your chosen `K,V`. Include alignment, capacity policy, index thresholds, allocator rounding, payload ownership, and excluded terms.

### Exercise 2

Choose inline, node, vector-indexed, or hybrid storage for three workloads: tiny integers, 256-byte movable values, and stable-address polymorphic objects. Justify load, cached-hash, small-map, and invalidation policies.

### Exercise 3

Specify metadata and operation invariants for a Swiss-style flat map with EMPTY/DELETED/FULL tags, short fingerprints, reserve, erase, tombstone cleanup, and failure-atomic growth.

### Exercise 4

Design a measurement harness that reconciles representation accounting with allocator and process metrics across lifecycle states. Include peak growth, fragmentation, concurrency/shards, and reproducibility controls.

### Exercise 5

Design property, boundary, fault, adversarial, lifetime, and concurrency tests for a compact map with variable-width indices and a tiny inline representation. State what evidence would and would not justify production adoption.

## Answers to the Exercises

### Answer 1

For flat storage use `H+align(control(m)+tail)+m*align(sizeof(K),sizeof(V),pair layout)`, then add allocator rounding and any hasher/seed allocation. For indexed storage use `H+align(m*I)+align(p*E)+order/free/reverse metadata`; define `I` at each signed/sentinel threshold and `p` from packed-vector policy. For nodes use `H+align(m*P)+sum usable(node_j)` plus pool/slab headers and empty retained slabs where applicable. Direct owned payload buffers belong in owned bytes; externally owned objects do not, but the transitive graph they keep alive belongs in retained bytes. Peak adds old/new allocations, duplicated/moved payload, temporary state, readers/snapshots, and cleanup after failure. State architecture, ABI, allocator, load/fill/deletions, capacity, ownership, and exclusions; never infer exact owned bytes from RSS alone.

### Answer 2

Tiny integers favor inline control-plus-slots, a measured tiny inline/linear state, no full cached hash unless profiling supports it, and a safe high-but-not-tail-breaking load. Movable 256-byte values favor small control/index slots plus a packed value vector or nodes: vector packing minimizes slack and iteration cost if pointer invalidation/moving erase are acceptable; nodes preserve addresses and reduce moves. Stable polymorphic objects require node/arena/handle indirection with explicit ownership and reclamation; flat slots cannot silently invalidate them. Each design uses checked reserve/growth, collision-resistant hashing, resource limits, and a documented iterator/reference matrix. Small optimization is selected from cardinality distributions, not assumed universal.

### Answer 3

Each capacity position has one tag: EMPTY terminates according to the probe theorem, DELETED preserves reachability but contains no initialized payload, and FULL contains a fingerprint whose slot holds exactly one initialized entry. `size=FULL count`; `fill=FULL+DELETED`; growth-left matches the permitted occupancy policy. Lookup computes full hash, probes groups, uses tag masks only to choose full equality candidates, and stops only on an allowed EMPTY. Insert constructs payload before publishing FULL and rolls back counters/metadata on failure. Erase removes visibility, destroys once, installs DELETED or performs a proven shift, and updates counts. Cleanup/growth builds a destination from each live entry exactly once, validates placement/count, publishes atomically/exclusively, then retires old storage. Checked capacity, byte arithmetic, control tail/alignment, seed, hash/equality, and lifetime are part of the invariant.

### Answer 4

Instrument every requested allocation/deallocation with purpose, requested and allocator-usable bytes, capacity, size, fill, packed capacity, index width, generation, and timestamp. Snapshot empty, tiny thresholds, pre/post growth, post reserve, deletion/tombstone, shrink, migration, failure, and reader-retired states. Independently collect allocator allocated/active/resident/retained statistics and OS resident/committed/private metrics; reconcile expected direct bytes with usable rounding, arenas, pages, unrelated baseline, GC, and sharing. Sweep payload size/alignment/ownership, cardinality/load, reserve error, operation mix, hashes, shards/skew/threads, and pressure. Record toolchain/ABI/allocator/architecture, warmup, affinity, repetitions, uncertainty, latency/throughput/probes/cache/TLB/allocations/moves, and raw artifacts. Peak sampling must be frequent or event-driven enough to capture simultaneous generations.

### Answer 5

Model-test all operations against a reference map across empty, inline maximum, promotion, demotion policy, every index-width boundary, maximum capacity, duplicate/update/delete, tombstones, cleanup, reserve, shrink, clear, copy/move/drop, and serialization. Assert state counts, tag/payload initialization, placement, index ranges, dense reverse mappings, exact order/stability contract, and one destruction per payload. Inject allocation, hash, equality, move/copy, promotion, widening, growth, and publication failure. Use same-full-hash, same-tag, long probes, deletion histories, overflow encodings, corrupt physical input rejection, repeated growth, and peak-budget exhaustion. Race readers/writers with promotion/growth/compaction/retirement under sanitizers and history checking. Adoption additionally needs representative release-build memory/latency data, allocator/process reconciliation, dependency/platform testing, security/resource review, and named human review. Finite tests do not prove universal minimum memory, hash-flood immunity, exception safety for all types, lock-free correctness, cross-ABI layout, or workload-independent superiority.
