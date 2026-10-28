---
module_id: OS-006
program: Operating Systems
level: 1
module_number: 6
title: Boot Process and Kernel Initialization
status: complete
last_verified: 2026-09-04
---

# Boot Process and Kernel Initialization

## One-Page Review

### Governing question

How does a machine move from reset state to a protected, concurrent operating system without using services before they exist or trusting handoff data beyond its contract?

### Essential definitions

- **Reset state** is the architecture-defined processor state from which firmware begins; exact registers, privilege, addressability, and active cores are platform-specific.
- **Firmware** initializes enough platform hardware and exposes interfaces or description data used by later boot stages.
- A **boot manager or bootloader** selects, validates under configured policy, loads, and transfers control to an OS image with a defined handoff.
- A **boot protocol** specifies entry state, image placement, registers, memory maps, platform tables, command line, and optional initial filesystem supplied to a kernel.
- **Early kernel initialization** establishes execution, memory, exception, and diagnostic foundations before general kernel facilities are available.
- An **initcall** is an initialization routine ordered by explicit framework and dependencies rather than ordinary runtime discovery alone.
- **Initial user space** is the first process environment started by the kernel, often using an initramfs before or while the persistent root filesystem is located.

### Central model, mechanism, or theorem

Boot is a sequence of narrowing contracts and expanding invariants:

`reset -> firmware -> loader -> early_kernel -> core_kernel -> devices -> initial_user_space`.

At each handoff, the receiving stage validates inputs it can validate, records their provenance and lifetime, establishes the prerequisites for the next stage, and retires interfaces that will no longer be safe. Correctness is not “run these functions in order”; it is a dependency graph whose nodes have preconditions, owned resources, published postconditions, and failure policy.

### Critical invariants

- The selected image, configuration, and platform data have known provenance under the configured trust policy.
- The kernel does not overwrite its image, handoff data, firmware-reserved regions, initramfs, stacks, or early allocation state.
- Each initialization routine runs only after its dependencies and publishes state only when fully usable.
- Exception vectors and trusted stacks exist before exceptions or interrupts are enabled.
- General allocation replaces bootstrap allocation only after existing objects remain addressable and reserved.
- Secondary processors observe fully initialized shared state before entering schedulable execution.
- Failure chooses an explicit retry, alternate boot, recovery, degraded mode, or halt; it does not continue through an invalid partial state.

### Common failures

Frequent mistakes are treating UEFI as the only firmware model, assuming Secure Boot measures or makes all code safe, trusting command-line and device-description data, freeing boot memory too early, enabling interrupts before handlers, running init routines by incidental link order, releasing secondary CPUs before publication, hiding a hung dependency behind a longer timeout, and treating arrival at a login prompt as proof of a trustworthy or repeatable boot.

### Compact example

A loader places a kernel image and initramfs in permitted RAM, supplies a memory map and platform description, and enters at the documented address and processor mode. Early kernel code validates the handoff, reserves occupied ranges, installs a temporary mapping and stack, records diagnostics, and creates exception vectors. It initializes the physical allocator before the general heap, then interrupts, clocks, scheduler, and device frameworks in dependency order. Only after the root path is available does it start initial user space. A missing root device produces a diagnosed recovery path rather than execution with uninitialized storage state.

### Connections

[OS-002](002-privilege-levels-and-protection-rings.md) defines privilege setup, [OS-004](004-interrupts-and-exceptions.md) defines event entry, and [OS-005](005-kernel-architectures-monolithic-microkernel-and-hybrid.md) determines component placement. [OS-007](../ROADMAP.md) and [OS-008](../ROADMAP.md) develop initialized data structures and allocators. Platform handoffs connect to [Computer Architecture](../../23-computer-architecture/ROADMAP.md) and trust chains to [Security Engineering](../../25-security-engineering/ROADMAP.md).

## Governing Question

Operating-system explanations usually begin with abstractions already working: memory can be allocated, locks can block, clocks advance, interrupts have handlers, drivers can log, and processes can run. At reset, none of those kernel services exists. Some processors may be held offline, memory availability may be only a firmware claim, and even the stack and address mode may follow a boot protocol rather than the kernel's steady-state convention.

Boot constructs those assumptions without circularity. A primitive allocator helps build a general allocator. Early console paths diagnose failures before the full device stack. One processor establishes shared state before others join. Firmware services may be usable before a handoff and forbidden afterward. The first user process depends on storage or an initial memory filesystem that itself depends on validated placement.

