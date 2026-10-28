---
module_id: DBE-063
program: Database Engineering
level: 2
module_number: 63
title: Statistics and Histograms
status: complete
last_verified: 2026-08-30
---

# Statistics and Histograms

## One-Page Review

### Governing question

How can a database summarize a changing, skewed, correlated data population within bounded collection, storage, planning, and privacy budgets—and make the uncertainty and domain of every estimate explicit?

### Essential definitions

A **planner statistic** is a versioned summary used to estimate row counts, widths, ordering, or costs. **Selectivity** is the fraction of input occurrences expected to satisfy a predicate. **NDV** is the number of distinct non-null values under a stated equality. An **MCV list** stores frequent values and their masses. A **histogram** partitions an ordered domain or frequency distribution into bounded buckets. **Equi-width** buckets span similar domain widths; **equi-depth/height** buckets carry similar population. A **sample** is a probability-selected subset with a declared design. **Staleness** is mismatch between the summarized population and the population planned against. **Extended statistics** model expressions or multiple columns. A **sketch** is a compact approximate summary with an algorithm-specific error contract. **Feedback statistics** learn from executed predicates or operators.

### Central model, mechanism, or theorem

Let N be total rows. Decompose probability mass into null mass, explicit MCV mass, and residual mass. Equality on an MCV uses its recorded frequency; an unseen residual value often receives `residual_mass / residual_NDV`, subject to domain and zero policies. A range estimate integrates whole and partial histogram buckets under an explicit within-bucket model. Every component must reconcile: masses remain in `[0,1]`, categories do not overlap, and accounted mass sums to one within rounding. These formulas are model outputs, not truths; sampling, compression, correlation, drift, and out-of-range values introduce error.

### Critical invariants

- Every statistic binds table/partition, column/expression identities, types, collation, snapshot/epoch, population row count, method, sample, target, and software/format version.
- Nulls are modeled separately; MCV entries are excluded from residual histogram/NDV mass when the format says so.
- Frequencies are nonnegative, cumulative bounds are monotone, bucket domains do not overlap accidentally, and total mass is conserved.
- NDV, row count, width, ordering correlation, MCV frequency, and histogram selectivity are different quantities.
- Univariate statistics are not multiplied under independence when known dependencies, mutual exclusion, keys, or joint skew dominate.
- Sample uncertainty, estimator error, histogram compression error, and data staleness are reported separately.
- Empty, all-null, unique, constant, heavy-hitter, sparse, NaN, out-of-range, and rapidly growing populations have explicit handling.
- Statistics collection, storage, operator evaluation, export, and feedback are access-controlled because summaries may expose data.

### Common failures

Failures include uniformity-by-default on heavy hitters; counting null as an ordinary distinct value inconsistently; double-counting MCV mass inside a histogram; interpolating strings as numbers; assuming independence for city/state or tenant/status; trusting a small sample for rare values; merging nonmergeable histograms; using global statistics for one partition; ignoring ascending-key inserts; treating approximate NDV as exact; comparing error ratios when actual/estimate is zero without a policy; refreshing after the incident but analyzing the wrong snapshot; or exporting literal MCVs from sensitive columns.

### Compact example

In a 16-row finite population, two nulls give null fraction 0.125. Values 1 and 2 occur four and two times, so their MCV masses are 0.250 and 0.125. Eight singleton residual values carry total mass 0.500, giving a residual equality estimate of 0.0625 each. Residual bounds `(3,6,10)` divide the eight residual occurrences into two equal-depth buckets. The executable verifies exact mass reconciliation for this deliberately small population.

### Connections

Retrieve [Relational Rewrite Rules](061-relational-rewrite-rules.md), [Predicate Pushdown and Projection Pruning](062-predicate-pushdown-and-projection-pruning.md), [B+ Tree Structure](031-b-tree-structure.md), and [Profiling a Query Operator Pipeline](060-profiling-a-query-operator-pipeline.md). Continue through [the roadmap](../ROADMAP.md) to cardinality estimation, cost models, join ordering, access paths, plan caching, adaptation, and diagnosis.

## Governing Question

A cost-based optimizer cannot inspect every row while planning every query. It instead consumes compact claims about table size, nulls, distinctness, frequent values, ranges, dependencies, widths, physical order, and change. How should those claims be constructed, interpreted, maintained, combined, and audited so they improve decisions without masquerading as exact knowledge?

Statistics are lossy interfaces between data and optimizer. The collector observes a full population or sample under one snapshot. The summary format compresses it. The estimator interprets the summary for a predicate it may not have anticipated. The cost model turns estimated rows and widths into resource predictions. The search engine chooses a plan. Error at an early boundary can amplify through joins, aggregation, memory grants, parallelism, and distributed exchanges.

