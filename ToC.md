# Polars Deep Dive

## Module 01: Polars First Principles — The Columnar Contract and Expression Calculus

### 01. Columnar Contract: DataFrame vs Series, Copies vs Views, Eager vs Lazy

* Columns (Series) are the compute unit; row-wise thinking is the main slowdown
* Copy vs zero-copy expectations; schema-first discipline
* Eager vs Lazy as two execution modes over the same expression language
* **Diagram:** *Row-wise vs columnar layout* (why column ops are fast, row ops are slow)

### 02. Expression Calculus + Control Flow Inside the Engine

* Expression trees: `pl.col`, `pl.lit`, chaining, `alias`, `cast`
* Branching without Python: `when().then().otherwise()`, `coalesce`, `clip`, `is_in`
* Null semantics (three-valued logic) and correctness-first null handling

### 03. Transform Patterns That Scale (and Compose)

* `select` vs `with_columns` vs `with_columns_seq` (dependency/ordering)
* Column selectors by dtype/name; struct/list-safe transforms
* `pipe` for functional composition of reusable DataFrame/LazyFrame transforms
* Anti-patterns: row loops, accidental materialization, “one-off” intermediates

### 04. Types as Performance: Schema Discipline + Categorical Strategy

* High-impact dtypes: datetime/duration/decimal/categorical/struct/list
* Categorical vs String: memory, join/group speed, category hygiene, unknown categories
* Parse vs cast; strict schemas at IO boundaries for predictable pipelines

### 05. Ingestion for the Optimizer: Pushdown as a Skill

* Prefer `scan_*` for pipelines; use `read_*` for small interactive work
* Predicate/projection pushdown and the ordering constraints that enable it
* Practical structuring: keep filters/projections early; avoid transforms that block pushdown

## Module 02: Analytics Core — Joins, Aggregation, Windows, Reshape, Nested Data

### 01. Filtering, Sorting, Uniqueness (Determinism as a Contract)

* Deterministic outputs: explicit sorting + tie-breakers
* `unique` / `is_unique` / `n_unique`; dedupe without changing meaning
* Null-aware comparisons and “missingness” correctness traps

### 02. GroupBy and Aggregation as an Algebra

* Multi-agg patterns, conditional aggs, distribution summaries
* Pivot/unpivot tradeoffs; wide vs long cost model
* “Aggregate then join back” vs window functions: choose deliberately

### 03. Joins Without Surprise (Cardinality Discipline)

* Inner/left/full/semi/anti joins; duplicate keys → row explosion
* `asof_join`: sort requirements, tolerance, direction, correctness traps
* Habit: assert key invariants and validate expected join cardinality

### 04. Windows vs Rolling: Two Different Tools

* Windows: `over` partitions, `sort_by` semantics
* Rolling expressions on sorted frames (often simpler/faster than windows)
* EWM/rolling boundaries: define them explicitly or get wrong results

### 05. Nested Data Mastery: Struct/List + Null Semantics

* `explode`, `unnest`, struct fields, list aggregations
* Outer-null vs inner-null: `list.drop_nulls()` vs fill strategies vs preserving structure
* Normalization patterns for JSON-like data; performance implications

## Module 03: Production Polars — Plans, Performance, UDFs, and Engineering Practice

### 01. Lazy Query Plans: Read `explain` or You’re Guessing

* Logical vs physical plan; where materialization happens
* Join strategy visibility, optimizer rewrites, spotting bad plans early
* Failure modes: blocked pushdowns, wide intermediates, unnecessary sorts
* **Diagram:** *User pipeline → logical plan → optimizer → physical plan* (pushdowns/reordering)

### 02. Performance Rules That Actually Matter

* Keep compute in expressions; reduce width early; minimize materialization
* Memory engineering: categorical encoding, string cost control, cardinality awareness
* Performance is dominated by data shape (keys, skew, width), not syntax

### 03. The UDF Trap: `apply`/`map_elements` vs Controlled `map_batches`

* Why row-wise UDFs are slow (Python boundary + per-element overhead + GIL effects)
* When `map_batches` is acceptable: batch contracts, typed outputs, no hidden state
* Preferred replacements: expression rewrites, joins-as-maps, `when/then/otherwise`

### 04. Robust Pipelines: Contracts, Tests, Deterministic Outputs

* Schema + invariants: null rates, uniqueness, monotonicity, ranges
* Golden-frame tests + property tests for invariants
* Determinism: explicit sorting, stable assumptions, reproducible IO

### 05. Interop and Ecosystem Reality (Why Polars Wins)

* Arrow ↔ Polars ↔ Pandas: where zero-copy holds vs where conversion allocates
* Rust engine + Python bindings: speed comes from staying out of Python
* Hybrid strategy: parquet partitioning; DuckDB/SQL engines when they’re the better tool
