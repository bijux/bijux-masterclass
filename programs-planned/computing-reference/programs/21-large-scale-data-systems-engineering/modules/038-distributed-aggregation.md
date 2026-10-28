---
module_id: LSDS-038
program: Large-Scale Data Systems Engineering
level: 1
module_number: 38
title: Distributed Aggregation
status: complete
last_verified: 2026-09-03
---

# Distributed Aggregation

## One-Page Review

### Governing question

How can a distributed engine reduce records into exact or explicitly approximate group results using local, intermediate, and final states while preserving algebra, null and empty semantics, bounded resources, deterministic expectations, retry safety, and policy compliance?

### Essential definitions

- An **aggregate** maps a multiset or ordered sequence of inputs to a smaller result such as count, sum, mean, minimum, set, sketch, or collection.
- A **group key** identifies the records whose aggregate state must be combined.
- An **accumulator state** is the mergeable intermediate representation, which may differ from both input and output types.
- `add(state, value)` incorporates one input; `merge(left, right)` combines partial states; `finalize(state)` produces the user-visible result.
- A **local aggregate** or **combiner** summarizes records before shuffle; an **intermediate aggregate** merges partials in a tree; a **final aggregate** produces one result per group.
- A **decomposable aggregate** has sufficient partial state and a merge operation that reproduce the single-stage semantics under allowed regrouping.
- A **monoid** is a set with an associative binary operation and identity; commutativity is additionally needed when input/partial order is unconstrained.
- A **hash aggregate** stores group states in a hash table; a **sort aggregate** consumes rows ordered by group key and finalizes contiguous groups.
- A **distinct aggregate** tracks unique argument tuples exactly or with an explicitly approximate sketch.
- **reduction ratio** compares shuffled partial states with original input records or bytes; it can be negative when states are larger than inputs.

### Central model, mechanism, or theorem

Let input group $X$ be divided arbitrarily into chunks $X_1,\ldots,X_t$. A distributed aggregate is correct when each chunk produces a sufficient state $s_i$, `merge` combines states associatively (and commutatively when scheduling may reorder them), identity represents no inputs, and $finalize(merge(s_1,\ldots,s_t))$ equals the specified aggregate over $X$. This is a homomorphism from allowed input composition into accumulator composition.

Mean is not safely combined by averaging averages. Its state is `(sum,count)`; merge adds both fields and finalize divides when count is nonzero. Exact variance can use a mergeable state such as `(count,mean,M2)` with a numerically reviewed parallel merge. Exact distinct uses set union and may be as large as the input; approximate sketches trade a stated error/confidence model for bounded state.

If $N$ input records become $C$ local partial states of average serialized sizes $v$ and $s$, input-to-shuffle byte ratio is $Cs/(Nv)$. Combining saves network only when it is below one after keys, headers, codecs, spill, and retries. A hot key can shrink to one partial per producer for an associative aggregate yet still serialize final merge work; high cardinality can create nearly one state per input and make hash memory dominant.

### Critical invariants

- Group key normalization, equality, hash/partition function, null grouping, collation, schema, and version are pinned.
- Accumulator schema, identity, `add`, `merge`, `finalize`, serialization, and code version are compatible across all stages.
- Partial grouping and merge preserve the specified aggregate for every permitted partitioning and merge tree.
- No mutable identity or accumulator object is accidentally shared across groups, tasks, or attempts.
- Null, empty-input, filter, distinct, ordering, overflow, NaN, and error semantics match the declared API.
- Each accepted input contributes exactly once logically; failed/speculative partials cannot double-count.
- Hash tables, sort runs, distinct sets/sketches, intermediate trees, output, spill, and concurrent tasks are bounded and admitted.
- Approximate outputs identify algorithm/version/parameters and carry their actual error semantics; they are never labeled exact.
- Nondeterministic or order-sensitive aggregates declare and enforce order, tie-breaking, and replay behavior.
- Partial state and results obey tenant, region, confidentiality, retention, deletion, and audit rules.

### Common failures

Common failures include averaging mapper averages; using subtraction or string concatenation with arbitrary reduction order; assuming a combiner runs exactly once; using a non-neutral zero; sharing a mutable zero across keys; merging accumulator versions; overflowing a narrow partial sum; assuming floating-point addition is associative; counting nulls incorrectly; returning zero where SQL requires null on an empty value set; treating `DISTINCT` as a cheap flag; moving full value lists instead of sufficient states; using one output partition for millions of groups; trusting average state size under a giant group; retrying a partial without winner fencing; claiming deterministic results from arbitrary merge order; pushing aggregation into an untrusted connector without semantic proof; and publishing raw group keys in metrics.

### Compact example

Eight input rows across three producer partitions become five `(sum,count,nulls)` local states. Shuffling states rather than rows reduces record count by $1-5/8=37.5\%$ in this toy case. Merging produces `a=(60,3,1)`, `b=(45,3,0)`, and `c=(0,0,1)`; final means are 20, 15, and null. The state distinguishes an all-null group from a nonempty numeric group and never averages partial averages.

