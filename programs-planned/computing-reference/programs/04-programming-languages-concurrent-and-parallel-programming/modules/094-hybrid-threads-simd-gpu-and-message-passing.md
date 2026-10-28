---
module_id: CONPAR-094
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 94
title: Hybrid Threads, SIMD, GPU, and Message Passing
status: complete
last_verified: 2026-08-29
---

# Hybrid Threads, SIMD, GPU, and Message Passing

## One-Page Review

### Governing question

How can a program compose rank-level distribution, host tasks/threads, SIMD lanes, and accelerator queues into one ownership and happens-before protocol that is correct under the weakest supported runtime guarantees and profitable on the target topology?

### Essential definitions

- **hybrid parallelism** combines two or more execution models, commonly MPI between address spaces, threads/tasks within a process, SIMD within cores, and kernels/streams on accelerators.
- A **parallelism hierarchy** maps algorithmic domains to nodes, ranks, host places, tasks, vector lanes, devices, teams/blocks, and lanes/threads.
- **ownership** identifies the unique authority allowed to mutate a logical state at an epoch.
- **MPI thread support** is the provided World-model level (`SINGLE`, `FUNNELED`, `SERIALIZED`, or `MULTIPLE`); the application must check it and obey the returned level.
- **funneled communication** routes MPI calls through the initializing/main thread; **serialized communication** allows multiple threads to call but never concurrently; **multiple** permits concurrent MPI calls subject to MPI/application ordering rules.
- A **SIMD lane** executes one element of a vector instruction; lane masking/divergence and tail handling affect work and validity.
- A **device stream/queue** orders enqueued operations according to its API; host submission generally does not imply device completion.
- A **completion event** establishes that an asynchronous transfer/kernel/request reached a documented state and permits buffer reuse/consumption.
- **host-device coherence/visibility** is API- and allocation-specific; a pointer value alone does not establish accessibility or freshness.
- **GPU-aware communication** is an implementation capability, not a portable inference from ordinary MPI buffer syntax.
- **oversubscription** creates more runnable software workers than allocated hardware contexts, often accidentally through nested runtimes.
- A **progress engine** advances communication/device work through calls, threads, or offload under implementation-specific guarantees.

### Central model, mechanism, or theorem

Treat every buffer/state transition as a versioned dependency graph: a producer owns generation g until its completion event; a consumer may read it only after the required host, MPI, device, or language happens-before edge; reuse begins only after every consumer completes. Map coarse distributed domains to ranks, shared subdomains to threads/tasks, regular inner work to SIMD, and high-throughput kernels to devices. The composition is correct only if each layer's assumptions—MPI provided thread level and collective order, language race freedom, SIMD independence, device stream/event/memory semantics, and process/device failure policy—hold simultaneously.

### Critical invariants

Ranks/threads/tasks/devices have stable identities and one owner per mutable object/version; actual MPI thread support is checked before worker launch; communicator/collective order is consistent; no two threads post conflicting receives or mutate MPI/device handles unsafely; host/device/MPI buffers remain alive, accessible, and immutable until completion; device events and host synchronization create required visibility; vector tails/alignment/aliasing/numerics are valid; rank/thread/device placement matches allocation and NUMA/NIC topology; nested runtimes cannot oversubscribe unexpectedly; queues/requests/staging are bounded; failures cannot publish partial epochs; and a scalar/host/reference path validates results.

### Common failures

Teams request `MPI_THREAD_MULTIPLE` but ignore a lower provided level, funnel calls through a thread other than allowed, serialize with a lock while collectives still occur in different order, let multiple threads wildcard-receive the same messages, reuse a send or device buffer early, assume kernel launch completion, copy pageable memory expecting overlap, pass device pointers to an unsupported MPI, mix default/nondefault stream semantics, oversubscribe through MPI×OpenMP×BLAS, assign multiple ranks the same GPU, vectorize across dependencies, omit SIMD tails, compare only kernel time, or call one backend's success portability.

### Compact example

