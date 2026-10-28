---
module_id: DSE-042
program: Data Structures Engineering
level: 1
module_number: 42
title: Compressed Sparse Graph Layouts
status: complete
last_verified: 2026-08-30
---

# Compressed Sparse Graph Layouts

## One-Page Review

### Governing question

How can a sparse graph be encoded as compact offset, endpoint, and property arrays while preserving exact edge semantics, predictable traversal, efficient construction, and a defensible mutation and persistence contract?

### Essential definitions

- **compressed sparse row (CSR)** groups directed edges by source: `offset[u]..offset[u+1]` indexes the destination and property arrays for vertex `u`.
- **compressed sparse column (CSC)** groups directed edges by destination and therefore supports predecessor traversal; it is CSR for the transpose graph.
- **coordinate format (COO)** stores one source, destination, and property tuple per edge and is convenient for ingestion, sorting, and redistribution.
- A **row pointer/offset array** has `|V|+1` entries, begins at zero, is nondecreasing, and ends at the number of stored edge entries.
- An **edge slot** is an aligned position across endpoint and property arrays; it is not necessarily a stable logical edge ID.
- **canonical order** is the declared ordering within each row or column, commonly endpoint then stable edge identity.
- A **duplicate** is another stored edge with the same endpoint pair; whether duplicates remain distinct or are combined is a graph-model decision.
- A **structural zero** is an absent matrix entry; it must not be confused with a stored edge whose numeric property equals zero.
- A **transpose** reverses every directed edge; in layout terms it converts source-grouped traversal into destination-grouped traversal.
- A **delta overlay** is a mutable insertion/deletion layer consulted with an immutable compressed base until compaction rebuilds a new base.

### Central model, mechanism, or theorem

For `n=|V|` and `m` stored directed edge entries, CSR uses an offset array of length `n+1`, a destination array of length `m`, and zero or more aligned property arrays of length `m`. Out-neighbors of `u` occupy the half-open slice `[offset[u],offset[u+1])`, so enumeration takes `Theta(out_degree(u))` and a whole traversal takes `Theta(n+m)`. Direct adjacency lookup is linear in a row unless canonical sorting permits binary search or another index is added.

Construction from COO is a histogram-plus-prefix-sum problem. Count entries per source, exclusive-scan counts into offsets, scatter every edge into its source interval, and optionally sort within intervals. The prefix sum proves that intervals are disjoint, cover exactly `m` slots, and have the requested capacities. CSC follows by grouping on destination, or by transposing CSR in `Theta(n+m)` work with additional arrays.

The compression removes per-vertex container objects and per-edge pointers, improving locality and transfer. It does not compress arbitrary vertex IDs, guarantee stable edge descriptors, or make mutation cheap. Inserting one edge into canonical packed arrays can shift `Theta(m)` entries; production designs rebuild in batches, leave capacity/gaps, partition into blocks, or merge a delta overlay.

### Critical invariants

1. The vertex domain and mapping from external IDs to dense indices `0..n-1` are explicit and versioned.
2. `offset` has length `n+1`, `offset[0]=0`, is nondecreasing, and `offset[n]=m`.
3. Every destination/source index is within the vertex domain, and every edge property array has exactly `m` aligned entries.
4. Each edge appears in the interval for its declared source in CSR and destination in CSC; empty and isolated vertices have equal adjacent offsets.
5. Directedness, self-loop, parallel-edge, duplicate-combination, and zero/absence semantics are preserved during conversion.
6. Any promised within-row ordering and uniqueness property is validated, not inferred from the format name.
7. CSR, CSC, edge IDs, transpose indices, degrees, and properties describe the same logical graph version.
8. Integer widths and prefix sums cannot overflow at supported `n`, `m`, byte sizes, or partition boundaries.
9. Publication and persistence expose complete immutable snapshots or a specified base-plus-delta view, never partially built arrays.

### Common failures

- Allocating `n` offsets instead of `n+1`, or forgetting the terminal sentinel `m`.
- Losing vertices with zero degree when inferring `n` only from observed edge endpoints.
- Confusing CSR row number with an external vertex ID.
- Assuming rows are sorted, deduplicated, or duplicate-free merely because data is CSR.
- Combining parallel edges by numeric addition when edge identity requires them to remain distinct.
- Dropping a zero-weight edge as if it were absent.
- Reordering destinations without applying the identical permutation to weights and edge IDs.
- Exposing array positions as stable descriptors across sort, insertion, deletion, compaction, or reload.
- Keeping only CSR while claiming efficient incoming traversal.
- Using 32-bit offsets for a graph or byte calculation that can exceed the representable range.

### Compact example

A directed graph over vertices `0..5` has eight stored edges, including two parallel `0->2` edges, loop `1->1`, and no outgoing edges from vertex 3. Its CSR offsets are `0,3,4,6,6,7,8`; the equal entries around row 3 encode an empty row without losing the vertex. Its CSC offsets are `0,1,3,6,7,8,8`, exposing that vertex 5 has no incoming edges. Aligned weights support a finite sparse matrix-vector product while keeping the parallel edges distinct.

### Connections

[DSE-005](005-contiguous-and-linked-layouts.md), [DSE-006](006-memory-locality-and-cache-behavior.md), and [DSE-011](011-fixed-arrays.md) supply contiguous layout and cache models. [DSE-041](041-adjacency-matrices-lists-and-edge-arrays.md) defines the graph semantics being compressed. The [program roadmap](../ROADMAP.md) continues with disjoint sets, graph traversal, connectivity, ordering, shortest paths, and graph storage systems whose behavior depends on these layout contracts.

