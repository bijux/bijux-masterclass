---
module_id: CONPAR-073
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 73
title: Compiler Auto-Vectorization
status: complete
last_verified: 2026-08-29
---

# Compiler Auto-Vectorization

## One-Page Review

### Governing question

How does a compiler prove that scalar operations may be grouped into vector operations, decide whether doing so is profitable, and expose enough evidence for engineers to validate the result?

### Essential definitions

- **auto-vectorization** is a compiler transformation from scalar intermediate representation to vector operations without source-level intrinsics specifying each instruction.
- **loop vectorization** packs operations from different iterations; **SLP vectorization** packs isomorphic independent operations in straight-line code.
- **legality analysis** determines whether the transformation preserves permitted program behavior.
- **profitability analysis** estimates whether a legal vector plan costs less than alternatives on a target.
- A **dependence** constrains relative execution order because operations access the same state and at least one writes.
- **alias analysis** estimates whether two references can denote overlapping storage.
- **runtime versioning** emits a checked vector path and a general fallback when legality depends on runtime facts.
- **if-conversion** maps divergent control flow to predicates and selects.
- A **reduction recognition** identifies a recurrence with a supported combine pattern and authorized ordering semantics.
- **vectorization factor (VF)** is scalar work represented by one vector iteration; **interleave/unroll factor (UF)** duplicates vector work to expose throughput.
- An **optimization remark** reports a transformation, missed opportunity, or analysis explanation at a source location.
- A **cost model** predicts instruction, control, memory, and setup costs; it is heuristic and target-specific.

### Central model, mechanism, or theorem

A compiler normalizes code into an intermediate representation, discovers candidate loop or SLP packs, proves memory/control/arithmetic legality, constructs one or more scalar/vector plans, estimates target cost for candidate VFs/UFs and tails, selects a plan or scalar form, and lowers it to target instructions. Correctness is conditional on source-language semantics and every programmer-supplied fact. Profitability is a prediction until measured. Review therefore triangulates remarks, transformed IR or assembly, executed-path tests, semantic comparison, and representative performance.

### Critical invariants

Every transformed iteration or statement has a scalar correspondence; dependencies and side effects remain ordered as required; alias, alignment, bounds, and trip-count facts are proven or runtime checked; reductions have authorized machine-arithmetic semantics; calls have suitable vector forms or safe scalarization; exceptions and inactive lanes obey language/target rules; fallback paths cover failed runtime predicates and unsupported targets; compilation flags, target features, profiles, libraries, and toolchain are recorded; tests force all versions; and “vectorized” never substitutes for semantic or performance evidence.

### Common failures

Developers force a loop after a legitimate dependence warning, use false `restrict`/alignment/`safelen` claims, enable fast math without a numeric contract, mistake SLP for loop vectorization, read one success remark but miss scalarized operations, inspect assembly for the wrong target, benchmark a compile-time-known trip count unlike production, ignore runtime-check and tail costs, let PGO profiles go stale, assume a newer compiler makes identical decisions, test only the vector path, or freeze fragile source contortions around one compiler heuristic.

### Compact example

A planner sees 100 independent scalar iterations costing 2 units each. With VF=4, 25 vector groups cost 4 each plus setup 12: estimated 112 versus scalar 200, so vector wins. At n=3, the same plan costs 16 versus 6, so scalar wins. A recurrence remains illegal even if its hypothetical vector cost is lower. Legality filters plans before cost ranks them.

### Connections

[SIMD Execution and Vector Lanes](071-simd-execution-and-vector-lanes.md) supplies execution semantics; [Data Layout for Vectorization](072-data-layout-for-vectorization.md) supplies address shapes. [Compiler and Processor Reordering](021-compiler-and-processor-reordering.md) distinguishes source observations from transformations. The [program roadmap](../ROADMAP.md) next covers explicit intrinsics and GPU execution.

## Governing Question

Which facts let a compiler transform scalar source into semantically valid and profitable vector code, and which artifacts let a reviewer distinguish a sound optimization from an unsafe assertion or unmeasured assumption?

The compiler has more context than a local source loop after inlining, constant propagation, alias analysis, and target selection, but less domain knowledge than the programmer. Productive auto-vectorization makes this boundary explicit: source communicates only true semantic facts, the compiler explains decisions, and testing verifies both transformed and fallback executions.

