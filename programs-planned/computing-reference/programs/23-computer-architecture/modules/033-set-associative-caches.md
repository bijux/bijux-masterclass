---
module_id: CA-033
program: Computer Architecture
level: 1
module_number: 33
title: Set-Associative Caches
status: complete
last_verified: 2026-09-04
---

# Set-Associative Caches

## One-Page Review

### Governing question

How does allowing each memory block to occupy one of several ways in an indexed set reduce mapping conflicts while preserving exact address identity, one-hot hit selection, coherent replacement and a hit path whose latency, energy and physical cost remain acceptable?

### Essential definitions

- A **set-associative cache** contains `S` indexed sets with `W` candidate lines, or **ways**, per set.
- **associativity** `W` is the number of candidate resident blocks sharing one index.
- A **way** contains tag, data and per-line state for one possible resident block in each set.
- The **set index** selects one row across all ways.
- A **way hit** is valid/state-qualified equality between the requested tag and one way's stored tag.
- A **hit vector** contains one Boolean match per way and should be one-hot-or-zero in a coherent cache.
- A **way select** chooses the matching way's data on a hit or the allocated victim way on a miss.
- A **replacement policy** chooses a resident way when all candidates are valid and allocation is required.
- **invalid-first** allocation chooses an invalid way before evicting a valid resident.
- **least recently used** (`LRU`) evicts the way whose last access is oldest under an exact recency model.
- **pseudo-LRU** approximates recency with less metadata/update complexity.
- A **fully associative cache** has one set containing all lines; a direct-mapped cache has one way.
- A **conflict miss** is a mapping-caused miss that an equal-capacity fully associative reference would hit.
- **way prediction** speculatively chooses a likely way to reduce access energy/latency, with tag verification and recovery.
- **skewed indexing** maps different ways using different index functions to reduce concentrated conflicts.

### Central model, mechanism, or theorem

For data capacity `C`, line size `B=2^b` and associativity `W`, total lines are `L=C/B` and sets `S=L/W` (requiring integral supported geometry). For power-of-two `S=2^s`, address maps to one set: `block=addr//B`, `index=block mod S`, `tag=block//S`, `offset=addr mod B`. All `W` ways at `index` are candidates. A hit requires exactly one qualified way match; data comes only from that way. On an allocating miss, choose invalid first, else a replacement victim; preserve any dirty victim, install the full identified block, update metadata, and never expose duplicate live tags within a set.

### Critical invariants

- Capacity, line size, way count and set count produce exact offset/index/tag geometry.
- Every block maps to exactly one set and at most one valid way within that set.
- The qualified hit vector is one-hot-or-zero; duplicate tags are detected/prevented.
- Returned/updated data and state come from the selected matching way only.
- Invalid-first allocation never evicts a valid way while a compatible invalid way exists.
- Replacement chooses only an eligible way and updates policy state on precisely defined events.
- Dirty victim tag/index/data remain coherent through writeback before overwrite.
- Refill/transient state cannot collide with lookup or install a duplicate block.
- Maintenance, coherence, reset and integrity operations act on the correct way set.
- Associativity performance comparisons include hit time, energy, metadata, miss traffic and exact traces.

### Common failures

Common failures include keeping direct-mapped index bits after adding ways at fixed capacity, comparing only one way's tag, ORing hit data from multiple matches, allowing duplicate valid tags, replacing a valid way while another is invalid, updating LRU on misses that never allocate, using incoming tag for dirty writeback, changing replacement state on squashed/speculative hits without policy, assuming four-way eliminates all conflicts, calling an all-way search free, ignoring data mux and tag fanout timing, comparing caches with different total capacity, and using simulator hit rate without validating replacement/warm state.

### Compact example

