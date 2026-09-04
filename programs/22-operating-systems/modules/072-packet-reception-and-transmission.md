---
module_id: OS-072
program: Operating Systems
level: 2
module_number: 72
title: Packet Reception and Transmission
status: complete
last_verified: 2026-09-04
---

# Packet Reception and Transmission

## One-Page Review

### Governing question

How should an operating system move packets between a network device and protocol endpoints while preserving DMA ownership, bounds, checksum and segmentation meaning, queue fairness, namespace and policy decisions, timestamps, completion, and safe recovery under overload or device failure?

### Essential definitions

- A **receive descriptor** gives a device writable buffer ownership and later reports a received frame, length, status, and metadata.
- A **transmit descriptor** gives a device packet segments and offload instructions whose memory remains owned until completion.
- **NAPI** is Linux's event-processing mechanism that schedules bounded polling after device notification and can process receive events and transmit completions.
- An **interrupt moderation** policy coalesces device notifications to reduce interrupt work at the cost of added event delay.
- **RSS** distributes received flows among device queues; **RPS/RFS** can steer processing in software; **XPS** selects transmit queues using CPU or receive-queue relationships.
- **XDP** executes a verified program early in the receive path and can pass, drop, transmit, or redirect a frame under defined ownership rules.
- **GRO** combines compatible received packets into a larger internal packet; **GSO** represents a large outgoing packet that software or hardware later segments.
- A **checksum offload state** records whether a checksum is absent, verified, complete, or prepared for later completion; it is not a generic “checksum good” Boolean.
- A **qdisc** is a transmit queueing discipline that can schedule, shape, classify, or drop packets before driver submission.
- **BQL** bounds bytes queued to a device transmit queue dynamically so software can avoid excessive hidden device queueing while keeping hardware busy.

### Central model, mechanism, or theorem

Represent a packet instance as

$$
K=(b,o,d,q,n,h,c,g,t,r),
$$

where $b$ is the backing buffer, $o$ its current owner, $d$ the DMA mapping and synchronization state, $q$ the queue, $n$ the network namespace, $h$ validated header offsets, $c$ checksum and offload metadata, $g$ segmentation or aggregation state, $t$ timestamps, and $r$ reference and recycle state. A transition is legal only when the current owner authorizes it and every consumer receives metadata that truthfully describes the bytes it will observe.

Receive follows device-owned descriptor to completed buffer, bounded driver validation, optional XDP, packet construction, GRO, protocol demultiplexing, and socket delivery. Transmit reverses the direction: socket or forwarding output, protocol and route, qdisc, feature validation, optional segmentation, driver descriptor publication, device ownership, completion, unmap, and final release or recycle. Each queue is bounded, and every drop or error belongs to one precise stage.

### Critical invariants

- A descriptor is published only after its buffer, DMA address, length, direction, and ownership are valid and visible to the device.
- The CPU does not read device-owned receive bytes or mutate device-owned transmit bytes without the platform's DMA synchronization and ownership transition.
- Received length, offsets, fragment count, checksum state, VLAN or tunnel metadata, and offload claims are validated before deeper parsing.
- NAPI processes no more receive work than its budget and unmasks interrupts only after proving the event source is drained under the driver's race protocol.
- XDP actions transfer or release buffer ownership exactly once; redirected frames are flushed and completed under the target contract.
- GRO combines only packets whose headers, checksum, flow, encapsulation, and policy state permit aggregation.
- GSO and checksum metadata never request features the final device path cannot perform; software fallback restores correct wire packets.
- Queue selection preserves required per-flow ordering and respects topology, traffic class, shaping, and device capabilities.
- Transmit success at driver enqueue, device completion, wire emission, peer receipt, and peer application consumption remain distinct events.
- Device stop, reset, detach, and queue reconfiguration synchronize NAPI, interrupts, DMA, timers, and outstanding buffers before memory release.

### Common failures

Common mistakes are parsing beyond the reported receive length, trusting device checksum metadata without validating feature context, unmasking interrupts before a final empty-ring check, counting transmit completions against the receive budget, returning an XDP-redirected page to the source pool, merging GRO packets across incompatible metadata, applying GSO after a device feature changes without fallback, changing a flow's transmit queue while packets remain outstanding, freeing an SKB when the device still owns a descriptor, assuming driver enqueue means wire transmission, hiding all drops in one counter, tuning interrupt coalescing only for throughput, and destroying a page pool while packets still hold its pages.

### Compact example

A NAPI instance has five receive completions and two transmit completions. With receive budget three, the first poll reclaims both transmit completions and processes three receive packets, then remains scheduled because the receive budget was exhausted. The second poll processes the remaining two receive packets, completes NAPI because work is below budget, and reenables notification using the driver's race-safe sequence. Transmit cleanup is essential but does not consume the receive fairness budget.

### Connections

[OS-004](004-interrupts-and-exceptions.md), [OS-031](031-address-translation.md), [OS-051](051-per-cpu-state.md), [OS-052](052-smp-kernel-synchronization.md), [OS-055](055-numa-memory-placement.md), [OS-058](058-timer-and-interrupt-scalability.md), [OS-063](063-direct-memory-access.md), [OS-067](067-zero-copy-and-kernel-bypass.md), [OS-070](070-designing-an-i-o-path-for-latency-or-throughput.md), and [OS-071](071-socket-layer-architecture.md) connect packet processing to interrupts, DMA, concurrency, topology, queues, direct paths, and socket delivery.

## Governing Question

A packet crosses many representations between the wire and an application. The device sees descriptors and DMA addresses. The driver sees rings and completion fields. XDP sees a bounded frame view. The network stack sees an SKB with offsets and offload state. Protocols see headers and connection state. A socket sees bytes, messages, errors, and metadata.

The governing question is how every transition preserves truthful data and ownership at line rate. Performance features deliberately defer work: checksum completion, segmentation, aggregation, batching, interrupt notification, allocation, and recycling. Correctness depends on knowing exactly which work was deferred, who owns it now, and where fallback occurs.

## Why This Matters

Network packet rates can make per-packet allocation, interrupts, cache misses, locks, and crossings dominate CPU time. Batching and offload are necessary for throughput, but they also expand the scope of a malformed descriptor, stale feature bit, or teardown race.

