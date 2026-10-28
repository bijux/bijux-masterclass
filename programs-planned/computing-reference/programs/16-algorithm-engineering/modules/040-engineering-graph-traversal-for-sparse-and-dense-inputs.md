---
module_id: ALGE-040
program: Algorithm Engineering
level: 1
module_number: 40
title: Engineering Graph Traversal for Sparse and Dense Inputs
status: complete
last_verified: 2026-09-05
---

# Engineering Graph Traversal for Sparse and Dense Inputs

## One-Page Review

### Governing question

How should an implementation choose, build, traverse, measure, and validate a graph representation when sparsity, density, degree skew, mutability, memory hierarchy, direction, and output requirements materially change observed behavior?

### Essential definitions

- $n=|V|$ and $m=|E|$ count declared vertices and logical directed edges.
- **Density** for a simple directed graph is $m/n^2$ when self-loops are allowed, under an explicitly chosen denominator.
- An **adjacency list** stores neighbors of each vertex, using $O(n+m)$ logical entries.
- **CSR** stores contiguous neighbor entries plus $n+1$ offsets and is compact for static sparse graphs.
- An **adjacency matrix** stores one cell per ordered pair, using $\Theta(n^2)$ cells.
- A **frontier** is the active set for the next traversal step.
- **Push** visits outgoing edges of frontier vertices; **pull** lets unvisited vertices inspect incoming neighbors.
- **locality** describes how predictably accesses use nearby memory/cache lines.
- A **logical edge** may occupy one arc in a directed representation or two stored arcs in an undirected representation.

### Central model, mechanism, or theorem

BFS and DFS over adjacency lists perform $O(n+m)$ vertex and edge work. Scanning a matrix row for every reached vertex performs $O(n^2)$ potential-neighbor probes, even when few cells contain edges. The asymptotic crossover is not a fixed density percentage: cell width, offsets, identifiers, properties, cache behavior, vectorization, update pattern, and algorithm access shape determine actual costs.

Representation is part of the algorithm contract. A traversal is correct only if the encoded vertex universe, direction, multiplicity, self-loop policy, property association, and snapshot match the modeled graph. Performance evidence requires the actual workload, graph family, machine, layout, compiler/runtime, and measurement method.

### Critical invariants

- Stable vertex IDs map bijectively to the dense indices used by arrays or matrices.
- Every stored endpoint is in range and every required isolated vertex exists.
- Directed and undirected logical edges expand into the declared stored-arc convention exactly once.
- CSR offsets are monotone, start at zero, end at the neighbor-array length, and delimit each vertex's adjacency.
- Neighbor order is either semantically irrelevant or explicitly deterministic.
- Discovery is atomic with frontier insertion under parallel traversal, preventing duplicate ownership.
- Each list/CSR arc is considered at most as promised; matrix traversal accounts for absent-cell probes.
- Input conversion and output materialization are counted separately from kernel traversal.
- Snapshot identity covers vertices, edges, properties, index mapping, representation, traversal, and validation.

### Common failures

Frequent failures include inferring vertices only from edges; counting stored undirected arcs as logical edges; losing parallel edges in a Boolean matrix; using zero as both absent and zero-weight; building CSR with incorrect prefix sums; assuming sorted neighbors without sorting; invalidating vector-backed IDs after deletion; comparing kernels while excluding only one format's conversion cost; reporting wall time without warm-up or machine metadata; using push on a huge high-degree frontier; using pull without incoming adjacency; racing discovery bits; materializing a quadratic matrix accidentally; and generalizing from one synthetic graph.

### Compact example

With five vertices and five directed edges, adjacency-list BFS from a source that reaches all vertices examines five stored arcs. Matrix BFS scans five cells for each of five reached vertices: 25 probes. Both return the same reachability, but their work and memory access differ. At high density, those matrix probes may become regular, vectorizable accesses rather than mostly wasted tests.

### Connections

