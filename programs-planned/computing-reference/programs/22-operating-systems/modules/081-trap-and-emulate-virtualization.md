---
module_id: OS-081
program: Operating Systems
level: 2
module_number: 81
title: Trap-and-Emulate Virtualization
status: complete
last_verified: 2026-09-04
---

# Trap-and-Emulate Virtualization

## One-Page Review

### Governing question

How can a virtual-machine monitor let ordinary guest instructions execute efficiently while retaining control of every operation that could reveal or alter the real machine?

### Essential definitions

- A **virtual-machine monitor** (VMM), or hypervisor, mediates physical resources while presenting each guest with a virtual machine.
- **Direct execution** runs a guest instruction on the physical processor without software interpretation.
- A **privileged instruction** traps or faults when executed without the required processor privilege.
- A **sensitive instruction** changes resource configuration or behaves according to hidden privileged state.
- A **trap** transfers control to a more privileged handler with architectural cause and saved guest state.
- **Emulation** computes the guest-visible architectural effects of an intercepted operation without granting its physical effects.
- **Shadow state** is monitor-owned state that represents guest-visible control state while protecting host-owned state.
- **Equivalence** means that a guest observes the specified virtual-machine behavior, allowing only documented differences such as resource availability or timing.

### Central model, mechanism, or theorem

For an instruction whose virtual effect is safe, execute it directly. For a sensitive operation, enter the monitor, identify the exact guest operation, validate it against the virtual-machine contract, compute all guest-visible effects, commit them atomically or inject the specified guest exception, and resume at the architecturally correct program counter. In the classical model, a sufficient condition for efficient trap-and-emulate virtualization is that every sensitive instruction is privileged. This condition is sufficient within that model, not a universal definition of virtualization.

### Critical invariants

- A guest cannot directly mutate monitor or another guest's resources.
- An intercepted instruction retires exactly once or faults exactly as the virtual architecture specifies.
- The saved program counter, privilege, flags, fault address, access width and exception metadata agree.
- Shadow state and effective hardware state have an explicit synchronization rule.
- Device reads, writes, interrupts and DMA preserve ordering and ownership.
- Guest-visible time remains within its declared monotonicity, rate and suspension contract.
- Unsupported inputs fail closed as guest exceptions or bounded monitor errors.

### Common failures

The monitor advances the PC after a fault that should retry; decodes bytes from a page the guest changes concurrently; exposes host control bits through a read; applies a device write twice; loses an interrupt edge; lets stale shadow translations survive a mapping change; or reports host elapsed time as guest CPU time.

### Compact example

A guest writes a virtual control register. The write traps. The monitor masks reserved bits, updates the guest's shadow register, synchronizes only the permitted effective controls, advances the guest PC once, and resumes. Writing the physical register directly would violate control; ignoring the write would violate equivalence.

### Connections

This mechanism connects exception handling, instruction-set semantics, memory protection, device models, schedulers, timekeeping, security monitors, binary translation and paravirtual interfaces.

## Governing Question

Trap-and-emulate is not simply “catch privileged instructions.” It is a refinement problem: the real execution, including monitor intervention, must implement a virtual architecture whose resources the monitor can control. The central engineering question is which operations may run directly, which must be intercepted, and what exact state transition each intercept must produce.

## Why This Matters

Virtual machines run operating systems that expect to own processors, page tables, interrupt controllers, timers and devices. Sharing those resources requires mediation, but interpreting every instruction sacrifices the principal performance advantage of same-ISA virtualization. Direct execution is attractive precisely because most computation is innocuous. It is safe only when every operation that can escape the virtual abstraction is intercepted or transformed.

The difficult bugs live at boundaries: fault versus trap semantics, instruction bytes versus mutable memory, guest privilege versus host privilege, shadow versus effective state, CPU versus device ordering, and wall time versus scheduled time. A monitor can appear functional while corrupting rare instructions, mishandling partial device operations or leaking cross-guest state. The design therefore needs explicit architectural obligations, not a list of exit handlers.

## Prerequisites and Retrieval

Before studying this module, be able to:

- describe processor privilege levels, exceptions, precise architectural state and instruction retirement;
- distinguish virtual addresses, guest-physical addresses and host-physical addresses;
- reason about page tables, TLB invalidation, memory-mapped and port-mapped I/O;
- explain interrupts, DMA, timers and multiprocessor memory ordering;
- read an instruction-set architecture specification and a device register contract.

