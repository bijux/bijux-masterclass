---
module_id: ALGE-029
program: Algorithm Engineering
level: 1
module_number: 29
title: Randomization as a Design Tool
status: complete
last_verified: 2026-09-04
---

# Randomization as a Design Tool

## One-Page Review

### Governing question

How can deliberately sampled choices make an algorithm simpler, faster, or more robust while leaving its probability space, correctness guarantee, resource risk, reproducibility, and security assumptions explicit?

### Essential definitions

- A **randomized algorithm** is a distribution over deterministic executions: fixing the input and the complete random tape fixes the run.
- A **sample space** lists the possible random outcomes; a probability measure assigns their probabilities.
- A **Las Vegas algorithm** always returns a correct result but has random cost.
- A **Monte Carlo algorithm** has a bounded cost or budget but may return an incorrect or inconclusive result with a stated probability.
- A **one-sided error** permits error in only one answer direction; a **two-sided error** permits either direction.
- A **uniform bounded draw** returns each integer in $\{0,\ldots,b-1\}$ with probability $1/b$.
- **Independence** means joint probabilities factor for the random variables under discussion; distinct API calls are not independent merely because they have different names.
- **Amplification** repeats trials so that an aggregate rule reduces failure probability.
- A **pseudorandom number generator** expands a finite state into a deterministic stream; its seed and stream-derivation policy define the run.
- An **adversary model** states what an input chooser can observe and when it may adapt.
- A **replay record** contains enough stable information to reconstruct the intended random choices under a versioned implementation.

### Central model, mechanism, or theorem

Let $R$ be a random tape drawn from distribution $\mathcal D$, and let $A(x;R)$ be the deterministic execution produced for fixed input $x$. Correct randomized analysis quantifies over the internal choices:

$$
\Pr_{R\sim\mathcal D}[A(x;R)\text{ violates its contract}]
\le \varepsilon(x).
$$

For Las Vegas algorithms, $\varepsilon(x)=0$ and cost $C(x,R)$ is random. A useful claim may be

$$
\mathbb E_R[C(x,R)]\le f(|x|)
$$

for every valid fixed input $x$. This differs from average-case analysis, which draws $x$ from an input distribution.

If independent trials each fail with probability at most $q<1$, and the aggregate result fails only when every trial fails, then

$$
\Pr[\text{aggregate failure}]
\le q^r.
$$

Equivalently, if each trial succeeds with probability at least $p$, then failure is at most $(1-p)^r\le e^{-pr}$. Independence, fresh streams, a verifier or aggregation rule, and the meaning of failure are proof premises—not operational details.

### Critical invariants

- The probability guarantee is quantified for every input covered by the contract.
- Every finite choice uses the intended distribution; range conversion introduces no modulo or floating-point bias.
- Random choices influence only behavior permitted by the Las Vegas or Monte Carlo contract.
- A Las Vegas result is verified before return; a Monte Carlo error direction and bound remain visible to callers.
- Repetition uses genuinely disjoint or otherwise justified streams and the proved aggregation rule.
- Seed, generator algorithm, version, domain separator, trial identity, and input revision are controlled together.
- Concurrency and retries do not duplicate streams, silently change sample weights, or make replay depend on scheduling.
- Expected cost is not presented as a latency bound; tails, caps, fallbacks, and cancellation are specified separately.
- Noncryptographic pseudorandomness is never used where unpredictability is a security requirement.
- Statistical tests supplement structural proofs and reference vectors; they do not prove uniformity, independence, or security.

### Common failures

Frequent failures include taking a machine word modulo a nondivisor range; shuffling by random-key sorting; reseeding on every call from a low-resolution clock; sharing mutable generator state across threads; assuming different seeds imply independent streams; confusing random input with internal randomization; proving an expectation and promising a deadline; retrying correlated failures as if they were independent; reporting “probably correct” without an error direction; discarding an inconclusive status; using a user-visible seed as a secret; allowing an adaptive client to learn and exploit hash choices; forgetting duplicate and tie semantics; measuring only successful trials; and treating a passed statistical battery as a proof of cryptographic unpredictability.

### Compact example

Suppose a source emits uniform four-bit words $X\in\{0,\ldots,15\}$ and an algorithm needs a uniform die index in $\{0,\ldots,5\}$. Directly returning $X\bmod6$ is biased: residues $0,1,2,3$ have three preimages, while $4,5$ have two.

Set

$$
L=\left\lfloor\frac{16}{6}\right\rfloor6=12.
$$

Reject $X\ge12$ and otherwise return $X\bmod6$. Each result now has exactly two accepted preimages, so its conditional probability is $1/6$. The rejection probability is $4/16=1/4$, and the expected number of words per accepted draw is $1/(3/4)=4/3$.

### Connections

[ALGE-006](./006-best-worst-expected-and-amortized-cost.md) separates expected cost from tails, [ALGE-008](./008-lower-bounds-and-adversary-arguments.md) supplies adversary quantifiers, [ALGE-014](./014-quicksort-and-partitioning.md) analyzes random pivots, [ALGE-017](./017-order-statistics-and-quickselect.md) supplies selection contracts, [ALGE-020](./020-engineering-a-sort-for-real-data-distributions.md) uses sampling for diagnosis, and [ALGE-030](../ROADMAP.md) compares design paradigms.

## Governing Question

How do we turn random choices into a precisely specified algorithmic resource, prove what they buy, and operate the resulting algorithm without confusing probability, reproducibility, and security?

Randomization can destroy a hostile pattern, sample a large stream, balance a data structure without rotations, choose a compact fingerprint, or trade deterministic certainty for a tunable error probability. Its value comes from a distributional invariant: for every covered input, the algorithm's internal choices make undesirable executions sufficiently rare or make the expected work sufficiently small.

The word “random” is not a proof. The design must name the sample space, distribution, required independence, adversary, output contract, and resource budget. The implementation must then realize those choices without bias, preserve deterministic replay when needed, and obtain unpredictable entropy when replay would be a vulnerability.

## Why This Matters

Randomization is one of the few design tools that can change both simplicity and robustness. A uniform quicksort pivot gives an expected comparison bound for every fixed ordering rather than relying on a benign input distribution. A uniformly shuffled worklist can remove a systematic order effect. Reservoir sampling preserves a uniform sample without knowing stream length. Universal hashing chooses a function independently of the keys and bounds expected collision behavior. Random priorities yield treaps and skip-list levels. Random contraction turns a global graph question into repeated simple trials. Probabilistic primality tests provide one-sided error that can be driven extremely low.

Production use introduces concerns absent from a blackboard proof. Random words must be converted to bounded choices correctly. Generators have algorithms, finite states, periods, initialization requirements, and version behavior. Parallel jobs need stream ownership. Retries need new trial identities. Experiments need replay records. Services exposed to adaptive clients need explicit leakage assumptions. Security tokens need an approved entropy and deterministic-random-bit-generation path, not a fast simulation generator.

Randomness also creates observability traps. A mean hides rare long runs. A trial may be selected for logging only after success. A fixed canary seed may miss whole behaviors. A rollout can accidentally correlate every replica. The engineering discipline is therefore to make probability part of the API and evidence model rather than an invisible call buried inside an implementation.

## Prerequisites and Retrieval

Retrieve:

- finite sets, functions, counting, permutations, combinations, and geometric series;
- conditional probability, independence, expectation, indicator variables, and linearity of expectation;
- union bounds, Markov's inequality, and elementary exponential inequalities;
- asymptotic time and space, worst-case versus expected cost, and tail percentiles;
- sorting, partitioning, selection, hashing, graph contraction, and streaming;
- modular arithmetic, fixed-width words, rejection sampling, and overflow;
- preconditions, postconditions, loop invariants, witness verification, and error status;
- pseudorandom generators, seeds, state, domain separation, and reference vectors;
- concurrency, retries, idempotence, snapshot identity, telemetry, and rollout controls;
- threat models, entropy, unpredictability, and the distinction between simulation and cryptographic randomness.

You should be able to explain why linearity of expectation does not require independence, while multiplying trial failure probabilities usually does.

## Learning Objectives

After completing this module, you should be able to:

1. model a randomized algorithm as deterministic execution over an explicit random tape;
2. distinguish Las Vegas, one-sided Monte Carlo, two-sided Monte Carlo, and heuristic behavior;
3. separate internal randomization from average-case assumptions about inputs;
4. derive exact distributions for bounded draws, permutations, reservoirs, pivots, and hash collisions;
5. prove expected-cost and error-amplification results with their quantifiers and independence premises;
6. implement unbiased bounded sampling and deterministic replay without claiming cryptographic security;
7. choose randomization for sorting, selection, streaming, hashing, data structures, graphs, or number theory;
8. design stream ownership, retry, concurrency, observability, and failure policies;
9. validate structural invariants, reference sequences, bounded distributions, statistical behavior, and adversarial cases independently;
10. decide when deterministic, randomized, hybrid, or verified-probabilistic behavior best fits a problem contract.

## Core Exposition

### Model a random tape before selecting a generator

A randomized procedure is easiest to reason about as a deterministic function with an extra input. Let

$$
A:\mathcal X\times\mathcal R\to\mathcal Y\times\mathcal C,
$$

where $\mathcal X$ is the valid input domain, $\mathcal R$ is a space of random tapes, $\mathcal Y$ is the output domain, and $\mathcal C$ records cost or trace information. A distribution $\mathcal D$ over $\mathcal R$ induces the output and cost distributions.

This formulation separates three obligations:

1. **semantic behavior:** which outputs can each tape produce?
2. **probabilistic behavior:** how much measure do good, bad, and expensive tapes receive?
3. **realization:** does the generator and range-mapping code implement the assumed tape distribution closely enough for the contract?

Fixing $x$ and $R$ fixes every pivot, sample, priority, retry, and tie. That makes a failing execution a deterministic artifact that can be replayed if the generator contract is stable. It also makes clear that a seed is not “the randomness” by itself: generator family, version, derivation tree, draw order, and input snapshot are part of the mapping from seed to tape.

### Choose the correctness class explicitly

A **Las Vegas** algorithm may vary in work, but every normal answer is correct. Randomized quickselect is Las Vegas when it continues until the requested rank is isolated and validates its partition invariants. A restart cap changes the API: after the cap, it must return an explicit incomplete result or invoke a correct deterministic fallback. Returning the current guess would silently turn it into Monte Carlo behavior.

A **Monte Carlo** algorithm has a probability of error or inconclusive output. Its contract needs:

- whether error is one-sided or two-sided;
- the bound for one trial and for the deployed repetition rule;
- the random-choice assumptions behind the bound;
- whether the result is independently verifiable;
- the behavior on budget exhaustion or entropy failure.

For a one-sided primality test, a composite witness proves compositeness, while “probable prime” retains a false-positive bound. For a randomized min-cut trial, the cut it emits is always a valid cut, but it may not be minimum; taking the smallest cut over trials is a safe aggregation because success of any trial suffices.

Do not put an unproved heuristic into either category. Random tie breaking, randomized local search, or a hash fingerprint can be useful even without a theorem, but the API and documentation must say what is measured rather than borrowing a formal error bound from a different sampling process.

### Separate internal coins from random inputs

Average-case analysis assumes an input distribution $\mu$ and studies

$$
\mathbb E_{x\sim\mu}[C(D,x)]
$$

for a deterministic algorithm $D$. Randomized analysis can instead establish

$$
\max_{x\in\mathcal X_n}\mathbb E_R[C(A,x;R)]\le f(n).
$$

The latter promise covers every fixed input of size $n$, provided the input is fixed independently of hidden random choices. It does not automatically cover an adaptive adversary that observes pivots, table locations, timing, or past outputs before choosing the next operation.

Name the adversary:

- an **oblivious adversary** fixes the full operation sequence before the random tape is drawn;
- an **online adversary** may react to public history but not hidden current choices;
- an **adaptive adversary** may use revealed behavior to shape later inputs;
- a **state-compromise adversary** may learn generator state and predict related outputs.

A proof against one model does not transfer silently to another. Rekeying a hash family, hiding seeds, limiting timing leakage, or selecting a deterministic worst-case fallback may be necessary at an exposed boundary.

### Generate uniform finite choices without modulo bias

Assume a source returns a uniform $w$-bit word $X\in\{0,\ldots,M-1\}$ where $M=2^w$, and let $1\le b\le M$. To draw uniformly from $\{0,\ldots,b-1\}$, define

$$
L=\left\lfloor\frac Mb\right\rfloor b.
$$

Draw until $X<L$, then return $X\bmod b$. Every residue has exactly $L/b$ accepted preimages. The rejection probability is

$$
\frac{M-L}{M}
=\frac{M\bmod b}{M}
<\frac bM.
$$

Direct modulo is unbiased only when $b$ divides $M$. Scaling a floating-point variate by $b$ may also be biased or make some large-range integers unreachable because the variate has finite precision. Prefer a runtime's documented uniform bounded-integer primitive or implement a reviewed word-level method with known overflow behavior.

Range contracts include endpoints. Confusing `[0,b)` with `[0,b]` changes distributions, array safety, and proofs. Invalid bounds, entropy-source failure, and rejection cancellation need explicit behavior rather than infinite loops or fallback to a biased expression.

### Treat seeds and streams as versioned resources

A pseudorandom generator is a deterministic state machine:

$$
s_{t+1}=T(s_t),\qquad z_t=G(s_t).
$$

The initial state derives from a seed. Period, equidistribution, empirical test results, or speed can support a simulation use case, but none alone establishes unpredictability. Conversely, a cryptographic deterministic random bit generator still needs sufficient entropy, correct instantiation, reseeding policy, health handling, and protection of internal state.

For reproducible algorithm engineering, record at least:

- generator algorithm and semantic version;
- root seed or an authorized opaque seed reference;
- stream or domain identifier;
- trial, partition, and attempt identity;
- range-conversion algorithm;
- relevant implementation version and input digest.

Never log secret generator state or security seeds merely to gain replay. Security incidents need safe audit metadata and test-only deterministic fixtures, not disclosure of production secrets.

Parallel code should derive a stream from stable logical ownership, such as `(job, stage, partition, trial)`, rather than thread number or execution order. A retry must either replay the same logical trial idempotently or receive a fresh, recorded trial identity; it must not ambiguously do both.

### Shuffle by successive uniform placement

For an array of length $n$, the in-place Fisher–Yates form iterates $i=n-1,n-2,\ldots,1$, draws $j$ uniformly from $\{0,\ldots,i\}$, and swaps positions $i$ and $j$. There are

$$
n(n-1)\cdots2=n!
$$

possible choice sequences, each with probability

$$
\frac1n\frac1{n-1}\cdots\frac12=\frac1{n!}.
$$

Each choice sequence produces one permutation, so every permutation is uniform. The proof depends on every bounded draw being uniform and on the declared identity model. Equal values make several identity permutations look the same; a value-level frequency test must account for that quotient.

Sorting records by independent random keys is not automatically a uniform shuffle. Finite keys collide, and the sort's tie policy then changes permutation probabilities. Drawing keys large enough to make collisions “unlikely” creates a Monte Carlo approximation with an error budget, not the exact Fisher–Yates contract.

### Randomize pivots to detach cost from input order

For randomized quicksort on $n$ distinct ranks, let $X_{ij}$ indicate whether ranks $i<j$ are compared. They are compared exactly when the first pivot chosen from ranks $i,\ldots,j$ is one of the endpoints, hence

$$
\Pr[X_{ij}=1]=\frac{2}{j-i+1}.
$$

By linearity of expectation,

$$
\mathbb E[C_n]
=\sum_{1\le i<j\le n}\mathbb E[X_{ij}]
=2(n+1)H_n-4n
=\Theta(n\log n).
$$

No independence among the indicators is required. The input ordering can be arbitrary, but pivot choice must be uniform among active ranks and independent of that fixed input. Equal keys require a declared three-way partition or a separate analysis. Expected comparisons do not bound recursion depth on every tape, so production implementations commonly cap depth and fall back to a worst-case-safe sorter.

Randomized quickselect applies the same idea to one active partition. Correctness is deterministic conditional on each chosen pivot; randomness changes the sequence of subproblem sizes. Stable identity and rank semantics still matter when keys repeat.

### Execute a replayable randomized selection

The following executable uses a fixed SplitMix-style generator solely to make the educational run reproducible. Its rejection method realizes uniform bounded choices from 64-bit words. The generator is not offered for secrets, and the module's theorem does not depend on this particular generator.

