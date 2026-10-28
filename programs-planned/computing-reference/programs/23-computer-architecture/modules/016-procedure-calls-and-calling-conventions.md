---
module_id: CA-016
program: Computer Architecture
level: 1
module_number: 16
title: Procedure Calls and Calling Conventions
status: complete
last_verified: 2026-09-04
---

# Procedure Calls and Calling Conventions

## One-Page Review

### Governing question

How do ISA control-transfer mechanisms and an ABI calling convention combine so independently compiled functions agree on arguments, results, registers, stacks, return state, unwinding and exceptional crossings?

### Essential definitions

- A **procedure call** transfers control while preserving enough state to resume at a return address.
- A **calling convention** defines how callers and callees exchange values and divide preservation duties.
- An **ABI** is the broader binary contract covering calling convention, data layout, object format, relocation and related interfaces.
- An **argument register** carries a parameter at function entry; a **result register** carries a return value.
- A **caller-saved** register may be clobbered by a call, so a caller preserves any live value it needs.
- A **callee-saved** register must be restored by a conforming callee before returning if the callee changes it.
- A **stack pointer** identifies the active stack boundary under exact alignment and growth rules.
- A **stack frame** is storage associated with one invocation for saved state, locals, spills and outgoing arguments.
- A **frame pointer** is an optional stable reference within a frame.
- A **return address** identifies the caller continuation, held in a link register, stack entry or protected state.
- A **prologue** establishes callee state; an **epilogue** restores it and returns.
- A **leaf function** makes no further calls; a **non-leaf function** may need to preserve return state.
- A **variadic function** accepts arguments beyond a statically fixed parameter list under additional layout rules.
- A **tail call** transfers to another function without retaining the current frame when ABI conditions permit.
- **unwind information** describes how to recover caller state at program points for exceptions, debugging or profiling.

### Central model, mechanism, or theorem

Let ABI-visible call state be

`C = (PC, SP, registers, stack_memory, return_state, abi_context)`.

A conforming caller marshals arguments and establishes required stack alignment before an ISA call transfer. A conforming callee may change caller-saved state and its owned frame, but on normal return it restores every callee-saved location and stack invariant, places results in defined locations and transfers to the saved return address. Composition holds when caller and callee use the same ABI variant, type classification and feature set.

### Critical invariants

- Call target and return-address mechanics follow the ISA; argument and preservation roles follow the selected ABI.
- Stack pointer alignment and owned memory regions hold at every ABI-defined boundary.
- Caller-saved and callee-saved obligations cover every active register class, not only integers.
- Arguments and results use exact type classification, width, extension, aggregate and hidden-parameter rules.
- Return state is preserved across nested calls, interrupts, exceptions and unwinding as specified.
- Prologue/epilogue operations have matching frame sizes, offsets and restore paths.
- Tail calls, variadic calls, dynamic stack allocation and foreign interfaces satisfy their extra constraints.
- Unwind metadata and generated code describe the same machine state transitions.

### Common failures

Frequent failures are calling a jump-and-link instruction a complete calling convention, assuming register names imply ABI roles, entering a call with a misaligned stack, treating every register as caller-saved, forgetting vector or predicate preservation, saving the return address after overwriting it with a nested call, using mismatched aggregate classification, reading variadic arguments as ordinary fixed arguments, returning a large object without its hidden pointer, applying a red-zone rule in an interrupt context where it is unavailable, tail-calling with a live incompatible frame, hand-writing assembly without unwind metadata, and mixing ABI variants that use the same ISA.

### Compact example

Suppose a 64-bit ABI passes two integers in `a0=7` and `a1=5`, requires 16-byte stack alignment and gives a non-leaf callee a 32-byte frame. From `SP=0x1000`, the prologue sets `SP=0x0fe0`, saves return address `0x0104` at `SP+24` and old frame register at `SP+16`, then establishes a frame reference. The body returns `12` in `a0`; the epilogue restores saved state and `SP=0x1000`, then transfers to `0x0104`.

