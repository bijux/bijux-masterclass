---
module_id: CONPAR-079
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 79
title: Heterogeneous CPU-GPU Pipelines
status: complete
last_verified: 2026-08-29
---

# Heterogeneous CPU-GPU Pipelines

## One-Page Review

### Governing question

How should CPU work, transfers, GPU kernels, and completion handling be connected so that multiple chunks can overlap safely while ownership, capacity, errors, cancellation, and recovery remain explicit?

### Essential definitions

- A **heterogeneous task DAG** has CPU, transfer, accelerator, and external-I/O tasks connected by data/control dependencies.
- **Submission** records work for later execution; it is not start, completion, visibility, or durable acceptance.
- A **stream/queue** orders commands according to an API contract; different queues require explicit dependencies unless the model infers them.
- An **event** represents completion/status of submitted work and can order consumers without globally blocking unrelated work.
- **Overlap** is simultaneous progress of eligible stages; asynchronous APIs express opportunity but do not guarantee hardware concurrency.
- **Double/triple buffering** gives chunks distinct slots so one can transfer while another computes or returns.
- **Backpressure** prevents producers from admitting more work than bounded downstream capacity can safely retain.
- **Pinned host memory** enables some direct/asynchronous transfers but is scarce and must be bounded.
- **Critical path** is the longest dependency-weighted path; **throughput bottleneck** is the stage/resource limiting steady-state completions.
- **Affinity** associates a task, allocation, queue, event, NUMA node, or device with the context that owns it.
- **Cancellation** requests that future effects cease; already submitted device work may require draining rather than preemption.
- A **commit point** is the application-defined transition after which an output is accepted externally and retry semantics change.

### Central model, mechanism, or theorem

For every chunk, define a DAG such as CPU prepare → host-to-device transfer → kernel → device-to-host transfer → CPU validate/commit. Add resource constraints for host workers, pinned slots, device buffers, copy engines, compute queues, and result slots. Correctness requires each task start only after all producer completion/visibility events, each slot remain owned and alive through ordered last use, and external commit occur only after validation. Performance comes from overlapping independent eligible tasks subject to real capabilities and bounded capacity; the ideal pipeline interval is at least the maximum constrained stage demand, while latency includes the full path and queueing.

### Critical invariants

Every chunk has a stable identity and generation; every buffer slot has exactly one state/owner; byte ranges, shapes, pitches, devices, contexts, and queues match; event edges cover every cross-queue/device/host dependence; host mutation and deallocation wait for completion; pinned and device memory are quota-bounded; admission stops before capacity exhaustion; errors are collected at submission and completion; cancellation drains or quarantines in-flight work; retries are idempotent or deduplicated before commit; multi-GPU placement and peer paths are capability-checked; result order follows the declared policy; sensitive staging is isolated and erased; and correctness never depends on observed overlap.

### Common failures

Teams treat an asynchronous return as completion, reuse a ring slot while a copy still reads it, assume streams implicitly order each other, synchronize the whole device after every stage, allocate unbounded pinned buffers, omit backpressure, measure enqueue time, confuse throughput with latency, expect two copy directions or compute/copy overlap without capability evidence, pass an event/stream under the wrong device context, oversubscribe CPU threads and GPUs, mutate managed memory concurrently without a valid protocol, lose exceptions from callbacks, cancel only host bookkeeping, retry after an external side effect, reorder identities accidentally, or report average throughput while tail latency and device-reset recovery fail.

### Compact example

Three chunks each need two time units of host-to-device copy, five of GPU compute, and two of device-to-host copy on one engine per stage. Serial execution takes 27 units. With three independent slots and explicit edges, copies and compute overlap: chunk completions occur at 9, 14, and 19, so makespan is 19. This schedule is a deterministic resource model, not evidence that a device exposes these engines or durations.

### Connections

[Kernel Fusion and Data Movement](078-kernel-fusion-and-data-movement.md) chooses device materialization boundaries. [GPU Memory Hierarchies](076-gpu-memory-hierarchies.md) defines host/device placement and pinned/managed trade-offs. [Happens-Before Relations](023-happens-before-relations.md) supplies publication reasoning. The [program roadmap](../ROADMAP.md) next profiles a complete accelerator kernel before moving to distributed-memory ranks.

## Governing Question

