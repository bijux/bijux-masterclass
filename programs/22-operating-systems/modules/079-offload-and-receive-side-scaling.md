---
module_id: OS-079
program: Operating Systems
level: 2
module_number: 79
title: Offload and Receive-Side Scaling
status: complete
last_verified: 2026-09-04
---

# Offload and Receive-Side Scaling

## One-Page Review

### Governing question

How should an operating system delegate packet work to devices and distribute flows across queues and CPUs while preserving wire correctness, truthful metadata, per-flow ordering, ownership, bounded queues, NUMA locality, feature fallback, and coherent reconfiguration under traffic and device churn?

### Essential definitions

- **Checksum offload** delegates all or part of checksum calculation or validation while recording exactly which bytes and layers are covered.
- **GSO** represents one large software packet that will be segmented later; **TSO** and **USO** are device-assisted TCP and UDP segmentation forms.
- **GRO** combines compatible receive packets into a larger internal packet; **LRO** is a less-transparent device or driver aggregation approach with stricter forwarding concerns.
- **RSS** hashes selected packet fields in a NIC and maps the hash through an indirection table to a receive queue.
- **RPS** selects a CPU for receive protocol processing in software; **RFS** additionally steers toward the CPU consuming the flow.
- **XPS** selects a transmit queue using CPU or receive-queue relationships.
- **NAPI** executes bounded polling for receive work and transmit completions after notification.
- A **flow-ordering domain** is the packet set that must remain consistently sequenced for protocol or application behavior.
- A **feature set** is the capability intersection valid for the final device path, packet layout, encapsulation, checksum state, and policy.
- An **indirection generation** identifies one coherent mapping from hash buckets to queues and their CPU, interrupt, NAPI, and memory-placement relationships.

### Central model, mechanism, or theorem

Represent an offloaded and steered packet as

$$
P=(B,H,C,G,F,Q,I,N,X,O,R),
$$

where $B$ is byte and fragment layout, $H$ validated header geometry, $C$ checksum coverage, $G$ segmentation or aggregation state, $F$ final-path features, $Q$ hardware and software queues, $I$ hash and indirection generation, $N$ CPU and NUMA placement, $X$ execution stage, $O$ ownership and DMA state, and $R$ references and recycling.

An optimization is transparent only when later consumers see bytes equivalent to correct non-offloaded processing at their defined observation point. Scaling is correct only when every packet maps through a live queue graph and required ordering domains do not move across concurrently backlogged queues without a drain or reorder-tolerant transition.

### Critical invariants

- Offload state identifies exact layer, start, offset, coverage, encapsulation depth, segment size, header length and final device capability.
- Byte mutation, pull, encapsulation, decapsulation, route change or device change updates or invalidates every dependent offload claim.
- Software fallback produces valid wire packets whenever the selected path cannot execute the requested feature.
- Aggregation combines only packets with compatible flow, sequence, header, checksum, policy, timestamp, mark, device and forwarding semantics.
- RSS hash inputs and indirection are defined for fragments, tunnels, unknown protocols and symmetric-flow requirements.
- A live queue has compatible ring, interrupt, NAPI, CPU, NUMA, page-pool, device and generation ownership.
- Reconfiguration does not publish packets to a queue after its poller, interrupt, pool, or device lifetime ends.
- Flow remapping either drains old work, preserves sequence with a handoff, or explicitly accepts and measures reordering.
- Queue, CPU and flow distribution are bounded and observable; scaling does not hide one hot queue behind aggregate throughput.
- Device reset, feature withdrawal and CPU hotplug activate safe software or surviving-queue fallback before old state disappears.

### Common failures

Common failures are treating checksum status as one Boolean, retaining partial-checksum offsets after encapsulation, assuming GSO size is the wire size, forwarding LRO packets as ordinary frames, merging GRO traffic across marks or tunnels, enabling advertised features without final-path validation, counting one aggregate as one packet in congestion state, selecting RSS fields that split fragments or collapse many flows, changing an indirection table without considering old backlogs, equating equal IRQ counts with equal useful work, steering to offline CPUs, recycling pages while redirected traffic retains them, and benchmarking loopback as proof of NIC behavior.

### Compact example

An eight-bucket RSS table maps `[0,1,2,3,0,1,2,3]`. Queue 2 fails. A controlled replacement changes only its two buckets, producing `[0,1,0,3,0,1,1,3]`. Flows in buckets 2 and 6 move; the other six remain stable. Correctness still requires stopping new device writes to queue 2, draining its descriptor and software backlogs, preserving or explicitly tolerating ordering during handoff, rebinding interrupts and NAPI, and retiring queue-2 memory only after references quiesce.

### Connections

