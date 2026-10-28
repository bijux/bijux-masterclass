---
module_id: ALGE-007
program: Algorithm Engineering
level: 1
module_number: 7
title: Recurrences and the Master Method
status: complete
last_verified: 2026-09-04
---

# Recurrences and the Master Method

## One-Page Review

### Governing question

How can the recursive control structure of an algorithm be translated into a valid cost recurrence, solved with an applicable method, and checked against base cases, rounding, and actual execution semantics?

### Essential definitions

- A **recurrence** defines a cost at size $n$ using costs at smaller sizes plus non-recursive work.
- A **base condition** gives finite costs below a threshold and makes the recurrence well founded.
- **unrolling/iteration** repeatedly substitutes the recurrence until reaching base cases.
- A **recursion tree** represents subproblem calls as nodes and sums non-recursive work by level.
- The **substitution method** proposes a bound and proves it, usually by induction with carefully chosen constants and lower-order slack.
- The **Master Method** solves recurrences $T(n)=aT(n/b)+f(n)$ by comparing $f(n)$ with $n^{\log_b a}$ under explicit hypotheses.
- A **regularity condition** in the root-dominated Master case ensures recursive levels shrink geometrically relative to $f(n)$.
- The **Akra–Bazzi method** extends recurrence analysis to certain unequal, perturbed divide-and-conquer subproblems.
- A **work recurrence** totals all executed work; a **span/depth recurrence** follows the longest parallel dependency; a **peak-space recurrence** counts simultaneously live storage.

### Central model, mechanism, or theorem

For constants $a\ge1$, $b>1$, base cost $T(n)=\Theta(1)$ below a fixed threshold, and asymptotically nonnegative $f$, consider

$$
T(n)=aT(n/b)+f(n).
$$

Let $p=\log_b a$. A common extended Master theorem gives:

1. If $f(n)=O(n^{p-\epsilon})$ for some $\epsilon>0$, then $T(n)=\Theta(n^p)$.
2. If $f(n)=\Theta(n^p\log^k n)$ for constant $k\ge0$, then $T(n)=\Theta(n^p\log^{k+1}n)$.
3. If $f(n)=\Omega(n^{p+\epsilon})$ for some $\epsilon>0$ and $af(n/b)\le cf(n)$ eventually for a constant $c<1$, then $T(n)=\Theta(f(n))$.

The theorem is a classifier, not a recurrence generator. A wrong recurrence produces a confidently wrong solution.

### Critical invariants

- Derive one recurrence for the exact resource and case being analyzed; do not copy a familiar formula from similar-looking code.
- State base conditions, admitted sizes, floors/ceilings, and whether subproblems overlap or execute at all.
- Prove recursive sizes strictly decrease and remain in the domain.
- Separate number of recursive calls from syntactic occurrences, memoized hits, parallel execution, and short-circuit branches.
- At recursion-tree level $i$, use $a^i$ nodes of size $n/b^i$ and cost $a^if(n/b^i)$ only when the balanced model applies.
- Verify every Master theorem premise, including polynomial separation and case-3 regularity.
- Do not force unequal splits, variable branching, $T(n-1)$ recurrences, or irregular input-dependent calls into the Master template.
- Use induction/substitution to verify a guessed result and preserve enough slack for floors and lower-order terms.
- For peak space, add only simultaneously live storage; sequential sibling calls often use a maximum, not a sum.
- Distinguish work, span, I/O, allocation, and elapsed time recurrences.

### Common failures

Common failures include omitting a base case; using $n/b$ without a rounding convention; counting a recursive call that a branch does not take; multiplying memoized subproblems as though recomputed; treating two sequential calls as parallel span; adding both sibling stacks for peak space after one returns; applying Master to $T(n)=T(n-1)+f(n)$ or unequal splits; choosing the wrong $a$ or $b$; confusing $n^{\log_b a}$ with $a^{\log_a n}$ without checking bases; omitting case-3 regularity; accepting a recursion-tree pattern without summing leaves; and validating a recurrence solution without validating the recurrence-to-code correspondence.

### Compact example

For the idealized merge recurrence on powers of two,

$$
T(1)=0,
\qquad
T(n)=2T(n/2)+n,
$$

level $i$ has $2^i$ subproblems, each contributing $n/2^i$, so every non-leaf level costs $n$. There are $\log_2 n$ such levels, hence

$$
T(n)=n\log_2 n.
$$

Master case 2 gives the same $\Theta(n\log n)$ class with $a=b=2$, $p=1$, and $f(n)=\Theta(n)$.

### Connections

[ALGE-004](./004-inductive-correctness-proofs.md) supplies inductive verification; [ALGE-005](./005-asymptotic-time-and-space.md) supplies growth notation; [ALGE-006](./006-best-worst-expected-and-amortized-cost.md) supplies cost quantifiers. [ALGE-021](../ROADMAP.md) develops divide-and-conquer design, while ALGE-081 separates parallel work and span.