A 32 KiB four-way cache with 64-byte lines and 48-bit addresses has 512 lines and 128 sets: 6 offset, 7 index and 35 tag bits. With valid/dirty per line and three tree-PLRU bits per set, logical tag/state/replacement metadata is 19,328 bits, 7.37% of 262,144 data bits. For block trace `[0,4,0,4,8,0,4,8]`, equal four-line caches yield 0/2/5 hits for direct/two-way/four-way LRU. Under invented hit times 1.00/1.18/1.42 ns and 50 ns additional penalty, AMAT is 51.00/38.68/20.17 ns.

### Connections

Set associativity connects address geometry, parallel comparison/mux timing, replacement algorithms, locality/conflict classification, SRAM banking, miss handling, coherence, way prediction, security partitioning and trace-based performance evaluation.

## Governing Question

Direct mapping gives each block one possible line. Associativity gives each block several candidates within one indexed set, reducing collisions among blocks sharing that index. It does not make the cache globally flexible unless it is fully associative.

The benefit is workload-dependent and physically priced. More ways mean more tag comparisons, data access/selection, metadata, wiring and policy state. Lower miss rate must outweigh longer hit paths and energy.

## Why This Matters

Associativity is a core cache design axis. It often captures much of fully associative conflict reduction with tractable indexing, but diminishing returns arrive quickly for many workloads.

Correctness gains new cases: multiple matches must never select ambiguous data; replacement state must remain coherent; refill and coherence races must not create duplicate copies in one set.

Simulation can compare policies and traces, while synthesis/physical implementation determines hit latency, energy and feasible SRAM organization. Both evidence layers are required.

## Prerequisites and Retrieval

Before studying this module, be able to:

- derive direct-mapped offset/index/tag geometry;
- trace valid/tag/data hits, misses and dirty refills;
- distinguish compulsory, capacity and conflict misses;
- implement a small LRU list or finite replacement state;
- interpret AMAT and physical timing trade-offs.

Retrieve exact address identity, cache data capacity, line size, associativity and set count; bank/way organization; tag/data/state fields and ECC; read/write port/collision behavior; parallel/serial/way-predicted lookup; hit vector/priority/duplicate detection; replacement policy, eligibility, insertion and update events; invalid-first rule; transient/refill/MSHR state and same-block merge; dirty writeback; write allocation; coherence/partition/locking state; virtual/physical indexing/aliases; maintenance; reset/scrub/integrity; prefetch interaction; synthesis/STA/area/power; traces and cache/reference simulators; event counters; workloads; tests/formal properties; hardware/firmware/tool/library revisions and errata.

## Learning Objectives

After completing this module, you should be able to:

1. derive set count and tag/index/offset widths for `W`-way geometry;
2. map addresses to one set and enumerate all candidate ways;
3. design parallel qualified tag comparison and one-hot data selection;
4. prevent/detect duplicate live tags within a set;
5. implement invalid-first and exact/approximate replacement state;
6. integrate victim writeback, refill and transient same-block handling;
7. explain how way count changes conflicts, capacity use, latency and energy;
8. compare associativities fairly with equal capacity/line/policy/warm state;
9. verify cache data refinement and replacement invariants;
10. choose associativity from traces plus physical implementation evidence.

## Core Exposition

### Hold total capacity constant

For fair associativity comparison, keep total data bytes and line size fixed unless the experiment deliberately varies them. Increasing ways then decreases sets: `S=C/(B*W)`.

If capacity or line size also changes, miss differences cannot be attributed to associativity alone.

### Derive the address split

Offset bits depend on line size. Index bits depend on set count, not total line count. Adding ways at fixed capacity reduces index bits and increases tag bits.

Check reconstruction `addr=((tag*S+index)*B+offset)` and all configuration divisibility/power assumptions.

### Map one block to one set

Conventional set associativity maps a block to one set and allows any way within that set. It does not search other sets.

Blocks separated by `S` block numbers share the set. Up to `W` distinct such blocks can coexist before replacement is necessary.

### Read all candidate tags

