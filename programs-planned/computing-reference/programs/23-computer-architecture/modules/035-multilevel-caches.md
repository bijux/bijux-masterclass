---
module_id: CA-035
program: Computer Architecture
level: 1
module_number: 35
title: Multilevel Caches
status: complete
last_verified: 2026-09-04
---

# Multilevel Caches

## One-Page Review

### Governing question

How should several cache levels cooperate so that the common access is fast, the uncommon access is affordable, every block has a coherent authoritative state, and measured improvements survive queueing, traffic, inclusion, maintenance and physical implementation costs?

### Essential definitions

- A **cache hierarchy** is an ordered set of storage levels between requesters and main memory.
- **L1**, **L2** and **last-level cache** (`LLC`) name progressively downstream cache roles, not universal capacities or latencies.
- A **local hit rate** is hits at one level divided by requests that reach that level.
- A **global hit rate** is hits at one level divided by original top-level accesses.
- **hit time** includes lookup, selection and delivery work required before that level can respond.
- **miss penalty** is the additional latency from a miss until the requester can resume under a stated completion definition.
- An **inclusive** relationship requires every valid block in an upper cache to have a corresponding lower-cache representation.
- An **exclusive** relationship normally permits a block to reside in only one of the related cache data arrays.
- A **non-inclusive/non-exclusive** (`NINE`) relationship imposes neither blanket property; exact coherence rules still apply.
- A **back-invalidation** invalidates an upper copy when an inclusive lower copy is evicted.
- A **victim cache** retains recently displaced blocks, often as a small fully associative level.
- A **miss-status holding register** (`MSHR`) tracks an outstanding miss and its dependents.
- **critical-word-first** and **early restart** return needed data before the entire line arrives, when protocol and integrity rules permit.
- **average memory access time** (`AMAT`) is an expectation over a specified request population; it is not a tail-latency guarantee.

### Central model, mechanism, or theorem

For serial lookups with L1 hit time `t1`, L1 local miss probability `m1`, L2 hit time `t2`, L2 local miss probability `m2`, and memory service `tm`, the elementary model is `AMAT = t1 + m1*(t2 + m2*tm)`. The nesting matters: `m2` is conditional on reaching L2. A correct hierarchy also needs a block-state refinement: hits, fills, writebacks, probes, invalidations and evictions across all levels must implement one coherent memory abstraction, preserve the newest bytes, and complete exactly once despite concurrency and errors.

### Critical invariants

- Each level decodes the same physical block identity despite different line, sector, banking or indexing choices.
- A response comes from a qualified, complete and permitted copy or from an explicitly forwarded newer owner.
- At most the coherence protocol's allowed writers/owners exist for a block across private and shared levels.
- Dirty data cannot be silently displaced by a lower-level eviction, back-invalidation or upper-level replacement.
- Inclusive eviction finds and invalidates every required upper copy before reusing directory/data state.
- Exclusive movement neither duplicates nor loses a line during swap, refill or retry.
- MSHRs, fill buffers and writeback queues retain identity, byte validity, ordering and ownership until completion.
- Same-block misses merge or serialize rather than allocate conflicting transient copies.
- Maintenance and coherence completion cover every participating level named by the architectural contract.
- AMAT and performance claims use conditional probabilities, measured overlaps, queueing and identical workloads/configurations.

### Common failures

Common failures include multiplying an L2 local hit rate by all references, adding all level hit times on an L1 hit, calling a hierarchy inclusive merely because duplicates happen to exist, discarding an upper dirty copy during back-invalidation, assuming exclusive caches never need coherence metadata, installing a late fill after an invalidation, under-sizing MSHRs for advertised memory-level parallelism, ignoring writeback queue deadlock, counting early restart as full miss completion, treating an LLC hit as fixed latency under contention, comparing equal hit rates with unequal traffic, flushing only one level, and reporting AMAT without latency distributions or request-class definitions.

### Compact example

