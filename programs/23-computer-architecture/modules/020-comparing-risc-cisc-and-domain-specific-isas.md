---
module_id: CA-020
program: Computer Architecture
level: 1
module_number: 20
title: Comparing RISC, CISC, and Domain-Specific ISAs
status: complete
last_verified: 2026-09-04
---

# Comparing RISC, CISC, and Domain-Specific ISAs

## One-Page Review

### Governing question

How can architects compare RISC, CISC and domain-specific instruction sets using explicit contracts, workloads and evidence instead of labels, stereotypes or one implementation’s benchmark result?

### Essential definitions

- **RISC** describes an ISA/design tradition emphasizing regular operations, explicit load/store data movement and implementation-friendly encodings, not a single formal feature checklist.
- **CISC** describes an ISA/design tradition with richer or more varied instruction forms and often variable-length encodings, not necessarily slow or microcoded execution.
- A **domain-specific ISA** (DSA ISA) exposes operations and data types tailored to a workload domain such as tensor, signal, graphics or cryptographic computation.
- **instruction semantic complexity** is the amount of architectural work and exceptional behavior one instruction specifies.
- **encoding regularity** measures how consistently fields, lengths and operand forms are represented.
- **code density** is useful work represented per instruction byte under a defined workload/toolchain.
- **micro-operation translation** converts architectural instructions into implementation-internal operations.
- **microcode** is implementation control storage/sequencing used for selected operations; it is not synonymous with CISC.
- **architectural state** is software-visible state; specialized accumulators, matrices or queues can enlarge it.
- **programmability** captures how effectively software, compilers and tools can express and debug intended algorithms.
- **domain coverage** is the set of important workload operations efficiently represented by a specialized ISA.
- **fallback path** executes unsupported or uncommon work using a host/general processor, library or emulation.
- **arithmetic intensity** is operations performed per byte transferred at a defined memory boundary.
- **total cost of ownership** includes development, verification, silicon, software, deployment, compatibility and maintenance costs.
- A **workload-weighted comparison** aggregates named metrics only after fixing workload mix, constraints and normalization.

### Central model, mechanism, or theorem

There is no context-free ordering `RISC > CISC > DSA` or its reverse. Compare candidate `a` under workload/environment `W` with a vector

`Q(a,W) = (correctness coverage, latency, throughput, energy, code size, area, tool maturity, compatibility, assurance cost)`.

Any scalar score `Score(a,W)=sum_j weight_j * normalized_metric_j(a,W)` embeds stakeholder values and workload assumptions. Report the vector and sensitivity analysis, not only the aggregate. ISA properties, microarchitecture, process, compiler and system integration must be controlled or attributed separately.

### Critical invariants

- Labels never substitute for an inventory of encodings, operands, state, memory and exception semantics.
- Comparisons use equivalent defined work, quality, precision and security requirements.
- ISA effects are separated from the selected microarchitecture, process and clock.
- Code density, instruction count, cycles and energy are reported as different metrics.
- Domain-specific speedups include host transfer, fallback, synchronization and utilization costs.
- Compiler maturity and generated-code quality are part of the tested configuration.
- Compatibility and verification burdens cover extensions, legacy behavior and exceptional cases.
- Conclusions remain scoped to measured workload mix and sensitivity assumptions.

### Common failures

Frequent failures are defining RISC as “few instructions,” defining CISC as “slow,” assuming fixed-length decode guarantees high frequency, attributing modern x86 micro-ops to the ISA contract, calling every accelerator a new ISA, comparing instruction counts across unequal semantic work, ignoring code size and fetch bandwidth, quoting peak tensor throughput for sparse or transfer-bound work, omitting precision differences, excluding fallback and host orchestration, comparing mature compilers with prototype backends, ignoring compatibility costs, and turning a workload-specific result into a universal ranking.

### Compact example

Suppose synthetic normalized cost estimates cover control, systems and tensor kernels. Under weights `(0.5,0.4,0.1)`, a general-purpose design can win because control and systems dominate. Under `(0.1,0.1,0.8)`, a tensor-specific design can win because specialized arithmetic dominates. The reversal does not prove either architecture universally superior; it proves the decision depends on workload mix and metric assumptions that must be exposed.

### Connections

ISA comparison connects encoding, datapaths, compilers, caches, accelerators, numerical formats, benchmarking, security, compatibility, economics and systems engineering.

## Governing Question

