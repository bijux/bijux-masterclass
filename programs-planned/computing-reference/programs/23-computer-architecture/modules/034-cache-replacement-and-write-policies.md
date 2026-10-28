---
module_id: CA-034
program: Computer Architecture
level: 1
module_number: 34
title: Cache Replacement and Write Policies
status: complete
last_verified: 2026-09-04
---

# Cache Replacement and Write Policies

## One-Page Review

### Governing question

When a cache set is full or software writes a cached address, which resident may be displaced, where do the authoritative updated bytes live, when must lower levels observe them, and how do policy choices affect correctness, traffic, latency, endurance and recoverability?

### Essential definitions

- A **replacement policy** chooses an eligible victim line when allocation targets a full set.
- **invalid-first** allocation uses an invalid eligible way before evicting a valid resident.
- **least recently used** (`LRU`) evicts the resident whose most recent qualifying access is oldest.
- **first in, first out** (`FIFO`) evicts by insertion age rather than hit recency.
- **pseudo-LRU** approximates LRU with less state/update logic.
- **random replacement** chooses among eligible ways using a defined random/pseudorandom source.
- **insertion policy** selects the initial replacement priority of a newly filled/prefetched line.
- **write-through** propagates each accepted cache write toward the next level while maintaining the cached copy.
- **write-back** modifies the cache, marks the line dirty, and writes it lower on eviction/clean/flush.
- **write-allocate** brings/owns a missed line before applying a write.
- **no-write-allocate** sends a write miss lower without installing the line.
- A **write buffer** decouples CPU/cache acceptance from lower-level completion.
- **write combining** merges compatible writes to reduce transactions.
- A **dirty line** contains bytes newer than the corresponding lower-level copy.
- A **persistence point/domain** identifies when a write survives specified failures; cache write policy alone does not define durability.

### Central model, mechanism, or theorem

Replacement is constrained selection: on allocation into set `s`, choose an invalid eligible way if one exists; otherwise `victim=Policy(R_s,eligible_s)`. Preserve dirty victim identity/data until its writeback obligation completes, then install the incoming block and update policy state exactly once. Write correctness tracks ownership: write-through accepts a store only with a buffered/ordered lower propagation obligation; write-back makes the dirty cache line the newest owned copy until ordered writeback. For every architectural load after ordered stores, returned bytes must equal the coherent memory abstraction, regardless of which performance policy chose residence.

### Critical invariants

- Replacement never selects invalid, locked, transient or otherwise ineligible state incorrectly.
- An eligible invalid way is chosen before a valid eviction under invalid-first policy.
- Replacement metadata updates on exactly the defined hit, fill, prefetch, coherence or replay event.
- Dirty victim tag/index/data/mask remain coherent until lower acceptance/completion required by protocol.
- At most one cache-domain owner represents the newest writable copy of each block under coherence rules.
- Write hits update exactly enabled byte lanes and preserve all others.
- Write-through buffering cannot acknowledge more writes than it can retain/order.
- Write-back eviction cannot discard dirty data or expose incoming tag with victim data.
- Write misses follow allocation and memory-type/device ordering policy exactly.
- Clean/flush/fence completion corresponds to the specified visibility or persistence boundary.

### Common failures

Common failures include running replacement when an invalid way exists, calling tree-PLRU exact LRU, updating recency on every speculative lookup, choosing a busy/locked victim, overwriting dirty data before writeback acceptance, reconstructing victim address from incoming tag, acknowledging write-through with a full buffer, merging writes across incompatible address/order/device attributes, assuming write-back means durable, assuming write-through means globally visible immediately, fetching a whole line for no-write-allocate, mishandling partial stores, replaying an accepted non-idempotent write, and comparing traffic using payload bytes for one policy but line bytes for another.

### Compact example

