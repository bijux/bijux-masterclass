---
module_id: DBE-015
program: Database Engineering
level: 1
module_number: 15
title: Window Functions
status: complete
last_verified: 2026-08-30
---

# Window Functions

## One-Page Review

### Governing question

How can a query compare each row with related rows, rank or offset them, and compute cumulative or moving measures without losing row identity or making ordering and frame semantics accidental?

### Essential definitions

A **partition** is the subset of query rows sharing a window's `PARTITION BY` values. The window **order** sequences rows inside a partition; equal order values form a **peer group**. A **frame** is the moving subset read by frame-sensitive functions for the current row. `ROWS` counts physical positions, `GROUPS` counts peer groups, and `RANGE` uses order-value relationships under dialect rules. `ROW_NUMBER`, `RANK`, and `DENSE_RANK` assign different positions around ties. `LAG` and `LEAD` address rows at offsets in window order. A named window centralizes a reusable partition/order/frame specification.

### Central model, mechanism, or theorem

For query bag `R`, partition key `p`, and window ordering relation `≺`, row `r` belongs to `P(r)={x in R | p(x)=p(r)}`. A total order gives every occurrence a deterministic position. A frame rule derives `F(r)`, a sub-bag of `P(r)`, from that position or its peer group. A frame-sensitive result is `f(F(r),r)`; ranking and offset functions instead use the ordered partition according to their own contract. Correctness therefore requires four separate declarations: partition identity, peer/order keys, deterministic tie-breakers where row identity matters, and frame boundaries.

### Critical invariants

- Windowing preserves one output occurrence per input occurrence unless a later query layer filters it.
- `PARTITION BY` defines independent populations; it does not collapse rows like `GROUP BY`.
- The window's `ORDER BY` determines analytic order but does not guarantee final presentation order.
- Row-sensitive selection uses a total deterministic order, including a stable tie-breaker.
- Peer-sensitive rankings intentionally omit tie-breakers from the peer definition when ties should share rank.
- Every aggregate window states an explicit frame when cumulative, moving, or whole-partition semantics matter.
- `LAG`/`LEAD` offset, default, null, and boundary behavior are domain decisions.
- Plans, sorts, memory, spill, parallelism, and index claims are verified on the target engine and workload.

### Common failures

Failures include omitting a tie-breaker from `ROW_NUMBER`, adding a unique ID to `RANK` and thereby erasing ties, confusing window order with final order, relying on the default frame, expecting `LAST_VALUE` to mean the last row of the partition, treating `ROWS` and `RANGE` as synonyms, filtering a window alias in `WHERE` where unsupported, calculating a window before the intended filter/grain boundary, dividing by zero in percent change, using `LAG` over duplicate timestamps without an event order, and assuming a covering index removes every sort or spill.

### Compact example

Team A has events `(time,amount)` `(1,10)`, `(2,20)`, `(2,30)`, `(4,40)`. Ordered by `(time,id)`, row-based running sums are 10, 30, 60, 100. A peer-aware cumulative range ordered only by time yields 10, 60, 60, 100 because both time-2 peers enter together. Ranks by time are 1, 2, 2, 4; dense ranks are 1, 2, 2, 3. `LAST_VALUE` over an explicit whole-partition frame is 40 for every A row.

### Connections

[DBE-013](013-aggregation-and-grouping.md) defines grouped aggregates and grain. [DBE-014](014-subqueries-and-common-table-expressions.md) supplies the outer query needed to filter window results portably. Later modules cover execution plans, indexes, sorting, memory, spill, statistics, and distributed query processing. Data Engineering uses the same ideas for event-time deduplication, change capture, and analytical pipelines.

## Governing Question

Ordinary aggregation replaces many detail rows with a group row. Many engineering questions need both levels simultaneously: each invoice beside the customer lifetime total, each event beside its predecessor, the latest version per key, a running balance, a seven-observation mean, or the top three results within every category. Window functions provide this relationally, but concise syntax hides several independent semantic choices.

The governing question is not merely which function name to use. It is which rows constitute the population, which order defines before and after, whether ties are peers or distinct occurrences, which subset a frame contains, and at what logical query boundary the computation occurs. A correct result must remain correct under duplicate values, nulls, reordered storage, new access paths, parallel plans, and engine upgrades.

## Why This Matters

