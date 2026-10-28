---
module_id: DBE-013
program: Database Engineering
level: 1
module_number: 13
title: Aggregation and Grouping
status: complete
last_verified: 2026-08-30
---

# Aggregation and Grouping

## One-Page Review

### Governing question

How does SQL turn a bag of input occurrences into trustworthy group-level measures while preserving grain, null semantics, numeric meaning, grouping provenance, and reproducibility?

### Essential definitions

A **grouping key** maps each input occurrence to a group identity. **Grain** states what one output row represents. An **aggregate** folds the values in a group into a result such as count, sum, minimum, maximum, or average. `WHERE` filters input rows before grouping; an aggregate `FILTER` or conditional expression selects values for one measure; `HAVING` filters group rows after aggregation. `COUNT(*)` counts input occurrences, while `COUNT(x)` counts nonnull `x`. A **grouping set** requests several grouping grains in one query; `ROLLUP` and `CUBE` generate structured grouping sets. **Algebraic state** is mergeable partial state used for parallel/distributed aggregation.

### Central model, mechanism, or theorem

Let `g(r)` map input occurrence `r` to key `k`. Each group bag is `G_k={r | g(r)=k}` with multiplicity. Aggregates operate on that bag, often after discarding null arguments according to function rules. Many useful aggregates have mergeable state: `COUNT` adds counts; `SUM` adds sums; `AVG` must merge `(nonnull_count,sum)`, not averages of partitions; variance requires a stable sufficient-state algorithm. Correctness therefore begins with input grain, group identity, measure definition, and empty/null behavior—not with SQL syntax or a hash-versus-sort plan.

### Critical invariants

- Input and output grain are written in domain terms before the query.
- Joins preserve or deliberately transform measure grain before aggregation.
- Every selected nonaggregate expression is grouped or validly functionally dependent under the chosen dialect.
- `COUNT(*)`, `COUNT(x)`, null, zero, and empty-input behavior are distinguished.
- Units, currency, time zone, numeric type, rounding stage, and overflow policy are explicit.
- Ordered aggregates specify an internal order; final rows use an outer `ORDER BY`.
- Grouping-set subtotal nulls are distinguished from real null keys with grouping metadata.
- Partial-state merge, spill, skew, parallelism, and approximate error are verified before scale claims.

### Common failures

Failures include aggregating after a many-to-many fanout, counting nullable columns when rows are intended, treating null sum as zero without domain authority, averaging averages, summing percentages, mixing currencies or units, grouping timestamps without time-zone policy, selecting arbitrary ungrouped columns, using `HAVING` for a simple input filter, assuming group output is sorted, omitting order inside array/string aggregation, confusing subtotal null with stored null, double-counting across overlapping grouping sets, overflowing fixed-width totals, and comparing floating sums bit-for-bit across parallel plans.

### Compact example

Six sales rows group into null, `se`, and `us` regions. The Swedish group has three rows, two nonnull amounts, sum 150, and average 75 over nonnull amounts. The US group has two rows and sum 100. A null-region row is a real group with sum 10. A rollup adds a grand-total row whose region is also null-looking, so a grouping flag distinguishes `(NULL,10,detail)` from `(NULL,260,grand total)`. An empty input gives `COUNT(*)=0` but `SUM(amount)=NULL` in the modeled SQL behavior.

### Connections

[DBE-012](012-joins-and-join-semantics.md) controls fanout before aggregation. [DBE-014](../ROADMAP.md) composes grouped subqueries and CTEs. Later execution modules cover hash/sort aggregation, spilling, statistics, and distributed partial aggregation. Data Engineering and Data Architecture govern measure definitions, event time, and semantic consistency.

## Governing Question

Aggregation compresses many occurrences into fewer facts. That compression is irreversible unless the underlying detail remains accessible, so a wrong grain or measure can look polished while hiding duplication, omission, incompatible units, or time-boundary errors. The engineer must prove what each group represents and exactly which occurrences and values contribute.

