---
module_id: CA-045
program: Computer Architecture
level: 1
module_number: 45
title: Network Interface Architecture
status: complete
last_verified: 2026-09-04
---

# Network Interface Architecture

## One-Page Review

### Governing question

How does a network interface transform wire frames into protected processor-visible buffers and transmit descriptors into valid frames while preserving byte/packet identity, DMA ownership, queue ordering, checksums/offload semantics, flow steering, interrupt/poll progress, isolation and truthful payload/line-rate performance?

### Essential definitions

- A **network interface controller** (`NIC`) connects a host/device memory system to one or more network links.
- An **RX queue** receives frame data into host-provided buffers and writes completion metadata.
- A **TX queue** consumes host descriptors/buffers and emits frames, later returning completion/ownership.
- A **descriptor ring** is a circular producer/consumer structure shared between software and NIC.
- **receive-side scaling** (`RSS`) hashes selected packet fields and maps flows to RX queues/CPUs.
- **flow steering** applies rules to direct matching traffic to queues, functions or actions.
- **NAPI-style polling** switches from per-event interrupts toward bounded polling under load.
- **interrupt moderation/coalescing** delays/groups notifications to reduce CPU overhead.
- **checksum offload** calculates or verifies protocol checksums under specified header/parsing conditions.
- **segmentation offload** accepts a large host packet and emits multiple wire-sized segments.
- **receive coalescing** combines several received segments into a larger host object while preserving protocol semantics.
- A **scatter-gather packet** spans multiple DMA buffers/descriptors.
- **headroom/tailroom** are buffer bytes reserved before/after packet data for headers/metadata/alignment.
- **line rate** is physical link bit rate; **payload goodput** excludes encoding, framing, gaps and headers selected by the measurement.
- A **virtual function** or mediated queue exposes limited NIC resources to a tenant/guest.

### Central model, mechanism, or theorem

RX is an ownership pipeline: software maps empty buffers, publishes descriptors, NIC receives/validates a frame and DMA-writes only within owned bounds, writes length/status/hash/checksum metadata, orders data before completion/interrupt, then software synchronizes and consumes. TX reverses ownership: software constructs packet/metadata, maps/publishes descriptors and doorbell; NIC validates, fetches, segments/checksums as requested, transmits, records completion and returns buffers. At every transition, exact lengths, context, IOMMU permissions and offload preconditions determine valid bytes and semantics.

### Critical invariants

- NIC DMA reads/writes stay within currently owned, mapped descriptor segments and validated lengths.
- Descriptor/ring phase prevents producer overrun, consumer reuse and stale completion ABA.
- RX packet bytes and completion metadata are visible before software observes ownership/notification.
- TX packet bytes/metadata are visible before NIC observes ownership/doorbell.
- Reported lengths exclude/include FCS, VLAN and padding exactly as the driver/API contract states.
- Checksum/segmentation/coalescing results match non-offloaded protocol semantics for supported packets.
- RSS/steering never bypasses tenant/function/IOMMU isolation or silently reorders a flow beyond guarantees.
- Interrupt-to-poll and poll-to-interrupt transitions cannot lose wakeups or starve queues.
- Errors, reset, link changes and partial multi-descriptor packets return ownership without double free/use.
- Throughput/latency claims state link encoding, wire bytes, payload definition, queues, CPU and workload.

### Common failures

Common failures include advertising a buffer before DMA mapping/synchronization, trusting a device length larger than capacity, consuming RX data before completion ordering, freeing TX buffers before device completion, ring wrap without generation bits, splitting a packet but returning only some descriptors, claiming checksum-valid without parsing/tunnel conditions, applying segmentation with wrong header offsets, steering fragments inconsistently, enabling RSS with an exposed stable secret-less hash, losing a packet in the NAPI unmask race, coalescing until latency becomes unbounded, counting 1,500 payload bytes as a 1,500-byte wire event, and benchmarking loopback/offload aggregates as physical packet rate.

### Compact example

