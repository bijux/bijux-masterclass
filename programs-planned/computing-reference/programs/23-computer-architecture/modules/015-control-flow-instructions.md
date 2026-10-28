---
module_id: CA-015
program: Computer Architecture
level: 1
module_number: 15
title: Control-Flow Instructions
status: complete
last_verified: 2026-09-04
---

# Control-Flow Instructions

## One-Page Review

### Governing question

How does an ISA specify sequential, conditional, direct, indirect, call and return control transfers so target computation, link state, alignment, faults and committed execution remain unambiguous across software and processors?

### Essential definitions

- **control flow** is the architectural sequence of instruction addresses selected during execution.
- The **fall-through address** is the address of the sequential instruction following the current instruction under its actual length.
- A **branch** conditionally selects a target or fall-through address.
- A **jump** unconditionally selects a nonsequential target.
- A **direct transfer** derives its target primarily from instruction bits and a specified base.
- An **indirect transfer** derives its target from a register or memory-provided value, optionally adjusted by an immediate.
- A **link register** or link destination receives a return address as part of a call-like transfer.
- A **return** is an indirect transfer following calling-convention or architecture-defined return state.
- A **branch condition** is the architectural predicate deciding whether a conditional transfer is taken.
- A **delay slot** is an architecturally defined instruction position executed around a control transfer in some ISAs.
- **control-flow alignment** constrains legal target addresses or instruction boundaries.
- A **control-flow graph** abstracts basic blocks and possible edges; dynamic execution selects a trace through it.
- **branch prediction** is a microarchitectural guess about direction or target, not the architectural decision.
- A **misprediction recovery** discards wrong-path effects so committed state follows the resolved transfer.
- **control-flow integrity** constrains permitted dynamic transfer targets using software, ISA or hardware mechanisms.

### Central model, mechanism, or theorem

For instruction at architectural address `PC` and length `L`, define `fallthrough=PC+L`. A direct conditional branch computes target `T=BranchBase(PC)+sext(imm)*scale` and next PC

`PC' = T if Condition(S) else fallthrough`.

A link-producing transfer additionally writes its specified destination with `fallthrough`. An indirect transfer computes and normalizes a register-derived target before checking alignment, privilege and executable mapping. All ordinary state outside the permitted write set remains unchanged. Speculative paths are conformant only when retirement exposes the same permitted control-flow and exception trace.

### Critical invariants

- Fall-through uses the actual instruction length and address arithmetic rules.
- Every condition names exact source values, signedness and comparison semantics.
- Direct targets use the correct PC/page base, displacement reconstruction and scale.
- Indirect targets use the correct pre-state register, offset, normalization and alignment.
- Link value and link destination are exact, including suppressed or overlapping writes.
- Illegal or faulting targets cannot commit wrong-path ordinary effects.
- Prediction structures influence timing but not architectural branch decisions.
- CFI, privilege and executable-memory policy reject unauthorized targets at defined boundaries.

### Common failures

Frequent failures are adding a branch displacement to the next PC when the ISA uses the current PC, assuming every instruction is four bytes, comparing signed operands as unsigned, forgetting that a branch offset is scaled, using a newly written register instead of its pre-state value for an overlapping indirect jump, storing the target rather than fall-through as the link, failing to clear required low target bits, fetching before alignment or execute permission is resolved, treating returns as a unique hardware instruction when they are ABI patterns, committing wrong-path stores, calling prediction architecturally visible, and claiming CFI from a return-address stack alone.

### Compact example

A loop branches from PC 16 back to PC 8 while `x1!=0`. With `x1=2`, each body iteration increments `x2` and decrements `x1`; the branch is taken once and then falls through, leaving `x1=0` and `x2=2`. A jump at PC 20 to PC 28 writes link value 24. An indirect jump at PC 32 can select address 36 while suppressing a link write to constant `x0`. Prediction may guess these events, but only resolved targets and link effects commit.

### Connections

Control-flow instructions connect encoding, PC-relative addressing, calling conventions, pipelines, prediction, exceptions, compilers, linkers, virtualization, debugging, security and formal verification.

## Governing Question

Most instructions transform data and advance sequentially. Control-flow instructions choose which instruction is interpreted next, so one error changes every later effect. Their semantics must define both paths, not merely the “taken” case.

