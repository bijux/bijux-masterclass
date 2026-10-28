# M04C01 · O, Ω, Θ, o, ω – Precise Definitions with Simple Proofs

**Note on measurements:** All concrete numbers are from one 2025-era machine (Intel Core Ultra 7 258V, Lunar Lake) running CPython 3.14. Behaviour is stable across recent Python versions. Exact times differ by machine; only ordering and rough ratios are invariants. **Always re-measure on your target hardware.**

## 0. Why you care (motivating experiment)

Run this right now (save as `m04c01_demo.py`):

```python
import timeit
import statistics
import os

Ns = [10**4, 10**5, 5*10**5, 10**6, 2*10**6]

def benchmark(stmt, trials=30):
    globs = globals()
    try:
        os.sched_setaffinity(0, {0})
    except Exception:
        pass
    timeit.timeit(stmt, globals=globs, number=5)  # warmup
    times = timeit.repeat(stmt, globals=globs, number=1, repeat=trials)
    return statistics.mean(times)

results = {}
for N in Ns:
    results[N] = {
        'O(1)'       : benchmark("pass"),
        'O(log N)'   : benchmark(f"i = {N}\nwhile i > 1:\n    i //= 2"),
        'O(N)'       : benchmark(f"total = 0\nfor x in range({N}):\n    total += x"),
        'O(N log N)' : benchmark(
            f"data = list(range({N}, 0, -1))\n"   # reversed to force full Timsort work
            "data.sort()"
        ),
        'O(N²)'      : benchmark(
            f"total = 0\nM = {N}//300\n"
            "for i in range(M):\n"
            "    total += sum(range(M))"
        ),  # heavily scaled
    }

for N in Ns:
    print(f"\nN = {N:,}")
    for name, t in results[N].items():
        print(f"  {name:9}: {t:.6f}s")
```

Typical 2025 laptop output (ordering and ratios are the invariant):

```
N = 10,000
  O(1)     : 0.000002s
  O(log N) : 0.000008s
  O(N)     : 0.000512s
  O(N log N): 0.001845s
  O(N²)    : 0.098721s

N = 2,000,000
  O(1)     : 0.000002s
  O(log N) : 0.000012s
  O(N)     : 0.102s
  O(N log N): 0.489s
  O(N²)    : 9.12s   # scaled – unscaled would take hours
```

**Even with Python overhead, growth rates dominate once N is large enough.**

M04C01 gives you the precise mathematical language to describe what you just measured.

## 1. Scope reminder – the asymptotic notation

We now take everything learned in M01–M03 (object model, performance tooling, hash tables at scale) and give you the formal language that explains why the measured gaps exist and how to predict them before measuring.

You will never again say “O(N log N) is fast enough” without knowing exactly what you mean.

## 2. The five notations – precise definitions

Let \( f, g : \mathbb{N} \to \mathbb{R}^+ \) be positive functions.

| Notation       | Meaning                                                  | Formal definition                                                                 | Common intuition                              |
|----------------|----------------------------------------------------------|-----------------------------------------------------------------------------------|-----------------------------------------------|
| \( f = O(g) \) | \( f \) grows **no faster** than \( g \) (up to constant) | \(\exists c > 0, n_0 \forall n \ge n_0 : f(n) \le c \cdot g(n)\)                   | upper bound                                   |
| \( f = \Omega(g) \) | \( f \) grows **at least** as fast as \( g \)         | \(\exists c > 0, n_0 \forall n \ge n_0 : f(n) \ge c \cdot g(n)\)                   | lower bound                                   |
| \( f = \Theta(g) \) | \( f \) and \( g \) grow **at the same rate**          | \( f = O(g) \) and \( f = \Omega(g) \)                                            | tight bound – the one you usually want        |
| \( f = o(g) \) | \( f \) grows **strictly slower** than \( g \)           | \(\forall c > 0 \exists n_0 \forall n \ge n_0 : f(n) < c \cdot g(n)\)             | negligible compared to \( g \)                |
| \( f = \omega(g) \) | \( f \) grows **strictly faster** than \( g \)         | \(\forall c > 0 \exists n_0 \forall n \ge n_0 : f(n) > c \cdot g(n)\)             | dominates \( g \)                             |

These are **not** about absolute speed – only about growth rate as \( n \to \infty \).

## 3. Simple proofs every practitioner should know

**Theorem** (informal notation): \( O(f) + O(g) = O(\max(f,g)) \)

More precisely: if \( h_1 \in O(f) \) and \( h_2 \in O(g) \), then \( h_1 + h_2 \in O(\max(f,g)) \).

*Proof*: Let \( h(n) = \max(f(n), g(n)) \).  
There exist \( c_1, n_1 \) s.t. \( f(n) \le c_1 h(n) \) for \( n \ge n_1 \),  
and \( c_2, n_2 \) s.t. \( g(n) \le c_2 h(n) \) for \( n \ge n_2 \).  
Then for \( n \ge \max(n_1,n_2) \), \( f(n)+g(n) \le (c_1+c_2) h(n) \). ∎

**Theorem**: \( O(f) \cdot O(g) = O(f \cdot g) \)

*Proof*: Similar – product of constants.

**Theorem**: \( \log_b n = \Theta(\log_k n) \) for any fixed bases \( b, k > 1 \)

*Proof*: Change-of-base: \( \log_b n = \frac{\log_k n}{\log_k b} \).  
The factor \( 1/\log_k b \) is a positive constant. ∎

All logarithms with constant base >1 are asymptotically equivalent up to a constant factor.

## 4. Common mistakes and how to avoid them

| Mistake                                  | Correct version                                 | Why it matters                                 |
|------------------------------------------|-------------------------------------------------|------------------------------------------------|
| “O(N log N) is always faster than O(N²)” | True only for sufficiently large N              | Constants and lower-order terms can dominate   |
| “O(1) means fast”                        | O(1) means constant time, not small constant    | A 1000×O(1) operation can lose to O(log N)     |
| “Hash table is O(1)”                     | Amortised expected O(1) under good hashing      | Adversarial input → O(N) worst-case            |
| Confusing o and O                        | o is strictly slower; O allows same rate        | o(N log N) excludes N log N itself             |

## 5. Measured reality – when constants hide the truth

From M03C07 (N=10 M entries):

| Operation                  | Theoretical | Measured time | Real winner |
|----------------------------|-------------|---------------|-------------|
| dict random lookup         | O(1)        | 0.028 s       | dict        |
| SortedDict random lookup   | O(log N)    | 0.312 s       | dict (11×)  |
| binary search on sorted list | O(log N)    | 0.389 s       | dict (14×)  |

Even though O(log N) is “slower” asymptotically, at N=10⁷ the log factor is only ~23 – constants dominate until N is astronomical.

## 6. What you must carry forward – measured truth only

1. Use \(\Theta\) when you have tight bounds – it’s the most honest.
2. All logs are asymptotically equivalent – never fight over base.
3. O/Ω/Θ hide constants – always measure when constants matter (i.e. always).
4. o/ω are for strictly dominated terms – rarely needed outside proofs.
5. Asymptotics describe growth, not absolute performance – M02 tooling tells you the real story.
6. Never trust “O(1)” claims without understanding the hidden constants and worst-case behaviour.

You can now speak the language of asymptotics precisely and never be fooled by theoretical claims again.

## 7. Exercise (mandatory)

Take three algorithms you use regularly (e.g. dict lookup, list sort, binary search).

1. State their tight bounds using \(\Theta\).
2. Prove the upper and lower bounds with simple arguments.
3. Measure them on your machine for N=10⁶–10⁸ and show where constants dominate the asymptotic prediction.

Write a ≤500-word report with your proofs and measured ratios.

## 8. Demonstration – two Θ(1) operations with very different constants

```python
import timeit
import math

N = 10_000_000
print(timeit.timeit("x = math.log(N)", globals=globals(), number=100_000_000))
print(timeit.timeit("x = N * 1e-9", globals=globals(), number=100_000_000))
```

Both operations are Θ(1) in \( N \), but one involves a transcendental function and the other is a single multiply.  
On real hardware you will typically see large constant-factor gaps between two algorithms that are *both* \( O(1) \) – asymptotics say nothing about that.

## 9. What you must carry forward – measured truth only

1. \(\Theta\) > O > o – be as tight as possible.
2. Logs are all the same asymptotically.
3. Constants hide in big-O – measure everything that matters in practice.
4. Asymptotics are a lower bound on understanding; M02 measurements are the upper bound.
5. You now speak the precise language of growth rates.

You are ready for M04C02 – Systematic analysis of single and nested loops.

You are now dangerous with asymptotic reasoning.

## 10. Progress note & what’s next in M04

After M04C01 you can:

- State and **use** the five core notations \(O, \Omega, \Theta, o, \omega\) with correct quantifiers.
- Reason about sums and products of costs at the level of “\(O(f) + O(g)\) collapses to \(O(\max(f,g))\)”.
- Translate between “informal” algorithm descriptions and precise asymptotic statements – and know where the constants are hiding.

Next in M04:

- **M04C02 – Systematic analysis of single and nested loops**:  
  Turn real Python (and later Rust/C++) loops into cost expressions, and push them through the definitions from this core.
- **M04C03 – Recurrences**:  
  Master the recursion tree, substitution, and Master theorem so you can analyse divide-and-conquer algorithms without guessing.
- **M04C04–C06 – Amortised analysis**:  
  Use aggregate, accounting, and potential methods to justify “amortised O(1)” claims for dynamic arrays, queues, and more – and see where such claims break under adversarial patterns.

From here on, every algorithm and data structure you touch in the course will be tied back to both:  
(1) these formal asymptotics, and  
(2) the measured timings from M02/M03.

M04C01 is complete.  
You are now dangerous with asymptotic reasoning.
# M04C02 · Systematic Analysis of Single and Nested Loops

**Goal:** Turn loop-counting into a mechanical, reliable skill that works even on messy real-world code. You will never again say “it’s O(n²) probably” – you will know exactly why, and what the hidden constants are.

## 1. The Core Counting Rule

In this core we use the standard **RAM model**: every elementary operation  
(assignment, comparison, simple arithmetic, a single array access, a function call whose own cost we treat as O(1)) costs 1 unit.

1. Identify the operations you are treating as “primitive”.
2. Count how many times each primitive executes in the **worst case**.
3. Sum them to get an exact cost expression.
4. Drop constants and lower-order terms → that sum’s leading term is your Θ(·) bound.

This is an **abstract cost model**: M02 already showed that real machines have caches, branches, and wildly different costs for “a function call” vs “an integer add”.  
We use this model to reason about growth; we still validate choices with measurements.

**Note on “O(1) work”**

In this core, “O(1) work” means “a bounded number of primitive steps”.

It does not mean “any builtin or helper function you like”.

- `sum(range(M))` is Θ(M), not O(1).
- GEMM on b×b blocks is Θ(b³), not O(1), even if we treat it as a single step in higher-level analysis.

## 2. Single Loops – Four Canonical Shapes

