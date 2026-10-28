---
module_id: ALGE-077
program: Algorithm Engineering
level: 2
module_number: 77
title: Reservoir Sampling
status: complete
last_verified: 2026-09-05
---

# Reservoir Sampling

## One-Page Review

### Governing question

How can a one-pass algorithm retain an exactly uniform fixed-size sample from a stream of unknown final length, and how do identities, random priorities, merging, weighting, windows, estimation, and adversaries change that claim?

### Essential definitions

- A **population unit** is one eligible stream occurrence under a fixed admission and identity policy.
- A **simple random sample without replacement** (SRSWOR) of size $k$ from $N$ units assigns every $k$-subset probability $1/\binom Nk$.
- A **reservoir** is bounded state holding at most $k$ selected units while the population arrives.
- In **Algorithm R**, the first $k$ units fill the reservoir; unit $t>k$ is accepted with probability $k/t$ and, if accepted, replaces one uniformly chosen reservoir position.
- The **inclusion probability** $\pi_i$ is the probability that population unit $i$ appears in the final sample.
- A **priority sample representation** assigns each unit an independent continuous random key and retains an extreme $k$ keys.
- **Bottom-$k$ merge** keeps the $k$ smallest keys from compatible input samples.
- **Probability-proportional-to-size** (PPS) sampling favors positive-weight units under a declared without-replacement design.
- A **design-unbiased estimator** has expectation equal to its finite-population target over the sampling design, conditional on the fixed population.
- A **window sample** targets a changing suffix or time interval; a cumulative reservoir does not become a window sample by deleting expired selected units.

### Central model, mechanism, or theorem

After processing $t\ge k$ units, Algorithm R maintains the invariant that its reservoir is uniform over all $k$-subsets of the first $t$ units. For an old unit,

$$
\Pr(i\in R_t)=\frac{k}{t-1}\left(1-\frac1t\right)=\frac kt,
$$

because an accepted new unit replaces that particular old unit with probability $1/t$. The new unit is included with probability $k/t$. The stronger subset proof treats final subsets that contain $t$ and those that do not; each has probability $1/\binom tk$.

Equivalently, assign every unit an independent collision-free continuous key $U_i$ and retain the $k$ smallest. The induced key order is a uniformly random permutation, so every $k$-subset is equally likely. This representation makes compatible distributed merging algebraic:

$$
B_k(A\cup B)=B_k\bigl(B_k(A)\cup B_k(B)\bigr),
$$

where $B_k$ denotes bottom $k$. The equality concerns keyed occurrence sets; identity, key derivation, collision handling, and merge metadata remain premises.

### Critical invariants

- Every eligible occurrence is considered exactly once, or replay is deduplicated before sampling.
- For Algorithm R, the counter $t$ is the total number of eligible occurrences seen, not accepted or distinct units.
- Acceptance is exactly $k/t$, and accepted units replace a uniformly selected reservoir slot.
- Random choices are independent enough for the claimed design and are not predictable to an applicable adversary.
- Priority keys are stable, unique or deterministically tie-broken, and bound to immutable occurrence identity.
- Merge inputs share population semantics, key family and seed/key identifier, $k$, window, and version.
- Estimators use the actual inclusion probabilities of the sampling design.

### Common failures

Sampling records while claiming users; incrementing $t$ only on acceptance; modulo-biased random indices; retrying an update twice; merging equal local reservoirs from unequal shards; discarding priority keys; confusing weighted selection with inverse-probability estimation; treating sample uniformity as estimator correctness; using cumulative state for a sliding window; and exposing a deterministic seed to chosen-input manipulation.

### Compact example

With $k=2$, start from `[A,B]`. At $t=3$, choose a uniform integer from 1 through 3; if it is 1, replace slot 1 and obtain `[C,B]`. At $t=4$, a draw of 4 rejects `D`. The final sample is `[C,B]` for this random trace. Uniformity is a distribution over every valid trace, not a claim that this particular pair is representative.

### Connections

[ALGE-076](./076-streaming-quantiles.md) can use a uniform sample to estimate ranks with sampling error. ALGE-078 changes from insertion-only sampling to dynamic graph connectivity, where deletions create a different information problem.

## Governing Question

When the final population size is unknown and retaining all units is impossible, how can a streaming algorithm produce the same simple random sample distribution as an offline draw, then preserve that distribution through distributed execution and valid downstream estimation?

## Why This Matters

Uniform samples support inspection, debugging, approximate aggregation, model evaluation, quality audits, and exploratory statistics. The deceptively simple requirement “keep 1,000 representative events” combines an algorithmic sampling design with operational population construction. If admission drops errors, retries duplicate successes, or partitions merge incorrectly, a flawless random replacement loop samples the wrong population.

