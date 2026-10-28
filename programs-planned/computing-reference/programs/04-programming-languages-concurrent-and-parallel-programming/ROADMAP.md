# 04. Programming Languages: Concurrent & Parallel Programming

**Program code:** `CONPAR`

**Purpose:** Build precise, practical command of concurrency and parallelism across shared memory, asynchronous runtimes, actors, accelerators, and distributed-memory programming.

**Level-II professional outcome:** Ready to implement, debug, test, and optimize concurrent and parallel software using threads, async/await, actors, SIMD, OpenMP-style tasks, GPUs, and MPI-style message passing.

**Prerequisites:** Programming Languages & Semantics Level I; algorithms and data structures; basic computer architecture.

**Primary ownership:** language-level concurrency; synchronization; memory models; async programming; actors; task and data parallelism; lock-free programming; SIMD and GPU models; distributed-memory parallel programming; parallel performance.

**Explicit exclusions:** operating-system scheduler implementation (Program 22); distributed fault tolerance and consensus (Program 27); network protocol engineering (Program 24); general language semantics (Program 01).

## Level I — Undergraduate Core

Modules 001–050 establish the complete foundational model and canonical mechanisms.

### Block 01 — Concurrency Models and Correctness

| Module | Canonical chapter | Future file |
|---:|---|---|
| 001 | **Concurrency, Parallelism, and Asynchrony** | `001-concurrency-parallelism-and-asynchrony.md` |
| 002 | **Processes, Threads, Tasks, and Fibers** | `002-processes-threads-tasks-and-fibers.md` |
| 003 | **Interleavings and State-Space Explosion** | `003-interleavings-and-state-space-explosion.md` |
| 004 | **Safety, Liveness, and Progress** | `004-safety-liveness-and-progress.md` |
| 005 | **Race Conditions and Atomicity Violations** | `005-race-conditions-and-atomicity-violations.md` |
| 006 | **Deadlock, Livelock, and Starvation** | `006-deadlock-livelock-and-starvation.md` |
| 007 | **Determinism and Reproducibility** | `007-determinism-and-reproducibility.md` |
| 008 | **Critical Sections and Shared-State Invariants** | `008-critical-sections-and-shared-state-invariants.md` |
| 009 | **Message Passing and Ownership Transfer** | `009-message-passing-and-ownership-transfer.md` |
| 010 | **Choosing a Concurrency Model from the Workload** | `010-choosing-a-concurrency-model-from-the-workload.md` |

### Block 02 — Threads and Synchronization

| Module | Canonical chapter | Future file |
|---:|---|---|
| 011 | **Creating and Joining Threads** | `011-creating-and-joining-threads.md` |
| 012 | **Mutexes and Mutual Exclusion** | `012-mutexes-and-mutual-exclusion.md` |
| 013 | **Condition Variables and Predicate Waiting** | `013-condition-variables-and-predicate-waiting.md` |
| 014 | **Semaphores and Resource Counting** | `014-semaphores-and-resource-counting.md` |
| 015 | **Read-Write Locks** | `015-read-write-locks.md` |
| 016 | **Barriers, Latches, and Phasers** | `016-barriers-latches-and-phasers.md` |
| 017 | **Thread-Safe Queues** | `017-thread-safe-queues.md` |
| 018 | **Lock Ordering and Deadlock Prevention** | `018-lock-ordering-and-deadlock-prevention.md` |
| 019 | **Thread Pools and Bounded Work Queues** | `019-thread-pools-and-bounded-work-queues.md` |
| 020 | **Designing a Correct Multithreaded Component** | `020-designing-a-correct-multithreaded-component.md` |

### Block 03 — Memory Models and Atomics

| Module | Canonical chapter | Future file |
|---:|---|---|
| 021 | **Compiler and Processor Reordering** | `021-compiler-and-processor-reordering.md` |
| 022 | **Sequential Consistency in Shared Memory** | `022-sequential-consistency-in-shared-memory.md` |
| 023 | **Happens-Before Relations** | `023-happens-before-relations.md` |
| 024 | **Visibility and Publication** | `024-visibility-and-publication.md` |
| 025 | **Atomic Read-Modify-Write Operations** | `025-atomic-read-modify-write-operations.md` |
| 026 | **Compare-and-Swap Loops** | `026-compare-and-swap-loops.md` |
| 027 | **Acquire and Release Ordering** | `027-acquire-and-release-ordering.md` |
| 028 | **Relaxed Atomics** | `028-relaxed-atomics.md` |
| 029 | **False Sharing and Cache-Line Contention** | `029-false-sharing-and-cache-line-contention.md` |
| 030 | **Reasoning About a Weak-Memory Program** | `030-reasoning-about-a-weak-memory-program.md` |

