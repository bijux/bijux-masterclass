---
module_id: DBE-020
program: Database Engineering
level: 1
module_number: 20
title: Writing Correct SQL Under Duplicate and Null Semantics
status: complete
last_verified: 2026-08-30
---

# Writing Correct SQL Under Duplicate and Null Semantics

## One-Page Review

### Governing question

How can an engineer prove that a complete SQL statement returns or modifies exactly the intended bag of domain facts when joins multiply occurrences, predicates yield UNKNOWN, aggregation changes grain, and ordering is not implicit?

### Essential definitions

A **query contract** states input snapshot, one-row meaning, keys, multiplicity, null policy, output grain, order, and completeness. **Bag semantics** preserve occurrence counts unless an operator removes or combines them. **Three-valued logic** gives predicates T, F, or U; filter and join contexts accept only T. **Fanout** is the number of joined matches per input occurrence. **Grain** says what one row represents. A **semantic checksum** is an independently derived count, sum, key set, or invariant used to reconcile output—not a replacement for row-level proof.

### Central model, mechanism, or theorem

Model a query as typed bag transformations. For a row occurrence `r`, selection produces multiplicity `m(r)` when predicate is T and zero for F/U. An inner equijoin produces `m_L(l)*m_R(r)` occurrences for each true pair; a left join additionally emits one null-extended occurrence for a left row with zero true matches. Grouping maps occurrences to group keys, then folds each group bag under function-specific null rules. Projection can make distinct source occurrences look equal; DISTINCT maps every positive projected multiplicity to one. Correctness follows by proving each boundary preserves the stated grain and invariants.

### Critical invariants

- The contract names source authority, snapshot, tenant, input grain, output grain, keys, null meanings, and total order.
- Every join has expected per-key cardinality and measured fanout before aggregation.
- T/F/U outcomes are derived for every nullable predicate and anti-membership candidate.
- Identity deduplication uses stable business/event keys, never `DISTINCT` on an arbitrary payload.
- Counts identify whether they measure occurrences, matches, nonnull values, or distinct identities.
- Empty input, all-null input, null-extended rows, and stored nulls have separate expected results.
- Windows and top-N use a total stable order; final presentation has its own total order.
- Rewrites are accepted only with explicit key, null, multiplicity, type, volatility, and snapshot assumptions.

### Common failures

Failures include starting from SELECT syntax before defining grain, joining one-to-many data then summing parent measures, using DISTINCT to hide fanout, counting `*` after a left join when matches are intended, using nullable `NOT IN`, moving predicates across outer joins, coalescing unknown into zero without authority, averaging averages, selecting ungrouped arbitrary values, ranking without a tie-breaker, limiting without total order, comparing queries only on duplicate-free/non-null fixtures, and treating a green execution plan as semantic proof.

### Compact example

Customers 1–4 are checked against blacklist `(2,NULL)`. `id NOT IN (...)` is UNKNOWN for 1, 3, and 4 and false for 2, so WHERE returns none. A correlated `NOT EXISTS` on nonnull customer ID correctly retains 1, 3, and 4. Customer 1 has two paid orders, amounts 100 and null; customers 3 and 4 have none. A left join yields two rows for customer 1 and one null-extended row each for 3 and 4. `COUNT(order_id)` is 2,0,0; nonnull amount count is 1,0,0; sum is 100,null,null before a domain-approved zero presentation.

### Connections

[DBE-011](011-selection-projection-and-ordering.md) through [DBE-019](019-data-modification-and-upsert.md) supply the operators integrated here. Later storage, indexing, optimization, concurrency, and distributed modules explain physical execution and changing snapshots; those mechanisms never remove the need for this logical proof.

## Governing Question

SQL compresses a large semantic specification into a small expression. A query can parse, execute quickly, and return plausible rows while answering the wrong question. Most serious errors arise at boundaries: one-to-many joins change multiplicity, null changes a predicate from false to unknown, projection erases identity, aggregation hides fanout, or a partial order chooses an arbitrary winner.

Correct SQL is therefore not “SQL that runs.” It is a proof that each output occurrence represents the named domain fact, that all and only qualifying source occurrences contribute with intended multiplicity, and that nulls and ordering have declared meanings. The proof must survive adversarial fixtures and target-dialect execution, then be complemented by plan and operational evidence.

## Why This Matters

