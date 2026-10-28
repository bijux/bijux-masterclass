---
module_id: CA-012
program: Computer Architecture
level: 1
module_number: 12
title: Registers and Operand Models
status: complete
last_verified: 2026-09-04
---

# Registers and Operand Models

## One-Page Review

### Governing question

How should an instruction-set architect or implementer reason about registers and operands so every instruction has unambiguous inputs, outputs, widths and exceptional behavior across assemblers, compilers, operating systems and processors?

### Essential definitions

- An **architectural register** is a named software-visible state element whose value and access rules are defined by the architecture.
- A **physical register** is an implementation resource used to hold a value; register renaming may map one architectural name to many physical registers over time.
- A **register file** is an implementation structure that supplies storage and read/write ports for some register class.
- An **explicit operand** appears in instruction syntax or encoding; an **implicit operand** is read or written by semantics without being named in the ordinary syntax.
- A **source operand** contributes a value to an operation; a **destination operand** identifies architectural state to update.
- A **read set** and **write set** enumerate all architectural locations an instruction may observe or modify.
- An **immediate** is an operand encoded in or derived from instruction bits rather than read from a named register or memory location.
- A **register class** groups registers with common value types, widths and instruction constraints.
- A **subregister** names a portion of a wider register and requires exact preservation, clearing or extension semantics.
- A **constant register** reads a fixed value and suppresses or otherwise defines attempted writes.
- A **condition-code register** records predicates such as zero, carry, negative or overflow for later control or arithmetic operations.
- A **load-store operand model** permits ordinary computation on registers and uses explicit loads/stores for memory.
- A **register-memory operand model** permits at least some operations to name memory directly as an operand.
- A **stack operand model** takes operands from and returns results to an implicit evaluation stack.
- An **ABI register role** is a software convention such as argument, return, saved or temporary; it is layered on architectural register semantics.

### Central model, mechanism, or theorem

For instruction `I`, define

`S' = Exec(I, S, Imm(I), E)`

with explicit architectural read set `R(I, S)`, write set `W(I, S)`, operand widths, conversions and exception alternatives. Values read from registers belong to the pre-state `S`; ordinary destination updates become visible in `S'`. Every architectural component outside the permitted write set remains unchanged. An implementation may rename, forward, bypass or replicate values internally, but its committed state must refine this relation.

### Critical invariants

- Register count, width, reset/unknown status and access privilege are explicit for every architectural register class.
- Every instruction defines all explicit and implicit sources, destinations and state dependencies.
- Immediate extraction, sign/zero extension, shifting and scaling are exact functions of encoding bits.
- Constant-register writes and subregister writes have specified suppression, preservation or clearing effects.
- Flags, PC, stack pointer, link state, vector masks and control/status state appear in read/write sets when affected.
- Faulting instructions expose only the state updates permitted by their exception model.
- ABI aliases never change architectural identity or semantics.
- Physical renaming and bypassing cannot create an architectural observation absent from the ISA relation.

### Common failures

Frequent failures are calling every storage element a register, assuming all registers are interchangeable, treating ABI names as ISA semantics, omitting implicit flags or stack operands, reading a destination after an overlapping source has been updated, confusing sign extension with zero extension, ignoring subregister clearing rules, assuming a constant register stores writes, modeling PC as always an ordinary general register, overlooking privilege on control registers, treating a register pair as two independent commits, assuming architectural register count determines physical count, exposing speculative values through exceptions, and using a passing arithmetic example as proof of complete operand decoding.

### Compact example

In a 32-bit load-store model, `addi x1,x0,-1` reads constant `x0=0`, sign-extends the immediate and writes `0xffffffff` to `x1`. `add x3,x1,x2` reads both sources from the pre-state, adds modulo `2^32`, writes only `x3` and advances PC. An attempted ordinary write to `x0` is suppressed. A core may forward the new `x1` from a pipeline rather than read it from an array, but the committed register trace is the same.

### Connections

Register and operand models connect instruction encoding, datapaths, pipelines, compiler register allocation, calling conventions, context switching, exceptions, virtualization, debugging, formal semantics, information flow and performance.

## Governing Question

