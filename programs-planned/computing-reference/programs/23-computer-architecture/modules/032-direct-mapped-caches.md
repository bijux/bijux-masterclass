---
module_id: CA-032
program: Computer Architecture
level: 1
module_number: 32
title: Direct-Mapped Caches
status: complete
last_verified: 2026-09-04
---

# Direct-Mapped Caches

## One-Page Review

### Governing question

How does a direct-mapped cache translate each address into exactly one candidate line, determine hit or miss safely, move and replace whole blocks, and expose the performance and conflict behavior implied by that simple mapping?

### Essential definitions

- A **cache** holds copies of blocks from a backing address space to reduce average access cost.
- A **cache block/line** is the allocation, transfer and tag granularity.
- A **direct-mapped cache** provides exactly one candidate cache line for each memory block.
- The **block offset** selects a byte/word within a cache line.
- The **index** selects one cache set/line in a direct-mapped organization.
- The **tag** distinguishes backing-memory blocks that share an index.
- A **valid bit** states whether a cache line's tag/data represent an allocated block.
- A **hit** requires valid and matching tag plus operation/permission/state conditions.
- A **miss** occurs when the indexed line does not contain the requested valid block.
- A **refill** obtains the requested block from a lower level and installs it.
- **eviction** removes the indexed resident block to make room for another.
- A **dirty bit** marks write-back data newer than the lower level.
- A **compulsory miss** is the first reference to a block in the chosen trace/reference model.
- A **conflict miss** occurs because mapping forces blocks to compete despite sufficient fully associative capacity.
- A **critical-word-first/early-restart** policy returns the demanded portion before the entire refill completes under a correctness contract.

### Central model, mechanism, or theorem

For byte address width `A`, line size `B=2^b` bytes and `S=2^s` direct-mapped lines, block number is `floor(addr/B)`, `offset=addr mod B`, `index=block_number mod S`, and `tag=floor(block_number/S)`. Equivalently, address bits partition as `[tag A-s-b | index s | offset b]` when sizes are powers of two. A read hits exactly when `valid[index] && stored_tag[index]==tag`; returned bytes are selected by offset. On a miss, any dirty victim is handled first, the correct lower block is fetched, and tag/data/state become visible atomically under the refill protocol.

### Critical invariants

- Geometry powers, address units and capacity definition yield exact offset/index/tag widths.
- Each address maps to one and only one candidate line.
- Invalid lines never hit, regardless of stale tag/data bits.
- Tag comparison uses all required physical/address-space/context bits.
- Returned data comes from the matching valid block and correct byte lanes.
- A miss cannot expose partially refilled bytes as valid beyond the permitted beat-valid policy.
- Dirty victims are written back with their reconstructed original block address before replacement.
- Refill request/response identity survives stalls, errors, redirects and reset.
- Simultaneous CPU, refill, eviction and maintenance operations have defined priority/port behavior.
- Performance classifications and AMAT use exact trace, denominator, lower-level and overlap assumptions.

### Common failures

Common failures include using word rather than byte offsets, deriving index bits from total capacity instead of line count, omitting the valid bit, comparing a virtual tag with physical data identity, returning stale data during refill, reconstructing a dirty victim address from the incoming tag, treating every first miss as capacity, calling alternating same-index blocks a small-capacity problem, assuming hit rate alone determines speed, adding miss penalty twice, ignoring write allocation/writeback traffic, reissuing a refill on a stalled request, accepting a late response into a new miss, and assuming inferred arrays provide the needed read/write collision behavior.

### Compact example

A 4 KiB direct-mapped cache with 64-byte lines and 32-bit byte addresses has 64 lines: 6 offset bits, 6 index bits and 20 tag bits. Address `0x1234` maps to tag 1, index 8, offset 52; `0x2234` maps to tag 2, the same index and offset, so the blocks conflict. In a four-line/16-byte teaching cache, the trace `0,4,64,0,64,16,20,80,16` yields 2 hits and 7 misses: four compulsory and three conflict misses relative to a four-line fully associative reference. At 1 ns hit time and 50 ns additional miss penalty, simple AMAT is 39.89 ns.

