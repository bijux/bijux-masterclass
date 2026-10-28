---
module_id: OS-084
program: Operating Systems
level: 2
module_number: 84
title: Virtual Memory for Guests
status: complete
last_verified: 2026-09-04
---

# Virtual Memory for Guests

## One-Page Review

### Governing question

How can a hypervisor give each guest a convincing physical-memory abstraction while the host retains ownership, isolation, reclamation and migration control?

### Essential definitions

- A **guest virtual address** (GVA) is interpreted by guest-controlled stage-one translation.
- A **guest physical address** (GPA) names the machine-address space presented to the guest.
- A **host virtual address** (HVA) names backing memory in a host process when that architecture uses one.
- A **host physical address** (HPA) identifies actual platform memory after host translation.
- **Two-stage translation** composes guest GVA-to-GPA mapping with monitor GPA-to-HPA mapping.
- A **shadow page table** encodes guest and host constraints into a hardware-walkable derived mapping.
- A **memory slot or region** associates a GPA range with backing, attributes and lifecycle.
- **Dirty tracking** records guest writes for migration, snapshots, display or replication.

### Central model, mechanism, or theorem

The guest owns its virtual-to-guest-physical policy; the monitor owns guest-physical-to-host-resource authority. Hardware nested translation or software shadowing composes them. An access succeeds only when every required stage, permission, memory attribute and ownership check permits it. Changes in guest tables, host mappings, device mappings or lifecycle generations must invalidate every derived translation before stale access can outlive authority.

### Critical invariants

- No guest translation reaches host memory outside that guest's current allocation.
- Effective access is no broader than any contributing translation stage.
- RAM, MMIO, reserved holes and aliases agree across CPU, device and migration views.
- Host mapping changes invalidate secondary translations before memory reuse.
- Dirty state is not cleared until its data is captured under the tracking protocol.
- Reclaimed, ballooned, unplugged or migrated pages have one owner at every instant.
- Page-size, NUMA and sharing optimizations never weaken isolation or coherence.

### Common failures

An implementation injects a guest page fault for a stage-two denial, reuses a host page before secondary-TLB invalidation, maps one alias cacheable and another device-like, clears dirty bits while a vCPU writes concurrently, treats ballooned pages as zeroed without proof, or completes migration while device DMA can still dirty source memory.

### Compact example

Stage one maps GVA page 0 to GPA page 5 with read/write permission. Stage two maps GPA page 5 to HPA page 40 as read-only for dirty tracking. A read reaches HPA; a write exits at stage two even though the guest page table permits it. The monitor records the write and applies its tracking policy rather than blaming the guest OS.

### Connections

Guest memory connects MMUs, page faults, TLBs, host virtual memory, NUMA, IOMMUs, device models, snapshots, live migration, confidential computing and memory-pressure policy.

## Governing Question

A guest operating system expects to allocate physical frames, edit page tables, change permissions and handle faults. Yet its “physical” frames are resources owned and possibly moved, shared, swapped or transmitted by the host. The governing question is how to preserve the guest's architectural contract while retaining complete host authority over backing and lifecycle.

## Why This Matters

Memory translation is on nearly every instruction's critical path. Nested page walks, TLB misses, invalidations and NUMA placement can dominate performance without producing VM exits. At the same time, one stale translation can become a cross-tenant memory breach. Correctness and speed therefore depend on carefully composed hardware and software state.

Production requirements extend beyond translation. Hosts overcommit memory, deduplicate identical pages, track writes, take snapshots, migrate VMs, assign devices and support memory hotplug. Confidential guests may deliberately remove host access to private pages. Each feature changes who can map a page and what must be synchronized before ownership changes.

## Prerequisites and Retrieval

Before studying this module, be able to:

- walk multilevel page tables and explain TLB fill, permission checks and invalidation;
- distinguish virtual, physical and device-visible addresses;
- explain hardware-assisted virtualization, memory slots and VM exits;
- reason about copy-on-write, demand paging, NUMA and host memory reclaim;
- describe DMA, IOMMU translation, snapshots and live migration.

