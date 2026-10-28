---
module_id: ALGE-098
program: Algorithm Engineering
level: 2
module_number: 98
title: Numerical Stability in Algorithm Implementation
status: complete
last_verified: 2026-09-05
---

# Numerical Stability in Algorithm Implementation

## One-Page Review

### Governing question

How do we implement an algorithm over finite arithmetic so that rounding, cancellation, overflow, underflow, scaling, ordering, and stopping decisions do not invalidate its mathematical contract?

### Essential definitions

- **roundoff error** is the difference introduced when an exact result is represented or computed in finite arithmetic.
- **unit roundoff** $u$ bounds relative error for correctly rounded basic operations under stated normal-range assumptions.
- **conditioning** describes sensitivity of the mathematical problem to input perturbations.
- **stability** describes whether an algorithm behaves like an exact computation on nearby data.
- **forward error** compares the computed output with the exact output for the original input.
- **backward error** asks how much the input must change for the computed output to be exact.
- **cancellation** occurs when subtracting close values exposes error already present in their leading digits.
- A **robust predicate** returns a topologically or logically correct discrete decision despite finite arithmetic, often by filtering then increasing precision.

### Central model, mechanism, or theorem

For a basic operation in round-to-nearest arithmetic, away from exceptional overflow and underflow,

$$
\operatorname{fl}(a\circ b)=(a\circ b)(1+\delta),\qquad |\delta|\le u.
$$

This local model does not itself prove a whole implementation stable. For a problem $y=f(x)$, a backward-stable algorithm returns $\hat y=f(x+\Delta x)$ with small $\Delta x$. Forward error is then controlled by both backward error and problem conditioning. A stable algorithm cannot recover information destroyed by an ill-conditioned problem, while an unstable algorithm can lose accuracy even on well-conditioned inputs.

### Critical invariants

- Numeric type, rounding mode, exceptional-value policy, input domain, scale, units, and accuracy obligation are explicit.
- Mathematical identities are not assumed equivalent after rounding, overflow, underflow, or compiler reassociation.
- Error analysis follows the actual operation order and precision.
- Discrete control decisions use a justified error bound, exact method, or explicit indeterminate path.
- Rescaling preserves the intended mathematical result and handles zero and exceptional inputs.
- Stopping tests use meaningful residual and scale, not exact equality or an arbitrary absolute epsilon.
- Higher-precision or exact references are independent of the implementation under test.
- Performance optimization cannot silently weaken reproducibility, robustness, or semantic guarantees.

### Common failures

Treating real-number algebra as machine semantics; saying “double precision has 15 correct digits” without scale or conditioning; subtracting nearly equal approximations; computing norms by squaring values that overflow; using the textbook quadratic formula for both roots; summing mixed magnitudes in arbitrary order; comparing floats with one universal epsilon; using a small residual as proof of small forward error without conditioning; allowing NaN to fall through comparisons; changing reduction order while claiming bitwise reproducibility; hiding underflow with flush-to-zero; and testing only ordinary well-scaled inputs.

### Compact example

In binary64, evaluating $10^{16}+1-10^{16}$ from left to right yields 0 because the unit increment is lost at the first addition. The exact real result is 1. A high-quality summation routine that tracks rounding remnants can return 1 for this finite sequence. The lesson is not that one library call solves all error: order, condition, dynamic range, subnormals, exceptional values, and the required guarantee still belong in the contract.

### Connections

[ALGE-009](./009-machine-models-and-hidden-constants.md) separates computation models, [ALGE-036](./036-dijkstra-s-shortest-paths.md) exposes weight and comparison semantics, [ALGE-082](./082-parallel-prefix-and-reduction.md) changes evaluation order, [ALGE-090](./090-mapping-an-algorithm-across-memory-threads-and-storage.md) exposes hardware mapping, and [ALGE-093](./093-profiling-time-memory-and-i-o.md) prevents speed from masking semantic regressions. ALGE-099 next reproduces published claims, including their numeric environment.

