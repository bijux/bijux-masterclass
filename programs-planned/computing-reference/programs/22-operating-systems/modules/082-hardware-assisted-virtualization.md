---
module_id: OS-082
program: Operating Systems
level: 2
module_number: 82
title: Hardware-Assisted Virtualization
status: complete
last_verified: 2026-09-04
---

# Hardware-Assisted Virtualization

## One-Page Review

### Governing question

How do processor and platform virtualization facilities accelerate guest execution while preserving a monitor-controlled architectural boundary?

### Essential definitions

- A **guest execution mode** lets guest supervisor code execute without granting host supervisor authority.
- A **virtualization control structure** records guest state, host state, entry controls, exit controls and exit information.
- A **VM entry** validates controls, loads guest context and begins or resumes guest execution.
- A **VM exit** transfers control to the monitor with saved guest state, a reason and qualifying information.
- **Nested translation** composes guest-controlled stage-one translation with monitor-controlled stage-two translation.
- A **translation tag** distinguishes cached translations belonging to address spaces or virtual machines.
- **Interrupt virtualization** supports virtual interrupt state, routing, acknowledgment and sometimes direct or posted delivery.
- An **IOMMU** translates and authorizes device-originated memory transactions and remaps device interrupts.

### Central model, mechanism, or theorem

Hardware assistance adds a processor mode and control plane in which guest privileged operations can execute directly except where configured interception, faults or external events require a monitor exit. Correctness does not come from enabling the feature bit. The monitor must construct a valid virtual CPU contract, program controls from discovered capabilities, compose memory permissions, route interrupts, contain DMA, preserve time and migrate only state supported by the destination profile.

### Critical invariants

- Guest execution never acquires host control merely because guest code is privileged within its virtual machine.
- Entry controls contain only architecturally legal combinations for the exact processor and firmware.
- Every exit is attributed from saved architectural reason and qualification before state is changed.
- Effective memory permission is no broader than either translation stage permits.
- Tagged translations are invalidated before ownership or mapping reuse can expose stale access.
- Interrupt delivery and DMA identify the intended virtual machine and device owner.
- Exposed CPU features remain semantically implemented across reset, migration and nested operation.

### Common failures

A monitor copies control bits from another processor, exposes a feature it only partially emulates, misattributes a stage-two fault, reuses a translation tag too early, injects an interrupt into stale vCPU state, removes an IOMMU mapping before DMA quiesces, or migrates a guest to a destination lacking a relied-on capability.

### Compact example

A requested profile requires nested translation and tagged TLBs, and optionally requests posted interrupts and counter scaling. Capability discovery confirms all except posted interrupts. The monitor admits the VM with the required features, enables counter scaling, and selects exit-and-inject as the interrupt fallback. It does not write an unsupported posted-interrupt control bit or advertise that behavior to the guest.

### Connections

Hardware-assisted virtualization joins ISA privilege, exception entry, page translation, cache invalidation, interrupt controllers, IOMMUs, timers, device assignment, migration, confidential computing and scheduler policy.

## Governing Question

Hardware facilities can turn many former traps and software translations into direct execution, but they also introduce a dense configuration surface. The governing question is how to choose and validate controls so that acceleration refines the declared virtual machine rather than exposing accidental host behavior.

## Why This Matters

Modern hypervisors rely on CPU execution modes, nested page tables, tagged TLBs and virtual interrupt facilities for acceptable performance. Platform support extends the boundary to DMA and interrupt remapping. These mechanisms reduce common exits and software shadowing, yet a wrong control field can prevent entry, leak state, misdeliver an event or silently change guest behavior.

Capabilities vary by architecture, processor generation, microcode, firmware and kernel. The host-visible feature set is not automatically a safe guest-visible feature set. Operations teams also need a stable migration profile spanning heterogeneous machines. A durable design therefore treats hardware assistance as negotiated, versioned mechanisms with software fallbacks and explicit assurance limits.

## Prerequisites and Retrieval

Before studying this module, be able to:

- explain trap-and-emulate refinement, guest versus host privilege and precise exceptions;
- trace virtual, guest-physical and host-physical addresses through page tables and TLBs;
- describe local and external interrupt routing, masking, priority and acknowledgment;
- reason about DMA ownership, device reset and I/O translation;
- distinguish architectural capability, implementation choice and exposed virtual contract.

