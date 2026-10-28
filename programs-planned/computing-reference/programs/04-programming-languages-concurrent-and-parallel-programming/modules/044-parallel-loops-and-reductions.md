---
module_id: CONPAR-044
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 44
title: Parallel Loops and Reductions
status: complete
last_verified: 2026-08-29
---

# Parallel Loops and Reductions

## One-Page Review

### Governing question

When may a loop's iterations execute in parallel, and how should scheduling, variable scope, reduction algebra, ordering, failure, and numerical reproducibility be specified so the result remains meaningful?

### Essential definitions

- A **parallel loop** assigns iterations from a finite iteration space to concurrent workers under a declared schedule.
- A **canonical iteration space** has enumerable bounds and a well-defined mapping from logical iteration identity to work.
- A **loop-carried dependence** requires one iteration to observe an operation from another iteration.
- A **private variable** has an independent instance per worker or logical task; a **shared variable** denotes common storage.
- **Static scheduling** assigns chunks before execution; **dynamic scheduling** assigns new chunks as workers become available.
- **Guided scheduling** decreases chunk size as remaining work shrinks, subject to a minimum and runtime contract.
- A **chunk** is a group of iterations assigned as one scheduling unit.
- A **reduction** maps iterations to partial accumulators and combines them under a declared operation.
- A **reduction identity** is the neutral accumulator value; **associativity** permits regrouping.
- An **ordered region** serializes a specified effect in logical encounter order while other loop work may remain parallel.

### Central model, mechanism, or theorem

For iteration `i` with read/write sets `R_i,W_i`, arbitrary parallel execution is safe only when distinct iterations have no unhandled conflicting accesses or required effect order. A reduction replaces a shared update with owned partials `p_k`, then combines them. If combine `op` is associative over the actual accumulator domain and has identity `e`, a tree may regroup partials without changing the declared meaning; commutativity is additionally needed if operand order may change. Loop time is bounded by total work, dependence span, maximum chunk cost, scheduling overhead, and memory/resource bottlenecks—not iteration count alone.

### Critical invariants

Iteration bounds are valid and every required iteration executes exactly once unless cancellation/early-exit semantics say otherwise. Each ordinary output location has one writer or correct synchronization. Variable sharing/private initialization/copy-out rules are explicit. Reduction identity, lift, combine, ordering, overflow, and empty-domain behavior are correct. Every local partial is initialized once and combined once. Schedule choice cannot alter public semantics. Barriers/ordered regions have consistent participation. Exceptions and cancellation settle started iterations, and aggregate success publishes only after the loop's required synchronization.

### Common failures

Code parallelizes a recurrence; captures the loop index by a mutable reference; accidentally shares scratch state; uses a critical section around every addition; chooses static equal counts for skewed costs; chooses tiny dynamic chunks and spends time scheduling; assumes `lastprivate` means last to finish; relies on completion order for output; uses subtraction or average as an invalid reducer; ignores integer overflow or floating regrouping; nests parallel loops into oversubscription; returns from one iteration as if it breaks the loop; or catches one exception while other iterations continue mutating state invisibly.

### Compact example

Iterations over values 1–12 are split statically into `[0,4)`, `[4,8)`, and `[8,12)`. Each worker computes an owned sum-of-squares partial: 30, 174, and 446, plus two even values. A deterministic tree combines partials to 650 and the even count to six. Coverage proves every index appears once. This exact-integer teaching trace demonstrates schedule-independent reduction meaning, not parallel execution or optimal chunking.

### Connections

[Data Parallelism and Bulk Operations](042-data-parallelism-and-bulk-operations.md) establishes independence and reduction algebra; [Fork-Join Computation](043-fork-join-computation.md) establishes nested execution and joins. The [program roadmap](../ROADMAP.md) next examines partitioning and granularity directly.

## Governing Question

How should an engineer transform a sequential loop into a parallel loop while proving dependence legality, choosing a schedule, and retaining a precise result, lifecycle, and performance contract?

A parallel-loop directive or API is a request to reorder work, not a proof that reordering is valid.

## Why This Matters

