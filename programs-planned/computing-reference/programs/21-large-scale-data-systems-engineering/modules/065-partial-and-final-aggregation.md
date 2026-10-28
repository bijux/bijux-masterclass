---
module_id: LSDS-065
program: Large-Scale Data Systems Engineering
level: 2
module_number: 65
title: Partial and Final Aggregation
status: complete
last_verified: 2026-09-04
---

# Partial and Final Aggregation

## One-Page Review

### Governing question

How should a distributed query engine decompose aggregation into local, intermediate, and final stages so SQL null, empty-input, distinct, ordering, grouping, numerical, memory, and retry semantics remain correct while data movement is reduced?

### Essential definitions

- An **aggregate state** is the typed internal summary updated by input rows, merged with peer states, and finalized into an output value.
- A **partial aggregation** builds states near input partitions before exchange.
- An **intermediate aggregation** merges partial states, often in a tree or after repartition.
- A **final aggregation** produces the externally defined result from complete merged state.
- A **distributive aggregate** merges states of the same result form, such as count or sum under an appropriate numeric contract.
- An **algebraic aggregate** uses a fixed-size tuple of distributive states, such as average represented by sum and count.
- A **holistic aggregate** may require unbounded information for an exact result, such as an arbitrary exact median.
- **decomposability** means there is a sound state/merge/finalize contract for the chosen partitioning and semantics.
- A **combine ratio** compares rows or bytes after local aggregation with its input and indicates exchange reduction.
- A **grouping set** specifies one subset of grouping expressions; rollup and cube generate several such sets.

### Central model, mechanism, or theorem

For aggregate state space $S$, identity $e$, row lift $\phi:X\to S$, and associative merge $\oplus$, a decomposable aggregate over bag $X$ has

$$A(X)=\operatorname{finalize}\left(\bigoplus_{x\in X}\phi(x)\right).$$

Partitioning $X$ into bags $X_1,\ldots,X_p$ is sound when merging partial states yields the same defined result as aggregating the whole bag, subject to type, null, overflow, order, and approximation contracts. Grouped aggregation additionally hash/range-routes each grouping key to one final owner. This algebra explains why `AVG` merges `(sum,count)`, why averaging partition averages is wrong, and why exact order-sensitive or distinct aggregates need richer state or additional distribution.

### Critical invariants

- Aggregate name, arguments, filter, distinct/order clauses, grouping sets, types, null behavior, empty-input behavior, and output schema are fixed before decomposition.
- Partial, intermediate, and final stages use a versioned compatible state schema and merge semantics.
- Every selected input row contributes exactly once to the winning aggregate attempt; retries and speculation do not double-merge.
- Equal grouping keys meet at one compatible final owner; null grouping keys follow the language's grouping semantics.
- `AVG` and similar algebraic aggregates merge sufficient statistics, not finalized partition results.
- Exact distinct aggregation deduplicates in the declared argument tuple and scope before final counting or combination.
- Order-sensitive aggregates receive an explicit compatible order or retain enough state to reproduce it.
- Hash tables, distinct sets, sorted runs, sketches, buffers, spill, and recursive partitions have governed bounds.
- Numeric overflow, precision, floating nondeterminism, NaN, and approximation error are declared and tested.
- Connector pushdown is trusted only under compatible snapshot, grouping, null, type, overflow, filter, and security semantics.

### Common failures

Common failures include averaging partition averages; finalizing a partial state too early; treating `SUM` over empty input like `COUNT`; forgetting that null values are usually ignored by many aggregates but null grouping keys form a group; pushing `DISTINCT` through an unsafe boundary; losing aggregate filters; assuming floating addition is associative; overflowing narrow partial sums; using hash aggregation when group cardinality exceeds memory; claiming partial aggregation helps when almost every input key is unique; merging sketches with incompatible parameters; emitting results from speculative states twice; and trusting a connector's aggregate result despite different snapshot or null semantics.

### Compact example

Three partitions contain non-null values with local `(sum,count)` states `(4,2)`, `(12,2)`, and `(12,1)`. Merging yields `(28,5)` and final average `5.6`. Averaging local means `(2,6,12)` would yield about `6.67`, incorrectly weighting partitions rather than rows. Empty partials contribute identity `(0,0)`; finalization must define the zero-count result according to SQL semantics.

### Connections

[LSDS-031](031-shuffle-architecture.md) supplies shuffle, [LSDS-061](061-distributed-logical-and-physical-plans.md) defines physical properties, [LSDS-063](063-exchange-operators.md) establishes grouping-key ownership, and [LSDS-064](064-distributed-hash-and-merge-joins.md) provides related hash/sort, spill, skew, and attempt mechanics.