Index selects the same row in each tag way. Compare requested tag with each stored tag, gated by valid and coherence/permission/transient state.

Physical designs may read tag/data ways in parallel, serialize data after tag, bank ways, or predict a way. The logical result remains a verified unique match.

### Enforce one-hot-or-zero hits

The hit vector may contain no match or one match. Two valid qualified copies of the same block in one set indicate a refill/coherence/maintenance error unless an explicit sector/data-replication design proves otherwise.

Assert `$onehot0`-style behavior and choose containment rather than arbitrary priority if duplicates make data trust ambiguous.

### Select hit data

A one-hot mux selects the matching way's data and state. OR-muxing is safe only under proven one-hot matches and electrical/logical encoding; otherwise duplicates can combine corrupt values.

Byte/word selection, extension and ECC occur under exact timing. Way select must remain aligned with data if the lookup is pipelined or stalled.

### Prefer invalid ways

On allocation, search candidate ways for invalid/eligible entries. Using invalid capacity avoids unnecessary eviction and dirty writeback.

If several invalid ways exist, choose a deterministic or policy-defined one. Replacement metadata initialization must remain consistent with that choice.

### Choose a victim when full

When all eligible ways are valid, replacement selects one. Exact LRU uses full recency order; tree-PLRU, NRU, random or RRIP-like policies reduce state/update cost with different behavior.

Locked/reserved/transient/coherence-busy ways may be ineligible. If no victim is available, backpressure rather than overwrite protected state.

### Define replacement update events

Specify whether demand hits, prefetch hits, fills, writebacks, coherence accesses and speculative/killed references update state. Define insertion position for a new line.

Update exactly once at the chosen architectural/microarchitectural event. Replay or multi-cycle lookup must not age the set repeatedly.

### Implement exact LRU for small way counts

An ordered list of way identities or pairwise recency bits can represent exact LRU. On a qualified access, move the way to most recent; victim is least recent.

State count and update logic grow quickly with ways. Verify all permutations, invalid initialization and simultaneous events.

### Implement tree pseudo-LRU

For power-of-two ways, tree direction bits guide victim traversal and are updated away from the accessed path. A four-way tree uses three bits per set.

Tree-PLRU does not always choose the truly least-recent way. Call it an approximation and validate adversarial traces.

### Use random/re-reference policies deliberately

Random replacement can avoid deterministic adversarial thrashing and has little metadata; reproducibility needs seed/state handling. Re-reference interval policies protect lines predicted to return sooner.

Policy superiority is workload- and level-dependent. Preserve traces and exact initialization.

### Keep replacement out of hit correctness

Replacement policy affects which line remains, not whether a current matching valid way returns correct data. A broken policy can hurt performance but must not corrupt memory.

Separate data-coherence invariants from optimization-quality checks. This simplifies assurance.

### Handle dirty victims

Capture selected victim way's stored tag, set index, dirty/coherence state and data. Reconstruct its original block address before any incoming metadata overwrites it.

A victim/writeback buffer can decouple eviction. It becomes part of uniqueness and data refinement: lookup may need to check/forward from it.

### Handle refills and duplicates

Record set and allocated way in the miss entry. During refill, ordinary hits must not see incomplete state except under explicit sector validity.

A second miss to the same block should merge, wait or find the transient entry. Allocating another way can create duplicate tags and lost writes.

### Handle simultaneous hits and fills

A demand hit, refill install, writeback completion and coherence probe may touch one set/way in the same cycle. SRAM ports and priority determine legal concurrency.

Bypass freshly installed/updated state if the macro returns old data, or serialize. Simulation scheduling cannot substitute for port semantics.

### Handle write policies

Write-back marks only the matching selected way dirty and preserves replacement state policy. Write-through forwards lower while maintaining cache copy and buffering/order.

Write misses apply allocation policy and victim selection. Partial writes merge correct line bytes; never choose a way before same-block transient matching.

### Handle virtual/physical identity

