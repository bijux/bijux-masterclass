---
module_id: OS-059
program: Operating Systems
level: 2
module_number: 59
title: TLB Shootdowns
status: complete
last_verified: 2026-09-04
---

# TLB Shootdowns

## One-Page Review

### Governing question

How should an operating system invalidate stale address translations across processors and devices after page-table changes so no observer can use revoked mappings, permissions, or memory while avoiding unnecessary interrupts, full flushes, refill work, and global synchronization?

### Essential definitions

- A **translation lookaside buffer (TLB)** caches virtual-to-physical translations and associated access attributes.
- A **shootdown** coordinates invalidation on processors that may retain a stale translation after a page-table change.
- An **address-space identifier (ASID)** or **process-context identifier (PCID)** tags translations so multiple address spaces can coexist in a TLB.
- A **local invalidation** affects the executing processor; a **remote invalidation** must affect another processor or translation agent.
- A **range invalidation** targets selected virtual pages; a **full invalidation** discards a wider context and causes collateral refill.
- **TLB gather** batches page-table removal, invalidation, and deferred freeing across a range operation.
- A **lazy TLB** state lets a processor retain an address-space context while it is not actively executing that address space under strict reuse rules.
- A **shootdown generation** records which invalidation epoch a processor or context has observed.
- An **MMU notifier** coordinates CPU page-table changes with secondary translation users such as devices.
- A **secondary TLB** is a translation cache outside the CPU MMU, such as an IOMMU or device address-translation cache.

### Central model, mechanism, or theorem

For address space `m` and change generation `g`, every processor or translation agent that could use an affected stale entry must either acknowledge invalidation through at least `g`, prove it never cached the entry, or be prevented from using the context until it performs the required invalidation. Only then may revoked access be considered effective and backing frames or page-table pages be reused.

Choose invalidation granularity by comparing targeted work with wider-flush collateral cost. A simple model compares `n*c_page` against `c_context+r*c_refill`, where `n` is pages invalidated, `c_page` targeted-invalidation cost, `c_context` context-flush cost, and `r*c_refill` estimated refill damage. Real decisions additionally include remote targets, page sizes, TLB levels, architecture, current contents, concurrent changes, and security urgency.

### Critical invariants

- A more restrictive permission, unmap, or remap is not externally complete while an affected observer can use an older translation.
- Page-table stores, visibility barriers, invalidation requests, acknowledgements, and memory reuse follow the architecture's required order.
- Target selection cannot omit a processor that can concurrently enter or continue using the affected address space.
- Each acknowledgement corresponds to the requested address space, range or context, and generation.
- A physical frame and page-table page are not reused until all relevant stale translations and walkers are excluded.
- Range and full invalidations cover every page size and translation level affected by the modification.
- CPU, IOMMU, and device translations are coordinated under their respective notifier and completion contracts.
- Failure, hotplug, virtualization, and timeout paths preserve safety rather than pretending a missing acknowledgement succeeded.

### Common failures

Common mistakes are editing a page table and assuming coherent data caches update TLBs, sending an IPI before the page-table store is visible, targeting only CPUs currently observed in user mode, reusing a frame before acknowledgements, batching across a point where revoked access must already be effective, invalidating base-page entries while overlooking a huge translation, flushing every CPU despite address-space residency evidence, using per-page invalidation for enormous ranges, using full flushes that destroy valuable unrelated translations, forgetting global kernel mappings, ignoring speculative walkers, omitting IOMMU or device caches, and reporting shootdown counts without wait time, target fan-out, refill cost, or workload impact.

### Compact example

Suppose a targeted invalidation costs 40 units per page. A context flush costs 500 units and is predicted to cause 64 refills at 8 units each, for 1,012 units. This toy chooses targeted invalidation for 1, 8, and 32 pages, and a context flush for 128 pages. The threshold is workload- and architecture-specific; the arithmetic does not model remote IPIs, huge pages, current TLB contents, or security ordering.

### Connections

[OS-031](031-address-translation.md), [OS-032](032-page-tables.md), [OS-033](033-translation-lookaside-buffers.md), [OS-037](037-copy-on-write.md), and [OS-058](058-timer-and-interrupt-scalability.md) connect shootdowns to translation, page tables, faults, mapping replacement, and interprocessor interrupts.

## Governing Question

Page tables live in memory, but processors do not consult them for every access. They cache translations and permissions in structures whose coherence rules differ from ordinary data caches. When the kernel revokes write access, unmaps a page, changes the physical target, or frees a page-table subtree, an old translation can remain usable elsewhere.

The governing question is how to establish that every relevant observer has crossed the invalidation boundary before the kernel exposes the new security or lifetime state. Efficiency then asks how to narrow targets, batch ranges, use hardware tagging, and avoid collateral refills without weakening that proof.

## Why This Matters

