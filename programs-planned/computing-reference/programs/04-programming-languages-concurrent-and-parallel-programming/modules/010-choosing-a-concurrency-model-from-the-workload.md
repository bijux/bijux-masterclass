---
module_id: CONPAR-010
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 10
title: Choosing a Concurrency Model from the Workload
status: complete
last_verified: 2026-08-29
---

# Choosing a Concurrency Model from the Workload

## One-Page Review

### Governing question

Which concurrency model makes the workload's dependencies, state ownership, waiting, failure, resource topology, and service objectives easiest to express correctly—and which measurements could falsify that choice before it becomes architecture?

### Essential definitions

- A **workload** is the operations, inputs, arrival process, dependencies, state, resource demands, and service objectives a system must support.
- **Concurrency** structures overlapping progress; **parallelism** executes work simultaneously. A workload can need either, both, or neither.
- **Work** (W) is total computation on one ideal processor; **span** (S) is the longest dependency chain. Average parallelism is (W/S).
- **Task parallelism** assigns distinct dependent or independent activities to tasks; **data parallelism** applies similar operations across partitions.
- **Shared-memory threads** communicate through shared addresses and synchronization; **message ownership** communicates through explicit values and owners.
- **Asynchronous tasks** suspend rather than occupy an execution thread while awaiting supported operations; async does not make CPU work parallel.
- **Pipeline parallelism** overlaps stages on different items; throughput is limited by the bottleneck stage and capacity policy.
- **Distributed-memory parallelism** partitions data and communicates explicitly across processes or nodes, accepting higher latency and partial-failure concerns.
- **Granularity** is useful work per scheduling, synchronization, or communication event.
- **Operational intensity** relates useful computation to data movement and helps distinguish compute-bound from bandwidth-bound work.
- A **model-selection hypothesis** states the expected correctness, latency, throughput, scaling, and operational consequences of one design under declared conditions.

### Central model, mechanism, or theorem

For (P) processors, any schedule satisfies (T_P >= max(W/P,S)). This work–span lower bound says processors cannot beat either total-work capacity or the critical dependency chain. If serial fraction (f) remains fixed, Amdahl's ideal speedup bound is:

(Speedup(P) <= 1 / (f + (1-f)/P)).

These are upper bounds, not forecasts: scheduling, communication, contention, memory bandwidth, imbalance, I/O, failure handling, and coordination add cost. Model choice therefore begins with the dependency and ownership graph, then uses measurement to test an explicit hypothesis.

### Critical invariants

Correctness requirements precede speedup. The chosen model has one clear state authority. Blocking operations do not occupy scarce executors unexpectedly. Capacity and terminal accounting are bounded. Task lifetime and cancellation are structured. Parallel partitions preserve domain invariants. Ordering scope is explicit. Resource topology and data movement are measured. Benchmarks include correctness checks, warmup, variance, saturation, and realistic skew. Baselines include a simple sequential design. Model-specific complexity must purchase a measured benefit.

### Common failures

Teams choose async because traffic is high though work is CPU-bound; add threads around a bandwidth-saturated loop; use actors for state that requires constant cross-owner transactions; place blocking calls on an event loop; split tiny tasks below scheduling overhead; launch one task per item without admission control; move to processes without budgeting serialization; move to a cluster before one-node profiling; benchmark only uniform happy paths; tune thread count from core count while ignoring blocking and quotas; or combine every model before one has a proved responsibility.

### Compact example

An image transform has independent tiles, high compute per byte, immutable input, and associative aggregation. Data-parallel tasks or an accelerator are plausible. A chat-room membership service has mutable per-room state, ordered commands, and many waiting connections; sharded owners plus async I/O fit better. A shared-memory thread pool is possible for both, but it hides the first workload's regular bulk structure and the second workload's state authority.

### Connections

