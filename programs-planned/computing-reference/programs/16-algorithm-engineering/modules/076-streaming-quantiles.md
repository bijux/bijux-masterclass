---
module_id: ALGE-076
program: Algorithm Engineering
level: 2
module_number: 76
title: Streaming Quantiles
status: complete
last_verified: 2026-09-05
---

# Streaming Quantiles

## One-Page Review

### Governing question

How can a one-pass system answer order-statistic queries with bounded memory, and how should it choose, prove, merge, and operate a summary whose error model matches the decision being made?

### Essential definitions

- A stream induces an ordered multiset $S=(x_1,\ldots,x_n)$; multiplicity matters.
- The lower and upper ranks of $y$ are $L(y)=|\{i:x_i<y\}|+1$ and $U(y)=|\{i:x_i\le y\}|$. They form an interval when values repeat.
- For $0<\phi\le1$, the target rank is $r_\phi=\lceil\phi n\rceil$ and the exact lower quantile is $Q(\phi)=\min\{y:U(y)\ge r_\phi\}$.
- An **$\varepsilon$-rank approximation** returns a stream value whose feasible rank interval is within additive $\varepsilon n$ of $r_\phi$.
- A **quantile sketch** retains a small summary from which approximate ranks or quantiles can be queried.
- A **deterministic summary** provides its declared bound for every valid stream; a **randomized summary** provides a probability-qualified bound over its internal randomness.
- A **rank envelope** stores lower and upper bounds on the rank of a retained value.
- A **compactor** sorts a buffer, discards alternating items, and doubles retained weights so estimated rank remains unbiased.
- **Mergeability** means compatible summaries can be combined with the declared error law; concatenating serialized states is not automatically a valid merge.
- A **relative-value guarantee** bounds value error, not rank error. It answers a different question.

### Central model, mechanism, or theorem

Greenwald--Khanna (GK) stores ordered tuples $(v_i,g_i,\Delta_i)$. With

$$
r_{\min}(v_i)=\sum_{j\le i}g_j,\qquad
r_{\max}(v_i)=r_{\min}(v_i)+\Delta_i,
$$

insertion and compression preserve a rank envelope of width controlled by $2\varepsilon n$. This yields deterministic additive rank error with worst-case space $O(\bigl(\varepsilon^{-1}\log(\varepsilon n)\bigr))$ [1].

KLL uses randomized weighted compaction. An item at level $\ell$ represents weight $2^\ell$; choosing one parity from each sorted pair and doubling retained weights preserves total weight exactly and preserves every fixed rank estimate in expectation. A capacity schedule and concentration analysis turn that mechanism into a high-probability rank guarantee, with optimal asymptotic dependence on $\varepsilon$ and failure probability $\delta$ in its model [3]. The local invariant alone is not the theorem.

### Critical invariants

- The value order, duplicate convention, target-rank convention, and population are fixed before querying.
- Retained rank envelopes contain the true ranks permitted by all discarded data.
- Weighted compactors conserve total represented mass.
- Random choices, capacity schedule, and probability scope match the cited proof.
- Only states with compatible algorithm, parameters, ordering, value encoding, weights, and window may merge.
- Published uncertainty covers every query, group, and time point for which a simultaneous claim is made.

### Common failures

Confusing rank and value error; silently changing interpolation conventions; dropping duplicates; treating NaN as ordinarily ordered; claiming a deterministic guarantee from an empirical sketch; merging incompatible states; losing compactor weights; using insertion-only state for deletion or expiry; and treating a percentile estimate as a service-level guarantee.

### Compact example

For $n=1000$, $\phi=0.99$, and $\varepsilon=0.01$, the target rank is 990 and an additive-rank contract can permit ranks 980 through 1000. If rank 1000 is $10^9$ while rank 999 is $999$, returning $10^9$ can satisfy the rank contract yet have enormous value error. The metric and decision must therefore choose the error geometry, not merely the sketch name.

### Connections

[ALGE-075](./075-distinct-counting.md) establishes compatible synopsis merging and probability scope. ALGE-077 develops uniform sampling, which can also estimate quantiles but has a different space--confidence trade-off.

## Governing Question

Given an ordered stream too large to retain, which values should an algorithm keep so that later rank or quantile answers have an explicit error bound, and which implementation and operational conditions make that bound honest?

## Why This Matters

Medians, latency percentiles, price bands, database histograms, sensor thresholds, and fairness audits are distribution questions. A mean cannot reconstruct them: the multisets $\{0,0,0,100\}$ and $\{25,25,25,25\}$ have the same mean and radically different tails. Exact quantiles require enough information to distinguish order; in a one-pass sublinear-memory setting, approximation is therefore a model choice, not an incidental optimization. The limited-storage lower-bound lineage begins with Munro and Paterson [8].

