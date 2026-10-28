---
module_id: OS-062
program: Operating Systems
level: 2
module_number: 62
title: Memory-Mapped and Port-Mapped I/O
status: complete
last_verified: 2026-09-04
---

# Memory-Mapped and Port-Mapped I/O

## One-Page Review

### Governing question

How should an operating system claim a device's register resources, map the correct address space, perform width-, endian-, and ordering-correct accesses, coordinate concurrent CPUs and device state, and tear the mapping down without treating device registers as ordinary memory?

### Essential definitions

- **Memory-mapped I/O (MMIO)** places device registers in a physical address range reached with load/store-like operations but governed by device-memory semantics.
- **Port-mapped I/O (PMIO)** uses a distinct I/O address space and dedicated input/output instructions or operating-system accessors.
- A **resource range** is an address interval assigned to a device and reserved against conflicting ownership.
- An **I/O mapping** establishes a kernel virtual token for an MMIO resource with architecture-appropriate attributes.
- An **accessor** is an operating-system operation such as `readl()` or `writel()` that expresses device access width, ordering, and representation requirements.
- An **I/O memory token** is an annotated handle, commonly `__iomem` in Linux, that must be used through I/O accessors rather than ordinary dereference.
- A **posted write** is accepted by a CPU or bridge before it has reached the target device; a later safe read can be used to drain it where the device contract permits.
- A **device barrier** constrains ordering visible to a device; it is distinct from compiler ordering, CPU-to-CPU memory ordering, and DMA ownership synchronization.
- A **register contract** defines width, offset, byte order, access type, valid bits, reset value, side effects, and ordering for one register.
- A **destructive read** changes device state by reading, as with read-to-clear status or FIFO consumption.

### Central model, mechanism, or theorem

Treat every register operation as a typed protocol event, not as an ordinary memory access. Correctness requires the conjunction

$$
C = O \land L \land W \land E \land S \land R \land P,
$$

where $O$ is valid ownership of the resource, $L$ is a live mapping and device, $W$ is the required access width and alignment, $E$ is correct device byte order, $S$ is the register's side-effect and bit semantics, $R$ is the required CPU, compiler, device, and DMA ordering, and $P$ is the required power/reset state. Failure of any term makes a syntactically valid access unsafe or meaningless.

The durable lifecycle is `discover -> reserve -> map -> configure -> publish -> operate -> stop arrivals -> quiesce -> unmap -> release`. Publication occurs only after the register interface is usable. Teardown removes reachability and drains interrupts, workers, polling, DMA, and peer CPUs before unmapping. Accessors preserve the architecture's I/O semantics; locks preserve software invariants; neither substitutes for the other.

### Critical invariants

- A driver accesses only resources assigned to its device and reserved for its ownership interval.
- The mapping type, cacheability, width, alignment, and byte order match the platform and device register contract.
- Device registers are reached through approved I/O accessors, never through ordinary pointer dereference or generic memory-copy routines.
- Reserved bits retain required values, and destructive, write-one, command, FIFO, and doorbell semantics are never treated as plain read-write storage.
- Required writes become visible before dependent device actions, and posted writes are drained before ownership or lifecycle transitions that assume completion.
- Shared register sequences are serialized at the semantic operation boundary, including interrupt and peer-CPU paths.
- No accessor runs while the device is unpowered, held in reset, surprise-removed, or after its mapping has been revoked.
- Mapping teardown follows cancellation and synchronization of every path that can still use the token.

### Common failures

Common mistakes are mapping without reserving, confusing CPU physical and bus addresses, deriving a virtual address by arithmetic, directly dereferencing `__iomem`, using `volatile` as an ordering primitive, assuming every register is little-endian, issuing the wrong access width, copying register blocks with `memcpy`, byte-swapping FIFO repeat accesses incorrectly, using read-modify-write on write-one-to-clear status, touching a destructive register for logging, assuming a spinlock flushes posted writes, using a normal memory barrier where an I/O readback is required, polling forever, accessing a suspended or removed device, unmapping before callbacks drain, and exposing raw port or MMIO access to untrusted userspace.

### Compact example

A driver must set `ENABLE` and a two-bit `MODE` while preserving reserved bits in an ordinary read-write little-endian control register. It masks only documented writable fields, encodes the value as little-endian, and writes with the required 32-bit accessor. This calculation is correct only if the register is genuinely read-write and a lock protects the read-modify-write sequence; it would be wrong for a write-one-to-clear or command register.

### Connections

[OS-004](004-interrupts-and-exceptions.md), [OS-021](021-critical-sections-in-the-kernel.md), [OS-024](024-atomic-operations.md), [OS-054](054-kernel-read-copy-update.md), [OS-061](061-device-discovery-and-driver-models.md), and [OS-063](../ROADMAP.md) connect register access to interrupts, synchronization, lifetime, device ownership, and DMA.

## Governing Question

Device register access looks deceptively simple. A CPU loads from an address or stores a value, and hardware responds. Between those two events lie firmware descriptions, bus address translation, resource arbitration, page-table attributes, compiler behavior, CPU ordering, interconnect posting, bridge conversion, device byte order, register side effects, power state, and concurrent execution.

