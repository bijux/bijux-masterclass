---
module_id: CONPAR-042
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 42
title: Data Parallelism and Bulk Operations
status: complete
last_verified: 2026-08-29
---

# Data Parallelism and Bulk Operations

## One-Page Review

### Governing question

How can one operation be applied across a data domain in parallel while preserving dependence safety, partition ownership, deterministic meaning, numerical accuracy, locality, and bounded resource use?

### Essential definitions

- **Data parallelism** applies the same operation or operation family to many elements or partitions concurrently.
- A **bulk operation** describes work over a collection—such as map, filter, reduce, scan, scatter, or gather—rather than manually scheduling each element.
- An **iteration space** is the indexed/keyed domain over which work is defined.
- A **partition** is a disjoint or explicitly overlapping subset assigned as a scheduling/locality unit.
- **Map** transforms each input independently; **filter** selects elements; **reduce** combines values with an operator.
- **Scan/prefix** returns reductions for every prefix; **segmented scan** resets at segment boundaries.
- **SIMD** executes one instruction over vector lanes; **SIMT** executes many logical threads in groups with divergence rules.
- A **data dependence** is a required order caused by reads/writes to the same logical location.
- **False sharing** occurs when independent variables share a cache-coherence unit and concurrent writes cause contention.
- A **collective** is a coordinated group operation such as broadcast, reduction, gather, scatter, or barrier.

### Central model, mechanism, or theorem

For input domain `I`, a pure map has outputs `y_i=f(x_i)` with no cross-iteration write conflict, so any execution order yields the same indexed result. A reduction over operator `op` may regroup elements in parallel only when the required algebra and result contract permit it. Associativity supports tree regrouping; an identity supports empty/partitioned folds; commutativity permits reordering, but floating-point addition is not real-number associative in finite precision. Total work `T1`, span `T_infinity`, communication, and memory traffic jointly limit speedup.

### Critical invariants

Every input belongs to the declared domain and each output slot has one writer or synchronized combination. Partitions cover required indices exactly once unless overlap has explicit merge semantics. Kernel reads/writes and aliasing satisfy dependence assumptions. Bulk API ordering and exception/cancellation behavior are declared. Reduction operator properties match the implementation's grouping/order. Partial results have owned identity and are combined once. Memory, task, and output expansion are bounded. Barriers/collectives have identical participant membership. Final publication occurs only after all required partitions terminate.

### Common failures

Code parallelizes a loop with a loop-carried dependence; writes through hidden aliases; assumes a library preserves encounter order; uses nonassociative subtraction as a reduction; expects bitwise-identical floating sums after regrouping; makes one task per element; creates skewed partitions; writes adjacent counters and triggers false sharing; copies more bytes than computation justifies; diverges every GPU lane; places a barrier in a branch not taken by all participants; allows filter/flat-map output to grow without a bound; or treats successful kernel launch as completed, visible results.

### Compact example

Values 1 through 8 split into contiguous partitions `[1,2,3]`, `[4,5,6]`, and `[7,8]`. Each partition squares locally and computes a partial sum: 14, 77, and 113. Combining partials gives 204, equal to the sequential sum of squares. Stable partition order reconstructs `[1,4,9,16,25,36,49,64]`. This trace demonstrates exact integer map/reduce accounting, not parallel speedup or floating-point reproducibility.

### Connections

[Task Parallelism and Dependency Graphs](041-task-parallelism-and-dependency-graphs.md) supplies work/span reasoning; [Critical Sections and Shared-State Invariants](008-critical-sections-and-shared-state-invariants.md) supplies write ownership. The [program roadmap](../ROADMAP.md) next develops recursive fork-join computation.

## Governing Question

How should engineers prove that a data transformation admits parallel execution, choose its partition and bulk primitive, and interpret the resulting performance and numerical behavior honestly?

Data parallelism begins with dependence and algebra, not processor count.

## Why This Matters

