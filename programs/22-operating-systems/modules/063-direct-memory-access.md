---
module_id: OS-063
program: Operating Systems
level: 2
module_number: 63
title: Direct Memory Access
status: complete
last_verified: 2026-09-04
---

# Direct Memory Access

## One-Page Review

### Governing question

How should an operating system let a device transfer data to or from memory without CPU copying while preserving addressability, cache coherence, ordering, ownership, isolation, completion, and lifetime across architectures and failures?

### Essential definitions

- **Direct memory access (DMA)** is a device-initiated transfer between an I/O endpoint and memory, or between devices, under software-configured bounds and direction.
- A **CPU virtual address** names memory through the CPU page tables; it is not generally usable by a device.
- A **DMA address** is the address programmed into a device after the DMA layer applies translation, constraints, or bounce buffering.
- A **DMA mask** states the address bits a device can drive for streaming or coherent transfers.
- A **coherent mapping** permits CPU and device access without explicit cache-maintenance transitions, while still requiring memory ordering.
- A **streaming mapping** creates a direction-specific, normally temporary device view whose ownership transitions require map, sync, and unmap discipline.
- A **scatter-gather list** represents a logical buffer as segments and lets the DMA layer return the device-visible segment sequence.
- An **IOMMU** translates I/O virtual addresses and can constrain a device to explicitly mapped memory.
- A **bounce buffer** is DMA-addressable intermediate storage copied to or from the original buffer when direct mapping is impossible or unsafe.
- A **completion** is trusted evidence that the device no longer accesses a submitted buffer; an interrupt alone is not necessarily that evidence.

### Central model, mechanism, or theorem

Treat a DMA mapping as a revocable capability

$$
M=(d, i, n, q, g, o, \ell),
$$

where $d$ is the device, $i$ the DMA address or segments, $n$ the byte extent, $q$ the direction, $g$ the translation or protection domain, $o$ the current CPU/device ownership state, and $\ell$ the mapping lifetime. A transfer is safe only if the device can address every segment, the mapping direction grants the actual access, CPU and device ownership do not conflict, required data and descriptor writes precede notification, completion precedes reuse or unmap, and teardown revokes device access before backing memory is freed.

For streaming memory the durable cycle is `CPU owns -> map/sync for device -> device owns -> completion -> sync/unmap for CPU -> CPU owns`. Coherent memory removes explicit cache-maintenance transitions, not the need for barriers, device protocol, synchronization, or lifetime control.

### Critical invariants

- Program only DMA addresses returned for the exact device, buffer, size, direction, and live mapping.
- Check mask setup, allocation, and every mapping result before exposing an address to hardware.
- CPU and device never modify a streaming buffer concurrently outside an explicitly supported ownership protocol.
- Direction reflects the device's actual read and write permissions and remains identical across map, sync, and unmap.
- Descriptor contents and payload ownership become device-visible before a doorbell; validated completion precedes CPU access, reuse, unmap, and free.
- Scatter-gather iteration uses the mapped segment count and DMA fields, while unmap uses the original input count required by the API.
- Cache-line sharing cannot let maintenance for a DMA buffer corrupt unrelated CPU-written data.
- Reset, timeout, cancellation, and removal contain or stop bus mastering before mappings and backing storage disappear.
- IOMMU isolation is scoped to domain membership, granularity, permissions, invalidation, and topology; its presence alone is not a proof.

### Common failures

Common mistakes are programming a CPU pointer or physical address, skipping DMA mask negotiation, ignoring mapping failure, choosing `DMA_BIDIRECTIONAL` by habit, touching a streaming buffer while the device owns it, believing coherent means ordered, omitting the barrier before a valid bit or doorbell, using the original scatter-list entries after mapping, unmapping with the returned count, placing unrelated fields in the same cache line, reusing a descriptor after an interrupt without checking ownership, freeing on timeout while DMA continues, resetting before stopping submissions, trusting an IOMMU with an overbroad domain, and assuming a DMA-capable device is non-adversarial.

### Compact example

A receive buffer is mapped `DMA_FROM_DEVICE`. Mapping transfers ownership to the device. After a validated completion, synchronization transfers ownership to the CPU before it reads the bytes. If the buffer is reused without unmapping, synchronization returns ownership to the device; final completion precedes unmap. The direction describes device writes, not the CPU's later read.

### Connections

[OS-031](031-address-translation.md), [OS-039](039-shared-pages-and-page-cache.md), [OS-052](052-smp-kernel-synchronization.md), [OS-061](061-device-discovery-and-driver-models.md), [OS-062](062-memory-mapped-and-port-mapped-i-o.md), and [OS-064](../ROADMAP.md) connect DMA to translation, memory lifetime, ordering, device lifecycle, register notification, and I/O interfaces.

## Governing Question