The governing question is how to specify target computation and state updates independently of implementation prediction. Modern processors may fetch far beyond a branch, yet the architectural trace must look as though each transfer selected one permitted successor or precise exception.

## Why This Matters

Branches implement decisions and loops; calls and returns organize software; indirect transfers support dispatch, dynamic linking and virtual methods. Wrong signedness, offset base or instruction length can redirect execution only at rare layout boundaries.

Control flow is also a central performance and security surface. Prediction hides latency but creates recovery and side-channel risks. Indirect targets are attractive attack primitives, motivating software CFI, landing pads, shadow stacks and privilege checks.

Verification must connect semantics, binary encoding, linker relocation, compiler CFG and processor commit. A correct target calculator alone does not prove condition evaluation, exception priority, wrong-path suppression or CFI enforcement.

## Prerequisites and Retrieval

Before studying this module, be able to:

- derive instruction length and PC-relative effective addresses;
- compare fixed-width signed and unsigned values;
- distinguish architectural and speculative state;
- explain precise exceptions and executable-memory permission;
- read a basic control-flow graph.

Retrieve ISA/profile/version; instruction lengths; PC/fall-through convention; conditional operations and signedness; flag/predicate definitions; direct-target displacement layouts and scales; indirect-target computation and normalization; target alignment; link semantics; call/return aliases; delay-slot rules; exception/trap transfers; privilege-return operations; CFI extensions; branch hints; relocation types; veneers/thunks; compiler lowering; executable model; predictor and recovery design; commit trace; architecture tests; security policy; silicon errata; and exact tool/hardware revisions.

## Learning Objectives

After completing this module, you should be able to:

1. specify fall-through, direct and indirect target calculations;
2. derive signed, unsigned, flag and predicate branch conditions;
3. distinguish branch, jump, call and return architectural effects;
4. reason about link values, overlapping operands and target normalization;
5. specify alignment, permission and exception behavior for transfers;
6. relate compiler CFG edges and linker relocations to ISA control flow;
7. separate branch prediction and recovery from architectural semantics;
8. analyze control-flow-integrity mechanisms and their limits;
9. verify wrong-path suppression and commit-level refinement;
10. govern compatibility, security and errata for control-flow features.

## Core Exposition

### Define the sequential successor

Start every instruction with an architecture-defined sequential successor, usually `PC+length`. Variable-length encodings make length part of the transition.

Sequential overflow, alignment and address validity follow ISA rules. Do not bake a four-byte increment into a generic control-flow model.

### Define direct jumps

A direct jump reconstructs a displacement or absolute target from instruction bits. PC-relative forms add a signed scaled displacement to an exact PC base.

The encoder and relocation must prove target reach and alignment before discarding implied low bits. The processor reconstructs the identical value.

### Define conditional branches

A branch has a condition plus taken and not-taken successors. State both explicitly, including PC and any flag or link effects.

Some branches compare registers directly; others consume flags or predicates produced earlier. Hidden condition state belongs in the architectural read set.

### Compare equality conditions

Equality compares bit patterns of the declared width; signedness usually does not change equality. Width extension before comparison can still matter.

Branch-on-zero may be a distinct encoding or an alias using a constant register. These representations can share semantics without sharing bytes.

### Compare signed and unsigned order

The same bit vector can order differently under signed and unsigned interpretation. At eight bits, `0xff` is 255 unsigned and -1 signed.

Compilers choose conditions from source/IR types and transformations. Verification should pair boundary values around zero and the sign bit.

### Use flags and predicates

Flag-based branches read condition codes set by a previous instruction. Correctness depends on which intervening operations preserve or overwrite them.

Predicate-register branches make the dependency explicit. Both models require exact truth-table semantics and width for the producing comparison.

### Reconstruct branch displacements

Branch immediates can be scattered across encoding fields and scaled by instruction alignment. Sign extension occurs from the semantic immediate’s sign bit.

Distinguish encoded units, byte displacement and final target. Range checks apply before truncation during assembly or linking.

### Define the PC base

Architectures can use current instruction address, fall-through address or an aligned page base. Documentation must name it rather than saying “relative to PC.”

The same convention must appear in assembler fixups, relocations, veneers, executable models and processor target logic.

