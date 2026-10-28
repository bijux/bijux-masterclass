# 16. Algorithm Engineering

**Program code:** `ALGE`

**Purpose:** Develop the full cycle of algorithmic work: precise problem formulation, design, proof, implementation, measurement, tuning, and selection under real machine and workload constraints.

**Level-II professional outcome:** Ready to solve unfamiliar computational problems, implement robust high-performance algorithms, compare alternatives empirically, and justify choices in production or research software.

**Prerequisites:** discrete mathematics; programming proficiency; data structures; basic probability.

**Primary ownership:** algorithm design paradigms; correctness and analysis; searching and sorting; graph and flow algorithms; string and sequence algorithms; optimization algorithms; randomized and approximation algorithms; online and streaming algorithms; parallel and external-memory algorithms; experimental algorithmics.

**Explicit exclusions:** complexity-class theory (Program 15); data-structure implementation ownership (Program 17); hardware architecture (Program 23).

## Level I — Undergraduate Core

Modules 001–050 establish the complete foundational model and canonical mechanisms.

### Block 01 — Algorithmic Problems, Proof, and Cost

| Module | Canonical chapter | Future file |
|---:|---|---|
| 001 | **Problem Statements, Inputs, Outputs, and Constraints** | `001-problem-statements-inputs-outputs-and-constraints.md` |
| 002 | **Preconditions, Postconditions, and Correctness** | `002-preconditions-postconditions-and-correctness.md` |
| 003 | **Loop Invariants for Algorithm Correctness** | `003-loop-invariants-for-algorithm-correctness.md` |
| 004 | **Inductive Correctness Proofs** | `004-inductive-correctness-proofs.md` |
| 005 | **Asymptotic Time and Space** | `005-asymptotic-time-and-space.md` |
| 006 | **Best, Worst, Expected, and Amortized Cost** | `006-best-worst-expected-and-amortized-cost.md` |
| 007 | **Recurrences and the Master Method** | `007-recurrences-and-the-master-method.md` |
| 008 | **Lower Bounds and Adversary Arguments** | `008-lower-bounds-and-adversary-arguments.md` |
| 009 | **Machine Models and Hidden Constants** | `009-machine-models-and-hidden-constants.md` |
| 010 | **Combining Proof and Measurement in Algorithm Evaluation** | `010-combining-proof-and-measurement-in-algorithm-evaluation.md` |

### Block 02 — Searching, Sorting, and Selection

| Module | Canonical chapter | Future file |
|---:|---|---|
| 011 | **Linear and Binary Search** | `011-linear-and-binary-search.md` |
| 012 | **Insertion, Selection, and Shell Sorting** | `012-insertion-selection-and-shell-sorting.md` |
| 013 | **Merge Sort** | `013-merge-sort.md` |
| 014 | **Quicksort and Partitioning** | `014-quicksort-and-partitioning.md` |
| 015 | **Heapsort** | `015-heapsort.md` |
| 016 | **Counting, Radix, and Bucket Sorting** | `016-counting-radix-and-bucket-sorting.md` |
| 017 | **Order Statistics and Quickselect** | `017-order-statistics-and-quickselect.md` |
| 018 | **Stable Sorting and Indirect Sorting** | `018-stable-sorting-and-indirect-sorting.md` |
| 019 | **Adaptive and Hybrid Sorting** | `019-adaptive-and-hybrid-sorting.md` |
| 020 | **Engineering a Sort for Real Data Distributions** | `020-engineering-a-sort-for-real-data-distributions.md` |

### Block 03 — Core Design Paradigms

| Module | Canonical chapter | Future file |
|---:|---|---|
| 021 | **Divide and Conquer** | `021-divide-and-conquer.md` |
| 022 | **Greedy Choice and Exchange Arguments** | `022-greedy-choice-and-exchange-arguments.md` |
| 023 | **Dynamic Programming State Design** | `023-dynamic-programming-state-design.md` |
| 024 | **Memoization and Bottom-Up Evaluation** | `024-memoization-and-bottom-up-evaluation.md` |
| 025 | **Backtracking** | `025-backtracking.md` |
| 026 | **Branch and Bound** | `026-branch-and-bound.md` |
| 027 | **Meet-in-the-Middle** | `027-meet-in-the-middle.md` |
| 028 | **Transform-and-Conquer** | `028-transform-and-conquer.md` |
| 029 | **Randomization as a Design Tool** | `029-randomization-as-a-design-tool.md` |
| 030 | **Selecting a Design Paradigm from Problem Structure** | `030-selecting-a-design-paradigm-from-problem-structure.md` |

