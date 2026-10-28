---
module_id: OS-068
program: Operating Systems
level: 2
module_number: 68
title: Storage Queues and NVMe
status: complete
last_verified: 2026-09-04
---

# Storage Queues and NVMe

## One-Page Review

### Governing question

How should an operating system map block requests onto NVMe administration and I/O queue pairs, preserve DMA and doorbell ordering, identify out-of-order completions safely, expose namespaces and paths correctly, and recover from timeout, reset, path loss, and controller removal without losing or duplicating I/O?

### Essential definitions

- An **NVM subsystem** contains one or more NVMe controllers and namespaces under a common storage architecture.
- A **controller** implements host-facing administration and I/O command processing over a transport such as PCIe, RDMA, or TCP.
- A **namespace** is a formatted logical block address space identified within an NVM subsystem and exposed through one or more controllers.
- A **submission queue (SQ)** is a host-produced sequence of fixed-format commands consumed by a controller.
- A **completion queue (CQ)** is a controller-produced sequence of completion entries consumed by the host.
- A **queue pair** associates an I/O SQ with a CQ for command submission and result delivery; several SQs can share one CQ where supported.
- A **command identifier (CID)** correlates a completion with an outstanding command within the relevant SQ scope.
- A **phase tag** distinguishes new completion entries from stale entries after a circular CQ wraps.
- A **doorbell** is an MMIO register through which the host reports an updated queue head or tail to the controller.
- **Asymmetric Namespace Access (ANA)** reports path access states so multipath policy can prefer optimized paths and react to change.

### Central model, mechanism, or theorem

Represent an outstanding command as

$$
K=(q,c,g,r,d,s),
$$

where $q$ is the queue, $c$ the CID or block tag, $g$ a software lifecycle generation, $r$ the request, $d$ its DMA mapping, and $s$ its state. Before ringing the SQ doorbell, the host makes command and data descriptors visible. The controller may complete commands out of submission order. A completion is accepted only if queue, CID, phase, generation, status, and request state all validate; then DMA ownership and the block request terminate exactly once.

Queue depth is capacity, not a performance target. Useful depth exposes controller parallelism; excess depth increases waiting, tail latency, memory, and reset scope. The operating system maps software contexts to hardware queues according to controller capability, CPU/NUMA topology, interrupt vectors, polling policy, and workload objectives.

### Critical invariants

- The admin queue carries only administration or permitted fabrics commands; I/O commands use correctly created and associated I/O queues.
- A live SQ slot, CID, block tag, DMA mapping, and request have one coherent owner and generation.
- Command fields, PRPs or SGLs, and payload ownership become device-visible before the SQ tail doorbell.
- A CQ entry is read only after its expected phase becomes visible, and its remaining fields are acquired before processing.
- Every accepted command reaches exactly one terminal block-layer result despite interrupt, polling, timeout, abort, reset, and removal races.
- Queue head and tail arithmetic never overwrites unconsumed commands or completions and respects the protocol's reserved capacity.
- Namespace identity, capacity, format, path, and controller identity remain separate; a path change does not create a new logical namespace accidentally.
- Flush, FUA, write-cache, atomicity, metadata, protection, discard, and zone capabilities are reported no stronger than the complete path guarantees.
- Reset stops submission and DMA, drains or invalidates generations, reconstructs queues, and republishes only after controller and namespaces are ready.

### Common failures

Common mistakes are treating NVMe as a raw faster disk, using queue depth equal to the maximum everywhere, ringing a doorbell before descriptors are visible, confusing SQ head with host-consumed progress, ignoring CQ phase on wrap, assuming completion order equals submission order, reusing a CID before terminal completion, trusting a completion without queue and generation validation, mapping all CPUs to one queue, overdistributing queues across NUMA nodes, blocking recovery behind exhausted tags, identifying a namespace only by a transient device name, retrying non-idempotent uncertainty blindly, and declaring reset complete before stale DMA and interrupts are contained.

### Compact example

A CQ consumer starts at slot 3 with expected phase one. It consumes slot 3, wraps to slot zero, toggles expected phase to zero, consumes slot zero, then stops because slot one's phase remains one. Phase distinguishes two new entries from stale memory without clearing the ring. This calculation models one consumer rule only, not DMA visibility, MMIO, interrupts, command validation, or an NVMe controller.

### Connections

[OS-020](020-measuring-scheduler-latency-and-throughput.md), [OS-052](052-smp-kernel-synchronization.md), [OS-055](055-numa-memory-placement.md), [OS-058](058-timer-and-interrupt-scalability.md), [OS-063](063-direct-memory-access.md), [OS-065](065-i-o-schedulers.md), and [OS-067](067-zero-copy-and-kernel-bypass.md) connect NVMe to performance, concurrent queues, topology, interrupts, DMA, scheduling, and mapped fast paths.

## Governing Question

NVMe was designed for nonvolatile memory devices capable of many concurrent operations. It replaces a single host-adapter bottleneck with memory-based or message-based submission and completion queues, compact commands, tagged results, and multiple transports.

The governing question is how the operating system turns this parallel interface into safe block semantics. Queue creation, tag ownership, DMA, doorbells, interrupts, namespaces, multipath, timeouts, and resets form one lifecycle. Optimizing only steady-state IOPS leaves the most dangerous transitions unproved.

## Why This Matters