Suppose `t1=1 ns`, `m1=0.08`, `t2=6 ns`, `m2=0.25`, and `tm=80 ns`. Serial `AMAT=1+0.08*(6+0.25*80)=3.08 ns`. The L1 global hit rate is 92%; the L2 global hit rate is `0.08*0.75=6%`; memory receives `0.08*0.25=2%`. Removing L2 gives `1+0.08*80=7.40 ns`, so this latency-only model predicts `2.40x` speedup. It excludes queueing, overlap, write traffic, coherence and early restart and therefore is not an implementation result.

### Connections

Multilevel caches connect locality, conditional probability, replacement, prefetching, coherence directories, interconnects, DRAM scheduling, nonblocking pipelines, virtual memory, cache maintenance, persistence, timing closure, energy and workload methodology.

## Governing Question

A tiny nearby cache can be fast but cannot hold a large working set. A larger cache catches more reuse but costs more time, energy, wires and contention. A hierarchy attempts to obtain the common-case latency of the first and the miss reduction of the second.

The levels are not independent filters. An upper miss creates work below; a lower eviction may change upper state; dirty ownership may reside above the shared cache; queues couple progress; prefetch and coherence traffic compete with demand. The design question is therefore both probabilistic and protocol-level.

## Why This Matters

Modern processors spend substantial time and energy moving data. A small change in L1 miss rate can amplify downstream traffic, while a modest LLC hit-rate improvement may be irrelevant if queueing or coherence dominates its response.

Hierarchy organization affects correctness as well as speed. Inclusion can simplify snoop filtering but turns a lower eviction into upper invalidations. Exclusivity increases effective data capacity but makes movement and metadata more complicated. Neither label proves coherent ownership.

Average latency alone hides dependent misses, bandwidth saturation and tails. Architects must combine analytical models, cycle simulation, RTL/physical evidence, counters and representative applications.

## Prerequisites and Retrieval

Before studying this module, be able to:

- derive tag, index and offset geometry;
- trace set-associative hit, victim and refill behavior;
- distinguish write-through, write-back, allocate and bypass policies;
- compute conditional probability and weighted averages;
- explain basic coherent ownership and memory ordering.

Retrieve exact level capacities, line/sector sizes, associativities, banks and indexing; private/shared ownership; physical/virtual identity; tags, coherence/directory state and ECC; latency pipeline and clock crossings; lookup order and parallelism; inclusion/exclusion policy and victim handling; fill destination and promotion; write allocation, writeback path and dirty ownership; MSHR/fill/writeback/snoop queue depths; merge and replay rules; prefetch paths; coherence agents and directory coverage; maintenance/fence/persistence semantics; interconnect topology, credits and priorities; memory-controller mapping; reset/error/retry behavior; counters and trace definitions; simulator/RTL/SRAM/toolchain revisions; workloads, warm-up and measurement windows; silicon configuration and errata.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish local from global level hit/miss probabilities;
2. derive nested serial AMAT and state its assumptions;
3. trace demand, refill, eviction and writeback across several levels;
4. compare inclusive, exclusive and NINE relationships;
5. preserve dirty data and coherent ownership during back-invalidations and moves;
6. design same-block merging and finite miss/writeback resources;
7. explain critical-word-first, early restart and parallel lookup trade-offs;
8. model bandwidth, queueing and memory-level parallelism beyond AMAT;
9. verify hierarchy refinement, safety and conditional progress;
10. select a hierarchy using workload, protocol and physical evidence.

## Core Exposition

### Give every level a role

L1 generally prioritizes hit latency and bandwidth. Mid-level caches may isolate cores, absorb writebacks and reduce shared contention. An LLC may reduce memory traffic, hold directory information or provide shared capacity.

Names do not guarantee behavior. Document whether instruction/data paths are split, whether levels are private or shared, and which level owns coherence or persistence responsibilities.

### Use local probabilities correctly

An L2 local hit rate counts only requests that missed L1 and actually consulted L2. Its global contribution is the probability of reaching it multiplied by its local hit probability.

For a serial hierarchy, global outcome probabilities should sum to one. This provides a simple audit against mixing counter denominators.

### Derive nested AMAT

Start at the first lookup and add conditional downstream cost only on misses. With more serial levels, nest each subsequent hit time and miss probability.

State whether a reported hit time is total-from-request or incremental-after-prior-level discovery. Mixing these conventions double-counts latency.

