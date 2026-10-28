---
module_id: DSE-086
program: Data Structures Engineering
level: 2
module_number: 86
title: Quantile Sketches
status: complete
last_verified: 2026-08-30
---

# Quantile Sketches

## One-Page Review

### Governing question

How can a streaming system approximate ranks and quantiles with bounded memory while stating the error domain, compaction rules, merge semantics, and tail-decision limits precisely?

### Essential definitions

For sorted observations (x_{(1)}\le\cdots\le x_{(n)}), an **inclusive rank** is (R(v)=|\{i:x_i\le v\}|), with normalized rank (r(v)=R(v)/n). A quantile query (Q(q)) asks for a stream value whose rank is near (qn). An **absolute rank-error** contract permits

\[
|R(\widehat Q(q))-qn|\le\varepsilon n
\]

deterministically or with a stated probability. Rank error is not value error: moving one percent in rank can cross an arbitrarily large value gap.

Greenwald–Khanna (GK) stores ordered tuples ((v,g,\Delta)) that bound each retained value's possible rank. KLL stores weighted items in compaction levels and randomizes which items survive; it achieves near-optimal space for probabilistic additive rank error. REQ reallocates accuracy toward one end of the rank domain. A t-digest clusters numeric values into weighted centroids, emphasizing tails and interpolation, with accuracy characterized differently from GK/KLL guarantees.

### Central model, mechanism, or theorem

Quantile sketches delete observations while transferring their represented mass to retained values. The invariant is not “sample looks representative” but a bound on rank uncertainty or a weighted-rank approximation. For GK, tuple gaps bound deterministic rank intervals. For compactor sketches, a retained item at level (ell) represents weight (2^\ell), total retained weight remains (n), and randomized parity makes compaction error analyzable.

### Critical invariants

- Comparator and normalization define one total order consistently across producers.
- Retained weights sum to total accepted observation weight.
- Minimum, maximum, NaN, infinity, and duplicate conventions are explicit.
- Query inclusion semantics—less-than versus less-than-or-equal—are versioned.
- Merge is allowed only for compatible algorithm, accuracy, comparator, item encoding, and weight semantics.
- Rank guarantees, confidence, tail-relative guarantees, and empirical value error are reported separately.
- A sketch does not support arbitrary deletion or sliding-window expiration unless its algorithm explicitly does.

### Common failures

Teams report “one percent accurate” without saying rank or value, compare p99 values from incompatible definitions, discard exact extrema, feed NaNs into a non-total comparator, merge different (k) values without documented behavior, treat t-digest observations as a KLL theorem, assume arbitrary merge order is bitwise reproducible, expand huge weights into repeated updates, or subtract sketches to expire windows.

### Compact example

A deterministic GK teaching fixture inserts 200 distinct integers with (\varepsilon=0.05), retains 15 tuples, and preserves total tuple weight 200. Across 101 queries from (q=0) through (1), maximum observed rank error is 10, exactly (\varepsilon n). Its median estimate has true rank 110 versus target 100. This validates one finite execution, not the general GK proof.

### Connections

[DSE-085](085-hyperloglog.md) supplies sketch compatibility, estimator versioning, and merge-lineage discipline. The roadmap successor is [DSE-087, “k-d Trees”](../ROADMAP.md), which shifts from one-dimensional rank summaries to multidimensional spatial partitioning. Database and Data Engineering use quantile sketches for approximate aggregation, partitioning, telemetry, and service-level analysis.

## Governing Question

How do we select, prove, implement, merge, and operate a quantile sketch whose reported percentile actually matches the application's rank, tail, and failure requirements?

## Why This Matters

Latency, price, size, utilization, and risk distributions rarely fit in memory. Exact sorting costs (O(n)) retained values and substantial distributed shuffle. A quantile sketch processes observations online, retains bounded or slowly growing state, and answers many rank/quantile queries later.

The word “percentile” hides choices. Duplicate values make inverse rank ambiguous. A small rank error can mean a huge value difference in a discontinuous distribution. Tail estimates may need accuracy relative to (1-q), not a uniform absolute rank band. Randomized sketches need a failure probability, and empirical structures need workload evidence. Merging introduces comparator, encoding, parameter, and reduction-tree concerns. Production quality begins with a decision contract, not with a library class name.