## Governing Question

Recursive algorithms define cost indirectly: the work for a problem includes work for smaller problems. How do we turn that execution into a mathematical recurrence, solve the recurrence without using a theorem outside its domain, and show that the solution describes the intended implementation and resource?

Three tasks are involved. Modeling determines the recurrence. Mathematics solves or bounds it. Correspondence checks base thresholds, rounding, branching, memoization, parallelism, allocation, and failure behavior. A correct algebraic solution cannot compensate for a recurrence that double-counts calls or models time when the decision requires peak space.

## Why This Matters

Recurrences reveal how local decomposition compounds. Halving once per call produces logarithmic depth; branching into two halves can produce linear leaves; adding linear combine work at every balanced level produces $n\log n$; decrementing by one while doing linear work produces quadratic time. These outcomes are hard to infer safely from recursive syntax alone.

The Master Method is useful precisely because many balanced divide-and-conquer algorithms share a template. Its convenience also invites misuse. Production code has cutoff thresholds, uneven partitions, memoization, early termination, parallel tasks, failed retries, and bounded stacks. Engineers need both the fast classifier and the judgment to step away from it.

Recurrences also bridge proof and measurement. A recursion tree predicts which levels dominate and what counters to collect. A trace can reveal that partition balance, branch frequency, or combine cost violates the model. Measurement can challenge premises, but a finite timing curve does not prove a recurrence solution.

## Prerequisites and Retrieval

Retrieve:

- functions, sequences, induction, inequalities, and asymptotic notation;
- finite and geometric sums, logarithms, exponents, floors, and ceilings;
- recursive calls, base cases, stacks, trees, divide-and-conquer, and memoization;
- worst, expected, amortized, work, depth, and peak-live-space distinctions;
- exact operation counts and representation-based input size.

You should be able to prove a proposed upper bound by induction and sum $1+r+\cdots+r^k$. Recall that correctness induction and cost recurrence are separate: one proves returned values; the other counts resources under a model.

## Learning Objectives

After completing this module, you should be able to:

1. derive a recurrence from recursive control flow and a declared cost model;
2. specify base costs, thresholds, size domains, and rounding conventions;
3. solve decrementing and halving recurrences by unrolling;
4. build and sum balanced recursion trees by level;
5. prove candidate bounds with substitution and induction;
6. apply all three Master cases only after checking their premises;
7. recognize gaps and recurrences outside the Master Method;
8. use Akra–Bazzi at a conceptual level for eligible unequal splits;
9. distinguish time/work, span, and peak-space recurrences;
10. validate recurrence-to-implementation correspondence with counters and adversarial inputs.

## Core Exposition

### Model one execution resource at a time

Let $C(x)$ be modeled cost on admitted input $x$, and let $T(n)$ summarize the selected case over inputs of size $n$. For a recursive branch that creates subproblems $x_1,\ldots,x_k$ and performs local work $g(x)$, a work equation has the shape

$$
C(x)=\sum_{j=1}^{k}C(x_j)+g(x).
$$

Turning this into a one-variable recurrence requires bounds on each subproblem size and local work. If every size-$n$ input creates two half-size calls and $\Theta(n)$ local work, worst-case work may satisfy

$$
T(n)=2T(\lceil n/2\rceil)+\Theta(n).
$$

If only one of two branches executes, the factor is not two. If results are memoized, syntactic calls can be cache hits rather than new subproblems. If subproblem sizes depend on values, a worst-case recurrence must maximize over legal splits rather than assume balance.

### Base conditions make the definition complete

A recurrence needs a base threshold, such as

$$
T(n)=\Theta(1)\quad\text{for }0\le n\le n_0.
$$

This reflects validation, empty input, a leaf, or an implementation cutoff to an iterative routine. It also stops descent. Without a base, $T(n)=T(n/2)+1$ is not a complete cost definition.

Exact solutions depend on base constants and rounding. Asymptotic solutions often tolerate floors/ceilings under standard monotonicity and bounded-base assumptions, but that tolerance should be argued. A clean derivation may first restrict $n$ to powers of $b$ and then bound neighboring sizes for general $n$.

Every recursive argument must be strictly smaller in a well-founded domain. A cost recurrence for a call that can repeat the same size may conceal nontermination; ALGE-004's descent proof remains necessary.

### Unrolling handles simple recurrences transparently

For

$$
T(n)=T(n-1)+c,
\qquad T(0)=d,
$$

substitute repeatedly:

$$
T(n)=T(n-k)+kc.
$$

At $k=n$, $T(n)=d+nc=\Theta(n)$ when $c>0$. If local work is the current size,