Modern CPUs expose vector lanes and multiple cores; GPUs expose thousands of logical threads; distributed engines divide datasets across workers. Their efficient interfaces are bulk-oriented. Image transforms, simulations, analytics, linear algebra, search, compilation passes, and machine learning repeatedly apply related work across large domains.

A sequential loop encodes an order even when the computation does not require one. Bulk primitives express semantic intent and let runtimes choose vector width, chunking, work distribution, and device execution. This can improve portability and optimization.

The abstraction does not erase correctness. Aliasing, boundary stencils, reductions, exceptions, cancellation, output ordering, numeric precision, and external effects remain. Nor does massive logical parallelism guarantee speedup: memory bandwidth, transfer, launch overhead, skew, synchronization, and serial fractions often dominate.

## Prerequisites and Retrieval

Retrieve:

- shared-state invariants from [Critical Sections and Shared-State Invariants](008-critical-sections-and-shared-state-invariants.md);
- execution-model selection from [Choosing a Concurrency Model from the Workload](010-choosing-a-concurrency-model-from-the-workload.md);
- atomic combination from [Atomic Read-Modify-Write Operations](025-atomic-read-modify-write-operations.md);
- cache behavior from [False Sharing and Cache-Line Contention](029-false-sharing-and-cache-line-contention.md);
- task-graph bounds from [Task Parallelism and Dependency Graphs](041-task-parallelism-and-dependency-graphs.md); and
- bounded output from [Backpressure in Asynchronous Pipelines](040-backpressure-in-asynchronous-pipelines.md).

Retrieval prompt: for a loop, list the read and write locations of iteration `i`, then state whether iterations `i` and `j` can commute for every distinct pair.

## Learning Objectives

After completing this module, a learner can:

1. distinguish data, task, pipeline, SIMD, SIMT, and distributed parallelism;
2. prove iteration independence or identify flow, anti-, and output dependencies;
3. choose map, filter, reduce, scan, gather, scatter, stencil, or histogram structures;
4. derive partition coverage, disjointness, and halo obligations;
5. state algebraic requirements for parallel reductions;
6. explain floating-point regrouping and reproducibility choices;
7. compare static, cyclic, dynamic, and cost-aware partitioning;
8. reason about locality, false sharing, vectorization, divergence, and transfer;
9. define failure, cancellation, collective, and publication semantics; and
10. test result equivalence, bounds, and performance claims proportionately.

## Core Exposition

### Data-parallel semantics

A data-parallel operation separates logical domain from execution schedule. For map, each logical index `i` consumes `x_i` and produces `y_i`. Runtime chunks may execute in any order, but the indexed mapping preserves result identity. This differs from task parallelism, where tasks may perform different operations, and pipeline parallelism, where stages overlap different items.

Bulk APIs are valuable because they can fuse operations, vectorize, choose grain, and avoid per-element scheduling. Their contract matters: some preserve encounter order, some only return an unordered set, some stop after one error, and some permit work to continue after cancellation is requested.

Purity makes reordering easy, but is not mandatory. Partition-owned mutation is safe when each logical location has exactly one writer and publication follows completion. Effects such as logging, random generation, file writes, and remote requests need explicit identity/order/idempotency; “parallel for” does not make them deterministic.

### Dependence analysis

Iteration `i` has read set `R_i` and write set `W_i`. Distinct iterations are conflict-free when `W_i` does not intersect `R_j`, `W_j`, and symmetrically `W_j` does not intersect `R_i`, absent an approved reduction/atomic protocol. A flow dependence writes a value a later iteration reads. An anti-dependence protects a read before overwrite. An output dependence orders writes.

Loop `a[i]=2*b[i]` is independent if arrays do not overlap unexpectedly. `a[i]=a[i-1]+x[i]` has a recurrence. `a[p[i]]+=x[i]` may collide when indices repeat. Language aliasing rules, slice overlap, pointer arithmetic, views, and shared object fields can hide conflicts.