Set index may use page-offset bits to overlap translation; tags typically use physical identity. More sets require more index bits and can exceed page offset, creating synonym constraints.

Associativity can help place synonyms but does not solve identity automatically. ASIDs, coloring or synonym detection follow the exact design.

### Handle coherence

Snoops/probes may need parallel tag search across all ways of a set. Coherence state qualifies hits and victim eligibility.

Invalidation clears exactly the matching way; duplicate detection matters because invalidating only one duplicate would leave stale data.

### Handle maintenance and partitioning

Address-based maintenance searches the target set's ways. Set/way iteration operations must cover every physical entry and coordinate with refill/writeback.

Way locking or partition masks restrict eligibility/capacity. Performance comparisons must use effective ways per principal, not nominal associativity.

### Handle reset and integrity

Reset invalidates all ways/transients and initializes replacement state to a legal condition. Full data/tag scrubbing depends on security/ECC policy.

Tag ECC errors must not generate arbitrary multi-hit or victim behavior. Correct, invalidate/refetch, poison or contain under documented trust rules.

### Analyze hit timing

Parallel tag comparisons and a `W`-input data select grow with associativity. High-fanout index/control and way routing can dominate.

Serial tag-then-data saves energy/ports but adds latency. Way prediction accesses one likely way early and verifies, paying recovery on misprediction.

### Analyze energy

Reading all data ways each access wastes energy when one hits. Tag-first, banking, way prediction or phased access reduce toggles at latency/control cost.

Measure energy per useful access and miss traffic. Higher associativity can reduce lower-level energy even if hit energy rises.

### Analyze metadata

Tag width grows as set count shrinks at fixed capacity. Per-line tags/state scale with total lines; replacement state scales by sets and policy.

Logical bit ratios omit decoder/sense/mux/routing and physical macro fragmentation. Use synthesis/memory compiler evidence.

### Compare miss behavior

Simulate identical physical block traces with equal data capacity, line size, write/prefetch policy, replacement model and initial state. Report compulsory/capacity/conflict using an explicit reference.

Increasing ways never guarantees monotonic misses under different replacement approximations or policy state; exact LRU has stronger stack properties than many approximations.

### Compare AMAT and time

Use each design's measured hit time and miss rate plus compatible miss penalty/overlap model. More ways can reduce misses while increasing every hit's latency.

Application time includes clock-period effects, bandwidth/MLP and energy/thermal changes. AMAT is only one layer.

### Test adversarial mappings

Generate more than `W` blocks with the same set index and alternate/reuse them. Exercise duplicate fills, invalid ways, all replacement states, locked ways and dirty victims.

Random traces may rarely hit exact corner permutations. Directed policy tests are required.

### Verify data refinement

Compare cache-visible reads and ordered writes with a shadow backing memory. Every block exists in at most one live way per cache domain, plus explicitly modeled transient/victim copies with coherent ownership.

Assert geometry, onehot0 hits, selected-way data, invalid-first allocation, eligible victim, policy update, dirty address, response matching, maintenance and progress.

### Gather layered evidence

Use generated geometry tests, set/way trace tables, exact-policy model comparison, random cache/shadow-memory differential tests, multi-hit injection, refill/writeback stalls/errors, coherence/maintenance/reset/integrity races, formal safety/liveness/refinement, SRAM mapping, synthesis/STA/area/power, counters, workloads and errata.

Bind evidence to exact address/cache/policy configuration, RTL, macros, protocols, ISA/OS maintenance, tools/libraries, traces/seeds, hardware and firmware/errata. One associativity does not validate another.

## Definitions and Notation