When evaluating an implementation, retrieve the exact guest ISA revision, host ISA revision, processor errata, VMM version, machine type, virtual CPU model, device model, firmware, migration compatibility profile and enabled acceleration. Names such as “x86,” “virt machine,” or “legacy NIC” are not precise semantic versions.

## Learning Objectives

After completing this module, you should be able to:

1. explain direct execution, trapping, emulation and their control boundary;
2. classify privileged, control-sensitive, behavior-sensitive and innocuous operations;
3. apply the classical virtualizability condition without overstating its necessity or scope;
4. design a precise exit-to-resume state machine for CPU and device operations;
5. preserve exception, program-counter, register, memory and interrupt semantics;
6. manage shadow control, translation, time and device state with explicit coherence rules;
7. compare trap-and-emulate with interpretation, binary translation, paravirtualization and hardware assistance;
8. test equivalence, isolation, progress, migration and exit-path performance adversarially.

## Core Exposition

### Start with the virtual architecture contract

Define the machine the guest is promised: instructions, registers, privilege rules, exceptions, memory model, interrupt controller, timers, devices, topology and reset behavior. The physical host is an implementation resource, not the guest contract. Compatibility profiles must freeze guest-visible details that migration or upgrades cannot silently change.

### Separate control from equivalence

Resource control means the monitor can reclaim or deny physical CPU, memory and I/O. Equivalence means accepted guest operations behave as specified by the virtual machine. A monitor that protects itself but returns invented register values has control without equivalence. A faithful device model with unrestricted DMA has equivalence without control.

### Classify instructions by semantic effect

Privileged describes how the processor reacts at insufficient privilege. Control-sensitive operations attempt to change resource configuration, such as address translation or interrupt masking. Behavior-sensitive operations reveal or vary with privileged configuration. Innocuous operations do neither under the model. These sets overlap but are not synonyms.

### Apply the classical sufficient condition carefully

Popek and Goldberg's classical result gives a sufficient construction when the set of sensitive instructions is a subset of the privileged instructions. Then sensitive operations trap outside their required privilege, while innocuous instructions can execute directly. The result depends on its abstract machine and VMM definitions. Binary translation, paravirtualization and later architectural facilities can virtualize cases outside the simple construction.

### Build a run-intercept-emulate loop

The monitor restores guest state and enters guest execution. An intercept saves architecturally defined state and a reason. The handler validates the source, reconstructs the operation, applies virtual policy and semantics, commits state, queues any resulting event, chooses retry or next PC, and re-enters. Host scheduling and signals may occur around this loop, so incomplete operations need explicit ownership.

### Preserve precise retirement semantics

A fault commonly reports the offending instruction for retry; a trap may report the following instruction. Architecture-specific definitions prevail. The emulator must know whether memory or register side effects already occurred. Advancing the PC on a non-retired fault skips work; failing to advance after successful emulation repeats it. Both can corrupt a guest silently.

### Treat instruction decoding as security-critical

Variable-length instructions, prefixes, address sizes, segment rules and cross-page fetches enlarge the decoder surface. The monitor must bind decoded bytes to the guest state that caused the exit. If another vCPU can rewrite executable memory between exit and fetch, revalidation, protected fetch or architecture-provided decode information is required. Unsupported encodings must not fall through as privileged host work.

### Reconstruct effective addresses exactly

An I/O or protected-memory access may depend on registers, privilege, segmentation, paging, alignment, endianness and access width. Emulation must reproduce fault ordering and partial-access rules, not merely calculate a host pointer. Guest addresses must pass through monitor-owned translation and bounds checks before touching backing memory or devices.

### Maintain shadow control state

A guest may believe it controls flags or registers that the monitor cannot install literally. Store a guest-visible shadow, derive the safe effective value, and define which reads return shadow versus synthesized state. Reserved bits, write-one-to-clear fields and dependent controls require per-field semantics. Copying host state into guest reads leaks implementation and may break migration.

### Virtualize address translation coherently

Without a directly usable guest translation regime, the monitor can derive shadow translations that combine guest mappings with host ownership. Guest page-table writes, control-register changes, invalidations and aliases must invalidate affected shadow entries before stale access becomes possible. Write protection or instruction transformation can expose updates, but both need progress and race rules.

