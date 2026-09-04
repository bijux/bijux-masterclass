---
module_id: CA-019
program: Computer Architecture
level: 1
module_number: 19
title: Vector and SIMD Extensions
status: complete
last_verified: 2026-09-04
---

# Vector and SIMD Extensions

## One-Page Review

### Governing question

How do vector and SIMD ISAs represent many data-parallel operations while keeping element widths, active lanes, masks, memory access, exceptions, numerical behavior and implementation freedom precise?

### Essential definitions

- **SIMD** executes one operation over multiple packed elements in a fixed-width architectural register.
- A **vector-length architecture** exposes a configurable number of active elements, often independent of the implementation’s physical lane count.
- A **lane** is an implementation or conceptual element-processing position; architectural element order must not be inferred from physical wiring.
- **element width** determines the bits interpreted for each vector element.
- **vector length** (`VL`) is the number of active elements for an instruction under the current configuration.
- **maximum vector length** is the implementation/profile capacity governing strip mining.
- A **mask** or **predicate** enables or disables per-element effects.
- **tail elements** lie beyond `VL` in a destination group; **inactive elements** lie within `VL` but have false mask bits.
- **tail/mask policy** defines whether such elements are preserved, zeroed or architecturally agnostic.
- **vector register grouping** combines multiple architectural registers for one wider logical operand.
- A **widening** operation produces wider elements; a **narrowing** operation reduces width under specified rounding/saturation/truncation.
- A **reduction** combines multiple elements into fewer results under a specified association/order contract.
- A **gather** loads from indexed addresses; a **scatter** stores to indexed addresses.
- **strip mining** partitions an iteration space into chunks no larger than the available active vector length.
- **restart state** identifies the element at which a partially completed vector instruction may resume after a precise/restartable trap.

### Central model, mechanism, or theorem

For configuration `C`, mask `M`, vector length `VL` and element function `f`, a lane-wise operation defines destination elements

`D'[i] = f(A[i], B[i])` for `0 <= i < VL` and `M[i]=1`.

Inactive and tail elements follow explicit policy; all other architectural state follows frame conditions. An implementation may use fewer physical lanes than active elements and execute several beats, or more lanes and fuse work, provided committed element values, faults, ordering and restart state refine the architectural relation.

### Critical invariants

- Element width, signedness, grouping and active `VL` are valid and explicit for every operation.
- Element numbering and memory byte order are distinguished from physical lane order.
- Masked-off and tail destinations follow the selected undisturbed/zero/agnostic policy exactly.
- Widening, narrowing, rounding, saturation and floating behavior are defined per element.
- Vector memory operations compute every active address and apply ordering/fault rules precisely.
- Partial completion exposes only permitted prefix/progress state and is safely restartable.
- Reductions and permutations constrain ordering enough to justify numerical/reproducibility claims.
- Context save, ABI, virtualization and debug preserve all enabled vector configuration and data state.

### Common failures

Frequent failures are using vector and SIMD as exact synonyms, equating physical lane count with architectural vector length, assuming all vector registers have one element type permanently, reversing element order because memory is little-endian, writing inactive lanes despite undisturbed policy, relying on agnostic tails as zero, masking a load after it has already faulted, assuming gathers are contiguous, treating a reduction as scalar left-to-right arithmetic, ignoring floating reassociation, overlapping register groups illegally, losing restart index on a trap, saving data registers but not vector configuration, and claiming speedup equal to element count.

### Compact example

To add ten elements on a machine with `VLMAX=4`, software sets `VL=min(remaining,4)` and executes chunks of 4, 4 and 2 active elements. The same binary structure remains correct on an implementation with another vector capacity because each iteration advances by returned `VL`. A fixed-width four-lane SIMD loop can use the same chunking but must handle its final two elements through masking or a scalar remainder under that ISA’s rules.

### Connections

Vector/SIMD extensions connect data-parallel algorithms, register files, pipelines, memory systems, compilers, numerical analysis, machine learning, cryptography, operating systems, virtualization and performance engineering.

## Governing Question

Data-parallel work repeats similar operations across arrays, pixels, samples and model tensors. Vector ISAs reduce instruction/control overhead by naming many element operations at once.

The governing question is what “many” means architecturally. Fixed-width SIMD bakes a width into registers and instructions. Scalable models let one program adapt to implementation capacity, but introduce configuration, tails, predicates and restart state.