Retrieve the exact guest and host page-table formats, processor and microcode, hypervisor, host kernel, VMM, memory backend, machine type, IOMMU, guest firmware and migration protocol. Record base and huge page sizes, NUMA topology, dirty-log mode, memory-locking policy, sharing policy, confidential-guest mode and assigned devices.

## Learning Objectives

After completing this module, you should be able to:

1. trace GVA, GPA, HVA, HPA and IOVA translations without collapsing their owners;
2. compare shadow paging and hardware two-stage translation;
3. compose permissions, attributes, faults and accessed/dirty state correctly;
4. design mapping-change and secondary-TLB invalidation protocols;
5. evaluate huge pages, NUMA, overcommit, ballooning, swap and deduplication;
6. reason about dirty logging, snapshots, pre-copy and post-copy migration;
7. integrate DMA and confidential-memory ownership into the memory model;
8. test translation, lifecycle, pressure and migration boundaries adversarially.

## Core Exposition

### Name every address domain

Write the complete path for each actor. A guest CPU may use GVA to GPA to HPA. A hosted VMM may map GPA to HVA, while the host MM maps HVA to HPA. A device may issue an IOVA that an IOMMU maps to HPA. Nested guests add further guest-controlled stages. “Physical address” without an owner is ambiguous.

### Define the guest physical map

The machine type determines RAM ranges, firmware regions, MMIO windows, reserved holes and hotplug capacity. This layout is guest ABI: firmware tables, device bars and operating-system assumptions depend on it. Migration must recreate the same visible map even if destination backing differs.

### Register backing deliberately

Memory slots or regions associate non-overlapping GPA ranges with host backing and flags. Anonymous pages, files, huge-page files, shared memory and protected guest memory have different allocation and migration semantics. The region owner must stay alive while CPU or device translations can refer to it.

### Separate allocation from residency

Declaring 64 GiB of guest RAM does not prove 64 GiB is resident or physically allocated. Demand paging may instantiate pages on first access; sparse files may lack blocks; shared pages may have multiple mappings. Capacity policy must distinguish configured, committed, resident, pinned, dirty and reclaimable bytes.

### Compose stage-one and stage-two translation

Stage one implements the guest OS's address-space policy. Stage two restricts GPAs to host-owned pages. A hardware walker can cache the composite result in a TLB. Failure at either stage retains distinct cause and ownership, even when one guest access triggers several memory references for page-table walks.

### Understand shadow paging

When hardware cannot directly walk every required stage, the monitor constructs shadow mappings that encode guest translation plus host ownership. Guest page-table writes, control changes and invalidations must update or invalidate shadows. Write protection can expose changes but creates exits; unsynchronized shadows can reduce exits under a defined reconciliation protocol.

### Compose permissions without widening

Effective read, write and execute permission is constrained by every stage. Architecture-specific rules also combine privilege, execute-never, memory type and page-table-walk permissions. A writable guest PTE cannot override read-only stage two. Conversely, stage two permitting write does not override a guest read-only mapping.

### Preserve accessed and dirty semantics

Processors may set access and dirty bits in guest or nested tables, sometimes through hardware-managed updates. The guest expects its architectural bits; the host may separately need dirty state. Write protection, hardware dirty bits and dirty rings have different races and costs. Never conflate guest A/D state with migration evidence.

### Attribute faults by stage

A stage-one fault normally belongs to the guest and is injected with guest-visible syndrome. A stage-two fault reaches the monitor because backing is missing, protected or MMIO. A stage-two fault during a stage-one page-table walk carries different context from a final data access. Preserve addresses, access type and walk metadata.

### Treat page-table walks as memory access

Walkers read guest page-table pages through host-controlled translation and may write accessed or dirty metadata. Those accesses can fault, cross page sizes and interact with protection. An emulator that reads backing directly can bypass guest permissions or report the wrong fault order.

### Tag and invalidate TLB state

ASIDs, VMIDs or equivalent tags let translations coexist. Tags are finite and reusable. Mapping removal, permission reduction, memory-type change and owner reassignment require scope-correct invalidation plus completion barriers. Reuse cannot begin while any CPU or device retains the old translation.

