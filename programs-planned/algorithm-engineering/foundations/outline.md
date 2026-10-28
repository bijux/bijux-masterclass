## S00
**M00 · Primitive Data Structures & Pointer Reality**

*(Pre-S01 warmup: concrete mental model for links, nodes, and layouts.)*

### **1. Node-Based Structures & Pointer Semantics**

* Minimal node layouts: payload + pointer(s); alignment and padding.
* Forward-only traversal; termination conditions; cycle vs acyclic assumptions.
* Pointer chasing as a performance primitive: cache misses, latency chains, branch mispredicts.

---

### **2. Singly Linked Lists (SLL)**

* Invariants: head reference, acyclicity, and size consistency.
* Core operations: push-front, push-back (with tail), insert-after, delete-after, search.
* Cost model: O(n) scans, impact of fragmentation and poor locality.
* When SLLs are *actually justified* vs when they are just pedagogical.

---

### **3. Doubly, Circular & Sentinel Lists**

* Node layout: `prev` + `next` + payload; the two-pointer consistency rule.
* Doubly linked lists (DLL): insert/delete invariants and minimal update patterns.
* Circular and sentinel-based lists: removing boundary cases by construction.
* Trade-offs: extra pointers vs simpler algorithms vs worse cache behaviour.

---

### **4. Array-Based vs Pointer-Based Sequences**

* Contiguity vs indirection: locality, prefetching, sequential scans.
* Dynamic arrays: high-level preview of growth/shrink strategies and amortised cost.
* When an array-based structure dominates any linked variant in practice.
* Why CPython `list` is a resizable array, not a linked list.

---

### **5. Basic Trees (Unbalanced Binary Trees / BSTs)**

* Node layout: value + left/right; optional parent pointer.
* Height, depth, and shape; degeneration into a list under adversarial inserts.
* Binary search tree invariants: key ordering, subtree intervals.
* Scope: *no balancing yet*—just enough to understand how shape affects cost.

---

### **6. Fundamental Traversals & Search**

* Pre-order / in-order / post-order: definitions, typical use-cases, O(n) cost.
* BFS/DFS using explicit queue/stack built from earlier list structures.
* Recursion vs explicit stack: call stack usage, overflow risks, debuggability.
* Binary search on arrays vs tree search: contrasting access patterns and locality.

---

### **7. Cost & Locality Models for These Primitives**

* Operation counts: pointer dereferences, comparisons, indirections.
* Latency chains: long pointer chains vs tight contiguous loops.
* Rough complexity sketches: SLL/DLL ops, BST search/insert vs array-based operations.
* How these informal models feed into S01’s more formal asymptotics and amortised analysis.

---

### **8. Invariants, Correctness & Pointer Bugs**

* Failure modes: lost nodes, self-loops, dangling pointers, broken DLL symmetry.
* “Edge-case-first” discipline: designing operations from boundaries inward.
* Micro-proofs:

  * SLL insert/delete preserve reachability and acyclicity.
  * BST search returns correct result under ordering invariant.
* Using invariants as design tools, not afterthoughts.

---

### **9. Implementation Discipline for Pointer-Like Structures**

* Clean, minimal APIs for list/tree primitives (no “god” structures).
* Explicit pre/postconditions for operations (even if only in comments/asserts).
* Lightweight checks: debug builds with invariants, release builds without them.
* Mental mapping from high-level language references (Python) to pointer semantics (C/Rust).

---

### **10. Bridge to the Main Track**

* How SLL/DLL/trees underpin:

  * CPython `list`/`dict`/`set` internals,
  * heaps and priority queues,
  * B-trees, LSM-trees, and storage engines later.
* Why pointer-chasing and locality become central in S01’s memory model and S02’s algorithms.
* Takeaway: after M00, “data structure” = **layout + invariants + cost + locality**, not just “container type”.

## S01 – Python Systems Foundations & Core Reasoning

### M01 · Python Object Model & Memory Reality

