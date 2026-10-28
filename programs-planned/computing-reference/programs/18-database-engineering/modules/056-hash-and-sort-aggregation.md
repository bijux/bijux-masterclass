---
module_id: DBE-056
program: Database Engineering
level: 2
module_number: 56
title: Hash and Sort Aggregation
status: complete
last_verified: 2026-08-30
---

# Hash and Sort Aggregation

## One-Page Review

### Governing question

How can an execution engine partition a bag into SQL groups and compute aggregate states correctly using hashing or ordering, including NULL/empty semantics, `DISTINCT`, ordered inputs, partial combination, memory growth, spill, and parallel finalization?

### Essential definitions

A **grouping key** identifies rows belonging to one SQL group; grouping treats NULL key values as not distinct and colocates them. An aggregate has an **initial state**, **transition function**, optional **combine/serialize/deserialize functions**, and **final function**. A **hash aggregate** maps each distinct grouping key to transition states. A **sort/stream aggregate** consumes rows ordered by grouping key and finalizes a group when its key changes. A **partial aggregate** produces mergeable intermediate states; a **final aggregate** combines/finalizes them. An **ordered aggregate** depends on sequence inside a group. A **holistic aggregate** generally needs state that grows with input for exact results. **Spill** moves rows or states into bounded temporary partitions or sorted runs.

### Central model, mechanism, or theorem

Aggregation separates grouping from reduction. Define exact grouping equivalence. For each group occurrence, feed eligible values—after `FILTER`, NULL, `DISTINCT`, and aggregate-local ordering semantics—through a transition function. Finalization maps complete state to SQL output. Hash and sort aggregation are equivalent when they form the same groups and apply the same per-group multiset or sequence semantics. Partial aggregation is valid only when a combine operation reconstructs state observationally equivalent to processing all represented inputs, including type, overflow, floating, order, error, and NULL behavior.

### Critical invariants

- Every eligible input occurrence contributes exactly once to every applicable aggregate and no ineligible occurrence contributes.
- Group equality, hashing, sorting, collation, coercion, and NULL grouping semantics agree.
- `count(*)`, `count(expr)`, `sum`, `avg`, and empty/all-NULL groups preserve their distinct SQL contracts.
- `FILTER`, `DISTINCT`, and aggregate-local `ORDER BY` occur at the correct logical boundary.
- Transition states are isolated by group and aggregate; mutable state is not accidentally shared.
- Partial combine, serialization, and finalization run only when their algebraic and effect contracts permit them.
- Spill owns every row/state in exactly one recoverable partition or run, without double application or loss.
- Output ordering is claimed only when the complete plan and final SQL `ORDER BY` establish it.

### Common failures

Failures include separating NULL grouping keys; making `count(expr)` count NULL; returning zero for `sum` with no non-NULL values; averaging partial averages; assuming every user aggregate is mergeable; using equality-incompatible hashing; forgetting per-aggregate modifiers; spilling an unserializable state; underestimating groups or growing transition state; letting one group exhaust memory; finalizing partial states twice; assuming hash output is sorted; and globally raising per-operator memory without concurrency accounting.

### Compact example

For A values `10,NULL,20`, `count(*)=3`, `count(value)=2`, `sum=30`, and average state `(30,2)`. C with one NULL has counts 1 and 0 but NULL sum/min/max/average. Two NULL grouping keys form one group. Hash, ordered-stream, and two-part partial-combine implementations in the executable produce identical finite states. This is not proof for arbitrary SQL types, aggregate functions, spill, or parallel engines.

### Connections

Retrieve [Aggregation and Grouping](013-aggregation-and-grouping.md), [Hash Joins](054-hash-joins.md), and [Single-Node Sort-Merge Joins](055-single-node-sort-merge-joins.md). Continue through the Database Engineering [roadmap](../ROADMAP.md) to external sorting, iterator execution, vectorization, and parallel query.

## Governing Question

