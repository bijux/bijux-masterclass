---
module_id: ALGE-068
program: Algorithm Engineering
level: 2
module_number: 68
title: Monte Carlo and Las Vegas Algorithms
status: complete
last_verified: 2026-09-05
---

# Monte Carlo and Las Vegas Algorithms

## One-Page Review

### Governing question

When an algorithm uses randomness, which quantity is allowed to vary—answer correctness, running time, or both—and how can its error, termination, independence, composition, and operational evidence be stated precisely?

### Essential definitions

- A **Monte Carlo algorithm** has a declared resource bound but may return an incorrect answer with bounded probability.
- A **Las Vegas algorithm** returns only correct answers, while its running time or number of attempts is random; the claimed expectation requires a termination premise.
- A **one-sided-error** decision algorithm can err on only yes-instances or only no-instances; a **two-sided-error** algorithm can err on both.
- A **witness** is evidence that a deterministic verifier can check; finding a witness can turn random candidate generation into a zero-error retry loop.
- **Amplification** combines repetitions to reduce error. Product bounds require fresh independence or a suitable conditional bound.
- An **error budget** allocates an allowed probability of incorrect output across calls, stages, tenants, and time.
- A **randomness transcript** records generator identity, version, seed or draws, and input snapshot sufficiently for replay.
- **Oblivious input** is fixed independently of private random choices; an adaptive adversary may choose later inputs after observing prior behavior.

### Central model, mechanism, or theorem

Freivalds' matrix-product verifier checks whether $AB=C$ by sampling $r$ uniformly from $\{0,1\}^n$ and testing $A(Br)=Cr$. If $AB=C$, it always accepts. If $D=AB-C\ne0$, select a nonzero row of $D$ and a nonzero coefficient in that row. After all other bits are fixed, at most one of the two choices for that bit can make the row's dot product zero. Thus an incorrect product is accepted with probability at most $1/2$.

With $k$ fresh independent vectors, false acceptance is at most $2^{-k}$. Reusing one vector $k$ times leaves the bound at $1/2$; repeated computation is not repeated evidence.

For a Las Vegas retry loop whose independent attempts succeed with probability at least $p>0$, attempts $T$ satisfy

$$
\mathbb E[T]\le\frac1p,
\qquad
\Pr[T>t]\le(1-p)^t.
$$

Correctness comes from the verifier; the probability premise controls time.

### Critical invariants

- The input domain, output relation, and meaning of error are fixed before probability is discussed.
- Every returned Las Vegas answer passes a sound deterministic verifier or follows an always-correct construction.
- One-sided claims identify exactly which output can be wrong.
- Random choices have the distribution and conditional independence used by the proof.
- Amplification combines outcomes using the proved rule: all, any, majority, or verified retry.
- Error budgets account for the number of opportunities for failure, including retries and service lifetime.
- Timeouts, cancellation, `unknown`, and partial results are part of the public output contract.
- Seeds enable replay but do not by themselves establish uniformity, independence, secrecy, or correctness.

### Common failures

Common failures include calling every randomized heuristic Monte Carlo; calling a retry loop Las Vegas without a sound verifier; swapping false-positive and false-negative directions; multiplying error probabilities for correlated repetitions; using the same seed and input for every round; selecting a repetition count without accounting for total calls; reporting “with high probability” without a parameter; converting a timed-out Las Vegas run into an unchecked answer; hiding `unknown` as a negative result; using public predictable randomness against adaptive clients; accepting arithmetic overflow in a supposedly exact verifier; and treating successful tests as proof of the promised distribution.

### Compact example

An incorrect matrix product passes one Freivalds round with probability at most $1/2$. Thirty independent rounds reduce this to $2^{-30}\approx9.31\times10^{-10}<10^{-9}$. If a service performs one million such verifications, assigning $10^{-9}$ to each call permits a union bound near $10^{-3}$, not $10^{-9}$ for the service.

### Connections

