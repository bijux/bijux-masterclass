# Dask Deep Dive — Unified Table of Contents

## [Module 01: First Principles — The Task-Graph Contract](M01.md)

### [Core 1 — Execution Model: DAGs, Schedulers & Overhead Economics](M01.md#core-1--execution-model-dags-schedulers--overhead-economics)

* Dask as a **DAG executor** (not “parallel pandas”)
* Local vs Distributed schedulers: latency, coordination, failure modes
* Task overhead economics: granularity, why micro-tasks fail
* Diagram: *pipeline → graph → scheduler → workers*

### [Core 2 — Picking the Right Abstraction: `delayed`, `bag`, `array`, `dataframe`](M01.md#core-2--picking-the-right-abstraction-delayed-bag-array-dataframe)

* What each collection optimizes for (tabular / irregular / numeric / custom DAG)
* Boundary hygiene: avoid accidental `compute()`
* Anti-pattern: coercing semi-structured data into DataFrame too early

### [Core 3 — Dask DataFrame Reality: Partitions, Index, Divisions, Unknown Divisions](M01.md#core-3--dask-dataframe-reality-partitions-index-divisions-unknown-divisions)

* Partitions as parallelism **and** memory/survivability units
* Divisions: why they gate `.loc`, joins, fast paths
* Unknown divisions: detection, causes, worst-case behavior
* `repartition` vs `set_index` and the shuffle cost model

### [Core 4 — Laziness Control: `compute`, `persist` & Graph Optimization](M01.md#core-4--laziness-control-compute-persist--graph-optimization)

* `compute()` vs `persist()` vs stay lazy: correct use and failure patterns
* Fusion, inlining, graph blow-ups: causes and prevention
* Purity discipline: determinism, restart-safe execution

### [Core 5 — I/O at Scale: Dataset Layout as a Performance Primitive](M01.md#core-5--io-at-scale-dataset-layout-as-a-performance-primitive)

* Parquet-first: row groups, metadata, file sizing
* Projection + predicate pushdown + partition pruning (what gets skipped)
* Writing strategy: avoid small files, stable schema, non-skewed partition keys

---

## [Module 02: Scalable Analytics — Shuffles, Metadata, and Cost-Controlled Computation](M02.md)

### [Core 1 — Shuffles: The Dominant Runtime and Memory Event](M02.md#core-1--shuffles-the-dominant-runtime-and-memory-event)

* What a shuffle is and why it dominates
* Shuffle triggers: `groupby`, `join`, `set_index`, many sorts
* Cost control levers: width → rows → pre-aggregate → key choice

### [Core 2 — GroupBy and Aggregations Under Skew (Correctness + Throughput)](M02.md#core-2--groupby-and-aggregations-under-skew-correctness--throughput)

* Mergeable reductions vs hard aggregations (tree-reduction thinking)
* Skew/hot keys: detection and mitigation (pre-agg, salting, alternative keys)
* Avoid accidental global work (implicit sorts, unnecessary repartitions)

### [Core 3 — `map_partitions` as the Production Knife: Metadata Coherence](M02.md#core-3--map_partitions-as-the-production-knife-metadata-coherence)

* `map_partitions` (and `map_overlap` when needed) for controlled per-partition logic
* Metadata coherence: schema/dtype drift as a distributed failure mode
* `meta=` contracts (including `make_meta`)
* Vectorize inside partitions; row-wise apply as an explicit tradeoff

### [Core 4 — Array + Bag Pipelines (When DataFrames Are the Wrong Tool)](M02.md#core-4--array--bag-pipelines-when-dataframes-are-the-wrong-tool)

* Array chunking: shape-driven performance; avoid tiny chunks
* Bag for logs/JSON: schema-free filtering → normalization to DataFrame
* Mixed topology: bag → dataframe → parquet (where shuffles enter)

### [Core 5 — Partition/Chunk Sizing: The Practical Performance Lever](M02.md#core-5--partitionchunk-sizing-the-practical-performance-lever)

* Byte-based sizing heuristic (~50–200MB) and when it breaks
* Coalesce vs repartition: overhead vs memory safety vs shuffle pressure
* Pipeline shape discipline: avoid repartition ping-pong and repeated reshuffles

---

