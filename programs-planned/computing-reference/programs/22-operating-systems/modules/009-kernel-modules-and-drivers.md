---
module_id: OS-009
program: Operating Systems
level: 1
module_number: 9
title: Kernel Modules and Drivers
status: complete
last_verified: 2026-09-04
---

# Kernel Modules and Drivers

## One-Page Review

### Governing question

How can a kernel extension discover and control hardware, expose services, survive asynchronous events, and be loaded or removed without violating compatibility, authority, lifetime, or recovery invariants?

### Essential definitions

- A **kernel module** is a loadable unit of privileged code and data linked against a kernel's exported interface; loadability does not create a stable cross-version ABI.
- A **device** is an instance represented by bus, firmware, or platform discovery; a **driver** is implementation logic that may bind to compatible device instances.
- **Matching** selects candidate driver-device pairs from identifiers and policy; **probing** verifies and initializes one candidate pair.
- A **resource** is anything acquired for an instance—memory, registers, clocks, interrupts, DMA mappings, queues, names, or references—with a corresponding release obligation.
- **Quiescence** is a state in which new work is rejected and asynchronous producers can no longer access resources scheduled for release.
- A **module signature** authenticates module bytes under a configured trust policy; it does not establish correctness, safety, or fitness for a device.
- A **driver ABI** is the user-visible behavior exposed through system calls, device nodes, sysfs, netlink, or another interface; internal kernel interfaces may evolve independently.

### Central model, mechanism, or theorem

Treat binding as a transaction and unbinding as an ordered shutdown:

`match → acquire → initialize → publish → serve → quiesce → drain → revoke → release`.

Before publication, each failure unwinds every acquired resource exactly once in reverse dependency order. After publication, teardown first prevents new entrants, stops hardware and software producers, waits for in-flight ownership, revokes user-visible access, and only then releases memory and executable module text. A module is unloadable only when no code path, callback, interrupt, work item, reference, or device can enter it.

### Critical invariants

- A driver binds only to an identified and verified device instance whose resources belong to it.
- Every successful acquisition is either transferred into published instance ownership or released once on every failure path.
- Interrupts, DMA, timers, work queues, and callbacks are enabled only after their state is initialized and are stopped before that state is released.
- User-visible operations acquire a live instance reference and reject access after quiescence begins.
- Register access uses the architecture and bus accessors, ordering, width, endianness, and power-state rules required by the device.
- Module dependencies, exported symbols, configuration, version checks, signatures, and policy are validated before executable code is admitted.
- Suspend, resume, reset, hot removal, failed probe, and unload preserve the same ownership and device-state invariants as normal operation.

### Common failures

Common mistakes are assuming an identifier proves the hardware is usable, publishing a device node before initialization, leaking the first resources when a later acquisition fails, freeing state before disabling interrupts or DMA, confusing interrupt acknowledgement with completion, touching registers while power is off, trusting module signatures as code review, exposing an unstable sysfs format, assuming module reference counts cover every callback, unloading after a timeout while hardware remains active, and debugging only the successful probe path.

### Compact example

A storage driver matches a discovered controller, verifies its revision, enables power and bus access, maps registers, sets a DMA mask, allocates rings, registers an interrupt, initializes queues, and only then publishes the block device. If interrupt registration fails, it frees rings, unmaps registers, disables the device, and returns an error. On hot removal, it blocks new requests, marks the instance gone, stops queue submission, masks device interrupts, stops DMA, synchronizes interrupt and worker completion, removes the user-visible device, releases mappings and power, drops references, and finally permits module text to unload.

### Connections

[OS-004](004-interrupts-and-exceptions.md) develops interrupt entry, [OS-008](008-kernel-memory-allocation.md) develops allocation and DMA shape, and [OS-010](../ROADMAP.md) traces a request through these boundaries. [OS-065](../ROADMAP.md) develops the device model and hotplug in depth. Hardware protocols belong to [Computer Architecture](../../23-computer-architecture/ROADMAP.md); trust and signing belong to [Security Engineering](../../25-security-engineering/ROADMAP.md).

## Governing Question

Drivers translate generic kernel operations into device-specific register access, memory transactions, interrupts, resets, and power changes. They execute with kernel privilege and often consume inputs from untrusted hardware, firmware, and users. A one-line bounds error can corrupt the kernel; a stale DMA engine can write after memory reuse; a bad unload can jump into freed module text.

Modules add operational flexibility: functionality can be built separately, loaded when hardware appears, updated or diagnosed without placing all code in the core image, and omitted from systems that do not need it. The same flexibility enlarges the trusted computing base at runtime. Compatibility, provenance, configuration, dependency resolution, signature policy, and loading authority become part of system integrity.

