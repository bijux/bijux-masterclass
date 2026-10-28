---
module_id: SYSP-003
program: Programming Languages: Systems Programming
level: 1
module_number: 3
title: Floating-Point Representation and Exceptional Values
status: complete
last_verified: 2026-08-29
---

# Floating-Point Representation and Exceptional Values

## One-Page Review

### Governing question

How do finite floating-point formats approximate real arithmetic, and how must systems code handle rounding, subnormals, signed zeros, infinities, NaNs, and exception state without inventing guarantees its language does not provide?

### Essential definitions

- A **floating-point format** represents a finite set of values using a sign, significand, exponent, radix, and encodings for exceptional categories.
- A **normal** finite binary value has full format precision and an implicit leading significand bit in common IEEE interchange formats.
- A **subnormal** value uses the minimum exponent with a reduced leading significand, filling the gap between the smallest normal magnitude and zero.
- **Rounding** maps an exact mathematical result to a representable value under a named rounding direction.
- One **unit in the last place** (ulp) is the spacing associated with a representable value at its magnitude; spacing grows with exponent.
- **Positive and negative zero** compare numerically equal in ordinary IEEE comparisons but retain a sign that can affect later operations.
- **Infinity** represents an exceptional unbounded result or input category; it is not the largest finite value.
- **NaN** represents a non-number result or datum. Quiet and signaling NaNs and payloads are format concepts whose preservation is language- and platform-dependent.
- IEEE 754 names five exception conditions: invalid operation, division by zero, overflow, underflow, and inexact.

### Central model, mechanism, or theorem

For a binary format with precision $p$, a positive normal value has the abstract form

$$
x=(1.f)_2 2^e,
$$

while a positive subnormal has

$$
x=(0.f)_2 2^{e_{min}}.
$$

An arithmetic operation is modeled as exact real computation followed by format rounding:

$$
fl(x\circ y)=round_F(x\circ y).
$$

For round-to-nearest and a normal result, a common local model is $fl(z)=z(1+\delta)$ with $|\delta|\le u$, where unit roundoff $u=2^{-p}$ for binary precision $p$. The model needs qualification near zero, overflow, and exceptional values.

### Critical invariants

- Representation range and precision are separate; a value can be in range yet not exactly representable.
- Every claim names format, operation, rounding mode, intermediate precision, contraction policy, and language/toolchain when relevant.
- Normal spacing scales with magnitude; one global absolute epsilon is not a universal equality test.
- Subnormal support provides gradual underflow but reduced relative precision.
- NaN is unordered under ordinary numeric comparisons; detect and order it with specified classification/total-order operations.
- Signed zeros compare equal numerically but must not be collapsed when sign-sensitive behavior matters.
- Exception flags, language exceptions, signals, and traps are different mechanisms.
- Optimizations may reassociate or contract only when permitted by the active language and build contract.

### Common failures

Typical defects are assuming decimal literals are exact binary values, comparing with one arbitrary epsilon, treating `NaN != NaN` as a complete validation policy, using infinity as a missing-value sentinel, losing signed zero in serialization, flushing subnormals without recording the mode, summing ill-conditioned data naively, enabling fast-math while relying on NaN/zero semantics, and expecting bitwise reproducibility across unspecified toolchains.

### Compact example

Binary64 cannot represent $0.1$ or $0.2$ exactly, so their rounded sum in Python is displayed as `0.30000000000000004` and does not equal the binary64 approximation selected for literal `0.3`. Binary64 also has only 53 bits of significand precision: converting integers $2^{53}$ and $2^{53}+1$ to binary64 produces the same value. These are defined consequences of a finite value set, not random hardware errors.

### Connections

[SYSP-002](002-integer-representation-overflow-and-conversion.md) separates values, bit patterns, and language arithmetic policy. Later modules cover binary representation and generated assembly. Numerical algorithm selection connects to [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md), and execution details connect to [Computer Architecture](../../23-computer-architecture/ROADMAP.md).

## Governing Question

What can a floating-point datum and operation actually promise, from source literal through machine execution and serialization?

Real numbers are infinite and often require infinite expansions. A machine format has finitely many bit patterns. Floating-point succeeds by distributing those patterns across many orders of magnitude: values near zero are close together; large values are farther apart. Arithmetic usually computes or approximates an exact result and rounds it back into that nonuniform set.

This model provides extraordinary range and useful relative precision, but it is not real arithmetic with occasional noise. Addition can lose small addends. Reassociation can change answers. Subtraction can expose prior approximation. Overflow can produce infinity; invalid operations can produce NaN; gradual underflow enters a region with reduced relative precision. Systems code must know which of these behaviors its language exposes, which the compiler may alter, and which a binary interface or persisted format promises.