DMA shifts bulk movement away from CPU instructions, but it does not remove software responsibility. The driver selects memory, grants a device access, publishes addresses and ownership, starts an engine, interprets completion, and revokes the grant. Each action crosses an address, cache, ordering, privilege, or lifetime boundary.

The governing question is how to express those boundaries through the operating system's DMA API rather than assumptions about physical memory. A portable driver must remain correct whether the platform uses direct physical addressing, an IOMMU, noncoherent caches, software bounce buffers, memory encryption, or a virtual device.

## Why This Matters

DMA enables high-throughput storage, networking, graphics, audio, accelerators, and inter-device pipelines. It can avoid copies and amortize interrupts, but a small bookkeeping error can corrupt arbitrary memory or persistent data.

Devices act asynchronously. The CPU may time out while the device still owns a buffer. An interrupt can race reset. A completion entry can become visible before payload data if ordering is wrong. On noncoherent systems, stale cache lines can hide either side's writes.

DMA is also a protection problem. A bus-mastering device can bypass CPU page permissions. IOMMUs narrow that authority, but isolation depends on exact mappings, permissions, invalidation, device grouping, and behavior during faults and reset.

## Prerequisites and Retrieval

Review [OS-004](004-interrupts-and-exceptions.md), [OS-021](021-critical-sections-in-the-kernel.md), [OS-024](024-atomic-operations.md), [OS-031](031-address-translation.md), [OS-032](032-page-tables.md), [OS-039](039-shared-pages-and-page-cache.md), [OS-052](052-smp-kernel-synchronization.md), [OS-055](055-numa-memory-placement.md), [OS-061](061-device-discovery-and-driver-models.md), and [OS-062](062-memory-mapped-and-port-mapped-i-o.md).

Retrieve these distinctions:

- CPU virtual, CPU physical, bus, DMA, and I/O virtual addresses belong to different translation domains;
- physical contiguity, virtual contiguity, and device-visible segment contiguity are separate properties;
- cache coherence, memory ordering, device completion, and mutual exclusion are different guarantees;
- a transfer direction is stated from the device's perspective;
- coherent and streaming mappings express different ownership and maintenance contracts;
- an interrupt reports an event, while protocol state establishes which buffer completed;
- a software reference keeps memory metadata alive but does not revoke a device's ability to write;
- an IOMMU mapping grants authority and must be treated as a security-sensitive capability.

## Learning Objectives

After this module, you should be able to:

1. distinguish CPU pointers, physical addresses, DMA addresses, I/O virtual addresses, and device constraints;
2. negotiate DMA masks and select coherent, streaming, scatter-gather, pool, or shared-buffer mechanisms;
3. model ownership transitions, direction, cache maintenance, barriers, notification, completion, and reuse;
4. map and unmap single buffers and scatter lists with correct counts, sizes, directions, and error handling;
5. reason about IOMMU protection, bounce buffering, peer-to-peer DMA, user memory, and virtual machines;
6. design timeout, reset, cancellation, suspend, and hot-unplug paths that contain active DMA;
7. verify DMA safety with API debugging, fault injection, ordering tests, telemetry, and scoped evidence.

## Core Exposition

### DMA as delegated memory access

The CPU configures a device with addresses, lengths, direction, and control state. The device then reads or writes memory independently and reports progress through descriptors, status, interrupts, or completion queues.

This is delegation, not magic copying. Software must prove that the delegate has the intended authority for exactly the intended interval and that the memory remains stable until authority is revoked.

### Address domains

A kernel pointer is meaningful to the CPU page tables. A physical address names host memory. A DMA address is meaningful to one device under its bus and translation domain.

The DMA layer can translate a CPU buffer through an IOMMU, return a directly reachable bus address, or allocate a bounce buffer. Never derive one domain from another with a cast or `virt_to_phys()` shortcut.

### Device-specific mappings

Pass the correct `struct device` to DMA APIs. Its masks, IOMMU domain, offsets, coherency properties, segment limits, encryption rules, and topology determine the mapping.

A DMA address returned for one function is not automatically valid for a sibling function. Sharing requires an explicit framework and attachment per device.

### Address masks

Devices have a finite address width. Probe declares streaming and coherent capabilities with the DMA mask APIs and handles failure if the platform cannot satisfy them.

Do not assume 32 bits is always safe or that a 64-bit register implies 64-bit DMA capability. Some functions, descriptor rings, payloads, or device modes have different constraints.

### Segment constraints

Hardware can limit maximum segment size, boundary crossings, alignment, number of descriptors, and low address bits. The DMA and upper-layer APIs communicate these limits.

Validate length arithmetic before mapping and before writing device descriptor fields. A byte length that truncates into a smaller hardware field can authorize a transfer different from the mapped extent.

### Coherent allocation

Coherent allocation returns a CPU pointer and a DMA address for memory suitable for concurrent visibility under the platform contract. Descriptor rings and command mailboxes commonly use it.

Keep the two values distinct. The CPU dereferences its pointer; hardware receives the DMA address. Free with the matching device, size, CPU pointer, and DMA handle after all access stops.