The governing question is how to make extension and device lifecycles explicit. Correctness spans build time, module admission, bus matching, probe, publication, concurrent service, power transitions, reset, hot removal, failure unwind, observability, and final unload. No single callback or reference count covers all of them.

## Why This Matters

Drivers account for much of a general-purpose kernel's code and its exposure to complex external behavior. Devices can deliver malformed descriptors, surprise removal, duplicate or missing interrupts, delayed DMA, impossible status bits, firmware crashes, and resets at arbitrary times. Kernel code must contain those conditions without trusting that hardware follows the happy path.

Initialization and teardown are mirror-image dependency problems. An interrupt handler requires mapped registers and initialized queues. DMA requires allocated memory and a valid device mapping. A user-visible node requires a live reference and operations table. Releasing a lower dependency before its consumers creates a use-after-free or hardware access fault.

Interfaces outlive implementations. A sysfs attribute, ioctl, netlink field, device-node permission, error code, or event ordering can become a user-space ABI. Internal module symbols are often deliberately not stable across kernel builds, but user-visible behavior still needs versioning, documentation, compatibility, and security review.

## Prerequisites and Retrieval

Recall from [OS-002](002-privilege-levels-and-protection-rings.md) that kernel execution carries broad authority. Recall from [OS-004](004-interrupts-and-exceptions.md) that interrupt handlers have restricted context and shared interrupts require source identification. Recall from [OS-007](007-kernel-data-structures.md) that lookup does not itself acquire lifetime. Recall from [OS-008](008-kernel-memory-allocation.md) that a CPU pointer, physical address, and DMA address are distinct.

Retrieve these distinctions:

- module loading is runtime linking of privileged code, not process isolation;
- device discovery creates an instance candidate, while a driver verifies and binds it;
- successful `probe` transfers ownership into the bound instance, while failed `probe` publishes nothing;
- stopping new requests does not drain old requests;
- masking a CPU interrupt does not necessarily stop device DMA or queued work;
- a signed binary has authenticated provenance under a key policy, not demonstrated correctness;
- a stable user ABI is different from the kernel's internal module symbol interface.

## Learning Objectives

After completing this module, you should be able to:

- explain module construction, exported symbols, dependency resolution, version checks, signatures, and load policy;
- distinguish devices, drivers, buses, classes, matching, probing, binding, and publication;
- design a reversible probe sequence with explicit resource ownership;
- order interrupt, DMA, register, queue, user-interface, and module lifetimes;
- reason about memory-mapped I/O access, barriers, device endianness, and posted writes;
- design bounded interrupt top halves and deferred processing;
- handle reset, hot removal, suspend, resume, firmware, and partial failure;
- define stable, permissioned user-visible interfaces without leaking kernel internals;
- use fault injection, emulation, tracing, static analysis, and hardware testing appropriately;
- identify security, real-time, or safety claims requiring accountable human review.

## Core Exposition

### Modules are admitted kernel code

A module contains relocatable code, data, metadata, dependency information, and references to exported kernel symbols. Loading resolves permitted symbols, applies relocations, allocates executable and data mappings, runs initialization, and makes new entry points reachable. Any bug executes inside the kernel's trust domain.

The build must target the exact kernel environment expected by the compatibility policy: architecture, configuration, compiler-relevant options, headers, exported symbols, and version information. Linux kbuild supports in-tree and external modules and performs a modpost stage for symbol checks. `CONFIG_MODVERSIONS` adds CRC-based prototype consistency checks, but no checksum can make arbitrary private internals a stable semantic ABI.

Export symbols deliberately. Each export expands coupling and potential attack surface. Namespaces and license rules can express intended consumers, but architectural ownership still matters. Prefer subsystem operations that preserve invariants over exposing raw data structures or low-level mechanisms.

### Admission, signatures, and policy

Before loading, verify format, target architecture, dependencies, compatibility metadata, signature policy, and caller authority. A module signature binds exact bytes to a trusted key and lets the kernel enforce rejection of missing or invalid signatures under configuration. The security result depends on private-key custody, enrolled public keys, revocation, build provenance, and whether module loading can later be disabled.

Signing does not inspect logic. A correctly signed vulnerable or malicious module remains dangerous if the signer or build chain admitted it. Conversely, taint records conditions relevant to diagnosis, such as proprietary or unsigned modules under particular configurations; unloading does not erase the historical state used to interpret a crash.

