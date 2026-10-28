---
module_id: DBE-014
program: Database Engineering
level: 1
module_number: 14
title: Subqueries and Common Table Expressions
status: complete
last_verified: 2026-08-30
---

# Subqueries and Common Table Expressions

## One-Page Review

### Governing question

How can a query safely compose other queries as scalar values, predicates, derived relations, or named statement-scoped relations while preserving cardinality, null, correlation, evaluation, and optimization semantics?

### Essential definitions

A **subquery** is a query nested in an expression or table expression. A **scalar subquery** must yield at most one row and one column: zero rows produce null in standard/PostgreSQL semantics, one produces its value, and more than one is an error. A **correlated subquery** references columns from an outer query level. `EXISTS` asks whether any row exists; `IN`, `ANY`/`SOME`, and `ALL` compare against subquery rows under three-valued logic. A **derived table** is a subquery in `FROM`. A **common table expression (CTE)** names an auxiliary result within one statement. **Folding/merging** integrates a subquery/CTE into its parent plan; **materialization** computes/stores an intermediate result.

### Central model, mechanism, or theorem

Treat each nested query as a typed interface:

- scalar: cardinality `0..1`, arity `1`;
- row comparison: compatible arity and per-field null logic;
- existence: boolean based only on whether a row is produced;
- membership/quantified comparison: boolean or `UNKNOWN` over a one-column/compatible-row bag;
- table/CTE: named columns, types, multiplicity, grain, and scope.

Equivalent SQL forms need not have the same plan, and similar-looking forms need not be equivalent. CTE syntax is primarily a naming/composition construct; materialization, reuse, predicate pushdown, volatile evaluation, and temporary indexing are engine/version/configuration decisions unless explicitly controlled and documented.

### Critical invariants

