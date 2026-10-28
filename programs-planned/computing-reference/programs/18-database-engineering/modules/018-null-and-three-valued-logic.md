---
module_id: DBE-018
program: Database Engineering
level: 1
module_number: 18
title: Null and Three-Valued Logic
status: complete
last_verified: 2026-08-30
---

# Null and Three-Valued Logic

## One-Page Review

### Governing question

How should unknown or absent database values flow through comparisons, Boolean expressions, query contexts, joins, constraints, grouping, and interfaces without silently turning uncertainty into falsehood or equality?

### Essential definitions

`NULL` is a database marker for the absence of a value, not a value equal to itself, zero, an empty string, or a universal “unknown object.” Ordinary comparisons involving null commonly yield **UNKNOWN**. SQL predicate logic therefore has truth values `TRUE`, `FALSE`, and `UNKNOWN`. `WHERE`, `HAVING`, and join `ON` retain or match rows only when their predicate is true. `IS NULL` tests the marker. A **null-safe equality** returns a two-valued result even for null operands. A predicate is **null-rejecting** for an input when it cannot be true if that input is null.

### Central model, mechanism, or theorem

Under strong three-valued logic, `NOT U=U`; `F AND U=F`; `T AND U=U`; `T OR U=T`; and `F OR U=U`. A query context then maps truth to action. A filter keeps only T, so both F and U disappear. A PostgreSQL `CHECK` constraint accepts T or U and rejects F, which is why `CHECK (price>0)` does not replace `NOT NULL`. Duplicate elimination and grouping use their own “not distinct” treatment rather than ordinary `=`. Correctness requires deriving the truth value first, then applying the exact context rule.

### Critical invariants

- Every nullable field has a domain meaning, owner, source, and transition policy.
- Ordinary equality/inequality with null is never used as a null test.
- Complete T/F/U truth tables are derived before Boolean rewrites.
- Filter, join, CASE, CHECK, uniqueness, grouping, DISTINCT, and aggregate contexts are reviewed separately.
- `IN`/`NOT IN` account for null on both the left and candidate sides.
- Outer-join absence is detected with a guaranteed-nonnull matched-side key.
- Null-safe comparison is chosen explicitly and scoped to the target dialect.
- Plans, indexes, null fractions, parameter values, and schema/API mappings are verified independently of semantics.

### Common failures

Failures include writing `x = NULL`, assuming `NOT p` retrieves every row excluded by `p`, using `NOT IN` with a nullable subquery, placing a right-side predicate in `WHERE` and collapsing a left join, using `COALESCE` to invent a business default, assuming `CHECK (x>0)` rejects null, expecting UNIQUE to treat nulls identically across engines, counting nullable expressions instead of rows, equating outer-join null extension with stored null, conflating JSON missing with JSON null, and applying classical excluded-middle rewrites to nullable predicates.

### Compact example

For scores 10, null, 5, and -1, `score>7` yields T, U, F, F; `WHERE score>7` keeps only 10. `WHERE NOT(score>7)` keeps 5 and -1 but not null. Adding `OR score IS NULL` keeps 10 and null. Against candidate list `(5,NULL)`, `10 IN (...)` is U because no true comparison exists and one is unknown; its `NOT IN` is also U. `CHECK(score>0)` accepts 10, null, and 5, rejecting only -1.

### Connections

[DBE-011](011-selection-projection-and-ordering.md) places predicates in query processing. [DBE-012](012-joins-and-join-semantics.md) derives null extension and anti-joins. [DBE-013](013-aggregation-and-grouping.md) separates null arguments, empty inputs, and grouping equality. [DBE-014](014-subqueries-and-common-table-expressions.md) covers nullable membership. [DBE-016](016-set-operations.md) covers duplicate equality.

## Governing Question

Null is not merely a storage option. It changes the logic used to determine which rows survive, match, satisfy constraints, group together, compare as changed, or cross an API boundary. A predicate can be neither true nor false because the available data does not determine the answer. If engineers mentally replace UNKNOWN with FALSE too early, negation, joins, constraints, and anti-membership become wrong.

The governing discipline is contextual: derive a predicate's T/F/U result, then ask how the current SQL construct treats it. `WHERE` rejects unknown, while a check constraint may accept it. Ordinary equality with two nulls is unknown, while `DISTINCT` can collapse null-bearing duplicate rows. These are not contradictions; they are different operations with different contracts.

## Why This Matters