### Connections

[LSDS-023](023-partitioners-and-combiners.md) introduces safe combining, [LSDS-027](027-task-retry-and-speculation.md) supplies attempt identity, [LSDS-031](031-shuffle-architecture.md) through [LSDS-034](034-hash-based-shuffle.md) define exchange and spill, and [LSDS-036](036-repartition-joins.md) supplies key co-location. [LSDS-039](../ROADMAP.md) develops heavy-hitter handling and [LSDS-040](../ROADMAP.md) integrates wide-operation cost reduction.

## Governing Question

Aggregation looks like a simple reduction: group equal keys and fold their values. At cluster scale, the engine wants to reduce data early, merge partial results in parallel, repartition only compact state, spill when cardinality grows, and recover failed work without recounting. Every optimization changes grouping and merge order, so the aggregate's algebra becomes an execution contract.

Some functions decompose naturally. Counts and integer sums merge by addition. Minimum merges by minimum. Mean needs sum and count. Variance needs more state and careful numerical formulas. Median cannot be recovered from partial medians; exact computation must preserve enough ordered values, while approximate quantile sketches declare error.

SQL semantics add edges. `count(*)` includes rows while `count(x)` excludes null `x`. Many sums/means ignore nulls and produce null when no non-null value exists. A global aggregate over empty input may still produce one output row, while grouped aggregation produces no absent groups. Filters, `DISTINCT`, ordered collection aggregates, and grouping sets change state and output.

Execution has two main local organizations. Hash aggregation updates an in-memory table and spills/partitions when state grows. Sort aggregation clusters equal keys and can stream one group at a time, but sorting and giant ordered/collection states still cost. Both can use local/intermediate combine only when accumulator laws permit.

The governing question is how to specify sufficient state and merge laws, choose a physical organization and stage tree from real cardinality/skew/state sizes, and maintain exact contribution and semantic identity across retries, pushdown, approximation, and policy boundaries.

## Why This Matters

Effective partial aggregation can turn terabytes of events into megabytes of per-key states before the network. It reduces shuffle records, serialization, blocks, reducer input, and downstream memory. Tree aggregation avoids one coordinator ingesting every partial and exposes parallelism for global results.

Unsafe combining silently changes answers. Averaging averages weights partitions rather than rows. A combiner that drops duplicate values breaks counts. A mutable accumulator shared between keys contaminates groups. A retry whose partial is accepted twice doubles sums. These defects often survive small tests because local execution happens to choose one order.

Cardinality controls the economic result. If every row has a unique key, local aggregation creates one state per row plus hash overhead. Complex states—sets, maps, arrays, sketches, top-k heaps—may exceed input size. Hot keys reduce network well for sums but can concentrate CPU or produce giant collection state.

Numerical reproducibility is subtle. Integer arithmetic can overflow. Floating-point addition changes under reassociation, so valid parallel trees can return slightly different low bits. Stable/reproducible summation needs an explicit stronger algorithm, deterministic merge tree, higher precision, compensation, or a documented tolerance.

Aggregates also concentrate information. A per-person total, distinct set, or rare-key count can be more sensitive than one source row. Partial states, sketches, spill, logs, and metrics require the same governance rigor as final output.

## Prerequisites and Retrieval

Retrieve partitioning, serialization, failures, and scale accounting from [LSDS-002](002-horizontal-partitioning.md) through [LSDS-010](010-reasoning-about-work-movement-and-state-at-scale.md). Retrieve storage integrity and metadata from [LSDS-011](011-distributed-block-storage.md) through [LSDS-018](018-consistency-of-listings-and-metadata.md).

Review partitioner/combiner algebra in [LSDS-023](023-partitioners-and-combiners.md), lazy planning and attempt identity in [LSDS-025](025-lazy-evaluation-and-plan-construction.md) through [LSDS-030](030-tracing-a-batch-job-through-a-cluster-engine.md), and shuffle/hash/sort mechanics in [LSDS-031](031-shuffle-architecture.md) through [LSDS-037](037-distributed-sort-merge-joins.md). You should understand multisets, associative/commutative operations, identities, hash tables, external sorting, nulls, numerical precision, sketches, checksums, retries, and transactional output.

## Learning Objectives

After this module, you should be able to:

1. define input, accumulator, merge, and output types for a distributed aggregate;
2. prove when local/intermediate combining is valid under arbitrary partition and merge trees;
3. construct sufficient states for count, sum, mean, variance, minimum/maximum, distinct, and ordered aggregates;
4. distinguish associative, commutative, idempotent, order-sensitive, exact, and approximate contracts;
5. estimate row/byte reduction and recognize high-cardinality or large-state regressions;
6. compare hash, sort, one-stage, two-stage, tree, pushdown, and skew-split aggregation;
7. preserve null, empty, filter, distinct, overflow, NaN, and ordering semantics;
8. fence partial states and final output through retry, speculation, and adaptive execution;
9. validate algebra, multiplicity, numerical error, resources, and failure behavior; and
10. govern group keys, states, sketches, spill, metrics, and results through their lifecycle.