## Governing Question

Aggregation replaces many input rows with one state per group, making it a natural opportunity to reduce data before network exchange. Yet the optimization is only correct if the state can be merged without losing information. Count and sum look simple; average needs sum plus count; variance needs a numerically meaningful merge state; exact distinct may require sets or a deduplication plan; ordered concatenation needs order; exact quantiles may need essentially all values.

SQL adds edge semantics. Most aggregates ignore null argument values, but grouping treats null keys as not distinct for grouping. A global aggregate over an empty relation still returns one row, while grouped aggregation over no groups returns none. `COUNT` returns zero; many others return null. Filters, distinct tuples, grouping sets, decimal overflow, collation, and nondeterministic input order constrain decomposition.

The governing question is how to define aggregate algebra first, map it into distributed stages and compatible exchange, keep state bounded, recover attempts, and measure whether partial work reduces the critical path rather than merely adding another operator.

## Why This Matters

Aggregation is central to reporting, features, monitoring, data quality, billing, and scientific analysis. A subtle state-merge error can alter financial totals or cardinalities while returning reasonable-looking rows. Numerical order changes can break reproducibility. Duplicate attempt state can inflate counts after a retry. Incorrect empty-input handling can change downstream joins or alerts.

Performance stakes are equally large. Local partial aggregation can turn billions of rows into thousands of group states before shuffle. With high-cardinality keys, it may reduce nothing while consuming memory and CPU. One hot group can dominate a final partition; exact distinct can create state proportional to the data; grouping sets can multiply state; spill can turn a fast hash aggregation into repeated I/O.

The plan must therefore connect semantic state, distribution, memory, storage, fault tolerance, and observability. “Partial aggregation enabled” is not an outcome; combine ratio, bytes avoided, CPU added, spill, tail partition, result correctness, and recovery behavior are.

## Prerequisites and Retrieval

Review shuffle in [LSDS-031](031-shuffle-architecture.md), resource models in [LSDS-051](051-cluster-resource-models.md), isolation in [LSDS-057](057-memory-cpu-and-i-o-isolation.md), distributed physical plans in [LSDS-061](061-distributed-logical-and-physical-plans.md), exchange semantics in [LSDS-063](063-exchange-operators.md), and hash/merge execution in [LSDS-064](064-distributed-hash-and-merge-joins.md).

You should understand SQL bags and nulls, grouping, monoids, hash tables, sorting, partitioning, numeric types, floating-point arithmetic, sketches, spill, retries, snapshots, and cost-based optimization.

## Learning Objectives

After this module, you should be able to:

1. specify update, merge, identity, finalize, state-schema, and error contracts for an aggregate;
2. classify distributive, algebraic, holistic, distinct, and order-sensitive aggregation needs;
3. preserve SQL null, empty-input, filter, duplicate, and grouping-set semantics across stages;
4. design local/intermediate/final aggregation and grouping-key exchange;
5. compare hash, sort/streaming, tree, and connector-pushed aggregation;
6. implement bounded spill and diagnose high-cardinality or hot-group behavior;
7. reason about overflow, decimals, floating reproducibility, variance, and approximation error;
8. commit aggregate attempts safely under retry, speculation, and adaptive repartitioning;
9. instrument combine ratio, state, skew, spill, estimate error, and full resource cost; and
10. validate aggregates with algebraic, differential, metamorphic, fault, and performance tests.

## Core Exposition

### Define the aggregate contract

For each aggregate, declare argument and result types, accepted rows, null behavior, state type, identity, update, merge, finalize, serialization, version, overflow, determinism, and error semantics. `FILTER`, `DISTINCT`, and argument `ORDER BY` are part of this contract, not decorations.

State may differ from result. Average state includes numerator and count; approximate distinct state is a sketch; string aggregation may hold ordered values or runs. Never infer mergeability because final values share a type.

### Classify decomposability

Distributive aggregates such as count, min, max, and an appropriately defined sum can merge same-form summaries. Algebraic aggregates use a bounded tuple of summaries: average uses sum/count, while variance can use count/mean/second-moment state. Holistic exact aggregates may grow with input.

These categories depend on semantics and representation. An approximate quantile sketch is mergeable under fixed parameters while exact median is not fixed-size. An ordered aggregate may become mergeable with sorted runs and a global merge, but its state and cost differ.

### Preserve SQL null semantics

