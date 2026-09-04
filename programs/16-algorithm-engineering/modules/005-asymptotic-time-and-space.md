---
module_id: ALGE-005
program: Algorithm Engineering
level: 1
module_number: 5
title: Asymptotic Time and Space
status: complete
last_verified: 2026-09-04
---

# Asymptotic Time and Space

## One-Page Review

### Governing question

How can an engineer describe how an algorithm's time and storage requirements grow with input size while preserving the quantifiers, cost model, size parameters, and practical limits that make the claim meaningful?

### Essential definitions

- An **input-size measure** maps an admitted input to one or more nonnegative parameters, such as sequence length $n$, graph dimensions $(|V|,|E|)$, or binary encoding length $b$.
- A **cost model** assigns abstract cost to selected primitive operations; a time or space function is meaningless without one.
- $f\in O(g)$ is an eventual asymptotic upper bound, $f\in\Omega(g)$ is an eventual lower bound, and $f\in\Theta(g)$ is a tight bound in both directions.
- $f\in o(g)$ means $f$ grows strictly more slowly than $g$; $f\in\omega(g)$ means it grows strictly faster.
- **worst-, best-, and expected-case functions** quantify over inputs or randomness; asymptotic notation can bound any of them and does not itself name the case.
- **auxiliary space** excludes storage occupied by the supplied input and required output under a declared convention; **total space** includes them.
- **output-sensitive analysis** retains output size as a parameter when producing the output already requires nonconstant work or space.
- A **tight bound** describes an analyzed function, not necessarily the smallest possible complexity among all algorithms for the problem.

### Central model, mechanism, or theorem

For eventually nonnegative functions $f,g:\mathbb{N}\to\mathbb{R}_{\ge0}$ with $g$ eventually positive,

$$
f\in\Theta(g)
\iff
\exists c_1,c_2>0\;\exists n_0\;\forall n\ge n_0:
c_1g(n)\le f(n)\le c_2g(n).
$$

Derive a cost function from the algorithm and model first; only then bound it. For example,

$$
T(n)=3n^2+7n+20
$$

satisfies $3n^2\le T(n)\le30n^2$ for every $n\ge1$, so $T\in\Theta(n^2)$. The constants prove the claim; dropping terms is a consequence, not the proof rule.

### Critical invariants

- Name the algorithm, admitted input family, size parameters, case/quantifier, and primitive operation before giving a bound.
- Do not equate $O$ with exact or tight complexity; state $\Theta$ when both bounds are established.
- Do not equate $O$, $\Omega$, and $\Theta$ with worst, best, and average cases.
- Measure encoded input length rather than numeric magnitude when representation length controls work.
- Keep multiple independent parameters when collapsing them would hide sparse, dense, skewed, or output-heavy regimes.
- Count stack frames, temporary buffers, live copies, and required output according to a stated space convention.
- Separate peak live space from cumulative allocation and physical process memory.
- Treat constant-time primitives, word size, arithmetic, comparison, allocation, and I/O as model assumptions.
- Use asymptotics to compare growth; use exact analysis and measurement to evaluate finite regimes.
- Never infer a lower bound for a problem merely from the running time of one implementation.

### Common failures

Common failures include saying “the algorithm is Big-O” without naming a function; using $O$ to mean equality; calling $\Omega$ the best case; hiding graph density in one $n$; analyzing an integer by its value rather than its bit length; dropping an output-size term; claiming recursive code uses constant space because it allocates no collection; counting cumulative allocation as peak space; treating a library operation as constant without its contract; comparing bounds from different models; applying a limit ratio when its hypotheses fail; extrapolating finite timings into a theorem; and assuming a better bound always wins for real workloads.

### Compact example

A routine scans $n$ records and emits every matching pair. If it compares all unordered pairs, its comparison count is

$$
\sum_{i=0}^{n-1}(n-i-1)=\frac{n(n-1)}{2}\in\Theta(n^2).
$$

If it materializes $k$ matches, total output storage is $\Theta(k)$ even when its working state is $\Theta(1)$. Report comparison time $\Theta(n^2)$, auxiliary space $\Theta(1)$, and total additional storage $\Theta(k)$ rather than the ambiguous phrase “quadratic algorithm.”

### Connections

[ALGE-001](./001-problem-statements-inputs-outputs-and-constraints.md) defines inputs and size parameters. [ALGE-002](./002-preconditions-postconditions-and-correctness.md) defines the admitted domain, and [ALGE-004](./004-inductive-correctness-proofs.md) supplies proof structure. [ALGE-006](../ROADMAP.md) separates best, worst, expected, and amortized costs; ALGE-009 and ALGE-010 add machine models and measurement.

## Governing Question

An algorithm may be correct for every admitted input yet become unusable as instances grow. How should we state and prove a resource-growth claim that transfers beyond one example or computer without pretending that constants, representations, and machines do not matter?

