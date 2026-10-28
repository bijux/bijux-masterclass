---
module_id: CONPAR-078
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 78
title: Kernel Fusion and Data Movement
status: complete
last_verified: 2026-08-29
---

# Kernel Fusion and Data Movement

## One-Page Review

### Governing question

When may adjacent accelerator operations be executed as one kernel so an intermediate value stays in registers or shared/local storage, and when does fusion destroy correctness, parallelism, locality, or operability?

### Essential definitions

- A **kernel graph** is a directed graph whose nodes are operations and whose edges carry data or control dependencies.
- **Materialization** writes a logical value into an addressable storage boundary for later use.
- **Kernel fusion** replaces multiple kernel nodes with one kernel while preserving declared observable behavior.
- **Kernel fission** splits one kernel into multiple kernels to recover parallelism, overlap, specialization, or resource fit.
- **Producer-consumer fusion** computes a producer value near or inside its consumer instead of materializing the entire producer output.
- **Horizontal fusion** combines independent same-domain operations; **vertical fusion** combines dependent stages.
- A **fusion group** is a set of graph operations selected for one generated kernel.
- **Recomputation** regenerates a producer value rather than storing and loading it.
- A **live range** spans the period during which a value must remain available; fusion often extends live ranges.
- A **global synchronization boundary** orders work that cannot be coordinated by an ordinary work-group barrier.
- A **launch graph** batches and replays dependency nodes to reduce submission overhead; it does not necessarily fuse device kernels.
- **Operational intensity** and byte ledgers must name the hierarchy boundary at which avoided traffic is claimed.

### Central model, mechanism, or theorem

Fusion is legal only if a schedule exists that preserves every data/control dependency, address and lifetime rule, synchronization edge, side effect, identity mapping, and numeric contract. Its benefit is the value of avoided intermediate allocation, global writes/reads, transfers, and launches. Its cost includes redundant producer work, larger tiles/halos, barriers, extended live ranges, registers/spills, shared memory, lower residency, instruction/cache pressure, reduced parallelism, lost library specialization, compilation, and operational coupling. Compare complete verified pipelines; never infer speedup from an intermediate-byte ratio alone.

### Critical invariants

Every consumer receives the same defined producer value under the declared equivalence; all producer-consumer dependences are preserved; aliases and in-place updates cannot overwrite values still needed; each output has one owner or a valid atomic/reduction protocol; no cross-work-group dependence is replaced by an insufficient local barrier; tile halos cover every read; recomputation is pure or explicitly repeatable; floating and reduction order follows policy; memory and failure boundaries remain intentional; asynchronous buffers live through completion; launch-graph edges retain required ordering; resource use fits all targets; and fallback, debugging, attribution, privacy, and high-stakes review remain possible.

### Common failures

Teams fuse because two kernels are adjacent, subtract logical intermediate bytes without cache or spill evidence, erase a necessary grid synchronization, duplicate an impure producer, change reduction order silently, mishandle aliases, load incomplete halos, fuse across incompatible iteration domains, increase registers until spills replace the avoided traffic, lower occupancy below useful latency hiding, recompute an expensive producer for many consumers, block overlap, reject a tuned library kernel, confuse graph replay with fusion, compare only kernel time, or deploy an opaque megakernel with no attribution or bounded fallback.

### Compact example

For eight values, three pure pointwise stages `a=2x`, `b=a+3`, `y=b²` materialized separately perform three global reads and three writes per value in a simple boundary ledger. A fused stage performs one read and one write: 192 versus 64 modeled bytes for 4-byte values, avoiding 128 bytes. Both produce `[9,25,49,81,121,169,225,289]`. This 3× traffic ratio is not a 3× speed claim.

### Connections

[GPU Memory Hierarchies](076-gpu-memory-hierarchies.md) defines placement and transfer boundaries. [Coalescing, Divergence, and Occupancy](077-coalescing-divergence-and-occupancy.md) explains resource and lane-efficiency costs. [Happens-Before Relations](023-happens-before-relations.md) supplies dependency reasoning. The [program roadmap](../ROADMAP.md) next composes heterogeneous CPU-GPU pipelines and profiles an accelerator kernel.