For 2 nodes × 2 ranks/node × 4 host threads/rank × 8 SIMD lanes/thread, the nominal host-lane width is 128 elements at once, not a guaranteed speedup. If each rank also owns one GPU, exactly four GPUs are required; on two-GPU nodes the mapping is feasible. A request for three ranks/node with one GPU/rank is infeasible without sharing or a changed mapping. Capacity arithmetic validates configuration, not concurrency, correctness, or performance.

### Connections

[Processes and Ranks in Distributed-Memory Programs](081-processes-and-ranks-in-distributed-memory-programs.md) defines rank ownership. [Structured Concurrency](037-structured-concurrency.md) bounds task lifetime. [SIMD Execution and Vector Lanes](071-simd-execution-and-vector-lanes.md) covers lane semantics. [GPU Execution: Grids, Blocks, and Warps](075-gpu-execution-grids-blocks-and-warps.md) and [GPU Memory Hierarchies](076-gpu-memory-hierarchies.md) cover device execution. The [program roadmap](../ROADMAP.md) next analyzes allocator contention across these layers.

## Governing Question

What is the smallest parallel hierarchy that maps naturally to the algorithm and hardware, and what explicit dependency, ownership, completion, placement, resource, and failure contract connects every layer?

Hybridization is not an optimization by accumulation. Each layer adds a semantic boundary and resource pool; include it only when measured benefit repays complexity.

## Why This Matters

Large systems are hierarchical. MPI maps across failure/address-space domains; threads share node memory; SIMD uses core datapaths; GPUs provide massive throughput with distinct queues/memory. A single model may waste memory or locality, while a well-designed hybrid reduces ranks, uses node-local memory, vectorizes kernels, and offloads suitable work.

Composition creates bugs absent in isolation. MPI may offer weaker thread support than requested. Host completion differs from device completion. Thread-safe does not mean collective-order-safe. Device-aware messaging varies by implementation and transport. Nested libraries spawn hidden threads. A synchronization at one layer may not publish state to another.

The durable approach starts from ownership and a dependency DAG, maps each domain once, verifies runtime capabilities, then measures whole valid execution. Backends remain replaceable behind a narrow contract.

## Prerequisites and Retrieval

Retrieve:

- structured lifetime, synchronization, cancellation, and memory-model reasoning from [Structured Concurrency](037-structured-concurrency.md), [Task Parallelism and Dependency Graphs](041-task-parallelism-and-dependency-graphs.md), and [Reasoning About a Weak-Memory Program](030-reasoning-about-a-weak-memory-program.md);
- SIMD/GPU legality, layout, transfers, and completion from [SIMD Execution and Vector Lanes](071-simd-execution-and-vector-lanes.md), [Data Layout for Vectorization](072-data-layout-for-vectorization.md), [GPU Execution: Grids, Blocks, and Warps](075-gpu-execution-grids-blocks-and-warps.md), and [GPU Memory Hierarchies](076-gpu-memory-hierarchies.md);
- MPI request, collective, overlap, and scaling invariants from [Point-to-Point Message Passing](082-point-to-point-message-passing.md), [Collective Communication](083-collective-communication.md), and [Communication-Computation Overlap](086-communication-computation-overlap.md); and
- NUMA/device placement from [NUMA-Aware Allocation and Scheduling](093-numa-aware-allocation-and-scheduling.md).

Retrieval prompt: state algorithmic hierarchy/dependencies; ranks/nodes; threads/tasks/places; SIMD width/tails; GPUs/streams; memory regions and owners/versions; MPI requested/provided thread level; which threads call MPI; communicator/collective order; device-aware capability; host/device/staging allocation; completion edges; nested runtime threads; placement; queue/request/memory bounds; progress; failure/cancellation; validity oracle; and baseline.

## Learning Objectives

After completing this module, a learner can:

1. choose rank, thread/task, SIMD, and GPU decomposition by algorithmic ownership;
2. request, check, and obey MPI thread support levels;
3. design legal concurrent MPI call and collective-order protocols;
4. establish host-language, MPI-request, stream/event, and device-memory dependencies;
5. manage buffer lifetime, visibility, staging, and device-aware capability explicitly;
6. prevent nested oversubscription and enforce NUMA/NIC/GPU placement;
7. bound queues, requests, streams, staging, and memory;
8. validate vector/GPU numeric equivalence and tail/boundary behavior;
9. measure layer-specific and end-to-end performance without double counting; and
10. scope security, operations, portability, and high-stakes review.

