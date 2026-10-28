---
module_id: CA-017
program: Computer Architecture
level: 1
module_number: 17
title: Exceptions, Interrupts, and Privilege
status: complete
last_verified: 2026-09-04
---

# Exceptions, Interrupts, and Privilege

## One-Page Review

### Governing question

How does a processor transfer control across exceptional and asynchronous events while preserving precise architectural state, enforcing privilege, selecting the correct handler, and enabling safe restart or termination?

### Essential definitions

- An **exception** is a synchronous architectural event attributable to the current instruction or its execution context.
- An **interrupt** is an asynchronously requested event accepted at an architecture-defined instruction boundary.
- A **trap** is a control transfer to privileged handling state caused by an exception or interrupt.
- **privilege mode** determines which instructions, registers, memory and resources code may access.
- A **precise trap** exposes state equivalent to all older instructions having completed and no younger instruction having completed, with the faulting instruction treated exactly as specified.
- A **trap cause** identifies the event class; **trap value** can record an address, instruction or other event-specific datum.
- A **saved PC** records the restart, faulting or continuation address defined for the event.
- A **trap vector** determines the handler entry address, directly or through a vectored offset.
- **pending** means an interrupt source has requested service; **enabled** means policy allows its acceptance.
- **interrupt priority** orders simultaneously eligible events; **delegation** assigns handling responsibility to another privilege level.
- A **non-maskable interrupt** is an urgent event not controlled by ordinary interrupt-enable rules, though its exact semantics remain architecture-specific.
- **nested handling** permits a handler to accept another eligible event before returning.
- A **trap return** restores saved privilege/status and selects a saved resume address.
- A **system call** is a deliberate synchronous exception used to request privileged service.
- A **machine-check** or fatal exception reports severe hardware or system failure with architecture/platform-specific recoverability.

### Central model, mechanism, or theorem

At an architectural boundary, select the highest-priority eligible event `e` under mode, delegation, pending and enable state. Trap entry is a state transition

`S' = EnterTrap(S, e)`

that records cause/value and an event-defined saved PC, saves prior privilege/enable state, enters the target privilege, applies interrupt-masking rules and sets `PC=Vector(e)`. Precision requires the visible ordinary-instruction prefix to match the ISA. Trap return validates saved state and produces `S'' = ReturnTrap(S')`; it does not merely jump to an address.

### Critical invariants

- Every exception and interrupt has an exact cause, priority, delegation and handler-target rule.
- Saved PC semantics distinguish retry, skip, continuation and asynchronous boundary cases.
- Faulting instructions commit ordinary effects only when the ISA explicitly permits partial progress.
- Older effects are visible and younger speculative effects are absent at a precise trap boundary.
- Privilege checks precede unauthorized architectural reads, writes or control effects.
- Pending, enable and priority state cannot lose or invent interrupt requests outside specified behavior.
- Nested handlers preserve a stack of return state or otherwise enforce non-overwrite rules.
- Trap return restores only validated privilege, status and PC values permitted by the architecture.

### Common failures

Frequent failures are using exception and interrupt as synonyms, saving the next PC for a retrying fault, saving the faulting PC for an already completed system call without adjustment, writing an ordinary destination before a precise fault, accepting an interrupt halfway through an architectural instruction, confusing pending with enabled, assuming numeric cause order equals priority, delegating an event while retaining the wrong vector/status bank, reenabling interrupts before return state is protected, returning with an ordinary indirect jump, trusting user-written privileged status, losing a level during nesting, and treating a green handler test as proof of out-of-order rollback.

### Compact example

User execution encounters an illegal instruction at PC `0x0104`. A precise trap records cause `illegal_instruction`, saved PC `0x0104`, previous mode `user`, disables ordinary interrupts, enters supervisor mode and selects handler `0x0800`. The handler may emulate or reject the instruction; if policy skips it, it advances saved PC to `0x0108` before trap return. A timer interrupt accepted at boundary `0x0108` saves that continuation address without advancing it and enters its selected handler.

### Connections

Traps connect control flow, ISA semantics, pipelines, operating systems, virtual memory, devices, timers, virtualization, debugging, safety, security and formal refinement.

## Governing Question

Normal instruction execution assumes the next transition follows the program. Exceptions and interrupts deliberately break that flow to report faults, request services or respond to external events. The transfer must be deterministic enough for system software to recover.

