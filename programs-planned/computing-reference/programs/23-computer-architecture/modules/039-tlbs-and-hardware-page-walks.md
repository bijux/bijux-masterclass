---
module_id: CA-039
program: Computer Architecture
level: 1
module_number: 39
title: TLBs and Hardware Page Walks
status: complete
last_verified: 2026-09-04
---

# TLBs and Hardware Page Walks

## One-Page Review

### Governing question

How can a processor cache virtual-to-physical translations and walk hierarchical page tables quickly while enforcing address-space identity, permissions, page size, accessed/dirty semantics, invalidation ordering, coherence and precise faults under speculation and concurrent page-table changes?

### Essential definitions

- A **translation lookaside buffer** (`TLB`) caches page-translation and permission metadata.
- An **instruction TLB** (`ITLB`) and **data TLB** (`DTLB`) serve instruction fetch and data access; a shared lower TLB may back both.
- A **virtual page number** (`VPN`) is the virtual address above the page offset.
- A **physical page number** (`PPN`) identifies the translated physical page frame.
- A **page-table entry** (`PTE`) contains a next-level table pointer or a leaf translation with permissions/status.
- A **page walk** reads successive PTEs from a root through indexed levels until a leaf or fault is found.
- An **address-space identifier** (`ASID`) or process-context identifier distinguishes translations for different address spaces.
- A **global mapping** is deliberately shared across eligible address spaces under architecture rules.
- A **superpage/huge page** is a leaf above the lowest walk level, mapping a larger aligned region.
- A **walk cache** caches intermediate page-table state or PTEs; it is not necessarily an architectural TLB.
- **accessed** and **dirty** (`A/D`) state records translation use/write according to the ISA/OS contract.
- A **TLB shootdown** coordinates invalidation of stale translations on multiple processors/threads.
- A **page fault** is an architecturally defined translation/permission/status failure attributed to an access.
- A **speculative walk** begins before the initiating operation is known to retire; it cannot expose an otherwise absent architectural effect.

### Central model, mechanism, or theorem

For a base page with `p` offset bits and `L` radix levels of `v` VPN bits each, a canonical virtual address decomposes into `VPN[L-1]...VPN[0]` and offset. On TLB hit, tag/context/page-size and permissions must match before combining cached PPN bits with the appropriate untranslated offset bits. On miss, the walker repeatedly computes `pte_addr = table_base + index*pte_bytes`, retrieves a coherent PTE, validates type/permissions/status/alignment, and either follows the next table or forms a leaf result. A cached result remains usable only while invalidation/version rules prove it current.

### Critical invariants

- Every TLB/walk entry is tagged with sufficient virtual, address-space, privilege, virtualization and page-size identity.
- A hit matches all required VPN bits and preserves the correct offset bits for its page size.
- Permissions, memory attributes, execute/read/write and user/supervisor rules are checked for the initiating access.
- Every PTE address is derived from the validated current table base, level index and PTE size without overflow.
- Nonleaf and leaf encodings, reserved bits and superpage alignment are validated exactly.
- Page-table reads observe the architecture's coherent/orderable view; stale walk data cannot bypass required invalidation.
- A/D updates are atomic/coherent according to the contract and never lose concurrent software changes.
- Invalidation/shootdown completion prevents subsequent use of targeted stale entries on every required observer.
- Speculative faults and PTE side effects become architectural only for the correct nonsquashed access.
- Walkers, miss queues and invalidation paths retain progress under finite resources and stated fairness.

### Common failures

Common failures include tagging only by VPN while omitting ASID/VMID, treating global as universally global, concatenating a superpage PPN without alignment checks, indexing a PTE with byte-offset bits, multiplying page-walk levels by memory latency without considering cache hits while claiming measured time, caching a nonleaf across page-table reuse without invalidation, racing A/D read-modify-write with the OS, acknowledging shootdown before remote invalidation, allowing a late walk to refill after invalidation, faulting a squashed speculative load, prefetching page tables across unsafe boundaries, flushing only one TLB level, and measuring TLB hit rate without page-size/walk-traffic context.

### Compact example

With 4 KiB pages, 8-byte PTEs and 512 entries/table, each level consumes 9 VPN bits. For virtual address `0x000000123456789a`, the page offset is `0x89a` and lowest-to-highest indices are 359, 418 and 72. In an invented timing model with one-cycle TLB lookup, three-cycle L1 data access, 95% TLB hits and three serial 50-cycle PTE accesses per miss, average translation-plus-data time is `1+3+0.05*150=11.5` cycles. A walk cache averaging 1.8 PTE accesses gives 8.5 cycles; neither is an implementation result.