The governing problem is to order authority and resource transitions so that each stage consumes only established services and leaves an auditable, recoverable state for its successor.

## Why This Matters

Boot code runs rarely compared with steady-state paths but holds exceptional authority. It selects images, parses attacker-influenced configuration, constructs translation tables, discovers devices, installs interrupt vectors, initializes credentials, and determines which protection mechanisms become active. A bug can corrupt state before later defenses exist.

Initialization order is a major reliability surface. Implicit dependencies may work on one build and fail after link-order, CPU-count, firmware, or timing changes. Parallel device probing can expose races hidden by serial boots. A driver that returns success before its resources are ready lets downstream consumers observe partial state.

Boot also defines recovery. Failed upgrades, unavailable roots, invalid signatures, corrupt initramfs images, missing devices, and watchdog resets need explicit alternate paths. Fast boot is useful, but shortening time by omitting validation, diagnostics, rollback, or synchronization changes the system's assurance and operability.

## Prerequisites and Retrieval

Recall from [OS-004](004-interrupts-and-exceptions.md) that event entry requires protected vectors, stacks, and controller state. Recall from [OS-005](005-kernel-architectures-monolithic-microkernel-and-hybrid.md) that component placement determines authority and recovery boundaries. You should understand executable images, linking, privilege modes, page tables, caches, memory maps, device buses, interrupts, concurrency, cryptographic signatures, and filesystems.

Retrieve these distinctions:

- firmware, boot manager, bootloader, kernel, and initial user space are separate roles even when one image combines several;
- authentication verifies an artifact under a key policy, while measurement records evidence for later appraisal;
- a firmware memory map is input that must be preserved and reconciled, not a general allocator;
- discovering a device is not the same as binding a ready driver;
- completion of an init function is not necessarily publication of a usable service;
- boot success, boot integrity, availability, and correct application state are different claims.

## Learning Objectives

After completing this module, you should be able to:

- trace reset, firmware, loader, kernel, initramfs, root selection, and initial user-space handoffs;
- distinguish UEFI, architecture boot protocols, device tree, ACPI, and firmware-call interfaces;
- state entry and lifetime obligations for a kernel handoff;
- order early stacks, translation, memory reservation, allocators, exceptions, interrupts, timers, and schedulers;
- model initialization as a dependency graph with explicit publication and rollback;
- explain secondary-processor release and memory-ordering requirements;
- separate verified boot, measured boot, image correctness, and runtime security;
- diagnose early-boot hangs, dependency cycles, stale firmware data, and premature resource reuse;
- design boot-time, fault-injection, and provenance evidence;
- identify high-consequence boot claims requiring named human review.

## Core Exposition

### Reset and firmware

Reset behavior belongs to the processor and platform specifications. A designated bootstrap processor or hart commonly begins at a defined address and privilege state while other processors wait or execute firmware-specific paths. Caches, translation, memory controllers, and devices may be uninitialized or retain platform-defined reset values. Do not generalize one PC sequence to Arm servers, RISC-V systems, microcontrollers, or virtual machines.

Firmware establishes enough environment to select a boot path. It may train memory, enumerate buses, construct ACPI tables or a device tree, expose runtime or boot services, choose a console, and apply platform policy. Some work occurs in immutable roots, some in updateable firmware, and some in option ROMs or device firmware. Each expands the pre-OS attack and failure surface.

UEFI defines a boot manager, NVRAM boot variables, image loading, boot services, runtime services, and a handoff such as `ExitBootServices`. It is one standardized ecosystem, not the definition of boot itself. Other systems use platform firmware, a supervisor binary interface, a board-specific loader, a hypervisor contract, or a fixed image.

### Image selection and trust decisions

A boot manager chooses among configured entries, recovery paths, removable media, or network sources. A loader may understand filesystems, decompress an image, load modules and an initramfs, relocate addresses, and construct kernel parameters. Every parser operates before the normal OS defense stack and must bound lengths, arithmetic, nesting, decompression ratios, and overlapping ranges.

Secure Boot verifies signatures or hashes under configured key databases and policy before executing selected images. It can establish an authenticated chain under those assumptions. It does not prove that authenticated code is correct, that keys are well governed, that rollback is prevented, or that runtime policy is safe.

Measured boot records measurements—commonly into protected platform registers—for later appraisal or key-release policy. Measurement alone does not block execution. Verified and measured boot can coexist: one decides whether to run, the other records what ran. Claims must state algorithms, key ownership, revocation, rollback counters, mutable configuration, firmware coverage, and recovery behavior.

