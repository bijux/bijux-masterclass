---
module_id: CA-042
program: Computer Architecture
level: 1
module_number: 42
title: Interrupts and Direct Memory Access
status: complete
last_verified: 2026-09-04
---

# Interrupts and Direct Memory Access

## One-Page Review

### Governing question

How can devices asynchronously request processor service and transfer data directly to memory while preserving interrupt identity/priority, descriptor and buffer ownership, address translation/protection, cache coherence, ordering, partial-completion/error semantics, progress and diagnosability?

### Essential definitions

- An **interrupt** is an asynchronous control-transfer request delivered according to architecture/controller state.
- An **interrupt source** is a device or internal event that asserts pending state.
- An **interrupt controller** prioritizes, routes, masks/enables and tracks interrupts for targets/contexts.
- A **level-triggered interrupt** remains asserted while its condition holds; an **edge-triggered interrupt** records a transition/event.
- **claim/acknowledge** identifies an interrupt selected for service; **complete/end-of-interrupt** releases controller in-service state.
- An **interrupt service routine** (`ISR`) handles enough device state to make progress, often deferring heavier work.
- **interrupt coalescing** combines multiple completions/events before notifying a processor.
- **direct memory access** (`DMA`) lets an engine transfer between device, memory or peripherals without CPU copying each data beat.
- A **DMA descriptor** describes source, destination, length, direction, attributes, chaining and completion/error metadata.
- A **descriptor ring** is a circular producer/consumer queue shared between software and hardware.
- **ownership** identifies whether software or device may modify/consume a descriptor or buffer.
- An **IOMMU** translates/protects device DMA addresses and may maintain device translation caches.
- A **scatter-gather list** describes a logical transfer using multiple noncontiguous memory segments.
- **cache-coherent DMA** participates in platform coherence; **noncoherent DMA** requires explicit cache maintenance/ownership rules.
- **residue** is the amount not transferred when an operation stops, under a defined accounting point.

### Central model, mechanism, or theorem

Interrupt correctness is a pending/in-service state machine: a source event becomes pending, routing/priority selects one enabled target, claim transfers its identity into service, the handler quiesces or records the device cause, and completion releases controller state without losing a concurrently arriving event. DMA correctness is an ownership protocol: software constructs data/descriptors, performs required visibility operations, transfers ownership; hardware validates/translates and moves only authorized bytes, records completion/error atomically, returns ownership, orders the record before notification; software then synchronizes before consuming results.

### Critical invariants

- Every delivered interrupt corresponds to a permitted pending source and correct privilege/target context.
- Masking/prioritization cannot fabricate, misidentify or permanently lose a pending condition.
- Level conditions are quiesced or remain pending; edge events are latched/countable according to capacity.
- Claim/complete identities match and concurrent events cannot be cleared accidentally.
- DMA never reads/writes outside validated descriptor segments, IOMMU permissions or length boundaries.
- At any moment, descriptor/buffer mutability belongs to software or device under an explicit ownership state.
- Descriptor/data visibility precedes device consumption; completion/result visibility precedes processor notification/consumption.
- Noncoherent cache maintenance covers exact ranges/directions without discarding dirty/newer data.
- Partial transfers, faults, cancellation and reset report exact committed bytes/residue and do not silently replay non-idempotent work.
- Finite rings, credits, interrupts and response queues retain conditional progress without deadlock/starvation.

### Common failures

Common failures include clearing device status before recording all causes, completing a level interrupt while the source remains asserted without re-pending, acknowledging the wrong ID, reusing vectors across guests without isolation, enabling interrupts before handler/ring initialization, publishing an owned descriptor before its fields/data, using a CPU virtual pointer as a DMA address, mapping the wrong direction, flushing rather than cleaning dirty transmit buffers, invalidating receive buffers while CPU dirty data exists, assuming coherent means ordered, notifying before completion data is visible, trusting device-provided length, wrapping a ring without generation bits, retrying a partially completed device write, and freeing mappings while DMA remains outstanding.

### Compact example