A missed shootdown can let a processor write through a read-only mapping, access memory after unmap, corrupt a frame reassigned to another object, or walk a freed page table. These are correctness and security failures, not merely stale performance data.

Over-invalidation is also costly. Each remote target may take an interprocessor interrupt, serialize execution, invalidate local translation state, acknowledge, and later refill page-table walks. Large machines amplify fan-out, while memory-management workloads can generate invalidations faster than cores retire useful work.

Modern systems add more agents. Devices can share process address spaces through IOMMUs, address-translation services, and process identifiers. Guests add virtual and nested translations. A correct protocol names every coherence domain rather than treating “the TLB” as one CPU-local cache.

## Prerequisites and Retrieval

Review [OS-004](004-interrupts-and-exceptions.md), [OS-021](021-critical-sections-in-the-kernel.md), [OS-022](022-spinlocks-and-interrupt-context.md), [OS-024](024-atomic-operations.md), [OS-031](031-address-translation.md), [OS-032](032-page-tables.md), [OS-033](033-translation-lookaside-buffers.md), [OS-034](034-demand-paging.md), [OS-035](035-page-faults.md), [OS-037](037-copy-on-write.md), [OS-038](038-memory-mapped-files.md), [OS-052](052-smp-kernel-synchronization.md), [OS-054](054-kernel-read-copy-update.md), and [OS-058](058-timer-and-interrupt-scalability.md).

Retrieve these distinctions:

- page-table memory and cached translations have separate visibility mechanisms;
- virtual address, address-space identity, page size, translation level, physical frame, and permissions jointly identify what becomes stale;
- making a mapping more permissive and revoking access can have different synchronization urgency;
- local invalidation does not automatically affect remote CPUs or device translation caches;
- an IPI delivery, handler completion, acknowledgement, and subsequent refill are distinct events;
- active-address-space tracking is an optimization whose races must preserve conservative targeting;
- removing a mapping, freeing a physical page, and freeing the page-table page are separate lifetime boundaries;
- batching reduces synchronization count but can delay the moment at which revocation becomes effective.

## Learning Objectives

After this module, you should be able to:

1. identify page-table operations that require local, range, context, global, device, or nested invalidation;
2. explain store, barrier, request, handler, invalidation, acknowledgement, and reclamation ordering;
3. design target tracking that remains correct across context switches, lazy states, hotplug, and concurrent entry;
4. choose page, range, context, ASID, and generation mechanisms from measured cost and architecture semantics;
5. batch unmap and permission changes without violating access-revocation or memory-reuse boundaries;
6. coordinate CPU TLBs with IOMMUs, device address-translation caches, guests, and hypervisors;
7. validate shootdown correctness and performance with traces, counters, adversarial races, and lifecycle tests.

## Core Exposition

### What a TLB caches

A TLB caches the result of translation: address-space identity and virtual page map to a physical frame plus access attributes. Implementations can have separate instruction and data structures, multiple levels, and entries for several page sizes.

Page-walk caches can retain intermediate page-table information as well. The architecture's invalidation operation defines which translation and walk state it covers; software must not assume one visible structure is the entire cache.

### Why ordinary coherence is insufficient

Cache-coherent page-table stores make new bytes visible to processors that read memory. They do not necessarily force processors to discard previously cached translations.

The invalidation protocol therefore couples data-memory ordering with architecture-specific translation maintenance. Both are required: invalidating before the new PTE is visible can allow a later walk to refill the old value.

### Changes requiring invalidation

Unmapping, remapping to another frame, revoking write or execute permission, clearing presence, changing memory type, splitting or collapsing huge mappings, and replacing page-table levels can invalidate cached meaning.

Some architectures permit more-permissive updates with lighter synchronization because stale restrictive entries merely fault or deny access. The generic kernel contract and architecture rules decide; applications cannot infer safety from the direction of one flag change.

### Address-space tags

ASIDs or PCIDs tag translations by address space, avoiding a full non-global flush on every context switch. Tag capacity is finite and identifiers are eventually reused.

Reuse requires a generation or explicit invalidation proving that entries from the prior owner cannot match the new owner. A tag value without its allocation epoch is not a globally unique address-space identity.

### Global mappings

Kernel mappings may be shared across address spaces or marked global so ordinary context switches retain them. Changing such a mapping can require broader invalidation than one user context.

Target scope follows where the mapping could be cached, not which user process initiated the change. Kernel text, direct maps, modules, and temporary aliases have their own update protocols.

### Local invalidation

A local invalidation instruction affects the executing processor under architecture-defined scope. It is sufficient only when no other processor or device can retain or acquire the affected translation.

Single-threaded address-space use does not automatically prove locality: the address space may have run elsewhere earlier, and lazy contexts or device attachments may persist.

### Remote invalidation