## Why This Matters

Floating point appears in graphics, simulation, control, scientific computing, machine learning, telemetry, geospatial systems, media, statistics, databases, and protocol fields. Representation mistakes cross boundaries. A service serializes NaN although its schema forbids it. A sort comparator violates ordering requirements because NaN is unordered. A checksum changes when a platform canonicalizes NaN payloads. An optimization assumes no infinities while the error path uses one as a sentinel. A threshold changes around a rounding boundary after a fused operation replaces two rounded operations.

Correctness is not achieved by banning floating point. Binary floating point is often the right representation and IEEE 754 provides disciplined, interoperable behavior. The task is to select a format and algorithm from error and range requirements, classify exceptional values at trust boundaries, state reproducibility needs, and verify the actual compiler/runtime mode. Decimal arithmetic, scaled integers, intervals, exact rationals, arbitrary precision, and fixed point solve different problems and introduce their own contracts.

## Prerequisites and Retrieval

You should know binary positional notation, powers, scientific notation, integers, functions, comparisons, and the value/representation distinction from SYSP-002. Retrieve these points:

1. A bit pattern has meaning only under a specified type and format.
2. A mathematical operation and the source-language operation bearing the same symbol can have different domains and outcomes.
3. A finite test demonstrates selected cases, not a universal numerical bound.
4. Serialization fixes an interchange contract, not necessarily the host's evaluation format.
5. Compiler flags and target features can be semantic inputs to reproducibility.
6. Validation must classify exceptional values before downstream code assumes finiteness or ordering.

Basic algebra is sufficient. The chapter derives the representation model; advanced error analysis and numerical linear algebra are outside its scope.

## Learning Objectives

After completing this module, you should be able to:

- decode the category and value of simplified IEEE-style binary encodings;
- distinguish sign, exponent, precision, significand, normal, subnormal, zero, infinity, and NaN;
- explain why decimal-to-binary conversion and arithmetic require rounding;
- calculate spacing and identify integer-collision thresholds for binary formats;
- distinguish absolute, relative, and ulp-based error statements;
- trace propagation and comparison behavior for signed zero, infinity, and NaN;
- distinguish IEEE exception conditions and status flags from language exceptions and traps;
- identify non-associativity, absorption, cancellation, double rounding, and contraction boundaries;
- design robust validation, comparison, serialization, and accumulation policies;
- define evidence required for reproducible and high-stakes floating-point claims.

## Core Exposition

A general floating-point number has sign $s$, radix $\beta$, significand digits, and exponent $e$:

$$
(-1)^s\times significand\times\beta^e.
$$

IEEE 754 specifies binary and decimal formats, operations, conversions, comparisons, exceptions, and default handling. The familiar binary32 and binary64 interchange formats use radix two. Binary32 has precision 24 and binary64 precision 53, counting the implicit leading bit of normal values. Their stored fields are not simply “a sign bit, an integer, and a decimal exponent”; decoding depends on exponent categories.

For binary interchange formats, an exponent field strictly between its all-zero and all-one encodings denotes a **normal** finite value. The leading significand bit is implicit and equals one. An all-zero exponent denotes signed zero when the fraction is zero and a **subnormal** when the fraction is nonzero. An all-one exponent denotes signed infinity when the trailing significand is zero and NaN otherwise. The exact quiet/signaling and payload conventions require the standard and language contract; do not infer portable application metadata from spare-looking NaN bits.

Normalization gives each nonzero normal value a unique leading one and full precision. Subnormals remove that leading-one assumption at the minimum exponent. They make underflow gradual: results can decrease through a linearly spaced interval toward zero rather than jumping directly from the smallest normal to zero. Relative precision worsens as the significand loses leading bits, but absolute spacing remains small and important identities can degrade more gracefully.

Floating-point spacing is nonuniform. For a binary format of precision $p$, adjacent normal values in a binade $[2^e,2^{e+1})$ are spaced $2^{e-p+1}$ apart. Binary64 values in $[1,2)$ are spaced $2^{-52}$; values near $2^{53}$ are spaced by 2. Therefore $2^{53}+1$ is not representable as binary64 even though it is far below the format's maximum magnitude. Range says a finite approximation exists; precision says which values are distinct.

Most finite decimal fractions do not have finite binary expansions. A reduced rational $a/b$ has a finite radix-two expansion only when $b$ has no prime factor other than two. Thus $1/10$, whose denominator contains five, repeats in binary. Parsing literal `0.1` selects a nearby representable value according to language conversion rules. Printing commonly chooses a short decimal that round-trips to the same binary value, not the complete exact decimal expansion of that stored fraction.

