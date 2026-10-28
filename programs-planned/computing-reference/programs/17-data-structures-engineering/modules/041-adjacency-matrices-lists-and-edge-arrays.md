---
module_id: DSE-041
program: Data Structures Engineering
level: 1
module_number: 41
title: Adjacency Matrices, Lists, and Edge Arrays
status: complete
last_verified: 2026-08-30
---

# Adjacency Matrices, Lists, and Edge Arrays

## One-Page Review

### Governing question

How should an engineer encode vertices, directedness, parallel edges, self-loops, properties, identity, and mutation in a matrix, adjacency collection, or edge array so graph algorithms receive exactly the semantics and costs they assume?

### Essential definitions

- A graph `G=(V,E)` contains vertices and edges; an edge may be directed or undirected and may carry identity/properties.
- A **simple graph** has no parallel edges and normally no self-loops; a **multigraph** permits multiple distinct edges between the same endpoints.
- An **adjacency matrix** stores a value for every ordered vertex pair, using `Theta(|V|^2)` cells.
- An **adjacency list** stores, for each vertex, its incident or outgoing edge references, using `Theta(|V|+|E|)` structural space under a sparse model.
- An **edge array/list** stores edge records contiguously and makes whole-edge scans natural; it does not by itself provide efficient neighbor lookup.
- An **edge ID/descriptor** identifies one logical edge independently of its endpoint pair.
- **out-degree** counts outgoing edge incidences; **in-degree** counts incoming incidences. In an undirected graph, a self-loop's degree contribution must be declared.
- **density** compares live edges with the number of possible endpoint pairs under the graph model.
- **structure of arrays (SoA)** stores sources, targets, and properties in separate arrays; **array of structures (AoS)** stores them together per edge.
- A **tombstone** marks a physically retained edge record logically absent until compaction.

### Central model, mechanism, or theorem

Representation follows the operations. A dense boolean/bit matrix provides constant-time adjacency testing and row scans of `Theta(|V|)`, whether or not a vertex has few neighbors. An adjacency list enumerates neighbors in `Theta(degree(v))`; membership is linear in degree unless neighbors are sorted, hashed, indexed, or bit-packed. An edge array scans all edges in `Theta(|E|)` and is ideal for edge-centric passes, sorting, batching, transfer, and construction.

Directedness and multiplicity change storage. A boolean matrix cannot distinguish two parallel edges; a count matrix can represent multiplicity but not individual properties without another table. An undirected adjacency list often stores two incidences per nonloop edge. Edge IDs connect adjacency indices to one canonical property record and make deletion of one parallel edge unambiguous.

### Critical invariants

1. Vertex identity/domain and whether isolated vertices exist independently of edges are explicit.
2. Directed/undirected, loop, parallel-edge, duplicate, and property-update policies are defined before layout.
3. Every live edge has valid endpoints and exactly the required outgoing/incoming/undirected incidences.
4. Matrix cells encode the declared boolean, multiplicity, weight, or semiring value without ambiguous zero/absence.
5. Edge IDs remain unique and their invalidation/generation rules survive swaps, compaction, and vertex deletion.
6. Degree, edge count, transpose/incoming index, offsets, and property columns agree with canonical live membership.
7. Iteration order and descriptor/iterator invalidation are API contracts, not incidental container behavior.
8. Publication, snapshot, persistence, and reclamation expose one coherent graph version to algorithms.

### Common failures

- Choosing a boolean matrix for a weighted multigraph and silently collapsing edges.
- Treating weight zero as “no edge.”
- Forgetting isolated vertices when importing an edge list.
- Counting one undirected edge twice as `|E|`, or storing it once but exposing only one endpoint's neighbors.
- Counting a directed self-loop incorrectly in in/out degree.
- Deleting endpoint pair `(u,v)` when only one parallel edge ID should be removed.
- Assuming adjacency iteration is sorted or stable after mutation.
- Storing only outgoing edges and then claiming constant-time predecessor traversal.
- Using big-O cell counts as actual byte counts while ignoring objects, capacities, IDs, and properties.
- Running an algorithm whose required graph interface the representation does not provide.

### Compact example

A directed five-vertex multigraph has seven edges, including two `0->1` edges and loop `1->1`. A multiplicity matrix records cells 2 and 1, six nonzero cells, and 25 total cells. Out lists and in lists each contain seven edge IDs; an edge-array scan finds three weights at most 3. Removing only edge `e1` changes multiplicity `0->1` from 2 to 1 and leaves the other parallel edge live.

### Connections

[DSE-005](005-contiguous-and-linked-layouts.md), [DSE-006](006-memory-locality-and-cache-behavior.md), and [DSE-012](012-dynamic-arrays-and-geometric-growth.md) supply layout/capacity models. [DSE-022](022-separate-chaining.md) through [DSE-030](030-engineering-a-memory-efficient-hash-map.md) supply hashed adjacency choices. The [program roadmap](../ROADMAP.md) continues with compressed sparse layouts, disjoint sets, graph traversal, connectivity, ordering, and shortest paths.

## Governing Question

Which graph model, identity scheme, query/update mix, density, property layout, iteration contract, lifetime rule, and hardware/storage target justify an adjacency matrix, adjacency list, edge array, or synchronized combination?

## Why This Matters

Graph algorithms are usually stated over mathematical sets, but programs operate over layouts. Breadth-first search needs outgoing neighbor enumeration. Bellman-Ford naturally scans edges. Floyd-Warshall and GraphBLAS-style algorithms map to matrices. Kruskal sorts an edge array. Reverse reachability needs incoming adjacency or a transpose. A representation that omits one required operation can change the whole algorithmic cost.