<!-- bijux-verify: {"id":"replayable-randomized-selection","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"selection=value:7 index:2 pivots:(5, 7) words:2\nshuffle=('d', 'e', 'b', 'c', 'a') words:4\n","stderr":""}} -->
```python
from dataclasses import dataclass

MASK = (1 << 64) - 1


class ReplayRng:
    def __init__(self, seed: int) -> None:
        self.state = seed & MASK
        self.words = 0

    def next_u64(self) -> int:
        self.state = (self.state + 0x9E3779B97F4A7C15) & MASK
        z = self.state
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & MASK
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & MASK
        self.words += 1
        return (z ^ (z >> 31)) & MASK

    def uniform_below(self, bound: int) -> int:
        modulus = 1 << 64
        if not 0 < bound <= modulus:
            raise ValueError("bound outside the 64-bit source domain")
        limit = modulus - modulus % bound
        while True:
            word = self.next_u64()
            if word < limit:
                return word % bound


@dataclass(frozen=True)
class Selection:
    value: int
    source_index: int
    pivot_values: tuple[int, ...]


def randomized_select(
    values: tuple[int, ...], rank: int, rng: ReplayRng
) -> Selection:
    if not 0 <= rank < len(values):
        raise IndexError("rank outside the input")
    active = list(enumerate(values))
    pivots: list[int] = []
    while True:
        pivot = active[rng.uniform_below(len(active))][1]
        pivots.append(pivot)
        lower = [item for item in active if item[1] < pivot]
        equal = [item for item in active if item[1] == pivot]
        higher = [item for item in active if item[1] > pivot]
        if rank < len(lower):
            active = lower
        elif rank < len(lower) + len(equal):
            source_index = min(index for index, _ in equal)
            return Selection(pivot, source_index, tuple(pivots))
        else:
            rank -= len(lower) + len(equal)
            active = higher


def fisher_yates(values: tuple[str, ...], rng: ReplayRng) -> tuple[str, ...]:
    items = list(values)
    for i in range(len(items) - 1, 0, -1):
        j = rng.uniform_below(i + 1)
        items[i], items[j] = items[j], items[i]
    return tuple(items)


selection_rng = ReplayRng(0xA17E029)
selection = randomized_select((9, 1, 7, 3, 7, 5), 3, selection_rng)
shuffle_rng = ReplayRng(0x5EED029)
shuffled = fisher_yates(("a", "b", "c", "d", "e"), shuffle_rng)

print(
    f"selection=value:{selection.value} index:{selection.source_index} "
    f"pivots:{selection.pivot_values} words:{selection_rng.words}"
)
print(f"shuffle={shuffled} words:{shuffle_rng.words}")
```

The selected rank is zero-based over the multiset: sorted values are $(1,3,5,7,7,9)$, so rank 3 has value 7. The contract chooses the smallest source index among equal selected keys. Every returned result can be replayed against a deterministic sorting oracle; the pivot trace and consumed-word count are evidence, not a portable seed contract by themselves.

### Sample an unknown-length stream with a reservoir

To retain a uniform sample of $k$ identities from a stream whose final length is not known, place the first $k$ items in a reservoir. When the $t$th item arrives using one-based indexing and $t>k$, draw $J$ uniformly from $\{1,\ldots,t\}$. If $J\le k$, replace reservoir slot $J$.

After processing $t$ items, each item is present with probability $k/t$. An old item survives the next step with probability

$$
\frac{k}{t}\left(1-\frac1{t+1}\right)
=\frac{k}{t+1},
$$

while the new item is inserted with probability $k/(t+1)$. A stronger subset-level argument shows that every $k$-subset is equally likely, not merely that marginal inclusion probabilities match.

The unit of sampling must be explicit. Events, users, bytes, requests, and deduplicated keys induce different populations. Merged reservoirs require weights or priority constructions that reflect shard sizes; concatenating equal-size local samples overweights small shards. Late records, retries, deletes, and a stream that ends before $k$ all affect the contract.

### Randomize a hash family, not the key assumption

Let $\mathcal H$ be a universal family mapping universe $U$ to $m$ buckets, meaning that for distinct $x,y\in U$,

$$
\Pr_{h\sim\mathcal H}[h(x)=h(y)]\le\frac1m.
$$

For a fixed set $S$ of $n$ distinct keys, define an indicator for every unordered pair. Linearity of expectation gives

$$
\mathbb E_h[\text{colliding pairs}]
\le\binom n2\frac1m.
$$

The keys need not be sampled from a benign distribution; the function is sampled independently of the fixed keys. This does not imply cryptographic collision resistance, secrecy, or resilience after an adaptive party learns enough about $h$. It also does not make a poor table load factor disappear. Function-family definition, seed secrecy or publicity, bucket reduction, deletion semantics, and rehash policy remain part of the design.

### Build probabilistically balanced structures

A treap assigns each key a random priority, maintains binary-search order by key, and heap order by priority. With independent continuous priorities, the tree shape has the distribution of a binary search tree built in uniformly random insertion order, regardless of actual insertion order. Equal priorities in a finite representation require a deterministic secondary key or a collision policy.

In a skip list, each node independently reaches another level with probability $p$. Under the ideal model,

$$
\Pr[\text{one node reaches level }h]=p^h,
\qquad
\Pr[\text{some of }n\text{ nodes reaches }h]\le np^h.
$$

The second statement is a union bound, not equality. Expected search work is logarithmic under the stated random-level assumptions; a realized structure can be taller, and an adversary who predicts levels may target weak shapes. Persisted structures must persist priorities or levels rather than redraw them differently on recovery.

### Use repeated contraction when any successful trial certifies the optimum

Karger's basic contraction algorithm repeatedly chooses a uniformly random current multigraph edge, contracts its endpoints, retains parallel edges, and removes self-loops until two supervertices remain. The remaining crossing edges form a valid cut. For a fixed minimum cut in an $n$-vertex graph, a single trial preserves it with probability at least

$$
\prod_{r=3}^{n}\left(1-\frac2r\right)
=\frac{2}{n(n-1)}.
$$

The proof uses the fact that a graph with minimum-cut value $\lambda$ and $r$ supervertices has at least $r\lambda/2$ edges, while exactly $\lambda$ edges cross the fixed cut. Avoiding those cut edges at size $r$ therefore has conditional probability at least $1-2/r$.

The output cut is always valid, but a trial may miss the global minimum. Taking the smallest verified cut across independent trials succeeds if any trial preserves a minimum cut. Correct implementation must sample multigraph edges by multiplicity, preserve original vertex membership for lifting, use fresh trial streams, and never mistake “best seen” for a deterministic optimality certificate.

### Amplify only a proved event

Suppose a trial's good event has probability at least $p$ and fresh trials are independent. If any good trial is enough, $r$ trials fail with probability at most

$$
(1-p)^r.
$$

To make this at most $\delta$, choose

$$
r\ge
\left\lceil
\frac{\log\delta}{\log(1-p)}
\right\rceil.
$$

Because both logarithms are negative, the ratio is positive. The looser inequality $(1-p)^r\le e^{-pr}$ yields the sufficient condition $r\ge\lceil\log(1/\delta)/p\rceil$.

Majority vote applies to a different event. If independent two-sided trials are correct with probability strictly greater than $1/2$, concentration can bound majority error. Repeating a biased estimator does not remove bias. Reusing identical streams gives no amplification. Choosing the best metric across many noisy trials can introduce selection bias unless the validation procedure accounts for that choice.

### Use one-sided error without erasing its direction

For an odd candidate $N>2$, the Miller–Rabin procedure writes

$$
N-1=2^sd
$$

with $d$ odd and tests a sampled base through modular exponentiation. A compositeness witness proves that $N$ is composite. Passing a sampled base means only that the base did not expose compositeness. Under the standard independent uniform-base theorem for an odd composite, at most one quarter of eligible bases are strong liars, so $r$ independent rounds give a false-probable-prime bound at most $4^{-r}$.

The exact base domain, small-prime cases, uniform sampling, modular multiplication, independence, and input model matter. Some fixed base sets deterministically cover bounded integer ranges, but that is a different theorem with a range-specific proof. A “probably prime” result must not be relabeled “prime” unless a deterministic certificate or range theorem supplies that contract.

Random fingerprints for polynomial or string equality have similar one-sided structure when unequal objects collide with bounded probability but equal objects always match. The field, evaluation-point domain, degree bound, canonical encoding, and adversary timing determine the actual guarantee.

### Combine probability with verification, budgets, and fallback

Randomization is especially attractive when answers are cheap to verify. A randomized search can propose a witness, and a deterministic predicate can validate it. A probabilistic equality test can trigger an exact comparison on a fingerprint match. A randomized optimizer can produce feasible incumbents while a lower-bound method controls the remaining optimality gap.

Design the termination state explicitly:

- **verified result:** the deterministic checker accepts;
- **probabilistic result:** the declared error bound and evidence accompany it;
- **inconclusive:** the trial, time, memory, or entropy budget ended;
- **fallback result:** a deterministic method completed under its own contract;
- **failed:** an invariant, source, or infrastructure dependency failed.

Expected termination is not a permission to run forever. Use a checked iteration budget, cancellation points, memory ceilings, and a fallback selected before deployment. Do not condition performance metrics only on runs that happened to finish.

### Partition streams independently of scheduling

A global mutable generator protected by a lock serializes parallel work and makes draw order depend on scheduling. Copying its state gives workers identical streams. Seeding each worker with nearby integers offers no general proof that streams are independent.

A stable design derives substreams by a reviewed splitting or counter-based mechanism and domain-separates logical owners. Let

$$
d=(\text{job},\text{stage},\text{partition},\text{trial},\text{purpose}).
$$

The stream identifier is a canonical encoding of $d$, not its language-specific default hash. Rescheduling the same logical owner then reproduces the same choices. A new independent trial changes the trial component. Speculative duplicates share an idempotence key so only one result publishes, while their randomness policy remains explicit.

Distributed amplification needs global trial accounting. A coordinator records which disjoint trial identities reached verified completion; a quiet queue or a worker's local count is not proof that $r$ independent trials finished. Lost, duplicated, or partially logged trials change the actual failure bound.

### Keep security randomness in a separate contract

Algorithmic randomness may need uniformity and reproducibility. Security randomness needs unpredictability against a stated attacker, sufficient entropy, state protection, and often compromise resistance. These goals can conflict: publishing a seed makes experiments replayable and security tokens predictable.

Use platform or library interfaces backed by applicable cryptographic guidance for keys, nonces whose construction requires randomness, reset tokens, salts, session identifiers, and secret sampling. Do not implement a deterministic random bit generator from an algorithm-course example. Do not infer security from a long period or a statistical test suite. A 128-bit output derived from an eight-bit seed has at most eight bits of seed uncertainty to an attacker who knows the construction.

Cryptographic protocols also impose domain-specific nonce rules; “random-looking” is not a substitute for uniqueness, unpredictability, or misuse resistance. Route those choices to the security specification that owns them.

### Measure distributions without replacing proofs

Validation has complementary layers:

1. **structural proof:** map implementation choices to the sample space and show distribution preservation;
2. **reference vectors:** verify generator and derivation behavior for known states;
3. **bounded exhaustive checks:** enumerate small choice spaces and compare exact outcome counts;
4. **metamorphic checks:** permute labels, replay seeds, split work, and compare invariant outputs;
5. **statistical diagnostics:** detect large distribution regressions over many samples;
6. **adversarial tests:** exercise chosen inputs, adaptive sequences, collisions, cancellation, and resource limits;
7. **production telemetry:** observe tails, rejection rate, retries, stream reuse, error budgets, and fallback.

A chi-squared or similar diagnostic can reject a generator-range pipeline that is visibly inconsistent with a target distribution. Failure is evidence of a defect; passing is not proof of exact uniformity or security. Select tests and significance thresholds before inspecting results, account for repeated testing, and retain sample counts and software versions.

### Govern tail cost and service behavior

An expectation is an average over tapes, not a service-level objective. If $C\ge0$, Markov's inequality gives

$$
\Pr[C\ge a]\le\frac{\mathbb E[C]}a,
$$

but this bound may be far too weak for operational use. A geometric retry loop with per-attempt success probability $p$ has expected attempt count $1/p$, yet it has no finite deterministic maximum. Quicksort has a quadratic worst-case tape even though expected comparisons are $\Theta(n\log n)$.

Measure the full distribution of comparisons, draws, rejections, restarts, depth, allocation, and wall time. State any concentration theorem and its premises. Cap work where necessary and preserve semantics with an inconclusive result or deterministic fallback. If fallback activates on a rare event, test it deliberately; ordinary random tests may almost never traverse it.

### Use a randomized-design worksheet

For each proposed randomized component, record:

1. fixed input domain, output semantics, identity, multiplicity, and tie contract;
2. the obstruction that randomization is intended to remove;
3. Las Vegas, one-sided Monte Carlo, two-sided Monte Carlo, sampling, or heuristic classification;
4. random variables, sample spaces, distributions, and range endpoints;
5. adversary timing, visibility, and state-compromise assumptions;
6. correctness event, failure event, and deterministic verifier if any;
7. expected cost, tail claim, hard budget, and fallback;
8. required independence or limited-independence property;
9. generator, entropy source, seed policy, version, and domain separation;
10. concurrency, partition, retry, and speculative-execution ownership;
11. amplification or aggregation rule and deployed error calculation;
12. overflow, rejection, cancellation, and entropy-failure behavior;
13. replay evidence that is safe to retain;
14. bounded oracle, exact-distribution, reference-vector, and metamorphic tests;
15. statistical diagnostics and production telemetry;
16. rollout limits, security review boundary, rollback trigger, and deterministic alternative.

Randomization is ready only when another engineer can reconstruct the probability claim and the operational stream graph without guessing.

## Definitions and Notation

- $\mathcal X$: valid input domain; $\mathcal X_n$ is the subset of size $n$.
- $\mathcal R$: random-tape space.
- $\mathcal D$: declared probability distribution over random tapes.
- $A(x;R)$: deterministic execution of algorithm $A$ on input $x$ and tape $R$.
- $C(x,R)$: nonnegative cost of that execution under a declared cost model.
- $G(x,R)$: event that the execution satisfies the desired success condition.
- $\varepsilon(x)$: upper bound on contract violation probability for input $x$.
- $p$: lower bound on success probability of one trial; $q=1-p$ is its failure upper bound.
- $r$: number of completed trials counted by an amplification argument.
- $\delta$: deployed upper bound requested for aggregate failure.
- $X_i$: random variable; $\mathbf 1_E$ is the indicator of event $E$.
- $\mathbb E[X]$: expectation of random variable $X$.
- $\Pr[E]$: probability of event $E$ in the declared probability space.
- $H_n=\sum_{k=1}^{n}1/k$: the $n$th harmonic number.
- $M=2^w$: number of values emitted by a uniform $w$-bit source.
- $b$: exclusive upper bound for a bounded draw, with $1\le b\le M$ in the stated word-rejection construction.
- $L=\lfloor M/b\rfloor b$: largest multiple of $b$ not exceeding $M$.
- $\mathcal H$: a sampled family of hash functions; $m$ is its bucket count.
- $s_t$: generator state before a transition; $z_t$ is an emitted word.
- $d$: canonical domain separator identifying logical stream ownership.
- **Entropy** measures uncertainty in a modeled source; output length is not entropy.
- **Seed** initializes generator state; **state** may contain more information than the external seed.
- **Reference vector** is a known input/state and output sequence used to detect implementation drift.
- **Rejection sampling** discards source outcomes so every accepted target outcome has equal preimage count.
- **Replay** reconstructs a run under a recorded generator and derivation contract.
- **Independence** of $X$ and $Y$ means $\Pr[X\in S,Y\in T]=\Pr[X\in S]\Pr[Y\in T]$ for all relevant sets $S,T$.
- **Pairwise independence** is weaker than mutual independence and supports only arguments that need pairwise relationships.
- **With high probability** is an asymptotic phrase that requires an explicit bound such as $1-n^{-c}$; it is not a synonym for “usually.”

Probability subscripts identify what is sampled. For example,

$$
\Pr_R[G(x,R)]
$$

holds the input fixed and samples the tape, whereas

$$
\Pr_{x\sim\mu,R\sim\mathcal D}[G(x,R)]
$$

also samples an input. These are different contracts even when an experiment estimates them with similar code.

## Mechanisms, Invariants, or Proof Structure

### Random-tape soundness

Let $V(x,y)$ be the deterministic validity predicate for a returned answer. A Las Vegas implementation is sound if

$$
\forall x\in\mathcal X,\ \forall R\in\mathcal R:
A(x;R)=y
\Longrightarrow
V(x,y).
$$

Randomness is absent from this implication because correctness holds tape by tape. If some tapes produce an explicit incomplete result $\bot$, use

$$
A(x;R)=y\ne\bot\Longrightarrow V(x,y).
$$

Termination then has a separate distributional or budget argument. A verifier establishes validity of emitted answers, not completeness of a search or optimality unless its predicate proves those stronger properties.

For Monte Carlo behavior, define bad tapes

$$
\mathcal B_x=
\{R:A(x;R)\text{ violates the output contract}\}.
$$

The error proof must establish $\Pr_R[R\in\mathcal B_x]\le\varepsilon(x)$ for every covered input. Measuring a small fraction over a convenient input sample proves neither the universal quantifier nor the bound.

### Linearity-of-expectation mechanism

If total cost decomposes as

$$
C=\sum_{i=1}^{k}X_i
$$

and each $X_i$ is integrable, then

$$
\mathbb E[C]
=\sum_{i=1}^{k}\mathbb E[X_i].
$$

The $X_i$ need not be independent. This is why randomized quicksort can sum pair-comparison indicators even though pivot events interact. Independence becomes necessary only when a later step factors joint probabilities or applies a theorem whose premises demand it.

Expectation also obeys a tail-sum identity for a nonnegative integer-valued $T$:

$$
\mathbb E[T]=\sum_{t\ge0}\Pr[T>t].
$$

This can derive geometric retry cost. It does not turn a finite expectation into a hard upper bound.

### Rejection-sampling proof

Partition the accepted set $\{0,\ldots,L-1\}$ into residue classes modulo $b$. Because $L$ is a multiple of $b$, every residue has exactly $L/b$ representatives. Conditional on acceptance,

$$
\Pr[X\bmod b=j\mid X<L]
=\frac{L/b}{L}
=\frac1b.
$$

Every attempt accepts with probability $L/M$, so independent fresh words give expected attempt count

$$
\frac{1}{L/M}=\frac ML.
$$

The proof assumes a uniform source word and exact integer comparisons. A defective source is not repaired merely by rejecting a high interval.

### Fisher–Yates bijection proof

At iteration $i$, the algorithm selects which one of the $i+1$ remaining identities occupies final position $i$. Once placed, that identity is never moved again. Reading choices from $i=n-1$ down to $1$ defines a unique permutation. Conversely, reading a desired permutation from its final position backward determines the unique choice at every iteration.

Thus choice sequences and identity permutations are in bijection. Uniform independent choice at each step assigns probability

$$
\prod_{i=1}^{n-1}\frac1{i+1}=\frac1{n!}
$$

to each permutation. An off-by-one range that draws only from $\{0,\ldots,i-1\}$ excludes every sequence that leaves position $i$ unchanged and destroys the bijection.

### Reservoir invariant proof

Induct on processed length $t\ge k$. At $t=k$, the reservoir is the only $k$-subset, so it is uniform. Assume every $k$-subset of the first $t$ items has probability $1/\binom tk$.

For a target subset $Q$ of the first $t+1$ items:

- if $Q$ omits the new item, it must already be the reservoir and the new item must be rejected, giving

$$
\frac1{\binom tk}\frac{t+1-k}{t+1}
=\frac1{\binom{t+1}k};
$$

- if $Q$ contains the new item, a predecessor is $Q$ without the new item plus one of the $t-k+1$ old identities outside $Q$; for each such predecessor, replacing that outside identity has probability $1/(t+1)$, giving

$$
(t-k+1)\frac1{\binom tk}\frac1{t+1}
=\frac1{\binom{t+1}k}.
$$

Therefore every $k$-subset remains uniform. Marginal inclusion $k/(t+1)$ follows, but the subset theorem is stronger.

### Quicksort comparison proof

For distinct sorted ranks $i<j$, ranks outside $[i,j]$ cannot determine whether $i$ and $j$ meet. Among the $j-i+1$ ranks in the interval, the first selected pivot separates them unless that pivot is $i$ or $j$. Because the first pivot is uniform, the endpoint event has probability $2/(j-i+1)$.

Summing by distance $d=j-i$,

$$
\mathbb E[C_n]
=\sum_{d=1}^{n-1}(n-d)\frac{2}{d+1}
=2(n+1)H_n-4n.
$$

The exact equality is for distinct ranks and the stated partition comparison model. Three-way partitioning, pivot-sampling overhead, insertion-sort cutoffs, branch behavior, and memory traffic require their own accounting.

### Universal-hashing collision proof

For each unordered key pair $\{x,y\}\subseteq S$, define

$$
I_{xy}=\mathbf 1_{\{h(x)=h(y)\}}.
$$

Then

$$
\text{colliding pairs}=\sum_{\{x,y\}\subseteq S}I_{xy}.
$$

Universality gives $\mathbb E[I_{xy}]\le1/m$. Linearity yields

$$
\mathbb E[\text{colliding pairs}]
\le\frac{\binom n2}{m}.
$$

This is an expectation over the chosen function for a fixed distinct-key set. It is neither a bound on maximum chain length for every function nor a security claim.

### Amplification proof and accounting invariant

Let $F_i$ be failure of completed trial $i$. If the trials are independent and $\Pr[F_i]\le q$, then

$$
\Pr\left[\bigcap_{i=1}^{r}F_i\right]
=\prod_{i=1}^{r}\Pr[F_i]
\le q^r.
$$

The product step is exactly where independence is used. If all trials share the same tape, the left side can remain $q$, regardless of $r$.

Operationally, count only trials with distinct justified stream identities that reached the proof's terminal event. Retried fragments, speculative duplicates, cancelled workers, and unverified outputs do not automatically add to $r$. The coordinator should publish the bound computed from the durable completed-trial set, not a requested trial count.

### Karger survival proof

Fix a particular minimum cut of value $\lambda$. With $r$ supervertices remaining, every supervertex has degree at least $\lambda$, so the current multigraph has at least $r\lambda/2$ edges. Conditional on preserving the fixed cut so far, exactly $\lambda$ current edges cross it. A uniform edge contraction avoids it with probability at least

$$
1-\frac{\lambda}{r\lambda/2}
=1-\frac2r.
$$

Multiplying the conditional probabilities from $r=n$ through $3$ telescopes:

$$
\prod_{r=3}^{n}\frac{r-2}{r}
=\frac{2}{n(n-1)}.
$$

Sampling unique endpoint pairs instead of edge copies is not uniform on a multigraph and invalidates this proof.

### Generator-publication invariant

A reproducible randomized result should bind the tuple

$$
(\text{input digest},\text{algorithm version},\text{generator version},
\text{root reference},\text{domain},\text{completed trials},
\text{aggregation rule})
$$

to the output and its claimed bound. Publication is atomic only after input and implementation revisions match, every counted trial is terminal and verified as required, duplicate trial identities are removed, the bound is recomputed, and sensitive seed material is excluded from ordinary logs.

For security-sensitive randomness, replace public replay material with the audit fields permitted by the owning security design. Reproducibility and secrecy are separate invariants.

## Alternatives and Trade-Offs

| Design | Correctness profile | Principal benefit | Principal cost or risk | Prefer when |
|---|---|---|---|---|
| Deterministic worst-case algorithm | Same bound on every execution | Predictable semantics and tails | May be more complex or slower in common regimes | Hard deadlines or hostile adaptive inputs dominate |
| Las Vegas randomization | Every returned answer correct; cost varies | Often simple and input-order robust | Rare long executions and stream governance | Answers are verifiable and fallback is available |
| One-sided Monte Carlo | Only one answer direction can err | Clean certificates in the other direction | Caller must preserve “probable” status | The error direction is operationally acceptable |
| Two-sided Monte Carlo | Either answer may err within a bound | Can reduce work dramatically | Aggregation and error budgets are harder | Bounded approximation is an explicit product contract |
| Randomized preprocessing | Random structure supports later operations | Amortizes sampling or balancing | Updates, leakage, and stale state | Many queries share one controlled snapshot |
| Reservoir or priority sampling | Fixed memory over an unknown stream | Single-pass representative subset | Population and merge semantics are subtle | Exact full retention is impossible or unnecessary |
| Universal hashing | Expectation over a sampled function for fixed keys | Reduces reliance on input distribution | Adaptive leakage and rehash complexity | Key distribution is unknown and threat model fits |
| Random priorities or levels | Expected balance with simple updates | Avoids rigid balancing machinery | Realized tails and persistence requirements | Expected bounds and simpler concurrency are valuable |
| Repeated randomized search | Failure falls exponentially under premises | Embarrassingly parallel amplification | Duplicate streams waste trials | Any successful trial can be recognized or safely aggregated |
| Deterministic seed in tests | Exact replay | Excellent diagnosis and fixtures | Narrow seed coverage; unsafe for secrets | Reproducibility is the goal |
| Entropy-backed secure generator | Unpredictability under a security model | Protects secrets and tokens | Platform dependency and state lifecycle | An attacker benefits from prediction |
| Hybrid with deterministic fallback | Expected fast path plus bounded completion | Controls tails without discarding randomization | Two implementations and transition testing | A hard service budget coexists with average speed goals |

Randomization should remove a named dependency or reduce a quantified cost. Adding random tie breaking to an already stable algorithm can make incidents harder to reproduce without improving a theorem or workload. Conversely, forcing determinism can require complex balancing or retain a hostile order effect. Compare the whole contract rather than treating either choice as inherently superior.

A useful expected-speed comparison is

$$
\mathbb E[C_{\mathrm{hybrid}}]
=\mathbb E[\min(C_R,B)]
+\Pr[C_R>B]C_F,
$$

where $C_R$ is randomized-path work, $B$ is the cutoff, and $C_F$ is fallback work after the cutoff. This expression is schematic: duplicated setup, partially reusable progress, cache effects, and cancellation overhead must be included in an implementation model.

When error has business cost $L$ and execution cost is $C(r)$ for $r$ trials, an expected-loss objective might be

$$
C(r)+Lq^r.
$$

That is not sufficient for safety-critical policy: regulatory, ethical, or per-case constraints may impose a hard error ceiling regardless of average monetary loss.

## Failure Modes and Misconceptions

1. **Implicit probability space:** the design says “choose randomly” without naming outcomes or their probabilities.
2. **Average-input substitution:** a measurement over shuffled test inputs is used to claim internal-randomization guarantees for every input.
3. **Modulo bias:** a fixed-width word is reduced modulo a bound that does not divide the word domain.
4. **Float scaling:** finite floating-point values make some large bounded integers unreachable or unequally likely.
5. **Inclusive-bound confusion:** a draw intended for `[0,b)` sometimes returns $b$.
6. **Shuffle by random keys:** finite-key collisions and tie behavior distort permutation probabilities.
7. **Off-by-one shuffle:** position $i$ cannot select itself, excluding many permutations.
8. **Identity collapse:** duplicate values are treated as one object although sampling is over source identities.
9. **Wrong reservoir population:** sampling requests instead of users, or shards instead of records, answers a different question.
10. **Naive reservoir merge:** equally weighting local samples overweights small partitions.
11. **Reseeding per call:** clock or process identifiers create repeated, predictable, or highly correlated prefixes.
12. **Copied state:** forked workers emit identical streams and amplification counts duplicates.
13. **Schedule-owned stream:** thread interleavings change results and make replay unstable.
14. **Adjacent-seed assumption:** numerically different seeds are asserted to create independent streams without a generator-specific argument.
15. **Unversioned replay:** a seed is retained but generator, range mapping, code, or input revision changes.
16. **Secret seed logging:** a security-sensitive state is exposed in ordinary diagnostic metadata.
17. **Simulation generator for secrets:** speed, period, or statistical quality is mistaken for unpredictability.
18. **Output-length entropy:** a long deterministic expansion is claimed to contain as much entropy as its output bits.
19. **Las Vegas drift:** a timeout returns the current guess instead of incomplete status or a correct fallback.
20. **Monte Carlo relabeling:** “probable prime,” fingerprint equality, or best observed cut is presented as certain.
21. **Wrong error direction:** a one-sided theorem is documented as if both false positives and false negatives were bounded.
22. **Unproved amplification:** repeated trials share state, data-dependent choices, or correlated failures.
23. **Wrong aggregation:** majority vote is used when success means any trial found a better witness, or vice versa.
24. **Requested-trial accounting:** cancelled, lost, duplicate, or unverified trials are counted in the deployed error bound.
25. **Expectation as deadline:** expected logarithmic or linear work becomes an unqualified latency promise.
26. **Tail censoring:** timed-out and failed runs are omitted from performance statistics.
27. **Adaptive-adversary gap:** a proof for fixed inputs is used after choices leak through timing or table behavior.
28. **Hash-family overclaim:** universal hashing is treated as collision resistance or as a worst-case bound for every sampled function.
29. **Multigraph sampling defect:** contraction samples endpoint pairs rather than edge copies, invalidating the survival probability.
30. **Lost contraction provenance:** supervertices no longer retain original membership, so the reported cut cannot be lifted.
31. **Redrawn persistent priorities:** recovery changes treap or skip-list structure and violates replicated-state expectations.
32. **Statistical-test proof:** passing a finite battery is treated as exact uniformity, independence, or cryptographic security.
33. **Multiple-testing blindness:** enough seeds and metrics are tried that an apparently significant anomaly or success is selected by chance.
34. **Fallback neglect:** the worst-case-safe path is so rarely exercised that it fails when the rare event occurs.
35. **Entropy failure concealment:** a platform randomness error silently falls back to a constant, clock, or weak generator.
36. **Probability without consequence:** a tiny numeric error rate is accepted without considering correlated scale, harm, or irreversible actions.

## Worked Examples

### Example 1

**Question:** A generator emits each integer in $\{0,\ldots,31\}$ uniformly. Compare direct modulo and rejection sampling for a draw below $6$.

**Reasoning:** Direct modulo gives residues $0$ and $1$ six preimages each, but residues $2,3,4,5$ only five. Thus their probabilities are $6/32$ and $5/32$, not $1/6$. Rejection uses

$$
L=\left\lfloor\frac{32}{6}\right\rfloor6=30.
$$

Accepting only $0$ through $29$ gives every residue five preimages. Rejection probability is $2/32=1/16$, acceptance probability is $15/16$, and expected words per result are $16/15$.

**Result:** Rejection produces an exact uniform bounded draw under the uniform-word premise; direct modulo is biased.

### Example 2

**Question:** Interpret the executable's randomized selection contract for values $(9,1,7,3,7,5)$ and zero-based rank $3$.

**Reasoning:** The deterministic oracle is

$$
(1,3,5,7,7,9).
$$

The first pivot is $3$, so ranks $0$ and $1$ fall below it and the requested rank moves into the higher partition as local rank $1$. Pivot $7$ then creates lower value $5$, equal identities at source indices $2$ and $4$, and higher value $9$. Local rank $1$ belongs to the equal group.

**Result:** The selected value is $7$ and the declared tie rule returns source index $2$. Random pivots change work, not rank correctness.

### Example 3

**Question:** For four distinct identities, what probability does a correct Fisher–Yates shuffle assign to output $(d,b,a,c)$?

**Reasoning:** Backward placement uniquely requires choosing $c$ for position $3$, then $a$ for position $2$, then $b$ for position $1$. The conditional choice probabilities are $1/4$, $1/3$, and $1/2$.

$$
\Pr[(d,b,a,c)]
=\frac14\frac13\frac12
=\frac1{24}.
$$

All $4!=24$ identity permutations have the same probability. If $a$ and $b$ held equal values, multiple identity permutations could render the same value sequence.

**Result:** Uniformity is over declared identities; observed value sequences need not each have probability $1/24$ when values repeat.

### Example 4

**Question:** A size-two reservoir processes identities $a,b,c,d,e$. What are the final subset and marginal probabilities?

**Reasoning:** The subset invariant makes each of the

$$
\binom52=10
$$

two-subsets have probability $1/10$. Each identity occurs in four of those subsets, so its marginal inclusion probability is $4/10=2/5$. Equivalently, an old item after four records has inclusion probability $2/4$ and survives the fifth step with probability $4/5$:

$$
\frac24\frac45=\frac25.
$$

**Result:** Equal marginals are consistent with, but do not alone prove, uniform subset sampling; the induction proof supplies the stronger contract.

### Example 5

**Question:** Recompute the expected comparison count for uniform-pivot quicksort on five distinct ranks and compare it with a degenerate pivot tape.

**Reasoning:** Since

$$
H_5=1+\frac12+\frac13+\frac14+\frac15=\frac{137}{60},
$$

the exact expectation is

$$
\mathbb E[C_5]
=2(6)\frac{137}{60}-20
=\frac{37}{5}
=7.4.
$$

A tape that repeatedly selects an extreme pivot performs

$$
4+3+2+1=10
$$

comparisons.

**Result:** $7.4$ is an expectation over tapes for any fixed distinct-key ordering under the model; it is not a per-run ceiling.

### Example 6

**Question:** Independent trials succeed with probability at least $1/4$. How many are required for aggregate failure at most $10^{-9}$ when any success suffices?

**Reasoning:** Solve

$$
\left(\frac34\right)^r\le10^{-9}.
$$

Thus

$$
r\ge
\left\lceil
\frac{\log(10^{-9})}{\log(3/4)}
\right\rceil
=73.
$$

The exact upper bound at $73$ trials is approximately $7.577\times10^{-10}$. The convenient exponential inequality gives the looser sufficient count

$$
\left\lceil\frac{\log(10^9)}{1/4}\right\rceil=83.
$$

**Result:** Both counts are valid under independence, but $73$ follows the exact per-trial bound and $83$ is conservative.

### Example 7

**Question:** A universal family maps ten fixed distinct keys to 64 buckets. Bound the expected number of colliding unordered key pairs.

**Reasoning:** There are

$$
\binom{10}{2}=45
$$

pairs, and each collides with probability at most $1/64$. Therefore

$$
\mathbb E[\text{colliding pairs}]
\le\frac{45}{64}
=0.703125.
$$

This does not say that every selected function has fewer than one collision, which would not even be a meaningful integer guarantee.

**Result:** The expectation is over the independently selected hash function for this fixed key set.

### Example 8

**Question:** Use the basic Karger lower bound for an eight-vertex graph. What does 100 independent trials guarantee for one fixed minimum cut?

**Reasoning:** One trial preserves that cut with probability at least

$$
p=\frac{2}{8\cdot7}=\frac1{28}.
$$

All 100 trials miss it with probability at most

$$
\left(\frac{27}{28}\right)^{100}
\approx0.02634.
$$

Hence the probability that at least one trial returns that cut is at least $0.97366$. The calculation assumes uniform multigraph-edge sampling and 100 distinct completed trial streams.

**Result:** The best verified cut is a high-probability answer under the trial theorem, not a deterministic optimality certificate.

### Example 9

**Question:** In the ideal skip-list model with promotion probability $p=1/2$ and $n=10^6$ nodes, bound the probability that some node reaches level $30$.

**Reasoning:** One node reaches level 30 with probability $2^{-30}$. A union bound gives

$$
\Pr[\text{some node reaches level }30]
\le\frac{10^6}{2^{30}}
\approx9.313\times10^{-4}.
$$

The expected number of promoted levels above the base for one node is

$$
\sum_{h\ge1}2^{-h}=1,
$$

so the expected number of level memberships including the base is $2$ per node.

**Result:** Expected space is linear, while height remains a tail event that must be governed separately.

### Example 10

**Question:** A distributed search requests 64 trials with success probability at least $0.1$, but four records duplicate earlier trial identities. Compare the claimed and justified failure bounds.

**Reasoning:** Treating all records as independent would publish

$$
0.9^{64}\approx0.001179.
$$

Only 60 distinct completed trials exist, so the justified bound is

$$
0.9^{60}\approx0.001797.
$$

If the duplicated streams are correlated with other streams too, even the latter calculation needs more evidence.

**Result:** Amplification is determined by the durable set of justified independent trials, not requested work or row count.

## Cross-Program Connections

- [Theory of Computation & Complexity](../../15-theory-of-computation-and-complexity/ROADMAP.md) owns probability models, randomized complexity classes, minimax lower-bound reasoning, derandomization, and formal error models.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) owns universal hashing, treaps, skip lists, randomized indexes, persistence, and adversarial operation sequences.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) owns sampling units, repeatable samples, approximate queries, snapshots, and distributed reservoir or priority aggregation.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) owns word operations, generator throughput, vectorization, counter-based execution, and memory contention.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns entropy-source assessment, deterministic random bit generators, secret-state handling, nonces, tokens, and adaptive attackers.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) owns logical stream identities, retries, speculative duplicates, global trial completion, and atomic publication.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns reference vectors, seed corpora, property tests, statistical diagnostics, failure injection, and reproducible incident evidence.