### Model exceptions as guest events

Emulation can succeed, reject an operation, or discover an architectural fault. A guest fault needs the specified vector or syndrome, error code, address, privilege transition and delivery ordering. A monitor bug is not automatically a guest machine check. Nested faults and event-delivery failures need bounded escalation rather than recursive corruption.

### Model interrupts as state, not callbacks

An interrupt may be pending while masked, coalesced, level asserted until acknowledgment, or edge-triggered once. The virtual controller owns priority, destination, masking and acknowledgment. Injection occurs only at a legal guest boundary. Lost edges harm liveness; duplicate level delivery can repeat device work; premature acknowledgment can erase the source.

### Emulate device registers transactionally

MMIO and port I/O can have read side effects, posted writes, byte enables, split accesses and ordering constraints. Decode address and width, validate the region, perform one device-model transition, return read data or record write completion, and retire once. Re-entry protocols must identify whether a userspace device operation is pending so migration cannot snapshot a half-completed instruction.

### Keep DMA behind an ownership boundary

An emulated device should read and write guest-owned memory through checked guest-physical mappings. A passed-through device additionally needs I/O translation, interrupt remapping, reset isolation and invalidation ordering. CPU instruction trapping alone cannot contain a bus master that can address host memory.

### Virtualize time as an explicit policy

Guests can observe counters, timers, interrupt cadence and scheduling gaps. Define whether clocks track wall time, execution time, or a scaled virtual timeline; whether suspend advances them; and how migration preserves monotonicity. Trapping every time read is expensive, while direct reads need offset, scale and stability controls. Timing differences may remain observable even when functional equivalence holds.

### Coordinate multiple virtual CPUs

Each vCPU has architectural state, but shared memory, interrupt controllers, devices and global control registers create cross-vCPU order. Emulation locks must preserve the guest memory model without serializing unrelated work. A vCPU exit cannot assume peers stopped. Reset, TLB shootdown and virtual interrupt delivery require explicit rendezvous or generation protocols.

### Bound monitor work and guest influence

Exit reasons, instruction bytes, register values and device inputs are attacker-controlled. Decoders, maps, queues and retry loops need bounds. Rate-limit pathological exits without violating the advertised machine, and separate “guest receives an architectural fault” from “VM is terminated by operational policy.” Host secrets must never enter diagnostic state returned to the guest.

### Optimize exits only after measuring semantics

Exit cost includes guest-to-monitor transition, state save, dispatch, emulation, locks, userspace crossings, scheduling and re-entry. First reduce avoidable exit frequency: batch I/O, use shared rings, coalesce interrupts or permit safe direct execution. Then shorten handlers and avoid global contention. An average exit time hides expensive reasons and queueing tails.

### Make migration replay one coherent machine

Migration state includes virtual CPU registers, shadow-visible controls, pending and in-service interrupts, device queues, timers, dirty memory and incomplete emulation. Quiesce or complete operations according to their interface contract. Restore using a compatible virtual machine profile, not whichever host feature set happens to exist at the destination.

### Test differential behavior

Compare a guest operation on the reference architecture and virtual machine: result registers, memory, flags, exceptions, PC, device state and event order. Generate reserved encodings, page-boundary instructions, concurrent code modification, invalid widths, interrupted I/O and reset races. Differential tests complement isolation tests, fuzzing, migration cycles and exit-distribution measurements.

### State the assurance boundary

Passing conformance tests supports selected architectural claims. It does not prove freedom from side channels, microarchitectural leakage, host-kernel defects, device firmware bugs or denial of service. Trap-and-emulate controls architectural operations; broader isolation also depends on memory translation, scheduling, DMA containment and platform security.

## Definitions and Notation

Let guest-visible state be $g\in G$, monitor state be $v\in V$, and physical state be $h\in H$. A representation function

$$
\alpha(v,h)=g
$$

maps implementation state to the virtual state observed by the guest.

For guest instruction $i$, let the promised virtual transition be $A_i:G\rightarrow G\cup E$, where $E$ is a guest-visible exception. Let an implementation step sequence be $R_i$ over monitor and host state. Correct emulation requires

$$
\alpha(R_i(v,h))=A_i(\alpha(v,h))
$$

for admitted starting states, including the same retirement or exception outcome. Timing equality is included only if the virtual contract promises it.

