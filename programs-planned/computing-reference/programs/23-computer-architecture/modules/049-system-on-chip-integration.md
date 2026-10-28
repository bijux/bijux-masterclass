---
module_id: CA-049
program: Computer Architecture
level: 1
module_number: 49
title: System-on-Chip Integration
status: complete
last_verified: 2026-09-04
---

# System-on-Chip Integration

## One-Page Review

### Governing question

How can independently correct processors, memories, accelerators, peripherals, interconnects, clocks, resets, power domains, interrupts, DMA agents, and security controllers be composed into one system whose transactions remain attributable, ordered, live, isolated, and diagnosable through every operating transition?

### Essential definitions

- A **system on chip** (`SoC`) integrates compute, memory, communication, I/O, control, security, and physical infrastructure on one device.
- An **integration contract** states an IP block's functional protocol, parameters, address map, clock/reset/power requirements, interrupt/DMA behavior, security attributes, and verification assumptions.
- An **initiator** issues a transaction; a **target** accepts and completes it. Some specifications use manager/subordinate or requester/completer terminology.
- An **interconnect** routes transactions and responses among initiators and targets while implementing decode, arbitration, ordering, buffering, and attributes.
- **ready/valid transfer** occurs only when both handshake signals are asserted in the same cycle.
- A **transaction ID** distinguishes outstanding operations within its specified identity scope.
- A **clock-domain crossing** (`CDC`) moves information between independently timed domains.
- A **reset-domain crossing** (`RDC`) connects logic that can enter or leave reset independently.
- A **power domain** is circuitry with a shared supply-state policy, often requiring isolation and retention at its boundaries.
- A **protocol bridge** converts semantics, widths, clocks, outstanding depth, ordering, or error behavior between interfaces.
- A **security firewall** admits transactions according to authenticated source, address, operation, privilege, lifecycle, and policy attributes.
- A **top-level register/address specification** is the canonical machine-readable assignment of memory windows and externally visible integration parameters.
- **integration closure** is evidence that composed protocol, function, timing, power, reset, security, and physical assumptions hold together.

### Central model, mechanism, or theorem

Represent every request as `q=(source,security,privilege,opcode,address,length,ID,ordering,attributes,data)` and every response as `r=(source,ID,status,data)`. For each accepted request, the SoC must select exactly one authorized target or a defined error target, preserve enough identity to match exactly one response, refine source/target ordering rules across adapters, and guarantee conditional progress under stated readiness and fairness. A domain transition may change routing only after admissions stop, outstanding work drains or is explicitly aborted, boundary isolation is active, and new state is synchronized before service resumes.

### Critical invariants

- Every address byte belongs to at most one enabled target window at a given lifecycle state.
- An unmapped, misaligned, unsupported, or unauthorized request completes with a defined error and no unintended effect.
- Request/response IDs remain unique within the actual outstanding scope through every width/clock/protocol adapter.
- Backpressure preserves payload stability and cannot create or duplicate a transfer.
- Ordering is neither weakened nor accidentally strengthened beyond the composed protocol contract.
- CDC transports coherent events/data; RDC and reset release cannot create phantom handshakes.
- Isolation is asserted before a source or target loses power and removed only after power, clock, reset, and state are valid.
- Interrupt and DMA identity maps to the intended device, context, privilege, and software-visible number.
- Debug, test, boot, and lifecycle modes cannot bypass production access policy unexpectedly.
- Every admitted transaction eventually completes or reaches a bounded, attributable timeout/containment path under stated assumptions.

### Common failures

Common failures include overlapping address windows, truncating high address bits, decoding only the first beat of a burst, reusing IDs across merged sources, dropping security attributes at a bridge, combinational ready/valid loops, counting a transfer when only valid is high, unsafe multi-bit synchronization, reset deassertion without synchronization, isolating after power loss, accepting traffic during clock gating, acknowledging writes before durable target acceptance, converting an error into success, connecting an interrupt to the wrong context, allowing DMA around the IOMMU/firewall, deadlocking through circular backpressure, and verifying each IP while omitting the composed path.

### Compact example

An invented 32-bit map assigns SRAM `[0x10000000,0x10010000)`, UART `[0x20000000,0x20001000)`, and DMA registers `[0x20000800,0x20001800)`. Half-open range analysis finds the UART and DMA windows overlap by 2 KiB. A request at `0x20000a00` therefore has two decoders, violating unique selection even if each peripheral and bus interface is individually correct.