## Why This Matters

Auto-vectorization can deliver SIMD performance while keeping source portable across widths and instruction sets. It centralizes target mapping in the compiler, reduces hand-written intrinsic variants, and lets later compiler versions benefit unchanged algorithms. It is often the most maintainable first optimization for maps, reductions, image loops, numeric kernels, parsing, and data-system scans.

It also makes implicit contracts executable. A no-alias qualifier, alignment assumption, loop directive, relaxed floating flag, or target option grants the compiler permission. If the fact is false, the generated vector code may be wrong even though the compiler is conforming. Conversely, a conservative missed optimization is not necessarily a compiler defect; the source may genuinely lack enough proof or the cost model may rationally prefer scalar code.

Graduate-level practice therefore studies the transformation pipeline, not just flags. The goal is to explain why a plan is legal, why it was selected for this target and workload, and how that claim will survive compiler, architecture, and profile changes.

## Prerequisites and Retrieval

Retrieve:

- lane grouping, masks, tails, reductions, and dispatch from [SIMD Execution and Vector Lanes](071-simd-execution-and-vector-lanes.md);
- AoS/SoA, strides, gathers, alignment, and conversion from [Data Layout for Vectorization](072-data-layout-for-vectorization.md);
- memory and compiler observability from [Compiler and Processor Reordering](021-compiler-and-processor-reordering.md); and
- reduction structure and numeric obligations from [Parallel Loops and Reductions](044-parallel-loops-and-reductions.md).

Retrieval prompt: choose a hot scalar loop and enumerate reads, writes, calls, exits, exceptions, iteration dependencies, alias possibilities, numeric ordering requirements, trip-count distribution, and target features. Which facts are language guarantees, runtime facts, or guesses?

## Learning Objectives

After completing this module, a learner can:

1. distinguish loop, SLP, outer-loop, and interleaving transformations;
2. trace candidate discovery, legality, planning, cost selection, and lowering;
3. analyze data dependences, aliasing, calls, control flow, and recurrences;
4. explain runtime versioning, peeling, epilogues, tail folding, VF, and UF;
5. scope reductions, floating reassociation, contraction, and vector math calls;
6. use source restructuring and directives without making false promises;
7. collect success, missed, and analysis remarks and inspect generated code;
8. test fallback, vector, target, profile, and compiler-version matrices;
9. benchmark cost-model assumptions on representative workloads; and
10. define evidence and external review for high-stakes transformed code.

## Core Exposition

### The transformation boundary

Compilers rarely vectorize source text directly. Parsing and semantic analysis produce intermediate representation (IR); earlier passes inline functions, simplify control flow, propagate constants, expose induction variables, and establish static single assignment relations. Vectorization operates on this normalized graph under the source language's permitted behavior.

Undefined behavior gives no useful reference execution. A loop that reads outside an array, overflows an undefined signed type, violates an alias contract, or races is not made correct by retaining scalar instructions. First establish a valid scalar specification. Auto-vectorization then refines that specification for allowed inputs.

Compiler output depends on target triple, CPU/features, optimization level, language mode, floating options, link-time visibility, libraries, profile data, and compiler version. “The source vectorizes” is incomplete; record the compilation configuration and exact artifact.

### Loop vectorization

Loop vectorization packs corresponding operations from VF scalar iterations. A scalar induction variable becomes vector indices or a base plus lane offsets. Consecutive loads may widen, uniform values broadcast, comparisons form masks, and stores widen. The loop bound changes to a vector trip count, with a scalar epilogue, masked tail, or proven exact multiple.

Unknown trip counts are common and not inherently blocking. A vector preheader can calculate whether enough iterations exist, execute a vector body for the largest covered prefix, and handle the remainder. For short inputs, the scalar path can bypass setup. Runtime versioning may add alias or alignment checks before selecting the vector body.

Outer-loop vectorization packs outer iterations when the inner loop is too short or contains a structure better preserved per lane. Nested vectorization may combine levels, but planning, masks, control flow, and memory locality become harder. Loop interchange, distribution, fusion, unswitching, or inlining can expose a better candidate before vectorization.

### SLP vectorization