## Core Exposition

### Map the algorithm to a hierarchy

Begin with the dependency/ownership graph. Ranks own coarse partitions requiring failure isolation or distributed memory. Within a rank, tasks/threads share data and exploit irregular or loop parallelism. SIMD handles independent regular inner iterations. GPUs receive sufficiently large, regular, high-throughput regions whose transfer/residency cost can be amortized.

Avoid duplicating parallelism. If MPI creates one rank/core and a threaded library also creates all cores, oversubscription follows. If every rank owns a full GPU context but GPUs are fewer than ranks, memory/context contention follows. Define resources from the allocation, then derive ranks per node, places/threads per rank, device mapping, and vector policy.

Retain a simpler baseline. MPI-only, rank+threads, or host-only variants help attribute benefit and provide fallback. Hybrid decomposition can change halo shapes, reduction order, memory footprint, and convergence; validate semantics.

### MPI and threads

With the World model, initialize through the thread-aware MPI routine and inspect the provided level. `SINGLE` allows one thread total. `FUNNELED` requires MPI calls from the main/initializing thread. `SERIALIZED` permits different threads, but application synchronization must prevent concurrent calls. `MULTIPLE` allows concurrent calls but does not remove communicator ordering, message matching, buffer, or application race obligations.

Fail or select a supported architecture if `provided < required`; never continue on the requested value. A funnel can use a bounded communication queue serviced by the main thread. A serialized design uses a lock plus a single protocol ordering discipline. Multiple may cost more and must be benchmarked; request the minimum needed.

Threads inside one MPI process are not separate MPI ranks. A receive may be satisfied by a thread consistent with matching rules; wildcard receives and concurrent wait-any can create nondeterminism. Partition messages by communicator/tag/source/owner and prevent competing conflicting receives.

Collectives on a communicator must be issued in matching order. A mutex alone cannot fix thread A choosing all-reduce while a peer's thread B chooses broadcast first. Use a per-communicator sequencer/epoch or dedicate a communication thread. Finalize on the required thread after worker MPI calls and pending operations are complete.

### Host concurrency and SIMD

Shared state must be data-race-free under the language/runtime memory model. Task completion, mutexes, atomics, barriers, or futures create host happens-before edges. An MPI call is not a universal host-thread fence; publish data through language synchronization before the communicating thread reads it.

SIMD requires independent iterations or a legal dependence transformation, valid alias/alignment assumptions, tail handling, and defined reductions. Masked lanes still may execute some operations; avoid invalid addresses/side effects. Match precision/FMA/fast-math policy and validate scalar/reference outputs.

Task grain should amortize scheduling and vector setup. Vectorize inner contiguous work while tasks partition coarse blocks. Dynamic task stealing can harm NUMA and device ownership; use hierarchical/local queues and stable data homes.

### Device queues and completion

Host kernel/transfer submission is generally asynchronous. Within a stream, operations follow documented order; across streams, use events/dependencies. A host may reuse/free/read a buffer only after the operation consuming/producing it completes and visibility semantics permit access. Device-wide synchronization is simple but destroys overlap; prefer narrow events/stream waits with clear ownership.

Default stream behavior and implicit synchronization depend on API/configuration. Record it. Pageable versus pinned host buffers, allocation calls, and transfers can change overlap. Pinned memory is finite and affects the OS; pool and bound it.

For double buffering, slot k has states FREE → HOST_READY → TRANSFER_IN_FLIGHT → DEVICE_READY → KERNEL_IN_FLIGHT → RESULT_READY → MPI_IN_FLIGHT → FREE. Each transition has one event/request and owner. An epoch/slot cannot be reused early, including on cancellation/error.

### Executable capacity model

This deterministic configuration check computes nominal hierarchy width and device feasibility. It does not create threads, vector instructions, MPI ranks, streams, or concurrency and proves no speedup.

