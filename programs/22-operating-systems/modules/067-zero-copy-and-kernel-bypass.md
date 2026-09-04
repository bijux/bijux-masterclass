---
module_id: OS-067
program: Operating Systems
level: 2
module_number: 67
title: Zero-Copy and Kernel Bypass
status: complete
last_verified: 2026-09-04
---

# Zero-Copy and Kernel Bypass

## One-Page Review

### Governing question

When do copy avoidance and user-controlled fast paths improve I/O, and how should an operating system preserve ownership, lifetime, synchronization, isolation, accounting, fallback, and teardown when data or device queues no longer traverse the ordinary buffered path?

### Essential definitions

- **Copy avoidance** removes one or more explicit data copies from a specified path; it does not imply that no copy occurs anywhere.
- **Zero-copy** is a scoped engineering claim that payload bytes avoid particular CPU copies, often by sharing, remapping, pinning, or transferring buffer ownership.
- **Kernel bypass** lets userspace submit or receive work through mapped queues or device access with fewer kernel transitions; setup, policy, interrupts, faults, and teardown can still involve the kernel.
- A **page pin** prevents backing pages from being reclaimed or moved while an external agent can access them.
- A **buffer capability** combines an extent, permissions, owner, device mapping, generation, and lifetime.
- **Completion** is evidence that the previous owner no longer needs the buffer under the interface contract; notification alone may not mean successful transmission.
- A **shared ring** transfers descriptors or ownership between producers and consumers without copying each payload.
- **UMEM** is AF_XDP registered userspace memory divided into frames exchanged through fill, receive, transmit, and completion rings.
- **dma-buf** is a Linux framework for sharing DMA-capable buffers among devices, drivers, and processes with attachments and synchronization.
- A **fallback path** preserves functional semantics when zero-copy or bypass prerequisites are unavailable, even if it uses copies or more transitions.

### Central model, mechanism, or theorem

Model each transferable buffer as

$$
B=(M,[a,a+n),p,o,g,\ell),
$$

where $M$ is backing memory, $[a,a+n)$ the authorized extent, $p$ permissions, $o$ the current owner, $g$ a reuse generation, and $\ell$ the pin, mapping, and object lifetime. Copy avoidance is correct only when every consumer can use a compatible representation and ownership transfers before mutation or reuse.

The performance decision compares total cost, not copy count:

$$
C_{copy}=C_{fixed}+nC_{byte},\qquad
C_{share}=C_{setup}+C_{pin}+C_{map}+C_{sync}+C_{complete}+C_{teardown}.
$$

For small or fragmented transfers, sharing overhead can exceed copying. For large reusable buffers, avoided byte work can dominate. The crossover is empirical and platform-specific.

### Critical invariants

- Every “zero-copy” claim names the source, destination, avoided copy, remaining transformations, and measurement boundary.
- A buffer has one mutable owner at a time unless an explicit coherent read-sharing protocol permits more.
- Pages, mappings, files, devices, queues, and metadata remain live until all CPU and DMA users complete.
- Descriptors reference only authorized, registered, aligned, generation-correct extents.
- Completion transfers reuse authority but is not silently promoted into delivery, durability, or remote-consumption proof.
- Shared-ring producer and consumer roles, memory ordering, capacity, and wakeup rules are obeyed exactly.
- Bypass does not bypass authorization, isolation, resource accounting, rate control, or revocation.
- Failure and removal stop device access and drain queues before unpinning or returning memory.
- A copy fallback preserves user-visible correctness and reports whether requested forced zero-copy could not be provided.

### Common failures

Common mistakes are calling `mmap` automatically zero-copy, counting API calls instead of payload movement, reusing a send buffer before zerocopy notification, interpreting AF_XDP completion as successful wire transmission, placing one UMEM frame on two ownership rings, pinning unbounded memory, sharing buffers without cache or fence synchronization, exposing whole pages for small ranges, trusting device descriptors after bypass, assuming IOMMU presence proves isolation, ignoring NUMA and cache-line traffic, forcing zero-copy for tiny messages, and tearing down mappings while NIC, device, VMA, or peer references remain.

### Compact example

A toy cost model charges copying per byte and sharing a fixed setup plus a per-page cost. It chooses copying for 4 KiB and sharing for 64 KiB. This demonstrates only why a crossover can exist; the constants are illustrative and do not predict a kernel, device, workload, security cost, or real performance threshold.

### Connections

[OS-031](031-address-translation.md), [OS-039](039-shared-pages-and-page-cache.md), [OS-052](052-smp-kernel-synchronization.md), [OS-063](063-direct-memory-access.md), [OS-066](066-asynchronous-i-o.md), and [OS-068](../ROADMAP.md) connect copy avoidance to mappings, page sharing, rings, DMA ownership, asynchronous completion, and storage queues.

## Governing Question

Traditional I/O often copies between userspace and kernel buffers, then maps or copies again for a device. Copy avoidance reuses pages, pipe buffers, registered memory, or DMA mappings. Kernel bypass maps data-plane queues or device resources into userspace so operations avoid ordinary system-call and protocol paths.