### Connections

SoC integration connects digital logic, computer architecture, real-time scheduling, networks-on-chip, formal protocol verification, clock/reset/power intent, physical design, firmware machine descriptions, operating-system drivers, IOMMUs, interrupt controllers, functional safety, hardware security, observability, manufacturing test, and supply-chain IP governance.

## Governing Question

Reusable IP makes chips feasible, but component reuse shifts risk to boundaries. A processor, DMA engine, SRAM controller, and peripheral can each pass local verification while their address widths, ID scopes, clocks, resets, attributes, and error expectations disagree.

The architectural task is to turn hundreds of local assumptions into one explicit system contract and prove that every end-to-end path refines it during normal operation, boot, low power, debug, reset, and fault containment.

## Why This Matters

Integration defects often survive block-level tests because no block owns the whole path. They appear as rare data corruption, security bypass, reset hang, interrupt loss, or workload-dependent deadlock.

Late changes to address maps, clocks, power intent, interrupt numbering, or interface parameters propagate into RTL, firmware, operating systems, verification environments, emulation, and documentation.

Systematic integration makes those facts generated, reviewable, and checked rather than copied manually across teams.

## Prerequisites and Retrieval

Before studying this module, be able to:

- reason about synchronous ready/valid protocols and finite buffers;
- calculate half-open address ranges and burst byte coverage;
- explain coherence, DMA, interrupts, clocks, resets, and power domains;
- distinguish safety, liveness, ordering, and security properties;
- read an RTL interface and a machine-readable register description.

Retrieve IP versions and configuration parameters; initiator/target ports; protocol revision/subset; data/address/ID/user widths; burst/atomic/exclusive capabilities; outstanding limits; ordering domains; memory map and aliases; register side effects; endianness; clock frequencies/relationships/gating; reset polarity/assertion/deassertion and domains; power states/isolation/retention; interrupt sources/types/routes; DMA requester/stream IDs and IOMMU paths; cache/coherence domains; memory attributes; security/lifecycle/debug signals; error/timeout behavior; test/DFT connections; pin/analog interfaces; performance/QoS targets; CDC/RDC waivers; firmware descriptions; generated artifacts; verification matrices; physical constraints; errata.

## Learning Objectives

After completing this module, you should be able to:

1. specify a complete top-level contract for heterogeneous IP;
2. prove address decoding and access-control coverage/disjointness;
3. compose handshakes, IDs, ordering, responses, and outstanding limits;
4. design protocol, width, and clock adapters without semantic loss;
5. verify CDC, RDC, clock gating, reset, isolation, and retention sequences;
6. preserve interrupt, DMA, IOMMU, coherence, and security identity end to end;
7. analyze arbitration, backpressure, timeout, and deadlock progress;
8. generate consistent RTL, firmware, OS, and verification views;
9. verify top-level normal, transition, and fault behavior;
10. collect integration evidence tied to exact configurations and revisions.

## Core Exposition

### Begin with an integration inventory

List every IP instance, version, parameter set, interface, clock, reset, power domain, interrupt, DMA identity, memory window, pin, lifecycle mode, and generated artifact. Include tie-offs and unused features.

An untracked optional port or default parameter is an architectural decision made invisibly.

### Make one canonical configuration

Store instance parameters, address assignments, interrupts, clocks, resets, and interconnect connectivity in validated machine-readable sources. Generate RTL constants, firmware headers, machine descriptions, documentation, and verification models.

Derived files need provenance and consistency checks; generation does not make a wrong source correct.

### Define the transaction envelope

For each interface, record legal opcodes, address/data/byte-enable widths, burst lengths, alignment, IDs, user/security/QoS attributes, response codes, atomicity, exclusives, and outstanding limits.

Do not integrate from signal names alone; identical-looking channels can carry different semantics.

### Use ready/valid exactly

A transfer occurs on `valid && ready`. While `valid && !ready`, the source retains valid and keeps payload stable until acceptance unless the protocol explicitly permits cancellation.

Avoid combinational dependency cycles across modules; register slices or elastic buffers break timing and deadlock-prone paths.

### Size buffering from protocol obligations