Retrieve the exact processor model and stepping, architectural manuals, virtualization capability registers, microcode, firmware, kernel, hypervisor, virtual CPU model, machine type, IOMMU configuration and device firmware. Record mitigations that disable or constrain acceleration. Re-run discovery after microcode, firmware or kernel changes.

## Learning Objectives

After completing this module, you should be able to:

1. explain guest execution modes, entries, exits and virtualization control structures;
2. construct legal controls through capability discovery rather than assumed feature names;
3. distinguish guest-visible CPU features from host implementation features;
4. reason about two-stage translation, permission composition, tags and invalidation;
5. explain virtual interrupt acceleration, IOMMU translation and interrupt remapping;
6. preserve clock, counter, multiprocessor and nested-virtualization semantics;
7. evaluate exit frequency, page-walk cost, device paths and fallback performance;
8. test isolation, compatibility, migration and security across a hardware capability matrix.

## Core Exposition

### Add a guest supervisor domain

Hardware virtualization separates “guest supervisor” from “host supervisor.” On x86, VMX root/non-root or SVM host/guest state supplements ordinary privilege rings; Arm uses EL2 controls around lower exception levels; RISC-V adds hypervisor-managed virtual supervisor state. Names differ, but the purpose is stable: privileged guest code must not inherit host authority.

### Treat the control structure as an interface

Control structures contain entry state, exit state, interception policy, translation roots, interrupt fields and implementation-defined or reserved areas. Some fields are memory resident, some cached internally and some accessed only through dedicated instructions. Ownership, update order and required invalidation must follow the architecture, not ordinary-structure intuition.

### Discover legal control values

Capability registers commonly describe controls that must be one, may be one or are unavailable. Build requested controls from the virtual-machine profile, intersect optional mechanisms with support, verify required mechanisms and satisfy dependencies. A copied bitmask can contain a reserved combination even across processors bearing the same marketing family.

### Construct VM entry transactionally

Before entry, install valid guest state, host return state, translation roots, event injection, interrupt controls and execution policy. Entry can fail because controls or guest state are inconsistent. Treat failure as a diagnosable construction error with bounded reporting; do not repeatedly enter or partially expose a vCPU that never reached guest execution.

### Dispatch exits from architectural metadata

An exit reason alone may be insufficient. Qualification can carry access type, register, address, instruction length, fault stage or pending state. Snapshot the fields whose validity the manual associates with that reason, then dispatch. Reading unrelated stale fields creates plausible but incorrect emulation inputs.

### Minimize the intercept surface deliberately

Controls may intercept selected instructions, exceptions, register ranges, I/O ports, page faults and external events. Intercept what correctness, policy or observability requires; allow direct execution only where the hardware virtualizes semantics completely. Fewer exits can improve performance, but disabling an intercept without a replacement can surrender control or compatibility.

### Expose a constructed virtual CPU

The guest CPU model is a contract assembled from hardware execution, monitor emulation and policy. Feature enumeration, control-register behavior, instruction availability and exception semantics must agree. If a feature is advertised, every reachable semantic path must exist. Host passthrough maximizes exposure but weakens migration and reproducibility.

### Compose two translation stages

The guest maps a virtual address to a guest-physical address at stage one; the monitor maps that guest-physical address to host physical memory at stage two. Effective read, write, execute, memory type and access attributes derive from architecture-defined composition. Stage-two denial protects host ownership even if stage one permits access.

### Attribute translation faults to the right owner

A stage-one fault usually belongs to the guest operating system. A stage-two fault reaches the monitor because the guest-physical mapping is absent, protected or used for emulated I/O. Page walks themselves can encounter stage-two faults. Report or inject the architecture-defined address, access and syndrome rather than collapsing every failure into a generic page fault.

### Manage combined page-walk cost

Two-stage translation can multiply memory references on TLB misses. Large pages, page-walk caches, locality and appropriate mapping geometry reduce cost, but large mappings amplify dirty tracking, copy-on-write and fragmentation trade-offs. Measure miss and walk behavior under the actual guest and host page sizes.