For a three-line set and trace `[0,1,2,0,3,0,1,2,3]`, exact LRU gives two hits while FIFO gives one because a hit refreshes only LRU recency. In a two-line write-back/write-allocate example with six operations, one hit and five fills cause three dirty victim writebacks, totaling 512 lower-level bytes at 64-byte lines before final drain. Separately, 10,000 repeated 8-byte stores across 100 lines generate 80,000 payload bytes under an ideal byte-granular write-through/no-allocate model, versus 12,800 line bytes for one fill and one eventual writeback per line under write-back/write-allocate—a synthetic 84% reduction whose assumptions must be verified.

### Connections

Replacement/write policy connects locality, associativity, dirty ownership, store buffers, coherence, device memory, fences/maintenance, persistence, endurance, security partitioning, trace simulation and performance/energy evidence.

## Governing Question

Replacement decides which cached information remains available. Write policy decides where the newest data resides and what obligation accompanies a store. They interact whenever a victim is dirty or a write miss allocates.

Correctness should not depend on predicting future reuse. A poor replacement policy may cause more misses; it must never lose or fabricate data. Write policy, by contrast, directly participates in memory visibility and failure behavior.

## Why This Matters

Workloads differ: recency helps repeated working sets; scans can evict useful lines; randomization avoids some deterministic patterns. Prefetch and coherence events complicate what counts as reuse.

Write-through simplifies lower-level freshness but creates traffic/buffering pressure. Write-back amortizes repeated writes but adds dirty state, eviction latency and recovery/maintenance obligations.

Policies also affect security, QoS and endurance. Shared replacement state can leak contention, and write amplification can dominate nonvolatile-media wear.

## Prerequisites and Retrieval

Before studying this module, be able to:

- trace set-associative hit, miss, victim and refill state;
- distinguish valid, dirty and transient lines;
- reason about byte masks and lower-level handshakes;
- compute line/payload traffic and AMAT components;
- explain architectural memory ordering and cache maintenance at a basic level.

Retrieve exact cache geometry and address identity; eligible/locked/partitioned/transient ways; replacement algorithm, state encoding, invalid-first, insertion and update events; prefetch/coherence/replay treatment; random seed/source; read/write ports; write-through/back and write-allocate/bypass rules per memory type; byte/subline/atomic behavior; write/eviction/victim buffers and depths; merge ordering; dirty ownership and coherence protocol; lower-level request/response/error/retry; fences and clean/invalidate/flush semantics; DMA/noncoherent agents; persistence domain and power-fail guarantees; ECC/poison; reset/recovery; counters/traces; synthesis/STA/area/power/endurance; simulator/reference model; tests/formal properties; hardware/firmware/OS/tool/library revisions and errata.

## Learning Objectives

After completing this module, you should be able to:

1. separate victim eligibility from replacement preference;
2. implement and trace LRU, FIFO, pseudo-LRU and random-like policies;
3. define insertion/update behavior for demand, prefetch, replay and coherence events;
4. compare write-through/write-back and allocate/no-allocate combinations;
5. preserve byte correctness, dirty ownership and victim writeback identity;
6. size and verify write/victim buffers and combining rules;
7. distinguish visibility, coherence, ordering and persistence completion;
8. compute fills, writebacks, payload/line traffic and write amplification;
9. verify cache data refinement independently of policy quality;
10. choose policies using representative traces and physical/system evidence.

## Core Exposition

### Separate eligibility from preference

First exclude ways that cannot be replaced: invalid handling aside, locked, partition-excluded, transient, probed, pinned or otherwise reserved entries may be ineligible. Only then apply a preference policy.

If every way is ineligible, backpressure or wait. Evicting protected state to avoid a stall violates ownership.

### Choose invalid capacity first

Under invalid-first allocation, any eligible invalid way avoids loss of a valid block and possible dirty writeback. Define deterministic selection among several invalid ways.

Initialize replacement metadata consistently when ways are invalidated/reset. Invalid ways should not distort victim order unexpectedly.

### Define policy events

State exactly which event updates replacement metadata: qualified demand hit, fill installation, prefetch, maintenance touch, coherence probe, writeback lookup or speculative access.

Use one logical update even if an operation replays over several cycles. Killed speculative work may or may not train policy; document performance/security consequences.

