---
module_id: DBE-016
program: Database Engineering
level: 1
module_number: 16
title: Set Operations
status: complete
last_verified: 2026-08-30
---

# Set Operations

## One-Page Review

### Governing question

How should compatible query results be combined, compared, and subtracted while preserving intended multiplicity, row identity, type meaning, provenance, and deterministic presentation?

### Essential definitions

Two query results are **union compatible** when they have the same column count and corresponding positions have compatible types under the target database. `UNION ALL` concatenates bags and adds multiplicities. `UNION`, `INTERSECT`, and `EXCEPT` default to duplicate elimination. Under multiset variants, `INTERSECT ALL` takes the minimum multiplicity and `EXCEPT ALL` takes truncated subtraction. **Row equality** for duplicate elimination compares the entire projected row under operation-specific null, type, and collation rules. **Provenance** records which source and version contributed an occurrence.

### Central model, mechanism, or theorem

Represent a query result as a bag with multiplicity `m_A(x)`. Then `m_(A UNION ALL B)(x)=m_A(x)+m_B(x)`, `m_(A INTERSECT ALL B)(x)=min(m_A(x),m_B(x))`, and `m_(A EXCEPT ALL B)(x)=max(m_A(x)-m_B(x),0)`. DISTINCT variants replace every positive resulting multiplicity by one. These equations prove counts only after both arms project the same domain attributes in the same positions with compatible equality semantics.

### Critical invariants

- Each arm declares the same output contract: position, name, type, unit, null meaning, collation, and grain.
- Columns align by position, not semantic name; every arm uses explicit projections and casts.
- `ALL` versus duplicate elimination is a domain decision, not a style preference.
- Duplicate equality is defined over the full projected row and is not ordinary predicate `=` with null.
- Mixed operators are parenthesized because precedence differs across dialects.
- Branch-local and compound-wide `ORDER BY`, `LIMIT`, and filtering scopes are explicit.
- Provenance and stable identity are retained before deduplication whenever audit or conflict resolution matters.
- Hash/sort duplicate elimination, memory, spill, skew, and estimates are verified on production-shaped data.

### Common failures

Failures include swapping same-typed columns between arms, trusting aliases to align values, silently widening or coercing types, using `UNION` to hide an accidental join duplicate, using `UNION ALL` when distinct entities are intended, discarding source provenance before conflict resolution, expecting input order to survive, mis-scoping `ORDER BY` or `LIMIT`, assuming all engines parse mixed operators identically, treating null duplicate equality like `NULL = NULL`, replacing `EXCEPT` with a null-unsafe anti-join, and underestimating the memory or spill cost of global deduplication.

### Compact example

Let left contain `a` twice, `b` once, and `c` once; right contain `a` once, `b` twice, and `d` once. `UNION ALL` has counts `a:3,b:3,c:1,d:1`; distinct union has one of each. `INTERSECT ALL` has `a:1,b:1`; `EXCEPT ALL` left-minus-right has `a:1,c:1`; distinct left-minus-right has only `c`. Direction matters: right-minus-left has only `d` under DISTINCT.

### Connections

[DBE-011](011-selection-projection-and-ordering.md) defines projection and result order. [DBE-012](012-joins-and-join-semantics.md) contrasts horizontal combination and semijoin/antijoin logic. [DBE-014](014-subqueries-and-common-table-expressions.md) provides explicit composition boundaries. [DBE-017](../ROADMAP.md) uses union in recursive evaluation. Data Engineering uses union and difference for ingestion, backfills, reconciliation, and change processing.

## Governing Question

Set operators combine relations vertically: each arm contributes rows to one shared output schema. The syntax is compact, but correctness depends on a structural contract that SQL cannot infer from business names. Two arms can each return two integers while placing `customer_id` and `region_id` in opposite positions; the statement may run and still corrupt the meaning of every row.

The second challenge is multiplicity. SQL query results are commonly bags, not mathematical sets. Duplicate elimination changes counts and can erase evidence that the same value arrived twice from one source or once from each of two sources. Retaining all occurrences can also double-count replicated data. The governing question therefore combines schema compatibility, domain identity, equality, multiplicity, provenance, operator grouping, and physical evidence.

## Why This Matters