The graph model is equally important. Real systems contain self-loops, parallel connections, isolated entities, edge identity, timestamps, labels, capacities, and deletion history. A matrix cell, neighbor integer, or endpoint pair cannot represent all of these without conventions and auxiliary data. Import/export formats commonly lose isolated vertices, direction, duplicates, property types, or stable IDs.

Performance folklore such as “lists for sparse, matrices for dense” is a useful beginning, not an engineering decision. Bit matrices make adjacency and bulk intersections extraordinarily compact/fast for bounded dense domains. Hash-heavy adjacency lists may use far more memory than their asymptotic label suggests. Contiguous edge arrays stream well and parallelize even when lookup is poor. Mutability, descriptor stability, NUMA/GPU movement, snapshot requirements, and algorithm mix determine the right design.

## Prerequisites and Retrieval

Retrieve representation invariants from [DSE-002](002-representation-invariants.md), cost and byte accounting from [DSE-004](004-time-space-and-allocation-cost.md), and locality/layout trade-offs from [DSE-005](005-contiguous-and-linked-layouts.md) and [DSE-006](006-memory-locality-and-cache-behavior.md). Retrieve generic descriptors/comparators from [DSE-007](007-genericity-and-type-constraints.md), property/model tests from [DSE-009](009-property-based-testing-of-data-structures.md), and workload benchmarking from [DSE-010](010-benchmarking-a-structure-without-misleading-results.md). Retrieve arrays and growth from [DSE-011](011-fixed-arrays.md) and [DSE-012](012-dynamic-arrays-and-geometric-growth.md), plus hash-table choices from [DSE-023](023-linear-probing.md) and [DSE-028](028-resizing-and-incremental-rehashing.md).

## Learning Objectives

After completing this module, you should be able to:

1. define directed/undirected, simple/multi, loop, isolated-vertex, and property semantics;
2. derive matrix, adjacency-list, and edge-array storage/costs for required operations;
3. preserve edge identity and distinguish one-edge deletion from endpoint-pair deletion;
4. account correctly for directed/undirected incidences, loops, degrees, and edge count;
5. choose nested vector, linked, sorted, hashed, bitset, AoS, or SoA sublayouts;
6. design conversions that preserve vertices, direction, multiplicity, properties, and ordering metadata;
7. specify mutation, descriptor invalidation, tombstone/compaction, snapshot, and concurrency behavior;
8. explain current Boost Graph, NetworkX, GraphBLAS, and benchmark-suite contracts accurately;
9. validate synchronized matrix/list/edge views against one canonical live-edge model;
10. benchmark memory, lookup, traversal, scan, mutation, conversion, and tail behavior for real graph distributions.

## Core Exposition

**Begin with the graph model, not the container.** Define a vertex universe. Dense integer IDs `0..n)` enable direct indexing; sparse external IDs require a mapping to dense internal IDs or hash/ordered containers. Decide whether deleting a vertex renumbers later IDs. Isolated vertices must be represented separately from edges or they disappear from edge-only input.

For a directed graph, an edge has ordered endpoints `(source,target)`. For an undirected graph, endpoint order is not semantic, though storage may choose a canonical pair. A self-loop has identical endpoints. A multigraph assigns identity to each edge so two edges with the same endpoints remain distinct. Edge properties may include weight, capacity, label, timestamp, provenance, or application state.

State duplicate insertion behavior. A simple graph may reject an existing pair, replace its property, combine weights, or report “already present.” A multigraph normally allocates a new edge ID. State deletion: by edge ID removes one edge; by endpoint pair may remove one, all, or a selected property match. These are different operations and should not share an ambiguous name.

**Matrices encode endpoint products.** Number vertices `0..n)`. An adjacency matrix has cell `A[u,v]`. For a directed boolean graph, `A[u,v]=true` iff an edge exists. An undirected simple graph has symmetric `A`; implementations may store the full matrix or one triangle. A diagonal cell represents a loop.

Boolean matrices collapse parallel edges. A multiplicity matrix stores the number of live edges per ordered pair. A weight matrix can store one weight but needs an absence representation distinct from every legal weight. Zero is often a valid weight, so zero cannot implicitly mean absence unless the domain forbids it. Use a presence bitmap plus values, an option/tag, infinity under a proved algorithmic convention, or sparse tuples.

Multiple parallel weights do not fit one scalar cell without aggregation. `min` may be sufficient for some shortest-path algorithms but loses edge identity and other weights. A cell can point to a collection, but then the representation is a matrix of adjacency buckets with different costs. Explain the abstraction honestly.

A dense matrix allocates `n^2` cells for directed graphs. Bit-packing needs roughly `n^2/8` bytes plus alignment; byte booleans need about `n^2`; 64-bit weights need about `8n^2` before metadata. Check `n*n`, bit rounding, and byte multiplication for overflow. At `n=100,000`, even a bit matrix requires about 1.25 GB, while 64-bit cells require 80 GB.

Adjacency testing is constant-time indexing. Adding/removing an existing-domain simple edge is constant-time cell update. Enumerating outgoing neighbors scans a row in `Theta(n)` unless auxiliary bit operations enumerate set bits. Dense bitset row intersections can process a machine word at once and support common-neighbor/count operations effectively. Matrix transpose is conceptual index reversal but physical access/locality depends on row/column layout.

Vertex insertion into a contiguous `n x n` matrix may require reallocating/repacking `Theta(n^2)` cells. Fixed bounded vertex domains avoid this. Blocked/tiled matrices improve cache, SIMD, GPU, or distributed partitioning. Sparse matrices are compressed adjacency layouts and belong to the next module; do not call a hash-of-hash adjacency list a dense matrix merely because the API exposes `A[u,v]`.