### Implement exact LRU

For a small set, keep ways ordered from least to most recent. A qualifying hit removes its way from the current position and appends it as MRU; fill does likewise under insertion policy.

Exact LRU state grows with associativity and its update network can affect timing. Verify every permutation and simultaneous event.

### Understand FIFO

FIFO records insertion order. Hits do not change victim age. It is cheaper in some implementations and can outperform LRU on selected cyclic traces, but ignores temporal hits.

Do not label a rotating pointer FIFO unless it advances exactly on qualifying replacement/insertion events and handles invalid ways correctly.

### Understand pseudo-LRU

Tree-PLRU uses direction bits to approximate a cold subtree and updates away from the accessed path. Bit cost is often `W-1` per set for power-of-two ways.

It lacks exact LRU's full recency order and stack behavior. Test traces that revisit ways in patterns exposing its approximation.

### Understand random replacement

Random/pseudorandom choice can avoid fixed adversarial cycles and simplifies metadata. The generator distribution, seed/reset and modulo selection must avoid systematic bias.

Reproducible testing records the seed/state. Security analysis asks whether predictability or shared random state matters.

### Consider re-reference policies

RRIP-like policies store a small predicted interval until reuse. Insertion can protect established residents from scans by placing new lines near eviction rather than MRU.

Such policies can outperform LRU on mixed scans/reuse but introduce tuning and workload sensitivity. State the exact variant and update rules.

### Consider bypass and insertion

An allocation policy may bypass a low-value block or insert it at low priority. Prefetches often use different insertion from demand.

Bypass cannot violate inclusion/coherence/atomicity requirements. A wrong prediction should cost performance, not correctness.

### Preserve a dirty victim

Before replacement, capture stored victim tag, set, dirty/coherence state and data. Reconstruct the victim block address from stored identity.

Do not overwrite tag/data/dirty until a victim buffer owns the obligation or lower-level protocol reaches the required point. Writeback error needs retry/fault/containment policy.

### Use a victim buffer carefully

A victim buffer decouples dirty eviction from refill and can catch conflict reuses. It becomes another possible owner/lookup source.

Track unique block identity, valid/dirty state and request acceptance. Full buffer prevents another dirty victim unless lower service frees capacity.

### Define write-through hits

On a write hit, update selected byte lanes and enqueue the lower write with address/data/mask/attributes/order tag. CPU acknowledgment depends on architecture and buffer acceptance, not necessarily lower completion.

If the write buffer is full, backpressure before accepting. A later read may need forwarding from buffered writes if the cache/lower copy ordering exposes stale bytes.

### Define write-back hits

On a write hit, update selected lanes and set dirty/ownership state. Lower propagation occurs on eviction, clean/flush or coherence request.

Dirty means the cache-domain copy is newer; it does not imply persistent storage. ECC protects data/state according to policy.

### Define write-allocate misses

Acquire/refill the target line, merge the pending store mask/data, then publish valid dirty state. Full-line stores may avoid reading old bytes if the protocol supplies ownership and all bytes.

Partial stores require old untouched bytes from refill or subline validity. Atomic operations require stronger read-modify-write serialization.

### Define no-write-allocate misses

Send the write to the next level without installing the line. This avoids cache pollution/fill traffic for streams but repeated writes/reads may miss.

Check for an existing transient/victim/buffered copy first. Bypass must not create two incoherent newest copies.

### Match common policy pairs

Write-back commonly pairs with write-allocate so dirty merging occurs in cache. Write-through often pairs with either allocation or no-allocate.

These are conventions, not laws. Specify actual behavior per cache level, memory type, operation and full/partial line case.

### Handle partial writes

Byte enables select updated lanes; all other bytes remain from the correct prior line. Buffer combining can merge disjoint/overlapping masks only when address, order and attributes permit.

For overlapping bytes, newer program-order data wins. Endianness affects byte interpretation, not address mask identity.

### Handle write combining

