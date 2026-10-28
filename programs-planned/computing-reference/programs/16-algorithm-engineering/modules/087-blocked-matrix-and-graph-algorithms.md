---
module_id: ALGE-087
program: Algorithm Engineering
level: 2
module_number: 87
title: Blocked Matrix and Graph Algorithms
status: complete
last_verified: 2026-09-05
---

# Blocked Matrix and Graph Algorithms

## One-Page Review

### Governing question

How should an algorithm partition matrix or graph work so that useful data is reused near the processor, communication is bounded, irregularity remains manageable, and the transformed execution still computes the specified result?

### Essential definitions

- A **block** or **tile** is a subproblem and its associated data region processed as a unit.
- **Blocking** changes traversal and sometimes representation to increase reuse before data leaves a fast memory or an owner.
- **Operational intensity** is useful work per byte transferred at a specified boundary; the boundary must always be named.
- A **working set** is the data simultaneously needed by a computation unit, including operands, output, metadata, and temporary state.
- A **dense tile** is usually a rectangular index range. A **sparse or graph block** may instead be defined by vertex sets, edge sets, or nonzero structure.
- An **edge cut** counts edges crossing vertex-owner boundaries; a **vertex cut** replicates vertices while assigning edges to owners.
- A **frontier** is the active vertex set for the current graph step. Its size and distribution can change the best traversal and blocking policy.

### Central model, mechanism, or theorem

For conventional dense multiplication $C=AB$, a tile update

$$
C_{I,J}\mathrel{+}=A_{I,K}B_{K,J}
$$

is algebraically the same sum as scalar multiplication when the $K$ tiles form a disjoint cover in the prescribed accumulation order. If square tiles have side $b$, three tiles require roughly $3b^2s$ bytes for $s$-byte scalars, while performing about $2b^3$ floating-point operations. Reuse therefore grows with $b$, but only until cache capacity, associativity, packing, registers, concurrency, and numerical policy intervene. For graphs, blocking seeks reuse of vertex state and adjacency metadata, but partition quality, skew, frontier sparsity, and cross-block synchronization replace the regular guarantees of dense geometry.

### Critical invariants

- Every required scalar product, nonzero contribution, or traversed edge is assigned exactly once, unless deliberate replication is reconciled explicitly.
- Tiles cover the legal index or graph domain without gaps or unintended overlap.
- Partial results have a defined owner and a valid reduction order.
- The live working set fits the intended level after metadata, temporaries, padding, and concurrent workers are included.
- Graph relabeling preserves vertex identity and edge semantics; directedness, multiplicity, weights, and self-loops remain governed.
- Measurement distinguishes arithmetic, cache traffic, memory traffic, inter-thread communication, and inter-node communication.

### Common failures

Choosing a tile from nominal cache size; assuming blocked automatically means cache-efficient; copying or packing more bytes than reuse saves; treating sparse blocks as dense; ignoring conflict misses, NUMA placement, false sharing, or load imbalance; confusing a low edge cut with balanced work; losing edges during graph relabeling; racing on shared destinations; changing floating-point results without documenting accumulation order; benchmarking only one matrix shape or one graph family; and attributing performance to cache behavior without counters or controlled evidence.

### Compact example

Multiplying two $4\times4$ matrices with $2\times2$ tiles executes eight tile triples: two row tiles, two column tiles, and two reduction tiles. It still performs $4^3=64$ scalar multiply-add updates. Blocking does not reduce arithmetic here; it changes when each $2\times2$ region is reused. Correctness follows from the same triples $(i,k,j)$ being covered once, while performance remains an empirical question.

### Connections

[ALGE-009](./009-machine-models-and-hidden-constants.md) supplies machine models, [ALGE-040](./040-engineering-graph-traversal-for-sparse-and-dense-inputs.md) supplies graph representations, [ALGE-084](./084-parallel-graph-traversal.md) supplies frontier ownership, and [ALGE-085](./085-external-memory-cost-models.md) supplies transfer accounting. ALGE-088 next removes explicit tile parameters; ALGE-090 maps the same algorithm across memory, threads, and storage.

## Governing Question

Given an operation, data shape, representation, memory hierarchy, processor topology, numerical semantics, and workload distribution, how can we design blocks that preserve correctness while reducing expensive movement rather than merely rearranging loops?

## Why This Matters

Modern processors can execute arithmetic much faster than distant data can be supplied. Dense matrix multiplication exposes this sharply: the arithmetic is regular, yet a poor loop order repeatedly reloads rows or columns. Tiling turns a large operation into submatrix updates that reuse resident operands. High-performance implementations go further, combining macro-kernel blocking, packing, register-level micro-kernels, vectorization, and architecture-specific choices [1]. The durable idea is hierarchical data reuse, not one universal tile size.