Asymptotic analysis answers an eventual-growth question. It starts with a mathematical cost function under a declared model, then compares that function with a simpler reference function once inputs are sufficiently large. It does not measure seconds, bytes, energy, or service-level latency by itself. Its value is that it exposes scalable structure: an extra nested traversal, an output term, dependence on graph density, or exponential growth that finite examples can hide.

## Why This Matters

Resource growth determines feasibility. A quadratic comparison routine may be excellent for a dozen records and impossible for a billion. A linear-time streaming pass may still fail if it retains all outputs. An algorithm polynomial in a numeric value may be exponential in the number of bits used to encode that value. These distinctions affect architecture, capacity, cost, energy, safety margins, and denial-of-service exposure.

Asymptotic notation also creates unusually persistent misunderstandings. “Big-O” is often used as a synonym for runtime, worst case, or a tight bound, though it means none of those alone. Such imprecision can turn a valid theorem into an invalid engineering conclusion. The remedy is not to abandon asymptotics but to attach every bound to its function, quantifiers, parameters, and cost model.

The eventual view is deliberately incomplete. It suppresses constants and lower-order terms, so it cannot predict a crossover or production latency. Algorithm engineering combines asymptotic proof with exact counting, machine-aware analysis, and controlled measurement. This module establishes the growth layer cleanly so later evidence can be combined without category errors.

## Prerequisites and Retrieval

Retrieve:

- functions, sets, implication, universal and existential quantification;
- inequalities, absolute value, sums, products, powers, logarithms, limits, and basic algebra;
- sequence, graph, integer, matrix, and encoded-input representations;
- loops, recursion, call stacks, allocation, input, output, and live storage;
- algorithm contracts, admitted inputs, correctness cases, and exact operation counting;
- proof by inequality, induction, and counterexample.

From ALGE-001, recall that size is a modeling choice: an integer's magnitude and its encoding length are different quantities. From ALGE-004, recall that an inductive proof must state its predicate and domain. An asymptotic proof has the same discipline: state the compared functions and quantify the witnesses.

## Learning Objectives

After completing this module, you should be able to:

1. define input-size parameters and a model-relative time or space function;
2. state $O$, $\Omega$, $\Theta$, $o$, and $\omega$ with correct quantifiers;
3. prove elementary bounds by explicit inequalities, limits, or summation;
4. distinguish bound direction from worst, best, expected, and amortized cases;
5. simplify polynomial, logarithmic, and exponential expressions without losing relevant parameters;
6. analyze sequential statements, branches, simple and nested loops, and output production;
7. distinguish auxiliary, total, stack, peak-live, and output space;
8. recognize encoding-length and pseudopolynomial traps;
9. compare growth classes without claiming finite-machine performance from notation alone;
10. write reviewable resource claims that connect proof, implementation, and measurement honestly.

## Core Exposition

### Begin with an input family and a size function

Let $A$ be the admitted inputs from the algorithm contract. A size function $s:A\to\mathbb{N}$ groups inputs for analysis. For a sequence, $s(x)=|x|$ is often natural. For a matrix, retain rows $r$ and columns $c$ when shape matters. For a graph, retain $n=|V|$ and $m=|E|$; replacing both with “graph size” can hide the difference between a tree-like graph with $m=\Theta(n)$ and a dense graph with $m=\Theta(n^2)$.

The correct measure follows representation and question. If an integer $N$ is encoded in binary, its length is

$$
b=\lfloor\log_2 N\rfloor+1
$$

for $N\ge1$. A loop that executes $N$ times is $\Theta(N)$ in numeric magnitude but $\Theta(2^b)$ in the bit length in the worst case. Calling it “linear in the input” without naming the measure is materially misleading.

Size can be a vector. String matching may depend on text length $n$, pattern length $m$, and number of matches $k$. Sparse matrix work may depend on dimensions and nonzeros $z$. Parameterized analysis is often more useful than forcing every input into one scalar.

### Define the cost function before classifying it

Choose a cost model and a quantity. In a comparison model, count comparisons. In a word-RAM abstraction, count declared word operations under a word-size assumption. In a storage model, count peak simultaneously live words or bytes. The resulting function might be

$$
T_A(n)=\max\{steps_A(x):x\in A,\ s(x)=n\}
$$

for worst-case time, or it may be an exact cost for a fixed input. ALGE-006 develops the input and probability quantifiers. Here the key point is that $O$ can bound $T_{worst}$, $T_{best}$, $T_{expected}$, or any other well-defined nonnegative function.

An elementary statement sequence adds costs. Mutually exclusive branches use the cost of the executed branch; a worst-case function then maximizes over inputs. A loop sums iteration costs. Nested loops multiply only when each inner loop performs the same count independently; triangular or data-dependent nests require an actual sum.

### Big-O is an eventual upper-bound relation

