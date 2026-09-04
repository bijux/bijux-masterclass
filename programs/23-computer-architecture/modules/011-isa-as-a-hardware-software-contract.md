---
module_id: CA-011
program: Computer Architecture
level: 1
module_number: 11
title: ISA as a Hardware-Software Contract
status: complete
last_verified: 2026-09-04
---

# ISA as a Hardware-Software Contract

## One-Page Review

### Governing question

What must an instruction-set architecture specify so independently developed processors, compilers, operating systems, debuggers and programs agree on machine behavior while implementations remain free to differ internally?

### Essential definitions

- An **instruction-set architecture**, or ISA, specifies software-visible machine state, instructions and their permitted effects.
- **architectural state** is state whose values or effects are defined for software observation, such as registers, memory, privilege and status.
- **microarchitectural state** implements the ISA but is not ordinarily part of its functional contract, such as pipeline queues or predictor entries.
- An **instruction encoding** maps bit patterns to operations and operands; **instruction semantics** defines the associated state transition.
- An **instruction-set extension** adds or refines named capabilities under compatibility and discovery rules.
- A **privilege architecture** defines execution modes, protected state, traps and control over resources.
- An **exception** is a synchronous architectural event caused by the current instruction; an **interrupt** is an asynchronous event accepted at a defined boundary.
- A **memory consistency model** constrains the order in which memory operations may be observed across execution agents.
- An **ABI** defines calling conventions, object layout, system-call interfaces and binary conventions layered on an ISA.
- An **execution environment** supplies services and policies, such as address spaces, devices and process lifecycle, not fully determined by the ISA.
- **reserved** encodings are held for future or constrained use; **illegal** encodings trigger specified unsupported-instruction behavior.
- **architectural compatibility** means required software-visible behaviors remain valid for the declared ISA/profile/version.

### Central model, mechanism, or theorem

Model an ISA as a labeled transition relation

`S --I--> S'` or `S_(n+1) = Exec_ISA(S_n, instruction, environment_event)`.

`S` includes every architectural value relevant to the instruction: PC, registers, memory and required status/privilege. The ISA defines legal preconditions, next-state effects, traps and nondeterministic choices. A processor is functionally conformant when every committed architectural trace it produces is permitted by the ISA for the same inputs and environment. Internal execution may be pipelined, speculative or out of order, provided committed observations refine the architectural relation.

### Critical invariants

- Architectural state and observation boundaries are complete enough to distinguish every software-visible outcome.
- Each legal encoding has defined operands, state effects, PC behavior and exception conditions.
- Reserved and illegal encodings cannot silently acquire implementation-specific privileged side effects.
- Loads, stores, atomics and fences obey width, alignment, address translation and memory-order rules.
- Exceptions and interrupts expose a precise or explicitly defined architectural state and restart point.
- Optional extensions and profiles have reliable discovery, dependency and illegal-use behavior.
- ABI, platform, firmware and OS assumptions are never attributed to the base ISA without specification.
- Conformance evidence covers exact ISA/profile/version and does not substitute tests for missing specification.

### Common failures

Frequent failures are calling assembly syntax the ISA, equating one microarchitecture with the contract, assuming instruction count predicts performance, treating unspecified behavior as implementation freedom without limits, decoding reserved encodings as no-ops, assuming every register is general purpose, mixing ABI register roles into architectural semantics, omitting memory ordering, treating a page fault as a load result, making interrupts visible halfway through an architectural instruction, enabling extensions without discovery, relying on a simulator that shares the same semantic bug, and declaring test-suite success full conformance.

### Compact example

A three-instruction abstract program executes `addi x1,x0,5`, `addi x2,x1,-2`, and `add x3,x1,x2`. Starting with `PC=0` and `x0=0`, its architectural trace commits `x1=5` at PC 0, `x2=3` at PC 4, and `x3=8` at PC 8, ending with PC 12 and `x0=0`. A single-cycle core, multicycle core and out-of-order core may take different internal steps and wall time; conformant commit traces agree on these architectural transitions.

### Connections

ISA contracts connect processor datapaths, compilers, ABIs, operating systems, virtual machines, memory models, exceptions, debuggers, formal semantics, compatibility, performance and security.

## Governing Question

Software needs a stable machine model. Hardware designers need freedom to pipeline, cache, predict and specialize. The ISA is the boundary that lets both evolve: it specifies what must be observed while leaving most details of how it is achieved open.