For an illustrative 10 Gb/s Ethernet link, a frame carrying 1,500 payload bytes has 14 header plus 4 FCS bytes, and adding 8 preamble/SFD plus 12 interpacket-gap byte-times gives 1,538 modeled wire bytes. The ceiling is 812,743.82 packets/s, 9.753 Gb/s selected payload, or 97.529% efficiency. Minimum 64-byte frames plus 20 wire-overhead byte-times yield 14,880,952.38 packets/s but only 5.476 Gb/s of 46-byte payload. The model excludes encoding and optional tags/headers.

### Connections

NIC architecture connects Ethernet/protocol framing, PCIe, DMA/IOMMU, interrupts, queues, hashing, parallel CPUs, checksum/segmentation, virtualization, security filtering, congestion, time synchronization and packet-performance methodology.

## Governing Question

A NIC is a specialized parallel packet computer. It parses link/protocol headers, steers traffic, moves buffers with DMA, performs optional transforms and communicates through queue/interrupt state.

High packet rates make per-packet CPU work, cache locality and synchronization decisive. Correctness still depends on exact ownership and length validation: one malicious frame or device error must not become an arbitrary DMA write.

## Why This Matters

Network traffic is externally influenced and often untrusted. RX paths must treat length, checksum and metadata as device-provided evidence, not authority. TX offload bugs can emit invalid packets at scale.

Multiqueue/RSS improves parallelism but can reorder flows or concentrate hotspots. Interrupt moderation improves throughput but raises latency. Virtual functions improve density but share firmware, link and internal resources.

Wire-rate claims require framing arithmetic and end-to-end measurement; host aggregation can obscure actual segment count.

## Prerequisites and Retrieval

Before studying this module, be able to:

- trace DMA descriptor ownership and IOMMU mappings;
- reason about circular queues, phases and memory ordering;
- parse Ethernet and basic IP/transport headers safely;
- distinguish IOPS/packet rate, bit rate and payload goodput;
- explain interrupts, polling, affinity and cache locality.

Retrieve link technology/rate/encoding/FEC and trained state; MAC frame rules, MTU, FCS/VLAN/padding; PCIe/device/function topology; RX/TX queue/ring/descriptor formats, alignment and phase; buffer size/headroom/scatter limits; DMA/coherence/IOMMU; completion/doorbell order; interrupts/MSI-X, NAPI budget and moderation; RSS key/hash/input/indirection; steering/filter priorities; checksum/segmentation/coalescing/tunnel capabilities; timestamping; pause/flow control; virtualization/isolation/rate limits; reset/link/error/stat counters; NIC firmware/driver/OS/offload settings; traffic generator topology, packet sizes and errata.

## Learning Objectives

After completing this module, you should be able to:

1. trace RX and TX ownership from ring publication through completion;
2. validate descriptor segments, packet lengths and multi-buffer chains;
3. design ring wrap/phase and doorbell/completion ordering;
4. explain RSS, flow steering, queue affinity and ordering trade-offs;
5. integrate interrupts, moderation and bounded polling without lost wakeups;
6. specify checksum, segmentation and receive-coalescing preconditions;
7. isolate DMA/interrupt/queue resources across functions and tenants;
8. calculate wire packet rate and selected payload efficiency explicitly;
9. verify byte/packet conservation, offloads and recovery;
10. benchmark NICs with reproducible wire/host/CPU evidence.

## Core Exposition

### Separate planes

The data plane moves frames through RX/TX queues. The control plane configures link, addresses, queues, filters, offloads and statistics. The management plane may update firmware and health state.

Protect each plane separately; a data queue should not rewrite global control.

### Understand the receive path

Software allocates/maps buffers, fills RX descriptors and publishes ownership. NIC receives a frame, chooses queue, writes data/metadata, completes and optionally interrupts.

Software synchronizes, validates and passes the packet upward before recycling/replacing the buffer.

### Understand the transmit path

Software builds a packet, maps one or more segments, writes TX descriptors/offload context, publishes and rings doorbell. NIC fetches and transmits before completion.

Driver unmaps/frees only after device ownership returns.

### Validate DMA addresses

Descriptors contain device-visible addresses, not arbitrary CPU pointers. IOMMU mappings grant least required read/write permissions for exact buffer lifetime.