[OS-024](024-atomic-operations.md), [OS-040](040-diagnosing-memory-pressure-and-thrashing.md), [OS-051](051-per-cpu-state.md), [OS-052](052-smp-kernel-synchronization.md), [OS-053](053-scalable-locking.md), [OS-054](054-kernel-read-copy-update.md), [OS-055](055-numa-memory-placement.md), [OS-058](058-timer-and-interrupt-scalability.md), [OS-063](063-direct-memory-access.md), [OS-067](067-zero-copy-and-kernel-bypass.md), and [OS-071](071-socket-layer-architecture.md) through [OS-078](078-packet-filtering.md) connect offload and scaling to DMA, buffers, sockets, packet semantics, policy, concurrency and topology.

## Governing Question

Offloads deliberately make internal representations differ from wire packets. A large SKB can stand for dozens of segments. A checksum field can be incomplete because hardware will finish it. GRO can make the protocol stack observe one aggregate where the NIC received many frames. These differences are safe only when metadata tells the truth.

Receive-side scaling deliberately makes execution location depend on packet fields. A NIC queue, interrupt vector, NAPI instance, software backlog, protocol CPU, application CPU and NUMA node form a placement graph. Increasing queue count helps only if that graph spreads the actual bottleneck without breaking ordering or multiplying overhead.

## Why This Matters

At high packet rates, checksums, segmentation, interrupt work, allocation, cache misses and cross-CPU movement can dominate. Hardware and software batching can turn an unusable CPU budget into line-rate service. Incorrect metadata, however, produces corrupted wire packets or skipped validation.

Scaling also changes latency and fairness. Too few queues serialize unrelated flows; too many create sparse interrupts, cold caches and coordination. A single elephant flow can remain hot on one queue even when aggregate traffic appears balanced. Application placement and NUMA memory can outweigh the hash distribution.

Capabilities change during route selection, tunnel processing, virtualization, device reset, feature updates and migration. Every optimization needs a correctness-preserving fallback that does not depend on the failed device function.

## Prerequisites and Retrieval

Review [OS-004](004-interrupts-and-exceptions.md), [OS-024](024-atomic-operations.md), [OS-040](040-diagnosing-memory-pressure-and-thrashing.md), [OS-051](051-per-cpu-state.md), [OS-052](052-smp-kernel-synchronization.md), [OS-053](053-scalable-locking.md), [OS-054](054-kernel-read-copy-update.md), [OS-055](055-numa-memory-placement.md), [OS-058](058-timer-and-interrupt-scalability.md), [OS-063](063-direct-memory-access.md), [OS-067](067-zero-copy-and-kernel-bypass.md), [OS-071](071-socket-layer-architecture.md), [OS-072](072-packet-reception-and-transmission.md), [OS-073](073-network-buffers.md), [OS-074](074-protocol-processing.md), [OS-075](075-routing-and-neighbor-tables.md), [OS-076](076-connection-state-management.md), [OS-077](077-congestion-control-hooks.md), and [OS-078](078-packet-filtering.md).

Retrieve these distinctions:

- packet bytes, checksum field, checksum metadata, verified checksum level and deferred checksum work are different things;
- SKB length, GSO size, segment count, descriptor count, frame length and wire packet count are different units;
- segmentation, fragmentation, aggregation, coalescing, batching and interrupt moderation happen at different layers;
- RSS hash, RSS bucket, receive queue, interrupt CPU, NAPI CPU, RPS CPU, RFS CPU and application CPU are different selections;
- hardware ring, NAPI budget, per-CPU backlog, GRO list, socket queue and application queue are separate capacity boundaries;
- flow equality for RSS, GRO, routing, filtering, connection lookup and application ordering can use different fields;
- advertised device feature, enabled feature, packet eligibility and final-path support are different claims;
- DMA mapping, device ownership, CPU synchronization, page-pool reference and recycle eligibility are different states;
- configured affinity, scheduler placement, actual execution and memory allocation location are different evidence;
- device completion, correct wire emission, receiver validation and application delivery are different outcomes.

## Learning Objectives

After this module, you should be able to:

1. trace checksum, segmentation and aggregation metadata across transmit, receive, tunnels, routing, filtering and device feature validation;
2. design software fallback that restores correct wire packets when offload is unavailable or withdrawn;
3. map flows through RSS, RPS, RFS and XPS into rings, interrupts, NAPI instances, CPUs, NUMA memory and sockets;
4. preserve flow ordering and queue lifetime during indirection, CPU, channel and device reconfiguration;
5. choose queue counts, affinities, hash fields, indirection, page pools, polling and moderation from workload evidence;
6. handle fragments, tunnels, XDP, AF_XDP, virtualization, resets, hotplug and pressure without stale ownership;
7. diagnose imbalance, corruption, reorder and latency with per-stage, per-queue, per-CPU and wire-level evidence.

