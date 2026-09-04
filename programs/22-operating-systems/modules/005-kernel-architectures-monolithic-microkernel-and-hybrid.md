---
module_id: OS-005
program: Operating Systems
level: 1
module_number: 5
title: Kernel Architectures: Monolithic, Microkernel, and Hybrid
status: complete
last_verified: 2026-09-04
---

# Kernel Architectures: Monolithic, Microkernel, and Hybrid

## One-Page Review

### Governing question

Which operating-system mechanisms should execute in a privileged kernel, which should live in isolated services, and what evidence shows that the chosen boundaries meet performance, containment, evolution, and assurance needs?

### Essential definitions

- A **monolithic kernel** places most core OS services—commonly scheduling, virtual memory, filesystems, networking, and many drivers—in one privileged address space, often with loadable modules.
- A **microkernel** retains a deliberately small privileged mechanism set and implements many traditional OS services as isolated user-space servers communicating through IPC.
- A **hybrid kernel** deliberately combines mechanisms associated with both families; the label alone does not identify exact placement or isolation.
- The **trusted computing base** (TCB) is the hardware and software whose correct behavior is necessary for a stated security property.
- A **protection domain** is a boundary within which code has a defined set of accessible objects and operations.
- An **IPC fast path** is the latency-critical path for transferring control and data between isolated components.
- **Fault containment** limits direct propagation of a component failure; it does not automatically preserve service availability or data correctness.

### Central model, mechanism, or theorem

Kernel architecture is a placement-and-interface decision over a dependency graph. For each component, choose a protection domain, authority set, communication edges, recovery owner, and update boundary. Then evaluate:

`system outcome = placement + interface semantics + enforcement + implementation quality + operational configuration`.

Moving a driver out of the kernel can remove its direct write authority over kernel memory, but it adds IPC, scheduling, data-transfer, lifecycle, and recovery protocols. Keeping it in the kernel can shorten paths and simplify shared-state coordination, but expands privileged failure impact. Labels summarize a design; they do not prove its properties.

### Critical invariants

- Privileged placement is justified by mechanisms that truly require it, not convenience alone.
- Every cross-domain request authenticates its sender context, validates data, authorizes objects, and bounds resource use.
- Direct mappings, DMA, shared memory, and capabilities do not bypass the stated isolation boundary.
- Failure containment includes dependencies, cached state, in-flight work, and recovery—not only address-space separation.
- IPC preserves ordering, cancellation, partial completion, priority, and backpressure semantics.
- Component restart cannot reuse stale authority or expose a prior instance's resources.
- Performance and assurance claims name the exact configuration, workload, threat model, and evidence scope.

### Common failures

Common errors are equating monolithic with unmodular, equating microkernel with small source size or automatic security, treating hybrid as a precise architecture class, counting context switches without measuring work, assuming process isolation contains DMA, ignoring server dependencies and priority inversion, claiming restartability without reconstructing state, and comparing unlike APIs or configurations.

### Compact example

A storage driver in a monolithic kernel can call filesystem and memory-management code directly, share kernel structures, and submit device work without an IPC round trip. A user-space driver instead receives bounded device and memory authority, serves messages, and returns completions. A memory bug in the isolated driver cannot directly overwrite kernel virtual memory if mappings and DMA controls are correct, but the driver can still corrupt storage commands, delay clients, or fail. The system needs protocol validation, IOMMU configuration, restart state, timeouts, and representative latency evidence.

### Connections

[OS-002](002-privilege-levels-and-protection-rings.md) defines protection domains; [OS-003](003-system-calls-and-user-kernel-transitions.md) and [OS-004](004-interrupts-and-exceptions.md) define crossings. [OS-061](../ROADMAP.md) develops driver models, while [OS-083](../ROADMAP.md) compares hypervisor architectures. Architecture assurance connects to [Security Engineering](../../25-security-engineering/ROADMAP.md) and [Systems Engineering](../../26-systems-engineering/ROADMAP.md).

## Governing Question

An operating system must schedule threads, manage address spaces, handle interrupts, mediate devices, name files, move packets, and enforce policy. The processor requires some trusted privileged code, but it does not dictate that all these responsibilities share one address space. Architecture decides where mechanisms live and how they cooperate.

