---
module_id: CONPAR-041
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 41
title: Task Parallelism and Dependency Graphs
status: complete
last_verified: 2026-08-29
---

# Task Parallelism and Dependency Graphs

## One-Page Review

### Governing question

How can a computation be decomposed into tasks whose dependency graph exposes safe parallelism, predicts unavoidable critical-path time, and preserves ownership, failure, and termination?

### Essential definitions

- A **task** is a bounded unit of computation with declared inputs, outputs, effects, and completion state.
- A **dependency edge** `u -> v` means task `v` may not start its dependent action until `u` satisfies the named condition.
- A **directed acyclic graph (DAG)** contains directed edges and no directed cycle.
- A **ready task** has all required predecessors satisfied and required resources/admission available.
- A **topological order** lists every vertex after all its predecessors; one exists exactly for finite DAGs.
- **Work** `T1` is total execution cost on one processor in the task model.
- **Span** `T_infinity` is the longest weighted dependency path and lower-bounds parallel execution time.
- **Average parallelism** is `T1/T_infinity`, an upper bound on useful average processor count in the idealized model.
- The **critical path** is a maximum-weight dependency path; accelerating work outside it may not reduce makespan.
- **Grain size** is useful work per task relative to creation, scheduling, synchronization, communication, and locality costs.

### Central model, mechanism, or theorem

Represent a computation as weighted DAG `G=(V,E)` with task cost `w(v)>=0`. Work is `T1=sum_v w(v)`. Earliest finish is `EF(v)=w(v)+max_{u in pred(v)} EF(u)`, with empty maximum zero; span is `T_infinity=max_v EF(v)`. Any schedule on `P` identical processors satisfies `T_P >= max(T1/P,T_infinity)`. For fully strict greedy task computations, the classical work-span result gives an upper bound of the form `T_P <= T1/P + O(T_infinity)` under its stated runtime assumptions—not for arbitrary effects, resource constraints, or heterogeneous machines.

### Critical invariants

The graph is acyclic and every required predecessor edge is present. A task becomes ready only after dependency completion and publication of its outputs. Each task has one terminal outcome and each output/effect has declared ownership. Scheduler execution order among ready tasks is not program semantics unless explicitly required. Task creation and outstanding graph state are bounded. Cancellation/failure propagates along declared ownership and dependents never consume invalid partial output. Resources are acquired in a way that cannot create hidden cycles. Final success requires all required sinks and owned child tasks to terminate.

### Common failures

Code creates tasks without declaring data dependencies; confuses source-code order with happens-before; inserts a false edge and serializes independent work; omits a true edge and races; uses a cycle as a “workflow”; creates millions of tiny tasks; waits inside a worker needed to run its child; measures task count instead of work; assumes `T1/T_infinity` is achieved speedup; ignores memory bandwidth, locality, NUMA, accelerators, or locks; allows failed predecessors to leave dependents runnable; or reports parent completion while detached descendants still mutate results.

### Compact example

Tasks have weights `A=3, B=2, C=4, D=2, E=1`; edges are `A->B`, `A->C`, `B->D`, `C->D`, and `C->E`. Total work is 12. Earliest finishes are 3, 5, 7, 9, and 8, so span is 9 along `A-C-D`. The available parallelism is only `12/9=1.333...`, despite five tasks. The graph exposes parallel pairs `B/C` and `D/E`, but its critical chain fundamentally limits speedup.

### Connections

[Structured Concurrency](037-structured-concurrency.md) governs task lifetime; [Backpressure in Asynchronous Pipelines](040-backpressure-in-asynchronous-pipelines.md) bounds task admission. The [program roadmap](../ROADMAP.md) next contrasts task parallelism with data-parallel bulk operations.

## Governing Question

How should engineers derive a task graph from semantic dependencies, analyze its work and span, and schedule it without turning implicit state, resource waits, or failures into hidden edges?

A task graph is both a parallelization opportunity and a correctness contract.

## Why This Matters

Many computations are neither one homogeneous loop nor a collection of independent requests. A compiler parses files, resolves names, type-checks units, optimizes functions, and links outputs. A build system executes commands after their inputs exist. A query engine runs scans, joins, shuffles, and aggregation. A renderer prepares geometry, culls, shades, and composes. Machine-learning systems preprocess, execute operators, and reduce gradients.

