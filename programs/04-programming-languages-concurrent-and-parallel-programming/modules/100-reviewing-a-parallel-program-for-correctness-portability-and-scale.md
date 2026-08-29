---
module_id: CONPAR-100
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 100
title: Reviewing a Parallel Program for Correctness, Portability, and Scale
status: complete
last_verified: 2026-08-29
---

# Reviewing a Parallel Program for Correctness, Portability, and Scale

## One-Page Review

### Governing question

What evidence is sufficient for independent reviewers to decide whether a parallel program implements its stated contract correctly, remains defined and usable across its supported environments, scales for representative workloads, contains failures, and limits every claim to verified scope?

### Essential definitions

- A **review claim** is one falsifiable statement about semantics, correctness, progress, resources, portability, performance, recovery, security, or operation.
- An **assurance case** links claims to arguments, evidence, assumptions, limitations, owners, dates, and decisions.
- A **program contract** specifies inputs, outputs, errors, ordering, consistency, precision, progress, resource and side-effect behavior.
- A **concurrency model** identifies actors, ownership, synchronization, atomicity, memory ordering, cancellation and lifetime.
- A **linearization point** is the abstract instant at which a concurrent operation takes effect when linearizability is the chosen criterion.
- A **progress property** states obstruction-free, lock-free, wait-free, blocking, fairness, bounded-liveness, or deadline behavior under explicit assumptions.
- **semantic portability** preserves defined required behavior across supported language/runtime implementations.
- **build portability** means supported toolchains/targets can build and link; **performance portability** means acceptable efficiency across named systems and metrics, not identical speed.
- A **scaling envelope** is the measured region of inputs, workers, nodes, devices, memory, network and failure conditions for which requirements hold.
- A **negative test** demonstrates that a violated assumption or defect is detected rather than silently accepted.
- A **gate** is an independently decidable requirement with owner, evidence, status and blocking policy.
- A **waiver** is a narrow, risk-owned, time/condition-bounded exception; it is not a passing gate.
- **release evidence** is immutable and traceable to exact source, dependencies, tools, configurations, data and reviewers.
- **residual risk** is risk remaining after controls, stated without converting uncertainty into confidence.

### Central model, mechanism, or theorem

Construct a claim–evidence matrix. For every applicable gate `g`, record requirement, assumptions, implementation surface, positive and negative evidence, environments, result, limitations, owner and reviewer. Release is permitted only if every mandatory gate passes, evidence identity matches the candidate, no blocking result is skipped/unavailable, waivers satisfy policy, and cross-gate contradictions are resolved. Testing demonstrates observed executions; static analysis establishes properties within abstractions; model checking explores a declared model/bound; proof establishes a theorem under assumptions; benchmarks establish measurements within an experimental envelope. These evidence kinds compose only when their interfaces and assumptions align.

### Critical invariants

The candidate source/binary/dependency/configuration identity is immutable; requirements and supported environments are versioned; ownership and shared state are inventoried; memory-model reasoning is language/runtime specific; lifetimes and reclamation are proved; safety, progress and performance claims are separate; numeric acceptance includes precision/reproducibility policy; negative and boundary tests exist; unsupported tool/device/runtime surfaces remain visible; sanitizer/systematic/formal evidence binds to representative code; performance tests preserve correctness and work; portability tests execute outputs, not merely compile; recovery reconciles external effects; security/privacy controls cover telemetry and artifacts; waivers cannot hide failed mandatory evidence; named reviewers are independent enough for risk; and the decision is reproducible from retained artifacts.

### Common failures

Teams review only happy-path code, equate absence of races with correctness, inspect atomics without object lifetime, call a blocking algorithm lock-free, infer portability from one compiler, infer performance portability from one GPU, benchmark different work or wrong output, average away tail/imbalance, treat a sanitizer/model-checker clean run as proof, ignore cancellation/shutdown, leave external effects outside recovery, accept flaky tests by retrying, omit unsupported dependencies, let stale evidence survive code changes, approve vague waivers, publish sensitive traces, or make a release decision with no named accountable reviewer.

### Compact example

A ten-gate matrix has eight passed gates, one blocked recovery gate, and one unavailable required device-portability gate. Even if 80% passed, release is not allowed: gates are logical obligations, not a score. The correct output is a blocked decision naming missing recovery evidence and unavailable target validation.

### Connections