### Coherent does not mean ordered

Coherence ensures that explicit cache synchronization is not needed for visibility. CPUs can still reorder descriptor field stores, and the device protocol can require a valid bit last.

Use the documented DMA or memory barrier before publishing ownership. Then use the required MMIO accessor to ring a doorbell. Neither coherence nor a lock replaces those edges.

### DMA pools

DMA pools allocate many small coherent objects with alignment and boundary constraints. They suit descriptors or command blocks smaller than a page.

The pool lifetime must exceed every object and in-flight transfer. Return objects only after completion and destroy the pool only after all objects are freed.

### Streaming mappings

Streaming mapping temporarily makes an existing CPU buffer accessible to a device. The map operation returns a DMA address and establishes direction-specific cache and ownership state.

Mapping can fail because address space, bounce space, or translation resources are unavailable. Always use the DMA mapping error API instead of interpreting a magic address.

### Direction

`DMA_TO_DEVICE` means the device reads memory. `DMA_FROM_DEVICE` means the device writes memory. `DMA_BIDIRECTIONAL` permits both and can impose extra synchronization or weaker protection.

Choose the narrowest correct direction. `DMA_NONE` is a debugging sentinel, not a transfer direction. Use the same direction for every sync and unmap associated with a mapping.

### Ownership transitions

After a streaming buffer is mapped or synchronized for the device, the CPU must not access it until completion and synchronization for the CPU. After synchronization back to the device, the CPU stops again.

Ownership is about legal access, not object references. Locks between CPU threads do not constrain a device, and a device cannot acquire a software mutex.

### Mapping single buffers

`dma_map_single()` maps a suitable virtually contiguous kernel region; page-based variants accept a page and offset. The driver retains the original CPU-side object separately from the returned DMA handle.

On completion, unmap with the exact device, DMA address, size, and direction. Partial construction unwinds every successfully mapped region in reverse order.

### Buffer suitability

Not every pointer is legal for `dma_map_single()`. Stack memory, module image memory, arbitrary `vmalloc()` regions, and addresses without stable backing can violate API rules.

Use memory from documented allocators or page interfaces and keep it pinned and alive for the full mapping. Avoid unrelated data in the same cache line on noncoherent platforms.

### Cache-line sharing

Cache maintenance can operate at cache-line granularity. If a receive buffer shares a line with CPU-written metadata, invalidating the buffer can discard the CPU's unrelated writes.

Align and isolate DMA regions as required. Treat sub-cache-line `DMA_FROM_DEVICE` buffers as a correctness hazard unless the API and allocation guarantee safe handling.

### Synchronization for CPU and device

Long-lived streaming mappings can alternate ownership through `dma_sync_*_for_cpu()` and `dma_sync_*_for_device()`. Synchronize the needed range and retain the original mapping parameters.

Do not access the buffer between submission and validated completion. Synchronization performs required maintenance; it does not wait for hardware to finish.

### Scatter-gather input

Scatter-gather represents a logical request across pages or fragments. The driver supplies the original list and entry count to the DMA mapping API.

The implementation may merge adjacent entries or split according to constraints. Mapping returns the device-visible entry count, which can differ from the input count.

### Scatter-gather iteration

Program descriptors by iterating the returned mapped count and reading `sg_dma_address()` and `sg_dma_len()`. Do not program original CPU page addresses or assume a one-to-one relation.

Unmap with the original input entry count, not the returned mapped count. This apparent asymmetry is part of the API contract and should be captured in per-request state.

### Mapping failure

Single and page mappings require `dma_mapping_error()` checks; scatter-gather returns zero on failure; allocation can return null. Failure is a normal resource condition, not an impossible platform defect.

Backpressure, retry, request splitting, or failure belongs to the subsystem contract. Never program a failed handle, and unwind a partially built descriptor chain completely.

### Descriptor design

Descriptors contain DMA addresses, lengths, flags, identifiers, and ownership bits. Validate every conversion into the device's field width and endian representation.

Initialize data and metadata before the ownership or valid field. Prevent the compiler and CPU from publishing valid early with the required barrier. Avoid reusing a descriptor until completion transfers ownership back.

### Rings and generations

Producer and consumer indices wrap. Pair indices with generations, phase bits, or bounded differences so full and empty remain distinguishable.

Validate device-returned indices before using them for array access or freeing buffers. A faulty or malicious device can report an impossible completion.

### Doorbells

After descriptors are device-visible, an MMIO write notifies the engine. The required order is

$$
\text{payload} \prec \text{descriptor} \prec \text{ownership} \prec \text{doorbell}.
$$

The DMA barrier establishes memory order; the register accessor establishes I/O order. A posted-write readback is added only when the device protocol needs completion before another transition.

### Completion

Completion can be a device-written descriptor bit, a completion-queue entry, an interrupt plus status, or a fence. Validate identity, generation, range, and state before accepting it.