### State the completion point

Miss penalty may end when the critical word is forwarded, the full line is installed, the instruction retires, or an ordered/persistent operation completes. These are different measurements.

Use the completion point appropriate to the claim and record outstanding background work such as remaining beats or dirty writebacks.

### Trace a read miss

An L1 miss allocates or merges tracking state, issues a request and may probe L2. An L2 hit returns the requested sector/line; L1 validates identity and permissions, installs permitted bytes and wakes dependents.

If L2 also misses, it tracks its downstream request. Responses must be matched to the original block, generation and destination even if other requests reorder.

### Trace a write miss

The hierarchy first applies memory type, coherence and allocation policy. A write-allocate path may obtain ownership and old bytes before merging the store; a full-line ownership write may avoid fetching unused bytes if the protocol proves coverage.

A bypass or no-allocate write still needs ordering and duplicate-state checks. Dirty ownership cannot be inferred from level position alone.

### Preserve dirty victims

An L1 dirty victim usually becomes a writeback or ownership transfer to L2. If L2 must evict another line to accept it, enough queue/resource space must exist before committing the upper eviction.

Retain victim address, data, mask, coherence state and error status until the receiving level accepts the defined obligation.

### Define inclusion precisely

Strict inclusion requires every upper valid block to be represented below. Some systems include tags/directory coverage without retaining identical data; say which property is intended.

An inclusive lower eviction cannot simply reuse its entry. It must identify sharers, issue required back-invalidations, collect acknowledgments and obtain any dirty/newer data.

### Handle inclusive back-invalidations

The lower level may choose a victim whose upper copy is dirty or actively used. Protocol state must prevent new access/ownership races while invalidation completes.

Only after all required responses and data transfers may the lower entry be safely replaced. Timeouts or errors need containment rather than data loss.

### Define exclusivity precisely

An exclusive data hierarchy aims to place a block in one related data array. On an upper miss/lower hit, promotion may swap the upper victim downward while moving the hit upward.

Transient duplication during movement can be legal if hidden and tracked. The permanent-state invariant and recovery behavior must be explicit.

### Understand NINE designs

Non-inclusive/non-exclusive means a lower copy may or may not accompany an upper copy. It avoids forced back-invalidations solely for inclusion and avoids mandatory swaps solely for exclusion.

Coherence still needs complete sharer/owner knowledge. NINE is not permission to lose track of private dirty data.

### Consider line-size differences

Levels may use equal lines, sectors or different transfer units. A larger lower line can supply several upper lines; a dirty upper subline must merge without corrupting siblings.

Track valid/dirty state at the granularity required by partial fills, coherence and writeback. Whole-line assumptions are unsafe when only sectors are current.

### Choose serial or parallel lookup

Serial lookup saves some energy because lower levels are accessed only after upper miss detection, but adds downstream launch latency. Parallel lookup can reduce miss latency but consumes bandwidth/energy on upper hits and complicates cancellation.

Specify when the lower request becomes irrevocable and how canceled responses release resources.

### Use critical-word-first carefully

Critical-word-first prioritizes the requested beat. Early restart wakes the requester once that beat is trustworthy, while remaining beats continue filling.

Per-beat validity, ECC, duplicate access, eviction and coherence behavior must prevent consumers from reading absent bytes or treating a partial line as complete.

### Make caches nonblocking deliberately

Nonblocking caches allow hits under miss and possibly miss under miss. MSHRs track block identity, dependents, requested bytes, permissions, destination and outstanding messages.

Same-block requests merge only when operations and permissions are compatible. Different-block requests need independent resources and fair arbitration.

### Size queues as a coupled system

MSHR count alone does not determine concurrency. Fill buffers, writeback queues, interconnect credits, downstream MSHRs and response slots can become the limiting resource.

Admission should reserve or prove access to resources needed for completion. Otherwise circular wait can arise when all entries await writebacks or responses that cannot be accepted.

### Avoid coherence deadlock

Demand, refill, writeback and snoop traffic may depend on one another. Separate virtual channels, reserved credits or carefully proven priorities break cycles.

Backpressure must never cause a cache to accept an obligation it cannot retain. Liveness claims require fairness assumptions about downstream service.