Guard against descriptor corruption, address overflow and cross-page/boundary constraints.

### Validate RX length

Completion length must be nonnegative, within sum of owned segment capacities and consistent with descriptor/status rules. Reject/truncate only according to safe contract.

Never let device-reported length drive an unchecked CPU copy/parser.

### Define FCS and padding semantics

NIC may strip or retain Ethernet FCS; padding may be included in DMA length while upper payload length differs. VLAN tags may be stripped into metadata.

Document exact byte representation at every API layer.

### Handle multi-buffer RX

Jumbo or header-split packets can span descriptors. Start/end/error flags and total lengths assemble one packet.

On malformed/incomplete chains, reclaim every consumed buffer exactly once without exposing partial untrusted data.

### Handle scatter-gather TX

One packet may reference several mapped segments. Check total length, segment count and offload header contiguity/alignment.

Completion returns the entire packet chain under descriptor rules; partial freeing causes leaks/use-after-free.

### Use ring phases

Producer/consumer index plus phase/generation distinguishes full, empty and wrapped entries. Ownership bits transition only after fields are stable.

Counters wider than ring index simplify occupancy and wrap proofs.

### Publish RX buffers

Map/synchronize empty storage, write descriptor address/capacity, then release-order ownership/producer before doorbell. CPU does not access device-owned receive bytes.

Maintain reserve descriptors so temporary allocation pressure does not deadlock RX.

### Consume RX completions

Observe completion with acquire/DMA synchronization, validate status/length/chain, then access packet bytes. Refill/recycle only after upper-layer ownership decision.

Completion is ordered after NIC DMA data under platform rules.

### Publish TX packets

Finish payload/header writes and DMA mapping, write descriptor/context, release-order ownership, then doorbell. NIC must not see a half-initialized descriptor.

Noncoherent platforms require direction-specific cache synchronization.

### Reclaim TX completions

Read completion/consumer state, synchronize, unmap segments and free packet once. Batch reclaim to reduce cache/MMIO cost while bounding resource delay.

Timeout/reset paths must reconcile descriptors whose wire effect is uncertain.

### Manage doorbells

Doorbells announce producer progress, not descriptor content. Batch multiple descriptors per MMIO write when latency allows.

Ensure descriptor visibility before doorbell and avoid ringing beyond published entries.

### Manage writebacks

NIC may write completion entries or consumer indices. Host avoids false sharing and reads with appropriate DMA ordering.

Writeback batching reduces PCIe traffic but can delay reclamation/interrupt decisions.

### Map queues to CPUs

Bind RX interrupt/poll and TX completion work near application/queue memory to improve cache locality. Too many queues add state and dilute traffic.

Topology/NUMA placement matters for DMA memory and PCIe root.

### Understand RSS hashing

RSS hashes selected tuple fields with a key and uses indirection to choose a queue. Packets of a supported flow normally map consistently while configuration is stable.

Fragments, tunnels and asymmetric directions require defined parsing/input.

### Choose RSS inputs

Including more fields spreads traffic but can split flows/fragment sets. Excluding ports for fragments may concentrate load.

Document protocol/header depth and fallback for malformed/encrypted/tunneled packets.

### Protect RSS state

Hash keys and indirection affect predictability and tenant isolation. Untrusted traffic can target queues if mapping is learnable.

Rotate/partition/configure under threat model without silently reordering active flows.

### Apply flow steering

Exact/wildcard filters match header fields and choose queue/drop/mirror/action. Rule priority, overlap and resource exhaustion need explicit behavior.

Validate parser bounds and isolate tenant rule tables/actions.

### Use receive packet steering

Software can redirect processing after RX to another CPU using flow hashes/backlogs. It trades cache transfer and queueing for load balance.

Hardware RSS, IRQ affinity and software steering should be designed together.

### Use transmit packet steering

Software chooses TX queues by flow/CPU/device policy. Queue selection affects lock contention, ordering and traffic-class scheduling.

One flow should not reorder unless transport/path permits it.

### Moderate interrupts

Count/time thresholds group completions. High thresholds reduce CPU/PCIe messages but add latency and can delay low-rate queues.