The governing question is therefore not merely which address to use. It is how the kernel establishes authority for the range, represents the access so every layer applies the correct semantics, orders operations across all relevant observers, and withdraws access safely during failure and removal.

## Why This Matters

An incorrect ordinary-memory access usually damages memory owned by software. An incorrect device access can acknowledge an interrupt that was not handled, launch DMA to an attacker-controlled address, reset a controller, consume a FIFO entry, wedge a bus, or silently configure the wrong hardware function.

Register bugs are often timing-sensitive. They may disappear under a debugger because an extra status read drains posted writes, occur only on a weakly ordered architecture, or surface only when two CPUs share a device. Code that works on one x86 development machine can be invalid on another architecture or behind a different bridge.

The kernel's resource, mapping, accessor, barrier, and lifecycle APIs encode hard-won platform knowledge. Using them is not stylistic ceremony. It preserves portability, makes static checking possible, and gives reviewers a vocabulary for proving that a hardware transaction is safe.

## Prerequisites and Retrieval

Review [OS-002](002-privilege-levels-and-protection-rings.md), [OS-004](004-interrupts-and-exceptions.md), [OS-007](007-kernel-data-structures.md), [OS-009](009-kernel-modules-and-drivers.md), [OS-021](021-critical-sections-in-the-kernel.md), [OS-022](022-spinlocks-and-interrupt-context.md), [OS-024](024-atomic-operations.md), [OS-031](031-address-translation.md), [OS-032](032-page-tables.md), [OS-052](052-smp-kernel-synchronization.md), [OS-054](054-kernel-read-copy-update.md), and [OS-061](061-device-discovery-and-driver-models.md).

Retrieve these distinctions:

- a device-reported bus address, a host physical address, and a CPU virtual address are different names in potentially different translation domains;
- ordinary RAM, persistent memory, MMIO, configuration space, and I/O-port space have different access semantics;
- compiler ordering, CPU-to-CPU memory ordering, device-register ordering, DMA ownership, and completion at the device are separate claims;
- mutual exclusion protects software state and sequences, but it need not drain a posted interconnect write;
- byte order, access width, alignment, and register side effects are parts of an interface contract;
- a live object reference does not prove the hardware is powered, present, or accessible;
- graceful removal and surprise disappearance offer different opportunities for device acknowledgement;
- a mapping creates a qualified access token, not ordinary memory.

## Learning Objectives

After this module, you should be able to:

1. distinguish system memory, MMIO, port I/O, configuration space, CPU physical addresses, bus addresses, and kernel virtual mappings;
2. trace resource discovery, reservation, mapping, use, unmapping, and release for a device register window;
3. select accessors by width, byte order, ordering strength, FIFO behavior, and architecture support;
4. reason about compiler, CPU, device, interconnect, and DMA ordering without conflating barriers and readback;
5. classify register semantics and avoid destructive reads, invalid read-modify-write, and reserved-bit corruption;
6. design polling, interrupt, power, reset, hotplug, and concurrent access paths around one explicit lifecycle;
7. test register interfaces with emulation, tracing, fault injection, static analysis, hardware evidence, and bounded claims.

## Core Exposition

### Begin with the device contract

A register map is a protocol specification. For every offset record the legal widths, alignment, endianness, readable and writable bits, reset value, access class, side effects, ordering dependencies, power requirements, and concurrency rules. Record whether an absent device returns a sentinel value or faults.

Do not infer semantics from a C type or a register name. Two adjacent 32-bit registers can require opposite access ordering; a field called `status` can be read-only, read-to-clear, or write-one-to-clear depending on the device.

### Discover resources through the bus

Firmware, a bus enumerator, or a parent device supplies register resources. PCI base address registers, platform resources, and firmware descriptors have bus-specific meaning and can be translated by host bridges.

The driver consumes the resource published for its device. It does not scan arbitrary physical space or copy a literal address from one machine. Discovery establishes the authoritative start, length, flags, and ownership context.

### Reserve before access

Reservation claims a range so conflicting drivers cannot control it simultaneously. It also exposes overlaps and malformed descriptions before the first hardware access.

Mapping without reservation can appear to work until another driver binds or firmware assigns an overlapping window. Combined helpers can request and map a resource transactionally, but reviewers should still identify both obligations.

### Address domains

Let $a_b$ be a device or bus address, $a_p$ a host physical address, and $a_v$ a kernel virtual token. A platform may implement translations

$$
a_p = T_{bp}(a_b), \qquad a_v = T_{pv}(a_p, \text{attributes}).
$$

Neither transformation is necessarily identity. An IOMMU introduces yet another translation for device DMA and does not make the CPU's MMIO mapping usable by the device.

### System RAM is not MMIO

Ordinary RAM tolerates caching, speculation, merging, and generic loads and stores according to the memory model. MMIO represents external effects. Reads can consume data, and writes can launch operations.

