---
module_id: OS-002
program: Operating Systems
level: 1
module_number: 2
title: Privilege Levels and Protection Rings
status: complete
last_verified: 2026-08-29
---

# Privilege Levels and Protection Rings

## One-Page Review

### Governing question

How can a processor let an operating-system kernel control the machine while preventing ordinary application code from performing operations that would defeat protection?

### Essential definitions

- A **privilege level** is an architectural execution state that affects which instructions, registers, memory accesses, and transitions the processor permits.
- A **protection ring** is the x86 representation of ordered privilege levels: ring 0 is most privileged and ring 3 least privileged; rings 1 and 2 exist architecturally but mainstream general-purpose systems commonly concentrate on rings 0 and 3.
- **User mode** is the least-privileged application execution state; **kernel mode** is the state in which the OS can exercise the authority needed to manage hardware and protection mechanisms.
- A **privileged instruction** is rejected or trapped when attempted from a state without the required architectural privilege.
- A **controlled transition** changes privilege only through an architecturally defined entry path whose target, saved state, and return behavior the kernel configures.
- **Least privilege** gives a subject only the authority and duration needed for its task.
- A **protection domain** is a set of accessible objects and permitted operations; a CPU privilege level is one input to a domain, not the whole domain.

### Central model, mechanism, or theorem

Protection requires three cooperating layers:

`execution privilege × memory permissions × controlled transitions`.

Execution privilege restricts sensitive processor operations. Page and segment permissions restrict memory. Exception, interrupt, and system-call entry mechanisms transfer control to approved privileged code. If any layer is configured incorrectly, the boundary can fail even when the other two operate correctly.

### Critical invariants

- Unprivileged execution cannot directly perform privileged operations.
- Unprivileged memory access cannot read, write, or execute supervisor-only mappings.
- Privilege can increase only through an authorized entry mechanism to a validated target.
- Entry saves enough prior state for a checked return and switches to trusted kernel-owned execution state where required.
- The kernel validates every pointer, length, identifier, and requested operation received from a less-privileged caller.
- Return restores an authorized less-privileged state without leaking privileged registers, mappings, or control data.
- Privileged code is minimized and reviewed because hardware permits it to do more; the hardware does not make it correct.

### Common failures

Frequent mistakes are saying every architecture has four rings, treating ring number as user identity, assuming supervisor mode automatically isolates processes, believing a trap proves a request is authorized, trusting user pointers after validation, confusing CPU privilege with hypervisor or firmware authority, and treating a successful toy model as evidence about a real kernel.

### Compact example

An application attempts a privileged interrupt-control instruction. The processor rejects the instruction in user mode. The same application requests a service through an approved system-call entry. Hardware transfers control to a kernel-selected address and privileged stack; kernel code then validates the operation. The first attempt is forbidden execution, while the second is controlled delegation—not temporary unrestricted privilege for the application.

### Connections

[OS-001](001-operating-system-goals-and-resource-abstractions.md) defines protection as a resource-governance obligation. [OS-003](../ROADMAP.md) develops system-call transitions, and [OS-004](../ROADMAP.md) develops interrupts and exceptions. Architectural mechanisms connect to [Computer Architecture](../../23-computer-architecture/ROADMAP.md); least privilege and mediation connect to [Security Engineering](../../25-security-engineering/ROADMAP.md).

## Governing Question

An operating system must let programs compute, communicate, and use devices without letting any program rewrite page tables, disable interrupts indefinitely, inspect arbitrary memory, or take permanent control of a processor. A purely conventional rule—“applications must not do that”—cannot contain buggy or hostile code. The processor must enforce an execution boundary.

Privilege levels supply part of that enforcement. They classify the current execution context and make selected operations conditional on that state. Memory-management permissions and controlled entry paths complete the basic pattern. The result is not a magical wall: it is a state machine whose registers, tables, entry addresses, stacks, mappings, and return paths must all be configured correctly.

## Why This Matters