## Governing Question

Which graph semantics, traversal direction, ordering requirement, property model, construction pipeline, mutability rate, integer width, and hardware or storage target justify CSR, CSC, COO, a blocked derivative, or synchronized compressed views?

## Why This Matters

Sparse graphs are common precisely where a dense `n`-by-`n` representation is impossible. A web graph with billions of potential vertices cannot reserve a cell for every pair. Yet a conventional adjacency list built from vectors, objects, pointers, hashes, and allocator metadata may still spend more bytes on representation than on endpoints. It may also scatter traversal across memory, underutilize cache lines, and be expensive to transfer to an accelerator or map from storage.

Compressed sparse layouts replace many small containers with a few dense arrays. Offsets encode all row boundaries; endpoints and properties stream contiguously. The representation serves graph traversal, sparse linear algebra, graph analytics, serialization, and interchange. It is used because its constants and access pattern matter, not because it changes the asymptotic `Theta(n+m)` storage bound of a well-designed adjacency list.

Compression creates obligations. A packed slot is easy to move and therefore is a poor stable identity. A graph with parallel edges cannot casually “sum duplicates” during conversion. Zero weights may be meaningful. Empty rows must remain represented. Incoming algorithms need CSC or a transpose. Dynamic updates conflict with sorted packed arrays. Parallel construction must make prefix sums, scatter ownership, and property permutations race-free. Persistent and untrusted inputs require stronger validation than a pointer-rich in-memory structure often receives.

This module treats CSR/CSC as engineered contracts, not three arrays that happen to pass one traversal. The goal is to derive representation, construction, query, update, parallel, persistence, security, and evidence decisions from one declared logical graph.

## Prerequisites and Retrieval

Retrieve representation invariants from [DSE-002](002-representation-invariants.md), operation and failure contracts from [DSE-003](003-operation-contracts.md), asymptotic and byte costs from [DSE-004](004-time-space-and-allocation-cost.md), and locality from [DSE-005](005-contiguous-and-linked-layouts.md) and [DSE-006](006-memory-locality-and-cache-behavior.md). Retrieve property testing from [DSE-009](009-property-based-testing-of-data-structures.md) and measurement discipline from [DSE-010](010-benchmarking-a-structure-without-misleading-results.md). [DSE-041](041-adjacency-matrices-lists-and-edge-arrays.md) supplies directedness, loops, multiplicity, properties, edge identity, and synchronized-view foundations.

## Learning Objectives

After completing this module, you should be able to:

1. state and validate CSR, CSC, and COO representation invariants;
2. derive `Theta(n+m)` traversal and storage costs while also calculating concrete bytes;
3. build CSR from edge records using counting, prefix sums, scattering, and optional canonical sorting;
4. preserve parallel edges, self-loops, zero properties, isolated vertices, and stable logical edge IDs;
5. construct and validate CSC as a transpose view of the same logical graph;
6. distinguish slot identity from durable edge identity and describe invalidation precisely;
7. select mutable overlays, slack, blocking, or rebuilds according to an update workload;
8. reason about parallel/GPU construction, NUMA placement, integer widths, and load balance;
9. design versioned persistent formats and validate hostile inputs safely; and
10. build differential, metamorphic, failure-injection, and benchmark evidence for compressed layouts.

## Core Exposition

**Begin with the logical graph, not the arrays.** Declare whether edges are directed, whether loops and parallel edges are legal, whether an external edge ID is stable, and how properties attach. Declare the full vertex set separately from the observed endpoints. A file containing only `(source,destination)` pairs cannot express an isolated vertex; either a header supplies `n`, a vertex table supplies membership, or the importer receives a separate domain.

Map external vertex keys to dense integer indices when the domain is not already `0..n-1`. This remapping is not incidental preprocessing. It is a versioned dictionary that controls reproducibility, joins with external properties, partitioning, and interpretation after reload. Sorting external IDs gives deterministic indices but costs work and may expose a chosen ordering; first-seen assignment streams cheaply but depends on input order. Persist the mapping or a reproducible recipe.

For a directed graph, CSR stores outgoing incidences. Let `row_offsets` contain `n+1` integers. For vertex `u`, its edge slots are the half-open interval

`I(u) = [row_offsets[u], row_offsets[u+1])`.

The destination at slot `p` is `column_indices[p]`. A weight, timestamp, edge ID, label reference, or other fixed-width property is stored at the same `p` in an aligned array. Variable-length values normally use an offset/length into a separate byte arena so the primary scan stays compact.

The half-open convention eliminates special cases. Degree is `row_offsets[u+1]-row_offsets[u]`. An empty row has equal boundaries. Vertex `n-1` uses the terminal `row_offsets[n]`; omitting this sentinel forces another stored edge-count branch and invites an out-of-bounds read. A zero-edge graph has `n+1` zero offsets and empty endpoint/property arrays.

With `m` edge slots, structural space is `(n+1)*w_o + m*w_v` bytes before properties, alignment, headers, and mapping tables, where `w_o` is offset width and `w_v` is vertex-index width. If both are 64-bit, structure costs `8(n+1+m)` bytes. If `n<2^32` but `m` may exceed that, 32-bit destinations and 64-bit offsets are valid and often save substantial memory. Width selection must follow the largest representable value for each field, not a single fashionable integer type.