For eventually nonnegative $f$ and eventually positive $g$,

$$
f\in O(g)
\iff
\exists c>0\;\exists n_0\in\mathbb{N}\;\forall n\ge n_0:
0\le f(n)\le cg(n).
$$

The witnesses $c$ and $n_0$ may depend on $f$ and $g$ but not on the varying $n$. The relation ignores any finite prefix. A slow startup, table initialization, or enormous constant can coexist with a small growth class.

The notation describes a set of functions, so $f\in O(g)$ is clearest. The conventional $f=O(g)$ is widespread but is not ordinary equality: $n\in O(n^2)$ while $n^2\notin O(n)$. Replacing both sides as though equality were symmetric produces invalid algebra.

An upper bound need not be tight. If $f\in\Theta(n)$, then $f\in O(n)$, $f\in O(n\log n)$, and $f\in O(n^2)$ for sufficiently large $n$. Give the tightest useful proven bound, and say when only a looser safe bound is known.

### Omega and Theta name lower and tight bounds

An eventual lower bound is

$$
f\in\Omega(g)
\iff
\exists c>0\;\exists n_0\;\forall n\ge n_0:
0\le cg(n)\le f(n).
$$

A tight bound is

$$
f\in\Theta(g)\iff f\in O(g)\land f\in\Omega(g).
$$

$\Omega$ does not mean “best case,” just as $O$ does not mean “worst case.” One may prove the worst-case cost is in both $O(n\log n)$ and $\Omega(n\log n)$, hence $\Theta(n\log n)$. One may separately show the best-case function is $\Theta(n)$. Case selection and bound direction are independent axes.

A lower bound on one implementation is also not a lower bound on the problem. Showing a particular sorting program always performs at least $n^2/4$ comparisons only describes that program. A problem lower bound must quantify over every algorithm in a declared model; ALGE-008 develops those arguments.

### Little-o and little-omega express strict separation

For nonnegative functions,

$$
f\in o(g)
\iff
\forall c>0\;\exists n_0\;\forall n\ge n_0:
0\le f(n)<cg(n).
$$

Thus $n\in o(n\log n)$ and $n\log n\in o(n^{1+\epsilon})$ for every fixed $\epsilon>0$. Conversely, $g\in\omega(f)$ expresses that $g$ eventually dominates every positive constant multiple of $f$.

When $f,g$ are eventually positive and the limit exists,

$$
\lim_{n\to\infty}\frac{f(n)}{g(n)}=
\begin{cases}
0 &\Rightarrow f\in o(g),\\
L\in(0,\infty) &\Rightarrow f\in\Theta(g),\\
\infty &\Rightarrow f\in\omega(g).
\end{cases}
$$

The limit test is convenient, not the definition. Oscillating ratios or zero denominators may defeat it even when direct inequalities establish a bound.

### Prove simplifications rather than chanting “drop constants”

For $T(n)=3n^2+7n+20$ and $n\ge1$, use $n\le n^2$ and $1\le n^2$:

$$
3n^2\le T(n)le(3+7+20)n^2=30n^2.
$$

The two inequalities prove $T\in\Theta(n^2)$. More generally, a nonzero polynomial with positive leading coefficient has the order of its highest-degree term because every lower power is eventually bounded by that power.

Logarithm bases differ by a constant:

$$
\log_a n=\frac{\log_b n}{\log_b a},
$$

so fixed valid bases give the same $\Theta(\log n)$ class. This does not allow suppressing a base that changes with $n$, nor does it erase domain and rounding choices from exact counts.

For fixed $0<\epsilon<k$ and $c>1$, standard growth ordering gives

$$
1\prec\log n\prec n^\epsilon\prec n^k\prec c^n\prec n!
$$

where $f\prec g$ here means $f\in o(g)$. Labels such as “log-linear” or “exponential” should accompany formulas; names alone can hide parameters or variable bases.

### Summations expose loop structure

A loop with $n$ iterations and constant modeled work per iteration has $\Theta(n)$ time. Two independent length-$n$ loops in sequence take $\Theta(n+n)=\Theta(n)$, not $\Theta(n^2)$. A fully nested pair takes $\Theta(n^2)$ if the inner loop executes $n$ times for every outer iteration.

For a triangular nest,

$$
\sum_{i=0}^{n-1}(n-i-1)
=\sum_{j=0}^{n-1}j
=\frac{n(n-1)}{2}
\in\Theta(n^2).
$$

If an inner loop doubles an index until it reaches $n$, its iteration count is $\lfloor\log_2 n\rfloor+1$ for positive $n$. If that loop occurs for every one of $n$ outer iterations, the total is $\Theta(n\log n)$. Derive ranges and boundary counts before simplifying.

### Preserve independent and output parameters