An interrupt can be shared, spurious, coalesced, early, or late. It tells software to inspect authoritative protocol state; it does not by itself prove a particular buffer is free.

### Receive ordering

For device-to-CPU data, software first observes a valid completion under the device's ordering contract, then uses the required read barrier or sync before consuming payload.

Do not read payload speculatively while the device owns it. On noncoherent systems, synchronization makes device writes visible; on coherent systems, an ordering barrier can still be necessary after the ownership indicator.

### Transmit ordering

For CPU-to-device data, finish payload writes, map or synchronize for the device, initialize the descriptor, publish ownership with a barrier, and ring the doorbell.

Completion precedes unmap and reuse. If a timeout leaves ownership uncertain, freeing the buffer is unsafe until reset or isolation proves the engine cannot access it.

### IOMMUs

An IOMMU maps I/O virtual addresses to physical pages, supplies permissions, and reports some faults. It can provide contiguous device address space for scattered pages and isolate devices from unrelated memory.

Its granularity can expose padding within a mapped page, and devices in one group can share isolation boundaries. Domain attachment, permissions, invalidation completion, and fault policy all matter.

### Translation caches

IOMMUs and devices can cache translations. Revoking a page-table entry is not complete until required invalidation has finished and outstanding transactions are contained.

The DMA API owns these details for normal drivers. Bypassing it with home-grown mappings risks reuse of physical memory while a stale device translation remains live.

### Bounce buffering

Software I/O translation buffers handle devices that cannot address the original memory, encrypted guest memory inaccessible to a host, or isolation granularity that would expose neighbors.

Mapping, synchronization, and unmapping can copy data. This adds latency, CPU use, memory pressure, size limits, and failure modes. Drivers use normal DMA APIs and honor reported segment limits rather than calling the bounce layer directly.

### NUMA placement

DMA buffers placed near the submitting CPU may be far from the device's I/O root, and device-local placement can be remote to consumers. Measure memory-controller, interconnect, IOMMU, and CPU costs together.

Placement policy must retain mask, topology, hotplug, and fallback correctness. Performance affinity never licenses an inaccessible address.

### Shared DMA buffers

The dma-buf framework shares backing memory across devices and processes. Exporters own allocation and migration; importers attach per device and map an attachment into that device's DMA domain.

References preserve the object, attachments describe device relationships, and fences coordinate asynchronous access. CPU access is bracketed by begin/end operations; a file descriptor alone does not establish cache ownership.

### Fences and reservation objects

A fence represents completion of asynchronous work. Reservation objects collect usage-scoped fences so importers and memory managers can order readers, writers, and migration.

Signal only after device access is truly complete. Error and device-loss paths must resolve fences so waiters do not hang forever, while preserving the fact that output may be invalid.

### User memory

DMA to userspace memory requires pinning or another subsystem-owned registration model, accounting, revocation, permissions, and process-exit handling. Ordinary virtual mappings can change independently.

Long-term pins interfere with migration, reclaim, copy-on-write, and filesystem rules. Use established subsystem interfaces rather than translating arbitrary user pointers inside a driver.

### Userspace-controlled devices

VFIO and IOMMUFD can delegate device and I/O page-table management to a privileged userspace component. Correctness depends on viable isolation groups, pinned or registered memory, interrupt routing, reset, dirty tracking where needed, and orderly teardown.

The kernel must validate every request and retain containment. A userspace driver is not a reason to trust guest-provided addresses or leave bus mastering enabled after process death.

### Peer-to-peer DMA

PCI peer-to-peer DMA moves data between device memory and another device without routing through system RAM. Topology and host-bridge support determine whether the path is safe and routable.

Use the PCI P2P framework to validate providers, clients, distance, and mappings. A device MMIO resource is not ordinary memory and cannot be fed through the RAM DMA API casually.

### Virtualization

A guest DMA address may pass through guest translation, virtual IOMMU state, host pinning, host IOMMU translation, and device queues. Each layer owns a separate lifetime and failure domain.

Live migration must capture device state or quiesce DMA and dirty tracking consistently. Confidential guests may force bounce buffering between encrypted and shared memory.

### Security boundaries

DMA can read secrets, modify code or page tables, and persist after driver compromise. Apply least privilege to address range, direction, duration, device domain, and userspace delegation.

Clear newly exposed buffers, prevent integer overflow, validate device-written metadata, isolate untrusted devices, and revoke mappings on error. An IOMMU reduces blast radius but does not make firmware or completion data trustworthy.

### Timeout and cancellation

A timeout means software lacks timely completion evidence; it does not mean DMA stopped. Mark the request uncertain, stop new submissions, disable or isolate the engine, and follow the device's abort or reset protocol.

Only after bus mastering is contained, interrupts synchronized, and invalidations complete may software unmap or free uncertain buffers. Record which guarantee justified the transition.

### Reset