[Designing a Correct Multithreaded Component](020-designing-a-correct-multithreaded-component.md) starts the design contract. [Parallel Performance Models](091-amdahl-gustafson-and-work-span-models.md) scopes scale. [Systematic Concurrency Testing](097-systematic-concurrency-testing.md), [Tracing and Profiling Parallel Execution](098-tracing-and-profiling-parallel-execution.md), and [Failure Containment in Long-Running Parallel Jobs](099-failure-containment-in-long-running-parallel-jobs.md) complete the executable evidence chain. The [program roadmap](../ROADMAP.md) provides the full prerequisite map.

## Governing Question

Can an independent reviewer reconstruct what the program promises, why its synchronization and algorithms satisfy that promise, where the claim is portable, how performance and recovery were measured, which risks remain, and why the exact candidate is or is not releasable?

The capstone review is a decision protocol, not a checklist ceremony. It forces claim granularity, evidence identity, contradiction resolution, and honest stop conditions.

## Why This Matters

Parallel programs fail across boundaries. An algorithm may be logically correct but invoke undefined behavior. A race-free implementation may violate linearizability. A fast kernel may produce wrong floating-point results. A portable API may depend on one vendor's forward-progress or memory-scope behavior. A scalable clean run may fail during shutdown, recovery, oversubscription, or partial device loss.

No single tool spans these concerns. Review must compose specifications, code reasoning, tests, sanitizers, systematic exploration, weak-memory checks, benchmarks, traces, portability matrices, fault injection and operational controls. Each evidence type has a scope and freshness rule.

An elite review makes uncertainty actionable. Missing required evidence blocks; nonapplicable gates have a reason; unavailable targets remain risk; waivers have owners and expiry/removal conditions; and the final decision identifies the exact release candidate.

## Prerequisites and Retrieval

Retrieve the program's complete chain, especially:

- contract, ownership, safety, progress and memory-model reasoning from [Designing a Correct Multithreaded Component](020-designing-a-correct-multithreaded-component.md), [Happens-Before Relations](023-happens-before-relations.md), [Relaxed Atomics](028-relaxed-atomics.md), [Obstruction-Free, Lock-Free, and Wait-Free Progress](051-obstruction-free-lock-free-and-wait-free-progress.md), [Hazard Pointers](055-hazard-pointers.md), and [Epoch-Based Reclamation](056-epoch-based-reclamation.md);
- reproducibility, CPU/GPU/distributed portability and performance from [Reproducible Randomness in Parallel Programs](069-reproducible-randomness-in-parallel-programs.md), [Designing for Replayable Concurrency](070-designing-for-replayable-concurrency.md), [GPU Execution: Grids, Blocks, and Warps](075-gpu-execution-grids-blocks-and-warps.md), [Collective Communication](083-collective-communication.md), [Scaling a Parallel Program Across Multiple Nodes](090-scaling-a-parallel-program-across-multiple-nodes.md), [Roofline and Operational Intensity Analysis](092-roofline-and-operational-intensity-analysis.md), and [Hybrid Threads, SIMD, GPU, and Message Passing](094-hybrid-threads-simd-gpu-and-message-passing.md); and
- final verification from [Race Detection and Concurrency Sanitizers](096-race-detection-and-concurrency-sanitizers.md), [Systematic Concurrency Testing](097-systematic-concurrency-testing.md), [Tracing and Profiling Parallel Execution](098-tracing-and-profiling-parallel-execution.md), and [Failure Containment in Long-Running Parallel Jobs](099-failure-containment-in-long-running-parallel-jobs.md).

Retrieval prompt: identify release/source/binary/dependency/configuration/input digests; requirements and risk classification; supported compilers/runtimes/OS/architectures/devices/topologies/scales; actor/ownership/shared-state graph; invariants, linearization, memory order, lifetime and progress arguments; numeric/work/output oracle; test/static/sanitizer/systematic/weak-memory/formal evidence; performance methodology/results; resource bounds; portability matrix; observability; recovery/fault matrix; security/privacy; operations/runbook; waivers; evidence freshness; named reviewers; decision and residual risks.

## Learning Objectives

After completing this module, a learner can:

1. decompose release assertions into falsifiable review claims and mandatory gates;
2. review contracts, ownership, synchronization, memory order, lifetime and progress together;
3. distinguish testing, sanitization, systematic exploration, static analysis and proof scopes;
4. verify numerical, deterministic, side-effect and resource behavior under concurrency;
5. assess source, semantic, build, runtime, device and performance portability;
6. construct representative strong/weak/scale/oversubscribed/failure experiments;
7. connect traces and models to causal bottlenecks without compromising correctness;
8. evaluate recovery, external effects, security, privacy and operational readiness;
9. enforce evidence identity, freshness, waiver and reviewer independence; and
10. write an auditable approve, reject, or blocked decision with residual risk.

