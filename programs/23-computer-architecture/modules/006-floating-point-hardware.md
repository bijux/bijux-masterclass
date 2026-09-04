---
module_id: CA-006
program: Computer Architecture
level: 1
module_number: 6
title: Floating-Point Hardware
status: complete
last_verified: 2026-09-04
---

# Floating-Point Hardware

## One-Page Review

### Governing question

How can hardware represent a wide dynamic range, execute floating-point operations with specified rounding and exceptional behavior, and preserve exact format, flag, latency and reproducibility contracts across pipelines and implementations?

### Essential definitions

- A **floating-point format** encodes sign, exponent and trailing significand fields plus special values.
- A **normal number** uses a nonzero, non-all-ones exponent and an implicit leading significand bit in a binary interchange format.
- A **subnormal number** uses the minimum exponent with no implicit leading one, providing gradual underflow toward zero.
- **signed zero** represents positive or negative zero, which compare equal numerically but can affect some operations.
- **infinity** represents an unbounded result or operand under defined operations; it is not the largest finite number.
- A **NaN** represents not-a-number results; quiet and signaling forms have different exception behavior.
- A **unit in the last place**, or ulp, is spacing at a specified representable value scale.
- **round to nearest, ties to even** selects the closest representable value and resolves exact midpoint ties toward an even retained least-significant bit.
- **guard, round and sticky bits** summarize discarded significand information needed for correct rounding decisions.
- **fused multiply-add**, or FMA, computes `a*b+c` with one final rounding rather than rounding the product first.
- Floating-point **status flags** record invalid operation, division by zero, overflow, underflow and inexact under the architectural contract.

### Central model, mechanism, or theorem

For a normal binary value with sign `s`, biased exponent field `E`, bias `B` and fraction bits representing `F`, the value is

`(-1)^s * (1+F) * 2^(E-B)`.

For subnormals, the leading significand bit is zero and exponent uses the minimum normal exponent. Arithmetic proceeds through exact conceptual result followed by one declared rounding into the destination format, while special-value and exception rules select alternate results where required. Correct hardware must agree not merely on approximate magnitude but on the exact result bits, NaN/zero semantics and flags for every modeled operand and rounding mode.

### Critical invariants

- Format width, field layout, precision, exponent range and special encodings are explicit.
- Every operation names its rounding mode, destination format and exception behavior.
- Alignment and normalization preserve all information needed by guard, round and sticky logic until final rounding.
- Signed zero, infinity, quiet/signaling NaN and subnormal cases take specified paths before ordinary arithmetic assumptions are applied.
- FMA retains sufficient internal precision to round the mathematical `a*b+c` only once.
- Conversion, comparison, minimum/maximum and sign operations follow the target ISA or standard rather than intuition.
- Pipeline tags, rounding modes, results and accrued flags remain aligned through stalls, flushes and exceptions.
- Exhaustive/formal format evidence remains distinct from synthesis, timing, power and physical evidence.

### Common failures

Frequent failures are treating floating point as real arithmetic, assuming every finite integer is exactly representable, decoding subnormals with an implicit one, calling negative zero identical in every operation, treating NaN as one universal bit pattern, propagating signaling NaNs without invalid flag, using truncation as all rounding modes, dropping sticky information, double-rounding intermediate values, flushing subnormals without declaring it, confusing overflow with infinity input, detecting underflow from exponent alone, implementing FMA as multiply then add, and comparing decimal text or host-language results without controlling format and rounding.

### Compact example

Binary32 pattern `0x3f800000` is normal `+1`; `0x80000000` is negative zero; `0x00000001` is the least positive subnormal `2^-149`; `0x7f800000` is positive infinity; and `0x7fc00001` is a quiet NaN with payload bits. All occupy 32 bits, but exponent and fraction classes change decoding before ordinary numerical interpretation.

### Connections

Floating-point hardware connects scientific computing, numerical analysis, ISA contracts, compilers, vector and accelerator design, pipelines, exception handling, formal verification, reproducible computation and physical implementation.

## Governing Question

Integers provide uniform absolute spacing but limited range. Floating point trades uniform spacing for a significand whose scale is selected by an exponent. That enables extremely small and large magnitudes while making rounding unavoidable.