### Connections

TLBs/page walks connect radix trees, caches, virtual memory, protection, context switching, coherence, atomic PTE updates, speculative execution, multicore interrupts, virtualization, memory encryption/tagging, performance counters and formal refinement.

## Governing Question

Virtual memory gives each execution context protected address spaces while caches and DRAM use physical identity. Translation sits on the latency-critical path and must be both cached and revocable.

The hard part is concurrency: software edits page tables while hardware caches and walks them; other cores may hold stale entries; speculative requests may disappear; accessed/dirty state may be updated by hardware. Speed cannot weaken the invalidation and permission contract.

## Why This Matters

A TLB hit can make translation nearly invisible. A miss may cause several memory accesses that themselves traverse caches and contend with demand. Huge pages can expand reach but increase allocation, fragmentation and invalidation granularity.

Incorrect context tags expose another process's memory. Incorrect shootdown lets freed/remapped pages retain stale access. Incorrect speculative fault handling changes program behavior.

Translation performance must include reach, page sizes, walk-cache behavior, PTE traffic and application locality, not only raw hit rate.

## Prerequisites and Retrieval

Before studying this module, be able to:

- split addresses into page number and offset;
- trace cache hits/misses and hierarchical memory latency;
- interpret radix-tree indexing and aligned tables;
- explain privilege, permissions and precise exceptions;
- reason about coherence, atomics and multicore synchronization.

Retrieve exact ISA/privilege/virtualization translation mode; virtual/physical width and canonicality; base/superpage sizes and level/index widths; PTE size/layout/reserved encodings; root/context registers; ASID/VMID/global rules and widths; ITLB/DTLB/shared-TLB geometry and replacement; permission/status checks; A/D behavior; walker width/queues/merge; PTE cacheability/coherence and walk caches; invalidation instructions, address/context scope and ordering; OS shootdown protocol; page-table allocation/reuse; fault priority/attribution; speculative behavior; nested translation; IOMMU interaction; counters/traces; core/RTL/OS/hypervisor/simulator revisions, mitigations and errata.

## Learning Objectives

After completing this module, you should be able to:

1. decompose virtual addresses for a radix page-table mode;
2. form PTE addresses at each walk level;
3. distinguish nonleaf, base-page and superpage leaves;
4. design TLB tags for context, page size and virtualization;
5. check permissions, status and physical-address validity;
6. integrate A/D updates with coherent concurrent software;
7. specify invalidation and multicore shootdown ordering;
8. prevent stale late-walk fills and speculative fault leakage;
9. model TLB reach, walk traffic, latency and finite resources;
10. verify translation refinement and performance evidence.

## Core Exposition

### Start from architectural translation

Translation maps a legal canonical virtual address and access context to a physical address, attributes/permissions or a precise fault. The page offset is normally untranslated for aligned pages.

Treat the ISA and platform translation mode as authoritative; similar-looking schemes differ in PTE bits, invalidation and A/D rules.

### Decompose the virtual address

For 4 KiB pages, the low 12 bits are the offset. A radix-512 table uses 9 index bits because 512 entries fit in one 4 KiB page when PTEs are 8 bytes.

Higher address bits may require canonical sign/zero extension. Reject invalid forms before unsafe table access.

### Locate the root

A privileged register or virtualization structure identifies the root physical page and address-space context. Validate alignment, mode and supported physical width.

Changing roots/context needs the architecture's synchronization. Pipeline state cannot silently use the old root under the new context.

### Compute a PTE address

At level `i`, select the corresponding VPN index and compute aligned table base plus `index*pte_size`. Check arithmetic and physical-address bounds.

Never use virtual addresses to read a physically addressed page table unless the architecture explicitly defines that mechanism.

### Distinguish nonleaf and leaf PTEs

A valid nonleaf points to the next-level table; a valid leaf supplies translation/permissions. Reserved combinations fault according to architecture.

Do not follow a leaf as a table or accept writable-without-readable encodings where forbidden.

### Form a base-page result

At the lowest-level leaf, combine the PPN with the original page offset. Verify physical width and page attributes.

The translation result includes permissions and memory type, not only an address.

### Form a superpage result