The engineer therefore needs more than “run ANALYZE.” For every statistic ask: which population, equality/order semantics, sample design, representation, assumptions, update trigger, privacy boundary, and downstream formula does it govern? Then compare its predictions with independent actuals at the correct plan node and parameter class.

## Why This Matters

Consider a tenant column with one tenant holding half the table and millions of tiny tenants sharing the rest. `1/NDV` is a poor equality estimate for both. An MCV list can represent the heavy tenant exactly and reserve a residual distribution for the tail. A histogram helps range predicates whose density changes across the domain. Neither solves correlation: multiplying independent estimates for `country='SE'` and `city='Stockholm'` can understate a relationship already encoded by the data.

Statistics affect more than scan choice. Underestimating a join can select nested loops, undergrant a hash table, create an undersized exchange, or defer spill too late. Overestimation can reject an index, reserve excessive memory, reduce concurrency, or choose unnecessary parallelism. Small local errors can multiply along a plan; DBE-064 will formalize cardinality propagation.

Collection has operational cost. A full scan may be accurate for that snapshot but expensive and soon stale. Random samples bound work but introduce variance and can miss rare or clustered values. Higher targets store more buckets/MCVs and spend more analysis/planning time. Multivariate summaries confront a dimensional explosion. Feedback targets workload-relevant regions but inherits workload bias and delayed labels.

Current products expose distinct representations. PostgreSQL 18 documents null fraction, average width, NDV, MCVs, histogram bounds excluding MCVs, and physical/logical ordering correlation; it supports multivariate NDV, functional dependencies, MCVs, and expression statistics. MySQL 8.4 documents singleton or equi-height JSON histograms. Current SQL Server documentation describes sampled/full statistics, density vectors, and at most 200 histogram steps on the first statistics-key column. SQLite uses ANALYZE statistics tables, with richer `stat4` samples when compiled accordingly. A portable mental model must respect these differences rather than invent one universal histogram layout.

## Prerequisites and Retrieval

You should understand probability mass, samples, frequencies, quantiles, sets/bags, null semantics, collations, indexes, partitions, query plans, and the difference between estimates and observations. Familiarity with variance and confidence intervals helps, but this chapter derives the operational formulas it uses.

Retrieve: population N; sample n and design; null fraction; non-null NDV; average width; heavy hitter/MCV; residual mass/NDV; bucket boundary; equi-width/equi-depth; singleton; cumulative frequency; density; physical-order correlation; joint distribution; functional dependency; expression statistic; sketch; mergeability; relative standard error; staleness; modification counter; feedback bias; and q-error with zero policy.

## Learning Objectives

After this module, you can:

1. specify the identity, snapshot, method, and uncertainty contract of a planner statistic;
2. reconcile null, MCV, and residual probability mass;
3. construct and interpret equi-width, equi-depth, singleton, MaxDiff-like, and hybrid histograms;
4. estimate equality and ranges while stating within-bucket and out-of-range assumptions;
5. distinguish exact NDV, sampled NDV estimators, and mergeable sketches;
6. detect independence failures and choose multivariate NDV, dependency, joint MCV, filtered, or expression statistics;
7. design refresh, incremental, partition/global, and feedback maintenance policies;
8. diagnose stale, sparse, biased, or internally inconsistent statistics from plan evidence;
9. protect sensitive values and operator execution at statistics boundaries; and
10. validate statistics with deterministic populations, randomized trials, workload-weighted errors, and production-safe rollout.

## Core Exposition

**Bind every summary to a population.** A statistic needs stable relation/column/expression IDs, schema/type/collation, partition/inheritance scope, visibility/snapshot rule, filter predicate if partial, collection timestamp and data epoch, total/sample row counts, sampling design and seed policy, target/bucket budget, algorithm/version, and null/NaN treatment. Without this envelope, a number cannot be interpreted or safely merged.

Table statistics often include row/page counts and modification estimates. Column statistics add null fraction, average width, NDV, MCVs, and an ordered histogram. Index statistics may describe prefix distinctness or clustering. Expression statistics summarize a normalized bound expression, not merely its printed text. Filtered statistics summarize a declared subset. Multivariate statistics summarize a tuple of attributes/expressions.

**Separate exact counts from estimates.** A catalog row count may itself be approximate. A sample frequency is an estimator of population frequency. A histogram range is a model based on compressed observations. A sketch has an algorithm-specific distribution of error. Round trips through serialization and float arithmetic add smaller error. Label each layer rather than attaching one vague “confidence.”