Registers look simple because assembly displays short names beside operations. The real contract is larger: which state is read, when values are sampled, which bits are transformed, which state is written, what overlaps, and what happens on a fault.

The governing question is how to specify that contract without confusing architectural names with ABI roles or implementation storage. A compiler reasons about live architectural values, an operating system preserves context, and a processor may rename those values into a much larger physical space. All must agree at architectural boundaries.

## Why This Matters

A one-bit ambiguity in operand semantics can corrupt every program that uses an instruction. Sign-extending a displacement where zero extension was intended changes addresses. Preserving the high portion of a register where the ISA requires clearing it creates data dependencies and wrong values. Omitting an implicit flag write can miscompile a later branch.

Register design also shapes instruction density, datapath ports, context-switch cost and compiler behavior. More architectural registers can reduce spills but consume encoding space and saved context. Specialized register classes can express vectors or predicates well but complicate allocation and movement.

Verification must cover more than final arithmetic. It must establish exact read/write sets, overlap behavior, constant registers, reserved names, privilege checks, exceptional exits and the committed abstraction over physical renaming.

## Prerequisites and Retrieval

Before studying this module, be able to:

- distinguish architectural state from microarchitectural state;
- trace a register read, ALU operation and guarded writeback;
- interpret fixed-width signed and unsigned bit vectors;
- explain instruction fields, exceptions and calling conventions conceptually;
- reason about pre-state and post-state in a transition system.

Retrieve ISA name and version; execution modes; integer, floating-point, vector, predicate, capability and control/status register inventories; register widths; hardwired values; aliases; privilege and access rules; explicit and implicit operands per instruction; immediate layouts; extension/truncation rules; subregister overlap; PC and link semantics; flag definitions; memory operands; register-pair constraints; exception atomicity; reset values; context format; ABI register roles; debug access; virtualization behavior; rename/commit documentation; formal semantics; architecture tests; compiler target description; silicon errata; and exact hardware or simulator revision.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish architectural registers, physical registers and register-file structures;
2. enumerate complete explicit and implicit instruction read/write sets;
3. derive immediate operands and width conversions from encoding bits;
4. compare accumulator, stack, register-memory and load-store operand models;
5. reason about constant, overlapping and special-purpose registers;
6. separate ISA register semantics from ABI aliases and roles;
7. analyze flags, predicates, vector state and control/status registers;
8. specify fault and interrupt behavior for multi-state updates;
9. relate compiler allocation and context switching to register architecture;
10. verify commit-level behavior despite forwarding and physical renaming.

## Core Exposition

### Start with architectural identity

An architectural register name denotes a location in the software-visible state model. Its identity persists across instructions even if the implementation moves its value among latches, queues, bypass networks and physical registers.

Do not infer physical layout from an ISA diagram. A logical file with two reads and one write per instruction may be banked, replicated or bypassed. Conversely, one physical array can serve several architectural purposes through scheduling.

### Inventory register classes

General-purpose integer registers are only one class. Architectures may expose floating-point, vector, predicate, capability, segment, control/status, debug and performance registers.

For each class, record count, width, element interpretation, privilege, reset state, accessibility and save/restore requirements. “Register” does not imply unrestricted arithmetic or user access.

### Define sources and destinations

Instruction syntax should not be the sole source of operand truth. Semantics must state each architectural source and destination, including conditional writes.

For a three-operand add, two sources and one destination are explicit. For an instruction that accumulates into its destination, the destination is also a source. Treating it only as an output loses a dependency.

### Make read and write sets explicit

Define `R(I,S)` as locations whose pre-state values can affect execution and `W(I,S)` as locations the instruction may update. Sets can depend on mode, operands and exceptional conditions.

The complement rule is essential: locations outside the selected write set remain unchanged. This converts vague pseudocode into checkable frame conditions.

### Sample operands from the pre-state

An architectural transition conceptually reads required inputs from `S` and produces `S'`. This handles overlap cleanly: if `rd=rs1`, the old source value participates in the operation before the destination is replaced.

Hardware can implement this by register-file timing, forwarding or renaming. The architectural model need not prescribe which mechanism supplies the logically old value.

### Specify value widths