Nearly every kernel abstraction depends on privilege separation. A scheduler needs a timer or other event that can recover control from running code. Virtual memory needs protected translation structures. Device sharing needs access to control registers and memory-mapped I/O to remain mediated. Filesystem permissions mean little if an application can bypass the kernel and command storage directly.

The boundary also determines failure severity. A bad calculation in a restricted process may corrupt that process. The same defect in privileged code may corrupt any address space, reprogram a device, expose secrets, or crash the machine. Moving code into a kernel for speed therefore changes the trust and failure model, not just latency.

Protection rings are historically important but potentially misleading as a universal term. Intel 64 and IA-32 define four privilege levels. Arm A-profile systems use exception levels such as EL0 and EL1. RISC-V defines modes including U, S, and M. The names, ordering, optional features, transition instructions, and virtualization structures differ. The transferable idea is ordered architectural authority with controlled transitions.

## Prerequisites and Retrieval

Recall from [OS-001](001-operating-system-goals-and-resource-abstractions.md) that a mechanism enables and enforces actions while a policy chooses among allowed actions. You should understand registers, instructions, virtual addresses, page tables, exceptions, stacks, and processes at an introductory level.

Retrieve these distinctions before proceeding:

- execution state is not an application identity;
- virtual-memory permission is not the same as filesystem permission;
- an exception is a control transfer caused by an event, not necessarily an error;
- authentication establishes a principal, while authorization decides an operation;
- isolation limits interaction, whereas trusted code may still be defective.

## Learning Objectives

After completing this module, you should be able to:

- explain why convention alone cannot protect a kernel from applications;
- distinguish privilege levels, protection rings, protection domains, and identities;
- compare x86 rings, Arm exception levels, and RISC-V privilege modes without forcing false equivalence;
- identify instruction, register, memory, device, and transition enforcement surfaces;
- trace a controlled privilege increase and return at the level of architectural obligations;
- state the role of page permissions alongside current execution privilege;
- explain why a system call does not grant kernel privilege to application code;
- apply least privilege to kernel, driver, hypervisor, and firmware placement;
- diagnose confused-deputy, time-of-check/time-of-use, entry-state, and return-state failures;
- design bounded evidence for a privilege-boundary claim and identify where human review remains necessary.

## Core Exposition

### Privilege as architectural state

A processor maintains state describing the currently executing context. Among that state is a privilege classification. Instruction semantics consult it. Some instructions execute normally in an authorized state and fault or trap in an unauthorized state. Access to control registers, translation structures, interrupt controls, and device-facing facilities may likewise be restricted.

Privilege is authority to use mechanisms, not a moral label. “Supervisor” code can be malicious or wrong. “User” code can be an essential trusted service. The distinction is what the processor will permit at that instant. Software trust decisions must be layered above the architectural state.

The current state alone is also insufficient. A kernel at high privilege must not automatically read every application byte without purpose, and two applications at the same user privilege must still be isolated from one another. Page-table selection, page permissions, address-space identifiers, kernel policy, capabilities, credentials, and object references create finer domains.

### The x86 ring model

Intel 64 and IA-32 describe privilege levels 0 through 3, conventionally pictured as concentric rings. Smaller numbers represent greater privilege. The **current privilege level** (CPL) derives from execution context. Segment and gate descriptors carry descriptor privilege levels (DPL), while selectors can carry a requestor privilege level (RPL). Exact access checks depend on the operation and descriptor type; the slogan “lower number wins” is not a substitute for the architecture manual.

Ring 0 is normally used for the kernel and ring 3 for applications. Rings 1 and 2 allow intermediate privilege in the architecture, but a two-domain arrangement reduces complexity and fits paging-based process isolation. Their existence does not mean every OS uses them, nor that modern virtualization simply occupies “ring −1.” VMX root/non-root operation is another architectural dimension, with its own controls, and should not be collapsed into the four-ring diagram.

The ring drawing can also suggest that more privileged code must pass through every intermediate ring. It does not. An authorized gate or entry instruction can transfer from a less-privileged context to the configured privileged target directly. The relevant questions are which transitions exist, who configured them, what state hardware saves, which stack becomes active, and how the kernel validates the request.