[ALGE-031](./031-breadth-first-search.md) and [ALGE-032](./032-depth-first-search.md) supply traversal invariants; [ALGE-034](./034-strongly-connected-components.md) needs both directions or a transpose; [ALGE-036](./036-dijkstra-s-shortest-paths.md) adds priority access; [ALGE-038](./038-all-pairs-shortest-paths.md) motivates dense matrices. [ALGE-041](../ROADMAP.md#block-05--flows-matching-and-combinatorial-optimization) next introduces residual graphs with stricter paired-edge mutation.

## Governing Question

For a known graph family and workload, which representation and traversal schedule minimizes total resource cost while preserving graph semantics, deterministic evidence, failure behavior, and a reproducible performance claim?

There is no universal “best graph structure.” Lists expose existing neighbors, matrices expose potential neighbors, CSR packs static sparse edges, hash-backed adjacency supports mutation, and edge lists support scans and sorting. Algorithms consume different operations: neighbor iteration, edge lookup, reverse traversal, bulk frontier expansion, edge sorting, or dense algebra.

## Why This Matters

Two implementations of the same $O(n+m)$ traversal can differ by orders of magnitude because graph computation often stresses memory bandwidth and irregular access rather than arithmetic. Degree skew concentrates work. Vertex labels trigger random writes. Poor index mapping inflates storage. A representation conversion may cost more than one query.

Engineering decisions are correctness decisions too. A Boolean matrix collapses parallel edges. A one-direction CSR cannot supply incoming neighbors. A dynamic adjacency vector can invalidate descriptors. An undirected loader can double self-loops accidentally. A benchmark that drops isolated vertices changes both $n$ and the answer.

Current graph systems expose multiple structures because these tradeoffs persist. Boost.Graph 1.92.0 documents adjacency lists, matrices, and compressed sparse row graphs with different mutability and access profiles; GraphBLAS expresses graph kernels through sparse matrix/vector operations over declared algebraic operators. These are current interfaces, while representation invariants and workload-based selection are durable.

## Prerequisites and Retrieval

Retrieve BFS, DFS, connected components, SCC, shortest paths, and APSP; arrays, linked or vector containers, hash tables, bitsets, prefix sums, CSR/CSC, matrices, queues, caches, bandwidth, atomics, asymptotic analysis, experimental design, and confidence limits. Review [ALGE-031](./031-breadth-first-search.md), [ALGE-032](./032-depth-first-search.md), and [ALGE-038](./038-all-pairs-shortest-paths.md).

## Learning Objectives

After completing this module, you should be able to:

1. specify logical graph semantics separately from physical storage;
2. derive list, CSR, edge-list, matrix, and bit-matrix costs;
3. build and validate CSR offsets and neighbor arrays;
4. compare list and matrix traversal with equivalent outputs and explicit probes;
5. choose push, pull, or direction-optimizing frontier processing;
6. account for degree skew, locality, allocation, identifiers, and properties;
7. design fair conversion-inclusive and kernel-only measurements;
8. handle parallel discovery, partitioning, snapshots, cancellation, and publication;
9. validate cross-representation semantic equivalence;
10. make bounded performance conclusions without treating asymptotics or one benchmark as universal proof.

## Core Exposition

### Specify graph semantics before layout

Declare directedness, whether self-loops and parallel edges are allowed, complete vertex universe, stable edge identity, property types, ordering promises, snapshot revision, and required operations. A simple Boolean adjacency matrix represents existence, not multiplicity or per-edge identity. An undirected logical edge usually becomes two adjacency arcs, except a self-loop policy must avoid accidental duplication.

Density itself needs a denominator. For directed simple graphs with loops allowed there are $n^2$ possible edges; without loops $n(n-1)$. Undirected denominators halve the off-diagonal possibilities. State the convention before comparing datasets.

### Compare representation costs

An adjacency list uses one per-vertex container plus stored arcs. It iterates existing neighbors in $O(\deg^+(v))$, but pointer-rich containers add allocation and locality costs. Sorted vectors improve scans and binary lookup but make insertion expensive.

CSR stores offset array `offset[0..n]` and contiguous `neighbor[0..a-1]`, where $a$ is stored-arc count. Neighbors of $v$ occupy half-open range `[offset[v], offset[v+1])`. Static construction counts arcs per source, prefix-sums counts, then fills positions. CSC or a second reverse CSR supports incoming traversal.

An adjacency matrix uses $n^2$ cells for directed graphs. Edge lookup is constant and rows are regular, but neighbor enumeration scans $n$ positions. Bit matrices reduce existence storage by a factor near word width and enable word-parallel intersections, while weighted/property matrices need wider cells or separate structures.

An edge list is compact and natural for sorting, streaming, Bellman-Ford passes, and bulk transforms, but repeated per-vertex neighbor queries require indexing or rescanning.

### Make the sparse/dense work visible

The following executable builds the same directed graph as sorted adjacency lists and a Boolean matrix, performs BFS with identical discovery policy, and records potential-neighbor probes.

<!-- bijux-verify: {"id":"list-matrix-bfs","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"vertices=5 edges=5 density=0.200\nlist_order=('a', 'b', 'c', 'd', 'e')\nmatrix_order=('a', 'b', 'c', 'd', 'e')\nlist_probes=5 matrix_probes=25\nsame=True\n","stderr":""}} -->
```python
from collections import deque


def build(vertices, edges):
    vertices = tuple(sorted(set(vertices)))
    index = {vertex: position for position, vertex in enumerate(vertices)}
    adjacency = {vertex: [] for vertex in vertices}
    matrix = [[False] * len(vertices) for _ in vertices]
    seen = set()
    for edge_id, tail, head in edges:
        if edge_id in seen or tail not in index or head not in index:
            raise ValueError(f"invalid edge: {edge_id}")
        seen.add(edge_id)
        adjacency[tail].append(head)
        matrix[index[tail]][index[head]] = True
    adjacency = {v: tuple(sorted(ns)) for v, ns in adjacency.items()}
    return vertices, index, adjacency, tuple(tuple(row) for row in matrix)


def bfs_list(adjacency, source):
    queue, seen, order, probes = deque([source]), {source}, [], 0
    while queue:
        vertex = queue.popleft()
        order.append(vertex)
        for neighbor in adjacency[vertex]:
            probes += 1
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return tuple(order), probes


def bfs_matrix(vertices, index, matrix, source):
    queue, seen, order, probes = deque([source]), {source}, [], 0
    while queue:
        vertex = queue.popleft()
        order.append(vertex)
        for position, neighbor in enumerate(vertices):
            probes += 1
            if matrix[index[vertex]][position] and neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return tuple(order), probes


vertices = {"a", "b", "c", "d", "e"}
edges = (("ab", "a", "b"), ("ac", "a", "c"),
         ("bd", "b", "d"), ("cd", "c", "d"),
         ("de", "d", "e"))
vertices, index, adjacency, matrix = build(vertices, edges)
list_order, list_probes = bfs_list(adjacency, "a")
matrix_order, matrix_probes = bfs_matrix(vertices, index, matrix, "a")
print(f"vertices={len(vertices)} edges={len(edges)} "
      f"density={len(edges) / len(vertices) ** 2:.3f}")
print(f"list_order={list_order}")
print(f"matrix_order={matrix_order}")
print(f"list_probes={list_probes} matrix_probes={matrix_probes}")
print(f"same={list_order == matrix_order}")
```

Probe counts are one cost dimension, not timings. Python object overhead dominates this tiny run, and deterministic order was engineered explicitly. The result demonstrates semantic equivalence for one graph and makes absent matrix probes observable; it does not establish a universal crossover.

### Build CSR with checkable invariants

Given dense source indices, count outgoing arcs into `degree[v]`. Exclusive prefix sum yields offsets: `offset[0]=0` and `offset[v+1]=offset[v]+degree[v]`. Copy offsets into cursors, then place each neighbor and advance its source cursor.

Validate offset length $n+1$, monotonicity, first zero, last equal to arc length, cursor completion, endpoint range, and declared neighbor ordering. To retain edge IDs or weights, align parallel arrays or store structs; all arrays need the same permutation and snapshot. For deterministic sorted adjacency, sort each CSR slice or globally sort by `(source,target,edge_id)` before construction.

### Engineer frontier direction

Top-down or **push** BFS scans outgoing arcs of frontier vertices. It is efficient when the frontier is small. Near the middle of a low-diameter graph, a large frontier may inspect many edges leading to already visited vertices.

Bottom-up or **pull** BFS scans unvisited vertices and asks whether any incoming neighbor lies in the current frontier, stopping at the first match. It can reduce work for broad frontiers but needs incoming adjacency, a fast frontier-membership structure, and scans over unvisited vertices. Direction-optimizing BFS switches using observed frontier/remaining-work metrics. Beamer, Asanović, and Patterson's 2012 work supplies a primary analysis; thresholds remain machine and graph dependent.

DFS has a narrow active stack rather than a level frontier and usually benefits from compact sequential adjacency. Algorithms such as PageRank or GraphBLAS kernels may prefer edge-centric or sparse-matrix schedules. Match layout to the actual access pattern rather than the generic word “traversal.”

### Account for degree skew and locality

Average degree $m/n$ hides hubs. A power-law-like graph can assign most edge work to few vertices, harming static vertex partitioning. Partition by estimated arc work, split high-degree adjacency, or use dynamic scheduling, while preserving deterministic/correct discovery.

CSR improves neighbor locality but destination-state accesses remain irregular. Reordering vertices can improve locality or compression but changes external indices; retain a bijection and translate outputs. Compressed integer encodings reduce bandwidth but add decode cost and complicate random access. NUMA placement, prefetching, huge pages, vectorization, and GPU transfer matter only when measured under the target environment.

### Make parallel discovery correct

Sequential BFS marks a vertex discovered before enqueueing it. Parallel push must preserve the same single-owner transition with an atomic test-and-set or equivalent partitioned ownership. Marking after enqueue permits duplicates, excess memory, duplicate callbacks, and possibly incorrect parent claims.

Parallel outputs need a tie policy. Distances may be deterministic while predecessor trees and visitation order vary. If deterministic parents are required, choose a stable reduction rule and include its additional synchronization/work. Never infer semantic nondeterminism from two different valid BFS trees.

### Design honest measurements

Separate input parse, identity mapping, deduplication, transpose, representation build, warm-up, kernel, validation, and output. Report both end-to-end and kernel-only results when both matter. Record dataset digest and structural statistics: $n$, logical $m$, stored arcs, loops, parallel edges, degree distribution, component sizes, diameter proxy, and property widths.

Record hardware, OS, runtime/compiler and flags, thread affinity, memory placement, run count, aggregation statistic, variance, cold/warm cache policy, and correctness outcome. Measure edges examined, absent probes, frontier sizes, bytes allocated, peak resident memory, cache/bandwidth counters when trustworthy, atomic conflicts, and conversion time.

A crossover observed on one graph family and machine is empirical evidence for that scope only. Big-O bounds exclude constants and architecture but remain useful for ruling out quadratic materialization at scale.

### Validate across representations

Build two representations from one canonical edge stream and compare normalized vertex sets and logical edge multisets, not raw bytes. Run BFS/DFS from sampled sources including isolates, hubs, sinks, and small components; compare reachability and distances while allowing declared tie differences.

Adversarial cases include empty graph, one vertex, self-loops, zero-property edges, parallel edges, reciprocal arcs, disconnected components, one huge hub, long chain, complete graph, invalid endpoint, duplicate edge ID, integer overflow in offsets, allocation failure, truncated input, cancellation at every build/traversal boundary, and snapshot replacement.

### Govern lifecycle and current interfaces

Mutable lists suit updates but can fragment and invalidate iterators. CSR usually requires rebuild or delta overlays; compaction must be versioned. Matrices have fixed quadratic capacity but simple edge toggles. Choose batch/update/query architecture explicitly.

Current [Boost.Graph 1.92.0 documentation](https://www.boost.org/doc/libs/latest/libs/graph/doc/html/graph/graph_classes/overview.html) distinguishes adjacency-matrix, adjacency-list, and CSR mutability and access patterns. The [GraphBLAS C API 2.1.0 specification](https://graphblas.org/docs/GraphBLAS_API_C_v2.1.0.pdf) defines sparse matrix/vector graph primitives. These versioned interfaces illustrate present practice; they do not replace workload measurement or the graph's semantic contract.

Pin canonical graph digest, vertex-index map, representation build parameters, reverse-edge policy, algorithm, runtime state, and validation. Checkpoints record revision, frontier/stack, visited and distance state, representation version, cursors, thread schedule assumptions, and output position. Cancellation is incomplete, not unreachable. Publish results only with scope, snapshot, representation/algorithm version, and validation outcome.

## Definitions and Notation

- $n$, $m$: vertex and logical directed-edge counts.
- $a$: stored-arc count, which may differ from $m$.
- $\deg^+(v)$, $\deg^-(v)$: out-degree and in-degree.
- **adjacency list:** per-vertex collection of existing neighbors/edges.
- **CSR/CSC:** compressed sparse row/column layouts.
- **adjacency matrix:** one cell per possible ordered pair.
- **frontier:** active vertices at one level or iteration.
- **push/pull:** edge expansion from active sources / inspection from inactive targets.
- **index map:** bijection between external stable IDs and dense positions.
- **kernel-only time:** traversal computation excluding declared conversion and output stages.
- **end-to-end time:** full accepted-input-to-validated-output latency.

## Mechanisms, Invariants, or Proof Structure

Representation construction preserves the canonical graph's vertex and logical-edge semantics. List traversal bounds work by summing degrees: $\sum_v\deg^+(v)=m$. Matrix traversal checks $n$ potential neighbors for each of up to $n$ reached vertices. CSR correctness follows from degree counts and prefix-sum slice ownership. BFS discovery remains correct when each unseen-to-seen transition is atomic. Cross-representation validation compares semantic outputs under one snapshot. Measurement conclusions remain bounded to the recorded environment and graph population.

## Alternatives and Trade-Offs

- **Vector adjacency:** compact scans and sortable order; insert/delete may move storage.
- **Hash adjacency:** flexible lookup and mutation; high overhead and unstable iteration unless governed.
- **CSR/CSC:** compact static scans; expensive rebuild and dual storage for both directions.
- **Dense matrix:** constant edge lookup and regular rows; quadratic storage and sparse wasted probes.
- **Bit matrix:** compact Boolean operations; loses multiplicity/properties unless supplemented.
- **Edge list:** excellent streaming/sorting; poor repeated neighbor queries without indexes.
- **Push:** frontier-proportional outgoing work; redundant probes on broad frontiers.
- **Pull:** useful for broad frontiers; requires incoming adjacency and scans unvisited vertices.

## Failure Modes and Misconceptions

- Sparse/dense is not a universal fixed-percentage threshold.
- $O(n+m)$ does not predict cache misses, allocation, or parallel contention.
- An undirected logical edge count is not automatically its stored-arc count.
- A matrix may collapse parallel identities and properties.
- CSR is not inherently immutable, but safe mutation needs a declared design beyond static arrays.
- Deterministic distances do not imply deterministic predecessor trees.
- Faster unvalidated output is not a valid benchmark win.
- Excluding conversion from only one competitor is not a fair comparison.
- One social, road, mesh, or random graph cannot represent all graph families.
- Parallelism does not repair a representation whose memory footprint cannot fit.

## Worked Examples

### Example 1

**Situation.** A directed graph has $n=1{,}000{,}000$ and $m=5{,}000{,}000$. A byte matrix needs $10^{12}$ bytes; CSR with 64-bit offsets and 32-bit neighbors needs roughly 8,000,008 plus 20,000,000 bytes before properties. **Conclusion.** Sparse layout changes feasibility, not merely speed.

### Example 2

**Situation.** Undirected edge $\{u,v\}$ becomes arcs $u\to v$ and $v\to u$. A self-loop $\{u,u\}$ should follow one declared encoding rather than being doubled accidentally. **Conclusion.** Logical and physical edge counts require explicit policy.

### Example 3

**Situation.** Degrees are $(2,0,1)$. CSR offsets are $(0,2,2,3)$ and neighbor length three. Offset decrease or final value four would prove malformed storage. **Conclusion.** Prefix-sum invariants make representation checkable.

### Example 4

**Situation.** A five-vertex sparse BFS examines five list arcs but 25 matrix cells. Both orders match. **Conclusion.** Equivalent semantics can expose very different work.

### Example 5

**Situation.** One frontier contains 80% of vertices, most remaining vertices have a frontier predecessor, and outgoing push would scan nearly all arcs. Pull can stop after the first matching incoming neighbor. **Conclusion.** Frontier shape can justify direction switching.

### Example 6

**Situation.** Two parallel workers both see vertex $x$ unseen and enqueue it before either writes the visited flag. Its callback runs twice. **Conclusion.** Discovery must be one atomic state transition when ownership matters.

### Example 7

**Situation.** Relabeling vertices by partition improves locality but a caller interprets dense index 17 as the old external vertex. **Conclusion.** Reordering requires a versioned bijection at every boundary.

### Example 8

**Situation.** Algorithm A reports kernel-only warm-cache time; B includes parsing, CSR build, validation, and cold start. A appears faster without comparable scope. **Conclusion.** Measurement boundaries are part of evidence.

### Example 9

**Situation.** A Boolean matrix receives three parallel weighted edges. One cell cannot preserve all IDs or weights. **Conclusion.** Representation may be semantically incapable even when memory fits.

### Example 10

**Situation.** Cancellation occurs after a CSR prefix sum but before all neighbor slots are filled. Publishing it exposes in-range offsets over uninitialized data. **Conclusion.** Build state is incomplete until cursor and endpoint validation pass.

## Cross-Program Connections

- Data Structures Engineering owns arrays, CSR, matrices, hash tables, queues, and layout invariants.
- Computer Architecture owns cache, NUMA, vectorization, bandwidth, atomics, and accelerators.
- Concurrent Programming and Distributed Systems own parallel discovery, barriers, partitioning, and termination.
- Database/Data Engineering own canonical ingestion, index maps, snapshots, deltas, compaction, and lineage.
- Performance Engineering owns benchmark design, measurement uncertainty, and regression governance.
- Security Engineering owns hostile sizes, malformed offsets, allocation limits, and identity confusion.

## References

1. Scott Beamer, Krste Asanović, and David Patterson, “Direction-Optimizing Breadth-First Search,” *SC '12*, 2012, DOI [10.1109/SC.2012.50](https://doi.org/10.1109/SC.2012.50). Primary source checked 2026-09-05.
2. Julian Shun and Guy E. Blelloch, “Ligra: A Lightweight Graph Processing Framework for Shared Memory,” *PPoPP '13*, 2013, DOI [10.1145/2442516.2442530](https://doi.org/10.1145/2442516.2442530). [Author publication page](https://jshun.csail.mit.edu/ligra.shtml), checked 2026-09-05.
3. Aydın Buluç and John R. Gilbert, “The Combinatorial BLAS: Design, Implementation, and Applications,” *International Journal of High Performance Computing Applications* 25(4), 2011, DOI [10.1177/1094342011403516](https://doi.org/10.1177/1094342011403516). Primary source checked 2026-09-05.
4. Boost C++ Libraries, “Graph Data Structures,” Boost.Graph 1.92.0 documentation. [Official documentation](https://www.boost.org/doc/libs/latest/libs/graph/doc/html/graph/graph_classes/overview.html), checked 2026-09-05.
5. GraphBLAS Forum, *GraphBLAS C API Specification*, version 2.1.0, 2023. [Official specification](https://graphblas.org/docs/GraphBLAS_API_C_v2.1.0.pdf), checked 2026-09-05.
6. David A. Bader et al., “Designing Scalable Synthetic Compact Applications for Benchmarking High Productivity Computing Systems,” 2006, Graph Analysis Benchmark specifications. [Graph500 benchmark specification site](https://graph500.org/), checked 2026-09-05.

## Exercises

### Exercise 1

For a directed graph with $n=6$ and adjacency lists of lengths $(2,0,3,1,0,2)$, construct CSR offsets, state the stored-arc count, and compare full list versus matrix neighbor probes.

### Exercise 2

Prove list traversal takes $O(n+m)$ under constant-time arc iteration and matrix traversal takes $O(n^2)$ when every reached row is scanned. State when the matrix bound does not imply slower wall time.

### Exercise 3

Diagnose a parallel BFS that infers vertices from edges, uses outgoing CSR for pull, marks visited after enqueue, reports logical $m$ as twice its directed arc count, and benchmarks only warm kernel time against a cold end-to-end competitor.

### Exercise 4

Choose vector adjacency, CSR plus transpose, bit matrix, or edge list for a mutable sparse service, static direction-optimizing BFS, dense Boolean reachability, and external-memory Kruskal preprocessing.

### Exercise 5

Design a reproducible traversal evaluation for untrusted graph uploads across sparse and dense regimes. Include semantic validation, datasets, machine/runtime metadata, measurements, cancellation, and the limits of conclusions.

## Answers to the Exercises

### Answer 1

Degrees prefix-sum to offsets $(0,2,2,5,6,6,8)$, so stored-arc count is eight. If all six vertices are reached, list traversal considers eight arcs plus vertex/queue work. A Boolean matrix scan considers $6\cdot6=36$ potential neighbors. If only a subset is reached, list probes sum reached out-degrees and matrix probes equal six times reached vertices.

### Answer 2

Each vertex is discovered at most once, contributing $O(n)$ state/queue work. List traversal iterates each stored directed arc from its tail once, and $\sum_v\deg^+(v)=m$, yielding $O(n+m)$. Matrix traversal scans $n$ cells for each of at most $n$ reached vertices, yielding $O(n^2)$.

Wall time also depends on density, compact cell width, sequential/vectorized access, pointer/object overhead, cache and bandwidth, conversion, and output. On a dense graph $m=\Theta(n^2)$, both bounds are quadratic; a matrix may be faster. The theorem does not name a universal crossover.

### Answer 3

Accept a complete vertex universe so isolates and counts survive. Pull needs incoming adjacency or a transpose, not outgoing-only CSR. Atomically mark or claim an unseen vertex before enqueue/callback. Define whether $m$ counts directed logical edges, undirected edges, or stored arcs; do not double an already directed count.

Report comparable end-to-end and kernel-only measurements for both systems, with equal cold/warm policies and conversion scope. Also pin index mapping and snapshot, record frontier/edge work and machine metadata, validate distances/reachability, and distinguish allowed parent nondeterminism.

### Answer 4

A mutable sparse service favors vector or hash-backed adjacency depending update, ordering, lookup, and descriptor-stability requirements. Static direction-optimizing BFS needs compact outgoing CSR plus incoming CSC/transpose and frontier bitsets. Dense Boolean reachability favors a bit matrix or GraphBLAS-like sparse/dense algebra when its semantics fit.

External-memory Kruskal preprocessing favors an edge list sorted by `(weight,tie_key)` with a separate complete vertex inventory; adjacency queries are unnecessary. Each choice must retain stable edge identity and property alignment.

### Answer 5

Validate quotas, complete vertices, stable edge IDs, endpoints, directedness, loops, multiplicity, property widths, and snapshot digest. Include empty, chain, hub-skewed, disconnected, mesh/road-like, random sparse, medium-density, and near-complete graphs, with named provenance and digests. Build list/CSR and matrix representations only where feasible; cross-check normalized edge multisets and BFS reachability/distances from isolate, hub, sink, and random stratified sources.

Record CPU/GPU, memory, cache/NUMA topology, OS, runtime/compiler and flags, threads/affinity, representation parameters, warm-up, cold/warm policy, trials, aggregation and variance. Measure parse/map/build/kernel/validation/output separately and end-to-end; record arcs and absent probes, frontier sizes, bytes/peak RSS, bandwidth/cache counters where reliable, atomic conflicts, and cancellation latency.

Bind checkpoints and outputs to the graph and index-map revision. Inject malformed offsets/endpoints, allocation failure, duplicate IDs, extreme degrees, cancellation at every boundary, and snapshot replacement. Publish only validated complete results or an explicit partial contract. Conclusions apply to the recorded graph population, environment, implementation, and confidence interval; they do not establish a universal sparse/dense threshold.