The question has three layers: logical grouping and null/bag semantics; domain meaning such as revenue, active users, or conversion; and physical execution under memory, spill, skew, parallelism, and numerical limits. SQL validity addresses only part of the first layer.

## Why This Matters

Dashboards, billing, experimentation, capacity, compliance, and machine-learning features depend on aggregates. A join that multiplies order totals by line count inflates revenue. `COUNT(email)` undercounts customers with null email. Summing daily distinct users overstates monthly distinct users. Averaging regional averages weights small and large regions equally unless that is intended.

Null and empty groups create interface bugs. A scalar aggregate over no rows may still return one row; count is zero while most other general aggregates return null. A left join can create a group with one null-extended row, making `COUNT(*)=1` while `COUNT(right.id)=0`. Choosing `COALESCE(...,0)` changes presentation and possibly domain meaning.

At scale, aggregation is resource-intensive. High-cardinality or skewed groups consume memory, spill to storage, and imbalance workers. Parallel or distributed combination can change floating-point accumulation order. Approximate distinct/count/sketch methods trade exactness for bounded resources and need an explicit error/confidence contract.

## Prerequisites and Retrieval

Retrieve bags, functions, equivalence, null, three-valued logic, joins, keys, functional dependency, numeric types, units, time zones, sorting, hashing, memory, parallelism, probability, and query plans.

Distinguish input rows from nonnull aggregate arguments; group absence from a present null-valued group; zero from null; row filter from aggregate filter from group filter; group order from ordered aggregate input; detail null from rollup placeholder; exact from approximate; and mathematical real arithmetic from finite database numeric behavior.

## Learning Objectives

After this module, you should be able to:

1. state input and output grain for a grouped query;
2. derive group bags and aggregate results including duplicates and nulls;
3. distinguish row, per-aggregate, and group filtering;
4. use count, sum, average, min/max, boolean, and distinct measures correctly;
5. prove when an ungrouped selected column is functionally determined;
6. design conditional aggregation and ratios without denominator errors;
7. interpret grouping sets, rollups, cubes, and grouping provenance;
8. merge partial aggregate state correctly;
9. control numerical type, units, rounding, overflow, and reproducibility; and
10. diagnose aggregation plans, skew, memory, spill, and fanout.

## Core Exposition

`GROUP BY` partitions the post-`WHERE` input bag by equal grouping expressions under the database's type/collation semantics. Every occurrence belongs to one group for that grouping set, including duplicate rows. Null grouping values are generally collected into one group for grouping purposes even though ordinary `NULL = NULL` is unknown in predicates; grouping equality is an operation-specific notion.

No `GROUP BY` with aggregate calls creates one conceptual group over all selected input rows. On empty input, that global group still yields a result row in ordinary aggregate queries: `COUNT(*)` returns zero; most general aggregates such as `SUM`, `AVG`, `MIN`, and `MAX` return null. With explicit grouping, no input means no group rows. A `HAVING` condition can remove the global result.

`COUNT(*)` counts occurrences after `FROM`/`WHERE`. `COUNT(expression)` counts occurrences for which the expression is nonnull. `COUNT(DISTINCT expression)` counts distinct nonnull values under dialect rules. These answer different questions. For an outer join, count a guaranteed-nonnull right key to count matches; `COUNT(*)` counts the preserved left/null-extended row too.

`SUM(x)` and `AVG(x)` ordinarily ignore null `x`. A null may mean unknown rather than zero, so silently coalescing each null to zero changes the denominator of average and the knowledge claim. `COALESCE(SUM(x),0)` can be correct when an empty set means zero additive contribution; document this at the domain boundary. Never use formatting defaults to settle semantics.