Combine adjacent/same-line stores to reduce lower transactions. Retain ordering tags and exception/commit status; do not merge across fences, device semantics or principals incorrectly.

Capacity accounting includes partial entries. A combining buffer can delay visibility and affect latency tails.

### Handle read-after-write

A load after an older store must observe required forwarding/coherence even if the lower write remains buffered. Search store/write buffers or maintain the cache line as the authoritative copy.

Partial overlap needs byte-wise merging from the newest older stores plus cache/lower data.

### Handle device and uncached memory

Device accesses can have side effects and strict sizes/order. They often bypass normal caches and combining, but exact platform rules govern.

Never replay or merge an accepted non-idempotent write merely because cached-memory paths do so.

### Integrate coherence

Write-back coherence represents dirty/exclusive ownership and supplies data on probes or writes it lower. Replacement may need to initiate eviction protocol before the way becomes reusable.

Write-through does not eliminate coherence: other caches still need invalidation/update rules. Policy state cannot contradict coherence state.

### Integrate maintenance

Clean writes dirty data toward the defined point; invalidate removes residency; flush terminology varies. Completion must mean the architecture/platform-specified visibility.

Set/way iteration coordinates with refills, victim buffers and new writes. A clean racing a store cannot declare completion while losing the newer data.

### Distinguish ordering and visibility

Architectural fences order specified operations/observers; they may drain write buffers or wait for acknowledgments as required. Cache-line residency alone does not define global visibility.

Document multi-copy atomicity, coherence point and device ordering. These are system contracts, not replacement details.

### Distinguish persistence

A write can be coherent and globally visible yet lost on power failure. Persistence depends on caches, memory controllers, buffers, media and platform-provided flush/drain semantics.

Name persistence domain and failure model. Write-through to a volatile lower cache is not durable.

### Handle reset and errors

Reset cannot discard dirty data if the platform promises preservation; many reset contracts instead abandon volatile cache contents. Specify which resets/power failures apply.

ECC errors on dirty data may make correct writeback impossible, requiring poison/fatal containment. Replacement metadata corruption must not select ineligible state or lose ownership silently.

### Model traffic

Count demand fills, ownership reads, write-through payload/transactions, dirty writeback lines, coherence transfers and maintenance. Report useful versus transferred bytes.

Write amplification depends on locality, line size, masks, eviction frequency and lower granularity. A policy can reduce transactions but increase bytes.

### Model latency and queues

Write-through hit latency may be buffered, but buffer-full stalls and fence drains expose lower latency. Write-back hits are local, while dirty misses pay victim service unless decoupled.

Report average and tails. Rare dirty evictions can dominate high-percentile miss service.

### Model endurance and energy

Nonvolatile lower levels may have write endurance/asymmetry. Coalescing and write-back reduce events but dirty eviction writes full lines; wear leveling is a broader system policy.

Replacement reads/updates metadata each access and affects lower traffic energy. Use measured implementation/workloads.

### Compare policies fairly

Use identical physical traces, geometry, initial state, prefetch/coherence model and write semantics. Preserve random seeds and count final drain consistently.

Evaluate hit/miss, dirty evictions, lower bytes/transactions, latency, throughput, energy, fairness and persistence/ordering constraints—not hit rate alone.

### Verify data independently of quality

A shadow coherent memory model determines correct loads and ordered stores. Any replacement policy must refine it. Separately compare policy decisions to an independent LRU/FIFO/PLRU model.

Assert eligible victim, invalid-first, exact metadata update, dirty preservation, byte merge, buffer capacity/order, request uniqueness, maintenance completion and progress.

### Gather layered evidence

Use directed policy permutations/scans/thrashing, random trace-model differential tests, dirty/partial/full writes, buffer-full/merge/fence cases, refill/writeback errors, coherence/maintenance/reset/ECC races, formal safety/liveness/refinement, SRAM mapping, synthesis/STA/area/power, traffic/counter validation, workloads and errata.

Bind evidence to exact cache/policy configuration, RTL, macros, protocols, memory types, ISA/platform persistence rules, tools/libraries, traces/seeds, hardware and firmware/errata. Policy names alone are insufficient identity.

