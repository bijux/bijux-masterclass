---
module_id: OS-033
program: Operating Systems
level: 1
module_number: 33
title: Translation Lookaside Buffers
status: complete
last_verified: 2026-09-04
---

# Translation Lookaside Buffers

## One-Page Review

### Governing question

How can processors cache address translations for speed while operating systems preserve permission, mapping, address-space, and frame-lifetime correctness across CPUs and virtualization layers?

### Essential definitions

- A **translation lookaside buffer (TLB)** is a processor cache of virtual-to-physical translations and associated access attributes.
- A **TLB hit** supplies cached translation state; a **TLB miss** invokes a hardware or software refill path.
- **TLB reach** is the amount of virtual memory whose translations can be represented at once for a stated page-size and entry organization.
- An **address-space identifier (ASID)** or **process-context identifier (PCID)** tags translation state so multiple address spaces can coexist in caches.
- A **global translation** is designed to survive some address-space changes under architecture-specific rules.
- A **TLB invalidation** makes specified cached translation state unusable according to an architecture contract.
- A **TLB shootdown** coordinates invalidation on other processors that may hold affected translations.

### Central model, mechanism, or theorem

Model a cached entry as `E=(context,VPN,page_size,PFN,permissions,attributes,generation)`. It matches access `(c,v,op)` only if context rules match, `v` lies in its virtual range, and cached permissions authorize `op`. On a miss, the translation mechanism consults page tables or traps for refill.

After software changes authoritative mapping `T`, correctness requires every later access covered by the change to reject any stale `E` whose translation or permissions conflict. The update protocol orders page-table writes, targets every relevant CPU and translation stage, performs a sufficient invalidation, waits for required completion, and only then reuses frames, page tables, or context identifiers.

### Critical invariants

- Cached entries are keyed by the full architecture-defined context, including global and virtualization rules.
- A permission revocation or unmap completes before protected data or frames can be reused under the stronger claim.
- Invalidation scope covers the correct virtual range, page size, address-space identity, CPU set, and translation stage.
- Address-space identifiers are not reused for unrelated roots until stale tagged state is excluded.
- Page-size changes cannot leave simultaneously matching incompatible translations.
- Shootdown initiators and targets agree on request generation and completion before reclamation.
- Performance claims distinguish hits, misses, page walks, faults, invalidations, and scheduling effects.

### Common failures

Common mistakes are assuming PTE writes update TLBs, invalidating only the current CPU, flushing the wrong ASID, forgetting global or nested entries, reusing a PCID too early, invalidating one base address for a huge mapping without checking scope, freeing a page before shootdown acknowledgment, counting page faults as TLB misses, estimating reach as entry count times only one page size, and treating architecture event names as portable measurements.

### Compact example

An address space maps virtual page `V` to frame `A` on CPUs 0 and 1. The kernel replaces it with frame `B`. It prevents new users of `A`, atomically updates the PTE, orders the write, sends a range-and-context invalidation to both CPUs, and waits for acknowledgments. Only then can `A` be assigned to another security domain. If CPU 1 is omitted, it may keep writing `A` through its stale cached entry.

### Connections

[OS-031](031-address-translation.md) defines translation; [OS-032](032-page-tables.md) defines authoritative tables. [OS-034](../ROADMAP.md) uses misses and faults during demand paging, while [OS-036](../ROADMAP.md) creates invalidation pressure through replacement.

## Governing Question

Multilevel page walks can require several dependent memory accesses before the requested load or store. TLBs and page-walk caches make translation fast in the common case, but they replicate security-sensitive state outside memory-resident page tables.

The governing question is how software changes that replicated state safely. Updating one PTE is insufficient when other CPUs, cached walk intermediates, global entries, or nested translation stages can still authorize the old mapping. Safe design combines invalidation semantics, CPU tracking, generation, completion, and delayed reuse.

## Why This Matters

TLB behavior affects nearly every workload. Working sets with poor translation locality can spend substantial time walking tables. Huge pages can increase reach. ASIDs can reduce context-switch flushing. Batched invalidations can improve throughput.

