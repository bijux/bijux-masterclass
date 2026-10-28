---
module_id: OS-096
program: Operating Systems
level: 2
module_number: 96
title: Crash Dumps and Kernel Debugging
status: complete
last_verified: 2026-09-04
---

# Crash Dumps and Kernel Debugging

## One-Page Review

### Governing question

How can an operating-system team preserve trustworthy first-failure evidence, capture useful kernel state after integrity may be lost, reconstruct it against the exact build, and debug without turning diagnostics into a new outage or data leak?

### Essential definitions

- A **warning** reports a violated expectation while the kernel may continue; an **oops** reports a serious fault that may terminate the current context and taint continued execution.
- A **panic** is a terminal kernel failure path that stops or restarts the system according to policy.
- A **hang or lockup** is loss of required progress; it may produce no ordinary exception or log without watchdog or external intervention.
- A **vmcore** is an ELF-formatted representation of selected crashed-kernel physical memory and metadata exposed to a dump-capture environment.
- **kdump** preserves crashed-kernel memory while entering a preloaded capture kernel in reserved memory through crash kexec.
- **VMCOREINFO** records kernel-specific symbols, offsets, sizes, constants and configuration used by dump tools to interpret memory layout.
- **symbolization** maps runtime program counters and stack addresses to the matching image, modules, source and line information.
- A **postmortem debugger** inspects preserved state without executing the crashed kernel; a **live debugger** controls or inspects a running target and changes its timing and availability.

### Central model, mechanism, or theorem

Crash analysis follows an evidence chain:

`latent defect -> first invalid transition -> first detectable symptom -> warning/oops/panic/hang -> stabilization -> capture handoff -> stored evidence -> exact-build reconstruction -> hypothesis -> controlled reproduction -> root-cause fix -> regression proof`.

Each edge can lose or corrupt information. A dump is a later snapshot, not the defect itself. Reliable diagnosis preserves earliest evidence, records capture omissions, binds memory to exact executable and module identities, checks structural consistency before trusting pointers, and validates the proposed mechanism through a reproducer and negative test.

### Critical invariants

- Panic, oops, watchdog and manual triggers are configured deliberately and produce distinguishable outcomes.
- The capture kernel and required storage/network path are loaded, reserved, authenticated and tested before failure.
- Capture operations avoid dependencies likely corrupted or unavailable in panic context, including ordinary allocation, scheduling, locks and unsafe DMA assumptions.
- Raw logs, registers, stacks, taint, CPU state, hardware identity and build IDs are preserved before transformation.
- `vmlinux`, modules, debug information, source, configuration and relocation state match the crashed kernel exactly.
- Dump filtering and compression document excluded pages, errors and privacy consequences.
- Production debugging never executes untrusted commands in a possibly compromised kernel or exports unredacted memory without authorization.

### Common failures

Frequent failures are reading only the last panic line, continuing after an oops until evidence is overwritten, reserving too little capture memory, loading the dump kernel after the failure, relying on the failed root disk, reusing ordinary drivers in corrupt state, allowing stale DMA to damage capture memory, collecting a truncated vmcore without noticing, symbolizing against the nearest package version, ignoring modules and KASLR, trusting every unwind frame, sharing dumps as ordinary logs, reproducing on production, and declaring a reboot a fix.

### Compact example

A fleet reserves and preloads a minimal signed capture kernel during healthy boot. A watchdog converts a defined hard lockup into the crash path. The capture environment boots from reserved memory, resets only validated devices, writes an encrypted filtered vmcore and manifest to isolated storage, and reports omitted/unreadable pages. Analysis selects `vmlinux`, modules, BTF and source by build ID, applies recorded relocation, inspects the first CPU fault and allocation history, and treats later panics as consequences. A minimized reset race reproduces in a VM and on sacrificial hardware; the ownership fix is stress-tested with fault injection before rollout.

### Connections

Crash capture connects boot reservation, memory layout, exception handling, watchdogs, storage and networking, build reproducibility, symbols and unwinding, security response, fault injection and fleet recovery.

## Governing Question

When a kernel fails, the diagnostic machinery runs in the environment least able to support it. Allocators may be corrupt, locks held, interrupts disabled, CPUs unresponsive, devices mid-DMA and storage inconsistent. The code that would normally flush logs or contact a service may depend on the failed subsystem.

Postmortem analysis faces a second uncertainty. The visible faulting instruction may only be the first detected consequence of corruption that occurred seconds earlier. Stacks can be incomplete, registers can reflect exception entry, and memory can change while CPUs are being stopped. A filtered dump intentionally omits state.