## Governing Question

Given an operation graph and target, which materialization boundaries are semantically necessary, which are merely one schedule, and which fusion group minimizes verified end-to-end cost for the actual workload?

The answer is not “fuse everything.” Materialization can provide synchronization, fan-out, reuse, checkpointing, observability, isolation, or access to a highly tuned library. Fusion is a schedule transformation with a proof obligation and a target-specific cost model.

## Why This Matters

Accelerators can execute a pointwise operation faster than they can launch it or round-trip a large intermediate through global memory. ML, imaging, scientific, database, and signal pipelines therefore benefit from retaining values on chip and amortizing launch work. Compiler systems use graph IRs, dependence analysis, tiling, and cost models to discover these opportunities.

Yet fusion enlarges the unit of compilation, execution, resource allocation, failure, and diagnosis. It may serialize stages that were previously parallel, extend values across branches, inflate registers, duplicate boundary work, or turn a recoverable node into a long-running kernel. A production design treats fusion and fission as alternatives, preserves a reference graph, and records why each removed boundary was safe.

## Prerequisites and Retrieval

Retrieve:

- address spaces, residency, tiling, migration, and byte ledgers from [GPU Memory Hierarchies](076-gpu-memory-hierarchies.md);
- transaction efficiency, divergence, occupancy, spills, and causal measurement from [Coalescing, Divergence, and Occupancy](077-coalescing-divergence-and-occupancy.md);
- grids, group-local barriers, block independence, and device events from [GPU Execution Grids, Blocks, and Warps](075-gpu-execution-grids-blocks-and-warps.md); and
- ordering, visibility, and publication from [Happens-Before Relations](023-happens-before-relations.md).

Retrieval prompt: draw one accelerator DAG with shapes, index maps, producers/consumers, aliases, side effects, numeric contracts, synchronization and memory boundaries, byte sizes, launch times, compiler resources, and measured critical path. For each edge, why does it materialize?

## Learning Objectives

After completing this module, a learner can:

1. represent an accelerator pipeline as a dependency graph with observable and scheduling boundaries;
2. prove pointwise fusion by substitution under purity, domain, bounds, alias, and numeric assumptions;
3. design tiled producer-consumer fusion with complete regions, halos, barriers, and output ownership;
4. identify reductions, scans, scatters, global dependencies, side effects, and fan-out that restrict fusion;
5. calculate avoided intermediate traffic and launch cost without presenting them as speedups;
6. compare materialization, recomputation, registers, shared/local storage, and cache reuse;
7. reason about registers, spills, shared capacity, occupancy, instruction pressure, and lost parallelism;
8. distinguish kernel fusion, launch graphs, batching, persistent kernels, and fission;
9. validate compiler-generated fusion across dynamic shapes, targets, failures, and numeric modes; and
10. preserve profiling, privacy, rollout, fallback, and human-review boundaries in production.

## Core Exposition

### Start from the operation DAG

Represent each operation as a node with iteration domain, inputs, outputs, index maps, side effects, shape/dtype/layout, numeric semantics, and target placement. Edges carry values and ordering. A materialized tensor or buffer is one possible implementation of an edge, not necessarily part of the algorithm.

Classify observations: final outputs; host/device I/O; externally visible mutations; atomics or ordered logging; exceptions and errors; timing/timeout boundaries; deterministic/reproducible order; checkpoints; and debug/audit records. Fusion may change internal storage while preserving the declared observation set. If intermediate values are part of an API, inspection contract, or retry checkpoint, deleting them changes behavior unless an alternative preserves that contract.

A legal fusion group must have a schedulable dependence subgraph. Producer values must be available before each consumer use, and writes must not destroy still-live inputs. Cycle-free high-level graphs can still contain loop-carried or cross-item dependencies that prevent simple same-item fusion.

### Pointwise substitution