Adaptive moderation uses load evidence with bounds/hysteresis.

### Poll under load

Interrupt disables/masks queue notification and schedules a bounded poll. Poll processes up to budget; if work remains, reschedules; if empty, rearms with race check.

The rearm protocol must catch a packet arriving between empty observation and interrupt enable.

### Budget polling fairly

Budgets stop one busy queue from monopolizing CPU. Too small increases scheduling overhead; too large raises latency for others.

Track work and time budgets plus per-queue starvation.

### Verify checksums

RX hardware can report checksum verified only for recognized header layout/protocol coverage. Driver conveys exact level/status, not a universal “good packet.”

Software validates unsupported, fragmented, tunneled or error cases.

### Generate TX checksums

Driver supplies start/offset/protocol context that matches final headers. NIC computes after segmentation/modification at correct layer.

Wrong offsets can corrupt arbitrary payload or emit invalid checksums.

### Perform segmentation offload

Host submits a large logical packet plus MSS/header context; NIC emits multiple packets with updated lengths, sequence numbers and checksums.

Wire packet/byte counters differ from host packets; validate each generated segment.

### Perform receive coalescing

Hardware/software may combine compatible sequential transport segments. Preserve flow, ordering, flags/options/checksum/timestamps and maximum size.

Coalescing changes host packet counts/latency, not wire events.

### Handle VLANs

NIC can insert/strip/filter VLAN tags and report metadata. Stacked tags and tenant policies require exact parser/action support.

Payload/wire length calculations state included tags.

### Handle tunnels

Offloads may parse outer and inner headers to defined depth/types. Unsupported tunnels fall back without false checksum/steering claims.

Malformed length recursion is hostile input.

### Timestamp packets

Hardware timestamps near MAC/PHY reduce software jitter. Match timestamp to packet/queue and define clock domain/correction point.

Queueing and asymmetric path delay remain outside timestamp hardware.

### Handle pause and congestion

Link flow control can pause traffic, affecting latency and head-of-line blocking. Per-priority mechanisms require consistent classification.

Lossless claims need buffer/deadlock analysis across the network, not NIC alone.

### Handle drops

Drops can occur at MAC errors, filters, no RX descriptors, internal buffers, DMA faults or software backlog. Counters need scope and overlap definitions.

Preserve reason and avoid double-counting one packet at several layers.

### Recover RX starvation

If no buffers are posted, NIC drops/backpressures per technology. Driver replenishes safely and exposes starvation counters.

Do not reuse an upper-owned buffer just to keep ring full.

### Recover TX stalls

Queue can stop when descriptors unavailable and wake after reclaim. Use ordering to avoid missed wakeup between fullness check and completion.

Watchdog timeout records evidence before reset and treats on-wire outcome carefully.

### Handle link changes

Link down/up renegotiates speed/duplex/FEC and may invalidate in-flight assumptions. Stop/restart queues in documented order.

Carrier notification and packet completion are distinct.

### Handle reset

Disable traffic/interrupts, quiesce DMA, reconcile rings/mappings, reset, restore configuration and republish fresh generations. Reject late completions.

Virtual functions and shared firmware expand reset scope.

### Virtualize queues

SR-IOV/mediated designs assign queue, DMA and interrupt resources per tenant. IOMMU and filtering enforce boundaries.

Shared link/internal buffers/scheduler/firmware still need QoS and side-channel analysis.

### Enforce rate/QoS

Traffic classes, shapers and schedulers allocate transmit service. Validate rate units, burst size and starvation bounds.

RX policing/drop policy affects tenant isolation and counters.

### Secure device firmware

Firmware controls parsers/DMA/scheduling and is part of trusted computing base. Authenticate updates, support rollback policy and expose version/health.

Contain a compromised function/device with IOMMU, remapping and reset ownership.

### Compute wire accounting

State Ethernet header, payload/padding, VLAN, FCS, preamble/SFD and interpacket gap byte-times; add encoding/FEC where relevant.

Different measurement points count different subsets, so label payload, frame, MAC and wire rates.

### Measure packet rate