Set operations appear in partitioned archives, event ingestion, federated reads, migrations, access-control comparisons, reconciliation, testing, cohort analysis, feature construction, and recursive queries. `UNION ALL` is often the correct way to append disjoint shards; `UNION` can mask overlap while making the query expensive. `EXCEPT` can identify missing keys between systems; projecting too few columns can conflate distinct versions, while projecting volatile metadata can prevent intended matches.

Schema drift is especially dangerous. If one branch changes a currency from integer minor units to decimal major units, type compatibility does not establish unit compatibility. A cast may make the query legal while producing false totals. If text arms use different normalization or collation assumptions, duplicate elimination may not match domain identity. A production contract must state more than “both queries have three columns.”

Set operations also create global work. Duplicate-eliminating union, intersection, and difference may hash or sort large results and spill to temporary storage. Skew and wide rows increase state. Branch predicates, partition pruning, parallel reads, and indexes affect cost, but pushing operations across branches is legal only when semantics are preserved. Plan success on a small fixture is not evidence of bounded production resources.

## Prerequisites and Retrieval

Retrieve sets, bags/multisets, tuples, functions, equivalence relations, null and three-valued logic, projection, types and casts, collation, keys, joins and anti-joins, grouping, subqueries, operator precedence, sorting/hashing, memory/spill, snapshots, and data provenance.

Distinguish column position from alias, type compatibility from domain compatibility, row equality from entity identity, duplicate values from replayed occurrences, `ALL` from DISTINCT, left-minus-right from right-minus-left, branch-local order/limit from compound-wide order/limit, and logical set equations from physical hash/sort implementation.

## Learning Objectives

After this module, you should be able to:

1. state and validate a union-compatible output contract;
2. derive DISTINCT and ALL multiplicities for union, intersection, and difference;
3. reason about nulls and full-row duplicate equality;
4. choose between preservation and elimination of duplicates from domain evidence;
5. parenthesize mixed set operations portably;
6. place branch-local and result-wide filtering, ordering, and limiting correctly;
7. compare `EXCEPT` with anti-join and `NOT EXISTS` formulations;
8. control type, collation, unit, and schema-evolution risks;
9. preserve provenance and reconcile source counts; and
10. inspect algorithms, estimates, memory, spill, parallelism, and incremental alternatives.

## Core Exposition

`UNION`, `INTERSECT`, and `EXCEPT` combine complete query results. Each arm must return the same number of columns. Corresponding columns are matched by ordinal position, not alias. The output names commonly derive from the first arm, but naming details and permissible references in final ordering are dialect-specific. Write explicit column lists in every arm; never use `SELECT *` across evolving schemas.

Union compatibility is syntactic and type-related, not semantic. `(account_id,amount)` and `(amount,account_id)` can both be integer pairs. Cast every arm toward a documented canonical output: entity key type, timestamp basis, numeric precision/scale, currency/unit, normalized text, null policy, and provenance fields. A successful implicit cast is evidence only that the engine found a conversion.

`UNION ALL` appends every occurrence. For row value `x`, its result multiplicity is the sum of multiplicities in both arms. This preserves duplicates and source volume, enables additive reconciliation, and usually avoids global duplicate elimination. It is appropriate for provably disjoint partitions or when occurrences themselves are meaningful. “Probably disjoint” is not proof; enforce or monitor the partition invariant.

`UNION` means duplicate-eliminating union (`UNION DISTINCT` where explicit syntax is accepted). It emits one occurrence of every distinct projected row appearing in either arm. It does not deduplicate by a selected business key unless the projection contains only that key, and doing so discards all non-key distinctions. It also does not choose a winning record among conflicting versions; define precedence and use an auditable row-selection design.

`INTERSECT` emits rows present in both arms, ordinarily once. `INTERSECT ALL` emits each row `min(m_A,m_B)` times where supported. Intersection is commutative at the logical bag level for compatible equality and snapshot assumptions. It is useful for comparing exact projections, but “present in both” says nothing about which system is authoritative or whether omitted attributes agree.

`EXCEPT` (called difference) emits distinct rows present on the left and absent on the right. `EXCEPT ALL` emits `max(m_A-m_B,0)` occurrences where supported. Difference is directional and not commutative. It is a powerful reconciliation primitive: `expected EXCEPT actual` finds missing distinct rows; `actual EXCEPT expected` finds unexpected rows. Run both directions and retain source counts when equality matters.