What group-equivalence, transition-state, ordering, combination, and resource proofs make hash and sort aggregation interchangeable physical implementations of SQL aggregate semantics?

## Why This Matters

Aggregation turns many rows into summaries used for billing, monitoring, science, and product decisions. A one-row or one-cent discrepancy can be material. Physical optimization is valuable only after the exact logical grain, NULL rules, duplicate handling, filters, order, and numerical behavior are established.

Hash aggregation is attractive for unordered input: one lookup locates or creates each group's state, with expected linear work. Memory scales with group count, key width, number and size of transition states, table overhead, and skew. Sort aggregation can stream one group at a time when input is ordered, but otherwise pays sorting and external I/O. Existing index order and downstream ordering can make it globally superior even if hashing looks locally cheaper.

Aggregate functions are programs, not merely names. `avg(x)` needs sum and count rather than unweighted partial averages. Variance needs numerically considered state. String, array, JSON, percentile, and user aggregates can depend on order or have growing state. `DISTINCT` introduces a per-group set problem. Partial results combine only when their state and operation preserve the specified semantics.

Parallelism magnifies opportunity and risk. Workers can reduce locally and exchange compact states, but only for safely combinable aggregates. A million groups may erase the reduction benefit and overload finalization. Floating addition is non-associative, so regrouping can change low-order bits; reproducibility policies need exact types, deterministic trees, stronger accumulation, or stated tolerances.

## Prerequisites and Retrieval

You should understand SQL `GROUP BY`, bags, NULL logic, hash tables, sorting, memory/spill, numerical types, physical plans, and parallel dataflow. Retrieve grouping equivalence, grouping set, transition state, identity, strict transition, finalizer, combine, serialize/deserialize, distributive/algebraic/holistic, `FILTER`, `DISTINCT`, within-aggregate order, partial/final aggregation, group cardinality, state width, spill partition, run, and numerical stability.

DBE-013 established logical aggregation and grain. This module makes its execution state explicit. DBE-057 deepens generic external sorting/spilling; DBE-058 through DBE-060 place aggregation in iterator, vectorized, and parallel pipelines.

## Learning Objectives

After this module, you can:

1. derive SQL group and aggregate results for duplicates, NULLs, empty inputs, filters, and distinctness;
2. specify initialization, transition, combine, serialization, and finalization contracts;
3. implement and prove hash and ordered-stream aggregation equivalence;
4. distinguish distributive, algebraic, holistic, order-sensitive, and growing-state aggregates;
5. derive partial/final aggregation and reject invalid average-of-averages combination;
6. estimate hash-state and external-sort resources, including group and state skew;
7. reason about hash partition spill, sort runs, grouping sets, and per-aggregate auxiliary state;
8. diagnose plans using groups, batches, memory, temporary I/O, workers, and final fan-in;
9. test code with exact oracles, input permutations, partition trees, serialization, and faults; and
10. design production gates for correctness, numerical reproducibility, concurrency, and recovery.

## Core Exposition

**Define logical grouping first.** Let input be a bag of row occurrences and grouping expression tuple K(r). SQL grouping uses not-distinct semantics; multiple NULL keys belong together. This differs from ordinary join equality, where `NULL = NULL` is UNKNOWN. Empty input with grouping columns yields zero groups. An aggregate query without grouping columns creates one global group even on empty input.

Each aggregate call has its own eligibility pipeline. Evaluate its argument and `FILTER`; apply function-specific NULL treatment; apply `DISTINCT`; establish aggregate-local `ORDER BY`; then transition state. `count(*)` sees occurrences regardless of value. `count(x)` counts non-NULL x. Conventional sum/min/max/average ignore NULL and return NULL if no non-NULL value exists, while count returns zero. User aggregates can declare other contracts.

**An aggregate is a state machine.** Represent it by initial state s₀, transition T(s,x), and finalizer F(s). A strict transition may skip NULL arguments. State can differ from input/output: integer average needs sum and count; mergeable variance can retain count, mean, and squared-deviation state; approximate distinct retains a sketch.