Task parallelism expresses different operations that may execute concurrently when their true dependencies allow it. A DAG makes those constraints inspectable. It supports readiness scheduling, cycle detection, critical-path analysis, incremental recomputation, cancellation, provenance, and trace interpretation.

The graph is useful only if its edges mean something exact. Missing edges permit consumers to observe absent or concurrently changing data. Extra edges suppress legal concurrency. Hidden edges through locks, files, environment, global state, devices, or connection pools invalidate schedule analysis. Production tasking therefore begins with ownership and effects, then performance.

## Prerequisites and Retrieval

Retrieve:

- shared-state publication from [Critical Sections and Shared-State Invariants](008-critical-sections-and-shared-state-invariants.md);
- component lifecycle from [Designing a Correct Multithreaded Component](020-designing-a-correct-multithreaded-component.md);
- task termination from [Structured Concurrency](037-structured-concurrency.md);
- future outcomes from [Futures and Promises](033-futures-and-promises.md);
- bounded admission from [Backpressure in Asynchronous Pipelines](040-backpressure-in-asynchronous-pipelines.md); and
- wait cycles from [Deadlock, Livelock, and Starvation](006-deadlock-livelock-and-starvation.md).

Retrieval prompt: given four operations, write each read set, write set, external effect, and required predecessor; then remove any edge that represents habit rather than semantic necessity.

## Learning Objectives

After completing this module, a learner can:

1. distinguish task parallelism from concurrency, data parallelism, and pipelines;
2. derive dependency edges from data, control, effect, and resource constraints;
3. detect cycles and construct a topological order;
4. compute weighted work, earliest finish, span, and average parallelism;
5. use work/span bounds with their assumptions and limitations;
6. identify critical and near-critical paths;
7. choose task grain while accounting for scheduling and locality overhead;
8. specify readiness, output publication, failure, cancellation, and retry semantics;
9. diagnose scheduler starvation and hidden resource dependencies; and
10. verify a dynamic task graph with deterministic and adversarial schedules.

## Core Exposition

### From computation to tasks

Decomposition starts with semantic units. A good task has clear inputs, an owned output or effect, a bounded lifetime, and a useful amount of work. Tasks need not map one-to-one to threads. A runtime may execute many tasks on a small worker set, inline a child, fuse adjacent operations, or migrate ready work.

Task parallelism runs distinct operations concurrently: parse independent files, compute left/right subtrees, or evaluate independent DAG operators. Data parallelism applies similar work across partitions. Pipeline parallelism overlaps stages across different items. These forms compose, but their bounds and communication differ.

Do not create tasks merely because functions exist. A trivial task can cost more to allocate, enqueue, steal, wake, and synchronize than its body performs. Conversely, one monolithic task hides independent work. Decomposition is a modeling decision that affects correctness evidence, locality, cancellation, observability, and scheduling.

### Deriving dependency edges

An edge must name a prerequisite. A true data dependency exists when `v` reads a value produced by `u`. An anti-dependency occurs when order protects a read before a later overwrite; renaming or immutable versions can remove it. An output dependency orders competing writes. Control dependencies select whether work is needed. Effect dependencies order noncommutative I/O or state transitions.

Resource limits are usually not DAG dependencies. If two tasks both use one database connection, they may be semantically independent but contend for a permit. Encoding an arbitrary edge chooses an order and reduces graph parallelism; representing the connection pool separately preserves readiness while constraining execution. Yet acquisition order can introduce a hidden wait graph, so resource constraints remain part of scheduling correctness.

Declare edges at the granularity of publication. If producer writes several fields and consumer needs only one, a fine-grained ready event can expose more parallelism, but it also increases states and synchronization. Never publish a mutable output before its invariant holds unless the consumer protocol explicitly permits incremental states.

### DAG validity and topological order

A dependency graph for one finite computation should be acyclic. A directed cycle means no member can become initially ready if every edge is a strict completion prerequisite. Recurring computations belong in iterations, streams, state machines, or successive graph instances; the per-iteration dependency relation can remain acyclic.