A higher-level leaf maps a larger page. Lower VPN fields become part of the physical page result while low PPN fields generally must meet alignment rules.

Misaligned superpage PTEs fault rather than alias multiple virtual regions unpredictably.

### Define TLB reach

Reach equals entries times covered page bytes, adjusted for associativity, page-size partitions and workload mapping. A 64-entry 4 KiB TLB nominally covers 256 KiB.

Nominal reach overstates useful reach under conflicts, mixed page sizes or context sharing.

### Tag context precisely

A TLB tag includes VPN bits plus ASID/PCID or equivalent, and virtualization may add VMID/nested context. Global mappings bypass only the context fields specified by the architecture.

Context identifiers can wrap/reuse; software must invalidate or version safely before reuse.

### Match variable page sizes

Entries need a page-size/level indication that determines which VPN bits compare and which offset/VPN bits pass through. Overlapping entries require deterministic architectural priority or prevention.

Assert that no two eligible entries create ambiguous different translations for one access.

### Check permissions on every hit

Cache sufficient PTE permission/status attributes and compare access type, privilege and architectural overrides. Execute, read and write are distinct.

Permission changes require invalidation. A cached physical address without current permission is not a valid hit.

### Separate ITLB and DTLB roles

Split first-level TLBs give fetch and data independent bandwidth/policies. A shared second-level TLB pools reach but adds latency and contention.

Instruction/data invalidation scope must reach every structure and queued result that can satisfy the targeted translation.

### Design replacement

TLB replacement affects miss rate, not translation correctness. Eligibility handles locked/global/wired/transient entries before LRU-like or random preference.

ASID and page-size partitioning influence conflicts. Measure per-context/page-size behavior.

### Merge same-page misses

Multiple misses for the same translation/context/access compatibility can share one walk and attach dependents. Stores may require dirty status or stronger permissions than loads.

Use exact tags/generations so unrelated contexts or invalidation epochs never merge.

### Cache intermediate walks

Walk caches store nonleaf PTEs or subtree pointers, reducing memory references. Entries require physical page-table identity, level, context/virtualization and invalidation semantics.

They can be stale even when no final TLB entry exists. Flush/snoop them according to the contract.

### Access PTEs through memory hierarchy

PTE reads may hit caches and contend with demand, prefetch, coherence and DRAM. A page walk is not necessarily `levels*DRAM latency`.

Page-table memory attributes and coherence determine visibility of software updates.

### Update accessed and dirty state

Architectures may set A/D bits in hardware, trap for software handling or use mixed rules. Hardware updates must be atomic/coherent with PTE modification.

Do not overwrite concurrent permission/PPN changes with a stale read-modify-write. Revalidate and retry as required.

### Preserve precise faults

Invalid/reserved PTEs, permissions, canonicality and physical faults have defined fault classes/priorities. Attribute fault address and access type to the initiating instruction.

Speculative walks may discover faults, but delivery waits until the instruction is architecturally eligible.

### Contain speculative effects

Squashed walks release resources and cannot install stale unauthorized translations. Cache/PTE traffic may remain microarchitectural and needs security analysis.

Architectural A/D side effects under speculation follow exact ISA rules; do not invent them from performance convenience.

### Order page-table updates

Software writes new PTE data with required memory ordering, executes architecture-specific invalidation/fences, and only then relies on new translations. Break-before-make rules may apply.

Hardware must not reorder stale TLB use beyond that synchronization contract.

### Implement local invalidation

Invalidation may target an address, context, page size, virtualization stage or all entries, with special global rules. Match scope exactly.

It must also cancel/version outstanding walks and dependent refill paths where required.

### Implement multicore shootdown

The OS identifies processors that might cache the mapping, sends requests, each performs required local invalidation/order, acknowledges, and the initiator waits before reusing memory or completing protection change.

An acknowledgment sent before local invalidation is globally effective violates the protocol.

### Prevent late refill

A walk begun before invalidation may return afterward. Associate epochs/generations, snoop invalidations or revalidate before fill so stale results cannot resurrect.

This applies to final TLBs, walk caches and queued translations.

### Handle page-table reuse

Freed table pages may become ordinary memory or new tables. Stale intermediate cache entries must not interpret reused contents under old identity.

Use invalidation, quiescence and allocation lifecycle appropriate to architecture/OS.

### Support virtualization