[Message Passing and Ownership Transfer](009-message-passing-and-ownership-transfer.md) supplies explicit authority; [Critical Sections and Shared-State Invariants](008-critical-sections-and-shared-state-invariants.md) supplies shared-memory proof; [Determinism and Reproducibility](007-determinism-and-reproducibility.md) supplies measurement comparators. The [program roadmap](../ROADMAP.md) now proceeds from this model-selection foundation into threads, synchronization, memory models, async systems, and parallel decomposition.

## Governing Question

Given a real workload rather than a preferred tool, how should engineers select, combine, and validate concurrency mechanisms so that the design exposes domain structure, preserves correctness, scales within physical limits, and remains operable under overload and failure?

There is no universally best model. The durable choice makes the most important dependencies and ownership rules explicit, supplies required progress and isolation, and incurs costs justified by measured demand. A hybrid is valuable only when each boundary has a stable responsibility.

## Why This Matters

Concurrency architecture hardens quickly. Once public APIs return futures, actors own state, queues define overload, data is sharded, or kernels target an accelerator, changing models affects error handling, testing, observability, and deployment. Choosing from fashion or syntax can create years of accidental complexity.

Workloads differ along several independent axes. Thousands of sockets spend most time waiting. A numerical kernel performs dense arithmetic over regular arrays. A compiler build is a dependency graph of medium-sized processes. A trading engine owns ordered state under a latency budget. A video pipeline has stages with different device affinities. A simulation partitions a domain across nodes because memory exceeds one machine. “It needs concurrency” does not identify the model.

Correctness and performance interact. Shared-memory access can minimize copy cost but expand interference. Message ownership simplifies invariants but adds queues and transfer. Async I/O supports many waits with few threads but blocking one executor can stall unrelated work. Fine tasks improve balance until overhead dominates. Distribution provides capacity and isolation but introduces serialization, network variability, and partial failure.

The right process is empirical without being benchmark-driven. Derive a candidate from dependencies and authority, create a simple correctness-preserving baseline, identify the expected bottleneck, state measurable predictions, and test representative load. A faster microbenchmark cannot justify a model whose cancellation, overload, or state semantics are wrong.

## Prerequisites and Retrieval

Retrieve:

- concurrency, parallelism, asynchrony, processes, threads, tasks, and fibers from modules [001](001-concurrency-parallelism-and-asynchrony.md) and [002](002-processes-threads-tasks-and-fibers.md);
- work graphs and state-space limits from [Interleavings and State-Space Explosion](003-interleavings-and-state-space-explosion.md);
- safety, progress, race, deadlock, and determinism from modules [004](004-safety-liveness-and-progress.md) through [007](007-determinism-and-reproducibility.md);
- shared-state invariants and message ownership from modules [008](008-critical-sections-and-shared-state-invariants.md) and [009](009-message-passing-and-ownership-transfer.md);
- directed acyclic graphs, critical paths, rates, queues, percentiles, and confidence intervals; and
- computer architecture basics: cores, caches, memory bandwidth, NUMA, vector units, accelerators, storage, and networks.

Retrieval prompt: for one familiar application, draw the dependency graph for a request, label mutable state owners, mark blocking and CPU work, estimate item size and arrival rate, and name the externally visible ordering and failure requirements. Do not name a framework yet.

## Learning Objectives

After completing this module, a learner can:

1. characterize a workload by dependencies, state, waiting, computation, data movement, failure, and objectives;
2. apply work–span, Amdahl, Little, granularity, and bandwidth reasoning without treating bounds as forecasts;
3. compare threads, async tasks, message owners, fork–join, data parallelism, pipelines, processes, and distributed memory;
4. identify blocking mismatches, oversubscription, unbounded admission, and ownership fragmentation;
5. define a model-selection hypothesis with falsifiable correctness and performance predictions;
6. design representative experiments across load, skew, topology, overload, cancellation, and failure;
7. introduce hybrid boundaries with one stable responsibility each;
8. plan an incremental transition with baseline, compatibility, observability, and rollback; and
9. bound high-consequence architecture recommendations that require named authorized review.