Graphs share the movement problem but deny us dense regularity. Degrees are skewed, frontiers vary, adjacency lists have unequal lengths, and writes may converge on popular vertices. A rectangular partition of an adjacency matrix can cluster useful edges and destination state, but empty space and metadata can dominate. Vertex partitioning can balance vertices while badly imbalancing edges. Edge partitioning can balance work while replicating vertex state. Blocking is therefore a joint choice of representation, ordering, work assignment, and synchronization.

The subject joins proof and measurement. A block transformation needs a coverage and reduction proof. A capacity calculation shows whether a proposed working set could fit. Neither proves speed. Actual cache behavior depends on replacement, associativity, translation, prefetching, packing, instruction mix, contention, and graph structure. A serious evaluation records these assumptions and compares against unblocked and alternative layouts.

## Prerequisites and Retrieval

Retrieve asymptotic cost from [ALGE-005](./005-asymptotic-time-and-space.md), machine-model qualification from [ALGE-009](./009-machine-models-and-hidden-constants.md), evidence design from [ALGE-010](./010-combining-proof-and-measurement-in-algorithm-evaluation.md), BFS and DFS semantics from [ALGE-031](./031-breadth-first-search.md) and [ALGE-032](./032-depth-first-search.md), sparse/dense graph representation from [ALGE-040](./040-engineering-graph-traversal-for-sparse-and-dense-inputs.md), parallel reductions from [ALGE-082](./082-parallel-prefix-and-reduction.md), parallel frontiers from [ALGE-084](./084-parallel-graph-traversal.md), and block-transfer notation from [ALGE-085](./085-external-memory-cost-models.md). You should be able to expand matrix multiplication into scalar sums and state a graph traversal invariant.

## Learning Objectives

After this module, you should be able to:

1. distinguish algorithmic blocking, storage layout, packing, scheduling, and ownership;
2. derive tile coverage, working-set, arithmetic, and approximate traffic calculations;
3. implement and verify a blocked dense matrix multiplication reference;
4. select row, column, two-dimensional, vertex, edge, or hybrid blocks for sparse matrices and graphs;
5. reason about accumulation ownership, races, reproducibility, and floating-point order;
6. diagnose capacity, conflict, translation, skew, frontier, and synchronization failures;
7. compare explicit blocking with recursive and cache-oblivious decomposition; and
8. design evidence that separates semantic correctness from locality and performance claims.

## Core Exposition

### Separate five design decisions

The word “blocked” often hides five independent decisions. **Partitioning** divides the logical domain. **Layout** decides where elements reside in addresses or files. **Packing** copies a block into a contiguous, kernel-friendly form. **Scheduling** orders block tasks. **Ownership** decides who produces or reduces each output. Changing loop bounds alone alters traversal but not layout; storing a graph by destination blocks alters layout even if traversal remains sequential.

State each decision explicitly. For a matrix, give index ranges, storage order, leading dimensions, edge-tile handling, and accumulation order. For a graph, give the vertex-to-block map, edge placement rule, representation inside a block, destination update rule, and treatment of directed edges, duplicate edges, weights, and self-loops.

### Derive dense tile coverage

Let $A$ be $m\times k$, $B$ be $k\times n$, and $C$ be $m\times n$. Partition row indices into disjoint ranges $I_p$, reduction indices into $K_r$, and column indices into $J_q$. Then

$$
C_{I_p,J_q}=\sum_r A_{I_p,K_r}B_{K_r,J_q}.
$$

For every output entry $(i,j)$, exactly one $I_p$ contains $i$ and one $J_q$ contains $j$. Every scalar index $t\in\{0,\ldots,k-1\}$ belongs to exactly one $K_r$. Thus the blocked form includes every term $A_{it}B_{tj}$ exactly once. This is a coverage proof, independent of tile size and loop order.

The qualification matters for floating point. Real-number addition is associative; floating-point addition generally is not. Reordering $K_r$ or reducing partial tiles as a tree may change rounding. A valid implementation must promise either a specific accumulation order, a reproducibility regime, or only an error tolerance. “Algebraically equal” is not “bitwise identical.”

### Estimate a dense working set

For square $b\times b$ tiles of scalar width $s$, the simplified live data for one update is two input tiles and one output tile:

$$
W\approx 3b^2s.
$$

If a usable cache budget is $S$, the necessary simplified condition is $3b^2s\le S$, hence $b\le\lfloor\sqrt{S/(3s)}\rfloor$. It is not sufficient. Set conflicts, cache lines, translation lookaside buffers, packed copies, alignment, kernel panels, prefetch distance, and neighboring work consume capacity. Multiple concurrent tasks multiply some parts of the working set.