Dependences can be transformed. Prefix sum replaces a recurrence with an associative scan algorithm. Privatization gives each partition a local histogram then reduces bins. Double buffering makes a stencil read one grid and write another. Renaming versions removes anti-dependencies. Transformations require a proof of equivalent semantics.

### Map, filter, and flat-map

Map preserves cardinality and naturally assigns one output per input index. It is often easiest to parallelize deterministically. In-place map is safe only with disjoint element ownership and no cross-element aliases.

Filter has data-dependent output positions. A parallel implementation may compute predicates, scan selection counts, then scatter selected values into exact offsets. Appending all matches to one locked list is correct under a suitable lock but contended and may produce schedule order rather than encounter order.

Flat-map has variable expansion. Bound per-input and total output or stream results with backpressure. Prefix counts can allocate exact output for finite inputs; otherwise expansion can exhaust memory even when input partitions are bounded.

### Reductions and algebra

A sequential left fold fixes grouping: `(((x1 op x2) op x3) ...)`. Parallel reduction computes partition partials and combines them as a tree. Associativity, `(a op b) op c = a op (b op c)`, permits regrouping. An identity `e` with `e op a=a op e=a` supports empty partitions. Commutativity permits arbitrary operand reordering but is not required when a stable tree preserves order.

Integer addition is associative only under a declared overflow model. Mathematical addition differs from trapping, wrapping, saturating, and unbounded integer semantics. String concatenation is associative but order-sensitive. Subtraction and division are not associative. “Average” is not a direct associative operator; reduce `(sum,count)` then divide, with numeric policy.

A correct reducer defines accumulator type, identity/empty behavior, element-to-accumulator lift, combine operation, overflow/precision, and deterministic grouping. Side-effecting combiners are hazardous because runtimes may invoke them in unexpected groupings or retry contexts.

### Floating-point reproducibility

IEEE 754 floating addition rounds after operations, so regrouping can change low bits and sometimes materially change cancellation error. A parallel tree often has different rounding than a sequential fold. Both can conform to the declared arithmetic while differing bitwise.

Choose a contract: exact reproducibility via fixed tree/order and fixed environment; numerical tolerance backed by error analysis; improved accuracy with pairwise or compensated summation; higher-precision accumulator; or exact/superaccumulator methods when required. Tolerance is domain-specific, not a universal epsilon.

Compiler fast-math modes may reassociate, ignore exceptional values, or change contraction. Device architectures may differ in fused operations and intermediate precision. Record compiler/runtime/device modes when reproducibility matters.

### Scan, stencil, scatter, and gather

An inclusive scan returns `y_i=x_0 op ... op x_i`; exclusive scan starts with identity and excludes `x_i`. Parallel scan uses upsweep/downsweep or block partials, doing linear work with logarithmic ideal span under suitable models. It powers compaction, offsets, stream compaction, and radix algorithms.

A stencil reads a neighborhood. Same-step in-place updates create dependencies; double buffering gives one immutable input epoch and one output epoch. Partitions need halo/ghost values at boundaries. Halo exchange becomes communication and synchronization; corner and periodic boundaries must be explicit.

Gather reads indices into disjoint output positions; invalid/repeated reads are fine if source is immutable. Scatter writes to indexed destinations and may collide. Resolve with uniqueness proof, atomics, ownership partitioning, sorting/grouping, or deterministic reduction. Histograms are scatter reductions; local histograms plus combination often outperform one atomic global array.

### Partition correctness

For domain `[0,n)`, partitions `P_k` should cover it: union equals the domain. For single-owner map, they should be pairwise disjoint. Empty partitions are legal if kernels and identities handle them. Bound formulas carefully when `n` is not divisible by worker count or `n<P`.