**Adjacency lists organize incidences by vertex.** Maintain a vertex table and, for each vertex, a collection of outgoing neighbor or edge references. A directed out-adjacency list enumerates successors in `Theta(out_degree(u))`. To enumerate predecessors efficiently, also store in-adjacency or build/compute a transpose. Doubling indices increases writes/space and creates a cross-view invariant.

For an undirected edge `{u,v}` with `u!=v`, store one edge record and normally two incidences: one in `u`'s adjacency and one in `v`'s. `|E|` counts the logical edge once; the sum of undirected degrees is `2|E|` when a loop contributes two incidences under the standard convention. Some APIs expose a loop once in neighbor iteration but degree two; state the representation/API relationship.

For a directed self-loop `u->u`, store one logical edge. It contributes one to out-degree and one to in-degree. If the same edge ID appears in both out and in collections, that is two index entries referencing one record, not two edges. Maintaining separate live-edge count prevents incidence count from being mistaken for `|E|`.

An adjacency entry may be only a neighbor vertex, `(neighbor,property)`, `(neighbor,edge_id)`, or a pointer to a canonical edge record. Neighbor-only storage is compact for simple unweighted graphs but makes parallel identity and shared properties difficult. Canonical edge records plus IDs simplify multigraphs and property ownership, at an indirection cost.

**The per-vertex container changes the complexity.** An unsorted vector gives fast append and contiguous iteration; edge existence/removal by neighbor is `O(degree)`, while swap-delete changes order. A sorted vector gives binary-search membership `O(log degree)` but insertion/deletion shifts entries. A linked list offers stable nodes and constant splice after location, but locating remains linear and locality is poor.

A hash set/map gives expected constant membership and removal, higher memory, unordered iteration, hash-flooding considerations, and resizing pauses. An ordered tree gives logarithmic worst-case membership and sorted neighbors with pointer overhead. A bitset gives constant membership and word-parallel scans for dense bounded neighbor universes, paying `Theta(n)` bits per vertex. Hybrid containers can switch representation by degree, but conversion/hysteresis and iterator semantics become part of the contract.

Adjacency lists use `Theta(n+m)` logical entries for a directed out-only graph with `m` edges. Directed out+in uses about `2m` index entries. Undirected usually uses `2m` incidences. Actual bytes include vertex objects, empty-container headers, capacity slack, allocator metadata, neighbor/ID width, property pointers, hashes, and alignment. Millions of zero-degree vertices can make nested container headers dominate.

Flattened arrays of per-vertex vectors reduce allocation overhead but mutation may relocate segments. Chunked adjacency allocates fixed-size blocks per high-degree vertex. Small-vector optimization keeps a few neighbors inline. Degree-skewed graphs need special care: one hub can dominate allocation and parallel work despite sparse global density.

**Edge arrays make edges primary.** Store records `(source,target,properties,id)` contiguously. Appending is amortized constant time; scanning every edge is linear and cache-friendly. Sorting by source, destination, weight, time, or ID supports different algorithms and conversions. Structure-of-arrays makes reading only sources/targets/weights more bandwidth-efficient and vectorizable; array-of-structures simplifies per-edge access.

An edge array does not directly enumerate one vertex's neighbors without scanning all edges. Build offsets or adjacency indices, sort/group by source, or maintain auxiliary maps. Once source-sorted with offsets, it becomes compressed sparse row, the next module. An unsorted edge array alone implements an edge-list graph interface, sufficient for edge-centric algorithms such as Bellman-Ford or Kruskal but not ordinary efficient BFS.

Edge deletion can swap with the last record, shift, leave a tombstone, or mark a bitmap. Swap-delete invalidates indices/changes order and requires every adjacency reference to be repaired. Stable edge IDs need an indirection table/generation rather than raw array positions. Tombstones preserve positions but inflate scans and memory until compaction; track live/physical counts and bound the ratio.

Batch ingestion naturally begins as edge arrays. Validate endpoints/properties, preserve isolated vertices separately, assign IDs, then sort/deduplicate/aggregate/build target layout. External sorting handles graphs beyond memory. Provenance may require retaining original input order and source row even after canonical sorting.

**Combinations are often correct.** A dynamic multigraph may keep canonical edge records in a slab/array, outgoing and incoming lists of IDs, plus a hash index from endpoint pair to a small ID set. A dense graph may keep a bit matrix for membership and edge arrays for properties. Each extra view accelerates an operation but multiplies mutation and recovery obligations.

Choose one canonical membership authority or define a transaction across all views. On insertion, allocate/validate the edge record, then update out, in, matrix/hash, degree, and count with rollback or publish at one version. On deletion, logical marking can make the edge absent before physical index cleanup. Validators rebuild every derived view from canonical live records and compare exactly.

Eventual asynchronous derived indices may be appropriate in analytics, but algorithms must name the snapshot/version they consume. “Matrix says present while list says absent” cannot be silently tolerated in a structure advertised as one linearizable graph.

**Directedness affects transpose and algorithms.** Out-only adjacency supports reachability from sources. Strong components, reverse BFS, dominators, and some pull-style parallel algorithms need predecessors. Building transpose costs `Theta(n+m)` and memory. Keeping both orientations doubles adjacency indexing but can reduce repeated queries.

An undirected API can store symmetric directed arcs, shared edge IDs with two incidences, or canonical endpoints plus per-vertex references. Symmetric arcs risk treating one logical edge as two in edge scans. Shared IDs require neighbor computation based on which endpoint is current. Canonical-only endpoint storage makes one vertex's adjacency incomplete unless another index exists.

Converting directed to undirected needs policy: retain parallel opposite arcs as separate undirected edges, collapse by endpoint pair, combine weights, or reject conflicts. Converting a multigraph to simple loses information unless an aggregation is explicit. Never hide this behind a convenience cast in a correctness-sensitive path.