The word “percentile” hides several independent choices. A batch library may interpolate between adjacent values; a streaming sketch normally returns an observed or bucket-representative value. One system may promise additive rank error; another may promise relative value error for nonzero values; a third may publish only measured accuracy. Those statements are incomparable until the population, ordering, target rank, probability, and merge history are fixed.

Production consequences can be severe. A rank-accurate p99 latency may still be value-inaccurate across a tail gap. A sketch accurate for one query may not support a simultaneous claim across thousands of tenants. A mechanically valid merge may combine different windows or units. A percentile used for alerting is evidence about observed events; it is not by itself a causal diagnosis, capacity guarantee, or service-level compliance proof.

## Prerequisites and Retrieval

Retrieve exact sorting and selection from ALGE-017, probability and randomized design from ALGE-029 and ALGE-066, approximation guarantees from ALGE-061, and stream and merge semantics from [ALGE-074](./074-streaming-frequency-estimation.md) and [ALGE-075](./075-distinct-counting.md). You should be able to sort a multiset, compute a ceiling rank, distinguish expectation from high probability, apply a union bound, and identify an invariant separately from an implementation test.

## Learning Objectives

After this module, you should be able to:

1. define exact and approximate quantiles under duplicates and boundary conventions;
2. derive the GK rank-envelope model and the weighted-compaction invariants behind KLL;
3. distinguish deterministic rank, probabilistic rank, absolute-value, and relative-value guarantees;
4. validate a quantile implementation against exact ranks and adversarial streams;
5. specify safe merge, serialization, window, weighting, and probability contracts; and
6. defend an estimator choice for database, telemetry, and consequential decision workloads.

## Core Exposition

### Quantiles begin with an ordered multiset

Let $S=(x_1,\ldots,x_n)$ be a finite multiset in a totally ordered domain. Multiplicity is intentional: one thousand latency observations from one endpoint count one thousand times unless a separately defined weighting policy says otherwise. For $0<\phi\le1$, this chapter uses the lower empirical quantile

$$
r_\phi=\lceil\phi n\rceil,\qquad
Q(\phi)=x_{(r_\phi)},
$$

where $x_{(j)}$ is the $j$th value in nondecreasing order. The empty stream has no quantile. We define $Q(0)=x_{(1)}$ only when an API explicitly chooses that extension.

Duplicates require rank intervals. For a returned value $y$ define

$$
L(y)=1+|\{i:x_i<y\}|,\qquad U(y)=|\{i:x_i\le y\}|.
$$

Every occurrence of $y$ occupies a rank from $L(y)$ through $U(y)$. Calling only $U(y)$ “the rank” is harmless for distinct data but can falsely mark a correct answer wrong when ties span the target. A returned $y$ is an $\varepsilon$-rank answer here when the distance between $r_\phi$ and $[L(y),U(y)]$ is at most $\varepsilon n$.

Ordering is part of the metric. Numeric 10 is below numeric 20, but lexicographic string `"10"` is below `"2"`. IEEE NaN is not an ordinary member of a total numeric order. Units, collation, timestamps, infinities, signed zero, and missing values need a canonical policy before ingestion because discarded information cannot repair the order later.

### Exact state and why summaries discard information

An exact implementation may retain all values and sort them, or maintain an order-statistic tree whose counts support rank selection. Either consumes state that grows with the number of distinct values or observations. A bounded-memory streaming summary deliberately makes multiple streams map to one state. It can therefore guarantee only properties that its retained evidence distinguishes.

Quantile sketches usually expose two dual queries:

- a **quantile query** takes $\phi$ or target rank and returns a value;
- a **rank query** takes a value $y$ and estimates how many observations are at most $y$.

An error definition should specify which interface the theorem covers. Inverting an approximate rank function to obtain a quantile is sound only under the stated monotonicity and boundary rules.

### Deterministic rank envelopes: the GK design

GK stores sorted tuples $(v_i,g_i,\Delta_i)$. The cumulative gaps give a certified minimum rank, while $\Delta_i$ gives remaining uncertainty:

$$
r_{\min}(v_i)=\sum_{j\le i}g_j,
\qquad
r_{\max}(v_i)=r_{\min}(v_i)+\Delta_i.
$$

On insertion, a new ordered value receives gap one and an uncertainty chosen from the current threshold; boundary values receive zero uncertainty. A compression step may delete a retained value by transferring its gap to its successor only when the successor's enlarged envelope remains admissible. The characteristic invariant is

$$
g_i+\Delta_i\le \lfloor2\varepsilon n\rfloor
$$

for compressible interior structure, with endpoints handled specially. A query scans cumulative minimum ranks and selects a retained value whose envelope brackets the target within tolerance. Greenwald and Khanna prove deterministic error at most $\varepsilon n$ and worst-case space $O(\bigl(\varepsilon^{-1}\log(\varepsilon n)\bigr))$ without knowing $n$ in advance [1].

