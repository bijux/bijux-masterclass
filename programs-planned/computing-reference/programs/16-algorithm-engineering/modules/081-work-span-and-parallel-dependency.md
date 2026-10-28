---
module_id: ALGE-081
program: Algorithm Engineering
level: 2
module_number: 81
title: Work, Span, and Parallel Dependency
status: complete
last_verified: 2026-09-05
---

# Work, Span, and Parallel Dependency

## One-Page Review

### Governing question

How can a computation's dependency graph reveal unavoidable work, unavoidable serial depth, attainable parallelism, and the gap between an abstract schedule and a correct, efficient execution on finite processors?

### Essential definitions

- A **computation DAG** is a directed acyclic graph whose weighted vertices are indivisible strands of work and whose edges are required precedence constraints.
- The **work** $T_1$ is the total strand cost: execution time on one ideal processor under the model.
- The **span** $T_\infty$ is the maximum weighted path cost: ideal execution time with arbitrarily many processors.
- On $P$ processors, runtime $T_P$ obeys the **work law** $T_P\ge T_1/P$ and the **span law** $T_P\ge T_\infty$.
- **Parallelism** $T_1/T_\infty$ is an average upper bound on useful processor count, not a promise of speedup.
- A **ready** strand has all predecessors complete. A **greedy scheduler** runs ready work whenever a processor is available.
- A **dependence** is semantic ordering required for correctness. Resource contention and scheduler policy may add delays without adding semantic DAG edges.
- **Speedup** is $T_1/T_P$ only when numerator and denominator compute the same result under a comparable cost model.

### Central model, mechanism, or theorem

For any legal schedule, all $T_1$ work must occupy processor capacity, so $P T_P\ge T_1$. Every strand on a critical path must execute in precedence order, so $T_P\ge T_\infty$. Brent's scheduling principle shows that a computation expressed with abundant ideal parallelism can be simulated on $P$ processors in time bounded, up to the precise discrete formulation, by work per processor plus depth [1]. Greedy DAG scheduling therefore targets

$$
T_P=O(T_1/P+T_\infty),
$$

while concrete schedulers add creation, synchronization, stealing, locality, operating-system, and memory costs. Work stealing has a corresponding expected bound for fully strict computations under its stated model [4].

### Critical invariants

- The DAG is acyclic and contains every correctness-relevant precedence edge.
- Every strand executes exactly once and only after all predecessors finish.
- Strand weights and $T_1$ use the same cost model as the claimed $T_P$ comparison.
- The span is a maximum weighted path, not the number of source lines or tasks.
- Scheduler and runtime guarantees retain their processor, computation-structure, randomness, and overhead assumptions.
- Published speedup preserves input, result semantics, numerical policy, and validation strength.

### Common failures

Omitting a data dependence and calling the resulting race parallelism; adding unnecessary edges that serialize independent work; dividing work evenly while ignoring the critical path; counting tasks instead of costs; treating $T_1/T_\infty$ as achieved speedup; using wall-clock serial time as theoretical work without saying so; making tasks too fine; overlooking memory bandwidth and NUMA; relying on floating-point associativity; and quoting an expected work-stealing theorem as a worst-case guarantee for arbitrary task graphs.

### Compact example

A DAG has $T_1=20$ and $T_\infty=10$. With $P=2$, both lower bounds equal 10, yet a valid greedy schedule may take 13 because an early tie choice delays a strand that unlocks the tail. Twenty processors cannot make the computation faster than 10 under the model. The bounds expose capacity and dependency limits; they do not uniquely determine a schedule.

### Connections

[ALGE-033](./033-topological-ordering.md) supplies DAG order. [ALGE-073](./073-online-scheduling.md) distinguishes scheduling objectives and information. [ALGE-080](./080-engineering-algorithms-under-one-pass-and-update-constraints.md) supplies operational evidence discipline. ALGE-082 next develops prefix and reduction structures from these work/span foundations.

## Governing Question

Given a parallel computation with task costs, correctness dependencies, finite processors, runtime overhead, and a real memory system, how should we derive work, span, lower and upper bounds, identify the critical path, construct a legal schedule, and decide whether measured speedup supports the claimed model?

## Why This Matters

Parallel code often begins with an attractive count: there are one million items and 32 cores. That count says almost nothing about attainable speedup. Items may depend on earlier results, a final serial step may dominate, work may be imbalanced, tasks may be too small, or all workers may compete for one memory channel. Conversely, accidental serialization can hide abundant semantic parallelism.

