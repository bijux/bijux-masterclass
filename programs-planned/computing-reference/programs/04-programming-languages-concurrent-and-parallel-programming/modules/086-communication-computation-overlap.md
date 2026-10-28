---
module_id: CONPAR-086
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 86
title: Communication-Computation Overlap
status: complete
last_verified: 2026-08-29
---

# Communication-Computation Overlap

## One-Page Review

### Governing question

When can communication, copies, and computation truly proceed concurrently, and how can a program prove dependency safety and measure a shorter end-to-end critical path rather than merely use asynchronous APIs?

### Essential definitions

- **asynchronous initiation** returns before an operation completes; it expresses potential concurrency.
- **progress** is execution of pending communication activity; **strong progress** can occur without relevant MPI calls, while **weak progress** may require blocked or repeated test calls.
- **independent work** does not read receive buffers or modify send buffers/resources protected by the pending operation.
- **overlap window** is the time between initiation and the first dependency-required completion.
- **hidden communication time** is communication removed from the critical path by useful concurrent work.
- **exposed communication time** remains on the critical path at the completion point.
- **arrival skew** is variation in when ranks initiate a related operation; local elapsed time can include waiting for late peers.
- **pipelining** divides work/data into stages so communication for one chunk overlaps computation for another.
- **double buffering** separates buffers owned by different pipeline generations.
- **progress thread/offload** advances communication concurrently using CPU runtime work or a NIC/device engine.
- **resource contention** occurs when communication and computation compete for cores, memory bandwidth, PCIe/NVLink, cache, NIC, or power.

### Central model, mechanism, or theorem

Let communication take C, dependency-independent interior work take W, and dependent boundary/finalization work take B. A serialized lower model is `T_ser=C+W+B`. With immediate progress and no harmful contention, the best schedule is `T_ov=max(C,W)+B`; hidden time is `min(C,W)` and exposed time is `max(0,C-W)`. These are bounds, not guarantees. Correct overlap also requires that every pending operation's buffers, request, datatype, communicator, and device events remain valid and untouched, and that completion occurs before dependent work.

### Critical invariants

Receives are posted early enough; matching and collective order remain correct; sends read stable produced data; independent work touches neither protected send regions nor incomplete receive regions; outputs are generation-separated; progress assumptions are documented and tested under weak progress; polling is bounded and does not starve work; thread support matches progress-thread behavior; device streams/events establish production and consumption order; every request completes exactly once; outstanding operations and pinned/staging memory are bounded; final results match the serialized reference; and claimed overlap reduces a verified critical-path metric with uncertainty reported.

### Common failures

Teams equate `Isend` return with transfer, place no work between initiate/wait, call “interior” code that reads halos, modify send buffers, depend on strong progress, poll so often that calls dominate, poll never on a weak-progress runtime, dedicate an unpinned/unbound progress thread that steals the compute core, serialize GPU work in a default stream, overlap two bandwidth-bound kernels that slow each other, oversubscribe requests, time ranks without arrival skew, or report initiation latency instead of full valid iteration time.

### Compact example

If communication C=7 ms, independent work W=5 ms, and dependent boundary work B=3 ms, serialization costs 15 ms. The ideal overlap bound is `max(7,5)+3=10` ms: 5 ms hidden, 2 ms exposed, speedup 1.5. If the runtime makes no progress during W, the actual time remains 15 ms despite nonblocking calls.

### Connections

[Halo Exchange and Stencil Computation](085-halo-exchange-and-stencil-computation.md) supplies the safe interior/boundary split. [Point-to-Point Message Passing](082-point-to-point-message-passing.md) supplies completion and buffer ownership. [Heterogeneous CPU-GPU Pipelines](079-heterogeneous-cpu-gpu-pipelines.md) supplies stream/copy dependencies. The [program roadmap](../ROADMAP.md) next applies asynchronous structure to parallel I/O.

## Governing Question

For each pending transfer or collective, which useful operations are dependency-independent, what mechanism actually advances the operation on the target, what resources contend, and does the complete validated critical path become shorter across realistic ranks, messages, and load skew?

