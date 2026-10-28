---
module_id: ALGE-075
program: Algorithm Engineering
level: 2
module_number: 75
title: Distinct Counting
status: complete
last_verified: 2026-09-05
---

# Distinct Counting

## One-Page Review

### Governing question

How can a streaming system estimate the number of distinct canonical identities with bounded memory, and what do hashing, estimator range, merge semantics, windows, and downstream use do to that guarantee?

### Essential definitions

- For a stream $x_1,\ldots,x_T$, the **distinct count** or **cardinality** is $D=|\{x_t:1\le t\le T\}|$, also called frequency moment $F_0$.
- An insertion-only distinct summary is **duplicate-insensitive** when repeated copies of an identity leave its state unchanged after the first effective observation.
- An **exact set** stores canonical identities and reports its size; its memory grows with $D$.
- A **hash synopsis** maps each identity deterministically to a pseudorandom rank or bit string and retains selected order statistics or register maxima.
- A **$k$-minimum-values** (KMV) synopsis retains the $k$ smallest distinct hash ranks.
- A **relative-error** estimate targets $|\widehat D-D|\le\varepsilon D$ under a declared probability.
- **HyperLogLog** (HLL) partitions hashes into $m=2^p$ registers and records the maximum leading-zero rank in each register.
- A valid insertion-only **union merge** produces the same summary as inserting every identity from both inputs, under identical encoding and hashing.
- **Intersection estimation** is not the same operation as sketch intersection; inclusion–exclusion can amplify errors.
- A **hash collision** is equality of finite hash outputs for distinct canonical identities; it is separate from multiple identities updating the same sketch register.
- **Sparse** and **dense** representations are storage modes whose transition must preserve one logical sketch.

### Central model, mechanism, or theorem

Assume $D\ge k>2$ distinct identities receive independent continuous uniform ranks in $(0,1)$, and let $R=U_{(k)}$ be the $k$th smallest rank. Its order-statistic distribution is $\operatorname{Beta}(k,D-k+1)$. The KMV estimator

$$
\widehat D=\frac{k-1}{R}
$$

is unbiased because

$$
\mathbb E[R^{-1}]=\frac{D}{k-1}.
$$

Using $\mathbb E[R^{-2}]=D(D-1)/((k-1)(k-2))$ gives

$$
\operatorname{Var}(\widehat D)
=\frac{D(D-k+1)}{k-2},
\qquad
\frac{\operatorname{sd}(\widehat D)}{D}
=\sqrt{\frac{D-k+1}{D(k-2)}}.
$$

When fewer than $k$ distinct collision-free hashes are retained, their count is exact. The theorem assumes ideal continuous independent ranks. Finite hashes introduce collision risk, and production hash families may provide weaker independence or adversarial resistance.

HLL uses different statistics. It splits a uniform hash into register index and suffix, stores the maximum suffix leading-zero rank per register, and combines registers with a calibrated harmonic-mean estimator [4]. Under the original idealized range, its typical relative standard error is approximately $1.04/\sqrt m$; small and large ranges need estimator-specific treatment.

### Critical invariants

- Identity canonicalization, tenant namespace, and population boundary precede hashing.
- The same identity always receives the same hash within a logical sketch version.
- Hash algorithm, width, salt or seed, precision, estimator, and encoding accompany persisted state.
- Duplicate replay is harmless only if duplicates denote the same canonical identity and updates are insertion-only.
- KMV retains distinct ranks and exactly the smallest $k$; HLL registers change only by maxima.
- Union merges require compatible metadata; HLL uses registerwise maximum, and KMV keeps the union's bottom $k$ ranks.
- Deletion, expiry, and sliding windows are unsupported unless the selected construction explicitly represents them.
- Probability scope distinguishes one final estimate, repeated estimates, many groups, and continuous tracking.
- Hash-domain exhaustion and estimator-range limits trigger rejection, wider hashing, or a documented fallback.
- Exact audit data is independent of the approximate ingestion and implementation path.

### Common failures

Common failures are counting raw spellings instead of canonical identities; confusing distinct count with row count; assuming duplicate-insensitivity fixes semantically duplicated IDs; using a weak or changing hash; ignoring finite-hash collisions; merging sketches with different precision, seeds, or encodings; deleting from max registers; subtracting HLL states; estimating small intersections by subtracting three noisy large estimates; applying one-estimate error to millions of groups; hiding sparse-to-dense bias changes; serializing registers without version metadata; and letting an approximate estimate decide irreversible access, billing, or enforcement without verification.

### Compact example