### Synchronize host MM changes

Host copy-on-write, unmap, page migration, swap and reclaim can change HVA-to-HPA backing while guest translations exist. MMU-notifier-style protocols tell secondary MMUs to invalidate. When an old page can be freed or a mapping points to a new page, ordering must prevent a secondary walker from reaching reused memory or observing inconsistent updates.

### Preserve alias and memory-type consistency

Two GPAs can intentionally alias one backing object, and devices may view the same memory. Conflicting cacheability or access attributes can produce architecture-dependent behavior. Track alias relationships and restrict mappings to combinations the platform defines. Migration must preserve alias identity, not serialize two independent copies.

### Choose page sizes as a coupled policy

Large pages improve TLB reach and reduce walk depth. They require aligned contiguous backing and compatible guest mappings, and can be split by dirty logging, write protection, copy-on-write or memory pressure. Small pages enable fine-grained migration and reclamation. Measure the whole lifecycle rather than boot-time TLB reach.

### Align guest and host geometry

A large guest page backed by scattered small host pages may not yield a large stage-two entry. Memory-slot boundaries and unaligned backing can prevent promotion. Reserve geometry deliberately when large-page behavior is a requirement, and expose fallback rather than assuming configuration produces hardware entries.

### Place memory by NUMA ownership

vCPUs, guest memory, device queues and host threads should reflect intended NUMA locality. First-touch placement can follow an accidental launcher CPU. Automatic migration can help or create churn. Record node residency, remote-access events and vCPU movement before attributing latency to guest code.

### Budget overcommit explicitly

Overcommit improves utilization when guest working sets do not peak together. It converts host pressure into reclaim, swap, balloon requests or termination. Admission needs a model for committed, resident, pinned and nonreclaimable memory plus correlated bursts. A configured-memory sum is neither demand nor safe capacity.

### Use ballooning as cooperation

A balloon driver allocates guest pages and reports their GPAs so the host can reclaim backing. The guest decides which pages to surrender under its own policy. Inflate and deflate protocols require ownership and zeroing rules. Host reclamation without guest knowledge can cause double paging and opaque latency.

### Understand host swapping and double paging

If the host swaps a page the guest believes resident, the guest cannot choose its victim or observe the cause directly. The guest may simultaneously swap another page, multiplying I/O. Host swap can protect availability under mild pressure but becomes unpredictable under sustained overcommit, especially for latency-sensitive VMs.

### Treat deduplication as shared state

Same-page merging replaces identical private pages with one write-protected page and copies on write. It can save memory while adding scan cost, reverse mappings and COW latency. Cross-tenant content sharing can alter timing and side-channel analysis, so sharing policy belongs to the threat model, not only capacity tuning.

### Optimize zero and copy-on-write pages carefully

Read-only zero pages and template-backed pages reduce startup allocation. The first write allocates private backing and must update every derived translation coherently. Burst writes after cloning can create synchronized allocation spikes. Pre-fault or rate-limit according to workload objectives.

### Track dirtiness as a protocol

Dirty bitmaps or rings identify pages written during an interval. Clearing and reprotecting must not lose writes racing with collection. Define who owns each dirty state, when hardware buffers are flushed, and how overflow or full rings force exits or fallback. Device-originated writes require compatible tracking.

### Build snapshots from a consistency boundary

A memory snapshot alone may not correspond to CPU registers, device queues or storage. Stop all writers or use a coordinated copy-on-write protocol that defines the snapshot instant. Persist region identity, aliases, page contents, zero or discarded ranges and machine type. Verify restore, not only capture.

### Analyze pre-copy convergence

Pre-copy sends memory while the VM runs, then resends pages dirtied during transfer. It converges only when effective transfer bandwidth outpaces the workload's dirtying behavior enough to meet downtime. Page size, compression, duplicate writes and device DMA change the observed rate.

### Understand post-copy ownership