## Core Exposition

### Specify the aggregate as a state machine

Define accumulator state type $S$, identity constructor `zero()`, input transition $add:S\times V\to S$, state merge $merge:S\times S\to S$, and result extraction $finalize:S\to O$. Include serialization schema and code version. The zero constructor returns a fresh state per group.

This interface separates input values from mergeable summaries. A mean state `(sum,count)` accepts one value, merges componentwise, and finalizes only when count is positive. A top-k state is a bounded heap with ordering/tie rules. A collection aggregate may be an ordered list and cannot be freely merged without order metadata.

State must be sufficient: two input subsets producing the same state must be interchangeable for all future merges and finalization. Partial medians fail this test because subset sizes and distributions lost by the median affect the global median.

### Prove algebra before enabling combination

Associativity requires $merge(merge(a,b),c)=merge(a,merge(b,c))$ in the aggregate's semantic domain. Identity requires merging an empty state changes nothing. When runtime may permute partials, commutativity requires $merge(a,b)=merge(b,a)$.

These are semantic equalities, not necessarily byte equality. Floating-point sums violate exact associativity. List concatenation is associative but not commutative; it is safe only if the framework preserves a declared total partial order. Subtraction is neither suitable for arbitrary reassociation nor permutation.

Idempotence, $merge(s,s)=s$, is different. Set union is idempotent; sum is not. Do not use idempotence as a substitute for accepted-attempt fencing because most useful aggregates count multiplicity.

### Local, intermediate, and final stages

A local stage updates one state per group within a producer partition. It emits partial states. Partitioning those states by group key co-locates them at final destinations. One or more intermediate stages combine states in a tree before finalization.

The runtime may call local combine zero, one, or many times depending on spill, partition size, and optimization. Correctness cannot depend on a fixed invocation count. It may merge states in different shapes after retry or adaptive coalescing.

Two-stage aggregation reduces network when groups repeat locally. Tree aggregation reduces fan-in for global or low-cardinality groups. Each additional stage adds serialization, tasks, metadata, latency, and opportunities for version mismatch.

### Count and sum semantics

Count state is an integer with identity zero and merge addition. Define whether it counts rows, non-null expressions, predicate-true rows, or distinct values. Use a width that cannot overflow allowed input scale, or detect overflow according to declared behavior.

Integer sum similarly needs overflow policy: wider accumulator, arbitrary precision, checked failure, or specified wrap/saturation if the API permits. Decimal sum must preserve precision/scale rules. Boolean counts are not interchangeable with truth-valued three-state logic unless null handling is explicit.

Sum over no non-null inputs may finalize to null under SQL semantics even though the internal numeric identity is zero. Carry a `seen` or count field so identity for merging is not confused with user-visible empty result.

### Mean and weighted mean

For ordinary mean, state `(sum,count)` adds non-null values and merges both components. Finalize returns `sum/count` or the specified empty result. Averaging partial means fails when chunk counts differ: means 0 from one row and 100 from nine rows average to 50, but the correct mean is 90.

Weighted mean state `(weighted_sum,weight_sum)` requires rules for null, negative, zero, infinite, and NaN weights. Final division occurs once. If products overflow or lose precision, use reviewed numeric types/algorithms.

Retain count separately even when a partial mean is stored for numerical stability. Merge formulas must weight by counts, not assume equal partitions.

### Variance and higher moments

Naive state `(sum,sum_squares,count)` can suffer catastrophic cancellation when values are large and variance is small. A mergeable state `(n,mean,M2)` can combine two states with $\delta=mean_b-mean_a$, $n=n_a+n_b$, new mean $mean_a+\delta n_b/n$, and

$$M2=M2_a+M2_b+\delta^2n_an_b/n.$$

Finalize divides by $n$ or $n-1$ for population or sample variance as specified. Handle empty/singleton states, overflow, infinities, NaNs, and rounding. Parallel reassociation still affects floating-point bits; test error bounds against high-precision references.

Higher moments and covariance need reviewed merge formulas, not independent averaging of finalized statistics. Version the state schema/formula.

### Minimum, maximum, and arg aggregates

Minimum and maximum merge naturally under a total comparison and an empty sentinel represented outside the value domain. Null/NaN/collation rules determine comparisons. A fabricated maximum-value sentinel can collide with legitimate input.

`arg_min`, `arg_max`, “first,” and “last” require tie semantics. Returning any associated value may be nondeterministic. Stable behavior needs a total tie-break key such as event time plus durable record identity, with explicit null ordering.

The comparator version is part of state identity. Merging locale-sensitive minima produced under different collation libraries can be invalid.

### Exact distinct aggregation

Exact distinct state is conceptually a set of normalized argument tuples; merge is set union. It is associative, commutative, and idempotent, but memory grows with distinct cardinality. Composite tuple encoding, null inclusion, equality, collation, NaN, and type coercion must match query semantics.