Software shootdown sends requests to relevant processors, commonly through IPIs. Each target enters a handler, validates the request, performs the required local operation, records completion, and returns.

The initiator waits when correctness or reuse requires synchronous completion. Asynchronous invalidation is safe only when a later barrier prevents affected access and reclamation until completion is established.

### Ordering the protocol

A restrictive update conceptually publishes the new page-table state, executes required barriers, initiates invalidation, and waits for relevant acknowledgements before allowing stale access or reuse.

Architectures specify exact barrier placement and invalidation sequences. Generic prose cannot replace their memory model, particularly for weakly ordered systems and break-before-make requirements.

### Target discovery

Sending every request to every processor is conservative and expensive. The kernel can track which CPUs have used an address space and target only that set.

Tracking must cover races with context switch. A CPU entering the address space either appears in the target snapshot before it can use stale state or detects an outstanding generation and invalidates before access.

### Active versus historical users

A CPU actively running an address space clearly needs consideration. A CPU that ran it earlier can still retain tagged entries even though it currently runs something else.

Historical residency can be ignored only if context switching, tag generations, or lazy-state rules prove old entries cannot be reused without checking the newer invalidation generation.

### Lazy TLB state

Kernel threads can borrow or retain an address-space context without actively executing its user code. This reduces context-switch overhead but complicates who may carry stale entries.

Lazy-state transitions participate in shootdown tracking. A CPU can drop the lazy context, invalidate immediately, or record that it must flush before returning to the address space.

### Generation-based invalidation

An address space increments an invalidation generation. Each CPU records the generation through which its local context is valid.

A currently active CPU can be interrupted promptly; an inactive CPU can lazily compare generations on next use and flush then, provided memory reuse and access are impossible meanwhile. Generation wrap and tag reuse require conservative handling.

### Page invalidation

A page-specific operation avoids destroying unrelated translations. It is attractive for a small change when the architecture's per-page instruction and IPI handler loop are cheap.

The operation must cover the mapping's actual page size and all relevant translation structures. One nominal base address can represent a huge mapping whose invalidation semantics are broader.

### Range invalidation

A range interface lets architecture code select an efficient operation for `[start,end)`. It may loop over pages, use range hardware, or choose a wider context flush.

Callers communicate the precise changed interval and mapping information. Off-by-one endpoints, overflow, alignment, and mixed page sizes can leave stale entries outside an incorrectly normalized range.

### Context invalidation

A context flush invalidates all translations for one address-space tag or current non-global context. It has nearly fixed instruction cost and can avoid a long page loop.

Collateral damage means unaffected hot entries must refill. The cost depends on actual TLB occupancy and workload locality, which software rarely knows exactly.

### Full and global invalidation

A full flush can discard multiple contexts or global state depending on architecture. It is a correctness fallback for broad changes and a performance hazard if used routinely.

Document exact scope: “full” can mean the current context, all non-global entries, all page sizes, or a wider architectural domain. Names alone are insufficient.

### Choosing granularity

Compare targeted instruction count with wider-flush instruction and refill cost. The threshold changes with TLB size, hierarchy, page size, microarchitecture, current occupancy, and workload.

Use architecture defaults and measure before tuning. A threshold learned from one CPU generation or microbenchmark does not generalize automatically.

### Batching and TLB gather

Unmapping a large interval one PTE at a time and synchronously shooting down each page multiplies IPIs and waits. A gather object records the range, removed page tables, and pages pending reclamation, then performs a combined invalidation.

Batch boundaries follow memory pressure, lock duration, range shape, revocation requirements, and allocation failure. Batching must never let a freed frame be reused while a stale mapping remains executable.

### Delayed reclamation

After page-table entries are cleared, physical frames and page-table pages can be queued until the invalidation barrier completes. This separates logical unmap from safe reuse.

The deferred list is bounded. Very large operations periodically flush and reclaim rather than retaining unbounded memory or locks until the end.

### Page-table page freeing

A hardware walker can be traversing a page-table page while software removes the parent entry. Clearing the parent alone does not prove every earlier walker stopped referencing the child.

Architecture and MMU-gather protocols establish the safe free point through invalidation, barriers, reference rules, or deferred reclamation. Reusing a page-table page too soon can turn a walk into arbitrary memory access.

### Concurrent page faults

A fault can race unmap, protection change, and shootdown. Page-table locks and VMA or address-space synchronization determine whether the fault installs a new entry, retries, or observes removal.

The invalidation range and generation must cover any entry installed under the old state. Selection based on an unlocked snapshot is revalidated before completion.

### Copy-on-write

A COW fault replaces a read-only mapping with a private writable frame for one address space. The old translation must not continue directing writes to the shared frame.

The sequence coordinates allocation, content copy, PTE update, invalidation as required, fault retry, reverse mappings, and old-page lifetime. Devices sharing the address space add notifier ordering.

### Permission revocation