### Connections

Calling conventions connect control flow, register allocation, stack memory, compilers, linkers, exceptions, debuggers, security, foreign-function interfaces, operating systems and binary compatibility.

## Governing Question

The ISA supplies jumps, link registers, loads and stores. It does not ordinarily decide which register carries the first integer argument, which registers survive, or how a structure is returned. Those are ABI decisions.

The governing question is how the layers compose. A correct call requires legal ISA effects and shared ABI expectations. Either layer can fail independently: a processor can execute a call perfectly while two object files disagree on parameter layout.

## Why This Matters

Calling conventions make separate compilation possible. Compilers, hand-written assembly, libraries, runtimes, debuggers and kernels can interoperate without knowing one another’s internal implementation.

Small violations create delayed corruption. A callee-saved register restored from the wrong offset may fail only under optimization. Stack misalignment may surface only in a vector instruction. Inaccurate unwind metadata can make normal execution pass while exception handling fails.

Security mechanisms also depend on call structure. Stack canaries protect frame data, shadow stacks protect return state, pointer authentication binds return addresses, and CFI restricts indirect calls. Each needs precise ABI and ISA integration.

## Prerequisites and Retrieval

Before studying this module, be able to:

- trace direct and indirect call/return control transfers;
- distinguish architectural register semantics from ABI aliases;
- compute aligned stack addresses and fixed-width offsets;
- explain object files, linking and exceptions conceptually;
- read simple compiler-generated assembly.

Retrieve ISA/profile/version; ABI name/version/variant; data model; register-role table for integer, floating, vector and predicate state; argument/result classification algorithm; stack direction and alignment; entry stack state; frame layout; caller/callee preservation; link/return mechanism; aggregate and hidden-result rules; variadic rules; red zone or home area; dynamic alignment; tail-call rules; thread/local context; unwind format; exception personality; signal/interrupt boundary; system-call convention; FFI mappings; security extensions; compiler options; object attributes; disassembly; tests; errata; and exact tool/runtime/hardware versions.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish ISA call mechanics from ABI calling conventions;
2. classify argument, result, caller-saved and callee-saved locations;
3. construct and unwind a correctly aligned stack frame;
4. explain leaf, non-leaf, frame-pointer and return-address choices;
5. reason about scalar, aggregate, floating, vector and variadic arguments;
6. analyze tail calls, dynamic stack allocation and red-zone constraints;
7. connect compiler register allocation and linker stubs to ABI rules;
8. validate unwind metadata against prologue/epilogue machine state;
9. assess return protection, CFI and cross-domain call boundaries;
10. build evidence for ABI interoperability and compatibility.

## Core Exposition

### Separate ISA and ABI

An ISA instruction can write a link register and select a target. The ABI assigns that register a return role and specifies everything surrounding the transfer.

Never infer a calling convention solely from instruction mnemonics. One ISA can host multiple ABIs, data models and operating-system conventions.

### Define the call boundary

State what must be true immediately before transfer and at callee entry: argument locations, stack pointer, alignment, return state and special context.

The callee can then rely on those preconditions. The caller can rely on the documented postconditions when control returns normally.

### Assign argument registers

ABIs commonly allocate early scalar arguments to registers and overflow arguments to a stack area. Separate integer, floating and vector banks may have distinct assignment sequences.

Assignment is positional only after type classification. A wide or aggregate argument can consume multiple slots, require alignment or force later values to memory.

### Assign result locations

Small scalar results often use one register; pairs or small aggregates can use several. Large or irregular objects may use a caller-provided result buffer addressed by a hidden argument.

Define whether the hidden pointer also returns in a register. Call declarations, code generation and debug types must agree.

### Classify types

The ABI maps source-level types into machine classes and locations. Integer width/extension, floating format, homogeneous aggregates, vectors and capabilities need exact rules.

