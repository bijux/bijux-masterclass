---
module_id: CONPAR-048
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 48
title: Pipeline Parallelism
status: complete
last_verified: 2026-08-29
---

# Pipeline Parallelism

## One-Page Review

### Governing question

How can a computation overlap distinct processing stages across multiple items while preserving capacity, ownership, ordering, deterministic meaning, failure settlement, and honest latency and throughput claims?

### Essential definitions

- A **pipeline** decomposes work into ordered stages connected by explicit transfer boundaries.
- **Pipeline parallelism** runs different stages on different items at the same time.
- A **stage** owns a transformation, service-time distribution, concurrency limit, and input/output contract.
- **Initiation interval** is the time between admitting successive items; steady-state throughput is its reciprocal when the system is stable.
- **Item latency** is time from the declared admission boundary to that item's terminal output.
- A **bottleneck** is the stage or resource constraining sustainable throughput under the measured workload.
- **Fill** and **drain** are the transient periods before all stages are occupied and after admission stops.
- A **pipeline register**, channel, or queue transfers one item's ownership and may bound in-flight work.
- A **reorder buffer** retains out-of-order completions until the required order can be committed.
- A **bubble** is an unused pipeline opportunity caused by dependencies, imbalance, stalls, hazards, or missing work.

### Central model, mechanism, or theorem

For `k` single-server stages with deterministic service times `s_j`, infinite intermediate capacity, and independent items, the first item completes after `sum(s_j)`. Once filled, the initiation/completion interval cannot be smaller than `max(s_j)`, so ideal steady throughput is at most `1/max(s_j)`. For `n` items in the balanced special case `s_j=s`, makespan is `(k+n-1)s`, versus `nks` without overlap. Real queues, finite buffers, variability, shared resources, dependencies, batching, scheduling, and failures change the result.

### Critical invariants

Each admitted item has one stable identity, one owner at a time, and one terminal outcome. A stage consumes only values satisfying its input contract and publishes a complete output before transfer. Every boundary is bounded or has a proved finite input. Stage replication cannot introduce unsafe shared state. Required order is explicit and restored before ordered effects. Backpressure does not form a resource wait cycle. Cancellation and failure settle queued, running, replicated, partially transformed, and reordered items. Shutdown closes admission, drains or discards by policy, propagates edge closure, and joins every stage.

### Common failures

Engineers divide total work by stage count; report steady throughput as first-item latency; ignore fill and drain; create a stage for every function despite transfer overhead; use unbounded queues to hide imbalance; replicate a stateful stage without partitioning; mistake local FIFO queues for global order; let a reorder window grow without bound; make two stages contend for the same CPU, cache, accelerator, or connection; block all executors on full outputs; retry in every stage; commit external effects before downstream acceptance; or treat one fast benchmark as proof of production speedup.

### Compact example

Four independent items traverse stages of two, three, and one time units. Completion vectors are `[2,5,6]`, `[4,8,9]`, `[6,11,12]`, and `[8,14,15]`. The first item takes six units; subsequent items complete three units apart because stage two is the bottleneck; makespan is 15 rather than serial 24; and observed speedup is 1.6 for exactly this deterministic model. The trace proves neither concurrent implementation correctness nor behavior under finite buffers, variance, or shared resources.

### Connections

[Backpressure in Asynchronous Pipelines](040-backpressure-in-asynchronous-pipelines.md) governs finite capacity. [Work Partitioning and Granularity](045-work-partitioning-and-granularity.md) governs stage/transfer cost. [Load Balance and Scheduling Overheads](046-load-balance-and-scheduling-overheads.md) governs utilization claims. The [program roadmap](../ROADMAP.md) continues with MapReduce and quantitative scalability.

## Governing Question

How should engineers design, analyze, implement, verify, and operate a staged parallel computation so overlap improves useful throughput without changing meaning or concealing latency, memory, and lifecycle costs?

Pipeline parallelism is a dependency-preserving schedule over multiple items, not merely a chain of functions or queues.

## Why This Matters

Many systems naturally contain unlike operations: decode, validate, transform, infer, encode; fetch, parse, optimize, emit; read, decompress, analyze, write. A single item must visit these stages in order, yet different items can occupy different stages concurrently. That overlap can use heterogeneous resources, isolate ownership, and raise throughput without making every transformation internally parallel.