On fast devices, software queue contention, cache-line movement, interrupt routing, IOMMU overhead, and completion processing can rival media latency. Per-CPU and per-hardware-queue paths make topology a correctness and performance concern.

Large concurrency magnifies error scope. A controller reset can affect thousands of outstanding commands. One stale completion can terminate a new request after tag reuse. A full completion queue can prevent progress even when storage is healthy.

NVMe also spans local PCIe and remote fabrics. The same logical namespace can have optimized, nonoptimized, inaccessible, or changing paths. A durable operating-system design separates storage identity from transport attachment and makes uncertainty explicit during path failure.

## Prerequisites and Retrieval

Review [OS-004](004-interrupts-and-exceptions.md), [OS-020](020-measuring-scheduler-latency-and-throughput.md), [OS-024](024-atomic-operations.md), [OS-031](031-address-translation.md), [OS-052](052-smp-kernel-synchronization.md), [OS-055](055-numa-memory-placement.md), [OS-058](058-timer-and-interrupt-scalability.md), [OS-061](061-device-discovery-and-driver-models.md), [OS-062](062-memory-mapped-and-port-mapped-i-o.md), [OS-063](063-direct-memory-access.md), [OS-064](064-block-and-character-devices.md), and [OS-065](065-i-o-schedulers.md).

Retrieve these distinctions:

- NVM subsystem, controller, namespace, path, PCI function, block device, and userspace name are different identities;
- block software queues, blk-mq hardware contexts, NVMe SQs, CQs, controller queues, and flash-internal queues are separate layers;
- request tag, command identifier, SQ slot, CQ slot, phase, and software generation have different scopes;
- command publication, doorbell arrival, controller fetch, media completion, CQ publication, interrupt, and block completion are different events;
- queue capacity, allocated depth, outstanding depth, useful parallelism, and optimal operating depth are different quantities;
- DMA coherence, device ordering, MMIO ordering, and controller completion are separate guarantees;
- abort request completion, target command completion, controller reset, and proof of contained DMA are different outcomes;
- namespace access state, transport reachability, controller health, and data integrity can fail independently.

## Learning Objectives

After this module, you should be able to:

1. distinguish NVMe subsystems, controllers, namespaces, paths, transports, queues, commands, and block-layer objects;
2. trace controller initialization, admin queue creation, identify, feature negotiation, I/O queue creation, namespace publication, and teardown;
3. reason about SQ and CQ circular arithmetic, doorbells, CIDs, phase tags, interrupts, polling, DMA, and memory ordering;
4. map blk-mq software contexts, hardware contexts, tags, NUMA nodes, and interrupt vectors onto controller queues;
5. preserve capacity, format, cache, flush, FUA, metadata, protection, discard, atomic, and zoning semantics;
6. handle command error, timeout, abort, reset, ANA change, reconnect, firmware quirks, suspend, and hot-unplug;
7. validate performance and recovery with fault injection, trace correlation, workload controls, and scoped evidence.

## Core Exposition

### The NVM subsystem

An NVM subsystem is the storage entity behind one or more controllers. It can expose namespaces through several paths and transports.

Do not equate one PCI function or network connection with the stored data's durable identity. Multipath and controller replacement require identity above attachment.

### Controllers

A controller implements NVMe registers, admin commands, I/O command sets, queues, features, status, and events. A local PCIe controller uses memory queues and MMIO doorbells; a fabrics controller exchanges capsules through a transport.

Driver initialization validates the transport, controller capabilities, page-size compatibility, timeouts, queue limits, and state before enabling I/O.

### Namespaces

A namespace supplies a logical block address space, format, capacity, metadata and command-set properties. Namespace identifiers can allow stable association across controllers.

Validate identifiers and capacity changes. A namespace can appear, disappear, reformat, or become inaccessible independently of the controller object.

### Admin queue

The host creates the admin submission and completion queues as part of controller enablement. Admin commands identify capabilities, create and delete I/O queues, manage features, obtain logs, update firmware, abort commands, and handle namespaces.

Reserve admin capacity for recovery and asynchronous events. Saturating it with optional management work can prevent abort or health handling.

### I/O queue pairs

I/O SQs carry read, write, flush, dataset management, write-zeroes, compare, zone and other supported command-set operations. Each SQ is associated with one CQ; one CQ can serve multiple SQs under permitted configurations.

Queue layout affects locks, cache lines, interrupt vectors and completion routing. Choose it from the operating system and controller topology rather than maximum counts alone.

### Memory-based queue model

For PCIe transport, SQs and CQs reside in DMA-coherent host memory satisfying alignment and contiguity rules. The controller reads SQEs and writes CQEs.

The CPU uses its virtual mapping while the controller uses DMA addresses. Queue lifetime contains every controller access, including reset and shutdown uncertainty.

### Message-based queue model

NVMe over Fabrics sends command and completion capsules over RDMA, TCP, Fibre Channel or another specified transport. Queue pairs remain logical channels, but doorbell and DMA details become transport operations.

The transport adds connection, authentication where configured, keep-alive, retransmission, congestion, and remote failure semantics. Do not project PCIe ordering assumptions onto fabrics unchanged.

### Submission queue arithmetic

The host owns SQ tail; the controller reports or advances consumption through completion information and protocol state. The host must not overwrite commands the controller has not consumed.