## Core Exposition

### Treat offload metadata as deferred work

An offload flag is not a performance hint that downstream code may ignore. It is a contract describing work already done or required later. Record the protocol layer, header locations, checksum start and offset, segmentation type, MSS or GSO size, encapsulation, fragment structure and validation level.

Every consumer either preserves the contract, completes the work, transforms it by a proved rule, or rejects it. Clearing an offload bit without completing deferred work corrupts output; preserving it after dependent bytes move can direct hardware to the wrong location.

### Distinguish receive checksum states

Receive hardware can provide no checksum information, a complete checksum value, or evidence that one or more protocol checksums were validated. The stack interprets this only under device feature and encapsulation context. An outer validated UDP checksum does not imply an inner TCP checksum passed.

After decapsulation, update checksum level and offsets precisely. Software verifies layers that hardware did not cover. A checksum detects covered corruption; it does not authenticate source or policy.

### Complete transmit checksums at the final path

Transport output may leave a partial checksum whose pseudo-header and payload completion occurs in software or hardware. Header rewrite, NAT, encapsulation, route change, fragmentation or device selection can change the calculation.

Immediately before device enqueue, intersect requested features with packet eligibility and final device features. If partial checksum is unsupported, complete it in software. Mapping failure or reset cannot leave a partially checksummed packet reported as transmitted.

### Segment only with valid geometry

GSO metadata identifies header lengths, segment payload size, segment count and type. Validate that every resulting segment fits protocol, MTU and device limits and that header replication and sequence or identification updates are defined.

Tunnel segmentation may require inner and outer header metadata plus checksum dependencies. If the final path lacks the exact feature combination, software segmentation produces ordinary packets before enqueue. One unsupported nested case cannot be approximated as a different offload.

### Aggregate only compatible receive packets

GRO compares flow and header state, sequence continuity, checksum validity, encapsulation, marks, security state, device context and protocol-specific options. Any incompatibility flushes the current aggregate. Aggregation never repairs malformed packets.

Later consumers must understand aggregate semantics or receive deaggregated packets. Forwarding and bridging need special care with LRO because device aggregation can destroy one-to-one wire-frame assumptions.

### Count logical work, not containers

Congestion control, qdisc accounting, policers, statistics and packet capture can require bytes, logical segments or wire packets rather than SKBs. Carry segment count and size through the path. When software segments, distribute timestamps, marks, checksums and accounting correctly.

Define which counters count input frames, aggregates, output segments, descriptors or completions. Otherwise an offload toggle appears to change traffic volume.

### Build the receive queue graph

For each hardware receive queue, inventory its ring, interrupt vector, NAPI instance, driver poll, page pool, RSS buckets, CPU affinity, NUMA node, RPS map, backlog, XDP path and application destinations. This graph reveals hidden cross-CPU movement.

Queue count should reflect device capability, CPU budget, flow parallelism and application layout. More queues than active flows cannot split one ordered flow and can add interrupts and cold state.

### Understand RSS selection

RSS computes a configured hash over selected packet fields, then indexes an indirection table to choose a hardware queue. The hash key, fields and tunnel interpretation affect distribution and security. Symmetric hashing can place both directions together but may reduce entropy or enable crafted collisions.

Fragments may not expose transport ports. The device needs a consistent fallback so fragments of one datagram do not scatter unexpectedly. Unknown protocols and encrypted headers likewise require documented behavior.

### Design indirection for stability

An indirection table separates many hash buckets from a smaller queue set. It enables weighted distribution and limited remapping. Update it as one generation, not bucket by bucket from the packet path's perspective.

When a queue fails or CPU changes, first prevent unsafe new ownership, publish the new mapping under the device contract, then drain or hand off old ring and software work. Packets already classified under the old generation can coexist; ordering policy must account for that interval.

### Add RPS only where it pays

RPS hashes packets in software and enqueues them to a selected CPU's backlog for protocol processing. It helps when hardware queues are few or software understands additional flows, but it adds a remote enqueue, inter-processor wakeup and another bounded queue.

Do not use RPS merely to make CPU graphs look even. Measure device-poll CPU, protocol CPU, cache locality, IPIs, backlog drops and application locality. Keep control traffic and low-rate queues from starvation.

### Use RFS to follow consumption carefully

RFS learns where an application consumes a flow and steers protocol work toward that CPU. Accelerated RFS can program compatible hardware steering. This can improve cache locality when application placement is stable.

