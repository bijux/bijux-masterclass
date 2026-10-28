---
module_id: CA-014
program: Computer Architecture
level: 1
module_number: 14
title: Addressing Modes
status: complete
last_verified: 2026-09-04
---

# Addressing Modes

## One-Page Review

### Governing question

How does an ISA define the operands, arithmetic, widths, side effects and fault behavior that turn an instruction into an effective address without confusing address formation with translation, protection or memory access?

### Essential definitions

- An **addressing mode** is an architectural rule for deriving an operand value or effective address from instruction fields and architectural state.
- An **effective address** is the address produced by instruction-level address-generation semantics before later translation or access checks unless the ISA defines another boundary.
- A **base register** supplies a reference address; a **displacement** is an encoded constant added to it.
- An **index register** supplies a variable offset, sometimes multiplied by a **scale**.
- **register indirect** uses the contents of a register as an address.
- **base-plus-displacement** computes an address from a base register and signed or unsigned encoded offset.
- **scaled indexed** computes from base, scaled index and displacement.
- **PC-relative** uses an architecture-defined program-counter value as the base.
- **pre-indexed** addressing updates a base before access; **post-indexed** addressing uses the old base and updates it afterward.
- **auto-update** addressing writes an address register as a side effect of a memory instruction.
- **absolute** or **direct** addressing derives an address primarily from instruction bits rather than a general base register.
- **address translation** maps a virtual address to a physical address under privilege and page-table state.
- **alignment** constrains an address relative to access size or architectural rules.
- A **capability address** combines location with bounds, permission, provenance and validity metadata.
- A **relocation** lets a linker finish address-dependent instruction fields once symbol placement is known.

### Central model, mechanism, or theorem

For a common scaled-index form at address width `w`, define

`EA = trunc_w(base + index * scale + displacement)`.

The ISA separately defines operand extraction and extension, address-width truncation or fault, optional base update, translation/protection, alignment, memory access and exception state. A useful staged relation is

`operands -> effective address -> translated address/permissions -> memory transaction or precise fault`.

Every stage has an exact input and failure boundary. A processor may fuse or pipeline the stages internally, but committed state must match a permitted architectural outcome.

### Critical invariants

- The base value, index value, displacement sign/scale and address width are explicit.
- PC-relative calculations name the exact architectural PC base.
- Effective-address arithmetic is distinct from memory data arithmetic and from address translation.
- Access size and alignment are checked according to the active mode and instruction.
- Pre/post-update instructions define old/new base use and behavior on every fault path.
- Translation and permission failure cannot expose an ordinary load result or unauthorized store.
- Relocations preserve the same range, scaling, PC-base and overflow rules as direct encoding.
- Capability or segmented modes check bounds, permissions and metadata at the specified boundary.

### Common failures

Frequent failures are calling a pointer an effective address before adding its offset, sign-extending from the wrong immediate bit, scaling a byte offset twice, assuming address arithmetic never wraps, confusing virtual and physical addresses, using the next PC where the current aligned PC is specified, treating assembler brackets as universal semantics, updating a base register despite a fault, checking alignment after a visible store, assuming unaligned support implies atomicity, overlooking address-size overrides, truncating relocation overflow, treating array-index arithmetic as automatically in bounds, and assuming a cache hit changes architectural addressing.

### Compact example

With 32-bit address arithmetic, base `0x1000`, index `3`, scale `4` and displacement `-8` produce `EA=0x1004`. That result is not yet a successful load: translation, permissions, alignment and the memory system still determine whether data is returned or a precise exception occurs. If the same instruction performs post-increment by 4, it uses the old base for the access and changes the base only according to the ISA’s success/fault rule.

### Connections

Addressing modes connect instruction encoding, register operands, arrays and objects, compilers, linkers, virtual memory, caches, exceptions, atomics, capabilities, security and performance.

## Governing Question

Assembly makes address formation look like punctuation: brackets, parentheses and plus signs. The actual contract is a state transition over fixed-width values, encoded fragments, privilege, memory and possible base-register side effects.

The governing question is what the instruction contributes before the memory hierarchy takes over. Correct reasoning separates address generation from translation and access while preserving their ordered fault and commit relationship.

## Why This Matters

Address errors often survive simple tests. They appear at negative offsets, large arrays, page boundaries, address-width changes or relocation limits. A wrong PC base can misaddress position-independent code only after layout changes.