Suppose `a_i=f(x_i)` and `y_i=g(a_i)` over identical domains with pure total functions. Substitution gives `y_i=g(f(x_i))`, so one work-item can load x, retain a privately, and store y. The materialized a buffer disappears.

The assumptions matter. If f writes a counter, may trap for values later masked by g, uses randomness, reads mutable state, or must be rounded/stored at a narrower dtype before g, direct substitution changes behavior. If y aliases x, execution order can expose overwritten inputs. If broadcasting or indexing maps differ, a producer value may serve many consumers; recomputing it per consumer changes work and possibly semantics.

Floating fusion can contract operations, retain extra precision, change rounding points, reassociate expressions, or alter math-library calls. Define whether equivalence is bitwise, correctly rounded at materialization types, tolerance-based, deterministic per target, or scientifically validated. Compiler fast-math modes are part of the proof context.

### Byte and launch ledgers

For an intermediate of N elements and s bytes, separate materialization commonly writes Ns bytes and a consumer later reads Ns bytes at the global-memory boundary: up to 2Ns candidate bytes avoided by fusion. Multiple consumers, partial use, compression, cache hits, write allocation, spill traffic, and recomputation alter the actual value. Count measured transactions/bytes at a named level.

Kernel fusion also removes launch/dispatch edges. Launch overhead matters for many short kernels, but device execution may overlap with host work or other kernels. CUDA and HIP graphs can reduce repeated submission overhead while retaining kernel nodes and explicit dependencies. Graph replay is therefore an alternative experiment, not evidence that a device kernel was fused.

End-to-end accounting includes allocation, compilation/autotuning, transfers, graph setup, launches, execution, synchronization, retries, and cleanup. Amortize one-time costs over the real reuse count. Include energy or memory-capacity objectives when relevant.

### Tiled producer-consumer fusion

When a consumer uses a neighborhood of producer values, one fused block can compute a producer tile plus halo, synchronize, then consume its core. For consumer output tile `T_x×T_y` and producer radius r, the required producer region is commonly `(T_x+2r)×(T_y+2r)` subject to boundary policy and composed index maps.

Prove that cooperative loads or computations initialize every producer slot read, including edges/corners. All required work-items reach the publication barrier. Each core output has exactly one owner. A second barrier precedes scratchpad reuse. Check checked arithmetic, pitch/layout, partial tiles, shared capacity, banks, and register live ranges.

Halos duplicate producer computation across adjacent blocks. This may be cheaper than global materialization or may dominate for small tiles/expensive producers. Enlarging tiles reduces relative halo but consumes resources. A compiler cost model needs operation cost, reuse, tile shape, and target resources; a benchmark validates candidates.

### Dependences that constrain fusion

A kernel boundary naturally gives grid-wide completion and global-memory visibility through the command/event model. An ordinary block barrier cannot replace it. If stage B consumes values from arbitrary blocks of stage A, naive fusion can deadlock or race because blocks execute independently. Legal alternatives include tiled ownership that contains dependences, cooperative grid mechanisms with checked residency/support, a separate launch, or a redesigned algorithm.

Reductions and scans carry order and communication. Fusing a pointwise epilogue into the final reduction stage may be straightforward; folding arbitrary producers or consumers can change reduction trees, precision, atomic order, and determinism. Scatters and histograms require ownership/atomic analysis. Stateful random generators, queues, I/O, host callbacks, and device-side allocation add effects that may be non-repeatable.

Fan-out creates a storage/recompute decision. If many consumers use the same expensive producer at different schedules, materialize once. Selective fusion may clone the producer for one consumer and retain materialization for another. Multi-output fusion can share computation but extend live values and stores. Dead outputs should be eliminated before costing fusion.

### Resource and parallelism costs

Separate kernels release registers/shared memory and allow each stage its own block shape, launch size, specialization, and scheduling. Fused kernels combine resource demands and extend live ranges. More registers can cross allocation cliffs or spill intermediates to local/global-backed memory, replacing the traffic supposedly removed. More shared memory can reduce resident blocks and latency hiding.