The governing question is what belongs in that boundary. Registers and instruction effects clearly do. Memory ordering, traps, privilege, optional features and self-modifying code also affect programs. Cache size and branch-predictor design normally do not, except through separately specified timing or security properties.

## Why This Matters

An incomplete ISA forces software to depend on accidents. If misaligned access behavior is unclear, binaries fail across processors. If extension discovery is unreliable, a legal instruction on one core traps on another. If exception state is imprecise, an OS cannot safely restart a faulting instruction.

ISA stability enables long-lived binaries and diverse implementations. It also constrains future design: encoding space, register semantics and ordering guarantees become compatibility obligations.

Conformance is more than getting arithmetic examples right. It covers all encodings, privilege checks, exceptional operands, memory interactions and permitted nondeterminism. Tests, formal models and differential execution support different pieces of evidence.

## Prerequisites and Retrieval

Before studying this module, be able to:

- distinguish values, encodings and architectural state;
- trace a simple processor datapath from instruction to commit;
- explain registers, memory, PC and exceptions conceptually;
- distinguish sequential program order from hardware timing;
- reason about a state-transition system.

Retrieve ISA name, edition, base and extensions; profiles; instruction lengths and byte order; register/state inventory; encodings; pseudocode or formal semantics; address and data widths; memory operations and consistency model; alignment; atomicity; privilege modes; trap causes and restart rules; reset state; extension discovery; reserved behavior; environment interfaces; ABI and platform specifications; errata; implementation deviations; reference model; architecture tests; formal properties; toolchain targets; binaries; trace schema; and exact hardware/simulator versions.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish ISA, microarchitecture, ABI and execution environment;
2. represent instructions as architectural state transitions;
3. identify complete software-visible state and observations;
4. separate encoding, syntax and semantics;
5. explain memory, ordering, exception and privilege contracts;
6. reason about optional extensions and discovery;
7. assess backward/forward compatibility and reserved encodings;
8. compare implementations by commit-level refinement;
9. design conformance evidence using independent models and tests;
10. identify performance and security properties outside functional ISA semantics.

## Core Exposition

### Define the architectural boundary

List what software can read, write or infer through specified effects: registers, PC, memory, status, privilege, exceptions, counters and device-visible operations where included.

Observation need not mean direct register access. Memory ordering and faults are architectural because programs can distinguish them.

### Separate architecture and implementation

The ISA can say an add reads two registers and writes a result. It need not say whether hardware uses ripple or prefix addition, one pipeline stage or several.

Microarchitectural choices may affect performance, energy and side channels. They remain subject to nonfunctional requirements even when functionally invisible.

### Model architectural state

State includes PC, register files, memory and required control/status. In privileged systems it includes translation, interrupt enables and execution mode.

Avoid including irrelevant internal queues in the ISA model. Include enough environment state to make memory and trap behavior meaningful.

### Define instruction syntax

Assembly mnemonics and operand notation are human/tool interfaces. Aliases can express one encoding in several textual forms.

Syntax is not semantics. `nop` may assemble to an add-immediate with zero effect; disassemblers may choose either spelling.

### Define instruction encoding

Encoding fixes instruction length, opcode/function fields, register indices and immediate placement. Variable-length ISAs add prefix and boundary rules.

Every bit pattern must be legal, reserved, custom or illegal under a defined context. Decoders must not depend on fields that are semantically unused unless allowed.

### Define instruction semantics

Semantics states values read, computation, state written, PC update and exceptions. Pseudocode must define width, overflow, signedness and ordering precisely.

Narrative descriptions and formal models should agree. Ambiguous pseudocode becomes an interoperability defect.

### Define the PC convention

Specify whether the architectural PC denotes the current instruction and how sequential next PC is calculated. Branches, jumps, traps and returns select alternatives.

Compressed or variable-length instructions make fixed `PC+4` assumptions invalid. Alignment faults need explicit rules.

### Define registers

State register count, width, special behaviors and reset or unspecified values. Some registers are constant, paired, banked or privilege-dependent.

ABI names such as stack pointer are software conventions unless the ISA gives them special instruction semantics.

### Define arithmetic behavior

Specify fixed width, wrapping, flags or traps. RISC-V base integer arithmetic wraps without condition-code flags; other ISAs differ.

Floating-point instructions add formats, rounding and accrued exceptions. Vector instructions add lane and mask semantics.

### Define memory address space

