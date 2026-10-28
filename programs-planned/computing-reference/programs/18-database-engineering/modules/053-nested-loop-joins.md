---
module_id: DBE-053
program: Database Engineering
level: 2
module_number: 53
title: Nested-Loop Joins
status: complete
last_verified: 2026-08-30
---

# Nested-Loop Joins

## One-Page Review

### Governing question

How can a join executor repeatedly evaluate an inner access path for outer rows or blocks while preserving bag, null, outer/semi/anti, parameter, order, visibility, and failure semantics—and when is that repetition economical?

### Essential definitions

A **nested-loop join** obtains an outer item and evaluates an inner plan against it, emitting combinations that satisfy the join condition. A **tuple nested loop** compares each outer row with an inner scan. A **block/page nested loop** retains several outer rows and scans/batches the inner side to amortize I/O. An **index nested loop** parameterizes an inner index lookup with outer values. A **parameterized path** depends on values supplied by an ancestor. **Batched key access** groups several outer lookup keys so the storage engine can improve locality. **Memoization** caches inner results by parameter key. The **outer** and **inner** roles are physical roles, not necessarily SQL textual left/right roles; for an outer join, logical preserved/null-supplying roles still constrain legal transformations.

### Central model, mechanism, or theorem

Nested loops are correlation made physical. For every outer row (o), bind its parameter environment, obtain exactly the inner rows (i) visible to the statement for which the join predicate is TRUE, and emit according to join kind. The cost is outer production plus the sum of inner evaluation costs—not merely “quadratic.” Indexing, batching, caching, early stop, outer cardinality, parameter skew, and repeated-key locality determine that sum. Correctness requires a fresh logical inner evaluation per binding even when physical state/results are safely reused.

### Critical invariants

- Every qualifying pair appears with bag multiplicity equal to the product of participating multiplicities.
- SQL equality with NULL is UNKNOWN, not a match; null-safe operators require their own semantics.
- Left/right/full outer joins emit a null-extended row exactly when the preserved row has no TRUE match.
- Semi joins emit each qualifying outer row once; anti joins emit it only when no TRUE match exists.
- Inner rescans receive the current complete parameter binding and do not leak state from a prior outer row.
- Memo/batch keys include every value, type, collation, snapshot, authorization, and effect dimension needed for equivalence.
- Residual predicates, visibility, locking, and rechecks remain enforced on inner candidates.
- Ordering and early-stop claims are derived from outer/inner properties and parent demand, never loop syntax alone.

### Common failures

Failures include calling every nested loop quadratic; choosing a large outer side with a full inner rescan; underestimating outer rows and multiplying a cheap-looking inner node millions of times; dropping duplicate matches; equating NULLs; emitting an outer null row before proving no match; using `LIMIT 1` where all matches are required; caching a volatile, snapshot-dependent, or incompletely keyed inner result; overlooking per-loop metrics; assuming SQL order fixes physical outer/inner orientation; batching while losing correspondence between keys and outer duplicates; and forcing hash/merge when correlation or non-equality predicates make nested loops appropriate.

### Compact example

Two duplicate outer rows with key 1 and two inner rows with key 1 produce four inner-join rows, not two. A second outer key 2 produces one row, while a NULL key produces no equality match and becomes one null-extended row under a left join. A simple loop performs 16 comparisons for four-by-four inputs; a parameterized lookup probes three non-null outer rows; memoizing repeated key 1 reduces distinct probes to two. Finite equality evidence does not prove arbitrary SQL types, effects, concurrency, or engine implementations.

### Connections

Retrieve [Joins and Join Semantics](012-joins-and-join-semantics.md), [Composite and Covering Indexes](035-composite-and-covering-indexes.md), [Snapshot Visibility](047-snapshot-visibility.md), [Logical and Physical Plans](051-logical-and-physical-plans.md), and [Sequential and Index Scans](052-sequential-and-index-scans.md). Continue through the Database Engineering [roadmap](../ROADMAP.md) to hash and sort-merge joins.

## Governing Question

What proof and cost structure lets tuple, block, indexed, batched, and memoized nested loops implement relational joins correctly across cardinality, parameter, and concurrency regimes?

## Why This Matters

Nested loops are the most general join family. They need only a way to enumerate an outer input, evaluate an inner input under a binding, and test a predicate. They can implement equality and non-equality joins, spatial/range predicates, parameterized `LATERAL` expressions, correlated subqueries that were not decorrelated, and tiny joins. An index nested loop can deliver the first answer with little startup and excel when the outer side is small and the inner lookup is selective.