### Define indirect jumps

An indirect jump reads a register from pre-state, optionally adds an offset, applies address-width and normalization rules, then validates the target.

It supports switch tables, function pointers, dynamic linkage and returns. Because runtime data chooses the target, static range is broader and security validation harder.

### Normalize targets

Some ISAs clear low target bits or interpret mode bits in addresses. Others require all alignment bits already zero.

Normalization must precede or follow addition exactly as specified. Silently clearing extra bits can redirect invalid pointers into valid code.

### Define link semantics

A call-like jump writes a return address, commonly fall-through, to a link register or stack. The link destination may be explicit or implicit.

If link destination overlaps a target source, the target reads pre-state and the link writes post-state under ordinary transition semantics. Constant destinations can suppress the link.

### Distinguish calls from jumps

Some ISAs have dedicated call opcodes; others use a general jump-and-link with an ABI-selected link register. Architectural control transfer and calling convention are separate layers.

The ABI adds register preservation, stack, unwinding and return conventions. A jump with a link can be ISA-legal without forming an ABI-valid call.

### Distinguish returns

A return can be a dedicated instruction, an alias for an indirect jump, or a protected operation with shadow-stack semantics. Specify which level defines it.

Predictors may recognize ABI return patterns. Recognition affects performance, not the functional target, unless an architectural CFI mechanism also validates return state.

### Model switch dispatch

Compilers implement multiway branches with comparison trees, jump tables or ISA-specific table operations. A jump table turns an index into an indirect target.

Bounds checks and table entry interpretation must precede the transfer. Speculation can transiently bypass software checks, so security evidence includes mitigation behavior.

### Handle delay slots

In a delay-slot ISA, one or more architecturally defined instructions near a transfer execute regardless of the selected successor or under exact annul rules.

This is not the same as speculative fetch. Delay-slot effects are architectural and complicate exceptions, debugging, binary rewriting and compatibility.

### Validate target alignment

A target must identify a legal instruction boundary under the active profile. Compressed or mixed-length support can reduce required alignment.

Misalignment behavior must be attributed to the correct transfer or fetch boundary. Wrong-path fetch artifacts cannot replace the required precise exception.

### Enforce execute permission

Target formation does not authorize instruction fetch. Address translation and execute permission determine whether the selected successor can execute.

Architectures define whether a transfer commits before a subsequent instruction-fetch fault is reported. Trace schemas should distinguish transfer resolution from target fetch.

### Include privilege transfers

Trap entry and return change PC plus privilege, status and often translation context. They are control transfers with larger architectural write sets.

Return-from-exception instructions validate saved mode and status. They are not interchangeable with ordinary indirect returns.

### Preserve precise exceptions

If a control-flow instruction itself is illegal, misaligned or violates CFI, ordinary link and PC effects follow the architecture’s fault rule. Saved faulting address and cause must be exact.

If the target fetch faults afterward, earlier architecturally completed effects may differ. Distinguish these exception points.

### Build compiler CFGs

A compiler basic block ends at a terminator. Conditional branches have multiple successors; returns and traps have no ordinary successor; indirect branches need an allowed destination set.

Optimizations preserve observable behavior while reshaping the graph. Undefined source behavior and IR constraints must not be confused with ISA target permission.

### Resolve linker ranges

Final layout determines whether a direct displacement reaches. A linker can insert a veneer/thunk or select a longer sequence when it does not.

Relocation overflow must not truncate. Relaxation and thunk insertion update debug, unwind and exception metadata as well as branch bytes.

### Understand branch prediction

Direction predictors guess taken/not-taken. Target buffers guess destination. Return-address stacks specialize common call/return patterns.

These structures improve fetch continuity. Their state and mistakes ordinarily do not alter the architectural condition or target.

### Recover from misprediction

When resolution differs from prediction, younger wrong-path operations are squashed and fetch restarts at the correct successor. Rename, queue and memory-order state must recover coherently.

No wrong-path register or store may commit. Microarchitectural caches or predictors may still change, creating separate side-channel concerns.

### Retire control flow

Commit traces should record instruction PC, length, branch kind, condition result, resolved target, fall-through, link write and exception. Indirect targets deserve full values.

Retirement order establishes the architectural path even if execution resolved branches out of order. Trace loss near flushes is itself a verification risk.