The governing question is how hardware implements that abstraction exactly. An adder must align operands before adding; cancellation may require a long normalization shift; a multiplier must combine signs, exponents and significands; every path must round and raise flags under the selected semantics.

## Why This Matters

Floating point supports graphics, machine learning, simulation, finance, signal processing and scientific workloads. A one-bit rounding defect can destabilize a long computation or break cross-machine reproducibility. Mishandling NaNs can bypass comparisons or poison aggregates.

The hardware is also structurally different from integer arithmetic. Addition latency depends on exponent comparison, shifting and normalization. Division and square root may iterate. FMA changes both accuracy and compiler-visible results. Subnormal support affects datapaths and performance.

“Close enough” is not a complete architectural claim. Standards and ISAs define exact results for basic operations under specified modes. Approximate units need a separate contract with explicit error and domain limits.

## Prerequisites and Retrieval

Before studying this module, be able to:

- interpret unsigned and two's-complement fields;
- reason about fixed-width addition, multiplication, shifts and leading bits;
- distinguish mathematical value, bit pattern and exception flag;
- explain combinational, iterative and pipelined hardware;
- use powers of two and basic error bounds.

Retrieve source and destination formats; operation set; supported rounding modes; subnormal policy; NaN payload and signaling behavior; signed-zero rules; exception flags and trap policy; conversions and comparisons; FMA semantics; latency and initiation interval; stalls and flushes; vector lane behavior; accumulation precision; target ISA; HDL signedness; reference model; conformance suite; synthesis mapping; hardened block modes; timing, area and power; clock and reset; fault model; and exact tool, configuration and artifact identities.

## Learning Objectives

After completing this module, you should be able to:

1. decode normal, subnormal, zero, infinity and NaN patterns;
2. explain biased exponents and implicit significand bits;
3. apply rounding modes using guard, round and sticky information;
4. trace floating-point addition and subtraction stages;
5. trace multiplication, division, square root and FMA stages;
6. distinguish exception flags and special-value behavior;
7. specify conversions, comparisons and mixed-precision operations;
8. compare iterative, pipelined and approximate implementations;
9. verify exact result bits and flags across all operation classes;
10. assess performance, reproducibility, security and physical trade-offs.

## Core Exposition

### Separate value from encoding

A floating-point datum is a fixed bit pattern. Its class and value follow format rules. Bitwise identity is stronger than numerical equality: positive and negative zero compare equal numerically but have different encodings.

NaNs are unordered under ordinary comparisons and can carry payload. Never infer semantic equality from raw fields or raw identity from numerical comparison.

### Decode binary interchange fields

Binary formats divide bits into sign, exponent and fraction. For binary32, widths are 1, 8 and 23, with exponent bias 127 and normal precision 24 including the implicit leading one.

Binary64 uses wider exponent and fraction fields. Parameterized hardware must derive constants from the selected format rather than embed binary32 assumptions.

### Decode normal numbers

For exponent fields between all-zero and all-one, subtract bias to obtain the unbiased exponent. Prefix the fraction with an implicit one.

The spacing between adjacent normals grows with exponent. Relative precision is roughly uniform within the normal range; absolute precision is not.

### Decode subnormal numbers

An all-zero exponent with nonzero fraction represents `fraction * 2^(minimum normal exponent)` without an implicit leading one. Subnormals fill the gap between zero and the least normal.

Gradual underflow reduces abrupt loss near zero. Leading-zero normalization and low-precision paths can cost hardware and latency.

### Decode zeros, infinities and NaNs

All-zero exponent and fraction encode signed zero. All-one exponent with zero fraction encodes signed infinity. All-one exponent with nonzero fraction encodes NaN.

A designated fraction bit commonly distinguishes quiet from signaling NaNs in an interchange convention. Payload propagation and canonicalization follow the architecture.

### Understand representable spacing

Within one binade, adjacent normal numbers have constant absolute spacing determined by exponent and precision. Moving to the next binade doubles spacing.

Integers are exactly representable only while precision suffices. At larger magnitudes, adjacent floats skip some integers. Converting, incrementing and converting back can lose change.