Rich addressing can improve code density and reduce instruction count, but it creates multi-input arithmetic and side effects that complicate pipelines and precise exceptions. Simple base-plus-offset modes move work into separate arithmetic instructions and give compilers explicit dataflow.

Security depends on the full chain. Correct arithmetic can still access unauthorized memory if translation or bounds checks are wrong. Conversely, speculative address generation may leak information even when architectural permission checks eventually fault.

## Prerequisites and Retrieval

Before studying this module, be able to:

- derive register and immediate operands from an instruction;
- perform fixed-width signed and unsigned arithmetic;
- distinguish virtual and physical memory conceptually;
- explain access size, byte order, alignment and precise exceptions;
- trace pre-state reads and guarded post-state writes.

Retrieve ISA/profile/version; active address size; register and immediate widths; every memory and control-flow addressing form; displacement extraction and scaling; legal scales; PC base; segment or capability state; pre/post-update rules; access sizes; alignment behavior; address wrap or fault semantics; translation stages; permission checks; memory attributes; atomicity; exception priority; relocation definitions; code model; linker relaxation; compiler lowering; executable semantics; address-generation RTL; MMU/TLB interface; architecture tests; binary corpus; silicon errata; and exact tool/hardware revisions.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish effective-address formation, translation and memory access;
2. derive base, displacement, indexed and scaled-indexed addresses;
3. reason about address width, extension, truncation and wraparound;
4. specify PC-relative and absolute addressing precisely;
5. analyze pre-indexed, post-indexed and auto-update side effects;
6. connect access size and alignment to fault and atomicity rules;
7. explain segmented and capability-based addressing extensions;
8. verify relocation and compiler lowering against ISA formulas;
9. compare simple and rich addressing-mode trade-offs;
10. construct implementation and security evidence for address generation.

## Core Exposition

### Begin with an address expression

Write each mode as a pure expression over architectural pre-state before discussing caches or pipelines. Examples include `EA=base`, `EA=base+disp` and `EA=base+index*scale+disp`.

Then add side effects and failure alternatives. This keeps a compact formula from hiding base update, privilege or exception behavior.

### Distinguish address namespaces

An instruction commonly forms a virtual or effective address. Translation may produce an intermediate or physical address; devices and debuggers may use additional namespaces.

Always label traces. A hexadecimal number without its address space is insufficient evidence when translation, tagging or segmentation is active.

### Use register indirect

Register-indirect addressing treats a register value as the effective address. It is the core of pointer dereference and dynamic data structures.

The simple syntax still requires an active address width, access size, alignment, translation and permission behavior. The register may contain a wider value than the active address calculation uses.

### Add a displacement

Base-plus-displacement supports stack slots, object fields and fixed offsets. The encoded displacement is reconstructed, extended and added under the ISA’s address arithmetic.

A signed displacement conveniently reaches before and after a base. An unsigned displacement may devote the same bits to a larger nonnegative range. Never infer signedness from the printed plus sign.

### Add an index

Indexed addressing combines a stable base with a changing element index. Some ISAs provide direct base-plus-index forms; others require a separate shift/add before the load or store.

Index width and extension matter. A negative signed 32-bit index extended to 64 bits differs from zero-extending the same low bits.

### Scale for element size

Scaled-index modes multiply the index by a small legal scale, commonly a power of two. This directly represents array byte offsets.

The scale belongs to address formation, not to the source-language index type. A compiler must not pre-scale and also select a scaled mode unless that double scaling is intended.

### Define address arithmetic width

Specify the width at which operands are extended and the sum is formed. Some modes use the current execution address size; others derive a wider intermediate then apply canonical-address checks.

If arithmetic wraps modulo `2^w`, document it. If noncanonical or overflowed addresses fault later, distinguish arithmetic result from validation outcome.

### Treat PC-relative bases precisely

PC-relative addressing supports position-independent code, literals and branches. The base might be the current instruction address, an aligned page address or another architecture-defined PC value.

Variable instruction length makes “next PC” especially dangerous as an assumption. Relocation formulas must use the identical base convention.

### Understand absolute forms

Absolute/direct modes encode much or all of an address in the instruction or associated literal. They can simplify access to fixed locations.

They consume encoding space, constrain address range and complicate relocation under address randomization. Many modern toolchains synthesize large addresses from multiple instructions.