Simple random sampling gives each row a known chance of selection. Systematic page/block sampling may be cheaper but can interact with clustering. Reservoir sampling supports one-pass unknown-length streams. Stratification can protect important partitions/classes when weights are retained. Samples must reflect visible rows and current data; retries, parallel workers, partitions, replicas, and deleted versions must not create hidden inclusion bias.

Rare values expose sampling limits. If a value occurs with population fraction p, a simple independent sample of size n misses it with probability `(1-p)^n`. At p=`0.0001` and n=`10,000`, that is about `e^-1`, not negligible. Increasing n helps, but targeted MCV discovery, sketches, stratification, or workload feedback may be more economical. State the approximation used in such probability calculations.

**Reconcile mass before estimating.** Let `f_null` be null fraction. For MCV set M with frequencies `f_i`, define `f_mcv=sum f_i` and residual mass `f_r=1-f_null-f_mcv`. Let `d_r` be residual non-null NDV. A basic unseen-residual equality model is `f_r/d_r` when `d_r>0`. It assumes residual values have equal frequency. If `d_r=0`, non-MCV equality mass is zero. If query value is null, use null semantics (`IS NULL` versus `= NULL`) rather than equality machinery.

MCV selection should not blindly take sample top-k. Sampling noise can promote false heavy hitters and miss true ones. Formats use thresholds, significance tests, or budgets. Stored frequencies should have defined denominators—usually total rows, not only non-null rows. Validate all MCVs are distinct under the statistic's equality/collation and absent from the residual histogram when required.

**A histogram is a compressed distribution model.** Equi-width partitions a numeric/order domain into similar widths; it is easy but wastes buckets on empty regions and hides skew inside dense regions. Equi-depth chooses boundaries so buckets have similar population; it places resolution where data exists but still assumes something inside each bucket. Singleton histograms represent each distinct value when NDV fits the budget. MaxDiff-like schemes place boundaries at large adjacent frequency/value changes. V-optimal histograms minimize a chosen within-bucket error objective. The 1996 Poosala et al. study formalized multiple partition and value/frequency sorting choices and evaluated their range-selectivity error.

Buckets need an exact convention: inclusive/exclusive endpoints, discrete versus continuous domain, boundary frequency, cumulative versus per-bucket mass, distinct count, null/MCV exclusion, and collation. PostgreSQL's `histogram_bounds` are approximately equal-population groups over non-MCV values. MySQL's equi-height bucket encoding records lower/upper inclusive values, cumulative frequency, and distinct values. SQL Server steps separate equality rows at the upper bound from range rows and distinct-range counts. Never transplant one formula into another representation.

For a range, add fully covered bucket mass plus an interpolated fraction of partially covered buckets. Uniform-spread interpolation assumes values/frequency are smooth within the bucket. For integers, domain cardinality matters; for strings, timestamps, decimals, collations, and NaNs, numeric distance may be meaningless or product-specific. When no supported interpolation exists, a conservative/default estimate is more honest.

The executable constructs an exact small hybrid summary. Its “histogram” uses residual values directly; it demonstrates accounting rather than sampling or a production estimator.