Breadth-first traversal with adjacency lists is conventionally $\Theta(n+m)$ for $n$ vertices and $m$ edges under a suitable model. Writing $O(n^2)$ may be a valid upper bound for simple dense graphs, but it discards the sparse-graph result that makes the representation useful.

An algorithm that reports $k$ items needs $\Omega(k)$ time merely to emit them under a unit-output model and $\Omega(k)$ storage if it materializes them. A range-reporting query might therefore be $\Theta(\log n+k)$ rather than “logarithmic.” If results stream to a consumer, auxiliary storage may remain small, but output transfer time does not disappear.

Parameters may be related by the input contract. For a simple undirected graph, $0\le m\le n(n-1)/2$. Substitute such relationships only when the targeted workload/domain warrants it, and keep the more informative multivariate form when sparse and dense regimes both matter.

### Time and space need separate conventions

Time complexity counts modeled work; space complexity usually reports a maximum amount simultaneously live during an execution. Define what is included:

- **input space:** representation supplied to the algorithm;
- **output space:** representation required for the result;
- **auxiliary space:** additional working state beyond input and required output;
- **stack space:** live call frames, whether explicit or runtime-managed;
- **total space:** all included live storage under the chosen boundary.

An iterative summation may use $\Theta(1)$ auxiliary words. A recursive predecessor summation has $\Theta(n)$ stack frames unless a specified implementation eliminates them. A transformation returning a new length-$n$ sequence needs $\Theta(n)$ output space even if its auxiliary working state is $\Theta(1)$.

Peak live space is not cumulative allocated bytes. A loop may allocate and release one buffer $n$ times: cumulative allocation can be $\Theta(n)$ buffers while peak coexistence remains $\Theta(1)$. Conversely, a resize can briefly retain old and new arrays simultaneously. Resident process memory additionally includes allocator, runtime, code, shared pages, and operating-system policy; it is not an asymptotic object-space proof.

### Encoding length prevents pseudopolynomial confusion

Suppose dynamic programming uses a table indexed from $0$ through integer capacity $W$. A bound $\Theta(nW)$ is polynomial in numeric parameters $n$ and $W$, but $W$ may require only $b=\Theta(\log W)$ bits. In terms of encoded input length, $W$ can be exponential in $b$. Such a running time is called pseudopolynomial, not polynomial in the ordinary bit-input sense.

The same issue affects arithmetic. Treating addition, multiplication, or comparison of arbitrarily large integers as constant time is a unit-cost assumption. A bit-cost model includes operand lengths. ALGE-009 studies how models change conclusions; here, always state which size and primitive assumptions support the formula.

### Composition rules require their premises

For nonnegative functions, asymptotic bounds are transitive: if $f\in O(g)$ and $g\in O(h)$, then $f\in O(h)$. Sums satisfy $O(f)+O(g)\subseteq O(f+g)$, which often simplifies to the dominating term when functions are comparable and nonnegative. Products multiply bounds under corresponding assumptions.

Composition is subtler. From $f\in O(g)$ one cannot blindly conclude $f(h(n))\in O(g(h(n)))$ unless $h$ eventually stays in the quantified domain and relevant positivity/monotonicity conditions hold. Likewise, cancellation and subtraction can destroy nonnegativity. When algebra becomes delicate, return to explicit witnesses.

### Asymptotic superiority is eventual, not immediate

If $T_A(n)=10^6n$ and $T_B(n)=n^2$, then $A$ grows more slowly but $B$ is smaller for a large finite range. Asymptotics guarantees an eventual ordering, not the crossover point, hardware behavior, or constant stability. Exact counting can estimate a model crossover; controlled measurement checks a concrete implementation and workload.

This limitation is a feature. The growth class isolates scalability from transient engineering details. The complete decision needs both: eliminate algorithms whose growth cannot meet projected scale, then compare feasible candidates using relevant constants, locality, parallelism, memory traffic, implementation risk, and measured distributions.

### Executable evidence checks a model, not a theorem

The program below implements an artificial exact-cost counter with $20$ setup units, $7$ units per input item, and $3$ units for each ordered pair. It checks the derived formula and finite witness inequalities for $0\le n\le256$.