Circular full and empty tests account for wrap and the protocol's usable-entry rule. Store indices at sufficient width and keep software outstanding counts for validation.

### Building a command

Initialize opcode, namespace, CID, data pointer, metadata, starting logical block, length, control flags and operation-specific words from validated request state. Clear reserved fields.

Convert multi-byte fields according to the specification and check every narrowing conversion. A block request larger than the command or data-pointer limit must split above this boundary.

### Command identifiers

CID correlates a CQE with an outstanding command in the SQ context. Linux can align it with a blk-mq tag while retaining driver-private generation and queue identity.

A numerical CID is reusable only after the prior command reaches a terminal state. Reset invalidates old generations so a late completion cannot match new work.

### PRPs

Physical Region Page entries describe data pages for a command under alignment and page rules. A transfer can use a direct pointer pair or a list for additional pages.

Construct PRPs only from DMA mappings returned for the controller. Validate first-page offset, page count, list capacity, chain pages and transfer extent.

### Scatter-gather lists

Supported SGL descriptors can represent data segments with different formats and chaining. Controller capability and command-set rules determine whether they are allowed.

Do not confuse a Linux scatterlist with an NVMe SGL encoding. The driver translates mapped DMA segments into protocol descriptors and owns list memory through completion.

### DMA ownership

Map block request data in the correct direction, check errors, and retain mapping parameters. The device owns payload and descriptor memory after publication until validated completion or contained recovery.

Unmap only after access has ended. Timeout is not proof of stopped DMA; reset and IOMMU teardown participate in containment.

### Publishing an SQE

Write all command and data descriptors, apply the DMA and memory ordering required by the platform, advance the SQ tail in software, then ring the tail doorbell with the ordered MMIO accessor.

The doorbell is notification, not a substitute for descriptor visibility. A posted MMIO write may require a readback only at protocol-defined transitions.

### Doorbell batching

The host can prepare several SQEs and ring once, amortizing MMIO. Batching improves throughput and can delay the first command.

Bound batch size and dwell time, and never publish beyond available queue space. Measure doorbell rate, latency and queue occupancy together.

### Controller SQ consumption

The controller fetches commands after observing the doorbell and can execute them in parallel or reorder within command and namespace constraints.

Host software learns command completion from CQEs, not merely from an SQ head estimate. Consumed does not mean completed or durable.

### Completion queue entries

A CQE carries result data, SQ head, SQ identifier, CID, status, and a phase tag. Its status and command-specific result define the operation outcome.

Validate SQ and CID before indexing driver state. Map status to accurate block-layer results and retain raw evidence for diagnosis without leaking data.

### Phase tags

On CQ creation the host expects an initial phase. The controller writes entries with that phase and toggles after wrapping. The host consumes while entry phase equals expected and toggles its expectation on wrap.

This avoids clearing CQ memory. Read the phase with appropriate ordering before trusting the remainder of a controller-written entry.

### CQ head doorbell

After consuming completions, the host advances its CQ head and rings the head doorbell so the controller can reuse those entries.

Batching head updates reduces MMIO but reduces visible free capacity. A stalled consumer can fill the CQ and block controller progress.

### Completion ordering

Commands can complete out of SQ order. Multiple SQs further remove any global completion order.

Correlate through queue and CID, and let upper layers express required ordering with flush, FUA, dependencies or serialization. Never release requests by “oldest outstanding.”

### Interrupts

PCIe NVMe commonly uses MSI-X vectors assigned to completion queues. Interrupt handlers or threaded work drain CQEs and complete block requests.

Vector count, queue mapping, CPU affinity and moderation shape cache locality and tail latency. Shared vectors require bounded fair draining across queues.

### Interrupt coalescing

Controller features can delay or batch interrupts to reduce CPU overhead. Coalescing can improve throughput but increases completion latency and burst size.

Tune from workload evidence and preserve recovery responsiveness. An interrupt storm or lost interrupt still needs polling or timeout diagnosis.

### Polling

Polling a suitable queue avoids interrupt wakeups and can reduce latency at high utilization. It consumes CPU and works best with queue and core affinity.

Separate polled queues where required. At low rates, interrupts or hybrid behavior usually save power; compare full CPU efficiency, not only device latency.

### blk-mq integration

blk-mq translates bios into tagged requests and maps software submission contexts to hardware contexts. The NVMe driver maps hardware contexts onto controller I/O queues.

The shortest path can dispatch directly when scheduling and merging permit. Driver resource responses and stopped queues preserve work until capacity returns.

### Block tags and CIDs

Using the blk-mq tag as CID avoids a second lookup, but tag and command lifetimes must match. Reserved tags provide capacity for internal or recovery work.

Validate tag bounds and state before completion. A tag becomes reusable only after request completion and driver cleanup, not when an interrupt merely arrives.

### Software and hardware queues

Per-CPU software contexts reduce shared submission locks. Hardware contexts represent dispatch domains and map to NVMe SQ/CQ resources.

There need not be one NVMe queue per CPU. Queue counts are capped by controller capability, vectors, memory, topology, polling modes and useful parallelism.

### CPU affinity

Align submission, completion interrupt, queue data and application CPU to reduce cross-core cache movement. Completion on the submitting CPU can improve locality for some workloads.

CPU hotplug and scheduler migration change the mapping. Use kernel affinity mechanisms rather than durable assumptions about one CPU number.

### NUMA placement