### Distinguish literal addressing

A literal load may use PC-relative addressing to read a constant stored near code. The address computation and memory access remain ordinary architectural events.

Executable permissions do not imply readable literal data on every platform. Compilers and linkers must respect section placement, range and memory attributes.

### Model pre-indexed update

Pre-indexed addressing first computes an updated base, uses it for the memory effective address and may write it back. The semantic relation must say whether writeback occurs before, with or only after a successful access.

If base and data destination overlap, the architecture may restrict the form or define an ordering. Treat such constraints as legality, not assembler taste.

### Model post-indexed update

Post-indexed addressing uses the old base for the memory access, then derives the new base. It is useful for stream traversal and stack operations.

Precise fault semantics are essential. A fault-restart loop cannot tolerate an undocumented base advance that causes the retried instruction to skip data.

### Handle auto-decrement stacks

Push and pop operations may be special instructions or syntactic forms of pre/post-update addressing. Direction, element size and stack convention must agree.

Multiple-register transfers raise partial-completion questions. An implementation may perform several memory beats, but architectural restart state must be defined.

### Compare source and destination overlap

A load with base writeback and destination equal to the base can request two writes to one architectural register. Some architectures forbid it; others define which result survives.

Generate overlap cases explicitly. Relying on assembler rejection alone leaves raw machine code and hardware decode unverified.

### Separate access size

The address points to the first addressed byte or another precisely defined location. Access size determines byte lanes, alignment, page crossing and returned extension.

Address formation normally does not change merely because a load is signed. Signedness commonly affects data extension, while width can affect displacement scaling in specialized modes.

### Check alignment

Natural alignment places an `n`-byte object at an address divisible by `n`. An ISA can require alignment, support unaligned access or make behavior dependent on attributes.

Support does not promise one transaction or atomicity. An unaligned access can cross cache lines, pages or devices and have different performance and ordering behavior.

### Order validation and access

The architecture defines the visible outcome and exception priority when address canonicality, alignment, translation and permission checks interact.

Hardware may perform checks in parallel. It must select a permitted architectural fault and suppress unauthorized ordinary effects regardless of internal timing.

### Translate virtual addresses

Translation consults privilege state, page tables, TLBs and memory-management configuration after or alongside effective-address formation. Multi-stage virtualization can add guest and host translations.

TLB hits and page walks are implementation mechanisms. The architectural result is a permitted mapping, attribute set or translation fault for the active context.

### Enforce permissions

Permissions depend on access type: instruction fetch, read, write, atomic and sometimes privilege-specific execute/read distinctions. The effective address alone does not authorize access.

Accessed/dirty updates and fault priority may modify translation metadata. Such effects require specification and evidence separate from the program’s requested load/store.

### Incorporate segmentation

Segmented addressing combines an offset with segment base, limit and attributes. In some modes segmentation is prominent; in others most segments are architecturally constrained.

The effective linear address and later paging address must not be conflated. Limit and privilege checks belong at their defined stage.

### Incorporate capabilities

Capability addressing associates a pointer-like value with bounds, permissions, validity and provenance. Address arithmetic alone cannot manufacture authority.

Loads/stores must pass tag, bounds and permission checks. Narrowing bounds or clearing validity can be architectural outcomes even when integer address bits look plausible.

### Treat tags and top-byte metadata

Some architectures use address bits or side metadata for tagging, authentication or memory safety. Define which bits participate in translation and which are ignored, checked or transformed.

Compiler pointer arithmetic and debugger display must preserve the contract. Masking “unused” high bits ad hoc can remove protection or create noncanonical addresses.

### Connect to source-language pointers

Source languages attach object, provenance and undefined-behavior rules beyond ISA integer arithmetic. A computed machine address is not automatically a valid language pointer.

Compiler IR operations such as typed address calculation communicate bounds and layout assumptions. Lowering must preserve defined programs without inventing architectural guarantees for undefined ones.

### Lower arrays and structures

For array element size `s`, source index `i` often lowers toward `base+i*s`. A rich mode may fold the multiply and add into a load.

Structure fields contribute constant offsets; multidimensional arrays combine strides. Overflow and in-bounds assumptions must match language and IR semantics before ISA selection.

### Support position-independent code

Position-independent code derives code and data addresses relative to PC, global-offset structures or relocatable sequences. The linker resolves distances after layout.