### Arm exception levels

In AArch64, Arm names architectural privilege states **Exception levels**. A common software arrangement places applications at EL0, a rich operating-system kernel at EL1, a hypervisor at EL2, and low-level firmware or security software at EL3. Higher numbers indicate greater privilege, the opposite visual direction from x86 ring numbering.

Arm explicitly notes that this is a common usage model rather than an architectural command that particular software must have a particular role. Exception entry and return change the active level under defined rules. Memory-system permissions distinguish privileged and unprivileged access, while translation regimes and security states introduce additional dimensions.

Therefore, “EL1 equals ring 0” is useful only as a rough statement that each commonly hosts a kernel. It is not an equivalence of registers, entry frames, page formats, interrupt routing, virtualization, firmware boundaries, or security states.

### RISC-V privilege modes

The ratified RISC-V privileged architecture defines privilege modes for distinct execution environments. Machine mode (M) is mandatory and has the greatest architectural authority. Supervisor mode (S) and user mode (U) support conventional operating-system arrangements when implemented; virtualization adds further state and behavior.

A common stack places application code in U-mode, an OS kernel in S-mode, and platform firmware or a minimal machine-mode monitor in M-mode. Delegation registers can route selected traps toward a lower privileged supervisor instead of handling all of them in M-mode. This demonstrates a general design principle: greater privilege can delegate bounded mechanisms without surrendering control over everything.

Again, names do not establish complete equivalence. A robust explanation states the architecture, version, implemented modes, security assumptions, and active virtualization state.

### What is actually protected

Privilege enforcement appears across multiple surfaces:

1. **Instructions.** Operations that change translations, interrupt state, processor configuration, or execution control can require privilege.
2. **Control state.** Special registers hold page-table roots, trap vectors, status, delegation, and device-control information.
3. **Memory.** Translation entries distinguish accessible, writable, executable, user-accessible, and supervisor-only pages, with architecture-specific encodings.
4. **I/O.** Port I/O, memory-mapped device regions, and interrupt controllers must be mapped or authorized so applications cannot bypass drivers.
5. **Entry and return.** Hardware restricts which transitions raise privilege and which state a return can restore.
6. **Observation.** Debug, performance, and timing facilities may expose sensitive information and therefore need policy and architectural controls.

No single surface substitutes for the others. If a kernel maps its writable memory as user-accessible, instruction privilege does not prevent ordinary loads and stores to that mapping. If applications cannot edit page tables but can command a DMA-capable device without an IOMMU or equivalent restriction, the device may access memory outside the application's intended domain. If the entry target is writable by a caller, a nominally controlled transition becomes attacker-directed privileged execution.

### Controlled entry

A safe privilege increase has obligations before, during, and after transfer.

Before entry, privileged software configures an allowed vector or gate, its privilege rules, a trusted target, appropriate stack or saved-state locations, and memory mappings. The kernel keeps these control structures outside unprivileged modification.

On entry, hardware recognizes an allowed cause, records enough prior execution state, changes relevant privilege state, selects the defined target, and may switch stacks or translation context according to the architecture and kernel design. The exact saved frame differs among system calls, exceptions, interrupts, and architectures.

After entry, software still has substantial work. The kernel identifies the service and calling convention, validates scalar values and object handles, copies or pins user memory safely, checks credentials and capabilities, accounts resource use, handles interruption, and returns results without disclosing privileged state.

Return is a second security boundary. The kernel must validate or construct the outgoing state so the return instruction cannot install forbidden flags, selectors, addresses, mappings, or privilege. Sensitive registers and transient data may require clearing. A correct entry with an unsafe return is not a correct boundary.

### Least privilege and smaller trusted surfaces

Saltzer and Schroeder's least-privilege principle says programs and users should operate with only the privileges necessary for the task. Applied to operating systems, this motivates restricting applications, dropping authority after initialization, separating drivers or services where practical, constraining modules, and reducing privileged parsing.