Mutable/pass-by-reference state must belong to one group/aggregate context unless copy rules permit sharing. Transition and final functions can allocate, error, or have declared volatility/parallel safety. Destructive finalization is valid only if the state will not be combined or reused afterward.

**Hash aggregation maps keys to state vectors.** For each row, hash its canonical group key, locate candidates, recheck full grouping equality, create a group if absent, and transition each aggregate. Entries include key, table metadata, states, distinct/order auxiliaries, and ownership. Collisions change candidate work, never group identity.

An expected cost model is `N(key+lookup) + Σa Na transition_a + G final + spill + emit`, where N is rows, Na eligible values for aggregate a, and G groups. Memory is roughly G times key/entry/state overhead plus variable auxiliary/state growth. One `array_agg` group can exhaust memory even with G=1.

Hash output follows table/partition traversal and has no SQL ordering guarantee. Hashing also requires group equality and hash compatibility across types, collation, coercion, and versions.

**Sort aggregation turns key changes into boundaries.** Obtain input ordered by grouping key. Initialize state for the first group, transition while keys remain not distinct, finalize when the key changes, and reset. Correctness depends on all occurrences of one group being consecutive. Memory can approach one group's state, excluding the sort and ordered/distinct auxiliaries.

Already ordered input enables streaming and early group output. Otherwise full or incremental external sorting adds comparisons, run I/O, memory, and startup. Stream output may carry a group-key physical order, but applications still need final `ORDER BY`, and later operators can destroy it.

The executable implements hash aggregation, ordered-stream aggregation, and two-way partial combination. State holds occurrence count, non-NULL count, exact integer sum, min, and max; exact average remains `(sum,count)`. It demonstrates a NULL grouping key and an all-NULL group. It excludes SQL collation/types, overflow, floating arithmetic, `DISTINCT`, ordered aggregates, spill, effects, and parallel faults.