Each operand has a bit width and interpretation at each boundary. Addition may ignore signedness at the bit-vector level while comparisons, division and extension depend on signed or unsigned interpretation.

State whether results wrap, saturate, trap or set flags. Define narrowing by low-bit selection, rounding or exception rather than saying merely “convert.”

### Derive immediate values exactly

An immediate can be contiguous or assembled from scattered instruction bits. Define concatenation order, inserted low zeros, sign bit, extension width and any scaling.

For a `k`-bit two’s-complement immediate extended to width `w`, the upper `w-k` bits repeat bit `k-1`. Zero extension fills them with zero. The same encoded low bits can therefore denote different operands.

### Treat constants as semantics

A constant-zero register can simplify encoding and common operations. Reading it returns zero; an ordinary write is either suppressed or follows the architecture’s exact rule.

The implementation need not allocate writable storage for it. Verification should attempt every instruction form that names it as destination and source, including faulting instructions.

### Separate architectural names from aliases

One register can have numeric, architectural and ABI names. An ABI might call the same location `sp`, `a0` or `saved0` depending on its assigned role.

Aliases do not create new state. Changing an ABI role does not change instruction semantics, although software interoperability depends on following the convention.

### Specify subregister overlap

Some architectures name low or high portions of wider registers. A write may preserve untouched bits, clear upper bits or make them architecturally unknown.

These rules affect dependencies and security. A verifier must model overlap as a relation over the enclosing architectural state, not as independent variables with the same spelling root.

### Treat the PC deliberately

The program counter may be implicit, partly visible or directly addressable. Instructions can read the address of the current instruction, a defined aligned base, the next instruction or another architecture-specific value.

Branches, calls, returns, traps and variable-length encodings all update control-flow state. Do not assume every instruction merely adds four.

### Model link and stack registers

A call may write a link register explicitly or implicitly. A push may update a stack pointer and memory as one instruction’s effect.

Architectures that use ordinary general registers for these roles still rely on ABI conventions. Architectures with implicit stack or link state place those locations directly in instruction read/write sets.

### Compare accumulator models

An accumulator machine uses one implicit register as a frequent source and destination. Encodings can be compact because fewer operand names are required.

The implicit dependency lengthens value chains and constrains scheduling. Specifications and compiler models must include accumulator reads and writes even when assembly omits them.

### Compare stack models

A stack machine consumes top elements and pushes results. Operand naming is compact and maps naturally to expression evaluation.

Stack depth, value types, underflow, overflow and exceptional atomicity become architectural questions. Implementations may cache stack entries in physical registers without changing the logical stack model.

### Compare register-memory models

A register-memory instruction can combine a register operand with a memory operand. This can improve code density and reduce explicit loads.

It couples computation to address generation, memory faults and variable latency. The specification must define whether any register or flag update occurs if the memory access faults.

### Compare load-store models

A load-store architecture performs ordinary arithmetic on registers; dedicated instructions transfer values between registers and memory. This regularizes datapaths and dependencies.

It can increase dynamic instruction count and require more architectural registers. “Load-store” does not mean every instruction has three register operands or that memory semantics are simple.

### Handle two-operand and three-operand forms

In a two-operand form such as `add d,s`, `d` is both source and destination. In a three-operand form `add d,a,b`, the inputs can remain live independently of the result.

Two-operand encoding saves bits but introduces destructive updates. Compilers may insert copies; renaming can eliminate some physical copies while preserving architectural dependencies.

### Make implicit flags visible

Condition-code architectures write flags even when ordinary syntax names only a data destination. Later branches, carries or conditional moves read those flags.

Some instruction variants deliberately suppress flag writes. Confusing the variants changes dependency graphs and program behavior.

### Compare flags and predicate results

An ISA can record comparisons in global flags, general registers or predicate registers. Global flags encode common branches compactly but create implicit shared dependencies.

Explicit predicate destinations expose dataflow and support predication or vector masks, at the cost of operand fields and register state.

### Specify vector operands

Vector instructions may read vector registers, scalar registers, masks, vector length and element configuration. A short mnemonic can therefore have a large implicit read set.

Define inactive elements as undisturbed, zeroed or agnostic, and define tail behavior. Restart after a fault may require an architectural progress index.