Specify address width and the abstraction of memory bytes. Platform documents commonly map RAM and devices; the base ISA defines load/store behavior.

Virtual address translation belongs to privileged architecture where supported. Physical map is a platform property, not universal ISA state.

### Define load and store behavior

Specify access widths, byte order, sign/zero extension, alignment and faults. Partial stores define byte lanes and preserved data.

A store may become architecturally performed before physical persistence. Durability is a separate memory/platform contract unless explicit instructions define it.

### Define memory ordering

Single-thread instruction semantics does not determine what several harts/cores observe. The memory model defines permitted reordering and visibility.

Fences and acquire/release atomics constrain ordering. Compilers map language synchronization to these rules.

### Define atomic operations

Atomic read-modify-write operations appear indivisible at specified granularity and ordering. Load-reserved/store-conditional adds reservation behavior and permitted failure.

Progress guarantees and reservation invalidation need specification. Atomicity does not imply persistence or fairness.

### Define exceptions

Synchronous exceptions include illegal instruction, access fault, misalignment and arithmetic traps where defined. Record cause, faulting address and restart PC under privilege rules.

Normal instruction writes must be suppressed or precisely ordered. A fault is an alternative transition, not a returned data value.

### Define interrupts

Interrupts arise independently of the current instruction and are accepted at architecturally defined boundaries. Priority, masking, delegation and return state belong to privileged architecture.

Microarchitecture can detect early but must present permitted state. Precise acceptance supports OS preemption and recovery.

### Define privilege

Privilege modes restrict instructions and state. Control/status registers configure translation, traps, interrupts and protection.

Access checks are semantic preconditions. An unauthorized operation traps without performing its protected ordinary effect.

### Separate ISA from platform

The ISA may define instruction behavior without fixing boot address, interrupt controller, timer, device map or firmware calls.

Platform profiles and firmware specifications fill those gaps. Software targeting “the ISA” alone may not boot anywhere.

### Separate ISA from ABI

The ABI assigns argument, return, saved, temporary, stack and thread-pointer roles; defines stack alignment and object files; and specifies calls.

Two ABIs can target one ISA. One binary compiled for the wrong ABI can use legal instructions yet communicate incorrectly.

### Separate ISA from OS API

System-call numbers, process semantics, file descriptors and signals are operating-system ABI. The trap instruction is ISA; the service selected by a register value is OS policy.

Bare-metal and hosted programs can share an ISA while using different environments.

### Define optional extensions

Extensions add instructions, registers or semantics. State dependencies and privilege support must be explicit.

Software needs static profiles or runtime discovery. Executing an unsupported extension must have defined illegal-instruction behavior.

### Manage extension composition

Two extensions can compete for encodings or change shared state. Names, versions, prerequisites and conflicts govern legal combinations.

Profiles reduce combinations for ecosystems. A custom opcode remains outside portable software unless coordinated.

### Reserve encoding space

Reserved encodings support future growth. Implementations should produce specified illegal behavior instead of treating them as undocumented aliases.

Software must not rely on current trap behavior if a future standard can assign meaning, unless the compatibility contract preserves it.

### Distinguish unspecified and undefined

Some results permit several values; others are constrained but implementation-selected; some behavior may be illegal. Use the specification's exact vocabulary.

Nondeterminism is not permission for arbitrary side effects. Formal models should enumerate allowed outcomes.

### Define reset and initial state

Reset establishes a privilege mode and PC under ISA/platform rules. Many registers or memory contents can be unspecified until firmware initializes them.

Do not write tests that assume zero where the contract says unknown. Boot software must establish its own invariants.

### Support virtualization

A hypervisor presents virtual architectural state and intercepts selected operations. Guests should observe permitted ISA behavior independent of host microarchitecture.

Timing, counter and device virtualization add separate contracts. Nested privilege and trap delegation must preserve ownership.

### Support debugging

Debug architecture can halt, single-step, inspect registers and control execution. It is privileged state outside ordinary program semantics.

Single-step across exceptions and variable-length instructions needs precise PC behavior. Debug actions can perturb timing.

### Define self-modifying code rules

Instruction fetch and data stores may use distinct caches or visibility paths. The ISA defines fences or synchronization needed before newly written instructions execute.

Writing bytes and branching immediately is not universally sufficient. Compilers, loaders and JITs must follow the contract.

### Define counters and time

Architectural counters may report cycles, retired instructions or time under privilege and filtering rules. Frequency changes complicate the meaning of cycles versus time.