The familiar monolithic, microkernel, and hybrid labels are starting points, not complete designs. Two “monolithic” systems can differ in module isolation, language safety, driver frameworks, and subsystem boundaries. Two microkernels can retain different primitives and build radically different servers. A hybrid may describe history or marketing more than an auditable placement rule.

The engineering question is concrete: for every responsibility, what privilege and memory authority does it have, through which interface does it interact, what happens when it fails, and what cost does the boundary add under the intended workload?

## Why This Matters

Placement determines blast radius. A parser defect in privileged code may corrupt arbitrary kernel state. The same defect in a restricted server may be confined to that server's memory, provided capabilities, shared mappings, devices, and recovery paths preserve the boundary. Smaller privilege can make some assurance arguments tractable, but system security still depends on trusted services and configuration.

Placement also determines the communication path. A filesystem request may be a direct call through shared structures or a sequence of messages among a client, virtual-filesystem server, filesystem server, and driver. Crossings can add scheduling, copying, cache, translation, and queueing costs. Optimized IPC, shared buffers, batching, and co-location reduce some costs while changing isolation assumptions.

Operational behavior differs too. Isolated services can sometimes restart or update without rebooting the kernel. That benefit is real only when clients reconnect safely, state is reconstructed or reconciled, in-flight operations have known outcomes, and authority from the failed instance is revoked. Architecture is therefore inseparable from protocols and lifecycle engineering.

## Prerequisites and Retrieval

Recall from [OS-002](002-privilege-levels-and-protection-rings.md) that processor privilege is only one dimension of a protection domain. Recall from [OS-003](003-system-calls-and-user-kernel-transitions.md) that crossings require ABI, validation, ownership, and return contracts. You should understand virtual memory, processes, threads, IPC, interrupts, drivers, locks, caches, and basic threat modeling.

Retrieve these distinctions:

- modular source structure does not imply separate protection domains;
- a process boundary restricts memory access only under correctly configured mappings and hardware;
- reliability, availability, safety, and security are related but nonidentical claims;
- fewer lines in privileged mode do not imply fewer trusted assumptions in the complete system;
- a direct function call and an IPC request expose different failure and scheduling semantics;
- one architecture label cannot substitute for a component-and-authority inventory.

## Learning Objectives

After completing this module, you should be able to:

- describe monolithic, microkernel, and hybrid organization without turning labels into universal definitions;
- construct a component placement, authority, communication, and recovery map;
- distinguish modularity, privilege separation, TCB size, attack surface, and fault containment;
- trace an operation through direct-call and server-based designs;
- analyze IPC crossing, copying, scheduling, cache, and queueing costs;
- explain how capabilities, shared memory, DMA, and device access affect isolation;
- design restart, upgrade, cancellation, and partial-completion protocols for isolated services;
- compare architecture choices under performance, assurance, compatibility, and operational constraints;
- design a fair benchmark and fault-injection study;
- identify claims requiring independent security, safety, or certification review.

## Core Exposition

### Architecture as placement and authority

Begin with responsibilities rather than labels: scheduling, physical-memory management, address-space construction, IPC, interrupts, clocks, filesystems, networking, drivers, security policy, and naming. For each, record its executable domain, privilege level, address mappings, device authority, callable interfaces, dependencies, and recovery owner.

This map reveals the architecture. If filesystem and network code execute in the same privileged address space as the scheduler, their internal module boundaries aid development but do not create hardware-enforced memory isolation. If they execute as processes with narrowly granted capabilities, calls become messages and the kernel mediates their resources. Shared libraries, shared pages, kernel extensions, and co-located servers produce intermediate arrangements.

Authority matters more than location names. A nominal user-space driver with an unrestricted physical-memory mapping and unconstrained DMA device can still compromise the machine. A kernel module written in a memory-safe language may reduce one failure class without changing its logical authority. Review executable code, mappings, capabilities, call gates, and device translations.

### Monolithic kernels

A monolithic kernel normally implements most OS mechanisms in a shared privileged address space. Subsystems can invoke one another through ordinary calls and share kernel data structures. Linux is a prominent modular monolithic design: built-in and loadable components participate in one kernel, with configuration, symbol, ownership, and module-lifecycle conventions.