### Tag cached translations

Address-space and virtual-machine identifiers allow TLB entries from different contexts to coexist. A tag is a finite recyclable namespace, not permanent identity. Before reusing a tag for a different translation regime, issue the required invalidation and completion barrier on every processor that may retain entries.

### Invalidate by dependency and scope

Mapping removal, permission reduction, memory-type change and ownership transfer require architecture-specific invalidation. Choose address, context or global scope from what changed and which caches can hold derived state. Publish new tables and synchronize invalidation in the prescribed order. An invalidation instruction's completion semantics matter as much as issuing it.

### Accelerate interrupt delivery without losing state

Hardware may virtualize controller registers, track pending priorities, suppress exits for acknowledgment or deliver posted interrupts to a running vCPU. The monitor still owns routing, affinity, masking and fallback when a vCPU is not runnable. Direct delivery must bind device, interrupt identity and current vCPU ownership despite migration and descheduling.

### Remap external interrupts

Interrupt remapping prevents a device from choosing arbitrary host destinations or vectors. Tables associate device identities with authorized delivery. Update, invalidate and quiesce ordering must close reuse races. CPU interrupt virtualization cannot substitute for remapping interrupts originating outside the CPU.

### Contain DMA with an IOMMU

I/O translation maps device-visible addresses to memory owned by the assigned guest or backend. Device identifiers, process address spaces, translation caches and invalidation queues extend the ownership graph. Safe teardown stops new work, drains transactions, disables delivery, invalidates translations and only then reuses memory or device context.

### Virtualize clocks and counters

Offset and scaling facilities can let guests read counters without exiting while observing a chosen time domain. Validate width, rate, wrap, stability and migration representation. Timers also depend on interrupt delivery and descheduling. A monotonic counter does not by itself guarantee correct wall-clock or scheduled-time behavior.

### Coordinate vCPU scheduling

VM exits, preemption, halt states and host scheduling interact. A vCPU that blocks while holding a guest lock can stall peers; directed yield or paravirtual hints may help. Hardware preserves architectural context, not fairness. Account separately for guest execution, exit service, ready-but-not-running delay and host steal time.

### Understand nested virtualization composition

With an L0 monitor, L1 guest hypervisor and L2 guest, L0 must implement the virtualization interface exposed to L1 while using one physical facility. Control structures, translations, exits and interrupts are merged or shadowed. An L2 exit may belong to L1 policy or L0 enforcement; wrong attribution breaks the nested contract.

### Handle confidential-VM variants explicitly

Protected guest modes can restrict host access to guest memory or register state and add firmware-mediated lifecycle operations. That changes emulation, debugging, migration and device sharing. Confidentiality from the host is a separate property from ordinary guest isolation, and attestation describes a measured configuration rather than proving workload correctness.

### Budget transition and translation costs

Measure exits per reason, entry/exit duration, userspace crossings, interrupt latency, TLB misses, nested-walk events, invalidations and IOMMU faults. Compute distributions and denominators per vCPU and device. One faster transition does not compensate for an exit storm or pathological page-walk locality.

### Maintain software fallbacks

Optional acceleration may be absent or disabled by errata and mitigation. A correct fallback can emulate an instruction, inject interrupts through exits, use smaller mappings or reject the requested VM profile. Silent degradation is dangerous when it changes semantics or violates a performance service level; report the selected mechanism.

### Freeze a migration compatibility profile

Migration requires a destination that implements every exposed feature and serialized state semantic. Use a named baseline or negotiated contract rather than raw host passthrough. Carry time offsets, interrupt state, translation-relevant state and nested state. Validate destination controls before committing ownership transfer.

### Test the matrix and negative paths

Test required and optional capabilities, reserved controls, invalid guest states, each exit family, stage-one and stage-two faults, tag reuse, invalidations, interrupt races, IOMMU teardown, reset and migration. Include processors with different feature subsets and mitigations. Fuzz control construction and exit qualification within documented validity rules.

### State the security boundary

Hardware enforces selected architectural separations, but monitor software constructs the policy. Microarchitectural side channels, speculative execution, shared caches, denial of service, firmware, system-management modes and device bugs may cross the intended boundary. Cite the precise mechanism and threat model for each isolation claim.

