---
module_id: CONPAR-071
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 71
title: SIMD Execution and Vector Lanes
status: complete
last_verified: 2026-08-29
---

# SIMD Execution and Vector Lanes

## One-Page Review

### Governing question

When may several scalar operations be represented by one vector operation without changing required behavior, and what lane, mask, memory, arithmetic, and portability contracts must remain true?

### Essential definitions

- **single instruction, multiple data (SIMD)** applies one encoded operation to several data elements held in vector lanes.
- A **lane** is one element position in a vector operation; lane count depends on register width, element width, and architecture configuration.
- The **vectorization factor** (VF) is the number of scalar iterations represented by a vector iteration; it need not equal one physical register's lane count after unrolling or grouping.
- An **active mask** or **predicate** selects lanes whose operation has semantic effect.
- A **tail** is the final partial group when the scalar trip count is not divisible by VF.
- **if-conversion** represents control flow as predicated data flow, often executing operations from multiple paths under different masks.
- A **contiguous** vector access touches adjacent elements; **gather** and **scatter** use per-lane addresses.
- A **horizontal operation** combines lanes, as in a reduction; a **vertical operation** computes each result lane independently.
- **fixed-width SIMD** exposes a particular architectural vector width; **scalable SIMD** permits an implementation-selected width and supports vector-length-agnostic code.
- **SPMD-on-SIMD** maps several logical program instances to lanes while a compiler manages masks and varying control flow.

### Central model, mechanism, or theorem

For scalar iterations `i=0..n-1`, group indices `b+l`, where b advances by VF and `0≤l<VF`. Set mask `m_l=(b+l<n)` and compute each active lane with the scalar operation for index `b+l`. This transformation preserves pointwise results if active iterations are independent, each lane observes permitted scalar values, inactive lanes cause no forbidden effect, and arithmetic/order rules meet the specification. Reductions additionally require a permitted association order. This is a conditional semantic argument, not a speed claim.

### Critical invariants

Every required scalar iteration is represented exactly once; no out-of-range lane performs a visible or faulting access; masks follow the ISA's merge/zero and fault-suppression rules; dependence and alias claims are true for every runtime input; duplicate scatter destinations have defined resolution; integer width and floating-point contraction/reassociation satisfy the numeric contract; feature dispatch checks hardware and operating-system support; scalable code never embeds an assumed vector length; scalar and vector versions share input, error, and side-effect semantics; and performance is measured on representative hardware and data.

### Common failures

Engineers confuse SIMD with threads, count bits rather than element lanes, read beyond a buffer in a tail, assume a masked expression suppresses all exceptions, promise false alignment or non-aliasing, vectorize a loop-carried dependence, scatter duplicate indices, change a reduction tree without permission, overlook NaN/signed-zero/FMA behavior, hard-code an SVE or RISC-V vector length, dispatch on CPU identity without OS state support, benchmark only warm aligned arrays, or infer correctness or speed from vector-looking source.

### Compact example

Ten elements processed at VF=4 form masks `1111`, `1111`, and `1100`. The final two inactive lanes must neither load nor store elements 10 and 11. Twelve lane slots are issued for ten useful elements, so tail lane utilization is `10/12`, but this ratio alone predicts neither throughput nor latency.

### Connections

[Work Partitioning and Granularity](045-work-partitioning-and-granularity.md) reasons about useful work per scheduling unit; SIMD adds sub-thread lane utilization. [Parallel Functional Evaluation](068-parallel-functional-evaluation.md) supplies independence and work/span reasoning. The [program roadmap](../ROADMAP.md) continues with data layout, compiler vectorization, intrinsics, GPUs, and accelerator pipelines.

## Governing Question

How should a programmer or compiler establish that lane-wise execution is semantically legal, memory safe, numerically acceptable, portable across vector widths, and actually beneficial for a concrete workload?

The answer requires three separate judgments: a legality proof about behavior, a mapping choice about instructions and masks, and an empirical profitability decision. A compiler remark or SIMD instruction can provide evidence for the latter two, but neither discharges the first for an incorrectly specified program.

## Why This Matters

Modern CPUs devote substantial execution resources to vector operations. Image, signal, simulation, database, cryptographic, machine-learning, and numerical kernels commonly perform the same operation across large collections. Using several lanes per instruction can reduce instruction-fetch, decode, loop-control, and dependency overhead while increasing arithmetic and memory throughput.