The mapping must use architecture-approved device attributes. Mapping device registers through an ordinary cached RAM alias can hide updates, combine writes, reorder effects, or create conflicting aliases with undefined coherence.

### Map the resource

On Linux, `ioremap()` and bus- or subsystem-specific wrappers create an I/O mapping. The result is an `__iomem` token used with I/O accessors. A mapping failure is handled before any register access or interface publication.

Prefer helpers that combine resource lookup, reservation, mapping, and device-managed cleanup when their lifetime matches the driver. Explicit teardown remains necessary for semantic quiescence before the mapping is released.

### Mapping lifetime

The mapping becomes usable after successful creation and remains valid only while its resource, device, power state, and owning object permit access. Store it in per-device state, not in an unscoped global.

During removal, first block new operations, stop hardware production, synchronize interrupts and work, and resolve DMA. Only then unmap and release the range. A dangling mapping token is as dangerous as a freed pointer, with hardware effects added.

### `__iomem` as a semantic token

Linux annotates I/O address-space pointers with `__iomem`. Sparse can diagnose accidental mixing with normal pointers and direct dereferences. The annotation has value because it makes a semantic boundary visible to tools and reviewers.

Casts that erase the annotation also erase evidence. An accessor accepts the token and gives the architecture a place to implement the required instruction, conversion, and ordering.

### Access width and alignment

Use the width required by the register: byte, 16-bit, 32-bit, or 64-bit. A device may reject narrower cycles, combine them differently, or treat them as access to different lanes.

Alignment follows both architecture and device rules. Never assume that a compiler-generated unaligned access will become the one bus transaction the device expects.

### Base accessors

Linux provides families such as `readb()`, `readw()`, `readl()`, and where supported `readq()`, with corresponding writes. `ioread*()` and `iowrite*()` can abstract over certain MMIO and port mappings.

Choose the documented interface for the bus and subsystem. Do not replace an accessor with `*(volatile u32 *)base`; `volatile` constrains some compiler transformations but does not select device attributes, byte order, bus instructions, or complete ordering semantics.

### Byte order

The register specification defines byte order independently of the CPU. Standard accessors have defined conventions; explicit big-endian variants such as `ioread32be()` express a big-endian register file.

Convert exactly once. A value should be interpreted as a host integer in software and encoded or decoded at the device boundary. Double conversion often survives same-endian testing and fails on another platform.

### Sixty-four-bit registers

Some 32-bit systems cannot perform one atomic 64-bit MMIO transaction. A device may require low word then high word, high then low, a latch read, or another protocol.

Use the ordered split-access helper defined for that device when available. Two arbitrary 32-bit reads can combine halves from different device updates; two arbitrary writes can momentarily command an invalid value.

### Ordered, relaxed, and raw access

Normal accessors provide a documented portable ordering envelope. Relaxed accessors weaken some ordering and are appropriate only when surrounding protocol establishes what the omitted ordering is not needed for.

Raw accessors provide even less conversion or ordering and are commonly useful for carefully specified streams. Their names are warnings, not performance recommendations. Every relaxed or raw use needs a local explanation tied to the device contract.

### FIFO and repeated accessors

FIFO data ports require repeated transfers at one register offset. Repeat helpers such as `ioread32_rep()` perform a sequence without incrementing the device address and have byte-stream conventions distinct from scalar register conversion.

Generic `memcpy()` increments ordinary addresses and applies no I/O semantics. A loop using the wrong endian-converting scalar accessor can also corrupt an intended byte stream.

### Register semantic classes

Classify registers as read-only, write-only, ordinary read-write, write-one-to-clear, write-one-to-set, read-to-clear, command, status, FIFO, doorbell, snapshot, latch, or mixed-field. Mixed registers require field-level analysis.

Code generation and review can use this classification to forbid illegal reads or writes. Diagnostic tooling must obey it too: dumping every offset can itself acknowledge events or consume data.

### Reserved bits

Specifications commonly require reserved bits to remain zero, retain their previous values, or be written with a documented reset value. Future device revisions may assign meaning to them.

Construct writes from named masks. Use read-modify-write only when reads are safe, the register is ordinary read-write, concurrent agents cannot change relevant fields, and the device permits the sequence.

### Read-modify-write hazards

Suppose status bit 3 is write-one-to-clear. Reading `00001000`, OR-ing a control bit, and writing the result clears bit 3 unintentionally. If hardware asserts another bit between read and write, software can also lose the event.

Prefer dedicated set, clear, mask, and acknowledge registers. If an ordinary control register must be shared, serialize access and maintain a software shadow only when the specification makes that shadow authoritative.

### Command and doorbell registers

A command or doorbell write is an event, not stored state. Repeating it after an uncertain failure can duplicate work. Reading it may be undefined.

Define command identifiers, queue ownership, completion evidence, timeout behavior, and reset recovery. Ensure descriptor and DMA writes are visible before ringing the doorbell.

### Destructive reads

Read-to-clear status, FIFO ports, event counters, and snapshot latches change the device when read. Logging, health checks, and tracing cannot inspect them casually.