Work and span provide a compact language for separating two fundamental limitations. Work captures total computational demand; span captures the longest chain that no scheduler can overlap. Their ratio identifies how much average parallel slack the algorithm exposes before implementation effects. A dependency DAG also provides a proof object: edges explain why order is required, and missing or excessive edges can be reviewed.

The model is deliberately idealized. It does not automatically include cache misses, coherence, bandwidth, task creation, synchronization, preemption, vectorization, heterogeneity, failures, or operating-system scheduling. Its value is diagnostic: derive algorithmic limits first, then account for the mechanisms that explain the difference between those limits and measured execution.

## Prerequisites and Retrieval

Retrieve asymptotic cost models from ALGE-003 through ALGE-006, topological order, cycle detection, and DAG dynamic-programming order from [ALGE-033](./033-topological-ordering.md), online scheduling distinctions from [ALGE-073](./073-online-scheduling.md), and experimental discipline from ALGE-061 through ALGE-067. You should be able to sum weighted operations, perform a topological traversal, distinguish a lower bound from an achieved runtime, and state assumptions behind a probability claim.

## Learning Objectives

After this module, you should be able to:

1. construct a weighted computation DAG from program semantics rather than source layout;
2. calculate $T_1$, $T_\infty$, average parallelism, speedup, and efficiency;
3. prove the work and span laws and apply Brent-style scheduling reasoning;
4. distinguish semantic dependence, scheduler order, synchronization, and resource contention;
5. trace and validate a finite-processor greedy schedule;
6. interpret work-stealing guarantees under fully strict and randomized assumptions;
7. diagnose granularity, load balance, locality, bandwidth, false sharing, and numerical-order failures; and
8. design differential, invariant, schedule-fuzzing, and performance evidence for a parallel implementation.

## Core Exposition

### Model a computation, not a program listing

A **strand** is a maximal sequence treated as indivisible by the analysis. Let $G=(V,E)$ be a DAG. Vertex $v$ has positive cost $w(v)$, and edge $(u,v)$ means $v$ may not start until $u$ finishes. Sources have no predecessors; sinks have no successors. A fork creates multiple ready regions, and a join waits for required predecessors.

Edges must follow semantics. If task `B` reads a value written by `A`, a true read-after-write dependence orders `A→B`. If two tasks write the same location and final order matters, an output dependence orders them. Reusing storage can create anti-dependence when an earlier reader must finish before a later writer; renaming or private storage may remove that edge. Control, exception, I/O, lock, transaction, and external side-effect semantics can also impose order.

Source-code sequence is not automatically a dependence. Two pure function calls on independent immutable inputs may execute in either order even if written on adjacent lines. Conversely, a shared mutable update with no declared edge is not independence; it is an incomplete graph and likely a race. The DAG is correct only if every topological execution preserves the program's promised observable behavior.

Granularity is a modeling choice. Combining several operations into one strand reduces graph and scheduling overhead but hides internal parallelism. Splitting every instruction exposes maximum theoretical detail but makes task overhead unrealistic. Use a level appropriate to the algorithm, then separately model spawn, queue, and synchronization costs when predicting a runtime.

### Define work and span

The work is

$$
T_1=\sum_{v\in V} w(v).
$$

The span is the maximum cost of any directed path:

$$
T_\infty=\max_{\pi\text{ a path in }G}\sum_{v\in\pi}w(v).
$$

For each vertex in topological order, compute earliest finish

$$
EF(v)=w(v)+\max_{u\in pred(v)} EF(u),
$$

using zero for the maximum over an empty predecessor set. Then $T_\infty=\max_v EF(v)$. Recording the maximizing predecessor reconstructs a critical path. Multiple critical paths may exist; accelerating only one need not reduce span if another remains tied.

Parallelism is $T_1/T_\infty$. It measures average work available per unit of critical-path time on an ideal machine. A computation can have enormous peak width but modest average parallelism. A wide first layer followed by a long serial chain is not scalable merely because one instant contains many ready tasks.

### Derive lower bounds

In $T_P$ time units, $P$ unit-speed processors supply at most $P T_P$ processor-time. Executing all work requires $P T_P\ge T_1$, hence

$$
T_P\ge T_1/P.
$$

No two dependent vertices on one path may overlap. A longest path consumes $T_\infty$ time on any number of processors, hence

$$
T_P\ge T_\infty.
$$

Together,

$$
T_P\ge\max(T_1/P,T_\infty).
$$

This is a lower bound, not necessarily attainable. Processor fragmentation, indivisible weighted strands, precedence shape, and scheduler choices can create slack. Stronger lower bounds can use cuts, resource types, communication, or memory capacity.

