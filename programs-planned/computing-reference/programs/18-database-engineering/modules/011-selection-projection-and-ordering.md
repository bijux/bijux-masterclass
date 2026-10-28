---
module_id: DBE-011
program: Database Engineering
level: 1
module_number: 11
title: Selection, Projection, and Ordering
status: complete
last_verified: 2026-08-30
---

# Selection, Projection, and Ordering

## One-Page Review

### Governing question

How does a SQL query choose rows, construct output columns, and impose a deterministic order without confusing relational semantics, SQL bag behavior, null logic, or physical access order?

### Essential definitions

**Selection** filters input rows by a predicate; in relational notation it is `sigma_P(R)`. SQL `WHERE` retains only rows for which its condition is `TRUE`, rejecting both `FALSE` and `UNKNOWN`. **Projection** computes the output expressions; relational projection is often set-valued, while ordinary SQL `SELECT` preserves duplicate rows. **Bag semantics** allow repeated equal tuples. `DISTINCT` removes duplicates from the projected result. **Ordering** maps a bag to a sequence using comparison keys, directions, collation, and null placement. A **total order** distinguishes every output position; a **stable pagination key** is immutable or governed well enough to resume traversal deliberately.

### Central model, mechanism, or theorem

For a simple query, reason conceptually as:

`FROM -> WHERE -> SELECT expressions -> DISTINCT -> ORDER BY -> OFFSET/FETCH or LIMIT`.

Optimizers may execute equivalent operations differently. Selection does not preserve a physical order contract; projection does not remove duplicates unless requested; and ordering is guaranteed only by an applicable outer `ORDER BY`. If ordering keys tie, their relative output order remains unspecified. Deterministic `LIMIT`, pagination, or “first row” therefore requires enough keys—usually including a unique tie-breaker—to form a total order under an explicit collation and null policy.

### Critical invariants

- Every predicate is evaluated with SQL three-valued logic and explicit null intent.
- Parameters carry values; dynamic identifiers and sort choices come from allowlists.
- Projection names and types form a deliberate interface rather than relying on `*`.
- Duplicate preservation or elimination is specified and tested intentionally.
- An ordering guarantee appears at the consumer's outer query boundary.
- Direction, collation, null placement, and a unique tie-breaker define total order.
- Pagination cursor and predicate use the exact same lexicographic order.
- Result row/byte limits, timeouts, authorization, and sensitive-column exposure are bounded.

### Common failures

Failures include writing `column = NULL`, accidentally excluding nulls through `NOT`, using truthiness instead of SQL predicates, interpolating values or `ORDER BY` tokens, projecting `*` across schema changes, assuming projection removes duplicates, adding `DISTINCT` to hide a faulty join, relying on heap/index/insertion order, sorting only inside a subquery, paginating tied keys without a tie-breaker, using a mismatched keyset predicate, accepting arbitrary collations, large offsets, leaking hidden sort keys, and returning unbounded rows.

### Compact example

Five rows contain three Swedish scores at least 30, one Swedish null score, and one US row. `WHERE country='se' AND score>=30` selects IDs `(1,3,5)`; null comparison is `UNKNOWN`. Projecting `(name,score)` yields two identical `('Ada',30)` tuples and one `('Mira',40)` because SQL is a bag. `DISTINCT` reduces that projection to two tuples. Ordering by score descending, name ascending, and ID ascending gives `(5,1,3)`; a two-row first page ends at ID 1, and the matching keyset continuation yields ID 3.

### Connections

[DBE-002](002-relational-model-and-relational-algebra.md) provides relational foundations, while [DBE-009](009-life-of-a-read-query.md) explains execution. [DBE-012](../ROADMAP.md) adds joins. API Engineering connects result contracts and cursors; Security Engineering owns parameter, authorization, and data-exposure boundaries.

## Governing Question