### Specify register groups

Wide values can occupy aligned register pairs or groups. The legal starting names, overlap restrictions and update atomicity must be explicit.

An illegal group should trap according to the encoding contract. It must not silently wrap from the last register to the first unless specified.

### Control access to status registers

Control/status registers can hold privilege, interrupt, translation, feature and counter state. Access may be read-only, write-one-to-clear, WARL, masked or mode-dependent.

A generic “register write” model is inadequate. Define implemented fields, reserved bits, side effects, serialization and traps.

### Distinguish register state from memory

Registers and memory occupy different architectural namespaces even if an implementation spills internal values or maps devices into addresses. Register access ordinarily has instruction-specified naming and atomicity.

Memory introduces addressing, translation, ordering and sharing. A register-window spill performed by hardware may cross the boundary and needs its own architectural exception rules.

### Define exceptional atomicity

If an instruction faults, specify which destinations, flags, PC and memory effects are visible. Precise exceptions commonly require no ordinary architectural result before the trap state is established.

Complex or vector instructions may permit partial progress, but progress state and restart rules must then be architectural. “The instruction failed” is not enough.

### Preserve state across interrupts

Interrupt acceptance occurs at an architectural boundary defined by the ISA. The saved PC and status must identify the correct restart or resume point.

Physical registers and speculative results are not OS context. The implementation drains, checkpoints or rolls back internal state so software sees the architectural boundary.

### Design context switching

An OS saves register state that can be live for the execution context. Optional floating-point or vector state may be saved lazily under controlled ownership rules.

Context formats need version and feature awareness. Failing to preserve a newly enabled register class leaks or corrupts state between processes or virtual machines.

### Layer the calling convention

The ABI assigns argument, result, temporary, callee-saved, stack, global and thread roles to architectural registers. It also defines preservation and stack alignment.

ISA conformance does not imply ABI conformance. A hand-written function may use any architecturally legal register and still fail when linked because it violates preservation rules.

### Connect to compiler allocation

Register allocation maps program values to architectural registers or spill locations. The compiler uses register classes, interference, calling conventions, instruction constraints and clobbers.

Inline assembly with an incomplete clobber list breaks this model. Hidden flag, mask or special-register effects must appear in the compiler description.

### Distinguish physical renaming

Out-of-order processors map each destination version to a physical register, eliminating false write-after-read and write-after-write dependencies. A rename map binds current architectural names to speculative versions.

At commit, the machine exposes effects in permitted architectural order. Flush recovery restores the correct map and prevents wrong-path values from becoming architectural.

### Treat forwarding as value delivery

A dependent instruction may receive its source from an execution result before register-file writeback. Forwarding changes latency, not the architectural source.

Verification compares the value with the preceding committed transition and checks selection priority. A stale register-file value must not win over the required newer producer.

### Include debug and virtualization

Debuggers read and write architectural registers while execution is halted or through defined access mechanisms. Observed values must correspond to an architectural boundary.

Hypervisors virtualize guest register and control state. Banking, trapping and shadowing must reproduce the guest-visible contract without leaking host or other-guest state.

### Analyze information flow

Registers can carry secrets across privilege or tenant boundaries if context clearing is incomplete. Reserved upper bits, vector tails and debug registers deserve explicit handling.

Microarchitectural remnants can also leak through side channels even when architectural state is cleared. Functional register semantics and residual-state security evidence are related but distinct.

### Build executable semantics

An executable model should implement extraction, reads, conversions, operation, exception choice and writes in an auditable order. Frame conditions should be testable.

Keep specification code independent from RTL where possible. Shared decoding or copied pseudocode can produce correlated defects in both model and design.

### Verify operand behavior systematically

Generate tests across every legal register name, source/destination equality pattern, immediate boundary, width, privilege mode and exception. Include constant and reserved registers.

Compare committed traces containing instruction address, decoded operands, source values, destinations, write masks, results, flags and traps. Normalize only behavior the specification truly leaves open.

### Govern changes over time

Adding registers or operand forms consumes encoding, context and toolchain capacity. Define discovery, reset, save/restore, debug and virtualization before deployment.