Buffers absorb latency and decouple timing, but finite entries must cover accepted outstanding work. Credits or readiness must stop admission before capacity is exceeded.

Account separately for requests, write data, responses, retries, and cross-channel coupling.

### Define ID scope

IDs can be unique per source port rather than globally. An interconnect that merges sources extends IDs with source identity and reverses the mapping on response.

If a bridge narrows IDs, it must serialize or maintain a collision-free translation table until completion.

### Route every response

Remember enough path/context to send each response to its issuing source even when targets complete out of order. Validate status and beat count before releasing tracking state.

Late or duplicate responses after timeout/reset are quarantined rather than matched to a reused ID.

### Specify ordering domains

Protocols can order transactions by ID, address, barrier, channel, source, destination, or explicit attribute. Write data and response channels may have separate rules.

Adapters must preserve every required before/after edge while avoiding unnecessary serialization that destroys throughput.

### Decode complete byte ranges

Compute every beat and byte touched by a transaction with checked arithmetic. Require one enabled target for the whole legal transaction or split only where the protocol and side effects permit.

A start-address hit does not authorize a burst crossing into another target.

### Prove map disjointness and coverage

Use half-open windows and explicit priorities only for intentional aliases. Check overflow, alignment, power-of-two assumptions, remap states, debug views, and lifecycle-dependent windows.

Route unmapped space to a bounded error responder rather than hanging forever.

### Preserve byte lanes and endianness

Width adapters map addresses, byte strobes, ordering, and data lanes explicitly. Narrow writes must not modify unselected bytes; reads return the documented lane placement.

Endianness conversion belongs at a named boundary and must include atomics and register side effects.

### Split and combine transactions safely

A wide request may become multiple narrow operations. Define partial failure, observation order, atomicity, and response aggregation.

Never split an atomic or side-effecting access unless the target contract guarantees equivalence.

### Bridge protocols semantically

Map request classes, burst rules, IDs, responses, errors, barriers, attributes, and backpressure—not merely wires. Unsupported operations fail before any effect.

Prove the bridge refines a source transaction into permitted target operations and one source-visible completion.

### Cross clock domains by information type

Use synchronizers for stable single-bit levels, toggle/pulse schemes for sparse events, Gray-coded counters for monotonic multi-bit state, and asynchronous FIFOs or handshakes for payloads.

Specify metastability containment, source/destination reset behavior, coherency, loss/duplication, and throughput.

### Verify asynchronous FIFOs

Synchronize Gray-coded pointers, compare them conservatively for full/empty, and ensure payload memory is written/read only on local handshakes. Reset cannot invent a word or hide an accepted word without explicit flush semantics.

Depth and pointer width include the wrap bit; full and empty must not alias.

### Treat reset as a protocol

Asynchronous assertion can force safety promptly; deassertion is synchronized independently in each clock domain. Dependencies release only after power-good and clock validity.

Reset values must produce legal handshake, isolation, interrupt, and access-control states.

### Analyze reset-domain crossings

A source in reset can change outputs while a destination remains live. Clamp, handshake, retain, or tolerate those values according to the interface contract.

RDC analysis complements CDC; a common clock does not make independent resets safe.

### Gate clocks only when quiescent

Stop new work, wait for local accepted work and required responses to drain, establish stable boundary values, then gate. Wake restores clock and synchronization before readiness.

Clock gating in the middle of a handshake can deadlock the peer waiting for completion.

### Sequence power domains

Power-down disables admissions, quiesces transactions/DMA/interrupts, saves retention state, asserts isolation, resets/gates clocks, then removes power. Power-up reverses dependencies with power-good and state validation.

Isolation cells clamp off-domain outputs to values safe for live neighbors.

### Define retention precisely

Name retained registers/memory, save/restore conditions, reset interactions, integrity protection, and software-visible loss indicators. All other state is reinitialized.

Partial retention must not combine a new transaction with an old ID, permission, or interrupt state.

### Integrate coherence boundaries

Classify initiators as coherent, I/O-coherent, or noncoherent and map their memory attributes/snoop behavior. Connect home nodes, snoop filters, caches, and barriers consistently.

A coherent interconnect does not repair a noncoherent device or wrong cacheability attribute automatically.

### Integrate DMA paths