One path should own destructive consumption and distribute a software representation to other consumers. Capture who read, when, in which lifecycle state, and what follow-up acknowledgement occurred.

### Compiler ordering

The compiler can reorder or remove ordinary memory operations when the language model permits. Accessor and barrier APIs provide compiler-visible constraints, while plain `volatile` applies only to accesses through that qualified object.

Compiler ordering is necessary but insufficient. The CPU, cache system, host bridge, and device can still observe a different order unless the architecture and accessor contract constrain them.

### CPU memory ordering

Locks and memory barriers order ordinary shared-memory communication according to the architecture's memory model. They establish relations between CPUs and can participate in preparing descriptors consumed by a device.

Do not infer device completion from a CPU ordering relation. A barrier can ensure one write is issued before another without proving that the first reached the peripheral.

### Device I/O ordering

The accessor family defines ordering relative to prior or subsequent operations within its documented scope. Weakly ordered mappings and relaxed accessors require explicit reasoning.

Write the protocol as a partial order: initialize data before publishing ownership, configure before enable, acknowledge before unmask where required, and stop before freeing backing state. Then map each edge to the API that enforces it.

### Posted writes

PCI and other interconnects can post a write: the CPU completes the instruction while a bridge still holds the transaction. Releasing a spinlock can therefore let the next CPU enter before the device has observed the prior owner's final write.

Where the hardware and bus specify it, read a safe register on the same device after the write to flush posted transactions. The read target must be valid in the current state and free of destructive side effects. During reset, a bridge-level safe read may be required instead.

### Locks and posted writes

A lock serializes software entry and orders ordinary shared state. It does not universally force an interconnect queue to drain. If device-visible serialization requires completion, perform the defined readback before unlocking.

Conversely, readback does not protect a multi-operation software invariant from a competing CPU. Many protocols require both a lock and device-specific completion evidence.

### DMA ordering boundary

MMIO often coordinates DMA: software fills descriptors in memory, transfers ownership, and writes a doorbell. Mapping a register says nothing about the device's view of descriptor memory.

Use the DMA API for allocation, mapping, synchronization, and ownership, and use the required DMA barrier before notification. OS-063 develops this contract. Never substitute a generic MMIO accessor for DMA synchronization.

### Port-mapped I/O

Some architectures, especially x86, expose a separate I/O-port address space reached by instructions such as `in` and `out`. Kernel port accessors preserve this distinction and can include delayed variants for legacy hardware.

A port number is not a physical memory address and cannot be passed to `ioremap()` as though the spaces were interchangeable. On systems without distinct port instructions, platform abstractions may translate port space through MMIO.

### Userspace port access

Linux interfaces such as `ioperm()` and `iopl()` are architecture- and privilege-sensitive and expose powerful direct hardware access. Input/output helpers may require optimization settings and architecture-specific headers.

Direct userspace access bypasses normal driver arbitration, lifecycle, auditing, and policy. Prefer a kernel subsystem interface with narrow operations. Grant raw access only for a justified trusted component and reserved resources.

### PCI register mapping

PCI base address registers can describe memory or I/O space. Use PCI resource and mapping helpers so the kernel handles address translation, reservation, mapping type, and teardown consistently.

Do not assume BAR zero is MMIO, that its value is a directly dereferenceable address, or that all functions implement the same layout. Enable the device and validate selected regions in the bus-defined order.

### Cacheability and mapping aliases

Register windows normally require device or uncached attributes, while framebuffer-like apertures may permit write combining under explicit rules. The bus and architecture decide which mapping helper is valid.

Avoid mapping one physical range simultaneously with incompatible attributes. Alias-induced behavior can evade software synchronization and differ across CPU models.

### Polling

Polling is suitable for bounded initialization, short transitions, or contexts where interrupts are unavailable. Every loop needs a deadline, appropriate delay or relaxation, a device-presence check, and a defined timeout path.

Select sleepable polling in process context and atomic polling only when the context requires it. A tight infinite loop can monopolize a CPU, saturate an interconnect, and prevent the completion path it awaits.

### Interrupt interaction

An interrupt handler and process context can share registers. Specify which path owns status consumption, acknowledgement, masking, and configuration, then choose locks safe for both contexts.

Masking the device and synchronizing the interrupt at teardown are separate steps: the first stops new generation, while the second waits for handlers already dispatched. Posted writes can affect the mask's observed timing.

### Multi-CPU register access

Per-register atomicity does not make a multi-register protocol atomic. Two CPUs can interleave bank selection and data access, command composition, or read-modify-write even when each bus operation is indivisible.

Lock at the semantic transaction boundary. Document interrupt-disable, sleeping, and lock-order constraints, and avoid holding a spinlock across unbounded polling.

### Power and reset state

Registers can be inaccessible, return reset values, or fault when clocks or power domains are off. Runtime power references and supplier links make the legal access interval explicit.

Reset can invalidate cached configuration and in-flight commands. Quiesce users, execute the specified reset ordering, wait with a bound, restore authoritative state, and only then republish readiness.

### Hotplug and surprise loss