### Connections

Direct mapping connects address bit decomposition, SRAM/memory inference, locality, write policy, miss handling, physical addressing/translation, cache coherence, timing, trace simulation and later associativity/replacement design.

## Governing Question

A direct-mapped cache answers lookup with one indexed tag/data candidate. That simplicity can provide low hit latency, but any two blocks with the same index continually replace one another.

Correctness depends on more than the mapping equation. Validity, refill atomicity, dirty eviction, lower-level protocol, faults and maintenance must preserve the illusion of one coherent backing memory under the architecture's ordering rules.

## Why This Matters

Direct mapping makes cache geometry and misses concrete. It exposes how capacity, line size and address bits create hardware structures and why conflict behavior can dominate an otherwise small working set.

Its short lookup path remains relevant in instruction caches, small first-level structures, scratch-adjacent designs and predictor-like tables. More associativity is not free; it adds comparisons, selection and replacement state.

Trace arithmetic can verify mapping, but performance requires implementation evidence. Hit time, miss overlap, write traffic, prefetch and physical memory macros influence elapsed time.

## Prerequisites and Retrieval

Before studying this module, be able to:

- convert byte addresses among binary, hexadecimal and integer forms;
- reason about powers of two, modulo and integer division;
- distinguish capacity, line size, latency and bandwidth;
- explain temporal/spatial locality and AMAT assumptions;
- trace valid/ready request-response state.

Retrieve exact address width and whether lookup uses virtual, physical or translated bits; cache data capacity versus total storage; line size, line count and sectoring; tag/context/protection/coherence fields; valid/dirty/ECC/parity; read/write ports and latency; hit pipeline and byte/word selection; allocation/write policy; miss-status entries; refill beat order and critical-word rules; victim writeback address/data; lower-level request/response IDs/errors/retry; uncached/device regions; aliases/homonyms; maintenance/fence/flush/invalidate; coherence/DMA; reset/scrub; arbitration and clock gating; synthesis/STA/area/power; traces/counters; tests/formal properties; simulator/reference model; hardware/errata; and exact RTL/configuration/memory/tool/library/revision identities.

## Learning Objectives

After completing this module, you should be able to:

1. derive line count and offset/index/tag widths from cache geometry;
2. map byte addresses to block, index, tag and offset;
3. trace valid/tag/data state through hits, misses, evictions and refills;
4. distinguish compulsory, capacity and direct-mapping conflict misses;
5. reconstruct dirty victim addresses correctly;
6. specify refill validity, errors, stalls and response identity;
7. integrate write, maintenance, translation and coherence boundaries;
8. compute metadata overhead, hit rate, traffic and simple AMAT;
9. verify mapping and cache data refinement against backing memory;
10. decide when direct mapping's latency/area advantages outweigh conflicts.

## Core Exposition

### Define capacity precisely

Cache data capacity is usually `number_of_lines * bytes_per_line`. Total array/storage area also includes tags, valid/dirty/coherence bits, ECC, replacement/miss state and unused physical macro bits.

State whether advertised size excludes metadata. Geometry arithmetic commonly uses data capacity, while area/power uses realized total implementation.

### Use byte addresses

Most ISAs expose byte addresses. A 64-byte line therefore uses six low offset bits even if the CPU loads 32- or 64-bit words.

Word selection and byte enables are derived within the line. Mixing word-address and byte-address formulas shifts index/tag boundaries incorrectly.

### Derive line count

For data capacity `C` and line size `B`, direct-mapped line/set count is `S=C/B`, assuming exact divisibility. If `S` is a power of two, `s=log2(S)` address bits select the line.

Non-power-of-two modulo indexing is possible but requires different logic; do not apply bit-slice formulas automatically.