<!-- bijux-verify: {"id":"polynomial-cost-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"n=0 cost=20\nn=1 cost=30\nn=2 cost=46\nn=5 cost=130\nn=10 cost=390\nchecked=257\nfinite_theta_witness=True\n","stderr":""}} -->
```python
def modeled_cost(size):
    assert size >= 0
    cost = 20
    for _ in range(size):
        cost += 7
    for _ in range(size):
        for _ in range(size):
            cost += 3
    return cost


for size in (0, 1, 2, 5, 10):
    print(f"n={size} cost={modeled_cost(size)}")

checked = 0
finite_theta_witness = True
for size in range(257):
    actual = modeled_cost(size)
    assert actual == 3 * size * size + 7 * size + 20
    if size >= 1:
        finite_theta_witness &= 3 * size * size <= actual <= 30 * size * size
    checked += 1

print(f"checked={checked}")
print(f"finite_theta_witness={finite_theta_witness}")
```

The run can catch an implementation/counting mismatch for the checked sizes. The universal $\Theta(n^2)$ result comes from the algebraic inequalities for every $n\ge1$, not from stopping the enumeration at 256.

## Definitions and Notation

Let $A_n=\{x\in A:s(x)=n\}$ be admitted inputs of size $n$. Let $C_A(x)$ be cost of algorithm $A$ on input $x$ in the declared model. Common case functions include

$$
T_{worst}(n)=\sup_{x\in A_n}C_A(x),
\qquad
T_{best}(n)=\inf_{x\in A_n}C_A(x).
$$

Use maximum/minimum when finite sets and attained values justify them. Expected functions require an explicit distribution or algorithmic random variable, developed in ALGE-006.

For eventually nonnegative functions:

$$
O(g)=\{f:\exists c>0,n_0\;\forall n\ge n_0, 0\le f(n)\le cg(n)\},
$$

$$
\Omega(g)=\{f:\exists c>0,n_0\;\forall n\ge n_0, 0\le cg(n)\le f(n)\},
$$

$$
\Theta(g)=O(g)\cap\Omega(g).
$$

$o(g)$ and $\omega(g)$ replace existence of one multiplicative constant with domination for every positive constant. The asymptotic equivalence $f\sim g$ means $\lim f(n)/g(n)=1$ when defined; it is stronger than $f\in\Theta(g)$.

For multivariate functions, state the limiting regime. A bound as both $n,m\to\infty$ can differ from a bound uniform in $m$ for each $n$. Prefer an explicit quantified domain, such as all $n\ge n_0$ and $0\le m\le n^2$, when uniformity matters.

For space, let $L_x(t)$ be included live storage at execution point $t$. Then peak space on input $x$ is

$$
S_A(x)=\max_t L_x(t).
$$

The ownership boundary and inclusion of input, output, stack, runtime, and allocator metadata must accompany the definition.

## Mechanisms, Invariants, or Proof Structure

Use this analysis worksheet:

1. **Contract and domain:** identify admitted inputs, outputs, and exceptional paths.
2. **Size parameters:** define representation-based scalar or vector sizes and their relationships.
3. **Cost model:** name counted operations or live-storage units and their assumed costs.
4. **Case function:** state whether the analyzed function is exact, fixed-input, worst, best, expected, or sequence-based.
5. **Control decomposition:** add sequential costs, select branch costs, and write sums for loops/recursion.
6. **Exact or bounded expression:** keep endpoints, output terms, and independent parameters long enough to avoid off-by-one and regime errors.
7. **Upper proof:** exhibit constants and a threshold, or use a theorem whose premises are checked.
8. **Lower proof:** exhibit a matching lower inequality when claiming tightness.
9. **Space liveness:** identify which objects coexist at the peak instead of totaling every allocation.
10. **Representation audit:** translate numeric magnitude to encoding length and include stack/output conventions.
11. **Scope statement:** list arithmetic, word, library, allocator, I/O, and environment assumptions.
12. **Engineering bridge:** retain exact counts and measure concrete implementations separately for finite-scale choice.

Proof techniques include direct inequalities, limit ratios, dominance lemmas, summation identities, induction over loop counts, and charging each object/event a bounded number of times. Any technique must ultimately discharge the quantifiers in the claimed relation.

For a direct $O$ proof, choose plausible $c,n_0$, then verify the inequality for every $n\ge n_0$. To refute $f\in O(g)$, show that for every proposed $c,n_0$ there exists a later $n$ with $f(n)>cg(n)$; an unbounded ratio often supplies that witness.

## Alternatives and Trade-Offs

**Exact counts versus asymptotic bounds.** Exact formulas retain constants and boundaries but bind tightly to one model and implementation. Asymptotic classes transfer the dominant growth structure but suppress finite crossovers. Preserve both when the exact count is available.

**Single versus multiple parameters.** One parameter simplifies comparison and communication. Multiple parameters reveal sparsity, shape, key length, output volume, and skew. Collapse only under a justified domain relationship.

**Worst-case versus other case functions.** Worst-case supports a hard model-relative upper guarantee. Best, average, expected, high-probability, and amortized functions answer different workload or sequence questions. ALGE-006 treats their evidence and assumptions.

**Auxiliary versus total space.** Auxiliary space highlights working-memory efficiency. Total space exposes unavoidable input/output and can better support capacity planning. State both when either interpretation could change a decision.

**Unit-cost versus bit-cost analysis.** Word-level models make ordinary array and graph algorithms tractable to analyze. Bit models reveal large-integer and encoding costs. Choose the abstraction that preserves the resource bottleneck and admissible operand sizes.

**Materialized versus streamed output.** Materialization simplifies random access and ownership but incurs $\Theta(k)$ output storage. Streaming may use bounded auxiliary memory but retains output time, backpressure, failure, and consumer-liveness concerns.

**Growth-optimal versus finite-regime choice.** A better growth class protects scaling. A simpler higher-order algorithm can win for bounded inputs through small constants, locality, or implementation maturity. Define projected regimes and retain a safe switch or review threshold.

## Failure Modes and Misconceptions

1. **“The algorithm is $O(n)$.”** A bound applies to a defined cost function, not to code without domain, size, case, and model.
2. **“Big-O means exact complexity.”** It is an upper relation; use $\Theta$ for a proved tight class.
3. **“Omega means best case.”** Bound direction and input-case quantifier are independent.
4. **“Ignore constants means constants never matter.”** They do not change a fixed asymptotic class but can dominate finite operation.
5. **“Two loops imply quadratic.”** Sequential loops add; nested iteration ranges must be summed.
6. **“Nested loops are always quadratic.”** Inner work may be logarithmic, shrinking, disjoint across iterations, or dependent on another parameter.
7. **“Log base never matters.”** Fixed bases differ asymptotically by a constant; variable bases and exact counts can differ materially.
8. **“An integer input has size $N$.”** Its encoded size may be $\Theta(\log N)$.
9. **“Polynomial in a numeric capacity is polynomial time.”** It may be pseudopolynomial in bit length.
10. **“$O(n+m)$ and $O(n^2)$ say the same thing for graphs.”** The latter hides sparse behavior and may be only a loose domain-derived bound.
11. **“Output is free.”** Emitting or materializing $k$ results costs at least according to the output model.
12. **“No heap allocation means constant space.”** Recursion, stacks, runtime temporaries, and output still count under their conventions.
13. **“Allocated bytes equal space complexity.”** Space is typically peak live storage, not cumulative churn.
14. **“A finite benchmark proves $\Theta$.”** It samples one implementation and range; asymptotic claims require quantified argument.
15. **“A lower bound for my code is a problem lower bound.”** The latter quantifies over all algorithms in a model.
16. **“A smaller class is automatically faster.”** Eventual dominance does not identify the finite crossover or machine behavior.
17. **“Library calls are constant because they occupy one line.”** Their cost follows data, representation, and library contracts.
18. **“Space and time use the same size convention automatically.”** Each claim must state included inputs, outputs, stack, and live-storage boundary.

## Worked Examples

### Example 1

**Question:** Prove $5n+12\in\Theta(n)$.

**Reasoning:** For $n\ge1$, $5n\le5n+12\le17n$. The lower witness is $c_1=5$, the upper witness is $c_2=17$, and $n_0=1$ works for both.

**Conclusion:** Explicit constants establish the tight linear bound.

### Example 2

**Question:** Is $n\in O(n^2)$, and does that make “$n=O(n^2)$” an equality?

**Reasoning:** For $n\ge1$, $n\le n^2$, so membership holds with $c=1$. But $n^2\notin O(n)$ because $n^2/(cn)=n/c$ exceeds one for sufficiently large $n$. The relation is not symmetric.

**Conclusion:** Conventional equals-sign notation denotes set membership, not algebraic equality.

### Example 3

**Question:** What is the time of two consecutive scans of a length-$n$ array?

**Reasoning:** If each scan performs at most $an+b$ and $cn+d$ modeled operations, their sum is $(a+c)n+(b+d)\in\Theta(n)$ when each must inspect all elements. Multiplying the two lengths would incorrectly model nesting.

**Conclusion:** Sequential costs add, and linear plus linear remains linear.

### Example 4

**Question:** Analyze `for i in range(n): for j in range(i): visit(i,j)`.

**Reasoning:** The inner body executes $\sum_{i=0}^{n-1}i=n(n-1)/2$ times. For $n\ge2$, this lies between $n^2/4$ and $n^2/2$, so it is $\Theta(n^2)$.

**Conclusion:** A triangular nest is quadratic, established by its sum rather than loop appearance.

### Example 5

**Question:** Why is binary search logarithmic under its comparison model?

**Reasoning:** Each nonterminal comparison reduces the unresolved interval to at most half. After $k$ reductions its size is at most $n/2^k$; reaching size at most one requires $k\ge\log_2 n$. Matching upper and lower comparison arguments give $\Theta(\log n)$ worst-case unsuccessful-search cost under the usual implementation conventions.

**Conclusion:** Multiplicative shrinkage produces logarithmic depth.

### Example 6

**Question:** Can a graph traversal be summarized as $O(n)$?

**Reasoning:** With adjacency lists, initializing vertex state costs $\Theta(n)$ and scanning adjacency entries costs $\Theta(m)$, giving $\Theta(n+m)$ for a full traversal. Calling it linear is acceptable only if “input size” explicitly means the representation length proportional to $n+m$.

**Conclusion:** Preserve vertex and edge parameters or define the combined representation size.

### Example 7

**Question:** A function returns a copied array of length $n$ using only an index and accumulator variable. Is its space $\Theta(1)$?

**Reasoning:** Its auxiliary working state may be $\Theta(1)$, but the required returned array is $\Theta(n)$. If old and new arrays coexist, the algorithm's additional output allocation is linear and total live storage includes both according to the boundary.

**Conclusion:** Report auxiliary and output/total space separately.

### Example 8

**Question:** A loop counts from $1$ to numeric input $N$. Is it linear-time?

**Reasoning:** It is $\Theta(N)$ in magnitude. A binary encoding has $b=\Theta(\log N)$ bits, so worst-case work as a function of $b$ is $\Theta(2^b)$. Both formulas can be true, but only the second describes ordinary encoded-input scalability.

**Conclusion:** Complexity depends on the selected representation-based size measure.

### Example 9

**Question:** Algorithm A takes $10^6n$ model steps and B takes $n^2$. Which should run for $n=1{,}000$?

**Reasoning:** The model counts are $10^9$ for A and $10^6$ for B, so B wins at that size despite worse growth. Their positive crossover is $n=10^6$. Machine effects can move it, so measure implementations after confirming the modeled candidates satisfy the same contract.

**Conclusion:** Asymptotic dominance is eventual; finite choice needs constants and evidence.

### Example 10

**Question:** A service enumerates all authorization-policy conflicts among $n$ rules. What must a production claim include beyond $O(n^2)$?

**Reasoning:** Define rule encoding and comparison cost, retain key-length and emitted-conflict count $k$, distinguish preprocessing, working memory, materialized/streamed output, and worst/adversarial inputs, and state overflow, cancellation, memory, and partial-result behavior. Measure representative and hostile distributions under the target implementation. Security and policy owners must validate whether the conflict semantics are complete; asymptotic analysis does not authorize access decisions.

**Conclusion:** A growth bound is one component of a resource and assurance contract.

## Cross-Program Connections

- [Theory of Computation & Complexity](../../15-theory-of-computation-and-complexity/ROADMAP.md) owns complexity classes, machine-independent tractability, reductions, and problem lower bounds.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) applies time, space, allocation, and workload analysis to concrete representations.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) explains pipelines, caches, memory traffic, and hardware effects hidden by abstract operations.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies virtual memory, stacks, residency, scheduling, and process resource accounting.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) treats adversarial complexity and resource exhaustion as attack surfaces.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies benchmark design and evidence interpretation for concrete implementations.