## Core Exposition

### Freeze the candidate and claims

Assign one review identity to source revision, submodules/dependencies, lockfiles, generated code, compiler/linker/runtime, build flags, containers/images, schemas, configuration, deployment descriptors and representative data. Record reproducible build status and binary/image digests. Any correctness-affecting change invalidates dependent evidence unless a documented impact analysis and rerun policy says otherwise.

Translate requirements into claims: output equivalence/tolerance, operation ordering, consistency, progress, maximum resources, cancellation/shutdown, supported targets, scaling threshold, recovery RPO/RTO, side effects, security/privacy and observability. Each claim names assumptions and counterexamples. Avoid “thread-safe,” “portable,” “scalable,” or “fault tolerant” without definitions.

Map claims to gates with stable domain names, not delivery sequence. A gate is `pass`, `fail`, `blocked`, `unavailable`, or `not_applicable` with justification. Missing evidence cannot be averaged away.

### Evaluate a gate matrix

This executable model demonstrates decision logic. It does not review real code or imply that each gate has equal risk. The recovery and required device-portability gates prevent release despite eight passes.

<!-- bijux-verify: {"id":"parallel-review-gate-decision","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"contract=pass evidence=3\nalgorithm=pass evidence=4\nmemory_lifetime=pass evidence=5\nprogress=pass evidence=3\nverification=pass evidence=6\nnumerics=pass evidence=4\nperformance_scale=pass evidence=5\noperations_security=pass evidence=4\nrecovery=blocked evidence=1\ndevice_portability=unavailable evidence=0\npassed=8\nblocking=2\nrelease_allowed=False\n","stderr":""}} -->
```python
gates = [
    ("contract", "pass", 3),
    ("algorithm", "pass", 4),
    ("memory_lifetime", "pass", 5),
    ("progress", "pass", 3),
    ("verification", "pass", 6),
    ("numerics", "pass", 4),
    ("performance_scale", "pass", 5),
    ("operations_security", "pass", 4),
    ("recovery", "blocked", 1),
    ("device_portability", "unavailable", 0),
]
passed = 0
blocking = 0
for name, status, evidence_count in gates:
    print(f"{name}={status} evidence={evidence_count}")
    if status == "pass":
        passed += 1
    else:
        blocking += 1
print(f"passed={passed}")
print(f"blocking={blocking}")
print(f"release_allowed={blocking == 0}")
```

Evidence count is metadata, never a vote. One proved invariant may be stronger than hundreds of shallow tests; one failed mandatory negative test blocks. Gate policy comes from risk and requirements.

### Review the contract and state model

Enumerate operations, inputs, outputs, errors, partial results, ordering and consistency. Define behavior during concurrent calls, duplicate calls, cancellation, timeout, shutdown, resource exhaustion and failure. Specify which callbacks may reenter and on which executor. Document exception/panic propagation and whether destructors/finalizers may block.

Build an ownership graph: state/object, creator, readers/writers, synchronization, lifetime owner, publication path, reclamation, external resource and mutation invariant. Include caches, statistics, logging, allocators, signal handlers, device buffers, MPI requests and foreign libraries. Hidden shared state is a review defect.

Write the abstract sequential or concurrent specification. For objects claiming linearizability, identify candidate linearization points and histories; for reductions/batch pipelines, define legal partial orders and numerical equivalence. Prove representation invariants from initialization through every transition, including failure exits.

### Review memory and lifetime semantics

Choose the normative language/runtime/device specifications for the candidate versions. For every shared non-atomic access, show a happens-before path or confinement/immutability. For atomics, state object, operation, memory order, scope and synchronization relation; explain why weaker orders admit no forbidden observation. Do not infer semantics from one architecture's assembly.

Review publication, compound invariants, ABA, reference counts, hazard/epoch/quiescent reclamation, allocator reuse, cancellation and teardown. Memory safety and race freedom differ from abstract correctness. Safe-language code can still deadlock, race logically, leak resources or misuse unsafe/FFI code.

At host/device/process boundaries, verify visibility and lifetime: transfer/event completion, stream dependencies, unified-memory rules, MPI buffer/request completion, RMA epochs, NIC/device DMA and foreign ownership. Audit every unsafe, raw-pointer, assembly, intrinsic and FFI boundary with explicit pre/postconditions.

### Review progress and resource bounds

State whether operations block and under what scheduler/runtime/fairness assumptions. Lock-free system progress does not guarantee per-thread completion; wait-free claims need a bounded-step argument. Locks require order, contention, priority inversion and condition-predicate review. Async tasks require executor availability and structured cancellation.

Bound threads/tasks, queues, retries, recursion, allocations, temporary buffers, logs/traces, messages/requests, device memory, streams/events, checkpoint space and file descriptors. Backpressure must reach producers without deadlock. Test overload and resource exhaustion; graceful degradation must preserve correctness.

Review termination, shutdown and partial initialization as first-class protocols. Every spawned operation is joined, cancelled or deliberately detached with owned lifetime. Cleanup is idempotent and cannot race use.

### Review algorithm and numerics

Check partition coverage/nonoverlap, loop bounds, dependency DAGs, reductions/scans, convergence, work queues, load balance and termination detection. Prove conservation, uniqueness, monotonicity or domain invariants. Test empty, singleton, uneven, maximum, adversarial and malformed inputs.

Floating-point parallel reductions change order. Specify precision, reproducibility and tolerance by output/domain; justify error bounds and stable algorithms. Test NaN, infinities, subnormals, overflow/underflow, cancellation and condition numbers where relevant. A performance optimization cannot reduce work/precision silently.

Randomized programs bind algorithm, seed, stream derivation and logical work identity so worker-count or scheduling changes have the declared effect. Statistical validation uses independent references and uncertainty, not one seed.

### Compose verification evidence

Unit and property tests cover functional partitions and oracles. Negative tests prove invalid input, stale epoch, duplicate completion, overflow and invariant violations are detected. Stress tests sample natural runtime behavior. Sanitizers dynamically observe supported races/memory/UB/device hazards in executed coverage.

Systematic testing controls schedules/faults within declared bounds and preserves replay. Weak-memory checking targets legal behaviors beyond sequential consistency. Static analysis and compiler warnings cover specific abstractions. Formal models/proofs establish stated properties under assumptions; refine or trace mapping back to implementation. Fuzz inputs and protocols separately.

Maintain a coverage ledger: requirement→evidence, code/build/target scope, positive/negative cases, tool/version/options, passes/failures/skips/timeouts/unavailable, artifacts, limitations and reviewer. A clean result with setup abort, unsupported module or stale digest is not passing.

Triangulate high-risk claims with independent methods: memory-order reasoning plus weak-memory model checking plus targeted tests; lifetime proof plus sanitizer churn; deadlock order proof plus systematic cycles; numerical error analysis plus independent recomputation. Agreement strengthens confidence only when methods do not share the same blind spot.

### Review portability

Define the support matrix by language/ABI, compiler/version, runtime/library, OS/kernel, CPU architecture/features/endian/alignment, accelerator/vendor/driver, MPI implementation, filesystem/network, process/thread count and build mode. Distinguish required, best-effort and unsupported cells.

Compile with strict warnings, but also execute semantic conformance/litmus, functional and representative integration tests. Detect optional features at configure/runtime and fail clearly or choose validated fallback. Do not branch on vendor strings when capability queries exist. Validate integer widths, serialization, alignment, atomics, clocks and filesystem behavior.

Performance portability requires a threshold/metric per named target—such as fraction of a reviewed baseline, throughput per resource, or bounded slowdown—plus correct outputs. One source implementation may require target-specific variants; keep dispatch and fallback correct, tested and observable. Never promise automatic identical performance across architectures.

### Review scale and performance

Define workload classes and resource envelope. Measure one worker, representative concurrency, saturation, oversubscription, multiple NUMA domains, GPUs, nodes, weak/strong scaling and failure/recovery. Record exact candidate/topology/affinity/frequency/input/tool configuration, warm-up, repetitions, raw values and uncertainty.

Check work and span, serial fraction, load imbalance, granularity, queue contention, memory bandwidth/operational intensity, communication volume/latency, synchronization, device gaps, transfers and exposed wait. Trace critical paths with semantic correlations. Counts/utilization need correct units and denominators.

Correctness gates run with performance experiments. Verify output/work/item/message digests, precision and failures. Before/after comparisons are equivalent and randomized/interleaved where drift matters. Performance regressions cannot be waived by reducing validation, logging or recovery invisibly.

Capacity planning includes tails, noisy neighbors, allocation delay, checkpoint overhead, telemetry volume, memory fragmentation and growth across long runs. Scaling evidence stops at the measured envelope.

### Review recovery, observability, and operations

Define failure domains, detection/suspicion, containment, checkpoint completeness/consistency, epoch fencing, idempotent external effects, restore validation, retry/escalation and observed RPO/RTO. Inject process/node/device/storage/network/corruption faults and failures during recovery. Preserve the last known-good generation and original evidence.

Logs/metrics/traces have stable run/actor/task/message/device/epoch identity, units, clock uncertainty, sampling/loss and bounded cardinality. Health signals distinguish progress, waiting, overload, failure and observation gaps. Alerts map to owned runbooks; telemetry does not expose secrets, personal data or uncontrolled payloads.

Deployments pin artifacts/configuration, use least privilege and resource limits, expose safe rollback/disable/fallback, and verify compatibility. Operators can drain, cancel and recover without violating invariants. Generated reports are reproducible from raw governed artifacts.

### Review security, privacy, and abuse

Concurrency changes attack surfaces: TOCTOU, duplicate effects, cancellation races, stale authorization, unbounded fan-out, queue/resource exhaustion, speculative or shared-resource leakage, unsafe parsers and trace/context forgery. Threat-model trusted/untrusted boundaries and tenant isolation.

Authenticate commands and propagated context, authorize at effect time, fence old epochs, validate sizes/counts/indices, bound work/memory/logs, redact/minimize/encrypt telemetry/checkpoints, audit access, and define retention/deletion. Use constant-time or isolation requirements where side channels matter; performance evidence cannot weaken them silently.

### Conduct human review and decide

Reviewers need named roles and relevant independence. Require algorithm/domain, concurrency/memory-model/runtime, compiler/toolchain/architecture/device, verification, performance/HPC, reliability/operations, security/privacy, quality/release and any safety/regulatory/human-factors expertise implied by use. No automated artifact claims external review.

Record findings by severity, evidence, owner and closure. A waiver names exact failed/unavailable requirement, risk, compensating controls, approver, expiry/removal trigger and monitoring. Some safety, correctness, privacy or unsupported-target gaps are nonwaivable.

Decision is approve, reject, or blocked. It includes candidate identity, gate table, verification commands/results, supported envelope, waivers, residual risk, reviewers/date and rollout/rollback conditions. Approval says only that defined requirements are met for the reviewed scope.

### High-stakes limits

For medical, transport, energy, finance, emergency or critical infrastructure use, repository evidence does not replace hazard analysis, qualified processes, target/hardware validation, domain trials, regulatory approval or independent assurance. Benchmarks do not establish worst-case deadlines; tests do not prove all executions; formal proofs do not cover unmodeled physics or operations.

Named domain/safety, algorithm/numerics, concurrency/memory-model, compiler/runtime/hardware/device/network, verification, security/privacy, reliability/operations, quality/regulatory/certification, human-factors/accessibility, ethics and independent validation reviewers must approve the applicable assurance case. None is claimed here.

## Definitions and Notation

- `K`: immutable release-candidate identity.
- `C={c_i}`: versioned falsifiable review claims.
- `G={g_j}`: applicable gates and blocking policy.
- `E(g)`: digest-bound evidence, assumptions, environments, results and limitations for gate `g`.
- `S`: supported semantic/build/runtime/device environment matrix.
- `P`: measured performance/scaling envelope.
- `F`: tested failure/recovery envelope.
- `W`: governed waivers with owner, approval and expiry/removal condition.
- `R`: residual risks and unsupported surfaces.
- `D(K,C,G,E,S,P,F,W,R)`: reproducible approve/reject/blocked decision.

## Mechanisms, Invariants, or Proof Structure

### Specification-to-implementation proof

Map each requirement to state/operation ownership, invariants, linearization/ordering, numeric policy, progress/resources, errors and side effects. Review all unsafe/FFI/device/runtime boundaries and failure transitions.

### Evidence-validity proof

Bind every artifact to `K`; validate tools, setup, positive/negative probes, coverage, skips/timeouts/loss, digest freshness and model assumptions. Independently recompute formulas/results and replay counterexamples.

### Portability-and-scale proof

Execute required matrix cells with defined fallbacks and correctness oracles; measure representative scaling/performance with equivalent configurations and uncertainty; stop claims at `S` and `P`.

### Recovery-and-operation proof

Inject faults in `F`; demonstrate containment, consistent state, fenced/idempotent effects, validation, RPO/RTO and bounded escalation; validate telemetry, security/privacy and runbooks.

### Decision proof

Require every mandatory `g` to pass or follow explicit nonwaivable/waiver policy; resolve contradictions; document named reviewers, `W` and `R`; issue one candidate-specific decision reproducible from retained evidence.

## Alternatives and Trade-Offs

| Evidence | Establishes | Principal limitation |
|---|---|---|
| code inspection | intent, invariants and boundary reasoning | human omission; no execution |
| unit/property/fuzz tests | observed input/output properties | schedule/environment/model coverage |
| sanitizers | observed supported dynamic defects | instrumentation and executed paths |
| systematic/weak-memory checking | bounded/model executions | state space and model-code mapping |
| static analysis | properties in tool abstraction | model precision and unsupported code |
| formal proof | theorem under explicit assumptions | specification/refinement/implementation gap |
| conformance matrix | behavior on named targets | finite versions/configurations |
| benchmark/trace | performance/causality in envelope | observer effect, variance, generalization |
| fault injection | observed containment/recovery | finite fault combinations/fidelity |
| external independent review | broader challenge/accountability | scope, expertise and evidence still matter |

## Failure Modes and Misconceptions

- **“Race-free means correct.”** logical ordering, lifetime, progress and specification can still fail.
- **“Correct means production-ready.”** portability, scale, recovery, security and operation remain.
- **“Compile means portable.”** execute semantics and outputs on required targets.
- **“One fast target means performance portable.”** define and test a target matrix.
- **“More tests mean proof.”** coverage and oracle quality matter.
- **“Formal proof covers the binary.”** refinement, compiler/runtime/hardware assumptions must connect.
- **“Safe language means no concurrency bugs.”** deadlock, logical races, leaks and unsafe/FFI remain.
- **“Lock-free means every call finishes.”** distinguish system and per-operation progress.
- **“Atomic fields protect compound invariants.”** composition needs a protocol.
- **“Deterministic output proves deterministic execution.”** hidden state/order may differ.
- **“Tolerance permits wrong work.”** quantify numerical and semantic acceptance.
- **“Average speedup proves scale.”** inspect tails, imbalance, resources and envelope.
- **“Clean sanitizer/systematic runs certify.”** dynamic/model scope remains finite.
- **“Recovery success validates output.”** semantic and external-effect checks remain.
- **“Unavailable equals not applicable.”** required unavailable evidence blocks.
- **“Waiver means pass.”** it records accepted residual risk under policy.
- **“Old evidence remains valid.”** candidate-impact and digest freshness decide.
- **“Automated review is independent human review.”** named humans must actually review.

## Worked Examples

### Example 1

**Gate arithmetic.** Eight of ten gates pass; recovery is blocked and device portability unavailable. **Conclusion:** release is blocked, not 80% approved.

### Example 2

**Atomic queue.** Head/tail are atomic, but reclaimed nodes can be reused before readers finish. **Conclusion:** review lifetime/reclamation with ordering.

### Example 3

**Progress claim.** CAS loop is lock-free globally but one thread can starve. **Conclusion:** do not label it wait-free.

### Example 4

**Portability.** Code compiles on CPU and GPU, but subgroup width assumption corrupts one device. **Conclusion:** semantic boundary tests belong in each matrix cell.

### Example 5

**Numerics.** Faster reduction changes order and exceeds domain tolerance on ill-conditioned input. **Conclusion:** performance requires an output oracle.

### Example 6

**Verification gap.** TSan passes, but device memory and uninstrumented plugin are outside coverage. **Conclusion:** absence claims retain blind spots.

### Example 7

**Scaling.** Strong scaling flattens because span/communication dominate, not because workers are idle accidentally. **Conclusion:** use models and traces to identify the envelope.

### Example 8

**Recovery.** Restart restores memory but duplicates a committed external write. **Conclusion:** checkpoint review includes side-effect reconciliation.

### Example 9

**Stale evidence.** Memory-order code changes after weak-memory tests. Artifact digest mismatch invalidates the gate. **Conclusion:** freshness is part of correctness.

### Example 10

**Radiotherapy planning system.** Review must preserve patient/image/structure/prescription/beam/model/calibration/unit/plan/configuration generations; prove dose/geometry/numeric bounds and concurrency ownership; validate CPU/GPU variants against independent references; bound resources/deadlines; contain failures and duplicate exports; protect clinical data; and maintain traceable human approval. Named radiation oncology/medical physics/dosimetry, numerical algorithm, concurrency/memory-model, compiler/runtime/CPU/GPU, clinical safety/cybersecurity/privacy, operations, quality/regulatory, human-factors/accessibility, ethics and independent validation reviewers must approve it; none is claimed here. **Conclusion:** a passing software review cannot authorize treatment.

## Cross-Program Connections

- **Programming languages/compilers:** normative semantics, UB, optimization, ABI and code generation constrain reasoning.
- **Algorithms/formal methods:** invariants, linearizability, progress, error bounds and proofs form the argument core.
- **Operating systems/runtimes:** scheduling, cancellation, clocks, resources and failure behavior affect liveness.
- **Distributed/cloud systems:** messages, partial failure, consistency, epochs and operations extend boundaries.
- **GPU/HPC:** memory scopes, devices, ranks, topology, operational intensity and scaling define portability/performance.
- **Testing/quality:** coverage, negative tests, artifact identity, gate policy and human review drive decisions.
- **Security/privacy:** concurrency and evidence artifacts introduce abuse and disclosure paths.
- **Data/science:** provenance, numerical validity, reproducibility and independent references protect outputs.
- **Reliability:** recovery consistency, RPO/RTO and fault injection govern long runs.
- **Safety/ethics:** application authority requires domain-specific independent assurance.

## References

1. ISO/IEC JTC 1/SC 22/WG21, *C++ Working Draft N5032*, 2025. <https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/n5032.pdf>
2. Rust Project, *The Rust Reference: Behavior Considered Undefined*, current documentation; retrieved 2026-08-29. <https://doc.rust-lang.org/reference/behavior-considered-undefined.html>
3. Oracle, *Java Language Specification, Java SE 26: Threads and Locks*, current specification; retrieved 2026-08-29. <https://docs.oracle.com/javase/specs/jls/se26/html/jls-17.html>
4. The Open Group and IEEE, *POSIX.1-2024, System Interfaces: General Information*, 2024. <https://pubs.opengroup.org/onlinepubs/9799919799/functions/V2_chap02.html>
5. OpenMP Architecture Review Board, *OpenMP API Specification 6.0*, 2024, with current errata. <https://www.openmp.org/specifications/>
6. MPI Forum, *MPI: A Message-Passing Interface Standard, Version 5.0*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report.pdf>
7. NVIDIA, *CUDA Programming Guide*, current documentation; retrieved 2026-08-29. <https://docs.nvidia.com/cuda/cuda-programming-guide/index.html>
8. Khronos Group, *SYCL 2020 Specification, Revision 11*, current specification; retrieved 2026-08-29. <https://registry.khronos.org/SYCL/specs/sycl-2020/pdf/sycl-2020.pdf>
9. Maurice P. Herlihy and Jeannette M. Wing, “Linearizability: A Correctness Condition for Concurrent Objects,” ACM TOPLAS, 1990. <https://www.cs.cmu.edu/~wing/publications/HerlihyWing90.pdf>
10. Mark D. Hill and Michael R. Marty, “Amdahl's Law in the Multicore Era,” *Computer*, 2008. <https://research.cs.wisc.edu/multifacet/amdahl/>

## Exercises

### Exercise 1

Construct a release gate table for a concurrent bounded queue covering contract, memory/lifetime, progress, verification, numerics/data, portability, performance/resources, recovery, security/operations and review. Define blocking rules and evidence freshness.

### Exercise 2

Review a lock-free stack using relaxed atomics and epoch reclamation. State abstract specification, linearization, ordering, progress and reclamation obligations plus independent evidence.

### Exercise 3

Design a CPU/GPU/MPI portability and scaling matrix for a parallel reduction. Include numeric tolerance, work/output equivalence, target capabilities, weak/strong scaling, traces, unsupported cells and decision thresholds.

### Exercise 4

A candidate has passed unit/sanitizer tests, unavailable weak-memory hardware, a flaky recovery test, 12% speedup with changed floating-point results, and an expiring security waiver. Issue a decision and closure plan.

### Exercise 5

Apply the full review protocol to concurrent autonomous-drone route deconfliction. Specify correctness, memory/progress, numeric/geospatial, portability/scale, verification, recovery, security/privacy, operations and named human review requirements without claiming flight authorization.

## Answers to the Exercises

### Answer 1

Give each gate requirement, owner/reviewer, candidate digest, environments, positive/negative evidence, result and limitation. Contract: FIFO/capacity/close/cancel/error semantics and linearizable histories. Memory/lifetime: ownership, HB, ABA/reclamation, shutdown. Progress: blocking/fairness/bounds. Verification: unit/property/stress/sanitizer/systematic/weak-memory with skips visible. Data: item identity/conservation. Portability: required compiler/runtime/architecture cells execute. Performance/resources: throughput/latency/memory under representative load with output checks. Recovery: restart/epoch/effects if applicable. Security/operations: untrusted sizes, exhaustion, telemetry/runbooks. Review: named accountable roles. Mandatory failed/blocked/unavailable gates block; `not_applicable` requires requirement-based justification; waivers follow explicit nonwaivable policy and expiry. Any code/dependency/compiler/configuration change invalidates affected evidence through digest/impact rules; periodic/tool-current evidence also expires by policy.

### Answer 2

Specify sequential push/pop/empty results and histories; identify successful top CAS as candidate linearization while accounting for empty reads and retries. Prove initialization before release publication and acquire/appropriate reads before dereference; justify every relaxed operation and failure order in the language model. Claim lock-free only with a system-progress argument; do not claim starvation freedom. Epoch proof shows a node retired in epoch `e` cannot be reclaimed until all possible readers have left/quiesced beyond it; handle stalled threads, nesting, thread exit, generation/ABA, allocator reuse and shutdown. Evidence includes line-by-line memory/lifetime proof, linearizability model/history tests, language-aware weak-memory checking, systematic schedules, sanitizer churn, allocation reuse/empty/singleton/contention/cancel tests, architecture/compiler matrix and known-bug negative probes. Bind all evidence to the candidate and retain model/tool limitations.

### Answer 3

Define reference reduction and absolute/relative/ULP or domain tolerance, NaN/Inf policy, deterministic/reproducible modes, item/work conservation and independent high-precision cases. Matrix CPU compilers/architectures/SIMD widths, GPU vendors/models/drivers/subgroup sizes and MPI implementations/rank counts/networks; query capabilities and test fallbacks. Execute empty/single/uneven/large/ill-conditioned inputs in each required cell. Measure one worker, threads, devices, ranks, strong and weak scaling, NUMA/oversubscription and multi-node, retaining topology/affinity/frequency/repetitions/raw uncertainty. Trace load balance, reduction tree, transfers/collectives and critical path; apply work/span/roofline models. Required unsupported/unavailable cells block unless product support changes or governed waiver applies. Thresholds combine correctness first, then per-target performance baseline/fraction, resource ceilings and scaling envelope; no result generalizes outside tested cells.

### Answer 4

Decision: blocked/reject, not approve. Unit/sanitizer evidence is useful but cannot replace required weak-memory scope. Classify hardware as unavailable only after alternatives (appropriate model checker/emulator/target lab) and keep the required gate blocking. A flaky recovery test is a failure until its root cause is fixed and repeated fault/replay evidence passes; retries cannot relabel it. The 12% speedup is invalid until changed results meet predeclared numeric/domain tolerance and identical-work requirements; otherwise restore correctness or redesign the contract with independent approval. Inspect the security waiver's exact risk, controls, approver and expiry; close it or renew under policy before expiry, and block if nonwaivable. Rerun all affected evidence on one frozen candidate, then obtain named reviewers and issue a new decision with residual risks.

### Answer 5

Contract uniquely identifies drone/mission/route/airspace/geofence/weather/map/model/configuration/operator and command epochs; deconfliction forbids separation violations, stale/duplicate commands and unauthorized routes with bounded safe fallback. Review ownership, atomics/locks/channels, task cancellation, sensor/map lifetime, linearization and progress/deadline assumptions; validate geodesy/units/coordinate frames, uncertainty, numeric tolerances and independent conflict oracle. Test CPU/edge accelerator/radio/runtime variants, fleet size, density, degraded compute/network and resource bounds. Compose property/fuzz/sanitizer/systematic/weak-memory tests, simulation and hardware-in-loop with negative conflicts; preserve causal traces. Inject process/device/network/GNSS/map/storage faults and recovery during effects; fence epochs and reconcile issued commands. Authenticate/authorize commands/context, isolate fleets/tenants, protect location/operator data, bound fan-out/logs and audit. Runbooks cover loss of link, overload, safe landing/hold and human override. Named aviation/airspace and autonomous-flight safety, robotics/control/geospatial/weather, concurrency/memory-model/runtime, compiler/hardware/accelerator/radio, verification, cybersecurity/privacy, reliability/operations, quality/regulatory/certification, human-factors/accessibility, ethics and independent validation reviewers must approve. No external review, airworthiness, regulatory approval or flight authorization is claimed.