Enumeration of one row is proportional to its stored degree; enumeration of every vertex and edge is `Theta(n+m)`. Testing whether `(u,v)` exists scans `degree(u)` destinations unless rows are sorted, in which case binary search costs `O(log degree(u))`. Hash or bitmap auxiliaries may improve membership for selected high-degree vertices. Their construction, bytes, and invalidation belong in the contract.

Sorting rows yields deterministic traversal, binary-search membership, merge/intersection operations, and better delta merging. It does not follow from CSR itself. Some APIs accept unsorted indices and expose flags such as “sorted” or “canonical.” A validation routine must check the actual monotonic property before setting such metadata. Sorting destinations requires applying exactly the same permutation to every property and edge-ID array.

Parallel edges force a secondary order. Sorting only by destination groups duplicates but leaves their order unspecified. Sort by `(destination,edge_id)` for deterministic distinct edges, or by `(destination,input_sequence)` if stable ingestion order is contractual. If the mathematical object is a sparse matrix rather than a multigraph, a library may combine duplicates under addition or another operator. That is safe only if the caller explicitly selects the operator and it matches property semantics. Summing capacities may be meaningful; summing timestamps or security labels is not.

Structural absence and numeric zero are different. A stored zero-weight edge remains an edge and contributes a slot. Sparse algebra may prune explicit zeros for efficiency, but graph conversion must not do so unless the graph model declares zero equivalent to absence. NaN, infinity, signed zero, overflow, and nonassociative floating reduction also affect duplicate combining and reproducibility.

**Build from COO by counting and scanning.** COO records `(source,destination,properties...)` in arbitrary or partially ordered input. First validate or remap endpoints, decide the duplicate policy, and perform checked counting. Create `counts[n]`, increment `counts[source]` per accepted record, then compute an exclusive prefix sum:

`offset[0]=0` and `offset[u+1]=offset[u]+counts[u]`.

Before each addition, prove the result fits the chosen offset type and allocation size. At completion, `offset[n]=m`. Because prefix sums are nondecreasing, the intervals are ordered and disjoint; because their lengths sum to `m`, they cover every slot exactly once.

Copy `offset[0:n]` into `cursor`. For each COO record, reserve slot `p=cursor[source]`, increment that cursor, and write destination plus every property into slot `p`. After scatter, `cursor[u]` must equal `offset[u+1]`. This last equality is a powerful independent assertion: it detects missed, duplicated, misclassified, and overrun records.

Sequential scatter preserves input order within a row when records are processed in order. Parallel scatter with atomic fetch-add generally does not. Deterministic parallel construction can count per partition, prefix-sum a two-dimensional histogram, and give each partition a private subrange of every row; a final per-row sort can canonicalize regardless of scatter order. The histogram itself may be too large for `threads*n`, so blocked vertex ranges or radix sorting may be preferable.

An alternative is to sort COO globally by `(source,destination,edge_id)`, then identify row boundaries in one scan. Comparison sort costs `O(m log m)`; radix/counting methods exploit bounded integer keys. Sorting can simultaneously canonicalize, group duplicates, and improve bulk I/O. Histogram scatter can be `Theta(n+m)` but still needs row sorting when canonical destination order matters. Choose from measured input order, widths, memory budget, parallelism, and duplicate policy.

Construction needs failure semantics. Validate counts and allocation sizes before publishing. Build all arrays in private temporary ownership; if mapping, allocation, sorting, or property conversion fails, discard them and leave the previous graph unchanged. Publish one immutable snapshot only after all invariants pass. Writing directly into a live object exposes partial offsets or uninitialized properties to readers and makes rollback difficult.

**CSC is CSR grouped by destination.** CSC's `column_offsets[v]..column_offsets[v+1]` contains source vertices of edges entering `v`. It supports predecessor traversal, reverse reachability, pull-based graph algorithms, and column-oriented sparse algebra. Given a CSR, count each destination, prefix-sum counts, and scatter each `(u,v)` into column `v` while carrying properties and logical IDs. This is a sparse transpose in `Theta(n+m)` work and `Theta(n+m)` additional space.

When both directions are stored, edge correspondence must be explicit. Keeping the same logical edge ID in CSR and CSC is robust. Alternatively, store cross-position maps `csr_to_csc[p]` and `csc_to_csr[q]`; these make property lookup and deletion faster but add `2m` indices and must be rebuilt on either reordering. Duplicates make endpoint-only matching ambiguous. A stable ID or deterministic occurrence rank resolves the bijection.

Validate transpose metamorphically. Every CSR slot `(u,v,id,property)` must have exactly one corresponding CSC slot in column `v` with source `u`, the same ID, and the same property. Degree sums must both equal `m`. Transposing twice must recover the original logical multiset, although physical slot order may differ unless canonical ordering is declared.

Undirected graphs have two common encodings. Store both directed incidences so every vertex row enumerates all neighbors; a nonloop logical edge consumes two slots and a loop convention consumes one or two. Or store one canonical triangle, such as `min(u,v),max(u,v)`, saving space but requiring algorithms to inspect both row and column directions or use specialized symmetric kernels. APIs must distinguish logical edges from stored incidences when reporting `m`, degree, and memory.