Correctness failures can cross protection domains. A stale writable entry can modify a newly allocated object. A reused identifier can apply one process's translation to another. An incomplete guest-stage invalidation can expose migrated memory. These bugs are often rare because they require concurrency and reuse timing.

Optimization and safety therefore share the same model. The system must know where an address space ran, which translations may persist, and when reclamation becomes legal.

## Prerequisites and Retrieval

Recall cache locality, privilege, and memory ordering; review [OS-031](031-address-translation.md) and [OS-032](032-page-tables.md). Recall interrupt delivery from [OS-004](004-interrupts-and-exceptions.md) and synchronization from [OS-021](021-critical-sections-in-the-kernel.md).

Retrieve these distinctions:

- TLB entries and page-walk-cache entries are both cached translation information but may have different invalidation behavior;
- a miss is not necessarily a page fault, and a page fault is not necessarily a TLB miss metric;
- local invalidation and remote shootdown solve different scopes;
- ordering a PTE write and invalidating a translation are distinct steps;
- issuing a request and completing it on all target CPUs are distinct events;
- ASID tagging reduces flushing only while identifier ownership remains valid;
- reach, hit rate, walk cost, fault cost, and end-to-end latency are different measures.

## Learning Objectives

After this module, you should be able to:

1. explain TLB hits, misses, refill, reach, hierarchy, and page-walk caching;
2. model entries tagged by address-space and virtualization context;
3. classify mapping changes by required invalidation scope and completion;
4. design local invalidation, remote shootdown, ASID reuse, and delayed reclamation;
5. reason about huge pages, global mappings, nested translation, and speculative walks;
6. diagnose stale permissions, wrong-target flushes, shootdown storms, and measurement errors;
7. design architecture-scoped experiments and assurance evidence.

## Core Exposition

### What a TLB caches

A TLB entry usually combines a virtual page range, physical output range, permissions, and memory attributes. Its exact format is implementation-specific even when architectural behavior is specified. Separate instruction and data TLBs, multiple levels, and shared last-level structures are common possibilities, not portable guarantees.

Software reasons from architectural effects rather than presumed organization. A processor may cache intermediate walk results or invalid entries where permitted. It may evict entries at any time.

### Hit path

On a hit, cached translation and access checks avoid a full page-table walk. The physical address preserves the offset within the matched page size. A cached permission denial can fault without reading the current leaf again under the architecture's rules.

Hits make stale state dangerous: the processor may not observe a new PTE until software performs the required synchronization and invalidation.

### Miss and refill

On a miss, hardware-managed systems walk tables and may populate translation caches. Software-managed systems trap to a refill handler. A miss can complete successfully without an application-visible page fault if the authoritative mapping is valid and present.

A page fault occurs when translation or permission rules require architectural exception handling. Measurement tools and vendor events must be read carefully so walk activity, misses, completed walks, and faults are not conflated.

### TLB reach

For a fully utilized structure with entries `n_i` covering page sizes `P_i`, nominal reach is `sum(n_i*P_i)`. Set associativity, replacement, separate instruction and data structures, page-size partitions, conflicts, and workload locality reduce useful reach.

Huge pages increase bytes covered per entry but require alignment and can increase fragmentation or change invalidation cost. Report effective workload hit behavior, not nominal reach alone.

### Page-walk caches

Processors can cache upper paging-structure information independently of leaf translations. A PTE change may require invalidating derived walk state as well as a visible TLB entry. Architecture instructions define sufficient effects.

Do not write code to an assumed undocumented cache hierarchy. Use the architecture's page-table update and invalidation sequence, which may conservatively invalidate more than the requested entry.

### Context switches

Without tags, switching page-table roots commonly requires discarding address-space-specific translations. ASIDs or PCIDs let entries from several roots coexist and be selected by context identity. Global entries can survive certain switches.

Tags are finite. The allocator needs generations or flush-before-reuse. A numeric ASID can have hart-local, CPU-local, VM-local, or system-wide meaning depending on architecture and environment.

### Identifier allocation