1. CPython object layout: header, refcount, type pointer.
2. Identity vs equality; aliasing and object graphs.
3. Mutability vs immutability; views vs copies vs slices.
4. Allocators: arenas, pools, fragmentation and reuse.
5. GIL and reference counting; cycle GC, weakref, finalisers.
6. `sys.getsizeof` vs true footprint; `tracemalloc` basics.
7. Dict-backed objects vs `__slots__` vs tuples/namedtuples.
8. Cost of attribute lookup, dynamic dispatch, descriptors.
9. High-level reading of CPython `list`/`dict` sources.
10. Tracing “one Python line” into allocations and pointer traffic.

---

### M02 · Linear Layout, Scans & Performance Tooling

1. Memory hierarchy: caches, lines, latency and bandwidth.
2. Contiguous vs pointer-chasing layouts; AoS vs SoA.
3. Prefix sums and difference arrays as core building blocks.
4. Streaming aggregates and sliding window computations.
5. Basics of sound microbenchmarking (warmup, variance, pinning).
6. Using `timeit` and `perf` for trustworthy measurements.
7. Generating and reading a flamegraph for a hot loop.
8. First energy proxies (RAPL/OS counters if available).
9. Refactoring loop-soup code into scan-based, measured pipelines.
10. Establishing “no single `time.time()` hacks” as a permanent rule.

---

### M03 · Hash Tables, Maps & Sets

1. Chaining vs open addressing vs cuckoo hashing: trade-offs.
2. CPython `dict`/`set`: layout, perturbation, order guarantees.
3. Load factor, clustering, tombstones, resize policies.
4. Writing correct `__hash__` + `__eq__` for composites.
5. Sets, multisets, maps, multimaps – choosing the right abstraction.
6. Ordered maps via `bisect`/`sortedcontainers` vs tree-based maps.
7. Hash vs tree vs flat array: performance and memory sketches.
8. Small Python map implementation with explicit invariants.
9. Hypothesis-based tests + adversarial key distributions.
10. When hash tables are the wrong tool, and why.

---

### M04 · Asymptotics, Recurrences & Amortised Analysis

1. O, Ω, Θ, o, ω – precise definitions with simple proofs.
2. Systematic analysis of single and nested loops.
3. Recurrences: recursion tree, substitution, Master theorem.
4. Classic divide-and-conquer costs (sort, select, convolution).
5. Aggregate and accounting methods for amortised analysis.
6. Potential method on dynamic arrays and queues.
7. How adversarial patterns can break naive amortised arguments.
8. Relating asymptotic predictions to measured timings (M02).
9. Full analysis of one nontrivial DS (recurrence + amortised).
10. Personal “complexity cheatsheet” of reusable patterns.

---

### M05 · Proofs, Invariants & Property-Based Testing

1. Constructing loop invariants and variants from first principles.
2. Induction for arrays, lists, trees, recursive algorithms.
3. Pre/postconditions and contracts in Python.
4. Termination arguments and well-founded measures.
5. Encoding invariants as runtime checks and debug modes.
6. Hypothesis: strategies, shrinking, stateful tests.
7. Using property tests to break naive invariants and corner cases.
8. Proof sketch for binary search or partition correctness.
9. Spec + proof sketch for a simple DS (stack/queue).
10. Program-wide discipline: **spec → prove → implement → test → measure**.

---

## S02 – Classical Algorithms, Randomisation & Design

### M06 · Priority Queues & Scheduling

1. Binary heap invariants and array layout.
2. Python `heapq` idioms; stale entries, decrease-key patterns.
3. Indexed priority queues: handles and lazy deletion.
4. Min/max heaps and running median / sliding quantile patterns.
5. k-way merge and external merge using heaps.
6. d-ary and pairing heaps: when constants dominate.
7. Event/timer queues and discrete-event simulation.
8. Scheduling with priorities and deadlines; fairness considerations.
9. Heap vs sort vs bucketed strategies: when each wins.
10. Small scheduling API with documented complexity and behaviour.

---

### M07 · Trees & Balanced Search Trees

