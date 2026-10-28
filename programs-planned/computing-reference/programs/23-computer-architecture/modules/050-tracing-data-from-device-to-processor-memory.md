---
module_id: CA-050
program: Computer Architecture
level: 1
module_number: 50
title: Tracing Data from Device to Processor Memory
status: complete
last_verified: 2026-09-04
---

# Tracing Data from Device to Processor Memory

## One-Page Review

### Governing question

When an input device, network interface, storage controller, or accelerator places data in memory, which identities, address translations, ownership transfers, ordering edges, cache-coherence actions, completion records, and fault decisions make the bytes safe for a processor to consume?

### Essential definitions

- A **data path** carries payload bytes; a **control path** carries descriptors, doorbells, completions, interrupts, faults, and ownership state that govern those bytes.
- A **DMA descriptor** names one or more buffers, lengths, directions, options, and a completion identity.
- A **CPU virtual address** is interpreted by a processor MMU; a **DMA address** or **I/O virtual address** (`IOVA`) is presented by a device and interpreted by the platform DMA path.
- A **requester ID** identifies the device function that originates a transaction; a **process address space ID** (`PASID`) can select a subordinate process context where supported.
- An **IOMMU** selects a device context, translates IOVAs, checks permissions, and reports faults before authorized requests reach system memory.
- A **home agent** or analogous coherence point establishes ownership and ordering for a physical address in a coherent memory hierarchy.
- **DMA-coherent memory** permits CPU and device observations without explicit cache-line clean/invalidate operations, but still requires ordering primitives.
- **noncoherent DMA** requires explicit ownership and cache-maintenance operations appropriate to direction and platform.
- A **completion record** is device-written state proving a particular operation reached its specified completion point; an interrupt is only a notification that work may be available.
- An **epoch** distinguishes work accepted before a reset, teardown, remap, or ownership change from work accepted afterward.

### Central model, mechanism, or theorem

Let a posted receive operation be `D=(requester,context,IOVA,length,direction,slot,epoch)`. Software initializes the buffer and descriptor, makes them visible, and transfers ownership to the device. The device fetches `D`, translates and authorizes every byte, emits one or more memory writes, then publishes a matching completion only after those writes have reached the protocol-defined visibility point. The processor observes returned ownership with the required acquire/DMA synchronization before reading payload. Correctness therefore needs the partial order `publish(D) -> fetch(D) -> payload writes -> completion -> CPU observation`; notification may follow completion but is not itself evidence that payload is visible.

### Critical invariants

- The CPU pointer, physical pages, IOVA ranges, requester context, and device descriptor refer to the same live allocation and generation.
- Every written byte lies within a mapped, writable interval belonging to the descriptor; checked range arithmetic cannot wrap.
- Requester and PASID identity select the intended IOMMU domain and cannot be forged or lost in a bridge.
- Descriptor fields are visible before ownership publication; ownership cannot be held simultaneously by CPU and device.
- Payload writes become visible at the required observer before completion becomes visible; CPU acquire/synchronization precedes payload reads.
- Coherent DMA still uses barriers; noncoherent DMA additionally uses direction-correct cache maintenance and avoids partial-line sharing.
- Completion identity, length, status, slot, and epoch match one outstanding operation exactly once.
- Under a precise commitment model, `requested bytes = completed bytes + residue`; partial failure never becomes silent success.
- Reset, unmap, hot removal, and reassignment cannot free or reuse memory while an old device write can still arrive.
- Interrupt loss or coalescing cannot lose work because software validates completion state in memory.

### Common failures

Common failures include giving a device a CPU virtual pointer, publishing a descriptor before its fields, ringing a doorbell before descriptor visibility, mapping the wrong DMA direction, trusting only the first page of a multi-page range, dropping requester identity, reusing an IOVA before invalidation completes, assuming a posted write has reached DRAM, publishing completion before payload, treating an interrupt as the completion record, reading a noncoherent buffer without synchronization, invalidating a cache line that contains unrelated dirty data, trusting a device-reported length, wrapping a ring without a phase, and freeing memory after reset while late writes remain possible.

### Compact example

An invented receive buffer begins at IOVA `0x10000f80` and contains 5,000 bytes. It spans 128 bytes in one page, 4,096 in a second, and 776 in a third. The three IOVA pages map to noncontiguous physical pages. With modeled memory requests of at most 256 bytes, the device emits 21 requests touching 79 physical cache lines. Those counts say nothing about CPU visibility until a correctly ordered completion and the required processor-side acquire or DMA synchronization occur.

### Connections