<!-- bijux-verify: {"id":"hybrid-capacity-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"nodes=2\nranks_per_node=2\nthreads_per_rank=4\nsimd_lanes=8\ntotal_ranks=4\ntotal_host_threads=16\nnominal_host_lanes=128\ngpus_per_node=2\nrequired_gpus=4\navailable_gpus=4\ndevice_mapping_feasible=True\nthree_ranks_per_node_feasible=False\n","stderr":""}} -->
```python
nodes = 2
ranks_per_node = 2
threads_per_rank = 4
simd_lanes = 8
gpus_per_node = 2

total_ranks = nodes * ranks_per_node
total_threads = total_ranks * threads_per_rank
required_gpus = total_ranks
available_gpus = nodes * gpus_per_node

print(f"nodes={nodes}")
print(f"ranks_per_node={ranks_per_node}")
print(f"threads_per_rank={threads_per_rank}")
print(f"simd_lanes={simd_lanes}")
print(f"total_ranks={total_ranks}")
print(f"total_host_threads={total_threads}")
print(f"nominal_host_lanes={total_threads * simd_lanes}")
print(f"gpus_per_node={gpus_per_node}")
print(f"required_gpus={required_gpus}")
print(f"available_gpus={available_gpus}")
print(f"device_mapping_feasible={required_gpus <= available_gpus}")
print(f"three_ranks_per_node_feasible={nodes * 3 <= available_gpus}")
```

### MPI and device buffers

The MPI standard specifies buffer semantics, but accelerator-pointer support and performance depend on implementation/runtime/environment. Discover and test capability using official implementation mechanisms; do not infer from a successful small message. Unsupported pointers can fail, stage unexpectedly, or appear to work unsafely.

If GPU-aware communication is supported, establish that producing kernel completed before MPI consumes the buffer, and that MPI request completed before the next device operation overwrites/uses results. An MPI completion may require device/runtime integration whose details are implementation-specific. Preserve context/device association per calling thread.

Otherwise use explicit bounded host staging: device event → device-to-host copy completion → MPI request → host-to-device copy → device event. Pinned pools have slot/epoch ownership and backpressure. Compare direct versus staged paths across sizes/topologies and validate payloads.

### Progress and overlap

MPI may provide weak progress; CUDA/device engines have their own concurrency/engine constraints. A host thread that launches work then computes indefinitely may prevent MPI progress. A progress thread consumes an allocated core and needs affinity/NUMA design. Polling cadence trades latency for CPU overhead.

Trace submission, actual start, completion, dependencies, MPI post/complete, CPU tasks, and critical path. Concurrent timeline bars are not proof of useful overlap if they contend for memory/NIC/PCIe or extend the critical path. Measure exposed wait and full valid time.

Schedule independent work before dependent waits. Avoid oversubscribing transfer engines/streams; more streams do not create more hardware engines. Bound outstanding collectives/requests and preserve per-communicator order.

### Placement and resources

Derive CPU places from scheduler allocation and NUMA topology. Assign ranks to sockets/NUMA domains, threads to distinct allowed places, first-touch data with owners, GPUs uniquely or through an explicit sharing service, and NIC affinity where relevant. Record actual mappings.

Coordinate `OMP_NUM_THREADS`/places/bind, task runtime, BLAS/library threads, GPU contexts/streams, MPI progress threads, and profiling threads. Set library thread counts deliberately. Count every worker against allocated CPUs.

Budget per rank/thread/device buffers, halos, staging, request objects, streams/events, allocator pools, communicator state, and checkpoints. Multiplying per-rank metadata by many ranks can erase hybrid memory benefits. Apply backpressure before pools exhaust.

### Numeric and semantic equivalence

Parallel hierarchy changes order. SIMD FMA, threaded reductions, GPU atomics, MPI collective trees, asynchronous scheduling, and mixed precision change floating results. State reproducibility policy: bitwise, deterministic within backend, bounded error/residual, or domain outcome.

Test scalar/serial small cases, host threaded/SIMD, each device backend, different ranks/threads/blocks/streams, boundary/tail sizes, NaN/Inf/subnormal/extreme values, reduction orders, and restart. Compare high-precision or independent references and convergence trajectories.

Do not call a device result equivalent because a checksum matches if accuracy matters. Preserve global IDs and counter-based randomness across decomposition where required.

### Failure and cancellation

Structured ownership must drain/cancel child tasks, MPI requests, and device work before freeing state. Many operations cannot be safely cancelled after start; mark the epoch failed, stop new work, complete/drain or abort according to supported APIs, and discard unpublished outputs.

Ordinary MPI process failure is generally not recoverable by application continuation. Device errors may poison a context. Define abort/checkpoint/restart and re-discover topology/devices/thread support on restore. External effects are idempotent and publication is generation-atomic.

A communication thread failure or deadlock must be observable through timeouts/watchdogs designed not to violate collective semantics. Avoid detached background workers with access to finalized runtimes.

### Performance experiment

Compare validated variants: scalar/reference, host threads, threads+SIMD, GPU, MPI-only, MPI+threads, and justified full hybrid. Keep problem, algorithm, precision/tolerance, output, allocation, and timing boundaries comparable; document intentional changes.

Measure full/phase critical time, ranks/threads/devices, useful work/vector utilization, task queues/steals, MPI calls/messages/bytes/arrival/progress, transfers/kernels/streams/occupancy, CPU/GPU/memory/NIC/PCIe utilization, NUMA, staging/allocations, synchronization, energy/resources, failures, and numerical error. Retain distributions and all invalid runs.

Vary sizes, node/device shapes, ranks per node, threads, vector policy, GPU mapping, message sizes, thread support modes, funnel/serialized/multiple, progress, staging/direct communication, streams, imbalance, and failures. Select the smallest robust hierarchy with positive end-to-end benefit and operational evidence.

### Security, operations, and high-stakes limits

Validate counts, device IDs, pointer spaces, ranges, message metadata, kernel dimensions, queue limits, and runtime capabilities. GPU-aware/staging paths are trust boundaries; authenticate distributed peers where threat model requires. Minimize sensitive traces containing hostnames, topology, kernel names, data shapes, or medical/customer activity.

Monitor provided thread level, mapping/oversubscription, queue/request/stream depth, progress, device/NIC/NUMA health, transfer/kernel/MPI tails, memory pools, numerical checks, errors, checkpoints, and fallback usage. Preserve backend/config provenance.

High-stakes hybrid systems require domain, numerical, concurrency/MPI, accelerator/vendor, safety, security/privacy, operations, quality/regulatory, ethics, accessibility/human-factors, and independent validation reviewers. Hardware utilization never establishes domain validity.

## Definitions and Notation

- N: nodes; R: MPI ranks; H: host threads/tasks; V: SIMD lanes; D: devices.
- e: run/algorithm epoch; g: buffer/data generation; s: bounded slot.
- `owner(x,g)`: unique authority for object x generation g.
- `E_host`, `E_mpi`, `E_device`: language, request, and stream/event dependency edges.
- `requested`, `provided`: MPI thread support levels; correctness uses provided.
- `Q_max`: bounded outstanding tasks/requests/transfers per stage.
- **completion**: API-specific state allowing declared reuse/visibility; never generic.
- **nominal width**: product of hierarchy counts, not speedup or guaranteed simultaneous execution.
- Obs: topology, capabilities, mapping, versions, timelines, resources, results, and limitations.

## Mechanisms, Invariants, or Proof Structure

### Capability/mapping proof

Discover allocation/topology/runtime/device capabilities; verify provided MPI thread level, places, device-aware support, visible devices, stream semantics, and actual bindings. Reject infeasible or weaker configurations before work.

### Ownership/dependency proof

Every mutable object/version has one owner. Every producer-consumer transition has the exact host synchronization, MPI completion, and device event needed; buffers live and remain immutable until all consumers complete; slot/epoch reuse is safe.

### Protocol-order proof

Per communicator, collectives and matching operations follow one versioned sequence; concurrent threads cannot race on matching, requests, handles, or state. Funnel/serialization respects main-thread and mutual-exclusion requirements.

### Resource/failure proof

Worker, queue, request, stream, staging, allocator, context, and memory totals fit allocation; backpressure holds. Cancellation/error drains or aborts safely; publication is atomic; restart reinitializes capabilities/mapping.

### Equivalence/benefit proof

All hierarchy/backends pass independent result/numerical tests across tails/boundaries/schedules. Controlled full timelines show predicted overlap/locality/utilization and improved time-to-valid-solution/resources over simpler baselines within the tested envelope.

## Alternatives and Trade-Offs

| Design | Main benefit | Principal limitation |
|---|---|---|
| MPI-only | simple process isolation | memory/context duplication |
| threads+SIMD | shared memory, low communication | one-process failure/races/NUMA |
| MPI+funneled threads | low MPI concurrency burden | communication-thread bottleneck |
| MPI serialized | flexible callers | lock/order contention |
| MPI thread multiple | concurrent calls | implementation cost/protocol complexity |
| GPU offload | high regular throughput | transfers, device memory, backend variance |
| GPU-aware MPI | avoids explicit host staging | capability/transport portability |
| bounded pinned staging | explicit portable pipeline | copies and pinned-memory pressure |
| full hybrid | maps all hardware levels | maximum verification/operations burden |

## Failure Modes and Misconceptions

- **“Requested MPI thread level is provided.”** inspect and obey the return.
- **“Thread multiple removes ordering.”** communicator/matching/application rules remain.
- **“A mutex makes collectives safe.”** peers still need the same order.
- **“Threads have MPI rank identities.”** rank addresses a process.
- **“MPI completion synchronizes all host state.”** language happens-before remains necessary.
- **“Kernel launch means result ready.”** use documented completion.
- **“Same pointer means same accessibility.”** address spaces/coherence/capability differ.
- **“Successful device-pointer send proves support.”** discover/test official capability.
- **“Pinned memory is unlimited.”** pool and bound it.
- **“More streams mean more overlap.”** engines/dependencies/resources limit it.
- **“SIMD lanes are threads.”** execution/memory semantics differ.
- **“Nominal width is speedup.”** dependencies and resources decide.
- **“Nested runtimes coordinate automatically.”** oversubscription is common.
- **“One rank per GPU is always best.”** mapping depends on workload/device count.
- **“GPU result order matches CPU.”** reductions/FMA/scheduling differ.
- **“Kernel speedup is application speedup.”** critical path and transfers matter.
- **“Device error is locally recoverable.”** contexts/MPI job may require restart.
- **“One hybrid configuration is portable.”** capabilities/topologies vary.

## Worked Examples

### Example 1

**Thread-level downgrade.** Program requests MULTIPLE, receives SERIALIZED, and selects a locked per-rank communication service. **Conclusion:** capability determines architecture.

### Example 2

**Collective inversion.** Two local threads call broadcast/all-reduce in opposite peer order. A communicator sequencer fixes the protocol. **Conclusion:** thread safety is not protocol order.

### Example 3

**Early device reuse.** MPI reads a device buffer before producing kernel event. Add event-to-communication dependency. **Conclusion:** compose completion domains.

### Example 4

**Staged pipeline.** Two pinned slots overlap device copy, MPI, and next kernel with explicit state transitions. **Conclusion:** bounded ownership enables safe overlap.

### Example 5

**Hidden oversubscription.** Four ranks × eight OpenMP × eight BLAS threads target 32 cores. Set BLAS to one or redesign nesting. **Conclusion:** count every worker.

### Example 6

**SIMD tail.** Vector width eight processes N=67 with eight full vectors plus a safe three-lane mask/scalar tail. **Conclusion:** boundary sizes are correctness cases.

### Example 7

**GPU sharing.** Four ranks contend for two GPUs and duplicate memory. Two GPU-owning ranks with host threads win. **Conclusion:** map capacity explicitly.

### Example 8

**Progress loss.** Host threads compute while no thread enters weak-progress MPI. Dedicated pinned progress restores overlap at one-core cost. **Conclusion:** account for progress resources.

### Example 9

**Numeric divergence.** Tensor precision reduces iterations/sec but fails residual/domain tolerance. Reject or treat as separately reviewed algorithm. **Conclusion:** throughput follows validity.

### Example 10

**Weather data-assimilation cycle.** Hybrid changes must preserve observation/model/grid/ensemble/time/coordinate/unit/calibration/solver/partition/random/precision epochs, conservation/residual/uncertainty, late/missing observations, deadline/failure/restart, provenance/privacy/security, and forecast publication gates. Named meteorology/data-assimilation, numerical/statistics, MPI/concurrency, accelerator/vendor, operations, cybersecurity/privacy, quality/regulatory, emergency-management, ethics, accessibility/human-factors, and independent validation reviewers must approve evidence; none is claimed here. **Conclusion:** hybrid utilization does not establish forecast skill or safe warnings.

## Cross-Program Connections

- **Languages:** memory models, atomics, SIMD legality, and structured lifetime define intra-process correctness.
- **Runtimes:** task queues, nested pools, affinity, progress, streams, and events compose execution.
- **Distributed systems:** epochs, ownership, message matching, collectives, failures, and restart cross processes.
- **Architecture:** vector units, NUMA, GPUs, NICs, engines, caches, and memory tiers shape mapping.
- **Compilers/libraries:** vectorization, offload, BLAS, and MPI capabilities change worker/resource counts.
- **Numerical computing:** reduction order, precision, FMA, convergence, and randomness bound equivalence.
- **Performance engineering:** timelines, layer counters, baselines, and resource accounting prove benefit.
- **Security/privacy:** device/staging/message boundaries and traces need validation/access control.
- **Operations:** capability discovery, monitoring, fallback, checkpoint/restart, and provenance sustain runs.
- **Safety:** valid domain results outrank utilization.

## References

1. MPI Forum, *MPI: A Message-Passing Interface Standard, Version 5.0*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report.pdf>
2. MPI Forum, *MPI-5.0: MPI and Threads*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node283.htm>
3. MPI Forum, *MPI-5.0: General Thread Semantics*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node284.htm>
4. MPI Forum, *MPI-5.0: Thread Clarifications*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node285.htm>
5. OpenMP Architecture Review Board, *OpenMP API Specification 6.0*, 2024. <https://www.openmp.org/wp-content/uploads/OpenMP-API-Specification-6-0.pdf>
6. OpenMP Architecture Review Board, *OpenMP API 6.0 Reference Guide*, 2024. <https://www.openmp.org/wp-content/uploads/OpenMP-RefGuide-6.0-OMP60SC24-web.pdf>
7. NVIDIA, *CUDA Programming Guide*, release 13.2. <https://docs.nvidia.com/cuda/cuda-programming-guide/pdf/cuda-programming-guide.pdf>
8. NVIDIA, *CUDA Runtime API: Stream Management*, current documentation; retrieved 2026-08-29. <https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__STREAM.html>
9. NVIDIA, *CUDA Runtime API: Event Management*, current documentation; retrieved 2026-08-29. <https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__EVENT.html>
10. Open MPI Project, *Process Placement, Affinity, and Binding*, current documentation; retrieved 2026-08-29. <https://docs.open-mpi.org/en/main/tuning-apps/affinity.html>

## Exercises

### Exercise 1

A two-node allocation has 32 cores and four GPUs per node. Evaluate configurations `(ranks/node,threads/rank,GPU/rank)` of `(4,8,1)`, `(8,4,1)`, and `(2,16,2)` for CPU oversubscription and GPU capacity. State ambiguities.

### Exercise 2

Design legal communication architectures for FUNNELED, SERIALIZED, and MULTIPLE thread support, including collective order, matching, progress, and finalization.

### Exercise 3

Specify a three-slot GPU-aware or staged halo pipeline as a state machine with host, device, and MPI completion edges, backpressure, cancellation, and reuse.

### Exercise 4

Design an experiment to decide among MPI-only, MPI+threads+SIMD, MPI+GPU, and full hybrid. Include capabilities, mappings, results, metrics, perturbations, and decision rule.

### Exercise 5

Transfer the hybrid framework to distributed real-time stroke imaging. Specify data/numeric, ownership/completion, deadline/failure, privacy/security, validation/publication, and named human reviewer invariants without claiming review.

## Answers to the Exercises

### Answer 1

Per node, 4×8=32 host threads and 4 GPUs required: fits exactly. 8×4=32 threads but needs 8 GPUs: infeasible for exclusive one-GPU/rank unless explicit sharing/change. 2×16=32 threads and two GPUs per rank means 4 GPUs: fits if each rank legally manages two. All omit MPI/progress/library/profiling threads, SMT policy, memory/context capacity, NUMA/NIC locality, GPU partitioning/sharing rules, workload granularity, and whether GPU/rank means exclusive.

### Answer 2

FUNNELED: initializing main thread owns all MPI; workers publish bounded commands/results via host synchronization to a communication service; main sequences communicators and finalizes after workers/drain. SERIALIZED: callers may differ, but one application lock/sequencer prevents overlap and assigns monotonically ordered per-communicator operations; host data is published before the lock/call and progress ownership is explicit. MULTIPLE: concurrent calls are allowed only after `provided` check; partition communicators/tags/requests/receives by owner, preserve collective order through a sequencer, prevent conflicting wildcards/handle races, and define progress. In every mode complete requests/buffers, stop workers, then finalize on the required main thread.

### Answer 3

Each slot `(epoch,index)` transitions FREE→HOST_FILLING→HOST_READY; host publication then H2D_IN_FLIGHT; a copy event yields DEVICE_READY; producing kernel yields DEVICE_PRODUCED; event/capability bridge permits MPI_IN_FLIGHT directly, or D2H_IN_FLIGHT→STAGED_READY→MPI_IN_FLIGHT. MPI completion yields REMOTE_READY or, for receive, H2D_IN_FLIGHT→device event→CONSUMER_KERNEL→RESULT_READY→FREE. One owner mutates each state, IDs validate epoch/peer/size, and three slots bound pressure. Cancellation stops new acquisition, drains legally noncancellable work or aborts epoch, never frees/reuses until completions, discards failed generation, and publishes only after all required slots/results validate.

### Answer 4

Discover provided MPI thread level, CPUs/NUMA/GPUs/NICs, device-aware support, stream engines, runtime/library worker counts and memory. Build feasible verified mappings and keep problem/algorithm/precision/tolerance/output/resources comparable. Validate scalar/reference plus each backend across tails, schedules, device counts and failures. Measure full/phase critical time, useful/vector work, task queues/steals, MPI traffic/arrival/progress, transfer/kernel/stream timelines, NUMA/device/NIC utilization, staging/pools, memory, energy, errors and numerical difference over repetitions. Vary size, ranks/node, threads, affinity, thread mode, progress, direct/staged path and streams. Choose the simplest configuration whose assumptions/capacity hold, all results pass, and confidence-bounded end-to-end/resource benefit is robust; retain fallback and reject kernel-only wins.

### Answer 5

Bind patient/study/consent/image/sequence/geometry/calibration/model/algorithm/partition/device/precision epochs; preserve coordinates/units, acquisition completeness, residual/reference/image-quality and clinical decision boundary. One rank owns each shard, host tasks own versions, SIMD/GPU kernels consume only after host/device events, and MPI exchanges only after producing completion; provided thread level, collective order, buffer slots and device mapping are enforced. Bound queues/memory/pinned buffers and define corrupt/missing frame, device/MPI/process error, deadline, drain/abort, checkpoint/restart, conservative CPU/reference fallback and fail-closed display. Encrypt/authenticate least-privilege traffic, pseudonymize, minimize/redact traces, retain audit. Validate phantoms and independent cases, high-precision/reference, adversarial tails/schedules/devices/thermals/failures/restores, subgroup/artifact sensitivity, privacy/security and workflow. Named stroke neurology/neuroradiology, imaging/medical physics, numerical/reconstruction, MPI/concurrency/accelerator, clinical data/privacy/security, operations, quality/regulatory, ethics, accessibility/human-factors, and independent validation reviewers are required. No external review, diagnostic validity, privacy guarantee, approval, or deployment authorization is claimed.