The governing question is which architectural prefix has completed and which state the handler owns. Modern processors execute speculatively and devices signal asynchronously, but software needs a precise, privilege-safe boundary.

## Why This Matters

Without precise exceptions, an OS cannot retry a page fault, emulate an instruction or terminate a process without uncertain side effects. Incorrect interrupt masking can lose events or livelock. Incorrect privilege restoration can hand supervisor authority to user code.

Trap latency affects real-time response, but functional correctness is separate from timing bounds. A conforming design may take varying cycles while still exposing the same saved state; a safety system may additionally require bounded latency and fault containment.

Verification spans decode, retirement, control/status registers, translation, interrupt controller, firmware and OS entry code. Testing handlers alone does not establish instruction rollback or privilege noninterference.

## Prerequisites and Retrieval

Before studying this module, be able to:

- model instructions as architectural state transitions;
- distinguish sequential, branch, call and return control flow;
- explain privilege and virtual memory conceptually;
- distinguish architectural commit from speculative execution;
- reason about priority and masked event selection.

Retrieve ISA/privileged-spec version; privilege modes; exception/interrupt cause tables; cause priority; saved-PC rules; trap-value rules; vector modes and alignment; delegation; pending/enable bits; global and per-source masks; non-maskable events; trap-entry status transformations; return instructions; system-call convention; page/access fault distinctions; debug entry; reset; virtualization intercepts; interrupt-controller interface; timer/device semantics; nesting policy; OS entry/exit code; executable model; RTL retirement/trap logic; formal properties; architecture tests; latency measurements; fault injection; silicon errata; and exact firmware/software/hardware revisions.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish synchronous exceptions, asynchronous interrupts and the general trap mechanism;
2. specify precise trap state and instruction-prefix semantics;
3. derive saved PC, cause, trap value and vector target for an event;
4. reason about pending, enabling, masking, priority and delegation;
5. analyze nested handling and trap-return state;
6. explain system calls, page faults, access faults and machine checks;
7. connect out-of-order retirement and speculation recovery to precise traps;
8. distinguish guest, hypervisor, debug and physical interrupt boundaries;
9. design functional, timing, security and fault-injection evidence;
10. govern compatible exception behavior and errata over a system lifecycle.

## Core Exposition

### Classify events by synchrony

An exception is caused by or attributed to the current instruction: illegal encoding, arithmetic condition, alignment, translation, permission, breakpoint or explicit environment call. Repeating the same state usually reproduces it.

An interrupt originates independently, such as a timer or device request, and is accepted between architectural instructions. Its arrival time need not align with execution stages.

### Use trap as the common transition

Both classes can reuse handler-vector, cause, status and return machinery. A cause encoding commonly includes an interrupt/exception discriminator.

Shared mechanism does not erase semantic differences. Saved PC, priority, maskability and retry policy can differ.

### Define precise architectural state

A precise trap exposes an instruction prefix. All instructions older than the boundary have their permitted effects; no younger instruction has architectural effects.

For a faulting instruction, specify whether it is absent from the prefix, completed before a post-instruction trap, or partially progressed under an explicit restart model.

### Save the correct PC

Restartable faults commonly save the faulting instruction address. Asynchronous interrupts commonly save the next instruction boundary to resume.

System calls may save their own address while software advances it, or save continuation directly. Handlers must follow the actual architecture rather than a mnemonic-based assumption.

### Record cause and auxiliary value

Cause identifies the event class. Auxiliary trap state can record a faulting virtual address, instruction bits, access details or zero.

Define validity per cause. Software must not consume stale trap-value bits for an event that does not populate them.

### Select a vector

A direct vector mode sends events to one base; software dispatches from cause. A vectored mode adds a cause-dependent offset for selected event classes.

Vector base alignment, privilege bank and mode bits are architectural. The target must itself pass the applicable fetch and protection rules.

### Define exception priority

One instruction can encounter multiple potential failures: illegal operation, misalignment, translation and access permission. The architecture constrains which cause is reported.

Hardware may check in parallel but must select a permitted cause. Tests should deliberately construct overlapping failures.

### Track interrupt pending state

A pending bit or controller state records an outstanding request. Level-triggered sources remain asserted until the device condition is cleared; edge-triggered sources require captured events.

Acknowledgment order matters. Clearing the CPU pending view before servicing the device can immediately reassert or lose a pulse depending on platform semantics.

### Apply enables and masks

Eligibility can depend on global enable, per-source enable, current privilege, delegation and controller masks. Pending does not imply immediately accepted.