Billing, access control, regulatory reports, experiments, capacity, product analytics, and migrations depend on SQL. A duplicated revenue total can move money. A null-poisoned anti-join can omit every eligible customer. A nondeterministic latest-row query can oscillate after an index change. A soft-delete filter in the wrong join layer can erase parent rows. These defects often remain invisible in samples where keys happen to be unique and fields happen to be populated.

Query review is also a maintenance problem. Constraints change, nullable columns are introduced, joins gain another relationship, collations and time zones shift, and optimizers choose new plans. The durable artifact is a contract, adversarial fixture, independent oracle, and reconciliation suite that states why the query remains correct—not a screenshot of one result.

Performance and semantics interact but are distinct. Rewriting a correlated subquery as a join may improve a plan and change multiplicity. Pre-aggregation may reduce rows and move a filter boundary. An index can alter which tied row appears first without changing logical legality. Every optimization needs an equivalence proof under explicit assumptions and a physical measurement.

## Prerequisites and Retrieval

Retrieve relations and bags, keys and functional dependencies, T/F/U logic, selection/projection, joins, aggregation, subqueries, CTEs, set operations, windows, modifications, types and casts, collations, time zones, constraints, indexes, plans, transactions, parameterization, and testing.

Distinguish row occurrence from projected value, value equality from entity identity, base null from join-generated null, false from unknown, no rows from one null result, input grain from join grain from output grain, window order from result order, logical equivalence from plan similarity, and statement snapshot from multi-statement observation.

## Learning Objectives

After this module, you should be able to:

1. write a complete query contract before composing SQL;
2. trace multiplicities through selection, projection, joins, grouping, windows, and set operations;
3. derive every nullable predicate over T/F/U and its context action;
4. prove join cardinality and prevent fanout corruption;
5. distinguish occurrence, match, nonnull, and distinct-identity counts;
6. design correct anti-membership and outer-join predicates;
7. specify deterministic top-per-group, pagination, and final ordering;
8. justify or reject rewrites with explicit semantic assumptions;
9. construct independent oracles, metamorphic properties, and reconciliations; and
10. combine semantic, plan, resource, security, concurrency, and upgrade evidence.

## Core Exposition

Begin with a prose contract. Name the authoritative sources and snapshot/as-of. State one row in each source and one row in the output. List primary/business keys, tenant scope, expected uniqueness, nullable fields and meanings, units/currency/time zone, filters, duplicate policy, output ordering, pagination, and completeness. If one output row cannot be described precisely, the SQL is premature.

Represent each source as a bag. A key constraint may prove at most one occurrence per key; absent enforcement, current uniqueness is only an observation. Duplicate full values may be distinct events. Before every join or union, write expected per-key multiplicities and the identity whose occurrences must survive.

Follow logical boundaries rather than textual intuition: source/CTE construction; FROM and joins; WHERE; grouping and aggregates; HAVING; window calculations; projection; DISTINCT or set operation; final order; limit/offset/locking. Dialects expose aliases and extensions differently, and optimizers reorder physical work, but this decomposition is an effective semantic proof scaffold.

Selection preserves the multiplicity of an occurrence only when its predicate is true. False and unknown both yield no output in WHERE. Derive primitive comparisons first, especially nullable operands, then combine them with complete T/F/U tables. A test fixture needs match, nonmatch, and null—not merely two Boolean cases.

Do not assume negation forms a partition. `WHERE p` and `WHERE NOT p` omit rows where p is unknown. If a business complement includes uncertainty, name it: `p IS NOT TRUE` where supported or an explicit case expression. Security/eligibility policy must decide whether unknown denies, quarantines, escalates, or is treated as an allowed exceptional state.

An inner join starts from pairs and retains each true ON pair. If left key k occurs `a_k` times and right key k occurs `b_k` times, an equijoin can emit `a_k*b_k` pairs. This multiplication is correct bag semantics, not an optimizer bug. A declared many-to-one relationship needs a unique constraint on the one side; a many-to-many relationship needs a bridge identity and explicit downstream measures.

A left join emits true pairs, plus exactly one null-extended output for a left occurrence with zero true matches. It does not emit a null-extended row when a match exists but a right payload is null. Count a guaranteed-nonnull right identity to count matches. Test that identity for absence. `COUNT(*)` counts the preserved/null-extended occurrence too.

ON and WHERE are different around outer joins. A right predicate in ON defines qualifying matches while preserving unmatched left rows. The same null-rejecting predicate in WHERE removes null-extended rows and can make the result inner-like. To prove a move, enumerate active match, inactive match, null attribute, and no match, including several right matches.