Kahn's algorithm tracks each vertex's unsatisfied-predecessor count. Put zero-count vertices in a ready set, repeatedly remove one, emit it, and decrement successors. If fewer than `|V|` vertices are emitted, a cycle or malformed edge remains. Depth-first color marking is another cycle/topological method.

A topological order is not necessarily a runtime order. Multiple valid orders exist when tasks are incomparable. Deterministic graph serialization can choose lexical/stable IDs while runtime execution remains nondeterministic. Tests should compare allowed partial-order outcomes or deterministic final assembly, not one accidental ready-task order.

### Work, span, and lower bounds

Assign each vertex cost `w(v)` in a declared model. `T1=sum w(v)` is work. Earliest start `ES(v)` is zero for sources and otherwise the maximum predecessor finish. `EF(v)=ES(v)+w(v)`. The span `T_infinity=max EF(v)` is longest weighted path.

On `P` identical processors, at least `T1/P` time is required because processors can perform at most `P` units per unit time. At least `T_infinity` is required because dependent tasks on a path cannot overlap. Thus `T_P >= max(T1/P,T_infinity)`. These are lower bounds; real time can be larger.

Average parallelism `T1/T_infinity` indicates the maximum useful average width in the idealized graph. Five hundred tasks can have parallelism near one if chained. A small task count can have high parallelism if costs are balanced and independent. Width alone ignores weights and time-varying readiness.

The critical path may change with costs, input, resource constraints, or failures. Near-critical paths matter because accelerating the current maximum can expose the next. Profile the executed graph rather than assuming source structure supplies accurate weights.

### Greedy scheduling and work-span theory

A greedy scheduler keeps available processors busy with ready tasks. Classical scheduling results bound execution in terms of work and span under particular models. For fully strict multithreaded computations, work stealing can achieve expected time near `T1/P + O(T_infinity)` with assumptions about costs and scheduler/runtime behavior.

This is powerful but scoped. It does not include arbitrary blocking I/O, oversubscribed libraries, lock convoys, memory bandwidth, cache/NUMA placement, heterogeneous processors, GPU transfers, priority constraints, failures, or external rate limits. Nor does a bound predict constant factors.

Scheduling arbitrary weighted DAGs optimally on multiple processors is generally computationally difficult. Practical list schedulers choose among ready tasks using critical-path rank, priority, locality, age, or estimated cost. The policy should preserve dependency safety while making performance/fairness trade-offs explicit.

### Grain size and overhead

Let useful work per task be `g` and per-task overhead roughly `h`. When `g` approaches `h`, scheduling dominates. Coarsening groups tasks to amortize overhead and improve cache locality. Finer tasks expose parallelism and load balance, especially under irregular work.

Use cutoffs in recursive algorithms: below a problem size, execute sequentially. Batch small independent nodes. Fuse producer-consumer nodes when intermediate materialization costs exceed useful overlap. Avoid global fixed thresholds without measurement; machine, runtime, input distribution, and data placement matter.

Grain also affects cancellation. Large tasks respond slowly unless they check cancellation at safe points. Tiny tasks enlarge graph metadata and terminal accounting. Choose boundaries that align with invariants and observable completion, then tune with work/span and profile evidence.

### Readiness, publication, and memory

Dependency completion must publish output according to the language/runtime memory model. A future becoming ready, a channel handoff, a join, or a scheduler's documented task edge can establish visibility; an integer counter without correct synchronization cannot.

Ready means all semantic prerequisites succeeded or produced an accepted alternative state. It does not mean resources are available, priority allows execution, or deadline remains useful. Distinguish dependency-ready, admitted, scheduled, running, suspended, and terminal.

Tasks should prefer immutable inputs and uniquely owned outputs. If incomparable tasks mutate shared state, the DAG alone does not prevent races. Add synchronization, partition ownership, a reduction, or an actual dependency. External effects need idempotency and ordering beyond in-memory output publication.

### Failure and cancellation propagation

When predecessor `u` fails, dependent `v` must not blindly run with absent output. Policies include fail-fast cancellation of the owned subgraph, typed failure values that allow recovery nodes, fallback dependencies, or partial-result semantics. Mark whether edges require success, terminal completion, or a specific outcome.