Classification operates on ABI data layout, not a compiler’s private structure representation. Cross-language calls require compatible declared layouts.

### Define caller-saved state

A caller assumes caller-saved registers may change across a call. It spills or moves live values before the transfer when necessary.

This allocation gives callees temporary storage without mandatory saves. Calls therefore create interference points for compiler register allocation.

### Define callee-saved state

A callee that modifies callee-saved state records the old values and restores them along every returning path. It may omit saves for untouched registers.

Preservation is value equality at the ABI boundary, not a requirement to use a particular stack slot or instruction sequence.

### Cover every register class

Floating-point, vector, predicate, capability and control state may be caller-saved, callee-saved or conditionally preserved. Feature variants can change obligations.

Hand-written code that saves only integer state can corrupt programs when optional classes are active. Object attributes and build options must identify the variant.

### Manage the return address

The ISA may place fall-through in a link register or push it to a stack. A leaf can often leave link state untouched; a non-leaf must preserve its caller’s return state before another call overwrites it.

Exceptions and signals also need recoverable return state. Protected return mechanisms add shadow or authenticated state without removing the ordinary ABI contract.

### Establish stack direction

Most contemporary ABIs use a descending stack, but direction is a contract rather than a theorem. Define what `SP` points to before and after allocation.

Frame diagrams should label increasing addresses. Phrases such as “above the stack pointer” are otherwise ambiguous.

### Enforce stack alignment

An ABI can require `SP mod A=0` at call boundaries and stricter alignment for local objects. Subtract a frame size that preserves the required congruence.

Dynamic alignment may save the original pointer before rounding down. The epilogue must restore from reliable frame state rather than guessing the allocation size.

### Own frame memory

After allocation, a callee owns defined frame bytes for saved registers, locals, spills and outgoing arguments. It must not overwrite caller data or guard pages.

Fixed offsets should derive from one reviewed layout. Prologue code, unwind metadata, sanitizers and debuggers must share it.

### Use a frame pointer selectively

A frame pointer provides a stable base when `SP` moves because of dynamic allocation or outgoing arguments. It also simplifies some unwinding and debugging.

Omitting it frees a register and can shorten prologues. Reliable unwind tables can describe stack-pointer-relative frames without a permanent frame register.

### Design leaf functions

A leaf function makes no calls and may need no frame if arguments, temporaries and results fit in volatile registers. It still obeys stack and preservation rules.

Interruptibility, instrumentation or security policy can require a frame or protected return update even for leaves. “Leaf” is not equivalent to “no prologue.”

### Design non-leaf functions

A non-leaf protects its incoming return address and any used callee-saved registers before nested calls can clobber them. It also prepares outgoing arguments.

Shrink-wrapping may delay saves until a path needs them. Every execution path and unwind point must still have accurate state descriptions.

### Pass stack arguments

Arguments beyond register capacity occupy ABI-defined stack slots with exact alignment and padding. Some conventions reserve a caller-provided home area even for register arguments.

The callee’s frame allocation changes `SP`, so entry-stack arguments may use a frame pointer or adjusted offsets. Mixing entry and current `SP` bases is a common bug.

### Handle aggregate values

An aggregate may be split into register classes, passed by value in memory or replaced with a pointer to caller-owned storage. Size, alignment and field types drive classification.

Padding bytes may be unspecified and should not be treated as semantic data. Cross-language interfaces need stable representation or explicit serialization.

### Handle variadic calls

Variadic callees cannot derive unnamed argument types from the fixed signature. The ABI defines register save areas, class counters and `va_list` traversal.

Default argument promotions and named-versus-unnamed classification matter. Calling a variadic function with an incompatible prototype is not repaired by identical low bits.

### Support dynamic stack allocation

Runtime-sized objects move `SP` by a value rounded for alignment. A stable base or saved original pointer supports restoration and fixed-slot access.

Check stack limits before large movement and account for probing requirements. Skipping guard pages with one subtraction can bypass stack-growth protection.

### Understand red zones