Average is `sum(nonnull x)/count(nonnull x)` under an appropriate numeric type. To combine partitions, add sums and counts, then divide; do not average partition averages unless their counts are equal or weights are applied. A weighted mean is `sum(w*x)/sum(w)` with explicit rules for nulls, zero/negative weights, and units. Ratios similarly require separately defined numerator and denominator.

Minimum and maximum ignore null inputs and return null when no nonnull value exists. For text they depend on collation/type semantics. They do not identify the row that contains the extremum when ties exist. Selecting an arbitrary ungrouped companion column is invalid or nondeterministic. Use a totally ordered row-selection technique such as a window function or lateral top-one query.

Boolean aggregates and conditional counts encode quantifiers when supported. “Any violation” is an existential; “all checks pass” is universal but empty-group and null behavior need policy. Conditional aggregation can use aggregate `FILTER (WHERE predicate)` in supporting dialects or `CASE` expressions. `COUNT(*) FILTER` and `SUM(CASE WHEN ... THEN 1 ELSE 0 END)` can agree, but `COUNT(CASE ... THEN 1 END)` relies on null else values; write and test deliberately.

Filtering occurs at distinct boundaries. `WHERE occurred_at>=start` removes rows before all aggregates and grouping. `SUM(amount) FILTER (WHERE status='paid')` feeds only paid amounts to that measure while another aggregate can see all group rows. `HAVING SUM(amount)>100` removes completed group rows. A group-key-only `HAVING` predicate may be logically movable to `WHERE`, but clarity and outer/join semantics matter; optimizers can perform proven transformations.

Grouping expressions define identity. Grouping by an extracted local day requires a named time zone and calendar; daylight-saving transitions create 23/25-hour local days. Grouping floats can be unstable due to representation. Grouping normalized versus raw text changes equivalence. Persist or compute canonical dimensions with versioned rules when business reporting depends on them.

Every selected expression in a grouped query must be an aggregate, a grouping expression, or validly functionally dependent according to SQL/dialect rules. A primary key can determine other columns of its base row, but joins, nullable uniqueness, expressions, and schema transformations complicate inference. Listing intended grouping columns is often clearer and more portable. Never rely on a mode that chooses arbitrary ungrouped values.

Functional dependency is a semantic claim: `customer_id -> customer_name` holds only in a relation where customer ID is unique and name belongs to that identified version. A join can introduce several historical names per ID. Constraint evidence, not current coincidence, supports omission. Dialects recognize different subsets of standard dependency rules.

`DISTINCT` inside an aggregate changes its input multiset. `SUM(DISTINCT amount)` adds each distinct numeric amount once; it does not deduplicate business transactions. Two legitimate orders for 10 become one contribution. Deduplicate by a stable event/entity key at the correct grain before aggregation, with conflict/replay policy.

Aggregates over joins inherit multiplicity. If each order joins five lines, `SUM(order.total)` multiplies totals fivefold. First assert output grain, then either aggregate line measures, pre-aggregate lines to order, or join a one-row-per-order summary. Compare pre/post counts and sums; `SUM(DISTINCT total)` is not a repair.

Ratios are not generally additive. Conversion is `sum(conversions)/sum(eligible)` at the target grain, not average of per-row or per-group rates unless weighted correctly. Percentages need denominator scope, exclusions, zero-denominator result, and time window. Store numerator and denominator alongside displayed ratio for reconciliation.

Units and currencies must be homogeneous within a sum. Convert at a defined rate/source/time and preserve original plus converted values where audit matters. Choose exact decimal/integer minor units for money according to domain bounds. Define whether tax/rounding happens per line, invoice, currency, or final display; rounding each input before summing differs from rounding the total.

Integer sums can overflow narrower accumulator types; dialect return types vary. Decimal precision/scale can overflow or round. Floating addition is not associative, so parallel/order changes can alter low bits. Use an adequate exact type where required, stable algorithms for variance, tolerances for floats, and version/configuration evidence. Do not promise bitwise stability without proving it.