## Why This Matters

A vector bug can corrupt only the final partial chunk, one masked element or one rare faulting gather, making it difficult to reproduce. Numerical discrepancies can arise from reduction order or fused operations even when every individual operation is legal.

Performance depends on memory bandwidth, alignment, dependencies, masking, gather locality and physical resources—not just arithmetic width. A nominal 16-element instruction can take multiple cycles or stall on memory.

Verification must scale beyond a few hand vectors. It covers configuration combinations, every element boundary, overlap rules, masks, tails, exception progress, floating modes and context switching.

## Prerequisites and Retrieval

Before studying this module, be able to:

- reason about fixed-width integer and floating representations;
- distinguish architectural registers from physical execution resources;
- explain scalar loads/stores, alignment and precise exceptions;
- trace a loop and its memory addresses;
- distinguish ISA semantics from compiler and ABI policy.

Retrieve ISA/profile/version; vector register count and width model; fixed/scalable lengths; supported element widths/types; grouping constraints; `VL`/configuration instructions; mask registers and policy; tail/inactive rules; arithmetic, logical, comparison, permutation and reduction operations; rounding/saturation/exception state; load/store, strided, indexed and segment operations; memory ordering and alignment; fault-only-first/restart behavior; ABI roles; context save/restore; virtualization/debug; compiler IR/intrinsics; autovectorizer reports; executable model; RTL lane design; architecture tests; numerical tolerances; benchmarks; power/thermal data; silicon errata; and exact tool/hardware revisions.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish fixed-width SIMD, vector-length and scalable-vector models;
2. derive active element sets from configuration, `VL` and masks;
3. specify tail, inactive and register-group behavior;
4. reason about widening, narrowing, saturation and floating-point modes;
5. analyze contiguous, strided, indexed and segmented memory operations;
6. explain reduction, permutation and cross-lane semantics;
7. design restartable vector exception behavior;
8. relate compiler strip mining and predication to ISA operations;
9. verify contexts and implementations across vector capacities;
10. evaluate performance, numerical and security evidence separately.

## Core Exposition

### Distinguish fixed and scalable width

Fixed-width SIMD exposes an architectural register width such as 128, 256 or 512 bits. Element count follows from register width divided by element width.

Scalable/vector-length designs expose operations over a runtime active length up to implementation capacity. Portable code queries/sets `VL` rather than assuming a physical width.

### Separate elements from lanes

Architectural element `i` is defined by the ISA. A physical lane is an implementation resource that may process several elements over time.

Four physical lanes can execute eight active elements in two beats. Eight lanes can share or split units. Correctness depends on element semantics, not lane count.

### Configure element width

One vector register’s bits can represent different element widths across instructions/configurations. The ISA defines legal widths and how grouping changes available elements.

Changing element width does not magically convert existing bits. Conversion instructions explicitly widen, narrow or reinterpret as specified.

### Set vector length

Scalable code sets `VL` from remaining elements. The architecture returns a legal value bounded by request and capacity under its configuration rules.

Software advances pointers and loop index by the actual `VL`, not the requested value. This is the heart of vector-length-agnostic strip mining.

### Form register groups

Some configurations treat consecutive registers as one logical operand. Legal starting indices and alignment prevent wrap or partial overlap.

Widening can enlarge a destination group. Source/destination overlap restrictions must be checked against the full byte ranges, not only first names.

### Apply masks

A mask predicate selects active operations element by element. It can suppress destination updates and, for memory instructions, suppress accesses/faults according to semantics.

Mask bits are architectural data. The mask register itself can overlap specially or be reserved depending on the operation.

### Define inactive policy

Within `VL`, a false mask creates an inactive element. Undisturbed policy preserves the old destination; agnostic policy permits specified values; zeroing policy writes zero where supported.

Compiler liveness and security clearing depend on this choice. Never read agnostic elements as meaningful results.

### Define tail policy

Elements beyond `VL` but inside the destination register group are tail elements. Tail-undisturbed preserves them; tail-agnostic permits architecture-defined nondeterminism.

Tail policy enables implementation freedom, but tests must compare only constrained values. Software needing zero tails must explicitly establish them.

### Perform lane-wise arithmetic

Ordinary vector add, subtract and logic apply independently to active elements. Fixed-width wrapping, signedness and flag/saturation behavior are per operation.