RISC and CISC began as useful descriptions of design tendencies. Modern systems blur them: a regular ISA can acquire many extensions, a variable-length ISA can decode into regular micro-operations, and domain accelerators can sit behind a host command interface.

The governing question is therefore not which label wins. It is which explicit architectural contract and implementation ecosystem best satisfies a named workload, lifecycle and assurance case.

## Why This Matters

Architecture choices persist for decades. Encodings, binaries, compiler targets and operating-system support create compatibility obligations long after the first processor is replaced.

Benchmarks can mislead if they compare different precision, algorithms, libraries or system boundaries. A DSA may accelerate a kernel by 100× while the application improves little because transfer or preprocessing dominates.

Correct comparison supports transparent decisions. It identifies whether a result comes from ISA expressiveness, implementation resources, software maturity, process technology or changed requirements.

## Prerequisites and Retrieval

Before studying this module, be able to:

- distinguish ISA from microarchitecture and ABI;
- interpret instruction encoding, operands and exceptions;
- compute latency, throughput, code-size and energy metrics;
- apply Amdahl’s law and arithmetic-intensity reasoning;
- identify benchmark configuration and confounding variables.

Retrieve each ISA/profile/version; instruction lengths and formats; operand/memory models; architectural state; exception/privilege model; extensions; implementation microarchitecture; process/frequency; caches/memory; accelerator host interface; supported types/precision; compiler/backend/library versions and flags; binary size; dynamic instruction/micro-operation counts; latency/throughput; energy/power; area; transfer/synchronization time; workload inputs and quality criteria; fallback behavior; security controls; virtualization/debug; conformance and formal evidence; compatibility horizon; licensing/standards governance; silicon errata; and lifecycle cost assumptions.

## Learning Objectives

After completing this module, you should be able to:

1. describe RISC, CISC and domain-specific tendencies without treating them as rigid taxonomies;
2. separate ISA properties from microarchitectural implementation choices;
3. compare encoding, operand, state and exception complexity;
4. measure instruction count, code density, cycles, throughput and energy independently;
5. analyze domain-specific coverage, utilization, transfers and fallback;
6. control compiler, precision, process and system-boundary confounders;
7. apply workload weighting, Amdahl’s law and sensitivity analysis;
8. assess compatibility, programmability, security and verification cost;
9. construct reproducible benchmark and evidence packages;
10. make scoped architecture recommendations with explicit uncertainty.

## Core Exposition

### Treat labels as hypotheses

Use RISC, CISC and DSA to form questions, not answers. Ask about field regularity, instruction lengths, memory operands, specialized state and semantic work.

Two ISAs under one label can differ more than two across labels. Record the actual profile and extensions.

### Compare architectural contracts

Inventory state, operations, operands, memory effects, exceptions, privilege and ordering. This contract determines what binaries may assume.

Do not infer pipeline stages, caches or execution units from the instruction manual unless those features are architectural.

### Characterize RISC tendencies

RISC traditions often use load/store arithmetic, many registers, regular formats and simple common operations. These choices can ease parallel decode and compiler scheduling.

Modern RISC ISAs include atomics, vectors, compressed forms and privileged features. “Reduced” does not mean tiny or one-cycle.

### Characterize CISC tendencies

CISC traditions often expose variable lengths, multiple operand forms, memory operands and semantically rich operations. They can provide dense binaries and strong legacy compatibility.

Modern implementations may translate complex instructions into internal operations, cache decoded forms and execute out of order. The architectural instruction is still the compatibility unit.

### Characterize domain-specific ISAs

A DSA ISA exposes domain types and operations: matrix multiply, convolution, butterfly, finite-field or packet-processing primitives. It can reduce control/data-movement overhead.

Specialization narrows coverage and raises software/integration dependence. Unsupported shapes, sparsity or precision may fall back or underutilize hardware.

### Distinguish an accelerator interface

Some accelerators have a true programmable instruction stream; others expose command queues, kernels or fixed-function registers. Both can be useful but have different architectural contracts.

Name host-visible commands, device-local instructions and compiler IR separately. “ISA” should not blur those boundaries.

### Compare instruction length

Fixed length simplifies boundary discovery and field extraction. Compressed subsets can regain density while preserving a regular base.

Variable length improves common-case density and operand flexibility but needs predecode/boundary machinery. Implementation techniques can hide much of this cost.

### Compare operand models