## Prerequisites and Retrieval

Retrieve:

- order statistics, cumulative distribution functions, inverse CDFs, and duplicate handling;
- absolute versus relative error, confidence/failure probability, and union bounds;
- weighted samples, binary compaction, merge-and-reduce, and total-order comparators;
- deterministic and probabilistic invariants from prior approximate structures;
- [DSE-085](085-hyperloglog.md) on representation compatibility and estimator migration.

For an exact sorted list, define inclusive normalized rank (r(v)=|\{x_i\le v\}|/n). A repository or API may instead use exclusive rank ( |\{x_i<v\}|/n) or interpolate between values. None is universally “the percentile definition.” The query contract must pin one down, especially with duplicates.

## Learning Objectives

After this chapter, you should be able to:

1. define rank, quantile, duplicates, interpolation, and error direction unambiguously;
2. trace GK tuples and KLL-style weighted compaction;
3. distinguish deterministic, probabilistic, uniform-rank, relative-rank, and empirical guarantees;
4. select among exact, GK, KLL, REQ, t-digest, histogram, and sampling approaches;
5. specify compatible merges, comparator/encoding identity, randomization, and serialization;
6. diagnose tail, value-gap, NaN, weight, window, concurrency, and reduction-tree failures;
7. build verification that combines exact rank oracles, randomized trials, adversarial orders, and operational evidence.

## Core Exposition

### Rank is the error domain

Let (S=(x_1,\ldots,x_n)) be values under a total order. The inclusive natural rank is (R(v)=\sum_i\mathbf1[x_i\le v]). A quantile query takes normalized rank (q\in[0,1]) and returns a value. With duplicates, many ranks may correspond to the same value and one value spans a rank interval. An API must state inclusive or exclusive search, endpoint behavior, and whether returned values are retained observations or interpolations.

An additive rank guarantee says the returned value's rank is within (\varepsilon n) of the target. It says nothing about numeric distance. Consider 990 zeros and 10 values equal to one million. Moving from rank 0.989 to 0.991 crosses nearly the entire value range. Conversely, a large rank interval inside a plateau may have zero value error. Validate the decision in rank space and separately measure value impact on relevant distributions.

### Greenwald–Khanna rank intervals

GK is deterministic for insertion-only ordered streams. It retains sorted tuples ((v_i,g_i,\Delta_i)). Let

\[
r_{\min}(v_i)=\sum_{j\le i}g_j,
\qquad
r_{\max}(v_i)=r_{\min}(v_i)+\Delta_i.
\]

The tuple asserts that the true rank of (v_i) lies within those bounds. Insert places a new value in order with (g=1) and a permitted uncertainty based on current (n). Compression merges adjacent tuple mass only when the resulting uncertainty stays within the (2\varepsilon n) invariant. A query walks cumulative lower ranks and returns a neighboring retained value whose rank interval satisfies the error rule.

The published space bound is (O((1/\varepsilon)\log(\varepsilon n))) in the relevant regime, without knowing final (n) in advance. Implementation details matter: off-by-one choices for floor, insertion uncertainty, endpoint tuples, and inclusive query thresholds must be internally consistent. A code fragment that merely “looks like GK” is not evidence.

### KLL weighted compaction

KLL uses randomized compactors arranged in levels. Level zero receives observations with weight one. When a level exceeds capacity, sort its items, choose a parity, discard every other item, and promote survivors to the next level. Each promoted item has twice the weight. If a pair of weight (w) is represented by one randomly selected member of weight (2w), total represented mass remains unchanged and the rank error contribution has controlled expectation.

At query time, sort retained items with their weights and find where cumulative weight crosses the desired rank. Randomized choices across levels yield a probabilistic error bound. KLL's analysis achieves (O((1/\varepsilon)\log\log(1/\delta))) space for failure probability (\delta), matching the stated lower-bound form. Library parameter (k) is not automatically identical to theorem (\varepsilon); use that library's documented error function.

Compaction makes state sensitive to random choices, update order, and merge tree. Two valid sketches over the same multiset need not be byte-identical or return identical values. Correctness is distributional and invariant-based. Reproducible tests may fix a seed, but production confidence requires many independent seeds and adversarial stream orders.