Loops dominate scientific computing, analytics, simulation, media processing, compilers, and machine learning. When iterations are independent or reducible, loop parallelism exposes cores with less manual task plumbing than an explicit graph. Compilers and runtimes can schedule chunks, vectorize inner work, build reduction trees, and manage joins.

The concise syntax is dangerous when it hides assumptions. Sequential source order may protect a recurrence, alias, file position, allocator, random stream, or exception choice. A loop variable can be private while referenced objects remain shared. A correct sum can become numerically different after regrouping. A “balanced” schedule by iteration count can place all costly cases on one worker.

Production design therefore separates three questions: is concurrent iteration semantically legal; which scheduling/resource policy fits the cost distribution; and which synchronization, reduction, failure, and reproducibility contract defines completion?

## Prerequisites and Retrieval

Retrieve:

- race and invariant reasoning from [Critical Sections and Shared-State Invariants](008-critical-sections-and-shared-state-invariants.md);
- atomic combine semantics from [Atomic Read-Modify-Write Operations](025-atomic-read-modify-write-operations.md);
- false sharing from [False Sharing and Cache-Line Contention](029-false-sharing-and-cache-line-contention.md);
- task work/span from [Task Parallelism and Dependency Graphs](041-task-parallelism-and-dependency-graphs.md);
- data dependence and reduction laws from [Data Parallelism and Bulk Operations](042-data-parallelism-and-bulk-operations.md); and
- structured completion from [Fork-Join Computation](043-fork-join-computation.md).

Retrieval prompt: for loop iteration `i`, list reads, writes, effects, private state, reduction contribution, and required order; then give a counterexample input for each unproved assumption.

## Learning Objectives

After completing this module, a learner can:

1. determine whether a loop has true, anti-, output, control, or effect dependencies;
2. state variable scoping and publication rules for a parallel-loop API;
3. compare static, dynamic, guided, cyclic, and ordered schedules;
4. choose chunk size from overhead, skew, locality, and cancellation constraints;
5. design a reduction with valid identity, lift, combine, and empty behavior;
6. distinguish ordered, commutative, reproducible, and numerically tolerant results;
7. remove shared hot updates with owned partial accumulators;
8. specify exception, cancellation, early-exit, nested-loop, and cleanup behavior;
9. diagnose false sharing, oversubscription, bandwidth limits, and schedule imbalance; and
10. verify semantic equivalence and scaling using structural and empirical evidence.

## Core Exposition

### Define the iteration space

A parallel loop needs stable logical iteration identities. A counted range `[lo,hi)` with stride has a clear finite domain when bounds do not overflow and mutation cannot change them during execution. Collection traversal requires the collection not be structurally invalidated, unless the API supplies concurrent iteration semantics.

Iteration identity is independent of worker, chunk, or completion position. Preserve the logical index with outputs and diagnostics. Dynamic scheduling can execute index 90 before index 2; that must not change product meaning.

Canonical-loop restrictions in systems such as OpenMP exist so runtimes can enumerate and divide work. Exact permitted syntax and overflow behavior are specification/version-specific. A compiler accepting a directive is not evidence that the loop has no semantic dependence.

### Prove iteration independence

For distinct iterations `i,j`, compare read/write sets. A conflict exists if one writes a location the other reads or writes. A recognized reduction, atomic update, lock, dependence directive, or transformed algorithm may govern that conflict; otherwise arbitrary concurrent execution races or changes meaning.

`out[i]=f(in[i])` is independent only if output locations are disjoint, inputs are stable, and hidden aliases/effects do not cross iterations. `a[i]=a[i-1]+x[i]` has a true dependence and needs scan/reformulation. `a[index[i]]+=x[i]` may collide and needs atomics, privatization, grouping, or unique-index proof.

Effects can be dependent without sharing memory. Appending lines, consuming one random generator, updating a transaction, or requesting a rate-limited service introduces order, contention, or external lifecycle. Compute pure indexed results in parallel and perform ordered effects afterward when possible.

### Variable data-sharing attributes