Production policy should minimize load authority, available modules, automatic-load aliases, writable module storage, and unnecessary exported interfaces. High-assurance systems may compile required drivers into a measured image and disable later module loading. Flexibility and recovery needs must be weighed against runtime extensibility.

### Device model: instance, implementation, and bus

A device object represents one instance and its place in a parent-child, bus, class, firmware, and power topology. A driver object represents code capable of controlling compatible instances. A bus or subsystem defines discovery, identifiers, matching rules, resource interpretation, and lifecycle callbacks.

Matching says “this driver may support this instance.” Probe must verify device presence, supported revision, required capabilities, and resources. Identifiers supplied by firmware or a bus can be wrong, incomplete, or spoofable. A driver must avoid destructive access until it has enough evidence that the hardware and ownership are correct.

One driver can bind many devices, so per-driver global state and per-device instance state must be separated. Locks, queues, counters, references, DMA mappings, register windows, power state, and failure state usually belong to the instance. Global registries need their own synchronization and unload rules.

### Probe as a transaction

Write the dependency sequence before code. A common ordering is enable parent resources, enable the device, map registers, configure addressability, allocate software state, allocate and map DMA buffers, initialize hardware, register interrupts, register subsystem objects, then publish user-visible access. Actual hardware may require a different order, but every edge should be justified.

After acquisition `r_i`, the current path owns its release obligation. If `r_(i+1)` fails, release `r_i` through `r_1` in reverse dependency order. Do not run full detach code on a half-built instance unless that code explicitly accepts every partial state. Managed device resources can automate release on probe failure and detach, but they do not infer quiescence or fix the wrong acquisition order.

Return deferred probe only when a genuine supplier is not ready, and do so before expensive or externally visible work when possible. Repeated deferral must not leak resources, reset shared hardware destructively, or flood logs. Permanent incompatibility, missing optional features, transient absence, and dependency deferral are different results.

Publish last. Until the instance is initialized, operations tables, device nodes, sysfs controls, interrupts, and upstream queues must not offer entry. If a framework registers an object before final activation, its operations need an explicit inactive state and lifetime protection.

### Register and bus access

Memory-mapped I/O is not ordinary memory. Use the platform's accessors so width, ordering, endianness, barriers, sparse checking, and architecture behavior are respected. Compiler `volatile` does not provide the complete device ordering contract. Read-modify-write can be unsafe for write-one-to-clear, self-clearing, latched, or concurrently updated registers.

Posted writes may reach the device after the CPU instruction retires. A documented readback or bus-specific flush may be required before assuming completion. Device and CPU memory ordering interact when descriptors are filled in memory, ownership is transferred through a register, and completion arrives through DMA or interrupt.

Validate offsets, lengths, reserved bits, and device-reported capabilities. Never use an untrusted device length directly for host allocation or copy. Bound polling and timeouts, and distinguish a slow device from a removed, reset, or power-gated one.

### Interrupts and deferred work

Before enabling a device interrupt, initialize the handler's state and register the CPU-side interrupt path according to the hardware sequence. The handler must identify whether a shared interrupt belongs to its device, acknowledge or mask it correctly, capture minimal status, and schedule bounded follow-up work. It must not sleep in hard-interrupt context.

Acknowledging an interrupt can mean clearing a notification, not completing the request that caused it. A level-triggered source may immediately retrigger until the underlying condition is resolved. Masking only the CPU vector can leave the device asserting the line or continuing DMA.

Deferred work—threaded interrupts, tasklets where supported, work queues, polling, or subsystem callbacks—moves expensive processing into a suitable context. It also creates asynchronous lifetime. Teardown must stop scheduling, synchronize the interrupt handler, cancel or drain queued work, and account for work that requeues itself.

### DMA and ownership transfer

Configure the device's DMA addressing capability before allocating or mapping buffers that depend on it. Use the DMA API to obtain device-visible addresses and obey mapping errors, direction, synchronization, cache-coherency, segment, alignment, and lifetime rules. Do not derive a DMA address from a CPU virtual pointer.

Descriptor ownership is a state machine. The CPU initializes a buffer and descriptor, performs required synchronization, then makes it device-owned. It must not mutate or release the buffer until completion and the matching synchronization transfer ownership back. The device must not receive stale pointers during reset or teardown.

An IOMMU limits or remaps device access only under its configured domain and mappings. It improves isolation but does not stop a device from corrupting any still-mapped buffer or make incorrect lengths safe. Unmap only after the hardware cannot issue late transactions; hardware reset and bus-level transaction drainage may be required.

### User-visible interfaces