Graceful removal lets the driver stop arrivals, quiesce hardware, drain asynchronous work, and unmap. Surprise removal begins with the device already inaccessible, so register reads used for acknowledgement or flush may be unsafe.

Maintain a disconnected state checked before operations, contain DMA through the bus and IOMMU, complete users with errors, and synchronize software callbacks. Treat all-ones reads or bus errors according to bus-specific removal semantics, not as universally valid register values.

### Virtual devices

A hypervisor can emulate MMIO and port I/O. Every access can cause a costly exit, and repeated polling can become a denial of service. Batched or paravirtual interfaces can reduce traps.

Emulation is also an adversarial input boundary. Validate register offsets, widths, transitions, queue indices, and command rates on both guest-driver and device-model sides.

### Observability

Useful evidence includes the authoritative resource range, mapping helper and attributes, register specification revision, access width and endian path, CPU and context, lifecycle generation, power state, command identifier, timeout, interrupt state, and errors.

Avoid logging secrets, raw credentials, or every destructive access. Tracepoints should observe a software copy when reading the device would alter it.

### Verification strategy

Static analysis checks address-space annotations and illegal pointer mixing. Unit models check masks, endian conversion, state transitions, and timeouts. Emulation exercises register protocols and malformed operations. Hardware tests cover architecture, bridge, revision, power, reset, and hotplug behavior.

Inject mapping failure, absent device, stuck status, delayed posted write, concurrent interrupt, reset, removal, and every timeout. Preserve traces and negative results. Passing on one system is evidence for that configuration, not proof of portability.

## Definitions and Notation

Let a resource be $r=(b, n, k, o)$, where $b$ is base, $n$ length, $k$ address-space kind, and $o$ owner. Let a mapping be $m=(r, v, a, \ell)$, with virtual token $v$, attributes $a$, and live state $\ell$. An access is

$$
x=(m, d, w, e, q, s),
$$

where $d$ is offset, $w$ width, $e$ endian rule, $q$ ordering strength, and $s$ register semantics. It is well formed only if $0 \le d$, $d+w/8 \le n$, alignment is valid, $m.\ell=\text{live}$, and all fields match the register contract.

For a write protocol, use $A \prec B$ to mean the device must observe event $A$ before event $B$. For example,

$$
\text{descriptor writes} \prec \text{DMA ownership} \prec \text{doorbell}.
$$

A readback edge `write -> safe read complete` is stronger than mere program order when it is the documented mechanism for draining posted writes.

The lifecycle state $L$ belongs to `{absent, reserved, mapped, initializing, active, quiescing, disconnected, unmapped, released}`. An object reference can keep software storage alive but cannot move $L$ backward or make hardware present.

## Mechanisms, Invariants, or Proof Structure

A reviewable register-I/O design discharges these obligations:

1. **Authority:** derive each resource from the bus or firmware description for the matched device.
2. **Exclusivity:** reserve the complete range and reject overlap before first access.
3. **Translation:** use bus and mapping APIs rather than assuming bus, physical, and virtual identity.
4. **Typing:** retain the I/O token and use an accessor whose width and architecture contract fit.
5. **Representation:** apply the device's endian rule exactly once at the boundary.
6. **Semantics:** classify each field and forbid illegal reads, writes, and read-modify-write sequences.
7. **Ordering:** enumerate required compiler, CPU, DMA, I/O, and completion edges separately.
8. **Concurrency:** serialize every multi-access transaction across process, interrupt, and peer-CPU paths.
9. **State:** prove power, clock, reset, presence, and mapping are valid at every access site.
10. **Progress:** bound polling and retry, and define recovery or escalation for timeout.
11. **Revocation:** block new access and drain every asynchronous user before unmapping.
12. **Evidence:** test masks, ordering assumptions, faults, architectures, revisions, and lifecycle races with scoped claims.

The key proof separation is intentional. Reservation proves ownership, not readiness. An accessor proves a qualified operation, not a legal register state. A lock proves exclusion, not posted-write completion. A barrier proves only its documented ordering relation. A reference proves storage lifetime, not device presence. Correctness requires all obligations together.

## Alternatives and Trade-Offs