A red zone is ABI-permitted storage adjacent to `SP` that a leaf may use without allocation. Its size and asynchronous-clobber rules are environment-specific.

Kernel, interrupt or signal contexts may forbid it. Code-generation options must match the execution environment.

### Perform tail calls

A tail call reuses or removes the current frame and transfers without needing to return to the current function. Argument locations, stack cleanup and preservation must be compatible.

The caller’s return state becomes the callee’s. Security metadata, unwind state and language semantics can restrict the optimization.

### Support recursion

Each recursive invocation needs distinct live frame state unless optimization eliminates the call. Return addresses, locals and saved values cannot share one writable frame accidentally.

Stack exhaustion becomes a systems concern. Bounds, guard pages and failure behavior must be defined for the environment.

### Link external calls

Position-independent binaries may call through procedure linkage stubs and global-offset structures. The linker/loader resolves symbols while preserving ABI-visible argument and return state.

Lazy binding introduces a resolver call on a first path. Resolver stubs must preserve all state promised by the ABI at that point.

### Cross shared-library boundaries

Symbol version, visibility, interposition and data model affect binary calls. Two functions with matching source names can still have incompatible binary signatures.

Compatibility tests should use independently built caller and callee objects, not a single compiler invocation that can optimize the boundary away.

### Build foreign-function interfaces

An FFI translates language types, ownership, exceptions and runtime context into ABI calls. Trampolines may adapt closures, callbacks or managed stacks.

Pinning, garbage-collector safepoints and thread attachment can be as important as register placement. State the full runtime boundary.

### Distinguish system calls

System-call conventions assign numbers, arguments, results and error reporting for a privilege transition. They can differ from the user-space function ABI on the same ISA.

Kernel entry also changes privilege and protected state. Do not call an ordinary library wrapper’s convention the raw system-call ABI.

### Integrate exceptions

Language exceptions unwind frames using metadata and personality routines rather than normal epilogues. Each program point needs recoverable caller state.

Cleanup actions and catch selection add language/runtime contracts. ISA precise exceptions alone do not supply stack unwinding.

### Emit unwind information

Unwind records describe canonical frame address and where prior registers reside as code changes the frame. Instructions need accurate address ranges.

Validate prologue, body, shrink-wrapped paths, epilogues and asynchronous samples. Stale metadata can restore an attacker-controlled value as a return address.

### Support debugging and profiling

Debuggers reconstruct frames and arguments using ABI, unwind and debug-type information. Optimized values may move or disappear without violating the ABI.

Sampling profilers require unwindability at arbitrary PCs. Frame-pointer policies trade a register for simpler traversal; table-based unwinding needs trustworthy metadata.

### Protect return state

Stack canaries detect some frame overwrites before return. Shadow stacks separate return addresses; pointer authentication can bind them to context.

These mechanisms have different threat models. None automatically protects function pointers, non-return data or every exceptional control path.

### Enforce indirect-call CFI

CFI checks that an indirect call’s target belongs to an allowed type/edge set and begins with any required landing form. The function ABI still handles arguments.

Type erasure, casts, dynamic linking and callbacks shape policy precision. Compiler, linker, loader and hardware metadata must compose.

### Verify prologue and epilogue symmetry

Symbolically track `SP`, saved locations and register values across every path. Frame allocation and deallocation must cancel; each save must pair with the correct restore.

Inject calls, exceptions and early returns at relevant points. Compare machine state with unwind metadata and ABI postconditions.

### Test interoperability

Build a matrix of callers and callees across supported compilers, optimization levels, languages, ABIs and optional register features. Exercise scalars, aggregates, variadics and callbacks.

Record object attributes and prevent link-time optimization from erasing the boundary. Passing self-calls is weaker evidence than cross-tool calls.

### Govern ABI evolution

Changing register roles, stack layout or classification can break every existing binary while leaving ISA semantics unchanged. Introduce a new named ABI variant when compatibility cannot be preserved.