### Integrate prefetching

Prefetches can turn lower misses into hits, but they consume MSHRs, bandwidth and replacement capacity. Record useful, late, redundant and harmful prefetches at each level.

Demand should normally have a progress path when prefetch resources saturate. Prefetch coherence and fault behavior must follow the architecture.

### Integrate coherence directories

A shared level may act as a snoop filter or directory. Its metadata coverage can be logically separate from its data inclusion policy.

Directory eviction must preserve knowledge required to find upper sharers/owners, often by invalidating them or moving metadata to another structure.

### Handle aliases and translation

Upper caches may be virtually indexed while lower levels use physical identity. Translation, ASIDs and page offset constrain when lookups can start and how synonyms are prevented.

Every interlevel transaction must carry enough physical/context identity to avoid merging unrelated blocks.

### Define maintenance scope

Invalidate, clean and flush operations may target one level, a point of coherence or a persistence domain. Hardware and software must agree on which agents and levels participate.

Completion acknowledgment must not precede required writebacks, invalidations and ordered drains. Instruction/data coherence may add separate synchronization.

### Handle reset, power and errors

Reset sequencing must invalidate stale tags before service or restore protected state. Power-gated levels need retained or reconstructed coherence ownership.

ECC errors on dirty data require containment, correction or architected failure; silently dropping the only new copy is invalid. Retries must be idempotent or uniquely identified.

### Model traffic, not only hits

Count demand requests, refills, writebacks, probes, invalidation acknowledgments, prefetches, retries and transferred bytes. Two hierarchies with equal demand miss rate can impose very different downstream load.

Report useful bytes and line/protocol bytes separately. Inclusion, line size and write policy alter amplification.

### Model queueing and overlap

AMAT assumes a convenient expectation but does not capture independent overlap or saturation. A core may hide several misses yet stall completely on a dependent pointer chain.

Measure latency distributions, outstanding requests, queue occupancy, blocked cycles and bandwidth by request class. Use a queueing or cycle model only within validated assumptions.

### Separate latency from throughput

One request's service time differs from the hierarchy's sustained requests per cycle. Banking and ports may provide throughput without reducing isolated hit latency.

Conflicts, coherence and shared contention can reduce achieved throughput. Include per-bank utilization and unfairness.

### Account for physical implementation

Larger structures need longer wires, more banking, repeaters and pipeline stages. An architected cycle count that ignores SRAM macro and physical timing is provisional.

Evaluate tag/data arrays, muxing, crossbars, clock crossings, area, energy, thermal limits and frequency together with miss behavior.

### Partition shared capacity deliberately

Shared LLC capacity and bandwidth may be partitioned for isolation or quality of service. Way masks, coloring and allocation priorities change effective capacity and replacement eligibility.

Verify that reserved capacity cannot be consumed through transient entries, victim buffers or prefetch paths. Measure fairness and utilization trade-offs.

### Address security leakage

Shared tags, replacement, banks, MSHRs and interconnect queues expose timing contention. Partitioning or randomization changes but does not automatically eliminate leakage.

Threat-model attacker capabilities and validate isolation on the actual hierarchy, including speculative and maintenance traffic.

### Compare hierarchies fairly

Hold ISA, core, memory, compiler, workload inputs and completion criteria fixed. Record capacities, associativities, line sizes, policies, prefetchers, coherence, warm-up and random seeds.

Separate analytical predictions from simulation, RTL and silicon measurements. Explain counter denominators and sampling error.

### Verify refinement across levels

Use a shadow coherent memory model and scoreboards for every accepted operation. Assert identity, unique permitted ownership, byte correctness, no lost/duplicate response and ordered visibility.

Stress same-block races, back-invalidations, dirty movement, full queues, retries, ECC, reset and maintenance. Prove bounded-resource safety and conditional progress where tractable.

### Gather layered evidence

Begin with hand traces and executable arithmetic, then use a reference cache model, directed/random tests and formal properties. Run cycle simulation with traces and applications.

Finally assess SRAM mapping, synthesis, timing, power and hardware counters. Bind every result to revisions, configuration and known errata.