### Block 04 — Graph Algorithms

| Module | Canonical chapter | Future file |
|---:|---|---|
| 031 | **Breadth-First Search** | `031-breadth-first-search.md` |
| 032 | **Depth-First Search** | `032-depth-first-search.md` |
| 033 | **Topological Ordering** | `033-topological-ordering.md` |
| 034 | **Strongly Connected Components** | `034-strongly-connected-components.md` |
| 035 | **Minimum Spanning Trees** | `035-minimum-spanning-trees.md` |
| 036 | **Dijkstra's Shortest Paths** | `036-dijkstra-s-shortest-paths.md` |
| 037 | **Bellman-Ford and Negative Weights** | `037-bellman-ford-and-negative-weights.md` |
| 038 | **All-Pairs Shortest Paths** | `038-all-pairs-shortest-paths.md` |
| 039 | **Disjoint Sets in Graph Algorithms** | `039-disjoint-sets-in-graph-algorithms.md` |
| 040 | **Engineering Graph Traversal for Sparse and Dense Inputs** | `040-engineering-graph-traversal-for-sparse-and-dense-inputs.md` |

### Block 05 — Flows, Matching, and Combinatorial Optimization

| Module | Canonical chapter | Future file |
|---:|---|---|
| 041 | **Flow Networks and Residual Graphs** | `041-flow-networks-and-residual-graphs.md` |
| 042 | **Ford-Fulkerson Method** | `042-ford-fulkerson-method.md` |
| 043 | **Edmonds-Karp Algorithm** | `043-edmonds-karp-algorithm.md` |
| 044 | **Dinic's Algorithm** | `044-dinic-s-algorithm.md` |
| 045 | **Max-Flow Min-Cut Theorem** | `045-max-flow-min-cut-theorem.md` |
| 046 | **Bipartite Matching** | `046-bipartite-matching.md` |
| 047 | **Assignment Problems** | `047-assignment-problems.md` |
| 048 | **Minimum-Cost Flow** | `048-minimum-cost-flow.md` |
| 049 | **Network-Flow Modeling Patterns** | `049-network-flow-modeling-patterns.md` |
| 050 | **Turning a Domain Problem into a Graph Optimization Problem** | `050-turning-a-domain-problem-into-a-graph-optimization-problem.md` |

## Level II — Graduate and Professional Depth

Modules 051–100 add internals, difficult cases, production constraints, advanced theory, and independent technical judgment.

### Block 06 — String, Sequence, and Compression Algorithms

| Module | Canonical chapter | Future file |
|---:|---|---|
| 051 | **Naive and Prefix-Based Pattern Matching** | `051-naive-and-prefix-based-pattern-matching.md` |
| 052 | **Knuth-Morris-Pratt** | `052-knuth-morris-pratt.md` |
| 053 | **Boyer-Moore Family** | `053-boyer-moore-family.md` |
| 054 | **Rabin-Karp and Rolling Hashes** | `054-rabin-karp-and-rolling-hashes.md` |
| 055 | **Suffix Arrays and LCP** | `055-suffix-arrays-and-lcp.md` |
| 056 | **Suffix Trees and Automata** | `056-suffix-trees-and-automata.md` |
| 057 | **Edit Distance** | `057-edit-distance.md` |
| 058 | **Global and Local Sequence Alignment** | `058-global-and-local-sequence-alignment.md` |
| 059 | **Dictionary Compression** | `059-dictionary-compression.md` |
| 060 | **Engineering Search over Large Text and Sequence Collections** | `060-engineering-search-over-large-text-and-sequence-collections.md` |

### Block 07 — Approximation, Heuristics, and Randomized Algorithms