## Core Exposition

### Characterize before choosing

Build a workload dossier with evidence:

1. **Operations and arrivals:** request types, rates, bursts, concurrency, deadlines, and priorities.
2. **Dependency graph:** independent tasks, critical path, joins, loops, and feedback.
3. **State topology:** immutable inputs, shared mutable invariants, natural owners, partitions, and cross-partition transactions.
4. **Resource demand:** CPU cycles, blocking time, memory capacity, bandwidth, cache behavior, device and network use.
5. **Granularity:** useful work per task, message, synchronization, and transfer.
6. **Semantics:** ordering, determinism, cancellation, idempotency, delivery, and terminal results.
7. **Failure boundary:** what must survive task, process, node, or device failure.
8. **Service objective:** throughput, latency percentiles, jitter, cost, energy, and availability.

Measure distributions, not only means. A rare large item can dominate span. One hot key can defeat even sharding. A 1% blocking path can exhaust a small event-loop executor if it blocks long enough. Averages hide queue buildup and tail latency.

Separate intrinsic dependencies from implementation artifacts. A global mutex may serialize work today without being a domain requirement. Conversely, two functions that look independent may update one conservation invariant. Draw the logical graph first, then annotate current constraints.

### Quantitative bounds

Work–span reasoning supplies a ceiling. With total work (W) and span (S), parallelism beyond roughly (W/S) has no ideal benefit for that input. Brent's theorem relates a greedy schedule to work and span, while practical overhead adds task creation, synchronization, cache misses, and imbalance.

Amdahl's law models a fixed serial fraction. With (f=0.25), infinite ideal processors cannot exceed 4x speedup. It prevents promises like “eight cores means eight times faster.” Gustafson's scaled-speedup view asks a different question: as processors grow, can the problem size grow while elapsed time remains useful? State which workload scaling assumption applies.

Little's law relates average number in a stable system (L), arrival/throughput rate (lambda), and average time (R): (L=lambda R). If 2,000 operations per second spend 50 milliseconds in the system, average in-flight population is 100. This helps size concurrency and expose impossible latency/throughput/capacity combinations. It assumes a stable observation boundary; it does not prescribe queue capacity or tail behavior.

Data movement often dominates compute. Arithmetic intensity, working-set size, cache misses, NUMA placement, serialization bytes, and network collectives can set the limit. Adding workers to a saturated memory channel usually increases contention. Measure bandwidth and locality rather than labeling every slow loop “CPU-bound.”

### Shared-memory threads

Choose threads when tasks need low-latency access to shared address-space data, blocking libraries are unavoidable, state fits one process, and invariants have manageable synchronization. They work well for coarse tasks, legacy synchronous APIs, and shared caches when ownership and contention are explicit.

Costs include races, deadlock, oversubscription, stack/runtime overhead, cache coherence, and failure sharing. Thread count is not simply core count. CPU-bound runnable work often targets available execution capacity; blocking workloads need either more threads within budgets or nonblocking operations. Foreign runtimes and libraries may create their own pools, causing nested oversubscription.

Use a bounded executor, structured task lifetime, and one synchronization policy per invariant. Measure runnable count, blocked count, queue age, lock wait, context switches, CPU utilization, and memory bandwidth.

### Async tasks and event loops

Choose async when there are many logically concurrent operations that spend substantial time awaiting APIs with genuine nonblocking support, while per-event CPU work is short and bounded. Suspension releases an execution thread; it does not accelerate CPU work.

An event loop requires a “do not block” invariant. Synchronous DNS, filesystem, foreign-function, logging, or lock acquisition can violate it. Offload blocking work to a bounded dedicated executor and propagate backpressure. CPU-heavy callbacks need a compute pool or data-parallel model.