## References

1. Rajeev Motwani and Prabhakar Raghavan. [*Randomized Algorithms*](https://www.cambridge.org/core/books/randomized-algorithms/6A3E5CD760B0DDBA3794A100EE2843E8), Cambridge University Press, 1995; online edition 2013. Authoritative probability tools, randomized techniques, and applications.
2. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. [*Introduction to Algorithms*, fourth edition](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), MIT Press, 2022. Authoritative undergraduate treatment of randomized analysis, permutation, quicksort, selection, and hashing.
3. Andrew Chi-Chih Yao. [“Probabilistic Computations: Toward a Unified Measure of Complexity”](https://doi.org/10.1109/SFCS.1977.24), *18th Annual Symposium on Foundations of Computer Science*, 1977, pp. 222–227. Primary distinction and relationship between randomized and distributional complexity.
4. J. Lawrence Carter and Mark N. Wegman. [“Universal Classes of Hash Functions”](https://doi.org/10.1016/0022-0000(79)90044-8), *Journal of Computer and System Sciences* 18(2), 1979, pp. 143–154. Primary universal-hashing construction and fixed-input expected analysis.
5. Jeffrey Scott Vitter. [“Random Sampling with a Reservoir”](https://doi.org/10.1145/3147.3165), *ACM Transactions on Mathematical Software* 11(1), 1985, pp. 37–57. Primary reservoir-sampling algorithms and analysis.
6. David R. Karger. [“Global Min-cuts in RNC, and Other Ramifications of a Simple Min-Cut Algorithm”](https://people.csail.mit.edu/karger/Papers/mincut.pdf), *Fourth Annual ACM–SIAM Symposium on Discrete Algorithms*, 1993, pp. 21–30. Primary random-contraction algorithm and survival analysis.
7. Michael O. Rabin. [“Probabilistic Algorithm for Testing Primality”](https://doi.org/10.1016/0022-314X(80)90084-0), *Journal of Number Theory* 12(1), 1980, pp. 128–138. Primary practical one-sided probabilistic primality algorithm.
8. William Pugh. [“Skip Lists: A Probabilistic Alternative to Balanced Trees”](https://doi.org/10.1145/78973.78977), *Communications of the ACM* 33(6), 1990, pp. 668–676. Primary probabilistically balanced skip-list design.
9. Daniel Lemire. [“Fast Random Integer Generation in an Interval”](https://doi.org/10.1145/3230636), *ACM Transactions on Modeling and Computer Simulation* 29(1), 2019, article 3. Primary analysis and engineering of unbiased bounded integer generation.
10. Guy L. Steele Jr., Doug Lea, and Christine H. Flood. [“Fast Splittable Pseudorandom Number Generators”](https://doi.org/10.1145/2660193.2660195), *OOPSLA 2014*, pp. 453–472. Primary splittable-stream design for deterministic parallel computation.
11. Elaine Barker and John Kelsey. [*Recommendation for Random Number Generation Using Deterministic Random Bit Generators*, NIST SP 800-90A Revision 1](https://csrc.nist.gov/pubs/sp/800/90/a/r1/final), National Institute of Standards and Technology, 2015; consulted 2026-09-04. Official cryptographic deterministic-random-bit-generation guidance.
12. Donald Eastlake 3rd, Jeffrey Schiller, and Steve Crocker. [*Randomness Requirements for Security*, RFC 4086 / BCP 106](https://www.rfc-editor.org/info/rfc4086/), IETF, 2005. Official security guidance on entropy, unpredictability, and common failures.
13. ACM, IEEE Computer Society, and AAAI. [*Computer Science Curricula 2023: Algorithmic Foundations*](https://csed.acm.org/algorithms-and-complexity/), endorsed 2024; consulted 2026-09-04. Current curricular scope for randomized algorithms, analysis, correctness, and design strategies.

## Exercises

### Exercise 1

A device emits uniform bytes. Derive an exact uniform draw below $10$ using rejection. State the accepted interval, direct-modulo bias, rejection probability, and expected byte count per accepted draw. Explain what the calculation does and does not prove about the device.

### Exercise 2

Prove that a size-three reservoir after six distinct stream identities is uniform over all three-subsets. Compute the probability of one specified subset and one specified identity's inclusion. Then diagnose why taking three items from each of a 100-record shard and a 900-record shard and choosing three uniformly from the six candidates is not a uniform global sample.

### Exercise 3

Compute the exact expected comparison count for uniform-pivot quicksort on six distinct ranks and the comparison count for repeated extreme pivots. Identify where linearity of expectation is used and whether comparison indicators must be independent. State two implementation details that would require a different cost model.

### Exercise 4

A service runs 40 Monte Carlo trials, each advertised to fail with probability at most $0.2$. Ten workers are created by copying one initialized generator state; each worker performs four trials. The service publishes $0.2^{40}$ as its bound, logs only successful runs, and returns its best unverified candidate as exact after a timeout. Identify every contract defect and propose a defensible trial, status, evidence, and fallback design.

### Exercise 5

Transfer the module to this unfamiliar constraint: a daily audit must choose 200 account identities uniformly without replacement from $N$ distinct accounts split across uneven, changing shards. The selection must be reproducible from authorized audit metadata and invariant under worker scheduling and resharding; it is not security-secret. Design a random-priority solution, explain how local results merge, handle finite-priority collisions and $N<200$, state the proof and error contract, and define validation plus publication evidence.

## Answers to the Exercises

### Answer 1

A byte has domain size $M=256$. The largest multiple of $10$ at most $256$ is

$$
L=\left\lfloor\frac{256}{10}\right\rfloor10=250.
$$

Draw bytes until $X<250$, then return $X\bmod10$. Each residue has 25 accepted preimages, so the conditional distribution is uniform. Direct modulo over all 256 bytes gives residues $0,\ldots,5$ 26 preimages each and residues $6,\ldots,9$ 25 each.

The rejection probability is

$$
\frac{256-250}{256}
=\frac{3}{128},
$$

the acceptance probability is $125/128$, and the expected number of independent bytes is

$$
\frac{1}{125/128}=\frac{128}{125}=1.024.
$$

This proves the range mapping is exact if source bytes are independent and uniform. It does not prove that the device satisfies either premise, has enough entropy, resists state prediction, or is appropriate for security. Those are separate source and threat-model obligations.

### Answer 2

The reservoir subset induction establishes that after $t$ items every three-subset has probability $1/\binom t3$. At $t=3$ the only subset is certain. In the induction step, a target subset omitting the new item survives with probability $(t-2)/(t+1)$. A target subset containing the new item has $t-2$ possible predecessor subsets: add one old identity outside its two old members, then draw the one reservoir slot holding that added identity. Both cases simplify to $1/\binom{t+1}3$ as derived in the chapter.

At six items, one specified subset has probability

$$
\frac1{\binom63}
=\frac1{20}.
$$

A specified identity belongs to $\binom52=10$ of the 20 subsets, hence has inclusion probability $10/20=1/2=3/6$.

The naive shard merge first gives every shard three of six candidate positions. An identity in the 100-record shard reaches its local reservoir with probability $3/100$ and, by symmetry, survives the three-of-six second sample with probability $1/2$, for total probability $3/200$. An identity in the 900-record shard has probability

$$
\frac3{900}\frac12=\frac1{600}.
$$

They should all have global inclusion probability $3/1000$. The two-stage scheme therefore overweights each small-shard identity by a factor of five and underweights each large-shard identity. A correct merge must account for partition population, use mergeable random priorities, or run a proven weighted reservoir scheme.

### Answer 3

For six distinct ranks,

$$
H_6
=1+\frac12+\frac13+\frac14+\frac15+\frac16
=\frac{49}{20}.
$$

Therefore

$$
\mathbb E[C_6]
=2(6+1)H_6-4\cdot6
=14\frac{49}{20}-24
=\frac{103}{10}
=10.3.
$$

Repeated extreme pivots perform

$$
5+4+3+2+1=15
$$

comparisons. The expectation decomposes comparison count as $\sum_{i<j}X_{ij}$ and uses linearity to sum $\mathbb E[X_{ij}]$. The indicators do not need to be independent. A three-way duplicate partition changes the rank model, while median-of-three sampling adds pivot-selection comparisons and changes pivot probabilities. Cutoffs, fallback, swaps, recursion, branches, and memory traffic are further costs outside this exact comparison formula.

### Answer 4

Copying one initialized state makes the ten workers begin with identical streams. If their code and inputs align, the system may have only four distinct random tapes, repeated ten times. Different row or worker identifiers do not restore independence unless they enter a reviewed stream derivation. The $0.2^{40}$ product is therefore unjustified; even $0.2^4$ would require evidence that the four positions form independent trials under the theorem.

Logging only successes censors the observed failure and runtime distributions. Returning a best unverified candidate as exact changes Monte Carlo behavior into an undocumented correctness claim. A timeout is not evidence that the best seen candidate is optimal.

A defensible design derives each stream from a canonical `(job, algorithm version, trial id, purpose)` domain using a generator mechanism whose trial relationship supports the proof. It records 40 distinct terminal trial identities, verifies every candidate's feasibility, and applies the aggregation rule actually proved. If any successful trial suffices, the published failure bound is $0.2^{40}$ only after all 40 distinct trials complete under the assumptions. The result status remains probabilistic unless a deterministic optimality certificate exists.

Timeout returns inconclusive with the bound justified by the number of distinct completed trials, or invokes a predetermined correct deterministic fallback. Telemetry includes all trials, durations, failures, cancellations, verifier outcomes, duplicate ids, generator and derivation versions, input digest, and fallback behavior. Secret seed material would be excluded, though this particular nonsecurity service may retain an authorized replay seed.

### Answer 5

Assign every distinct account identity $u$ a priority

$$
P_s(u)
$$

derived from a root audit seed $s$, a canonical identity encoding, a fixed generator or pseudorandom-function version, and a domain label such as “daily-account-audit.” Under the ideal proof model, priorities are independent continuous uniform values. Select the 200 identities with smallest priorities.

Each shard needs to emit only its local 200 smallest `(priority, identity)` records. Any identity outside a shard's local 200 has at least 200 smaller priorities in that same shard and therefore cannot be in the global 200. Merging all local candidates and taking the global 200 is consequently exact. Because priority depends on logical identity and audit domain rather than shard or worker, scheduling, retries, and resharding do not change the result.

With distinct exchangeable continuous priorities, every ordering of the $N$ identities is equally likely, so every 200-subset has probability

$$
\frac1{\binom N{200}}.
$$

A finite $w$-bit priority can collide. A union bound makes the probability of any collision at most

$$
\frac{\binom N2}{2^w}
$$

when pair collision probability is $2^{-w}$. Deterministic identity tie breaking gives reproducibility but makes exact uniformity conditional on no collision. The design can publish this explicit Monte Carlo deviation bound, extend priorities with additional domain-separated words until they differ, or reject the entire seed and recompute after a global collision check. The latter two choices need their own termination and implementation proof. If $N<200$, return all $N$ identities and state the short-population status rather than duplicating records.

Validation compares bounded populations against exhaustive subset frequencies, verifies identity canonicalization and reference vectors, confirms local-to-global merge equivalence under many shardings, replays after scheduling and retry changes, injects priority collisions, and tests $N=0,199,200,201$. Publication binds the date and input snapshot digest, account-population rule, $N$, requested and actual sample sizes, seed reference, generator and derivation versions, priority width and collision policy, shard completion set, selected identity digest, verifier results, and exact or bounded-error status. Atomic publication occurs only after every shard for the snapshot is complete and the global merge validates.