Track specification versions, compiler descriptions, models, tests, RTL, silicon revisions and errata together. A workaround is not a silent redefinition of the architectural contract.

## Definitions and Notation

- `S`: complete architectural pre-state.
- `S'`: architectural post-state after one permitted transition.
- `I`: decoded instruction with its encoding and execution context.
- `R(I,S)`: architectural locations whose pre-state values affect instruction behavior.
- `W(I,S)`: architectural locations that the instruction may update.
- `Reg[c,i]`: register index `i` in architectural class `c`.
- `XLEN`: width of a general-purpose integer register for the selected execution mode.
- `bits[x,h:l]`: bits `h` through `l` of value `x`.
- `sext_k_to_w(x)`: sign extension of a `k`-bit bit vector to `w` bits.
- `zext_k_to_w(x)`: zero extension of a `k`-bit bit vector to `w` bits.
- `write_mask`: bits of an enclosing register changed by a subregister destination.
- `PC`: architectural control-flow location defined for the instruction.
- `Flags`: architectural condition state, if present.
- `Map[a]`: speculative mapping from architectural register `a` to a physical register.
- `commit`: event that makes an instruction’s permitted architectural effects visible.

Unless stated otherwise, arithmetic examples operate on unsigned bit vectors modulo `2^XLEN`; signed interpretation is applied only by named signed operations.

## Mechanisms, Invariants, or Proof Structure

1. **Inventory obligation:** enumerate every architectural register class, count, width, alias, access rule and reset/unknown condition.
2. **Decode obligation:** prove every legal encoding selects the specified explicit register and immediate operands.
3. **Read-set obligation:** prove every state value that can affect an instruction appears in its architectural read set.
4. **Pre-state obligation:** prove overlapping sources are sampled according to the pre-state relation.
5. **Width obligation:** prove extraction, extension, truncation, scaling and modulo behavior at every operand boundary.
6. **Write-set obligation:** prove successful execution updates exactly the permitted destinations and masks.
7. **Frame obligation:** prove every architectural location outside the permitted write set remains unchanged.
8. **Constant obligation:** prove constant registers return their fixed value and reject writes exactly as specified.
9. **Overlap obligation:** prove subregister and register-group updates preserve, clear or replace enclosing bits correctly.
10. **Implicit-state obligation:** prove PC, flags, stack, link, mask and control/status effects are included when applicable.
11. **Exception obligation:** prove faults suppress or expose partial operand effects only as permitted and establish correct trap state.
12. **Privilege obligation:** prove restricted register accesses return, mask or trap according to mode and field policy.
13. **Context obligation:** prove save, restore, debug and virtualization preserve the complete enabled architectural state.
14. **Refinement obligation:** prove forwarding, renaming and speculative execution commit a trace allowed by the register transition model.
15. **Evidence obligation:** bind tests and proofs to exact ISA, ABI, model, compiler, RTL and hardware versions and record limitations.

## Alternatives and Trade-Offs

1. **Few versus many architectural registers:** fewer names save encoding and context; more names reduce spills and expose parallel values.
2. **Uniform versus specialized classes:** uniform registers simplify movement and allocation; specialization represents types and operations efficiently.
3. **Explicit versus implicit operands:** explicit dataflow improves analysis; implicit operands improve density and familiar idioms.
4. **Two versus three operands:** two-operand forms encode compactly; three-operand forms avoid destructive updates.
5. **Accumulator versus general registers:** an accumulator saves fields; general registers support scheduling and parallel live ranges.
6. **Stack versus named operands:** stack code is compact; named operands make random access and dependencies explicit.
7. **Register-memory versus load-store:** memory operands can reduce instruction count; load-store designs regularize execution and faults.
8. **Global flags versus predicates:** flags encode common conditions cheaply; predicate results make dependencies explicit and scalable.
9. **Constant register versus immediate encodings:** a constant register enables reusable forms; dedicated forms can reclaim a name or encode richer immediates.
10. **Overlapping versus independent widths:** overlap supports compact legacy operations; independent state avoids partial-register hazards.
11. **Fixed versus windowed registers:** fixed names simplify context; windows reduce some calls but complicate overflow and switching.
12. **Scalar versus vector architectural state:** vectors raise throughput and density; they enlarge context and restart semantics.
13. **Eager versus lazy context save:** eager save is simple; lazy save reduces common cost but complicates ownership and security.
14. **Precise all-or-none versus restartable partial effects:** precision simplifies software; partial progress can support long vector operations efficiently.
15. **Architectural exposure versus implementation freedom:** exposing more state enables control and tuning; hidden physical organization evolves more freely.