Changing writable to read-only or executable to non-executable is security-sensitive. Completion means affected agents can no longer exercise the old permission, not merely that the PTE shows the new bits.

Batching may be allowed within a locked operation, but user-visible transitions and subsequent memory reuse wait for the documented invalidation boundary.

### Unmap and remap

Unmap removes accessibility, while remap can assign the same virtual address to a different frame. A stale entry after remap is especially dangerous because it reaches a valid but wrong object.

Use an invalidate-before-reuse sequence. Never rely on the new frame coincidentally remaining allocated to hide a stale mapping.

### Accessed and dirty bits

Hardware can update accessed or dirty state while software clears or samples it. Some operations invalidate so a future access sets the bit again; others use architecture-specific atomic helpers.

Reclaim and migration algorithms need an honest observation window. Losing a concurrent dirty update can corrupt data even when virtual-to-physical translation remains unchanged.

### Huge mappings

Huge pages reduce TLB pressure but expand the coverage of one entry. Splitting a huge mapping changes a higher-level leaf into a page-table subtree; collapsing performs the reverse.

Invalidation must remove stale huge and base-page interpretations under architecture rules. Range costs count translations and levels, not only bytes divided by the smallest page size.

### Kernel mapping changes

Kernel mappings can be accessible on many or all CPUs and may use global entries. Module loading, executable permission changes, direct-map updates, and memory hotplug can require cache and TLB coordination.

Kernel invalidation targets the actual shared mapping domain. Address-space residency optimizations for a single process do not necessarily apply.

### Instruction-cache interaction

Changing code mappings or writing executable content can require instruction-cache maintenance in addition to TLB invalidation on architectures without automatic instruction/data coherence.

Translation coherence does not prove instruction bytes are visible. Follow the architecture's cache-to-execution publication sequence.

### Shootdown IPIs

An IPI interrupts target work, executes a high-priority handler, and can serialize on shared request state or acknowledgement counters. Large target sets create a latency fan-out.

Batch address changes per target and avoid redundant requests. Handler work remains bounded because a shootdown storm can otherwise prevent the threads causing progress from running.

### Acknowledgement design

An acknowledgement proves a particular target passed the required invalidation point. A shared counter is simple and can become a contended cache line; per-CPU completion state distributes writes and costs scanning.

Tag acknowledgements by request or generation so a late completion cannot satisfy a newer shootdown accidentally. Memory ordering connects local invalidation to published completion.

### Concurrent shootdowns

Several threads can modify one address space or many address spaces simultaneously. Requests can merge only when their ranges, generations, urgency, and target semantics are compatible.

Serialization simplifies proof and can bottleneck. Parallel designs use per-address-space generations and per-CPU queues while preserving acknowledgement identity and bounded storage.

### Shootdown storms

Frequent protection toggles, allocator churn, mapping teardown, page migration, deduplication, sampling, and garbage collectors can generate repeated invalidations. More CPUs sharing one address space multiply targets.

Diagnose the producer and semantic need before tuning the handler. Larger batches, stable arenas, fewer permission changes, local address spaces, huge pages, or application redesign can remove work at the source.

### Affinity and target-set size

Restricting a process to fewer CPUs can reduce the address space's active target set, but may create load imbalance. Wide shared worker pools increase scheduling flexibility and invalidation fan-out.

Measure the whole service objective. Pinning solely to reduce shootdowns can lose more through queueing or NUMA pressure.

### NUMA effects

Remote IPI delivery, shared acknowledgement state, page-table memory, and subsequent page walks traverse topology. One initiator can wait for a slow or power-idle remote socket.

Hierarchical or clustered signalling can reduce shared contention on architectures that support it, but completion still covers every required target. Measure fan-out by topology.

### Device and IOMMU translations

Devices can cache translations through IOMMUs or address-translation services. CPU invalidation alone does not revoke DMA or device access.

MMU notifiers tell secondary users about invalidation ranges and boundaries. The sequence prevents a device from using an old mapping after a frame is freed or reassigned.

### Notifier ordering

Some changes require notifier invalidation while holding the page-table lock, especially when a backing page can be freed or a PTE changes to a different page. This prevents a device from observing an invalid intermediate order across addresses.

Other protection-only cases can defer completion to the range-end boundary under documented rules. Choose from the semantic hazard, not from a blanket performance preference.

### Pinned and device-owned memory

Long-term DMA pins can prevent unmap, migration, or reclamation rather than relying on shootdown alone. Device ownership transitions include DMA synchronization and completion.

A page being present in a CPU page table does not describe every physical reference. Track pins, mappings, IOMMU state, device queues, and memory ownership independently.

### Virtualization

Virtual machines can have guest virtual, guest physical, and host physical translation layers. Guest invalidation may trap, be paravirtualized, or use hardware invalidation mechanisms; host remapping can require nested-context invalidation.