1. BST invariants and degeneration scenarios.
2. Rotations: local transformations and formal invariants.
3. AVL tree insert/delete and height guarantees.
4. Red-Black tree insert/delete and colour invariants.
5. Treaps: minimal balanced tree with expected performance.
6. Augmentations: size/sum/min/max and custom aggregates.
7. Interval trees and range queries over balanced trees.
8. Pointer-based vs array-based vs B-tree-like node layouts.
9. Invariant checks and property tests for search trees.
10. Comparison against library ordered maps/sets.

---

### M08 · Graphs & Core Algorithms

1. Graph models: directed/undirected, weighted, multigraphs.
2. Representations: adjacency list, CSR, matrix – cost trade-offs.
3. BFS/DFS; tree/forest structure and connected components.
4. Dijkstra with heaps; multi-source and 0–1 variants.
5. Bellman–Ford and negative-cycle detection.
6. Floyd–Warshall sketch for APSP and when it actually applies.
7. MST: Kruskal + DSU and Prim + heap in practice.
8. Max-flow/min-cut (Dinic or Push–Relabel at high level).
9. Basic bipartite matching (Hopcroft–Karp idea).
10. Implement and benchmark at least one SSSP and one MST algorithm.

---

### M09 · DC, DP & Greedy Design Patterns

1. Divide-and-conquer template, recurrences and cost mapping.
2. DC examples beyond sorting (closest pair, etc.).
3. DP state design: position/resource/history dimensions.
4. Memoisation vs tabulation vs pure DC.
5. Greedy algorithms: local decisions and exchange arguments.
6. Matroid-style reasoning at conceptual level.
7. One DC, one DP and one Greedy solution with full reasoning.
8. Implement and test at least two contrasting designs.
9. Empirical comparison of DC/DP/Greedy approaches.
10. Written design note: chosen pattern and why alternatives were rejected.

---

### M10 · Randomised Algorithms & Probabilistic Analysis

1. Linearity of expectation and indicator variables.
2. Basic tail bounds (Chernoff/Hoeffding flavour).
3. Randomised quicksort and selection; expected bounds.
4. Randomised hashing and simple universal families.
5. Treaps revisited with formal probabilistic guarantees.
6. Error bounds for Count-Min style sketches.
7. “With high probability” arguments in DS/algorithms.
8. Empirical validation of theoretical error bounds.
9. Randomised vs deterministic designs under adversarial loads.
10. Foundations for later probabilistic DS (HLL, sketches, learned).

---

## S03 – Systems Language, Advanced DS, Spatial & Text

### M11 · Systems Programming for Data Structures (Rust/C++)

1. Ownership/borrowing (Rust) or RAII/move semantics (C++).
2. Lifetimes/references and aliasing vs UB.
3. Manual memory management and simple arenas/allocators.
4. Struct layout, padding, alignment, cache friendliness.
5. Iterators/ranges and generic programming for DS.
6. Safe vs minimal `unsafe` boundaries; encapsulating danger.
7. Testing & benchmarking frameworks in Rust/C++.
8. FFI between Python and Rust/C++ (PyO3 or Cython).
9. Style and idioms for OSS-quality DS code.
10. Skeleton DS library with CI, tests and basic benchmarks.

---

### M12 · Advanced Sorting & Layout

1. Timsort internals: run detection, galloping, invariants.
2. Quicksort/mergesort/Timsort: branch, cache, stability trade-offs.
3. Radix/bucket/spreadsort for numeric and structured keys.
4. External multi-way merge and I/O-aware sorting.
5. Sorting as layout normalisation (row/column, AoS/SoA).
6. Partial sort, nth_element, and top-k patterns.
7. Branchless partitioning and simple sorting networks.
8. Profiling sorts with perf/callgrind/flamegraphs.
9. Benchmarks across value distributions and sizes.
10. “Sort choice” guide for storage and analytics engines.

---

### M13 · Range Index Structures – Fenwick, Segment, Sparse