Code models define assumed reach. When a symbol falls outside a form’s range, tools need a longer sequence, veneer or error rather than silent truncation.

### Apply relocations

A relocation specifies symbol, addend, place/base, shift, field fragments and overflow rules. Split high/low address construction requires paired rounding and consistency.

The linker must produce the same effective address the abstract formula intends. Disassembly alone may show field values but not the original symbol-level proof.

### Consider linker relaxation

Relaxation can replace a general address sequence with a shorter PC-relative or immediate form when final layout permits. It must preserve value and all relevant side effects.

Recompute debug ranges, exception data and subsequent addresses. Signed reach and alignment boundaries deserve explicit regression tests.

### Separate addressing from caching

Caches use portions of translated or physical addresses for lookup, tags and offsets, but cache organization does not change the ISA’s effective-address formula.

A hit affects latency. It cannot legalize an out-of-bounds capability, bypass a permission fault or change architecturally required alignment behavior.

### Analyze address-generation units

Processors may dedicate address-generation units that add base, scaled index and displacement. Port count and supported forms affect scheduling throughput.

That performance structure remains microarchitectural. A slower sequence can be conformant if its committed address and exception behavior match the ISA.

### Handle speculation safely

Out-of-order processors may calculate and probe addresses before older branches resolve. Architectural state rolls back on a wrong path or fault.

Microarchitectural traces can still leak address-dependent information. Bounds-check bypass and fault-based channels require threat models and mitigations beyond functional precision.

### Verify formulas independently

Generate operand-boundary tests: zero, minimum and maximum displacements; address wrap; legal scales; signed/unsigned indices; PC bases; overlaps and every access size.

Compare an independent executable model, compiler-selected instructions, relocation results, RTL address-generation traces and processor commit/fault traces. Shared formulas demonstrate consistency, not independent correctness.

### Govern lifecycle evidence

Bind source language, compiler IR, code model, ABI, relocation, ISA/profile, model, RTL, MMU configuration, binary and hardware revision. Preserve failing addresses and page/capability state.

Track silicon errata involving update-on-fault, page crossing, canonical checks or address-size modes. A software workaround does not erase the affected hardware deviation.

## Definitions and Notation

- `w`: active address-arithmetic width.
- `B`: architectural base-register value from pre-state.
- `I`: architectural index-register value from pre-state.
- `s`: legal scale applied to the index.
- `D`: reconstructed and extended displacement.
- `EA`: effective address produced by instruction address generation.
- `VA`: virtual or linear address presented to translation.
- `PA`: translated physical address.
- `A`: address of the current instruction under the stated PC convention.
- `size`: memory access size in bytes.
- `align(a,n)`: predicate `a mod n = 0`.
- `trunc_w(x)`: low `w` bits of integer `x`.
- `Translate(VA,C)`: mapping/permission result under context `C` or a fault.
- `Access(PA,size,kind)`: memory read/write/atomic operation or a fault.
- `B'`: post-state base value for an auto-update form.

Unless stated otherwise, hexadecimal examples use byte addresses and arithmetic modulo the declared address width.

## Mechanisms, Invariants, or Proof Structure

1. **Operand obligation:** prove base, index, displacement and scale are extracted from the specified pre-state and instruction bits.
2. **Extension obligation:** prove index/displacement signedness and extension width match the active addressing form.
3. **Arithmetic obligation:** prove multiply, addition, truncation, canonicality and overflow behavior produce exactly the defined `EA`.
4. **PC-base obligation:** prove every PC-relative form uses the architecture-defined instruction/page/next-address base.
5. **Access obligation:** prove access size and byte range derive from `EA` as specified.
6. **Alignment obligation:** prove aligned, unaligned and cross-boundary cases receive permitted behavior and atomicity claims.
7. **Update obligation:** prove pre/post-indexed forms use the correct old/new base and overlap rules.
8. **Fault obligation:** prove every failure path commits only permitted base, destination, memory, PC and trap changes.
9. **Translation obligation:** prove the correct address space, context, stage and attributes feed translation.
10. **Permission obligation:** prove read, write, execute and atomic requests cannot bypass privilege or page/capability policy.
11. **Capability obligation:** prove bounds, tag, provenance and permission checks accompany applicable address arithmetic.
12. **Relocation obligation:** prove symbol, addend, place, scale, fragments and overflow reconstruct the intended address.
13. **Compiler obligation:** prove lowering preserves defined source/IR pointer and layout semantics for the selected mode.
14. **Refinement obligation:** prove fused, pipelined or speculative address generation commits the architectural address/fault relation.
15. **Evidence obligation:** bind specifications, tools, page/capability state, binaries, RTL, hardware and errata to exact versions.