The governing question is when those changes improve the desired metric after accounting for fixed setup, page pins, cache coherence, memory ordering, completion processing, security, resource pressure, and fallback. Removing a copy changes ownership and lifetime; removing a transition changes the enforcement point.

## Why This Matters

At high byte rates, memory bandwidth and cache pollution can cost more than protocol computation. Avoiding a full payload copy can free CPU capacity and reduce latency. Mapped rings can batch descriptors and keep work on one core.

The costs move rather than disappear. Long-term pins resist reclaim and migration. Shared buffers need explicit ownership. User-driven queues can monopolize device capacity or submit malicious descriptors. Polling burns CPU and power.

The safest architecture treats fast paths as capabilities governed by a slower control plane. The kernel establishes identity, mappings, limits, queue ownership, fault handling, and teardown; the application earns lower overhead by obeying a stricter protocol.

## Prerequisites and Retrieval

Review [OS-002](002-privilege-levels-and-protection-rings.md), [OS-003](003-system-calls-and-user-kernel-transitions.md), [OS-024](024-atomic-operations.md), [OS-031](031-address-translation.md), [OS-039](039-shared-pages-and-page-cache.md), [OS-045](045-buffer-cache-and-page-cache.md), [OS-052](052-smp-kernel-synchronization.md), [OS-055](055-numa-memory-placement.md), [OS-062](062-memory-mapped-and-port-mapped-i-o.md), [OS-063](063-direct-memory-access.md), [OS-064](064-block-and-character-devices.md), and [OS-066](066-asynchronous-i-o.md).

Retrieve these distinctions:

- virtual sharing, physical sharing, page remapping, DMA mapping, copy-on-write, and device-local memory are different mechanisms;
- allocation, registration, pinning, attachment, mapping, ownership transfer, completion, unmapping, and release are separate events;
- CPU copying, DMA movement, checksum, encryption, compression, packetization, and device-internal copying are different costs;
- a buffer pointer, page, frame identifier, I/O virtual address, descriptor, and generation have different scopes;
- successful enqueue, local stack acceptance, DMA completion, link transmission, peer receipt, and durable storage are different completion levels;
- kernel bypass reduces data-plane mediation but does not eliminate kernel control-plane or hardware trust boundaries;
- cache coherence, memory ordering, and exclusive ownership are separate guarantees;
- throughput, latency, CPU efficiency, memory pressure, fairness, power, and security can move in opposite directions.

## Learning Objectives

After this module, you should be able to:

1. define a zero-copy claim precisely and enumerate remaining payload movements and metadata work;
2. compare ordinary copy, mmap, sendfile, splice, MSG_ZEROCOPY, shared DMA buffers, AF_XDP, io_uring zero-copy receive, and device bypass;
3. model buffer extent, pin, mapping, cache, owner, ring, generation, completion, and teardown lifetime;
4. reason about IOMMU isolation, page-granularity exposure, descriptor validation, quotas, queue sharing, and revocation;
5. choose copying or sharing from measured fixed, per-byte, cache, NUMA, and lifecycle costs;
6. design fallback, reset, process-exit, hot-unplug, and partial-failure paths without leaks or reuse races;
7. verify fast paths with ownership models, copy accounting, fault injection, topology controls, and scoped benchmarks.

## Core Exposition

### Define the claimed copy

Start with a path diagram and label every payload representation. An application buffer can be copied into a socket buffer, fragmented into packets, DMA-read by a NIC, copied by a hypervisor, and reconstructed by a peer.

Claim “avoids the user-to-kernel payload copy on send” rather than “zero-copy networking.” The narrower claim is testable and survives discovery of copies elsewhere.

### Metadata still moves

Copy avoidance usually leaves descriptors, headers, checksums, completion records, reference counts, and queue indices. Control data can dominate small operations.

Measure CPU instructions, cache misses, memory bandwidth, mapping work, and completions alongside payload-copy counters. An API name is not measurement.

### Ordinary copying baseline

Copying gives the receiver private bytes and lets the sender reuse its buffer immediately. It has predictable lifetime, participates naturally in reclaim, and can combine validation with movement.

Modern copy routines are fast and cache-aware. For small payloads, their linear cost can be lower than page pinning, mapping, accounting, and delayed reuse.

### Sharing changes ownership

When two components reference the same bytes, mutation becomes visible across the boundary. The protocol must say who may read, who may write, and when ownership returns.

Reference counting prevents premature object destruction but does not prevent concurrent mutation. Use state, fences, and generation-bearing descriptors in addition to references.

### Page granularity

Virtual-memory and IOMMU operations commonly act at page or larger granularity. Sharing a small subrange can expose or pin neighboring bytes in the same page.

Allocate dedicated, aligned buffers for untrusted sharing. Clear padding and validate lengths so a device or peer cannot read stale adjacent data.

### Page pinning

DMA and some zero-copy paths pin user pages while external access is possible. Pins limit migration, reclaim, compaction, and filesystem operations and require resource accounting.

Use the kernel's pin-user-pages interfaces and correct write intent. Long-term device access has stronger constraints than a short copy; release pins only after mappings and DMA are revoked.

### Short-term versus long-term pins

A short pin supports a bounded operation. A long-term pin supports persistent registration and can interact badly with movable, file-backed, or device-private memory.