Let $S$ be the set of sensitive instructions and $P$ the set of privileged instructions in the classical model. The familiar sufficient condition is

$$
S\subseteq P.
$$

It enables sensitive operations to trap when the guest runs without monitor privilege; it is not asserted here as a necessary condition for every virtualization technique or modern ISA.

For exit reasons $r$, let arrival rate be $\lambda_r$ and mean service demand be $c_r$. Approximate monitor utilization from exits is

$$
U_e=\sum_r \lambda_r c_r.
$$

As shared-handler utilization approaches capacity, queueing can dominate transition time. This accounting omits direct guest execution, device backends and host scheduling unless added explicitly.

Let shadow object generation be $q_s$ and the latest guest configuration generation be $q_g$. A shadow-derived access is admissible only when $q_s=q_g$ for every dependency or after a synchronization rule proves equivalent freshness.

## Mechanisms, Invariants, or Proof Structure

Review a trap-and-emulate design with these obligations.

1. **Contract obligation:** the virtual ISA, CPU model, memory model, devices, time and reset semantics are versioned.
2. **Classification obligation:** every operation that can change or observe protected resources is intercepted, transformed or proven safe.
3. **Control obligation:** no guest transition directly mutates monitor, host or peer-owned state.
4. **Refinement obligation:** each admitted operation matches virtual results, side effects, faults and event order.
5. **Retirement obligation:** the saved and resumed PC causes exactly one retirement or the specified retry.
6. **Decode obligation:** bytes, mode, privilege, width and effective address are bound to the exiting operation.
7. **Shadow obligation:** guest-visible and effective state have explicit derivation, invalidation and readback rules.
8. **Device obligation:** register, interrupt and DMA transitions preserve width, ordering, ownership and completion.
9. **Concurrency obligation:** peer vCPUs cannot invalidate assumptions between validation and commit.
10. **Progress obligation:** repeated exits, blocked backends and event delivery have bounded forward-progress rules.
11. **Lifecycle obligation:** reset, snapshot and migration serialize all pending CPU, device and timer state coherently.
12. **Assurance obligation:** tests and claims state architectural, performance, isolation and side-channel limits separately.

The refinement argument has a direct case and an intercepted case. In the direct case, classification and host execution establish that the physical transition projects to the promised guest transition without escaping resource control. In the intercepted case, precise saved state, validated decoding, virtual-model execution and atomic commit establish the same projection. Exception delivery and retry form explicit subcases.

This argument is conditional on the ISA model, decoder, memory ownership, device model, concurrency protocol and hardware behavior. It is not completed by observing that the guest boots.

## Alternatives and Trade-Offs

- **Direct execution versus interpretation:** direct execution is fast for safe instructions; interpretation gives uniform control at high cost.
- **Trap-and-emulate versus binary translation:** trapping uses architectural interception; translation can rewrite non-trapping sensitive sequences and adds cache invalidation complexity.
- **Full virtualization versus paravirtualization:** full virtualization preserves an unmodified guest interface; paravirtualization exposes cooperation and compatibility work.
- **Kernel versus userspace emulation:** kernel handling avoids crossings; userspace narrows kernel complexity and can increase latency.
- **Shadow state versus literal passthrough:** shadows preserve a stable contract; passthrough reduces emulation and binds the guest to host behavior.
- **Fine exits versus batched interfaces:** fine exits preserve legacy register semantics; batches amortize transitions and need guest-aware protocols.
- **Synchronous versus posted writes:** synchronous completion simplifies order; posting improves throughput and complicates failure visibility.
- **Device emulation versus passthrough:** emulation supports compatibility and migration; passthrough improves data-path performance and expands isolation dependencies.
- **Global locks versus partitioned models:** global locks simplify shared-device order; partitioning improves scalability and complicates coordination.
- **Wall time versus execution time:** wall time matches external clocks; execution time hides descheduling and diverges from reality.
- **Strict fidelity versus compatibility quirks:** strict models are easier to reason about; real guests may depend on historical behavior.
- **Terminate versus inject a fault:** termination contains unknown states; architectural faults preserve availability only when semantics are known.
- **Broad host feature exposure versus a baseline CPU:** broad exposure improves performance; baselines support migration and reproducibility.
- **Exit coalescing versus latency:** coalescing reduces overhead; delayed events can violate responsiveness or timer assumptions.
- **Transparent timing versus deterministic time:** realistic time supports production guests; controlled time supports replay and changes external interaction.
- **Nested virtualization versus one monitor level:** nesting enables infrastructure use cases; exit ownership and state composition become harder.

