---
module_id: DBE-012
program: Database Engineering
level: 1
module_number: 12
title: Joins and Join Semantics
status: complete
last_verified: 2026-08-30
---

# Joins and Join Semantics

## One-Page Review

### Governing question

How do joins combine related row occurrences under SQL bag and null semantics, and how can an engineer preserve intended cardinality, unmatched rows, authorization scope, and temporal meaning?

### Essential definitions

A **cross join** forms every left/right pair. An **inner join** retains pairs whose join condition is `TRUE`. A **left outer join** adds one null-extended right side for each left row with no true match; right and full outer joins preserve the corresponding sides. A **semi join** returns each left occurrence that has at least one match, without duplicating it per right match. An **anti join** returns left occurrences with no match. **Join cardinality** is output occurrence count, not the count of distinct entities. A **fanout** occurs when one input row matches multiple rows on the other side.

### Central model, mechanism, or theorem

For bags `L` and `R` with equality key `k`, inner-join cardinality is

`|L join R| = sum_v count_L(v) * count_R(v)`

over values that compare `TRUE`; ordinary null equality does not match. Outer joins first produce true matches and then null-extend unmatched preserved rows. A predicate in `ON` participates in match formation; a predicate in `WHERE` evaluates after null extension and can remove preserved rows. Keys, constraints, and pre-join cardinality checks are the basis for proving one-to-one, many-to-one, one-to-many, or many-to-many behavior.

### Critical invariants

- Every join states its business relationship, complete key, tenant/scope fields, and expected multiplicity.
- Column references are qualified and output names are intentional.
- Null-key behavior is explicit; equality is not assumed null-safe.
- Outer-join predicates are classified as match conditions or post-join filters.
- Primary/unique and foreign-key constraints support cardinality claims where applicable.
- Semi/anti existence questions use `EXISTS`/`NOT EXISTS` or a proven equivalent.
- Many-to-many fanout is expected, bounded, and tested before aggregation.
- Temporal/range joins define interval boundaries, overlap policy, and tie resolution.

### Common failures

Failures include omitting part of a composite or tenant key, using a cross join accidentally, confusing entity rows with joined occurrences, applying `DISTINCT` after an unintended fanout, moving a right-side predicate from `ON` to `WHERE` on a left join, using `NOT IN` with nullable subquery values, matching nulls unintentionally through sentinels, selecting `*` from colliding schemas, using `NATURAL JOIN` across schema evolution, chaining outer joins without parentheses/reasoning, joining current facts to multiple overlapping history rows, and tuning join algorithms before proving result semantics.

### Compact example

Customers 1 and 2 have two and one orders; customer 3 has none. Inner join yields three pairs. Left join also emits `(3,NULL)`. Two orders have no matching customer: one has a null foreign key and one references 9; full join preserves both on the right. Filtering `status='paid'` in `ON` preserves customer 3 as null-extended, while placing it in `WHERE` removes that row. `EXISTS` returns customers 1 and 2; `NOT EXISTS` returns customer 3.

### Connections

[DBE-003](003-schemas-keys-and-constraints.md) supplies keys, [DBE-011](011-selection-projection-and-ordering.md) supplies predicates and bags, and [DBE-013](../ROADMAP.md) aggregates joined results. Data Architecture supplies entity/grain modeling; Security Engineering supplies tenant and authorization scope.

## Governing Question

A join states which occurrences from two derived tables can coexist in an output row. It is both a logical relationship and a multiplicity operator. If one customer matches three orders, the customer's values appear three times. If two supposedly unique dimension rows match one fact, measures double. If no right row matches a left outer join, the output contains right-side null placeholders that are not necessarily stored nulls.

The task is to derive expected output from keys, predicates, nulls, and bag multiplicities before considering nested-loop, hash, or merge execution. A fast wrong join is wrong; a row-count coincidence is weak evidence. Production review must cover orphaned data, schema evolution, tenant boundaries, late/overlapping history, authorization filters, and concurrent snapshots.

## Why This Matters

Join mistakes frequently produce plausible results. Omitting tenant ID from `tenant_id,customer_id` can connect records across organizations. Joining facts to a nonunique name can multiply revenue. `DISTINCT` may hide the duplicated rows while preserving a wrong sum. An outer join intended to retain all customers can silently become inner-like when a nullable right predicate is placed in `WHERE`.