Post-copy resumes at the destination before all pages arrive. Missing-page faults fetch source content on demand while background transfer continues. This changes failure semantics: losing the source or transport after switchover can make the running destination unrecoverable. Duplicate fetch prevention and page ownership must be explicit.

### Integrate demand-fault services

User-managed fault mechanisms can externalize page supply for post-copy or snapshot loading. Register ranges, choose missing or write-protect modes, validate fault identity and resolve exactly once. Fault-handler capacity becomes guest progress capacity; deadlocks arise if handlers depend on memory or services blocked by the faulting VM.

### Include device DMA in dirtiness and ownership

An assigned device can write guest memory without a vCPU. IOMMU mappings must mirror current ownership, and migration needs device dirty tracking or a conservative alternative. Unmapping a GPA from CPU stage two does not automatically stop cached device DMA. Quiesce and invalidate before reuse.

### Handle memory hotplug and unplug

Hotplug adds a guest-visible region, firmware description and backing generation. Unplug requires the guest to offline pages, migrate contents and acknowledge removal before the host deletes mappings. Forced removal can corrupt guest state. Reserved hotplug address space is part of the machine ABI.

### Treat confidential memory as a different contract

Confidential modes can distinguish private pages inaccessible to the ordinary host from shared pages used for I/O. Conversion requires platform-defined state transitions, validation and TLB synchronization. Traditional userspace device emulation, snapshots, deduplication and post-copy may be restricted because the VMM cannot read private content.

### Compose nested guest memory

Nested virtualization may require nested-GVA to nested-GPA to L1-GPA to HPA translation. Hardware supports a limited number of stages, so the outer monitor may shadow or merge L1's nested controls. Fault attribution must make L1 observe the interface it exposed to L2 while preserving L0 ownership.

### Define pressure and failure behavior

When allocation fails, decide whether to stall, reclaim, balloon, swap, poison a page, inject a guest event or terminate the VM. Host OOM selection is an operational policy, not an architectural memory mechanism. Reserve memory for hypervisor progress, I/O completion and fault handlers so pressure recovery does not deadlock.

### Observe every layer

Measure guest faults and reclaim, stage-two faults, TLB and page-walk events, huge-page promotion and split, host faults, swap, NUMA location, dirty rate, balloon state, KSM activity, IOMMU faults and migration backlog. Join evidence by VM, region, GPA range, host mapping generation and time domain.

### Test reuse and concurrency adversarially

Race guest PTE writes with host unmap, dirty-log clear, huge-page split, balloon, hot-unplug, DMA and migration. Reuse freed host pages for a sentinel tenant and prove no stale translation reaches them. Test page-boundary faults, aliases, partial migration and recovery under memory pressure.

## Definitions and Notation

Let stage-one translation be $T_1:VA_g\rightarrow PA_g$ and monitor translation be $T_2:PA_g\rightarrow PA_h$. A successful guest access resolves as

$$
T(VA_g)=T_2(T_1(VA_g)).
$$

For access-permission sets $P_1$ and $P_2$, effective authority is $P=P_1\cap P_2$, with additional architecture-defined attribute composition.

Let configured, resident, pinned and reclaimable bytes for VM $i$ be $C_i$, $R_i$, $P_i$ and $Q_i$. A host capacity argument must at least distinguish

$$
\sum_i P_i \le H_{usable}
$$

from assumptions about reclaiming $Q_i$ or correlated growth in $R_i$. This inequality alone is necessary for pinned memory, not sufficient for host stability.

For a pre-copy round with remaining dirty bytes $M_k$, effective bandwidth $b_k$, duration $t_k=M_k/b_k$ and dirtying rate $d_k$, an idealized recurrence is

$$
M_{k+1}=\min(M, d_k t_k).
$$

Convergence requires sustained conditions roughly equivalent to $d_k<b_k$; duplicates, tracking granularity and protocol overhead reduce effective bandwidth.

Let mapping generation be $g$. A derived CPU, device or shadow translation built under $g$ is usable only while its dependencies still equal $g$ or after the update protocol proves it compatible.

## Mechanisms, Invariants, or Proof Structure