Reservoir sampling solves a precise finite-population problem: choose $k$ occurrences uniformly without replacement in one pass when $N$ is unknown initially. It does not automatically sample distinct entities, recent events, sessions, or importance-weighted units. It does not make every statistic unbiased, repair missing-not-at-random data, guarantee privacy, or turn observational data into causal evidence.

Distributed systems make representation decisive. A reservoir that stores only values can be correct locally yet difficult to merge without shard counts and additional randomization. A priority representation stores the random order evidence needed for bottom-$k$ union. That benefit comes with requirements for stable occurrence identity, random-key quality, collision policy, secret management where adversaries matter, and versioned serialization.

## Prerequisites and Retrieval

Retrieve conditional probability and induction from ALGE-004 and ALGE-029, order statistics from ALGE-017, approximation and probability-qualified guarantees from ALGE-061 and ALGE-068, and stream, merge, and window distinctions from [ALGE-074](./074-streaming-frequency-estimation.md), [ALGE-075](./075-distinct-counting.md), and [ALGE-076](./076-streaming-quantiles.md). You should distinguish an occurrence from a value, a marginal inclusion probability from a joint sample design, and a random algorithm from its one observed output.

## Learning Objectives

After this module, you should be able to:

1. specify the population and SRSWOR contract for a reservoir;
2. prove Algorithm R's uniform-subset invariant by induction;
3. derive inclusion probabilities, expected replacement work, and basic design-unbiased estimators;
4. implement and validate per-item and priority-key reservoirs without random-index bias;
5. merge distributed reservoirs correctly and reject incompatible states;
6. distinguish uniform, weighted, priority, stratified, and window sampling; and
7. design operational evidence for replay, randomness, estimation, privacy, and consequential use.

## Core Exposition

### Define the population before the random draw

Let the eligible stream be labeled occurrences $1,\ldots,N$ in arrival order. Labels identify occurrences even when payload values repeat. For $0\le k\le N$, an SRSWOR design returns a subset $R$ of size $k$ such that

$$
\Pr(R=A)=\frac{1}{\binom Nk}
$$

for every $A\subseteq\{1,\ldots,N\}$ with $|A|=k$. Consequently each unit has first-order inclusion probability $\pi_i=k/N$, and each distinct pair has joint inclusion probability

$$
\pi_{ij}=\frac{k(k-1)}{N(N-1)}.
$$

Uniformity is over units, not payload values. In an event stream `[A,A,B]`, the two `A` occurrences jointly receive twice the expected sample count of `B`. If the target is distinct users, deduplicate or define one stable eligible unit per user before applying the design. A bounded occurrence reservoir cannot later infer which repeated payloads represented one entity.

Admission is part of the population. Parsing failures, tenant filters, consent, late-event rules, backpressure drops, and retry deduplication must occur under a declared policy. Increment the stream counter only for eligible logical occurrences, but increment it for every such occurrence whether or not it enters the sample.

### Algorithm R

For capacity $k$, retain the first $k$ eligible units. When unit $t>k$ arrives, draw $J_t$ uniformly from $\{1,\ldots,t\}$. If $J_t\le k$, replace reservoir position $J_t$; otherwise discard the new unit. This is equivalent to accepting with probability $k/t$ and then choosing a uniform slot, but one uniform integer avoids inconsistent two-stage implementations.

Edge cases are contractual. Capacity zero returns an empty sample without drawing. Before $k$ units arrive, return all observed units and report the realized size. A negative capacity is invalid. Counter overflow, process restart, and serialization must not reset $t$. Uniform integer generation should use a library route that avoids modulo bias when the generator's raw range is not divisible by $t$.

