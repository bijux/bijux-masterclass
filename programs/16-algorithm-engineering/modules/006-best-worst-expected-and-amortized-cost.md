---
module_id: ALGE-006
program: Algorithm Engineering
level: 1
module_number: 6
title: Best, Worst, Expected, and Amortized Cost
status: complete
last_verified: 2026-09-04
---

# Best, Worst, Expected, and Amortized Cost

## One-Page Review

### Governing question

Which quantifier or probability space turns an operation count into a best-case, worst-case, average/expected, or amortized guarantee, and what can an engineer safely infer from each?

### Essential definitions

- **best-case cost** minimizes cost over admitted inputs of a fixed size; **worst-case cost** maximizes it.
- **average-case cost** is an expectation over an explicit input distribution, not an informal claim about “typical” data.
- **expected cost of a randomized algorithm** averages over declared internal random choices, often for each fixed input.
- A **tail bound** limits the probability that cost exceeds a threshold; expectation alone does not provide a hard latency bound.
- **amortized cost** bounds total actual cost across every admitted operation sequence and assigns that total across operations without requiring probability.
- **aggregate analysis** bounds an entire sequence directly; **accounting analysis** uses nonnegative saved credits; **potential analysis** represents saved work as a nonnegative function of state.
- **deamortization** changes an implementation so deferred work is spread across operations, trading simplicity or throughput for a stronger per-operation bound.
- An **adversary model** states what input/sequence chooser can know about random choices and state.

### Central model, mechanism, or theorem

For finite size class $I_n$ and cost $C(x,r)$ with random choice $r$,

$$
C_{best}(n)=\min_{x\in I_n}C(x),
\qquad
C_{worst}(n)=\max_{x\in I_n}C(x),
$$

while a randomized expected guarantee for each fixed input is

$$
\forall x\in I_n:\quad \mathbb{E}_{R}[C(x,R)]\le g(n).
$$

For states $D_0,D_1,\ldots,D_m$, actual costs $c_i$, and potential $\Phi(D)\ge0$, define

$$
\hat c_i=c_i+\Phi(D_i)-\Phi(D_{i-1}).
$$

Then

$$
\sum_{i=1}^{m}c_i
=\sum_{i=1}^{m}\hat c_i+\Phi(D_0)-\Phi(D_m)
\le\sum_{i=1}^{m}\hat c_i+\Phi(D_0).
$$

With $\Phi(D_0)=0$, bounded amortized charges bound every admitted sequence total.

### Critical invariants

- Define admitted inputs/states, size parameters, cost model, and operation before selecting a case label.
- Keep bound direction ($O,\Omega,\Theta$) separate from best/worst/expected/amortized quantifiers.
- Name the probability source: input distribution, algorithmic randomness, environment, or a declared combination.
- State whether an expected bound holds for each fixed input or only after averaging over inputs.
- Report tail probability or a hard bound when rare cost matters; a small mean can hide large spikes.
- Amortization covers operation sequences without assuming a random distribution and does not cap each operation.
- Credits/potential must pay every prefix or include an explicit initial balance; borrowing from future operations is invalid.
- A potential function belongs to the proof, need not be stored, and must have a justified lower bound.
- Persistent versions, rollback, copying, concurrency, and external mutation can invalidate a state-based amortized proof.
- Measurements estimate a concrete workload distribution; they do not establish a universal worst-case or amortized theorem.

### Common failures

Common failures include calling $O$ worst case and $\Omega$ best case; saying “average” without a distribution; averaging uniformly over values when production is skewed; confusing input randomness with algorithm randomness; applying linearity of expectation without defining random variables; turning expectation into a percentile promise; calling a rare resize constant-time; dividing one friendly trace by its length and calling it amortized; letting credits go negative; choosing a negative or unbounded-below potential; ignoring the initial/final potential; replaying persistent states to spend the same credits twice; and assuming an adversary cannot observe a supposedly secret random seed.

### Compact example

A doubling array performs one write on an ordinary append and copies $q$ existing elements when full at capacity $q$. The append that grows from $q$ to $2q$ costs $q+1=\Theta(q)$, so worst-case append is linear in current size. Across $n$ appends from empty, copied capacities form

$$
1+2+4+\cdots<2n,
$$

so total writes plus copies are below $3n$ and append is $\Theta(1)$ amortized. No probability is involved, and no constant per-append latency follows.

### Connections

[ALGE-005](./005-asymptotic-time-and-space.md) supplies size, cost, and growth notation. [ALGE-007](../ROADMAP.md) solves recursive cost equations, while ALGE-009 and ALGE-010 connect guarantees to machine models and measurement. [DSE-004](../../17-data-structures-engineering/modules/004-time-space-and-allocation-cost.md) applies amortized/resource contracts to data-structure implementations.