Contiguous blocks improve spatial locality and ordered assembly. Cyclic assignment distributes periodic cost patterns but increases striding. Block-cyclic balances while retaining blocks. Dynamic chunks handle unpredictable costs at scheduling overhead and less deterministic placement. Cost-aware partitioning uses estimates but can be wrong or expensive.

Skew matters more than average. One partition containing a hot key or large sparse row controls makespan. Split heavy keys, use work stealing, adapt chunks, or change algorithm. Preserve deterministic output with stable indices rather than forcing deterministic execution order.

### SIMD and vectorization

SIMD vector instructions operate on lanes in one core. Vectorization needs independent iterations, supported operations, useful alignment/access patterns, and manageable branches. Structure-of-arrays often improves contiguous field access compared with array-of-structures, but can hurt whole-record operations.

Remainder/tail elements require masked operations or scalar cleanup. Alignment improves some targets but correctness must not depend on assumed alignment unless enforced. Gather/scatter vectors exist on some architectures but can be slower than contiguous loads.

Compiler vectorization reports and generated-code inspection provide evidence. Writing a bulk loop does not prove vectorization. Benchmark realistic sizes, include warm-up/environment, verify outputs, and measure bandwidth/counters where possible.

### SIMT and GPU execution

GPUs schedule groups of logical threads that execute common instruction streams. Branch divergence can serialize paths within a group. Coalesced memory access and enough occupancy help hide latency. Shared/local memory may stage tiles, requiring correctly uniform barriers.

A barrier reached by only some required participants can deadlock or produce undefined behavior under the programming model. Kernel launch is commonly asynchronous relative to host; success at launch does not prove completion. Synchronize through documented events/streams before reading results or freeing memory.

Transfer and launch overhead can dominate small kernels. Fuse operations, retain data on device, batch work, and overlap transfer only when ownership prevents reuse races. Device memory, outstanding kernels, and error propagation need bounds and lifecycle.

### Memory hierarchy and false sharing

Data-parallel work often becomes bandwidth-bound. Arithmetic intensity—useful operations per byte moved—helps explain why adding cores stops scaling. Blocking/tiling reuses cache or shared memory. Loop interchange and layout can turn strided access into contiguous access if dependence allows.

When workers write distinct counters on one cache line, coherence invalidations cause false sharing. Pad/align per-worker accumulators or aggregate in local blocks, then combine. Padding is architecture-sensitive and increases footprint; measure rather than guessing.

NUMA systems favor first-touch/local allocation and partition placement near data. Dynamic stealing improves balance but may increase remote memory. A runtime scheduler cannot infer all logical ownership, so placement and partition design remain engineering inputs.

### Collectives and barriers

Bulk-synchronous algorithms alternate local computation and collective synchronization. A barrier guarantees that participating tasks reached a point under its memory contract; it does not validate their results. Participant membership must agree. Early return, exception, or cancellation before a barrier can strand peers.

Distributed collectives require matching operation, datatype/count, communicator/group, and order. A reduction's tree and result placement may be implementation-specific. Collective failure semantics are runtime-dependent and often more complex than ordinary exceptions.

Avoid global barriers when point-to-point dependencies suffice; barriers couple progress to the slowest participant. Sometimes they clarify epoch invariants and simplify reasoning. Treat barrier count and scope as part of the algorithm, not incidental synchronization.

### Exceptions, cancellation, and boundedness

Bulk APIs differ on whether one failure cancels pending iterations, aggregates errors, chooses an arbitrary first error, or lets started work complete. Side effects may have happened before failure is reported. Give work stable identity and define partial-result visibility.

Cancellation is cooperative in many runtimes. A kernel or vector loop may not observe it until a chunk ends. Grain balances responsiveness against overhead. Do not publish aggregate success until all required partitions have terminal outcomes and device/remote work is synchronized.

Bound input partitions, task count, device buffers, partial accumulators, filter/flat-map output, retry attempts, and trace volume. A finite array helps, but nested expansion or per-element remote operations can still create unbounded obligations elsewhere.