Variance can be computed from naive `sum(x^2)-sum(x)^2/n`, but cancellation can destroy accuracy for large close values. Online algorithms such as Welford's maintain count, mean, and second central moment; mergeable variants support partial aggregation. Population and sample variance use different denominators. Rely on documented engine functions and validate against high-precision references for critical use.

Order-sensitive aggregates such as string/array/JSON collection need an order within the aggregate call under supported syntax. Sorting the outer result does not order elements inside each aggregate. Without internal order, parallel plans or access changes can alter collection sequence. If object aggregation sees duplicate keys, define rejection or winner policy rather than accept arbitrary overwrite.

Grouping sets request multiple grains. `GROUP BY GROUPING SETS ((region,product),(region),())` is conceptually like `UNION ALL` of those groupings, though execution can share work. `ROLLUP(region,product)` creates hierarchical prefixes; `CUBE` creates combinations. Output can contain a null grouping column because the source key is actually null or because that dimension is absent from the subtotal.

Use `GROUPING(...)` or dialect metadata to distinguish subtotal placeholders. A row `(region=NULL,total=10,grouping=0)` is the real null-region detail group; `(region=NULL,total=260,grouping=1)` is the grand total. Labels like “All” belong in presentation after provenance is retained. Overlapping grouping sets can intentionally emit identical-looking keys at different grains.

Group output order is unspecified without outer `ORDER BY`; a sort-based aggregate may happen to emit key order and a hash aggregate may not. Grouping order is not presentation order. Add a total deterministic order, including grouping-level flags and tie-breakers, for reports and pagination.

Physical aggregation commonly uses hashing, sorting/streaming, indexes, or mixed strategies. Hash aggregation tracks state per group and may spill/partition when memory is insufficient. Sorted aggregation can stream consecutive keys but requires/profits from order. High-cardinality groups increase state count; skew makes one group disproportionately expensive, especially for collection or distinct state.

Parallel/distributed aggregation computes partial state, moves/merges it, then finalizes. An aggregate is distributable only if its state and merge semantics support it. Count/sum/min/max are straightforward under type constraints; average carries count+sum; exact distinct may need large sets/shuffle; holistic measures such as exact median require richer state/order. Approximate sketches reduce state with an error contract and merge compatibility/version requirements.

Aggregation evidence includes input and group counts, null counts, distinct counts, min/max, sums by independent route, join fanout, per-key skew, accumulator types, grouping flags, estimates versus actual groups, memory/spill/temp I/O, parallel workers, and output ordering. Reconcile totals: when grouping sets partition inputs without overlap at one grain, child sums should match parent under additive measures and consistent null/unit rules.

## Definitions and Notation

For input bag `R`, grouping map `g:R->K`, and group bag `G_k`:

- `count_star(G_k)=sum_r m_G(r)`;
- `count_x(G_k)` counts occurrences with `x(r)` nonnull;
- `sum_x` adds nonnull inputs and returns the engine-defined empty result, commonly null in SQL;
- average state is `(n,s)` with final `s/n` for `n>0` and merge `(n1+n2,s1+s2)`;
- additive measure `A` satisfies `A(X bag-union Y)=A(X)+A(Y)` under compatible units/types;
- algebraic aggregate has fixed-size mergeable state; holistic aggregates may require unbounded detail for exact results.

`WHERE`, per-aggregate filtering, grouping, `HAVING`, projection, and final ordering are distinct logical boundaries even when an optimizer rewrites equivalent forms.

## Mechanisms, Invariants, or Proof Structure

An aggregation review should:

1. state input grain, output grain, business key, snapshot/as-of, and source authority;
2. validate joins and deduplication before grouping;
3. define grouping equality, null, collation, calendar/time-zone, and version rules;
4. define each measure's inputs, null/empty behavior, units, type, denominator, and rounding;
5. distinguish `WHERE`, aggregate filter, and `HAVING` predicates;
6. justify every ungrouped selected expression through dependency evidence;
7. distinguish detail/subtotal/grand-total rows using grouping metadata;
8. independently recompute counts/sums/ratios and reconcile additive levels;
9. test empty, all-null, duplicate, skewed, overflow, precision, and order-sensitive cases; and
10. inspect estimated/actual groups, memory, spill, parallel merge, approximate error, and final order.