### The kernel handoff contract

A boot protocol states where the image and supporting blobs reside; processor mode, endianness, interrupt state, and translation assumptions; register arguments; available and reserved memory; platform description; command line; initramfs; and callable firmware interfaces. Linux x86 and arm64 contracts differ substantially.

The kernel treats this information as structured input. It validates magic, versions, sizes, alignments, addresses, integer overflow, overlaps, string termination, and supported flags. Some claims cannot be independently verified yet, such as whether firmware correctly describes physical topology, so the kernel records assumptions and applies architecture-specific reservations and quirks.

Lifetime is essential. If an ACPI table, device tree, memory map, command line, or initramfs will be read later, its pages must remain reserved or the data must be copied. Memory advertised as reclaimable becomes available only after the consuming stage and applicable firmware contracts permit reclamation.

### Earliest kernel execution

Early assembly code establishes a known execution context before ordinary compiled code can assume its ABI. Work can include selecting a bootstrap stack, clearing or relocating the uninitialized-data region, applying relocations, establishing a global or per-CPU base, transitioning privilege or execution mode, and constructing temporary page tables.

Order is architecture-specific. Instruction and data caches may require maintenance around loaded or relocated code. Translation changes require prescribed barriers and invalidations. Address-space randomization may choose a relocation while preserving all occupied and reserved ranges. Diagnostics initially use a firmware console, serial port, memory buffer, or other minimal mechanism with strict availability limits.

Failure here is difficult to observe. A halt before the console appears can look like no power, invalid entry mode, wrong image placement, page-table failure, or an exception with no vector. Durable designs provide staged markers, platform debug channels, watchdog policy, and reproducible image metadata without leaking secrets.

### Memory discovery and allocator bootstrap

The kernel builds a normalized physical-memory model from firmware ranges, image sections, platform reservations, device apertures, persistent regions, initramfs placement, crash-reserved areas, and architecture constraints. Overlapping or contradictory entries need deterministic conservative resolution. “RAM” is not synonymous with “free.”

An early allocator often hands out aligned regions monotonically because a general allocator's metadata does not yet exist. Every early allocation must be recorded so the later physical allocator excludes it. The system then initializes page metadata, free lists, zones or nodes, and a general kernel heap in dependency order.

The transition is a proof obligation: all live early objects remain mapped and reserved; unused bootstrap memory is reclaimed at a defined point; later allocation cannot overlap firmware runtime regions or devices; and concurrency begins only after allocator synchronization works.

### Exceptions, interrupts, clocks, and scheduling

Exception vectors and per-CPU or bootstrap stacks must exist before an exception can be handled safely. Early faults may require dedicated handlers because the full VM subsystem and diagnostics are absent. Interrupt controllers are initialized with sources masked or routed predictably before device drivers enable them.

Clocks and timers establish timekeeping and preemption inputs. Their ordering interacts with interrupt readiness, calibration, power management, and scheduler initialization. The scheduler needs task structures, per-CPU state, timing, run queues, locks, and an idle context before arbitrary threads can run.

Enabling interrupts is a publication boundary. Every source that can arrive must have valid vector, controller, stack, and handler state. A device must not assert into freed or uninitialized data. Conversely, leaving interrupts disabled during slow probing can violate watchdog or latency requirements.

### Secondary processors

The bootstrap processor constructs shared kernel state and releases secondary processors through architecture- and platform-defined mechanisms. Each secondary establishes a stack, per-CPU data, privilege and translation state, exception vectors, interrupt-controller interface, and scheduler context before becoming online.

Publication requires memory ordering. The boot processor initializes shared objects, executes required barriers, then signals release. A secondary observes the release with the matching ordering before reading those objects. A simple flag without the architecture's synchronization can expose partially initialized tables.

Failure policy must define whether the system continues with fewer CPUs, retries startup, isolates a failing core, or halts. CPU topology, interrupt affinity, timers, allocator locality, and scheduler domains must reflect only processors that reached the appropriate online state.

### Initcalls, discovery, and driver binding

Initialization frameworks group routines by level or explicit dependencies. Foundational buses and resource managers precede consumers. Discovery identifies hardware descriptions or bus functions; matching chooses a driver; probing acquires registers, interrupts, clocks, DMA mappings, and dependent services; successful publication makes a device available to clients.

