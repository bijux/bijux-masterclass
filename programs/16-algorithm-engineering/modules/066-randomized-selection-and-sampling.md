---
module_id: ALGE-066
program: Algorithm Engineering
level: 2
module_number: 66
title: Randomized Selection and Sampling
status: complete
last_verified: 2026-09-05
---

# Randomized Selection and Sampling

## One-Page Review

### Governing question

How can randomized algorithms select an order statistic or draw a representative sample while making the probability space, rank semantics, bias, runtime, reproducibility, and adversarial assumptions precise enough to prove and test?

### Essential definitions

- The **$k$th order statistic** is the element of zero-based rank $k$ in sorted order; duplicate policy must be explicit.
- **Randomized Quickselect** partitions around a sampled pivot and recurses only into the partition containing the requested rank.
- A **uniform permutation** assigns probability $1/n!$ to each ordering of $n$ distinct positions.
- A **uniform $k$-subset** assigns probability $1/\binom nk$ to each size-$k$ subset.
- Sampling **with replacement** makes independent draws from the original population; sampling **without replacement** changes later probabilities.
- A **bounded uniform draw** returns each integer in $[0,b)$ with probability $1/b$.
- **Modulo bias** appears when a source range is mapped to a non-dividing target range by remainder.
- A **sampling frame** is the exact population from which selection is possible.
- A **randomness transcript** records enough source identity or draws to reproduce one execution.

### Central model, mechanism, or theorem

Randomized Quickselect chooses a pivot uniformly from the current $m$ elements, partitions into values less than, equal to, and greater than it, and follows only the rank-containing side. If the pivot rank falls in the middle half, the next active size is at most $3m/4$. That event has probability at least $1/2$, so constant expected trials shrink the problem by a constant factor. Summing expected partition work over geometrically shrinking sizes gives expected $O(n)$ work. A fixed bad pivot sequence can still cause $\Theta(n^2)$ work.

For partial Fisher–Yates, iteration $i$ swaps position $i$ with a uniform position from $i$ through $n-1$. Every ordered length-$k$ sample has probability

$$
\frac1n\frac1{n-1}\cdots\frac1{n-k+1}=\frac{(n-k)!}{n!},
$$

so ignoring order yields a uniform $k$-subset.

### Critical invariants

- Rank range, comparator, duplicate and missing-value semantics are fixed before selection.
- Every pivot is sampled uniformly from the current active positions under the proved algorithm.
- Partition sizes conserve all active elements, and rank adjustment matches the discarded prefix.
- Every bounded draw is unbiased; rejection handles source-range remainders.
- Without-replacement sampling never selects one position twice.
- Sampling-frame construction precedes randomization and is independently auditable.
- Seeds support replay but do not prove independence, unpredictability, or distributional correctness.
- Worst-case fallback, work budget, and adversarial-input policy are part of service behavior.

### Common failures

Common failures include mixing zero- and one-based ranks; losing duplicates during set conversion; selecting a pivot by biased remainder; claiming worst-case linear time for randomized Quickselect; reusing one random key and colliding; shuffling with a fixed full-range swap at every index; treating seeded pseudorandomness as cryptographic; sampling from only readily available records; using row order or partition completion as hidden randomness; comparing observed frequencies without a power or multiplicity plan; and logging sensitive raw random draws or sampled identities unnecessarily.

### Compact example

To sample two positions uniformly from four, partial Fisher–Yates makes a bounded draw from four choices, then from three. Each ordered pair has probability $1/4\cdot1/3=1/12$. Each unordered pair has two orders and therefore probability $2/12=1/6=1/\binom42$.

### Connections