Counters are observations and potential side channels. Access control and virtualization can modify availability.

### Preserve precise commit

An implementation can execute ahead internally but commits instructions in a manner that yields a permitted architectural trace. Squashed speculative work cannot change ordinary architectural state.

Side effects such as cache state may remain microarchitecturally observable and create security concerns outside simple functional equivalence.

### Refine with pipelines

Several instructions occupy internal stages simultaneously. Hazards, stalls and forwarding alter cycles, not architectural data dependencies.

Commit order and exceptions must implement the ISA's observable order. CA-024 onward develops pipeline structure.

### Refine with out-of-order execution

Rename registers, reservation stations and reorder buffers let independent operations execute early. Retirement reconstructs architectural order and precise state.

Memory speculation must remain within consistency rules. Mispredicted paths cannot commit architectural writes.

### Separate correctness from performance

The ISA does not promise one cycle per instruction unless explicitly timed. Two conformant cores can differ by orders of magnitude.

Instruction count alone ignores CPI, frequency, cache misses and parallelism. Performance claims name implementation and workload.

### Treat hints carefully

Prefetch, pause or branch hints may permit implementation to ignore the hint while preserving function. Their performance is not guaranteed.

Software must remain correct if a hint is ineffective. Reserved encodings are not informal hint space.

### Address security beyond semantics

Architectural privilege and checks protect specified state. Speculation, caches, predictors and contention can leak information without violating functional results.

Security architecture can add fences, domains or controls. Threat models must include microarchitectural observation when relevant.

### Write executable semantics

An interpreter or formal model makes widths, state reads/writes and trap paths testable. Sail models provide one route for RISC-V.

Executable does not mean correct automatically. Review model/spec alignment, version and environmental abstractions.

### Generate architecture tests

Tests set known state, execute an instruction and inspect allowed results. Boundary encodings, operands, privilege and exceptions need coverage.

Tests show behavior for selected cases. They do not prove every encoding sequence or memory execution.

### Use differential testing

Run the same program on independent implementations and compare commit traces. Divergence reveals a defect or permitted nondeterminism needing normalization.

Common source code or model lineage reduces independence. Preserve exact binaries and environment events.

### Use formal refinement

Prove each implementation commit corresponds to a legal ISA transition, with invariants relating internal and architectural state.

Proof scope may exclude caches, interrupts, liveness or physical faults. State assumptions and abstraction boundaries.

### Manage errata

Silicon can deviate from the published ISA. Errata state affected revisions, conditions, consequences and workarounds.

Toolchains and OSes may apply mitigations. Identification must distinguish fixed and affected parts; a workaround is not conformance.

### Govern compatibility

Freeze ISA/profile/version, extensions, ABI and platform in binary metadata and release evidence. Test old binaries on new implementations and new tools against minimum targets.

Changes to reserved behavior, counters or traps can break low-level software. Treat clarification and extension changes as versioned contracts.

## Definitions and Notation

- `S`: complete architectural state under the modeled ISA scope.
- `I`: decoded legal instruction plus operands from state.
- `Exec_ISA`: architectural transition function or relation.
- `PC`: architectural program counter.
- `S --I--> S'`: one permitted committed instruction transition.
- **commit/retire:** point where an instruction's architectural effects become visible and nonspeculative.
- **base ISA:** required core instruction/state subset.
- **extension:** named additional architectural capability.
- **profile:** constrained combination of ISA features for an ecosystem.
- **architectural trace:** ordered sequence of visible states or committed effects.
- **implementation trace:** richer internal event sequence refining architectural behavior.
- **trap:** control transfer caused by exception or accepted interrupt under privilege rules.
- **conformance:** agreement with all applicable normative requirements under declared scope.
- **erratum:** documented implementation deviation from intended specification.
- **execution environment:** services and external events surrounding instruction execution.

## Mechanisms, Invariants, or Proof Structure