Load/store ISAs make memory traffic explicit. Register-memory instructions can combine address generation, memory access and arithmetic.

Fewer architectural instructions do not imply less internal work. Compare memory transactions, micro-operations, dependencies and exceptions.

### Compare semantic complexity

Count architectural effects: inputs, outputs, memory locations, fault points, progress state and ordering. One string/tensor instruction can specify many operations.

Rich semantics reduce fetch/dispatch overhead but can complicate restart and verification. Implementations may iterate internally.

### Compare decode complexity

Measure critical delay, energy, area and throughput of the actual decode design. Field regularity is only one contributor.

Micro-op caches, instruction buffers and parallel decoders change costs. Do not use format diagrams as timing evidence.

### Compare code density

Measure text bytes for equivalent programs using controlled compilers and link settings. Separate static binary size from dynamic fetched bytes.

Libraries, alignment, literal pools and relaxation affect results. Dense code can improve instruction-cache/TLB behavior even if decode is complex.

### Compare dynamic instruction count

Count retired architectural instructions for equivalent defined work. Also record micro-operations, vector active elements and accelerator commands where relevant.

Instruction counts across different semantic granularity are not directly proportional to time or energy.

### Compare CPI and frequency

Execution time is related to instruction count, cycles per instruction and clock period, but averages hide overlap and stalls.

Frequency depends on microarchitecture, physical design and process. It is not an intrinsic RISC/CISC property.

### Compare front-end bandwidth

Fetch bytes, instruction boundaries, decode width, branch prediction and instruction-cache misses constrain supply.

Dense complex instructions can reduce byte demand; regular wide encodings can simplify parallel decode. Measure the actual workload/frontend.

### Compare backend work

After decode, execution depends on internal operations, ports, dependency chains and memory traffic. Different ISAs can map similar algorithms to similar datapaths.

Special instructions can fuse work and reduce intermediate register traffic. Their benefit depends on throughput and utilization.

### Compare memory behavior

Record bytes transferred at cache levels and external memory, locality, alignment and synchronization. Many workloads are memory-bound regardless of ISA label.

DSAs often use scratchpads, tiling and compressed dataflows. Include host-device and off-chip movement.

### Apply arithmetic intensity

Arithmetic intensity relates operations to bytes at a named memory boundary. Roofline reasoning bounds performance by compute peak or bandwidth.

Changing the boundary changes intensity. On-chip reuse can look excellent while host transfer dominates the application.

### Apply Amdahl’s law

If fraction `p` is accelerated by factor `s`, ideal total speedup is `1/((1-p)+p/s)`. Even infinite kernel acceleration is bounded by unaccelerated work.

Include orchestration, conversion, transfers and fallback in `1-p`. Measure rather than assume `p`.

### Compare energy

Measure energy per completed equivalent task and break down compute, memory, front-end and transfer. Power alone does not equal efficiency.

Specialization can remove instruction overhead and exploit local data reuse. Idle/leakage and host energy can erase gains at low utilization.

### Compare area and opportunity cost

Report silicon area, memory capacity, interfaces and utilization. Specialized units displace cache, cores or other accelerators.

Compare at equivalent process and design targets where possible. Otherwise attribute process/node differences explicitly.

### Control numerical precision

DSAs may gain throughput using reduced precision, saturation, approximate functions or sparsity. Compare output quality and numerical contract.

A faster 8-bit result is not equivalent to a required 32-bit result unless application criteria accept the difference.

### Compare programmability

Assess compiler coverage, diagnostics, libraries, debuggers, profilers, simulators and deployment tools. Manual kernel effort is a real cost.

General ISAs often have mature ecosystems. DSAs can be productive when high-level compilers/libraries cover the domain well.

### Compare compiler quality

Use supported versions and tune fairly. Inspect generated instructions, spills, vectorization, layout and library selection.

A weak prototype backend measures software immaturity as much as ISA potential. Report that honestly rather than hand-optimizing only one candidate.

### Use intermediate representations

Layered IRs can preserve tensor, vector or target-neutral structure until appropriate lowering. Early scalarization loses domain information.

IR extensibility supports multiple DSAs but introduces legality and conversion boundaries that need verification.

### Compare fallback paths

Real workloads include unsupported operators, shapes or data types. Measure fallback execution, data conversion and synchronization.

One fallback can force round-trip transfers and destroy pipeline overlap. Coverage percentage by operator count is weaker than weighted execution coverage.

