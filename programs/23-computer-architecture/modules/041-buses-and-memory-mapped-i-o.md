---
module_id: CA-041
program: Computer Architecture
level: 1
module_number: 41
title: Buses and Memory-Mapped I/O
status: complete
last_verified: 2026-09-04
---

# Buses and Memory-Mapped I/O

## One-Page Review

### Governing question

How can processors and devices exchange reads/writes over shared or switched interconnects so that every address decodes uniquely, requests and responses survive backpressure, byte lanes and side effects are exact, ordering matches memory attributes, faults terminate cleanly and software-visible registers behave as documented?

### Essential definitions

- A **bus/interconnect** transports requests, responses, addresses, data, control and sometimes coherence among initiators and targets.
- An **initiator/master/requester** originates a transaction; a **target/slave/completer** accepts and responds.
- **memory-mapped I/O** (`MMIO`) assigns device registers or apertures within an address space accessed with load/store-like operations.
- An **address decoder** selects the target and local offset for a request.
- An **aperture** is a contiguous or otherwise defined device-visible address range.
- A **beat** is one data transfer on a channel; a **burst** groups multiple beats under protocol rules.
- A **byte enable/write strobe** identifies which byte lanes of a data beat are valid for a write.
- **ready/valid** is a decoupled handshake where transfer occurs only when both sides assert the required signals in one cycle.
- **backpressure** is a receiver's mechanism for delaying acceptance without losing or changing the offered item.
- A **posted write** may be acknowledged upstream before final target effect under a defined retained/order/error contract.
- A **non-posted request** requires a matching completion/response before requester completion.
- A **device memory type** constrains caching, speculation, gathering, reordering and early acknowledgment.
- A **read side effect** changes device state when a register is read, such as clearing status or advancing a FIFO.
- An **ordering point/barrier** constrains when earlier/later operations may become observable.
- A **bus fault/error response** terminates a request that is unmapped, denied, malformed or failed.

### Central model, mechanism, or theorem

For each accepted request `q=(address, operation, size, data, mask, attributes, source_id, order_domain)`, decode must yield exactly one authorized target/local offset or one defined error. The interconnect retains all fields until target acceptance and, for non-posted operations, matches exactly one terminal response to the source. A ready/valid producer holds payload stable while valid and not ready. MMIO register semantics then refine the bus transfer into one documented atomic state transition; memory type and fences govern visibility rather than ordinary cache assumptions.

### Critical invariants

- Every legal address selects exactly one intended target and local offset; holes/overlaps terminate by defined policy.
- Request payload and control remain stable until handshake, retry or architected cancellation.
- No request or response is dropped, duplicated, reordered beyond attributes, or delivered to the wrong source.
- Byte enables, access size, alignment and endianness update exactly the intended register lanes.
- Side effects occur exactly once at the documented acceptance/completion event, never on mere signal presentation or replay.
- Posted buffers retain writes and order/error obligations until the promised completion boundary.
- Device/strongly ordered accesses are not speculated, cached, merged or reordered contrary to architecture.
- Timeouts, errors and reset cannot convert an incomplete transaction into silent success.
- Arbitration/backpressure provides conditional progress and cannot create a protocol deadlock cycle.
- Hardware/software register maps, reserved behavior, widths and ordering examples refer to the same version.

### Common failures

Common failures include overlapping power-of-two masks, silently wrapping local offsets, accepting a payload then dropping it when ready falls, changing address/data while stalled, triggering write/read side effects every wait cycle, using read-modify-write on write-one-to-clear registers, ignoring byte strobes, assuming native endianness at every bridge, treating MMIO as cacheable RAM, using compiler barriers as hardware I/O fences, reading a status register without draining posted writes when required, timing out but later applying the transaction, returning all-zero data for unmapped space, allowing one initiator to starve, and resetting a target while an upstream completion remains expected.

### Compact example

An invented 32-bit map assigns RAM `[0x00000000,0x00100000)`, UART `[0x10000000,0x10001000)` and timer `[0x10001000,0x10002000)`. Addresses `0x10000004`, `0x10001008` and `0x20000000` decode to UART offset 4, timer offset 8 and error. A 32-bit write at UART+4 has strobe `0xf`; a two-byte write at timer+2 has strobe `0xc`; a one-byte write at timer+1 has strobe `0x2`. Pairwise range checking reports zero overlaps.

### Connections