### Split the address

Low `b=log2(B)` bits are offset. The next `s=log2(S)` bits are index. Remaining required identity bits form the tag.

For physical caches, tag and sometimes index derive from physical addresses. Virtually indexed/physically tagged designs constrain index/page-offset relationships and synonym handling.

### Compute block number first

An implementation-neutral method is `block=addr//B`, `index=block%S`, `tag=block//S`, `offset=addr%B`. It avoids manual bit-position errors and generalizes modulo indexing.

Check reconstruction: `addr = ((tag*S + index)*B + offset)` within address width.

### Store tag, data and state

Each line stores a tag and `B` data bytes plus validity. A write-back design also tracks dirty state; coherence/integrity may add state/ECC.

Tag/data/state must correspond to one backing block. Split-array writes need atomic visibility or transient state preventing mismatched hits.

### Perform a read lookup

Index reads the candidate tag/data. Compare requested tag and require valid plus any coherence/permission/state predicate. On hit, select requested byte lanes and apply sign/zero extension outside or within the cache pipeline.

Data array access can occur in parallel with tag comparison, with the result gated by hit. This saves time but consumes energy.

### Never omit validity

After reset, tag/data bits may coincidentally equal a request. Valid false prevents a false hit. Reset can clear valid state without clearing the full data array when security/integrity policy permits.

Validity may be per line or sector/beat. Define exactly which bytes can be served during partial refill.

### Trace same-index conflicts

Blocks separated by `S*B` bytes share an index because their block numbers differ by `S`. They carry different tags and replace one another.

Alternating between two such blocks can miss every time even when the useful footprint is only two lines and total cache has many lines.

### Classify misses against a reference

Compulsory is first touch in the trace/reference history. Compare direct mapping with a fully associative cache of equal line capacity and replacement policy: additional direct misses that the reference hits are conflicts.

Misses in both after first touch can be capacity under the chosen model. Prefetch/coherence/invalidation complicate the classic classification; record the classifier.

### Begin a miss transaction

Capture requested block address, operation, byte enables/data, privilege/attributes, destination and transaction identity. Mark the line or miss entry transient so ordinary lookup cannot hit stale/partial contents.

If only one miss may be outstanding, backpressure later misses. Nonblocking designs need entries/tags and are covered more deeply later.

### Select and preserve the victim

The indexed resident is the only victim. If valid and dirty, reconstruct its lower address from stored victim tag plus index and zero offset—not the incoming tag.

Hold victim data stable through writeback acceptance/completion under the lower protocol before overwriting it, unless a separate victim buffer owns it.

### Refill the requested block

Issue a lower-level aligned block request. Match each response beat/error to the captured miss. Write bytes and integrity state into the intended line.

Publish requested tag/valid only when the policy guarantees all served bytes are correct. A refill error leaves the line invalid or restored under a documented rule and reports the fault precisely.

### Support critical-word-first safely

If lower memory returns the demanded word first, the CPU may restart before all beats arrive. Track per-sector/beat validity or prohibit accesses to incomplete portions.

The miss entry remains live through final beat/error. A second request to the same block needs merge/hold behavior, not a blind hit on partial data.

### Define write-hit policy

Write-through updates cache and lower level; write-back updates cache and marks dirty. Both require byte-mask, ordering, error and buffering rules.

Same-cycle tag/data/write interactions follow physical memory port semantics. Add forwarding/bypass if the selected macro returns old data on read-during-write.

### Define write-miss allocation

Write-allocate fetches/owns the line then updates it. No-write-allocate sends the write lower without installing, often paired with write-through/streaming behavior.

Partial stores need merge with existing/refilled bytes unless lower byte writes avoid allocation. Device/uncached regions follow separate ordering/side-effect rules.

### Handle instruction caches

Instruction caches are often read-mostly and need no dirty data, but self-modifying code, executable mapping changes, DMA and instruction-cache maintenance require explicit synchronization.