There is usually no carry between packed elements unless a dedicated carry-chain instruction says so.

### Widen operations

Widening extends sources and produces wider results, reducing element capacity or increasing group size. Signed and unsigned extension differ.

Intermediate width matters for multiply-accumulate. State whether accumulation occurs in wide precision and when narrowing happens.

### Narrow operations

Narrowing maps wide values into smaller destinations by truncation, rounding, clipping or saturation. Shift amount and rounding mode can be operands or control state.

Sticky saturation flags can be architectural side effects. They belong in read/write sets and context state.

### Handle saturation

Saturating arithmetic clamps at signed/unsigned bounds rather than wrapping. This is common in media and signal processing.

Test exact minimum/maximum and one step beyond. Confusing signed and unsigned saturation produces plausible interior results but wrong edges.

### Handle floating point

Vector floating operations inherit or define formats, rounding, exceptions, NaNs and fused behavior. Each active element can raise status while traps may be summarized.

Reassociation and contraction affect reproducibility. Compiler fast-math promises, not hardware width alone, determine allowed transformations.

### Compare and predicate

Vector comparisons produce masks or all-ones/zero elements depending on ISA. Signedness, ordered/unordered floating comparisons and NaNs require exact truth tables.

Predicates then drive selection, control or memory. Mask density affects performance but not functional selection.

### Select and merge

Merge chooses elements from sources under a mask. It differs from a masked arithmetic instruction with an old destination policy.

Define which operand supplies inactive values and whether destination is also a source. This affects dependencies and overlap.

### Permute elements

Slides, shuffles, compress, expand and table lookup move data across element positions. Out-of-range index behavior can be zero, preserved or constrained.

Cross-lane networks can be expensive. Semantics remain independent of whether hardware implements a full crossbar or multiple passes.

### Reduce vectors

Reductions combine active elements into a scalar or element result. Integer associative operations can admit tree evaluation under fixed-width semantics.

Floating addition is not mathematically associative. The ISA/compiler must constrain or permit order explicitly; reproducibility claims require the selected mode.

### Scan and prefix operations

Scans produce intermediate prefix results rather than one reduction. Inclusive/exclusive direction and mask behavior define outputs.

Dependencies can cross all elements. Physical parallel-prefix implementation changes latency, not architectural indices.

### Load contiguous elements

A unit-stride vector load accesses consecutive element-sized locations. Active address `i` commonly derives from base plus `i*element_bytes`.

Masked-off elements should not access memory when the ISA specifies suppression. Page crossings and partial faults need explicit handling.

### Load with stride

Strided operations use base plus `i*stride`, with signedness/address width defined. Zero stride can broadcast one memory location or follow special constraints.

Negative strides traverse backward. Address overflow, translation and ordering apply per active element.

### Gather and scatter

Indexed loads/stores compute each address from an index vector. Indices can be byte offsets or scaled element offsets and may have their own width/extension.

Addresses can alias. Scatter ordering for repeated addresses must be specified or treated as constrained nondeterminism; it is not automatically an atomic reduction.

### Use segmented operations

Segment loads/stores map interleaved structures into multiple vector fields. Field count, element width and register grouping interact.

They reduce address/control overhead for array-of-structures layouts but enlarge register and fault behavior.

### Handle alignment and memory types

Vector accesses span many bytes and can cross cache lines/pages even with aligned base. Each active element or whole instruction follows architecture-specific alignment rules.

MMIO is often unsuitable for vector access because repeated/combined transactions and side effects are platform-specific.

### Specify memory ordering

Vector memory instructions can generate multiple element accesses. The memory model defines order relative to one another and to other instructions.

Do not assume ascending element order is globally visible. Ordered indexed variants or fences may exist when order matters.

### Design precise/restartable faults

A vector instruction may complete a prefix before a fault and record a restart element such as `vstart`. The handler repairs the fault and resumes without repeating completed side effects.

The completed set, destination state and restart value must agree. Stores and repeated addresses make duplication especially dangerous.

### Fault-only-first loads

Fault-only-first forms support loops over memory whose accessible length is not known. The first element’s fault and later-element faults can have different behavior, including shortening `VL`.

They are not blanket fault suppression. Exact destination, `VL` and trap rules govern safe use.

### Handle interrupts