Semijoins answer existence without multiplying left rows. `EXISTS` is often the direct expression for “has a qualifying related row.” Antijoins require an absence definition. Nullable `NOT IN` can become unknown due to any null candidate; `NOT EXISTS` with a complete correlation is safer when candidate identity is nonnull or its null policy is explicit.

Projection can collapse visible distinctions without changing bag multiplicity. Two different orders can both project `(customer_id,amount)=(2,50)` and appear duplicated. `DISTINCT` removes one projected occurrence, but this is not entity deduplication. Deduplicate by stable order/event key with a conflict and winner policy before dropping identity from presentation.

Aggregation changes grain. Define the input bag to each measure after joins and filters. `COUNT(*)` counts input occurrences; `COUNT(x)` counts nonnull x; distinct count counts value classes under type/collation rules. `SUM` and `AVG` commonly ignore null inputs; empty/all-null behavior differs from zero. A final `COALESCE` is valid only under an additive-domain rule.

Fanout before aggregation is the canonical silent error. If an order header joins five lines and its total is summed, it contributes five times. Pre-aggregate line measures to order grain, aggregate only line facts, or join a one-row-per-order relation. Reconcile counts and additive totals before and after joins; `SUM(DISTINCT order_total)` is not a repair because equal legitimate totals collapse.

Ratios, averages, and rates need separately additive numerator/denominator state. Do not average group averages without weights. Do not sum percentages. Preserve counts and sums, define zero/unknown denominators, units, eligibility, and rounding. Parallel/distributed aggregation later relies on the same merge-state proof.

Grouping null keys ordinarily forms one null group, despite ordinary `NULL=NULL` being unknown. DISTINCT and set operators use operation-specific not-distinct equality. Grouping-set subtotal nulls require grouping metadata to distinguish absent dimension from a real null key. Never apply predicate-equality intuition to every equivalence operation.

Subqueries have result-shape contracts. A scalar subquery returns null for zero rows, a value for one row, and errors on too many rows in documented systems; do not mask missing cardinality with arbitrary LIMIT. EXISTS observes row presence, not projected null. Correlation is logical dependence and may or may not be executed as nested loops after optimization.

CTEs name relations, not guaranteed materialized steps. A CTE boundary can improve the proof by stating schema/grain and assertions, but dialect/version decides folding and materialization. Do not rely on repeated evaluation, optimization fencing, or snapshot separation without documentation and plan evidence.

Set operations align columns by position and resolve types. UNION ALL adds multiplicities. DISTINCT union, intersection, and difference eliminate duplicates unless ALL is requested under documented syntax. Parenthesize mixed operators because precedence differs across engines. Cast every arm to a canonical semantic schema, including unit, time, collation, and provenance.

Window functions preserve row occurrences while deriving partition-relative values. Define partition key, peer order, deterministic occurrence order, and frame separately. `ROW_NUMBER` selection needs a total order; RANK peer semantics may intentionally omit a unique tie-breaker. Ordered aggregate defaults and `LAST_VALUE` can surprise; state frames explicitly.

Top-per-group needs an authority order, not merely determinism. Timestamp plus ID consistently chooses a row, but if timestamp ties indicate conflicting sources, ID does not establish truth. Define source precedence, effective versus recorded time, correction/tombstone policy, and retain discarded evidence.

Final output order is independent of joins, grouping, window order, DISTINCT implementation, or index traversal. Use a total `ORDER BY`, including stable tie-breaker. LIMIT/OFFSET without total order selects an unstable subset. Offset pagination can drift under concurrent inserts; keyset pagination and snapshot/as-of policy address different aspects.

Types are semantics. Implicit casts can change precision, time zone, collation, index use, and equality. Currency and units must be homogeneous. Numeric overflow and floating nonassociativity matter. Text normalization/collation determines join, grouping, distinct, and ordering classes. Explicit canonical conversion belongs at an owned boundary with versioned rules.

Query equivalence is conditional. An inner join can replace EXISTS for left-row retrieval only when right multiplicity cannot duplicate the left result or a justified deduplication follows. A left join plus `WHERE right.id IS NULL` can represent NOT EXISTS when id is guaranteed nonnull and join correlation is complete. Predicate pushdown through outer joins, aggregation, limits, volatility, or security barriers needs separate proof.