The pattern also creates obligations. Stage boundaries retain data. Replicas change ordering. A slow stage creates queues; a variable stage creates bubbles; an external-effect stage creates retry ambiguity. The pipeline can have excellent steady throughput while one item suffers unacceptable latency. It can appear parallel while every stage contends for one saturated resource. Correctness therefore requires explicit data, capacity, order, effect, cancellation, and termination contracts.

Pipelines appear in processors, media, compilers, streaming systems, machine-learning inference, databases, build systems, networks, and ordinary application code. The shared reasoning is valuable; the implementations differ. A CPU instruction pipeline's hazards and clocking are not identical to asynchronous application stages, and a distributed durable stream is not equivalent to an in-process bounded channel.

## Prerequisites and Retrieval

Retrieve:

- producer-consumer ownership from [Thread-Safe Queues](017-thread-safe-queues.md);
- stage coordination from [Channels and Communicating Sequential Processes](039-channels-and-communicating-sequential-processes.md);
- capacity feedback from [Backpressure in Asynchronous Pipelines](040-backpressure-in-asynchronous-pipelines.md);
- cancellation ownership from [Cancellation and Timeouts](036-cancellation-and-timeouts.md);
- task lifetime from [Structured Concurrency](037-structured-concurrency.md);
- useful grain from [Work Partitioning and Granularity](045-work-partitioning-and-granularity.md); and
- overhead attribution from [Load Balance and Scheduling Overheads](046-load-balance-and-scheduling-overheads.md).

Retrieval prompt: for a three-stage pipeline, name the owner of an item before, during, and after each transfer; then distinguish first-item latency, completion interval, makespan, and queueing delay.

## Learning Objectives

After completing this module, a learner can:

1. distinguish functional composition, pipeline parallelism, data parallelism, and task parallelism;
2. calculate deterministic fill, steady-state, drain, latency, interval, throughput, and makespan;
3. state the assumptions behind bottleneck and balanced-pipeline formulae;
4. choose stage boundaries using dependency, resource, state, and transfer costs;
5. size and place bounded buffers without confusing buffering with capacity creation;
6. replicate, fuse, batch, or repartition stages while preserving semantics;
7. preserve or deliberately relax order with bounded reordering;
8. specify cancellation, failure, retry, checkpoint, and shutdown behavior end to end;
9. instrument stage service, wait, occupancy, utilization, bubbles, and item age; and
10. design experiments that separate pipeline benefit from batching, caching, and resource contention.

## Core Exposition

### From a chain to an overlapped schedule

Suppose item `i` must undergo functions `f_1,...,f_k`, with output of `f_j` becoming input to `f_(j+1)`. Calling the functions sequentially is a chain. It becomes pipeline parallelism only when the implementation can advance different items in different stages concurrently. The dependency along one item remains; independence lies across items.

Each transfer needs a type and ownership contract. Does the producer move an immutable value, lend a buffer, or share a reference? When may it reuse memory? Can the receiver reject? Does successful send mean enqueued, durably accepted, or processed? Ambiguous boundaries cause data races and false acknowledgements.

Stage workers can be threads, tasks, processes, devices, vector units, or event-loop activities. The scheduling substrate matters less than the logical rule: a stage may claim only ready input, perform its declared transformation once under the chosen delivery semantics, and transfer or terminally settle the result.

### Deterministic timing model

Let stage `j` take deterministic time `s_j>0` per independent item and have one server. With unlimited buffers and no transfer cost, the completion recurrence is

`C(i,j)=max(C(i,j-1), C(i-1,j))+s_j`,

with missing predecessor completions treated as zero. The maximum expresses two prerequisites: item `i` finished the previous stage, and stage `j` finished the previous item. This recurrence is safer than memorizing one formula because it exposes both data dependence and resource exclusion.

The first item latency is `sum_j s_j`. Sustainable initiation interval cannot beat `b=max_j s_j`; ideal steady throughput cannot exceed `1/b`. For the special balanced case `s_j=s`, `n` items complete in `(k+n-1)s`: `k` slots fill the first item, then `n-1` additional items complete one per slot. Serial execution needs `nks`, so speedup approaches `k` only as `n` grows and only under the model.

For unequal stages, a unique slow stage waits less while faster stages accumulate idle slots. Total makespan for a simple deterministic line can often be derived by the recurrence; blindly using `sum(s_j)+(n-1)max(s_j)` is valid under this simple no-blocking, single-server line but not for arbitrary blocking, finite buffers, re-entrant routes, shared resources, or item-dependent costs.