Overload is normal, not exceptional. Receive rings fill, NAPI budgets expire, socket queues reach limits, qdiscs drop, transmit rings stop, and devices reset. A well-designed stack degrades through bounded, attributable loss and backpressure. A poorly designed one corrupts memory or spends every CPU retrying work it cannot admit.

Packets also carry security boundaries. The earliest bytes are untrusted. Hardware parsing, XDP programs, tunnels, namespaces, filters, and protocol demultiplexing can redirect them. Metadata must never grant stronger trust than the bytes and path justify.

## Prerequisites and Retrieval

Review [OS-004](004-interrupts-and-exceptions.md), [OS-024](024-atomic-operations.md), [OS-031](031-address-translation.md), [OS-040](040-diagnosing-memory-pressure-and-thrashing.md), [OS-051](051-per-cpu-state.md), [OS-052](052-smp-kernel-synchronization.md), [OS-053](053-scalable-locking.md), [OS-054](054-kernel-read-copy-update.md), [OS-055](055-numa-memory-placement.md), [OS-058](058-timer-and-interrupt-scalability.md), [OS-062](062-memory-mapped-and-port-mapped-i-o.md), [OS-063](063-direct-memory-access.md), [OS-067](067-zero-copy-and-kernel-bypass.md), [OS-070](070-designing-an-i-o-path-for-latency-or-throughput.md), and [OS-071](071-socket-layer-architecture.md).

Retrieve these distinctions:

- device descriptor, DMA buffer, XDP buffer or frame, SKB, protocol segment, and socket message are different representations;
- descriptor availability, device completion, interrupt, NAPI scheduling, poll execution, and protocol delivery are different events;
- DMA mapping, ownership, cache synchronization, and memory ordering solve different problems;
- hardware receive queue, NAPI instance, software backlog, protocol queue, socket queue, qdisc, and transmit ring are separate queues;
- packet length, buffer capacity, headroom, tailroom, fragment length, and aggregate length need independent bounds;
- checksum calculation, checksum verification, checksum status metadata, and wire checksum fields are not synonymous;
- IP fragmentation, transport segmentation, GSO, TSO, GRO, and reassembly occur at different layers;
- XDP pass, drop, abort, transmit, redirect, and AF_XDP delivery transfer ownership differently;
- driver enqueue, hardware fetch, transmit completion, wire emission, and remote receipt are different completion levels;
- a drop counter, error counter, queue overflow, policy rejection, allocation failure, and malformed packet identify different failure stages.

## Learning Objectives

After this module, you should be able to:

1. trace a received frame from descriptor provisioning through DMA completion, NAPI, XDP, SKB construction, GRO, protocol lookup, and socket delivery;
2. trace transmission from socket or forwarding output through routing, qdisc, GSO and checksum validation, driver enqueue, DMA completion, and buffer release;
3. reason about descriptor rings, ownership, memory ordering, interrupt masking, NAPI budgets, queue stop and wake, and teardown;
4. preserve packet geometry, fragment, checksum, VLAN, tunnel, timestamp, hash, segmentation, and device metadata;
5. choose queue counts, RSS/RPS/RFS/XPS mappings, polling, coalescing, batching, page recycling, and offloads from workload evidence;
6. localize drops, stalls, corruption, reordering, and latency across hardware and software queues;
7. validate fast paths with malformed descriptors, feature changes, allocation pressure, races, resets, traffic mixes, and scoped measurement.

## Core Exposition

### Packet paths are ownership pipelines

Treat packet processing as a sequence of ownership transfers, not a list of function calls. At any point one agent may mutate a buffer, while other agents may hold read-only references or metadata.

Write the owner in the design: page pool, receive ring, device, driver poll, XDP target, SKB, protocol queue, socket, qdisc, transmit ring, or userspace. Every failure path returns or transfers ownership once.

### Network-device queues

A multiqueue device exposes receive and transmit queues backed by descriptor rings. Each queue can have its own interrupt vector, NAPI context, locks or single-consumer assumptions, statistics, and CPU affinity.

The number of queues is a topology choice. Too few serialize processing; too many increase interrupts, memory, cache footprint, and imbalance. Measure the smallest count that meets per-CPU and per-queue capacity.

### Receive-buffer provisioning

Before reception, the driver allocates or recycles storage, maps it for DMA if necessary, writes descriptor address and capacity, and publishes the descriptor before updating the device tail or ownership bit.

Do not expose memory outside the mapped range. Record enough state to unmap or recycle the exact allocation after completion, error, reset, or partial setup failure.

### Descriptor publication

Initialize every descriptor field, then apply the DMA and memory ordering required by the architecture before notifying the device. Device ownership begins only at that publication boundary.

A doorbell is notification, not a substitute for descriptor visibility. Ring wrap, generation bits, and producer-consumer arithmetic must not overwrite a live entry.

### Device reception

The NIC receives a frame, applies physical and link checks, can classify it, selects a queue, writes bytes by DMA, and posts completion length, status, hash, VLAN, checksum, timestamp, or other metadata.

Hardware metadata is input. Validate status and advertised feature context before converting it into kernel trust or offload state.

### Interrupts and moderation

Without moderation, a device can interrupt for each packet. Coalescing uses event counts or time to reduce interrupts and increase batch size.

Moderation adds dwell and can create bursts. Tune receive and transmit behavior under representative load, including low-rate latency, not only peak packets per second.

### NAPI scheduling

The interrupt handler acknowledges or masks the queue event and schedules its NAPI instance. Successful scheduling transfers poll ownership under NAPI's state protocol.

Do minimal interrupt work. Repeated interrupts while the poller already owns the queue waste CPU and can race with mask or unmask operations.

### Poll budgets

The NAPI poll method reclaims transmit completions and processes received packets. Receive processing is bounded by the supplied budget; transmit completion cleanup is not counted against that receive budget.

If receive work reaches the budget, return the budget and remain scheduled. If the ring is drained before budget, use the completion-and-unmask sequence required by the driver.

### The empty-ring race

The poller may see no completion just before the device posts one. If it completes polling and unmasks incorrectly, the new event can be left without either a poll owner or a future interrupt.

Drivers use device-defined acknowledgement, mask, final-check, and rearm ordering. Prove that every interleaving leaves either scheduled polling or enabled notification.

### Softirq and threaded processing

NAPI commonly runs in software-interrupt context, but threaded modes and busy polling exist. Context determines which operations can sleep, which per-CPU assumptions hold, and how work competes with applications.

