# Module 02: Analytics Core — Joins, Aggregation, Windows, Reshape, Nested Data

## Version & scope contract

* Target: **Polars 1.x (Python bindings)**. Current stable is **~1.36.1 as of mid-December 2025**.
* Always verify your runtime (and pin it in reproducible work):

```python
import polars as pl
print(pl.__version__)
```

Scope: **single-node analytics** with `DataFrame` (eager) and `LazyFrame` (lazy). Assumes Module 01 discipline: express logic in expressions, reduce width/rows early, enforce schema contracts, handle nulls intentionally, inspect plans when performance matters.

---

## Table of contents

1. **Core 01 — Filtering, Sorting, Uniqueness:** Determinism as a Contract
2. **Core 02 — GroupBy and Aggregation:** An Algebra You Can Reason About
3. **Core 03 — Joins Without Surprise:** Cardinality Discipline
4. **Core 04 — Windows vs Rolling:** Two Different Tools
5. **Core 05 — Nested Data Mastery:** Struct/List + Null Semantics

**Appendix**
A. Analytics pipeline checklist (shape + determinism + nulls)
B. Patterns / anti-patterns (analytics edition)
C. Mastery exercises (actionable datasets)

---

# Core 01 — Filtering, Sorting, Uniqueness: Determinism as a Contract

## Learning objectives

You will be able to:

* write filters that remain correct under nulls and edge cases,
* enforce deterministic outputs with explicit ordering and tie-breakers,
* validate uniqueness assumptions before they become join bugs,
* deduplicate only with an explicit survivor rule.

---

## 1. Filtering: strict truth under three-valued logic

`filter` keeps a row only when the predicate is **True**. If the predicate is **False** *or* **Null**, the row is dropped.

```python
import polars as pl

df = pl.DataFrame({"x": [1, None, 3]})
out = df.filter(pl.col("x") > 2)
print(out)
```

Expected:

```
shape: (1, 1)
┌─────┐
│ x   │
│ --- │
│ i64 │
╞═════╡
│ 3   │
└─────┘
```

If your meaning is “keep values > 2 and keep missing values,” encode it:

```python
import polars as pl

df = pl.DataFrame({"x": [1, None, 3]})
out = df.filter((pl.col("x") > 2) | pl.col("x").is_null())
print(out)
```

Expected:

```
shape: (2, 1)
┌──────┐
│ x    │
│ ---  │
│ i64  │
╞══════╡
│ null │
│ 3    │
└──────┘
```

### What to notice

* Missingness is not “a nuisance.” It is a semantic decision.
* If you want missing to act like a value (0, empty string), do it explicitly with `fill_null` / `coalesce` and document the contract.

---

## 2. Sorting: determinism is a contract you write

After `group_by`, `join`, `unique`, or concatenation, you must not rely on incidental ordering. If you need reproducibility (tests, reporting, top-k), sort explicitly.

```python
import polars as pl

df = pl.DataFrame({
    "group": ["a", "a", "a", "b"],
    "ts":    [2,   1,   1,   1],
    "value": [10,  20,  30,  40],
})

out = df.sort(["group", "ts", "value"], descending=[False, False, True])
print(out)
```

Expected:

```
shape: (4, 3)
┌───────┬─────┬───────┐
│ group │ ts  │ value │
│ ---   │ --- │ ---   │
│ str   │ i64 │ i64   │
╞═══════╪═════╪═══════╡
│ a     │ 1   │ 30    │
│ a     │ 1   │ 20    │
│ a     │ 2   │ 10    │
│ b     │ 1   │ 40    │
└───────┴─────┴───────┘
```

### Tie-breakers are non-negotiable

If timestamps tie, “latest” is undefined unless you specify a tie-breaker (ingest id, version, priority). Ship a tie-breaker or admit nondeterminism.

---

## 3. Uniqueness and deduplication: validate, then choose survivors

Uniqueness assumptions underpin joins and “latest record” logic. Validate them early.

```python
import polars as pl

df = pl.DataFrame({"id": [1, 2, 2, 3]})
check = df.select([
    pl.col("id").n_unique().alias("n_unique"),
    pl.col("id").is_unique().all().alias("all_unique"),
])
print(check)
```

Expected:

```
shape: (1, 2)
┌──────────┬────────────┐
│ n_unique  │ all_unique │
│ ---      │ ---        │
│ u32      │ bool       │
╞══════════╪════════════╡
│ 3        │ false      │
└──────────┴────────────┘
```

Dedup is not “cleanup.” It is “choose which record represents the key.”

```python
import polars as pl

events = pl.DataFrame({
    "id": [1, 1, 2, 2],
    "ts": [5, 5, 3, 4],
    "ingest_id": [10, 11, 20, 21],
    "value": [100, 101, 200, 201],
})

dedup = (
    events.sort(["id", "ts", "ingest_id"])
          .unique(subset=["id"], keep="last")
)
print(dedup)
```

Expected:

```
shape: (2, 4)
┌─────┬─────┬──────────┬───────┐
│ id  │ ts  │ ingest_id│ value │
│ --- │ --- │ ---      │ ---   │
│ i64 │ i64 │ i64      │ i64   │
╞═════╪═════╪══════════╪═══════╡
│ 1   │ 5   │ 11       │ 101   │
│ 2   │ 4   │ 21       │ 201   │
└─────┴─────┴──────────┴───────┘
```

---

# Core 02 — GroupBy and Aggregation: An Algebra You Can Reason About

## Learning objectives

You will be able to:

* compute many metrics in one groupby pass,
* express conditional metrics inside the engine,
* understand distribution summaries and their costs,
* reshape (pivot/unpivot) with semantic discipline,
* choose between aggregate-join-back and windows deliberately.

---

## 1. Multi-aggregation in one pass (default)

```python
import polars as pl

df = pl.DataFrame({
    "group": ["a", "a", "b", "b", "b"],
    "value": [1, 2, 3, 4, 5],
})

out = (
    df.group_by("group")
      .agg([
          pl.len().alias("n"),
          pl.col("value").sum().alias("sum"),
          pl.col("value").mean().alias("mean"),
          pl.col("value").min().alias("min"),
          pl.col("value").max().alias("max"),
      ])
      .sort("group")
)
print(out)
```

Expected:

```
shape: (2, 6)
┌───────┬─────┬─────┬──────┬─────┬─────┐
│ group │ n   │ sum │ mean │ min │ max │
│ ---   │ --- │ --- │ ---  │ --- │ --- │
│ str   │ u32 │ i64 │ f64  │ i64 │ i64 │
╞═══════╪═════╪═════╪══════╪═════╪═════╡
│ a     │ 2   │ 3   │ 1.5  │ 1   │ 2   │
│ b     │ 3   │ 12  │ 4.0  │ 3   │ 5   │
└───────┴─────┴─────┴──────┴─────┴─────┘
```

---

## 2. Conditional aggregation (and why boolean sums work)

Two idioms dominate:

* `filter(...)` inside aggregation,
* boolean arithmetic (`True→1`, `False→0`) under `sum`/`mean`.

```python
import polars as pl

df = pl.DataFrame({
    "group": ["a", "a", "b", "b", "b"],
    "value": [1, 2, 3, 4, 5],
})

out = (
    df.group_by("group")
      .agg([
          (pl.col("value") >= 3).sum().alias("count_ge_3"),
          (pl.col("value") >= 3).mean().alias("rate_ge_3"),
          pl.col("value").filter(pl.col("value") >= 3).mean().alias("mean_ge_3"),
      ])
      .sort("group")
)
print(out)
```

Expected:

```
shape: (2, 4)
┌───────┬────────────┬──────────┬──────────┐
│ group │ count_ge_3 │ rate_ge_3 │ mean_ge_3│
│ ---   │ ---        │ ---       │ ---      │
│ str   │ u32        │ f64       │ f64      │
╞═══════╪════════════╪═══════════╪══════════╡
│ a     │ 0          │ 0.0       │ null     │
│ b     │ 3          │ 1.0       │ 4.0      │
└───────┴────────────┴───────────┴──────────┘
```

---

## 3. Distribution summaries: quantify cost (micro-benchmark)

Quantiles typically cost more than means. Measure on your target machine.