## Definitions and Notation

- `ti`: incremental hit/lookup time at level `i` under a stated serial model.
- `hi`: local hit probability among requests reaching level `i`.
- `mi=1-hi`: local miss probability at level `i`.
- `Gi`: global probability that an original access is served by level `i`.
- `tm`: additional main-memory service time in the elementary model.
- `AMAT`: expected access time over the defined request population.
- `Bi`: line or transfer bytes at level `i`.
- `Qi`: occupancy/capacity of a queue associated with level `i`.
- `MLP`: memory-level parallelism, the number of useful overlapping misses under a definition.
- `CPI`: cycles per instruction; cache effects may change its stall component rather than instruction count.
- `P99`: 99th-percentile latency for a specified request population.
- `owner(b)`: protocol state holding newest writable authority for block `b`.
- `copies(b)`: valid or transient representations of block `b` across levels/buffers.
- `complete(r)`: the documented completion predicate for request `r`.

For two serial cache levels, `G1=h1`, `G2=m1*h2`, and `Gmem=m1*m2`; these sum to one when every access follows that path. The elementary expression `AMAT=t1+m1*(t2+m2*tm)` excludes overlap, queueing, write traffic and coherence unless those effects are already embedded consistently in measured terms.

## Mechanisms, Invariants, or Proof Structure

1. **Identity obligation:** every request, transient entry, response and victim refers to the intended physical block and byte lanes.
2. **Decode obligation:** each level's index/tag/sector mapping reconstructs the same block identity.
3. **Qualification obligation:** only valid, complete-enough, permission-qualified data may satisfy an access.
4. **Data-refinement obligation:** loads return the newest bytes permitted by the coherent memory abstraction.
5. **Ownership obligation:** writers/dirty copies conform to the coherence protocol across all arrays and buffers.
6. **Inclusive obligation:** required lower representations cover upper copies, or an in-progress transition blocks unsafe eviction.
7. **Back-invalidation obligation:** a lower inclusive victim cannot disappear before all upper copies respond and dirty data is captured.
8. **Exclusive-move obligation:** promotion/demotion preserves exactly one stable data residence without a loss window.
9. **Transient-uniqueness obligation:** same-block misses merge/serialize and late responses cannot resurrect invalid state.
10. **Buffer obligation:** every accepted miss, fill and writeback fits retained state until exactly one terminal outcome.
11. **Ordering obligation:** stores, atomics, fences and device operations become visible in the required order.
12. **Maintenance obligation:** clean/invalidate/flush completion covers the documented levels and agents.
13. **Integrity obligation:** ECC/poison/retry/reset never turns untrusted or stale data into a valid response.
14. **Progress obligation:** under stated downstream fairness, arbitration and reserved resources prevent permanent circular wait.
15. **Measurement obligation:** local/global counters, timing endpoints, traffic and configurations match the reported claim.

A useful proof decomposition first establishes each cache/buffer as a data refinement of a single-block abstract state machine. Composition then proves ownership and message invariants across levels. Liveness is conditional on explicit fairness and bounded-retry assumptions. Performance is evaluated separately: it can choose among correct designs but cannot prove them correct.

## Alternatives and Trade-Offs

1. **One cache versus several:** fewer interfaces simplify control; more levels can reduce average latency and memory bandwidth.
2. **Private versus shared mid-level:** private capacity lowers local contention; shared capacity improves pooling and communication.
3. **Inclusive versus exclusive:** inclusion can aid filtering; exclusivity can increase effective data capacity but complicates movement.
4. **NINE versus strict policies:** flexibility avoids forced actions; metadata must still locate owners and sharers.
5. **Serial versus parallel lookup:** serial saves energy; parallel can reduce miss launch latency at higher traffic/cancellation cost.
6. **Equal versus mixed line sizes:** equal sizes simplify movement; sectors/larger lower lines exploit spatial transfer but add partial state.
7. **Blocking versus nonblocking:** blocking control is smaller; nonblocking execution exposes MLP but needs tracking and deadlock design.
8. **Full-line completion versus early restart:** full completion is simpler; early restart lowers dependent latency with beat-valid complexity.
9. **Writeback routing choices:** direct-to-memory can bypass shared pollution; through-LLC paths may simplify ordering/coherence.
10. **Victim cache versus larger associativity:** victim storage targets recent conflicts; more ways broaden placement at hit-path cost.
11. **Unified versus split L1:** unified capacity is flexible; split instruction/data caches provide independent bandwidth and policies.
12. **Banked versus monolithic levels:** banking scales throughput; bank conflicts and routing complicate latency.
13. **Directory with versus without data:** combined entries align capacity; decoupled metadata can preserve coverage independently.
14. **Hardware versus software partitioning:** hardware adapts quickly; page coloring can expose policy with coarser control.
15. **Average versus distribution targets:** AMAT is compact; percentiles and blocked-time distributions expose tails and QoS.