$$
T(n)=T(n-1)+n
=T(0)+\sum_{j=1}^{n}j
=\Theta(n^2).
$$

For a halving recurrence,

$$
T(n)=T(\lfloor n/2\rfloor)+\Theta(1),
$$

only $\Theta(\log n)$ substitutions occur before reaching a constant. If local work is $\Theta(n)$, the unrolled geometric sum $n+n/2+n/4+\cdots$ is $\Theta(n)$.

### Recursion trees separate breadth, depth, and per-node work

For $T(n)=aT(n/b)+f(n)$ with balanced sizes, level $i$ contains $a^i$ nodes of size $n/b^i$. Its non-recursive work is

$$
W_i=a^if(n/b^i).
$$

The height is approximately $h=\log_b n$. The leaf count is

$$
a^h=a^{\log_b n}=n^{\log_b a}.
$$

The total combines internal levels and base leaves:

$$
T(n)=\sum_{i=0}^{h-1}a^if(n/b^i)+\Theta(n^{\log_b a}).
$$

This expression explains the Master cases. If level costs grow geometrically, leaves dominate. If every level has comparable cost, a logarithmic number of levels multiplies it. If costs shrink geometrically, the root dominates.

A recursion tree is a proof aid only when node counts, sizes, local costs, and stopping depths are justified. Drawing three levels and spotting a pattern is a conjecture until the general level and terminal sum are established.

### Substitution verifies a candidate bound

The substitution method guesses an upper or lower form, assumes it for smaller arguments, substitutes into the recurrence, and chooses constants so the inequality closes. For

$$
T(n)=2T(n/2)+n,
$$

a direct guess $T(n)\le cn\log_2 n$ gives

$$
T(n)
\le2c\frac{n}{2}\log_2\frac{n}{2}+n
=cn(\log_2 n-1)+n
=cn\log_2 n+(1-c)n.
$$

Any $c\ge1$ closes the inductive step after the base constant is absorbed. For recurrences with additive constants or floors, a stronger hypothesis such as $T(n)\le cn\log n-dn$ may provide the slack a bare leading term lacks.

Substitution verifies a guess; it does not generate one. Unrolling, recursion trees, characteristic methods, integrals, or experience can suggest the form. Prove upper and lower bounds when claiming $\Theta$.

### Apply the Master Method by a fixed checklist

For

$$
T(n)=aT(n/b)+f(n),
$$

first identify constants $a\ge1$ and $b>1$, then compute

$$
p=\log_b a.
$$

Compare $f(n)$ with $n^p$, not merely by informal labels:

- **leaf dominated:** $f(n)=O(n^{p-\epsilon})$ for some fixed $\epsilon>0$, so $T(n)=\Theta(n^p)$;
- **balanced levels:** $f(n)=\Theta(n^p\log^k n)$ for fixed $k\ge0$, so $T(n)=\Theta(n^p\log^{k+1}n)$;
- **root dominated:** $f(n)=\Omega(n^{p+\epsilon})$ plus eventual $af(n/b)\le cf(n)$ for some $c<1$, so $T(n)=\Theta(f(n))$.

Polynomial separation matters. If $f$ differs from $n^p$ by only a factor such as $\log\log n$, the displayed three cases may not apply. “None of the cases” means use another theorem or direct analysis, not that the recurrence lacks a solution.

### Case 1: leaves dominate

Consider

$$
T(n)=4T(n/2)+n.
$$

Here $p=\log_2 4=2$ and $f(n)=n=O(n^{2-1})$. At level $i$, total local work is $4^i(n/2^i)=n2^i$, growing geometrically toward $n^2$ leaves. Therefore $T(n)=\Theta(n^2)$.

The result does not mean the root work vanished. It means the total contribution of upper levels is within a constant multiple of the leaf scale.

### Case 2: levels balance

For merge-style recurrence

$$
T(n)=2T(n/2)+n,
$$

$p=1$ and $f(n)=\Theta(n)$. Each level costs $\Theta(n)$, and there are $\Theta(\log n)$ levels, yielding $\Theta(n\log n)$.

The extended logarithmic form also handles

$$
T(n)=2T(n/2)+n\log^k n
$$

for fixed $k\ge0$, producing $\Theta(n\log^{k+1}n)$. State which Master theorem version is being used; textbooks differ in the breadth of case 2 they present.

### Case 3: root work dominates, with regularity

For

$$
T(n)=2T(n/2)+n^2,
$$

$p=1$ and $f(n)=n^2=\Omega(n^{1+1})$. Moreover,

$$
2f(n/2)=2(n/2)^2=\frac12n^2,
$$

so regularity holds with $c=1/2$. Level work shrinks geometrically and $T(n)=\Theta(n^2)$.