Null complicates matching. `NULL = NULL` is `UNKNOWN`, not true, so nullable keys do not match under ordinary equality. `NOT IN` can become unknown for every candidate when its subquery contains null; `NOT EXISTS` expresses absence more robustly. Null introduced by an outer join must also be distinguished from a real nullable right column.

Join structure shapes cost. Cardinality error propagates into join order, algorithm, memory, spill, and downstream aggregation. But physical tuning should start only after the relationship, grain, and multiplicity are correct and constrained.

## Prerequisites and Retrieval

Retrieve relations, bags, Cartesian product, predicates, three-valued logic, keys, foreign keys, uniqueness, null, aliases, constraints, indexes, snapshots, intervals, aggregation, cardinality estimation, and query plans.

Distinguish join condition from post-join filter; null-extended marker from stored null; entity cardinality from occurrence cardinality; semantic join nesting from physical join order; semi join from inner join plus distinct; anti join from nullable `NOT IN`; and current-state equality join from temporal as-of matching.

## Learning Objectives

After this module, you should be able to:

1. derive cross, inner, left, right, and full outer join results;
2. calculate bag join multiplicity from per-key counts;
3. explain `ON` versus `WHERE` behavior for outer joins;
4. specify composite, tenant, null, and collation-aware keys;
5. identify and bound one-to-one, many-to-one, one-to-many, and many-to-many fanout;
6. express existence and absence with semi/anti semantics;
7. reason about self, lateral, range, and temporal joins;
8. preserve meaning in nested outer joins and optimizer rewrites;
9. design constraints and tests that support join claims; and
10. inspect execution evidence only after logical correctness is established.

## Core Exposition

The Cartesian product `L x R` contains one occurrence for every left/right occurrence pair. If `L` has `N` rows and `R` has `M`, the cross join has `N*M`, including duplicates. Cross join is appropriate for deliberate combinations such as every scenario with every region, but an omitted condition can cause explosive accidental fanout.

An inner join applies a condition to product pairs and keeps only `TRUE`. `FALSE` and `UNKNOWN` pairs do not match. The condition can include equality, inequalities, ranges, spatial predicates, or arbitrary booleans, though physical support differs. With duplicate keys, every matching occurrence pairs with every occurrence on the other side.

For equality by key, make a frequency table first. If key A occurs twice on the left and three times on the right, it contributes six rows. Summing products predicts output and exposes unexpected nonuniqueness. Null keys contribute no ordinary equality matches. The formula applies to each composite key value that compares true under its type/collation semantics.

Keys establish expectations. A join from many orders to a unique customer key is many-to-one: output cannot exceed input orders solely from that relationship, assuming every order occurrence matches at most one customer. A declared foreign key can ensure referenced existence for nonnull values; a unique/primary key bounds matches. Without constraints, uniqueness is a data observation that can fail tomorrow.

Composite relationships require every component. If customer identity is `(tenant_id,customer_id)`, joining only `customer_id` crosses tenants. The same applies to version, locale, source-system, effective-date, and partition dimensions. Constraints and indexes should reflect the actual relationship where possible, and queries must use compatible types/collations without lossy casts.

Aliases name each input role and make self-joins comprehensible. `employee e LEFT JOIN employee manager ON e.manager_id=manager.id` uses one relation twice. Qualify columns, especially keys and predicates. Project deliberate aliases such as `employee_name` and `manager_name`; `SELECT *` produces collisions, hidden coupling, and accidental sensitive exposure.

A left outer join performs true matches, then emits one null-extended right tuple for each left occurrence with no match. If a left row has two right matches, it emits two rows, not one plus a null row. The null extension marks absence of a matching occurrence; a right column may also be null in a real matched row, so test a nonnull right key when detecting unmatched rows.

Right outer join is the converse and can usually be expressed by swapping sides of a left join. Full outer join preserves unmatched occurrences from both sides. Full joins are useful for reconciliation, but coalescing keys can obscure which side was absent. Project side-presence flags and original keys before merging representations.

Predicate placement is semantic. `L LEFT JOIN R ON L.id=R.l_id AND R.active` defines an active right row as a match and preserves each left row without one. `L LEFT JOIN R ON L.id=R.l_id WHERE R.active` first creates matches/null extensions, then retains only rows for which `R.active` is true, normally removing unmatched left rows. Optimizers may transform only when equivalence is proven.

