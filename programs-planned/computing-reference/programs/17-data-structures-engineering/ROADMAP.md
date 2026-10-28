# 17. Data Structures Engineering

**Program code:** `DSE`

**Purpose:** Develop workload-aware command of in-memory, persistent, concurrent, external-memory, approximate, and distributed data structures, including their invariants and machine-level costs.

**Level-II professional outcome:** Ready to design, implement, test, benchmark, and select data structures for libraries, databases, runtimes, search systems, and high-performance applications.

**Prerequisites:** programming proficiency; algorithms and asymptotic analysis; basic memory hierarchy.

**Primary ownership:** abstract data types and invariants; linear and associative structures; trees and heaps; graph and string structures; persistent structures; concurrent structures; external-memory structures; probabilistic structures; spatial and vector indexes; succinct and distributed structures.

**Explicit exclusions:** algorithm-design ownership (Program 16); database-engine internals beyond structures (Program 18); distributed consistency protocols (Program 27).

## Level I — Undergraduate Core

Modules 001–050 establish the complete foundational model and canonical mechanisms.

### Block 01 — Representation, Invariants, and Cost Models

| Module | Canonical chapter | Future file |
|---:|---|---|
| 001 | **Abstract Data Types and Concrete Representations** | `001-abstract-data-types-and-concrete-representations.md` |
| 002 | **Representation Invariants** | `002-representation-invariants.md` |
| 003 | **Operation Contracts** | `003-operation-contracts.md` |
| 004 | **Time, Space, and Allocation Cost** | `004-time-space-and-allocation-cost.md` |
| 005 | **Contiguous and Linked Layouts** | `005-contiguous-and-linked-layouts.md` |
| 006 | **Memory Locality and Cache Behavior** | `006-memory-locality-and-cache-behavior.md` |
| 007 | **Genericity and Type Constraints** | `007-genericity-and-type-constraints.md` |
| 008 | **Iterators and Traversal Protocols** | `008-iterators-and-traversal-protocols.md` |
| 009 | **Property-Based Testing of Data Structures** | `009-property-based-testing-of-data-structures.md` |
| 010 | **Benchmarking a Structure Without Misleading Results** | `010-benchmarking-a-structure-without-misleading-results.md` |

### Block 02 — Sequences and Linear Structures

| Module | Canonical chapter | Future file |
|---:|---|---|
| 011 | **Fixed Arrays** | `011-fixed-arrays.md` |
| 012 | **Dynamic Arrays and Geometric Growth** | `012-dynamic-arrays-and-geometric-growth.md` |
| 013 | **Gap Buffers** | `013-gap-buffers.md` |
| 014 | **Singly Linked Lists** | `014-singly-linked-lists.md` |
| 015 | **Doubly and Intrusive Linked Lists** | `015-doubly-and-intrusive-linked-lists.md` |
| 016 | **Stacks** | `016-stacks.md` |
| 017 | **Queues** | `017-queues.md` |
| 018 | **Deques** | `018-deques.md` |
| 019 | **Ring Buffers** | `019-ring-buffers.md` |
| 020 | **Ropes and Piece Tables** | `020-ropes-and-piece-tables.md` |

### Block 03 — Hash-Based Structures

| Module | Canonical chapter | Future file |
|---:|---|---|
| 021 | **Hash Functions and Distribution** | `021-hash-functions-and-distribution.md` |
| 022 | **Separate Chaining** | `022-separate-chaining.md` |
| 023 | **Linear Probing** | `023-linear-probing.md` |
| 024 | **Quadratic Probing and Double Hashing** | `024-quadratic-probing-and-double-hashing.md` |
| 025 | **Robin Hood Hashing** | `025-robin-hood-hashing.md` |
| 026 | **Cuckoo Hashing** | `026-cuckoo-hashing.md` |
| 027 | **Hopscotch Hashing** | `027-hopscotch-hashing.md` |
| 028 | **Resizing and Incremental Rehashing** | `028-resizing-and-incremental-rehashing.md` |
| 029 | **Hash-Flooding Resistance** | `029-hash-flooding-resistance.md` |
| 030 | **Engineering a Memory-Efficient Hash Map** | `030-engineering-a-memory-efficient-hash-map.md` |