Three invented DMA descriptors copy 64, 128 and 32 bytes for 224 total. With 16-byte beats they require 4, 8 and 2 beats. At five setup cycles per descriptor and one beat/cycle, total modeled time is 29 cycles and payload throughput 7.72 bytes/cycle. One interrupt per descriptor gives three notifications; one coalesced notification reduces that count by 66.67%. The arithmetic excludes contention, translation, cache maintenance and error recovery.

### Connections

Interrupts/DMA connect exceptions/privilege, MMIO, queues/rings, memory ordering, coherence, IOMMUs, PCIe/MSI, cache maintenance, OS drivers, virtualization, real-time latency, device security, zero-copy networking/storage and formal ownership protocols.

## Governing Question

Polling lets software ask repeatedly whether work exists. Interrupts let devices signal asynchronously. Programmed I/O lets the CPU move each word; DMA lets a device engine move blocks using descriptors.

Both optimizations create concurrency. A handler races new events; a DMA engine races CPU cache accesses and descriptor updates. Correctness comes from explicit pending/in-service and producer/consumer ownership protocols.

## Why This Matters

Interrupt loss can leave a device permanently stuck. Interrupt storms can monopolize a core. DMA with an unchecked address can overwrite arbitrary memory. A missing ordering operation can expose a descriptor before its payload or an interrupt before completion data.

High-throughput devices depend on rings, batching, coalescing and scatter-gather. These improve efficiency but complicate wraparound, fairness, latency and recovery.

Virtualization and untrusted devices require remapping, interrupt isolation and revocation that extend beyond CPU page tables.

## Prerequisites and Retrieval

Before studying this module, be able to:

- trace exceptions, privilege transitions and MMIO register effects;
- use producer/consumer ring invariants and memory-order reasoning;
- distinguish virtual, physical and device/DMA addresses;
- explain coherent versus noncoherent caches;
- reason about partial I/O, idempotence and error recovery.

Retrieve interrupt architecture/controller version; sources, IDs/vectors, triggers, polarity, priority, routing, contexts, masking, claim/complete; CPU trap delegation and handler ABI; MSI/message format/remapping; device cause/status/clear behavior; DMA engine/channels; descriptor/ring layouts, alignment and endian; address/length widths; scatter-gather/chaining; burst/alignment/boundary rules; coherent/noncoherent attributes and cache-line constraints; IOMMU domains, translations, permissions and invalidation; memory barriers/accessors; completion/writeback/notification ordering; outstanding/cancel/reset/timeout; partial/error/residue semantics; security isolation; counters/traces; RTL/firmware/OS/driver/device revisions and errata.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish edge/level pending, claim and completion behavior;
2. design interrupt routing, masking, priority and handler ordering;
3. construct safe DMA descriptors and rings with explicit ownership;
4. map CPU buffers to device addresses through DMA/IOMMU APIs;
5. apply coherent or noncoherent synchronization correctly;
6. order descriptor/data publication and completion notification;
7. handle scatter-gather, alignment, boundaries and partial results;
8. design coalescing/polling trade-offs and progress/fairness controls;
9. verify interrupt/DMA safety under concurrency, errors and reset;
10. evaluate throughput, latency, CPU cost and isolation with reproducible evidence.

## Core Exposition

### Model interrupt state

Separate raw source condition, pending latch/counter, enable/mask, selected target and in-service identity. Delivery is not the same as source generation.

Document which stage retains an event while masked and what capacity exists for repeated edges.

### Handle level-triggered sources

A level remains asserted until its device condition is cleared or deasserted. The handler normally reads cause, services/records work and clears/quiesces before controller completion.

If level persists, the controller should redeliver or keep pending rather than lose the condition.

### Handle edge-triggered sources

An edge becomes a latch, counter or message. A single pending bit can coalesce multiple edges, so devices needing exact counts require queue/counter state.

Define behavior for another edge while pending or in service.

### Route and prioritize

Controllers map sources to cores/harts/contexts and compare priority against thresholds/current privilege. Affinity spreads load or preserves locality.