For every DMA-capable IP, trace descriptors, requester/stream ID, address width, IOMMU/firewall, coherent/noncoherent path, interrupt, reset, and quiescence. Deny-by-default before software assignment.

Hidden debug/test DMA and peer paths need the same analysis.

### Integrate interrupts end to end

Map source event through synchronizer/gateway, pending state, priority/enable/route, target context, claim/acknowledge/complete, and software number. Preserve level versus edge semantics.

Test simultaneous sources, persistent levels, reassertion, masking, migration, reset, and power transitions.

### Preserve source and security attributes

Carry authentic initiator identity, privilege, security state, virtual context, instruction/data classification, and lifecycle/debug policy to each enforcement point. Define trusted transformations explicitly.

Never synthesize a privileged default when an upstream attribute is absent or malformed.

### Place firewalls at complete boundaries

Check entire ranges, operation, source, privilege, state, and target permissions before effects. Protect configuration registers that can disable or reroute the firewall.

Account for DMA, debug, test, peer, speculative, and maintenance traffic—not only CPU loads/stores.

### Integrate IOMMU identity

Requester/stream IDs must be unique at the IOMMU, stable through bridges, and match firmware/OS tables. Reset and hot reconfiguration cannot let old requests inherit a new owner's context.

Interrupt remapping and peer routes are related but separate isolation paths.

### Make register side effects explicit

Record read-clear, write-one-clear, write-one-set, self-clearing, shadowed, locked, hardware-updated, and atomic-alias behavior. Bridges and width conversion must preserve allowed access sizes.

Generated models should drive RTL, software accessors, documentation, and scoreboards consistently.

### Define errors end to end

Map decode, permission, alignment, timeout, target, parity/ECC, poison, and unsupported-operation errors into unambiguous source responses and logs. Preserve attribution without leaking protected data.

An adapter must not turn an unknown response into success to maintain compatibility.

### Bound timeouts carefully

Timeouts contain hangs but cannot retract an operation already accepted by a target. Quarantine late responses and reconcile whether an effect occurred before retry.

Set budgets from legal worst-case latency and power/wake behavior, not arbitrary simulation convenience.

### Analyze deadlock structurally

Build a channel dependency graph for buffers, credits, arbitration, bridges, coherence, memory, and power-management waits. Break cycles with ordering rules, escape resources, or independent progress paths.

Random testing alone rarely proves the absence of rare circular waits.

### Specify arbitration and QoS

Choose fixed priority, round-robin, weighted, deadline-aware, or class-based service per resource. State fairness and maximum interference assumptions.

Reserve progress for interrupts, invalidation, errors, and power/reset control under hostile bulk traffic.

### Budget performance end to end

Decompose latency into source queue, arbitration, bridge, CDC, interconnect, target, and response components. Budget bandwidth at each shared link including protocol overhead and read/write directionality.

Average throughput does not establish tail latency or critical-client service.

### Integrate debug and test modes

Define lifecycle authorization, authentication, ownership, memory access, trace, halt, scan, boundary-test, and reset effects. Tie unused test inputs to safe values and verify production locks.

Debug access can bypass CPU permissions and must be modeled as another powerful initiator.

### Integrate analog and pins

Synchronize/control analog status, calibration, power-good, entropy, thermal, and clock signals with explicit validity. Map pads, muxes, pulls, voltage domains, and contention rules.

Digital simulation assumptions must match mixed-signal and package constraints.

### Generate firmware-facing descriptions

Emit address constants, interrupt numbers, clock frequencies/IDs, resets, power domains, DMA/IOMMU mappings, and compatible/version data from the canonical source. Validate generated ACPI/Devicetree/headers against RTL elaboration.

Software discovery is part of the integration product, not after-the-fact documentation.

### Verify top-level connectivity

Lint every port, width, direction, constant, unconnected net, clock/reset association, and parameter. Compare elaborated connectivity with intended instance/interface graph.

Explicitly review tie-offs because syntactically legal constants can disable security or error reporting.

### Verify transactions end to end

Scoreboard accepted requests against a reference model through decode, policy, adaptation, target effect, and exactly one matching response. Assert payload stability, ID integrity, ordering, and no effect on rejected traffic.

Cover every initiator-target-operation-state combination allowed by policy.

### Verify transitions and faults