## Governing Question

The same algorithm can take one step on one input, a million on another, and a random number on repeated executions of a third. A stateful structure can make one operation expensive but keep every long sequence cheap. Which summary is being claimed, over what set or probability space, and what operational promise does it support?

There is no universally correct single “complexity” for such behavior. Best case describes an achievable lower extreme. Worst case supplies a robust per-input upper envelope. Average and expected costs depend on probability. Amortized cost describes the worst total over sequences while redistributing that total analytically. These are different mathematical objects, not alternative spellings for Big-O.

## Why This Matters

Choosing the wrong quantifier produces unsafe engineering. An expected constant-time map operation may have a linear collision case. An amortized constant append may pause to copy an entire buffer. A low mean may coexist with a damaging tail. Conversely, demanding a hard worst-case bound everywhere can reject a simpler design whose rare work is acceptable and whose sequence total is excellent.

Workloads are also policies. Uniform lookup keys, independent requests, stationary traffic, and secret random seeds are assumptions, not natural laws. Production skew, adaptive users, retries, shared caches, and adversarial inputs can change the probability space or operation sequence. Analysis must state who controls each variable and what they observe.

The goal is a portfolio of honest guarantees. Use worst-case bounds for hard limits and attack surfaces, expected or distributional analysis when a defensible probability model exists, amortized bounds for sequence throughput, and measurements for the concrete workload/environment. Their combination is stronger than relabeling one as another.

## Prerequisites and Retrieval

Retrieve:

- sets, finite minima/maxima, sequences, sums, inequalities, and induction;
- random variables, probability distributions, expectation, conditional probability, and linearity of expectation;
- asymptotic upper, lower, and tight bounds from ALGE-005;
- arrays, stacks, counters, hash tables, recursion, and mutable state;
- workload contracts, adversarial inputs, latency, throughput, and percentiles;
- loop and inductive correctness arguments from ALGE-003 and ALGE-004.

Be able to distinguish a deterministic input chosen before a random seed from an input chosen after observing prior outcomes. Recall that an expectation is defined only relative to a probability measure, while a universal bound quantifies over all admitted cases.

## Learning Objectives

After completing this module, you should be able to:

1. define best- and worst-case cost functions over fixed-size admitted inputs;
2. construct an average-case cost from an explicit input distribution;
3. state an expected randomized guarantee for every fixed input;
4. distinguish expectation, high-probability, quantile, and hard worst-case claims;
5. define amortized cost as a worst-sequence total rather than a probability average;
6. carry out aggregate, accounting, and potential-method analyses;
7. verify prefix-credit, initial-potential, and terminal-potential conditions;
8. identify persistence, rollback, concurrency, and adversary assumptions that break an amortized or randomized proof;
9. decide when deamortization or a hard capacity policy is required;
10. combine theorem-level guarantees with distribution and measurement evidence without overclaiming.

## Core Exposition

### Start from a cost random variable or deterministic function

Let $I_n$ be admitted inputs of size $n$, let $R$ represent internal randomness, and let $C(x,r)$ be a nonnegative cost under a declared model. A deterministic algorithm is the special case in which $r$ is absent. Before summarizing, decide which variables are fixed, maximized, averaged, or sequenced.

This order matters. The expressions

$$
\max_x\mathbb{E}_R[C(x,R)]
\quad\text{and}\quad
\mathbb{E}_R\left[\max_x C(x,R)\right]
$$

need not be equal. In the first, one input is fixed before randomness; in the second, the maximizing input may depend on the realized random choice. The latter can model a stronger observer/adversary.

### Best and worst case are extrema over a domain

For nonempty finite $I_n$, define

$$
C_{best}(n)=\min_{x\in I_n}C(x),
\qquad
C_{worst}(n)=\max_{x\in I_n}C(x).
$$

For linear search on a nonempty sequence, a target at the first position gives one comparison; an absent target or a match at the last position gives $n$ comparisons under the simple comparison model. Thus successful best case is $\Theta(1)$ and overall worst case is $\Theta(n)$.

Best case is useful for fast-path design and lower-envelope understanding, but it rarely supports capacity or latency guarantees. Worst case is robust to unknown input distributions but may be unattainable or irrelevant under a validated domain restriction. Both depend on what inputs and outcomes the contract admits.

The asymptotic symbol does not choose the case. One may prove $C_{worst}\in O(n)$, $C_{worst}\in\Omega(n)$, and therefore $C_{worst}\in\Theta(n)$. Saying “Omega is the best case” confuses the input quantifier with bound direction.

### Average case requires an input distribution

Let $X_n$ be a random input drawn from probability distribution $D_n$ over $I_n$. The average-case cost is

$$
C_{avg}(n)=\mathbb{E}_{X_n\sim D_n}[C(X_n)].
$$

