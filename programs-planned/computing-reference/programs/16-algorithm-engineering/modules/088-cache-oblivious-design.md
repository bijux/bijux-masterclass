---
module_id: ALGE-088
program: Algorithm Engineering
level: 2
module_number: 88
title: Cache-Oblivious Design
status: complete
last_verified: 2026-09-05
---

# Cache-Oblivious Design

## One-Page Review

### Governing question

How can one algorithm obtain asymptotically efficient data movement across unknown memory levels without encoding cache capacity or transfer-block size, while keeping the model assumptions and implementation limits honest?

### Essential definitions

- A **cache-aware** algorithm uses memory parameters such as cache capacity $M$ or block size $B$ in its structure or tuning.
- A **cache-oblivious** algorithm does not use $M$ or $B$, yet is analyzed for transfers between adjacent memory levels.
- The **ideal-cache model** has a cache of $M$ words, blocks of $B$ consecutive words, full associativity, and optimal replacement [1].
- A **cache miss** transfers the block containing an accessed word; computation on resident words is separately accounted.
- The **tall-cache assumption**, commonly $M=\Omega(B^2)$, is a theorem hypothesis for some bounds, not a fact about every hierarchy.
- A **recursive layout** stores recursively related regions near one another; recursive control flow alone does not change a poor layout.
- **Resource obliviousness** is not security **data obliviousness**: the former omits machine parameters, while the latter constrains access dependence on secrets.

### Central model, mechanism, or theorem

Recursive decomposition generates subproblems at every geometric scale. For any actual cache level, there is a recursion depth where a subproblem’s live data fits that level even though the program never names $M$. Once resident, depth-first completion reuses the subproblem before leaving it. Under the ideal-cache assumptions, a scan costs $\Theta(1+N/B)$ transfers, recursive matrix transpose can match $\Theta(1+mn/B)$, and conventional recursive square matrix multiplication can attain

$$
\Theta\!\left(1+\frac{n^2}{B}+\frac{n^3}{B\sqrt M}\right)
$$

transfers under the usual layout and tall-cache qualifications [1]. These are model-relative asymptotic bounds, not cycle or energy predictions.

### Critical invariants

- Recursive children form a disjoint cover of the parent domain, or overlap is deliberate and reconciled.
- Base cases terminate for empty, singleton, and uneven dimensions.
- The traversal and layout preserve logical identity and output ownership.
- The transfer recurrence includes compulsory leaves, boundary blocks, and any temporary storage.
- The proof explicitly states $M$, $B$, replacement, associativity, layout, and tall-cache assumptions.
- Implementation evidence distinguishes theoretical transfers from measured misses, elapsed time, stack use, prefetching, and parallel effects.

### Common failures

Calling ordinary divide-and-conquer cache-oblivious without a transfer proof; using a recursive algorithm over pointer-scattered data; silently choosing a cache-sized base case; confusing cache-oblivious with cache-free or data-oblivious; dropping the additive scan term; assuming an optimal two-level result predicts every real level; ignoring set conflicts, virtual memory, prefetchers, recursion overhead, layout-conversion cost, NUMA placement, false sharing, and parallel scheduler behavior; and reporting a speedup as proof of the model mechanism.

### Compact example

A recursive transpose splits the longer dimension until reaching cells. It never reads $M$ or $B$. For a particular cache, some intermediate rectangles eventually fit, so depth-first traversal completes those rectangles with local reuse. Correctness follows from assigning source $(i,j)$ exactly once to destination $(j,i)$. Transfer optimality needs the ideal-cache analysis; speed needs measurement.

### Connections

[ALGE-085](./085-external-memory-cost-models.md) defines $M$, $B$, scan, and sorting costs; [ALGE-087](./087-blocked-matrix-and-graph-algorithms.md) uses explicit tiles. ALGE-089 next applies I/O-efficient thinking to search and index construction, while ALGE-090 integrates hierarchy, threads, and storage.

## Governing Question

Given a problem, representation, recursion, memory hierarchy, and deployment context, when does a parameter-free decomposition provably exploit unknown transfer granularities, and what additional engineering is required before that proof supports a production choice?

## Why This Matters

A cache-aware implementation chooses tile and buffer sizes for a known boundary. That can be excellent for one machine, but machines contain many boundaries: registers, several caches, local and remote memory, page translation, persistent storage, and sometimes networked tiers. A single parameter rarely fits them all. Cache-oblivious design asks whether geometric recursion can expose locality at every scale without hard-coding those capacities.