## Failure Modes and Misconceptions

1. “L2 hit rate is over all loads.” It is normally local to L1 misses unless explicitly global.
2. “Global hit rates add directly from local counters.” Each lower rate needs reach probability.
3. “Every hit pays every level's hit time.” Not in a serial hierarchy that stops on an upper hit.
4. “AMAT predicts application speedup exactly.” Dependencies, overlap, queueing and instruction mix intervene.
5. “A lower hit has fixed latency.” Banks, contention, arbitration and coherence create distributions.
6. “Duplicate blocks prove inclusion.” Inclusion is an invariant over all upper valid blocks.
7. “Inclusive eviction can discard clean upper copies silently.” They must be invalidated before the invariant/state is reused.
8. “An upper dirty copy is safe because the lower copy is clean.” The clean copy is stale and cannot replace the owner.
9. “Exclusive means coherence is unnecessary.” Other cores, DMA and transients still require ownership tracking.
10. “NINE means unconstrained.” It relaxes residence policy, not data/coherence obligations.
11. “A late fill is always useful.” It may be stale or canceled after invalidation, context change or newer ownership.
12. “More MSHRs always improve performance.” Other queues, bandwidth and dependencies can dominate.
13. “MSHR availability guarantees completion.” Fill/writeback/response resources and credits also matter.
14. “Backpressure cannot lose data.” It can if an obligation was acknowledged before storage was reserved.
15. “Writebacks are not on the demand path.” Full queues and victim dependencies can stall demand.
16. “Early restart completes the fill.” Remaining beats and integrity/coherence work remain outstanding.
17. “Parallel lookup is free latency.” It spends energy/bandwidth and requires cancellation correctness.
18. “Different line sizes only change bandwidth.” They change validity, merge, coherence and amplification granularity.
19. “An LLC directory entry can be evicted like data.” Sharer/owner coverage must be preserved.
20. “Prefetch hits are demand hits.” Their usefulness, timeliness and resource cost need separate counters.
21. “A flush of L1 flushes the hierarchy.” Architectural scope and persistence domain determine completion.
22. “ECC error on dirty data can invalidate the line.” That may destroy the newest copy.
23. “Average occupancy proves queues are sufficient.” Bursts and circular dependencies depend on maxima/tails.
24. “Higher LLC hit rate always helps.” Added hit latency, traffic, energy or harmful inclusion may outweigh it.
25. “Equal capacity makes comparisons fair.” Policies, latency, ports, prefetch, coherence and warm-up must also match.
26. “Simulator defaults are implementation facts.” Models and parameters require validation against the intended design.

## Worked Examples

### Example 1

With L1 local hit `0.92` and L2 local hit `0.75`, global outcomes are `0.92`, `0.08*0.75=0.06`, and `0.08*0.25=0.02`; they sum to one.

### Example 2

For `t1=1`, `m1=0.08`, `t2=6`, `m2=0.25`, `tm=80 ns`, nested serial AMAT is `3.08 ns`, not `1+6+80` and not a local-rate weighted sum over all accesses.

### Example 3

An inclusive LLC chooses block A while a private L1 holds dirty A. It marks the LLC entry transient, requests invalidation/data, waits for the owner response, then installs the new victim safely.

### Example 4

An exclusive L1/L2 promotion of B reserves an L2 destination for the displaced L1 block A before moving B upward; if reservation fails, neither stable residence changes.

### Example 5