Associate each address-space root with an identifier generation. When free identifiers remain, assign one and retain tagged state. When recycling, ensure all processors that could interpret the old identifier exclude its stale entries before using it for a new root.

Lazy schemes can advance a global generation and flush on each CPU when it next enters the new epoch. The proof must cover offline CPUs, migration, virtualization, rollover, and return from low-power states.

### Global mappings

Global mappings reduce repeated invalidation for kernel or shared translations, but their matching and invalidation rules differ from ordinary tagged entries. A context-specific invalidation may intentionally retain them.

Changing a global mapping therefore needs a global-capable invalidation scope. Overusing global state enlarges coupling and can retain sensitive translations longer than intended.

### Classifying updates

Installing a previously invalid mapping, making a mapping more permissive, revoking permission, changing physical output, changing page size, and removing a mapping have different risk. Some architectures allow deferring invalidation for changes that cannot create unauthorized access; others impose exact rules.

Centralize classification in reviewed helpers. Security-sensitive revocation and physical reuse take the conservative path when the architecture guarantee is unclear.

### Ordering and invalidation

First make the authoritative table transition with required atomicity. Then order explicit page-table writes before later implicit translation reads. Perform an invalidation that subsumes the affected address and context.

An invalidation instruction is not a generic full memory barrier unless the architecture says so. Additional ordering may be needed for data visibility, devices, or cross-CPU request metadata.

### Local invalidation

A local invalidation affects the executing processor or hart according to its instruction semantics. Scope may identify one address, one context, all nonglobal entries, or everything. Implementations may legally invalidate more than requested.

Choose the narrowest correct scope based on transition and measured cost. A narrow loop can be worse than one context flush for a large range.

### Remote shootdown

If an address space executed on other CPUs, they may hold stale translations. The initiator records the update, identifies targets, sends interprocessor requests, and waits for each required target to execute the appropriate local invalidation.

The request carries address range, context generation, and operation identity. Targets acknowledge only after the invalidation's architectural completion point. The initiator must handle CPU hotplug, concurrent migrations, duplicate requests, and target delays.

### CPU tracking

An address-space CPU mask can avoid sending to processors that never ran it or no longer can retain relevant state under a proven protocol. Incorrectly clearing the mask creates missed invalidations; never clearing it creates scaling cost.

Coordinate context switch and shootdown so a CPU cannot enter an address space between target enumeration and table change without seeing the new generation or participating in invalidation.

### Batching and ranges

Unmapping many pages one at a time can cause a shootdown per page. Batch PTE changes, accumulate a range, and issue one sufficient invalidation when frame reuse can wait. Batching reduces interrupts and fences but delays memory return.

Architecture thresholds decide when per-page invalidation becomes more expensive than a range or whole-context operation. Tune with workload evidence and preserve worst-case correctness.

### Lazy invalidation

Some changes permit deferred invalidation if physical frames and permissions are not reused in a way that makes stale access unsafe. A generation check on context entry can perform the pending flush.

Lazy does not mean omitted. Track obligations durably through scheduling and CPU state changes. Reclamation waits until every relevant observer crossed the required generation.

### Frame reuse

Unmapping removes the authoritative leaf, but a stale TLB entry can still address the frame. Do not allocate that frame to another protection domain until all required shootdown completion and other references are resolved.

This is a security invariant, not only a memory-management optimization. Delayed-free queues often couple frame reclamation to invalidation completion.

### Page-size transitions

Promoting base pages to one huge mapping or splitting a huge mapping can temporarily create overlapping candidates. Architectures prescribe clearing, invalidating, and installing sequences to prevent unpredictable selection.

Invalidate a scope that covers all translations derived from the old page size. One virtual address can represent a much larger cached entry than the base page.

### Instruction and data sides

Some processors separate instruction and data translation structures and caches. Making new executable code visible can require data-cache cleaning, instruction-cache invalidation, and translation synchronization in a specific order.

Do not assume coherent data caches imply coherent instruction fetch or translation. Use platform code-publication interfaces.

### Nested translation