Nullable data occurs in staged migrations, optional relationships, incomplete measurements, redacted attributes, future values, failed parsing, outer joins, sparse dimensions, and partial updates. One marker cannot explain which cause applies, so the schema and surrounding status/provenance fields must carry meaning. Treating null as empty or zero can corrupt billing, scientific data, eligibility, and access decisions.

Three-valued logic produces plausible omissions. `WHERE status <> 'closed'` excludes rows whose status is null. `NOT IN` can return no rows because one candidate is null. A right-table filter in `WHERE` removes null-extended left rows and changes an outer join. A nullable check passes unknown values. These statements can execute successfully, use indexes, and still violate the domain requirement.

Null also affects physical behavior. Null fractions influence selectivity estimates; indexes and uniqueness treat null according to engine and definition; null-safe operators may have different access paths; parameterized predicates can change plans. Semantic proof must be followed by actual plan and production-shaped data evidence, not replaced by it.

## Prerequisites and Retrieval

Retrieve propositional logic, truth tables, equivalence, partial information, relations and bags, selection, joins, subqueries, grouping, aggregates, constraints, types, keys, indexes, statistics, query plans, JSON/interface schemas, and migrations.

Distinguish null marker from its domain reason; UNKNOWN truth from stored null; false from unknown; missing row from a row containing null; no join match from matched nullable payload; ordinary equality from null-safe “not distinct” equality; empty set from null aggregate result; and storage null from absent or explicit-null API fields.

## Learning Objectives

After this module, you should be able to:

1. derive complete `NOT`, `AND`, and `OR` truth tables over T/F/U;
2. calculate comparison, `IN`, and `NOT IN` outcomes with nullable operands;
3. distinguish filter, join, CASE, CHECK, uniqueness, grouping, DISTINCT, and aggregate contexts;
4. use null tests and null-safe equality deliberately;
5. prove outer-join and anti-join behavior under null extension;
6. identify which classical Boolean rewrites remain valid and which assumptions fail;
7. design nullable schemas with explicit domain reasons and constraints;
8. preserve missing/null/value distinctions through APIs and migrations;
9. build adversarial tests for nullable data; and
10. verify null selectivity, indexes, plans, parameters, and upgrade behavior.

## Core Exposition

SQL null marks the absence of a value in a column position. It does not record why the value is absent. “Not measured,” “not applicable,” “withheld,” “not yet known,” and “failed to parse” can require different business behavior. If those distinctions matter, add a constrained status/reason and provenance rather than attempting to recover meaning from null later.

Ordinary comparisons such as `=`, `<>`, `<`, and `>` generally yield UNKNOWN when either operand is null. Therefore `x = NULL` and `x <> NULL` do not test nullness. Use `x IS NULL` or `x IS NOT NULL`. PostgreSQL also documents `IS [NOT] TRUE/FALSE/UNKNOWN` and `IS [NOT] DISTINCT FROM`; MySQL documents the null-safe `<=>` operator. Syntax and row/composite behavior are dialect-specific.

Let T, F, and U denote truth values. Negation maps T to F, F to T, and U to U. Conjunction is false if either operand is false, true only if both are true, otherwise unknown. Disjunction is true if either operand is true, false only if both are false, otherwise unknown. These rules express what is forced by available information: `FALSE AND unknown` is already false; `TRUE OR unknown` is already true.

Evaluation order is not a truth-table guarantee. An optimizer may reorder expressions when legally equivalent, and SQL does not generally promise left-to-right short-circuiting for suppressing errors or side effects. Avoid predicates whose safety depends on another conjunct being evaluated first; use safe expressions, constraints, or documented conditional constructs and test the target engine.

`WHERE` retains only rows for which its predicate is TRUE. Both FALSE and UNKNOWN are discarded. Thus `WHERE x>7` and `WHERE NOT(x>7)` do not partition all rows when x is nullable: the null rows appear in neither result. To express “not greater than seven, including missing,” write and validate the domain rule explicitly, for example `x<=7 OR x IS NULL` if that is truly intended.

`HAVING` similarly keeps groups only on TRUE. A CASE searched condition chooses a `WHEN` branch only when its predicate is true; false and unknown move to later branches or ELSE. A row-level security predicate commonly grants visibility only on true, which is a useful fail-closed property, but every nullable input and bypass path must still be tested.