- **MMIO versus PMIO:** MMIO fits load/store machines and large spaces; PMIO preserves a distinct legacy space but is architecture-specific and instruction-constrained.
- **Explicit versus managed mapping:** explicit cleanup makes lifecycle visible; managed helpers reduce leaks but still require explicit quiescence.
- **Normal versus relaxed accessors:** normal accessors offer a stronger portable contract; relaxed access can reduce barriers when a proved protocol permits it.
- **Scalar versus repeated accessors:** scalar access fits registers; repeated access preserves a fixed FIFO port and byte-stream conventions.
- **Interrupts versus polling:** interrupts avoid continuous reads; bounded polling can simplify short initialization and failure recovery.
- **Readback versus timed delay:** readback can provide protocol-specific completion; delay guesses at timing and remains fragile across bridges and loads.
- **Read-modify-write versus dedicated aliases:** RMW is compact for ordinary control; set/clear registers avoid lost updates and destructive-read hazards.
- **Hardware state versus software shadow:** reading is authoritative when safe; a shadow supports write-only registers but must define reset and concurrent ownership.
- **One global lock versus fine-grained locks:** a global lock simplifies multi-register invariants; finer locks improve concurrency but expand ordering and reset analysis.
- **Raw userspace access versus kernel mediation:** raw access can aid trusted diagnostics; mediation supplies arbitration, lifecycle, portability, and least privilege.
- **Direct register ABI versus subsystem abstraction:** direct access exposes device quirks; a subsystem API stabilizes semantics and permits driver replacement.
- **Emulation versus physical testing:** emulation is deterministic and fault-friendly; hardware exposes real posting, power, timing, and electrical behavior.
- **Write combining versus device mapping:** write combining can accelerate approved apertures; ordinary registers require stronger device semantics.
- **Per-access tracing versus sampled semantic events:** exhaustive traces aid ordering diagnosis but change timing and risk side effects; semantic tracing is safer and smaller.

## Failure Modes and Misconceptions

- **“A BAR value is a pointer.”** It describes a bus resource that must be enabled, reserved, translated, and mapped.
- **“Physical and bus addresses are identical.”** Host bridges and IOMMUs create distinct domains.
- **“If mapping succeeds, the range is mine.”** Ownership requires reservation and correct device binding.
- **“`volatile` makes MMIO correct.”** It does not encode mapping type, accessor instruction, endian conversion, or full ordering.
- **“All 32-bit register accesses are interchangeable.”** Alignment, endian convention, ordering, and side effects still differ.
- **“Two 32-bit accesses equal one 64-bit access.”** The device can update between halves or require a prescribed order.
- **“A register dump is read-only diagnostics.”** Reads can acknowledge, consume, latch, or launch behavior.
- **“RMW preserves every bit.”** Write-one, reserved, volatile, and concurrently updated fields can be corrupted.
- **“A spinlock makes the last write reach hardware.”** Posted writes can remain in a bridge after unlock.
- **“Any read flushes posted writes.”** The target must be on the appropriate path, safe, live, and non-destructive.
- **“A memory barrier waits for the device.”** Ordering and device completion are different claims.
- **“MMIO ordering also synchronizes DMA.”** DMA mappings and ownership use the DMA API and its barriers.
- **“`memcpy` is efficient register I/O.”** It lacks device and FIFO access semantics.
- **“Polling can wait until hardware responds.”** Hardware can disappear or fail; every wait needs a deadline.
- **“An open file keeps hardware accessible.”** It can keep software state alive after disconnection only.
- **“Removal can unmap and let failures stop users.”** A late callback can touch revoked I/O and fault or corrupt another device.
- **“All-ones means one universal error.”** It can be data, absent-device behavior, or a bus-specific error signal.
- **“Emulated MMIO is harmless memory.”** It can trap, block, validate inputs, and expose an attack surface.

## Worked Examples

### Example 1

A platform driver receives a 4 KiB register resource from firmware, requests the entire range, maps it with a managed resource helper, verifies an ID register, and publishes its subsystem object. If the ID is wrong, managed cleanup unmaps and releases the range before probe returns.

### Example 2

A PCI network driver fills coherent queue descriptors, applies the DMA ordering required by the API, and writes a queue doorbell. It does not claim that `writel()` alone publishes ordinary cached descriptor memory to the device.

### Example 3

Two CPUs configure a banked register interface. One lock spans selection and data access, preventing CPU B from changing the bank between CPU A's two operations. Each individual 32-bit transaction was atomic, but only the lock made the pair coherent.

### Example 4

An interrupt status register is write-one-to-clear. The handler reads status once, masks supported pending bits, services them, and writes exactly that mask to acknowledge. It never ORs the read value into a control word.

### Example 5

A driver disables a device before handing a lock to another CPU. Because writes are posted, it follows the disable write with a safe status read on the same device before unlocking. The next owner cannot overtake the disable at the bridge.

### Example 6

A receive FIFO exposes one 32-bit data port. The driver uses a repeat accessor for the declared word count, preserving a fixed device offset and stream byte convention. Ordinary `memcpy_fromio()` would have the wrong increment behavior for this FIFO contract.

### Example 7

On a 32-bit host, a 64-bit counter latches the high half when low is read. The driver uses the low-then-high helper required by the device. A generic pair of reads could combine values across rollover.

### Example 8

Runtime suspend begins after the last user releases its power reference. New register operations first acquire a power reference or fail; suspend masks interrupts, drains work, saves approved state, and only then gates the clock.

### Example 9

A hot-unplugged PCI function returns an absent-device pattern. The driver marks itself disconnected, stops new submissions, contains DMA, and drains callbacks without trying to flush posted writes through the vanished function.

### Example 10

The following program checks a pure value transformation for an ordinary little-endian read-write control register. It preserves all bits outside `ENABLE` and `MODE`, encodes the wire bytes, and decodes them again. It does not perform MMIO, prove an accessor's ordering, make RMW atomic, or establish that a real register permits reading.