Bound per-invocation work so one busy queue cannot monopolize a CPU. Backlog processing and rescheduling extend work without violating fairness.

### Receive descriptor validation

Reject completion errors, impossible lengths, invalid fragments, missing end-of-packet markers, unsupported metadata, and inconsistent generation before parsing packet headers.

When a multi-buffer packet fails, release every owned fragment exactly once. Never let one corrupt length move header access past DMA capacity.

### DMA synchronization

On noncoherent paths, transition a completed receive range from device to CPU before reading it. Before recycling to the device, transition the correct range back.

Mapping lifetime and cache synchronization are separate. Persistent mappings can avoid repeated map operations but still require ownership synchronization.

### Page-pool allocation and recycling

Page pools cache DMA-suitable pages or fragments for receive queues. Recycling avoids allocator and mapping work and can preserve queue-locality.

The pool tracks in-flight pages. An SKB or XDP target can outlive the poll cycle, so pool destruction waits until all pages return or detach safely. NUMA mismatch and extra references can force slower release.

### Packet geometry

An SKB carries metadata while data can occupy a linear head, page fragments, and fragment lists. Headroom permits adding headers; tailroom permits trailers or expansion.

Maintain validated MAC, network, transport, inner, and data offsets whenever headers are pushed, pulled, cloned, segmented, encapsulated, or decapsulated.

### XDP execution

XDP runs early over a bounded receive buffer. The program can pass the packet to the normal stack, drop it, transmit it, redirect it, or signal an abort under supported actions.

The verifier constrains program safety, but driver and program must honor headroom, metadata, fragment, device, queue, map, and action contracts.

### XDP pass

On pass, convert or build the normal packet representation without losing length, offset, checksum, hash, VLAN, timestamp, or page-pool recycling information.

Conversion changes ownership. A driver must not recycle the buffer after the SKB has taken responsibility.

### XDP drop and abort

Drop releases the frame under the receive allocator's rules. Abort also reports an exceptional program result for diagnosis before release.

Count policy drops separately from malformed descriptors, allocation failures, and ring overflow. Sampling must be rate-limited under attack.

### XDP transmit

XDP transmit returns a frame through a supported device path, often the ingress device. It changes direction and DMA synchronization requirements.

Completion still determines when the backing frame can be recycled. A successful action result does not mean the frame reached the wire.

### XDP redirect

Redirect transfers the frame to another device, CPU map, devmap, or AF_XDP socket according to map and target validation. Batched redirects require an explicit flush before the poll cycle ends.

Source and destination ownership must agree on completion. A missing map entry or queue mismatch produces a defined drop, not fallback to an arbitrary consumer.

### AF_XDP rings

AF_XDP connects XDP to userspace through RX and TX rings plus UMEM fill and completion rings. Ring roles define who produces descriptors and who owns frames.

A completion entry returns ownership to userspace but does not guarantee successful wire transmission. Starving the fill ring can stop receive progress and require the documented wakeup path.

### SKB allocation and construction

If the packet enters the stack, construct an SKB around the buffer or copy data into appropriate storage. Initialize protocol, device, hash, queue, timestamp, checksum, VLAN, encapsulation, and recycling metadata.

Clear fields not supplied by the device. Reused metadata that retains a stale trust bit can be worse than missing offload.

### Receive checksum state

Checksum metadata distinguishes not computed, verified for known headers, complete checksum contribution, and partial checksum still requiring work. Encapsulation can introduce several checksum layers.

The driver reports only what hardware actually verified. Protocol code validates the remaining layers, and forwarding or modification updates the state.

### VLAN metadata

Hardware can strip a VLAN header and report its tag separately. The SKB must retain equivalent semantics so policy, bridge, namespace, and protocol processing see the correct logical packet.

Do not confuse stripped-on-receive metadata with an on-wire header still present in bytes. Reinsertion or transmit offload depends on the representation.

### Receive hash and flow identity

RSS hardware can report a hash and type. The stack can use it for queueing, CPU steering, socket selection, or diagnostics.

A hash is not unique identity or authorization. Record which header fields and key produced it where that matters, and handle fragments or tunnels that lack the expected tuple.

### GRO

Generic Receive Offload combines compatible packets into a larger internal representation so later layers process fewer objects. It preserves enough segmentation metadata to recover protocol semantics.

Aggregate only compatible flow, header, checksum, encapsulation, sequence, option, policy, and device state. Flush on incompatibility, timeout, budget boundary where required, or control conditions.

### GRO trade-offs

GRO improves throughput and cache efficiency. It can add dwell, create larger bursts, change observation points, and hide original packet boundaries from some instrumentation.

Measure both aggregate and wire-packet counts. Disable or constrain aggregation for experiments only when the resulting workload claim is explicit.

### Protocol receive dispatch

After link processing, the stack selects network protocol, applies ingress policy, routing or local-delivery decisions, and dispatches to transport or forwarding.

Each parser checks minimum header, declared length, options, fragments, checksum, and namespace. Never trust a later header offset solely because hardware recognized an earlier layer.

### Socket delivery

Local transport lookup selects a socket inside the network namespace, validates state and policy, and queues bytes, messages, or errors subject to memory and flow-control limits.

Socket wakeup follows queue publication. A packet consumed by the protocol can still be dropped before application delivery because of state, memory, filter, or checksum failure.

### Receive drops

Drops can occur at device FIFO, descriptor exhaustion, driver validation, XDP, allocation, software backlog, protocol parse, routing, firewall, socket lookup, socket memory, or application policy.

No single counter covers every stage. Reconcile adjacent counters and traces while accounting for sampling, aggregation, per-CPU updates, resets, and offloaded paths.

### Receive-side scaling

RSS hashes flows into hardware receive queues, commonly with separate interrupts. RPS can enqueue processing to another CPU; RFS tries to steer toward the consuming application.

Steering improves parallelism only when queue, interrupt, protocol, and application topology align. Cross-CPU enqueue and cache movement can outweigh benefit.

### Receive ordering

Packets within one transport flow often need consistent processing order. Hash configuration, indirection updates, queue migration, RPS backlog, GRO, and failover can reorder arrivals.

Protocols tolerate only their defined reordering. Reconfigure queues with a transition that accounts for in-flight packets rather than changing maps as if queues were empty.

### Forwarding

A forwarded packet traverses receive validation, routing and policy, header modification, neighbor resolution, qdisc, and transmit. It can retain or lose offload eligibility as headers change.

