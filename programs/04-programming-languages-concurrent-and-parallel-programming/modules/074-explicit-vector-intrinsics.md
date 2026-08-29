---
module_id: CONPAR-074
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 74
title: Explicit Vector Intrinsics
status: complete
last_verified: 2026-08-29
---

# Explicit Vector Intrinsics

## One-Page Review

### Governing question

When does explicit vector programming justify its target-specific ownership cost, and how can an intrinsic implementation remain semantically exact, safely dispatched, testable, and portable through a durable boundary?

### Essential definitions

- An **intrinsic** is a compiler-recognized language operation exposing target or vector semantics without inline assembly; it may lower to one instruction, several instructions, or no instruction.
- An **ISA feature** is an architecturally defined capability required by an operation.
- A **fixed-width vector type** has a compile-time bit or lane count; a **scalable vector type** has a runtime architectural length.
- An **immediate operand** must be a compile-time constant encoded in an instruction field.
- A **mask/predicate** selects active lanes; **merge** preserves passthrough lanes while **zeroing** clears them.
- A **lane operation** applies independently; a **horizontal operation** combines or permutes across lanes.
- **wrapping**, **saturating**, and **trapping** arithmetic are distinct overflow contracts.
- A **feature-specific function** is compiled only for a declared target feature set.
- **runtime dispatch** selects a supported implementation after checking hardware and required operating-system state.
- A **baseline fallback** implements the same interface without the optional feature.
- A **portable SIMD abstraction** presents vector semantics independent of one ISA and lowers through a compiler or library.
- An **intrinsic containment boundary** isolates target code behind a stable semantic API, tests, dispatch, and ownership.

### Central model, mechanism, or theorem

Begin with semantic operation F over logical lanes and a target capability predicate P. Implement target version `V_P` using intrinsic specifications, including element types, mask/tail behavior, immediate ranges, memory effects, exceptions, and arithmetic. Prove `V_P(x)` is equivalent to reference F for every input in the API domain, and dispatch to `V_P` only when P plus OS/ABI preconditions hold; otherwise use fallback S that also refines F. Generated-code inspection establishes mapping, differential tests establish scoped semantics, and benchmarks establish value. None substitutes for the others.

### Critical invariants

Element signedness, width, overflow, conversion, shift, rounding, NaN, and exception semantics match the API; lane order and shuffle indices are correct; inactive lanes have the specified merge/zero and fault behavior; memory ranges, alignment, alias, and scatter collisions are valid; immediate arguments are in range; target code cannot execute before dispatch; OS extended-state support and ABI boundaries are checked; every implementation handles zero length and tails; scalable code derives progress from active length; the baseline is always buildable and force-testable; generated instructions are reviewed for target/security-critical kernels; and toolchain/intrinsic-reference versions are recorded.

### Common failures

Programmers assume intrinsic name equals one instruction, confuse signed and unsigned comparisons, choose wrap when saturation is required, reverse shuffle conventions, use a variable where an immediate is required, blend after an unsafe unmasked load, trust alignment from an allocation after slicing, compile the entire binary for the newest ISA, check CPU features but not OS vector-state support, pass target vector types across unstable ABIs, hard-code a scalable length, omit the scalar tail, compare floats with a naive tolerance, benchmark without verifying the selected variant, or duplicate algorithms across targets until they diverge.

### Compact example

For unsigned 8-bit lanes, `250+10` is 4 under wrap and 255 under saturation. With active mask `1101` and merge passthrough 9, left/right vectors `[250,1,200,0]` and `[10,2,100,255]` yield saturated `[255,3,9,255]` but wrapped `[4,3,9,255]`. The opcode family and mask policy are part of correctness, not tuning details.

### Connections

[Compiler Auto-Vectorization](073-compiler-auto-vectorization.md) explains when the compiler can own mapping; [SIMD Execution and Vector Lanes](071-simd-execution-and-vector-lanes.md) defines masks, tails, and arithmetic; [Data Layout for Vectorization](072-data-layout-for-vectorization.md) defines address shape. The [program roadmap](../ROADMAP.md) next moves to GPU grids, memory, coalescing, and pipelines.

## Governing Question

What semantic, performance, portability, compatibility, and maintenance evidence is required before replacing compiler-selected scalar/vector code with explicit intrinsic operations?