Predicates referring solely to the preserved left side commonly belong in `WHERE` when selecting left entities; placing one in `ON` can preserve excluded left rows as unmatched, contrary to intent. Ask separately: which left rows enter the question, which right rows count as matches, and which derived joined rows pass final filtering?

`USING(a,b)` abbreviates equalities for same-named columns and emits one copy of each using column under dialect rules. It can improve clarity when schemas deliberately align. `NATURAL JOIN` derives its key from every shared column name; adding an unrelated same-named column can silently change results, while no shared columns can degenerate to a cross join. Avoid it in durable production interfaces.

SQL joins are nested table expressions. Inner joins are associative/commutative under appropriate conditions at the logical level, enabling reorder. Outer joins generally are not freely associative because null extension changes later matches. Parenthesize complex outer join trees, qualify predicates, and test unmatched cases. The optimizer may reorder only through transformations it deems equivalent.

A semi join answers whether at least one match exists. SQL commonly expresses it with `EXISTS`. It returns left rows at most at their left multiplicity and ignores how many right matches exist after the first semantically. An inner join plus `DISTINCT` can produce a similar value set in some projections but adds fanout, duplicate-elimination work, and subtle differences when left duplicates or projected columns matter.

An anti join answers whether no match exists and is commonly `NOT EXISTS`. `LEFT JOIN ... WHERE right_nonnull_key IS NULL` can be equivalent when carefully written. `NOT IN (subquery)` follows three-valued logic: a null among candidate values can make the result unknown rather than true, producing surprising emptiness. Use `NOT EXISTS` with an explicit correlation for absence unless a nonnull contract proves equivalence.

Null-safe equality operators are dialect-specific. They can intentionally match two null keys, but that creates groups where “unknown identity” occurrences fan out against each other. Replacing null with a sentinel through `COALESCE` risks collision and may affect indexes/types. Prefer nonnull keys for identity; when null matching is a domain requirement, state equivalence and test multiplicity explicitly.

Many-to-many joins are legitimate—students to courses through enrollment—but should usually be mediated by an association relation whose key prevents duplicate edges and whose attributes describe the relationship. Directly joining two fact tables on a coarse dimension such as date multiplies every left fact by every right fact for that date. Aggregate each to compatible grain first or define the intended pair relation.

Aggregation after joins inherits fanout. `SUM(order.total)` after joining orders to order lines repeats total per line. Aggregate line amounts to order grain, use a semantically correct measure, or restructure. `SUM(DISTINCT order.total)` is not a repair: two different orders may share the same total and be incorrectly collapsed.

Range joins match intervals or inequalities. A price band join must define inclusive/exclusive boundaries and ensure bands do not overlap unless multiple matches are intended. Index support differs. Boundary fixtures should include exact endpoints, gaps, overlaps, nulls, reversed ranges, and extreme values.

Temporal/as-of joins connect a fact timestamp to a version effective during that time, commonly `valid_from <= t AND t < valid_to`. Correctness requires a time zone/precision policy and an invariant that versions for one business key do not overlap. If overlapping versions exist, one fact matches several versions; ordering and limiting inside a lateral subquery may choose one, but that is a conflict-resolution policy, not proof the history is valid.

Lateral joins allow a right derived table/function to refer to a preceding left row in supporting dialects. They express per-row top-N, interval lookup, or dependent expansion. A left lateral join can preserve left rows with no derived result. Because evaluation semantics are correlated, bound per-left work, add total ordering for top-N, and inspect plans; a naive implementation can repeat expensive work.

Join authorization is part of the key. Tenant ID and visibility predicates must constrain every relevant side. Row-level policies can add hidden predicates, but application queries still need correct domain relationships. Joining a permitted entity to an unscoped association can leak existence or values. Test with colliding IDs across tenants and roles.

Physical algorithms do not change logical results. Nested-loop joins repeatedly probe or scan an inner side; hash joins build/probe equality keys; merge joins consume compatible orders. Optimizers choose join order and algorithms using cardinality/cost. Later modules study these mechanisms. Here, inspect actual-versus-estimated rows at each join, loops, memory/spill, filters, and output without treating algorithm choice as semantic evidence.

Join verification uses more than final row count. Reconcile per-key frequencies, unmatched IDs on each side, duplicate keys, null keys, referential violations, and side-presence categories. Assert expected grain and unique keys on output. Compare with independent semi/anti queries. Use small hand-derived fixtures plus production-shaped skew and high-frequency keys.

## Definitions and Notation