Structured task ownership ties child lifetime to a scope. On failure, stop spawning, cancel owned descendants, wait for their terminal cleanup, and aggregate/report deterministically. Detached tasks break the graph's completion claim if they still own state or effects.

Retries form new attempts, not time travel. Give the logical operation stable identity; ensure effects are idempotent or compensable; bound attempts; and decide whether downstream depends on one successful attempt or observes attempt history. Dynamic retry nodes must remain within capacity and deadline budgets.

Cancellation of a node can invalidate descendants but not necessarily independent siblings. Compute the affected subgraph from data ownership rather than cancelling every task reflexively. Conversely, if the scope's goal has failed, allowing expensive siblings to continue may waste resources. Policy belongs to task-group ownership.

### Dynamic task graphs

Some graphs are discovered while running: recursive divide-and-conquer spawns children, a crawler discovers links, and a build reads depfiles. Acyclicity and termination can no longer be validated only from an initial static file.

Require bounded spawning or a proved finite discovery domain, stable task identity, deduplication, parent/child ownership, atomic dependency registration, and a termination detector. Register a child before a parent can report completion; otherwise the coordinator may observe zero outstanding tasks while a late child appears.

Dynamic dependencies cannot be added after a consumer already ran unless the model supports invalidation and recomputation. Build systems solve this with declared/discovered inputs and cache invalidation rules. A mutable graph needs epochs or synchronization so scheduler readiness is not based on stale predecessor counts.

### Resource constraints and hidden cycles

A DAG can be acyclic while execution deadlocks. Task A holds resource X and waits for a child; the child is queued behind tasks holding Y and waiting for X. All worker threads may block waiting on descendants that can run only on those workers. GPU tasks may wait for host callbacks starved by the same executor.

Add resource-acquisition and worker-availability edges to a separate wait-for graph. Prefer nonblocking suspension, helping (a worker awaiting a child executes other ready work), reserved capacity, ordered acquisition, or architectures that do not hold scarce resources across task joins.

Nested parallel libraries can oversubscribe processors: `P` outer tasks each start `P` internal threads. Coordinate runtimes, cap parallel regions, or use one executor. CPU count is not the only cap; memory bandwidth and shared caches can make additional ready tasks harmful.

### Locality, heterogeneity, and placement

Moving a task to an idle worker can cost cache misses and NUMA-remote access. Work stealing commonly lets workers pop local work and steal from others, trading locality for balance. Task affinity can preserve data placement but cause imbalance. Measure bytes moved and cache/NUMA behavior alongside task time.

Heterogeneous graphs assign tasks to CPUs, GPUs, accelerators, or remote workers. Cost includes transfer, kernel launch, serialization, and device occupancy. A shortest compute kernel may lose after transfer. Resource-specific queues and capabilities constrain readiness beyond graph edges.

Placement does not change semantic dependencies, but it changes weights and may add staging tasks. Keep correctness graph, resource constraints, and cost model conceptually separate so a performance estimate is not mistaken for validity.

### Observability and verification

Give tasks stable logical IDs and attempts distinct IDs. Record predecessor satisfaction, ready time, enqueue, start, suspension, finish, outcome, worker/resource, bytes, and cancellation. From traces compute queue delay, execution time, work estimate, realized critical path, processor utilization, steals, and blocked-resource time.

Critical-path tracing requires causal edges, not only timestamps. Clock overlap does not prove independence. Include spawn/join, future, channel, lock, and external dependency events where they govern progress.

Tests validate graph construction with missing vertices, duplicate edges, cycles, disconnected components, empty/single-node graphs, multiple sources/sinks, zero/large weights, and deterministic topological tie-breaking. Controlled schedulers enumerate ready-task orders for race-sensitive cases. Fault injection fails every node before/after publication and verifies descendants, cleanup, credits, and terminal accounting. Stress and profiling supply empirical evidence, not a proof over all schedules.

## Definitions and Notation

Let `G=(V,E)` be a finite DAG. Edge `(u,v)` states the declared completion condition from `u` required by `v`. `pred(v)` and `succ(v)` are predecessor and successor sets.