1. Range algebra: monoids, invertible operations, prefixes.
2. Fenwick tree (BIT) in Rust/C++ with robust tests.
3. Segment tree: array layout, generic merge functions.
4. Lazy propagation for range updates and correctness invariants.
5. One concrete “segment tree beats” optimisation.
6. Sparse tables for static idempotent queries (min/gcd/RMQ).
7. Coordinate compression and block-wise layouts.
8. Python harness driving Rust/C++ range DS.
9. Benchmarks under mixed query/update workloads.
10. Design note: choosing a range DS for a metrics/time-series service.

---

### M14 · Spatial Partitioning & Geospatial Indexes

1. Spatial query types: range, kNN, radius, intersection, containment.
2. Uniform and hash grids; pros and failure modes.
3. kd-trees: build, balance, search; high-dim breakdown.
4. Quadtrees and octrees for 2D/3D partitioning.
5. R-trees/R*-trees: MBRs, split heuristics, overlap reduction.
6. Geohash, H3, S2 at conceptual level.
7. Robust geometric predicates and FP pitfalls.
8. Rust/C++ spatial core with Python query harness.
9. Benchmarks: grids vs kd-tree vs R*-tree on realistic datasets.
10. Minimal geospatial index for radius search on Earth.

---

### M15 · String & Text Algorithms

1. String storage: slices, interning, small-string optimisation.
2. KMP/prefix function and Z-function with proofs and code.
3. Rolling hash for search, chunking and deduplication.
4. Suffix array + LCP (doubling/induced sorting variant).
5. Aho–Corasick automaton for multi-pattern search.
6. Unicode, tokenisation and normalisation issues.
7. When to move from exact search to embedding/ANN-based retrieval.
8. Minimal text engine: substring + prefix + simple ranking.
9. Benchmarks: naive vs indexed vs hash-based search.
10. Design checklist for text search engines under constraints.

---

## S04 – Parallel, Concurrency, GPU & Distributed

### M16 · Vectorised & Blocked Algorithms (CPU)

1. Vectorisation patterns: map, reduce, scan, stencil.
2. Blocking/tiling for caches and TLB; rectangular vs recursive.
3. Matrix-free operators and iterative methods as DS operations.
4. Graph and DP kernels via sparse/dense linear algebra.
5. Using BLAS/GEMM from Rust/C++ and Python.
6. Profiling CPU kernels with perf/callgrind/flamegraphs.
7. Naive vs vectorised vs blocked vs BLAS comparisons.
8. Time vs energy trade-offs for CPU kernels.
9. Vector-first API designs with explicit performance contracts.
10. Small vector-kernel library with tests and performance report.

---

### M17 · Parallel Algorithms & Work–Span Analysis

1. Fork–join model; work/span and Brent’s theorem.
2. Parallel map/reduce/scan/gather/scatter templates.
3. Parallel partition and compaction strategies.
4. Parallel sorting (sample sort, multi-phase quicksort).
5. Parallel BFS/SSSP sketches and frontier representations.
6. Work stealing and load balancing; grain size control.
7. Strong vs weak scaling, speedup and efficiency curves.
8. Using OpenMP/Rayon/TBB in DS/algorithms code.
9. One serious CPU-parallel artifact with full analysis.
10. Written report: bottlenecks, scaling limits, energy behaviour.

---

### M18 · Concurrent Data Structures

1. Hardware memory models: high-level view of reordering.
2. Atomics, fences, CAS; ABA problem and workaround patterns.
3. Lock-free stack or queue (one fully implemented).
4. Concurrent hashmap: sharded or striped baseline design.
5. Overview of advanced designs (Hopscotch, split-ordered).
6. RCU, epoch-based reclamation, hazard pointers (conceptual + one scheme).
7. Linearizability at a high level; simple histories and arguments.
8. Fuzzing + property-based testing harness for concurrency.
9. Benchmarks under varying contention levels.
10. One serious concurrent DS with spec, tests, perf report.

---

### M19 · GPU & Accelerator Data Structures