Arithmetic introduces another rounding. The useful model is `exact then round`: take the mathematical result of representable operands and choose a representable destination value under the active rounding direction. IEEE 754 includes round-to-nearest ties-to-even, round-to-nearest ties-away, toward positive infinity, toward negative infinity, and toward zero for specified operations and formats, with required support depending on the standard's clauses. A source language may expose only part of this control or fix its own evaluation rule.

Round-to-nearest ties-to-even limits bias over many midpoint cases and gives a normal result within one-half ulp of the exact value. Unit roundoff $u$ expresses a relative bound for one correctly rounded normal operation under assumptions. It is not a promise that a long computation has relative error $u$; errors propagate according to algorithm, conditioning, dependence, overflow, underflow, cancellation, and exceptional behavior.

The name **machine epsilon** is used inconsistently. In many libraries it means the distance from 1 to the next representable value, $2^{1-p}$ for binary precision $p$, while numerical analysis often uses unit roundoff $2^{-p}$. State which quantity is meant. Neither is a universal tolerance. Comparing coordinates near $10^{12}$, probabilities near zero, and account balances in fixed minor units demands different domain policies.

Floating-point addition is not generally associative. Let a format approximate a very large $a$ and small $b$. If $b$ is below half the spacing at $a$, `fl(a+b)=a`; subtracting $a$ later yields zero. Grouping `a + (b-a)` can yield something else after separate roundings. Compilers may reassociate only under applicable language and optimization permissions. A proof over real addition does not silently authorize the transformation.

**Absorption** occurs when a small addend does not change a much larger value. **Cancellation** occurs when subtracting nearby approximations removes leading shared digits, exposing error in the residual. The subtraction may itself be correctly rounded; the loss came from limited information in the inputs. Stable algorithms restructure computations, scale inputs, compensate sums, or use greater precision based on analysis. Simply replacing equality with a tolerance does not repair an unstable algorithm.

A fused multiply-add computes $x\times y+z$ with one final rounding rather than rounding the product and then the sum. It often improves accuracy and performance, but can differ bitwise from the two-operation sequence. Contraction is therefore a semantic choice when reproducibility requires a particular result. Extended intermediates and double rounding can likewise make a stored result differ across targets or compiler modes unless the language and build fix them.

IEEE-style exceptional categories extend computation. A finite nonzero value divided by signed zero can produce signed infinity under languages that expose IEEE division semantics. Zero divided by zero and infinity minus infinity are invalid operations producing NaN under default non-trapping handling. Overflow commonly yields infinity or a maximum finite value depending on sign and rounding direction. Underflow concerns tiny results and can yield subnormal values or signed zero. Inexact records that rounding changed the exact result; it is extremely common and not itself an application error.

The five IEEE exception **conditions** can raise sticky status flags in an environment. A flag remains set until explicitly cleared under the relevant API, permitting code to inspect whether an earlier operation encountered a condition. Alternate handling can trap where supported and enabled. This is different from a C++ exception object, Java exception, Rust `Result`, Python exception, POSIX signal, or hardware fault. Many language expressions use default non-trapping behavior and do not expose flags portably.

NaN means ordinary numeric ordering is partial. Comparisons with NaN, including equality with itself, normally return false except inequality behavior defined by the language. The idiom `x != x` can detect many NaNs under strict semantics but is poor boundary documentation and can conflict with optimizer assumptions under aggressive modes. Use classification functions. Sorting requires a total-order policy: reject NaNs, place them explicitly, or use a specified total order that distinguishes categories and possibly encodings.

NaN is not a safe general-purpose missing value. Payloads can be quieted, canonicalized, or changed by operations, runtimes, serialization formats, databases, processors, or optimization. A schema may reject non-finite JSON numbers. If absence matters, represent it as an option/null variant with explicit validation and provenance. If NaN payload transport matters, define exact bit-preservation tests at every boundary and treat it as a specialized binary protocol.

Positive and negative zero compare equal in ordinary numeric equality, but they are distinguishable by sign-aware operations and representations. Reciprocals under IEEE semantics have opposite infinities; functions such as complex operations can use the sign to preserve approach direction across branch cuts. Hashing and serialization must decide whether equality-normalized zeros share one representation or bitwise identity is retained. Both choices can be correct if consistent.

Infinity is useful for extended arithmetic and bounds, but it is not an ordinary large measurement. An overflowed sensor result, explicit unbounded interval, and missing reading have different meanings. Boundary validation should distinguish finite, infinite, NaN, normal, subnormal, and zero when the domain cares. A check like `x <= maximum` rejects NaN because comparison is false, but it does not communicate why, and inverted logic can accidentally admit it.