Virtualization introduces guest virtual, guest physical, and host physical stages. Hardware may cache intermediate or combined translations tagged by guest and host identities. Guest PTE changes and hypervisor second-stage changes require different fences.

Migration, dirty logging, memory ballooning, and device assignment can create frequent nested invalidations. Scope includes virtual machine identity and stage, not only guest virtual address.

### IOMMU translation caches

Devices and IOMMUs can cache DMA translations. CPU TLB invalidation does not automatically invalidate device translation caches. Drivers and IOMMU code follow separate invalidation queues and completion rules.

Before freeing or repurposing a DMA page, wait for both translation invalidation and outstanding transactions. Device failure and timeout need containment policy.

### Speculative walks

Architectures can permit speculative translation-table reads and caching within defined constraints. Software must not reclaim table memory merely because no architecturally completed access is visible.

Broad fences may terminate or wait for launched walks. Use the architecture contract rather than assuming speculative activity cannot outlive a PTE change.

### Shootdown storms

Large mapping churn across many CPUs produces interprocessor interrupts, serialization, and wait time. Allocator behavior, garbage collectors, database mappings, and security mitigations can amplify this cost.

Mitigations include batching, larger mappings, per-CPU data, reducing shared address-space breadth, lazy safe invalidation, and avoiding needless permission toggles. Each changes memory, latency, or complexity trade-offs.

### Side channels

Translation timing can reveal address-space activity, page presence, or contention. ASID retention and shared structures create microarchitectural sharing. Exact attacks and mitigations depend on processor and threat model.

Do not expose physical mapping information broadly. Evaluate partitioning, flushes, page-fault behavior, and timer access as part of layered side-channel defense.

### Measuring TLB behavior

Use microbenchmarks that sweep working-set pages and access patterns to locate changes in effective reach, then validate with application workloads. Separate warm hits, cold walks, faults, and shootdowns. Randomized page order reduces ordinary data-cache and prefetch confounds but does not eliminate them.

Hardware performance events are model-specific. Record event definitions, counter constraints, multiplexing, sampling, kernel mode, page size, affinity, frequency, NUMA, and raw results.

### Observability

Track invalidations by scope, pages changed, targets, acknowledgment latency, batching, identifier rollover, deferred frees, faults, walks, huge-page transitions, and CPU migrations. High-percentile shootdown time can reveal stalled targets.

Instrumentation adds interrupts and cache traffic. Compare traced and untraced runs and avoid exposing sensitive address or process information.

### Security and assurance

Audit every mapping transition from authoritative PTE through all translation caches to physical reclamation. Verify target enumeration, context identity, global and nested scope, completion, and failure behavior.

Tests inject migration, concurrent unmap, identifier rollover, huge split, CPU hotplug, and target delay. Formal state models can help, but hardware conformance and human review remain necessary. No benchmark certifies invalidation correctness.

## Definitions and Notation

Let cached entry be `E=(c,V,P,F,perm,attr,g)`: context `c`, virtual base `V`, page size `P`, frame base `F`, permissions, attributes, and generation `g`. It matches address `v` when context rules match and `V<=v<V+P`; output is `F+(v-V)` if access is permitted.

For structure classes `i` with `n_i` entries of page size `P_i`, nominal reach is `R=sum(n_i*P_i)`. Useful reach `R_u` depends on associativity, partitions, replacement, conflicts, and workload and is established empirically.

For shootdown generation `q`, target set is `S_q` and acknowledgment set `A_q`. Reclamation that depends on the shootdown is permitted only when `A_q` covers `S_q` under a protocol that prevents a new unflushed entrant.

## Mechanisms, Invariants, or Proof Structure

A reviewable translation-cache protocol follows ten obligations:

1. State architecture, translation stages, cache-visible context, and global rules.
2. Classify the mapping or permission transition and stale-state hazard.
3. Publish authoritative table state with required atomicity and ordering.
4. Select an invalidation covering virtual range, page size, identity, CPU set, and stage.
5. Coordinate context switches and target enumeration against new entrants.
6. Wait for required local and remote completion before permission claims or reuse.
7. Manage finite ASID or PCID allocation, generations, rollover, and CPU locality.
8. Handle huge transitions, speculative walks, nested tables, and device caches separately.
9. Bound shootdown frequency, batching delay, deferred frees, and target stalls.
10. Measure hits, walks, faults, and invalidations with model-specific evidence labels.