Race traffic with reset, clock gating, power-down/up, remap, timeout, interrupt mask, firewall change, and IOMMU invalidation. Inject malformed responses, stuck ready/valid, ECC, CDC delay, and missing acknowledgments.

Check bounded recovery and evidence preservation, not only eventual reset.

### Close implementation assumptions

CDC/RDC correctness, timing exceptions, synchronizer placement, isolation/retention insertion, clock-tree constraints, voltage crossings, congestion, IR drop, and thermal limits must match RTL intent.

Post-layout timing and power-aware simulation can invalidate clean functional RTL results.

### Gather layered evidence

Combine generated consistency checks, lint, protocol assertions, formal decode/security/deadlock properties, CDC/RDC, unit and subsystem simulation, emulation, FPGA, power-aware gates, firmware/OS boot, stress, and silicon counters.

Bind evidence to exact IP commits, configuration inputs, generators, tool versions, waivers, netlist, firmware, board/package, workload, and errata.

## Definitions and Notation

- `q=(src,sec,priv,op,addr,len,id,ord,attr,data)`: accepted request identity and payload.
- `r=(src,id,status,data)`: response routed to its source context.
- `R=[base,end)`: enabled target address window after checked `end=base+size`.
- `bytes(q)=[addr,addr+len)`: complete byte range, including burst expansion.
- `decode(q)`: unique target or defined error target for every byte of `q`.
- `outstanding(src,id)`: accepted request not yet completed or explicitly aborted.
- `transfer=valid && ready`: one channel beat accepted on a clock edge.
- `owner(resource,state)`: component authorized to mutate a resource in a lifecycle state.
- `quiescent(domain)`: no new admission and no unaccounted operation that can affect a live neighbor.
- `CDC_refine`: destination event/data sequence equals the permitted source sequence without corruption, duplication, or unreported loss.
- `progress(q)`: an admitted request eventually completes or enters its documented bounded containment path.

Protocol names and attribute encodings are architecture-specific. Map these abstract fields to the exact interface version and configured subset.

## Mechanisms, Invariants, or Proof Structure

1. **Inventory obligation:** every instance, interface, parameter, tie-off, mode, and derived artifact is owned and versioned.
2. **Decode obligation:** complete request ranges select exactly one enabled authorized target or explicit error.
3. **Handshake obligation:** acceptance occurs exactly on protocol handshakes with stable payload under stall.
4. **Identity obligation:** source/context/ID remains unique until exactly one matching completion or abort.
5. **Ordering obligation:** all required ordering edges survive arbitration, buffering, splitting, merging, and bridging.
6. **Attribute obligation:** byte enables, cacheability, security, privilege, QoS, and error meaning are preserved or validly transformed.
7. **Capacity obligation:** credits/readiness prevent every finite queue and tracking table from overflow.
8. **CDC/RDC obligation:** asynchronous timing and independent resets cannot corrupt, invent, duplicate, or silently lose state.
9. **Power obligation:** quiescence, retention, isolation, reset, clock, and power-good follow the dependency order.
10. **Coherence obligation:** each initiator's coherent/noncoherent behavior and memory attributes match the shared-memory contract.
11. **Isolation obligation:** CPU, DMA, debug, test, peer, and maintenance traffic all pass the intended enforcement points.
12. **Interrupt obligation:** every source/event maps to the correct target/context with exact acknowledge/complete semantics.
13. **Fault obligation:** failures are bounded, attributable, non-escalating, and cannot be mistaken for success.
14. **Progress obligation:** arbitration and channel dependencies guarantee conditional completion for admitted legal work.
15. **Evidence obligation:** RTL, generated software views, verification models, physical constraints, and results share configuration identity.

Prove local interface refinement first, then compose paths from initiator acceptance to target effect and response. Safety covers unique decode, identity, ordering, isolation, and no unintended effect. Liveness uses explicit readiness/fairness/power assumptions. Transition proofs introduce an epoch so late responses and retained state cannot cross ownership generations.

## Alternatives and Trade-Offs