## Alternatives and Trade-Offs

1. **Simple versus rich modes:** simple forms regularize pipelines; rich forms reduce instruction count and code size.
2. **Signed versus unsigned displacement:** signed fields reach around a base; unsigned fields extend positive reach.
3. **Unscaled versus scaled offset:** unscaled addresses arbitrary bytes; scaling expands aligned object reach.
4. **Separate shift/add versus scaled index:** explicit arithmetic exposes dataflow; folded modes improve density.
5. **Register indirect versus absolute:** registers support dynamic/rebased data; absolute forms directly name fixed locations.
6. **PC-relative versus global-base-relative:** PC relative aids local position independence; global bases can cover broader shared data.
7. **No writeback versus auto-update:** separate updates simplify faults; auto-update speeds streams and stacks.
8. **Pre-index versus post-index:** pre-index naturally allocates before access; post-index naturally advances after access.
9. **Strict alignment versus unaligned support:** strict rules simplify hardware/atomicity; support eases packed data access.
10. **Wraparound versus checked addresses:** modulo arithmetic is simple; checks catch invalid/canonicality boundaries.
11. **Flat versus segmented addressing:** flat models simplify software; segments provide base/limit domains and compatibility.
12. **Integer versus capability pointers:** integers are compact/flexible; capabilities bind authority and bounds.
13. **Short versus long code model:** short forms improve density; long models reach arbitrary layouts.
14. **Static sequences versus relaxation:** static bytes aid reproducibility; relaxation improves final layout efficiency.
15. **Early speculation versus conservative access:** speculation improves latency; conservative checks reduce side-channel exposure.

## Failure Modes and Misconceptions

1. “A base register value is always the final address.” Displacement, index, segmentation and translation may follow.
2. “Effective and physical address are synonyms.” Translation separates them.
3. “Addressing mode includes cache lookup semantics.” Caching is an implementation/memory-system layer.
4. “The plus sign proves an unsigned displacement.” Encoding semantics decide signedness.
5. “The printed displacement is the encoded integer.” Scaling and relocation can differ.
6. “A scaled index should be pre-multiplied by the compiler too.” That can double-scale.
7. “Address addition uses unlimited mathematical integers.” Width, wrap and canonical checks matter.
8. “A wider base forces wider address arithmetic.” Mode-specific address-size rules can override it.
9. “PC relative always uses the next instruction.” Architectures choose exact bases.
10. “Instruction length is irrelevant to PC-relative code.” It affects addresses and layout even when base is current PC.
11. “Absolute addressing needs no relocation.” Final placement may remain unknown until link/load time.
12. “Literal loads read instruction bits as an immediate.” They usually perform a memory access near code.
13. “Pre-index and post-index differ only in syntax.” They select different access addresses and update timing.
14. “Base writeback always happens even on fault.” The ISA’s exception rule governs it.
15. “Destination/base overlap is obviously ordered.” It can be restricted or architecture-specific.
16. “Signed loads use signed address arithmetic.” Signedness usually describes loaded-data extension.
17. “Unaligned support guarantees one atomic access.” It may split across boundaries.
18. “Alignment can be checked after the store.” Visible partial writes may violate precision.
19. “A TLB hit proves permission.” Cached translation includes context and attributes that must be valid.
20. “Page tables turn invalid source pointers valid.” Language provenance and architecture permission are distinct.
21. “Bounds are implied by address bits.” Capabilities or software metadata carry bounds separately.
22. “Ignoring high address bits is always harmless.” Tags, canonicality and authentication can use them.
23. “Relocation overflow may safely truncate.” It redirects access to the wrong location.
24. “Relaxation only changes speed.” It changes bytes and downstream addresses/metadata.
25. “Correct committed faults eliminate address side channels.” Speculative microarchitectural effects need separate evidence.
26. “One successful array load proves the mode.” Boundaries, negative indices, faults, updates and profiles remain uncovered.

## Worked Examples

### Example 1

Register indirect with `B=0x1000` gives `EA=0x1000`; a four-byte access addresses bytes `0x1000..0x1003` before translation.