The same generality creates a multiplicative failure mode. An inner node estimated at one small lookup may run once for every actual outer row. If outer cardinality is underestimated from 100 to one million, one million probes, remote calls, or scans replace the planned 100. Per-loop explain time and rows can appear harmless until multiplied. Skew means one parameter may return thousands of inner rows while most return zero; repeated keys can either waste probes or create memoization opportunity.

Nested loops also expose semantic details hidden by the phrase “for each row.” SQL uses bags: duplicates on both sides multiply. Join predicates retain only TRUE, so ordinary equality does not match NULL to NULL. Outer joins need a match flag per preserved row; semi/anti joins need existence logic rather than pair emission. Parameterized inner expressions may raise errors, observe volatile functions, or access protected data. Reusing results is correct only when all observable dependencies are part of the cache identity and reuse is allowed.

For engine builders and practitioners, the lesson is to reason in three layers: logical join semantics, physical rescan/batch/cache mechanism, and measured workload. A nested loop is neither primitive embarrassment nor universal fast path. It is a precise execution strategy whose value depends on outer cardinality, inner access, locality, result fanout, startup needs, order, memory, and legal parameterization.

## Prerequisites and Retrieval

You should understand SQL inner/outer/semi/anti joins, bags and three-valued logic, iterators, pages/buffers, indexes and sargability, snapshots and locks, cardinality/selectivity, physical properties, and cost estimates versus runtime measurements. Retrieve outer input, inner input, parameter slot, rescan, join qualification, other/residual qualification, matched flag, null extension, early stop, materialization, memo key, cache hit/eviction, batch, fanout, startup/total cost, loops, and parameter skew.

DBE-052 established scan/access contracts. A nested loop composes them: the inner scan may be sequential, indexed, bitmap, remote, materialized, or another operator tree. DBE-054 and DBE-055 will trade parameterization/general predicates for hash or order-based bulk processing.

## Learning Objectives

After this module, you can:

1. derive inner, left outer, semi, and anti nested-loop algorithms from SQL bag/null semantics;
2. prove tuple-loop correctness using per-outer-row invariants and match-state transitions;
3. derive tuple, page/block, indexed, batched, materialized, and memoized cost models;
4. choose physical outer and inner roles under join-kind, parameterization, order, and cardinality constraints;
5. distinguish join qualification from residual filtering and null extension;
6. reason about composite parameter keys, null-safe comparisons, collation, volatility, and cache validity;
7. diagnose multiplicative work using actual rows, loops, searches, fanout, buffers, and waits;
8. explain batching/locality gains without confusing them with hash-join semantics;
9. test joins adversarially across duplicates, nulls, skew, empty inputs, versions, cancellation, and faults; and
10. design production controls for plan sensitivity, remote inner access, memory, and retry behavior.

## Core Exposition

**Start from logical bags.** Let outer bag (O), inner bag (I), and predicate θ(o,i) returning TRUE, FALSE, or UNKNOWN. The inner join contains one concatenated row for every pair occurrence in (O × I) where θ is TRUE. If an outer value occurs (m) times and a matching inner value occurs (n) times, the pair contributes (mn) rows. Algorithmic de-duplication is incorrect unless a logical distinct/semi operation requires it.

For a left outer join, process the same TRUE pairs but retain a `matched` bit for each outer occurrence. If no inner row made the join qualification TRUE, emit that outer occurrence once with a null-extended inner schema. UNKNOWN does not set `matched`. A post-join residual/WHERE filter may later remove the null-extended row; it must not be moved into join qualification without an equivalence proof.

A left semi join emits an outer occurrence once after finding its first TRUE match; additional inner matches do not add rows. A left anti join emits the outer occurrence only after the inner search is exhausted with no TRUE match. `NOT EXISTS` follows existence semantics, whereas `NOT IN` with NULL has distinct three-valued behavior and cannot be substituted casually.

**The iterator state machine is small but exacting.** Initialize outer and inner children. Fetch an outer row. Bind every inner parameter derived from it. Reset/rescan or initialize the inner path in a state equivalent to a fresh evaluation for that binding. Fetch inner rows, check join qualification, update match state, apply any post-join qualification, and emit as the join kind permits. When the inner exhausts, emit null extension or anti result if required, then advance the outer. On exhaustion or error/cancellation, release both child states and owned resources.