Scheduler migration makes the learned location stale. Apply hysteresis and ordering-aware handoff so a flow does not bounce between CPUs while packets remain queued. Bound flow-table state and expire it safely.

### Select transmit queues with XPS

XPS maps transmitting CPUs or receive queues to hardware transmit queues. CPU-based selection improves lock and cache locality; receive-queue-based selection can keep request and response handling aligned. Route, traffic class, qdisc and device mapping still constrain the final choice.

Preserve per-flow ordering across queue changes or explicitly use a reorder-tolerant protocol. Queue stop and wake must coordinate with completion so capacity cannot be stranded.

### Align interrupts, polling and applications

RSS directs device work to a queue, interrupt affinity selects notification CPU, NAPI may run there or in a threaded mode, RPS may move protocol work, and the scheduler places the application. Optimize the entire chain rather than one affinity mask.

Interrupt moderation and NAPI weight trade notification overhead against latency and fairness. Busy polling can reduce wake latency by spending CPU. Record these settings with measurements; “low latency mode” is not a proof.

### Place memory near the work

Receive pages, rings, SKBs, page pools, queue state and socket buffers touch different CPUs. Allocate queue-owned memory on the intended NUMA node where possible. A remote application may justify steering work or accepting one cross-node transfer.

Page recycling preserves DMA mapping and allocation cost but can preserve old NUMA placement. Reconfiguration must decide whether to drain and rebuild pools or accept remote memory temporarily.

### Integrate XDP and AF_XDP ownership

XDP executes before ordinary SKB protocol processing and can pass, drop, transmit or redirect. Each action transfers or releases the receive buffer once. Metadata exposed by the device has a driver-specific capability contract and cannot be assumed universal.

AF_XDP maps queue traffic to userspace rings and UMEM. Fill, receive, transmit and completion rings transfer ownership explicitly. Queue remapping, program replacement and socket teardown must drain frames before pool or UMEM reuse.

### Reconfigure as a state machine

Changing channel count, RSS table, feature bits, ring size, IRQ affinity or XDP program affects coupled objects. Validate the complete target graph, allocate new resources, quiesce the affected ownership domain, publish new generation, drain old work, then release.

If programming hardware partially fails, roll back or establish one coherent safe software path. Do not report new settings merely because a control-plane request returned before the device applied them.

### Survive feature withdrawal and reset

A device can reset, detach, lose firmware state or withdraw a feature. Stop new enqueue, reclaim or fail outstanding descriptors under the driver contract, disable dependent offload metadata, segment and checksum future packets in software, and remap queues before traffic resumes.

Cached routes and sockets can retain old feature expectations. Final-path validation, not cache age, decides eligibility. Late completions carry a generation and cannot touch rebuilt rings or pools.

### Bound every queue and table

Hardware rings, NAPI work, RPS backlogs, GRO lists, flow tables, AF_XDP rings and sockets have object, byte and time bounds. Admission happens before ownership transfer. Drop or backpressure is attributed to the exact queue.

Under pressure, preserve completion, page return, link control, routing and recovery capacity. An optimization that blocks reclamation when its table is full is not safe.

### Observe distribution and correctness together

Collect per-queue packets, bytes, drops, descriptors, interrupts, polls, budget exhaustion, GRO merges and flushes, checksum states, software segmentation, feature fallback, RPS enqueues, IPIs, backlog depth, XDP actions, page recycling and NUMA locality.

Join with per-CPU softirq time, application CPU, flow distribution, reorder, latency, retransmission and wire capture. Equal packet counts can hide unequal bytes or protocol cost. A clean checksum counter cannot prove the wire checksum without an appropriate observation point.

### Test transitions and physical paths

Exercise each feature alone and in supported combinations across plain, VLAN, tunnel, fragment, NAT, bridge, forward and local paths. Compare offload enabled and disabled bytes at a receiver or wire observer. Inject unsupported device selection, mapping failure and reset.

Change RSS buckets, CPU affinity, channel count and application placement under traffic. Offline CPUs and remove queues with old backlogs. Assert bounded reorder, no stale DMA, no double recycle, correct fallback and eventual retirement.

## Definitions and Notation

Let a large packet have logical payload $L$, per-segment payload $m>0$, and header size $h$. Its logical segment count is

$$
n=\left\lceil\frac{L}{m}\right\rceil,
$$

while its SKB count can remain one. Each resulting segment must satisfy its protocol and output MTU bound.

Let RSS hash $q=\mathcal{H}_K(x)$ use key $K$ over defined fields $x$, with indirection table $I$ of size $b$:

$$
\operatorname{queue}(x)=I[q\bmod b].
$$

The table value must name a live eligible queue in the same generation.