- Scalar subqueries prove `0..1` rows with a key/aggregate, not arbitrary `LIMIT 1`.
- Correlation references are qualified and scoped to the intended outer level.
- `EXISTS`/`NOT EXISTS` express existence/absence without right-side fanout.
- Nullable membership values make `IN`, `NOT IN`, `ANY`, and `ALL truth tables explicit.
- Derived-table/CTE columns have deliberate names, types, grain, and multiplicity.
- A CTE is not assumed to be a performance fence or cached result across statements.
- Materialization/folding choices preserve semantics for side-effect-free logic and are verified from plans.
- Security, tenant scope, snapshot, result bounds, timeout, and cancellation apply inside every query block.

### Common failures

Failures include using a scalar subquery with unproven multiplicity, adding `LIMIT 1` without deterministic business policy, confusing zero rows with zero, using `NOT IN` against nullable output, assuming `EXISTS` evaluates its entire projection, relying on function side effects inside subqueries, missing or shadowing a correlation predicate, converting `EXISTS` to an inner join that duplicates outer rows, assuming a CTE is always materialized or always inlined, forcing materialization without pricing memory/temp I/O, duplicating expensive work through folding, relying on inner `ORDER BY` for outer output, and splitting one semantic query into multiple statements with inconsistent snapshots.

### Compact example

Customers 1, 2, and 3 have two, one, and zero orders. A correlated count returns `(2,1,0)`; `EXISTS` returns customers 1 and 2, while `NOT EXISTS` returns 3. A scalar amount subquery returns 10 for customer 2, null for customer 3, and a cardinality error for customer 1. Against blacklist values `(2,NULL)`, `1 IN` and `3 IN` are unknown, `2 IN` is true; `NOT IN` negates those truth values, so only the match is false and the unknowns remain unknown. A CTE safely names totals `(1,50),(2,10)` but its physical evaluation is not inferred from the syntax.

### Connections

[DBE-011](011-selection-projection-and-ordering.md) supplies null and ordering semantics, [DBE-012](012-joins-and-join-semantics.md) supplies semi/anti equivalences, and [DBE-013](013-aggregation-and-grouping.md) supplies scalar aggregate cardinality. [DBE-017](../ROADMAP.md) owns recursive queries. Compiler and Algorithm Engineering connect scope, rewriting, and cost.

## Governing Question

Nested queries let SQL express “the total for this customer,” “there exists a matching row,” “this value is among a derived set,” or “name this intermediate relation and use it below.” Each context imposes a shape contract. A subquery returning a table cannot be inserted where one scalar is required; a set of nullable values changes membership logic; a correlated reference changes evaluation dependencies.

The engineering task is to make those contracts visible and independently testable, then let the optimizer choose legal transformations. Readability refactors between subqueries, joins, and CTEs must preserve bag multiplicity, null truth, outer-row preservation, volatile behavior, and snapshot. Performance claims require plans and representative execution, not folklore about one syntax.

## Why This Matters

Scalar cardinality bugs often survive test fixtures containing one row and fail in production when duplicates arrive. `LIMIT 1` suppresses the error but chooses an arbitrary fact unless a total order and domain policy exist. Zero-row scalar results become null, which can propagate unknown through predicates or arithmetic.

Membership and absence are security- and correctness-sensitive. `NOT IN` can return unknown for every unmatched candidate when the subquery includes one null, silently selecting no rows. A missing tenant component in a correlated predicate can match another tenant. An inner-join rewrite of existence can multiply entities and inflate later aggregates.

CTEs improve decomposition and reuse, but version-dependent optimization matters. A materialized intermediate may prevent predicate pushdown and scan excessive data; folding a multiply referenced expensive expression may repeat work. Treating syntax as a fixed physical boundary causes both regressions and false explanations.

## Prerequisites and Retrieval

Retrieve query blocks, expressions, bags, null, three-valued logic, joins, keys, constraints, aggregation, aliases, lexical scope, volatility, snapshots, query plans, memory, temporary storage, and transactions.

Distinguish scalar null from no outer row; subquery arity from cardinality; correlated from uncorrelated; semantic dependency from repeated physical execution; `EXISTS` from membership; `NOT EXISTS` from nullable `NOT IN`; derived table from persistent/temporary table; statement-scoped CTE from materialized view; and logical naming from physical materialization.

## Learning Objectives

After this module, you should be able to:

1. classify scalar, row, predicate, and table subquery contexts;
2. prove scalar cardinality and handle zero/multiple rows;
3. evaluate `EXISTS`, `IN`, `NOT IN`, `ANY`, and `ALL` with null/empty inputs;
4. write qualified and tenant-safe correlated subqueries;
5. compare semi/anti subqueries with join alternatives under bag semantics;
6. design derived-table and CTE interfaces with explicit grain;
7. explain folding, materialization, reuse, and predicate pushdown without folklore;
8. bound volatile functions and data-modifying CTE behavior;
9. test snapshot, ordering, authorization, and resource behavior; and
10. diagnose nested-query plans using estimates, loops, memory, and spills.

## Core Exposition

A query block has its own input namespace, grouping, projection, and result shape. Parentheses can place a query where the grammar expects a value expression, boolean subquery expression, row source, or auxiliary CTE definition. The surrounding context determines required columns and rows; aliases define what names escape the block.

A scalar subquery produces one column and at most one row. Zero rows become null; one row returns that value, even when the value itself is null; multiple rows raise a cardinality violation rather than choosing. This makes duplicates observable. Prove uniqueness with a primary/unique key and full predicate, or use an aggregate whose global group yields one row. Do not erase a violated invariant with unqualified `LIMIT 1`.

When business meaning truly says “latest,” use an explicit total order such as effective timestamp plus unique version ID and document ties, nulls, snapshot, and mutation. A lateral top-one derived table may express this more clearly than a scalar subquery. Still test history nonoverlap; deterministic conflict resolution is not the same as valid source data.

Scalar aggregates deserve care. `SELECT SUM(x) ...` without `GROUP BY` normally returns one row even when no inputs, with null sum; `COUNT(*)` returns zero. A grouped aggregate can return zero rows for a missing group. Wrapping it as a scalar changes whether the outer expression sees null through aggregate output or through absent row, sometimes observationally equal but diagnostically different.

`EXISTS(subquery)` is true when the subquery produces at least one row and false otherwise; projection contents are usually irrelevant. Write `SELECT 1` to signal intent. The engine may stop after proving existence and can decorrelate into a semi join. Never put required side effects in the projection or predicate: evaluation count/completion is not a side-effect API.

`NOT EXISTS` expresses absence: for an outer row, no inner row makes the correlation condition true. It is robust to unrelated null values because the predicate itself defines matching. It maps naturally to anti join. Include every identity, tenant, time, and authorization component in the correlation.

`x IN (subquery)` compares `x` with a one-column result. It is true if any comparison is true; false if no row exists or all comparisons are false; unknown if no comparison is true and at least one is unknown. If `x` is null, comparisons are normally unknown unless a true result arises through nonstandard semantics. `WHERE` retains only true.

`x NOT IN (subquery)` is equivalent to `x <> ALL(subquery)` under SQL rules. It is false on an equal match, true only when every comparison is true—including vacuously for empty input—and unknown when no comparison is false and at least one is unknown. A single null in the right result can turn an otherwise unmatched candidate into unknown. Prefer correlated `NOT EXISTS` for absence, or prove/filter nonnull output and document equivalence.

`op ANY`/`SOME` is true if any comparison is true, false for empty input, and otherwise may be unknown. `op ALL` is true for empty input, false if any comparison is false, and otherwise may be unknown. These existential/universal empty-set identities can surprise applications. Test empty, all-null, match, nonmatch, and mixed truth values.

Row constructors permit multi-column membership/comparison when arity and types align. Per-field comparisons combine under three-valued rules. Composite tenant keys must include all components. A row `IN` list with nullable fields can yield unknown even when no all-fields-equal row exists. Constraints against null identity simplify reasoning.

A correlated subquery references an outer alias. During logical evaluation, outer values act as parameters for the inner block. Correlation can occur in `WHERE`, projection, `HAVING`, or lateral table expressions depending on dialect. Qualify names: an accidental unqualified inner column can shadow the intended outer reference and turn a correlation into a tautology.

Correlation does not guarantee row-by-row physical execution. Optimizers may decorrelate to semi/anti joins, aggregates, or other plans. Conversely, unsupported patterns may execute an inner plan many times. Inspect loops and actual rows. Rewrite only after verifying equality of null behavior, multiplicity, volatility, and outer preservation.

A derived table is a subquery in `FROM` and returns a relation with an alias. It can pre-aggregate to a safe grain, isolate window results, or expose computed columns. The outer query sees only projected columns. An inner `ORDER BY` does not generally promise outer output order unless tied to a meaningful inner limit/operation; add outer `ORDER BY` for delivery.

A CTE gives a name and optional column list to an auxiliary statement in one containing statement. It can make stages readable, centralize a shared definition, and allow sibling dependencies according to dialect scope. It is not a schema object, session temporary table, cached query, or materialized view, and disappears after the statement.

Name CTEs by domain result—`eligible_orders`, `customer_totals`, `authorized_accounts`—not delivery sequence. Define input/output grain in comments or adjacent design docs when nonobvious. Project only needed columns, qualify sources, and ensure each CTE preserves tenant and authorization scope. A readable chain can still hide fanout, null changes, or repeated scans.

Optimization varies. PostgreSQL 18 can fold a nonrecursive side-effect-free CTE into the parent, commonly when referenced once, enabling predicate pushdown; multiply referenced CTEs commonly materialize unless directed. `MATERIALIZED` and `NOT MATERIALIZED` influence this under documented preconditions. MySQL can merge or materialize derived tables/CTEs and may add indexes to materialized intermediates. SQLite documents its own materialization hints. Never generalize one engine/version.

Folding enables joint optimization: an outer selective predicate can reach the base table and use an index. It can also duplicate an expensive expression when a CTE is referenced multiple times. Materialization computes an intermediate once and can stabilize evaluation of expensive/volatile work under engine semantics, but consumes memory/temp storage, may lose base indexes, and can block pushdown. Choose from evidence.

Materialization hints are not portable universal commands. Even when supported, their exact meaning and exceptions are documented by the engine. A plan node or trace, version, settings, reference count, volatility, and actual execution evidence support the claim. Recheck after upgrades.

Volatile or side-effecting functions make evaluation count observable. SQL optimizers assume purity categories according to engine declarations. Mislabeling a function as immutable/stable can yield wrong caching or rewrite. Sequence advancement, external calls, random values, clocks, and logging should not be embedded where correctness depends on exact subquery evaluation count.

Data-modifying CTEs are powerful and dialect-specific. PostgreSQL allows auxiliary `INSERT`, `UPDATE`, `DELETE`, or `MERGE` under a top-level statement, exposes `RETURNING` results, and defines shared snapshot/concurrency behavior that must be read precisely. They are not a substitute for clear transaction/outbox design, and execution ordering between siblings cannot be inferred from textual order. This module emphasizes read composition; use modifying CTEs only with dedicated engine tests.

Recursive CTEs add an anchor, recursive term, working table, termination, cycle, and traversal concerns. They are owned by [DBE-017](../ROADMAP.md). Here, merely recognize that `WITH RECURSIVE` changes the dependency/evaluation model and cannot be reasoned about as a simple named nonrecursive subquery.

CTE chains do not automatically create multiple snapshots within one statement; engine transaction/isolation rules govern visibility. Splitting a query into several client statements with temporary application state can observe different committed states under statement-level snapshots. If one consistent semantic result is required, retain one query/transaction or state the accepted drift.

Security applies at each block. Parameterize values; allowlist dynamic syntax; use qualified tenant keys; project only authorized columns; understand view/CTE/policy execution context; prevent error/cardinality messages from exposing sensitive facts; and bound correlated work to avoid denial of service. A subquery that only checks existence can still leak whether protected data exists if authorization is misplaced.

Physical evidence should capture query blocks, correlation parameters, estimated/actual rows, loops, subplans, semi/anti transformations, pushed predicates, materialized row/byte counts, temp I/O, memory, indexes, repeated expressions, first/last-row latency, and output equality. Test rare/common outer keys, no/one/many inner matches, nulls, skew, empty outer input, concurrency, timeout, and cancellation.

## Definitions and Notation

Let subquery `Q(o)` depend on outer occurrence `o` and yield bag `B_o` of rows.

- Scalar contract: arity one and `|B_o|<=1`; result is null for zero, the sole value for one, error for more.
- `EXISTS Q(o)` is `|B_o|>0`; `NOT EXISTS` is its boolean negation.
- `x IN B` is disjunction of equality comparisons with SQL three-valued logic.
- `x op ANY B` is existential comparison; `x op ALL B` is universal comparison.
- A derived table/CTE interface is `(column names, types, nullability, bag grain, scope)`.
- Materialization cost includes producing/storing/reading `B`; folding cost includes parent integration and possible repeated computation.

These are semantic/cost abstractions. The optimizer need not literally enumerate `B_o` per outer row, and CTE syntax alone does not decide either cost path.

## Mechanisms, Invariants, or Proof Structure

A nested-query review should:

1. classify context and declare expected arity/cardinality/grain;
2. prove scalar `0..1` with keys, constraints, or aggregate semantics;
3. enumerate empty, null, one, duplicate, and many-row truth/results;
4. qualify correlations and include tenant, time, and authorization scope;
5. compare `EXISTS`/`NOT EXISTS`, membership, and join alternatives under bags;
6. define CTE columns, types, grain, dependencies, reuse, and volatility;
7. inspect whether predicates fold/push down or intermediates materialize/spill;
8. reject reliance on evaluation order/count or inner presentation order;
9. test one-statement snapshot, deadlines, cancellation, and sensitive errors; and
10. retain plan/version/settings/raw result evidence for every performance rewrite.

The finite model below evaluates correlated counts, existence/absence, nullable membership, scalar cardinality, and one named totals relation. It uses a string marker for SQL `UNKNOWN` and a string for cardinality error; it is not a SQL engine or optimizer.

<!-- bijux-verify: {"id":"finite-subquery-cte-semantics","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"correlated_counts=((1, 2), (2, 1), (3, 0))\nexists_customers=(1, 2)\nnot_exists_customers=(3,)\nblacklist_in=((1, 'unknown'), (2, True), (3, 'unknown'))\nblacklist_not_in=((1, 'unknown'), (2, False), (3, 'unknown'))\nscalar_customer_2=10\nscalar_customer_3=None\nscalar_customer_1=cardinality_error\ncte_totals=((1, 50), (2, 10))\n","stderr":""}} -->
```python
UNKNOWN = "unknown"
customers = (1, 2, 3)
orders = (
    {"customer_id": 1, "amount": 20},
    {"customer_id": 1, "amount": 30},
    {"customer_id": 2, "amount": 10},
)
blacklist = (2, None)