- `C`: cache data capacity in bytes.
- `B=2^b`: line bytes and offset bits `b`.
- `W`: ways per set (associativity).
- `L=C/B`: total cache lines.
- `S=L/W=2^s`: sets and index bits `s` for power-of-two geometry.
- `block=addr//B`; `offset=addr%B`; `index=block%S`; `tag=block//S`.
- `hit_w`: valid/state-qualified tag match for way `w` in selected set.
- `H=[hit_0,...,hit_{W-1}]`: hit vector, required one-hot-or-zero.
- `victim(set)`: eligible allocated/replacement way on miss.
- `R[set]`: replacement metadata for a set.
- `m_W`: miss rate for associativity `W` under a fixed experiment.
- **invalid-first:** allocate an invalid eligible way before replacing a valid one.
- **way prediction:** provisional early way selection followed by full identity verification.
- **stack property:** increasing exact-LRU capacity/associativity under a compatible model does not evict blocks retained by the smaller stack.
- **duplicate tag:** more than one live qualified way represents the same block in one set/domain.

## Mechanisms, Invariants, or Proof Structure

1. **Geometry obligation:** capacity/line/way choices yield integral sets and exact address split.
2. **Mapping obligation:** every block maps to one set and enumerates exactly `W` candidate ways.
3. **Uniqueness obligation:** at most one qualified valid/transient owner represents a block in the cache domain.
4. **Hit obligation:** the hit vector is one-hot-or-zero and full identity/state qualifies each match.
5. **Selection obligation:** returned/updated bytes and metadata come only from the matching way.
6. **Invalid-first obligation:** allocation uses eligible invalid capacity before valid eviction.
7. **Replacement obligation:** a full-set victim is eligible and chosen/updated exactly per policy.
8. **Victim obligation:** dirty identity/data remain coherent through writeback and replacement.
9. **Refill obligation:** same-block misses merge/serialize and partial data cannot create duplicate/false hits.
10. **Port/race obligation:** hit, fill, write, probe and maintenance concurrency follows real array semantics/priority.
11. **Identity/coherence obligation:** translation, aliases, permissions, coherence and partitions cannot return stale data.
12. **Reset/integrity obligation:** every way/transient/policy state initializes or contains corruption safely.
13. **Progress obligation:** under lower-level fairness and available eligible way, accesses complete/fault finitely.
14. **Timing obligation:** tag, compare, select, ECC, prediction and routing meet all implemented constraints.
15. **Evidence obligation:** miss/latency/energy claims hold capacity/trace/policy/state constant and bind artifacts.

## Alternatives and Trade-Offs

1. **Direct versus set-associative:** direct gives one fast candidate; ways reduce collisions with comparison/mux cost.
2. **Set-associative versus fully associative:** indexed sets scale lookup; full search eliminates index conflicts at high cost.
3. **Few versus many ways:** few ways are fast/efficient; many ways improve placement with diminishing miss returns.
4. **Parallel versus serial data access:** parallel minimizes hit cycles; serial saves energy and adds latency.
5. **Way prediction versus all-way access:** prediction saves common energy/time; misprediction recovery/state adds complexity.
6. **Exact LRU versus pseudo-LRU:** exact order can improve policy fidelity; approximations reduce bits/update paths.
7. **Random versus recency:** random is compact/robust to some patterns; recency exploits temporal reuse.
8. **Invalid-first versus policy-only:** invalid-first preserves useful lines; unified policy logic may be simpler but waste capacity.
9. **Victim buffer versus blocking writeback:** buffer hides dirty eviction; blocking design reduces ownership state.
10. **Per-line versus sectored state:** line state is compact; sector state supports partial validity/writes.
11. **Physical versus virtual indexing:** physical mapping avoids synonyms; virtual index overlaps translation with constraints.
12. **Shared versus way-partitioned capacity:** sharing improves utilization; partitions improve isolation/QoS and reduce effective capacity.
13. **Demand-only versus prefetch insertion:** demand protects capacity; prefetch can hide misses and pollute sets.
14. **Logical optimality versus physical timing:** more hits may lose if the hit path sets a longer cycle.
15. **Average AMAT versus tail/QoS:** average guides common time; conflicts/dirty evictions can dominate tails.

