---
module_id: SYSP-001
program: Programming Languages: Systems Programming
level: 1
module_number: 1
title: From Source Text to Process Image
status: complete
last_verified: 2026-08-28
---

# From Source Text to Process Image

## One-Page Review

### Governing question

Which contracts and transformations turn separately written source modules into a running process whose machine instructions, data, libraries, startup state, and resources agree?

### Essential definitions

- A **translation unit** or compilation unit is source presented to one compiler invocation after language-defined preprocessing or expansion.
- An **object file** contains machine code or intermediate code, data, symbol information, relocation records, and metadata; it is not yet necessarily runnable.
- A **symbol** names a definition or reference for linking, subject to visibility and linkage rules.
- A **relocation** records a place whose encoded value depends on a final symbol address or load position.
- A **linker** combines input objects and libraries, resolves references, lays out output, and applies or preserves relocations.
- An **executable image file** is a static representation that a compatible loader can use to construct a process image.
- A **process image** is the running program's virtual address space and initial machine/process state, including mapped code and data, stack, arguments, environment, and inherited resources.
- An **ABI** is the binary contract for object format, calling convention, data layout, registers, relocation, and other interoperation details on a target.

### Central model, mechanism, or theorem

The durable pipeline is

$$
source\xrightarrow{compile}relocatable\ objects
\xrightarrow{link}executable/shared\ objects
\xrightarrow{load}process\ image
\xrightarrow{startup}language\ entry.
$$

For a typical relocation, the linker or dynamic loader computes an encoded value from symbol address (S), addend (A), and sometimes relocation place (P): absolute (S+A) or PC-relative (S+A-P). Correct execution requires agreement among compiler, linker, loader, libraries, target ABI, and operating system—not merely successful parsing.

### Critical invariants

- Source names, link symbols, file offsets, virtual addresses, and runtime objects are different namespaces.
- Every required external reference must resolve according to the platform's linkage rules.
- Relocation arithmetic and encoded width must match the target ABI.
- File sections organize linking information; loadable segments organize process mappings. They are not interchangeable.
- The executable entry point is startup code and need not be the source-level `main` function.
- Loading creates mappings and initial state; it does not copy every byte eagerly in every implementation.
- A successful `exec`-style replacement preserves selected process attributes while replacing the process image.

### Common failures

Typical failures are calling compilation and linking one step, assuming source files map one-to-one to memory pages, confusing sections with segments, treating virtual addresses as file offsets, expecting `main` to be the loader entry, ignoring target triples and ABIs, omitting runtime libraries, relying on accidental symbol visibility, and diagnosing a load-time library failure as a compiler bug.

### Compact example

`main.o` defines `main` and refers to `twice`; `math.o` defines `twice`. The linker builds one definition table, resolves `main.o`'s reference to `math.o`, places both code contributions in an executable segment, and relocates the call. The loader maps that segment, maps writable data separately, prepares startup state, and transfers control to the executable entry—not directly to the source line containing `main`.

### Connections