**Edge identity and vertex identity are lifecycle contracts.** Dense vertex index is excellent for arrays and algorithm workspaces. If vertex deletion compacts the table, all later indices change and every edge/workspace/external reference must update. Stable opaque vertex IDs can map through generations to dense slots. Some libraries deliberately invalidate descriptors on vector-backed deletion and offer list-backed choices for stability.

Edge descriptors similarly may be a pair, array index, pointer, or opaque token. An endpoint pair cannot identify one parallel edge. A pointer can be invalidated by reallocation/deletion. An array index can refer to a different edge after compaction. Generation-tagged slots or never-moving node records preserve identity at a cost.

Document iterator order and invalidation. Vector insertion may invalidate per-vertex iterators; hash resize changes bucket iteration; edge sort changes global order; vertex compaction invalidates descriptors. Deterministic algorithms/tests may require sorted neighbors, but sorting changes build/mutation cost. Reproducible output should request a canonical order rather than rely on allocation history.

**Boost Graph exposes interface requirements and storage choices.** Its adjacency list is parameterized by vertex/out-edge containers and directedness, affecting parallel edges, mutation, descriptor stability, and incoming access. Its adjacency matrix fixes vertex count and fits dense graphs. Its edge-list adaptor provides edge iteration, source, and target but not vertex/adjacency/incidence interfaces; algorithms requiring BFS-style neighbors cannot use it directly.

This concept-based design captures a durable lesson: algorithms should declare the graph operations they require. A type may model EdgeListGraph without modeling AdjacencyGraph. Static typing can reject a mismatch; dynamic systems need explicit capability checks or adapters with documented construction cost.

**NetworkX prioritizes flexible semantics.** Its `Graph` supports undirected edges and self-loops but not parallel edges; `MultiGraph`/`MultiDiGraph` add edge keys for parallel identity. Nodes may be arbitrary hashable objects and properties are dictionaries. This is excellent for exploratory/application graphs but carries Python object/hash/dict overhead far beyond a compact C++/CSR layout. Converting formats must select the right graph class or duplicates/direction can be lost.

**GraphBLAS makes matrix meaning algebraic.** A sparse/dense matrix represents adjacency values, and graph operations use user-selected semirings, masks, and sparse linear algebra. “Zero” can mean the additive identity/absent stored entry under one algebra, while an explicitly stored zero may still have semantic presence depending on the API. Matrix dimensions, types, duplicate tuple assembly, transpose, and operators are part of the graph meaning.

This generality avoids hard-wiring BFS or shortest paths to numeric arithmetic. It also means ordinary adjacency-matrix intuition is insufficient: select, reduce, multiply, masking, and sparsity formats operate under the chosen algebra. Cite the exact GraphBLAS version when interoperating.

**Memory and locality need concrete arithmetic.** For `n` vertices and `m` directed edges, a bit matrix costs `n^2` bits. An adjacency ID array with `n+1` offsets and `m` 32-bit destinations costs roughly `4(n+1+m)` bytes before properties—the CSR case—provided counts fit. A nested vector layout adds `n` headers and capacity slack. A hash adjacency may consume several words per edge.

Edge AoS `(u32,u32,f64,u64)` may pad to 24 or 32 bytes; SoA consumes 4+4+8+8=24 logical bytes per edge and lets a topology-only pass read eight rather than all columns. Measure actual `sizeof`, allocator committed/resident bytes, and peak construction memory. Conversion may temporarily hold input, sort buffers, offsets, and output simultaneously.

Neighbor traversal of adjacency vectors follows contiguous entries but then may access random vertex properties. Reordering vertices can improve locality but changes ID mappings. Matrices stream rows; bitsets exploit word/SIMD operations. Edge arrays partition by contiguous ranges for parallel scans, though destination property updates can contend.

**Concurrency depends on mutation granularity.** A read-only graph is easiest: publish an immutable snapshot and run algorithms with stable descriptors. Copy-on-write/versioned graphs replace changed blocks/lists and reclaim old versions after readers finish. This often outperforms intricate fine-grained mutation for analytic workloads.

Mutable adjacency vectors need locks or ownership per vertex; undirected insertion touches two vertices and must lock in canonical vertex order to avoid deadlock. Directed out+in insertion touches source and target. Global edge arrays/counters/ID registries add more synchronization. A transaction must not expose one incidence without the other when the abstract operation is atomic.

Lock-free adjacency is possible but needs immutable records, CAS publication, logical deletion, ABA defense, and safe reclamation. Range/neighbor iteration may be weakly consistent or snapshot-based. Atomic degree counters can disagree transiently unless their semantics are relaxed. State the linearization point and which derived metrics are exact.

Parallel graph algorithms need partitioning. High-degree hubs cause load imbalance; matrices partition by tiles, edge arrays by edge ranges, and adjacency lists by vertices or edge-balanced ranges. False sharing on frontiers/visited/degree accumulators can dominate. NUMA placement and GPU transfer favor contiguous compressed formats, motivating the next module.

**Persistence and interchange need schemas.** An edge-list text file with two columns cannot preserve isolated vertices, direction metadata, edge IDs, parallel-edge distinction beyond repeated lines, property types, or comparator/vertex mapping. Include a header/schema and vertex table. Define endianness, widths, nulls, encoding, checksums, and version.

On-disk matrices need dimension and cell semantics. Sparse formats need sortedness, duplicate, and offset invariants. Persisting raw pointers/container internals is invalid. Recovery can replay logical edge operations or load a validated immutable snapshot. Check endpoints before allocation, counts before multiplication, and cumulative offsets for monotonicity/overflow.