Many aggregates ignore null arguments: `COUNT(x)` counts non-null `x`, while `COUNT(*)` counts rows. `SUM`, `AVG`, `MIN`, and `MAX` over no contributing values commonly finalize to null, whereas count finalizes to zero. Verify the target dialect and function.

Grouping keys behave differently: null keys belong to a group under SQL grouping rules. Composite grouping keys need type/collation/null-compatible hashing or comparison across exchanges. Do not reuse join ordinary-equality null exclusion blindly.

### Handle empty inputs correctly

A global aggregate without grouping keys generally produces one result row even on empty input. A local partition may be empty and emit no state or the identity; the final stage must still synthesize the global empty result. Grouped aggregation over an empty input has no groups and returns no rows.

Grouping sets may include the empty grouping set, which creates a grand-total row. Distinguish a null placeholder introduced by rollup from a data null using grouping metadata where the language exposes it.

### Use sufficient partial states

Average is not the average of partial averages unless partitions contain equal contributing counts. Lift each value to `(value,1)`, merge components by addition, and finalize `sum/count` when count is positive. Preserve numeric widening and null behavior.

For ratios or weighted means, retain numerator and denominator defined by the formula. For variance, use a mergeable stable state rather than subtracting two large nearly equal sums naively. Document whether the result is population or sample variance.

### Build a staged aggregation plan

A common grouped plan scans and filters, performs partial aggregation per input task, hash-exchanges partial states by grouping keys, then performs final aggregation per destination. An intermediate tree can reduce fan-in or merge states before a distant exchange.

Each stage knows whether input is raw rows or serialized states. State schema/version is part of the plan and exchange. Finalize only at the boundary that needs the external result; a finalized value may not be mergeable.

### Prove grouping-key ownership

All partial states for one group must reach the same final owner unless a later merge reunites them. Hash exchange must agree on grouping expressions, resolved types, canonical encoding, collation, null policy, hash version, partition count, and epoch.

Range distribution can support ordered group output but boundaries must not split equal keys. If input already has compatible distribution, the plan may skip exchange. Validate storage/file-level guarantees rather than trusting table labels.

### Decide when partial aggregation helps

Compute rows and bytes before versus after local aggregation. Low-cardinality repeated keys yield strong reduction. If nearly every input row has a unique key, partial state may be as large as or larger than input due to hash/state overhead.

Cost added CPU, memory, latency, and spill against exchange saved. An adaptive planner can sample or observe combine ratio and bypass further partial work where safe. Do not disable semantic stages that are required, only optional pre-combination.

### Choose hash aggregation

Hash aggregation maps each group key to mutable state and works without sorted input. It provides expected constant-time lookup but consumes memory proportional to groups and state size, with skew and allocator effects. Use vectorized batch updates where semantics permit.

Account for keys, hash values, bucket arrays, state payload, distinct/filter/order state, null/grouping-set metadata, alignment, and fragmentation. Serialized output bytes underestimate live memory. Reserve and spill before hard exhaustion.

### Choose sort or streaming aggregation

If input is compatibly ordered by grouping keys, streaming aggregation keeps one group or equal-key run at a time. If not, external sort creates order at CPU and I/O cost. Sort aggregation can be more predictable for high cardinality and can share required downstream ordering.

Ordering comparison and grouping equality must agree so one group is contiguous. Collation, nulls, NaN, decimal normalization, and composite keys need consistent rules. Large ordered-aggregate values may still require spill.

### Spill hash state safely

Partition raw rows or partial states by a secondary hash into aligned spill partitions, then aggregate each partition. Serialize versioned state only if merge is supported; otherwise spill raw arguments. Record query/operator/side, partition, attempt, schema, count, checksum, and completion manifest.

Recursive partitioning must show size reduction. One hot group remains indivisible in a normal final aggregation and may require an external state representation, specialized aggregate, more memory, approximation, or bounded failure. Limit files, passes, writers, and storage.

### Handle hot groups and skew

A popular key sends all final state to one owner, but local partial aggregation may reduce each producer to one small state. For simple sum/count this is often manageable; for exact distinct, arrays, maps, percentiles, or ordered collections, state remains large.

Some aggregates can split a hot group's state across subpartitions and merge later because $\oplus$ is associative. Assign deterministic subpartition ownership, then add another merge stage. This distributes update work but finalization may still be singular.

### Implement count and sum precisely

`COUNT(*)` adds one for every accepted row; `COUNT(x)` adds only for non-null `x`. Partial counts merge by addition using a sufficiently wide type and defined overflow behavior. Failed/speculative attempts must not contribute twice.