Bind specification, compiler flags, object attributes, libraries, unwinders, runtime, OS, binary and hardware features. Track errata and security mitigations without silently changing old contracts.

## Definitions and Notation

- `C`: ABI-visible call state.
- `SP_in`: stack pointer at callee entry.
- `SP_cur`: current stack pointer after allocation/alignment.
- `A`: required stack alignment in bytes.
- `F`: frame size in bytes.
- `RA`: architectural return address.
- `Args`: ordered source-language or IR argument values.
- `Loc(Args)`: ABI classification into registers and stack locations.
- `Ret`: result value or hidden-result storage.
- `CallerSaved`: locations the caller must preserve when live.
- `CalleeSaved`: locations a modifying callee must restore.
- `CFA`: canonical frame address used by unwind descriptions.
- `frame(pc)`: machine-state layout at instruction address `pc`.
- `call`: transfer establishing ABI entry state and return state.
- `return`: transfer reestablishing caller-visible postconditions.

Stack addresses in examples are byte addresses; the example stack descends toward smaller addresses.

## Mechanisms, Invariants, or Proof Structure

1. **Variant obligation:** prove caller, callee, linker and runtime select the same named ISA/ABI/data-model variant.
2. **Classification obligation:** prove every scalar, aggregate, vector and hidden argument/result maps to exact locations and extensions.
3. **Entry obligation:** prove target, return state, stack alignment and special context satisfy callee-entry preconditions.
4. **Caller obligation:** prove every live caller-saved value needed after the call is preserved by the caller.
5. **Callee obligation:** prove every modified callee-saved location is restored on every normal return.
6. **Frame obligation:** prove allocation, alignment, ownership, offsets and deallocation are internally consistent.
7. **Return obligation:** prove nested calls cannot destroy the caller continuation and return selects the correct target.
8. **Variadic obligation:** prove register-save areas, promotions and traversal match unnamed argument classes.
9. **Tail-call obligation:** prove argument, frame, preservation, return and security state permit frame reuse.
10. **Unwind obligation:** prove metadata reconstructs caller CFA, registers and return address at every covered PC.
11. **Exception obligation:** prove cleanup and unwinding preserve language/runtime and ABI state across nonlocal exits.
12. **Boundary obligation:** prove FFI, system-call, signal and privilege crossings use their distinct adapters/conventions.
13. **Security obligation:** prove canary, shadow-stack, authentication and CFI claims cover named state and paths.
14. **Interoperability obligation:** prove independent supported producers/consumers exchange boundary values correctly.
15. **Evidence obligation:** bind ABI spec, compiler flags, objects, link, libraries, unwind, runtime, OS and hardware versions.

## Alternatives and Trade-Offs

1. **Register versus stack arguments:** registers reduce common latency; stack slots scale and provide addressable storage.
2. **Many versus few argument registers:** many reduce traffic; few simplify context and reserve registers for allocation.
3. **Caller-saved versus callee-saved:** caller-save favors leaf callees; callee-save favors values live across many calls.
4. **Link register versus stack return:** link registers accelerate calls; stack return naturally supports nesting with memory cost.
5. **Frame pointer versus omission:** a frame pointer stabilizes access/unwind; omission frees a register.
6. **Fixed versus dynamic frames:** fixed offsets simplify tooling; dynamic allocation supports variable objects.
7. **Mandatory home area versus none:** home space simplifies spilling/variadics; omission saves stack bandwidth.
8. **Red zone versus explicit allocation:** red zones speed leaves; allocation is safer across asynchronous contexts.
9. **By-value versus by-reference aggregates:** by-value can use registers for small data; references bound copying and classification complexity.
10. **Unified versus separate register classes:** unification simplifies movement; separate classes exploit specialized hardware.
11. **Eager versus lazy optional-state save:** eager is simple; lazy reduces common cost but complicates ownership/security.
12. **Normal versus tail call:** normal calls preserve a frame for return; tail calls reduce depth and overhead.
13. **Frame-pointer versus table unwinding:** frame chains are simple but costly; tables are compact at runtime but metadata-sensitive.
14. **Software versus hardware return protection:** software is deployable; hardware can protect state more strongly.
15. **Stable ABI versus optimized private convention:** stability enables ecosystem interoperability; private conventions optimize closed boundaries.