The shortest useful SQL query can still make several independent promises: which source rows qualify, which values and names appear, whether duplicate tuples survive, and in what sequence a client observes them. These promises are logical. An index, sort operator, or current plan may implement them, but implementation artifacts do not silently become query semantics.

The engineering task is to express each promise explicitly and test difficult values: nulls, duplicates, collation-equivalent strings, numeric and temporal boundaries, tied order keys, schema changes, concurrent inserts/deletes, and large result sets. Correctness precedes access-path tuning; after semantics are fixed, indexes and plans can be evaluated against the exact workload.

## Why This Matters

Selection defines data access and business meaning. A null comparison can silently exclude rows; a misplaced predicate can turn an outer join into an inner one; a permissive dynamic filter can become injection or authorization bypass. Parentheses, data types, collations, time zones, and function volatility matter.

Projection is an API and governance boundary. `SELECT *` couples consumers to column order and future sensitive fields. Computed expressions can change types or nullability. Duplicate rows may be legitimate under SQL bags, but a client may mistakenly treat them as unique entities. `DISTINCT` can hide incorrect multiplicity while adding sort/hash work.

Ordering controls reproducibility, pagination, and “top” decisions. Without an outer order, an engine may return any valid sequence and change it with data, statistics, parallelism, indexes, version, or `LIMIT`. A non-unique order is only partial: tied rows can swap. Production cursors must encode the same total order used by the query and define behavior under mutation.

## Prerequisites and Retrieval

Retrieve relations, tuples, bags/multisets, predicates, three-valued logic, null, data types, expressions, aliases, collations, indexes, sorting, lexicographic order, transactions, snapshots, parameters, authorization, pagination, and query plans.

Distinguish input column from output alias; value from identifier; logical order from physical access; set projection from SQL bag projection; row uniqueness from projected-tuple uniqueness; `UNKNOWN` from `FALSE`; and deterministic ordering from repeatable results under changing data.

## Learning Objectives

After this module, you should be able to:

1. translate selection and projection between relational notation and SQL bag semantics;
2. evaluate predicates under `TRUE`, `FALSE`, and `UNKNOWN`;
3. design typed, parameterized filters with correct boundary conditions;
4. construct stable projection interfaces with explicit aliases and types;
5. reason about duplicates before and after `DISTINCT`;
6. specify direction, collation, null order, and unique tie-breakers;
7. distinguish offset from keyset pagination semantics and costs;
8. design mutation-aware cursor contracts;
9. choose candidate indexes from filter/order requirements; and
10. verify result equality, order, resource bounds, and authorization.

## Core Exposition

In relational algebra, selection `sigma_P(R)` returns tuples of relation `R` satisfying predicate `P`. It preserves the relation's attributes and, in classical set algebra, cannot introduce duplicates. SQL begins from tables and intermediate results that usually behave as bags. `WHERE P` filters occurrences: if two identical input rows each satisfy `P`, both continue.

SQL conditions use three truth values. Comparison with null generally yields `UNKNOWN`, including `x = NULL` and `x <> NULL`; use `IS NULL` or `IS NOT NULL`. `WHERE` retains only `TRUE`, so both `FALSE` and `UNKNOWN` disappear. `NOT UNKNOWN` remains `UNKNOWN`. This is why `NOT (status='closed')` does not necessarily include rows whose status is null.

The truth tables matter. `TRUE AND UNKNOWN` is `UNKNOWN`; `FALSE AND UNKNOWN` is `FALSE`; `TRUE OR UNKNOWN` is `TRUE`; `FALSE OR UNKNOWN` is `UNKNOWN`. De Morgan transformations remain compatible with three-valued logic at the truth-value level, but application intuitions about “everything not equal” often omit null. State whether null means unknown, absent, not applicable, or invalid; do not collapse meanings casually.

Predicate precedence typically places `NOT` above `AND` above `OR`, but production queries should use parentheses around business rules. `active AND country='se' OR privileged` differs in readability and possibly intent from `active AND (country='se' OR privileged)`. Tests should enumerate boundary combinations rather than rely on prose.