### Apply static prediction hints

Some encodings or profiles expose hints. A hint may guide performance while remaining functionally ignorable.

Do not make correctness depend on a predictor honoring it. Measure benefit and energy on representative code separately from ISA conformance.

### Enforce software CFI

Software CFI inserts checks so indirect transfers target approved sets. Precision depends on the computed control-flow policy and protected metadata.

An overbroad set stops fewer attacks; an incomplete set breaks valid execution. Compiler, linker, loader and runtime transformations must preserve instrumentation.

### Enforce architectural CFI

ISA support can mark valid landing pads, protect return state or restrict indirect transfers. It needs discovery, exception, privilege and compatibility rules.

Hardware enforcement does not automatically cover every edge or data-only attack. State the protected transfer classes and threat model.

### Use shadow stacks carefully

A shadow stack protects return addresses in storage separate from the ordinary stack. Calls and returns update/check it under controlled access.

Tail calls, exceptions, signals, context switches and unwinding need defined integration. A branch predictor return stack is not a security shadow stack.

### Analyze speculation security

Prediction can transiently execute wrong-path instructions using secret-dependent data. Architectural rollback does not erase every timing footprint.

Mitigations include speculation barriers, target restrictions, predictor isolation and software transformations. Verify functional behavior and leakage claims separately.

### Verify the branch unit

Test all condition truth tables, signed boundaries, equal operands, displacement extrema, instruction lengths, target wrap, alignment and source/link overlap.

Compare independent semantic models, assembled relocations, RTL resolution and commit traces. Force mispredictions and exceptions to prove wrong-path suppression.

### Govern control-flow changes

New control instructions consume encoding space and interact with compilers, unwinders, debuggers, virtualization and CFI. Freeze version and discovery before deployment.

Track specifications, opcode tables, toolchain, binary, model, predictor/RTL, silicon and errata. A microcode workaround does not erase revision-specific evidence.

## Definitions and Notation

- `PC`: architectural address of the current instruction.
- `L`: decoded instruction length in bytes.
- `F=PC+L`: sequential fall-through under address-width rules.
- `C(S)`: architectural branch predicate evaluated from pre-state `S`.
- `D`: reconstructed, extended and scaled direct displacement.
- `T`: resolved direct or indirect target.
- `B(PC)`: architecture-defined base for a relative target.
- `R`: pre-state register value used by an indirect transfer.
- `N(x)`: architecture-defined target normalization.
- `link`: return address written by a call-like transfer.
- `taken`: boolean selecting target rather than fall-through.
- `CFG=(V,E)`: static control-flow graph of blocks and possible edges.
- `trace`: committed sequence of instruction addresses and effects.
- `predict`: microarchitectural direction/target guess.
- `flush`: recovery action that discards younger wrong-path state.

Unless stated otherwise, addresses are byte addresses and comparisons operate on the instruction-declared fixed width.

## Mechanisms, Invariants, or Proof Structure

1. **Length obligation:** prove fall-through uses the actual decoded instruction length and address-width rule.
2. **Condition obligation:** prove every branch predicate uses the exact sources, widths, flags and signedness.
3. **Displacement obligation:** prove direct fragments, sign extension, scaling and PC base reconstruct the intended target.
4. **Indirect obligation:** prove register source, offset, address width and normalization produce the defined indirect target.
5. **Link obligation:** prove calls write the exact fall-through/link value to the permitted destination using pre-state target operands.
6. **Alignment obligation:** prove target alignment and instruction-boundary rules for every supported length/profile.
7. **Permission obligation:** prove target translation, executable permission, privilege and CFI checks cannot be bypassed architecturally.
8. **Exception obligation:** prove transfer faults and target-fetch faults expose their distinct permitted PC, link and trap state.
9. **Delay obligation:** prove every architectural delay-slot/annul rule or absence thereof.
10. **Relocation obligation:** prove linker range checks, thunks and relaxation preserve target and link semantics.
11. **CFG obligation:** prove compiler direct and indirect successors cover defined source/IR behavior and generated targets.
12. **Recovery obligation:** prove misprediction flush restores rename, queue, memory and fetch state without wrong-path commit.
13. **Retirement obligation:** prove committed control-flow traces follow resolved ISA successors in permitted order.
14. **Security obligation:** prove claimed CFI/shadow-stack/speculation controls cover their named edge classes and threat model.
15. **Evidence obligation:** bind specification, compiler, linker, binary, model, RTL, hardware, configuration and errata versions.