Loop index is normally private under parallel-loop constructs, but surrounding variables follow language/API rules. `shared` storage is one object. `private` often creates uninitialized/default per-worker instances; `firstprivate`-style behavior copies an initial value; `lastprivate`-style behavior copies from the logically last iteration, not whichever worker finishes last.

A private reference variable can still point to shared mutable data. Deep object ownership is not created by a scoping clause. Closure capture can accidentally bind one mutable index or buffer; capture stable values or partition-owned slices.

Per-worker scratch reduces contention but its lifetime and size multiply by worker count. Initialize before use, reset between chunks when required, combine/dispose exactly once, and do not assume a logical iteration always runs on the same worker across scheduling points.

### Static scheduling

Static scheduling assigns work deterministically or predictably before execution. Contiguous blocks favor spatial locality and stable ownership. Cyclic static chunks distribute regular periodic cost patterns but cause strided access. Specification details determine exact mapping when chunk size is omitted.

Static scheduling has low assignment overhead and can support affinity. It balances when iteration cost is uniform or the partition accounts for weights. One expensive block controls completion under skew.

Static mapping may improve repeatability of a fixed reduction tree in a particular runtime, but do not infer a portable numeric order unless the API promises it. Worker IDs and counts can change across environments.

### Dynamic and guided scheduling

Dynamic scheduling exposes chunks from a shared/distributed work source. Workers request another after finishing, so fast workers process more chunks. It handles irregular cost but adds scheduling synchronization, reduces placement predictability, and can disrupt cache/NUMA locality.

Chunk size trades balance against overhead. Unit chunks react best to variance but maximize queue operations. Large chunks amortize scheduling but leave a straggling tail. Guided schedules start larger and shrink as work decreases, attempting to combine amortization with tail balance; exact formula and minimum are runtime-specific.

Runtime/adaptive scheduling can defer the policy decision to an environment setting. Useful for tuning, it weakens reproducibility if deployments do not record the chosen policy. Treat schedule and chunk as observable configuration when performance or order depends on them.

### Loop barriers and nowait

Many parallel-loop constructs have an implicit barrier at the end. It ensures all iterations complete and publishes their results according to the memory model before subsequent dependent work. Removing it with a `nowait`-style clause is legal only when no subsequent operation needs unfinished iterations and the enclosing region still owns them.

Adjacent independent loops can omit a barrier to overlap, but if loop two reads outputs from loop one at corresponding or arbitrary indices, a global or finer dependency is required. An accidental missing barrier creates intermittent stale reads; an unnecessary barrier serializes phases and amplifies stragglers.

All required participants must encounter matching barriers. Conditional exit or exception behavior is API-specific. Do not put a collective barrier in an iteration branch unless the model guarantees identical membership.

### Ordered effects

An ordered region allows a designated portion to execute in logical iteration order while other computation remains parallel. It is appropriate when output order is required and effect cannot be deferred. It creates a serial critical path and may retain completed iterations waiting for predecessors.

Often a better design computes `(index,result)` in parallel, stores one result per index, joins, then emits sequentially. This bounds ordered-region contention but can require output memory. Streaming large results may need a bounded reorder buffer and backpressure.

Never rely on a critical section for logical order. Mutual exclusion prevents overlap but admits workers in schedule order. An explicit ordered construct or indexed assembly defines order.

### Reduction construction

A reduction has four components: lift an iteration value into accumulator state, initialize with identity, combine accumulators, and finalize. For sum of squares, lift `x` to `x*x`, identity is zero, combine is addition, finalize is identity. For average, accumulator is `(sum,count)` and finalization divides; “average of averages” is wrong for unequal partitions.

Associativity permits regrouping. Identity must be neutral for every valid accumulator and must not be shared mutable state. Commutativity is needed if the runtime changes operand order; an ordered tree can preserve noncommutative associative operations such as sequence concatenation.

For minimum without a natural bounded identity, use an option/nonempty reducer or domain-approved sentinel. For checked integer sum, combine can fail; the reduction then needs deterministic error and partial-state policy. Custom reducers must specify copy/initialization/destruction and thread safety under the target API.

### Privatization versus hot shared updates