The proof obligations are coupled. Sorted tuples alone do not suffice; an implementation must compute thresholds at the correct stream size, preserve endpoints, use the correct merge inequality and scan direction, and implement the paper's query rule. Moving a floor, changing a strict inequality, or compressing in another order needs a new proof or exhaustive evidence plus a retained limitation—not intuition that the change is harmless.

The original GK construction is a strong deterministic single-stream baseline. It should not be labeled fully mergeable merely because two tuple arrays can be sorted together. A merge must reconstruct valid rank envelopes and account for uncertainty contributed by the opposite summary; formal mergeability is a separate property [5].

### Randomized weighted compaction: the KLL design

Merge-and-reduce summaries replace rank envelopes with weighted samples. Level zero receives observations of weight one. When a level exceeds its scheduled capacity, sort its buffer, choose one parity, discard the other item in each adjacent pair, and promote retained items with doubled weight. An odd boundary item is handled by the algorithm's declared rule.

Two local facts drive the analysis. First, mass is conserved: each pair with total weight $2w$ becomes one representative of weight $2w$. Second, for any fixed query threshold, a fair parity choice makes the promoted pair's contribution to estimated rank unbiased. If both items lie on the same side of the query, the contribution is exact; if the query separates them, the contribution is either zero or $2w$, each with probability one half, around the true contribution $w$.

KLL is more than “occasionally discard half.” Its nonuniform level capacities, compaction schedule, random choices, and analysis control the sum of weighted rank errors. Karnin, Lang, and Liberty establish an $O((1/\varepsilon)\log\log(1/\delta))$-space randomized summary with matching dependence in their comparison-based model for failure probability $\delta$ [3]. A production implementation must identify the precise variant whose proof it claims; a finite compaction trace proves only that trace's mechanics.