The governing question is how to design capture before failure, interpret evidence conservatively afterward, and prove a correction without repeating a dangerous event on production systems.

## Why This Matters

Kernel faults can corrupt tenant memory, credentials, filesystems and devices. Fast reboot improves availability but erases volatile evidence and may return a vulnerable host to service. Waiting indefinitely for a full dump can worsen an outage. The response policy must balance integrity, evidence and recovery objectives.

Full memory can include disk keys, credentials, application payloads, personal data and cross-tenant state. A vmcore is often more sensitive than ordinary telemetry. Encryption at rest is insufficient if capture transmits to the wrong tenant or analysts receive unrestricted access.

Debug builds and live debuggers also perturb execution. Breakpoints stop CPUs, serial links change timing, debug information affects layout, and sanitizer configurations expose different races. The strongest diagnosis combines raw production evidence with controlled reproduction and mechanism-specific tests.

## Prerequisites and Retrieval

Before studying this module, be able to:

- explain exception entry, per-CPU state, kernel virtual memory and KASLR;
- distinguish panic, reboot, power loss, hang, watchdog and machine check;
- read assembly, registers, call stacks and symbol offsets;
- reason about storage durability, DMA ownership and encrypted transport;
- distinguish correlation, first symptom, root cause and reproducible mechanism.

Retrieve kernel release and build ID; complete configuration; compiler/linker; `vmlinux` and detached debug data; module names, build IDs, load addresses and signatures; source revision; boot command line; KASLR slide or relocation evidence; firmware and microcode; hardware inventory; taint flags; panic/oops/watchdog policy; crashkernel reservation; loaded capture image and initramfs; capture-kernel config; storage/network target; dump filter and compression settings; vmcore and VMCOREINFO; kernel logs; per-CPU registers and stacks; lost-record indicators; timestamps; reboot reason; prior warnings; workload; and chain-of-custody metadata.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish warnings, oopses, panics, hangs, lockups and hardware exceptions;
2. design and test a kdump capture path independent of likely production failures;
3. explain reserved memory, crash-kernel handoff, `/proc/vmcore` and VMCOREINFO;
4. preserve exact-build, module and relocation evidence for symbolization;
5. assess stack, pointer and filtered-page evidence under possible corruption;
6. choose pstore, netconsole, serial, postmortem or live debugging by failure class;
7. protect dump confidentiality, integrity, availability and custody;
8. turn a crash signature into a minimized reproducer, root-cause fix and regression evidence.

## Core Exposition

### Classify the terminal condition

A warning records an expectation failure and may taint later evidence. An oops kills or disrupts a context but can leave the kernel running in an uncertain state. A BUG path is a deliberate invariant trap. A panic enters system-wide failure policy. Hard and soft lockups report different progress failures. Machine checks may indicate hardware-detected corruption.

Record the exact trigger and policy. `panic_on_oops`, `panic_on_warn`, lockup panic settings and restart timeout change whether the same defect yields continued operation, a dump or immediate reboot.

### Preserve the first symptom

Later failures often cascade from the earliest corruption. Preserve sequence numbers, timestamps, CPU, task, interrupt state, first warning, taint changes and prior device errors. Do not discard an early recoverable warning because the eventual panic looks more severe.

Slow consoles can interleave or truncate output and alter timing. Use bounded multiple paths where risk justifies them, such as local ring buffer, persistent storage and remote console.

### Decide whether continued execution is safe

After an oops, locks can remain held, references unbalanced and memory partially modified. Continuing may preserve availability for a narrow failure or may silently corrupt durable state. Define subsystem and system escalation policy before incidents.

High-assurance or multi-tenant systems commonly favor containment and restart after integrity-relevant faults. Never interpret “the machine stayed up” as proof the state remained valid.

### Design capture before the crash

Kdump reserves memory for a capture kernel during healthy boot and loads the crash image in advance. On a qualifying failure, crash kexec transfers control while preserving the production kernel's memory for extraction.

Loading or configuring after panic is too late. Verify reservation, loaded image, command line, initramfs, signature/provenance and destination continuously across kernel and firmware updates.

### Size reserved memory empirically

The capture kernel needs code, page tables, initramfs, drivers, buffers and destination client under the target hardware and dump policy. Too little memory can fail only on the largest or most complex machines. Excess reservation permanently removes memory from normal workloads.

Test each supported memory tier, architecture, device path, encryption mode and compression setting. Treat automatic sizing as a policy to validate, not a universal guarantee.