“Monolithic” does not mean one file, one team, no modules, or no abstraction. Mature kernels can have rigorous subsystem APIs, internal object models, loadable drivers, namespaces, policy hooks, and extensive testing. Those software boundaries aid evolution and reasoning. They generally do not prevent a sufficiently powerful memory corruption in one privileged component from modifying another.

Advantages include direct calls, flexible in-kernel composition, shared caches, mature hardware support, and avoiding some IPC and scheduling boundaries on hot paths. Costs include a broad privileged attack surface, difficult fault containment, complicated global concurrency, and upgrades or recovery that may require kernel-wide coordination.

### Microkernels

A microkernel keeps a small set of mechanisms privileged—commonly scheduling, low-level address-space control, interrupt delivery, and IPC—while user-space servers implement services such as filesystems, drivers, or networking. Exact contents differ. Size is a consequence or goal, not a sufficient definition; the decisive feature is enforced separation and service composition over IPC.

The design can reduce the authority of individual services and make their interfaces explicit. A driver fault can be prevented from directly corrupting the kernel or unrelated servers. Services can sometimes be restarted, replaced, or replicated. A small kernel can also support strong verification, as seL4 demonstrates for specified configurations and assumptions.

The trade is distributed-systems-like complexity inside one machine. Naming, discovery, message schemas, request identities, cancellation, priority propagation, server death, client death, buffer ownership, backpressure, and version negotiation become operating-system concerns. IPC performance and scheduler interaction are central. A bug in a critical server can still deny service or corrupt the objects it legitimately owns.

### Hybrid architectures

Hybrid designs combine a microkernel lineage or message-oriented structure with substantial services executing in privileged space, or otherwise mix placements to meet compatibility and performance goals. Apple's XNU identifies itself as a hybrid combining Mach, BSD, and IOKit components. Other systems use “hybrid” differently.

The label gives little evidence by itself. Ask which scheduler, VM, filesystem, network, security, graphics, and driver code runs in which domain; which calls are direct; which messages cross boundaries; and which components can write which memory or devices. The answers, not the category, determine risk and cost.

Hybrid placement can preserve established APIs and driver ecosystems while using selected message abstractions or isolation mechanisms. It can also accumulate multiple synchronization and object-lifetime models. Reviewers should trace actual paths instead of assuming the best property of every ancestor.

### IPC as an architectural substrate

In a server-based OS, IPC is not an auxiliary feature; it is the substrate joining services. The kernel must transfer a message and authority, block or enqueue the sender, wake a receiver, propagate scheduling information where required, and return a reply or failure. Payloads may be copied, mapped, lent, or described through shared memory.

Synchronous request/reply simplifies a sequential service conversation but can create dependency chains and priority inversion. Asynchronous messaging decouples execution but needs explicit correlation, capacity, ordering, cancellation, and completion. Shared buffers improve bandwidth while reintroducing mutable shared state and lifetime hazards.

A fast path can reduce register saves, address-space changes, copies, and scheduler work. Performance still depends on cache warmth, translation state, core placement, message size, contention, server load, and call-chain depth. Counting “two context switches” without defining endpoints and scheduler behavior is not a measurement.

### Failure containment and recovery

Memory isolation prevents direct writes outside a domain under stated hardware and mapping assumptions. It does not prevent semantic harm through authorized messages, corrupted device output, shared pages, or DMA. It also does not guarantee availability: if every file request depends on a failed server, isolation keeps the kernel alive while files remain unavailable.

Recovery requires a state model. Stateless services may restart and re-register. Stateful services must reconstruct from durable state, peers, journals, or client replay. Each in-flight request needs a known disposition: not accepted, accepted but not committed, committed with a lost reply, or completed. Blind replay can duplicate non-idempotent effects.

The recovery manager needs authority to detect failure, revoke the old instance, reset devices, reclaim memory, start a replacement, restore routing, and notify clients. It is itself part of the relevant TCB and availability argument. Cascading restarts and restart loops require budgets and escalation.

### Trusted computing base and assurance

TCB is property-relative. For process-memory isolation, it includes the processor mechanisms, privileged kernel code, page-table management, boot configuration, and any component that can modify those controls. For storage confidentiality, it can also include filesystem and driver code, DMA configuration, firmware, and key management. There is no single context-free TCB count.

A smaller kernel can make code review and formal verification more feasible, but a verified kernel theorem has a specification, configuration coverage, toolchain and hardware assumptions, and properties it does not claim. Unverified servers remain capable of violating services they legitimately control. Formal kernel correctness is not proof that a complete deployed system is safe.