## Alternatives and Trade-Offs

1. **Direct versus indirect transfer:** direct edges are compact and analyzable; indirect edges support dynamic dispatch.
2. **PC-relative versus absolute target:** relative code relocates well; absolute forms can reach fixed locations directly.
3. **Short versus long displacement:** short fields improve density; long fields reduce veneers.
4. **Register compare versus flags:** direct compares expose sources; flags reuse condition state and encode compactly.
5. **Signed versus unsigned branches:** distinct conditions preserve type meaning but consume decode/encoding capacity.
6. **Link register versus link stack:** registers simplify ISA state; stacks can protect/nest returns with more machinery.
7. **Dedicated call/return versus aliases:** dedicated forms aid decode/protection; aliases conserve opcode space.
8. **Delay slots versus immediate transfer:** slots expose pipeline timing; no slots simplify portable scheduling.
9. **Strict versus relaxed alignment:** strict alignment simplifies fetch; mixed-length support improves density.
10. **Static versus dynamic prediction:** static policy is simple; dynamic learning improves common performance.
11. **Small versus large predictors:** small structures save area/energy; large histories improve accuracy.
12. **Early versus late resolution:** early resolution limits wrong path; late resolution may enable higher frequency/richer conditions.
13. **Precise versus coarse CFI:** precise sets block more invalid edges; coarse sets reduce metadata and compatibility burden.
14. **Software versus hardware CFI:** software is deployable/flexible; hardware can protect metadata and enforce lower-level rules.
15. **Speculation versus conservative execution:** speculation raises throughput; restraint reduces recovery and leakage exposure.

## Failure Modes and Misconceptions

1. “Every instruction’s fall-through is PC+4.” Length can vary.
2. “A branch has only a taken effect.” Not-taken state is equally architectural.
3. “Equality needs signedness.” Bit-pattern equality usually does not, though width does.
4. “Signed and unsigned less-than are interchangeable.” Sign-bit values reverse order.
5. “Branch syntax lists every source.” Flags or predicates may be implicit.
6. “A displacement is always a byte count in the encoding.” It can be scaled.
7. “PC-relative means relative to the next instruction.” The ISA defines the base.
8. “Assembler range checks make hardware target verification unnecessary.” Raw bytes still reach hardware.
9. “An indirect target is just the register value.” Offset, width and normalization may apply.
10. “Clearing any low bits is safe.” Only specified normalization is permitted.
11. “A call stores its target as the return address.” Link normally records fall-through.
12. “Calls and returns are purely ISA concepts.” ABI roles often distinguish general jumps.
13. “A return-address predictor validates returns.” It predicts; it does not enforce authority.
14. “Delay slots are speculative instructions.” Their effects are architectural.
15. “Compressed support changes only code size.” It changes boundaries and alignment.
16. “A selected target is automatically executable.” Translation and permissions still apply.
17. “Target misalignment and target-fetch fault are the same event.” Cause and architectural timing can differ.
18. “Trap return is an ordinary indirect jump.” It restores privileged state.
19. “A compiler CFG lists every runtime edge automatically.” Indirect edges require explicit allowed sets/analysis.
20. “Relocation overflow can wrap.” It silently redirects execution.
21. “A veneer is semantically invisible in every tool.” Unwind, debug and security metadata must include it.
22. “Prediction changes the branch condition.” It only guesses before resolution.
23. “Squashing registers proves wrong-path safety.” Stores, queues, predictors and caches also matter.
24. “Architectural rollback removes every side channel.” Microarchitectural footprints can remain.
25. “Landing pads protect all control flow.” They cover only specified transfer classes/policies.
26. “Passing branch tests proves control-flow correctness.” Exceptions, recovery, indirect edges and security remain.

## Worked Examples

### Example 1

A 16-bit instruction at `PC=0x100` has fall-through `0x102`; assuming `0x104` skips a legal instruction boundary.

### Example 2

At eight bits, signed `0xff < 0x01` is true because `-1<1`; unsigned `255<1` is false.