```python
import time
import polars as pl

n = 2_000_000
df = pl.DataFrame({
    "g": pl.repeat("x", n, eager=True),
    "v": pl.int_range(0, n, eager=True),
})

t0 = time.perf_counter()
_ = df.group_by("g").agg(pl.col("v").mean())
t1 = time.perf_counter()

t2 = time.perf_counter()
_ = df.group_by("g").agg(pl.col("v").quantile(0.99))
t3 = time.perf_counter()

print(f"mean: {t1 - t0:.4f}s")
print(f"p99:  {t3 - t2:.4f}s")
```

Interpretation: machine-dependent; in practice p99 is often multiple-× slower than mean. Treat quantiles as “pay for insight,” not a default.

---

## 4. Pivot/unpivot: semantics + alternatives (`first` vs `sum`)

Pivot is a semantic transformation. If `(index, column)` is not unique, your aggregation function defines reality.

```python
import polars as pl

# Note the duplicate (id=1, metric=m1): two values.
long = pl.DataFrame({
    "id":     [1, 1, 1, 1, 2, 2],
    "metric": ["m1","m1","m2","m3","m1","m3"],
    "value":  [10, 2,  20, 30, 40, 50],
})

wide_first = long.pivot(values="value", index="id", columns="metric", aggregate_function="first")
wide_sum   = long.pivot(values="value", index="id", columns="metric", aggregate_function="sum")

print(wide_first)
print(wide_sum)
```

Expected `wide_first` (survivor semantics):

```
shape: (2, 4)
┌─────┬─────┬─────┬─────┐
│ id  │ m1  │ m2  │ m3  │
│ --- │ --- │ --- │ --- │
│ i64 │ i64 │ i64 │ i64 │
╞═════╪═════╪═════╪═════╡
│ 1   │ 10  │ 20  │ 30  │
│ 2   │ 40  │ null│ 50  │
└─────┴─────┴─────┴─────┘
```

Expected `wide_sum` (additive semantics):

```
shape: (2, 4)
┌─────┬─────┬─────┬─────┐
│ id  │ m1  │ m2  │ m3  │
│ --- │ --- │ --- │ --- │
│ i64 │ i64 │ i64 │ i64 │
╞═════╪═════╪═════╪═════╡
│ 1   │ 12  │ 20  │ 30  │
│ 2   │ 40  │ null│ 50  │
└─────┴─────┴─────┴─────┘
```

### What to notice

* `"first"` is only meaningful if you enforced a deterministic order before pivoting (or uniqueness already holds).
* Keep long form for computation; pivot late for reporting.

A crude width intuition (time + memory estimate):

```python
import time
import polars as pl

wide = pl.DataFrame({"id": [1, 2]})
for i in range(500):
    wide = wide.with_columns(pl.lit(i).alias(f"m{i}"))

print("estimated_size_bytes:", wide.estimated_size())

t0 = time.perf_counter()
_ = wide.select(pl.all().exclude("id").sum())
t1 = time.perf_counter()
print(f"wide sum over 500 cols: {t1 - t0:.4f}s")
```

---

## 5. Aggregate-join-back vs windows (identical results, different contracts)

```python
import polars as pl

df = pl.DataFrame({"group": ["a", "a", "b"], "value": [1.0, 3.0, 10.0]})

metrics = df.group_by("group").agg(pl.col("value").mean().alias("group_mean"))
join_back = df.join(metrics, on="group", how="left")

windowed = df.with_columns(pl.col("value").mean().over("group").alias("group_mean"))

print(metrics)
print(join_back)
print(windowed)
```

Expected:

* `join_back` and `windowed` match here.
* `join_back` materializes assumptions as a separate artifact (often easier to validate/debug).

---

# Core 03 — Joins Without Surprise: Cardinality Discipline

## Learning objectives

You will be able to:

* choose join types by meaning,
* predict and quantify row explosion from duplicates,
* validate invariants before joining,
* use semi/anti joins for correctness filters,
* perform `asof_join` correctly with direction and tolerance.

---

## 1. Join types with explicit outputs

```python
import polars as pl

left = pl.DataFrame({"k": [1, 2, 3], "lv": ["L1", "L2", "L3"]})
right = pl.DataFrame({"k": [2, 3, 3], "rv": ["R2", "R3a", "R3b"]})

print("INNER")
print(left.join(right, on="k", how="inner"))

print("\nLEFT")
print(left.join(right, on="k", how="left"))

print("\nFULL")
print(left.join(right, on="k", how="full"))

print("\nSEMI")
print(left.join(right, on="k", how="semi"))

print("\nANTI")
print(left.join(right, on="k", how="anti"))
```