Returning success before publication is complete creates races. Returning failure after partial acquisition requires reverse-order cleanup. Deferred probing can handle a dependency not yet ready, but indefinite deferral needs diagnostics that name the missing provider rather than silently hanging boot.

Parallel probing reduces elapsed time only when dependencies and shared resources are synchronized. It can reveal hidden reliance on serial link or enumeration order. Stable device identity should not depend solely on whichever concurrent probe finishes first.

### Initramfs, root, and initial user space

An initramfs supplies files already present in memory at boot. The kernel can unpack it as an initial root and execute an initial program. That environment may load drivers, assemble storage, unlock encryption, configure networking, verify or mount a persistent root, and transfer control to the system's long-lived init process.

This is a trust and ownership handoff, not merely a convenience archive. The initramfs image and command line influence privileged policy. Secrets used to unlock storage need controlled lifetime. Switching roots must preserve required mounts and process state while discarding obsolete files and memory where policy allows.

If the root is unavailable, distinguish not-yet-discovered from permanently absent, unauthorized, corrupt, and timed out. Recovery may choose another slot, a signed rescue environment, remote diagnosis, or a fail-safe halt. Infinite retries can defeat availability; immediate fallback can conceal a transient but recoverable delay.

### Observability, reproducibility, and boot time

Timestamped milestones reveal firmware, loader, early kernel, driver, root, and user-space contributions. A single “boot time” needs endpoints: power application, reset release, kernel entry, first process, service-ready, or application-ready. Parallel work makes summed routine durations exceed wall time, while dependency stalls may appear in consumers rather than providers.

Capture image digests, configuration, command line with secrets redacted, firmware versions, hardware identity, boot source, recovery selection, and failure reason. Persistent or remote logs help when local storage is the failure. Watchdogs must identify which stage owns feeding and what reset evidence survives.

Reproducibility requires more than an identical kernel file. Firmware configuration, NVRAM variables, keys, device firmware, platform tables, initramfs, root image, and mutable policy all affect the path. Provenance records should support diagnosis without claiming bit-for-bit hardware determinism.

## Definitions and Notation

Let boot stages form a directed graph `B = (S, E)`. Each stage `s ∈ S` has preconditions `pre(s)`, outputs `post(s)`, owned resources `own(s)`, accepted inputs `input(s)`, and a failure policy `fail(s)`. An edge `u -> v` means `post(u)` contributes to `pre(v)`.

A stage is ready when

`ready(s) ⇔ all predecessors completed ∧ pre(s) holds ∧ input(s) validates`.

Completion means outputs are fully published under the required memory ordering, not merely that a function returned. A valid schedule is a topological ordering of the acyclic dependency graph; dynamic discovery may add nodes and edges but must preserve cycle detection and diagnostics.

Let memory ranges be half-open intervals `[base, end)`. The free set is advertised usable memory minus kernel image, handoff blobs, early allocations, firmware reservations, devices, and other retained regions. Address-plus-length arithmetic is checked before interval construction.

For artifact `a`, `verified(a, policy)` means its authentication evidence satisfies a named key and rollback policy. `measured(a, log)` means a named digest and event were extended and recorded according to a measurement protocol. Neither predicate implies functional correctness.

## Mechanisms, Invariants, or Proof Structure

Review boot through seven obligations.

**Provenance integrity.** Firmware, loader, kernel, modules, initramfs, configuration, and recovery artifacts have identified sources, versions, verification or measurement status, key policy, and rollback behavior.

**Handoff integrity.** Entry mode, registers, memory ranges, platform tables, command line, image, and callable services match a versioned boot protocol; all indirect data is bounded and retained for its documented lifetime.

**Bootstrap integrity.** Stacks, relocations, page tables, caches, early diagnostics, and bootstrap allocations are established without relying on unavailable services or overlapping owned memory.

**Dependency integrity.** Initialization occurs only after prerequisites. Publication is synchronized and success means usable state. Cycles, deferred providers, timeouts, and partial cleanup produce actionable diagnostics.

**Concurrency integrity.** Interrupts and secondary processors begin only after vectors, stacks, controller state, per-CPU data, locks, allocators, timers, and scheduler context are ready and ordered.

**Transition integrity.** Firmware services retire at the contractual boundary; bootstrap memory, init sections, and temporary mappings are reclaimed only after last use; initial user space receives intentional authority.

**Failure integrity.** Invalid input, missing devices, failed processors, corrupt roots, bad upgrades, and watchdog resets choose explicit bounded recovery or halt and preserve sufficient evidence.