Implementations using multiple beats can accept interrupts between instructions or at architecture-defined restart points. Architectural progress state preserves a valid prefix.

Latency bounds may require checkpoints. Functional restart correctness and real-time response are separate evidence.

### Save vector context

An OS must preserve live vector data plus configuration, mask, rounding/saturation and restart state. Lazy ownership can avoid saves for tasks that never use vectors.

Lazy schemes need secure ownership transitions and interrupt handling. Stale tail or physical-lane state can leak across processes.

### Define vector ABIs

An ABI assigns vector argument/result and caller/callee-save roles, or prohibits persistent vector state across ordinary calls. Variants depend on extension/profile.

Cross-module object attributes ensure compatible code. ISA support alone does not establish a vector calling convention.

### Virtualize vector state

Hypervisors expose a virtual vector capacity/profile and preserve guest state. Migration targets must support the promised architectural maximum or use a compatible abstraction.

Physical lane count need not match guest vector length. Correctness follows the architectural configuration and saved state.

### Support debugging

Debuggers display register bits and current element interpretation. A register view without `VL`, element width, grouping and mask policy can mislead.

Stopping during restartable execution must expose a defined architectural boundary and progress state, not arbitrary physical beat state.

### Autovectorize loops

Compilers prove iteration independence or insert runtime alias checks before combining iterations. Reductions need approved reassociation rules.

Reports should state why a loop vectorized or did not. A vector instruction in disassembly does not prove all intended work uses vectors.

### Handle remainder iterations

Fixed SIMD uses scalar cleanup, masked final operations or overread-safe padding. Scalable vectors naturally reduce `VL` for the final chunk.

Overreading beyond an array is invalid even if unwanted lanes are later discarded, unless masking suppresses the memory access and language rules permit it.

### Use intrinsics carefully

Intrinsics expose target operations/types but still follow compiler semantics and feature flags. They can constrain optimization or encode policy more explicitly than autovectorization.

Feature dispatch must prevent execution on unsupported hardware. ABI and inlining across feature boundaries require care.

### Measure throughput realistically

Report operations per instruction, instructions per cycle, active-lane utilization and memory bytes separately. A wide instruction can decompose into several micro-operations.

Include alignment, mask density, gather locality, reductions and tails. Roofline limits distinguish compute from bandwidth bottlenecks.

### Analyze energy and thermal effects

Wide datapaths and register files increase switching and port pressure. Sustained vector code can trigger frequency or power limits.

Measure delivered work per joule and sustained frequency, not only short peak throughput. Thermal environment and workload duration belong in evidence.

### Analyze security

Vector state can retain secrets in inactive/tail elements and physical storage. Context clearing and architectural agnostic policies need a threat-specific strategy.

Masked/gather addresses can affect caches and timing. Constant-time claims require instruction, implementation and memory-system evidence.

### Verify across capacities

Run vector-length-agnostic binaries with multiple legal `VLMAX` configurations in models and hardware. Exercise `VL=0`, one, maximum and partial tails.

Generate masks, overlaps, widths, rounding modes, address patterns and faults. Compare only architecturally constrained elements and exact progress state.

### Govern lifecycle evidence

Bind ISA/profile, compiler flags, intrinsics, ABI, binary, OS context policy, hypervisor, model, RTL configuration and silicon. Preserve numerical inputs and tolerances.

Track errata for tails, masks, gathering, restart or context. Workarounds remain explicit and revision-scoped.

## Definitions and Notation

- `VL`: active vector element count for the current instruction.
- `VLMAX(C)`: maximum active elements under configuration `C`.
- `SEW`: selected element width in bits.
- `LMUL`: architectural register-group multiplier where applicable.
- `A[i]`, `B[i]`, `D[i]`: architectural source/destination elements.
- `M[i]`: predicate bit selecting element `i`.
- `Active(i)`: `0 <= i < VL` and mask enabled or absent.
- `Tail(i)`: `VL <= i < VLMAX(C)` within the destination group.
- `Inactive(i)`: `i < VL` and `M[i]=0`.
- `vstart`: restart element index where provided.
- `base`, `stride`, `index[i]`: vector-memory address operands.
- `EA[i]`: effective address of active element `i`.
- `sat`: architectural saturation status where defined.
- `round`: active rounding mode.
- `beat`: implementation subset of elements processed together; not necessarily architectural.