Join `ON` matches row pairs only when the condition is TRUE. FALSE and UNKNOWN pairs do not match. An inner join discards them. A left join preserves an unmatched left row and creates nulls for every right output column. Those generated nulls mean “no matching right row in this join,” which is distinct from a matched right row whose nullable payload is null.

Detect outer-join absence using a right-side key that is guaranteed nonnull for every real match, such as a primary key: `right.id IS NULL`. Testing `right.optional_value IS NULL` combines unmatched rows with matched rows having null payload. This distinction controls counts, anti-joins, and application status.

Predicate placement around outer joins matters. `LEFT JOIN R ON L.id=R.l_id AND R.active` preserves L rows without an active match. Moving `R.active` to `WHERE` rejects the null-extended row and often yields inner-join behavior. An optimizer may transform a left join when a later predicate is null-rejecting, but only a proven semantic equivalence justifies the plan.

`IN` is conceptually a disjunction of equality comparisons, with database-specific row and type details. If any comparison is true, the result is true. If none is true but at least one is unknown, the result is unknown. Otherwise it is false. A null left operand ordinarily makes every ordinary equality unknown unless the candidate set is empty under the dialect's subquery rules.

`NOT IN` is the negation of that membership result. If the candidate set contains null and no equal value is found, membership is unknown and negation remains unknown. A WHERE filter then removes the row. For nullable candidate data, use `NOT EXISTS` with a deliberately chosen equality and null policy, or eliminate/prohibit candidate nulls when the domain supports that. Do not patch the symptom without deciding whether null should match null.

`EXISTS` asks whether a subquery returns any row; the projected values, including null, do not affect existence. This makes `NOT EXISTS` robust for anti-membership when the correlation predicate correctly encodes identity. It still requires tenant scope, composite keys, temporal policy, and null-safe equality if nulls are intended to match.

Null-safe equality maps two nulls to equal, one null to unequal, and nonnull values through normal equality, returning only T/F. PostgreSQL's `IS NOT DISTINCT FROM` and MySQL's `<=>` are examples. This is useful for change detection, reconciliation, and nullable composite keys, but two missing values are not necessarily the same domain fact. Equality semantics cannot supply missing provenance.

Classical double negation and De Morgan laws hold under the common strong three-valued truth tables, but excluded middle does not: `p OR NOT p` is U when p is U. Nor is `p AND NOT p` always false; it is U for unknown p. The operational “complement” of a WHERE result must include an explicit `p IS NOT TRUE`-style test where supported or an equivalent complete case analysis, not simply `NOT p`.

Rewrites involving comparison complements require null assumptions. For nonnull x, `NOT(x=5)` and `x<>5` agree; for null x both are unknown, so they still agree as truth values but neither retrieves null in WHERE. The common mistake is not that these two expressions differ; it is assuming either selects the set-theoretic complement of `WHERE x=5` over all rows.

`BETWEEN`, pattern matching, arithmetic comparisons, and most strict functions propagate unknown/null when relevant inputs are null, but functions and operators have individual contracts. `COALESCE` selects the first nonnull expression. `NULLIF(a,b)` returns null when its comparison is true. Conditional expressions can convert uncertainty into a value; doing so changes meaning and must be owned by the domain.

`COALESCE(x,0)` is correct only when absent x is authoritatively equivalent to zero at that boundary. It may conflate “not measured” with a measured zero, change averages and comparisons, block ordinary index use, and hide upstream quality defects. Presentation defaults should not silently become stored or analytical facts.

Aggregates have function-specific null rules. `COUNT(*)` counts occurrences; `COUNT(x)` counts nonnull x. Many general aggregates ignore null inputs and return null on an empty or all-null input, while count returns zero. Boolean aggregates, JSON/object aggregates, ordered aggregates, and dialect extensions require their own review. Null is not automatically zero or an identity element.

Grouping and duplicate elimination use equality notions different from ordinary predicate equality. Null grouping keys are ordinarily placed together for grouping. DISTINCT and set operations can treat null-bearing rows as duplicates. Therefore “`NULL=NULL` is unknown” does not predict grouping cardinality. Always identify the operation-specific equivalence relation.

Unique constraints have engine- and definition-specific null behavior. PostgreSQL documents nulls as distinct by default for unique constraints and offers `NULLS NOT DISTINCT`; the SQL standard leaves aspects implementation-defined. A filtered/partial unique index can express uniqueness only for nonnull rows on supporting engines. Portability requires live DDL tests, not assumptions from ordinary equality.