Routing changes need synchronization so an interrupt is not lost between old and new targets.

### Mask safely

Masking prevents delivery, not necessarily event capture. Determine whether a pending event remains latched and whether device generation must also be disabled.

Initialization masks before installing state, clears stale causes, installs handler/ring, then unmasks in defined order.

### Claim and complete

Claim returns an eligible source identity and marks/controller-tracks service. Completion must use the matching ID/context under controller rules.

Do not complete an ID never claimed or reuse an in-service slot across guests/handlers.

### Read device cause

One vector may represent several causes. Snapshot cause/status before destructive clear and loop until quiescent when new events can arrive concurrently.

Use documented W1C/read-clear semantics; unsafe read-modify-write can erase new status.

### Keep ISRs bounded

An ISR acknowledges/quiesces hardware, records minimum state and schedules deferred processing. Long handlers increase interrupt latency and priority inversion.

Budget nesting, stack, locking and preemption explicitly.

### Prevent interrupt storms

Faulty or high-rate sources can continually interrupt. Mask-on-entry, moderation, budgets and polling modes bound CPU consumption while retaining work.

Storm containment must not discard the only error/completion evidence.

### Coalesce notifications

Devices can interrupt after `N` completions or a timer. Larger batches reduce CPU overhead but increase first-item latency and may delay low traffic indefinitely.

Use count plus timeout and expose tuning/counters.

### Use polling adaptively

Under load, poll a bounded batch after one interrupt, then re-enable interrupts with a race-free check for newly arrived work. This avoids per-packet interrupts.

The handoff must close the lost-wakeup window between empty check and unmask.

### Understand message-signaled interrupts

MSI-like interrupts are device writes/messages containing destination/vector data. They require address/data authorization and ordering after completion records.

Interrupt remapping isolates devices/guests and validates messages.

### Define DMA roles

The CPU/driver prepares descriptors and buffers; a DMA engine fetches them and issues memory/device transactions; completion returns status/ownership.

The engine may be integrated in the device or a general system DMA controller.

### Distinguish address domains

A CPU virtual pointer is not automatically usable by a device. DMA mapping returns a device-visible address that may equal a physical address or an IOMMU IOVA.

Use platform APIs so translation, bounce buffering, cache and lifetime rules are honored.

### Validate descriptors

Check valid/owned bit, format/version, source/destination, nonzero/maximum length, alignment, boundary, permissions, direction and next pointer before execution.

Treat descriptors from untrusted devices/guests as hostile input.

### Transfer descriptor ownership

Software writes all descriptor fields/data, performs required synchronization, then sets/publishes ownership or advances producer index. It no longer mutates owned fields.

Hardware returns ownership only after completion/error fields are visible.

### Use generation bits

Producer/consumer indices alone are ambiguous when equal after wrap. Generation/phase bits distinguish empty from full and old from new descriptors.

Increment/toggle only at the specified wrap and retain enough counter width.

### Handle rings

A ring of `N` entries must never let producer lap consumer beyond capacity. Reserve entries before publishing and reclaim only completed ownership.

Doorbells indicate new work but are not the descriptor data themselves.

### Order doorbells

Make descriptor and source-buffer writes visible to the device before MMIO doorbell. Architecture/platform DMA barriers and cache sync may both be necessary.

A compiler barrier alone does not guarantee device observation.

### Order completion notifications

The engine writes destination/completion status, establishes required visibility, then raises interrupt/update. The handler synchronizes before reading them.

An interrupt arriving first can expose stale completion records or data.

### Implement scatter-gather

Scatter-gather describes multiple segments. Validate each address/length and total without integer overflow; preserve logical byte order.

Hardware segment count, page/burst boundaries and maximum transfer limits apply.

### Respect alignment and boundaries

Engines may require beat/cache-line/page alignment or prohibit crossing 4 KiB boundaries in one burst. Split safely while preserving total length and side effects.

Never round outward into unauthorized adjacent memory.

### Handle unaligned endpoints