### Example 2

Base-plus-displacement with `B=0x1000` and signed `D=-16` gives `EA=0x0ff0` at 32 bits.

### Example 3

Scaled index with `B=0x1000`, `I=3`, `s=4`, `D=-8` gives `EA=0x1004`.

### Example 4

At 32 bits, `0xfffffffc+8` wraps to `0x00000004` if modulo arithmetic applies; later canonicality or permission checks are separate.

### Example 5

PC-relative with architectural base `0x0200` and displacement `0x30` gives target/effective address `0x0230`.

### Example 6

Pre-index from base `0x1000` by 16 uses `0x1010` and proposes new base `0x1010`; fault behavior determines whether writeback commits.

### Example 7

Post-index from base `0x1000` by 16 accesses `0x1000` and proposes new base `0x1010` after the access.

### Example 8

An eight-byte access at `0x0ffc` crosses a `0x1000` page boundary, so translation and permission may need both pages even though the start is aligned to four.

### Example 9

A capability with range `[0x1000,0x1100)` permits a four-byte access at `0x10fc` but rejects one at `0x10fe` because the byte range exceeds the bound.

### Example 10

A PC-relative relocation whose signed range is exceeded must select a longer code sequence or fail; retaining low bits could point to an unrelated mapped object.

## Cross-Program Connections

- **Instruction encoding:** immediate fragments, scales and register fields represent address formulas.
- **Compilers:** arrays, structures and pointer IR lower into address arithmetic and memory operations.
- **Linkers:** relocations, code models and relaxation complete placement-dependent addresses.
- **Virtual memory:** translation and protection consume effective/virtual addresses under context.
- **Caches:** address bits select sets and tags after the architectural formation boundary.
- **Exceptions:** alignment, translation, permission and capability failures require precise state.
- **Concurrency:** access size, splitting and atomicity affect shared-memory observations.
- **Security:** bounds, privilege, tagging and speculation govern unauthorized address use.
- **Performance:** address-generation units and mode complexity affect scheduling and latency.
- **Systems engineering:** binary, MMU, tool, RTL, hardware and errata versions define assurance scope.

## References