Bound registered bytes per process and tenant. Prefer reusable pools sized from workload evidence rather than pinning the entire address space.

### mmap is shared access, not automatically zero-copy

`mmap` can map file pages, anonymous shared memory, device apertures, or driver buffers into an address space. It may avoid explicit read/write copies, but page faults, copy-on-write, cache fills, writeback, migration, and device transfers remain.

Define consistency, invalidation, permissions, VMA lifetime, fork behavior, and removal. Closing the file need not remove existing VMAs.

### Page cache sharing

Mapped file I/O lets an application access page-cache pages directly. Buffered read and write system calls copy between those pages and user buffers, while mmap shifts access to page faults and coherence mechanisms.

The page cache can still copy data to storage through DMA or bounce paths. Dirtying and durable completion remain separate.

### sendfile

`sendfile()` transfers data between file descriptors within the kernel, commonly from a file to a socket, avoiding a userspace bounce buffer. Supported descriptor types, offsets, counts, and partial returns define the actual path.

The filesystem, network stack, checksum, encryption, and device may still copy or transform data. Handle short transfers and fallback without duplicating bytes.

### splice

`splice()` moves data through a pipe-based kernel path between descriptors, allowing page references to be transferred or shared where implementations support it. At least one endpoint follows pipe semantics.

Flags are hints under documented rules, not universal guarantees. Pipe capacity, nonblocking behavior, partial progress, and unsupported endpoints require a stateful loop.

### vmsplice

`vmsplice()` maps or copies user pages into a pipe depending on conditions and flags. Gift-like ownership promises are strict: modifying memory after transferring ownership can corrupt data or violate the contract.

Do not infer physical page donation from the function name. Validate the running kernel and use documented lifetime until pipe consumers finish.

### copy_file_range

`copy_file_range()` lets filesystems or storage perform an in-kernel or offloaded copy without a userspace buffer. The implementation may fall back to copying and can impose same-filesystem, offset, or filesystem-specific rules.

It preserves copy semantics—the source and destination are logically distinct—even if data movement is offloaded. Check partial results, holes, metadata, and durability separately.

### MSG_ZEROCOPY

`MSG_ZEROCOPY` asks supported socket sends to avoid the user-to-kernel payload copy. The socket must opt in, and the kernel can pin pages until it reports safe reuse through the error queue.

The optimization has fixed accounting and notification overhead and is generally intended for larger sends. Applications can mix copied and zero-copy sends according to measured size thresholds.

### MSG_ZEROCOPY ownership

After a successful zerocopy send, the application must not modify the submitted range until the corresponding completion notification says reuse is safe. System-call return means accepted bytes, not returned ownership.

Notifications can cover ranges of send identifiers and can indicate that copying occurred. Track every outstanding interval, partial send, wrap, and fallback result.

### Notification is not delivery

A zerocopy notification tells the sender that the kernel no longer references its pages. It does not prove a TCP peer consumed bytes, a UDP datagram arrived, or an application transaction committed.

Use transport acknowledgements and application protocols for stronger completion. Keep buffer-reuse and delivery state separate.

### AF_XDP overview

AF_XDP connects an XDP program and a userspace socket to a network device queue. A registered UMEM supplies fixed frames exchanged through shared rings.

Driver zero-copy mode lets a compatible NIC DMA into or from UMEM. Copy mode preserves the interface on unsupported paths with different performance.

### UMEM frames

UMEM is virtually contiguous registered memory divided into equal chunks, optionally with headroom and unaligned-chunk rules. Descriptors carry offsets and lengths within it.

Validate that offset plus length lies within one permitted frame representation. Address masking in aligned mode can make distinct input offsets refer to the same chunk.

### AF_XDP ownership rings

The fill ring transfers empty receive frames from userspace to the kernel. The RX ring transfers filled frames to userspace. The TX ring transfers frames for transmission, and the completion ring returns them for reuse.

Never place one frame in fill and TX simultaneously or in multiple queue-owned rings. The NIC can otherwise read and write the same memory concurrently.

### Ring synchronization

AF_XDP rings are designed as single-producer, single-consumer structures. Multiple threads or processes need external serialization rather than assuming the ring becomes multi-producer safely.

Initialize descriptors before release-publishing the producer index, and acquire the index before consuming. Use libbpf helpers that encode the supported protocol.

### Fill starvation

If userspace does not replenish the fill ring, ingress lacks buffers and packets drop or follow the configured behavior. Holding frames for long computation reduces receive capacity.

Size the pool for burst and processing latency, return frames promptly, and expose starvation and drop counters. Copy into application-owned long-term storage when retention would exhaust UMEM.

### Completion semantics

An AF_XDP TX completion returns frame ownership whether the descriptor transmitted or was rejected and reclaimed. It does not universally prove successful wire transmission.

Validate descriptor submission and maintain separate protocol delivery evidence. Recycle only after completion and after no application reference remains.

### Queue binding and steering

An XSK binds to a network device and queue. XDP redirection validates the map entry against queue and device, while hardware flow steering and RSS determine which traffic reaches zero-copy queues.