## Failure Modes and Misconceptions

1. “Four-way means four sets.” It means four candidate lines per set.
2. “Adding ways adds capacity.” At fixed capacity it reduces set count.
3. “Index bits stay constant when ways change.” They follow set count.
4. “Every address can use any line.” It can use any way only in its mapped set.
5. “Compare the requested tag with one chosen way.” All candidate ways or a verified prediction are required.
6. “OR all matching data safely.” Only a proven one-hot match makes such encoding safe.
7. “Duplicate tags merely waste capacity.” They can return ambiguous/stale data and break coherence.
8. “Valid tags alone define a hit.” Coherence/permission/transient/integrity state also qualifies.
9. “Replacement runs on every miss first.” Same-block transient and invalid-way checks precede valid eviction.
10. “An invalid way may be skipped.” Doing so creates needless eviction/writeback.
11. “LRU is one bit per way.” Exact recency represents ordering, not independent flags.
12. “Tree-PLRU is exact LRU.” It is an approximation.
13. “Random policy needs no state/evidence.” Random source/seed and distribution affect reproducibility.
14. “Every hit should update recency.” Speculative, killed, prefetch and coherence events follow policy.
15. “Replay may update policy repeatedly.” Logical event must update exactly as specified.
16. “Incoming tag reconstructs dirty victim.” Stored victim tag/index are required.
17. “Refill can choose another way for a duplicate miss.” Same-block operations must merge/serialize.
18. “All ways can read/write simultaneously.” Physical ports/banking/collisions constrain them.
19. “Associativity solves virtual aliases.” Identity/page-index rules remain.
20. “More ways eliminate coherence misses.” External invalidation is separate from mapping conflict.
21. “Way locking has no performance effect.” It reduces eligible associativity/capacity.
22. “More ways always reduce misses.” Approximate policies/adversarial traces can behave nonmonotonically.
23. “Higher hit rate always wins.” Hit latency/energy/clock and miss overlap matter.
24. “Logical metadata predicts area.” Macros, routing, comparators and muxes dominate too.
25. “Cache simulation proves timing.” It proves trace behavior under its policy model only.
26. “One warm trace represents the workload.” initial state, phases and mappings change results.

## Worked Examples

### Example 1

A 32 KiB, 64-byte, four-way cache has 512 lines and 128 sets, so a 48-bit address has 6 offset, 7 index and 35 tag bits.

### Example 2

Blocks 0, 128, 256 and 384 all map set 0 and can occupy its four ways; block 512 requires an invalid slot—none—or a victim.

### Example 3

Two valid ways accidentally hold the same tag. A onehot0 assertion fails and containment prevents arbitrary data selection.

### Example 4

One set has two invalid ways. Invalid-first chooses one deterministically and leaves all valid/dirty residents untouched.

### Example 5

Four-way exact LRU order `[A,B,C,D]` from least to most recent becomes `[A,C,D,B]` after a hit on B; A remains victim.

### Example 6

A refill for block X is transient in way 2. A second X request merges with the miss entry rather than allocating duplicate X in way 1.

### Example 7

A dirty way is selected. Its stored tag and set reconstruct writeback address before the incoming tag/state installation.

### Example 8

Way prediction selects way 0 but full tag comparison finds way 3. Recovery returns way 3 data and updates predictor; wrong way never commits data.

### Example 9

A coherence invalidate searches all ways of the indexed set and clears the unique matching way even while replacement metadata points elsewhere.

### Example 10

This deterministic model derives geometry/metadata and simulates equal-capacity direct, two-way and four-way exact-LRU caches.