Reset ordering is device-specific. Quiesce queue producers, block doorbells, mask interrupts, contain DMA, synchronize callbacks, issue reset, wait with a deadline, rebuild mappings or rings as required, and publish a new generation.

Late completions from an old generation must not release new buffers that reused the same slot. Generation identifiers turn this race into a checkable invariant.

### Suspend and resume

Suspend stops submissions and drains, aborts, or preserves transfers under the device contract before power loss. Wake-capable DMA needs explicit platform support and restricted memory.

Resume restores translation and device state before bus mastering and interfaces. Never assume IOMMU or device context survived a power transition.

### Hot-unplug

Graceful unplug follows normal quiescence. Surprise removal begins without device cooperation; the bus and IOMMU must contain requests while software completes callers with errors and drains callbacks.

Keep buffer metadata alive until every possible completion path is synchronized. Do not read vanished MMIO merely to confirm that DMA stopped.

### Observability

Record device identity, mapping type, direction, byte count, input and mapped segment counts, DMA mask, mapping failures, queue and generation, submission and completion times, timeout state, IOMMU faults, resets, bounce usage, and outstanding mappings.

Protect DMA addresses and buffer contents according to threat model. Counters and semantic events are usually safer than payload dumps.

### Verification

Enable DMA API debugging in development kernels to catch size, direction, device, double-unmap, missing error-check, and lifetime violations. Treat its bookkeeping limits and performance cost as part of the evidence.

Use fault injection for allocation, mapping, bounce exhaustion, IOMMU failure, dropped and duplicate completion, timeout, reset, suspend, and unplug. Test noncoherent and weakly ordered platforms or faithful emulation, not only one coherent workstation.

## Definitions and Notation

Let $B$ be a byte interval backed by stable pages. A DMA capability is $M=(d,I,n,q,g,o,\ell)$ as above, where $I=[(a_1,n_1),\ldots,(a_k,n_k)]$ and $\sum n_j=n$. The device descriptor must not authorize bytes outside $I$.

For a streaming buffer, ownership transitions are

$$
C \xrightarrow{\text{map/sync-device}} D
\xrightarrow{\text{validated completion}} D_c
\xrightarrow{\text{sync/unmap-CPU}} C.
$$

CPU access in state $D$ is forbidden even if a CPU pointer exists. Device access after state $C$ is forbidden even if a stale DMA address remains in hardware.

Let $P$ mean payload ready, $H$ descriptor header ready, $V$ ownership valid, $K$ doorbell visible, and $F$ completion validated. A standard submission requires $P \prec H \prec V \prec K \prec F$; buffer reuse requires $F \prec U$. Each edge names a barrier, accessor, or protocol event rather than relying on source-code order.

## Mechanisms, Invariants, or Proof Structure

A reviewable DMA path discharges these obligations:

1. **Capability:** negotiate the device's masks, segment limits, boundaries, alignment, and topology.
2. **Backing:** allocate or pin permitted memory with adequate lifetime and cache-line isolation.
3. **Mapping:** map for the exact device, extent, direction, and attributes and check failure.
4. **Translation:** program only returned DMA addresses and mapped scatter-gather lengths.
5. **Ownership:** make CPU/device access states explicit and synchronize every transition.
6. **Ordering:** publish payload, descriptor, ownership and doorbell in proved order.
7. **Validation:** distrust device-written identifiers, indices, lengths and status.
8. **Completion:** establish authoritative end-of-access before CPU use, reuse, unmap, or free.
9. **Isolation:** scope IOMMU or bounce authority to the intended pages, permissions and lifetime.
10. **Failure:** unwind partial mappings and contain uncertain in-flight DMA on timeout or reset.
11. **Revocation:** stop submissions, bus mastering and callbacks before unmapping backing memory.
12. **Evidence:** exercise error, ordering, coherence, architecture, topology and lifecycle boundaries.

These proofs do not collapse. Coherent allocation proves a visibility property, not store order. IOMMU translation proves only configured reachability, not benign device behavior. An interrupt proves notification, not buffer identity. Unmapping asks the DMA layer to revoke a capability but is safe only after device use has ended.

## Alternatives and Trade-Offs