Review guest-memory virtualization with these obligations.

1. **Domain obligation:** every GVA, GPA, HVA, HPA and IOVA has a named owner and translation path.
2. **Map obligation:** RAM, MMIO, holes, aliases and hotplug ranges implement one versioned machine layout.
3. **Permission obligation:** composite access never exceeds any guest, monitor, host or device restriction.
4. **Fault obligation:** stage, walk context, address, access and owner determine handling or injection.
5. **Invalidation obligation:** mapping and ownership changes retire every stale CPU, shadow and I/O translation before reuse.
6. **Backing obligation:** allocation, residency, pinning, sharing, NUMA and reclaim state remain distinguishable.
7. **Dirty obligation:** collection, clearing, overflow and device writes cannot lose dirtiness.
8. **Lifecycle obligation:** balloon, hotplug, unplug, snapshot and reset transfer page ownership exactly once.
9. **Migration obligation:** pre-copy or post-copy preserves content, identity, aliases and failure semantics.
10. **Device obligation:** DMA mappings, dirty tracking, quiescence and invalidation agree with CPU memory ownership.
11. **Progress obligation:** pressure, missing-page service and recovery reserve enough resources to avoid deadlock.
12. **Assurance obligation:** performance, isolation, confidentiality and recoverability claims use distinct evidence.

The isolation argument follows ownership from GPA region through host backing, then proves composite permissions and revocation before reuse for every CPU and device path. The consistency argument adds dirty generations, snapshots and migration. The performance argument measures TLBs, walks, locality, reclaim and copying separately; none follows from isolation alone.

## Alternatives and Trade-Offs

- **Nested translation versus shadow paging:** hardware composition reduces software trapping; shadows consolidate stages and add coherence work.
- **Anonymous versus file backing:** anonymous memory fits host reclaim; files support sharing and persistence with different failure semantics.
- **Demand allocation versus preallocation:** demand saves idle capacity; preallocation improves predictability and startup cost.
- **Small versus huge pages:** small pages support fine-grained control; huge pages improve TLB reach and constrain lifecycle operations.
- **Pinned versus pageable backing:** pinning supports deterministic DMA; pageable memory improves reclaim and can stall unpredictably.
- **Local versus interleaved NUMA placement:** locality reduces access cost; interleaving spreads bandwidth and can increase remote latency.
- **Conservative admission versus overcommit:** reservation improves guarantees; overcommit improves utilization and correlated-risk exposure.
- **Ballooning versus host swap:** ballooning gives the guest victim choice; host swap acts without cooperation and can double page.
- **Deduplication versus private pages:** merging saves memory; privacy, scanning and COW behavior become coupled.
- **Bitmap versus dirty ring:** bitmaps aggregate compactly; rings provide ordered records and finite-capacity backpressure.
- **Write protection versus hardware dirty bits:** protection is portable and exit-heavy; hardware tracking reduces exits and has flush semantics.
- **Pre-copy versus post-copy:** pre-copy preserves source recovery longer; post-copy bounds duplicate transfer and worsens post-switchover failure.
- **Stop-the-world versus concurrent snapshot:** stopping simplifies consistency; concurrency reduces pause and adds COW state.
- **Emulated versus assigned device memory:** emulation centralizes access; assignment adds IOMMU and device tracking dependencies.
- **Shared versus private confidential pages:** shared pages enable host I/O; private pages strengthen confidentiality and restrict tooling.
- **Automatic versus explicit memory tuning:** automation adapts to load; explicit policy improves reproducibility and auditability.

## Failure Modes and Misconceptions