For each chunk and stage, what data version is owned where, which event proves it is usable, which bounded resource it occupies, what can overlap, and what happens if any submission, execution, transfer, validation, cancellation, or device operation fails?

The durable answer is an ownership-and-event DAG plus a capacity model. Streams are mechanisms for submitting part of that graph; they are not the architecture, and concurrency observed on one target is not a correctness premise.

## Why This Matters

A GPU kernel can be fast while the service is slow because CPU preprocessing, pageable staging, transfers, queue gaps, synchronization, postprocessing, and admission dominate. Chunking and asynchronous queues can hide some costs, but they also create concurrent lifetimes and multiple partially completed generations.

Those states are where corruption and operational failures occur: a host producer overwrites a slot still being copied, a callback publishes an unchecked result, a timeout frees live device memory, or an automatic retry duplicates an external action. A production pipeline optimizes after it can name every state, edge, budget, and recovery transition.

## Prerequisites and Retrieval

Retrieve:

- kernel submission, events, block independence, and delayed errors from [GPU Execution Grids, Blocks, and Warps](075-gpu-execution-grids-blocks-and-warps.md);
- pinned/mapped/managed memory, migration, peer topology, and asynchronous lifetime from [GPU Memory Hierarchies](076-gpu-memory-hierarchies.md);
- fusion, materialization, launch graphs, compilation, and fallback from [Kernel Fusion and Data Movement](078-kernel-fusion-and-data-movement.md); and
- release/acquire, happens-before, and data-race reasoning from [Happens-Before Relations](023-happens-before-relations.md).

Retrieval prompt: draw one real chunk's stages and events. Annotate chunk/generation identity, input/output byte ranges, allocation/slot, host thread/NUMA node, device/context/queue, capability, earliest start, completion/error observation, cancellation state, retry key, commit point, and release. Which edges are API guarantees, application invariants, measurements, or assumptions?

## Learning Objectives

After completing this module, a learner can:

1. express a CPU-transfer-GPU pipeline as a task/resource DAG with explicit completion events;
2. distinguish submission, start, completion, visibility, validation, commit, and release;
3. design double/triple-buffer slot state machines with generation-safe reuse;
4. calculate simple serial and overlapped schedules, critical paths, bottlenecks, and bounded in-flight capacity;
5. apply backpressure, batching, queueing, deadlines, cancellation, and idempotent retry;
6. compare explicit copies, pinned/mapped/managed memory, integrated systems, and peer transfers;
7. schedule across CPUs, NUMA nodes, GPUs, queues, and heterogeneous task implementations;
8. validate capability-dependent overlap and measure end-to-end latency/throughput without enqueue-time errors;
9. handle synchronous/asynchronous errors, device loss, partial results, draining, fallback, and rollout; and
10. protect identity, privacy, fairness, auditability, and high-stakes acceptance across asynchronous stages.

## Core Exposition

### Model tasks, data versions, and resources

Create one logical chunk identifier and monotonically safe generation before preprocessing. Each task declares input versions, output versions, effects, eligible processors, resource needs, and completion signal. Each data version declares owner, address space/residence, size/layout, lifetime, and consumers. A dependency edge means the consumer cannot start until the producer's completion supplies the required visibility.

Add resource nodes or constraints: CPU worker pools, NUMA memory, pinned host slots, device allocations, H2D/D2H/peer paths, compute queues, library handles, compiler caches, and output capacity. DAG acyclicity does not prevent resource deadlock: tasks can hold one bounded pool while waiting for another. Establish a global acquisition order or reserve complete per-chunk capacity before admission.

Separate task readiness from scheduler choice. A ready task may run on CPU or one of several GPUs if an implementation and data placement exist. Scheduling should include transfer and queue cost, existing replicas, target speed, memory pressure, deadline, fairness, and failure domain—not compute time alone.

### Streams, queues, and events

A stream commonly orders commands submitted to it; independent streams/queues may overlap or run in another order. Exact default-stream, in-order/out-of-order, context, cross-device, and event semantics are API-specific. Express every dependence instead of relying on timing or prior observations.

Record an event after the producer operation and make the consumer queue wait on that event, or use a task runtime whose buffer/access requirements build an equivalent dependency DAG. A host wait is appropriate only when the host truly needs the value. Device-wide synchronization is a diagnostic or phase mechanism, not a default edge: it destroys unrelated overlap and couples failures.