For successful linear search with the target uniformly distributed among $n$ positions, expected comparisons are

$$
\frac{1}{n}\sum_{i=1}^{n}i=\frac{n+1}{2}=\Theta(n).
$$

Uniformity is the model, not a default. If the first position receives probability $0.9$ and the remaining probability is spread across later positions, the expectation can be much smaller while the worst case remains $n$. If absence is possible, its probability and cost belong in the sum.

Average-case analysis can be powerful when the distribution follows a validated generative process or stable product behavior. It is fragile when traffic drifts, keys correlate, users adapt, or the chosen distribution was selected for analytical convenience. Report sensitivity to plausible alternatives.

### Randomized expected cost can hold for each fixed input

A randomized algorithm deliberately draws $R$. A strong expected-time statement has the form

$$
\forall x\in I_n:\quad \mathbb{E}_{R}[C(x,R)]\le g(n).
$$

No random-input assumption is required: the adversary may choose any fixed $x$ before the private random choices occur. Randomized quicksort with appropriate independent pivot selection is analyzed in this style. The output-correctness claim must separately say whether the algorithm is always correct (Las Vegas) or may err with bounded probability (Monte Carlo), developed in ALGE-068.

An implementation must actually supply randomness satisfying the model. Reused or predictable seeds, biased sampling, modulo bias, shared-state races, and an adaptive observer can invalidate a proof premise. The cost of producing randomness can also belong to the model.

### Mixed randomness needs explicit conditioning

Inputs and the algorithm may both be random. A joint expectation can be expanded as

$$
\mathbb{E}_{X,R}[C(X,R)]
=\mathbb{E}_{X}\left[\mathbb{E}_{R}[C(X,R)\mid X]\right].
$$

If the inner bound is at most $g(n)$ for every fixed $X=x$, then the joint expectation is also at most $g(n)$ for any input distribution. The reverse does not follow: a good joint average may hide a small class of inputs with terrible conditional expected cost.

Linearity of expectation,

$$
\mathbb{E}\left[\sum_i Y_i\right]=\sum_i\mathbb{E}[Y_i],
$$

does not require independence when expectations exist. Independence may be needed for products, concentration, or conditional steps. Define indicator variables and probability spaces rather than invoking “randomness” as an informal explanation.

### Expectation does not control the tail by itself

Let cost be $n^2$ with probability $1/n$ and $1$ otherwise. Its expectation is

$$
\mathbb{E}[C]
=\frac{1}{n}n^2+\left(1-\frac{1}{n}\right)
=n+1-\frac{1}{n}
=\Theta(n),
$$

yet a quadratic event still occurs with probability $1/n$. For large request volumes, such events may be operationally routine.

A high-probability statement gives a threshold and failure function, for example

$$
\Pr[C(x,R)>g(n)]\le\delta(n)
$$

for every admitted $x$. A quantile measurement estimates a distribution in one environment. A deterministic worst-case bound rules out higher modeled cost entirely. These evidence strengths are not interchangeable.

For $a>0$, Markov's inequality gives $\Pr[C\ge a]\le\mathbb{E}[C]/a$ for nonnegative $C$, but it can be loose. Strong tail guarantees usually require more structure, such as bounded differences or independent trials. State which theorem and premises produce the tail.

### Amortized analysis quantifies over sequences, not probability

Let an initial valid state $D_0$ receive an admitted sequence $\sigma=(o_1,\ldots,o_m)$. Let actual costs be $c_i$. An amortized upper bound assigns charges $\hat c_i$ such that

$$
\forall\sigma:\quad
\sum_{i=1}^{m}c_i
\le
\sum_{i=1}^{m}\hat c_i+B_0,
$$

where $B_0$ is an explicit initial credit if needed. The sequence can be adversarial. “Average per operation” here means the worst-sequence total divided across operations, not an expectation over random traces.

One operation may remain expensive. If a dynamic-array append triggers a copy of $n$ elements, its actual cost is $\Theta(n)$ even though append has $\Theta(1)$ amortized cost from empty. Throughput-oriented clients may accept this; hard-deadline clients may not.

### Aggregate analysis bounds total participation

Aggregate analysis derives a sequence total directly. A stack supporting `push`, `pop`, and `multipop(k)` may pop many elements in one call, but each pushed element can be removed at most once before being pushed again. Across $m$ operations, total successful pushes and pops are $O(m)$ under the usual cost model, so amortized cost per operation is $O(1)$.

For a doubling array, resizes copy capacities $1,2,4,\ldots$ below the final size scale. Across $n$ appends from empty, total copies are less than $2n$, and writes equal $n$, so total modeled work is less than $3n$. This is a guarantee for every prefix of the sole append sequence, not a measured average.