1. RISC-V International, [RV32I Base Integer Instruction Set](https://docs.riscv.org/reference/isa/unpriv/rv32.html), base-plus-offset loads/stores, PC-relative address formation, alignment and exceptions; retrieved 2026-09-04.
2. Arm, [Arm Architecture Reference Manual for A-profile Architecture](https://developer.arm.com/documentation/ddi0487/latest/), scaled/unscaled, indexed, writeback, literal and address-size semantics; retrieved 2026-09-04.
3. Intel, [Intel 64 and IA-32 Architectures Software Developer's Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), base/index/scale/displacement, address-size, segmentation and canonical-address behavior; retrieved 2026-09-04.
4. LLVM Project, [getelementptr Instruction](https://llvm.org/docs/LangRef.html#getelementptr-instruction), typed aggregate address calculation and in-bounds/provenance semantics; retrieved 2026-09-04.
5. WebAssembly Community Group, [Memory Instructions](https://webassembly.github.io/spec/core/exec/instructions.html#memory-instructions), linear-memory effective addresses, offsets, bounds and traps; retrieved 2026-09-04.
6. RISC-V International, [ELF psABI](https://riscv-non-isa.github.io/riscv-elf-psabi-doc/), address relocations, code sequences and linker relaxation; retrieved 2026-09-04.
7. GNU Binutils, [Using as](https://sourceware.org/binutils/docs/as/), machine-dependent address syntax, expressions and relocation emission; retrieved 2026-09-04.
8. Robert N. M. Watson et al., [Capability Hardware Enhanced RISC Instructions: CHERI Instruction-Set Architecture](https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-951.pdf), capability bounds, permissions, tags and address semantics; retrieved 2026-09-04.

## Exercises

### Exercise 1

Derive effective addresses for register-indirect, base-plus-displacement, scaled-index, PC-relative, pre-index and post-index examples at 32-bit width.

### Exercise 2

Implement a small address-generation model for scaled-index, wraparound, PC-relative, pre-index and post-index forms and reproduce their exact trace.

### Exercise 3

Specify the state transitions for a post-indexed load under success, alignment fault, translation fault and destination/base overlap.

### Exercise 4

Design compiler/linker evidence for lowering a global array access into a PC-relative high/low address sequence with possible relaxation.

### Exercise 5

Construct assurance for adding capability bounds to an existing integer-addressed processor and software stack.

## Answers to the Exercises

### Answer 1

Register-indirect `B=0x1000` gives `0x1000`; base plus `-16` gives `0x0ff0`; base `0x1000` plus index `3` scaled by four plus `-8` gives `0x1004`. PC base `0x0200` plus `0x30` gives `0x0230` under that explicit PC convention.

Pre-index by 16 uses and proposes `0x1010`; post-index uses `0x1000` and proposes `0x1010`. At width 32, `0xfffffffc+8` produces `0x00000004` when the mode specifies modulo arithmetic. Translation, alignment, permission and access remain later steps.

### Answer 2

The model below makes arithmetic width and old/new base explicit. It does not perform memory translation or access.

<!-- bijux-verify: {"id":"addressing-mode-calculations","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"scaled base=0x00001000 index=3 scale=4 displacement=-8 ea=0x00001004\nwrap base=0xfffffffc displacement=8 ea=0x00000004\npc_relative pc=0x00000200 displacement=48 ea=0x00000230\npre_index old_base=0x00001000 displacement=16 ea=0x00001010 new_base=0x00001010\npost_index old_base=0x00001000 displacement=16 ea=0x00001000 new_base=0x00001010\n"}} -->
```python
mask = (1 << 32) - 1


def address(*terms):
    return sum(terms) & mask


base = 0x1000
index = 3
scale = 4
displacement = -8
ea = address(base, index * scale, displacement)
print(
    f"scaled base=0x{base:08x} index={index} scale={scale} "
    f"displacement={displacement} ea=0x{ea:08x}"
)

wrap_base = 0xFFFFFFFC
print(f"wrap base=0x{wrap_base:08x} displacement=8 ea=0x{address(wrap_base, 8):08x}")

pc = 0x200
print(f"pc_relative pc=0x{pc:08x} displacement=48 ea=0x{address(pc, 48):08x}")

updated = address(base, 16)
print(
    f"pre_index old_base=0x{base:08x} displacement=16 "
    f"ea=0x{updated:08x} new_base=0x{updated:08x}"
)
print(
    f"post_index old_base=0x{base:08x} displacement=16 "
    f"ea=0x{base:08x} new_base=0x{updated:08x}"
)
```

The passing trace establishes five arithmetic cases only. It provides no ISA-wide, translation, permission, memory, timing or hardware evidence.

### Answer 3

On success, read old base and other operands, form `EA=old_base+D`, translate/check/access, write loaded data to the destination, write `new_base=old_base+U`, and advance PC according to the ISA. For post-index, the access address is the old base even when `U` equals `D`.

On alignment or translation fault, establish specified trap state and suppress ordinary destination, memory and base writes if the ISA promises precise no-writeback failure. Define exception priority if both apply. If destination equals base, either declare the encoding illegal/unpredictable under exact architectural terminology or specify which write wins; do not infer it from implementation scheduling.

### Answer 4

Start with source/IR proof that the array object, element size, index and bounds justify the intended byte address. Define high/low PC-relative relocation formulas using the exact instruction addresses, rounding, scales, fragments and signed ranges. Test symbols at both range limits, page rounding boundaries, negative distances and layout changes.

Compare compiler IR, assembly object relocations, linked bytes, disassembled operands and an executable address model. If relaxation replaces the pair, prove the shorter form computes the same address and updates debug/exception metadata. Preserve source, IR, objects, linker map, options, binary digest and tool versions.

### Answer 5

Define capability representation, tag/provenance, bounds, permissions, sealing, arithmetic, load/store checks, exceptions, reset, privilege, context switching, virtualization and debug. State how integer addresses convert to or derive from capabilities without silently creating authority.

Extend compiler pointer models, ABI argument/preservation rules, loader relocations, OS/hypervisor context, debugger display, executable semantics and RTL. Test exact-boundary accesses, wrap, tag clearing, permission combinations, speculative paths, faults, process/guest isolation and legacy interoperation. Preserve models, traces, binaries, capability state, hardware revisions and errata. Named architecture, language/compiler, ABI, OS, hypervisor, RTL, formal, security, safety, verification and independent-assurance reviewers assess their scopes. This module supplies no certification.