For bags `L` and `R`, multiplicities `m_L(l)` and `m_R(r)`, and predicate `theta(l,r)`:

- inner multiplicity for pair `(l,r)` is `m_L(l)*m_R(r)` when `theta` is `TRUE`, else zero;
- equality-key cardinality is `sum_v n_L(v)n_R(v)` over true-comparing nonnull keys under ordinary equality;
- left outer join adds `m_L(l)` null-extended occurrences when no right occurrence makes `theta(l,r)` true;
- semi join retains left occurrence `l` iff `exists r: theta(l,r)=TRUE`;
- anti join retains `l` iff no such `r` exists.

Let `g_L(v)` and `g_R(v)` be observed per-key counts. A claimed many-to-one `L -> R` requires `g_R(v)<=1` for every reachable key, ideally guaranteed by a unique constraint. Output grain is the semantic identity of one result occurrence and must be stated separately from SQL column uniqueness.

## Mechanisms, Invariants, or Proof Structure

A join review should:

1. state output grain and why rows are being related;
2. list complete typed keys, tenant/scope components, null/collation rules, and constraints;
3. compute per-key frequencies and predicted inner cardinality;
4. classify relationship as one-to-one, many-to-one, one-to-many, or many-to-many;
5. derive matched and unmatched outputs for each outer join;
6. label each predicate as left input, match (`ON`), or post-join (`WHERE`) logic;
7. use semi/anti semantics for existence/absence and test nullable adversaries;
8. validate temporal/range nonoverlap, boundaries, gaps, and tie policy;
9. assert output key/grain, per-side reconciliation, and authorization; and
10. inspect plans, estimates, loops, memory/spill, and indexes after semantics pass.

The finite model below computes inner, left, full-unmatched, filtered-on, filtered-after, semi, and anti outcomes for explicit bags. It is not a SQL engine and deliberately uses ordinary nonnull integer equality for matches.