The executable model below topologically orders a small boot dependency graph and checks publication. It cannot emulate reset, firmware, memory maps, processors, or real driver timing.

<!-- bijux-verify: {"id":"toy-boot-dependencies","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"order=memory,vectors,interrupts,scheduler,drivers,root,user_space\ninterrupts-ready=yes\nuser-space-ready=yes\ncycle-detected=yes\n","stderr":""}} -->
```python
dependencies = {
    "memory": set(),
    "vectors": {"memory"},
    "interrupts": {"vectors"},
    "scheduler": {"memory", "interrupts"},
    "drivers": {"scheduler"},
    "root": {"drivers"},
    "user_space": {"root"},
}


def boot_order(graph):
    done, order = set(), []
    while len(order) < len(graph):
        ready = [name for name, needs in graph.items()
                 if name not in done and needs <= done]
        if not ready:
            raise ValueError("dependency cycle")
        name = sorted(ready)[0]
        done.add(name)
        order.append(name)
    return order


order = boot_order(dependencies)
print("order=" + ",".join(order))
print("interrupts-ready=" + ("yes" if order.index("vectors") < order.index("interrupts") else "no"))
print("user-space-ready=" + ("yes" if order[-1] == "user_space" else "no"))
try:
    boot_order({"a": {"b"}, "b": {"a"}})
except ValueError:
    print("cycle-detected=yes")
```

Passing proves only deterministic ordering and cycle detection for these Python sets. It does not show that real preconditions hold, that publication is correctly synchronized, that hardware descriptions are truthful, or that a deployed boot is secure.

## Alternatives and Trade-Offs

**Firmware-rich versus kernel-owned initialization.** Firmware can hide platform complexity and support shared boot policy. Moving work into the kernel can improve control and observability but duplicates platform knowledge and may violate firmware contracts.

**Direct kernel loading versus a feature-rich loader.** A small loader reduces pre-kernel code and parser surface. Rich loaders support filesystems, networking, menus, recovery, decompression, and multiple OSes but enlarge the early TCB and update problem.

**Built-in drivers versus loadable early modules.** Built-ins simplify availability of critical devices. Modules reduce the base image and support hardware variation, but their discovery, authentication, dependencies, and initramfs packaging become boot requirements.

**Serial versus parallel initialization.** Serial order is simpler and deterministic but may be slow. Parallel probing shortens independent work while demanding explicit dependencies, thread-safe publication, stable identity, and better traces.

**Polling versus interrupt-driven early devices.** Polling works before interrupt infrastructure and can simplify early consoles. It consumes CPU and needs timeouts. Interrupt-driven paths scale better after vectors, controller, scheduler, and handlers are ready.

**Immediate failure versus degraded boot.** Failing fast avoids operation under unknown assumptions. Degraded boot can preserve availability with fewer CPUs, devices, or services, but must state reduced guarantees and prevent unsafe use.

**Fast boot versus diagnostic and trust work.** Caching, skipped enumeration, parallel work, and abbreviated tests reduce latency. They need invalidation rules and must not bypass authentication, recovery, or evidence required by the threat and hazard models.

## Failure Modes and Misconceptions

1. **“Every machine boots through UEFI.”** Firmware and handoff models vary across architectures, boards, hypervisors, and embedded systems.
2. **“Secure Boot proves the image is correct.”** It authenticates under configured keys and policy; signed defects remain defects.
3. **“Measured boot blocks bad code.”** Measurement records evidence; enforcement requires an appraisal or release policy.
4. **“Firmware-marked RAM is immediately free.”** Images, tables, runtime regions, devices, and early allocations must be subtracted and retained by lifetime.
5. **“The command line is harmless text.”** It can select privileged policy and exercises an early parser.
6. **“Interrupts may be enabled once a vector address exists.”** Stacks, controller state, handlers, per-CPU data, and dependencies must also be ready.
7. **“A returned init routine published a service.”** Asynchronous setup and missing barriers can expose partial state.
8. **“Link order is a dependency model.”** Incidental order is fragile across builds and configurations.
9. **“Secondary CPUs see bootstrap writes automatically.”** Release and observation need architecture-defined synchronization.
10. **“Deferred probe always resolves eventually.”** Missing providers and dependency cycles need bounded diagnosis.
11. **“Reaching user space means boot succeeded.”** Required services, trust policy, root correctness, and application readiness may still fail.
12. **“A longer timeout fixes slow boot.”** It may conceal a lost event, absent dependency, deadlock, or wrong device identity.
13. **“Recovery is safe because an older slot exists.”** Rollback policy, data compatibility, keys, and boot-attempt accounting must be correct.
14. **“One timestamp is boot performance.”** Endpoint, parallelism, firmware, loader, kernel, devices, and service readiness must be separated.

## Worked Examples

### Example 1

**Question:** Why must the kernel reserve its initramfs before starting the physical allocator?

**Reasoning:** The archive occupies physical pages supplied by the loader and will be read later. If those pages enter the free set, allocator clients can overwrite the archive before unpacking.

**Conclusion:** Handoff data remains owned until copied, consumed, or explicitly reclaimed.

### Example 2

**Question:** A signed kernel contains a privilege-escalation defect. Did Secure Boot prevent it?

**Reasoning:** Signature validation can establish that the image was authorized by the configured key policy. It does not establish functional correctness or absence of vulnerabilities.

**Conclusion:** Artifact authentication and software correctness require different evidence.

### Example 3

**Question:** Why install exception vectors before enabling a general allocator?

**Reasoning:** Page-table construction, cache setup, or allocator bootstrap can itself fault. Without a valid vector and stack, the original diagnosable error becomes uncontrolled entry or reset.

**Conclusion:** Early recovery and diagnostics are prerequisites for risky initialization, even if their handlers are minimal.

### Example 4

**Question:** A secondary CPU reads a zero pointer even though the bootstrap CPU assigned it before release. What is missing?

**Reasoning:** Compiler and hardware ordering may let the release become visible before the pointed-to data. The protocol needs the architecture's publishing barrier and matching acquire observation.

**Conclusion:** CPU startup is a concurrent publication protocol, not only a power-control action.

### Example 5

**Question:** A driver probe returns “defer” forever. Why is this more than slow hardware?

**Reasoning:** The required clock, bus, regulator, firmware, or parent may never publish, a dependency cycle may exist, or identity may be wrong. Repetition without a dependency trace cannot distinguish them.

**Conclusion:** Deferred initialization needs provider tracking, cycle awareness, a budget, and an actionable failure path.

### Example 6

**Question:** Can boot memory be reclaimed as soon as the general allocator starts?

**Reasoning:** Some early objects, tables, code, and firmware regions remain in use beyond allocator initialization. Reclamation follows last-use and contract boundaries, not one global moment.

**Conclusion:** Track lifetimes by region and owner before adding pages to free pools.

### Example 7

**Question:** Parallel probing changes which identical disk becomes `disk0`. What invariant failed?

**Reasoning:** A user-visible identity depended on completion order rather than stable hardware path, identifier, or policy. Timing changed naming and possibly root selection.

**Conclusion:** Concurrency requires stable identity independent of scheduler races.

### Example 8

**Question:** Why can initial user space be necessary to mount the real root?

**Reasoning:** The root may require storage drivers, RAID assembly, network configuration, integrity verification, or key acquisition. An initramfs supplies those tools before the persistent root is available.

**Conclusion:** Root discovery can be a privileged user-space workflow with its own trust and recovery boundary.

### Example 9

**Question:** A boot optimization reuses a cached device inventory. What must invalidate it?

**Reasoning:** Hardware changes, firmware updates, reset reason, device errors, hotplug state, and configuration changes can make it stale. Using stale resource ranges or identities can be unsafe.

**Conclusion:** Cached discovery needs provenance, validity predicates, fallback enumeration, and diagnostics.

### Example 10

**Question:** A surgical robot reaches its control application within the deadline. Is boot readiness established?

**Reasoning:** The application may lack calibrated sensors, verified actuator state, synchronized clocks, required redundancy, or completed self-tests. Process start is only one milestone.

**Conclusion:** A named safety authority must approve the application-ready definition, fault tests, recovery, and residual risk; this chapter claims no certification.

## Cross-Program Connections

[Computer Architecture](../../23-computer-architecture/ROADMAP.md) owns reset state, privilege, caches, translation, barriers, interrupts, and processor startup. This module composes those mechanisms with OS memory ownership, initialization dependencies, devices, and user-space launch. [Compilers and Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md) connects image layout, relocation, ABI, and initialization sections.

[Security Engineering](../../25-security-engineering/ROADMAP.md) develops roots of trust, signature policy, measurement, rollback prevention, key lifecycle, and early parser threats. [Cloud and Infrastructure Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) connects image selection, immutable infrastructure, recovery slots, provisioning, and readiness above the machine.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) adds startup-state requirements, hazard analysis, watchdog ownership, traceability, degraded-mode policy, and accountable acceptance. Successors [OS-007](../ROADMAP.md), [OS-008](../ROADMAP.md), and [OS-009](../ROADMAP.md) deepen kernel data structures, allocation, modules, and drivers initialized here.