Updating one shared counter under a critical section serializes iterations. Atomic addition removes the lock but still contends on a cache line and defines a schedule-dependent order for floating point. Per-worker or per-chunk partials keep hot updates local, then combine in `O(partials)` work and logarithmic ideal tree span.

Histograms can privatize all bins, but memory is `workers*bins`; large/sparse domains may require blocked bins, maps, sort/group, or atomics. Adjacent partial accumulators can falsely share; align/pad or give each worker a sufficiently separated local object, then measure.

Partial identity should be logical chunk or stable range when deterministic diagnostics matter, not worker identity. Dynamic scheduling can give one worker multiple chunks and a chunk can be retried under some frameworks.

### Integer and floating arithmetic

Machine integer addition may wrap, trap, saturate, or invoke undefined behavior depending on language/type/mode. Associativity holds differently: modular wrap addition is associative, but checked addition can fail at intermediate groupings even when a mathematical total fits or vice versa. Specify accumulator width and error behavior.

Floating addition is not associative because each operation rounds. A parallel reduction tree changes grouping and can change low bits or catastrophic-cancellation behavior. “Within epsilon” needs domain-derived absolute, relative, or ULP criteria and treatment of zero, subnormals, NaN, and infinity.

Options include a fixed partition/tree and arithmetic environment for bitwise reproducibility, pairwise summation for improved typical error, compensated local accumulators, higher precision, or exact/superaccumulator methods. Compiler fast-math and device contraction modes are part of the contract.

### Multiple reductions and compound state

A loop may compute sum, count, min, max, errors, and diagnostics. Separate reductions can traverse once but have coordinated failure semantics. A compound accumulator can preserve relationships—for example `(sum,count)`—but increases combine complexity.

For deterministic diagnostics, each iteration returns `(index,outcome)`, partials retain a bounded set under a stable selection policy, and finalization sorts/selects by index. “First error observed” is schedule-dependent. If all errors are unbounded, define cap, truncation, and total-error count.

Reduction finalization occurs after all required partials arrive. Publishing fields from a partially combined accumulator exposes an invalid snapshot unless the API explicitly supports streaming monotonic aggregates.

### Early exit, exceptions, and cancellation

A sequential `break` means no later iteration executes. In a parallel loop, later iterations may already be running or complete. APIs may prohibit break, provide cooperative cancellation, or return an arbitrary/lowest match under specialized algorithms. Define whether the goal is any match, first encounter-order match, minimum index, or all matches.

Exceptions may be captured and rethrown, aggregated, terminate a process, or be unsupported in device code. Other iterations can continue after one fails. Effects already committed remain. Stable error policy must distinguish prompt notification from final cleanup.

Cancellation stops admission where possible, signals running chunks, waits/synchronizes started work, disposes local partials, and prevents aggregate success publication. Chunk size bounds observation latency. Retrying iterations with effects requires stable identity and idempotency.

### Nested loops and collapse

Nested iteration spaces may parallelize the outer loop, inner loop, or a collapsed Cartesian space. Outer-only parallelism preserves inner locality but may expose too few tasks. Inner parallelism repeated per outer item can pay setup each time. Collapse improves work supply but changes mapping/locality and needs valid rectangular/canonical bounds under the API.

Nested parallel regions can oversubscribe or serialize depending on runtime configuration. A parallel outer loop calling a library that internally parallelizes may create `P^2` work. Establish one processor budget and decide which layer owns parallelism.

Triangular or dependent bounds need explicit linearization or tasking; naive rectangular collapse can execute invalid points. Preserve logical `(i,j)` identity for outputs and dependence proofs.

### Locality, bandwidth, and vectorization

Contiguous chunks favor cache lines and prefetch. Cyclic/dynamic schedules may scatter accesses. Loop fusion can reuse data but reduce scheduling freedom; fission can separate dependencies or working sets. Tiling improves cache reuse for multidimensional loops.

Multiple cores often saturate memory bandwidth before CPU. If each iteration performs one addition after loading large arrays, speedup plateaus. Report bytes, arithmetic intensity, cache misses, and bandwidth—not only CPU utilization.