Sum chooses an accumulation type and overflow contract. Integer, decimal, interval, and floating sums differ. Widen partial states where the dialect requires it, and make connector pushdown return compatible state or a finalized result used only at the correct boundary.

### Implement min and max carefully

Min/max ignore nulls under common SQL semantics and retain whether any non-null value was observed. The identity cannot always be represented by a normal domain value; use an explicit empty flag. Merge chooses the better observed value.

Comparison follows type, collation, time-zone, and NaN rules. Returning an arbitrary payload associated with a min/max key requires a tie policy or a different aggregate such as `min_by`; distributed merge must preserve its exact contract.

### Merge variance and numeric state

A stable parallel variance state can retain count $n$, mean $\mu$, and sum of squared deviations $M_2$. Merging two states adjusts for the difference between means rather than simply summing independently centered deviations.

Test zero/one counts, extreme magnitudes, cancellation, infinities, and NaN. Floating merge order can change low bits because addition is not mathematically associative in finite precision. State whether reproducibility is bitwise, tolerance-based, or unspecified.

### Design exact distinct aggregation

`COUNT(DISTINCT x)` needs global uniqueness of non-null argument values per group. A plan can locally deduplicate `(group,x)`, exchange by a compatible ownership key, deduplicate globally, then count per group, possibly requiring another exchange depending on ownership.

Multiple distinct aggregates over different argument tuples cannot always share one set or exchange. State can be enormous. Bound it, spill exact sets/runs, or offer an explicitly approximate function rather than silently changing semantics.

### Merge approximate sketches

Sketches for distinct counts, quantiles, frequent items, or distributions can be compact and mergeable. Compatibility includes algorithm/version, precision, seed/hash, type encoding, error model, and any ordering/weight rules. Reject incompatible states.

Report confidence/error guarantees and adversarial limitations. Merging many sketches may affect error or representation. Approximation is part of the function contract and must not replace an exact aggregate without user/policy authorization.

### Preserve order-sensitive aggregates

String/list aggregation with argument ordering, ordered-set aggregates, and some user-defined functions depend on a total or partial order. Partial states can be sorted runs carrying order keys and stable tie semantics; final merge produces the requested order.

Without an explicit order, distributed arrival order is nondeterministic and may legitimately vary. Do not promise reproducibility based on current task completion order. For ties, the language may leave order unspecified unless an additional key is declared.

### Apply filters before aggregate update

An aggregate `FILTER` controls which rows update that aggregate, not the whole input necessarily. Several aggregates can have different filters over the same groups. Preserve three-valued predicate behavior; only true contributes.

Push filters toward scans when semantically safe, but retain per-aggregate distinctions. Partial states need no record of rejected rows if the filter was evaluated exactly under the same types/functions/security context.

### Expand grouping sets without losing identity

Rollup, cube, and explicit grouping sets can conceptually map an input row to several grouping identities. Include grouping-set ID or equivalent metadata in hash state and exchange so data-null and rolled-up placeholder remain distinguishable.

Naive cube expansion grows exponentially with grouping columns. Share scans and compatible states, prune unused sets, and enforce policy limits. Cost output cardinality and state multiplication explicitly.

### Push aggregation into connectors cautiously

Connector pushdown can reduce source bytes dramatically, especially when the source owns compatible partitions. Negotiate supported functions, grouping expressions, filters, distinct/order clauses, null/empty semantics, numeric types/overflow, snapshots, collation, and security.

An incomplete pushdown may return partial states only if the engine understands their versioned schema and merge. Otherwise treat returned values as final for their proven scope and add a sound outer merge plan. Explain what executed remotely.

### Handle retries and speculation

Partial states belong to logical input partitions and attempts. Exchange or stage commit selects one complete attempt per logical partition before final merge. Adding both a failed prefix and retry state double-counts; count equality alone will not detect offsetting errors.

Spill and sketch files carry attempt identity and integrity. Final outputs are attempt-scoped until selected. Cleanup honors recovery retention. User-defined aggregates with external effects are unsafe for transparent retry unless isolated and committed separately.

### Adapt aggregation safely

Runtime group count, state bytes, combine ratio, and partition skew can switch optional partial aggregation, hash to sort/spill, partition count, or hot-group splitting. Adapt before downstream consumers commit to the old state distribution, or restart them under a new epoch.

State version and semantic contract remain unchanged unless the entire affected pipeline is replaced compatibly. Bound adaptations and retain evidence. A low combine ratio alone does not authorize dropping necessary global aggregation.

### Observe aggregation causally