<!-- bijux-verify: {"id":"mmio-register-encoding","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"old=0xa5000000\nnew=0xa5000021\nwire=210000a5\nenabled=True\nmode=2\nreserved-preserved=True\n","stderr":""}} -->
```python
ENABLE = 1 << 0
MODE_SHIFT = 4
MODE_MASK = 0b11 << MODE_SHIFT

old = 0xA5000000
new = (old & ~(ENABLE | MODE_MASK)) | ENABLE | (2 << MODE_SHIFT)
wire = new.to_bytes(4, "little")
decoded = int.from_bytes(wire, "little")
reserved_mask = ~(ENABLE | MODE_MASK) & 0xFFFFFFFF

print(f"old={old:#010x}")
print(f"new={decoded:#010x}")
print(f"wire={wire.hex()}")
print(f"enabled={bool(decoded & ENABLE)}")
print(f"mode={(decoded & MODE_MASK) >> MODE_SHIFT}")
print(f"reserved-preserved={(decoded & reserved_mask) == (old & reserved_mask)}")
```

## Cross-Program Connections

[Computer Architecture](../../23-computer-architecture/ROADMAP.md) explains load/store execution, byte order, memory types, interconnects, PCI, bridges, cacheability, interrupts, and virtualization. [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) connects partial orders, atomics, locks, compiler transformations, and weak memory.

[Security Engineering](../../25-security-engineering/ROADMAP.md) connects least privilege, direct device access, malicious peripherals, DMA containment, emulation, and audit. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) contributes interface contracts, state machines, hazards, fault containment, evidence, and assurance. Within this program, [OS-061](061-device-discovery-and-driver-models.md) establishes device ownership and [OS-063](../ROADMAP.md) develops DMA.

## References