Nested translation composes guest virtual to guest physical and guest physical to host physical, potentially multiplying PTE references. Combined TLBs cache composed results with both contexts.

Invalidations from guest and hypervisor must target the appropriate stages/combined entries.

### Coordinate with IOMMUs

Devices may cache translations independently. CPU TLB shootdown alone does not revoke DMA mappings; IOMMU invalidation and device ATS caches may participate.

Ordering, completion and fault reporting cross interconnect/device boundaries.

### Integrate caches

Virtually indexed caches may begin alongside TLB lookup when index bits lie within the page offset. Physical tags/permissions must qualify the hit before architectural use.

Large caches or synonyms require coloring, alias detection or other design.

### Budget walk resources

Walkers need request slots, PTE-read MSHRs, response capacity and fault/completion queues. Reserve progress paths so walks and cache writebacks/coherence cannot deadlock.

Prioritize demand and bound speculative/prefetch walk occupation.

### Measure translation performance

Report ITLB/DTLB/lower-TLB hits/misses by page size and context, completed/merged walks, PTE references by cache level, A/D updates, invalidations and walk latency distributions.

Connect translation stalls to runtime; out-of-order execution can overlap some walks.

### Use huge pages deliberately

Huge pages increase reach and reduce walk depth/frequency, but require alignment/contiguous physical allocation and can increase fragmentation, migration and protection granularity.

Measure memory footprint, placement and shootdown effects alongside TLB benefit.

### Address security

TLB/walk timing, shared walk caches and page-table accesses can leak context or mapping information. Speculation can amplify observations even without architectural faults.

Partition/flush/tag state as threat model requires and validate mitigations on exact hardware/OS.

### Verify translation refinement

Compare each completed translation/fault with a reference page-table walk over coherent memory at the correct synchronization point. Assert tags, permissions, level/alignment and physical address.

Stress concurrent PTE changes, invalidations, ASID reuse, late responses, faults, full queues, virtualization and reset.

### Gather layered evidence

Use hand/executable decompositions, reference walkers, directed/random tests and formal invariants. Run OS tests for mapping/protection/shootdown and simulator workloads for performance.

Bind ISA mode, core RTL, firmware, hypervisor/OS, page sizes, simulator/hardware, mitigations and errata.

## Definitions and Notation

- `p`: base-page offset bits; base page bytes are `2^p`.
- `v`: VPN index bits per uniform radix level; entries/table are `2^v`.
- `L`: number of page-table levels.
- `VPN[i]`: index used at level `i`, with convention stated.
- `PPN`: physical page number from a leaf PTE.
- `pte_bytes`: encoded PTE bytes.
- `root`: aligned physical base of the first table.
- `pte_addr=table_base+VPN[i]*pte_bytes` for a direct radix level.
- `H`: TLB local hit probability under a defined request population.
- `A`: first-level TLB lookup time.
- `P`: conditional page-walk/additional penalty on a miss.
- `translation_expectation=A+(1-H)*P` in an elementary serial model.
- `reach=sum(entries_size*page_bytes_size)` only as nominal coverage before conflicts/context effects.
- `epoch`: invalidation/version state used to reject stale outstanding results.

Level numbering varies between architectures and texts. Always state whether level zero is the leaf or root and bind formulas to the selected mode.

## Mechanisms, Invariants, or Proof Structure

1. **Canonicality obligation:** accepted virtual addresses meet width/extension rules.
2. **Context obligation:** tags/root/walk state contain sufficient ASID/VMID/privilege/stage identity.
3. **Index obligation:** VPN/offset fields and PTE addresses are exact, aligned and nonoverflowing.
4. **PTE obligation:** validity, leaf/nonleaf, reserved bits and physical width are checked.
5. **Page-size obligation:** superpage alignment and offset substitution are exact.
6. **Permission obligation:** access type, privilege, status and memory attributes qualify every result.
7. **Coherence obligation:** page-table reads/A-D updates observe the required coherent ordered view.
8. **Atomicity obligation:** A/D changes cannot lose concurrent software PTE changes.
9. **Uniqueness obligation:** eligible TLB/walk entries do not produce ambiguous translations.
10. **Invalidation obligation:** targeted cached and outstanding results become unusable before completion acknowledgment.
11. **Speculation obligation:** squashed accesses expose no absent architectural fault/authorization.
12. **Fault obligation:** exact cause/address/access are attributed once to the correct instruction.
13. **Resource obligation:** accepted walks retain state/response capacity until completion.
14. **Progress obligation:** walks, invalidations and demand complete under stated fairness.
15. **Evidence obligation:** correctness/performance claims bind mode, contexts, page sizes, revisions and workload.