The result is not magic. The model idealizes replacement and associativity and counts block transfers, not instructions. Real implementations have recursion overhead, finite associativity, hardware prefetch, translation, vector units, NUMA placement, and parallel scheduling. A cache-aware library may outperform a theoretically optimal cache-oblivious routine by packing data or selecting machine-specific kernels. Conversely, recursive decomposition can provide robust behavior across unknown or changing capacity.

Cache-oblivious analysis is valuable because it is both constructive and falsifiable. The algorithm omits $M$ and $B$; the theorem quantifies over them. A recursion tree reveals the scale where subproblems fit. Transfer recurrences can be checked. Model assumptions are visible. The approach therefore connects elegant algorithm analysis with a disciplined engineering question: which locality properties survive on the actual hierarchy?

## Prerequisites and Retrieval

Retrieve asymptotic reasoning from [ALGE-005](./005-asymptotic-time-and-space.md), recurrence analysis from [ALGE-007](./007-recurrences-and-the-master-method.md), model qualification from [ALGE-009](./009-machine-models-and-hidden-constants.md), empirical validation from [ALGE-010](./010-combining-proof-and-measurement-in-algorithm-evaluation.md), divide-and-conquer design from [ALGE-021](./021-divide-and-conquer.md), merge sorting from [ALGE-013](./013-merge-sort.md), external-memory notation from [ALGE-085](./085-external-memory-cost-models.md), and explicit blocking from [ALGE-087](./087-blocked-matrix-and-graph-algorithms.md). You should be able to draw a recursion tree and distinguish words, blocks, and transfers.

## Learning Objectives

After this module, you should be able to:

1. define cache-obliviousness precisely and distinguish it from cache awareness and security obliviousness;
2. state the ideal-cache model and identify where each assumption enters a proof;
3. explain why recursive subproblems create useful scales without knowing $M$ and $B$;
4. derive scan, transpose, search-layout, and matrix-multiplication transfer bounds at an appropriate level;
5. implement and validate a parameter-free recursive transpose reference;
6. identify when recursive layout, not recursion alone, supplies locality;
7. diagnose base-case, layout, prefetch, associativity, stack, NUMA, and parallel failures; and
8. design measurements that test rather than merely repeat a cache-oblivious explanation.

## Core Exposition

### State the ideal-cache model

The ideal-cache model considers a processor with a fast cache holding $M$ words and an arbitrarily large slow memory divided into aligned blocks of $B$ consecutive words. Accessing a word whose block is absent causes a block transfer. The cache is fully associative and uses an optimal offline replacement policy. The algorithm’s source does not contain $M$ or $B$ [1].

Analysis asks for $Q(N;M,B)$, the number of transfers. CPU operations, instructions, branch misses, translation, and parallel communication require separate models. A cold-cache convention typically yields an additive constant or scan term. If input already resides in cache, bounds may differ; state the initial condition.

Full associativity removes conflict misses. Optimal replacement makes the model analytically strong. Frigo and colleagues relate optimal replacement to least-recently-used replacement within qualified bounds, and show how two-level analysis can extend through multilevel hierarchies under their framework [1]. This does not make a real cache ideal; it explains why the abstraction can support hierarchy-wide asymptotics.

### Understand the quantifiers

Cache-oblivious does not mean “works without a cache.” It means the same algorithm, independent of $M$ and $B$, has a proved transfer bound for eligible $M,B$. The proof may still mention both parameters. Indeed, without them there is no transfer complexity to state.

The order is important: choose one algorithm, then analyze it across parameter values. Choosing a base case from detected cache size is cache-aware. Choosing a small constant base case for instruction efficiency remains cache-oblivious in the asymptotic definition because the constant is independent of $M,B$, although deployment may still tune that constant and thereby create a hybrid.

### Use recursion to generate all scales

Suppose a problem of size $N$ is repeatedly divided into balanced children and processed depth first. The recursion contains subproblems near size $M$ for any actual $M$. If a subproblem’s total live data is at most a suitable fraction of $M$, its blocks can remain resident while that subtree completes. The algorithm discovers no boundary at runtime; the proof identifies the boundary after the fact.