Language rules vary. Java SE 25 defines `float` and `double` around IEEE binary32 and binary64 values and gives specified results for non-finite operations. Rust documents `f32`/`f64` categories, NaN caveats, bit conversions, and `total_cmp`, while exact results can still depend on operation guarantees and target behavior documented by the language. C and C++ provide implementation-property and floating-environment facilities with conditional IEC 60559 conformance; build flags and `FENV_ACCESS`-style contracts matter. Python commonly maps `float` to C double and documents binary representation behavior, while Python division by zero raises `ZeroDivisionError` rather than merely returning infinity. Never transfer one language's surface outcome by assuming common hardware.

Serialization requires a separate contract. Decimal text should specify accepted grammar, non-finite policy, precision, rounding, and round-trip property. For binary interchange, specify IEEE format, byte order, NaN policy, and whether signaling state or payload is preserved. Native-memory dumping is not a portable format. Canonical hashes may normalize NaNs and zeros, but then cannot claim bitwise round trip.

Approximate comparison begins with the domain. Absolute tolerance fits values near a meaningful zero scale. Relative tolerance scales with magnitude but needs a near-zero rule. Ulp distance measures representation adjacency but does not encode application significance and needs careful handling across signs, NaNs, and zeros. For geometry, finance, measurement, or convergence, derive tolerance from units, propagated uncertainty, algorithmic error, and decision consequences.

Accumulation deserves deliberate design. Summing small terms into a large running total can repeatedly absorb them. Pairwise summation reduces error growth for many inputs; compensated algorithms track some lost low-order information; wider accumulators can help; exact or reproducible accumulators serve stronger requirements. The correct choice follows an error and performance budget, not a blanket rule that binary64 is enough.

The executable example uses Python's documented binary64-like `float` behavior on the verification platform. It avoids division by zero because Python's source-language result is an exception, not an IEEE infinity value.