1. **Shared bus versus network on chip:** a bus is simple at small scale; a NoC scales bandwidth/topology with more routing state.
2. **Crossbar versus multistage fabric:** crossbars reduce hops; staged fabrics reduce wiring and quadratic growth.
3. **Central versus distributed decode:** central decode is easy to audit; distributed routing scales but duplicates policy.
4. **Wide versus narrow links:** wide links provide bandwidth; narrow links save area/wires but need serialization.
5. **Deep versus shallow buffering:** depth absorbs latency; shallow queues reduce area and bound hidden work.
6. **Many versus few outstanding IDs:** concurrency hides latency; tracking and verification complexity grow.
7. **Strong versus relaxed ordering:** strong ordering simplifies clients; relaxation improves parallelism with explicit fences.
8. **Synchronous versus asynchronous bridges:** synchronous paths are simpler; asynchronous bridges permit independent clocks.
9. **Asynchronous versus synchronous reset assertion:** asynchronous assertion reacts promptly; synchronous behavior simplifies timing.
10. **Retention versus reinitialization:** retention accelerates wake; reinitialization reduces stale-state risk and leakage.
11. **Coherent versus software-managed DMA:** coherence simplifies sharing; explicit maintenance can reduce fabric cost/traffic.
12. **Central firewall versus per-target checks:** central policy is uniform; distributed checks protect alternate paths.
13. **Timeout versus indefinite wait:** timeout contains hangs; it complicates late effects and retry safety.
14. **Generated versus handwritten integration:** generation enforces consistency; handwritten code can express exceptions more directly.
15. **Aggressive QoS versus simple fairness:** tailored QoS meets critical tails; simple fairness is easier to verify and prevent starvation.

## Failure Modes and Misconceptions

1. “Correct IP blocks make a correct SoC.” Boundary contracts and composed paths create new failures.
2. “Matching port widths means protocols match.” Ordering, errors, bursts, IDs, attributes, and lifecycle still differ.
3. “Valid alone transfers data.” Transfer requires valid and ready together.
4. “A stalled source may change payload.” It must remain stable under the protocol contract.
5. “IDs are globally unique.” Their scope is usually interface/source specific.
6. “Narrowing IDs is harmless.” It aliases outstanding transactions unless serialized or translated.
7. “Start-address decode is enough.” Bursts and lengths can cross target or protection boundaries.
8. “Power-of-two masks cannot overlap.” Wrong high bits, aliases, and remap states still overlap.
9. “Unmapped requests may wait forever.” They need a defined bounded error path.
10. “Width conversion is only data slicing.” Addresses, strobes, order, failures, and atomics matter.
11. “Any request can be split.” Side effects and atomicity may forbid it.
12. “Two-flop synchronizers carry buses.” Independently synchronized bits can form incoherent words.
13. “A narrow pulse always crosses.” It may vanish between destination edges.
14. “Common clock means reset crossing is safe.” Independent reset transitions still create hazards.
15. “Asynchronous reset may deassert anywhere.” Deassertion needs domain synchronization.
16. “Clock gating is safe when the block seems idle.” Accepted/in-flight work and peer waits must quiesce.
17. “Isolation can follow power-off.” Off-domain outputs can corrupt live logic before clamping.
18. “Retention preserves correctness automatically.” Old IDs, permissions, and partial transactions may be invalid.
19. “A coherent fabric makes every DMA coherent.” Device capability and attributes must opt into the domain.
20. “An IOMMU fixes requester identity.” Integration must carry unique authentic identities to it.
21. “One firewall protects every path.” Debug, test, DMA, peer, and maintenance routes can bypass it.
22. “An interrupt wire is enough.” Trigger type, synchronization, route, priority, claim, and completion matter.
23. “Timeout cancels the target effect.” The operation may complete late after the source timed out.
24. “Fair arbitration proves no deadlock.” Circular buffer/channel dependencies can block all contenders.
25. “Generated RTL needs no review.” Wrong canonical data or generator semantics propagate consistently.
26. “Top-level simulation proves integration closure.” Formal, CDC/RDC, power, physical, firmware, and silicon evidence remain.

## Worked Examples

### Example 1

Two target windows overlap by 2 KiB. Formal decode assertions find addresses that select both even though software normally touches only each block's base.

### Example 2

Two initiators both use ID 3. A merger prefixes source identity internally and strips it only when returning each response.

### Example 3

An ID-width bridge has four target IDs but eight possible source outstanding requests, so it backpressures after four translation entries rather than aliasing.

### Example 4

A 64-bit write with two enabled byte lanes becomes one legal 32-bit access only if both bytes reside in the same target word and side-effect policy permits it.