Review [Interrupts and Direct Memory Access](042-interrupts-and-direct-memory-access.md), [PCI Express](043-pci-express.md), [I/O Memory Management Units](046-i-o-memory-management-units.md), and [System-on-Chip Integration](049-system-on-chip-integration.md). The next block begins with [Instruction-Level Parallelism](../ROADMAP.md#block-06--out-of-order-and-speculative-execution), where the processor side of ordering and latency becomes more detailed.

## Governing Question

“The device wrote the buffer” compresses several distinct claims. The device may have accepted an input into local SRAM, issued a posted interconnect request, passed an IOMMU, updated a coherent cache, reached a memory controller, written a completion entry, or merely raised an interrupt. None of those events implies all the others without a stated protocol.

The architectural problem is to trace one identified payload and its control state from source to a processor-observable byte sequence. A valid trace names each address space, enforcement point, ownership state, ordering edge, completion point, and failure boundary. It does not replace them with an arrow labeled “DMA.”

## Why This Matters

Modern devices routinely move data without a processor copying each word. A network interface receives packets, an NVMe controller returns blocks, a camera produces frames, and an accelerator emits results into system memory. DMA saves instruction and cache bandwidth, but it creates another active memory agent with its own address space, queues, caches, reorderings, and failures.

Data-path defects are difficult because control can appear healthy. An interrupt can arrive for stale data; a completion can name the wrong generation; an IOMMU mapping can cover the first page but not the last; a CPU cache can retain an old line; or a reset can be reported complete while a fabric still holds posted writes. The resulting symptom may be rare corruption far from the violated contract.

A disciplined trace provides a shared explanation for architecture, firmware, kernel, driver, device, verification, security, and performance work. It also separates what was observed in one implementation from what the governing specifications guarantee.

## Prerequisites and Retrieval

Before studying this module, be able to:

- distinguish CPU virtual, system physical, bus, and I/O virtual addresses;
- explain descriptors, rings, DMA direction, interrupts, and MMIO doorbells;
- trace a PCIe or on-chip request through requester, interconnect, and completer identities;
- explain page translation, IOTLBs, mapping invalidation, and least privilege;
- distinguish cache coherence from memory ordering;
- use half-open intervals and checked arithmetic for byte ranges;
- distinguish a completion record from an interrupt notification;
- reason about ownership, happens-before, finite queues, reset, and partial failure.

For a real trace, retrieve the exact device and firmware revision; queue format; descriptor and completion layouts; negotiated features; DMA mask; requester/stream/PASID identities; IOMMU mode and page tables; ATS or device translation-cache state; coherence attributes; interconnect route; NUMA/home node; cache-line size; memory type; barrier/accessor semantics; interrupt vector and moderation state; ring indices/phases; reset generation; error logs; and the platform errata. A generic diagram cannot substitute for those facts.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish the payload data path from the control path that authorizes and completes it;
2. translate one buffer consistently across CPU virtual, physical, DMA, and IOMMU address spaces;
3. trace descriptor publication, doorbells, device fetch, payload writes, completion, notification, and CPU observation;
4. state the ordering and ownership invariants needed for coherent and noncoherent DMA;
5. calculate page, request, cache-line, ring, and byte-commit boundaries;
6. analyze IOMMU, interconnect, coherence, memory-controller, and NUMA consequences;
7. diagnose stale data, overruns, wrong-domain writes, lost wakeups, and generation reuse;
8. contain partial completion, reset, hot removal, and late device writes;
9. measure latency and traffic at named points without confusing them with end-to-end goodput;
10. construct verification evidence for one complete device-to-processor-memory path.

## Core Exposition

### Name the transfer and its completion point

Begin with a single operation: for example, “receive packet `p` into queue slot 37 in epoch 12” or “read storage command 814 into buffer `b`.” Record its direction, maximum length, descriptor identity, completion identity, and failure semantics.

Also state what “complete” means. It may mean that the device consumed a descriptor, that all payload writes reached a coherent visibility point, that a completion entry was published, or that software reclaimed the buffer. These are different milestones.

### Draw two paths, not one

The **data path** begins at device input or device-local state and ends in a CPU-observable memory region. The **control path** usually runs in both directions: software allocates and maps memory, fills descriptors, publishes a producer index, writes a doorbell, later observes completion, and returns buffers.

The paths meet through identities. A payload without a matching descriptor is unauthorized; a completion without matching payload visibility is premature; an interrupt without a completion is only a prompt to inspect state.

### Allocate memory with a lifetime

Software first obtains pages or buffers whose lifetime exceeds every possible device access. Virtual contiguity does not imply physical contiguity. Pages may need pinning, may be collected into a scatter-gather list, or may be represented through an IOMMU as one contiguous IOVA range.

The allocation's owner must know when it is safe to release. A timeout or function reset is not sufficient if an interconnect, device queue, or translation cache can still produce a write.

### Map through the platform DMA interface

Portable software asks the platform DMA layer to map the buffer for a specific device and direction. The returned DMA address is the address placed in the descriptor; it is not generally a CPU pointer or raw physical address. The [Linux DMA mapping guide](https://docs.kernel.org/core-api/dma-api-howto.html) explicitly distinguishes CPU virtual, CPU physical, and device/bus addresses and explains coherent versus streaming mappings.

Mapping may install IOMMU entries, choose bounce buffers, constrain addresses to the device's mask, merge scatter segments, and arrange cache behavior. The driver must check mapping success and use the returned segment list rather than assuming the input list survived unchanged.

### Define direction as an access contract

For a device-to-memory transfer, the device needs write permission. A bidirectional mapping is not a harmless default: it weakens protection and can require more cache work. Direction also tells the platform which side's dirty data must be preserved and when synchronization is required.

Separate payload buffers from bidirectional descriptor or completion structures when their access patterns differ. Least privilege applies to bytes and operations, not just devices.

### Initialize queue state before enabling activity

Set ring base addresses, sizes, producer/consumer positions, phase bits, interrupt vectors, IOMMU domains, and device features while the queue is stopped. Install the handler or polling mechanism before enabling notifications. Validate that firmware, OS, IOMMU, and device agree on requester identity.

The initial empty/full interpretation must be unambiguous. A ring with equal indices needs another fact—occupancy, a reserved slot, or phase/generation—to distinguish empty from full.

### Construct a descriptor completely

Populate every address, length, flag, segment link, buffer capacity, and correlation field while software owns the slot. Validate checked `start + length`, segment count, device limits, alignment, and that every writable byte belongs to the allocation.

Descriptor fields are part of the trust boundary. A device may return hostile or corrupted lengths and flags; software must retain independent capacity and ownership metadata rather than trusting a round trip through device-controlled memory.

### Publish memory before ownership

The descriptor and any data it references must become visible before software changes the ownership bit or producer index that lets the device consume it. Even coherent DMA memory requires a suitable ordering primitive; coherence does not prevent CPU store reordering. The [Linux memory-barrier documentation](https://docs.kernel.org/core-api/wrappers/memory-barriers.html) gives the canonical pattern of data first, a DMA write barrier, and ownership second.

Publication is a release operation over a precise observer set. A compiler-only barrier cannot make cache lines or interconnect writes visible to a device.

### Ring the doorbell with the correct I/O semantics

After publishing queue state, software may write an MMIO doorbell. An ordered I/O accessor can provide ordering that a relaxed accessor does not; the required primitive is platform-specific. The [Linux device-I/O documentation](https://docs.kernel.org/driver-api/device-io.html) distinguishes ordered and relaxed accessors and posted-write considerations.

A doorbell is a hint or index update, not ownership of uninitialized entries. Batching several descriptors behind one doorbell amortizes MMIO cost but increases queueing latency.

### Fetch and validate at the device

The device reads the new producer state, fetches descriptors, and checks format, supported lengths, flags, alignment, queue generation, and available local resources. A robust device does not issue payload writes from a malformed descriptor merely because the address translated.

Descriptor fetch itself is a DMA read and can fault, time out, or observe stale state. Its request identity and ordering need the same trace discipline as payload writes.

### Acquire data at the device boundary

For an input device, bytes first enter a PHY, protocol engine, sensor interface, media controller, or device-local buffer. Error detection, framing, decompression, or integrity checks may occur before DMA. Define whether bad data is discarded, delivered with status, or partially written.

“Received by the device” is not “stored in processor-visible memory.” Local FIFO occupancy and backpressure determine whether the device can preserve input while waiting for descriptors, translations, credits, or memory service.

### Attach authentic transaction identity

Every memory request must carry the requester or stream identity assigned to the function. If PASID or another process selector is enabled, its use must be authorized for that requester. Bridges may translate encodings but must preserve the authenticated context.

Identity selects protection and attribution. A correct address under the wrong requester can map to another tenant; a correct requester with a forged PASID can select another process.

### Translate and authorize every byte

The IOMMU selects a device context and translates the IOVA page by page, checking operation permissions and output bounds. A request crossing a page or protection boundary must be split or rejected according to the architecture; validating only its first byte is insufficient.

IOMMUs can cache device contexts and translations. Current [RISC-V IOMMU documentation](https://docs.riscv.org/reference/iommu/v20260222/iommu_data_structures.html) explicitly describes cached device, process, first-stage, second-stage, and MSI translation structures. Map changes therefore require the architecture's invalidation and completion protocol, not only page-table stores.

### Account for ATS and device-side translations

With Address Translation Services or analogous facilities, the device can cache translations and issue translated requests. The trace then includes the device translation cache, translation requests, permissions, invalidations, and generation reuse. PASID may permit multiple process address spaces behind one function.

Stopping CPU page-table use does not revoke cached device translations. Teardown must cover both IOMMU and device observers before physical pages are reused.

### Packetize the memory write

A logical payload becomes one or more bus or interconnect transactions constrained by maximum payload, alignment, page boundaries, byte enables, credits, and device implementation. Transaction count therefore depends on starting offset as well as length.

Track each transaction's logical byte interval and translated physical interval. The union must equal the committed logical bytes; unintended overlaps, gaps, duplication, or wrap are failures even if the total byte count happens to match.

### Traverse bridges and the host interconnect

PCIe switches, root ports, on-chip fabrics, protocol bridges, and width/clock adapters route and buffer requests. Posted writes can leave the requester without an end-to-end response. Their acceptance transfers responsibility downstream but does not prove immediate CPU visibility or a DRAM write.

The route must preserve source identity, byte enables, ordering attributes, poison/error state, and failure attribution. A bridge that silently changes an error into success breaks the end-to-end contract.

### Reach the coherent memory system

At the processor complex, a request may enter a home agent, last-level cache, coherent interconnect, memory controller, or a platform-specific I/O cache. “Processor memory” means the system memory address space observable by processors; it does not guarantee that the newest bytes physically reside in DRAM.

For a coherent requester, the coherence machinery establishes a single current value and resolves conflicting cached copies according to the platform protocol. For a noncoherent requester, software must arrange that stale CPU cache state cannot hide or overwrite device results.

### Distinguish coherence from ordering

Coherence answers which value a location has and how cached copies converge. Ordering answers when operations to different locations become observable relative to one another. A device can write coherent payload and completion memory yet expose completion first unless the device/interconnect ordering contract prevents it.

The required property is not “the bus is coherent” but “all payload writes for descriptor generation `g` are ordered before the completion that returns generation `g` to software.”

### Handle noncoherent caches by ownership

On a noncoherent path, CPU and device do not freely access a buffer at the same time. Before device ownership, software performs the platform's mapping or sync-for-device operation. After completion, it performs sync-for-CPU or unmaps before reading.

Cache maintenance operates at cache-line granularity. Two independently owned objects must not share a line if invalidating one could discard dirty bytes from the other. Page or cache-line alignment is therefore a correctness issue, not merely a performance preference.

### Publish completion after payload

The device writes status, actual length, error flags, and generation into a completion entry or descriptor. It must order payload writes before the ownership/phase field that software uses as the completion indicator. The [Virtio 1.3 specification](https://docs.oasis-open.org/virtio/virtio/v1.3/virtio-v1.3.html) provides a concrete standardized queue model with separate descriptor, driver, and device areas plus explicit barrier requirements.

The completion point must say whether all bytes are visible, whether some are merely accepted by an intermediate component, and how poison or partial failure is represented.

### Treat notification as a wakeup

After completion publication, the device may emit MSI/MSI-X, assert a line, update an event index, or rely on polling. Interrupt coalescing and suppression deliberately allow many completions per notification, and races can make a notification unnecessary.

Correct software drains completion state until its queue protocol says no work remains, then reenables or rechecks notification without a lost-wakeup window. An interrupt count is not a payload or completion count.

### Observe completion with acquire semantics

The CPU reads the completion ownership or phase field using the queue's required synchronization. Once returned ownership is observed, an acquire or DMA read barrier orders subsequent reads of length, status, and payload after device publication.

On noncoherent systems, cache synchronization is also required. A CPU memory barrier alone does not invalidate stale cache lines; a cache operation alone does not necessarily impose the needed ordering between completion and data.

### Validate before exposing bytes

Compare device-reported length with the posted capacity, validate segment count and status, reject impossible combinations, and check integrity metadata where available. Do not let a corrupt length turn a bounded DMA into an out-of-bounds software read.

Only after validation does software hand the initialized byte interval to a network stack, filesystem, userspace, or accelerator consumer. Bytes beyond actual length remain uninitialized or retain old data and must not be exposed.

### Recycle only after the final consumer

Returning a receive buffer while another CPU or subsystem still references it creates a use-after-recycle even if the DMA was correct. The higher-level ownership protocol must return the buffer to the driver before it is synchronized, remapped if necessary, republished, and given back to the device.

Ring indices and epochs prevent an old completion from reclaiming a new use of the same slot. Address reuse alone is never a sufficient identity.

### Trace storage queues as the same pattern

In a memory-based NVMe transport, host software writes commands into submission queues, rings a tail doorbell, the controller transfers data using described memory pages or scatter-gather lists, posts completion queue entries, and may signal an interrupt. The current [NVMe Base 2.3 and transport specifications](https://nvmexpress.org/nvm-express-specification-archives/) make queue identity and completion state explicit.

The media operation, controller-local caching, payload DMA, completion posting, and durable persistence are separate completion domains. A successful memory transfer is not automatically proof that data is durable on media.

### Trace receive and transmit symmetrically but not identically

For receive, device writes payload and software consumes it. For transmit, software initializes payload, publishes it, and device reads it. The direction reverses cache-maintenance and trust questions; transmit completion says when software may reclaim memory, not necessarily when a remote peer received data.

A bidirectional accelerator may read inputs and write outputs under one command. Model each region and direction independently, then join them at a command completion with explicit ordering.

### Handle partial faults precisely

An IOMMU fault, poison, link failure, device-local overflow, or memory error can occur after some writes. Define the commitment point and whether later writes are suppressed. Preserve `completed_bytes`, residue, and affected intervals rather than reporting one undifferentiated failure.

Retry is safe only when repeating already committed effects is harmless or when the protocol resumes from an exact uncommitted boundary. Input streams and device side effects are often not replayable.

### Quarantine reset and late traffic

Reset stops a function's visible logic but may not instantly remove posted requests from every buffer. Stop new submissions, disable notifications, fence or drain device activity, invalidate translations, wait for architecture-defined completion, and retain memory until late writes are impossible.

Increment an epoch when a queue is recreated. A completion from an old epoch is contained and logged; it cannot return ownership of the same slot in the new queue.

### Respect virtualization boundaries

Virtual functions, mediated devices, and emulated virtqueues add hypervisor mappings, interrupt remapping, guest-physical translation, and migration state. Trace guest virtual to guest physical to system physical addresses where applicable, and bind requester/PASID to the correct guest.

A shared physical queue, reset domain, or completion vector can couple tenants even when page mappings are disjoint. Isolation includes finite resources and control paths as well as addresses.

### Place work near memory deliberately

Queue affinity, interrupt routing, IOMMU placement, home-node selection, and page allocation affect NUMA traffic. A device attached to one socket writing pages homed on another can cross multiple interconnects before the consuming CPU reads them.

Measure where bytes travel rather than assuming the nearest CPU is the nearest memory. Locality optimization must preserve queue ownership and interrupt correctness during CPU or device migration.

### Decompose latency and traffic

End-to-end latency can include device ingress, local buffering, descriptor fetch, IOTLB lookup or page walk, fabric queueing, memory service, completion write, interrupt moderation, interrupt delivery, scheduler delay, and CPU synchronization. Report a distribution, not only an average.

Traffic includes descriptor reads, payload writes, completion writes, translations/page walks, coherence probes, writebacks, interrupts, and software reads. Payload bytes divided by link bandwidth ignores most of this work.

### Observe named boundaries

Useful evidence includes device queue indices, descriptor/completion snapshots, requester and IOMMU fault logs, fabric counters, PCIe errors, memory-controller traffic, cache/coherence counters, interrupt timestamps, and CPU tracepoints. All observations need a common operation ID or time correlation.

Instrumentation can perturb ordering and timing. A trace that observes only software timestamps cannot establish the internal device-to-memory sequence.

### Verify by refinement and fault injection

Build a reference model that maps each accepted descriptor to authorized logical and physical intervals, expected completion identity, and ownership transitions. Scoreboard observed requests and completions against it. Assert that no unauthorized byte is written and that returned ownership implies the required payload visibility.

Inject missing pages, permission errors, stale IOTLB entries, delayed writes, completion-before-data, corrupt lengths, ring wrap, notification suppression, reset, surprise removal, and finite-queue pressure. Combine simulation, formal properties, IOMMU guard pages, driver tests, hardware traces, and performance counters; no one layer proves the whole path.

## Definitions and Notation

- `D=(rid,pasid,iova,n,dir,slot,epoch)`: one descriptor with requester identity, optional process context, byte interval, direction, ring identity, and generation.
- `V`: CPU virtual interval owned by software.
- `P`: system-physical page intervals backing `V`.
- `I`: device-visible IOVA intervals returned by the DMA mapping layer.
- `T_g(rid,pasid,I,op)`: IOMMU translation and permission relation in generation `g`.
- `W_i=[l_i,u_i) -> [p_i,q_i)`: logical payload interval mapped by one authorized device write to a physical interval of equal length.
- `C=(slot,epoch,status,completed,residue)`: completion record.
- `O_cpu(slot,epoch)`: processor observation that ownership has returned for that exact generation.
- `P_D`: software publication of a complete descriptor.
- `F_D`: device fetch/acceptance of that descriptor.
- `N`: optional notification event; correctness cannot require one notification per completion unless the protocol explicitly promises it.
- `hb`: the required happens-before or visibility relation for the named observers; its implementation depends on the platform protocol.
- `line(x)`: physical cache line containing address `x`.

Use half-open ranges so interval length is `u-l`. Compute endpoints with checked arithmetic before translation. “Physical” means the system-physical address used at the memory-system boundary; device, guest, and CPU-visible address spaces can differ.

## Mechanisms, Invariants, or Proof Structure

1. **Allocation obligation:** every payload byte belongs to a live allocation whose lifetime covers all possible DMA.
2. **Naming obligation:** CPU virtual, physical, IOVA, descriptor, requester, PASID, slot, and epoch names resolve to one operation.
3. **Publication obligation:** descriptor/data initialization happens before device-visible ownership publication and notification.
4. **Identity obligation:** authentic requester and process identity select the intended IOMMU context through every bridge.
5. **Range obligation:** checked full ranges—not only starting addresses—are mapped, permitted, and within device/address-width limits.
6. **Translation obligation:** IOTLB and device-cache entries match the live mapping generation, page size, operation, and permissions.
7. **Byte-refinement obligation:** authorized writes cover exactly the committed logical intervals with equal-length physical intervals and no unintended overlap.
8. **Ordering obligation:** all payload writes reach the required visibility point before completion publication becomes observable.
9. **Coherence obligation:** coherent attributes or explicit cache maintenance prevent stale or destructive CPU cache state.
10. **Ownership obligation:** software and device never mutate a descriptor or payload concurrently outside a documented shared protocol.
11. **Completion obligation:** exactly one matching completion reports status, length, residue, slot, and epoch for each terminal operation.
12. **Observation obligation:** processor acquire/DMA synchronization precedes interpretation of device-written metadata and payload.
13. **Notification obligation:** interrupt, polling, and suppression logic cannot lose completion work or create false completion.
14. **Revocation obligation:** unmap, reset, removal, or reassignment completes before pages, IOVAs, IDs, or slots are reused.
15. **Progress obligation:** descriptor, translation, fabric, completion, and notification resources cannot form an unbroken wait cycle under stated fairness.
16. **Evidence obligation:** conclusions bind exact hardware, firmware, IOMMU, OS/driver, topology, configuration, workload, and errata.

A safety proof sketch composes three refinements. First, descriptor publication refines software-owned state into one device-owned operation. Second, translation and packetization refine that operation into authorized physical byte writes. Third, completion publication and processor acquire refine those writes into one CPU-owned initialized interval. Liveness is conditional on device input, descriptor availability, translation service, interconnect credits, memory response, completion capacity, and processor service. Notification is an optimization on that liveness path, not a safety premise.

For partial failure, let the pairwise-disjoint committed logical intervals be `K={K_1,...,K_m}`. Require each `K_i` to map to an equal-length authorized physical interval, require their ordered union to be a prefix or another explicitly permitted subset, and define `completed=sum(|K_i|)` and `residue=requested-completed`. A count alone cannot prove correctness because duplicated and omitted intervals can have the same sum.

## Alternatives and Trade-Offs

1. **Coherent versus noncoherent DMA:** coherence simplifies sharing; noncoherent paths can reduce hardware traffic but require strict ownership and cache maintenance.
2. **Contiguous allocation versus scatter-gather:** contiguity simplifies descriptors; scatter-gather avoids copying and large contiguous allocation pressure.
3. **Physical addressing versus IOMMU translation:** direct addressing reduces translation work; IOMMUs add isolation, remapping, and contiguous IOVA construction.
4. **IOMMU page walks versus ATS:** centralized walks simplify control; device-cached translations reduce latency but expand invalidation and trust state.
5. **One descriptor per buffer versus chained descriptors:** one entry is simple; chains represent fragmented or structured data with more validation risk.
6. **Inline completion versus separate completion queue:** inline ownership reduces structures; a completion queue supports dense batching and independent producer/consumer flow.
7. **Interrupts versus polling:** interrupts save idle CPU; polling lowers wakeup overhead at sustained load but consumes processor time.
8. **Immediate notification versus moderation:** immediate signals minimize light-load latency; batching reduces interrupts and can worsen tail latency.
9. **Deep rings versus shallow rings:** depth absorbs bursts; it increases queued latency, memory footprint, and reset uncertainty.
10. **Posted versus acknowledged data writes:** posted writes improve throughput; explicit acknowledgment simplifies completion reasoning at higher transaction cost.
11. **Large versus small IOMMU pages:** large pages reduce translation pressure; small pages give finer protection and reduce overmapping.
12. **Bounce buffers versus direct mapping:** bounce buffers satisfy addressing/alignment and isolate partial lines; they add copying and memory traffic.
13. **Shared versus per-queue mappings:** sharing reduces setup cost; per-queue domains narrow blast radius and simplify tenant attribution.
14. **NUMA-local allocation versus flexible placement:** locality lowers interconnect traffic; flexible placement improves capacity balance and failover options.
15. **Device offload versus CPU processing:** offload reduces CPU work; it adds opaque state, metadata contracts, and verification surface.

## Failure Modes and Misconceptions

1. “A DMA address is a physical address.” An IOMMU, host bridge, or bounce layer may translate it.
2. “A CPU pointer can be stored in a descriptor.” The device generally cannot interpret a CPU virtual address.
3. “Virtual contiguity means one physical segment.” Page mappings can be discontiguous.
4. “Mapping the first byte authorizes the request.” Every crossed page and byte needs permission.
5. “Read/write direction describes the CPU.” DMA direction is conventionally named from the device's perspective; use the selected API precisely.
6. “Coherent memory needs no barriers.” Coherence does not prohibit CPU or device reordering.
7. “A barrier flushes stale cache lines.” Ordering and cache maintenance are distinct operations.
8. “Invalidating a receive buffer is always safe.” It can discard unrelated dirty data in a shared cache line.
9. “Publishing the producer index publishes prior fields automatically.” Only the specified release/barrier sequence provides that edge.
10. “A doorbell causes the device to reread everything.” Queue protocols define what indices and ownership the device consumes.
11. “The device sees descriptors in CPU program order.” Compiler, CPU, cache, bridge, and fabric ordering all matter.
12. “Requester identity is only for logging.” It selects IOMMU and interrupt-remapping policy.
13. “An IOTLB invalidation is complete when issued.” Reuse waits for the architecture's completion and in-flight containment.
14. “An IOMMU prevents malformed descriptors.” It limits addresses and permissions; length, format, and semantic validation remain necessary.
15. “A posted write has reached DRAM when issued.” It may reside in device, bridge, cache, home-agent, or controller state.
16. “DMA always bypasses processor caches.” Coherent platforms can place or reconcile data through cache hierarchy mechanisms.
17. “Completion means persistence.” Queue completion, CPU visibility, controller cache, and durable media are different domains.
18. “An interrupt proves one completion.” Interrupts can be coalesced, suppressed, duplicated by handling races, or unrelated.
19. “No interrupt means no work.” Polling and lost-wakeup avoidance require checking shared completion state.
20. “Actual length is trustworthy.” It is device-controlled input bounded by the posted capacity.
21. “Equal producer and consumer indices mean empty.” Without phase or occupancy, they can also mean full.
22. “Reset cancels posted writes.” Old writes can remain in device or fabric state unless explicitly drained or contained.
23. “Unmapping immediately revokes the device.” Translation caches and in-flight requests need invalidation and completion.
24. “Reusing the same slot is safe after timeout.” A late completion needs an epoch to avoid ABA confusion.
25. “Payload byte count proves correct placement.” Gaps and duplicates can preserve a total count.
26. “Peak link bandwidth predicts CPU-visible throughput.” Translation, packetization, coherence, memory, completion, scheduling, and software all contribute.
27. “One successful trace proves the design.” Boundary, adversarial, reset, load, and failure cases need independent evidence.

## Worked Examples

### Example 1

A coherent NIC receive queue contains slot 37 in epoch 12. Software maps a 2 KiB buffer, writes its DMA address and capacity into the descriptor, executes the required DMA write barrier, advances the producer index, and writes the doorbell. The NIC receives a 1,500-byte frame, writes those bytes, orders them before a completion containing `(slot=37,epoch=12,length=1500,status=ok)`, and signals MSI-X.

The CPU handler drains the completion queue, observes its phase with the required acquire/DMA read barrier, bounds 1,500 by 2,048, and only then parses the frame. No cache clean/invalidate is required for this coherent mapping, but the publication and observation barriers remain. **Conclusion:** coherence removes explicit cache maintenance, not ownership, range validation, or ordering.

### Example 2

On a noncoherent system, a CPU previously read a receive buffer and retains an old cache line. The device later writes new payload to memory and returns ownership. If the CPU reads without `sync-for-CPU` or the platform equivalent, it can observe the cached old bytes even after seeing a new completion.

The repair is to keep the CPU off the device-owned buffer, perform direction-correct synchronization after completion, and then acquire/validate metadata before consuming data. A generic CPU fence alone cannot invalidate the stale line. **Conclusion:** completion visibility and payload cache visibility are separate obligations.

### Example 3

A 5,000-byte receive starts 128 bytes before a 4 KiB IOVA boundary. It spans three pages: 128, 4,096, and 776 bytes. The IOMMU maps those pages to three noncontiguous physical pages with write permission. Packetization produces one request for the first fragment, sixteen 256-byte requests for the full page, and four for the final fragment.

The logical intervals are adjacent while physical intervals need not be. Verification compares their ordered logical union with `[0,5000)` and checks each translated physical range. **Conclusion:** a contiguous IOVA makes the descriptor simple but does not make the physical path contiguous.

### Example 4

A descriptor covers 6 KiB, but only its first IOVA page is writable; the second is read-only. The device writes the first 4 KiB and faults on the next page under a platform that permits partial completion. The completion reports `completed=4096`, `residue=2048`, and an IOMMU permission status.

Software must not report success or replay all 6 KiB blindly. It quarantines the buffer, correlates the fault with requester and epoch, and applies the device protocol's recovery rule. **Conclusion:** protection prevents unauthorized bytes, while the device contract must still describe already committed bytes.

### Example 5

A faulty device emits payload writes and a completion write on paths where completion can overtake payload. The CPU sees the completion phase, then reads partially old data. Raising the interrupt later does not repair the missing ordering edge because the completion itself was premature.

The device must apply the interconnect-specific ordering rule so payload reaches the required visibility point before completion publication; software must use the matching acquire sequence. **Conclusion:** notification order cannot substitute for data-before-completion order.

### Example 6

Two receive buffers share one noncoherent cache line. The CPU modifies metadata beside buffer A while the device owns buffer B. Synchronizing B by invalidating the shared line discards the dirty metadata for A, even though the device never addressed A.

Aligning and padding independently owned buffers, or using a safe bounce/copy scheme, prevents destructive maintenance. **Conclusion:** protection at byte granularity is insufficient when coherence actions operate at cache-line granularity.

### Example 7

A completion ring wraps so producer and consumer indices are both 5. An interrupt is suppressed because the device believes the CPU is polling. Without phase bits, software can misclassify a full set of new entries as empty and sleep forever.

With a phase per entry, software recognizes the new generation, drains all completions, publishes its consumer position, reenables notification, and rechecks the ring to close the lost-wakeup race. **Conclusion:** durable work state lives in the ring; notification only accelerates discovery.

### Example 8

An NVMe read command names host memory through PRP or scatter-gather structures. Host software publishes the submission entry and rings the submission-queue tail doorbell. The controller fetches the command, transfers block data into the named pages, posts a completion identified by submission queue and command ID, and may interrupt.

The CPU checks the completion phase and status before using the data. That completion establishes the NVMe command's specified host-visible result, not a generic claim about every storage or persistence domain. **Conclusion:** the same descriptor-data-completion pattern applies, but the protocol defines the exact milestone.

### Example 9

A queue times out and the function is reset. Software immediately reuses slot 12 and its IOVA for a new buffer. A delayed old payload write and completion then arrive, corrupting the new buffer and apparently completing the new request—an ABA failure.

Safe teardown fences or drains the function, invalidates translations, waits for required completion, and retains old memory until late traffic is impossible. Queue recreation increments the epoch so an old completion is rejected. **Conclusion:** reset indication alone is not proof of DMA revocation.

### Example 10

This deterministic model translates the compact example page by page, packetizes each physical segment into requests of at most 256 bytes, and counts distinct 64-byte physical cache lines.

<!-- bijux-verify: {"id":"device-memory-path-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"range iova=[0x10000f80,0x10002308) bytes=5000\nsegment=1 iova=[0x10000f80,0x10001000) physical=[0x80000f80,0x80001000) bytes=128 requests=1\nsegment=2 iova=[0x10001000,0x10002000) physical=[0x90000000,0x90001000) bytes=4096 requests=16\nsegment=3 iova=[0x10002000,0x10002308) physical=[0xa0000000,0xa0000308) bytes=776 requests=4\nsummary segments=3 requests=21 cache_lines=79\nownership=device_written completion=published interrupt=1 cpu_visible=after_acquire\n","stderr":""}} -->
```python
page_bytes = 4096
request_bytes = 256
cache_line_bytes = 64
start = 0x10000F80
length = 5000
end = start + length

page_map = {
    0x10000000: 0x80000000,
    0x10001000: 0x90000000,
    0x10002000: 0xA0000000,
}

segments = []
cursor = start
while cursor < end:
    iova_page = cursor - cursor % page_bytes
    segment_end = min(end, iova_page + page_bytes)
    physical_start = page_map[iova_page] + (cursor - iova_page)
    physical_end = physical_start + (segment_end - cursor)
    requests = (segment_end - cursor + request_bytes - 1) // request_bytes
    segments.append((cursor, segment_end, physical_start, physical_end, requests))
    cursor = segment_end

assert sum(iova_end - iova_start for iova_start, iova_end, _, _, _ in segments) == length
print(f"range iova=[0x{start:08x},0x{end:08x}) bytes={length}")

cache_lines = set()
for number, (iova_start, iova_end, physical_start, physical_end, requests) in enumerate(segments, 1):
    first_line = physical_start // cache_line_bytes
    last_line = (physical_end - 1) // cache_line_bytes
    cache_lines.update(range(first_line, last_line + 1))
    print(
        f"segment={number} iova=[0x{iova_start:08x},0x{iova_end:08x}) "
        f"physical=[0x{physical_start:08x},0x{physical_end:08x}) "
        f"bytes={iova_end - iova_start} requests={requests}"
    )

print(
    f"summary segments={len(segments)} requests={sum(item[4] for item in segments)} "
    f"cache_lines={len(cache_lines)}"
)
print("ownership=device_written completion=published interrupt=1 cpu_visible=after_acquire")
```

The addresses, page mappings, request limit, cache-line size, and perfect completion are invented. The script checks range decomposition and arithmetic only; it does not model an actual PCIe payload-boundary rule, IOMMU implementation, cache protocol, memory controller, or hardware ordering. **Conclusion:** numerical trace evidence is useful only when its abstraction boundary is explicit.

## Cross-Program Connections

- **Operating Systems:** DMA APIs, page pinning, cache synchronization, IRQ handling, queue lifetimes, and device reset realize the software side of the trace.
- **Concurrent Programming:** release/acquire publication, exclusive ownership, phase bits, ABA avoidance, and lost-wakeup reasoning govern CPU-device concurrency.
- **Network Engineering:** receive framing, queue selection, checksums, packet lengths, and backpressure define what NIC payload means.
- **Database and Storage Engineering:** queue completion, write ordering, controller caches, and durability boundaries prevent false persistence claims.
- **Security Engineering:** requester identity, least-privilege mappings, guard pages, PASID authorization, and revocation contain hostile or faulty devices.
- **Distributed Systems:** notification is a hint, duplicate/late messages need identities, and partial failure requires explicit commitment semantics.
- **Performance Engineering:** packetization, translation, coherence, NUMA, batching, moderation, and CPU scheduling determine end-to-end tails.
- **Formal Methods:** interval refinement, ownership state machines, generations, safety, and conditional liveness structure verification.
- **Systems Engineering:** the complete path is an interface chain whose claims need requirement-to-evidence traceability across components.

## References

1. Linux kernel, [Dynamic DMA Mapping Guide](https://docs.kernel.org/core-api/dma-api-howto.html), CPU, physical, and DMA addresses; coherent and streaming mappings; current documentation retrieved 2026-09-04.
2. Linux kernel, [Memory Barriers](https://docs.kernel.org/core-api/wrappers/memory-barriers.html), DMA ownership publication and observation ordering; current documentation retrieved 2026-09-04.
3. Linux kernel, [Bus-Independent Device Accesses](https://docs.kernel.org/driver-api/device-io.html), MMIO accessors, relaxed ordering, and posted writes; current documentation retrieved 2026-09-04.
4. RISC-V International, [RISC-V IOMMU Architecture Specification Library](https://docs.riscv.org/reference/iommu/v20260222/iommu_intro.html), device/process contexts, translation, ATS/PRI, and interrupt support; retrieved 2026-09-04.
5. OASIS Open, [Virtual I/O Device (VIRTIO) Version 1.3](https://docs.oasis-open.org/virtio/virtio/v1.3/virtio-v1.3.html), descriptor, driver, and device queue areas with publication and completion rules; Committee Specification Draft 01 dated 2023-10-06, latest-stage page retrieved 2026-09-04.
6. NVM Express, [NVM Express Base Specification Revision 2.3](https://nvmexpress.org/wp-content/uploads/NVM-Express-Base-Specification-Revision-2.3-2025.08.01-Ratified.pdf), submission/completion queue and command/data model; ratified 2025-08-01, retrieved 2026-09-04.
7. NVM Express, [NVMe over PCIe Transport Specification Revision 1.3](https://nvmexpress.org/wp-content/uploads/NVM-Express-NVMe-over-PCIe-Transport-Specification-Revision-1.3-2025.08.01-Ratified.pdf), PCIe doorbells, data transfer, interrupts, reset, and error binding; ratified 2025-08-01, retrieved 2026-09-04.
8. PCI-SIG, [PCI Express Specifications Library](https://pcisig.com/specifications), current base, ordering, ATS, PASID, virtualization, and test specification catalogue; retrieved 2026-09-04.
9. John L. Hennessy, David A. Patterson, and Christos Kozyrakis, *Computer Architecture: A Quantitative Approach*, 7th ed., Morgan Kaufmann/Elsevier, 2025, I/O, memory hierarchy, interconnect, and quantitative evaluation foundations.

## Exercises

### Exercise 1

Define CPU virtual address, system-physical address, IOVA, requester ID, completion record, notification, coherence, and ordering. Then put descriptor publication, doorbell, device fetch, translation, payload writes, completion, interrupt, CPU acquire, and payload read in a defensible partial order.

### Exercise 2

A receive begins at IOVA `0x40000e00` with length 5,632 bytes. It uses 4 KiB pages mapped to physical bases `0x81000000`, `0x92000000`, and `0xb3000000`. Trace the IOVA and physical segments, number of at-most-512-byte requests per segment, and distinct 64-byte physical cache lines.

### Exercise 3

A driver sees a valid completion and correct length but intermittently reads the previous packet's first 64 bytes on one noncoherent platform. Diagnose the violated obligations and design a focused experiment that distinguishes publication ordering, cache maintenance, premature completion, and slot-generation errors.

### Exercise 4

Compare coherent DMA with noncoherent streaming DMA, and compare interrupt-driven completion with polling, for a 100 Gb/s multiqueue NIC. Choose one combination for low sustained traffic and one for saturated traffic, stating correctness invariants and measurements that could change the choice.

### Exercise 5

An accelerator uses PASID, ATS, shared virtual memory, bidirectional input/output buffers, and completion polling. Design an end-to-end isolation, revocation, reset, and verification argument for reassigning one process context while other contexts continue running.

## Answers to the Exercises

### Answer 1

A CPU virtual address is interpreted by a processor page table; a system-physical address names the memory-system destination; an IOVA is a device-visible address translated or passed by the DMA path. Requester ID authenticates the originating function/context. A completion record is durable shared state for one operation; notification merely prompts inspection. Coherence establishes a single current value across relevant caches/agents, while ordering constrains relative observation of operations.

The minimum partial order is: initialize buffer/descriptor, release/publish ownership, then doorbell; device fetch follows publication; authorization/translation precedes each payload write; all payload writes reach the stated visibility point before completion publication; if used, interrupt follows a visible completion; CPU observes completion with acquire/DMA synchronization before reading metadata and payload. Independent payload writes may reorder if the data format permits it, and notifications may be coalesced or omitted under polling.

### Answer 2

The start offset is `0xe00=3584`, so the first page contributes 512 bytes: IOVA `[0x40000e00,0x40001000)` maps to physical `[0x81000e00,0x81001000)`. The second contributes 4,096 bytes: `[0x40001000,0x40002000)` maps to `[0x92000000,0x92001000)`. The remaining `5632-512-4096=1024` bytes map from `[0x40002000,0x40002400)` to `[0xb3000000,0xb3000400)`.

At most 512 bytes per request gives 1, 8, and 2 requests, for 11 total. All segment starts and lengths are 64-byte aligned, so they touch 8, 64, and 16 distinct cache lines, for 88 total because physical pages do not overlap. This arithmetic proves decomposition only; permissions, ordering, completion, and hardware packet rules still require evidence.

### Answer 3

A valid completion rules out neither stale cache state nor premature device publication. First verify exclusive ownership and that the completion's slot and epoch match the outstanding buffer. On the CPU, instrument the required sync-for-CPU plus DMA read/acquire barrier; replace the buffer with cache-line-aligned dedicated pages to eliminate destructive sharing. On the device/fabric side, capture payload and completion writes and assert payload-before-completion.

Run four controlled variants: correct versus omitted cache synchronization; forced ordered versus intentionally delayed payload writeback in a model; dedicated versus shared cache lines; and unique versus deliberately reused epochs. Guard-fill every buffer and compare device-side and CPU-side digests after synchronization. If correct sync removes the defect only on noncoherent hardware, cache maintenance is implicated; if CPU still sees completion before captured payload, device ordering is wrong; if errors correlate with wrap/reuse, generation ownership is wrong.

### Answer 4

Coherent DMA avoids per-buffer clean/invalidate operations and is attractive when the platform provides it, but it can generate coherence traffic and still needs release/acquire ordering. Noncoherent streaming DMA can suit large one-owner buffers if cache maintenance is exact and amortized; it is hazardous with partial-line sharing. Interrupts minimize idle CPU consumption but add delivery/scheduling latency; polling consumes a core yet can reduce wakeups and jitter under saturation.

For low sustained traffic, choose coherent buffers with interrupt moderation tuned for a bounded light-load delay; verify completion-before-data, lost-wakeup closure, and idle power. At saturation, choose coherent polling if coherence traffic remains acceptable, or noncoherent polling with large aligned batches when measurements show a material gain and ownership is simple. Measure packet-size/flow mixes, pps and goodput, latency percentiles, CPU cycles, cache/coherence and NUMA traffic, IOTLB misses, memory bandwidth, drops, queue fairness, moderation delay, and power. The choice changes if the platform lacks I/O coherence, page placement is remote, or cache maintenance dominates.

### Answer 5

Bind each descriptor to `(requester,PASID,domain_generation,slot,epoch)` and grant only the input-read and output-write pages required. Authenticate PASID use, validate complete ranges, tag IOMMU and device translation-cache entries by live context, and order input publication before device reads and output writes before completion. Polling observes completion phase with acquire/DMA synchronization; it does not weaken ownership rules.

To revoke one context, stop only its new submissions, fence its queue, wait or abort its in-flight commands, remove authorization, invalidate matching IOMMU and ATS/device translations, await architectural completion, drain late writes/completions, and only then unpin/reassign pages and increment generations. On timeout, quarantine the pages and requester context rather than guessing. Verify with page guards, cross-PASID negative requests, stale translation injection, delayed writes, completion reordering, ring wrap, concurrent unaffected contexts, reset/hot removal, fault-queue pressure, and formal assertions that revoked generations cannot write or complete. Bind results to exact accelerator firmware, IOMMU/ATS revision, OS/driver, topology, configuration, and errata; internal tests do not constitute external isolation certification.