## Failure Modes and Misconceptions

1. “The ISA defines the calling convention.” The ABI layers roles and layout on ISA mechanisms.
2. “A call instruction guarantees ABI-valid entry.” Caller preparation remains required.
3. “Register aliases are architectural semantics.” ABI names are conventions over architectural locations.
4. “All arguments are assigned by position alone.” Type classification and alignment intervene.
5. “A value passed in a register needs no stack rule.” Home areas, variadics or spills may require one.
6. “Caller-saved means a callee must clear it.” It may clobber it; the caller preserves live values.
7. “Callee-saved means a callee always saves it.” Only modification requires restoration.
8. “Integer preservation covers the entire context.” Floating, vector, predicate and capability state may matter.
9. “A leaf never needs a frame.” Locals, alignment, instrumentation or protection can require one.
10. “A non-leaf can keep incoming RA in the link register.” A nested call may overwrite it.
11. “Stack alignment matters only for performance.” Some instructions and ABIs require it for correctness.
12. “Subtracting any frame size preserves alignment.” The size must respect entry congruence.
13. “Frame offsets stay relative to current SP automatically.” Dynamic movement changes them.
14. “A frame pointer is required for unwinding.” Accurate tables can describe frameless code.
15. “Variadic arguments follow fixed-argument access.” Separate save areas and promotions apply.
16. “Matching structure size proves ABI compatibility.” Field classes, alignment and padding also matter.
17. “Large returns always use result registers.” Hidden result storage is common.
18. “A red zone is safe in every environment.” Interrupt/kernel policies can prohibit it.
19. “Tail calls are ordinary calls followed by returns.” They reuse return state and remove the current continuation.
20. “System calls use the user function ABI.” Their registers, errors and privilege transitions can differ.
21. “Precise hardware exceptions unwind language frames.” Runtime metadata and personality logic are required.
22. “Normal execution proves unwind metadata.” Exceptional and asynchronous PCs need direct tests.
23. “A return-address predictor protects returns.” It predicts rather than authorizes.
24. “A shadow stack protects function pointers.” Its primary scope is return state.
25. “Same-compiler tests prove interoperability.” Correlated producer/consumer bugs can agree.
26. “ABI changes are safe when the ISA is unchanged.” Existing binaries can still break completely.

## Worked Examples

### Example 1

With 16-byte alignment, entry `SP=0x1000` and frame size 32 yield `SP=0x0fe0`; both addresses are aligned.

### Example 2

A non-leaf saves incoming `RA=0x0104` at frame offset 24 before a nested call overwrites the architectural link register.

### Example 3

If `s0` is callee-saved and initially `0x2222`, a callee may use another value internally but must return `s0=0x2222`.

### Example 4

Arguments `a0=7` and `a1=5` enter in registers; returning their sum places `12` in result register `a0`.

### Example 5

A ninth scalar argument may occupy an entry-stack slot even though the callee later subtracts a frame; access must use the adjusted address.

### Example 6

A 24-byte aggregate can be passed indirectly through a hidden pointer while a 16-byte aggregate may be split across two registers under a specific ABI.

### Example 7

A variadic callee saves incoming argument registers to an ABI-defined area so `va_list` can traverse register and stack arguments consistently.

### Example 8

A tail call is legal only after restoring callee-saved state, removing the current frame and arranging outgoing arguments without destroying incoming stack data.

### Example 9

At a PC after saving `RA` but before saving `s0`, unwind metadata must describe those two values differently; one generic prologue rule is insufficient.

### Example 10