Wrong-path fetches can allocate lines under policy. They cannot create architectural instruction effects, while security/performance consequences need separate analysis.

### Handle translation and aliases

A physically tagged cache must wait for enough translation to compare tag. Virtually indexed access may start earlier if index bits lie within unchanged page offset.

Synonyms are distinct virtual addresses for one physical block; homonyms reuse virtual address across address spaces. ASIDs/tags, page coloring or physical identity prevent stale duplicates.

### Handle coherence and DMA

Shared coherent caches add state and snoop/probe behavior. Direct mapping still selects a line, but a coherence invalidation can turn a would-be hit into a miss.

Noncoherent DMA requires software/platform clean/invalidate rules. Cache correctness is system-wide, not only CPU lookup logic.

### Handle maintenance operations

Invalidate clears validity; clean writes dirty data lower; flush commonly combines operations but terminology is architecture-specific. Address/range/all-cache commands need exact iteration and completion rules.

Maintenance races with lookup/refill/writeback need serialization/arbitration. Fence completion must reflect lower-level visibility required by the ISA/platform.

### Handle reset and integrity

Reset invalidates resident/transient/miss state and follows outstanding-request drain/tag rules. Security may require data scrubbing beyond functional invalidation.

Tag/data ECC or parity errors must not return corrupt data as a hit. Define correction, invalidate/refetch, precise exception or fatal containment based on trust and architecture.

### Model timing

Hit path includes index generation, array access, tag compare, valid/state check, way—trivial here—data selection and output capture. Direct mapping avoids multi-way comparison/muxing.

Large arrays, routing, ECC and translation can still dominate. Use mapped memory and physical STA rather than inferring speed from one candidate.

### Model metadata overhead

Raw tag-state overhead per line includes tag width plus valid/dirty/coherence/ECC. Divide total metadata bits by data bits for a logical ratio; physical macros/decoders/routing add more.

Line size trades metadata ratio against overfetch and miss penalty. Larger is not automatically better.

### Model AMAT and traffic

A simple blocking model is `hit_time + miss_rate*additional_miss_penalty`. If miss latency is already end-to-end, use exclusive outcome weighting instead.

Include dirty writebacks, write allocation and refill bytes in traffic. Nonblocking overlap needs queue/MLP models beyond serial AMAT.

### Simulate address traces

A small reference simulator tracks valid/tag/data identity per line and classifies accesses. Use independent code from RTL and include byte-crossing, writes, resets and errors as the model matures.

Trace inputs must specify virtual/physical addresses, operation/size and prefetch/coherence events consistent with the claim.

### Verify refinement

Maintain a shadow backing memory. On a cache hit, returned data must equal the shadow value after all architecturally ordered writes. Dirty cache state represents newer shadow-visible pending data under the write-back abstraction.

Assert mapping, hit qualification, no stale/partial hit, victim-address reconstruction, request uniqueness, response matching, precise error and maintenance completion.

### Gather layered evidence

Use geometry generators, directed same-index traces, compulsory/capacity/conflict patterns, random reference-model comparison, writes/masks, refill stalls/errors/beats, reset/maintenance/coherence/DMA races, integrity injection, formal safety/liveness/refinement, synthesis/STA/area/power, counters/traces, workloads and errata.

Bind evidence to exact address/cache/memory configuration, RTL, macros, lower protocol, ISA/OS maintenance, tools/libraries, traces/seeds, hardware and firmware/errata. One geometry's proof does not cover another automatically.

## Definitions and Notation