<!-- bijux-verify: {"id":"hash-sort-partial-aggregation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"hash_rows=(('A', 3, 2, 30, 10, 20, (30, 2)), ('B', 2, 1, 5, 5, 5, (5, 1)), ('C', 1, 0, None, None, None, (None, 0)), (None, 2, 1, 7, 7, 7, (7, 1)))\nsort_rows=(('A', 3, 2, 30, 10, 20, (30, 2)), ('B', 2, 1, 5, 5, 5, (5, 1)), ('C', 1, 0, None, None, None, (None, 0)), (None, 2, 1, 7, 7, 7, (7, 1)))\npartial_rows=(('A', 3, 2, 30, 10, 20, (30, 2)), ('B', 2, 1, 5, 5, 5, (5, 1)), ('C', 1, 0, None, None, None, (None, 0)), (None, 2, 1, 7, 7, 7, (7, 1)))\nglobal_empty=(0, 0, None, None, None, (None, 0))\ngrouped_empty=()\nall_equivalent=True\nevidence=finite_group_and_state_equivalence\n","stderr":""}} -->
```python
rows = (
    ("A", 10), ("A", None), ("A", 20),
    ("B", None), ("B", 5), ("C", None),
    (None, 7), (None, None),
)


def initial():
    return [0, 0, 0, None, None]


def transition(state, value):
    state[0] += 1
    if value is not None:
        state[1] += 1
        state[2] += value
        state[3] = value if state[3] is None else min(state[3], value)
        state[4] = value if state[4] is None else max(state[4], value)


def combine(left, right):
    result = [left[0] + right[0], left[1] + right[1], left[2] + right[2], None, None]
    mins = [value for value in (left[3], right[3]) if value is not None]
    maxs = [value for value in (left[4], right[4]) if value is not None]
    result[3] = min(mins) if mins else None
    result[4] = max(maxs) if maxs else None
    return result


def finish(key, state):
    count_all, count_value, total, minimum, maximum = state
    sql_sum = total if count_value else None
    return (key, count_all, count_value, sql_sum, minimum, maximum, (sql_sum, count_value))


def aggregate(input_rows):
    states = {}
    for key, value in input_rows:
        transition(states.setdefault(key, initial()), value)
    return states


def ordered_results(states):
    keys = sorted(states, key=lambda key: (key is None, repr(key)))
    return tuple(finish(key, states[key]) for key in keys)


hash_states = aggregate(rows)
sort_states = aggregate(sorted(rows, key=lambda row: (row[0] is None, repr(row[0]))))
partials = [aggregate(rows[::2]), aggregate(rows[1::2])]
combined = {}
for partial in partials:
    for key, state in partial.items():
        combined[key] = combine(combined.get(key, initial()), state)

hash_rows = ordered_results(hash_states)
sort_rows = ordered_results(sort_states)
partial_rows = ordered_results(combined)
print(f"hash_rows={hash_rows}")
print(f"sort_rows={sort_rows}")
print(f"partial_rows={partial_rows}")
print(f"global_empty={finish(None, initial())[1:]}")
print("grouped_empty=()")
print(f"all_equivalent={hash_rows == sort_rows == partial_rows}")
print("evidence=finite_group_and_state_equivalence")
```

The compact sort branch stores finalized groups in a map for comparison; a production stream aggregate would retain only current-key state. The result demonstrates equivalence, not executor memory.

**Partial aggregation needs an algebra.** Combine C(s₁,s₂) must yield state equivalent to transition over the represented union, under the aggregate's sequence semantics. Count combines by addition. Sum adds partial sums while retaining whether any non-NULL value was seen and honoring overflow/type rules. Average combines `(sum,count)`, never unweighted finalized averages.

Associativity and identity enable arbitrary combination trees; commutativity enables reorder. Floating addition is not associative, and order-sensitive aggregates are noncommutative. An engine may specify deterministic trees or numerical tolerance, but must not claim bitwise equivalence without evidence. User aggregate combine functions need property tests.

Serialization preserves state type/version, NULL/empty distinction, numerical metadata, and ownership. Deserialization rejects unknown/corrupt states. Partial output is not necessarily user output: serializing a displayed average instead of `(sum,count)` prevents correct combination. Finalization occurs once at the plan-defined boundary.

PostgreSQL 18 currently documents worker partial aggregation followed by leader finalization. It requires parallel-safe aggregates and combine support, plus serialization for certain internal states, and currently excludes cases such as aggregate `DISTINCT`, aggregate-local `ORDER BY`, ordered-set aggregates, and grouping sets. These are product/version constraints, not universal impossibility results.

**Aggregate classes predict state.** Distributive count/min/max and suitably defined sum use bounded same-form partials. Algebraic average uses bounded components. Exact median, percentile, distinct, and collection aggregation can require state growing with group cardinality or sorting/deduplication. Approximate sketches bound state only with explicit error/confidence and compatibility contracts.

Order-sensitive aggregation such as string/list concatenation requires aggregate-local order. Group-key order alone is insufficient. Different ordered aggregates may need different per-group sorts. Without local order, current documentation can call processing order unspecified/arbitrary; observed scan/hash order is not a contract.

`DISTINCT` means each distinct argument tuple contributes once per group and aggregate call. Implementations use per-group sets or sorting, sharing only when full semantic identity matches. NULL handling, collation, multiple arguments, filters, and order remain part of that identity.

**Hash spill partitions future work.** Under pressure, partition raw rows or serializable partial states by group-key hash. Equal keys must reach the same eventual partition or combine later. Spilling raw rows is general but repeats transitions; states save work only when combine/serialization are valid.

Dynamic growth assigns every row/state to exactly one batch. Oversized partitions can recurse with new bits. One huge group or state cannot be split unless the aggregate is decomposable; a new hash seed does not divide one equality key. Disk-full, corruption, cancellation, or unknown state versions are explicit failures, not empty groups.

**Sort spill externalizes order.** Generate ordered runs and merge them, streaming states as group boundaries appear. It handles many groups with bounded aggregation memory but pays comparisons and I/O. Grouping sets may exploit rollup-compatible order, require multiple passes, or use multiple hash tables. Grouping-set identity distinguishes subtotal placeholder NULLs from data NULLs.

Hash and sort spill face different skew: many groups pressure hash entries; a growing single-group state pressures either method. Adaptive switching is correct only if every state transfers once and aggregate capabilities are preserved.

**Numerical correctness is policy.** Integer sums may widen, error, or overflow according to type contracts. Floating sums vary by order and suffer cancellation. Pairwise/compensated summation and mergeable variance improve behavior but carry their own states. Min/max depend on collation, NaN, signed zero, and comparison rules.

Choose a fitting oracle: exact integer/rational, high-precision decimal, derived tolerance, interval bound, or bitwise deterministic policy. Partial tests permute rows and trees. Approximate functions verify error distribution, confidence, bias, seed/version compatibility, and adversarial inputs—not exact equality.

**Execution includes HAVING and lifecycle.** Evaluate grouping expressions and arguments at their logical point; finalize, construct group output, evaluate `HAVING`, then project. Push `HAVING` only with a rewrite proof. Errors/cancellation clean group contexts, tables, sorts, spill files, and workers.

Global empty aggregation initializes and finalizes one state; grouped aggregation emits none. Grouping sets can include an empty-set total. A per-aggregate `FILTER` false for all rows means empty input to that call inside a nonempty group.

**Evidence must expose resources.** Capture engine/build, SQL/parameters, grouping sets/keys/collations, aggregate definitions/modifiers, input/order paths, estimated/actual rows/groups, rows per group, hash batches, state memory/width, sort method/runs, temp I/O, distinct/ordered auxiliaries, partial/final rows, worker balance, exchange bytes, output, latency, concurrency, and cleanup.

Per-operation memory is not necessarily query/server memory. Operators, auxiliary structures, workers, and sessions multiply it. PostgreSQL 18 documents per-operation sort/hash memory and a hash multiplier. Capacity uses peak overlapping workload, not one plan node.

Regressions often reflect stale group estimates, wider/growing states, new high-cardinality keys, skew, added `DISTINCT`/order, lost input order, changed collation, more grouping sets, disabled partial combination, or concurrency. Remedies address grain, statistics, projection, compatible order/indexes, safe partial reduction, bounded approximations where allowed, scheduling, or algorithm choice. Hints remain scoped and expiring.

**Verification separates semantics, state algebra, and performance.** Generate duplicate/NULL keys, empty/global/grouped inputs, all-NULL values, filters, distinct duplicates, ordering ties, boundary numerics, collations, large states, skew, and multiple calls. Compare hash and sort maps to an independent evaluator. Compare many partial trees with single-pass state under exact or declared tolerance semantics.

Force collisions, many groups, growing states, spill recursion, external runs, serialization round trips, corrupt/disk-full files, worker loss, cancellation, and unknown versions. Verify ownership, states, outputs, errors, ordering claims, and cleanup. Only then sweep memory, group cardinality, state width, skew, workers, concurrency, and temp storage for latency, CPU, bytes, memory, and fairness.

## Definitions and Notation

- K(r): grouping tuple for row occurrence r.
- s₀, T, C, F: initial, transition, combine, and final functions.
- N, G, Na: input occurrences, groups, and values eligible for aggregate a.
- **Grouping equivalence**: SQL not-distinct relation, including NULL grouping.
- **State vector**: all transition states and auxiliaries for one group.
- **Hash aggregate**: key-to-state table over unordered input.
- **Sort/stream aggregate**: state machine over consecutive ordered groups.
- **Partial/final aggregate**: intermediate state production and later combination/finalization.
- **Distributive/algebraic/holistic**: same-form bounded, bounded-component, or generally unbounded exact state classes.
- **Aggregate modifiers**: per-call `FILTER`, `DISTINCT`, and `ORDER BY` semantics.
- **Spill partition/run**: bounded external hash ownership or sorted sequence.
- **Grouping-set identity**: metadata distinguishing subtotal levels and placeholder NULLs.

## Mechanisms, Invariants, or Proof Structure

Hash proof maintains: after any input prefix, every observed grouping key has exactly one entry and its states equal transitions over exactly that group's eligible occurrences. Compatible hash plus equality recheck locates the group; one transition preserves the invariant. Finalization after exhaustion yields every group once.

Sort proof adds: completed ordered keys cannot recur, so their states are complete; current state represents exactly the current key prefix. Bag-preserving sorting plus this boundary proof gives hash-equivalent output.

Partial proof requires C(S(X),S(Y)) observationally equal S(X ⊎ Y), with identity and order constraints stated. Induction over the combination tree establishes final equivalence. Spill additionally requires every row/state owned exactly once and all same-key contributions combined before finalization.

## Alternatives and Trade-Offs

Hash avoids ordering and offers expected linear lookup but stores all groups/states and may spill under skew. Sort streams ordered groups and can deliver useful order but pays sorting and I/O. Index order may remove sorting but adds scan/write/locality costs. Partial aggregation reduces movement only when combination is safe and groups shrink meaningfully. Exact holistic states preserve exactness but grow; sketches bound state with explicit error. Materialized summaries reduce query work while adding freshness, correction, and lineage obligations.

Choose by semantics, group count, state size/growth, input/required order, modifiers, combination ability, numerical policy, memory/temp, concurrency, parallel reduction, skew, and recovery.

## Failure Modes and Misconceptions

1. **“GROUP BY uses ordinary equality.”** It colocates not-distinct NULL keys; join semantics differ.
2. **“All counts and sums treat NULL alike.”** `count(*)`, `count(x)`, and `sum(x)` differ.
3. **“Average partial averages.”** Combine sum/count or another proven weighted state.
4. **“Every aggregate is associative.”** Floating, ordered, holistic, and user states may not freely regroup.
5. **“Hash collisions merge groups.”** Full grouping equality rechecks candidates.
6. **“Sort aggregation always uses little memory.”** Sorts, distinctness, order, and one growing group can spill.
7. **“One memory setting caps the query.”** Auxiliaries, workers, operators, and sessions multiply usage.
8. **“Any state can spill.”** It needs valid serialization/combine or raw input retention.
9. **“Partial aggregation always helps.”** High group cardinality or large states can erase reduction.
10. **“Hash output is grouping order.”** Group identity does not imply output sequence.
11. **“Any floating difference proves failure.”** Judge the declared exact/tolerance/reproducibility contract.
12. **“More memory fixes one huge group.”** State/output may be logically unbounded.

## Worked Examples

### Example 1

Rows `(NULL,1)` and `(NULL,2)` group together and sum to 3. An ordinary equality join would not match those NULL keys. Conclusion: grouping uses not-distinct semantics.

### Example 2

A values `10,NULL,20` yield counts 3 and 2, sum 30, average 15. C `[NULL]` yields counts 1 and 0 with NULL sum/average. Conclusion: occurrence and eligible-value states are separate.

### Example 3

Empty global aggregation returns one row `(count=0,sum=NULL)`; empty grouped aggregation returns no rows. Conclusion: global state initialization differs from grouped execution.

### Example 4

Partitions average 10 over 100 rows and 30 over one row. Average-of-averages gives 20; correct result is 1030/101. Conclusion: combine weighted state.

### Example 5

Input already ordered by tenant lets stream aggregation emit one tenant at a time and feed an ordered report. Hash stores all tenants and needs a final sort. Conclusion: existing/downstream order can dominate.

### Example 6

Ten groups each build arrays of millions of values. Group count looks tiny while transition state dominates memory. Conclusion: estimate state distributions, not only G.

### Example 7

`count(DISTINCT user_id) FILTER (WHERE paid)` needs a paid-only distinct set. Sharing an unfiltered set changes results. Conclusion: modifiers belong to the call's semantic identity.

### Example 8

Workers emit nearly one partial state per input row because keys are unique. Exchange and final aggregation see little reduction. Conclusion: partial aggregation value depends on group reduction.

### Example 9

Hash aggregate expects 50,000 groups but sees 20 million and spills many partitions after a dimension-grain change. Conclusion: inspect grain/statistics/state width before raising memory.

### Example 10

A user state lacks a version tag; rolling upgrade deserializes old bytes using a new layout and corrupts totals. Conclusion: state format/upgrade compatibility is correctness.

## Cross-Program Connections

- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies hash tables, sets, sketches, heaps, and compact state.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies reductions, monoids, external sorting, numerical analysis, and adversarial tests.
- [Programming Languages and Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) supplies state machines, effects, serialization, type laws, and equivalence.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) supplies cache-local hashing, vector reductions, SIMD, and bandwidth.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies keyed shuffle, combiners, retry, partitioning, and version coordination.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) supplies batch/stream aggregation, watermarks, corrections, and semantic metrics.