<!-- bijux-verify: {"id":"finite-histogram-accounting","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"rows=16\nnon_null_rows=14\nnull_fraction=0.125\nndv_non_null=10\nmcv=((1, 4), (2, 2))\nmcv_mass=0.375\nresidual_rows=8\nresidual_ndv=8\nhistogram_bounds=(3, 6, 10)\nestimate_eq_1=0.2500\nestimate_eq_5=0.0625\nestimate_range_3_6=0.2500\nmass_conserved=True\nevidence=exact_finite_summary\n","stderr":""}} -->
```python
from collections import Counter
from fractions import Fraction

rows = [1, 1, 1, 1, 2, 2, 3, 4, 5, 6, 7, 8, 9, 10, None, None]
counts = Counter(value for value in rows if value is not None)
total = len(rows)
null_count = rows.count(None)
mcv = ((1, counts[1]), (2, counts[2]))
mcv_values = {value for value, _ in mcv}
residual = sorted(value for value in rows if value is not None and value not in mcv_values)
residual_ndv = len(set(residual))
null_mass = Fraction(null_count, total)
mcv_mass = sum((Fraction(count, total) for _, count in mcv), Fraction())
residual_mass = Fraction(len(residual), total)

estimate_eq_1 = Fraction(counts[1], total)
estimate_eq_5 = residual_mass / residual_ndv
estimate_range_3_6 = Fraction(sum(3 <= value <= 6 for value in residual), total)
histogram_bounds = (residual[0], residual[3], residual[-1])

print(f"rows={total}")
print(f"non_null_rows={total - null_count}")
print(f"null_fraction={float(null_mass):.3f}")
print(f"ndv_non_null={len(counts)}")
print(f"mcv={mcv}")
print(f"mcv_mass={float(mcv_mass):.3f}")
print(f"residual_rows={len(residual)}")
print(f"residual_ndv={residual_ndv}")
print(f"histogram_bounds={histogram_bounds}")
print(f"estimate_eq_1={float(estimate_eq_1):.4f}")
print(f"estimate_eq_5={float(estimate_eq_5):.4f}")
print(f"estimate_range_3_6={float(estimate_range_3_6):.4f}")
print(f"mass_conserved={null_mass + mcv_mass + residual_mass == 1}")
print("evidence=exact_finite_summary")
```

The MCV residual equality formula happens to be exact because all eight residual values occur once. Change one residual frequency and it becomes an approximation. The bounds `(3,6,10)` describe two equal-population residual intervals only under the chosen endpoint convention; they are not sufficient to reconstruct arbitrary point frequencies.

**NDV deserves its own estimator.** Exact distinct counting needs memory proportional to observed distinct values or external processing. Sampled NDV cannot simply scale sample distinctness linearly: repeats and unseen species matter. Database estimators use sample frequencies and domain assumptions. Streaming/distributed systems often use mergeable sketches.

HyperLogLog hashes values into m registers and derives cardinality from extreme leading-zero patterns; the original analysis gives typical relative standard error about `1.04/sqrt(m)` for the stated estimator regime. This is not a universal confidence interval, nor permission to merge sketches with different hash, seed, precision, encoding, correction, or version. Sketch union estimates set union; intersection by subtracting approximate unions can have much worse relative error. Hash collisions, adversarial input, privacy, and serialization compatibility matter.

**Univariate summaries cannot encode arbitrary joint distributions.** Under independence, selectivities multiply. For perfectly dependent predicates that is disastrous. If every Stockholm row has country SE and city selectivities are 0.01 while country SE is 0.02, multiplication predicts 0.0002 for their conjunction instead of 0.01—a 50-fold underestimation. Mutual exclusion can make a nonzero product when the true result is zero.

Multivariate options include joint MCV lists for frequent tuples, NDV for column sets/group counts, functional-dependency strength, multidimensional histograms, copulas/models, and workload-specific feedback. Keys and constraints provide exact facts when enforced. PostgreSQL 18 `CREATE STATISTICS` currently supports multivariate `ndistinct`, `dependencies`, and `mcv`, plus expression statistics. Its documentation also cautions that functional dependencies apply to compatible equality conditions and do not replace semantic constraints.

Expression statistics help predicates such as normalized email, date extraction, or computed keys, but expression identity includes function/operator versions, casts, collation, time zone, and immutability. Partial/filtered statistics describe a subset and are useful for active rows or dominant parameter classes; the optimizer must prove the query predicate implies the statistics filter.

**Physical-order correlation is not semantic dependence.** Correlation between column order and physical row position can inform random-versus-sequential access cost. It does not estimate conjunction selectivity and changes after clustering, bulk load, page splits, or compaction. Average width informs memory and I/O but hides heavy-tailed varlena values and correlations between width and predicates.

**Maintain statistics as governed state.** Refresh triggers may use elapsed time, modification count/fraction, partition arrival, drift tests, estimate error, or workload importance. Fixed percentages behave poorly: one million changed rows is negligible for a trillion-row table but enormous for a tiny hot partition. Append-only ascending keys create out-of-range values even when global change fraction is low. Track high-water marks and recent partitions separately.

Partition-local statistics are easier to refresh and model local skew; global queries need global summaries. Row counts and some sketches merge naturally. MCV lists and histograms generally do not merge by concatenation: partition weights, overlapping domains, bucket models, and global heavy hitters require recomputation or a defined merge algorithm. A value modest in every partition can become globally dominant; local top-k truncation may lose it.

Collection must coexist with DDL, transactions, replicas, and failures. Define which snapshot is sampled, how schema changes invalidate objects, whether partial refresh publishes atomically, how retries avoid mixing epochs, and how planner caches learn a new generation. Keep the previous valid generation until the new one validates; never publish half-updated row counts with old histograms as one coherent snapshot.

**Feedback closes a biased loop.** Executed plans supply actual rows for observed predicates. Self-tuning histograms use such feedback to refine workload-relevant regions without repeatedly scanning all data. Benefits come with selection bias: only chosen plans and admitted/completed queries generate labels; timeouts and rare parameter classes may be absent; estimates influence plans which influence observations. Bind feedback to query/plan/predicate/data/statistics versions, normalize parameter privacy-safely, decay stale evidence, reserve exploration or offline audits, and prevent one tenant from poisoning shared statistics.

**Measure accuracy at decisions.** For node estimate E and actual A, q-error is `max(E/A,A/E)` when both are positive. Zero/nonzero needs an infinite or separately capped/labeled category; zero/zero is exact for that event. Also record signed log error, absolute row error, and downstream resource impact. A 100-fold error from 1 to 100 rows may not change a plan; a twofold error around a spill or join-order threshold may.

Evaluate held-out predicates across equality/range/IN/null/conjunction/join/group classes, parameter classes, partitions, scale, and time. Report median/tails/worst, under-versus-over direction, workload-weighted and coverage metrics, plan changes, planning overhead, collection cost, catalog size, and execution outcomes. Avoid training and testing feedback statistics on the same workload window.

**Protect statistics.** MCV literals, endpoints, min/max, counts, sketches, correlations, and feedback can reveal presence, rarity, business volume, tenant behavior, or secrets. PostgreSQL 18 restricts `pg_statistic` and documents risks when user-defined operators are invoked on stored values during selectivity estimation. Apply least privilege, safe operators, redaction/tokenization where semantically valid, encryption, retention, tenant separation, export controls, and audit. Differential privacy can bound some disclosure but consumes privacy budget and adds estimator noise; it is not a free switch.

Production diagnosis starts from evidence: confirm query/parameters/plan/snapshot; compare estimated and actual at the first divergence; inspect statistic identity, age, sample/target, null/MCV/hist/NDV, partition/global scope, dependencies, expression match, and out-of-range data; reproduce with controlled refresh/target/extended statistic; validate plan and workload effects; then automate the narrow corrective policy. Do not prescribe blanket maximum targets or continuous full scans.

## Definitions and Notation

- **N, n**: population and sample row counts.
- **A, E**: actual and estimated row counts for a declared node/event.
- **s**: predicate selectivity; estimated result rows are typically input estimate times s.
- **f_null**: null fraction over total rows.
- **M, f_i**: MCV set and total-row frequency of member i.
- **f_mcv**: sum of MCV frequencies.
- **f_r**: residual non-null, non-MCV mass `1-f_null-f_mcv`.
- **d, d_r**: non-null NDV and residual NDV.
- **Bucket**: domain/frequency region with boundary and mass metadata.
- **Density**: context-specific duplicate/selectivity summary; define its denominator and keys.
- **RSE**: relative standard error, standard deviation divided by estimand.
- **Q-error**: symmetric multiplicative error for positive E and A.
- **Statistic generation**: atomically published compatible set of summaries and metadata.

For unseen residual equality, a common model is `s=f_r/d_r`. For a simple random sample, missing a value of population fraction p in n independent draws has probability `(1-p)^n`; finite-population sampling without replacement uses the exact hypergeometric probability instead.

## Mechanisms, Invariants, or Proof Structure

**Mass proof.** Nulls, stored MCV occurrences, and residual occurrences form a disjoint partition of rows. Their exact or estimated masses must sum to one within declared rounding. Histograms over the residual cannot silently include MCVs again.

**Bucket invariant.** Bounds are ordered under the statistic's collation; endpoint convention assigns every represented residual value to exactly one bucket; bucket masses are nonnegative and cumulative masses monotone. Empty-domain and duplicate-boundary behavior is explicit.

**Sampling argument.** Record inclusion probabilities and weights. An estimator is unbiased only under its sampling/model assumptions. Quantify variance or empirical error; a large n does not repair systematic exclusion of partitions, pages, tenants, or invisible rows.

**NDV/sketch invariant.** Exact and approximate NDV are labeled. Merge requires identical hash/equality, seed, precision, register format, correction, and generation policy. Validate serialization and reject incompatible unions.

**Dependency argument.** Independence multiplication is a model, not an identity. Constraints, joint MCVs, NDV sets, dependencies, and workload evidence may override it only within their supported predicate forms and snapshot.

**Publication invariant.** A statistic generation is validated for schema/identity, counts/mass/bounds, sample metadata, security, and compatibility before atomic visibility. Failed refresh leaves the last valid generation or an explicit no-statistics state.

**Feedback invariant.** Each label binds actual rows to predicate, operator, plan, parameters/class, snapshot/data epoch, statistics generation, software, and completion state. Training/evaluation windows are separated and tenant influence bounded.

## Alternatives and Trade-Offs

**Full scans** reduce sampling error for one snapshot but cost I/O/CPU and may block freshness. **Sampling** is bounded and fast but adds variance and rare-value risk.

**Equi-width** is simple and merge-friendly only under a shared fixed grid. **Equi-depth** allocates resolution to populated regions but boundary construction/merging costs more. **V-optimal/MaxDiff-like** schemes target error structure at higher build complexity.

**MCV lists** capture heavy hitters exactly within the sample/format. Larger lists consume storage/planning time and expose more literals.

**Exact NDV** is costly at scale. **Sketches** are compact and mergeable under strict compatibility, but approximate and sometimes poor for set differences/intersections.

**Univariate statistics** scale linearly in columns. **Multivariate statistics** capture dependence but face combinatorial candidate selection, build cost, storage, staleness, and workload bias.

**Scheduled refresh** is predictable. **Change-triggered refresh** reacts to churn. **Feedback adaptation** targets observed errors. Mature systems combine them with held-out audits and conservative fallback.

**Global statistics** answer global queries but hide local skew. **Partition statistics** refresh cheaply but need principled aggregation for global planning.

## Failure Modes and Misconceptions

1. “Fresh statistics are exact” ignores sampling and compression.
2. “More buckets always help” ignores collection, storage, planning, noise, and stale detail.
3. “NDV means one equality estimate” ignores MCVs, nulls, residual skew, and predicate class.
4. “Histograms contain every value” confuses compact boundaries with a frequency table.
5. “Equi-depth is uniform inside buckets” equal bucket mass does not prove within-bucket uniformity.
6. “Sample distinct times N/n estimates NDV” unseen-species/repeat behavior invalidates naive scaling.
7. “Independent columns can be multiplied” independence must be supported, not presumed.
8. “A foreign key statistic proves integrity” statistics are not constraints.
9. “Partition histograms concatenate globally” weights, overlap, and lost heavy hitters prevent it.
10. “One q-error average is enough” direction, zeros, tails, coverage, and decision impact matter.
11. “Execution feedback is ground truth for all queries” it covers a selected, censored workload.
12. “Statistics cannot leak rows” MCVs, bounds, counts, and operator execution can expose data.
13. “Auto-analyze removes operations work” thresholds, partitions, bulk loads, replicas, and ascending keys still need policy.
14. “A better estimate guarantees a faster plan” costs/search/runtime variability can dominate.

## Worked Examples

### Example 1

**Mass reconciliation.** In the executable population, null mass is 2/16, MCV mass is 6/16, and residual mass is 8/16. Their sum is 1. Conclusion: verify disjoint accounting before using any selectivity formula.

### Example 2

**Heavy hitter versus uniform NDV.** With N=1,000,000 and NDV=10,000, uniform equality predicts 100 rows. If tenant A actually owns 400,000 rows, MCV frequency predicts 400,000; uniformity is 4,000-fold low. Conclusion: isolate heavy hitters from the tail.

### Example 3

**Rare-value sample miss.** A value at fraction 0.0001 and independent sample n=10,000 is missed with probability `(0.9999)^10000`, approximately `e^-1` or 0.368. Conclusion: a seemingly large sample can miss operationally important rare classes.

### Example 4

**Range interpolation failure.** One bucket spans integers 1–100 with half its mass. If all bucket rows are at 1 and 100, linear interpolation for 40–60 predicts positive mass while actual is zero. Conclusion: bucket boundaries plus uniform-spread assumptions can hide internal gaps.

### Example 5

**Correlation error.** City Stockholm has selectivity 0.01 and country SE 0.02; every Stockholm row is in SE. Independence gives 0.0002 instead of 0.01, 50-fold low. Conclusion: joint MCV/dependency evidence is needed for the conjunction.

### Example 6

**All-null column.** N=50,000, null fraction 1, non-null NDV 0, residual mass 0. `x=7` selects zero while `x IS NULL` selects all rows. Conclusion: zero-domain policies prevent division by zero and semantic confusion.

### Example 7

**Ascending-key staleness.** Statistics cover timestamps through yesterday; today's append adds 20% of rows. A query for today lies beyond the maximum histogram bound and defaults low. Conclusion: high-water/out-of-range monitoring can matter more than average modification fraction.

### Example 8

**Incompatible sketch merge.** Two HLL objects both have 16,384 registers, but use different hashes/seeds. Register-wise maximum has no valid union interpretation. Conclusion: same shape is not compatibility; persist and validate algorithm identity.

### Example 9

**Partition/global MCV loss.** Value X ranks just below local top-10 in each of 100 partitions but is common across all; merging only local top-10 lists never discovers X. Conclusion: truncated local summaries need candidate recovery or global collection.

### Example 10

**Feedback-induced blind spot.** Bad estimates choose a plan that times out for large tenants; only completed small-tenant plans feed learning. Feedback declares the model healthy. Include timeouts/cancellations and reserved large-tenant probes in coverage. Conclusion: observation is selected by the system being trained.

## Cross-Program Connections

- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md): randomized algorithms, approximation, and error analysis underpin sampling/sketches.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md): counters, heaps, quantile summaries, sketches, and merge protocols implement statistics.
- [Data Engineering](../../19-data-engineering/ROADMAP.md): partitioned datasets, schema evolution, incremental computation, and quality monitoring determine freshness.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md): semantic identity, ownership, classification, lineage, and retention govern statistic meaning and access.
- [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md): distribution shift, calibration, validation splits, coverage, and adversarial testing strengthen estimator evidence.
- [Security Engineering](../../25-security-engineering/ROADMAP.md): access control, side channels, privacy budgets, and poisoning apply to statistics and feedback.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): scheduling, budgets, multitenancy, atomic publication, rollout, and observability make statistics operational.