- **Programmed I/O versus DMA:** CPU copies simplify tiny transfers; DMA amortizes setup for larger or asynchronous work.
- **Coherent versus streaming:** coherent memory simplifies cache transitions; streaming can use ordinary buffers efficiently with explicit ownership.
- **Single buffer versus scatter-gather:** one segment simplifies hardware; scatter-gather avoids copies and large contiguous allocations.
- **Persistent versus per-transfer mapping:** persistent mappings reduce setup cost; they lengthen authority and demand explicit sync transitions.
- **Direct mapping versus bounce buffering:** direct access avoids copies; bounce buffers extend reachability and isolation at CPU and memory cost.
- **IOMMU translation versus physical DMA:** translation improves placement and protection; it consumes page tables, invalidation work and I/O TLB capacity.
- **Interrupt per completion versus batching:** immediate interrupts reduce latency; batching improves throughput but increases delay and recovery scope.
- **Polling versus interrupts:** polling can win at high rates; interrupts save CPU when completions are sparse.
- **One queue versus per-CPU queues:** one queue simplifies reset; multiple queues reduce contention and expand generation and affinity management.
- **Kernel-owned versus user-owned queues:** kernel ownership centralizes policy; delegation reduces crossings but enlarges isolation obligations.
- **System RAM versus peer memory:** RAM is broadly routable; peer memory can avoid hops but depends on topology and provider lifetime.
- **Implicit versus explicit fences:** implicit synchronization eases composition; explicit fences expose dependencies and require disciplined propagation.
- **Long-term pinning versus migration:** pins stabilize backing pages; migratable memory improves reclamation and placement.
- **Strict direction versus bidirectional:** narrow direction improves optimization and protection; bidirectional supports genuine two-way protocols at added cost.

## Failure Modes and Misconceptions

- **“The device can use my kernel pointer.”** It needs a DMA address returned for that device.
- **“Physical address equals DMA address.”** Translation, offsets, IOMMUs and bounce buffers can differ.
- **“Mapping cannot fail after probe.”** I/O virtual or bounce space can be exhausted dynamically.
- **“The default mask fits every device.”** Capabilities must be negotiated and failure handled.
- **“Bidirectional is safest.”** It can weaken permissions and require more maintenance.
- **“Coherent means no barriers.”** Coherence does not impose descriptor field order.
- **“Sync waits for hardware.”** It performs ownership/cache work after completion is established elsewhere.
- **“A lock prevents device access.”** Devices do not participate in CPU locks.
- **“An interrupt completes the oldest request.”** Completion identity and generation must be validated.
- **“Scatter-gather output mirrors input.”** The mapper can merge or otherwise transform segments.
- **“Unmap uses the returned SG count.”** Linux unmap receives the original entry count.
- **“A short receive buffer may share metadata's cache line.”** Maintenance can corrupt neighbors.
- **“Timeout permits free.”** The engine may still write until contained.
- **“Reset erases every stale transaction.”** Bus, device and IOMMU completion rules still apply.
- **“IOMMU present means isolated.”** Domain scope, groups, permissions, granularity and invalidation decide isolation.
- **“A dma-buf file descriptor means CPU coherence.”** CPU access needs the framework's synchronization protocol.
- **“Peer memory is ordinary RAM.”** Routing and access APIs differ.
- **“DMA API debugging proves hardware correctness.”** It catches API misuse within its recorded coverage.

## Worked Examples

### Example 1

A 32-bit device on a host with high memory negotiates a 32-bit mask. The DMA layer maps a high buffer through a low bounce region; the driver programs the returned address and sees only higher latency, not a different API.

### Example 2

A network transmit path maps packet fragments `DMA_TO_DEVICE`, checks a nonzero mapped count, programs only DMA segment fields, and stores the original count for unmap. Mapping failure drops or backpressures according to the network contract.

### Example 3

A storage receive buffer is `DMA_FROM_DEVICE`. Completion identifies the command and generation; sync-for-CPU precedes parsing. CPU inspection ends before sync-for-device returns the reusable buffer to the controller.

### Example 4

A coherent ring descriptor contains address, length, flags and valid. The CPU writes the first three, executes the required DMA write barrier, sets valid, and rings the doorbell. Coherence alone would not prevent valid from appearing first.

### Example 5

An IOMMU fault reports a device write beyond a receive buffer. The driver stops the queue, preserves the fault and descriptor evidence, invalidates the request, resets the device, and never trusts its completion index.

### Example 6

A timeout occurs during transmit. Software cannot free the packet because completion is unknown. It disables queue submission, contains bus mastering through reset and isolation, synchronizes callbacks, and only then unmaps and reports failure.

### Example 7

A video buffer is exported with dma-buf and attached to a display and accelerator. Each attachment maps into its own device domain; reservation fences order writes, and begin/end CPU access bracket a software fallback.

### Example 8

A confidential guest uses bounce buffers because encrypted private pages are inaccessible to the host device. Sync operations copy through shared memory, making buffer size and pool pressure visible performance constraints.

### Example 9

A peer-to-peer storage-to-accelerator path is accepted only when the PCI P2P framework validates topology. On a different host bridge it falls back to system RAM without inventing a peer bus address.

### Example 10

The following ownership model checks one reusable receive-buffer cycle. It demonstrates direction and state transitions only; it performs no DMA mapping, cache maintenance, barrier, IOMMU operation, interrupt, or hardware transfer.