For queue $j$, let packet rate $p_j$, byte rate $v_j$, CPU time $c_j$ and drop rate $d_j$. Balance is multidimensional; equal $p_j$ does not imply equal $v_j$ or $c_j$.

Let a flow's packets occupy old backlog $Q_o$ and new backlog $Q_n$ during remap. Strict order requires a handoff relation proving all earlier packets in $Q_o$ complete before later packets in $Q_n$, or a single ordered merge.

Let feature eligibility be intersection

$$
F_{use}=F_{device}\cap F_{route}\cap F_{packet}\cap F_{protocol}\cap F_{policy}.
$$

Requested features outside $F_{use}$ require correct software completion or rejection.

## Mechanisms, Invariants, or Proof Structure

Review offload and scaling with these obligations.

1. **Geometry obligation:** header offsets, lengths, fragments, encapsulation and segment size describe current bytes exactly.
2. **Checksum obligation:** validation and deferred work identify precise layer and coverage and survive transformations correctly.
3. **Feature obligation:** final-path capability intersects device, route, packet, protocol and policy before enqueue.
4. **Fallback obligation:** software checksum, segmentation or ordinary receive processing produces correct semantics when optimization is absent.
5. **Aggregation obligation:** only fully compatible packets merge, and every later consumer understands or reverses the aggregate.
6. **Hash obligation:** fields, key, fragment and tunnel behavior define stable intended flow domains with bounded collision risk.
7. **Queue-graph obligation:** ring, interrupt, NAPI, CPU, NUMA, pool, device and generation are compatible and live.
8. **Ordering obligation:** remapping drains, hands off or explicitly tolerates old/new backlog interleaving.
9. **Ownership obligation:** DMA, XDP, AF_XDP, SKB, redirect and page-pool references transfer and recycle once.
10. **Capacity obligation:** rings, backlogs, aggregation lists, flow tables and userspace queues are precharged and bounded.
11. **Reconfiguration obligation:** target graph validates and publishes coherently; partial hardware failure restores one safe path.
12. **Evidence obligation:** per-feature, queue, CPU, NUMA, flow and wire observations identify both performance and correctness.

The equivalence argument uses a reference path. For every eligible offloaded packet, completing deferred checksum and segmentation must yield the bytes the software reference would emit. For every aggregate, splitting at its semantic boundary must yield the validated receive packets. Scaling adds a placement proof: mapping changes execution location but not packet semantics, ownership, or required order.

This is not a proof for arbitrary hardware. Evidence must cover exact driver, firmware, device features, tunnel combinations, DMA model, topology, queue configuration and observation points.

## Alternatives and Trade-Offs

- **Software checksum versus hardware completion:** software is directly inspectable and costs CPU; hardware saves cycles with metadata dependency.
- **Software segmentation versus TSO/USO:** software creates ordinary packets early; device segmentation saves CPU and delays wire visibility.
- **No aggregation versus GRO/LRO:** ordinary packets simplify semantics; aggregation reduces protocol overhead and expands compatibility rules.
- **Few queues versus many queues:** few preserve warm state; many add parallelism, interrupts and memory.
- **Hardware RSS versus RPS:** hardware spreads before CPU processing; software steering understands more context and adds remote enqueue.
- **RPS versus RFS:** RPS balances configured CPUs; RFS follows consumers and can chase migrations.
- **CPU-based versus receive-queue-based XPS:** CPU mapping favors local locks; receive mapping can preserve bidirectional locality.
- **Symmetric versus directional hashing:** symmetry co-locates directions; directional hashes can distribute more evenly and separate work.
- **Modulo versus indirection:** direct modulo is simple; indirection enables weights and limited remapping.
- **Immediate remap versus drain:** immediate failover restores capacity; drain better preserves ordering and delays change.
- **Local NUMA allocation versus pooled reuse:** locality reduces remote access; reuse avoids allocation and can retain old placement.
- **Interrupt-driven versus busy polling:** interrupts save idle CPU; polling lowers some wake latencies at constant cost.
- **Static moderation versus adaptive moderation:** static settings are predictable; adaptation follows load and complicates latency attribution.
- **Kernel SKB path versus AF_XDP:** kernel path provides protocol integration; userspace queues reduce crossings and transfer more responsibility.
- **Automatic feature enablement versus explicit allowlist:** automation uses capability broadly; allowlists constrain poorly tested combinations.
- **Aggregate counters versus per-queue telemetry:** aggregates cost less; per-queue evidence finds hot spots and failures.

## Failure Modes and Misconceptions