Element indices are architectural logical indices; physical lane assignment is intentionally unspecified.

## Mechanisms, Invariants, or Proof Structure

1. **Configuration obligation:** prove `VL`, element width/type, grouping and feature state are legal and decoded consistently.
2. **Element obligation:** prove every active element applies the exact scalar/vector function at its declared width.
3. **Mask obligation:** prove masked-off elements suppress computation/access and follow inactive-destination policy.
4. **Tail obligation:** prove tail elements are preserved, zeroed or agnostic exactly as configured.
5. **Overlap obligation:** prove source/destination groups are legal and pre-state data is used under allowed overlap.
6. **Conversion obligation:** prove widening/narrowing, signedness, rounding, saturation and exception flags per element.
7. **Permutation obligation:** prove index, out-of-range, duplicate and cross-element movement semantics.
8. **Reduction obligation:** prove association/order and mask/tail participation match numerical claims.
9. **Address obligation:** prove contiguous, strided, indexed and segment addresses, sizes and active access sets.
10. **Memory-order obligation:** prove element and instruction observations obey the ISA memory model and ordered variants.
11. **Fault obligation:** prove completed prefix, destination/memory state, restart index and reexecution are consistent.
12. **Context obligation:** prove OS, ABI, virtualization and debug preserve every enabled vector/configuration state item.
13. **Compiler obligation:** prove vectorization, alias checks, remainders and feature dispatch preserve defined source/IR behavior.
14. **Refinement obligation:** prove physical lanes/beats and speculation commit the architectural element/fault relation.
15. **Evidence obligation:** bind specs, compiler, ABI, binary, OS, model, RTL, hardware, numerical policy and errata versions.

## Alternatives and Trade-Offs

1. **Fixed versus scalable width:** fixed SIMD simplifies state/code generation; scalable vectors make binaries capacity-agnostic.
2. **Many narrow versus fewer wide elements:** narrow raises parallel count; wide extends range/precision.
3. **Dedicated predicate versus vector masks:** predicates compress control state; vector masks reuse registers/types.
4. **Undisturbed versus agnostic tails:** undisturbed eases composition; agnostic policy frees implementation dependencies.
5. **Zeroing versus merging masks:** zeroing breaks dependencies; merging preserves prior values.
6. **Separate versus grouped registers:** separate registers simplify allocation; grouping supports wide logical vectors.
7. **Wrap versus saturation:** wrap matches modular arithmetic; saturation suits media/signal domains.
8. **Ordered versus unordered reductions:** ordered improves reproducibility; unordered trees improve throughput.
9. **Contiguous versus gather/scatter:** contiguous maximizes locality; indexed forms express irregular data.
10. **Scalar cleanup versus masked tail:** cleanup is portable/simple; masking avoids control overhead.
11. **All-or-none versus restartable partial faults:** precision simplifies software; restart supports long vectors efficiently.
12. **Eager versus lazy context save:** eager is simple; lazy saves common overhead but complicates ownership.
13. **Autovectorization versus intrinsics:** auto preserves portability; intrinsics expose target control.
14. **Wide peak versus sustained efficiency:** width raises peak operations; memory/power can limit sustained work.
15. **Architectural detail versus implementation freedom:** exact policies aid software; agnostic/length-neutral rules enable diverse hardware.

## Failure Modes and Misconceptions