### Example 3

A branch at PC 16 with byte displacement `-8` selects PC 8 when its condition is true and PC 20 when its 4-byte fall-through is selected.

### Example 4

A jump at PC 20 with displacement 8 selects target 28 and writes link 24 to its nonconstant destination.

### Example 5

An indirect jump at PC 32 reads pre-state `x4=36`, selects target 36 and suppresses a requested link write to constant `x0`.

### Example 6

If an indirect form requires clearing target bit zero, register value `0x1001` normalizes to `0x1000`; it must not clear additional bits without specification.

### Example 7

A direct branch just outside signed displacement reach requires a longer sequence or linker veneer, not low-bit truncation.

### Example 8

A taken transfer to a nonexecutable mapped page can resolve correctly yet cause an instruction-fetch permission fault at the architectural boundary.

### Example 9

A predicted-taken branch that resolves not-taken flushes wrong-path operations and commits fall-through; predictor/cache traces require separate security analysis.

### Example 10

A shadow stack compares the architectural return target with protected call history; a predictor return stack merely guesses the target to reduce latency.

## Cross-Program Connections

- **Instruction encoding:** displacement fields, lengths and function bits define transfer forms.
- **Addressing modes:** direct and indirect targets reuse width, base, extension and alignment rules.
- **Calling conventions:** link registers, stacks, tail calls and returns structure procedures.
- **Compilers:** CFGs, terminators, switches and indirect-edge metadata lower into transfers.
- **Linkers:** relocations, relaxation and veneers make final targets reachable.
- **Pipelines:** prediction, resolution, flush and retirement manage control hazards.
- **Operating systems:** traps and privilege returns alter PC plus protected state.
- **Formal methods:** successor relations and commit traces support refinement proofs.
- **Security:** CFI, shadow stacks and speculation controls protect dynamic targets.
- **Systems engineering:** versions, configurations, binaries and errata bound assurance.

## References