Typed parameters separate values from SQL syntax and let binding select operators. They do not parameterize arbitrary identifiers, keywords, or directions in many interfaces. A user-selected field or sort direction should map from a small public enum to reviewed SQL fragments. Never concatenate unchecked input. Parameter type also matters: implicit casts can change semantics, collation, precision, and index eligibility.

Range boundaries must be explicit. For timestamps, a half-open interval `occurred_at >= start AND occurred_at < end` composes cleanly and avoids inventing a “last instant” at an unknown precision. Normalize the intended time zone before comparison. Decimal versus floating arithmetic, Unicode normalization, case folding, and locale comparison require domain policy and test fixtures.

Predicates may be sargable—usable to derive an access range—or may require evaluating an expression for many rows. Rewriting `date(ts)=d` as an appropriate half-open timestamp range can permit an index range while preserving intended time-zone semantics. An expression index is another option. Sargability is engine-specific performance evidence; never change null, collation, overflow, or function semantics merely to attract an index.

Projection is the `SELECT` list. Each item can be an input column, constant, scalar expression, conditional, function, or composite value. Give public expressions durable aliases. Qualify ambiguous source columns. Define output type, nullability, units, time zone, encoding, and sensitivity. A database driver can expose different host types for numerics, timestamps, arrays, and nulls, so integration tests belong at the client boundary.

Avoid `SELECT *` for durable interfaces. Adding a column can change output position, network bytes, object mapping, access control, covering-index eligibility, or serialization. Wide blobs can dominate latency even if unused. `table_alias.*` can be useful for controlled exploration or internal transformations, but explicit public projection is reviewable and least-privilege friendly.

Ordinary SQL projection preserves duplicates. `SELECT country FROM customer` can return `se` many times. `SELECT DISTINCT country` applies duplicate elimination after computing the projection. It treats rows equal under the engine's type/collation/null distinctness rules for that operation. `DISTINCT` changes meaning and often requires hash or sort resources; it is not a generic performance repair.

Projection can create duplicates even if source rows have unique IDs. Two customers named Ada become the same tuple after projecting only `name`. Conversely, including the unique ID prevents equal full projected tuples. Always ask whether the consumer operates on entities, events, or value combinations. Row counts before and after projection/distinct are valuable invariants.

Output aliases name expressions. SQL dialects differ in where aliases are visible; PostgreSQL allows output labels in `ORDER BY` with ambiguity rules but not as a universal replacement for input expressions in all clauses. Prefer unambiguous aliases and avoid reusing an input name for a different expression. Ordinal ordering such as `ORDER BY 2` is terse but fragile when projection changes.

A table/relation has no inherent presentation order. Without an applicable outer `ORDER BY`, output order is unspecified. A sequential scan can follow current physical pages, an index scan can follow key order, a hash join can reorder, and parallel workers can interleave. The optimizer may choose a different plan for different limits. Tests that compare unsorted sequences encode an invalid promise.

`ORDER BY` evaluates one or more keys lexicographically. For each key, specify ascending or descending direction as needed. Direction can differ by key. The engine's data type and operator class define comparison. Text ordering depends on collation; byte order, linguistic order, case-insensitive order, and locale/version-specific order are different contracts. Pin or record collation for reproducibility and upgrades.

Null placement is dialect- and direction-sensitive unless specified. Use supported `NULLS FIRST` or `NULLS LAST`, or a portable explicit discriminator such as `ORDER BY (x IS NULL), x` after verifying dialect behavior. A null-order policy must be mirrored in cursor encoding and continuation predicates. Treat null cursor values as structured states, not ad hoc sentinels that can collide with real data.

Ordering keys define a total order only if no two output rows compare equal across all keys. Add a unique, immutable tie-breaker such as primary key. `ORDER BY created_at DESC` is partial when timestamps tie; `ORDER BY created_at DESC,id DESC` is total if `id` is unique. If collation considers distinct strings equal, ID still resolves their order.