Packet/s ceiling is line bits/s divided by modeled wire bits/packet. Small packets maximize packet-processing pressure while carrying less payload.

Bidirectional results state per-direction/full-duplex aggregation.

### Measure host cost

Report CPU cycles/instructions/cache misses, IRQ/poll time, copies, batching and NUMA placement per packet/byte. Offloads shift work rather than erase it.

Pin frequency/affinity and include application stack.

### Verify rings and DMA

Use byte-accurate scoreboards, guard pages/IOMMU faults and assertions for ownership/phase/occupancy. Inject wrap, full/empty, backpressure and malformed completions.

Check every mapped segment is unmapped/freed exactly once.

### Verify offloads

Compare captured wire packets with software reference segmentation/checksum/parser results over randomized headers, fragments, tunnels and boundaries.

Never infer correctness from throughput alone.

### Gather layered evidence

Start with wire arithmetic/ring models, then RTL/device emulation, driver tests, packet captures, fault injection and physical traffic generators.

Bind link/NIC firmware, driver/OS, queues/offloads, CPU/NUMA, topology, generator and errata.

## Definitions and Notation

- `R`: physical link bits/second per direction under trained mode.
- `P`: selected payload bytes/packet.
- `F`: bytes counted in the MAC frame, under explicit FCS/tag inclusion.
- `O`: additional preamble/gap/encoding/FEC byte-equivalent overhead included in a model.
- `wire_bytes=F+O` under that model.
- `pps=R/(8*wire_bytes)`.
- `goodput=pps*8*P` selected payload bits/second.
- `efficiency=P/wire_bytes` for the selected numerator/denominator.
- `N`: descriptor ring entries; `prod`, `cons`, `phase` identify state.
- `capacity(d)`: DMA bytes authorized for descriptor `d`.
- `length(c)`: device-reported bytes in completion `c`, requiring `length<=capacity` across chain.
- `ownership(x) in {software,nic,transition,error}`.
- `notify_after_data`: DMA data/metadata happens-before observed completion notification.
- `flow_key`: defined header fields hashed/matched for steering.

Wire conventions vary by link mode and measurement point. Every throughput calculation must enumerate included fields rather than relying on “packet size.”

## Mechanisms, Invariants, or Proof Structure

1. **Descriptor obligation:** address, capacity, flags, segments, context and phase validate before device use.
2. **Ownership obligation:** CPU/NIC mutate or consume only states they own.
3. **Range obligation:** every DMA byte lies within mapped authorized descriptor segments.
4. **Publication obligation:** RX buffers/TX packets and descriptors are visible before NIC ownership/doorbell.
5. **Completion obligation:** RX/TX data/status is visible before ownership return/notification.
6. **Length obligation:** packet/segment/header lengths are consistent and bounded before parsing/use.
7. **Chain obligation:** multi-descriptor packets complete/reclaim exactly once as a coherent unit.
8. **Offload obligation:** checksum/segmentation/coalescing output refines non-offloaded protocol semantics.
9. **Steering obligation:** parser/hash/rules route only within permitted queue/function/tenant state.
10. **Ordering obligation:** per-flow, descriptor, DMA and interrupt order matches interface/platform rules.
11. **Resource obligation:** ring/buffer/interrupt/backlog state never exceeds capacity.
12. **Lifecycle obligation:** link/reset/error transitions reconcile DMA mappings and stale generations.
13. **Progress obligation:** interrupt/poll/queue scheduling prevents lost wakeups/starvation under fairness.
14. **Accounting obligation:** packet/byte/drop/offload counters identify exact layer and events.
15. **Evidence obligation:** claims bind link framing, configuration, revisions, topology and workload.

Prove ring/DMA ownership and byte bounds, then refine NIC transforms to a reference packet sequence. Compose completion-before-notification and flow-order rules with host driver processing. Liveness relies on buffer replenishment, scheduling and link fairness. Performance proof is empirical after correctness.

## Alternatives and Trade-Offs