## References

1. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. [*Introduction to Algorithms*, fourth edition](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), MIT Press, 2022. Growth notation, analysis conventions, summations, and algorithmic resource bounds.
2. Donald E. Knuth. [“Big Omicron and Big Omega and Big Theta”](https://doi.org/10.1145/1008328.1008329), *ACM SIGACT News* 8(2), 1976, pp. 18–24. Primary historical and notational treatment.
3. MIT OpenCourseWare 6.006. [“Asymptotic Complexity” recitation notes](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/ce8348ec64dce3841ced6a9d0c9e48f2_MIT6_006F11_rec01.pdf), 2011. Formal bounds and algorithm examples.
4. Paul E. Black, ed. [“big-O notation,” *Dictionary of Algorithms and Data Structures*](https://xlinux.nist.gov/dads/HTML/bigOnotation.html), NIST, revised 2019. Formal upper-bound definition and terminology.
5. NIST Digital Library of Mathematical Functions. [“Definitions and Elementary Properties,” §2.1](https://dlmf.nist.gov/2.1), current online edition; consulted 2026-09-04. General order symbols and asymptotic relations.
6. Ronald L. Graham, Donald E. Knuth, and Oren Patashnik. *Concrete Mathematics*, second edition. Addison-Wesley, 1994. Sums, floors, logarithms, recurrences, and asymptotic methods.
7. ACM, IEEE Computer Society, and AAAI. [*Computer Science Curricula 2023: Algorithmic Foundations*](https://csed.acm.org/al-cs-core/), endorsed 2024; consulted 2026-09-04. Current curricular scope for input size, primitive operations, time/space efficiency, and asymptotic complexity.

## Exercises

### Exercise 1

State the formal definitions of $O(g)$, $\Omega(g)$, and $\Theta(g)$ for eventually nonnegative functions. Explain why $4n+9$ belongs to both $O(n^2)$ and $\Theta(n)$ without contradiction.

### Exercise 2

Derive a tight count and asymptotic bound for a routine whose outer loop uses $i=1,2,\ldots,n$ and whose inner body executes $2i+1$ times. Show intermediate summation steps and explicit $\Theta$ witnesses.

### Exercise 3

Diagnose the claim: “This recursive function allocates no arrays, so it uses $O(1)$ space.” The function processes a linked list of length $n$ by recursively calling itself on the tail and doing constant local work after the call returns.

### Exercise 4

Compare algorithms with modeled times $A(n)=200n\log_2 n$ and $B(n)=n^2$ and auxiliary spaces $S_A(n)=n$ and $S_B(n)=1$. Explain what asymptotics proves, what exact model calculations can add, and what must be measured before a production choice.

### Exercise 5

Analyze an unfamiliar service that receives two sets of variable-length byte strings, constructs every equal cross-set pair, and either streams or materializes the results. Define size parameters, time and space conventions, lower bounds imposed by input reading/output, cost-model assumptions, hostile cases, and the evidence needed for a capacity claim.

## Answers to the Exercises

### Answer 1

For eventually nonnegative $f,g$ with $g$ eventually positive, $f\in O(g)$ when there exist $c>0,n_0$ such that $f(n)\le cg(n)$ for all $n\ge n_0$. It is in $\Omega(g)$ when there exist $c>0,n_0$ such that $f(n)\ge cg(n)$ thereafter. It is in $\Theta(g)$ when both relations hold, equivalently when positive lower and upper multiples of $g$ eventually sandwich $f$.

For $n\ge1$, $4n+9\le13n\le13n^2$, so $4n+9\in O(n^2)$. Also $4n\le4n+9\le13n$, so it is in $\Theta(n)$. Big-O bounds need not be tight; membership in a loose quadratic upper class does not erase the tighter linear class.

### Answer 2

The exact body count is

$$
T(n)=\sum_{i=1}^{n}(2i+1)
=2\frac{n(n+1)}{2}+n
=n^2+2n.
$$

For $n\ge1$, $n^2\le T(n)\le3n^2$ because $2n\le2n^2$. Thus $c_1=1$, $c_2=3$, and $n_0=1$ prove $T\in\Theta(n^2)$. Loop-control costs can add another linear term without changing the class, but an exact implementation count must declare whether they are included.

### Answer 3

The conclusion ignores the call stack. Before the deepest call returns, one frame for each list node can remain live. With constant-size frames and no guaranteed tail-call elimination, peak stack space is $\Theta(n)$, while additional heap allocation by the algorithm may indeed be $\Theta(1)$. The input list itself is $\Theta(n)$ but is normally excluded from auxiliary space.

If the language/runtime guarantees a transformation that eliminates the recursion, analyze the transformed implementation and its conditions. Also include callbacks, exceptions, frame size, maximum recursion depth, and stack-overflow behavior in a concrete contract. “No arrays” establishes none of these properties.

### Answer 4

As $n\to\infty$, $A\in\Theta(n\log n)$ grows strictly more slowly than $B\in\Theta(n^2)$, while A uses linear auxiliary space and B uses constant auxiliary space. Asymptotics therefore exposes an eventual time advantage and persistent modeled space disadvantage; it does not choose a finite workload automatically.

Exact calculations can solve or approximate the crossover $200n\log_2 n=n^2$, check whether the projected sizes fit A's storage budget, and retain boundary/rounding terms. Production evidence must verify both algorithms implement the same contract, then measure representative and adversarial sizes on the target toolchain/machine, including latency distributions, memory peaks, allocation, cache/I/O behavior, warm/cold state, output validation, and failure behavior. A hard memory limit may rule out A before speed comparison.

### Answer 5

Let $n,m$ be element counts, let $B_X,B_Y$ be total input bytes, let $L$ bound or describe string lengths, and let $k$ be the number of emitted pairs. A naive cross product performs $nm$ equality checks, but byte-comparison cost is not constant: it depends on common prefixes and lengths, so a safe formula retains examined bytes. Merely reading inputs costs $\Omega(B_X+B_Y)$ under a byte model, and emitting $k$ pair identifiers costs $\Omega(k)$ or more according to encoding.

A hash-index design can reduce candidate comparisons under explicit hashing, collision, memory, and adversary assumptions. Its time includes hashing all bytes plus build/probe/collision/output work; its auxiliary space includes the index and retained keys or references. Streaming output can keep result storage bounded but still incurs output time and backpressure state. Materialization requires $\Theta(k)$ result records and may create a large transient peak.

The contract must specify duplicate semantics, normalization/encoding, equality, malformed and oversized strings, hash seeding, collision attacks, integer/size overflow, allocation failure, cancellation, partial output, ordering, and consumer failure. Evidence should combine algebraic upper/lower analysis with correctness tests, collision and long-common-prefix adversaries, empty/all-equal/disjoint/skewed inputs, peak-memory instrumentation, output-rate/backpressure tests, and reproducible target-environment measurements. Capacity claims name size envelopes and resource limits; finite measurements are not presented as asymptotic proof.