## Governing Question

For a declared input domain and output obligation, what finite-arithmetic implementation, error argument, exceptional-value policy, and verification evidence justify trusting each numeric result and control decision?

## Why This Matters

An algorithm proved correct over integers or real numbers is not automatically correct in machine arithmetic. Floating-point addition is not associative, integer arithmetic may overflow, transcendental functions have implementation contracts, and compiler or accelerator transformations may change evaluation. Small numeric discrepancies can become discrete failures: a geometry predicate flips orientation, a priority comparison changes a path, or a convergence test terminates too early.

Numerical reliability is not synonymous with using more bits. Precision is one resource among reformulation, scaling, compensation, exact predicates, interval bounds, and independent verification. The engineering task is to meet a quantified obligation at acceptable time, memory, energy, portability, and reproducibility cost.

## Prerequisites and Retrieval

Retrieve input and output contracts from [ALGE-001](./001-problem-statements-inputs-outputs-and-constraints.md), machine models from [ALGE-009](./009-machine-models-and-hidden-constants.md), proof/measurement boundaries from [ALGE-010](./010-combining-proof-and-measurement-in-algorithm-evaluation.md), shortest-path hypotheses from [ALGE-036](./036-dijkstra-s-shortest-paths.md), approximation obligations from [ALGE-061](./061-approximation-ratios-and-guarantees.md), parallel reduction structure from [ALGE-082](./082-parallel-prefix-and-reduction.md), hardware mapping from [ALGE-090](./090-mapping-an-algorithm-across-memory-threads-and-storage.md), and experimental comparison from [ALGE-096](./096-comparing-implementations-statistically.md).

## Learning Objectives

After this module, you should be able to:

1. state a finite-arithmetic model with its range, rounding, and exceptional assumptions;
2. distinguish representation error, forward error, backward error, residual, conditioning, and stability;
3. derive first-order sensitivity and rounding-error bounds for simple algorithms;
4. reformulate cancellation-prone, overflow-prone, and underflow-prone calculations;
5. select summation, scaling, predicate, and precision strategies from an error budget;
6. govern NaN, infinity, signed zero, subnormal, integer overflow, and mixed-precision behavior;
7. test numerical code with independent oracles, adversarial generators, properties, and cross-environment evidence; and
8. balance accuracy, robustness, reproducibility, and performance without overstating proof.

## Core Exposition

### Specify the numeric contract

Name input units, ranges, distributions, correlation, and exceptional values. Name the mathematical target and output form: correctly rounded value, relative or absolute tolerance, certified interval, residual, topological decision, feasible solution, or reproducible bit pattern. A tolerance meaningful for temperature may be meaningless for a determinant near zero.

Record storage and evaluation formats separately. Values can be stored in binary32, accumulated in binary64, evaluated through fused multiply-add, or promoted inconsistently. State rounding mode, subnormal behavior, overflow policy, library/version, compiler flags, device, and whether contractions or reassociation are allowed. “IEEE 754” alone does not fix every language, compiler, and library choice [1].

### Separate problem conditioning from algorithm stability

Conditioning belongs to the mathematical map. For scalar differentiable $f$, a local relative condition estimate is