Recompute or update checksums, TTL or hop limit, MTU decisions, and metadata. Namespace and device transitions must be explicit.

### Transmit entry

Locally generated output begins with socket and protocol state; forwarded output begins with a received packet. Both converge on route, neighbor, policy, qdisc, and network-device paths.

Define success at each caller. Queuing an SKB to a lower layer transfers ownership but rarely proves wire delivery.

### Route and neighbor state

Routing selects egress, next hop, source, MTU, and features. Neighbor resolution can queue packets while link-layer reachability is established.

Bound unresolved queues and timeouts. A route cached before device or namespace change must be revalidated under its lifetime rules.

### Traffic control and qdiscs

A qdisc can classify, schedule, shape, pace, reorder within policy, or drop packets. Some devices and queues use minimal or noqueue-style software behavior.

Queue discipline is part of latency, fairness, and overload. Track qdisc enqueue-to-dequeue delay independently from driver-ring residence.

### Queue selection

The stack selects a transmit queue using traffic class, socket mapping, flow hash, CPU, receive-queue association, and device policy. The mapping can be cached for a flow.

Avoid switching queues while outstanding packets could reorder. XPS can align transmit completion with the CPU or receive queue that handles the flow.

### GSO

Generic Segmentation Offload represents several wire packets as one large SKB with segmentation type, size, and header offsets. Software or a capable device performs final segmentation.

Validate segment count, sizes, checksum setup, header lengths, tunnel nesting, and feature support. An oversized internal object is not a legal wire frame until segmentation succeeds.

### TSO and USO

TCP Segmentation Offload lets a device produce TCP segments; UDP Segmentation Offload produces multiple UDP datagrams. They have different header and identifier rules.

Do not confuse UDP segmentation with IP fragmentation. Tunnel offloads add inner and outer header requirements and can exceed hardware nesting support.

### Feature validation

Devices advertise offload capabilities, but the usable set also depends on protocol, packet type, encapsulation, queue, configuration, and current device state.

Immediately before driver submission, validate requested features. If unsupported, calculate checksum or segment in software, or reject safely. Never pass impossible metadata to hardware.

### Transmit checksum offload

For partial checksum offload, the SKB identifies the checksum start and destination offset. The device or software helper completes the requested checksum.

Validate that both positions lie in the correct packet and that only the supported checksum is deferred. Encapsulated packets can require inner and outer work.

### Driver transmit contract

The driver's transmit method either takes ownership under the interface contract or reports a busy/resource result without consuming the SKB. It maps fragments, builds descriptors, and publishes them before ringing the device.

A busy path must not modify ownership ambiguously. Queue stop and wake prevent repeated calls when the ring lacks capacity.

### Transmit ring capacity

Reserve descriptors based on fragments and segmentation needs before publication. One SKB can consume several descriptors.

Stop the software queue before capacity becomes unsafe, then recheck to avoid a lost wake race with completion. Wake only after sufficient space is visible.

### Byte Queue Limits

Descriptor count alone poorly represents queued service because packets and offload aggregates vary in bytes. BQL tracks bytes sent to and completed by a device queue and adapts the permitted in-flight amount.

The aim is enough bytes to keep the device busy without building a large hidden queue. It complements rather than replaces qdisc policy and socket backpressure.

### DMA mapping for transmit

Map the linear area and each fragment in the device's direction, checking every result. If a later mapping fails, unmap earlier mappings exactly once and retain or release the SKB according to the caller contract.

The mapped data is immutable to the CPU while the device owns it unless the DMA API says otherwise. Clones require shared-data lifetime to exceed all transmissions.

### Descriptor publication on transmit

Write addresses, lengths, flags, offload context, and ownership markers in the device-defined order. Apply memory barriers before the tail doorbell.

Generation and ring indices distinguish new descriptors from stale memory. Do not let cleanup observe a terminal marker before the rest of a completion is visible.

### Transmit completion

Completion means the device no longer needs the descriptor buffers under its contract. The driver unmaps, accounts bytes and packets, reports timestamps or errors, releases SKBs, and makes ring capacity available.

It may not mean the packet reached the physical wire. Distinguish DMA completion, MAC completion, hardware timestamp, and remote acknowledgement.

### Completion batching

NAPI can reclaim several transmit descriptors per poll, amortizing locks and unmaps. Reclaim even when the receive budget is zero if the API requires transmit cleanup.

Bound cleanup work by actual ring state and scheduling fairness. Delayed completion retains memory and can keep queues stopped.

### Hardware timestamps

Receive and transmit timestamping can use software, transformed hardware, or raw hardware clocks. Metadata identifies which clock and event were sampled.

Correlate timestamps with socket requests and handle clock conversion, wrap, adjustment, missing values, and delayed error-queue delivery. A transmit timestamp is not peer receipt.

### Multiqueue fairness

Separate queues reduce locks but can isolate unused capacity and let one hot flow dominate a queue. Queue mapping and qdisc structure determine whether priorities compose across hardware queues.

Measure per-queue depth, drops, bytes, interrupts, poll time, and CPU. Aggregate device totals can hide one saturated queue.

### Busy polling

Application or kernel busy polling invokes NAPI processing near a target socket or queue, reducing interrupt and scheduler latency. It consumes CPU and interacts with NAPI ownership.

Use documented APIs and budgets. Avoid two pollers simultaneously processing one queue and measure power, fairness, and idle behavior.

### Memory pressure

Receive buffers, SKBs, page pools, fragments, socket queues, retransmission, qdiscs, and driver rings consume memory. Per-CPU caches can multiply reserves.

Charge before exposure, bound every pool, and preserve emergency progress. Under pressure, recycle safely, shed at an attributable boundary, and avoid retry loops that spend more memory.

### Device reset and removal

Stop new transmit, detach receive publication, disable and synchronize NAPI, mask and synchronize interrupts, stop DMA, resolve outstanding descriptors, and only then free rings and pools.

Reset distinguishes completions from the old generation. Surprise removal can make MMIO unsafe; bus and driver recovery rules define which accesses remain valid.

### Observability

Record device and queue identity, descriptor occupancy, refill failures, NAPI polls and budget exhaustion, interrupt counts and moderation, XDP actions, page-pool recycling, SKB allocation, GRO/GSO sizes, checksum fallback, qdisc delay, BQL, queue stops, completions, drops, timestamps, CPU, NUMA, and protocol delivery.

