---
module_id: CA-040
program: Computer Architecture
level: 1
module_number: 40
title: Analyzing Cache Misses from an Access Trace
status: complete
last_verified: 2026-09-04
---

# Analyzing Cache Misses from an Access Trace

## One-Page Review

### Governing question

Given an ordered memory-access trace and an exact cache specification, how can we reproduce every hit, miss, eviction and writeback; classify misses without circular reasoning; connect events to bytes and latency; and distinguish what the trace proves from behavior it omits or perturbs?

### Essential definitions

- An **access trace** is an ordered record of memory references with stated fields, scope and collection semantics.
- A **block trace** maps byte addresses to cache-block identities using the analyzed line size.
- A **cold/empty start** initializes all cache entries invalid; a **warmed start** carries or prepares state before measurement.
- A **compulsory miss** is the first observed reference to a block in the defined trace/history.
- A **capacity miss** is a non-first miss that also misses an equal-capacity fully associative reference cache under the chosen replacement model.
- A **conflict miss** is a non-first target-cache miss that hits that equal-capacity fully associative reference.
- The **3C model** partitions misses into compulsory, capacity and conflict under explicit assumptions.
- A **shadow cache** is a reference structure run on the same accesses to support counterfactual classification.
- **reuse distance** is the number of distinct blocks between consecutive references to a block under a stated convention.
- A **stack-distance profile** relates reuse distances to fully associative LRU miss behavior across capacities.
- A **writeback** transfers a dirty victim toward a lower level; it is traffic caused by a miss but not itself necessarily a demand miss.
- A **sampling trace** records only selected accesses or intervals and needs weighting/limitations.
- A **trace-driven simulation** replays recorded events; it may not reproduce timing-dependent interleavings or feedback.

### Central model, mechanism, or theorem

For each trace event in order, first derive exact block identity, set and tag. Query target state and an equal-line-count fully associative LRU shadow before updating either. A target miss is compulsory if the block has never appeared; otherwise it is conflict if the shadow hits and capacity if the shadow misses. Then perform the target's exact write/allocation/replacement transition, record evictions/writebacks/bytes, and update shadow state. Under empty start, demand accesses, uniform line size and LRU reference assumptions, the categories partition target misses: `misses=compulsory+conflict+capacity`.

### Critical invariants

- Trace order, access type, address, size, context and inclusion/exclusion rules are preserved exactly.
- Every byte access maps to all and only the cache blocks it touches; split accesses are not silently collapsed.
- Target geometry, replacement, insertion, write and allocation policy match the stated configuration.
- Classification consults seen/shadow state before the current access updates those structures.
- The fully associative shadow has the same data-line capacity and line size as the target for 3C comparison.
- Compulsory, conflict and capacity categories are mutually exclusive and sum to target demand misses.
- Dirty state, partial writes and victim identity are preserved through writeback accounting.
- Warm-up, flushes, context switches, coherence and prefetch events follow one documented inclusion policy.
- Metrics use stable denominators and separately report accesses, misses, evictions, transactions and bytes.
- Reproduction binds exact trace digest, cache parameters, simulator version, initialization and random seed.

### Common failures

Common failures include using byte addresses as block identities, ignoring accesses spanning two lines, updating LRU before classifying, calling every repeated miss capacity, comparing a set-associative target with a differently sized shadow, using FIFO shadow for LRU stack claims, counting writebacks as misses, counting instruction fetches in one denominator but not another, treating sampled traces as complete, forgetting cold versus warmed state, allowing prefetches to alter one run only, losing process/physical identity, replaying a timing trace as though scheduling were unchanged, and reporting a miss-rate reduction without checking traffic or runtime.

### Compact example

For block trace `[0,4,0,4,1,5,1,5,0,4,8,0,1,5]`, a four-line direct-mapped cache has zero hits and 14 misses because blocks collide by index. An equal-capacity fully associative LRU shadow has seven misses. The 3C classifier reports five compulsory, seven conflict and two capacity misses, which sum to 14. At 64-byte lines, target fills total 896 bytes versus 448 shadow-fill bytes. With invented one-cycle hit and 50-cycle additional miss penalty, modeled AMAT is 51 versus 26 cycles.

### Connections