## Definitions and Notation

Let host capability set be $H$, required profile features be $R$, and optional requested features be $O$. Admission requires

$$
R\subseteq H,
$$

and the exposed acceleration set is $A=R\cup(O\cap H)$. Guest-advertised features may be narrower because policy and complete software semantics impose additional constraints.

Let stage-one translation be $T_1:VA\rightarrow GPA$ and stage-two translation be $T_2:GPA\rightarrow HPA$. For a successful access,

$$
T(VA)=T_2(T_1(VA)).
$$

If permissions are modeled as allowed-operation sets $P_1$ and $P_2$, effective permission is $P=P_1\cap P_2$, subject to the architecture's memory-attribute composition rules.

For exit reason $r$, rate $\lambda_r$ and mean service demand $c_r$, exit demand is

$$
D_e=\sum_r\lambda_r c_r.
$$

Total lost guest service also includes queueing, descheduling and cache disruption; $D_e$ is not total virtualization overhead.

Let translation tag $x$ have generation $g_x$. Reassignment from owner $a$ to owner $b$ is safe only after every processing element and translation cache that can use $(x,g_a)$ has completed the required invalidation before $(x,g_b)$ becomes runnable.

## Mechanisms, Invariants, or Proof Structure

Review a hardware-assisted design with these obligations.

1. **Domain obligation:** guest privilege remains distinct from monitor and host privilege on every entry and exit.
2. **Capability obligation:** required controls are supported, optional controls are negotiated, and dependencies are validated.
3. **Profile obligation:** enumeration, executable behavior, exceptions and migration state describe one virtual CPU.
4. **Entry obligation:** control and guest state are valid before any guest instruction executes.
5. **Exit obligation:** reason-specific valid fields drive exactly one handler transition and correct resume state.
6. **Translation obligation:** address and attribute composition never broadens either stage's authority.
7. **Invalidation obligation:** stale CPU and I/O translations cannot survive permission or ownership change.
8. **Interrupt obligation:** pending, routed, posted, injected and acknowledged states preserve identity and priority.
9. **DMA obligation:** device transactions and interrupts remain inside the assigned ownership domain through reset.
10. **Time obligation:** counters, timers, scheduling and migration preserve the declared virtual time policy.
11. **Fallback obligation:** absence or withdrawal of acceleration yields an explicit correct alternative or admission failure.
12. **Assurance obligation:** architectural, performance, confidentiality and side-channel claims remain separately evidenced.

The safety argument composes CPU domain separation, control validation, two-stage translation, interrupt identity and I/O translation. Performance is a separate argument about exits, page walks, invalidations and device paths. Neither argument follows merely from a feature flag being present.

## Alternatives and Trade-Offs

- **Host passthrough versus baseline CPU:** passthrough exposes speed and features; a baseline improves migration and reproducibility.
- **More direct execution versus more intercepts:** direct execution reduces exits; intercepts provide control and observability.
- **Nested translation versus shadow paging:** nested translation moves composition into hardware; shadows can reduce some walk depth and increase software complexity.
- **Large versus small stage-two pages:** large pages improve reach; small pages improve dirty tracking and fine-grained ownership.
- **Tagged versus flush-on-switch TLBs:** tags retain locality; reuse requires disciplined invalidation.
- **Posted versus exit-based interrupts:** posted delivery lowers latency; exits simplify mediation and fallback.
- **In-kernel versus userspace interrupt controller:** in-kernel paths reduce transitions; userspace models can simplify portability and inspection.
- **Emulated device versus assigned device:** emulation supports compatibility; assignment improves throughput and expands IOMMU/reset dependencies.
- **Counter passthrough versus trapped time reads:** passthrough is fast; trapping permits arbitrary policy at high frequency cost.
- **Static versus dynamic capability policy:** static profiles are reproducible; dynamic policy can exploit hosts and complicate migration.
- **Fine invalidation versus broad flush:** fine scope preserves caches; broad scope simplifies correctness and raises disruption.
- **Polling versus interrupt delivery:** polling avoids transitions under load; interrupts preserve idle efficiency.
- **Nested virtualization versus flat ownership:** nesting supports guest hypervisors; composition adds exits and migration state.
- **Confidential guests versus host introspection:** protected state improves confidentiality; debugging, emulation and migration become constrained.
- **Reject versus emulate a missing feature:** rejection preserves a clear contract; emulation expands compatibility and attack surface.
- **Maximum acceleration versus conservative mitigations:** acceleration reduces overhead; mitigations may be required for the current threat model.