### Define rounding as part of the operation

An exact mathematical result usually falls between representable values. Rounding selects one according to the active mode.

Common modes include nearest ties-to-even, toward zero, toward positive infinity and toward negative infinity. Some formats or extensions support additional modes. The mode can be instruction-encoded or architectural state.

### Use guard, round and sticky bits

The guard and round bits retain leading discarded positions; sticky is the OR of all remaining discarded nonzero bits. Together with the retained least-significant bit and sign, they decide rounding.

Sticky must remain true once any shifted-away bit is one. Keeping only one discarded bit can misclassify a midpoint or exact result.

### Apply ties to even

For exact halfway cases under nearest-even, increment the retained significand only when its low retained bit is odd. This avoids a systematic upward bias from always rounding midpoint away.

For values beyond halfway, increment regardless of evenness. For values below, retain. Rounding can carry out and require exponent adjustment.

### Align addition operands

Compare exponents and right-shift the smaller significand by the exponent difference. Accumulate all discarded ones into sticky.

If the difference is very large, the smaller operand may not change the retained result but can still make it inexact or determine directed rounding.

### Add or subtract significands

Equal operand signs add magnitudes and preserve the sign. Different signs subtract smaller magnitude from larger and take the larger magnitude's sign, subject to exact-zero sign rules.

Effective subtraction can cancel many leading bits, making normalization a long left shift. Compare magnitude, not raw signed fields.

### Normalize the addition result

An addition carry can shift the significand right and increment exponent. Cancellation can require leading-zero detection, left shift and exponent decrement.

Normalization must preserve rounding information. Underflow handling may produce a subnormal before rounding; rounding can then lift it into the least normal.

### Handle exact zero

Exact cancellation yields zero. Its sign depends on rounding mode and operation rules rather than whichever operand happened to win an internal mux.

Zero retains useful directional information for reciprocal, complex functions and branch behavior. Test all sign combinations.

### Multiply significands and exponents

Product sign is operand-sign XOR. Add unbiased exponents and multiply significands, producing roughly twice the precision before normalization.

The product lies in a bounded range requiring at most a small normalization adjustment for normal operands. Round once into the destination format.

### Handle special multiplication cases

Zero times infinity is invalid and produces NaN under standard semantics. Infinity times a finite nonzero operand produces signed infinity.

NaNs generally take priority according to propagation rules. Do special classification before ordinary exponent arithmetic overflows fields.

### Implement division iteratively

Floating division subtracts exponents and divides significands, then normalizes and rounds. Digit-recurrence methods generate quotient digits over cycles; multiplicative methods use reciprocal approximation and refinement.

Iterations must produce enough extra bits and a correct sticky indication for final rounding. Terminating early based on approximation needs a proof of the rounding decision.

### Implement square root

Square root halves an adjusted exponent and computes a significand root using recurrence or iterative approximation. Negative finite inputs other than negative zero are invalid.

Remainder information decides correct rounding. A close approximation without a proven rounding interval is not necessarily the required result.

### Fuse multiply and add

FMA forms the exact product, aligns it with the addend, adds and rounds once. Separate multiply and add round twice and can produce a different result.

FMA improves accuracy and performance for dot products and polynomial kernels. Compiler contraction changes numerical behavior and must follow language and user controls.

### Preserve enough internal precision

An implementation can use recoded formats, carry-save representations or widened accumulators internally. External behavior must match the declared destination rounding.

Dropping product or alignment bits before sticky and rounding are established risks incorrect last bits. Formal recoding equivalence is valuable.

### Raise invalid-operation flags

Invalid operations include signaling NaN inputs and specified indeterminate forms such as infinity minus infinity, zero times infinity or square root of a negative finite value.

The result is a quiet NaN under nontrapping behavior, with payload selection defined by the architecture. Invalid is different from inexact.

### Raise division-by-zero flags

Finite nonzero divided by zero produces signed infinity and raises division by zero under the usual basic operation. Zero divided by zero is invalid instead.

Classification order matters. NaN operands follow NaN behavior rather than ordinary division rules.

### Raise overflow flags