### Accounting analysis stores nonnegative credits

The accounting method overcharges some operations and assigns credits to objects or state. Credits later pay expensive work. Its invariant is that every prefix has a nonnegative balance and that credits are spent at most once.

For a binary counter, charge two units when a bit changes from $0$ to $1$: one pays that flip and one is stored on the bit to pay its later $1$-to-$0$ flip. Every increment may flip many trailing ones, but those flips are prepaid. Total charge is at most two per introduced $1$ flip, yielding constant amortized bit changes.

Credits are proof artifacts unless an implementation explicitly records them. Allowing a negative balance means borrowing from future operations; a sequence that stops at the debt point violates the bound. Persistent snapshots can duplicate logical access to a credited state, so a proof for destructive updates may not transfer.

### Potential analysis generalizes stored work

Choose a potential $\Phi(D)$ over valid states. Define

$$
\hat c_i=c_i+\Phi(D_i)-\Phi(D_{i-1}).
$$

Summing telescopes:

$$
\sum_{i=1}^{m}\hat c_i
=\sum_{i=1}^{m}c_i+\Phi(D_m)-\Phi(D_0).
$$

If $\Phi(D)\ge0$ and $\Phi(D_0)=0$, actual total cost is at most total amortized charge. More generally, retain the initial and terminal terms. A potential may be shifted by a constant without changing individual differences, but its lower-bound/initial accounting must remain valid.

For an append-only doubling table with size $s$ and capacity $q$, one convenient potential after initialization is

$$
\Phi=2s-q.
$$

Between resizes, one write increases potential by $2$, so actual one plus potential change is $3$. When a full table of size/capacity $q\ge1$ grows and appends, actual cost is $q+1$, while potential changes from $q$ to $2$, giving amortized cost $3$. The first insertion is a small base case. Potential accumulated during cheap appends pays for copying.

### Select a method that exposes the invariant

Aggregate analysis is simplest when total object participation or a geometric sum is apparent. Accounting is intuitive when work can be prepaid per object. Potential is algebraically flexible when operations transform global state or have different amortized charges. The methods can establish equivalent totals, but a poor credit scheme or potential may fail even when a good amortized bound exists.

The proof must cover every operation type and valid transition, not a representative trace. It must include initialization, clear/reset, growth and shrink, errors, failed allocation, cancellation, and destruction if those paths affect stored work. If the public operation can stop midway, define whether state and credits roll back together.

### Initial state, persistence, and concurrency change the theorem

“Starting empty” is an assumption. If a client begins from an arbitrary valid state with stored deferred work, include $\Phi(D_0)$ or prove a bound for that state. If a structure is persisted and reopened, analytical credit must follow the durable state or the restart theorem must pay reconstruction.

Persistent data structures permit access to old versions. An analysis that destroys an expensive configuration after charging it once may fail if many versions retain that configuration and repeat the cost. Copying a state cannot copy free analytical money unless the theorem accounts for branching histories.

Concurrent operations complicate linearization, interference, helping, retries, and ownership of potential. A sequential state transition proof does not automatically bound contended executions. Define whether cost is per operation, thread, successful commit, attempt, or global schedule and what scheduler/adversary is allowed.

### Deamortization strengthens per-operation behavior

If a linear resize pause is unacceptable, allocate the new table and migrate a bounded number of entries on each later operation while reads consult both tables. This can turn a large spike into incremental work, but adds representation states, lookup branches, memory coexistence, failure recovery, and correctness invariants.

Other options include fixed capacity with explicit rejection, segmented growth, background work with a liveness budget, or a structure with a stronger worst-case bound. Deamortization is an algorithm design change, not a relabeling of the amortized theorem.

### Measurements estimate workload behavior, not quantifiers you did not test

Empirical means and percentiles describe the sampled implementation, workload, time window, and environment. A benchmark with uniformly random keys does not validate production skew. A long trace can expose resize or compaction spikes but cannot prove every operation sequence total. Conversely, a worst-case proof may be too coarse to predict observed latency.

Record raw distributions by operation class and state age. Include warm-up, resize/rehash/collection phases, misses and hits, cancellations, retries, and adversarial candidates. Use proof to state robust envelopes and measurement to determine constants and frequency under the real workload.

### Executable evidence checks one amortized model

The following exact counter models append cost as one element write plus one cost for each element copied during doubling. It reports a 16-append trace and verifies the potential identity and a charge of at most three for every transition.