Under DISTINCT set operations, duplicates are compared as complete result rows under operation-specific rules. Null rows can be considered duplicates of other null rows even though ordinary predicate `NULL = NULL` evaluates unknown. PostgreSQL and SQLite document duplicate elimination behavior consistent with treating null values as not distinct for this purpose; exact type, collation, and composite comparison details must be checked per engine.

Full-row equality can be too broad or too narrow for business identity. Projecting `(customer_id,name)` treats a corrected name as a different row; projecting only `customer_id` hides the conflict. For reconciliation, first compare keys, then compare versioned payload hashes or canonical attributes, while retaining raw source evidence. Never let `UNION` decide a master-data merge policy implicitly.

`ALL` is not automatically more correct because it preserves information. If two arms read replicated copies of the same logical event, union-all double-counts it. Conversely, DISTINCT can collapse two legitimate equal-valued purchases. Establish occurrence identity: source event ID, ledger entry ID, immutable version, or another durable key. Record replay, correction, tombstone, and source-precedence rules.

Algebraic laws help review rewrites. Bag `UNION ALL` is associative and commutative in multiplicity, although output order remains unspecified. `INTERSECT ALL` is also associative and commutative through `min`. `EXCEPT ALL` is directional and generally neither commutative nor associative. DISTINCT union and intersection have the familiar set laws after applying the database's equality relation. Physical evaluation, errors, volatile expressions, types, and resource usage can still differ after algebraic regrouping.

Mixed operator precedence is not safely portable. PostgreSQL 18 and MySQL 8.4 document `INTERSECT` as binding more tightly than `UNION` and `EXCEPT`, while SQLite documents compound SELECT grouping from left to right. Thus `A UNION B INTERSECT C` can denote `A UNION (B INTERSECT C)` on one engine and `(A UNION B) INTERSECT C` on another. Parenthesize every mixed expression and add a fixture that distinguishes the two trees.

Even repeated operators benefit from parentheses when review intent matters. `A EXCEPT B EXCEPT C` is usually left-associated in documented dialects, meaning `(A EXCEPT B) EXCEPT C`, not `A EXCEPT (B EXCEPT C)`. The results differ. A CTE per named intermediate relation can improve auditability and give each boundary an explicit schema and row-count assertion.

Ordering belongs to the combined result unless a branch is explicitly parenthesized in syntax that permits branch-local `ORDER BY`/`LIMIT`. Input ordering is not preserved by set semantics. A final `ORDER BY` must define a total result order for deterministic output. Branch-local top-N changes which rows enter the operation; compound-wide top-N selects after combination. These are different queries, and syntax/alias rules vary.

Limiting without a total order is nondeterministic. Even with a branch order, an optimizer may discard ordering that has no semantic effect except through a bound. For “latest ten from each source, then merge,” parenthesize each source query with its own total order and limit, then apply an outer total order. Verify the target database supports the exact form and preserves the intended limiting semantics.

Types are resolved per output position according to dialect rules. PostgreSQL documents a pairwise resolution algorithm for nested unions; placement of unknown/null literals can affect success. Other engines have different coercion and affinity systems. Explicitly cast null literals and constants to the canonical type in every arm, especially for decimals, timestamps, enums/domains, JSON, binary/text, and identifiers.

Numeric compatibility does not preserve precision. Combining an exact decimal with floating input may select a result type or conversion that changes rounding and equality. Combining signed and unsigned ranges can overflow or coerce unexpectedly. Record bounds, precision, scale, unit, and comparison tolerance. Authority-sensitive reconciliation should canonicalize using an agreed exact representation before the set operation.

Text equality depends on type and collation rules. Unicode normalization, case folding, locale, trailing spaces, and binary versus linguistic comparison can change duplicate classes. Do not normalize away distinctions without a domain rule and versioned transformation. Include original source values and canonicalization version in evidence when deduplication has legal or financial effects.

Set operations and anti-joins can sometimes express related questions, but their multiplicity and null behavior differ. `A EXCEPT B` compares projected complete rows and deduplicates by default. `SELECT DISTINCT A.* FROM A WHERE NOT EXISTS (...)` can match it only with a corresponding null-safe equality contract. A left anti-join can multiply or misclassify rows if the join condition is incomplete or a nullable right marker is tested incorrectly.