Keys and constraints are proof premises. A primary/unique constraint justifies at-most-one matches and some functional dependencies. Foreign keys can justify referential existence subject to null/match rules and snapshot. CHECK and NOT NULL support predicate simplification. If the database does not enforce the premise, encode validation and do not present it as guaranteed.

Modifications reuse query semantics to select affected rows. A nullable/duplicate-unsafe predicate can update or delete the wrong set. Upsert requires a unique business arbiter; optimistic updates require expected version; retries require payload-bound idempotency. RETURNING evidence and affected counts must be interpreted per dialect and commit outcome.

Parameterization separates values from SQL structure and prevents injection, but it does not validate tenant scope, identifier allowlists, units, or semantics. Dynamic identifiers and sort choices need strict allowlists and generated syntax. Different parameter values, especially null or skewed keys, can produce different plans and must be included in tests.

An independent oracle should use a different implementation route: a small standard-library model, hand-derived bag table, another validated query formulation, or controlled domain calculation. Avoid copying the same join/aggregation logic into both expected and actual paths. Compare sorted canonical rows and per-key multiplicities, not unordered screenshots.

Metamorphic properties strengthen tests. Duplicating a right row should double inner-join pairs but not change an EXISTS result. Adding an unrelated null to a `NOT IN` candidate set can turn nonmatches unknown but should not change a correct nonnull-key NOT EXISTS result. Reordering storage must not change a totally ordered result. Duplicating a legitimate equal-valued event must change occurrence counts but not distinct value count.

Reconciliation captures invariants: source/filtered counts; key/null/duplicate distributions; join match and fanout histograms; pre/post sums; unmatched keys; group counts; subtotal/grand totals; window selected identities; both set-difference directions; and modification outcomes. Hashes can accelerate comparison only with canonicalization and collision policy.

Adversarial fixtures include empty tables, singleton rows, duplicate full values with distinct IDs, duplicate relationship edges, null keys and payloads, unmatched and multiply matched joins, all-null groups, equal sort keys, boundary timestamps, type extremes, collation variants, stale versions, and concurrent changes. Tiny fixtures are powerful because every occurrence can be derived manually.

Semantic validation precedes physical validation. Then capture actual plans, estimated/actual rows at each node, join algorithms, sorts/hashes, memory, spill/temp I/O, parallel workers, partition pruning, index access, locks, latency, cancellation, and parameter cases. A plan can be fast and wrong because the query contract was wrong.

Production evidence records schema/constraint versions, query text/digest, parameters or safe classes, engine/configuration/statistics version, snapshot/as-of, output/reconciliation counts, plan, resource metrics, and reviewer. Re-run after schema, type, collation, time-zone data, index, statistics, engine, driver, or optimizer changes.

## Definitions and Notation

For bag `R`, multiplicity `m_R(r)`, predicate `p(r) in {T,F,U}`, and projection `pi`:

- selection has `m_(sigma_p R)(r)=m_R(r)` when `p(r)=T`, otherwise zero;
- inner equijoin pair `(l,r)` has multiplicity `m_L(l)*m_R(r)` when equality is T;
- left join adds one null-extended occurrence for each left occurrence with zero true right matches;
- projection multiplicity is `m_(pi R)(x)=sum_{r:pi(r)=x} m_R(r)`;
- DISTINCT maps every positive projected multiplicity to one;
- grouping key `g` forms group bag `G_k` from all occurrences with grouping-equivalent key k;
- a measure is correct only relative to the declared input bag, null rule, type, unit, and grain.

## Mechanisms, Invariants, or Proof Structure

A complete SQL review should:

1. write source authority, snapshot, tenant, source/output grain, keys, nulls, units, and total order;
2. inventory constraints and treat every unenforced key/dependency as an assumption to validate;
3. derive T/F/U for nullable filters, joins, membership, CASE, and HAVING;
4. trace per-key bag multiplicities through joins, projection, DISTINCT, and set operations;
5. define each aggregate's exact input occurrences, null/empty rule, type, unit, and denominator;
6. prove subquery cardinality, CTE boundaries, window partitions/orders/frames, and top-row authority;
7. justify rewrites with key/null/multiplicity/type/volatility/snapshot premises;
8. compare an independent oracle on adversarial and metamorphic fixtures;
9. reconcile counts, fanout, nulls, keys, measures, ordering, and modification outcomes; and
10. inspect actual plans, resources, locks, security, concurrency, cancellation, and upgrade regressions.

