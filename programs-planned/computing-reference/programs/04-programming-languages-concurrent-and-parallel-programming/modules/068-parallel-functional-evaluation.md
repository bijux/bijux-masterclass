---
module_id: CONPAR-068
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 68
title: Parallel Functional Evaluation
status: complete
last_verified: 2026-08-29
---

# Parallel Functional Evaluation

## One-Page Review

### Governing question

When may a functional expression's subcomputations be evaluated in parallel without changing its specified value, termination, exception, effect, space, or resource behavior, and when is doing so actually profitable?

### Essential definitions

- A **pure expression** has no externally observable effect and its value depends only on explicit inputs.
- A **redex** is a reducible expression; an evaluation strategy determines which redexes may reduce and when.
- **strict/eager evaluation** evaluates required arguments before function application; **nonstrict evaluation** need not evaluate an unused argument.
- **call-by-need** shares a demanded computation so it is evaluated at most once and its result is memoized.
- A **future** is a handle to a computation that may proceed concurrently and blocks or suspends a consumer when its value is demanded.
- A **spark** is a hint that an expression is a candidate for parallel evaluation; the runtime may discard or convert it to work.
- A **dependency DAG** contains one node per unit of work and edges for value dependencies.
- **work** `T_1` is total computation cost; **span** `T_∞` is critical-path cost with unbounded processors.
- **parallelism** `T_1/T_∞` is an upper bound on useful processor count in the ideal model.
- **granularity** is useful work per scheduled task relative to creation, communication, synchronization, and allocation overhead.
- A **deterministic reduction** fixes the value-relevant grouping/order or uses an operator whose actual semantics make alternatives equivalent.
- **effect isolation** keeps I/O, mutation, time, randomness, exceptions, cancellation, and resource decisions outside or explicitly ordered around the pure parallel core.

### Central model, mechanism, or theorem

Translate an expression into a value-dependency DAG G. A scheduler may evaluate any ready pure node while preserving dependencies. If each node is deterministic, demanded nodes terminate, and parallel evaluation does not force an expression that sequential semantics would leave unevaluated in a value-relevant way, every schedule produces the same value. The ideal lower bound is `max(T_1/P,T_∞)` on P processors; greedy/work-stealing results approach `O(T_1/P + T_∞)` only under stated structured-computation and cost assumptions. Purity supplies semantic freedom, not free speedup.

### Critical invariants

Parallel tasks read immutable inputs or isolated state. Single-assignment results publish once and consumers wait correctly. Sharing prevents duplicate evaluation where the semantics/cost contract requires it. The strictness transformation preserves value, termination, and exception behavior claimed. Task creation is bounded by granularity policy. Reductions use stable identities and numeric semantics. Exceptions and cancellation select deterministic outcomes or are explicitly nondeterministic. A task cannot outlive resources it captures. Memo tables do not expose duplicate effects. Space retention, black holes/cycles, nested parallelism, oversubscription, and foreign blocking are measured. Result equivalence is tested independently from performance.

### Common failures

Programs call code pure while it reads time, randomness, mutable caches, addresses, or I/O; evaluate both conditional branches speculatively; turn a lazy terminating program into a diverging one; duplicate shared thunks; create a future for each tiny element; flatten nested parallelism into excessive memory; reduce floating point in schedule order; let “first exception” depend on timing; cancel a task after it emitted an effect; deadlock on cyclic futures; retain entire input graphs through thunks; block worker pools on foreign calls; or report processor utilization as algorithmic speedup.

### Compact example

A balanced eight-leaf sum tree has 15 unit-cost nodes and span 4: one leaf level and three combine levels. Its ideal parallelism is `15/4=3.75`; with four processors the lower bound is 4 time units, while actual time also includes task and memory overhead. An unbalanced left fold has the same 15 nodes but span 8, limiting parallelism to 1.875. Evaluation tree shape matters even for a pure associative operation.

### Connections

[Task Parallelism and Dependency Graphs](041-task-parallelism-and-dependency-graphs.md) supplies DAG scheduling. [Parallel Loops and Reductions](044-parallel-loops-and-reductions.md) supplies aggregation. [Deterministic Parallel Execution](065-deterministic-parallel-execution.md) supplies observation contracts, and [Immutable Snapshots and Multi-Version State](067-immutable-snapshots-and-multi-version-state.md) supplies safe shared values.