<!-- bijux-verify: {"id":"binary64-boundaries","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"sum=0.30000000000000004\nequals_0.3=False\ninteger_collision=True\nsigned_zeros_equal=True reprs=0.0,-0.0\nnan_equal_self=False\nsmallest_subnormal=0x0.0000000000001p-1022\n","stderr":""}} -->
```python
decimal_sum = 0.1 + 0.2
large = 2 ** 53
positive_zero = 0.0
negative_zero = -0.0
not_a_number = float("nan")
smallest_subnormal = float.fromhex("0x0.0000000000001p-1022")

print("sum=" + repr(decimal_sum))
print("equals_0.3=" + str(decimal_sum == 0.3))
print("integer_collision=" + str(float(large) == float(large + 1)))
print("signed_zeros_equal=" + str(positive_zero == negative_zero) + " reprs=" + repr(positive_zero) + "," + repr(negative_zero))
print("nan_equal_self=" + str(not_a_number == not_a_number))
print("smallest_subnormal=" + smallest_subnormal.hex())
```

This output verifies representation boundaries for the recorded Python toolchain. It does not prove arbitrary platform conformance, compiler modes, exception flags, NaN payload preservation, correct financial or scientific modeling, numerical stability, or bitwise reproducibility beyond this execution.

## Definitions and Notation

Let a binary format have precision $p$, minimum normal exponent $e_{min}$, maximum exponent $e_{max}$, sign $s\in\{0,1\}$, and fraction integer $F$.

For a normal value with $0\le F<2^{p-1}$,

$$
value=(-1)^s\left(1+\frac{F}{2^{p-1}}\right)2^e,
\qquad e_{min}\le e\le e_{max}.
$$

For a subnormal,

$$
value=(-1)^s\left(\frac{F}{2^{p-1}}\right)2^{e_{min}},
\qquad 0<F<2^{p-1}.
$$

When $F=0$ in the subnormal exponent category, the value is signed zero. Infinity and NaN use reserved exponent encodings and are not described by the finite equations.

Let $Fset$ be the format's representable values and $RN:F_{extended}\to Fset$ round to nearest, ties to even. For finite exact $z$ with a normal rounded result,

$$
RN(z)=z(1+\delta),\qquad |\delta|\le u=2^{-p}.
$$

Define absolute error $|\hat x-x|$, relative error $|\hat x-x|/|x|$ for $x\ne0$, and ulp error by scaling absolute error to local representable spacing. These measures answer different questions.

For binary64, $p=53$, $e_{min}=-1022$, and the smallest positive subnormal is $2^{-1074}$. The spacing in $[2^e,2^{e+1})$ is

$$
ulp=2^{e-(p-1)}.
$$

Thus spacing in $[2^{53},2^{54})$ is 2, explaining why adjacent mathematical integers are not all representable there.

Let classification

$$
class_F(x)\in\{zero,subnormal,normal,infinity,nan\}
$$

be accompanied by sign where the format makes it meaningful. Ordinary numeric comparison $<_n$ is partial because NaN is unordered. A format's `totalOrder`-style predicate is a separate relation designed to order all canonical members or encodings according to its specification.

## Mechanisms, Invariants, or Proof Structure

**Finite binary criterion.** For rational $a/b$ in lowest terms, a finite binary expansion exists iff $b=2^k$ for some $k\ge0$. If $b$ contains another prime factor, no multiplication by a power of two makes $a2^n/b$ an integer, so the binary expansion cannot terminate. This proves why $1/10$ needs rounding.

**Normal spacing.** Fix exponent $e$. Incrementing fraction integer $F$ by one changes the value by $2^e/2^{p-1}=2^{e-p+1}$. Spacing doubles at the next binade. Consequently, a fixed absolute epsilon represents different ulp counts at different magnitudes.

**Integer exactness threshold.** Binary precision $p$ represents every integer through $2^p$, but above that point spacing exceeds one. For binary64, $2^{53}$ is representable and the next representable value is $2^{53}+2$; rounding $2^{53}+1$ under ties-to-even collides with $2^{53}$.

**Subnormal continuity.** The largest subnormal and smallest normal differ by one subnormal spacing. This gradual transition avoids a format gap immediately below the smallest normal. Relative error grows toward zero because the absolute spacing remains constant while magnitudes shrink.

**Non-associativity witness.** In binary64 let $a=2^{53}$, $b=1$, and $c=-2^{53}$. Rounding gives `fl(fl(a+b)+c)=0` because $a+b$ ties to $a$, while `fl(a+fl(b+c))=1` for the relevant exact representable intermediate. One witness refutes universal associativity; it does not quantify every sum's error.

**NaN validation invariant.** A domain requiring finite values must explicitly establish `is_finite(x)` before arithmetic or ordering. Range comparisons alone are insufficient as a communicative proof because NaN makes each ordered comparison false and infinity can satisfy one-sided bounds.

**Reproducibility tuple.** A bitwise-result claim is incomplete without source and input bits, language/runtime version, target and instruction set, compiler and flags, format and rounding, contraction/reassociation policy, subnormal mode, math-library version, thread reduction order, and serialization rule. Omitting a varying component weakens the claim to a narrower environment.

**Error-bound boundary.** The one-operation relative model assumes finite inputs and a normal rounded result under the named rounding rule. It must not be applied unchanged to subnormal results, overflow, NaNs, infinities, exact zero, or an algorithm whose inputs already contain unbounded error.

## Alternatives and Trade-Offs

**Binary floating point versus decimal floating point.** Binary formats match binary hardware and many scientific workloads efficiently. Decimal formats represent decimal fractions such as 0.1 exactly within their precision, useful for decimal rules. Both still have finite precision, rounding, overflow, and exceptional cases.

**Floating point versus scaled integer.** Scaled integers make a fixed quantum and range explicit and can fit money or device units. Multiplication, division, rescaling, overflow, and mixed-scale operations still require policy. Floating point provides wide dynamic range and relative precision where a fixed scale is unsuitable.

**Standard precision versus wider precision.** Wider formats reduce rounding and extend range but cost memory, bandwidth, vector throughput, and interoperability. They do not repair an unstable algorithm automatically. Use error analysis and measurements.

**Gradual underflow versus flush-to-zero.** Subnormals preserve tiny values and smoother error properties. Flush-to-zero modes can simplify or accelerate particular hardware paths but change semantics and can turn small nonzero results into zero. Record and test the mode.

**Strict semantics versus aggressive optimization.** Strict rules preserve NaN, signed-zero, exception, and evaluation-order assumptions. Fast-math families permit transformations that can improve performance but invalidate those assumptions. Enable them only under proven input and observation contracts, isolated scope, and differential evidence.

**Tolerance comparison versus exact comparison.** Exact comparison is right for bit-stable protocol fields, integer-valued floats within range, sentinels under a controlled contract, and results that are specified exactly. Approximate comparison is right only with a derived error/measurement model. Neither is universally safer.

**Reject versus propagate non-finite values.** Scientific kernels may intentionally propagate NaNs/infinities for later diagnosis. Business, storage, and security boundaries often require finite values and explicit errors. Choose at the boundary; do not let an accidental NaN become silent missing data.

**Deterministic reduction versus fastest reduction.** Fixing reduction tree, format, rounding, and contraction improves reproducibility. Dynamic parallel reduction can improve throughput and load balance but change low bits. Decide whether the consumer needs bitwise, bounded-error, statistical, or decision-level reproducibility.

## Failure Modes and Misconceptions

1. **“Floating point stores decimals.”** Binary formats store binary significands and exponents; decimal literals undergo conversion.
2. **“Binary64 has about 16 digits everywhere.”** Decimal-digit summaries hide nonuniform spacing, subnormals, and magnitude-dependent absolute precision.
3. **“If a value is in range, it is exact.”** Binary64 has enormous range but cannot distinguish every integer above $2^{53}$.
4. **“One epsilon fixes equality.”** A tolerance needs scale, units, uncertainty, algorithmic bound, and near-zero policy.
5. **“NaN is just another large or missing number.”** It is unordered and has special propagation, encoding, and serialization behavior.
6. **“`x != x` is the complete NaN policy.”** Classification, admissibility, optimizer mode, provenance, and boundary response remain unspecified.
7. **“Positive and negative zero are interchangeable.”** Numeric equality says yes; reciprocal, sign, branch-cut, bits, and serialization can say no.
8. **“Underflow means zero.”** Gradual underflow can produce subnormals; exact behavior depends on format, result, rounding, and mode.
9. **“An IEEE exception is a thrown language exception.”** Conditions, flags, traps, signals, and language exceptions are distinct.
10. **“Correct rounding makes an algorithm accurate.”** It controls each operation, not conditioning or accumulated error.
11. **“More precision makes algebraic rewrites safe.”** Non-associativity and exceptional cases remain in every finite format.
12. **“Same source and inputs guarantee identical bits.”** Toolchain, target, contraction, math library, environment, and reduction order can vary.
13. **“Fast math only makes answers slightly less precise.”** It can alter NaN, infinity, signed-zero, reassociation, and exception assumptions.
14. **“Dumping native float bytes is a portable file format.”** Endianness, format support, NaN conventions, and schema policy must be fixed.

## Worked Examples

### Example 1

**Question:** Why is decimal `0.1` not exact in a finite binary format?

**Reasoning:** In lowest terms it is $1/10$, and denominator 10 contains factor 5. A finite binary fraction has denominator dividing a power of two. No power of two cancels 5, so the expansion repeats and conversion must round.

**Conclusion:** The approximation follows number representation, not a defective adder.

### Example 2

**Question:** Why do $2^{53}$ and $2^{53}+1$ collide in binary64?

**Reasoning:** Precision is 53 bits. In the binade beginning at $2^{53}$, adjacent values are two apart. The odd integer lies exactly halfway between neighboring representable even integers; ties-to-even selects $2^{53}$ for this case.

**Conclusion:** Dynamic range does not imply unit resolution.

### Example 3

**Question:** What category does a zero exponent with nonzero fraction denote in an IEEE binary interchange format?

**Reasoning:** It is subnormal. The significand lacks the implicit leading one and uses the minimum normal exponent. Zero fraction in the same exponent category gives signed zero.

**Conclusion:** Exponent and fraction categories must be decoded together.

### Example 4

**Question:** Is `(a+b)+c` equivalent to `a+(b+c)` for binary64 addition?

**Reasoning:** With $a=2^{53}$, $b=1$, and $c=-2^{53}$, the first grouping rounds away `b` before cancellation and yields zero; the second preserves a unit residual and yields one under the stated mode.

**Conclusion:** Real-number associativity is not a floating-point identity.

### Example 5

**Question:** Why can a zero sign matter if `+0.0 == -0.0`?

**Reasoning:** Ordinary equality deliberately merges them, but the encoding preserves sign. IEEE-style reciprocal behavior distinguishes positive and negative infinity, and sign-sensitive transcendental or complex functions can preserve approach direction. Bitwise serialization also distinguishes them unless canonicalized.

**Conclusion:** Equality relation and representation identity are different.

### Example 6

**Question:** Can a program sort raw floats with ordinary `<` and assume a total order?

**Reasoning:** NaN is unordered, so comparisons needed for a strict total ordering do not behave like ordinary finite comparisons. The program must reject NaNs, map them to an explicit position, or use a language operation implementing a specified total order.

**Conclusion:** Collection ordering needs a non-finite policy.

### Example 7

**Question:** Does receiving infinity from a calculation always mean division by zero?

**Reasoning:** Infinity can be an input, arise from overflow, or result from division by zero under applicable semantics. Rounding direction affects some overflow results. Exception flags or prior classification may distinguish origin; the value alone may not.

**Conclusion:** Exceptional value and causal diagnostic are not the same evidence.

### Example 8

**Question:** Why can fused multiply-add change a test's expected low bits?

**Reasoning:** Separate multiplication and addition round twice. FMA computes the combined exact expression and rounds once. The fused result is often closer to the real result but is not required to match the two-step bit pattern. Build and test contracts must state whether contraction is allowed.

**Conclusion:** Greater local accuracy can still break an unspecified reproducibility assumption.

### Example 9

**Question:** Should a telemetry API accept any JSON numeric token into a floating field?

**Reasoning:** The schema should constrain finite range, units, resolution, and non-finite spelling policy. Standard JSON does not define NaN and infinity as ordinary numbers. The decoder must reject unsupported tokens and values, record conversion errors, and avoid treating NaN as absence.

**Conclusion:** Numeric syntax is only the first stage of domain validation.

### Example 10

**Question:** A radiation-treatment dose calculation is moved to a new vectorized build. What evidence supports equivalence?

**Reasoning:** A numerical reviewer must analyze conditioning, rounding bounds, exceptional inputs, subnormal policy, accumulation, contraction, and threshold sensitivity. A compiler/runtime reviewer must record target, instructions, flags, formats, rounding, libraries, and reduction order. A clinical physicist must validate units, calibration, dose model, admissible error, and acceptance cases. Safety and quality reviewers must evaluate hazard controls, traceability, rollback, and independent calculation. Differential and metamorphic tests need boundary/adversarial cases and archived artifacts. No external approval is claimed here.

**Conclusion:** Bit comparison is one possible datum inside a multidisciplinary safety case, not the safety case itself.

## Cross-Program Connections

- [Programming Languages & Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) defines observable equivalence and language-level numeric behavior.
- [Compilers & Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md) treats constant folding, excess precision, contraction, reassociation, and target lowering.
- [Concurrent & Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) studies reduction order and reproducible parallel aggregation.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) owns conditioning, stable algorithms, compensated summation, and empirical performance trade-offs.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) governs numeric schema, ingestion validation, non-finite values, and aggregation reproducibility.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) explains floating-point units, vector instructions, rounding hardware, and subnormal performance.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies differential, metamorphic, boundary, and reproducibility tests.