Predicate pushdown can reduce branch volume when a predicate applies equivalently to every arm and references the canonical output semantics. A filter after union-all is often distributive over arms; casts, volatile expressions, outer joins, limits, security barriers, and errors can invalidate naive rewrites. Use the optimizer's plan plus semantic tests; do not duplicate authorization filters manually without ensuring every arm remains protected.

Provenance should be added before combination: source system, partition, extraction/as-of, schema version, event/version ID, and transformation version. Adding provenance makes otherwise equal payload rows distinct, so deduplicate on a deliberate key/payload layer and join provenance into an audit relation rather than assuming one projection serves both published output and evidence. Preserve occurrence counts before and after each boundary.

Reconciliation begins with invariants. For finite bags, `|A UNION ALL B|=|A|+|B|`. Per value, intersection-all plus left-except-all reconstructs left multiplicity: `min(a,b)+max(a-b,0)=a`. DISTINCT difference in both directions plus intersection partitions unique values. Validate source counts, distinct keys, null counts, per-key multiplicities, checksums/hashes with collision policy, and sampled/full payload comparisons.

Physical implementations commonly concatenate for union-all and hash or sort for duplicate-eliminating operators. Intersection and difference may use hashing, sorting/merge, or join-like strategies. Wide rows inflate keys and memory; high distinct cardinality increases state; skew affects partitioned/parallel work. Capture actual input/output rows, estimates, hash batches, sort method, memory, temporary I/O, worker distribution, and latency.

Pre-deduplicating each arm can reduce global work because duplicate elimination is idempotent for DISTINCT semantics, but it can obscure occurrence diagnostics and add redundant scans. Projecting narrower comparison keys reduces state but changes equality unless payload is reattached through a proven dependency. Partition-wise operations can scale when partition boundaries align and are disjoint; otherwise a final global reconciliation remains necessary.

Distributed systems add snapshot and retry risks. Two arms read at different as-of times can produce a difference caused by timing rather than data defect. Retried extraction can add occurrences under union-all. Capture source snapshots/watermarks, transaction isolation, manifests, idempotency keys, and completeness signals. Repeat a reconciliation only after defining whether late or corrected records are expected.

Security must apply to every arm before combination. A tenant predicate missing from one branch leaks rows even if the final projection hides tenant ID. Row-level security and view boundaries can behave differently across sources. Test authorized and unauthorized fixtures, inspect effective policies and roles, and preserve tenant identity through internal stages until isolation is proven.

Schema evolution requires compatibility gates. Adding a column to one `SELECT *` arm can fail immediately or, after simultaneous changes, shift meanings. Renaming does not alter positional alignment. Version canonical schemas, enumerate fields, cast deliberately, validate units and nullability, and make incompatible changes fail closed. Data contracts should compare both structural schema and semantic metadata.

Tests should include empty arms; only-left/only-right; identical distinct rows; unequal multiplicities; all-null and partially null rows; swapped same-typed columns; incompatible and lossy types; collation variants; wide rows; high cardinality; skew; branch errors; mixed precedence; limits; and snapshot drift. Independently compute multiplicity maps, then execute live dialect queries and compare sorted outputs. Successful parsing is only the beginning.

## Definitions and Notation

For finite bags `A` and `B` over compatible row domain `D`, let `a=m_A(x)` and `b=m_B(x)`:

- `m_(A union-all B)(x)=a+b`;
- `m_(A intersect-all B)(x)=min(a,b)`;
- `m_(A except-all B)(x)=max(a-b,0)`;
- `distinct(A)` has multiplicity one exactly where `a>0`;
- `A union B=distinct(A union-all B)`;
- `A intersect B=distinct(A intersect-all B)`;
- `A except B=distinct(A except-all B)` under the operation's row-equivalence rules.

These equations describe logical multiplicity, not output ordering, source authority, type resolution, or physical algorithms.

## Mechanisms, Invariants, or Proof Structure

A set-operation review should:

1. name each arm, source authority, snapshot, input grain, and expected overlap;
2. enumerate canonical output positions with types, units, null meanings, collations, and grain;
3. cast and alias every arm explicitly and reject `SELECT *`;
4. define row equality, entity identity, occurrence identity, provenance, and conflict policy;
5. choose DISTINCT or ALL from multiplicity equations and reconciliation goals;
6. parenthesize mixed operators and scope every filter, order, and limit;
7. derive per-value multiplicities including null and duplicate cases;
8. reconcile input/output counts, keys, payloads, and both difference directions;
9. test dialect type/coercion/collation behavior and security on every arm; and
10. inspect actual algorithms, estimates, memory, spill, skew, snapshots, retries, cancellation, and upgrades.

The finite model below uses explicit tuple bags to compute DISTINCT and ALL variants, including rows containing `None`. It defines equality through Python tuple keys solely for this bounded oracle; it is not a SQL type, null, collation, or optimizer model.

<!-- bijux-verify: {"id":"finite-set-operation-multiplicity","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"left_counts=((('a', 1), 2), (('b', 2), 1), (('c', None), 1), ((None, 3), 1))\nright_counts=((('a', 1), 1), (('b', 2), 2), (('d', 4), 1), ((None, 3), 1))\nunion_all=((('a', 1), 3), (('b', 2), 3), (('c', None), 1), (('d', 4), 1), ((None, 3), 2))\nunion_distinct=(('a', 1), ('b', 2), ('c', None), ('d', 4), (None, 3))\nintersect_all=((('a', 1), 1), (('b', 2), 1), ((None, 3), 1))\nexcept_all=((('a', 1), 1), (('c', None), 1))\nexcept_distinct=(('c', None),)\nreverse_except_distinct=(('d', 4),)\n","stderr":""}} -->
```python
from collections import Counter

left = (("a", 1), ("a", 1), ("b", 2), (None, 3), ("c", None))
right = (("a", 1), ("b", 2), ("b", 2), (None, 3), ("d", 4))


def row_key(row):
    return tuple((value is None, "" if value is None else str(value)) for value in row)


def ordered_counts(counter):
    return tuple(sorted(((row, count) for row, count in counter.items() if count), key=lambda item: row_key(item[0])))


left_counts = Counter(left)
right_counts = Counter(right)
union_all = left_counts + right_counts
intersect_all = left_counts & right_counts
except_all = left_counts - right_counts
union_distinct = tuple(sorted(set(left) | set(right), key=row_key))
except_distinct = tuple(sorted(set(left) - set(right), key=row_key))
reverse_except_distinct = tuple(sorted(set(right) - set(left), key=row_key))

print(f"left_counts={ordered_counts(left_counts)}")
print(f"right_counts={ordered_counts(right_counts)}")
print(f"union_all={ordered_counts(union_all)}")
print(f"union_distinct={union_distinct}")
print(f"intersect_all={ordered_counts(intersect_all)}")
print(f"except_all={ordered_counts(except_all)}")
print(f"except_distinct={except_distinct}")
print(f"reverse_except_distinct={reverse_except_distinct}")
```

Python `Counter`, set, tuple, string conversion, and `None` equality are not SQL bag, type, collation, ordering, or null semantics. The model omits schema/type resolution, implicit casts, NaN and composite values, provenance, snapshots, query plans, memory, spill, concurrency, and distributed execution.

## Alternatives and Trade-Offs

`UNION ALL` preserves occurrences and typically streams/concatenates efficiently, but overlapping or replayed sources can double-count. DISTINCT union publishes unique projected values at global deduplication cost and can erase provenance. A full outer join can expose side-by-side differences and counts but requires null-safe complete keys. Two directional `EXCEPT` queries are concise for exact canonical rows but do not explain mismatched attributes without further joins.

Hash-based duplicate elimination avoids ordering but consumes state and can spill or batch. Sort-based methods can merge ordered inputs and support deterministic diagnostics with an outer order, but sorting wide/high-volume rows is costly. Incremental materialized reconciliation reduces repeated work but adds watermark, correction, tombstone, idempotency, and rebuild contracts.

## Failure Modes and Misconceptions

- “Aliases align columns.” Set arms align by ordinal position.
- “Compatible types mean compatible meaning.” Units, identifiers, time zones, and authority can still differ.
- “SQL results are sets.” Query results commonly preserve duplicate occurrences until DISTINCT semantics are requested.
- “`UNION` is safer.” It can silently hide source overlap, replay, or join defects.
- “`UNION ALL` is always faster and therefore preferable.” It changes multiplicity and can corrupt downstream aggregates.
- “Null cannot equal null.” Duplicate-elimination equality is not ordinary predicate equality.
- “`EXCEPT` is an anti-join.” Projection, DISTINCT/ALL multiplicity, and null-safe equality must match.
- “Input order survives concatenation.” Only a final total `ORDER BY` guarantees output order.
- “Operator precedence is universal.” SQLite and PostgreSQL/MySQL document different grouping for mixed compounds.
- “A passing small query proves scale.” Global hashes/sorts may spill or fail under width, cardinality, skew, or concurrency.

## Worked Examples

### Example 1

Archive partitions are guaranteed disjoint by a checked date-range constraint and each row has immutable event ID. `UNION ALL` preserves every event and satisfies output count equal to the sum of partition counts. If ranges overlap after a configuration defect, that invariant must fail visibly rather than be hidden by DISTINCT.

### Example 2

One arm projects `(customer_id,region_id)` and another accidentally projects `(region_id,customer_id)`. Both columns are integers, so type checking may pass. Explicit canonical projections and fixture values with different ID ranges expose the positional corruption.

### Example 3

Left has three copies of `x`; right has two. `UNION ALL` yields five, `UNION` one, `INTERSECT ALL` two, `INTERSECT` one, `EXCEPT ALL` left-minus-right one, and `EXCEPT` none because `x` exists on the right. The DISTINCT difference is not the distinct form of the remaining count intuition.

### Example 4

Both arms contain `(NULL,'unknown')`. A DISTINCT compound can collapse them as duplicate rows even though `NULL = NULL` is unknown in a predicate. A `NOT EXISTS` rewrite must use the database's null-safe row equivalence if it is intended to reproduce the compound result.

### Example 5

`A UNION B INTERSECT C` is ambiguous across target dialects. PostgreSQL/MySQL interpret intersection first; SQLite documents left-to-right compound grouping. Write either `A UNION (B INTERSECT C)` or `(A UNION B) INTERSECT C`, and test values that make the results differ.

### Example 6

Source A reports dollars as decimal major units; source B reports integer cents. Casting both to decimal does not align units. Convert B with a versioned currency/unit rule, preserve originals, and reconcile totals before unioning canonical amounts.

### Example 7

To compare expected and actual permission tuples, compute both `expected EXCEPT actual` and `actual EXCEPT expected`. The first reveals missing grants; the second reveals excess grants. Preserve tenant, subject, resource, action, condition version, and policy snapshot in the comparison key.

### Example 8

“Latest five per source, then latest five overall” requires each parenthesized branch to have a total order and limit, followed by an outer total order and limit. A single trailing limit means latest five after the entire compound, not five from each arm.

### Example 9

Two sources publish the same business key with different names. Projecting only the key into `UNION` hides the conflict; projecting full payload produces two rows. Build a conflict relation keyed by entity, apply named source/version precedence, and retain both payloads and the decision evidence.

### Example 10

A billion-row DISTINCT union hashes wide JSON payloads and spills. A canonical payload digest plus key can reduce comparison width only with a collision and canonicalization contract; payload equality must still be verified for authority-sensitive discrepancies. Capture actual plan, batches, memory, temporary I/O, and skew.

## Cross-Program Connections

- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies sets, multisets, hash tables, sorting, and external-memory structures.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) analyzes union/intersection/difference algorithms and complexity.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) uses these operators for append, deduplication, CDC, backfills, and reconciliation.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) governs canonical schemas, grain, identity, lineage, and semantic compatibility.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) applies bidirectional difference to entitlement verification and requires isolation in every arm.