<!-- bijux-verify: {"id":"finite-join-semantics","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"inner_pairs=((1, 101), (1, 102), (2, 103))\nleft_pairs=((1, 101), (1, 102), (2, 103), (3, None))\nfull_unmatched_left=(3,)\nfull_unmatched_right=(104, 105)\non_filtered_pairs=((1, 101), (2, 103), (3, None))\nwhere_filtered_pairs=((1, 101), (2, 103))\nsemi_customers=(1, 2)\nanti_customers=(3,)\ninner_count=3\n","stderr":""}} -->
```python
customers = (
    {"id": 1, "name": "Ada"},
    {"id": 2, "name": "Lin"},
    {"id": 3, "name": "Sol"},
)
orders = (
    {"id": 101, "customer_id": 1, "status": "paid"},
    {"id": 102, "customer_id": 1, "status": "void"},
    {"id": 103, "customer_id": 2, "status": "paid"},
    {"id": 104, "customer_id": None, "status": "paid"},
    {"id": 105, "customer_id": 9, "status": "paid"},
)


def matches(customer, order):
    return order["customer_id"] is not None and customer["id"] == order["customer_id"]


inner = tuple(
    (customer["id"], order["id"])
    for customer in customers
    for order in orders
    if matches(customer, order)
)
left = tuple(
    pair
    for customer in customers
    for pair in (
        tuple((customer["id"], order["id"]) for order in orders if matches(customer, order))
        or ((customer["id"], None),)
    )
)
unmatched_right = tuple(
    order["id"] for order in orders if not any(matches(customer, order) for customer in customers)
)
on_filtered = tuple(
    pair
    for customer in customers
    for pair in (
        tuple(
            (customer["id"], order["id"])
            for order in orders
            if matches(customer, order) and order["status"] == "paid"
        )
        or ((customer["id"], None),)
    )
)
where_filtered = tuple(
    (customer["id"], order["id"])
    for customer in customers
    for order in orders
    if matches(customer, order) and order["status"] == "paid"
)
semi = tuple(customer["id"] for customer in customers if any(matches(customer, order) for order in orders))
anti = tuple(customer["id"] for customer in customers if not any(matches(customer, order) for order in orders))

print(f"inner_pairs={inner}")
print(f"left_pairs={left}")
print(f"full_unmatched_left={tuple(pair[0] for pair in left if pair[1] is None)}")
print(f"full_unmatched_right={unmatched_right}")
print(f"on_filtered_pairs={on_filtered}")
print(f"where_filtered_pairs={where_filtered}")
print(f"semi_customers={semi}")
print(f"anti_customers={anti}")
print(f"inner_count={len(inner)}")
```

Tuple order is fixture construction order, not a SQL output-order promise. The model omits duplicate identical source rows, composite keys, true SQL `UNKNOWN`, collations, lateral/temporal joins, snapshots, authorization, and physical algorithms.

## Alternatives and Trade-Offs

`ON` is explicit and supports all qualified joins; `USING` reduces duplicate same-named keys but changes output shape; `NATURAL` is schema-fragile. Inner join returns each matching pair; `EXISTS` expresses left-side existence without fanout. `NOT EXISTS` is null-robust for anti semantics; left-join-is-null can be readable when a guaranteed-nonnull right marker is used.

Pre-aggregation controls fact-to-fact fanout but changes available detail. Lateral top-one lookup resolves multiple candidates deliberately but can be costly and must be totally ordered. Enforcing nonoverlapping temporal constraints prevents ambiguity earlier but may require specialized constraints/transactions. Denormalizing a frequently joined attribute saves read work but adds synchronization obligations.

## Failure Modes and Misconceptions

“A join connects tables” is underspecified; it relates occurrences under a predicate and bag multiplicity. “Foreign key means one-to-one” is false; it usually supports many referencing rows to one referenced key. “Left join always returns exactly left count” is false when left rows have multiple matches; it returns at least the left occurrence count.

“Move predicates between `ON` and `WHERE`” is unsafe for outer joins. “Null matches null” is false under ordinary equality. “`NOT IN` means no match” can fail with a nullable candidate. “`DISTINCT` repairs fanout” can erase legitimate duplicates and leave aggregates wrong.

“Joins execute left-to-right” confuses syntax/nesting with optimizer physical order. “Hash join is less correct than nested loop” is false when both implement the same semantics. “Matching final count proves correctness” ignores compensating missing/duplicate groups. Reconcile per key and side.

## Worked Examples

### Example 1

Two A rows and three B rows share key 7, contributing `2*3=6` inner-join occurrences. A uniqueness claim on B is disproved even if projected values happen to duplicate-collapse.

### Example 2

Orders join customers on `(tenant_id,customer_id)`. Omitting tenant ID connects tenant A's order to tenant B's same numeric customer ID; colliding-ID fixtures catch the leak.

### Example 3

A left join places `right.active` in `ON` to mean “active right rows count as matches.” Moving it to `WHERE` removes left rows with no active match and changes the question.

### Example 4

A full join reconciliation projects `left_present`, `right_present`, both original IDs, and values before coalescing. It distinguishes left-only, right-only, and mismatched records without losing provenance.

### Example 5

`EXISTS` returns each customer with any order once per customer occurrence, even when one has 100 orders. An inner join returns 100 occurrences unless later reduced, doing a different logical operation.

### Example 6

`NOT IN (SELECT nullable_customer_id ...)` can return no true candidates because of one null. Correlated `NOT EXISTS` returns customers for which no true equality match exists.

### Example 7

Joining order totals to line rows repeats each total per line. The review asserts output grain `order_line`, then computes revenue from line amounts or aggregates lines to order before comparing order totals.

### Example 8

An as-of price join uses `valid_from <= ordered_at AND ordered_at < valid_to`. A constraint/audit rejects overlapping ranges; otherwise one order can match multiple prices.

### Example 9

A self-join names roles `employee` and `manager`. A left join preserves the chief executive with no manager; filtering manager department in `WHERE` would remove that employee.

### Example 10

A many-table plan underestimates an early join by 1,000x due to correlated keys, then spills downstream. Statistics/index experiments follow only after per-key multiplicity and query semantics are independently verified.

## Cross-Program Connections

- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies hash tables, ordered trees, and merge/search complexity behind joins.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) uses joins for enrichment, deduplication, temporal dimensions, and reconciliation under late data.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) owns entity identity, grain, relationships, history, and conformed keys.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies tenant scoping, row policy, authorization, and leakage analysis.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) explains colocated versus distributed joins, skew, shuffle, and snapshot consistency.

## References