<!-- bijux-verify: {"id":"dma-buffer-ownership","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"map direction=from-device owner=device\ncomplete bytes=4 owner=device-complete\nsync owner=cpu checksum=10\nrequeue owner=device\ncomplete bytes=4 owner=device-complete\nunmap owner=cpu\n","stderr":""}} -->
```python
class ReceiveBuffer:
    def __init__(self):
        self.owner = "cpu"
        self.data = bytearray(4)

    def map(self):
        assert self.owner == "cpu"
        self.owner = "device"

    def complete(self, values):
        assert self.owner == "device"
        self.data[:] = values
        self.owner = "device-complete"

    def sync_for_cpu(self):
        assert self.owner == "device-complete"
        self.owner = "cpu"

    def sync_for_device(self):
        assert self.owner == "cpu"
        self.owner = "device"

b = ReceiveBuffer()
b.map()
print(f"map direction=from-device owner={b.owner}")
b.complete([1, 2, 3, 4])
print(f"complete bytes={len(b.data)} owner={b.owner}")
b.sync_for_cpu()
print(f"sync owner={b.owner} checksum={sum(b.data)}")
b.sync_for_device()
print(f"requeue owner={b.owner}")
b.complete([4, 3, 2, 1])
print(f"complete bytes={len(b.data)} owner={b.owner}")
b.sync_for_cpu()
print(f"unmap owner={b.owner}")
```

## Cross-Program Connections

[Computer Architecture](../../23-computer-architecture/ROADMAP.md) explains buses, caches, coherence, memory ordering, interrupts, IOMMUs and accelerators. [Security Engineering](../../25-security-engineering/ROADMAP.md) connects least privilege, malicious peripherals, isolation domains, memory disclosure and revocation.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) contributes ownership transfer, generations, completion, timeout and uncertain outcomes. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) contributes hazard analysis, state machines, fault containment and assurance. Within this program, [OS-062](062-memory-mapped-and-port-mapped-i-o.md) develops register notification and [OS-064](../ROADMAP.md) develops device interfaces.

## References