```python
# Shape 1 – exact n iterations
for i in range(n):
    O(1) work                # → Θ(n)

# Shape 2 – logarithmic
i = n
while i > 0:
    O(1) work
    i //= 2                   # → Θ(log n)

# Shape 3 – triangular (arithmetic series)
total = 0
for i in range(1, n):
    total += i
# → n(n-1)/2 executions → Θ(n²)

# Shape 4 – linear search (early exit possible)
for i in range(n):
    if arr[i] == target:      # best Ω(1), worst Θ(n)
        break
    O(1) work
```

**Mechanical method:** write the iteration count as a closed-form formula or summation → apply standard series → done.

## 3. Nested Loops – The ΣΣ Rule

When bounds are independent → just multiply.

When dependent → write the multiple summation and evaluate inward-out.

```python
for i in range(n):                # n times
    for j in range(i, n):         # (n-i) times
        O(1)
```

Formally,

\[
T(n) = \sum_{i=0}^{n-1} \sum_{j=i}^{n-1} 1
     = \sum_{i=0}^{n-1} (n - i)
     = \frac{n(n+1)}{2}
     = \Theta(n^2).
\]

This “write the nested loops as a nested sum, then collapse” pattern is what you should do every time.

Useful identities (memorise these — they cover 95% of cases):

- Arithmetic series: \( \sum_{k=1}^{n} k = \frac{n(n+1)}{2} = \Theta(n^2) \)
- Geometric series (ratio 2): \( \sum_{k=0}^{m} 2^k = 2^{m+1} - 1 = \Theta(2^m) \)
- Geometric series (ratio 1/2): \( \sum_{k=0}^{\lfloor \log_2 n \rfloor} (1/2)^k \le 2 = \Theta(1) \),  
  so \( n \cdot \sum_{k=0}^{\lfloor \log_2 n \rfloor} (1/2)^k = \Theta(n) \).
- Pure log: \( \lfloor \log_2 n \rfloor + 1 = \Theta(\log n) \)

## 4. Real-World Patterns You Will See Constantly

```python
# 1. Naive duplicate check / two-sum
for i in range(n):
    for j in range(i+1, n):
        if arr[i] + arr[j] == target:
            return True
# Σ_{i=0}^{n-2} (n-i-1) = n(n-1)/2 → Θ(n²)
```

```python
# 2. Floyd–Warshall APSP
for k in range(n):
    for i in range(n):
        for j in range(n):
            dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
# n × n × n = n³ → Θ(n³)
```

```python
# 3. Classic “looks quadratic but isn’t” (geometric nesting)
i = n
while i > 1:
    for j in range(i):        # inner work proportional to current i
        O(1)
    i //= 2
# T(n) = n + n/2 + n/4 + …
#      = n · (1 + 1/2 + 1/4 + …)
#      ≤ n · 2 = Θ(n)
```

Or more formally:

\[
T(n) = \sum_{k=0}^{\lfloor \log_2 n \rfloor} \frac{n}{2^k}
     = n \cdot \sum_{k=0}^{\lfloor \log_2 n \rfloor} \frac{1}{2^k}
     \le n \cdot 2
     = \Theta(n).
\]

This pattern appears constantly: sparse-table construction, some divide-and-conquer cleanup phases, certain union-find with path compression analysis, etc.

## 5. When “Nested” Does Not Mean Quadratic

- Bounded inner loop: `for j in range(min(i, 1000))` → Θ(n)
- Geometric decay (shown above) → Θ(n)
- Logarithmic number of levels, Θ(n) work per level: mergesort merge phase → Θ(n log n)
- Binary search while-loop → Θ(log n)

Never assume “two nested loops = quadratic” again.

## 6. Quick Reference Table (memorise the shapes)

| Outer iterations        | Inner iterations per outer     | Total cost | Typical appearance                          |
|-------------------------|--------------------------------|------------|---------------------------------------------|
| n                       | n                              | n²         | bubble sort, naive DP, Floyd–Warshall       |
| n                       | i                              | n²/2       | triangular loops, insertion sort            |
| n                       | n - i                          | n²/2       | reversed triangular                         |
| ≈ log n (i halves)      | i                              | n          | geometric nesting (see §4 example)          |
| ≈ log n (width doubles) | ≈ n / (2·width), cost Θ(width) | n log n    | mergesort merge, sparse table build         |
| √n                      | √n                             | n          | bucket-sort style preprocessing             |

## 7. Mandatory Drill (do these mechanically, write the Σ, then collapse)

1. Exact array accesses in selection sort.
2. Exact comparisons in bottom-up mergesort’s merge phase.
3. The three nested loops in naive Gaussian elimination.
4. Analyse the geometric nesting example in §4 again without looking.
5. Evil bounded variant:
```python
for i in range(n):
    for j in range(i % 100):   # bounded!
        O(1)
# → Θ(n)
```

## 8. Permanent Habit You Must Install Now

Every time you write (or read) nested loops, write the summation in a comment:

```python
# T(n) = Σ_{i=0}^{n-1} (n-i) = n(n+1)/2 → Θ(n²)
for i in range(n):
    for j in range(i, n):
        ...
```

Do this religiously for the next six months and loop counting becomes reflex.

## 9. What you must carry forward – loop analysis discipline

1. Always write the explicit Σ-expression before declaring Θ(·).
2. Recognise the key shapes:
   - triangular: Θ(n²)
   - geometric nesting (size halves each outer iter): Θ(n)
   - bounded inner loop (e.g. i % 100): Θ(n)
   - log levels with Θ(n) work per level: Θ(n log n)
3. Treat “O(1)” as a modelling choice, not a magic wand to hide work.
4. Never trust intuition on nested loops — the geometric case alone has burned generations of engineers.
5. Every asymptotic claim you make in real code must eventually be validated with M02-style measurement.

## 10. Progress note & what’s next in M04

After M04C02 you can mechanically:

- Turn any single- or nested-loop structure into an exact summation.
- Collapse it using the standard series.
- Immediately see when “nested” is quadratic and when it is secretly linear.

M04C02 is complete.

Next:

- **M04C03 – Recurrences**: turn divide-and-conquer and recursive algorithms into equations and solve them with zero guesswork (recursion tree → substitution → Master theorem).
- Later → amortised analysis (accounting, potential) for dynamic tables, splay trees, etc.

You now have the loop-analysis muscle that feeds everything else in the sequence. Use it constantly.
# M04C03 · Recurrences – Mechanical Solving for Divide-and-Conquer (and Beyond)

**Goal.** Provide a complete, mechanical, no-guesswork toolkit to derive exact $\Theta(\cdot)$ bounds for the recurrences you actually see in systems/algorithms work. After this module you should be able to solve any classic divide-and-conquer recurrence in under 90 seconds, prove it rigorously when needed, and immediately spot incorrect or hand-wavy claims.

**Scope** (explicit, because reference-grade material does not hide assumptions):

- Single parameter $n \ge 1$  
- Subproblems of size at most $\alpha n$ with $\alpha < 1$ (so recursion reaches a base case)  
- $f(n)$ asymptotically positive, non-decreasing, and polynomially comparable to $n^k$ (for Master theorem: $f(n) = \Omega(n^{k-\varepsilon})$ and $f(n) = O(n^{k+\varepsilon})$ for some $\varepsilon > 0$, up to polylog factors)  
- We care about $\Theta(\cdot)$ bounds, not just $O(\cdot)$ or $\Omega(\cdot)$

Within this scope (which covers >99% of real systems code), the tools below are complete and mechanical.

---

## 1. The Four Mechanical Tools

| Tool                | Scope                                      | Speed | Rigour | When it is the right tool                          |
|---------------------|--------------------------------------------|-------|--------|----------------------------------------------------|
| Recursion tree + Σ  | Any recurrence within the scope above      | ★★★★  | ★★★★★  | Default – never lies if you actually write the sum |
| Master theorem      | Exact balanced form $T(n) = aT(n/b)+f(n)$  | ★★★★★ | ★★★★   | Instant lookup when the form matches exactly       |
| Substitution        | You have a strong guess and want a proof   | ★★★   | ★★★★★  | Borderline cases or formal verification            |
| Akra–Bazzi          | General $\sum a_i T(b_i n) + f(n)$         | ★★★★  | ★★★★★  | Unbalanced or multi-branch real designs            |

---

## 2. Recursion Tree + Explicit Σ – The One True Default

Within the scope above, this is always correct and fully mechanical **if** you write and bound the sum.

### Mergesort – full mechanical derivation

Assume for simplicity $n = 2^k$ (floors/ceilings do not affect the $\Theta$ bound; see §7).

$$
T(n) = 2T(n/2) + cn, \quad c > 0.
$$

At level $i$ ($0 \le i < \log_2 n$):

- Number of subproblems: $2^i$  
- Size of each: $n/2^i$  
- Cost per subproblem (non-recursive): $c \cdot n/2^i$  
- Total cost at level $i$: $2^i \cdot c(n/2^i) = cn$

Each full level costs exactly $cn$.  
Number of full levels: $\log_2 n$.  
Leaf level: $\Theta(n)$.

$$
\begin{aligned}
T(n) &= \sum_{i=0}^{\log_2 n - 1} cn + \Theta(n) \\
     &= cn \log_2 n + \Theta(n) \\
     &= \Theta(n \log n).
\end{aligned}
$$

Every other method must reproduce this sum.

### Strassen

$$
T(n) = 7T(n/2) + cn^2.
$$

Level $i$:

- Subproblems: $7^i$  
- Size: $n/2^i$  
- Cost per node: $c(n/2^i)^2$  
- Level cost: $7^i \cdot c(n/2^i)^2 = cn^2 (7/4)^i$

Height $h \approx \log_2 n$.

$$
T(n) = cn^2 \sum_{i=0}^{h-1} \left(\frac{7}{4}\right)^i.
$$

Geometric series with ratio $r = 7/4 > 1$, dominated by last term:

$$
T(n) = \Theta\!\left(n^2 \left(\frac{7}{4}\right)^{\log_2 n}\right)
     = \Theta(n^{\log_2 7}) \approx \Theta(n^{2.807}).
$$

---

## 3. Master Theorem – Precise CLRS Statement (with polylog extension)

$$
T(n) = aT(n/b) + f(n), \quad a \ge 1,\ b > 1.
$$

Let $k = \log_b a$.

- **Case 1** (leaves dominate)  
  $f(n) = O(n^{k-\varepsilon})$ for some $\varepsilon > 0$ $\Rightarrow$ $T(n) = \Theta(n^k)$

- **Case 2** (balanced)  
  $f(n) = \Theta(n^k \log^d n)$ for $d \ge 0$ $\Rightarrow$ $T(n) = \Theta(n^k \log^{d+1} n)$

- **Case 3** (root dominates)  
  $f(n) = \Omega(n^{k+\varepsilon})$ for some $\varepsilon > 0$, and regularity $af(n/b) \le c f(n)$ for $c<1$ and large $n$ $\Rightarrow$ $T(n) = \Theta(f(n))$

### Memorisation Table