Suppose six distinct identities hash to normalized ranks $0.08,0.19,0.31,0.43,0.70,0.91$, and $k=4$. KMV retains the first four and uses $R=0.43$, giving $\widehat D=3/0.43\approx6.98$. Repeated observations do not change the retained ranks. The estimate is high on this realization; unbiasedness is an expectation across valid random rankings, not exactness on each stream.

### Connections

[ALGE-074](./074-streaming-frequency-estimation.md) estimates multiplicities but does not thereby estimate $F_0$. [ALGE-076](../ROADMAP.md#block-08--online-streaming-and-dynamic-algorithms) treats quantiles. Database Engineering uses cardinality estimates for planning, while Data Architecture Engineering determines which canonical identity is actually being counted.

## Governing Question

Given a stream with arbitrary duplication and a cardinality too large for an exact set, how do we define the identity set, select and analyze an order-statistic or register sketch, merge distributed state, quantify uncertainty over the real query surface, and prevent an approximate count from acquiring unjustified authority?

The mathematical problem is short: estimate $D$, the size of the support of a frequency vector. The engineering problem is not. “Unique user” may mean account, device, authenticated principal, household, or privacy-preserving token. A late merge may combine windows twice. A hash upgrade may make old and new registers incomparable. A deletion cannot be undone from a maximum without additional history.

Distinct summaries solve a memory problem after semantics are fixed. They do not perform entity resolution, deduplication across unstable IDs, privacy protection, temporal correction, or exact set algebra. A rigorous design binds estimator claims to identity, update model, hash assumptions, range, probability surface, state version, and downstream decision.

## Why This Matters

Distinct counts drive database selectivity, capacity planning, telemetry, experimentation, security monitoring, audience measurement, and scientific pipelines. Exact sets can dominate memory because their state grows with cardinality. Probabilistic summaries compress this state dramatically and often merge across partitions without transferring raw identities.

That convenience invites overreach. A 1% relative standard error is not a deterministic 1% bound. Ten million group estimates create a different failure surface from one total. A union operation is natural for max-register sketches, while intersection can be numerically unstable. A 64-bit hash that seems enormous can have material collision probability at billion-scale cardinality.

The estimator is also only as correct as identity and ingestion. If one person rotates identifiers, the sketch correctly counts identifiers rather than people. If two tenants use the same unnamespaced key, the sketch collapses them. The first design document is therefore a population and identity contract, not a register layout.

## Prerequisites and Retrieval

Retrieve sets, probability density functions, expectation, variance, order statistics, the beta distribution, hashing, birthday bounds, and floating-point arithmetic. Review [ALGE-066](./066-randomized-selection-and-sampling.md), [ALGE-068](./068-monte-carlo-and-las-vegas-algorithms.md), and [ALGE-074](./074-streaming-frequency-estimation.md).

This chapter owns insertion-only $F_0$, KMV analysis, HLL mechanisms, finite hashing, union, intersection hazards, and operational evidence. Entity resolution belongs to Data Architecture Engineering; event-time pipeline mechanics belong to Data Engineering; advanced signed-stream $F_0$ algorithms are identified but not replaced by HLL folklore.

## Learning Objectives

After completing this module, you should be able to:

1. define cardinality over a canonical identity and bounded population;
2. decide when an exact set is preferable;
3. derive the KMV estimator's expectation and variance;
4. trace HLL register updates and explain its estimator shape;
5. size HLL precision from relative standard error while preserving caveats;
6. quantify finite-hash collision risk and estimator range;
7. merge compatible KMV and HLL summaries for union;
8. explain deletion, window, intersection, and continuous-tracking boundaries;
9. validate implementations with independent exact and distributional evidence; and
10. govern approximate counts used in consequential decisions.

## Core Exposition

### Define what distinct means before counting

Let canonicalization $c$ map a source record to an identity in universe $U$ or reject it. For accepted records $x_1,\ldots,x_T$, define

$$
S=\{c(x_t):1\le t\le T\},\qquad D=|S|.
$$

State the population: tenant, dataset, event-time interval, filters, consent state, and schema version. State whether missing or invalid identities are rejected, counted as one sentinel, or assigned separate provenance. These choices can change $D$ far more than sketch error.

Distinct record IDs, users, devices, sessions, values, and tuples are different metrics. Composite identities need unambiguous length-delimited encoding; string concatenation can make `(ab,c)` collide semantically with `(a,bc)` before hashing. Unicode, case, locale, numeric normalization, and namespace rules must be deterministic.

Duplicate-insensitivity means repeated insertion of the same canonical identity leaves a set synopsis unchanged. It does not mean two rotating device IDs for one person are deduplicated, nor does it decide whether a reissued identifier denotes the same entity.

### Use exact state when its bound is honest

An exact hash set gives exact cardinality, enumeration, deletions, and arbitrary set operations subject to identity semantics. It is the default when cardinality has a safe bound, exactness is required, or stored identities are already needed. Estimate complete memory, including keys, allocator overhead, load factor, and persistence—not only payload bytes.

Approximation is justified when exact state exceeds a declared budget or distributed transfer cost. Retaining an exact sparse representation before switching to a dense sketch can improve small-cardinality behavior. The transition must be deterministic, tested at the boundary, and semantically one summary rather than two counts that can overlap.

Even with sketches, maintain exact state for small consequential groups when feasible. A global probabilistic summary and exact exception ledger can align cost with risk, but promotion, demotion, replay, and merge rules must prevent double counting.

### Derive KMV from an order statistic

Assign each distinct identity an independent rank $U_i\sim\operatorname{Uniform}(0,1)$ and retain the $k$ smallest distinct ranks. Duplicates map to the same rank and do not alter the synopsis. If fewer than $k$ ranks exist, $D<k$ and the retained count is exact under collision-free hashing.

For $D\ge k$, the $k$th order statistic $R=U_{(k)}$ has density

$$
f_R(r)=\frac{D!}{(k-1)!(D-k)!}r^{k-1}(1-r)^{D-k},
\quad 0<r<1.
$$

Integrating $r^{-1}f_R(r)$, or using beta-function ratios, gives

$$
\mathbb E[R^{-1}]
=\frac{B(k-1,D-k+1)}{B(k,D-k+1)}
=\frac{D}{k-1}.
$$

Thus $(k-1)/R$ is unbiased for $k>1$. For $k>2$,

$$
\mathbb E[R^{-2}]
=\frac{D(D-1)}{(k-1)(k-2)}.
$$

Substituting into $\operatorname{Var}((k-1)/R)$ yields $D(D-k+1)/(k-2)$. At large $D$ relative to $k$, relative standard deviation approaches $1/\sqrt{k-2}$. This variance is not a deterministic interval and does not include finite-hash collisions.

### Verify KMV mechanics within the evidence boundary

This executable uses a small fixed permutation-like hash solely for deterministic mechanics. It does not supply cryptographic, independence, collision, or production-range evidence.

<!-- bijux-verify: {"id":"kmv-order-statistic-mechanics","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"true_distinct=6 bottom=(22, 32, 49, 59) estimate=5.186\nsmall_exact=2\nduplicate_replay_same=True\nmerged_bottom=(22, 32, 49, 59)\ninvalid_k=rejected\n","stderr":""}} -->
```python
def rank(item):
    return ((37 * item + 11) % 101) + 1


def kmv(items, k):
    if k < 2:
        raise ValueError("k must be at least two")
    ranks = sorted({rank(item) for item in items})
    retained = tuple(ranks[:k])
    if len(retained) < k:
        return retained, float(len(retained)), True
    threshold = retained[-1] / 102
    return retained, (k - 1) / threshold, False


items = (1, 2, 1, 3, 4, 5, 6, 2)
bottom, estimate, exact = kmv(items, 4)
print(f"true_distinct={len(set(items))} bottom={bottom} estimate={estimate:.3f}")
_, small_estimate, small_exact = kmv((1, 1, 2), 4)
print(f"small_exact={int(small_estimate) if small_exact else 'no'}")
replayed, _, _ = kmv(items + items, 4)
print(f"duplicate_replay_same={replayed == bottom}")
left, _, _ = kmv((1, 2, 3), 4)
right, _, _ = kmv((3, 4, 5, 6), 4)
merged = tuple(sorted(set(left) | set(right))[:4])
print(f"merged_bottom={merged}")
try:
    kmv(items, 1)
except ValueError:
    print("invalid_k=rejected")
```

The trace verifies deduplication, truncation, exact sparse state, idempotent replay, union mechanics, and validation on CPython. Because its small hash is deterministic and finite, its numerical estimate is an illustration, not a sample from the theorem's ideal family.

### Understand the HLL mechanism and estimator

HLL hashes an identity to a fixed-width uniform bit string [4]. The first $p$ bits select one of $m=2^p$ registers. Let $\rho$ be one plus the number of leading zero bits in the remaining suffix. Update the selected register by

$$
M_j\leftarrow\max(M_j,\rho).
$$

A long zero prefix is rare, so a large register suggests many distinct hashes reached that register. HLL combines all registers through the harmonic-like raw estimate

$$
E=\alpha_m m^2\left(\sum_{j=1}^{m}2^{-M_j}\right)^{-1},
$$

where $\alpha_m$ and range corrections belong to the specified estimator. The original algorithm uses empty-register linear counting at small range and a finite-hash correction at large range. Later engineering changes use sparse representations and empirically corrected estimators [5]. “HLL” without variant, precision, hash width, and estimator version is incomplete.

Under the original ideal-hash asymptotic regime, typical relative standard error is approximately $1.04/\sqrt m$. With $p=14$, $m=16{,}384$, giving about $0.008125$ or $0.8125\%$. That is a standard deviation model, not a worst-case bound or a 99% interval. Bias and error change at range transitions and under nonideal hashes.

### Treat finite hashing as a separate approximation

The ideal model assigns independent continuous values, so distinct identities almost surely have distinct ranks. A $b$-bit hash has only $2^b$ outputs. For $D$ uniformly hashed distinct identities, the expected number of colliding pairs is

$$
\frac{D(D-1)}{2^{b+1}},
$$

and the birthday approximation gives collision probability about $1-\exp(-D(D-1)/2^{b+1})$ when the ratio is moderate. At $D=10^9$ and $b=64$, expected colliding pairs are about 0.0271 and the probability of at least one is about 2.67%. A collision does not necessarily shift a rounded estimate visibly, but “64-bit collision-free” is false.

Use enough bits for scale and consequence, and account for storage or computation. Hash quality includes uniformity, avalanche behavior, deterministic cross-language encoding, seed management, and resistance to chosen inputs. A secret keyed hash may reduce adversarial targeting but is not a proof of the estimator's required independence and creates key-rotation obligations.

Register rank also has a finite ceiling. An all-zero suffix needs a convention, commonly suffix length plus one. Counter width and estimator large-range logic must cover the advertised domain. Reject impossible precision or hash-width combinations rather than silently saturating.

### Merge unions, but do not pretend subtraction exists

For compatible HLL sketches, the registerwise maximum represents inserting the union: for each register, the maximum rank across $A\cup B$ is the maximum of the two register maxima. This operation is associative, commutative, and idempotent. Compatibility requires identical identity encoding, hash algorithm and seed, hash width, precision, register convention, and version.

For KMV, take the set union of retained hashes and keep its smallest $k$. Any discarded input hash exceeds that input's $k$th rank and cannot enter the global bottom $k$ ahead of $k$ retained hashes from the same input. The operation is likewise associative, commutative, and idempotent under compatible ranking.

Neither sketch supports state subtraction. HLL maxima forget which identity established a register, and KMV discards ranks beyond $k$. Estimating intersection by $|A|+|B|-|A\cup B|$ subtracts noisy estimates. If $|A|=|B|=10^6$ and $|A\cup B|=1.99\times10^6$, the true intersection is 10,000. Independent 1% scale errors can contribute tens of thousands of absolute error and even a negative result. Use a method designed and evaluated for set similarity or intersections [7].

### Distinguish insertion-only from deletion and windows

Repeating an insertion is idempotent because the canonical hash and max or bottom-$k$ state do not change. Deleting one occurrence should not remove an identity if other occurrences remain, and deleting the last occurrence would require knowing multiplicity. Plain HLL cannot reverse a maximum; plain KMV cannot reveal a discarded successor rank after deletion.

Signed-update $F_0$ is a different streaming problem with dedicated algorithms [6]. Counting inserted identities and deleted identities separately and subtracting their cardinality estimates is incorrect because cardinality is nonlinear. Tombstones, reference counts for retained identities, or periodic rebuilds may support bounded operational cases but require their own guarantees.

A sliding window expires identities and may later reintroduce them. Use an explicitly windowed distinct structure, time-bucketed sketches with understood union overcoverage, or exact state. Event-time lateness, watermarks, and corrections define whether an estimate is preliminary. A daily reset is not a 24-hour sliding window.

### Allocate uncertainty across the query surface

An estimator's variance or success probability may concern one estimate after one prefix. A service can expose millions of groups, periodic refreshes, and continuous tracking. Selection of the largest observed estimates creates winner's-curse bias even when individual estimates are unbiased. Repeatedly querying until a desired value appears invalidates a one-shot interpretation.

Specify whether the requirement is expected squared error, relative standard error, a confidence interval, high-probability relative error, simultaneous accuracy over groups, or strong tracking across time. Allocate failure probability across tenants, windows, metrics, retries, and releases. Validate correlations introduced by shared hashes or merged partitions.

Near zero, relative error is awkward; exact sparse state is often preferable. At thresholds, define a gray zone and exact verification. Report estimate, algorithm and version, precision, range, window completeness, and uncertainty semantics together.

### Validate implementation and system behavior

Use exact sets as independent oracles on generated and retained test data. Cover $D=0$, $D=1$, just below and above sparse transition, register-index boundaries, maximum rank, hash collisions injected deliberately, duplicate floods, skew, uniform identities, partition overlap, and serialized round trips.

For randomized evidence, preregister cardinalities and distributions, use independent frozen seeds, and report bias, relative-error quantiles, empirical interval coverage, and failures—not only mean error. Test each range and estimator transition. Compare merged summaries with a single summary over the union for state equality where the construction promises it.

End-to-end audits need independent identity and ingestion evidence. A sketch and exact set fed by the same truncated partition agree while both are wrong. Reconcile source partitions, offsets, checksums, rejects, schema versions, and window closure. Measure update, estimate, merge, serialization, rebuild, and recovery latency plus total resident memory.

### Operate cardinality as versioned evidence

Persist algorithm family, implementation version, estimator version, precision, hash algorithm and width, seed or key identifier, key schema, namespace, window, source coverage, sparse/dense mode, register encoding, checksum, and creation time. Reject incompatible state. A rolling upgrade may need dual writing and a fresh window because registers under different hashes cannot be translated.

Guard source completeness, update lag, invalid identities, hash and register range, sparse transition, corrupted state, incompatible merges, missing partitions, audit bias, error quantiles, and downstream threshold volume. Retain a rebuild source when the service obligation requires recovery.

Fallback to exact counting for bounded critical groups, widened uncertainty, delayed action, or unavailable status. Approximate counts can guide planning and screening. Billing, access removal, fraud sanctions, or scientific claims need verification and governed authority proportionate to consequences.

## Definitions and Notation

- $x_t$: source item at stream position $t$.
- $c(x)$: canonicalization function from source item to accepted identity.
- $S$: set of canonical identities in the population.
- $D=|S|=F_0$: true distinct count.
- $\widehat D$: estimated distinct count.
- $U_i$: ideal continuous uniform rank for distinct identity $i$.
- $U_{(k)}=R$: $k$th order statistic among distinct ranks.
- $k$: KMV retained-rank capacity and order-statistic index.
- $b$: finite hash width in bits.
- $p$: HLL register-index bits; $m=2^p$ is register count.
- $M_j$: maximum observed rank in HLL register $j$.
- $\rho$: one plus the number of leading zero suffix bits.
- $\alpha_m$: HLL estimator calibration constant for register count $m$.
- $V$: number of empty HLL registers in small-range correction.
- $\varepsilon$: required relative-error magnitude when such a guarantee is stated.
- $\delta$: probability budget for failure under the specified query scope.

## Mechanisms, Invariants, or Proof Structure

### KMV proof obligations

Establish distinct uniform ranks, the beta order-statistic density, inverse first and second moments, the unbiased estimator, its variance, exact sparse behavior, and restrictions from finite hashing. Do not infer a deterministic interval from variance.

### HLL mechanism obligations

Establish deterministic identity hashing, index/rank bit separation, register maxima, estimator and correction version, precision range, duplicate idempotence, and finite register behavior. Keep empirical calibration distinct from ideal-hash analysis.

### Algebra obligations

Prove compatible union by bottom-$k$ selection or registerwise maximum. Check associativity, commutativity, idempotence, and metadata compatibility. Do not claim deletion, subtraction, or accurate small intersections from union closure.

### Evidence obligations

Separate analytic distribution claims, executable mechanics, finite collision calculation, seeded simulation, exact-oracle comparison, ingestion reconciliation, and operational monitoring.

## Alternatives and Trade-Offs

| Method | State and answer | Strength | Principal boundary |
|---|---|---|---|
| Exact set | Every identity; exact $D$ | Enumeration and deletion | Memory grows with $D$ |
| Bitmap or linear counting | Occupied hash buckets | Simple at bounded range | Saturation and range-sensitive bias |
| Flajolet–Martin | Extreme hash-bit patterns | Seminal tiny summary [1] | High variance needs aggregation |
| KMV | Bottom-$k$ distinct ranks | Unbiased order-statistic estimate; union | Stores hashes; finite collisions; insertion-only core |
| LogLog | Register maxima with geometric mean | Compact register family [3] | Estimator and range behavior matter |
| HyperLogLog | Register maxima with harmonic estimator | Compact, fast union | Approximate, versioned corrections, no subtraction |
| Exact sparse plus HLL | Exact small range then dense registers | Broad operating range [5] | Transition and serialization complexity |
| Signed-stream $F_0$ algorithm | Specialized linear or sampled state | Supports update models beyond insertion | More complex theory and implementation [6] |

Choose exact state when possible. KMV is attractive when retained hashes also support overlap estimators. HLL is attractive for compact cardinality and union. A product library's named variant may differ materially from the original paper, so validate its documented estimator and serialization rather than assuming a universal “HLL accuracy.”

## Failure Modes and Misconceptions

- **“Distinct means deduplicated people.”** A sketch deduplicates canonical keys, not real-world entities.
- **“Duplicate-insensitive means exactly-once ingestion is irrelevant.”** Duplicates with changed IDs still inflate cardinality.
- **“Unbiased means close on every run.”** It is an expectation over the stated random experiment.
- **“Relative standard error is a hard error bound.”** It is a dispersion measure under a model.
- **“A 64-bit hash cannot collide.”** Billion-scale birthday risk is measurable.
- **“Register collision is a bug.”** Many hashes share registers by design; full-hash identity collisions are a separate loss.
- **“HLL union allows HLL subtraction.”** Maximum state has no inverse.
- **“Inclusion–exclusion gives accurate intersections.”** Subtracting large noisy estimates can overwhelm a small result.
- **“Same precision means mergeable.”** Hashing, seed, identity, estimator, encoding, and window must match.
- **“A reset creates a sliding window.”** It creates a tumbling lifetime within reset boundaries.
- **“Sparse and dense are separate estimates.”** They must be representations of one state with a tested transition.
- **“Approximation error dominates.”** Identity, coverage, duplication, and window defects can be much larger.

## Worked Examples

### Example 1

**Situation.** A configuration field has at most 64 legal values.

**Reasoning.** A 64-bit exact bitmap records membership, merges by bitwise OR, and reports population count exactly. HLL would require more state and introduce estimator uncertainty.

**Conclusion.** Known small universes favor exact representations.

### Example 2

**Situation.** Records `A,A,a` arrive under case-sensitive and case-insensitive identity rules.

**Reasoning.** Case-sensitive canonicalization yields two identities, `A` and `a`; case folding yields one. Both sketches can be mechanically correct while reporting different metrics.

**Conclusion.** Canonicalization is part of the cardinality definition.

### Example 3

**Situation.** Six ranks have fourth order statistic $R=0.43$.

**Reasoning.** With $k=4$, KMV reports $(4-1)/0.43\approx6.98$. Repeated occurrences preserve the same bottom ranks. This realization overestimates the true six.

**Conclusion.** KMV is approximate per realization despite an unbiased ideal-model estimator.

### Example 4

**Situation.** KMV retains $k=1024$ ranks while $D$ is much larger.

**Reasoning.** Relative standard deviation approaches $1/\sqrt{k-2}=1/\sqrt{1022}\approx3.13\%$. Quadrupling retained ranks roughly halves asymptotic dispersion, while storage roughly quadruples.

**Conclusion.** Order-statistic accuracy has the familiar inverse-square-root trade-off.

### Example 5

**Situation.** An 8-bit HLL toy uses $p=2$, and a hash begins `10 000100`.

**Reasoning.** Prefix `10` selects register 2 under zero-based indexing. The suffix has three leading zeros before one, so $\rho=4$; update sets that register to the maximum of its old value and 4. Repeating the identity changes nothing.

**Conclusion.** Index bits choose a substream; suffix rarity supplies magnitude evidence.

### Example 6

**Situation.** HLL uses $p=14$.

**Reasoning.** There are $m=16{,}384$ registers. The original asymptotic relative standard error approximation is $1.04/128=0.008125$, or $0.8125\%$. This does not include hash, identity, range-transition, or implementation defects.

**Conclusion.** Precision sizing begins, but does not end, with $1.04/\sqrt m$.

### Example 7

**Situation.** One billion distinct identities use a uniform 64-bit hash.

**Reasoning.** Expected colliding pairs are approximately $10^{18}/2^{65}\approx0.0271$. The birthday approximation gives at least one collision with probability $1-e^{-0.0271}\approx2.67\%$.

**Conclusion.** Hash width must be justified against scale and consequence.

### Example 8

**Situation.** Three partitions share HLL metadata and contain overlapping identities.

**Reasoning.** Registerwise maximum is associative, commutative, and idempotent, so merge order and retry do not change the union state. If one partition uses another seed, corresponding registers no longer summarize the same substreams.

**Conclusion.** Algebraic merge safety depends on semantic compatibility.

### Example 9

**Situation.** Two million-element sets have a union of 1.99 million.

**Reasoning.** Their intersection is only 10,000. Inclusion–exclusion combines three estimates near one or two million; 1% errors can create roughly 40,000 absolute error in an adverse combination, exceeding the signal.

**Conclusion.** Small intersections need an estimator designed for overlap, not casual subtraction.

### Example 10

**Situation.** A service deletes expired events from a 24-hour HLL.

**Reasoning.** A register maximum does not reveal whether the expiring identity established it or whether another live identity supports the same rank. Decrementing or clearing the register can undercount. Use a window-aware construction, bucketed overapproximation, or rebuild.

**Conclusion.** Plain HLL insertion state cannot implement exact expiry.

## Cross-Program Connections

- **Data Architecture Engineering:** entity identity, namespace, consent, and canonical tuples determine the counted set.
- **Data Engineering:** partitions, offsets, event time, watermarks, replay, and rebuild determine source coverage.
- **Database Engineering:** query optimizers consume distinct-value estimates and magnify estimation errors through plan choice.
- **Distributed Systems Engineering:** semilattice-like union, retries, checkpoints, and rolling upgrades govern replicated state.
- **Security Engineering:** chosen-input hashing, privacy leakage, poisoning, and enforcement thresholds govern threat and authority.
- **Platform Engineering:** metadata envelopes, compatibility, telemetry, resource budgets, and fallback make sketches operable.
- **Data Structures Engineering:** sets, bitmaps, heaps, packed registers, and serialization implement exact and approximate state.
- **Algorithm Engineering:** [ALGE-074](./074-streaming-frequency-estimation.md) handles $F_1$-based frequency estimates; ALGE-076 continues to rank summaries for quantiles.

## References

1. Philippe Flajolet and G. Nigel Martin, “Probabilistic Counting Algorithms for Data Base Applications,” *Journal of Computer and System Sciences* 31(2), 1985, 182–209. DOI: [10.1016/0022-0000(85)90041-8](https://doi.org/10.1016/0022-0000(85)90041-8). Primary source for probabilistic distinct counting; publisher record checked 2026-09-05.
2. Ziv Bar-Yossef, T. S. Jayram, Ravi Kumar, D. Sivakumar, and Luca Trevisan, “Counting Distinct Elements in a Data Stream,” *RANDOM 2002*, LNCS 2483, 1–10. DOI: [10.1007/3-540-45726-7_1](https://doi.org/10.1007/3-540-45726-7_1). Primary source for distinct-stream approximation and order-statistic methods; proceedings record checked 2026-09-05.
3. Marianne Durand and Philippe Flajolet, “LogLog Counting of Large Cardinalities,” *ESA 2003*, LNCS 2832, 605–617. DOI: [10.1007/978-3-540-39658-1_55](https://doi.org/10.1007/978-3-540-39658-1_55). Primary source for the LogLog register estimator; Springer record checked 2026-09-05.
4. Philippe Flajolet, Éric Fusy, Olivier Gandouet, and Frédéric Meunier, “HyperLogLog: The Analysis of a Near-Optimal Cardinality Estimation Algorithm,” *DMTCS Proceedings AH, Analysis of Algorithms 2007*, 127–146. [Official proceedings paper](https://dmtcs.episciences.org/3545). Primary source for HLL analysis; official DMTCS record checked 2026-09-05.
5. Stefan Heule, Marc Nunkesser, and Alexander Hall, “HyperLogLog in Practice: Algorithmic Engineering of a State of the Art Cardinality Estimation Algorithm,” *EDBT 2013*, 683–692. DOI: [10.1145/2452376.2452456](https://doi.org/10.1145/2452376.2452456). Primary source for sparse representation and empirical estimator corrections; author and proceedings records checked 2026-09-05.
6. Daniel M. Kane, Jelani Nelson, and David P. Woodruff, “An Optimal Algorithm for the Distinct Elements Problem,” *PODS 2010*, 41–52. DOI: [10.1145/1807085.1807094](https://doi.org/10.1145/1807085.1807094). Primary source for optimal-space distinct estimation and signed-stream extensions; ACM and author records checked 2026-09-05.
7. Kevin S. Beyer, Rainer Gemulla, Peter J. Haas, Berthold Reinwald, and Yannis Sismanis, “Distinct-Value Synopses for Multiset Operations,” *Communications of the ACM* 52(10), 2009, 87–95. DOI: [10.1145/1562764.1562787](https://doi.org/10.1145/1562764.1562787). Research synthesis for KMV, overlap, and multiset operations; ACM and author records checked 2026-09-05.
8. Pankaj K. Agarwal, Graham Cormode, Zengfeng Huang, Jeff M. Phillips, Zhewei Wei, and Ke Yi, “Mergeable Summaries,” *PODS 2012*, 23–34. DOI: [10.1145/2213556.2213562](https://doi.org/10.1145/2213556.2213562). Primary source for formal mergeability of streaming summaries; ACM record checked 2026-09-05.

## Exercises

### Exercise 1

Define row count, distinct record ID, distinct account, and distinct person. Explain why a cardinality sketch cannot reconcile these definitions after ingestion.

### Exercise 2

Derive the KMV expectation and variance from the beta density. State the restrictions on $D$, $k$, hash ranks, and sparse exact behavior.

### Exercise 3

An HLL service expects up to $3\times10^9$ identities, uses 64-bit hashes and $p=14$, calls $1.04/\sqrt m$ a “guaranteed error,” and subtracts daily sketches for expiry. Diagnose each defect and propose bounded corrections.

### Exercise 4

Design a cardinality service across 500 partitions. Specify identity, window, estimator, hash, precision, metadata, sparse transition, union, probability scope, persistence, audit, upgrade, fallback, and deletion behavior.

### Exercise 5

A public-health team wants approximate distinct-patient counts by rare condition and region, with suppression below a privacy threshold. Design an evidence and governance plan covering identity, uncertainty, small groups, privacy, overlap, late records, exact verification, disclosure, and invalidation.

## Answers to the Exercises

### Answer 1

Row count is the number of accepted records including duplicates. Distinct record ID counts unique event or row identifiers. Distinct account counts canonical account keys, so several records per account collapse. Distinct person requires an entity-resolution policy relating accounts and identifiers to people. A sketch sees only the canonical bytes presented to it and discards identity detail; it cannot later decide that two keys were one person or one reused key represented two people. Define and version canonicalization before hashing, and rebuild when the semantic mapping changes.

### Answer 2

For $D\ge k$ independent continuous uniform ranks, $R=U_{(k)}$ has density $D!r^{k-1}(1-r)^{D-k}/((k-1)!(D-k)!)$. Beta-function ratios give $E[R^{-1}]=D/(k-1)$ and, for $k>2$, $E[R^{-2}]=D(D-1)/((k-1)(k-2))$. Therefore $\widehat D=(k-1)/R$ is unbiased and its variance is $(k-1)^2E[R^{-2}]-D^2=D(D-k+1)/(k-2)$. The variance expression requires $k>2$ and $D\ge k$. With fewer than $k$ retained distinct collision-free hashes, report their exact number. Finite hashes, insufficient independence, and adaptive adversaries require separate analysis.

### Answer 3

With $p=14$, $m=16{,}384$ and $1.04/\sqrt m=0.8125\%$ is an asymptotic relative standard-error approximation, not a deterministic guarantee. At three billion identities, 64-bit expected colliding pairs are about $9\times10^{18}/2^{65}\approx0.244$, so collision probability is material; use a justified wider hash and compatible estimator range. Validate small, intermediate, and large cardinalities for the exact implementation. Plain HLL cannot subtract yesterday's maxima or expire identities; use explicit time buckets with declared boundary overcoverage, a window-aware structure, or rebuild from retained data. Publish probability and tracking scope rather than “guaranteed error.”

### Answer 4

Define tenant-qualified canonical identity and event-time population with lateness and closure. Choose HLL for compact union or KMV when retained ranks serve overlap needs; record estimator version, hash algorithm and width, one shared seed or key ID, precision, encoding, register/rank convention, sparse mode, window, partition coverage, checksum, and version. Use exact sparse state below a tested threshold. Merge compatible states only by register maxima or union-bottom-$k$, checking associativity, idempotence, overlap, empty and missing partitions, and single-stream parity. Allocate uncertainty across all published groups and times. Persist atomically with source offsets, audit against an independent exact stratified sample and bounded exact fixtures, and dual-write or restart windows for incompatible upgrades. Reject deletion unless the construction supports it; otherwise bucket or rebuild. Fallback to exact bounded groups, delayed estimates, widened uncertainty, or unavailable status.

### Answer 5

Define patient identity under approved linkage and count only authorized, tenant- and region-scoped canonical tokens; rotating tokens and cross-provider duplicates need governed resolution before hashing. Rare groups should remain exact inside a protected system when feasible because relative uncertainty and inclusion–exclusion instability are largest there. Privacy suppression is not supplied by HLL: apply an approved disclosure-control or differential-privacy mechanism with its own budget after validating the count, and prevent repeated differencing queries. Treat region and condition overlap with a designed estimator or exact secure computation, not noisy subtraction. Expose window completeness and correct late records under a versioned policy. Independently verify threshold-adjacent groups, restrict raw access, log queries and releases, and require human statistical/privacy review. Linkage changes, consent changes, late-data surges, missing providers, hash or estimator upgrades, audit failures, small-cell leakage, or privacy-budget exhaustion invalidate release and trigger suppression or rebuild.