### Latency, throughput, and finite workloads

Latency and throughput answer different questions. Overlap can improve completion rate while leaving first-item processing latency unchanged or increasing it through queues and transfers. A long stream amortizes fill and drain; a batch of one cannot. Interactive systems may prefer a fused low-latency path even when a staged path wins bulk throughput.

Makespan measures completion time for a declared finite set. Average item latency includes queueing and can grow while makespan improves. Tail latency reflects variability, head-of-line blocking, retries, and reordering. Always state workload size, admission pattern, boundaries, warm-up, drain, and percentiles.

Pipeline efficiency is sometimes defined as useful occupied stage capacity divided by available stage capacity. That number depends on whether stages are equally provisioned and whether time represents comparable resources. Adding CPU time and accelerator time without a resource model is misleading. Use per-resource utilization alongside end-to-end outcomes.

### Choosing stage boundaries

A durable stage boundary follows an independent responsibility, resource, state owner, or failure boundary. It should expose enough work to amortize enqueue, context, serialization, cache, and scheduling overhead. Splitting every small function produces queues and coordination without useful overlap. Fusing stages reduces transfers and latency but can reduce independent scheduling and heterogeneous placement.

Analyze data volume across the boundary. An early filter may shrink items before an expensive transfer; an early decoder may expand compressed inputs dramatically. Moving a large mutable object between cores can cost more than its transformation. Ownership transfer, cache behavior, allocation, and serialization belong in the stage cost.

Avoid cyclic dependency unless the protocol explicitly supports feedback. A linear pipeline is easier to terminate than a graph whose later stage injects work upstream. If feedback is necessary, model it as a bounded protocol with generation identity and a termination argument.

### Balance by replication, fusion, and partitioning

If stage `j` has service time `s_j` and `p_j` truly parallel replicas, a rough capacity is `p_j/s_j`. This assumes independent work, divisible routing, comparable replicas, and no shared bottleneck. The pipeline capacity is limited by the smallest stage capacity. Use measurements rather than treating the ratio as proof.

Replication is safe for stateless transformations or state partitioned by an explicit key. A mutable parser cache, sequence counter, model session, or device handle may not be freely replicated. Per-key routing can preserve state order but creates skew. Work stealing can balance independent tasks but may violate affinity or required item order unless integrated carefully.

Fusion combines adjacent stages when transfer dominates or they compete for the same resource. Fission splits a broad stage into separately provisioned responsibilities. Repartitioning changes the key or batch ownership boundary. Each transformation must preserve the semantic oracle, not merely benchmark faster.

### Buffers, backpressure, and bubbles

Intermediate buffers let adjacent stages tolerate short variability and work simultaneously. Capacity does not increase sustainable throughput; it stores the difference between arrival and service. An unbounded queue hides a bottleneck as memory and latency. A very small queue can increase producer blocking or reduce overlap. Select a finite count/byte/cost bound from burst, memory, latency, and recovery budgets.

Backpressure propagates downstream scarcity upstream. A producer must not hold a lock, worker, buffer pool slot, or device context that the consumer needs to release capacity. In synchronous thread pools, all workers can block sending to full downstream queues while no worker remains to drain them. Async suspension releases a thread but still owns memory and lifecycle state.

A bubble is an empty service opportunity. Causes include pipeline fill/drain, imbalance, data dependencies, branch hazards, cache misses, unavailable input, full output, cancellation, and scheduling delay. Some bubbles are necessary to preserve correctness. Measure and classify them before changing capacity or concurrency.

### Variable work and batching

Real stage times are distributions, often correlated with item size, key, or content. A slow item can block FIFO successors. Replication reduces some head-of-line effects but can create out-of-order completion. Size-aware routing may improve tails but risks starvation and prediction overhead. Heavy-tailed stages require tail measurements and bounded work, not average-only provisioning.

Batching amortizes calls, vectorizes computation, and raises device utilization. It also waits to form batches, increases failure scope, and changes ordering and cancellation granularity. Bound both batch size and formation delay. Charge capacity by retained bytes or cost, not just batch count. Report batching separately so its benefit is not mislabeled as pipeline overlap.

### Ordering and reordering