Two loads miss on block C. The second merges into the first MSHR and records its dependent; one downstream request returns and wakes both exactly once.

### Example 6

A four-beat line returns its critical beat first. The dependent load restarts, but per-beat valid bits prevent another offset from reading the three absent beats.

### Example 7

All writeback entries are full while downstream waits for a snoop response. A reserved response/writeback path prevents the circular wait that unrestricted demand allocation could create.

### Example 8

Two designs have the same LLC demand miss count. One transfers twice the bytes because inclusive back-invalidations and large-line writebacks amplify traffic; hit rate alone hides the cost.

### Example 9

A pointer chase exposes nearly every miss latency while an independent array loop overlaps eight misses. Both can share the same AMAT inputs yet experience different stall time.

### Example 10

This deterministic calculation audits global probabilities, nested AMAT and the latency-only comparison with no L2.

<!-- bijux-verify: {"id":"multilevel-cache-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"global_l1=0.9200 global_l2=0.0600 global_memory=0.0200 probability_sum=1.0000\namat_with_l2_ns=3.0800 amat_without_l2_ns=7.4000 latency_model_speedup=2.4026\nrequests=100000 l1_misses=8000 l2_hits=6000 memory_requests=2000\n"}} -->
```python
t1_ns = 1.0
l1_miss = 0.08
t2_ns = 6.0
l2_miss = 0.25
memory_ns = 80.0

global_l1 = 1.0 - l1_miss
global_l2 = l1_miss * (1.0 - l2_miss)
global_memory = l1_miss * l2_miss
probability_sum = global_l1 + global_l2 + global_memory

amat_with_l2 = t1_ns + l1_miss * (t2_ns + l2_miss * memory_ns)
amat_without_l2 = t1_ns + l1_miss * memory_ns
speedup = amat_without_l2 / amat_with_l2

requests = 100_000
l1_misses = round(requests * l1_miss)
l2_hits = round(requests * global_l2)
memory_requests = round(requests * global_memory)

print(f"global_l1={global_l1:.4f} global_l2={global_l2:.4f} global_memory={global_memory:.4f} probability_sum={probability_sum:.4f}")
print(f"amat_with_l2_ns={amat_with_l2:.4f} amat_without_l2_ns={amat_without_l2:.4f} latency_model_speedup={speedup:.4f}")
print(f"requests={requests} l1_misses={l1_misses} l2_hits={l2_hits} memory_requests={memory_requests}")
```

The values are invented and assume serial fixed-latency reads without queueing, overlap, writes, prefetch, coherence or early restart. The result verifies arithmetic, not a real hierarchy.

## Cross-Program Connections

- **Probability and Statistics:** conditional rates and distributions turn local counters into global outcomes.
- **Algorithms:** online replacement, promotion and admission allocate scarce capacity without future knowledge.
- **Concurrent Systems:** MSHRs, queues and coherence messages require safety, ordering and progress.
- **Operating Systems:** page attributes, coloring, aliases and maintenance expose hierarchy contracts to software.
- **Distributed Systems:** ownership, invalidation, retry and exactly-once matching resemble replicated-state protocols.
- **Performance Engineering:** queueing, MLP, throughput and tails determine observed speedup.
- **Security Engineering:** shared capacity and queues create timing channels and denial-of-service surfaces.
- **Formal Methods:** refinement, invariants and fairness assumptions structure hierarchy verification.

## References

1. gem5, [Classic Caches](https://www.gem5.org/documentation/general_docs/memory_system/classic_caches/), current nonblocking cache, MSHR, write-buffer and port modeling; retrieved 2026-09-04.
2. gem5, [Replacement Policies](https://www.gem5.org/documentation/general_docs/memory_system/replacement_policies/), current replacement and insertion policy framework used across cache levels; retrieved 2026-09-04.
3. RISC-V International, [Cache Management Operations](https://docs.riscv.org/reference/isa/unpriv/cmo.html), current clean, invalidate, flush and ordering semantics relevant to hierarchy maintenance; retrieved 2026-09-04.
4. Intel, [Intel 64 and IA-32 Architectures Software Developer Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), current architectural cache, memory-type, ordering and maintenance context; retrieved 2026-09-04.
5. ChampSim, [ChampSim Repository](https://github.com/ChampSim/ChampSim), current trace-based multicore cache-hierarchy simulation framework and reproducibility context; retrieved 2026-09-04.
6. Valgrind, [Cachegrind Manual](https://valgrind.org/docs/manual/cg-manual.html), current cache simulation, hierarchy configuration and event interpretation; retrieved 2026-09-04.
7. Sarah L. Harris and David Money Harris, [Digital Design and Computer Architecture: RISC-V Edition Resources](https://pages.hmc.edu/harris/ddca/ddcarv.html), cache-hierarchy and AMAT teaching resources; retrieved 2026-09-04.

## Exercises

### Exercise 1

Derive local/global outcome probabilities and nested AMAT for a three-cache serial hierarchy, then identify which assumptions prevent direct application to an out-of-order core.

### Exercise 2

Design safe inclusive-LLC eviction states when an upper cache may hold a dirty copy and coherence messages may be delayed or retried.

### Exercise 3

Specify an exclusive L1/L2 promotion/demotion transaction that remains safe with full queues, same-block requests and errors.

### Exercise 4

Extend the executable model with request classes, latency samples and finite bandwidth; report mean, P99, traffic and blocked cycles.

### Exercise 5

Write a verification and measurement plan for selecting among inclusive, exclusive and NINE shared-cache organizations.

## Answers to the Exercises

### Answer 1

For local miss rates `m1,m2,m3`, outcomes are `G1=1-m1`, `G2=m1*(1-m2)`, `G3=m1*m2*(1-m3)` and `Gmem=m1*m2*m3`. With incremental serial times, `AMAT=t1+m1*(t2+m2*(t3+m3*tm))`; audit that the global outcomes sum to one.

An out-of-order core overlaps independent misses and other execution, while queues make service variable. Writes, prefetches and coherence add traffic; early restart changes the observed endpoint. Use the formula as a checked baseline, then a validated timing model and application stall measurements.

### Answer 2

Mark the LLC victim transient and block conflicting reuse; retrieve its directory sharers/owner; send invalidations or recall; retain retry identity; accept acknowledgments exactly once; capture and integrity-check dirty owner data; update coherent memory or the replacement destination; only then clear directory/data identity.

Reserve response and dirty-data capacity before starting. Merge or serialize same-block demands, reject stale-generation replies, contain timeout/ECC errors, and prove no lost newest bytes, no response duplication and conditional progress under network fairness.

### Answer 3

Before promotion, reserve the L1 target plus L2 space or a demotion buffer for the L1 victim. Lock both block identities, acquire required permissions, move/swap data with byte-valid and dirty state, then atomically expose the new stable locations. Release old entries only after destinations acknowledge.

Same-block requests attach to the transaction or wait; full resources prevent admission rather than partial movement. Responses carry transaction generations. On retry/error, retain one authoritative copy and either resume or roll back to a documented stable state.

### Answer 4

Create separate demand-read, writeback, prefetch and probe arrivals with service/priority rules and bounded queues. Record each request's arrival, service start, critical-word and full completion, transferred bytes and blocked cause. Validate zero-load latency against the analytical model and conservation against accepted/completed counts.

Report mean and P99 by class, throughput, occupancy distributions, admission blocks, useful/prefetch/coherence/writeback bytes and application-visible stall. State synthetic arrival distributions and avoid treating the queue model as hardware evidence.

### Answer 5

Use identical core, memory, capacity budget, line/sector sizes, prefetch, coherence, workloads, warm-up and completion rules. Verify identity, byte refinement, dirty ownership, inclusion coverage/back-invalidation, exclusive movement, NINE directory coverage, same-block races, finite queues, retries, maintenance, ECC and reset with reference models, assertions, formal properties and stress tests.

Measure demand misses, global outcomes, traffic by class, invalidations, writebacks, queue occupancy, latency distributions, MLP, stalls, fairness, leakage, area, timing and energy through simulation, RTL/SRAM implementation and hardware counters. Bind revisions and errata; internal evidence does not constitute independent architecture, coherence, security or silicon certification.