Moving a service out of the kernel can reduce what one defect can corrupt, but it adds communication, scheduling, copying, and recovery paths. Keeping it in the kernel can improve direct access and performance while expanding the trusted computing base. Architecture alone does not settle the choice. Workload evidence, threat models, failure containment, interface design, verification strategy, and operational needs do.

## Definitions and Notation

Let `P` be a set of architectural privilege states with an ordering `≼` where `p₁ ≼ p₂` means `p₂` has at least the architectural authority of `p₁` for the operation being considered. This qualification matters because real architectures expose multiple dimensions rather than one universal scalar order.

Let:

- `cur ∈ P` be the current execution privilege;
- `op` be a requested instruction or processor operation;
- `need(op)` be its required privilege under the active architecture and configuration;
- `perm(v, a, cur)` be whether virtual address `v` permits access type `a` at `cur`;
- `G` be the configured set of legal privilege-changing entries;
- `T(s, e)` be the state transition from machine state `s` caused by entry `e`;
- `A(subject, object, operation)` be the kernel's authorization decision.

A simplified instruction rule is `allow(op) ⇔ cur` satisfies `need(op)`. A simplified memory rule is `allow(v, a) ⇔ translation succeeds ∧ perm(v, a, cur)`. A service request needs more:

`service_allowed ⇔ e ∈ G ∧ transition_valid(T) ∧ A(subject, object, operation)`.

This is an obligation decomposition, not a complete formal semantics for x86, Arm, RISC-V, or any kernel.

**Protection domain** denotes accessible objects and operations. **Privilege escalation** is an unintended or unauthorized increase in effective authority. **Trap** is a synchronous control transfer term whose precise architectural meaning varies. **Trusted computing base (TCB)** is the hardware and software whose correct behavior is necessary for a stated security property. **Attack surface** is the set of reachable interactions an adversary can try; it is not measured adequately by lines of code alone.

## Mechanisms, Invariants, or Proof Structure

Review a privilege boundary as a state machine with five groups of invariants.

**Configuration integrity.** Unprivileged code cannot modify entry vectors, privileged code, page tables governing the boundary, trusted stacks, saved-state areas, or authorization metadata. Configuration changes are themselves privileged and synchronized.

**Entry integrity.** Every increase in privilege has an architecturally valid cause and enters an approved target. The target begins with bounded assumptions about registers and caller-controlled memory. Nested events cannot corrupt entry state.

**Mediation integrity.** Entry does not imply authorization. The kernel validates the service number, values, handles, address ranges, lengths, overflow behavior, access direction, lifetime, and caller authority. Every sensitive operation follows a checked path.

**Return integrity.** The return target and restored state are suitable for the lower-privileged context. Privileged data is not exposed. Failures unwind ownership, locks, accounting, and partially completed effects according to the interface contract.

**Temporal integrity.** A value validated earlier cannot silently change before use unless the kernel deliberately tolerates and revalidates that change. CPU-local state, migration, preemption, concurrent revocation, and device activity are included in the reasoning.

The executable model below illustrates an intentionally small policy: ring 3 may read user pages but not supervisor pages; ring 0 may access either; a privileged interrupt-control operation is refused at ring 3; and an approved gate enters a kernel handler before returning. It is a teaching model, not an emulator of any architecture.