| Module | Canonical chapter | Future file |
|---:|---|---|
| 061 | **Approximation Ratios and Guarantees** | `061-approximation-ratios-and-guarantees.md` |
| 062 | **Greedy Approximation** | `062-greedy-approximation.md` |
| 063 | **Linear-Programming Rounding** | `063-linear-programming-rounding.md` |
| 064 | **Primal-Dual Approximation** | `064-primal-dual-approximation.md` |
| 065 | **Local Search** | `065-local-search.md` |
| 066 | **Randomized Selection and Sampling** | `066-randomized-selection-and-sampling.md` |
| 067 | **Randomized Incremental Construction** | `067-randomized-incremental-construction.md` |
| 068 | **Monte Carlo and Las Vegas Algorithms** | `068-monte-carlo-and-las-vegas-algorithms.md` |
| 069 | **Metaheuristics and Their Evidence Requirements** | `069-metaheuristics-and-their-evidence-requirements.md` |
| 070 | **Choosing Between Exact, Approximate, and Heuristic Solutions** | `070-choosing-between-exact-approximate-and-heuristic-solutions.md` |

### Block 08 — Online, Streaming, and Dynamic Algorithms

| Module | Canonical chapter | Future file |
|---:|---|---|
| 071 | **Online Decisions and Competitive Analysis** | `071-online-decisions-and-competitive-analysis.md` |
| 072 | **Caching and Paging Algorithms** | `072-caching-and-paging-algorithms.md` |
| 073 | **Online Scheduling** | `073-online-scheduling.md` |
| 074 | **Streaming Frequency Estimation** | `074-streaming-frequency-estimation.md` |
| 075 | **Distinct Counting** | `075-distinct-counting.md` |
| 076 | **Streaming Quantiles** | `076-streaming-quantiles.md` |
| 077 | **Reservoir Sampling** | `077-reservoir-sampling.md` |
| 078 | **Dynamic Connectivity** | `078-dynamic-connectivity.md` |
| 079 | **Dynamic Shortest-Path and Reachability Concepts** | `079-dynamic-shortest-path-and-reachability-concepts.md` |
| 080 | **Engineering Algorithms Under One-Pass and Update Constraints** | `080-engineering-algorithms-under-one-pass-and-update-constraints.md` |

### Block 09 — Parallel, External-Memory, and Cache-Efficient Algorithms

| Module | Canonical chapter | Future file |
|---:|---|---|
| 081 | **Work, Span, and Parallel Dependency** | `081-work-span-and-parallel-dependency.md` |
| 082 | **Parallel Prefix and Reduction** | `082-parallel-prefix-and-reduction.md` |
| 083 | **Parallel Sorting** | `083-parallel-sorting.md` |
| 084 | **Parallel Graph Traversal** | `084-parallel-graph-traversal.md` |
| 085 | **External-Memory Cost Models** | `085-external-memory-cost-models.md` |
| 086 | **External Sorting** | `086-external-sorting.md` |
| 087 | **Blocked Matrix and Graph Algorithms** | `087-blocked-matrix-and-graph-algorithms.md` |
| 088 | **Cache-Oblivious Design** | `088-cache-oblivious-design.md` |
| 089 | **I/O-Efficient Search and Index Construction** | `089-i-o-efficient-search-and-index-construction.md` |
| 090 | **Mapping an Algorithm Across Memory, Threads, and Storage** | `090-mapping-an-algorithm-across-memory-threads-and-storage.md` |

### Block 10 — Experimental Algorithmics and Advanced Judgment

| Module | Canonical chapter | Future file |
|---:|---|---|
| 091 | **Representative Workload Construction** | `091-representative-workload-construction.md` |
| 092 | **Benchmark Design and Reproducibility** | `092-benchmark-design-and-reproducibility.md` |
| 093 | **Profiling Time, Memory, and I/O** | `093-profiling-time-memory-and-i-o.md` |
| 094 | **Adversarial and Pathological Inputs** | `094-adversarial-and-pathological-inputs.md` |
| 095 | **Parameter Tuning Without Overfitting** | `095-parameter-tuning-without-overfitting.md` |
| 096 | **Comparing Implementations Statistically** | `096-comparing-implementations-statistically.md` |
| 097 | **Algorithm Portfolios and Adaptive Selection** | `097-algorithm-portfolios-and-adaptive-selection.md` |
| 098 | **Numerical Stability in Algorithm Implementation** | `098-numerical-stability-in-algorithm-implementation.md` |
| 099 | **Reading and Reproducing an Algorithm Paper** | `099-reading-and-reproducing-an-algorithm-paper.md` |
| 100 | **Defending an Algorithmic Choice Under Proof and Performance Review** | `100-defending-an-algorithmic-choice-under-proof-and-performance-review.md` |

## Completion standard

This program is complete only when all 100 future module files satisfy `MODULE_CONTENT_CONTRACT.md`. The roadmap itself is not course completion.