Tag identities and generations exist at each layer. A guest acknowledgement cannot prove a host or device translation is gone unless the virtualization contract composes those boundaries.

### KPTI and context switching

Separate user and kernel page-table contexts can reduce exposure to speculative attacks while increasing context and tag complexity. PCID-like tags can preserve selected translations across switches.

Invalidation chooses the affected context or both where mappings overlap. Security mitigations and architecture errata can deliberately require broader flushes than a performance-only model predicts.

### Speculation and security

Architectures define what invalidation and barriers prevent architecturally and speculatively. Software cannot assume a removed PTE erases all microarchitectural traces or side channels.

Follow current mitigation guidance for the platform. Security-driven flushes have a different threat model from ordinary mapping coherence and remain explicit in evidence.

### CPU hotplug

An offlining CPU must stop entering user address spaces, drain pending shootdowns, leave active masks, and discard or make irrelevant its tagged translations before completion.

An online CPU initializes tag and generation state before executing address spaces. Races between target snapshots and hotplug use locks or lifecycle barriers that conservatively preserve coverage.

### Failure and timeout

A processor that does not acknowledge can indicate lockup, lost interrupt, virtualization delay, firmware stall, or broken hardware. Continuing to reuse memory would convert availability failure into corruption.

Escalate through diagnostics, watchdog, CPU quarantine, crash, or platform-specific recovery according to safety requirements. Timeouts report the exact missing target and generation.

### Observability

Record initiator, address space, generation, range, page sizes, operation reason, target count and topology, invalidation type, IPI send and handler times, acknowledgement wait, batching, and failures.

Correlate with page-table changes, faults, context switches, active CPU masks, device notifiers, TLB miss and walk counters, cache misses, scheduler delay, application latency, and memory reuse. Counter names and meanings vary by microarchitecture.

### Experiment design

Test one page, short and long ranges, whole contexts, mixed page sizes, huge split and collapse, permission tightening and relaxation, unmap, remap, COW, page-table freeing, device attachment, and kernel mappings.

Vary active CPU count, affinity width, sockets, power states, concurrent faults, concurrent shootdowns, hotplug, virtualization, and memory pressure. Separate direct invalidation time from later refill cost and application recovery.

### Assurance

Correctness tests attempt stale read, write, execute, DMA, and page-walk access after the declared completion boundary. Stress uses identifier reuse, delayed targets, concurrent entry, huge mappings, device notifiers, failure injection, and frame reuse.

Reviewers include MMU architecture, memory management, scheduler, interrupt, device and IOMMU, virtualization, security, performance, and operations specialists. Unsupported counters and hardware behavior remain explicit limitations.

## Definitions and Notation

Let `M` be address spaces, `C_m` processors that may use address space `m`, `D_m` secondary translation agents, `g_m` its invalidation generation, and `a_x(m)` the generation acknowledged by observer `x`. Reclamation after a restrictive change at generation `g` requires every relevant `x` either satisfy `a_x(m)>=g` or be unable to use the context until it invalidates through `g`.

For a range of `n` pages, let `c_page` be targeted invalidation cost, `c_context` wider flush cost, `r` predicted unrelated entries lost, `c_refill` mean refill cost, `k` remote targets, and `c_ipi(k)` signalling plus acknowledgement cost. A toy choice compares `n*c_page+c_ipi(k)` with `c_context+r*c_refill+c_ipi(k)`. Common terms can cancel in one request, but batching, topology, architecture and concurrent target changes make the real decision richer.

Invalidation completion, access revocation, frame reuse, page-table-page reuse, and secondary-device completion are distinct boundaries. A protocol states which boundary its acknowledgement proves.

## Mechanisms, Invariants, or Proof Structure

1. **Classify the change.** Identify address space, range, levels, page sizes, old and new frame, permissions, global scope, devices, and urgency.
2. **Publish safely.** Modify page tables under required locks and make stores visible with architecture-prescribed ordering.
3. **Capture targets.** Include active, historical, lazy, entering, device, virtual and lifecycle observers or prove why each is excluded.
4. **Choose granularity.** Select page, range, context or global invalidation from correctness scope and measured total cost.
5. **Batch legally.** Merge compatible changes while preserving every user-visible revocation and memory-pressure boundary.
6. **Deliver requests.** Send bounded, generation-tagged work through local operations, IPIs, hardware broadcast and notifier paths.
7. **Invalidate locally.** Cover translation levels, walk caches, tags, global state and architecture barriers required by the change.
8. **Acknowledge exactly.** Publish completion for the correct context, range and generation with ordered per-target evidence.
9. **Reclaim afterward.** Reuse frames and page-table pages only when CPU, device and walker access is excluded.
10. **Handle concurrency.** Revalidate faults, context entry, nested shootdowns, hotplug, tag reuse and failure without losing coverage.
11. **Measure total cost.** Include signalling, handler work, wait, collateral loss, refills, page walks and application service.
12. **Retain assurance.** Preserve architecture, topology, configuration, traces, stress results, failures, reviewers and limitations.