### Example 5

An asynchronous FIFO transports DMA descriptors while Gray pointers synchronize across clocks; independent bit synchronizers would permit a mixed descriptor.

### Example 6

Power manager stops admissions, drains target responses, saves retention, asserts isolation and reset, gates clock, then removes power; wake reverses dependencies.

### Example 7

A level interrupt remains asserted after claim until the device clears its cause, then completion allows the gateway to forward a later event.

### Example 8

A DMA source has a unique stream ID through the fabric, IOMMU, fault log, and firmware table; a reset epoch prevents late traffic from using a reassigned context.

### Example 9

A timeout returns an error but retains the ID in quarantine until the late target response is absorbed, preventing collision with a new request.

### Example 10

This deterministic map audit checks three half-open windows and demonstrates the unique-decode violation.

<!-- bijux-verify: {"id":"soc-address-map-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"sram=[0x10000000,0x10010000) size=65536\nuart=[0x20000000,0x20001000) size=4096\ndma=[0x20000800,0x20001800) size=4096\nsram_uart_overlap=0\nsram_dma_overlap=0\nuart_dma_overlap=2048\naddress=0x20000a00 targets=uart,dma unique=no\nintegration=reject\n"}} -->
```python
windows = {
    "sram": (0x10000000, 0x00010000),
    "uart": (0x20000000, 0x00001000),
    "dma": (0x20000800, 0x00001000),
}

intervals = {}
for name, (base, size) in windows.items():
    end = base + size
    intervals[name] = (base, end)
    print(f"{name}=[0x{base:08x},0x{end:08x}) size={size}")

def overlap(a, b):
    return max(0, min(a[1], b[1]) - max(a[0], b[0]))

for left, right in (("sram", "uart"), ("sram", "dma"), ("uart", "dma")):
    print(f"{left}_{right}_overlap={overlap(intervals[left], intervals[right])}")

address = 0x20000a00
targets = [name for name, (base, end) in intervals.items() if base <= address < end]
print(f"address=0x{address:08x} targets={','.join(targets)} unique={'yes' if len(targets) == 1 else 'no'}")
print("integration=accept" if all(overlap(intervals[a], intervals[b]) == 0 for a, b in (("sram", "uart"), ("sram", "dma"), ("uart", "dma"))) else "integration=reject")
```

## Cross-Program Connections

- **Digital Logic:** handshake, FIFO, arbitration, synchronizer, reset, and state-machine correctness are composed at scale.
- **Operating Systems:** generated memory maps, interrupt routes, clocks, power domains, and IOMMU identities become driver-visible contracts.
- **Computer Security:** authentic transaction identity and complete enforcement paths determine isolation.
- **Networks:** NoCs use routing, flow control, buffering, ordering, QoS, and deadlock reasoning familiar from packet networks.
- **Real-Time Systems:** arbitration and interference budgets determine worst-case service latency.
- **Formal Methods:** safety and conditional-liveness properties expose boundary cases beyond simulation.
- **Systems Engineering:** configuration control and requirement-to-evidence traceability are essential to integration closure.

## References

1. Arm, [Learn the Architecture: An Introduction to AMBA AXI](https://developer.arm.com/documentation/102202/latest/), accessed 2026-09-04.
2. Arm, [AMBA AXI and ACE Protocol Specification](https://developer.arm.com/-/media/Arm%20Developer%20Community/PDF/IHI0022H_amba_axi_protocol_spec.pdf), accessed 2026-09-04.
3. OpenTitan, [Earl Grey top-level design](https://opentitan.org/book/hw/top_earlgrey/doc/design/index.html), accessed 2026-09-04.
4. OpenTitan, [Comportability specification](https://opentitan.org/book/doc/contributing/hw/comportability/index.html), accessed 2026-09-04.
5. OpenTitan, [DMA theory of operation and SoC integration](https://opentitan.org/book/hw/ip/dma/doc/theory_of_operation.html), accessed 2026-09-04.
6. OpenTitan, [TileLink Uncached Lightweight protocol](https://opentitan.org/book/hw/ip/tlul/index.html), accessed 2026-09-04.
7. RISC-V International, [Platform-Level Interrupt Controller Specification](https://docs.riscv.org/reference/plic/index.html), accessed 2026-09-04.
8. RISC-V International, [RISC-V IOMMU specification repository](https://github.com/riscv-non-isa/riscv-iommu), accessed 2026-09-04.

## Exercises

### Exercise 1

Specify an integration contract for two CPUs, a coherent cache, noncoherent DMA, SRAM, UART, interrupt controller, IOMMU, and debug module across three clocks and two power domains. Include every identity and lifecycle boundary.

### Exercise 2

Design a bridge from an eight-ID, 64-bit burst interface to a four-ID, 32-bit target. State admission, ID translation, splitting, strobes, ordering, errors, atomics, timeout, and late-response behavior.

### Exercise 3

Prove a power-gated peripheral can shut down and wake without losing or duplicating a transaction or interrupt. Give assumptions, sequence, assertions, and fault injections.

### Exercise 4

Construct the channel dependency graph for CPUs, DMA, coherent fabric, memory controller, IOMMU, and power manager. Identify one possible cycle and a durable method to break it while preserving priority traffic.

### Exercise 5

Create an end-to-end integration verification plan spanning canonical configuration, generated artifacts, RTL, firmware, OS, power intent, implementation, and silicon. State coverage and explicit limitations.

## Answers to the Exercises

### Answer 1

Inventory each port/version/width/outstanding rule; give CPUs coherent source IDs, DMA an authentic stream ID through IOMMU, and debug a lifecycle-authorized initiator identity. Define unique half-open SRAM/MMIO windows, byte/ordering/error rules, interrupt source-to-context mapping, and firmware-visible constants from one source.

Use asynchronous FIFOs/handshakes across clocks, synchronized reset deassertion, and isolation/retention at the peripheral-domain boundary. Trace DMA data coherence maintenance, firewall/IOMMU permissions, debug bypass prohibition, quiescence, interrupt drain, power sequencing, timeout, logs, and ownership for normal/boot/debug/reset/sleep states.

### Answer 2

Maintain four bridge slots mapping `(source,source_ID)` to target ID, burst progress, error, and response state; deassert request ready when full. Split legal aligned beats, map each byte strobe/lane/address, preserve source ordering, and combine results into exactly one source completion. Reject unsupported atomics/side effects before issuing any target operation.

On partial error, follow the declared source semantics and never report success. Timeout returns error only with the slot quarantined until reset/abort proof or late completion; a late response cannot match a reused target ID. Assertions cover capacity, bijective live mapping, stable stalls, ordered effects, and exact completion.

### Answer 3

Assume peers obey backpressure and clocks can run until acknowledged quiescence. Stop admissions, record accepted work, drain or explicitly abort it, clear/route interrupts, save and check retention, assert isolation, reset/gate, then power off. Wake on always-on request, wait power-good/stable clock, release synchronized reset, restore/check state, remove isolation, then admit work.

Assert no transfer after stop acknowledgement, outstanding count zero at isolation, stable clamped outputs while off, no phantom handshake on reset, one response per accepted request, and correct interrupt epoch. Inject missing target response, wake during shutdown, clock failure, retention corruption, power-good chatter, and persistent interrupt.

### Answer 4

Create directed edges whenever one channel/resource holds state while waiting for another: CPU miss to memory response, DMA translation to IOMMU walk, walk to memory credits, memory response to fabric buffer, and power quiescence to completion. A cycle arises if memory responses need a fabric credit held by new requests while the power manager prevents those requests from draining.

Break it with reserved response/escape credits and separate always-on control progress, plus admission thresholds that preserve them. Prove acyclicity for escape paths and weak fairness for arbitration; stress saturated CPU/DMA misses during invalidation and power transitions.

### Answer 5

Validate one canonical schema and compare generated RTL constants, address/interrupt/IOMMU tables, firmware headers, Devicetree/ACPI, documentation, and scoreboards. Run elaboration connectivity/parameter/tie-off checks, lint, protocol assertions, formal decode/firewall/ID/order/deadlock properties, CDC/RDC, power-aware transition simulation, subsystem/full-chip simulation, emulation, firmware/OS boots, stress, and post-layout checks.

On silicon, correlate trace, errors, counters, QoS tails, reset causes, power cycles, and negative security/debug tests to exact IP/config/generator/tool/firmware revisions. Passing internal evidence does not establish external protocol, safety, security, timing, power, or silicon certification.