Buses/MMIO connect address decoding, synchronous handshakes, arbitration, buffering, endian/lane conversion, memory models, device-driver APIs, interrupts/DMA, security firewalls, register generation, formal protocol verification and integration testing.

## Governing Question

Loads and stores suggest a uniform address space, but RAM and devices have different semantics. A RAM read is usually repeatable; a device read may consume data. A RAM write changes bytes; a device write may acknowledge an interrupt or launch work.

The interconnect must preserve each transaction through finite queues and bridges while enforcing decode, permissions, order and completion. MMIO correctness is a composition of processor memory rules, bus protocol and register behavior.

## Why This Matters

One dropped ready/valid beat can corrupt arbitrary device state. One overlapping decoder can send a secret-bearing write to two targets. One incorrect byte-enable can clear unrelated status.

Posted writes and weak memory models make intuitive program order unreliable without the documented accessors/fences. Reset, timeout and power transitions add ambiguous completion risks.

Interconnects also determine bandwidth, latency, isolation and diagnosability. Verification must cover protocol and system integration, not just each endpoint.

## Prerequisites and Retrieval

Before studying this module, be able to:

- derive address ranges, masks and local offsets;
- reason about synchronous state and ready/valid handshakes;
- distinguish architectural memory ordering from source-code order;
- apply byte masks and endianness to words;
- explain privilege, faults and basic device registers.

Retrieve address width and full map; ranges, aliases, priority and holes; initiator/target IDs and privileges; bus protocol/version/profile; channel widths and clock/reset domains; request/response fields; size/alignment/burst rules; byte strobes/endianness; outstanding depth, IDs and ordering; arbitration/QoS; posted/non-posted completion; retry/error/timeout; memory types/cacheability/speculation; bridges and width/clock conversions; register layout/access semantics/reserved behavior; side-effect event; atomic/locked operations; security firewall/IOMMU; tracing/counters; RTL/firmware/OS/driver versions and errata.

## Learning Objectives

After completing this module, you should be able to:

1. design and prove a nonoverlapping address map with local offsets;
2. trace request/response and ready/valid transfers under backpressure;
3. implement size, alignment, byte strobe and endianness behavior;
4. distinguish posted from non-posted completion and error handling;
5. specify safe MMIO register read/write side effects;
6. apply device-memory attributes and I/O ordering primitives correctly;
7. integrate arbitration, outstanding IDs, bridges and timeouts;
8. handle reset/power/security boundaries without lost transactions;
9. verify protocol, register and software-driver refinement;
10. measure latency/throughput/fairness with reproducible evidence.

## Core Exposition

### Define the address space

List every RAM, ROM, peripheral, configuration and reserved range as half-open intervals. Half-open form `[base,limit)` makes size `limit-base` and adjacency unambiguous.

State aliases and priorities explicitly. Unintentional overlap is a security and correctness defect.

### Decode one target

For each request, compute matches against enabled ranges and attributes. Require one-hot-or-zero selection, then translate `local=address-base` without truncation.

If no target matches, produce a defined error rather than arbitrary data or indefinite wait.

### Use masks cautiously

Power-of-two aligned ranges can decode with `(address & mask)==base`, but only if mask, base and size are consistent. Irregular ranges need comparisons or hierarchical decode.

Test first/last valid byte and both adjacent invalid addresses.

### Preserve request identity

A request includes more than address/data: operation, size, strobes, privilege, security, cacheability, source ID and order domain may affect behavior.

Retain all required fields through arbitration, buffering and bridges.

### Understand ready/valid

Transfer occurs when valid and ready are both asserted at the sampling edge. Valid indicates a real stable payload; ready indicates capacity to accept it.

A producer cannot pulse valid for one cycle and discard the payload when ready is low.

### Hold payload under stall

While valid is high and ready low, address/data/control remain stable unless protocol explicitly permits another mechanism. Assertions should compare consecutive stalled cycles.

The receiver must not apply side effects until the actual transfer event.

### Separate channels

Many protocols split address, write-data and response channels. Independent handshakes can arrive in different cycles and require association state.

Never assume address/data simultaneous unless the selected profile guarantees it.

### Buffer deliberately

Skid/elastic buffers break timing paths and absorb backpressure. Their occupancy/full/empty logic must conserve items during simultaneous enqueue/dequeue.

Every accepted item needs storage or a proven same-cycle consumer.

### Arbitrate initiators