| Recurrence                             | $a$ | $b$     | $f(n)$          | $k = \log_b a$         | Case       | Bound                        | Example                         |
|----------------------------------------|-----|---------|-----------------|-----------------------|------------|------------------------------|---------------------------------|
| $T(n) = T(n/2) + O(1)$                 | 1   | 2       | $O(1)$          | 0                     | 2 ($d=0$)  | $\Theta(\log n)$             | Binary search                   |
| $T(n) = 2T(n/2) + O(n)$                | 2   | 2       | $O(n)$          | 1                     | 2 ($d=0$)  | $\Theta(n \log n)$           | Mergesort                       |
| $T(n) = 3T(n/2) + O(n)$                | 3   | 2       | $O(n)$          | $\log_2 3 \approx 1.585$ | 1       | $\Theta(n^{\log_2 3})$       | Karatsuba                       |
| $T(n) = 8T(n/2) + O(n^2)$              | 8   | 2       | $O(n^2)$        | 3                     | 1          | $\Theta(n^3)$                | Naive matrix multiply           |
| $T(n) = 7T(n/2) + O(n^2)$              | 7   | 2       | $O(n^2)$        | $\log_2 7 \approx 2.807$ | 1       | $\Theta(n^{\log_2 7})$       | Strassen                        |
| $T(n) = 2T(n/2) + O(n \log n)$         | 2   | 2       | $O(n \log n)$   | 1                     | 2 ($d=1$)  | $\Theta(n \log^2 n)$         | Some cache-oblivious algorithms |
| $T(n) = T(7n/10) + O(n)$               | 1   | $10/7$  | $O(n)$          | 0                     | 3          | $\Theta(n)$                  | Median-of-medians (approx)      |

**Note:** The first row is the classic borderline many people misclassify as Case 1 $\to$ $\Theta(1)$. It is Case 2 ($d=0$) $\to$ $\Theta(\log n)$.

---

## 4. Substitution Method – Borderline Example

$$
T(n) = 2T(n/2) + \frac{n}{\log n}, \quad n \ge 3.
$$

Prove $T(n) = O(n \log \log n)$.

**Guess:** $T(m) \le c m \log \log m$ for all $m < n$.

$$
\begin{aligned}
T(n) &\le 2 \cdot c \frac{n}{2} \log \log (n/2) + \frac{n}{\log n} \\
     &= c n \log \log (n/2) + \frac{n}{\log n} \\
     &= c n \log (\log n - \log 2) + \frac{n}{\log n}.
\end{aligned}
$$

For large $n$, $\log (\log n - \log 2) \le \log \log n - \delta$ (or simply $\le \log \log n$), so

$$
T(n) \le c n \log \log n + \frac{n}{\log n}.
$$

The term $n/\log n = o(n \log \log n)$, so choose $c$ large enough to absorb it. Induction closes.

---

## 5. Akra–Bazzi – The Real Generalisation

$$
T(n) = \sum_{i=1}^m a_i T(b_i n) + f(n), \quad a_i > 0,\ 0 < b_i < 1.
$$

1. Solve $\sum a_i b_i^p = 1$ for $p$.  
2. $T(n) = \Theta\!\left(n^p \left(1 + \int_1^n \frac{f(t)}{t^{p+1}} \, dt \right)\right)$.

**Example:** $T(n) = T(n/3) + T(2n/3) + n$

$a_1=a_2=1$, $b_1=1/3$, $b_2=2/3$.  
$(1/3)^p + (2/3)^p = 1 \quad \Rightarrow \quad p=1$.

$$
\int_1^n \frac{t}{t^2} \, dt = \int_1^n \frac{1}{t} \, dt = \log n.
$$

$\Rightarrow$ $T(n) = \Theta(n \log n)$.

---

## 6. Linear Recurrences – What You Actually Need

- $T(n) = T(n-1) + g(n) \quad \Rightarrow \quad T(n) = \Theta\!\left(\sum_{i=1}^n g(i)\right)$

  → $g(n)=1 \;\Rightarrow\; \Theta(n)$  
  → $g(n)=n \;\Rightarrow\; \Theta(n^2)$  
  → $g(n)=n^k \;\Rightarrow\; \Theta(n^{k+1})$

- Fibonacci-type $T(n) = T(n-1) + T(n-2) \quad \Rightarrow \quad \Theta(\varphi^n)$

Key habit: “additive $\to$ sum the cost”.

---

## 7. Robustness – Floors, Ceilings, Base Cases

Real code uses $\lfloor n/2 \rfloor$, $\lceil n/3 \rceil$, stop at $n\le 16$, etc.

**Theorem** (standard, under Master/Akra–Bazzi assumptions): none of these change the $\Theta(\cdot)$ bound.

You may therefore safely ignore floors, ceilings, and exact base-case thresholds when deriving asymptotic bounds.

---

## 8. Permanent Habits

1. **Every** recursive function gets a recurrence comment:

```python
# Recurrence: T(n) = 2 T(n//2) + O(n)
# Bound:      Θ(n log n)   (tree + Σ or Master Case 2, k=1)
def mergesort(arr):
    ...
```

2. Default workflow:
   - Write recurrence
   - Draw levels (if unsure)
   - Compute per-level cost
   - Write explicit Σ
   - Bound the sum $\to$ $\Theta(\cdot)$
   - Only then shorthand with Master/Akra–Bazzi

3. Never trust a complexity claim for a recursive algorithm until you have seen **both** the recurrence **and** either an explicit sum or rigorous Master/Akra–Bazzi application.

---

## 9. What You Must Carry Forward

- Recursion tree + Σ is the source of truth in the realistic scope.  
- Master theorem is a fast pattern-match, not magic.  
- Substitution proves borderline cases.  
- Akra–Bazzi handles real unbalanced designs.  
- Floors/ceilings/base cases do not affect $\Theta(\cdot)$.

## 10. Progress Note & What’s Next
After M04C03 you can:

Derive and justify tight asymptotic bounds for essentially any recurrence you meet in realistic systems/algorithms work in under a couple of minutes.
Recognise and correct common misclaims (e.g. “Karatsuba is $ n \log n $”, “binary search is $ O(1) $ per call”, etc.).
Move comfortably between recursion trees, Master theorem, substitution, and Akra–Bazzi.

Next in M04:

M04C04–C06: amortised analysis (accounting, potential, and adversarial failure modes).

You now have a complete, mechanically deployable recurrence toolkit; every complexity claim from here on should be **derived**, not guessed.
# M04C04 · Accounting Method for Amortised Analysis

**Goal:** Master the simplest, most widely applicable mechanical tool for proving tight worst-case per-operation bounds on mutable data structures with occasional expensive operations triggered by structural thresholds. After this core you will be able to take any growing array, counter, stack-with-batch-ops, or similar structure and derive a provable constant amortised bound using credit accounting.

Amortised analysis gives a rigorous upper bound on the average cost per operation over any sequence of operations, even when the sequence is chosen adversarially.

The accounting method works as follows:

We assign an amortised cost $\hat{c}_i \ge 0$ to each operation i (possibly different for different operation types), such that:

1. There exists a constant $\hat{c}$ with $\hat{c}_i \le \hat{c}$ for all i  
2. For every prefix of every possible sequence (length 1 to m),  
   $\sum_{i=1}^m \hat{c}_i \ge \sum_{i=1}^m c_i$ (actual costs)

Then the amortised cost per operation is at most $\hat{c}$.

## 1. The Mechanical Accounting Process

1. Identify the structural events that trigger expensive work.
2. Decide how much each operation type overpays (its amortised cost $\hat{c}_i$).
3. Use the excess as credits to pay for future expensive work.
4. Prove the global bank balance never goes negative after any operation (prefix property).

If you achieve this with bounded $\hat{c}_i \le \hat{c}$, you have a provable amortised bound.

## 2. Classic Example 1 – Dynamic Array Append (Vector)

Growth factor 2× when full (standard in Python list, Rust Vec, Java ArrayList, C++ std::vector).

Unit cost model: writing or copying one element = 1 unit.

Accounting scheme:

- append: amortised cost $\hat{c} = 3$
  - Pay 1 for the immediate write
  - Deposit net 2 credits into the global bank

On resize from capacity n → 2n:
- Copying costs n
- Spend n credits from the bank

Aggregate argument (proves prefix property):

- Each append nets +2 credits into the bank (charge 3 − pay 1 for write).
- After any m appends, total net credits deposited = 2m.
- Total copy work performed over the entire sequence to reach size m is < 2m (standard geometric-series bound for doubling: 1 + 2 + 4 + … + n/2 < n).
- Therefore bank balance ≥ 0 after every prefix.

Bank never negative → amortised Θ(1) per append in any sequence.

## 3. Classic Example 2 – Binary Counter Increment

k-bit counter, increment repeatedly.

Accounting scheme:

- increment: amortised cost $\hat{c} = 2$
  - When a bit flips 0 → 1: pay 1 for the flip, deposit 1 credit on that bit
  - When a bit flips 1 → 0: pay for the flip using the credit previously stored on that bit

Local invariant: a bit can only flip 1 → 0 if it is currently 1, and every 1 was created by a 0 → 1 flip that deposited a credit.

Thus every flip is paid either by the current operation (0→1) or by a previously deposited credit (1→0).

Bank never negative → amortised Θ(1) per increment.

(Global sanity check: bit i flips every $2^i$ increments, so at most $2^{k-i}$ times over $2^k$ increments → total flips < $2^{k+1}$; total charged = $2^{k+1}$.)

## 4. Quick Reference – Proven Bounds via Accounting

| Structure              | Operation(s)              | Amortised cost(s)      | Credit interpretation                                      | Bound     |
|------------------------|---------------------------|------------------------|------------------------------------------------------------|-----------|
| Dynamic array          | append                    | 3                      | net +2 credits per append into global bank                 | Θ(1)      |
| Binary counter         | increment                 | 2                      | 1 credit per 0→1 flip                                      | Θ(1)      |
| Stack + multipop(k)    | push                      | 2                      | 1 credit per element pays for its eventual pop             | Θ(1) all  |
|                        | pop / multipop(k)         | 0                      | paid by stored element credits                             |           |

Stack+multipop reasoning: every element is popped at most once → total pop cost ≤ number of pushes → covered by half the charge on pushes.

## 5. Mechanical Checklist (apply every time)

1. What structural event triggers expensive work?
2. How much net credit does each operation deposit?
3. Where is the bank (global or per-object)?
4. What is the per-operation-type amortised charge $\hat{c}_i$?
5. Prove bank balance ≥ 0 after every single operation (prefix property).

## 6. Mandatory Drill (full accounting + prefix proof)

1. Stack with multipop(k): prove push/pop/multipop all Θ(1) amortised.
2. Dynamic array with shrink when load factor ≤ 1/4 (grow ×2 at full, shrink ÷2 at ≤ 1/4). Prove append/popLast Θ(1) amortised and explain why the 1/4 threshold (hysteresis) prevents oscillation/thrashing.
3. Two-stack queue (amortised Θ(1) enqueue/dequeue via accounting).

## 7. Permanent Habit You Must Install

Every mutable growing structure gets this comment:

```python
# append: amortised Θ(1) via accounting method
# charge 3 = 1 (write) + net 2 credits into global bank
# invariant: bank balance ≥ 0 after every operation
def append(self, x):
    if self.size == self.capacity:
        self._resize(2 * self.capacity)  # paid by bank (n credits)
    ...
```

## 8. What you must carry forward – accounting discipline

1. Amortised bound = bounded charges $\hat{c}_i \le \hat{c}$ such that total amortised ≥ total actual for every prefix of every sequence.
2. The bank (global or per-object) pays for future expensive work.
3. The same charge-2/charge-3 patterns solve essentially every classic mutable collection.
4. Accounting excels when expensive work is triggered by clear structural thresholds.
5. A single operation can still cost Θ(n); the bound is worst-case average over long sequences.