The finite model below evaluates nullable blacklist membership, a nonnull-key antijoin, paid-order left-join multiplicity, nullable aggregates, and deterministic latest identity for a fixed fixture. It makes the incorrect NOT IN result visible beside the intended NOT EXISTS result.

<!-- bijux-verify: {"id":"finite-sql-correctness-pipeline","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"not_in_truth=((1, 'U'), (2, 'F'), (3, 'U'), (4, 'U'))\neligible_customers=(1, 3, 4)\njoined_rows=((1, 'o1', 100), (1, 'o2', None), (3, None, None), (4, None, None))\nsummaries=((1, 2, 1, 100), (3, 0, 0, 0), (4, 0, 0, 0))\nlatest_paid=((1, 'o2'), (3, None), (4, None))\ngrand_paid_sum=100\nreconciled=True\n","stderr":""}} -->
```python
T, F, U = "T", "F", "U"
customers = ((1, "se"), (2, "se"), (3, None), (4, "us"))
orders = (
    ("o1", 1, 100, "paid", 1),
    ("o2", 1, None, "paid", 2),
    ("o3", 2, 50, "pending", 1),
    ("o4", 2, 50, "paid", 2),
    ("o5", 2, 50, "paid", 3),
    ("o6", None, 20, "paid", 1),
)
blacklist = (2, None)


def sql_equal(left, right):
    if left is None or right is None:
        return U
    return T if left == right else F


def sql_in(value, candidates):
    comparisons = tuple(sql_equal(value, candidate) for candidate in candidates)
    if T in comparisons:
        return T
    return U if U in comparisons else F


not_in_truth = []
eligible = []
for customer_id, _ in customers:
    membership = sql_in(customer_id, blacklist)
    not_in_truth.append((customer_id, {T: F, F: T, U: U}[membership]))
    if not any(sql_equal(customer_id, blocked) == T for blocked in blacklist):
        eligible.append(customer_id)

joined = []
summaries = []
latest = []
for customer_id in eligible:
    paid = tuple(order for order in orders if order[1] == customer_id and order[3] == "paid")
    if paid:
        joined.extend((customer_id, order[0], order[2]) for order in paid)
        latest.append((customer_id, max(paid, key=lambda order: (order[4], order[0]))[0]))
    else:
        joined.append((customer_id, None, None))
        latest.append((customer_id, None))
    amounts = tuple(order[2] for order in paid if order[2] is not None)
    summaries.append((customer_id, len(paid), len(amounts), sum(amounts) if amounts else 0))

grand_paid_sum = sum(summary[3] for summary in summaries)
source_paid_sum = sum(order[2] for order in orders if order[1] in eligible and order[3] == "paid" and order[2] is not None)

print(f"not_in_truth={tuple(not_in_truth)}")
print(f"eligible_customers={tuple(eligible)}")
print(f"joined_rows={tuple(joined)}")
print(f"summaries={tuple(summaries)}")
print(f"latest_paid={tuple(latest)}")
print(f"grand_paid_sum={grand_paid_sum}")
print(f"reconciled={grand_paid_sum == source_paid_sum}")
```

Python equality, `None`, integers, tuple order, and explicit loops are not SQL null, type, collation, join, grouping, window, or execution semantics. The model omits duplicate customer IDs, duplicate full order rows, time zones, overflow, database constraints, plans, concurrency, and modifications.

## Alternatives and Trade-Offs

One complex query can keep a single snapshot and let the optimizer share work, but it can obscure grain boundaries and create interacting fanout. Several named CTEs/subqueries can make contracts reviewable, though names do not force materialization and extra layers can affect optimization. Precomputed summaries improve repeated reads but add freshness, correction, lineage, and reconciliation obligations.

EXISTS/NOT EXISTS preserve left multiplicity directly; joins expose related rows but can multiply them. Window selection retains evidence for ranking; aggregate-plus-join can be efficient but needs tie handling. DISTINCT is appropriate for value-set semantics; key-based row selection is appropriate for entity deduplication. Portable syntax reduces dialect divergence, while target-specific features can be safer or clearer when isolated, documented, and tested.

## Failure Modes and Misconceptions

- “The schema sample is unique.” Only an enforced key or validation evidence supports cardinality.
- “Duplicates are dirty data.” They may be legitimate occurrences; identify entities and events first.
- “DISTINCT repairs duplicate joins.” It hides projected symptoms and can erase legitimate equal values.
- “Null is false.” Filter contexts discard both, but truth, negation, checks, and equality differ.
- “NOT IN is an antijoin.” Nullable candidates can make nonmatches unknown.
- “A left join preserves left rows after any WHERE.” Null-rejecting right predicates can remove them.
- “COUNT(*) counts matches.” It counts null-extended occurrences after an outer join too.
- “Latest timestamp selects a row.” Ties need stable authority and deterministic ordering.
- “Equivalent-looking queries are equivalent.” Keys, nulls, bags, types, volatility, and snapshots are premises.
- “A fast plan proves correctness.” Physical evidence answers resource questions only after semantic proof.

## Worked Examples

### Example 1

Orders contain two distinct IDs with the same customer and amount. Projecting `(customer,amount)` shows duplicates; DISTINCT removes one and undercounts events. Preserve order ID through identity-sensitive stages and aggregate occurrences deliberately.

### Example 2

Blacklist contains customer 2 and null. `NOT IN` yields false for 2 and unknown for other nonnull IDs, so WHERE can return none. `NOT EXISTS` correlated on a nonnull customer ID returns customers 1, 3, and 4. The null candidate is also surfaced as a data-quality signal.

### Example 3

Customer 1 has two paid orders, so a left join emits two rows. Customers 3 and 4 have none, so each emits one null-extended row. `COUNT(*)` gives 2,1,1; `COUNT(order_id)` gives 2,0,0. Neither is “the count” without a named measure.

### Example 4

One paid amount is 100 and another is null. `COUNT(amount)=1`, paid-order count is 2, and sum is 100. The null amount is not zero. Customers with no paid orders receive null sum in ordinary SQL aggregation; converting that to zero requires an additive-domain presentation rule.

### Example 5

Order headers join lines. Summing header total after the join multiplies it by line count. Aggregate line amounts to order grain or select one header occurrence per order, then reconcile header and line totals. `SUM(DISTINCT total)` collapses separate equal-total orders.

### Example 6

A left join filters `right.active` in ON to find optional active relationships while preserving every left row. Moving it to WHERE drops left rows with no active match. An adversarial fixture with active, inactive, null-active, and absent right rows proves the difference.

### Example 7

Latest order per customer uses `ROW_NUMBER` over `(event_time DESC, source_sequence DESC, order_id)`. If source sequence is not authoritative, the order is deterministic but may choose the wrong correction. Preserve competing versions and document precedence.

### Example 8

`SELECT customer_id, customer_name, SUM(...) GROUP BY customer_id` is safe only if customer ID functionally determines the intended name at the query snapshot. A history join may produce several names. Constraint and temporal evidence—not current coincidence—justify the dependency.

### Example 9

An optimizer rewrite changes NOT EXISTS to an antijoin and chooses a hash plan. The semantics can remain correct while row estimates and spill behavior change. Compare canonical output plus per-key counts, then inspect estimates, hash memory/batches, temp I/O, and skew separately.

### Example 10

A report is exported twice while source rows change. Total ordering makes each statement deterministic but does not make snapshots equal. Record as-of/isolation, query and schema versions, parameters, row counts, reconciliations, and result digest; use a stable snapshot/versioned source for reproducible exports.

## Cross-Program Connections

- [Programming Languages and Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) supplies denotational reasoning, types, and contextual equivalence.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies independent oracles, invariants, complexity, sorting, and hashing.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) governs event identity, deduplication, CDC, schema drift, and reconciliation.
- [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies property, metamorphic, differential, boundary, and regression testing.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) requires tenant isolation, parameterization, least privilege, and fail-closed unknown handling.