<!-- bijux-verify: {"id":"doubling-array-amortized-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"costs=1,2,3,1,5,1,1,1,9,1,1,1,1,1,1,1\ntotal=31\nworst_single=9\nactual_average=1.9375\namortized_total=47\nfinal_potential=16\nidentity=True\ncharge_bound=True\n","stderr":""}} -->
```python
size = 0
capacity = 0
potential = 0
costs = []
amortized = []

for _ in range(16):
    before = potential
    if size == capacity:
        copied = size
        capacity = 1 if capacity == 0 else 2 * capacity
    else:
        copied = 0
    size += 1
    actual = copied + 1
    potential = 2 * size - capacity
    charge = actual + potential - before
    costs.append(actual)
    amortized.append(charge)

print("costs=" + ",".join(map(str, costs)))
print(f"total={sum(costs)}")
print(f"worst_single={max(costs)}")
print(f"actual_average={sum(costs) / len(costs):.4f}")
print(f"amortized_total={sum(amortized)}")
print(f"final_potential={potential}")
print(f"identity={sum(costs) == sum(amortized) - potential}")
print(f"charge_bound={all(charge <= 3 for charge in amortized)}")
```

This is executable evidence for a small abstract counter, not a measurement of Python list growth. The proof covers arbitrary append prefixes under the declared doubling model; a real container needs its documented growth, allocation, failure, and concurrency behavior verified.

## Definitions and Notation

- $I_n$: admitted inputs/states of size $n$.
- $C(x,r)$: nonnegative modeled cost on input $x$ and random choice $r$.
- $D_n$: declared distribution over $I_n$.
- $R$: internal random variable or random bit stream.
- $C_{best},C_{worst}$: extrema over a fixed-size domain.
- $C_{avg}=\mathbb{E}_{X\sim D_n}[C(X)]$: distributional average cost.
- $\mathbb{E}_R[C(x,R)]$: randomized expected cost for fixed input $x$.
- $\delta(n)$: tail failure probability attached to a threshold.
- $\sigma=(o_1,\ldots,o_m)$: admitted operation sequence.
- $c_i$: actual cost of operation $i$; $\hat c_i$: its analytical amortized charge.
- $\Phi(D)$: potential assigned to valid state $D$.
- **prefix solvency:** accumulated charge/credit pays actual work after every prefix.
- **deamortization:** redesign that schedules deferred work to strengthen individual-operation bounds.

For mixed random inputs and choices, conditional expectation makes quantifier order visible. For stateful randomized structures, a complete claim may take a form such as

$$
\sup_{\sigma\in\mathcal{S}_m}
\mathbb{E}_{R}[C(\sigma,R)]\le G(m),
$$

where $\mathcal{S}_m$ and the adversary's access to prior randomness/outcomes must be defined.

## Mechanisms, Invariants, or Proof Structure

Use this cost-quantifier worksheet:

1. **Domain:** state valid inputs, states, operation sequences, and size parameters.
2. **Primitive cost:** define what is counted and what operations/failures are included.
3. **Controlled variables:** identify input, random bits, state history, scheduler, and environment.
4. **Quantifier order:** write which variables are fixed, maximized, averaged, or conditioned upon.
5. **Case function:** define best, worst, input-average, randomized expected, tail, or sequence total explicitly.
6. **Asymptotic bound:** apply $O,\Omega,\Theta$ only after the function is defined.
7. **Distribution evidence:** justify input/randomness assumptions and analyze sensitivity or drift.
8. **Tail evidence:** derive a probability bound or state that only expectation is known.
9. **Amortized invariant:** choose aggregate participation, prefix-solvent credits, or bounded-below potential.
10. **Telescoping:** retain initial and final credit/potential terms and cover every transition.
11. **Operational gap:** assess spikes, deadlines, memory peaks, persistence, rollback, and concurrency.
12. **Concrete validation:** test correctness, exact counters, hostile sequences, random-source behavior, and measured distributions separately.

To refute a claimed worst-case bound, one admitted input family suffices. To refute an average claim, show its distribution is missing or compute expectation under the stated distribution. To refute an amortized proof, find an admitted sequence/prefix whose actual work exceeds available charge, or a state transition for which the potential calculation fails.

## Alternatives and Trade-Offs

**Worst-case versus expected bounds.** Worst case is robust and supports hard resource planning but may be conservative. Expected bounds can justify simpler/faster algorithms when randomness assumptions are enforceable; they need tail and adversary analysis for consequence-sensitive use.

**Distributional average versus workload measurement.** A mathematical distribution enables derivation and sensitivity analysis. Measurement observes a concrete evolving workload but includes sampling error and system effects. Use measurements to validate, revise, and parameterize—not silently define—the model.

**Amortized versus per-operation worst case.** Amortization gives strong sequence throughput without probability. Per-operation bounds protect latency. Incremental work, fixed capacity, or another representation can buy a stronger individual bound at added complexity or average cost.

**Aggregate versus accounting versus potential.** Aggregate proofs are concise for globally countable events. Accounting explains object-local prepayment. Potential handles interdependent state. Prefer the simplest invariant that covers every transition and remains valid across the API lifecycle.

**Private randomness versus deterministic behavior.** Randomization can prevent fixed pathological inputs and simplify expected analysis. Determinism supports reproducibility and removes random-source assumptions. Public/predictable randomness may offer neither adversarial robustness nor stable repetition.

**Tail bound versus empirical percentile.** A theorem can cover all modeled inputs/random choices with stated probability. A percentile estimates one sampled distribution/environment. Both matter, but neither should borrow the other's scope.

## Failure Modes and Misconceptions

1. **“Big-O is worst case.”** Big-O bounds any defined function; worst case is a separate maximum.
2. **“Omega is best case.”** Omega is a lower bound and can apply to a worst-case function.
3. **“Average means typical.”** An expectation needs a named probability distribution.
4. **“Uniform input is neutral.”** Uniformity is a substantive workload assumption.
5. **“Expected randomized time assumes random inputs.”** A guarantee can hold for every fixed input over private internal randomness.
6. **“Linearity of expectation needs independence.”** It does not; concentration or products often do.
7. **“Expected time is a deadline.”** Rare large costs may coexist with a small mean.
8. **“A p99 measurement is a probability theorem.”** It estimates a particular sampled population and method.
9. **“Amortized means average input.”** It bounds worst-sequence totals without a distribution.
10. **“Amortized constant means each operation is constant.”** Individual spikes can be linear or worse.
11. **“One cheap trace proves amortization.”** Every admitted sequence and prefix must be covered.
12. **“Credits may go negative temporarily.”** Then a sequence ending at that prefix is unpaid.
13. **“Any potential function works.”** It needs correct transition algebra and a justified lower/initial bound.
14. **“Final potential can be ignored.”** Telescoping terms determine the actual-cost inequality.
15. **“Proof credits are stored metadata.”** They are analytical unless explicitly implemented.
16. **“Persistence preserves destructive amortization.”** Old versions may repeat work previously paid once.
17. **“Sequential amortization covers contention.”** Retries and interference require a schedule-aware theorem.
18. **“Deamortization is documentation.”** It is an implementation/algorithm redesign with new invariants.

## Worked Examples

### Example 1

**Question:** What are linear search's best and worst comparison costs on nonempty length-$n$ input?

**Reasoning:** A first-position match costs one comparison. An absent target or last-position match costs $n$. Under the simple sequential comparison model, best cost is $1=\Theta(1)$ and worst cost is $n=\Theta(n)$.

**Conclusion:** Extrema depend on admitted match/absence cases, not on asymptotic symbols.

### Example 2

**Question:** What is average successful linear-search cost under uniform target position?

**Reasoning:** Position $i$ costs $i$ comparisons and has probability $1/n$. Therefore $\mathbb{E}[C]=(1/n)\sum_{i=1}^{n}i=(n+1)/2=\Theta(n)$.

**Conclusion:** The expectation is linear and conditional on the uniform-success distribution.

### Example 3

**Question:** If 90% of searches hit the first position, is the average still $(n+1)/2$?

**Reasoning:** No. The distribution changed. If the remaining 10% are uniform over positions $2$ through $n$, expectation is $0.9+0.1((n+2)/2)$, still asymptotically linear but with a very different finite coefficient. Absence would add its own $n$-comparison probability term.

**Conclusion:** Workload probabilities determine average cost and must be preserved.

### Example 4

**Question:** What does expected randomized quicksort time claim about an adversarially ordered array?

**Reasoning:** With pivots sampled according to the proof model after the fixed input is chosen, the expectation is over pivot choices for that exact array. It does not require a random permutation. Predictable or manipulable choices can change the adversary model and invalidate the implementation correspondence.

**Conclusion:** Algorithmic randomness can provide a per-fixed-input expectation.

### Example 5

**Question:** Can $\mathbb{E}[C]=\Theta(n)$ coexist with $C=n^2$?

**Reasoning:** Yes. Let $C=n^2$ with probability $1/n$ and $1$ otherwise. Then expectation is $n+1-1/n$, but the quadratic event probability is nonzero and may matter across many requests.

**Conclusion:** Expected growth does not state a hard or percentile bound.

### Example 6

**Question:** Why is a stack `multipop(k)` operation constant amortized even though one call can be linear?

**Reasoning:** Across any operation sequence, each item can be popped only after a push and at most once before another push. Charging constant work to its push and eventual pop bounds total element operations by a constant multiple of sequence length.

**Conclusion:** Aggregate participation yields a universal sequence bound, not a per-call cap.

### Example 7

**Question:** How does $\Phi=2s-q$ pay for doubling-array copies?

**Reasoning:** Cheap appends increase potential by two and have charge three. At a resize from full capacity $q$, copying plus writing costs $q+1$, but potential drops from $q$ to $2$, so charge is $3$ for $q\ge1$. Stored potential pays the copy.

**Conclusion:** Potential converts irregular actual costs into bounded amortized charges.

### Example 8

**Question:** Why is a credit scheme invalid if it becomes negative before the next cheap operation?

**Reasoning:** The client may stop at the indebted prefix. Actual work then exceeds charges collected so far; future repayment is not guaranteed by the sequence theorem.

**Conclusion:** Prefix solvency is the accounting invariant.

### Example 9

**Question:** Does an expected constant-probe hash lookup protect against an adaptive remote client?

**Reasoning:** Only if hashing, seed secrecy/renewal, key processing, load control, and the adversary's observations match the proof. A client that learns collision behavior or exploits deterministic hashing can concentrate work; key-byte cost may also be nonconstant.

**Conclusion:** Expected guarantees are conditional on randomness and adversary models.

### Example 10

**Question:** A datastore compacts every million writes. Is “amortized constant write” enough for a latency SLO?

**Reasoning:** No. The sequence total may be linear while one compaction stalls writes, doubles live storage, fails, or is replayed after crash. Analyze per-write tail/worst case, background bandwidth, backpressure, crash recovery, durable progress, and space coexistence; deamortize or isolate compaction if the deadline requires it.

**Conclusion:** Amortized throughput and operational latency/recovery are separate contracts.

## Cross-Program Connections

- [Theory of Computation & Complexity](../../15-theory-of-computation-and-complexity/ROADMAP.md) supplies formal resource classes, randomized computation, probability amplification, and problem-level bounds.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) owns concrete growth, rebalancing, hashing, persistence, and allocation behavior.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies adaptive adversaries, complexity attacks, entropy, and denial-of-service analysis.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) treats retries, compaction, coordination, and scheduler/failure effects across histories.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) turns latency, throughput, capacity, and background work into service contracts.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies distribution-aware, adversarial, and reproducible performance evidence.