Refine TLB hits and walks to one architectural translation function over a synchronized page-table snapshot. Prove cached-result validity using context and invalidation epochs, then compose with coherent PTE memory and precise exception retirement. Progress depends on finite-resource and interprocessor fairness assumptions; performance requires empirical workloads.

## Alternatives and Trade-Offs

1. **Unified versus split TLB:** unified pools entries; split ITLB/DTLB provides bandwidth and policy separation.
2. **One versus multiple TLB levels:** one minimizes hit path; multiple levels extend reach with latency/complexity.
3. **Fully versus set associative:** full placement reduces conflicts; set associativity scales lookup energy/timing.
4. **ASID tagging versus flush-on-switch:** tags retain translations; flushing simplifies reuse at performance cost.
5. **Hardware versus software A/D:** hardware avoids traps; software offers policy/control with fault overhead.
6. **Hardware versus software walk:** hardware lowers common latency; software-managed misses expose flexible policy.
7. **Base versus huge pages:** base pages reduce fragmentation; huge pages extend reach/reduce walks.
8. **Walk cache versus larger TLB:** walk cache helps diverse final pages sharing prefixes; TLB directly hits repeats.
9. **Serial versus parallel cache/TLB lookup:** parallel lowers hit latency; it complicates qualification/energy.
10. **Eager versus lazy shootdown:** eager revokes promptly; lazy/versioned schemes reduce interrupts with lifecycle complexity.
11. **Broadcast versus tracked shootdown:** broadcast is simple; tracking targets likely holders.
12. **Merge versus independent walks:** merge saves traffic; compatibility/context checks add logic.
13. **Speculative versus retirement-triggered walks:** speculation hides latency; conservative triggering reduces side effects.
14. **Combined versus separate nested TLBs:** combined hits quickly; staged caches simplify invalidation ownership.
15. **Shared versus partitioned walk state:** sharing improves utilization; partitioning strengthens isolation/QoS.

## Failure Modes and Misconceptions

1. “A TLB caches only VPN-to-PPN.” It also carries page size, context, permission and attributes.
2. “Same VPN means same translation.” ASID/VMID/root/privilege stages differ.
3. “Global means all virtualization contexts.” Its scope is architecture-specific.
4. “Page offset indexes the page table.” VPN fields select PTEs.
5. “Any valid PTE is a leaf.” Leaf/nonleaf/reserved encodings matter.
6. “A high-level leaf concatenates its PPN unchanged.” Lower VPN bits substitute and alignment must hold.
7. “TLB reach equals entries times 4 KiB always.” Page sizes/partitions/conflicts change it.
8. “Permission checks happen only during walk.” Cached hits must enforce them too.
9. “PTE writes are immediately visible.” Ordering, coherence and invalidation are required.
10. “Flushing the L1 TLB is sufficient.” Lower TLBs, walk caches and outstanding fills may remain.
11. “Shootdown completes when an interrupt is sent.” Required observers must invalidate/order and acknowledge.
12. “A walk started before invalidation may refill.” It needs cancellation/version validation.
13. “ASID reuse is safe after changing root.” Stale tagged entries must be invalidated/versioned.
14. “A/D update is an ordinary stale writeback.” It must preserve concurrent PTE changes.
15. “Speculative page faults can be delivered early.” Squashed accesses cannot fault architecturally.
16. “Speculative walks have no effects.” Cache/A-D/security behavior requires exact analysis.
17. “Page walks always reach DRAM.” PTEs often hit caches or walk caches.
18. “Levels times memory latency is measured penalty.” Queueing/cache hits/overlap make it a model.
19. “More walkers always reduce stalls.” Cache/MSHR/bandwidth and dependencies can dominate.
20. “Huge pages are free reach.” Allocation, fragmentation and granularity costs matter.
21. “CPU invalidation revokes device DMA.” IOMMU/device translation caches are separate participants.
22. “Virtually indexed caches eliminate translation latency.” Physical qualification/alias rules remain.
23. “Translation miss rate predicts runtime.” Walk latency, overlap and instruction mix matter.
24. “Page-table prefetch is harmless.” It consumes translation/cache resources and may cross contexts.
25. “Simulator TLB defaults match hardware.” Geometry, modes and invalidation must be configured.
26. “Passing single-core tests proves shootdown.” Concurrent reuse and late-fill races require multicore stress/proof.