<!-- bijux-verify: {"id":"tlb-flush-granularity","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"full-flush-cost=1012\npages=1 targeted-cost=40 choice=targeted\npages=8 targeted-cost=320 choice=targeted\npages=32 targeted-cost=1280 choice=full\npages=128 targeted-cost=5120 choice=full\n","stderr":""}} -->
```python
targeted_cost_per_page = 40
context_flush_cost = 500
collateral_entries = 64
refill_cost_per_entry = 8
full_cost = context_flush_cost + collateral_entries * refill_cost_per_entry

print(f"full-flush-cost={full_cost}")
for pages in (1, 8, 32, 128):
    targeted_cost = pages * targeted_cost_per_page
    choice = "targeted" if targeted_cost < full_cost else "full"
    print(f"pages={pages} targeted-cost={targeted_cost} choice={choice}")
```

The executable example compares two fixed cost expressions. It does not execute invalidation instructions, send IPIs, inspect TLB contents, cover page sizes and levels, model concurrent processors or devices, establish architecture ordering, or recommend a production threshold.

## Alternatives and Trade-Offs

- Broadcast to all CPUs is conservative but scales poorly; residency targeting reduces fan-out and makes target tracking part of correctness.
- Immediate synchronous invalidation gives a simple revocation boundary but blocks the initiator; deferred generations reduce interruption and delay reuse.
- Per-page invalidation preserves unrelated entries but repeats instructions; a context flush is constant-time locally and causes collateral refill.
- Small batches bound revocation delay and memory retention but send more IPIs; large batches amortize signalling and increase lock, memory, and latency exposure.
- Shared acknowledgement counters are simple and contended; per-CPU generations distribute writes and require aggregation.
- Context tags avoid flushes on switches but require safe reuse and generation management; untagged switching is simpler and discards locality.
- Huge pages reduce translation pressure but make one stale entry cover more memory; base pages permit precise changes and use more TLB reach.
- Lazy invalidation avoids interrupting inactive CPUs but postpones completion; eager invalidation permits immediate reuse and disturbs more CPUs.
- Narrow process affinity reduces target sets but can increase queueing; wide affinity improves scheduling flexibility and shootdown fan-out.
- Page-table batching improves throughput but retains freed objects; immediate reclaim returns memory and synchronizes more often.
- Hardware range or broadcast invalidation reduces software loops but depends on platform semantics; software IPIs are portable within the architecture layer and costly.
- Device shared virtual memory simplifies programming but adds secondary coherence domains; pinned isolated buffers simplify invalidation and reduce flexibility.
- Coalescing concurrent shootdowns removes duplicates but complicates generation ownership; strict serialization simplifies proof and bottlenecks modifiers.
- Security-wide flushes reduce stale microarchitectural state but cost performance; narrow coherence flushes preserve locality and may not satisfy the threat model.

## Failure Modes and Misconceptions

- **“Coherent caches make TLBs coherent.”** Translation caches require their own maintenance protocol.
- **“Changing the PTE completes the unmap.”** Stale translations can remain usable.
- **“Sending an IPI completes a shootdown.”** Targets must execute and acknowledge the required invalidation.
- **“Only CPUs currently in user mode matter.”** Historical tagged or lazy contexts can retain entries.
- **“A CPU-mask snapshot cannot race.”** Context switches and hotplug can change membership concurrently.
- **“Page invalidation always covers huge mappings.”** Scope follows architecture and page-table level.
- **“Full flush is always safer.”** Correct scope can be achieved narrowly; wider operations add cost and still need proper ordering.
- **“Per-page flush is always faster.”** Large ranges can make instruction loops exceed collateral refill cost.
- **“Batching is only a performance choice.”** It changes revocation and reclamation timing.
- **“The physical page can be reused after clearing its PTE.”** CPUs, walkers and devices may retain access.
- **“CPU acknowledgement revokes DMA.”** IOMMU and device translations have separate completion.
- **“ASID values uniquely identify address spaces forever.”** Finite tags are reused under generations.
- **“Shootdown cost ends at the acknowledgement.”** Refill and page-walk cost follows later.
- **“Fewer shootdowns proves improvement.”** Larger flushes or delayed revocation can hide worse collateral cost.
- **“Timeout permits best-effort continuation.”** Memory reuse without coverage risks corruption and isolation failure.

## Worked Examples

### Example 1

A process loses write permission on a shared page. The kernel publishes the read-only PTE, invalidates every relevant CPU context, waits for acknowledgements, and only then reports revocation complete.

### Example 2

An address space has run on two of 256 CPUs. Residency tracking targets those two while generation checks prevent a third CPU from entering with stale tagged state during the request.

### Example 3

A large unmap gathers thousands of entries, issues bounded range flushes, and defers frame and page-table freeing until each batch's invalidation barrier completes.

### Example 4

A huge mapping splits into base pages. The protocol removes the higher-level leaf and invalidates stale huge translations before publishing or relying on the new subtree.

### Example 5

An inactive CPU retains a lazy address-space context. It records an old generation and flushes before next user execution, while frames remain unreused until that deferred guarantee is sufficient.

### Example 6

A COW fault installs a private writable frame. Invalidation prevents a stale writable or shared translation from directing later stores to the wrong physical page.

### Example 7

A device uses process-address-space translation. MMU notifier ordering invalidates the device cache before the old frame is reassigned to another tenant.

### Example 8

Thirty-two individual invalidations appear cheaper by instruction count but cause long IPI-handler loops across 128 CPUs. Measurement selects a context flush and includes subsequent refill cost.

### Example 9

A shootdown waits indefinitely for a virtual CPU descheduled by the host. Hypervisor-aware invalidation marks the virtual context stale and forces a flush before reentry under the virtualization contract.

### Example 10

CPU offlining races a target snapshot. The hotplug barrier either keeps the CPU targetable through acknowledgement or proves it cannot execute the context and discards its translation state before removal.

## Cross-Program Connections

[Computer Architecture](../../23-computer-architecture/ROADMAP.md) connects TLB hierarchy, page walks, ASIDs, invalidation instructions, barriers, caches, IPIs, speculation, and virtualization. [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) connects generations, acknowledgements, lock ordering, deferred reclamation, race analysis, and distributed barriers.

[Security Engineering](../../25-security-engineering/ROADMAP.md) connects permission revocation, isolation, stale-state threats, speculative behavior, device DMA, and assurance. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) contributes lifecycle hazards, failure response, cost models, verification and evidence. Within this program, [OS-058](058-timer-and-interrupt-scalability.md) covers IPI delivery and [OS-060](../ROADMAP.md) covers contention diagnosis.