Use stable trace correlation where possible. Instrumentation itself changes cache, branches, timing, and aggregation, so report observer configuration and overhead.

### Testing

Test zero, minimum, maximum, malformed, fragmented, tunneled, VLAN-tagged, checksum-bad, checksum-offloaded, multi-buffer, and GSO packets. Exercise ring wrap, budget boundaries, empty-ring races, allocation failure, redirect failure, qdisc drops, queue stop/wake, map failure, late completion, reset, and removal.

Compare packet captures at appropriate points, protocol checks, reference and DMA diagnostics, counters, and end-to-end payload oracles. Hardware offload tests require real capable hardware; software fallback tests prove a different path.

## Definitions and Notation

Let:

- $R_x$ and $R_t$ be receive and transmit descriptor rings;
- $p_r,c_r$ be receive producer and consumer indices;
- $p_t,c_t$ be transmit producer and consumer indices;
- $K_r,K_t$ be safe ring capacities;
- $B$ be the NAPI receive budget;
- $w_r$ be receive packets processed in one poll;
- $w_t$ be transmit completions reclaimed in one poll;
- $O(x)$ be the unique mutable owner of buffer $x$;
- $D(x)$ be its DMA mapping and synchronization state;
- $L(x)$ be validated packet length;
- $C(x)$ be checksum state;
- $G(x)$ be segmentation or aggregation state;
- $F(d,x)$ mean device $d$ supports every feature requested by packet $x$;
- $Q_j$ be occupancy of queue $j$ and $K_j$ its capacity.

Ring safety requires

$$
0\le (p_r-c_r)\bmod M_r\le K_r,
\qquad
0\le (p_t-c_t)\bmod M_t\le K_t,
$$

with the device's generation convention resolving wrap ambiguity.

NAPI receive fairness requires

$$
0\le w_r\le B,
$$

while $w_t$ is accounted separately. Completion of polling is permitted only after $w_r<B$ and the driver's drained-event condition holds.

Unique mutable ownership requires

$$
\forall x,t:\ |O(x,t)|=1,
$$

although immutable references may coexist under explicit reference rules.

Safe transmit requires

$$
F(d,x)=true
$$

after feature validation and any required software checksum or segmentation fallback.

Every queue remains bounded:

$$
0\le Q_j\le K_j,
$$

with a defined stop, drop, backpressure, or retry action at capacity.

These relations are subsystem reasoning tools, not a formal specification of Linux, a NIC, DMA architecture, or protocol.

## Mechanisms, Invariants, or Proof Structure

### Obligation 1: publish valid DMA resources

Every descriptor names a mapped in-range buffer, initialized metadata, live generation, and correct ownership before device notification.

Counterexample: the tail doorbell advances before the final address word is visible, so the NIC DMA-writes an old page.

### Obligation 2: validate completions before bytes

The driver acquires completion state, checks generation, error, length, fragment structure, and capabilities, then synchronizes DMA before CPU parsing.

Counterexample: an impossible received length becomes an unchecked transport-header pointer beyond the allocation.

### Obligation 3: close the interrupt-poll race

Mask, schedule, drain, completion, final check, and rearm leave each event owned by a poller or guaranteed to notify.

Counterexample: a packet arrives between the empty check and interrupt enable and neither condition schedules work.

### Obligation 4: honor the receive budget

One poll processes at most $B$ receive packets and reports budget exhaustion truthfully. Transmit reclamation proceeds without stealing the receive count.

Counterexample: a driver reports less than budget after stopping only because its local batch filled, so NAPI completes while descriptors remain.

### Obligation 5: transfer XDP ownership once

Pass, drop, transmit, redirect, and abort each have one terminal owner transition, including multi-buffer and batched redirect cleanup.

Counterexample: a redirected frame is both queued to another device and returned to the source page pool.

### Obligation 6: preserve packet metadata truth

Offsets, length, fragments, checksum, VLAN, tunnel, hash, timestamp, aggregation, security, and namespace metadata always describe the current bytes.

Counterexample: decapsulation moves headers but leaves checksum level claiming hardware verified the now-exposed transport.

### Obligation 7: aggregate and segment compatibly

GRO combines only equivalent state; GSO produces legal output segments under final path features and MTU.

Counterexample: two packets with different policy marks aggregate, causing one to bypass its required decision.

### Obligation 8: bound every queue

Receive descriptors, software backlog, redirect batches, protocol queues, sockets, qdiscs, transmit rings, and completion work have capacity and overflow behavior.

Counterexample: a stopped transmit ring causes unlimited SKBs to accumulate in an uncharged retry list.

### Obligation 9: preserve flow ordering

Queue selection and reconfiguration do not move a flow across concurrently draining queues unless the protocol permits resulting reorder.

Counterexample: XPS mapping changes while prior packets remain in the old qdisc, reversing wire order.

### Obligation 10: release transmit ownership on evidence

DMA mappings, fragments, pages, SKBs, timestamps, and accounting remain live until a validated completion or contained reset ends device access.

Counterexample: driver enqueue success frees a cloned payload while hardware still reads it.

### Obligation 11: teardown from the outside inward

Stop publication, detach entry, quiesce NAPI and interrupts, stop DMA, drain or invalidate generations, then release rings, pools, programs, and device state.

Counterexample: page-pool destruction races an SKB freed later from a socket queue.

### Obligation 12: scope evidence by path

Tests identify hardware, firmware, driver, queues, offloads, XDP, qdisc, namespace, topology, workload, observer, faults, and capture point.

Counterexample: software-loopback checksum success is presented as evidence for a NIC's tunneled checksum offload.

## Alternatives and Trade-Offs