Three conditions make this argument work. First, each child must touch a compact or otherwise transfer-efficient region. Second, depth-first execution must finish the child before unrelated work evicts it. Third, the recurrence must charge boundary blocks and shared state without double-counting unjustified reuse. Balanced recursion alone is insufficient over linked nodes scattered by an allocator.

### Start with scan

A contiguous scan of $N$ words touches at most $\lceil N/B\rceil+1$ blocks depending on alignment, hence $\Theta(1+N/B)$ transfers. It is trivially cache-oblivious: the loop does not know $B$. This example prevents a misconception that cache-oblivious algorithms must be recursive.

The lower bound is compulsory input access when all $N$ words must be examined from slow memory. The result depends on contiguity. Scanning $N$ pointers to random records may cause $\Theta(N)$ transfers even though the pointer array itself scans optimally.

### Recursively transpose a matrix

For an out-of-place transpose, split the longer dimension until reaching a base case. Each child maps a source rectangle to the corresponding destination rectangle. This keeps aspect ratios controlled and supplies subrectangles across scales. When a source and destination subproblem fit, its depth-first work can reuse their blocks.

The reference below intentionally has no cache parameter and stops at one cell. It tests logical decomposition, not practical speed. A production version usually uses a small constant base case, careful leading dimensions, and possibly vectorized copying.