1. **Scope claim:** identify ISA, edition, profile, extensions, privilege and environment.
2. **State invariant:** enumerate every software-visible register, memory and status component.
3. **Decode invariant:** classify every encoding as legal, reserved, custom or illegal.
4. **Semantic invariant:** define reads, computation, writes, PC and exceptional transition.
5. **Width invariant:** preserve signedness, overflow, alignment and byte-order rules.
6. **Memory invariant:** loads, stores, atomics and fences obey consistency and translation.
7. **Protection invariant:** privilege checks precede protected side effects.
8. **Trap invariant:** exception/interrupt state supplies correct cause and restart boundary.
9. **Extension invariant:** discovery, dependency, state and unsupported-use behavior compose.
10. **Refinement invariant:** each commit maps to a permitted architectural transition.
11. **Compatibility invariant:** old required behaviors remain under declared later targets.
12. **Model invariant:** prose, formal semantics, simulator and tests share one versioned meaning.
13. **Evidence invariant:** combine directed, generated, differential and formal checks.
14. **Deviation invariant:** identify errata and workarounds by exact implementation revision.
15. **Change invariant:** revalidate after specification, model, toolchain or hardware change.

## Alternatives and Trade-Offs

- **Small versus rich ISA:** small contracts simplify implementation; rich instructions reduce sequence length and add semantics.
- **Fixed versus variable length:** fixed length simplifies fetch/decode; variable length improves density and boundary complexity.
- **Few versus many registers:** fewer registers shorten fields; more reduce spills and enlarge encoding/state.
- **Flags versus flagless comparisons:** flags compact conditional state; explicit results simplify dependencies.
- **Strict versus weak memory order:** strict order simplifies reasoning; weak order enables implementation freedom and needs fences.
- **Trap versus defined wrap:** traps surface exceptional arithmetic; wrap is composable and explicit to software.
- **Required versus optional extensions:** required features simplify software; optionality permits smaller implementations and discovery.
- **Stable reserved space versus aggressive custom use:** reservation supports evolution; custom opcodes specialize deployments.
- **Narrative versus formal semantics:** prose is approachable; formal models make ambiguity executable and still need review.
- **Architectural versus platform feature:** architecture improves portability; platform scope can evolve hardware ecosystems separately.
- **Precise versus imprecise exceptions:** precise state simplifies recovery; imprecise mechanisms can reduce implementation cost.
- **Hardware versus software emulation:** hardware improves speed; trap-and-emulate preserves compatibility at overhead.
- **Exposed versus hidden counters:** exposure aids profiling; restriction reduces side channels and virtualization complexity.
- **Backward compatibility versus cleanup:** compatibility preserves binaries; cleanup removes historical constraints.
- **Functional conformance versus timed contract:** functional ISAs permit diversity; timed ISAs support real-time guarantees and constrain implementation.

## Failure Modes and Misconceptions

1. **“Assembly syntax is the ISA.”** encoding and state semantics are the contract.
2. **“An ISA is one processor design.”** many microarchitectures can conform.
3. **“A block diagram defines the ISA.”** it shows one implementation abstraction.
4. **“The ABI is part of every ISA instruction.”** register roles and calls are layered conventions.
5. **“System calls are ISA services.”** the trap is architectural; OS service numbers are environment ABI.
6. **“Legal instructions never trap.”** operands, privilege, alignment and memory can cause exceptions.
7. **“Illegal encodings can safely be no-ops.”** they need specified containment and future compatibility.
8. **“Reserved means permanently unused.”** later versions may assign meaning.
9. **“All registers are interchangeable.”** constant and control registers have special semantics.
10. **“PC always advances by four.”** length and control transfers vary.
11. **“Arithmetic flags exist on every ISA.”** some use explicit comparison and wrapping results.
12. **“One-thread semantics defines multicore memory.”** a consistency model is separate.
13. **“Atomic means durable.”** atomic visibility and persistence differ.
14. **“A faulting load returns an error value.”** it takes an exceptional transition.
15. **“Interrupts can appear mid-instruction architecturally.”** acceptance boundaries are specified.
16. **“Privilege is an OS-only idea.”** privileged ISA defines protected machine control.
17. **“Extension instructions are safe to probe blindly.”** discovery and trap handling matter.
18. **“Two extensions always compose.”** encoding, state and semantic dependencies can conflict.
19. **“Reset zeros architectural state.”** many values are unspecified or platform-defined.
20. **“Conformance determines speed.”** timing is mostly implementation-specific.
21. **“Instruction count predicts performance.”** CPI, frequency and memory behavior differ.
22. **“Speculation is invisible in every sense.”** microarchitectural side effects can leak.
23. **“A reference simulator is the specification.”** it can contain bugs or omit behaviors.
24. **“Architecture tests prove all sequences.”** they sample a vast state space.
25. **“Differential agreement proves correctness.”** implementations can share the same mistake.
26. **“An erratum workaround makes silicon conformant.”** it mitigates a documented deviation.