Monolithic systems can use memory-safe languages, control-flow integrity, sanitizers, privilege-restricted helpers, IOMMUs, sandboxed firmware, module signing, and subsystem verification. These controls can reduce risk without changing the high-level label. Compare claims and evidence, not architectural tribal identities.

### Performance accounting

For request path `q`, use an accounting model

`T(q) = T_compute + T_cross + T_copy + T_schedule + T_queue + T_cache + T_device`.

A monolithic path may reduce `T_cross` and `T_schedule` but pay through lock contention or a broad shared cache footprint. A server path may add crossings but improve CPU placement, parallelism, fault isolation, or scheduling control. Batching and shared buffers amortize costs at the expense of latency or stronger sharing assumptions.

Fair comparison holds semantics, hardware, workload, durability, security controls, compiler, power state, and measurement endpoints constant. Report distributions and saturation behavior, not only unloaded averages. A benchmark that disables isolation in one design or omits required durability in another is not comparing the same service.

### Evolution and ecosystem

Stable user APIs, driver availability, debugging tools, observability, and operational expertise often dominate architecture selection. An elegant isolation boundary is expensive if required hardware lacks drivers or if failures cannot be diagnosed. A mature monolithic ecosystem may deliver better real-world reliability than an immature isolated design despite weaker theoretical containment.

Explicit server interfaces can support independent replacement and versioning, but compatibility protocols persist for years. In-kernel interfaces can evolve together because they are shipped as one unit, though external modules constrain that freedom. Source ownership, release cadence, ABI commitments, and deployment model shape the durable architecture.

## Definitions and Notation

Let `C` be components, `D` protection domains, and placement `p: C -> D`. Let `auth(c)` be component `c`'s direct authority over memory, devices, objects, and control state. Let communication graph `G = (C, E)` contain a directed edge for each permitted request or shared-state dependency.

For property `P`, define `TCB(P) ⊆ C` as components whose incorrect behavior can violate `P` under explicit hardware, boot, and configuration assumptions. Domain count alone does not determine `TCB(P)` because an isolated service may remain trusted for the property.

For failure `f` in component `c`, direct memory containment requires that enforcement prevent writes outside `p(c)`. Semantic impact can still follow authorized edges in `G`, shared objects, devices, and dependencies. Thus `contained_memory(f)` does not imply `available(service)` or `correct(output)`.

For request path `q = (c₀, ..., cₙ)`, let `cross(q)` count protection-domain transitions where `p(cᵢ) != p(cᵢ₊₁)`. This count helps explain a path but does not predict latency without payload, scheduling, cache, contention, and hardware evidence.

## Mechanisms, Invariants, or Proof Structure

Review an architecture through seven linked obligations.

**Placement integrity.** Each privileged component has a documented need for authority; executable placement matches the diagram and build configuration.

**Authority integrity.** Mappings, capabilities, handles, device registers, DMA translations, debug paths, and boot controls restrict each domain to its declared resources.

**Interface integrity.** Cross-domain messages validate identity, schema, length, flags, object authority, resource budgets, ordering, and version. Shared memory has publication and lifetime rules.

**Scheduling integrity.** Blocking chains, server priorities, donation or inheritance, queue bounds, overload, and cancellation preserve progress for critical work.

**Lifecycle integrity.** Startup establishes dependencies in a safe order. Shutdown, crash, restart, upgrade, and rollback revoke stale authority and resolve in-flight operations.

**Containment integrity.** Fault injection demonstrates which memory, device, semantic, timing, and availability effects cross each boundary. Claims name what is not contained.

**Evidence integrity.** Security, performance, formal, and safety evidence applies to the exact source, configuration, assumptions, workload, and property being claimed.

The executable model below computes domain placement and crossings for one abstract storage path. It illustrates only graph bookkeeping; it cannot measure IPC or establish containment.