The finite model below groups a fixed bag, applies SQL-like null-skipping aggregates and per-measure filters, distinguishes an actual null region from a rollup placeholder, and records empty-input results. It is not a SQL engine or numerical-performance model.

<!-- bijux-verify: {"id":"finite-aggregation-groups","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"region_groups=((None, 1, 1, 10, 10), ('se', 3, 2, 150, 75), ('us', 2, 2, 100, 50))\npaid_sums=((None, 10), ('se', 150), ('us', 80))\ndistinct_products=((None, 1), ('se', 2), ('us', 1))\ngrand_total=260\nempty_count=0\nempty_sum=None\nrollup_rows=((None, 10, 0), ('se', 150, 0), ('us', 100, 0), (None, 260, 1))\ngroup_count=3\n","stderr":""}} -->
```python
rows = (
    {"region": "se", "product": "a", "amount": 100, "status": "paid"},
    {"region": "se", "product": "a", "amount": None, "status": "pending"},
    {"region": "se", "product": "b", "amount": 50, "status": "paid"},
    {"region": "us", "product": "a", "amount": 80, "status": "paid"},
    {"region": "us", "product": "a", "amount": 20, "status": "refund"},
    {"region": None, "product": "x", "amount": 10, "status": "paid"},
)


def sql_sum(values):
    present = tuple(value for value in values if value is not None)
    return sum(present) if present else None


def region_sort_key(region):
    return (region is not None, region or "")


regions = tuple(sorted({row["region"] for row in rows}, key=region_sort_key))
groups = []
paid_sums = []
distinct_products = []
for region in regions:
    members = tuple(row for row in rows if row["region"] == region)
    amounts = tuple(row["amount"] for row in members)
    present = tuple(amount for amount in amounts if amount is not None)
    groups.append((region, len(members), len(present), sum(present), sum(present) // len(present)))
    paid_sums.append((region, sql_sum(row["amount"] for row in members if row["status"] == "paid")))
    distinct_products.append((region, len({row["product"] for row in members})))

grand_total = sql_sum(row["amount"] for row in rows)
rollup = tuple((region, group[3], 0) for region, group in zip(regions, groups)) + (
    (None, grand_total, 1),
)

print(f"region_groups={tuple(groups)}")
print(f"paid_sums={tuple(paid_sums)}")
print(f"distinct_products={tuple(distinct_products)}")
print(f"grand_total={grand_total}")
print("empty_count=0")
print(f"empty_sum={sql_sum(())}")
print(f"rollup_rows={rollup}")
print(f"group_count={len(groups)}")
```

The integer averages are exact only for this fixture. Python equality, set behavior, integer arithmetic, and ordering are not database type/collation semantics. The model omits joins, duplicates with identical full rows, overflow, decimal/floating behavior, time zones, spill, concurrency, and parallel merge.

## Alternatives and Trade-Offs

Conditional `FILTER` syntax is clear and lets several measures use different inputs; `CASE` is more portable but null/else/count details must be reviewed. Pre-aggregation prevents fanout and reduces data, but can remove detail needed by later predicates. Materialized summaries speed repeated reports but introduce refresh, correction, and freshness contracts.

Hash aggregation handles unordered input but consumes per-group memory and can spill. Sorted aggregation can stream ordered groups but may require sorting. Exact distinct is authoritative but state-heavy; approximate sketches bound resources with error and merge/version constraints. One grouping-sets query may share scans but produce multiple grains that need provenance; separate queries can be simpler to validate at extra scan/snapshot cost.

## Failure Modes and Misconceptions

“`COUNT(column)` counts rows” is false for null values. “`SUM` of no rows is zero” is not the common SQL result. “Average is additive” is false; merge count and sum. “`SUM(DISTINCT amount)` deduplicates orders” confuses values with identities.

“Every selected column can come from some row in the group” is arbitrary unless functionally determined or explicitly selected by a rule. “`HAVING` and `WHERE` are interchangeable” ignores input versus group filtering. “Grouping sorts” is not an output contract. “Null subtotal means missing data” ignores grouping placeholders.

“Parallel aggregation returns identical floats” ignores nonassociative addition. “More memory fixes skew” may only delay a single huge group's failure. “A green total proves all groups” permits offsetting errors. Reconcile keys, counts, nulls, and independent measures.

## Worked Examples

### Example 1

A left-joined customer with no orders produces one null-extended row: `COUNT(*)=1`, `COUNT(order.id)=0`, and `SUM(order.amount)=NULL`. The report explicitly coalesces the last value only if “no orders means zero revenue.”

### Example 2

Two identical order amounts are distinct transactions. `SUM(DISTINCT amount)` undercounts them; deduplication uses order ID and a replay/conflict rule before summing.

### Example 3

Regional conversion stores `(converted,eligible)` and computes `sum(converted)/sum(eligible)`. Averaging regional percentages would overweight a region with few eligible users.

### Example 4

An order total joined to five lines repeats five times. The query aggregates lines to order grain first, validates one row per order, then joins and rolls up customers.

### Example 5

Daily revenue groups event timestamps in `Europe/Stockholm`. The query converts from authoritative UTC under a versioned timezone database and tests daylight-saving days rather than assuming 24 hours.

### Example 6

An array of event IDs includes `ORDER BY occurred_at,id` inside the aggregate. An outer report order does not determine array element order.

### Example 7

A rollup contains a real null-region detail row and a grand total. `GROUPING(region)` yields 0 and 1 respectively, so presentation can label them without corrupting the source key.

### Example 8

Four workers produce average states `(count,sum)`. The finalizer adds both components then divides; averaging the four worker averages would be wrong under unequal partitions.

### Example 9

Floating totals differ in low bits after parallel plan change. A financial report switches to bounded exact decimal/minor units; a scientific metric uses tolerance and records algorithm/version.

### Example 10

A million distinct user IDs make exact per-group sets spill. The team either provisions and measures exact computation or adopts a documented sketch with tested relative error, seed/hash/version, merge compatibility, and non-billing use.

## Cross-Program Connections

- [Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) explains finite representations, overflow, memory, and low-level numerical behavior.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies stable online algorithms, mergeable state, error analysis, and resource-aware evaluation.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) operationalizes incremental aggregation, late data, replay, watermarks, and reconciliation.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) owns grain, dimensions, measures, units, semantic models, and history.
- [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md) develops partial aggregation, shuffle, skew handling, and approximate sketches.