Choose an existing subsystem interface when possible. It supplies naming, lifetime, permissions, polling, event, compatibility, and tooling conventions. A bespoke ioctl or sysfs format creates a durable ABI and review burden. Sysfs attributes conventionally represent one value or a clearly defined structured representation, not arbitrary command languages.

Define units, ranges, encoding, atomicity, permissions, errors, blocking, event order, and behavior during removal. Parse all input strictly, reject trailing or overflowing values as appropriate, and copy only initialized output. Never expose kernel pointers or mutable internal layouts.

Each open file, mapping, request, and callback needs instance lifetime. Hot removal can make hardware unavailable while user handles remain open. Operations should detect the gone state and return a stable error without touching released registers or memory. Mapping device memory to userspace requires additional revocation and isolation design.

### Firmware and device trust

Some drivers request firmware blobs or expose device firmware update paths. Validate size, structure, target identity, version policy, cryptographic authorization where required, rollback rules, and failure recovery before a device executes the image. The kernel's generic transport cannot decide whether arbitrary bytes are safe for a particular device.

Firmware loading can involve user space and filesystem availability, so it participates in probe timing, dependency, suspend, and recovery. Asynchronous requests create callback lifetime. An update interrupted by power loss needs a device-specific transactional or recovery story.

Treat device output as hostile input even when the hardware is trusted: faults, signal integrity, old firmware, DMA corruption, and shared virtualized devices can violate expectations. Validate completion indices, lengths, counts, status enums, and ownership generations before accessing host memory.

### Power management and reset

Runtime power management reduces idle consumption; system sleep coordinates a hierarchy. Before suspend, block new I/O as required, drain or cancel work, stop DMA and ordinary interrupts, save necessary state, and enter a supported low-power state. Resume restores parent access, power, clocks, bus state, registers, queues, and interrupt readiness before reopening service.

Wake-capable devices intentionally retain limited behavior. The driver, bus, power domain, and core share responsibility, so callback order matters. Suspend failure must unwind already suspended devices. Surprise removal or reset can occur while suspend is in progress and must converge on a consistent state.

Reset is not merely register initialization. It changes ownership of in-flight commands and may invalidate DMA, firmware, sequence numbers, and cached state. Fence old completions with generations or reset epochs so they cannot complete new requests accidentally.

### Quiescence, removal, and unload

Begin removal by making the instance unavailable to new entrants under the same synchronization used for lookup. Stop upstream queues and revoke control operations. Mark a permanent gone state for surprise removal; avoid register access if the bus says the device is absent.

Then stop producers: device command fetch, DMA, interrupts, timers, work, callbacks, and asynchronous firmware operations. Synchronize every consumer and wait for in-flight references. Remove user-visible registration at the lifecycle point defined by the subsystem, but remember that existing handles may outlive name removal.

Release resources in dependency order only after quiescence. Module unload additionally requires that no instance, exported operation, registered callback, trace hook, work item, or other module depends on its code or data. A timeout is evidence of an unresolved owner, not permission to free underneath it.

### Observability and testing

Log stable instance identifiers, state transitions, bounded error detail, reset epochs, timeouts, interrupt counts, DMA mapping failures, queue depths, and recovery results. Rate-limit device-controlled events. Avoid raw addresses, secrets, unbounded register dumps, or diagnostics that touch powered-off and removed hardware.

Fault-inject each probe acquisition and verify zero published state and complete reverse unwind. Exercise unload during opens and I/O, surprise removal, interrupt storms, lost interrupts, late DMA, malformed completions, reset races, suspend at every queue state, firmware failure, dependency deferral, and repeated bind-unbind cycles.

Static analysis and sanitizers find classes of memory, locking, and API bugs. Emulation and virtual hardware improve determinism and rare-state coverage. Real hardware is still required for timing, ordering, DMA, power, reset, electrical, firmware, and errata behavior. Evidence from one layer does not subsume the others.

## Definitions and Notation

Let the binding state be one of `U` (unbound), `A_i` (the first `i` resources acquired but unpublished), `L` (live and published), `Q` (quiescing), `D` (drained), and `R` (released). Normal transitions are

`U → A_1 → ... → A_n → L → Q → D → R`.

A failure in `A_i` follows `A_i → A_(i-1) → ... → U`, releasing each resource exactly once. Publication is permitted only from `A_n`. Teardown release is permitted only after `Q → D` proves that no prohibited producer or consumer retains access.

Let `E` be the set of entry sources: user operations, interrupts, timers, workers, subsystem callbacks, power callbacks, and device DMA. Let `enabled(e, s)` mean source `e` can enter instance state in lifecycle state `s`. A necessary release condition for state memory `M` is