## References

1. PostgreSQL Global Development Group, [Aggregate Functions](https://www.postgresql.org/docs/current/functions-aggregate.html), PostgreSQL 18 current documentation, retrieved 2026-08-30; NULL/empty behavior, order-sensitive calls, partial capability, and ordered-set aggregates.
2. PostgreSQL Global Development Group, [Table Expressions](https://www.postgresql.org/docs/current/queries-table-expressions.html), PostgreSQL 18 current documentation, retrieved 2026-08-30; `GROUP BY`, grouping sets, `HAVING`, and evaluation.
3. PostgreSQL Global Development Group, [Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html), PostgreSQL 18 current documentation, retrieved 2026-08-30; aggregate/sort plans and runtime evidence.
4. PostgreSQL Global Development Group, [Resource Consumption](https://www.postgresql.org/docs/current/runtime-config-resource.html), PostgreSQL 18 current documentation, retrieved 2026-08-30; per-operation sort/hash memory and concurrency.
5. PostgreSQL Global Development Group, [Parallel Plans](https://www.postgresql.org/docs/current/parallel-plans.html), PostgreSQL 18 current documentation, retrieved 2026-08-30; partial/final aggregation and combine/serialization constraints.
6. PostgreSQL Global Development Group, [`nodeAgg.c`](https://github.com/postgres/postgres/blob/REL_18_STABLE/src/backend/executor/nodeAgg.c), PostgreSQL 18 stable source, retrieved 2026-08-30; transition/final phases, strategies, grouping sets, partial states, and hash spill.
7. PostgreSQL Global Development Group, [`execGrouping.c`](https://github.com/postgres/postgres/blob/REL_18_STABLE/src/backend/executor/execGrouping.c), PostgreSQL 18 stable source, retrieved 2026-08-30; grouping equality and tuple hash-table support.
8. Goetz Graefe, [“Query Evaluation Techniques for Large Databases”](https://web.stanford.edu/class/cs346/2014/graefe.pdf), *ACM Computing Surveys* 25(2), 1993; hash/sort aggregation, duplicate removal, and partitioning.
9. DuckDB Foundation, [`GROUP BY` Clause](https://duckdb.org/docs/current/sql/query_syntax/groupby.html), current official documentation, retrieved 2026-08-30; grouping syntax, sets, and current `GROUP BY ALL` behavior.
10. SQLite Project, [Built-in Aggregate Functions](https://www.sqlite.org/lang_aggfunc.html), current official documentation, retrieved 2026-08-30; NULL, empty, numeric, `DISTINCT`, `FILTER`, and aggregate-order behavior.

## Exercises

### Exercise 1

Derive grouped/global results for keys `[A,A,B,NULL,NULL]`, values `[10,NULL,NULL,5,NULL]`, and count/sum/min/max/average state. Include empty input.

### Exercise 2

Specify transition, combine, and final functions for exact average and population variance, including identity, NULL behavior, representation, and parallel validity.

### Exercise 3

Design a hash aggregate that spills raw rows or partial states. Specify grouping identity, memory accounting, ownership, recursion, growing state, serialization, cancellation, and oracle tests.

### Exercise 4

Diagnose partial hash aggregation followed by spilled sorted final aggregation where workers emit nearly as many groups as rows and floating totals differ in low bits. Separate correctness, resource, and reproducibility issues.

### Exercise 5

Design exact and approximate per-tenant distinct aggregation for retried, late-corrected events across schema upgrades, skew, and privacy constraints. Define algebra, identity/error semantics, persistence, and gates.

## Answers to the Exercises

### Answer 1

A has `(count*=2,count(value)=1,sum=10,min=10,max=10,avg-state=(10,1))`. B has `(1,0,NULL,NULL,NULL,(NULL,0))`. The NULL keys form one group with `(2,1,5,5,5,(5,1))`. The global group has count 5, non-NULL count 2, sum 15, min 5, max 10, state `(15,2)`, and exact average 15/2. Empty grouped output has no rows; empty global output is `(0,0,NULL,NULL,NULL,(NULL,0))`. Zero is not a substitute for absent sum unless explicitly coalesced.

### Answer 2

Average state `(sum,count)` ignores NULL, starts `(0,0)`, adds `(x,1)`, combines componentwise, and finalizes NULL for zero count else exact sum/count. Choose a widening/exact representation and overflow policy. Population variance can use `(n,mean,M2)`: transition uses `delta=x-mean`, new mean `mean+delta/(n+1)`, and `M2+delta*(x-new_mean)`. Combine A/B using total n, mean shift weighted by counts, and `M2a+M2b+delta²*na*nb/n`; empty is identity, final is NULL for zero else M2/n. Arbitrary tree combination is exact over real/rational arithmetic. Floating implementations are order-sensitive and need tolerance, deterministic tree, or stronger arithmetic.

### Answer 3

Use canonical group keys with compatible hash/equality and entries containing key, states, auxiliaries, widths, and ownership. Account for buckets, keys, state/allocator growth, distinct/order structures, child/spill buffers, and output. On pressure partition by group hash. Raw spill stores key, needed arguments/filter decisions, occurrence identity, integrity/version; state spill requires valid combine and serialization. Every row/state owns exactly one batch and same-key contributions combine before finalization. Repartition oversized batches with new bits, but route one huge state to aggregate-specific spill, raw retention, bounded approximation, or explicit resource failure. Fail on disk-full/corruption/version mismatch; stop readers before cleanup. Differentially test all forced paths against a logical evaluator and single-pass states.

### Answer 4

Capture engine/build, definitions/modifiers, keys/collations, estimates/actual rows/groups and per-worker reduction, state widths, batches/memory, final sort runs/temp, exchange, worker/final-stage time, concurrency, and an exact/high-precision oracle. Near-one group per row explains weak partial reduction and large exchange/final sort. Low floating differences can be legal non-associative regrouping under a tolerance contract; missing groups or excessive error is incorrect. Remedies include corrected grain/statistics, safe hash finalization, useful order, narrower state, scheduling/memory evidence, or deterministic/compensated arithmetic. Gate group reconciliation, numerical policy, p95/p99, temp/memory, balance, and rollback.

### Answer 5

Define canonical event and subject identity plus retry deduplication. Exact state is a per-tenant set with union combine and cardinality final; persist partitioned/sorted sets with checksum, watermark/snapshot, schema/hash/policy version, encryption, and reversible correction or window recomputation. It is unbounded, so quota/partition/compact or fail visibly for hot tenants. Approximate state is a compatible mergeable sketch with fixed precision, hash/seed/version, sparse/dense format, bias correction, and confidence/error contract. Never merge incompatible sketches or tenants. Test retries, late add/retract, NULLs, equal cross-tenant IDs, upgrades, skew, corruption, worker loss, and replay. Gate exact samples, statistical coverage/bias, privacy isolation, deterministic compatible merges, resources, recovery, cleanup, and rollback.