A CHECK expression in PostgreSQL succeeds when TRUE or UNKNOWN and rejects FALSE. Consequently `CHECK (price>0)` permits null price; combine it with `NOT NULL` if absence is prohibited. Write cross-column checks with explicit null-state rules: for example, require both timestamps or neither, or require an end after start when both exist. Test every allowed/disallowed null combination.

Foreign keys also have null rules. Under common simple matching, a referencing row with a null key component can escape the match requirement; composite `MATCH FULL` behavior differs from simple matching and support varies. If a relationship is mandatory, use not-null constraints as well as a foreign key. Partial-null composite references deserve explicit fixtures.

Nullability is part of schema evolution. Adding a nullable column is operationally easy but creates an incomplete-state contract. A robust migration may add the column, write dual-compatible code, backfill with provenance, validate a constraint, then set not null when every writer/read path is ready. A default can distinguish future writes but does not prove historical values.

Interfaces often have more states than a database column. JSON can omit a field or include it as null; patch protocols can distinguish “leave unchanged,” “clear,” and “set.” Language option types may collapse missing and explicit null during deserialization. Define request, storage, response, event, cache, and analytics mappings with round-trip tests. Never infer update intent from a generic nullable value alone.

Indexes may include, omit, cluster, or specially optimize null values depending on engine and index type. Predicates such as `IS NULL`, null-safe equality, and `COALESCE(column, sentinel)` can have different sargability. Sentinels risk collision and distort domain order. Inspect documented index rules and actual plans with representative null fractions.

Statistics commonly track a null fraction separately. Correlated nullability—such as `shipped_at` null exactly when status is pending—can defeat independence estimates. Collect supported extended statistics, maintain constraints, or redesign predicates, then compare estimated and actual rows. Parameter null versus nonnull can also lead to different selectivity and plan choices.

Security decisions should make unknown handling explicit. SQL filter contexts naturally retain only true, but an application that converts nullable Boolean to a language false might obscure “insufficient evidence” from “denied.” Store or emit decision reason when audit requires it. For grants, eligibility, fraud, or compliance, define whether unknown denies, quarantines, escalates, or awaits data.

Testing requires complete partitions, not happy examples. For each nullable operand enumerate nonnull-match, nonnull-nonmatch, and null; for two operands cover all relevant pairs. Add empty and null-containing subqueries, matched/unmatched outer joins, stored-null payloads, duplicate/group nulls, check and unique constraints, composite FKs, API omitted/null/value states, and production null skew. Compare results to hand-derived truth tables and verify the target dialect.

## Definitions and Notation

Let truth domain be `L={T,F,U}`. Under strong three-valued logic:

- `not(T)=F`, `not(F)=T`, `not(U)=U`;
- `a AND b=F` if either is F, T if both are T, otherwise U;
- `a OR b=T` if either is T, F if both are F, otherwise U;
- ordinary `eq(x,y)=U` if x or y is null, otherwise T/F from type equality;
- a WHERE-like acceptance map keeps exactly T;
- a PostgreSQL CHECK-like acceptance map accepts T or U and rejects F;
- `not_distinct(null,null)=T`, one-null pairs are F, and nonnull pairs use equality.

This truth algebra does not by itself define grouping, uniqueness, foreign keys, function strictness, or physical plans.

## Mechanisms, Invariants, or Proof Structure

A null-semantics review should:

1. document each nullable field's domain causes, owner, lifecycle, and external representation;
2. derive primitive comparison truth values for nonnull-match, nonmatch, and null;
3. expand `NOT`, `AND`, `OR`, `IN`, and `NOT IN` over complete T/F/U cases;
4. apply the exact filter, join, CASE, CHECK, grouping, DISTINCT, aggregate, unique, or FK context;
5. distinguish unmatched outer rows from matched nullable payload via a guaranteed-nonnull key;
6. prove every rewrite under nullable and nonnull assumptions, including predicate placement;
7. test constraints and indexes on the target engine/version rather than infer them from `=`;
8. round-trip omitted/null/value states across APIs, events, caches, migrations, and analytics;
9. reconcile counts for true, false, unknown, null, matched, unmatched, and grouped rows; and
10. inspect actual plans, null fractions, parameter cases, indexes, statistics, latency, and upgrades.