The regularity condition prevents $f$ from being asymptotically large at the root while recurring subproblem values spike enough to dominate. Do not omit it because a polynomial example happens to satisfy it automatically.

### Recurrences outside the Master template

The Master Method does not directly solve:

- $T(n)=T(n-1)+f(n)$ (additive rather than multiplicative shrinkage);
- $T(n)=T(n/3)+T(2n/3)+n$ (unequal subproblem sizes);
- $T(n)=nT(n/2)+f(n)$ (nonconstant branching);
- data-dependent recurrences whose split distribution must be maximized or averaged;
- mutually recursive cost systems without reduction to the template;
- recurrences with negative/oscillatory work that violate nonnegativity assumptions.

Use unrolling, substitution, a recursion tree with variable sizes, a change of variables, probabilistic conditioning, generating functions, Akra–Bazzi, or another justified result.

### Akra–Bazzi covers eligible unequal splits

For a broad class

$$
T(x)=\sum_{i=1}^{k}a_iT(b_ix+h_i(x))+g(x),
$$

with constants $a_i>0$, $0<b_i<1$, controlled perturbations $h_i$, and suitable regularity, let $p$ solve

$$
\sum_{i=1}^{k}a_ib_i^p=1.
$$

Then the Akra–Bazzi result has the form

$$
T(x)=\Theta\left(
x^p\left(1+\int_1^x\frac{g(u)}{u^{p+1}}\,du\right)
\right).
$$

For $T(n)=T(n/3)+T(2n/3)+n$, $p=1$ because $1/3+2/3=1$. The integral is $\int_1^n du/u=\log n$, giving $\Theta(n\log n)$. This invocation is conditional on the theorem's technical hypotheses and appropriate rounding treatment; it is not a license for arbitrary recurrences.

### Expected recurrences condition on random choices

Randomized quicksort does not always split evenly. A correct expected recurrence conditions on pivot rank and averages subproblem costs under the randomness model. Replacing it with $2T(n/2)+\Theta(n)$ assumes the conclusion's balance rather than deriving it.

More generally, apply the law of total expectation:

$$
\mathbb{E}[T(n)]
=\sum_r\Pr[R=r]\,
\mathbb{E}[T(n)\mid R=r].
$$

The distribution, independence, adversary timing, and whether recursive subproblems retain the same probabilistic model are proof obligations. ALGE-006 owns the quantifier distinction; later randomized modules develop full analyses.

### Work, span, and peak space obey different recurrences

If two recursive calls execute sequentially, work adds both:

$$
W(n)=2W(n/2)+\Theta(n).
$$

If they can execute in parallel after $\Theta(1)$ spawn work and combine in $\Theta(n)$ sequential span, a simplified span recurrence follows the longer child:

$$
S(n)=S(n/2)+\Theta(n),
$$

which is $\Theta(n)$, even though work is $\Theta(n\log n)$. A parallel combine could produce another span.

Peak auxiliary space also follows liveness. Sequential child calls can reuse stack/workspace, so sibling peaks use a maximum. Merge sort allocating an $\Theta(n)$ temporary at the current level can satisfy

$$
M(n)=M(n/2)+\Theta(n)=\Theta(n),
$$

not $2M(n/2)+\Theta(n)$. If both children run concurrently and each retains separate storage, their spaces may coexist. Specify allocation/release order and output ownership.

### Cutoffs and hybrid implementations alter exact recurrences

Real divide-and-conquer code stops at threshold $k$ and calls an iterative base routine. Then

$$
T(n)=aT(n/b)+f(n)\quad\text{for }n>k,
$$

with base cost $B(n)$ for $n\le k$. A constant $k$ often preserves the asymptotic class but changes depth and constants. If $k$ grows with $n$, the class may change.

Cutoffs affect stack depth, cache behavior, vectorization, task overhead, and partition imbalance. Record them in exact/correspondence analysis even when asymptotic notation suppresses them.

### Validate both the solution and the recurrence

Check a proposed solution by substitution, independent summation, or symbolic algebra. Then instrument the implementation with deterministic counters: number and sizes of calls, local operations, base hits, allocation peaks, and span dependencies. Test empty, threshold-adjacent, power-of-$b$, non-power, balanced, and pathological inputs.

Counters can refute a recurrence-to-code mapping. They do not prove the mapping for all inputs unless paired with control-flow reasoning. Wall-clock measurements add compiler, runtime, cache, scheduler, and system effects and belong to ALGE-010.

### Executable evidence verifies one exact recurrence identity

This model evaluates $T(1)=0$ and $T(n)=2T(n/2)+n$ for powers of two, then checks the closed form $T(n)=n\log_2 n$.