`for every e in E: not enabled(e, D) and in_flight(e, D) = 0`.

Device ownership of buffer `b` is `owner(b) ∈ {CPU, device, retired}`. CPU mutation is permitted only in `CPU`; release requires `retired` after device access and all CPU readers end. Required memory and DMA synchronization operations are part of each ownership transition.

Module unload has the stronger condition `instances = 0`, `dependents = 0`, and `callable_entries = 0`. A numerical module reference count is evidence for mechanisms wired into it, not proof that every possible entry source was registered correctly.

## Mechanisms, Invariants, or Proof Structure

Review a module or driver through eight obligations.

**Admission integrity.** Build identity, exported symbols, dependency graph, signature, key trust, loader authority, and policy admit exactly the intended code.

**Identity integrity.** Matching and probe establish the actual device, revision, resource ownership, capabilities, firmware, and isolation domain before destructive use.

**Acquisition integrity.** Each resource has one owner, dependency position, publish boundary, and reverse unwind for every partial failure.

**Entry integrity.** Every user, interrupt, callback, worker, power, and device entry checks or inherits a live instance and valid context.

**I/O integrity.** Register and DMA access obey address space, width, order, endian, coherence, ownership, bounds, and power-state rules.

**Quiescence integrity.** New work closes before producers stop, in-flight work drains before revocation, and state and module text outlive all possible entries.

**Recovery integrity.** Reset, suspend, resume, hot removal, timeouts, firmware failure, and malformed device output converge on defined live, degraded, or gone states.

**Evidence integrity.** Failure injection, concurrency tests, emulation, analyzers, hardware runs, and human review state which lifecycle, device, build, and timing claims they cover.

The executable model below demonstrates reverse unwind for failed binding and reverse release after successful publication.