SIMD is also a semantic pressure test. Transforming a scalar loop exposes assumptions about independence, aliasing, bounds, exceptions, arithmetic, and observable order. Those assumptions often existed implicitly and sometimes falsely. A scalar implementation may appear correct only because its particular order hides a dependency or because undefined behavior happens not to fail.

The programming landscape includes fixed-width x86 SSE/AVX and Arm Advanced SIMD, scalable Arm SVE and RISC-V V, compiler auto-vectorizers, portable vector abstractions, explicit intrinsics, and SPMD languages. Their surface syntax differs, but the enduring questions are identical: which indices occupy lanes, which lanes are active, what addresses they touch, what result ordering is permitted, and how the program selects a supported implementation.

## Prerequisites and Retrieval

Retrieve:

- independence, work, span, and granularity from [Parallel Functional Evaluation](068-parallel-functional-evaluation.md);
- compiler and hardware observability distinctions from [Compiler and Processor Reordering](021-compiler-and-processor-reordering.md);
- race and ordering vocabulary from [Happens-Before Relations](023-happens-before-relations.md); and
- reproducible numeric inputs from [Reproducible Randomness in Parallel Programs](069-reproducible-randomness-in-parallel-programs.md).

Retrieval prompt: for a loop with iteration function `F(i)`, list every read, write, exception, and externally visible event. Which pairs of iterations may conflict? Which events may change if the iterations are grouped or reordered?

## Learning Objectives

After completing this module, a learner can:

1. distinguish SIMD, SIMT, SPMD, instruction-level parallelism, and thread parallelism;
2. derive lane count, vectorization factor, active masks, and tail utilization;
3. prove legality for pointwise maps and identify loop-carried and alias dependences;
4. explain predication, divergence, merge/zero behavior, and masked exceptions;
5. compare contiguous, strided, interleaved, gather, scatter, and permuted access;
6. analyze reductions under integer and floating-point semantic constraints;
7. write vector-length-agnostic loop logic without assuming hardware width;
8. design safe feature dispatch, scalar fallback, and compatibility testing;
9. interpret vectorization reports, disassembly, counters, and benchmarks; and
10. build review evidence for safety- or correctness-critical vector kernels.

## Core Exposition

### Separate execution models

Flynn's taxonomy calls an organization with one instruction stream operating on multiple data streams SIMD. A vector instruction such as lane-wise addition conceptually reads corresponding elements from two vector operands and produces corresponding result elements. This differs from instruction-level parallelism, where a core overlaps independent scalar instructions, and from MIMD thread parallelism, where workers follow independent instruction streams.

SIMT, commonly used to describe GPUs, presents many scalar-like threads grouped for execution; hardware schedules groups in lockstep or converged subsets. SPMD is a programming model in which many logical instances run the same program on different data. A compiler such as ISPC can map SPMD instances onto CPU SIMD lanes. The programmer may write scalar-looking control flow, but varying conditions become masks. These terms describe distinct abstraction layers and should not be used as synonyms.

### Lanes, widths, and vectorization factor

For a fixed W-bit vector holding e-bit elements, the nominal lane count is `L=W/e`. A 256-bit operand therefore holds eight 32-bit elements or four 64-bit elements. This arithmetic says nothing about instruction latency, throughput, number of execution units, or whether an operation exists for that element type.

VF describes the compiler transformation. A VF of eight means one vector-loop iteration represents eight scalar iterations. Unrolling by two can operate on sixteen elements with two eight-lane instructions. Conversely, a wide logical vector may lower to several machine instructions. Treat source vector length, transformation VF, architectural width, and physical datapath width as separate facts.

Fixed-width code selects concrete types or intrinsics. Scalable architectures expose a vector length chosen by the implementation within architectural limits. RISC-V V records active vector length `vl` and vector type; Arm SVE uses predicates and instructions that derive progress from the available length. Correct vector-length-agnostic code queries or establishes the active element count, processes it, advances by that count, and repeats. Hard-coding the width defeats binary portability and often breaks the last group.

### Mapping scalar iterations to lanes