### Verification and performance claims

Use a sequential oracle for finite representative inputs and property tests for coverage, disjointness, permutation/order, reduction identities, and collision policy. Test sizes zero, one, below/at/above vector/chunk width, nondivisible sizes, maximum payload, repeated scatter indices, skew, NaN/infinity/signed zero, overflow, failure, and cancellation.

Controlled schedules and tiny partitions expose races. Sanitizers and race detectors add evidence within supported executions. Numeric tests derive tolerances from conditioning and domain requirements. Metamorphic tests compare partition counts/groupings to the declared equivalence class.

Performance evaluation reports hardware, topology, compiler/runtime flags, input distribution, transfer, warm-up, repetitions, and uncertainty. Compare useful work, not an implementation that omits validation or changes semantics. Strong scaling fixes problem size; weak scaling grows it. A speedup on one machine/input is empirical, never universal.

## Definitions and Notation

For iteration `i`, `R_i` and `W_i` are read/write sets. Independence for distinct `i,j` requires `W_i intersect (R_j union W_j)=empty` and its symmetric condition, unless conflicts use a proved combination protocol.

Partitions `{P_0,...,P_{p-1}}` cover domain `I` when `union_k P_k=I`; single-owner partitions also satisfy `P_j intersect P_k=empty` for `j!=k`.

Map is `y_i=f(x_i)`. Reduction over sequence `x` and operator `op` combines lifted elements into an accumulator. Associativity is `(a op b) op c=a op (b op c)` over the actual value domain; identity `e` satisfies both-sided identity.

Work `T1` sums useful algorithmic operations in a declared cost model; span `T_infinity` is longest dependency chain. Parallel time remains at least `max(T1/P,T_infinity)` and may also be lower-bounded by communication/bandwidth.

Arithmetic intensity `q` is useful operations divided by bytes transferred at a specified memory boundary. It is a diagnostic ratio, not by itself a performance guarantee.

## Mechanisms, Invariants, or Proof Structure

Audit a data-parallel operation in this order:

1. state the logical domain, element identity, input/output and effect contract;
2. derive per-iteration read/write sets and alias assumptions;
3. classify true/anti/output dependencies and transform only with equivalence proof;
4. choose map/filter/reduce/scan/stencil/scatter/gather or another exact primitive;
5. prove partition coverage, disjointness or overlap/halo merge semantics;
6. define operator identity, associativity, ordering, overflow, precision, and empty input;
7. select static/dynamic grain using overhead, skew, locality, and cancellation needs;
8. bound tasks, partials, bytes, expansion, transfers, retries, and effects;
9. declare SIMD/SIMT alignment, tail, divergence, barrier, and completion behavior;
10. define exception, cancellation, partial result, and terminal publication;
11. test against oracle/properties across sizes, collisions, numeric edges, and schedules; and
12. measure scaling with complete hardware/software/input/transfer evidence.

The executable model partitions integers 1–8, squares each element, computes partition partials, combines them once, and validates coverage and deterministic assembly.