## Failure Modes and Misconceptions

- “A virtualization feature bit means every control is available.” Capability fields and dependencies decide legality.
- “Guest kernel privilege is host kernel privilege.” Hardware adds a distinct execution domain.
- “Valid entry means the virtual CPU contract is coherent.” Enumeration and behavior can still disagree.
- “Every exit field is valid for every reason.” Qualification validity is reason-specific.
- “Fewer exits always means safer and faster.” Removed intercepts can surrender policy, and bottlenecks may lie elsewhere.
- “Host feature passthrough is transparent.” It binds behavior and migration to that host.
- “Nested paging eliminates page-walk overhead.” TLB misses can require composed walks.
- “Stage one can grant access denied by stage two.” Effective authority cannot exceed monitor ownership.
- “Every nested fault is a guest page fault.” The stage and walk context determine ownership.
- “A VM identifier never needs flushing.” Tags are finite and recycled.
- “Issuing invalidation completes invalidation.” Architecture-defined barriers and acknowledgments may be required.
- “Posted interrupt means no monitor state.” Routing, blocking and migration still require ownership.
- “CPU interrupt controls secure device interrupts.” External sources require remapping.
- “An IOMMU mapping alone makes passthrough safe.” Reset, firmware, peer traffic and interrupt isolation also matter.
- “Device reset instantly stops DMA.” Outstanding transactions may survive until quiesced.
- “A direct counter read equals correct guest time.” Offset, scale, scheduling and migration remain.
- “Hardware scheduling makes vCPUs fair.” The host scheduler still allocates processors.
- “Nested virtualization adds only one more mode.” Controls, translations, exits and interrupts must compose.
- “Confidential VM means secure VM.” It addresses a defined confidentiality threat model, not all correctness or availability.
- “Average VM-exit time is total overhead.” Frequency, queueing, cache disruption and page walks also contribute.
- “Optional acceleration may silently disappear.” Semantic or service-level changes require explicit fallback reporting.
- “Live migration copies CPU registers.” It must preserve an exposed capability and device-time contract.
- “Same processor family means same virtualization behavior.” Stepping, microcode, firmware and mitigations matter.
- “Passing a boot test validates IOMMU teardown.” Ownership reuse races need targeted stress.
- “Architectural isolation closes timing channels.” Shared microarchitecture requires separate analysis.

## Worked Examples

### Example 1

A monitor requests a secondary execution control that exists only when a primary “activate secondary controls” bit is legal and set. Capability discovery supports both. Setting only the secondary bit fails entry; dependency validation constructs both fields together.

### Example 2

The following executable toy admits required accelerators, selects supported optional ones and names the fallback for an unavailable mechanism. It demonstrates set negotiation only, not processor control encoding or safe VM construction.