Fixed priority is small/predictable but can starve low priority. Round-robin improves sharing; weighted/QoS schemes provide service classes.

Arbitration chooses among eligible requests without violating per-ID/order rules.

### Track outstanding requests

Protocols may allow multiple requests before responses. IDs/source fields and scoreboards associate completions and enforce ordering domains.

Do not recycle an ID while an earlier response or timeout-late-response ambiguity remains.

### Match responses exactly once

Every accepted non-posted request gets one terminal success/error response. Route it to the originating initiator and release tracking once.

Unknown, duplicate or late responses require containment and telemetry.

### Define posted writes

A posted write can release upstream before target-visible completion only when an intermediate buffer owns data/order/error obligations. “Posted” does not mean disposable.

Drivers may need a readback or architecture-specific barrier to ensure earlier writes reached the required point.

### Define errors

Unmapped, permission-denied, malformed, unsupported-size and target-failure cases should terminate with defined status. Decide whether faults are precise, asynchronous or logged.

Never translate an error into ordinary zero data unless the architecture explicitly defines that behavior.

### Handle timeouts

A timeout bounds waiting but creates uncertainty: the target might later act. Tag/cancel generations or reset/quarantine the path so late completion cannot double-apply or corrupt a reused ID.

Timeout policy must match side-effect idempotence and recovery ownership.

### Decode access size and alignment

Verify supported 1/2/4/8-byte sizes and address alignment. Some buses split unaligned accesses; many devices fault them.

Bridges must not invent a split that changes register side effects.

### Generate byte strobes

For an `N`-byte data word, a size-`s` access at lane offset `o` sets `s` contiguous strobes if `o+s<=N`. Payload bytes align to those lanes.

Reject crossings or split only under explicit safe rules.

### Handle endianness

Endianness maps addressed byte order to word lanes. Bridges may swap bytes and strobes together, never one without the other.

Register documentation should define byte offsets/bit fields independent of host-language struct accidents.

### Define register access types

Registers may be read/write, read-only, write-only, write-one-to-clear/set/toggle, read-clear, FIFO ports or command strobes. Each needs an exact state transition.

Reserved bits return documented values and ignore/fault writes as specified.

### Trigger side effects once

Choose side-effect event: accepted request, accepted write data, completed read response or another protocol milestone. Backpressure/replay must not repeat it.

Register logic should receive a one-cycle qualified enable derived from the handshake.

### Avoid unsafe read-modify-write

Software read-modify-write can lose asynchronous status or mishandle W1C fields. Provide dedicated set/clear aliases or use documented masks.

Hardware atomicity and driver concurrency expectations must agree.

### Treat FIFO registers specially

Reading a receive-data register may pop one entry; writing transmit data may push. Only successful qualified transfer changes pointers.

An error/retry cannot consume twice. Empty/full behavior and blocking policy are explicit.

### Apply memory types

Device/strongly ordered attributes restrict speculative reads, cache allocation, gathering and reordering. Normal-memory operations follow different rules.

Map the aperture with the required page-table and interconnect attributes end to end.

### Use accessors

OS MMIO accessors encode volatile/compiler and architecture-specific ordering/endianness behavior. Plain pointer dereference may be insufficient or undefined for device registers.

Follow platform driver APIs and their relaxed/ordered variants precisely.

### Distinguish barriers

A compiler barrier constrains compilation; a CPU memory barrier constrains architectural ordering; an I/O readback may drain posted bridges. These are not interchangeable.

State which observers and completion point a primitive orders.

### Order doorbells and descriptors

Software writes descriptors in normal memory, makes them visible with required DMA/cache/order operations, then writes an MMIO doorbell. Reversing visibility can let the device fetch stale descriptors.

Completion reads need complementary ordering before consuming device-written data.

### Handle caching and aliases

MMIO should not acquire ordinary cacheable aliases unless the platform explicitly supports coherent semantics. Multiple mappings with different memory types can be hazardous.

Firmware, page tables, IOMMU and interconnect attributes must agree.

### Bridge widths

A wide-to-narrow bridge may split one memory transfer into beats. For side-effect registers, splitting can be illegal or non-atomic.

Preserve byte strobes, ordering, error aggregation and response only after all required subtransfers.

### Cross clock domains

Asynchronous FIFOs or synchronizers transfer requests/responses across clocks. Multi-bit payloads require coherent capture, not independent bit synchronization.