A C caller and Rust callee can interoperate when they select the same C ABI and compatible types; language-native conventions need not match.

## Cross-Program Connections

- **Control flow:** calls, indirect targets and returns supply the ISA transfer mechanism.
- **Registers:** ABI roles and preservation constrain compiler allocation across calls.
- **Memory:** stack frames, arguments and spills occupy governed address ranges.
- **Compilers:** type classification, prologues, tail calls and unwind emission lower language calls.
- **Linkers/loaders:** stubs, symbol resolution and object attributes preserve external calls.
- **Operating systems:** signals, system calls and context switching cross related but distinct conventions.
- **Debugging:** frame reconstruction uses ABI, unwind tables and type/location data.
- **Languages/runtimes:** exceptions, garbage collection and FFI extend the binary boundary.
- **Security:** canaries, shadow stacks, authentication and CFI protect call state.
- **Systems engineering:** versioned binaries, runtimes, tools and mitigations govern compatibility.

## References

1. RISC-V International, [ELF psABI](https://riscv-non-isa.github.io/riscv-elf-psabi-doc/), register convention, stack, argument passing, relocations and unwind integration; retrieved 2026-09-04.
2. RISC-V International, [Calling Convention Chapter](https://docs.riscv.org/reference/isa/unpriv/calling-convention.html), explanatory ISA/ABI calling-convention relationship; retrieved 2026-09-04.
3. Arm, [Procedure Call Standard for the Arm 64-bit Architecture](https://github.com/ARM-software/abi-aa/blob/main/aapcs64/aapcs64.rst), AArch64 arguments, results, registers, stack and variants; retrieved 2026-09-04.
4. x86-64 psABI Project, [System V x86-64 ABI](https://gitlab.com/x86-psABIs/x86-64-ABI), AMD64 calling, data representation, stack, objects and linking; retrieved 2026-09-04.
5. DWARF Standards Committee, [DWARF Version 5](https://dwarfstd.org/doc/DWARF5.pdf), call-frame information, canonical frame addresses and unwinding; retrieved 2026-09-04.
6. LLVM Project, [Calling Conventions](https://llvm.org/docs/LangRef.html#calling-conventions), IR call compatibility and target/runtime convention selection; retrieved 2026-09-04.
7. WebAssembly Community Group, [Function Calls](https://webassembly.github.io/spec/core/exec/instructions.html#function-calls), typed direct/indirect calls and return behavior in a virtual ISA; retrieved 2026-09-04.
8. Intel, [Intel 64 and IA-32 Architectures Software Developer's Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), call/return instruction mechanisms and protected control transfer; retrieved 2026-09-04.

## Exercises

### Exercise 1

Separate ISA, ABI, compiler, linker, runtime and OS responsibilities for a normal external function call and return.

### Exercise 2

Trace a 32-byte descending stack frame with two register arguments, saved return/frame state, result register and full epilogue restoration.

### Exercise 3

Classify a mix of integers, floating values, vectors, small/large structures and variadic arguments under one explicitly selected ABI.

### Exercise 4

Design verification for prologue, shrink-wrapped save, dynamic allocation, tail call, normal return and exception unwind paths.

### Exercise 5

Construct assurance for a cross-language plugin boundary using dynamic linking, callbacks, exceptions and return-address protection.

## Answers to the Exercises

### Answer 1

The ISA defines link-producing and indirect control transfers, registers, loads/stores and exceptions. The ABI assigns argument/result roles, preservation, stack layout, type classification and unwind format. The compiler lowers typed calls, allocates registers and emits prologue/epilogue plus metadata.

The assembler/linker encode relocations and resolve external targets, possibly through stubs; the loader binds dynamic symbols. The runtime handles language exceptions, TLS, GC or FFI adapters. The OS supplies address spaces, signals and system-call transitions. Successful composition requires the same variants and documented adapters at every changed convention.

### Answer 2

The model uses an aligned descending frame. It saves return and frame state before doing work, then restores both and deallocates exactly 32 bytes.

<!-- bijux-verify: {"id":"calling-convention-frame-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"entry sp=0x1000 a0=7 a1=5 ra=0x0104 s0=0x2222 aligned=true\nprologue sp=0x0fe0 save_ra=0x0ff8 save_s0=0x0ff0 fp=0x1000 aligned=true\nbody result_a0=12\nepilogue sp=0x1000 ra=0x0104 s0=0x2222 return_pc=0x0104 aligned=true\n"}} -->
```python
registers = {"sp": 0x1000, "a0": 7, "a1": 5, "ra": 0x104, "s0": 0x2222}
memory = {}

print(
    f"entry sp=0x{registers['sp']:04x} a0={registers['a0']} a1={registers['a1']} "
    f"ra=0x{registers['ra']:04x} s0=0x{registers['s0']:04x} "
    f"aligned={str(registers['sp'] % 16 == 0).lower()}"
)

registers["sp"] -= 32
memory[registers["sp"] + 24] = registers["ra"]
memory[registers["sp"] + 16] = registers["s0"]
registers["s0"] = registers["sp"] + 32
print(
    f"prologue sp=0x{registers['sp']:04x} save_ra=0x{registers['sp'] + 24:04x} "
    f"save_s0=0x{registers['sp'] + 16:04x} fp=0x{registers['s0']:04x} "
    f"aligned={str(registers['sp'] % 16 == 0).lower()}"
)

registers["a0"] += registers["a1"]
print(f"body result_a0={registers['a0']}")

registers["ra"] = memory[registers["sp"] + 24]
registers["s0"] = memory[registers["sp"] + 16]
registers["sp"] += 32
print(
    f"epilogue sp=0x{registers['sp']:04x} ra=0x{registers['ra']:04x} "
    f"s0=0x{registers['s0']:04x} return_pc=0x{registers['ra']:04x} "
    f"aligned={str(registers['sp'] % 16 == 0).lower()}"
)
```

This proves only one toy scalar frame trace. It provides no binary encoding, aggregate, variadic, unwind, exception, security or hardware evidence.

### Answer 3

Select and cite an ABI before classifying. Record each type’s size, alignment and ABI class, then advance the appropriate integer, floating/vector and stack allocators exactly as the algorithm states. Small aggregates may split into classes; large or unaligned aggregates may become indirect pointers. Results use their own classification, possibly a hidden buffer.

For variadic calls, apply default promotions and the ABI’s unnamed-argument rules; construct required register-save and overflow areas. Verify by independently compiled caller/callee pairs that hash received bytes and values, including boundary exhaustion of each register class and stack alignment.

### Answer 4

Symbolically track `SP`, CFA, RA, every modified callee-saved register and owned slot at each instruction range. Prove fixed allocation and deallocation cancel. For shrink wrapping, show metadata changes exactly where each save occurs. For dynamic allocation, preserve a stable restoration source.

Exercise each normal return, early return, tail call and exception at every unwind-visible PC. Compare an independent unwinder with live register/memory snapshots and compiler metadata. Inject nested calls and asynchronous samples. Include corrupted metadata/stack negative tests and exact build flags, objects and runtime versions.

### Answer 5

Freeze the exported ABI, data model, type/layout rules, ownership, callback lifetime, thread attachment and exception policy. Use explicit adapters where languages differ; prevent exceptions from crossing an unsupported boundary. Version symbols and validate loader resolution.

Build callers, callees and callbacks independently across supported compilers and optimization modes. Test aggregates, null/error values, reentrancy, unload, exceptions and asynchronous callbacks. Verify unwind and debug metadata through stubs. Enable and test CFI plus return protection across plugin transitions, including failure traps and legacy compatibility. Preserve headers, generated bindings, objects, binaries, loader maps, metadata and tool/runtime versions. Named language, ABI, compiler, linker/loader, runtime, security, testing and independent-assurance reviewers assess their scopes. This module supplies no certification.