## Failure Modes and Misconceptions

- “Privileged and sensitive mean the same thing.” One is a processor access rule; the other is a virtualization property.
- “The classical subset condition is necessary for all virtualization.” It is a sufficient condition in its model.
- “A trap automatically emulates an instruction.” It only transfers control and records architecture-defined state.
- “Booting proves equivalence.” Rare faults, devices, concurrency and migration can still diverge.
- “The PC always points at the failing instruction.” Fault and trap conventions differ by architecture and exit.
- “Advancing the PC is harmless.” It can skip a faulting operation or double-retire a completed one.
- “The instruction bytes cannot change during an exit.” Another vCPU or alias may modify them.
- “A decoder only affects compatibility.” It consumes attacker-controlled bytes in a privileged component.
- “Returning zero for an unknown register is safe.” The architecture may require a fault or reserved value.
- “Shadow state is a cache.” Some shadow values are the authoritative guest-visible contract.
- “Invalidating one virtual address always suffices.” Aliases, page sizes and global mappings may widen scope.
- “CPU trapping contains DMA.” A device bus master needs separate translation and reset isolation.
- “MMIO is ordinary memory.” Reads and writes can have side effects and ordering rules.
- “A userspace exit means the instruction completed.” Some interfaces complete only on re-entry.
- “An interrupt is a function call.” It has pending, mask, priority, level and acknowledgment state.
- “Dropping duplicate interrupts is an optimization.” Edge and level semantics decide correctness.
- “Guest time is host time.” Descheduling, offset, scale, suspension and migration intervene.
- “Direct counter reads are always transparent.” Host topology and scheduling can leak through timing.
- “One exit-cost average predicts performance.” Reason mix, contention and tails matter.
- “Faster emulation always helps.” Reducing exit frequency can dominate handler tuning.
- “A global device lock guarantees correctness.” It may preserve order while destroying progress.
- “Reset clears only registers.” Pending events, DMA, queues, timers and backend work also matter.
- “Migration is a memory-copy problem.” In-flight emulation and device state must form one snapshot.
- “Hardware assistance removes emulation.” Devices and selected operations still require models.
- “Architectural isolation proves side-channel isolation.” Microarchitectural and timing channels remain separate claims.

## Worked Examples

### Example 1

A guest clears a virtual interrupt-enable bit. The operation traps, the monitor updates the guest shadow flag, leaves host interrupts enabled, and suppresses guest interrupt injection until the guest unmasks. Installing the literal physical flag would surrender host control.

### Example 2

The following executable toy distinguishes direct instructions from intercepted operations and commits each virtual effect once. It demonstrates one state-machine shape only, not an ISA decoder, privilege mechanism, concurrent VMM or secure device model.