Trace analysis connects address geometry, data structures, reuse/stack distance, replacement/write policy, multilevel caches, prefetch/coherence, profiling, simulation validation, statistical sampling, performance counters and reproducible experimentation.

## Governing Question

A miss counter says how often a cache could not serve a request, but not why. An ordered trace plus an exact model allows event-by-event explanation and counterfactual comparison.

The answer is only as trustworthy as the trace and configuration. Virtual versus physical addresses, omitted kernel/DMA accesses, warm-up, speculation and timing feedback can change results substantially.

## Why This Matters

Miss classification guides different remedies. Compulsory misses suggest transfer/prefetch opportunity; conflict misses suggest mapping/associativity; capacity misses suggest working-set/capacity or locality changes.

Yet 3C labels are model-relative. Coherence and prefetch misses need additional categories, and a larger cache can be slower or use more energy despite fewer misses.

Executable analysis prevents hand-trace drift and establishes conservation properties before larger simulation or hardware study.

## Prerequisites and Retrieval

Before studying this module, be able to:

- derive block, index and tag from an address;
- simulate direct-mapped and set-associative LRU state;
- distinguish write-back/write-through and allocation policies;
- compute rates, bytes and elementary AMAT;
- explain trace collection and performance-counter limitations.

Retrieve trace producer and version; workload/binary/input; ISA and address width; virtual/physical/process/thread identity; included access classes and privilege; instruction/data distinction; timestamp/order semantics; access address, size, type, masks and atomics; sampling/filtering/loss; warm-up and region boundaries; cache levels, capacities, line sizes, sets, ways, sectoring; replacement/insertion/write/allocation; prefetch/coherence/maintenance events; random seeds; simulator/toolchain configuration; hardware counters and event definitions; compression/parser schema; trace digest and known errata.

## Learning Objectives

After completing this module, you should be able to:

1. normalize byte accesses into ordered cache-block events;
2. trace set/tag/hit/victim/dirty transitions exactly;
3. implement a seen set and equal-capacity fully associative LRU shadow;
4. classify compulsory, conflict and capacity misses under stated assumptions;
5. validate miss-category conservation and shadow behavior;
6. account separately for fills, evictions, writebacks, transactions and bytes;
7. handle warm-up, split accesses, writes and multilevel/prefetch/coherence scope;
8. explain reuse-distance and trace-driven limitations;
9. compare analytical, simulator and hardware-counter evidence;
10. produce a reproducible cache-trace study.

## Core Exposition

### Define the question first

State whether the goal is to debug one mapping, classify misses, select capacity/associativity, estimate traffic or explain measured stalls. This determines required trace fields and model fidelity.

A trace adequate for read-only L1 classification may be inadequate for writebacks, coherence or physical indexing.

### Identify the trace producer

Instrumentation, functional simulation, sampled hardware tracing and cycle simulation observe different events. Record producer version and whether addresses reflect committed, speculative or filtered accesses.

Do not infer completeness from file size. Check loss indicators and collection boundaries.

### Define event order

Cache state depends on order. Per-thread program order may not equal global memory-system arrival order, especially on multicore systems.

Choose the ordering appropriate to the modeled cache and preserve stable ties or explicit timestamps.

### Normalize addresses

For line bytes `B`, block is `address//B` and byte offset is `address mod B`. Validate nonnegative/canonical address width and arithmetic overflow.

Keep original address/size for reporting and split-access handling.

### Split crossing accesses

An access from offset `B-2` of size eight touches two blocks. Generate ordered subevents or an atomic multi-block representation matching cache behavior.

Do not count one source instruction automatically as one cache access.

### Derive set and tag

For `S` sets, `index=block mod S` and `tag=block//S` under ordinary modulo mapping. Hashed/skewed caches need their real functions.

Round-trip block from tag/index to catch geometry mistakes.

### Initialize explicitly

Empty start makes every first-seen block miss. Warmed analysis runs a prelude or loads a defined snapshot before resetting measurement counters.

State whether replacement and dirty/prefetch state are also warmed.

### Simulate the target cache

On every event, check all eligible ways for a valid matching tag. On hit, update data/dirty and replacement state according to policy.

On miss, apply write allocation/bypass, invalid-first selection, dirty victim writeback and insertion exactly.