Overflow occurs when a rounded result's magnitude exceeds the destination finite range under the standard's tininess and rounding rules. Result may be infinity or greatest finite value depending on direction.

Overflow generally implies inexact for ordinary finite operands. An infinity input is not itself an overflow event.

### Raise underflow and inexact flags

Inexact says rounded result differs from exact result. Underflow concerns tiny inexact results under the standard's detection rule; an exact subnormal need not raise underflow.

Architectures can specify tininess detection before or after rounding. Do not infer underflow merely from an all-zero exponent.

### Accrue status flags

Status flags are often sticky architectural state: once raised, they remain until explicitly cleared. Individual vector lanes can contribute to one accrued flag set.

Pipeline each operation's flags with its result and accrue only on valid nonsquashed completion. Traps, if supported, need precise ordering.

### Compare floating-point values

Ordinary equality treats signed zeros as equal and NaN as unequal to everything, including itself. Ordered comparisons are false for NaN and can raise invalid for signaling or specified quiet cases.

Total-order predicates can order encodings or classes for sorting without being ordinary numerical comparison. Use the exact ISA operation.

### Define min and max semantics

Minimum and maximum operations differ across historical specifications and ISAs in NaN and signed-zero treatment. Some return a numeric operand when the other is quiet NaN; others propagate or canonicalize.

Do not implement min as only `a<b ? a:b`. Equal zeros and unordered NaNs need explicit selection.

### Convert integers and floats

Integer-to-float conversion may round when integer magnitude exceeds significand precision. Float-to-integer conversion needs rounding rule, range checks, NaN/infinity handling and destination signedness.

Detect invalid before narrow truncation loses information. ISA-defined saturation or sentinel results are not universal.

### Convert between formats

Widening from a smaller binary format is exact for finite values when the larger format contains its range and precision, though NaN payload treatment can change bits. Narrowing rounds and can overflow or underflow.

Double rounding can occur when a value is rounded first to an intermediate precision and then to a smaller one. Direct conversion should round once from sufficient source information.

### Address subnormal performance policy

Some implementations flush input or output subnormals to zero for speed. That changes numerical semantics and flags and can break algorithms relying on gradual underflow.

Expose the mode, control privilege and context-switch behavior. Benchmark subnormal paths separately; do not hide a variable-latency assist.

### Use recoded internal formats

Internal recoding can distinguish classes conveniently, widen exponents or normalize subnormals early. Berkeley HardFloat is an example of parameterized recoded implementation structure.

Prove conversion into and out of recoded state, including NaNs and zeros. Internal representation is not the architectural storage format.

### Pipeline floating-point units

Stages can classify, align, operate, normalize and round. Multipliers and FMAs may use compressor trees and several registers.

Carry operand tags, operation, format, rounding mode and validity. Stalls and flushes must keep result and flags together. Variable divide/square-root units need arbitration with pipelined paths.

### Map to hardened blocks

FPGA floating-point IP and DSP resources offer configured widths, modes and latencies. Not every combination is fully IEEE conformant, and resource/latency settings change behavior.

Record generator version and parameters; inspect mapping; verify wrapper backpressure and flags. A vendor core's existence does not prove the system integration.

### Support vector and mixed precision

Vector lanes repeat operations but share issue, exception and mask behavior. Inactive lanes must not raise flags or alter state unless specified.

Mixed-precision multiply-accumulate can multiply narrow inputs and accumulate wider. State where rounding occurs and whether reduction order is fixed.

### Understand reproducibility limits

Associativity fails after rounding: `(a+b)+c` can differ from `a+(b+c)`. Parallel reduction order, FMA contraction, extended intermediates and flush modes affect bits.

Reproducibility needs controlled format, rounding, operation order, compiler options and environment. Numerical stability can matter more than identical bits, but it is a separate requirement.

### Consider security and faults

Variable-latency subnormal or divide paths can expose operand classes. Shared FP units create contention channels. NaN payloads can carry untrusted data through computations.

Parity, residue checks or duplication can cover selected datapath faults. Include control, rounding and flag logic; a correct approximate magnitude with a wrong exception remains faulty.

### Verify by classes and boundaries