Fusion can also increase instruction footprint, compilation time, divergence, and imbalance. A cheap pointwise producer fused into a large matrix library kernel may prevent use of a highly tuned vendor implementation. Different stages may prefer incompatible layouts or tile shapes. A materialization can be an intentional layout conversion that makes the next stage far faster.

Conversely, fission may improve occupancy, specialization, concurrent scheduling, transfer overlap, and error attribution. It pays intermediate storage and launches. Horizontal fusion of independent operations amortizes launch/input reads but can couple unrelated critical paths and make tails wait for the slowest portion.

### Compiler and DSL reasoning

Graph compilers typically perform shape/type inference, alias/effect and dependence analysis, canonicalization, dead-code elimination, fusion grouping, tiling, memory planning, lowering, code generation, and autotuning. Higher-level structured IR retains iteration and indexing information needed to decide fusion; premature lowering to opaque loops makes analysis harder.

Fusion heuristics are target and workload policies. Cache compiled artifacts by complete keys: graph/IR hash, shapes or guards, dtypes/layouts, numeric flags, compiler/runtime versions, target architecture/features, and tuning parameters. Dynamic shapes need guards and fallbacks; a kernel specialized for one extent must not silently run another.

Validate generated source/IR/resource reports where possible. Differentially execute unfused reference and fused variants. Compiler success is not semantic evidence; a compiler bug, wrong alias fact, invalid shape guard, or stale cache can miscompile production workloads.

### Executable materialization model

This deterministic Python model compares pure pointwise values and a simplified global-boundary byte ledger. It does not launch or fuse GPU kernels, model cache/spill traffic, preserve hardware rounding, measure time, or validate a compiler.