1. **Single versus multiqueue:** one queue is simple; many queues scale CPUs/flows with more state.
2. **Interrupts versus polling:** interrupts save idle CPU; polling amortizes high-rate events.
3. **Low versus high moderation:** low minimizes latency; high reduces notification/CPU overhead.
4. **Small versus large rings:** small bounds queueing/memory; large absorbs bursts.
5. **Per-packet versus batched doorbells:** per-packet lowers launch delay; batching saves MMIO.
6. **Contiguous versus scatter-gather:** contiguous simplifies DMA; SG avoids copies.
7. **Hardware versus software steering:** hardware avoids CPU work; software is flexible/observable.
8. **RSS versus exact filters:** RSS scales many flows; exact rules give deterministic placement.
9. **Offloads on versus off:** on reduces host work; off simplifies semantics/debugging.
10. **Large versus standard MTU:** large frames improve efficiency; standard MTU improves compatibility/granularity.
11. **Coherent versus streaming DMA:** coherence simplifies sharing; streaming APIs can control locality/traffic.
12. **Shared versus isolated functions:** sharing uses hardware efficiently; VFs strengthen queue/tenant separation.
13. **Throughput versus latency QoS:** batching/deep queues raise throughput; reservations/bounds protect tails.
14. **Pause versus drop:** pause preserves frames but spreads congestion; drop provides backpressure to transports.
15. **Host versus SmartNIC processing:** offload saves CPU; programmable device expands trusted/operational complexity.

## Failure Modes and Misconceptions

1. “NIC receives directly into an arbitrary pointer.” DMA mappings/descriptors authorize exact buffers.
2. “Device-reported length is trustworthy.” Validate it against owned capacity/format.
3. “One packet always uses one descriptor.” Jumbo/header split/SG can chain.
4. “Ring index equality always means empty.” Phase/generation distinguishes wrap/full.
5. “Doorbell publishes descriptor data.” Memory/DMA ordering must precede it.
6. “Interrupt guarantees packet data is visible.” Completion ordering/synchronization is required.
7. “TX buffer may be freed after doorbell.” NIC owns it until completion.
8. “Coherent DMA removes ownership rules.” It does not remove ordering/concurrent mutation hazards.
9. “Checksum-good means every protocol layer verified.” Coverage/parser level is specific.
10. “Segmentation offload emits one wire packet.” It emits many segments.
11. “Receive coalescing reduces wire packets.” It only changes host representation.
12. “RSS always preserves flow ordering.” Configuration, fragments/tunnels and queue processing matter.
13. “More queues always scale.” CPU/NUMA/cache/link/flow distribution can bottleneck.
14. “Fixed RSS key is only performance state.” Predictable hashing can enable queue attacks.
15. “Interrupt moderation only saves CPU.” It raises latency and can strand sparse work.
16. “Empty poll then unmask is race-free automatically.” Arrival between steps can be lost without protocol.
17. “Poll budget should be unlimited at high load.” Other queues/tasks need fairness.
18. “No RX buffers means backpressure always.” Ethernet may drop; technology/configuration decides.
19. “Link down means all TX failed.” Some packets may already be on wire/completed.
20. “Reset makes ring ownership obvious.” In-flight DMA and stale completions require reconciliation.
21. “1,500-byte packet uses 1,500 wire bytes.” Headers/FCS/preamble/gap add overhead.
22. “10 Gb/s means 10 GB/s.” Bits and bytes differ by eight before overhead.
23. “Host pps equals wire pps with offloads.” Segmentation/coalescing change host object counts.
24. “Drop counters are additive.” One packet can trigger overlapping layered counters.
25. “Loopback benchmark proves NIC line rate.” It may bypass physical/link/device paths.
26. “Good throughput proves parser/offload safety.” Byte-accurate adversarial verification remains required.

## Worked Examples

### Example 1

Software posts a 2 KiB RX buffer; completion length 1,518 is valid under stated FCS semantics, while length 4,096 is rejected before parsing/copying.

### Example 2

A two-descriptor jumbo frame marks start then end; an error on the second causes both consumed buffers to be reclaimed once and no partial packet delivered.

### Example 3

TX descriptor references three DMA segments and checksum context; NIC completes packet chain before driver unmaps any segment.