Thread-level parallelism and SIMD can compose. Ensure inner vector lanes satisfy dependence/alias/alignment/tail requirements. A parallel directive does not prove vectorization; inspect compiler reports/generated code and benchmark equivalent results.

### Verification and performance evidence

Start with a sequential oracle. Test empty/one, below/at/above chunk and worker counts, nondivisible trip counts, zero/negative stride where legal, maximum bounds, aliasing, repeated scatter keys, skew, failure, cancellation, nested execution, and numeric extremes.

Property checks assert coverage exactly once, output-by-index equality, reduction laws over generated small accumulators, and invariance across legal worker/chunk schedules within the declared result equivalence. An invalid law should have a concrete counterexample.

Benchmark sequential and parallel paths with identical validation/effects. Record hardware/topology, compiler/runtime/version, flags, schedule/chunk, workers, affinity, input distribution, warm-up, repetitions, uncertainty, allocations, and result verification. Report overhead and break-even size. A single speedup proves only that measurement.

## Definitions and Notation

Iteration domain is finite set `I`. Iteration `i` has read set `R_i`, write set `W_i`, cost `c_i`, and effect set `E_i`. Unordered independence requires no ungoverned cross-iteration conflict or required effect order.

A schedule partitions or assigns `I` into chunks `C_k`. Exact-once coverage requires `union_k C_k=I` and `C_j intersect C_k=empty` for distinct non-retry chunks. Makespan is at least `max(sum_i c_i/P, max_k sum_{i in C_k}c_i)` before additional overhead/dependencies.

A reduction is `(A,e,lift,op,finish)`, with accumulator domain `A`, identity `e`, lift from iteration contribution, combine `op`, and finalizer. Associativity and identity apply over reachable accumulator states under actual arithmetic.

If partials are `p_0,...,p_{q-1}`, a fixed ordered tree preserves their operand order; an unordered tree additionally requires commutativity for schedule-independent meaning.

Let scheduling overhead per chunk be `h` in a simplified model. With `q` chunks, overhead includes approximately `q*h` total work while balance improves as maximum remaining chunk cost decreases; actual contention and cache costs are not constant.

## Mechanisms, Invariants, or Proof Structure

Audit a parallel loop in this order:

1. define finite iteration identity, bounds, stride, and overflow behavior;
2. derive read/write/effect sets and prove independence or a governed dependence;
3. state shared/private/initialized/copy-out variables and deep ownership;
4. choose static, dynamic, guided, cyclic, ordered, or custom schedule from cost/locality;
5. prove exact coverage and set chunk size from overhead, skew, locality, and cancellation;
6. define barriers, nowait dependencies, ordered effects, and publication;
7. specify reduction accumulator, identity, lift, combine laws/order, finalizer, and arithmetic;
8. privatize hot state and bound partial memory, false sharing, diagnostics, and expansion;
9. define early match, exception, cancellation, retry, and partial-effect semantics;
10. coordinate nested loops/libraries under one processor and memory budget;
11. verify schedules, laws, numeric edges, failures, and sequential equivalence; and
12. measure break-even/scaling with full schedule, runtime, hardware, and result evidence.

The executable model uses three deterministic static contiguous chunks, owned integer sum-of-squares and even-count partials, and an explicit stable pairwise reduction tree.