## References

1. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. [*Introduction to Algorithms*, fourth edition](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), MIT Press, 2022. Probabilistic analysis, randomized algorithms, and aggregate/accounting/potential amortization.
2. Robert E. Tarjan. [“Amortized Computational Complexity”](https://doi.org/10.1137/0606031), *SIAM Journal on Algebraic and Discrete Methods* 6(2), 1985, pp. 306–318. Primary survey and formal development of amortized complexity.
3. MIT OpenCourseWare 6.046J. [“Lecture 11: Amortized Analysis”](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2012/resources/mit6_046js12_lec11/), 2012. Aggregate, accounting, and potential methods with sequence quantifiers.
4. Rajeev Motwani and Prabhakar Raghavan. [*Randomized Algorithms*](https://www.cambridge.org/core/books/randomized-algorithms/6A3E5CD760B0DDBA3794A100EE2843E8), Cambridge University Press, 1995; online 2013. Probability tools and fixed-input analysis of randomized algorithms.
5. Michael Mitzenmacher and Eli Upfal. [*Probability and Computing*, second edition](https://assets.cambridge.org/97811071/54889/frontmatter/9781107154889_frontmatter.pdf). Cambridge University Press, 2017. Randomized algorithms, tail bounds, balls-and-bins, hashing, and probabilistic analysis.
6. Daniel D. Sleator and Robert E. Tarjan. [“Self-Adjusting Heaps”](https://doi.org/10.1137/0215004), *SIAM Journal on Computing* 15(1), 1986, pp. 52–69. Amortized complexity and self-adjusting structures under operation sequences.
7. ACM, IEEE Computer Society, and AAAI. [*Computer Science Curricula 2023: Algorithmic Foundations*](https://csed.acm.org/al-cs-core/), endorsed 2024; consulted 2026-09-04. Current curricular scope for best, average, worst, randomized, and amortized analysis.

## Exercises

### Exercise 1

Define best-case, worst-case, input-average, randomized expected, and amortized cost using explicit sets, distributions, random variables, or operation sequences. State why none is a synonym for $O$.

### Exercise 2

Linear search costs $i$ comparisons for a successful target at position $i$ and $n$ for absence. If absence has probability $q$ and, conditional on presence, the target position is uniform, derive expected comparisons and inspect $q=0$, $q=1$, and fixed $0<q<1$.

### Exercise 3

Prove an append-only doubling array has constant amortized copy-and-write cost by both aggregate and potential methods. Include the first insertion, an arbitrary prefix length, the potential's lower bound, and the fact that one append remains linear.

### Exercise 4

Compare a deterministic dictionary with $O(\log n)$ worst-case lookup and a randomized dictionary with $O(1)$ expected lookup but $O(n)$ worst case. Specify what must be known about keys, randomization, adversaries, tails, memory, and deadlines before choosing.

### Exercise 5

Design an analysis and evidence plan for an unfamiliar stateful service that accepts cheap updates, periodically rebuilds a derived index, persists snapshots, permits rollback, and serves concurrent reads. State candidate amortized theorem, invalidating histories, per-operation risks, deamortization options, and validation evidence.

## Answers to the Exercises

### Answer 1

For cost $C(x)$ on nonempty fixed-size domain $I_n$, best and worst are $\min_{x\in I_n}C(x)$ and $\max_{x\in I_n}C(x)$. Given input distribution $D_n$, average is $\mathbb{E}_{X\sim D_n}[C(X)]$. For randomized cost $C(x,R)$, a robust fixed-input expected claim is $\forall x\in I_n:\mathbb{E}_R[C(x,R)]\le g(n)$. Amortized analysis bounds $\sum_i c_i$ for every admitted operation sequence using aggregate work, solvent charges, or potential.

$O$ is an eventual upper-bound relation applied after one of these functions/totals is defined. Each case function can have $O$, $\Omega$, or $\Theta$ bounds, so the symbols cannot select the quantifier.

### Answer 2

Conditional on presence, expected comparisons are $(n+1)/2$. Therefore

$$
\mathbb{E}[C]
=qn+(1-q)\frac{n+1}{2}.
$$

At $q=0$, this is $(n+1)/2$; at $q=1$, it is $n$. For any fixed $0<q<1$, it remains $\Theta(n)$ with coefficient $(1+q)/2$ on the leading term. If $q$ varies with $n$, retain it rather than treating it as a constant. The derivation assumes uniform successful position and simple comparison cost; skew or early filters change the distribution/model.

### Answer 3

For $n$ appends from empty, each append writes once. Completed resizes copy capacities $1,2,4,\ldots,2^k<n$; their geometric sum is $2^{k+1}-1<2n$. Thus writes plus copies are below $3n$ and are $O(n)$, while $n$ writes give $\Omega(n)$, so amortized work is $\Theta(1)$ per append. The append at a full size $q$ still costs $q+1=\Theta(q)$.

For potential, set $\Phi(0,0)=0$ and after insertion use $\Phi(s,q)=2s-q$. The representation maintained by doubling gives $\Phi\ge0$. The first insertion costs one and moves potential to one, for charge two. A no-resize append has actual cost one and potential change two, for charge three. A resize from $s=q\ge1$ copies $q$, writes once, and changes potential from $q$ to $2$, again charge three. Telescoping yields actual total at most $3n$ because initial potential is zero and final potential is nonnegative.

### Answer 4

The deterministic design supplies a logarithmic model-relative upper bound for every admitted key/state. The randomized design supplies a smaller expectation only under its hashing/randomness/adversary assumptions and still permits linear cost. Determine key-byte lengths and comparison/hash costs, input skew and collision control, whether seeds are secret and independently generated, what an adaptive caller can observe, rehash/load policies, high-probability or tail bounds, memory overhead, mutation/concurrency behavior, and failure recovery.

For a hard deadline or hostile public boundary, worst-case protection, quotas, collision-resistant hashing, or a fallback may outweigh expected speed. For a controlled internal workload with enforceable randomness and measured tails, the randomized design may be preferable. Validate functional equivalence, hostile collisions, seed failures, resize spikes, latency distributions, and peak memory on the target implementation; do not turn benchmark averages into a universal guarantee.

### Answer 5

Model state as base data, derived-index generation, rebuild cursor, durable snapshot lineage, and concurrent read/update versions. A candidate theorem might bound total rebuild work by charging each accepted mutation enough to process its contribution once, under a single forward history, bounded mutation size, successful incremental progress, and reclamation of superseded generations. A potential can count remaining migration work plus newly accumulated changes, with explicit initial/restart potential.

Rollback, snapshot branching, replay after crash, repeated failed rebuilds, duplicated versions, reader pinning, cancellation, and an update rate above rebuild capacity can spend work more than once or prevent potential from falling. Concurrent retries/helping require a schedule-aware cost owner and linearization theorem. Individual rebuild steps can also create latency and old/new-index memory peaks even when total work is amortized.

Options include incremental bounded migration per update/read, a fixed rebuild budget with backpressure, immutable generation swaps, checkpointed cursor progress, rate/capacity limits, background isolation, or a structure with stronger update bounds. Evidence should include exact state-transition tests, crash/restart and rollback histories, snapshot branching, slow-reader reclamation, concurrent stress/model checking, adversarial update rates, bounded-work assertions, peak-space and tail-latency measurement, and reconciliation against an independently rebuilt index. The handoff must state whether the theorem covers throughput only or also individual deadlines and recovery.