- `A`: number of address bits used for cache identity.
- `C`: cache data capacity in bytes.
- `B=2^b`: bytes per cache line and offset-bit count `b`.
- `S=C/B=2^s`: direct-mapped line/set count and index-bit count `s`.
- `block=addr//B`: backing-memory block number.
- `offset=addr%B`; `index=block%S`; `tag=block//S`.
- `valid[i]`, `tag_array[i]`, `data[i]`: state of indexed line `i`.
- `hit=valid[index] && tag_array[index]==tag` plus required state checks.
- `m`: miss rate under a stated access denominator.
- `AMAT=T_hit + m*P_miss`: simple serial model with additional miss penalty.
- **victim:** resident line displaced by the incoming block.
- **transient state:** line/miss state not yet eligible as an ordinary complete hit.
- **sector validity:** valid bits for independently usable portions of a line.
- **alias:** multiple names/addresses that can refer to the same underlying data identity.
- **reference cache:** comparison model used to classify mapping/capacity behavior.

## Mechanisms, Invariants, or Proof Structure

1. **Geometry obligation:** capacity, line count and address split are exact for every supported configuration.
2. **Mapping obligation:** each address maps to exactly one index and reconstructs from tag/index/offset.
3. **Hit obligation:** only valid, full-identity, permitted-state matches return data.
4. **Data obligation:** returned/updated byte lanes equal the addressed coherent backing-memory value.
5. **Invalid/transient obligation:** reset, stale and partially refilled state cannot falsely hit.
6. **Victim obligation:** dirty eviction uses stored victim tag/index and preserves data until accepted safely.
7. **Request obligation:** one logical miss/writeback/maintenance action is accepted at most once.
8. **Response obligation:** refill beats/errors match the live miss and publish validity only as permitted.
9. **Write obligation:** hit/miss, allocation, mask, ordering and dirty/write-through behavior match policy.
10. **Translation/coherence obligation:** physical identity, aliases, permissions and external agents cannot yield stale hits.
11. **Maintenance obligation:** clean/invalidate/fence operations complete with required lower-level visibility.
12. **Reset/integrity obligation:** outstanding and corrupt state enters defined safe recovery/containment.
13. **Progress obligation:** under lower-level fairness, every accepted access completes, faults or is safely cancelled.
14. **Timing obligation:** mapped tag/data/state/selection paths meet setup, hold and interface constraints.
15. **Evidence obligation:** miss classification and performance bind to exact traces, geometry, policies and hardware.

## Alternatives and Trade-Offs

1. **Direct-mapped versus associative:** one candidate shortens lookup; multiple ways reduce conflicts at comparison/selection cost.
2. **Small versus large lines:** small lines reduce overfetch; large lines exploit spatial reuse and lower tag overhead.
3. **Physical versus virtual indexing:** physical identity is simple; virtual indexing starts early with synonym constraints.
4. **Parallel versus serial tag/data access:** parallel is fast and energy-hungry; serial gates data after tag with extra latency.
5. **Blocking versus nonblocking:** one miss is simple; multiple outstanding misses improve overlap with entries/tags complexity.
6. **Whole-line versus sectored validity:** whole-line state is compact; sectors support early restart/partial fills.
7. **Critical-word-first versus full refill:** early word reduces exposed latency; full refill simplifies availability.
8. **Write-through versus write-back:** write-through simplifies lower freshness; write-back saves traffic with dirty eviction.
9. **Write-allocate versus no-allocate:** allocation exploits reuse; bypass avoids line fill for streams.
10. **Victim buffer versus direct writeback:** buffering decouples replacement; direct sequence reduces state and stalls longer.
11. **Reset invalidation versus scrubbing:** validity clear is fast; scrubbing addresses confidentiality/integrity needs.
12. **Parity versus ECC:** parity detects cheaply; ECC can correct at bit/latency/area cost.
13. **Prefetch allocation versus demand-only:** prefetch hides latency; it can evict direct-mapped demand lines.
14. **More capacity versus different mapping:** capacity reduces footprint pressure; remapping/associativity targets conflicts.
15. **Low hit latency versus hit rate:** direct mapping may win instruction time despite more misses, or lose under thrashing.

## Failure Modes and Misconceptions