- “Checksum offload means the checksum field is valid now.” It can describe work deferred to hardware.
- “A verified outer checksum verifies inner transport.” Coverage and checksum level are specific.
- “Clearing the partial flag completes the checksum.” Deferred arithmetic must actually occur.
- “GSO size is packet size.” It is typically the logical segment payload target.
- “One SKB is one wire packet.” Aggregates can represent many segments.
- “GRO merges anything in one flow.” Header, sequence, checksum and metadata compatibility also matter.
- “LRO is always safe to forward.” It can violate forwarding assumptions unless explicitly handled.
- “Advertised hardware support guarantees packet eligibility.” Encapsulation and final path can exclude it.
- “RSS uses the full packet.” It hashes selected parsed fields under device rules.
- “Fragments always hash like complete flows.” Later fragments may lack ports.
- “More queues always increase throughput.” Flow count, CPU, cache and device limits can dominate.
- “Balanced interrupts mean balanced networking.” Protocol and application work can still concentrate.
- “RPS is free parallelism.” It adds queues, IPIs and cache movement.
- “RFS always improves locality.” Application migration can make steering oscillate.
- “Flow remap only changes performance.” Concurrent old and new queues can reorder.
- “IRQ affinity pins all network work.” NAPI, RPS, kthreads and applications can execute elsewhere.
- “Configured NUMA node equals allocation locality.” Pool history and fallback allocation can differ.
- “XDP redirect returns the page to the source driver.” The destination path owns it until completion.
- “AF_XDP completion means peer receipt.” It resolves local transmit-buffer ownership.
- “Page-pool return is safe after driver processing.” Clones or redirects can retain references.
- “Disabling a feature fixes packets already queued.” Old metadata and descriptors need transition handling.
- “Device reset ends every DMA reference.” Completion and teardown must establish ownership explicitly.
- “Loopback validates NIC offload.” It omits the physical device and its firmware.
- “A host capture shows exact wire segmentation.” Capture point can precede offload completion.
- “Aggregate throughput proves correct scaling.” It can hide hot queues, reorder, drops and remote memory.

## Worked Examples

### Example 1

A tunneled TCP GSO packet requests inner TCP checksum and outer UDP tunnel checksum offload. The selected device supports plain TSO but not this tunnel combination. Final validation performs software segmentation and checksum completion before enqueue.

### Example 2

The following executable model reassigns only buckets owned by failed queue 2. It illustrates mapping stability, not NIC programming, flow ordering, queue drain, hashing or hardware behavior.