If supported, first/last partial beats use exact byte enables. Otherwise reject/bounce through aligned storage.

Reads must not disclose bytes outside the authorized buffer and writes must preserve them.

### Participate in coherence

Coherent DMA transactions snoop/cache-cohere under platform attributes, reducing explicit maintenance. Coherence does not automatically impose descriptor/order barriers.

Verify device, IOMMU/interconnect and mapping all select coherent semantics.

### Manage noncoherent transmit buffers

Before device reads CPU-produced data, clean/write back exact cache lines and order completion; avoid later CPU writes until ownership returns.

Partial-line sharing risks writing unrelated dirty bytes or device/CPU false sharing.

### Manage noncoherent receive buffers

Before device writes, ensure CPU dirty lines cannot later overwrite device data. After completion, invalidate/synchronize so CPU reads new bytes.

Use platform DMA APIs rather than ad hoc cache operations.

### Choose DMA direction correctly

Direction tells mapping/synchronization which agent reads/writes. `to-device`, `from-device` and bidirectional have different maintenance and permission consequences.

Wrong direction can corrupt or expose stale data even if addresses are correct.

### Use IOMMU protection

Map only required pages with least read/write privilege into the device domain. Validate IOVA ranges and isolate devices/guests.

Unmap/revoke only after DMA quiescence and required IOTLB invalidation completion.

### Invalidate device translations

IOMMUs/devices can cache translations. Page-table update plus invalidation/order must prevent a late device access using stale permissions.

CPU TLB shootdown alone is insufficient.

### Handle faults

Translation, permission, bus, device and descriptor faults stop or mark operations per contract. Capture offending descriptor/address/cause and exact completed/residue bytes.

Do not continue into subsequent unvalidated descriptors after fatal state unless explicitly safe.

### Define partial completion

Specify whether completion counts fetched, accepted, committed or destination-visible bytes. Residue must use the same endpoint.

Partial non-idempotent device writes may not be replayable; recovery might resume only remaining safe segments or fail the operation.

### Cancel safely

Cancellation first prevents new descriptor fetch/issue, then waits/aborts outstanding work under supported semantics and returns exact status/ownership.

Freeing/unmapping buffers before quiescence creates use-after-free DMA.

### Reset safely

Reset can destroy engine tracking while memory transactions remain. Quiesce/fence upstream, isolate late responses and reconcile descriptor ownership.

Never mark all descriptors free without determining which writes may have committed.

### Handle timeouts

A timeout signals lack of observed completion, not proof of zero side effect. Stop/quarantine the engine and inspect progress/error state before retry.

Use generations/transaction IDs to reject late completions.

### Allocate fair channels

Multiple clients share DMA channels, memory bandwidth and descriptor fetch queues. Weighted/round-robin/priority policies need starvation bounds.

Reserve progress for completions/errors so full outbound work cannot deadlock response handling.

### Bound outstanding work

Descriptors may expand into many bus transactions. Credits bound requester IDs, IOMMU walks, interconnect and completion buffers.

Admission should reserve enough downstream/return state for accepted work.

### Secure descriptors

Place rings in protected memory, validate owner/length/next fields and prevent device writes into control fields it should not own. Use IOMMU least privilege.

Avoid leaking stale bytes in bounce buffers or padding.

### Virtualize interrupts and DMA

Guests need isolated vectors, controller contexts, DMA domains and reset ownership. Hypervisors remap MSI and IOVA while preserving completion/order.

Migration/quiescence must capture or drain in-flight device state.

### Measure interrupt behavior

Count generated, pending, delivered, claimed, completed, coalesced, spurious and storm-masked events. Measure device-event-to-handler and handler/service distributions.

Correlate affinity, masking and load; interrupt count alone is not work count.

### Measure DMA behavior

Report payload bytes, bus bytes, descriptors, segments, transactions, setup/queue/service latency, throughput, CPU cycles, cache maintenance, IOMMU misses/faults and errors.

Separate useful payload from descriptor/completion/coherence overhead.

### Verify interrupts