## Governing Question

Which semantic equivalences justify parallel functional evaluation, how should the runtime expose and schedule that parallelism, and which cost, space, failure, and effect boundaries prevent a theoretically parallel expression from becoming a reliable production speedup?

“No mutation” removes a major source of interference. It does not decide evaluation order, strictness, exceptions, memory use, granularity, numeric grouping, or external effects.

## Why This Matters

Functional structure makes dependencies explicit: a function result waits on its arguments, immutable values can be shared, and independent subexpressions need no locks. Divide-and-conquer, trees, maps, folds, dynamic programs, query plans, compilers, simulations, and analytics can expose abundant nested parallelism.

Yet implicit parallelism has repeatedly proved harder than its semantic elegance suggests. Fine-grained work costs more to schedule than compute. Lazy evaluation hides when work occurs and can retain large graphs. Speculation may evaluate unused, failing, or diverging expressions. Memory bandwidth and allocation can dominate. Effects can leak through allegedly pure APIs.

The right goal is controlled semantic freedom plus an explicit cost model. Prove that schedule changes preserve the required observation; then measure whether the selected decomposition, runtime, and machine realize useful speedup.

## Prerequisites and Retrieval

Retrieve:

- work, span, and task DAGs from [Task Parallelism and Dependency Graphs](041-task-parallelism-and-dependency-graphs.md);
- divide-and-conquer structure from [Fork-Join Computation](043-fork-join-computation.md);
- grouping and numeric laws from [Parallel Loops and Reductions](044-parallel-loops-and-reductions.md);
- result determinism from [Deterministic Parallel Execution](065-deterministic-parallel-execution.md); and
- immutable value publication from [Immutable Snapshots and Multi-Version State](067-immutable-snapshots-and-multi-version-state.md).

Retrieval prompt: draw dependency DAGs for `(f a) + (g b)` and for a left fold over eight values. Identify ready nodes, work, span, and the assumptions required to evaluate `f a` and `g b` concurrently.

## Learning Objectives

After completing this module, a learner can:

1. state semantic conditions for schedule-independent pure evaluation;
2. distinguish eager, lazy, call-by-need, futures, sparks, and dataflow variables;
3. compute work, span, parallelism, and processor lower bounds from a DAG;
4. design balanced divide-and-conquer and nested parallel evaluation;
5. select granularity, cutoff, chunking, and work-stealing policies;
6. preserve termination, exception, cancellation, and reduction semantics;
7. isolate mutation, memoization, I/O, time, randomness, and foreign calls;
8. diagnose space leaks, duplicate work, black holes, oversubscription, and bandwidth limits;
9. construct correctness, determinism, performance, and resource evidence separately; and
10. scope higher-assurance review for functional parallel computation.

## Core Exposition

### Values, effects, and observations

For a closed pure expression e, denotational reasoning treats evaluation as finding one value independent of reduction order when the language calculus has the required confluence and e terminates. A real language adds partiality, exceptions, resource limits, floating point, unsafe operations, pointer identity, weak references, finalizers, and effects. The production contract must decide which are observed.

Parallel evaluation is safe for value equivalence when independent deterministic subexpressions share no mutable effects and their results combine through a deterministic function. But evaluating more than the sequential strategy can change termination or failure. `if true then 1 else loop()` terminates under ordinary conditional semantics; speculatively evaluating both branches may not. Likewise an unused argument that throws must remain unused if exceptions are observable.

Referential transparency supports substitution: equal expressions can replace one another without changing program meaning. It does not assert equal cost. Duplicating an expensive pure expression preserves value but can destroy performance or termination under resource bounds.

### Evaluation strategies

Call-by-value evaluates arguments before a call. Independent arguments can run concurrently, but all are demanded. Call-by-name substitutes unevaluated expressions and may recompute them. Call-by-need adds sharing: the first demand evaluates a thunk, other demands wait, and the thunk becomes the value.

Parallel call-by-need may spark thunks before demand. A spark can be ignored when workers are busy, preserving semantics and limiting overhead. If converted to a task, the runtime must synchronize one evaluation, handle concurrent demand, update the thunk atomically, and detect self/cyclic demand (“black holes”) rather than deadlock silently.