Expected (key outcomes):

* **INNER** includes keys 2 and 3; key 3 duplicates expand rows.
* **LEFT** keeps key 1 with `rv=null`.
* **SEMI** returns only left rows whose keys exist in right (2,3), without right payload.
* **ANTI** returns left rows whose keys do not exist in right (1).

---

## 2. Cardinality explosion: quantified and visible

```python
import polars as pl

left = pl.DataFrame({"k": ["a", "a", "a", "b", "b"], "lv": [1, 2, 3, 4, 5]})
right = pl.DataFrame({"k": ["a", "a", "b"], "rv": [10, 11, 20]})

joined = left.join(right, on="k", how="inner")

print("left rows:", left.height)
print("right rows:", right.height)
print("joined rows:", joined.height)
print(joined)
```

Expected:

* joined rows = 8 (6 for `a`, 2 for `b`), showing multiplicative pairing.

Before joining in production, inspect per-key multiplicity:

```python
print(left.group_by("k").len().sort("k"))
print(right.group_by("k").len().sort("k"))
```

---

## 3. `asof_join`: complete example with tolerance

```python
import polars as pl

trades = pl.DataFrame({"t": [10, 20, 30], "price": [100.0, 101.0, 99.5]}).sort("t")
quotes = pl.DataFrame({"t": [5, 15, 25, 35], "bid": [99.0, 100.0, 100.5, 99.2]}).sort("t")

backward = trades.join_asof(quotes, on="t", strategy="backward")
print(backward)
```

Expected:

```
shape: (3, 3)
┌─────┬───────┬───────┐
│ t   │ price │ bid   │
│ --- │ ---   │ ---   │
│ i64 │ f64   │ f64   │
╞═════╪═══════╪═══════╡
│ 10  │ 100.0 │ 99.0  │
│ 20  │ 101.0 │ 100.0 │
│ 30  │ 99.5  │ 100.5 │
└─────┴───────┴───────┘
```

Tolerance (units match `t` dtype; here integer distance):

```python
tol3 = trades.join_asof(quotes, on="t", strategy="backward", tolerance=3)
print(tol3)
```

Expected:

```
shape: (3, 3)
┌─────┬───────┬──────┐
│ t   │ price │ bid  │
│ --- │ ---   │ ---  │
│ i64 │ f64   │ f64  │
╞═════╪═══════╪══════╡
│ 10  │ 100.0 │ null │
│ 20  │ 101.0 │ null │
│ 30  │ 99.5  │ null │
└─────┴───────┴──────┘
```

Note: other strategies (`"forward"`, `"nearest"`) are different contracts—test them on a toy sequence before trusting them.

---

# Core 04 — Windows vs Rolling: Two Different Tools

## Learning objectives

You will be able to:

* use windows for group-aware columns (row count preserved),
* demonstrate order sensitivity for cumulative windows,
* compute rolling features and explicitly control leakage,
* verify EWM behavior via a reference definition.

---

## 1. Windows: order-independent vs order-dependent

### 1.1 Order-independent: group mean and centering

```python
import polars as pl

df = pl.DataFrame({"g": ["a", "a", "b"], "x": [1.0, 3.0, 10.0]})
out = df.with_columns(
    pl.col("x").mean().over("g").alias("g_mean"),
    (pl.col("x") - pl.col("x").mean().over("g")).alias("x_centered"),
)
print(out)
```

Expected:

```
shape: (3, 3)
┌─────┬───────┬───────────┐
│ g   │ g_mean│ x_centered│
│ --- │ ---   │ ---       │
│ str │ f64   │ f64       │
╞═════╪═══════╪═══════════╡
│ a   │ 2.0   │ -1.0      │
│ a   │ 2.0   │ 1.0       │
│ b   │ 10.0  │ 0.0       │
└─────┴───────┴───────────┘
```

### 1.2 Order-dependent: cumulative sum (unsorted vs sorted)