Allocate queue memory and steer work near the PCIe root or fabric interface where beneficial. A local submitting CPU can still access remote device memory paths.

Measure memory, IOMMU, interrupt and application placement together. Maximum queue distribution can create cross-socket traffic that outweighs contention savings.

### Queue depth

Depth bounds outstanding commands, command memory, PRP or SGL resources, DMA mappings and reset scope. Some depth exposes NAND channels and controller parallelism.

After throughput saturates, more depth increases queueing latency. Sweep depth under realistic sizes and mixes; preserve reserved recovery capacity.

### Controller arbitration

Controllers can arbitrate among SQ priorities according to supported mechanisms. Host I/O scheduler and cgroup intent does not automatically map to controller arbitration.

Use supported priority fields and features carefully. Strict priority can starve lower classes, and firmware behavior must be measured.

### Namespace formats

Identify reports supported logical-block formats, metadata placement, protection information and current format. The block device publishes the selected logical size and capacity.

Formatting is destructive and changes interpretation of stored data. Serialize administrative format with all paths, mounts, opens and I/O, and refresh namespace state afterward.

### Maximum transfer size

Controller and namespace capabilities, host page size, transport, PRP or SGL capacity, DMA segments and block queue limits bound each command.

Advertise the conservative composite limit so the block layer splits safely. Revalidate after reconnect or controller replacement.

### Volatile write cache

Identify and feature state determine whether completed writes can remain in volatile controller cache. The driver reports cache behavior so upper layers issue flushes and FUA appropriately.

Changing cache policy requires synchronized state and truthful reporting. Power-loss protection is a device property requiring evidence, not an inference from low latency.

### Flush and FUA

Flush commits prior relevant writes according to NVMe namespace and path semantics. FUA on a write requests the required persistence behavior for that command.

Preserve flags through block and multipath layers. Completion order alone does not replace the persistence protocol.

### Atomic write properties

NVMe reports atomic write units and boundary constraints under stated conditions. These are narrower than arbitrary transaction atomicity.

Translate capabilities conservatively and include power failure, namespace format and controller mode. Filesystems and databases still require logging for multi-command invariants.

### Dataset management and write zeroes

Dataset management can convey deallocation hints; write zeroes provides zero-read semantics under its command contract. Limits, alignment and namespace support apply.

Deallocation does not universally promise zeros. Map status precisely and avoid advertising unsupported discard behavior.

### Protection information and metadata

Namespaces can attach metadata and protection information to logical blocks. Host and controller coordinate checks across application tags, reference tags and guards.

DMA and descriptor lifetime includes metadata. A stacked layer that changes logical addressing must transform protection information correctly.

### Zoned namespaces

ZNS namespaces impose sequential write rules, write pointers, zone states and open or active resource limits. Zone append returns the actual written logical address.

Queue scheduling and completion must preserve zone ordering. Validate returned addresses and do not infer them from submission order.

### Persistent reservations

Reservation commands coordinate host access to shared namespaces. They are distributed fencing mechanisms with registration keys, generations and failure semantics.

Multipath and failover must preserve the intended host identity. Reservations do not replace application concurrency control or data integrity.

### Asynchronous events

The controller can report namespace change, firmware activation, health and other events through asynchronous event requests and log pages.

Maintain sufficient outstanding event requests as specified, validate event type, read authoritative logs, rescan safely, and repost. An event is notification, not the complete new state.

### Health and logs

SMART/health, error, telemetry, firmware and persistent-event logs expose controller evidence. Reading can have side effects or version-specific fields.

Rate-limit collection and retain raw identifiers, timestamps and versions. Health counters do not prove data correctness, and thresholds do not replace end-to-end integrity.

### Firmware and quirks

The driver generally follows specifications and applies quirks only for documented, narrowly identified deviations. A quirk should not become a default weakening for conforming devices.

Record vendor, model, firmware and exact condition. Remove or scope obsolete workarounds when upstream evidence permits.

### Feature policy

Optional NVMe features interact with power, latency, arbitration, queues and persistence. Enable from negotiated capability and operating-system policy, not device presence alone.

Feature commands can fail or reset across power cycles. Read back effective state where specified and retain fallback behavior.

### Timeouts

A block timeout says completion was not observed within a policy interval. The command can still be queued, executing, completed but unprocessed, or lost with a path.

Arbitrate timeout with normal CQ processing. Do not unmap DMA or reuse the CID until abort, reset, transport recovery, or completion establishes safety.

### Abort

An admin abort command requests cancellation of a target command. Its own completion reports the abort request outcome, not automatically a second completion for the target.

Handle already-completed, not-found, abort-limit and racing cases. The target retains one terminal owner and its resources until resolved.

### Controller reset

Reset freezes new submission, stops or quiesces queues, masks and synchronizes interrupts, disables the controller under transport rules, contains DMA, and invalidates old command generations.

Recreate admin and I/O queues, renegotiate features, rescan namespaces and unfreeze only after readiness. Complete or retry old requests according to operation idempotency and block policy.

### Retry classification

Status includes information relevant to retry, but policy also considers operation, elapsed deadline, path, namespace state and side-effect uncertainty.

Reads are often retryable; writes, compare, reservation or administrative commands can require stronger analysis. Bound retries and preserve the original error chain.

### Hot removal