Consider a pointwise loop `y[i]=f(x[i])`. Select base b and map lane l to scalar index `i=b+l`. Full groups have every lane active. At the tail, predicate `m_l=(i<n)` determines activity. Correctness requires coverage—each valid i occurs—and exclusivity—no valid i is emitted twice unless the scalar specification calls for it.

The following executable teaching model makes the mapping visible. It simulates masks sequentially; it does not execute a vector ISA, model masked fault rules, or measure SIMD performance.

<!-- bijux-verify: {"id":"predicated-tail-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"width=4\nmasks=[[True, True, True, True], [True, True, True, True], [True, True, False, False]]\nsquares=[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]\nactive_lanes=10\nissued_lanes=12\nutilization=0.833\nscalar_match=True\n","stderr":""}} -->
```python
values = list(range(1, 11))
width = 4
masks = []
result = []

for base in range(0, len(values), width):
    mask = [base + lane < len(values) for lane in range(width)]
    masks.append(mask)
    for lane, active in enumerate(mask):
        if active:
            value = values[base + lane]
            result.append(value * value)

active_lanes = sum(sum(mask) for mask in masks)
issued_lanes = len(masks) * width
print(f"width={width}")
print(f"masks={masks}")
print(f"squares={result}")
print(f"active_lanes={active_lanes}")
print(f"issued_lanes={issued_lanes}")
print(f"utilization={active_lanes / issued_lanes:.3f}")
print(f"scalar_match={result == [value * value for value in values]}")
```

### Predication and varying control flow

If lanes disagree on a branch condition, a vector implementation may if-convert the branch. It evaluates the true path under one mask and the false path under its complement, then merges results. This preserves per-lane choices when operations are safe to predicate and side effects occur only for the appropriate active lanes.

Predication is not free. Both paths may consume issue bandwidth, so effective utilization declines when masks are sparse. A uniform condition can take one branch for the whole group. Rearranging or sorting work to increase coherence may help, but its data-movement cost and semantic effect must be counted.

Mask semantics are instruction-specific. An inactive destination may retain its old value (merging) or become zero. Some masked memory operations suppress access and faults for inactive lanes; other source-language expressions may have already formed an invalid pointer or performed an unsafe operation before a later select. Floating exceptions, integer traps, function calls, volatile access, atomics, and language undefined behavior require exact compiler and ISA rules. “The result is masked away” is not a general safety proof.

### Tail strategies

A scalar epilogue processes full vectors and then runs scalar iterations for the remainder. It is simple and often profitable, but adds control flow and may be inefficient for short arrays. A masked tail executes one partial vector and suppresses inactive lanes. Padding rounds storage to a safe size, but only works when allocation, initialization, object lifetime, and externally visible stores permit access to padding. Peeling can process early elements until a preferred alignment, followed by a vector body and tail.

Tail folding predicates iterations throughout a vector loop rather than creating a scalar epilogue. The best strategy depends on trip-count distribution, mask cost, exception rules, code size, branch prediction, and architecture. None permits an ordinary out-of-bounds language access merely because the hardware load would stay within a mapped page.

### Memory access shapes

Contiguous unit-stride loads and stores are the most direct mapping: adjacent lanes touch adjacent elements. Interleaved structures may require deinterleave/interleave operations or shuffles. Strided access can waste transferred cache-line bytes. Gather loads and scatter stores accept per-lane addresses, enabling irregular algorithms but adding address generation, cache/TLB pressure, and often greater latency.

Alignment describes address divisibility. Some instructions require alignment; many modern instructions support unaligned addresses with performance dependent on cache-line or page crossings. A compiler annotation promising 64-byte alignment is a semantic assertion, not a request. If false, behavior may be undefined or fault. Prefer an aligned allocator and runtime assertion when the guarantee is part of the interface.

Aliasing is equally important. If `x` and `y` may overlap, storing `y[i]` can change a value a later lane reads from `x`. A compiler may emit runtime disambiguation: test whether accessed ranges overlap, use a vector version if they do not, and retain a scalar version otherwise. Language qualifiers or assumptions that promise non-aliasing are safe only when callers enforce them.

Scatter needs a collision contract. If two active lanes store the same destination, an ISA may leave the winner unspecified or define an order different from the scalar loop. Atomic scatter-like updates require dedicated operations or conflict handling. A uniqueness proof, conflict detection, sorting/combining, or scalar fallback is necessary when duplicate destinations matter.

### Dependences and legality

A pointwise map has no loop-carried dependence when iteration i reads only immutable inputs for i and writes a unique output i. A recurrence such as `a[i]=a[i-1]+x[i]` carries a true dependence: iteration i requires the result of i-1. Executing lanes as independent additions changes the algorithm. Specialized scans can parallelize the recurrence, but they use a different dependency graph and proof.

Dependence distance matters. If iteration i writes a location read by `i+d`, VF must respect the semantic ordering or the transformation must handle the recurrence explicitly. OpenMP's `safelen` communicates a minimum distance constraint; falsely asserting it produces an incorrect program. Compiler legality analysis reasons about memory, control, calls, and recurrences, but its conclusions depend on the source language and supplied assumptions.

Volatile and device memory accesses are observable operations whose count and order may be contractual. Atomics do not automatically make lane grouping legal: ordering, return values, contention, and duplicated addresses still matter. Vectorization operates within, not outside, the language memory model.

### Reductions and arithmetic semantics

A reduction combines many values into one. Vector code commonly accumulates partial sums per lane and horizontally combines them. For mathematical real addition, association is irrelevant. Fixed-width modular integer addition is associative, although signed overflow may be undefined, trapping, or wrapping depending on language and mode. Saturating addition is not generally associative.

IEEE 754 floating addition is not associative because rounding occurs after operations. A scalar left fold and a balanced vector tree can produce different finite results; NaNs, infinities, signed zeros, subnormals, exception flags, and fused multiply-add contraction add more distinctions. A compiler needs permission—explicit fast-math rules, a reduction construct, or a language guarantee—to reassociate. A production numerical specification should state whether it requires bitwise identity, correctly rounded output, bounded error, reproducibility under a fixed tree, or statistically acceptable tolerance.

Minimum and maximum also need NaN and tie rules. Integer narrowing needs a specified wrap, saturation, or trap. Shifts need valid counts and signedness. Vectorizing an underspecified arithmetic contract simply makes discrepancies harder to diagnose.

### Compiler mapping and evidence

Auto-vectorization normally has legality and profitability stages. LLVM's loop vectorizer widens independent loop iterations; its SLP vectorizer packs isomorphic scalar operations. Its VPlan representation models candidates, costs, masks, reductions, and generated control flow. A compiler may decline vectorization because it cannot prove alias freedom, a call lacks a vector form, a trip count is small, or gather/scatter costs exceed estimated gain.

Use optimization remarks to learn whether and why a loop vectorized. Inspect generated intermediate representation or assembly to identify vector instructions, masks, versioning checks, and tails. Confirm the executed path with representative inputs. Hardware counters can report instructions, cycles, cache/TLB misses, branches, and architecture-specific vector events. Each source answers a different question; source syntax alone answers none of them conclusively.

### Profitability and the memory system

Peak lane count is an upper bound, not expected speedup. A kernel may be limited by memory bandwidth, cache misses, dependency latency, instruction throughput, gathers, shuffles, reductions, front-end pressure, or scalar setup. Wider vectors can increase register pressure and spills. On some processor families, instruction mix and vector width affect frequency or power behavior; measure the exact deployed systems rather than transferring folklore.

Benchmark end-to-end behavior and isolated kernels. Include cold and warm data, realistic sizes and tails, alignment distributions, alias/version paths, sparse masks, irregular indices, NUMA placement, and concurrent load. Account for conversion and layout transformation. Report compiler, flags, binary, ISA path, hardware, firmware/OS, clock policy, repetitions, uncertainty, and correctness oracle.

### Dispatch and portability

A binary may ship a baseline scalar or conservative-vector implementation plus ISA-specific versions. Runtime dispatch must check architectural feature bits and any operating-system support required to save/restore extended vector state. Virtual machines and containers may expose a reduced feature set. Cache a validated dispatch decision, but provide deterministic overrides for testing and diagnosis.

Test every version against one specification and scalar oracle, including zero length, lengths around vector boundaries, misalignment, overlap according to the interface, exceptional numeric values, and page-boundary guards. Test forced feature absence and invalid configuration. Never execute an unsupported instruction merely to discover support by crash in ordinary application flow.

Scalable-vector code should express progress in elements returned active for the current iteration. Fixed-width assumptions can enter through buffer sizes, shuffle constants, loop increments, or reduction layout even if the main arithmetic uses scalable types. Portability includes semantic portability across endianness, element types, ABI, compiler versions, and floating modes—not just successful compilation.

### Verification ladder

Start with a scalar reference whose specification is independent of the vector implementation. Use exhaustive tests for small finite domains where possible, property tests for coverage and non-interference, adversarial lengths around every VF, guard pages or sanitizers for bounds, and differential tests across ISA paths. Preserve failing inputs and the selected path.

For arithmetic, recompute exact integer cases and high-precision floating cases; establish error bounds for permitted reordering. For concurrency, run vector kernels under the relevant calling synchronization and memory model. For performance, distinguish empirical measurements from guarantees and monitor regressions by hardware class.

Safety- or security-critical kernels need independent inspection of generated code or a qualified toolchain strategy, requirements traceability, target-specific exception analysis, and named domain review. Passing sample vectors proves only those samples. A vectorized cryptographic loop can be functionally correct yet leak secrets through lane-dependent memory or control; constant-time properties need separate evidence.

## Definitions and Notation

- `W`: architectural or effective vector width in bits for a fixed-width operation.
- `e`: element width in bits.
- `L=W/e`: nominal fixed-width lane count when W is divisible by e.
- `n`: scalar iteration count.
- `VF`: scalar iterations represented by one vector iteration.
- `UF`: vector-loop unroll factor.
- `b`: base scalar index for a vector group.
- `l`: lane index, `0≤l<VF` in the abstract mapping.
- `i=b+l`: scalar iteration represented by lane l.
- `m_l`: predicate indicating whether lane l is active.
- `A_i`: set of memory addresses accessed by scalar iteration i, annotated by read/write mode.
- `d`: loop-carried dependence distance.
- `T_s`, `T_v`: measured scalar and vector execution times under a declared protocol.
- `S=T_s/T_v`: empirical speedup for that protocol.

Lane utilization for one predicated group is active lanes divided by available lane slots. It is a work-shape statistic, not a complete performance model.

## Mechanisms, Invariants, or Proof Structure

### Pointwise preservation proof

Assume scalar iteration i computes deterministic `y[i]=f(x[i])`, reads valid immutable `x[i]`, writes only unique `y[i]`, and has no other observable effect. Partition `[0,n)` into groups by `b=k·VF`; activate l exactly when `b+l<n`. Euclidean division assigns each valid i unique `(k,l)`, proving coverage and exclusivity. Lane independence permits any within-group execution order. Each active lane applies the same f to the same input, so every output equals the scalar result. Inactive lanes have no effect by premise. This proves scoped semantic equality, not profitability or f's correctness.

### Dependence test

For iterations i and j, a conflict exists if their access sets share an address and at least one access writes. Grouping is freely reorderable only when conflicts are absent or the specification permits the resulting order. Static analysis can be conservative; runtime alias checks can refine actual ranges. An asserted no-alias fact transfers proof obligation to the interface and callers.

### Predicated-tail proof obligation

Prove `(m_l=false) ⇒ no forbidden read, write, exception, or visible effect`. This implication depends on source evaluation, lowering, and target instruction semantics. It cannot be inferred solely from the final destination mask.

### Reduction proof obligation

Define scalar fold order and vector combination tree. Prove algebraic equivalence under the operation's actual domain, or state and validate an allowed error/behavior relation. Associativity over mathematical values is insufficient when machine overflow, rounding, exceptions, or NaN policies differ.

### Dispatch invariant

Every selectable implementation refines one interface specification. The dispatcher selects a version only when hardware, OS, ABI, and configuration predicates hold; a supported baseline always remains. Forced-path tests establish that each branch is reachable and independently correct.

## Alternatives and Trade-Offs

| Approach | Main benefit | Principal limitation |
|---|---|---|
| Scalar baseline | simple oracle and broad portability | leaves lane parallelism unused |
| Compiler auto-vectorization | portable source and centralized legality analysis | profitability and proof depend on visible facts |
| Pragmas/directives | communicate intent and verified assumptions | false assertions can change semantics |
| Portable vector abstraction | one source across targets | may obscure exact lowering or miss ISA features |
| Fixed-width intrinsics | precise instruction-level control | high maintenance, dispatch, and tail burden |
| Scalable-vector programming | one binary adapts to implemented VL | demands vector-length-agnostic algorithms |
| SPMD-on-SIMD | natural per-instance control flow | masks, gathers, and divergence remain costly |
| Layout transformation | enables contiguous lanes | conversion, memory, and ownership costs |
| Scalar epilogue | straightforward tail semantics | branches and poor short-loop utilization |
| Predicated tail | uniform loop and safe partial groups when specified | mask and exception semantics are target-specific |

Begin with clear scalar semantics and measured hotspots. Prefer compiler mapping when its report and generated code are adequate. Introduce directives only with checked assumptions, and intrinsics only when enduring performance or semantic needs justify target-specific ownership.

## Failure Modes and Misconceptions

- **“SIMD means eight operations happen simultaneously.”** Architectural lanes do not reveal physical timing.
- **“A 512-bit vector always has sixteen lanes.”** Element width determines lane count.
- **“VF equals register lane count.”** unrolling, legalization, and multiple registers break that identity.
- **“A mask makes every inactive expression safe.”** source evaluation and instruction fault rules matter.
- **“Reading a few bytes past the array is harmless.”** it violates bounds and may cross an unmapped page.
- **“Unaligned means incorrect.”** requirements and costs are instruction- and address-specific.
- **“Alignment annotations align memory.”** they assert a precondition; they do not repair allocation.
- **“`restrict` is an optimization hint.”** it imposes an aliasing contract whose violation is serious.
- **“Atomics make vector scatter safe.”** duplicate destinations and ordering still need semantics.
- **“Floating addition is associative enough.”** acceptable error and exception policy must be explicit.
- **“Fast math only makes code faster.”** it grants transformations that may change observable results.
- **“The compiler said vectorized, so it is faster.”** legality or code generation is not workload measurement.
- **“Vector-looking source guarantees SIMD.”** lowering may scalarize or choose another path.
- **“Scalable vector means use the maximum width.”** code must adapt to the runtime architectural length.
- **“CPU feature bits are enough.”** operating-system extended-state support may also be required.
- **“One benchmark size represents production.”** tails, caches, alignment, masks, and contention vary.

## Worked Examples

### Example 1

**Lane arithmetic.** A 256-bit operation over 32-bit elements has eight nominal lanes; over 64-bit elements it has four. **Conclusion:** vector bits alone do not specify data parallelism.

### Example 2

**Tail mapping.** For `n=10`, `VF=4`, bases are 0, 4, and 8 with masks `1111`, `1111`, `1100`. Every index 0–9 appears once and 10–11 remain inactive. **Conclusion:** bounds are part of lane identity.

### Example 3

**False mask safety.** A source expression loads `x[i]` and then selects zero when `i≥n`. The out-of-range load occurs before the select. Move the predicate into a specified masked load or branch. **Conclusion:** masking a result is not masking an access.

### Example 4

**Loop-carried recurrence.** `a[i]=a[i-1]+x[i]` cannot become independent lane additions because lane i needs lane i-1's new value. A parallel scan is a different algorithm with its own combine phases. **Conclusion:** similar operators do not establish iteration independence.

### Example 5

**Runtime alias versioning.** A compiler tests whether source and destination ranges overlap. It takes a vector path for disjoint ranges and the scalar semantics-preserving path otherwise. **Conclusion:** runtime facts can discharge a legality condition without lying in the type contract.

### Example 6

**Divergent branch.** In an eight-lane SPMD group, three lanes take A and five take B. If both paths execute under complementary masks, useful-lane fractions are `3/8` and `5/8`; sorting may improve coherence but costs movement. **Conclusion:** lane occupancy and algorithmic work distribution interact.

### Example 7

**Duplicate scatter.** Lanes 2 and 6 both write histogram bucket 9. An ordinary scatter cannot be assumed to reproduce scalar last-writer order. Detect conflicts, combine lane contributions, use suitable atomics, or fall back. **Conclusion:** distinct lane IDs do not imply distinct destinations.

### Example 8

**Floating reduction.** Scalar `(10^20 + -10^20) + 3` yields 3 in a common binary format, while `10^20 + (-10^20 + 3)` can yield 0 after rounding. **Conclusion:** a vector reduction tree needs a declared numeric equivalence relation.

### Example 9

**Scalable progress.** A VLA loop requests up to the remaining elements, obtains active count q, processes q under a predicate, and advances by q. Runs with q=4 and q=13 cover the same index interval without recompilation. **Conclusion:** progress derives from active length, not a compiled constant.

### Example 10

**Radiotherapy image kernel.** A vectorized dose-volume computation must preserve voxel bounds, units, calibration, masks, interpolation, overflow/rounding, NaN policy, reduction error, hardware dispatch, and fallback behavior. Validate golden phantoms, guard-page tails, high-precision recomputation, every ISA path, and worst-case error. Named radiation-oncology, medical-physics, numerical-analysis, imaging, SIMD/compiler, hardware, software-safety, quality/regulatory, security/privacy, and independent verification reviewers must approve requirements and evidence; none is claimed here. **Conclusion:** SIMD equivalence evidence cannot establish clinical suitability by itself.

## Cross-Program Connections

- **Programming languages:** aliasing, undefined behavior, exceptions, and floating modes define legal transformations.
- **Algorithms:** maps, scans, reductions, sorting, and conflict resolution expose different lane structures.
- **Computer architecture:** registers, masks, execution ports, caches, TLBs, and frequency govern realized cost.
- **Compilers:** dependence analysis, if-conversion, cost models, multiversioning, and VPlan connect source to ISA.
- **Data systems:** scans, predicates, compression, and joins benefit from vector-at-a-time processing.
- **Machine learning:** tensor kernels combine lane arithmetic with layout, tiling, mixed precision, and accelerators.
- **Security:** constant-time behavior, bounds, dispatch integrity, and side channels require separate verification.
- **Numerical computing:** reduction trees and contraction determine reproducibility and error.
- **Software engineering:** scalar oracles, differential tests, benchmarks, and ownership keep optimized paths maintainable.
- **Safety engineering:** target-specific evidence and named domain review bound high-stakes claims.

## References

1. Michael J. Flynn, “Some Computer Organizations and Their Effectiveness,” *IEEE Transactions on Computers* C-21(9), 1972. <https://doi.org/10.1109/TC.1972.5009071>
2. Intel, *Intel 64 and IA-32 Architectures Software Developer's Manuals*, version 092; retrieved 2026-08-29. <https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html>
3. Intel, *Intel 64 and IA-32 Architectures Optimization Reference Manual*, version 050; retrieved 2026-08-29. <https://www.intel.com/content/www/us/en/developer/articles/technical/intel64-and-ia32-architectures-optimization.html>
4. Arm, *A Sneak Peek into SVE and VLA Programming*, 2020. <https://developer.arm.com/-/media/Arm%20Developer%20Community/Images/White%20Paper%20and%20Webinar%20Images/HPC%20White%20Papers/a-sneak-peek-into-sve-and-vla-programming.pdf>
5. RISC-V International, *“V” Standard Extension for Vector Operations, Version 1.0*, ratified specifications library; retrieved 2026-08-29. <https://docs.riscv.org/reference/isa/unpriv/v-st-ext>
6. LLVM Project, *Auto-Vectorization in LLVM*, current documentation; retrieved 2026-08-29. <https://llvm.org/docs/Vectorizers.html>
7. LLVM Project, *Vectorization Plan*, current documentation; retrieved 2026-08-29. <https://llvm.org/docs/VectorizationPlan.html>
8. OpenMP Architecture Review Board, *OpenMP API Specification 5.2: SIMD Construct*, November 2021. <https://www.openmp.org/spec-html/5.2/openmpse60.html>
9. Matt Pharr and William R. Mark, “ispc: A SPMD Compiler for High-Performance CPU Programming,” *Innovative Parallel Computing*, 2012. <https://ispc.github.io/papers/ispc_inpar_2012.pdf>
10. IEEE, *IEEE Standard for Floating-Point Arithmetic*, IEEE 754-2019. <https://doi.org/10.1109/IEEESTD.2019.8766229>

## Exercises

### Exercise 1

For `n=23`, fixed `VF=8`, derive every base, active mask, useful/issued lane count, and tail utilization. Explain why utilization does not predict speedup.

### Exercise 2

Analyze legality for `y[i]=x[i]+x[i-1]`, `i=1..n-1`, under disjoint x/y and then under `y=x`. State exact conflicts and propose correct implementations.

### Exercise 3

Design scalar, fixed-width, and vector-length-agnostic implementations of a clamped transform. Specify tails, aliasing, integer/floating behavior, dispatch, and differential tests.

### Exercise 4

Compare scalar epilogue, masked tail, and padding for a service whose message lengths cluster around 15, 16, and 17 elements and whose buffers may end at a guard page.

### Exercise 5

A genomics service vectorizes a base-quality filter and reduction on heterogeneous hosts. Create a correctness, performance, compatibility, privacy, and human-review plan suitable for a regulated decision-support pipeline.

## Answers to the Exercises

### Answer 1

Bases are 0, 8, and 16. The first two masks are `11111111`; the last is `11111110`, where lane 7 represents invalid index 23. Useful lanes are 23 and issued slots are 24, so utilization is `23/24≈0.9583`. This says only one tail slot is inactive. It omits instruction availability, latency/throughput, memory bandwidth and locality, setup, masks, alignment, dependencies, scalar/vector clock behavior, and measurement noise. Speedup must compare validated implementations under a declared workload protocol.

### Answer 2

With disjoint x and y, iteration i reads immutable `x[i]` and `x[i-1]` and writes unique `y[i]`; adjacent iterations share reads only, so vectorization is legal with a safe first index and tail. With `y=x`, iteration i overwrites `x[i]`, which iteration i+1 is specified to read after the overwrite in scalar order. This is a distance-one flow dependence; naïve simultaneous lanes read old values and change results. Preserve scalar order, copy the source first and vectorize from the copy, or reformulate only if a proven recurrence/scan matches the desired semantics. Runtime alias versioning can choose the disjoint vector path and overlapping safe path.

### Answer 3

First specify `out[i]=min(high,max(low,f(in[i])))`, including NaN handling, signed zero, overflow, rounding, and whether in/out may overlap. The scalar version is the oracle. A fixed-width version handles full vectors plus a scalar or fault-suppressing masked tail; it uses only truthful alignment/non-alias facts. A VLA version obtains a predicate for remaining elements, processes active lanes, and advances by returned active count. Dispatch validates hardware and OS support and retains baseline fallback. Tests force every path and cover lengths 0, 1, `VF-1`, VF, `VF+1`, multiple groups, guard-page ends, all supported overlaps, misalignment, extrema, NaNs/infinities, and randomized cases. Compare exact bits or a specified tolerance and exception relation; use sanitizers and generated-code inspection.

### Answer 4

A scalar epilogue gives simple bounds but lengths 15 and 17 combine a vector body with meaningful remainder overhead. A masked tail can handle all three uniformly if the target's masked loads/stores suppress inactive accesses and the source lowering never forms forbidden accesses; this is especially important at a guard page. Padding can make fixed full loads safe only if the allocator owns initialized live padding through the full access and stores to it are permitted. An external message pointer cannot be assumed padded. Benchmark the actual length mixture, cold/warm cache, alignment, and dispatch paths. Prefer masked tails where proven and supported, retain scalar fallback, and use guard-page tests rather than relying on mapped neighboring memory.

### Answer 5

Define the biological input encoding, quality threshold, ambiguous-base policy, coordinate system, reduction operation/order, overflow, missing data, and allowed numeric equality. Maintain a simple scalar oracle and separately versioned fixed/scalable implementations. Prove lane coverage, tail safety, aliasing, gather bounds, reduction behavior, and feature dispatch; test guard pages, boundary lengths/qualities, malformed records, every forced ISA path, virtualization, and fallback. Use representative genomes and host classes to measure latency, throughput, memory bandwidth, tails, and uncertainty without exposing patient data. Bind binary, compiler, flags, reference data, host/ISA path, and benchmark protocol in provenance. Apply least privilege, de-identification, encrypted artifacts, retention controls, audit, and side-channel review. Named genomics, clinical-domain, biostatistics, numerical, SIMD/compiler, hardware/platform, software-safety, data-governance, privacy/security, quality/regulatory, and independent validation reviewers approve requirements, datasets, error thresholds, and residual risk. Functional equality and speed do not establish clinical validity or regulatory approval.