## Definitions and Notation

- `E_s`: eligible ways in set `s` after locks/transients/partitions.
- `I_s`: invalid eligible ways in `s`.
- `R_s`: replacement metadata/state for set `s`.
- `victim=Policy(R_s,E_s)` when `I_s` is empty.
- `W`: associativity; exact LRU state orders `W` ways.
- `M`: byte-write mask; updated bytes select new data where `M=1`.
- `D`: dirty predicate indicating cache-owned newer data.
- `F`: number of lower-level line fills; `B`: line bytes.
- `WB`: dirty writeback count; line traffic includes `(F+WB)*B` under simple assumptions.
- `WA=bytes_transferred/bytes_useful_written`: write amplification at a named boundary.
- **insertion position:** initial policy priority assigned to an allocated line.
- **victim buffer:** storage owning an evicted line/writeback obligation.
- **visibility point:** observer/boundary at which a write must be observable.
- **persistence domain:** components whose contents survive the declared failure.
- **policy quality:** performance/resource behavior distinct from cache data correctness.

## Mechanisms, Invariants, or Proof Structure

1. **Eligibility obligation:** replacement considers exactly the validly replaceable way set.
2. **Invalid-first obligation:** invalid eligible capacity is used before a valid victim.
3. **Policy obligation:** full-set victim and state transitions match exact algorithm/insertion/update events.
4. **Single-update obligation:** replay/speculation/coherence cannot update policy more times than specified.
5. **Victim obligation:** dirty tag/index/data/mask remain coherent until writeback ownership transfers/completes.
6. **Uniqueness obligation:** cache, victim, refill and write buffers preserve one coherent newest block ownership.
7. **Byte obligation:** writes update exactly enabled bytes and loads merge/forward newest ordered bytes.
8. **Buffer obligation:** accepted writes/evictions never exceed capacity and remain ordered/matched.
9. **Allocation obligation:** write misses follow allocate/bypass/full-line/partial rules per memory type.
10. **Protocol obligation:** lower requests occur once, hold stable, match responses/errors and obey retry safety.
11. **Coherence/order obligation:** policy, ownership, fences and external agents preserve architectural visibility.
12. **Maintenance/persistence obligation:** clean/flush/drain completion means the documented boundary under the failure model.
13. **Reset/integrity obligation:** dirty/metadata errors and reset follow defined preservation or containment.
14. **Progress obligation:** under lower fairness and buffer service, accepted operations eventually complete/fault.
15. **Evidence obligation:** performance/traffic/endurance claims bind to equal traces, exact policies and system identity.

## Alternatives and Trade-Offs

1. **LRU versus FIFO:** LRU exploits hits; FIFO has simpler insertion-age state and different cyclic behavior.
2. **Exact versus pseudo-LRU:** exact recency improves fidelity; approximation reduces state/update timing.
3. **Recency versus random:** recency uses locality; random avoids some deterministic adversarial patterns.
4. **MRU versus low-priority insertion:** MRU favors immediate reuse; low insertion protects residents from scans.
5. **Allocate versus bypass:** allocation captures reuse; bypass avoids pollution/traffic for low-reuse streams.
6. **Write-through versus write-back:** through keeps a lower propagation obligation per write; back amortizes writes with dirty complexity.
7. **Write-allocate versus no-allocate:** allocation supports repeated/partial reuse; bypass avoids read ownership for streams.
8. **Write buffer versus synchronous propagation:** buffers hide latency; synchronous completion simplifies pending state and stalls.
9. **Combining versus immediate writes:** combining reduces transactions; immediate propagation improves visibility latency.
10. **Victim buffer versus blocking eviction:** buffer overlaps refill/writeback; blocking reduces ownership/race state.
11. **Full-line versus subline dirty:** one dirty bit is compact; subline state can reduce writeback and adds metadata/protocol cases.
12. **Demand versus prefetch training:** demand reflects proven use; prefetch training can improve or pollute policy.
13. **Shared versus partitioned replacement:** sharing maximizes capacity; partitioning improves isolation/QoS.
14. **Volatile visibility versus persistence:** coherence completion is cheaper; durability needs platform drains/media guarantees.
15. **Traffic reduction versus hit-path cost:** richer policy/buffering can save lower work while increasing timing/energy/verification.