Surprise PCIe removal can make registers inaccessible before graceful shutdown. Mark the controller deleting, stop new requests, contain DMA through bus and IOMMU, synchronize callbacks and complete outstanding work with removal status.

Do not depend on a final MMIO read from a vanished function. Release queue memory only after the controller cannot access it.

### Suspend and power management

Power-state transitions coordinate queues, cache persistence, controller state and platform rules. Autonomous power-state features trade latency for energy.

Measure exit-latency tails and failure behavior. Resume validates controller identity and queue state rather than assuming context survived.

### NVMe multipath

Linux can combine paths to namespaces with the same identity into one block device. ANA states guide selection among optimized, nonoptimized, inaccessible and changing paths.

Path policy can favor NUMA locality, round-robin distribution or lower queue depth. Identity and ANA correctness precede performance policy.

### ANA change

An ANA event prompts the host to retrieve updated state. During transition, requests can queue, fail, or use another eligible path under policy.

Do not send ordinary I/O through a persistent inaccessible state. Bound transition and reconnect waits and expose path availability separately from namespace identity.

### Queue-depth path selection

Choosing the path with fewer in-flight requests can balance similar paths under uniform request sizes. Count alone ignores operation cost, network delay and controller load.

Use it as a policy with telemetry, not a proof of lowest completion time. NUMA and ANA state remain eligibility inputs.

### NVMe over Fabrics

Fabrics connect host and remote controller using discovery, connection and transport mechanisms. The storage queue is now coupled to network queues and remote service.

Keep-alive, reconnect, authentication, congestion, duplicate connections and target failover add distributed-system uncertainty. Preserve command identity and bounded recovery across reconnect.

### Transport differences

RDMA exposes registered-memory and completion-queue constraints; TCP adds sockets, segmentation, congestion and software processing; Fibre Channel has its own exchange and fabric semantics.

The NVMe command layer is common, but latency, failure detection, ordering and resource accounting differ. Tune and test each transport separately.

### Discovery and identity

Discovery controllers and records identify available subsystems and transports. Discovery data is untrusted input and can change.

Authenticate and authorize connections where required, validate identifiers and addresses, and separate discovery availability from existing I/O connection health.

### Userspace passthrough

Management and passthrough interfaces can submit commands outside ordinary filesystem and block policy. They require strict privilege, opcode, namespace, buffer, timeout and lifecycle controls.

Do not expose destructive format, firmware or reservation operations to untrusted callers. Kernel validation remains necessary even when a vendor tool constructs commands.

### Virtualization

Guests can see emulated NVMe, mediated devices, virtual functions or assigned controllers. Queue and interrupt paths may cross guest, hypervisor and host IOMMUs.

Validate untrusted guest doorbells and commands, cap queues and pinned memory, and coordinate migration by quiescing or capturing every outstanding operation and completion.

### Security

Controllers and fabrics can read and write host memory through DMA or transport. IOMMU domains, authentication, least privilege, firmware trust, descriptor validation and memory clearing constrain authority.

Treat completion fields, namespace metadata, log lengths and firmware responses as untrusted. Integer overflow or stale CID reuse can turn a storage error into kernel memory corruption.

### Observability

Record subsystem, controller, namespace, path, transport, queue, CID, tag, generation, opcode, logical range, bytes, submit, doorbell, issue, completion, interrupt, block-complete and error timestamps.

Also record queue depth, batching, polling, vector, CPU, NUMA, DMA segments, retries, aborts, resets, ANA states, reconnects, firmware and effective features. Protect data and raw addresses.

### Performance experiments

Control operation size, mix, address distribution, queue depth, jobs, cache, direct or buffered mode, flushes, dataset fill, device temperature, power state, CPU affinity, NUMA, scheduler, firmware and transport.

Sweep depth to find throughput saturation and tail growth. Separate host queue, controller, media and fabric delay where telemetry permits; avoid coordinated omission.

### Fault injection

Linux NVMe fault injection can return selected NVMe statuses and retry flags. Combine it with block timeout, transport loss, interrupt delay, mapping failure, reset, namespace change and removal tests.

Verify status mapping, bounded retries, one completion, resource release, recovery capacity and retained evidence. Injection proves tested software paths, not physical device failure behavior.

## Definitions and Notation

Let an SQ of capacity $N_s$ have host tail $T_s$ and controller-consumed head $H_s$. Let a CQ of capacity $N_c$ have controller tail $T_c$, host head $H_c$, and expected phase $\phi$. Valid occupancy stays within protocol-specific usable capacity, and neither producer overwrites an unconsumed entry.