Assert pending conservation, legal routing/priority, matching claim/complete and level/edge behavior under simultaneous cause/clear. Test masking, nesting, storms and reset.

Use latency tests and formal state-machine properties where feasible.

### Verify DMA

Use a reference memory/ownership model, guard pages, IOMMU faults and byte-accurate scoreboards. Inject backpressure, partial errors, cancellation, reset and ring wrap.

Assert bounds, permissions, order, no duplicate/lost bytes and exact completion records.

### Gather layered evidence

Start with descriptor arithmetic/state traces, then block formal/tests, subsystem simulation, kernel driver tests, IOMMU fault injection and hardware tracing.

Bind architecture/controller/DMA RTL, device firmware, IOMMU, OS/driver, topology and errata.

## Definitions and Notation

- `pending[i]`: source `i` has retained service condition/event.
- `enabled[i,c]`: source `i` may signal context `c`.
- `in_service[c]`: claimed source or empty for target context.
- `claim(c)`: highest eligible pending source under routing/priority/threshold.
- `N`: descriptor-ring entry count.
- `prod`, `cons`, `phase`: producer/consumer positions and wrap generations.
- `D=(src,dst,length,flags,next,status,owner)`: abstract descriptor.
- `IOVA`: device-visible virtual address translated by IOMMU.
- `completed_bytes`: bytes at the contract's committed/visible endpoint.
- `residue=total_length-completed_bytes` under the same endpoint.
- `B`: DMA beat bytes; beats for aligned length `L` are `ceil(L/B)`.
- `coalescing_count`: completions per notification threshold, with timeout as needed.
- `ownership(x) in {software,device,transition,error}`.
- `notify_after_visible`: completion writes happen-before interrupt observation under platform rules.

Interrupt controller and DMA APIs use architecture-specific names. Map pending/claim/complete, direction, coherence and completion endpoints to exact documentation.

## Mechanisms, Invariants, or Proof Structure

1. **Event obligation:** every source event/level condition is retained or explicitly coalesced within documented capacity.
2. **Delivery obligation:** only enabled/routed/priority-eligible interrupts reach the correct context.
3. **Service obligation:** claim and complete identities match; concurrent source changes are not lost.
4. **Descriptor obligation:** format, address, length, flags, links and arithmetic validate before use.
5. **Ownership obligation:** only the owning agent mutates/consumes each descriptor/buffer state.
6. **Publication obligation:** descriptor/source data is visible before device ownership/doorbell.
7. **Completion obligation:** destination/status is visible before ownership return/notification.
8. **Address obligation:** DMA accesses only mapped IOVA/physical segments with correct direction/permissions.
9. **Byte obligation:** bursts, masks, scatter segments and boundaries move exactly authorized bytes.
10. **Coherence obligation:** coherent attributes or noncoherent cache synchronization preserve newest data.
11. **Ordering obligation:** barriers, atomics, device accesses and same-buffer dependencies observe platform rules.
12. **Recovery obligation:** faults/cancel/timeout/reset preserve exact partial state and block unsafe replay/free.
13. **Resource obligation:** rings, IDs, credits, response/error state remain within capacity.
14. **Progress obligation:** interrupts, completions and clients make progress under stated fairness.
15. **Evidence obligation:** correctness/performance claims bind mappings, revisions, workloads and endpoints.

Prove interrupt state conservation and descriptor-ring ownership separately, then compose notification ordering so each completion causes eventual observable service without preceding its data. Refine DMA transactions to an authorized byte-copy relation plus explicit partial/error states. Progress depends on controller, interconnect and scheduler fairness.

## Alternatives and Trade-Offs