Control-plane mistakes can send traffic to a normal queue or drop it. Record program, map, queue, RSS, flow rules, driver, and bind mode with benchmark results.

### io_uring zero-copy receive

io_uring zero-copy receive can place network payloads directly into registered userspace memory while the kernel TCP stack still processes headers and protocol state. It differs from full kernel bypass.

It requires specific NIC features, queue configuration, flow steering, ring setup flags, memory registration, and refill discipline. Capability failure needs an ordinary receive fallback.

### Header/data split

The NIC separates headers for kernel protocol processing from payload directed into userspace memory. This preserves the TCP stack while avoiding a payload copy on the supported receive path.

Header processing, metadata, checksums, retransmission, and control traffic remain. “Zero-copy receive” names one payload movement boundary.

### Refill ownership

Userspace receives offsets in completion metadata, consumes bytes, then returns areas through a refill ring. It must not refill while application code still holds the payload.

Ring exhaustion can stall zero-copy receive. Bound retention and integrate completion consumption with application backpressure.

### dma-buf sharing

dma-buf exports a backing allocation as an object that importers attach to their devices. Attachments map the buffer into each device's DMA domain, while reservation objects and fences coordinate asynchronous access.

References keep the object alive; fences establish when readers or writers may proceed. CPU access uses begin/end synchronization rather than casual dereference during device ownership.

### Cross-device sharing

Graphics, video, accelerators, and displays can pass dma-buf file descriptors without copying payloads. Each device can have different segment, address, cache, and placement needs.

The exporter owns backing and migration rules. Importers must honor invalidation and synchronization; an attachment is not permanent physical placement.

### Kernel bypass model

Fuller bypass frameworks map device queues, doorbells, and registered memory to a userspace driver. VFIO and an IOMMU can provide controlled device assignment and interrupt delivery.

The kernel still discovers the device, enforces ownership, establishes mappings, handles faults, accounts resources, and tears down. Firmware and hardware remain privileged actors.

### IOMMU isolation

An IOMMU restricts device-visible addresses to mapped pages and permissions. Isolation depends on group topology, granularity, domain membership, invalidation, and device behavior.

Map the smallest required extents and unmap only after DMA completion. Page-size padding and peer paths can enlarge authority beyond an application record.

### Queue ownership

Assign hardware queues or virtual functions to tenants so descriptors, interrupts, and resets have clear ownership. Shared queues require a trusted multiplexor and per-tenant validation.

Reserve control and recovery capacity. A tenant that fills every descriptor must not prevent cancellation, fault handling, or device reset.

### Doorbells and ordering

Userspace initializes payload and descriptors, applies DMA and shared-memory ordering, then writes a doorbell. Device completion becomes visible through a completion queue with the reverse ownership transition.

Mapped MMIO requires approved access methods and architecture-specific ordering. A normal language atomic alone does not guarantee device I/O completion.

### Interrupts versus polling

Bypass applications often poll queues to reduce wakeup latency and preserve cache locality. Polling consumes a core and power even when idle.

Hybrid schemes interrupt or sleep at low load and poll during bursts. Measure transition cost, latency distributions, CPU efficiency, and thermal effects.

### CPU and NUMA affinity

Place application thread, queue, interrupt, memory, and device near the same NUMA node when it improves the path. Cross-socket cache-line transfers on ring indices can erase copy savings.

One producer and consumer on different sockets may contend on shared head and tail lines. Align metadata and measure interconnect traffic, not only packets per second.

### Cache pollution

Copying reads and writes payload through CPU caches; avoiding it can preserve cache for application state. But polling and shared descriptors also create hot cache lines.

Some applications immediately parse every byte, so the payload must enter CPU caches anyway. Copying can prefetch and linearize it beneficially. Benchmark the actual computation.

### Transformation boundaries

Encryption, compression, checksum, framing, and format conversion can require reading or producing new bytes. Copy avoidance around an unavoidable transformation may yield little benefit.

Fuse transformations where possible, use device offload with verified semantics, and state which copies remain. Never sacrifice authentication or validation merely to preserve a zero-copy label.

### Small-message crossover

Per-operation pin, mapping, reference, notification, and ring costs make copy avoidance unattractive below a workload-specific size. Batching can change the crossover.

Choose thresholds from repeated measurements across sizes, alignments, cache states, and concurrency. Treat documentation heuristics as starting points, not universal constants.

### Fragmentation and scatter-gather

Shared data can span many pages. Devices and protocols impose maximum segments, sizes, alignment, and boundary constraints, leading to coalescing, bounce buffering, or fallback copies.

Record mapped segment count and IOMMU pressure. A logical single buffer need not be a cheap device mapping.

### Memory pressure

Pinned pages cannot satisfy normal reclaim and migration. Large pools can worsen fragmentation, NUMA imbalance, and out-of-memory behavior.

Charge pins and huge pages to the correct tenant, cap them, expose current and high-water usage, and shrink or reject new registrations under pressure.

### Fairness and rate control

Bypass can evade ordinary socket, block, or scheduler queues where policy is applied. Reintroduce admission, bandwidth, packet, descriptor, and CPU controls at the queue or device boundary.

One busy-poll tenant can consume a full core and NIC queue while appearing light in syscall metrics. Account all resources, not only bytes.