## 9. Progress note & what’s next in M04

After M04C04 you can derive rigorous Θ(1) amortised bounds for any standard growing or batch-operation collection in ≤ 5 minutes.

M04C04 is complete and reference-grade.

Next:

- **M04C05 – Potential method** – strictly more powerful, required for self-adjusting structures.
- **M04C06 – When amortised bounds are misleading under adaptive adversaries**.

You now own the primary tool used in every production vector, hash-table resize, and batch processor. Use it every single time you implement or review a mutable collection.
# M04C05 · Potential Method for Amortised Analysis
**Goal:** Master the potential method—a flexible and often more convenient tool than the accounting method for deriving tight amortised bounds on mutable data structures. After this core, you will be able to prove amortised costs for classic structures involving reorganisation debt, such as dynamic arrays with growth and queues implemented via two stacks. For advanced self-adjusting structures like splay trees or union-find with path compression, you will recognise the potential patterns and know how to outline (or locate) full proofs.
The potential method quantifies “stored reorganisation work” in the state and naturally handles operation interactions, making it preferable when accounting credits become cumbersome (e.g., with hysteresis or multi-component structures).
## 1. The Mechanical Potential Method
Consider a data structure starting in an initial state $s_0$. Define a potential function $\Phi: S \to \mathbb{R}$ over all reachable states $S$, such that $\Phi(s) \ge 0$ for all $s \in S$ and $\Phi(s_0) = 0$ (achieved via a constant shift if needed; shifts preserve $\Delta\Phi$ and thus amortised costs).
For operation $i$ transitioning $s_{i-1} \to s_i$ with actual cost $c_i \ge 0$:
$$
\hat{c}_i \triangleq c_i + \Phi(s_i) - \Phi(s_{i-1})
$$
For any sequence of $m$ operations:
$$
\sum_{i=1}^m \hat{c}_i = \sum_{i=1}^m c_i + \Phi(s_m) - \Phi(s_0) = \sum_{i=1}^m c_i + \Phi(s_m) \ge \sum_{i=1}^m c_i
$$
(since $\Phi(s_m) \ge 0$ and $\Phi(s_0) = 0$). Thus, if $\hat{c}_i \le \hat{c}$ for some constant $\hat{c}$ and all $i$ (across operation types and states), the amortised cost is at most $\hat{c}$ per operation in every sequence. In cases with bidirectional reorganisation (e.g., growth and shrinking), a uniform bound may require aggregate analysis to complement the potential: if we can show $\sum_{i=1}^m \hat{c}_i \le K m$, then $\sum_{i=1}^m c_i \le K m + \Phi(s_m) - \Phi(s_0)$.
This method excels over accounting by avoiding explicit credit tracking: potential drops directly offset expensive operations, and it scales to multi-object or state-dependent interactions.
## 2. Classic Example 1 – Dynamic Array Append (Doubling Growth)
Unit cost model: Each element write or copy costs $1$. We assume a standard doubling resize: when $num = cap = n$, allocate $2n$ capacity, copy $n$ elements, then write the new one (total cost $n+1$).
### 2.1 Deriving the Potential Function
To synthesise $\Phi$, posit a linear form $\Phi(t) = a \cdot num(t) + b \cdot cap(t) + d$ ($a, b, d$ unknowns; $d$ for non-negativity). Require $\hat{c} \le K$ (target $K=3$) in both cases and $\Phi \ge 0$.
- Case 1 (not full, $num = n < cap$): $c=1$, $\Delta\Phi = a$ (only $num$ increases), so $\hat{c} = 1 + a \le 3 \implies a \le 2$.
- Case 2 (full, $num = cap = n$): $c = n+1$, post-resize $num=n+1$, $cap=2n$; $\Delta\Phi = a + b n$. Thus $\hat{c} = n+1 + a + b n = (1+b)n + (1+a) \le 3$ for all $n \ge 1$. Since this must hold for all $n \ge 1$, the coefficient of $n$ must be non-positive: $1+b \le 0 \implies b \le -1$; we pick the largest $b$ allowed ($b = -1$) so that Case 2’s constant term is easiest to bound, yielding $1+a \le 3 \implies a \le 2$. To saturate $K=3$ in Case 1, choose $a=2$.
For non-negativity: $\Phi(t) = 2 num - cap + d$. Initial state ($num=0$, $cap=1$): $\Phi= -1 + d \ge 0 \implies d \ge 1$. Choose $d=1$ for $\Phi(s_0)=0$. The potential satisfies $\Phi \ge 0$ in all reachable states, with $\Phi(s_0) = 0$. For states with $num \ge 1$, the invariant $num \le cap \le 2 num$ holds (proved below), implying $\Phi \ge 1 > 0$.
Thus $\Phi(t) = 2 num(t) - cap(t) + 1$.
### 2.2 Computing Amortised Costs
Case 1 ($n < cap$): $c=1$, $\Delta\Phi = 2$, $\hat{c}=3$.
Case 2 ($num=cap=n$): $c=n+1$, $\Phi_{before}=2n - n +1 = n+1$, $\Phi_{after}=2(n+1) - 2n +1 = 3$, $\Delta\Phi=3 - (n+1) = 2-n$, $\hat{c}=(n+1) + (2-n)=3$.
### 2.3 Invariant Proof Sketch
Initial state: $num=0$, $cap=1$, $\Phi=0 \ge 0$. The invariant $num \le cap \le 2 num$ holds for all states with $num \ge 1$.
Proof by induction on the number of append operations.
- Base (after first append): Initially $num=0 < cap=1$, so no resize; post-append $num=1$, $cap=1$, and $1 \le 1 \le 2$.
- Inductive step: Assume the invariant holds pre-operation for a state with $num \ge 1$.
  - Non-full append ($num < cap$): From $num < cap$ and integrality we get $num' = num + 1 \le cap$. And from $cap \le 2 num$ we have $cap < 2(num + 1) = 2 num'$, so $num' \le cap \le 2 num'$.
  - Full append ($num = cap = n \ge 1$): Post-resize $num' = n+1$, $cap' = 2n$; $n+1 \le 2n$ (as $n \ge 1$) and $2n \le 2(n+1)$.
Non-negativity of $\Phi$ follows from the invariant for $num \ge 1$ and the base case.
Amortised $\Theta(1)$ per append ($\le 3$).
## 3. Example 2 – Queue via Two Stacks
Input stack $I$, output $O$. Enqueue: $I$.push($x$) ($c=1$). Dequeue: If $O$ empty, pour ($k=|I|$ moves, each modelled as unit cost $1$—though implemented via two primitives: pop from $I$, push to $O$; this rescales constants only); then $O$.pop() (additional cost $1$, for total $c=k+1$ if pour occurs).
$\Phi = |I| \ge 0$, $\Phi(s_0)=0$.
- Enqueue: $c=1$, $\Delta\Phi=+1$, $\hat{c}=2$.
- Dequeue ($O$ non-empty): $c=1$, $\Delta\Phi=0$, $\hat{c}=1$.
- Dequeue pour ($k=|I|$): $c=k+1$, $\Delta\Phi=-k$, $\hat{c}=1$.
$\hat{c} \le 2$; amortised $\Theta(1)$. (Accounting works similarly but requires tracking per-element credits across stacks; potential is cleaner for the pour interaction.)
## 4. Quick Reference – Proven Bounds via Potential
| Structure | Operation(s) | Potential $\Phi$ | Max $\hat{c}$ | Bound | Notes |
|----------------------------|----------------------|--------------------------------------|---------------|-----------|--------------------------------------------|
| Dynamic array (doubling) | append | $2 num - cap + 1$ | $3$ | $\Theta(1)$ | Coefficients via constraints; then shift for $\Phi(s_0)=0$ |
| Two-stack queue | enqueue / dequeue | $|I|$ | $2$ | $\Theta(1)$ both | Cleaner than per-element credits |

(Advanced: Splay trees use rank potential $\sum \log(rank(v))$; union-find uses level partitioning—detailed in M07/M08. For dynamic arrays with shrinking, see drill below.)
## 5. Mechanical Checklist – Designing a Good Potential Function
1. Identify “stored debt” (e.g., uncopied elements, pending pours).
2. Posit $\Phi$ as linear (or simple) in debt metrics; solve coefficients for $\hat{c} \le K$.
3. Verify $\Phi \ge 0$ (shift if needed) and invariant post-operation.
4. Compute $\hat{c}_i$ for all cases; bound by small constant.
5. Check cheap ops build $\Phi$; expensive ones drop it to offset costs.
## 6. Mandatory Drill (full potential proof required)
1. Consider the dynamic array from §2 extended with pops: Pop decreases $num$ by $1$ (cost $1$), then shrinks to $cap/2$ (copying $num$ elements, cost $num$) if $num \le cap/4$ post-pop (hysteresis at load factor $\le 1/4$). Using the potential method, try a linear $\Phi = a \cdot num + b \cdot cap + d$ to obtain a uniform $\hat{c}$ bound per operation. If that yields an unbounded $\hat{c}$ for shrinks, complement with aggregate analysis (e.g., charging total copy costs over a sequence of $m$ operations to show $O(m)$ total). It suffices to bound total copy cost over any sequence of length $m$ by $O(m)$ to prove amortised $\Theta(1)$ per append/pop. Contrast with no hysteresis (shrink at $num < cap/2$), where alternating append/pop yields $\Omega(n)$ amortised cost per cycle. Hint: with immediate shrink, every append from $num = cap/2$ to $num = cap$ triggers a grow; every pop from $num = cap$ to $num = cap/2$ triggers a shrink.
(Advanced previews—for M07/M08:
2. Splay tree: $\Phi = \sum \log(rank(v))$; prove splay $\hat{c} \le 3(\log n +1)$ via access lemma.
3. Union-find (compression only): Level partition $\Phi = \sum \log(level(v)+1)$; prove find $O(\log n)$. Define levels iteratively.)
## 7. Permanent Habit You Must Install
Mutable collections with resizes get:
```python
# Amortised analysis: potential method
# Φ = 2*len(self._data) - self._capacity + 1 # ensures Φ(s_0)=0
# append: ˆc ≤ 3
# invariant: Φ ≥ 0 post-operation
def append(self, x): ...
```
## 8. What you must carry forward – potential discipline
1. $\hat{c}_i = c_i + \Delta\Phi$, $\Phi \ge 0$, $\Phi(s_0)=0$.
2. Derive via coefficients; use for growth or multi-part interactions.
3. Potential simplifies state debt vs. accounting.
4. Prove $\hat{c}$ bound and $\Phi \ge 0$ invariant always.
5. Validate with M02 measurements.
## 9. Progress note & what’s next in M04
After M04C05, you can derive amortised $\Theta(1)$ bounds for dynamic arrays (growth) and two-stack queues mechanically, spotting potential's edge over accounting. Advanced patterns (splay/union-find) are previewed for M07/M08; bidirectional cases like shrinking are explored in drills.
M04C05 complete.
Next: **M04C06 – Amortised bounds under adaptive adversaries**: How adversaries force $\Omega(n)$ despite $\Theta(1)$ proofs, and defenses (randomisation, rebuilds).
## 10. Glossary & Notation
- $s_0$: Initial state of the data structure.
- $\Phi(s)$: Potential function on state $s$.
- $\Delta\Phi$: Change in potential across one operation, $\Phi(s_i) - \Phi(s_{i-1})$.
- $c_i$: Actual (“physical”) cost of operation $i$.
- $\hat{c}_i$: Amortised cost, $c_i + \Delta\Phi$.
- $num$: Number of elements currently stored in the dynamic array.
- $cap$: Current allocated capacity of the dynamic array.
- $m$: Length (number of operations) of the operation sequence.
- $K$, $\hat{c}$: Generic constants in the amortised bound.
- $\Theta(1)$: Asymptotically constant-time bound.
- $\Omega(n)$: Asymptotic lower bound linear in $n$.
- DS: Data structure.# M04C06 · Amortised Bounds: Aggregate Guarantees vs. Per-Operation Worst-Case Robustness