Window functions are central to reporting, billing, monitoring, fraud analysis, data quality, event processing, and application read models. A nondeterministic latest-row query can choose different records after a vacuum, index change, or replica execution. A default peer-aware frame can jump a running balance across same-time transactions. A supposed partition total can become a running total merely because `ORDER BY` was added. These errors often return plausible numbers and pass shallow tests.

Windows also expose boundary and causality questions. `LAG(value)` means little until the order is total and the relation between adjacent rows is valid. A missing previous row may mean the start of a customer history, an ingestion gap, or an excluded event. A moving average over three rows is not a three-day average when dates are sparse. Ranking ties requires a product rule: competition rank, dense category rank, or arbitrary but deterministic row selection.

At scale, several windows with incompatible orders can require several sorts. Large partitions can consume working memory and spill. Skew can place most rows in one partition. An index may provide some useful order, but filters, joins, grouping, collation, null placement, and the exact partition/order prefix affect whether it can be reused. Logical correctness and physical evidence must therefore be reviewed separately.

## Prerequisites and Retrieval

Retrieve bags and multiplicity; stable entity keys; total and partial orders; equality, null, and three-valued logic; grouping and aggregation; subqueries and CTEs; numeric types; timestamps and time zones; sorting; indexes; query plans; memory and external sorting; and transaction snapshots.

Distinguish the input relation from each window partition, partition from frame, order value from row identity, ties from duplicates, ranking from row selection, window order from final result order, observation count from elapsed time, null input from missing offset row, and logical window semantics from the engine's chosen sort and execution strategy.

## Learning Objectives

After this module, you should be able to:

1. define a window partition, order, peer group, and frame precisely;
2. contrast window aggregation with ordinary grouped aggregation;
3. derive `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `NTILE`, `PERCENT_RANK`, and `CUME_DIST` results;
4. design deterministic top-per-group and latest-row queries;
5. reason about `LAG`, `LEAD`, `FIRST_VALUE`, `LAST_VALUE`, and `NTH_VALUE` boundaries;
6. choose and derive `ROWS`, `GROUPS`, and `RANGE` frames;
7. place filters and query layers around window evaluation correctly;
8. define null, timestamp, tie, and numeric policies for analytic calculations;
9. reuse compatible specifications with named windows; and
10. diagnose sorts, memory, spill, skew, and index opportunities without confusing plans with semantics.

## Core Exposition

A window function has an `OVER` clause. Without `PARTITION BY`, all query rows form one partition. With it, rows with equal partition expressions share a partition under the database's equality, type, and collation rules. Unlike `GROUP BY`, partitioning does not reduce cardinality: each input occurrence remains an output occurrence, decorated with a result derived from related rows.

The rows visible to windows have already passed the query's `FROM`, `WHERE`, grouping, and `HAVING` boundaries in the documented logical model. This allows a window to operate on grouped results, such as ranking departments by `SUM(revenue)`. It also means a window result generally cannot be referenced by the same query block's `WHERE`; use a subquery or CTE, or a dialect-specific post-window filter where supported. Apply filters in the correct layer because moving a filter can change the population and every derived value.

`ORDER BY` inside `OVER(...)` defines analytic order inside each partition. It is separate from the query's final `ORDER BY`. The engine may use one physical sort for both when legal, but syntax and semantics remain distinct. A report needs an explicit final total order even when a window happens to emit rows in analytic order.

An order is total for the relevant occurrences when every pair has a deterministic sequence. `ORDER BY occurred_at` is not total when timestamps tie. For `ROW_NUMBER`, latest-version selection, `LAG`, or running ledgers, append stable tie-breakers such as source sequence and immutable event ID. Do not use a mutable value or storage location as authority. State null placement and collation because dialect defaults vary.

Peer groups are rows equal on the window's order expressions. Ranking functions deliberately expose peer semantics. `ROW_NUMBER` assigns 1, 2, 3, ... to occurrences and therefore needs a total order for deterministic identity. `RANK` gives peers the same position and leaves gaps: scores 100, 90, 90, 80 receive 1, 2, 2, 4. `DENSE_RANK` gives 1, 2, 2, 3. If a unique ID is added to the ranking window order, no two rows remain peers; often the correct design uses one peer order for rank and a separate total order for deterministic display.

`PERCENT_RANK` scales rank as `(rank-1)/(partition_rows-1)` with a defined singleton result in supporting engines. `CUME_DIST` is the fraction of partition rows whose order position is at or before the current peer group. `NTILE(n)` assigns ordered rows to numbered buckets whose sizes differ by at most one, but tied values can be split because buckets allocate occurrences. Quantile terminology must say whether it concerns row buckets, values, interpolation, or an approximate distribution algorithm.

Top-per-group is commonly implemented by computing `ROW_NUMBER() OVER (PARTITION BY business_key ORDER BY preference DESC, stable_id)` and filtering to one in an outer query. This is correct only if the preference order fully encodes authority. If two source versions conflict, an arbitrary ID tie-breaker gives determinism but not business truth. Record source precedence, effective time, ingestion sequence, deletion/correction policy, and audit the discarded candidates.

`LAG(value,offset,default)` returns the value evaluated at an earlier ordered partition row; `LEAD` looks later. The default offset is commonly one and an out-of-range result commonly defaults to null, but a real prior value can also be null. A sentinel default can distinguish missing row only when it cannot collide with valid values, or compute an accompanying row count/position. Negative, zero, dynamic, or null offsets and null-skipping options vary by engine and version; consult the target documentation.

Change calculations require domain safeguards. `current - lag(current)` is an absolute change. Percent change needs a policy for a missing, null, or zero predecessor and a numeric type that avoids unintended integer division or overflow. For counters, a decrease may be a reset or wrap, not negative activity. For timestamps, `LAG` compares adjacent observations, not necessarily adjacent time intervals.

Frame-sensitive functions read a subset of the partition associated with the current row. Aggregate functions used with `OVER`, plus `FIRST_VALUE`, `LAST_VALUE`, and `NTH_VALUE`, are important examples. Ranking and offset functions have their own ordered-partition definitions and may ignore a written frame in some dialects. Never infer that every window function consumes the same frame just because it shares a named window.

`ROWS` boundaries count ordered row positions. `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` contains at most three occurrences, not three days. With tied order values, two peers can receive different `ROWS` frames because they occupy different positions; a deterministic tie order is therefore essential when order-sensitive aggregate results must be reproducible.

`GROUPS` boundaries count peer groups. `GROUPS BETWEEN 1 PRECEDING AND CURRENT ROW` includes the current peer group and the immediately preceding distinct order-value group. It is useful when ties must move together. Support differs: SQLite and PostgreSQL document `GROUPS`, while MySQL 8.4 documents it as unsupported even though parsed.

`RANGE` is value/peer based. With a simple cumulative frame ending at `CURRENT ROW`, current peers enter together. Offset `RANGE` rules, permitted order expressions, interval syntax, numeric requirements, and null behavior are dialect-specific. It can represent a time/value band when supported, but “last seven calendar days” still requires a named timestamp, time zone, inclusivity, and sparse-event policy.

Default frames are dangerous because adding a window `ORDER BY` often changes an aggregate from whole-partition behavior to a cumulative peer-aware frame. PostgreSQL and SQLite document a default that extends from the partition start through the current row's last peer when ordering exists. Thus `SUM(x) OVER (PARTITION BY account)` is a partition total, while `SUM(x) OVER (PARTITION BY account ORDER BY time)` is generally cumulative under the default. State `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` for row-by-row cumulative intent, or `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` for an explicit whole-partition frame.

The default also surprises `LAST_VALUE`: if the frame ends at the current peer group, the last value is not the partition's final value. For the final partition value, specify a whole-partition frame with a total order. For the current row's value, selecting the column is clearer. `FIRST_VALUE` can appear to work under both frames because the frame starts at the partition beginning; that coincidence should not hide an underspecified frame.

Frame exclusion can remove the current row, its peer group, or ties in supporting dialects. This helps compare a row with “others,” but support and exact options differ. A portable alternative can use algebraic subtraction, a self-join, or a correlated subquery, each with null, duplicate, and cost implications. MySQL 8.4 documents `EXCLUDE` as unsupported; SQLite documents all standard exclusion forms. Do not advertise portable syntax after testing only one engine.

Nulls participate at several layers. Partition expressions can group nulls. Order expressions place nulls according to dialect/default or explicit syntax where supported. Aggregate windows ordinarily follow their aggregate null rules. Offset/value functions can return null because a row is missing or because the addressed expression is null. `IGNORE NULLS` support varies; PostgreSQL 18 documents only standard-respecting behavior for its listed functions, and MySQL 8.4 documents `IGNORE NULLS` as parsed but rejected. Emulate carefully and test boundary cases if the target lacks the option.

Named windows reduce duplication: define a partition/order once and reuse it. Extension rules—whether a referenced window may add order or frame clauses and which combinations are legal—are dialect-specific. A name improves consistency but does not prove two calculations need identical frames. Often a base named partition/order is extended with explicit frames for cumulative and whole-partition measures.

Several window calculations can be layered. A window function generally cannot be nested directly inside another in the same expression. Compute the first result in a subquery/CTE, then apply a later window in the outer query. Each layer creates a new relation and possibly a new grain/order requirement. Verify that projection and filtering retain the stable keys needed for deterministic downstream windows.

Running totals over financial ledgers require more than syntax. Define which records are posted, opening balance, currency/unit, reversal treatment, effective versus recorded time, tie sequence, transaction snapshot, numeric type, and reconciliation equation. An unbounded-preceding frame can be expensive for arbitrary aggregates, though engines optimize common cumulative state. Never replace an authoritative stored balance without a reconciliation and correction model.

Moving calculations need a denominator contract. `AVG(x) OVER (ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)` averages available nonnull inputs, so early rows and nulls change the count. If exactly three observations are required, gate on `COUNT(x)` over the same frame. If three elapsed days are required, use a supported time range or a calendar relation and define missing days. A centered frame uses future rows and is unsuitable for causal online features unless delayed intentionally.

Sessionization and gap detection compare adjacent timestamps, mark a new session when the gap exceeds a threshold, then cumulatively sum the marks. This uses at least two logical window layers because the cumulative aggregate consumes a result derived from `LAG`. Define equality at the threshold, event-time corrections, late arrivals, time zones, and stable order. Data Engineering revisits these issues under streaming watermarks and retractions.

Window plans often sort by `(partition keys, order keys)`, then process partitions. Compatible windows may reuse an order; incompatible directions, collations, or keys may require more sorting. Existing index order can help when its leading keys and direction/null semantics align after filters and joins, but a plan may still sort or spool. Inspect actual plans, row estimates, sort method, memory, temporary I/O, partition skew, and repeated scans.

Large or unbounded partitions increase memory and latency, especially for functions needing future rows or entire frames. Whole-partition values may delay output. A single hot tenant can dominate a worker. Bound the query population by legitimate predicates, pre-aggregate only when grain permits, align compatible windows, and choose indexes from measured access patterns. Never add a partition key merely to improve performance if it changes the question.

Concurrency and snapshots matter. A statement usually observes a database-defined snapshot, but multi-statement pagination or repeated ranking can see different populations depending on isolation. A deterministic order cannot compensate for rows appearing or disappearing between statements. For exported rankings or balances, record as-of/snapshot, inputs, query and schema version, parameters, engine version, and reconciliation checks.

Testing must use adversarial fixtures: empty input; singleton partitions; all peers; no peers; duplicate full values with distinct identities; null partition/order/value fields; same timestamp with different sequence; missing offset; zero predecessor; partition skew; and rows exactly on frame boundaries. Derive expected rows manually or with an independent semantic model, then compare live dialect output and plans. A successful execution alone does not establish that the intended population, order, frame, or business authority was correct.

## Definitions and Notation

For query bag `R`, partition key `p`, and row `r`:

- `P(r)={x in R | p(x)=p(r)}` is the ordered partition after applying a window order;
- peers share all window `ORDER BY` values;
- `pos(r)` is deterministic only under a total order over occurrences;
- `rank(r)=1 + count(x in P(r) whose order value is strictly before r's peer value)`;
- `dense_rank(r)=1 + count(distinct peer values strictly before r's peer value)`;
- `F(r)` is the frame produced by frame unit, boundaries, and exclusion;
- a window aggregate returns `A(F(r))`, while a partition aggregate has `F(r)=P(r)` for every row.

Bag multiplicity remains relevant: two identical-looking rows are two occurrences unless a prior operation removes one. A stable identity key lets a total order distinguish them without necessarily changing a separate peer-based rank definition.

## Mechanisms, Invariants, or Proof Structure

A window-query review should:

1. state input and output grain, population filters, snapshot, and business authority;
2. define partition expressions and prove they isolate the intended populations;
3. define peer order separately from deterministic occurrence order where ties matter;
4. state null placement, collation, timestamp/time-zone, and stable tie-breakers;
5. classify each function as ordered-partition or frame-sensitive under the target dialect;
6. write explicit frame unit, start, end, and exclusion for cumulative, moving, and whole-partition claims;
7. place post-window filtering in a legal outer boundary without changing the population prematurely;
8. derive empty, singleton, peer, null, missing-offset, and boundary cases;
9. reconcile totals, ranks, selected identities, and denominators by an independent route; and
10. inspect actual order reuse, sorts, memory, spill, skew, latency, cancellation, and version-specific behavior.

The finite model below derives ranking, row-based and peer-aware cumulative sums, offsets, partition totals, and explicit whole-partition last values. It models fixed integer data and deterministic tuple ordering; it is not a SQL parser, database executor, collation model, or performance benchmark.

<!-- bijux-verify: {"id":"finite-window-semantics","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"window_rows=(('A', 'a1', 1, 10, 1, 1, 1, 10, 10, None, 100, 40), ('A', 'a2', 2, 20, 2, 2, 2, 30, 60, 10, 100, 40), ('A', 'a3', 2, 30, 3, 2, 2, 60, 60, 20, 100, 40), ('A', 'a4', 4, 40, 4, 4, 3, 100, 100, 30, 100, 40), ('B', 'b1', 1, 5, 1, 1, 1, 5, 5, None, 20, 15), ('B', 'b2', 3, 15, 2, 2, 2, 20, 20, 5, 20, 15))\ntop_two=(('A', 'a1'), ('A', 'a2'), ('B', 'b1'), ('B', 'b2'))\nlatest=(('A', 'a4'), ('B', 'b2'))\npartition_count=2\n","stderr":""}} -->
```python
events = (
    ("A", "a1", 1, 10),
    ("A", "a2", 2, 20),
    ("A", "a3", 2, 30),
    ("A", "a4", 4, 40),
    ("B", "b1", 1, 5),
    ("B", "b2", 3, 15),
)

teams = tuple(sorted({team for team, _, _, _ in events}))
window_rows = []
top_two = []
latest = []
for team in teams:
    partition = tuple(sorted((row for row in events if row[0] == team), key=lambda row: (row[2], row[1])))
    total = sum(row[3] for row in partition)
    distinct_times = tuple(sorted({row[2] for row in partition}))
    for position, row in enumerate(partition):
        _, event_id, event_time, amount = row
        rank = 1 + sum(candidate[2] < event_time for candidate in partition)
        dense_rank = 1 + sum(value < event_time for value in distinct_times)
        rows_sum = sum(candidate[3] for candidate in partition[: position + 1])
        range_sum = sum(candidate[3] for candidate in partition if candidate[2] <= event_time)
        previous = None if position == 0 else partition[position - 1][3]
        window_rows.append(
            (team, event_id, event_time, amount, position + 1, rank, dense_rank, rows_sum, range_sum, previous, total, partition[-1][3])
        )
        if position < 2:
            top_two.append((team, event_id))
    latest.append((team, partition[-1][1]))

print(f"window_rows={tuple(window_rows)}")
print(f"top_two={tuple(top_two)}")
print(f"latest={tuple(latest)}")
print(f"partition_count={len(teams)}")
```

Python tuple ordering, equality, integer arithmetic, and `None` rendering are not SQL type, collation, numeric, or null semantics. The model omits filters, joins, duplicate full rows, time zones, `GROUPS`, offset `RANGE`, exclusions, live dialect restrictions, plans, indexes, memory, spill, concurrency, and parallel execution.

## Alternatives and Trade-Offs

A grouped query plus join can attach partition totals to details and may be clearer when only whole-partition aggregates are needed; windows avoid a separate join but can sort or spool. A correlated subquery expresses local comparison directly but may be decorrelated or may repeat work. Dialect-specific top-per-group syntax can be concise and efficient, while `ROW_NUMBER` plus an outer filter is broadly recognizable and exposes tie policy.

`ROWS` gives exact occurrence counts and deterministic ledger behavior with a total order. `GROUPS` moves peers together but is not universally supported. `RANGE` expresses value bands or peer-aware accumulation but has dialect-specific offset constraints. Pre-aggregation reduces volume but changes grain. Materialized analytical tables reduce repeated cost but add freshness, correction, lineage, and reconciliation obligations.

## Failure Modes and Misconceptions

- “The table has an insertion order.” Relational results need an explicit stable order; storage position is not authority.
- “`ROW_NUMBER` resolves ties.” It assigns numbers, but without a total order the chosen identity is nondeterministic.
- “Add the ID to every rank order.” That makes every row a separate peer and changes tie semantics.
- “The window `ORDER BY` sorts the output.” Only a final query `ORDER BY` guarantees presentation order.
- “The frame equals the partition.” It may, but an ordered default often ends at the current peer group.
- “`LAST_VALUE` returns the partition's last value.” It returns the last value in the current frame.
- “Three preceding rows means three days.” `ROWS` counts occurrences, not elapsed time.
- “Null from `LAG` means no prior row.” The prior row's expression may itself be null.
- “Filter first for efficiency.” Moving a filter before the window can change ranks, offsets, totals, and frames.
- “A passing query proves performance.” Plans depend on data, statistics, indexes, memory, concurrency, engine version, and parameters.

## Worked Examples

### Example 1

A customer partition has payments 10, 20, 30 ordered by sequence 1, 2, 3. `SUM(amount) OVER (PARTITION BY customer_id)` yields 60 on every row. An explicit cumulative `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` yields 10, 30, 60. Same partition, different frames and claims.

### Example 2

Scores 100, 90, 90, 80 have row numbers 1, 2, 3, 4 under a total tie order, ranks 1, 2, 2, 4 under score order, and dense ranks 1, 2, 2, 3. Use the total order for deterministic selection and score-only peers for competition ranking.

### Example 3

Versions for key `k` share effective time. Ordering only by time makes latest-row selection ambiguous. Adding trusted source precedence, ingestion sequence, then immutable event ID is deterministic; the review must still prove that this precedence represents authority rather than merely consistency.

### Example 4

At times 1, 2, 2, 4 with amounts 10, 20, 30, 40, a row-based cumulative frame yields 10, 30, 60, 100 in `(time,id)` order. A peer-aware cumulative range ordered by time yields 10, 60, 60, 100. The time-2 peer group enters as a unit.

### Example 5

`LAST_VALUE(amount)` under a default ordered frame can return the current peer group's last amount. To claim the partition-final amount, use a total order and an explicit frame from unbounded preceding through unbounded following. Verify null ordering and whether the final expression may be null.

### Example 6

Daily observations occur on Monday, Thursday, and Friday. `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` on Friday includes all three observations, spanning five calendar days. A three-day business measure needs a date/time range or calendar join, not a row-count frame.

### Example 7

Counter readings are 90, 100, 5. `LAG` gives changes 10 and -95, but the negative value may signal a reset. The query should surface reset evidence and apply a domain rule; silently treating it as ordinary negative usage corrupts the total.

### Example 8

To keep the top two rows per department, compute `ROW_NUMBER` in a subquery over `(salary DESC, employee_id)` and filter `row_number <= 2` outside. Filtering employees before ranking changes the population; filtering the alias in the same `WHERE` is illegal in PostgreSQL and MySQL's documented query blocks.

### Example 9

A moving average with frame `2 PRECEDING` sees one row at the partition start, two on the next row, then up to three. Pair it with `COUNT(value)` over the identical frame and publish only when the required denominator is met. Null values reduce the aggregate denominator unless explicitly replaced under a domain rule.

### Example 10

Three analytic expressions use `(tenant_id, occurred_at, event_id)` while another orders by amount descending. The first three may share physical ordering; the fourth may need another sort. Confirm with the actual plan and spill metrics. Do not rewrite the fourth order merely to save a sort because that changes its meaning.

## Cross-Program Connections

- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) explains sorting, order statistics, prefix computation, and asymptotic/resource analysis.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) applies ranking and offsets to deduplication, CDC, sessionization, late data, and event-time corrections.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) governs grain, semantic measures, historical identity, and analytical ownership.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) explains snapshots, partition skew, parallel order, and reproducibility across workers.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) requires tenant and authorization filters to be placed before analytic populations are exposed.