### Security of descriptors

Treat every userspace descriptor as untrusted. Validate opcode, address or frame offset, length, flags, headroom, queue, generation, and arithmetic before programming hardware.

Validate device-written completions before array access or free. A compromised device can return stale, duplicate, oversized, or invented identifiers.

### Data confidentiality

Clear frames before reassignment across tenants and avoid exposing padding. Copy fallback can accidentally include uninitialized tail bytes if lengths are wrong.

Shared buffer file descriptors are capabilities. Apply close-on-exec, transfer policy, labeling, and revocation appropriate to the data.

### Failure and fallback

Zero-copy setup can fail because the driver, NIC features, alignment, addressability, memory locks, IOMMU space, or endpoint does not support it. Define whether to fail or use a copied path.

Forced modes should fail visibly so performance-sensitive applications know the guarantee was not met. Automatic fallback must preserve byte, order, error, and completion semantics.

### Cancellation

Canceling an operation does not instantly revoke device access. Arbitrate normal completion and cancellation, stop the queue or command where required, and retain the buffer until ownership is returned.

Copy paths can discard private kernel storage more easily; shared paths make this delayed lifetime explicit.

### Process exit

Exit closes descriptors but the kernel must quiesce mapped queues, DMA, pins, event delivery, and device ownership. Abrupt death cannot leave a NIC writing into pages reassigned to another process.

Supervisors need recovery timeouts and device reset policy. Shared UMEM or dma-buf references in other processes can legitimately keep memory alive.

### Device reset

Reset stops new submissions, contains DMA, drains or invalidates completions, increments generations, reconstructs queues, and republishes readiness. Old descriptors cannot be trusted after reset.

If a shared device reset affects other tenants, the isolation boundary is larger than one queue. Expose that blast radius in design and service objectives.

### Hot-unplug

Removal revokes userspace reachability, wakes pollers, stops DMA through device and IOMMU mechanisms, synchronizes interrupts, invalidates mappings, then releases pins and memory.

VMAs and file references can remain after hardware disappears. Their operations return defined errors without touching revoked MMIO.

### Observability

Record path and fallback mode, avoided-copy boundary, bytes and sizes, pin and map time, pinned pages, segments, queue and frame, generation, owner transitions, batching, syscalls, wakeups, completion latency, drops, faults, reset, and cleanup.

Avoid payload capture and raw I/O addresses in routine telemetry. Correlate sanitized identifiers across application, ring, kernel, driver, and device layers.

### Benchmark design

Compare against an optimized copy baseline with equal semantics. Control payload size, alignment, reuse, cache state, NUMA placement, queue depth, batch, protocol, encryption, device mode, interrupt or poll behavior, and offered load.

Measure throughput, tails, CPU cycles, memory bandwidth, cache misses, pins, drops, power, setup, steady state, and teardown. Include short transfers and fallback frequency.

### Verification

Model every frame owner and generation. Inject ring full and empty, duplicate descriptor, invalid length, completion loss, copied fallback, memory pressure, mapping failure, stalled consumer, cancel, reset, process death, and hot-unplug.

Use IOMMU faults, sanitizers, page-pin accounting, hardware counters, network or block traces, and canary data around authorized extents. Preserve versions, topology, configuration, seeds, traces, negative results, and exact claim boundaries.

## Definitions and Notation

Let payload state be $B=(M,E,P,O,G,L)$ for memory $M$, authorized extent $E$, permissions $P$, owner $O$, generation $G$, and lifetime state $L$. A descriptor $D=(e,n,g,q)$ is admissible only if its extent $[e,e+n)$ is contained in $E$, generation $g=G$, and queue $q$ is authorized for the current owner transition.

For copy path $c$ and shared path $z$, define measured cost at size $n$ as

$$
C_c(n)=F_c+n\beta_c,\qquad
C_z(n)=F_z+\left\lceil\frac{n}{P_s}\right\rceil\pi + S_z,
$$

where $F$ are fixed costs, $\beta_c$ is marginal copy cost, $P_s$ page size, $\pi$ per-page pin or mapping cost, and $S_z$ synchronization and completion cost. These are workload-fit parameters, not architectural constants.

An ownership trace can move `free -> application -> kernel/device -> completed -> application -> free`. Every transition publishes initialized metadata before the receiving owner proceeds. Reference lifetime contains ownership lifetime, and pin lifetime contains every possible DMA interval.

## Mechanisms, Invariants, or Proof Structure

A reviewable zero-copy or bypass design discharges these obligations:

1. **Claim:** name exactly which payload copies and kernel transitions are avoided and which remain.
2. **Extent:** validate every offset, length, alignment, page, frame, descriptor and generation.
3. **Ownership:** assign one mutable owner and a completion-backed transition for each buffer.
4. **Lifetime:** retain objects, pages, mappings, files, queues and metadata through all CPU and DMA access.
5. **Ordering:** publish payload and descriptors before handoff and acquire completion before reuse.
6. **Isolation:** constrain devices and peers with permissions, IOMMU domains, groups and dedicated padding.
7. **Capacity:** bound pins, maps, frames, rings, descriptors, completions, polling CPU and backlog.
8. **Semantics:** preserve short I/O, errors, order, delivery level, durability and cancellation across fast and fallback paths.
9. **Fairness:** retain tenant accounting, rate limits and reserved recovery capacity outside bypassed queues.
10. **Revocation:** contain device access and drain references before unmap, unpin, reuse or release.
11. **Observability:** record path, copies, owners, resources, fallbacks, faults and lifecycle without leaking data.
12. **Evidence:** compare complete costs under controlled sizes, topologies, loads, failures and security checks.