### Block 04 — Ordered Trees and Priority Structures

| Module | Canonical chapter | Future file |
|---:|---|---|
| 031 | **Binary Search Trees** | `031-binary-search-trees.md` |
| 032 | **AVL Trees** | `032-avl-trees.md` |
| 033 | **Red-Black Trees** | `033-red-black-trees.md` |
| 034 | **Treaps** | `034-treaps.md` |
| 035 | **Splay Trees** | `035-splay-trees.md` |
| 036 | **Order-Statistic Trees** | `036-order-statistic-trees.md` |
| 037 | **Fenwick, Interval, and Segment Trees** | `037-fenwick-interval-and-segment-trees.md` |
| 038 | **Binary and d-Ary Heaps** | `038-binary-and-d-ary-heaps.md` |
| 039 | **Indexed and Meldable Priority Queues** | `039-indexed-and-meldable-priority-queues.md` |
| 040 | **Skip Lists** | `040-skip-lists.md` |

### Block 05 — Graphs, Strings, and Disjoint Structures

| Module | Canonical chapter | Future file |
|---:|---|---|
| 041 | **Adjacency Matrices, Lists, and Edge Arrays** | `041-adjacency-matrices-lists-and-edge-arrays.md` |
| 042 | **Compressed Sparse Graph Layouts** | `042-compressed-sparse-graph-layouts.md` |
| 043 | **Disjoint-Set Forests** | `043-disjoint-set-forests.md` |
| 044 | **Tries** | `044-tries.md` |
| 045 | **Compressed and Radix Tries** | `045-compressed-and-radix-tries.md` |
| 046 | **Patricia Tries** | `046-patricia-tries.md` |
| 047 | **Suffix Arrays** | `047-suffix-arrays.md` |
| 048 | **Suffix Trees** | `048-suffix-trees.md` |
| 049 | **Inverted Indexes** | `049-inverted-indexes.md` |
| 050 | **Choosing Representations for Large Graphs and Text** | `050-choosing-representations-for-large-graphs-and-text.md` |

## Level II — Graduate and Professional Depth

Modules 051–100 add internals, difficult cases, production constraints, advanced theory, and independent technical judgment.

### Block 06 — Persistent and Immutable Structures

| Module | Canonical chapter | Future file |
|---:|---|---|
| 051 | **Path Copying** | `051-path-copying.md` |
| 052 | **Structural Sharing** | `052-structural-sharing.md` |
| 053 | **Persistent Lists and Queues** | `053-persistent-lists-and-queues.md` |
| 054 | **Persistent Balanced Trees** | `054-persistent-balanced-trees.md` |
| 055 | **Hash Array Mapped Tries** | `055-hash-array-mapped-tries.md` |
| 056 | **Finger Trees** | `056-finger-trees.md` |
| 057 | **Persistent Union-Find Trade-Offs** | `057-persistent-union-find-trade-offs.md` |
| 058 | **Fat Nodes and Partial Persistence** | `058-fat-nodes-and-partial-persistence.md` |
| 059 | **Full and Confluent Persistence** | `059-full-and-confluent-persistence.md` |
| 060 | **Measuring Persistent-Structure Time and Memory** | `060-measuring-persistent-structure-time-and-memory.md` |

### Block 07 — Concurrent Data Structures

| Module | Canonical chapter | Future file |
|---:|---|---|
| 061 | **Thread-Safe Wrappers and Coarse-Grained Locks** | `061-thread-safe-wrappers-and-coarse-grained-locks.md` |
| 062 | **Fine-Grained Locking** | `062-fine-grained-locking.md` |
| 063 | **Concurrent Hash Maps** | `063-concurrent-hash-maps.md` |
| 064 | **Concurrent Skip Lists** | `064-concurrent-skip-lists.md` |
| 065 | **Lock-Free Stack Structure and Invariants** | `065-lock-free-stack-structure-and-invariants.md` |
| 066 | **Michael-Scott Queues** | `066-michael-scott-queues.md` |
| 067 | **ABA Avoidance** | `067-aba-avoidance.md` |
| 068 | **Hazard Pointers and Epoch Reclamation** | `068-hazard-pointers-and-epoch-reclamation.md` |
| 069 | **Read-Copy-Update Structures** | `069-read-copy-update-structures.md` |
| 070 | **Linearizability Testing of Concurrent Structures** | `070-linearizability-testing-of-concurrent-structures.md` |