<!-- bijux-verify: {"id":"parallel-loop-reduction-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"chunks=[(0, 4), (4, 8), (8, 12)]\npartials=[30, 174, 446]\ntree_levels=[[30, 174, 446], [204, 446], [650]]\ntotal=650\neven_count=6\ncoverage=True\nunique=True\nsequential_equivalent=True\n","stderr":""}} -->
```python
values = list(range(1, 13))
chunks = [(0, 4), (4, 8), (8, 12)]
partials = []
even_partials = []
scheduled_indices = []

for start, end in chunks:
    local_sum = 0
    local_even = 0
    for index in range(start, end):
        value = values[index]
        local_sum += value * value
        local_even += int(value % 2 == 0)
        scheduled_indices.append(index)
    partials.append(local_sum)
    even_partials.append(local_even)

tree_levels = [partials[:]]
current = partials[:]
while len(current) > 1:
    next_level = []
    for index in range(0, len(current), 2):
        if index + 1 < len(current):
            next_level.append(current[index] + current[index + 1])
        else:
            next_level.append(current[index])
    current = next_level
    tree_levels.append(current[:])

total = current[0]
print(f"chunks={chunks}")
print(f"partials={partials}")
print(f"tree_levels={tree_levels}")
print(f"total={total}")
print(f"even_count={sum(even_partials)}")
print(f"coverage={scheduled_indices == list(range(len(values)))}")
print(f"unique={len(set(scheduled_indices)) == len(values)}")
print(f"sequential_equivalent={total == sum(value * value for value in values)}")
```

Limitations: this sequential teaching model fixes one static schedule and exact integer arithmetic. It does not execute workers, model compiler directives, aliasing, memory visibility, scheduling contention, dynamic/guided policies, caches, false sharing, SIMD, floating point, exceptions, cancellation, nested regions, external effects, or performance.

## Alternatives and Trade-Offs

**Sequential loop** fixes order and minimizes setup; **parallel loop** amortizes setup for independent sufficient work.

**Static blocks** give locality/low overhead; **dynamic chunks** handle skew; **guided chunks** trade early amortization for smaller tail work.

**Cyclic scheduling** distributes patterned costs; **contiguous scheduling** reduces striding and simplifies range ownership.

**Critical/atomic shared reduction** saves partial storage but serializes/contends; **owned partials plus tree** scale better with combine overhead.

**Ordered region** streams effects in encounter order with a serial bottleneck; **indexed assembly after join** uses memory for cleaner parallelism.

**Fixed reduction tree** improves reproducibility; **runtime-selected tree** may balance better; **exact/high-precision accumulator** costs more.

**Outer-loop parallelism** amortizes setup/locality; **collapse/inner parallelism** exposes more work; nested ownership avoids oversubscription.

**Early-any match** can stop sooner but is nondeterministic; **minimum/encounter-first match** requires stable selection and possibly more work.

## Failure Modes and Misconceptions

- “The compiler accepted the parallel loop, so it is independent.” Semantic alias/effect proof remains.
- “The loop index is the only shared state.” Captured objects and global services also matter.
- “Private pointer means private pointee.” Only the reference instance is private.
- “Static schedule is balanced.” Equal counts do not imply equal costs.
- “Dynamic schedule is always faster.” Scheduling and locality overhead may dominate.
- “Chunk one maximizes parallelism.” It can maximize coordination work.
- “A critical section preserves loop order.” It preserves exclusion, not logical order.
- “Lastprivate means last worker.” It denotes the sequentially last logical iteration under the API.
- “Atomic sum is a scalable reduction.” One cache line can remain a hot serialization point.
- “Addition is associative.” Actual overflow and floating semantics decide.
- “Average of partial averages is average.” Only with equal counts; reduce sum/count.
- “Break stops all iterations immediately.” Parallel work may already be running.
- “One thrown exception means the loop has stopped.” Runtime and started work must be settled.
- “Nowait is a performance-only flag.” It removes a dependency/publication barrier.
- “Nested parallel loops use available cores.” They can oversubscribe or serialize.

## Worked Examples

### Example 1

`out[i]=in[i]*in[i]` writes disjoint slots. With immutable nonaliasing input, any schedule preserves indexed result. If `out` overlaps `in` with an offset, one iteration can destroy another's unread value; copy/version or prove safe mapping.

### Example 2

`prefix[i]=prefix[i-1]+x[i]` has a loop-carried flow dependence. A parallel-for directive is unsound. Replace it with a specified parallel scan whose algorithm and arithmetic preserve the intended prefix contract.

### Example 3

Twelve uniform iterations on three workers use static contiguous ranges of four. Coverage is exact and locality good. If only indices 0–3 are expensive, dynamic chunks or weighted static partitioning reduce the straggler; count balance alone failed.

### Example 4

Each iteration enters a critical section to add a value. The result can be correct but hot update serializes. Per-chunk owned sum then one tree combine removes `n` contended entries; integer overflow and floating grouping remain declared.

### Example 5

An average reducer uses `(local_mean)` and averages three partial means for chunk counts 2, 2, and 8. It weights chunks equally and is wrong. Reduce `(sum,count)` associatively, then divide once with empty/precision policy.

### Example 6

Dynamic iterations emit text under a mutex. Lines are race-free but schedule-ordered. Store `(index,line)` in disjoint slots and emit after join, or use an ordered construct and accept serialization/reorder waiting.

### Example 7

Floating values include large cancellation terms. Static and dynamic reductions differ in low bits because their trees differ. Select fixed tree, compensated/higher-precision scheme, or a domain-derived tolerance; do not hide difference by an arbitrary epsilon.

### Example 8

A worker finds a matching record and sets cancellation. Higher indices have already caused external requests. Define any versus lowest match, stable operation IDs, cancellation settlement, and effect reconciliation. A return from the iteration callback is not necessarily loop break.

### Example 9

Outer image-row parallelism calls an internally multithreaded codec. `P` outer workers each create `P` codec workers, causing oversubscription. Configure codec sequential within outer loop or make the codec own the sole parallel region; benchmark full stack.

### Example 10

A nuclear simulation parallelizes safety-margin reductions and accepts whichever floating result a dynamic schedule returns. Software convergence alone cannot establish physical or regulatory adequacy. Named nuclear/domain, numerical, scientific-computing, systems, real-time, cybersecurity, verification, quality, operations, human-factors, and regulatory reviewers must approve models, uncertainty, precision/reproducibility, validation data, timing, hazards, fault behavior, standards, and residual risk. This chapter cannot authorize operational use.

## Cross-Program Connections

- **Algorithms:** loops become maps, scans, reductions, histograms, stencils, and searches after dependence analysis.
- **Compilers:** alias/dependence analysis, privatization, canonical forms, vectorization, and directives implement transformations.
- **Architecture:** cache lines, prefetch, SIMD, NUMA, bandwidth, and coherence shape schedules.
- **Numerical computing:** accumulator design, conditioning, overflow, rounding, and reproducibility define results.
- **Operating systems:** affinity, preemption, worker counts, and nested runtimes affect balance.
- **Data engineering:** partition skew, aggregation, ordering, and bounded diagnostics reappear at cluster scale.
- **Security:** adversarial bounds, skew, expansion, and shared-resource contention can be denial mechanisms.
- **Reliability:** failure aggregation, cancellation settlement, idempotent effects, and complete joins protect state.
- **Performance:** chunk overhead, maximum chunk cost, serial ordered regions, and bandwidth determine break-even.
- **Formal methods:** iteration relations, algebraic laws, and schedule equivalence support proofs and property tests.

## References

1. OpenMP Architecture Review Board. “OpenMP API Specification 6.0.” November 2024. <https://www.openmp.org/wp-content/uploads/OpenMP-API-Specification-6-0.pdf>.
2. OpenMP Architecture Review Board. “OpenMP Examples 6.0.1.” 2025. <https://www.openmp.org/wp-content/uploads/openmp-examples-6-0-1.pdf>.
3. ISO C++ Working Draft. “Parallel Algorithms.” <https://eel.is/c++draft/algorithms.parallel>.
4. Intel oneAPI Threading Building Blocks. “parallel_for.” <https://uxlfoundation.github.io/oneTBB/main/tbb_userguide/parallel_for_os.html>.
5. Intel oneAPI Threading Building Blocks. “parallel_reduce.” <https://uxlfoundation.github.io/oneTBB/main/tbb_userguide/parallel_reduce.html>.
6. Rayon Project. “ParallelIterator.” <https://docs.rs/rayon/latest/rayon/iter/trait.ParallelIterator.html>.
7. IEEE. “IEEE Standard for Floating-Point Arithmetic.” IEEE 754-2019. <https://standards.ieee.org/standard/754-2019.html>.
8. N. J. Higham. “Accuracy and Stability of Numerical Algorithms,” 2nd ed. SIAM, 2002. <https://doi.org/10.1137/1.9780898718027>.
9. NVIDIA. “CUDA C++ Programming Guide.” <https://docs.nvidia.com/cuda/cuda-programming-guide/index.html>.
10. LLVM Project. “Loop Vectorization.” <https://llvm.org/docs/Vectorizers.html#loop-vectorizer>.

## Exercises

### Exercise 1

Classify dependencies in four loops: disjoint map, prefix recurrence, indirect histogram update, and ordered log output. Give a sound parallel transformation or reject it.

### Exercise 2

Compare static blocks of four, dynamic chunks of one, and dynamic chunks of four for 16 iteration costs `[8,8,8,8,1,...,1]` on four workers. Discuss ideal assignment, overhead, locality, and worst tail.

### Exercise 3

Design a custom reduction for `(checked_sum,count,minimum,diagnostics)`. State identity, combine laws, overflow/error ordering, empty input, and bounded diagnostics.

### Exercise 4

Specify cancellation and deterministic result behavior for a parallel search that must return the lowest matching index while iterations may fail or cause idempotent effects.

### Exercise 5

A medical dose loop passes average performance and floating tolerance tests. Explain why that does not prove clinical suitability and define required human evidence.

## Answers to the Exercises

### Answer 1

Disjoint `out[i]=f(in[i])` is a parallel map after proving no alias/effect conflicts. Prefix recurrence reads the previous output; use a specified scan, not ordinary parallel loop. Histogram indirect writes collide for repeated keys; use atomics with contention/numeric policy, per-worker histograms plus reduction, or sort/group by key. Ordered logging is an effect dependence: compute indexed lines then render sequentially, use an ordered region, or explicitly weaken the product to unordered logs. A mutex alone gives exclusion but not encounter order.

### Answer 2

Static contiguous blocks place four expensive iterations on worker zero for cost 32 while others get cost four, so makespan is at least 32 despite total 44. Dynamic unit chunks can distribute expensive iterations among workers and approach 11 plus overhead, but makes 16 assignments and weakens locality. Dynamic chunks of four reproduce the bad first heavy block if chunks are handed one per worker, though later stealing cannot split it; overhead is only four assignments. Cyclic static unit assignment would distribute one heavy item to each worker with low runtime assignment overhead but strided access. Exact runtime behavior must be measured; this reasoning isolates cost distribution.

### Answer 3

Accumulator contains checked/wider sum state, count, optional minimum, bounded indexed diagnostics, and overflow identities. Identity is `(zero,0,None,empty,no-overflow)`. Combine adds counts, combines sums under the declared checked/wider rule, selects minimum from options, merges diagnostics by index with a cap while retaining total error count, and aggregates overflow in stable source-range order. If checked intermediate grouping can change failure, either use a wide exact accumulator and validate final range or fix tree/order as contract. Empty finalization returns count zero and no minimum (not a fabricated sentinel). Property-test identity/associativity over reachable bounded states.

### Answer 4

Attach stable indices and operation IDs. Workers can publish candidate indices through a monotonic atomic minimum, using it only to prune indices proven unable to beat the current best; scheduling-first match is never final. Each failure is indexed and selected/aggregated by deterministic policy. Cancellation stops unneeded admission but all started iterations join and effects reconcile by idempotency key. If a lower unprocessed index could still match or fail decisively, the loop cannot finalize a higher candidate. Publish the minimum only after the required prefix/domain has terminal evidence and all owned started work is settled.

### Answer 5

Average tests omit worst-case anatomy/input, conditioning, schedule trees, hardware/toolchain variance, exceptional values, timing tails, faults, cancellation, and downstream treatment effects. Production requires named radiation oncologists, medical physicists, numerical experts, clinical safety, software/runtime, hardware, cybersecurity/privacy, human-factors, quality, independent verification, operations, and regulatory reviewers; requirements/hazard traceability; validated reference data and independent calculations; tolerance/uncertainty rationale; reproducibility/toolchain qualification; worst-case timing, saturation, fault-injection, cancellation, recovery, environmental, commissioning, and patient-specific QA; and signed residual-risk acceptance. This answer is not clinical authorization.