1. [PostgreSQL 18 Documentation, Joined Tables](https://www.postgresql.org/docs/18/queries-table-expressions.html#QUERIES-JOIN)
2. [PostgreSQL 18 Documentation, SELECT](https://www.postgresql.org/docs/18/sql-select.html)
3. [PostgreSQL 18 Tutorial, Joins Between Tables](https://www.postgresql.org/docs/18/tutorial-join.html)
4. [PostgreSQL 18 Documentation, LATERAL Subqueries](https://www.postgresql.org/docs/18/queries-table-expressions.html#QUERIES-LATERAL)
5. [SQLite Documentation, SELECT](https://www.sqlite.org/lang_select.html)
6. [MySQL 8.4 Reference Manual, JOIN Clause](https://dev.mysql.com/doc/refman/8.4/en/join.html)
7. [MySQL 8.4 Reference Manual, Outer Join Optimization](https://dev.mysql.com/doc/refman/8.4/en/outer-join-optimization.html)
8. [MySQL 8.4 Reference Manual, Nested Join Optimization](https://dev.mysql.com/doc/refman/8.4/en/nested-join-optimization.html)

## Exercises

### Exercise 1

Given per-key frequencies on two bags, compute inner, left, and full join cardinalities including null and unmatched keys. State every assumption.

### Exercise 2

Compare a right-side predicate in `ON` versus `WHERE` for a left join and construct a fixture that proves the semantic difference.

### Exercise 3

Design safe semi and anti queries over nullable composite tenant keys. Explain why inner-plus-distinct and `NOT IN` are weaker expressions.

### Exercise 4

Design an as-of join from events to versioned dimensions, including boundary rules, nonoverlap enforcement, late corrections, and deterministic conflict handling.

### Exercise 5

Prepare a correctness and performance evidence plan for a five-table query suspected of fanout and cardinality-estimation error.

## Answers to the Exercises

### Answer 1

Group nonnull true-comparing keys. For each value `v`, inner contribution is `n_L(v)n_R(v)`. Left adds `n_L(v)` for each left-only key occurrence group and every null left occurrence; full additionally adds `n_R(v)` for each right-only group and every null right occurrence. If key 1 has left 2/right 3, key 2 left 1/right 0, key 3 left 0/right 4, plus one null on each side: inner 6, left 6+1+1=8, full 8+4+1=13. Assumptions: ordinary equality, null never true-matches, bags, one join key, no extra predicate, and counts include occurrences.

### Answer 2

Use left rows A and B; right rows A/inactive and A/active, with no B. `LEFT JOIN R ON key AND R.active` returns A/active and B/null; inactive does not count as a match. `LEFT JOIN R ON key WHERE R.active` forms A/inactive, A/active, B/null then filters to A/active only because false and unknown fail `WHERE`. Thus `ON` answers “all left rows with active matches if any,” while `WHERE` answers “joined rows whose right side is active.” Include a left row having only an inactive match as another adversary.

### Answer 3

Correlate every nonnull identity component: `EXISTS (SELECT 1 FROM R WHERE R.tenant_id=L.tenant_id AND R.id=L.r_id)` and the corresponding `NOT EXISTS`. Define behavior when any component is null; ordinary equality produces no match, or reject null identity via constraints. Inner-plus-distinct builds match occurrences then removes projected duplicates and can collapse duplicate left occurrences/entities; `EXISTS` states the question directly. `NOT IN` can become unknown when its candidate set contains null and is awkward for composite/null semantics. Cross-tenant collision fixtures and uniqueness/foreign-key constraints support the claim.

### Answer 4

Use business key plus half-open validity `[valid_from,valid_to)`, normalized time zone/precision, and join `key AND valid_from<=event_time AND event_time<valid_to`. Enforce or audit nonoverlap per key transactionally; define open-ended end values without ambiguous sentinels. Preserve source event time and dimension version ID. Late corrections create a new governed history version or rebuild affected assignments; do not silently mutate reproducibility. If overlaps temporarily exist, quarantine or apply a totally ordered policy such as latest correction version, record the conflict, and reconcile—never arbitrary `LIMIT 1`.

### Answer 5

State final and intermediate grain, full composite/tenant keys, constraints, null rules, and expected relationship at every edge. Compute per-key frequency histograms, duplicates, nulls, orphans, predicted pair counts, and matched/unmatched categories independently. Add joins incrementally in a diagnostic query while preserving semantic boundaries; assert output keys and reconcile measures before/after. Capture exact parameters, schema/statistics/settings, machine-readable plan, estimated/actual rows and loops at each node, filters, buffers/I/O, memory/spill, waits, output bytes, and latency under representative skew/concurrency. Correct keys/data/constraints first, then test statistics, indexes, pre-aggregation, or query restructuring and measure write costs/regressions.