<!-- bijux-verify: {"id":"virtualization-capability-negotiation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"admitted=True\nselected=nested_translation,tagged_tlb,tsc_scaling\nmissing_required=none\nfallbacks=posted_interrupt:exit_and_inject\n","stderr":""}} -->
```python
supported = {"nested_translation", "tagged_tlb", "tsc_scaling"}
required = {"nested_translation", "tagged_tlb"}
optional = {"posted_interrupt", "tsc_scaling"}

missing = required - supported
selected = required | (optional & supported)
fallbacks = {
    feature: "exit_and_inject"
    for feature in sorted(optional - supported)
    if feature == "posted_interrupt"
}

print(f"admitted={not missing}")
print(f"selected={','.join(sorted(selected))}")
print(f"missing_required={','.join(sorted(missing)) or 'none'}")
print("fallbacks=" + ",".join(f"{key}:{value}" for key, value in fallbacks.items()))
```

### Example 3

Stage one permits a guest write, but stage two marks the guest-physical page read-only for dirty tracking. The access exits as a stage-two violation. The monitor records dirtiness, updates policy if appropriate and resumes; injecting an ordinary guest page fault would blame the wrong owner.

### Example 4

A host reassigns VM identifier 12 after a VM exits. One remote CPU retains a translation tagged 12. Without cross-CPU invalidation completion, the new VM can resolve an address through stale ownership. Generation-aware retirement precedes reuse.

### Example 5

A posted interrupt targets a vCPU that migrated between host CPUs. The routing entry and notification destination must change under a protocol that handles an interrupt racing with the move. Otherwise the event can reach the old CPU after its vCPU context departed.

### Example 6

An assigned device is detached. The host unmaps I/O pages first, then immediately gives the physical pages to another tenant. A late DMA faults rather than corrupting memory, but safe teardown still requires draining and reset completion before reuse and must treat the IOMMU fault as evidence of a broken sequence.

### Example 7

Nested-walk events rise sharply after transparent huge pages split under dirty logging. VM exits remain flat, yet throughput falls. Exit-only profiling would miss translation cost; page-size geometry and walk caches explain the change.

### Example 8

A guest profile exposes counter scaling. The destination supports counter offsets but not scaling. Migration admission fails before switchover because emulating frequent direct counter reads cannot preserve the already advertised instruction semantics transparently under the chosen profile.

### Example 9

L2 executes an instruction that L1 requested to intercept but L0 allows for its own guests. L0 must synthesize the appropriate L1-visible exit rather than execute through, because L1 owns that part of the nested virtual contract.

### Example 10

A microcode update disables one interrupt-virtualization optimization under a mitigation. The monitor retains correct exit-and-inject fallback, reports the selected path, and blocks VM admission only where the declared latency service level requires the missing accelerator.

## Cross-Program Connections

- **Computer architecture:** execution domains, control registers, page walkers, TLBs and interrupt controllers provide mechanisms.
- **Security engineering:** complete mediation, IOMMU containment, speculative threats and confidential modes define threat boundaries.
- **Performance engineering:** exits, translation walks, invalidations, interrupt latency and device paths determine cost.
- **Distributed systems:** capability negotiation, clocks, migration and nested ownership create versioned state-machine problems.
- **Platform engineering:** CPU baselines, host pools, firmware, scheduling and fleet compatibility operationalize acceleration.
- **Network and storage engineering:** assigned devices, queues, DMA and interrupts connect virtualization to high-rate I/O.
- **Reliability engineering:** negative entry tests, fallback paths, reset sequencing and fault attribution support recovery.
- **Formal methods:** refinement, set inclusion, permission intersection and generation invariants structure correctness.
- **API and service engineering:** capability discovery, optional features and explicit admission failures resemble durable protocol negotiation.
- **Systems engineering:** CPU, memory, interrupt, device and firmware mechanisms must satisfy one end-to-end isolation case.

## References

1. Intel, [Intel 64 and IA-32 Architectures Software Developer Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), VMX operation, control structures, entries, exits, nested translation and interrupt virtualization; retrieved 2026-09-04.
2. AMD, [AMD64 Architecture Programmer's Manual, Volume 2: System Programming](https://docs.amd.com/v/u/en-US/24593_3.44_APM_Vol2), SVM, control blocks, intercepts, nested paging and interrupt behavior; retrieved 2026-09-04.
3. Arm, [Armv8-A Virtualization](https://developer.arm.com/-/media/Arm%20Developer%20Community/PDF/Learn%20the%20Architecture/Armv8-A%20virtualization.pdf), EL2, traps, stage-two translation, VMIDs and virtual interrupts; retrieved 2026-09-04.
4. RISC-V International, [Hypervisor Extension](https://docs.riscv.org/reference/isa/priv/hypervisor), hypervisor privilege, virtual supervisor state, two-stage translation and virtual interrupts; retrieved 2026-09-04.
5. Linux Kernel Documentation, [KVM API](https://docs.kernel.org/virt/kvm/api.html), capability discovery, virtual CPU execution, exits, devices and migration-visible state; retrieved 2026-09-04.
6. Linux Kernel Documentation, [The x86 KVM Shadow MMU](https://docs.kernel.org/virt/kvm/x86/mmu.html), translation, nested paging, shadow pages, invalidation and memory events; retrieved 2026-09-04.
7. Linux Kernel Documentation, [Timekeeping Virtualization for x86-Based Architectures](https://docs.kernel.org/virt/kvm/x86/timekeeping.html), counters, timers, offsets, scaling, scheduling and migration; retrieved 2026-09-04.
8. Intel, [Virtualization Technology for Directed I/O Architecture Specification](https://www.intel.com/content/www/us/en/content-details/868911/intel-virtualization-technology-for-directed-i-o-architecture-specification.html), DMA remapping, interrupt remapping and I/O translation invalidation; retrieved 2026-09-04.
9. AMD, [I/O Virtualization Technology Specification](https://docs.amd.com/v/u/en-US/48882_3.10_PUB), IOMMU translation, device tables, interrupts and invalidation; retrieved 2026-09-04.
10. Linux Kernel Documentation, [Running Nested Guests with KVM](https://www.kernel.org/doc/html/latest/virt/kvm/x86/running-nested-guests.html), L0/L1/L2 terminology, nested facilities, CPU models and migration constraints; retrieved 2026-09-04.

## Exercises

### Exercise 1

A host supports nested translation and counter offsets but lacks tagged TLBs. A profile requires nested translation and tagged TLBs and optionally requests counter offsets. Apply the admission model.

### Exercise 2

Explain the correct fault owner when stage-one permission allows a write but stage two denies it, and list the minimum exit information needed to decide how to handle it.

### Exercise 3

Design a safe protocol for reusing a finite virtual-machine translation tag after destroying its previous VM.

### Exercise 4

A workload produces $300{,}000$ exits/s at $1.2\ \mu s$, $40{,}000$ exits/s at $5\ \mu s$, and $10{,}000$ exits/s at $3\ \mu s$. Compute $D_e$ and explain what it excludes.

### Exercise 5

An assigned device and its interrupt are being moved between guests. Give the ownership sequence that prevents stale DMA and interrupt delivery.

## Answers to the Exercises

### Answer 1

Required set $R$ is `{nested_translation, tagged_tlb}` and host set $H$ lacks `tagged_tlb`, so $R\nsubseteq H$. Admission fails even though the optional counter-offset mechanism is supported. The monitor may offer a different declared profile with flush-on-switch translation handling, but it must not claim that the original required profile was admitted.

### Answer 2

The denial belongs to monitor-controlled stage two, not the guest operating system's stage-one mapping. The monitor decides whether it represents dirty tracking, copy-on-write, absent backing, protected memory, emulated MMIO or a fatal ownership violation.

The exit must reliably identify the translation stage and walk context, guest-physical address or equivalent fault address, access type, width where relevant, privilege and reason-specific syndrome or qualification. The saved guest PC and retirement state determine resume or exception behavior.

### Answer 3

Stop every vCPU that can issue translations under the old tag or otherwise prevent new uses. Publish that the old context is retired. Issue the architecture-required invalidation for the tag to every processor and relevant translation cache, wait for completion with prescribed barriers, and only then bind the tag to the new translation root and generation. Make the new vCPU runnable after that binding. A time delay is not a substitute for acknowledged invalidation.

### Answer 4

The mean exit service demand is

$$
D_e=(300{,}000)(1.2\times10^{-6})+(40{,}000)(5\times10^{-6})+(10{,}000)(3\times10^{-6})=0.59.
$$

This is about 0.59 CPU-seconds of handler demand per wall-clock second under the stated means. It excludes direct guest execution, waiting behind other exits, host descheduling, userspace backend work not included in the measurements, TLB and cache disruption, nested page walks, interrupt delay and device execution.

### Answer 5

Block new submissions and interrupt generation at the source, then quiesce the device and drain outstanding transactions. Mask and detach its interrupt route, complete pending interrupt-remapping invalidations, remove I/O translations, complete IOMMU invalidations on all relevant caches, and reset the device to a documented clean state. Only after those acknowledgments may the old guest memory and identifiers be reused.

Create the new guest's I/O mappings and interrupt-remapping entry, complete required invalidations, bind the device context, initialize its state, and finally enable interrupts and submissions. If reset cannot isolate all device state, assignment is not safe under this model.