The executable model calculates nominal reach and shows that one huge-page entry can cover the same bytes as many base-page entries.

<!-- bijux-verify: {"id":"toy-tlb-reach","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"base-reach-kib=256\nhuge-reach-mib=8\ntotal-reach-mib=8.25\nbase-entries-per-huge=512\n","stderr":""}} -->
```python
base_entries = 64
base_page = 4 * 1024
huge_entries = 4
huge_page = 2 * 1024 * 1024

base_reach = base_entries * base_page
huge_reach = huge_entries * huge_page
total_reach = base_reach + huge_reach

print(f"base-reach-kib={base_reach // 1024}")
print(f"huge-reach-mib={huge_reach // (1024 * 1024)}")
print(f"total-reach-mib={total_reach / (1024 * 1024):.2f}")
print(f"base-entries-per-huge={huge_page // base_page}")
```

The toy computes nominal capacity only. It omits associativity, conflicts, separate TLBs, walk caches, replacement, faults, invalidations, and workload behavior.

## Alternatives and Trade-Offs

- Untagged context switching simplifies identifier management but discards useful translations.
- ASIDs and PCIDs retain translations but require safe finite-identifier reuse.
- Narrow invalidation preserves unrelated entries but can cost more across large ranges.
- Whole-context invalidation is simple but increases later misses and walks.
- Synchronous shootdown simplifies reclamation but exposes target stalls to the caller.
- Deferred invalidation can batch work but delays frame reuse and complicates generations.
- Huge pages increase reach but enlarge fragmentation and transition scope.
- Global mappings reduce repeated refill but couple address spaces and require broader revocation.
- Busy working-set tuning can improve hits while masking security, NUMA, or application costs.

## Failure Modes and Misconceptions

1. **“The TLB is the page table.”** it is cached derived translation state.
2. **“Every miss is a page fault.”** a valid walk can refill without a fault.
3. **“Writing the PTE updates the TLB.”** stale cached state may remain.
4. **“A local flush updates all CPUs.”** remote holders require shootdown or a proven exclusion.
5. **“ASID values are globally unique.”** scope and reuse rules are architecture-specific.
6. **“Acknowledging an interrupt means invalidation finished.”** acknowledgment must follow the architectural completion point.
7. **“One-page invalidation always covers a huge mapping.”** scope must account for old page size.
8. **“Unmapped frames can be reused immediately.”** stale entries can retain access.
9. **“Global mappings follow ordinary context flushes.”** many context operations intentionally preserve them.
10. **“More nominal reach guarantees more hits.”** conflicts and workload locality matter.
11. **“Huge pages only reduce misses.”** they alter allocation, fragmentation, copy, and invalidation.
12. **“CPU flushes cover DMA.”** IOMMU and device caches have separate protocols.
13. **“Event names are portable.”** hardware counter semantics vary by model.
14. **“A fast benchmark proves safe shootdown.”** timing does not establish target and reclamation correctness.

## Worked Examples

### Example 1

Sixty-four 4 KiB entries provide 256 KiB nominal reach. Four 2 MiB entries add 8 MiB. Effective reach can be lower because the workload conflicts within sets.

### Example 2

CPU 0 unmaps a page used on CPU 1 and flushes locally. CPU 1 retains the old writable translation. Target tracking and acknowledgment are required before frame reuse.

### Example 3

An ASID wraps and is assigned to a new root without excluding the old generation. Cached entries from the prior process match. Flush-before-reuse or per-CPU generation checks prevent it.

### Example 4

A mapping becomes read-only. The kernel delays invalidation, then gives the frame to a different tenant. A stale writer corrupts it. Security-sensitive reuse cannot precede completed revocation.

### Example 5

A thousand-page unmap sends one shootdown per page. Range batching reduces requests, but physical pages stay on a deferred list until the batched invalidation completes.

### Example 6

Base mappings promote to a huge leaf while stale base entries remain. Overlapping matches can select incompatible translations. Use the architecture's page-size transition sequence.

### Example 7

A CPU migrates into an address space during target enumeration. The context-switch path compares generations and flushes before use, preventing it from becoming an untracked stale holder.

### Example 8

A hypervisor changes second-stage mapping but issues only a guest first-stage fence. Combined stale translation remains. Invalidate the correct guest and host context and stage.

### Example 9

A profiler reports many page faults and labels them TLB misses. Faults include demand events; TLB misses can refill without faults. Use documented architecture events and controlled workloads.

### Example 10

A shootdown target is delayed in a long nonpreemptible section. The initiator's high-percentile unmap latency rises. Observability ties wait time to the target CPU and request generation.

## Cross-Program Connections

[Computer Architecture](../../23-computer-architecture/ROADMAP.md) develops cache hierarchy, MMUs, performance counters, and virtualization. [Security Engineering](../../25-security-engineering/ROADMAP.md) frames stale translations, identity reuse, isolation, and timing leakage.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies replicated-state, hazard, performance, and assurance reasoning. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) connects mapping churn and shootdowns to runtime isolation and fleet performance.