Reset sequencing must avoid phantom entries and lost outstanding transactions.

### Cross protocol domains

Bridges translate channel structure, bursts, IDs, ordering and error codes. The target protocol may support fewer outstanding operations or sizes.

Reject or serialize unsupported features without weakening semantics.

### Manage bursts

Burst addresses, lengths and boundaries follow protocol rules. MMIO devices often disallow bursts or treat each beat as a separate side effect.

Never coalesce register accesses merely because addresses are adjacent.

### Support atomic operations cautiously

Some interconnects carry exclusives/atomics; many MMIO registers do not. Unsupported atomics return defined failure rather than decomposed unsafe accesses.

Atomic scope across bridges/targets must match software expectations.

### Add security firewalls

Check initiator identity, privilege, secure/nonsecure state, address and operation before forwarding. Error behavior should avoid leaking protected data.

Configuration registers themselves need protected update and reset defaults.

### Isolate faulty targets

One nonresponsive device should not block unrelated traffic indefinitely. Timeouts, per-target queues and fault containment can isolate it.

Isolation must preserve any accepted side-effect uncertainty and route a terminal upstream result.

### Handle reset

Reset register values, FIFO pointers and interrupt states are documented. Coordinate interconnect/target reset so outstanding transactions finish, abort explicitly or remain blocked before acceptance.

Never return success solely because the target reset.

### Handle power domains

Access to a powered-off target may be blocked, awakened or faulted. Isolation clamps must prevent random handshake/data values.

Power manager and software need a sequencing protocol with acknowledgment.

### Measure latency and throughput

Separate arbitration wait, bridge/queue time, target service and response return. Report distributions by initiator/target/access class.

Throughput depends on beat widths, outstanding depth and backpressure; peak bus width times frequency is only a ceiling.

### Measure fairness

Track service share, maximum wait and missed QoS deadlines under adversarial requesters. Average throughput can hide starvation.

Use exact arrival processes and downstream behavior in experiments.

### Verify protocol locally

Assert stable stalled payload, transfer conservation, bounded occupancy, legal IDs, response matching and no duplicate side effects. Use protocol checkers where available.

Cover simultaneous handshakes, full/empty transitions and every error path.

### Verify integration end to end

Generate or cross-check RTL register maps, firmware headers and human documentation from one source of truth. Run driver/device tests through actual bridges.

Use formal connectivity/decode proofs plus simulation and hardware tracing.

### Gather layered evidence

Start with executable decode/strobe examples, then block-level formal/tests, subsystem simulation, firmware/driver tests and board/silicon measurement.

Bind protocol/profile, RTL, register-map revision, firmware/OS/driver, clock/reset/power topology and errata.

## Definitions and Notation

- `[base,limit)`: half-open aperture; size is `limit-base`.
- `decode(a)`: unique target and `offset=a-base`, or defined error.
- `N`: data-bus bytes per beat.
- `s`: access bytes; `o=a mod N` is lane offset.
- `strobe=((1<<s)-1)<<o` when `o+s<=N`.
- `valid`, `ready`: handshake signals; transfer is `valid and ready` at sampling edge.
- `q`: retained request tuple including address, operation, size, data/mask, attributes, ID and order domain.
- `outstanding`: accepted requests lacking terminal response under the protocol.
- `posted_complete(q)`: documented point where upstream may release while an intermediary owns remaining obligation.
- `latency=response_time-accept_time` under named endpoints.
- `throughput=completed_payload/time` under sustained conditions.
- `onehot0(matches)`: zero or one selected target; zero follows error policy.

Protocols use different channel names and completion rules. Map these abstract terms to the exact selected specification/profile.

## Mechanisms, Invariants, or Proof Structure

1. **Decode obligation:** every access yields exactly one authorized target/local offset or one defined error.
2. **Range obligation:** first/last boundaries, holes, aliases and overlaps match the governed map.
3. **Handshake obligation:** stalled valid payload is stable and transfer occurs exactly on the defined handshake.
4. **Conservation obligation:** each accepted request/response occupies retained state until one consumption.
5. **Identity obligation:** IDs/source/order/privilege remain attached through arbitration and bridges.
6. **Lane obligation:** size, alignment, endianness, payload and strobes affect exactly addressed bytes.
7. **Side-effect obligation:** each qualified register effect occurs exactly once.
8. **Response obligation:** every non-posted acceptance receives one matching terminal success/error.
9. **Posted obligation:** early completion transfers data/order/error ownership to sufficient buffering.
10. **Ordering obligation:** memory attributes, barriers, atomics and device rules constrain observation.
11. **Security obligation:** denied accesses cannot read/change protected state or bypass via alias/bridge.
12. **Lifecycle obligation:** reset/power/clock transitions cannot invent, duplicate or silently lose transactions.
13. **Progress obligation:** arbitration/backpressure cycles are broken under stated fairness.
14. **Software obligation:** accessors/register definitions/order sequences match hardware semantics.
15. **Evidence obligation:** claims bind map, protocol/profile, revisions, clocks and workloads.