[ALGE-066](./066-randomized-selection-and-sampling.md) supplies unbiased random draws. [ALGE-067](./067-randomized-incremental-construction.md) is typically Las Vegas: order changes work, not the final structure. [ALGE-069](../ROADMAP.md#block-07--approximation-heuristics-and-randomized-algorithms) distinguishes theorem-backed randomized algorithms from empirically supported metaheuristics.

## Governing Question

Given a randomized algorithm, how do we determine whether it may return a wrong answer or merely take a random amount of time, prove the relevant probability bound, amplify it without false independence, and expose a production contract that remains honest under composition and deadlines?

“Randomized” describes a mechanism, not a guarantee. Two programs can consume identical random bits while making fundamentally different promises. A primality screen may occasionally label a composite “probably prime.” Randomized Quicksort always returns a sorted permutation under a valid comparator but has random comparison count. A candidate generator plus exact verifier never returns a bad candidate, yet may retry for an unbounded number of attempts.

## Why This Matters

Randomization often replaces expensive exhaustive work with a small failure probability or avoids deterministic pathological behavior. It supports algebraic verification, primality testing, graph cuts, hashing, sampling, optimization, distributed checking, and numerical algorithms. The gain is useful only if the displaced cost is replaced by a quantified and governed risk.

At service scale, a per-run error can accumulate across millions of calls. Correlated seeds can defeat amplification. A deadline can change a zero-error algorithm into a partial algorithm or a wrong-answer algorithm depending on fallback. Adaptive users can exploit exposed randomness. Machine arithmetic can invalidate a verifier that the proof assumes is exact.

The engineering objective is therefore a complete claim: input and adversary, random experiment, answer guarantee, runtime guarantee, repetition rule, error budget, arithmetic model, failure response, and reproducibility evidence.

## Prerequisites and Retrieval

Retrieve conditional probability, independence, union bounds, geometric random variables, expectation, matrix multiplication, finite fields, graph cuts, deterministic verification, pseudorandom generators, and service-level error accounting. Review [ALGE-006](./006-best-worst-expected-and-amortized-cost.md) for quantifiers, [ALGE-029](./029-randomization-as-a-design-tool.md) for fixed-input analysis, and [ALGE-066](./066-randomized-selection-and-sampling.md) for unbiased bounded draws and transcripts.

This chapter owns behavioral taxonomy, one- and two-sided error, amplification, verified retry, composition, deadlines, and operational evidence. It uses Freivalds verification and random contraction as canonical examples. Formal randomized complexity classes belong to Theory of Computation and Complexity; cryptographic random-number construction belongs to Security Engineering; broad heuristic evaluation begins in ALGE-069.

## Learning Objectives

After completing this module, you should be able to:

1. classify a randomized algorithm by answer and runtime guarantees rather than by reputation;
2. state one-sided error in the correct direction;
3. prove Freivalds' false-acceptance bound over an explicit arithmetic domain;
4. derive independent repetition and majority amplification bounds;
5. identify when shared state or repeated seeds invalidate product bounds;
6. construct a Las Vegas loop from random candidate generation and a sound verifier;
7. derive expectation and tail bounds for geometric retry;
8. allocate error across stages and repeated service calls without assuming independence;
9. specify timeout, fallback, adversary, randomness, and replay policies; and
10. separate mathematical guarantees from finite tests and operational observations.

## Core Exposition

### Classify the public behavior, not the source code

Let input $x$ have a set of acceptable outputs $F(x)$. A randomized program consumes random transcript $\rho$ and returns an output, failure status, or perhaps does not terminate. Classification begins with the public contract.

A Monte Carlo solver guarantees termination within a stated bound for every permitted $x$ and $\rho$, but permits

$$
\Pr_\rho[A(x;\rho)\notin F(x)]\le\epsilon(x)
$$

for a declared error bound. “Bounded time” can mean a deterministic operation count or an enforced resource budget; say which. If the process can overrun and be killed, its public behavior includes that outcome.

A Las Vegas solver satisfies $A(x;\rho)\in F(x)$ whenever it returns an answer. Its runtime $T(x;\rho)$ is random, with a claim such as $\mathbb E[T(x;\rho)]\le g(|x|)$. Some definitions permit an explicit `failure` followed by external retry; then success probability and orchestration are part of the full algorithm. Returning `unknown` is not a wrong answer if the output relation permits it, but it no longer solves a total yes/no contract on every invocation.

Randomized Quicksort with a consistent total comparator is Las Vegas: partitioning correctness is deterministic, while pivots determine work. A stochastic local-search heuristic with no error theorem is neither automatically a bounded-error Monte Carlo algorithm nor Las Vegas; it is a randomized heuristic with empirical evidence.

### State one-sided error without ambiguous labels

For decision problem language $L$, a one-sided algorithm may take one of two common forms:

- **false-positive side:** if $x\in L$, it accepts with probability one; if $x\notin L$, it accepts with probability at most $\epsilon$;
- **false-negative side:** if $x\notin L$, it rejects with probability one; if $x\in L$, it rejects with probability at most $\epsilon$.

Always state the conditional sentences. Terms such as “positive one-sided error” are used inconsistently across communities. A composite witness in a primality screen proves compositeness, while a round that finds no witness supports only “probably prime.” Freivalds never rejects a correct matrix identity under exact arithmetic, but may accept an incorrect one.

Two-sided error permits both directions, usually with correctness probability at least $1/2+\gamma$ for some advantage $\gamma>0$. Repeating and taking a majority can reduce error, provided trial errors satisfy the independence or martingale-style premises of the chosen concentration bound.

### Derive Freivalds' verifier

Given $n\times n$ matrices $A,B,C$ over a field, recomputing $AB$ by the classical method costs $\Theta(n^3)$ field operations. Freivalds samples $r\in\{0,1\}^n$ uniformly and compares $A(Br)$ with $Cr$, using three matrix-vector products and $\Theta(n^2)$ operations.

If $AB=C$, associativity gives equality for every $r$, so exact execution never rejects. Suppose $D=AB-C\ne0$. Choose a nonzero row $d$ and an index $j$ with $d_j\ne0$. Condition on every bit of $r$ except $r_j$. The equation $d\cdot r=0$ can hold for at most one of $r_j=0$ and $r_j=1$, because changing the bit changes the sum by nonzero $d_j$. Thus

$$
\Pr[Dr=0]\le\Pr[d\cdot r=0]\le\frac12.
$$

The argument works over a field and, with care, rings where the chosen nonzero coefficient does not vanish under the two-point difference. Overflow arithmetic is a different ring from mathematical integers and can make both completeness and soundness claims false. Declare the domain: exact integers, modular arithmetic with a specified modulus, or a finite field.

The executable model uses exact Python integers and injected bit vectors. Injection tests deterministic behavior; it is not a random generator or an amplification experiment.

<!-- bijux-verify: {"id":"freivalds-transcripts","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"correct r=(0, 1) accepted=True\nbad r=(0, 0) accepted=True\nbad r=(1, 0) accepted=True\nbad r=(0, 1) accepted=False\ninvalid_vector=rejected\n","stderr":""}} -->
```python
def mat_vec(matrix, vector):
    result = []
    for row in matrix:
        total = 0
        for index in range(len(vector)):
            total += row[index] * vector[index]
        result.append(total)
    return result


def freivalds(a, b, c, vector):
    n = len(a)
    if len(vector) != n or any(bit not in (0, 1) for bit in vector):
        raise ValueError("vector must contain n bits")
    if any(len(row) != n for matrix in (a, b, c) for row in matrix):
        raise ValueError("matrices must be square and equally sized")
    return mat_vec(a, mat_vec(b, vector)) == mat_vec(c, vector)


A = ((1, 2), (3, 4))
B = ((2, 0), (1, 2))
C = ((4, 4), (10, 8))
BAD = ((4, 4), (10, 9))

print(f"correct r={(0, 1)} accepted={freivalds(A, B, C, (0, 1))}")
for r in ((0, 0), (1, 0), (0, 1)):
    print(f"bad r={r} accepted={freivalds(A, B, BAD, r)}")
try:
    freivalds(A, B, C, (0, 2))
except ValueError:
    print("invalid_vector=rejected")
```

The incorrect product differs only in the second column, so vectors with second bit zero miss the error. This is expected one-round behavior, not a defect in the bound.

### Amplify the guarantee actually proved

For a one-sided false-accept algorithm with per-round conditional error at most $q<1$, reject if any round rejects and accept only if all $k$ rounds accept. With fresh independent rounds, or more generally when the error bound $q$ holds conditional on every prior transcript, the probability of false acceptance is at most $q^k$.

For Freivalds, $q=1/2$, so choose

$$
k\ge\left\lceil\log_2\frac1\delta\right\rceil
$$

to obtain error at most $\delta$. Thirty rounds suffice for $\delta=10^{-9}$. This calculation assumes every round draws a new uniform vector. Resetting a generator to the same seed, caching the first vector, or hashing the same input to one fixed vector repeats the same test and gives no product amplification.

For a false-negative algorithm, accept if any round accepts; all rounds must miss for failure. For independent two-sided trials correct with probability at least $1/2+\gamma$, majority voting has an exponentially decreasing error bound, for example at most $e^{-2\gamma^2k}$ by a standard Hoeffding argument. Odd $k$ avoids a majority tie; a tie policy must otherwise be part of the algorithm.

Independence is sufficient but not always necessary. A proof can use conditional soundness: even after observing prior draws and outcomes, the next round's failure probability is at most $q$. Pairwise independence is not generally enough to multiply $k$ failure probabilities. Name the actual property supplied by the generator and stream derivation.

### Convert candidate generation into verified retry

Suppose random procedure `propose(x)` produces a candidate, and deterministic `verify(x,y)` is sound: whenever it accepts, $y\in F(x)$. Repeat proposals until verification accepts. Every returned candidate is correct, so the construction is Las Vegas. To claim finite expected runtime, additionally prove that each attempt succeeds with probability at least $p>0$ under the conditional state and that attempt cost is bounded appropriately.

If trials are independent with success probability $p$, the number of attempts is geometric:

$$
\Pr[T=t]=(1-p)^{t-1}p,
\quad
\mathbb E[T]=1/p,
\quad
\Pr[T>t]=(1-p)^t.
$$

Soundness alone does not prove termination. Completeness bugs, unreachable witnesses, stateful proposal bias, resource leaks, or an adaptive adversary can make $p=0$. A verifier that is itself Monte Carlo does not create a Las Vegas algorithm unless its possible mistakes are eliminated by another sound layer.

Randomized selection, Quicksort, and randomized incremental construction are zero-error because their deterministic mechanisms establish the result for every choice transcript. They do not need a post-hoc verifier for correctness, though invariant checks remain useful evidence.

### Analyze random contraction as Monte Carlo

Karger's contraction algorithm repeatedly chooses a uniformly random current edge, contracts its endpoints, and removes self-loops until two supervertices remain. The remaining edges define a cut. Every returned object is a cut, but it need not be a minimum cut, so the optimization answer has Monte Carlo error.

Fix one global minimum cut of value $\lambda$ in an unweighted multigraph with $r$ current supervertices, assuming none of its edges has yet been contracted. Every supervertex has degree at least $\lambda$, so there are at least $r\lambda/2$ edges. The probability that the next random edge crosses the fixed cut is at most $2/r$. Its survival probability down to two vertices is therefore at least

$$
\prod_{r=n}^{3}\left(1-\frac2r\right)
=\prod_{r=n}^{3}\frac{r-2}{r}
=\frac{2}{n(n-1)}.
$$

This is a lower bound for finding a fixed minimum cut in one run, not a claim that failure probability is constant. Independent repetitions and taking the smallest returned cut amplify success. A deterministic cut-value check proves that each output is a cut of its reported value, but cannot cheaply certify global minimality without additional machinery; selecting the best observed cut does not convert the method to Las Vegas.

### Compose error across a system

A per-call error target is not a service-lifetime target. If events $E_1,\ldots,E_m$ denote incorrect outputs, the union bound gives

$$
\Pr\!\left[\bigcup_{i=1}^mE_i\right]\le\sum_{i=1}^m\Pr[E_i],
$$

without requiring independence. Allocate budgets $\delta_i$ so their sum is within the accepted system risk. Include preprocessing screens, algorithm rounds, replica comparisons, retries that may publish, and downstream decisions that reuse probabilistic answers.

If one result is cached and served one million times, there was one random failure opportunity but one million impacts. If one million independent computations occur, there are one million opportunities. Risk governance should distinguish probability, blast radius, reversibility, and detection.

Conditional execution complicates counting. A second probabilistic stage invoked only after the first accepts still consumes budget on paths where it runs. Union bounds remain safe; tighter composition requires a joint probability model. Never assume tenant, thread, or machine independence merely because labels differ.

### Specify timeouts and fallback honestly

A hard timeout on a Las Vegas algorithm yields three possible designs:

1. return `unknown` and preserve zero wrong-answer probability under a partial-output contract;
2. fall back to a deterministic exact algorithm, preserving total correctness with a new runtime bound; or
3. return an unchecked candidate, changing the system into a Monte Carlo or unquantified heuristic algorithm.

These are not operationally equivalent. Cancellation must occur at a coherent state boundary, and background work must not later publish a result after the caller treats the request as failed. Retry limits change expected-runtime semantics into a bounded-attempt success/failure contract.

For latency planning, expectation is insufficient. Derive a tail bound when possible and measure quantiles, maxima, cancellations, and fallback rates. Markov's inequality can turn an expectation into a weak tail bound, but algorithm-specific concentration or geometric tails are usually more useful. Do not label a bound “with high probability” unless the parameter and asymptotic meaning are given, such as failure at most $n^{-c}$ for declared $c$.

### Protect the random experiment

The theorem may assume an input fixed before private random choices. Logging seeds publicly before an adversary commits input, deriving choices from predictable timestamps, or allowing repeated oracle queries against a fixed hidden vector can enable adaptation. Security-sensitive deployments need an explicit attacker capability model and an appropriate cryptographic generator; statistical quality alone does not imply unpredictability.

Reproducibility pulls in the opposite direction. Store a protected transcript or deterministic derivation keyed by snapshot identity and attempt number. Record generator algorithm and version because a numeric seed alone may replay differently after an implementation change. Separate operational replay access from public observability.

Parallel workers require disjoint or formally derived substreams. Forking identical process state can repeat random choices. Speculative execution that accepts the first completed result can bias the selected distribution toward faster transcripts; that may preserve correctness for Las Vegas algorithms but changes performance measurements and may alter Monte Carlo error when runtime correlates with error.

### Build evidence at the right strength

Proof evidence records the sample space, arithmetic model, fixed/adaptive input assumption, error event, and derivation. Implementation evidence extracts random-draw boundaries, verifies range mappings, injects deterministic transcripts, checks both accepting and rejecting paths, and records toolchain behavior. Exhaustive finite enumeration can validate the Freivalds bound for small matrices and all bit vectors.

Statistical tests can reveal generator, stream, or integration defects. They do not prove the theorem or show that an observed zero failures has zero risk. Predeclare trial count and acceptance criteria; report confidence intervals and every failed or timed-out trial. Rare-event probabilities such as $10^{-12}$ cannot be validated directly with a few thousand ordinary trials.

Production telemetry should include algorithm and generator versions, input-class and snapshot identifiers, round count, stream derivation, decision path, verifier result, retries, timeout/fallback, resource usage, and whether exact downstream confirmation occurred. Minimize sensitive raw data and seeds while retaining controlled replay.

## Definitions and Notation

| Term | Precise use in this chapter |
|---|---|
| $F(x)$ | Set of acceptable outputs for input $x$ |
| $\rho$ | Randomness transcript consumed by one run |
| $\epsilon,\delta$ | Per-round or target error probability, as labeled |
| $q$ | Upper bound on conditional failure probability of one round |
| $k$ | Number of amplification rounds |
| $p$ | Lower bound on success probability of one verified attempt |
| $T$ | Random number of attempts or runtime |
| witness | Object accepted by a sound deterministic verifier |
| completeness | A correct assertion is accepted, often with probability one |
| soundness | An incorrect assertion is accepted only within a declared bound |
| one-sided error | Only one of false acceptance and false rejection is possible |
| two-sided error | Both false acceptance and false rejection may occur |
| error budget | Governed upper bound allocated across failure opportunities |

A **model** declares inputs, outputs, adversary, arithmetic, and randomness. A **mechanism** samples pivots, vectors, contractions, or candidates. A **guarantee** bounds answer error or runtime under that model. An **implementation** supplies concrete generators, arithmetic, concurrency, and cancellation. A **policy** allocates error and chooses rounds, timeout, fallback, logging, and confirmation. **Evidence** supports specific code and environments without silently upgrading empirical absence of failure into proof.

## Mechanisms, Invariants, or Proof Structure

### Classification checklist

1. Define $F(x)$ and every public status, including `unknown`, timeout, and partial output.
2. For every transcript, ask whether a returned answer must belong to $F(x)$.
3. If not, define the exact error event and its direction.
4. State whether runtime is deterministically bounded, bounded only by policy, expected, or given a tail bound.
5. Identify the probability space and what the adversary observes before fixing input.
6. Audit arithmetic and verifier soundness independently of random quality.

### Amplification checklist

1. Decide whether acceptance requires all rounds, any round, or a majority.
2. Prove the single-round conditional error bound for the actual input domain.
3. Establish fresh independence or the weaker conditional property the product proof needs.
4. Solve the bound for $k$ with exact rounding.
5. Include tie rules, early stopping, retries, cache reuse, and parallel selection.
6. Allocate the resulting per-operation bound within the larger system error budget.

### Las Vegas retry invariant

- only verifier-accepted candidates may be returned;
- verifier acceptance implies membership in $F(x)$ under exact semantics;
- failed candidates cannot corrupt later attempts unless stateful analysis includes that state;
- each attempt's success lower bound holds conditional on prior failures;
- resources are released or bounded across attempts; and
- timeout produces only a declared partial status or a correctness-preserving fallback.

## Alternatives and Trade-Offs

| Approach | Answer guarantee | Resource profile | Main engineering obligation |
|---|---|---|---|
| Deterministic exact | Correct for all permitted inputs | Often higher fixed or worst-case cost | Validate implementation and arithmetic |
| Monte Carlo, one-sided | One output direction may err | Usually bounded and amplifiable | Preserve witness direction and error budget |
| Monte Carlo, two-sided | Either output may err | Bounded; majority can amplify | Prove advantage and trial conditions |
| Las Vegas construction | Every returned answer correct | Random expected/tail runtime | Prove invariant and control tails |
| Candidate plus exact verifier | Only verified candidates returned | Geometric retries plus verification | Prove soundness and success probability |
| Bounded Las Vegas with `unknown` | No wrong answers, may abstain | Hard budget | Make abstention explicit to callers |
| Deterministic fallback | Correct answer after random fast path | More code; bounded tail | Preserve shared semantics across routes |
| Randomized heuristic | No general theorem | Empirically selected budget | Avoid Monte Carlo/Las Vegas labels and evaluate honestly |

Monte Carlo is attractive when a tiny quantified error is acceptable and deterministic verification would erase the speedup. Las Vegas is attractive when wrong answers are unacceptable but variable work can be absorbed or capped with a safe fallback. Deterministic algorithms remain preferable when input sizes are modest, adversaries are strong, audit rules prohibit probabilistic answers, or implementation complexity dominates theoretical savings.

## Failure Modes and Misconceptions

- **“Randomized means Monte Carlo.”** Randomized Quicksort is zero-error; an unproved randomized heuristic has no Monte Carlo error bound.
- **“Las Vegas means bounded runtime.”** It means returned answers are correct; runtime is random and needs expectation or tail analysis.
- **“A verifier makes any retry Las Vegas.”** The verifier must be sound, and a termination claim needs nonzero success probability.
- **“One-sided error is obvious.”** State which true condition is never rejected and which false condition may be accepted.
- **“Ten executions divide error by ten.”** Independent all-round acceptance multiplies error; repetition alone has no universal rule.
- **“Different thread IDs imply independent randomness.”** Forked state or weak derivation can create identical or correlated streams.
- **“A per-call bound is the system bound.”** Repeated calls, stages, and publication opportunities consume a composed budget.
- **“A timeout preserves Las Vegas semantics.”** Only if it returns `unknown` or uses a correctness-preserving fallback.
- **“Exact theorem, floating implementation.”** Overflow, rounding, NaN, and nondeterministic reductions can violate verifier premises.
- **“No failures observed proves the target.”** Ordinary tests cannot directly validate extremely rare-event guarantees.
- **“Public seeds are harmless.”** They aid replay but can permit adaptive inputs or repeated evasion.
- **“First replica wins is neutral.”** Runtime-dependent selection can change transcript distributions and measured error.

## Worked Examples

### Example 1

**Situation.** Randomized Quicksort chooses every pivot uniformly and uses a consistent total comparator. Is it Monte Carlo or Las Vegas?

**Reasoning.** For every pivot transcript, partitioning preserves the multiset and recursive postconditions produce sorted subranges. Thus the returned array is correct for every transcript. The number of comparisons varies from typical $O(n\log n)$ expected work to quadratic bad paths.

**Conclusion.** It is Las Vegas: correctness is deterministic, while runtime depends on randomness.

### Example 2

**Situation.** A Freivalds round accepts a claimed product $C=AB$. What exactly follows?

**Reasoning.** Under exact arithmetic, a correct product is accepted for every bit vector. An incorrect product can also be accepted, but with probability at most $1/2$ for a uniform vector. Therefore rejection certifies inequality, while acceptance is probabilistic evidence for equality.

**Conclusion.** It is one-sided Monte Carlo with possible false acceptance and no false rejection under the model.

### Example 3

**Situation.** In the executable example, $C$ is changed only from 8 to 9 in row two, column two. Trace vectors $(1,0)$ and $(0,1)$.

**Reasoning.** The error matrix has zero first column and nonzero second column. Multiplying it by $(1,0)^T$ gives zero, so the bad product passes. Multiplying by $(0,1)^T$ exposes the nonzero error and rejects. Both outcomes conform to the one-half upper bound over all four bit vectors.

**Conclusion.** A passing transcript is allowed; soundness is a probability statement across the declared vector distribution.

### Example 4

**Situation.** Choose the number of independent Freivalds rounds for false-accept probability below $10^{-9}$.

**Reasoning.** Require $2^{-k}<10^{-9}$. Since $2^{-29}\approx1.86\times10^{-9}$ is too large and $2^{-30}\approx9.31\times10^{-10}$ is small enough, $k=30$.

**Conclusion.** Thirty fresh rounds meet the target; 29 do not.

### Example 5

**Situation.** A worker runs 30 rounds but reinitializes its generator with seed 17 before every draw.

**Reasoning.** Every round obtains the same vector. An incorrect product annihilated by that vector passes all 30 rounds. The events are identical, so their intersection probability is the single-round probability, not its thirtieth power.

**Conclusion.** Stream freshness is a proof obligation; repeated execution with repeated randomness provides no amplification.

### Example 6

**Situation.** What lower bound does random contraction give for finding a fixed minimum cut of an eight-vertex graph in one run?

**Reasoning.** The survival product is $2/(n(n-1))=2/(8\cdot7)=1/28$. Thus failure probability is at most $27/28$ for that one-run lower bound. Repeating $t$ independently makes failure at most $(27/28)^t$.

**Conclusion.** One run has small success probability; the algorithm becomes useful through analyzed repetition, not wishful “randomness.”

### Example 7

**Situation.** A sound verifier accepts each independently proposed candidate with probability $p=1/4$. Find expected attempts and the probability of needing more than ten.

**Reasoning.** Geometric retry gives $\mathbb E[T]=1/p=4$. The tail is $\Pr[T>10]=(3/4)^{10}\approx0.0563$. Sound verification makes every returned answer correct, but about 5.6% of runs exceed ten attempts.

**Conclusion.** Expected work and tail latency are separate even for a valid Las Vegas construction.

### Example 8

**Situation.** The retry loop above is capped at ten attempts. What algorithm results?

**Reasoning.** If it returns `unknown` after ten failures, it remains zero-error but succeeds with probability $1-(3/4)^{10}$ per invocation. If it returns the tenth unchecked candidate, correctness is lost and no Monte Carlo bound follows unless candidate error was separately proved. If it calls an exact fallback, total correctness remains and latency includes fallback.

**Conclusion.** A timeout policy can preserve, weaken, or destroy the original guarantee.

### Example 9

**Situation.** A service performs at most one million probabilistic checks and wants lifetime wrong-answer probability at most $10^{-6}$.

**Reasoning.** Without assuming independence, assign each check error at most $10^{-12}$. The union bound gives $10^6\cdot10^{-12}=10^{-6}$. With Freivalds, $k=40$ gives $2^{-40}\approx9.09\times10^{-13}$, meeting the per-check allocation; $k=39$ does not.

**Conclusion.** Round count follows from the composed service budget, not an isolated per-call convention.

### Example 10

**Situation.** A storage system probabilistically verifies a large batch before irreversible publication. Which design is defensible?

**Reasoning.** Bind the immutable batch digest; derive fresh protected vectors by batch, round, algorithm version, and domain; choose rounds from the lifetime publication budget; execute exact or declared modular arithmetic; reject on any failing round; and retain the decision transcript. If policy forbids any probabilistic publication risk, use the fast check only as a screen and perform deterministic verification before commit.

**Conclusion.** Algorithm choice depends on consequence and reversibility as well as operation count.

## Cross-Program Connections

- **Theory of Computation and Complexity:** RP, coRP, ZPP, and BPP formalize machine classes; this chapter focuses on concrete algorithm and service contracts.
- **Security Engineering:** generator unpredictability, side channels, seed exposure, and adaptive adversaries determine whether mathematical sampling premises survive attack.
- **Software Testing and Quality Engineering:** deterministic transcript tests, fault injection, statistical tests, and rare-event experiments supply complementary but bounded evidence.
- **Software Delivery and Reliability Engineering:** error budgets, timeout behavior, fallback, telemetry, incident impact, and irreversible publication govern deployment.
- **Database Engineering:** snapshot binding and atomic publication prevent a verified object from being swapped for unverified data.
- **Distributed Systems:** replica races, stream derivation, retries, and correlated failure complicate independence and composition.
- **Algorithm Engineering:** [ALGE-066](./066-randomized-selection-and-sampling.md) owns draw correctness; [ALGE-067](./067-randomized-incremental-construction.md) applies zero-error random ordering; [ALGE-069](../ROADMAP.md#block-07--approximation-heuristics-and-randomized-algorithms) owns evidence for methods without classical guarantees.

## References

1. Rajeev Motwani and Prabhakar Raghavan, *Randomized Algorithms*, Cambridge University Press, 1995. DOI: [10.1017/CBO9780511814075](https://doi.org/10.1017/CBO9780511814075). Graduate reference for randomized-algorithm taxonomy, probability tools, and applications; publisher record checked 2026-09-05.
2. Michael Mitzenmacher and Eli Upfal, *Probability and Computing: Randomization and Probabilistic Techniques in Algorithms and Data Analysis*, 2nd ed., Cambridge University Press, 2017, ISBN 978-1-107-15488-9. Reference for amplification, concentration, hashing, and Monte Carlo methods; bibliographic record checked 2026-09-05.
3. Rūsiņš Freivalds, “Fast Probabilistic Algorithms,” in *Mathematical Foundations of Computer Science 1979*, LNCS 74, 57–69. DOI: [10.1007/3-540-09526-8_5](https://doi.org/10.1007/3-540-09526-8_5). Primary source for probabilistic matrix-product verification; record checked 2026-09-05.
4. David R. Karger, “Global Min-cuts in RNC, and Other Ramifications of a Simple Min-Cut Algorithm,” *Proceedings of the Fourth Annual ACM-SIAM Symposium on Discrete Algorithms*, 1993, 21–30. [Author-hosted paper](https://people.csail.mit.edu/karger/Papers/mincut.pdf). Primary source for random contraction; checked 2026-09-05.
5. Michael O. Rabin, “Probabilistic Algorithm for Testing Primality,” *Journal of Number Theory* 12(1), 1980, 128–138. DOI: [10.1016/0022-314X(80)90084-0](https://doi.org/10.1016/0022-314X(80)90084-0). Primary source for one-sided probabilistic primality testing; publisher record checked 2026-09-05.
6. Jacob T. Schwartz, “Fast Probabilistic Algorithms for Verification of Polynomial Identities,” *Journal of the ACM* 27(4), 1980, 701–717. DOI: [10.1145/322217.322225](https://doi.org/10.1145/322217.322225). Primary source for probabilistic polynomial-identity verification; record checked 2026-09-05.
7. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein, *Introduction to Algorithms*, 4th ed., MIT Press, 2022, ISBN 978-0-262-04630-5. Textbook reference for randomized algorithms, indicator analysis, and graph algorithms; bibliographic data checked 2026-09-05.

## Exercises

### Exercise 1

A randomized procedure always returns a valid spanning tree but its weight may exceed the minimum with probability at most $0.01$. Classify its guarantee, state the error direction, and explain why checking only that the output is a spanning tree does not make it Las Vegas for minimum spanning tree.

### Exercise 2

A one-sided verifier has conditional false-acceptance probability at most $1/3$ in every fresh round. Derive the rounds required for error at most $10^{-8}$. State the acceptance combination and independence/conditional premise.

### Exercise 3

A process forks eight workers after initializing one pseudorandom generator. Each worker performs the same four-round verifier and all report the same vectors. Diagnose the error calculation and design reproducible disjoint streams.

### Exercise 4

Design a deadline policy for a Las Vegas candidate generator with sound verification. Compare `unknown`, deterministic fallback, and unchecked-candidate fallback in terms of correctness, availability, and evidence.

### Exercise 5

A pipeline performs up to $10^4$ polynomial identity checks and $10^6$ matrix-product checks before one irreversible release. The accepted total wrong-release probability is $10^{-9}$. Allocate a defensible error budget, derive Freivalds rounds for the matrix checks, and state what must be known to determine rounds for the polynomial checks.

## Answers to the Exercises

### Answer 1

The procedure is Monte Carlo for the optimization problem: it returns a feasible spanning tree but can falsely assert or imply optimality. Its error is a false claim of minimum weight, with probability at most $0.01$ under the stated random experiment. A deterministic tree verifier proves only connectivity, acyclicity, and vertex coverage. It does not prove that no lighter tree exists. The procedure becomes Las Vegas for minimum spanning tree only if an exact optimality certificate is soundly verified before return, or if its construction proves optimality for every transcript.

### Answer 2

Accept only if every round accepts. With fresh rounds whose false-acceptance probability remains at most $1/3$ conditional on all previous outcomes, error is at most $(1/3)^k$. We need

$$
k\ge\left\lceil\frac{\ln(10^8)}{\ln3}\right\rceil=17,
$$

because $3^{16}=43{,}046{,}721<10^8$ while $3^{17}=129{,}140{,}163>10^8$. Independence is sufficient; the stated per-round conditional bound is also sufficient. Merely obtaining different object instances or thread IDs is not.

### Answer 3

Forking copied generator state, so the eight workers duplicate rather than amplify four rounds. The global false-acceptance bound remains the four-round bound, not its eighth power. Derive each stream from a protected master key and a domain-separated tuple containing snapshot digest, algorithm version, worker identity, attempt, and round, using a specified generator or keyed derivation. Record those nonsecret identities and generator version for replay, test non-overlap at the derivation boundary, and keep secret material access controlled. Alternatively assign one coordinator-generated vector transcript with disjoint slices.

### Answer 4

Returning `unknown` at the deadline preserves zero wrong answers but lowers per-call availability; record attempts, verifier failures, and timeout. A deterministic exact fallback preserves a total correct-answer contract but adds worst-case latency and duplicate implementation that must share semantics. Returning an unchecked candidate maximizes apparent availability but abandons Las Vegas correctness; it is acceptable only if a separate Monte Carlo error bound and policy explicitly authorize that risk. In every design, cancellation must prevent late publication, the coherent input snapshot and transcript must be retained, and metrics must include fallback rather than sampling only fast successes.

### Answer 5

One simple union-bound allocation assigns half the budget to each family: $5\times10^{-10}$ total for polynomial checks and the same for matrix checks. Each of $10^6$ matrix checks then receives $5\times10^{-16}$. Freivalds requires $2^{-k}\le5\times10^{-16}$; $k=51$ works because $2^{-51}\approx4.44\times10^{-16}$, whereas $k=50\approx8.88\times10^{-16}$ does not. Each of $10^4$ polynomial checks receives $5\times10^{-14}$. To choose its repetitions, we need the single-round polynomial-identity error bound, which depends on degree, evaluation-set size and distribution, arithmetic field, and whether the conditional bound survives adaptive repetition. Other allocations are acceptable if all per-check bounds sum to at most $10^{-9}$ and the consequences justify the split.