<!-- bijux-verify: {"id":"toy-kernel-placement","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"monolithic-domains=1\nmicrokernel-domains=4\nmonolithic-crossings=0\nmicrokernel-crossings=3\nmonolithic-driver-domain=kernel\nmicrokernel-driver-domain=driver\n","stderr":""}} -->
```python
path = ["client", "vfs", "filesystem", "driver", "device"]
monolithic = {name: "kernel" for name in path}
microkernel = {
    "client": "client",
    "vfs": "vfs",
    "filesystem": "filesystem",
    "driver": "driver",
    "device": "driver",
}


def crossings(placement):
    return sum(placement[left] != placement[right]
               for left, right in zip(path, path[1:]))


print(f"monolithic-domains={len(set(monolithic.values()))}")
print(f"microkernel-domains={len(set(microkernel.values()))}")
print(f"monolithic-crossings={crossings(monolithic)}")
print(f"microkernel-crossings={crossings(microkernel)}")
print(f"monolithic-driver-domain={monolithic['driver']}")
print(f"microkernel-driver-domain={microkernel['driver']}")
```

Passing proves only these assignments and counts. The monolithic model unrealistically places the client and device label in one domain to keep the example compact. No result measures latency, models hardware isolation, represents a complete OS, or proves that more domains are better.

## Alternatives and Trade-Offs

**Direct calls versus IPC.** Direct calls provide low-friction composition and shared data. IPC creates enforcement and explicit ownership but adds marshalling, failure, scheduling, and versioning semantics.

**Kernel drivers versus user-space drivers.** Kernel drivers integrate closely and may minimize crossings. Isolated drivers narrow direct memory authority and can improve restartability, but device DMA, reset, interrupt routing, and recovery must preserve the boundary.

**Shared memory versus copied messages.** Shared memory reduces bulk-copy cost but introduces mutable shared state, synchronization, revocation, and information-flow concerns. Copying produces a stable snapshot at transfer and bandwidth cost.

**Static placement versus adaptive co-location.** Fixed boundaries simplify assurance. Co-locating trusted servers for a workload can reduce crossings, but changes the failure domain and invalidates evidence based on separation.

**Small verified kernel versus richer kernel mechanisms.** Minimal mechanisms can reduce proof scope. Moving policy outward may increase trusted service and protocol work for an end-to-end property. Richer primitives can simplify applications while enlarging privileged specification and implementation.

**Independent service upgrades versus whole-kernel releases.** Service upgrades can reduce disruption and ownership coupling. They require compatible protocols, state transfer, rollback, and mixed-version testing. Whole-kernel releases coordinate changes at the cost of a larger restart boundary.

**Compatibility versus architectural purity.** Existing APIs, drivers, and applications often require placement compromises. A production design should record those trade-offs rather than disguise them with a category label.

## Failure Modes and Misconceptions

1. **“Monolithic means no modules.”** Software modularity and hardware protection domains are different properties.
2. **“Microkernel means few lines.”** Minimal privileged mechanisms and isolated services define the pattern more usefully than an arbitrary size threshold.
3. **“Hybrid has one precise definition.”** Implementations use the label for different placements and histories.
4. **“Microkernels are automatically secure.”** Servers, authority, mappings, DMA, protocols, configuration, and hardware remain in the argument.
5. **“Monolithic kernels cannot be reliable.”** Engineering maturity, controls, testing, and operational evidence matter; the label only shapes certain risks.
6. **“A user-space driver cannot damage the system.”** Authorized commands, shared memory, DMA, firmware, and denial of service can cross the process boundary.
7. **“A live kernel means the service recovered.”** Clients, state, devices, and in-flight outcomes may remain unavailable or inconsistent.
8. **“IPC cost equals a fixed context-switch count.”** Scheduling, copies, caches, payload, contention, and fast paths vary.
9. **“Shared memory gives IPC speed without a trade-off.”** It reintroduces shared-state and lifetime obligations.
10. **“Fewer privileged lines mean a smaller complete TCB.”** TCB membership depends on the property and all components able to violate it.
11. **“Formal verification proves the deployed system.”** The theorem covers named code, configurations, specifications, and assumptions.
12. **“Restart is safe if a process can be relaunched.”** Authority, state, request outcomes, clients, and devices must be reconciled.
13. **“One microbenchmark selects an architecture.”** End-to-end workload distributions, overload, recovery, assurance, and ecosystem costs matter.
14. **“Architecture fixes bad interfaces.”** Ambiguous ownership and cancellation remain dangerous on either side of a boundary.

## Worked Examples

### Example 1

**Question:** Linux has loadable modules. Why is it commonly called monolithic?

**Reasoning:** Modules create build and lifecycle boundaries, but loaded code normally executes with kernel privilege in the shared kernel address space and can call exported kernel interfaces.

**Conclusion:** Modularity does not by itself create a separately enforced protection domain.

### Example 2

**Question:** A filesystem server runs in user space. Is it outside the confidentiality TCB for file contents?

**Reasoning:** It legitimately receives and interprets file data, names, metadata, and storage authority. Isolation may protect the kernel from its memory faults, but the server can still disclose content it is authorized to see.

**Conclusion:** TCB membership is property-relative; user placement does not automatically remove trust.

### Example 3

**Question:** An isolated network driver crashes. What must happen before restart?

**Reasoning:** Delivery must stop, DMA must quiesce, interrupts and mappings must be revoked, in-flight buffers must reach known ownership, device state may need reset, and clients must learn which requests completed.

**Conclusion:** Process relaunch is one step in a device and protocol recovery transaction.

### Example 4

**Question:** A microkernel file read crosses four domains. Is it necessarily slower than a monolithic read?

**Reasoning:** Extra crossings create costs, but batching, shared pages, optimized IPC, CPU placement, cache behavior, lock contention, and device time determine the result. The monolithic path may also queue and schedule.

**Conclusion:** Crossing count explains structure; representative measurement determines performance.

### Example 5

**Question:** A team maps a shared cache into three servers to remove copying. What changed?

**Reasoning:** Bandwidth cost may fall, but corrupted indexes, stale references, synchronization, revocation, and confidentiality now span all three domains. The cache becomes shared trusted machinery for relevant properties.

**Conclusion:** A performance optimization can deliberately widen the effective failure and trust boundary.

### Example 6

**Question:** Does verified microkernel correctness prove that an unverified driver cannot issue a destructive device command?

**Reasoning:** Kernel correctness can enforce the capabilities and memory mappings in its theorem. If policy grants the driver command authority, the driver may misuse that legitimate channel unless another component constrains it.

**Conclusion:** Enforcement proof and authority policy are both required for the end-to-end claim.

### Example 7

**Question:** Why can synchronous IPC cause priority inversion?

**Reasoning:** A high-priority client blocks on a server that runs at lower priority or itself depends on another delayed server. Without priority propagation or suitable scheduling, the request chain inherits the slowest scheduling position.

**Conclusion:** IPC semantics and scheduler policy form one progress argument.

### Example 8

**Question:** A hybrid kernel uses Mach messages internally but runs filesystem and networking code privileged. Which label predicts their fault containment?

**Reasoning:** Neither “hybrid” nor “Mach” shows whether those components share writable kernel memory. The actual placement, mappings, call path, and authority determine containment.

**Conclusion:** Inspect the deployed component map rather than reasoning from ancestry.

### Example 9

**Question:** Can a stateful service upgrade be atomic from every client's perspective?

**Reasoning:** It can be designed so, but requests need identities and commit points, state transfer needs a consistent snapshot or log, routing needs a cutover rule, and old authority must be revoked. Failures during each boundary need recovery.

**Conclusion:** Independent deployment is a protocol property, not a free consequence of process separation.

### Example 10

**Question:** A flight controller isolates an untrusted payload driver with a microkernel. Is the safety case complete?

**Reasoning:** The review must include capability configuration, shared memory, DMA and IOMMU, interrupt timing, scheduler budgets, trusted servers, device failure, recovery, physical interfaces, and the exact verified-kernel assumptions.

**Conclusion:** A named safety authority and security reviewer must assess end-to-end evidence and residual risk; this chapter makes no certification claim.

## Cross-Program Connections

[Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) develops component boundaries, quality attributes, and architecture decisions. Kernel architecture adds hardware privilege, interrupt context, DMA, and low-level scheduling. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) connects message protocols, partial failure, retries, naming, and state recovery even when components share one machine.