## References

- Linux kernel documentation, [Cache and TLB Flushing Under Linux](https://docs.kernel.org/core-api/cachetlb.html), current page checked 2026-09-04. Page, range, address-space, kernel and cache-flushing interfaces, SMP scope and residency optimization.
- Linux kernel documentation, [The TLB on x86](https://docs.kernel.org/arch/x86/tlb.html), current page checked 2026-09-04. Individual versus full invalidation, collateral damage, tuning, tracepoints and refill measurement.
- Linux kernel documentation, [Architecture Page Table Helpers](https://docs.kernel.org/mm/arch_pgtable_helpers.html), current page checked 2026-09-04. Generic PTE and higher-level helper semantics, invalidation-related operations, huge entries and debug tests.
- Linux kernel documentation, [MMU notifier invalidation ordering](https://docs.kernel.org/mm/mmu_notifier.html), current page checked 2026-09-04. Secondary TLB correctness, notification under page-table locks, frame replacement, write protection and range completion.
- Linux kernel documentation, [Process Addresses](https://docs.kernel.org/mm/process_addrs.html), current page checked 2026-09-04. Address-space structures, VMA and page-table locking, fault interaction, read and write stability and iterator rules.
- Linux kernel documentation, [Memory Management APIs](https://docs.kernel.org/core-api/mm-api.html), current page checked 2026-09-04. MMU gather state, page-table removal, notifier APIs, huge-page operations, locking and reclamation interfaces.
- Linux man-pages project, [mprotect(2)](https://man7.org/linux/man-pages/man2/mprotect.2.html), current page checked 2026-09-04. Page protection changes, alignment, protection keys, errors and mapping behavior.
- Linux man-pages project, [munmap(2)](https://man7.org/linux/man-pages/man2/munmap.2.html), current page checked 2026-09-04. Mapping removal, page alignment, range semantics, errors and address-space effects.
- Linux man-pages project, [madvise(2)](https://man7.org/linux/man-pages/man2/madvise.2.html), current page checked 2026-09-04. Range advice, page discard, removal, protection-like behavior, huge pages and process-memory effects.
- Linux kernel documentation, [CPU hotplug in the kernel](https://docs.kernel.org/core-api/cpu_hotplug.html), current page checked 2026-09-04. Online masks, lifecycle state machine, callbacks, failure, synchronization and per-CPU teardown.

## Exercises

### Exercise 1

Design the shootdown protocol for changing a four-page range from writable to read-only while eight CPUs can execute the address space and one device uses shared virtual memory.

### Exercise 2

Compare page, range, context, global, eager and generation-lazy invalidation for small permission changes, large unmaps, kernel mapping changes, and inactive CPUs.

### Exercise 3

Specify safe MMU-gather batching for a terabyte unmap under memory pressure. Include locks, batch boundaries, huge pages, faults, acknowledgements, and reclamation.

### Exercise 4

Trace target discovery racing context switches, CPU hotplug, ASID reuse, and a delayed virtual CPU. State how no observer escapes an invalidation generation.

### Exercise 5

Build a verification and performance plan for a shootdown optimization. Cover stale access, CPU and device translations, fan-out, refill, failure, security, and reproducibility.

## Answers to the Exercises

### Answer 1

Lock the relevant address-space and page-table state, validate mapping identity and device attachment, then publish read-only PTEs for the entire range with architecture-required barriers. Capture a generation and a conservative target set covering active, historical and concurrently entering CPUs. Notify the device translation owner at the point required for permission revocation, enqueue generation-tagged CPU requests, perform local range or page invalidations, and wait for ordered acknowledgements from every required CPU and the secondary translation domain.

Only after completion may the API report that write revocation is effective. Concurrent write faults retry against the new state; no frame is replaced or freed in this case, but device writes must still be excluded. Test writes already in flight according to the architecture and device contract, CPUs switching in and out, delayed handlers, huge-page aliases, notifier failure and device removal. Preserve range, generation, targets, handler and device completion timestamps, barriers, faults and post-boundary attempted writes.

### Answer 2

One or a few base-page permission changes favor targeted invalidation when architecture instructions and refill avoidance beat handler loops. A range interface communicates intent and lets architecture code choose hardware range operations or a context flush. A large unmap often favors context invalidation plus gathered reclamation, while a kernel global mapping change can require a broader kernel or all-context scope that user residency masks cannot narrow.

Eager invalidation interrupts every currently or historically relevant CPU and permits a simple immediate reuse boundary. Generation-lazy invalidation avoids disturbing inactive CPUs, provided they cannot access or reuse the context before comparing generations and provided memory is retained until the deferred guarantee suffices. Global invalidation is a correctness fallback with high collateral damage. Every choice covers actual page sizes, walk caches, ASID reuse, devices and architecture barriers; measured instruction, IPI, wait and refill costs determine thresholds.

### Answer 3

Create an MMU-gather object tied to the locked address-space operation and current invalidation generation. Walk VMAs and page-table levels, clear entries under their proper locks, collect the exact normalized ranges, distinguish huge leaves and page-table subtrees, queue physical frames and table pages for later freeing, and revalidate concurrent fault state. Block or force faults to retry so no old-generation entry is installed outside the gathered range.

Set batch limits by deferred bytes, page-table pages, target count, lock hold time and latency. At each limit, publish stores, notify secondary MMUs in required order, invalidate CPUs and devices, wait for exact acknowledgements, then release only that batch's frames and page-table pages. On allocation or signalling failure, flush the current conservative range rather than dropping records. Memory pressure can shorten batches but cannot move reclamation before completion. Final teardown verifies no deferred objects, notifier ranges or unacknowledged generations remain.

### Answer 4

Context entry and target capture share a generation protocol. Before a CPU can use address space `m`, it publishes active membership or compares its local acknowledged generation with `g_m`; if stale, it invalidates before user access. The initiator increments and snapshots under ordering that ensures each racing CPU is either in the target set or sees the new generation. Leaving active state does not erase historical tagged state unless the context is flushed or lazy reuse remains generation-checked.

Hotplug either keeps an offlining CPU in the shootdown domain until pending generations complete or prevents further context use and discards its tags before removing membership. ASID reuse couples the numeric tag with an allocation generation and flushes every CPU that could retain the previous owner. A descheduled virtual CPU is marked stale in hypervisor-visible context state and must invalidate before reentry; if the contract cannot prove that, the initiator waits. Assertions and traces cover every interleaving and never convert delayed response into permission to reuse memory.

### Answer 5

First define exact completion claims for unmap, write and execute revocation, remap, frame reuse, page-table-page reuse, CPU tags, global mappings, device DMA and nested virtualization. Stress stale reads, writes, instruction fetch, DMA and walks immediately after each claimed boundary, including identifier reuse, huge aliases, concurrent faults, delayed IPIs, target entry and exit, hotplug, device reset, virtual-CPU descheduling and acknowledgement timeout.

Compare baseline and optimization across page counts, address spaces, active CPUs, sockets, affinity widths, page sizes, mapping operations, concurrent modifiers and memory pressure. Measure initiator time, target fan-out, IPI delivery, handler duration, acknowledgement wait, invalidation instructions, batch size, retained memory, TLB misses, page-walk duration, cache effects, faults and application latency. Preserve architecture, microcode, kernel, mitigations, topology, power state, virtualization, devices, workload, raw traces, counters, seeds, failures, reviewer roles and limitations. Fewer IPIs or lower direct time is insufficient if refill, stale access, retained memory or tail service worsens.