## References

1. PostgreSQL Global Development Group, [Window Functions Tutorial](https://www.postgresql.org/docs/18/tutorial-window.html), PostgreSQL 18 documentation.
2. PostgreSQL Global Development Group, [Window Functions](https://www.postgresql.org/docs/18/functions-window.html), PostgreSQL 18 documentation.
3. PostgreSQL Global Development Group, [Window Function Calls](https://www.postgresql.org/docs/18/sql-expressions.html#SYNTAX-WINDOW-FUNCTIONS), PostgreSQL 18 documentation.
4. PostgreSQL Global Development Group, [Window Function Processing](https://www.postgresql.org/docs/18/queries-table-expressions.html#QUERIES-WINDOW), PostgreSQL 18 documentation.
5. SQLite Project, [Window Functions](https://www.sqlite.org/windowfunctions.html), including frames, exclusion, chaining, and history.
6. Oracle, [Window Function Concepts and Syntax](https://dev.mysql.com/doc/refman/8.4/en/window-functions-usage.html), MySQL 8.4 Reference Manual.
7. Oracle, [Window Function Frame Specification](https://dev.mysql.com/doc/refman/8.4/en/window-functions-frames.html), MySQL 8.4 Reference Manual.
8. Oracle, [Window Function Restrictions](https://dev.mysql.com/doc/refman/8.4/en/window-function-restrictions.html), MySQL 8.4 Reference Manual.

## Exercises

### Exercise 1

For ordered amounts `(time,id,amount)` `(1,a,10)`, `(2,b,20)`, `(2,c,30)`, `(4,d,40)`, derive row number under `(time,id)`, rank and dense rank under `time`, cumulative `ROWS` sum under `(time,id)`, and cumulative peer-aware `RANGE` sum under `time`.

### Exercise 2

Design a deterministic latest-address-per-customer query contract. State the partition key, preference order, tie-breakers, null policy, deletion/correction policy, and why determinism alone does not prove authority.

### Exercise 3

A sensor has observations at days 1, 4, and 5 with values 10, 20, 30. Compare a three-row moving average with a three-calendar-day moving average at day 5. State boundary and missing-day policies.

### Exercise 4

Explain why `LAST_VALUE(x) OVER (PARTITION BY k ORDER BY t)` can fail to return the final partition value. Write the semantic window specification needed for a deterministic partition-final value and list two remaining portability checks.

### Exercise 5

Propose an evidence plan for a query with four windows over a 200-million-row tenant/event table. Cover correctness fixtures, population/grain, order and frame review, plan evidence, index hypotheses, skew, memory/spill, concurrency, cancellation, and upgrade regression.

## Answers to the Exercises

### Answer 1

In `(time,id)` order, row numbers are 1, 2, 3, 4. Under time-only peers, ranks are 1, 2, 2, 4 and dense ranks are 1, 2, 2, 3. `ROWS UNBOUNDED PRECEDING` sums are 10, 30, 60, 100. A cumulative peer-aware `RANGE` ordered by time gives 10, 60, 60, 100 because both time-2 rows share the same frame endpoint. A target dialect must be checked for its exact default and `RANGE` rules.

### Answer 2

Partition by immutable customer identity. Order valid, nondeleted candidates by business-effective time descending, trusted source precedence, source sequence, then immutable record ID. Define null timestamps and whether corrections replace or append; retain rejected candidates and provenance. The final ID makes selection repeatable, but only a domain-approved precedence and correction policy establishes which address is authoritative.

### Answer 3

The three-row frame at day 5 contains days 1, 4, 5 and averages to 20. A trailing three-calendar-day interval includes days 3 through 5 under an inclusive policy, so it sees days 4 and 5 and averages to 25. Specify time zone, endpoint inclusivity, whether absent days contribute nothing or imputed values, and whether the current observation is included.

### Answer 4

An ordered default frame commonly ends at the current row's last peer, so `LAST_VALUE` sees the current frame rather than the partition tail. Use a total order such as `(t,event_id)` and `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`. Still verify dialect support/defaults and explicit null ordering or null-treatment behavior; also confirm that the final row is authoritative under the domain rule.

### Answer 5

Build independently derived empty, singleton, peer, null, duplicate-time, boundary, and hot-tenant fixtures. State the post-filter input grain and snapshot, then review every partition/order/tie/frame and reconcile selected rows and totals. On production-shaped data, capture actual plans, estimates, sort reuse, index access, memory, temporary I/O, partition-size distribution, latency, and cancellation behavior under concurrency. Test proposed indexes against write/storage cost, retain engine/configuration/statistics versions, and rerun semantic fixtures plus plan/resource thresholds before upgrades.