A tile update performs about $2b^3$ floating-point operations under the convention that multiplication and addition count separately. Dividing by the simplified $3b^2s$ resident bytes gives about $2b/(3s)$ operations per resident byte. This explains why larger tiles can improve reuse, but the estimate is neither whole-program traffic nor a speed guarantee.

### Execute a blocked reference

The reference below uses a single tile size in all dimensions and clips boundary tiles. It compares with a direct implementation so that changed traversal is checked against an independent loop ordering. Python integers avoid floating-point-order ambiguity in this semantic test.

<!-- bijux-verify: {"id":"blocked-matrix-reference","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"result: [[2, 2, 5, 3], [6, 4, 1, 3], [5, 1, 5, 5], [3, 1, 5, 5]]\ntile triples: 8\nscalar updates: 64\nmatches reference: True\n","stderr":""}} -->
```python
def direct_multiply(left, right):
    rows = len(left)
    inner = len(right)
    columns = len(right[0])
    result = [[0 for _ in range(columns)] for _ in range(rows)]
    for row in range(rows):
        for column in range(columns):
            for shared in range(inner):
                result[row][column] += left[row][shared] * right[shared][column]
    return result


def blocked_multiply(left, right, tile_size):
    rows = len(left)
    inner = len(right)
    columns = len(right[0])
    result = [[0 for _ in range(columns)] for _ in range(rows)]
    tile_triples = 0
    scalar_updates = 0
    for row_start in range(0, rows, tile_size):
        for column_start in range(0, columns, tile_size):
            for shared_start in range(0, inner, tile_size):
                tile_triples += 1
                row_stop = min(row_start + tile_size, rows)
                column_stop = min(column_start + tile_size, columns)
                shared_stop = min(shared_start + tile_size, inner)
                for row in range(row_start, row_stop):
                    for shared in range(shared_start, shared_stop):
                        for column in range(column_start, column_stop):
                            result[row][column] += left[row][shared] * right[shared][column]
                            scalar_updates += 1
    return result, tile_triples, scalar_updates


left = [[1, 2, 0, 1], [0, 1, 3, 0], [2, 0, 1, 1], [1, 1, 0, 2]]
right = [[1, 0, 2, 1], [0, 1, 1, 0], [2, 1, 0, 1], [1, 0, 1, 2]]
result, tile_triples, scalar_updates = blocked_multiply(left, right, 2)
print("result:", result)
print("tile triples:", tile_triples)
print("scalar updates:", scalar_updates)
print("matches reference:", result == direct_multiply(left, right))
```

The execution proves only the stated integer result on the recorded interpreter. It does not establish cache residency, vectorization, parallel safety, floating-point error, or performance. Those require distinct evidence.

### Choose loop order, packing, and micro-kernels

A legal block-loop permutation can have very different reuse. Keeping one $C_{I,J}$ tile active across $K$ tiles favors output reuse. Holding an $A_{I,K}$ panel while sweeping $J$ favors reuse of $A$. The best choice depends on layout, cache hierarchy, kernel shape, and whether output reads and writes are expensive.

Packing copies strided or misaligned panels into contiguous buffers. The copy is worthwhile when the packed data is reused enough to repay allocation and transfer, or when it enables a much stronger vectorized kernel. Packing a tiny or single-use tile can lose. Production dense multiplication commonly layers cache blocking around a register-resident micro-kernel rather than treating one square tile as the whole design [1].

Edge tiles are smaller when dimensions are not multiples of $b$. Options include clipped loops, padded storage, masked vector operations, or specialized remainder kernels. Padding simplifies address arithmetic but increases traffic and may change numeric behavior if padded values are mishandled.

### Move from dense matrices to sparse structure

Sparse matrices store nonzeros and indices rather than every coordinate. A blocked sparse row representation groups coordinates into rectangular blocks, sometimes storing each nonempty block densely and sometimes retaining a sparse encoding inside it. Dense microblocks reduce index overhead and enable vectorization only when occupancy is high enough. With irregular sparsity, materializing zeros wastes memory and arithmetic.

For sparse matrix-vector multiplication $y=Ax$, row blocking gives disjoint ownership of $y$ ranges and simple race-free accumulation. Column blocking can improve reuse of input vector regions but creates partial output vectors that need reduction. Two-dimensional blocking trades both dimensions and can expose parallel block tasks. Sparse matrix-matrix multiplication adds symbolic structure discovery: output nonzeros are not known solely from dimensions, and temporary accumulators may dominate.

Gustavson’s sparse multiplication organization accumulates contributions row by row and illustrates that accumulator representation is part of the algorithm, not an incidental container [2]. Hypersparse and highly rectangular submatrices require representations whose metadata scales with nonempty structure rather than full dimensions [3].

### Interpret a graph as blocked sparse structure

An adjacency matrix $A$ places an edge $u\to v$ at $(u,v)$ under one common convention. Partition vertices into source ranges $S_p$ and destination ranges $D_q$; block $(p,q)$ stores edges from $S_p$ to $D_q$. Traversing one block can reuse source frontier bits and destination state. GraphBLAS formalizes graph computation through sparse matrix and vector operations over selectable algebraic operators, masks, and descriptors [4]. Blocking remains an implementation and data-organization choice beneath those semantics.

The matrix view does not erase graph details. Direction fixes which dimension is source. A transpose traversal may require a second index or explicit transpose. Parallel edges may be distinct events or algebraically combined depending on the problem. A Boolean BFS ignores weight, whereas shortest paths needs a different algebra and convergence rule. The chosen semiring or update operator must match the graph specification.

### Select graph partitions and orderings

A one-dimensional vertex partition assigns vertices and usually their outgoing adjacency to owners. It makes source ownership simple, but high-degree vertices cause work skew and remote destination updates. An edge partition balances edge counts more directly but may replicate source or destination state. A two-dimensional partition assigns adjacency blocks across a processor grid and can reduce per-owner state at the cost of row/column communication.

Relabeling vertices to cluster communities, separators, or traversal-related regions can improve locality. It also costs preprocessing time, stores forward and inverse maps, and can become stale as a dynamic graph changes. Degree ordering may cluster similar work but does not necessarily minimize edge cuts. A partition metric is a proxy: low edge cut does not guarantee cache locality, balanced frontiers, or low synchronization.

For sparse matrix-vector multiplication, recursive hypergraph partitioning can seek reuse through a separated block-diagonal form; reported benefits belong to the tested matrices and machine, not all graphs [5]. The durable lesson is to match the partition objective to the data movement of the exact kernel.

### Block frontier-based traversal

In a push BFS step, active sources scan outgoing edges and attempt destination discovery. Source-block ordering reuses frontier membership and adjacency. Destination-block ordering can buffer updates and reduce random writes, but it may scan irrelevant source regions. In pull traversal, undiscovered destinations inspect incoming neighbors; destination ownership can avoid write races, while an incoming index is required.

The frontier changes every level. A static block layout optimized for a dense frontier may waste work on a sparse frontier. Store per-block edge counts or compact active-source lists, skip empty block/frontier intersections, and consider direction switching using measured work estimates. Block scheduling should use active edges rather than vertex counts alone.

### Define ownership and synchronization

Dense output tiles are convenient units of exclusive ownership: one worker accumulates all $K$ contributions for a $C$ tile. Splitting the $K$ dimension creates parallel partial tiles, then a reduction. That increases temporary storage and may change floating-point order. Atomic scalar updates avoid explicit reduction but can serialize contention and obscure reproducibility.

Graphs have similar choices. Destination ownership routes updates to one worker; source ownership emits remote updates; edge ownership needs reconciliation for shared vertices. Per-worker bitmaps, sparse update buffers, sorting/grouping by destination, atomics, and deterministic reductions offer different memory, traffic, latency, and ordering costs. The invariant is not “no duplicate work”; some algorithms deliberately generate duplicates. It is that the acceptance rule produces the specified final state.

### Treat communication bounds as constraints

Arithmetic counts cannot explain an implementation that spends most time moving operands. Communication lower bounds establish that broad classes of matrix multiplication must move a minimum amount of data under explicit memory and processor assumptions [6]. They rule out impossible traffic targets; they do not select a tile, predict a cache, or account for all software overhead.

Blocking can approach a bound by reusing a resident tile before eviction. Distributed algorithms additionally choose a processor grid and may replicate data to trade memory for communication. State whether “communication” means cache-line transfers, main-memory bytes, messages, network words, or synchronization. Counts at different boundaries cannot be substituted.

### Validate and measure in layers

First validate semantics on tiny and adversarial cases against a structurally independent reference. Check rectangular dimensions, empty dimensions allowed by the API, non-divisible tile sizes, zeros, negative values, repeated edges, self-loops, disconnected components, and high-degree vertices. Verify coverage using identities or tagged contributions, not only a checksum.

Then validate resource claims. Measure allocated and resident bytes, packed-buffer peaks, per-worker multiplication, task counts, load distribution, and cross-owner updates. Hardware counters can support cache and translation claims, but counter availability, event meaning, multiplexing, and attribution must be recorded.

Finally measure end-to-end performance across sizes, shapes, sparsity patterns, graph families, frontier densities, thread counts, NUMA placements, and warm/cold policies. Include preprocessing and packing according to the intended reuse horizon. Report distributions, not only the best run. A faster result establishes observed behavior for the recorded system and workload, not universal superiority.

## Definitions and Notation

Let $A\in R^{m\times k}$, $B\in R^{k\times n}$, and $C\in R^{m\times n}$ over a ring or another specified algebra. Let $I_p$, $K_r$, and $J_q$ be disjoint index partitions. Let $b_i,b_k,b_j$ be tile extents and $s$ bytes per scalar. Let $S$ be usable capacity at a named memory level, $L$ cache-line bytes, and $P$ workers.

For a graph $G=(V,E)$, let $\pi:V\to\{0,\ldots,p-1\}$ map vertices to blocks. For blocks $a,b$, define $E_{ab}=\{(u,v)\in E:\pi(u)=a,\pi(v)=b\}$. Let $F_t\subseteq V$ be the frontier at step $t$, $d(v)$ a specified in- or out-degree, and $X$ the cross-owner updates or edges under the selected ownership policy.

**Capacity** is not automatically usable capacity. **Reuse distance** is the distinct data touched between accesses under a chosen trace abstraction. **Packing cost** includes reading the source and writing the packed representation. **Balance** must name its weight: vertices, edges, active edges, nonzeros, bytes, or predicted operations. **Locality** must name its boundary and evidence.

## Mechanisms, Invariants, or Proof Structure

### Dense correctness argument

Assume the index partitions are disjoint covers and scalar multiplication/addition obey the specified algebra. Fix $(i,j)$. Unique $p,q$ place it in $C_{I_p,J_q}$. For each $t$, unique $r$ places $t$ in $K_r$. The block updates therefore contribute $A_{it}B_{tj}$ once for every $t$ and no other term. Summing produces the definition of $C_{ij}$. For floating point, the conclusion is exact only relative to the implementation’s accumulation order or an accepted error specification.

### Sparse and graph coverage argument

Assume each edge has a stable occurrence identity and the block-placement rule assigns that occurrence to exactly one $E_{ab}$. Because $\pi(u)$ and $\pi(v)$ are functions, every edge occurrence belongs to one ordered block pair. Processing every nonempty block covers every edge once. If edges are replicated, replace uniqueness with a reconciliation proof that identifies duplicates before their effects become visible.

### Race-freedom argument

Exclusive ownership of output tile $C_{I,J}$ is race-free if only its owner mutates it and all input tiles are immutable during the task. For destination-owned graph updates, race freedom holds if messages are immutable, the destination owner alone applies them, and its local application order satisfies the operator’s semantics. Commutativity may permit order independence; idempotence may tolerate duplicates; neither should be assumed without proof.

### Capacity and progress invariants

At every task boundary, live operands, output, packed buffers, indices, queues, and temporary reductions must fit the declared budget. Every scheduled block is eventually processed or durably retried. A completed block records enough identity to prevent omission or unintended duplicate publication. These resource and progress properties are separate from mathematical correctness.

## Alternatives and Trade-Offs

| Choice | Advantage | Cost or risk | Appropriate evidence |
|---|---|---|---|
| explicit rectangular tiles | predictable bounds and tunable kernels | parameter tied to hierarchy and shape | size sweep plus counters |
| recursive subdivision | adapts across several scales | base-case and layout overhead | recursion/base-case comparison |
| packed dense panels | contiguous access and vectorization | copy, workspace, NUMA placement | amortized end-to-end timing |
| blocked sparse format | fewer indices and denser kernels when occupied | zero fill and conversion cost | occupancy distribution |
| vertex partition | simple state ownership | degree and edge imbalance | per-owner active-edge counts |
| edge partition | direct work balance | replicated or contested vertex state | communication and reduction counts |
| two-dimensional graph partition | smaller source/destination slices | row/column coordination | message volume and latency |
| atomics | simple shared update path | contention and nondeterminism | collision distribution |
| private partials plus reduction | fewer write races | memory and reduction traffic | peak memory and reduction cost |

Cache-oblivious algorithms, developed next in ALGE-088, use recursive structure without a cache-size parameter. They can obtain good asymptotic transfer behavior under idealized models, but base cases, layout, allocation, and parallel scheduling still need engineering. Autotuning chooses parameters empirically; it must avoid overfitting to one size or machine state.

## Failure Modes and Misconceptions

- **“The tile fits in cache.”** Three payload tiles are not the full live set, and associativity can defeat capacity arithmetic.
- **“Blocking changes big-O arithmetic.”** Conventional dense tiling still performs $mnk$ scalar products; its main target is movement and kernel efficiency.
- **“The largest fitting tile is best.”** Register blocking, cache levels, prefetching, packing, edge tiles, and concurrency create a multidimensional choice.
- **“A graph block is a dense tile.”** Low occupancy can make dense storage catastrophically wasteful.
- **“Balanced vertices mean balanced work.”** Degrees and active-frontier membership may be highly skewed.
- **“A low edge cut solves locality.”** It may ignore cache layout, messages, destination contention, and dynamic frontiers.
- **“Relabeling is semantics-free.”** Identity maps, external references, directed orientation, duplicates, and update streams must remain correct.
- **“Associativity licenses arbitrary floating-point reduction.”** Algebraic associativity does not hold exactly for finite-precision addition.
- **“More parallel blocks always help.”** Tasks can multiply buffers, create false sharing, overload queues, and reduce per-task reuse.
- **“A faster blocked benchmark proves cache efficiency.”** Vectorization, compiler changes, frequency, allocation, or warm state may be the cause; collect targeted evidence.

## Worked Examples

### Example 1

**Situation.** Multiply an $m=5$, $k=3$, $n=4$ problem with tile size two. Does the clipped last row tile lose work?

**Reasoning.** Row ranges are $\{0,1\}$, $\{2,3\}$, and $\{4\}$; reduction ranges are $\{0,1\}$ and $\{2\}$; column ranges are $\{0,1\}$ and $\{2,3\}$. Entry $C_{4,3}$ belongs to the unique row/column tile $\{4\}\times\{2,3\}$. Its two reduction tiles contribute terms for $t=0,1$ and $t=2$, so all three terms occur once. Clipping changes loop endpoints, not coverage.

**Conclusion.** Non-divisible dimensions are correct when ranges form disjoint covers; padding is optional, not required.

### Example 2

**Situation.** A simplified kernel has 32 KiB usable storage for three square tiles of eight-byte values. What upper bound follows?

**Reasoning.** Require $3b^2(8)\le32768$. Thus $b^2\le1365.33$ and $b\le36$. This is only a necessary estimate: a practical design reserves space for packing, stack, cache conflicts, and concurrent activity. Choosing $b=32$ uses $3\cdot32^2\cdot8=24576$ bytes for payload tiles, leaving 8192 bytes of nominal headroom.

**Conclusion.** Capacity arithmetic narrows candidates; measurement and a fuller working-set model choose among them.

### Example 3

**Situation.** Why are there eight tile triples and 64 scalar updates for the $4\times4$, tile-two reference?

**Reasoning.** Each dimension has $\lceil4/2\rceil=2$ tile ranges, so $(I,J,K)$ has $2^3=8$ combinations. Each triple contains $2^3=8$ scalar update iterations, giving $8\cdot8=64$. The direct algorithm also covers $4^3=64$ triples $(i,k,j)$. The result matrix matches exactly because integer addition and multiplication are exact for these values.

**Conclusion.** The trace validates coverage and output, while making no cache-performance claim.

### Example 4

**Situation.** Can reduction tiles be combined in any order and still produce the same floating-point result?

**Reasoning.** Consider the terms $10^{16}$, $-10^{16}$, and $1$ in binary64-like arithmetic. Accumulating left to right gives $(10^{16}-10^{16})+1=1$. Combining the last two first can round $-10^{16}+1$ to $-10^{16}$, then add $10^{16}$ to obtain $0$. A parallel $K$-tile reduction can select either grouping.

**Conclusion.** A blocked implementation needs an error or reproducibility contract; algebraic equivalence alone does not promise bitwise equality.

### Example 5

**Situation.** A $4\times4$ sparse block contains three nonzeros. Values and indices each use eight bytes. Compare simple dense payload with coordinate pairs.

**Reasoning.** Dense payload stores 16 values, or 128 bytes, ignoring outer metadata. Three `(index,value)` pairs use $3\cdot16=48$ bytes, again ignoring metadata. Dense storage performs or scans many zero positions, although it may enable a regular kernel. At occupancy $3/16$, its payload is already $128/48\approx2.67$ times larger.

**Conclusion.** Block coordinates alone do not justify dense microblocks; occupancy and kernel benefit must repay zero fill.

### Example 6

**Situation.** Eight vertices are split four per worker. The first partition has degrees $100,1,1,1$ and the second has $26,26,26,25$. Is the partition balanced?

**Reasoning.** Vertex counts are equal. Edge work is $103$ versus $103$, so this particular split is also edge-balanced overall. Yet within the first worker, one vertex owns 97% of its work and may form a serial straggler if vertices are task units. If that high-degree vertex’s destinations concentrate remotely, communication can also be skewed.

**Conclusion.** Balance must name both weight and scheduling granularity; equal totals can still hide a large indivisible task.

### Example 7

**Situation.** A push traversal has 10,000 active outgoing edges, 70% crossing destination owners. Should sources or destinations own updates?

**Reasoning.** Source ownership scans local adjacency naturally but emits about 7,000 cross-owner update attempts. Destination ownership can make application race-free, yet those updates still need routing or prepartitioned edge blocks. Grouping by destination block can convert scattered atomics into buffered messages, but buffering adds memory and latency. A pull representation may avoid update messages only if incoming adjacency exists and the frontier density makes its scans worthwhile.

**Conclusion.** Ownership changes where synchronization occurs; it does not erase communication implied by the partition.

### Example 8

**Situation.** Partition A cuts 1,000 edges with balanced active work. Partition B cuts 700 edges but assigns 80% of the current frontier edges to one worker. Which is better?

**Reasoning.** Partition B wins the static edge-cut metric but creates a likely step-time straggler. If traversal barriers each level, completion time is governed by the slowest worker. Partition A sends 300 more cross edges yet may finish sooner through balanced active work. The decision needs message cost, per-worker work, and frontier evolution, not cut alone.

**Conclusion.** Static partition quality is a workload-dependent proxy, not the optimization objective itself.

### Example 9

**Situation.** Packing a panel costs reading and writing 64 KiB. It saves 24 KiB of later traffic per reuse. How many reuses repay the copy under a byte-only model?

**Reasoning.** Packing moves approximately $2\cdot64=128$ KiB. After $r$ reuses, saved traffic is $24r$ KiB. Require $24r\ge128$, so $r\ge5.34$ and the first integer break-even is six reuses. Allocation, vector speedup, write allocation, and bandwidth asymmetry can move the real threshold.

**Conclusion.** Packing needs amortization; a one-use panel loses under this simplified traffic account.

### Example 10

**Situation.** A tiled graph kernel is 1.8 times faster on one social graph. What evidence supports a locality explanation?

**Reasoning.** Preserve a semantic oracle and record graph checksum, orientation, relabeling map, and result equivalence. Compare unblocked, loop-blocked, and layout-blocked variants under the same compiler, affinity, NUMA placement, and warm/cold policy. Use multiple graph families and frontier densities. Report preprocessing separately and amortized. Collect named cache, memory, translation, branch, synchronization, and per-worker work metrics where reliable; repeat runs and report distributions.

**Conclusion.** The speedup is an observation; the locality explanation becomes credible only when controlled measurements exclude plausible alternatives.

## Cross-Program Connections

- [Computer Architecture CA-031](../../23-computer-architecture/modules/031-locality-and-the-memory-wall.md) explains the hierarchy and memory wall that blocking targets.
- [Computer Architecture CA-040](../../23-computer-architecture/modules/040-analyzing-cache-misses-from-an-access-trace.md) supplies trace-based cache reasoning and its limitations.
- [Data Structures Engineering DSE-001](../../17-data-structures-engineering/modules/001-abstract-data-types-and-concrete-representations.md) distinguishes graph or matrix semantics from concrete representation.
- [Operating Systems OS-031](../../22-operating-systems/modules/031-address-translation.md) connects tile footprints to pages, translation, and TLB behavior.
- [Operating Systems OS-040](../../22-operating-systems/modules/040-diagnosing-memory-pressure-and-thrashing.md) shows why aggregate working sets and concurrency can defeat local capacity plans.
- [Distributed Systems DIST-001](../../27-distributed-systems-engineering/modules/001-why-distribution-changes-the-problem.md) frames remote communication, ownership, and partial failure beyond shared memory.

## References

1. Kazushige Goto and Robert A. van de Geijn, “Anatomy of High-Performance Matrix Multiplication,” *ACM Transactions on Mathematical Software* 34(3), Article 12, 2008. [doi:10.1145/1356052.1356053](https://doi.org/10.1145/1356052.1356053). Checked 2026-09-05.
2. Fred G. Gustavson, “Two Fast Algorithms for Sparse Matrices: Multiplication and Permuted Transposition,” *ACM Transactions on Mathematical Software* 4(3), 250–269, 1978. [doi:10.1145/355791.355796](https://doi.org/10.1145/355791.355796). Checked 2026-09-05.
3. Aydın Buluç and John R. Gilbert, “On the Representation and Multiplication of Hypersparse Matrices,” *IPDPS 2008*, 2008. [doi:10.1109/IPDPS.2008.4536313](https://doi.org/10.1109/IPDPS.2008.4536313). Checked 2026-09-05.
4. Benjamin Brock et al., *The GraphBLAS C API Specification*, Version 2.1.0, 22 December 2023. [Official specification](https://graphblas.org/docs/GraphBLAS_API_C_v2.1.0.pdf). Checked 2026-09-05.
5. A. N. Yzelman and Rob H. Bisseling, “Cache-Oblivious Sparse Matrix–Vector Multiplication by Using Sparse Matrix Partitioning Methods,” *SIAM Journal on Scientific Computing* 31(4), 3128–3154, 2009. [doi:10.1137/080733243](https://doi.org/10.1137/080733243). Checked 2026-09-05.
6. Dror Irony, Sivan Toledo, and Alexander Tiskin, “Communication Lower Bounds for Distributed-Memory Matrix Multiplication,” *Journal of Parallel and Distributed Computing* 64(9), 1017–1026, 2004. [doi:10.1016/j.jpdc.2004.03.021](https://doi.org/10.1016/j.jpdc.2004.03.021). Checked 2026-09-05.
7. Grey Ballard, James Demmel, Olga Holtz, and Oded Schwartz, “Communication-Optimal Parallel and Sequential Cholesky Decomposition,” *SIAM Journal on Scientific Computing* 32(6), 3495–3523, 2010. [doi:10.1137/090760969](https://doi.org/10.1137/090760969). Checked 2026-09-05.
8. Ulrich Meyer, Peter Sanders, and Jop Sibeyn, editors, *Algorithms for Memory Hierarchies*, Springer, 2003. [doi:10.1007/3-540-36574-5](https://doi.org/10.1007/3-540-36574-5). Checked 2026-09-05.

## Exercises

### Exercise 1

A program merely changes loop order over a row-major matrix. Identify which of partitioning, layout, packing, scheduling, and ownership necessarily changed and which did not.

### Exercise 2

For $A$ of shape $7\times5$, $B$ of shape $5\times6$, and tile size three in every dimension, derive the number of tile triples and scalar updates when boundary loops are clipped.

### Exercise 3

A parallel blocked multiplication assigns different $K$ tiles of the same output tile to workers that write directly into shared $C$ without atomics or reduction. Explain the failure and give two correct designs, including their numerical implications.

### Exercise 4

Compare one-dimensional source partitioning with two-dimensional adjacency blocking for a directed graph with skewed degrees and repeated sparse frontiers. State the deciding measurements.

### Exercise 5

Design a blocking plan for repeated two-dimensional five-point stencil updates. State the block, halo, ownership, correctness invariant, capacity concern, boundary treatment, and evidence needed for a locality claim.

## Answers to the Exercises

### Answer 1

Loop order necessarily changes scheduling: it changes when logical iterations execute. It may expose a conceptual partition if loops now traverse explicit ranges, but a permutation alone need not create stored block objects. Row-major layout does not change. Packing does not occur without copying into another representation. Ownership does not change in a sequential program and changes in a parallel program only if iterations are reassigned. A good answer separates the source-code loop transformation from claims about physical representation.

### Answer 2

The row dimension has $\lceil7/3\rceil=3$ tiles, the reduction dimension has $\lceil5/3\rceil=2$, and the column dimension has $\lceil6/3\rceil=2$. Therefore there are $3\cdot2\cdot2=12$ tile triples. Clipping preserves every scalar triple $(i,t,j)$, so updates total $7\cdot5\cdot6=210$, not $12\cdot27=324$; the latter incorrectly treats boundary tiles as full. The expected evidence is the ceiling calculation plus the coverage argument.

### Answer 3

Workers can lose updates through read-modify-write races: two workers may read the same old $C_{ij}$ and overwrite one another. One correct design gives an output tile exclusively to one worker, which processes all its $K$ tiles in a defined order. Another gives workers private partial output tiles and reduces them after a barrier. The latter consumes extra memory and traffic; its reduction grouping may change floating-point rounding. Atomics are a possible third design but may contend and still provide an unspecified accumulation order. Correctness requires race freedom plus the declared numerical contract.

### Answer 4

Source partitioning keeps outgoing adjacency and frontier tests local and is simple, but high-degree active vertices can skew work and remote destinations create messages or atomics. Two-dimensional blocking can cluster source and destination slices, reduce per-task state, and offer more edge-granular scheduling, but it adds block metadata and row/column coordination and may create many nearly empty blocks. Decide using distributions of active edges per owner and block, cross-owner updates, nonempty-block counts, metadata bytes, frontier densities, synchronization time, preprocessing/amortization horizon, and end-to-end step time across representative graphs. Edge cut alone is insufficient.

### Answer 5

Partition the interior grid into rectangular output tiles. Each owner computes one tile for one time step and reads a one-cell halo from the previous immutable time layer; double buffering prevents reading partially updated values. The invariant is that every next-layer interior cell is written once from exactly its previous-layer north, south, east, west, and center values. The live set includes the output tile, input tile plus halo, both time layers as applicable, metadata, and concurrent-worker buffers. Clip physical boundaries and apply the specified boundary condition—fixed, periodic, or reflective—rather than silently padding zeros. Validate tiny grids and boundary cases against an unblocked reference, then measure bytes, cache/translation events where reliable, halo exchange, balance, and end-to-end time across tile sizes. Acceptable alternatives include temporal blocking, but they must enlarge halos and prove dependency coverage. Evaluation should reward explicit semantics, ownership, capacity, and separated correctness/performance evidence.