### Compare exceptions and restart

General CPUs often require precise per-instruction exceptions for OS integration. Long vector/domain operations may use progress state or command completion errors.

Compare the actual software recovery contract. A fast operation that cannot contain faults may be unsuitable for multiprogrammed or safety-critical systems.

### Compare privilege and isolation

General ISAs provide mature privilege, translation and virtualization. DSAs need address isolation, command validation, context separation and reset.

Shared accelerators can leak data through local memory, queues or timing. Include IOMMU and firmware trust boundaries.

### Compare compatibility

Mature CISC families often carry large legacy binary obligations; RISC profiles and extensions also accumulate compatibility. DSAs may version rapidly.

Compatibility enables ecosystem value but constrains encoding/state evolution. Quantify binaries, OSes, tooling and field lifetime that must remain supported.

### Compare extension governance

Open standards, vendor extensions and custom spaces differ in allocation, discovery, review and long-term stewardship.

An extension is not deployable when assembler, compiler, OS context, virtualization and fallback are missing. Count ecosystem completion.

### Compare verification burden

Regular formats can ease decode proofs; rich instructions enlarge semantic/fault cases; DSAs create large data/configuration spaces.

Verification cost depends on specification quality, models, generators and reuse—not label alone. Include negative/exception and composition testing.

### Compare security surfaces

Variable decoders, microcode, speculative state, accelerator firmware, shared memories and command parsers create different attack surfaces.

Use a threat model. Simplicity in one layer can shift complexity into compiler, firmware or host runtime.

### Design fair workloads

Use representative inputs, sizes and mixes; include cold/warm states and latency/throughput modes. Prevent dead-code elimination and validate outputs.

Microbenchmarks explain mechanisms but do not replace application/system measurements.

### Normalize comparisons

Normalize each metric with direction and reference: lower latency/energy/bytes is better, higher coverage/tool maturity may be better. Publish raw values too.

Weights express priorities. Run sensitivity analysis over plausible weights rather than hiding decisions in one score.

### Report uncertainty

Repeat measurements, report distributions and control thermal/frequency state. Model projections carry parameter uncertainty and validation limits.

Avoid false precision in lifecycle cost or future compiler quality. Scenario ranges are more honest.

### Make scoped recommendations

State: for workload set, precision, platform, time horizon and constraints, candidate A is preferred because of named evidence.

List conditions that reverse the decision. Architecture selection is a governed trade, not a universal taxonomy contest.

### Govern lifecycle evidence

Bind ISA/profile, implementation, process, firmware, compiler, libraries, flags, binaries, data, measurement tools and environment. Preserve raw outputs.

Track security advisories and silicon errata. Re-run when workload mix, software maturity or implementation changes materially.

## Definitions and Notation

- `a`: candidate architecture plus specified implementation/software stack.
- `W`: workload set, inputs, quality rules and execution environment.
- `Q(a,W)`: vector of scoped comparison metrics.
- `m_j`: raw metric `j` with unit and preferred direction.
- `n_j(a,W)`: declared normalization of metric `j`.
- `w_j`: stakeholder weight for metric `j`, with documented scale.
- `Score(a,W)`: weighted aggregate used only with raw vector/sensitivity.
- `IC`: retired architectural instruction count.
- `uops`: implementation-internal operation count where observable.
- `CPI`: cycles divided by retired architectural instructions under a named workload.
- `T`: end-to-end elapsed time.
- `E`: energy per completed equivalent task.
- `D`: static/dynamic instruction bytes under a named boundary.
- `p`: accelerated fraction in Amdahl analysis.
- `s`: speedup of that fraction.
- `AI`: arithmetic intensity at a named memory boundary.

Synthetic scores in this module illustrate decision sensitivity; they are not measurements of real ISAs.

## Mechanisms, Invariants, or Proof Structure