Trap entry often disables or saves a global enable to prevent uncontrolled nesting. Software deliberately reenables when its frame is safe.

### Resolve priority

When several eligible interrupts are pending, an architecture/controller priority rule selects one. Numeric cause value need not define that order.

Priority can be fixed, programmable or threshold-based. Starvation and real-time requirements need evidence beyond functional selection.

### Delegate handling

Delegation routes selected events to a lower privileged supervisor rather than the highest mode. It changes target mode, vector and status/cause banks.

Delegation is constrained by current mode and security policy. It must not let less-privileged software capture events that require a more trusted handler.

### Enter privilege safely

Trap entry saves previous privilege/status in protected architectural state, sets target mode, updates interrupt-enable stacking and selects handler PC.

These changes form one architectural transition. A handler must not run with partially updated authority or an attacker-controlled vector.

### Build an entry frame

Hardware usually saves a minimal architectural set; software saves general registers and establishes a kernel stack. Exact ownership divides between ISA and ABI/OS.

Entry code cannot assume user stack safety. It selects trusted stack/context before storing privileged data.

### Handle nested traps

Before reenabling eligible events, a handler preserves cause, saved PC and status that another trap could overwrite. Software frames or banked registers provide nesting depth.

Define maximum depth, priorities and emergency paths. Unbounded nesting can exhaust trusted stack and destroy recoverability.

### Return with a privileged instruction

Trap return reads protected saved state, restores privilege/enable fields under validation and selects resume PC. It can also change translation behavior when returning to a different context.

An ordinary indirect jump cannot safely perform these status changes. Return instructions must reject or mask invalid saved combinations.

### Handle illegal instructions

Illegal/unsupported encodings trap without ordinary instruction effects. A handler can terminate, emulate or enable a feature under controlled policy.

Emulation must reproduce exact operands, exceptions and PC behavior. It must avoid repeatedly trapping on the same instruction unless retry is intended.

### Implement system calls

An environment-call instruction intentionally enters privileged software with a designated cause. A separate syscall ABI supplies number, arguments, results and errors.

The kernel validates every user pointer and value. Privilege entry authenticates the boundary, not the contents of untrusted registers.

### Distinguish page and access faults

Page faults arise from translation validity or page-level permissions; access faults can report physical protection, bus or implementation/platform access failure. Exact taxonomy is ISA-specific.

Handlers use the distinction to allocate/map pages, signal processes or diagnose hardware. Collapsing causes can break recovery policy.

### Preserve store precision

A faulting store must not leave unauthorized or partial ordinary memory effects unless the architecture explicitly permits them. Store buffers delay visibility until safety is established.

Multi-beat or vector stores require defined partial-progress semantics. Restart information must prevent duplicate or skipped writes.

### Preserve load precision

A faulting load normally suppresses its destination update. Speculative data may exist internally but cannot become architectural.

Fault-suppression or first-fault vector operations are special semantics with explicit masks/progress state, not ordinary imprecision.

### Retire in order

Out-of-order cores execute younger instructions before an older fault resolves. A reorder/retirement structure commits in order and chooses the oldest reportable exception.

On a trap, younger rename, queue and store state is squashed or made unreachable. Committed prefix and saved PC must match the ISA.

### Accept interrupts at boundaries

An interrupt can arrive during a long pipeline operation, but architectural acceptance occurs at a permitted boundary. The implementation may finish, abort or checkpoint internally.

Long or restartable instructions need explicit interruptibility. Timing requirements can force checkpoints without weakening functional precision.

### Treat non-maskable events explicitly

NMI-like events serve urgent failures but are not universally unstoppable or nestable. Define state save, vector, priority and behavior if they arrive during another critical event.

If normal trap state could be overwritten, provide separate banked state or an emergency protocol. Otherwise diagnosis itself destroys the original fault.

### Handle machine checks

Machine checks report parity/ECC, bus, cache, internal or platform failures. Some are corrected, recoverable, contained or fatal.

State validity must be classified. A precise-looking PC is insufficient if register or memory integrity is unknown.

### Integrate virtual memory

Instruction fetch, load and store translations can fault with distinct access types and virtual addresses. Privilege mode and status influence permission checks.

Trap entry may switch address-space context or use protected translation mappings. Entry code and vector pages must remain reachable under the defined transition.

### Virtualize traps