<!-- bijux-verify: {"id":"weighted-compaction-mechanics","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"lower=[(1, 2), (3, 2), (6, 2), (8, 2)]\nupper=[(2, 2), (4, 2), (7, 2), (9, 2)]\nweights=8,8\nmedians=3,4\nrank_errors=1,0\n","stderr":""}} -->
```python
from math import ceil

values = [7, 1, 9, 3, 8, 2, 6, 4]

def compact_once(items, parity):
    ordered = sorted(items)
    assert len(ordered) % 2 == 0 and parity in (0, 1)
    return [(ordered[i], 2) for i in range(parity, len(ordered), 2)]

def weighted_quantile(summary, phi):
    target = ceil(phi * sum(weight for _, weight in summary))
    seen = 0
    for value, weight in sorted(summary):
        seen += weight
        if seen >= target:
            return value
    raise AssertionError("nonempty summary must answer")

lower = compact_once(values, 0)
upper = compact_once(values, 1)
answers = [weighted_quantile(s, 0.5) for s in (lower, upper)]
exact = sorted(values)
target = ceil(0.5 * len(values))
errors = [abs((exact.index(value) + 1) - target) for value in answers]
print(f"lower={lower}")
print(f"upper={upper}")
print(f"weights={sum(w for _, w in lower)},{sum(w for _, w in upper)}")
print(f"medians={answers[0]},{answers[1]}")
print(f"rank_errors={errors[0]},{errors[1]}")
```

This executable is a one-level mechanics experiment, not a KLL implementation. It checks conservation and shows two parity outcomes; it does not instantiate KLL's capacity schedule or establish its tail bound.

### Rank error and value error are different geometries

An additive rank guarantee says how far the returned item may move in the ordered population. It is distribution-free, but it says nothing about numerical spacing. A move of ten ranks can mean one microsecond in a dense latency region or hours across a tail gap. Conversely, a relative-value guarantee can be meaningful for latency magnitude while allowing many ranks in a dense plateau.

DDSketch targets relative value error for quantiles over a declared range and is fully mergeable in its model [4]. For the positive-value core, choose desired relative error $0<\alpha<1$ and

$$
\gamma=\frac{1+\alpha}{1-\alpha}.
$$

Bucket $i$ covers $[\gamma^{i-1},\gamma^i]$. Returning the harmonic midpoint

$$
c_i=\frac{2\gamma^i}{1+\gamma}
$$

gives worst endpoint-relative error

$$
\frac{c_i-\gamma^{i-1}}{\gamma^{i-1}}
=1-\frac{c_i}{\gamma^i}
=\frac{\gamma-1}{\gamma+1}=\alpha.
$$

Counts in logarithmic buckets can be added across compatible partitions. Negative values, zero, finite bucket ranges, collapsing, and floating-point boundary placement require the construction's explicit rules; the positive derivation does not silently cover them.

### Probability has a scope

For a randomized sketch, $\Pr(|\widetilde r-r|>\varepsilon n)\le\delta$ must name what is fixed and what is random. Is the claim for one quantile chosen independently of the sketch, all quantiles from one state, one state over its lifetime, or a fleet of states? Adaptive queries may invalidate a theorem proved for a fixed query.

If only a per-query failure bound is available and a dashboard makes $K$ nonadaptive claims, the union bound gives fleet failure at most $K\delta$. To target at most $\delta_{\mathrm{fleet}}$, a conservative allocation is $\delta\le\delta_{\mathrm{fleet}}/K$. Independence is not required for this inequality. It may be expensive, and a simultaneous-all-quantiles theorem may be a better fit, but reporting the per-query number alone is not honest fleet assurance.

### Merge, weights, updates, and windows

A mergeable summary must produce a state with the same declared guarantee as a valid construction over the union multiset. Compatible KLL-family states merge level buffers and then apply the specified compactions; weighted items represent their exact logical multiplicities. Merge order may change randomized output while remaining within the same probability law. Reproducible bytes, deterministic output, and distributionally valid merge are three different requirements.

Metadata is part of state: algorithm and implementation version, $\varepsilon$ and $\delta$ or $\alpha$, capacity schedule, random-seed policy, value type and order, unit, weight semantics, interpolation and boundary convention, window, partition coverage, and serialization schema. Reject mismatches rather than producing a precise-looking hybrid.

Positive integer weights can often be represented without literal repetition if the implementation and theorem support weighted compaction. Fractional weights change the rank population and require a defined weighted-quantile contract. Negative updates are not ordinary multiplicities: deletion can invalidate retained representatives and their weights. Likewise, a cumulative insertion-only sketch cannot exactly expire a sliding window. Window-specific algorithms, bounded time buckets with disclosed boundary error, or rebuild from retained data are honest alternatives.

### Engineering and validation

Validation needs exact oracles on bounded streams. For each stream, sort the accepted canonical values, enumerate target quantiles including boundaries, compute duplicate-aware rank intervals, and check the declared inequality. Exhaust permutations for small distinct sets because arrival order exercises compaction. Add ascending, descending, constant, alternating-extreme, heavy-duplicate, highly skewed, and tail-gap families. Test merge trees, retries, empty partitions, weight conservation, serialization round trips, incompatible metadata, and numerical bucket boundaries.

Randomized algorithms need more than a fixed seed. Fixed seeds make regression failures reproducible; a many-seed experiment measures only the tested distribution. A proof audit must still connect code paths to the analyzed algorithm. Measure memory, update latency, query latency, merge latency, allocation, and error jointly on representative and adversarial workloads, as experimental comparisons of quantile summaries emphasize [6].

Operationally, persist source offsets and summary state atomically or make replay idempotent. Expose accepted, rejected, late, missing, and weighted counts; compaction levels; retained items or buckets; parameter version; merge rejections; and rebuild status. Audit against exact bounded groups and stratified retained samples. When the error budget, range, or input policy is violated, return unavailable, fall back to an exact bounded computation, widen a disclosed interval, or rebuild—do not emit an unqualified percentile.

## Definitions and Notation

- $S=(x_1,\ldots,x_n)$: accepted ordered multiset stream, including multiplicity.
- $x_{(j)}$: $j$th order statistic, indexed from one.
- $\phi$: requested quantile fraction, normally in $(0,1]$.
- $r_\phi=\lceil\phi n\rceil$: this chapter's exact target-rank convention.
- $Q(\phi)=x_{(r_\phi)}$: exact lower empirical quantile.
- $L(y)$, $U(y)$: first and last feasible ranks of value $y$ under duplicates.
- $\varepsilon$: additive rank-error fraction.
- $\delta$: failure-probability budget for a declared scope.
- $\alpha$: relative-value error fraction.
- $(v_i,g_i,\Delta_i)$: GK retained value, rank gap, and additional rank uncertainty.
- $r_{\min}$, $r_{\max}$: certified lower and upper rank envelope.
- $\ell$: compactor level; its logical item weight is commonly $2^\ell$.
- $\gamma=(1+\alpha)/(1-\alpha)$: logarithmic bucket ratio in the positive DDSketch core.
- **Empirical quantile:** a statistic of the finite observed multiset, not a population-distribution parameter without further assumptions.
- **Interpolation:** an API rule returning a value between order statistics; it is separate from a sketch's rank theorem.
- **Simultaneous guarantee:** one probability statement covering a declared family of queries.

## Mechanisms, Invariants, or Proof Structure

### GK proof skeleton

The representation proof first establishes that each tuple's cumulative gaps and uncertainty enclose the true rank of its retained value. Insertion adds exactly one observation and assigns an admissible envelope. Compression removes a predecessor only when transferring its gap cannot exceed the allowed envelope width. Induction therefore preserves the invariant after every update. The query rule chooses a retained value whose envelope lies close enough to the target; the $2\varepsilon n$ width and scan inequalities yield at most $\varepsilon n$ returned-rank error. The space proof groups tuples by uncertainty bands and bounds the number retained in each band [1]. These are distinct obligations; checking the tuple count does not prove the rank result.

### Weighted-compaction proof skeleton

Consider a compacted adjacent pair $a\le b$, each of weight $w$, and a fixed rank query at threshold $q$.

- If $q<a$, both the original and compacted contribution below $q$ are zero.
- If $q\ge b$, the original contribution is $2w$ and either retained representative contributes $2w$.
- If $a\le q<b$, the original contribution is $w$; random lower parity contributes $2w$ and upper parity contributes zero, each with probability one half.

Thus the compaction error is zero outside a straddling pair and is $+w$ or $-w$ with equal probability inside it. Total represented weight is deterministically conserved. KLL's theorem bounds the weighted sum of such random errors across its scheduled levels [3]; arbitrary parity bias, shared randomness, capacity changes, or adaptive behavior cannot inherit that theorem without analysis.

### Relative-bucket proof skeleton

For positive bucket endpoints $a$ and $b=\gamma a$, choose $c=2ab/(a+b)$. The upper relative error from $a$ to $c$ equals the lower relative error from $b$ to $c$, both $(\gamma-1)/(\gamma+1)$. Substituting $\gamma=(1+\alpha)/(1-\alpha)$ yields $\alpha$. Count conservation and compatible bucket addition provide merge mechanics; range and collapsing policies determine whether the basic guarantee remains applicable [4].

### Review invariants

Before accepting a state, verify: total accepted mass equals represented mass; minimum and maximum policies are preserved; rank or value bounds use the configured convention; random and deterministic claims are labeled; merge metadata agree; serialization is versioned; the window and source coverage are complete; probability is budgeted over the actual query family; and empirical evidence is not promoted into a universal theorem.

## Alternatives and Trade-Offs

- **Exact sort or order-statistic tree:** exact and auditable, but state grows with data. Prefer it for bounded groups and threshold-adjacent consequential decisions.
- **GK:** deterministic distribution-free additive rank error and a strong reference design; update constants and merge requirements need careful engineering.
- **KLL:** excellent randomized rank-space trade-off and natural hierarchical compaction; requires probability governance, random-path testing, and variant fidelity.
- **Earlier buffer-and-collapse summaries:** historically important one-pass designs with explicit guarantees [2]; useful for understanding merge-and-reduce evolution, though newer constructions improve bounds.
- **q-digest:** hierarchical counts over a bounded integer universe and useful distributed aggregation semantics [7]; universe/range knowledge and value discretization are material.
- **DDSketch:** relative-value error and full mergeability suit positive, wide-range telemetry; it does not provide the same distribution-free additive rank contract as GK or KLL [4].
- **Empirical clustering summaries such as t-digest:** often useful for tails, but a named implementation's measured behavior must not be restated as a theorem it does not publish.
- **Reservoir sampling:** simple, mergeable with correct sampling weights, and supports many statistics; its quantile error is probabilistic and may require larger samples for a desired uniform rank bound.
- **Histograms:** provide interpretable distribution summaries and range counts; bin edges impose value error and may hide within-bin order.

Choose by decision loss. Database selectivity often wants rank/CDF control; latency alerting may care about relative magnitude; regulatory or contractual thresholds may require exact recomputation near the boundary. Memory, update rate, merge topology, supported values, reproducibility, deletions, and simultaneous-query scope can dominate asymptotic elegance.

## Failure Modes and Misconceptions

1. **“One percentile definition is standard.”** Libraries differ on ceiling, interpolation, endpoints, and ties. Version the convention.
2. **“One-percent rank error means one-percent value error.”** Gaps and heavy tails break that inference.
3. **“Randomized means usually accurate.”** State $\varepsilon$, $\delta$, and their exact scope.
4. **“Compaction conservation proves KLL.”** It proves a local invariant, not the capacity schedule or concentration theorem.
5. **“Any sorted tuple list is GK.”** Envelope construction, compression, endpoints, and query inequalities are proof-critical.
6. **“Merge means concatenate.”** Error and metadata must remain valid under the algorithm's merge operation.
7. **“Retries are harmless.”** Replaying an observation adds multiplicity unless ingestion is idempotent.
8. **“Weighted rows are just repeated rows.”** Only supported nonnegative integral semantics justify that equivalence.
9. **“A cumulative sketch can forget yesterday.”** Insertion-only summaries do not provide exact expiry or arbitrary deletion.
10. **“NaN sorts somewhere.”** A canonical reject, separate-count, or total-order policy is required.
11. **“A dashboard's p99 has per-query confidence.”** Thousands of repeated claims need simultaneous or fleet-level budgeting.
12. **“A percentile proves an SLO.”** Eligibility, time windows, missing traffic, aggregation, and contractual rules are separate.

## Worked Examples

### Example 1

**Situation.** The stream is $[9,1,5,5,5,20]$ and $\phi=0.5$.

**Reasoning.** Sorting gives $[1,5,5,5,9,20]$. With the chapter convention, $r=\lceil0.5\cdot6\rceil=3$ and $Q(0.5)=5$. For value 5, $L(5)=2$ and $U(5)=4$, so all three copies occupy the target-spanning interval.

**Conclusion.** Duplicate-aware ranks make 5 an exact answer without inventing an occurrence identity.

### Example 2

**Situation.** An API requests $\phi=0$ from the same nonempty stream.

**Reasoning.** The base definition uses $0<\phi\le1$ because $\lceil0\cdot n\rceil=0$ is not a one-indexed rank. If the API explicitly extends $Q(0)$ to the minimum, it returns 1. An empty stream still has no minimum.

**Conclusion.** Boundary behavior is policy and must be tested, not inferred from a formula outside its domain.

### Example 3

**Situation.** A GK tuple prefix has gaps $[1,3,2]$ and uncertainties $[0,2,4]$.

**Reasoning.** Cumulative minimum ranks are 1, 4, and 6. The third retained value therefore has envelope $[6,10]$. If the true target is rank 8, that tuple can represent it; if the target is 14, it cannot. Whether compression was legal additionally depends on the current $\lfloor2\varepsilon n\rfloor$ threshold and neighboring tuple.

**Conclusion.** GK tuples encode rank intervals, not approximate frequencies of their stored values.

### Example 4

**Situation.** One compactor receives sorted pairs $(1,2),(3,4),(6,7),(8,9)$ at weight one.

**Reasoning.** Lower parity retains $1,3,6,8$ at weight two; upper parity retains $2,4,7,9$ at weight two. Both represent total mass eight. Their lower-median answers are 3 and 4; relative to exact target rank four, the rank errors are one and zero.

**Conclusion.** Compaction conserves mass while randomizing rank error; one trace is not a tail-bound proof.

### Example 5

**Situation.** A thousand sorted values have ranks 1 through 999 equal to their ranks, but rank 1000 is $10^9$. A sketch promises $\varepsilon=0.01$ additive rank error for p99.

**Reasoning.** The target is rank 990 and the allowed interval reaches rank 1000. Returning $10^9$ can satisfy the rank contract even though the exact p99 is 990 and the numerical error is about $9.9999901\times10^8$.

**Conclusion.** Rank accuracy alone does not bound tail value error.

### Example 6

**Situation.** A positive logarithmic sketch needs $\alpha=0.01$ relative value error.

**Reasoning.** It uses $\gamma=(1.01)/(0.99)\approx1.020202$. For any basic bucket with endpoint ratio $\gamma$, the harmonic representative makes the two endpoint-relative errors equal to $(\gamma-1)/(\gamma+1)=0.01$.

**Conclusion.** The bucket ratio derives from the value-error contract; it is not an arbitrary histogram width.

### Example 7

**Situation.** A report exposes 100 quantiles for each of 1,000 tenants and wants the probability of any reported rank failure below $10^{-3}$, using only per-query bounds.

**Reasoning.** There are $K=100{,}000$ claims. A union-bound allocation requires per-query $\delta\le10^{-3}/10^5=10^{-8}$. Configuring $\delta=10^{-3}$ per query does not give the fleet claim.

**Conclusion.** Query multiplicity changes the probability budget by five orders of magnitude here.

### Example 8

**Situation.** Two partitions use the same KLL algorithm and nominal $\varepsilon$, but one sorts milliseconds as integers and the other stores seconds as floating-point values.

**Reasoning.** Level buffers may be mechanically mergeable, yet their values inhabit different units and encodings. Sorting the hybrid produces nonsense. The merge envelope must reject unit and value-schema mismatch before touching sketch state.

**Conclusion.** Semantic metadata is part of merge compatibility.

### Example 9

**Situation.** A 24-hour percentile service drops expired events from a cumulative compactor summary.

**Reasoning.** A promoted item may represent expired and live observations with no reversible membership record. Subtracting one from its weight neither identifies which value should remain nor reconstructs discarded alternatives. Use a window-aware algorithm, merge bounded time buckets with disclosed edge coverage, or rebuild from retained events.

**Conclusion.** Insertion-only weighted compaction does not support arbitrary deletion.

### Example 10

**Situation.** A p95 latency alert fires at an estimated 201 ms against a 200 ms threshold; the sketch's valid rank interval includes values from 190 to 215 ms.

**Reasoning.** The point estimate is not enough to assert violation. Recompute exactly from a bounded retained window, use conservative upper/lower decision rules specified in advance, or report the result as indeterminate. Also verify missing traffic, window closure, and eligibility before applying the alert policy.

**Conclusion.** Threshold-adjacent decisions need an uncertainty-aware fallback, not false precision.

## Cross-Program Connections

- **Data Structures Engineering:** ordered multisets, trees, buffers, compactors, and serialization implement the summary state.
- **Database Engineering:** optimizer histograms and selectivity estimates consume approximate CDF and quantile information.
- **Data Engineering:** event time, partitions, watermarks, replay, units, and late data define the measured population.
- **Data Architecture Engineering:** schema, metric definition, weighting, retention, and lineage determine semantic compatibility.
- **Distributed Systems Engineering:** merge trees, retries, checkpoints, replica determinism, and rolling upgrades govern distributed evidence.
- **Platform Engineering:** telemetry schemas, resource budgets, fallback, version negotiation, and fleet probability make summaries operable.
- **Security Engineering:** adversarial values, resource-exhaustion ranges, poisoning, privacy leakage, and threshold authority shape the threat model.
- **Algorithm Engineering:** [ALGE-075](./075-distinct-counting.md) covers support-size sketches; ALGE-077 next derives uniform streaming samples.

## References

1. Michael Greenwald and Sanjeev Khanna, “Space-Efficient Online Computation of Quantile Summaries,” *Proceedings of ACM SIGMOD 2001*, 58–66. DOI: [10.1145/375663.375670](https://doi.org/10.1145/375663.375670). Primary source for deterministic rank envelopes, error, and space; ACM and SIGMOD records checked 2026-09-05.
2. Gurmeet Singh Manku, Sridhar Rajagopalan, and Bruce G. Lindsay, “Approximate Medians and Other Quantiles in One Pass and with Limited Memory,” *Proceedings of ACM SIGMOD 1998*, 426–435. DOI: [10.1145/276304.276342](https://doi.org/10.1145/276304.276342). Primary source for one-pass buffer-and-collapse quantile summaries; IBM, ACM-linked, and proceedings records checked 2026-09-05.
3. Zohar Karnin, Kevin Lang, and Edo Liberty, “Optimal Quantile Approximation in Streams,” *57th IEEE Symposium on Foundations of Computer Science (FOCS 2016)*, 71–78. DOI: [10.1109/FOCS.2016.17](https://doi.org/10.1109/FOCS.2016.17). Primary source for KLL randomized compaction and optimal space dependence; official FOCS paper and author manuscript checked 2026-09-05.
4. Charles Masson, Jee E. Rim, and Homin K. Lee, “DDSketch: A Fast and Fully-Mergeable Quantile Sketch with Relative-Error Guarantees,” *Proceedings of the VLDB Endowment* 12(12), 2019, 2195–2205. DOI: [10.14778/3352063.3352135](https://doi.org/10.14778/3352063.3352135). Primary source for relative-value buckets, range, and mergeability; official PVLDB paper checked 2026-09-05.
5. Pankaj K. Agarwal, Graham Cormode, Zengfeng Huang, Jeff M. Phillips, Zhewei Wei, and Ke Yi, “Mergeable Summaries,” *Proceedings of ACM PODS 2012*, 23–34. DOI: [10.1145/2213556.2213562](https://doi.org/10.1145/2213556.2213562). Primary source for formal mergeability and quantile-summary transformations; ACM record checked 2026-09-05.
6. Lu Wang, Ge Luo, Ke Yi, and Graham Cormode, “Quantiles over Data Streams: An Experimental Study,” *Proceedings of ACM SIGMOD 2013*, 737–748. DOI: [10.1145/2463676.2465312](https://doi.org/10.1145/2463676.2465312). Research comparison of quantile implementations, workloads, and space--time--accuracy trade-offs; author and institutional records checked 2026-09-05.
7. Nisheeth Shrivastava, Chiranjeeb Buragohain, Divyakant Agrawal, and Subhash Suri, “Medians and Beyond: New Aggregation Techniques for Sensor Networks,” *Proceedings of ACM SenSys 2004*, 239–249. DOI: [10.1145/1031495.1031524](https://doi.org/10.1145/1031495.1031524). Primary source for q-digest and bounded-message distributed aggregation; author manuscript and proceedings metadata checked 2026-09-05.
8. J. Ian Munro and Mike Paterson, “Selection and Sorting with Limited Storage,” *Theoretical Computer Science* 12(3), 1980, 315–323. DOI: [10.1016/0304-3975(80)90061-4](https://doi.org/10.1016/0304-3975(80)90061-4). Primary source for limited-storage selection lower bounds; publisher metadata checked 2026-09-05.

## Exercises

### Exercise 1

For $S=[2,2,2,7,9,9,15]$, compute $Q(0.5)$, $Q(0.9)$, and the duplicate-aware rank intervals of 2 and 9 under this chapter's convention. State the behavior at $\phi=0$ and on the empty stream.

### Exercise 2

Prove total-weight conservation and unbiased fixed-threshold rank contribution for one randomized compaction of equal-weight adjacent pairs. Identify what this proof does not establish about KLL.

### Exercise 3

A service claims “1% accurate p99” from a randomized sketch. It accepts NaN, merges states with different units, retries non-idempotently, and publishes 50 quantiles for 20,000 hosts using a per-query $\delta=10^{-4}$. Diagnose the specification and implementation defects.

### Exercise 4

Design a distributed quantile service for latency with one-minute ingestion, 24-hour queries, and a mixture of tail dashboards and contractual thresholds. Specify quantile and error definitions, algorithm choices, metadata, merge, windows, validation, observability, probability, and fallback.

### Exercise 5

A hospital wants treatment-wait p90 by clinic and demographic group, with weights correcting a sampling design. Transfer the chapter's reasoning to propose an evidence and governance plan covering weighting, small groups, privacy, missing data, fairness comparisons, uncertainty, exact audit, and invalidation.

## Answers to the Exercises

### Answer 1

The sorted multiset is already shown and $n=7$. For $\phi=0.5$, $r=\lceil3.5\rceil=4$, so $Q(0.5)=7$. For $\phi=0.9$, $r=\lceil6.3\rceil=7$, so $Q(0.9)=15$. Value 2 occupies ranks $[1,3]$ because nothing is smaller and three values are at most 2. Value 9 occupies $[5,6]$ because four values are smaller and six are at most 9. The base domain excludes $\phi=0$; an explicitly documented extension returns the minimum 2. The empty stream has no quantile under either rule.

### Answer 2

Each pair has two items of weight $w$, hence mass $2w$. Retaining either item at weight $2w$ conserves that mass exactly. For a fixed threshold, a pair wholly below contributes $2w$ before and after, and a pair wholly above contributes zero. A straddling pair contributes $w$ before compaction; retaining its lower or upper member produces $2w$ or zero below the threshold with equal probability, whose expectation is $w$. Summing pairs gives unbiased estimated rank for that fixed threshold. This does not prove a concentration bound, simultaneous queries, a capacity schedule, odd-item handling, merge behavior, adaptive-query robustness, implementation fidelity, or KLL's space theorem.

### Answer 3

“1% accurate” must be replaced by an additive-rank, value, or relative-value contract with the p99 convention, stream population, window, and probability scope. NaN needs rejection, separate accounting, or a declared total order. Unit mismatch must reject merge. Non-idempotent retry changes multiplicity and therefore the target distribution; bind state atomically to source offsets or deduplicate. There are $50\times20{,}000=10^6$ published claims, so per-query $\delta=10^{-4}$ permits a union-bound fleet failure probability as high as 100, which is vacuous after capping at one. For a fleet target $10^{-4}$ using only per-query bounds, allocate at most $10^{-10}$ per query, or use an applicable simultaneous theorem and declare its scope. Then validate adversarial tails, duplicates, merge trees, and threshold fallbacks.

### Answer 4

Define accepted request latency in one unit, exclusions, NaN/infinity policy, event-time windows, lateness, multiplicity, lower quantile, and whether dashboards need rank or relative-value error. Use a mergeable rank sketch such as a faithful KLL variant for distribution/CDF dashboards, or a relative-value sketch for magnitude-sensitive tails; retain exact bounded data or recompute near contractual thresholds. Record algorithm/version, parameters, probability scope, unit, order, weights, random policy, window, source offsets, partition coverage, and serialization. Build compatible per-minute states and merge exactly the closed 24-hour buckets, disclosing partial-bucket policy; do not subtract cumulative sketches. Test exact oracles, ties, tail gaps, arrival orders, many seeds, merge shapes, replay, and upgrades. Observe counts, lateness, compaction/bucket range, merge rejection, and audit error. Budget probability over all exposed host/quantile/time claims. On missing data, range overflow, incompatibility, audit failure, or threshold overlap, return unavailable, widen a declared interval, or use exact fallback.

### Answer 5

Define a weighted empirical population from the approved sampling design; weights, inclusion probabilities, eligibility, clinic, demographic categories, time window, and tie convention must be versioned before sketching. Use only an algorithm whose weighted-quantile semantics and guarantee cover the nonnegative weights, and compare it against exact weighted order statistics on protected bounded samples. Small groups need minimum-data rules and wider uncertainty; sketch error is separate from sampling error, nonresponse bias, and missing-wait mechanisms. Apply approved privacy controls and query auditing because a sketch is not anonymization. Fairness comparisons should publish group definitions, coverage, both sampling and sketch uncertainty, sensitivity to missingness, and an exact threshold-adjacent review rather than rank point estimates alone. Independent statistical, clinical, privacy, and fairness review is required. Weight revisions, coding drift, consent or eligibility change, late or missing clinics, incompatible merges, probability-budget exhaustion, audit failure, privacy leakage, or evidence that nonresponse is differential invalidates release and triggers suppression or rebuild.