### Preserve update order

Query target, seen history and shadow before inserting the current block. Updating first converts a miss into a false reference hit.

Record a pre-state row, classification and post-state for auditable small traces.

### Count compulsory misses

If the block has not appeared in the classification history, its target miss is compulsory. Then add it to the seen set.

The definition depends on trace start. A first observed access may not be first in the program or machine lifetime.

### Build the fully associative shadow

Give the shadow the same number of data lines and same line bytes as target, one set and LRU replacement. Feed the same class/order of demand block accesses.

Query before update. Move a hit to MRU; on full miss, evict LRU and insert MRU.

### Classify conflict misses

A non-first target miss that hits the shadow is conflict under 3C assumptions. Equal capacity could hold the block; target placement/replacement caused its absence.

The label does not prove higher associativity is free or that a specific alternative policy hits.

### Classify capacity misses

A non-first miss in both target and equal-capacity fully associative LRU shadow is capacity. The recent distinct working set exceeded what that reference retained.

Capacity remains relative to line size, access stream, initialization and LRU reference.

### Check conservation

For every target demand miss, exactly one 3C category applies. Assert `misses=compulsory+conflict+capacity`.

Also assert hits plus misses equals classified target accesses and shadow hits plus misses equals shadow accesses.

### Understand stack distance

For fully associative LRU, a repeated reference hits capacity `C` when its reuse distance is below `C` under the selected convention. First references have infinite/undefined distance.

One stack-distance profile can derive LRU misses across many fully associative capacities.

### Respect replacement assumptions

The classical stack property applies to LRU, not arbitrary FIFO/random/adaptive policies. A FIFO target/shadow can exhibit non-stack behavior.

Name the policy used for classification and separate alternative-policy deltas.

### Handle writes

Write hits update enabled bytes and dirty state under write-back or propagate under write-through. Write misses follow allocate/no-allocate policy.

Demand miss count, fill count and lower writes can differ. Track each separately.

### Account for dirty evictions

When a dirty target victim leaves, reconstruct its stored block address and add the protocol's writeback bytes/transactions. Do not use the incoming block identity.

At measurement end, state whether remaining dirty lines are drained or carried.

### Handle no-write-allocate

A write miss may bypass without filling target cache. It is still a target miss but does not cause a line fill under that policy.

Decide how the 3C demand stream treats bypassing writes; publish the choice.

### Handle multilevel caches

Feed L2 only events it actually receives: L1 misses/fills, writebacks, prefetch/coherence traffic according to design. L2 local denominators differ from original accesses.

An independent all-demand trace at every level invents requests.

### Handle prefetching

Prefetches change residence and may eliminate or create demand misses. Classical 3C classification is clearest with demand-only baseline/shadow; prefetch effects need useful/late/pollution categories.

Replay identical prefetch policy or disable it consistently across compared designs.

### Handle coherence

Invalidation misses occur because another agent revoked a copy and are not explained fully by 3C placement/capacity. Record invalidation and ownership events if claiming coherence classification.

Without them, label unexplained repeated misses conservatively.

### Handle instruction and data streams

Split I/D caches require separate traces/models; unified caches receive a merged ordered stream. Self-modifying code adds maintenance/coherence events.

Report denominators by access class and combined only when meaningful.

### Preserve address-space identity

Virtual traces can alias/synonym differently from physical caches. Reused virtual addresses across processes are not one physical block.

Include process/ASID and translation mapping or restrict claims to virtual-cache models.

### Treat atomics and split operations

Atomics may translate into read-modify-write/coherence transactions while one architectural instruction. Trace schema defines whether one or several cache events appear.

Do not expand or collapse without matching the analyzed interface.

### Validate the parser

Reject malformed lines, overflow, unknown operation codes and truncated records. Count accepted/rejected events and compare producer totals.

Test endianness/compression framing and deterministic replay.

### Validate small traces by hand

Use compulsory-only, repeated-one-block, conflict pairs, working-set overflow, dirty victim and split-line cases. Tabulate expected states.

Small counterexamples expose update-order and geometry bugs before large traces obscure them.

### Differential-test simulators