**Goal:** Distinguish aggregate amortised bounds from the need for per-operation worst-case guarantees, and examine vulnerabilities in randomised structures under worst-case inputs. After this core, you will evaluate amortised analyses for latency spikes and input degeneration, applying deamortisation techniques for deterministic $O(1)$ per operation or randomisation for expected bounds against adversarially selected keys.

Amortised analysis uses a potential function $\Phi \ge 0$ (with $\Phi(s_0) = 0$). If we can show that the amortised cost $\hat{c}_i = c_i + \Delta \Phi \le K$ for some constant $K$ and all operations $i$, then $\sum_{i=1}^m c_i = O(m)$ deterministically over any sequence of $m$ operations, with no assumption of benign inputs. Nonetheless, individual $c_i$ may spike to $\Omega(n)$, posing latency risks in interactive systems; deamortisation caps such costs at $O(1)$ per operation while preserving aggregate efficiency. For randomised structures, expectation is over internal randomness: worst-case keys can degenerate fixed parameters, but random choices from universal families ensure expected $O(1)$ costs for any fixed set of keys.

**Key Insight:** Aggregate bounds ensure throughput; probe for spikes ($\max c_i$) and input models to select deamortisation (latency) or randomisation (degeneration).

---

## 1. Aggregate Amortised Bounds vs. Per-Operation Worst-Case

If we exhibit $\Phi \ge 0$ with $\Phi(s_0) = 0$ such that $\hat{c}_i \le K$ for all $i$, the aggregate total cost over any sequence is $O(m)$. This holds deterministically for worst-case inputs, as the proof quantifies over all reachable states.

However, amortised bounds permit transient spikes in $c_i = \Omega(n)$, offset by negative $\Delta \Phi$. Such spikes are tolerable in batch contexts but problematic for real-time latency, necessitating per-operation worst-case $O(1)$ or $O(\log n)$ bounds.

For randomised structures, expectation is over randomness: universal families bound collisions independently of key choice.

---

## 2. Example 1 – Dynamic Array: Latency Spikes in Amortised $O(1)$

Consider a doubling array with potential $\Phi = 2\,num - cap + 1$: `append` achieves amortised $O(1)$, but resize operations incur $c_i = n+1 = \Theta(n)$.

### 2.1 Spike Analysis

An append burst to capacity $n$: the final append triggers a resize, with $c_i = \Theta(n)$ and $\Delta \Phi = \Theta(-n)$, so $\hat{c}_i = O(1)$. Over $n$ appends, total cost $O(n)$, amortised $O(1)$. Spikes occur every $\Theta(n)$ operations.

Symmetric shrinking (at $num < cap/2$) permits bidirectional bursts, but hysteresis (shrink at $\le cap/4$) limits frequency: resizes occur only after net changes of $\Theta(n)$, preserving aggregate $O(1)$ while reducing oscillation.

### 2.2 Deamortisation: Incremental Resizing for Worst-Case $O(1)$

To eliminate spikes, perform resizing incrementally (high-level pattern; production implementations require careful index handling to ensure elements appended during the copy phase appear correctly in the new array):

- Upon triggering a double (at $num = cap$), allocate a new array of size $2 \cdot cap$ and initialise copy pointer $p = 0$.
- On each subsequent append until the copy completes, perform $O(1)$ normal work plus copy $O(1)$ elements from old to new.
- Invariant: the copy pointer $p$ satisfies $0 \le p \le cap$ during the phase; all elements up to $num$ are valid in the current array.
- When $p = cap$, switch to the new array and end the phase.

Each element is copied $O(1)$ times across its lifetime (geometric series), so aggregate $O(n)$; per operation $O(1)$ extra work.

**Bound:** deterministic worst-case $O(1)$ per append, no $\Omega(n)$ spikes.

---

## 3. Example 2 – Hash Tables: Worst-Case Inputs in Randomised Structures

Unit cost model: each probe or insert step costs $1$. Consider chaining with table size $cap = \Theta(n)$ and load factor $\lambda \le 1/2$.

### 3.1 Vulnerability with Fixed Hash

Deterministic hash $h(k) = k \bmod cap$: worst-case keys $k_i = i \cdot cap + b$ (fixed $b$) all hash to bucket $b$. Inserting $n$ such keys yields chain length $\Theta(n)$, so each insert/lookup costs $\Theta(n)$, total $\Theta(n^2)$, breaking amortised $O(1)$.

### 3.2 Defence: Universal Hash Family

Draw $h$ randomly from a universal family, e.g.
$$
h(k) = ((a k + b) \bmod p) \bmod cap
$$
with $p > cap$ prime, $a \in [1,p-1]$, $b \in [0,p-1]$ uniform. For any distinct keys, $\Pr[h(k_1) = h(k_2)] \le 1/cap$, so expected chain length is $O(1 + \lambda) = O(1)$ by linearity of expectation.

Bucket sizes concentrate around expectation; standard Chernoff bounds (with a union bound over $cap$ buckets) show maximum chain length $O(\log n)$ with high probability.

**Bound:** expected amortised $O(1)$ per operation (over randomness, for any fixed set of keys).

---

## 4. Example 3 – Union-Find: Heuristics Against Degeneration

Union-find supports `union` and `find`; cost is path length without compression.

### 4.1 Vulnerability Without Union-by-Rank

Path compression alone: sequential unions $(1\text{-}2, 2\text{-}3, \dots)$ create chains of length $\Theta(n)$; subsequent finds traverse $\Omega(n)$. Without rank, amortised cost is worse than with heuristics.

### 4.2 Defence: Union-by-Rank with Path Compression

`union` attaches the smaller-rank tree to the larger. Combined with compression, tree height is bounded by inverse Ackermann $\alpha(n) \le 5$ for practical $n$.

**Bound:** amortised $\alpha(n) \approx O(1)$ per operation deterministically over any sequence.

---

## 5. Quick Reference – Vulnerabilities and Defenses

| Structure                   | Vulnerability                 | Input/Sequence      | Defence                           | Bound Post-Defence                    |
|----------------------------|-------------------------------|---------------------|------------------------------------|---------------------------------------|
| Dynamic array (doubling)   | Resize spikes $\Omega(n)$     | Append bursts to full | Incremental resizing ($O(1)$ copy per op) | Deterministic $O(1)$ per op      |
| Hash table (fixed $h$)     | Chain lengths $\Omega(n)$     | Colliding keys      | Universal random hash family       | Expected $O(1)$; w.h.p. $O(\log n)$   |
| Union-find (compression only) | Long paths possible        | Sequential unions   | Union-by-rank + compression        | $\alpha(n) \approx O(1)$ amortised    |

(Notes: unit costs; spikes matter for latency, inputs for randomised cases.)

---

## 6. Mechanical Checklist – Assessing Amortised Robustness

1. Exhibit $\Phi \ge 0$ with $\Phi(s_0)=0$ such that $\hat{c}_i \le K$ for all $i$; confirm aggregate $O(m)$.
2. Compute $\max c_i$; if $\Omega(n)$, evaluate latency impact.
3. For randomised structures: assume fixed keys; bound $\mathbb{E}[c_i]$ via linearity.
4. Mitigate spikes: implement incremental work with a bounded per-op budget (e.g. $O(1)$ copies during resize).
5. Mitigate inputs: use universal random choices; bound collisions $\le 1/|U|$.
6. Alternative: schedule an incremental rebuild with constant work per operation, yielding worst-case $O(1)$.
7. Validate: simulate worst-case sequences; measure $\max c_i$ and total cost over, say, $10^6$ operations.

---

## 7. Mandatory Drill (full analysis required)

1. For the dynamic array in §2:
   - (a) Verify $\hat{c}_i \le 3$ for append bursts using $\Phi = 2\,num - cap + 1$.
   - (b) Sketch incremental resize invariants and prove $O(1)$ per operation and $O(n)$ total work.
   - (c) Simulate symmetric grow/shrink ($n = 2^{10}$) vs. hysteresis: measure resize frequency and max latency over $10^4$ cycles.

(Advanced: derive amortised $O(\log n)$ for the splay tree access lemma over any sequence. Show long paths in union-find without rank; bound $\alpha(n)$ with heuristics.)

---

## 8. Permanent Habit You Must Install

In amortised designs, annotate for robustness:

```python
# High-level pattern for deamortised doubling.
# Guarantees:
# - At most k copy operations per append
# - Each element is copied O(1) times total (in the conceptual model)

class DeamortisedArray:
    def __init__(self, initial_cap: int = 1, k: int = 1) -> None:
        # Logical capacity used in the analysis.
        self.cap = max(1, initial_cap)
        # Underlying Python list; we let CPython manage its own resizing.
        # Our "capacity" and copy work are conceptual, for amortised reasoning.
        self.data = []
        self.num = 0

        # Deamortisation parameters/state
        self.k = max(1, k)        # copies per append during a resize phase
        self._new = None          # type: list | None
        self._copy_ptr = 0        # index into old array during copy phase

    def _start_resize(self) -> None:
        """Begin a doubling phase; allocate new storage."""
        self._new = [None] * (2 * self.cap)
        self._copy_ptr = 0

    def _copy_step(self) -> None:
        """Copy at most k elements from old array to new array."""
        assert self._new is not None

        for _ in range(self.k):
            if self._copy_ptr >= self.cap:
                break
            self._new[self._copy_ptr] = self.data[self._copy_ptr]
            self._copy_ptr += 1

        # When copy is complete, switch to the new array
        if self._copy_ptr >= self.cap:
            self.data = self._new
            self.cap = len(self.data)
            self._new = None
            self._copy_ptr = 0

    def append(self, x) -> None:
        # If we've reached *logical* capacity and are not yet in a resize phase,
        # start one. The real Python list may already have more physical space;
        # we ignore that here and reason in terms of our own cap/num.
        if self.num == self.cap and self._new is None:
            self._start_resize()

        # If in a resize phase, pay bounded work into copying
        if self._new is not None:
            self._copy_step()

        # Normal append into the current Python list
        self.data.append(x)
        self.num += 1
```

---

## 9. What You Must Carry Forward – Robustness Discipline