### Keep the capture kernel minimal

Include only drivers and services needed to enumerate preserved memory and write the dump. Minimize filesystems, networking, shells and writable state. The capture environment is privileged and handles secrets from every crashed workload.

A familiar general-purpose image may have broader attack surface and depend on unavailable services. A tiny image can fail on hardware variation. Maintain an explicit compatibility matrix.

### Respect the crash handoff

The failed kernel prepares crash metadata and enters the preloaded image through architecture-specific mechanisms. The capture kernel receives an ELF core header location and exposes preserved physical memory as `/proc/vmcore`.

Not every CPU or device reaches a clean reset. Stop or isolate secondary CPUs according to the architecture. Record failures to collect per-CPU state rather than fabricating a coherent instant.

### Treat DMA as a threat to evidence

Devices programmed by the failed kernel may continue DMA into memory, including capture-kernel or evidence pages. Reserved placement, device shutdown, IOMMU state and capture-driver reset behavior affect integrity.

Do not assume rebooting through kexec resets hardware. Capture designs must state which devices can remain active and how the dump path prevents or detects corruption.

### Use panic-safe operations

Ordinary scheduling, allocation, locks and interrupt-driven I/O may not work after panic. Preallocate necessary memory and use explicitly supported polling or reset flows. Bound retries so an inaccessible destination does not stall recovery forever.

Panic notifiers and dump callbacks run under severe constraints. Keep them short, independent and ordered only by documented contracts.

### Choose a failure-independent destination

Writing to the crashed system's root storage can fail if the fault involved its driver, controller, filesystem or encryption service. A network path can fail if networking or credentials are implicated. Select local, remote and fallback targets from the failure model.

Preprovision authentication and keys without exposing them to workloads. Record partial-transfer state and checksum completed artifacts before marking capture successful.

### Understand vmcore structure

`/proc/vmcore` presents an ELF-format view of crashed memory plus notes such as CPU state and VMCOREINFO. It is a representation assembled under architecture and kernel rules, not necessarily a byte-for-byte file of every physical address.

Validate ELF headers, segments, bounds and notes before analysis. Record source size, stored size, filter policy, compressor version, checksum and any read errors.

### Use VMCOREINFO to interpret layout

Dump tools need structure sizes, member offsets, symbols, constants and configuration-dependent facts. VMCOREINFO packages selected values into an ELF note so a tool can navigate memory from the matching kernel.

It does not replace the exact debug image or validate every corrupted structure. Treat missing or inconsistent metadata as a limitation, not permission to guess offsets.

### Filter with explicit loss

Tools may exclude free pages, user pages, caches or other classes to reduce size. Filtering improves capture probability and privacy but can remove the object that explains corruption. Compression trades CPU and memory for transfer volume.

Choose filters by investigation goals and retention policy. Store the exact filter level and page exclusions; “dump complete” must mean complete under that declared policy.

### Bind every address to the exact build

Symbolization needs the precise unstripped `vmlinux`, debug data, source revision, compiler effects and module objects from the crashed system. Package version strings can hide local patches or rebuilds.

Use build IDs and artifact checksums. Preserve module load addresses and build IDs because modules relocate independently and can unload before failure.

### Account for KASLR and relocation

Runtime kernel and module addresses differ from link-time addresses. Recover the relocation slide from trusted crash metadata or tool-supported notes, then translate before source lookup. Never subtract a slide from an address belonging to another region.

An address that lands in a plausible symbol under the wrong slide can mislead more than an unresolved address. Cross-check several known symbols and build identity.

### Interpret registers by exception frame

Architecture, exception type, privilege transition and entry code determine which registers reflect the faulting context, which were saved later, and whether values are complete. The program counter may name the detected access rather than the corrupting write.

Decode fault status, access type, address and instruction bytes together. Check whether speculative, imprecise or asynchronous hardware reporting changes interpretation.

### Treat stack unwinding as evidence with assumptions

Frame pointers, ORC or other unwind metadata, debug info and architecture rules reconstruct call chains. Corrupted stacks, wrong metadata, exceptions, interrupts, tail calls and hand-written assembly can create missing or misleading frames.

Validate stack bounds, frame progression and executable addresses. Mark uncertain frames instead of presenting a polished but invented call path.

### Inspect multiple CPUs and tasks

The faulting CPU shows one local path. Other CPUs may hold locks, wait for the failed CPU, perform DMA teardown or contain the earlier warning. Inspect current tasks, run queues, interrupt state, locks and per-CPU data.