<!-- bijux-verify: {"id":"toy-privilege-boundary","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"user-read-user: allow\nuser-read-kernel: deny\nkernel-read-kernel: allow\nuser-disable-interrupts: deny\nsystem-call-gate: enter ring 0\nreturn: ring 3\n","stderr":""}} -->
```python
def memory_access(ring, page_kind):
    if page_kind == "user":
        return "allow"
    return "allow" if ring == 0 else "deny"


def privileged_operation(ring):
    return "allow" if ring == 0 else "deny"


def enter_gate(ring, gate):
    if ring == 3 and gate == "system-call":
        return 0
    raise PermissionError("unauthorized privilege transition")


print("user-read-user:", memory_access(3, "user"))
print("user-read-kernel:", memory_access(3, "supervisor"))
print("kernel-read-kernel:", memory_access(0, "supervisor"))
print("user-disable-interrupts:", privileged_operation(3))
entered = enter_gate(3, "system-call")
print("system-call-gate: enter ring", entered)
print("return: ring", 3)
```

Passing this snippet proves only the six outputs of this abstract Python policy. It does not implement CPL/DPL/RPL rules, exception levels, control registers, page tables, speculation, concurrency, interrupts, DMA isolation, authorization, or safe kernel entry. Real evidence requires architecture-specific inspection and adversarial testing at the actual boundary.

## Alternatives and Trade-Offs

**Two privilege domains versus several.** A user/kernel split is conceptually and operationally simpler. Intermediate levels can express more structure in hardware, but unused mechanisms still increase architectural complexity, and software may prefer paging, processes, capabilities, or virtualization for finer separation.

**Kernel-resident versus isolated services.** Kernel placement avoids some crossings and grants direct access. User-space services can narrow privileged authority and improve fault containment, but introduce IPC, scheduling, data transfer, protocol, and recovery costs. A microkernel, monolithic kernel, and hybrid kernel allocate these responsibilities differently; [OS-005](../ROADMAP.md) compares them directly.

**Trapping versus delegated access.** Trapping each sensitive operation centralizes mediation but costs transitions. Carefully mapped read-only data, restricted device queues, batched requests, or hardware delegation can reduce crossings. Each delegation adds invariants concerning ownership, revocation, validation, and containment.

**Static versus temporary privilege.** A component can run permanently privileged, enter privilege only through a service, or start privileged and drop authority. Shorter privileged duration reduces exposure, but transition and cleanup paths must be correct. Regaining authority must not rely on attacker-controlled state.

**Compatibility versus a smaller interface.** Legacy instruction, descriptor, and I/O behavior can support existing systems while enlarging what implementers must configure and audit. A smaller architecture or ABI can simplify reasoning, but ecosystem and hardware requirements constrain redesign.

**Performance versus stronger separation.** Mapping kernel data, sharing predictors or caches, and avoiding address-space changes can reduce latency. Stronger unmapping, flushing, isolation, or validation can increase cost. Security decisions require a threat model and measurements on the deployed architecture; folklore benchmarks are insufficient.

## Failure Modes and Misconceptions

1. **“Every CPU has rings 0–3.”** Those names and numbers are x86-specific. Arm and RISC-V organize privilege differently.
2. **“Ring 0 code is safe.”** Ring 0 code is powerful. A memory-safety or logic defect can therefore have greater impact.
3. **“All kernel activity is ring 0 and everything else ring 3.”** This ignores architecture, virtualization, firmware, security states, and user-space privileged services.
4. **“Page isolation follows automatically from supervisor mode.”** The kernel must construct and protect translations and select the correct address-space context.
5. **“A system call promotes the process.”** Hardware transfers execution to kernel code; the application's arbitrary instruction stream does not continue with kernel authority.
6. **“Taking a trap authorizes the request.”** Entry establishes a controlled path. Kernel policy must still authenticate context and authorize the operation.
7. **“One validated pointer stays valid.”** Another thread can change mappings or memory between check and use. Copying, pinning, locking, retry, or revalidation may be needed.
8. **“More rings always mean stronger security.”** Security depends on used mechanisms, configuration, mediation, TCB size, and verified properties.
9. **“CPU protection controls every device.”** DMA-capable devices and accelerators require their own mapping, ownership, and isolation mechanisms.
10. **“Architectural denial eliminates information flow.”** Timing, speculation, shared microarchitectural state, permitted IPC, and resource contention can still convey information.
11. **“A hypervisor is simply ring −1.”** That nickname conceals a separate virtualization mode and its controls.
12. **“A passing negative test proves non-bypassability.”** It samples one operation and state; completeness requires architecture-aware analysis and broader evidence.

## Worked Examples

### Example 1

**Question:** An application executes an instruction that disables maskable interrupts. What should happen?

**Reasoning:** If arbitrary applications could suppress the event used for preemption, one process could retain a processor indefinitely. The architecture classifies interrupt-control state as privileged. An unauthorized attempt faults or is otherwise rejected according to the instruction and architecture.

**Conclusion:** Privileged-instruction enforcement protects the kernel's ability to regain control; scheduler fairness still depends on correct kernel policy.

### Example 2

**Question:** Both process A and process B execute at the same least-privileged level. Why can they still have different accessible memory?

**Reasoning:** Current privilege is only one input to translation. The active page-table root or address-space context maps the same virtual address differently, and entries carry access permissions. The kernel controls both contexts.

**Conclusion:** Process isolation is built from privilege plus protected address translation, not from assigning every process a distinct ring.

### Example 3

**Question:** Does a system call temporarily let an application's next instructions execute in kernel mode?

**Reasoning:** A controlled instruction or exception transfers to a configured kernel entry address. Hardware and entry code preserve caller state, establish trusted execution state, and dispatch a service. Return resumes the caller at a lower privilege.

**Conclusion:** The kernel acts as a mediated deputy; application code does not receive unrestricted privileged execution.

### Example 4

**Question:** Can one say that x86 ring 0, Arm EL1, and RISC-V S-mode are identical?

**Reasoning:** They commonly host general-purpose kernels, so their system roles can be compared. Their numbering, mandatory features, control registers, transitions, translations, interrupt models, firmware relationships, and virtualization behavior differ.

**Conclusion:** Compare obligations and roles, then state architecture-specific mechanisms precisely.

### Example 5

**Question:** A kernel validates a user buffer, blocks, and later copies from the original address. What is wrong?

**Reasoning:** Another thread may alter the mapping or contents after validation. The later use may concern a different object or invalid range. This is a time-of-check/time-of-use problem across a mutable lower-trust boundary.

**Conclusion:** Validation must be coupled to use through copying, stable references, pinning, synchronization, or deliberate revalidation with well-defined failure behavior.

### Example 6

**Question:** Why place a network driver in user space?

**Reasoning:** Driver defects then need not automatically have arbitrary kernel memory authority. The design may instead grant restricted device queues and memory regions. Costs include IPC, scheduling, mapping management, interrupt delivery, and recovery complexity.

**Conclusion:** Placement trades TCB size and fault containment against crossings and coordination; privilege is one design variable, not the entire decision.

### Example 7

**Question:** A user page is executable and writable. Is that automatically a privilege violation?

**Reasoning:** It need not expose supervisor memory, so it is not by itself a ring transition. It can still undermine exploit resistance by allowing injected data to become code. Policy may enforce write-xor-execute and restrict executable mappings.

**Conclusion:** Architectural privilege is necessary but broader memory-safety policy can impose stricter invariants.

### Example 8

**Question:** A process can submit work directly to a device queue. Has the kernel lost control?

**Reasoning:** Not necessarily. The kernel might provision a bounded queue, configure device and IOMMU translations, validate descriptors, account work, and revoke access. Without those controls, DMA or commands may escape the process's domain.

**Conclusion:** Delegation is safe only under explicit device, memory, lifetime, and revocation invariants.

### Example 9

**Question:** A service runs in a highly privileged mode but accepts requests only from authenticated clients. Is complete mediation established?

**Reasoning:** Authentication does not show that every sensitive object access passes through authorization, that cached decisions respect revocation, or that alternate entry and device paths are closed. Privilege only tells what the service can do.

**Conclusion:** Complete mediation requires path analysis, authorization semantics, revocation behavior, and adversarial evidence in addition to architectural placement.

### Example 10

**Question:** May a safety controller rely on privilege separation as proof that an unprivileged task cannot cause a hazardous actuator command?

**Reasoning:** Privilege tests can show selected instructions and mappings are denied. The safety claim also depends on every authorized command path, shared memory, IPC, driver, DMA route, interrupt, timing assumption, physical interlock, failure mode, and deployed configuration. Requirements and acceptable risk belong to the responsible safety process.

**Conclusion:** Architecture evidence is one input. A named human with domain and safety authority must review the hazard analysis, independence assumptions, traceability, test coverage, and residual risk; this chapter makes no certification or external-review claim.

## Cross-Program Connections

[Computer Architecture](../../23-computer-architecture/ROADMAP.md) owns instruction semantics, exceptions, translation, interrupt controllers, and virtualization mechanisms. This program uses those mechanisms to construct OS protection domains. [Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) develops user-space interactions with operating-system interfaces.

[Security Engineering](../../25-security-engineering/ROADMAP.md) develops threat models, least privilege, complete mediation, exploit chains, and assurance. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) shows why a local privilege boundary does not establish trust across machines. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) adds lifecycle, interface, hazard, and safety-assurance obligations to privilege decisions in cyber-physical systems.