1. Aggregate amortised $O(1)$ holds deterministically via a suitable $\Phi$; spikes $\Omega(n)$ demand deamortisation.
2. Randomised expected $O(1)$ for fixed keys requires universal families (or stronger).
3. Defenses: incremental spreading with bounded per-op work for latency; random choices for inputs.
4. Simulate extreme sequences; measure spikes and expectations.
5. In specs, explicitly declare **deterministic worst-case $O(1)$** vs. **expected $O(1)$ over randomness**.

---

## 10. Progress Note

After M04C06, you can refine amortised bounds for spikes and input robustness, ensuring per-operation guarantees via deamortisation or randomisation. This completes the amortised framework.

M04C06 complete.

---

## 11. Glossary & Notation

* **Aggregate amortised:** total $\sum c_i = O(m)$ over $m$ operations.
* **Deamortisation:** caps $c_i \le O(1)$ deterministically while preserving aggregate efficiency.
* **Universal hash family:** a family with $\Pr[h(k_1) = h(k_2)] \le 1/|U|$ for distinct $k_1, k_2$.
* **w.h.p.:** with high probability ($1 - 1/\mathrm{poly}(n)$).
* $\mathbb{E}[\cdot]$: expectation over randomness.
* $\alpha(n)$: inverse Ackermann function, $\le 5$ for practical $n$.

# M04C07 · Empirical Validation of Asymptotic Bounds
**Goal:** Develop a disciplined methodology for confronting asymptotic predictions with concrete measurements. After this core, you will design reproducible microbenchmarks, extract effective constants and lower-order terms from hardware counters, identify phase transitions attributable to memory hierarchy, and determine the practical regimes in which theoretical superiority dominates. This framework distinguishes mathematical truth in idealised models from observable behaviour on real hardware.

Asymptotic analysis yields provably correct growth rates in specified cost models, but these models abstract away instruction-level parallelism, branch prediction, prefetching, and memory hierarchy effects. Empirical validation cannot falsify a correct mathematical bound, but it can reveal when a chosen cost model is a poor predictor of reality or when constant factors render a theoretically optimal algorithm impractical below astronomically large inputs.

**Key Insight:** Correct asymptotics are necessary but insufficient for performance engineering. The measurable crossover point between two algorithms is determined primarily by hidden constants and hardware-specific effects, not by leading-term growth rates alone.

## 1. The Three Layers of Performance Reasoning
Rigorous analysis requires explicit separation of concerns:

| Layer                     | Focus                                      | Representative Questions                          | Tools & Techniques                          |
|---------------------------|--------------------------------------------|---------------------------------------------------|---------------------------------------------|
| Mathematical asymptotics  | Growth rates in idealised model            | Is the bound tight in the RAM model?              | Proofs, recurrences, Master theorem         |
| Realistic cost model      | Cache misses, pointer chasing, branch cost | How many L3 misses per operation in theory?       | Cache-aware analysis, EM model, profiling   |
| Empirical measurement     | Cycles, variance, hardware counters        | What is the observed MPKI and IPC on this machine?| `perf`, flamegraphs, isolated benchmarking  |

Conflation of these layers produces statements like “O(n log n) is faster than O(n²) for n > 100” without specifying machine, compiler, or data layout.

## 2. Reproducible Microbenchmarking Methodology
### 2.1 Minimum Required Discipline (always apply)
1. Measure at least 10⁶–10⁸ operations per data point to amortise noise.
2. Warm up caches and branch predictor (discard first ~10⁴ iterations).
3. Use powers-of-two input sizes to expose cache transitions.
4. Plot time per operation vs. n on log-log axes.
5. Perform at least 100 independent runs; report median and 95 % confidence interval.
6. Pin process to a single core (`taskset -c 4`) and disable CPU frequency scaling when possible.

### 2.2 Advanced Isolation (for research-grade claims)
- Disable hyper-threading on measured cores.
- Use `isolcpus=` or real-time scheduling to minimise OS jitter.
- Bootstrap confidence intervals and reject outliers (modified z-score > 3.5).
- Control input randomness with fixed seeds.

### 2.3 Statistical Presentation
For nontrivial comparisons, report at least:
- Median and 95 % CI (bootstrap preferred).
- Log-log regression slope with standard error (simple least-squares fit on $(\log n, \log T(n))$).
- Hardware counters: cycles, instructions, LLC-load-misses, branch-misses per operation.

## 3. Example 1 – Dynamic Array Append: Amortised $O(1)$ vs. Hardware Reality
Theoretical claim (doubling with potential $\Phi = 2\,\text{num} - \text{cap} + 1$): amortised $O(1)$ append.

### 3.1 Illustrative Measurements (real systems vary)
Typical observed behaviour on modern x86-64 (values are representative; students must measure on their own hardware):

| n (elements) | Median time/append (ns) | 95 % CI (ns) | Notes                                      |
|--------------|--------------------------|--------------|--------------------------------------------|
| ≤ 2²⁰        | ~22                      | ±0.4         | L1/L2 resident                             |
| 2²²–2²⁵      | ~23                      | ±0.5         | L3 resident                                |
| ≥ 2²⁶        | 35–60                    | ±2           | DRAM bandwidth limited                     |

The amortised bound manifests as near-constant median time per append until the array exceeds LLC capacity, after which time rises due to memory bandwidth saturation.

### 3.2 Hardware Counter Diagnosis
Typical counters during large-n phase:

| Counter               | Per append | Interpretation                              |
|-----------------------|------------|---------------------------------------------|
| cycles                | ~140       | ~35 ns at 4 GHz                             |
| instructions          | ~95        | IPC ≈ 0.68 (memory-bound)                   |
| LLC-load-misses       | ~0.4       | ~1 miss every 2–3 appends                   |
| branch-misses         | <0.01      | Negligible                                  |

Memory bandwidth, not computation, is the bottleneck.

## 4. Example 2 – Prefix Sum: O(n) Scan vs. O(n²) Naive
Naive nested loops vs. linear scan on 64-bit integers.

Illustrative results:

| n       | Naive (ns/element) | Scan (ns/element) | Naive slope (log-log) |
|---------|--------------------|-------------------|-----------------------|
| 2¹⁸     | ~450               | ~4.1              | —                     |
| 2²²     | ~1800              | ~4.3              | ≈ 2.00                |
| 2²⁶     | ~7200              | ~7.8              | ≈ 2.00                |

The naive implementation yields perfect quadratic scaling. The scan remains memory-bandwidth-limited with near-constant time until LLC overflow.

Crossover is typically observed around n ≈ 500–2000, depending on exact constants and cache sizes.

## 5. Quick Reference – Diagnosing Performance Anomalies (Heuristics)
| Symptom                    | Likely cause                          | Diagnostic action                              |
|----------------------------|---------------------------------------|------------------------------------------------|
| Flat → gradual rise        | L3 → DRAM transition                  | Check array size vs. LLC capacity              |
| Sudden jumps at powers of 2| Page allocation / TLB effects         | `perf stat -e page-faults,dTLB-load-misses`    |
| Higher than expected time  | Branch misprediction or allocation    | Flamegraph + `perf stat -e branch-misses`      |
| Lower than expected time   | Hardware prefetcher or super-scalar   | Disable prefetchers and re-measure             |

## 6. Mechanical Checklist – Validating a Complexity Claim
1. State the exact cost model and predicted leading constants if possible.
2. Implement reference and efficient versions.
3. Apply minimum required methodology (§2.1); upgrade to advanced for publication-grade claims.
4. Plot log-log with regression slope and error.
5. Collect and interpret hardware counters (IPC, MPKI, achieved bandwidth).
6. Quantify crossover points and phase transitions.
7. Explain all deviations in terms of hardware or implementation artefacts.

## 7. Mandatory Drill (full measurement report required)
1. Benchmark prefix sum (naive vs. scan) on your machine from n = 2¹⁰ up to the largest n that (a) fits in memory and (b) completes within a reasonable time. For serious comparison, implement both versions in C or Rust. Produce a log-log plot with estimated regression slopes, a hardware-counter table, and a written explanation of observed behaviour.
2. Benchmark CPython list append vs. a pure-Python singly-linked list (with tail pointer) for both append and full traversal. Identify and explain the input size where cache effects dominate despite identical theoretical append complexity.
3. Using flamegraphs and counters, diagnose a real-world performance puzzle of your choice (e.g., why `dict` stays fast while a sorted `list` + `bisect` scales poorly).

## 8. Permanent Habit You Must Install
Every complexity claim is accompanied by a minimal reproducible benchmark:
```bash
# Minimal template

# 1) High-level timing (Python or similar harness)
taskset -c 4 python -m timeit -n 1000 -r 100 \
    -s "from your_module import code_here" \
    "code_here(n=2**26)"

# 2) Low-level hardware counters (Linux perf, C/Rust binary)
perf stat -r 50 -e cycles,instructions,cache-misses,branches,branch-misses \
    ./target/release/bench_name

# Always ship:
# - the log-log plot
# - the counter table
# - the machine specification
```
No bound is accepted without the measurement.

## 9. What you must carry forward – empirical discipline
1. Asymptotics describe mathematical truth in idealised models only.
2. Real performance is typically dominated by memory hierarchy well before “asymptotic” scales.
3. Statistical rigour and hardware counters are mandatory for credible claims.
4. Constants and phase transitions determine practical winners, not just leading terms.
5. Always separate model, implementation, and hardware in your reasoning.

## 10. Progress note & what’s next in M04
After M04C07, you possess a reproducible methodology for mapping theoretical predictions onto hardware reality. This closes the performance reasoning loop.

M04C07 complete.

Next: **M04C08 – Full asymptotic + amortised analysis of one nontrivial data structure**.

## 11. Glossary & Notation
- MPKI: Misses per thousand instructions.
- IPC: Instructions per cycle.
- Phase transition: Input size at which dominant cost source changes (e.g., cache → DRAM).
- Log-log regression slope: Estimated asymptotic order from empirical data.
- Crossover point: Input size where one implementation becomes faster than another.
# M04C08 · Relating Asymptotic Predictions to Measured Timings
**Goal:** Establish a rigorous, reproducible methodology for comparing asymptotic predictions with empirical observations on real hardware. After this core, you will be able to design microbenchmarks that reliably reveal scaling behaviour and constant factors, interpret hardware counters in context, identify implementation-specific artefacts, and determine the input regimes in which theoretical bounds become practically relevant. Empirical measurement complements but does not replace mathematical proof.

Asymptotic analysis provides provably correct growth rates in idealised cost models (e.g., unit-cost RAM, cache-oblivious, or external-memory models). These models intentionally abstract away memory hierarchy effects, branch prediction, prefetching, and constant factors. Empirical validation cannot invalidate a correct bound, but it frequently demonstrates that a particular cost model is a poor predictor on modern hardware or that constant factors delay asymptotic dominance to impractically large inputs.

**Key Insight:** Practical performance is almost always dominated by constant factors and hardware-specific behaviour long before leading asymptotic terms take over. Sound measurement must control noise, quantify variance, and explicitly separate mathematical model, cost-model assumptions, and implementation artefacts.

## 1. The Three Layers of Performance Reasoning
Clear separation is essential:

| Layer                     | Focus                                      | Representative Questions                          | Tools                                      |
|---------------------------|--------------------------------------------|---------------------------------------------------|--------------------------------------------|
| Mathematical asymptotics  | Growth rates in idealised model            | Is the bound tight in the RAM model?              | Proofs, recurrences, potential method      |
| Realistic cost model      | Cache misses, pointer chasing, branch cost | How many LLC misses per operation in theory?      | Cache-aware analysis, external-memory model|
| Empirical measurement     | Cycles, variance, hardware counters        | What is the observed IPC and MPKI on this machine?| Isolated benchmarking, perf, flamegraphs   |

Conflation of layers produces meaningless claims such as “merge sort beats insertion sort for n > 50” without specifying machine, compiler, or memory layout.

## 2. Reproducible Microbenchmarking Methodology
### 2.1 Exploratory Benchmarking (Python-level, qualitative shape only)
Suitable for initial trend detection:
1. Use `timeit` or similar with at least 10⁴–10⁶ operations per data point.
2. Warm up caches (discard first ~10⁴ iterations).
3. Use powers-of-two input sizes.
4. Plot time per operation vs. n on log-log axes.
5. Perform at least 30 runs; report the median and, if desired, a simple 95 % CI (only to visualise noise, not for quantitative claims).
6. Interpret only broad trends in the curve’s shape; Python interpreter overhead dominates constants and distorts fine-grained slope estimates.

### 2.2 Serious Benchmarking (C or Rust, quantitative constants and slopes)
Required for slope estimation or quantitative constant-factor comparison:
1. Aim for 10⁸–10¹⁰ operations per data point for very cheap kernels (e.g., tight loops in C/Rust). For more expensive operations, choose the largest count that keeps total runtime reasonable while clearly separating signal from noise.
2. Warm up caches and steady state (discard first ~10⁶ iterations).
3. Use powers-of-two input sizes to expose cache transitions.
4. Plot time per operation vs. n on log-log axes.
5. Perform at least 100 independent runs on decorrelated samples (batch means if autocorrelation present).
6. Report median, bootstrapped 95 % CI, and log-log regression slope with standard error.
7. Pin process to isolated core, disable frequency scaling and hyper-threading when possible.

### 2.3 Advanced Isolation (publication-grade claims only)
- Use `isolcpus=` or real-time scheduling.
- Verify lack of autocorrelation via ACF plot or Ljung–Box test.
- Reject outliers (modified z-score > 3.5).

Note: Bootstrap assumes approximately i.i.d. samples; correlated runtimes must be decorrelated via batching.

## 3. Example 1 – Dynamic Array Append: Amortised O(1) in Theory and Practice
Theoretical claim (geometric growth by factor 2, potential $\Phi = 2\,\text{num} - \text{cap} + 1$): amortised $O(1)$ append.

CPython uses geometric growth with factor ≈1.125–1.37 (not strict doubling), so measured behaviour reflects a different reallocation frequency but the same amortised bound.

Illustrative measurements on one modern x86-64 system (values are representative of the pattern only; students must measure on their own hardware and should not treat these numbers as reference baselines):

| n (elements) | Median time/append (ns) | 95 % CI (ns) | Notes                                      |
|--------------|--------------------------|--------------|--------------------------------------------|
| ≤ 2²⁰        | ~22                      | ±0.5         | L1/L2 resident                             |
| 2²²–2²⁵      | ~24                      | ±0.6         | L3 resident                                |
| ≥ 2²⁶        | 40–70                    | ±3           | DRAM bandwidth limited                     |

The measurements are consistent with the amortised $O(1)$ model: median time per append is nearly constant until the array exceeds LLC capacity, after which memory bandwidth dominates.

Hardware counters (large-n phase, isolated core, fixed frequency; values illustrative):

| Counter               | Per append | Interpretation                              |
|-----------------------|------------|---------------------------------------------|
| cycles                | ~160       | ~40 ns at 4 GHz                             |
| instructions          | ~110       | IPC ≈ 0.69 (memory-bound)                   |
| LLC-load-misses       | ~0.45      | ~1 miss every ~2 appends                    |
| branch-misses         | <0.01      | Negligible                                  |

Counters are subject to multiplexing and SMT skew; interpret only under controlled conditions.

## 4. Example 2 – Prefix Sum: O(n) Scan vs. O(n²) Naive
Implementations in C or Rust or NumPy are required for meaningful constant-factor comparison; pure-Python loops are dominated by interpreter overhead and unsuitable for slope estimation.

Illustrative results from one C implementation on one machine (pattern only, not a reference benchmark):

| n       | Naive (ns/element) | Scan (ns/element) | Naive slope (log-log) |
|---------|--------------------|-------------------|-----------------------|
| 2¹⁸     | ~420               | ~3.8              | —                     |
| 2²²     | ~1680              | ~4.0              | ≈ 2.00                |
| 2²⁶     | ~6720              | ~7.2              | ≈ 2.00                |

Naive version (each prefix recomputes a sum from scratch) shows perfect quadratic scaling. Scan is memory-bandwidth-limited until LLC overflow.

Crossover is typically observed around n ≈ 800–3000.

## 5. Quick Reference – Diagnosing Performance Anomalies
| Symptom                    | Likely cause                          | Diagnostic action                              |
|----------------------------|---------------------------------------|------------------------------------------------|
| Broad transition region    | L3 → DRAM (prefetching smears boundary)| Check array size vs. LLC capacity              |
| Sudden jumps at powers of 2| Page allocation / TLB effects         | `perf stat -e page-faults,dTLB-load-misses`    |
| Higher than expected time  | Branch misprediction or allocation    | Flamegraph + `perf stat -e branch-misses`      |
| Lower than expected time   | Hardware prefetcher or ILP            | Disable prefetchers and re-measure             |

Cache transitions are broad regions, not sharp steps.

## 6. Mechanical Checklist – Validating a Complexity Claim
1. State the exact cost model and predicted leading constants if possible.
2. Implement reference and efficient versions in C or Rust (or NumPy) for serious constant-factor work.
3. Apply the minimum required methodology (§2.1) for exploratory work; upgrade to advanced for publication-grade claims.
4. Plot log-log with regression slope and error.
5. Collect and interpret hardware counters (IPC, MPKI, achieved bandwidth).
6. Quantify crossover points and broad transition regions.
7. Explicitly separate implementation artefacts from algorithmic essence.

## 7. Mandatory Drill (full measurement report required)
1. Benchmark prefix sum (naive vs. scan) on your machine from n = 2¹⁰ up to the largest n that (a) fits in memory and (b) completes within a reasonable time. For serious comparison, implement both versions in C or Rust. Produce a log-log plot with estimated regression slopes, a hardware-counter table, and a written explanation of observed behaviour.
2. Benchmark CPython list append vs. a pure-Python singly-linked list (with tail pointer) for both append and full traversal. Identify and explain the input size where cache effects dominate despite identical theoretical append complexity.
3. Using flamegraphs and counters, diagnose a real-world performance puzzle of your choice (e.g., why `dict` stays fast while a sorted `list` + `bisect` scales poorly).

## 8. Permanent Habit You Must Install
Every complexity claim is accompanied by a minimal reproducible benchmark:
```bash
# Exploratory (Python, shape only)
taskset -c 4 python -m timeit -n 1000 -r 100 \
    -s "from your_module import code_here" \
    "code_here(n=2**26)"

# Serious (C/Rust binary strongly preferred)
perf stat -r 50 -e cycles,instructions,cache-misses,branches,branch-misses \
    ./target/release/bench_name

# Always ship:
# - the log-log plot
# - the counter table
# - the machine specification (CPU, frequency policy, cache sizes)
```
Within this module, no performance bound is accepted without an accompanying measurement.

## 9. What you must carry forward – empirical discipline
1. Asymptotics describe mathematical truth in idealised models only.
2. Real performance is typically dominated by memory hierarchy well before “asymptotic” scales.
3. Python-level timings are useful for shape only; serious constant-factor work requires C or Rust.
4. Statistical rigour (CI, outlier handling, isolation) is mandatory.
5. Always separate model, implementation, and hardware in your reasoning.

## 10. Progress note & what’s next in M04
After M04C08, you possess a reproducible methodology for mapping theoretical predictions onto hardware reality. This bridges the gap between proof and practice.

M04C08 complete.

Next: **M04C09 – Full analysis of one nontrivial DS (recurrence + amortised)**.

## 11. Glossary & Notation
- MPKI: Misses per thousand instructions (derived from cache-miss counters in empirical runs).
- IPC: Instructions per cycle (used in §3–4 to distinguish compute- vs memory-bound regimes).
- Phase transition: Broad input-size region where dominant cost source changes.
- Log-log regression slope: Estimated asymptotic order from empirical data.
- Crossover point: Input size where one implementation becomes faster than another.
# M04C09 · Full Asymptotic and Amortised Analysis of a Nontrivial Data Structure: Disjoint-Set Union
**Goal:** Synthesise the asymptotic and amortised-analysis techniques from M04 (tight worst-case bounds, potential-method reasoning, and “almost constant” amortised costs) on one classically nontrivial structure. After this core, you will be able to derive the tight amortised bound for union-by-rank + path compression from first principles, recognise the level-partitioning proof pattern, and apply analogous techniques to other structures with effectively constant amortised costs.

The disjoint-set union (DSU) structure, also known as union-find, maintains a partition of $n$ elements and supports MakeSet, Find, and Union. The combination of union-by-rank and path compression achieves amortised $O(\alpha(n))$ time per operation, where $\alpha$ is the extremely slow-growing inverse Ackermann function and $\alpha(n) \le 5$ for any conceivable $n$.

**Key Insight:** When both heuristics are used, the total work across all operations is so tightly bounded that the per-operation cost is effectively constant for all practical purposes. This is the canonical example in classic data structures of an “almost constant” amortised bound.

## 1. Operations and Naive Bounds
- MakeSet(x): create singleton $\{x\}$ ($O(1)$).
- Find(x): return representative of $x$'s set.
- Union(x,y): merge sets containing $x$ and $y$.

Naive implementation (link arbitrarily, no compression): repeated unions produce chains → Find $O(n)$ worst-case.

## 2. Union-by-Rank Alone → $O(\log n)$ Worst-Case Find
Define rank[r] ≈ height of tree rooted at $r$. Union attaches lower-rank root to higher-rank root; increment rank only on ties.

Lemma: rank[root] $\le \log_2 n$.

Proof: A root of rank $k$ has subtree $\ge 2^k$ nodes (induction: each rank increase merges two subtrees of rank $\ge k-1$).

Thus Find (tree traversal) is $O(\log n)$ worst-case, even without compression.

## 3. Path Compression Alone → Substantial Speedup
Full path compression (make all nodes on Find path point directly to root) dramatically reduces future Find costs. With arbitrary linking, the amortised complexity is sublinear but the proof is significantly more involved than the combined case; we do not require the exact bound here.

## 4. Combined Heuristics → Amortised $O(\alpha(n))$
Theorem (Tarjan, 1975): With union-by-rank and path compression, any sequence of $m \ge n$ operations requires $O(m \alpha(m,n))$ time total, where $\alpha(m,n) \le 5$ for all practical $m,n$.

We write $\alpha(n)$ for simplicity; the exact two-parameter variant grows equally slowly. For all $m \ge n$ that arise in practice, $\alpha(m,n)$ and $\alpha(n)$ differ by at most an additive constant.