<!-- bijux-verify: {"id":"partitioned-map-reduce-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"partitions=[[1, 2, 3], [4, 5, 6], [7, 8]]\nmapped=[[1, 4, 9], [16, 25, 36], [49, 64]]\npartials=[14, 77, 113]\nresult=[1, 4, 9, 16, 25, 36, 49, 64]\ntotal=204\ncoverage=True\nunique_inputs=True\nsequential_equivalent=True\n","stderr":""}} -->
```python
values = list(range(1, 9))
boundaries = [(0, 3), (3, 6), (6, 8)]
partitions = [values[start:end] for start, end in boundaries]
mapped = [[value * value for value in part] for part in partitions]
partials = [sum(part) for part in mapped]
result = [value for part in mapped for value in part]
covered = [value for part in partitions for value in part]

print(f"partitions={partitions}")
print(f"mapped={mapped}")
print(f"partials={partials}")
print(f"result={result}")
print(f"total={sum(partials)}")
print(f"coverage={covered == values}")
print(f"unique_inputs={len(set(covered)) == len(values)}")
print(f"sequential_equivalent={result == [value * value for value in values]}")
```

Limitations: this sequential exact-integer trace uses hand-chosen contiguous partitions and list materialization. It does not run concurrently, check arbitrary partition algorithms, model aliasing, finite overflow, floating point, vectorization, SIMD/SIMT, caches, NUMA, transfer, barriers, failures, cancellation, side effects, expansion, or performance.

## Alternatives and Trade-Offs

**Sequential loop** minimizes overhead and fixes order; **bulk parallel operation** exposes reordering and scaling for sufficient work.

**Contiguous blocks** favor locality/order; **cyclic blocks** reduce patterned skew; **dynamic chunks** balance irregular cost with overhead and placement variability.

**Map** preserves one-output ownership; **in-place mutation** saves allocation but tightens alias/publication constraints.

**Atomic scatter** handles collisions directly but contends; **local privatization plus reduce** uses memory to reduce contention.

**Stable filter** preserves encounter order using counts/scan/scatter; **unordered append** may be simpler/faster when order is irrelevant.

**Fixed reduction tree** supports reproducibility; **dynamic tree** may balance better; **compensated/high-precision accumulation** trades cost for accuracy.

**CPU threads/SIMD** avoid device transfer; **GPU/SIMT** offers throughput when work, locality, and batch size justify staging.

**Barrier epochs** simplify global invariants but couple to stragglers; **dependency events** allow finer progress at more state complexity.

## Failure Modes and Misconceptions

- “A loop is data parallel because iterations look similar.” Read/write dependence decides.
- “Distinct indices imply no alias.” Views/pointers may overlap underlying storage.
- “Read-only means free.” Bandwidth and cache capacity still limit scaling.
- “Associative in mathematics means associative in code.” Overflow and rounding change algebra.
- “Commutative is required for reduction.” Stable ordered tree can use associative, order-sensitive operators.
- “Parallel sum should equal sequential bits.” Regrouped floating operations may differ.
- “One element per task maximizes parallelism.” Overhead can dominate.
- “Equal counts balance work.” Data-dependent cost and skew matter.
- “A GPU has thousands of independent cores.” Execution groups, occupancy, divergence, and memory govern behavior.
- “Kernel launch success means result ready.” Host/device execution is often asynchronous.
- “All threads can conditionally reach a barrier.” Required membership must reach it consistently.
- “Filter output is bounded by worker count.” It is bounded by selected cardinality/bytes.
- “Padding always fixes false sharing.” Layout, line size, allocator, and footprint require evidence.
- “Speedup proves equivalent semantics.” Correctness must be checked independently.

## Worked Examples

### Example 1

`out[i]=3*in[i]+1` has disjoint output slots and immutable input. Contiguous partitions cover `[0,n)` once, including a shorter tail. Publish output only after all partitions finish; scheduling order is irrelevant to indexed result.

### Example 2

`a[i]=a[i-1]+x[i]` carries a flow dependence and cannot become an ordinary parallel map. Reformulate as an associative prefix scan, preserving inclusive/exclusive and overflow semantics.

### Example 3

A histogram's `bins[key] += 1` collides. Each worker accumulates a private bounded histogram, then bins are reduced. This removes hot atomics at the cost of `workers*bins` memory; sparse/huge key spaces need another design.

### Example 4

Parallel stable filter computes predicates `[1,0,1,1]`, exclusive offsets `[0,1,1,2]`, total three, then writes selected inputs to offsets 0,1,2. Atomic append might return a valid set but not encounter order.

### Example 5

Summing `[1e16,1,-1e16]` left-to-right can lose 1, while another grouping can retain it. Specify fixed grouping, error tolerance, compensated/pairwise accumulation, or higher precision from domain analysis; do not label the difference a race automatically.

### Example 6

Four workers increment adjacent per-worker counters. Values are race-free but share cache lines, causing coherence traffic. Align/pad or accumulate larger local batches, then measure line invalidations and footprint.

### Example 7

A 2-D five-point stencil partitions rows. Each partition reads one halo row above/below from immutable epoch `t` and writes disjoint epoch `t+1`. Boundary conditions and halo readiness precede computation; swapping epochs occurs after all partitions finish.

### Example 8

A GPU branch sends alternating lanes through expensive different paths, so each group serializes both paths. Reorder/group input by path when semantics allow, use predication for small branches, or redesign the kernel. Include regrouping cost and output identity.

### Example 9

One partition fails after writing an external record. Cancelling siblings does not undo it. Use stable per-element identity/idempotency, record partial terminal outcomes, synchronize started device/remote work, and publish aggregate failure only after cleanup.

### Example 10

A genomic clinical pipeline parallelizes variant scoring and accepts tolerance-based numeric differences. Software tests alone cannot establish diagnostic validity. Named clinical geneticists, bioinformaticians, laboratory scientists, numerical experts, privacy/security, quality, validation, and regulatory reviewers must approve reference data, algorithm/version provenance, thresholds, uncertainty, reproducibility, auditability, clinical interpretation, and validated workflows. This chapter provides no clinical authorization.

## Cross-Program Connections

- **Algorithms:** scan, reduction, sorting, compaction, stencils, and graph frontiers are bulk patterns.
- **Computer architecture:** SIMD, caches, coherence, NUMA, GPUs, and bandwidth determine realized execution.
- **Compilers:** dependence/alias analysis and vectorization reports justify transformations.
- **Numerical computing:** conditioning, rounding, reproducible summation, and error budgets define acceptable results.
- **Data engineering:** partitions, skew, shuffle, aggregation, and collectives scale bulk datasets.
- **Machine learning:** tensor kernels, batching, fusion, and accelerator placement are data-parallel systems.
- **Distributed systems:** collectives add network topology, stragglers, partial failure, and replay.
- **Security/privacy:** partitioning must preserve access boundaries and bound adversarial expansion.
- **Reliability:** partial effects, retries, cancellation, and terminal accounting survive failures.
- **Performance:** work/span, arithmetic intensity, locality, transfer, and scaling separate bottlenecks.

## References

1. G. E. Blelloch. “Prefix Sums and Their Applications.” Carnegie Mellon University, 1990. <https://www.cs.cmu.edu/~guyb/papers/Ble93.pdf>.
2. G. E. Blelloch. “Programming Parallel Algorithms.” Communications of the ACM 39(3), 1996. <https://doi.org/10.1145/227234.227246>.
3. IEEE. “IEEE Standard for Floating-Point Arithmetic.” IEEE 754-2019. <https://standards.ieee.org/standard/754-2019.html>.
4. OpenMP Architecture Review Board. “OpenMP API Specification 6.0.” November 2024. <https://www.openmp.org/wp-content/uploads/OpenMP-API-Specification-6-0.pdf>.
5. ISO C++ Working Draft. “Parallel Algorithms.” <https://eel.is/c++draft/algorithms.parallel>.
6. Intel. “Intel 64 and IA-32 Architectures Optimization Reference Manual.” <https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html>.
7. NVIDIA. “CUDA C++ Programming Guide.” <https://docs.nvidia.com/cuda/cuda-programming-guide/index.html>.
8. Khronos Group. “SYCL 2020 Specification.” <https://registry.khronos.org/SYCL/specs/sycl-2020/html/sycl-2020.html>.
9. Open MPI. “Collective Communication.” <https://docs.open-mpi.org/en/main/man-openmpi/man3/MPI_Reduce.3.html>.
10. NumPy Developers. “CPU/SIMD Optimizations.” <https://numpy.org/doc/stable/reference/simd/index.html>.

## Exercises

### Exercise 1

Analyze whether `a[i]=b[i]+c[i]`, `a[i]=a[i-1]+b[i]`, and `bins[key[i]]+=1` are directly parallel maps. State alias and transformation requirements.

### Exercise 2

Partition `[0,10)` across three workers using contiguous blocks. Prove coverage/disjointness, then compare cyclic assignment for costs `[10,1,1,10,1,1,10,1,1,10]`.

### Exercise 3

Design a reproducible parallel floating-point sum contract, including empty input, NaN/infinity, grouping, accumulator, tolerance or bitwise requirement, and evidence.

### Exercise 4

Specify a bounded stable parallel filter with cancellation and one partition failure. Include count/scan/scatter, memory, ordering, and publication.

### Exercise 5

A radiotherapy dose kernel produces GPU results within average tolerance and deadline. Explain missing production evidence and required human review.

## Answers to the Exercises

### Answer 1

`a[i]=b[i]+c[i]` is a map if output slots are disjoint and `a` does not overlap inputs in a way that lets one iteration overwrite another's future read; otherwise copy/version or prove safe traversal. `a[i]=a[i-1]+b[i]` has a recurrence; reformulate as scan over the declared arithmetic rather than parallel map. Histogram updates collide for repeated keys; use atomics with an explicit numeric model, partition-owned bins, sort/group keys, or private histograms reduced afterward. In every case actual language aliasing and overflow semantics are part of the proof.

### Answer 2

One balanced contiguous division is `[0,4)`, `[4,7)`, `[7,10)`: union is `[0,10)`, endpoints meet without overlap, and sizes differ by at most one. Its costs are 22, 12, and 12. Cyclic indices `{0,3,6,9}`, `{1,4,7}`, `{2,5,8}` yield costs 40, 3, and 3—worse because expensive items repeat every three. A different cyclic stride/blocking or dynamic chunks can handle this pattern. Equal counts alone do not prove balance; locality costs may still favor contiguous blocks.

### Answer 3

Define result for empty input (identity +0 or error), NaN propagation/selection, infinities, signed zero, overflow, rounding mode, subnormals, contraction, and accumulator precision. For bitwise reproducibility, fix input order, partition boundaries, reduction tree, implementation/toolchain arithmetic modes, and device class, and test golden edge cases. For numerical reproducibility, select pairwise/compensated or higher-precision accumulation and derive absolute/relative/ULP bounds from conditioning and domain thresholds. Compare against a trusted higher-precision oracle across adversarial magnitude/cancellation distributions; never choose an arbitrary epsilon after seeing failures.

### Answer 4

Bound input and output count/bytes. Each partition computes predicates/count without publishing output. After all counts succeed, a deterministic scan assigns disjoint encounter-order offsets and verifies total capacity. Scatter writes each selected item once. If cancellation/failure occurs before publication, cancel pending work, wait for started partitions, dispose partial buffers, and return typed terminal outcomes; external effects are prohibited or separately reconciled. Publish the single ordered output only after all scatters complete. Chunk size bounds cancellation latency; retained predicates/counts/partials are included in memory budget.

### Answer 5

Average tolerance/deadline omits worst-case anatomy/input, conditioning, rounding/device/compiler variation, transfer/synchronization, thermal throttling, faults, stale data, and clinical consequence. Production requires named medical physicists, radiation oncologists, treatment-planning/domain experts, numerical analysts, GPU/hardware, real-time, software, cybersecurity, quality, independent verification, human-factors, and regulatory reviewers; requirements/hazard traceability; algorithm and reference-dataset provenance; independent dose calculation; commissioning; tolerance rationale; deterministic/version evidence; worst-case timing, saturation, fault-injection, hardware, environmental, recovery, and patient-specific QA; and signed residual-risk acceptance. This answer is not clinical authorization.