- “Guest physical means hardware physical.” It names the machine presented to the guest.
- “HVA is always part of translation.” Architectures without a userspace backing process may not use it.
- “Two-stage translation means two memory references.” Multilevel walks can require many references.
- “Stage two can widen stage one.” Effective permission remains constrained by both.
- “Every memory fault belongs to the guest.” Stage-two and host-backing faults have different owners.
- “A page-walk fault is an ordinary data fault.” Walk context affects syndrome and handling.
- “Nested paging eliminates shadow state.” Software still tracks mappings, MMIO and invalidation metadata.
- “A TLB flush is immediate everywhere.” Scope, completion and remote processors matter.
- “Unmapping prevents DMA.” Device translation caches need quiescence and invalidation.
- “A memory slot is only a range.” Backing, flags, owner and generation define it.
- “Configured RAM is resident RAM.” Demand paging and sharing separate them.
- “A huge guest page yields a huge host mapping.” Backing geometry and protection can prevent it.
- “First touch always improves locality.” The touching thread may be the launcher, not the vCPU.
- “Overcommit is free while totals fit on average.” Correlated working sets and pinned pages determine risk.
- “Balloon pages are immediately safe to reuse.” The surrender and zeroing protocol must complete.
- “Host swap is equivalent to guest swap.” The guest loses victim choice and can page twice.
- “Deduplicated pages stay shared after write.” Copy-on-write creates private backing.
- “KSM savings have no security effect.” Sharing can alter timing and threat analysis.
- “Dirty means currently different from destination.” It means a write was observed under a tracking interval.
- “Reading a dirty bitmap atomically clears every race.” Collection and reprotection semantics decide that.
- “A RAM snapshot is a VM snapshot.” CPU, devices, storage and time must align.
- “Pre-copy always converges.” Dirty rate can match or exceed effective bandwidth.
- “Post-copy removes downtime risk.” It transfers failure dependence to source and network.
- “Confidential pages behave like ordinary VMM mappings.” Host visibility and operations can be restricted.
- “No IOMMU fault proves memory safety.” Stale permitted mappings may not fault.

## Worked Examples

### Example 1

A guest maps a code page executable at stage one. Stage two marks its GPA non-executable. Instruction fetch exits with stage-two context. The monitor does not inject a guest stage-one permission fault unless the virtual architecture explicitly requires one.

### Example 2

The following executable toy composes page translations and reports the stage that denies an access. It demonstrates one flat-page permission model only, not a hardware walker, TLB, fault syndrome or memory-attribute rules.