1. “Direct-mapped means one cache line total.” It means one candidate line per memory block.
2. “Capacity equals line count.” Capacity is line count times bytes per line.
3. “Offset bits select a word only.” Byte-addressed caches include byte position.
4. “Index bits are log2(capacity).” They are log2(line count) for power-of-two geometry.
5. “Tag is whatever bits remain in a diagram.” Address identity/context/translation determine required tag.
6. “Matching tag proves a hit.” Valid and state/permission conditions also matter.
7. “Data arrays reset to zero.” Functional invalidity can leave arbitrary bits.
8. “Stale invalid data cannot hurt.” It hurts if any effect forgets valid gating.
9. “Two blocks fit, so they cannot thrash.” Same-index blocks replace each other.
10. “Every repeated miss is capacity.” A fully associative equal-capacity reference distinguishes conflicts.
11. “First access always means compulsory.” Prefetch/prior history and classifier scope matter.
12. “Incoming tag reconstructs the victim address.” The stored victim tag is required.
13. “Refill tag may be made valid immediately.” Partial data can then be exposed.
14. “Critical word means the line is complete.” Remaining beats/errors still need transient tracking.
15. “A second request during refill is a hit.” It needs merge/hold/per-sector validity.
16. “Write-back reduces all traffic.” Dirty evictions and ownership reads remain.
17. “Write-through needs no buffer.” Lower latency/backpressure can stall writes.
18. “No-write-allocate means ignore ordering.” Bypassed writes still follow architecture/device rules.
19. “Virtual address bits always identify a line safely.” Synonyms/homonyms and page offsets constrain use.
20. “Instruction cache never changes.” Self-modifying code/DMA/maintenance require synchronization.
21. “Reset cancels refills.” The lower protocol governs accepted requests.
22. “ECC correction is invisible.” Timing, logging, poisoning and repeated faults need policy.
23. “Higher hit rate guarantees faster time.” Hit path, penalty and overlap also matter.
24. “AMAT predicts nonblocking throughput.” It omits MLP/queues/bandwidth unless extended.
25. “Simulator agreement proves physical feasibility.” SRAM ports/timing/power need implementation evidence.
26. “One trace proves cache quality.” Workloads, mappings and states vary.

## Worked Examples

### Example 1

A 4 KiB/64-byte direct cache has 64 lines; a 32-bit byte address partitions into 20 tag, 6 index and 6 offset bits.

### Example 2

Addresses `0x1234` and `0x2234` have the same index 8/offset 52 but tags 1/2, so alternating them evicts the prior line.

### Example 3

After reset a stale tag happens to match, but valid false forces a miss and prevents stale data return.

### Example 4

A dirty victim's writeback address concatenates stored victim tag, current index and zero offset before the incoming tag overwrites metadata.

### Example 5

A four-beat refill returns the demanded beat first. Per-beat validity allows early restart; the miss entry persists through all beats/error.

### Example 6

A byte store hit updates only enabled lanes and sets dirty. Same-cycle read behavior follows explicit bypass/macro collision rules.

### Example 7

A write miss to normal cached memory allocates/refills, merges the byte mask and marks dirty; an uncached device write bypasses under stronger ordering.

### Example 8

Two virtual addresses synonymously map one physical line. Physical tags and index/page constraints prevent incoherent duplicate hits.

### Example 9

An invalidate arriving during refill either cancels publication or waits/serializes; priority prevents the refill from resurrecting invalidated state.

### Example 10

This deterministic model derives geometry, decodes addresses, simulates conflicts, classifies misses and computes metadata/AMAT.