The proofs remain separate. Shared pages prove copy avoidance at one boundary, not exclusive ownership. Completion proves reuse authority at one interface, not peer delivery. An IOMMU mapping narrows reachability, not descriptor intent. Higher throughput does not prove lower CPU, latency, memory pressure, or security risk.

## Alternatives and Trade-Offs

- **Copy versus share:** copying gives private ownership and low fixed cost; sharing saves byte movement and extends lifetime.
- **Read/write versus mmap:** system calls provide explicit transfer points; mappings avoid copies and shift work into faults and coherence.
- **sendfile versus userspace relay:** sendfile avoids a bounce buffer; a relay can transform and inspect bytes flexibly.
- **splice versus explicit buffers:** splice composes kernel pipe buffers; explicit buffers provide portable ownership and application access.
- **MSG_ZEROCOPY versus copied send:** zerocopy benefits large sends; copying permits immediate buffer reuse and simpler error handling.
- **AF_XDP copy versus zero-copy mode:** copy mode is broadly available; driver mode avoids payload copies with stricter hardware and queue requirements.
- **Kernel TCP versus full bypass:** kernel TCP provides mature protocol control; bypass offers specialized performance and greater implementation burden.
- **Short versus long-term registration:** short mappings reduce retained authority; pools amortize cost and consume pinned memory.
- **Interrupts versus polling:** interrupts save idle CPU; polling lowers wake latency and raises power use.
- **Shared versus per-queue UMEM:** sharing saves memory; separate pools simplify producer, consumer and tenant ownership.
- **One large pool versus sized pools:** a large pool absorbs bursts; smaller pools bound memory pressure and blast radius.
- **Device offload versus CPU transform:** offload can preserve copy avoidance; CPU work offers portability and easier observability.
- **Automatic versus forced fallback:** automatic fallback preserves function; forced mode makes performance-contract failure visible.
- **Direct device assignment versus mediated queues:** assignment minimizes mediation; multiplexing centralizes validation, fairness and recovery.

## Failure Modes and Misconceptions

- **“Zero-copy means bytes never move.”** DMA and device-internal movement remain.
- **“mmap is always faster than read.”** faults, cache behavior and access pattern decide cost.
- **“sendfile guarantees no copy.”** endpoint and implementation paths can transform or fall back.
- **“System-call return returns zerocopy ownership.”** completion notification controls buffer reuse.
- **“TX completion proves delivery.”** it can only return local ownership or reclaim an invalid descriptor.
- **“One frame can be on fill and TX rings.”** concurrent NIC read and write corrupt data.
- **“Reference counting prevents data races.”** it protects lifetime, not mutable ownership.
- **“Long-term pins are ordinary allocations.”** they obstruct reclaim, migration and filesystem operations.
- **“IOMMU present means the device is safe.”** group, granularity, permissions and invalidation matter.
- **“Kernel bypass removes the kernel.”** setup, mappings, policy, faults and teardown remain.
- **“Polling has zero latency cost.”** it consumes CPU, power and shared-cache capacity.
- **“Fewer copies guarantees higher throughput.”** setup and synchronization dominate some sizes.
- **“A shared buffer is coherent everywhere.”** devices and CPUs need mapping, cache and fence protocols.
- **“Fallback is merely slower.”** it must preserve completion and buffer-reuse semantics too.
- **“Closing a descriptor revokes DMA.”** mappings and in-flight device work can outlive table entries.
- **“Reset makes stale completions harmless.”** generation checks are required before reuse.
- **“Huge pages solve every mapping cost.”** they increase pin granularity and internal fragmentation.
- **“A microbenchmark proves production value.”** topology, transforms, load, failures and security controls differ.

## Worked Examples

### Example 1

A static file server uses sendfile for large unmodified files and a buffered userspace path for compressed responses. Both loops handle partial transfers and nonblocking sockets.

### Example 2

A TCP sender enables `SO_ZEROCOPY` only above a measured size. It records each successful send range and waits for error-queue notifications before modifying or freeing those pages.

### Example 3

An AF_XDP application owns frame 12 after RX, parses it, places it on TX, and waits for completion before returning it to fill. It never publishes the frame to two rings simultaneously.

### Example 4

An AF_XDP bind forced with zero-copy mode fails on an unsupported virtual NIC. The service reports the unavailable performance contract instead of silently benchmarking copy mode.

### Example 5

An io_uring zero-copy receiver uses NIC header/data split. TCP headers stay in the kernel stack while payloads land in a registered area; consumed offsets return through a bounded refill ring.

### Example 6

A video decoder exports dma-buf frames to a display. Reservation fences prevent display reads before decode writes finish, and CPU diagnostics bracket access with begin/end synchronization.