<!-- bijux-verify: {"id":"guest-two-stage-translation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"0x0080 read -> hpa=0x28080\n0x0090 write -> denied=stage2\n0x1100 write -> denied=stage1\n","stderr":""}} -->
```python
page_size = 4096
stage1 = {0: (5, "rw"), 1: (7, "r")}
stage2 = {5: (40, "r"), 7: (41, "rw")}
accesses = [(0x0080, "read"), (0x0090, "write"), (0x1100, "write")]

for gva, operation in accesses:
    gva_page, offset = divmod(gva, page_size)
    required = operation[0]
    first = stage1.get(gva_page)
    if first is None or required not in first[1]:
        result = "denied=stage1"
    else:
        gpa_page = first[0]
        second = stage2.get(gpa_page)
        if second is None or required not in second[1]:
            result = "denied=stage2"
        else:
            hpa = second[0] * page_size + offset
            result = f"hpa=0x{hpa:x}"
    print(f"0x{gva:04x} {operation} -> {result}")
```

### Example 3

The host replaces an HVA mapping through copy-on-write. It invalidates secondary translations before publishing reusable old backing. A vCPU fault then resolves the new host page. Reversing the order can expose the old page after another process owns it.

### Example 4

A 1 GiB guest huge page spans a memory-slot boundary and includes write-protected dirty-log pages. The monitor uses smaller stage-two entries. Guest page size alone does not prove effective TLB geometry.

### Example 5

One VM reports low guest fault rates but high tail latency. Host evidence shows its pages frequently swapped because another VM's pinned working set expanded. The relevant pressure is below the guest abstraction and cannot be diagnosed from guest free memory alone.

### Example 6

Pre-copy transfers 16 GiB, but the guest dirties 3 GiB/s over an effective 2 GiB/s channel. Remaining dirty data does not contract. The controller must throttle, add bandwidth, accept larger downtime, choose post-copy or abort safely.

### Example 7

During post-copy, two vCPUs fault on the same missing page. A claimed-page bitmap lets one fetch while the other waits. Independent fetches could race and overwrite a newer resolved page or waste scarce fault-handler capacity.

### Example 8

A balloon inflates by 4 GiB, but the guest driver has only selected pages; host backing is reclaimed after acknowledgment. Counting the target as free before the protocol completes overstates capacity and can trigger unsafe admission.

### Example 9

An assigned NIC writes through an IOMMU mapping while CPU dirty logging is active. Unless device dirtiness is tracked or all potentially written pages are conservatively dirty, migration can omit newer packet buffers.

### Example 10

A confidential guest converts a page from private to shared for virtio I/O. The platform transition completes, translations are invalidated, the guest scrubs or encrypts sensitive content as required, and only then is the shared GPA published to the backend.

## Cross-Program Connections

- **Computer architecture:** page walkers, TLBs, permissions, memory types and invalidation define translation.
- **Security engineering:** ownership, stale translations, deduplication, DMA and confidential pages define exposure.
- **Performance engineering:** TLB reach, page walks, NUMA, faults, reclaim, dirty rate and copying define cost.
- **Distributed systems:** snapshots, pre-copy, post-copy, generations and ownership transfer resemble replicated state movement.
- **Storage engineering:** file backing, swap, copy-on-write, stable snapshots and image layers persist memory state.
- **Device engineering:** IOVA mappings, DMA, assigned devices and dirty tracking join CPU and I/O memory.
- **Platform engineering:** admission, overcommit, huge-page pools, NUMA placement and migration operate the fleet.
- **Reliability engineering:** pressure reserves, fault services, recovery and reuse tests protect progress.
- **Formal methods:** translation composition, permission intersection and generation invariants structure proofs.
- **Data engineering:** dirty logs, page streams, compression, deduplication and provenance shape migration pipelines.

## References

1. Intel, [Intel 64 and IA-32 Architectures Software Developer Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), paging, EPT, permissions, accessed and dirty state, TLBs and invalidation; retrieved 2026-09-04.
2. AMD, [AMD64 Architecture Programmer's Manual, Volume 2: System Programming](https://docs.amd.com/v/u/en-US/24593_3.44_APM_Vol2), paging, nested page translation, protection, memory types and invalidation; retrieved 2026-09-04.
3. Arm, [Armv8-A Virtualization](https://developer.arm.com/-/media/Arm%20Developer%20Community/PDF/Learn%20the%20Architecture/Armv8-A%20virtualization.pdf), stage-two translation, intermediate physical addresses, VMIDs and faults; retrieved 2026-09-04.
4. RISC-V International, [Hypervisor Extension](https://docs.riscv.org/reference/isa/priv/hypervisor), guest physical addressing, two-stage translation, fences and fault state; retrieved 2026-09-04.
5. Linux Kernel Documentation, [The x86 KVM Shadow MMU](https://docs.kernel.org/virt/kvm/x86/mmu.html), direct and shadow translation, memory events, dirty tracking, large pages and generations; retrieved 2026-09-04.
6. Linux Kernel Documentation, [KVM API](https://docs.kernel.org/virt/kvm/api.html), memory regions, backing, dirty bitmaps, dirty rings and protected guest memory interfaces; retrieved 2026-09-04.
7. QEMU Project, [Memory API](https://qemu.readthedocs.io/en/master/devel/memory.html), address spaces, RAM, MMIO, aliases, region lifecycle and migration identity; retrieved 2026-09-04.
8. Linux Kernel Documentation, [MMU Notifier Ordering](https://docs.kernel.org/mm/mmu_notifier.html), secondary-TLB invalidation during page replacement and reuse; retrieved 2026-09-04.
9. Linux Kernel Documentation, [Userfaultfd](https://docs.kernel.org/admin-guide/mm/userfaultfd.html), user-managed missing and write-protect faults and post-copy VM migration; retrieved 2026-09-04.
10. Linux Kernel Documentation, [Kernel Samepage Merging](https://docs.kernel.org/admin-guide/mm/ksm.html), page deduplication, copy-on-write, NUMA, scan cost and profit accounting; retrieved 2026-09-04.

## Exercises

### Exercise 1

Trace a guest load from GVA through a hosted two-stage VMM and name the owner of each mapping and the likely handler for a failure at each stage.

### Exercise 2

Stage one grants `r-x`, stage two grants `rw-`, and a device IOMMU mapping grants `rw-`. State effective CPU and device permissions without inventing a shared virtual-address path.

### Exercise 3

A host has 512 GiB usable memory. VMs pin 180 GiB, currently hold 260 GiB resident unpinned memory and report 120 GiB reclaimable. Explain what can and cannot be concluded from the pinned-capacity inequality.

### Exercise 4

An idealized pre-copy round starts with 12 GiB remaining, bandwidth is 4 GiB/s and dirty rate is 1.5 GiB/s. Compute round duration and next remaining dirty bytes, then repeat once with constant rates.

### Exercise 5

Design a test proving safe host-page reuse while guest PTE changes, host copy-on-write, DMA and VM teardown race.

## Answers to the Exercises

### Answer 1

The guest CPU supplies a GVA. Guest page tables owned by the guest OS map it to a GPA; a missing or denied stage-one entry normally produces a guest architectural fault. The hypervisor's stage-two tables map the GPA to an HPA and enforce VM ownership; a miss may allocate backing, dispatch MMIO, perform policy work or terminate an invalid access.

In a hosted architecture, userspace may define GPA-to-HVA memory regions, and the host MM maps HVA to HPA. A host fault can demand-allocate, load a file page, copy on write, swap in or fail under pressure. The hypervisor kernel coordinates derived translation with host-MM change notifications. Each failure retains its owner even when hardware reports combined walk information.

### Answer 2

For CPU execution, stage intersection is read only: stage one permits read and execute, while stage two permits read and write, so only read is common. CPU write and execute are denied by one stage each.

The device does not ordinarily issue a guest virtual address through the guest CPU's stage-one PTE. Its IOVA and IOMMU mapping form a separate path. Under only the stated IOMMU grant it can read and write the authorized host backing, subject to any additional device and platform restrictions. Do not intersect its permission with unrelated `r-x` GVA state unless the architecture explicitly shares those tables.

### Answer 3

Pinned memory satisfies $180\text{ GiB}\le512\text{ GiB}$, so the stated pinned set alone fits. This does not prove host stability. Pinned memory leaves 332 GiB for the host, hypervisor, unpinned VM pages and other workloads. Current VM residency totals 440 GiB including pinned memory if the categories are nested as stated, but precise accounting must confirm overlap.

The 120 GiB labeled reclaimable is a policy estimate, not instantly free memory. Reclaim latency, dirty writeback, correlated VM growth, host reserves, huge-page fragmentation, devices and minimum guest working sets remain. The inequality is necessary for pinned capacity and insufficient for overall admission.

### Answer 4

The first duration is $t_0=12/4=3$ seconds. Idealized writes during it are $M_1=(1.5)(3)=4.5$ GiB. The next duration is $t_1=4.5/4=1.125$ seconds, producing

$$
M_2=(1.5)(1.125)=1.6875\text{ GiB}.
$$

The recurrence contracts because dirty rate is below effective bandwidth. Real systems add duplicate-page granularity, tracking, protocol and competing-traffic costs and may have nonconstant dirtying.

### Answer 5

Map a sentinel page to the test VM and let guest vCPUs repeatedly rewrite PTEs and access aliases while a device performs DMA. Concurrently force host copy-on-write, revoke the memory region and destroy the VM. The teardown protocol must stop new CPU and device work, invalidate derived CPU and I/O translations, wait for acknowledgments and only then reassign the HPA to a sentinel process or VM.

After reassignment, continuously verify the new owner's canary while attempting stale guest and device accesses. Collect guest faults, stage-two faults, IOMMU faults, mapping generations, notifier begin/end, invalidation acknowledgments, vCPU stop state, device quiescence and page-owner transitions. Repeat across CPUs, page sizes and forced preemption; any old-owner read or write after the ownership fence fails the invariant.