Run the same normalized trace/configuration through an independent model such as Cachegrind, gem5 or a second local implementation where semantics align.

Reconcile differences in allocation, instruction events, writeback and warm-up rather than averaging results.

### Connect misses to traffic

Multiply fills/writebacks by actual transferred granularity only after counting them. Add prefetch, coherence, retries and partial-sector behavior separately.

Payload bytes and bus/protocol bytes are different measures.

### Connect misses to latency

Elementary `hit_time+miss_rate*penalty` is a baseline. Real traces omit or approximate overlap, queueing, contention, early restart and dependent stalls.

Use timed simulation or hardware counters for runtime claims, while retaining the trace model for causality checks.

### Use sampling carefully

Sampled traces may miss intervening accesses that alter cache/reuse state. Scaling counts cannot restore exact ordering.

Use sampling-aware methods, confidence intervals and validation against full smaller regions.

### Define warm-up and windows

Choose instruction/reference/time warm-up, then reset counters while retaining intended state. Ensure all configurations receive equivalent warm-up opportunity.

Phase boundaries can dominate results; report per-phase and aggregate weighting.

### Measure uncertainty

Deterministic trace replay has no run-to-run sampling variance for fixed seed/configuration, but workload/input sampling and randomized replacement do.

Use multiple seeds/inputs where applicable and report dispersion.

### Protect sensitive traces

Addresses reveal code/data layout and behavior. Minimize collected fields, restrict access, anonymize carefully and delete/retain under policy.

Anonymization that changes block/set relationships can invalidate cache analysis.

### Make results reproducible

Record trace digest, schema, producer, workload, binary/input, filters, configuration, warm-up, simulator commit, seed and command.

Store generated reports in governed artifacts, not beside source modules.

### Verify the complete analysis

Assert conservation, target/shadow capacity, one-hot hits, legal victims, byte correctness and deterministic output. Spot-check sampled state rows.

Compare summary counters to per-event logs and independent tools/hardware where scopes match.

### Gather layered evidence

Begin with hand traces and executable models, then full traces/reference simulators, cycle models and hardware counters. Use application outcomes for impact.

State trace omissions and never promote functional replay to timing proof.

## Definitions and Notation

- `a`: byte address; `n`: access size in bytes.
- `B`: cache-line bytes; `block=floor(a/B)`.
- `S`: number of target sets; `index=block mod S`, `tag=floor(block/S)` for modulo mapping.
- `L`: total data lines in target and equal-capacity shadow.
- `Seen`: blocks observed before the current event.
- `T_hit`: target-cache hit before current update.
- `F_hit`: fully associative LRU shadow hit before current update.
- `C0`, `Cf`, `Cc`: compulsory, conflict and capacity miss counts.
- `M=C0+Cf+Cc`: 3C partition under stated assumptions.
- `fills`: lower-to-cache line/sector transfers caused by allocation.
- `writebacks`: dirty cache-to-lower transfers.
- `miss_rate=M/accesses` for the named request class.
- `reuse_distance`: count of distinct intervening blocks under the documented convention.

The shadow is a classification instrument, not necessarily a proposed implementation. Extensions may add coherence, policy or prefetch categories; do not force those events into 3C without stating a model.

## Mechanisms, Invariants, or Proof Structure

1. **Trace obligation:** accepted events preserve producer order, fields and stated scope.
2. **Normalization obligation:** every byte range maps to exactly its touched blocks.
3. **Geometry obligation:** block/set/tag decoding and reconstruction match configuration.
4. **Target-state obligation:** hits, victims, dirty data and replacement updates follow exact policy.
5. **Pre-update obligation:** target, seen and shadow queries occur before current-event mutation.
6. **Shadow obligation:** fully associative LRU shadow has equal line capacity/size and input stream.
7. **Partition obligation:** each target demand miss receives exactly one applicable category.
8. **Conservation obligation:** hits+misses=accesses and 3C counts sum to misses.
9. **Write obligation:** allocation/bypass, byte masks, dirty state and final drain are explicit.
10. **Traffic obligation:** fills, writebacks, prefetch/coherence and bytes remain separate.
11. **Hierarchy obligation:** lower levels receive only modeled upstream events.
12. **Identity obligation:** address-space/physical identity prevents false block merging.
13. **Window obligation:** initialization, warm-up, sampling and end state are documented.
14. **Reproduction obligation:** trace/config/tool/seed digests and versions identify the run.
15. **Claim obligation:** functional, traffic and timing evidence are not conflated.