- Linux kernel documentation, [Bus-Independent Device Accesses](https://docs.kernel.org/driver-api/device-io.html), current page checked 2026-09-04. I/O mappings, `__iomem`, accessor families, ordering, endianness, repeated accesses, port I/O, posted writes and higher-level helpers.
- Linux kernel documentation, [Ordering I/O Writes to Memory-Mapped Addresses](https://docs.kernel.org/driver-api/io_ordering.html), current page checked 2026-09-04. Weakly ordered MMIO, locks, posted writes and safe readback.
- Linux kernel documentation, [Linux Kernel Memory Barriers](https://docs.kernel.org/core-api/wrappers/memory-barriers.html), current page checked 2026-09-04. Compiler, CPU, device and DMA ordering domains and accessor interactions.
- Linux kernel documentation, [How To Write Linux PCI Drivers](https://docs.kernel.org/PCI/pci.html), current page checked 2026-09-04. PCI enablement, resources, BAR reservation, mapping, DMA, interrupts and shutdown ordering.
- Linux kernel documentation, [Devres](https://docs.kernel.org/driver-api/driver-model/devres.html), current page checked 2026-09-04. Device-managed resource acquisition, I/O mapping helpers, rollback and lifetime.
- Linux kernel documentation, [Dynamic DMA Mapping Guide](https://docs.kernel.org/core-api/dma-api-howto.html), current page checked 2026-09-04. CPU, bus and DMA address distinctions, mapping, ownership and synchronization.
- Linux kernel documentation, [Memory Management APIs](https://docs.kernel.org/core-api/mm-api.html), current page checked 2026-09-04. Kernel mapping APIs and memory attributes relevant to distinguishing RAM mappings from I/O mappings.
- Linux kernel documentation, [Sparse](https://docs.kernel.org/dev-tools/sparse.html), current page checked 2026-09-04. Address-space annotations and static checking of `__iomem` use.
- Linux man-pages project, [ioperm(2)](https://man7.org/linux/man-pages/man2/ioperm.2.html), current page checked 2026-09-04. Userspace I/O-port permission scope, privilege, inheritance and architecture limitations.
- Linux man-pages project, [outb(2)](https://man7.org/linux/man-pages/man2/outb.2.html), current page checked 2026-09-04. Userspace port input/output helpers, privilege, architecture and compiler requirements.

## Exercises

### Exercise 1

Design the resource and mapping lifecycle for a PCI controller with one MMIO control BAR, one prefetchable data aperture, an optional I/O-port BAR, runtime power management, interrupts, and hot-unplug.

### Exercise 2

Given a mixed register containing ordinary enable bits, write-one-to-clear interrupt status, reserved bits, and a self-clearing command field, design safe update and acknowledgement operations.

### Exercise 3

Construct the ordering proof for a transmit queue: descriptor initialization, DMA ownership, doorbell write, posted-write flush, interrupt completion, queue reset, and buffer reuse.

### Exercise 4

Design bounded polling for a reset-complete bit that can run during probe, ordinary operation, and removal. Include timing, context, device loss, and evidence.

### Exercise 5

Build a verification and assurance plan for a portable register-access layer used on little- and big-endian CPUs, 32- and 64-bit systems, physical and virtual devices, and weakly ordered interconnects.

## Answers to the Exercises

### Answer 1

Enable the PCI function through the bus API and inspect each BAR's declared type, length and flags. Request only the control and data regions the driver will own, plus the optional port region when the feature is supported. Map the control BAR with device semantics and the data aperture with a prefetchable or write-combining helper only if PCI, architecture and device documentation permit it. Map I/O-port space through the PCI I/O abstraction rather than converting the port number to an MMIO pointer. Validate register revision before enabling interrupts or publishing queues.

Store all tokens in per-device state. Runtime operations acquire a power reference before access; resume restores mapping-independent software state, powers suppliers, verifies identity and restores approved registers before making the device active. Removal marks disconnected and unpublishes entry points, stops submissions, disables device interrupt generation, synchronizes handlers, cancels work, contains and drains DMA, and only then unmaps apertures, releases regions and disables the function. Surprise removal skips unsafe device acknowledgement and relies on bus and IOMMU containment. Managed resources can reverse mechanical allocation, but explicit quiescence must precede their release.

### Answer 2

Do not perform one read-modify-write across the mixed value. Define masks for ordinary writable enable bits, W1C status, command and reserved fields. Update enables through a dedicated control alias if available. Otherwise serialize with all writers, read only if the specification says the mixed register is safely readable, clear status and command bits from the value, replace only enable fields, force reserved bits to their mandated values, and issue the width-correct write. Maintain a shadow if the ordinary fields are write-only and the reset contract makes a shadow sound.

Acknowledge interrupts with a separate write containing ones only for the observed and serviced W1C bits and zeros elsewhere. Issue a command as its own write with only the documented command field, then use the specified completion indication and deadline; do not retry blindly if duplicate execution is unsafe. Test hardware assertions between status read and acknowledgement, concurrent enable updates, unknown future reserved bits, command timeout, and reset. If hardware supplies set, clear, acknowledge and command aliases, use them because they remove the mixed-operation ambiguity.

### Answer 3

Let $D$ be descriptor initialization, $O$ ownership publication, $B$ doorbell visibility, $F$ safe readback completion, $I$ validated completion, $Q$ queue quiescence, $R$ reset completion, and $U$ buffer reuse. The required order is $D \prec O \prec B$. CPU stores and DMA ownership use the DMA API and its barrier; the MMIO doorbell expresses notification but does not replace those edges. If another CPU or lifecycle transition must know the doorbell reached the device, the bus-specific safe read establishes $B \prec F$.

Normal reuse requires device completion, validated through the completion queue or interrupt protocol, so $B \prec I \prec U$. Reset recovery instead blocks submissions, masks arrivals, drains or aborts DMA through the documented mechanism, synchronizes interrupts, issues reset, waits with a bound, and restores state: $F \prec Q \prec R \prec U$ where readback is legal. Locks serialize queue indices and reset state but do not prove device completion. Test delayed descriptor visibility, posted doorbells, lost interrupts, spurious completion, reset races, timeout, surprise removal and two CPUs sharing the queue.

### Answer 4

Define one poll helper with an explicit legal-state predicate, accessor, expected mask/value, monotonic deadline, delay policy, cancellation or disconnect check, and structured result. During sleepable probe, use a sleep-capable polling helper with a delay appropriate to device latency. In a short atomic transition, use a bounded atomic helper and document the maximum occupied CPU time. Ordinary operation should normally use completion or interrupts when waits are long. Removal first prevents new polling and cancels or joins existing pollers before revoking the mapping.

Each iteration checks that mapping, power generation and presence remain valid before a non-destructive status read. Success records elapsed time and final status. Timeout captures device identity, state, register contract revision, iteration count, last value and surrounding command without dumping destructive registers, then enters a defined abort, reset or failure state. Surprise loss returns a distinct disconnected error rather than spinning on an absent-device pattern. Test immediate completion, last-instant completion, never-complete, transient value, power loss, reset, concurrent interrupt completion, cancellation, clock changes and delayed emulation.

### Answer 5

Specify every register's offset, legal widths, byte order, semantic class, masks, reset state, access state, concurrency owner and ordering edges in a machine-reviewable schema. Generate or wrap only approved scalar, repeated and split-64 accessors; keep `__iomem` or equivalent tokens typed. Compile with sparse and architecture warnings, cross-build for endian and word-size variants, and unit-test encode/decode, masks, bounds, split ordering, timeouts and lifecycle generations. Ban direct dereference, generic memory copies and unexplained raw or relaxed access in review rules.

Use an emulator to record widths, offsets and order and to inject malformed access, delayed writes, changing 64-bit halves, stuck status, reset, removal and hostile values. Run physical tests across CPU architectures, host bridges, device revisions, cacheability modes, power cycles, interrupt routing and hotplug. Stress peer CPUs, handler/process sharing, suspend, reset and unbind while tracing semantic events. Confirm reservation exclusivity, publish-after-ready, descriptor-before-doorbell, safe posted-write flush, bounded progress and drain-before-unmap. Preserve source revisions, toolchains, configurations, seeds, traces, hardware topology, negative results and limitations; do not generalize one emulator or board result to all architectures.