## References

1. PostgreSQL Global Development Group, [Combining Queries: UNION, INTERSECT, EXCEPT](https://www.postgresql.org/docs/18/queries-union.html), PostgreSQL 18 documentation.
2. PostgreSQL Global Development Group, [UNION, CASE, and Related Constructs](https://www.postgresql.org/docs/18/typeconv-union-case.html), PostgreSQL 18 type-resolution documentation.
3. PostgreSQL Global Development Group, [SELECT](https://www.postgresql.org/docs/18/sql-select.html), PostgreSQL 18 operator, multiplicity, ordering, and locking documentation.
4. PostgreSQL Global Development Group, [Type Conversion Overview](https://www.postgresql.org/docs/18/typeconv-overview.html), PostgreSQL 18 documentation.
5. SQLite Project, [SELECT: Compound Select Statements](https://www.sqlite.org/lang_select.html#compound), including duplicate, null, collation, ordering, and grouping rules.
6. Oracle, [Set Operations with UNION, INTERSECT, and EXCEPT](https://dev.mysql.com/doc/refman/8.4/en/set-operations.html), MySQL 8.4 Reference Manual.
7. Oracle, [Parenthesized Query Expressions](https://dev.mysql.com/doc/refman/8.4/en/parenthesized-query-expressions.html), MySQL 8.4 Reference Manual.
8. Oracle, [UNION Clause](https://dev.mysql.com/doc/refman/8.4/en/union.html), MySQL 8.4 Reference Manual.

## Exercises

### Exercise 1

Let `m_A(x)=5` and `m_B(x)=2`. Derive the multiplicity of `x` under union-all, distinct union, intersect-all, distinct intersection, left-except-all, distinct left-except, right-except-all, and distinct right-except.

### Exercise 2

Design a canonical output contract for unioning payments from a decimal-euro system and an integer-cent system. Include positions, types, units, timestamps, nulls, identifiers, provenance, and compatibility gates.

### Exercise 3

Give finite sets `A`, `B`, and `C` for which `A UNION (B INTERSECT C)` differs from `(A UNION B) INTERSECT C`. Explain why explicit parentheses are required in a multi-dialect repository.

### Exercise 4

Compare `A EXCEPT B` with a `NOT EXISTS` rewrite when rows contain nulls and duplicates. State the equality, projection, and multiplicity requirements for equivalence.

### Exercise 5

Create a production evidence plan for reconciling two 500-million-row datasets. Include snapshots, canonicalization, bidirectional differences, occurrence counts, provenance, type/collation tests, plan/resource evidence, retries, security, cancellation, and upgrades.

## Answers to the Exercises

### Answer 1

Union-all has 7; distinct union has 1; intersect-all has `min(5,2)=2`; distinct intersection has 1; left-except-all has `max(5-2,0)=3`; distinct left-except has 0 because `x` exists in B; right-except-all has 0; distinct right-except has 0. DISTINCT difference tests presence, not leftover multiplicity.

### Answer 2

Define `(payment_id text, source text, amount_eur decimal(p,s), occurred_at_utc timestamp-with-zone canonical form, customer_id canonical type, source_version text)`. Convert cents by exact division by 100 under a versioned currency rule, reject unknown currencies or out-of-range precision, define nullability and timestamp source/time-zone conversion, and retain original amount/unit/time. Validate positional schemas, casts, ranges, uniqueness, source snapshots, and additive totals before combination.

### Answer 3

Take `A={1}`, `B={2}`, and `C={2}`. `A UNION (B INTERSECT C)={1,2}`, while `(A UNION B) INTERSECT C={2}`. PostgreSQL/MySQL documented precedence chooses the first tree for the unparenthesized expression; SQLite's documented left-to-right grouping chooses the second. Parentheses make intent portable and reviewable.

### Answer 4

`A EXCEPT B` compares the full projected row and removes duplicates by default. A rewrite must match every projected column using the dialect's null-safe “not distinct” equivalence, then apply DISTINCT to surviving A rows. Without DISTINCT it preserves left duplicates; with ordinary `=` it may fail to match nulls; with fewer comparison columns it changes identity. `EXCEPT ALL` additionally requires per-row multiplicity subtraction and is not reproduced by a simple existential predicate.

### Answer 5

Capture transaction snapshots or compatible watermarks and extraction manifests for both sides. Version canonical types, units, time, text normalization/collation, null rules, and payload digest; retain raw provenance. Reconcile total and per-key multiplicities, null counts, distinct keys, intersection, and both differences, verifying digest discrepancies against payloads. On production-shaped data capture actual algorithms, estimates, memory, spill, I/O, skew, concurrency, latency, and cancellation; make retries idempotent, test tenant/role isolation in both arms, and rerun semantic plus resource thresholds for engine/schema/configuration upgrades.