One worker per stage and FIFO edges often preserve order in a simple line. Replicated stages, variable latency, branches, retries, and asynchronous external calls do not. Decide whether global input order, per-key order, causal order, or no order is required.

To restore order, assign a monotonic sequence within the required domain and hold later completions until the next expected sequence arrives. The reorder buffer must be bounded. If one item stalls forever, choose a policy: wait within deadline, fail the stream, emit a gap marker, cancel later items, or relax order by contract. Silent indefinite retention is not a policy.

Deterministic meaning can survive nondeterministic schedules when each pure stage has deterministic input/output and ordered effects are committed through a stable protocol. Floating-point reductions, time reads, randomness, thread-local identity, and external effects need explicit policies.

### Branches, joins, and hazards

A pipeline may fork one item into independent branches and join their results. Register all branch obligations before publication so completion cannot race registration. Bound concurrent join state. Define behavior when one branch fails, is cancelled, or produces no value. Strict broadcast couples progress to the slowest subscriber; independent subscriber queues require independent lag policies.

Data hazards arise when items share mutable state. A read-after-write dependence may require ordering; write-after-write may require serialization or version selection; write-after-read can invalidate a borrowed view. Processor pipelines use forwarding, stalls, and speculation; application pipelines more often use ownership, versioned state, partitioning, or explicit barriers. The names transfer, but the implementation proof does not.

Speculation can compute later work before earlier validation commits. Bound speculative population and side effects. A discarded speculative result must release every buffer, permit, and child task. Never expose irreversible effects before the validation/ordering point unless compensation is part of the contract.

### Errors, retries, and exactly-once meaning

An exception at stage three does not say whether stages one and two may continue admitting. Choose fail-fast scope, per-item isolation, or error-as-data. Preserve original item identity and stage attempt identity. Terminal accounting must distinguish completed, rejected, cancelled, failed, and intentionally discarded items.

Retry belongs to one declared layer. Independent retries at several stages multiply work and reorder effects. A timeout does not prove an external call did not commit. Use idempotency keys or transactional protocols where effects require safe replay. “Exactly once” is an end-to-end claim involving effects and recovery, not proof that an in-memory queue removes each object once.

Checkpointing can reduce recomputation but adds consistency questions. A checkpoint must identify stage version, item identity, input provenance, owned state, and effect frontier. Restoring incompatible stage code or replaying beyond an unrecorded effect can corrupt results.

### Cancellation and shutdown

Cancellation is location-independent: an item may be waiting at any edge, running in a stage, awaiting a batch/reorder gap, or committed externally. The stage that owns it must either produce a transferable result or one terminal settlement. Cancellation of one item may cancel its branches; cancellation of the pipeline should stop new admission and propagate in the dependency direction required to unblock everyone.

Orderly shutdown closes admission, records the drain-or-discard policy, wakes blocked producers/consumers, closes edges after their producers terminate, settles pending reorder/join entries, reconciles external effects, and joins stage workers. Closing the first queue alone can strand downstream stages waiting forever; closing an edge while a producer can still send creates loss or panic.

Termination of a finite pipeline requires no admission, queued items, active transformations, in-transit transfers, pending retries/timers, branch obligations, reorder entries, or unsettled effects. Local empty queues are insufficient because a running stage can publish new work.

### Heterogeneous and distributed pipelines

Stages mapped to CPU, GPU, network, or storage can overlap genuinely different resources. Include host-device copies, synchronization, pinned buffers, kernel launch, serialization, and device queueing. Multiple “parallel” stages that saturate one memory channel will not achieve independent capacity.

Across processes, transfer becomes delayed and fallible. Delivery acknowledgements, durable ownership, duplicates, partitions, version compatibility, and recovery enter the contract. Network buffers and broker retention may decouple temporarily but do not remove end-to-end capacity limits. Distributed stream processing additionally needs watermark, event-time, state, checkpoint, and delivery semantics beyond this in-process foundation.

### Measurement and verification

Record per-item timestamps for admission, stage queue entry, start, finish, transfer, and terminal settlement. Derive service time, queue wait, transfer time, item latency, initiation/completion intervals, and makespan without double counting. Measure occupancy in count and bytes, oldest-item age, active replicas, blocked/suspended time, bubbles by cause, batch fill, reorder depth, retries, and outcomes.