### Block 04 — Asynchronous and Message-Driven Programming

| Module | Canonical chapter | Future file |
|---:|---|---|
| 031 | **Event Loops and Nonblocking Execution** | `031-event-loops-and-nonblocking-execution.md` |
| 032 | **Callbacks and Inversion of Control** | `032-callbacks-and-inversion-of-control.md` |
| 033 | **Futures and Promises** | `033-futures-and-promises.md` |
| 034 | **Async/Await State Machines** | `034-async-await-state-machines.md` |
| 035 | **Cooperative Scheduling** | `035-cooperative-scheduling.md` |
| 036 | **Cancellation and Timeouts** | `036-cancellation-and-timeouts.md` |
| 037 | **Structured Concurrency** | `037-structured-concurrency.md` |
| 038 | **Actor Mailboxes and Message Ordering** | `038-actor-mailboxes-and-message-ordering.md` |
| 039 | **Channels and Communicating Sequential Processes** | `039-channels-and-communicating-sequential-processes.md` |
| 040 | **Backpressure in Asynchronous Pipelines** | `040-backpressure-in-asynchronous-pipelines.md` |

### Block 05 — Parallel Decomposition and Execution

| Module | Canonical chapter | Future file |
|---:|---|---|
| 041 | **Task Parallelism and Dependency Graphs** | `041-task-parallelism-and-dependency-graphs.md` |
| 042 | **Data Parallelism and Bulk Operations** | `042-data-parallelism-and-bulk-operations.md` |
| 043 | **Fork-Join Computation** | `043-fork-join-computation.md` |
| 044 | **Parallel Loops and Reductions** | `044-parallel-loops-and-reductions.md` |
| 045 | **Work Partitioning and Granularity** | `045-work-partitioning-and-granularity.md` |
| 046 | **Load Balance and Scheduling Overheads** | `046-load-balance-and-scheduling-overheads.md` |
| 047 | **Work Stealing** | `047-work-stealing.md` |
| 048 | **Pipeline Parallelism** | `048-pipeline-parallelism.md` |
| 049 | **MapReduce as a Parallel Programming Pattern** | `049-mapreduce-as-a-parallel-programming-pattern.md` |
| 050 | **Measuring Speedup, Efficiency, and Scalability** | `050-measuring-speedup-efficiency-and-scalability.md` |

## Level II — Graduate and Professional Depth

Modules 051–100 add internals, difficult cases, production constraints, advanced theory, and independent technical judgment.

### Block 06 — Lock-Free and Nonblocking Programming

| Module | Canonical chapter | Future file |
|---:|---|---|
| 051 | **Obstruction-Free, Lock-Free, and Wait-Free Progress** | `051-obstruction-free-lock-free-and-wait-free-progress.md` |
| 052 | **Implementing a Lock-Free Stack** | `052-implementing-a-lock-free-stack.md` |
| 053 | **Lock-Free Queues** | `053-lock-free-queues.md` |
| 054 | **ABA Problems and Tagged References** | `054-aba-problems-and-tagged-references.md` |
| 055 | **Hazard Pointers** | `055-hazard-pointers.md` |
| 056 | **Epoch-Based Reclamation** | `056-epoch-based-reclamation.md` |
| 057 | **Read-Copy-Update as a Nonblocking Pattern** | `057-read-copy-update-as-a-nonblocking-pattern.md` |
| 058 | **Linearizability Proofs** | `058-linearizability-proofs.md` |
| 059 | **Contention Management in Nonblocking Algorithms** | `059-contention-management-in-nonblocking-algorithms.md` |
| 060 | **Deciding When Lock-Free Code Is Justified** | `060-deciding-when-lock-free-code-is-justified.md` |

### Block 07 — Transactional and Deterministic Concurrency

| Module | Canonical chapter | Future file |
|---:|---|---|
| 061 | **Software Transactional Memory** | `061-software-transactional-memory.md` |
| 062 | **Optimistic Concurrency and Validation** | `062-optimistic-concurrency-and-validation.md` |
| 063 | **Transactional Retry and Composition** | `063-transactional-retry-and-composition.md` |
| 064 | **Conflict Detection and Contention** | `064-conflict-detection-and-contention.md` |
| 065 | **Deterministic Parallel Execution** | `065-deterministic-parallel-execution.md` |
| 066 | **Deterministic Schedulers for Testing** | `066-deterministic-schedulers-for-testing.md` |
| 067 | **Immutable Snapshots and Multi-Version State** | `067-immutable-snapshots-and-multi-version-state.md` |
| 068 | **Parallel Functional Evaluation** | `068-parallel-functional-evaluation.md` |
| 069 | **Reproducible Randomness in Parallel Programs** | `069-reproducible-randomness-in-parallel-programs.md` |
| 070 | **Designing for Replayable Concurrency** | `070-designing-for-replayable-concurrency.md` |