1. **Contract obligation:** enumerate actual encoding, state, operand, memory, exception and privilege properties instead of relying on labels.
2. **Equivalence obligation:** prove compared executions perform equivalent defined work with accepted output quality/precision.
3. **Boundary obligation:** define whether measurements cover kernel, process, device, host-device or full application/system.
4. **Attribution obligation:** separate ISA, microarchitecture, process, memory, compiler and library contributions where claims require it.
5. **Workload obligation:** justify input sizes, mixes, warm/cold state and representativeness.
6. **Metric obligation:** report raw units for time, throughput, energy, bytes, area, quality and cost before normalization.
7. **Software obligation:** record compiler/backend/library maturity, flags and generated-code inspection.
8. **Specialization obligation:** include supported-domain coverage, utilization, precision, transfer, synchronization and fallback.
9. **Performance obligation:** include frontend, backend, memory and bottleneck evidence rather than instruction count alone.
10. **Compatibility obligation:** quantify binary, OS, tooling, standards and lifecycle constraints.
11. **Assurance obligation:** compare specification, conformance, formal, exception, security and safety evidence burdens.
12. **Normalization obligation:** publish direction, reference, weights and aggregation formula for any scalar score.
13. **Sensitivity obligation:** identify plausible changes in weights/workloads/parameters that reverse the decision.
14. **Reproducibility obligation:** preserve configurations, binaries, data, tools, raw observations and uncertainty.
15. **Lifecycle obligation:** revalidate conclusions after material ISA, implementation, compiler, workload or errata change.

## Alternatives and Trade-Offs

1. **Regular versus varied encoding:** regularity eases decode; variety improves density/operand reach.
2. **Load/store versus memory operands:** explicit transfers simplify dataflow; memory operands reduce architectural instructions.
3. **Simple versus rich semantics:** simple operations compose flexibly; rich operations reduce dispatch/intermediate traffic.
4. **Fixed versus variable length:** fixed length simplifies boundaries; variable length improves density.
5. **General versus specialized state:** general registers fit broad code; domain state accelerates structured work.
6. **Compiler sequences versus fused instructions:** sequences expose scheduling; fusion reduces overhead and movement.
7. **Hardware versus microcode sequencing:** hardware offers throughput; microcode provides compact flexible implementation.
8. **Backward compatibility versus clean design:** compatibility preserves ecosystem value; clean breaks remove legacy constraints.
9. **Broad coverage versus peak efficiency:** broad ISAs handle diversity; DSAs excel inside a narrower envelope.
10. **Precise exceptions versus coarse command failure:** precision aids OS recovery; coarse completion reduces accelerator control cost.
11. **Mature ecosystem versus rapid specialization:** maturity lowers deployment risk; specialization can deliver large domain gains.
12. **High precision versus reduced precision:** high precision broadens correctness; reduced precision raises throughput/energy efficiency.
13. **Transparent caches versus explicit scratchpads:** caches ease programming; scratchpads provide predictable reuse/control.
14. **Open standard versus proprietary control:** standards improve portability/governance; proprietary designs can move quickly.
15. **Single score versus Pareto comparison:** a score simplifies choice; Pareto vectors expose real stakeholder trade-offs.

## Failure Modes and Misconceptions

1. “RISC means few instructions.” Modern profiles can be extensive.
2. “Every RISC instruction takes one cycle.” Latency is microarchitectural and operation-dependent.
3. “CISC means slow.” Modern implementations decode/execute complex ISAs aggressively.
4. “CISC always uses microcode.” Many operations use hardwired fast paths.
5. “Microcode is architecturally visible.” It is normally implementation control.
6. “Fixed length guarantees simple fast decode.” Width, extensions and implementation matter.
7. “Variable length always loses energy.” Density can reduce fetch/cache energy.
8. “Fewer instructions means less work.” Semantic granularity and internal operations differ.
9. “More registers always improve performance.” Encoding, context and implementation costs trade off.
10. “Load/store always transfers more memory.” Register spills and optimization determine traffic.
11. “A specialized unit automatically has an ISA.” It may expose only commands or fixed functions.
12. “A DSA’s peak operations predict application speed.” Utilization and bottlenecks dominate.
13. “Kernel speedup equals end-to-end speedup.” Amdahl and transfers limit it.
14. “Operator coverage percentage measures workload coverage.” Frequency/time weighting matters.
15. “Reduced precision results are directly comparable.” Output quality must meet the same requirement.
16. “Instruction count predicts energy.” Memory, frontend, execution and leakage contribute separately.
17. “CPI compares unrelated ISAs directly.” Instruction semantics differ.
18. “Higher frequency proves a better ISA.” Process/physical/microarchitecture determine frequency.
19. “One compiler is a neutral measurement instrument.” Backend maturity and flags affect results.
20. “Hand tuning one candidate is fair.” Optimization effort must be controlled or disclosed.
21. “Legacy support is pure waste.” It can carry substantial ecosystem value.
22. “Open ISA guarantees open implementations/tools.” Licensing/governance layers differ.
23. “Simple ISA means simple system.” Complexity can move into compiler, firmware or runtime.
24. “One benchmark suite proves universal superiority.” Workload mixes and constraints differ.
25. “A weighted score is objective.” Normalization and weights encode preferences.
26. “Current results remain true after software changes.” Compilers, libraries and workloads evolve.