### Example 7

A VFIO process maps only dedicated huge pages into its device domain. Process death stops bus mastering and completes IOMMU invalidation before those pages return to another tenant.

### Example 8

A 200-byte message copies faster than it can be pinned, mapped, and completed. A 1 MiB reusable registered buffer amortizes fixed setup and reduces memory bandwidth under sustained transfer.

### Example 9

Hot-unplug wakes a bypass poller with an error, blocks doorbells, contains DMA, drains interrupts and invalidates mappings. Existing VMAs retain metadata but cannot touch removed device registers.

### Example 10

The following toy compares illustrative fixed and marginal costs at two sizes. It does not measure a CPU, kernel, cache, page pin, IOMMU, device, network, or application and supplies no real crossover threshold.

<!-- bijux-verify: {"id":"copy-sharing-cost-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"size=4096 copy=8192 share=12200 choice=copy\nsize=65536 copy=131072 share=15200 choice=share\n","stderr":""}} -->
```python
PAGE = 4096

for size in (4096, 65536):
    pages = (size + PAGE - 1) // PAGE
    copy_cost = 2 * size
    share_cost = 12000 + 200 * pages
    choice = "copy" if copy_cost <= share_cost else "share"
    print(f"size={size} copy={copy_cost} share={share_cost} choice={choice}")
```

## Cross-Program Connections

[Network Engineering](../../24-network-engineering/ROADMAP.md) connects packet queues, RSS, flow steering, TCP completion, offloads, drops and congestion. [Security Engineering](../../25-security-engineering/ROADMAP.md) connects device assignment, IOMMU isolation, descriptor validation, memory disclosure, quotas and revocation.

[Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) connects ownership transfer, single-producer rings, fences, atomics and polling. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) connects tenant isolation, resource accounting, workload placement, observability and safe fallback. Within this program, [OS-066](066-asynchronous-i-o.md) develops completion rings and [OS-068](../ROADMAP.md) develops storage queues and NVMe.

## References