1. “SIMD and vector-length architectures are identical.” Their width/configuration contracts differ.
2. “Architectural elements equal physical lanes.” Hardware can time-multiplex or subdivide lanes.
3. “Vector register bits have a permanent type.” Configuration/instruction supplies interpretation.
4. “Requested VL is always returned unchanged.” Capacity/configuration can reduce it.
5. “Pointer advance uses requested length.” It must use actual `VL`.
6. “Any register can start any group.” Alignment and range constraints apply.
7. “Mask false means destination zero.” Policy may preserve or make it agnostic.
8. “Tail elements are always preserved.” Tail policy can allow agnostic values.
9. “Agnostic values are random but safe to consume.” They are semantically unconstrained.
10. “Little endian reverses element numbering.” Byte order and element index are distinct.
11. “Packed addition carries between elements.” Ordinary lane-wise addition does not.
12. “Widening only changes the destination type.” Group capacity and overlap change too.
13. “Narrowing always truncates.” Rounding/saturation forms differ.
14. “Floating reduction equals scalar left fold.” Association can differ.
15. “Masked loads may access then discard inactive lanes.” Architectural suppression can forbid those accesses/faults.
16. “Gather indices are element numbers.” They may be byte offsets or scaled under exact rules.
17. “Scatter duplicate addresses behave like atomic reduction.” Ordering/conflict semantics differ.
18. “Aligned vector base prevents page crossing.” Total access span can cross.
19. “Elements become globally visible in index order.” Memory-order rules decide.
20. “Any partial vector fault can restart at zero.” Repeating completed stores can be wrong.
21. “Saving vector data registers is a complete context.” Configuration, mask/status/restart also matter.
22. “ISA vector support defines the call ABI.” ABI variants separately assign roles.
23. “A vector instruction proves a speedup.” Utilization, latency and memory determine it.
24. “Speedup equals active element count.” Dependencies/resources prevent that bound.
25. “Architectural context clearing removes physical remnants.” Separate leakage evidence is needed.
26. “Testing one vector width proves scalable correctness.” Multiple capacities and tails are essential.

## Worked Examples

### Example 1

With `VLMAX=4` and ten elements, strip mining chooses `VL` values 4, 4 and 2 and advances by each actual value.

### Example 2

Four 32-bit elements occupy one fixed 128-bit SIMD register; eight 16-bit elements occupy the same bits under another operation.

### Example 3

With `VL=3` and mask `[1,0,1]`, only elements 0 and 2 compute; element 1 follows inactive policy.

### Example 4

With tail-undisturbed and capacity four but `VL=2`, destination elements 2 and 3 retain their pre-state values.

### Example 5

Signed widening of byte `0xff` yields wider `-1`; unsigned widening yields 255.

### Example 6

Saturating signed 8-bit addition of 120 and 20 yields 127, whereas wrapping addition yields -116 as an 8-bit signed interpretation.

### Example 7

Unit-stride 32-bit element addresses from base `0x1000` are `0x1000`, `0x1004`, `0x1008`, and so on.

### Example 8

Stride `-4` from base `0x1010` visits `0x1010`, `0x100c`, `0x1008`, showing signed address progression.

### Example 9

A gather fault at element 5 after a permitted completed prefix records restart state 5 so elements 0–4 are not repeated.

### Example 10

A tree floating reduction can differ in low bits from left-to-right accumulation; both require an explicit permitted-order/tolerance claim.

## Cross-Program Connections

- **Registers:** grouping, masks and configuration enlarge architectural context.
- **Pipelines:** lanes, beats, hazards and crossbars implement element operations.
- **Memory systems:** bandwidth, gathers, page crossings and ordering dominate many vectors.
- **Compilers:** dependence analysis, strip mining, predication and remainders lower loops.
- **Numerical computing:** reductions, rounding, fusion and saturation affect reproducibility.
- **Operating systems:** context ownership and traps preserve vector state.
- **Virtualization:** guests see architectural capacity independent of physical lanes.
- **Security:** masks, tails, context remnants and access timing can leak secrets.
- **Performance:** utilization, roofline limits, energy and thermal behavior shape speedup.
- **Formal methods:** element relations and restart prefixes support refinement proofs.

## References