With nonnegative vertex weight `w(v)`, work is `T1=sum_{v in V} w(v)`. Define `ES(v)=0` for sources and `ES(v)=max_{u in pred(v)} EF(u)` otherwise; `EF(v)=ES(v)+w(v)`. Span is `T_infinity=max_v EF(v)`.

For `P>=1` identical processors, `T_P>=T1/P` and `T_P>=T_infinity`, hence `T_P>=max(T1/P,T_infinity)`. Speedup is `S_P=T1/T_P`; efficiency is `E_P=S_P/P`; ideal average parallelism is `T1/T_infinity`.

The ready set at scheduler state `s` is `R(s)={v | v not started and every required predecessor outcome is satisfied}`. Resource eligibility and policy can further restrict which member runs.

Kahn residual indegree `d(v)` starts as `|pred(v)|`. Emitting `u` decrements each `d(v)` for `v in succ(u)` once. A finite graph is acyclic exactly when the algorithm emits all vertices.

## Mechanisms, Invariants, or Proof Structure

Review a task-parallel computation in this order:

1. name task inputs, outputs, effects, identity, and terminal states;
2. derive data/control/effect edges and remove artificial sequencing edges;
3. separate semantic dependencies from resource constraints;
4. validate vertex/edge identity, acyclicity, and topological coverage;
5. ensure completion publishes outputs under the runtime memory model;
6. estimate/measure weights, compute work, earliest finish, span, and critical paths;
7. compare available parallelism with processor/resource capacity;
8. choose grain, cutoffs, fusion, and placement using overhead/locality evidence;
9. bound task creation, ready queues, dynamic discovery, retries, and retained outputs;
10. define predecessor failure, cancellation, fallback, and partial-result semantics;
11. add resources/workers to the wait-for graph and exclude hidden cycles;
12. record causal task traces and test alternative ready orders/failures; and
13. stop spawning, cancel as owned, settle outputs/effects, and join all required sinks.

The executable model validates a five-task DAG, computes a stable topological order, earliest finishes, work, span, average parallelism, and one critical path.