Correlate logical aggregate, physical stage, grouping set, exchange, partition, task/attempt, worker, spill, state version, and adaptive epoch. Emit estimated/actual input/output rows/bytes, groups, nulls, distincts, state memory, combine ratio, hash collisions, sort runs, spill, network, blocked time, and tail.

Track numeric overflow/error, sketch parameters/error, retries, selected attempts, and connector pushdown. Protect sensitive group keys and cardinalities. Compare resource saved by partial reduction with CPU/memory/spill it added.

### Validate algebra and execution

Property-test identity and merge behavior over many random partitionings and merge trees. Differentially compare single-stage and staged execution. Generate empty/all-null inputs, duplicates, high cardinality, hot groups, composite/null keys, filters, distinct tuples, grouping sets, overflow, extreme floating values, and ordered ties.

Inject spill corruption/full storage, worker loss, duplicate attempts, stale epochs, connector mismatch, adaptive restart, and state-version incompatibility. Gate exact results first, approximation error separately, then bounds, throughput, tail, fairness, recovery, and cost.

## Definitions and Notation

Let input bag be $X$, grouping function $g:X\to K$, aggregate state space $S$, identity $e\in S$, row lift/update contribution $\phi:X\to S$, associative merge $\oplus:S\times S\to S$, and finalizer $f:S\to Y$.

For partition $X_i$, partial state is $s_i=\bigoplus_{x\in X_i}\phi(x)$. The final result is $f(\bigoplus_i s_i)$ when the aggregate contract permits decomposition. Commutativity is needed when merge order is unconstrained; otherwise execution must preserve a declared order.

For group $k$, use $X_k=\{x:g(x)\text{ is not distinct from }k\}$ under grouping semantics. A compatible exchange sends all partial states for $k$ to one final owner or a merge tree that eventually reunites them.

Let input rows/bytes be $(N_i,B_i)$ and partial output $(N_p,B_p)$. Row combine ratio $\rho_N=N_p/N_i$ and byte ratio $\rho_B=B_p/B_i$ are defined for positive denominators; lower values mean stronger reduction but omit CPU, memory, spill, and tail.

Average state is $(s,n)$ with merge $(s_1+s_2,n_1+n_2)$ and final $s/n$ for $n>0$, otherwise the dialect's empty result. State types may widen beyond input/result types.

## Mechanisms, Invariants, or Proof Structure

Use this audit sequence:

1. Fix aggregate/grouping/filter/distinct/order semantics, types, nulls, empty input, overflow, approximation, and output schema.
2. Specify versioned state, identity, update/lift, merge, finalize, serialization, algebraic laws, and compatibility.
3. Choose hash, sort/streaming, connector, partial/intermediate/final stages and derive grouping-key distribution/order requirements.
4. Prove every group/state meets at compatible final ownership and every selected input attempt contributes once.
5. Cost combine ratio, state amplification, group count, network, hash/sort, spill, skew, output, and critical path with uncertainty.
6. Bound hash/distinct/order/sketch state, buffers, recursion, files, writers, and tenant resources; define hot-group escape.
7. Commit attempt-scoped state/manifests and recover worker, exchange, connector, spill, and adaptive failure without double-merge.
8. Protect snapshots, security filters, connector trust, sensitive keys/statistics, and approximate-function authorization.
9. Observe estimates, actuals, algebra/state generations, resources, skew, retries, numerical outcomes, fairness, and cost.
10. Property/differential/metamorphic test partitions and merge trees, fault-inject distributed states, canary, and roll back.

Associativity and identity allow parenthesization and empty-partition changes without altering abstract state. If arbitrary execution reorders states, commutativity or a canonical merge order is additionally required. Finite-precision implementations may only satisfy a documented numerical tolerance.

Average-of-averages fails because it discards partition counts. Merging `(sum,count)` retains sufficient information, so final division weights every contributing row once when attempts are selected exactly once.

Local partial aggregation reduces exchange only when state output is smaller than raw projected input. Correctness can hold with no reduction; cost evidence determines whether the optional stage is worthwhile.

## Alternatives and Trade-Offs