## Failure Modes and Misconceptions

1. “Every named register is general purpose.” Classes, privilege and instruction constraints differ.
2. “Every hardware latch is architectural.” Pipeline and queue state can be purely microarchitectural.
3. “The architectural register count equals physical storage count.” Renaming, replication and banking break that equality.
4. “ABI aliases create distinct registers.” Multiple names can denote one architectural location.
5. “A destination is never a source.” Accumulators and two-operand forms read the old destination.
6. “Assembly lists every operand.” PC, flags, stack state, masks and status can be implicit.
7. “Signed and unsigned add use different bit-vector addition.” Often the sum bits agree while overflow, comparison and extension differ.
8. “An immediate is the literal printed by the assembler.” Relocation, scattered fields, scaling and canonical display can intervene.
9. “Sign extension fills zeros.” It repeats the encoded sign bit.
10. “Narrow writes always preserve upper bits.” Some architectures clear or make them unknown.
11. “Subregisters are independent variables.” Their state overlaps an enclosing register.
12. “Writing a constant-zero register stores a value.” Its architectural write behavior is specified, commonly suppressed.
13. “PC always denotes the next instruction.” The value exposed to an operation is architecture-specific.
14. “All instructions advance PC by four.” Variable length, control flow, traps and replay contradict this.
15. “Flags are only performance metadata.” If software can read them or branch on them, they are architectural state.
16. “Load-store means no implicit memory access ever occurs.” Stack/window management or architecture-defined mechanisms may differ.
17. “A memory operand is just another register operand.” It brings addressing, translation, ordering, latency and faults.
18. “A faulting instruction never changes any state.” Trap state or specified partial progress can change.
19. “Register-pair names may wrap freely.” Alignment and legal-group rules must be followed.
20. “Reserved control bits can hold arbitrary application data.” Future definitions and write policies make that unsafe.
21. “Context switch only saves integer registers.” Enabled flags, vectors, predicates, control and other state may be live.
22. “Lazy state save is automatically safe.” Ownership transitions, interrupts and speculation require discipline.
23. “Forwarding changes which architectural value is read.” It changes delivery, not the specified dependency.
24. “Renaming changes the ISA register set.” It versions values behind the architectural abstraction.
25. “Passing compiler tests proves operand decoding.” Boundary names, overlaps, faults and privilege still require direct evidence.
26. “Clearing architectural registers removes every secret.” Microarchitectural remnants require separate security analysis.

## Worked Examples

### Example 1

In `add x3,x1,x2`, `R={x1,x2,PC}` and an ordinary write set includes `{x3,PC}`. If `x3=x1`, the original `x1` is read before its post-state replacement.

### Example 2

A 12-bit immediate `0xfff` sign-extends to `0xffffffff` at width 32, representing `-1`; zero extension yields `0x00000fff`, representing 4095.

### Example 3

An attempted `addi x0,x0,9` in a constant-zero-register design still reads zero and computes a temporary result, but the architectural destination write is suppressed and `x0` remains zero.

### Example 4

In a destructive `add r1,r2`, the old `r1` and `r2` are sources and `r1` is destination. A compiler must preserve old `r1` elsewhere if it remains live.

### Example 5

A low-32-bit write that clears bits 63:32 breaks dependence on the previous high half; a low-16-bit write that preserves upper bits retains that dependence. The exact rule belongs in semantics.

### Example 6

A compare that writes global flags has `Flags` in its write set. A later conditional branch reads `Flags` even though no flag operand appears in ordinary syntax.

### Example 7

A vector add with masking can read two vector sources, a mask, vector length and element configuration, then conditionally write active destination elements while following a specified tail policy.

### Example 8

A register-memory add that faults during address translation must follow the exception rule: ordinary destination and flags remain unchanged if the ISA promises precise all-or-none completion.