The stopped state is not perfectly simultaneous. Use sequence and ownership evidence to reason about allowed interleavings rather than treating every memory value as one atomic snapshot.

### Read taint as provenance

Taint flags record events relevant to interpretation, such as proprietary or out-of-tree modules, prior warnings, forced unload, machine checks, live patches or a previous oops. Taint commonly persists after the immediate condition is removed.

It does not prove causation. Preserve and decode it, then reproduce on an untainted kernel when possible without erasing evidence from the original environment.

### Use persistent logs for small evidence

Pstore backends such as ramoops can preserve bounded kernel messages or tracing across restart. They work when full kdump is unavailable and can capture shutdown hangs. Capacity and overwrite policy determine which records survive.

Reserve persistent RAM correctly and retrieve data before it is cleared or overwritten. A short log complements, rather than replaces, memory state.

### Use remote and serial consoles carefully

Netconsole or serial output can escape a failing local storage stack. Network paths can drop, reorder or expose sensitive messages, and console printing can be slow in critical context.

Authenticate or isolate receivers where supported by the deployment design, rate-limit normal floods and retain raw sequence evidence. Never claim delivery solely because a sender attempted output.

### Diagnose hangs without ordinary scheduling

A hung system may not run the logger, shell or dump trigger. Watchdogs, NMI-based diagnostics, SysRq, management controllers, JTAG or hypervisor interfaces provide more independent entry paths.

Each can perturb or terminate the target. Define whether the priority is a stack snapshot, full dump or rapid recovery and test the chosen escalation under actual lockup classes.

### Use SysRq under explicit authorization

Magic SysRq can dump tasks, adjust logging, sync, remount, signal processes, reboot or trigger a crash depending on configuration and invocation path. It is powerful production control, not a harmless debugging shortcut.

Restrict access, record the operator and reason, and practice safe sequences on nonproduction systems. An administrative write to the trigger interface has semantics distinct from keyboard policy.

### Choose live debugging for controlled targets

KDB offers console-oriented inspection and limited run control; KGDB connects a source debugger to a target. QEMU/KVM stubs and hardware debug interfaces support other controlled environments.

Breakpoints stop execution and can violate timeouts, device protocols and distributed leases. Use live debugging on isolated reproductions unless an approved incident procedure accepts the production effect.

### Keep host and target separate

A source debugger should use the matching `vmlinux` and scripts on a trusted analysis host. The target exposes a deliberately limited debug transport. Do not install an expansive toolchain into the capture kernel merely for convenience.

Assume a compromised target can send malicious or inconsistent debug data. Analysis parsers need bounds and isolation too.

### Reproduce safely

Translate the evidence into the smallest workload, configuration and interleaving that triggers the same first symptom. Start in a VM or emulator, then use sacrificial hardware for device- or timing-specific behavior.

Preserve the production signature while adding assertions, sanitizers, tracing or fault injection. A debug build that no longer fails may have changed layout or timing; that is evidence about sensitivity, not disproof.

### Minimize without deleting the cause

Reduce configuration, modules, workload and input one dimension at a time. Keep the exact known-good and known-bad results. Statistical races require repeated trials and confidence, not one success.

A minimal trigger need not be the root cause. It is an experimental handle used to test the ownership, bounds, ordering or device-state hypothesis.

### Bisect controlled regressions

Verify the problem on suitable current and baseline kernels with comparable configuration and environment. Use known-good/known-bad commits and automate a reliable test. Mark inconclusive results rather than forcing them to good or bad.

Build changes can move races and addresses. A bisected enabling change may expose an older defect; inspect mechanism before assigning causality.

### Inject failures deliberately

Kernel fault-injection facilities can fail allocations, user copies, I/O and selected functions. They test cleanup and recovery paths that ordinary workloads rarely reach. Combine them with sanitizers and state assertions.

Never enable broad injection on production by accident. Record probability, interval, task filtering, seed and exact injected site so results are reproducible.

### Protect dump confidentiality

Classify vmcores as highly sensitive. Encrypt transport and storage, authorize access by incident and tenant, log use, isolate analysis environments, bound retention and destroy expired copies. Filtering can reduce exposure but is not guaranteed redaction.

Redaction changes forensic completeness and can itself parse corrupt data. Preserve a governed raw source when policy permits and derive narrower analyst artifacts with lineage.

### Verify capture continuously

After every relevant kernel, initramfs, firmware, driver, storage, network or encryption update, confirm reservation and preload, trigger a controlled crash on a representative canary, validate artifact checksum and symbolization, and measure time to reboot.