### Uniform versus tail-relative accuracy

GK and common KLL configurations target a roughly uniform absolute rank allowance. At p99.99, an absolute error of 1% spans most of the tail and may be useless. A **relative rank-error** sketch scales error with distance to a selected end of the rank domain. High-rank accuracy can target error proportional to (1-q); low-rank accuracy targets (q).

REQ-style sketches allocate capacity asymmetrically and provide formal relative-rank behavior under their documented model. A t-digest groups numeric observations into ordered weighted centroids whose permitted mass shrinks near the tails. It often achieves strong empirical tail accuracy and interpolates numerically, but its error contract, scale function, and merge behavior are different from KLL. Choose by required query region and evidence, not by a generic “percentile sketch” label.

### t-digest centroids and interpolation

A centroid stores a mean and weight for nearby values. Compression combines centroids subject to a scale function that limits cluster size as a function of cumulative rank. Small tail centroids preserve extreme resolution; larger central centroids save space. Quantile queries interpolate across centroid locations and weights.

Means are numeric synthetic values, not necessarily observations from the stream. Floating-point summation and merge order can affect centroids. Implementations differ in compression variants, scale functions, sorting discipline, and handling of repeated or ordered data. Size bounds for scale functions do not by themselves prove a universal rank-error bound. Record the exact implementation and characterize accuracy on adversarial as well as representative data.

### Merge semantics

Mergeable sketches must conserve represented mass and reapply their compression rules to the union of retained summaries. Concatenating KLL levels or t-digest centroids without controlled recompression can violate capacity or accuracy. GK's basic online structure does not acquire a correct merge operation merely by concatenating tuple lists; mergeable variants need a separate construction and proof.

Compatibility includes algorithm and format version, (k) or compression parameter, error mode, comparator identity, canonical item encoding, floating-point/NaN policy, weight semantics, randomization protocol, and min/max retention. Some libraries define how different (k) values merge, commonly degrading to a weaker effective accuracy. If that behavior is not documented and tested, reject the merge.

Distributed reduction introduces a second concern: a highly unbalanced tree may repeatedly compact one shard's representation. Randomized sketches can remain within their theorem while results vary by tree. Define whether the contract is statistical equivalence, deterministic bitwise output, or a canonical reduction topology. Store total (n), shard/window lineage, and configuration digest with every summary.

### Values, weights, and ordering

Numeric streams require policies for NaN, positive and negative infinity, and signed zero. IEEE NaN does not participate in an ordinary total order; accepting it without normalization can break sorting invariants. Generic-item sketches require a stable comparator across languages and versions. Locale-sensitive collation is especially risky.

Weighted quantiles treat an observation as having mass (w). Expanding a weight of one billion into repeated updates is not an implementation. A sketch must natively prove weighted operations, or the pipeline must aggregate and use a suitable weighted structure. Negative weights and deletion do not follow from positive weighted support.

Exact minimum and maximum may be retained separately because compaction can discard them. Whether endpoints are exact is an API promise, not a universal property. Similarly, interpolation changes whether the result must be an observed value. These differences affect billing bands, bucket boundaries, and reproducibility.

### Windows, concurrency, and persistence

Most quantile sketches are insertion-only. A sliding window cannot be implemented by subtracting an expired sketch. Use sealed time buckets and merge only live buckets, an exponential histogram, a window-specific algorithm, or exact recomputation. Boundary buckets may need finer granularity or retained raw data.

Concurrent updates mutate buffers, sort, compact, promote, and possibly resize. A single atomic counter does not make those transitions safe. Use owner-thread ingestion, per-worker sketches plus controlled merge, locks, or immutable publication. Snapshot serialization must not observe half a compaction. Crash recovery needs a log or replayable source and an atomic generation/checkpoint protocol.

### Verification

Deterministic algorithms need exact rank-oracle comparison on monotone, reverse, duplicate-heavy, alternating-extreme, and random permutations. Randomized algorithms need many seeds and measurements of bias, normalized rank error, tail error, failure frequency, and simultaneous-query coverage. Merge tests vary shard sizes, overlap, parameters, tree shape, and order. Representation tests cover serialization, endian/comparator identity, sparse or level transitions, extrema, NaNs, infinities, and corruption.