**Slot positions are not durable descriptors.** Insertion, deletion, sorting, duplicate reduction, compaction, width conversion, and transpose reconstruction can move every later slot. Returning `p` as a permanent edge handle is safe only for an immutable snapshot whose lifetime bounds the handle. For mutable or persistent identity, store a stable edge ID in an aligned column and maintain an optional ID-to-current-slot index. Include snapshot generation in borrowed descriptors so a slot from one version cannot address another silently.

Deletion from immutable CSR creates a new representation. A batch filter can count retained edges per row, scan the counts, and copy retained aligned records in `Theta(n+m)`. A bitset tombstone avoids immediate movement but traversal must test it, degree metadata becomes logical rather than physical, and space accumulates. Tombstones need a compaction threshold and cannot be confused with absent property values.

Single-edge insertion into a flat canonical CSR may shift `Theta(m)` endpoints and properties and adjust all later offsets. Workloads with many updates commonly use an immutable base plus per-vertex or global delta. Queries merge base insertions, delta insertions, and deletion markers under a snapshot/version rule. A compaction builds a replacement base and atomically publishes it. The design is an LSM-like trade: updates become cheap, while reads pay merge/deduplication cost and temporary memory can approach old base plus delta plus new base.

Other dynamic variants reserve gaps, use per-row capacity, group vertices into blocks/pages, store chunks linked by indexes, or maintain high-degree rows separately. These weaken perfect packing to reduce shifts. State whether iteration remains sorted, how many fragments a row may touch, and when rebuilding occurs. Calling all such formats “CSR” without qualifiers hides important query and invalidation behavior.

**Blocked formats target machines and degree distributions.** SELL-C-sigma, ELLPACK, blocked CSR, tiled edge arrays, and hybrid formats reorganize slots for SIMD, GPU coalescing, cache tiles, or matrix blocks. Padding a set of similarly sized rows makes fixed-width parallel lanes efficient but wastes slots for skewed degrees. Reordering vertices by degree improves padding and load balance but changes the external-to-dense mapping and may harm application locality.

Graph workloads differ from regular sparse matrices. Power-law-like graphs can contain a few enormous rows and many tiny rows. Assigning one thread per row causes severe imbalance. Partition by edge ranges, split high-degree rows, use dynamic scheduling, or combine push and pull traversals. Edge-balanced partitions may begin inside a row, so algorithms that produce one row result need segmented reduction or atomic combination.

GPU formats also require host/device transfer and ownership rules. Device libraries document accepted base indexing, sortedness, duplicate behavior, property types, and temporary workspaces; follow those contracts rather than assuming all CSR is interchangeable. A benchmark that excludes conversion and transfer answers only a steady-state question. Include those costs when the application rebuilds or moves the graph frequently.

NUMA systems need first-touch or explicit placement. A single global CSR streams well for readers local to its pages but may cause remote accesses for other sockets. Partitioned CSR duplicates boundary metadata and sometimes ghost vertices while improving locality. Partition quality, mapping, cut edges, load balance, and reconstruction become part of the representation evidence.

**Sparse algebra gives a precise execution model.** Interpret adjacency as a sparse matrix `A`. A row-oriented product computes outputs from outgoing edges; transpose or CSC supports reverse direction. GraphBLAS generalizes scalar addition and multiplication to a semiring and uses masks and accumulators. The format must preserve structural membership separately from values because algorithms often use the pattern of `A`, not only nonzero arithmetic values.

For a weighted outgoing CSR, `y[u]=sum_{p in I(u)} weight[p]*x[destination[p]]` is a sparse matrix-vector product under ordinary arithmetic. Replace the operators to express reachability, shortest-path relaxations, or other graph computations, subject to their algebraic assumptions. Duplicate entries are reduced according to an operator; parallel ordering matters if that operator is not associative and commutative. Numerical reproducibility may require a defined reduction tree or stronger arithmetic.

Graph frameworks such as Ligra and GBBS separate graph layout from vertex-subset/frontier processing. Direction-optimizing algorithms switch between sparse push and dense pull according to frontier and graph state. Keeping both outgoing and incoming compressed views costs memory but can avoid repeated transpose construction and enable the switch. Measure total algorithm suites, not one favorable kernel.

**Persistence turns arrays into a format contract.** A durable image needs magic bytes, schema version, byte order, integer widths, directedness, logical/stored edge-count interpretation, flags for sortedness/duplicates/properties, mapping identity, array offsets and lengths, and integrity protection. Absolute process pointers do not belong on disk. Use checked file-relative offsets and ensure alignment only after range checks.

Memory mapping can make startup fast and share clean pages, but mapped bytes remain untrusted until validated. Verify that every region lies within the file without overflow or overlap, `n+1` offsets are available, offsets are nondecreasing and at most `m`, the terminal equals `m`, endpoints are below `n`, property regions contain `m` elements, and declared canonical properties actually hold. Bound `n`, `m`, allocations, sorting, and diagnostic output before trusting header values.

Checksums detect corruption, not semantic compatibility or malicious construction. Authenticate inputs when provenance matters. A checksum over all immutable arrays plus header prevents unnoticed bit changes but does not prove that rows contain the correct business graph. Record build source, transformation version, and mapping digest for reproducibility. For crash-safe replacement, write and validate a new immutable file, durably publish a manifest/reference, then retire the old version after readers release it.

Endian conversion and width narrowing require elementwise validation. A 64-bit file offset cannot be cast to 32 bits because the current test graph is small. Reject unsupported widths or explicitly convert after checking every value. Floating properties need a declared encoding and NaN policy. Variable-length arenas need independently validated offsets that cannot point into headers or other fields.