## [Module 03: Production Dask — Distributed Runtime, Diagnostics, and Deployment](M03.md)

### [Core 1 — Distributed Runtime: Client, Workers, Futures, Orchestration](M03.md#core-1--distributed-runtime-client-workers-futures-orchestration)

* Collections vs futures: when futures are the right control plane
* Threads vs processes; GIL/BLAS oversubscription; locality/transfer costs
* Orchestration primitives: `submit`, `wait`, `as_completed`, cancellation/error patterns

### [Core 2 — Memory, Spilling, Survival Engineering](M03.md#core-2--memory-spilling-survival-engineering)

* Managed vs unmanaged memory; what spilling can/can’t save
* Failure regimes: serialization bloat, shuffle buffers, runaway graphs, stragglers
* Mitigation playbook: partitions, stage boundaries, payload control, retries

### [Core 3 — Diagnostics: Read the Dashboard Like an Engineer](M03.md#core-3--diagnostics-read-the-dashboard-like-an-engineer)

* Task Stream, Graph, Shuffle, Workers/Memory, Profile panels
* Diagnosing: scheduler-bound vs shuffle-bound vs memory-bound vs serialization-bound
* Inside-task profiling: separating Python/pandas from scheduling/I/O overhead

### [Core 4 — Deployment: Local → HPC → Kubernetes → Gateway](M03.md#core-4--deployment-local--hpc--kubernetes--gateway)

* LocalCluster for parity; environment reproducibility
* SLURM/jobqueue patterns; storage realities (FS vs object store)
* Kubernetes operator patterns; Gateway for multi-tenant clusters
* Adaptive scaling: safe bounds and churn avoidance during shuffles

### [Core 5 — Engineering Practice: Contracts, Testing, When Not to Use Dask](M03.md#core-5--engineering-practice-contracts-testing-when-not-to-use-dask)

* Unit-test partition logic; minimal distributed integration tests
* Idempotent I/O boundaries; restart-safe pipelines
* When not to use Dask: Spark / DuckDB / Polars / Ray / pandas decision criteria

---

## [Module 04: Advanced Topics — Control Plane, Scheduling, and “Sharp Edges”](M04.md)

### [Core 1 — Control Plane Primitives: Locality, Scatter, Sync, Actors](M04.md#core-1--control-plane-primitives-locality-scatter-sync-actors)

* Data locality as a knob: `scatter`, broadcast, avoiding repeated transfers
* Published datasets: scheduler-scoped named handles
* Distributed sync: `Lock`, `Semaphore`, `Event`, `Queue`, `Variable`
* Actors: stateful services on workers (tradeoffs and failure semantics)

### [Core 2 — Scheduling Controls: Resources, Priorities, Annotations, Retries](M04.md#core-2--scheduling-controls-resources-priorities-annotations-retries)

* Resource constraints / placement (GPU, high-mem, licensed resources)
* Priorities and starvation prevention in mixed workloads
* `dask.annotate(...)`: applying scheduling policy over graph regions
* Retries as policy: where retries belong; failure amplification risks

### [Core 3 — Advanced DataFrame Scalability Knobs: Shuffle Engines, `split_out`, Categoricals](M04.md#core-3--advanced-dataframe-scalability-knobs-shuffle-engines-split_out-categoricals)

* Shuffle engines/config tradeoffs (disk/network/memory profile)
* Reduction-tree tuning: `split_out`, `split_every`
* Categoricals for payload/state reduction (when cardinality is truly low)

### [Core 4 — Advanced Array + Bag Patterns: Rechunk, Overlap, Custom Reductions](M04.md#core-4--advanced-array--bag-patterns-rechunk-overlap-custom-reductions)

* Rechunk planning: global cost, one-time planning, avoiding casual reshapes
* Overlap/halo computations: `map_overlap` for rolling/stencils/windows
* Bag reductions: fold patterns and reduction-tree control (`split_every`)

### [Core 5 — Operational Instrumentation and Safety: Spans, TLS, Shared Clusters](M04.md#core-5--operational-instrumentation-and-safety-spans-tls-shared-clusters)

* Spans: phase-causal tracing for postmortems and perf reports
* TLS basics: when transport security is mandatory
* Shared-cluster guardrails: quotas, fairness, resource pools, autoscaling safety (Gateway tie-in)