Intrinsics are appropriate when a measured hot operation needs target functionality the compiler cannot express or reliably select, when instruction semantics are themselves required, or when a reviewed library kernel must control a stable mapping. They are not a default marker of expert code. They expand the support matrix and place future correctness on the team.

## Why This Matters

Explicit vector APIs expose saturating arithmetic, permutes, masked memory, population counts, dot products, crypto primitives, conversions, and other instructions that ordinary source may not select. They can eliminate compiler ambiguity and make a carefully designed kernel predictable for a chosen target class.

That control is local and conditional. The compiler still allocates registers, schedules instructions, inserts moves, legalizes unsupported operations, and may fold or reorder code under language rules. An intrinsic can expand to a sequence slower than expected. A fixed-width implementation can require multiple ISA variants and dispatch. A scalable API uses different types and loop structure.

The engineering goal is not to maximize intrinsic count. It is to own the smallest target-specific surface that closes a measured gap while preserving one authoritative specification and fallback.

## Prerequisites and Retrieval

Retrieve:

- lane, mask, tail, scatter, reduction, and dispatch semantics from [SIMD Execution and Vector Lanes](071-simd-execution-and-vector-lanes.md);
- layout, alignment, gather, view, and conversion obligations from [Data Layout for Vectorization](072-data-layout-for-vectorization.md);
- compiler legality, remarks, target plans, and scalar oracle strategy from [Compiler Auto-Vectorization](073-compiler-auto-vectorization.md); and
- numeric reduction structure from [Parallel Loops and Reductions](044-parallel-loops-and-reductions.md).

Retrieval prompt: name the exact operation the compiler fails to produce, the source semantics it must preserve, the target feature that supplies it, the measured gain available, and who will own every fallback and target variant.

## Learning Objectives

After completing this module, a learner can:

1. distinguish intrinsics, builtins, vector extensions, portable SIMD, and inline assembly;
2. read an intrinsic's operation pseudocode, feature requirements, arguments, and exceptions;
3. specify lane types, masks, arithmetic, conversions, shuffles, and memory effects precisely;
4. implement fixed-width bodies, tails, and scalable-vector progress safely;
5. design feature-specific compilation, dispatch, baseline fallback, and ABI boundaries;
6. contain target code behind a semantic API without duplicated policy;
7. inspect lowering for moves, shuffles, scalarization, and instruction sequences;
8. build lane-wise, differential, boundary, cross-target, and sanitizer tests;
9. benchmark intrinsics against auto-vectorized and library alternatives; and
10. scope security, safety, and independent review claims.

## Core Exposition

### Intrinsics are specified operations

An intrinsic looks like a function call, but the compiler recognizes its semantics. The reference usually specifies operand and result types, per-lane operation, mask behavior, required ISA subset, header, and sometimes an illustrative instruction. Treat the operation description as normative for code reasoning; the mnemonic association is evidence about likely lowering, not a guaranteed one-to-one mapping.

Some intrinsics lower to multiple instructions because the target lacks a direct form, an operand is not constant, widths require legalization, or the compiler must move data. Others disappear through constant folding or combine with surrounding operations. Conversely, an ordinary vector operator can lower to the same instruction. Always inspect the actual configured build.

Builtins are compiler-defined recognized operations; vendor intrinsics commonly wrap builtins in headers. GNU/Clang vector extensions provide vector types and overloaded operators. Portable SIMD types expose data-parallel operations through a standard/library abstraction. Inline assembly controls encoding more directly but blocks many compiler analyses and adds register, ABI, and side-effect hazards. Choose the highest-level mechanism that supplies the required semantics and measured mapping.

### Read the complete contract

Before using an intrinsic, record:

- element type, signedness, lane count or scalable type;
- exact arithmetic, widening/narrowing, saturation, rounding, and exceptional values;
- operand lane order and result lane order;
- mask type and whether inactive results merge, zero, or remain unspecified;
- memory alignment, address calculation, inactive fault suppression, and ordering;
- immediate operand range and encoding;
- ISA feature flags and compiler header/options;
- latency/throughput data only for the actual microarchitecture; and
- whether the guide warns that a sequence may be generated.