def sql_equal(left, right):
    return UNKNOWN if left is None or right is None else left == right


def sql_in(value, candidates):
    comparisons = tuple(sql_equal(value, candidate) for candidate in candidates)
    if True in comparisons:
        return True
    if UNKNOWN in comparisons:
        return UNKNOWN
    return False


def sql_not(value):
    return UNKNOWN if value == UNKNOWN else not value


def amounts(customer_id):
    return tuple(row["amount"] for row in orders if row["customer_id"] == customer_id)


def scalar(values):
    if len(values) == 0:
        return None
    if len(values) == 1:
        return values[0]
    return "cardinality_error"


counts = tuple((customer, len(amounts(customer))) for customer in customers)
exists = tuple(customer for customer in customers if amounts(customer))
not_exists = tuple(customer for customer in customers if not amounts(customer))
in_results = tuple((customer, sql_in(customer, blacklist)) for customer in customers)
not_in_results = tuple((customer, sql_not(sql_in(customer, blacklist))) for customer in customers)
totals = tuple((customer, sum(amounts(customer))) for customer in customers if amounts(customer))

print(f"correlated_counts={counts}")
print(f"exists_customers={exists}")
print(f"not_exists_customers={not_exists}")
print(f"blacklist_in={in_results}")
print(f"blacklist_not_in={not_in_results}")
print(f"scalar_customer_2={scalar(amounts(2))}")
print(f"scalar_customer_3={scalar(amounts(3))}")
print(f"scalar_customer_1={scalar(amounts(1))}")
print(f"cte_totals={totals}")
```

Tuple order follows fixture construction and is not a SQL output-order guarantee. The totals tuple models a named relation only; it says nothing about CTE folding, materialization, reuse, or temp indexes. The model omits bags with duplicate identical customer rows, row comparisons, `ANY`/`ALL`, types/collations, snapshots, authorization, recursion, modification, and execution costs.

## Alternatives and Trade-Offs

Scalar subqueries are compact for proven one-value relationships; joins/lateral forms expose multiplicity and related columns more clearly. `EXISTS`/`NOT EXISTS` state semi/anti intent without fanout; `IN` can be concise for nonnull membership; joins may be easier when right attributes are required. Derived tables localize one use; CTEs name/reuse results and dependency chains.

Folding permits pushdown and base indexes but can duplicate work. Materialization supports one computation/reuse and can control volatile/expensive evaluation under documented rules, but costs memory/temp I/O and may block optimizations. Temporary tables cross statement boundaries and can be indexed/analyzed explicitly, but introduce lifecycle, transaction, privilege, cleanup, and snapshot considerations.

## Failure Modes and Misconceptions

“Scalar means the query happens to return one row” is not a durable proof. “`LIMIT 1` fixes it” hides invalid multiplicity without a policy. “No scalar row means zero” is false; it normally means null. “`NOT IN` is anti join” fails with nullable values.

“Correlated means executed once per outer row” is a logical model, not guaranteed plan. “CTEs are always materialized” and “CTEs are always inlined” are both version/dialect folklore. “Materialized means persisted/cached across statements” confuses an execution intermediate with a schema object.

“Textual CTE order controls side effects” is unsafe. “Inner `ORDER BY` orders the final result” is false without an applicable outer order. “Refactoring to a join is equivalent” can introduce duplicates, change nulls, or remove outer rows. Prove results on adversarial bags.

## Worked Examples

### Example 1

A scalar lookup by declared unique `(tenant_id,external_id)` yields zero/null or one value. A duplicate violates a constraint and the query fails visibly rather than selecting an arbitrary record.

### Example 2

A latest-version lookup uses `ORDER BY valid_from DESC,version_id DESC LIMIT 1` only as a documented conflict policy. A separate audit rejects overlapping histories so the ordering is not treated as data validity.

### Example 3

`EXISTS` selects customers with orders once per customer occurrence even when one has 1,000 orders. An inner join would fan out before any duplicate elimination.

### Example 4

`NOT EXISTS` finds customers without orders despite a null `orders.customer_id`. `NOT IN` against that nullable column produces unknown for unmatched nonnull customers.

### Example 5

`amount > ALL(empty_subquery)` is true by universal empty-set semantics; `amount > ANY(empty_subquery)` is false. Tests name this behavior instead of assuming both false.

### Example 6

An unqualified `tenant_id=tenant_id` inside a subquery binds both names locally and becomes tautological. Aliases `o.tenant_id=c.tenant_id` make correlation and security review explicit.

### Example 7

A derived table aggregates lines to one row per order before joining orders. Its output key is asserted, preventing line fanout from multiplying order-level measures.

### Example 8

A single-reference side-effect-free CTE folds so an outer key predicate reaches an index. The plan, not the word `WITH`, proves this for the recorded engine version.

### Example 9

A multiply referenced expensive pure expression is materialized once in a measured plan. Forcing `NOT MATERIALIZED` duplicates computation but may still win when each reference selects a tiny different subset; both are benchmarked.

### Example 10

A production upgrade changes CTE plan shape. Regression evidence compares exact results plus estimates, loops, pushed filters, intermediate rows/bytes, temp I/O, memory, and latency across representative parameters before accepting it.

## Cross-Program Connections

- [Compilers and Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md) supplies scope, name resolution, intermediate representations, rewriting, and optimization.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies equivalence, complexity, memoization/materialization trade-offs, and evidence design.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) uses CTEs and subqueries for staged transformations, deduplication, and reconciliation.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) governs correlation scope, tenant isolation, authorization, side channels, and bounded execution.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) connects typed parameters, deadlines, cancellation, error contracts, and result bounds.

## References

1. [PostgreSQL 18 Documentation, Subquery Expressions](https://www.postgresql.org/docs/18/functions-subquery.html)
2. [PostgreSQL 18 Documentation, Scalar Subqueries](https://www.postgresql.org/docs/18/sql-expressions.html#SQL-SYNTAX-SCALAR-SUBQUERIES)
3. [PostgreSQL 18 Documentation, WITH Queries](https://www.postgresql.org/docs/18/queries-with.html)
4. [PostgreSQL 18 Documentation, Common Table Expression Materialization](https://www.postgresql.org/docs/18/queries-with.html#QUERIES-WITH-CTE-MATERIALIZATION)
5. [SQLite Documentation, The WITH Clause](https://www.sqlite.org/lang_with.html)
6. [MySQL 8.4 Reference Manual, WITH](https://dev.mysql.com/doc/refman/8.4/en/with.html)
7. [MySQL 8.4 Reference Manual, Subqueries](https://dev.mysql.com/doc/refman/8.4/en/subqueries.html)
8. [MySQL 8.4 Reference Manual, Derived Table and CTE Merging or Materialization](https://dev.mysql.com/doc/refman/8.4/en/derived-table-optimization.html)

## Exercises

### Exercise 1

Derive scalar subquery results for zero, one-null, one-value, and multiple rows. Give durable proofs for the `0..1` cases and reject arbitrary repairs.

### Exercise 2

Construct complete truth tables for `IN`, `NOT IN`, `= ANY`, and `<> ALL` over empty, null-only, matching, nonmatching, and mixed subquery results.

### Exercise 3

Rewrite a correlated existence and absence query as joins where possible, proving multiplicity and null equivalence or explaining why the rewrite is unsafe.

### Exercise 4

Compare a derived table, folded CTE, materialized CTE, and temporary table for an expensive intermediate referenced twice with different selective filters.

### Exercise 5

Design a correctness/performance evidence plan for refactoring a ten-CTE reporting query across a database major-version upgrade.

## Answers to the Exercises

### Answer 1

Zero rows yield null; one row containing null also yields null but has different provenance; one row containing `v` yields `v`; two or more rows raise cardinality violation. A full unique-key predicate/constraint proves at most one; an aggregate without grouping proves one output row under documented semantics; a left lateral join can expose zero/one as rows. `LIMIT 1` is valid only when the domain requests one winner and a total ordering plus snapshot/tie policy defines it. Otherwise it hides duplicate corruption and must be rejected.

### Answer 2

For empty right input, `IN`/`=ANY` are false and `NOT IN`/`<>ALL` are true. For null-only with nonnull left, all four comparisons reduce to unknown. With an equal value, `IN`/`=ANY` are true and their negations false even if null is also present. With only unequal nonnull values, `IN`/`=ANY` are false and `NOT IN`/`<>ALL` true. With unequal plus null, existential equality has no true but an unknown, so `IN`/`=ANY` are unknown; universal inequality has no false but an unknown, so `NOT IN`/`<>ALL` are unknown. A null left normally yields unknown for nonempty comparisons. Verify dialect row-comparison extensions separately.

### Answer 3

`WHERE EXISTS (SELECT 1 FROM R WHERE match(L,R))` maps to a semi join, not ordinary inner output: an inner join emits one L occurrence per matching R. It is equivalent only if the plan/query restores exactly the left bag multiplicity, for example because R is unique on the match key; `DISTINCT` can collapse duplicate L occurrences and is not a general proof. `NOT EXISTS` maps to anti join. A left join followed by `WHERE R.guaranteed_nonnull_key IS NULL` can match it if ON contains the exact correlation and the marker cannot be null in real matches. Nullable `NOT IN` is unsafe without a nonnull proof/filter and matching three-valued semantics.

### Answer 4

A derived table names one occurrence and lets the optimizer merge/materialize per dialect. A folded CTE can push each outer selective predicate into base access but may compute the expensive expression twice. A materialized CTE computes/stores once and supports two reads, but processes the full intermediate, uses memory/temp I/O, and may lose base indexes/pushdown. A temporary table explicitly persists across statements, can be indexed/analyzed and reused, but needs transaction/snapshot consistency, privileges, cleanup, concurrency isolation, and extra writes. Measure expression calls, base/intermediate rows and bytes, indexes, memory/temp I/O, plan, latency, snapshot correctness, and cleanup under representative selectivities.

### Answer 5

Pin old/new engine builds, schema/catalog digest, statistics, settings, roles, data snapshot/distributions, query text, parameters, and concurrency. Define each CTE's columns, grain, keys, nulls, multiplicity, authorization, and expected reconciliation. Compare final and intermediate results with adversarial zero/one/many/null/duplicate/tenant fixtures. Capture machine-readable plans: folding/materialization, pushed filters, loops, estimated/actual rows, expression evaluation, intermediate bytes, generated indexes, memory, temp I/O/spill, buffers, waits, and first/last-row/end-to-end distributions. Test cancellation and resource limits. Accept changes only when semantics match and workload-wide objectives improve; retain rollback and version-specific limitations.