Async introduces cancellation, task leakage, context propagation, error aggregation, and executor affinity. Structured concurrency ties child lifetime to a scope and makes terminal accounting visible. Measure loop lag, ready-queue age, suspension count, blocking detector events, and executor saturation.

### Message owners and actors

Choose message ownership when mutable state partitions naturally by entity or key, commands benefit from serialization, and explicit queues are acceptable. One owner can maintain invariants without callers sharing its representation. Actors additionally package state, behavior, and mailbox.

This fit weakens when most operations require atomic transactions across many owners, messages are extremely fine-grained, or queue latency violates objectives. A hot owner becomes a bottleneck. Rebalancing changes routing and ownership epochs. Bounded mailboxes and explicit overload are mandatory.

Measure mailbox occupancy and age, per-owner utilization, hot-key skew, cross-owner message count, retries, and terminal outcomes. Do not assume actors remove shared runtime resources or distributed failures.

### Fork–join and work stealing

Choose fork–join for recursive or DAG-shaped CPU work whose subproblems become independent and whose joins express the span. Work stealing gives idle workers access to ready tasks and has strong theoretical bounds for suitable fully strict computations. It often balances irregular divide-and-conquer workloads without central scheduling.

Tasks must be large enough to amortize spawn, deque, synchronization, and cache costs. Cut off recursion to sequential kernels. Blocking inside a fixed compute pool can starve required tasks unless the runtime compensates under a documented policy. Avoid nested pools.

Measure work, span proxy, steals, task size, queue depth, worker utilization, join wait, and locality. Compare with the best sequential algorithm, not a deliberately weak baseline.

### Data parallelism and accelerators

Choose data parallelism when similar operations apply across many elements with limited cross-element dependence. SIMD, parallel loops, vector libraries, GPUs, and other accelerators exploit regular bulk structure. Reduction operations need algebraic and numerical semantics.

Accelerator fit requires enough computation to amortize launch and transfer, suitable memory access, sufficient parallel items, and supported control flow. Device memory capacity, host-device transfer, kernel occupancy, divergence, and numerical differences matter. A small irregular graph walk may lose to one CPU core.

OpenMP 6.0 supports user-directed shared-memory, tasking, work-distribution, SIMD, and device constructs, but its specification does not relieve developers of dependency, race, or deadlock correctness. Use model features only after the algorithm supplies legal independence.

### Pipelines

Choose a pipeline when work has stable stages, different items can overlap, and stages have distinct resource affinities. Steady-state throughput is limited by the slowest effective stage. Latency includes all stages and queues. Capacity between stages controls burst absorption and backpressure.

Balance by replicating a parallelizable bottleneck, fusing tiny stages, batching transfers, or changing algorithms. Replication can violate ordering or state ownership. A serial bottleneck cannot be fixed by adding workers elsewhere.

Measure per-stage service distributions, utilization, queue occupancy/age, batch size, drop/retry, and end-to-end terminal accounting. Test shutdown with items in every stage.

### Processes and distributed memory

Choose processes for fault and resource isolation, incompatible runtimes, privilege boundaries, or explicit memory ownership. Costs include serialization, copies, IPC, startup, and lifecycle. Shared memory between processes reintroduces synchronization and recovery.

Choose distributed memory when data or computation exceeds one node, locality can be partitioned, and the algorithm can tolerate network coordination and node failures according to its environment. MPI 5.0 is a current portable message-passing standard for C and Fortran programs across parallel platforms; using MPI does not make a poorly partitioned algorithm scale.

Measure communication volume, message size, collective cost, imbalance, synchronization, topology, stragglers, and failure/restart behavior. Strong scaling fixes problem size and increases resources; weak scaling grows problem size with resources. Report which experiment is used.

### Hybrid models with owned boundaries

Real systems combine models: async network admission, sharded message owners, a bounded CPU pool, vector kernels, and process isolation. A hybrid is coherent when every boundary names its role:

- async owns waiting and request lifetime;
- an actor owns mutable entity state;
- a compute pool owns blocking or CPU tasks;
- a data-parallel kernel owns bulk array transformation;
- a process boundary owns isolation; and
- distributed messages own cross-node data exchange.

Avoid arbitrary layering. Each crossing needs capacity, cancellation, context, ownership, error, ordering, and observability. Count total parallelism across nested libraries to prevent oversubscription.

### Form and test a selection hypothesis

Write a candidate claim:

> Under input distribution D and load range R, model M preserves invariants I and ordering O, bounds admitted work by B, meets latency/throughput objective Q on topology H, and fails through explicit outcomes F.

Then list falsifiers. A blocking call on the event loop, mailbox age above budget, memory bandwidth saturation below target, cross-shard rate exceeding prediction, cancellation leak, or incorrect numerical reduction can reject the model.

Build a sequential or simple bounded baseline first. Use representative input sizes, skew, bursts, cold/warm state, failure, and overload. Measure end-to-end outcomes as well as isolated kernels. Preserve seeds, versions, topology, and raw results under `artifacts/`. Report confidence intervals or distributions rather than one best run.

## Definitions and Notation

Let workload dependency DAG be (G=(V,E)). Each vertex has work cost (w(v)), resource demand, state owner, and failure behavior. Total work is (W=sum_v w(v)); span (S) is the maximum weighted path. Ideal average parallelism is (W/S).

For serial fraction (f) and processors (P), Amdahl bound is (A(P)=1/(f+(1-f)/P)). For stable observation boundary, Little's law is (L=lambda R). These models require declared measurement boundaries and assumptions.

Let candidate model (M) have overhead function (H_M), data movement (D_M), contention (C_M), and failure cost (F_M). Actual time is not determined by simply adding abstract symbols; these name quantities to measure and compare.

A selection hypothesis is a falsifiable tuple (D,R,M,I,O,B,Q,H,F). A benchmark result is evidence only for its declared workload, implementation, environment, comparator, and uncertainty.

## Mechanisms, Invariants, or Proof Structure

Use this workflow:

1. **Specify correctness and service objectives.** Include ordering, cancellation, overload, and failure.
2. **Draw dependencies and ownership.** Separate inherent constraints from current implementation.
3. **Measure resource behavior.** CPU, wait, memory, bandwidth, locality, device, and network.
4. **Compute bounds.** Work–span, serial fraction, in-flight population, capacity, and data movement.
5. **Choose the simplest fitting model.** Match its semantics to dominant structure.
6. **Define every boundary.** Admission, task lifetime, state authority, transfer, and terminal result.
7. **Write predictions and falsifiers.** Avoid untestable “should scale” claims.
8. **Implement a baseline and prototype.** Preserve the same correctness oracle.
9. **Test representative variation.** Size, skew, burst, topology, overload, cancellation, and failure.
10. **Adopt incrementally.** Instrument, compare, retain rollback, and re-evaluate as workload changes.

Maintain these invariants:

- the model exposes rather than obscures state authority and dependency;
- async executors never block on undeclared operations;
- admitted tasks, messages, buffers, and retries remain bounded;
- nested concurrency respects one total resource budget;
- data-parallel transformations preserve dependency and reduction semantics;
- process and node boundaries specify serialization and failure;
- benchmarks retain identical correctness oracles and representative inputs;
- claims state strong versus weak scaling and topology;
- hybrid boundaries have one stable responsibility; and
- model complexity is retained only with measured benefit.

## Alternatives and Trade-Offs

**Sequential execution** is the reference for simplicity, determinism, and overhead. It is often correct for small workloads and is the essential performance baseline.

**Threads** minimize in-process sharing cost but require synchronization and share failure. **Processes** strengthen isolation and ownership at serialization and lifecycle cost.

**Async tasks** scale waiting operations with modest thread count. They require nonblocking dependencies and disciplined cancellation. A larger blocking pool is simpler for moderate concurrency but consumes stacks and scheduler capacity.