<!-- bijux-verify: {"id":"fusion-materialization-ledger","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"inputs=[0, 1, 2, 3, 4, 5, 6, 7]\nunfused_outputs=[9, 25, 49, 81, 121, 169, 225, 289]\nfused_outputs=[9, 25, 49, 81, 121, 169, 225, 289]\nequivalent=True\nunfused_global_bytes=192\nfused_global_bytes=64\nmodeled_bytes_avoided=128\nmodeled_traffic_ratio=3.000\n","stderr":""}} -->
```python
inputs = list(range(8))
value_bytes = 4

stage_a = [2 * value for value in inputs]
stage_b = [value + 3 for value in stage_a]
unfused_outputs = [value * value for value in stage_b]

fused_outputs = []
for value in inputs:
    temporary = 2 * value + 3
    fused_outputs.append(temporary * temporary)

unfused_global_bytes = len(inputs) * value_bytes * 6
fused_global_bytes = len(inputs) * value_bytes * 2

print(f"inputs={inputs}")
print(f"unfused_outputs={unfused_outputs}")
print(f"fused_outputs={fused_outputs}")
print(f"equivalent={unfused_outputs == fused_outputs}")
print(f"unfused_global_bytes={unfused_global_bytes}")
print(f"fused_global_bytes={fused_global_bytes}")
print(f"modeled_bytes_avoided={unfused_global_bytes - fused_global_bytes}")
print(f"modeled_traffic_ratio={unfused_global_bytes / fused_global_bytes:.3f}")
```

The model counts one read and one write for each of three separate stages, versus one input read and final write when fused. Real intermediates may remain cached, fused values may spill, and the pipeline may include other traffic; counters and timing decide.

### Verification and operations

Test zero/one, tile and halo boundaries, dynamic shapes, broadcasts, non-contiguous views, aliases/in-place forms, fan-out, unused outputs, extreme values, NaN/infinity/signed zero, dtype conversions, reductions, empty reductions, sparse masks, and every side effect. Use race/bounds/uninitialized tools, forced scheduling, heterogeneous targets, and compiler optimization modes. Compare intermediates in a diagnostic unfused mode when final mismatch localization matters.

Benchmark isolated nodes, unfused pipeline, fused candidates, graph replay, and fission with the same inputs/outputs. Record global/cache/spill bytes, registers/shared memory, occupancy/readiness, launches, compilation, memory peak, critical path, energy where relevant, and time distributions. Test cold/warm caches and compilation, concurrency, pressure, cancellation, device loss, and fallback.

Operationally retain fusion-group provenance and per-region correlation so failures are attributable. Bound compilation/autotuning and cache growth. Validate artifacts before load; isolate tenants; do not expose sensitive tensors through dumps, generated source, profiler traces, or caches. Canary by target and shape class, monitor correctness and latency tails, and roll back to a verified graph.

High-stakes transformations require named domain, numerical, compiler, safety, security, operations, and independent reviewers. Internal differential tests do not establish clinical/scientific validity or certification.

## Definitions and Notation

- `G=(V,E)`: operation DAG with nodes V and dependency edges E.
- `D_v`: iteration domain of operation v.
- `I_v`: index mapping from an output point to each input point.
- `M_e`: materialized value on edge e.
- `N_e`: element count and `s_e` bytes per element for edge e.
- `X_q`: measured or modeled bytes crossing hierarchy boundary q.
- `L_k`: launch/dispatch cost for kernel k under a stated protocol.
- `C_r`: recomputation cost introduced by fusion.
- `R_f,S_f`: fused-kernel register and shared/local resource allocation.
- `H(T,r)`: halo region required for output tile T and radius r.
- `F`: selected fusion group.
- `Obs(P)`: declared observable behavior of pipeline P.
- `T(P)`: measured end-to-end time distribution for P.

`Obs(P_fused)=Obs(P_reference)` is conditional on declared numeric, failure, ordering, and inspection contracts; it is not implied by equal shapes.

## Mechanisms, Invariants, or Proof Structure

### Dependence preservation proof

Topologically order operations inside F or construct an equivalent tiled schedule. For every read, identify the unique/valid writer and show its value is produced and visible first. Preserve anti/output dependences caused by aliasing. Prove all external input/output and side-effect edges retain order and lifetime.

### Domain and region proof

Compose consumer index maps backward through producers to derive exactly the required producer region. Bounds and boundary rules cover every point. Cooperative initialization and barriers cover shared regions; unique output ownership covers the consumer domain. Redundant halo work is quantified, not ignored.

### Numeric and effect equivalence

For pure pointwise operations, substitute expressions while preserving mandated dtype conversions and rounding points. For reductions, atomics, RNG, exceptions, or other effects, compare allowed orders and state; reject fusion unless the declared equivalence and safety contract is proven.

### Cost inequality

Fusion is a measured candidate when avoided materialization/launch benefit exceeds recomputation, staging, resource/spill, lost parallelism/library, compilation, and operational costs for the workload objective. Terms require common units or direct comparative measurement; logical bytes alone cannot satisfy the inequality.

### Lifecycle proof

Generated artifacts are keyed and validated for graph, shapes/guards, numeric flags, target, and versions. Buffers survive ordered last use. Cancellation/failure produces an attributable state and safe retry/fallback. Rollback restores a reference path without incompatible intermediate assumptions.

## Alternatives and Trade-Offs

| Choice | Main benefit | Principal cost or limitation |
|---|---|---|
| Separate kernels | synchronization, modularity, specialization | intermediate traffic and launches |
| Pointwise fusion | private intermediates, fewer launches | live ranges and coupled code |
| Tiled fusion | locality across neighborhoods | halos, barriers, resources |
| Recomputation | avoids storage/loads | duplicated compute and effects risk |
| Materialization | fan-out reuse, checkpoint, inspection | memory capacity and traffic |
| Horizontal fusion | shared input/launch amortization | divergent domains and tail coupling |
| Fission | resources, overlap, specialization | extra boundary and orchestration |
| Launch graph | lower repeated submission overhead | retains device boundaries/traffic |
| Persistent kernel | amortized launch and dynamic work | queues, fairness, watchdog, complexity |
| Tuned library node | mature target specialization | boundary/layout and fusion limits |

Preserve at least one trusted unfused/reference execution mode for evidence and fallback.

## Failure Modes and Misconceptions

- **“Adjacent kernels are fusible.”** dependency domains, aliases, effects, and synchronization decide.
- **“Fusion is algebraic substitution.”** storage rounding, errors, order, and state may be observable.
- **“Two fewer buffers means their full bytes are avoided.”** caches, partial use, fan-out, and spills intervene.
- **“A local barrier replaces the launch boundary.”** it cannot order arbitrary work-groups.
- **“Recomputation is free.”** producer cost, duplication, and effects matter.
- **“More fusion means more locality.”** live ranges and working sets can grow.
- **“Removing launches always improves time.”** execution/resource regression can dominate.
- **“Graphs fuse kernels.”** graphs primarily represent/replay nodes and dependencies.
- **“Compiler fusion is correct by construction.”** analysis, guards, caches, and code generation can fail.
- **“Equal final samples prove equivalence.”** boundaries, adversarial values, races, and side effects remain.
- **“Floating point is unchanged.”** contraction, precision, and reduction order can move.
- **“Fan-out should always be recomputed.”** materialization may amortize an expensive producer.
- **“A megakernel maximizes occupancy.”** combined resources can reduce residency or spill.
- **“One block shape suits all stages.”** iteration and resource optima can conflict.
- **“A faster kernel is a faster service.”** compilation, transfers, queues, and retries remain.
- **“Opaque fusion is acceptable in production.”** attribution, rollback, and auditability are requirements.

## Worked Examples

### Example 1

**Pure maps.** `a=2x`, `b=a+3`, `y=b²` fuse by substitution with one input read and final store. **Conclusion:** declare dtype rounding and purity before applying the algebra.

### Example 2

**Masked exception.** A separate producer computes reciprocal only for valid items; eager fused predication divides by zero for invalid lanes. **Conclusion:** removed control boundaries must preserve evaluation safety.

### Example 3

**Stencil halo.** A blur consumer tile needs a larger producer color-conversion region. Neighboring blocks duplicate halo conversion. **Conclusion:** region composition and redundant work belong in the cost.

### Example 4

**Grid dependency.** Stage B reads neighbor outputs produced by arbitrary blocks of A. A block barrier in one fused kernel is insufficient. **Conclusion:** keep a launch boundary or redesign ownership/cooperation.

### Example 5

**Fan-out.** An expensive transform feeds three consumers with different tilings. Fusing into each triples work. **Conclusion:** one materialization can be the optimal reuse boundary.

### Example 6

**Spill inversion.** Fusion removes 64 MB of intermediate traffic but extends live accumulators and generates 110 MB of spill traffic. **Conclusion:** measure final-binary traffic, not source buffers.

### Example 7

**Library epilogue.** A supported matrix-library epilogue fuses bias/activation without abandoning the tuned matrix kernel. **Conclusion:** use reviewed fusion surfaces before replacing mature libraries.

### Example 8

**Graph replay.** Ten short kernels retain their boundaries but execute through one instantiated launch graph. Host submission time falls while intermediate device traffic remains. **Conclusion:** isolate launch and materialization hypotheses.

### Example 9

**Fission for overlap.** Splitting a monolithic transform lets chunks transfer concurrently with compute and reduces register pressure. **Conclusion:** an extra kernel can improve the complete schedule.

### Example 10

**Radiation-dose reconstruction.** Fusing correction, filtering, projection, and dose stages must preserve patient/series/geometry identity, units, calibration, detector defects, interpolation/boundaries, precision and summation, masks, uncertainty, error attribution, fallback, privacy, and audit records. Named medical-physics, radiation-oncology, imaging/reconstruction, numerical, GPU/compiler, software-safety, security/privacy, operations, quality/regulatory, human-factors, and independent validation reviewers must approve requirements and evidence; none is claimed here. **Conclusion:** eliminated tensors and lower latency establish neither dose correctness nor clinical safety.

## Cross-Program Connections

- **Compilers:** dependence/effect analysis, structured IR, tiling, lowering, guards, and artifact caches enable fusion.
- **Algorithms:** maps, stencils, reductions, scans, sparse operations, and dynamic work impose different boundaries.
- **Computer architecture:** hierarchy traffic, registers, caches, scratchpads, instruction footprint, and schedulers price schedules.
- **Programming languages:** purity, exceptions, aliasing, numeric semantics, and observation define equivalence.
- **Distributed systems:** DAGs, materialization, recomputation, checkpoints, lineage, retries, and failure domains recur at cluster scale.
- **Databases:** operator pipelines, vectorized batches, exchanges, and blocking operators mirror fusion decisions.
- **Numerical computing:** rounding points, contraction, reduction trees, and reproducibility constrain transformation.
- **Testing:** differential execution, intermediate capture, metamorphic cases, race tools, and shape matrices provide evidence.
- **Security:** generated artifacts, tensor dumps, caches, spills, and traces require isolation and retention controls.
- **Operations:** compilation budgets, canaries, attribution, timeouts, rollback, and target-aware fallback make fusion deployable.

## References

1. Jonathan Ragan-Kelley et al., “Halide: A Language and Compiler for Optimizing Parallelism, Locality, and Recomputation in Image Processing Pipelines,” PLDI 2013. <https://doi.org/10.1145/2491956.2462176>
2. Tianqi Chen et al., “TVM: An Automated End-to-End Optimizing Compiler for Deep Learning,” OSDI 2018. <https://www.usenix.org/conference/osdi18/presentation/chen>
3. Philippe Tillet, H. T. Kung, and David Cox, “Triton: An Intermediate Language and Compiler for Tiled Neural Network Computations,” MAPL 2019. <https://doi.org/10.1145/3315508.3329973>
4. LLVM Project, *MLIR Linalg Dialect*, current documentation; retrieved 2026-08-29. <https://mlir.llvm.org/docs/Dialects/Linalg/>
5. NVIDIA, *CUDA Programming Guide*, current documentation; retrieved 2026-08-29. <https://docs.nvidia.com/cuda/cuda-programming-guide/>
6. NVIDIA, *CUDA Programming Guide: CUDA Graphs*, current documentation; retrieved 2026-08-29. <https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/cuda-graphs.html>
7. NVIDIA, *CUDA C++ Best Practices Guide*, current documentation; retrieved 2026-08-29. <https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html>
8. AMD, *Introduction to the HIP Programming Model: Graph and Fusion APIs*, current documentation; retrieved 2026-08-29. <https://rocm.docs.amd.com/projects/HIP/en/develop/understand/programming_model.html>
9. AMD, *HIP Graph API Tutorial*, current documentation; retrieved 2026-08-29. <https://rocm.docs.amd.com/projects/HIP/en/latest/tutorial/graph_api.html>
10. Khronos SYCL Working Group, *SYCL 2020 Specification*, revision 12, 2026. <https://registry.khronos.org/SYCL/specs/sycl-2020/html/sycl-2020.html>

## Exercises

### Exercise 1

Prove or reject fusion for `a_i=round_f16(2x_i)`, `y_i=float32(a_i)+3` when a compiler substitutes `float32(2x_i)+3`. State the correct fused form under bitwise materialization semantics.

### Exercise 2

For three pure pointwise stages over ten million f32 values, calculate the simplified intermediate/global byte ledger for separate and fused kernels, peak intermediate capacity, and the evidence needed before predicting speedup.

### Exercise 3

Design tiled fusion for a radius-two producer-consumer stencil with a 16×8 output tile. Derive region size, f32 shared bytes, barriers, output ownership, halo duplication, and legality limits.

### Exercise 4

Compare kernel fusion, launch-graph replay, and fission for twelve small stages with one fan-out, a tuned library node, dynamic shapes, and a need for per-stage failure attribution.

### Exercise 5

A regulated genomic pipeline fuses normalization, filtering, alignment scoring, and variant statistics. Specify semantic, numeric, synchronization, privacy, compiler, failure/fallback, performance, and human-review evidence.

## Answers to the Exercises

### Answer 1

Reject the substitution under bitwise materialization semantics: storing a as f16 rounds after `2x_i`, whereas the proposed expression retains float precision until after addition and can differ. A correct scalar fused form computes `a16=round_f16(2x_i)` using the specified conversion/rounding mode, then converts `a16` to float32 and adds 3. Preserve overflow, subnormal, NaN, signed-zero, exception, and fast-math policy. Differentially test all relevant f16 values and extremes; inspect generated instructions. If the contract instead explicitly permits the wider fused expression within validated tolerance, that is a different declared equivalence.

### Answer 2

Let N=10,000,000 and s=4. Three separate pointwise stages each read and write Ns, totaling `6Ns=240,000,000` modeled global bytes. One fused stage reads input and writes final output: `2Ns=80,000,000`; candidate avoided bytes are 160,000,000 and ratio 3.0. Separate execution needs two intermediate tensors simultaneously only if lifetimes overlap; straightforward sequential reuse needs at least one 40,000,000-byte buffer, while distinct named outputs may need 80,000,000. Fused private temporaries remove that global capacity. Before predicting time, measure actual per-level traffic/cache/spills, launch cost, registers/shared/occupancy/readiness, instruction work, compilation, transfers, end-to-end distributions, and identical outputs on representative targets/workloads.

### Answer 3

Radius two expands a 16×8 consumer tile to `(16+4)×(8+4)=20×12=240` producer values, 960 f32 bytes before padding and other state. Compose index maps and boundary policy; cooperatively compute/load every halo/core value; all required members reach barrier 1 before consumption; one work-item or declared mapping owns each valid 16×8 output; barrier 2 precedes scratchpad reuse. Neighboring tiles duplicate halo producer work; quantify it against avoided writes/reads. Check partial tiles, pitch/overflow, shared allocation/banks, registers/spills, group limits, numeric order, aliases, and that every dependence lies inside the tile. Cross-tile dependencies need another boundary or supported grid mechanism.

### Answer 4

Preserve the tuned library node unless its reviewed epilogue supports the intended fusion. Fuse compatible short pointwise chains around it when dependence, shape guards, resources, and attribution allow. Retain the fan-out producer materialized if recomputing it or combining incompatible consumers costs more; selective fusion may keep one output. A launch graph can amortize twelve repeated submissions while preserving nodes, dependency edges, library specialization, and per-node diagnosis. Fission any fused region whose registers/shared footprint, dynamic shape mix, imbalance, or transfer-overlap opportunity dominates. Benchmark unfused, graph, fusion candidates, and fission with compilation/instantiation amortization, bytes/spills/resources, critical path, failures, and end-to-end distributions. Attach correlation metadata and keep per-stage diagnostic/reference replay.

### Answer 5

Define sample/read/reference/coordinate/allele identity, normalization and filtering rules, alignment scoring, variant model/statistics, all shapes/layouts/dtypes, exact integer and declared floating/reduction semantics, RNG, missing/duplicate data, and observable intermediate/audit requirements. Prove dependence/alias/ownership, complete regions, collective/event scope, and async lifetimes; retain materialization for cross-grid, fan-out, checkpoint, or review boundaries. Differentially compare reference/unfused/fused intermediates and finals across extremes, distributions, targets, compilers, dynamic guards, pressure, cancellation, device loss, and retry. Key artifacts completely; sign/validate caches; isolate tenants; encrypt/minimize genomic tensors; control dumps/traces/spills and retention/erasure. Bound compilation, memory, runtime, and retries; attribute failures; provide CPU/unfused fallback, canary, monitoring, and rollback. Named genomics, bioinformatics/statistics, clinical/laboratory where applicable, numerical, GPU/compiler, software-safety, security/privacy, operations/SRE, quality/regulatory, human-factors, and independent validation reviewers approve validity, bias, limitations, and residual risk. Fusion evidence alone establishes no biological or clinical validity.