[ALGE-065](./065-local-search.md) uses randomized starts and move choices. [ALGE-067](../ROADMAP.md#block-07--approximation-heuristics-and-randomized-algorithms) uses random insertion order to simplify evolving geometry. [ALGE-077](../ROADMAP.md#block-08--online-streaming-and-dynamic-algorithms) owns reservoir sampling for unknown-length streams.

## Governing Question

Given an array, dataset, or population description, how do we select a rank or sample using randomness while proving the target distribution and expected cost, defending against bad random paths and adversarial inputs, and preserving enough evidence to reproduce observed behavior?

Randomized selection and statistical sampling share a requirement: write down the probability space before writing code. A random-looking implementation may have the wrong rank, wrong population, wrong inclusion probabilities, or correct distribution with unacceptable tail latency.

## Why This Matters

Order statistics support quantiles, robust summaries, pivoting, top-$k$ thresholds, and load shedding. Sampling supports audits, experimentation, approximate processing, distributed diagnosis, and randomized algorithms. Full sorting or scanning every downstream record can waste work when only one rank or a bounded representative set is needed.

Randomness trades deterministic control for distributional guarantees. Expected linear time does not cap one request. Uniform selection from an encoded array does not imply representativeness of the real population. Reproducibility, independence, and unpredictability are different properties. Production systems must state which one they need.

The durable method separates four layers: deterministic state transformation, the abstract random draws it consumes, the concrete generator that supplies them, and the evidence used to support the theorem and deployment claim.

## Prerequisites and Retrieval

Retrieve partitioning and comparison invariants, expectation and indicator variables, conditional probability, geometric series, permutations and combinations, rejection sampling, pseudorandom generators, stable identifiers, and exact integer arithmetic. Retrieve [ALGE-006](./006-best-worst-expected-and-amortized-cost.md) for cost quantifiers and [ALGE-061](./061-approximation-ratios-and-guarantees.md) for claim discipline.

This chapter covers finite-array randomized selection, uniform permutations and subsets, weighted and stratified sampling concepts, bounded-integer generation, evidence, and production controls. Streaming reservoirs belong to ALGE-077. Randomized incremental geometry belongs to ALGE-067, and the general Monte Carlo/Las Vegas taxonomy belongs to ALGE-068.

## Learning Objectives

After completing this module, you should be able to:

1. specify rank, comparator, duplicates, and mutation semantics for selection;
2. derive the partition and rank-adjustment invariant of Quickselect;
3. prove expected linear work under uniform independent pivots;
4. distinguish expected cost from worst-case and tail guarantees;
5. prove partial Fisher–Yates produces uniform ordered samples and subsets;
6. implement unbiased bounded draws from fixed-width random words;
7. distinguish with-replacement, without-replacement, weighted, and stratified designs;
8. separate generator reproducibility, statistical quality, and cryptographic unpredictability;
9. validate randomized code with deterministic transcripts and distributional tests; and
10. publish sampling-frame, inclusion-probability, seed, version, and failure evidence honestly.

## Core Exposition

### Define selection semantics first

For sequence $A$ of length $n$, zero-based selection requires $0\le k<n$ and returns a value $x$ such that fewer than or equal to $k$ elements are strictly less than $x$, and at least $n-k$ elements are greater than or equal to $x$. Equivalently, $x$ equals `sorted(A)[k]` under the declared total ordering.

Duplicates make a three-way partition preferable: $L=\{a:a<p\}$, $E=\{a:a=p\}$, and $G=\{a:a>p\}$. If $k<|L|$, continue in $L$; if $k<|L|+|E|$, return $p$; otherwise continue in $G$ with rank $k-|L|-|E|$. Conservation requires $|L|+|E|+|G|=m$ for active size $m$.

Define behavior for NaN, incomparable mixed types, locale-sensitive text, nulls, and user comparators. A comparator that is not transitive can make “rank” incoherent. Decide whether input may be mutated; in-place partitioning reduces allocation but creates ownership and rollback obligations.

### Analyze randomized Quickselect

Choose a pivot uniformly among current positions. Partition in $\Theta(m)$ time and recurse on at most one side. Unlike Quicksort, work does not branch into both partitions. A pivot whose sorted rank lies between $m/4$ and $3m/4$ leaves at most $3m/4$ active elements. At least half the pivot positions are in that middle range.

Let a **successful shrink event** mean choosing such a pivot. Its expected waiting time is at most two trials when draws are fresh and uniform. Between successful events, active size does not increase. Charging the expected constant number of partitions at sizes $n,3n/4,(3/4)^2n,\ldots$ gives

$$
\mathbb E[T(n)]
\le c'\sum_{j\ge0}n(3/4)^j
=4c'n
=O(n).
$$

This is an expectation over the pivot choices for each fixed input. It is not a deterministic upper bound. Consistently choosing the smallest element on sorted input produces partition sizes $n-1,n-2,\ldots,1$ and $\Theta(n^2)$ comparisons.

Independence assumptions must match the generator and call pattern. An adversary that sees pivots before constructing later data can violate an oblivious-input analysis. Randomizing once and exposing the seed may allow repeatable denial-of-service inputs.

### Engineer selection against bad paths

Set a work or depth budget rather than trusting expectation for latency-critical calls. On exhaustion, switch to a deterministic worst-case-linear selection algorithm, heap-based selection, or full sort according to constants and mutation constraints. The result remains exact; only the route changes. A fallback is part of the complexity theorem and must use the same rank/comparator semantics.

Three-way partitioning collapses large equal regions immediately. Stable partitioning costs additional memory; unstable in-place partitioning changes element order. If callers care which equal record is returned, extend the comparator with a stable identifier or specify that any equal-key record is acceptable.

For multiple quantiles, repeatedly invoking independent Quickselect can duplicate work. Multi-selection partitions once and routes several ranks. Full sorting may win when the requested rank count is large, data is reused, or library sort is heavily optimized. Benchmark crossover points on representative data without changing semantic contracts.

### Prove uniform sampling without replacement

The modern in-place Fisher–Yates algorithm processes position $i$ and draws $j$ uniformly from $\{i,\ldots,n-1\}$. Swap positions $i,j$. After iteration $i$, the prefix of length $i+1$ is an ordered sample without replacement, uniformly distributed among all such prefixes.

Proof by product: any particular ordered length-$k$ sequence of distinct original positions requires one choice from $n$, then one from $n-1$, through $n-k+1$. Its probability is $(n-k)!/n!$. Every unordered subset has exactly $k!$ orderings, so its probability is

$$
k!\frac{(n-k)!}{n!}=\frac1{\binom nk}.
$$

Stop after $k$ iterations when only a sample is needed. This uses $O(k)$ random draws and $O(n)$ storage if the population array already exists. Sparse remapping can avoid copying a large immutable population, but its map invariant must emulate the same swaps exactly.

The common incorrect loop draws $j$ from the entire $[0,n)$ range at every position. Different permutations then have different numbers of generating paths. Visual disorder is not a proof of uniformity.

### Use a reproducible abstract random source

The executable example injects a deterministic transcript of already-valid bounded draws. That transcript is a test fixture, not a random generator. It makes partition and swap behavior exactly replayable while keeping probability generation outside deterministic algorithm logic.

<!-- bijux-verify: {"id":"selection-and-partial-shuffle","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"select value=5 rounds=3 inspected=13\nsample=('E', 'B', 'D') remainder=('C', 'A') draws=3\nout_of_range=rejected\n","stderr":""}} -->
```python
class DrawTape:
    def __init__(self, values):
        self.values = iter(values)
        self.count = 0

    def below(self, bound):
        value = next(self.values)
        self.count += 1
        if not 0 <= value < bound:
            raise ValueError("bounded draw outside declared range")
        return value


def randomized_select(values, rank, draws):
    if not 0 <= rank < len(values):
        raise IndexError("rank outside sequence")
    active = list(values)
    rounds = inspected = 0
    while True:
        pivot = active[draws.below(len(active))]
        less, equal, greater = [], [], []
        for value in active:
            (less if value < pivot else greater if value > pivot else equal).append(value)
        rounds += 1
        inspected += len(active)
        if rank < len(less):
            active = less
        elif rank < len(less) + len(equal):
            return pivot, rounds, inspected
        else:
            rank -= len(less) + len(equal)
            active = greater


def partial_shuffle(values, size, draws):
    if not 0 <= size <= len(values):
        raise ValueError("sample size outside population")
    result = list(values)
    for i in range(size):
        j = i + draws.below(len(result) - i)
        result[i], result[j] = result[j], result[i]
    return tuple(result[:size]), tuple(result[size:])


select_tape = DrawTape([2, 0, 1])
value, rounds, inspected = randomized_select([9, 1, 7, 3, 5, 3], 3, select_tape)
print(f"select value={value} rounds={rounds} inspected={inspected}")

sample_tape = DrawTape([4, 0, 1])
sample, remainder = partial_shuffle(tuple("ABCDE"), 3, sample_tape)
print(f"sample={sample} remainder={remainder} draws={sample_tape.count}")
try:
    partial_shuffle((1, 2), 1, DrawTape([2]))
except ValueError:
    print("out_of_range=rejected")
```

### Generate bounded integers without modulo bias

Suppose a source produces each integer in $[0,M)$ uniformly and target bound is $b$. Returning $R\bmod b$ is uniform only when $b$ divides $M$. Write $M=qb+r$, with $0\le r<b$. Then $r$ residues occur $q+1$ times and the remaining residues occur $q$ times.

Rejection mapping accepts only a region whose size is a multiple of $b$. For example, with source $[0,256)$ and $b=6$, accept values below 252 and return remainder modulo 6; reject 252–255 and redraw. Each result has exactly 42 preimages. Expected draws are $256/252$, close to one.

Fixed-width multiplication methods can avoid division while remaining unbiased, but their proof still identifies and rejects a remainder region. Use a vetted bounded-draw primitive where possible and record its generator and library version. Avoid floating multiplication such as `floor(U*b)` when the source's finite precision, endpoints, and large bounds are unclear.

### Distinguish sampling designs

With replacement, $k$ uniform draws from $n$ positions create $n^k$ equally likely ordered samples, and positions may repeat. Without replacement, the inclusion probability of every position in a uniform size-$k$ subset is $k/n$, but inclusion indicators are dependent. This dependence reduces variance for many population estimators.

Weighted sampling must define whether weights are selection probabilities per draw, target inclusion probabilities, or priorities in a without-replacement design. Sequentially renormalizing remaining weights produces one valid design but not every desired set distribution. Zero, negative, infinite, or NaN weights require rejection or documented semantics. Large dynamic ranges need numerically stable sums or exact integer totals.

Stratified sampling partitions the frame before sampling and assigns sample sizes per stratum. It can guarantee coverage and reduce variance when strata are meaningful. Estimates then require design weights; concatenating unequal-rate stratum samples and taking an unweighted mean is biased for the population mean.

Cluster and systematic sampling have still different dependence. “Random sample” is incomplete without design, frame, unit, replacement, inclusion probabilities, and estimator.

### Separate algorithmic randomness from data representativeness

Uniformly sampling the rows present in a table proves uniformity over those rows, not over users, events, devices, or time. Missing ingestion partitions, deduplication errors, survivorship, access filters, and snapshot drift alter the sampling frame before the first random draw.

Define the unit of analysis. Sampling events overrepresents high-activity users if the claim concerns users. Sampling stored rows after retries can overrepresent failed operations. Build and version a canonical frame or use inclusion probabilities that model the multi-stage design.

Distributed data creates coordination choices. Assigning independent random priorities to stable record IDs and taking the global smallest priorities can implement a uniform subset when priorities are independent, continuous, and ties are handled without bias. Finite priorities can collide; include a secondary independent draw or a stable-ID rule whose effect is analyzed. Taking equal sample counts from unequal partitions is generally not globally uniform.

### Specify the random generator contract

A pseudorandom generator expands a finite state into a deterministic stream. A seed plus exact algorithm, version, stream derivation, and call order can reproduce results. A seed alone is insufficient when libraries change, workers consume draws in different orders, or rejection causes variable draw counts.

Statistical quality means generated sequences satisfy relevant distributional properties to the needed precision. Cryptographic unpredictability additionally resists prediction given observations and partial state. Simulation and algorithmic randomization often need reproducibility; security tokens, lotteries, and adversarial allocation may need a cryptographically secure generator and protected entropy. Do not use a fast simulation generator merely because frequency tests pass.

Parallel systems should derive independent logical streams from stable domain-separated keys such as job, trial, and partition identifiers, using a documented splittable or counter-based construction. Adding worker number to a seed is not automatically an independence proof. Schedule-dependent shared generators destroy replay and can create accidental overlap.

### Analyze cost, tails, and adversaries

State the random variable being bounded: comparisons, partitions, bytes moved, random words, rejections, or wall time. Expected $O(n)$ Quickselect allows rare quadratic paths. Markov's inequality gives weak tails; stronger selection algorithms use sampled pivot ranges, fallback, or deterministic pivots to control high percentiles.

Sampling runtime also has tails when rejection probability is high. For bounded integer generation, the accepted fraction should be calculated for every supported bound and word width. For weighted rejection samplers, one underestimated envelope can invalidate correctness; one very loose envelope can make runtime unusable.

Adversaries may choose input before the seed, after learning the algorithm, after observing previous outputs, or adaptively during execution. These models differ. Hash randomization, hidden seeds, periodic reseeding, or deterministic worst-case fallback address different threats. State the threat model rather than saying “randomization prevents worst cases.”

### Validate deterministic mechanics and statistical behavior

Use injected draw transcripts to cover every branch: smallest and largest pivots, duplicate blocks, empty sides, invalid ranks, zero/full sample sizes, repeated rejection, and generator exhaustion. Compare selection with sorting and samples with a reference enumerator on exhaustive small domains.

For a population of size $n$, enumerate all valid bounded-draw transcripts for small $n$ and count outputs. This can prove the implementation maps an abstract uniform source to equally many paths per permutation or subset. It does not test the concrete generator.

Distribution tests can detect gross bias but cannot prove absence of bias. Predeclare statistics, significance levels, sample size, multiple-test correction, and seeds. A failed test may indicate code, generator, or test assumptions; a passed test supplies finite evidence only. Prefer exact combinatorial enumeration for small mapping logic and established generator analyses for the source.

### Publish reproducible and privacy-aware evidence

Record algorithm and version, input/frame digest, rank or sample-size semantics, comparator, replacement design, inclusion probabilities, generator family/version, stream derivation, seed or protected seed reference, draw count, rejection count, fallback, work count, output digest, and verification result.

Raw seeds and samples may be sensitive. A seed can reveal future draws; sampled row identifiers can disclose membership. Restrict access, rotate security-sensitive state, and retain hashed or encrypted transcripts according to policy. Reproducibility for an authorized audit does not require public disclosure.

On cancellation, Quickselect may have mutated input without producing a result; document rollback or ownership. Partial Fisher–Yates has a valid prefix sample only if the stop count was decided independently of observed sampled values. Data-dependent early stopping changes the design and needs sequential analysis.

## Definitions and Notation

Let $n$ be population size, $k$ either a zero-based rank or sample size as explicitly labeled, $A$ an active sequence, $p$ a pivot, $L,E,G$ its three partitions, $R$ a random source word, $b$ a target bound, and $\pi_i$ the inclusion probability of unit $i$.

- An **order statistic** is a value identified by position in sorted order.
- A **pivot transcript** is the sequence of bounded pivot positions consumed.
- A **random permutation** is a distribution over position orderings, not merely a scrambled-looking array.
- An **inclusion probability** is the probability a unit appears at least once in the sample.
- A **design weight** is commonly the reciprocal of inclusion probability for estimation.
- **Domain separation** derives distinct random streams for distinct logical purposes.
- A **fallback** is a bounded alternative invoked when the randomized path exceeds policy.
- An **oblivious adversary** fixes input without observing the current random choices.

## Mechanisms, Invariants, or Proof Structure

### Selection partition invariant

The active multiset is partitioned without loss into less, equal, and greater values. Rank remains unchanged when following `less` and decreases by `len(less)+len(equal)` when following `greater`. Returning from `equal` satisfies the original order-statistic contract.

### Expected-shrink argument

A uniformly chosen pivot lands in the middle half with probability at least one half. Expected constant attempts reach such a pivot, successful sizes shrink geometrically, and linear partition costs sum to expected linear work. The statement is conditional on fixed input and valid pivot draws.

### Partial-shuffle invariant

After $i$ iterations, the prefix is a uniform ordered sample of $i$ distinct original positions; the suffix contains every unselected position once. A uniform choice from the suffix extends every prefix with equal conditional probability.

### Randomness-evidence invariant

The deterministic algorithm consumes declared bounded draws; the mapping from raw source to bounded draws is unbiased; stream derivation matches independence assumptions; and the recorded transcript/version can reproduce the observed route without being mistaken for proof of the distribution.

## Alternatives and Trade-Offs

| Method | Benefit | Risk | Evidence required |
|---|---|---|---|
| Randomized Quickselect | Expected linear single-rank work | Quadratic bad path | Partition proof and work controls |
| Deterministic linear selection | Worst-case linear | Larger constants/complexity | Grouping and pivot proof |
| Full sorting | Reusable ordered result | $O(n\log n)$ work | Comparator and sort validation |
| Partial Fisher–Yates | Exact uniform subset from array | Mutation and $O(n)$ storage frame | Bounded-draw and induction proof |
| With-replacement draws | Simple independent samples | Duplicates and different variance | Draw and estimator contract |
| Weighted sampling | Unequal inclusion | Ambiguous set distribution | Exact design and numeric checks |
| Stratified sampling | Coverage and variance control | Requires weighted estimation | Allocation and inclusion records |
| Random priorities | Distributed mergeability | Collisions and frame drift | Priority source and tie proof |

## Failure Modes and Misconceptions

- **“Expected linear means linear deadline.”** Rare quadratic Quickselect paths remain.
- **“Any pivot randomness defeats adversaries.”** Exposure and adaptivity determine the claim.
- **“Duplicates are harmless.”** Two-way partitions can stall or distort rank adjustment.
- **“Remainder makes a uniform bounded integer.”** It is biased unless ranges divide exactly.
- **“A shuffle that looks mixed is uniform.”** Uniformity requires equal path probabilities.
- **“Without replacement means independent.”** Inclusion events are dependent.
- **“A seed reproduces everything.”** Generator version and draw schedule also matter.
- **“Uniform rows represent users.”** The sampling frame and unit define representativeness.
- **“Equal partition samples are globally uniform.”** Partition sizes must influence inclusion.
- **“Passing a frequency test proves correctness.”** It is finite detection evidence only.
- **“Random means secure.”** Predictability requirements are stronger than statistical appearance.
- **“A partial sample is always valid on cancellation.”** Value-dependent stopping changes inclusion.

## Worked Examples

### Example 1

**Situation.** Select zero-based rank 3 from `[9, 1, 7, 3, 5, 3]`.

Sorted order is `[1, 3, 3, 5, 7, 9]`, so the answer is 5. Pivot 7 leaves four smaller values; pivot 1 leaves three greater candidates after rank becomes 2; pivot 5 has two smaller active values and is returned.

**Conclusion.** Three-way partition and rank adjustment preserve duplicates correctly.

### Example 2

**Situation.** Every pivot on sorted length-$n$ input is the smallest active value while selecting the maximum.

Partition work is proportional to $n+(n-1)+\cdots+1=n(n+1)/2$, which is $\Theta(n^2)$. The answer remains exact.

**Conclusion.** Randomization changes expected cost, not correctness or worst-case path length.

### Example 3

**Situation.** A source uniform on bytes is mapped to six outcomes using `byte % 6`.

Because $256=42\cdot6+4$, residues 0–3 have 43 preimages and 4–5 have 42. Accepting only bytes below 252 gives exactly 42 preimages each.

**Conclusion.** Rejection removes measurable modulo bias.

### Example 4

**Situation.** Sample two positions without replacement from four by partial shuffle.

There are $4\cdot3=12$ equally likely ordered prefixes. Each of six unordered pairs appears in two orders, giving probability $2/12=1/6$.

**Conclusion.** Ordered-prefix uniformity implies uniform subsets.

### Example 5

**Situation.** Draw twice with replacement from three items.

There are nine equally likely ordered outcomes. The probability of seeing item A at least once is $1-(2/3)^2=5/9$, not $2/3$; duplicate `(A,A)` is possible.

**Conclusion.** Per-draw probability and sample inclusion probability differ.

### Example 6

**Situation.** Two strata contain 900 and 100 people; 90 and 50 are sampled respectively.

Inclusion probabilities are 0.1 and 0.5. An unweighted sample mean overrepresents the small stratum. Population estimation weights sampled units by reciprocals 10 and 2 under the declared design.

**Conclusion.** Stratification requires design-aware estimation.

### Example 7

**Situation.** Four equal-sized samples are taken from partitions containing 10, 100, 1,000, and 10,000 rows.

Row inclusion probabilities differ by factors of ten: $k/10$, $k/100$, $k/1000$, and $k/10000$ when feasible. Concatenation is not a global uniform row sample.

**Conclusion.** Distributed sampling must account for partition sizes or merge global priorities.

### Example 8

**Situation.** Two parallel trials use the same generator seed and identical call schedule.

They produce identical samples, contributing no independent replication. Distinct worker-number seeds may still have undocumented relationships; domain-separated supported streams are preferable.

**Conclusion.** Different labels do not by themselves establish random-stream independence.

### Example 9

**Situation.** Quickselect reaches a partition-work budget of $8n$ without returning.

Switch to a deterministic selector or sort the remaining active region, adjust rank under the same invariant, and report the fallback. The answer remains exact and latency no longer depends on unlimited favorable pivots.

**Conclusion.** A governed fallback converts an expectation into bounded service behavior.

### Example 10

**Situation.** A uniform database-row sample contains few mobile users.

Audit shows the mobile ingestion partition was missing from the snapshot. The random mapping was correct over the stored frame, but the frame did not represent the claimed event population.

**Conclusion.** Algorithmic uniformity cannot repair frame coverage bias.

## Cross-Program Connections

- **Algorithm Engineering:** [ALGE-065](./065-local-search.md) consumes randomized starts; [ALGE-067](../ROADMAP.md#block-07--approximation-heuristics-and-randomized-algorithms) analyzes random construction order; [ALGE-077](../ROADMAP.md#block-08--online-streaming-and-dynamic-algorithms) handles unknown-length streams.
- **Probability and Statistics:** owns estimators, variance, confidence, sequential stopping, and survey-design inference beyond the algorithmic mapping.
- **Data Engineering:** owns frame completeness, snapshot lineage, distributed partitions, deduplication, and unit-of-analysis transformations.
- **Security Engineering:** owns entropy, cryptographic generators, seed protection, unpredictability, and transcript disclosure risk.
- **Concurrent and Parallel Programming:** owns reproducible stream derivation, schedule independence, and deterministic reductions.
- **Software Testing:** owns transcript injection, exhaustive small mappings, metamorphic checks, statistical test plans, and failure replay.
- **Platform Engineering:** owns generator/library versions, resource budgets, cancellation, protected configuration, and audit retention.

## References

1. C. A. R. Hoare, “Algorithm 65: Find,” *Communications of the ACM* 4(7), 321–322, 1961, [doi:10.1145/366622.366647](https://doi.org/10.1145/366622.366647). Primary partition-selection source; ACM DOI record checked 2026-09-05.
2. Robert W. Floyd and Ronald L. Rivest, “Expected Time Bounds for Selection,” *Communications of the ACM* 18(3), 165–172, 1975, [doi:10.1145/360680.360691](https://doi.org/10.1145/360680.360691). Primary selection analysis; author and DBLP records checked 2026-09-05.
3. Manuel Blum, Robert W. Floyd, Vaughan Pratt, Ronald L. Rivest, and Robert E. Tarjan, “Time Bounds for Selection,” *Journal of Computer and System Sciences* 7(4), 448–461, 1973, [doi:10.1016/S0022-0000(73)80033-9](https://doi.org/10.1016/S0022-0000(73)80033-9). Primary deterministic worst-case-linear selection source.
4. Paul E. Black, [“Fisher–Yates Shuffle”](https://xlinux.nist.gov/dads/HTML/fisherYatesShuffle.html), NIST Dictionary of Algorithms and Data Structures, entry dated 2005-12-19. Official algorithm reference checked 2026-09-05.
5. Daniel Lemire, “Fast Random Integer Generation in an Interval,” *ACM Transactions on Modeling and Computer Simulation* 29(1), 2019, [doi:10.1145/3230636](https://doi.org/10.1145/3230636). Primary bounded-integer generation source; ACM record checked 2026-09-05.
6. Donald E. Knuth, *The Art of Computer Programming, Volume 2: Seminumerical Algorithms*, 3rd edition, Addison-Wesley, 1997. Random numbers, permutations, sampling, and algorithmic analysis reference.
7. Luc Devroye, [*Non-Uniform Random Variate Generation*](https://luc.devroye.org/rnbookindex.html), Springer, 1986. Author-hosted text; rejection, discrete, weighted, and non-uniform sampling reference checked 2026-09-05.
8. Michael Mitzenmacher and Eli Upfal, *Probability and Computing*, 2nd edition, Cambridge University Press, 2017, [doi:10.1017/CBO9781316651083](https://doi.org/10.1017/CBO9781316651083). Randomized-algorithm probability and tail-analysis reference.

## Exercises

### Exercise 1

State a precise zero-based order-statistic contract with duplicates. Derive all three Quickselect rank transitions and identify the assumptions used by expected-linear analysis.

### Exercise 2

Trace randomized Quickselect on `[8, 2, 6, 2, 9, 4]` for rank 2 with pivot values 6 and then 2. Show every partition, adjusted rank, returned value, and partition-inspection count.

### Exercise 3

A 32-bit generator supplies uniform words and code returns `word % 10`. Quantify the bias and design an unbiased rejection mapper, including its accepted region and expected draw count.

### Exercise 4

Compare full shuffle, partial Fisher–Yates, with-replacement draws, and distributed random priorities for selecting 1,000 records from one billion. Address distribution, work, memory, merging, ties, frame construction, reproducibility, and privacy.

### Exercise 5

A fraud-review service samples equal counts from shards, stops early when it sees five suspected cases, publishes the sample as representative, and stores a public seed. Design a rigorous algorithmic, statistical, security, and operational correction with explicit evaluation criteria.

## Answers to the Exercises

### Answer 1

For sequence $A$ of length $n$ under a total comparator and $0\le k<n$, return a value equal to `sorted(A)[k]`, retaining duplicate multiplicity. Partition around pivot into $L,E,G$. Continue in $L$ when $k<|L|$; return the pivot value when $|L|\le k<|L|+|E|$; otherwise continue in $G$ with $k'=k-|L|-|E|$. Expected-linear analysis assumes a fixed input, a pivot uniform over every current active position, suitable fresh randomness across shrink trials, linear partition work, and correct one-sided recursion. It does not imply worst-case linear work.

### Answer 2

With pivot 6, partitions are $L=[2,2,4]$, $E=[6]$, and $G=[8,9]$; six elements are inspected. Rank 2 is in $L$, unchanged. With pivot 2, active partitions are $L=[]$, $E=[2,2]$, and $G=[4]$; three more elements are inspected. Since $0\le2<2$ is false but $|L|\le2<|L|+|E|$ is also false for zero-based rank 2, this transcript is inconsistent with returning 2: rank 2 follows $G$ with adjusted rank 0 and returns 4 after one more inspected element. Total inspections are 10. The correct sorted sequence `[2,2,4,6,8,9]` confirms rank 2 is 4. The exercise exposes the boundary between the equal block and greater block.

### Answer 3

Here $M=2^{32}=4294967296=429496729\cdot10+6$. Remainder outcomes 0–5 have 429,496,730 preimages while 6–9 have 429,496,729, so modulo is biased. Let $L=M-(M\bmod10)=4294967290$. Draw a word; accept only when it is below $L$ and return remainder modulo 10, otherwise redraw. Every output then has exactly 429,496,729 preimages. Acceptance probability is $L/M$, so expected draws are $M/L$, approximately $1.0000000014$. Use checked width semantics so computing $M$ does not overflow the word type.

### Answer 4

Full shuffle is exactly uniform but writes or represents all billion positions and consumes roughly a billion bounded draws. Partial Fisher–Yates consumes 1,000 draws but needs mutable or sparse-swap access to the full indexed frame. Independent with-replacement draws are cheap and mergeable but can duplicate records and have different inclusion probabilities. Independent continuous random priorities per stable record, followed by a distributed global smallest-1,000 reduction, support merging and without-replacement inclusion when streams and ties are correct; finite collisions need analyzed secondary randomness. All methods need one complete versioned frame and stable unit definition. Record algorithm/generator versions, domain-separated stream identity, frame/output digests, and tie rules. Protect seeds and selected identities when they expose future choices or membership.

### Answer 5

Construct a versioned global frame and either allocate shard sample sizes proportional to eligible shard populations or merge globally comparable independent priorities; record each unit's inclusion probability. Decide sample size before observing labels, or use a predeclared sequential design whose stopping rule enters the estimator and uncertainty. Separate fraud enrichment from representative prevalence estimation: a targeted review queue is not a probability sample. Keep generator state and future-selection secrets protected while storing an access-controlled replay transcript or commitment. Verify shard completeness, deduplication, inclusion mapping, and selected-output integrity. Evaluation should require exact small-domain distribution checks, generator/version evidence, design-weighted estimates with uncertainty, held-out operational assessment, privacy controls, and explicit failure/timeout handling.