Hypervisors decide which guest events execute natively, are injected, delegated or intercepted. Two-stage translation adds guest-physical and host-physical fault information.

Virtual interrupt controllers preserve pending/enable/priority semantics for guests while isolating physical sources. Migration must serialize complete virtual event state.

### Distinguish debug entry

Debug halt, breakpoint and single-step can use trap-like state but may enter a separate debug mode and register bank. Debuggers need an architectural boundary.

Production access control must protect debug entry. A debug mechanism that bypasses privilege is a security authority, not a harmless observability feature.

### Define reset separately

Reset selects an initial privilege, PC and control-state baseline. It is not necessarily a precise trap from the prior instruction stream.

Warm reset, core-local reset and system reset can preserve different memory/device state. Boot software relies on the exact reset contract.

### Analyze interrupt latency

Latency spans source assertion, controller routing, eligibility, boundary acceptance, pipeline recovery, vector fetch and software prologue. Report distributions and worst-case assumptions.

Functional conformance does not prove deadlines. Real-time assurance includes masking intervals, contention, caches, nesting and long instructions.

### Avoid priority inversion and starvation

Long masking or low-priority handlers holding required resources can delay urgent service. Threshold and preemption policies mitigate some cases.

Measure under adversarial interrupt load and memory contention. A priority register setting alone is not latency evidence.

### Protect against confused deputies

System calls and faults transfer untrusted state into privileged handlers. Validate causes, pointers, lengths, identities and authorization before acting.

Clear sensitive temporary state on domain transitions as required. Speculative handler access can also expose secrets across privilege boundaries.

### Verify trap entry and exit

Generate every cause in every relevant mode, with enabled/disabled/delegated combinations and overlapping candidates. Check cause, value, saved PC, status, vector and frame conditions.

Return using valid and adversarial saved state. Compare an independent model with RTL retirement/trap traces and OS-observed frames.

### Inject asynchronous events

Vary interrupt arrival relative to fetch, execution, load/store completion and retirement. The accepted architectural boundary must always form a permitted prefix.

Test repeated levels, narrow pulses, simultaneous priorities, nested service and acknowledgment races. Include virtual and physical controller state.

### Inject hardware faults

Exercise parity/ECC, bus errors, corrupted control state, vector fetch failure and double-fault paths. Confirm containment, logging and safe-state behavior.

Do not label a synthetic cause-register write as equivalent to a physical fault unless the injection reaches the same detection and containment path.

### Govern lifecycle behavior

Bind privileged specification, platform interrupt architecture, firmware, OS, hypervisor, executable model, RTL, configuration and silicon revision. Preserve traces and failing event timing.

Track errata for lost interrupts, wrong saved PCs, incorrect priority or incomplete rollback. Mitigations remain explicit and revision-scoped.

## Definitions and Notation

- `S`: complete architectural pre-state at an instruction boundary.
- `e`: selected exception or interrupt event.
- `eligible(e,S)`: pending, enabled, delegated and mode-permitted event predicate.
- `priority(e)`: architecture/platform event ordering rule.
- `Cause(e)`: architectural cause encoding.
- `TVal(e)`: event-specific auxiliary trap value.
- `EPC(e,S)`: saved PC selected for event and boundary.
- `Vector(e,S)`: handler entry address.
- `Mode`: current architectural privilege mode.
- `PrevMode`: protected saved prior privilege.
- `IE`: current interrupt-enable state.
- `PIE`: protected saved prior interrupt-enable state.
- `EnterTrap(S,e)`: architectural trap-entry transition.
- `ReturnTrap(S)`: validated trap-return transition.
- `commit_prefix`: sequence of ordinary instructions visible before the trap.

Addresses are byte addresses. Event names in examples are conceptual; real cause encodings are ISA-specific.

## Mechanisms, Invariants, or Proof Structure