<!-- bijux-verify: {"id":"balanced-recurrence-identity","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"n=1 work=0\nn=2 work=2\nn=4 work=8\nn=8 work=24\nn=16 work=64\nn=1024 work=10240\nchecked=11\nidentity=True\n","stderr":""}} -->
```python
def recurrence(size):
    assert size >= 1 and size & (size - 1) == 0
    if size == 1:
        return 0
    return 2 * recurrence(size // 2) + size


for size in (1, 2, 4, 8, 16, 1024):
    print(f"n={size} work={recurrence(size)}")

checked = 0
identity = True
for exponent in range(11):
    size = 1 << exponent
    identity &= recurrence(size) == size * exponent
    checked += 1
print(f"checked={checked}")
print(f"identity={identity}")
```

The run establishes exact values for eleven powers of two under this model. The induction or recursion-tree derivation proves the identity for all powers of two; extensions to rounded sizes and a concrete merge implementation require additional correspondence arguments.

## Definitions and Notation

- $T(n)$: selected cost summary for size $n$ under a declared case/model.
- $a$: number of recursively solved subproblems in the balanced Master template.
- $b$: constant factor by which each subproblem size shrinks.
- $f(n)$: non-recursive divide, combine, and local work at size $n$.
- $p=\log_b a$: leaf-growth exponent in the balanced recursion tree.
- $n_0$: base threshold; $B(n)$: base-routine cost.
- $W(n)$: total work; $S(n)$: span/critical-path cost; $M(n)$: peak live space.
- A **recursion-tree level** contains calls at equal recursive depth, not necessarily equal wall-clock time.
- A **tight solution** supplies matching asymptotic upper and lower bounds for the recurrence.
- A **recurrence-to-code correspondence claim** maps calls and local operations in the implementation to recurrence terms.

For floors and ceilings, an exact recurrence might be

$$
T(n)=T(\lfloor n/2\rfloor)+T(\lceil n/2\rceil)+cn,
$$

with explicit bases at $n=0,1$. Replacing both children by $T(n/2)$ is an asymptotic simplification requiring monotonicity/bounding reasoning, not exact equality.

## Mechanisms, Invariants, or Proof Structure

Use this recurrence worksheet:

1. **Resource:** choose work/time, comparisons, allocations, I/O, span, or peak live space.
2. **Case and domain:** define input/state family, size parameters, and worst/expected/other quantifiers.
3. **Base:** record every threshold branch and its bounded or exact cost.
4. **Calls:** enumerate calls actually executed; account for branches, memoization, sharing, and retries.
5. **Sizes:** derive each recursive argument, including floors, ceilings, imbalance, and strict descent.
6. **Local work:** count validation, divide, combine, allocation, copying, and output work outside calls.
7. **Recurrence:** use equality only for an exact model; otherwise state upper/lower inequalities.
8. **Method selection:** choose unrolling, tree, substitution, Master, Akra–Bazzi, conditioning, or another applicable method.
9. **Premise audit:** check constants, nonnegativity, polynomial gaps, regularity, perturbations, and base behavior.
10. **Solution proof:** derive and verify the bound, with both directions for $\Theta$.
11. **Resource semantics:** for span/space, identify dependency and liveness instead of blindly summing children.
12. **Implementation evidence:** collect call-size/local-work counters and challenge cutoff, imbalance, and failure cases.

The durable invariant is correspondence: every recurrence term has an owned implementation mechanism, and every resource-consuming mechanism appears in the recurrence or an explicitly excluded layer.

## Alternatives and Trade-Offs

**Unrolling versus substitution.** Unrolling exposes accumulated work and often suggests the answer. Substitution gives a compact inductive verification but may require a strengthened hypothesis. Use them together when stakes are high.

**Recursion tree versus Master Method.** A tree explains level mechanics and handles more variation. Master is fast and reliable inside its template. Drawing a tree reduces memorization errors; checking Master premises reduces pattern-guessing errors.

**Exact recurrence versus asymptotic inequality.** Exact formulas support constants and executable checks but become cluttered by rounding and thresholds. Upper/lower recurrences can isolate growth. Do not present a simplified bound as exact.

**Balanced template versus Akra–Bazzi.** Master is simpler for equal constant-ratio splits. Akra–Bazzi handles eligible unequal splits and perturbations at greater mathematical/premise cost. Direct trees or substitution may be clearer for one recurrence.

**Recursive versus iterative implementation.** Recursion maps naturally to recurrence trees but consumes stack and call overhead. Iteration can expose state and memory reuse. Equivalent functional behavior does not imply identical cost recurrences.

**Sequential versus parallel execution.** Work adds all tasks; span follows dependencies; peak space follows concurrency/liveness. A parallel design can reduce span while increasing scheduling work and simultaneous memory.

**Asymptotic solution versus measured model.** A recurrence proves growth under assumed costs and split behavior. Instrumentation tests the mapping and constants on finite executions. Both are needed for algorithm engineering.

## Failure Modes and Misconceptions

1. **“Recursive syntax determines the recurrence.”** Branches, memoization, sharing, and short-circuiting determine executed calls.
2. **“Base cases do not affect analysis.”** They complete the definition and can affect depth, constants, or classes when thresholds grow.
3. **“Floors never matter.”** They may not change a standard class, but exact and boundary claims require treatment.
4. **“Two recursive calls means $2T(n/2)$.”** They may have unequal sizes, be mutually exclusive, share work, or hit a cache.
5. **“Master solves every recurrence.”** It covers a specific constant-branching, constant-ratio family.
6. **“Similar-looking $f(n)$ is close enough.”** Master cases require quantified polynomial relationships.
7. **“Case 3 needs only faster $f$.”** The regularity condition is part of the theorem.
8. **“No Master case means no solution.”** Use unrolling, substitution, another theorem, or a tighter recurrence.
9. **“A recursion tree diagram is a proof.”** General level counts and the terminal sum must be derived.
10. **“Substitution finds the answer.”** It verifies a candidate; another method usually suggests it.
11. **“Proving $O$ proves $\Theta$.”** A matching lower bound is still required.
12. **“Balanced average behavior permits a balanced recurrence.”** Expected split costs must be derived by conditioning.
13. **“Parallel calls make work a maximum.”** Work still sums; span uses the dependency maximum.
14. **“Peak space sums all recursive nodes.”** Only simultaneously live storage contributes.
15. **“A recurrence solution proves code performance.”** The recurrence-to-implementation mapping remains a separate claim.
16. **“Timing slope validates the exact recurrence.”** Many models can fit a finite range; counters and proof are needed.
17. **“Retries are just another recursive call.”** Without bounded progress they can change termination and cost fundamentally.
18. **“Cutoffs only change constants.”** That is usually true only when the threshold is fixed and base work is controlled.

## Worked Examples

### Example 1

**Question:** Solve $T(n)=T(n-1)+1$ with $T(0)=1$.

**Reasoning:** After $k$ substitutions, $T(n)=T(n-k)+k$. Set $k=n$ to obtain $T(n)=T(0)+n=n+1=\Theta(n)$.

**Conclusion:** Unit work along a decrementing chain accumulates linearly.

### Example 2

**Question:** Solve $T(n)=T(n-1)+n$ with constant base cost.

**Reasoning:** Unrolling yields $T(0)+\sum_{j=1}^{n}j=T(0)+n(n+1)/2=\Theta(n^2)$.

**Conclusion:** Linear local work across a linear-depth chain produces quadratic total work.

### Example 3

**Question:** Why does binary search satisfy a logarithmic recurrence?

**Reasoning:** One comparison selects one half; both halves are not recursively searched. Thus $T(n)\le T(\lceil n/2\rceil)+c$. The upper bound follows after $O(\log n)$ halvings. An unsuccessful search, or a successful search whose key is first compared at the deepest occupied level, supplies a matching $\Omega(\log n)$ execution in the usual comparison model.

**Conclusion:** The recurrence has one child because the branch chooses one subproblem.

### Example 4

**Question:** Apply Master to $T(n)=2T(n/2)+n$.

**Reasoning:** $a=2$, $b=2$, $p=1$, and $f(n)=\Theta(n^p)$. Case 2 with $k=0$ yields $T(n)=\Theta(n\log n)$. The recursion tree confirms $\Theta(n)$ per level for $\Theta(\log n)$ levels.

**Conclusion:** Equal leaf and local-work scales make every level contribute.

### Example 5

**Question:** Solve Strassen's idealized recurrence $T(n)=7T(n/2)+\Theta(n^2)$.

**Reasoning:** $p=\log_2 7\approx2.807$. Since $n^2=O(n^{p-\epsilon})$ for any fixed $0<\epsilon\le p-2$, Master case 1 gives $\Theta(n^{\log_2 7})$.

**Conclusion:** Recursive leaves dominate the quadratic combine work.

### Example 6

**Question:** Solve $T(n)=T(n/2)+n$.

**Reasoning:** Unrolling gives $n+n/2+n/4+\cdots$, a geometric series below $2n$ and at least $n$. Hence $T(n)=\Theta(n)$. Master case 3 also applies with $a=1$, $b=2$, $p=0$, and regularity $f(n/2)=f(n)/2$.

**Conclusion:** Linear root work dominates shrinking lower levels.

### Example 7

**Question:** Solve $T(n)=2T(n/2)+1$.

**Reasoning:** Here $p=1$ and $f(n)=\Theta(1)=O(n^{1-1})$. Case 1 gives $\Theta(n)$. Equivalently, the tree has $\Theta(n)$ constant-cost leaves and fewer internal nodes of the same order.

**Conclusion:** Branching can create linear total work even with constant local work.

### Example 8

**Question:** Can Master solve $T(n)=T(n/3)+T(2n/3)+n$?

**Reasoning:** No single $aT(n/b)$ describes the unequal children. Under Akra–Bazzi, $p=1$ solves $(1/3)^p+(2/3)^p=1$; the integral contributes $\log n$, so the eligible recurrence is $\Theta(n\log n)$.

**Conclusion:** Unequal splits need a more general theorem or direct tree/substitution analysis.

### Example 9

**Question:** Why is sequential merge-sort peak workspace not necessarily $2M(n/2)+n$?

**Reasoning:** If the first child's temporary state is released/reused before the second and the current merge buffer coexists with only one child peak, liveness gives $M(n)=M(n/2)+\Theta(n)=\Theta(n)$. Parallel children or retained outputs can change coexistence.

**Conclusion:** Space recurrences follow simultaneous liveness, not total recursive work.

### Example 10

**Question:** A recursive remote fetch retries on the same request after timeout. Is $T(n)=T(n-1)+c$ justified?

**Reasoning:** No size decreases. Retry count depends on policy and environment; without a cap or probabilistic/liveness premise, termination and finite expected cost may fail. Model attempts, backoff, deadline, cancellation, idempotency, and remote outcome separately rather than inventing descent.

**Conclusion:** Recurrence well-foundedness must reflect real progress, especially across effects.

## Cross-Program Connections

- [Theory of Computation & Complexity](../../15-theory-of-computation-and-complexity/ROADMAP.md) owns formal machine resource classes and problem-level complexity.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) applies recurrences to trees, heaps, union-find, persistence, rebuilding, and layout costs.
- [Concurrent & Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies task dependencies, work/span scheduling, synchronization, and parallel space.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) explains why local cost and cutoff assumptions change with caches, vectors, and memory traffic.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) treats retries, backoff, failures, and asynchronous progress that resist naive recursive cost models.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies counter instrumentation, boundary testing, and reproducible performance evidence.