- Linux kernel documentation, [Dynamic DMA Mapping Guide](https://docs.kernel.org/core-api/dma-api-howto.html), current page checked 2026-09-04. Address domains, masks, coherent and streaming mappings, direction, scatter-gather, synchronization and errors.
- Linux kernel documentation, [Dynamic DMA Mapping Using the Generic Device](https://docs.kernel.org/core-api/dma-api.html), current page checked 2026-09-04. DMA types, allocation, mapping, attributes, scatter lists and DMA API debugging.
- Linux kernel documentation, [Linux Kernel Memory Barriers](https://docs.kernel.org/core-api/wrappers/memory-barriers.html), current page checked 2026-09-04. CPU, DMA and device ordering, ownership and barrier semantics.
- Linux kernel documentation, [DMA Attributes](https://docs.kernel.org/core-api/dma-attributes.html), current page checked 2026-09-04. Weak ordering, write combining, no-kernel-mapping, skipped synchronization and MMIO attributes.
- Linux kernel documentation, [DMA and swiotlb](https://docs.kernel.org/core-api/swiotlb.html), current page checked 2026-09-04. Bounce-buffer use, copying, pool constraints, confidential guests and untrusted devices.
- Linux kernel documentation, [Buffer Sharing and Synchronization](https://docs.kernel.org/driver-api/dma-buf.html), current page checked 2026-09-04. dma-buf exporters, attachments, device mapping, fences, reservations and CPU access.
- Linux kernel documentation, [IOMMUFD](https://docs.kernel.org/userspace-api/iommufd.html), current page checked 2026-09-04. Userspace I/O address spaces, hardware page tables, access objects and lifecycle.
- Linux kernel documentation, [How To Write Linux PCI Drivers](https://docs.kernel.org/PCI/pci.html), current page checked 2026-09-04. DMA mask setup, bus mastering, resource lifecycle, interrupts and shutdown.
- Linux kernel documentation, [PCI Peer-to-Peer DMA Support](https://docs.kernel.org/driver-api/pci/p2pdma.html), current page checked 2026-09-04. Provider memory, clients, topology, distance and peer mappings.
- Linux kernel documentation, [VFIO](https://docs.kernel.org/driver-api/vfio.html), current page checked 2026-09-04. Secure userspace device access, IOMMU groups, DMA mappings, interrupts and device regions.

## Exercises

### Exercise 1

Design transmit and receive DMA lifecycles for a network driver using coherent descriptor rings and streaming packet buffers. Include masks, errors, barriers, completion, reset and removal.

### Exercise 2

A six-entry input scatter list maps to four device segments. Explain exactly which count and fields drive descriptor creation, synchronization and unmapping, including partial failure.

### Exercise 3

Construct a protection analysis for an untrusted 32-bit DMA device behind an IOMMU on a host with encrypted memory and 64 KiB IOMMU granules.

### Exercise 4

Trace a timeout racing an interrupt, queue reset, runtime suspend and hot-unplug. State when a buffer can be unmapped and freed.

### Exercise 5

Build a verification and assurance plan for a DMA driver across coherent and noncoherent CPUs, direct and translated DMA, bounce buffering, physical and virtual devices, and peer transfers.

## Answers to the Exercises

### Answer 1

During probe, set streaming and coherent masks and fail or reduce features if either required mask is unsupported. Allocate rings coherently, retaining CPU pointers and DMA handles. Allocate packet buffers from supported memory, map transmit fragments `DMA_TO_DEVICE` and receive buffers `DMA_FROM_DEVICE`, check every mapping, store original and mapped SG counts, and apply backpressure on resource failure. Initialize address, length, identifier and flags before a DMA write barrier publishes ownership; notify through the ordered MMIO path.

Completion validates queue, index, generation and device status. Transmit completion precedes unmap and packet release. Receive completion precedes sync or unmap for CPU and payload parsing; reuse synchronizes back for the device. Reset blocks producers, masks interrupts, contains bus mastering, synchronizes handlers, resolves or invalidates every request, establishes a new generation and rebuilds rings. Removal additionally unpublishes interfaces, drains workers, revokes mappings, frees buffers and rings, and disables the function. Surprise loss uses bus/IOMMU containment rather than unsafe device acknowledgement.

### Answer 2

Call the SG mapping API with the six-entry input list and original count six. If it returns zero, no descriptors are published and all request state unwinds. If it returns four, iterate four DMA-mapped entries and obtain addresses and lengths only through the DMA SG accessors. Validate each against descriptor field widths and hardware limits. The four returned segments can represent merges, so input page fields cannot substitute for their DMA fields.

Store both counts with the live mapping. Device descriptors and any mapped-range sync iteration use the API's mapped representation and documented sync interface. Final unmap receives the original list and original count six, plus the unchanged direction; passing four violates the Linux contract. If descriptor allocation fails after mapping, publish no ownership, unmap the whole mapped list with six, and release software descriptors. If separate single mappings were used instead, unwind only the successfully mapped handles in reverse order with their exact sizes and directions.

### Answer 3

Declare the 32-bit mask so the DMA layer knows the device limit. Attach the function to the narrowest viable IOMMU group and domain, map only request pages with direction-derived permissions, and validate that no sibling in the group defeats isolation. Because a 64 KiB IOMMU granule could expose unrelated bytes around a small buffer, use granule-aligned dedicated memory or bounce buffering whose unused area contains no secrets. Never map general encrypted private pages directly if the device or host cannot access them.

For outbound traffic, copy only authorized initialized bytes into shared bounce memory; for inbound traffic, clear padding and copy back only validated lengths after completion. Bound mapping extent arithmetic and descriptor widths. On IOMMU fault, timeout, process death, reset or removal, stop submissions, contain bus mastering, complete translation invalidation, erase shared sensitive buffers, and report affected requests. Measure bounce-pool capacity and reject or backpressure safely on exhaustion. Preserve group topology, mappings, permissions, faults and revocation evidence without logging payload secrets.

### Answer 4

Give each request a state and generation. The timeout atomically changes `submitted` to `uncertain` unless validated completion already won. The interrupt reads authoritative completion records and may move only matching current-generation requests to `complete`; it cannot free an uncertain request without the recovery protocol. Reset and runtime suspend serialize with submission, stop doorbells, mask and synchronize interrupts, and contain the engine before changing translation or power state. Hot-unplug marks disconnected and forces the containment path without relying on MMIO.

A buffer can be unmapped only after one of two proofs: validated normal completion says the device relinquished it, or recovery proves bus mastering and outstanding transactions are contained and IOMMU invalidation is complete. CPU access additionally requires sync-for-CPU for a streaming mapping. Free follows unmap, callback synchronization and removal of every software reference capable of resubmission. Old-generation late completions are recorded and ignored. If containment cannot be proved, quarantine the buffer rather than returning it to the allocator.

### Answer 5

Specify address widths, segment limits, boundaries, allocation sources, mapping type, direction, ownership states, descriptor formats, endian rules, barrier edges, completion identity, IOMMU domain, reset semantics and teardown order. Unit-test size arithmetic, descriptor encoding, ring wrap, generations and state transitions. Cross-build and run sparse and DMA API debugging. Inject allocation and mapping failure at every point and assert exact reverse unmap parameters and zero publication.

Exercise coherent and noncoherent machines, weak ordering, direct DMA, IOMMU translation, translation invalidation, bounce exhaustion and copies, different cache-line sizes, physical revisions, virtual devices, shared buffers and supported peer topology. Stress interrupts, polling, batching, timeout, reset, suspend, process exit and surprise removal across CPUs. Assert no CPU/device overlap for streaming ownership, payload-before-doorbell, completion-before-reuse, mapped-count descriptor use, original-count unmap and contain-before-free. Preserve kernel, firmware, hypervisor, topology, configuration, masks, seeds, traces, faults, performance counters, negative outcomes and limitations; no single platform result proves portability.