1. GPU model: threads, warps, blocks, grids; SIMT basics.
2. Memory hierarchy: shared, L2, global; coalescing constraints.
3. Parallel scan / segmented scan as GPU primitives.
4. GPU-friendly layouts: SoA, packed formats, alignment.
5. One actual GPU kernel: scan, histogram, radix pass or simple index.
6. Data transfer: PCIe/NVLink, unified memory trade-offs.
7. Calling CUDA/ROCm kernels from Rust/C++ and Python.
8. Profiling with Nsight/ROCm tools; reading utilisation graphs.
9. CPU vs GPU comparison on one workload.
10. Document when GPU offload helps and when it hurts.

---

### M20 · Distributed Dataflow & Large-Scale Graphs

1. Dataflow DAGs: Map, Shuffle, Reduce, Join, GroupBy.
2. Partitioning strategies, locality and skew handling.
3. Event time vs processing time; basic windowing.
4. Bulk-synchronous vs asynchronous models (Pregel/GraphLab-style).
5. Large-scale PageRank/CC/diffusion sketches.
6. Simple checkpointing and replay mechanisms.
7. Operator interfaces inspired by Spark/Flink/Beam.
8. Implementation on a local pseudo-cluster (containers/processes).
9. Evaluation of throughput, latency and simple failures.
10. One distributed algorithm artifact, aligned with future track.

---

## S05 – Storage, Persistence, Sketches & Succinctness

### M21 · Persistent & Immutable Data Structures

1. Structural sharing vs copying; persistent update patterns.
2. Persistent stacks/queues/deques with amortised guarantees.
3. Persistent balanced trees (Treap/RB) in Rust/C++.
4. HAMT internals: bitmap nodes, arity, collision handling.
5. Persistent segment trees and multi-version indices.
6. Version graphs and snapshot semantics (Git-like).
7. Immutability for concurrency, audit and rollback.
8. Integrating persistence into the track artifact (search/store/crypto).
9. Read-heavy benchmarks: persistent vs mutable variants.
10. Stable persistent index layer with tests and docs.

---

### M22 · Storage Engines – B-Tree, LSM & Skiplist

1. B-tree/B+-tree page layout, fan-out, splits/merges.
2. Copy-on-write B-trees and basic crash consistency.
3. LSM trees: memtables, SSTables, levels vs tiers, compaction.
4. Bloom filters and fence pointers in front of SSTables.
5. Skiplists as in-memory ordered structures (Redis/LevelDB style).
6. Space-filling curves (Z-order/Hilbert) for multi-dim keys.
7. Page/table compression: prefix, delta, dictionary, varint.
8. Tuning for write-heavy/read-heavy/mixed workloads.
9. Simple crash/restart tests and recovery logic.
10. Track-aligned toy storage engine integrated into the artifact.

---

### M23 · Search & Retrieval – Inverted, Vector & Hybrid

1. Inverted index: term dictionary, postings, skip data.
2. Ranking: BM25, field boosts and proximity hints.
3. Phrase queries, wildcards, fuzzy matching; tokenisation.
4. Vector search basics: embeddings, cosine/inner-product.
5. Overview of ANN structures (HNSW, IVF+PQ).
6. Hybrid search pipeline: BM25 + ANN reranking.
7. Simple learned index for monotone keys (PGM/RMI flavour).
8. Integrating indexes into the shared artifact.
9. Benchmarks on a realistic text/corpus dataset.
10. Design note: retrieval architecture choices and trade-offs.

---

### M24 · Probabilistic & Streaming Structures

1. Count-Min / Count sketch; heavy hitter detection.
2. HyperLogLog for cardinality; t-digest/KLL for quantiles.
3. Bloom, Cuckoo, quotient filters – membership trade-offs.
4. Sliding windows and time-decayed sketches.
5. LSH/MinHash for streaming similarity.
6. Exposed knobs: accuracy, latency, space, energy.
7. Validating sketch error vs M10’s theoretical bounds.
8. Integrating sketches into the track artifact (telemetry/logs/etc.).
9. Full metrics report for streaming components.
10. Design note: why sketching is justified (hardness, cost, scale).