Partition operands into zeros, subnormals, least and greatest normals, infinities, quiet/signaling NaNs and ordinary values. Cross signs, rounding modes and operations.

Target halfway cases, just-below/above ties, cancellation, normalization boundaries, overflow thresholds and exact/tiny results. Random values rarely hit the hardest rounding cases.

### Use independent exact references

Reference models should compute with enough exact integer or rational precision, then apply destination rounding once. Host floating point can reproduce its own double rounding or mode instead of the target.

Compare exact bits and flags. Formal proofs and established test generators can complement directed and random simulation.

### Verify implementation layers

Inspect HDL widths and recoding; validate synthesis or IP parameters; close setup and hold; test stalls, masks, flushes and precise flags; measure latency and throughput.

Post-layout and silicon evidence cover wiring, glitches, voltage, temperature, variation and faults. Preserve standard/ISA edition, tools, configuration, seeds, counterexamples and waivers.

## Definitions and Notation

- `s`: sign bit.
- `E`: stored biased exponent field.
- `B`: exponent bias.
- `F`: fractional significand value represented by trailing fraction bits.
- `p`: significand precision including any implicit leading bit.
- **binade:** interval between consecutive powers of two with one exponent scale.
- **ulp:** spacing of representable values at a specified scale.
- **GRS:** guard, round and sticky information below retained precision.
- **exact result:** mathematical operation result before destination rounding.
- **normal:** finite nonzero class with an implicit leading one in binary interchange decoding.
- **subnormal:** finite nonzero class with minimum exponent and leading zero.
- **qNaN, sNaN:** quiet and signaling NaN classes.
- **canonical NaN:** implementation- or ISA-selected NaN pattern used when payload is not preserved.
- **tininess:** result condition near or below the least normal, evaluated under a declared rule.
- **inexact:** flag that destination result differs from exact result.

## Mechanisms, Invariants, or Proof Structure

1. **Format claim:** define bit fields, bias, precision, range and all special encodings.
2. **Classification invariant:** select zero, subnormal, normal, infinity and NaN paths correctly.
3. **Exactness model:** define the conceptual exact operation before rounding.
4. **Alignment invariant:** preserve shifted-away information in sticky state.
5. **Normalization invariant:** maintain value while adjusting exponent and significand.
6. **Rounding invariant:** choose the unique destination under the selected mode.
7. **Special-case invariant:** NaN, infinity, zero and invalid combinations follow priority rules.
8. **Flag invariant:** invalid, divide-zero, overflow, underflow and inexact match result formation.
9. **FMA invariant:** retain full product/add precision through one final rounding.
10. **Conversion invariant:** check source class, range, signedness and destination rounding.
11. **Pipeline invariant:** tag, mask, mode, result and flags advance atomically.
12. **Mapping claim:** IP or synthesized structure preserves format, modes, flags and latency.
13. **Timing claim:** all paths meet clock and physical constraints at required corners.
14. **Evidence invariant:** separate conformance, formal, RTL, mapped and silicon claims.
15. **Change invariant:** revalidate after format, standard, ISA, IP or pipeline change.

## Alternatives and Trade-Offs

- **Floating versus fixed point:** floating spans range automatically; fixed point provides explicit scale and often simpler hardware.
- **Gradual underflow versus flush to zero:** subnormals preserve small values; flushing simplifies and speeds some implementations.
- **Payload propagation versus canonical NaN:** propagation preserves diagnostics; canonicalization improves determinism and reduces paths.
- **Nearest-even versus directed rounding:** nearest-even limits average error; directed modes support intervals and bounds.
- **FMA versus separate operations:** FMA rounds once and improves throughput; separate operations preserve explicitly staged rounding.
- **Iterative versus pipelined divide:** iteration saves area; pipelines or replicated units raise throughput.
- **Digit recurrence versus reciprocal refinement:** recurrence yields quotient digits directly; refinement exploits multipliers and needs error bounds.
- **Standard precision versus mixed precision:** uniform precision simplifies reproducibility; mixed precision improves density and needs error analysis.
- **Recoded versus interchange internal format:** recoding simplifies class handling; interchange form reduces conversion boundaries.
- **Fixed versus variable latency:** fixed timing simplifies scheduling; variable assists optimize common classes and expose timing.
- **Per-operation versus accrued flags:** per-operation flags attribute cause; accrued flags match architectural environments efficiently.
- **Exact conformance versus approximation:** exact units support portable semantics; approximate units trade error for cost under narrower contracts.
- **Deep pipeline versus short latency:** deep stages raise frequency and throughput; short paths reduce cycles and control state.
- **Shared versus replicated units:** sharing saves area; replication reduces contention and side channels.
- **Bitwise reproducibility versus optimized reduction:** fixed order preserves bits; reassociation and parallel trees improve performance.