The successor [OS-003](../ROADMAP.md) traces system-call entry and return in detail. [OS-004](../ROADMAP.md) distinguishes interrupts, faults, traps, and exceptions; [OS-005](../ROADMAP.md) compares how kernel architectures allocate privileged services.

## References

- Intel Corporation, [*Intel® 64 and IA-32 Architectures Software Developer's Manuals*](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), especially Volume 3 system programming and protection chapters, current documentation page checked 2026-08-29. Primary x86 privilege, descriptor, paging, transition, and virtualization specification.
- Arm Limited, [*AArch64 Programmer's Guides: Introduction to Security—Exception Model*](https://developer.arm.com/-/media/Arm%20Developer%20Community/PDF/Learn%20the%20Architecture/Exception%20model.pdf), 2019. Official overview of EL0–EL3, exception changes, and privileged versus unprivileged memory access.
- RISC-V International, [*RISC-V Ratified Specifications Library: Privileged Architecture*](https://docs.riscv.org/reference/home/index.html), current library checked 2026-08-29. Primary index for ratified RISC-V privilege modes, traps, delegation, protection, and virtualization specifications.
- Jerome H. Saltzer and Michael D. Schroeder, [*The Protection of Information in Computer Systems*](https://doi.org/10.1109/PROC.1975.9939), `Proceedings of the IEEE` 63(9), 1975. Foundational protection-domain and design-principles treatment.
- Gerwin Klein et al., [*seL4: Formal Verification of an OS Kernel*](https://dl.acm.org/doi/10.1145/1629575.1629596), SOSP, 2009. Primary account of machine-checked functional-correctness proof for a specific kernel and assumptions.
- Russ Cox, Frans Kaashoek, and Robert Morris, [*xv6: a simple, Unix-like teaching operating system*](https://pdos.csail.mit.edu/6.1810/2025/xv6/book-riscv-rev5.pdf), MIT, 2025 edition. Teaching treatment of RISC-V user/kernel boundaries, traps, page tables, and system calls.

## Exercises

### Exercise 1

Classify each statement as an architectural privilege fact, a memory-protection fact, a kernel authorization decision, or an unsupported security conclusion: (a) an instruction faults in user mode; (b) a page is supervisor-only; (c) a process may signal another process; (d) therefore no application can influence kernel control flow.

### Exercise 2

Trace the obligations for a least-privileged process requesting a kernel service. Cover configuration before entry, architectural transition, kernel validation, execution, error cleanup, and return. Do not assume that taking the entry authorizes the operation.

### Exercise 3

Compare a conventional kernel placement on x86, Arm AArch64, and RISC-V. State the common role and at least four reasons the privilege states are not interchangeable specifications.

### Exercise 4

A high-throughput service maps a device command queue into an application to avoid a system call per request. Construct the minimum protection argument. Include device memory access, descriptor validation, ownership, accounting, revocation, reset, concurrency, and evidence.

### Exercise 5

An industrial controller vendor claims, “Untrusted analytics runs unprivileged, so analytics cannot cause an unsafe actuator command.” Design a review plan that could support or refute this claim. Separate automated evidence, architecture-specific inspection, adversarial tests, operational configuration, physical safeguards, and named human review.

## Answers to the Exercises

### Answer 1

(a) is an architectural privilege fact, scoped to a named instruction, architecture, mode, and configuration. (b) is a memory-protection fact, scoped to the active translation and access type. (c) is a kernel authorization decision based on identity, credentials, namespace, object state, and policy. (d) is unsupported: applications intentionally influence kernel control flow through calls, exceptions, interrupts, shared state, and devices, while defects or side channels may provide unintended influence. The first three observations do not prove universal control-flow integrity.

### Answer 2

Before entry, the kernel protects a valid vector or gate, target code, entry stack, translation context, and authorization metadata. The application supplies a service identifier and arguments using the ABI. Hardware accepts only a defined entry, saves prior state, changes privilege, and transfers to the configured target. Entry code establishes trusted state before using caller values.

The kernel checks the service number, sizes, arithmetic, pointers, direction, object handles, credentials, capabilities, quotas, and current object state. It stabilizes mutable user data where required, executes the operation with bounded resources, records partial effects, and handles interruption. Every error path releases references, memory, locks, and accounting consistently. Return values are copied through checked destinations; outgoing register and control state is sanitized; an architectural return restores an authorized user context. Entry proves only that dispatch was controlled, not that the requested operation was allowed.

### Answer 3

A common x86 system uses ring 3 for applications and ring 0 for a kernel. A common AArch64 system uses EL0 for applications and EL1 for a kernel. A common RISC-V system uses U-mode for applications and S-mode for a kernel, with M-mode firmware retaining greater authority. Each realizes a user/kernel role split.

They are not interchangeable because their numbering and ordering differ; their mandatory and optional privilege states differ; their control/status registers and instruction semantics differ; their exception-entry and return frames differ; page-table formats and access rules differ; interrupt routing differs; firmware and security-state relationships differ; and virtualization adds different states and controls. A port must use the relevant architecture specification rather than translating labels.

### Answer 4

The argument begins with explicit ownership: which process owns which queue, device context, interrupt, and memory region. An IOMMU or equivalent device translation restricts DMA to pinned, authorized pages; the device cannot use caller-provided physical addresses unchecked. Queue descriptors have bounded formats, lengths, operation codes, and overflow behavior. Kernel or device validation rejects references outside the assigned domain.

Submission and completion rings need concurrency and memory-ordering rules. Quotas and scheduling account device time and bandwidth. Revocation stops new work, drains or cancels accepted work, removes mappings, and handles in-flight DMA before memory reuse. Reset behavior must not expose a prior owner's buffers or corrupt another context. Evidence includes architecture and device-manual review, configuration inspection, negative descriptor tests, cross-domain DMA attempts, races during unmap and reset, fault injection, resource-exhaustion tests, and workload measurements. Passing throughput tests alone proves none of the isolation claims.

### Answer 5

First define the hazard, actuator authority, analytics inputs and outputs, timing bounds, assumed architecture, firmware, kernel, drivers, IPC, device topology, and deployed configuration. Map every route from analytics-controlled data or timing to the actuator: system calls, messages, shared pages, files, network services, signals, interrupts, DMA devices, debug paths, updates, and recovery controls.

Automated checks can inspect mappings, privilege configuration, allowed IPC, device assignments, build provenance, and policy consistency. Architecture-specific review traces entry, translation, interrupt, DMA, and return behavior against the exact processor and device manuals. Adversarial tests attempt forbidden instructions, addresses, messages, malformed lengths, race conditions, exhaustion, timing interference, confused-deputy calls, restart and reset escapes, and stale authorization. Operational evidence verifies secure boot or equivalent assumptions, production policy, monitoring, update authority, and drift detection. Independent physical interlocks and safe-state behavior must be tested under specified failures.

A named safety engineer and domain authority must review hazard coverage, requirements traceability, independence assumptions, diagnostic coverage, test representativeness, residual risk, and applicable regulatory obligations. A security reviewer must examine bypass and escalation paths. The decision record must identify reviewers, evidence versions, unresolved findings, and acceptance authority. No Python model, privilege bit, or internal course review can replace that accountable human judgment.