## Failure Modes and Misconceptions

1. “Replacement runs on every miss.” Invalid and same-block transient checks precede valid victim choice.
2. “Any way in the set is eligible.” Locks, partitions, transient/coherence state constrain victims.
3. “LRU is always optimal.” Future-aware optimal is unattainable online; workloads vary.
4. “FIFO updates on hits.” FIFO normally retains insertion order.
5. “Tree-PLRU is LRU.” It approximates recency.
6. “Random replacement is stateless.” It needs a source/seed and unbiased selection.
7. “Policy update timing does not matter.” Speculative/replayed events can change victims.
8. “New fills always enter MRU.” Insertion policy may deliberately choose lower priority.
9. “A worse policy can corrupt data.” Quality and correctness should be independent.
10. “Incoming tag identifies dirty victim.” Stored victim identity is required.
11. “A full victim buffer can accept another eviction.” Backpressure must prevent overflow/loss.
12. “Write-through means no cache update.” Hits normally update the cached copy too.
13. “Write-through is instantly visible everywhere.” Buffering/coherence/ordering determine observation.
14. “Write-back means memory is correct only after eviction.” The coherent abstraction includes the owned dirty copy.
15. “Dirty means durable.” It only marks newer cached data.
16. “Write-allocate always reads a line.” Full-line ownership writes may avoid old data under protocol.
17. “No-write-allocate never checks cache state.” Existing/transient copies still matter.
18. “Partial stores overwrite the whole line.” Masks preserve untouched bytes.
19. “Combining any same-line writes is safe.” Order, attributes, atomics and device semantics constrain merging.
20. “A younger load can read lower memory directly.” It may need buffered-store forwarding.
21. “Write-through eliminates coherence.” Other cached copies still require protocol.
22. “Cache flush means persistence.” Exact architecture/platform persistence domain governs.
23. “Final dirty drain can be omitted from comparison.” It changes traffic/completion semantics.
24. “Fewer lower transactions means fewer bytes.” Coalescing/full-line writes can change granularity.
25. “Hit rate chooses policy.” Traffic, latency, energy, fairness and durability also matter.
26. “One trace/seed validates replacement.” Phase/adversarial patterns and initialization differ.

## Worked Examples

### Example 1

With three resident ways ordered `[A,B,C]` LRU-to-MRU, a hit on A changes exact LRU to `[B,C,A]`; FIFO order remains `[A,B,C]`.

### Example 2

One invalid eligible way exists alongside dirty residents. Invalid-first allocates it without eviction/writeback, then inserts per policy.

### Example 3

A prefetch fills at low replacement priority. If unused, it leaves quickly instead of evicting repeatedly reused demand lines.

### Example 4

A dirty victim buffer captures tag/set/data before the cache way installs incoming metadata; lower writeback uses captured identity.

### Example 5

A write-through buffer fills during lower backpressure. The next store stalls before cache acknowledgment so no propagation obligation is lost.

### Example 6

Ten stores update one write-back line; one fill and one eventual dirty writeback can replace ten lower payload writes under stated granularity.

### Example 7

A partial write-allocate miss refills untouched bytes, merges enabled bytes and marks the line dirty only after correct ownership/data arrival.

### Example 8

A load overlaps an older buffered partial store. Byte-wise forwarding supplies updated lanes and cache/lower data supplies the rest.

### Example 9

A cache clean reaches coherent memory but not the platform persistence domain. A separate documented drain is required before durability claim.

### Example 10

This deterministic model compares LRU/FIFO hits, dirty write-back traffic and repeated-store policy traffic.