<!-- bijux-verify: {"id":"trap-and-emulate-state-machine","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"pc=5 acc=6 ctrl=3 halted=True\nexits=4 reasons=write_ctrl,read_ctrl,io_write,halt\ndevice_log=9\n","stderr":""}} -->
```python
program = [
    ("ADD", 3),
    ("WRITE_CTRL", 19),
    ("READ_CTRL",),
    ("IO_WRITE", 9),
    ("HALT",),
]
state = {"pc": 0, "acc": 0, "ctrl": 0, "halted": False}
exits = []
device_log = []

while not state["halted"]:
    instruction = program[state["pc"]]
    opcode = instruction[0]
    if opcode == "ADD":
        state["acc"] += instruction[1]
    else:
        exits.append(opcode.lower())
        if opcode == "WRITE_CTRL":
            state["ctrl"] = instruction[1] & 0b111
        elif opcode == "READ_CTRL":
            state["acc"] += state["ctrl"]
        elif opcode == "IO_WRITE":
            device_log.append(instruction[1])
        elif opcode == "HALT":
            state["halted"] = True
        else:
            raise ValueError("unsupported intercepted operation")
    state["pc"] += 1

print(f"pc={state['pc']} acc={state['acc']} ctrl={state['ctrl']} halted={state['halted']}")
print(f"exits={len(exits)} reasons={','.join(exits)}")
print(f"device_log={','.join(map(str, device_log))}")
```

### Example 3

An intercepted instruction spans two guest pages. Fetch of the second page faults under guest translation. The monitor injects the specified instruction-fetch exception without performing the operation; substituting a host-side read from backing memory would bypass guest permissions.

### Example 4

A guest writes a page-table entry while another vCPU uses a derived shadow entry. Write protection exposes the update, the monitor advances the guest generation, invalidates every dependent shadow mapping, completes the write, and lets peers resume only after the invalidation barrier.

### Example 5

An MMIO read exits to a userspace device model. The backend supplies the value, but the interface defines completion on the next run call. Snapshotting before re-entry can capture neither the pre-read nor post-read machine, so migration first completes the pending operation without executing a later guest instruction.

### Example 6

A level-triggered virtual device asserts an interrupt. The controller records it pending, injects when the vCPU admits it, retains the source through masking, and clears only after virtual acknowledgment and device deassertion. Treating it as one callback loses a persistent level.

### Example 7

One workload performs a million byte-at-a-time port writes per second. Handler optimization saves little compared with replacing the legacy interface with a shared queue and notification. Exit-frequency reduction changes $\lambda_r$ rather than only $c_r$.

### Example 8

A virtual clock uses host elapsed time. During migration the destination counter is behind the source. Restoring without an offset makes time move backward; the migration contract must carry a correction or choose a different virtual time policy.

### Example 9

A passed-through device is function-reset during VM teardown but an outstanding DMA transaction still targets an old mapping. Safe reuse requires quiescence, I/O translation invalidation completion and interrupt cleanup before assigning memory or the device to another owner.

### Example 10

Differential testing finds that a reserved control-register bit faults on hardware but is silently cleared by the emulator. The guest usually boots, yet the mismatch can break feature detection. The fix follows the virtual CPU specification, not the behavior most workloads tolerate.

## Cross-Program Connections

- **Computer architecture:** privilege, precise exceptions, instruction decoding, MMUs and interrupt controllers define the intercept substrate.
- **Security engineering:** least privilege, complete mediation, decoder hardening, DMA containment and side-channel boundaries define isolation.
- **Formal methods:** abstraction functions, refinement, invariants and differential testing structure equivalence arguments.
- **Performance engineering:** exit rates, handler demand, batching, contention and tail latency determine overhead.
- **Distributed systems:** clocks, partial progress, replay and migration expose state-machine and ordering problems.
- **Network and storage engineering:** virtual devices, queues, DMA, interrupts and completion rules carry data-path semantics.
- **Platform engineering:** machine types, compatibility profiles, lifecycle control, observability and fleet migration operationalize VMs.
- **Compiler engineering:** binary translation, code caches, self-modifying code and precise exception recovery provide alternative interception.
- **API and service engineering:** versioned contracts, failure semantics and backward compatibility recur at the virtual hardware boundary.
- **Reliability engineering:** reset, snapshot, fail-closed handling, fuzzing and recovery test incomplete operations.

## References

1. Gerald J. Popek and Robert P. Goldberg, [Formal Requirements for Virtualizable Third Generation Architectures](https://www.cs.cornell.edu/courses/cs6411/2018sp/papers/popek-goldberg.pdf), classical VMM properties, sensitive instructions and sufficient virtualizability conditions; retrieved 2026-09-04.
2. Intel, [Intel 64 and IA-32 Architectures Software Developer Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), privilege, exceptions, system programming and virtual-machine extensions; retrieved 2026-09-04.
3. AMD, [AMD64 Architecture Programmer's Manual, Volume 2: System Programming](https://docs.amd.com/v/u/en-US/24593_3.44_APM_Vol2), system registers, memory management, protection, interrupts and exceptions; retrieved 2026-09-04.
4. Linux Kernel Documentation, [KVM API](https://docs.kernel.org/virt/kvm/api.html), vCPU execution, exit reasons, MMIO, I/O, emulation and pending-operation completion; retrieved 2026-09-04.
5. Linux Kernel Documentation, [The x86 KVM Shadow MMU](https://docs.kernel.org/virt/kvm/x86/mmu.html), guest translation, shadow pages, invalidation and synchronization; retrieved 2026-09-04.
6. Linux Kernel Documentation, [Timekeeping Virtualization for x86-Based Architectures](https://docs.kernel.org/virt/kvm/x86/timekeeping.html), virtual clocks, timers, scheduling and migration concerns; retrieved 2026-09-04.
7. QEMU Project, [Translator Internals](https://qemu.readthedocs.io/en/master/devel/tcg.html), dynamic translation, translation blocks, exception recovery and software MMU behavior; retrieved 2026-09-04.
8. QEMU Project, [System Emulation](https://qemu.readthedocs.io/en/master/system/), full-system and device-emulation documentation; retrieved 2026-09-04.
9. Xen Project, [Virtualization Concepts](https://handbook.xenproject.org/users/concepts.html), full virtualization, paravirtualization, hypercalls and device-model trade-offs; retrieved 2026-09-04.
10. RISC-V International, [Hypervisor Extension](https://docs.riscv.org/reference/isa/priv/hypervisor), hypervisor privilege, virtualized control state, traps and virtual-machine memory operations; retrieved 2026-09-04.

## Exercises

### Exercise 1

Classify a hypothetical instruction that reads the physical interrupt-mask state but does not trap at guest privilege. Explain why classical direct trap-and-emulate fails and give two remedy families.

### Exercise 2

Design the state transition for an intercepted virtual control-register write whose bits 0–2 are writable, bits 3–6 are read-only zero and bit 7 must raise a guest protection fault when set.

### Exercise 3

A handler successfully performs an MMIO write but resumes at the faulting PC. State the failure, likely symptom and invariant that would have prevented it.

### Exercise 4

Exit measurements show $600{,}000$ port-I/O exits/s at $0.8\ \mu s$, $50{,}000$ MMIO exits/s at $4\ \mu s$, and $20{,}000$ other exits/s at $2\ \mu s$. Compute $U_e$ and identify the first optimization question.

### Exercise 5

Propose a minimum migration checkpoint for a vCPU stopped after an MMIO exit whose userspace operation has returned data but whose interface completes the instruction only on re-entry.

## Answers to the Exercises

### Answer 1

The instruction is behavior-sensitive because it reveals protected configuration, but it is not privileged under the hypothesis. Therefore $S\nsubseteq P$, and running the guest without monitor privilege does not intercept the disclosure. Classical direct trap-and-emulate cannot preserve the virtual interrupt view.

One remedy is binary translation or interpretation that replaces the instruction with a monitor-controlled operation. Another is paravirtualization that changes the guest to query a virtual interface. An architectural interception control would be a third family, but belongs to hardware assistance.

### Answer 2

Capture the saved guest PC, mode and operand. If bit 7 is one, inject the specified guest protection fault, retain the same faulting PC and commit no register effect. Otherwise compute `new = operand & 0b00000111`, store it as the guest-visible shadow, derive any safe effective host controls, and retire by advancing the PC exactly once. Reads return the defined shadow with bits 3–6 and 7 zero. Concurrency must serialize dependent reads and control changes around the commit.

### Answer 3

The completed device transition will execute again after resume, producing a duplicate write or an endless exit loop. The handler confused a completed trap-like operation with a retryable fault. The retirement obligation prevents this: device state, completion marker and resume PC must commit as one logical transition, so an operation either has no side effect and retries or has one side effect and advances.

### Answer 4

The exit utilization estimate is

$$
U_e=(600{,}000)(0.8\times10^{-6})+(50{,}000)(4\times10^{-6})+(20{,}000)(2\times10^{-6})=0.72.
$$

The first question is whether the byte-oriented port interface can be batched or replaced, because it contributes $0.48$ of the utilization. Optimizing only its handler constant may help, but reducing its exit rate attacks the largest term. Validate the estimate with reason-specific distributions, CPU capacity, contention and host scheduling.

### Answer 5

Do not serialize the visible register file immediately. Re-enter in a mode that completes the pending MMIO operation without admitting a subsequent guest instruction, as required by the execution interface. Then checkpoint the post-instruction PC and registers, device read side effects, returned value, interrupt-controller state, virtual time, pending events and relevant memory generation together.

If the interface instead offers a durable pending-operation representation, that representation and the device's matching transaction identity may be serialized, but source and destination must share the exact completion protocol. The checkpoint must describe either the coherent pre-operation state or coherent post-operation state, never a mixture.