Ordering inside a subquery does not generally promise the outer query's delivery order. The outer consumer requires its own `ORDER BY`. Some inner ordering is meaningful to operations such as limiting, ordered aggregates, or window calculations, but final presentation remains a separate boundary. Likewise, an index may satisfy order without a sort operator, but the SQL order—not index existence—is the contract.

`LIMIT`, `FETCH`, or equivalent truncates an ordered sequence when deterministic selection is intended. Without a total order, “first 20” is undefined among valid arrangements. `WITH TIES` deliberately returns more than the nominal count when rows share the boundary ordering keys; understand whether unique tie-breakers defeat that grouping purpose.

Offset pagination asks the engine to discard preceding rows and can become expensive at deep pages. Under concurrent mutation, inserts before the offset can duplicate rows across pages and deletes can cause skips. A repeatable snapshot can stabilize one traversal but may be costly or impractical across stateless requests. Offset remains appropriate for small stable results or interfaces requiring arbitrary page numbers with accepted semantics.

Keyset pagination continues after the last order tuple. For `ORDER BY score DESC,name ASC,id ASC`, the continuation is a lexicographic “after” predicate respecting mixed directions and null policy, not simply `id > cursor_id`. Row-value comparison can simplify only when dialect and null semantics match. The cursor should encode all keys, query/filter/version identity, and be integrity-protected when clients must not alter it.

Keyset pagination is stable relative to a moving order boundary, not magically snapshot-consistent. If an ordering value changes, a row can move before or after the cursor; inserts can appear in future or already-passed regions. Choose immutable order keys, freeze an upper bound/as-of snapshot, or document live-feed behavior. Authorization and filters must be re-evaluated on every page.

Selection and order jointly suggest indexes. Equality-constrained leading keys followed by range/order keys can support filtering and ordered traversal; projection columns may make access covering. But index layout, direction, nulls, collation, selectivity, and engine capabilities matter. More indexes amplify writes. Establish correct SQL, inspect a plan, test representative data/skew/parameters, and measure read/write effects.

Sorting can be blocking and memory-intensive; large sorts may spill. A top-N algorithm may avoid fully sorting all rows, and an ordered index may avoid a separate sort. `DISTINCT` can also hash or sort. Capture actual rows, estimates, memory/spill, temp I/O, first/last-row latency, and output bytes. Do not infer semantics from the chosen algorithm.

Result governance completes the query. Bound row and byte counts; paginate or stream with backpressure; impose deadlines and cancellation; project only authorized fields; and avoid exposing secret hidden order keys. A client must not resort with a different collation and still claim database order. Verify decoded values and order at the consuming boundary.

## Definitions and Notation

For bag `R`, let multiplicity `m_R(t)` count occurrences of tuple `t`.

- Selection: `m_sigma(t)=m_R(t)` when predicate is `TRUE`, otherwise `0`; `UNKNOWN` is not retained.
- SQL bag projection onto expression vector `f`: `m_pi(u)=sum_{t:f(t)=u} m_R(t)`.
- `DISTINCT` maps every positive output multiplicity to `1`.
- Ordering key `K(t)=(k_1(t),...,k_n(t))` uses declared directions, collation, and null policy.
- Total order requires a comparison result for every pair and no equal `K` for distinct output occurrences when deterministic positions are required.
- Keyset continuation returns rows strictly after cursor key `K_c` under the exact same lexicographic comparator.

Classical relational projection commonly removes duplicates; SQL `SELECT` does not. The notation describes logical results, not optimizer execution order.

## Mechanisms, Invariants, or Proof Structure

A selection/projection/order review should:

1. define source scope, role, snapshot, and expected multiplicities;
2. enumerate predicate truth values for null and boundary inputs;
3. bind values as typed parameters and allowlist dynamic syntax;
4. specify projection aliases, types, nullability, units, and sensitivity;
5. decide whether duplicates are meaningful and justify `DISTINCT` if used;
6. define direction, collation, null placement, and unique tie-breaker;
7. derive pagination cursor and continuation from the same comparator;
8. test mutations, tied keys, nulls, duplicates, and cursor tampering;
9. inspect plans, rows, estimates, sort/distinct memory and spill, and index write cost; and
10. verify ordered decoded results, limits, authorization, timeout, and cancellation.

The finite model below implements SQL-like `UNKNOWN`, bag projection, explicit distinct, total ordering, limiting, and keyset continuation for a fixed fixture. It is not a SQL engine, collation implementation, optimizer, or concurrent snapshot.

<!-- bijux-verify: {"id":"finite-select-project-order","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"null_comparison=unknown\nselected_ids=(1, 3, 5)\nprojected_bag=(('Ada', 30), ('Ada', 30), ('Mira', 40))\ndistinct_projection=(('Ada', 30), ('Mira', 40))\nordered_ids=(5, 1, 3)\nfirst_page=(5, 1)\nnext_page=(3,)\nselected_count=3\ndistinct_count=2\n","stderr":""}} -->
```python
UNKNOWN = "unknown"
rows = (
    {"id": 1, "name": "Ada", "country": "se", "score": 30},
    {"id": 2, "name": "Lin", "country": "se", "score": None},
    {"id": 3, "name": "Ada", "country": "se", "score": 30},
    {"id": 4, "name": "Kay", "country": "us", "score": 40},
    {"id": 5, "name": "Mira", "country": "se", "score": 40},
)


def sql_gte(left, right):
    return UNKNOWN if left is None or right is None else left >= right


def sql_and(left, right):
    if left is False or right is False:
        return False
    if left == UNKNOWN or right == UNKNOWN:
        return UNKNOWN
    return True


def predicate(row):
    return sql_and(row["country"] == "se", sql_gte(row["score"], 30))


selected = tuple(row for row in rows if predicate(row) is True)
projected = tuple((row["name"], row["score"]) for row in selected)
distinct = tuple(dict.fromkeys(projected))
ordered = tuple(sorted(selected, key=lambda row: (-row["score"], row["name"], row["id"])))
first_page = ordered[:2]
cursor_key = (-first_page[-1]["score"], first_page[-1]["name"], first_page[-1]["id"])
next_page = tuple(
    row for row in ordered if (-row["score"], row["name"], row["id"]) > cursor_key
)

print(f"null_comparison={sql_gte(None, 30)}")
print(f"selected_ids={tuple(row['id'] for row in selected)}")
print(f"projected_bag={projected}")
print(f"distinct_projection={distinct}")
print(f"ordered_ids={tuple(row['id'] for row in ordered)}")
print(f"first_page={tuple(row['id'] for row in first_page)}")
print(f"next_page={tuple(row['id'] for row in next_page)}")
print(f"selected_count={len(selected)}")
print(f"distinct_count={len(distinct)}")
```

Python string comparison is not a database collation, dictionary insertion order is used only to make the distinct fixture deterministic, and rows never mutate. A production cursor must model nulls, directions, collation/version, authorization, query identity, and mutation policy explicitly.

## Alternatives and Trade-Offs

Explicit projection is stable and least-privilege friendly but requires intentional schema evolution. `*` is convenient for exploration but brittle for APIs. `DISTINCT` expresses value-combination uniqueness but consumes resources and can mask incorrect joins; model true entity uniqueness with keys. Database sorting centralizes the declared comparator, while client sorting can only reorder the fully fetched result and may use different semantics.

Offset pagination supports direct page numbers but performs/discards prefix work and shifts under mutation. Keyset pagination scales with a suitable access path and follows a boundary but cannot jump arbitrarily and requires cursor/comparator discipline. Snapshot pagination offers stable membership/order but retains state or versions. Materializing result IDs offers explicit stability at storage/cleanup cost.

## Failure Modes and Misconceptions

“`WHERE` keeps everything not false” is wrong: it keeps only true. “`NOT x=1` includes null” is wrong because `NOT UNKNOWN` remains unknown. “Projection means distinct” imports classical set algebra into default SQL bag semantics. “`DISTINCT` fixes duplicates” may conceal an unintended many-side join.

“The primary key determines output order” is false without `ORDER BY`. “The subquery is sorted” does not promise outer delivery. “Timestamp descending is deterministic” fails on ties. “Keyset means `id > cursor`” fails when the declared order uses other keys/directions/nulls. “The same query repeats the same pages” ignores snapshots and mutation.

“An index makes sorting free” ignores traversal, visibility, lookup, and write cost. “Large offset returns only 20 rows, so it examines 20” confuses output with work. “Parameterized SQL permits parameterized column names” confuses values with syntax. “Client collation is close enough” is not an ordering contract.

## Worked Examples

### Example 1

`WHERE deleted_at = NULL` returns no true comparisons. `WHERE deleted_at IS NULL` expresses active rows. A test includes null, past, and future timestamps.

### Example 2

`WHERE NOT status='closed'` excludes null status. If null should mean open, the query states `status <> 'closed' OR status IS NULL` and the domain documents that meaning.

### Example 3

A half-open UTC day uses `occurred_at >= start AND occurred_at < next_start`. It avoids fractional-second assumptions and composes adjacent days without overlap.

### Example 4

Two source rows have different IDs but both project to `('Ada',30)`. Default `SELECT name,score` returns two occurrences; `DISTINCT` returns one value tuple and loses entity identity.

### Example 5

An API replaces `SELECT *` with `id,name,score AS ranking_score`. A newly added `internal_note` is neither transmitted nor accidentally exposed, and output compatibility is testable.

### Example 6

`ORDER BY score DESC` ties IDs 1 and 3. Adding `name ASC,id ASC` produces a total order. The ID tie-breaker remains necessary even when names currently differ in most rows.

### Example 7

Swedish and binary collations order accented/case variants differently. The API records one database collation and cursor version; a collation upgrade triggers ordering regression tests and cursor compatibility policy.

### Example 8

Page one under `score DESC,name ASC,id ASC` ends at `(30,'Ada',1)`. Continuation compares the complete mixed-direction key and returns ID 3, not every ID greater than 1 globally.

### Example 9

An offset page duplicates a row after a new higher-scoring row is inserted before its boundary. A live keyset feed avoids prefix shift but may never show the new already-passed row; the API documents that behavior.

### Example 10

An index on `(country,score DESC,name,id)` is tested for the filtered order. Plans, skew, rows, buffers, sort/spill, output bytes, and added write amplification are measured before adoption.

## Cross-Program Connections

- [Programming Languages and Object-Oriented Programming](../../02-programming-languages-object-oriented-programming/ROADMAP.md) connects boolean/null models, types, expressions, and evaluation.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies ordered trees, sorting, heaps, and lexicographic comparison.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) governs parameterization, allowlists, authorization, cursor integrity, and sensitive projection.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) owns response schemas, pagination contracts, limits, deadlines, and backward compatibility.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) provides plan evidence, query budgets, regression fixtures, and collation-upgrade controls.