The maximum ideal speedup is at most $T_1/T_\infty$. For $P$ processors, speedup is also at most $P$ from the work law. Thus

$$
\frac{T_1}{T_P}\le\min(P,T_1/T_\infty).
$$

These ratios use modeled $T_1$. If a parallel implementation performs extra work, or if the serial baseline uses a different algorithm, report that distinction rather than calling the ratio an algorithmic speedup.

### From ideal parallelism to finite processors

Brent's result gives a simulation principle: if ideal parallel steps expose some number of operations at each depth, schedule at most $P$ of those operations per finite-processor step. Summing the full groups charges work divided by $P$; at most one partially filled group per depth charges a span term [1]. A common asymptotic statement is

$$
T_P=O(T_1/P+T_\infty).
$$

The exact additive constants and ceiling terms depend on the discrete model. Preserve the theorem's formulation rather than turning asymptotic notation into an exact wall-clock equation.

A greedy list scheduler never idles a processor while ready work exists. Classical scheduling analysis bounds such schedules in ideal precedence models [2]. But which ready task is chosen can affect the makespan. Priority by bottom level, critical-path membership, size, locality, or deadline may outperform an arbitrary name order on a particular DAG; no heuristic erases the lower bounds.

### Execute and check a weighted DAG

The following reference implementation validates dependency names and acyclicity, computes work and weighted span, then simulates deterministic nonpreemptive list scheduling. It models identical processors and zero scheduling cost. It is intentionally not a thread runtime.