- **Interrupt per event versus moderation:** immediate notification reduces dwell; moderation amortizes interrupts and builds batches.
- **Interrupts versus busy polling:** interrupts save idle CPU; polling can reduce wakeup latency while consuming cores and power.
- **One queue versus multiqueue:** one queue simplifies ordering; multiqueue adds parallelism with affinity and reconfiguration complexity.
- **RSS versus RPS/RFS:** hardware steering avoids cross-CPU enqueue; software steering can follow applications when hardware queues are limited.
- **Fresh allocation versus page-pool recycling:** allocation is flexible; recycling amortizes DMA and allocator cost but extends pool lifetimes.
- **Full pages versus fragments:** full pages simplify ownership; fragments reduce memory use while adding shared-page accounting and cache-line traffic.
- **XDP versus full-stack processing:** XDP handles early policy cheaply; the stack supplies protocols, sockets, routing, and richer context.
- **Copy versus redirect:** copying isolates ownership; redirect saves movement but couples buffer compatibility and completion.
- **GRO enabled versus disabled:** GRO improves throughput; disabling preserves closer-to-wire packet visibility and may reduce dwell.
- **Hardware versus software segmentation:** hardware saves CPU; software fallback improves portability and handles unsupported packet forms.
- **Checksum offload versus software checksum:** offload saves CPU; software provides a correctness fallback and simpler diagnosis.
- **Deep versus shallow transmit queues:** deep queues absorb bursts; shallow queues reduce latency and hidden failure scope.
- **FIFO versus managed qdisc:** FIFO minimizes policy work; scheduling and shaping preserve fairness and rate behavior.
- **CPU-based versus receive-queue-based XPS:** CPU maps suit pinned workloads; receive-queue maps can keep bidirectional flow processing together.
- **Linear SKB versus fragments:** linear data simplifies parsing; fragments avoid copies but complicate access and device limits.
- **Detailed tracing versus minimal hot path:** rich evidence localizes drops; instrumentation changes timing and cache behavior.

## Failure Modes and Misconceptions

- **“The interrupt receives the packet.”** It normally schedules or signals later bounded processing.
- **“One interrupt means one packet.”** moderation and batching break that relationship.
- **“NAPI is only polling.”** it is an event ownership and processing mechanism with interrupt, polling, and threaded modes.
- **“Transmit cleanup consumes the receive budget.”** NAPI's receive budget bounds receive packets, not TX reclamation count.
- **“Seeing an empty ring means it is safe to unmask.”** the device can post concurrently; use the defined race protocol.
- **“DMA mapping means the CPU can read now.”** ownership and synchronization still govern access.
- **“The device-reported length is trustworthy.”** validate it against descriptor capacity and frame structure.
- **“Checksum offload is a Boolean.”** states and verified layers carry precise meanings.
- **“Checksum verified means packet authorized.”** integrity arithmetic is not policy or authenticity.
- **“XDP pass leaves ownership with the driver.”** ownership moves into the normal network representation.
- **“XDP redirect is complete immediately.”** batched flush and destination completion still matter.
- **“AF_XDP completion proves wire transmission.”** it returns frame ownership under the ring contract.
- **“An SKB always contains linear packet bytes.”** payload can occupy fragments and fragment lists.
- **“GRO is IP reassembly.”** aggregation and fragment reassembly are different mechanisms.
- **“GSO packets are legal wire frames.”** they require successful segmentation before emission.
- **“TSO and IP fragmentation are equivalent.”** transport segmentation and network fragmentation obey different rules.
- **“Advertised device features apply to every packet.”** encapsulation and configuration can require fallback.
- **“Driver enqueue means the packet was sent.”** it commonly transfers ownership for later device work.
- **“A TX completion proves peer receipt.”** it marks a local device boundary.
- **“Descriptor count measures queued delay.”** byte volume and service rate also matter.
- **“More RSS queues always improve throughput.”** CPU, cache, IRQ, flow skew, and application topology can dominate.
- **“One drop counter explains loss.”** loss can occur at many queues and policy points.
- **“Large socket buffers prevent receive loss.”** they can move and enlarge queues without fixing consumers.
- **“Reset can free rings after interrupts are masked.”** NAPI, DMA, callbacks, and outstanding owners also require containment.
- **“Loopback validates hardware offloads.”** it exercises a different path.

## Worked Examples

### Example 1

A receive descriptor owns a 2,048-byte mapped buffer. Hardware reports length 9,000 because of a corrupt completion. The driver rejects the completion before reading an Ethernet header, records a descriptor error, and returns the allocation through the correct recovery path.

Clamping the length to 2,048 would hide corruption and could parse a truncated hostile frame as valid. Trust begins only after consistency checks.

### Example 2

Five receive packets and two transmit completions await one NAPI instance with receive budget three. The following toy shows separate accounting and the decision to remain scheduled after budget exhaustion:

<!-- bijux-verify: {"id":"napi-receive-budget-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"poll=1 tx_reclaimed=2 rx_processed=3 rx_remaining=2 complete=False\npoll=2 tx_reclaimed=0 rx_processed=2 rx_remaining=0 complete=True\ninterrupts=rearmed\n","stderr":""}} -->
```python
rx_remaining = 5
tx_remaining = 2
budget = 3
poll_number = 0

while rx_remaining:
    poll_number += 1
    tx_reclaimed = tx_remaining
    tx_remaining = 0
    rx_processed = min(budget, rx_remaining)
    rx_remaining -= rx_processed
    complete = rx_processed < budget
    print(
        f"poll={poll_number} tx_reclaimed={tx_reclaimed} "
        f"rx_processed={rx_processed} rx_remaining={rx_remaining} "
        f"complete={complete}"
    )

print("interrupts=rearmed")
```

The model assumes the second poll's drained check is valid. It does not implement an interrupt race, driver, DMA, or NAPI API.

### Example 3

An XDP program redirects a page-pool-backed frame from device A to device B. Device B queues it for transmit. Device A's driver must not recycle the page at the end of its poll; the redirect path and destination completion own it.

If destination mapping fails, one defined error path returns the page. Counting a redirect action without its flush and completion can conceal leaked frames.

### Example 4

A NIC reports `CHECKSUM_UNNECESSARY` for an outer UDP tunnel checksum and a checksum level that covers one consecutive inner layer. After decapsulation, the stack interprets exactly those verified layers.

Treating the flag as “all checksums valid” could skip validation of the inner TCP checksum. The checksum state must travel with header transformations.

### Example 5

GRO sees two sequential TCP packets with equal flow tuple and compatible options, but their security marks differ. It flushes rather than aggregate them.

Saving one protocol traversal cannot justify merging policy-distinct packets. Compatibility includes metadata, not only bytes and sequence numbers.

### Example 6

A tunneled GSO SKB requests an offload the selected egress device lacks. Feature validation invokes software segmentation and checksum completion, producing legal MTU-sized packets.

Passing the aggregate unchanged would not be a performance degradation; it would be an invalid wire path. Fallback correctness is part of offload architecture.

### Example 7

A device transmit ring has eight free descriptors. An SKB has one linear area and nine mapped fragments. The driver refuses or linearizes before ownership transfer rather than publishing a partial packet.

If mapping fragment seven fails, it unmaps fragments zero through six in reverse ownership and leaves the SKB in the caller-defined state. No stale DMA addresses remain live.

### Example 8

A queue is stopped because descriptor space is low. A completion frees capacity concurrently. The stop path sets stopped state, then rechecks visible capacity; if capacity already returned, it schedules or performs the wake.

Without the recheck, the completion can observe the queue as running before stop while the submitter observes no later completion, leaving a permanently stopped queue.

### Example 9

An RSS indirection change moves a live flow from queue 0 to queue 1 while packets remain in both software backlogs. The transport observes reordering.

A safe rollout drains or tolerates the transition, uses flow-aware steering, and measures reorder. Equal queue counts before and after do not establish ordering.

### Example 10

Application loss rises, but the NIC's missed-packet counter is flat. Driver counters show no descriptor shortage; XDP drop counters are flat; protocol counters show checksum errors; socket drops are low.

The evidence localizes the current symptom near protocol checksum validation. The team captures affected traffic under policy, checks offload metadata and recent feature changes, and does not enlarge rings blindly.

## Cross-Program Connections

- **Computer architecture:** DMA coherence, barriers, cache lines, interrupts, NUMA, PCIe, IOMMUs, and device queues define packet ownership costs.
- **Network engineering:** Ethernet, IP, transport, VLANs, tunnels, routing, MTU, checksum, fragmentation, congestion, and reordering define packet semantics.
- **Data structures engineering:** rings, per-CPU queues, hashes, fragments, reference counts, lists, qdiscs, and recycling pools implement the path.
- **Security engineering:** hostile lengths, early filters, namespace boundaries, device trust, BPF programs, policy marks, and raw packet access define exposure.
- **Performance engineering:** batching, moderation, aggregation, offload, affinity, cache locality, drops, percentiles, and observer effect govern evidence.
- **Distributed systems:** loss, duplication, reorder, backpressure, retry, partial failure, and endpoint semantics begin below the service protocol.
- **Platform engineering:** queue inventory, IRQ placement, offload policy, BPF rollout, health monitoring, rollback, and incident counters operationalize the stack.
- **API and service engineering:** socket buffers, streaming, message framing, deadlines, load shedding, and completion meaning depend on lower packet transitions.
- **Storage engineering:** descriptor rings, DMA, completion, queue depth, batching, and reset share structural invariants with high-performance storage.
- **Formal methods:** ownership types, transition systems, bounded rings, temporal wakeup properties, and fault interleavings make fast-path claims reviewable.

## References

1. Linux Kernel Documentation, [NAPI](https://docs.kernel.org/networking/napi.html), scheduling, poll ownership, receive budgets, transmit cleanup, completion, threading, busy polling, and configuration; retrieved 2026-09-04.
2. Linux Kernel Documentation, [`struct sk_buff`](https://docs.kernel.org/networking/skbuff.html), packet geometry, fragments, cloning, checksum, and segmentation metadata; retrieved 2026-09-04.
3. Linux Kernel Documentation, [Page Pool API](https://docs.kernel.org/networking/page_pool.html), DMA-aware allocation, fragments, recycling, in-flight pages, NUMA, and statistics; retrieved 2026-09-04.
4. Linux Kernel Documentation, [Scaling in the Linux Networking Stack](https://docs.kernel.org/networking/scaling.html), RSS, RPS, RFS, XPS, queue selection, interrupt affinity, and flow ordering; retrieved 2026-09-04.
5. Linux Kernel Documentation, [Segmentation Offloads](https://docs.kernel.org/networking/segmentation-offloads.html), TSO, USO, GSO, GRO, tunnels, headers, and checksum dependencies; retrieved 2026-09-04.
6. Linux Kernel Documentation, [Checksum Offloads](https://docs.kernel.org/networking/checksum-offloads.html), receive checksum states, partial checksums, hardware capability, encapsulation, and software fallback; retrieved 2026-09-04.
7. Linux Kernel Documentation, [Network device features](https://docs.kernel.org/networking/netdev-features.html), feature advertisement, dependencies, device updates, and offload interpretation; retrieved 2026-09-04.
8. Linux Kernel Documentation, [AF_XDP](https://docs.kernel.org/networking/af_xdp.html), UMEM, fill, completion, RX and TX rings, redirection, wakeups, ownership, and multi-buffer packets; retrieved 2026-09-04.
9. Linux Kernel Documentation, [XDP RX Metadata](https://docs.kernel.org/networking/xdp-rx-metadata.html), hardware metadata, timestamps, hashes, VLAN tags, XDP pass, redirect, and AF_XDP contracts; retrieved 2026-09-04.
10. Linux Kernel Documentation, [Network Devices, the Kernel, and You](https://docs.kernel.org/networking/netdevices.html), driver registration, transmit contract, NAPI lifetime, statistics, features, and device teardown; retrieved 2026-09-04.

## Exercises

### Exercise 1

Trace one received tunneled TCP packet from an empty page-pool-backed descriptor through hardware checksum metadata, XDP pass, SKB creation, GRO, decapsulation, transport lookup, and socket delivery. State ownership and validation at every transition.

### Exercise 2

Design the interrupt and NAPI protocol for a queue. Include masking, scheduling, receive budget, transmit completion, the empty-ring race, budget exhaustion, busy polling, disable, and teardown.

### Exercise 3

Trace one large tunneled TCP transmit from a socket through GSO, checksum preparation, qdisc, queue selection, feature fallback, DMA mapping, descriptor publication, completion, timestamp, and release.

### Exercise 4

Design an overload investigation for packet loss. Reconcile device, descriptor, NAPI, XDP, backlog, protocol, qdisc, socket, and application evidence without assuming one counter is complete.

### Exercise 5

Create a validation campaign for receive and transmit fast paths. Cover malformed metadata, offloads, fragments, multi-buffer packets, queue races, memory pressure, topology changes, reset, removal, performance, and assurance limits.

## Answers to the Exercises

### Answer 1

The page pool allocates or recycles a buffer compatible with the queue's DMA mapping. The driver publishes its DMA address and capacity in a receive descriptor, then the device owns writable bytes. Hardware writes the frame and completion metadata. The driver acquires completion, verifies generation, success, length and fragment structure, synchronizes the completed range for CPU access, and only then reads headers.

XDP receives bounded data and metadata. A pass result transfers responsibility toward the stack; it does not let the driver recycle the page. SKB construction records page-pool recycling, linear and fragmented geometry, device, namespace path, hash, VLAN, timestamp, and the precise checksum layers hardware reported. Every absent field is initialized safely.

GRO first checks flow, sequence, options, checksum, encapsulation, security and policy compatibility. It either aggregates with a compatible packet or flushes separately. Tunnel processing validates outer lengths and checksum, removes or advances outer headers, updates inner offsets and checksum level, and applies routing and policy. TCP validates the inner header and any checksum not already justified, finds the established socket in the correct network namespace, checks state and sequence, and queues bytes subject to socket memory. Publication precedes wakeup. The socket or copied user buffer ultimately owns consumption; the backing page returns to its pool only after the final SKB reference releases it.

### Answer 2

The interrupt handler acknowledges the queue cause, obtains NAPI scheduling ownership, masks further queue interrupts as required, and schedules the instance. If scheduling fails because another poll owner exists, it leaves notification state consistent with that owner. The poller first reclaims all available transmit completions needed for progress, without charging them against the receive budget, then processes at most $B$ receive packets.

If it processes exactly $B$, it returns budget and remains scheduled without unmasking. If it processes fewer, it confirms the event source is drained, calls the NAPI completion mechanism with actual receive work, and rearms or unmasks in the device-defined order. A final device status check or atomic rearm protocol closes the arrival-between-empty-and-unmask race; every interleaving yields a scheduled poll or a future interrupt.

Busy polling uses the same NAPI ownership rules and bounded work rather than running concurrently on one queue. Disable prevents new schedules, waits for active polling, then allows ring changes. Teardown first detaches external traffic and stops device queue activity, disables NAPI, masks and synchronizes interrupts, stops DMA, resolves all descriptors and redirects, and only then frees rings, page pools, and NAPI state. Test with packets arriving at every boundary and with a zero receive budget used for transmit-only cleanup.

### Answer 3

The transport builds a large SKB whose outer and inner header offsets, GSO type, segment size, checksum start and checksum offset accurately describe the intended wire packets. Routing determines egress and MTU; policy and neighbor processing attach current state. The qdisc classifies, shapes or schedules it and transfers ownership on dequeue. Queue selection uses traffic class, flow mapping and XPS while preserving ordering with older packets.

Immediately before the driver, feature validation compares the exact tunneled GSO and checksum requirements with the chosen device's current features. If unsupported, software segments the SKB, updates identifiers and lengths, and completes checksums as needed. Each resulting packet must satisfy MTU and header rules. A partial checksum is left only where the final device supports it.

The driver calculates descriptor demand, checks ring capacity, maps the linear region and fragments, and unwinds all earlier mappings if any later mapping fails. It writes data and context descriptors, establishes visibility with the required barrier, advances the producer and rings the device. Ownership remains with the device path. Completion validation identifies the correct generation, unmaps every segment, updates byte and BQL accounting, wakes the stopped queue after a race-safe capacity check, delivers a requested hardware timestamp through its correlation path, and releases the final SKB reference. Completion supports buffer release; it does not claim peer receipt.

### Answer 4

Begin with an end-to-end loss definition and stable device, queue, namespace, flow and socket identities. Capture offered application messages, accepted sends, received messages, protocol sequence or request IDs, and time windows. Read per-queue hardware FIFO or missed-packet counters, descriptor no-buffer and allocation failures, interrupt and NAPI poll counts, budget exhaustion, software backlog drops, XDP action and redirect errors, page-pool empty or recycle statistics, protocol checksum and parse errors, route and firewall drops, qdisc enqueue and drop statistics, driver busy and completion state, socket drops and memory, and application queue loss.

Compare deltas across the same window, recognizing that GRO, GSO and TSO change object counts between layers. Check counter reset, per-CPU aggregation, sampling, offloaded paths, capture-point placement, and observer drops. Correlate trace samples by flow, queue, hash and timestamp. Inspect CPU saturation, IRQ affinity, NUMA, softirq backlog, cgroup pressure, ring occupancy, buffer limits and consumer delay.

Form a stage-specific hypothesis only where upstream accepted work exceeds downstream observation consistently. Reproduce with controlled rate, sizes, flows, checksum validity, offload configuration and queue topology. Do not enlarge every buffer: that can shift loss downstream and worsen latency. Preserve raw evidence and report unobserved gaps; absence from one counter is not proof a stage cannot drop.

### Answer 5

Generate minimum and maximum Ethernet frames, VLAN stacks within support, IPv4 and IPv6, legal and illegal lengths, fragments, tunnel combinations, TCP and UDP, checksum-good and checksum-bad frames, linear and fragmented SKBs, large GSO aggregates, and multi-buffer XDP frames. Fuzz completion lengths, status, generation, fragment markers, checksum levels, offsets, hash types, VLAN metadata and timestamps. Require rejection before out-of-bounds access and exactly-once buffer release.

Exercise every XDP action, missing redirect targets, redirect flush failure, AF_XDP fill starvation, invalid descriptors, wakeup transitions, and completion ownership. Test GRO compatibility boundaries and software fallback for every advertised offload that can be disabled or unsupported after route change. Compare reconstructed wire packets with a protocol oracle.

Force ring wrap, full and empty transitions, interrupt arrival at every mask and rearm boundary, NAPI budget zero and exact exhaustion, queue stop/wake races, DMA mapping failure at every fragment, page-pool extra references, allocation pressure, qdisc overflow, remote-NUMA buffers, RSS/XPS map changes with packets in flight, CPU hotplug, device reset, suspend, and surprise removal. Use sanitizers, DMA debugging, lock and reference checking, fault injection, packet capture at defined boundaries, and leak detection.

Measure throughput, packet and byte rate, end-to-end latency distributions, interrupt and poll cost, batch and GRO/GSO sizes, cache misses, CPU, memory, queue residence, drops, reorder, power, and teardown time across realistic and adversarial traffic. Record hardware, firmware, driver, kernel, offloads, queues, XDP, qdisc, topology, workload, seed, duration and instrumentation.

Software devices do not prove physical DMA or offload behavior. A packet generator can conceal its own loss. Capture hardware can drop. One NIC does not validate another's metadata, and clean steady-state traffic does not prove reset safety. Scope every conclusion to the exercised path and evidence.