<!-- bijux-verify: {"id":"algorithm-r-mechanics","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"sample=[1, 17, 7, 4, 20]\nsize=5 unique=5\nzero=[]\ninvalid=k must be nonnegative\n","stderr":""}} -->
```python
import random

def reservoir(items, k, seed):
    if k < 0:
        raise ValueError("k must be nonnegative")
    rng = random.Random(seed)
    sample = []
    for t, item in enumerate(items, 1):
        if t <= k:
            sample.append(item)
        else:
            j = rng.randrange(t)  # exactly uniform over 0, ..., t-1
            if j < k:
                sample[j] = item
    return sample

sample = reservoir(range(1, 21), 5, 20260905)
print(f"sample={sample}")
print(f"size={len(sample)} unique={len(set(sample))}")
print(f"zero={reservoir(range(10), 0, 20260905)}")
try:
    reservoir(range(10), -1, 20260905)
except ValueError as error:
    print(f"invalid={error}")
```

The fixed seed makes this regression trace reproducible. It does not make Python's pseudorandom generator suitable against adversarial prediction, and one output does not demonstrate uniformity.

### Proof of the uniform-subset invariant

**Theorem.** After processing $t\ge k$, Algorithm R's state is uniform over the $\binom tk$ subsets of size $k$.

**Proof.** The base case $t=k$ has exactly one possible $k$-subset, the first $k$ units. Assume the claim after $t-1$ units and fix any $k$-subset $A$ of the first $t$ units.

If $t\notin A$, the prior reservoir must equal $A$, with probability $1/\binom{t-1}{k}$, and the new unit must be rejected, with probability $(t-k)/t$. Therefore

$$
\Pr(R_t=A)=\frac{t-k}{t\binom{t-1}{k}}=\frac1{\binom tk}.
$$

If $t\in A$, write $B=A\setminus\{t\}$. The prior reservoir must be $B\cup\{x\}$ for one of the $t-k$ old units outside $B$. Each such reservoir has probability $1/\binom{t-1}{k}$, and drawing the position occupied by $x$ has probability $1/t$. Summing disjoint cases gives

$$
\Pr(R_t=A)=\frac{t-k}{t\binom{t-1}{k}}=\frac1{\binom tk}.
$$

Both cases match, completing the induction. $\square$

The familiar marginal proof follows: a new unit enters with probability $k/t$; an old included unit survives with probability $1-1/t$, so $(k/(t-1))(1-1/t)=k/t$. Equal marginals alone would not prove a uniform joint design, which is why the subset proof matters.

### Work and skip algorithms

Algorithm R examines every unit and draws a random integer for every $t>k$. Its expected number of post-fill insertions is

$$
\sum_{t=k+1}^{N}\frac{k}{t}=k(H_N-H_k)\approx k\ln(N/k),
$$

where $H_m$ is the $m$th harmonic number. Most late units are rejected. Vitter's skip-based algorithms sample the number of records to bypass before the next reservoir change while preserving the same sampling design; Algorithm Z obtains optimal expected order up to constants beyond unavoidable scanning assumptions [1]. Li develops related skip algorithms with expected CPU time $O(k(1+\log(N/k)))$ when scan cost is excluded [2].

Skip implementations are numerically delicate. They use transformations of uniform variates, logarithms, products, and integer boundaries. Zero random variates, floating-point underflow, huge counters, off-by-one skip lengths, end-of-stream handling, and biased fallback paths need tests against an exact Algorithm R oracle on bounded populations and distributional tests over many seeds.

### Random priorities and distributed merging

Assign each eligible occurrence an independent continuous key $U_i\sim\mathrm{Uniform}(0,1)$ and retain the $k$ smallest keyed records. Exchangeability makes the sorted key order a uniformly random permutation of occurrences, so its first $k$ units form an SRSWOR. Bottom-$k$ is deterministic once keys exist.

For keyed sets $A$ and $B$, any item discarded from $B_k(A)$ already has at least $k$ smaller keys in $A$ and cannot enter the global bottom $k$ after adding $B$. Hence

$$
B_k(A\cup B)=B_k(B_k(A)\cup B_k(B)).
$$

The operation is associative, commutative, and idempotent on the same keyed occurrence set. Idempotence makes retrying the same immutable occurrence harmless only when it receives the same key and is deduplicated by identity. Re-keying a retry creates another population unit and changes the sample.

In practice a keyed pseudorandom function can map a versioned immutable occurrence identifier and secret or public seed to a wide priority. This is a model choice: hash outputs are finite, collisions need deterministic identity tie-breaking, and a public noncryptographic hash may permit chosen-identifier manipulation. Store the key or enough metadata to reproduce it. Two shards using different key identifiers or occurrence canonicalization do not have mergeable samples.

Naively combining equal local reservoirs is biased when shard sizes differ. Correct alternatives include global bottom-$k$ priorities, a merge algorithm that uses exact shard population sizes and the appropriate hypergeometric allocation, or a formally analyzed mergeable sampling design. “Select $k$ from the union of local samples” is valid only under conditions that make every global occurrence's inclusion law equal.

### Estimation from an equal-probability reservoir

Sampling design and estimator are separate. Let fixed population values be $y_1,\ldots,y_N$ and total $T=\sum_i y_i$. Under SRSWOR, $\pi_i=k/N$, so the Horvitz--Thompson estimator is

$$
\widehat T=\sum_{i\in R}\frac{y_i}{\pi_i}
=\frac Nk\sum_{i\in R}y_i.
$$

Linearity of expectation gives $E[\widehat T]=T$ [6]. The sample mean is unbiased for the finite-population mean $\mu=T/N$. If

$$
S^2=\frac1{N-1}\sum_{i=1}^N(y_i-\mu)^2,
$$

then

$$
\operatorname{Var}(\bar y_R)=\left(1-\frac{k}{N}\right)\frac{S^2}{k},
\qquad
\operatorname{Var}(\widehat T)=N^2\left(1-\frac{k}{N}\right)\frac{S^2}{k}.
$$

The finite-population correction appears because sampling is without replacement. Estimating variance from the sample, constructing confidence intervals, handling ratios, and making many or adaptive queries introduce further conditions. Uniform selection cannot repair coverage error, measurement error, nonresponse, or a population assembled by outcome-dependent drops.

### Weighted reservoirs are different designs

“Weight” can mean at least three things: multiplicity in the target population, desired selection probability, or inverse-probability correction in an estimator. They must not be interchanged.

For positive selection weights $w_i$, one useful key design draws $U_i\in(0,1)$ and keeps the $k$ largest $U_i^{1/w_i}$. A numerically stable equivalent keeps the $k$ smallest

$$
K_i=\frac{-\ln U_i}{w_i}.
$$

Because $-\ln U_i$ is exponential with rate one, $K_i$ is exponential with rate $w_i$. For $k=1$, the exponential race gives

$$
\Pr(i\text{ is selected})=\frac{w_i}{\sum_j w_j}.
$$

For $k>1$, successive weighted selection without replacement does not generally give marginal inclusion probability $kw_i/\sum_jw_j$; that expression can even exceed one. Efraimidis and Spirakis analyze weighted reservoir key algorithms [4], while Chao develops a fixed-size unequal-probability design with computable inclusion probabilities [3]. Choose the design from the inferential target and feasibility conditions.

Priority sampling for subset-sum estimation is another distinct construction: priorities such as $w_i/U_i$, retention of the top priorities, and a threshold yield unbiased weight estimators for arbitrary subsets under the stated design [5]. It should not be renamed “weighted reservoir sampling” without preserving its threshold and estimator.

### Windows, deletions, and changing populations

A cumulative reservoir is uniform over everything it has seen. If selected expired units are simply removed, the remaining sample is too small; unseen expired units may have displaced live candidates that were discarded forever. If selected units are retained until expiry without replacements, the state is not uniform over the live window.

Window sampling needs a window-aware algorithm, time-stratified reservoirs with analyzed boundary behavior, or retained priority candidates sufficient to replenish after expiration. Rebuilding from durable window data is often the safest threshold-adjacent fallback. Sliding-window streaming is its own model with separate bounds [8]. Arbitrary deletion similarly requires more evidence than the current $k$ winners.

Changing $k$ is asymmetric. If stable priorities and more than $k$ candidates were retained, decreasing $k$ takes a prefix. Increasing beyond retained state cannot recover discarded units without rescan or auxiliary samples. Combining samples across schema, consent, or eligibility changes constructs no coherent population; close the old version and start or rebuild the new one.

### Engineering, validation, and authority

A durable state envelope records algorithm and implementation version, capacity, eligible count $t$, occurrence-ID schema, admission policy, key/RNG algorithm, seed or key identifier, priority width and tie-break, value schema, weights and design, window, partition coverage, source offsets, serialization version, and checksum. Secret key material belongs in an appropriate key system, not the sample artifact.

Structural tests check capacity, count monotonicity, exact fill behavior, stable keys, unique occurrences, and metadata rejection. Exhaustive probability tests can enumerate every random branch for small $N$ and verify every $k$-subset has probability $1/\binom Nk$. Property tests compare priority and Algorithm R distributions, bottom-$k$ merge against a single global pass, and every merge-tree shape. Statistical tests across many seeds can detect gross bias but cannot prove exact uniformity.

Operational tests cover crash between counter and state writes, duplicate delivery, partition loss, late arrival, seed rotation, collision, counter overflow, empty shards, unequal shard sizes, resharding, and schema upgrades. Observe eligible, rejected, sampled, replaced, replayed, deduplicated, expired, missing-partition, merge-rejected, and collision counts. Preserve exact bounded fixtures and independently computed inclusion/estimation checks.

Samples can expose rare or sensitive records and membership. Sampling is not anonymization or consent. Access control, minimization, retention, query auditing, and approved disclosure controls remain necessary. For contractual, clinical, financial, safety, or fairness decisions, publish sampling and nonsampling uncertainty, predeclare estimators, and require exact or independently reviewed fallback near decision boundaries.

## Definitions and Notation

- $N$: final number of eligible logical population occurrences.
- $k$: requested maximum sample size, with $0\le k\le N$ for a full reservoir.
- $t$: count of eligible occurrences processed so far.
- $R_t$: reservoir after the first $t$ eligible occurrences.
- $\pi_i$: first-order inclusion probability of unit $i$.
- $\pi_{ij}$: joint inclusion probability of distinct units $i$ and $j$.
- $H_N=\sum_{t=1}^N1/t$: $N$th harmonic number.
- $B_k(A)$: the $k$ members of keyed set $A$ with smallest priorities, or all members if $|A|<k$.
- $U_i$: independent ideal continuous uniform variate assigned to occurrence $i$.
- $w_i>0$: declared selection weight for weighted sampling.
- $T=\sum_i y_i$: finite-population total of analysis values.
- $\widehat T$: estimator of $T$ under a specified sampling design.
- **Occurrence:** one eligible logical arrival; equal payloads may be different occurrences.
- **Entity sample:** a sample whose population units are canonical entities, requiring entity construction before or during sampling.
- **Design randomness:** randomness of the sampling procedure conditional on a fixed finite population.
- **Model randomness:** a statistical assumption that the finite population or observations arose from a stochastic process; reservoir uniformity does not require it.

## Mechanisms, Invariants, or Proof Structure

### Algorithm R proof obligations

The base state contains the only $k$-subset of the first $k$ units. For every later $k$-subset, split on whether it contains the new unit. Rejection supplies the correct probability for subsets without it; summing over every possible displaced outsider supplies the same probability for subsets containing it. The implementation must therefore draw exactly one of $t$ equiprobable outcomes and map the first $k$ outcomes one-to-one to current slots. Counter, index range, and replacement uniformity are theorem premises.

### Priority equivalence and merge obligations

Independent continuous priorities create a uniform random permutation, so its first $k$ labels are a uniform subset. A discarded local item has $k$ local witnesses with smaller keys, which remain witnesses in every superset; therefore local pruning cannot remove a global winner. This dominance proof yields bottom-$k$ merge. Finite keys, collisions, different key families, re-keyed retries, and overlapping occurrence IDs break or qualify its premises.

### Estimator obligations

For fixed $y_i$, write $I_i=1$ when unit $i$ is sampled. Since $E[I_i]=\pi_i$, the term $I_iy_i/\pi_i$ has expectation $y_i$, and summing proves Horvitz--Thompson unbiasedness. Variance depends on joint inclusion probabilities, not only marginals. Using uniform-reservoir formulas for weighted, clustered, stratified, or outcome-dependent samples is invalid.

### Weighted-key obligation

If $E_i=-\ln U_i\sim\operatorname{Exp}(1)$, then $E_i/w_i\sim\operatorname{Exp}(w_i)$. Independent exponential clocks race with probability proportional to rate for the first winner. Repeating after a winner is removed explains successive PPS selection. This proof covers the declared key design; it does not supply Chao or priority-sampling inclusion probabilities and estimators.

### Evidence ladder

An exact proof establishes the ideal sampling design. Exhaustive branch enumeration checks bounded algorithm realizations. Regression execution checks a toolchain and seed. Many-seed statistical tests seek detectable implementation bias. Merge and failure injection test distributed mechanisms. Population and estimator review test whether the correct real-world question is being answered. None substitutes for the others.

## Alternatives and Trade-Offs

- **Algorithm R:** minimal, auditable, exact SRSWOR and independent of final $N$; performs work and random generation on every item.
- **Vitter or Li skip algorithms:** preserve the design while reducing expected selection work for $N\gg k$ [1,2]; require careful numerical and boundary engineering.
- **Bottom-$k$ random priorities:** natural distributed merge, deterministic recomputation from stable keyed identities, and easy resizing downward; stores priorities and raises collision, key, and adversary concerns.
- **Hypergeometric merge:** can combine unkeyed uniform shard samples using exact shard sizes and a correct allocation law; more metadata and logic than bottom-$k$.
- **Stratified reservoirs:** guarantee capacity by important strata and can reduce variance; the union is not globally uniform, so estimators need stratum inclusion weights.
- **Weighted PPS reservoirs:** emphasize high-weight units under a chosen design [3,4]; unequal inclusion probabilities and estimators are more complex.
- **Priority sampling:** targets subset-sum estimation with thresholded weight estimates [5]; not interchangeable with simple weighted selection.
- **Bernoulli sampling:** independently retains each unit with probability $p$ and merges simply; sample size is random and can exceed memory budgets.
- **Window-aware sampling:** targets recent populations; needs time-aware state and often more memory than a cumulative reservoir.

Prefer the simplest design whose population, merge topology, estimator, and threat model match the application. A faster sampler that makes inclusion probabilities opaque can be worse than Algorithm R when auditability dominates throughput.

## Failure Modes and Misconceptions

1. **“The reservoir samples values uniformly.”** It samples eligible occurrences unless entities were defined first.
2. **“Equal marginal probabilities prove a simple random sample.”** Joint subset probabilities also matter.
3. **“Accept with probability $k/t$” is enough.** Replacement must also be uniform, and $t$ must count every eligible unit.
4. **“`random() % t` is uniform.”** It is biased unless the raw range divides evenly or rejection corrects it.
5. **“A fixed seed proves reproducibility and security.”** It helps replay but may enable prediction and chosen-input attacks.
6. **“Merge local samples by sampling their union.”** Unequal shard populations create unequal global inclusion.
7. **“Bottom-$k$ always deduplicates retries.”** Only stable occurrence identity and stable keys make repeated state idempotent.
8. **“Weighted selection and weighted estimation are the same.”** Selection weights, inclusion probabilities, and analysis weights have distinct roles.
9. **“Uniform data makes any statistic unbiased.”** Nonlinear estimators can be biased even under SRSWOR.
10. **“Delete expired sampled records to get a window sample.”** Lost candidates cannot be reconstructed.
11. **“Statistical tests prove exact uniformity.”** They can reveal defects but cannot prove all probabilities.
12. **“A sample is anonymous.”** Rare records and membership may remain identifying.

## Worked Examples

### Example 1

**Situation.** Capacity is two. The first records are `A,B`; the random outcome for `C` at $t=3$ is slot 1, and the outcome for `D` at $t=4$ is 4.

**Reasoning.** `C` replaces `A`, giving `[C,B]`. Because 4 exceeds $k$, `D` is rejected. The realized sample is `[C,B]`; another legal random trace produces another pair.

**Conclusion.** The algorithm's claim concerns the distribution of traces, not visual representativeness of one sample.

### Example 2

**Situation.** An old unit is in a size-$k$ reservoir after $t-1$ updates.

**Reasoning.** Its prior inclusion probability is $k/(t-1)$. The new draw replaces its particular slot with probability $1/t$, so it survives with probability $(t-1)/t$. Their product is $k/t$, equal to the new unit's $k/t$ inclusion probability.

**Conclusion.** Every unit has the correct marginal probability after the update, while the subset proof establishes the stronger joint design.

### Example 3

**Situation.** $k=1000$ and $N=10^6$.

**Reasoning.** Expected post-fill replacements are $1000(H_{10^6}-H_{1000})\approx6907.3$; its leading approximation $1000\ln(1000)$ is about 6907.8. Algorithm R still draws and branches on about 999,000 later arrivals, motivating a proven skip algorithm when per-record CPU dominates.

**Conclusion.** Few state changes do not imply few random decisions in Algorithm R.

### Example 4

**Situation.** Shard A has 1,000 units and shard B has 10. Each retains 10 units, then a coordinator chooses 10 uniformly from the 20 retained units.

**Reasoning.** An A unit reaches the coordinator with probability $10/1000$ and survives with probability $1/2$, giving 0.005. Every B unit reaches it and survives with probability $1/2$, giving 0.5. B units are 100 times as likely to appear.

**Conclusion.** Equal local capacities do not justify equal treatment of local samples.

### Example 5

**Situation.** Two shards' keyed candidates are A:`(a,.08),(b,.41),(c,.63)` and B:`(d,.03),(e,.52),(f,.77)`, with $k=2$.

**Reasoning.** Local bottom-two states are `a,b` and `d,e`. Their union's bottom two are `d` at .03 and `a` at .08. Discarded `c` and `f` cannot beat two local witnesses already below them.

**Conclusion.** Bottom-$k$ merge matches a global keyed pass.

### Example 6

**Situation.** The logical event population is `[A,A,B]` and $k=1$.

**Reasoning.** Each occurrence has inclusion probability $1/3$. Therefore the sampled payload is `A` with probability $2/3$ and `B` with probability $1/3$. If the intended population is distinct identities `{A,B}`, preprocessing must define those two units, yielding probability $1/2$ each.

**Conclusion.** Uniform occurrence sampling preserves multiplicity.

### Example 7

**Situation.** A uniform sample of $k=10$ from $N=100$ has sampled analysis-value sum 80; suppose the finite-population variance is known to be $S^2=25$.

**Reasoning.** The Horvitz--Thompson total estimate is $(100/10)80=800$. Its design variance is $100^2(1-10/100)25/10=22{,}500$, so its design standard deviation is 150.

**Conclusion.** An unbiased point estimate still carries sampling uncertainty.

### Example 8

**Situation.** Three units have positive selection weights 1, 3, and 6, and a weighted exponential-key reservoir keeps one.

**Reasoning.** The exponential clocks have rates 1, 3, and 6. The minimum belongs to each unit with probabilities $1/10$, $3/10$, and $6/10$. If $k=2$, doubling those probabilities is invalid because the last would exceed one and joint selection changes after the first winner.

**Conclusion.** The clean $w_i/\sum w$ result is a first-winner result, not a general fixed-size marginal formula.

### Example 9

**Situation.** A cumulative capacity-100 reservoir covers a week, and the first six days expire.

**Reasoning.** Removing sampled expired units leaves a random and usually tiny subset. Unselected day-seven units that lost to expired priorities are unavailable as replacements. Retaining only current winners cannot reconstruct the bottom 100 priorities of the live day.

**Conclusion.** Correct sliding-window sampling needs additional time-aware state or a rebuild.

### Example 10

**Situation.** An external client chooses occurrence IDs, and the service derives public 64-bit priorities from an unkeyed hash.

**Reasoning.** A client can search offline for IDs with exceptionally small priorities, then submit them to dominate a bottom-$k$ sample. A secret keyed pseudorandom function, authenticated eligibility, rate limits, wider keys, collision tie-breaking, and rotation with versioned window boundaries reduce the risk; they do not repair a sample already poisoned.

**Conclusion.** Random-looking deterministic keys require an adversarial threat model.

## Cross-Program Connections

- **Data Structures Engineering:** bounded arrays, heaps, order statistics, keyed sets, and serialization implement reservoirs and bottom-$k$ state.
- **Data Engineering:** admission, partitions, offsets, replay, event time, watermarks, and backpressure define the sampled population.
- **Data Architecture Engineering:** entity identity, schema, units, consent, weights, lineage, and retention determine sample meaning.
- **Distributed Systems Engineering:** deterministic keys, idempotence, merge trees, checkpoints, resharding, and rolling upgrades govern global inclusion.
- **Database Engineering:** sampled synopses support approximate queries only with design-aware estimators and optimizer risk controls.
- **Security Engineering:** chosen identifiers, random predictability, key custody, poisoning, privacy, and membership disclosure shape defenses.
- **Platform Engineering:** sampling services need compatibility envelopes, metrics, audit fixtures, resource budgets, and fallback.
- **Algorithm Engineering:** [ALGE-076](./076-streaming-quantiles.md) uses samples for approximate distribution queries; ALGE-078 next begins fully dynamic graph algorithms.

## References

1. Jeffrey S. Vitter, “Random Sampling with a Reservoir,” *ACM Transactions on Mathematical Software* 11(1), 1985, 37–57. DOI: [10.1145/3147.3165](https://doi.org/10.1145/3147.3165). Primary source for reservoir algorithms, including skip-based Algorithm Z and its analysis; ACM record checked 2026-09-05.
2. Kim-Hung Li, “Reservoir-Sampling Algorithms of Time Complexity $O(n(1+\log(N/n)))$,” *ACM Transactions on Mathematical Software* 20(4), 1994, 481–493. DOI: [10.1145/198429.198435](https://doi.org/10.1145/198429.198435). Primary source for skip-based reservoir algorithms and expected CPU bounds; ACM record checked 2026-09-05.
3. M. T. Chao, “A General Purpose Unequal Probability Sampling Plan,” *Biometrika* 69(3), 1982, 653–656. DOI: [10.1093/biomet/69.3.653](https://doi.org/10.1093/biomet/69.3.653). Primary source for fixed-size unequal-probability sampling without replacement; Oxford Academic record checked 2026-09-05.
4. Pavlos S. Efraimidis and Paul G. Spirakis, “Weighted Random Sampling with a Reservoir,” *Information Processing Letters* 97(5), 2006, 181–185. DOI: [10.1016/j.ipl.2005.11.003](https://doi.org/10.1016/j.ipl.2005.11.003). Primary source for weighted random-key reservoir algorithms; publisher and institutional records checked 2026-09-05.
5. Nick Duffield, Carsten Lund, and Mikkel Thorup, “Priority Sampling for Estimation of Arbitrary Subset Sums,” *Journal of the ACM* 54(6), 2007, Article 32. DOI: [10.1145/1314690.1314696](https://doi.org/10.1145/1314690.1314696). Primary source for priority-sampling thresholds and unbiased subset-sum estimators; ACM-linked and author records checked 2026-09-05.
6. D. G. Horvitz and D. J. Thompson, “A Generalization of Sampling Without Replacement from a Finite Universe,” *Journal of the American Statistical Association* 47(260), 1952, 663–685. DOI: [10.1080/01621459.1952.10483446](https://doi.org/10.1080/01621459.1952.10483446). Primary source for inverse-inclusion-probability estimation; publisher and author-manuscript records checked 2026-09-05.
7. Pankaj K. Agarwal, Graham Cormode, Zengfeng Huang, Jeff M. Phillips, Zhewei Wei, and Ke Yi, “Mergeable Summaries,” *Proceedings of ACM PODS 2012*, 23–34. DOI: [10.1145/2213556.2213562](https://doi.org/10.1145/2213556.2213562). Primary source for formal mergeability as a streaming-summary property; ACM, conference, and author records checked 2026-09-05.
8. Mayur Datar, Aristides Gionis, Piotr Indyk, and Rajeev Motwani, “Maintaining Stream Statistics over Sliding Windows,” *SIAM Journal on Computing* 31(6), 2002, 1794–1813. DOI: [10.1137/S0097539701398363](https://doi.org/10.1137/S0097539701398363). Primary source for the sliding-window streaming model and its separate space bounds; SIAM record checked 2026-09-05.

## Exercises

### Exercise 1

Define the SRSWOR reservoir contract. For $N=5$ and $k=2$, give every subset probability, one unit's inclusion probability, and one pair's joint inclusion probability. Explain why equal unit marginals alone are insufficient.

### Exercise 2

Complete the uniform-subset induction for Algorithm R, treating subsets that contain the new unit and those that do not. Then derive the expected number of post-fill replacements.

### Exercise 3

A sampler increments $t$ only when a record is selected, computes `raw_random % t`, restarts $t$ after crashes, and merges ten-record local reservoirs equally from shards of unequal size. Diagnose every defect and propose focused tests.

### Exercise 4

Design a global event-sampling service across 1,000 partitions. Specify population identity, admission, $k$, priorities, randomness and key custody, merge metadata, replay, persistence, windows, resizing, validation, observability, privacy, and fallback.

### Exercise 5

A city wants a sample of permit inspections for estimating total remediation cost, oversampling rare high-risk categories. Design the sampling and evidence plan, distinguishing selection weights, inclusion probabilities, estimators, variance, coverage, missingness, privacy, audit, and decision authority.

## Answers to the Exercises

### Answer 1

SRSWOR selects exactly $k$ distinct eligible occurrence labels and assigns each $k$-subset probability $1/\binom Nk$. With $N=5,k=2$, each of the ten pairs has probability $1/10$. A fixed unit appears in four pairs, so $\pi_i=4/10=2/5=k/N$. A fixed pair appears only as itself, so $\pi_{ij}=1/10=k(k-1)/(N(N-1))$. Equal marginals do not determine dependence: other fixed-size or variable-size designs can give every unit marginal $2/5$ while assigning unequal or zero probability to particular pairs. The full subset law—or sufficient joint inclusion structure for the estimator—is required.

### Answer 2

At $t=k$ the reservoir is the only $k$-subset. Assume uniformity at $t-1$ and fix $A$ of size $k$. If $t\notin A$, the prior state must be $A$ and the new item rejected, giving $(1/\binom{t-1}{k})((t-k)/t)=1/\binom tk$. If $t\in A$, let $B=A\setminus\{t\}$. For each of the $t-k$ old outsiders $x$, prior state $B\cup\{x\}$ has probability $1/\binom{t-1}{k}$ and replacing $x$ has probability $1/t$; summing gives the same $1/\binom tk$. Post-fill unit $t$ enters with probability $k/t$, so expected replacements are $\sum_{t=k+1}^N k/t=k(H_N-H_k)\approx k\ln(N/k)$.

### Answer 3

The counter must advance for every eligible occurrence; selection-only increments make late acceptance far too high and make the denominator state-dependent. Modulo reduction is biased unless the generator range divides by $t$ or rejection sampling removes excess outcomes; use a verified uniform bounded-integer API. Restarting $t$ changes every later inclusion probability; persist counter and reservoir atomically with source offsets, or reconstruct through idempotent replay. Equal sampling of local reservoirs overweights small shards; use stable global bottom-$k$ priorities or exact shard counts with a correct hypergeometric merge. Exhaustively enumerate small $N,k$ branch probabilities, test bounded-index frequencies, crash at every persistence boundary, replay duplicates, compare every merge tree with global bottom-$k$, and include shard sizes 0, below $k$, $k$, and orders of magnitude apart.

### Answer 4

Define one tenant-qualified immutable event occurrence after versioned eligibility, parsing, consent, and retry deduplication. Choose global or per-tenant $k$ explicitly. Derive a wide priority from the occurrence ID with a versioned keyed pseudorandom function; keep identity tie-breaks, store key IDs rather than secret material, and restrict key access. Each state records algorithm/version, $k$, eligible count, ID and value schema, admission, priority width, key ID, window, partition and offset coverage, serialization, and checksum. Merge only compatible bottom-$k$ states; stable IDs make retry idempotent. Persist state and offsets atomically. Use window-aware candidate state or rebuild, never deletion from cumulative winners. Decreasing $k$ takes a prefix; increasing requires retained candidates or rescan. Exhaustively test small designs and merge identities, run many-seed diagnostics and failure injection, and observe all population, retry, collision, merge, and coverage counters. Encrypt and access-control sensitive samples, minimize payloads, audit use, and expire them. On missing partitions, key/version mismatch, collision anomalies, audit failure, or poisoned admission, mark unavailable or rebuild from durable input.

### Answer 5

Define the finite population as eligible inspections in a fixed jurisdiction and period, including how canceled, missing, duplicate, and late inspections are handled. Predeclare strata or positive selection weights that raise rare high-risk inclusion while satisfying a known without-replacement design; do not call analysis weights selection probabilities. Record every unit's first-order and, for variance estimation, needed joint inclusion probabilities. Estimate total cost with Horvitz--Thompson terms $y_i/\pi_i$ and a design-valid variance estimator; publish both sampling and nonsampling uncertainty. Audit coverage against the permit register, investigate cost missingness and outcome-dependent access, and report stratum-specific realized sizes. Protect addresses and sensitive findings through minimization, access control, retention, and disclosure review. Recompute bounded high-consequence totals exactly where possible and obtain independent survey-statistical, domain, privacy, and fairness review. Frame changes, weight errors, unknown inclusion probabilities, missing strata, differential nonresponse, privacy leakage, variance instability, or audit failure invalidate the estimate and trigger redesign or withheld decisions.