### Block 08 — Vector, GPU, and Accelerator Programming

| Module | Canonical chapter | Future file |
|---:|---|---|
| 071 | **SIMD Execution and Vector Lanes** | `071-simd-execution-and-vector-lanes.md` |
| 072 | **Data Layout for Vectorization** | `072-data-layout-for-vectorization.md` |
| 073 | **Compiler Auto-Vectorization** | `073-compiler-auto-vectorization.md` |
| 074 | **Explicit Vector Intrinsics** | `074-explicit-vector-intrinsics.md` |
| 075 | **GPU Execution Grids, Blocks, and Warps** | `075-gpu-execution-grids-blocks-and-warps.md` |
| 076 | **GPU Memory Hierarchies** | `076-gpu-memory-hierarchies.md` |
| 077 | **Coalescing, Divergence, and Occupancy** | `077-coalescing-divergence-and-occupancy.md` |
| 078 | **Kernel Fusion and Data Movement** | `078-kernel-fusion-and-data-movement.md` |
| 079 | **Heterogeneous CPU-GPU Pipelines** | `079-heterogeneous-cpu-gpu-pipelines.md` |
| 080 | **Profiling and Optimizing an Accelerator Kernel** | `080-profiling-and-optimizing-an-accelerator-kernel.md` |

### Block 09 — Distributed-Memory Parallel Programming

| Module | Canonical chapter | Future file |
|---:|---|---|
| 081 | **Processes and Ranks in Distributed-Memory Programs** | `081-processes-and-ranks-in-distributed-memory-programs.md` |
| 082 | **Point-to-Point Message Passing** | `082-point-to-point-message-passing.md` |
| 083 | **Collective Communication** | `083-collective-communication.md` |
| 084 | **Domain Decomposition** | `084-domain-decomposition.md` |
| 085 | **Halo Exchange and Stencil Computation** | `085-halo-exchange-and-stencil-computation.md` |
| 086 | **Communication-Computation Overlap** | `086-communication-computation-overlap.md` |
| 087 | **Parallel I/O** | `087-parallel-i-o.md` |
| 088 | **Load Imbalance Across Nodes** | `088-load-imbalance-across-nodes.md` |
| 089 | **Bulk-Synchronous and Asynchronous Iterations** | `089-bulk-synchronous-and-asynchronous-iterations.md` |
| 090 | **Scaling a Parallel Program Across Multiple Nodes** | `090-scaling-a-parallel-program-across-multiple-nodes.md` |

### Block 10 — Advanced Parallel Engineering

| Module | Canonical chapter | Future file |
|---:|---|---|
| 091 | **Amdahl, Gustafson, and Work-Span Models** | `091-amdahl-gustafson-and-work-span-models.md` |
| 092 | **Roofline and Operational-Intensity Analysis** | `092-roofline-and-operational-intensity-analysis.md` |
| 093 | **NUMA-Aware Allocation and Scheduling** | `093-numa-aware-allocation-and-scheduling.md` |
| 094 | **Hybrid Threads, SIMD, GPU, and Message Passing** | `094-hybrid-threads-simd-gpu-and-message-passing.md` |
| 095 | **Concurrent Memory Allocators** | `095-concurrent-memory-allocators.md` |
| 096 | **Race Detection and Concurrency Sanitizers** | `096-race-detection-and-concurrency-sanitizers.md` |
| 097 | **Systematic Concurrency Testing** | `097-systematic-concurrency-testing.md` |
| 098 | **Tracing and Profiling Parallel Execution** | `098-tracing-and-profiling-parallel-execution.md` |
| 099 | **Failure Containment in Long-Running Parallel Jobs** | `099-failure-containment-in-long-running-parallel-jobs.md` |
| 100 | **Reviewing a Parallel Program for Correctness, Portability, and Scale** | `100-reviewing-a-parallel-program-for-correctness-portability-and-scale.md` |

## Completion standard

This program is complete only when all 100 future module files satisfy `MODULE_CONTENT_CONTRACT.md`. The roadmap itself is not course completion.