- **Single final aggregation:** simple state semantics; moves all raw rows and creates large fan-in.
- **Partial plus final:** can reduce exchange dramatically; adds CPU, memory, state serialization, and another operator.
- **Tree aggregation:** bounds fan-in and uses locality; adds stages and merge-order variability.
- **Hash aggregation:** no input ordering needed; memory grows with groups/state and can spill.
- **Sort/streaming aggregation:** bounded active groups when ordered; sorting may dominate.
- **Connector pushdown:** reduces source traffic; crosses semantic, snapshot, security, and observability boundaries.
- **Exact distinct set:** exact answers; unbounded cardinality and spill risk.
- **Approximate sketch:** compact mergeable state; explicit error and compatibility contract.
- **Many final partitions:** more parallelism; more exchange/tasks and hot keys remain hot.
- **Hot-group subpartitioning:** spreads update work; adds replication/extra merge and may not reduce final state.
- **Floating parallel merge:** scalable; low bits can depend on merge tree.
- **Canonical merge order:** more reproducible; coordination/sort can cost latency.
- **Aggressive partial aggregation:** saves network on repeated keys; wastes resources on unique keys.
- **Adaptive bypass:** responds to actual combine ratio; needs safe boundaries and stable state semantics.
- **Materialized states:** narrow retries and enable adaptation; add I/O, manifests, and cleanup.
- **Pipelined states:** lower latency; couple attempt/recovery boundaries.

## Failure Modes and Misconceptions

- **“Final values are mergeable states.”** average, variance, and many user-defined results disprove this.
- **“Average partial averages.”** unequal contributing counts require sum/count weighting.
- **“Identity is a normal value.”** min/max need an explicit unseen state.
- **“All aggregates return null on empty.”** count commonly returns zero.
- **“Null grouping keys disappear.”** grouping and ordinary join equality have different null behavior.
- **“Partial aggregation always saves network.”** unique groups can expand bytes.
- **“Hash input bytes predict memory.”** keys, buckets, state, alignment, and distinct/order data amplify it.
- **“Spill makes state bounded automatically.”** writers, files, queues, recursion, and one hot group still need limits.
- **“More partitions split a hot group.”** compatible grouping keeps one key together unless a mergeable subplan is added.
- **“Floating addition is associative.”** merge order changes rounding.
- **“Exact distinct is just count.”** global deduplication scope and nulls matter.
- **“A sketch can merge with any sketch.”** algorithm, precision, seed/hash, type, and version must match.
- **“Bloom-like approximation can replace exact.”** approximation requires an explicit function contract.
- **“Order-sensitive means arrival order.”** distributed arrival is nondeterministic without a property.
- **“Connector aggregate is equivalent.”** snapshots, filters, nulls, collation, types, overflow, and security can differ.
- **“Retrying partials is harmless.”** merging original and retry state double-counts.
- **“Low combine ratio proves success.”** CPU, memory, spill, skew, and critical path may regress.
- **“Same result once proves algebra.”** random partitionings, merge trees, failures, and edge data are required.

## Worked Examples

### Example 1

Partitions contain two and eight contributing values with local means 10 and 20. Averaging means gives 15, but the true mean is `(2*10+8*20)/10=18`. Merge `(sum,count)` states instead of finalized means.

### Example 2

An empty global input produces one row: `COUNT(*)=0`, while `SUM(x)` is null under common SQL semantics. Empty grouped input with `GROUP BY k` produces no rows. Final-stage synthesis distinguishes the cases.

### Example 3

Rows with null grouping key form one group, even though an ordinary equality join would not match null keys. The hash grouping contract uses grouping “not distinct” semantics and retains an explicit null-key bucket.

### Example 4

Each of 100 scan tasks reads one million rows over 1,000 repeated keys and emits at most 1,000 sum/count states. Partial aggregation greatly reduces shuffle. If each row has a unique UUID, it emits nearly one million larger states per task and may be disabled adaptively.

### Example 5

A decimal sum exceeds the input precision during partial accumulation but the final result type expects widened precision. Accumulating in the narrow input type can overflow before other partitions merge. State schema uses the required widened type and uniform overflow rule.

### Example 6

Grace aggregation repartitions spilled states, but one key owns a 30 GiB ordered list. Rehashing cannot divide one final group. The plan needs a mergeable run representation, an approximate/bounded function chosen explicitly, more capable execution, or rejection.

### Example 7

`COUNT(DISTINCT user_id)` locally deduplicates, but the same user appears in many source tasks. Summing local counts overcounts. Exchange/deduplicate values under a global ownership plan before counting.

### Example 8

A Bloom-style or cardinality sketch built with precision 12 cannot be merged silently with precision 14 under an unspecified implementation. The state header validates algorithm, version, precision, seed, and type before merge.

### Example 9

A speculative partial task produces the same logical input partition twice. The exchange manifest selects one complete attempt. Final aggregation consumes only selected states, preventing counts and sums from doubling.

### Example 10

The fixture merges `(sum,count)` states across uneven partitions while ignoring null values.