Local sets reduce duplicates but may not reduce high-cardinality input. Shuffle can repartition distinct values, deduplicate, then count or feed multiple final aggregates. Multiple distinct argument sets may need separate subplans, markers, or preaggregation.

Spill exact sets through sorted runs or hash partitions. Bloom filters cannot prove exact distinctness because false positives would omit values.

### Approximate sketches

Approximate distinct, quantiles, heavy hitters, and moments can use bounded mergeable sketches. State identity includes algorithm, version, precision, seed, normalization, and serialization. Only compatible sketches merge.

Publish error semantics: relative standard error, rank error, confidence, deterministic bounds, or empirical calibration as applicable. A requested parameter may translate into non-obvious memory. Validate actual implementation claims from primary specifications.

Approximation can introduce privacy concerns: sketches can leak membership or rare values. Noise for differential privacy is a separate mechanism with budget/composition/accounting, not an incidental benefit of approximation.

### Ordered and holistic aggregates

`array_agg`, string concatenation, first/last, exact percentile, and user code may depend on order or require all values. If the API exposes `ORDER BY` within the aggregate, states need sorted runs, mergeable order indexes, and deterministic tie-breaking as required.

Without declared ordering, an “arbitrary” result must be documented as such. Do not promise stable output based on current task completion order. An ordered aggregate can still combine by merging sorted partial sequences, but its state may remain as large as input.

Holistic functions that lack bounded sufficient state may group/spill all values or use an explicit approximation. Calling them “non-combinable” means no known state under the required size/semantics, not that distributed execution is impossible.

### Hash aggregation

Hash aggregation maps normalized keys to accumulator states. It offers expected constant-time updates and no comparison sort. Memory grows with distinct groups times state/entry overhead, plus hash buckets, keys, allocators, codecs, and spill buffers.

When memory pressure rises, spill hash partitions or partial states. A later stage reads and merges them. Recursive partitioning needs bounded fan-out and protection against hot keys or adversarial hashes. State mutation must not continue after ownership transfers to an asynchronous spill.

Collision resolution compares full normalized keys. Hash equality alone cannot group. Stable hash/seed/version are required across partitioning stages; local table placement can use a private hash if grouping equality remains correct and persisted identity is clear.

### Sort aggregation

Sort aggregation orders records or partial states by group key, then maintains one current group. It can operate with bounded group state after external sort and uses sequential I/O. Existing compatible order may eliminate sorting.

Sorting is helpful when cardinality makes hash state large or downstream needs order. It adds comparison and merge passes. Individual aggregate state may still be huge: exact distinct sets, collections, or one pathological UDAF need spill-aware representations.

Combining during sorted-run generation can collapse adjacent equal keys. Run merge can aggregate equal keys rather than emit them all, provided algebra and state versions match.

### Reduction ratio and state economics

Count both records and bytes. If $N$ rows of average $v$ bytes become $C$ states of average $s$ bytes, shuffled payload ratio is $Cs/(Nv)$. State keys, headers, indexes, checksums, compression, encryption, and block fragmentation change physical totals.

Low-cardinality repeated keys often yield strong reduction. High cardinality makes $C\approx N$. A 20-byte row transformed into a 2 KiB sketch is a regression until many rows share each state. Measure state expansion and spill.

Track local input rows/bytes, groups, states emitted, combine depth, state bytes, shuffle bytes, merge fan-in, final groups, and output. Report distributions by task/partition, not only totals.

### Partition count and skew

Final states for equal keys must co-locate. Too few partitions create large tables/sorts and idle workers. Too many multiply tasks, buffers, files, and metadata. Existing partitioning can be reused only under the exact group-key contract.

A hot key becomes one final state merge. For sums, tree combination reduces values to one partial per subtree and distributes CPU before the root. The root still receives partials but far fewer than raw records. For non-combinable collections, the full hot group remains.

High cardinality can be spread across more output partitions. Low cardinality may limit final-stage parallelism; adding a temporary salt and a second merge is valid only for decomposable aggregates.

### Null, empty, filter, and grouping semantics

Pin whether null group keys form one group; SQL grouping commonly treats them together even though ordinary equality comparisons yield unknown. Aggregate arguments may independently ignore or include null. `count(*)`, `count(x)`, `sum(x)`, and collection functions differ.

Filters apply before `add`. Distinguish a group with rows whose values all filter out from a group absent from input, especially under grouping sets or outer joins. A global no-key aggregate over empty input can require one finalized identity-derived row.

Grouping sets, rollup, and cube make one row contribute to multiple grouping identities. Encode grouping identifiers so a real null key is distinguishable from an aggregate-level placeholder where the SQL contract requires it.

### Floating-point and reproducibility

IEEE floating-point addition is not associative: $(a+b)+c$ can differ from $a+(b+c)$. Distributed sum/mean/variance results can vary with partitioning, spill, retry, or tree shape while remaining within an accepted numeric contract.

If bitwise reproducibility is required, define a deterministic ordering/tree and platform arithmetic, or use exact/superaccumulator methods. Compensated summation can improve accuracy but its merge also needs review. Higher precision may be a practical trade.