## Worked Examples

### Example 1

A fixed 32-bit load/store instruction and a variable-length register-memory instruction can perform different semantic work; compare bytes, memory events and internal operations separately.

### Example 2

If a dense binary fetches 25% fewer instruction bytes but decodes into equal backend work, its benefit may appear mainly in frontend-limited workloads.

### Example 3

A matrix instruction specifying thousands of multiply-accumulates can retire as one instruction yet occupy an array for many cycles.

### Example 4

With accelerated fraction `p=0.9` and kernel speedup `s=100`, ideal end-to-end speedup is about `1/(0.1+0.009)=9.17`, not 100.

### Example 5

A tensor engine’s 8-bit result is not equivalent to a 32-bit CPU baseline until application accuracy/tolerance accepts it.

### Example 6

A DSA supporting 95% of operator names can still cover only 50% of time if one unsupported operator dominates execution and transfers.

### Example 7

A prototype backend spilling domain state may understate ISA potential, but hand-written kernels overstate deployable compiler performance; report both.

### Example 8

An x86 implementation decoding into micro-operations does not make those micro-operations the portable x86 ISA.

### Example 9

A regular ISA plus compressed extension and vectors crosses simplistic RISC stereotypes while retaining a precisely versioned profile.

### Example 10

Synthetic workload weights can select a general design for control-heavy deployment and a DSA for tensor-heavy deployment without contradiction.

## Cross-Program Connections

- **Instruction encoding:** length, formats and semantic density influence frontend design.
- **Datapaths:** internal operations and specialized units implement architectural work.
- **Compilers:** IR preservation, instruction selection and libraries determine realized value.
- **Memory systems:** locality, movement and arithmetic intensity constrain all candidates.
- **Accelerators:** command/ISA boundaries, scratchpads and fallback shape specialization.
- **Numerical computing:** precision and reduction rules determine output equivalence.
- **Security:** decoders, microcode, firmware and shared accelerators expose different surfaces.
- **Verification:** regularity, semantic breadth and configuration spaces shape assurance cost.
- **Economics:** ecosystem maturity, compatibility and engineering effort affect lifecycle value.
- **Systems engineering:** explicit stakeholders, metrics and sensitivity support governed selection.

## References