<!-- bijux-verify: {"id":"weighted-dag-work-span","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"topological: ['A', 'B', 'C', 'D', 'E', 'F', 'G']\nwork=20 span=10 parallelism=2.00\nlower_bound_p2=10.00\nA worker=0 [0,2)\nB worker=0 [2,6)\nC worker=1 [2,6)\nD worker=0 [6,10)\nE worker=1 [6,9)\nF worker=0 [10,12)\nG worker=0 [12,13)\nmakespan=13\n","stderr":""}} -->
```python
tasks = {
    "A": (2, ()),
    "B": (4, ("A",)),
    "C": (4, ("A",)),
    "D": (4, ("A",)),
    "E": (3, ("B", "C")),
    "F": (2, ("D",)),
    "G": (1, ("E", "F")),
}


def analyze(graph):
    for name, (_, deps) in graph.items():
        if any(dep not in graph for dep in deps):
            raise ValueError(f"unknown dependency of {name}")
    order = []
    remaining = set(graph)
    while remaining:
        ready = sorted(name for name in remaining
                       if set(graph[name][1]) <= set(order))
        if not ready:
            raise ValueError("dependency cycle")
        order.extend(ready)
        remaining.difference_update(ready)
    earliest_finish = {}
    for name in order:
        duration, deps = graph[name]
        earliest_finish[name] = duration + max(
            (earliest_finish[dep] for dep in deps), default=0
        )
    return order, sum(duration for duration, _ in graph.values()), max(
        earliest_finish.values(), default=0
    )


def schedule(graph, processors):
    done, started, running = set(), set(), []
    free = list(range(processors))
    timeline, now = [], 0
    while len(done) < len(graph):
        ready = sorted(name for name in graph if name not in started
                       and set(graph[name][1]) <= done)
        while free and ready:
            worker = min(free)
            free = [candidate for candidate in free if candidate != worker]
            name = ready.pop(0)
            started.add(name)
            finish = now + graph[name][0]
            running.append((finish, name, worker))
            timeline.append((name, worker, now, finish))
        if not running:
            raise ValueError("no executable task")
        now = min(finish for finish, _, _ in running)
        finished = sorted(item for item in running if item[0] == now)
        for finish, name, worker in finished:
            done.add(name)
            free.append(worker)
        running = [item for item in running if item[0] != now]
    return timeline, now


order, work, span = analyze(tasks)
timeline, makespan = schedule(tasks, 2)
print("topological:", order)
print(f"work={work} span={span} parallelism={work / span:.2f}")
print(f"lower_bound_p2={max(work / 2, span):.2f}")
for name, worker, start, finish in timeline:
    print(f"{name} worker={worker} [{start},{finish})")
print(f"makespan={makespan}")
```

The schedule takes 13 although the simple lower bound is 10. At time 6, alphabetical choice starts `D` and `E`; this seems reasonable. The longer loss comes from only two processors initially: `D` waits while `B` and `C` run, so `F` finishes at 12 and delays `G`. A different two-processor schedule starting `B` and `D` at time 2, then `C`, still must satisfy the `B,C→E` join and can be analyzed explicitly. The example shows why bounds, scheduler trace, and optimality are separate claims.

### Find real dependencies

Use a read/write effect table. For each task, list immutable inputs, locations read, locations written, external effects, locks, exceptions, and completion signals. Add edges for conflicting accesses whose order is semantically fixed. If order need not be fixed, redesign storage: use task-local accumulators, immutable versions, ownership transfer, commutative updates with a proven combine, or renaming.

Synchronization should reflect the DAG. A barrier after every layer is safe but may add edges between tasks that have no semantic relationship. Point-to-point futures or task dependences can release a consumer as soon as its actual predecessors finish. OpenMP 5.2, for example, specifies task and cross-iteration dependence constructs; that versioned specification defines language behavior, not the performance of a particular runtime [7].

Cycles mean the proposed task graph is not a DAG. The program may contain iterative feedback, locks, or a cyclic wait. Model iterations as separate versions, collapse a genuinely sequential strongly connected region, or choose a different model. Deleting edges merely to make topological sorting pass can create a race or wrong result.

### Fork-join structure and work stealing

In a fully strict fork-join computation, spawned work has well-nested synchronization relationships. Work stealing normally lets a worker operate from one end of its own deque while idle workers steal from another worker. This decentralizes load balancing and tends to keep local work local.

Blumofe and Leiserson prove an expected running-time bound of the form

$$
T_P=O(T_1/P+T_\infty)
$$

for fully strict computations under their randomized work-stealing model, together with a space bound [4]. The result is powerful but narrow. Arbitrary dependencies, blocking I/O, oversubscription, priorities, processor heterogeneity, adversarial runtime behavior, nonconstant strand costs, and shared-memory contention require separate analysis. “Uses work stealing” does not imply the theorem's guarantee.

Steals are not free. Each may touch a remote deque, move a continuation, damage cache locality, or cross a NUMA boundary. Larger grains amortize scheduler cost but reduce available parallelism and increase imbalance. Recursive cutoff selection should be measured across inputs and processor counts, then guarded against pathological depth and tiny leaves.

### Work inflation and hidden critical paths

Parallel execution can perform more operations than the best serial algorithm: redundant boundary work, speculation, padding, synchronization, copying, and conflict retry create **work inflation**. Measure useful algorithmic work separately from runtime overhead and retries. Superlinear speedup can occur from cache or algorithm changes; it is not impossible, but it means the simple same-work ideal model does not explain the result.

Locks and atomics can form hidden serialization. If every task updates one counter, the source DAG may look wide while cache-coherence order creates an effective bottleneck. A reduction tree replaces one hot location with local accumulation plus logarithmic combine depth, subject to associativity and numerical semantics; ALGE-082 treats that structure directly.

Memory bandwidth imposes another resource lower bound. If the computation transfers $Q$ bytes through a sustainable bandwidth $B$, runtime is at least $Q/B$ under that measured level of the hierarchy. Arithmetic work/span alone does not include this. NUMA placement, cache capacity, false sharing, and prefetch behavior can dominate even when tasks are balanced.

### Numerical and observable equivalence

Parallel reordering is legal only relative to promised semantics. Integer addition may overflow under a fixed machine policy. Floating-point addition is not associative, so a different reduction tree can change low bits, exceptional values, or even a branch taken later. Random-number generation tied to task execution order can make results scheduler-dependent.

Specify exact, reproducible, deterministic-with-fixed-tree, correctly rounded, tolerance-bounded, or statistical equivalence as appropriate. Bind seeds to logical work rather than worker identity when schedules may change. Compare results against an independent serial oracle where feasible, including exceptional inputs and many legal schedules.

Side effects need equal care. Printing, file writes, network calls, metrics, and exceptions have observable order and duplication semantics. Buffer and commit effects in a defined order, or include the required edges. A fast execution that changes externally visible behavior has optimized a different program.

### Measure against the model

Record input, algorithm and compiler version, flags, processor topology, worker count, affinity, frequency policy, memory placement, runtime configuration, warmup, repetitions, clock, and background load. Measure serial baseline, parallel wall time, CPU time, task counts, task-size distribution, ready-queue depth, steals, idle time, synchronization, bytes, bandwidth, cache misses when reliable, and output validation.

For each $P$, report speedup $S_P=T_1^{measured}/T_P^{measured}$ and efficiency $E_P=S_P/P$, while keeping measured wall-clock notation distinct from abstract DAG costs. Compare the trend with $T_1/P$, $T_\infty$, and any bandwidth or serial fractions. Confidence intervals describe measurement variability, not algorithmic correctness.

Schedule fuzzing deliberately perturbs task order, worker count, yields, and delay. Race detectors and sanitizers help find implementation errors but cover only observed executions and their tool models. Exhaustive topological schedules are possible only for tiny DAGs; use them as strong bounded evidence, then add adversarial large shapes: chain, antichain, fork-join, diamond, comb, high fan-in, high fan-out, skewed weights, and nested cutoffs.

## Definitions and Notation

Let $G=(V,E)$ be a finite computation DAG with positive strand weights $w:V\to\mathbb{R}_{>0}$. A schedule assigns each vertex a processor and half-open interval, respecting capacity and precedence. $T_1$ is total work, $T_\infty$ maximum weighted path, and $T_P$ makespan on $P$ ideal unit-speed processors.

The ready set at time $t$ contains unstarted vertices whose predecessors completed by $t$. Width is the size of an antichain or a time-specific ready set depending on context; it is not synonymous with $T_1/T_\infty$. Speedup $S_P=T_1/T_P$ and efficiency $E_P=S_P/P$ refer to a declared abstract or measured baseline. A critical path is any path attaining $T_\infty$.

Semantic dependence preserves program meaning. Scheduling order selects among legal ready tasks. Synchronization implements dependence or mutual exclusion. Contention is competition for a limited resource. Work inflation is extra parallel work relative to the chosen serial baseline. Span inflation is additional critical depth introduced by implementation mechanisms.

## Mechanisms, Invariants, or Proof Structure

### DAG validation

Resolve every dependency identity, reject self-edges when they imply an impossible precedence, and topologically sort. For each task, verify declared predecessors cover read/write and side-effect conflicts. Then compute $T_1$ by independent summation and $T_\infty$ by topological dynamic programming. Reconstruct at least one critical path and confirm its cost.

### Schedule validation

For every vertex, check exactly one execution interval of the declared duration. For every edge $(u,v)$, check $finish(u)\le start(v)$. For each processor, sort intervals and reject overlap. The makespan is the latest finish minus the schedule origin. Recompute the work and span lower bounds and never label a nonmatching schedule optimal merely because it is legal.

### Performance claim validation

Separate theorem assumptions, model prediction, implementation evidence, and production judgment. Verify identical results and comparable baselines before speedup. Run scaling and adversarial shapes, record variability, and explain gaps using measured overhead, imbalance, critical path, or resources. Do not infer absence of races from stable timing or infer optimality from high utilization.

## Alternatives and Trade-Offs

**Static DAG scheduling** can use complete cost and dependency information, while **dynamic scheduling** discovers tasks or costs during execution. Static plans reduce runtime overhead but adapt poorly to skew; dynamic plans balance better at coordination cost.

**Central ready queues** simplify priority and observability but contend at scale. **Per-worker deques and stealing** distribute coordination and exploit locality but add randomized behavior and remote steals. **Work sharing** pushes tasks from busy workers; **work stealing** lets idle workers pull them. Each interacts differently with affinity and overload.

**Fine grains** expose parallelism and smooth imbalance; **coarse grains** amortize spawn, queue, and synchronization. **Barriers** are simple but can serialize unrelated paths; **futures or explicit dependences** are precise but increase graph-management cost. **Deterministic schedules** aid reproducibility; **adaptive schedules** may improve utilization.

## Failure Modes and Misconceptions

- **“Many tasks means high parallelism.”** Weighted critical depth may dominate.
- **“The critical path is the longest task.”** It is the maximum total cost along a dependency path.
- **“No edge means independent.”** Only if the graph includes all semantic conflicts.
- **“A barrier is harmless.”** It adds ordering and can inflate span.
- **“Parallelism predicts speedup.”** It is an ideal upper limit before finite $P$ and overhead.
- **“Greedy is optimal.”** Greedy has useful bounds, but ready-task choices can miss the optimum.
- **“Expected work stealing means every run is fast.”** Expectation and fully strict assumptions matter.
- **“Serial wall time equals $T_1$.”** It includes a machine and implementation; label measured and abstract quantities separately.
- **“One task per item is scalable.”** Scheduler overhead and locality may overwhelm useful work.
- **“Full CPU utilization proves efficiency.”** Workers can spin, retry, or saturate a shared bottleneck.
- **“Equal output text proves equivalence.”** Hidden side effects, numerical error, exceptions, and nondeterminism may differ.
- **“More processors cannot hurt.”** Scheduling, contention, NUMA, frequency, and overhead can increase runtime.

## Worked Examples

### Example 1

**Situation.** Weighted paths have costs 9, 14, and 11, while total task work is 48.

**Reasoning.** The span is the maximum path cost, 14, not the average or number of tasks. Parallelism is $48/14\approx3.43$. Even infinitely many ideal processors cannot finish before 14.

**Conclusion.** The computation exposes only about 3.43 units of average ideal parallelism despite any larger peak width.

### Example 2

**Situation.** A DAG has $T_1=120$, $T_\infty=18$, and $P=8$.

**Reasoning.** The work law gives 15; the span law gives 18. Therefore $T_8\ge18$. The work capacity is not the active limit. Maximum ideal speedup at eight processors is at most $120/18\approx6.67$, so efficiency is at most about $0.833$.

**Conclusion.** Adding processors beyond the work/span crossover cannot defeat critical depth.

### Example 3

**Situation.** Tasks `A` and `B` both read immutable `x`; `C` reads outputs from both.

**Reasoning.** There is no semantic `A→B` or `B→A` edge. Required edges are `A→C` and `B→C`. Adding `A→B` increases span without preserving any additional behavior.

**Conclusion.** Source order is not dependence; excessive edges destroy safe parallelism.

### Example 4

**Situation.** Tasks `A` and `B` increment a shared non-atomic counter, and the proposed DAG has no edge between them.

**Reasoning.** Their read-modify-write operations conflict. A topological schedule may overlap them and lose one increment. Add serialization, use an atomic with defined semantics, or give each task private state and combine later.

**Conclusion.** Missing edges manufacture invalid parallelism rather than optimize the program.

### Example 5

**Situation.** One serial strand costs 20 and 80 independent units follow. Compare $P=4$ and $P=16$.

**Reasoning.** Work is 100 and span at least 21 if the 80 units cost one and any is a sink after the serial strand. Bounds are $25$ for four processors and $21$ for sixteen. Infinite processors approach 21, not 1. The initial serial prefix limits scaling.

**Conclusion.** A wide phase does not erase serial depth.

### Example 6

**Situation.** A task performs 2 microseconds of useful work; spawn and completion handling total 5 microseconds.

**Reasoning.** Even perfect balance spends more than twice the useful cost on management. Grouping 100 items creates about 200 microseconds of useful work per task while paying the overhead once, though fewer tasks reduce load-balancing flexibility.

**Conclusion.** Grain size trades exposed parallelism against overhead and must be measured.

### Example 7

**Situation.** A fully strict computation has modeled $T_1=10^9$ operations and $T_\infty=10^5$ operations on 64 workers.

**Reasoning.** $T_1/P=15{,}625{,}000$ dominates $T_\infty$. The work-stealing theorem suggests expected order $T_1/P+T_\infty$ under its assumptions. It does not predict seconds without operation costs, memory behavior, or runtime overhead.

**Conclusion.** The theorem supplies an asymptotic expected schedule bound, not a hardware benchmark.

### Example 8

**Situation.** Sixty-four workers update distinct counters that occupy the same cache line.

**Reasoning.** The semantic DAG has no cross-counter dependence, so work/span predicts abundant parallelism. Cache coherence repeatedly transfers the shared line, creating false sharing and an effective resource bottleneck absent from the DAG.

**Conclusion.** Padding or ownership can improve runtime without changing algorithmic work or span.

### Example 9

**Situation.** A floating sum contains $10^{16}$, $-10^{16}$, and $1$.

**Reasoning.** One legal grouping produces 1; another may produce 0 under common binary floating arithmetic because adding 1 to $-10^{16}$ rounds it away. Both respect the dependency-free real-number reduction, but bitwise results differ.

**Conclusion.** Parallel reorderability depends on the promised numeric semantics, not just algebra over real numbers.

### Example 10

**Situation.** Measured times are 100 seconds serial and 20 seconds on eight workers.

**Reasoning.** Speedup is 5 and efficiency is $5/8=0.625$. This does not identify the cause of the missing ideal speedup. Measure critical path, extra work, idle periods, steals, bandwidth, and validation equivalence. If the parallel algorithm performs different work, even the numerator needs qualification.

**Conclusion.** Speedup is a result to explain with model and evidence, not a proof of correct parallelization.

## Cross-Program Connections

- **Concurrent and Parallel Programming:** happens-before, races, atomics, barriers, futures, and structured concurrency implement dependency edges.
- **Operating Systems:** worker scheduling, preemption, affinity, oversubscription, and page placement affect the gap between $T_P$ and the ideal model.
- **Computer Architecture:** caches, coherence, memory bandwidth, vector units, and NUMA introduce resource limits beyond precedence.
- **Software Architecture:** task boundaries, ownership, immutability, idempotence, and side-effect isolation determine whether the DAG is reviewable.
- **Software Delivery and Reliability Engineering:** reproducible benchmarks, sanitizers, telemetry, rollback, and safe feature flags govern parallel rollout.
- **Systems Engineering:** capacity models must combine work/span with bandwidth, latency objectives, failure domains, and degraded operation.

## References

1. Richard P. Brent, “The Parallel Evaluation of General Arithmetic Expressions,” *Journal of the ACM* 21(2), 1974, 201–206. DOI: [10.1145/321812.321815](https://doi.org/10.1145/321812.321815). Primary source for finite-processor simulation from work and depth; ACM-linked and author records checked 2026-09-05.
2. Ronald L. Graham, “Bounds on Multiprocessing Timing Anomalies,” *SIAM Journal on Applied Mathematics* 17(2), 1969, 416–429. DOI: [10.1137/0117039](https://doi.org/10.1137/0117039). Primary scheduling source for precedence and list-scheduling analysis context; SIAM and author records checked 2026-09-05.
3. Robert D. Blumofe et al., “Cilk: An Efficient Multithreaded Runtime System,” *5th ACM SIGPLAN Symposium on Principles and Practice of Parallel Programming*, 1995, 207–216. DOI: [10.1145/209936.209958](https://doi.org/10.1145/209936.209958). Primary systems source connecting work-first task execution with a runtime; ACM-linked records checked 2026-09-05.
4. Robert D. Blumofe and Charles E. Leiserson, “Scheduling Multithreaded Computations by Work Stealing,” *Journal of the ACM* 46(5), 1999, 720–748. DOI: [10.1145/324133.324234](https://doi.org/10.1145/324133.324234). Primary source for expected work-stealing time and space bounds on fully strict computations; ACM-linked, author, and DBLP records checked 2026-09-05.
5. Nimar S. Arora, Robert D. Blumofe, and C. Greg Plaxton, “Thread Scheduling for Multiprogrammed Multiprocessors,” *Theory of Computing Systems* 34, 2001, 115–144. DOI: [10.1007/s00224-001-0004-z](https://doi.org/10.1007/s00224-001-0004-z). Primary source extending randomized thread-scheduling analysis to multiprogrammed settings; publisher records checked 2026-09-05.
6. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein, *Introduction to Algorithms*, 4th ed., MIT Press, 2022, Chapter 26. Authoritative textbook treatment of task-parallel algorithms, work, span, and scheduling; edition and publisher record checked 2026-09-05.
7. OpenMP Architecture Review Board, *OpenMP Application Programming Interface*, Version 5.2, November 2021, Sections 12 and 15.9. Official versioned specification for tasks and dependences; specification HTML and PDF checked 2026-09-05.
8. Guy E. Blelloch, “Programming Parallel Algorithms,” *Communications of the ACM* 39(3), 1996, 85–97. DOI: [10.1145/227234.227246](https://doi.org/10.1145/227234.227246). Primary source for work/depth-oriented parallel algorithm design and scan-based programming context; ACM-linked records checked 2026-09-05.

## Exercises

### Exercise 1

Define a computation DAG, strand, work, span, critical path, parallelism, ready set, speedup, efficiency, semantic dependence, and work inflation. State which quantities are lower bounds and which are measurements.

### Exercise 2

For tasks `A=3`, `B=2 after A`, `C=5 after A`, `D=4 after B`, `E=1 after B,C`, and `F=2 after D,E`, compute $T_1$, every earliest finish, $T_\infty$, a critical path, parallelism, and the work/span lower bounds for $P=2$ and $P=4$. Give legal schedules and do not claim optimality without proof.

### Exercise 3

A parallel implementation omits a write/read dependence, adds a global barrier after each loop chunk, spawns one task per 200 ns item, uses a shared counter, seeds randomness by worker, and validates only one output. Diagnose each defect and design a focused check or correction.

### Exercise 4

Design the parallelization and evaluation of a DAG workload with skewed task costs, 64 hardware threads across four NUMA nodes, 30 GB/s measured memory bandwidth, exceptions, and a reproducibility requirement. Compare static partitioning, a central queue, and work stealing; specify invariants, metrics, adversarial inputs, and fallback.

### Exercise 5

A genomics pipeline reports 12× speedup on 16 workers after changing both its alignment heuristic and numeric reduction order. Transfer this chapter's reasoning to determine what can honestly be claimed, what evidence is missing, and how to separate algorithmic, scheduling, hardware, and semantic effects.

## Answers to the Exercises

### Answer 1

A computation DAG is an acyclic precedence graph; a strand is one modeled indivisible vertex. Work $T_1$ is the sum of strand costs. Span $T_\infty$ is the maximum weighted path; a critical path attains it. Parallelism is $T_1/T_\infty$. The ready set contains unstarted vertices whose predecessors completed. Speedup compares a declared serial baseline with parallel time; efficiency divides speedup by processor count. Semantic dependence is ordering required to preserve promised behavior. Work inflation is extra work performed by the parallel implementation relative to its chosen serial baseline. $T_1/P$ and $T_\infty$ yield lower bounds on ideal $T_P$; parallelism bounds ideal average useful processors. Measured runtime, speedup, efficiency, steals, and utilization are empirical. A scheduling theorem may give an upper bound under its model, not a measurement.

### Answer 2

Work is $3+2+5+4+1+2=17$. Earliest finishes are $EF(A)=3$, $EF(B)=5$, $EF(C)=8$, $EF(D)=9$, $EF(E)=1+\max(5,8)=9$, and $EF(F)=2+\max(9,9)=11$. Thus span is 11, with critical paths `A→B→D→F` and `A→C→E→F`, both cost 11. Parallelism is $17/11\approx1.55$. For $P=2$, the lower bound is $\max(8.5,11)=11$; for $P=4$ it remains 11. A legal two-processor schedule runs A at 0–3, B and C at 3–5 and 3–8, D at 5–9, E at 8–9, and F at 9–11, attaining 11. The same schedule is legal on four processors and also attains the span lower bound, so both are optimal under this ideal nonpreemptive model. The conclusion does not include runtime overhead or memory effects.

### Answer 3

The omitted write/read edge permits a consumer to see absent or partial data; inject delays and enumerate small schedules while comparing with a serial oracle, then add the edge or versioned handoff. Global barriers add false dependencies; replace them with precise futures or task dependences and compare span. A 200 ns item cannot amortize normal task machinery; batch items and sweep cutoff sizes. The shared counter serializes or races; use local counters and a validated combine, or a correctly ordered atomic if its semantics are required. Worker-derived random seeds make results schedule-dependent; derive streams from stable logical task IDs and record the scheme. One output misses nondeterministic faults; schedule-fuzz, vary workers and affinity, run sanitizers, test exceptional inputs, and validate all promised numeric and side-effect properties.

### Answer 4

Build a weighted DAG from immutable inputs, write ownership, exceptions, and output order; compute work, span, critical paths, bytes, and the bandwidth lower bound $Q/(30\text{ GB/s})$. Static NUMA-local partitions minimize movement when cost predictions are reliable but suffer skew. A central priority queue can favor critical tasks but may contend across 64 threads. Per-node work-stealing deques with local steals before remote steals adapt to skew while limiting NUMA traffic, though the fully strict randomized theorem applies only if the workload meets it. Pin workers by experiment, allocate data on its owning node, batch fine tasks, buffer deterministic outputs, and propagate cancellation/exceptions through explicit edges. Preserve a fixed logical reduction tree or reproducible accumulator. Validate acyclicity, exactly-once execution, predecessor completion, nonoverlapping ownership, equivalent results, and exception cleanup. Measure task distributions, ready depth, idle time, local/remote steals, queue contention, span proxy, bandwidth, remote access, cache misses, wall/CPU time, and result differences. Test chains, antichains, diamonds, skew, tiny grains, hot data, remote-heavy placement, faults, and oversubscription. Fall back to fewer pinned workers or a verified serial implementation when invariants or reproducibility fail.

### Answer 5

The reported ratio compares two changed systems, so it is an end-to-end throughput result, not yet parallel speedup of one algorithm. Run the old heuristic serial and parallel, and the new heuristic serial and parallel, on identical inputs and quality criteria. Count work, span proxies, explored candidates, memory traffic, task overhead, and hardware configuration. Specify whether the new heuristic returns the same optimum, an approximation, or merely acceptable domain quality. Fix or characterize reduction order, seeds, exceptional floating values, and tolerance; validate biological outputs independently rather than only byte equality. Measure scaling across worker counts with repetitions, affinity, NUMA placement, and bandwidth. Then attribute algorithmic improvement to changed work/quality, scheduling improvement to finite-processor execution, hardware effects to cache/vector/bandwidth changes, and semantic difference to the revised heuristic or numerics. Honest claims might be “12× end-to-end speedup at matched validated quality” plus separate same-algorithm parallel speedup; stronger equivalence requires corresponding evidence.