- Linux kernel documentation, [MSG_ZEROCOPY](https://docs.kernel.org/networking/msg_zerocopy.html), current page checked 2026-09-04. Socket copy avoidance, opt-in, page pins, size trade-offs, completion notifications and buffer reuse.
- Linux kernel documentation, [AF_XDP](https://docs.kernel.org/networking/af_xdp.html), current page checked 2026-09-04. UMEM, fill, completion, RX and TX rings, ownership, copy and zero-copy modes, queue binding and wakeups.
- Linux kernel documentation, [io_uring Zero-Copy Receive](https://docs.kernel.org/networking/iou-zcrx.html), current page checked 2026-09-04. Header/data split, NIC prerequisites, registered memory, refill rings, flow steering and receive completions.
- Linux kernel documentation, [Pinning User Pages](https://docs.kernel.org/core-api/pin_user_pages.html), current page checked 2026-09-04. Page-pin APIs, DMA pins, write intent, long-term registration, tracking and release cases.
- Linux kernel documentation, [Buffer Sharing and Synchronization](https://docs.kernel.org/driver-api/dma-buf.html), current page checked 2026-09-04. Exporters, attachments, mappings, fences, reservations, migration and CPU access.
- Linux kernel documentation, [VFIO](https://docs.kernel.org/driver-api/vfio.html), current page checked 2026-09-04. Userspace device access, IOMMU groups, mappings, regions, interrupts and isolation.
- Linux man-pages project, [sendfile(2)](https://man7.org/linux/man-pages/man2/sendfile.2.html), current page checked 2026-09-04. In-kernel descriptor transfer, offsets, limits, partial results and endpoint restrictions.
- Linux man-pages project, [splice(2)](https://man7.org/linux/man-pages/man2/splice.2.html), current page checked 2026-09-04. Pipe-mediated transfer, flags, blocking, partial results, errors and copy-avoidance scope.
- Linux man-pages project, [vmsplice(2)](https://man7.org/linux/man-pages/man2/vmsplice.2.html), current page checked 2026-09-04. User-page to pipe transfer, vector limits, ownership promises, blocking and errors.
- Linux man-pages project, [copy_file_range(2)](https://man7.org/linux/man-pages/man2/copy_file_range.2.html), current page checked 2026-09-04. In-kernel and offloaded file copying, filesystem constraints, partial results and fallback semantics.

## Exercises

### Exercise 1

Compare copy, sendfile, splice, mmap, and MSG_ZEROCOPY for a TLS-capable file server with small dynamic responses and large static files.

### Exercise 2

Design an AF_XDP frame-ownership protocol for four queues, two worker threads per queue, bounded packet retention, TX forwarding, reset, and shutdown.

### Exercise 3

Construct the security and lifecycle proof for a VFIO-assigned device using long-term pinned memory and direct userspace queues.

### Exercise 4

Design a fallback strategy for io_uring zero-copy receive when NIC features, flow steering, registration, or memory capacity are unavailable.

### Exercise 5

Build a verification and benchmark plan that can support a precise copy-avoidance claim across physical, virtual, and confidential-computing hosts.

## Answers to the Exercises

### Answer 1

Use an optimized ordinary-copy baseline for small dynamic responses because parsing, TLS framing, encryption, and fixed mapping costs dominate. A userspace TLS implementation normally transforms plaintext into distinct ciphertext, so a broad “zero-copy” claim is false unless kernel or device TLS offload changes the path. For large unmodified plaintext static files, test sendfile from page cache to socket. If the pipeline needs pipe-compatible transformations, test splice but retain partial, capacity, and unsupported-endpoint handling. mmap can reduce file-to-user copying for application inspection but still faults pages and does not solve socket transfer.

For large application buffers on supported sockets, test MSG_ZEROCOPY above measured thresholds. Track every partial send and wait for error-queue notification before reuse; separate local page-release from peer delivery. Ensure copied fallback produces the same bytes, order, errors and application completion. Compare size distributions, warm and cold cache, TLS modes, send congestion, NUMA, CPU, memory bandwidth, page pins, tail latency and teardown. Select per-response paths instead of forcing one mechanism, and report the exact avoided boundary for each.

### Answer 2

Give each device queue its own XSK, RX/TX rings, and a single logical producer and consumer per ring. A dispatcher can hand received frames to either worker through an application queue, but the frame state remains generation-tagged: `fill -> kernel-rx -> rx -> worker -> tx -> kernel-tx -> completion -> free`. Only the ring owner publishes descriptors. Workers return decisions to that owner rather than concurrently manipulating SPSC rings. Never place a frame in fill and TX or in two queue pairs simultaneously.

Cap worker-held frames and copy packets into separate storage if retention exceeds the budget. Replenish fill before starvation and apply upstream drop or backpressure policy. Validate offsets, lengths, headroom, queue and generation from RX and completion data. Reset stops producers, unbinds steering, contains DMA, drains rings, invalidates old generations, rebuilds state and republishes. Shutdown wakes polling threads, stops traffic, resolves TX ownership, drains completion, unregisters UMEM and closes sockets before freeing pages. Inject duplicate and stale descriptors, ring full and empty, worker death, copy fallback, invalid completion, reset and unplug.

### Answer 3

Bind only a viable isolation group to VFIO and prove that sibling functions or peer paths cannot bypass the domain. Allocate dedicated, cleared pages, charge and cap long-term pins, and map only required I/O virtual extents with direction-appropriate permissions and guard regions. Validate all descriptor lengths and arithmetic in the userspace driver and constrain the device through firmware and queue configuration. Do not place secrets in granularity padding. Capture credentials and restrict device, VFIO container, huge pages, interrupts and reset authority.

The device may access a buffer only between mapped ownership transfer and validated completion or contained reset. Doorbells follow descriptor and DMA barriers; completions are generation-checked. On fault, timeout, process death or unplug, stop new doorbells, mask and synchronize interrupts, disable or reset bus mastering, revoke mappings, wait for IOMMU invalidation, then unpin and clear pages. If containment cannot be proved, quarantine memory. Record mappings, group topology, pins, faults, resets and cleanup. IOMMU presence alone is insufficient evidence; test malicious out-of-range DMA and stale transactions on the actual topology.

### Answer 4

At startup query kernel, io_uring, NIC, driver, queue, header/data-split, RSS and flow-steering capabilities. Attempt dedicated queue configuration, registered area and refill-ring setup under tenant memory limits. If the user explicitly requires zero-copy, fail with a precise unmet prerequisite. In automatic mode, fall back first to ordinary io_uring receive with provided or registered buffers, then to nonblocking socket reads if necessary. Preserve stream ordering, short-read, error, EOF, cancellation and buffer-reuse semantics across modes.

Expose the active path and fallback reason. Keep flow steering transactional: do not direct traffic to a zero-copy queue until the ring is ready, and restore normal steering before teardown. Bound registered memory and retained payloads; replenish or copy out before starvation. On runtime device reset or feature loss, stop the fast path, resolve owned offsets, remove steering, unregister safely and resume through the copy path only after TCP state remains valid. Test every setup failure, partial steering update, ring exhaustion, mixed flows, memory pressure, reset and rollback while comparing byte sequences end to end.

### Answer 5

Draw the complete source-to-destination path for each host type and identify user copies, kernel copies, DMA, bounce buffers, encryption boundaries, hypervisor movement and device-internal unknowns. Instrument bytes at user-copy routines where practical, CPU memory bandwidth, cache misses, page pins, DMA mappings, ring ownership, syscalls, interrupts, IOMMU faults and device counters. Use canary regions around dedicated buffers to test extent isolation without exposing production data.

Compare identical semantics and offered loads across optimized copy and fast paths while sweeping size, alignment, fragmentation, batch, queue depth, cache state, NUMA, transforms, contention and duration. On virtual and confidential hosts, record host access rules and bounce-buffer use. Inject unsupported mode, pin exhaustion, ring starvation, duplicate descriptors, delayed completion, process death, reset and hot-unplug, and verify drain-before-unpin. Report throughput, latency distributions, CPU, memory bandwidth, power, pins, drops, setup and teardown with raw evidence. Limit the conclusion to the observed boundary: proving no user-to-kernel payload copy does not prove no copy in a hypervisor, encrypted-memory bridge, device, or peer.