Malformed graphs can request huge `n^2`, contain out-of-range endpoints, duplicate IDs, inconsistent symmetric arcs, NaN weights, cycles in linked adjacency, or property lengths differing from edge count. Parse into bounded staging, validate, then publish. Do not trust claimed counts for allocation without limits.

**Testing begins with a canonical edge multiset.** Use a reference model keyed by stable edge ID with endpoint/property records plus a separate vertex set. From it recompute out/in incidences, matrix multiplicities, degrees, nonzero cells, and edge counts. After every operation, compare every derived representation.

Exhaust tiny directed/undirected simple/multigraph combinations with zero vertices, isolated vertices, loops, parallel/opposite edges, zero/negative/NaN/extreme weights, and every deletion form. For undirected graphs verify symmetry, incidence count, loop degree policy, and one canonical edge enumeration. For multigraphs delete one ID and retain its siblings.

Conversion round trips must preserve the declared information, not byte layout. Matrix-to-edge conversion cannot recover identities/properties that were never encoded; the test should reject a “lossless” claim. Randomly permute insertion/storage order and confirm algorithms requiring no order return invariant results; separately test canonical deterministic order.

Fault injection targets vertex/edge/property allocation and each derived-view update. Check strong/basic guarantees. Concurrency testing forces partial cross-view interleavings and validates linearizability/snapshot semantics. Persistence fuzzing mutates counts, dimensions, offsets, IDs, symmetry, checksums, and schema versions.

Benchmarks report `n`, `m`, directedness, loop/parallel rates, density, degree distribution/skew, component structure, property bytes, update/lookup/traversal/edge-scan/range mix, and ordering. Measure build/conversion/peak memory, bytes per live edge/vertex, adjacency latency by degree, whole scan bandwidth, p50/tails, mutation, compaction, and parallel scaling. GAP and related suites help standardize algorithm workloads, but representation microbenchmarks still need direct evidence.

The executable below maintains one directed multigraph in three synchronized views: canonical edge records, outgoing/incoming edge-ID lists, and a multiplicity matrix. It includes a loop and parallel edges, shows degrees and edge-centric filtering, deletes exactly one parallel edge by ID, and rebuilds all derived facts during validation. It does not establish fixed-width/allocation/failure safety, undirected semantics, descriptor generations, iterator stability, concurrency, persistence, or production performance.