## Worked Examples

### Example 1

Two cores execute the same add in one and four cycles. Their commit result agrees, so cycle count alone is not ISA difference.

### Example 2

An assembler prints `nop`, while the binary encodes an add-immediate to constant register zero. Syntax alias and semantics remain distinct.

### Example 3

A legal load instruction traps on an unmapped address. Instruction legality does not guarantee normal completion.

### Example 4

An ABI names `x2` the stack pointer. ISA arithmetic can still address it like a register unless an instruction gives special meaning.

### Example 5

A future extension assigns a formerly reserved encoding. Old software that used it as an undocumented no-op breaks.

### Example 6

Two threads observe stores in an order permitted by the weak memory model. Each instruction is locally correct; synchronization needs fences or atomics.

### Example 7

An unsupported extension traps, and privileged software emulates it. Functional compatibility holds with different performance.

### Example 8

An out-of-order core executes a younger add early but retires after an older load. Commit trace preserves architectural dependencies.

### Example 9

A differential test diverges only on NaN payload. The ISA's permitted canonicalization determines whether either result is conformant.

### Example 10

Silicon errata identify one revision whose atomic instruction can fail under a rare condition. A software workaround does not erase the deviation record.

## Cross-Program Connections

- **Processor datapaths:** state and control implement instruction transitions.
- **Compilers:** instruction selection and scheduling target precise ISA semantics.
- **ABIs:** calling, object and binary conventions make independently built software interoperate.
- **Operating systems:** privilege, traps, translation, atomics and counters support kernels.
- **Concurrency:** language memory models compile to ISA ordering and atomic operations.
- **Virtualization:** hypervisors reproduce architectural state and intercept privileged transitions.
- **Formal methods:** transition relations and refinement connect specification to implementation.
- **Security:** privilege protects architectural state; microarchitectural channels extend threats.
- **Performance:** implementation structure, not functional semantics alone, determines cycles and energy.
- **Systems engineering:** profiles, compatibility, errata and conformance evidence govern lifecycle.

## References