<!-- bijux-verify: {"id":"mergeable-average-state","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"partial_states=((4, 2), (12, 2), (12, 1))\nmerged_state=(28, 5)\nfinal_average=5.6\n","stderr":""}} -->
```python
partitions = ((1, None, 3), (4, 8), (12, None))

def partial(values):
    contributing = [value for value in values if value is not None]
    return sum(contributing), len(contributing)

states = tuple(partial(values) for values in partitions)
merged = (sum(state[0] for state in states), sum(state[1] for state in states))
average = merged[0] / merged[1] if merged[1] else None

print(f"partial_states={states}")
print(f"merged_state={merged}")
print(f"final_average={average}")
```

Production average additionally specifies numeric widening, decimal/float behavior, overflow, state versions, selected attempts, and the exact empty-result contract.

## Cross-Program Connections

- **Abstract algebra:** identity, associativity, commutativity, homomorphisms, and sufficient statistics explain decomposition.
- **Algorithms:** hashing, sorting, external partitioning, merge trees, sketches, sampling, and heavy hitters shape execution.
- **Database systems:** bags, nulls, filters, distinct, grouping sets, ordered aggregates, types, and snapshots define semantics.
- **Distributed systems:** exchange ownership, attempts, manifests, retries, epochs, backpressure, and partial failure define correctness.
- **Data engineering:** shuffle reduction, skew, spill, object storage, schema evolution, and large groups determine cost.
- **Platform engineering:** worker memory, disk, network, scheduling, isolation, autoscaling, and telemetry constrain plans.
- **Reliability engineering:** numeric guards, spill integrity, attempt selection, adaptive fallback, canary, and rollback bound risk.
- **Security and governance:** grouping keys, cardinalities, connector delegation, approximation approval, retention, and audit protect data.

## References

1. Trino. [Aggregate Functions.](https://trino.io/docs/current/functions/aggregate.html) Current aggregate, null, ordering, filtering, map/array, approximate, and statistical function behavior.
2. Trino. [Optimizer Properties.](https://trino.io/docs/current/admin/properties-optimizer.html) Current partial aggregation, distinct strategies, pushdown, partitioning, and optimizer controls.
3. Trino. [Pushdown.](https://trino.io/docs/current/optimizer/pushdown.html) Current aggregate, projection, predicate, join, limit, top-N, and dereference connector-pushdown concepts.
4. Apache Spark. [Built-in Aggregate Functions.](https://spark.apache.org/docs/latest/sql-ref-functions-builtin.html#aggregate-functions) Current exact, approximate, statistical, collection, ordering, and null-related aggregate functions.
5. Apache Spark. [SQL Performance Tuning.](https://spark.apache.org/docs/latest/sql-performance-tuning.html) Current statistics, partitioning, adaptive coalescing, and skew behavior relevant to aggregate stages.
6. PostgreSQL. [Aggregate Functions.](https://www.postgresql.org/docs/current/functions-aggregate.html) Current general-purpose, statistical, ordered-set, grouping, partial-mode, null, and empty-input behavior.
7. PostgreSQL. [Using EXPLAIN.](https://www.postgresql.org/docs/current/using-explain.html) Current aggregate, group, sort, hash, estimated/actual row, memory, and execution-plan evidence.
8. Apache Calcite. [Relational Algebra.](https://calcite.apache.org/docs/algebra.html) Current aggregate calls, grouping sets, filters, distinct, collation, and planner-expression concepts.
9. Apache DataFusion. [EXPLAIN Usage.](https://datafusion.apache.org/user-guide/explain-usage.html) Current logical/physical aggregate plans, repartitioning, optimizer passes, statistics, and metrics.
10. DuckDB. [Aggregate Functions.](https://duckdb.org/docs/stable/sql/functions/aggregates.html) Current distinct, ordering, filter, null, empty-group, numeric, and collection aggregate semantics.
11. Shute et al. [F1 Query: Declarative Querying at Scale.](https://research.google/pubs/f1-query-declarative-querying-at-scale/) Primary account of distributed aggregation, operators, repartitioning, sorting, and production execution.
12. Melnik et al. [Dremel: Interactive Analysis of Web-Scale Datasets.](https://research.google/pubs/dremel-interactive-analysis-of-web-scale-datasets-2/) Primary account of serving-tree aggregation over distributed columnar data.
13. Dean and Ghemawat. [MapReduce: Simplified Data Processing on Large Clusters.](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/) Primary map/combine/shuffle/reduce and fault-tolerance account relevant to partial aggregation.

## Exercises

### Exercise 1

Define mergeable states and empty/null behavior for `COUNT(*)`, `COUNT(x)`, `SUM(x)`, `AVG(x)`, `MIN(x)`, and population variance. State numeric assumptions.

### Exercise 2

Design a distributed plan for `SELECT region, COUNT(DISTINCT user_id) FROM T GROUP BY region`. Cover local deduplication, exchange ownership, global deduplication, final count, nulls, spill, and attempts.

### Exercise 3

Compare partial hash, sort/streaming, and connector-pushed aggregation for 10 billion rows with either 1,000 groups or 9 billion groups. Include combine ratio, state, network, spill, trust, and adaptation.

### Exercise 4

Design hot-group handling for an ordered `array_agg` whose largest group contains 500 million values. Cover order, runs, subpartitioning, final merge, bounds, failure, and policy.

### Exercise 5

Design a validation campaign for a new partial-aggregation engine supporting decimals, variance, distinct, sketches, grouping sets, connector pushdown, retries, and adaptive bypass.

## Answers to the Exercises

### Answer 1

`COUNT(*)` state is a wide integer initialized zero, incremented per row, merged by checked addition, finalized zero on empty. `COUNT(x)` increments only non-null `x`. `SUM(x)` keeps an explicit seen flag plus widened numeric sum; merge combines seen states and checked sums, finalizing null if unseen. `AVG(x)` uses widened `(sum,count-non-null)` and finalizes null at count zero. `MIN(x)` keeps `(seen,value)`, ignores nulls, merges by compatible comparison, and returns null unseen. Population variance can use `(n,mean,M2)` with a stable parallel merge and returns the dialect-defined result for zero count. State numeric types, decimal scale, overflow, NaN/infinity, floating merge-order tolerance, and result conversion must be explicit.

### Answer 2

Filter/project `region,user_id`; exclude null `user_id` from `COUNT(DISTINCT)` while retaining null `region` as a group. Each scan task locally deduplicates `(region,user_id)` under compatible grouping/distinct semantics. Hash-exchange that pair so all copies of the same pair meet, then globally deduplicate. Either repartition resulting unique pairs by `region` and count them, or choose ownership that permits a hierarchical count without duplicates. Spill exact sets or sorted runs with schema/hash/attempt manifests and bounded files. Select one attempt per logical input/partition before merging. Finalize count zero only for groups that exist; an empty grouped input emits no rows.

### Answer 3

With 1,000 repeated groups, partial hash aggregation can reduce billions of rows to roughly 1,000 states per source task, usually saving enormous network at manageable state. Ordered input may make streaming aggregation even smaller in memory; sorting solely for it may not pay. Connector pushdown can eliminate source transfer if its snapshot, types, nulls, overflow, grouping, filters, and security match. With 9 billion groups, partial hash state approaches input cardinality and may expand bytes/spill; sort/external streaming offers more predictable memory but major I/O, while connector pushdown may merely move the same state burden. Measure sampled/runtime group count, state bytes, combine ratios, CPU, spill, network, and tail. Adaptively bypass optional local combining or switch hash to spill/sort at a safe state-compatible boundary.

### Answer 4

An ordered array is holistic in output size and cannot fit as one in-memory state. Preserve the complete order key plus deterministic tie policy, project only needed payload, create sorted spill runs per source/subpartition with checksums and selected attempts, and range- or hash-route the hot group under a dedicated plan. Subpartitions sort chunks; a bounded multiway final merge produces global order and streams/spools the array representation if the result type/protocol permits. If final materialization requires more than governed limits, reject or require an explicitly bounded/approximate alternative. Retain runs across worker retry, select one attempt, bound open files/fan-in/storage, encrypt sensitive values, and test cancellation/cleanup without deleting recovery inputs.

### Answer 5

Property-test identity, update/merge/finalize equivalence across random partitions and merge trees, using tolerances only for declared floating results. Differentially compare single-stage and staged execution over empty/all-null, duplicates, composite/null groups, extreme decimals/overflow, cancellation-prone variance, exact distinct, incompatible sketches, grouping-set placeholders, filters, and ordered inputs. Compare connector pushdown with engine evaluation under snapshots, security, time zones, collations, and failures. Inject duplicate attempts, worker loss, stale epochs, spill full/corruption, state-version mismatch, and adaptive restart. Assert one selected contribution, bounded memory/files/retries, exact results or declared sketch error, and no policy leakage. Measure combine ratios, CPU, memory, spill, network, tails, fairness, and cost; shadow plans, canary bounded workloads, freeze on semantic/security/bound regression, and roll back state/plan generations while retaining needed manifests.