$$
\kappa_f(x)=\left|\frac{x f'(x)}{f(x)}\right|
$$

when the denominator is nonzero. A small relative input perturbation can be magnified by approximately $\kappa_f(x)$. Absolute conditioning is appropriate near zero or when units make relative error meaningless.

Stability belongs to the procedure. Backward stability is powerful when the input perturbation is small in a problem-relevant norm and conditioning converts it to acceptable forward error. It is not a universal badge: componentwise and normwise perturbations differ, structured inputs may require structured perturbations, and a tiny backward error can coexist with large forward error for an ill-conditioned problem.

### Track local rounding without folklore

Under normal-range round-to-nearest assumptions, one operation has relative error bounded by $u$. Products of terms $1+\delta_i$ are often summarized by

$$
\gamma_n=\frac{nu}{1-nu},\qquad nu<1.
$$

The bound depends on operation count and structure. It excludes overflow and may need care around subnormals or zero. Worst-case bounds can be pessimistic, but observed accuracy does not replace them when a guarantee is required. Stochastic error models need explicit distributional premises.

### Reformulate cancellation-prone expressions

Subtraction is exact in some close-ratio cases under specific floating-point hypotheses, but the inputs may already contain error. In $1-\cos x$ for small $x$, cosine rounds near one and subtraction exposes lost digits. Use $2\sin^2(x/2)$ when its domain and library behavior fit. For $\sqrt{x+1}-\sqrt{x}$, rationalize to $1/(\sqrt{x+1}+\sqrt{x})$.

The quadratic formula can lose one root when $-b$ nearly cancels $\sqrt{b^2-4ac}$. Compute $q=-\tfrac12(b+\operatorname{sign}(b)\sqrt{D})$, then roots $q/a$ and $c/q$, with separate handling of zero, repeated roots, complex domains, scaling, and overflow in the discriminant.

### Scale before dangerous intermediate operations

Computing $\sqrt{x^2+y^2}$ can overflow even when the norm is representable, or underflow both squares. Let $m=\max(|x|,|y|)$; for $m>0$, compute $m\sqrt{(x/m)^2+(y/m)^2}$. A production hypot routine also handles infinities, NaNs, signed zeros, and wider argument sets under its specification.

Scaling supports matrix factorization, polynomial evaluation, probability normalization, and distance calculations. Preserve units and map the result back. Dynamic scaling that depends on data can change branches; test thresholds near transitions and include scaling cost in performance evidence.

### Sum and reduce according to the obligation

Naive left-to-right summation can lose small addends and has an error bound proportional to accumulated magnitude. Pairwise or tree summation reduces depth and often error growth; compensation tracks a lost low-order term; higher-precision accumulation expands cost and range. No method makes an ill-conditioned sum of heavily cancelling signed terms well-conditioned.

Parallel reductions legitimately change parenthesization and therefore bits. A fixed tree improves run-to-run reproducibility for fixed topology, not necessarily across device counts. Exact or long accumulators can provide stronger reproducibility at higher cost. State whether the contract is a tolerance, faithfully/correctly rounded sum, deterministic result, or statistical equivalence.

### Execute a compensated-summation illustration

The reference contrasts an explicit naive left-to-right loop with an accuracy-oriented library implementation on one adversarial ordering. It also checks permutation sensitivity. The observed library behavior is specific to CPython and its numeric library versions [9].

<!-- bijux-verify: {"id":"summation-order-and-compensation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"exact_integer_target: 1\nnaive_left_to_right: 0.0\nnaive_reverse_order: 0.0\nnaive_small_terms_first: 1.0\naccurate_fsum: 1.0\n","stderr":""}} -->
```python
from math import fsum


def naive_sum(items):
    total = 0.0
    for item in items:
        total += item
    return total


values = [1.0e16, 1.0, -1.0e16]
print("exact_integer_target:", 10**16 + 1 - 10**16)
print("naive_left_to_right:", naive_sum(values))
print("naive_reverse_order:", naive_sum(reversed(values)))
print("naive_small_terms_first:", naive_sum([1.0e16, -1.0e16, 1.0]))
print("accurate_fsum:", fsum(values))
```

The result demonstrates non-associativity and one effective implementation, not a proof about arbitrary sequences. For positive and negative data, condition number $\sum_i |x_i|/|\sum_i x_i|$ can be enormous. Test chosen accumulation across representative and adversarial distributions.

### Make predicates robust

A numeric value can tolerate error while its sign drives a discontinuous decision. Orientation, incircle, intersection, heap ordering, and feasibility predicates can corrupt topology if a rounded value crosses zero. A fixed epsilon creates a fuzzy band whose appropriate scale varies with inputs and transformation.

Use a filtered predicate: evaluate cheaply with a proven error bound; accept the sign only when magnitude exceeds the bound; otherwise increase precision or use exact arithmetic. Adaptive exact predicates can make the common case fast while preserving a discrete guarantee under their assumptions [5]. Keep construction coordinates consistent with predicates; exact decisions over already rounded inputs do not recover the original real geometry.

### Handle exceptional values deliberately

NaN is unordered under ordinary comparisons, so a branch such as “if not less, greater” is invalid. Infinities may be valid sentinels or evidence of overflow; distinguish them. Signed zero affects reciprocals and some branch-sensitive functions. Subnormals extend gradual underflow but may be flushed on some execution paths. Test and record actual environment behavior.

Integer overflow deserves the same rigor. Use checked arithmetic, wider types, preconditioned comparisons, or big integers as the contract requires. Rewriting $a+b<c$ to avoid overflow is valid only after signedness and domain analysis. Mixed integer/floating conversions can lose exact identity above the format's consecutive-integer range.

### Design stopping tests from residual and scale

Never wait for iterates to become exactly equal unless the algorithm proves finite stabilization. A common scaled test combines absolute and relative terms:

$$
\|x_{k+1}-x_k\|\le \tau_{\mathrm{abs}}+\tau_{\mathrm{rel}}\max(\|x_k\|,\|x_{k+1}\|).
$$

But small steps can indicate stagnation, not a solved problem. Also evaluate a problem residual, feasibility, monotonicity or descent expectations, iteration/resource limits, and exceptional values. Convert residual to forward error only with an applicable conditioning or convergence theorem.

### Use mixed precision with error gates

Low precision can improve throughput and data movement. A sound design may factor or estimate in low precision, compute residuals in higher precision, and refine while a condition-dependent convergence test holds. Fall back when scaling, residual, growth, condition estimate, or iteration behavior violates the supported regime.

Record precision at every operation and communication boundary. Accelerator defaults, fused operations, tensor formats, library kernels, and compiler flags change behavior. Benchmark the guarded end-to-end policy, including conversions, checks, and fallbacks, rather than only its favorable fast path.

### Verify claims independently

Use exact integer/rational cases, arbitrary-precision references, interval enclosures, known identities with conditioned domains, residuals, and independently derived bounds. Generate values near zero, overflow, underflow, representational binades, branch surfaces, repeated roots, singularity, and cancellation. Vary ordering, scale, translation, units, precision, compiler, vector width, threads, and devices as the claim requires.

The oracle must be stronger or independent. Computing expected output with the same formula and precision duplicates the defect. High precision still needs enough guard digits and a convergence check. Differential disagreement is a trigger for analysis, not automatic proof that the majority is correct.

### Review performance and semantics together

Fused multiply-add can improve one rounding path and alter bits relative to separate operations. Reassociation and fast-math transformations may improve vectorization while invalidating NaN, signed-zero, exception, or reproducibility assumptions. Treat flags and hardware capabilities as part of the algorithm version.

Set an error budget and spend it across input quantization, arithmetic, approximation, iteration, communication, and output conversion. Measure accuracy distributions and worst supported cases beside latency, memory, bandwidth, and energy. Reject a faster path that violates the numeric contract; restrict it to a guarded regime if evidence supports that boundary.

## Definitions and Notation

Let exact data be $x$, represented data $\tilde x$, exact solution $y=f(x)$, and computed result $\hat y$. Absolute forward error is $\|\hat y-y\|$; relative forward error divides by $\|y\|$ when meaningful. A residual measures violation of the defining equation, such as $r=b-A\hat x$. Backward error is the smallest permitted perturbation making $\hat y$ exact.

Let $u$ be unit roundoff under a named format and rounding mode. Machine epsilon is used inconsistently across ecosystems, so define it rather than relying on the phrase. ULP means a spacing unit at a specified representable value; a fixed ULP count does not imply a fixed relative error at exceptional boundaries.

## Mechanisms, Invariants, or Proof Structure

### Conditioning derivation

For differentiable scalar $f$, $f(x+\Delta x)-f(x)\approx f'(x)\Delta x$. Dividing output error by $|f(x)|$ and multiplying/dividing by $|x|$ yields relative amplification $|xf'(x)/f(x)|\,|\Delta x/x|$, provided the denominators are meaningful. This is local first-order analysis, not a global bound.

### Stable norm derivation

For $m=\max(|x|,|y|)>0$,

$$
\sqrt{x^2+y^2}=m\sqrt{(x/m)^2+(y/m)^2}.
$$

The scaled ratios have magnitude at most one, preventing overflow in their squares. The argument separately handles $m=0$ and must still account for exceptional values and underflow of extremely small ratios.

### Predicate-filter invariant

If an approximate predicate value $\hat p$ has a proved absolute error bound $E$, then $|\hat p|>E$ implies the exact value has the same sign. When $|\hat p|\le E$, the filter returns indeterminate and escalates; guessing breaks the invariant.

### Error-budget invariant

Every accepted fast path has a proved or empirically bounded error contribution compatible with the total obligation; every unsupported condition triggers a certified slower path or explicit failure. The evidence identifies which part is theorem, bound, measurement, or assumption.

## Alternatives and Trade-Offs

| Technique | Strength | Cost or limitation | Appropriate use |
|---|---|---|---|
| algebraic reformulation | often cheap and accurate | domain-specific edge cases | cancellation or overflow patterns |
| pairwise summation | parallel depth and better typical error | order/topology dependence | large reductions |
| compensated summation | recovers many lost low terms | extra operations and state | accuracy-sensitive sums |
| higher precision | wider range and smaller roundoff | throughput, memory, portability | narrow difficult regions |
| interval arithmetic | enclosure under directed semantics | width growth and ecosystem cost | certified bounds |
| adaptive exact predicate | discrete correctness | implementation complexity | computational geometry/topology |
| mixed precision plus refinement | fast common path | convergence guards and fallback | well-conditioned linear algebra |
| exact rational/integer arithmetic | exact supported semantics | size growth and variable latency | certificates and small exact cores |

No technique is universally stable. Reformulation can introduce a new singularity; higher precision postpones rather than removes conditioning; intervals can widen uselessly; compensation does not prevent overflow; exact predicates do not make constructed coordinates exact; and reproducible reductions may cost more than tolerance-based ones.

## Failure Modes and Misconceptions

- **“Floating point is random.”** Operations are governed by formats and environment, while order and transformations explain many differences.
- **“More precision proves correctness.”** It reduces some errors but does not repair wrong models, unstable formulas, or discrete overflow.
- **“Small residual means accurate answer.”** Forward error also depends on conditioning and the residual-to-error theorem.
- **“Relative error always works.”** It is undefined or misleading near zero; use a scale-aware absolute obligation.
- **“One epsilon compares all values.”** Units, magnitude, operation history, and consequence determine tolerance.
- **“Compensation makes sums exact.”** It improves a method under assumptions but has range and conditioning limits.
- **“Fast math only changes speed.”** It may change exceptional, ordering, contraction, and reproducibility semantics.
- **“Exact predicates solve geometry.”** They decide predicates for represented inputs; constructions and model semantics remain.
- **“NaN behaves like a large number.”** It is unordered and requires explicit policy.
- **“Passing random tests demonstrates stability.”** Adversarial numeric surfaces and independent bounds are indispensable.

## Worked Examples

### Example 1

**Situation.** A team reports 12 correct digits for a result near zero using relative error.

**Reasoning.** Relative error divides by the exact result and becomes unstable or undefined near zero. State an absolute tolerance tied to units, or a mixed absolute-relative contract. Also report input representation and conditioning.

**Conclusion.** Accuracy metrics must match scale and consequence.

### Example 2

**Situation.** Evaluate $1-\cos(10^{-8})$ directly and by $2\sin^2(5\times10^{-9})$.

**Reasoning.** Direct cosine may round to a value indistinguishable from one before subtraction, yielding zero and total relative loss. The reformulation avoids subtracting close approximations and returns a value near $5\times10^{-17}$, subject to the sine implementation.

**Conclusion.** Algebraically equal real formulas can have radically different finite behavior.

### Example 3

**Situation.** Compute $\sqrt{x^2+y^2}$ for $x=y=10^{308}$ in binary64.

**Reasoning.** Squaring overflows even though the norm is about $1.414\times10^{308}$, within the finite range. Scale by $m=10^{308}$, compute $m\sqrt{1+1}$, and use an environment-tested hypot implementation for exceptional cases.

**Conclusion.** Safe scaling prevents avoidable intermediate overflow.

### Example 4

**Situation.** The quadratic $x^2+10^8x+1=0$ is evaluated with one textbook formula for both roots.

**Reasoning.** The small root subtracts nearly equal large numbers. Compute a cancellation-safe $q$, one root as $q/a$, and the other from the product relation $c/q$. Check residuals with scaling and compare against higher precision.

**Conclusion.** Stable formulas use problem identities to avoid destructive branches.

### Example 5

**Situation.** A million positive small values are reduced on varying thread counts and differ in last bits.

**Reasoning.** Tree shape changes parenthesization. If tolerance is the obligation, bound and test error across supported trees. If bitwise reproducibility is required, fix a portable reduction structure or use a reproducible accumulator and include its cost.

**Conclusion.** Numerical equivalence and bitwise reproducibility are different contracts.

### Example 6

**Situation.** A geometry orientation estimate is $3\times10^{-18}$ with proved error bound $5\times10^{-18}$.

**Reasoning.** The sign is not certified because magnitude does not exceed the bound. Escalate to higher/adaptive exact precision. Replacing the result by zero or choosing its sign can corrupt mesh topology.

**Conclusion.** A robust filter exposes indeterminacy instead of guessing.

### Example 7

**Situation.** An iterative solve has residual norm $10^{-12}$, but the matrix condition estimate is $10^{14}$.

**Reasoning.** A small backward-style residual can be amplified severely in forward error, depending on scaling and theorem hypotheses. Inspect componentwise/normwise measures, refine or reformulate, and avoid claiming accurate solution digits from residual alone.

**Conclusion.** Stability and conditioning jointly determine forward trust.

### Example 8

**Situation.** A priority queue comparator receives NaN path estimates and uses ordinary less-than comparisons.

**Reasoning.** NaN compares false in both directions, violating a presumed total order and potentially heap invariants. Reject NaN at the boundary, define an explicit total-order policy where semantics allow, or propagate failure. Do not silently treat it as infinity.

**Conclusion.** Exceptional values are control-flow inputs requiring contract-level handling.

### Example 9

**Situation.** A mixed-precision solver is fast on most matrices but stagnates on badly scaled cases.

**Reasoning.** Compute residual and condition/growth indicators in higher precision, set a bounded refinement budget, and fall back when convergence premises fail. Benchmark conversions, checks, fallback frequency, and tail latency on held-out scales.

**Conclusion.** Mixed precision is a guarded portfolio, not one unconditional algorithm.

### Example 10

**Situation.** Enabling aggressive reassociation speeds a dot product by 30% and changes acceptance near a regulatory threshold.

**Reasoning.** The optimization changed semantic evidence, not just speed. Freeze flags as part of the version, analyze rounding and threshold uncertainty, use a certified comparison or wider-precision boundary path, and revalidate across targets.

**Conclusion.** Performance transformations must remain inside the declared numeric contract.

## Cross-Program Connections

- [Concurrent and Parallel Programming CONPAR-092](../../04-programming-languages-concurrent-and-parallel-programming/modules/092-roofline-and-operational-intensity-analysis.md) connects reduction structure with hardware cost.
- [Systems Programming SYSP-003](../../05-programming-languages-systems-programming/modules/003-floating-point-representation-and-exceptional-values.md) owns representation and language-level exceptional behavior.
- [Computer Architecture CA-006](../../23-computer-architecture/modules/006-floating-point-hardware.md) connects formats and operations to hardware implementation.
- [Data Structures Engineering DSE-001](../../17-data-structures-engineering/modules/001-abstract-data-types-and-concrete-representations.md) separates abstract numeric obligations from concrete representation.
- [Testing and Quality Engineering STQE-002](../../13-software-engineering-testing-and-quality-engineering/modules/002-specifications-expectations-and-test-oracles.md) supplies independent, partial, and metamorphic oracle design.
- [Systems Engineering SYSENG-043](../../26-systems-engineering/modules/043-cost-schedule-performance-and-risk.md) frames numeric error as a system risk with verification cost.

## References

1. IEEE Computer Society, *IEEE Std 754-2019: IEEE Standard for Floating-Point Arithmetic*, 2019. [Official standard record](https://standards.ieee.org/ieee/754/6210/). Active revision, formats, operations, exceptions, and reproducibility conditions checked 2026-09-05.
2. Nicholas J. Higham, *Accuracy and Stability of Numerical Algorithms*, 2nd ed., SIAM, 2002. [doi:10.1137/1.9780898718027](https://doi.org/10.1137/1.9780898718027). Authoritative monograph for rounding models, conditioning, stability, summation, and linear algebra; publisher record checked 2026-09-05.
3. David Goldberg, “What Every Computer Scientist Should Know About Floating-Point Arithmetic,” *ACM Computing Surveys* 23(1), 1991, 5–48. [doi:10.1145/103162.103163](https://doi.org/10.1145/103162.103163). Foundational systems tutorial; ACM record checked 2026-09-05.
4. Michael L. Overton, *Numerical Computing with IEEE Floating Point Arithmetic*, SIAM, 2001. [doi:10.1137/1.9780898718072](https://doi.org/10.1137/1.9780898718072). Reference for IEEE arithmetic and numerical examples; publisher record checked 2026-09-05.
5. Jonathan Richard Shewchuk, “Adaptive Precision Floating-Point Arithmetic and Fast Robust Geometric Predicates,” *Discrete & Computational Geometry* 18(3), 1997, 305–363. [doi:10.1007/PL00009321](https://doi.org/10.1007/PL00009321). Primary adaptive exact-predicate work; publisher and author records checked 2026-09-05.
6. James H. Wilkinson, *Rounding Errors in Algebraic Processes*, Prentice-Hall, 1963. Classic source for backward error and finite-precision algebra; bibliographic record checked 2026-09-05.
7. Siegfried M. Rump, Takeshi Ogita, and Shin'ichi Oishi, “Accurate Floating-Point Summation Part I: Faithful Rounding,” *SIAM Journal on Scientific Computing* 31(1), 2008, 189–224. [doi:10.1137/050645671](https://doi.org/10.1137/050645671). Primary accurate-summation algorithms and bounds; publisher record checked 2026-09-05.
8. Erin Carson and Nicholas J. Higham, “Accelerating the Solution of Linear Systems by Iterative Refinement in Three Precisions,” *SIAM Journal on Scientific Computing* 40(2), 2018, A817–A847. [doi:10.1137/17M1140819](https://doi.org/10.1137/17M1140819). Primary mixed-precision refinement analysis; publisher record checked 2026-09-05.
9. Python Software Foundation, “math — Mathematical Functions,” *Python 3.14 Documentation*, section on `math.fsum`. [Official documentation](https://docs.python.org/3.14/library/math.html#math.fsum). Current behavior and stated IEEE-rounding limitations checked 2026-09-05.

## Exercises

### Exercise 1

Define unit roundoff, conditioning, forward error, residual, backward error, stability, cancellation, and robust predicate for an engineer reviewing a numeric library.

### Exercise 2

For $f(x)=1/x$, derive the local relative condition number. For $x=2$ perturbed to $2.002$, compute the exact relative input and output changes and compare the first-order prediction.

### Exercise 3

Diagnose a norm implementation that computes square, sum, square root in binary64, treats NaN as a missing value, and tests correctness only on values between 0.1 and 10.

### Exercise 4

Compare naive, pairwise, compensated, binary128, and exact/reproducible accumulation for a parallel financial-risk aggregation containing mixed signs and a hard audit requirement.

### Exercise 5

Design a numerically governed shortest-path implementation with large integer and floating weights, parallel relaxations, equality-sensitive predecessor choice, infinity sentinels, negative-edge rejection, and cross-device deployment. Include contracts, bounds, overflow, predicates, reproducibility, tests, evidence, and fallback.

## Answers to the Exercises

### Answer 1

Unit roundoff bounds one correctly rounded basic operation's relative error under a named normal-range model. Conditioning is sensitivity of the mathematical problem to input perturbation. Forward error compares computed and exact outputs; a residual measures violation of the defining equation. Backward error is the smallest allowed input perturbation that makes the computed output exact. Stability bounds error introduced by the procedure, often through backward error. Cancellation exposes uncertainty when close approximations are subtracted. A robust predicate returns a certified discrete decision or escalates when finite precision cannot certify it. Every term needs format, norm/scale, domain, and exceptional assumptions.

### Answer 2

For $f(x)=x^{-1}$, $f'(x)=-x^{-2}$, so $\kappa_f(x)=|x(-x^{-2})/(x^{-1})|=1$ for nonzero $x$. Relative input change is $(2.002-2)/2=0.001$. Outputs are 0.5 and approximately 0.4995004995; relative output change is about $-0.000999001$, whose magnitude is close to the first-order prediction $1\times0.001$. The difference is a second-order finite-perturbation effect; this calculation does not include representation rounding.

### Answer 3

Squaring can overflow or underflow before the representable norm does; scale by the maximum magnitude or use a specified hypot routine. The summation order and accumulator need an error argument. Silently dropping NaN changes dimension and meaning; reject, propagate, or handle it through an explicit domain policy. Ordinary moderate tests miss zero, signed zero, subnormal, maximum finite, infinity, NaN, mixed scales, cancellation, and transition surfaces. Compare with high-precision or scaled references, test permutation/scale properties where valid, record environment and flags, and verify error bounds across the supported domain.

### Answer 4

Naive summation is cheapest and least defensible for severe cancellation. Pairwise reduction offers parallel depth and typically better error growth but changes bits with the tree. Compensation improves many losses with extra state and operations, yet does not ensure exactness or prevent overflow. Binary128 widens precision/range but may be slow or unavailable and still depends on order. Exact or reproducible accumulators can provide a portable rounded result or audit-stable bits at the highest implementation and resource cost. For a hard audit obligation, use an exact/reproducible method or a fixed certified scheme, checked overflow/range, versioned inputs and tree, independent recomputation, and reconciliation. Benchmark it against compensated/pairwise candidates only after the audit semantics are held fixed.

### Answer 5

Define graph identity, path semantics, accepted weight types/ranges, rounding and tie policy, unreachable representation, negative-edge behavior, maximum path length, output certificate, and device reproducibility requirement. For integers, derive path bounds and use checked wider addition or explicit overflow failure. For floats, reject NaN and unsupported negatives, distinguish infinity sentinel from overflow, compute guarded additions, and compare candidate distances with a scale/error bound; equality-sensitive predecessor choice needs a deterministic total policy that cannot replace a genuinely smaller path. Parallel relaxations use atomic/versioned updates and a fixed tie rule; do not assume associative reduction. Prove algorithm hypotheses for the weight domain, bound local arithmetic where possible, and independently verify predecessor paths and recomputed distances in stronger precision. Test extreme scale, near ties, zero, signed zero, subnormals, maximum finite, disconnected graphs, long paths, adversarial order, thread counts, compilers, flags, and devices. Use a conservative checked high-precision or integer fallback when a comparison is indeterminate or range unsupported, and reject the fast path if cross-device evidence cannot meet the declared reproducibility and correctness contract.