A configured service is not a working crash path. Monitor last successful end-to-end test and reject unsupported fleet combinations.

### Recover before returning service

Capture success does not make the host trustworthy. Boot a known-good kernel, validate storage and device state, rotate possibly exposed secrets and quarantine hardware when machine errors are plausible. Correct the triggering condition before restoring workload.

Track crash signatures across rollout. A falling rate without matched exposure, uptime and workload can hide recurrence.

## Definitions and Notation

Let $t_0$ be the first invalid transition, $t_1$ the first detectable symptom, $t_2$ panic or stop initiation, $t_3$ capture-kernel entry, and $t_4$ durable dump completion. Typically

$$
t_0\le t_1\le t_2\le t_3\le t_4.
$$

The dump most directly describes state near $t_2$ through $t_3$; it does not automatically identify the event at $t_0$.

For total addressable crash pages $P$, unreadable pages $U$, deliberately excluded pages $E$, and stored pages $S$, a simplified accounting identity is

$$
P=S+U+E,
$$

only when classes are disjoint and every page is classified. Compression changes bytes, not page classification. A stored-page ratio is not semantic completeness.

For a runtime core-text address $a_r$, runtime text base $b_r$ and matching link-time text base $b_l$, a simplified relocation is

$$
a_l=b_l+(a_r-b_r),
$$

provided the address belongs to that relocated image and the bases match the exact build.

## Mechanisms, Invariants, or Proof Structure

1. **Trigger obligation:** define which warnings, oopses, panics, hangs, watchdogs and manual actions enter capture.
2. **Preparation obligation:** reserve memory and preload an authenticated capture kernel, initramfs, configuration and credentials while healthy.
3. **Independence obligation:** keep capture CPU, memory, device, storage and network dependencies outside likely failure domains where practical.
4. **Panic-safety obligation:** avoid unbounded waits, ordinary allocation, unsafe locks, scheduling and uncontrolled DMA after integrity loss.
5. **Preservation obligation:** retain first logs, CPU/task state, taint, build identities, metadata and raw artifact checksums.
6. **Completeness obligation:** record unreadable, excluded, overwritten, truncated and failed evidence explicitly.
7. **Reconstruction obligation:** match `vmlinux`, modules, debug data, source, configuration, VMCOREINFO and relocation.
8. **Interpretation obligation:** validate ELF, pointers, structures, frames, clocks and cross-CPU consistency before inference.
9. **Security obligation:** protect secrets, tenant boundaries, capture keys, analyst access and parser isolation.
10. **Reproduction obligation:** test the inferred mechanism on isolated, versioned and sufficiently repeated targets.
11. **Remediation obligation:** repair the violated invariant, inspect sibling patterns and prove regression behavior.
12. **Recovery obligation:** restore known-good kernel and state, rotate exposed material and monitor matched fleet exposure.

## Alternatives and Trade-Offs

- **Immediate reboot versus dump:** reboot minimizes outage; capture preserves evidence but extends recovery time.
- **Full dump versus filtered dump:** full memory maximizes potential evidence and secrets; filtering improves size and privacy while omitting causes.
- **Local disk versus remote destination:** local paths avoid network dependency; remote storage survives local disk failure and expands credential needs.
- **Standard reservation versus reclaimable crash memory:** dedicated memory improves reliability; reclaimable designs reduce idle cost with corruption risk.
- **Minimal versus general capture kernel:** minimal images reduce dependencies; broader images support more hardware and destinations.
- **Pstore versus vmcore:** pstore preserves small logs cheaply; vmcore enables structural memory analysis.
- **Netconsole versus persistent local logs:** remote output escapes local failure; it may lose records or expose data in transit.
- **Frame pointers versus compact unwind metadata:** frame pointers simplify some unwinds at cost; metadata can be efficient and build-dependent.
- **Postmortem versus live debugging:** postmortem preserves a fixed state; live control tests hypotheses while perturbing timing.
- **VM reproduction versus physical hardware:** VMs improve control and snapshots; hardware preserves real devices, firmware and timing.
- **Sanitizer build versus production build:** instrumentation exposes classes; it changes layout, overhead and schedules.
- **Automatic panic versus continued operation:** panic limits uncertain corruption; continuation may preserve service for scoped recoverable faults.
- **Automatic upload versus manual custody:** automation shortens diagnosis; manual approval better controls highly sensitive dumps.
- **Long retention versus minimization:** retention supports rare correlation; deletion reduces exposure and compliance burden.
- **Broad fault injection versus targeted injection:** broad campaigns discover interactions; targeted faults reproduce and attribute more easily.
- **Fast bisect test versus statistical confidence:** fast runs accelerate search; rare races need repeated classification and inconclusive outcomes.