## Worked Examples

### Example 1

A 4 KiB page has 12 offset bits; an 8-byte PTE table occupying 4 KiB contains 512 entries and therefore uses 9 index bits.

### Example 2

For `0x000000123456789a`, offset is `0x89a`; lowest-to-highest 9-bit VPN indices are 359, 418 and 72.

### Example 3

A base-page TLB entry matches VPN and ASID, passes write permission and combines cached PPN with the original 12-bit offset.

### Example 4

A level-two leaf maps a superpage; nonzero prohibited low PPN fields cause a misaligned-superpage fault rather than silent masking.

### Example 5

Two loads to the same page/ASID miss together. One walker entry carries both dependents and returns/faults them according to access permissions.

### Example 6

Software clears write permission, orders the PTE store, shoots down remote CPUs and waits for acknowledgments before reusing the old physical page.

### Example 7

A walk response returns after shootdown. Its old epoch fails validation, so it is discarded instead of refilling stale access.

### Example 8

A speculative load encounters invalid PTE state but is squashed by a branch; the walker releases state and no architectural page fault is delivered.

### Example 9

A three-level walk has only 1.8 average PTE memory references because cached intermediate entries hit; calling it exactly three DRAM accesses would be false.

### Example 10

This deterministic decomposition and timing model audits radix indices and elementary hit/miss expectations.