<!-- bijux-verify: {"id":"task-dag-work-span-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"order=['A', 'B', 'C', 'D', 'E']\nearliest_finish={'A': 3, 'B': 5, 'C': 7, 'D': 9, 'E': 8}\nwork=12\nspan=9\navg_parallelism=1.333\ncritical_path=['A', 'C', 'D']\nvalid_edges=True\n","stderr":""}} -->
```python
weights = {"A": 3, "B": 2, "C": 4, "D": 2, "E": 1}
predecessors = {
    "A": [],
    "B": ["A"],
    "C": ["A"],
    "D": ["B", "C"],
    "E": ["C"],
}
remaining = {task: len(predecessors[task]) for task in weights}
order = []

while len(order) < len(weights):
    ready = sorted(
        task for task in weights
        if remaining[task] == 0 and task not in order
    )
    if not ready:
        break
    task = ready[0]
    order.append(task)
    for successor in weights:
        if task in predecessors[successor]:
            remaining[successor] -= 1

earliest_finish = {}
parent = {}
for task in order:
    best_predecessor = None
    for predecessor in predecessors[task]:
        if best_predecessor is None or earliest_finish[predecessor] > earliest_finish[best_predecessor]:
            best_predecessor = predecessor
    start = 0 if best_predecessor is None else earliest_finish[best_predecessor]
    earliest_finish[task] = start + weights[task]
    parent[task] = best_predecessor

span_task = max(order, key=lambda task: earliest_finish[task])
critical_path = []
cursor = span_task
while cursor is not None:
    critical_path.append(cursor)
    cursor = parent[cursor]
critical_path = list(reversed(critical_path))

work = sum(weights.values())
span = earliest_finish[span_task]
valid_edges = all(order.index(u) < order.index(v) for v in order for u in predecessors[v])

print(f"order={order}")
print(f"earliest_finish={earliest_finish}")
print(f"work={work}")
print(f"span={span}")
print(f"avg_parallelism={work / span:.3f}")
print(f"critical_path={critical_path}")
print(f"valid_edges={valid_edges}")
```

Limitations: this sequential analyzer assumes a finite valid vertex map, nonnegative deterministic weights, finish-to-start dependencies, zero communication cost, unlimited ideal processors for span, and lexicographic tie-breaking. It does not schedule threads, detect every malformed input, model resource constraints, overhead, locality, heterogeneity, cancellation, failure, dynamic spawning, memory visibility, external effects, or runtime fairness.

## Alternatives and Trade-Offs

**Static DAG** supports complete validation and planning before execution; **dynamic DAG** handles discovered/recursive work but needs bounded spawning and termination detection.

**Fine-grained tasks** expose parallelism and balance irregular work; **coarse tasks** reduce overhead and improve locality.

**Central ready queue** simplifies priority and observation but can contend; **per-worker deques/work stealing** scale and preserve locality while making execution order nondeterministic.

**Critical-path priority** targets makespan; **FIFO/fair scheduling** controls starvation; **locality priority** reduces movement. Hybrid policy needs explicit tie rules.

**Explicit dependency graph** is inspectable and reusable; **nested fork/join** is concise for strict recursive structure; **pipeline/channel composition** fits long-lived streams.

**Immutable outputs** simplify publication and retries; **shared mutable outputs** may reduce copying but require synchronization outside graph topology.

**Fail-fast scope** reduces wasted work; **partial-result graph** preserves independent successes but requires typed missing/failure states.

**CPU placement** avoids transfer; **accelerator placement** can reduce compute time but adds staging, capability, and device-failure concerns.

## Failure Modes and Misconceptions

- “Different functions are independent.” Shared inputs, effects, and resources can impose edges.
- “A DAG prevents races.” Incomparable tasks can still race on shared mutable state.
- “Topological order is the execution order.” It is one legal serialization of a partial order.
- “Any cycle can be scheduled iteratively.” A strict completion cycle has no initial ready vertex.
- “Task count measures parallelism.” Weighted span, not count, supplies the ideal bound.
- “`T1/T_infinity` is guaranteed speedup.” It is ideal available parallelism under a model.
- “Only the longest source-code chain is critical.” Weights and dynamic execution determine the path.
- “More tasks always balance better.” Scheduling and communication can dominate.
- “More workers always reduce time.” Bandwidth, locality, locks, and oversubscription can worsen it.
- “Waiting on a child is harmless.” Worker exhaustion can prevent the child from running.
- “Future ready means successful.” It may carry failure or cancellation.
- “Parent completion includes detached children.” Only structured ownership establishes that claim.
- “Retry the node.” Effects, descendants, identity, and capacity must be reconciled.
- “A resource permit is a semantic dependency.” It constrains eligibility but may not require a fixed order.
- “A trace timeline reveals causality.” Explicit dependency/synchronization edges are required.

## Worked Examples

### Example 1

`A` parses a file, then `B` resolves names and `C` extracts documentation independently; `D` type-checks using `B`; `E` indexes documentation using `C`. Edges `A->B`, `A->C`, `B->D`, `C->E` expose two branches. Adding `B->C` because the sequential prototype called B first needlessly removes parallelism.

### Example 2

Two tasks write different indices of an owned array and a final task reads the entire array. Partition ownership avoids a race; edges from both writers to the final reader publish completion. If writers can resize the shared array, disjoint index intention is insufficient—the storage mutation needs redesign or synchronization.

### Example 3

Weights `A=3,B=2,C=4,D=2,E=1` and the chapter edges yield work 12 and span 9. With two processors, both lower bounds are `max(6,9)=9`; the critical path already dominates, and an ideal two-processor schedule can meet 9. Accelerating only B cannot reduce the nine-unit `A-C-D` chain.

### Example 4

A recursive sort spawns one task for every single-element partition. Work remains useful, but allocation and joins dominate. A cutoff sorts small partitions sequentially; larger siblings remain parallel. Tune the cutoff with distribution-aware benchmarks, and retain cancellation checks between bounded chunks.

### Example 5

Eight executor workers each spawn a child into the same executor and synchronously wait. All workers become occupied, so children never start although the task DAG is acyclic. Use a fork/join runtime that helps while waiting, nonblocking continuations, inline execution, or reserve capacity; include worker slots in the wait graph.

### Example 6

Task P publishes a mutable dictionary future before finishing inserts. Dependent Q starts after “ready” and observes partial state. Complete construction before resolving the future, publish an immutable snapshot, or specify a separate incremental protocol with versioned events. Dependency edges require a valid publication point.

### Example 7

A build task discovers a generated header after downstream compilation was declared ready. Late edge insertion invalidates output. Register discovered dependencies before readiness, invalidate and rerun affected nodes under an epoch, or require a discovery pass. Silently mutating indegree after execution is unsound.

### Example 8

GPU task G takes one unit of kernel time but four units to transfer inputs/outputs; CPU task C takes three units on resident data. Selecting G by compute time lengthens the graph. Represent staging costs/tasks and resource occupancy in the cost model while keeping semantic dependencies unchanged.

### Example 9

Predecessor U fails after an external effect but before publishing output. Dependent V cannot run as success. The scope cancels V, reconciles U with stable operation identity, and allows unrelated branch W to finish only if partial-result policy values it. A retry attempt is a new task linked to the same logical operation and bounded budget.

### Example 10

A radiation-treatment planner parallelizes dose calculation into a DAG and treats span reduction as evidence that the plan is clinically safe. Work/span establishes only modeled execution structure. Named medical physicists, radiation oncologists, treatment-planning specialists, clinical safety, software, cybersecurity, human-factors, quality, verification, and regulatory reviewers must approve numerical algorithms, data provenance, determinism/tolerance, hardware behavior, hazard controls, independent calculation, commissioning, and patient-specific evidence. This chapter cannot authorize clinical use.

## Cross-Program Connections

- **Algorithms:** DAG traversal, topological sorting, longest paths, and list scheduling supply core mechanisms.
- **Compilers:** dependence analysis, SSA, instruction scheduling, and build graphs expose legal reordering.
- **Operating systems:** worker scheduling, affinity, blocking, and resource pools constrain graph execution.
- **Architecture:** dependency direction, immutable boundaries, and failure isolation shape maintainable task systems.
- **Distributed systems:** remote tasks add leases, duplication, partial failure, and uncertain completion.
- **Data engineering:** query/operator DAGs combine partitioning, shuffle, joins, and backpressure.
- **Machine learning:** computation graphs support automatic differentiation and heterogeneous placement.
- **Performance engineering:** critical paths, grain, locality, utilization, and steals explain scaling.
- **Formal methods:** partial orders, invariants, and bounded-state exploration support schedule reasoning.
- **Reliability:** task identity, retry ownership, cancellation, and terminal accounting govern recovery.

## References

1. T. H. Cormen, C. E. Leiserson, R. L. Rivest, and C. Stein. “Introduction to Algorithms,” 4th ed., chapters on elementary graph algorithms. MIT Press, 2022. <https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/>.
2. R. L. Graham. “Bounds for Certain Multiprocessing Anomalies.” Bell System Technical Journal 45(9), 1966. <https://doi.org/10.1002/j.1538-7305.1966.tb01709.x>.
3. R. D. Blumofe and C. E. Leiserson. “Scheduling Multithreaded Computations by Work Stealing.” Journal of the ACM 46(5), 1999. <https://doi.org/10.1145/324133.324234>.
4. C. E. Leiserson. “The Cilk++ Concurrency Platform.” Journal of Supercomputing 51, 2010. <https://doi.org/10.1007/s11227-010-0405-3>.
5. OpenMP Architecture Review Board. “OpenMP API Specification 6.0.” November 2024. <https://www.openmp.org/wp-content/uploads/OpenMP-API-Specification-6-0.pdf>.
6. oneAPI Specification. “oneAPI Threading Building Blocks: task_group.” <https://uxlfoundation.github.io/oneTBB/main/tbb_userguide/Task-Based_Programming.html>.
7. Rayon Project. “Rayon: How it works.” <https://github.com/rayon-rs/rayon/blob/main/FAQ.md>.
8. Python Software Foundation. “concurrent.futures.” <https://docs.python.org/3/library/concurrent.futures.html>.
9. ISO C++ Working Draft. “Parallel Execution Policies.” <https://eel.is/c++draft/algorithms.parallel.exec>.
10. NVIDIA. “CUDA C++ Programming Guide: Asynchronous Execution.” <https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#asynchronous-execution>.

## Exercises

### Exercise 1

For tasks `A=2,B=5,C=3,D=4,F=1` with edges `A->C`, `A->B`, `B->D`, `C->D`, `C->F`, compute a topological order, earliest finishes, work, span, critical path, average parallelism, and lower bound for two processors.

### Exercise 2

A program creates one task each for load, parse, validate, enrich, persist, and notify. Derive semantic edges, identify optional concurrency, and distinguish a database connection limit from a dependency.

### Exercise 3

Repair an eight-worker parent/child starvation deadlock. Explain why DAG acyclicity is insufficient and state the scheduler/resource invariant.

### Exercise 4

Specify failure and cancellation for a dynamic DAG whose tasks discover children, write idempotent external effects, and may retry. Include termination detection and bounds.

### Exercise 5

An autonomous-vehicle perception DAG meets an average work/span target. Explain why this does not establish a safe deadline and define required human review and evidence.

## Answers to the Exercises

### Answer 1

One lexical topological order is `A,B,C,D,F` (also `A,C,B,D,F` is valid if F placement respects C). Earliest finishes: `EF(A)=2`, `EF(B)=7`, `EF(C)=5`, `EF(D)=max(7,5)+4=11`, `EF(F)=5+1=6`. Work is `2+5+3+4+1=15`; span is 11 along `A-B-D`; average parallelism is `15/11=1.364` approximately. For two processors, `T2>=max(15/2,11)=11` in continuous-cost units. That lower bound does not itself construct a feasible schedule, though this graph can schedule C alongside B and F before D without extending the critical path.

### Answer 2

Load precedes parse; parse precedes validate. Enrich requires validated data if enrichment may not inspect invalid input. Persist requires validated base plus enrichment only if enrichment is part of the committed record. Notify should depend on authoritative persist success, not merely validation, if it announces committed state. Independent enrichments can be sibling tasks and combined before persist. A ten-connection pool restricts which database-ready tasks may run; it does not semantically order persist task X before Y. Acquire its permit without holding resources needed downstream, bound waiting tasks, and keep the graph edge set about data/effect truth.

### Answer 3

The DAG can be parent-to-child and acyclic while the executor wait graph has each of eight worker slots held by a parent waiting for a queued child. Repair with nonblocking continuation/join, work-helping fork/join semantics, safe inline child execution, separate/reserved executor capacity, or a rule forbidding blocking descendant waits on the same saturated pool. The invariant is that waiting tasks do not monopolize every execution resource required by ready dependencies; scheduler termination analysis includes worker slots and resources, not only semantic edges.

### Answer 4

Assign stable logical IDs and distinct attempt IDs; atomically register each child and increment owned outstanding count before the parent can become terminal. Deduplicate discovered identity and bound depth, fan-out, total outstanding work, retry count, bytes, and deadline. A successful attempt publishes immutable output/effect acknowledgement once. Failure cancels invalid descendants or activates typed recovery edges; unrelated siblings follow scope policy. Retries preserve logical identity and idempotency/compensation semantics and consume the original budget. Termination occurs only when spawning is closed and outstanding registered tasks reach zero after terminal cleanup; late registration is rejected or belongs to a new epoch.

### Answer 5

Average weights and ideal span omit worst-case execution, sensor/input variation, memory and accelerator contention, preemption, transfer, thermal behavior, scheduler overhead, faults, cancellation, and actuator deadlines. Establish worst-case and probabilistic assumptions separately, trace every end-to-end deadline and freshness condition, reserve resources, define degraded/fail-safe states, and test deadline misses. Production requires named perception, controls, vehicle systems, functional-safety, real-time, hardware/accelerator, cybersecurity, human-factors, operations, verification, quality, and regulatory reviewers; hazard/requirements traceability; applicable-standard assessment; independent algorithm review; scenario simulation, track/vehicle, saturation, timing, fault-injection, failover, environmental, and recovery evidence; and signed residual-risk acceptance. This answer is not deployment authorization.