```python
import polars as pl

df = pl.DataFrame({
    "g": ["a", "a", "a", "b", "b"],
    "t": [2, 1, 3, 1, 2],
    "x": [10, 20, 30, 1, 2],
})

unsorted = df.with_columns(pl.col("x").cum_sum().over("g").alias("cum_x"))
sorted_  = df.sort(["g", "t"]).with_columns(pl.col("x").cum_sum().over("g").alias("cum_x"))

print("UNSORTED (not a valid 'cumulative by time' implementation)")
print(unsorted)
print("\nSORTED (contract defined: cumulative by time)")
print(sorted_)
```

Expected:

* Sorted version yields cumulatives in time order.
* Unsorted version follows row order; it is not what you mean if “time” matters.

---

## 2. Rolling: local history, leakage explicit

```python
import polars as pl

df = pl.DataFrame({"t": [1, 2, 3, 4, 5], "x": [10, 20, 30, 40, 50]}).sort("t")

out = df.with_columns([
    pl.col("x").rolling_mean(3, center=False).alias("roll3_past_only"),
    pl.col("x").rolling_mean(3, center=True).alias("roll3_centered"),
])

print(out)
```

Expected:

```
shape: (5, 4)
┌─────┬─────┬────────────────┬───────────────┐
│ t   │ x   │ roll3_past_only│ roll3_centered│
│ --- │ --- │ ---            │ ---           │
│ i64 │ i64 │ f64            │ f64           │
╞═════╪═════╪════════════════╪═══════════════╡
│ 1   │ 10  │ null           │ null          │
│ 2   │ 20  │ null           │ 20.0          │
│ 3   │ 30  │ 20.0           │ 30.0          │
│ 4   │ 40  │ 30.0           │ 40.0          │
│ 5   │ 50  │ 40.0           │ null          │
└─────┴─────┴────────────────┴───────────────┘
```

### What to notice

* `center=True` **includes future values** for interior points (e.g., at `t=2` it uses `t=3`). That is leakage for causal/forecasting features.
* `center=False` is the default contract for “past-only history.”

---

## 3. EWM: reference definition + contrast alphas

Do not treat EWM as “just another moving average.” Lock the definition.

A common recursive definition is: `s0=x0`, `s_t = α x_t + (1-α) s_{t-1}`. For `x=[1,2,3,4]`:

* α=0.2 → `[1.0, 1.2, 1.56, 2.048]`
* α=0.8 → `[1.0, 1.8, 2.76, 3.752]`

Verify Polars’ output matches the contract you intend:

```python
import polars as pl

df = pl.DataFrame({"x": [1.0, 2.0, 3.0, 4.0]})
out = df.with_columns([
    pl.col("x").ewm_mean(alpha=0.2).alias("ewm_a02"),
    pl.col("x").ewm_mean(alpha=0.8).alias("ewm_a08"),
])
print(out)
```

If the numbers differ from your reference, check parameterization (e.g., adjust-like behavior) and record the exact contract in tests.

---

# Core 05 — Nested Data Mastery: Struct/List + Null Semantics

## Learning objectives

You will be able to:

* work with struct/list columns without flattening prematurely,
* distinguish outer-null vs inner-null and handle each correctly,
* use `unnest`/`explode` safely with explicit shape awareness,
* avoid explode→regroup cycles when list aggregations suffice.

---

## 1. Outer-null vs inner-null (fully explicit)

```python
import polars as pl

df = pl.DataFrame({"items": [[1, None], None, [3, None, 4], []]})

out = df.with_columns([
    pl.col("items").is_null().alias("outer_null"),
    pl.col("items").list.drop_nulls().alias("drop_inner_nulls"),
    pl.col("items").fill_null([]).alias("fill_outer_null_as_empty"),
])

print(out)
```

Expected:

```
shape: (4, 4)
┌──────────────┬────────────┬───────────────────┬──────────────────────────┐
│ items        │ outer_null │ drop_inner_nulls  │ fill_outer_null_as_empty │
│ ---          │ ---        │ ---               │ ---                      │
│ list[i64]    │ bool       │ list[i64]         │ list[i64]                │
╞══════════════╪════════════╪═══════════════════╪══════════════════════════╡
│ [1, null]    │ false      │ [1]               │ [1, null]                │
│ null         │ true       │ null              │ []                       │
│ [3, null, 4] │ false      │ [3, 4]            │ [3, null, 4]             │
│ []           │ false      │ []                │ []                       │
└──────────────┴────────────┴───────────────────┴──────────────────────────┘
```