## Failure Modes and Misconceptions

1. **“The panic line is the root cause.”** It may be the first detected consequence of earlier corruption.
2. **“An oops is recovered because execution continued.”** locks, references and state may remain invalid.
3. **“A hang will print a stack.”** ordinary logging may not run without watchdog or external entry.
4. **“Configuring kdump loads it forever.”** verify reservation and preloaded image after every relevant update and boot.
5. **“Reserved memory guarantees capture.”** image size, drivers, devices, destination and corruption still matter.
6. **“Kexec resets all hardware.”** devices and DMA may retain failed-kernel state.
7. **“The root disk is the safest dump target.”** it may share the failing subsystem.
8. **“Panic callbacks may use ordinary kernel services.”** scheduling, allocation and locks can be unavailable.
9. **“`/proc/vmcore` contains every physical byte.”** representation and filtering policies define coverage.
10. **“Compression loses semantic evidence.”** lossless compression preserves stored bytes; filtering removes pages.
11. **“A plausible symbol is the right symbol.”** exact build, module and relocation identity are required.
12. **“Kernel release text uniquely identifies a binary.”** local patches and rebuilds can share it.
13. **“KASLR is removed by guessing one address.”** validate the region and slide across several symbols.
14. **“Every unwind frame is authoritative.”** corruption, assembly and exception transitions can break unwinding.
15. **“All CPUs stopped at one instant.”** capture is a transition with possible missing or changing state.
16. **“Taint proves the listed module caused the crash.”** it records relevant history, not causation.
17. **“Pstore replaces a memory dump.”** its bounded logs answer fewer structural questions.
18. **“Netconsole delivery is guaranteed.”** the network and receiver can drop or fail.
19. **“SysRq is harmless diagnostics.”** it can sync, kill, reboot or deliberately crash a host.
20. **“A live breakpoint is observational.”** it changes timing, CPU progress and device behavior.
21. **“A VM-only fix proves a device race closed.”** physical DMA and firmware may be essential.
22. **“Failure disappearing under debug disproves it.”** instrumentation can perturb a race.
23. **“The first bad bisect commit contains the defect.”** it may expose an older latent fault.
24. **“A vmcore is just another log file.”** it can contain nearly every resident secret.
25. **“Successful capture means safe recovery.”** crashed persistent and hardware state still need validation.
26. **“No repeated signature means fixed.”** exposure, uptime or workload may have changed.

## Worked Examples

### Example 1

An allocation warning occurs, the system continues, and ten minutes later a NULL dereference panics. Preserving the earlier warning and taint redirects analysis from the final dereference to exhausted cleanup state.

### Example 2

The capture kernel boots but cannot mount the production root filesystem whose driver deadlocked. A pretested isolated network target succeeds because it does not reuse the failed storage path.

### Example 3

A NIC continues DMA after crash kexec and corrupts capture buffers. Resetting and isolating the device before reuse, or choosing another dump path, restores evidence integrity.

### Example 4

A filtered vmcore omits user pages that held an ioctl buffer. Kernel metadata identifies the pointer but not content. The report labels the missing payload rather than inventing an input.

### Example 5

Analysts symbolize against the same version string but a different local rebuild and blame the wrong source line. Build-ID matching and stored modules resolve the correct instruction.

### Example 6

One stack frame jumps outside kernel and module text after a buffer overwrite. The unwinder's earlier frames remain bounded, but the invalid tail is marked uncertain rather than used as a call chain.

### Example 7

Ramoops preserves a final shutdown trace after storage and networking stop. Its small persistent buffer supplies the missing ordering evidence without claiming a full memory snapshot.

### Example 8

KGDB breakpoint halts a CPU holding a device lock until hardware times out. The resulting fault is debugger-induced; reproducing with postmortem tracing distinguishes it from the original race.

### Example 9

A bisect test reproduces a race once in fifty runs. Classifying one quiet run as good sends the search to the wrong commit. Repeated trials and an inconclusive class preserve statistical validity.

### Example 10

A full vmcore from a multi-tenant host is attached to a public issue. Revoking the link does not revoke copied secrets. Controlled intake, encrypted restricted storage and a redacted derived report were required from capture time.

## Cross-Program Connections