Prove local handshake conservation and register state transitions, then compose them through decoders, arbiters and bridges using request/response ownership. End-to-end refinement maps qualified MMIO operations to architectural device effects. Liveness depends on fairness and target-response assumptions; performance follows only after safety.

## Alternatives and Trade-Offs

1. **Shared bus versus switched fabric:** buses are compact; fabrics scale concurrency/routing.
2. **Central versus distributed decode:** central maps globally; distributed decode eases hierarchy but needs overlap proof.
3. **Fixed versus round-robin arbitration:** fixed gives priority; round-robin bounds ordinary starvation.
4. **In-order versus IDs/out-of-order:** in-order simplifies matching; IDs expose concurrency.
5. **Posted versus non-posted writes:** posting hides latency; non-posted completion simplifies error/visibility.
6. **Deep versus shallow buffers:** deep absorbs bursts; shallow bounds state/latency and simplifies reset.
7. **Wide versus narrow buses:** wide raises payload/cycle; narrow reduces wires and may split side effects.
8. **Separate versus combined channels:** separation improves concurrency; combined protocols simplify state.
9. **Strict versus relaxed device accessors:** strict ordering is safe/easy; relaxed forms improve performance with proof burden.
10. **Native versus fixed peripheral endianness:** native eases CPU integration; fixed makes device ABI portable.
11. **Fault versus zero/default on holes:** faults expose errors; defaults can simplify probing but hide bugs.
12. **Timeout versus unbounded wait:** timeout contains stalls; it creates late-side-effect ambiguity.
13. **Generated versus handwritten maps:** generation aligns artifacts; handwritten maps can be direct but drift.
14. **Wake versus fault powered-off access:** wake is convenient; faulting makes latency/state explicit.
15. **Formal protocol proofs versus simulation only:** formal covers stalls/interleavings; simulation handles system/software realism.

## Failure Modes and Misconceptions

1. “Address ranges may share a boundary byte.” Half-open adjacency avoids overlap.
2. “Truncating high address bits forms a safe offset.” It can alias outside the aperture.
3. “Decoder priority resolves unintended overlap.” It hides integration errors and security ambiguity.
4. “Valid is a one-cycle pulse.” It must persist with stable payload until acceptance under ready/valid.
5. “Ready can accept without valid.” No transfer exists without both.
6. “Stalled cycles may update a register.” Only qualified transfer triggers effects.
7. “Address and write data always handshake together.” Split-channel protocols decouple them.
8. “A buffer can accept when full if downstream might move.” Simultaneous behavior must be proven from actual handshakes.
9. “IDs are only performance tags.” They preserve response ownership/order.
10. “Posted means completed at device.” It means remaining obligation is owned downstream.
11. “Reading after writing always drains the write.” Only documented path/order/readback guarantees do.
12. “MMIO is ordinary volatile RAM.” Device attributes and side effects differ.
13. “volatile is a hardware barrier.” It mainly constrains compiler behavior, not all CPU/interconnect order.
14. “A compiler barrier orders devices.” Architectural I/O ordering primitives are required.
15. “A 32-bit write ignores byte strobes.” Strobes may control each lane and side effect.
16. “Endianness swaps data but not strobes.” Lane enables must follow addressed bytes too.
17. “Read-modify-write is safe for W1C status.” It can clear newly asserted bits.
18. “Retrying a FIFO read is harmless.” It may pop twice unless side effect is exactly-once.
19. “A timeout proves no device effect occurred.” The target may complete late without cancellation.
20. “Returning zero for holes is safer.” It can hide wrong addresses and fabricate success.
21. “Bursts are valid for adjacent registers.” Each beat may have independent side effects.
22. “Width conversion preserves atomicity automatically.” Splitting can expose partial state.
23. “Reset clears protocol obligations.” Upstream may still expect responses.
24. “Fixed priority is fine if low-priority traffic is rare.” Continuous high-priority load can starve it.
25. “Peak width times clock is measured throughput.” Backpressure/protocol/target service reduce it.
26. “Block-level tests prove firmware compatibility.” Maps, accessors and ordering must match end to end.