<!-- bijux-verify: {"id":"direct-mapped-cache-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"geometry_sets=64 offset_bits=6 index_bits=6 tag_bits=20\naddress=0x00001234 tag=0x00001 index=8 offset=52\naddress=0x00002234 tag=0x00002 index=8 offset=52\naccesses=9 hits=2 misses=7 hit_rate=0.222\nmiss_classes compulsory=4 conflict=3 capacity=0\namat_ns=39.89 metadata_bits=1408 overhead_pct=4.30\n"}} -->
```python
from math import log2

address_bits = 32
capacity_bytes = 4096
line_bytes = 64
sets = capacity_bytes // line_bytes
offset_bits = int(log2(line_bytes))
index_bits = int(log2(sets))
tag_bits = address_bits - offset_bits - index_bits

def decode(address, lines=sets, block_bytes=line_bytes):
    block = address // block_bytes
    return block // lines, block % lines, address % block_bytes

print(f"geometry_sets={sets} offset_bits={offset_bits} index_bits={index_bits} tag_bits={tag_bits}")
for address in (0x1234, 0x2234):
    tag, index, offset = decode(address)
    print(f"address=0x{address:08x} tag=0x{tag:05x} index={index} offset={offset}")

trace = [0, 4, 64, 0, 64, 16, 20, 80, 16]
teaching_lines = 4
teaching_line_bytes = 16
cache = [None] * teaching_lines
seen = set()
hits = compulsory = conflict = capacity = 0

for address in trace:
    block = address // teaching_line_bytes
    index = block % teaching_lines
    tag = block // teaching_lines
    if cache[index] == tag:
        hits += 1
    else:
        if block not in seen:
            compulsory += 1
        else:
            conflict += 1
        cache[index] = tag
    seen.add(block)

misses = len(trace) - hits
miss_rate = misses / len(trace)
metadata_bits = sets * (tag_bits + 1 + 1)
data_bits = capacity_bytes * 8
amat_ns = 1.0 + miss_rate * 50.0
print(f"accesses={len(trace)} hits={hits} misses={misses} hit_rate={hits / len(trace):.3f}")
print(f"miss_classes compulsory={compulsory} conflict={conflict} capacity={capacity}")
print(f"amat_ns={amat_ns:.2f} metadata_bits={metadata_bits} overhead_pct={100 * metadata_bits / data_bits:.2f}")
```

This trace's four unique blocks equal reference capacity, so its three noncompulsory direct misses are conflicts. The timing and dirty metadata are illustrative.

## Cross-Program Connections

- **Digital Logic:** address slices, comparators, valid state, SRAMs and byte muxes implement lookup.
- **Data Structures:** direct mapping is a fixed hash with one slot and destructive collisions.
- **Operating Systems:** translation, aliases, page mapping and maintenance affect cache identity.
- **Concurrent Systems:** refill/writeback/coherence requests require matching and arbitration.
- **Security Engineering:** stale/transient data, aliases and shared-cache effects cross trust boundaries.
- **Formal Methods:** a shadow memory and mapping invariants establish data refinement.
- **Performance Engineering:** trace classes, AMAT, traffic, timing and energy decide value.
- **Systems Engineering:** macros, lower protocols, firmware/OS maintenance and errata jointly govern correctness.

## References

1. RISC-V International, [Cache Management Operations](https://docs.riscv.org/reference/isa/unpriv/cmo.html), current cache-block management, ordering and instruction semantics; retrieved 2026-09-04.
2. lowRISC, [Ibex Instruction Cache](https://ibex-core.readthedocs.io/en/latest/03_reference/icache.html), current open-core cache organization, refill and error behavior; retrieved 2026-09-04.
3. OpenTitan, [RV Core Ibex](https://opentitan.org/book/hw/ip/rv_core_ibex/), current integrated cache configuration, security and verification context; retrieved 2026-09-04.
4. gem5, [Classic Caches](https://www.gem5.org/documentation/general_docs/memory_system/classic_caches/), current cache-model and memory-port documentation; retrieved 2026-09-04.
5. Valgrind, [Cachegrind Manual](https://valgrind.org/docs/manual/cg-manual.html), current trace/simulation and cache-event interpretation; retrieved 2026-09-04.
6. Intel, [Intel 64 and IA-32 Architectures Software Developer Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), current address, memory and cache-management architectural context; retrieved 2026-09-04.
7. Sarah L. Harris and David Money Harris, [Digital Design and Computer Architecture: RISC-V Edition Resources](https://pages.hmc.edu/harris/ddca/ddcarv.html), direct-mapped cache teaching resources; retrieved 2026-09-04.
8. YosysHQ, [Memory Handling](https://yosyshq.readthedocs.io/projects/yosys/en/latest/using_yosys/synthesis/memory.html), current inferred-memory transformation and mapping documentation; retrieved 2026-09-04.

## Exercises

### Exercise 1

Derive geometry and decode addresses for a 16 KiB direct-mapped cache with 32-byte lines and 36-bit physical addresses.

### Exercise 2

Trace a workload alternating blocks separated by one cache capacity, then classify misses against an equal-capacity fully associative LRU reference.

### Exercise 3

Design a blocking refill/writeback FSM supporting write-back, write-allocate, byte masks, lower-level stalls/errors and reset.

### Exercise 4

Extend the executable model with an equal-capacity fully associative LRU simulator so conflict and capacity classification is computed rather than assumed.

### Exercise 5

Write a verification/measurement plan for a configurable direct-mapped cache integrated with translation, maintenance and a non-cancellable lower interface.

## Answers to the Exercises

### Answer 1

`C=16384`, `B=32`, so `S=512`. Offset bits `b=5`; index bits `s=9`; tag bits `36-5-9=22`. For address `a`, compute block `a//32`, index `block%512`, tag `block//512`, offset `a%32`.

Check reconstruction and address-width bounds. State whether 16 KiB is data capacity and whether all 36 physical bits plus context/coherence identity are required.

### Answer 2

Blocks separated by `S` block numbers, or one cache data capacity in bytes, share an index. Alternating A/B gives compulsory misses on first A/B and then direct-mapped misses on each switch.

An equal-capacity fully associative LRU reference holds both if at least two lines and no other footprint pressure, so later misses are conflict. If the trace includes more distinct reuse distance than reference capacity, those misses become capacity under the classifier.

### Answer 3

States capture request, test hit, save dirty victim, issue/await writeback, issue/await refill beats, install, merge pending write, respond or fault. Lower requests hold address/data/mask/tag stable until acceptance and cannot duplicate. Victim address uses stored tag/index.

Keep line transient/invalid until correct complete or sector-valid data. On refill error leave safe state and report precise fault. Reset invalidates CPU-visible/transient entries but retains ownership tags until non-cancellable responses drain. Assert data refinement, stable protocol, one acceptance, matched beats, dirty preservation and liveness under fairness.

### Answer 4

Maintain an MRU-to-LRU list of at most four block numbers. On each access, direct simulator and fully associative simulator run independently. First unseen block is compulsory. A later direct miss paired with associative hit is conflict; a later miss in both is capacity under this LRU reference.

Test duplicate accesses, more than four unique blocks, same-index pairs and long reuse distances. Keep prefetch/coherence absent or model them explicitly; otherwise classic classes become ambiguous.

### Answer 5

Generate geometry assertions for every configuration; directed tests cover address boundaries, aliases/homonyms, invalid/tag matches, dirty victim reconstruction, write masks, read-during-write, beat orders, errors, maintenance races, coherence/DMA and reset with late responses. Compare random operations against independent physical shadow memory and associative classifier.

Prove hit/data validity, no partial/stale hit, request uniqueness, response identity, ordered writes/maintenance, tag-wrap safety and progress under lower fairness. Run CDC/RDC, synthesis/STA/area/power on exact SRAM mappings; validate cache/traffic counters with traces and workloads. Bind ISA/OS maintenance, RTL/config, macros/protocol, tools, seeds, hardware and errata. Internal evidence is not independent certification.