Compare against a correct sequential baseline with identical algorithm, inputs, effects, warm-up, and output checks. Test multiple stream lengths to reveal fill/drain. Sweep capacities and replica counts. Use controlled stage delays and distributions; inspect CPU, cache, memory, accelerator, network, and storage utilization. Trace sampling overhead must be measured.

Deterministic tests use tiny capacities and controlled scheduling to force every full/empty/close/error transition. Property tests vary item count, cost, key skew, failures, and cancellation. Assert output equivalence, allowed order, one terminal outcome, bounds, no post-close send, and complete join. Model checking is appropriate for transfer and shutdown protocols. Passing tests establishes evidence for explored cases, not universal liveness or speedup.

## Definitions and Notation

Let there be `k` ordered stages and `n` admitted items. `s_(i,j)` is service time of item `i` at stage `j`; the deterministic homogeneous special case uses `s_j`. `C(i,j)` is completion time and obeys `C(i,j)=max(C(i,j-1),C(i-1,j))+s_(i,j)` for a one-server line.

First-item processing latency without queues is `L_1=sum_j s_j`. The bottleneck interval in the homogeneous ideal model is `b=max_j s_j`, yielding throughput upper bound `X<=1/b`. In the balanced case `s_j=s`, makespan is `M=(k+n-1)s` and serial time is `M_serial=nks`.

For edge `e`, `K_e` is finite capacity and `Q_e(t)` occupancy, with `0<=Q_e(t)<=K_e`. `R(t)` is reorder population. Total in-flight population includes queued, active, in-transfer, batched, retrying, joined, and reordered items.

Let `p_j` be replicas of stage `j`. The estimate `p_j/E[s_j]` is a capacity hypothesis only when work is independent and shared resources do not bind. `A`, `D`, and `T` denote cumulative admitted, deliberately discarded, and other terminally settled items; conservation requires every admitted identity to reach exactly one declared terminal category.

## Mechanisms, Invariants, or Proof Structure

Audit a pipeline in this order:

1. define item identity, input/output types, and the end-to-end semantic oracle;
2. draw stages, branches, joins, feedback, queues, batches, and reorder storage;
3. state readiness/dependency and one logical owner at every transition;
4. measure stage service distributions, transfer cost, and shared resources;
5. calculate recurrence-based ideal timing for a declared finite workload;
6. choose stage boundaries and fuse work below useful grain;
7. bound every queue, byte reservoir, batch, retry, join, and reorder window;
8. provision/replicate stages only where state and ordering permit;
9. define backpressure, overload, priority, and wait-for relationships;
10. settle errors, cancellation, retries, effects, closure, and termination exactly once;
11. verify order/equivalence and invariants under adversarial controlled schedules; and
12. benchmark against a matched sequential baseline while reporting fill, drain, tails, and resources.

The executable model calculates the recurrence for four items and three deterministic stages.