Superword-level parallelism packs isomorphic independent scalar statements within a basic block or unrolled region. Four separately written color-channel computations can form one vector even without a loop. SLP commonly builds packs bottom-up from stores or other roots, follows operand graphs, and evaluates shuffles, extracts, inserts, and reuse.

SLP and loop vectorization can interact: loop vectorization groups iterations while SLP packs independent operations within an iteration or an unrolled loop. A remark naming one does not prove the other occurred. Excessive source unrolling can help expose SLP or can obstruct loop analysis and bloat code; inspect current compiler behavior.

### Candidate legality

For memory operations, construct dependence constraints. Two iterations conflict when their address ranges overlap and at least one writes. True/flow dependence carries a produced value forward; anti-dependence constrains a write after an earlier read; output dependence orders writes. Reductions and inductions are recognized recurrences with specialized transformations. Arbitrary cycles generally block independent lane execution.

Alias analysis may prove disjoint objects from types, provenance, local allocation, inlining, or qualifiers. When pointers may overlap only for some calls, runtime versioning compares ranges and selects vector code for disjoint inputs. This is often preferable to strengthening an API contract. Range checks themselves must use overflow-safe reasoning and preserve valid partial-overlap semantics in the fallback.

Alignment can be established from allocation, type, known offsets, or a runtime check. Modern unaligned accesses may still vectorize, so alignment is often profitability rather than legality, but instructions and language assertions differ. A compiler assumption is not a request to repair a pointer.

Calls block or complicate packing when their side effects, exceptions, or vector form are unknown. Inlining may expose pure arithmetic. Compilers recognize intrinsics and math-library vector variants, generate masked calls, or scalarize per lane. `declare simd`-style interfaces can supply vector function variants, but uniform, linear, alignment, branch, and side-effect contracts must be true.

### Control flow and exceptions

If-conversion turns branches into predicated computations. It is legal only when evaluating predicated paths does not introduce forbidden effects. A masked store can suppress inactive writes, but an unmasked division, trap, volatile access, allocation, I/O call, or invalid pointer evaluation may not be speculatable. Compilers use safety analysis, predicated instructions, masked intrinsics, or scalarization.

Early exits, search loops, and exceptions require specialized representations. A vector search may compare a group and locate the first matching lane, but must preserve the scalar first-match rule and avoid later forbidden effects. Vectorizing exception-capable languages also interacts with precise exception ordering. A directive that promises a loop is SIMD-safe transfers these obligations to the programmer.

### Reductions and numeric permissions

Reduction recognition finds a loop-carried value combined with each iteration. Integer bitwise operations and defined modular addition have different algebra than undefined, trapping, or saturating arithmetic. Floating addition and multiplication are not associative under IEEE 754; vector trees, fused operations, reciprocal approximations, NaN behavior, signed zero, subnormals, and exception flags can differ.

Strict modes may prevent reassociation or use ordered vector reductions where supported. Fast-math flags grant a bundle of permissions; their exact meaning is compiler-specific. Prefer a documented application numeric contract and the narrowest matching options. Validate worst cases and error bounds. Never add fast math merely to turn a missed remark into success.

Vector math functions need implementations for the selected ABI, width, accuracy, and exception mode. A compiler may call a vector library, inline an approximation, or scalarize. The availability and accuracy contract are build inputs and must be recorded.

### Legality before cost: executable model

The following sequential planner illustrates the separation. It uses declared costs, not compiler IR or measured instructions, and it does not perform dependence or alias analysis.