## References

1. [PostgreSQL 18 Documentation, GROUP BY and HAVING](https://www.postgresql.org/docs/18/queries-table-expressions.html#QUERIES-GROUP)
2. [PostgreSQL 18 Documentation, Aggregate Functions](https://www.postgresql.org/docs/18/functions-aggregate.html)
3. [PostgreSQL 18 Documentation, Aggregate Expressions](https://www.postgresql.org/docs/18/sql-expressions.html#SYNTAX-AGGREGATES)
4. [PostgreSQL 18 Documentation, Grouping Sets, Cube, and Rollup](https://www.postgresql.org/docs/18/queries-table-expressions.html#QUERIES-GROUPING-SETS)
5. [PostgreSQL 18 Documentation, SELECT](https://www.postgresql.org/docs/18/sql-select.html)
6. [SQLite Documentation, Built-in Aggregate Functions](https://www.sqlite.org/lang_aggfunc.html)
7. [MySQL 8.4 Reference Manual, Aggregate Function Descriptions](https://dev.mysql.com/doc/refman/8.4/en/aggregate-functions.html)
8. [MySQL 8.4 Reference Manual, Handling of GROUP BY](https://dev.mysql.com/doc/refman/8.4/en/group-by-handling.html)

## Exercises

### Exercise 1

Derive `COUNT(*)`, `COUNT(x)`, `SUM(x)`, and `AVG(x)` for empty, all-null, mixed-null, and duplicate-value groups. State output row existence.

### Exercise 2

Design a grouped revenue and conversion query after joining orders, lines, customers, and campaign touches without fanout or denominator corruption.

### Exercise 3

Prove the correct partial-state merge for average and design validation for variance under large close floating values.

### Exercise 4

Design a rollup report containing real null dimension values, subtotals, grand totals, deterministic ordering, and reconciliation invariants.

### Exercise 5

Prepare a correctness/performance evidence plan for a high-cardinality aggregation that may spill and may use an approximate distinct sketch.

## Answers to the Exercises

### Answer 1

For a global aggregate on empty input, one result row normally has `COUNT(*)=0`, `COUNT(x)=0`, `SUM(x)=NULL`, and `AVG(x)=NULL`; explicit grouping yields no group row. For an existing group with two null `x` values: counts are 2 and 0, sum/average null. For values `(NULL,2,4)`: counts 3 and 2, sum 6, average 3. For `(2,2,4)`: counts 3/3, sum 8, average `8/3` in the aggregate return type; duplicates contribute. `DISTINCT` would change the argument bag, but should not be introduced unless value distinctness is the question.

### Answer 2

Declare grains: one order, one line, one customer, and potentially many touches per order. Aggregate line amount to one row/order first and validate it against authoritative order totals. Select one attribution rule—first/last touch, fractional weights summing to one, or a separate multi-touch measure—rather than joining all touches and summing full revenue. Join each order to one customer under tenant key. Group campaign with `sum(attributed_revenue)`, `sum(converted)`, and `sum(eligible)`, then compute conversion from totals. Reconcile order counts/revenue before and after every join, unmatched/orphan categories, attribution weights, null currency, and campaign totals to the authoritative population.

### Answer 3

For partition states `(n_i,s_i)` over nonnull inputs, merged state is `(sum n_i,sum s_i)` and final mean is `sum s_i/sum n_i` when count is positive. This equals the full-data sum/count because bag union makes both components additive; mean alone lacks the weights. For variance, compare the engine's documented population/sample results with a high-precision reference and stable Welford/merge implementation using empty, one-value, constant, symmetric, huge-baseline-small-delta, skewed-partition, null, and overflow cases. Test serial/parallel plans and tolerances; do not use the cancellation-prone difference of large squares as authority.

### Answer 4

Emit dimension keys plus `GROUPING` bits for detail `(region,product)`, region subtotal `(region)`, and grand total `()`. Retain real null dimension values and use bits—not `COALESCE` alone—to label levels. Order by grouping level, explicit null policy, region, product, and stable keys. For additive compatible measures, sum detail rows within each region and compare to its subtotal; sum region subtotals and compare to grand total. Separately reconcile count, nonnull count, currency/unit, and filtered-measure populations, avoiding summing rows across levels together.

### Answer 5

Freeze source snapshot, grain, key equality/collation, nulls, measure types, and exact expected results on a representative sample. Record input/groups/distinct estimates and actuals, per-key frequency/skew, memory, spill partitions/temp I/O, CPU, workers, shuffle, bytes, latency distributions, failures, and output order. Test empty/all-null, one massive group, all unique, hot keys, overflow, and concurrency. For a sketch, document algorithm, precision, hash/seed, serialized/version format, merge order/compatibility, theoretical bound, and prohibited uses; measure bias/error distributions against exact counts across cardinalities and adversarial distributions. Preserve exact reconciliation for billing/compliance paths.