<!-- bijux-verify: {"id":"pipeline-timing-recurrence","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"stage_times=[2, 3, 1]\ncompletions=[[2, 5, 6], [4, 8, 9], [6, 11, 12], [8, 14, 15]]\nfirst_item_latency=6\nsteady_completion_interval=3\nbottleneck_time=3\npipeline_makespan=15\nserial_makespan=24\nspeedup=1.60\nall_items_complete=True\n","stderr":""}} -->
```python
stage_times = [2, 3, 1]
item_count = 4
completions = []

for item in range(item_count):
    row = []
    for stage, duration in enumerate(stage_times):
        prior_stage = row[stage - 1] if stage > 0 else 0
        prior_item = completions[item - 1][stage] if item > 0 else 0
        row.append(max(prior_stage, prior_item) + duration)
    completions.append(row)

first_item_latency = completions[0][-1]
completion_times = [row[-1] for row in completions]
intervals = [completion_times[i] - completion_times[i - 1] for i in range(1, item_count)]
pipeline_makespan = completion_times[-1]
serial_makespan = item_count * sum(stage_times)

print(f"stage_times={stage_times}")
print(f"completions={completions}")
print(f"first_item_latency={first_item_latency}")
print(f"steady_completion_interval={intervals[-1]}")
print(f"bottleneck_time={max(stage_times)}")
print(f"pipeline_makespan={pipeline_makespan}")
print(f"serial_makespan={serial_makespan}")
print(f"speedup={serial_makespan / pipeline_makespan:.2f}")
print(f"all_items_complete={len(completion_times) == item_count}")
```

Limitations: this arithmetic simulation has deterministic per-stage times, one server per stage, independent identical items, zero transfer/scheduling cost, unlimited intermediate capacity, no shared resources, no variability, no failures, no cancellation, no ordering repair, and no concurrency. It validates recurrence arithmetic, not a pipeline runtime or production speedup.

## Alternatives and Trade-Offs

- **Sequential fusion:** lowest transfer/lifecycle complexity and often best single-item latency; no cross-item stage overlap.
- **Data parallelism:** applies the same operation across partitions; better when stages are homogeneous rather than resource-distinct.
- **Task DAG scheduling:** handles irregular dependencies; adds scheduler/graph overhead and less explicit steady flow.
- **Pipeline stages:** expose resource and ownership boundaries; add queues, latency, and lifecycle coordination.
- **One worker per stage:** preserves simple local order; wastes capacity when stages are imbalanced.
- **Replicated stages:** raises capacity and absorbs variability; complicates state, order, affinity, and reordering.
- **Small buffers:** bound latency/population tightly; can create stalls under jitter.
- **Large buffers:** absorb bursts and decouple stages; retain more memory and stale work.
- **Fine stages:** independently placeable and observable; transfer/scheduling cost may dominate.
- **Fused stages:** improve locality and reduce queues; reduce scheduling flexibility and resource overlap.
- **Ordered output:** deterministic consumption and simpler effects; one straggler can block a bounded reorder frontier.
- **Unordered output:** lower head-of-line blocking; downstream must tolerate schedule-dependent order.
- **Batching:** amortizes/vectorizes; increases formation latency, retained population, and failure/cancellation scope.

## Failure Modes and Misconceptions

1. **“`k` stages mean `k`-fold speedup.”** Imbalance, finite `n`, overhead, and shared resources bound speedup.
2. **“Throughput is latency.”** Completion interval and one-item elapsed time are different metrics.
3. **“Queues make stages faster.”** Queues absorb timing differences; they do not add service capacity.
4. **“FIFO edges guarantee global order.”** Replicas, branches, retries, and external calls can reorder.
5. **“More stage replicas always help.”** State, skew, contention, and reorder pressure can dominate.
6. **“A full pipeline is efficient.”** Occupied workers may wait, contend, retry, or compute discarded work.
7. **“An empty queue means completion.”** Active stages and in-transit/branch work can publish later.
8. **“Timeout means the item did not commit.”** Effects may have completed beyond the observer.
9. **“Unbounded queues prevent blocking.”** They relocate overload to memory, age, and recovery time.
10. **“A sequential timing model proves concurrency.”** It checks arithmetic under assumptions only.

## Worked Examples

### Example 1

Three balanced stages each take four milliseconds for `n=10`. Serial makespan is `120 ms`; ideal pipeline makespan is `(3+10-1)4=48 ms`; ideal finite-batch speedup is `2.5`, not three. First-item latency remains 12 ms, and steady completions are four milliseconds apart. Any measured comparison must add actual transfer and scheduling costs to both paths consistently.

### Example 2

A camera pipeline decodes in 2 ms, filters in 7 ms, and encodes in 3 ms. The ideal bottleneck interval is 7 ms. Replicating decode cannot improve this bound. Two independent filter replicas suggest aggregate filter capacity above the encoder, but only if filters share no saturated memory bandwidth and output order is either irrelevant or restored within a bounded window.

### Example 3

A compiler chains lexing, parsing, optimization, and emission. Lexing and parsing share mutable source-position state and produce tiny transfers; fusing them may improve locality. Optimization contains independent functions and can be replicated by function identity. Emission requires deterministic symbol/order policy. The best boundary follows ownership and grain, not the conceptual chapter list.

### Example 4

A four-item recurrence with stage times `[2,3,1]` yields completion rows `[2,5,6]`, `[4,8,9]`, `[6,11,12]`, `[8,14,15]`. Stage two never waits after starting; faster stages exhibit bubbles. Fifteen-unit makespan versus 24 serial units is an arithmetic consequence of the declared model, not evidence that a threaded version will achieve 1.6 speedup.

### Example 5

An image-transform stage has service times proportional to pixels. Four replicas receive FIFO work, but one enormous image finishes after many later thumbnails. If output must follow input order, the reorder buffer retains those thumbnails. Bound it in bytes/count, detect the gap deadline, and decide whether to fail, gap, or cancel; adding unbounded storage is not order correctness.

### Example 6

A pipeline batches up to 64 records for a GPU or waits two milliseconds. The batcher charges bytes on admission, exports batch and per-item identities, and returns unused capacity on cancellation. Experiments compare no batching, size-only batching, and size-or-time batching so vectorization gains are not attributed solely to pipeline overlap.

### Example 7

Stage A holds a buffer-pool lease while blocking on B's full queue. B needs a buffer lease to produce and release its output. The wait-for cycle deadlocks despite finite queues. A must transfer/release the lease before waiting, reserve progress capacity, or restructure ownership. Increasing queue size only postpones the cycle.

### Example 8

An enrichment call times out after an external service commits. Retrying with a new identity duplicates a charge. The pipeline uses a stable operation key, one retry owner, a query/reconcile path for ambiguous outcomes, and a commit stage that restores per-account order. Queue removal exactly once would not by itself provide exactly-once financial effect.

### Example 9

To validate a Rust, Java, or C++ pipeline implementation, use capacity-one edges, controlled stage gates, and a reference sequential oracle. Force full output, empty input, replicated reordering, one-stage panic, mid-transfer cancellation, and shutdown during admission. Record terminal identity conservation and joined workers. Stress tests complement but do not replace protocol reasoning.

### Example 10

An autonomous infusion-control pipeline senses, validates, estimates dose, checks safety constraints, and commands an actuator. Good average throughput cannot authorize use. Production requires named clinical, pharmacology, control, embedded, real-time, functional-safety, cybersecurity, human-factors, quality, operations, independent verification, and regulatory reviewers; hazard/requirements traceability; worst-case timing and memory evidence; validated sensor/model ranges; independent interlocks; hardware-in-the-loop, fault-injection, fail-safe, recovery, alarm, usability, and clinical validation; and signed residual-risk acceptance. This chapter supplies no deployment approval.

## Cross-Program Connections

- **Algorithms:** dependency DAGs, recurrences, stable ordering, partitioning, and queueing shape schedules.
- **Programming languages:** types, ownership, async tasks, effects, exceptions, and structured scopes define stage contracts.
- **Operating systems:** threads, wakeups, affinity, priorities, I/O, and process isolation determine execution cost.
- **Computer architecture:** instruction pipelines, hazards, cache transfer, memory bandwidth, and accelerators motivate mechanisms.
- **Distributed systems:** delivery, partitions, durable queues, checkpoints, and termination extend ownership across failure domains.
- **Data systems:** query operators, exchange, streaming, backpressure, watermarks, and stateful processing are staged graphs.
- **Machine learning:** preprocessing, batching, host-device transfer, inference, and postprocessing combine heterogeneous resources.
- **Reliability:** bounded obligations, retries, cancellation, checkpoints, and shutdown govern recovery.
- **Formal methods:** state machines, conservation invariants, refinement, and model checking validate transitions.
- **Safety engineering:** deadlines, hazard controls, independent interlocks, and human review bound high-stakes use.

## References

1. G. Kahn. “The Semantics of a Simple Language for Parallel Programming.” IFIP Congress, 1974. <https://perso.ensta.fr/~chapoutot/various/kahn_networks.pdf>.
2. E. A. Lee and D. G. Messerschmitt. “Synchronous Data Flow.” Proceedings of the IEEE 75(9), 1987. <https://doi.org/10.1109/PROC.1987.13876>.
3. J. D. C. Little. “A Proof for the Queuing Formula: L = λW.” Operations Research 9(3), 1961. <https://doi.org/10.1287/opre.9.3.383>.
4. OpenMP Architecture Review Board. “OpenMP API Specification 6.0.” <https://www.openmp.org/wp-content/uploads/OpenMP-API-Specification-6-0.pdf>.
5. UXL Foundation. “oneTBB parallel_pipeline Function.” <https://uxlfoundation.github.io/oneTBB/main/tbb_userguide/Working_on_the_Assembly_Line_pipeline.html>.
6. UXL Foundation. “oneAPI Threading Building Blocks: parallel_pipeline.” <https://uxlfoundation.github.io/oneTBB/main/specification/source/algorithms/functions/parallel_pipeline_func.html>.
7. Go Project. “Go Concurrency Patterns: Pipelines and Cancellation.” <https://go.dev/blog/pipelines>.
8. Python Software Foundation. “concurrent.futures — Launching Parallel Tasks.” <https://docs.python.org/3/library/concurrent.futures.html>.
9. NVIDIA. “CUDA C++ Programming Guide: Asynchronous Data Copies.” <https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#asynchronous-data-copies>.
10. Reactive Streams. “Reactive Streams Specification for the JVM.” <https://github.com/reactive-streams/reactive-streams-jvm/blob/master/README.md>.

## Exercises

### Exercise 1

For four single-server stages with deterministic times `[1,4,2,3]` and six independent items, compute first-item latency, ideal bottleneck interval, recurrence-based makespan, serial makespan, and finite-workload speedup. State assumptions.

### Exercise 2

A replicated stage preserves per-key but not global order. Specify identity, routing, bounded reordering, gap timeout, cancellation, and shutdown contracts for a consumer requiring global input order.

### Exercise 3

Given decode/filter/encode stages that all saturate one memory channel, explain why capacity estimates based only on isolated service time fail. Design a controlled experiment that distinguishes overlap, batching, and cache effects.

### Exercise 4

Design exact ownership and terminal accounting for a fork into two branches, a join, an external side effect, one retry owner, and pipeline cancellation during the side effect.

### Exercise 5

A railway obstacle-detection pipeline meets mean throughput in simulation. Explain why this is insufficient for deployment and enumerate required human review and evidence.

## Answers to the Exercises

### Answer 1

First-item latency is `1+4+2+3=10`. The ideal bottleneck interval is four. Applying the recurrence (or the simple-line formula under these assumptions) gives makespan `10+(6-1)4=30`. Serial makespan is `6*10=60`, so finite-workload speedup is `2.0`. Assumptions are identical independent items, deterministic stage times, one server per stage, infinite/nonblocking buffers, no transfer or scheduling cost, no shared-resource interference, no failure, and all items available for admission.

### Answer 2

Assign one global monotonic sequence and stable key identity at admission; route each key consistently while allowing replicas across keys. Completed results enter a count/byte-bounded map keyed by sequence, and only the next expected sequence commits. A missing sequence has a deadline and explicit fail-stream, gap-marker, or cancellation policy; later values cannot accumulate indefinitely. Cancellation follows identity wherever queued/running/reordered and settles once. Shutdown stops admission, drains replicas, resolves/fails gaps, commits or discards buffered values by contract, closes the consumer edge, and joins every worker.

### Answer 3

Isolated `p_j/s_j` assumes independent capacity; one saturated memory channel couples service rates, so concurrency can lengthen every `s_j`. Benchmark an identical sequential baseline and pipeline with the same algorithms/outputs. Sweep stream length, edge capacity, replicas, and fixed batch size; include no-batch and equal-batch controls. Record per-stage queue/service/transfer, makespan and item percentiles, memory bandwidth, cache misses, CPU occupancy, allocations, and output equality. Pin placements and repeat randomized inputs. Attribute gain to overlap only after separating warm-up/drain, batching, cache locality, and measurement overhead.

### Answer 4

Register two branch obligations under the item before publishing either. Each branch owns one derived identity and reaches success/failure/cancel exactly once. The join owns partial results under a bound and becomes ready only under declared all/partial policy. One effect stage uses the original operation key; timeout yields ambiguous, not failed, until queried/reconciled. Only one retry controller may replay with that key. Cancellation stops new branches, signals queued/running owners, waits for or reconciles the effect, releases join/buffer permits once, and produces one item terminal outcome. Pipeline termination includes branch, join, retry timer, and external-effect obligations.

### Answer 5

Mean throughput omits worst-case deadline, sensor/model validity, rare obstacles/weather, queue/reorder bounds, schedule variance, hardware faults, stale frames, cancellation, cybersecurity, failover, and safe actuation. Require named railway signalling/control, perception, safety, real-time, embedded/hardware, cybersecurity, human-factors, operations, quality, independent verification, and regulatory reviewers; hazard and requirements traceability; applicable-standard assessment; validated data/model provenance and operating domain; worst-case time/memory/resource analysis; simulation plus hardware-in-the-loop, environmental, saturation, fault-injection, degraded-mode, failover, recovery, alarm, and field evidence; independent fail-safe interlocks; and signed residual-risk acceptance. This answer is not deployment authorization.