1. **Polling versus interrupts:** polling reduces notification overhead under load; interrupts save idle CPU/time-to-first-work.
2. **Edge versus level:** edges capture events compactly; levels naturally represent persistent conditions.
3. **Dedicated versus shared vectors:** dedicated vectors aid affinity/isolation; shared vectors conserve controller entries.
4. **Immediate versus coalesced interrupts:** immediate minimizes latency; coalescing reduces CPU overhead.
5. **Fixed versus dynamic affinity:** fixed preserves locality; dynamic balances load.
6. **Programmed I/O versus DMA:** PIO suits tiny/control transfers; DMA amortizes setup for bulk data.
7. **Single buffer versus ring:** single state is simple; rings pipeline many operations.
8. **Contiguous versus scatter-gather:** contiguous simplifies hardware; SG avoids copies/large allocations.
9. **Coherent versus noncoherent DMA:** coherent simplifies sharing; noncoherent can reduce coherence cost with maintenance burden.
10. **Physical addressing versus IOMMU:** physical paths are simple; IOMMU provides isolation/remapping at translation cost.
11. **Per-descriptor versus batched doorbells:** per-item lowers queue delay; batching amortizes MMIO.
12. **In-order versus out-of-order completion:** in-order simplifies reclaim; out-of-order exposes device parallelism.
13. **Large versus small descriptors:** large amortize setup; small improve granularity/fairness/cancel precision.
14. **Abort versus drain cancellation:** abort lowers delay but complicates partial state; drain preserves simple completion.
15. **Throughput versus isolation/QoS:** shared deep queues maximize use; quotas/priority protect tenants/tails.

## Failure Modes and Misconceptions

1. “Interrupt delivery equals source generation.” Pending/mask/routing add state and delay.
2. “One pending bit counts every edge.” Multiple edges can coalesce/loss without counters/queues.
3. “Completing a level interrupt clears the device.” Device cause must be quiesced separately.
4. “Read-clear cause may be read repeatedly.” It can consume state.
5. “Masking always discards events.” Many controllers retain pending; exact rules matter.
6. “Claim and complete IDs are interchangeable.” Completion must match claimed context/source.
7. “ISR should finish all work.” Deferred/batched processing bounds latency.
8. “More coalescing only saves CPU.” It increases latency and can strand low-rate work without timeout.
9. “A C pointer is a DMA address.” Mapping/IOMMU returns the device-visible address.
10. “Descriptor ownership is advisory.” Concurrent mutation creates torn commands/results.
11. “Doorbell orders prior writes automatically.” DMA/MMIO barriers and cache sync may be required.
12. “Interrupt means completion data is visible.” Device/interconnect must order writes before notification.
13. “Coherent DMA needs no barriers.” Coherence and ordering are distinct.
14. “Noncoherent transmit needs invalidate.” Dirty CPU data generally must be cleaned for device reads.
15. “Noncoherent receive can invalidate anytime.” CPU dirty bytes could overwrite device results.
16. “Bidirectional mapping is always safest.” It can cost more and obscure actual permissions/direction.
17. “IOMMU mapping revocation is instant.” IOTLB/device caches and in-flight work need invalidation/quiescence.
18. “Scatter lengths can be summed in native width.” Overflow and maximum limits require checked arithmetic.
19. “DMA may round transfers to alignment.” That can access unauthorized adjacent bytes.
20. “Equal ring indices always mean empty.” Wrap/generation distinguishes full versus empty.
21. “Timeout means zero bytes moved.” Partial work may have committed.
22. “Retry the whole transfer after error.” Non-idempotent destinations can be duplicated.
23. “Reset returns all descriptors to software safely.” In-flight writes/ownership require reconciliation.
24. “Interrupt count equals packet/operation count.” Coalescing/shared causes break equivalence.
25. “Peak bus bandwidth equals DMA throughput.” Setup, descriptors, boundaries, contention and maintenance reduce it.
26. “Successful copy tests prove isolation.” Guard/IOMMU/error/concurrency cases are required.

## Worked Examples

### Example 1

A level UART interrupt remains asserted while RX FIFO nonempty; handler drains a bounded batch and completes, causing redelivery if data remains.

### Example 2

Two edges arrive before service but one pending bit exists; software observes one interrupt unless the device/controller also records a count/cause queue.

### Example 3

Software fills descriptors and transmit buffers, syncs/orders them, publishes producer ownership and finally rings the MMIO doorbell.