Submission APIs can fail immediately for invalid arguments/resources. Execution and transfer faults may surface only through event/queue synchronization or an asynchronous handler. Capture both. Callbacks must not lose exceptions, block a driver thread indefinitely, submit forbidden API calls, or access destroyed context. Prefer a controlled completion executor that turns raw events into typed task outcomes.

### Buffer-slot state machine

A safe slot moves through states such as free → host-filling → H2D-in-flight → device-ready → compute-in-flight → result-ready → D2H-in-flight → host-validating → free. Attach `(slot, generation, chunk_id)` to every event so a late completion cannot authorize a newer occupant.

The host relinquishes mutation before H2D submission and does not reclaim the input range until copy completion. Device compute waits for that copy; D2H waits for compute; host validation waits for D2H. The slot becomes free only after all consumers, logging required for the contract, and sensitive erasure complete. Separate input and output slots when their lifetimes differ.

Double buffering may overlap one chunk's compute with another's transfer. Triple buffering can cover H2D, compute, and D2H simultaneously if the target has suitable engines and the stages are balanced. More slots increase memory, queueing latency, stale work after cancellation, and blast radius. Pick the smallest depth that sustains the measured bottleneck under bounds.

### Backpressure and admission

Every queue and pool has a finite capacity. Admission obtains a permit representing all resources that cannot be acquired later safely, or it enters a bounded state machine that never waits while holding resources in a cyclic order. When permits are exhausted, block, shed, degrade, batch, or route according to policy. Never continue allocating pinned/device buffers.

Little's Law relates average in-flight work L, admitted/completed rate lambda, and average time W under stable conditions: `L=lambda W`. It diagnoses impossible targets and capacity needs but does not size tail percentiles by itself. Bursts, skew, failures, retries, and service objectives require distributions and headroom.

Batching amortizes launch and transfer overhead and can coalesce work, but increases wait-to-fill latency, memory, failure scope, and fairness risk. Use maximum batch size plus a deadline/age trigger. Preserve per-item identity and allow isolation for unusually large or high-priority items.

### Overlap and pipeline arithmetic

For one chunk with sequential stage durations, latency is at least their dependency sum. Across chunks, ideal steady-state interval is at least the maximum demand on each serialized resource. Multiple stages sharing a copy engine, memory bandwidth, CPU pool, or device invalidate a simple maximum; model resource contention and then measure.

Asynchronous calls create eligible concurrency, not guaranteed overlap. Query whether copies and kernels can overlap, how many relevant engines exist, whether host memory must be pinned, and whether peer paths are available. Integrated coherent devices can have different optimal movement. Even where engines exist, bandwidth contention may make overlap slower.

Measure events around actual work and a host clock around end-to-end acceptance. Record queue wait, H2D, kernel, D2H, validation, and commit separately with a common correlation ID and clock-domain caveats. Enqueue duration is submission overhead only.

### CPU and GPU placement

Not every task belongs on the GPU. Small, branch-heavy, latency-sensitive, unsupported, or already-host-resident work may be cheaper on CPU. Large regular work may amortize transfer and launch. Dynamic schedulers can select implementations using calibrated models, but exploration must obey deadlines, capacity, and high-stakes change control.

Pin CPU workers and staging allocations to appropriate NUMA nodes when it materially affects transfers; do not assume host memory is uniform. Avoid oversubscribing CPU preprocessing threads, runtime workers, driver callbacks, and library pools. Thread counts, affinity, and library handles are resources recorded in the deployment configuration.

Multi-GPU placement adds device-specific contexts, queues, events, memory, topology, peer capabilities, and replica versions. Partition mutable work with one owner; version replicated read-only state; route transfers along verified paths. Load balance includes data movement and tail work. A faster remote GPU can lose after staging across a host bridge.

### Cancellation, errors, and commit

Cancellation is a state transition, not proof that submitted work stopped. Stop admission and downstream effects; request cancellation where supported; otherwise let device operations drain into quarantined buffers. Retain allocations, contexts, and events until terminal completion or reset. A device reset may invalidate all work and state in its context, so scope the blast radius and reconstruct verified replicas.

Classify failures as submission, transfer, execution, validation, deadline, resource exhaustion, device loss, or external commit. Retry only from a checkpoint whose inputs and versions remain valid. Give each external result an idempotency key or deduplication record. The commit point follows result validation; an event proving D2H completion does not prove domain acceptance or durable publication.