1. RISC-V International, [RV32I Base Integer Instruction Set](https://docs.riscv.org/reference/isa/unpriv/rv32.html), a regular load/store base ISA and stated design rationale; retrieved 2026-09-04.
2. Arm, [Arm Architecture Reference Manual for A-profile Architecture](https://developer.arm.com/documentation/ddi0487/latest/), contemporary load/store ISA with scalar, SIMD, scalable and system extensions; retrieved 2026-09-04.
3. Intel, [Intel 64 and IA-32 Architectures Software Developer's Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), mature variable-length ISA, legacy compatibility, vector and system semantics; retrieved 2026-09-04.
4. LLVM Project, [Code Generator](https://llvm.org/docs/CodeGenerator.html), compiler target descriptions, legalization, instruction selection, scheduling and register allocation; retrieved 2026-09-04.
5. Norman P. Jouppi et al., [In-Datacenter Performance Analysis of a Tensor Processing Unit](https://arxiv.org/abs/1704.04760), workload-specific architecture, deployment measurements and performance/energy analysis; retrieved 2026-09-04.
6. NVIDIA, [NVDLA Hardware Architecture](https://nvdla.org/hw/v1/hwarch.html), open deep-learning accelerator units, data paths, memory interfaces and operation flow; retrieved 2026-09-04.
7. WebAssembly Community Group, [WebAssembly Core Specification](https://webassembly.github.io/spec/core/), portable typed virtual ISA and execution-environment boundary; retrieved 2026-09-04.
8. LLVM Project, [MLIR](https://mlir.llvm.org/), multi-level intermediate representation infrastructure for preserving and lowering domain structure; retrieved 2026-09-04.

## Exercises

### Exercise 1

Build a comparison table for one RISC, one CISC and one domain-specific ISA covering encoding, operands, state, memory, exceptions, toolchain and compatibility.

### Exercise 2

Compute synthetic workload-weighted costs under a general-purpose and tensor-heavy workload mix and explain why the preferred candidate changes.

### Exercise 3

Design a fair end-to-end benchmark comparing CPU vector code and a tensor accelerator, including precision, transfer and fallback.

### Exercise 4

Apply Amdahl and roofline reasoning to a kernel with measured host fraction, transfer bytes, arithmetic work and memory bandwidth.

### Exercise 5

Construct an architecture-selection assurance case for a ten-year product spanning performance, software, security, compatibility and verification.

## Answers to the Exercises

### Answer 1

Use exact named profiles rather than generic columns. Record instruction lengths, field regularity, register/memory operands, vector/domain state, privilege and faults. Add compiler/library maturity, debug/profile tools, binary/OS ecosystem and extension governance.

For an implementation comparison, separately record process, frequency, frontend, execution units, caches/memory and firmware. No table cell should infer an implementation property solely from the ISA label.

### Answer 2

The synthetic costs below are lower-is-better normalized values, not measurements. The general mix weights control/systems/tensor as `0.5/0.4/0.1`; the tensor mix uses `0.1/0.1/0.8`.

<!-- bijux-verify: {"id":"workload-weighted-isa-comparison","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"general_mix risc=1.400 cisc=1.220 dsa=3.140 preferred=cisc\ntensor_mix risc=4.200 cisc=3.770 dsa=1.020 preferred=dsa\n"}} -->
```python
costs = {
    "risc": {"control": 1.0, "systems": 1.0, "tensor": 5.0},
    "cisc": {"control": 0.9, "systems": 0.8, "tensor": 4.5},
    "dsa": {"control": 3.0, "systems": 4.0, "tensor": 0.4},
}
mixes = {
    "general_mix": {"control": 0.5, "systems": 0.4, "tensor": 0.1},
    "tensor_mix": {"control": 0.1, "systems": 0.1, "tensor": 0.8},
}

for mix_name, weights in mixes.items():
    scores = {
        candidate: sum(weights[k] * values[k] for k in weights)
        for candidate, values in costs.items()
    }
    preferred = min(scores, key=scores.get)
    print(
        f"{mix_name} risc={scores['risc']:.3f} cisc={scores['cisc']:.3f} "
        f"dsa={scores['dsa']:.3f} preferred={preferred}"
    )
```

The reversal demonstrates sensitivity to assumptions. Real selection requires raw measured vectors, justified normalization/weights, uncertainty and noncompensable constraints.

### Answer 3

Freeze model, inputs, batch sizes, output tolerance and precision. Use production-supported compiler/library versions and tune both paths under disclosed effort. Measure kernel and end-to-end latency/throughput, including allocation, format conversion, host-device transfer, synchronization and unsupported-operator fallback.

Record CPU/accelerator utilization, instruction/command counts, memory bytes, power/energy and thermal state. Validate every output and include small/large, sparse/dense and fallback-heavy inputs. Preserve source, IR, binaries, flags, libraries, firmware, data and raw observations.

### Answer 4

Measure accelerated fraction `p` at the full application boundary before acceleration, then use `1/((1-p)+p/s)` as an upper-bound model with measured kernel factor `s`. Add transfer/synchronization to the unaccelerated or explicitly modeled portion.

Compute arithmetic intensity as equivalent operations divided by bytes at the chosen memory boundary. Compare `peak_compute` with `bandwidth*AI`; the smaller bounds kernel throughput. Repeat at host-device and device-memory boundaries. Validate the model against measurements and report deviations/uncertainty.

### Answer 5

Define stakeholders, workloads, output quality, latency/throughput/energy/area constraints, security/safety needs and ten-year compatibility horizon. Compare Pareto vectors before applying disclosed weights. Include compiler/library maturity, fallback, OS/virtualization, diagnostics, supply/licensing and staff skills.

Prototype representative systems and preserve reproducible evidence. Threat-model decoders, firmware and shared devices; estimate conformance/formal/fault-injection burden; plan updates and errata response. Run sensitivity over workload growth, compiler improvement, process, volume and costs. Named architecture, compiler, domain, performance, power, security, safety, verification, operations, finance and independent-assurance reviewers approve their scopes. This module supplies no universal ranking or certification.