1. **Classification obligation:** prove every event is classified as synchronous/asynchronous, maskable/non-maskable and restart/continuation as specified.
2. **Prefix obligation:** prove trap state corresponds to the exact permitted committed instruction prefix.
3. **Cause obligation:** prove selected cause and auxiliary value match event type and exception priority.
4. **PC obligation:** prove saved PC denotes faulting, retry or continuation address exactly as required.
5. **Vector obligation:** prove mode, delegation, base, vector offset and alignment select the permitted handler.
6. **Status obligation:** prove prior mode/enable are protected and new privilege/mask state is atomically established.
7. **Effect obligation:** prove faulting and younger ordinary register/memory effects are suppressed or partial only as specified.
8. **Interrupt obligation:** prove pending, enable, priority, threshold and acknowledgment cannot lose or invent events.
9. **Nesting obligation:** prove nested entry cannot overwrite live return state or exceed defined emergency handling.
10. **Return obligation:** prove only validated saved privilege/status/PC are restored by the correct privileged instruction.
11. **Translation obligation:** prove fetch/load/store and multi-stage fault types, addresses and access permissions are correct.
12. **Virtualization obligation:** prove guest/host interception, injection and migration preserve virtual trap state and isolation.
13. **Timing obligation:** prove claimed latency bounds include masking, contention, recovery, vector fetch and prologue assumptions.
14. **Fault obligation:** prove hardware-error injection exercises actual detection, containment, logging and safe-state paths.
15. **Evidence obligation:** bind specs, platform, firmware, OS, hypervisor, model, RTL, configuration, hardware and errata versions.

## Alternatives and Trade-Offs

1. **Direct versus vectored entry:** direct entry centralizes dispatch; vectors reduce dispatch latency.
2. **Few versus rich causes:** few causes simplify hardware; rich causes improve diagnosis and recovery.
3. **Faulting versus continuation saved PC:** retry supports repair; continuation suits completed requests.
4. **Hardware versus software state save:** hardware speeds predictable entry; software saves only needed state flexibly.
5. **Global versus per-source masks:** global masks are fast; fine masks improve responsiveness control.
6. **Fixed versus programmable priority:** fixed order is analyzable; programmability adapts workloads.
7. **No nesting versus nested handlers:** no nesting simplifies state; nesting reduces urgent latency.
8. **Highest-mode versus delegated handling:** central handling maximizes control; delegation reduces overhead.
9. **Level versus edge interrupts:** levels tolerate delayed service; edges represent events but require reliable capture.
10. **Precise all-or-none versus restartable partial progress:** precision simplifies software; partial progress supports long operations.
11. **Finish versus abort long instructions:** finishing simplifies restart; abort/checkpoint can reduce latency.
12. **Physical versus virtual interrupt delivery:** direct physical delivery is fast; virtualization provides isolation/mobility.
13. **Unified versus separate debug entry:** unified traps reuse machinery; separate debug state protects observability workflows.
14. **Recovery versus fail-stop machine checks:** recovery preserves service; fail-stop limits uncertain-state propagation.
15. **Low latency versus speculative restraint:** aggressive prediction speeds entry; restraint reduces privilege side channels.

## Failure Modes and Misconceptions

1. “Exception and interrupt are synonyms.” Their synchrony and acceptance rules differ.
2. “Trap means an unrecoverable failure.” System calls and restartable page faults are traps.
3. “Precise means the handler runs immediately.” It describes visible state, not latency.
4. “The saved PC is always the next instruction.” Retry faults commonly save the faulting PC.
5. “The saved PC is always the faulting instruction.” Interrupts commonly save a continuation boundary.
6. “A faulting destination may be written before the handler fixes it.” Precise rules usually suppress it.
7. “Younger execution cannot occur before an older fault.” It can execute speculatively but cannot commit.
8. “Pending means enabled.” Masks and privilege can defer acceptance.
9. “Disabled interrupts disappear.” Pending semantics determine whether they remain recorded.
10. “Cause number defines priority.” Priority can use another ordering.
11. “Vectoring removes software dispatch entirely.” Causes, sharing and platform routing can still require it.
12. “Delegation only changes the handler address.” It changes privilege and state banks too.
13. “Trap entry saves all registers.” Hardware often saves only minimal control state.
14. “A user stack is safe for privileged entry.” It is untrusted and may be unmapped.
15. “Reenabling interrupts early is always faster and safe.” Return state must first be nest-safe.
16. “An ordinary jump can return from a trap.” Privilege/status restoration needs trap-return semantics.
17. “Illegal-instruction emulation can merely advance PC.” It must reproduce semantics/exceptions or reject.
18. “System-call entry validates its arguments.” The privileged handler must validate them.
19. “All memory failures are page faults.” Access, alignment, bus and capability causes differ.
20. “Unaligned or vector partial stores can always be retried wholesale.” Partial-progress rules may forbid duplication.
21. “Interrupt controllers are outside architectural evidence.” Delivery semantics span CPU and platform.
22. “NMI cannot ever be delayed or nested.” Exact architecture/platform rules vary.
23. “Machine-check saved PC proves recoverable state.” Data/control integrity may be uncertain.
24. “Guest interrupts are just host interrupts with another number.” Injection and virtual state need isolation.
25. “Functional trap tests prove real-time response.” Latency needs separate bounded evidence.
26. “Synthetic cause writes equal physical fault injection.” They may bypass detection and containment.