### Block 08 — External-Memory and Storage Structures

| Module | Canonical chapter | Future file |
|---:|---|---|
| 071 | **I/O Models and Page-Oriented Design** | `071-i-o-models-and-page-oriented-design.md` |
| 072 | **B-Trees** | `072-b-trees.md` |
| 073 | **B+ Trees** | `073-b-trees.md` |
| 074 | **Bulk Loading and Range Scans** | `074-bulk-loading-and-range-scans.md` |
| 075 | **Copy-on-Write Trees** | `075-copy-on-write-trees.md` |
| 076 | **Log-Structured Merge Trees** | `076-log-structured-merge-trees.md` |
| 077 | **SSTables and Sorted Runs** | `077-sstables-and-sorted-runs.md` |
| 078 | **Bloom-Assisted Lookup** | `078-bloom-assisted-lookup.md` |
| 079 | **Compaction Strategies** | `079-compaction-strategies.md` |
| 080 | **Balancing Read, Write, and Space Amplification** | `080-balancing-read-write-and-space-amplification.md` |

### Block 09 — Approximate, Spatial, and Vector Structures

| Module | Canonical chapter | Future file |
|---:|---|---|
| 081 | **Bloom Filters** | `081-bloom-filters.md` |
| 082 | **Counting and Scalable Bloom Filters** | `082-counting-and-scalable-bloom-filters.md` |
| 083 | **Cuckoo and Quotient Filters** | `083-cuckoo-and-quotient-filters.md` |
| 084 | **Count-Min Sketch** | `084-count-min-sketch.md` |
| 085 | **HyperLogLog** | `085-hyperloglog.md` |
| 086 | **Quantile Sketches** | `086-quantile-sketches.md` |
| 087 | **k-d Trees** | `087-k-d-trees.md` |
| 088 | **R-Trees** | `088-r-trees.md` |
| 089 | **Locality-Sensitive Hashing** | `089-locality-sensitive-hashing.md` |
| 090 | **HNSW and Approximate Nearest-Neighbor Graphs** | `090-hnsw-and-approximate-nearest-neighbor-graphs.md` |

### Block 10 — Succinct, Dynamic, and Distributed Structures

| Module | Canonical chapter | Future file |
|---:|---|---|
| 091 | **Bit Vectors with Rank and Select** | `091-bit-vectors-with-rank-and-select.md` |
| 092 | **Wavelet Trees** | `092-wavelet-trees.md` |
| 093 | **Succinct Trees and Graphs** | `093-succinct-trees-and-graphs.md` |
| 094 | **Compressed Suffix Arrays** | `094-compressed-suffix-arrays.md` |
| 095 | **Dynamic Fenwick and Segment Structures** | `095-dynamic-fenwick-and-segment-structures.md` |
| 096 | **Merkle Trees** | `096-merkle-trees.md` |
| 097 | **Consistent-Hash Rings** | `097-consistent-hash-rings.md` |
| 098 | **Distributed Hash-Table Data Structures** | `098-distributed-hash-table-data-structures.md` |
| 099 | **Conflict-Free Replicated Data Types as Structures** | `099-conflict-free-replicated-data-types-as-structures.md` |
| 100 | **Reviewing a Data Structure from Invariants, Workload, Hardware, and Failure** | `100-reviewing-a-data-structure-from-invariants-workload-hardware-and-failure.md` |

## Completion standard

This program is complete only when all 100 future module files satisfy `MODULE_CONTENT_CONTRACT.md`. The roadmap itself is not course completion.