## Failure Modes and Misconceptions

1. **“Floating point represents real numbers.”** it represents a finite set plus special classes.
2. **“Every integer fits exactly in binary32.”** spacing eventually exceeds one.
3. **“Exponent zero always means zero.”** nonzero fraction encodes subnormal.
4. **“Exponent all ones always means infinity.”** nonzero fraction encodes NaN.
5. **“Negative zero is identical in every operation.”** encoding and functions such as reciprocal distinguish sign.
6. **“All NaNs are the same bits.”** quiet/signaling and payload encodings vary within rules.
7. **“NaN compares equal to itself.”** ordinary equality is false.
8. **“Truncation implements nearest rounding.”** it rounds toward zero for magnitude under limited conditions.
9. **“Guard alone decides rounding.”** lower discarded bits distinguish ties from beyond-tie values.
10. **“A tiny result always underflows.”** exact subnormal results need not raise underflow.
11. **“An infinity result always means overflow.”** infinity operands can produce infinity without overflow.
12. **“FMA is syntactic multiply plus add.”** it has one rounding and can differ in bits.
13. **“Addition only needs an integer adder.”** alignment, normalization, special cases and rounding dominate.
14. **“Multiplication needs no rounding if significands are exact.”** destination precision is smaller than full product.
15. **“Division approximation close enough is correctly rounded.”** a last-bit proof needs a bounded interval.
16. **“Zero divided by zero raises divide-by-zero.”** it is invalid.
17. **“Float-to-int is just dropping fraction bits.”** range, NaN, infinity and rounding need policy.
18. **“Wider conversion changes no bits.”** NaN payload/canonicalization can change encoding.
19. **“Flushing subnormals is only a performance option.”** it changes values and flags.
20. **“Min is implemented by one less-than mux.”** NaNs and signed zeros need special rules.
21. **“Flags can be recomputed from final bits.”** exactness and invalid causes may be lost.
22. **“Masked vector lanes may raise harmless flags.”** inactive-lane side effects violate common contracts.
23. **“Same ISA guarantees identical results for all expressions.”** operation order and environment matter.
24. **“Host double is an exact binary32 oracle.”** intermediate precision and rounding can differ.
25. **“Random testing finds rounding boundaries.”** directed exact cases are essential.
26. **“Correct result bits prove the FPU.”** flags, latency, masks, exceptions, timing and faults remain.

## Worked Examples

### Example 1

Binary32 `0x3f800000` has sign 0, exponent 127 and fraction 0, so it represents `1.0 * 2^0 = 1`.

### Example 2

Pattern `0x80000000` is negative zero. It compares equal to positive zero, while reciprocal sign and total ordering can distinguish it.

### Example 3

Pattern `0x00000001` has zero exponent and one low fraction bit, so it is the least positive binary32 subnormal, `2^-149`.

### Example 4

Adding a tiny value to a large normal can leave result bits unchanged but set inexact because discarded sticky information is nonzero.

### Example 5

Subtracting nearly equal numbers cancels leading significand bits and requires a long normalization shift, making addition hardware asymmetric in cost.

### Example 6

An exact halfway value rounds to the candidate with an even retained low bit under nearest-even, not always away from zero.

### Example 7

`0 * infinity` produces NaN and invalid; it does not follow ordinary sign/exponent multiplication.

### Example 8

Separate multiply and add round the product before addition. FMA retains product precision and can return a different final low bit.

### Example 9