<!-- bijux-verify: {"id":"legality-before-cost-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"map: vector scalar_cost=200 vector_cost=112\nshort: scalar scalar_cost=6 vector_cost=16\nrecurrence: missed dependence\ngather: scalar scalar_cost=200 vector_cost=237\n","stderr":""}} -->
```python
def plan(name, count, legal, reason, scalar_per_item, vector_width, vector_group, setup):
    if not legal:
        return f"{name}: missed {reason}"
    scalar_cost = count * scalar_per_item
    groups = (count + vector_width - 1) // vector_width
    vector_cost = setup + groups * vector_group
    choice = "vector" if vector_cost < scalar_cost else "scalar"
    return f"{name}: {choice} scalar_cost={scalar_cost} vector_cost={vector_cost}"


cases = [
    ("map", 100, True, "", 2, 4, 4, 12),
    ("short", 3, True, "", 2, 4, 4, 12),
    ("recurrence", 100, False, "dependence", 2, 4, 4, 12),
    ("gather", 100, True, "", 2, 4, 9, 12),
]

for case in cases:
    print(plan(*case))
```

Real cost models estimate target instructions, latency/throughput, masks, memory kinds, shuffles, scalarized lanes, runtime checks, prologue/epilogue, code size, register pressure, and profiles. Estimates can be wrong. The model's correct role is to choose among legal candidates, not certify performance.

### Plans, VF, UF, and scalable vectors

A modern vectorizer may build explicit plans for candidate VFs and UFs, transform those plans, estimate each, and materialize the best. LLVM's VPlan represents vector control flow and recipes for widened, replicated, predicated, interleaved, and reduction operations. Plan construction should not modify source IR until selection.

Fixed VF candidates correspond to specific element counts; scalable VF candidates represent a runtime multiple of an architectural quantity. The compiler must ensure loop progress and masks work for every supported runtime length. Costing scalable values may require ranges or target estimates rather than one lane count.

UF can hide latency and increase throughput but consumes registers and code size. Too much unrolling spills vectors or bloats instruction cache. Epilogue vectorization may use a smaller VF for the remainder. Candidate choice is target- and workload-specific.

### Profitability inputs

Memory access classification distinguishes consecutive widening, interleaved groups, gather/scatter, and scalarization. Layout changes from the previous module can turn expensive candidates into consecutive loads, but conversion costs lie outside a local loop cost model unless exposed in surrounding IR.

Trip-count estimates matter because setup is amortized over iterations. Static bounds, branch probabilities, and profile-guided optimization (PGO) can guide versioning and candidate selection. Profiles must represent production and match the binary/source; stale or biased data can optimize the wrong path. Retain a non-profile build comparison.

Target descriptions supply legal types/instructions and costs. A generic target may avoid newer instructions; a native target may generate a binary unsuitable elsewhere. Function multiversioning can compile several variants and dispatch. Cross-compilation requires inspecting the intended target artifact rather than host execution alone.

### Source patterns that help without lying

Use canonical countable loops, simple induction, obvious bounds, contiguous data, local temporaries, pure/inlinable functions, and explicit reduction structure. Separate hot and exceptional cases when their semantics permit. Hoist loop invariants, but let normal optimization do it when clear. Use appropriate types and avoid needless conversions.

Expose alias facts through API design—distinct owned spans or views—before reaching for qualifiers. Propagate allocation alignment with checked views. Restructure AoS/SoA or loop order only when end-to-end data access supports it. A small, semantic refactoring is more durable than code shaped around a single missed-optimization message.

Directives and pragmas can request a preferred width, predication style, interleave count, or assertion of safe concurrent iterations. Distinguish hints the compiler may ignore from assumptions whose violation changes behavior. Document the proof next to the API/test, not as a vague performance comment. Test directive-free correctness and forced fallback.

### Remarks and diagnostics

Collect successful, missed, and analysis remarks. A success should identify the source region and often VF/UF; a missed remark provides a reason such as dependence, unsafe call, or unfavorable cost. Analysis remarks show facts considered. Filters must not accidentally hide other optimization passes or translation units.

Remarks are compiler observations, not stable APIs. Source locations change with inlining and templates. Store machine-readable records as CI artifacts and summarize durable expectations: which named kernels should have some vector plan on which target class, not an exact sentence forever.

A missed remark is a diagnostic hypothesis. Confirm the alleged dependence or cost with IR, alias facts, and source semantics. If the compiler lacks a transformation, decide among clear source restructuring, library call, explicit vector abstraction/intrinsics, or accepting scalar code. Do not silence the report with an unsafe promise.

### Inspect generated code

Verify target triple/features and find the executed function variant. Inspect IR or assembly for vector types/instructions, masks, runtime alias/alignment checks, vector loop bounds, tails, reduction trees, gathers/shuffles, scalarized calls, and fallback. Check that a vector instruction is inside the hot loop rather than initialization.

Static inspection cannot show which runtime version is taken or actual speed. Add controlled inputs that take both alias and disjoint paths, short and long trips, aligned and unaligned cases, exceptional numeric values, and different features. Hardware counters and sampling can confirm executed instructions and bottlenecks, subject to counter semantics.

### Testing compiler transformations

Maintain a simple scalar oracle or independently specified reference. Differentially compare every forced vector/target/profile variant across boundaries around VF and UF, zero/one length, tails, alignment, supported overlap, empty masks, exceptional numbers, and large ranges. Use sanitizers and guard pages where applicable. Test on actual target hardware or a qualified emulator for compatibility, but do not treat emulated timing as performance evidence.

Compiler upgrades can change output while preserving semantics. Pin production toolchains, then qualify upgrades using semantic suites, diagnostics diff, generated-code review for critical kernels, and performance distributions. A performance regression may be caused by vectorizer, inliner, register allocator, library, target model, or layout; isolate with controlled builds.

Avoid tests that assert exact assembly except where an ABI/security/certification requirement demands it; such tests are brittle. Prefer semantic properties and target-scoped evidence that a kernel remains vectorized without prescribing one instruction schedule.

### Benchmarking and operations

Measure the complete call path with realistic trip-count, alignment, alias, mask, and data distributions. Separate warm/cold cache, single/concurrent load, and host classes. Report latency distribution, throughput, bytes, vector-path rate, compilation configuration, binary digest, hardware, OS, profile identity, repetitions, and uncertainty.

Compare scalar-forced, auto-vectorized, and any intrinsic/library versions. Scalar-forced is a performance baseline only after confirming it shares semantics. A speedup ratio without absolute times can hide regressions in both variants. Monitor correctness and performance after deployment; a new input distribution can make runtime version checks or short loops dominate.

Security-sensitive code additionally checks constant-time requirements. Auto-vectorization can introduce table gathers, branches, or masked behavior dependent on secrets, or can remove intended barriers under invalid source assumptions. Use a separately verified coding/toolchain strategy. High-stakes code needs traceability from requirements through source facts, flags, compiler version, generated artifact, target, and independent review.

## Definitions and Notation

- `IR`: compiler intermediate representation after specified transformations.
- `D`: dependence relation constraining statement/iteration order.
- `VF`: scalar iterations or statements represented per vector group.
- `UF`: number of vector groups unrolled/interleaved in one loop body.
- `TC`: runtime trip count.
- `C_s(TC)`: estimated scalar cost.
- `C_v(TC,VF,UF)`: estimated vector cost including setup, body, masks, and tail.
- `P`: runtime legality predicate such as nonoverlap and alignment.
- `V`: vector version executed when P holds and target support is present.
- `S`: general scalar or semantics-preserving fallback.
- `R`: reduction operator under an explicitly stated machine domain.
- `O`: required observable behavior/equivalence relation.
- `B`: full compilation/build configuration and binary identity.

A profitable legal plan satisfies estimated `C_v<C_s`; actual speedup requires measured times under a workload protocol. A transformed version refines scalar behavior only if observations are equivalent under O for every allowed input.

## Mechanisms, Invariants, or Proof Structure

### Pointwise loop proof

Prove coverage and unique mapping of scalar iterations to active lanes; prove pairwise conflicting accesses are absent or ordered; prove each lane computes an O-equivalent operation; prove inactive lanes have no forbidden effects; and prove tails cover remaining iterations. Compiler analysis automates parts of this proof under language and IR semantics.

### Runtime versioning proof

Partition allowed inputs by predicate P. For P=true, prove V refines the scalar specification using nonoverlap/alignment facts established by the check. For P=false, S handles every remaining allowed input. Prove the check itself has defined overflow-safe behavior and dispatch chooses exactly one path. Tests must exercise both partitions.

### Reduction proof

Identify scalar recurrence and initial value, vector partial accumulators, and final combine tree. Prove equality under actual operator properties or prove a required error/exception relation. Compiler recognition does not create associativity; flags or language constructs define permission.

### Cost-selection argument

Legality yields a candidate set. The cost model orders candidates using target estimates and may select scalar. Because costs approximate a workload and machine, selection is a heuristic decision, not a theorem. Benchmark feedback may justify source, profile, or target-model changes without weakening legality.

### Upgrade qualification invariant

Every accepted toolchain version passes semantic differential tests for all supported paths, records its configuration, and meets target-scoped performance thresholds. Diagnostics/assembly changes trigger review proportional to kernel criticality; identical source does not imply identical generated plans.

## Alternatives and Trade-Offs

| Approach | Main benefit | Principal limitation |
|---|---|---|
| Auto-vectorized loop | portable source and target-aware plans | compiler visibility and heuristics govern outcome |
| SLP vectorization | finds straight-line packs | shuffle/packing cost and fragile graph shape |
| Source restructuring | can expose durable independence/locality | maintenance and whole-pipeline consequences |
| Runtime versioning | fast path without stronger universal contract | checks, code size, and fallback testing |
| Directives/pragmas | convey domain knowledge and preferences | unsafe assertions transfer proof burden |
| Vector math library | reviewed implementations and broad functions | ABI, accuracy, dispatch, and dependency ownership |
| Portable SIMD API | explicit vector intent across targets | abstraction/lowering variability |
| Intrinsics | exact target control | variants, tails, portability, and maintenance |
| Scalar baseline | robust reference and short-trip path | unused lane hardware |

Use auto-vectorization first when semantics are clear and evidence shows adequate plans. Escalate to libraries, portable SIMD, or intrinsics only for measured gaps with durable ownership. Never trade a correctness premise for a remark.

## Failure Modes and Misconceptions

- **“`-O3` guarantees vectorization.”** candidates may be illegal or unprofitable.
- **“A missed optimization is a compiler bug.”** the source may not prove needed facts.
- **“A success remark proves the whole loop is vector.”** calls or operations may scalarize.
- **“SLP and loop vectorization are the same.”** they pack different graph dimensions.
- **“No alias is just a hint.”** qualifiers/assumptions can be semantic contracts.
- **“Aligned annotation aligns data.”** it asserts a runtime fact.
- **“A SIMD directive checks safety.”** many directives rely on programmer truth.
- **“Fast math is required for all vector code.”** pointwise strict operations can vectorize; reductions differ.
- **“Vector reduction equals scalar bits.”** association and contraction can change results.
- **“VF is the hardware register lane count.”** scalable types, legalization, and UF complicate it.
- **“Native target is portable.”** it may emit unsupported instructions elsewhere.
- **“PGO always improves decisions.”** biased or stale profiles mislead.
- **“Assembly from my laptop verifies the deployed binary.”** target/configuration may differ.
- **“A vector instruction proves speedup.”** checks, gathers, tails, or memory may dominate.
- **“Compiler upgrades are transparent.”** legal plans and performance can change.
- **“Exact assembly tests ensure quality.”** they can reject equivalent better schedules and miss semantics.

## Worked Examples

### Example 1

**Independent map.** `a[i]=b[i]+c[i]` over disjoint arrays has unique stores and immutable per-index reads. **Conclusion:** it is a canonical loop-vectorization candidate.

### Example 2

**Possible overlap.** `a[i]=b[i]+1` is called with arbitrary spans. A runtime nonoverlap check selects V; overlap selects S. **Conclusion:** conditional facts can create a safe fast path.

### Example 3

**Distance-one recurrence.** `a[i]=a[i-1]+x[i]` forms a dependence cycle. A scan transformation is required, not a forced independent-lane directive. **Conclusion:** cost never overrides illegality.

### Example 4

**SLP pack.** Four independent statements compute the same clamp for r, g, b, and a values. SLP packs their isomorphic graph while no cross-iteration loop exists. **Conclusion:** straight-line parallelism is distinct from loop VF.

### Example 5

**Short loop.** A legal vector plan has setup 12 and body saving 1 per item. For three items it loses; for hundreds it wins. **Conclusion:** trip-count distribution shapes profitability.

### Example 6

**Unsafe exception.** If-converting `if (d[i]!=0) q[i]=n[i]/d[i]` into an unmasked division can trap on inactive zero lanes. Use specified masked division or retain control/scalarization. **Conclusion:** selected output does not erase speculative effects.

### Example 7

**Floating sum.** A strict scalar left fold cannot silently become a balanced vector tree. A reproducible tree or bounded-error contract can authorize a different algorithm. **Conclusion:** reduction recognition and numeric permission are separate.

### Example 8

**Misleading success.** A loop vectorizes its adds but scalarizes `sin` for each lane; remark and assembly reveal extract/call/insert overhead. A reviewed vector math library changes the plan. **Conclusion:** inspect the complete body.

### Example 9

**Compiler upgrade.** A new target cost model changes VF and removes an epilogue, improving large inputs but regressing small production messages. Qualification catches the distribution-specific regression. **Conclusion:** valid generated code still needs operational evidence.

### Example 10

**Flight-control filter.** Auto-vectorizing sensor filtering requires bounds, alias, alignment, fixed-point/floating overflow and rounding, NaN/fault handling, reduction order, deadlines, fallback, toolchain qualification, binary/target traceability, and fault-injection tests. Named control-systems, avionics, sensor, numerical, compiler/ISA, hardware, real-time, software-safety, cybersecurity, quality/certification, and independent verification reviewers must approve requirements and evidence; none is claimed here. **Conclusion:** a compiler's legal transformation and timing sample do not establish airworthiness.

## Cross-Program Connections

- **Programming languages:** alias, lifetime, undefined behavior, exceptions, and numeric modes bound transformations.
- **Compiler construction:** SSA, dependence graphs, IR planning, cost models, and lowering implement vectorization.
- **Algorithms:** maps, scans, reductions, searches, and recurrences offer different legal structures.
- **Computer architecture:** target instructions, registers, masks, caches, and throughput price plans.
- **Numerical computing:** reassociation, FMA, vector math, and error bounds govern reductions.
- **Testing:** differential oracles, boundary matrices, artifact inspection, and upgrade qualification provide evidence.
- **DevOps:** pinned toolchains, profiles, binary provenance, and host feature inventories make builds reproducible.
- **Security:** language UB, bounds, dispatch, vector libraries, and constant-time behavior require scrutiny.
- **Performance engineering:** remarks form hypotheses; profiles, counters, and representative benchmarks decide value.
- **Safety engineering:** requirements-to-binary traceability and independent review constrain high-stakes use.

## References

1. Samuel Larsen and Saman Amarasinghe, “Exploiting Superword Level Parallelism with Multimedia Instruction Sets,” PLDI 2000. <https://doi.org/10.1145/349299.349320>
2. Dorit Nuzman, Ira Rosen, and Ayal Zaks, “Auto-Vectorization of Interleaved Data for SIMD,” PLDI 2006. <https://doi.org/10.1145/1133981.1133997>
3. LLVM Project, *Auto-Vectorization in LLVM*, current documentation; retrieved 2026-08-29. <https://llvm.org/docs/Vectorizers.html>
4. LLVM Project, *Vectorization Plan*, current documentation; retrieved 2026-08-29. <https://llvm.org/docs/VectorizationPlan.html>
5. Clang Project, *Clang Compiler User's Manual: Options to Emit Optimization Reports*, current documentation; retrieved 2026-08-29. <https://clang.llvm.org/docs/UsersManual.html#options-to-emit-optimization-reports>
6. GNU Project, *Auto-vectorization in GCC*, current project documentation; retrieved 2026-08-29. <https://gcc.gnu.org/projects/tree-ssa/vectorization.html>
7. OpenMP Architecture Review Board, *OpenMP API Specification 6.0*, November 2024. <https://www.openmp.org/wp-content/uploads/OpenMP-API-Specification-6-0.pdf>
8. Intel, *Intel 64 and IA-32 Architectures Optimization Reference Manual*, version 050; retrieved 2026-08-29. <https://www.intel.com/content/www/us/en/developer/articles/technical/intel64-and-ia32-architectures-optimization.html>
9. IEEE, *IEEE Standard for Floating-Point Arithmetic*, IEEE 754-2019. <https://doi.org/10.1109/IEEESTD.2019.8766229>
10. ISO/IEC, *ISO/IEC 9899:2024 — Programming Languages — C*, 2024. <https://www.iso.org/standard/82075.html>

## Exercises

### Exercise 1

Classify four candidates—pointwise map, distance-one recurrence, four independent scalar statements, and conditional division—as loop-vector, SLP, specialized/predicated, or illegal without reformulation. Justify each.

### Exercise 2

Derive runtime versioning for `dst[i]=src[i]+1` with possibly overlapping byte spans. Specify predicate, overflow handling, fallback, tails, and tests.

### Exercise 3

Design a diagnostic workflow for a hot reduction that is not vectorized under strict floating semantics. Include legal alternatives and evidence, without automatically enabling fast math.

### Exercise 4

Create a compiler-upgrade qualification matrix for three CPU feature classes, PGO and non-PGO builds, short/long trips, and alias/alignment variants.

### Exercise 5

A regulated pricing engine uses auto-vectorized decimal/fixed-point risk aggregation. Specify semantic, toolchain, performance, operational, security, and human-review requirements.

## Answers to the Exercises

### Answer 1

The pointwise map is a loop-vector candidate when arrays are valid and conflicts absent. Four independent isomorphic statements are SLP candidates because parallelism lies within a basic block. The recurrence is illegal as independent iteration packing; a proven scan or recurrence-specific vector algorithm is a reformulation. Conditional division can use if-conversion only with target/source semantics that suppress division for inactive zero-denominator lanes; otherwise retain branches or scalarize. For each, profitability remains separate and memory/call/exception facts can change the plan.

### Answer 2

Compute source and destination byte ranges for n elements using checked size multiplication and endpoint arithmetic. P is true when ranges are disjoint (or when an explicitly supported exact-overlap case is semantically pointwise), required alignment/features hold, and n meets a profitable threshold. If P, execute V with proven unique stores, valid loads, and safe tail. Otherwise S preserves the documented overlap order, potentially with direction-aware copying if required. The check must avoid pointer-order operations not defined by the language; use sanctioned address/range facilities. Test zero, one, VF boundaries, huge/overflow-rejected n, disjoint adjacency, exact overlap, partial overlap in both directions, alignment classes, guard pages, forced V/S, and unsupported target.

### Answer 3

Record the exact missed/analysis remark, IR, target, flags, and source recurrence. Define required result: strict left-fold bits/exceptions, reproducible fixed tree, correctly rounded result, or bounded error. Options include retaining scalar strict order, an ordered vector reduction if it meets semantics, a specified reproducible tree, compensated/pairwise summation with analyzed error, or a reviewed library. Only use reassociation/fast options when the numeric contract explicitly permits their NaN, zero, exception, contraction, and approximation consequences. Differentially test adversarial cancellation, magnitude, NaN/infinity, signed zero, subnormal, and length/VF cases against high precision or specified oracle. Inspect lowering and benchmark complete distributions; document residual error and external numerical review requirements.

### Answer 4

Build each baseline feature class with generic and class-specific target settings, both with a versioned representative PGO profile and without it. Force and observe runtime paths. Cross product zero/one, VF−1/VF/VF+1, short modal, long, and tail-heavy trips with disjoint/overlapping and aligned/misaligned supported inputs. Run semantic differential, sanitizer/guard, exception/numeric, and dispatch tests on actual hardware. Capture success/missed/analysis remarks, binary/IR/assembly digests, selected VF/UF/tails/checks, vector-path rate, absolute latency/throughput, counters, repetitions, and uncertainty. Compare to the accepted compiler under identical source/profile/hardware. Investigate semantic failure absolutely and performance thresholds by workload importance; do not demand byte-identical assembly.

### Answer 5

Specify decimal/fixed-point scale, rounding, overflow/trap/saturation, accumulator width, order, missing values, and exact observable result. Prove dependence, alias, bounds, and reduction semantics for every vector variant and general fallback. Pin compiler, linker, libraries, target options, profile, build environment, binary digest, and feature dispatch; qualify upgrades and force all paths. Use an independent scalar/reference implementation, exact arithmetic recomputation, extremes, cancellations, overflows, tails, overlap, and malformed inputs. Measure end-to-end latency and deadlines across hosts, short/long distributions, load, and failure/fallback while monitoring path rates and regressions. Protect model/client data, build artifacts, profiles, logs, and supply chain with access control, provenance, retention, and incident procedures. Named financial-domain, quantitative-risk, decimal/numerical, compiler/ISA, platform, software-quality, model-validation, security/privacy, operations, regulatory/compliance, and independent assurance reviewers approve requirements, thresholds, limitations, and residual risk. Vectorization does not establish model validity or regulatory approval.