Within this program, [OS-031](031-address-translation.md) and [OS-032](032-page-tables.md) provide authoritative translation state; [OS-034](../ROADMAP.md), [OS-035](../ROADMAP.md), and [OS-036](../ROADMAP.md) create misses, faults, and invalidations.

## References

- Linux kernel documentation, [Cache and TLB Flushing Under Linux](https://docs.kernel.org/next/core-api/cachetlb.html), current page checked 2026-09-04. TLB abstractions, whole, address-space, range, and page invalidation, SMP scope, and CPU-mask optimization.
- Linux kernel documentation, [Page Tables](https://docs.kernel.org/mm/page_tables.html), current page checked 2026-09-04. MMU translation, TLBs, page-walk caches, hierarchy, faults, permissions, and huge pages.
- RISC-V International, [Supervisor-Level ISA](https://docs.riscv.org/reference/isa/priv/supervisor.html), current specification checked 2026-09-04. Address-translation caches, ASIDs, global entries, speculative walks, `SFENCE.VMA`, and page-size transitions.
- RISC-V International, [Hypervisor Extension](https://docs.riscv.org/reference/isa/priv/hypervisor), current specification checked 2026-09-04. Guest translation contexts, `HFENCE.VVMA`, `HFENCE.GVMA`, and two-stage invalidation.
- RISC-V International, [SBI RFENCE Extension](https://docs.riscv.org/reference/sbi/v3.0/ext-rfence.html), version 3.0 checked 2026-09-04. Remote instruction and translation fences, hart masks, address ranges, ASIDs, and errors.
- Intel, [Intel 64 and IA-32 Architectures Software Developer's Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), revision page checked 2026-09-04. TLB and paging-structure caching, PCIDs, global translations, invalidation instructions, and virtualization.
- Arm, [Learn the architecture: Memory management](https://developer.arm.com/documentation/101811/latest/), current documentation checked 2026-09-04. TLB organization concepts, ASIDs, VMIDs, translation maintenance, barriers, and context.
- Linux man-pages project, [perf_event_open(2)](https://man7.org/linux/man-pages/man2/perf_event_open.2.html), current page checked 2026-09-04. Hardware event interfaces, groups, sampling, multiplexing, permissions, and limits.
- Russ Cox, Frans Kaashoek, and Robert Morris, [*xv6: a simple, Unix-like teaching operating system*](https://pdos.csail.mit.edu/6.1810/2025/xv6/book-riscv-rev5.pdf), MIT, 2025 edition. Teaching RISC-V translation, `satp`, `sfence.vma`, context switches, page-table changes, and process isolation.

## Exercises

### Exercise 1

Calculate nominal and effective TLB reach for mixed page sizes, then design a workload that exposes conflicts rather than only capacity.

### Exercise 2

Specify a two-CPU unmap and frame-reuse protocol. Include PTE ordering, target tracking, context generation, acknowledgment, migration, and timeout.

### Exercise 3

Design a finite ASID allocator with rollover. Cover per-CPU scope, offline CPUs, lazy generation checks, global entries, and proof of safe reuse.

### Exercise 4

Construct a fair experiment comparing base and huge pages. Separate data caches, TLB misses, walks, page faults, promotion, fragmentation, and shootdowns.

### Exercise 5

Build an assurance review for nested translation invalidation. Cover guest and host stages, VM identity, devices, migration, evidence, and human review.

## Answers to the Exercises

### Answer 1

Sum `n_i*P_i` for each page-size class to obtain nominal reach, but document separate instruction, data, and hierarchy assumptions. For 64 base entries and four 2 MiB entries, reach is 256 KiB plus 8 MiB. Effective reach is measured with a pointer-chasing or randomized page sequence whose data footprint per page is small and whose working-set pages sweep beyond capacity.

Vary virtual coloring or set-index-relevant bits to compare well-distributed and adversarial placements. Pin the thread, pre-fault pages, separate cold and warm runs, control NUMA and huge-page policy, and record documented walk and miss events plus latency. Data-cache misses, prefetch, frequency, and counter multiplexing remain confounds to quantify.

### Answer 2

Lock or version the mapping, prevent an untracked new entrant, atomically clear the PTE, and apply the architecture's ordering before invalidation. Snapshot CPUs that may retain the address-space generation, including CPU 0 and CPU 1, and send a request containing range, old page size, context ID and generation, and shootdown sequence.

Each target executes a sufficient local invalidation and acknowledges after architectural completion. Context switch checks generation so migration during enumeration either joins the target set or flushes before access. The initiator retains the frame on a deferred list until all required acknowledgments and other mapping or pin references are resolved. Timeout invokes containment or escalation; it never silently reuses the frame.

### Answer 3

Maintain an allocation generation and per-CPU observed generation because identifier meaning may be CPU-local. Assign unused IDs freely. On exhaustion, advance generation and mark old IDs unavailable for unrelated roots until each relevant CPU performs a generation flush excluding nonglobal stale translations. A CPU entering an address space compares its observed generation and flushes before loading the recycled identifier.

Offline and low-power CPUs follow the platform's teardown or resume flush contract before rejoining. Rollover cannot alias an unobserved old generation; use sufficient generation width or a synchronized global reset. Global mappings are managed separately and are invalidated when their content changes. VMIDs and nested stages use independent identities and fences.

### Answer 4

Use identical application semantics and mapped bytes. Pre-fault for steady hit and walk tests, then separately measure first-touch, promotion, split, copy-on-write, and memory-pressure regimes. Sweep working-set size and access pattern with fixed CPU affinity and NUMA placement. Include fragmentation and compaction scenarios, mapping churn, and multiprocessor unmap.

Record page sizes actually used, TLB and walk events with vendor definitions, data-cache behavior, faults, CPU, memory waste, throughput, p50 through high-percentile latency, promotion and split time, invalidation count, targets, and shootdown delay. Preserve hardware, microcode, kernel, mitigations, frequency, counter scheduling, and raw samples. Restrict conclusions to tested systems.

### Answer 5

Model guest virtual-to-guest physical and guest physical-to-host physical entries, ASIDs, VMIDs, global state, combined caches, and device translations. For each guest or host change, identify affected stage, virtual and physical range, page size, vCPU and host CPU set, and architecture fence. Migration advances VM generation and excludes stale execution on source and destination before memory reassignment.

Device assignment adds IOMMU invalidation and outstanding DMA completion. Fault injection covers vCPU migration during shootdown, host CPU hotplug, identifier rollover, huge split, delayed target, invalidation queue failure, and device timeout. Preserve architecture revisions, hypervisor configuration, traces, and raw latency. Named CPU, hypervisor, kernel, device, security, migration, safety, and independent-verification reviewers assess assumptions and residual risk. No counter result alone proves correctness.