<!-- bijux-verify: {"id":"tlb-walk-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"virtual_address=0x000000123456789a offset=0x89a vpn_indices_low_to_high=359,418,72\npage_bytes=4096 pte_bytes=8 entries_per_table=512 index_bits=9 levels=3\nbaseline_cycles=11.50 walk_cache_cycles=8.50 modeled_reduction_pct=26.09\n"}} -->
```python
virtual_address = 0x000000123456789a
page_bits = 12
index_bits = 9
levels = 3
mask = (1 << index_bits) - 1
offset = virtual_address & ((1 << page_bits) - 1)
indices = [(virtual_address >> (page_bits + index_bits * level)) & mask for level in range(levels)]

tlb_lookup = 1
data_access = 3
tlb_miss = 0.05
pte_access = 50
baseline_walk_accesses = 3.0
cached_walk_accesses = 1.8
baseline = tlb_lookup + data_access + tlb_miss * baseline_walk_accesses * pte_access
with_walk_cache = tlb_lookup + data_access + tlb_miss * cached_walk_accesses * pte_access

print(f"virtual_address=0x{virtual_address:016x} offset=0x{offset:x} vpn_indices_low_to_high={','.join(str(value) for value in indices)}")
print(f"page_bytes={1 << page_bits} pte_bytes=8 entries_per_table={1 << index_bits} index_bits={index_bits} levels={levels}")
print(f"baseline_cycles={baseline:.2f} walk_cache_cycles={with_walk_cache:.2f} modeled_reduction_pct={100 * (baseline - with_walk_cache) / baseline:.2f}")
```

The timing inputs are invented and assume serial fixed-latency PTE accesses without queues, overlap, faults, A/D updates or nested translation. The address decomposition follows the explicitly stated three-level 9-bit convention.

## Cross-Program Connections

- **Data Structures:** radix trees index page tables and translation caches.
- **Operating Systems:** allocation, permissions, ASID lifecycle and shootdown implement revocation.
- **Concurrent Systems:** PTE updates, walks and remote invalidations require ordering and progress.
- **Virtualization:** nested translation composes guest/host protection and invalidation.
- **I/O Systems:** IOMMUs and device translation caches extend address-space control.
- **Security Engineering:** stale/context-aliased/speculative translation creates isolation risks.
- **Performance Engineering:** reach, walk cache, PTE traffic, overlap and tails determine cost.
- **Formal Methods:** translation refinement, epochs and precise faults structure verification.

## References

1. RISC-V International, [Supervisor-Level ISA](https://docs.riscv.org/reference/isa/priv/supervisor.html), current page-based virtual-memory, PTE, translation and SFENCE.VMA semantics; retrieved 2026-09-04.
2. RISC-V International, [Machine-Level ISA](https://docs.riscv.org/reference/isa/priv/machine.html), current privilege, physical-memory and trap context relevant to translation; retrieved 2026-09-04.
3. Intel, [Intel 64 and IA-32 Architectures Software Developer Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), current paging, TLB, invalidation and protection architectural context; retrieved 2026-09-04.
4. Linux kernel, [Page Tables](https://docs.kernel.org/mm/page_tables.html), current multi-level page-table concepts and Linux software context; retrieved 2026-09-04.
5. Linux kernel, [x86 TLB](https://docs.kernel.org/arch/x86/tlb.html), current TLB flushing and performance-counter guidance; retrieved 2026-09-04.
6. QEMU, [RISC-V System Emulator](https://www.qemu.org/docs/master/system/target-riscv.html), current RISC-V machine/CPU virtualization model context; retrieved 2026-09-04.
7. Sarah L. Harris and David Money Harris, [Digital Design and Computer Architecture: RISC-V Edition Resources](https://pages.hmc.edu/harris/ddca/ddcarv.html), virtual-memory/TLB teaching resources; retrieved 2026-09-04.

## Exercises

### Exercise 1

Decompose several boundary virtual addresses for a three-level radix-512 mode and form PTE addresses, base-page results and aligned/misaligned superpage outcomes.

### Exercise 2

Design a multilevel TLB tag/data entry supporting ASIDs, global mappings, two page sizes and virtualization context without ambiguous hits.

### Exercise 3

Specify page-table update and multicore shootdown steps for permission removal and physical-page reuse, including late walks.

### Exercise 4

Extend the executable model with per-level cache hit probabilities, nested translation and finite walkers; report PTE traffic and latency distributions.

### Exercise 5

Write a verification/evaluation plan for a hardware page walker and TLB hierarchy integrated with an OS and hypervisor.

## Answers to the Exercises

### Answer 1

Mask the low 12 offset bits, then successive 9-bit VPN fields under the chosen low-to-high convention. Starting from the root, compute `base+index*8`, validate each PTE and follow aligned nonleaf PPN bases. At a lowest leaf, concatenate PPN/offset; at a higher leaf, substitute lower VPN fields and require prohibited low PPN fields zero.

Test zero/high canonical addresses, every index rollover, last PTE, physical overflow, invalid/reserved encodings and superpage boundaries. Reject noncanonical or misaligned outcomes exactly.

### Answer 2

Tag entries with selected VPN high bits, ASID unless architecturally global, VMID/stage/root generation as needed, and page-size/level. Data holds PPN plus read/write/execute, user, global, A/D and memory attributes. Page size controls comparison and physical substitution.

Assert one-hot-or-zero qualified hits, exact permission checks and no global escape beyond defined context. Define replacement eligibility and invalidation matching for address/context/stage/all scopes.

### Answer 3

Construct the new invalid/restricted PTE state, publish it with required memory order, issue architecture-specific local invalidation and send shootdowns to every possible holder. Each target orders prior page-table observation, invalidates final/walk caches and versions/cancels outstanding walks before acknowledgment. The initiator waits for all acknowledgments before reusing the physical page.

Late responses carry old epochs and are discarded. ASID/root reuse follows separate generation/invalidation rules. Device mappings require IOMMU/device-cache invalidation too.

### Answer 4

Represent each walk as ordered level accesses whose service may hit walk cache/L1/L2/memory probabilistically or from a deterministic trace. Nested translation turns guest PTE accesses into host-translated memory references; cache composed results explicitly. Bound walker/PTE MSHR queues and schedule arrivals.

Report final-TLB hits, merged walks, PTE references by level, queue/service/total latency, faults and traffic. Validate constant-latency/no-queue cases against the supplied expectation before adding overlap.

### Answer 5

Verify canonicality, root/context tags, index/PTE arithmetic, leaf/nonleaf/reserved handling, superpage alignment, permissions, physical width, A/D atomicity, coherent PTE reads, unique hits, fault priority, speculative squash, finite resources, invalidation scopes, epochs/late fills, ASID reuse, nested stages, reset and progress using reference walks, assertions, formal checks and concurrent OS tests.

Measure per-level/page-size/context hits, reach/conflicts, merged/completed walks, PTE cache/memory traffic, A/D work, invalidations, latency distributions and application stalls under base/huge pages and virtualization. Bind ISA mode, core RTL, firmware, hypervisor/OS, simulator/hardware, mitigations and errata; internal evidence is not external architecture, OS, security or silicon certification.