**Concurrency is simplest through immutability.** Many readers can traverse a published CSR snapshot without locks if arrays and referenced properties never mutate and object lifetime is protected. Build a replacement privately, publish its pointer with release semantics, and reclaim the prior snapshot through reference counting, epochs/RCU, or another documented scheme. Atomic pointer publication does not itself protect a reader that loaded the old pointer.

Mutable property columns can be separated from immutable structure, but then readers need a consistency model. Atomic per-edge values give individual updates, not a coherent multi-edge snapshot. Copy-on-write property versions, transactional logs, or epoch-tagged columns provide stronger views at higher cost. Cross-view CSR/CSC updates must not expose different logical graph versions.

Parallel traversal must control output races. Read-only neighbor enumeration is safe, but marking a shared visited bit, relaxing a destination, or accumulating a row/column result needs atomics, ownership, reduction, or frontier deduplication. False sharing in visited/frontier arrays and contention on high-degree destinations can dominate the neat sequential layout.

**Security failures often begin in arithmetic.** An attacker-controlled `n` or `m` can overflow `(n+1)*width`, allocate a small buffer, and cause scatter writes beyond it. Use checked add/multiply before allocation and before converting between integer types. Counting a malicious number of duplicate edges can overflow a row counter. Prefix sums must detect overflow before wrapping to a plausible nondecreasing sequence.

Endpoint validation must precede indexing `counts[source]`. Negative signed values cast to unsigned become enormous. Untrusted sortedness flags can make binary search return false answers. Crafted offsets can overlap rows, point backward, or exceed the endpoint array. Property offsets can alias regions. Validate inexpensive header/range facts first, then linear invariants, then optional expensive canonical sorting and duplicate checks under resource limits.

Decompression and diagnostics can amplify. Do not allocate a dense `n*n` matrix to “validate” sparse input. Limit duplicate reports, row dumps, and error strings. Avoid invoking user comparators or decoders inside privileged unchecked loops. Fuzz parsers and builders with sanitizers and allocation failures.

**Evidence should compare logical graphs, not just bytes.** A reference multiset keyed by stable edge ID can preserve loops, duplicates, and properties. Generate vertices and operation-free snapshots, build CSR/CSC through independent paths, enumerate them back into records, and compare the logical multiset. Check every invariant separately rather than relying on one round trip that may repeat the same bug.

Exhaust tiny domains: `n=0`, vertices without edges, one loop, one edge, all-empty rows, first/last row, parallel equal endpoints, zero properties, and every permutation of a small edge set. Include maximum valid IDs, one-past IDs, offset-width boundaries, count overflow, allocation failure, comparator failure, and malformed persistent regions. Verify that failure leaves the old snapshot unchanged and no partially initialized object escapes.

Metamorphic relations add strength. COO permutation must not change a canonical logical result. Transpose twice preserves the edge multiset. CSR degree sum equals `m`; CSC degree sum equals `m`. Filtering then rebuilding equals rebuilding then filtering under the same predicate. Concatenating independently built vertex partitions and remapping should match one global build when cross-partition policy is accounted for. Sparse matrix-vector results should match a simple edge-record reference for many semirings where operations meet required laws.

Benchmarks report construction and steady-state separately. Vary `n`, `m`, degree skew, isolated fraction, loop/duplicate rate, property width, sortedness, input ordering, integer widths, and graph partition. Measure bytes resident and allocated, build throughput, peak temporary memory, row enumeration, membership, transpose, whole scans, SpMV/BFS-like kernels, delta merge, compaction, serialization, and reload. Record machine, compiler/runtime, allocator, page state, NUMA/GPU placement, and whether mapping/transfer is included.

The executable below constructs CSR and CSC independently from one finite directed multigraph. It validates offsets, ranges, aligned properties, sorted rows, stable IDs, and the exact transpose correspondence. It also demonstrates empty rows, a loop, parallel edges, neighbor/predecessor traversal, and a weighted sparse matrix-vector product. It does not establish performance, integer-width safety at scale, parallel determinism, device behavior, crash consistency, or universal correctness.