## References

1. PostgreSQL Global Development Group, [SELECT](https://www.postgresql.org/docs/18/sql-select.html), PostgreSQL 18 processing, join, DISTINCT, set, ordering, and limit documentation.
2. PostgreSQL Global Development Group, [Table Expressions](https://www.postgresql.org/docs/18/queries-table-expressions.html), PostgreSQL 18 FROM, WHERE, joins, grouping, and window processing.
3. PostgreSQL Global Development Group, [Comparison Functions and Operators](https://www.postgresql.org/docs/18/functions-comparison.html), PostgreSQL 18 null and distinct comparison documentation.
4. PostgreSQL Global Development Group, [Aggregate Functions](https://www.postgresql.org/docs/18/functions-aggregate.html), PostgreSQL 18 aggregate and empty/null behavior.
5. SQLite Project, [SELECT](https://www.sqlite.org/lang_select.html), SQLite join, DISTINCT, compound, null, order, and limit documentation.
6. SQLite Project, [NULL Handling](https://www.sqlite.org/nulls.html), SQLite cross-engine null behavior documentation.
7. Oracle, [SELECT Statement](https://dev.mysql.com/doc/refman/8.4/en/select.html), MySQL 8.4 Reference Manual.
8. Oracle, [MySQL Handling of GROUP BY](https://dev.mysql.com/doc/refman/8.4/en/group-by-handling.html), MySQL 8.4 functional-dependency and grouping documentation.

## Exercises

### Exercise 1

Given left key multiplicities `L(a)=2`, `L(b)=1` and right multiplicities `R(a)=3`, `R(b)=0`, derive inner-join and left-join row counts by key, plus `COUNT(*)` and `COUNT(right_key)` after grouping by left key.

### Exercise 2

Candidate values are `(2,NULL)` and source IDs are 1, 2, 3. Derive NOT IN truth and WHERE output. Then derive a NOT EXISTS antijoin under nonnull source/candidate identity and state the data-quality check still required.

### Exercise 3

Design a query contract and proof for revenue per customer when orders join line items, some line amounts are null, two orders can have the same total, currencies differ, and customers with no orders must appear.

### Exercise 4

Propose an adversarial/metamorphic suite to prove that an EXISTS query and a join-based rewrite return the same customer bag. State the exact uniqueness or deduplication premises needed.

### Exercise 5

Create a production evidence package for a monthly regulatory SQL report. Include schema/constraints, snapshot, parameters, grain/null/unit/time policy, oracle, fixtures, reconciliations, deterministic order, plan/resources, security, concurrency, rendered/export evidence, and upgrade regression.

## Answers to the Exercises

### Answer 1

For a, inner join emits `2*3=6`; for b, zero. A left join emits six for a and one null-extended occurrence for b. Grouped `COUNT(*)` is a:6, b:1. `COUNT(right_key)` is a:6, b:0 when right_key is guaranteed nonnull on real matches. If the measure is distinct right entities, these counts are still wrong without an identity-level distinct or pre-aggregation.

### Answer 2

For ID 2, membership is true and NOT IN false. For IDs 1 and 3, comparisons include false and unknown, so IN and NOT IN are unknown. WHERE retains none. With enforced nonnull candidate IDs, `NOT EXISTS (SELECT 1 FROM candidates c WHERE c.id=s.id)` retains 1 and 3. Validate/enforce candidate nonnullness and monitor violations rather than silently ignoring them.

### Answer 3

Output grain is one row per canonical customer at a named snapshot, including zero-order customers. Join customers left to a one-row-per-order measure relation; derive each order from lines at line grain, preserving order ID. Define null line amount as unknown/rejected rather than zero unless domain authority says otherwise; normalize currency using versioned rate/time before addition; use exact numeric/rounding rules. Never sum header total after line fanout or use DISTINCT amount. Count matched order IDs, coalesce empty sum only for the approved zero presentation, and reconcile per-currency/source/order/customer totals plus unmatched/null rows.

### Answer 4

Use empty right, one match, several matches, duplicate full right rows, null join keys, unmatched rows, several left duplicates, and tenant collisions. Metamorphically duplicate a qualifying right occurrence: EXISTS output multiplicity must not change, while a raw inner join multiplies left rows. Equivalence requires either an enforced at-most-one qualifying right row per correlation key or a justified semijoin/deduplication that preserves the left bag; correlation, null equality, tenant, filters, and snapshot must be identical.

### Answer 5

Freeze and record an authoritative snapshot/as-of, schema and constraint versions, query digest, safe parameter classes, source/output grain, keys, null/empty rules, currency/unit/time-zone/rounding, and total order. Maintain an independent calculation and adversarial fixtures covering duplicates, nulls, fanout, empty/all-null groups, ties, and boundaries. Reconcile source/filter/join/group counts, fanout, unmatched/nulls, additive totals, both differences, selected identities, and export digest. Capture actual plans, estimates, indexes, memory/spill, parallelism, latency, cancellation, and production-shaped parameter cases; test tenant/role/parameterization and snapshot concurrency. Validate rendered columns/order/rounding, obtain the required named human sign-off separately, and rerun semantic plus resource/export gates after schema, data-rule, collation/time-zone, engine, driver, statistics, index, or configuration changes.
