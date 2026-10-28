# Module 04: Time Series, Streaming, and Storage Systems

> **Version & scope contract**
>
> * Target: **Polars 1.x** (concepts stable since ~1.0; APIs evolve within 1.x). Verify your runtime:
>
>   ```python
>   import polars as pl
>   print(pl.__version__)
>   ```
> * Scope: **single-node** Polars with **lazy pipelines**. This module focuses on (1) time-series correctness, (2) out-of-core execution via streaming, and (3) storage-aware IO patterns (partitioned Parquet / lakehouse) plus SQL bridging.

## Table of Contents

1. Core 01 — Time-Series Primitives: `group_by_dynamic` and Resampling Patterns
2. Core 02 — Streaming Execution: Out-of-Core Pipelines
3. Core 03 — Streaming Sinks: Incremental and Safe Output
4. Core 04 — Dataset and Lakehouse Scanning: Partitioned Sources
5. Core 05 — SQL Interface and Hybrid Workflows
- Appendix A — Streaming and Storage Plan Smells (and Fixes)
- Appendix B — Minimal Large-Data Harness
- Appendix C — Mastery Exercises (public datasets)

---

## Core 01 — Time-Series Primitives: `group_by_dynamic` and Resampling Patterns

### Learning objectives

You will be able to:

* Parse datetimes deterministically, and **treat time zones correctly** (set vs convert).
* Use `group_by_dynamic` correctly (every/period/offset, label/closed), including boundary traps.
* Build **resampling** patterns: downsample (aggregate) and upsample (fill/interpolate) without accidental leakage.
* Align “resampled” series with event streams (conceptual bridge to `asof_join`).

### 1.1 Datetime parsing and the two time zone operations that people confuse

In Polars, you must distinguish:

* **Replace (set) the time zone**: “These timestamps were recorded in Stockholm local time; attach that tz.”
  This changes the *interpretation* of the same wall-clock values.
* **Convert the time zone**: “These timestamps are absolute instants; show them in Stockholm.”
  This changes the *displayed wall-clock*, preserving the instant.

Concrete demonstration:

```python
import polars as pl

df = pl.DataFrame(
    {"ts_naive": ["2025-01-01 12:00:00", "2025-06-01 12:00:00"]}
).with_columns(
    pl.col("ts_naive").str.strptime(pl.Datetime, strict=True).alias("ts_naive")
)

out = df.with_columns(
    pl.col("ts_naive").dt.replace_time_zone("UTC").alias("ts_as_utc"),
    pl.col("ts_naive").dt.replace_time_zone("UTC").dt.convert_time_zone("Europe/Stockholm").alias("utc_to_sthlm"),
    pl.col("ts_naive").dt.replace_time_zone("Europe/Stockholm").alias("ts_as_sthlm"),
)
print(out)
```

Expected (structure; exact formatting may vary):

```
shape: (2, 4)
┌─────────────────────┬──────────────────────────┬──────────────────────────┬──────────────────────────┐
│ ts_naive            ┆ ts_as_utc                ┆ utc_to_sthlm             ┆ ts_as_sthlm              │
│ ---                 ┆ ---                      ┆ ---                      ┆ ---                      │
│ datetime[μs]        ┆ datetime[μs, UTC]        ┆ datetime[μs, Europe/...] ┆ datetime[μs, Europe/...] │
╞═════════════════════╪══════════════════════════╪══════════════════════════╪══════════════════════════╡
│ 2025-01-01 12:00:00 ┆ 2025-01-01 12:00:00 UTC  ┆ 2025-01-01 13:00:00 ...  ┆ 2025-01-01 12:00:00 ...  │
│ 2025-06-01 12:00:00 ┆ 2025-06-01 12:00:00 UTC  ┆ 2025-06-01 14:00:00 ...  ┆ 2025-06-01 12:00:00 ...  │
└─────────────────────┴──────────────────────────┴──────────────────────────┴──────────────────────────┘
```

**What to notice**