The finite model below implements strong three-valued truth tables, ordinary nullable comparison, membership with a null candidate, WHERE acceptance, PostgreSQL-style CHECK acceptance, and null-safe equality. It is a bounded semantic oracle, not a SQL engine.

<!-- bijux-verify: {"id":"finite-three-valued-logic","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"and_table=(('T', 'T', 'T'), ('T', 'F', 'F'), ('T', 'U', 'U'), ('F', 'T', 'F'), ('F', 'F', 'F'), ('F', 'U', 'F'), ('U', 'T', 'U'), ('U', 'F', 'F'), ('U', 'U', 'U'))\nor_table=(('T', 'T', 'T'), ('T', 'F', 'T'), ('T', 'U', 'T'), ('F', 'T', 'T'), ('F', 'F', 'F'), ('F', 'U', 'U'), ('U', 'T', 'T'), ('U', 'F', 'U'), ('U', 'U', 'U'))\nnot_table=(('T', 'F'), ('F', 'T'), ('U', 'U'))\nscore_gt_7=((1, 'T'), (2, 'U'), (3, 'F'), (4, 'F'))\nwhere_gt_7=(1,)\nwhere_not_gt_7=(3, 4)\nwhere_gt_7_or_null=(1, 2)\nin_with_null=((1, 'U', 'U'), (2, 'U', 'U'), (3, 'T', 'F'), (4, 'U', 'U'))\ncheck_positive=((1, True), (2, True), (3, True), (4, False))\nnot_distinct_from_null=(2,)\n","stderr":""}} -->
```python
T, F, U = "T", "F", "U"
truths = (T, F, U)


def sql_not(value):
    return {T: F, F: T, U: U}[value]


def sql_and(left, right):
    if F in (left, right):
        return F
    return T if left == right == T else U


def sql_or(left, right):
    if T in (left, right):
        return T
    return F if left == right == F else U


def sql_equal(left, right):
    if left is None or right is None:
        return U
    return T if left == right else F


def sql_in(value, candidates):
    comparisons = tuple(sql_equal(value, candidate) for candidate in candidates)
    if T in comparisons:
        return T
    return U if U in comparisons else F


def is_not_distinct(left, right):
    if left is None or right is None:
        return left is None and right is None
    return left == right


rows = ((1, 10), (2, None), (3, 5), (4, -1))
comparisons = tuple((row_id, U if score is None else (T if score > 7 else F)) for row_id, score in rows)

and_table = tuple((left, right, sql_and(left, right)) for left in truths for right in truths)
or_table = tuple((left, right, sql_or(left, right)) for left in truths for right in truths)
not_table = tuple((value, sql_not(value)) for value in truths)
membership = tuple((row_id, sql_in(score, (5, None)), sql_not(sql_in(score, (5, None)))) for row_id, score in rows)

print(f"and_table={and_table}")
print(f"or_table={or_table}")
print(f"not_table={not_table}")
print(f"score_gt_7={comparisons}")
print(f"where_gt_7={tuple(row_id for row_id, truth in comparisons if truth == T)}")
print(f"where_not_gt_7={tuple(row_id for row_id, truth in comparisons if sql_not(truth) == T)}")
print(f"where_gt_7_or_null={tuple(row_id for (row_id, score), (_, truth) in zip(rows, comparisons) if sql_or(truth, T if score is None else F) == T)}")
print(f"in_with_null={membership}")
print(f"check_positive={tuple((row_id, score is None or score > 0) for row_id, score in rows)}")
print(f"not_distinct_from_null={tuple(row_id for row_id, score in rows if is_not_distinct(score, None))}")
```

Python `None`, Boolean comparison, tuples, and integer behavior are not SQL null, type, row, collation, constraint, or planner semantics. The model omits empty candidate subqueries, joins, grouping, aggregates, unique/FK enforcement, indexes, statistics, parameters, concurrency, and interfaces.

## Alternatives and Trade-Offs

`NOT NULL` simplifies logic, constraints, indexes, APIs, and statistics when absence is not a valid domain state. Nullable columns represent genuine partial information compactly but need explicit reason/lifecycle semantics. A companion status distinguishes causes but creates cross-column invariants. Separate subtype tables can model optional concepts relationally but add joins and presence constraints.

Null-safe equality is concise for reconciliation and change detection but may conflate two missing values and is dialect-specific. Explicit case analysis is verbose but exposes policy. `COALESCE` can produce convenient two-valued predicates but invents a sentinel/default and can change index use. `NOT EXISTS` avoids `NOT IN` null poisoning when its correlation equality and scope are correct, but it does not decide whether two null keys should match.

## Failure Modes and Misconceptions

- “Null is a value equal to null.” Ordinary comparison yields unknown; other operations define separate equivalence.
- “Unknown is false.” Filters discard both, but their negations and constraint behavior differ.
- “`p OR NOT p` is always true.” It is unknown when p is unknown.
- “`NOT p` selects every row p did not select.” Rows where p is unknown satisfy neither filter.
- “`NOT IN` means absent.” A null candidate can make nonmatches unknown.
- “A left join null means no match.” A matched right payload may itself be null; test a nonnull key.
- “CHECK enforces positive and present.” In PostgreSQL, unknown passes; add `NOT NULL` for presence.
- “UNIQUE null behavior follows equality.” It is constraint- and engine-specific.
- “`COALESCE` only changes display.” It changes logic, aggregation, identity, and possibly plans.
- “One null percentage supports one plan.” Correlation, parameters, indexes, statistics, and versions matter.

## Worked Examples

### Example 1

For predicate `p=(score>7)`, scores 10, null, and 5 produce T, U, F. `WHERE p` keeps 10; `WHERE NOT p` keeps 5. The null row is in neither result, demonstrating why the filters are not a partition of all input rows.

### Example 2

Candidates are `(5,NULL)`. Value 5 yields T for IN and F for NOT IN. Value 10 yields U for IN because comparisons are F and U; NOT IN remains U. A WHERE filter keeps neither. Prohibit/filter candidate nulls only if that matches domain identity.

### Example 3

A left join finds a right row whose optional note is null. Testing `right.note IS NULL` labels it “unmatched” incorrectly. Testing `right.primary_key IS NULL` distinguishes generated null extension because every real right row has a nonnull key.

### Example 4

`LEFT JOIN shipment s ON ... AND s.status='sent'` retains orders with no sent shipment. Moving `s.status='sent'` to WHERE removes null-extended orders. The first asks for optional matching sent shipment; the second asks only for orders having one.

### Example 5

`CHECK (discounted_price < price)` accepts a row with null discounted price in PostgreSQL because the comparison is unknown. If null means “no discount,” that may be valid; if both prices are mandatory, add not-null constraints. If they must appear together, encode the allowed state combinations.

### Example 6

`COUNT(*)` over three rows counts three; `COUNT(email)` counts only nonnull emails. A left join with one unmatched preserved row makes `COUNT(*)` at least one for that group while `COUNT(right.id)` is zero. Select the expression whose nullability matches the measure.

### Example 7

Two change-capture versions both have null middle name. Ordinary `old.middle_name <> new.middle_name` is unknown and does not signal equality. A null-safe comparison can classify unchanged, but the event model still distinguishes missing source field, explicit clear, and unavailable source.

### Example 8

A unique nullable email permits multiple nulls under PostgreSQL's default. `UNIQUE NULLS NOT DISTINCT` permits at most one null. Neither design says whether missing email should identify users; choose a constraint from the domain and test the target engine.

### Example 9

An API PATCH omits `display_name`, sends it as null, or sends a string. These can mean unchanged, clear, and set. Mapping all three to one nullable language field loses intent before SQL runs. Preserve a tagged state through validation and persistence.

### Example 10

A table has 90% null `closed_at`, strongly correlated with status. A query filters `status='closed' AND closed_at>=...`. Validate the invariant, collect supported correlation statistics, compare estimated/actual rows for null and nonnull parameters, and inspect index access rather than relying on marginal null fractions.

## Cross-Program Connections

- [Programming Languages and Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) explains denotation, option types, evaluation, and partial information.
- [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) models missing, unknown, inapplicable, and lifecycle states explicitly.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) governs null provenance, schema drift, late data, and quality metrics.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) preserves omitted, explicit-null, clear, and value states across contracts.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) defines fail-closed handling and auditable unknown decisions.