## Worked Examples

### Example 1

Range `[0x10000000,0x10001000)` includes offset `0xfff` but rejects address `0x10001000`, which may begin the adjacent timer.

### Example 2

With valid high and ready low for three cycles, address/data/strobes stay unchanged; one transfer occurs only when ready rises.

### Example 3

A four-byte bus writes two bytes at address lane offset 2, producing strobe `0b1100`; offset 3 with size two crosses and is rejected/safely split by policy.

### Example 4

A W1C interrupt status register receives write data bit 3=1 on a qualified transfer and clears only status bit 3.

### Example 5

A FIFO read response is accepted once; the dequeue occurs at the defined request/response event and a stalled channel cannot pop repeatedly.

### Example 6

A posted bridge accepts a doorbell write, retains it, then software performs the documented drain before assuming the device observed it.

### Example 7

An unmapped load receives a bus error tied to its source ID; returning zero would make a bad driver address appear valid.

### Example 8

A timed-out command later responds with an old generation. The bridge discards/records it and cannot attach it to a reused ID.

### Example 9

Descriptor writes become visible to a DMA device before the MMIO doorbell through the architecture/platform's required ordering sequence.

### Example 10

This deterministic map model audits half-open decode overlap, local offsets and byte strobes.

<!-- bijux-verify: {"id":"mmio-decode-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"ranges=3 overlaps=0\naddress=0x10000004 target=uart offset=0x004 size=4 strobe=0xf\naddress=0x10001002 target=timer offset=0x002 size=2 strobe=0xc\naddress=0x10001001 target=timer offset=0x001 size=1 strobe=0x2\naddress=0x20000000 target=error\n"}} -->
```python
ranges = [
    ("ram", 0x00000000, 0x00100000),
    ("uart", 0x10000000, 0x10001000),
    ("timer", 0x10001000, 0x10002000),
]

overlaps = 0
for left_index, (_, left_base, left_limit) in enumerate(ranges):
    for _, right_base, right_limit in ranges[left_index + 1:]:
        if max(left_base, right_base) < min(left_limit, right_limit):
            overlaps += 1

def decode(address):
    matches = [(name, address - base) for name, base, limit in ranges if base <= address < limit]
    return matches[0] if len(matches) == 1 else ("error", None)

def strobe(address, size, bus_bytes=4):
    offset = address % bus_bytes
    if size not in (1, 2, 4) or offset + size > bus_bytes:
        return None
    return ((1 << size) - 1) << offset

print(f"ranges={len(ranges)} overlaps={overlaps}")
for address, size in [(0x10000004, 4), (0x10001002, 2), (0x10001001, 1), (0x20000000, 4)]:
    target, offset = decode(address)
    if target == "error":
        print(f"address=0x{address:08x} target=error")
    else:
        print(f"address=0x{address:08x} target={target} offset=0x{offset:03x} size={size} strobe=0x{strobe(address, size):x}")
```

The map and access widths are invented. The model checks direct half-open ranges and one 32-bit little-lane strobe convention; it omits timing, IDs, bursts, permissions, endianness bridges and side effects.

## Cross-Program Connections

- **Digital Design:** ready/valid, buffers, arbitration and clock-domain crossing implement transport.
- **Operating Systems:** MMIO mappings, accessors and barriers encode architecture/platform rules.
- **Concurrent Systems:** outstanding transactions, ordering and backpressure require safety/progress.
- **Security Engineering:** decode/firewalls/aliases protect device and memory apertures.
- **API Engineering:** register maps are hardware-software APIs with versioned semantics.
- **Reliability Engineering:** timeout, reset, power and error containment preserve diagnosability.
- **Performance Engineering:** queueing, outstanding depth, throughput and fairness expose interconnect behavior.
- **Formal Methods:** one-hot decode, conservation and exactly-once side effects support proofs.

## References

1. RISC-V International, [RVWMO Memory Consistency Model](https://docs.riscv.org/reference/isa/unpriv/rvwmo.html), current ordering and fence context for loads/stores and I/O; retrieved 2026-09-04.
2. RISC-V International, [Machine-Level ISA](https://docs.riscv.org/reference/isa/priv/machine.html), current physical-memory attributes, privilege and trap context; retrieved 2026-09-04.
3. OpenTitan, [TL-UL](https://opentitan.org/book/hw/ip/tlul/), current open interconnect protocol, integrity and adapter documentation; retrieved 2026-09-04.
4. Linux kernel, [Bus-Independent Device Accesses](https://docs.kernel.org/driver-api/device-io.html), current MMIO mapping/accessor and ordering guidance; retrieved 2026-09-04.
5. Linux kernel, [Memory Barriers](https://docs.kernel.org/core-api/wrappers/memory-barriers.html), current compiler/CPU/device ordering guidance; retrieved 2026-09-04.
6. Arm, [AMBA Architectures](https://developer.arm.com/Architectures/AMBA), current interconnect protocol family and specification context; retrieved 2026-09-04.
7. Sarah L. Harris and David Money Harris, [Digital Design and Computer Architecture: RISC-V Edition Resources](https://pages.hmc.edu/harris/ddca/ddcarv.html), bus/MMIO teaching resources; retrieved 2026-09-04.

## Exercises

### Exercise 1

Design a nonoverlapping address map with RAM, ROM and five peripherals, then prove boundary decode and local-offset round trips.

### Exercise 2

Trace a ready/valid request and response through a one-entry elastic buffer under arbitrary backpressure, including simultaneous enqueue/dequeue.

### Exercise 3

Specify a register block containing RW, RO, W1C, read-clear, FIFO and command registers with byte-write behavior.

### Exercise 4

Extend the executable decoder with privileges, endian conversion, width splitting and terminal error responses.

### Exercise 5

Write an end-to-end verification plan for an MMIO device behind arbiters, a clock crossing and a protocol bridge, including firmware-driver tests.

## Answers to the Exercises

### Answer 1

Represent every aperture as `[base,limit)` and assert base<limit, architectural bounds and pairwise nonoverlap unless an alias/priority is intentional. For representative and boundary addresses, require one-hot-or-zero matches; valid decode returns `offset=address-base` with `0<=offset<size` and reconstructs `base+offset=address`.

Test one byte below/at base, last byte, limit and one byte above, plus high-bit variants that would alias if truncated. Holes produce the chosen error.

### Answer 2

The buffer stores payload and full bit. Input ready is true when empty or a same-cycle output transfer frees space; output valid mirrors full and output payload is stored. On input transfer without output, fill; output without input, empty; both transfer replaces old with new; neither holds state.

Assert stalled output payload stability, occupancy in {0,1}, accepted-consumed count equals occupancy, ordering and no duplication. Reset either occurs only quiescent or explicitly terminates upstream obligations.

### Answer 3

Define address, width/reset, readable/writable bits, strobes, reserved behavior and exact side-effect event per register. RW merges selected lanes; RO ignores/faults writes; W1C clears only written-one enabled bits; read-clear changes once on qualified read; FIFO pops/pushes once; command launches once and exposes busy/error.

Avoid software RMW for asynchronous W1C status. Generate RTL, headers and documentation from one schema where possible and test every lane, stall, retry and illegal size.

### Answer 4

Add each range's read/write privilege and endian attribute. Decode produces denied/unmapped/misaligned terminal errors. Swap payload bytes and strobes together for opposite endian. For wide-to-narrow access, prevalidate every subtransfer and reject side-effect registers that do not permit splitting; aggregate one response only after all safe beats.

Tag subrequests with parent ID/generation, preserve order and stop/contain errors without reapplying completed side effects. Assertions conserve parent/child operations and exact bytes.

### Answer 5

Prove decoder range/security one-hot behavior, arbitration fairness, ready/valid stability/conservation, IDs/responses, byte/size/endian semantics, bridge feature restrictions, CDC FIFO correctness, reset/power behavior, timeout generations and exactly-once register effects. Use protocol checkers, formal assertions and error/backpressure injection.

Cross-check generated RTL/map/docs/headers, then run firmware access, ordering/doorbell, FIFO, interrupt, denial, error and recovery tests through the real topology. Measure latency/throughput/tails/fairness under contention, binding protocol/profile, map/RTL, clocks/resets/power, firmware/OS/driver and errata. Internal evidence is not external protocol, security or silicon certification.