## References

1. Viswanath Poosala et al., [“Improved Histograms for Selectivity Estimation of Range Predicates”](https://www.cs.cmu.edu/~natassa/courses/15-823/F02/papers/poosala96improved.pdf), *SIGMOD 1996*. Primary taxonomy and empirical comparison of database histograms.
2. Philippe Flajolet et al., [“HyperLogLog: the Analysis of a Near-Optimal Cardinality Estimation Algorithm”](https://algo.inria.fr/flajolet/Publications/FlFuGaMe07.pdf), *AofA/DMTCS*, 2007. Primary algorithm and accuracy analysis.
3. PostgreSQL Global Development Group, [PostgreSQL 18: Statistics Used by the Planner](https://www.postgresql.org/docs/18/planner-stats.html), retrieved 2026-08-30. Current univariate and extended planner-statistics overview.
4. PostgreSQL Global Development Group, [PostgreSQL 18: `pg_stats`](https://www.postgresql.org/docs/18/view-pg-stats.html), retrieved 2026-08-30. Current null, width, NDV, MCV, histogram, correlation, and element-statistics schema.
5. PostgreSQL Global Development Group, [PostgreSQL 18: `ANALYZE`](https://www.postgresql.org/docs/18/sql-analyze.html), retrieved 2026-08-30. Current sampling, targets, concurrency, and collection behavior.
6. PostgreSQL Global Development Group, [PostgreSQL 18: `CREATE STATISTICS`](https://www.postgresql.org/docs/18/sql-createstatistics.html), retrieved 2026-08-30. Current multivariate NDV, dependencies, MCV, and expression statistics.
7. PostgreSQL Global Development Group, [PostgreSQL 18: Planner Statistics and Security](https://www.postgresql.org/docs/18/planner-stats-security.html), retrieved 2026-08-30. Current catalog and user-defined-operator disclosure risks.
8. Oracle, [MySQL 8.4: Optimizer Statistics](https://dev.mysql.com/doc/refman/8.4/en/optimizer-statistics.html), retrieved 2026-08-30. Current singleton/equi-height JSON histogram representation and sampling metadata.
9. SQLite Project, [`ANALYZE`](https://www.sqlite.org/lang_analyze.html), retrieved 2026-08-30. Current statistics-table and `stat4` behavior.
10. Microsoft, [SQL Server Statistics](https://learn.microsoft.com/en-us/sql/relational-databases/statistics/statistics?view=sql-server-ver17), retrieved 2026-08-30. Current histogram-step, density, sampling, filtered-statistics, and first-key behavior.
11. Ashraf Aboulnaga and Surajit Chaudhuri, [“Self-tuning Histograms: Building Histograms Without Looking at Data”](https://wwwiti.cs.uni-magdeburg.de/~eike/selftuning/sources/aboulnaga99selftuning.pdf), *SIGMOD 1999*. Primary execution-feedback histogram design and evaluation.

## Exercises

### Exercise 1

A table has N=200,000, null fraction 0.10, MCV A at 0.30 and B at 0.15, and residual NDV 9,000. Compute residual mass and basic equality estimates for A, an unseen residual value, `IS NULL`, and a value proven outside the domain. State assumptions.

### Exercise 2

Construct an equi-width and an equi-depth two-bucket histogram for values `[1,2,3,4,100,100,100,100]`. Explain how each answers `x<50` and where interpolation error enters.

### Exercise 3

An optimizer underestimates `country='SE' AND city='Stockholm'` by 50-fold after fresh ANALYZE. Give a diagnosis and a safe correction/validation plan without assuming staleness.

### Exercise 4

Compare full scan, random sample, HLL NDV, partition-local summaries, and execution feedback for a trillion-row, daily-partitioned table. Specify merge, freshness, cost, bias, and privacy trade-offs.

### Exercise 5

Design an elite statistics service and release gate for a multitenant distributed database: identity, collection, algorithms, atomic publication, compatibility, security, accuracy evaluation, operational budgets, canarying, rollback, and claim limits.

## Answers to the Exercises

### Answer 1

Residual mass is `1-0.10-0.30-0.15=0.45`. A uses its MCV mass 0.30, estimating 60,000 rows. An unseen residual value uses `0.45/9000=0.00005`, estimating 10 rows under uniform residual frequency and assuming it belongs to the residual domain. `IS NULL` uses 0.10, or 20,000 rows. A value proven outside the domain has selectivity zero; an absent MCV alone does not prove that. Frequencies use total-row denominators, MCV and residual sets are disjoint, NDV excludes null/MCVs as stated, and the statistic matches the query's type/collation/snapshot.

### Answer 2

Domain 1–100 split equi-width at about 50 gives bucket `[1,50]` with four rows and `(50,100]` with four rows; `x<50` is near the full first-bucket mass 4/8, with endpoint treatment explicit. Equi-depth also seeks four rows per bucket, but duplicate 100s make boundaries tricky: a valid representation may isolate `[1,4]` mass 4/8 and singleton 100 mass 4/8, representing `x<50` exactly. If an equi-depth format uses only bounds and permits a broad first range, interpolation still assumes an internal distribution. Equi-width wastes domain space 5–99 but happens to separate the two clusters; other split choices do not. Duplicate-boundary, inclusive endpoints, discrete integer domain, and boundary frequencies must be encoded; a bare pair of numbers is insufficient.

### Answer 3

Confirm query, parameters, plan, actual/estimated nodes, data snapshot, statistic generation, predicate binding, null/collation, and that the first divergence is the conjunction. Inspect univariate MCV/hist/NDV: each can be fresh and individually accurate while independence multiplication is wrong. Check enforced constraints and existing extended statistics. Create a targeted multivariate object—joint MCV and/or dependency as supported—for country/city, collect it on the same population, and verify the predicate form is eligible. Test held-out cities/countries, nulls, rare combinations, parameter classes, planning overhead, plan changes, and execution distributions. Do not encode “Stockholm implies SE” as a database constraint unless it is a true governed business invariant; statistics improve estimates but do not enforce facts.

### Answer 4

A full scan provides exact snapshot summaries but is likely too costly daily. A probability sample bounds cost and estimates frequencies/histograms, with recorded inclusion design and rare/skew risk. HLL gives compact mergeable NDV with algorithm-specific error, but not MCV/range distribution; merge only identical hash/precision/version. Per-partition exact/sample/sketch summaries refresh with arrivals and model local skew, while global histograms/MCVs need weighted algorithms rather than concatenation. Feedback cheaply improves observed predicate regions but is workload-selected, censored, delayed, and poisonable. Combine per-partition row/null/width plus compatible NDV sketches, targeted samples for MCV/histograms, periodic global audits, and versioned feedback for gaps. Budget I/O/CPU/catalog/planning, detect ascending/out-of-range values, restrict sensitive MCV/bounds/sketch export, isolate tenant influence, and evaluate on held-out workload/time windows.

### Answer 5

Use stable tenant/table/partition/column/expression/type/collation identities and bind every generation to schema, snapshot/epoch, row/sample counts, method, target, seed policy, algorithm/version, and visibility. Collect through quota-aware full/sample/stream paths with explicit inclusion probabilities; provide row/null/width, guarded MCV/histograms, exact or compatible-sketch NDV, selected multivariate/expression/filtered objects, and versioned feedback. Validate counts, mass, bounds, distinct MCVs, domain/type, sketch compatibility, sample metadata, and access policy before atomic generation publication; retain the previous valid generation on failure. Encrypt and least-privilege literal summaries, use safe operators, tenant-separate feedback, audit exports, and apply retention/privacy budgets. Evaluate held-out equality/range/null/conjunction/join/group workloads over partitions, parameters, scale, drift, zeros, and adversarial skew using direction, q-error categories, tails, coverage, plan decisions, runtime, collection/planning/catalog budgets. Canary by tenant/fingerprint with result and plan evidence, alert on first estimate divergence/out-of-range/refresh failure, and support generation rollback/statistics disable. Internal validation supports only named algorithms, versions, populations, and workloads; it does not prove universal estimation accuracy, plan optimality, privacy, or production fitness, and no external review is claimed without named reviewers.