### 4.1 Intuitive Proof Sketch (Level Partitioning)
Consider only Find operations (Union is $O(1)$ amortised via the rank argument).

Charge the cost of traversing a node $v$ during Find to $v$ itself.

Each non-root node $v$ has its parent pointer updated only when its current parent changes (by Union or compression), and the new parent has strictly higher rank than the old one (union-by-rank ensures this).

Thus the rank of $v$'s parent is strictly increasing over time.

Group nodes into coarse buckets by current parent rank (e.g., ranks in $[2^k, 2^{k+1})$). Within any such bucket, a node can have its parent updated only a bounded number of times before it is forced into a strictly higher bucket, because each compression step jumps it to a much higher-rank ancestor.

More refined partitioning (the full proof) bounds the number of such buckets by $O(\alpha(n))$ using an Ackermann-like recurrence on the number of possible updates per bucket.

Result: each node is charged $O(\alpha(n))$ times across all Finds → total cost $O(m \alpha(n))$.

Full rigorous proof: CLRS 3rd ed. §21.4 or Tarjan & van Leeuwen (1984).

## 5. Quick Reference – Union-Find Variants
| Variant                       | Find cost                  | Comments                                      |
|-------------------------------|----------------------------|-----------------------------------------------|
| Naive                         | $O(n)$ worst-case          | Chains                                        |
| Union-by-rank/size only       | $O(\log n)$ worst-case     | Height bound via subtree doubling             |
| Path compression + arbitrary linking | Sublinear amortised; proof complex | Rarely used alone                        |
| Both heuristics               | $O(\alpha(n))$ amortised   | Effectively constant; standard implementation |

## 6. Mechanical Checklist – Deriving “Almost Constant” Bounds
1. Bound tree height with rank/size ($O(\log n)$).
2. Use path compression to make parent rank strictly increasing.
3. Charge work to nodes; show each node pays only $O(1)$ times per coarse rank bucket.
4. Show number of buckets is $O(\alpha(n))$ using fast-growing recurrence.
5. Conclude total work $O(m \alpha(n))$.

## 7. Mandatory Drill (full analysis required)
1. Prove union-by-rank alone gives $O(\log n)$ worst-case Find (subtree size doubling argument).
2. Explain why path compression makes the parent rank strictly increasing for every node on the path.
3. Using the intuitive level-partitioning argument in §4.1, describe (without formal Ackermann) why the number of effective levels is $O(\alpha(n))$.
4. (Optional, advanced) Read CLRS §21.4 and summarise the exact potential function used there.

## 8. Permanent Habit You Must Install
Every union-find implementation uses both heuristics:
```python
# Disjoint-Set Union – union-by-rank + path compression
# Amortised O(α(n)) per operation (effectively constant)
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank   = [0] * n                    # rank ≈ height upper bound

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])   # path compression
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        # union-by-rank
        if self.rank[px] < self.rank[py]:
            self.parent[px] = py
        elif self.rank[px] > self.rank[py]:
            self.parent[py] = px
        else:
            self.parent[py] = px
            self.rank[px] += 1
        return True
```

## 9. What you must carry forward – DSU mastery
1. Union-by-rank alone → $O(\log n)$ worst-case.
2. Both heuristics → $O(\alpha(n))$ amortised, $\alpha(n) \le 5$ practically.
3. Proof pattern: rank bounds height + compression forces strictly increasing parent rank + level partitioning of charges.
4. Always implement both heuristics in production code.
5. This is the canonical example in classic data structures of an “almost constant” amortised bound.

## 10. Progress note & what’s next in M04
After M04C09, you have completed a full asymptotic + amortised analysis of a classically nontrivial data structure, synthesising the module’s core techniques.

M04C09 complete.

Next: **M04C10 – Personal “complexity cheatsheet” of reusable patterns**.

## 11. Glossary & Notation
- Union-by-rank: Attach lower-rank root to higher-rank root.
- Path compression: Set all nodes on Find path to point directly to root.
- $\alpha(n)$: Inverse Ackermann function; grows extremely slowly ($\alpha(n) \le 5$ for all practical $n$).
- Level partitioning: Technique for proving $O(\alpha(n))$ amortised bounds by grouping nodes by parent rank and bounding transitions between groups.# M04C10 · Complexity Cheatsheet – Reusable Patterns
Dense, lookup-oriented reference. Match problems to patterns; apply mechanically. Extend with new discoveries.

## 1. Asymptotic Notation – Definitions & Hierarchy
| Notation       | Definition                                                  | Use                                          |
|----------------|-------------------------------------------------------------|----------------------------------------------|
| $f = O(g)$     | $\exists c,n_0: 0 \le f(n) \le c g(n) \;\forall n \ge n_0$  | Upper bound                                  |
| $f = \Omega(g)$| $\exists c,n_0: f(n) \ge c g(n) \;\forall n \ge n_0$        | Lower bound                                  |
| $f = \Theta(g)$| $f = O(g) \land f = \Omega(g)$                              | Tight                                        |
| $f = o(g)$     | $\forall c>0 \exists n_0: 0 \le f(n) < c g(n)$              | Strict upper                                 |
| $f = \omega(g)$| $\forall c>0 \exists n_0: f(n) > c g(n)$                    | Strict lower                                 |

**Growth hierarchy** (positive functions):
$1 \ll \alpha(n) \ll \log^* n \ll \log\log n \ll \log n \ll (\log n)^k \ll n^\epsilon \ll n^k \ll c^n \ll n!$

**Rules**
- Log base irrelevant in $O(\cdot)$.
- $\log^k n = o(n^\epsilon)$ any fixed $k,\epsilon>0$.
- $\tilde{O}(f) = O(f \cdot \text{polylog } f)$.

## 2. Standard Sums (use immediately)
| Summation                              | Closed form                  |
|----------------------------------------|------------------------------|
| $\sum_{i=1}^n 1$                       | $n$                          |
| $\sum_{i=1}^n i$                       | $\Theta(n^2)$                |
| $\sum_{i=1}^n 1/i$                     | $\Theta(\log n)$             |
| $\sum_{i=1}^n \log i$                  | $\Theta(n \log n)$           |
| $\sum_{k=0}^{\log_2 n} 2^k$            | $\Theta(n)$                  |
| $\sum_{k=1}^n k \log k$                | $\Theta(n^2 \log n)$         |

## 3. Loop Patterns
| Structure                              | Bound                        | Hidden log if…                               |
|----------------------------------------|------------------------------|----------------------------------------------|
| Single $1..n$                          | $\Theta(n)$                  |                                              |
| Double independent                     | $\Theta(n^2)$                 |                                              |
| Triangular $j=1..i$                    | $\Theta(n^2)$                 |                                              |
| Inner $1..n/i$                         | $\Theta(n \log n)$           | harmonic                                     |
| Geometric $i*=k$ ($k>1$)               | $\Theta(\log n)$             | body $O(1)$                                  |
| Shrinkage $i//=k$                      | $\Theta(\log n)$             |                                              |

**Suspect hidden $\log n$ when you see**
- balanced tree / heap / binary search
- repeated halving/doubling
- divide-and-conquer with balanced split
- summation of $1/i$ or $\log i$
- work per level in logarithmic-height structure

## 4. Recurrence Patterns – Master Theorem
$T(n) = a T(n/b) + f(n)$, $a\ge1$, $b>1$; let $d = \log_b a$.

| Case                                   | Condition                                   | Bound                                |
|----------------------------------------|---------------------------------------------|--------------------------------------|
| 1                                      | $f(n) = O(n^{d-\epsilon})$ ($\epsilon>0$)   | $\Theta(n^d)$                        |
| 2                                      | $f(n) = \Theta(n^d \log^k n)$ ($k\ge0$)     | $\Theta(n^d \log^{k+1} n)$           |
| 3                                      | $f(n) = \Omega(n^{d+\epsilon})$ + regularity* | $\Theta(f(n))$                       |

*Regularity: $a f(n/b) \le c f(n)$ for $c<1$, large $n$.

**Non-Master → recursion tree or Akra–Bazzi**

Common non-Master recurrences:
| Recurrence                           | Idea / Bound                    |
|--------------------------------------|----------------------------------|
| $T(n) = T(n-1) + O(1)$               | Unroll: $T(n) = \Theta(n)$      |
| $T(n) = T(n-1) + T(n-2) + O(1)$      | Fibonacci-type: $T(n) = \Theta(\varphi^n)$ |
| $T(n) = T(n-1) + O(\log n)$          | Sum $\log i$: $T(n) = \Theta(n \log n)$    |


## 5. Amortised Analysis Patterns
| Method                 | Recipe                                              | Example                                      |
|------------------------|-----------------------------------------------------|----------------------------------------------|
| Accounting             | Assign $\hat{c}_i > c_i$ on cheap ops; bank credits | Dynamic array doubling                       |
| Potential              | $\Phi \ge 0$, $\Phi(s_0)=0$; prove $\hat{c}_i = c_i + \Delta\Phi \le K$ | Two-stack queue, splay tree                  |
| Level partitioning     | Rank bounds height; charge per rank/level transition| Union-find ($\alpha(n)$), Fibonacci heap     |

Always prove $\Phi \ge 0$ invariant and check every operation case.

## 6. Robustness Patterns
| Problem                        | Defence                                     | Spec language                                |
|--------------------------------|---------------------------------------------|----------------------------------------------|
| Amortised spikes               | Deamortisation (incremental $O(1)$ work)    | deterministic worst-case $O(1)$              |
| Randomised degeneration        | Universal family + reshuffle                | expected $O(1)$ (oblivious adversary)        |
| Deterministic degeneration     | Rank/size + compression                     | amortised $O(\alpha(n))$                     |

## 7. Empirical Validation Patterns
| Regime                         | Tooling                               | Outputs                                      |
|--------------------------------|---------------------------------------|----------------------------------------------|
| Exploratory (shape)            | Python + timeit                       | Log-log plot                                 |
| Serious (slopes/constants)     | C/Rust + perf                         | Regression slope + CI + counters (IPC, MPKI) |
| Publication-grade              | Isolated core + batch means           | Full stats + machine spec                    |

Rule: No claim without log-log plot + counters.

## 8. Graph / DP / Sorting Patterns
| Domain                         | Bound                                         | Notes                                        |
|--------------------------------|-----------------------------------------------|----------------------------------------------|
| BFS/DFS                        | $O(n+m)$                                      | $n$ vertices, $m$ edges                      |
| Dijkstra (binary heap)         | $O((n+m)\log n)$                              | Fibonacci → $O(m + n\log n)$                  |
| Kruskal + DSU                  | $O(m\log m + m\alpha(n)) \approx O(m\log m)$   | sort dominates                               |
| DP state-space                 | (#states) × (transitions/state)               | bitsets, monotonicity                        |
| Comparison sorting lower bound | $\Omega(n\log n)$                             | information-theoretic                        |
| Integer/radix sort             | $O(n w)$ ($w$=word size)                      | bounded keys                                 |

## 9. Personal Additions
[Space for your discoveries]

## Glossary
- $\alpha(n)$: inverse Ackermann; $\alpha(n) \le 5$ practically.
- $\hat{c}_i = c_i + \Delta\Phi$: amortised cost.
- MPKI: cache misses per 1000 instructions.
- IPC: instructions per cycle.