- **Computer architecture:** exception frames, machine checks, debug registers, KASLR and DMA determine captured state.
- **Boot engineering:** reserved memory and the crash-kernel handoff must be established before ordinary services.
- **Memory management:** page tables, allocators, VMCOREINFO and filtered page classes make dumps interpretable.
- **Concurrency:** locks, per-CPU state, RCU, races and non-simultaneous stopping complicate root-cause reconstruction.
- **Storage engineering:** durability, encryption, partial writes and failed-device independence govern artifact capture.
- **Networking:** remote consoles and dump transfer add loss, authentication, congestion and failure dependencies.
- **Security engineering:** possible kernel compromise, resident secrets, custody and parser isolation shape response.
- **Testing engineering:** reproduction, sanitizers, fault injection, stress and bisection validate mechanisms.
- **Platform engineering:** canary crashes, artifact catalogs, fleet configuration and recovery objectives operationalize kdump.
- **Data engineering:** provenance, checksums, schemas, retention and redaction preserve evidence lineage.

## References

1. Linux Kernel Documentation, [Kdump: the kexec-based Crash Dumping Solution](https://docs.kernel.org/admin-guide/kdump/kdump.html), reserved memory, crash-kernel loading, `/proc/vmcore`, capture and analysis; retrieved 2026-09-04.
2. Linux Kernel Documentation, [VMCOREINFO](https://docs.kernel.org/admin-guide/kdump/vmcoreinfo.html), ELF notes, symbols, offsets, sizes, constants and dump-tool interpretation; retrieved 2026-09-04.
3. Linux Kernel Documentation, [Bug Hunting](https://docs.kernel.org/admin-guide/bug-hunting.html), oops collection, exact lines, stack decoding, GDB and object disassembly; retrieved 2026-09-04.
4. Linux Kernel Documentation, [Using KGDB, KDB and the Kernel Debugger Internals](https://docs.kernel.org/process/debugging/kgdb.html), live debugger front ends, transport and target/host roles; retrieved 2026-09-04.
5. Linux Kernel Documentation, [Debugging Kernel and Modules via GDB](https://docs.kernel.org/process/debugging/gdb-kernel-debugging.html), matching `vmlinux`, scripts, virtual targets and module debugging; retrieved 2026-09-04.
6. Linux Kernel Documentation, [Ramoops Oops/Panic Logger](https://docs.kernel.org/admin-guide/ramoops.html), persistent RAM reservation, bounded records and post-restart retrieval; retrieved 2026-09-04.
7. Linux Kernel Documentation, [Netconsole](https://docs.kernel.org/networking/netconsole.html), remote kernel-message transport and configuration; retrieved 2026-09-04.
8. Linux Kernel Documentation, [Magic SysRq](https://docs.kernel.org/admin-guide/sysrq.html), configuration, invocation paths and diagnostic or crash operations; retrieved 2026-09-04.
9. Linux Kernel Documentation, [Tainted Kernels](https://docs.kernel.org/admin-guide/tainted-kernels.html), persistent provenance flags and crash-report interpretation; retrieved 2026-09-04.
10. Linux Kernel Documentation, [Reporting Issues](https://docs.kernel.org/admin-guide/reporting-issues.html), decoding failures, environment evidence and actionable reports; retrieved 2026-09-04.
11. Linux Kernel Documentation, [Fault Injection Capabilities](https://docs.kernel.org/fault-injection/fault-injection.html), controlled allocation, user-copy, I/O and function failures; retrieved 2026-09-04.

## Exercises

### Exercise 1

Design kdump for a storage server whose likely failures include root-controller hangs, NIC faults, low memory and stale DMA. Specify reservation, capture image, destination, fallbacks, time bounds, testing and recovery.

### Exercise 2

A runtime fault address is `0xffffffffa12345d0`, runtime core-text base is `0xffffffffa1000000`, and matching link-time core-text base is `0xffffffff81000000`. Compute the link-time address and state what must be verified before symbolization.

### Exercise 3

Given an oops followed by three secondary panics, construct a first-fault analysis procedure covering logs, taint, registers, stacks, CPUs, modules, VMCOREINFO, filtered pages and competing hypotheses.

### Exercise 4

Plan safe reproduction and bisection for a race that occurs in roughly two percent of device resets and disappears under a debug build. Include trial classification, instrumentation and physical-hardware gates.

### Exercise 5

Define security and custody controls for vmcores from multi-tenant machines, including capture keys, transfer, raw access, derived artifacts, retention, deletion and incident reporting.

## Answers to the Exercises

### Answer 1

Reserve enough dedicated memory for a minimal authenticated capture kernel, initramfs, page tables, polling drivers, encryption and buffers on the largest supported machine. Load it during healthy boot and continuously verify the reservation and image identity. Avoid the root controller as the only destination. Preprovision an isolated capture network on a second validated device, with local persistent storage or a small pstore record as bounded fallbacks.

On crash, quiesce or reset devices under tested panic-safe rules, protect capture memory from stale DMA with appropriate IOMMU/device state, and bound connection and write retries. Store an encrypted vmcore, metadata manifest, exclusions, errors and checksums, then reboot to a known-good kernel even if upload fails. Test controlled panics, simulated root-disk loss, NIC loss, low memory, full destination, encryption failure and active DMA on representative canaries after updates. Recovery quarantines the server, validates storage/controllers and rotates exposed secrets before workload returns.

### Answer 2

The runtime offset is `0x2345d0`, so the matching link-time address is `0xffffffff812345d0`.

<!-- bijux-verify: {"id":"kernel-text-relocation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"runtime_offset 0x2345d0\nlink_address 0xffffffff812345d0\nround_trip true\n"}} -->
```python
runtime_address = 0xFFFFFFFFA12345D0
runtime_text_base = 0xFFFFFFFFA1000000
link_text_base = 0xFFFFFFFF81000000

offset = runtime_address - runtime_text_base
link_address = link_text_base + offset
round_trip = runtime_text_base + (link_address - link_text_base)
print("runtime_offset", hex(offset))
print("link_address", hex(link_address))
print("round_trip", str(round_trip == runtime_address).lower())
```

Before using the result, verify that the fault belongs to core text rather than a module, JIT or another region; match kernel build ID, image, debug data and source; obtain the actual runtime base from trustworthy dump metadata; and cross-check multiple known symbols. Arithmetic consistency alone does not validate any base or artifact.

### Answer 3

Freeze raw evidence and order records by stable sequence and clock evidence. Start with the earliest warning or oops, its CPU, task, interrupt and preemption context, fault status, registers and instruction bytes. Decode taint changes and earlier allocator, device, watchdog or machine-check messages. Treat later panics as possible consequences until their state transitions show independence.

Validate the vmcore ELF, VMCOREINFO, page coverage, truncation and checksums. Select exact `vmlinux`, modules, load addresses, debug files, configuration and source by build ID; apply KASLR per region. Unwind conservatively with stack bounds and metadata, marking corrupt frames. Inspect other CPU stacks, locks, run queues, work items and per-CPU ownership while acknowledging that stopping was not simultaneous. Follow pointers only after validating address class, object state and required pages. Compare hypotheses for earlier corruption, hardware error, module behavior and a direct local fault, then design observations or a reproducer that makes them predict different outcomes.

### Answer 4

Preserve the production build/configuration and automate one complete reset trial with an objective signature. Estimate reproduction probability from many baseline trials, then classify candidate revisions using enough repetitions to bound false-good risk; permit an inconclusive result. Keep hardware, firmware, workload, timing and reset method fixed and log every exposure.

Add low-perturbation tracepoints and reference/ownership history first. Use KASAN, KCSAN, lockdep or assertions in separate builds to expose mechanism, while recognizing that disappearance under instrumentation indicates schedule sensitivity. Reproduce in a VM when possible, but require sacrificial physical devices before closing DMA, firmware or reset claims. Bisect with matched configs and inspect the first exposing change for latent defects. The fix repairs teardown, ownership or ordering, then passes the vulnerable reproducer, stress, fault injection and fleet canaries under both diagnostic and release builds.

### Answer 5

Use per-environment capture credentials available to the minimal crash image, protected from workloads and revocable independently. Authenticate and encrypt transfer to an incident-specific tenant-aware destination; reject ambiguous ownership. Hash raw artifacts on receipt, record device/build/incident identity, capture policy, filter omissions, timestamps and every custody action.

Restrict raw vmcore access to named responders in isolated analysis environments without general outbound access. Create redacted or structurally filtered derivatives for broader teams, preserving checksums and transformation lineage and warning that filtering can omit evidence. Set incident- and regulation-based retention, legal holds and automatic expiry; verify deletion from replicas and caches. Reports expose only necessary symbols and facts, never raw resident payload. If a dump was misrouted or publicly disclosed, treat all recoverable tenant secrets as potentially exposed, revoke access, rotate credentials and notify through the applicable incident process.