<!-- bijux-verify: {"id":"toy-driver-lifecycle","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"fail-at-0=status:failed released:none\nfail-at-2=status:failed released:irq,registers\nsuccess=status:bound held:registers,irq,dma,published\ndetach=released:published,dma,irq,registers\n","stderr":""}} -->
```python
def bind(fail_at):
    plan = ["registers", "irq", "dma", "published"]
    held = []
    released = []
    for index, resource in enumerate(plan):
        if index == fail_at:
            while held:
                released.append(held.pop())
            return "failed", held, released
        held.append(resource)
    return "bound", held, released


def detach(held):
    released = []
    while held:
        released.append(held.pop())
    return released


status, held, released = bind(0)
print("fail-at-0=status:" + status + " released:" + (",".join(released) or "none"))
status, held, released = bind(2)
print("fail-at-2=status:" + status + " released:" + (",".join(released) or "none"))
status, held, released = bind(99)
print("success=status:" + status + " held:" + ",".join(held))
print("detach=released:" + ",".join(detach(held)))
```

Passing proves only list ownership and reverse ordering for three deterministic runs. It does not model concurrency, real resource APIs, hardware, interrupts, DMA, partial release failure, references, power, reset, signatures, or module loading.

## Alternatives and Trade-Offs

**Built-in code versus loadable module.** Built-in code simplifies early availability and can support disabling runtime extension. Modules reduce static footprint and enable flexible deployment but add loader, compatibility, signing, dependency, and unload concerns.

**Manual unwind versus managed resources.** Explicit unwind makes ordering visible and can handle unusual lifetimes. Managed resources reduce repetitive failure paths but still require correct quiescence and ordering and may not fit resources that outlive binding.

**Interrupts versus polling.** Interrupts avoid continuous work at low rates but add asynchronous races and storms. Polling can batch efficiently under load but consumes CPU and needs latency and fairness policy; hybrids are common.

**Kernel driver versus user-space driver.** Kernel drivers integrate with subsystems and privileged resources. User-space drivers can improve fault isolation and iteration but still need a minimal trusted kernel boundary, safe interrupt/DMA mediation, and recovery.

**Generic subsystem versus custom ABI.** A subsystem supplies conventions, tooling, lifecycle, and compatibility. A custom ABI can expose unique hardware but creates lasting semantics and a larger review burden.

**Strict signature enforcement versus development flexibility.** Strict policy narrows admitted code and supports provenance. Development keys and unsigned loading ease diagnosis but expand authority and can invalidate production-like security evidence.

**Automatic recovery versus fail-stop.** Reset and retry improve availability for transient faults but can duplicate operations or hide degradation. Fail-stop contains ambiguity but may remove essential service; policy follows device semantics and hazard analysis.

## Failure Modes and Misconceptions

1. **“A module is isolated like a process.”** It normally executes in the kernel address space with kernel authority.
2. **“A successful build proves compatibility.”** Configuration, symbols, semantics, architecture, and the running kernel still matter.
3. **“A valid signature proves safe code.”** It authenticates bytes under a trust policy, not behavior.
4. **“Matching means the device is ready.”** Probe must verify capabilities, resources, state, and dependencies.
5. **“Managed resources make teardown automatic.”** They release registered resources but cannot infer hardware quiescence or asynchronous lifetime.
6. **“Masking the interrupt stops the device.”** DMA, queues, level conditions, and other event routes can continue.
7. **“Interrupt acknowledgement completes the request.”** It may only clear notification; ownership and completion need separate evidence.
8. **“Volatile makes register access correct.”** Bus accessors, barriers, width, endian, and device semantics remain necessary.
9. **“An IOMMU makes DMA bugs harmless.”** A device can still corrupt any incorrectly mapped or bounded region.
10. **“Removing a device node ends use.”** Existing opens, mappings, references, callbacks, and DMA may remain.
11. **“A timeout permits forced free.”** It reveals unresolved ownership; freeing can turn delay into corruption.
12. **“Internal kernel interfaces are stable ABIs.”** External modules must follow the target kernel's supported compatibility contract.
13. **“Sysfs is a convenient command parser.”** It is a durable user interface with format, permission, and lifecycle obligations.
14. **“Emulation replaces hardware testing.”** It cannot establish real bus, ordering, timing, power, DMA, firmware, and errata behavior.

## Worked Examples

### Example 1

**Question:** A module built for a similar kernel release has all expected symbol names. Is it safe to load?

**Reasoning:** Structure layout, configuration, symbol versions, compiler features, semantics, and architecture details may differ despite names.

**Conclusion:** Build and admit against the exact compatibility identity required by the target system.

### Example 2

**Question:** Probe maps registers and allocates a DMA ring, then interrupt registration fails. What state may remain?

**Reasoning:** Nothing was published, so reverse unwind must release the DMA mapping and storage, then the register mapping and device enablement.

**Conclusion:** Every acquisition point needs a complete partial-failure path.

### Example 3

**Question:** Why register the interrupt before enabling it at the device?

**Reasoning:** If the device raises an event first, no valid CPU handler may exist; if handler state is incomplete, entry can dereference invalid data.

**Conclusion:** Initialize state and the receive path before activating the producer.

### Example 4

**Question:** A shared interrupt fires, but this device's status has no pending bit. What should the driver do?

**Reasoning:** Another device may own the shared line. Acknowledging unrelated hardware or claiming the event breaks sharing.

**Conclusion:** Return the platform's not-mine result without disturbing the device.

### Example 5

**Question:** A completion descriptor reports length 4 GiB for a 4 KiB mapped buffer. Can trusted firmware make that safe?

**Reasoning:** Hardware or firmware can fail, and using the length would overrun host memory.

**Conclusion:** Validate every device-controlled index, length, state, and generation against host-owned bounds.

### Example 6

**Question:** The device is hot-removed while a user file remains open. Must the file object vanish?

**Reasoning:** The handle may retain software state, but hardware access is no longer valid. Operations need a stable gone state and error behavior.

**Conclusion:** Separate software-handle lifetime from device availability.

### Example 7

**Question:** A suspend callback powers off hardware before draining its DMA queue. What risk follows?

**Reasoning:** Transactions may be incomplete or later appear against buffers whose ownership the driver wrongly reclaimed.

**Conclusion:** Quiesce submission and resolve DMA ownership before power removal.

### Example 8

**Question:** An old completion arrives after reset and has the same queue index as a new request. What prevents aliasing?

**Reasoning:** Index reuse alone cannot distinguish epochs. The old event can complete or corrupt the new request.

**Conclusion:** Reset must fence old DMA and interrupts and validate a generation or equivalent ownership identity.

### Example 9

**Question:** A signed diagnostic module prints raw kernel pointers to an unprivileged sysfs file. Is signature enforcement enough?

**Reasoning:** The trusted signer admitted code that discloses address-layout information through a weak interface.

**Conclusion:** Provenance complements, but never replaces, interface and implementation security review.

### Example 10

**Question:** A medical pump driver passes repeated bind-unbind and fault-injection tests. Does that establish safe therapy delivery?

**Reasoning:** Sensor validity, actuation limits, timing, firmware, power loss, recovery, human factors, and system hazards remain outside those tests.

**Conclusion:** Named device, real-time, clinical-safety, security, and acceptance authorities must review the full evidence; this module claims no certification.

## Cross-Program Connections

[Computer Architecture](../../23-computer-architecture/ROADMAP.md) develops buses, interrupts, memory ordering, caches, DMA, IOMMUs, and device registers. This module turns those mechanisms into a lifecycle and ownership discipline. [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies synchronization, cancellation, quiescence, and reclamation models.

[Security Engineering](../../25-security-engineering/ROADMAP.md) connects signing, build provenance, loader authority, untrusted devices, memory corruption, and interface hardening. [Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md) contributes dependency inversion and resource acquisition patterns, while kernel context adds non-sleeping paths and hardware side effects.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) frames fault containment, degraded modes, recovery, assurance cases, and accountable acceptance. Successors [OS-010](../ROADMAP.md), [OS-065](../ROADMAP.md), [OS-066](../ROADMAP.md), and [OS-070](../ROADMAP.md) deepen request tracing, device models, interrupt-driven I/O, and storage-driver behavior.

## References

- Linux Kernel documentation, [Building External Modules](https://docs.kernel.org/kbuild/modules.html), current page checked 2026-09-04. Kbuild integration, prepared trees, modpost, exported symbols, Module.symvers, and versioning.
- Linux Kernel documentation, [Kernel module signing facility](https://docs.kernel.org/admin-guide/module-signing.html), current page checked 2026-09-04. Signing, supported keys and algorithms, enforcement, manual signing, and signature limitations.
- Linux Kernel documentation, [Device Drivers](https://docs.kernel.org/driver-api/driver-model/driver.html), current page checked 2026-09-04. Driver objects, registration, probe, deferred probe, removal, shutdown, and sysfs relationships.
- Linux Kernel documentation, [Platform Devices and Drivers](https://docs.kernel.org/driver-api/driver-model/platform.html), current page checked 2026-09-04. Discovery outside the driver, platform resources, matching, probe, removal, shutdown, and power callbacks.
- Linux Kernel documentation, [Devres: Managed Device Resource](https://docs.kernel.org/driver-api/driver-model/devres.html), current page checked 2026-09-04. Device-bound release actions, failure unwind, groups, and managed API trade-offs.
- Linux Kernel documentation, [Driver Basics](https://docs.kernel.org/driver-api/basics.html), current page checked 2026-09-04. Current resource-management, work, timer, interrupt, and driver helper contracts.
- Linux Kernel documentation, [Dynamic DMA mapping Guide](https://docs.kernel.org/core-api/dma-api-howto.html), current page checked 2026-09-04. DMA masks, coherent and streaming mappings, direction, synchronization, errors, and teardown.
- Linux Kernel documentation, [Device Power Management Basics](https://docs.kernel.org/driver-api/pm/devices.html), current page checked 2026-09-04. Runtime and system power transitions, hierarchy, callback ordering, I/O quiescence, wake, and unwind.
- Linux Kernel documentation, [Firmware Upload API](https://docs.kernel.org/driver-api/firmware/fw_upload.html), current page checked 2026-09-04. Driver-specific validation responsibility, sysfs transport, cancellation, status, and worker context.
- Linux Kernel documentation, [Kernel Self-Protection](https://docs.kernel.org/security/self-protection.html), current page checked 2026-09-04. Module-loading restrictions, attack-surface reduction, memory permissions, initialization, and information exposure.
- Linux Kernel documentation, [Tainted kernels](https://docs.kernel.org/admin-guide/tainted-kernels.html), current page checked 2026-09-04. Persistent diagnostic state for proprietary, unsigned, forced, staging, and other relevant conditions.
- Linux Kernel documentation, [sysfs: The filesystem for exporting kernel objects](https://docs.kernel.org/filesystems/sysfs.html), current page checked 2026-09-04. Kobject relationships, attributes, lifetime, and show/store interface conventions.
- Russ Cox, Frans Kaashoek, and Robert Morris, [*xv6: a simple, Unix-like teaching operating system*](https://pdos.csail.mit.edu/6.1810/2025/xv6/book-riscv-rev5.pdf), MIT, 2025 edition. Teaching examples of console, disk, interrupt, register, DMA-descriptor, sleep, and lock interactions.

## Exercises

### Exercise 1

Design a probe dependency graph for a PCI-like network device. Include device enablement, regions, register mapping, DMA mask, queues, interrupts, subsystem registration, user visibility, fault injection, and reverse unwind.

### Exercise 2

Define the buffer and request state machine for a DMA transmit ring. Cover CPU preparation, mapping, publication, device ownership, completion, timeout, reset, unmapping, generation reuse, and surprise removal.

### Exercise 3

Design a hot-unplug protocol for a character device with open files, memory mappings, a timer, a work queue, shared interrupts, and device DMA. State which objects can outlive hardware and module unload.

### Exercise 4

Specify a module admission policy for a production fleet and a separate development policy. Cover build identity, reproducibility, signing keys, revocation, load authority, automatic aliases, audit, taint, rollback, and disabling further loads.

### Exercise 5

Construct an assurance review for a safety-critical driver. Separate static analysis, fault injection, emulation, real hardware, timing, power, firmware, security, operational monitoring, and named human judgment.

## Answers to the Exercises

### Answer 1

Match bus identifiers, then verify revision and ownership without destructive access. Enable the function and request its register regions; map registers; set the supported DMA mask; allocate software queues and DMA-visible rings; initialize the device while interrupts remain masked; register and synchronize the interrupt path; register the network instance; then mark it live and open user-visible service. Each step records one release obligation.

Inject failure before and after every acquisition. Before publication, unwind in reverse: unregister the interrupt if registered, stop initialized hardware, unmap and free DMA rings, release queues, unmap registers, release regions, and disable the function. If subsystem registration partially publishes callbacks, first close entry and drain them. Managed resources may encode mechanical release, but explicit device quiescence precedes their execution. Verify no device node, queue, mapping, interrupt handler, reference, or power vote survives a failed probe.

### Answer 2

Begin with a generation-tagged slot free and CPU-owned. The CPU reserves it, maps the buffer for the correct direction, writes bounded descriptor fields, performs required DMA synchronization, and release-publishes the producer state. Ownership becomes device. The CPU no longer mutates or unmaps the region. Hardware fetches, transmits, writes completion status under its protocol, and raises or batches notification.

The completion path validates ring index, generation, length, and device state, synchronizes ownership back to the CPU, consumes status, unmaps if the API requires, completes the request once, and increments the generation before reuse. Timeout first prevents duplicate completion; reset masks interrupts, stops fetch and DMA, fences transactions, drains handlers, retires old generations, and resolves every request as completed or failed. Surprise removal takes the gone path without unsafe register access. A stale completion from an earlier epoch must fail generation validation.

### Answer 3

Under the lookup lock, mark the instance gone so new opens and operations fail. Remove its discoverable name at the subsystem-defined point, stop new submissions, disable the timer's ability to rearm, mask the device source, stop command fetch and DMA, then synchronize the shared interrupt. Cancel and drain the timer and work queue, including self-requeue paths. Revoke or fault device-backed mappings according to their ABI, and wait for device transactions before unmapping DMA and registers.

Open file objects may retain a reference to software state so reads or closes return a stable removal error, but they cannot touch hardware. Memory not dependent on device access may outlive physical removal until the last file and mapping ends. Module text must outlive every file operation, fault handler, timer, worker, interrupt, callback, and release function; if policy permits open handles across unplug, those references prevent unload. A timeout does not justify forced release.

### Answer 4

Production accepts only artifacts built for an exact recorded kernel identity from a reproducible, reviewed pipeline. Sign after verification with protected keys; enroll only necessary trust anchors; define revocation and emergency rotation; restrict loader authority; inventory modules and dependencies; limit automatic aliases; make module storage immutable or measured; audit every load; treat taint as diagnostic evidence; support atomic rollback; and disable further loading after boot where operations permit.

Development uses separate nonproduction keys, hosts, and telemetry and may allow unsigned modules only on isolated systems. It records build configuration and taint, blocks production credentials and data, and preserves crash artifacts. Neither policy equates signature with correctness. Release gates require static analysis, lifecycle fault injection, target-kernel tests, and relevant hardware results before a module moves from development trust to production trust.

### Answer 5

Define safe output, timing deadlines, device authority, corruption containment, loss-of-communication behavior, reset semantics, and power-failure response. Static analysis covers API use, bounds, integer arithmetic, locking, and lifetime patterns. Sanitized fault injection exercises every probe and service allocation, malformed descriptors, duplicate and lost events, cancellation, timeout, and teardown. Emulation explores deterministic interleavings and device faults but records model limitations.

Test production hardware revisions for register semantics, DMA ordering, IOMMU isolation, interrupt latency and storms, queue saturation, reset, firmware versions, thermal and power transitions, and surprise loss. Measure high-percentile timing under full system load and observation overhead. Verify signed-build provenance, key operations, least-privilege interfaces, update recovery, monitoring, alarms, and safe-state drills. A named driver maintainer, hardware owner, real-time specialist, security reviewer, safety authority, independent verifier, and acceptance owner must assess coverage and residual risk. This chapter and toy lifecycle model claim no external certification.