<!-- bijux-verify: {"id":"cache-policy-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"replacement_accesses=9 lru_hits=2 fifo_hits=1\nwrite_accesses=6 hits=1 misses=5 dirty_writebacks=3 line_traffic_bytes=512\nstreaming_stores=10000 unique_lines=100 wt_nwa_bytes=80000 wb_wa_bytes=12800 reduction_pct=84.00\n"}} -->
```python
def replacement_hits(trace, capacity, refresh_on_hit):
    order = []
    hits = 0
    for block in trace:
        if block in order:
            hits += 1
            if refresh_on_hit:
                order = [resident for resident in order if resident != block]
                order.append(block)
        else:
            if len(order) == capacity:
                order.pop(0)
            order.append(block)
    return hits

replacement_trace = [0, 1, 2, 0, 3, 0, 1, 2, 3]
lru_hits = replacement_hits(replacement_trace, 3, True)
fifo_hits = replacement_hits(replacement_trace, 3, False)

write_trace = [("W", 0), ("W", 1), ("R", 0), ("W", 2), ("R", 1), ("W", 3)]
cache = []
dirty = []
hits = misses = writebacks = 0
for operation, block in write_trace:
    if block in cache:
        hits += 1
        index = cache.index(block)
        cache.pop(index)
        was_dirty = dirty.pop(index)
    else:
        misses += 1
        was_dirty = False
        if len(cache) == 2:
            cache.pop(0)
            if dirty.pop(0):
                writebacks += 1
    cache.append(block)
    dirty.append(was_dirty or operation == "W")

line_bytes = 64
line_traffic = (misses + writebacks) * line_bytes
stores = 10_000
unique_lines = 100
store_bytes = 8
wt_nwa_bytes = stores * store_bytes
wb_wa_bytes = unique_lines * line_bytes * 2

print(f"replacement_accesses={len(replacement_trace)} lru_hits={lru_hits} fifo_hits={fifo_hits}")
print(f"write_accesses={len(write_trace)} hits={hits} misses={misses} dirty_writebacks={writebacks} line_traffic_bytes={line_traffic}")
print(f"streaming_stores={stores} unique_lines={unique_lines} wt_nwa_bytes={wt_nwa_bytes} wb_wa_bytes={wb_wa_bytes} reduction_pct={100 * (wt_nwa_bytes - wb_wa_bytes) / wt_nwa_bytes:.2f}")
```

The trace and byte-granularity assumptions are invented; final dirty drain in the mixed trace is excluded and must be stated in comparisons.

## Cross-Program Connections

- **Algorithms:** online replacement approximates uncertain future reuse.
- **Data Structures:** recency lists, trees, counters and buffers encode policy/ownership.
- **Operating Systems:** cache maintenance, memory types and persistence APIs define visibility boundaries.
- **Concurrent Systems:** write buffers, coherence and probes require ordering/backpressure.
- **Storage Engineering:** persistence domains, drains, amplification and endurance extend beyond volatile cache policy.
- **Security Engineering:** shared replacement and buffers can leak timing or cross partitions.
- **Formal Methods:** shadow memory, eligibility, ownership and exactly-once protocol properties establish correctness.
- **Performance Engineering:** hits, dirty evictions, bytes, queues, energy and tails determine policy value.

## References

1. RISC-V International, [Cache Management Operations](https://docs.riscv.org/reference/isa/unpriv/cmo.html), current cache clean/invalidate/flush and ordering semantics; retrieved 2026-09-04.
2. lowRISC, [Ibex Instruction Cache](https://ibex-core.readthedocs.io/en/latest/03_reference/icache.html), current replacement/refill/error behavior in an open multi-way cache; retrieved 2026-09-04.
3. OpenTitan, [RV Core Ibex](https://opentitan.org/book/hw/ip/rv_core_ibex/), current cache configuration, security and verification context; retrieved 2026-09-04.
4. gem5, [Classic Caches](https://www.gem5.org/documentation/general_docs/memory_system/classic_caches/), current cache, write buffer and memory-port modeling; retrieved 2026-09-04.
5. gem5, [Replacement Policies](https://www.gem5.org/documentation/general_docs/memory_system/replacement_policies/), current LRU, random, RRIP-family and policy framework documentation; retrieved 2026-09-04.
6. Valgrind, [Cachegrind Manual](https://valgrind.org/docs/manual/cg-manual.html), current cache-simulation and event interpretation; retrieved 2026-09-04.
7. Intel, [Intel 64 and IA-32 Architectures Software Developer Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), current memory type, ordering and cache-management architectural context; retrieved 2026-09-04.
8. Sarah L. Harris and David Money Harris, [Digital Design and Computer Architecture: RISC-V Edition Resources](https://pages.hmc.edu/harris/ddca/ddcarv.html), replacement/write-policy teaching resources; retrieved 2026-09-04.

## Exercises

### Exercise 1

Trace one four-way set under exact LRU, FIFO and tree-PLRU for a scan-plus-reuse sequence, including invalid initialization and insertion position.

### Exercise 2

Design write-through and write-back state transitions for hit/miss, partial store, dirty victim, buffer full and lower error.

### Exercise 3

Specify a write-combining buffer supporting byte masks, load forwarding, fences, atomics and device exclusions.

### Exercise 4

Extend the executable model to include final dirty drain and compare payload bytes, line bytes and transaction counts separately.

### Exercise 5

Write a verification/measurement plan for choosing a replacement/write policy for a coherent cache backed by persistent memory.

## Answers to the Exercises

### Answer 1

Create a table of valid ways, block identities and policy bits/order after each access. Allocate invalid ways first. Exact LRU moves qualified hits to MRU; FIFO leaves hit order unchanged; tree-PLRU follows/update direction bits and can diverge from exact victim.

State whether prefetch/demand fills enter MRU or low priority and whether killed accesses train. Verify every chosen victim is eligible; policy differences may change misses but never returned data.

### Answer 2

Write-through hit merges enabled bytes locally and reserves/enqueues one ordered lower write before acknowledgment; full buffer stalls. Write-back hit merges and marks dirty. On write-allocate miss, preserve dirty victim, acquire/refill old bytes as needed, merge mask and publish; no-allocate bypasses without duplicate cached ownership.

Errors preserve/retry ownership or raise the specified fault—never drop a dirty obligation. State transitions hold lower payload until acceptance, match response once and distinguish write-through buffered completion, coherence visibility and persistence.

### Answer 3

Each entry carries aligned block/subblock address, valid byte mask/data, age/order, memory type, privilege/context and acceptance state. Merge only compatible normal-memory writes without crossing fence/atomic/release/device ordering; for overlapping lanes newest older data wins.

Loads search older entries and merge bytes by age before cache/lower data. Fence waits for required entries/acknowledgments; atomics serialize ownership; device accesses bypass combining. Assert capacity, no loss/duplicate, byte correctness, order and progress under lower fairness.

### Answer 4

At measurement end, write every remaining dirty line once if the completion definition requires lower visibility; add those line bytes/transactions to prior fills/writebacks. Report useful store payload separately from cache-line ownership/fill/writeback and protocol transaction count.

Compare policies under identical final state requirement. Excluding drain may be appropriate for a steady interval with carried cache state, but then state it and avoid claiming completed persistence/traffic for the entire task.

### Answer 5

Use identical coherent physical traces/workloads across candidate policies, including scans, reuse, sharing, writes/masks, prefetch, maintenance and failure/restart. Verify replacement model/seed, invalid/eligibility, unique ownership, dirty victim, buffer order/forwarding, coherence races, lower errors, ECC and reset/power-fail persistence semantics against shadow coherent/persistent models.

Measure hits/misses, dirty evictions, useful/transferred bytes, transactions, stalls/tails, energy and media writes/endurance; run synthesis/STA/area/power and formal safety/liveness/refinement. Bind exact cache/protocol/persistence domain, RTL/macros, ISA/OS/firmware, tools, traces/seeds, hardware and errata. Independent persistence/safety certification is not claimed.