Test against exact/high-precision references over cancellation, extreme magnitude, subnormal, infinity, NaN, and signed-zero cases. State tolerances in absolute/relative/ULP terms appropriate to the API.

### User-defined aggregates

UDAFs declare input/state/output schemas, null behavior, algebra, determinism, resource bounds, serialization/version migration, and side-effect policy. `add` and `merge` must not read clocks, randomness, networks, or mutable global state unless semantics explicitly model them.

Never reuse one mutable zero object. Copy-on-write, ownership, and thread safety must be clear. Accumulators crossing language/runtime boundaries need canonical encoding and compatibility tests.

Planner optimizations should be conservative: unsupported split aggregation uses one stage rather than guessing a merge. A hint cannot prove algebra.

### Pushdown and metadata aggregation

A connector may compute aggregation near storage, reducing data movement. Validate function semantics, types, overflow, collation, nulls, filters, distinctness, approximation, snapshot isolation, and error reporting. `EXPLAIN` or plan evidence should reveal the boundary.

Metadata-only answers can be fast but require metadata to represent exactly the rows in scope. Empty/stale partitions, deleted files, uncommitted data, and connector differences can invalidate results. Treat metadata correctness as a premise, not an optimization axiom.

Partial pushdown returns compatible accumulator states or finalized values that the engine combines only under a proved rewrite. Do not merge averages as if they were sums.

### Retry, speculation, and commit

Partial states are attempt-scoped. A reducer consumes one accepted contribution for each logical producer/subtree. Sum/count are not idempotent, so accepting a speculative loser doubles results. A content digest cannot generally deduplicate legitimately identical partial values.

Retries use the same input snapshot, group contract, accumulator version, and plan generation, or the dependent aggregate advances coherently. Partial state serialization includes schema/version and checksums. Unknown versions fail or migrate through reviewed logic.

Final output remains attempt-scoped until one complete set of groups commits. Cancellation fences late spill/merge/output callbacks. Cleanup waits for retry/recovery references and holds.

### Observability

Record aggregate name/version, input/state/output types, algebra classification, exact/approximate parameters, null/empty/filter/order semantics, grouping contract, stage tree, physical algorithm, partition count, and planner confidence.

Measure rows/bytes in, local groups/states, reduction ratio, state-size distribution, hash load/collisions, sort runs, spills, intermediate depth/fan-in, shuffle, hot keys under safe representation, merge/finalize CPU, numerical warnings, output groups/bytes, and backpressure.

Track accepted/failed/speculative attempts, checksum/version rejection, pushdown evidence, approximation/error validation, memory/disk/network high-water marks, and cleanup. Avoid raw keys and unbounded metric labels.

### Validation and fault injection

Property-test algebra across randomized partitions, permutations, tree shapes, empty chunks, repeated merge, and serialization round trips. Compare final results with a trusted single-stage reference. Test identity freshness and accumulator aliasing.

Cover empty/global/grouped input, all-null, null keys, duplicates, filters, distincts, grouping sets, overflows, negative/zero weights, NaNs/infinities, floating cancellation, giant keys/states, high cardinality, and hot groups. Approximate aggregates need statistical/error tests across seeds and distributions.

Inject spill, disk full, corrupt/truncated state, worker loss, retry, speculation, cancellation, mixed state versions, adaptive repartition/tree changes, pushdown mismatch, auth expiry, sink failure, and cleanup races. Assert exact accepted contributions, bounded resources, and no partial commit.

### Security, privacy, and governance

Group keys and states can reveal identities, behavior totals, rare categories, or membership. Minimize input fields and state contents. Do not log raw keys, accumulator payloads, sketch registers, or sample values. Protect statistics and digests according to classification.

Authorize each worker, shuffle service, spill store, connector, and sink; enforce tenant/region purpose boundaries, scoped identity, encryption, integrity, quotas, and audit. Pushdown expands trust to the connector implementation and remote system.

Retention covers partials, intermediate states, distinct sets/sketches, hash/sort spill, checkpoints, losing attempts, logs, caches, results, and keys. Apply holds explicitly and verify deletion/cryptographic erasure. Privacy-preserving aggregates require a defined threat model and formal mechanism, not merely reduced row count.

## Definitions and Notation

- $V,S,O$: input value, accumulator state, and finalized output domains.
- $zero()$: fresh identity-state constructor.
- $add:S\times V\to S$: input transition.
- $merge:S\times S\to S$: compatible partial-state combination.
- $finalize:S\to O$: result extraction with empty/null/error semantics.
- $N,C$: input record count and emitted local partial-state count.
- $v,s$: average serialized input-row and partial-state sizes.
- $Cs/(Nv)$: logical shuffled-byte ratio before physical overhead.
- $(n,mean,M2)$: mergeable variance state.
- **aggregate generation**: immutable grouping, state-schema, function-code, snapshot, and plan identity.

## Mechanisms, Invariants, or Proof Structure