Retrieve [PLS-001's distinction between program text and execution](../../01-programming-languages-and-semantics/modules/001-programs-languages-and-observable-behavior.md). [SYSP-002](../ROADMAP.md) develops integer representation. Translation internals connect to [Compilers & Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md), process construction to [Operating Systems](../../22-operating-systems/ROADMAP.md), and calling conventions to [Computer Architecture](../../23-computer-architecture/ROADMAP.md).

## Governing Question

What has to agree between source code and the moment a processor begins executing the resulting process image?

“Build and run” compresses several authorities into one button. The language implementation parses, checks, and translates source. An assembler or code generator emits target instructions and relocatable data. A linker reconciles separately compiled units and libraries. An operating-system loader maps an executable representation. A runtime initializes the language environment before invoking application code. Each stage consumes one representation, produces another, and can fail for a different reason.

Systems programmers need this causal model because the boundaries are observable. Duplicate symbols are link failures, not type errors. A missing shared library is a load failure, not a compilation failure. A call can reach the wrong behavior when two sides disagree on the ABI even though both compiled. A process can start and fail before `main` because startup or dynamic initialization failed.

## Why This Matters

Low-level defects often live between tools. An object compiled for one architecture cannot be safely linked into another target. A struct layout compiled under incompatible options crosses a library boundary incorrectly. Stripping removes diagnostics needed after a crash. A dynamically loaded dependency changes without a matching compatibility policy. Build success therefore proves only that the selected tools accepted the selected inputs; it does not prove that deployment supplies the same compatible environment.

The pipeline also explains performance and security behavior. Loadable regions receive permissions derived from segment policy. Position-independent code supports placement at varying virtual addresses. Demand paging can defer physical reads. Symbol visibility affects interposition and attack surface. These mechanisms are target- and platform-conditioned, so the engineer must inspect the actual artifact rather than infer it from source layout.

## Prerequisites and Retrieval

You should understand source files, functions, hexadecimal notation, arrays, mappings, virtual memory at an introductory level, and the difference between a specification and an implementation. Retrieve these facts:

1. A name can be mapped to an address only after a namespace and representation are fixed.
2. Separate compilation hides final addresses from individual compiler invocations.
3. A file byte offset and a virtual address measure positions in different spaces.
4. A process is an operating-system execution context, not merely an executable file.
5. A contract failure can remain latent until independently produced components interact.

No assembly fluency is required. SYSP-010 later teaches inspection of generated assembly.

## Learning Objectives

After completing this module, you should be able to:

- name and order compilation, object generation, linking, loading, startup, and application entry;
- distinguish source, relocatable object, executable/shared object, and process image;
- explain symbol definition, reference, and resolution;
- calculate basic absolute and PC-relative relocations;
- distinguish sections from loadable segments;
- explain static versus dynamic dependency resolution at a foundational level;
- classify build-time, link-time, load-time, startup-time, and runtime failures;
- inspect an artifact using target-appropriate tools without treating one format as universal.

## Core Exposition

Source text first enters a language toolchain. Preprocessing, macro expansion, conditional compilation, generated source, or module resolution may change the effective compilation unit. The compiler front end parses and checks the language. Middle and back ends transform a checked representation and select target instructions. Toolchains may emit assembly, machine code, bytecode, or link-time intermediate representation; the conceptual output is still an input to later composition.

A **relocatable object** packages contributions for separate compilation. Code and read-only constants, writable initialized data, zero-initialized data, unwind information, symbols, relocations, and debug metadata commonly occupy distinct sections. Exact names and rules belong to the object format and target ABI. An object file can contain valid machine instructions yet remain non-runnable because addresses and dependencies are unresolved.

A symbol table relates names to definitions, references, scopes, and locations. A definition contributes storage or code; an undefined symbol requests a compatible definition elsewhere. The linker searches explicit objects and libraries under ordering and visibility rules, diagnoses prohibited duplicates or unresolved references, and decides which archive members or sections are retained.

Relocation bridges unknown addresses. When the compiler emits a call to an external function, it leaves a placeholder and relocation record describing how to encode the final displacement. If the symbol is known at static link time, the linker can apply it. If dynamic resolution is permitted, the output preserves metadata so a dynamic linker can finish or mediate binding at load or call time.

The **linker** also lays out the output. It merges compatible input sections, chooses addresses and alignment, synthesizes tables, selects an entry address, and writes program headers or analogous loading commands. A linker script or platform convention can control this mapping. Link-time optimization may allow the compiler and linker pipeline to exchange richer intermediate representations, but it does not erase the final ABI and loader contracts.

Sections answer “how is this file organized for linking, relocation, and tools?” Segments answer “which byte ranges become runtime mappings with which permissions and alignment?” Several sections can contribute to one segment, and some sections need not be loaded. A stripped executable may omit much debug information while preserving the segments needed to execute.

The **loader** validates the executable representation for the target, creates or replaces virtual memory mappings, establishes permissions, prepares stack and process parameters, arranges an interpreter or dynamic linker when required, and sets the initial instruction pointer. File-backed mappings can be demand paged; “loading” does not require eagerly copying the whole file into anonymous memory.

Dynamic linking maps shared objects and resolves runtime dependencies according to the platform's search and symbol rules. This can reduce duplication and permit library servicing, but it introduces deployment compatibility, search-path, initialization-order, and symbol-interposition concerns. Static linking resolves more dependencies into one artifact but does not make operating-system, kernel, configuration, or CPU requirements disappear.

The entry point normally belongs to startup code. Startup establishes the language runtime, turns process parameters into language-level arguments, initializes required state and constructors, invokes the application entry such as `main`, and translates its return or termination into process exit behavior. A process can therefore fail after loading but before application entry.

On POSIX systems, a successful `exec` family operation replaces the current process image rather than creating a new process. Selected attributes are inherited according to the standard; other state is reset or replaced. Creation is typically a separate operation or a combined spawn interface. This is one platform model, not the definition of process execution on every system.

## Definitions and Notation

For object module (O_i), let (D_i) be its exported definitions and (R_i) its unresolved references. A simplified link succeeds when every required reference has exactly one admissible definition under the platform's binding rules:

$$
\forall r\in\bigcup_i R_i,\quad |resolve(r,\bigcup_i D_i)|=1.
$$

Real formats include weak definitions, symbol versions, visibility, archive extraction, and interposition, so “exactly one” is the foundational case rather than a complete platform algorithm.

Let (S) be resolved symbol address, (A) an addend, and (P) the address of the relocation place. Two common relocation expressions are

$$
V_{abs}=S+A,
\qquad
V_{pc}=S+A-P.
$$

The ABI additionally specifies field width, signedness, overflow handling, instruction encoding, and when the expression is valid.

Represent a loadable segment by file interval ([o,o+n_f)), virtual interval ([v,v+n_m)), alignment (a), and permissions (p). Often $n_m\ge n_f$, allowing zero-filled memory beyond file-backed bytes. Validity requires format-specific alignment and range constraints.

## Mechanisms, Invariants, or Proof Structure

**Symbol completeness.** Every retained reference must resolve or have a permitted dynamic resolution route. A source declaration alone is not a definition.

**Relocation correctness.** Suppose a PC-relative target is at (S=0x1200), the relocation place is (P=0x1004), and (A=-4). Then

$$
S+A-P=0x1200-4-0x1004=0x1f8.
$$

The numerical result is usable only if it fits the relocation field and its architectural interpretation.

**Permission separation.** Code intended only for execution should not require writable mapping merely because source and data came from the same file. Segment construction is the relevant runtime boundary.

**ABI agreement.** Caller and callee must agree on argument placement, return values, preserved registers, stack alignment, data representation, and name/linkage rules. Separately successful compilation cannot repair a disagreement at the call boundary.

**Startup ordering.** Loader entry precedes runtime initialization, which precedes the application entry promised by the language environment. Diagnostics must identify the earliest failed stage.

**Artifact provenance.** Reproducible diagnosis records source revision, generated inputs, target, compiler, linker, flags, libraries, and resulting artifact identity. A filename alone is not enough to reconstruct the image.

## Alternatives and Trade-Offs

**Ahead-of-time versus just-in-time translation.** Ahead-of-time systems produce native artifacts before launch. JIT systems load bytecode or intermediate form and generate native code during execution. Both still have artifact, loader, runtime, target, and process-image boundaries.

**Static versus dynamic linking.** Static linking simplifies some deployment dependencies and enables whole-program decisions. Dynamic linking shares code and supports independent library deployment. Compatibility, licensing, patching, size, startup, and interposition policies shape the choice.

**Position-dependent versus position-independent code.** Fixed placement can simplify some encodings. Position-independent code supports flexible mapping and shared objects, at possible target-specific instruction or indirection costs. Measure the actual target.

**Debug-rich versus stripped artifacts.** Debug sections improve postmortem analysis and source correlation but enlarge artifacts and may reveal details. Production pipelines commonly separate deployable files from access-controlled matching symbols.

**One-step driver versus explicit tool stages.** A compiler driver conveniently invokes compilation and linking. Explicit intermediate artifacts improve teaching and diagnosis. The driver does not collapse the semantic stages merely because it runs them in one command.

**Portable source versus target-specific artifact.** Source can be portable across a declared language subset; object code is tied to architecture, ABI, object format, and often operating-system conventions. Cross-compilation makes that target explicit.

## Failure Modes and Misconceptions

1. **The compiler produces a process.** It produces an artifact; the operating system and runtime construct execution state.
2. **A declaration satisfies a linker reference.** Only a compatible retained definition or permitted dynamic route does.
3. **Sections are memory regions.** Segments or analogous load commands define runtime mappings.
4. **A symbol value is always a final virtual address.** Its meaning depends on file type, section, relocation, and ABI.
5. **`main` is the executable entry address.** Startup code commonly runs first.
6. **Static linking makes a binary self-contained.** Kernel, CPU, configuration, files, and platform contracts remain.
7. **Successful linking proves ABI compatibility.** Names can resolve while layout or calling conventions disagree.
8. **Loading copies the entire executable immediately.** File-backed demand paging is a common alternative.
9. **`exec` creates a child process.** POSIX `exec` replaces the calling process image on success.
10. **One executable works on every machine of the same architecture.** ABI, OS, instruction features, libraries, and format must also match.

## Worked Examples

### Example 1

**Question:** What artifacts arise from two separately compiled source files?

**Reasoning:** `main.c` and `math.c` are independently translated into `main.o` and `math.o`. Each object contains code/data contributions plus symbols and relocations. Neither compiler invocation needs final virtual addresses. The linker later combines them into one executable or library.

**Conclusion:** Separate compilation defers cross-unit address resolution to linking.

### Example 2

**Question:** Can a small model expose missing symbols and runtime placement categories?

**Reasoning:** The executable model builds a definition table, checks requested names, and groups definitions into simplified executable and writable segments. It models one strong-definition case; it is not an ELF linker.

<!-- bijux-verify: {"id":"symbol-resolution-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"definitions: count->main.o:.data, main->main.o:.text, twice->math.o:.text\nunresolved: none\nR-X: main twice\nRW-: count\nentry: main\n","stderr":""}} -->
```python
objects = (
    ("main.o", {"main": ".text", "count": ".data"}, ("twice",)),
    ("math.o", {"twice": ".text"}, ()),
)

definitions = {}
references = []
for object_name, defined, needed in objects:
    for symbol, section in defined.items():
        if symbol in definitions:
            raise ValueError(f"duplicate definition: {symbol}")
        definitions[symbol] = (object_name, section)
    references.extend(needed)

rendered = ", ".join(
    f"{symbol}->{object_name}:{section}"
    for symbol, (object_name, section) in sorted(definitions.items())
)
unresolved = sorted(symbol for symbol in references if symbol not in definitions)
executable = sorted(symbol for symbol, (_, section) in definitions.items() if section == ".text")
writable = sorted(symbol for symbol, (_, section) in definitions.items() if section == ".data")

print("definitions:", rendered)
print("unresolved:", " ".join(unresolved) or "none")
print("R-X:", " ".join(executable))
print("RW-:", " ".join(writable))
print("entry:", "main")
```

**Conclusion:** Definition, reference, section contribution, segment permissions, and entry selection are separate linker decisions.

### Example 3

**Question:** Compute a PC-relative relocation with (S=0x1200), (A=-4), and (P=0x1004).

**Reasoning:** Substitution gives (S+A-P=0x1200-0x4-0x1004=0x1f8). The linker must then verify that (0x1f8) fits the ABI-defined relocation field and encode it as the target instruction expects.

**Conclusion:** Relocation is typed target arithmetic, not arbitrary address subtraction.

### Example 4

**Question:** Why can `.text` and `.rodata` become one mapping?

**Reasoning:** They are distinct sections useful to compiler, linker, relocation, and diagnostic tools. The linker can place their file ranges inside one readable/executable segment if the platform policy permits, while writable `.data` belongs in a different segment. Section identity need not equal page mapping identity.

**Conclusion:** Sections organize artifact content; segments organize load behavior.

### Example 5

**Question:** What happens to a zero-initialized global array?

**Reasoning:** An object format can record its required memory size without storing all zero bytes in the file. A loadable segment may have memory size greater than file size; the additional region is initialized as specified by the format. This reduces artifact size while still creating runtime storage.

**Conclusion:** Process-image bytes need not all have one-for-one file bytes.

### Example 6

**Question:** Why can a dynamically linked executable pass linking and fail at launch?

**Reasoning:** Static linking records a dependency on a shared library and possibly symbol versions. At deployment, the dynamic loader applies platform search and compatibility rules. If no admissible library or required symbol version exists, construction of the process image cannot complete.

**Conclusion:** Link success and deployment-time dependency resolution are different evidence stages.

### Example 7

**Question:** Does the loader jump directly to `main`?

**Reasoning:** The executable header supplies an entry address, usually startup code. Startup receives process parameters, prepares the runtime, performs required initialization, calls `main`, and converts its completion into process termination. Constructors or loader hooks can fail before application entry.

**Conclusion:** Executable entry, runtime entry, and source-level application entry are distinct.

### Example 8

**Question:** Does POSIX `execve` create a new PID?

**Reasoning:** On success it replaces the current process image. The process retains its identity and standard-defined inherited attributes while its address space, code, data, and initial thread image are replaced. A successful call does not return to the old image.

**Conclusion:** Process creation and process-image replacement are separate operations.

### Example 9

**Question:** Why retain separate debug symbols for a stripped production executable?

**Reasoning:** Removing nonessential symbol/debug sections can shrink or limit information in the deployed file without changing loadable execution segments. Postmortem address-to-source analysis still needs an exactly matching, access-controlled debug artifact keyed by build identity.

**Conclusion:** Stripping changes diagnostic evidence, not necessarily executable behavior; provenance must preserve the match.

### Example 10

**Question:** Two libraries export the same function name and both compile. Why can calls still corrupt state?

**Reasoning:** Name resolution checks only part of the contract. If caller and selected callee disagree on argument width, struct layout, stack alignment, return convention, or ownership, the link can succeed while machine state is interpreted inconsistently. Header and binary version drift are common causes.

**Conclusion:** Symbol resolution is necessary but insufficient; ABI agreement is a runtime safety obligation.

## Cross-Program Connections

- **Compilers:** front ends, intermediate representations, code generation, and optimization produce linkable contributions.
- **Operating Systems:** virtual memory, loaders, processes, credentials, and inherited resources construct execution context.
- **Computer Architecture:** instruction sets, registers, calling conventions, alignment, and relocation widths constrain artifacts.
- **Security Engineering:** writable/executable permissions, library search, interposition, provenance, and hardening affect attack surface.
- **Software Delivery:** target matrices, reproducible builds, dependency packaging, symbols, and artifact identity carry build evidence into deployment.
- **Metaprogramming:** preprocessing and generated source can change the effective compilation unit before ordinary checking.
- **Testing & Quality Engineering:** compile, link, load, startup, and run tests cover different failure classes.
- **Platform Engineering:** deployment images and hosts must supply the ABI, loader, libraries, kernel, and CPU features recorded by the artifact contract.

## References

- Randal E. Bryant and David R. O'Hallaron. [*Computer Systems: A Programmer's Perspective*, 3rd ed.](https://csapp.cs.cmu.edu/3e/about.html). Pearson, 2016, ISBN 9780134092669. Author and publisher records checked 2026-08-28.
- John R. Levine. *Linkers and Loaders*. Morgan Kaufmann, 2000, ISBN 9781558604964. Publisher bibliographic record and book front matter checked 2026-08-28.
- Xinuos. [*ELF Object File Format: Program Loading and Dynamic Linking*](https://gabi.xinuos.com/elf/07-loading-intro.html). System V generic ABI specification, current online edition checked 2026-08-28.
- The Open Group. [“exec — execute a file.”](https://pubs.opengroup.org/onlinepubs/9799919799/functions/exec.html) *POSIX.1-2024 / The Open Group Base Specifications Issue 8*. Current standard checked 2026-08-28.
- GNU Project. [*The GNU Linker*](https://sourceware.org/binutils/docs/ld/index.html). GNU Binutils documentation, current online manual checked 2026-08-28.

## Exercises

### Exercise 1

Put these in causal order and state each input/output: source preprocessing, compilation/code generation, static linking, operating-system loading, dynamic linking, runtime startup, application entry. Identify which steps may be fused by a driver without becoming conceptually identical.

### Exercise 2

Object A defines `main` and `table`, and refers to `parse` and `emit`. Object B defines `parse` and refers to `table`. Library member C defines `emit`; library member D defines another strong `parse`. Analyze resolution when A, B, and C are selected, then when D is also selected. State the foundational rule and why real weak/versioned rules need ABI documentation.

### Exercise 3

Compute (S+A) and (S+A-P) for (S=0x5000), (A=8), and (P=0x4ff0). Then explain the additional checks needed before either value can be encoded in a relocation field.

### Exercise 4

Compare static and dynamic linking for a security-sensitive command-line utility deployed on several Linux distributions. Analyze artifact size, shared-library updates, compatibility, reproducibility, symbol provenance, runtime search, diagnostics, and remaining kernel/platform dependencies. Provide a defensible policy rather than one universal choice.

### Exercise 5

A native service builds successfully in CI but fails before `main` on one production host. The log reports a missing symbol version from a shared library. Design a diagnosis: classify the stage, list artifact and host evidence, distinguish source/API compatibility from ABI compatibility, propose immediate containment, and specify a durable release gate.

## Answers to the Exercises

### Answer 1

Preprocessing or expansion consumes declared source plus macros/generated inputs and produces the effective translation unit. Compilation/code generation consumes that unit plus target/options and produces a relocatable object or equivalent. Static linking consumes objects, archives, shared-library contracts, and layout policy and produces an executable/shared object with applied and deferred relocations. Operating-system loading validates the image and constructs initial mappings/state; an interpreter may invoke dynamic linking to map dependencies and complete permitted runtime resolution. Runtime startup initializes the language environment, then calls application entry. A compiler driver can invoke preprocessing, compilation, assembly, and linking in one command; a loader and dynamic linker can cooperate closely. Fusion changes orchestration, not representations, failure causes, or contracts.

### Answer 2

With A, B, and C, `main` and `table` resolve to A, `parse` resolves to B, and `emit` resolves to C; B's reference to `table` resolves to A. Every retained required reference has one strong definition. Selecting D adds a second strong `parse`, so the foundational model rejects the duplicate rather than choosing silently. Actual formats may define weak/strong precedence, visibility, archive extraction order, symbol versioning, or interposition. Those behaviors must come from the target ABI and linker policy, not a generic rule guessed from this example.

### Answer 3

Absolute relocation gives (S+A=0x5000+0x8=0x5008). PC-relative relocation gives (S+A-P=0x5008-0x4ff0=0x18). Before encoding, check that the relocation kind uses the chosen formula, the addend convention is correct, the result fits the signed or unsigned field width, required alignment holds, the instruction interprets the field as expected, overflow behavior is permitted, and the symbol/place addresses are defined in the ABI's address model.

### Answer 4

A static policy can reduce distribution-specific user-space library resolution and improve artifact pinning, but increases size and requires rebuilding to consume library fixes; licensing and libc/platform behavior also matter. A dynamic policy shares platform libraries and can receive compatible security updates, but depends on controlled search paths, symbol versions, distribution ABI promises, and deployment inventories. A defensible design might statically link owned leaf libraries while dynamically linking a distribution-supported system interface, record every build dependency and symbol version, prohibit ambient search directories, retain matching debug symbols, and test on each supported host image. Neither choice removes kernel, CPU, configuration, trust-store, filesystem, or syscall dependencies.

### Answer 5

The earliest visible failure is dynamic load/startup, before application entry. Capture the executable digest, build ID, target, dynamic dependency list, required symbol versions, linker map/options, CI library artifacts, host loader identity, installed library paths/versions/digests, search configuration, and exact loader diagnostic. Source/API compatibility says code compiled against declarations; ABI compatibility asks whether the deployed binary exports the required version with matching binary contract. Immediate containment is rollback to a known-compatible service artifact or host image, or deploy the approved matching library as one atomic release—never create an unreviewed search-path shadow. The durable gate launches the exact release artifact in every supported immutable host image, validates dependency closure and symbol versions, reaches a startup health oracle, and records artifact/host provenance before promotion.