## References

- Linux Kernel documentation, [The EFI Boot Stub](https://docs.kernel.org/admin-guide/efi-stub.html), current page checked 2026-09-04. Documents loading the Linux kernel as a PE/COFF EFI image and the firmware-to-kernel path.
- TianoCore project, [Understanding the UEFI Secure Boot Chain](https://github.com/tianocore-docs/Understanding_UEFI_Secure_Boot_Chain/blob/main/secure_boot_chain_in_uefi/uefi_secure_boot.md), current source checked 2026-09-04. Implementation-oriented account of image verification and UEFI key databases.
- Linux Kernel documentation, [ACPI Support](https://docs.kernel.org/firmware-guide/acpi/index.html), current page checked 2026-09-04. Kernel-facing platform-description and OS-directed configuration guidance.
- Devicetree Specification project, [Devicetree Specification](https://devicetree-specification.readthedocs.io/en/stable/), current specification checked 2026-09-04. Normative tree structure, properties, addressing, and boot-program-to-client interface.
- Linux Kernel documentation, [The Linux/x86 Boot Protocol](https://docs.kernel.org/arch/x86/boot.html), current page checked 2026-09-04. Architecture-specific image, setup-data, memory, command-line, and entry contract.
- Linux Kernel documentation, [Booting AArch64 Linux](https://docs.kernel.org/arch/arm64/booting.html), current page checked 2026-09-04. Architecture-specific image placement, device-tree, register, MMU, cache, and interrupt-controller requirements.
- Linux Kernel documentation, [Explaining the “No working init found” boot hang message](https://docs.kernel.org/admin-guide/init.html), current page checked 2026-09-04. Diagnostic boundaries between kernel root setup and initial user-space execution.
- Linux Kernel documentation, [Ramfs, rootfs and initramfs](https://docs.kernel.org/filesystems/ramfs-rootfs-initramfs.html), current page checked 2026-09-04. Documents Linux initial-root construction and the first user-space program.
- RISC-V International, [RISC-V Boot and Runtime Services specification source](https://github.com/riscv-non-isa/riscv-brs), current source checked 2026-09-04. Platform boot, discovery, handoff, UEFI, device-tree, ACPI, and Supervisor Binary Interface requirements.
- Linux Kernel documentation, [TPM Event Log](https://docs.kernel.org/security/tpm/tpm_event_log.html), current page checked 2026-09-04. Documents the firmware measurement log exposed for operating-system appraisal and diagnosis.
- GNU Project, [GNU GRUB Manual: Loading an operating system directly](https://www.gnu.org/software/grub/manual/grub/html_node/Loading-an-operating-system-directly.html), current page checked 2026-09-04. Bootloader treatment of direct OS image and multiboot loading.
- Russ Cox, Frans Kaashoek, and Robert Morris, [*xv6: a simple, Unix-like teaching operating system*](https://pdos.csail.mit.edu/6.1810/2025/xv6/book-riscv-rev5.pdf), MIT, 2025 edition. Teaching implementation of RISC-V kernel entry, page-table and allocator initialization, traps, devices, processes, and first user space.

## Exercises

### Exercise 1

Construct a boot-stage contract from loader to kernel. Include processor state, image and initramfs intervals, memory map, platform description, command line, firmware services, validation, ownership, lifetime, and failure behavior.

### Exercise 2

Order bootstrap stack, early console, exception vectors, temporary page tables, physical-memory model, early allocator, general allocator, interrupt controller, timer, scheduler, secondary CPUs, and device probing. Identify architecture-dependent edges and justify every universal dependency.

### Exercise 3

Design a parallel driver-initialization graph with a bus, clock, regulator, interrupt controller, storage device, network device, and encrypted root. Define readiness publication, deferred dependencies, cycle diagnosis, rollback, and stable identity.

### Exercise 4

Design a boot-evidence and fault-injection campaign for two-slot signed upgrades. Cover keys, rollback counters, measurements, corrupt artifacts, power loss, failed attempts, incompatible data, missing roots, watchdogs, recovery authentication, and audit retention.

### Exercise 5

An industrial controller claims it is safe when its control process starts within five seconds. Construct the review needed to define and verify actual readiness, including sensors, actuators, clocks, communications, degraded modes, physical safeguards, and named human judgment.

## Answers to the Exercises

### Answer 1

Version the contract and name the architecture. State entry privilege and execution mode, interrupt and MMU state, cache requirements, stack responsibility, register arguments, image format, relocation support, and permitted placement. Represent image, initramfs, platform tables, command line, and setup data as checked half-open intervals; reject overflow and forbidden overlap. Normalize usable, reserved, reclaimable, runtime, persistent, and device ranges conservatively.

Validate magic, versions, lengths, alignment, flags, string termination, node or table bounds, and supported firmware calls. Record which data is authenticated or measured and under which policy; do not infer correctness. Copy or reserve every input until its last consumer. Define the exact firmware-service retirement boundary and ownership of memory afterward. On failure, preserve a stage and reason code and choose a specified alternate image, authenticated recovery environment, or halt rather than continuing with partial assumptions.

### Answer 2

A bootstrap stack precedes ordinary calls. Minimal exception vectors should precede operations that can fault; a minimal diagnostic channel should be available as early as platform contracts allow. Temporary page tables precede execution at virtual addresses. The physical-memory model must reserve the image, stacks, tables, firmware regions, and handoff blobs before an early allocator can allocate safely. The general allocator follows page metadata and inherited early reservations.

The interrupt controller and vectors precede enabling interrupts; a timer and interrupt path precede preemptive scheduling. Scheduler structures, per-CPU state, stacks, translation, and ordered shared publication precede marking secondary CPUs online. Device probing follows its bus, clocks, regulators, DMA, interrupt, allocation, and synchronization providers. Some ordering—whether translation is initially enabled, how caches are maintained, how CPUs start, when firmware calls end—is architecture and boot-protocol specific and must be derived from those specifications rather than declared universal.

### Answer 3

Create provider edges from bus to each device, clock and regulator to consumers, interrupt controller to interrupt-driven devices, and storage plus cryptographic and policy services to encrypted root. A node becomes ready only after providers publish fully initialized handles with release ordering; consumers acquire those handles before use. A probe that lacks a provider registers the exact dependency rather than retrying anonymously.

Detect strongly connected unresolved dependencies and report their paths. Bound deferral attempts or time, distinguishing absent hardware from a slow asynchronous provider. On probe failure, revoke publication and release interrupts, DMA, mappings, clocks, regulators, allocations, and parent references in reverse ownership order. Parallel completion cannot assign durable names; use firmware path, serial identity, or explicit policy. Root selection waits for the named stable device and reports wrong identity separately from timeout.

### Answer 4

Inventory firmware, loader, kernel, modules, initramfs, configuration, root images, keys, revocation databases, rollback counters, measurement registers, and recovery artifacts by immutable identifier. Verify signature policy for both slots and recovery, key rotation and revocation, anti-rollback behavior, event-log correspondence, boot-attempt counters, and reset-resistant state.

Inject invalid signatures, corrupt headers, truncation, decompression bombs, wrong versions, missing initramfs, unavailable roots, bad counters, revoked keys, power loss during image and metadata writes, watchdog resets at every state transition, lost success acknowledgement, and data formats incompatible with rollback. Confirm atomic slot selection, bounded attempts, authenticated recovery, explicit unknown states, and preservation of the last bootable path. Retain tamper-evident stage, artifact, decision, reset, and recovery evidence with secrets redacted. Passing signature tests does not establish application correctness or safe data migration.

### Answer 5

Define readiness from the hazard analysis, not process existence. Required sensors must be identified, calibrated, fresh, and within diagnostic bounds; actuators must report known state and enforce command limits; clocks must meet synchronization and drift bounds; communications must be authenticated and timely; required redundancy and watchdogs must be active. Each prerequisite needs an observable publication event and a timeout leading to a defined degraded or safe state.

Measure reset-to-ready and every substage under cold, warm, update, maximum-load, component-loss, and recovery conditions at required percentiles and worst credible interference. Inject missing, stale, delayed, contradictory, and corrupt sensor and platform data; actuator faults; clock failures; network loss; storage corruption; CPU loss; boot loops; and incomplete upgrades. Verify independent physical interlocks and safe-state behavior. A named control engineer, domain operator, safety authority, security reviewer, and acceptance owner must approve requirements, traceability, test representativeness, independence, unresolved findings, and residual risk. This chapter and its dependency model claim no external certification.