<!-- bijux-verify: {"id":"set-associative-cache-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"geometry_sets=128 ways=4 offset_bits=6 index_bits=7 tag_bits=35\nlines=512 metadata_bits=19328 overhead_pct=7.37\ntrace_accesses=8 direct_hits=0 two_way_hits=2 four_way_hits=5\ndirect_misses=8 two_way_misses=6 four_way_misses=3\namat_direct_ns=51.00 amat_two_way_ns=38.68 amat_four_way_ns=20.17\n"}} -->
```python
from math import log2

address_bits = 48
capacity_bytes = 32 * 1024
line_bytes = 64
ways = 4
lines = capacity_bytes // line_bytes
sets = lines // ways
offset_bits = int(log2(line_bytes))
index_bits = int(log2(sets))
tag_bits = address_bits - offset_bits - index_bits
metadata_bits = lines * (tag_bits + 1 + 1) + sets * (ways - 1)

def simulate_lru(blocks, total_lines, associativity):
    set_count = total_lines // associativity
    state = [[] for _ in range(set_count)]
    hits = 0
    for block in blocks:
        set_index = block % set_count
        row = state[set_index]
        if block in row:
            hits += 1
            row = [resident for resident in row if resident != block]
            state[set_index] = row
        elif len(row) == associativity:
            row.pop(0)
        row.append(block)
    return hits

blocks = [0, 4, 0, 4, 8, 0, 4, 8]
direct_hits = simulate_lru(blocks, 4, 1)
two_hits = simulate_lru(blocks, 4, 2)
four_hits = simulate_lru(blocks, 4, 4)
accesses = len(blocks)

def amat(hit_time, hits):
    return hit_time + (1 - hits / accesses) * 50.0

print(f"geometry_sets={sets} ways={ways} offset_bits={offset_bits} index_bits={index_bits} tag_bits={tag_bits}")
print(f"lines={lines} metadata_bits={metadata_bits} overhead_pct={100 * metadata_bits / (capacity_bytes * 8):.2f}")
print(f"trace_accesses={accesses} direct_hits={direct_hits} two_way_hits={two_hits} four_way_hits={four_hits}")
print(f"direct_misses={accesses - direct_hits} two_way_misses={accesses - two_hits} four_way_misses={accesses - four_hits}")
print(f"amat_direct_ns={amat(1.00, direct_hits):.2f} amat_two_way_ns={amat(1.18, two_hits):.2f} amat_four_way_ns={amat(1.42, four_hits):.2f}")
```

The trace, exact-LRU policy and hit times are illustrative. Real selection needs physical timing/energy and representative traces.

## Cross-Program Connections

- **Digital Logic:** parallel tag compares, one-hot selection, SRAM banks and ECC define hit paths.
- **Data Structures:** sets are bounded associative containers with replacement metadata.
- **Algorithms:** exact/approximate recency and randomized policies trade state and behavior.
- **Operating Systems:** page coloring, aliases, maintenance and partitions affect effective ways.
- **Concurrent Systems:** refills, writebacks, probes and duplicate misses require ownership/matching.
- **Security Engineering:** shared sets/partitions and way prediction can expose timing state.
- **Formal Methods:** uniqueness, onehot hits, replacement eligibility and shadow-memory refinement are assertable.
- **Performance Engineering:** equal-capacity traces plus hit time, traffic, energy and tails determine value.

## References

1. RISC-V International, [Cache Management Operations](https://docs.riscv.org/reference/isa/unpriv/cmo.html), current cache-block management and ordering semantics; retrieved 2026-09-04.
2. lowRISC, [Ibex Instruction Cache](https://ibex-core.readthedocs.io/en/latest/03_reference/icache.html), current multi-way open-core cache, refill and error behavior; retrieved 2026-09-04.
3. OpenTitan, [RV Core Ibex](https://opentitan.org/book/hw/ip/rv_core_ibex/), current cache configuration, security and verification context; retrieved 2026-09-04.
4. gem5, [Classic Caches](https://www.gem5.org/documentation/general_docs/memory_system/classic_caches/), current configurable cache/memory-port modeling; retrieved 2026-09-04.
5. gem5, [Replacement Policies](https://www.gem5.org/documentation/general_docs/memory_system/replacement_policies/), current replacement-policy concepts and implementations; retrieved 2026-09-04.
6. Valgrind, [Cachegrind Manual](https://valgrind.org/docs/manual/cg-manual.html), current cache-simulation/event interpretation; retrieved 2026-09-04.
7. Intel, [Intel 64 and IA-32 Architectures Software Developer Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), current address/cache-management architectural context; retrieved 2026-09-04.
8. Sarah L. Harris and David Money Harris, [Digital Design and Computer Architecture: RISC-V Edition Resources](https://pages.hmc.edu/harris/ddca/ddcarv.html), associative-cache teaching resources; retrieved 2026-09-04.

## Exercises

### Exercise 1

Derive geometry for 64 KiB caches with 64-byte lines and one, two, four, eight and fully associative organizations under 48-bit addresses.

### Exercise 2

Trace five blocks mapping one set through a four-way cache under exact LRU and tree-PLRU, including invalid initialization.

### Exercise 3

Design hit/refill/coherence logic that proves unique ownership when a second request arrives for a transient block.

### Exercise 4

Modify the executable trace to create a case where two-way helps over direct but four-way's longer hit time loses overall AMAT.

### Exercise 5

Write a verification/measurement plan for selecting L1 associativity with way prediction, ECC, virtual indexing and coherence.

## Answers to the Exercises

### Answer 1

Total lines are `65536/64=1024`; offset bits are 6. Sets are `1024/W`, index bits `log2(1024/W)`, and tags `48-6-index_bits`: direct 1024/10/32; two-way 512/9/33; four-way 256/8/34; eight-way 128/7/35; fully associative one set/0/42.

Account separately for per-line tags/state and replacement metadata. Fully associative lookup compares 1,024 candidates and is not physically equivalent to a zero-index formula alone.

### Answer 2

Initialize all ways invalid, so first four unique blocks allocate without valid eviction; define deterministic invalid choice and recency insertion. The fifth evicts the exact LRU. For each later hit, move that way to MRU.

For tree-PLRU, record three direction bits, traverse them for a victim and update away from each accessed path. Produce a step table because tree-PLRU may select a different victim than exact LRU. Neither difference may corrupt data.

### Answer 3

Maintain one block-identity ownership directory over stable valid ways plus miss/transient/victim state. Before allocation, search qualified stable and transient identities. A matching transient request merges/waits and records dependent destinations; it cannot allocate another way.

Coherence probe searches all candidates/owners and serializes or updates transient handling. Refill installs once into reserved set/way, publishes validity only when safe, and wakes merged requests. Assert one live owner, one lower request, matched response beats, no partial hit, correct probe result and safe kill/reset disposal.

### Answer 4

Search or construct traces where direct repeatedly alternates two same-index blocks, while two-way retains them; add enough accesses that four-way has the same misses as two-way. Then use hit times such that `(t4-t2)` exceeds any four-way miss-rate benefit—which is zero for this trace—so four-way AMAT is worse.

Keep total lines, line size, exact LRU, warm state and penalty fixed. Report whether clock period, energy and bandwidth change; the exercise is an analytical example, not a universal associativity ranking.

### Answer 5

Sweep configurations using identical traces/workloads and physical address streams. Verify geometry, unique tags, onehot0 hits, way-predict verify/recovery, invalid-first, replacement permutations, dirty victim/refill, same-block merging, ECC injection, aliases/page colors, coherence/maintenance races and reset/late responses against a shadow model.

Run formal safety/liveness/refinement plus SRAM compilation, synthesis/STA/place-route/area/power for each way count/predictor. Validate cache/way-miss counters, measure hit/miss latency, traffic, energy, application time and tails across cold/warm phases. Bind exact ISA/OS, RTL/config, macros/protocol, tools, traces/binaries/seeds, hardware and errata. Internal evidence is not independent certification.