**Actors and channels** make state authority and backpressure visible. They add message allocation, queue latency, and cross-owner transaction complexity. Shared locks can be more direct for small tightly coupled state.

**Fork–join** balances irregular CPU DAGs. **Static partitioning** improves locality and predictability when work is regular. Work stealing trades some locality for balance.

**CPU data parallelism** avoids device transfer and handles moderate irregularity. **Accelerators** provide throughput for regular high-intensity kernels but add separate memory, launch, tooling, and numerical constraints.

**One-node optimization** reduces operational complexity. **Distributed memory** expands capacity and aggregate compute while adding network, topology, partition, collective, and recovery costs.

## Failure Modes and Misconceptions

- **“I/O-bound means async.”** Only supported nonblocking operations benefit; CPU and blocking dependencies need separate capacity.
- **“CPU-bound means one thread per core.”** Memory bandwidth, vectorization, NUMA, blocking, and other pools alter the optimum.
- **“More concurrency improves throughput.”** Past saturation it raises queues, contention, and tail latency.
- **“Amdahl predicts runtime.”** It is an ideal bound under a fixed serial fraction.
- **“Actors scale automatically.”** Hot owners and cross-owner protocols can dominate.
- **“GPUs accelerate parallel code.”** Transfer, size, divergence, and memory behavior decide.
- **“Processes eliminate races.”** Shared stores, files, protocols, and shared memory retain coordination.
- **“A cluster fixes a slow algorithm.”** Communication and imbalance can make it worse.
- **“Hybrid means flexible.”** Unowned boundaries and nested pools create hidden complexity.
- **“Average latency sizes the system.”** Bursts and tails govern capacity and objectives.
- **“The benchmark winner is the architecture.”** Correctness, failure, overload, maintainability, and representative variation matter.
- **“A model choice is permanent.”** Workload distributions and hardware change; hypotheses need reevaluation.

## Worked Examples

### Example 1

**Question:** Ten thousand connections mostly wait on sockets; handlers do short bounded CPU work.

**Reasoning:** Waiting dominates and APIs are nonblocking. Per-request thread stacks are unnecessary.

**Conclusion:** Structured async admission plus a bounded CPU offload pool is a strong candidate.

### Example 2

**Question:** A dense transform applies the same arithmetic to millions of contiguous elements.

**Reasoning:** Dependencies are regular, parallelism is abundant, and operational intensity can amortize vector/device execution.

**Conclusion:** Measure SIMD, parallel loops, and accelerator kernels against transfer and bandwidth.

### Example 3

**Question:** Commands mutate one account, with rare two-account transfers.

**Reasoning:** Per-account ownership serializes common operations; cross-owner transfers need a distinct protocol.

**Conclusion:** Sharded message owners may fit if hot keys and cross-account cost pass measurements.

### Example 4

**Question:** Recursive search creates irregular independent subtrees and joins their best results.

**Reasoning:** A DAG with unpredictable subtree cost suits dynamic task balance.

**Conclusion:** Fork–join with work stealing and a sequential cutoff is a candidate.

### Example 5

**Question:** A three-stage media workflow uses CPU decode, GPU transform, and network upload.

**Reasoning:** Resources and work types differ by stage and items can overlap.

**Conclusion:** A bounded pipeline with stage-specific executors and end-to-end backpressure fits.

### Example 6

**Question:** Does eight processors imply eightfold speedup when serial fraction is 0.25?

**Reasoning:** Compute the ideal Amdahl bounds.