---

### M25 · Compressed & Succinct Structures + Lean Proof

1. Succinct bitvectors; rank/select data structures.
2. Elias–Fano for monotone integer sequences.
3. Wavelet trees for compressed sequences/text.
4. Succinct tries and LOUDS encodings.
5. FM-index revisited in succinct style.
6. Compressed graph/adjacency encodings (conceptual).
7. Compression vs random access vs updates vs energy.
8. Lean formalisation of a crisp property (e.g. rank/select correctness).
9. Machine-checked Lean proof that compiles.
10. Linking the Lean spec to the implementation in the artifact.

---

## S06 – Complexity, Learned, Zero-Trust & Capstone

### M26 · Complexity & Hardness for DS/Algorithms

1. Refresher: asymptotics and tightness.
2. Reductions and NP-completeness (SAT → classic problems).
3. Why exact solutions are infeasible in many DS contexts.
4. Approximation basics and where guarantees matter.
5. Parameterised complexity and FPT flavour.
6. Fine-grained complexity and conditional lower bounds (SETH, 3SUM).
7. Data-structure lower bounds (cell-probe style overview).
8. Communication complexity intuition for distributed DS.
9. Connecting hardness to sketches, learned indexes and approximations.
10. Reduction/hardness write-up for one DS/alg design decision.

---

### M27 · Learned Data Structures

1. From CDFs to models-as-indexes: motivation and overview.
2. RMI architectures: training, routing, error handling.
3. PGM-index and spline-based learned indexing.
4. Learned Bloom filters and hybrid membership DS.
5. Robustness under skew, drift and adversarial queries.
6. CPU vs GPU implementations: when to target which.
7. Benchmarks vs classical indexes on SOSD-style workloads.
8. Integrating a learned DS into the shared artifact.
9. Failure mode analysis and mitigations.
10. Open questions and research directions in learned DS.

---

### M28 · Zero-Trust & Adversarial Data Structures

1. Threat models: malicious inputs, skew and corruption.
2. Attacks on learned indexes and sketches.
3. Timing-resistant DS and constant-time coding patterns.
4. Memory-safe vs unsafe implementations; Rust vs C++ risk.
5. Fuzzing and differential testing for robustness.
6. Randomisation and layout obfuscation as defences.
7. Side-channel considerations (cache/timing/branching).
8. Track-specific adversarial scenarios in the artifact.
9. Robustness evaluation under adversarial workloads.
10. Zero-trust design document for one DS in the project.

---

### M29 · Cryptographic & Verifiable Structures

1. Merkle trees and accumulators; inclusion proofs.
2. Sparse Merkle trees: inclusion and non-inclusion proofs.
3. Verkle trees and polynomial commitments (conceptual).
4. Authenticated dictionaries/maps for blockchains/PKI.
5. Transparent logs (certificate-transparency style).
6. Verifiable random functions in DS and protocols.
7. Side-channel-aware design for cryptographic DS.
8. Lean-based spec/argument for an authenticated DS property.
9. Implementation of one authenticated DS integrated into the artifact.
10. Benchmarks: proof size, verification time and energy.

---

### M30 · Approximation, Online & Learning-Augmented Algorithms + Capstone

1. Approximation algorithms: ratios and bicriteria guarantees.
2. Online algorithms and competitive analysis basics.
3. Learning-augmented algorithms: advice, robustness, regret.
4. Algorithm portfolios and bandits over algorithm choices.
5. Multi-objective tuning: latency, memory, energy, accuracy.
6. Evaluation methodology for approximate/online/learning-augmented methods.
7. Final shaping of the track artifact into a coherent system/library.
8. Capstone execution: Rust/C++ implementation, spec, tests, benchmarks, energy metrics.
9. Capstone outcome: merged OSS PR **or** benchmark-beating result **or** substantial OSS repo with full reproducible suite if external PR blocked.
10. Final defence: technical presentation linking theory (M10, M24, M26, M27) to system behaviour and empirical results.

---