<!-- bijux-verify: {"id":"recursive-transpose-reference","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"transpose: [[1, 6, 11], [2, 7, 12], [3, 8, 13], [4, 9, 14], [5, 10, 15]]\nrecursive calls: 29\ncell visits: 15\nmatches reference: True\n","stderr":""}} -->
```python
def recursive_transpose(source):
    rows = len(source)
    columns = len(source[0])
    target = [[0 for _ in range(rows)] for _ in range(columns)]
    calls = 0
    visits = 0

    def copy_rectangle(row_first, row_last, column_first, column_last):
        nonlocal calls, visits
        calls += 1
        height = row_last - row_first
        width = column_last - column_first
        if height == 1 and width == 1:
            target[column_first][row_first] = source[row_first][column_first]
            visits += 1
        elif height >= width:
            middle = row_first + height // 2
            copy_rectangle(row_first, middle, column_first, column_last)
            copy_rectangle(middle, row_last, column_first, column_last)
        else:
            middle = column_first + width // 2
            copy_rectangle(row_first, row_last, column_first, middle)
            copy_rectangle(row_first, row_last, middle, column_last)

    copy_rectangle(0, rows, 0, columns)
    return target, calls, visits


matrix = [[1, 2, 3, 4, 5],
          [6, 7, 8, 9, 10],
          [11, 12, 13, 14, 15]]
transposed, calls, visits = recursive_transpose(matrix)
reference = [[matrix[row][column] for row in range(len(matrix))]
             for column in range(len(matrix[0]))]
print("transpose:", transposed)
print("recursive calls:", calls)
print("cell visits:", visits)
print("matches reference:", transposed == reference)
```

There are 15 leaves and, because every internal call has exactly two nonempty children, 14 internal calls: 29 total. The execution proves coverage and output for one integer matrix on the recorded interpreter. It does not measure cache transfers or prove the ideal-cache bound.

### Sketch the transpose transfer bound

Assume row-major contiguous storage, an out-of-place destination, an ideal cache, and a suitable tall-cache condition. At a recursion level where a rectangle’s source and destination footprints fit in cache, processing it incurs transfers proportional to its occupied blocks. Across disjoint fitting subproblems, the total footprint is $O(1+mn/B)$. Higher recursion levels mostly direct traversal; lower levels reuse resident data. Reading $mn$ source values and writing $mn$ destination values also gives an $\Omega(1+mn/B)$ compulsory bound under a cold-cache block model. Thus the recursive transpose is asymptotically optimal in that model [1].

The proof must handle row boundaries, alignment, and skinny rectangles. Splitting the larger dimension prevents indefinitely pathological aspect ratios. It does not claim every real cache observes the exact bound or constant.

### Recursively multiply matrices

Divide each square matrix into quadrants. Each output quadrant receives two recursive products, for example $C_{11}=A_{11}B_{11}+A_{12}B_{21}$. Recursive decomposition supplies subproblems at cache-fitting scales. For conventional $\Theta(n^3)$ arithmetic, the ideal-cache transfer bound can be written

$$
Q(n)=\Theta\!\left(1+\frac{n^2}{B}+\frac{n^3}{B\sqrt M}\right)
$$

under the standard assumptions [1]. The $n^2/B$ term accounts for compulsory matrix footprints; the other term captures repeated movement needed for cubic work with only $M$ fast words.

The result is not obtained by blindly making eight recursive calls. Accumulation order, temporary matrices, layout, base cases, and rectangular dimensions matter. A naive implementation that allocates copied quadrants at every call can add traffic and allocation cost. Views preserve storage but may be strided. High-performance libraries often use cache-aware packing and tuned micro-kernels because real instruction and vector behavior matters.

### Make layout recursive when structure requires it

Search in a pointer-linked balanced binary tree can transfer one block per level. A van Emde Boas–style recursive layout stores the upper part of a tree recursively, followed by recursively laid-out lower subtrees. At any unknown block scale, search paths cross only logarithmically many compact clusters, supporting cache-oblivious search bounds.

Layout is part of the data structure contract. Static layout is simpler; dynamic insertion requires ordered-file maintenance or indirection. Cache-oblivious B-tree designs combine recursive layout with update mechanisms to approach B-tree transfer bounds without knowing $B$ [3]. Their complexity and constants are real engineering costs, not erased by asymptotic optimality.

### Sort without memory parameters

Ordinary mergesort is not automatically optimal in the external-memory sense because two-way merging yields too many transfer levels compared with a memory-aware multiway merge. Funnelsort constructs recursively composed merging funnels, obtaining the optimal comparison-sorting transfer form under stated ideal-cache and tall-cache assumptions [1]. The mechanism emulates high fan-in across scales without using $M$ or $B$.

This is a useful warning: divide-and-conquer syntax is not enough. A cache-oblivious algorithm needs a dataflow whose recurrence matches the desired transfer bound. Funnel buffers, layout, base cases, and construction costs all belong in the proof and implementation.

### Distinguish three meanings of oblivious

**Cache-oblivious** means independent of cache parameters. **Data-oblivious** means the observable access pattern does not reveal protected data beyond an allowed leakage function. **Cache-adaptive** concerns changing available cache capacity during execution [5]. None implies the others.

A cache-oblivious binary search still branches and accesses locations based on the query, so it is not data-oblivious. A sorting network may be data-oblivious but hard-coded for a memory organization or inefficient in transfers. Bender and colleagues show that cache-obliviousness and cache-adaptivity are distinct properties, even though certain recursive structures obtain both under their model [5].

### Account for real machines

Finite associativity can cause conflicts absent from the ideal model. Hardware prefetchers reward predictable streams and sometimes make a simple iterative algorithm outperform cache-aware and cache-oblivious alternatives; experiments on prefetch-oriented variants demonstrate this possibility for selected algorithms and systems [6]. Virtual addressing adds page walks and TLB reach. Recursion adds calls, branches, and stack frames. Compilers may inline or transform code differently.

On multicore systems, private caches, shared last-level caches, coherence, false sharing, work stealing, and NUMA placement introduce costs outside a sequential ideal cache. A depth-first order that is local sequentially may expose too little parallelism. A scheduler that steals tiny recursive tasks may destroy locality. Practical designs use grain-size cutoffs and affinity—parameters that can turn a pure cache-oblivious description into a hybrid resource-aware implementation.

### Validate in four layers

First, validate semantics against an independent reference: coverage, permutation, ordering, matrix equality, or query answers. Include empty and uneven cases and detect duplicate/missing leaves with stable identities.

Second, validate the theoretical argument: write the recurrence, identify fitting subproblems, state layout, prove disjoint charging, include compulsory terms, and list every model hypothesis. Test symbolic formulas and bounded small instances where possible.

Third, validate the implementation mechanism: inspect recursion depth, allocation, copy volume, stack use, base cases, layout conversion, and task scheduling. Confirm that the source does not secretly consult $M$ or $B$ if pure cache-obliviousness is claimed.

Fourth, measure the target systems. Compare iterative, cache-aware, cache-oblivious, and strong library baselines. Sweep sizes through hierarchy boundaries rather than testing one power of two. Record alignment, huge pages, compiler, affinity, NUMA policy, warm/cold state, counters, and distributions. Explain only what the evidence discriminates.

## Definitions and Notation

Let $N$ be input words, $M$ fast-memory capacity in words, $B$ consecutive words per transferred block, and $Q(N;M,B)$ the transfer count between a named adjacent pair of levels. Define

$$
\operatorname{Scan}_{M,B}(N)=\Theta(1+N/B)
$$

and, in the eligible external comparison-sorting regime,

$$
\operatorname{Sort}_{M,B}(N)=\Theta\!\left(\frac{N}{B}\log_{M/B}\frac{N}{B}\right),
$$

with conventional adjustments when the logarithm would be below a constant. Let $T(N)$ denote processor operations so that arithmetic and movement remain separate. Let $S(v)$ be a recursive subproblem’s live footprint and $d(v)$ its depth.

An algorithm is **cache-oblivious** if its description omits $M$ and $B$. It is **transfer-optimal** only relative to a problem, model, parameter regime, and lower bound. **Recursive traversal** specifies order; **recursive layout** specifies addresses. A **base case** is the terminating subproblem. A **cutoff** may be theoretical, constant, or machine-tuned; name which.

## Mechanisms, Invariants, or Proof Structure

### Recursion-tree proof template

1. Prove children cover the parent computation and establish termination.
2. Define live footprint $S(v)$, including source, destination, temporaries, and metadata.
3. For fixed but unknown $M$, identify a frontier of maximal nodes whose footprints fit: $S(v)\le cM$.
4. Bound transfers within each fitting subtree by its occupied blocks plus qualified boundary effects.
5. Show frontier nodes are disjoint enough that their charges sum to the claimed total.
6. Add work above the frontier, compulsory input/output transfers, and conversion costs.
7. Match a lower bound only under the same assumptions.

### Correctness invariant for recursive transpose

For a call on $[r_0,r_1)\times[c_0,c_1)$, every source cell in that rectangle is copied exactly once to its transposed destination, and no cell outside the rectangle is written by the call. Splitting one non-singleton dimension creates two disjoint rectangles whose union is the parent. Induction from the one-cell base case proves complete exact coverage.

### Model-to-machine discipline

A theorem establishes $Q$ in the ideal-cache model. A simulator establishes a trace count under its configured replacement and geometry. A hardware counter reports events according to a specific processor and measurement setup. Elapsed time combines movement, computation, runtime, operating-system, and measurement effects. These evidence types may corroborate one another, but none silently substitutes for another.

## Alternatives and Trade-Offs

| Design | Strength | Cost or limitation | Best validation |
|---|---|---|---|
| flat streaming | minimal overhead and prefetch-friendly | helps only stream-shaped access | byte/transfer lower bound |
| cache-aware tiling | exploits known boundary and tuned kernels | retuning and multilevel complexity | parameter sweep |
| cache-oblivious recursion | one structure exposes many scales | model gaps and recursion overhead | recurrence plus hierarchy sweep |
| recursive layout | compact paths/subproblems | conversion and dynamic-update complexity | query traces and update cost |
| autotuning hybrid | adapts constants to a deployment | training cost and overfitting | held-out sizes and machines |
| iterative emulation | controls stack and scheduling | more explicit state | semantic and locality comparison |
| parallel recursive tasks | exposes nested parallelism | steals, false sharing, and grain size | work/span/cache/coherence evidence |

Cache-aware and cache-oblivious are not moral categories. A stable library may reasonably combine recursive macrostructure with cache-aware packing and architecture-tuned kernels. The durable requirement is to label which claims survive parameterization and which belong to the deployed implementation.

## Failure Modes and Misconceptions

- **“No cache parameters appear, so the algorithm is cache-oblivious optimal.”** Parameter independence is a definition; optimality needs a proof and matching lower bound.
- **“Recursion guarantees locality.”** Children can traverse pointer-scattered or interleaved regions.
- **“Two-level optimal means exact multilevel performance.”** The transfer theorem is asymptotic and model-relative, not a cycle prediction.
- **“Tall cache is harmless notation.”** It is a premise; violating it can invalidate a bound.
- **“The base case is irrelevant.”** It affects termination, stack depth, instructions, vectorization, and constants.
- **“Cache-oblivious means data-oblivious.”** Query- or key-dependent accesses may leak data even when $M,B$ are absent.
- **“Optimal replacement describes my hardware.”** It is an analytical ideal; finite associativity and real policies add misses.
- **“Recursive layout is free.”** Construction, conversion, updates, identity maps, and interoperability can dominate.
- **“Hardware counters prove causation.”** Events need controlled variants and accurate attribution.
- **“One recursive implementation should beat a tuned library.”** The theorem does not include every instruction-level optimization.

## Worked Examples

### Example 1

**Situation.** Classify three programs: a scan, a tiled loop using detected L2 size, and a recursive transpose with a constant $16\times16$ base case.

**Reasoning.** The scan is cache-oblivious because it uses no $M,B$ and has scan-optimal transfers. The detected-L2 loop is cache-aware. The recursive transpose remains asymptotically cache-oblivious when 16 is a fixed implementation constant independent of the deployment, though calling 16 “optimal” needs measurement. If startup calibration changes it by cache size, the deployed hybrid is resource-aware.

**Conclusion.** Classification depends on parameter dependence; performance quality is a separate claim.

### Example 2

**Situation.** A contiguous array has $N=10{,}000$ eight-byte words and transfers 64-byte blocks. Give an alignment-safe upper estimate for a complete scan.

**Reasoning.** Each block contains $B=8$ words. Aligned storage touches $10{,}000/8=1{,}250$ blocks. Arbitrary starting alignment can add at most one boundary block, yielding at most 1,251 under the simple no-prefetch block account. The loop never needs to know 8.

**Conclusion.** The scan is parameter-free but its analysis still substitutes the actual $B$.

### Example 3

**Situation.** Explain the 29 calls in the executable $3\times5$ transpose.

**Reasoning.** The recursion splits a non-singleton rectangle into exactly two nonempty children and stops at 15 cells. A full binary tree with $L$ leaves has $L-1$ internal nodes, so total calls are $2L-1=29$. Each leaf writes the unique transposed destination for one source cell.

**Conclusion.** Tree shape proves call count and coverage, not cache traffic.

### Example 4

**Situation.** A recursive transpose omits an empty-matrix precondition and immediately reads `source[0]`. What failed?

**Reasoning.** The mathematical domain may include a $0\times n$ matrix, but the representation cannot infer $n$ from an empty nested list. Reading the first row raises an error before recursion. The API must either reject empty input explicitly, carry dimensions separately, or define a representation that preserves the missing dimension.

**Conclusion.** Base-case correctness begins at the representation boundary, not only at singleton recursion.

### Example 5

**Situation.** A recursive tree search follows one pointer per level through independently allocated nodes. Is it locality-efficient merely because it recurses?

**Reasoning.** No. The call tree mirrors the logical tree, but addresses can be unrelated. A height-$h$ path may touch $h$ blocks. A recursive van Emde Boas–style layout clusters path fragments at many scales; that physical arrangement, together with traversal, yields the transfer argument.

**Conclusion.** Recursive control flow and recursive storage layout are distinct mechanisms.

### Example 6

**Situation.** Compare conventional recursive multiplication for $n=1024$, $M=65{,}536$ words, and $B=16$ words using the dominant reuse term.

**Reasoning.** Since $\sqrt M=256$, the dominant term is $n^3/(B\sqrt M)=1024^3/(16\cdot256)=262{,}144$ transfers. The footprint term is $n^2/B=65{,}536$. Including both gives an order-model estimate around 327,680 plus constants, not an exact miss count.

**Conclusion.** The formula separates compulsory footprint from movement required to sustain cubic work.

### Example 7

**Situation.** Ordinary two-way mergesort is parameter-free. Why is that insufficient for external-memory sorting optimality?

**Reasoning.** It performs $\Theta(\log N)$ merge levels, each scanning $N/B$ blocks, for roughly $\Theta((N/B)\log N)$ transfers in a simple analysis. The optimal external-memory form uses logarithm base $M/B$, exploiting many resident buffers. Funnelsort recursively realizes high effective fan-in across scales without naming those values.

**Conclusion.** Cache-oblivious optimality depends on transfer-efficient dataflow, not merely omitting parameters.

### Example 8

**Situation.** A cache-oblivious binary search layout is proposed for secret keys. Does its name establish resistance to cache-timing leakage?

**Reasoning.** No. The visited path depends on comparisons with the secret query, so observed addresses may reveal information. Resource obliviousness says only that layout/search code omits cache parameters. Security requires a threat model and data-oblivious or ORAM-like access guarantee.

**Conclusion.** The two forms of obliviousness answer unrelated questions.

### Example 9

**Situation.** A simple iterative Floyd–Warshall variant beats a cache-oblivious version on a measured machine. Does this refute ideal-cache theory?

**Reasoning.** Not by itself. Predictable iteration may exploit hardware prefetch, vectorization, or compiler transformations absent from the transfer model; the recursive version may pay call or task overhead. Verify identical semantics, inspect code generation and counters, sweep sizes, and state model predictions separately. Published algorithm-engineering work has shown prefetch-friendly standard variants outperforming cache-aware and cache-oblivious versions on its tested systems [6].

**Conclusion.** A model bound and a machine outcome can both be correct within their scopes.

### Example 10

**Situation.** Design a test for the claim that a recursive transpose adapts across cache levels.

**Reasoning.** Compare direct, explicitly tiled, and recursive implementations over rectangular and square sizes spanning L1, L2, last-level cache, memory, and page/TLB thresholds. Hold algorithm semantics, compiler, affinity, layout, alignment, and initialization constant. Record wall time and relevant cache/TLB events with counter limitations. Include cold and steady-state regimes and inspect recursion depth, stack, and copy volume.

**Conclusion.** Adaptation is supported by a pattern across scale boundaries, not one winning size.

## Cross-Program Connections

- [Computer Architecture CA-031](../../23-computer-architecture/modules/031-locality-and-the-memory-wall.md) explains why hierarchy costs motivate locality models.
- [Computer Architecture CA-040](../../23-computer-architecture/modules/040-analyzing-cache-misses-from-an-access-trace.md) connects abstract traces to concrete cache geometry.
- [Data Structures Engineering DSE-001](../../17-data-structures-engineering/modules/001-abstract-data-types-and-concrete-representations.md) separates logical search semantics from recursive physical layouts.
- [Operating Systems OS-031](../../22-operating-systems/modules/031-address-translation.md) adds pages and translation behavior absent from the ideal-cache model.
- [Operating Systems OS-040](../../22-operating-systems/modules/040-diagnosing-memory-pressure-and-thrashing.md) shows why fluctuating and aggregate working sets matter.
- [Concurrent and Parallel Programming CONPAR-001](../../04-programming-languages-concurrent-and-parallel-programming/modules/001-concurrency-parallelism-and-asynchrony.md) introduces ownership and scheduling concerns that sequential cache analysis omits.

## References

1. Matteo Frigo, Charles E. Leiserson, Harald Prokop, and Sridhar Ramachandran, “Cache-Oblivious Algorithms,” *ACM Transactions on Algorithms* 8(1), Article 4, 2012; expanded from FOCS 1999. [doi:10.1145/2071379.2071383](https://doi.org/10.1145/2071379.2071383). Checked 2026-09-05.
2. Erik D. Demaine, “Cache-Oblivious Algorithms and Data Structures,” in *Algorithms for Memory Hierarchies*, LNCS 2625, Springer, 2003. [doi:10.1007/3-540-36574-5_2](https://doi.org/10.1007/3-540-36574-5_2). Checked 2026-09-05.
3. Michael A. Bender, Erik D. Demaine, and Martin Farach-Colton, “Cache-Oblivious B-Trees,” *SIAM Journal on Computing* 35(2), 341–358, 2005. [doi:10.1137/S0097539701389956](https://doi.org/10.1137/S0097539701389956). Checked 2026-09-05.
4. Lars Arge, Michael A. Bender, Erik D. Demaine, Bryan Holland-Minkley, and J. Ian Munro, “An Optimal Cache-Oblivious Priority Queue and Its Application to Graph Algorithms,” *SIAM Journal on Computing* 36(6), 1672–1695, 2007. [doi:10.1137/S0097539703428324](https://doi.org/10.1137/S0097539703428324). Checked 2026-09-05.
5. Michael A. Bender et al., “Cache-Adaptive Algorithms,” *Proceedings of SODA 2014*, 958–971, 2014. [doi:10.1137/1.9781611973402.71](https://doi.org/10.1137/1.9781611973402.71). Checked 2026-09-05.
6. Shen Pan, Cary Cherng, Kevin Dick, and Richard E. Ladner, “Algorithms to Take Advantage of Hardware Prefetching,” *ALENEX 2007*, 91–98, 2007. [doi:10.1137/1.9781611972870.9](https://doi.org/10.1137/1.9781611972870.9). Checked 2026-09-05.
7. A. N. Yzelman and Rob H. Bisseling, “Cache-Oblivious Sparse Matrix–Vector Multiplication by Using Sparse Matrix Partitioning Methods,” *SIAM Journal on Scientific Computing* 31(4), 3128–3154, 2009. [doi:10.1137/080733243](https://doi.org/10.1137/080733243). Checked 2026-09-05.
8. Peyman Afshani, John Iacono, Varunkumar Jayapaul, Ben Karsin, and Nodari Sitchinava, “Locality-of-Reference Optimality of Cache-Oblivious Algorithms,” *APOCS 2022*, 31–45, 2022. [doi:10.1137/1.9781611977059.3](https://doi.org/10.1137/1.9781611977059.3). Checked 2026-09-05.

## Exercises

### Exercise 1

Define cache-obliviousness and explain why an algorithm may be cache-oblivious even though its analysis contains $M$ and $B$.

### Exercise 2

For a row-major $9\times6$ matrix recursively split along the longer dimension to cells, derive the number of leaf and total calls. State the condition that justifies the total-call formula.

### Exercise 3

A recursive transpose returns wrong results only for $1\times n$ matrices. Diagnose the likely partition/base-case defect and state a test oracle.

### Exercise 4

Compare a pure cache-oblivious matrix multiplication with a hybrid that uses recursive macro-decomposition and a tuned packed micro-kernel. Give the claims each can honestly make and the evidence needed.

### Exercise 5

Transfer cache-oblivious reasoning to a recursive image pyramid stored as pointer-linked separately allocated tiles. Explain why recursion may fail to provide locality and propose a corrected design and evaluation.

## Answers to the Exercises

### Answer 1

A cache-oblivious algorithm’s description and control parameters do not depend on cache capacity $M$ or block size $B$. Its analysis must contain $M,B$ because transfer cost is a function of the hierarchy being modeled. The quantification fixes one parameter-independent algorithm and proves bounds across eligible parameter pairs. A cache-aware algorithm instead uses those values or measurements derived from them to select tiles, buffers, or branching factors. Full credit requires separating the algorithm definition from the theorem variables.

### Answer 2

There are $9\cdot6=54$ cell leaves. If every non-leaf rectangle is divided into exactly two nonempty children, the recursion tree is full binary and has $54-1=53$ internal nodes, hence $2\cdot54-1=107$ total calls. The formula fails if calls create empty children, use more than two children, or stop at multi-cell base cases. The dimension-splitting rule must ensure a dimension of length at least two is selected so both children are nonempty.

### Answer 3

A likely defect assumes both dimensions exceed one before splitting or treats `height == 1` as a completed rectangle rather than continuing to split columns. The correct base case is one cell, while a one-row rectangle with width greater than one must split its width. An oracle constructs the destination at coordinates $(j,i)$ from the source at $(i,j)$ using an independent direct pair of loops and also records that every source identity is visited once. Test $1\times1$, $1\times2$, $1\times n$, $n\times1$, and uneven rectangles.

### Answer 4

The pure version can claim that its algorithmic structure does not use $M,B$ and, if proved, meets a stated ideal-cache bound. It cannot claim best real performance. The hybrid can claim cache-oblivious recursive macrostructure but must label the tuned cutoff, packing, and micro-kernel as cache- or architecture-aware. Validate both against an independent numeric oracle and error policy. For theory, check transfer recurrences and hypotheses. For practice, record tuning procedure, packed bytes, workspace, instructions, vectorization, cache/TLB events, alignment, thread/NUMA policy, and runtime over held-out shapes and machines, including tuning and conversion cost where relevant.

### Answer 5

Pointer-linked independently allocated tiles may place recursive siblings far apart, so the logical recursion does not imply address locality; each pointer and tile can trigger unrelated blocks or pages. Correct the design by storing a subtree’s tiles contiguously in recursive order, using an arena with stable offsets, or maintaining a compact index and packed tile store. Preserve a mapping from logical image coordinates to storage and account for rebuilds or dynamic updates. Validate pixel equivalence and unique coverage, inspect address/transfer traces or reliable counters, measure conversion and query/update costs, and sweep images and tile occupancies across hierarchy sizes. A model answer must identify layout as the missing mechanism and include both semantic and locality evidence.