<!-- bijux-verify: {"id":"graph-representation-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"vertices=5\nlive_edges=7\nmatrix_0_1=2\nmatrix_1_1=1\nout_1=e2:1,e3:2\nin_1=e0:0,e1:0,e2:1\nweight_at_most_3=e2,e3,e5\nout_degrees=2,2,2,1,0\nin_degrees=1,3,1,1,1\nmatrix_nonzero_cells=6\nmatrix_slots=25\nerased_parallel_e1=True\nmatrix_0_1_after=1\nlive_edges_after=6\ninvariant=True\nevidence=finite_graph_representation_trace\n","stderr":""}} -->
```python
from dataclasses import dataclass


@dataclass
class Edge:
    source: int
    target: int
    weight: int
    alive: bool = True


class DirectedMultiGraph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.edges = []
        self.out_edges = [[] for _ in range(vertices)]
        self.in_edges = [[] for _ in range(vertices)]
        self.multiplicity = [[0] * vertices for _ in range(vertices)]
        self.live_edges = 0

    def add_edge(self, source, target, weight):
        if not (0 <= source < self.vertices and 0 <= target < self.vertices):
            raise IndexError("vertex out of range")
        edge_id = len(self.edges)
        self.edges.append(Edge(source, target, weight))
        self.out_edges[source].append(edge_id)
        self.in_edges[target].append(edge_id)
        self.multiplicity[source][target] += 1
        self.live_edges += 1
        return edge_id

    def erase_edge(self, edge_id):
        edge = self.edges[edge_id]
        if not edge.alive:
            return False
        edge.alive = False
        self.out_edges[edge.source] = [
            item for item in self.out_edges[edge.source] if item != edge_id
        ]
        self.in_edges[edge.target] = [
            item for item in self.in_edges[edge.target] if item != edge_id
        ]
        self.multiplicity[edge.source][edge.target] -= 1
        self.live_edges -= 1
        return True

    def validate(self):
        alive = {index for index, edge in enumerate(self.edges) if edge.alive}
        if len(alive) != self.live_edges:
            return False
        seen_out = set()
        seen_in = set()
        rebuilt = [[0] * self.vertices for _ in range(self.vertices)]
        for vertex in range(self.vertices):
            for edge_id in self.out_edges[vertex]:
                edge = self.edges[edge_id]
                if edge_id not in alive or edge.source != vertex:
                    return False
                seen_out.add(edge_id)
                rebuilt[edge.source][edge.target] += 1
            for edge_id in self.in_edges[vertex]:
                edge = self.edges[edge_id]
                if edge_id not in alive or edge.target != vertex:
                    return False
                seen_in.add(edge_id)
        return seen_out == alive == seen_in and rebuilt == self.multiplicity


graph = DirectedMultiGraph(5)
for source, target, weight in [
    (0, 1, 5), (0, 1, 7), (1, 1, 2), (1, 2, 3),
    (2, 0, 4), (2, 3, 1), (3, 4, 6),
]:
    graph.add_edge(source, target, weight)
print(f"vertices={graph.vertices}")
print(f"live_edges={graph.live_edges}")
print(f"matrix_0_1={graph.multiplicity[0][1]}")
print(f"matrix_1_1={graph.multiplicity[1][1]}")
print("out_1=" + ",".join(
    f"e{edge_id}:{graph.edges[edge_id].target}"
    for edge_id in graph.out_edges[1]
))
print("in_1=" + ",".join(
    f"e{edge_id}:{graph.edges[edge_id].source}"
    for edge_id in graph.in_edges[1]
))
print("weight_at_most_3=" + ",".join(
    f"e{edge_id}" for edge_id, edge in enumerate(graph.edges)
    if edge.alive and edge.weight <= 3
))
print("out_degrees=" + ",".join(str(len(items)) for items in graph.out_edges))
print("in_degrees=" + ",".join(str(len(items)) for items in graph.in_edges))
print(f"matrix_nonzero_cells={sum(value != 0 for row in graph.multiplicity for value in row)}")
print(f"matrix_slots={graph.vertices * graph.vertices}")
print(f"erased_parallel_e1={graph.erase_edge(1)}")
print(f"matrix_0_1_after={graph.multiplicity[0][1]}")
print(f"live_edges_after={graph.live_edges}")
print(f"invariant={graph.validate()}")
print("evidence=finite_graph_representation_trace")
```

## Definitions and Notation

- `G=(V,E)`: graph with vertex set `V` and logical edge set/multiset `E`.
- `n=|V|`, `m=|E|`: vertex and logical live-edge counts.
- `(u,v)`: directed edge from `u` to `v`; `{u,v}`: undirected edge.
- **self-loop**: edge whose endpoints are the same vertex.
- **parallel edges**: distinct edge IDs with equal endpoint pair.
- `A[u,v]`: matrix cell under declared presence/multiplicity/value semantics.
- `out_degree(v)`, `in_degree(v)`: outgoing/incoming incidence counts.
- **incidence**: one endpoint-to-edge relationship stored in an adjacency index.
- **descriptor**: representation-specific vertex or edge reference.
- **AoS/SoA**: array-of-structures/structure-of-arrays property layout.
- **canonical membership**: authoritative live edge records from which derived indices can be rebuilt.
- **density**: `m` divided by possible edge pairs under the declared directed/loop/simple model.
- **tombstone/compaction**: logical absence with retained slot/later physical rewrite.

## Mechanisms, Invariants, or Proof Structure

Matrix correctness maps every legal vertex pair to a cell whose presence/multiplicity/property algebra is explicit. Adjacency correctness maps every canonical live edge to the required out/in/undirected incidences and no others. Edge-array correctness maps every live ID to one valid endpoint/property record, with physical/tombstone state distinguished.

Cost derives from access path: a dense row has `n` cells; a per-vertex collection has degree-sized iteration plus its container's lookup/update cost; an edge array has `m` contiguous records and no implicit vertex index. Directedness, loops, multiplicity, and properties determine whether one logical edge creates one or two adjacency index entries and whether a matrix cell is sufficient.

Combined representations require a transaction or version across canonical record, out/in indices, matrix/hash membership, degrees, count, and lifetime registry. Independent rebuild validators detect drift. Concurrency and persistence add publication, snapshot, invalidation, reclamation, and recovery proofs that cannot be inferred from local container validity.

## Alternatives and Trade-Offs

| Representation | Best fit | Main obligation |
|---|---|---|
| Dense boolean/bit matrix | dense/bounded adjacency and bit operations | quadratic domain storage, no parallel identity |
| Dense value matrix | dense algebraic weights | absence versus zero and one value per cell |
| Vector adjacency | sparse traversal, fast build/scan | linear neighbor lookup/removal, invalidation |
| Sorted adjacency | membership plus deterministic neighbors | shifting/update and sort maintenance |
| Hashed adjacency | dynamic membership/removal | hash memory/order/adversarial behavior |
| Tree adjacency | ordered dynamic neighbors | pointer/rebalance overhead |
| Edge array AoS | edge-centric scans/sorts | poor neighbor lookup without index |
| Edge SoA | column-specific/vectorized scans | correlated mutation and row identity |
| Canonical edges plus ID indices | multigraph identity/properties | cross-view transaction and indirection |
| Out+in adjacency | fast successors and predecessors | doubled index writes/space |
| Immutable snapshot/CSR | analytics, transfer, traversal | rebuild/batching for mutation |
| Hybrid degree-adaptive graph | skewed mixed workload | switching thresholds and complex semantics |

## Failure Modes and Misconceptions

- **“An edge is an endpoint pair.”** Not in a multigraph; identity distinguishes parallel records.
- **“Zero means no edge.”** Zero may be a valid weight or algebraic value.
- **“Edge-list input defines all vertices.”** Isolated vertices require a separate vertex declaration.
- **“Undirected storage has exactly m adjacency entries.”** Common layouts store two incidences per nonloop edge.
- **“A loop always contributes degree one.”** Standard undirected degree often counts two; directed in/out each count one.
- **“Adjacency list means linked list.”** Per-vertex vectors, hashes, trees, bitsets, and chunks are all possible.
- **“Membership is O(1) in an adjacency list.”** It depends on the per-vertex container.
- **“A matrix supports multigraphs.”** Boolean/value cells collapse identities unless multiplicity/collections are added.
- **“Edge arrays support BFS efficiently.”** Not without a neighbor index or repeated full scans.
- **“Descriptor is a stable ID.”** It may be an invalidated index, iterator, or pointer.
- **“Iteration order is harmless.”** Reproducibility and tie-sensitive algorithms may observe it.
- **“O(n+m) predicts bytes.”** empty headers, capacities, hashes, IDs, properties, and allocator overhead matter.
- **“Two derived indices will stay consistent.”** every mutation/failure/recovery path must update them transactionally.
- **“Atomic edge publication makes the graph thread-safe.”** multiple incidences, counts, versions, and reclamation remain.
- **“Format conversion is lossless.”** direction, isolated vertices, duplicates, IDs, types, and ordering may be dropped.

## Worked Examples

### Example 1

A five-vertex graph file lists only edge `0->1`. Inferring vertices from endpoints yields two vertices and loses isolated 2, 3, and 4. Conclusion: vertex domain is independent metadata.

### Example 2

Two parallel edges `0->1` have weights 5 and 7. A boolean matrix stores only true; a weight matrix stores at most one value; a count matrix stores 2 but neither weight. Conclusion: full multigraph properties require edge records or cell collections.

### Example 3

Directed loop `1->1` appears once in the edge table, once in out[1], and once in in[1]. It adds one to each degree but remains one logical edge. Conclusion: incidences and edge count are distinct.

### Example 4

An undirected nonloop edge `{2,3}` is one canonical record and two adjacency IDs. Summing adjacency lengths counts two. Conclusion: derive `m` from canonical records or divide only under a loop-aware invariant.

### Example 5

A sparse vertex has degree 3 in a million-vertex graph. Matrix neighbor enumeration scans one million cells; vector adjacency reads three entries. Conclusion: constant membership does not imply efficient sparse traversal.

### Example 6

A hub has one million unsorted vector neighbors. Append/scan are efficient, but one membership query is linear. A hash index adds memory but changes membership to expected constant time. Conclusion: degree distribution and operation mix select the subcontainer.

### Example 7

Kruskal needs every edge sorted by weight but no repeated neighbor lookup. A contiguous edge array supports one scan/sort directly. Conclusion: edge-list capability can be sufficient and more natural than adjacency.

### Example 8

Swap-deleting edge-array position 4 moves edge 99 into that slot while adjacency lists still store 99's old index. Conclusion: raw positions are not stable edge IDs; repair every reference or use indirection/generations.

### Example 9

One thread publishes `out[u]` before `in[v]`; a simultaneous reverse traversal misses the new edge. Conclusion: if edge insertion is one atomic graph operation, all required views need one publication/version protocol.

### Example 10

A benchmark graph has average degree 8 but one vertex has half the edges. Equal vertex partitioning leaves one worker overloaded. Conclusion: report degree skew and use edge-balanced/hub-aware partitioning, not density alone.

## Cross-Program Connections

- **Algorithm engineering:** BFS/DFS, Bellman-Ford, Floyd-Warshall, Kruskal, SCC, and GraphBLAS each require different graph capabilities.
- **Programming languages:** generic graph concepts, descriptor types, iterator invalidation, option/absence, and property ownership define safe APIs.
- **Concurrent programming:** multi-vertex locking, snapshots, versioning, logical deletion, atomics, and reclamation govern mutable graphs.
- **Database engineering:** entity/relationship identity, secondary adjacency indices, MVCC, WAL, schema, and query access paths mirror graph layouts.
- **Data engineering:** edge ingestion, deduplication, partitioning, sorting, columnar properties, conversion, and skew dominate pipelines.
- **Computer architecture:** matrices/bitsets/edge arrays stream; nested hashed adjacency adds pointer/cache/TLB overhead; GPUs favor compact batches.
- **Security engineering:** allocation overflow, malformed endpoints/IDs, hash flooding, output-heavy neighborhoods, and property parsing need limits.
- **Distributed systems:** vertex cuts, edge cuts, ghosts, ownership, consistency, and communication depend on chosen local representation.

## References

1. Boost C++ Libraries, [Graph Concepts](https://www.boost.org/doc/libs/latest/libs/graph/doc/html/graph/concepts/graph_concepts.html). Current official graph, incidence, bidirectional, vertex-list, edge-list, adjacency-matrix, mutation, and property capability contracts.
2. Boost C++ Libraries, [Graph Data Structures](https://www.boost.org/doc/libs/latest/libs/graph/doc/html/graph/graph_classes/overview.html). Current official mutability, memory, edge lookup, neighbor iteration, density, and descriptor guidance.
3. Boost C++ Libraries, [`adjacency_list`](https://www.boost.org/doc/libs/latest/libs/graph/doc/html/graph/graph_classes/adjacency_list.html). Current official directedness, parallel-edge, storage-selector, mutation, descriptor, and iterator-invalidation contracts.
4. Boost C++ Libraries, [`edge_list`](https://www.boost.org/doc/libs/latest/libs/graph/doc/html/graph/adaptors/edge_list.html). Current official minimal edge-iteration interface and algorithm-capability boundary.
5. NetworkX Project, [`Graph`](https://networkx.org/documentation/stable/reference/classes/graph.html) and graph class contracts. Current official node, edge, loop, parallel-edge, property, adjacency, and conversion semantics.
6. NetworkX Project, [Tutorial: Graphs, DiGraphs, MultiGraphs, and Conversion](https://networkx.org/documentation/stable/tutorial.html). Current official multigraph edge-key and semantic-conversion guidance.
7. GraphBLAS Forum, [GraphBLAS C API Specification 2.1.0](https://graphblas.org/docs/GraphBLAS_API_C_v2.1.0.pdf). Current official matrix, sparse tuple, type, operator, monoid/semiring, mask, and graph-algebra contract.
8. Redis Project, [`src/t_zset.c`](https://github.com/redis/redis/blob/unstable/src/t_zset.c). Current primary source illustrating canonical member lookup plus ordered adjacency-like index, composite identity, and synchronized views.
9. Scott Beamer, Krste Asanović, and David Patterson, [The GAP Benchmark Suite](https://arxiv.org/pdf/1508.03619), 2015/2017. Primary source for reproducible graph algorithm workloads, graph inputs, verification, and reporting.
10. Laxman Dhulipala, Guy E. Blelloch, and Julian Shun, [The Graph Based Benchmark Suite](https://www.cs.cmu.edu/~guyb/papers/3398682.3399168.pdf), 2020. Primary source for graph representation/processing interfaces, compressed layouts, and parallel benchmark methodology.

## Exercises

### Exercise 1

Specify representations for directed and undirected multigraphs with loops, isolated vertices, stable edge IDs, and properties. Derive edge/incidence/degree invariants.

### Exercise 2

For several `n,m`, key/property sizes, and degree distributions, derive logical operations and approximate bytes for bit matrix, nested vector adjacency, hashed adjacency, and AoS/SoA edge arrays. Identify overflow checks.

### Exercise 3

Design loss-aware conversions among an external edge stream, multiplicity/value matrix, adjacency-ID lists, and edge array. State exactly which conversions can be lossless.

### Exercise 4

Choose representations for dynamic route planning, a static GraphBLAS analytics service, and a transactional social multigraph. Define capability interfaces and benchmarks.

### Exercise 5

Design a concurrent versioned multigraph maintaining canonical edge records plus out/in indices. Specify publication, deletion, snapshots, IDs, failure rollback, reclamation, persistence, and validation.

## Answers to the Exercises

### Answer 1

Keep an explicit vertex registry including isolated vertices and canonical live edge records `(id,u,v,properties,generation)`. Directed layout indexes each edge ID once in out[u] and once in in[v]; a loop is still one edge and contributes one to each degree. Undirected layout indexes a nonloop edge in both endpoint adjacency collections; define a loop as two degree incidences or the chosen alternative and implement it consistently. Stable edge IDs are opaque slot+generation tokens, never endpoint pairs or movable positions. Invariants require valid endpoints, unique live IDs, exact registry/live count, exact required incidences with no extras/duplicates, symmetric reachability for undirected edges, degree values recomputed from incidences under loop policy, and property ownership matching canonical records. Deleting one ID leaves parallel siblings; endpoint-pair deletion is a separately named bulk operation.

### Answer 2

A directed bit matrix uses `ceil(n^2/8)` data bytes and scans `n` bits per neighbor query; check `n*n` and rounding overflow. A 64-bit value matrix uses about `8n^2` plus presence semantics. Nested vectors use about `n*header_bytes + capacity_entries*entry_bytes`, where capacity exceeds `m` and out+in or undirected indexing can double entries. Hashed adjacency adds bucket/control arrays, load slack, hash/key/value/alignment and may use several words per incidence. Edge AoS uses `m*sizeof(record)` including padding; SoA approximates the sum of each column width times physical capacity and lets topology-only scans omit properties. Include vertex table, IDs, generations, tombstones, allocator metadata, build buffers, and peak conversion coexistence. Degree skew affects capacity fragmentation and cache even at equal `n,m`. Check edge/incidence counts, `2m`, capacity growth, byte multiplication, cumulative offsets, and matrix products against addressable limits.

### Answer 3

Parse a schema-declared stream with separate vertex records, direction, edge IDs, property types, and duplicate policy into bounded canonical staging. From canonical edges, build multiplicity matrix by incrementing cells and adjacency-ID lists by adding required out/in or undirected incidences; retain the edge array for identity/properties. Conversion to a boolean matrix loses multiplicity and identity; to a scalar value matrix loses parallel properties unless an explicit aggregation is declared. A count matrix preserves endpoint multiplicity but not individual IDs/properties. Neighbor-only adjacency loses parallel identity unless repeated entries plus aligned records are preserved. Edge-only export loses isolated vertices unless a vertex table/header accompanies it. Directed-to-undirected and multigraph-to-simple require a conflict/aggregation policy and are information-losing generally. A round trip is “lossless” only when the target encodes every source semantic field or the source domain is restricted so omitted distinctions cannot occur.

### Answer 4

Dynamic route planning needs weighted directed successors and often predecessors plus updates: use stable canonical edge records with vector/hash adjacency depending lookup/update mix, or a dynamic graph library; sorted/compact snapshots can serve route queries. Static GraphBLAS analytics uses a typed sparse adjacency matrix under explicit semirings/masks, often both orientations or cheap transpose views, built from validated tuples. A transactional social multigraph needs stable vertex/edge IDs, parallel relationship types, properties, out/in secondary indices, MVCC versions, and WAL—typically canonical records plus indexed adjacency rather than one cell. Define algorithm capability interfaces such as vertex iteration, edge iteration, out/in incidence, adjacency test, stable IDs, properties, and snapshot version. Benchmark real `n,m`, skew, direction, loops/parallels, properties, updates, lookups, range/neighbor scans, conversions, memory/peak build, p50/tails, concurrent scaling, recovery, and algorithm outputs under identical semantics.

### Answer 5

Use immutable or versioned canonical edge records addressed by generation IDs, versioned per-vertex out/in index roots or segments, and a global commit sequence. Prepare record and both index changes privately; after all fallible allocation/validation succeeds, publish one commit descriptor/version that snapshots interpret atomically. Deletion publishes a tombstone/end-version before later physical cleanup; IDs cannot be reused until generation advances and old snapshots cannot confuse reuse. Readers pin a snapshot epoch and traverse only records visible at that version. Writers lock vertices in canonical ID order or use transactional CAS with validation; out/in changes and degree/count deltas commit together. Rollback discards unpublished allocations. Epoch/reference reclamation waits for old snapshots; shutdown drains pins. WAL logs logical commit intent/data before acknowledgment, recovery replays committed versions and rebuilds/validates indices. Test parallel loops/edges, vertex deletion, stale IDs, allocation failure at every preparation point, source/target lock races, insert/delete/read interleavings, crash at log/publication boundaries, compaction with old snapshots, malformed logs, counter overflow, and full canonical-to-derived rebuild equality.