## Worked Examples

### Example 1

An illegal instruction at user PC `0x0104` saves `0x0104`, records cause, suppresses ordinary writes and enters supervisor vector `0x0800`.

### Example 2

If a handler emulates/skips a four-byte illegal instruction, it writes saved PC `0x0108` before trap return; retry without adjustment would trap again.

### Example 3

A timer interrupt accepted between instructions at continuation PC `0x0108` saves `0x0108`; return resumes the interrupted next instruction.

### Example 4

Pending timer with global enable false is not eligible, but it need not be discarded; it can be accepted after enable becomes true.

### Example 5

Simultaneous external and timer requests use the specified priority/threshold rule, not whichever signal arrives first at one internal gate.

### Example 6

A delegated page fault enters supervisor state and supervisor vector; a nondelegated machine check enters the higher protected mode and its bank.

### Example 7

An out-of-order core detects a younger divide fault but first retires an older load; if the load faults too, the oldest architectural exception wins.

### Example 8

A faulting store buffered speculatively is removed before visibility, preserving the precise prefix and unauthorized-memory invariant.

### Example 9

A nested external interrupt must save the first handler’s EPC/cause/status before shared control registers are overwritten.

### Example 10

A guest page fault and a host second-stage translation fault carry different addresses and ownership; the hypervisor must inject or handle the correct event.

## Cross-Program Connections

- **ISA semantics:** exceptions are alternative state transitions of instructions.
- **Control flow:** vectors and trap return select protected successors.
- **Pipelines:** retirement, rollback and store buffering create precise prefixes.
- **Operating systems:** handlers implement syscalls, faults, scheduling and signals.
- **Virtual memory:** translation and protection faults carry access-specific state.
- **Devices:** controllers, timers, levels, edges and acknowledgment produce interrupts.
- **Virtualization:** intercept and injection reproduce guest event state.
- **Security:** privilege entry, validation and speculative isolation protect domains.
- **Safety:** machine checks, latency, containment and fault injection support assurance.
- **Formal methods:** event selection and state transitions support refinement proofs.

## References