## References

1. IEEE Standards Association, [IEEE 754-2019: IEEE Standard for Floating-Point Arithmetic](https://standards.ieee.org/ieee/754/6210/). Active authoritative standard landing page covering formats, operations, conversions, exceptions, and default handling.
2. David Goldberg, [“What Every Computer Scientist Should Know About Floating-Point Arithmetic”](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html), *ACM Computing Surveys* 23(1), 1991. Foundational tutorial on representation, rounding, errors, guard digits, and system implications.
3. Oracle, [*The Java Language Specification*, §4.2.3 Floating-Point Types and Values](https://docs.oracle.com/javase/specs/jls/se25/html/jls-4.html#jls-4.2.3), Java SE 25. Current language value sets and exceptional categories.
4. Oracle, [*The Java Language Specification*, §15.4 Floating-Point Expressions](https://docs.oracle.com/javase/specs/jls/se25/html/jls-15.html#jls-15.4), Java SE 25. Current evaluation, value-set, overflow, underflow, NaN, and contraction rules.
5. Rust Project, [Rust `f64` primitive documentation](https://doc.rust-lang.org/stable/core/primitive.f64.html). Current official category, constants, bit-conversion, NaN, subnormal, and total-order APIs.
6. Python Software Foundation, [Floating-Point Arithmetic: Issues and Limitations](https://docs.python.org/3/tutorial/floatingpoint.html). Current official explanation of binary approximation, display, comparison, exact ratios, and summation tools.
7. ISO C++ working draft, [`numeric_limits` members](https://timsong-cpp.github.io/cppwp/support.limits#numeric.limits.members). Implementation properties for radix, precision, epsilon, infinity, NaN, subnormal values, rounding, and IEC 60559 adherence.
8. ISO C++ working draft, [Floating-point environment](https://timsong-cpp.github.io/cppwp/numerics#cfenv). Rounding direction, exception status, and environment access facilities.
9. William Kahan, [Lecture Notes on the Status of IEEE Standard 754](https://people.eecs.berkeley.edu/~wkahan/ieee754status/IEEE754.PDF), 1997. Primary historical and technical analysis of gradual underflow, exceptions, rounding, and implementation consequences.
10. Mike Cowlishaw, [General Decimal Arithmetic Specification](https://speleotrove.com/decimal/decarith.html). Primary specification for decimal arithmetic concepts, rounding, exceptional values, and context used by decimal implementations.

## Exercises

### Exercise 1

For a toy binary format with precision $p=4$, list the representable normal values in $[1,2)$, give their spacing, and state which value receives exact real number $1.3125$ under round-to-nearest ties-to-even.

### Exercise 2

Classify these categories and state one required handling rule for each: positive zero, negative zero, smallest positive subnormal, positive infinity, quiet NaN. Explain why ordinary numeric equality is insufficient to distinguish the set.

### Exercise 3

Using $a=2^{53}$, $b=1$, and $c=-2^{53}$, recompute both binary64 groupings `(a+b)+c` and `a+(b+c)` under round-to-nearest ties-to-even. Name the rounding point that creates the difference.

### Exercise 4

Design a boundary contract for ingesting temperature measurements into binary64. Include syntax, units, finite-range validation, NaN/infinity policy, signed zero, conversion/rounding, missing values, serialization, uncertainty, and audit evidence.

### Exercise 5

Prepare a verification plan for migrating a parallel risk-aggregation service to a new compiler and CPU. Cover formats, compiler flags, contraction/reassociation, rounding and subnormal modes, math library, reduction order, non-finite inputs, accuracy acceptance, performance evidence, security, financial-domain review, and the limits of automated validation.

## Answers to the Exercises

### Answer 1

With precision four, significands in $[1,2)$ are `1.000`, `1.001`, `1.010`, `1.011`, `1.100`, `1.101`, `1.110`, and `1.111`, corresponding to increments of $2^{-3}=0.125$. Thus 1.25 and 1.375 bracket 1.3125 exactly halfway. Their trailing stored significand integers are 2 and 3; ties-to-even selects the one with even least significant bit, 1.25 (`1.010`).

### Answer 2

Positive and negative zero are zero-category values with different signs; decide whether serialization preserves or canonicalizes the sign consistently with hashing and equality. The smallest positive subnormal is finite and nonzero with reduced relative precision; do not reject it as zero unless the domain explicitly flushes tiny values. Positive infinity is non-finite and must be admitted only for a defined unbounded/overflow meaning. Quiet NaN is unordered and must be rejected, propagated, or placed by an explicit policy. Ordinary equality merges the two zeros, reports NaN unequal to itself, and cannot express category/provenance, so classification and sign-aware operations are required.

### Answer 3

At $a=2^{53}$, binary64 spacing is two. Exact $a+b=2^{53}+1$ is a midpoint; ties-to-even rounds it to $2^{53}$. Adding $c=-2^{53}$ then yields zero. For the other grouping, $b+c=1-2^{53}=-(2^{53}-1)$, an exactly representable integer in range; adding $a$ yields one. The decisive information loss is the first grouping's rounding of $a+b$.

### Answer 4

Accept a documented decimal grammar plus an explicit unit such as degrees Celsius. Parse with a specified correctly rounded conversion into binary64 or reject conversion failure. Require finite values within the sensor's calibrated interval; reject NaN and infinities with structured reasons. Normalize `-0.0` only if the domain proves direction/sign irrelevant, and make hashing/serialization agree. Represent missing readings as a distinct tagged state, never NaN. Serialize with enough decimal digits for round trip or a specified binary64 big-endian field. Retain source token, device/time identity, calibration version, unit conversion, uncertainty, quality flags, parsed bits, and validation outcome. A finite in-range value still needs provenance and plausibility checks.

### Answer 5

Pin source, compiler version, target/ISA, flags, link-time optimization, floating format, rounding mode, exception environment, contraction and reassociation permissions, flush-to-zero/denormal mode, math library, thread count, partitioning, and reduction tree. Build reference datasets spanning cancellation, large dynamic range, subnormals, signed zeros, infinities, NaNs, thresholds, empty/singleton partitions, and adversarial input sizes. Compare against a higher-precision or analytically justified oracle using documented absolute/relative/ulp and decision-level limits; archive bitwise and error-distribution reports. Measure performance with workload, warmup, affinity, counters, uncertainty, and tail latency.

Security review must cover malformed numeric encodings, non-finite injection, resource exhaustion, artifact provenance, and unsafe compiler assumptions. Named numerical and financial-risk reviewers must approve conditioning, aggregation meaning, tolerances, regulatory reporting, and threshold consequences; reliability reviewers must approve rollback and observability. Automation can show repeatability and bounded disagreement for tested environments, but cannot establish universal numerical correctness, financial model validity, regulatory compliance, or production safety. This answer claims no external review.