A vector mask disables a lane containing signaling NaN. If the ISA suppresses inactive-lane evaluation, invalid must not accrue from it.

### Example 10

A vendor IP core returns correct normals but is configured to flush subnormals. It is not conformant to a contract requiring gradual underflow.

## Cross-Program Connections

- **Numerical analysis:** conditioning, stability and error accumulation govern algorithmic meaning.
- **Integer arithmetic:** significand operations, shifts, leading detection and counters form the datapath.
- **Instruction sets:** formats, rounding environment, flags, conversions and FMA are architectural contracts.
- **Compilers:** contraction, reassociation, excess precision and fast-math options change computations.
- **Pipelines:** variable latency, tags, masks and precise exceptions coordinate execution.
- **Vector architecture:** lane masks, reductions and mixed precision multiply hardware effects.
- **Accelerators:** tensor units trade formats and accumulation precision for throughput and energy.
- **Formal verification:** exact bit-vector and rational reference models prove last-bit behavior.
- **Security:** timing, contention, subnormal assists and payloads can expose information.
- **Systems engineering:** consequential numerical use needs domain error budgets and independent validation.

## References

1. IEEE, [IEEE 754-2019 — Standard for Floating-Point Arithmetic](https://standards.ieee.org/ieee/754/6210/), formats, operations, rounding, exceptions and special values; retrieved 2026-09-04.
2. RISC-V International, [F Extension for Single-Precision Floating-Point](https://docs.riscv.org/reference/isa/unpriv/f-st-ext.html), architectural registers, rounding, flags, NaNs and operations; retrieved 2026-09-04.
3. University of California, Berkeley, [Berkeley HardFloat](https://github.com/ucb-bar/berkeley-hardfloat), parameterized recoded floating-point hardware and operation modules; retrieved 2026-09-04.
4. AMD, [Floating-Point Operator](https://docs.amd.com/r/en-US/pg060-floating-point), configurable FPGA floating-point operations, precision, latency and resource behavior; retrieved 2026-09-04.
5. Intel, [Floating-Point Functions](https://www.intel.com/content/www/us/en/docs/programmable/683750/20-1/floating-point-functions.html), FPGA floating-point IP functions and configuration; retrieved 2026-09-04.
6. David Goldberg, [What Every Computer Scientist Should Know About Floating-Point Arithmetic](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html), rounding, guard digits, exceptions and numerical consequences; retrieved 2026-09-04.
7. Sarah L. Harris and David Money Harris, [Digital Design and Computer Architecture: RISC-V Edition Resources](https://pages.hmc.edu/harris/ddca/ddcarv.html), floating-point representation and processor hardware context; retrieved 2026-09-04.

## Exercises

### Exercise 1

Decode binary32 patterns `0x3f800000`, `0x80000000`, `0x00000001`, `0x7f800000` and `0x7fc00001` by class, sign and exact value or NaN description.

### Exercise 2

Explain guard, round and sticky behavior for values below, exactly at and above a midpoint under round-to-nearest ties-to-even.

### Exercise 3

Trace floating-point addition from classification through alignment, operation, normalization, rounding and flags for severe cancellation and for a huge exponent gap.

### Exercise 4

Design a pipelined binary32 FMA interface supporting rounding mode, stalls, flushes, vector masks and accrued flags. State invariants and evidence.

### Exercise 5

Construct an assurance plan for floating-point hardware used in a medical dose calculation. Include numerical requirements, conformance, faults, physical evidence and named review.

## Answers to the Exercises

### Answer 1

`0x3f800000` is positive normal 1. `0x80000000` is negative zero. `0x00000001` is positive subnormal `2^-149`. `0x7f800000` is positive infinity. `0x7fc00001` is a positive quiet NaN under the binary32 quiet-bit convention, with nonzero payload.

<!-- bijux-verify: {"id":"binary32-classification","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"0x3f800000 class=normal sign=0 value=1\n0x80000000 class=zero sign=1 value=-0\n0x00000001 class=subnormal sign=0 value=2^-149\n0x7f800000 class=infinity sign=0 value=+inf\n0x7fc00001 class=quiet_nan sign=0 payload=0x400001\n"}} -->
```python
def describe(bits):
    sign = bits >> 31
    exponent = (bits >> 23) & 0xFF
    fraction = bits & 0x7FFFFF
    if exponent == 0:
        if fraction == 0:
            return "zero", "-0" if sign else "+0"
        if fraction == 1:
            return "subnormal", "2^-149"
        return "subnormal", f"fraction=0x{fraction:x}"
    if exponent == 0xFF:
        if fraction == 0:
            return "infinity", "-inf" if sign else "+inf"
        kind = "quiet_nan" if fraction & (1 << 22) else "signaling_nan"
        return kind, f"payload=0x{fraction:x}"
    if bits == 0x3F800000:
        return "normal", "1"
    unbiased = exponent - 127
    return "normal", f"exponent={unbiased} fraction=0x{fraction:x}"


for bits in (0x3F800000, 0x80000000, 0x00000001, 0x7F800000, 0x7FC00001):
    kind, detail = describe(bits)
    label = "payload" if "nan" in kind else "value"
    if detail.startswith("payload="):
        detail = detail.split("=", 1)[1]
    print(f"0x{bits:08x} class={kind} sign={bits >> 31} {label}={detail}")
```

The code intentionally handles five pedagogical patterns and does not implement general exact binary32 formatting, arithmetic, rounding, signaling behavior or flags.

### Answer 2

Below the midpoint, retain the nearer lower-magnitude representable candidate for the local ordering; guard/round/sticky show discarded magnitude is less than half. Above the midpoint, increment toward the nearer upper candidate. At exactly halfway, discarded information encodes a tie: guard is one while lower discarded information is zero. Increment only when the retained least-significant bit is one, so the selected result's low bit becomes even.

For directed modes, sign and whether any discarded bit is nonzero determine increment direction. Sticky is the OR of all bits below the explicit round position and must survive arbitrarily large alignment shifts. A rounding increment that carries through the significand can renormalize and increase exponent.

### Answer 3

Classify operands first and dispatch special cases. For finite normals, compare exponents and magnitudes. In severe cancellation, align the smaller, subtract significands, detect many leading zeros, shift left, decrement exponent, then round from preserved GRS information. The result may become subnormal or exact zero; zero sign and underflow/inexact follow declared rules.

For a huge exponent gap, right-shift the small significand beyond retained precision while OR-reducing every lost one into sticky. The large operand's result bits may remain unchanged, but inexact is raised and directed rounding may move to the adjacent representable value. Validate both paths at exponent/subnormal boundaries and halfway cases.

### Answer 4

Accept operands, operation tag, destination format, rounding mode and active-lane mask only on input handshake. Carry them through classify, multiply, align/add, normalize and round stages. Each register bank advances or stalls atomically. A flush invalidates all younger entries; inactive lanes generate neither result effects nor flags under the selected ISA.

FMA retains the full product and add alignment until one final rounding. Output handshake holds result, tag and per-operation flags stable. Architectural accrual occurs only for accepted, active, nonsquashed completions in order required by the machine. Assertions cover no drop/duplication, tag/mode/mask alignment, stall stability, flush suppression, special cases and one-rounding equivalence. Evidence combines exact reference comparison, directed boundaries, formal properties, synthesis/IP configuration, timing, power and physical tests.

### Answer 5

Define dose formula, permitted formats and modes, input ranges/units, maximum numerical error, exceptional-input policy, required diagnostic coverage and end-to-end clinical consequence. Analyze conditioning and algorithm stability independently of hardware conformance. Compare every hardware operation with an exact reference over directed special classes and rounding boundaries; use formal or established conformance evidence where feasible.

Trace compiler contraction, conversion, library and ISA environment into deployed code. Fault-inject datapath, exponent, rounding, flag, register and control errors; verify detection and safe response. Close timing across required voltage, temperature, aging and process conditions and test reset, clock and power faults. Preserve artifacts, tools, configuration, raw results, counterexamples and limitations. Named numerical-analysis, clinical pharmacology, medical-device, architecture, RTL, physical, safety, cybersecurity, verification, quality, regulatory and independent-assurance authorities review their scopes. This course module supplies no clinical authorization or certification.