An induction over trace events proves target/shadow state corresponds to their specified transition functions. Pre-update classification and `Seen` establish mutual exclusion/exhaustiveness of 3C categories. Traffic refinement adds dirty/allocation state. Timing and real-system claims require separate evidence because recorded ordering may not preserve feedback.

## Alternatives and Trade-Offs

1. **Hand trace versus executable model:** hand tables teach mechanics; code scales and enforces conservation.
2. **Full trace versus sampling:** full order supports exact replay; sampling reduces collection/storage cost.
3. **Virtual versus physical addresses:** virtual collection is easier; physical identity matches many cache mappings.
4. **Cold versus warmed start:** cold is deterministic; warmed state better represents steady operation.
5. **3C versus reuse distance:** 3C explains target misses; reuse distance derives many fully associative LRU capacities.
6. **Event log versus summary counters:** logs enable audit; summaries reduce volume.
7. **Functional versus timed simulation:** functional models explain state; timed models capture contention/overlap.
8. **Demand-only versus all traffic:** demand-only clarifies locality; all traffic estimates system cost.
9. **One-level versus hierarchy replay:** one level isolates policy; hierarchy captures filtering/interactions.
10. **Exact LRU versus implementation policy:** LRU supports stack analysis; real policy matches deployed behavior.
11. **Per-thread versus merged order:** per-thread aids attribution; shared caches need an appropriate global order.
12. **Trace prefetch versus generated prefetch:** recorded events reproduce a run; generated policy supports counterfactuals.
13. **Per-phase versus aggregate:** phases expose behavior; aggregates summarize with weighting risk.
14. **Simulator versus hardware counters:** simulation exposes state; hardware observes real timing with event ambiguity.
15. **More associativity versus more capacity:** associativity targets conflicts; capacity targets working-set misses at different costs.

## Failure Modes and Misconceptions

1. “Address equals cache block.” Divide by line bytes first.
2. “One instruction means one cache access.” Size/alignment and microarchitecture can create several.
3. “Every first trace reference is globally compulsory.” It is compulsory relative to observed history/window.
4. “Every repeated miss is capacity.” An equal-capacity associative shadow separates conflict.
5. “Conflict means the shadow misses.” Conflict requires target miss and shadow hit.
6. “Update shadow then query.” That falsely makes every current reference a hit.
7. “Any fully associative size works.” 3C comparison needs equal data-line capacity/line size.
8. “FIFO shadow supports LRU stack distance.” Stack properties are policy-specific.
9. “Set count is capacity.” Total lines equal sets times ways.
10. “Invalid ways require replacement.” Invalid-first allocation avoids a valid eviction.
11. “Incoming tag reconstructs dirty victim.” Stored victim identity is required.
12. “Writeback is a demand miss.” It is a distinct lower transfer.
13. “Every miss causes one fill.” No-write-allocate, sectors and merges differ.
14. “End dirty lines need no policy.” Drain versus carried state changes traffic/completion.
15. “L2 sees every CPU access.” It sees filtered L1 misses/writebacks and other modeled traffic.
16. “Prefetches only reduce misses.” They can add traffic and pollution misses.
17. “3C explains coherence invalidations.” Coherence requires additional event/state evidence.
18. “Virtual addresses identify physical cache lines.” Synonyms, aliases and processes break that assumption.
19. “Sample scaling recreates reuse order.” Missing intervening blocks change state.
20. “A trace replays original timing.” Cache changes can alter issue/interleaving/feedback.
21. “Miss rate determines runtime.” Penalty, overlap, queueing and hit time matter.
22. “Fewer fills means fewer bytes universally.” Line/sector/writeback/protocol granularities differ.
23. “Warm-up may differ across designs.” That confounds comparison.
24. “Random replacement needs one run.” Seeds and dispersion matter.
25. “Counter agreement proves event identity.” Different events/scopes can coincidentally match.
26. “An anonymized trace is automatically valid.” Transformations may alter block/set relationships.

## Worked Examples