“Equivalent to fresh evaluation” permits safe physical reuse: retain an open index, rewind a materialized inner relation, reuse compiled expressions, batch probes, or return a memo entry. It forbids stale parameter slots, leftover cursor position, missed visibility/lock checks, cross-tenant cache leakage, and reuse across volatile or side-effecting evaluations whose semantics require repetition.

**Tuple nested loop is the baseline proof, not always the implementation.** With no useful inner access, compare every outer occurrence with every inner occurrence. CPU predicate evaluations are |O||I|. If the inner is rescanned from storage for every outer row, I/O can be disastrous. But if one side has a single row, the inner is tiny/in memory, or the predicate is arbitrary, it can be reasonable and provides a correctness oracle for optimized variants.

At page granularity, choosing the smaller input as physical outer reduces repeated scans when semantics permit. A simple page nested loop with (B_O) outer pages and (B_I) inner pages costs approximately (B_O + B_O B_I) page reads without cache reuse. With (M-2) pages available for an outer block, block nested loop costs approximately (B_O + ⌈B_O/(M-2)⌉B_I). The formulas omit buffer-cache survival, prefetch, output CPU, predicates, and concurrent interference; they explain why larger blocks amortize inner passes.

**Index nested loop makes the inner path parameterized.** For each outer row, derive a probe or range such as `inner.tenant_id = outer.tenant_id AND inner.key = outer.key`. The cost is


(C_{INLJ}=C_O+∑_{o∈O}(C_{probe}(key(o))+C_{matches/recheck}(o))).


This is not necessarily quadratic. A balanced lookup can be logarithmic plus matches, and cached upper index pages can make navigation cheap. Yet the sum includes outer multiplicity: duplicate outer keys repeat probes unless safely cached/batched, broad ranges create large fanout, and scattered heap fetches multiply random access. A covering lookup may avoid base fetches only under the visibility rules from DBE-052.

The physical outer should usually be the smaller or more selective stream when the inner supports selective parameterized lookup. “Usually” matters. A preserved side, `LATERAL` dependency, requested order, early limit, available indexes, and parameter availability can constrain orientation. SQL `FROM A JOIN B` does not force A to be physical outer for an inner join; outer-join transformations require null-preservation proofs.

**Parameterized paths make correlation explicit.** An inner plan may refer to one or several outer columns. PostgreSQL's current `LATERAL` documentation describes evaluating a lateral item for each row or row set providing cross-referenced values, then joining the result. Physical planners can sometimes decorrelate this into a bulk join; otherwise nested-loop parameterization directly implements the dependence.

Parameter identity includes value and semantic metadata. Composite keys need all components and their null/type/collation meaning. Security or tenant scope cannot remain implicit. If the inner result depends on snapshot, role/policy, configuration, time, random state, sequence, external service state, or side effects, caching may be invalid or require those dimensions and explicit freshness semantics.

**Materialization, memoization, and batching attack different repetition.** Materialization evaluates an unparameterized inner plan once and rewinds stored results; it exchanges memory/temp I/O and startup for eliminating repeated computation. Memoization stores results for previously seen parameter keys; it excels when the outer has locality or few distinct keys, but may thrash when keys are mostly unique or results are huge. Eviction changes performance, not semantics, provided misses recompute correctly and entries are valid.

Batched key access collects a block of outer rows or keys, submits grouped inner lookups, and maps each returned inner row back to every corresponding outer occurrence. Sorting requests by physical locator can improve locality; network storage can amortize round trips. It remains nested-loop-like parameterized lookup, not automatically a hash join. The implementation must preserve duplicate outer associations, per-key no-match state, outer/semi/anti semantics, and any required ordering—or add a reorder mechanism with bounded state.

The executable below independently implements ordinary nested loop and indexed lookup over a finite equality dataset. SQL-style equality returns false for NULL comparison. It demonstrates bag multiplication, left null extension, semi/anti existence, comparison/probe counts, and memo reuse. It omits SQL types/collations, MVCC, locks, effects, faults, memory limits, and real index/storage behavior.