1. RISC-V International, [Privileged Architecture](https://docs.riscv.org/reference/isa/priv/priv-index.html), privilege modes, CSRs, traps, delegation, interrupts, translation and return; retrieved 2026-09-04.
2. RISC-V International, [RV32I Base Integer Instruction Set](https://docs.riscv.org/reference/isa/unpriv/rv32.html), illegal instructions, environment calls, alignment and base exception behavior; retrieved 2026-09-04.
3. Arm, [Arm Architecture Reference Manual for A-profile Architecture](https://developer.arm.com/documentation/ddi0487/latest/), exception levels, synchronous exceptions, interrupts, vectors and exception return; retrieved 2026-09-04.
4. Intel, [Intel 64 and IA-32 Architectures Software Developer's Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), interrupts, exceptions, privilege, task state and system programming; retrieved 2026-09-04.
5. RISC-V International, [Sail RISC-V Model](https://github.com/riscv/sail-riscv), executable privileged and trap semantics for differential/refinement evidence; retrieved 2026-09-04.
6. lowRISC, [Ibex Exceptions and Interrupts](https://ibex-core.readthedocs.io/en/latest/03_reference/exception_interrupts.html), concrete core exception/interrupt behavior, priority and NMI handling; retrieved 2026-09-04.
7. Linux Kernel, [x86-64 Entry and Exit](https://docs.kernel.org/arch/x86/entry_64.html), kernel entry paths and state-transition concerns; retrieved 2026-09-04.
8. WebAssembly Community Group, [Traps](https://webassembly.github.io/spec/core/exec/runtime.html#traps), synchronous trap semantics in a sandboxed virtual instruction environment; retrieved 2026-09-04.

## Exercises

### Exercise 1

Specify trap-entry and return transitions for illegal instruction, page fault, system call, timer interrupt and non-maskable machine event.

### Exercise 2

Trace an illegal-instruction trap that skips one four-byte instruction, then a timer interrupt at the resumed boundary, including mode, saved PC and enable state.

### Exercise 3

Design tests for exception priority when one instruction is simultaneously illegal, misaligned and directed at inaccessible memory.

### Exercise 4

Construct a precise-trap verification plan for an out-of-order core with speculative loads, buffered stores and vectored interrupts.

### Exercise 5

Construct assurance for virtualized interrupt delivery in a safety-relevant system, including latency, nesting, migration and fault injection.

## Answers to the Exercises

### Answer 1

Illegal instruction and page fault save the faulting PC for retry/emulation, record their specific cause/value, suppress ordinary effects and enter the selected privilege/vector. A system call records its designated cause and follows the ISA’s saved-PC rule; the syscall ABI and handler determine result and continuation.

A timer interrupt is accepted at a permitted boundary, saves the continuation PC and previous mode/enable, masks according to entry rules and vectors. A non-maskable machine event uses its separate priority/vector/save policy and may declare state unrecoverable. Trap return validates and restores saved mode/status/PC; handlers adjust EPC only when their completion policy requires it.

### Answer 2

The toy state machine distinguishes a retry-address exception from an asynchronous continuation boundary.

<!-- bijux-verify: {"id":"trap-entry-return-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"exception cause=illegal_instruction from_mode=user saved_pc=0x0104 handler_pc=0x0800 mode=supervisor interrupts=false\nreturn resume_pc=0x0108 mode=user interrupts=true\ninterrupt cause=timer from_mode=user saved_pc=0x0108 handler_pc=0x0820 mode=supervisor interrupts=false\nreturn resume_pc=0x0108 mode=user interrupts=true\n"}} -->
```python
state = {"pc": 0x104, "mode": "user", "interrupts": True}


def enter(kind, cause, handler):
    saved = state["pc"]
    previous = state["mode"]
    state.update({"saved_pc": saved, "previous_mode": previous})
    state.update({"pc": handler, "mode": "supervisor", "interrupts": False})
    print(
        f"{kind} cause={cause} from_mode={previous} saved_pc=0x{saved:04x} "
        f"handler_pc=0x{handler:04x} mode={state['mode']} "
        f"interrupts={str(state['interrupts']).lower()}"
    )


def trap_return():
    state["pc"] = state["saved_pc"]
    state["mode"] = state["previous_mode"]
    state["interrupts"] = True
    print(
        f"return resume_pc=0x{state['pc']:04x} mode={state['mode']} "
        f"interrupts={str(state['interrupts']).lower()}"
    )


enter("exception", "illegal_instruction", 0x800)
state["saved_pc"] += 4
trap_return()
enter("interrupt", "timer", 0x820)
trap_return()
```

The trace establishes four toy control-state transitions only. It provides no real cause encoding, priority, delegation, pipeline, interrupt-controller, timing or hardware evidence.

### Answer 3

First extract the normative priority table; do not assume a desirable order. Create raw encodings and addresses where multiple checks could fail, then vary mode, translation state and alignment independently. Observe cause, trap value, saved PC and absence of ordinary writes.

Compare an independent executable model and RTL/processor commit trace. Add cases whose instruction fetch itself faults, because decode may not legally occur. Bind the result to the exact ISA mode/profile; another architecture may intentionally report a different cause.

### Answer 4

Tag every in-flight instruction with program order. Assert that retirement commits in order, reports the oldest eligible synchronous exception, and blocks all younger architectural register/store effects. Exercise faults discovered at decode, execute, translation, cache refill and store completion.

Inject interrupts at every cycle around retirement, branch recovery and long operations; compare the selected boundary with an independent sequential model. Check rename-map restoration, queue flushing, store-buffer cancellation, precise cause/value/EPC, vector and return. Include simultaneous exception/interrupt priority, nested traps and wrong-path faults. Preserve traces, seeds, RTL/configuration and proof assumptions.

### Answer 5

Define physical and virtual controller models, ownership, pending/enable/priority/threshold state, injection, acknowledgment, delegation, guest/host vectors and migration serialization. Specify maximum latency under masking, contention, nesting and hypervisor scheduling.

Test simultaneous sources, level/edge behavior, guest masking, host interception, migration with pending events, controller reset and malicious guests. Inject transport, controller, memory and CPU faults through real detection paths and verify containment/safe state. Compare model, hypervisor, guest and hardware traces. Named platform, ISA, hypervisor, OS, real-time, RTL, safety, security, verification and independent-assurance authorities review their scopes. This module supplies no certification.