### Example 4

RSS hash selects queue through an indirection table; changing the table during an active TCP flow can reorder packets unless updated safely.

### Example 5

Poll finds no work, rearms interrupts, then checks producer state; a packet arriving in the window triggers/requeues rather than being stranded.

### Example 6

TSO submits 64 KiB host data with MSS 1,460; NIC emits many wire frames with adjusted sequence/length/checksum.

### Example 7

RX checksum status covers outer UDP only; driver cannot mark the encapsulated inner TCP checksum verified without capability.

### Example 8

A VF maps only its queues/buffers through IOMMU; malformed descriptors cannot reach another tenant's memory.

### Example 9

At high load, moderation increases batch size while a maximum timer bounds sparse-flow notification latency.

### Example 10

This deterministic Ethernet model compares 1,500-byte and minimum-frame packet rate and selected payload goodput.

<!-- bijux-verify: {"id":"nic-wire-rate-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"line_rate_gbps=10.0 frame_bytes=1518 wire_bytes=1538\npackets_per_second=812743.82 payload_gbps=9.753 efficiency_pct=97.529\nmin_frame_wire_bytes=84 min_frame_pps=14880952.38 min_payload_gbps=5.476\n"}} -->
```python
line_rate = 10e9
payload_bytes = 1500
ethernet_header = 14
fcs = 4
preamble_sfd = 8
interpacket_gap = 12
frame_bytes = ethernet_header + payload_bytes + fcs
wire_bytes = frame_bytes + preamble_sfd + interpacket_gap
pps = line_rate / (wire_bytes * 8)
payload_gbps = pps * payload_bytes * 8 / 1e9

minimum_frame_bytes = 64
minimum_payload_bytes = 46
minimum_wire_bytes = minimum_frame_bytes + preamble_sfd + interpacket_gap
minimum_pps = line_rate / (minimum_wire_bytes * 8)
minimum_payload_gbps = minimum_pps * minimum_payload_bytes * 8 / 1e9

print(f"line_rate_gbps={line_rate / 1e9:.1f} frame_bytes={frame_bytes} wire_bytes={wire_bytes}")
print(f"packets_per_second={pps:.2f} payload_gbps={payload_gbps:.3f} efficiency_pct={100 * payload_bytes / wire_bytes:.3f}")
print(f"min_frame_wire_bytes={minimum_wire_bytes} min_frame_pps={minimum_pps:.2f} min_payload_gbps={minimum_payload_gbps:.3f}")
```

The model includes Ethernet header, FCS, preamble/SFD and interpacket-gap byte-times but excludes VLAN, higher-layer headers, link encoding/FEC, pause, errors and implementation limits. Payload is the selected 1,500/46 bytes, not application goodput.

## Cross-Program Connections

- **Operating Systems:** drivers, NAPI, queue affinity and network stacks implement host ownership.
- **Concurrent Systems:** rings, phases, barriers and poll/interrupt handoffs govern races.
- **Networking:** framing, flow hashing, checksums, segmentation and congestion define packets.
- **Virtualization:** VFs, IOMMU and interrupt remapping isolate guest queues.
- **Security Engineering:** hostile frames/descriptors, parser bounds and firmware define attack surfaces.
- **Performance Engineering:** pps, goodput, batching, NUMA, CPU and tails determine value.
- **Formal Methods:** byte/packet conservation and ownership/refinement validate offloads.
- **Distributed Systems:** NIC ordering/loss/timestamps underpin higher-level protocols.

## References

1. Linux kernel, [Scaling in the Linux Networking Stack](https://docs.kernel.org/networking/scaling.html), current RSS/RPS/RFS/XPS and queue-scaling guidance; retrieved 2026-09-04.
2. Linux kernel, [NAPI](https://docs.kernel.org/networking/napi.html), current interrupt/poll scheduling, budget and configuration guidance; retrieved 2026-09-04.
3. Linux kernel, [Network Devices, the Kernel, and You](https://docs.kernel.org/networking/netdevices.html), current network-driver interface, synchronization and lifetime context; retrieved 2026-09-04.
4. Linux kernel, [Ethernet Device Drivers](https://docs.kernel.org/networking/device_drivers/ethernet/index.html), current driver documentation and device-specific implementation context; retrieved 2026-09-04.
5. DPDK, [Programmer's Guide](https://doc.dpdk.org/guides/prog_guide/index.html), current poll-mode driver, memory, ring and packet-processing architecture; retrieved 2026-09-04.
6. IETF, [RFC 894: Transmission of IP Datagrams over IEEE 802.3 Networks](https://www.rfc-editor.org/rfc/rfc894.html), Ethernet encapsulation context; retrieved 2026-09-04.
7. IETF, [RFC 8200: Internet Protocol, Version 6](https://www.rfc-editor.org/rfc/rfc8200.html), current IPv6 packet/header/fragment processing context; retrieved 2026-09-04.

## Exercises

### Exercise 1

Trace RX and TX descriptor ownership around ring wrap, multi-buffer packets, doorbells, completion writeback and interrupts.

### Exercise 2

Design RSS/flow-steering configuration for four queues that preserves selected flows, handles fragments/tunnels and resists queue concentration.

### Exercise 3

Specify checksum, segmentation and coalescing metadata/preconditions and a software-reference fallback for unsupported packets.

### Exercise 4

Extend the executable model for VLAN/IPv4/TCP headers, multiple MTUs, encoding/FEC and bidirectional traffic.

### Exercise 5

Write an end-to-end verification/evaluation plan for a multiqueue virtualized NIC with hostile traffic, reset and performance requirements.

## Answers to the Exercises

### Answer 1

For each slot record index/phase/owner, DMA address/capacity, flags and packet-chain ID. Software publishes RX empties/TX data after mapping/order; NIC owns until completion data/status is visible. Host acquire/sync validates lengths/chains before consumption and returns/unmaps every segment once.

Test producer/consumer equality in both phases, simultaneous wrap, full/empty, partial chains, malformed lengths, delayed completions, reset generations and lost-wakeup transitions. Assert occupancy and accepted-completed ownership conservation.

### Answer 2

Choose a keyed hash over supported symmetric flow fields, define fragment/tunnel fallback and map indirection entries evenly to queues/CPUs near memory/PCIe. Add exact security/management rules above RSS with priority/isolation. Avoid mid-flow remaps or drain/version them.

Test crafted hash concentration, elephant/mice mixes, fragments, encrypted/tunneled traffic and CPU hotplug. Measure per-queue packets/bytes/drops/latency/CPU, ordering and fairness; rotate/partition key state under threat policy.

### Answer 3

Metadata identifies parse layer, header start/length, checksum start/offset, protocol, MSS and whether headers are contiguous/writable. Validate total/header lengths, fragments, options, tunnel depth and device capability. Unsupported/ambiguous packets use software checksum/segmentation and no false verified status.

Generate reference wire packets, compare every byte/length/sequence/checksum and ensure coalescing combines only same compatible flow/order/options. Randomize malformed/boundary headers.

### Answer 4

Parameterize MAC tags, IP/TCP header bytes, payload/MSS, minimum padding, preamble/gap and encoding/FEC efficiency. Packetize application bytes, then compute frames, per-frame padding/FCS/wire bits and per-direction rate; include ACK/reverse traffic separately.

Validate the untagged cases against the supplied model. Report application, transport, L2 frame and physical wire goodput distinctly and enumerate every included field.

### Answer 5

Verify descriptor/ring phase, DMA/IOMMU bounds, publication/completion order, RX lengths/chains, TX SG reclaim, interrupts/NAPI lost-wakeup, RSS/filter tenant isolation, offload byte equivalence, errors/link/reset generations and firmware controls with formal assertions, guard mappings, fuzzed frames/descriptors and packet capture.

Measure line/frame/host packets/bytes, drops/reasons, queue balance, pps/goodput, latency tails, CPU/cache/NUMA/PCIe, moderation and tenant fairness across packet sizes/flows/directions/offloads. Bind link/NIC firmware, driver/OS, queues/offloads, CPU/topology, generator and errata; internal evidence is not external protocol, isolation or performance certification.