<!-- bijux-verify: {"id":"nested-loop-bag-semantics","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"inner_rows=(('A', 'x'), ('A', 'y'), ('A', 'x'), ('A', 'y'), ('B', 'z'))\nleft_rows=(('A', 'x'), ('A', 'y'), ('A', 'x'), ('A', 'y'), ('B', 'z'), ('N', None))\nsemi_rows=('A', 'A', 'B')\nanti_rows=('N',)\nnaive_comparisons=16\nnon_null_index_probes=3\ndistinct_memo_probes=2\nindexed_equals_naive=True\nevidence=finite_bag_and_probe_model\n","stderr":""}} -->
```python
outer = (("A", 1), ("A", 1), ("B", 2), ("N", None))
inner = (("x", 1), ("y", 1), ("z", 2), ("null", None))


def sql_equal(left, right):
    return left is not None and right is not None and left == right


def matches_for(outer_row):
    return tuple(row for row in inner if sql_equal(outer_row[1], row[1]))


naive = tuple(
    (outer_name, inner_name)
    for outer_name, outer_key in outer
    for inner_name, inner_key in inner
    if sql_equal(outer_key, inner_key)
)

left = tuple(
    (outer_name, inner_name)
    for outer_name, outer_key in outer
    for inner_name in ([row[0] for row in matches_for((outer_name, outer_key))] or [None])
)

index = {}
for inner_name, inner_key in inner:
    if inner_key is not None:
        index.setdefault(inner_key, []).append(inner_name)

indexed = tuple(
    (outer_name, inner_name)
    for outer_name, outer_key in outer
    for inner_name in index.get(outer_key, ())
)
semi = tuple(name for name, key in outer if index.get(key))
anti = tuple(name for name, key in outer if not index.get(key))

print(f"inner_rows={naive}")
print(f"left_rows={left}")
print(f"semi_rows={semi}")
print(f"anti_rows={anti}")
print(f"naive_comparisons={len(outer) * len(inner)}")
print(f"non_null_index_probes={sum(key is not None for _, key in outer)}")
print(f"distinct_memo_probes={len({key for _, key in outer if key is not None})}")
print(f"indexed_equals_naive={indexed == naive}")
print("evidence=finite_bag_and_probe_model")
```

**Outer/semi/anti state is a correctness boundary.** For left outer join, a match flag is associated with an outer occurrence, not merely its key; duplicates remain separate. If batching reorders work, the engine retains identity for each buffered outer row. A residual predicate that is logically above the outer join is applied after null extension. For semi join, the inner can stop on the first TRUE match. For anti join, it can stop on the first TRUE match and suppress the outer row; otherwise it must prove exhaustion. Exception, cancellation, or timeout is not “no match.”

**Ordering and startup can make nested loops globally useful.** A streaming outer and parameterized inner can emit early without building a whole hash table or sorting both inputs. If the outer delivers required leading order and each inner lookup returns rows in a compatible suffix order, the nested loop may deliver composite order. But concatenating ordered inner runs does not create global order unless outer key progression and comparator semantics prove it. Batched/asynchronous probes can reorder completion and need an order-restoration buffer if the parent requires order.

`LIMIT` can reduce work only through parent demand and semantics. An inner/semi lookup may stop after one match; an inner join cannot discard additional matches merely because one was found. A top-level limit can stop the entire pipeline after enough ordered or arbitrary results as allowed, but estimates shown for child completion may exceed observed rows. Offset pagination can still force many loops; keyset predicates plus compatible indexes often bound work better.

**Cardinality errors multiply.** Estimate outer rows, distinct parameter keys, per-key match distribution, unmatched fraction, inner lookup startup, base-page locality, cache/memo hit rate, and residual selectivity. Averages hide heavy hitters: 99% of keys may return zero or one row while one key returns millions. Multi-column correlation and tenant skew matter. The optimizer must also compare planning alternatives without pruning the only feasible parameterized path.

Read plans from the pipeline outward. Record outer actual rows, inner actual rows per loop, loop count, index searches, rows removed by index/filter/recheck, memo hits/misses/evictions/overflows where exposed, materialization/spill, buffers/bytes, remote requests, waits, time to first/last row, and output cardinality. PostgreSQL's current EXPLAIN documentation shows nested-loop inner nodes executing once per outer row and notes that actual time/rows are per execution averages; total interpretation needs loops.

**Concurrency and failures remain visible.** All child accesses must observe the statement/transaction semantics. Repeated probes can enlarge lock/predicate footprints and transaction duration. Under read committed semantics in some systems, statement snapshots or rechecks are engine-defined; do not assume each rescan sees arbitrary new state. For DML, target rows may need requalification after locking, and duplicate join matches must not cause unintended repeated modification.

Remote parameterized loops deserve special suspicion: one request per outer row creates latency multiplication, rate-limit pressure, partial failure, and ambiguous retries. Batch with bounded size where semantics permit; attach request/result identity; enforce deadlines and cancellation; make retries idempotent or reconcile them. A failed inner evaluation cannot be cached as an empty successful result unless the source contract explicitly defines that outcome.

**Verification combines oracle comparison and workload envelopes.** Compare every optimized nested-loop form with a simple tuple-loop oracle on generated bags containing empty inputs, duplicates, nulls, unmatched and many-to-many keys, skew, composite/collated keys, non-equality predicates, and errors. Test all join kinds separately. Add snapshot/update/delete schedules, concurrent index changes, cancellation at each state transition, memory pressure/eviction/spill, and fault injection for remote or storage reads.

Performance experiments sweep outer cardinality, distinct parameter count, match fanout, ordering, index coverage/clustering, cache state, batch/memo capacity, row width, concurrency, and latency. Validate results before timing. Gate p50/p95/p99, probes/requests, bytes/pages, CPU, memory/temp, locks/aborts, and write/index maintenance. A plan hint is a reversible, parameter-scoped mitigation with expiry—not proof that the estimator, statistics, or schema is correct.

## Definitions and Notation

- (O,I): outer and inner input bags; an occurrence is preserved independently of equal-valued occurrences.
- θ(o,i): three-valued join qualification; only TRUE forms a match.
- |O|, |I|: tuple occurrence counts; (B_O,B_I): physical page counts.
- **Physical outer/inner**: driver and repeatedly evaluated roles in the implementation.
- **Preserved/null-supplying side**: logical outer-join roles; not interchangeable without proof.
- **Parameter binding**: environment of outer-derived values supplied to an inner plan.
- **Rescan**: returning a child to semantics equivalent to a fresh evaluation under current parameters.
- **Fanout**: inner match count for one outer occurrence or parameter key.
- **Match flag**: per-outer-occurrence state recording at least one TRUE join qualification.
- **Materialize**: store one child result for rewind/reuse.
- **Memoize**: cache inner result by complete parameter identity.
- **Batch/BKA**: group parameter lookups while retaining association with outer occurrences.
- (M): page budget in the simplified block-loop model.
- **Loops**: runtime executions of a plan node; per-loop rows/time require aggregation for total work.

## Mechanisms, Invariants, or Proof Structure

For inner join, maintain invariant: before fetching outer occurrence (o_k), output contains exactly all TRUE pairs for prior outer occurrences; while scanning inner prefix (I_j), it additionally contains exactly TRUE pairs ((o_k,i_1...i_j)). Exhaustion establishes all pairs for (o_k); outer exhaustion establishes the bag join.

For left outer join, add `matched=false` at each new outer occurrence; set it only on TRUE join qualification. After inner exhaustion, emit one null-extended row iff false. For semi join, first TRUE permits one emission and safe early stop. For anti join, first TRUE permits suppression/stop; exhaustion with false permits one emission. Prove batching/memoization simulates these transitions for each outer occurrence and preserves errors/effects/order required by context.

Cost proof is conditional: expand total inner work as a sum over actual outer occurrences or distinct cached/batched parameters, then add output, recheck, and resource terms. Big-O alone cannot choose orientation or predict latency. Legal transformation and result proof precede estimates; empirical evidence calibrates the cost inputs.

## Alternatives and Trade-Offs

Tuple nested loop is general and low-memory but repeats comparisons/scans. Block/page loops use bounded memory to amortize inner passes. Index nested loops provide selective, streaming parameter access but multiply probes and random fetches. Materialized loops remove repeated uncorrelated computation at startup/memory/temp cost. Memoized loops exploit repeated parameters but require correct keys, valid effects/snapshots, and capacity. Batched access improves storage/network locality while adding latency, association, order, and memory complexity. Hash join offers bulk equality matching with build memory/spill and weak parameterization; merge join exploits ordered inputs and ranges but may sort. Adaptive operators can switch only with state-transfer and duplicate/match correctness proofs.

Choose with join kind/predicate, outer cardinality/order, inner access, fanout/skew, distinct parameters, startup versus completion, memory/spill, cache/storage/remote locality, concurrency, and observability. No algorithm label replaces the workload-bound comparison.

## Failure Modes and Misconceptions

1. **“Nested loops are always (O(n^2)).”** Actual work is a sum of inner costs; indexes, unequal sizes, early stop, caching, and batching change it.
2. **“SQL left table is the physical outer.”** Inner joins can reorder; outer/correlated joins impose semantic constraints, not textual folklore.
3. **“One inner row estimate means one inner execution.”** The node can run once per outer row; multiply rows/time/searches by loops.
4. **“Duplicate parameters may be deduplicated.”** Cache probes, not outer occurrences or required output multiplicity.
5. **“NULL equals NULL in an equality join.”** Ordinary SQL equality is UNKNOWN; null-safe operators are distinct.
6. **“No row yet means outer no-match.”** Null extension/anti emission requires inner exhaustion, not delay or failure.
7. **“First match ends every join.”** It ends semi/existence search, not an inner/outer join that must emit all matching pairs.
8. **“Memoization is always safe.”** Volatility, side effects, snapshot/security dimensions, incomplete keys, and errors can invalidate reuse.
9. **“Batching is just a hash join.”** It batches parameterized requests and must map results back to outer occurrences.
10. **“Ordered inputs make ordered output automatically.”** Concatenated inner runs need a compositional order proof; async batching can reorder.
11. **“A tiny per-loop time is harmless.”** Millions of loops and remote round trips dominate totals and tails.
12. **“Forcing another join fixes the root cause.”** Cardinality, sargability, skew, missing access paths, or correlation may remain.

## Worked Examples

### Example 1

Outer bag has key 7 twice; inner bag has key 7 three times. Tuple nested loop evaluates six TRUE occurrence pairs and emits six rows. Deduplicating the probe key is allowed only if cached results are replayed for both outer occurrences. Conclusion: bag multiplicity is (2×3=6), independent of probe reuse.

### Example 2

Outer key NULL and inner key NULL use ordinary equality. The predicate is UNKNOWN, so inner join emits none; left join emits one null-extended outer row after exhaustion. With a defined null-safe comparator, behavior can differ. Conclusion: comparator semantics control match state.

### Example 3

Ten outer rows drive a full scan of a 1,000-page inner relation: roughly 10,000 repeated inner page visits beyond the outer. Buffering all ten outer rows and scanning inner once reduces the modeled inner passes to one. Conclusion: block loops trade bounded memory for pass amortization.

### Example 4

One hundred selected customers probe a covering orders index and average two rows each. Index nested loop starts quickly and avoids scanning all orders. At one million customers with scattered matches, probe/base-fetch multiplication reverses the choice. Conclusion: bind the plan to outer size, fanout, coverage, and locality.

### Example 5

A lateral subquery requests each customer's newest three orders using a `(customer_id, occurred_at DESC, id DESC)` index. Per-customer parameterization and early stop implement the requirement directly. A global rewrite must preserve three-per-customer grouping and ties. Conclusion: correlation plus bounded ordered lookup is a natural nested-loop use.

### Example 6

Outer keys repeat in long runs: A 50,000 times, B 30,000, C 20,000. Memoizing three complete inner results removes 99,997 probes but must replay results for every outer occurrence. If each result is huge, cache memory/output still dominate. Conclusion: distinct parameters and result size jointly determine memo value.

### Example 7

An anti join checks whether any prohibited event exists. The first TRUE match safely suppresses that outer row. A timeout on the inner service is not proof of absence and must fail/retry according to policy. Conclusion: exhaustion is logical evidence; operational failure is not.

### Example 8

Estimated outer rows 20 become 500,000. The inner index node reports 0.2 ms and one row per loop, implying about 100 seconds plus other work when multiplied. A hash alternative estimated too expensive would have built once. Conclusion: reconcile estimates, loops, total probes, and parameter skew.

### Example 9

Batched remote keys return out of request order. A left join must attach every match/no-match result to the correct buffered outer occurrence and reproduce duplicates; ordered output requires sequence IDs and bounded restoration. Conclusion: locality/latency batching adds association and order obligations.

### Example 10

A cache key contains account ID but omits tenant ID because accounts were once global. After schema evolution, equal account numbers across tenants reuse another tenant's inner rows. Conclusion: memo keys must encode the complete semantic/security parameter environment and be invalidated across incompatible evolution.

## Cross-Program Connections

- [Programming Languages and Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) supplies environments, substitution, effects, evaluation order, and observational equivalence.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies nested sums, amortization, cache models, skew analysis, and adversarial benchmarking.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies indexes, hash maps for memo tables, buffers, locality, and eviction policies.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies page caching, asynchronous I/O, scheduling, cancellation, and resource cleanup.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies batching, RPC fanout, deadlines, retries, idempotency, and partial failure.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies tenant isolation, authorization context, cache-key separation, and side-channel review.

## References

1. PostgreSQL Global Development Group, [Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html), PostgreSQL 18 current documentation, retrieved 2026-08-30; nested-loop plans, inner loops, per-execution actuals, index searches, and memoization evidence.
2. PostgreSQL Global Development Group, [Controlling the Planner with Explicit JOIN Clauses](https://www.postgresql.org/docs/current/explicit-joins.html), PostgreSQL 18 current documentation, retrieved 2026-08-30; legal join order, outer/full join constraints, and planning-search controls.
3. PostgreSQL Global Development Group, [Query Planning Configuration](https://www.postgresql.org/docs/current/runtime-config-query.html), PostgreSQL 18 current documentation, retrieved 2026-08-30; nested-loop and memoize planner controls and diagnostic caution.
4. PostgreSQL Global Development Group, [Table Expressions: LATERAL Subqueries](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-LATERAL), PostgreSQL 18 current documentation, retrieved 2026-08-30; per-source-row parameterized evaluation and left-lateral use.
5. PostgreSQL Global Development Group, [`nodeNestloop.c`](https://github.com/postgres/postgres/blob/REL_18_STABLE/src/backend/executor/nodeNestloop.c), PostgreSQL 18 stable source, retrieved 2026-08-30; executor outer/inner state, parameter propagation, rescans, join qualification, and outer-row handling.
6. SQLite Project, [Query Planning](https://www.sqlite.org/queryplanner.html), current official documentation, retrieved 2026-08-30; nested index searches, statistics, and multi-term lookup planning.
7. Oracle, [Nested-Loop Join Algorithms](https://dev.mysql.com/doc/refman/8.4/en/nested-loop-joins.html), MySQL 8.4 Reference Manual, retrieved 2026-08-30; nested-loop execution structure.
8. Oracle, [Block Nested-Loop and Batched Key Access Joins](https://dev.mysql.com/doc/refman/8.4/en/bnl-bka-optimization.html), MySQL 8.4 Reference Manual, retrieved 2026-08-30; join buffers, outer/semi handling, batched keys, and storage-engine cooperation.
9. Goetz Graefe, [“Query Evaluation Techniques for Large Databases”](https://web.stanford.edu/class/cs346/2014/graefe.pdf), *ACM Computing Surveys* 25(2), 1993; nested-loop variants, physical join trade-offs, and iterator execution.
10. Andy Pavlo, [“Joins Algorithms”](https://15445.courses.cs.cmu.edu/fall2023/slides/11-joins.pdf), CMU 15-445/645 lecture notes, Fall 2023; tuple/page/block/index nested-loop cost derivations and join algorithm comparison.

## Exercises

### Exercise 1

Trace inner, left outer, semi, and anti nested loops for outer bag `[1,1,NULL,3]` and inner bag `[1,1,NULL,2]` under ordinary SQL equality. Give outputs and match-state transitions.

### Exercise 2

Derive tuple, page, block, and index nested-loop work for an outer of 600 pages/60,000 rows, inner of 20,000 pages, 102 buffer pages, and a parameterized index lookup averaging four index/base page touches plus two matches. State omitted assumptions.

### Exercise 3

Design a correct memoized parameterized join executor. Specify cache identity, null/error/effect behavior, eviction, snapshot/security validity, duplicate replay, outer/semi/anti handling, ordering, and cancellation cleanup.

### Exercise 4

Diagnose a production nested-loop regression with 100 estimated versus 8 million actual outer rows, 70% repeated keys, remote inner access, and p99 timeouts. Propose evidence, immediate controls, and durable remedies.

### Exercise 5

Design a join strategy for a multi-tenant service that retrieves each account's latest five authorized events, where hot events are local and historical events are remote. Address lateral/top-N semantics, batching/cache safety, partial failure, ordering, isolation, and release gates.

## Answers to the Exercises

### Answer 1

Each of the two outer `1` occurrences matches both inner `1` occurrences, so inner join emits four `(1,1)` occurrence pairs. NULL-to-NULL is UNKNOWN and `3` matches nothing. Left join emits those four plus `(NULL,null-extended)` and `(3,null-extended)`. Semi join emits outer bag `[1,1]`: each outer occurrence stops after its first TRUE match. Anti join emits `[NULL,3]`: each is emitted only after inner exhaustion finds no TRUE. For each outer occurrence initialize `matched=false`; TRUE sets it, FALSE/UNKNOWN do not. Left null extension and anti emission happen only after exhaustion; semi emits once and stops on TRUE.

### Answer 2

Tuple loop performs (60,000×N_I) predicate comparisons, where inner tuple count (N_I) is missing and must be measured; page count alone cannot finish that CPU total. Simple page loop is approximately (600 + 600×20,000 = 12,000,600) page reads without reuse. With 102 buffers, retain (M-2=100) outer pages per block: (600 + ⌈600/100⌉×20,000 = 120,600) modeled page reads. Indexed loop models (600) outer-page production plus (60,000×4=240,000) lookup/base touches, plus visibility, residual, and 120,000 output-row CPU; page touches may be cached and the four-touch average may depend on key/fanout. Omitted factors include row width, clustering/coverage, index height, cache, prefetch, output materialization, skew, duplicates, nulls, concurrency, parallelism, and startup/latency. Compare calibrated resource coefficients, not raw counts alone.

### Answer 3

Represent each outer occurrence independently. Build a cache key from every referenced outer value plus type/collation/null-safe semantics and any tenant/role/policy, snapshot/version, configuration, or other dependency that permits reuse. Do not memoize volatile/side-effecting or freshness-sensitive evaluation unless its contract explicitly allows one evaluation per key; cache deterministic errors only if repeated-error semantics and diagnostics are preserved. On miss, run a fresh-equivalent inner evaluation, retaining complete rows or a safe spill handle; publish atomically only after success. On hit, replay the full result for every duplicate outer occurrence. Inner/left emit all TRUE pairs; left records per-occurrence match and null-extends empty results; semi emits once for nonempty; anti emits only for empty. Bound memory, evict without semantic change, clean partial entries on cancellation, preserve required sequence or restore it, and invalidate across snapshot/security/schema changes. Instrument hits, misses, evictions, overflows, result bytes, and recomputations.

### Answer 4

Capture engine/build, SQL/parameters, schema/indexes, statistics and extended correlations, estimated/actual rows at each node, loops, distinct/repeated parameter counts, fanout distribution, memo evidence, remote requests/bytes/latency/status, timeouts/retries, cache, concurrency, locks, and result reconciliation. Eight million outer rows turn per-row RPC into eight million failure opportunities; 70% repetition suggests memo/batch potential but only with complete identity/freshness semantics. Immediate controls include bounding concurrency/deadlines, circuit breaking, routing heavy parameters, a reversible plan/query control, or disabling the endpoint feature safely—not caching failures as empty. Durable remedies include correcting cardinality/statistics or query predicates, reducing outer rows early, bulk-fetching/batching remote keys, colocating/replicating authorized data, a valid index, safe memoization, or decorrelation to a bulk join. Gate correctness/tenant isolation, retry reconciliation, request count, p95/p99, source load, memory, and rollback.

### Answer 5

Define semantics first: per account, filter authorized visible events, order by `(occurred_at DESC,event_id DESC)`, return five; ties use event ID. A lateral/parameterized local lookup on `(tenant_id,account_id,occurred_at DESC,event_id DESC)` can stop at five when all required authorization predicates are safely applied. Determine whether remote history is needed from the fifth local boundary, then batch bounded account/range requests while retaining outer/account identity and deterministic order. Cache only immutable versioned historical segments keyed by tenant, account, authorization/policy version, snapshot/manifest, range, and projection; never share by account alone or treat timeout as empty. Merge local/remote candidates per account, recheck authorization and versions, select top five, preserve duplicate event semantics, and fail or return explicitly labeled partial results only under the API contract. Use idempotent requests, deadlines, cancellation, checksums, and resource bounds. Gate adversarial authorization/null/tie/late-event cases, snapshot consistency, injected loss/retry, request amplification, p99, source saturation, memory, ingest impact, and rollback.