Names can be deceptively similar. Packed signed versus unsigned min, saturating versus wrapping add, arithmetic versus logical shift, truncating versus rounding conversion, ordered versus unordered floating comparison, and merge versus zero masked variants differ semantically.

### A finite semantic model

The following executable code models two unsigned 8-bit arithmetic choices and merge-masked lanes. It does not call a vector intrinsic, model instructions, flags, exceptions, timing, or memory.

<!-- bijux-verify: {"id":"masked-u8-arithmetic-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"left=[250, 1, 200, 0]\nright=[10, 2, 100, 255]\nmask=[True, True, False, True]\npassthrough=[9, 9, 9, 9]\nsaturating=[255, 3, 9, 255]\nwrapping=[4, 3, 9, 255]\n","stderr":""}} -->
```python
left = [250, 1, 200, 0]
right = [10, 2, 100, 255]
mask = [True, True, False, True]
passthrough = [9, 9, 9, 9]


def masked_add(operation):
    result = []
    for lane in range(len(left)):
        if not mask[lane]:
            result.append(passthrough[lane])
        elif operation == "saturating":
            result.append(min(255, left[lane] + right[lane]))
        else:
            result.append((left[lane] + right[lane]) % 256)
    return result


print(f"left={left}")
print(f"right={right}")
print(f"mask={mask}")
print(f"passthrough={passthrough}")
print(f"saturating={masked_add('saturating')}")
print(f"wrapping={masked_add('wrapping')}")
```

This difference becomes a production bug when the scalar reference saturates pixels but the intrinsic path uses ordinary packed addition. Test semantic categories, not just representative values that avoid overflow.

### Fixed-width types and operations

Fixed-width ISAs expose types associated with 64-, 128-, 256-, 512-, or other bit widths. The type often says storage width and element family, while the intrinsic says interpretation. Reinterpreting bits should be distinguished from numerically converting lanes. A bitcast preserves representation; a conversion changes values, may round or saturate, and can change lane count.

Widening takes narrower lanes into wider results, often producing low/high halves. Narrowing may truncate, round, or saturate. Signedness determines extension and comparisons. Integer promotions from scalar C/C++ do not necessarily match vector-extension rules. Write wrapper names from semantics such as `add_saturating_u8`, not only a vendor mnemonic.

Horizontal operations reduce, pairwise-combine, or extract across lanes. They frequently have different order across ISA families. Permutes and shuffles use indices whose scope may be each 128-bit sublane, one source, two sources, bytes, or elements. Derive a lane table for every nontrivial shuffle and test unique sentinel values per lane.

Immediate operands encode control bits, shift counts, rounding modes, or lane selections. The API may require a compile-time constant. If runtime selection is needed, use a switch among valid constant forms, a variable-control instruction/intrinsic, or another algorithm. Do not assume the compiler will accept or efficiently lower an arbitrary value.

### Masks and predication

Legacy fixed-width code may represent masks as all-zero/all-one vector lanes and blend values. Newer ISAs may have dedicated mask registers. Scalable architectures use predicate types. Convert between mask representations only through defined APIs; bit widths, lane counts, and truth encoding differ.

Merge-masked operation `r=op(src,k,a,b)` keeps `src[l]` where k is false. Zero-masked operation writes zero. An unmasked operation followed by blend computes both sides and can fault, raise exceptions, or access invalid memory. Use a specified masked operation when suppression is required and confirm source/compiler/ISA semantics.

Mask granularity follows element width. Reusing a byte mask for 32-bit lanes without a defined conversion can activate the wrong positions. After narrowing or widening, regenerate or explicitly transform predicates. Scalable predicates also encode active elements by type granularity.

### Loads, stores, gathers, and scatters

Choose aligned or unaligned operations according to a proven effective address. A base allocation's alignment does not survive arbitrary byte/element offsets. Passing a false alignment promise can fault or invoke undefined behavior. When alignment materially helps, expose it in a checked view or branch.

Masked contiguous loads/stores and gather/scatter differ in address formation and inactive-lane guarantees. For a gather, validate every active address without arithmetic overflow and within live objects. A scatter with duplicate active addresses needs an ordering or conflict policy; an unordered intrinsic cannot implement a scalar last-writer rule by assumption.

Streaming/non-temporal stores are policies with alignment, ordering, cache, and fencing consequences. They help only for measured low-reuse patterns and can hurt small/reused data. Prefetch intrinsics are hints with architecture-specific fault/cache behavior; they do not validate an address or guarantee residency.

### Arithmetic and floating point

Integer vector code specifies lane width, signedness, overflow, shifts, comparisons, and narrowing. Cryptographic or hash code often requires exact wrapping. Image/audio code may require saturation. Financial or safety code may require checked overflow. One cannot substitute another based on speed.

Floating intrinsics interact with IEEE formats, rounding mode, exception flags, NaNs, infinities, signed zero, subnormals, approximations, and fused operations. A fused multiply-add rounds once and is not bit-identical to separate multiply then add. Reciprocal or reciprocal-square-root estimates need refinement and error analysis. Min/max instruction NaN rules vary by family and may not match language/library functions.

Define equivalence: exact bits, exact value with allowed zero sign, bounded ULP/relative/absolute error, interval containment, or application metric. Combine tolerances carefully near zero and infinities. Use high-precision or independently reviewed reference cases, not the same intrinsic algorithm rearranged.

### Scalable vector intrinsics

Arm SVE and RISC-V V APIs expose vectors whose element count depends on the implementation. Types may be sizeless and therefore forbidden in globals, structure fields, arrays, or `sizeof`. Code creates a predicate or vector length for remaining elements, loads active lanes, computes, stores active lanes, and advances by the number processed.

Never assume one observed length, even when deployment currently uses one CPU. Algorithms with cross-lane permutations, fixed tables, or partial reductions need scalable formulations. Predicated operations often offer merging, zeroing, or don't-care inactive variants; choose from semantic needs and initialization/liveness.

RISC-V V also exposes selected element width and LMUL/grouping, active vector length, tail policy, and mask policy through its intrinsic model. Arm SVE intrinsics encode predicate granularity and operation forms. These are not mechanical renamings of x86 fixed vectors.

### Feature-specific compilation

Compile intrinsic bodies with exactly the required target features. Options can apply to a translation unit, function attribute, or separate object/library. Compiling the whole program for the newest development machine risks executing unsupported instructions before dispatch—in initialization, compiler-generated code, inlined helpers, or unrelated paths.

Place feature-specific code in a clear boundary that prevents accidental inlining into baseline callers unless the compiler's multiversion mechanism safely handles it. Check generated object attributes and disassembly. Ensure build systems compile each object with intended flags and do not let link-time optimization erase isolation without equivalent target handling.

Runtime detection must test architectural feature bits and any OS support for saving/restoring extended vector state. Virtualization can mask features. Cache a validated selection and support a test override. The baseline must avoid optional instructions throughout its call graph.

### ABI and interface design

Do not expose vendor vector types across a broad public ABI unless the ABI explicitly guarantees their calling convention, alignment, target compatibility, and versioning. Passing wide vectors can differ across ABIs or feature levels. A stable boundary commonly accepts ordinary spans/views and returns semantic results; the target-specific implementation owns loads and stores internally.

Contain intrinsics by operation/domain, not by a generic “SIMD utilities” bucket. One module owns semantic reference, dispatch, target variants, tests, benchmarks, and target matrix for a kernel family. Keep policy such as validation, units, and error handling outside duplicated intrinsic bodies.

Use a portable SIMD abstraction when several ISAs share operations and the abstraction produces adequate code. Use a reviewed library when the problem is a standard primitive such as compression, image transform, crypto, BLAS, or math. Intrinsics are justified for measured gaps, missing operations, or stable kernel ownership.

### Tails and boundaries

Fixed-width implementations process full groups and then use scalar tail, masked tail, smaller-width variants, or proven padding. Zero length, less than one vector, exact width, width plus one, and page-end buffers all need tests. Never perform an ordinary full load beyond the object and blend away results.

For a scalar tail, ensure it uses identical arithmetic and error policy. A saturating vector body plus wrapping scalar tail creates length-dependent results. For a masked tail, inactive lanes must not read/write or raise forbidden effects under the actual intrinsic specification.

Scalable loops naturally predicate remaining elements, but still require progress when remaining is zero, correct active count, safe pointers, and no use of unspecified inactive lanes. A reduction must ignore inactive tail elements with a valid identity or explicit predicate.

### Generated-code review

Inspect the exact target binary. Confirm intended instructions, operand widths, mask forms, immediate values, loads/stores, shuffles, conversions, reduction order, and absence of unintended spills/scalar calls. An intrinsic may create extra moves because types or ABI force transitions. Mixing vector widths can have target-specific transition costs.

Count instructions cautiously: throughput, latency, port pressure, dependencies, memory, frequency, and code size matter. Vendor latency/throughput tables are microarchitecture-specific and may assume operand conditions. Use a dependency-aware model and measurement.

For constant-time security, review both source semantics and generated instructions. Variable-time gathers, table lookups, branches, divisions, or special data-dependent instructions may leak. Compiler changes can alter code; pin and re-audit qualified artifacts.

### Verification strategy

Start with an independently understandable scalar/reference function. Generate lane-distinct tests that expose ordering and shuffle mistakes. Exhaust small domains for byte operations where feasible. Test min/max, overflow edges, every shift/control immediate, all mask patterns for small widths, tail lengths, misalignment, supported overlap, guard pages, duplicate indices, exceptional floating values, and randomized inputs.

Force each feature variant and fallback, compare logical results, and run sanitizers. Run on real target hardware or a qualified emulator for compatibility; emulator timing is not performance evidence. Cross-compile with every supported compiler and version. Test debug and optimized builds because undefined assumptions can hide in one.

Round-trip conversion tests alone can share inverse bugs. Use golden vectors from specifications or independent implementations. For crypto, use official known-answer and differential tests plus side-channel analysis. For numeric kernels, recompute high-precision and boundary cases.

### Performance and lifecycle

Benchmark scalar, auto-vectorized, portable SIMD/library, and intrinsic implementations under identical semantics. Include realistic lengths/tails, alignment, data distributions, cache states, concurrency, target hosts, and dispatch. Measure complete API time and path-selection rate. Report binary/toolchain/flags/ISA, hardware, OS, repetitions, uncertainty, and correctness result.

An intrinsic win must exceed maintenance cost: additional code, compiler matrices, hardware access, dispatch, security review, and future ISA work. Record the reason and retirement condition. Compiler improvements may make the intrinsic path slower than clear source later; re-evaluate periodically.

Deprecate unsupported feature variants explicitly, retaining tests while deployed binaries exist. Never silently change arithmetic or mask policy during porting. Treat intrinsic reference errata and compiler bugs as dependency events with qualification and rollback.

## Definitions and Notation

- `F`: target-independent semantic operation over logical inputs.
- `V_P`: intrinsic implementation requiring capability/precondition P.
- `S`: baseline/reference-compatible fallback.
- `P_hw`: required architectural feature predicate.
- `P_os`: required operating-system vector-state support.
- `W`: fixed vector width in bits when applicable.
- `e`: lane element width in bits.
- `L=W/e`: fixed nominal lane count.
- `k_l`: activity of lane l.
- `src_l`: merge passthrough value for inactive lane l.
- `VL`: runtime active/available scalable vector length.
- `I`: immediate operand constrained at compile time.
- `O`: required observable-equivalence relation.
- `B`: exact build, toolchain, flags, headers, target, and binary identity.

Correct dispatch requires `(P_hw ∧ P_os ∧ other_preconditions) ⇒ select V_P`; otherwise select S. Both must refine F under O.

## Mechanisms, Invariants, or Proof Structure

### Lane refinement proof

For every active lane l, show the intrinsic operation produces F's result for the corresponding logical input under actual element and arithmetic semantics. For inactive lanes, show merge/zero/unspecified behavior is never observed contrary to F. Prove lane mapping, conversions, shuffles, and tails cover each logical element exactly once.

### Memory-safety proof

For every active memory lane, prove address formation is defined, overflow-free, aligned as required, and within a live object with permitted access. For inactive lanes, cite the exact fault/access suppression rule. Prove scatter collisions and ordering meet F or route them elsewhere.

### Dispatch proof

Partition executions by validated P. Feature-specific code is unreachable before P, including initialization/inlining. P=true selects a compatible `V_P`; P=false selects S. Both share the same input validation and output/error contract. Forced-path tests witness every branch.

### Scalable-loop proof

At index i<n, establish `0<VL≤n-i`, activate exactly indices `[i,i+VL)`, preserve F per active lane, and advance i by VL. The interval shrinks, so the loop terminates and covers `[0,n)` without overlap. Tail/inactive behavior remains safe for every permitted hardware length.

### Porting invariant

Each target variant implements semantic operations named independently of ISA spelling. Golden/differential tests and boundary matrices are shared. Adding or changing an ISA cannot change F, dispatch fallback coverage, error policy, or external ABI without a separately reviewed API change.

## Alternatives and Trade-Offs

| Approach | Main benefit | Principal limitation |
|---|---|---|
| Clear scalar source | simplest reference and portability | may not expose specialized instructions |
| Auto-vectorization | target-aware with low source duplication | compiler may miss required mapping |
| Standard/portable SIMD | shared explicit vector semantics | availability and lowering vary |
| Reviewed library kernel | externalized optimization and target matrix | dependency/API/accuracy constraints |
| Vendor intrinsics | precise access to ISA semantics | variants, dispatch, tests, maintenance |
| Compiler builtins/extensions | broader operation vocabulary | compiler-specific contracts |
| Inline assembly | maximal encoding control | optimization, ABI, safety, portability burden |

Escalate only as far as evidence requires. Keep a stable semantic API and reference regardless of implementation mechanism.

## Failure Modes and Misconceptions

- **“One intrinsic means one instruction.”** lowering can expand, fold, or scalarize.
- **“Same bits mean same numeric conversion.”** bitcasts and conversions differ.
- **“Packed add is saturation.”** ordinary integer lanes commonly wrap.
- **“Signed and unsigned compare share ordering.”** high-bit values reverse interpretation.
- **“A blend suppresses faults.”** unmasked operands may already have executed.
- **“All masks use all-one lanes.”** dedicated predicates and granularities differ.
- **“Shuffle indices are universal.”** lane groups and source conventions vary.
- **“Immediate operands accept runtime values.”** many must be compile-time constants.
- **“Aligned allocation makes every view aligned.”** offsets change effective alignment.
- **“Scatter order is scalar order.”** duplicates may be unordered.
- **“Compile native and dispatch later.”** optional instructions can escape before checks.
- **“CPUID alone is sufficient.”** OS extended-state support can be required.
- **“Wide vector types are a stable API.”** ABI and target feature rules differ.
- **“SVE/RVV are wider fixed vectors.”** their sizeless types and progress model are scalable.
- **“The scalar tail is trivial.”** it can differ in saturation, rounding, or exceptions.
- **“Passing vectors proves constant time.”** memory and instruction latency still matter.

## Worked Examples

### Example 1

**Overflow contract.** Unsigned byte lanes 250 and 10 produce 4 with wrap and 255 with saturation. **Conclusion:** select an operation from application semantics, not mnemonic familiarity.

### Example 2

**Signed comparison.** Byte bit pattern `0xFF` is −1 signed and 255 unsigned; comparing it with 1 yields opposite order. **Conclusion:** signedness is observable.

### Example 3

**Shuffle audit.** Four input lanes carry `[10,20,30,40]`; reversal must produce `[40,30,20,10]`. Unique sentinels reveal a mistaken pair-local shuffle yielding `[20,10,40,30]`. **Conclusion:** lane tables beat visual intuition.

### Example 4

**Masked tail fault.** Two valid elements remain before a guard page. A specified fault-suppressing masked load activates two lanes; full load plus blend can fault. **Conclusion:** mask placement is part of memory safety.

### Example 5

**Immediate control.** A byte-align intrinsic requires constant shift 0–31, but input chooses shift at runtime. Use a bounded switch of constant cases or a variable-index construction. **Conclusion:** encoding constraints shape APIs.

### Example 6

**Feature escape.** An AVX-specific helper is inlined into baseline initialization by LTO and executes before dispatch on an older host. Separate target functions and audit the binary/call graph. **Conclusion:** dispatch safety is a build property.

### Example 7

**Scalable tail.** At i=13,n=20 the runtime selects VL=5, then VL=2. Predicates cover `[13,18)` and `[18,20)`. **Conclusion:** scalable progress follows returned active count.

### Example 8

**FMA difference.** Separate multiply/add rounds twice; fused form rounds once and can change low bits or exceptions. **Conclusion:** fewer instructions may implement a different numeric contract.

### Example 9

**Intrinsic regression.** A formerly direct intrinsic expands to several instructions under a new target/compiler while auto-vectorized source improves. Periodic benchmark and assembly review retires it. **Conclusion:** explicit code is not permanently optimal.

### Example 10

**Cryptographic authentication kernel.** Intrinsic code must preserve the algorithm's exact modular/bit semantics, bounds, endianness, lane ordering, key erasure, feature dispatch, ABI, known-answer results, constant-time requirements, and fault behavior. Named cryptography, protocol, compiler/ISA, microarchitecture, platform, side-channel, secure-coding, operations, compliance, and independent security reviewers must approve the primitive and artifact; none is claimed here. **Conclusion:** functional SIMD speedup neither validates cryptography nor proves side-channel resistance.

## Cross-Program Connections

- **Programming languages:** UB, lifetime, aliasing, conversions, and ABI constrain intrinsic wrappers.
- **Compiler construction:** builtins, target features, legalization, scheduling, and register allocation still own lowering.
- **Computer architecture:** operation semantics, masks, immediates, ports, state, and feature discovery define targets.
- **Algorithms:** semantic wrappers isolate maps, reductions, scans, permutations, and packed transforms.
- **Numerical computing:** saturation, rounding, FMA, approximations, and reductions require explicit contracts.
- **Security:** constant-time behavior, feature dispatch, key handling, and compiler changes need separate evidence.
- **Testing:** golden vectors, lane sentinels, exhaustive byte domains, differential paths, and guard pages expose defects.
- **Build engineering:** target flags, LTO, multiversioning, headers, binaries, and host matrices determine reachability.
- **Performance engineering:** generated-code and workload measurements determine whether ownership pays.
- **Software architecture:** containment boundaries prevent ISA mechanics from duplicating domain policy.

## References

1. Intel, *Intel Intrinsics Guide*, version 3.6.9; retrieved 2026-08-29. <https://www.intel.com/content/www/us/en/docs/intrinsics-guide/index.html>
2. Intel, *Intel 64 and IA-32 Architectures Software Developer's Manuals*, version 092; retrieved 2026-08-29. <https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html>
3. Arm, *Arm C Language Extensions*, current specification; retrieved 2026-08-29. <https://arm-software.github.io/acle/main/acle.html>
4. Arm, *Arm Neon Intrinsics Reference*, current specification; retrieved 2026-08-29. <https://arm-software.github.io/acle/neon_intrinsics/advsimd.html>
5. RISC-V International, *RISC-V Vector C Intrinsic Specification v1.0*, ratified 2025-04-25. <https://docs.riscv.org/reference/vector-c-intrinsics/index.html>
6. GNU Project, *Using Vector Instructions through Built-in Functions*, current GCC documentation; retrieved 2026-08-29. <https://gcc.gnu.org/onlinedocs/gcc/Vector-Extensions.html>
7. Clang Project, *Clang Language Extensions: Vectors and Extended Vectors*, current documentation; retrieved 2026-08-29. <https://clang.llvm.org/docs/LanguageExtensions.html#vectors-and-extended-vectors>
8. Matthias Kretz, *std::simd — Merge Data-Parallel Types from the Parallelism TS 2*, WG21 P1928R15, 2024. <https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p1928r15.pdf>
9. LLVM Project, *LLVM Language Reference Manual: Masked Vector Intrinsics*, current documentation; retrieved 2026-08-29. <https://llvm.org/docs/LangRef.html#masked-vector-intrinsics>
10. IEEE, *IEEE Standard for Floating-Point Arithmetic*, IEEE 754-2019. <https://doi.org/10.1109/IEEESTD.2019.8766229>

## Exercises

### Exercise 1

Specify semantic wrappers for wrapping u16 addition, saturating u16 addition, signed i16 maximum, and bitwise selection. State edge cases that distinguish them.

### Exercise 2

Design a fixed-width masked transform for arbitrary n with scalar and masked-tail alternatives. Prove bounds and arithmetic equivalence.

### Exercise 3

Design a baseline plus two-ISA dispatch boundary robust to OS-state requirements, LTO, virtualization, tests, and ABI evolution.

### Exercise 4

Port a fixed four-lane permutation/reduction algorithm to a scalable-vector target. Identify which assumptions must be reformulated and how to validate every VL.

### Exercise 5

A healthcare image codec uses intrinsics for packed conversion. Define numeric, memory, interoperability, dispatch, performance, privacy, and human-review evidence for production.

## Answers to the Exercises

### Answer 1

Define `add_wrap_u16(a,b)` as `(a+b) mod 2^16` per lane; edge `65535+1→0`. Define `add_sat_u16` as `min(65535,a+b)` in a sufficiently wide intermediate; the same edge yields 65535. Define `max_i16` by signed range −32768..32767; bit pattern `0xFFFF` denotes −1, so max with 1 is 1, unlike unsigned. Define `select_bits(mask,a,b)` bitwise as `(mask & a) | (~mask & b)` only if arbitrary-bit mask is intended; lane-boolean selection instead chooses whole lanes and requires canonical truth semantics. Test zero, maxima/minima, high-bit values, overflow, noncanonical masks, all lanes, and scalar/intrinsic/fallback variants. Wrapper names and types encode the contract independently of ISA spelling.

### Answer 2

Specify pointwise F and choose width L. Full loop processes bases while `base+L≤n`, using only proven valid loads/stores. Option A runs scalar F for indices from the full prefix to n. Option B constructs mask `k_l=(base+l<n)` and uses specified fault-suppressing masked load/store; inactive results cannot be observed and unsafe operations are also predicated. Prove Euclidean grouping covers `[0,n)` exactly once, full ranges are within allocation, active tail addresses are valid, inactive addresses are not accessed, and vector/scalar operations share signedness, saturation/wrap, rounding, NaN, and exception policy. Test n=0,1,L−1,L,L+1,multiples, guard-page endpoints, alignment classes, exceptional values, and forced variants.

### Answer 3

Expose one ordinary-span semantic API and keep vector types internal. Compile baseline, ISA-A, and ISA-B functions with exact per-function or per-object features. Prevent cross-target inlining or configure supported multiversioning; inspect LTO output for optional instructions in baseline/startup. Dispatcher checks hardware bits, OS extended-state enablement, configuration, and any ABI/platform constraints, then caches a function pointer. Unknown/virtualized/reduced features choose baseline. Provide forced-path tests, feature masking, actual hosts/emulator compatibility, startup/static-initializer audit, binary disassembly, and fallback availability. Version the API semantically; target objects may change without ABI exposure. Record toolchain/flags/headers/binary and have a safe rollback.

### Answer 4

Fixed assumptions include lane count four, constant shuffle indices, one-register reduction tree, tail width, vector storage/`sizeof`, and perhaps ABI passage. Reformulate the algorithm around predicates and current active VL, with progress by returned VL. For a global permutation or reduction, define logical index mapping independent of register lanes; use scalable table/permutation operations, segmented processing, and a specified cross-segment combine tree. Do not store sizeless types in persistent objects. Test emulator/hardware configurations for every supported VL when possible, plus logical lengths around each VL, unique lane sentinels, tails, masks, and exceptional arithmetic. Compare to an independent scalar reference and inspect generated instructions. State whether results are bitwise stable across VL; floating reductions generally need a fixed logical tree to claim that.

### Answer 5

Specify pixel format, channel order, bit depth, signedness, range, saturation/rounding, color transform, alpha, endianness, padding, malformed-stream behavior, and exact/tolerant output relation. Prove active address bounds, overflow-safe sizes/strides, tail fault suppression, alignment, alias policy, lane/shuffle mapping, and scalar-tail equality. Decode untrusted dimensions before allocation and fuzz metadata; use guard pages and sanitizers. Maintain baseline plus isolated target variants with hardware/OS dispatch, forced tests, golden codec vectors, round trips against independent implementations, every feature/length/alignment case, and binary inspection. Measure complete decode/encode latency, throughput, memory peak, energy if relevant, and path rate on deployment classes. Minimize/encrypt patient images and artifacts, audit access, and define retention/deletion. Named imaging/codec, clinical-domain, numerical/color, compiler/ISA, hardware/platform, software-safety, security/privacy, interoperability, operations, quality/regulatory, and independent validation reviewers approve requirements and limitations. Speed and round-trip samples are not diagnostic validity or clinical approval.