1. RISC-V International, [RV32I Base Integer Instruction Set](https://docs.riscv.org/reference/isa/unpriv/rv32.html), base architectural state, instruction semantics, encodings and implementation freedom; retrieved 2026-09-04.
2. RISC-V International, [Privileged Architecture](https://docs.riscv.org/reference/isa/priv/priv-index.html), privilege modes, traps, control/status, translation and interrupts; retrieved 2026-09-04.
3. RISC-V International, [Sail RISC-V Model](https://github.com/riscv/sail-riscv), executable formal ISA semantics and generated emulation; retrieved 2026-09-04.
4. RISC-V International, [Architectural Certification Tests](https://github.com/riscv-non-isa/riscv-arch-test), architecture-test framework, test pools and model interfaces; retrieved 2026-09-04.
5. Intel, [Intel 64 and IA-32 Architectures Software Developer's Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), instruction, system, memory-order and programming contracts for a mature ISA family; retrieved 2026-09-04.
6. Arm, [Arm Architecture Reference Manual for A-profile Architecture](https://developer.arm.com/documentation/ddi0487/latest/), instruction, exception, memory and system-register semantics; retrieved 2026-09-04.
7. WebAssembly Community Group, [WebAssembly Core Specification](https://webassembly.github.io/spec/core/), typed virtual ISA syntax, validation, execution and embedding distinction; retrieved 2026-09-04.
8. RISC-V International, [ELF psABI](https://riscv-non-isa.github.io/riscv-elf-psabi-doc/), calling convention, ELF and linking rules layered on the ISA; retrieved 2026-09-04.
9. Sarah L. Harris and David Money Harris, [Digital Design and Computer Architecture: RISC-V Edition Resources](https://pages.hmc.edu/harris/ddca/ddcarv.html), ISA, assembly, datapaths and processor implementations; retrieved 2026-09-04.

## Exercises

### Exercise 1

For a small integer ISA, enumerate architectural state and specify `addi`, `add`, load, store, branch and illegal-instruction transitions.

### Exercise 2

Trace `addi x1,x0,5`, `addi x2,x1,-2`, `add x3,x1,x2` from PC 0. State what internal implementation differences are permitted.

### Exercise 3

Separate ISA, privileged architecture, platform, firmware, ABI and OS API responsibilities for booting a user program and making a file system call.

### Exercise 4

Design conformance evidence for a new optional arithmetic extension across hardware, simulator, compiler and OS discovery.

### Exercise 5

Construct assurance for an ISA implementation in a safety controller, including semantics, timing, faults, errata and named review.

## Answers to the Exercises

### Answer 1

State includes PC, integer registers with constant-zero rule, byte-addressed memory and exception cause/restart state. `addi` reads one register and signed immediate, writes wrapped fixed-width result to nonzero destination and advances PC. `add` reads two registers similarly. Load computes address, checks alignment/access, reads declared bytes, extends and writes destination or traps without normal write. Store computes address and writes declared bytes or traps without partial ordinary effect under the model. Branch compares and selects target or fall-through. Illegal encoding records cause and faulting PC and transfers to the trap vector with no ordinary register/memory write.

The full specification adds privilege, ordering, translation, interrupt priority and exact width/encoding rules. Every unchanged state component remains identical in the transition.

### Answer 2

The three commits set `x1=5`, then `x2=3`, then `x3=8`; PC values advance 0 to 4 to 8 to 12, and `x0` remains zero.

<!-- bijux-verify: {"id":"architectural-isa-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"pc=0 op=addi destination=x1 value=5\npc=4 op=addi destination=x2 value=3\npc=8 op=add destination=x3 value=8\nfinal_pc=12 x0=0 x1=5 x2=3 x3=8\n"}} -->
```python
registers = [0] * 32
pc = 0
program = (
    ("addi", 1, 0, 5),
    ("addi", 2, 1, -2),
    ("add", 3, 1, 2),
)

for instruction in program:
    op, rd, rs1, operand = instruction
    value = registers[rs1] + (registers[operand] if op == "add" else operand)
    value &= 0xFFFFFFFF
    if rd != 0:
        registers[rd] = value
    registers[0] = 0
    print(f"pc={pc} op={op} destination=x{rd} value={value}")
    pc += 4

print(
    f"final_pc={pc} x0={registers[0]} x1={registers[1]} "
    f"x2={registers[2]} x3={registers[3]}"
)
```

A conformant implementation can be single-cycle, multicycle, pipelined, in-order or out-of-order; use different adders, caches and predictors; and take different time. It must produce a permitted commit trace and exception/memory observations. The toy omits encoding, memory, privilege, traps, concurrency and environment events.

### Answer 3

ISA defines instructions, registers, memory operations and trap instruction. Privileged architecture defines modes, translation, interrupt/trap state and returns. Platform fixes reset address, memory/device map, interrupt controller and required hardware profile. Firmware initializes hardware, exposes boot interfaces and hands off machine state. ABI assigns register roles, stack, object format and binary calling. The OS API defines process, file, system-call numbers and results.

Boot crosses platform and firmware before privileged ISA establishes kernel execution. A user binary follows ISA plus ABI; its file call follows OS API and enters the kernel through an ISA trap mechanism. The kernel uses privileged ISA and platform devices. None of these layers alone specifies the whole path.

### Answer 4

Freeze extension name/version, encoding, registers, exact arithmetic, exceptions, privilege, dependencies and discovery bit. Produce normative prose and an independently reviewed executable model. Generate boundary and random tests, formally compare RTL operations where feasible, and differentially test hardware and independent simulators with normalized permitted nondeterminism.

Add assembler/disassembler, compiler feature flags, ABI preservation and OS context management. Test unsupported hardware: discovery is absent and executing the encoding traps without side effect. Cross extension combinations, virtualization, reset, interrupts and migration. Preserve binaries, signatures, trace schema, hardware revisions, models and failures. Passing tests remains bounded evidence; specification completeness and formal assumptions need separate review.

### Answer 5

Define the exact ISA/profile, instructions, privilege, memory and interrupt subset used by safety functions. Trace hazards to architectural state and required instruction outcomes. Compare RTL commit against a formal or independent executable model for all supported instructions and exception paths; verify reset, illegal encodings, privilege and memory ordering.

Add timing bounds, WCET/interference evidence and platform clocks separately because functional ISA conformance does not guarantee deadlines. Inject register, decode, arithmetic, memory, control, clock and power faults and verify detection/safe state. Track silicon errata and device identity; prohibit affected revisions unless an authorized, verified mitigation exists. Preserve specifications, models, tools, netlists and results. Named ISA, architecture, RTL, formal, physical, safety, domain, cybersecurity, verification, manufacturing, operations and independent-assurance authorities review their scopes. This module supplies no certification.