Overlap is a scheduling claim supported by a dependency proof and a timeline. An asynchronous function name supplies neither by itself.

## Why This Matters

Distributed programs often wait for halo messages, reductions, storage, or device copies. As scale increases, latency and late-rank arrival occupy more of the iteration. Moving independent work into that interval can hide part of the cost without changing the algorithm.

But apparent concurrency is fragile. MPI implementations can have different progress behavior; a progress thread consumes resources; interior work can saturate the same memory system used by communication; GPU streams can serialize through dependencies; and a different schedule can alter floating-point or convergence behavior. Excess in-flight work also increases memory and failure complexity.

Production overlap engineering therefore begins from a dependency DAG, protects asynchronous lifetimes, establishes portable weak-progress correctness, and measures timelines and outputs together. Often the best result comes from reducing communication or synchronization rather than hiding it.

## Prerequisites and Retrieval

Retrieve:

- exact envelope/signature matching, request completion, buffer/object lifetime, progress, flow control, and failure from [Point-to-Point Message Passing](082-point-to-point-message-passing.md);
- collective initiation order, nonblocking/persistent semantics, and global arrival effects from [Collective Communication](083-collective-communication.md);
- owned/ghost snapshot separation and interior/boundary dependencies from [Halo Exchange and Stencil Computation](085-halo-exchange-and-stencil-computation.md); and
- CPU/device queues, events, buffers, copies, and backpressure from [Heterogeneous CPU-GPU Pipelines](079-heterogeneous-cpu-gpu-pipelines.md).

Retrieval prompt: draw the operation DAG; mark produced send data, incomplete receive data, and first consumers; record communicator/peer/tag/order; request/buffer/datatype lifetime; C/W/B components; progress and thread-support mode; polling points; device streams/events; shared resource demand; outstanding limits; arrival skew; correctness oracle; instrumentation; and target versions/placement.

## Learning Objectives

After completing this module, a learner can:

1. distinguish asynchronous initiation, progress, concurrency, overlap, and latency hiding;
2. derive serialized and ideal-overlap critical-path bounds from a dependency DAG;
3. partition computation into truly independent and communication-dependent regions;
4. write correct nonblocking, persistent, partitioned, and begin/end schedules;
5. design weak-progress-safe polling or qualify strong progress/offload;
6. reason about progress threads, MPI thread levels, affinity, oversubscription, and contention;
7. coordinate MPI, host-device copies, kernels, streams, and events without lifetime races;
8. bound requests, buffers, pipeline depth, and failure cleanup;
9. measure hidden/exposed time, arrival skew, resource contention, and complete-result equivalence; and
10. scope numerical, operational, security, and high-stakes review claims.

## Core Exposition

### Start with the dependency DAG

Represent every pack, initiate, transfer, local kernel, completion, unpack, boundary kernel, reduction, copy, and publication as a node. Add edges for data production/consumption, buffer ownership, request completion, stream order, collective order, and resource serialization. Work is overlap-eligible only if no path from incomplete remote data or protected send data reaches it.

For a halo step, post receives and sends for `u^t`, compute owned points whose stencil lies entirely in owned `u^t`, complete/validate receives, then compute halo-dependent points. The geometric label “interior” is not enough: a high-radius or data-dependent operator can reach remote values. Generate bounds from the dependency set and test them with poisoned receive buffers.

Global reductions offer different opportunities. Initiate a nonblocking all-reduce only after its local contribution is finalized. Work between initiation and wait must not depend on the global result and must preserve collective initiation order on every rank. Speculative work may be discarded if the result changes a branch, but its cost and side effects require explicit control.

### Initiation is not progress

An MPI nonblocking start returns before completion and protects its buffers; it permits an implementation to overlap but does not require effective performance overlap. MPI 5.0 distinguishes strong and weak progress and requires applications to be correct assuming weak progress. Blocked MPI procedures and repeatedly called MPI test procedures provide specified progress contexts; a tight non-MPI compute region cannot blindly assume transfer completion.