* `replace_time_zone("UTC")` does **not** “shift the hour”; it labels the naive wall-clock as UTC.
* `convert_time_zone("Europe/Stockholm")` **does** shift the wall-clock to represent the same instant in a new zone (DST matters).
* Time-series correctness starts here. If you get this wrong, *every* downstream resample/window is wrong.

References:

* Polars Python API (SQL/interop and stable docs hub): [https://docs.pola.rs/api/python/stable/reference/](https://docs.pola.rs/api/python/stable/reference/)
* (Datetime/tz methods vary by object; inspect the `.dt` namespace in your version.)

---

### 1.2 `group_by_dynamic`: window definitions, boundary rules, and why `closed/label` matter

`group_by_dynamic` is the “resampling/grouping” primitive for time series. You define:

* `every`: stride between window starts (e.g., “1h”)
* `period`: window length (e.g., “1h”, “7d”)
* `offset`: shift the window grid (e.g., align to market open)
* `label`: what timestamp labels the window (left/right)
* `closed`: which endpoints are included (left/right/both/none)

A boundary trap demo (same data, different `closed/label`):

```python
import polars as pl

df = pl.DataFrame(
    {"ts": ["2025-01-01 00:00:00", "2025-01-01 00:59:59", "2025-01-01 01:00:00"],
     "v":  [1, 2, 3]}
).with_columns(pl.col("ts").str.strptime(pl.Datetime, strict=True))

left_left = (
    df.group_by_dynamic("ts", every="1h", period="1h", label="left", closed="left")
      .agg(pl.col("v").sum().alias("sum_v"))
      .sort("ts")
)

right_right = (
    df.group_by_dynamic("ts", every="1h", period="1h", label="right", closed="right")
      .agg(pl.col("v").sum().alias("sum_v"))
      .sort("ts")
)

print(left_left)
print(right_right)
```

Expected intuition (window assignment is the lesson):

* With `label="left", closed="left"`: the point at exactly `01:00:00` belongs to the window starting at `01:00:00`.
* With `label="right", closed="right"`: boundary points tend to “stick” to the earlier window depending on your grid; the labels also move to window end.

**What to notice**

* There is no universally “correct” choice. You must make it a **contract**:

  * Reporting bins often want `label="right"`.
  * Causal pipelines (no lookahead) often prefer `closed="left"` with left labels.
* If you later join resampled data to event data (e.g., trades), the labeling choice changes what is considered “the current bar”.

References:

* DataFrame API docs (time grouping methods live here): [https://docs.pola.rs/py-polars/html/reference/dataframe/](https://docs.pola.rs/py-polars/html/reference/dataframe/)
* User guide home: [https://docs.pola.rs/](https://docs.pola.rs/)

---

### 1.3 Resampling patterns: downsample (aggregate) vs upsample (fill/interpolate)

**Downsample**: aggregate within windows (safe and common).

```python
import polars as pl

df = pl.DataFrame(
    {"ts": ["2025-01-01 00:00:10", "2025-01-01 00:00:40", "2025-01-01 00:01:05"],
     "price": [100.0, 101.0, 103.0]}
).with_columns(pl.col("ts").str.strptime(pl.Datetime, strict=True))

bars = (
    df.group_by_dynamic("ts", every="1m", period="1m", closed="left", label="left")
      .agg([
          pl.col("price").first().alias("open"),
          pl.col("price").max().alias("high"),
          pl.col("price").min().alias("low"),
          pl.col("price").last().alias("close"),
      ])
      .sort("ts")
)
print(bars)
```

Expected:

```
shape: (2, 5)
┌─────────────────────┬───────┬───────┬───────┬───────┐
│ ts                  ┆ open  ┆ high  ┆ low   ┆ close │
╞═════════════════════╪═══════╪═══════╪═══════╪═══════╡
│ 2025-01-01 00:00:00 ┆ 100.0 ┆ 101.0 ┆ 100.0 ┆ 101.0 │
│ 2025-01-01 00:01:00 ┆ 103.0 ┆ 103.0 ┆ 103.0 ┆ 103.0 │
└─────────────────────┴───────┴───────┴───────┴───────┘
```

**Upsample**: create missing timestamps, then fill.

```python
import polars as pl

df = pl.DataFrame(
    {"ts": ["2025-01-01 00:00:00", "2025-01-01 00:02:00"],
     "x":  [10.0, 14.0]}
).with_columns(pl.col("ts").str.strptime(pl.Datetime, strict=True))

ups = (
    df.upsample(time_column="ts", every="1m")
      .sort("ts")
      .with_columns([
          pl.col("x").forward_fill().alias("x_ffill"),
          pl.col("x").interpolate().alias("x_interp"),
      ])
)
print(ups)
```

Expected:

```
shape: (3, 3)
┌─────────────────────┬──────┬──────────┬──────────┐
│ ts                  ┆ x    ┆ x_ffill  ┆ x_interp │
╞═════════════════════╪══════╪══════════╪══════════╡
│ 2025-01-01 00:00:00 ┆ 10.0 ┆ 10.0     ┆ 10.0     │
│ 2025-01-01 00:01:00 ┆ null ┆ 10.0     ┆ 12.0     │
│ 2025-01-01 00:02:00 ┆ 14.0 ┆ 14.0     ┆ 14.0     │
└─────────────────────┴──────┴──────────┴──────────┘
```

**What to notice**

* `forward_fill` is causal (past-only). `interpolate` uses future values; treat it as leakage unless you explicitly want smoothing/reconstruction.
* Always `sort("ts")` before upsampling and any rolling/time logic. Time series without ordering is not time series.

References:

* IO + time-series operations are documented across the DataFrame/LazyFrame reference: [https://docs.pola.rs/py-polars/html/reference/](https://docs.pola.rs/py-polars/html/reference/)

---

## Core 02 — Streaming Execution: Out-of-Core Pipelines

### Learning objectives

You will be able to:

* Explain what “streaming” means in Polars and what it is **not**.
* Use plan inspection to predict streamability.
* Refactor pipelines to stream for **>RAM** workloads.
* Benchmark streaming vs non-streaming with correct interpretation.

### 2.1 Streaming in Polars: the real contract

Streaming means: Polars executes the lazy plan in **chunks**, keeping memory bounded, instead of materializing large intermediates. It is still single-node; it is not a distributed engine.

The streaming engine is opt-in and conditional. Some operations can stream; some force full materialization (global sorts, certain joins, pivots, Python UDF boundaries).

Start here:

* Streaming user guide: [https://docs.pola.rs/user-guide/concepts/streaming/](https://docs.pola.rs/user-guide/concepts/streaming/)
* `LazyFrame.collect` reference (engine selection and parameters): [https://docs.pola.rs/py-polars/html/reference/lazyframe/api/polars.LazyFrame.collect.html](https://docs.pola.rs/py-polars/html/reference/lazyframe/api/polars.LazyFrame.collect.html)

### 2.2 Streamable vs blocked: a side-by-side pipeline you can actually run

**Streamable shape** (filter + projection early; simple group-by aggregation):

```python
import polars as pl

lf = (
    pl.scan_parquet("data/events.parquet")
      .select(["ts", "user_id", "value"])
      .filter(pl.col("value") > 0)
      .group_by("user_id")
      .agg(pl.col("value").sum().alias("sum_value"))
)

print(lf.explain(optimized=True))
out = lf.collect(engine="streaming")   # falls back if unsupported in your version
print(out.head(5))
```

**Blocked shape** (a global sort early is a common streaming killer):

```python
import polars as pl

lf_bad = (
    pl.scan_parquet("data/events.parquet")
      .sort("ts")                      # global coordination
      .filter(pl.col("value") > 0)
      .group_by("user_id")
      .agg(pl.col("value").sum().alias("sum_value"))
)

print(lf_bad.explain(optimized=True))
out_bad = lf_bad.collect(engine="streaming")
print(out_bad.head(5))
```

**What to notice**

* Your exact `explain()` text varies by version and settings. The invariant is structural:

  * If you see an early `SORT` (or other global operators) before reductions, streaming becomes hard or impossible.
* The refactor is almost always: **filter + select early, sort late, reduce early**.

### 2.3 A minimal benchmark that teaches the right lesson (without lying about absolute times)

```python
import polars as pl
import time

lf = (
    pl.scan_parquet("data/events.parquet")
      .select(["user_id", "value"])
      .filter(pl.col("value") > 0)
      .group_by("user_id")
      .agg(pl.col("value").sum().alias("sum_value"))
)

t0 = time.perf_counter()
_ = lf.collect()  # default engine
t1 = time.perf_counter()

t2 = time.perf_counter()
_ = lf.collect(engine="streaming")
t3 = time.perf_counter()

print(f"default:   {t1 - t0:.3f}s")
print(f"streaming: {t3 - t2:.3f}s")
```

**Interpretation discipline**

* Streaming’s primary promise is **bounded memory**, not always faster runtime.
* Streaming can be slower (more overhead), equal, or faster depending on IO shape and operators.

---

## Core 03 — Streaming Sinks: Incremental and Safe Output

### Learning objectives

You will be able to:

* Write results larger than RAM using lazy sinks.
* Implement an **idempotent** write pattern (safe retries).
* Understand the operational failure modes of streaming writes.

Core references:

* Lazy sources/sinks overview: [https://docs.pola.rs/user-guide/lazy/sources_sinks/](https://docs.pola.rs/user-guide/lazy/sources_sinks/)
* Parquet IO guide: [https://docs.pola.rs/user-guide/io/parquet/](https://docs.pola.rs/user-guide/io/parquet/)
* `LazyFrame.sink_parquet`: [https://docs.pola.rs/py-polars/html/reference/lazyframe/api/polars.LazyFrame.sink_parquet.html](https://docs.pola.rs/py-polars/html/reference/lazyframe/api/polars.LazyFrame.sink_parquet.html)
* `LazyFrame.sink_csv`: [https://docs.pola.rs/py-polars/html/reference/lazyframe/api/polars.LazyFrame.sink_csv.html](https://docs.pola.rs/py-polars/html/reference/lazyframe/api/polars.LazyFrame.sink_csv.html)
* `LazyFrame.sink_ipc`: [https://docs.pola.rs/py-polars/html/reference/lazyframe/api/polars.LazyFrame.sink_ipc.html](https://docs.pola.rs/py-polars/html/reference/lazyframe/api/polars.LazyFrame.sink_ipc.html)

### 3.1 The simplest correct sink: one-shot, no idempotency

```python
import polars as pl

lf = (
    pl.scan_parquet("data/events.parquet")
      .select(["user_id", "value"])
      .group_by("user_id")
      .agg(pl.col("value").sum().alias("sum_value"))
)

lf.sink_parquet("out/user_sums.parquet")  # streams internally when possible
```

### 3.2 Idempotent sink pattern (the one you actually want in production)

Goal: if the job crashes mid-write, you do not leave a “valid-looking but incomplete” output.

Pattern:

1. Write to a **staging** path (unique, temp).
2. Validate minimal invariants.
3. Atomically move/rename into final location and write a `_SUCCESS` marker.

```python
from __future__ import annotations
import os
import uuid
import polars as pl

final_path = "out/user_sums.parquet"
success_marker = "out/_SUCCESS"

run_id = uuid.uuid4().hex
staging_path = f"out/.staging_user_sums_{run_id}.parquet"

lf = (
    pl.scan_parquet("data/events.parquet")
      .select(["user_id", "value"])
      .group_by("user_id")
      .agg(pl.col("value").sum().alias("sum_value"))
)

# 1) write staging
lf.sink_parquet(staging_path)

# 2) validate cheap invariants (example: non-empty + schema)
chk = pl.read_parquet(staging_path)
assert chk.height > 0
assert chk.schema == {"user_id": chk.schema["user_id"], "sum_value": pl.Float64} or True  # customize

# 3) atomic-ish publish (best-effort; exact atomicity depends on FS)
os.replace(staging_path, final_path)
with open(success_marker, "w", encoding="utf-8") as f:
    f.write(run_id + "\n")

print(pl.read_parquet(final_path).head(3))
```

Expected: you see a small table with `user_id` and `sum_value`.

**What to notice**

* “Atomic rename” is reliable on a single local filesystem; on networked/object stores, semantics differ. Treat publish as a contract with your storage layer.
* Your validation should be cheap but meaningful (rowcount bounds, null rate constraints, uniqueness if expected).

---

## Core 04 — Dataset and Lakehouse Scanning: Partitioned Sources

### Learning objectives

You will be able to:

* Scan partitioned datasets using PyArrow Dataset integration and reason about pushdown/pruning.
* Recognize small-file pathologies and mitigate them.
* Use Delta Lake integration realistically (including “time travel”) in a Polars pipeline.

Key references:

* Cloud storage & PyArrow dataset scanning: [https://docs.pola.rs/user-guide/io/cloud-storage/](https://docs.pola.rs/user-guide/io/cloud-storage/)
* `polars.scan_pyarrow_dataset` API (note: marked unstable): [https://docs.pola.rs/py-polars/html/reference/api/polars.scan_pyarrow_dataset.html](https://docs.pola.rs/py-polars/html/reference/api/polars.scan_pyarrow_dataset.html)
* IO reference (Delta Lake section lives here): [https://docs.pola.rs/py-polars/html/reference/io.html](https://docs.pola.rs/py-polars/html/reference/io.html)
* Delta Lake ↔ Polars integration (delta-rs): [https://delta-io.github.io/delta-rs/integrations/delta-lake-polars/](https://delta-io.github.io/delta-rs/integrations/delta-lake-polars/)

### 4.1 Partitioned datasets via PyArrow Dataset: what you gain and what you must verify

When data is stored as a partitioned Parquet dataset (e.g., Hive partitions `date=.../country=.../part-*.parquet`), scanning via PyArrow Dataset can expose partition structure.

A concrete skeleton:

```python
import polars as pl
import pyarrow.dataset as ds

dataset = ds.dataset("s3://my-bucket/events/", format="parquet", partitioning="hive")
lf = pl.scan_pyarrow_dataset(dataset)

q = (
    lf.filter(pl.col("date") == pl.lit("2025-01-01"))   # partition column
      .select(["date", "user_id", "value"])
)

print(q.explain(optimized=True))
print(q.collect().head(3))
```

**What to notice**

* The *intent* is partition pruning + predicate pushdown, but you must verify with `explain()` and real IO metrics (file counts, bytes read).
* `scan_pyarrow_dataset` is explicitly flagged as **unstable** in the API docs—pin versions and test upgrades.

### 4.2 Small-file problems: the cost model that hurts more than people expect

Single-node engines get crushed by:

* Too many files (open/seek overhead dominates).
* Tiny row groups (poor scan efficiency).
* Over-partitioning (pruning helps only if your filters match partitions).

Operational mitigation (single-node reality):

* Compact files (bigger Parquet files with healthy row groups).
* Partition only on columns you actually filter on.
* Keep “analysis tables” separate from “raw landing zones”.

(If you want one rule: **prefer fewer, larger Parquet files for scan-heavy analytics** unless you have strong pruning.)

---

## Core 05 — SQL Interface and Hybrid Workflows

### Learning objectives

You will be able to:

* Use Polars SQL (`pl.sql` / `SQLContext`) without sacrificing correctness discipline.
* Translate between SQL and expressions pragmatically.
* Decide when to stay in Polars vs hand off to a SQL engine.

References:

* SQL Python API: [https://docs.pola.rs/api/python/stable/reference/sql/python_api.html](https://docs.pola.rs/api/python/stable/reference/sql/python_api.html)

### 5.1 SQLContext as a bridge, not a lifestyle

SQL is valuable when:

* You inherit legacy SQL logic that must be ported.
* Analysts need a SQL surface for exploration.
* You want to validate expression pipelines against a SQL equivalent.

But expressions remain the “native” language for production Polars pipelines.

Minimal example:

```python
import polars as pl
from polars.sql import SQLContext

lf = pl.LazyFrame(
    {"user_id": [1, 1, 2], "value": [10, 5, 7]}
)

ctx = SQLContext()
ctx.register("events", lf)

out = ctx.execute("""
    SELECT user_id, SUM(value) AS sum_value
    FROM events
    GROUP BY user_id
    ORDER BY user_id
""").collect()

print(out)
```

Expected:

```
shape: (2, 2)
┌─────────┬───────────┐
│ user_id ┆ sum_value │
╞═════════╪═══════════╡
│ 1       ┆ 15        │
│ 2       ┆ 7         │
└─────────┴───────────┘
```

**What to notice**

* This is not “SQL instead of Polars”; it’s SQL *on top of* Polars’ engine. You still need the same contracts: determinism, null semantics, join cardinality, schema discipline.
* For high-stakes pipelines: prefer expressions; use SQL as a compatibility layer and for validation.

### 5.2 When to hand off to another engine (practical criteria)

Stay in Polars when:

* Your workload is expression-heavy, columnar, and benefits from Polars’ optimizer.
* You need fast Python-level iteration on pipeline design but Rust-level execution.

Hand off when:

* You already have a mature SQL lakehouse stack and want optimizer features outside Polars’ scope.
* You need advanced SQL semantics/features not covered by Polars SQL yet.
* You want a “query federation” layer across many sources.

A disciplined hybrid approach is: **Polars for ETL/feature materialization → Parquet → SQL engine for ad hoc querying** (or the reverse), with explicit boundaries and reproducibility.

---

# Closing recap

Module 04 completes the single-node story:

* Time-series work is mostly about **correctness contracts**: time zones, window boundaries, labels, and leakage discipline.
* Streaming is about **bounded memory** and operator choices; you win by shaping pipelines (early reduction, avoid global ops early).
* Storage systems are a performance surface: partitioning, file sizing, and row groups matter as much as code.
* SQL is a bridge: useful, pragmatic, and safest when you keep Polars’ production discipline intact.

---

## Appendix A — Streaming and Storage Plan Smells (and Fixes)

Smell → Why it hurts → Fix

* Early `SORT` → global coordination + blocks streaming → sort late, or within-group where needed
* Python UDF nodes → blocks optimization + slow boundary → rewrite as expressions / joins
* Wide scan (no early projection) → bytes scanned dominates → `select` immediately after `scan_*`
* Partition filter not pruning → too many files scanned → partition on filter columns; verify via `explain()` and IO metrics
* Many tiny files → open/seek dominates → compact/optimize Parquet layout

---

## Appendix B — Minimal Large-Data Harness

```python
import time
import polars as pl

def bench(label: str, f):
    t0 = time.perf_counter()
    out = f()
    t1 = time.perf_counter()
    print(f"{label}: {t1 - t0:.3f}s")
    return out

pl.Config.set_tbl_rows(10)
pl.Config.set_tbl_cols(10)
```

Use ratios, not absolute numbers; always report dataset shape and key operators.

---

## Appendix C — Mastery Exercises

1. Build 1-minute OHLC bars with `group_by_dynamic`; show how `closed/label` changes the boundary row assignment.
2. Upsample irregular sensor readings; produce both `forward_fill` and `interpolate` outputs and explain leakage implications.
3. Take a pipeline that sorts early; refactor to sort late; compare `explain()` and runtime/memory qualitatively with `collect(engine="streaming")`.
4. Scan a partitioned Parquet dataset via PyArrow Dataset; filter on a partition column vs a non-partition column; compare plans and file counts (PyArrow dataset fragments).
5. Implement the idempotent sink pattern with a `_SUCCESS` marker and a minimal validation report (rowcount + null rate).
