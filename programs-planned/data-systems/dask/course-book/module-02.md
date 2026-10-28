# Module 02: Scalable Analytics — Shuffles, Metadata, and Cost-Controlled Computation

> **Version & scope contract**
> - This module targets **Dask Distributed (2024+) behavior patterns**. Exact defaults and some engine names vary by release; **verify in your deployed version**.
> - Scope: **Production Dask for Scalable Analytics** (DataFrame/Array/Bag + Distributed runtime). Not a full “distributed systems control-plane” survey.

## Table of Contents
- [0. Orientation](#0-orientation)
- [Core 1 — Shuffles](#core-1--shuffles-the-dominant-runtime-and-memory-event)
- [Core 2 — GroupBy Under Skew](#core-2--groupby-and-aggregations-under-skew-correctness--throughput)
- [Core 3 — `map_partitions` in Production](#core-3--map_partitions-as-the-production-knife-metadata-coherence)
- [Core 4 — Array + Bag Pipelines](#core-4--array--bag-pipelines-when-dataframes-are-the-wrong-tool)
- [Core 5 — Partition and Chunk Sizing](#core-5--partitionchunk-sizing-the-practical-performance-lever)
- [Appendix A — Lab Setup](#appendix-a--lab-setup)
- [Appendix B — Patterns and Anti-patterns](#appendix-b--patterns-and-anti-patterns)
- [Appendix C — Exercises](#appendix-c--exercises)
- [Further Reading (Official Docs Map)](#further-reading-official-docs-map)

---

## 0. Orientation

Module 01 gave the runtime contract: **lazy graphs, fixed task overhead, stage boundaries**.  
Module 02 is what breaks pipelines in practice: analytics operations that require **global coordination**.

### 0.1 Two dominant failure modes

1) **Shuffle pain**: global redistribution dominates wall time and peak memory.  
2) **Metadata pain**: dtype/schema drift breaks execution or forces slow, conservative paths.

Your design target is operational:

- **shuffle-thrifty**: few shuffles, minimal bytes moved, balanced keys,
- **metadata-stable**: explicit schema contracts at UDF boundaries,
- **memory-safe**: no uncontrolled shuffle-buffer amplification,
- **shape-disciplined**: no repartition ping-pong.

### 0.2 Global-work checklist (run this before running code)

Whenever you write `groupby`, `merge/join`, `set_index`, `sort_values`:

1) **Width**: which columns will move? project now.  
2) **Rows**: can you filter or pre-aggregate before the global step?  
3) **Key quality**: skew? cardinality? does it balance?  
4) **Partition geometry**: are partitions tiny/fragmented? too many participants?  
5) **Stage boundary**: will you reuse the post-shuffle result? `persist()` (with intent).

---

# Core 1 — Shuffles: The Dominant Runtime and Memory Event

## 1.1 Operational definition (what a shuffle is)

A shuffle is a **many-to-many exchange** to repartition records by key:

- each input partition splits into destination buckets,
- buckets are serialized + transferred,
- destination partitions concatenate buckets,
- downstream tasks run on the new partitioning.

### Shuffle diagram

```mermaid
flowchart LR
  subgraph Inputs
    P1[Partition 1] --> B11[(bucket→A)]
    P1 --> B12[(bucket→B)]
    P2[Partition 2] --> B21[(bucket→A)]
    P2 --> B22[(bucket→B)]
    P3[Partition 3] --> B31[(bucket→A)]
    P3 --> B32[(bucket→B)]
  end

  subgraph Exchange
    B11 --> OA[Output partition A]
    B21 --> OA
    B31 --> OA
    B12 --> OB[Output partition B]
    B22 --> OB
    B32 --> OB
  end
````

Why shuffles dominate:

* **bytes moved** (transfer + (de)serialization),
* **buffering** (peak memory amplification),
* **coordination** (many tasks + dependencies),
* **skew sensitivity** (long-tail stragglers),
* **fragmentation** (many tiny transfers when partitions are too small).

> **Memory reality:** shuffles amplify memory. If workers spill, shuffle buffers and intermediate states can still cause spikes. Design to reduce shuffle payload before relying on spill.

## 1.2 Recognize shuffle triggers immediately

These commonly force shuffles (unless already aligned):

* `groupby(key).agg(...)`
* `merge/join` on non-aligned keys
* `set_index(key)`
* global sorts (`sort_values`, many global top-k patterns)

If you cannot point to the line that triggers the shuffle, you are debugging blind.

## 1.3 Shuffle cost control (four levers, strict priority order)

### Lever A — Reduce width (project early)

```python
import numpy as np
import pandas as pd
import dask.dataframe as dd

pdf = pd.DataFrame({
    "k": np.random.randint(0, 200_000, 5_000_000),
    "v": np.random.randn(5_000_000),
    "junk1": np.random.randn(5_000_000),
    "junk2": np.random.randn(5_000_000),
})
ddf = dd.from_pandas(pdf, npartitions=200)

wide = ddf.groupby("k").sum()                    # shuffles v + junk1 + junk2
narrow = ddf[["k", "v"]].groupby("k").v.sum()    # shuffles only v

# Compare Shuffle bytes + peak memory in dashboard.
# wide.compute()
# narrow.compute()
```

### Lever B — Reduce rows (filter early)

```python
import numpy as np
import pandas as pd
import dask.dataframe as dd

pdf = pd.DataFrame({
    "k": np.random.randint(0, 200_000, 2_000_000),
    "v": np.random.randn(2_000_000),
})
ddf = dd.from_pandas(pdf, npartitions=200)

filtered = ddf[ddf["v"] > 0]
out = filtered[["k", "v"]].groupby("k").v.sum()
# out.compute()
```

### Lever C — Pre-aggregate locally (compress before global combine)

Exactness-preserving for mergeable aggregations (sum/count/min/max/mean via sum+count).

```python
import numpy as np
import pandas as pd
import dask.dataframe as dd

pdf = pd.DataFrame({
    "k": np.random.randint(0, 200_000, 2_000_000),
    "v": np.random.randn(2_000_000),
})
ddf = dd.from_pandas(pdf, npartitions=200)

def local_group_sum(pdf: pd.DataFrame) -> pd.DataFrame:
    return pdf.groupby("k", sort=False)["v"].sum().reset_index()

meta = pd.DataFrame({
    "k": pd.Series([], dtype="int64"),
    "v": pd.Series([], dtype="float64"),
})

partial = ddf[["k", "v"]].map_partitions(local_group_sum, meta=meta)
final = partial.groupby("k").v.sum()

# final.compute()
```

### Lever D — Choose keys deliberately (avoid self-inflicted skew)

Keys drive:

* skew (hot keys),
* cardinality (state size),
* balance (tail latency).

If the key is structurally skewed, you must mitigate skew (Core 2) or accept long tails.

## 1.4 Shuffle engines (disk vs peer-to-peer) and configuration

Many Dask releases provide multiple shuffle implementations (commonly “disk-based” vs “peer-to-peer”). Names and availability vary by version.

Pragmatic guidance:

* **Peer-to-peer**: often higher throughput, fewer scheduler bottlenecks, better tail behavior; requires healthy networking and enough memory headroom.
* **Disk-based**: more forgiving under memory pressure; can be slower; heavier local disk I/O.

**Configuration pattern (verify key names for your version):**

```python
import dask
import dask.dataframe as dd

# Example: choose a shuffle method globally (key names vary by version)
with dask.config.set({"dataframe.shuffle.method": "p2p"}):
    ddf = dd.read_parquet("dataset/")  # example read
    out = ddf.groupby("k").v.sum()
    # out.compute()
```

Dashboard signatures differ (transfer vs disk I/O proportions), but the engineering rule does not change:

> win by reducing shuffle bytes first; then choose the engine that best matches your cluster constraints.

---

# Core 2 — GroupBy and Aggregations Under Skew (Correctness + Throughput)

## 2.1 Mergeable vs non-mergeable aggregations

### Mergeable (decomposable) aggregations

Compute partial state per partition → combine associatively → finalize.

Examples:

* `sum`, `count`, `min`, `max`
* `mean` via `(sum, count)`
* many stats via moments (numerical stability is separate)

These enable local pre-aggregation (Core 1 Lever C).

### Non-mergeable (or expensive-to-merge) aggregations

Canonical example: **exact median / exact quantiles** (exactness typically requires global coordination over all values).

Engineering rule:

* If you need **exact median**, accept that it can be global-costly.
* If you can accept **approximation**, do it explicitly and document the contract.

## 2.2 Skew: why the job “hangs at 99%”

Skew means a few keys own a disproportionate share of rows.

Consequences:

* some destination partitions become huge,
* a few workers become stragglers,
* memory and runtime concentrate on the tail.

## 2.3 Detect skew cheaply

```python
import numpy as np
import pandas as pd
import dask.dataframe as dd

pdf = pd.DataFrame({
    "k": np.random.randint(0, 200_000, 2_000_000),
    "v": np.random.randn(2_000_000),
})
ddf = dd.from_pandas(pdf, npartitions=200)

sample = ddf[["k"]].sample(frac=0.001, random_state=0).compute()
print(sample["k"].value_counts().head(10))
```

## 2.4 Mitigation ladder (apply in order)

### Step 1 — Narrow + filter + local pre-aggregation

Do this first. It reduces both payload and intermediate group state.

### Step 2 — Salting (correct, partition-aware seeding)

**Goal:** split hot keys across buckets, then re-reduce.

Important correction: seeding a RNG identically inside each partition can create correlated patterns. Use **partition-aware seeding**.

```python
import numpy as np
import pandas as pd
import dask.dataframe as dd

pdf = pd.DataFrame({
    "k": np.random.randint(0, 1000, 2_000_000),
    "v": np.random.randn(2_000_000),
})
ddf = dd.from_pandas(pdf, npartitions=200)

def add_salt(pdf: pd.DataFrame, salt_n: int, base_seed: int, partition_info=None) -> pd.DataFrame:
    part = 0 if partition_info is None else int(partition_info["number"])
    seed = base_seed + part  # deterministic and partition-distinct
    rng = np.random.default_rng(seed)

    pdf = pdf.copy()
    pdf["salt"] = rng.integers(0, salt_n, size=len(pdf), endpoint=False)
    return pdf

meta = ddf._meta.assign(salt=np.int64())
salted = ddf.map_partitions(
    add_salt,
    meta=meta,
    salt_n=16,
    base_seed=42,
    partition_info=True,
)

partial = salted.groupby(["k", "salt"]).v.sum().reset_index()
final = partial.groupby("k").v.sum()

# final.compute()
```

### Step 2b — Stable salting without RNG (when you need deterministic, reproducible splits)

Useful when you want salts stable across reruns without relying on RNG streams.

```python
import numpy as np
import pandas as pd
import dask.dataframe as dd

pdf = pd.DataFrame({
    "k": np.random.randint(0, 1000, 2_000_000),
    "v": np.random.randn(2_000_000),
})
ddf = dd.from_pandas(pdf, npartitions=200)

def hash_salt(pdf: pd.DataFrame, salt_n: int, partition_info=None) -> pd.DataFrame:
    part = 0 if partition_info is None else int(partition_info["number"])
    # deterministic per row within partition: (part, position) -> salt bucket
    pos = np.arange(len(pdf), dtype=np.uint64)
    x = (pos ^ np.uint64(part * 0x9E3779B97F4A7C15)) * np.uint64(0xBF58476D1CE4E5B9)
    salt = (x % np.uint64(salt_n)).astype(np.int64)

    pdf = pdf.copy()
    pdf["salt"] = salt
    return pdf

meta = ddf._meta.assign(salt=np.int64())
salted = ddf.map_partitions(hash_salt, meta=meta, salt_n=16, partition_info=True)

partial = salted.groupby(["k", "salt"]).v.sum().reset_index()
final = partial.groupby("k").v.sum()
# final.compute()
```

### Step 3 — Change the question

If one key dominates, no framework makes it cheap. Options:

* aggregate on coarser keys,
* approximate,
* isolate hot keys into a dedicated path.

## 2.5 DataFrame edge knobs: `split_out` and `split_every` (brief but important)

For some groupby reductions, Dask can improve parallel combine behavior by:

* increasing output partitioning (`split_out`) to spread large groupby results,
* controlling tree-reduction fan-in (`split_every`) to reduce intermediate pressure.

These are not “speed buttons.” They are levers you use after:

1. projection/filter/pre-aggregation,
2. skew mitigation.

---

# Core 3 — `map_partitions` as the Production Knife: Metadata Coherence

## 3.1 The contract (why production failures happen)

`map_partitions` runs pandas logic per partition. Distributed concatenation requires:

> same columns, same order, compatible dtypes across all partitions.

If a UDF changes schema/dtypes, declare `meta`. Otherwise, empty partitions and dtype inference will eventually hurt you.

## 3.2 `meta` enforcement: two equivalent styles

### Style A — `make_meta` (schema declared as a contract)

```python
import numpy as np
import pandas as pd
import dask.dataframe as dd
from dask.dataframe.utils import make_meta

pdf = pd.DataFrame({"k": np.arange(10), "v": np.random.randn(10)})
ddf = dd.from_pandas(pdf, npartitions=2)

def enrich(pdf: pd.DataFrame) -> pd.DataFrame:
    pdf = pdf.copy()
    pdf["v2"] = pdf["v"] * pdf["v"]
    pdf["flag"] = pdf["v"] > 0
    return pdf[["k", "v2", "flag"]]

meta = make_meta({"k": "i8", "v2": "f8", "flag": "bool"})
ddf2 = ddf.map_partitions(enrich, meta=meta)
# ddf2.head()
```

### Style B — empty DataFrame with dtypes (useful when you want pandas-native declarations)

```python
import numpy as np
import pandas as pd
import dask.dataframe as dd

pdf = pd.DataFrame({"k": np.arange(10), "v": np.random.randn(10)})
ddf = dd.from_pandas(pdf, npartitions=2)

def local_keep(pdf: pd.DataFrame) -> pd.DataFrame:
    return pdf[["k", "v"]].copy()

meta = pd.DataFrame({
    "k": pd.Series([], dtype="int64"),
    "v": pd.Series([], dtype="float64"),
})

ddf2 = ddf.map_partitions(local_keep, meta=meta)
# ddf2.head()
```

Pick one style and apply it consistently.

## 3.3 `map_overlap`: why it exists (minimal, real example)

Use when a partition needs a halo of neighboring rows (rolling windows, local context). Cost increases: overlap copies data and can amplify memory.

```python
import numpy as np
import pandas as pd
import dask.dataframe as dd

pdf = pd.DataFrame({"x": np.arange(20), "v": np.arange(20, dtype=np.float64)}).set_index("x")
ddf = dd.from_pandas(pdf, npartitions=4)

# Rolling mean of window=3 implemented via overlap (before=2 rows)
rolled = ddf.map_overlap(
    lambda p: p.assign(r=p["v"].rolling(3).mean()),
    before=2,
    after=0,
    meta=ddf._meta.assign(r=np.float64()),
)

# rolled.compute()
```

Requirements you should assume unless proven otherwise:

* index order must be meaningful for your window,
* overlap magnifies memory; keep partitions sized accordingly.

## 3.4 Vectorize inside partitions; avoid row-wise apply

Bad:

```python
bad = ddf.map_partitions(
    lambda pdf: pdf.apply(lambda r: r["v"] * 2 if r["v"] > 0 else 0, axis=1),
    meta=("out", "f8"),
)
```

Good:

```python
good = ddf.map_partitions(
    lambda pdf: (pdf["v"].where(pdf["v"] > 0, 0) * 2),
    meta=("out", "f8"),
)
```

---

# Core 4 — Array + Bag Pipelines (When DataFrames Are the Wrong Tool)

This core exists to prevent category mistakes.

## 4.1 Array: blockwise fusion avoids DataFrame-style shuffles; chunking controls task overhead

```python
import dask.array as da

shape = (100_000, 1024)

x_small = da.random.random(shape, chunks=(500, 1024))      # task explosion
x_large = da.random.random(shape, chunks=(10_000, 1024))   # healthier

m_small = x_small.mean(axis=0)
m_large = x_large.mean(axis=0)

# Compare task count + runtime in dashboard
# m_small.compute()
# m_large.compute()
```

## 4.2 Rechunking warning: rechunk can be a global data movement event

Rechunking changes block boundaries. It can require moving data between workers and can explode task count.

```python
import dask.array as da

x = da.random.random((200_000, 256), chunks=(20_000, 256))
y = x.rechunk((5_000, 256))   # can generate many tasks and data movement

# y.mean().compute()
```

Treat rechunk like a design decision, not a casual tweak.

## 4.3 Bag: schema-free preprocessing defers expensive “relational” costs

```python
import json
import dask.bag as db

raw = db.read_text("logs/*.jsonl").map(json.loads)
clean = raw.filter(lambda r: r.get("status") == "success")

flat = clean.map(lambda r: {"user": r.get("user_id"), "ts": r.get("timestamp"), "v": float(r.get("metric", 0.0))})
# df = flat.to_dataframe(meta={"user": "i8", "ts": "object", "v": "f8"})
```

Bag helps you filter and extract before you pay DataFrame shuffle costs.

---

# Core 5 — Partition/Chunk Sizing: The Practical Performance Lever

## 5.1 Sizing rule-of-thumb (and the real constraint)

Start around **50–200 MiB per partition after projection**. Then calibrate using dashboard **peak memory under representative shuffles/joins**.

The true constraint is:

* post-projection bytes per partition,
* plus peak amplification during global steps.

## 5.2 Measure partition size (bytes, not rows)

```python
import numpy as np
import pandas as pd
import dask.dataframe as dd

pdf = pd.DataFrame({"k": np.random.randint(0, 10_000, 1_000_000), "v": np.random.randn(1_000_000)})
ddf = dd.from_pandas(pdf, npartitions=100)

p0 = ddf.partitions[0].compute()
mib = p0.memory_usage(deep=True).sum() / 1_048_576
print("partition0 (MiB):", round(mib, 2))
```

## 5.3 Partition ping-pong anti-pattern (and rewrite)

Anti-pattern: repeated repartition/shuffle without a clear stage boundary.

```python
import numpy as np
import pandas as pd
import dask.dataframe as dd

pdf = pd.DataFrame({
    "k": np.random.randint(0, 200_000, 2_000_000),
    "v": np.random.randn(2_000_000),
})
ddf = dd.from_pandas(pdf, npartitions=200)

a = ddf.repartition(npartitions=2000)     # fragmentation
b = a.groupby("k").sum()                  # shuffle wide if not projected
c = b.reset_index()                       # extra materialization work
d = c.set_index("k")                      # another shuffle
# d.compute()
```

Rewrite: one deliberate partition sizing step, one deliberate global step, optional stage boundary.

```python
import numpy as np
import pandas as pd
import dask.dataframe as dd

pdf = pd.DataFrame({
    "k": np.random.randint(0, 200_000, 2_000_000),
    "v": np.random.randn(2_000_000),
})
ddf = dd.from_pandas(pdf, npartitions=200)

stage = ddf[["k", "v"]]
stage = stage[stage["v"] > 0]
stage = stage.repartition(partition_size="128MiB")
# stage = stage.persist()  # only if reused downstream

out = stage.groupby("k").v.sum()
# out.compute()
```

---

## Appendix A — Lab Setup

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

## Appendix B — Patterns and Anti-patterns

### Patterns (default behaviors)

* **Narrow before shuffle** (project + filter).
* **Pre-aggregate locally** for mergeable aggregations.
* **Skew-first thinking**: detect skew before “tuning knobs.”
* **Explicit `meta`** for schema/dtype-affecting UDFs.
* **Partition sizing by bytes** (MiB), tuned to peak amplification.
* **One deliberate shuffle per pipeline** when possible.

### Anti-patterns (assume these are bugs)

* Shuffling wide frames “because it’s easier.”
* Groupby on skewed keys without mitigation.
* Conditional schema or implicit dtype inference in `map_partitions`.
* Row-wise apply as a default solution.
* Repartition ping-pong (repartition/set_index repeatedly without reuse justification).

---

## Appendix C — Exercises

1. **Shuffle payload study**
   Add 2–4 junk columns (including one `object` column). Compare wide vs projected groupby. Record shuffle bytes + peak memory.

2. **Skew drill**
   Force 40–60% of rows into one key. Compare baseline groupby vs pre-aggregation vs salting. Identify stragglers in Task Stream.

3. **Metadata failure drill**
   Write a UDF that conditionally creates a column. Observe failure. Fix with stable schema + explicit `meta`.

4. **Rechunk penalty drill (Array)**
   Run the same reduction with stable chunks vs after `rechunk`. Compare task count and runtime.

### Capstone (synthesis)

Build a single pipeline that combines:

* wide columns,
* skewed key,
* a schema-changing UDF.

Fix it strictly in this order:

1. project/filter,
2. local pre-aggregation,
3. skew mitigation (salting only if needed),
4. explicit `meta`,
5. partition sizing discipline.

Write a short postmortem mapping “before vs after” to the cost model:
`shuffle bytes`, `peak memory`, and `task_count × overhead`.

---

## Further Reading (Official Docs Map)

Consult the official docs for your installed version:

* DataFrame shuffles and shuffle configuration (`dataframe.shuffle.*`)
* `groupby` design notes and performance considerations
* `map_partitions`, `meta`, and `make_meta`
* `map_overlap` semantics and caveats
* Array chunking and rechunking guidance
* Dashboard panels: Shuffle, Task Stream, Profile