Characterize the target. Run a progress microexperiment with realistic message size and peer behavior: initiate, execute calibrated compute without MPI calls, then test/wait; compare with periodic tests and an enabled progress thread/offload configuration. Record MPI/library/transport/config and CPU use. A microtest informs mechanism behavior but application timelines remain authoritative.

Weak-progress-safe designs insert `MPI_Test`, `Testsome`, or other appropriate progress calls at bounded points while doing chunks of useful work. Choose chunk size so polling overhead and cache disruption remain small while exposed latency is acceptable. Correctness must not depend on a test becoming true before the final wait.

### Critical-path model

Let C include protocol, transfer, and required progress cost from initiation until data is ready. Let W be useful independent work that would be required even without overlap. Let B be dependent work after completion. Serialized time is `C+W+B`. With perfect concurrency and no interference, time becomes `max(C,W)+B`.

Hidden time `H=T_ser-T_ov=min(C,W)` in the simple model. Exposed communication is `E=max(0,C-W)`. The overlap fraction relative to communication is `H/C` when C>0. Speedup is `T_ser/T_ov`. Initiation, packing, completion, and unpacking can be split out: only intervals truly concurrent are candidates for hiding.

The model fails when C and W change under concurrency. If both use memory bandwidth, concurrent durations can expand. A progress thread can reduce available compute cores; polling can lengthen W; network contention and rank skew can lengthen C. Measure the overlapped schedule directly and compare it with a structurally equivalent serialized schedule.

Arrival skew matters. Rank-local time from initiation to completion may mostly represent waiting for a peer to initiate. Report per-rank initiation timestamps in a synchronized/correlated trace where possible, or derive relative arrival distributions. Improving load balance may outperform communication tuning.

### Executable overlap bound

This exact arithmetic model calculates a serialized schedule and the ideal-progress/no-contention overlap bound for C=7, W=5, B=3. It does not execute communication, simulate progress, model contention/skew, or establish performance.