<!-- bijux-verify: {"id":"rss-indirection-replacement","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"old=[0, 1, 2, 3, 0, 1, 2, 3]\nnew=[0, 1, 0, 3, 0, 1, 1, 3]\nmoved=2 stable=6\nhash=2 old_queue=2 new_queue=0\nhash=6 old_queue=2 new_queue=1\nhash=7 old_queue=3 new_queue=3\n","stderr":""}} -->
```python
old = [0, 1, 2, 3, 0, 1, 2, 3]
new = [0, 1, 0, 3, 0, 1, 1, 3]
moved = sum(before != after for before, after in zip(old, new))

print(f"old={old}")
print(f"new={new}")
print(f"moved={moved} stable={len(old) - moved}")
for flow_hash in (2, 6, 7):
    bucket = flow_hash % len(old)
    print(f"hash={flow_hash} old_queue={old[bucket]} new_queue={new[bucket]}")
```

### Example 3

A NIC reports one outer checksum verified for a UDP tunnel. After decapsulation, the stack retains only the proved level and verifies inner TCP separately. Treating checksum status as “all good” would skip required work.

### Example 4

GRO receives sequential TCP packets with identical tuple but different security marks. It flushes rather than merge. Flow equality is necessary but not sufficient for aggregation.

### Example 5

Four queues receive equal packet counts, but queue 0 carries large encrypted tunnel packets and consumes twice the CPU. Packet-only balance hides byte and processing imbalance; queue CPU and protocol mix reveal it.

### Example 6

RPS moves a flow from device CPU 0 to protocol CPU 4, while its application runs on CPU 7 and memory is on NUMA node 0. Added distribution creates two remote transfers. RFS or scheduler placement may be a better intervention.

### Example 7

An application migrates every few milliseconds. Immediate RFS updates bounce its flow between two backlogs and reorder packets. Hysteresis keeps the current CPU until the old queue drains and migration remains stable.

### Example 8

A page-pool-backed XDP frame redirects to another device. The source NAPI poll cannot recycle it. Destination transmit completion releases the final reference and returns it under the pool contract.

### Example 9

CPU 3 is offlined while RSS buckets and an IRQ target its queue. Reconfiguration first removes new selection, migrates or drains NAPI and backlogs, rebinds interrupts, then releases per-CPU and queue state.

### Example 10

Wire corruption appears only with one tunnel offload. Software fallback eliminates it; captures before the NIC look valid; receiver captures show bad outer checksums. Evidence localizes the failure after host capture and before receive validation.

## Cross-Program Connections

- **Computer architecture:** DMA, caches, interrupts, NUMA, IOMMUs and device queues determine offload and placement costs.
- **Network engineering:** checksums, segmentation, tunneling, fragments, flow hashing and ordering define external semantics.
- **Data structures engineering:** rings, indirection tables, flow maps, queues, fragments, counters and pools implement scaling.
- **Performance engineering:** CPU cycles, batching, pacing, locality, queue distributions and observer points determine evidence.
- **Security engineering:** malformed metadata, crafted hash collisions, userspace rings, feature trust and device isolation define exposure.
- **Platform engineering:** channel counts, affinity, namespaces, XDP, AF_XDP, feature policy, rollout and rollback operationalize the path.
- **API and service engineering:** connection ordering, application placement, request latency and zero-copy completion shape workload behavior.
- **Distributed systems:** consistent hashing, remapping, draining, generations and partial failure recur in queue placement.
- **Formal methods:** refinement to wire packets, capability intersections, ownership transitions and ordering proofs support correctness.
- **Reliability engineering:** feature fallback, reset recovery, hotplug, queue drain and resource reserves contain failures.

## References

1. Linux Kernel Documentation, [Scaling in the Linux Networking Stack](https://docs.kernel.org/networking/scaling.html), RSS, RPS, RFS, accelerated RFS, XPS, hashes, queues and flow ordering; retrieved 2026-09-04.
2. Linux Kernel Documentation, [NAPI](https://docs.kernel.org/networking/napi.html), queue polling, budgets, completion, IRQ relationships, threading and busy polling; retrieved 2026-09-04.
3. Linux Kernel Documentation, [`struct sk_buff`](https://docs.kernel.org/networking/skbuff.html), checksum states, GSO metadata, geometry, fragments and clones; retrieved 2026-09-04.
4. Linux Kernel Documentation, [Checksum Offloads](https://docs.kernel.org/networking/checksum-offloads.html), partial checksums, device features, encapsulation and software completion; retrieved 2026-09-04.
5. Linux Kernel Documentation, [Segmentation Offloads](https://docs.kernel.org/networking/segmentation-offloads.html), TSO, USO, GSO, GRO, tunnels and header dependencies; retrieved 2026-09-04.
6. Linux Kernel Documentation, [Network Device Features](https://docs.kernel.org/networking/netdev-features.html), feature advertisement, dependencies, updates and interpretation; retrieved 2026-09-04.
7. Linux Kernel Documentation, [XDP RX Metadata](https://docs.kernel.org/networking/xdp-rx-metadata.html), receive timestamps, hashes, VLAN metadata, device capabilities and XDP paths; retrieved 2026-09-04.
8. Linux Kernel Documentation, [Page Pool API](https://docs.kernel.org/networking/page_pool.html), DMA-aware allocation, recycling, fragments, in-flight references, NUMA and statistics; retrieved 2026-09-04.
9. Linux Kernel Documentation, [AF_XDP](https://docs.kernel.org/networking/af_xdp.html), UMEM, fill, completion, receive and transmit rings, wakeups and multi-buffer packets; retrieved 2026-09-04.
10. Linux Kernel Documentation, [Ethtool Netlink Specification](https://docs.kernel.org/netlink/specs/ethtool.html), channels, rings, RSS contexts, features, coalescing and device configuration; retrieved 2026-09-04.

## Exercises

### Exercise 1

Design transmit offload validation for plain and tunneled TCP/UDP packets across route changes, NAT, device feature withdrawal and software fallback. State metadata and ownership invariants.

### Exercise 2

Design an RSS/RPS/RFS queue graph for 16 CPUs across two NUMA nodes, eight NIC queues, mixed short flows and two elephant flows. Include application placement and reconfiguration.

### Exercise 3

Specify a zero-loss, bounded-reorder transition from eight receive queues to four during live traffic, including device programming, NAPI, interrupts, backlogs, page pools and CPU hotplug.

### Exercise 4

Diagnose high throughput with poor p99 latency and intermittent reorder on a host using GRO, interrupt moderation, RSS, RPS and XPS. Define evidence and controlled experiments.

### Exercise 5

Construct a correctness and performance test plan for checksum, segmentation, aggregation, XDP, AF_XDP and page recycling across physical and virtual devices. State evidence limits.

## Answers to the Exercises

### Answer 1

Represent current network, transport, inner and outer header offsets; total and fragment lengths; checksum start, offset, level and state; GSO type, size and segment count; route generation; and requested features. Every NAT or tunnel transformation makes the header writable, updates bytes, and recomputes or invalidates dependent checksum, route, hash and segmentation metadata.

At final device selection, intersect enabled device features with route, packet layout, protocol and policy eligibility. Validate segment size, resulting MTU, maximum fragments, header replication, inner and outer checksum relationships, and device descriptor limits. If any exact combination is absent, perform software checksum and segmentation in a fallible preparation stage before ownership transfer.

On allocation or segmentation failure, keep one owner and return an attributable error; never enqueue a partial packet. On device feature withdrawal, stop new enqueue under old capability, reclaim descriptors, invalidate cached feature assumptions and use software fallback. Receiver or wire capture verifies actual segment bytes because host pre-NIC capture may show the aggregate.

### Answer 2

Place four queues and their page pools on each NUMA node, with interrupt and NAPI CPUs local to their rings. Use an RSS indirection table larger than eight queues for weighted bucket control. Hash a stable validated transport flow tuple with explicit fragment and tunnel fallback. Map ordinary flows broadly while recognizing each elephant remains one ordering domain unless application or protocol permits finer spreading.

Place short-flow application workers near the queues or use measured RFS steering with hysteresis. If RPS is needed for queue shortage or protocol CPU imbalance, target local CPUs first and bound backlogs and IPIs. Use receive-queue-based XPS for request/response locality where qdisc and device behavior support it.

Measure packets, bytes, CPU, cache misses, remote memory, softirq, IPIs, backlog, queue delay and application latency per queue and NUMA node. Rebalance buckets rather than immediately adding queues. An elephant hot spot may need application sharding, multiple protocol flows or capacity policy; RSS cannot split one ordered tuple safely by itself.

### Answer 3

Validate a target graph whose four surviving queues have rings, vectors, NAPI instances, CPU affinities, pools and capacity. Mark removed queues quiescing and program indirection so new classified packets select only survivors. Respect device ordering and readback or completion semantics before assuming the table is active.

Mask or detach old queue notifications under the driver protocol, poll all completed descriptors, flush XDP redirects and GRO state, drain RPS backlogs with ordering-aware handoff, and reclaim transmit completions. Packets already in old and new software queues require a sequence-preserving merge or a documented bounded reorder window.

Remove NAPI and interrupt bindings only after no producer can schedule them. Page pools wait for redirected, cloned and AF_XDP references; destroy only after in-flight reaches zero. CPU hotplug migrates timers and per-CPU state. Publish a generation for diagnostics, retain rollback resources until health passes, and restore the old coherent graph if hardware programming fails.

### Answer 4

Inventory ring depth, coalescing, NAPI budgets, GRO size and flush reasons, RSS table and hash fields, IRQ affinity, RPS maps and backlogs, XPS queues, qdiscs, application CPUs and NUMA placement. Collect per-queue packets, bytes, CPU, polls, budget exhaustion, IPIs, backlog delay, GRO aggregates, reorder, retransmission and application percentiles.

First disable or reduce one mechanism at a time on a bounded canary: RPS to remove remote queueing, GRO to expose packet granularity, moderation to test wake latency, or XPS changes to test queue order. Keep load and application placement fixed. Compare packet, byte and CPU balance, not aggregate throughput alone.

Reorder concentrated at indirection or RFS changes suggests overlapping old and new backlogs. High p99 with large GRO and moderation can reflect batching delay. Remote NUMA access may appear after RPS. Confirm with timestamped stage traces and receiver evidence while accounting for observer overhead.

### Answer 5

Generate IPv4 and IPv6 TCP, UDP, fragments, VLANs, single and nested tunnels, NAT, bridge, forward and local traffic. Test every supported checksum and segmentation combination with offload on and off, malformed metadata, unsupported final devices, feature changes, mapping failure and reset. Compare receiver or wire bytes with a software reference.

Exercise GRO compatibility boundaries for sequence, options, checksums, marks, security, timestamps and tunnels. Trace logical segments through congestion and qdisc accounting. Test XDP pass, drop, transmit and redirect plus AF_XDP fill, receive, transmit and completion ownership for single and multi-buffer frames. Race teardown with page-pool returns.

Change channels, rings, RSS buckets, hash key, affinities, RPS/RFS/XPS maps, application CPUs and NUMA policy under load. Inject hotplug and device removal. Assert bounded queues, expected flow stability, no stale DMA, no double recycle, correct software fallback and eventual reclamation.

Record kernel, driver, firmware, physical or virtual device, features, DMA model, offloads, topology, traffic, faults and capture point. Loopback cannot prove NIC behavior; host capture can precede segmentation; one device cannot establish another's correctness; finite combinations do not prove all metadata interactions; throughput does not prove ordering or wire validity. State those limits.