Strictness analysis proves an argument is demanded whenever the function returns a value. A compiler may evaluate a proven-strict argument eagerly or unbox it. “Usually demanded” is a profitability observation, not a semantic proof. Exceptions and divergence complicate which equivalence the language promises.

### Futures and single assignment

`future e` conceptually starts e and returns a handle. Touch/demand waits for its value. Futures express producer-consumer overlap and dynamic DAGs. They are simplest when e is pure and the result is single assignment.

A future needs lifecycle semantics: eager or lazy start, executor ownership, priority, cancellation, exception storage, multiple waiters, task-local context, and resource scope. If a future raises, does every touch rethrow the same logical exception? If multiple futures fail, which error is observed? Does abandoning the handle cancel work or merely drop interest?

Structured futures remain within a lexical/task group, ensuring join or cancellation before captured resources close. Unstructured futures can leak computation, hold inputs, or emit late effects. Dataflow variables/I-structures similarly allow one definition and blocking reads; multiple writes are errors rather than races hidden by timing.

### Dependency DAG, work, and span

Build G with nodes weighted by operation cost and edges from producers to consumers. Work `T_1` is the sum of weights. Span `T_∞` is the maximum weighted path. On P processors, `T_P ≥ max(T_1/P,T_∞)`. No scheduler overcomes insufficient parallelism or the critical path.

Greedy scheduling bounds ideal structured computation by roughly `T_1/P + T_∞`; randomized work stealing has related expected bounds for fully strict computations. These results assume an abstract cost model. Real overhead includes task creation, deque contention, stealing, cache misses, allocation/GC, NUMA, synchronization, and operating-system interference.

Parallel slackness means exposing substantially more ready work than processors so load imbalance and variable task sizes can be absorbed. Infinite fine-grained slackness is counterproductive because scheduling and memory overhead grow with tasks.

### Executable work/span model

The following deterministic teaching model computes work and span for balanced and left-associated sum trees with eight leaves. Every leaf and combine has unit cost. It does not execute in parallel or model scheduling overhead, cache, allocation, floating point, or a runtime.

