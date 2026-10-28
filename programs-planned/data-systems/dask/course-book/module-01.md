# Module 01: First Principles — The Task-Graph Contract

> **Version & scope contract**
> - This module targets **Dask Distributed (2024+) behavior patterns**. Exact defaults and some internals vary by release; **verify in your deployed version**.
> - Scope: **Production Dask for Scalable Analytics** (DataFrame/Array/Bag + Distributed runtime). This is not a full “distributed systems toolkit” survey.

## Table of Contents
- [0. Orientation](#0-orientation)
- [Core 1 — Execution Model](#core-1--execution-model-dags-schedulers--overhead-economics)
- [Core 2 — Right Abstraction](#core-2--picking-the-right-abstraction-delayed-bag-array-dataframe)
- [Core 3 — DataFrame Reality](#core-3--dask-dataframe-reality-partitions-index-divisions-unknown-divisions)
- [Core 4 — Laziness Control](#core-4--laziness-control-compute-persist--graph-optimization)
- [Core 5 — I/O at Scale](#core-5--io-at-scale-dataset-layout-as-a-performance-primitive)
- [Appendix A — Minimal Lab Setup](#appendix-a--minimal-lab-setup)
- [Appendix B — Debugging Playbook](#appendix-b--debugging-playbook-what-you-see--what-it-means)
- [Appendix C — Exercises](#appendix-c--exercises)
- [Further Reading (Official Docs Map)](#further-reading-official-docs-map)

---

## 0. Orientation

**Precise definition:** Dask builds a **lazy** directed acyclic graph (DAG) of tasks and executes it later using a scheduler. High-level collections (DataFrame/Array/Bag) construct **HighLevelGraph** objects (layered graphs) that enable optimization and visualization.

Treat Dask as a **graph compiler + runtime**:
- You write expressions → Dask builds a graph (no work yet).
- Dask rewrites the graph to remove work.
- A scheduler executes tasks and coordinates data movement.

If you build the wrong graph (too many microtasks, unnecessary shuffles, unstable schemas), Dask will execute it faithfully and you will see predictable failure signatures.

### 0.1 Unified cost model (use this to predict failures)

> **Total runtime ≈ compute + I/O + shuffle/network + (task_count × overhead_per_task)**

Every disappointing job is dominated by one term:

1) **Too many tasks** → scheduler overhead dominates (scheduler-bound).  
2) **Too much global movement** → shuffle/network dominates (shuffle-bound).  
3) **Peak memory too high** → spilling/pausing/termination dominates (memory-bound).  
4) **Bad payloads** → serialization + unmanaged memory dominates (payload-bound).

**Pre-flight checklist (before you run):**
- **Task count:** how many tasks/futures will the scheduler coordinate?
- **Shuffle:** does any step require global redistribution by a key?
- **Amplification:** which steps multiply memory (groupby/join/shuffle buffers)?
- **Representation:** are you carrying `object` dtype or Python containers across partitions?

---

# Core 1 — Execution Model: DAGs, Schedulers & Overhead Economics

## 1.1 The contract: build → optimize → execute

### Phase A — Graph construction (client-side, lazy)
- Your code creates a **HighLevelGraph** (HLG): layered symbolic operations.
- No file reads and no heavy computation happen here.
- **Task boundaries are chosen here** (via partitions/chunks and UDF boundaries).

### Phase B — Optimization + lowering (automatic)
- Dask rewrites layers when safe:
  - projection (drop unused columns),
  - fusion (combine adjacent operations),
  - pushdown/pruning (when supported by storage engines).
- Then it lowers HLG layers into concrete tasks (still not executed).

### Phase C — Execution (scheduler-orchestrated)
Triggered by `compute()` or `persist()`:
- Scheduler tracks dependencies and assigns ready tasks to workers.
- Workers execute tasks; data moves when needed (notably during shuffles).
- Results materialize:
  - `compute()` returns to the client,
  - `persist()` stays distributed on workers.

### Renderable flow (graph-first mental model)

```mermaid
flowchart TD
  A[User code: lazy expressions] --> B[HighLevelGraph layers]
  B --> C[Optimize: projection/fusion/pushdown]
  C --> D[Lower to concrete tasks]
  D --> E[Scheduler: readiness + placement]
  E --> F[Workers: execute tasks]
  F --> G[Materialize: compute() to client / persist() on cluster]
````

## 1.2 Demonstration: the graph exists before execution (and layers matter)

```python
import numpy as np
import pandas as pd
import dask.dataframe as dd

pdf = pd.DataFrame({
    "key": np.random.randint(0, 200_000, size=200_000),
    "x": np.arange(200_000, dtype=np.int64),
    "y": np.random.randn(200_000),
})
ddf = dd.from_pandas(pdf, npartitions=50)

expr = (
    ddf[["key", "x", "y"]]
      .assign(z=lambda df: df.x * df.y)
      .query("x % 7 == 0")
      .groupby("key").z.mean()
)

# Still lazy: no execution
print(expr)

g = expr.__dask_graph__()
print("Graph type:", type(g))

# Graph complexity proxy: number of HLG layers (when available)
if hasattr(g, "layers"):
    print("HLG layers:", len(g.layers))
```

**Interpretation:**

* A small output does not imply small work. A single result can require a large DAG.
* Layer count is not “runtime,” but it’s a useful proxy for graph structure and optimization opportunity.

## 1.3 Local vs Distributed schedulers: same semantics, different physics

Scheduler choice changes dispatch latency, data-transfer costs, failure modes, and observability.

| Dimension     | Local schedulers (threaded/processes) | Distributed (`dask.distributed`) |
| ------------- | ------------------------------------- | -------------------------------- |
| Coordination  | in-process                            | scheduler + workers              |
| Data transfer | memory/IPC                            | serialization + network          |
| Failure modes | limited                               | retries, worker loss handling    |
| Diagnostics   | limited                               | dashboard + reports              |
| Small tasks   | less painful                          | saturates earlier                |

**Workflow:**

* Validate correctness locally.
* Validate performance/memory under **Distributed** (even on one machine) because it exposes real coordination and transfer costs.

## 1.4 Overhead economics: why micro-tasks destroy throughput

In Distributed execution, per-task overhead is often **millisecond-scale under load** (order-of-magnitude), so tasks that run in a few milliseconds frequently become scheduler-bound. This is why “more parallelism” can make things slower.

### Lab: micro-task pathology with `delayed`

```python
from dask import delayed

@delayed
def square(i: int) -> int:
    return i * i

N = 200_000
micro = [square(i) for i in range(N)]
total = delayed(sum)(micro)

# Run under distributed + dashboard to see scheduler-bound behavior.
result = total.compute()
print(result)
```

**Expected signature (Task Stream):**

* huge count of ultra-short tasks,
* visible scheduler backlog,
* low sustained worker efficiency.

### Fix: batch work into fewer, larger tasks

```python
from dask import delayed

@delayed
def square_batch(start: int, stop: int) -> int:
    s = 0
    for i in range(start, stop):
        s += i * i
    return s

N = 200_000
batch = 20_000

macro = [square_batch(i, min(i + batch, N)) for i in range(0, N, batch)]
total = delayed(sum)(macro)

result = total.compute()
print(result)
```

**Sanity check:**

* If you’re creating **hundreds of thousands to millions** of tiny tasks, assume scheduler-bound until proven otherwise.
* Prefer tasks that process meaningful bytes (often tens–hundreds of MiB after projection), then tune by measurement.

---

# Core 2 — Picking the Right Abstraction: `delayed`, `bag`, `array`, `dataframe`

## 2.1 What each abstraction is optimized for

| Collection | Best for                                | Semantics Dask can assume         | What this unlocks             | Common failure mode                      |
| ---------- | --------------------------------------- | --------------------------------- | ----------------------------- | ---------------------------------------- |
| DataFrame  | tabular analytics (groupby/join)        | stable schema, partitioned pandas | projection + planned shuffles | accidental shuffles, dtype drift         |
| Array      | dense numeric grids                     | chunked ndarray semantics         | blockwise fusion + reductions | tiny chunks → task explosion             |
| Bag        | semi-structured logs/JSON, text streams | partitions of Python objects      | schema-free map/filter/fold   | heavy serialization, slow relational ops |
| Delayed    | custom orchestration / irregular DAGs   | none                              | arbitrary DAGs                | microtasks, graph blow-ups               |

## 2.2 Boundary hygiene: avoid accidental execution

**Safe inspections (no full compute):**

* `ddf.dtypes`, `ddf.columns`, `ddf.npartitions`, `ddf._meta`

**Bounded execution (acceptable, but still execution):**

* `ddf.partitions[0].compute()` (one partition)
* `ddf.head()` (bounded read; still triggers work)

**Anti-pattern snippet (boundary hygiene failure):**

```python
import numpy as np
import pandas as pd
import dask.dataframe as dd

pdf = pd.DataFrame({"x": np.arange(1_000_000), "y": np.random.randn(1_000_000)})
ddf = dd.from_pandas(pdf, npartitions=200)

# Anti-patterns: can trigger large work unexpectedly
# n = len(ddf)          # often forces a full scan
# pdf2 = ddf.compute()  # forces full materialization on the client
```

### Disciplined partition inspection (and what `deep=True` means)

```python
import numpy as np
import pandas as pd
import dask.dataframe as dd

pdf = pd.DataFrame({"x": np.arange(100_000), "s": ["a"] * 100_000})
ddf = dd.from_pandas(pdf, npartitions=20)

p0 = ddf.partitions[0].compute()

# deep=True includes Python object payloads (strings/object dtype can dominate memory)
mib = p0.memory_usage(deep=True).sum() / 1_048_576
print("Partition 0 size (MiB):", round(mib, 2))
print(p0.dtypes)
```

## 2.3 Collections ↔ futures (one paragraph you must internalize)

High-level collections compile into task graphs; under the Distributed scheduler, concrete tasks are executed and tracked as futures internally. You usually want collections for declarative optimizations (projection/fusion/shuffle planning). You want explicit futures when you need imperative control (streaming, custom orchestration, bounded concurrency). If you express “tabular analytics” as thousands of `client.submit` calls, you usually block the optimizer from doing its job.

## 2.4 Anti-pattern: forcing semi-structured data into DataFrame too early

**Mechanism:** DataFrame enforces schema and dtypes; semi-structured data violates schema early. That pushes expensive parsing and dtype inference across the full dataset before you shrink it.

Correct shape:

1. Bag parse/filter/extract stable fields
2. Convert to DataFrame after volume reduction
3. Store as Parquet for repeatable reads

```python
import json
import dask.bag as db

raw = db.read_text("logs/*.jsonl").map(json.loads)

filtered = raw.filter(lambda r: r.get("event") in {"purchase", "refund"})
flat = filtered.map(lambda r: {
    "user": r.get("user_id"),
    "event": r.get("event"),
    "amount": float(r.get("amount", 0.0)),
})

# Convert only after stabilization (real workloads usually require meta)
# df = flat.to_dataframe(meta={"user": "i8", "event": "object", "amount": "f8"})
```

---

# Core 3 — Dask DataFrame Reality: Partitions, Index, Divisions, Unknown Divisions

## 3.1 Partitions are units of parallelism *and* memory pressure

A partition is the atomic unit for scheduling, memory residency, and shuffle exchange. Partition sizing is a survivability constraint.

**Empirical starting point (calibrate; not a law):**

* Start around **50–200 MiB per partition after projection**, then tune using dashboard peak memory under representative groupby/join/shuffle workloads.

### Measure partition size

```python
import numpy as np
import pandas as pd
import dask.dataframe as dd

pdf = pd.DataFrame({
    "key": np.random.randint(0, 10_000, size=1_000_000),
    "value": np.random.randn(1_000_000),
})
ddf = dd.from_pandas(pdf, npartitions=100)

p0 = ddf.partitions[0].compute()
mib = p0.memory_usage(deep=True).sum() / 1_048_576
print("npartitions:", ddf.npartitions)
print("partition0 (MiB):", round(mib, 2))
```

## 3.2 Divisions: precise definition and why they gate fast paths

`divisions` describes index boundaries per partition. When divisions are known, Dask can route `.loc` and other index-aligned operations to fewer partitions and unlock some optimized paths.

```python
import numpy as np
import pandas as pd
import dask.dataframe as dd

pdf = pd.DataFrame({"x": np.arange(100_000), "v": np.random.randn(100_000)}).set_index("x")
ddf = dd.from_pandas(pdf, npartitions=20)

print("known_divisions:", ddf.known_divisions)
print("divisions (first 5):", ddf.divisions[:5])
```

## 3.3 Unknown divisions: how you get them and what breaks

Filtering and many transformations destroy “provable” partition bounds, so divisions become unknown.

```python
import numpy as np
import pandas as pd
import dask.dataframe as dd

pdf = pd.DataFrame({"x": np.arange(100_000), "v": np.random.randn(100_000)}).set_index("x")
ddf = dd.from_pandas(pdf, npartitions=20)

filtered = ddf[ddf["v"] > 0]
print("known_divisions after filter:", filtered.known_divisions)
```

**Operational consequence:** Dask cannot prune partitions for index-based selection; `.loc` may scan many partitions.

> **Callout: divisions ≠ pruning**
>
> * Divisions are **in-memory index metadata**.
> * Parquet pruning is governed by **storage layout + filters** (partition columns and row-group stats).
>   Divisions do not make your Parquet reads skip files.

## 3.4 `repartition` vs `set_index`: two different cost classes

### `repartition` by size/count: granularity tuning

Used to coalesce/split partitions to manage task count and memory.

```python
balanced = filtered.repartition(partition_size="128MiB")
```

### `set_index`: key-based redistribution (often a shuffle)

Usually requires global data movement. Treat it as a major architectural decision.

```python
import numpy as np
import pandas as pd
import dask.dataframe as dd

pdf = pd.DataFrame({"k": np.random.randint(0, 100_000, 200_000), "v": np.random.randn(200_000)})
ddf = dd.from_pandas(pdf, npartitions=50)

# Expect global redistribution
ddf_ix = ddf.set_index("k")
print("known_divisions:", ddf_ix.known_divisions)
```

Use `set_index` only if you will amortize it across many downstream index-based operations.

---

# Core 4 — Laziness Control: `compute`, `persist` & Graph Optimization

## 4.1 Correct use cases

### `compute()` → return concrete result to the client

Use for small terminal results only.

```python
import numpy as np
import pandas as pd
import dask.dataframe as dd

pdf = pd.DataFrame({"v": np.random.randn(1_000_000)})
ddf = dd.from_pandas(pdf, npartitions=100)

print(ddf.v.mean().compute())
```

### `persist()` → materialize on the cluster and keep distributed

Use to create a reusable stage boundary (avoid recomputation across branches).

```python
import numpy as np
import pandas as pd
import dask.dataframe as dd

pdf = pd.DataFrame({
    "key": np.random.randint(0, 200_000, size=2_000_000),
    "v": np.random.randn(2_000_000),
})
ddf = dd.from_pandas(pdf, npartitions=200)

stage = ddf[["key", "v"]][ddf["v"] > 0].repartition(partition_size="128MiB")
stagep = stage.persist()

a = stagep.groupby("key").v.mean()
b = stagep.groupby("key").v.std()
print(a.compute().head())
print(b.compute().head())
```

### Anti-pattern: “persist is a speed button”

Symptom: you persist huge, wide intermediates unnecessarily and blow worker memory or force spilling.

Rule: persist only when it is a **reused stage boundary** or when it materially reduces graph size/recomputation.

## 4.2 Graph blow-ups: how they happen, how to prevent them

Blow-ups come from:

* deep non-fusible UDF chains,
* Python loops generating tasks,
* branching without persistence.

```python
import numpy as np
import pandas as pd
import dask.dataframe as dd

def bump(pdf: pd.DataFrame) -> pd.DataFrame:
    pdf = pdf.copy()
    pdf["v"] = pdf["v"] + 1
    return pdf

pdf = pd.DataFrame({"v": np.random.randn(1_000_000)})
ddf = dd.from_pandas(pdf, npartitions=100)

layered = ddf
for _ in range(40):
    layered = layered.map_partitions(bump, meta=ddf._meta)

# Branching without persist repeats upstream work
mean_v = layered.v.mean()
std_v = layered.v.std()

# Fix: persist once at the reuse boundary
layered_p = layered.persist()
print(layered_p.v.mean().compute(), layered_p.v.std().compute())
```

## 4.3 Purity discipline: determinism + restart-safe I/O

Tasks may run more than once (retries, worker loss). Therefore:

* task functions must be deterministic,
* writes must be idempotent or transactional.

### Concrete safe-write pattern (unique temp → atomic commit)

```python
import os
import pandas as pd

def write_partition(pdf: pd.DataFrame, out_dir: str, part_id: int) -> str:
    os.makedirs(out_dir, exist_ok=True)
    tmp = os.path.join(out_dir, f"part-{part_id}.tmp.parquet")
    final = os.path.join(out_dir, f"part-{part_id}.parquet")

    pdf.to_parquet(tmp, index=False)
    os.replace(tmp, final)  # atomic replace on most filesystems
    return final

# Usage sketch:
# parts = ddf.to_delayed()
# futures = [client.submit(write_partition, p, "out/", i) for i, p in enumerate(parts)]
```

---

# Core 5 — I/O at Scale: Dataset Layout as a Performance Primitive

## 5.1 Parquet-first: what matters operationally

Parquet enables three independent “skip work” mechanisms:

* **projection** (read fewer columns),
* **predicate pushdown** (skip row groups via stats),
* **partition pruning** (skip directories/files via hive layout).

## 5.2 What gets skipped (and what does not)

### Projection

```python
import dask.dataframe as dd
ddf = dd.read_parquet("dataset/", columns=["key", "value", "date"])
```

### Predicate pushdown

```python
import dask.dataframe as dd
ddf = dd.read_parquet("dataset/", filters=[("value", ">", 0)])
```

### Partition pruning (layout dependent)

Hive layout example:
`dataset/date=2025-12-01/region=EU/part-*.parquet`

```python
import dask.dataframe as dd
ddf = dd.read_parquet("dataset/", filters=[("date", "==", "2025-12-01"), ("region", "==", "EU")])
```

## 5.3 Object-store realities (high-level, but production-relevant)

If your storage is S3/GCS/Azure:

* **Listing and metadata** can dominate (many small files are catastrophic).
* Reads are bandwidth-friendly but latency-sensitive; batchy access patterns win.
* Partition pruning helps only if your partitioning aligns with common filters.

Practical implication: “avoid small files” becomes even more important on object stores than on local disks.

## 5.4 Writing strategy: avoid small files, stabilize schema, choose sane partition keys

```python
import numpy as np
import pandas as pd
import dask.dataframe as dd

pdf = pd.DataFrame({
    "date": pd.to_datetime("2025-12-01") + pd.to_timedelta(np.random.randint(0, 30, size=2_000_000), unit="D"),
    "region": np.random.choice(["EU", "US", "APAC"], size=2_000_000),
    "key": np.random.randint(0, 200_000, size=2_000_000),
    "value": np.random.randn(2_000_000),
})
ddf = dd.from_pandas(pdf, npartitions=200)

prepared = ddf[["date", "region", "key", "value"]].repartition(partition_size="256MiB")

prepared.to_parquet(
    "processed/",
    partition_on=["date", "region"],   # low/moderate cardinality keys
    write_metadata_file=True,
    compression="snappy",
)
```

Partition keys should be:

* low/moderate cardinality (avoid directory explosion),
* common filter predicates,
* not severely skewed.

---

## Appendix A — Minimal Lab Setup

Use Distributed even on one machine to observe real overhead, serialization, memory behavior, and dashboard signals.

```python
from dask.distributed import Client, LocalCluster

cluster = LocalCluster(
    n_workers=4,
    threads_per_worker=1,
    processes=True,
    memory_limit="4GiB",
    dashboard_address=":8787",
)
client = Client(cluster)
client
```

---

## Appendix B — Debugging Playbook: what you see → what it means

| Observation               | Dominant term in cost model | Primary cause                                     | First fixes (in order)                                    |
| ------------------------- | --------------------------- | ------------------------------------------------- | --------------------------------------------------------- |
| Many tiny tasks (<~50ms)  | task_count × overhead       | too-fine partitions/chunks, micro-delayed         | coalesce/repartition larger → fuse ops → batch            |
| Shuffle dominates runtime | shuffle/network             | wide data, high volume, poor key choice           | project/filter → pre-aggregate → mitigate skew            |
| Memory spikes/spill/pause | peak amplification          | shuffle buffers, join/groupby state, object dtype | narrow columns → tune partitions → remove object dtype    |
| “Stuck near 99%”          | stragglers                  | skew/hot keys, uneven partitions                  | detect skew → salt/two-phase reduce → adjust partitioning |
| High network, low CPU     | serialization/transfer      | object-heavy payloads, fragmented partitions      | consolidate → reduce object dtype → simplify payload      |

---

## Appendix C — Exercises

1. **Granularity sweep (evidence-based)**
   Run the same groupby with `npartitions` in {50, 200, 2000}. Record:

* wall time, task count proxy (graph size), shuffle bytes, peak memory (dashboard).
  Explain which cost term dominates in each run.

2. **Width impact (quantify shuffle)**
   Add 3–5 unused columns (including one `object` column). Compare:

* groupby with early projection vs without projection.
  Quantify shuffle bytes and runtime.

3. **Skew stress test (straggler diagnosis)**
   Force 40% of rows to share one `key`. Compare baseline groupby vs salted two-phase aggregation.
   Explain the “stuck near end” signature and how it changes.

4. **Capstone (synthesis): graph blow-up + persist boundary**
   Build a 40-layer `map_partitions` chain, branch into two downstream computations:

* observe recomputation without `persist`,
* fix with one `persist` at the reuse boundary,
* report changes in task stream and wall time.

---

## Further Reading (Official Docs Map)

Use these doc areas as canonical references (titles only; consult your installed version):

* High-level graphs / HighLevelGraph
* Scheduling overview (local vs distributed)
* Distributed efficiency (task granularity guidance)
* DataFrame divisions and known_divisions
* DataFrame best practices (partitioning, shuffles, diagnostics)
* Parquet I/O and filtering (projection/pushdown/pruning)