1. RISC-V International, [RV32I Base Integer Instruction Set](https://docs.riscv.org/reference/isa/unpriv/rv32.html), conditional branches, jumps, link semantics, target alignment and PC-relative control flow; retrieved 2026-09-04.
2. RISC-V International, [C Extension for Compressed Instructions](https://docs.riscv.org/reference/isa/unpriv/c-st-ext.html), compact control transfers, mixed instruction lengths and alignment; retrieved 2026-09-04.
3. RISC-V International, [Control-Flow Integrity Repository](https://github.com/riscv/riscv-cfi), landing-pad and shadow-stack ISA development and specifications; retrieved 2026-09-04.
4. Arm, [Arm Architecture Reference Manual for A-profile Architecture](https://developer.arm.com/documentation/ddi0487/latest/), direct, conditional, indirect, call, return and exception-control semantics; retrieved 2026-09-04.
5. Intel, [Intel 64 and IA-32 Architectures Software Developer's Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), jumps, calls, returns, conditions, indirect control and protection mechanisms; retrieved 2026-09-04.
6. LLVM Project, [Terminator Instructions](https://llvm.org/docs/LangRef.html#terminator-instructions), compiler IR branches, switches, indirect branches, calls and returns; retrieved 2026-09-04.
7. WebAssembly Community Group, [Control Instructions](https://webassembly.github.io/spec/core/exec/instructions.html#control-instructions), structured branches, calls, returns and traps in a typed virtual ISA; retrieved 2026-09-04.
8. RISC-V International, [Sail RISC-V Model](https://github.com/riscv/sail-riscv), executable control-transfer semantics for differential and refinement evidence; retrieved 2026-09-04.

## Exercises

### Exercise 1

Specify next-PC and write sets for sequential execution, conditional branch, direct jump-and-link, indirect jump-and-link, trap entry and trap return.

### Exercise 2

Trace a two-iteration loop followed by direct and indirect jumps, recording resolved control-flow events, link state and final registers.

### Exercise 3

Design boundary tests for signed/unsigned branch conditions, variable instruction lengths, displacement limits, target alignment and source/link overlap.

### Exercise 4

Explain and verify compiler/linker lowering of a large switch whose jump table and distant targets require relocation and possible veneers.

### Exercise 5

Construct assurance for indirect-branch landing pads and a shadow stack in an out-of-order processor and operating-system ecosystem.

## Answers to the Exercises

### Answer 1

Sequential execution writes the ordinary instruction destinations and `PC=PC+L`. A conditional branch reads condition sources and writes either target or fall-through PC. Direct jump-and-link derives target from the defined PC base and writes fall-through to link plus target to PC. Indirect jump-and-link reads its target source from pre-state, adds/normalizes, then writes link and PC.

Trap entry writes cause, saved PC, privilege/status and handler PC according to the privileged architecture, suppressing ordinary effects as specified. Trap return validates saved state, restores privilege/status and selects saved resume PC. Frame conditions keep all other architectural locations unchanged.

### Answer 2

The trace below prints resolved control transfers only. Ordinary arithmetic establishes loop values and the indirect target.

<!-- bijux-verify: {"id":"control-flow-resolution-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"branch pc=16 lhs=1 rhs=0 taken=true target=8\nbranch pc=16 lhs=0 rhs=0 taken=false target=20\njump pc=20 link=x3 value=24 target=28\nindirect pc=32 base=x4 value=36 target=36 link=x0 suppressed=true\nfinal_pc=36 x1=0 x2=2 x3=24 x4=36\n"}} -->
```python
registers = [0] * 8
pc = 0

while pc != 36:
    if pc == 0:
        registers[1] = 2
        pc = 4
    elif pc == 4:
        registers[2] = 0
        pc = 8
    elif pc == 8:
        registers[2] += 1
        pc = 12
    elif pc == 12:
        registers[1] -= 1
        pc = 16
    elif pc == 16:
        taken = registers[1] != 0
        target = 8 if taken else 20
        print(
            f"branch pc=16 lhs={registers[1]} rhs=0 "
            f"taken={str(taken).lower()} target={target}"
        )
        pc = target
    elif pc == 20:
        registers[3] = 24
        print("jump pc=20 link=x3 value=24 target=28")
        pc = 28
    elif pc == 28:
        registers[4] = 36
        pc = 32
    elif pc == 32:
        target = registers[4] & ~1
        print(
            f"indirect pc=32 base=x4 value={registers[4]} target={target} "
            "link=x0 suppressed=true"
        )
        pc = target

print(
    f"final_pc={pc} x1={registers[1]} x2={registers[2]} "
    f"x3={registers[3]} x4={registers[4]}"
)
```

This toy proves four resolved events and final scalar values only. It omits encoding, relocation, translation, traps, prediction timing, CFI and hardware.

### Answer 3

For each comparison width, pair zero, one, all-ones, signed minimum and maximum; run equal and unequal operands through equality, signed and unsigned order conditions. Exercise minimum/maximum taken displacements, one step outside each range, forward/backward zero-adjacent offsets and arithmetic wrap.

Mix every supported instruction length at source and target, valid and invalid target alignments, executable and nonexecutable pages, and source/link equality including constant link destinations. Force direction and target mispredictions, target-fetch faults and transfer faults. Compare semantic-model, RTL resolution and retirement records.

### Answer 4

Prove the source/IR switch range and default edge. Bounds-check the table index before loading an entry; define whether entries hold absolute addresses or signed PC-relative offsets and their width. Ensure every table target is a legal CFG destination and instruction boundary.

The linker resolves table and branch relocations, inserts veneers for out-of-range direct edges, and updates debug/unwind/exception and CFI metadata. Test layouts at reach boundaries, section movement, relaxation on/off and address randomization. Compare object relocations, linked bytes, CFG metadata and runtime committed targets using exact tool and binary versions.

### Answer 5

Define protected indirect classes, valid landing-pad state, shadow-stack storage and access authority, call/return updates, tail calls, exceptions, signals, context switches, virtualization, debug and failure traps. State discovery and compatibility for software that lacks the extension.

Verify compiler instrumentation and linker preservation, loader permissions, OS/hypervisor context handling, and processor decode/commit. Attack missing/wrong landing pads, return mismatch, stack overflow/underflow, async interruption, speculation, cross-process/guest state and rollback. Preserve threat model, binaries, metadata, traces, configurations, RTL and silicon revisions. Named ISA, compiler, linker, OS, hypervisor, RTL, formal, security, verification and independent-assurance reviewers assess their scopes. This module supplies no certification.