## References

1. PostgreSQL Global Development Group, [Logical Operators](https://www.postgresql.org/docs/18/functions-logical.html), PostgreSQL 18 three-valued truth tables.
2. PostgreSQL Global Development Group, [Comparison Functions and Operators](https://www.postgresql.org/docs/18/functions-comparison.html), PostgreSQL 18 null tests and distinct predicates.
3. PostgreSQL Global Development Group, [Constraints](https://www.postgresql.org/docs/18/ddl-constraints.html), PostgreSQL 18 CHECK, NOT NULL, UNIQUE, and foreign-key null behavior.
4. PostgreSQL Global Development Group, [Aggregate Functions](https://www.postgresql.org/docs/18/functions-aggregate.html), PostgreSQL 18 null and empty-input behavior.
5. SQLite Project, [NULL Handling in SQLite Versus Other Database Engines](https://www.sqlite.org/nulls.html), SQLite documentation.
6. SQLite Project, [SQL Language Expressions](https://www.sqlite.org/lang_expr.html), SQLite null, comparison, IN, and Boolean-expression rules.
7. Oracle, [Working with NULL Values](https://dev.mysql.com/doc/refman/8.4/en/working-with-null.html), MySQL 8.4 Reference Manual.
8. Oracle, [Comparison Functions and Operators](https://dev.mysql.com/doc/refman/8.4/en/comparison-operators.html), MySQL 8.4 Reference Manual.

## Exercises

### Exercise 1

For `p=U` and `q=F`, derive `NOT p`, `p AND q`, `p OR q`, `NOT(p OR q)`, `(NOT p) AND (NOT q)`, `p OR NOT p`, and `p AND NOT p`. Identify which classical expectations fail.

### Exercise 2

Candidate subquery values are `(2,NULL)`. Derive `x IN (...)` and `x NOT IN (...)` for x equal to 2, 3, and null. Then design a correct anti-membership query for a domain where candidate IDs must never be null.

### Exercise 3

Design constraints for `(started_at,finished_at)` where both may be absent for a draft, both must be present for a completed item, partial presence is invalid, and finish must not precede start. Enumerate null-state cases.

### Exercise 4

Prove whether moving predicate `R.active=TRUE` from a left join's ON clause to WHERE preserves results. Cover matching active, matching inactive, no right match, and matched right row with null active.

### Exercise 5

Create a production evidence plan for migrating a nullable customer tier to NOT NULL. Include semantic states, writers/readers, backfill provenance, constraints, APIs/events, truth-table tests, indexes/statistics/plans, concurrency, rollback, and verification.

## Answers to the Exercises

### Answer 1

`NOT U=U`; `U AND F=F`; `U OR F=U`; `NOT(U OR F)=U`; `(NOT U) AND (NOT F)=U AND T=U`, so De Morgan agrees. `U OR NOT U=U`, not T; `U AND NOT U=U`, not F. Excluded middle and noncontradiction do not produce their classical two-valued constants for unknown.

### Answer 2

For x=2, IN is T and NOT IN F. For x=3, comparisons are F and U, so IN and NOT IN are U. For null x, both comparisons are U, so both results are U. If candidate IDs are prohibited from being null, enforce `NOT NULL`, validate existing data, and use `NOT EXISTS (SELECT 1 FROM candidates c WHERE c.id=x.id)` with tenant/snapshot scope; retain a defensive null-quality check rather than silently filtering violations.

### Answer 3

Allow `(null,null)` for draft and `(nonnull,nonnull)` when `finished_at>=started_at`; reject `(nonnull,null)` and `(null,nonnull)`. One table CHECK can require `(both null) OR (both nonnull AND finish>=start)`, while status rules can require draft versus completed forms. Test all four presence combinations plus equal, later, and earlier finish values; remember PostgreSQL CHECK accepts unknown, so the presence clauses must prevent an unknown comparison from admitting partial rows.

### Answer 4

In ON, an active match joins; inactive or null-active matches fail the predicate, and a left row with no qualifying match is preserved with generated right nulls. In WHERE, the join first may produce inactive/null-active matched rows or an unmatched null-extended row; `R.active=TRUE` is F or U for all except active and removes them. The WHERE form therefore returns only active matches and is not equivalent unless a separate invariant proves every left row has an active right match and preservation is irrelevant.

### Answer 5

Define whether current null means unknown, legacy, invalid, or a real default and choose an authoritative mapping. Inventory every writer, reader, API, event, cache, and analytical consumer; deploy compatible code; add observability and a validated allowed-values/check rule; backfill in bounded batches with source/reason/version and reconcile counts. Prevent new nulls, test T/F/U and omitted/null/value interfaces, then enforce NOT NULL under a concurrency-safe migration and verify replicas. Recompute statistics, compare plans and index behavior for representative parameters, retain rollback/forward-repair procedures, and prove zero nulls plus semantic distribution after cutover.