1. Freeze grouping, input multiset/order, null/empty/filter/distinct semantics, types, overflow, approximation, and result contract.
2. Define fresh identity, input transition, sufficient state, merge, finalize, serialization, and version.
3. Prove associativity/identity and commutativity when scheduling can reorder; declare non-idempotence and order sensitivity.
4. Estimate cardinality, repetition, state size, skew, output, and row/byte reduction with uncertainty.
5. Choose local/intermediate/final tree, partitioning, hash/sort/spill, and output partitions.
6. Admit memory, disk, network, descriptors, state expansion, concurrent tasks, and giant/hot paths.
7. Emit immutable attempt-scoped compatible partial states and consume one accepted contribution per logical subtree.
8. Finalize only complete groups under one aggregate generation; commit one output attempt.
9. Validate algebra, numerical semantics, approximation, resources, faults, and connector/pushdown boundaries.
10. Measure estimate error, retain required recovery/audit evidence, and delete after references and holds end.

For a decomposable aggregate, prove by induction over the execution tree. Each leaf state summarizes exactly its input chunk. For an internal node, associativity (and commutativity if children may permute) makes merged state summarize the union of child chunks independent of tree grouping. At the root, finalize produces the specified aggregate. Exact accepted-attempt selection ensures the leaf chunks form the intended input multiset once.

This proof does not establish bitwise floating-point reproducibility, bounded state, or good performance. Those are separate contracts. It also fails for an insufficient state: two chunks with the same partial median can combine with a third chunk to different global medians.

## Alternatives and Trade-Offs

**One-stage aggregation** sends raw values to final groups and supports arbitrary group logic, but maximizes movement and per-group load. **Two-stage local/final aggregation** reduces repeat-heavy inputs but adds state serialization and may regress under high cardinality.

**Tree aggregation** bounds fan-in and exposes parallelism for global/hot combinable groups. More levels add scheduling, latency, and artifacts. **Temporary salting** similarly distributes a natural group only when partial states merge correctly.

**Hash aggregation** avoids sorting and is effective when group states fit or partitioned spill works. **Sort aggregation** handles high cardinality with external order and streams keys, paying sort/merge I/O.

**Exact distinct** preserves all uniqueness information and can be unbounded. **Approximate sketches** bound state but introduce algorithm/version/error/security contracts. **Bloom filters** are not exact distinct accumulators.

**Pushdown** saves source-to-engine traffic but expands semantic/trust boundaries. **Metadata-only aggregation** can be constant-time under exact metadata premises and dangerously wrong when empty/stale partitions exist.

**Deterministic trees or exact numerics** improve reproducibility at CPU, memory, and scheduling cost. **Unordered fast merging** maximizes flexibility while accepting documented numerical variation.

## Failure Modes and Misconceptions

1. **“Any binary function can reduce in parallel.”** Arbitrary regrouping requires reviewed algebra.
2. **“Average the averages.”** Mean partials require counts or equivalent weights.
3. **“The zero value is just a default object.”** It must be neutral and freshly owned for each group.
4. **“Associative means commutative.”** List concatenation is associative but order-sensitive.
5. **“Commutative means retry-safe.”** Sum is commutative yet duplicate acceptance double-counts.
6. **“Floating addition is associative enough for bitwise identity.”** Tree shape changes low-order results.
7. **“Local combine always reduces data.”** High cardinality or large states can expand bytes.
8. **“GroupBy and aggregate cost the same.”** Shipping full value bags loses sufficient-state reduction.
9. **“Distinct is one Boolean.”** Exact distinct state may approach all unique values.
10. **“Approximate means private.”** Sketches can leak membership and need explicit privacy analysis.
11. **“More output partitions split a hot key.”** One natural key still has one final state unless a second merge is designed.
12. **“Hash collision means same group.”** Full normalized equality remains authoritative.
13. **“Internal zero is the empty SQL result.”** `SUM` may finalize all-null/empty as null.
14. **“First and arbitrary are deterministic.”** Ordering/tie/replay contracts are needed.
15. **“A combiner runs exactly once.”** Runtimes may skip, repeat, spill, or tree-combine.
16. **“Identical partial values can be deduplicated.”** Two producers can legitimately emit equal counts/sums.
17. **“Connector pushdown is semantically identical.”** Types, nulls, overflow, collation, snapshot, and approximation must be proven.
18. **“Encryption completes governance.”** Identity, purpose, placement, telemetry, retention, and deletion remain.

## Worked Examples

### Example 1

Chunk A has one value 0 and chunk B has nine values 100. Averaging partial means gives 50; merging `(sum,count)` gives `(900,10)` and correct mean 90.

### Example 2

One million 40-byte rows collapse to 20,000 local states of 80 bytes. Logical bytes fall from 40 MB to 1.6 MB, a ratio 0.04. Headers and compression still need physical measurement.

### Example 3

One million unique 16-byte keys with 8-byte values become roughly one million states carrying key, sum, count, hash entry, and serialization metadata. Local combine can increase memory and shuffled bytes.