Operational tests tie rank accuracy to decisions: p99 latency SLOs, partition boundaries, pricing thresholds, or anomaly bands. Track retained items/centroids, level occupancy, compaction count, total weight, min/max, merge rejections, configuration versions, and exact sampled error.

The following model implements a bounded GK summary over 200 distinct integers. It uses the tuple invariant and queries 101 normalized ranks against an exact sorted oracle. It does not implement merge, weights, duplicates, concurrency, persistence, or the complete production optimization schedule, and its finite pass does not replace the general GK proof.

<!-- bijux-verify: {"id":"gk-quantile-summary","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"epsilon=0.05\nobservations=200\nretained_tuples=15\ntotal_tuple_weight=200\ntuples_sorted=True\ntuple_bounds_valid=True\nallowed_rank_error=10.0\nchecked_quantiles=101\nmax_observed_rank_error=10.0\nq50=value:113,rank:110,error:10.0\nq90=value:193,rank:185,error:5.0\nq95=value:210,rank:200,error:10.0\nq99=value:210,rank:200,error:2.0\nvalid=True\nevidence=gk_quantile_model\n","stderr":""}} -->
```python
import math

EPSILON = 0.05


def insert(summary, count, value):
    count += 1
    position = 0
    while position < len(summary) and summary[position][0] < value:
        position += 1
    if position == 0 or position == len(summary):
        delta = 0
    else:
        delta = max(0, math.floor(2 * EPSILON * count) - 1)
    summary = (
        summary[:position]
        + [(value, 1, delta)]
        + summary[position:]
    )

    threshold = math.floor(2 * EPSILON * count)
    index = len(summary) - 2
    while index >= 1:
        value_i, gap_i, delta_i = summary[index]
        next_value, next_gap, next_delta = summary[index + 1]
        if gap_i + next_gap + next_delta <= threshold:
            summary = (
                summary[:index]
                + [(next_value, gap_i + next_gap, next_delta)]
                + summary[index + 2:]
            )
        index -= 1
    return summary, count


def query(summary, count, quantile):
    desired_rank = quantile * count
    allowance = EPSILON * count
    minimum_rank = 0
    previous_value = summary[0][0]
    for value, gap, delta in summary:
        minimum_rank += gap
        if minimum_rank + delta > desired_rank + allowance:
            return previous_value
        previous_value = value
    return summary[-1][0]


def exact_rank(sorted_values, value):
    rank = 0
    for item in sorted_values:
        if item <= value:
            rank += 1
    return rank


values = [(index * 73) % 211 for index in range(1, 201)]
exact = sorted(values)
summary = []
count = 0
for value in values:
    summary, count = insert(summary, count, value)

errors = []
for point in range(101):
    quantile = point / 100
    estimate = query(summary, count, quantile)
    errors.append(abs(exact_rank(exact, estimate) - quantile * count))

tuples_sorted = all(
    summary[index][0] <= summary[index + 1][0]
    for index in range(len(summary) - 1)
)
threshold = math.floor(2 * EPSILON * count)
tuple_bounds_valid = all(
    gap + delta <= threshold
    for _, gap, delta in summary[1:-1]
)
total_tuple_weight = sum(gap for _, gap, _ in summary)
maximum_error = max(errors)

print(f"epsilon={EPSILON}")
print(f"observations={count}")
print(f"retained_tuples={len(summary)}")
print(f"total_tuple_weight={total_tuple_weight}")
print(f"tuples_sorted={tuples_sorted}")
print(f"tuple_bounds_valid={tuple_bounds_valid}")
print(f"allowed_rank_error={EPSILON * count:.1f}")
print(f"checked_quantiles={len(errors)}")
print(f"max_observed_rank_error={maximum_error:.1f}")
for label, quantile in (("q50", 0.50), ("q90", 0.90), ("q95", 0.95), ("q99", 0.99)):
    estimate = query(summary, count, quantile)
    rank = exact_rank(exact, estimate)
    error = abs(rank - quantile * count)
    print(f"{label}=value:{estimate},rank:{rank},error:{error:.1f}")
valid = (
    tuples_sorted
    and tuple_bounds_valid
    and total_tuple_weight == count
    and maximum_error <= EPSILON * count
)
print(f"valid={valid}")
print("evidence=gk_quantile_model")
```

## Definitions and Notation

- (n): accepted observation count or total positive weight.
- (R(v)), (r(v)): natural and normalized rank under a declared inclusive/exclusive convention.
- (Q(q)): quantile value requested at normalized rank (q).
- (\varepsilon): rank-error parameter; (\delta): failure-probability parameter where applicable.
- ((v,g,\Delta)): GK retained value, minimum rank gap, and additional rank uncertainty.
- (k): implementation capacity/accuracy parameter whose mapping to error is library-specific.
- **Compactor level**: retained items of a common power-of-two weight.
- **Absolute rank error**: error scaled by (n) uniformly across ranks.
- **Relative rank error**: error scaled by distance to a selected rank-domain endpoint.
- **Centroid**: numeric mean plus represented weight in a clustering sketch.
- **Exact rank oracle**: fully sorted reference data used only for bounded validation.

## Mechanisms, Invariants, or Proof Structure

### GK proof obligations

Insertion establishes rank bounds for the new tuple. Compression preserves sorted order and transfers a predecessor's gap into its successor only when the successor's maximum rank uncertainty stays within threshold. Query accumulates minimum ranks and chooses a retained neighbor before the target-plus-allowance boundary. A full proof connects these local statements to global (\varepsilon n) error.

### Compactor proof obligations

Every retained item has a level-derived weight, and total retained weight equals (n). Pair compaction preserves weight exactly. Random parity makes rank displacement a zero-centered random contribution; capacity scheduling bounds the sum of contributions across levels. Merge must recreate a state admitted by the same capacity and randomness analysis.

### Systems invariants

- values obey a stable total order and accepted-domain policy;
- retained mass, stream count, and serialized count agree;
- extrema and endpoint promises survive compaction and merge;
- configuration and comparator digests match before mutation;
- no partial compaction or conversion becomes visible;
- merge lineage represents intended windows exactly once;
- result metadata states rank convention, error type, confidence, and estimator version.

## Alternatives and Trade-Offs

Exact sorting provides arbitrary exact queries and values but requires retaining and shuffling data. Histograms give interpretable fixed boundaries but lose resolution inside buckets and require range planning. Reservoir samples retain witnesses and support many analyses, yet tail quantiles need large samples. GK offers deterministic rank error but more complex tuple maintenance and less straightforward distributed merge. KLL offers compact probabilistic uniform-rank accuracy and mature mergeable implementations. REQ trades central accuracy for one-sided relative-rank accuracy. t-digest offers compact, often excellent numeric tail behavior and interpolation, with an empirical contract that must be characterized. DDSketch-style logarithmic histograms target relative value error for positive magnitudes—a different guarantee that can be preferable for latency ratios.

## Failure Modes and Misconceptions

- **Rank error equals value error.** Distribution gaps break that inference.
- **Every p99 definition matches.** Inclusive, exclusive, nearest-rank, and interpolated APIs differ with duplicates and small (n).
- **A lower returned value means a better sketch.** Error must be evaluated by true rank and decision loss.
- **KLL parameter (k) is epsilon.** The mapping is implementation/version specific.
- **One deterministic seed proves probabilistic coverage.** It tests a path, not a failure rate.
- **t-digest inherits the KLL theorem.** It uses different representation, interpolation, and evidence.
- **Tuple or centroid concatenation is merge.** Correct merge must enforce capacity and invariants.
- **Equal class names imply compatible bytes.** Comparator, encoding, parameters, modes, and versions matter.
- **Weighted updates can always be expanded.** Large weights make expansion infeasible and may change analysis.
- **Sketch subtraction expires a bucket.** Most quantile summaries have no inverse.
- **NaN sorts like an ordinary number.** It can violate comparator laws unless normalized or rejected.
- **Atomic observation count makes snapshots safe.** Buffers and levels may still be half-compacted.

## Worked Examples

### Example 1

**Rank versus value.** In 990 zeros followed by ten million-valued observations, ranks 0.989 and 0.991 differ by only 0.002, yet their quantile values can differ by one million. **Conclusion:** an absolute rank guarantee must be evaluated against the distribution's value gaps.

### Example 2

**GK tuple check.** At (n=200), (\varepsilon=0.05), the uncertainty threshold is (2\varepsilon n=20). A candidate merge with (g_i=7), (g_{i+1}=8), and (\Delta_{i+1}=4) totals 19 and is permitted; total 21 is rejected. **Conclusion:** compression is governed by rank uncertainty, not merely tuple count.

### Example 3

**Fixture median.** The executable model returns 113 for (q=0.5); its exact inclusive rank is 110, target rank 100, and error 10. The allowance is (0.05\times200=10). **Conclusion:** a boundary result can be valid without equaling the exact median value.

### Example 4

**KLL mass transfer.** Four level-zero items each have weight one. Pairing and retaining one item per pair promotes two items of weight two; total represented mass remains four. A later promotion of one of those pairs creates one item of weight four. **Conclusion:** compaction deletes values but must conserve weight.

### Example 5

**Tail requirement.** A p99.99 latency decision cares about the final 0.01% of ranks. Uniform absolute error 1% spans 100 times that tail mass. **Conclusion:** choose tail-relative accuracy, much smaller uniform error, or exact tail retention rather than quoting central accuracy.

### Example 6

**Duplicate convention.** For values (10,20,20,20,50), inclusive rank of 20 is 4/5 and exclusive rank is 1/5. An API returning either without naming the convention makes inverse queries irreconcilable. **Conclusion:** duplicate semantics are part of serialized/API compatibility.

### Example 7

**Incompatible merge.** One shard orders strings by raw UTF-8 bytes; another uses locale collation. Their retained weighted values cannot be placed in one proven total order. **Conclusion:** comparator identity is as important as (k).

### Example 8

**Reduction variation.** Eight randomized shard sketches are merged in a balanced tree and a left-deep tree. Both may satisfy the rank guarantee while retaining different items and returning different p95 values. **Conclusion:** statistical correctness does not imply bytewise reproducibility.

### Example 9

**NaN boundary.** A latency parser emits NaN for missing spans. If NaN enters sorting, comparisons may be false in both directions. Rejecting it and counting rejections separately preserves the numeric distribution contract. **Conclusion:** missing-data policy precedes sketch accuracy.

### Example 10

**Window expiration.** Seven sealed daily KLL sketches can merge into a seven-day result. At the next boundary, yesterday's union cannot be “minus day one”; merge days two through eight or use a window-specific hierarchy. **Conclusion:** mergeability is not invertibility.

## Cross-Program Connections

- **Database Engineering:** approximate percentile aggregates, histograms, selectivity, and partition bounds depend on rank semantics.
- **Data Engineering:** windows, late data, shard skew, schema normalization, and reduction topology determine summary meaning.
- **Distributed Systems:** merge trees, retries, generation fencing, and snapshot lineage surround the algebra.
- **Observability Engineering:** tail latency and SLO decisions require tail-appropriate error and exact calibration.
- **Concurrent and Parallel Programming:** owner-thread sketches, per-core summaries, compaction publication, and cache layout govern safe throughput.
- **Security Engineering:** malformed weights, comparator attacks, NaNs, and untrusted serialized summaries require validation.

## References

1. Michael Greenwald and Sanjeev Khanna, [Space-Efficient Online Computation of Quantile Summaries](https://sigmodrecord.org/2001/06/07/space-efficient-online-computation-of-quantile-summaries/), *SIGMOD*, 2001; official publication record.
2. Michael Greenwald and Sanjeev Khanna, [Space-Efficient Online Computation of Quantile Summaries](https://www.cs.princeton.edu/~hy2/teaching/fall21-cos597J/files/cos597J-papers/sigmod01_quantiles.pdf), author-institution course archive.
3. Zohar Karnin, Kevin Lang, and Edo Liberty, [Optimal Quantile Approximation in Streams](https://arxiv.org/abs/1603.05346), *FOCS*, 2016.
4. Ted Dunning and Otmar Ertl, [Computing Extremely Accurate Quantiles Using t-Digests](https://arxiv.org/abs/1902.04023), 2019.
5. Ted Dunning, [The Size of a t-Digest](https://arxiv.org/abs/1903.09921), 2019.
6. Apache Software Foundation, [Introduction to Quantile Sketches](https://datasketches.apache.org/docs/QuantilesAll/QuantilesOverview.html), accessed 2026-08-30.
7. Apache Software Foundation, [KLL Sketch](https://datasketches.apache.org/docs/KLL/KLLSketch.html), accessed 2026-08-30.
8. Apache Software Foundation, [REQ Sketch](https://datasketches.apache.org/docs/REQ/ReqSketch.html), accessed 2026-08-30.

## Exercises

### Exercise 1

For (n=50{,}000) and absolute rank error (\varepsilon=0.002), compute the natural-rank allowance. Explain why this does not bound value error at p99.

### Exercise 2

Given consecutive GK tuple data (g_i=12), (g_{i+1}=9), (\Delta_{i+1}=6), determine whether compression is allowed at (n=300) for (\varepsilon=0.05). Show the invariant calculation.

### Exercise 3

A p99.9 dashboard changed after moving from a t-digest implementation to KLL. Give a diagnosis and migration-validation plan without assuming either result is wrong.

### Exercise 4

Design a distributed envelope and merge protocol for hourly quantile sketches across heterogeneous language runtimes. Include comparator, float, parameter, randomization, window, and corruption controls.

### Exercise 5

A payments platform needs median transaction value, p99.99 latency, exact minimum/maximum, seven-day rolling queries, and occasional weighted merchant aggregates. Select structures and evidence for each requirement.

## Answers to the Exercises

### Answer 1

The natural-rank allowance is (\varepsilon n=0.002\times50{,}000=100) observations. A valid p99 answer may have true rank between approximately 49,400 and 49,600 under the chosen endpoint convention. If values jump sharply inside that interval, numeric error can be arbitrarily large relative to the p99 value. Calibration must therefore inspect value loss on relevant distributions or require a value-relative structure.

### Answer 2

The GK compression expression is (g_i+g_{i+1}+\Delta_{i+1}=12+9+6=27). The threshold is (\lfloor2\varepsilon n\rfloor=\lfloor2(0.05)(300)\rfloor=30). Since 27 is at most 30, the local uncertainty condition permits the merge, assuming endpoint and schedule rules also permit that pair. If the sum were 31, it would be rejected.

### Answer 3

Freeze identical raw windows and define inclusive/exclusive rank, interpolation, NaN, infinity, and extrema behavior. Record both implementations' parameters, versions, comparators, numeric encodings, and merge trees. Compare returned values by exact ranks, not by value difference alone, across monotone, reverse, duplicate-heavy, skewed, and production windows. Run KLL over many seeds and measure failure/coverage; characterize t-digest centroid and tail error by compression/order/tree. Check whether the dashboard switched endpoint or interpolation semantics. Dual-publish versioned results until decision thresholds are recalibrated; rebuild rather than reinterpret incompatible serialized state.

### Answer 4

The envelope contains magic/format, algorithm/estimator, error mode, (k) or compression, comparator ID, item schema, IEEE encoding and NaN/infinity policy, endpoint/inclusion semantics, min/max policy, randomization/version, total count/weight, window/generation/shard lineage, payload size, and checksum. Producers pass cross-language golden ordering and serialization fixtures. Reducers reject mismatches before mutation, deduplicate shard windows, use a declared tree, validate retained weights/ranks, and fence generations. Corrupt or excessive weights and malformed floats are quarantined. Evidence includes exact-oracle tests, multi-seed accuracy trials, cross-language round trips, tree/order studies, replay/late-data tests, and fault injection.

### Answer 5

Use exact tracked extrema because they cost constant state and are contractually important. A KLL/GK-family uniform-rank sketch can serve the median. For p99.99, use REQ high-rank mode, a carefully characterized t-digest, or a much tighter KLL budget, selected by measured tail-rank and decision error. Maintain sealed daily/hourly sketches and re-merge live buckets for seven-day queries; do not subtract expired summaries. Weighted merchant aggregates require a natively weighted quantile algorithm or pre-aggregation with a proved weighted summary—not repeated expansion. Validate exact ranks on protected samples, tail coverage across seeds/orders, extrema, duplicate/NaN policy, weighted conservation, cross-window merges, late events, serialization, concurrency, and rollback. Consequential payment decisions retain an exact confirmation path near thresholds.