### Executable schedule model

This deterministic Python model schedules three chunks on one H2D engine, one compute engine, and one D2H engine with distinct slots. It models dependency/resource timing only—not threads, devices, queues, bandwidth, fairness, errors, or guaranteed overlap.

<!-- bijux-verify: {"id":"heterogeneous-pipeline-schedule","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"serial_makespan=27\nchunk_0=h2d:0-2,gpu:2-7,d2h:7-9\nchunk_1=h2d:2-4,gpu:7-12,d2h:12-14\nchunk_2=h2d:4-6,gpu:12-17,d2h:17-19\ncompletion_times=[9, 14, 19]\npipelined_makespan=19\nall_dependencies_hold=True\n","stderr":""}} -->
```python
chunks = 3
durations = {"h2d": 2, "gpu": 5, "d2h": 2}
available = {"h2d": 0, "gpu": 0, "d2h": 0}
schedules = []

for chunk in range(chunks):
    h2d_start = available["h2d"]
    h2d_end = h2d_start + durations["h2d"]
    available["h2d"] = h2d_end

    gpu_start = max(h2d_end, available["gpu"])
    gpu_end = gpu_start + durations["gpu"]
    available["gpu"] = gpu_end

    d2h_start = max(gpu_end, available["d2h"])
    d2h_end = d2h_start + durations["d2h"]
    available["d2h"] = d2h_end
    schedules.append((h2d_start, h2d_end, gpu_start, gpu_end, d2h_start, d2h_end))

serial_makespan = chunks * sum(durations.values())
print(f"serial_makespan={serial_makespan}")
for chunk, schedule in enumerate(schedules):
    hs, he, gs, ge, ds, de = schedule
    print(f"chunk_{chunk}=h2d:{hs}-{he},gpu:{gs}-{ge},d2h:{ds}-{de}")
print(f"completion_times={[schedule[-1] for schedule in schedules]}")
print(f"pipelined_makespan={schedules[-1][-1]}")
print(f"all_dependencies_hold={all(he <= gs and ge <= ds for _, he, gs, ge, ds, _ in schedules)}")
```

### Verification and operations

Test zero/one/many chunks, slot-count boundaries, partial batches, sizes around pin/copy thresholds, pitches, dynamic shapes, aliasing, delayed completions, event reuse, generation wrap policy, queue saturation, CPU/GPU skew, all stage failures, cancellation at every state, timeout, device loss/reset, retry, duplicate completion, and commit failure. Inject schedule delays and use race/bounds tools plus CPU/reference results.

Profile cold/warm allocation and compilation, prepare, queue wait, copies/migration, kernels, validation, commit, cleanup, memory high-water marks, throughput and latency distributions. Test target capabilities, NUMA placement, concurrency, tenants, clocks, thermal/power state, oversubscription, and reduced fallback. Explain missing overlap rather than assuming it.

Protect raw inputs, pinned staging, device pools, traces, dumps, logs, and retry stores. Enforce tenant quotas/fairness, access control, encryption where required, retention/erasure, and non-sensitive correlation. High-stakes release needs named domain, numerical, device/runtime, safety, privacy, operations, quality, and independent reviewers; none is implied by a correct event DAG.

## Definitions and Notation

- `G=(V,E)`: heterogeneous task DAG.
- `c,g`: chunk identity and generation.
- `S_j`: slot j and its state/owner.
- `E_v`: completion event for task v.
- `R(v)`: resources required by v.
- `d_v`: measured/model duration of v.
- `C_r`: capacity of resource r.
- `L`: average in-flight work; `lambda`: completion rate; `W`: average residence time.
- `P`: critical-path duration.
- `I`: steady-state initiation/completion interval under declared constraints.
- `t_commit(c)`: external acceptance point for chunk c.

Submission time is not `E_v` completion, and completion is not `t_commit`.

## Mechanisms, Invariants, or Proof Structure

### Dependency proof

Topologically order each chunk DAG. Every consumer queue waits for all producer events that supply its input version, and the API edge provides required visibility. Cross-queue/device/host edges are explicit. Independent work may reorder without changing observations.

### Slot-safety proof

The state machine grants one owner per `(slot,generation)`. No producer overwrites, consumer reads, host mutates, or allocator frees outside its state. Terminal event, validation, and erasure precede return to free. Late events compare generation and cannot release a reused slot.

### Capacity/deadlock proof

Every pool and queue has finite C. Admission is bounded, and tasks either reserve their complete acyclic resource set or acquire in a global order without waiting cyclically. Cancellation does not abandon held permits; every terminal path releases or quarantines them.

### Retry/commit proof

Before commit, a failed chunk may replay from a valid immutable/checkpointed version. After commit, duplicate effects are prevented by idempotency/deduplication or recovery is explicitly compensating. Results are validated before commit, and partial generations cannot masquerade as complete.

### Performance argument

A modeled schedule respects dependencies and resource serialization. Hardware overlap is claimed only from capability and timeline evidence. Comparisons retain workload/results, complete stages, queueing, repetitions, uncertainty, concurrency, and operating state.

## Alternatives and Trade-Offs

| Choice | Main benefit | Principal cost or risk |
|---|---|---|
| Synchronous phase | simple ownership/error point | destroys overlap |
| Streams plus events | explicit fine-grained overlap | lifetime/dependency complexity |
| Task-graph runtime | dependency/data placement abstraction | runtime policy and opacity |
| Double/triple buffer | covers multiple stages | memory and in-flight blast radius |
| Pinned staging | async/high-throughput copies | scarce host/NUMA resource |
| Managed/shared memory | simpler addresses/placement | migration/coherence variance |
| Larger batch | amortized overhead/throughput | wait latency, memory, fairness |
| Dynamic CPU/GPU choice | adapts to size/load | modeling, transfer, reproducibility |
| Multi-GPU partition | capacity/throughput | topology, replicas, failure |
| Device-wide wait | clear global phase | over-synchronization |
| Bounded fallback | predictable pressure/failure path | lower peak throughput |

Choose the smallest concurrency depth that sustains the measured objective and remains recoverable.

## Failure Modes and Misconceptions

- **“Async return means done.”** it usually means submitted.
- **“Same host order means device order.”** different queues need dependencies.
- **“An event makes data valid.”** wait/observe it in the correct context and validate results.
- **“More streams mean more overlap.”** engines, dependencies, and bandwidth bind.
- **“Pinned memory is free.”** it is finite and affects the host.
- **“Managed memory removes ownership.”** conflicting access and migration still require policy.
- **“Device synchronize is safest.”** it couples unrelated work and hides missing edges.
- **“Three slots are always enough.”** capacity follows stages, skew, and objectives.
- **“Unbounded queues maximize utilization.”** they create latency, memory, and failure collapse.
- **“Batching only improves throughput.”** it also adds waiting and fairness risk.
- **“Fastest device is best.”** placement/transfer/queue cost matters.
- **“Cancellation frees resources.”** in-flight work may still touch them.
- **“Retry is harmless.”** external effects need idempotency/commit rules.
- **“Completion order is result order.”** reorder explicitly by identity if required.
- **“Kernel timing is pipeline timing.”** host, transfers, queues, validation, and commit remain.
- **“Average throughput proves health.”** tails, saturation, resets, and tenant fairness remain.

## Worked Examples

### Example 1

**Slot reuse race.** The host refills slot 0 after kernel submission while H2D still reads it. **Conclusion:** reuse waits for the last actual reader event, not submission.

### Example 2

**Cross-stream gap.** D2H is submitted on another stream without waiting for compute and copies old data. **Conclusion:** host issue order is not a cross-stream edge.

### Example 3

**Triple pipeline.** Three distinct slots overlap H2D, compute, and D2H in the teaching schedule. **Conclusion:** slot identity and engine capability are preconditions.

### Example 4

**Pinned exhaustion.** Load spikes allocate one pinned buffer per request until the host becomes unstable. **Conclusion:** admission and pools bound concurrency.

### Example 5

**Small task routing.** A 2 KiB transform finishes faster on an available CPU than after a queued discrete-GPU transfer. **Conclusion:** schedule complete cost, not accelerator peak.

### Example 6

**NUMA staging.** A GPU-local CPU socket prepares data allocated on the remote node, saturating an inter-socket link. **Conclusion:** host placement belongs in the data path.

### Example 7

**Cancellation quarantine.** A deadline expires after launch; the slot is marked cancelled but retained until its event finishes, then erased. **Conclusion:** logical cancellation and physical completion differ.

### Example 8

**Duplicate callback.** Retry and a late original completion both attempt publication. An idempotency key admits one generation. **Conclusion:** commit must deduplicate.

### Example 9

**Multi-GPU skew.** Equal chunk counts overload a slower/topologically remote device. Weighted placement using transfer plus compute estimates reduces the tail. **Conclusion:** heterogeneous balance is not equal division.

### Example 10

**Emergency CT reconstruction.** Pipeline overlap must preserve patient/study/series/slice identity, geometry, calibration, units, ordering, missing-data policy, numeric/reconstruction validity, deadline/fallback, device-reset recovery, privacy, audit, and human override. Named radiology, emergency medicine, medical physics, imaging/numerical, GPU/runtime, software-safety, security/privacy, operations, quality/regulatory, human-factors, and independent validation reviewers must approve requirements and evidence; none is claimed here. **Conclusion:** throughput and correct event ordering do not establish diagnostic validity or clinical safety.

## Cross-Program Connections

- **Operating systems:** NUMA, pinned pages, queues, interrupts/callbacks, affinity, isolation, and device reset shape pipelines.
- **Distributed systems:** DAGs, backpressure, generations, idempotency, commit, retries, and partial failure recur across nodes.
- **Scheduling:** heterogeneous assignment, critical paths, fairness, deadlines, and admission govern resource use.
- **Programming languages:** futures/events, ownership, lifetimes, effects, exceptions, and cancellation encode correctness.
- **Databases/streaming:** bounded buffers, batching, watermarks, ordering, deduplication, and commit mirror accelerator flows.
- **Performance engineering:** timelines, queueing, distributions, and causal experiments expose actual bottlenecks.
- **Security:** staging pools, traces, multi-tenancy, erasure, and correlation metadata carry sensitive data.
- **Testing:** schedule perturbation, fault injection, target matrices, and reference execution provide evidence.
- **Reliability:** draining, quarantine, checkpoints, fallback, canary, rollback, and reset bound failures.
- **Human factors:** deadlines, degraded modes, alerts, and overrides must remain comprehensible under pressure.

## References

1. Cédric Augonnet et al., “StarPU: A Unified Platform for Task Scheduling on Heterogeneous Multicore Architectures,” *Concurrency and Computation* 23(2), 2011. <https://doi.org/10.1002/cpe.1631>
2. Michael Bauer et al., “Legion: Expressing Locality and Independence with Logical Regions,” SC 2012. <https://legion.stanford.edu/pdfs/sc2012.pdf>
3. NVIDIA, *CUDA Programming Guide: Asynchronous Execution*, current documentation; retrieved 2026-08-29. <https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/asynchronous-execution.html>
4. NVIDIA, *CUDA Programming Guide: Programming Systems with Multiple GPUs*, current documentation; retrieved 2026-08-29. <https://docs.nvidia.com/cuda/cuda-programming-guide/03-advanced/multi-gpu-systems.html>
5. NVIDIA, *CUDA Programming Guide: CUDA Graphs*, current documentation; retrieved 2026-08-29. <https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/cuda-graphs.html>
6. AMD, *HIP Asynchronous Concurrent Execution*, current documentation; retrieved 2026-08-29. <https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/hip_runtime_api/asynchronous.html>
7. AMD, *HIP Performance Guidelines*, current documentation; retrieved 2026-08-29. <https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/performance_guidelines.html>
8. Khronos SYCL Working Group, *SYCL 2020 Specification*, revision 12, Sections 3.7.1.2 and 4.6.6, 2026. <https://registry.khronos.org/SYCL/specs/sycl-2020/html/sycl-2020.html>
9. Khronos OpenCL Working Group, *OpenCL 3.0 Unified Specification*, current documentation; retrieved 2026-08-29. <https://registry.khronos.org/OpenCL/specs/3.0-unified/html/OpenCL_API.html>
10. OpenMP Architecture Review Board, *OpenMP API Specification 5.2*, 2021. <https://www.openmp.org/spec-html/5.2/openmp.html>

## Exercises

### Exercise 1

Derive the three-chunk H2D=2, GPU=5, D2H=2 serial and overlapped schedules under one engine per stage and three slots. State every non-hardware assumption.

### Exercise 2

Specify a generation-safe double-buffer state machine including ownership, events, errors, cancellation, validation, erasure, and reuse.

### Exercise 3

Use Little's Law to assess 500 chunks/s with 20 ms average residence and then design capacity for burst/tail behavior without misusing the average.

### Exercise 4

Design a controlled experiment comparing CPU, GPU synchronous, double-buffered, graph-replayed, and managed-memory implementations across size, NUMA, and concurrency.

### Exercise 5

A regulated genomic service pipelines CPU parsing, GPU alignment/scoring, transfer, CPU statistics, and publication across two GPUs. Specify semantic, scheduling, privacy, fairness, failure, performance, and human-review evidence.

## Answers to the Exercises

### Answer 1

Serial per chunk is 2+5+2=9 and three chunks take 27. With independent slots, H2D intervals are 0–2, 2–4, 4–6; compute waits for its H2D and engine, giving 2–7, 7–12, 12–17; D2H gives 7–9, 12–14, 17–19. Completion times are 9,14,19 and makespan 19. This assumes fixed durations, one independent resource per named stage, no shared-bandwidth contention, zero submission/CPU work, three live slots, dependency-correct events, no errors, and a device capable of the modeled overlap. It is not a speed guarantee.

### Answer 2

Represent `(slot,generation,chunk)` and allow one atomic/locked transition among free, filling, H2D, device-ready, compute, result-ready, D2H, validating, erasing/quarantined, free. Each submission records its event and expected generation. Producers relinquish mutation before transfer; consumers wait on predecessor events; all buffers live through completion. Immediate and delayed errors enter a terminal drain/quarantine path. Cancellation stops new stages but never frees in-flight memory. Validation precedes commit; sensitive erasure and all consumer/log obligations precede free. A late callback whose generation differs cannot transition the slot. Test every state and duplicated/reordered completion.

### Answer 3

For stable averages, `L=lambda W=500×0.020=10` chunks in flight. Ten is an average observation/requirement, not a safe capacity: it says nothing about arrival bursts, service variance, percentiles, retries, or outages. Measure distributions and dependency/resource stages, set an explicit queueing SLO, simulate or analytically bound burst envelopes, reserve headroom, and choose finite permits/pools. On exhaustion, apply documented blocking, shedding, batching, CPU fallback, or priority policy. Monitor queue age, pool use, tail latency, drops, retries, and fairness; reduce admission before memory/device collapse.

### Answer 4

Freeze inputs, outputs/numeric policy, identity/order, validation, and target/build. Measure end-to-end and stage distributions, queue waits, transfers/migration, kernel events, CPU work, compilation/graph setup, memory/pinned high water, power if relevant, and errors. Sweep zero/small/large, batch/chunk/slot depth, pageable/pinned, CPU NUMA affinity, integrated/discrete devices, cold/warm state, concurrent tenants, pressure, and failures. The synchronous GPU is a correctness baseline; double buffering tests overlap; graph replay isolates submission; managed memory tests placement/migration; CPU tests offload crossover. Require capability/timeline evidence, repetitions/uncertainty, reference equality, race/bounds checks, and complete cost rather than enqueue/kernel time.

### Answer 5

Preserve patient/sample/read/reference/coordinate identity and generation through parsing, batches, devices, results, statistics, and publication; define exact integer/floating/reduction, missing/duplicate/filter, ordering, and model/reference-version semantics. Build explicit H2D/kernel/D2H/CPU/commit events; use bounded generation-safe slots, device/context affinity, unique mutable ownership, replica versions, backpressure, quotas, fairness, deadlines, and topology-aware placement. Validate every supported device and CPU fallback across sizes/skew, concurrency, pressure, delayed errors, cancellation, loss/reset, retry/deduplication, and commit failure. Encrypt/minimize genomic staging, isolate tenants/pools, control traces/logs, audit access, and erase by policy. Measure stage/end-to-end distributions, bytes/migration, queues, high-water marks, throughput, tails, correctness, and degraded behavior. Named genomics, bioinformatics/statistics, clinical/laboratory where applicable, numerical, GPU/runtime, platform/scheduling, security/privacy, operations/SRE, quality/regulatory, human-factors, and independent validation reviewers approve validity, bias, limitations, and residual risk. Pipeline correctness and speed establish no biological or clinical validity.