## References

1. [PostgreSQL 18 Documentation, Table Expressions](https://www.postgresql.org/docs/18/queries-table-expressions.html)
2. [PostgreSQL 18 Documentation, Select Lists](https://www.postgresql.org/docs/18/queries-select-lists.html)
3. [PostgreSQL 18 Documentation, Sorting Rows](https://www.postgresql.org/docs/18/queries-order.html)
4. [PostgreSQL 18 Documentation, LIMIT and OFFSET](https://www.postgresql.org/docs/18/queries-limit.html)
5. [PostgreSQL 18 Documentation, SELECT](https://www.postgresql.org/docs/18/sql-select.html)
6. [SQLite Documentation, SELECT](https://www.sqlite.org/lang_select.html)
7. [MySQL 8.4 Reference Manual, SELECT Statement](https://dev.mysql.com/doc/refman/8.4/en/select.html)
8. [MySQL 8.4 Reference Manual, ORDER BY Optimization](https://dev.mysql.com/doc/refman/8.4/en/order-by-optimization.html)

## Exercises

### Exercise 1

Construct truth tables for a nullable `status` filter that should include `open` and null-as-unclassified but exclude `closed`. Compare two correct SQL formulations and their maintainability.

### Exercise 2

Given duplicated customer names and nullable scores, specify default bag projection, `DISTINCT` projection, and deterministic ordering. State which identities each result loses.

### Exercise 3

Design a keyset cursor for `priority DESC, due_at ASC NULLS LAST, id ASC`. Derive the continuation semantics and address collation, nulls, tampering, and versioning.

### Exercise 4

Compare offset, keyset, repeatable-snapshot, and materialized-result pagination for a frequently changing search result.

### Exercise 5

Design a correctness-and-performance evidence plan for a filtered, ordered, limited API query and a candidate covering index.

## Answers to the Exercises

### Answer 1

For status `open`, `status='open'` is true; for `closed`, false; for null, unknown. One expression is `status='open' OR status IS NULL`. Another is `status IS DISTINCT FROM 'closed'` where the selected dialect supports the intended null-safe comparison. The first is more portable and exposes the two included categories; the second is compact but dialect/operator knowledge matters. Test all three inputs and any other status. Do not use `NOT status='closed'`, because null becomes unknown and is filtered out.

### Answer 2

Default `SELECT name,score` preserves one output occurrence per selected source occurrence, so equal `(name,score)` tuples repeat. `SELECT DISTINCT name,score` retains one of each equal value tuple. Neither identifies customers after ID projection is removed; `DISTINCT` additionally removes multiplicity. Define `ORDER BY score DESC NULLS LAST,name ASC,id ASC`; ID must remain available as an order/tie key even if it is not displayed, subject to exposure policy. If consumers need entity identity, project ID rather than pretending names/scores are keys.

### Answer 3

The cursor carries priority, a due-null discriminator, due timestamp when present, and unique ID, plus filter/query version and collation/time-zone metadata. It is authenticated or server-stored. Continuation uses lexicographic “after”: lower priority; or equal priority and later due-null/order position; or equal priority/null class/due value and greater ID, with direction reversed where required. Implement using reviewed disjunctions or row comparison only if the dialect matches null and mixed-direction semantics. Reject expired/incompatible/tampered cursors and reapply authorization.

### Answer 4

Offset supports arbitrary page numbers but discards prefixes and shifts under inserts/deletes. Keyset uses the last total-order tuple and scales well with a matching index, but traverses sequentially and has documented live-mutation behavior. A repeatable snapshot stabilizes membership/order but retains transaction/version resources and is difficult across long stateless sessions. A materialized ID list gives explicit stable pages and random access but costs storage, build time, cleanup, authorization invalidation, and freshness. Select from result size, mutation, navigation, consistency, resource, privacy, and lifetime requirements.

### Answer 5

Freeze expected rows, multiplicities, values, types, null handling, collation, total order, and page boundaries using duplicates, ties, nulls, Unicode, range boundaries, rare/common parameters, and authorization cases. Record engine/schema/statistics/settings, plan, estimates/actuals, loops, buffers/I/O, memory/spill, rows examined/returned, bytes, first/last-row and end-to-end percentiles under warm/cold and concurrent load. Compare before/after the candidate index and measure insert/update/delete/log/storage amplification. Test cursor mutation/tampering, deadlines, cancellation, and client decoding. Adopt only if semantics remain equal and workload-wide objectives improve.