### Example 1

With 64-byte lines, addresses 63 and 64 map to blocks 0 and 1; an eight-byte access starting at 60 touches both.

### Example 2

A four-line direct-mapped cache has index `block mod 4`; blocks 0, 4 and 8 all contend for index 0.

### Example 3

On the first block-4 miss, query seen/shadow first, classify compulsory, then insert into both histories.

### Example 4

On a repeated block that target misses but equal-capacity shadow hits, classify conflict before updating LRU order.

### Example 5

On a repeated miss in both target and shadow, classify capacity under the equal-capacity LRU reference.

### Example 6

A dirty block-0 victim displaced by block 4 writes back block 0's address and data, not the incoming tag.

### Example 7

A no-write-allocate store miss counts as a demand miss but issues payload lower without a target fill.

### Example 8

An L1 miss plus later dirty eviction may create one L2 read and one L2 write-like event; they need distinct counters.

### Example 9

Sampling removes an intervening distinct block, shrinking apparent reuse distance and potentially converting a modeled miss to hit.

### Example 10

This deterministic direct-mapped and fully associative shadow model audits 3C classification, fill bytes and elementary AMAT.

<!-- bijux-verify: {"id":"cache-trace-classifier","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"accesses=14 target_hits=0 target_misses=14\ncompulsory=5 conflict=7 capacity=2 category_sum=14 shadow_misses=7\ntarget_fill_bytes=896 shadow_fill_bytes=448 target_amat_cycles=51.00 shadow_amat_cycles=26.00\n"}} -->
```python
from collections import OrderedDict

trace = [0, 4, 0, 4, 1, 5, 1, 5, 0, 4, 8, 0, 1, 5]
line_count = 4
line_bytes = 64
target = [None] * line_count
shadow = OrderedDict()
seen = set()
hits = misses = compulsory = conflict = capacity = 0

for block in trace:
    target_hit = target[block % line_count] == block
    shadow_hit = block in shadow
    if target_hit:
        hits += 1
    else:
        misses += 1
        if block not in seen:
            compulsory += 1
        elif shadow_hit:
            conflict += 1
        else:
            capacity += 1
    target[block % line_count] = block
    if shadow_hit:
        shadow.move_to_end(block)
    else:
        if len(shadow) == line_count:
            shadow.popitem(last=False)
        shadow[block] = True
    seen.add(block)

shadow_misses = compulsory + capacity
hit_time = 1
miss_penalty = 50
target_amat = hit_time + (misses / len(trace)) * miss_penalty
shadow_amat = hit_time + (shadow_misses / len(trace)) * miss_penalty

print(f"accesses={len(trace)} target_hits={hits} target_misses={misses}")
print(f"compulsory={compulsory} conflict={conflict} capacity={capacity} category_sum={compulsory + conflict + capacity} shadow_misses={shadow_misses}")
print(f"target_fill_bytes={misses * line_bytes} shadow_fill_bytes={shadow_misses * line_bytes} target_amat_cycles={target_amat:.2f} shadow_amat_cycles={shadow_amat:.2f}")
```

The trace, cache and timing are invented. The target is read-only direct-mapped; the shadow is fully associative LRU; both start empty. The model omits writes, split accesses, hierarchy, prefetch, coherence, queueing and overlap.

## Cross-Program Connections

- **Algorithms:** online replacement and counterfactual shadows classify history-dependent events.
- **Data Structures:** sets, LRU orders, seen sets and stack-distance trees encode trace state.
- **Operating Systems:** address spaces, physical mappings and context switches determine identity.
- **Concurrent Systems:** shared-cache ordering/coherence cannot be reconstructed from per-thread traces alone.
- **Data Engineering:** trace schemas, parsing, digests and provenance determine analytical integrity.
- **Statistics:** sampling, workload selection and randomized policies require uncertainty analysis.
- **Security Engineering:** address traces are sensitive and anonymization can alter analytical structure.
- **Performance Engineering:** misses, traffic, penalties, overlap and counters connect model to runtime.

## References

1. Valgrind, [Cachegrind Manual](https://valgrind.org/docs/manual/cg-manual.html), current cache simulation, configuration and event interpretation; retrieved 2026-09-04.
2. gem5, [Classic Caches](https://www.gem5.org/documentation/general_docs/memory_system/classic_caches/), current cache/MSHR/write-buffer trace and modeling context; retrieved 2026-09-04.
3. gem5, [Replacement Policies](https://www.gem5.org/documentation/general_docs/memory_system/replacement_policies/), current replacement/insertion policy definitions; retrieved 2026-09-04.
4. ChampSim, [ChampSim Repository](https://github.com/ChampSim/ChampSim), current trace-based cache simulation and reproducibility framework; retrieved 2026-09-04.
5. Linux perf wiki, [perf Main Page](https://perf.wiki.kernel.org/index.php/Main_Page), current Linux performance-counter tooling context; retrieved 2026-09-04.
6. Linux kernel, [Perf Events and Tool Security](https://docs.kernel.org/admin-guide/perf-security.html), current counter access and data-security context; retrieved 2026-09-04.
7. Intel, [Intel 64 and IA-32 Architectures Software Developer Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), current cache/performance-monitoring architectural context; retrieved 2026-09-04.
8. Sarah L. Harris and David Money Harris, [Digital Design and Computer Architecture: RISC-V Edition Resources](https://pages.hmc.edu/harris/ddca/ddcarv.html), cache tracing and miss-analysis teaching resources; retrieved 2026-09-04.

## Exercises

### Exercise 1

Hand-trace a two-way cache and equal-capacity fully associative LRU shadow, recording pre/post state and 3C category for every access.

### Exercise 2

Extend the classifier for byte addresses, sizes, reads/writes, write-back/write-allocate and final dirty drain.

### Exercise 3

Design a multilevel trace pipeline that generates only the events each lower level receives, including writebacks and prefetches.

### Exercise 4

Implement reuse distance and compare its fully associative LRU miss counts across capacities with direct simulations.

### Exercise 5

Write a reproducible study plan comparing cache organizations using traces, timed simulation and hardware counters.

## Answers to the Exercises

### Answer 1

For each block, write target set/tag/ways/replacement order and shadow LRU order before access. Query target, seen and shadow; classify first-seen, target-miss/shadow-hit or miss/miss; then update both. Allocate invalid ways first and move only qualified hits/fills according to policy.

Assert category sum equals target misses and both hit/miss sums equal accesses. Differences from hand expectation should be resolved at the first divergent event, not from final totals.

### Answer 2

Split `[address,address+size)` at line boundaries and retain source-event identity. For each subevent, simulate hit/miss; write hits merge enabled bytes and mark dirty. Write-allocate misses fill/merge; no-allocate misses bypass. Dirty victim writeback uses stored block identity.

Count source operations, cache subaccesses, demand misses, fills, bypass payload, dirty writebacks and bytes separately. At end either drain each dirty resident once or explicitly carry state; apply the same rule to comparisons.

### Answer 3

Normalize original demand events into L1. Its transition emits L2 reads/fills, dirty writebacks and configured prefetch/coherence events with causal ordering/IDs. L2 processes only those emitted events and may emit memory traffic. Preserve request class so denominators remain local.

Model merges and outstanding timing if ordering matters; a purely functional pipeline should state that limitation. Validate conservation between each producer's emitted count and consumer's accepted count.

### Answer 4

Maintain the most-recent order of distinct blocks; on repeated reference, count distinct blocks more recent than the target, then move it to MRU. First references are compulsory/infinite. For capacity `C`, repeated reference misses fully associative LRU when distance is at least `C` under this convention.

Compare predicted totals with independent fully associative LRU simulations for many small/random traces and capacities. Do not apply the stack theorem to FIFO/random without separate proof.

### Answer 5

Pin trace producer/schema/digest, workload/binary/input, address identity, included access classes, loss/sampling, warm-up/window and security handling. Pin each cache's geometry, policies, hierarchy, prefetch/coherence scope, simulator commit and seeds. Validate parsers, hand traces, conservation and independent models.

Report hits/3C/other misses, fills/writebacks/bytes, local/global rates, latency distributions, stalls, runtime, energy/area/timing and per-workload uncertainty. Reconcile simulator events with hardware-counter definitions before comparison. Internal trace evidence does not constitute external performance or hardware certification.