<!-- bijux-verify: {"id":"overlap-critical-path-bound","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"communication_ms=7\nindependent_work_ms=5\ndependent_work_ms=3\nserialized_ms=15\nideal_overlap_ms=10\nhidden_ms=5\nexposed_ms=2\noverlap_fraction=0.714286\nideal_speedup=1.500000\nweak_progress_without_calls_ms=15\n","stderr":""}} -->
```python
communication_ms = 7
independent_work_ms = 5
dependent_work_ms = 3
serialized = communication_ms + independent_work_ms + dependent_work_ms
ideal_overlap = max(communication_ms, independent_work_ms) + dependent_work_ms
hidden = serialized - ideal_overlap
exposed = max(0, communication_ms - independent_work_ms)
print(f"communication_ms={communication_ms}")
print(f"independent_work_ms={independent_work_ms}")
print(f"dependent_work_ms={dependent_work_ms}")
print(f"serialized_ms={serialized}")
print(f"ideal_overlap_ms={ideal_overlap}")
print(f"hidden_ms={hidden}")
print(f"exposed_ms={exposed}")
print(f"overlap_fraction={hidden / communication_ms:.6f}")
print(f"ideal_speedup={serialized / ideal_overlap:.6f}")
print(f"weak_progress_without_calls_ms={serialized}")
```

### Buffer, request, and language lifetimes

From initiation until completion, do not modify a send region or access a receive region contrary to MPI's rules. Derived datatypes, communicators, count/displacement arrays, operations, and persistent arguments also have specified lifetimes. Double or ring buffers assign each in-flight generation its own regions; a buffer returns to the producer only after the consuming operation completes.

Completion of a send releases the send buffer but does not generally prove remote receive or application processing. Completion of a receive makes received data/status available locally. Complete every request on normal, cancellation, timeout, and error paths as required; do not leak active requests or free bound persistent state.

Language compilers can move loads/stores unless the binding and program establish asynchronous access rules. In Fortran, use the modern `mpi_f08` interfaces and understand `ASYNCHRONOUS`/`MPI_ASYNC_PROTECTS_NONBLOCKING` conditions. In any language, library wrappers, garbage collectors, aliasing, and temporary objects must not move/free buffers while native operations hold them.

### Progress threads and thread support

A dedicated progress thread can call tests or be supplied by an MPI implementation. It needs the required MPI thread-support level, correct initialization, and no concurrent request misuse. Pin it deliberately; otherwise it may share a core with compute, migrate across NUMA nodes, or oversubscribe scheduler allocations. Record CPU affinity and thread count.

Strong progress can also come from NIC offload or transport workers, but capabilities vary by message protocol, datatype, collective, memory kind, and configuration. Small eager messages may appear asynchronous while large rendezvous transfers stall. Test sizes around protocol thresholds and direct/packed/device paths.

Progress consumes resources. Measure compute-only W with and without the thread/config, communication-only C, and the concurrent schedule. If W grows more than C is hidden, disable or retune. A low-priority thread can starve; a busy spin can waste power and steal execution. Blocking/yield/adaptive polling policies trade latency for resource use.

### Pipelining and partitioned communication

If one monolithic W cannot overlap enough, divide data into chunks. For each chunk, produce, mark/post/send, receive, and consume under a bounded pipeline. Steady-state throughput approaches the slowest stage, but fill/drain latency and contention remain. Choose chunk size: too small raises message, readiness, kernel, and request overhead; too large exposes latency and limits concurrency.

MPI partitioned point-to-point communication binds a persistent operation and allows multiple contributors to mark partitions ready; receivers can query arrival. It gives implementations flexibility and can connect tasks/threads to one message. It does not guarantee per-partition transfer/order or effective overlap: a conforming implementation may aggregate and defer. Prove partition readiness only after production, avoid duplicate readiness, keep the whole buffer/request valid, and benchmark the actual implementation.

Persistent point-to-point/collective/neighborhood operations can amortize setup for repeated fixed schedules. They do not create independent work or guarantee progress. Starting an active request, changing bound arrays, or reusing buffers early is erroneous.

### Collectives and asynchronous iterations

Nonblocking collectives can overlap local work and multiple communications, but every rank initiates compatible collectives in the same communicator order. Wait order need not define match order. Initiate only when local input is finalized and retain protected state. Too many outstanding collectives consume internal resources and can amplify congestion.

A global convergence reduction near every iteration often has little independent work after it. Options include moving truly independent preparation before the wait, combining reductions, pipelined numerical methods, or changing the algorithm. Such changes can affect numerical stability, convergence, and reproducibility and require separate analysis; calling `Iallreduce` immediately followed by wait does not help.

Speculative iterations that proceed with old/global-incomplete data are asynchronous numerical algorithms, not mere overlap. They need bounded staleness/convergence proofs and failure semantics, addressed later in the course.

### CPU-GPU-network overlap

An accelerator pipeline may include kernel production, device synchronization/event, device-to-host staging, MPI transfer, host-to-device copy, and consumer kernel. GPU-aware MPI may remove staging but still requires correct stream integration and support qualification. A nonblocking MPI call made before a producing kernel finishes can race unless the runtime is explicitly stream-aware or the application synchronizes with events/API contracts.

CUDA asynchronous calls return before work completes. Concurrent copy and kernel execution depends on device capability, pinned host memory for asynchronous host transfers, distinct streams where required, and no dependency/default-stream serialization. Copy engines, memory bandwidth, PCIe/NVLink, NIC, and kernels can contend. Trace device and CPU/network timelines with clock correlation.

Use buffer generations across all engines. Producer event authorizes communication/copy; communication completion authorizes consumer event/kernel. Never infer device visibility from host request completion without the supported integration contract.

### Bounding and failure handling

Every pipeline needs credits limiting messages, requests, partitions, buffers, pinned memory, device allocations, and speculative work. Unbounded issuance can exhaust MPI resources, increase tail latency, and turn one failed peer into a large cleanup problem. Backpressure should stop production before capacity is exceeded.

Timeout is an observation/policy trigger, not proof of a dead peer. Ordinary MPI failure recovery is not generally guaranteed. Define abort/checkpoint/restart or a separately supported fault model. Drain/complete/cancel requests only under documented semantics; do not publish partial generations. External side effects need generation IDs and deduplication.

### Measurement and verification

First prove output equivalence to the serialized reference across one/many ranks, message thresholds, polling frequencies, progress modes, thread affinities, pipeline depths, devices, and perturbations. Poison pending receive buffers and guard send buffers to expose illegal access. Run race/sanitizer tools where applicable.

Measure complete warm and steady iterations with identical input, output, algorithm, convergence, placement, I/O, and instrumentation. Record initiation, progress calls, completion, pack/unpack/copies, interior/dependent work, wait, arrival skew, hidden/exposed estimates, CPU utilization, memory bandwidth/cache, NIC/GPU/copy engines, requests/buffers high-water marks, and timing distributions/confidence.

Compare: serialized blocking/reference; nonblocking with immediate wait; independent work but no polling; bounded polling; progress thread/offload; pipeline depths; and reduced-communication algorithm. A trace must show temporal concurrency and a shorter verified critical path. Subtracting isolated C from total is insufficient when interference changes both.

## Definitions and Notation

- `C`: communication/progress duration in the modeled schedule.
- `W`: required dependency-independent useful work.
- `B`: communication-dependent boundary/finalization work.
- `T_ser=C+W+B`: serialized model time.
- `T_ov=max(C,W)+B`: ideal immediate-progress, no-contention bound.
- `H=T_ser-T_ov=min(C,W)`: ideally hidden time.
- `E=max(0,C-W)`: ideally exposed communication.
- `rho=H/C` for `C>0`: overlap fraction.
- `Q_i`: request for in-flight generation i.
- `buf_i`: buffer region owned by generation i.
- `p`: polling interval/chunk size.
- `d`: bounded pipeline depth.
- `A_r`: operation initiation time at rank r; its distribution represents arrival skew.
- `Obs`: serialized/overlapped result-equivalence contract.

These equations are conditional bounds; concurrency can change C, W, and B through contention and skew.

## Mechanisms, Invariants, or Proof Structure

### Dependency proof

Construct the DAG and show W has no path from incomplete receives/global results and writes no protected sends or shared objects. Every dependent consumer lies after the corresponding completion/event. Generation-specific buffers prevent cross-iteration aliasing.

### Progress and liveness proof

The program remains correct with weak progress: bounded work chunks eventually reach test/wait calls, matching peers/collectives initiate, request counts are bounded, and no circular dependency assumes background progress. Strong progress/offload is an optimization qualified per target.

### Lifetime and capacity proof

Buffers, datatypes, communicators, count arrays, operations, device events, and requests remain valid/protected until completion. Credits bound each resource; every path completes/releases exactly once; failure policy handles in-flight generations without partial publication.

### Critical-path proof

Under named no-contention/immediate-progress assumptions, derive `T_ov=max(C,W)+B`. Then measure concurrent C/W behavior, arrival skew, and full result timing; reject the model if resource interference or synchronization adds unmodeled edges.

### Equivalence and evidence proof

Serialized and overlapped executions consume the same generation inputs and apply the same numerical order/policy or an explicitly revalidated algorithm. Output/reference, conservation/error, and side-effect checks pass before performance comparison. Traces plus repeated distributions support—not replace—the dependency proof.

## Alternatives and Trade-Offs

| Approach | Main benefit | Principal limitation |
|---|---|---|
| blocking/reference schedule | simplest correctness/baseline | exposes all communication |
| nonblocking + final wait | flexible and deadlock-resistant | may make no progress during work |
| periodic polling | portable weak-progress opportunity | overhead and tuning |
| progress thread | background advancement | core/thread/NUMA/contention cost |
| NIC/runtime offload | low CPU progress cost | target/protocol dependent |
| persistent operations | amortized setup | fixed bound state |
| partitioned communication | producer partition readiness | implementation may aggregate/defer |
| chunked pipeline | steady-state hiding | fill/drain, buffers, small-chunk overhead |
| GPU streams/direct buffers | multi-engine concurrency | capability and synchronization complexity |
| reduce communication/synchronization | removes rather than hides cost | may require algorithm redesign |

Prefer the smallest schedule whose dependency proof is clear and whose complete verified critical path improves on the target.

## Failure Modes and Misconceptions

- **“Nonblocking means concurrent.”** it permits but does not require effective overlap.
- **“Initiation completes the transfer.”** buffer release and received-data availability require completion.
- **“Any local work is independent.”** derive dependencies and protected regions.
- **“MPI always progresses in the background.”** portable correctness assumes weak progress.
- **“More polling is safer and faster.”** correctness ends in wait; excessive polling can dominate.
- **“A progress thread is free.”** it consumes cores, bandwidth, cache, power, and thread support.
- **“Small-message behavior generalizes.”** eager/rendezvous and datatype/device paths differ.
- **“Interior time hides equal communication time.”** contention may lengthen both.
- **“Immediate wait is overlap.”** no useful work occupies the window.
- **“Outstanding operations are unlimited.”** requests/buffers/internal resources need credits.
- **“Persistent means asynchronous progress.”** persistence amortizes setup only.
- **“Partitioned means each partition transfers immediately.”** implementations may aggregate/defer.
- **“CUDA async guarantees device concurrency.”** streams, capability, pinned memory, and dependencies govern it.
- **“Request completion proves device visibility.”** integration contracts/events still govern memory spaces.
- **“Local elapsed time is network time.”** arrival skew and peer work contribute.
- **“A faster timing validates the algorithm.”** output/numerical/failure equivalence must pass first.

## Worked Examples

### Example 1

**Immediate wait.** Code calls `Irecv`, `Isend`, then `Waitall` before any work. It may avoid deadlock but exposes C entirely. **Conclusion:** asynchronous structure without independent work is not latency hiding.

### Example 2

**Unsafe interior.** A radius-two stencil labels points one cell from the cut “interior”; they read incomplete second ghosts. Shrink W to dependency-safe bounds. **Conclusion:** geometry must follow the actual operator.

### Example 3

**Weak progress.** A 100 ms compute kernel runs between start and wait; a large rendezvous message transfers only during wait. Periodic `Testsome` or qualified progress restores advancement. **Conclusion:** characterize and remain correct under weak progress.

### Example 4

**Polling granularity.** Testing every loop iteration adds 20 ms; testing every 1 ms leaves 2 ms exposed and costs 1 ms. The latter wins, but target changes require remeasurement. **Conclusion:** polling interval is a performance parameter, not a semantic guarantee.

### Example 5

**Progress-thread contention.** A rank receives four allocated cores but launches four compute threads plus one progress thread. Oversubscription lengthens W. Reserving/pinning one core or runtime offload improves total time. **Conclusion:** account for the progress engine as work.

### Example 6

**Late rank.** Rank 0's all-reduce request takes 12 ms; rank 7 initiates 10 ms late. The network is not necessarily slow. Balancing pre-reduction work removes most wait. **Conclusion:** measure arrival skew.

### Example 7

**Pipeline depth.** Depth one exposes transfer; depth four hides it; depth 64 exhausts pinned buffers and inflates tails. Credit-bound depth four is retained. **Conclusion:** concurrency has a capacity optimum.

### Example 8

**Partition readiness.** Tasks mark partitions ready after producing them, but one task calls readiness twice. Protocol validation rejects the duplicate; a conforming runtime may still send only after all are ready. **Conclusion:** readiness correctness and transfer behavior are distinct.

### Example 9

**GPU stream serialization.** A device-to-host copy and kernel use a stream order that makes the kernel wait, so no device overlap occurs. Independent data in distinct supported streams plus events produces concurrency. **Conclusion:** inspect the multi-engine DAG and trace.

### Example 10

**Real-time wildfire ensemble assimilation.** Overlap must preserve observation/model/mesh/time/ensemble generations, units, deterministic or bounded numerical policy, data authorization, deadline behavior, missing-member policy, restart lineage, uncertainty, and publication gates. Named wildfire science, meteorology, data-assimilation/statistics, geospatial, numerical/HPC, emergency-management, privacy/security, operations, quality/regulatory, accessibility/human-factors, ethics, and independent validation reviewers must approve evidence; none is claimed here. **Conclusion:** a shorter assimilation timeline does not establish forecast validity or safe public action.

## Cross-Program Connections

- **Algorithms:** DAG scheduling, span, pipelines, speculation, and communication-avoiding methods govern opportunity.
- **Operating systems:** threads, affinity, oversubscription, blocking, yielding, and timers govern progress engines.
- **Networks:** eager/rendezvous protocols, NIC offload, congestion, and collectives govern C.
- **Computer architecture:** bandwidth, cache, NUMA, DMA, PCIe/NVLink, and accelerators create contention.
- **Languages:** asynchronous buffer lifetimes, aliases, FFI, compiler movement, and task dependencies matter.
- **Numerical computing:** pipelined solvers, reduction order, staleness, convergence, and reproducibility constrain redesign.
- **Distributed systems:** backpressure, generations, timeouts, partial failure, and deduplicated side effects recur.
- **Testing:** poison, schedule perturbation, weak-progress modes, race tools, and reference equivalence expose defects.
- **Performance engineering:** traces, critical paths, skew, resource counters, distributions, and uncertainty establish claims.
- **Security/privacy:** in-flight buffers, staging, traces, dumps, and speculative work expand exposure.

## References

1. MPI Forum, *MPI: A Message-Passing Interface Standard, Version 5.0*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report.pdf>
2. MPI Forum, *MPI-5.0: Progress*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node50.htm>
3. MPI Forum, *MPI-5.0: Nonblocking Communication*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node73.htm>
4. MPI Forum, *MPI-5.0: Communication Completion*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node76.htm>
5. MPI Forum, *MPI-5.0: Partitioned Communication Introduction*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node88.htm>
6. MPI Forum, *MPI-5.0: Semantics of Partitioned Point-to-Point Communication*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node89.htm>
7. MPI Forum, *MPI-5.0: Problems with Code Movement and Register Optimization*, 2025. <https://www.mpi-forum.org/docs/mpi-5.0/mpi50-report/node486.htm>
8. PETSc Team, *Vectors and Parallel Data: Begin/End Communication*, PETSc 3.25 documentation; retrieved 2026-08-29. <https://petsc.org/release/manual/vec/>
9. PETSc Team, *DMGlobalToLocalBegin*, current documentation; retrieved 2026-08-29. <https://petsc.org/main/manualpages/DM/DMGlobalToLocalBegin/>
10. NVIDIA, *CUDA C++ Best Practices Guide: Asynchronous and Overlapping Transfers*, CUDA 13.3 documentation; retrieved 2026-08-29. <https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#asynchronous-and-overlapping-transfers-with-computation>

## Exercises

### Exercise 1

For C=12 ms, W=8 ms, and B=5 ms, derive serialized and ideal-overlap time, hidden/exposed time, overlap fraction, and ideal speedup. State assumptions.

### Exercise 2

Given a radius-three halo update on a local interval `[0,99]` with remote boundaries, identify the maximal dependency-independent interior for one time step and design a weak-progress-safe chunk/poll schedule.

### Exercise 3

Diagnose a code whose nonblocking version is 15% slower: it launches one progress thread per rank, uses all allocated cores for compute threads, polls in the main thread every 5 microseconds, and shares memory bandwidth with a large pack. Give an evidence-driven repair experiment.

### Exercise 4

Design a bounded CPU-GPU-network pipeline for four chunks, including producing kernels, device/host or direct MPI paths, partition readiness, consumer kernels, buffers/events/requests, progress, failure cleanup, and measurements.

### Exercise 5

Transfer the framework to an online radiotherapy adaptive-planning workflow with a strict deadline. Specify dependency, numeric/clinical/privacy/failure invariants, overlap evidence, publication gates, and named human reviewers without claiming review.

## Answers to the Exercises

### Answer 1

`T_ser=12+8+5=25` ms. Under immediate progress, perfect concurrency, unchanged C/W, and no extra overhead/contention, `T_ov=max(12,8)+5=17` ms. Hidden `H=8` ms; exposed `E=12-8=4` ms; fraction `rho=8/12=2/3≈0.666667`; ideal speedup `25/17≈1.470588`. These are bounds. Packing/initiation/completion, skew, weak progress, bandwidth contention, polling, and instrumentation can make actual time larger.

### Answer 2

A radius-three point at local index i is independent only when `i-3>=0` and `i+3<=99`, so indices `[3,96]` inclusive are safe if the owned interval and operator assumptions hold. Post exact receives then sends from immutable input, divide `[3,96]` into bounded compute chunks (for example measured 0.5–2 ms), and call `MPI_Testsome` between chunks. Tests may remain false; after all interior chunks call wait/validate, then compute `[0,2]` and `[97,99]`. Tune chunks by polling overhead/exposed time and verify with poisoned halos, varied message thresholds, and a final wait so correctness never assumes strong progress.

### Answer 3

The run is oversubscribed and duplicates progress work; pack, compute, and transfer contend for bandwidth. Establish serialized and nonblocking-immediate-wait baselines. Measure compute-only and communication-only durations, per-rank arrival skew, CPU affinity/utilization, memory bandwidth, polling cost, and timelines. Test mutually exclusive configurations: reserve/pin one allocated core for one progress thread and reduce compute threads; no progress thread with coarser bounded polling; implementation/NIC offload; and repacked/chunked work. Sweep polling interval and message thresholds. Retain only configurations with identical outputs and statistically lower complete iteration time; report resource allocation, versions, placement, and distributions.

### Answer 4

Allocate a credit ring of four (or fewer measured) generations, each with device producer/consumer regions, optional pinned staging regions, MPI partition/request, and events. Producer kernel for chunk i records readiness event. For staged MPI, an asynchronous D2H copy waits on it, host completion authorizes `Pready(i)`/send; for qualified stream-aware direct MPI, follow that contract instead. Post receive before readiness/send. Bounded polling/progress advances transfers. Receive completion or partition-arrival plus required H2D copy records a consumer event, and the consumer kernel waits on it. Never reuse a slot until kernel/copies/MPI complete. On failure, stop credits, complete/cancel only as supported, discard partial generation, zero/redact buffers, and abort/restart. Measure production, copies, readiness, network, polling CPU, arrivals, consumption, engine concurrency, contention, high-water memory/requests, fill/drain, output equivalence, and end-to-end distributions against serialized and no-staging alternatives.

### Answer 5

The DAG must ensure image acquisition/registration/segmentation/model inputs and dose computations are version-final before corresponding communication, while independent preparation cannot read incomplete plan/dose results. Bind buffers and messages to patient pseudonym, image/registration/contour/prescription/model/time/decomposition generations and units. Prove protected lifetimes, deterministic or bounded numerical behavior, dose/objective/reference agreement, deadline fallback, authorized placement/encryption/redaction, bounded pipeline resources, complete audit, and no partial publication. Test delayed/missing/corrupt inputs, weak progress, device/transport modes, deadline exhaustion, rank/device failure, restart, numeric extremes, and independent clinical reference cases. Compare verified complete latency and tails, not initiation. Publication requires named radiation oncologist, medical physicist/dosimetrist, imaging/registration, numerical/HPC, privacy/security, operations, quality/regulatory, ethics, accessibility/human-factors, and independent clinical safety reviewers. No external review, approval, or clinical validity is claimed.