### Example 4

Three partial counts `(a,10)` from different accepted producers are legitimate contributions; value-based deduplication would undercount. Attempt identities select winners, not accumulator equality.

### Example 5

Set union is associative, commutative, and idempotent, but exact distinct state for 100 million unique identifiers remains enormous. Algebraic safety does not imply bounded resources.

### Example 6

`array_agg(x ORDER BY timestamp,id)` can merge sorted partial sequences using the same comparator. Plain list concatenation under arbitrary task completion produces a different exposed order.

### Example 7

A global sum over no rows may use internal zero but finalize to null under its SQL contract. `count(*)` finalizes to zero. The accumulator must distinguish these semantics.

### Example 8

A hot key appears on 50,000 producer partitions with millions of rows each. Local sum produces 50,000 partials; a fan-in 10 tree needs about five levels and avoids sending raw values to one task.

### Example 9

A locale upgrade changes which string is minimum. States containing minima from old and new comparator versions are incompatible even if their serialized types match.

### Example 10

This executable fixture performs local and final `(sum,count,nulls)` aggregation without averaging averages.

<!-- bijux-verify: {"id":"distributed-aggregation-states","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"groups=3 input_rows=8 partial_states=5\na sum=60 count=3 nulls=1 mean=20.0\nb sum=45 count=3 nulls=0 mean=15.0\nc sum=0 count=0 nulls=1 mean=null\nshuffle_reduction=37.5%\n","stderr":""}} -->
```python
from collections import defaultdict

partitions = [
    [("a", 10), ("a", None), ("a", 20)],
    [("b", 5), ("b", 15), ("a", 30)],
    [("b", 25), ("c", None)],
]


def fresh_state():
    return {"sum": 0, "count": 0, "nulls": 0}


def add(state, value):
    if value is None:
        state["nulls"] += 1
    else:
        state["sum"] += value
        state["count"] += 1


def merge(left, right):
    return {field: left[field] + right[field] for field in ("sum", "count", "nulls")}


partials = []
for partition in partitions:
    local = defaultdict(fresh_state)
    for key, value in partition:
        add(local[key], value)
    partials.extend(local.items())

final = defaultdict(fresh_state)
for key, state in partials:
    final[key] = merge(final[key], state)

input_rows = sum(len(partition) for partition in partitions)
print(f"groups={len(final)} input_rows={input_rows} partial_states={len(partials)}")
for key in sorted(final):
    state = final[key]
    mean = "null" if state["count"] == 0 else str(state["sum"] / state["count"])
    print(f"{key} sum={state['sum']} count={state['count']} nulls={state['nulls']} mean={mean}")
print(f"shuffle_reduction={100 * (1 - len(partials) / input_rows):.1f}%")
```

The fixture validates state sufficiency, fresh identities, local/final merge, null accounting, and record-count reduction. It is not a distributed runtime, byte-size, spill, floating-point, or performance benchmark.

## Cross-Program Connections

- **Data Structures Engineering:** Hash tables, sets, heaps, sorted runs, sketches, accumulators, and serialization determine state cost.
- **Algorithms Engineering:** Monoids, homomorphisms, tree reductions, numerical stability, randomized sketches, and output-sensitive bounds underpin correctness.
- **Database Systems Engineering:** SQL null/empty semantics, distinct strategies, grouping sets, UDAFs, physical aggregation, and pushdown shape plans.
- **Data Engineering:** Metrics, rollups, deduplication, cube building, partition reuse, and incremental pipelines depend on mergeable state.
- **Distributed Systems Engineering:** Attempt fencing, immutable partials, checksums, lineage, replay, and transactional sinks prevent double counting.
- **Platform Engineering:** Memory/disk/network admission, shuffle, remote services, quotas, observability, and multi-tenant scheduling control reliability.
- **Security Engineering:** Aggregates and sketches concentrate sensitive information and require minimization, access control, privacy analysis, and deletion.
- **Systems Engineering:** Algebra, runtime, storage, network, numerical behavior, governance, and downstream contracts must be optimized together.

## References

1. Apache Spark, [RDD Programming Guide: Key-Value Aggregation and Shuffle](https://spark.apache.org/docs/latest/rdd-programming-guide.html), accessed 2026-09-03.
2. Apache Spark, [PySpark RDD.reduceByKey](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.RDD.reduceByKey.html), accessed 2026-09-03.
3. Apache Spark, [PySpark RDD.aggregateByKey](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.RDD.aggregateByKey.html), accessed 2026-09-03.
4. Apache Spark, [Built-in Aggregate Functions](https://spark.apache.org/docs/latest/sql-ref-functions-builtin.html), accessed 2026-09-03.
5. Apache Spark, [Tuning: Reduce-Task Memory](https://spark.apache.org/docs/latest/tuning.html), accessed 2026-09-03.
6. Apache Flink, [Table Configuration: Aggregate Phase and Mini-Batch](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/table/config/), accessed 2026-09-03.
7. Apache Flink, [AggregatePhaseStrategy API](https://nightlies.apache.org/flink/flink-docs-stable/api/java/org/apache/flink/table/api/config/AggregatePhaseStrategy.html), accessed 2026-09-03.
8. Apache Flink, [Table API and SQL Aggregation](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/table/common/), accessed 2026-09-03.
9. Trino, [Aggregate Functions](https://trino.io/docs/current/functions/aggregate.html), accessed 2026-09-03.
10. Trino, [Optimizer Properties: Distinct Aggregations and Partitioning](https://trino.io/docs/current/admin/properties-optimizer.html), accessed 2026-09-03.
11. Dask, [GroupBy.aggregate](https://docs.dask.org/en/stable/generated/dask.dataframe.api.GroupBy.aggregate.html), accessed 2026-09-03.
12. Apache Beam, [Combine](https://beam.apache.org/documentation/transforms/java/aggregation/combine/), accessed 2026-09-03.

## Exercises

### Exercise 1

Twenty million 32-byte records become 400,000 local partial states of 96 bytes. Compute logical input and partial bytes, byte ratio, and reduction percentage. Explain why record reduction alone would mislead.

### Exercise 2

Prove correctness of mean state `(sum,count)` under arbitrary chunking and merge trees. Give a counterexample to averaging unweighted partial means.

### Exercise 3

Design a mergeable population-variance accumulator using `(n,mean,M2)`. State empty, singleton, floating-point, serialization, and version tests.

### Exercise 4

Classify integer sum, floating sum, set union, list concatenation, exact median, top-k with a total tie-break, and an approximate distinct sketch by associativity, commutativity, idempotence, boundedness, order sensitivity, and exactness.

### Exercise 5

Design validation, admission, retry, and governance for a high-cardinality `COUNT(DISTINCT person_id)` grouped by clinic and month, with connector pushdown and an optional approximate mode.

## Answers to the Exercises

### Answer 1

Input is $20{,}000{,}000\times32=640{,}000{,}000$ bytes. Partials are $400{,}000\times96=38{,}400{,}000$ bytes. Ratio is 0.06 and logical reduction is 94%. The record ratio is 0.02, or 98% reduction, which overstates savings because each state is three times one input record. Physical accounting adds group keys, headers, indexes, checksums, codec/encryption, fragmentation, spill, retry, and possibly different compression.

### Answer 2

Each chunk state stores exact sum $s_i$ and non-null count $n_i$. Componentwise addition is associative and commutative with $(0,0)$ identity, so any accepted merge tree yields $(\sum_i s_i,\sum_i n_i)$, equal to the whole input's sum/count. Finalization divides once when total count is positive and applies the specified empty result otherwise. Counterexample: one chunk contains `[0]` and another contains nine `100`s. Their unweighted partial means average to 50, while $(0+900)/(1+9)=90$.

### Answer 3

Identity is $(0,0,0)$. Adding values uses a stable online update. To merge states $a,b$, handle either empty state, let $n=n_a+n_b$, $\delta=mean_b-mean_a$, $mean=mean_a+\delta n_b/n$, and $M2=M2_a+M2_b+\delta^2n_an_b/n$. Population variance is $M2/n$ for $n>0$; singleton is zero under that definition; empty follows API null/error semantics. Test randomized partitions/trees against high precision, constant and near-constant values, extreme magnitudes, cancellation, NaN/infinity policy, negative roundoff in M2, serialization round trips, cross-language compatibility, schema upgrades, and rejection of mixed versions.

### Answer 4

Exact integer sum is associative/commutative with zero, non-idempotent, constant state, exact absent overflow. Floating sum is not exactly associative and needs a tolerance or stronger method. Set union is associative/commutative/idempotent and exact but unbounded in distinct count. List concatenation is associative, noncommutative, order-sensitive, exact, and unbounded. Exact median has no bounded sufficient partial median; exact state is generally unbounded/orderable. Top-k merge is associative/commutative and bounded when comparator and total tie-break are fixed; it is exact for the declared top-k. A compatible approximate-distinct sketch is bounded and mergeable under its algorithm, usually order-insensitive, but approximate and not automatically private.

### Answer 5

Pin person normalization/equality, clinic/month grouping, null/filter/snapshot semantics, exact versus approximate result contract, and connector trust. For exact mode, measure distinct/state cardinality per group, hash/sort spill, partitions, bytes, hot clinics, disk/network, and concurrent tasks; reject metadata/Bloom substitutes. Validate pushdown with plans and differential canaries for nulls, duplicates, deletes, empty partitions, and snapshot isolation. Fence partials by producer/attempt/generation and commit one complete final set. Approximate mode pins sketch/version/precision/seed, tests stated error over representative/adversarial distributions, and labels output. Minimize identifiers, tokenize where authorized, restrict clinic/region/tenant placement, encrypt, use scoped identity and redacted metrics, audit connector/workers, define privacy threat model, and verify deletion of sets/sketches/spill/partials/caches/logs/keys after recovery needs and holds end.