<!-- bijux-verify: {"id":"amdahl-model-selection-bound","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"workers=1 speedup_bound=1.000\nworkers=2 speedup_bound=1.600\nworkers=4 speedup_bound=2.286\nworkers=8 speedup_bound=2.909\ninfinite_worker_bound=4.000\n","stderr":""}} -->
```python
serial_fraction = 0.25
for workers in [1, 2, 4, 8]:
    bound = 1 / (serial_fraction + (1 - serial_fraction) / workers)
    print(f"workers={workers} speedup_bound={bound:.3f}")
print(f"infinite_worker_bound={1 / serial_fraction:.3f}")
```

**Conclusion:** Eight ideal workers are bounded near 2.909x and infinity at 4x. This arithmetic does not estimate overhead, validate the serial-fraction measurement, choose hardware, or prove production scaling.

### Example 7

**Question:** A memory scan reaches peak bandwidth with four threads but slows with eight.

**Reasoning:** Compute units are not the limiting resource; extra workers increase contention.

**Conclusion:** Optimize locality, representation, vectorization, or traffic rather than adding threads.

### Example 8

**Question:** One-node data no longer fits memory, but partitions exchange only boundary summaries.

**Reasoning:** Capacity requires distribution and communication is limited relative to local work.

**Conclusion:** Distributed-memory decomposition is plausible; measure imbalance, collectives, and recovery.

### Example 9

**Question:** An async service calls a synchronous foreign library for 200 milliseconds on its event loop.

**Reasoning:** One handler occupies scarce executor capacity and delays unrelated ready tasks.

**Conclusion:** Use a bounded blocking executor, replace the library, or choose a thread/process model.

### Example 10

**Question:** Can benchmark superiority approve a concurrency design for an autonomous surgical robot?

**Reasoning:** Deadlines, hazards, device behavior, independence, human factors, certification, and fail-safe operation exceed throughput evidence.

**Conclusion:** No. Named authorized clinical, controls, safety, hardware, verification, and regulatory reviewers must approve the real architecture. No external review is claimed.

## Cross-Program Connections

- **Algorithms:** work, span, DAG scheduling, partitioning, locality, and reductions define exploitable parallelism.
- **Computer architecture:** caches, NUMA, SIMD, memory bandwidth, accelerators, and interconnects set physical limits.
- **Operating systems:** scheduling, threads, processes, I/O readiness, affinity, and isolation implement execution.
- **Distributed systems:** partitioning, message order, collectives, partial failure, and recovery shape node-scale models.
- **Cloud engineering:** quotas, autoscaling, managed queues, heterogeneous instances, and cost affect deployment.
- **Performance engineering:** experiment design, profiling, queueing, confidence intervals, and saturation validate hypotheses.
- **Software architecture:** ownership boundaries, API compatibility, observability, and rollback determine sustainable adoption.

## References

1. Gene M. Amdahl, “Validity of the Single Processor Approach to Achieving Large Scale Computing Capabilities,” *AFIPS 1967*, [doi:10.1145/1465482.1465560](https://doi.org/10.1145/1465482.1465560).
2. John L. Gustafson, “Reevaluating Amdahl's Law,” *Communications of the ACM* 31(5), 1988, [doi:10.1145/42411.42415](https://doi.org/10.1145/42411.42415).
3. Robert D. Blumofe and Charles E. Leiserson, “Scheduling Multithreaded Computations by Work Stealing,” *JACM* 46(5), 1999, [doi:10.1145/324133.324234](https://doi.org/10.1145/324133.324234).
4. Richard P. Brent, “The Parallel Evaluation of General Arithmetic Expressions,” *JACM* 21(2), 1974, [doi:10.1145/321812.321815](https://doi.org/10.1145/321812.321815).
5. John D. C. Little, “A Proof for the Queuing Formula: L = λW,” *Operations Research* 9(3), 1961, [doi:10.1287/opre.9.3.383](https://doi.org/10.1287/opre.9.3.383).
6. Samuel Williams, Andrew Waterman, and David Patterson, “Roofline: An Insightful Visual Performance Model,” *Communications of the ACM* 52(4), 2009, [doi:10.1145/1498765.1498785](https://doi.org/10.1145/1498765.1498785).
7. OpenMP Architecture Review Board, *OpenMP API 6.0*, November 2024, [official specification](https://www.openmp.org/specifications/) (retrieved 2026-08-29).
8. MPI Forum, *MPI: A Message-Passing Interface Standard 5.0*, June 2025, [official documents](https://www.mpi-forum.org/docs/) (retrieved 2026-08-29).
9. Maurice Herlihy et al., *The Art of Multiprocessor Programming*, second edition, Morgan Kaufmann, 2020.
10. David A. Patterson and John L. Hennessy, *Computer Organization and Design RISC-V Edition*, second edition, Morgan Kaufmann, 2021.

## Exercises

### Exercise 1

Characterize a web service with 20,000 mostly waiting connections, 5-millisecond CPU bursts, and one blocking dependency. Propose a model, capacities, measurements, and falsifiers.

### Exercise 2

A graph algorithm has large irregular frontiers and saturates memory bandwidth at six workers. Compare static partitions, work stealing, and an accelerator.

### Exercise 3

Use work–span and Amdahl reasoning for work 1,000 units, span 80 units, and measured serial fraction 0.1. State bounds and why neither predicts runtime.

### Exercise 4

Design a hybrid for image upload, validation, CPU decode, GPU inference, and per-user state update. Give every boundary one owner and overload policy.

### Exercise 5

A railway-control team reports lower average latency after replacing threads with actors. Assess the evidence and state where named authorized review is mandatory.

## Answers to the Exercises

### Answer 1

Structured async tasks fit the many waits if socket and main dependencies are genuinely nonblocking. Put the blocking dependency behind a bounded executor with admission propagated to requests. Size total accepted work from service objectives and measured wait distributions, not connection count alone. Measure event-loop lag, ready age, blocking duration, CPU saturation, queue occupancy, cancellation completion, and latency percentiles under bursts. Falsifiers include blocking on the loop, offload saturation below target, task leaks, unbounded queues, or worse tails than a bounded thread baseline.

### Answer 2

The bandwidth ceiling means extra execution units alone will not scale. Static partitions can maximize locality when frontier work is predictable; irregular frontiers may imbalance. Work stealing improves balance but can increase remote memory traffic and cache loss. An accelerator may help only if frontier representation, transfer, divergence, and bandwidth are favorable. Measure useful edges per byte, locality, skew, steal traffic, host-device transfer, and correctness on identical graphs. Improve layout or compression before adding workers past saturation.

### Answer 3

Average parallelism is (W/S=12.5), and (T_P >= max(1000/P,80)); even infinite processors cannot beat span 80 in the model. Amdahl with (f=0.1) bounds infinite speedup at 10 and, for example, eight workers at (1/(0.1+0.9/8)) approximately 4.706. The models use different inputs and assumptions. Neither includes scheduling, contention, bandwidth, imbalance, task overhead, or uncertainty in measured fraction; they constrain hypotheses rather than forecast actual runtime.

### Answer 4

Async admission owns network waiting and request lifetime; bounded storage capacity owns upload bytes. A validation stage rejects unsafe inputs. A bounded CPU pool owns decode tasks and buffers, then transfers batches to a GPU queue sized by device memory. The accelerator owns inference until result transfer. A per-user owner serializes state updates. Each crossing defines ownership, cancellation, error, ordering, context, and terminal accounting. Reject or delay admission at the first exhausted budget; do not let futures accumulate between stages. Measure all queue ages and end-to-end outcomes.

### Answer 5

Lower average latency is insufficient: compare tail latency, workload distribution, correctness, mailbox growth, hot routes, overload, cancellation, failure recovery, deadlines, and resource topology against an equivalent baseline. Preserve raw evidence and test worst-case operational scenarios. Model choice cannot establish safe route authority, timing, hardware behavior, hazard mitigation, independence, or certification. Named authorized railway systems, signaling, functional-safety, verification, human-factors, cybersecurity, and regulatory reviewers must approve those claims and deployment. This chapter claims no external review.