<!-- bijux-verify: {"id":"compressed-sparse-layout-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"vertices=6\nedges=8\ncsr_offsets=0,3,4,6,6,7,8\ncsr_columns=1,2,2,1,0,3,2,4\ncsc_offsets=0,1,3,6,7,8,8\ncsc_rows=2,0,1,0,0,4,2,5\nout_0=1:e0,2:e1,2:e2\nin_2=0:e1,0:e2,4:e6\nout_degrees=3,1,2,0,1,1\nin_degrees=1,2,3,1,1,0\nspmv=37,6,8,0,18,40\nparallel_0_2=2\nloop_1_1=True\ntranspose_consistent=True\ninvariant=True\nevidence=finite_compressed_sparse_layout_trace\n","stderr":""}} -->
```python
edges = [
    (0, 1, 5, "e0"),
    (0, 2, 2, "e1"),
    (0, 2, 7, "e2"),
    (1, 1, 3, "e3"),
    (2, 0, 4, "e4"),
    (2, 3, 1, "e5"),
    (4, 2, 6, "e6"),
    (5, 4, 8, "e7"),
]
n = 6


def compress(records, group_index, endpoint_index):
    ordered = sorted(records, key=lambda edge: (edge[group_index], edge[endpoint_index], edge[3]))
    counts = [0] * n
    for edge in ordered:
        counts[edge[group_index]] += 1
    offsets = [0]
    for count in counts:
        offsets.append(offsets[-1] + count)
    endpoints = [edge[endpoint_index] for edge in ordered]
    weights = [edge[2] for edge in ordered]
    ids = [edge[3] for edge in ordered]
    return offsets, endpoints, weights, ids


csr_o, csr_v, csr_w, csr_id = compress(edges, 0, 1)
csc_o, csc_u, csc_w, csc_id = compress(edges, 1, 0)


def valid(offsets, endpoints, weights, ids):
    return (
        len(offsets) == n + 1
        and offsets[0] == 0
        and offsets[-1] == len(edges)
        and all(a <= b for a, b in zip(offsets, offsets[1:]))
        and len(endpoints) == len(weights) == len(ids) == len(edges)
        and all(0 <= vertex < n for vertex in endpoints)
        and all(endpoints[offsets[u]:offsets[u + 1]] == sorted(endpoints[offsets[u]:offsets[u + 1]]) for u in range(n))
    )


csr_records = {
    (u, csr_v[p], csr_w[p], csr_id[p])
    for u in range(n)
    for p in range(csr_o[u], csr_o[u + 1])
}
csc_records = {
    (csc_u[p], v, csc_w[p], csc_id[p])
    for v in range(n)
    for p in range(csc_o[v], csc_o[v + 1])
}
x = [1, 2, 3, 4, 5, 6]
y = [sum(csr_w[p] * x[csr_v[p]] for p in range(csr_o[u], csr_o[u + 1])) for u in range(n)]
out_zero = [f"{csr_v[p]}:{csr_id[p]}" for p in range(csr_o[0], csr_o[1])]
in_two = [f"{csc_u[p]}:{csc_id[p]}" for p in range(csc_o[2], csc_o[3])]
invariant = valid(csr_o, csr_v, csr_w, csr_id) and valid(csc_o, csc_u, csc_w, csc_id)

print(f"vertices={n}")
print(f"edges={len(edges)}")
print("csr_offsets=" + ",".join(map(str, csr_o)))
print("csr_columns=" + ",".join(map(str, csr_v)))
print("csc_offsets=" + ",".join(map(str, csc_o)))
print("csc_rows=" + ",".join(map(str, csc_u)))
print("out_0=" + ",".join(out_zero))
print("in_2=" + ",".join(in_two))
print("out_degrees=" + ",".join(str(csr_o[u + 1] - csr_o[u]) for u in range(n)))
print("in_degrees=" + ",".join(str(csc_o[v + 1] - csc_o[v]) for v in range(n)))
print("spmv=" + ",".join(map(str, y)))
print(f"parallel_0_2={sum(1 for u, v, _, _ in edges if (u, v) == (0, 2))}")
print(f"loop_1_1={any(u == v == 1 for u, v, _, _ in edges)}")
print(f"transpose_consistent={csr_records == csc_records}")
print(f"invariant={invariant}")
print("evidence=finite_compressed_sparse_layout_trace")
```

## Definitions and Notation

Let `G=(V,E)` be a directed multigraph with `n=|V|` dense vertex indices and `m=|E|` stored directed edge records. CSR arrays are `O` (offsets), `D` (destinations), and aligned property columns `P_k`. Vertex `u` owns slots `[O[u],O[u+1])`. CSC arrays are `C` (column offsets), `S` (sources), and aligned properties, where vertex `v` owns incoming slots `[C[v],C[v+1])`.

`degree+(u)=O[u+1]-O[u]` and `degree-(v)=C[v+1]-C[v]`. COO is a collection or sequence of edge tuples before grouping. **Canonical CSR** in this module means valid CSR whose rows are sorted by `(destination,stable_edge_id)`; it does not mean duplicates are removed. A **snapshot generation** identifies one immutable physical layout. A **logical edge ID** survives reordering when the product contract requires it; a **slot** is only a physical index within one generation.

## Mechanisms, Invariants, or Proof Structure

The construction proof has four layers. First, endpoint validation ensures every count access is in range. Second, checked counts and exclusive prefix sums establish `O[0]=0`, monotonicity, and `O[n]=m`. Third, one reservation per accepted edge plus final cursor equality proves every slot is initialized exactly once in its source interval. Fourth, aligned scatter/sort permutations prove endpoint, property, and edge-ID columns remain attached.

CSR query correctness follows from the interval invariant: exactly the edges whose source is `u` occupy `I(u)`. CSC transpose correctness is a bijection by stable ID between `(u,v,p,id)` in CSR and `(u,v,p,id)` reconstructed from column `v`. Complexity claims require stating whether rows are sorted, whether lookup includes duplicate enumeration, and whether construction, mapping, transfer, or delta merging is included.

## Alternatives and Trade-Offs

| Layout | Natural operation | Principal advantage | Principal cost |
|---|---|---|---|
| COO edge arrays | ingest, sort, redistribute, edge scan | simplest records and parallel partitioning | neighbor queries require grouping/indexing |
| CSR | outgoing traversal, row kernels | compact contiguous rows | packed mutation and incoming traversal |
| CSC | predecessor traversal, column kernels | compact contiguous columns | outgoing traversal without another view |
| CSR plus CSC | bidirectional algorithms | both directions and push/pull | near-duplicate structure and synchronization |
| sorted CSR | membership, intersections, deterministic output | binary search and merge operations | construction/sort cost |
| base plus delta | read-mostly dynamic graph | cheap batches and immutable snapshots | query merging and compaction amplification |
| blocked/hybrid sparse format | SIMD/GPU/NUMA kernels | locality and load control | padding, remapping, format specialization |
| pointer/vector adjacency | frequent local mutation | independent per-vertex growth | allocation overhead and weaker streaming |

There is no universally best compressed format. Select against algorithm suite, mutation and snapshot rates, degree distribution, property width, stable-ID needs, construction frequency, platform, and persistence boundary. Retain COO as governed input or rebuild material when repeated alternate layouts are expected.

## Failure Modes and Misconceptions

- “Sparse” does not guarantee CSR is smaller: for extremely tiny `m` relative to a huge explicit `n`, `n+1` offsets dominate; segmented or key-addressed rows may be better.
- CSR does not imply sorted, unique, zero-free, one-based, or zero-based indices. Those are separate metadata and invariants.
- `m` may mean logical undirected edges, directed incidences, or physical slots. Name and serialize the distinction.
- A prefix sum can be monotone after integer wrap in an unsuitable representation; checked arithmetic is mandatory.
- Stable row order under sequential scatter does not imply deterministic parallel scatter.
- Binary search finds an endpoint occurrence, not necessarily every parallel edge or a specific logical edge.
- Keeping CSR and CSC without a snapshot rule can return mutually inconsistent answers during updates.
- Memory mapping does not validate a file and does not make random access free; page faults and hostile offsets remain.
- GPU throughput measured after conversion and transfer cannot justify the format for a rebuild-heavy application.
- A finite SpMV result validates one implementation trace, not the algebraic laws or production-scale behavior.

## Worked Examples

### Example 1

For row counts `[3,1,2,0,1,1]`, exclusive scanning gives `[0,3,4,6,6,7,8]`. The repeated `6` is not corruption: it proves row 3 owns the empty interval `[6,6)`. The terminal 8 independently states the physical edge count.

### Example 2

With 10 million vertices and 100 million edges, 64-bit offsets plus 32-bit destinations consume about `8*(10,000,001)+4*100,000,000`, roughly 480 MB before properties and alignment. Using 64-bit destinations adds another 400 MB. Concrete widths can matter more than container-level asymptotics.

### Example 3

Two records `(0,2,weight=2,id=e1)` and `(0,2,weight=7,id=e2)` are parallel graph edges. Canonical sorting retains both in `(destination,id)` order. Reducing them to weight 9 changes the object into a matrix entry and destroys edge-specific identity.

### Example 4

An explicit zero-weight edge `(4,5,0)` occupies a slot and appears in neighbor traversal. Removing it because sparse numeric libraries often eliminate zeros changes reachability. Structural pattern and numeric value must be independent.

### Example 5

To produce CSC, count CSR destinations, scan the counts, then scatter source and every aligned property into destination intervals. A stable edge ID lets a validator pair duplicate `0->2` entries exactly; endpoint pairs alone cannot tell which weight belongs to which logical edge.

### Example 6

A single insertion into the first row of flat CSR may shift all `m` destination/property values and increment `n` later offsets. Adding it to a sorted delta costs local work; a read merges the base row with delta records until compaction publishes a rebuilt snapshot.

### Example 7

An undirected nonloop `{2,7}` stored as incidences `2->7` and `7->2` uses two CSR slots but represents one logical edge. A loop convention might store one slot while contributing two to mathematical degree. Reporting only “edges=…” is ambiguous without the convention.

### Example 8

If row 0 destinations are sorted but weights are not permuted with them, topology tests can pass while SpMV silently uses weights for the wrong edges. Treat all aligned columns as one logical record during scatter, sort, filter, and compaction.

### Example 9

A file claims `n=2^63` and four-byte destinations. Computing `(n+1)*8` in signed 64-bit arithmetic overflows before allocation. A safe loader checks addition, multiplication, conversion to address size, file bounds, and configured resource limits before mapping array views.

### Example 10

A graph with one million small rows and one row holding half the edges defeats one-thread-per-row scheduling. Splitting the heavy row across edge ranges balances work, but its output then needs a segmented or atomic reduction. Layout and scheduler are one performance design.

## Cross-Program Connections

- **Algorithms:** BFS, PageRank, triangle counting, connectivity, and sparse shortest-path implementations derive work and load balance from row/column access.
- **Database engineering:** CSR resembles offset/index structures, immutable segments, columnar property storage, compaction, and snapshot publication.
- **Data engineering:** COO-to-CSR construction is group-by, histogram, prefix-sum, partition, sort, and aligned-column transformation at scale.
- **Concurrent and parallel programming:** scans, scatter ownership, work partitioning, atomics, snapshot publication, and safe reclamation determine correctness.
- **Computer architecture:** cache lines, vector lanes, memory bandwidth, NUMA pages, device transfer, and integer widths shape real performance.
- **Security engineering:** checked arithmetic, hostile format validation, authenticated provenance, and bounded diagnostics protect loaders and services.
- **Scientific computing:** CSR/CSC are sparse matrix formats; semirings and structural masks connect graph algorithms with GraphBLAS.

## References

1. [GraphBLAS Forum, *GraphBLAS C API Specification 2.1.0*](https://graphblas.org/docs/GraphBLAS_API_C_v2.1.0.pdf).
2. [SciPy, `csr_matrix` API reference](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html).
3. [SciPy, `csc_matrix` API reference](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csc_matrix.html).
4. [SuiteSparse:GraphBLAS maintained implementation](https://github.com/DrTimothyAldenDavis/GraphBLAS).
5. [NVIDIA, cuSPARSE sparse matrix storage formats](https://docs.nvidia.com/cuda/cusparse/storage-formats.html).
6. [Julian Shun and Guy E. Blelloch, *Ligra: A Lightweight Graph Processing Framework for Shared Memory*](https://jshun.csail.mit.edu/ligra.pdf).
7. [Graph Based Benchmark Suite documentation and source](https://paralg.github.io/gbbs/).
8. [Graph500 benchmark specification](https://graph500.org/?page_id=12).
9. [petgraph, `Csr` API documentation](https://docs.rs/petgraph/latest/petgraph/csr/struct.Csr.html).

## Exercises

### Exercise 1

Construct canonical CSR for `n=5` and edge records `(3,1,e4)`, `(0,2,e1)`, `(0,2,e0)`, `(4,4,e5)`, `(2,0,e3)`, `(0,1,e2)`. Give offsets, destinations, and IDs when rows sort by `(destination,id)`. Identify empty rows and parallel edges.

### Exercise 2

Derive a checked COO-to-CSR builder. State preconditions, intermediate invariants after counting, prefix sum, and scatter, and the failure guarantee if allocation or property conversion fails.

### Exercise 3

A directed CSR has offsets `[0,2,2,5,6]`, destinations `[1,3,0,1,1,2]`, and edge IDs `[a,b,c,d,e,f]`. Construct canonical CSC offsets, sources, and IDs sorted by `(source,id)` within each column. State a transpose validation property.

### Exercise 4

Design a read-mostly mutable graph using immutable CSR plus a delta. Define insertion, exact-edge deletion, query merge, snapshots, compaction trigger, stable IDs, publication, and reclamation. Name two kinds of amplification to measure.

### Exercise 5

Specify a benchmark and adversarial validation plan comparing CSR, CSR+CSC, and a vector adjacency representation for a graph analytics service. Include datasets, operations, byte accounting, construction, hardware controls, and correctness or security evidence.

## Answers to the Exercises

### Answer 1

Rows are: row 0 `(1,e2),(2,e0),(2,e1)`; row 1 empty; row 2 `(0,e3)`; row 3 `(1,e4)`; row 4 `(4,e5)`. Counts `[3,0,1,1,1]` give offsets `[0,3,3,4,5,6]`. Destinations are `[1,2,2,0,1,4]`; IDs are `[e2,e0,e1,e3,e4,e5]`. Row 1 is empty. The two `0->2` entries are parallel and remain distinguishable by ID.

### Answer 2

Preconditions declare `n`, valid/remappable endpoints, duplicate/property policies, and supported widths. Validate each source before incrementing a checked `counts[source]`; the sum of counts equals accepted `m`. Exclusive scan with checked addition establishes length `n+1`, start zero, monotonicity, interval lengths equal counts, and terminal `m`. Allocate all aligned arrays privately, copy row starts to cursors, and scatter one complete logical record into each reserved slot. Final `cursor[u]=offset[u+1]` and initialized-slot/property checks establish coverage and alignment. Optional sorting permutes whole records. Publish only after full validation. Any conversion/allocation error destroys the private build and leaves the prior graph unchanged, giving a strong failure guarantee.

### Answer 3

The edges are `(0,1,a),(0,3,b),(2,0,c),(2,1,d),(2,1,e),(3,2,f)`. Destination counts are `[1,3,1,1]`, so CSC offsets are `[0,1,4,5,6]`. Sorting by `(source,id)` within columns gives sources `[2,0,2,2,3,0]` and IDs `[c,a,d,e,f,b]`. Validation reconstructs `(source,destination,id)` records from both layouts and requires identical multisets with each stable ID occurring exactly once; degree sums and terminal offsets must both equal six.

### Answer 4

Keep a generation-tagged immutable CSR base and a delta indexed by source containing canonical insert records plus deletion markers keyed by stable edge ID. Insert allocates a new ID; exact deletion records that ID, never only an endpoint pair. A query merge-orders the base row and delta inserts, suppresses deleted IDs, and resolves repeated operations by sequence/version. Readers pin a generation containing base and a bounded delta snapshot. Trigger compaction by delta-to-base ratio, row fragmentation, query cost, memory, or age. Build a new CSR privately from the logical merged view, validate it, publish one generation pointer with release semantics, and reclaim old base/delta through epochs or references after readers drain. Measure read amplification from merging multiple sources and write/space amplification from rebuilding while old and new generations coexist.

### Answer 5

Use synthetic and real governed graphs spanning uniform and skewed degrees, isolated vertices, high-degree hubs, loops, duplicates, sorted/random COO, multiple `n:m` ratios, and property widths. Measure build, sort, transpose, peak temporary and resident bytes, outgoing/incoming scans, membership, BFS/SpMV-like suites, updates/rebuilds, serialization, mapping, and cold/warm reload. CSR+CSC must include both structures; vector adjacency must include capacities, objects, and allocator overhead. Pin compiler/runtime, CPU frequency, NUMA placement, page/cache state, threads, allocator, and device transfer. Validate all formats against the same edge-ID multiset and algorithm reference, fuzz malformed offsets/endpoints/lengths, inject overflow/allocation failures, and report distributions and confidence intervals rather than one best timing.