1. RISC-V International, [V Vector Extension](https://docs.riscv.org/reference/isa/unpriv/v-st-ext.html), configurable vector length, element widths, grouping, masks, memory and restart semantics; retrieved 2026-09-04.
2. RISC-V International, [RISC-V Vector Intrinsic Specification](https://github.com/riscv-non-isa/rvv-intrinsic-doc), compiler intrinsic types, policies and operation mappings; retrieved 2026-09-04.
3. Arm, [Arm Architecture Reference Manual for A-profile Architecture](https://developer.arm.com/documentation/ddi0487/latest/), Advanced SIMD and scalable vector/predicate architecture semantics; retrieved 2026-09-04.
4. Intel, [Intel 64 and IA-32 Architectures Software Developer's Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), packed SIMD/vector registers, masks, arithmetic and memory operations; retrieved 2026-09-04.
5. LLVM Project, [Vector Type](https://llvm.org/docs/LangRef.html#vector-type), fixed and scalable IR vectors and operation semantics; retrieved 2026-09-04.
6. WebAssembly Community Group, [SIMD Proposal](https://github.com/WebAssembly/simd), portable 128-bit SIMD types and instructions; retrieved 2026-09-04.
7. OpenMP Architecture Review Board, [SIMD Construct](https://www.openmp.org/spec-html/5.2/openmpse60.html), source-level loop SIMD semantics and clauses; retrieved 2026-09-04.
8. RISC-V International, [Sail RISC-V Model](https://github.com/riscv/sail-riscv), executable vector semantics for differential/refinement evidence; retrieved 2026-09-04.

## Exercises

### Exercise 1

Specify active, inactive and tail destination behavior for one masked add under undisturbed, zeroing and agnostic policies.

### Exercise 2

Implement capacity-agnostic strip mining for a ten-element vector add with `VLMAX=4` and print every chunk/result.

### Exercise 3

Compare contiguous, strided, gather and segmented loads for addresses, locality, ordering and fault restart.

### Exercise 4

Design verification for a restartable masked vector store in an out-of-order core across page faults and repeated addresses.

### Exercise 5

Construct assurance for deploying a scalable vector extension across compiler, ABI, OS, hypervisor and two hardware capacities.

## Answers to the Exercises

### Answer 1

For `i<VL` and true mask, write `f(A[i],B[i])`. For false mask within `VL`, undisturbed preserves old `D[i]`, zeroing writes zero when that policy exists, and agnostic permits only the architecture-defined unconstrained set. For `i>=VL` within the group, apply the separate tail policy.

The mask suppresses memory access for inactive elements only when the memory instruction says so. Tests seed old destination with recognizable values and compare agnostic positions as unconstrained rather than demanding one implementation value.

### Answer 2

The loop advances by returned active length and therefore handles the final two-element tail without overread.

<!-- bijux-verify: {"id":"vector-strip-mining-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"start=0 vl=4 values=[11, 22, 33, 44]\nstart=4 vl=4 values=[55, 66, 77, 88]\nstart=8 vl=2 values=[99, 110]\nresult=[11, 22, 33, 44, 55, 66, 77, 88, 99, 110]\n"}} -->
```python
left = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
right = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
result = [0] * len(left)
vlmax = 4
start = 0

while start < len(left):
    vl = min(vlmax, len(left) - start)
    values = [left[start + i] + right[start + i] for i in range(vl)]
    result[start : start + vl] = values
    print(f"start={start} vl={vl} values={values}")
    start += vl

print(f"result={result}")
```

The trace establishes one integer strip-mined calculation only. It provides no vector encoding, masks, faults, ordering, compiler, timing or hardware evidence.

### Answer 3

Contiguous uses `base+i*element_size` and usually offers best spatial locality. Strided uses `base+i*stride`, including negative/zero cases. Gather uses per-element indices with exact scale/extension and can touch unrelated pages. Segment loads fetch multiple interleaved fields per logical element and consume multiple destination groups.

For each, enumerate active addresses before reasoning about cache behavior. Apply mask suppression, translation, permission and alignment per semantics. Specify element visibility order and completed-prefix/restart state. Gather duplicates and segment partial faults need special tests.

### Answer 4

Generate masks with faults on every active index, and prove masked-off faulting addresses are not accessed. Track store addresses/data, committed prefix and `vstart`; after repair/restart, each permitted element must appear exactly as specified without unintended duplicate device/normal-memory effects.

Include repeated addresses, page crossings, alignment, translation races, interrupts and branch misprediction. Assert store-buffer entries cannot become visible before the element is permitted. Compare independent model, RTL retirement/memory traces and final memory, binding vector capacity/configuration and memory model.

### Answer 5

Freeze extension/profile, minimum capacity, element/group/mask/tail policies, fault restart and discovery. The compiler must generate length-agnostic loops and compatible feature dispatch; the ABI defines call roles; OS/hypervisor preserve data, configuration, masks/status and restart state; debug understands dynamic interpretation.

Run identical binaries on models/hardware with at least two capacities and all boundary `VL` values. Test context switching, migration, signals, nested faults, numerical modes, security clearing and errata. Measure performance/power separately. Preserve flags, objects, binaries, contexts, traces and revisions. Named ISA, compiler, ABI, OS, hypervisor, RTL, formal, numerical, security, performance and independent-assurance reviewers assess their scopes. This module supplies no certification.
