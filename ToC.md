# Dask Deep Dive

## Module 01: First Principles — The Task-Graph Contract

### 01. Execution Model: DAGs, Schedulers, and Overhead Economics

* Dask is a **DAG executor**, not “parallel pandas”
* Local schedulers vs Distributed scheduler: what truly changes (latency, coordination, failure modes)
* Overhead model: task count, granularity, and why micro-tasks destroy throughput
* **Diagram:** *User pipeline → task graph → scheduler → workers (execution timeline)*

### 02. Picking the Right Abstraction: `delayed`, `bag`, `array`, `dataframe`

* What each collection is optimized for (tabular vs irregular vs numeric grids vs custom graphs)
* Boundary hygiene: converting collections without accidental `compute()`
* Anti-pattern: forcing semi-structured data into DataFrame too early

### 03. Dask DataFrame Reality: Partitions, Index, Divisions, Unknown Divisions

* Partitions as units of parallelism *and* memory pressure
* Divisions: why they gate slicing, joins, and many “fast-path” behaviors
* **Unknown divisions**: how you get them, how to detect them, and why they trigger worst-case execution
* `repartition`, `set_index`, and the shuffle cost model (full data movement triggers)

### 04. Laziness Control: `compute`, `persist`, and Graph Optimization

* `compute()` vs `persist()` vs “leave it lazy”: correct use cases and failure patterns
* Fusion/inlining, graph blow-ups (too many tasks, too big graphs), and how to prevent them
* Purity discipline: side effects, determinism, and restart-safe computation

### 05. I/O at Scale: Dataset Layout as a Performance Primitive

* Parquet-first: partitioned datasets, row groups, metadata, file sizing
* Projection/predicate pushdown + partition pruning (what actually gets skipped)
* Writing strategy: avoid small files, stable schemas, partition keys that won’t skew

## Module 02: Scalable Analytics — Shuffles, Metadata, and Cost-Controlled Computation

### 01. Shuffles: The Dominant Runtime and Memory Event

* What a shuffle is (and why it dominates)
* Ops that force shuffles: `groupby`, `join`, `set_index`, many sorts
* Cost control: reduce width early, filter early, pre-aggregate, choose keys deliberately

### 02. GroupBy and Aggregations Under Skew (Correctness + Throughput)

* Reductions vs custom aggregations; combining partials (tree-reduction thinking)
* Hot keys/skew: detection and mitigation (salting, pre-aggregation, alternative keys)
* Avoiding accidental global work (implicit sorts, unnecessary repartitions)

### 03. `map_partitions` as the Production Knife: Metadata Coherence

* `map_partitions`, `map_overlap`, and defining safe UDF boundaries
* **Metadata coherence**: why dtype/schema drift becomes distributed failure
* `meta=` done correctly; hardening with `dask.dataframe.utils.make_meta`
* Rule: vectorize inside partitions; avoid row-wise `apply` unless you accept the cost

### 04. Array + Bag Pipelines (When DataFrames Are the Wrong Tool)

* Dask Array chunking: shape-driven performance; avoiding tiny chunks
* Bag for logs/JSON/semi-structured streams; principled normalization to DataFrame
* Mixed pipelines: bag → dataframe → parquet (and where shuffles enter)

### 05. Partition/Chunk Sizing: The Practical Performance Lever

* Sizing rule-of-thumb: **~50–200MB per partition**, tuned to worker memory and workload
* Coalesce vs repartition: overhead vs parallelism vs shuffle pressure
* Pipeline shape: avoid repeated reshuffles and wide materialized intermediates

## Module 03: Production Dask — Distributed Runtime, Diagnostics, and Deployment

### 01. Distributed Runtime: Client, Workers, Futures, Orchestration

* Collections vs futures: when futures are the right control plane
* Threads vs processes; GIL implications; locality and network transfer costs
* Orchestration patterns: `client.submit`, `wait`, `as_completed` for non-collection workflows

### 02. Memory, Spilling, and Survival Engineering

* Worker memory lifecycle: managed memory, spilling, pausing, killing
* Failure modes: serialization bloat, shuffle buffers, runaway graphs, long-tail stragglers
* Mitigation playbook: right-size partitions, selective `persist`, reduce shuffle width, simplify graphs

### 03. Diagnostics: Reading the Dashboard Like an Engineer

* Task stream, graph view, progress, memory/CPU, shuffle panels
* Diagnosing: too many tasks, skew, blocked shuffles, poor fusion, network saturation
* Profiling inside tasks: separating Python/pandas cost from scheduling/I/O cost

### 04. Deployment: Local → HPC → Kubernetes/Cloud

* LocalCluster vs managed clusters; reproducible environments
* SLURM patterns (jobqueue), K8s patterns, storage realities (shared FS vs object store)
* Adaptive scaling for cost control and responsiveness

### 05. Engineering Practice: Contracts, Testing, and When Not to Use Dask

* Test partition functions locally + minimal distributed integration tests
* Determinism/idempotence at I/O edges; restart-safe pipelines
* Decision boundaries: when Spark, Polars, DuckDB, Ray (or plain pandas) is the better choice