## References

1. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. [*Introduction to Algorithms*, fourth edition](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), MIT Press, 2022. Substitution, recursion trees, Master methods, and algorithm recurrences.
2. MIT OpenCourseWare 6.006. [“Recitation 3: Recurrences”](https://live.ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/1869dbf640ded6b31f1bd369d2001ef5_MIT6_006S20_r03.pdf), Spring 2020. Current course treatment of substitution, recursion trees, and the extended Master theorem.
3. Mohamad Akra and Louay Bazzi. [“On the Solution of Linear Recurrence Equations”](https://doi.org/10.1023/A:1018373005182), *Computational Optimization and Applications* 10(2), 1998, pp. 195–210. Primary generalization for unequal divide-and-conquer recurrences.
4. Ronald L. Graham, Donald E. Knuth, and Oren Patashnik. *Concrete Mathematics*, second edition. Addison-Wesley, 1994. Recurrences, finite sums, floors, asymptotics, and solution techniques.
5. Donald E. Knuth. *The Art of Computer Programming, Volume 1: Fundamental Algorithms*, third edition. Addison-Wesley, 1997. Mathematical analysis of recursive algorithms and recurrences.
6. Robert Sedgewick and Philippe Flajolet. *An Introduction to the Analysis of Algorithms*, second edition. Addison-Wesley, 2013. Recurrences, generating functions, asymptotic methods, and algorithm analysis.
7. ACM, IEEE Computer Society, and AAAI. [*Computer Science Curricula 2023: Algorithmic Foundations*](https://csed.acm.org/al-cs-core/), endorsed 2024; consulted 2026-09-04. Current curricular scope for recursive analysis, recurrence relations, substitution, and the Master theorem.

## Exercises

### Exercise 1

Solve $T(0)=3$ and $T(n)=T(n-1)+2n$ exactly, then prove a tight asymptotic bound.

### Exercise 2

For each recurrence, state whether the displayed Master theorem applies, identify the case, and give a tight bound: (a) $2T(n/2)+1$; (b) $2T(n/2)+n\log^2 n$; (c) $2T(n/2)+n^3$; (d) $T(n-1)+n$.

### Exercise 3

Use both a recursion tree and substitution to prove a tight bound for $T(n)=3T(n/2)+n$ on powers of two with positive constant base cost.

### Exercise 4

Diagnose a review that claims a recursive algorithm has both time and space $2R(n/2)+n$ merely because it makes two recursive calls and allocates an $n$-element combine buffer. Give the conditions under which the time equation and space equation differ.

### Exercise 5

An unfamiliar parallel partitioner scans $n$ records, creates subproblems of sizes $\alpha n$ and $(1-\alpha)n$, may retry a failed partition, and retains buffers until both tasks join. Design work, span, and peak-space recurrences or inequalities, state when Master/Akra–Bazzi applies, and specify implementation evidence needed to trust the model.

## Answers to the Exercises

### Answer 1

Unroll:

$$
T(n)=3+\sum_{j=1}^{n}2j
=3+n(n+1)
=n^2+n+3.
$$

For $n\ge1$, $n^2\le T(n)\le5n^2$, so $T(n)=\Theta(n^2)$. The exact result can also be proved by induction: substitute $n-1$ into $(n-1)^2+(n-1)+3$, then add $2n$ and simplify.

### Answer 2

(a) $a=b=2$, $p=1$, and $f=\Theta(1)$ is polynomially smaller, so case 1 gives $\Theta(n)$. (b) $f=\Theta(n^p\log^2 n)$, so extended case 2 with $k=2$ gives $\Theta(n\log^3 n)$. (c) $n^3$ is polynomially larger than $n$; regularity holds because $2(n/2)^3=n^3/4$, so case 3 gives $\Theta(n^3)$. (d) does not have constant-factor size reduction and is outside the Master template; unrolling gives $\Theta(n^2)$.

All claims require appropriate constant bases and rounding/bounded-base treatment.

### Answer 3

At level $i$, there are $3^i$ nodes of size $n/2^i$, so local work is

$$
3^i\frac{n}{2^i}=n(3/2)^i.
$$

The leaves occur at depth $h=\log_2 n$, after $h$ internal levels, and their count is $3^h=n^{\log_2 3}$. The geometric internal-level sum is dominated by its final scale, so $T(n)=\Theta(n^{\log_2 3})$.

For substitution, let $p=\log_2 3$. For an upper bound assume $T(m)\le cm^p-dm$ for smaller powers of two, where $d>0$. Then

$$
T(n)
\le3\left(c(n/2)^p-dn/2\right)+n
=cn^p+(1-3d/2)n
\le cn^p-dn
$$

when $d\ge2$. Choose $c$ to cover the base. A corresponding lower bound follows from the $n^p$ leaves with constant positive base cost, or an inductive lower inequality. Thus the tight class follows independently of Master case 1.

### Answer 4

The time/work recurrence is $2T(n/2)+\Theta(n)$ only if both calls always execute, each processes a half-size problem without memoized sharing, and scanning/combining costs linear work. Branch selection, unequal sizes, overlap, cache hits, or failed/repeated calls change it.

Peak space depends on liveness. If children execute sequentially, child workspace is released or reused, and the current $\Theta(n)$ buffer coexists with at most one child peak, then $M(n)=M(n/2)+\Theta(n)=\Theta(n)$. If both children run concurrently with separate workspaces while the parent buffer remains live, a sum such as $M(n)\le2M(n/2)+\Theta(n)$ may be appropriate, giving $O(n\log n)$ under that allocation model. Returned child outputs, sharing, buffer slicing, and allocator/runtime storage must be specified.

### Answer 5

Let one successful partition do $g(n)=\Theta(n)$ work and have span $s(n)$ (linear for a serial scan, potentially smaller for a parallel scan). For deterministic split ratio bounded away from zero and one, successful work can satisfy

$$
W(n)\le W(\lceil\alpha n\rceil)+W(\lceil(1-\alpha)n\rceil)+g(n).
$$

Span with parallel children follows

$$
S(n)\le\max\{S(\lceil\alpha n\rceil),S(\lceil(1-\alpha)n\rceil)\}+s(n)+s_{join}(n).
$$

If parent and both child buffers coexist, a safe recurrence may be $M(n)\le M(\lceil\alpha n\rceil)+M(\lceil(1-\alpha)n\rceil)+\Theta(n)$. If storage is partitioned into disjoint views or released incrementally, use the actual ownership/lifetime graph instead. Retained output also counts according to the space convention.

The equal-split Master theorem applies only when the calls reduce to a constant number of essentially equal $n/b$ sizes and local costs meet a case. Fixed unequal constant ratios may fit Akra–Bazzi; data-dependent $\alpha$, unbounded imbalance, variable branching, or irregular perturbations require worst-case maximization, conditioning, or direct analysis.

Retries add another dimension. A hard cap gives a multiplicative/additive bound and a failure outcome. An expectation needs an explicit failure probability, dependence model, and adversary/environment assumptions. Unbounded retries may destroy termination or finite expectation. Validate base/cutoff cases, call and split-size traces, actual retry counts, progress/cancellation, buffer lifetimes, work/span counters, scheduler overhead, peak memory, all-equal/pathological partitions, failure injection, and correspondence on non-power sizes. Report theorem and measurements separately.