An outstanding command is $K=(q,c,g,r,d,s)$ as above. A CQE $E=(q',c',\phi',z)$ can target $K$ only when $q'=q$, $c'=c$, $\phi'=\phi$ for the current slot, $g$ remains live in software, and state $s$ admits completion. Status $z$ then determines the terminal block result.

For command publication, required order is

$$
\text{payload/PRP} \prec \text{SQE} \prec \text{SQ tail doorbell}.
$$

For completion consumption, the controller publishes CQE fields before the phase visible to the host under the transport contract; the host acquires the entry, terminalizes the request, then advances the CQ head doorbell. These edges do not imply persistence unless flush or FUA semantics add it.

## Mechanisms, Invariants, or Proof Structure

A reviewable NVMe path discharges these obligations:

1. **Identity:** separate subsystem, controller, namespace, path, queue, request, tag and generation.
2. **Capability:** negotiate page, queue, transfer, format, cache, metadata, atomic, zone and transport limits.
3. **Allocation:** reserve admin and recovery capacity plus DMA-safe SQ, CQ and descriptor memory.
4. **Publication:** make payload and commands visible before ordered doorbells.
5. **Completion:** validate phase, SQ, CID, generation, status and request state before exactly-once termination.
6. **Capacity:** prevent SQ/CQ overwrite, tag exhaustion, completion starvation and excessive recovery scope.
7. **Topology:** map CPUs, NUMA nodes, vectors, blk-mq contexts and controller queues deliberately.
8. **Semantics:** preserve block errors, flush, FUA, atomicity, metadata, discard, zones and reservations.
9. **Paths:** validate namespace identity and ANA state before multipath optimization or retry.
10. **Recovery:** arbitrate normal completion, timeout, abort, reset, reconnect and removal while DMA stays contained.
11. **Authority:** constrain passthrough, firmware, DMA, discovery, transport and virtualized inputs.
12. **Evidence:** test depth, ordering, wrap, errors, topology, transports, power and lifecycle with scoped claims.

The proofs remain separate. A consumed SQ slot is not a completed command. A CQ interrupt is not a validated CQE. An abort CQE is not automatically the target's terminal result. A namespace identifier is not a healthy path. High IOPS is not evidence of correct persistence or bounded recovery.

## Alternatives and Trade-Offs

- **One queue versus many:** one queue simplifies synchronization; many queues reduce contention and enlarge memory and reset state.
- **Per-CPU versus shared queues:** per-CPU placement improves locality; shared queues adapt to CPU migration and limited vectors.
- **Interrupts versus polling:** interrupts save idle CPU; polling lowers wake latency at sustained load.
- **Immediate versus batched doorbells:** immediate notification lowers delay; batching amortizes MMIO.
- **Deep versus shallow queues:** depth exposes device parallelism; excess depth increases tails and recovery scope.
- **PRPs versus SGLs:** PRPs fit page-based mappings; SGLs express segments flexibly when controller and transport support them.
- **Host versus controller arbitration:** host policy sees workloads; firmware sees media internals but may hide fairness behavior.
- **Normal versus reserved tags:** shared tags maximize utilization; reservations guarantee management and recovery progress.
- **Local PCIe versus fabrics:** PCIe minimizes transport stack; fabrics add reach, sharing, path diversity and distributed failure.
- **NUMA versus round-robin path policy:** NUMA minimizes locality cost; round-robin spreads comparable paths.
- **Queue-depth path policy versus static affinity:** dynamic depth follows load; static affinity is predictable and can ignore imbalance.
- **Retry versus fail fast:** retry hides transient faults; failure bounds latency and avoids uncertain repeated side effects.
- **Quirk versus strict specification:** quirks support deployed hardware; broad workarounds weaken correctness and maintenance.
- **Kernel block path versus passthrough:** block abstractions enforce common policy; passthrough exposes features and a larger security contract.

## Failure Modes and Misconceptions

- **“NVMe is simply a faster SATA disk.”** Its queue, namespace, completion and transport model is distinct.
- **“One hardware queue per CPU is always optimal.”** vectors, NUMA, controller limits and workload decide.
- **“Maximum queue depth maximizes throughput.”** saturation can occur earlier while latency keeps growing.
- **“SQ head means the command completed.”** it reflects consumption-related state, not terminal I/O.
- **“Ring slots can be cleared instead of tracking phase.”** phase is the protocol's wrap discriminator.
- **“Commands complete in submission order.”** independent work can complete in any order.
- **“CID alone globally identifies a request.”** queue scope and software generation are also required.
- **“An interrupt identifies completion.”** software must drain and validate CQEs.
- **“Doorbell ordering publishes descriptors automatically.”** memory and DMA ordering precede MMIO notification.
- **“Timeout means DMA stopped.”** recovery must establish containment.
- **“Abort success is the target completion.”** abort and target have separate outcomes and races.
- **“Reset permits immediate tag reuse.”** stale completions and DMA require generation and synchronization.
- **“A namespace device name is stable identity.”** enumeration and path names can change.
- **“ANA optimization is merely load balancing.”** access state is an eligibility and correctness input.
- **“Flush is unnecessary on fast nonvolatile media.”** volatile controller caches and ordering still exist.
- **“Deallocate guarantees zero reads.”** that requires an explicit capability.
- **“NVMe-oF failure is a local device error.”** network and remote-controller uncertainty add layers.
- **“Fault injection proves hardware recovery.”** it exercises selected software status paths only.

## Worked Examples

### Example 1

A 32-core host receives 16 I/O queue pairs and 17 MSI-X vectors. The driver maps nearby CPU groups to queues rather than failing or forcing one global queue, and reserves the admin vector for control.

### Example 2

A request maps to blk tag 37 and CID 37 on SQ 5 with generation 9. Completion validates SQ 5, CID 37, phase and generation before unmapping DMA and ending the request.

### Example 3

The driver initializes a write command and PRP list, executes the required DMA barrier, advances the tail and rings the SQ doorbell. A source-code store order without the barrier is rejected in review.

### Example 4

A CQ interrupt arrives for several queues sharing one vector. The handler drains bounded batches from each queue, validates phase tags and schedules further work if entries remain.

### Example 5

Throughput saturates at depth 64 while the 99.9th percentile doubles from depth 64 to 256. The service caps normal tags and keeps reserved tags for abort and reset.

### Example 6

A volatile-cache namespace completes data writes quickly. A filesystem's later flush is translated and completed only when the controller confirms the required prior-write persistence.

### Example 7

Two controllers expose the same namespace identifier. Multipath selects an ANA-optimized path; after an ANA change it stops that path and moves eligible requests without changing the logical block identity.

### Example 8

An NVMe/TCP path times out. The host distinguishes transport reconnect, controller loss and target command uncertainty, bounds retries, and does not reuse DMA or request state until the transport path resolves it.

### Example 9

Surprise PCIe removal makes MMIO inaccessible. The driver freezes blk-mq queues, contains DMA through PCI and IOMMU state, synchronizes interrupts, completes outstanding requests and frees queue memory last.

### Example 10

The following toy consumes a circular CQ across wrap using phase tags. It does not model NVMe DMA, entry publication ordering, MMIO doorbells, interrupts, CIDs, status, controller behavior, or block completion.

<!-- bijux-verify: {"id":"nvme-cq-phase-consumption","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"consume slot=3 phase=1\nwrap expected=0\nconsume slot=0 phase=0\nstop slot=1 found=1 expected=0\nconsumed=2 head=1 expected=0\n","stderr":""}} -->
```python
phases = [0, 1, 1, 1]
depth = 4
head = 3
expected = 1
consumed = 0

while phases[head] == expected:
    print(f"consume slot={head} phase={expected}")
    consumed += 1
    head += 1
    if head == depth:
        head = 0
        expected ^= 1
        print(f"wrap expected={expected}")

print(f"stop slot={head} found={phases[head]} expected={expected}")
print(f"consumed={consumed} head={head} expected={expected}")
```

## Cross-Program Connections

[Computer Architecture](../../23-computer-architecture/ROADMAP.md) connects PCIe, DMA, MMIO, interrupts, caches, NUMA and persistent media. [Network Engineering](../../24-network-engineering/ROADMAP.md) connects NVMe-oF to RDMA, TCP, congestion, multipath, authentication and failure detection.

[Database Engineering](../../18-database-engineering/ROADMAP.md) connects flush, FUA, WAL, atomicity, tail latency and recovery. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) contributes state machines, queue capacity, fault containment, degraded modes and assurance. Within this program, [OS-067](067-zero-copy-and-kernel-bypass.md) develops mapped data paths and [OS-069](../ROADMAP.md) develops persistent memory.

## References

- NVM Express, Inc., [NVM Express Specification Archives](https://nvmexpress.org/nvm-express-specification-archives/), current page checked 2026-09-04. Current ratified Base, command-set and PCIe, RDMA and TCP transport specifications and revision history.
- Linux kernel documentation, [NVMe Subsystem](https://docs.kernel.org/nvme/index.html), current page checked 2026-09-04. Kernel NVMe documentation index, host policy, endpoint target and related interfaces.
- Linux kernel documentation, [Multi-Queue Block IO Queueing Mechanism](https://docs.kernel.org/block/blk-mq.html), current page checked 2026-09-04. Software and hardware contexts, requests, tags, dispatch, resource states and completion.
- Linux kernel documentation, [Linux NVMe Multipath](https://docs.kernel.org/admin-guide/nvme-multipath.html), current page checked 2026-09-04. Namespace integration, ANA and NUMA, round-robin and queue-depth path policies.
- Linux kernel documentation, [NVMe Feature and Quirk Policy](https://docs.kernel.org/nvme/feature-and-quirk-policy.html), current page checked 2026-09-04. Specification-first feature policy, quirks, compatibility and maintenance expectations.
- Linux kernel documentation, [NVMe PCI Endpoint Function Target](https://docs.kernel.org/nvme/nvme-pci-endpoint-target.html), current page checked 2026-09-04. PCIe endpoint target architecture, queue resources, interrupts, address translation and configuration.
- Linux kernel documentation, [NVMe Fault Injection](https://docs.kernel.org/fault-injection/nvme-fault-injection.html), current page checked 2026-09-04. Injected status, retry flags, debugfs controls and test examples.
- Linux kernel documentation, [How To Write Linux PCI Drivers](https://docs.kernel.org/PCI/pci.html), current page checked 2026-09-04. PCI resources, DMA, interrupts, power, error recovery and shutdown ordering.
- Linux kernel documentation, [Dynamic DMA Mapping Guide](https://docs.kernel.org/core-api/dma-api-howto.html), current page checked 2026-09-04. DMA address domains, mapping, scatter-gather, ordering, synchronization and error handling.
- Linux kernel documentation, [Linux Kernel Memory Barriers](https://docs.kernel.org/core-api/wrappers/memory-barriers.html), current page checked 2026-09-04. CPU, DMA and device ordering needed for queue publication and completion consumption.

## Exercises

### Exercise 1

Design queue allocation and CPU, NUMA and interrupt mapping for a 96-CPU dual-socket host with a 32-queue NVMe controller and four workload classes.

### Exercise 2

Prove the SQ submission and CQ completion protocol for one queue pair, including wrap, phase, CID reuse, DMA, doorbells, batching and exactly-once block completion.

### Exercise 3

Trace a write timeout racing a valid CQE, abort command, controller reset, namespace rescan and late interrupt. State when data buffers and tags can be reused.

### Exercise 4

Design NVMe multipath policy and failure handling for a two-controller subsystem reachable through local PCIe and NVMe/TCP paths with changing ANA state.

### Exercise 5

Build a verification and performance plan for a new NVMe driver across local, fabrics, virtualized, zoned and protection-information configurations.

## Answers to the Exercises

### Answer 1

Discover controller queue, vector and depth capability before allocation. Reserve the admin queue and vector plus tags and memory for abort and reset. Allocate 32 I/O queues on the NUMA node nearest the PCIe root. Map CPUs in each socket to queues deliberately rather than round-robin across sockets; CPUs remote to the device share queues with bounded locking rather than forcing remote queue memory for every core. Align completion vectors and application or blk-mq completion affinity where measurements show benefit.

Assign ordinary throughput work to most queues, retain separate polled queues only for eligible latency-critical direct I/O, and enforce cgroup and block admission above hardware queues. Recovery uses reserved tags independent of full normal depth. Sweep total and per-queue depth rather than multiplying controller maximum by CPU count. Measure cache-line traffic, remote memory, interrupts, polling CPU, throughput and tails per class. Handle CPU hotplug by remapping contexts through blk-mq, and controller reset by freezing all mapped hardware contexts before queue reconstruction.

### Answer 2

Maintain host tail, known free capacity, outstanding table indexed by CID, and one software generation per allocation. Reserve an unused SQ slot or follow exact protocol capacity. Map request data, build PRP or SGL descriptors, initialize the SQE and outstanding record, apply DMA and memory ordering, publish the tail and ring once for the batch. The controller cannot be assumed to complete in order. Do not reuse an SQ slot before consumption permits it or a CID before terminal cleanup.

For CQ, read the current slot's phase using acquire semantics under the transport contract. If it differs from expected, stop. Otherwise copy and validate SQ identifier, CID, generation, status and state; arbitrate with timeout; unmap DMA; translate status; complete the block request exactly once; and advance head. On wrap toggle expected phase. Ring the CQ head after a bounded batch. Prove neither producer overwrites an unconsumed slot, every accepted CID has one outstanding record, descriptor publication precedes doorbell, CQ publication precedes field use, and one terminal path releases each tag.

### Answer 3

Timeout atomically changes the request from ordinary in-flight to recovery-owned unless CQ processing already terminalized it. It retains DMA, command memory, tag and request. An admin abort uses reserved capacity and has its own CID and completion. If the target CQE arrives and validates while abort races, the state machine lets one target terminal transition win; the abort result is still reaped but cannot complete the target twice. If abort establishes cancellation under the specification, normal cleanup follows only after target access is resolved.

If uncertainty remains, freeze affected queues and reset. Disable submission, synchronize interrupt and polling paths, contain controller DMA, invalidate the old controller generation, recreate admin and I/O queues, renegotiate features and rescan namespaces. Late CQEs or interrupts from the old generation are rejected. A write is retried only when block and device policy make side effects safe; otherwise report the preserved failure. Buffer unmap, request completion and tag reuse occur after validated normal completion or reset containment, never at the timeout observation alone.

### Answer 4

Identify the namespace with stable subsystem and namespace identifiers and validate equal format and capacity across controllers. Treat ANA state as eligibility: optimized local paths first, nonoptimized only under policy, inaccessible paths excluded, and transition states bounded. Prefer the local PCIe path for latency and NUMA locality when healthy; use the second local controller if present, then NVMe/TCP for failover or deliberate bandwidth distribution. Queue-depth policy is useful only among eligible comparable paths and should include operation-size and observed-latency evidence.

On ANA event, retrieve authoritative ANA logs, serialize path-state update, stop sending on newly inaccessible paths and reroute eligible unissued work. For timed-out issued writes, do not blindly duplicate across TCP until command fate is resolved or higher-level idempotency permits it. Maintain transport keep-alive, reconnect bounds and authentication separately from namespace state. Test loss of each controller, partial network partition, stale ANA notification, asymmetric latency, reconnect with changed identity, simultaneous path recovery, flush ordering and reservation state. Expose logical availability, per-path health and degraded policy independently.

### Answer 5

Specify controller and namespace identity, queue counts and depths, page size, PRP and SGL formation, DMA directions, publication barriers, doorbells, CID generations, phase handling, status mapping, block limits, cache, flush, FUA, atomic properties, metadata, protection information, zones, reservations, events, timeout, abort, reset and removal. Unit-test circular arithmetic, wrap, phase, descriptor bounds, status tables and generation races. Use DMA and lock debugging plus NVMe fault injection.

Run physical PCIe, NVMe/RDMA or TCP, virtual and endpoint-target paths where supported. Exercise queue-count scarcity, every depth, vectors, polling, NUMA, IOMMU, mapping failure, CQ stall, invalid CQE, retry statuses, lost interrupt, timeout, abort limit, reset, power transition, firmware activation, namespace add/remove or format, ANA change, reconnect and hot-unplug. Include zoned write-pointer and protection-metadata corruption tests. Measure boundary-specific latency, throughput, CPU, cache, network and recovery while avoiding coordinated omission. Preserve specifications, kernel, firmware, hardware, topology, features, commands, seeds, traces, injected faults, negative results and limitations; no one transport or benchmark proves complete conformance.