---

## 2. Structs: `unnest` with strict schema

```python
import polars as pl

df = pl.DataFrame({
    "id": [1, 2],
    "meta": [{"a": 10, "b": "x"}, {"a": 20, "b": "y"}],
}).with_columns(
    pl.col("meta").cast(pl.Struct([
        pl.Field("a", pl.Int64),
        pl.Field("b", pl.String),
    ]))
)

out = df.unnest("meta")
print(out)
```

Expected:

```
shape: (2, 3)
┌─────┬─────┬─────┐
│ id  │ a   │ b   │
│ --- │ --- │ --- │
│ i64 │ i64 │ str │
╞═════╪═════╪═════╡
│ 1   │ 10  │ x   │
│ 2   │ 20  │ y   │
└─────┴─────┴─────┘
```

---

## 3. Explode is row multiplication (show the table)

```python
import polars as pl

df = pl.DataFrame({"id": [1, 2], "items": [[10, 11, 12], [20]]})
exploded = df.explode("items")

print("before:", df.shape)
print("after: ", exploded.shape)
print(exploded)
```

Expected:

```
before: (2, 2)
after:  (4, 2)
shape: (4, 2)
┌─────┬───────┐
│ id  │ items │
│ --- │ ---   │
│ i64 │ i64   │
╞═════╪═══════╡
│ 1   │ 10    │
│ 1   │ 11    │
│ 1   │ 12    │
│ 2   │ 20    │
└─────┴───────┘
```

---

## 4. List aggregations: avoid explode→regroup (show equality)

```python
import polars as pl

nested = pl.DataFrame({"id": [1, 2], "items": [[10, 11], [20, 21, 22]]})
exploded = nested.explode("items")
regrouped = exploded.group_by("id").agg(pl.col("items").alias("items")).sort("id")

print("ORIGINAL")
print(nested.sort("id"))
print("\nREGROUPED (after explode)")
print(regrouped)
```

Expected:

* The regrouped structure matches the original (up to ordering), proving the explode step was unnecessary unless you did real row-level work between them.

---

## Closing recap

Module 02 is analytics as **contracts**: filtering is truth under nulls, sorting is determinism under concurrency, grouping is algebra, joins/explodes are shape engines, windows/rolling require explicit order and leakage choices, and nested data requires disciplined handling of outer vs inner missingness. Combined with Module 01 habits (lazy pipelines, early reduction, schema discipline, plan inspection), this yields pipelines that are fast, auditable, and reproducible.

---

# Appendix A — Analytics pipeline checklist

Before shipping:

* Can you state and verify expected row counts after each join/explode?
* Are join keys’ multiplicities validated (not assumed)?
* Are “latest/top/first” semantics backed by explicit sorting and tie-breakers?
* Are null-handling rules explicit in filters and conditional metrics?
* Is pivoting postponed until reporting?

---

# Appendix B — Patterns / anti-patterns (analytics edition)

**Patterns**

* `sort + tie-breakers + unique` for deterministic dedupe
* pre-aggregate or deterministic-dedupe before joining
* validate per-key counts before joins
* keep long for compute; pivot late
* past-only rolling for causal features
* preserve nested structure; explode only when required

**Anti-patterns**

* dedupe without survivor semantics
* many-to-many joins without intent + tests
* cumulative/window features without explicit order
* rolling features that leak future values
* explode→regroup with no meaningful row-level work

---

# Appendix C — Mastery exercises (actionable datasets)

Datasets:

* NYC Taxi (Parquet; time-based; joinable)
* any event log with `(entity_id, timestamp, event_type)`
* any JSON dataset yielding struct/list columns

Exercises:

1. deterministic “latest per key” with explicit tie-breakers + golden output test
2. construct a many-to-many join, quantify explosion, fix via pre-aggregation
3. compute group z-scores via join-back and via window; assert equality
4. rolling leakage: centered vs past-only; write a test proving no future leakage
5. nested drill: outer-null vs inner-null policy with golden expected tables