### Example 4

A receive descriptor's buffer is owned by device; CPU does not touch it until completion plus DMA synchronization returns ownership.

### Example 5

An IOMMU domain maps only two read-only source pages and two writable destination pages; an out-of-range descriptor faults before memory corruption.

### Example 6

A scatter list splits at a hardware 4 KiB boundary while preserving the same logical byte sequence and total length.

### Example 7

A transfer faults after 96 of 128 bytes at the documented committed endpoint; residue reports 32 and whole replay is rejected for a non-idempotent target.

### Example 8

A coalescer interrupts after 32 completions or 50 microseconds, whichever comes first, avoiding indefinite latency at low load.

### Example 9

During cancel, the driver stops new fetch, waits for issued transactions and IOTLB quiescence, then unmaps and frees buffers.

### Example 10

This deterministic descriptor model audits byte/beat totals, setup amortization and notification coalescing.

<!-- bijux-verify: {"id":"dma-descriptor-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"descriptors=3 total_bytes=224 total_beats=14\nbeats=4,8,2 setup_cycles=15 transfer_cycles=14 total_cycles=29\npayload_bytes_per_cycle=7.72 interrupts_immediate=3 interrupts_coalesced=1 reduction_pct=66.67\n"}} -->
```python
descriptors = [
    (0x1000, 0x2000, 64),
    (0x1040, 0x2040, 128),
    (0x10c0, 0x20c0, 32),
]
beat_bytes = 16
setup_per_descriptor = 5

beats = [(length + beat_bytes - 1) // beat_bytes for _, _, length in descriptors]
total_bytes = sum(length for _, _, length in descriptors)
setup_cycles = len(descriptors) * setup_per_descriptor
transfer_cycles = sum(beats)
total_cycles = setup_cycles + transfer_cycles
immediate_interrupts = len(descriptors)
coalesced_interrupts = 1

print(f"descriptors={len(descriptors)} total_bytes={total_bytes} total_beats={sum(beats)}")
print(f"beats={','.join(str(value) for value in beats)} setup_cycles={setup_cycles} transfer_cycles={transfer_cycles} total_cycles={total_cycles}")
print(f"payload_bytes_per_cycle={total_bytes / total_cycles:.2f} interrupts_immediate={immediate_interrupts} interrupts_coalesced={coalesced_interrupts} reduction_pct={100 * (immediate_interrupts - coalesced_interrupts) / immediate_interrupts:.2f}")
```

The descriptors and timing are invented. Transfers are aligned, nonoverlapping, fully authorized and one beat/cycle; the model omits bus/IOMMU/cache/coherence contention, partial errors and actual interrupt latency.

## Cross-Program Connections

- **Operating Systems:** IRQ domains, DMA APIs, rings, barriers and drivers implement the contract.
- **Concurrent Systems:** pending/in-service and producer/consumer ownership govern races/progress.
- **Networking and Storage:** scatter-gather, completion queues, coalescing and zero-copy dominate data paths.
- **Virtualization:** interrupt remapping and IOMMU domains isolate guests/devices.
- **Security Engineering:** least-privilege DMA mapping and descriptor validation contain devices.
- **Reliability Engineering:** partial completion, timeout, reset and telemetry enable recovery.
- **Performance Engineering:** batching, setup amortization, CPU cost, latency and bandwidth guide tuning.
- **Formal Methods:** conservation, ownership, happens-before and byte refinement structure proofs.

## References

1. RISC-V International, [Machine-Level ISA](https://docs.riscv.org/reference/isa/priv/machine.html), current interrupt, trap, privilege and memory context; retrieved 2026-09-04.
2. Linux kernel, [Generic IRQ Handling](https://docs.kernel.org/core-api/irq/index.html), current interrupt descriptor/chip/domain handling documentation; retrieved 2026-09-04.
3. Linux kernel, [Dynamic DMA Mapping Guide](https://docs.kernel.org/core-api/dma-api-howto.html), current DMA address, direction, coherent/streaming mapping and synchronization guidance; retrieved 2026-09-04.
4. OpenTitan, [DMA Controller](https://opentitan.org/book/hw/ip/dma/), current open DMA architecture, registers, security and verification documentation; retrieved 2026-09-04.
5. Arm, [AMBA Architectures](https://developer.arm.com/Architectures/AMBA), current bus/interconnect transaction framework relevant to DMA engines; retrieved 2026-09-04.
6. Sarah L. Harris and David Money Harris, [Digital Design and Computer Architecture: RISC-V Edition Resources](https://pages.hmc.edu/harris/ddca/ddcarv.html), interrupt and DMA teaching resources; retrieved 2026-09-04.

## Exercises

### Exercise 1

Trace edge- and level-triggered source state through mask, route, claim, concurrent arrival, device clear and complete operations.

### Exercise 2

Design a descriptor ring with producer/consumer generation bits and precise ownership/publication/completion ordering.

### Exercise 3

Specify coherent and noncoherent DMA workflows for transmit and receive buffers, including partial cache lines and IOMMU mappings.

### Exercise 4

Extend the executable model with scatter-gather boundaries, ring batching, partial faults and exact residue accounting.

### Exercise 5

Write an end-to-end verification/evaluation plan for an interrupting DMA device assigned through an IOMMU to multiple guests.

## Answers to the Exercises

### Answer 1

Maintain raw event/level, pending storage, enable/route/priority and in-service ID separately. Mask suppresses delivery according to exact capture rules. Claim removes/selects pending into service; another edge increments/latches capacity, while persistent level remains or re-pends. Handler snapshots/clears device cause before matching completion.

Test simultaneous claim/new event, clear/new assertion, reroute, mask/unmask and wrong completion. Assert delivered implies permitted pending and every retained condition eventually redelivers under fairness.

### Answer 2

Each slot has phase/owner and immutable device-owned command fields plus device-written result fields. Software reserves a nonfull slot, writes fields/data, orders visibility, publishes owner/producer phase and rings doorbell. Hardware validates, executes, writes status/residue, orders visibility and returns owner/completion phase before notification.

Consumer compares index plus phase, reclaims only returned slots and toggles on wrap. Assert occupancy bounds, no overwrite, exclusive ownership, ordered publication/completion and no ABA across generations.

### Answer 3

Map buffers with correct direction and receive device-visible addresses. Coherent transmit still orders CPU data/descriptor before ownership; coherent receive synchronizes completion before CPU consumption. Noncoherent transmit cleans exact lines before device ownership and forbids CPU mutation; noncoherent receive prevents dirty CPU lines, then invalidates/syncs after device completion.

Avoid partial-line sharing or use bounce buffers. Map IOMMU least privilege, retain mapping until quiescence, invalidate IOTLB on revoke and never treat CPU virtual address as DMA address.

### Answer 4

Validate each segment with checked total arithmetic, split at maximum beat/page boundaries and preserve logical order. Model ring capacity, per-batch doorbells/notifications and setup cycles. Inject a fault at a chosen committed byte boundary, stop new issue and record completed bytes/residue at the same endpoint.

For idempotent memory copies, resume only remaining authorized segments after repair; for non-idempotent endpoints, report partial state without whole replay. Verify total=completed+residue and no byte outside segments moves.

### Answer 5

Verify interrupt event conservation, route/priority/context, claim/complete, masking/storm/coalescing and guest vector remapping. Verify ring ownership, descriptor hostility, IOVA permissions, IOTLB invalidation, exact bytes/order, coherent/noncoherent sync, completion-before-notify, partial errors, cancellation, reset/migration and finite-resource progress with scoreboards, formal assertions and fault injection.

Measure event-to-handler tails, notifications/work, CPU cost, descriptor/IOVA translation traffic, payload/bus bytes, setup/queue/service throughput, fairness and guest interference. Bind controller/DMA/device RTL/firmware, IOMMU/hypervisor/OS/driver, topology and errata; internal evidence is not external interrupt, isolation or silicon certification.