### Example 9

An out-of-order core maps two successive writes to architectural `x5` onto different physical registers. Consumers receive the correct version; retirement exposes writes in permitted architectural order.

### Example 10

An ABI calls one architectural register the stack pointer and requires callees to preserve another. The ISA permits arithmetic on both; interoperability depends on the additional ABI contract.

## Cross-Program Connections

- **Instruction encoding:** operand fields, immediate fragments and aliases determine representable register forms.
- **Datapaths:** ports, bypasses and write masks implement architectural reads and writes.
- **Pipelines:** hazards arise from dependencies among operand versions and commit ordering.
- **Compilers:** allocation, instruction selection and clobbers depend on accurate register classes and constraints.
- **ABIs:** register roles, preservation and stack conventions enable separately compiled code.
- **Operating systems:** context switching and traps preserve enabled architectural state.
- **Virtualization:** guest register state is banked, trapped, shadowed or emulated.
- **Formal methods:** read/write sets and frame conditions make instruction semantics compositional.
- **Security:** context clearing, privilege and residual physical state affect information flow.
- **Systems engineering:** versioned inventories, errata and evidence bind the register contract across lifecycle.

## References

1. RISC-V International, [RV32I Base Integer Instruction Set](https://docs.riscv.org/reference/isa/unpriv/rv32.html), integer register state, constant-zero register, immediates and base operand forms; retrieved 2026-09-04.
2. RISC-V International, [RV64I Base Integer Instruction Set](https://docs.riscv.org/reference/isa/unpriv/rv64.html), wider registers and word-operation sign-extension behavior; retrieved 2026-09-04.
3. RISC-V International, [Calling Convention Chapter](https://docs.riscv.org/reference/isa/unpriv/calling-convention.html), distinction between ISA semantics and software calling convention; retrieved 2026-09-04.
4. RISC-V International, [ELF psABI](https://riscv-non-isa.github.io/riscv-elf-psabi-doc/), register roles, preservation and binary conventions; retrieved 2026-09-04.
5. Arm, [Arm Architecture Reference Manual for A-profile Architecture](https://developer.arm.com/documentation/ddi0487/latest/), general, SIMD/vector, predicate, status and system register semantics; retrieved 2026-09-04.
6. Intel, [Intel 64 and IA-32 Architectures Software Developer's Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), general registers, subregisters, flags, vector state and instruction operands; retrieved 2026-09-04.
7. LLVM Project, [LLVM Language Reference Manual](https://llvm.org/docs/LangRef.html), typed SSA values and target-independent operand semantics for compiler comparison; retrieved 2026-09-04.
8. WebAssembly Community Group, [WebAssembly Instructions](https://webassembly.github.io/spec/core/syntax/instructions.html), typed stack-machine operand model and structured control; retrieved 2026-09-04.

## Exercises

### Exercise 1

Specify read sets, write sets, widths and frame conditions for `addi`, three-operand `add`, destructive two-operand `add`, load, call and conditional branch.

### Exercise 2

Trace a 32-bit register machine executing `addi x1,x0,-1`, `addi x2,x0,5`, `add x3,x1,x2`, `slli x4,x2,2` and `addi x0,x0,9`. Include hexadecimal writes and final state.

### Exercise 3

Compare accumulator, stack, two-operand register-memory and three-operand load-store implementations of `(a+b)*(c-d)`.

### Exercise 4

Design verification for a 64-bit architecture whose 32-bit destinations clear upper bits, 16-bit destinations preserve upper bits, and register zero suppresses writes.

### Exercise 5

Construct assurance for adding an optional vector register class to an existing processor, compiler, ABI, OS, hypervisor and debugger ecosystem.

## Answers to the Exercises

### Answer 1

`addi d,a,k` reads `a` and PC, derives and extends `k`, and writes `d` plus next PC; `add d,a,b` replaces the immediate with source `b`. If `d` is constant zero, the data write is suppressed. A destructive `add d,s` reads old `d` and `s`, then writes `d`. Every non-written register remains unchanged.

A load reads base, immediate, PC and memory/translation state, then writes destination and PC or takes a fault path with the specified ordinary-write suppression. A call reads its target inputs and PC, writes link state and PC, and may update stack only if the architecture—not merely the ABI—says so. A flag-based conditional branch reads PC, target operands and flags and writes PC. Exact exception and status writes augment each set.

### Answer 2

At width 32, sign-extending `-1` produces `0xffffffff`; adding 5 wraps to 4; shifting 5 left by two produces 20. The attempted `x0` write is suppressed.

<!-- bijux-verify: {"id":"register-operand-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"pc=00 op=addi destination=x1 value=0xffffffff\npc=04 op=addi destination=x2 value=0x00000005\npc=08 op=add destination=x3 value=0x00000004\npc=12 op=slli destination=x4 value=0x00000014\npc=16 op=addi destination=x0 value=0x00000009 suppressed=true\nfinal_pc=20 x0=0x00000000 x1=0xffffffff x2=0x00000005 x3=0x00000004 x4=0x00000014\n"}} -->
```python
width = 32
mask = (1 << width) - 1
registers = [0] * 8
pc = 0
program = (
    ("addi", 1, 0, -1),
    ("addi", 2, 0, 5),
    ("add", 3, 1, 2),
    ("slli", 4, 2, 2),
    ("addi", 0, 0, 9),
)

for op, destination, source, operand in program:
    if op == "add":
        value = registers[source] + registers[operand]
    elif op == "slli":
        value = registers[source] << operand
    else:
        value = registers[source] + operand
    value &= mask
    suppressed = destination == 0
    if not suppressed:
        registers[destination] = value
    suffix = " suppressed=true" if suppressed else ""
    print(
        f"pc={pc:02d} op={op} destination=x{destination} "
        f"value=0x{value:08x}{suffix}"
    )
    pc += 4

print(
    f"final_pc={pc} x0=0x{registers[0]:08x} x1=0x{registers[1]:08x} "
    f"x2=0x{registers[2]:08x} x3=0x{registers[3]:08x} "
    f"x4=0x{registers[4]:08x}"
)
```

The trace proves only these toy register transitions. It omits binary encoding, privilege, flags, memory, exceptions, concurrency, vector state and implementation timing.

### Answer 3

An accumulator machine loads `a`, adds `b`, stores the sum temporarily, loads `c`, subtracts `d`, and multiplies with the saved value; its arithmetic repeatedly reads/writes implicit accumulator state. A stack machine pushes operands, performs add and subtract on top entries, then multiplies the two stack results; depth and order are architectural.

A two-operand register-memory machine can load or move one value into a destination, add a register or memory source destructively, form the second result similarly, and multiply, with each memory operand adding a fault boundary. A three-operand load-store machine loads four values into registers, computes two non-destructive results, then multiplies them. Its code may use more instructions and registers, but arithmetic dependencies and memory operations are explicit.

### Answer 4

Generate every source/destination equality pattern at boundary indices, including register zero. For 32-bit writes, seed upper halves with nonzero patterns and prove bits 63:32 become zero. For 16-bit writes, seed both halves and prove bits 63:16 remain identical while bits 15:0 match the result. Attempt every instruction class with zero as destination and prove the full enclosing state is unchanged except other specified effects.

Add immediate minima/maxima, arithmetic carries, illegal names, privilege, interrupts and fault paths. Compare RTL commit masks and values with an independent model, assert frame conditions formally, and test forwarding and renaming cases where old and new partial values compete. Record exact ISA, RTL, model, test and silicon versions.

### Answer 5

Freeze vector register count, width model, element types, mask/tail behavior, configuration state, exception progress and discovery. Define movement between scalar and vector classes, reset, privilege, debug and virtualization. Extend the formal/executable model, decoder, trace schema and context inventory.

The compiler needs register classes, allocation constraints, intrinsics and instruction selection; the ABI needs argument/preservation and context rules; the OS and hypervisor need ownership and save/restore; the debugger needs display and mutation. Test unsupported discovery, process and guest isolation, interrupts during vector work, lazy-save ownership, migration, fault restart, all register overlaps and silicon errata. Named architecture, compiler, ABI, kernel, hypervisor, debug, RTL, formal, verification, security, safety and independent-assurance reviewers assess their scopes. This module supplies no certification.