[Security Engineering](../../25-security-engineering/ROADMAP.md) owns threat modeling, least privilege, TCB reasoning, capabilities, and assurance. [Computer Architecture](../../23-computer-architecture/ROADMAP.md) owns privilege, MMUs, IOMMUs, interrupt controllers, and crossing costs. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) applies analogous shared-service, tenancy, lifecycle, and developer-interface choices above the kernel.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) adds hazard analysis, independence, lifecycle traceability, and accountable acceptance. Successors [OS-006](../ROADMAP.md) through [OS-010](../ROADMAP.md) develop initialization, kernel structures, allocation, modules and drivers, and complete request traces inside whichever architecture is chosen.

## References

- Linux Kernel documentation, [Driver implementer's API guide](https://docs.kernel.org/driver-api/index.html), current page checked 2026-09-04. Primary documentation index for Linux's in-kernel driver and subsystem interfaces.
- Linux Kernel documentation, [The Linux kernel module signing facility](https://docs.kernel.org/admin-guide/module-signing.html), current page checked 2026-09-04. Documents module loading policy and integrity controls without implying memory isolation among loaded code.
- Apple Open Source, [XNU README](https://github.com/apple-oss-distributions/xnu/blob/main/README.md), current source checked 2026-09-04. Identifies XNU as a hybrid of Mach, BSD, and IOKit and maps its source subsystems.
- BlackBerry QNX, [Microkernel architecture](https://www.qnx.com/developers/docs/7.1/com.qnx.doc.neutrino.sys_arch/topic/intro_MICROKERNELARCH.html), current page checked 2026-09-04. Official account of QNX service placement and message-oriented modularity.
- BlackBerry QNX, [QNX Neutrino as a message-passing operating system](https://www.qnx.com/developers/docs/7.1/com.qnx.doc.neutrino.sys_arch/topic/intro_Message_passing_OS.html), current page checked 2026-09-04. Documents the role and semantics of message passing among QNX components.
- seL4 Foundation, [*The seL4 Microkernel—An Introduction*](https://sel4.systems/About/seL4-whitepaper.pdf), revision 1.4, 2025. Overview of seL4 mechanisms, assurance claims, configurations, and limitations.
- Gerwin Klein et al., [*seL4: Formal Verification of an OS Kernel*](https://sel4.org/Research/pdfs/sel4-formal-verification-os-kernel.pdf), SOSP, 2009. Primary paper describing a machine-checked functional-correctness result and its assumptions.
- Jochen Liedtke, [*On Micro-Kernel Construction*](https://os.inf.tu-dresden.de/L4/doc.html), SOSP, 1995, linked from the L4 project's publication archive. Primary L4 work on minimality and IPC-path design.
- Brian N. Bershad et al., [*Extensibility, Safety and Performance in the SPIN Operating System*](https://www-spin.cs.washington.edu/papers/SOSP95/abstract.html), SOSP, 1995. Primary project publication on a language-based approach to extensible in-kernel services.
- Fuchsia project, [Zircon kernel concepts](https://fuchsia.dev/fuchsia-src/concepts/kernel), current page checked 2026-09-04. Official description of Zircon kernel objects, handles, IPC, scheduling, and user-space services.
- Microsoft Learn, [User mode and kernel mode](https://learn.microsoft.com/en-us/windows-hardware/drivers/gettingstarted/user-mode-and-kernel-mode), current page checked 2026-09-04. Official description of Windows execution modes and failure consequences, used here without inferring a complete architecture from the mode split.

## Exercises

### Exercise 1

Create a placement-and-authority table for scheduler, VM, filesystem, network stack, storage driver, security policy, and update manager in one monolithic and one microkernel design. Identify the TCB for process-memory isolation and separately for file confidentiality.

### Exercise 2

Trace a 64 KiB file read through direct in-kernel calls and through client, VFS server, filesystem server, and driver. Account for crossings, copies or mappings, scheduling, queueing, cache state, cancellation, and partial completion without asserting a winner.

### Exercise 3

Design the recovery protocol for a user-space storage driver that crashes after submitting a write but before replying. Cover request identity, commit ambiguity, DMA, device reset, buffer ownership, replay, client notification, and repeated failure.

### Exercise 4

Design a fair experiment comparing two kernel architectures for a network appliance. Define equivalent service semantics and security controls, workloads, latency endpoints, percentiles, throughput, CPU use, overload, fault injection, recovery, and evidence limitations.

### Exercise 5

A railway platform proposes a verified microkernel with unverified signaling servers and drivers. Construct the assurance review needed before claiming failure containment or safety. Separate kernel theorem, configuration, component evidence, hardware assumptions, operational controls, and named human judgment.

## Answers to the Exercises

### Answer 1

The monolithic design may place all seven responsibilities in a kernel domain while retaining strong internal module boundaries. The microkernel design might keep scheduling and low-level VM in the kernel, place filesystem, network, driver, policy, and update responsibilities in separate services, and grant each explicit capabilities. The table must also list page mappings, device registers, DMA windows, shared buffers, debug authority, and allowed calls.

For process-memory isolation, the TCB includes processor translation and privilege mechanisms, boot configuration, microkernel or monolithic VM and scheduler code that manages domains, and every component able to change their mappings or authority. A user filesystem need not belong if it cannot affect those controls. For file confidentiality, the filesystem, storage path, authorized policy services, key management, driver or device components that see plaintext, DMA controls, and relevant firmware can join the TCB even when they run unprivileged. Property-relative analysis produces different sets.

### Answer 2

In the monolithic path, the client enters the kernel once; VFS, filesystem, cache, and driver code may call directly and share kernel buffers before return. Account for user copies, cache misses, locks, block-layer queues, device time, wakeups, and result copy-out. A cache hit may never reach the driver.

In the server path, the client sends to VFS, which may call a filesystem server and driver. Each edge can block and schedule, copy a message, map pages, or reference registered shared buffers. Count actual protection-domain transitions, payload movements, cache and translation disruption, queue waits, and device work. Define who cancels downstream requests and how a short or failed transfer propagates. For both designs measure the same durability and authorization semantics, cached and uncached cases, request sizes, concurrency, affinities, and high-percentile end-to-end latency. The trace identifies terms; it cannot select a winner without data.

### Answer 3

Give each write a stable client and generation identity plus a device-level completion record. Before submission, the driver owns a registered buffer and records enough intent for recovery. A supervisor detects death, blocks routing, revokes the old process's mappings, quiesces DMA and interrupts, and determines whether the device accepted or completed the command. Memory is not reused until access has stopped.

If durable state or device logs prove commitment, the replacement reports success without replay. If they prove nonacceptance, replay is allowed. If status is ambiguous, the protocol needs an idempotency token, a read-after-recovery reconciliation rule, or an explicit unknown outcome; blind replay can duplicate or reorder effects. Reset must preserve or deliberately invalidate controller state according to the device contract. Clients receive final status and retain buffers until ownership returns. Repeated crashes trigger bounded retries, isolation of the device or service, and escalation rather than an infinite restart loop.

### Answer 4

Implement equivalent routing, filtering, durability, observability, and isolation requirements on identical hardware and firmware. Pin or deliberately balance queues under documented policies. Exercise small and large packets, flows, connection churn, sparse latency traffic, sustained line rate, bursts beyond capacity, adversarial malformed inputs, and mixed management traffic.

Timestamp application request, kernel or server entry points, device submission and completion, and application-visible completion with stated clock domains. Report median and high-percentile latency, throughput, drops, CPU cycles, crossings, copies, scheduler delay, queue depth, cache and translation counters where trustworthy, and energy if relevant. Inject driver, network-server, and policy-server faults; measure corrupted scope, detection, quiescence, restart, lost or duplicated work, and recovery time. Keep mitigations and DMA isolation equivalent. Publish configurations, run order, uncertainty, and claims the experiment cannot establish.

### Answer 5

State the safety property and threat model first. Map signaling commands, timing deadlines, component dependencies, capabilities, shared pages, device access, DMA, interrupts, boot chain, firmware, diagnostics, and recovery authority. Read the exact kernel theorem: source revision, generated configuration, supported architecture, compiler and hardware assumptions, refinement boundary, proved properties, and exclusions. Verify that the deployed binary and capability configuration fall within that evidence.

Review each unverified server and driver for memory safety, protocol state, authorization, resource budgets, priority propagation, stale commands, cancellation, restart, versioning, and failure escalation. Test malformed messages, compromised authorized components, timing overload, server and driver crashes, DMA escape, device reset, common-cause faults, and degraded operation. Operational controls cover build provenance, secure boot, updates, configuration drift, monitoring, incident response, and maintenance. Independent physical and logical interlocks must enforce safe states where required. A named safety engineer, railway domain authority, security reviewer, assurance specialist, and acceptance owner must evaluate traceability, independence, evidence coverage, unresolved findings, and residual risk. Neither the architecture label nor the kernel proof alone certifies the whole railway system.