<!-- bijux-verify: {"id":"functional-work-span","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"balanced_value=36\nbalanced_work=15\nbalanced_span=4\nbalanced_parallelism=3.75\nleft_value=36\nleft_work=15\nleft_span=8\nleft_parallelism=1.875\nfour_processor_lower_bound=4\n","stderr":""}} -->
```python
def leaf(value):
    return {"value": value, "work": 1, "span": 1}


def combine(left, right):
    return {
        "value": left["value"] + right["value"],
        "work": left["work"] + right["work"] + 1,
        "span": max(left["span"], right["span"]) + 1,
    }


def balanced(values):
    nodes = [leaf(value) for value in values]
    while len(nodes) > 1:
        next_nodes = []
        for index in range(0, len(nodes), 2):
            next_nodes.append(combine(nodes[index], nodes[index + 1]))
        nodes = next_nodes
    return nodes[0]


def left_associated(values):
    result = leaf(values[0])
    for value in values[1:]:
        result = combine(result, leaf(value))
    return result


balanced_result = balanced([1, 2, 3, 4, 5, 6, 7, 8])
left_result = left_associated([1, 2, 3, 4, 5, 6, 7, 8])
lower_bound = max((balanced_result["work"] + 3) // 4, balanced_result["span"])

print(f"balanced_value={balanced_result['value']}")
print(f"balanced_work={balanced_result['work']}")
print(f"balanced_span={balanced_result['span']}")
print(f"balanced_parallelism={balanced_result['work'] / balanced_result['span']}")
print(f"left_value={left_result['value']}")
print(f"left_work={left_result['work']}")
print(f"left_span={left_result['span']}")
print(f"left_parallelism={left_result['work'] / left_result['span']}")
print(f"four_processor_lower_bound={lower_bound}")
```

Because exact integer addition is associative here, both trees yield 36. Floating-point addition may differ by grouping; balancing then changes value semantics unless the contract fixes or tolerates it.

### Divide-and-conquer and nesting

A balanced recursive computation splits input, evaluates children concurrently, and combines. If halves are balanced, span follows one child per level plus combine, often logarithmic. If partitions are skewed, span approaches work. Parallel quicksort, tree algorithms, merges, and dynamic programs require input-sensitive analysis.

Nested parallelism composes: a parallel map body can itself fork. A runtime should multiplex nested logical tasks onto one worker pool, not create a fresh pool per level. Work stealing naturally exposes local depth-first execution and steals alternative branches, often helping space locality.

Flattening transformations convert nested data parallelism into flat segmented operations. This supports irregular sequences on SIMD/vector hardware but adds representation and materialization cost. Nested-task and flattened-data execution have different locality, load balance, and space profiles.

### Granularity and cutoffs

Fork only when expected useful work exceeds overhead by a safety margin and enough parallel capacity exists. Divide-and-conquer often uses a size/depth cutoff; maps use chunks; adaptive runtimes may inline tasks when queues are full. The threshold is platform/input dependent and should be configuration backed by measurement, not a magic universal constant.

Coarsening reduces task count but may reduce balance. Very large chunks strand processors on skewed inputs; tiny tasks drown in creation and steal traffic. Useful metrics include task-size distribution, ready/running/spark-converted counts, steals, failed steals, inline conversions, wait time, and critical path.

Cutoffs must not change semantics. A sequential base case and parallel recursive case use the same operation order if order matters, or the contract explicitly permits different association. Random streams and stable identities derive from logical input partitions, not worker or cutoff choices.

### Reductions and numerical semantics

A parallel fold needs a monoid-like combine for flexible grouping: identity and associativity under the actual value/error model. Commutativity permits reordering, but stable ordered trees can parallelize noncommutative associative operations. Floating-point addition is not generally associative; concatenation is associative but not commutative.

Fix an index-derived tree for reproducibility across schedules and worker counts. Handle empty inputs, NaN, overflow, signed zero, exceptions, and ties. Numerically stable/reproducible algorithms may use compensated, pairwise, binned, or exact accumulators with different work/span/space.

Map-reduce fusion can avoid intermediate arrays but may change strictness and exception timing. Prove semantic equivalence and measure allocation separately.

### Exceptions, divergence, and cancellation

Parallel children can fail concurrently. “First observed failure” depends on schedule. Deterministic policies include lowest logical task ID, stable input order, or aggregate sorted failures. They may wait longer than fail-fast arrival. State the policy and preserve suppressed failures needed for diagnosis.

Speculative work may diverge although its result is never needed. Bound speculation distance, prioritize demanded work, and cancel orphaned branches. Cancellation in a pure computation changes resource use but not value if partial results remain invisible; unsafe/foreign effects break that reasoning.

Async exceptions or thread interruption can strike allocation, thunk update, memo publication, or foreign code. Masking/cleanup and runtime invariants are language-specific. Do not assume functional syntax makes cancellation safe.

### Memoization and sharing

Memoization maps pure input identity to value/failure. Parallel misses can compute the same entry twice or coordinate through a promise. Duplicate pure computation preserves value but may exceed resource limits; duplicated hidden effects are incorrect. Single-flight coordination needs failure eviction/caching, cancellation, recursion-cycle, key equality, and memory-lifetime policy.

Call-by-need heap updates replace a thunk with a value, an internal mutation hidden behind pure semantics. Publication and waiters must be thread-safe. Retaining memo keys/values can grow without bound; weak references alter caching predictability and interact with GC/finalizers.

Deterministic caching requires canonical keys and versioned function/environment dependencies. A result dependent on locale, time, model file, random source, or external service is not keyed only by explicit arguments.

### Space behavior

Parallel evaluation can retain inputs/results longer than sequential depth-first evaluation. Spawning both halves holds both subgraphs; a slow consumer causes completed futures to accumulate; lazy producer/consumer imbalance builds thunks; flattening materializes arrays; work stealing may multiply stacks under theoretical bounds.

Measure peak live bytes, allocation rate, residency by closure/task type, GC pause/work, future result backlog, maximum frontier width, and per-worker stacks. A time-efficient transformation can be unusable due to space. Blelloch and Greiner's NESL analysis explicitly combines work/depth and reachable-space concerns; practical runtimes require profile evidence.

Use bounded buffers, streaming folds, depth-first local execution, chunking, strict fields, early release, and backpressure. Forcing too much to cure a space leak may destroy laziness/termination, so validate semantics.

### Effects and foreign boundaries

Keep a pure parallel core that produces immutable values or effect descriptions, then interpret effects in a controlled order. If tasks perform I/O concurrently, the program is concurrent effectful computation; ordering, retries, idempotency, cancellation, and partial failure require explicit semantics.

Randomness uses logical task/sample streams. Time is captured input or excluded. Mutable arrays may be safe under uniqueness/regions with disjoint partitions, but the proof replaces broad purity. Foreign calls may block worker threads, use hidden global state, callback, pin memory, or lack cancellation. Use dedicated blocking pools and document thread safety.

GPU/vector offload changes numeric behavior, transfer costs, device failure, and memory lifetime. Treat it as a separate backend configuration with conformance and tolerance tests.

### Scheduling and operations

Work stealing lets busy workers push local work and idle workers steal. Fully strict computations enable useful time/space analyses; arbitrary future dependencies weaken assumptions. Local depth-first execution often preserves cache/space while thieves take older/coarser alternatives.

Priority inversion arises when workers run speculative tasks while a critical demanded task waits. Managed blocking or compensation may be needed when tasks block. Multiprogramming, CPU quotas, affinity, NUMA, heterogeneous cores, and thermal throttling change realized capacity.

Expose runtime observability without perturbing semantics: logical task IDs, spawn/join edges, work/span estimates, queue and steal data, exception/cancellation tree, allocation/residency, backend/configuration, and result digest. Avoid per-node synchronous logging in fine-grained paths.

### Evidence strategy

Prove or test pure-node determinism, dependency completeness, single assignment, sharing, reduction laws, strictness/termination, deterministic error policy, lifetime, and effect isolation. Compare parallel results with a trusted sequential reference across scheduler seeds, worker counts, cutoffs, chunking, stealing, cancellation, failures, and backends.

Use property-based expression/DAG generation with small-step or sequential oracle. Include unused divergent/failing branches, cyclic futures, duplicate demands, empty/single/skewed inputs, deep nesting, memo races, allocation failure, and numeric extremes. Race, memory, and sanitizer tools cover runtime boundaries.

Benchmark after warmup with fixed inputs and provenance. Report work, span estimate, elapsed/CPU, speedup, efficiency, allocation, peak memory, GC, steals, bandwidth, and variance. Compare against the best sequential implementation, not an intentionally slow baseline. Equal values do not prove performance; a speedup does not prove semantic equivalence.

## Definitions and Notation

- `e ⇓ v`: expression e evaluates to value v under the declared semantics.
- `G=(V,E)`: value-dependency DAG.
- `T_1`: total work (one-processor abstract time).
- `T_∞`: span/critical-path abstract time.
- `T_P`: execution time on P processors.
- `Π=T_1/T_∞`: average available parallelism.
- `S_1`, `S_P`: sequential and P-processor space under a stated scheduler/model.
- `spark(e)`: optional parallel-evaluation hint for e.
- `touch(f)`: demand the result of future f.
- `obs(e)`: declared observation including value and any selected failure/termination/resource behavior.

The value-preservation target is `obs(e_sequential)=obs(e_parallel)` for all permitted schedules and configurations in scope. A cost claim additionally names machine, runtime, input distribution, and measurement protocol.

## Mechanisms, Invariants, or Proof Structure

### Pure DAG induction

Source nodes compute deterministic values from captured inputs. Assuming predecessors have unique values, a pure deterministic node computes one value regardless of ready-node schedule. Topological induction yields unique sink values. This proof does not cover premature forcing, divergence, effects, or incorrect dependency edges.

### Work/span bound

Every P-processor schedule takes at least `T_1/P` by total capacity and at least `T_∞` by dependencies. Under a greedy scheduler, each step with P ready nodes charges full work capacity; a step with fewer ready nodes lies on progress toward the critical path, producing an upper bound proportional to `T_1/P + T_∞` in the model.

### Strictness-preservation obligation

For every expression moved earlier or evaluated speculatively, prove the sequential semantics demands it whenever the original observation completes, or prove its extra divergence/failure/resource use is unobservable under the stated contract. Purity alone proves neither demand nor termination.

### Structured-lifetime proof

Each spawned computation belongs to one scope. On scope success all required children joined; on failure/cancellation remaining children receive cancellation and are awaited/contained before captured resources close. Induction over the task tree prevents orphan tasks and late access.

## Alternatives and Trade-Offs

| Approach | Main benefit | Principal limitation |
|---|---|---|
| Sequential functional evaluation | simplest semantics/cost | no multicore speedup |
| Explicit futures | clear producer-consumer overlap | placement, lifecycle, blocking |
| Sparks/parallel hints | runtime can suppress excess work | unpredictable conversion/performance |
| Strict parallel fork/join | structured DAG and joins | can force unused work |
| Lazy parallel evaluation | preserves demand opportunities | thunk synchronization and space complexity |
| Nested task parallelism | compositional irregular algorithms | scheduler/task overhead |
| Flattened data parallelism | vector/SIMD/GPU suitability | transformation/materialization cost |
| Work stealing | dynamic balance for structured tasks | steals, locality, assumptions |
| Pure core plus ordered effects | strong semantic boundary | buffering and effect-commit latency |

Prefer the smallest annotation/decomposition that exposes coarse, dependency-correct work while leaving the runtime room to schedule. Preserve a sequential path for reference and small inputs.

## Failure Modes and Misconceptions

- **“Pure code automatically runs in parallel.”** A runtime needs explicit or inferred work and a cost-effective scheduler.
- **“Purity guarantees speedup.”** Span, overhead, locality, bandwidth, and space set limits.
- **“Any reduction tree is equivalent.”** Machine numeric and error semantics may differ.
- **“Parallel evaluation preserves laziness.”** It may force unused failure or divergence.
- **“A future is only a value.”** It also owns lifecycle, exception, cancellation, and resources.
- **“Duplicate pure work is harmless.”** Resource exhaustion and latency remain observable.
- **“Memoization is pure.”** Its implementation mutates shared state and retains memory.
- **“More tasks improve balance.”** Fine granularity can dominate useful work.
- **“Nested pools compose.”** They often oversubscribe or deadlock on blocking joins.
- **“Work-stealing bounds apply universally.”** They assume a computation/scheduler/cost model.
- **“High utilization means speedup.”** wasted speculation and GC can keep cores busy.
- **“Effects after mapping are ordered.”** Concurrent task effects follow explicit policy, not collection order automatically.
- **“Functional means no races.”** runtime thunks, caches, unsafe code, and foreign calls can race.
- **“Same value proves equivalence.”** termination, failure, resource, and effect observations may differ.
- **“Parallel faster once means production-ready.”** input distribution and tail memory/latency matter.

## Worked Examples

### Example 1

**Independent arguments.** Pure `f(a)` and `g(b)` run concurrently before deterministic `combine`; both are strict. **Conclusion:** dependencies, not source order, determine safe readiness.

### Example 2

**Unused divergence.** `if true then 1 else loop()` is speculatively forked and consumes a worker forever. **Conclusion:** purity does not preserve termination under extra evaluation.

### Example 3

**Balanced sum.** Eight leaves give work 15 and span 4; a left tree gives span 8. **Conclusion:** expression association controls available parallelism.

### Example 4

**Tiny futures.** One future per integer addition costs more than the addition. Chunked leaves followed by a balanced tree win. **Conclusion:** semantic parallelism needs granularity.

### Example 5

**Floating reduction.** Worker-arrival grouping changes low bits. Use an index-fixed tree or reproducible accumulator. **Conclusion:** schedule-independent purity does not make floating addition associative.

### Example 6

**Concurrent failures.** Tasks 3 and 8 fail; arrival order varies. Report lowest logical ID or stable aggregate. **Conclusion:** exception selection is an observation.

### Example 7

**Single-flight memo.** Two demands for key K share one promise; recursion on K detects a cycle; cancellation does not poison future callers unintentionally. **Conclusion:** pure interfaces contain concurrent mutable machinery.

### Example 8

**Space leak.** A producer sparks an entire lazy list while a slow consumer retains the head, growing residency. Bounded chunks/backpressure restore space. **Conclusion:** shorter time can require much larger space.

### Example 9

**Foreign blocking.** All compute workers enter blocking C calls while their continuations wait. A dedicated blocking pool preserves compute progress. **Conclusion:** executor capacity is part of the boundary.

### Example 10

**Genomic evidence pipeline.** Parallel pure stages must bind reference data, numeric/reduction semantics, random streams, failure policy, provenance, memory bounds, and external publication; reproducible values do not establish biological or clinical validity. Named clinical-genetics, molecular-biology, bioinformatics, statistical/numerical, concurrency/runtime, security/privacy, laboratory, quality/regulatory, operations, and independent safety reviewers must approve intended use and evidence; none is claimed here. **Conclusion:** functional determinism is one layer of high-stakes assurance.

## Cross-Program Connections

- **Programming-language semantics:** confluence, strictness, laziness, effects, and exceptions define legal schedules.
- **Algorithms:** work, span, balancing, associativity, and nested parallelism define theoretical opportunity.
- **Runtime systems:** futures, thunks, work stealing, GC, locality, and blocking realize the DAG.
- **Numerical computing:** grouping and machine arithmetic constrain reproducible reductions.
- **Software engineering:** structured lifecycle, reference implementations, profiling, and regression evidence support maintainability.
- **Distributed systems:** futures and dataflow extend to remote latency but add failure and partial availability.
- **Security:** hidden effects, stale caches, resource denial, and unsafe foreign code limit purity claims.
- **Safety engineering:** stable provenance and independent domain validation remain necessary beyond deterministic computation.

## References

1. Robert H. Halstead Jr., “MULTILISP: A Language for Concurrent Symbolic Computation,” *ACM TOPLAS* 7(4), 1985. <https://doi.org/10.1145/4472.4478>
2. Cormac Flanagan and Matthias Felleisen, “The Semantics of Future and Its Use in Program Optimization,” POPL 1995. <https://doi.org/10.1145/199448.199484>
3. Richard P. Brent, “The Parallel Evaluation of General Arithmetic Expressions,” *Journal of the ACM* 21(2), 1974. <https://doi.org/10.1145/321812.321815>
4. Robert D. Blumofe and Charles E. Leiserson, “Scheduling Multithreaded Computations by Work Stealing,” *Journal of the ACM* 46(5), 1999. <https://doi.org/10.1145/324133.324234>
5. Guy E. Blelloch, Jonathan C. Hardwick, Siddhartha Chatterjee, Jay Sipelstein, and Marco Zagha, “Implementation of a Portable Nested Data-Parallel Language,” PPOPP 1993. <https://doi.org/10.1145/155332.155343>
6. Guy E. Blelloch and John Greiner, “A Provable Time and Space Efficient Implementation of NESL,” ICFP 1996. <https://doi.org/10.1145/232627.232650>
7. Philip W. Trinder, Kevin Hammond, Hans-Wolfgang Loidl, and Simon L. Peyton Jones, “Algorithm + Strategy = Parallelism,” *Journal of Functional Programming* 8(1), 1998. <https://doi.org/10.1017/S0956796897002967>
8. Simon Marlow, Simon L. Peyton Jones, and Satnam Singh, “Runtime Support for Multicore Haskell,” ICFP 2009. <https://doi.org/10.1145/1596550.1596563>
9. Rishiyur S. Nikhil and Arvind, *Implicit Parallel Programming in pH*, Morgan Kaufmann, 2001. <https://shop.elsevier.com/books/implicit-parallel-programming-in-ph/nikhil/978-0-08-050852-8>
10. Guy E. Blelloch, *NESL: A Nested Data-Parallel Language*, CMU-CS-93-129, 1993. <https://www.cs.cmu.edu/~scandal/papers/CMU-CS-93-129.html>

## Exercises

### Exercise 1

State and prove value equivalence for parallel evaluation of two strict pure arguments. Then show why unused divergence and exceptions invalidate a broader claim.

### Exercise 2

For a sixteen-leaf balanced binary computation with unit leaves and combines, calculate work, span, ideal parallelism, and lower bounds for 1, 2, 4, 8, and 16 processors. Contrast a left-associated tree.

### Exercise 3

Design a parallel lazy map/fold using sparks or futures. Specify demand, sharing, granularity, reduction, exceptions, cancellation, memoization, and space bounds.

### Exercise 4

Diagnose a pure divide-and-conquer program that slows and uses ten times more memory on eight cores. Give an instrumentation, experiment, and redesign plan.

### Exercise 5

A parallel scientific analysis must be reproducible across approved CPU counts and backends. Specify semantic, numeric, scheduling, performance, provenance, and human-review evidence.

## Answers to the Exercises

### Answer 1

Let f(a) and g(b) be deterministic, terminating, pure, and demanded by a strict deterministic combine c. Their nodes have no dependency between them, only edges into c. Either schedule produces unique x=f(a) and y=g(b); c(x,y) is unique, so topological induction gives equal value. Single-assignment publication and lifetime must be correct in the implementation. This does not justify evaluating an unselected conditional branch or unused nonstrict argument: a pure unused expression may diverge or throw. Parallel forcing then changes termination/error observation even though it cannot mutate the selected value. Prove strict demand or explicitly weaken the contract before moving evaluation earlier.

### Answer 2

Sixteen leaves plus fifteen combines give `T_1=31`. A balanced tree has leaf level plus four combine levels, so `T_∞=5` and parallelism `31/5=6.2`. Lower bounds `max(ceil(31/P),5)` are 31, 16, 8, 5, and 5 for P=1,2,4,8,16. Actual schedules add overhead. A left-associated tree has one initial leaf followed by fifteen combines, each also introducing one new leaf in parallel with the accumulated chain; its critical chain is 16 and parallelism 1.9375, so more than about two processors cannot help ideally. Exact integer addition preserves value; floating semantics require fixed grouping or a scoped tolerance/reproducible accumulator.

### Answer 3

Partition input into bounded chunks. Spark pure chunk maps only within a maximum lookahead; demand converts/executes missing work. Each chunk result is one promise so concurrent consumers share evaluation. Reduce chunks through a fixed index-derived balanced tree with defined empty/exception/numeric rules. Choose a cutoff from measured work versus spawn/allocation cost. Use stable task IDs and report lowest-ID or stable aggregate failures. Scope all futures under the fold; on cancellation stop and join unused chunks before releasing input. Memoize only with complete deterministic keys, single-flight/cycle detection, bounded eviction, and intentional failure/cancellation policy. Bound ready/completed chunks to apply backpressure and measure peak residency. Do not parallelize hidden effects; return effect descriptions for ordered interpretation.

### Answer 4

Record DAG/task sizes, work/span estimate, ready/running tasks, sparks created/converted/discarded, steals/failures, worker wait/block, elapsed/CPU, allocation by task type, peak live bytes, retained roots, GC, cache/NUMA/bandwidth, and cutoff decisions. Compare the best sequential build with P=1,2,4,8 under fixed inputs and multiple repetitions; vary cutoffs and input skew. Likely causes include tiny tasks, low span parallelism, bandwidth saturation, duplicated speculation, lost depth-first locality, and simultaneous subtree retention. Increase cutoffs/chunking, keep local depth-first execution, cap lookahead/frontier, eliminate duplicate demands, stream combines, free child results promptly, use one nested pool, and isolate blocking calls. Revalidate equal results, error/cancellation behavior, and memory bounds before accepting speedup.

### Answer 5

Define captured inputs, algorithms, dependency versions, machine arithmetic, compiler/runtime, backend, worker count scope, and observed outputs/errors. Prove pure stages and complete dependencies; assign stable logical IDs/random streams; fix reduction trees or use a reproducible numeric method with error bounds. Test against an independent sequential/reference implementation across scheduler seeds, cutoffs, chunks, workers, CPU architectures, vector widths, GPU/backend modes, numeric extremes, cancellation, faults, and resource pressure. Record source/configuration/artifact digests, work/span, elapsed/CPU, allocation/peak memory, GC, transfers, retries, variance, and semantic hashes. Distinguish bitwise equality, bounded numerical agreement, scientific validity, and performance. Named domain-science, statistical/numerical, algorithm, concurrency/runtime, compiler/hardware, data-provenance, security, quality/reproducibility, operations, and independent assurance reviewers must approve methods, tolerances, reference data, performance envelope, and residual uncertainty; parallel reproducibility alone is not scientific or deployment validity.
