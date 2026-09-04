---
module_id: CA-005
program: Computer Architecture
level: 1
module_number: 5
title: Integer Arithmetic Circuits
status: complete
last_verified: 2026-09-04
---

# Integer Arithmetic Circuits

## One-Page Review

### Governing question

How can an architect implement fixed-width integer addition, subtraction, multiplication and division while preserving the exact bit-vector, signedness, flag, latency and exception contract across logic, RTL, synthesis and physical timing?

### Essential definitions

- An **unsigned `N`-bit integer** represents values from `0` through `2^N-1`.
- A **two's-complement `N`-bit integer** represents values from `-2^(N-1)` through `2^(N-1)-1` using the same `N` bit patterns.
- A **half adder** adds two bits; a **full adder** adds two operand bits and a carry-in.
- **carry-out** records an unsigned sum beyond the most significant bit; **signed overflow** records a two's-complement result outside its representable range.
- **borrow** indicates that an unsigned subtraction required value below zero; conventions for exposing carry/borrow must be specified.
- **propagate** and **generate** summarize whether a bit or group passes an incoming carry or creates a carry independently.
- A **ripple-carry adder** chains carries serially; a **carry-lookahead or parallel-prefix adder** computes carry relationships in a tree or hierarchy.
- **sign extension** widens a two's-complement value by repeating its sign bit; **zero extension** widens an unsigned value with leading zeros.
- A **partial product** is one shifted contribution to multiplication.
- **Booth recoding** reduces or regularizes partial products by encoding runs of multiplier bits as signed multiples.
- An **iterative divider** reuses arithmetic state over cycles; a **fully unrolled divider** exposes more parallel logic and a long path.

### Central model, mechanism, or theorem

For width `N`, fixed-width addition computes

`r = (a + b + cin) mod 2^N`, with `carry = floor((a+b+cin)/2^N)`.

The same `r` is correct at the bit-vector level for unsigned and two's-complement addition. Interpretation changes the exception flag. For signed operands, overflow occurs when both inputs have the same sign and the result has the opposite sign. Subtraction uses `a - b = a + not(b) + 1` modulo `2^N`; unsigned borrow and signed overflow remain distinct. Every arithmetic block must state width, signed interpretation, widening, rounding or truncation, flags, latency and behavior on exceptional operands.

### Critical invariants

- Every operand and intermediate has an explicit width and signedness.
- Arithmetic output equals the specified mathematical result modulo, saturated to, or trapped at the declared range.
- Carry, borrow, zero, negative and overflow flags follow one documented convention for every operation.
- Widening occurs before information is lost; sign and zero extension match operand interpretation.
- Partial-product generation and reduction preserve the exact full-precision product before declared truncation.
- Iterative arithmetic owns operands and quotient/remainder state until completion and handles stalls, cancel and reset coherently.
- Pipeline valid, tag, result and exception state advance atomically.
- Exhaustive or formal functional evidence remains distinct from timing, power, fault and physical evidence.

### Common failures

Frequent failures are treating carry as signed overflow, exposing inverted borrow without documentation, extending after narrow addition, mixing signed and unsigned HDL expressions, shifting signed values with the wrong operator, negating the most-negative value as though it were representable, truncating multiplication before required carries settle, assuming `N`-bit operands always need only an `N`-bit product, mishandling division by zero or minimum-signed divided by minus one, losing remainder-sign rules, optimizing average carry length instead of worst-case timing, misaligning flags in a pipeline, and claiming random arithmetic tests prove all input combinations.

### Compact example

In eight bits, `120 + 20` produces bit pattern `10001100`, unsigned 140 and signed -116. There is no carry-out because 140 is below 256, but signed overflow is true because two positive operands produced a negative two's-complement result. Conversely, unsigned `200 + 100` produces 44 with carry-out 1, while signed operands -56 and 100 sum to 44 without signed overflow. Carry and overflow answer different questions.

### Connections

Integer arithmetic connects Boolean logic, register timing, ALUs, instruction-set flags, compiler overflow semantics, address generation, multipliers, cryptography, DSP, pipeline design, power, error detection and formal equivalence.

## Governing Question

Arithmetic looks mathematical, but hardware operates on finite bit vectors. The value `11111111` can mean unsigned 255 or signed -1. An addition circuit does not know which meaning software intends; the surrounding contract chooses extensions, comparisons and flags.

The governing question is how to preserve that contract while changing implementation. A ripple adder, prefix tree, hardened DSP block and iterative unit can compute the same bits with different latency, area, energy and verification obligations.

## Why This Matters

Integer units sit in datapaths for instruction execution, addresses, loop indexes, counters, sizes and security checks. One width error can turn a bounds check into an out-of-range access. One flag error can misdirect a branch.

Arithmetic is also a first encounter with architecture trade-offs. Faster carry computation uses more wiring and logic. A full multiplier consumes area; an iterative multiplier consumes cycles. Pipelining increases throughput while complicating stalls, tags and precise exceptions.

The ideal algebra is necessary but incomplete. HDL sizing and signedness, synthesis inference, target DSP resources, physical wire delay, voltage and process corners all determine whether the implemented unit fulfills the architectural promise.

## Prerequisites and Retrieval

Before studying this module, be able to:

- manipulate Boolean expressions and truth tables;
- interpret unsigned and two's-complement bit patterns;
- model synchronous state and finite-state controllers;
- distinguish combinational delay, latency and throughput;
- read basic HDL-width and array notation.

Retrieve operation set; operand, intermediate and result widths; signedness; carry/borrow convention; condition flags; wrap, saturation or trap behavior; multiply high/low requirements; division quotient and remainder rules; divide-by-zero behavior; exceptional signed operands; combinational, iterative or pipelined latency; issue rate; stalls, cancel and reset; clock and timing budget; target standard cells or DSP blocks; area, power and fault requirements; test vectors; formal properties; synthesis mapping; static timing; pipeline alignment; physical corners; and exact artifact identities.

## Learning Objectives

After completing this module, you should be able to:

1. derive half-adder and full-adder equations;
2. distinguish carry, borrow and signed overflow;
3. implement addition and subtraction with one adder structure;
4. reason about ripple, lookahead and parallel-prefix carries;
5. apply extension and truncation rules safely;
6. explain shift-add, Booth and reduction-tree multiplication;
7. compare combinational, iterative and pipelined arithmetic;
8. specify signed division and exceptional cases;
9. verify arithmetic across bit-vector, RTL, mapping and timing layers;
10. assess area, performance, power and fault trade-offs.

## Core Exposition

### Begin with bit-vector semantics

An `N`-bit wire carries one of `2^N` stable binary patterns in the two-valued model. Arithmetic operations map input patterns to output patterns of declared width.

Interpretation is external. Addition modulo `2^N` uses the same low result bits for unsigned and two's-complement operands. Comparisons, extensions and exception detection differ.

### Derive the half adder

For operand bits `a` and `b`, sum is `a XOR b` and carry is `a AND b`. The two outputs encode the integer sum `a+b` in two bits.

A half adder lacks carry-in, so it cannot directly compose every interior bit of a multi-bit addition.

### Derive the full adder

For `a`, `b` and carry-in `c`, sum is `a XOR b XOR c`. Carry-out is `(a AND b) OR (a AND c) OR (b AND c)`.

Equivalently, define generate `g=a AND b` and propagate `p=a XOR b`; then carry-out is `g OR (p AND c)`. State which propagate definition is used because some derivations use OR.

### Build ripple-carry addition

Chain each bit's carry-out into the next bit's carry-in. The structure is regular and compact. The worst-case carry dependency traverses every bit.

Delay grows approximately with width and cell/wire implementation. Average data patterns do not justify a shorter clock when the architectural unit must accept every pattern.

### Interpret carry-out

For unsigned addition, carry-out indicates that the exact nonnegative sum is at least `2^N`. Appending it yields the `N+1`-bit full unsigned sum.

For two's-complement addition, the final carry-out alone does not indicate signed overflow. It remains a useful bit for multiprecision arithmetic under an ISA-defined convention.

### Detect signed overflow

Adding same-sign operands overflows when the result sign differs. In bits, `overflow = NOT(sa XOR sb) AND (sa XOR sr)`.

An equivalent implementation XORs carry into and out of the sign bit. Verify the equivalence for the selected adder and width.

### Implement subtraction with complement and carry

Two's-complement subtraction computes `a + NOT(b) + 1`. A shared adder can XOR each `b` bit with a subtract control and use that control as carry-in.

This produces the low `N` bits for both unsigned and signed interpretation. Flags need operation-specific logic.

### Define borrow explicitly

For unsigned `a-b`, borrow is true when `a<b`. In complement addition, the final carry-out is commonly the inverse of borrow, but architectures vary in flag naming and subtraction forms.

Document whether the exposed bit is borrow, no-borrow carry, or an ISA flag with another convention. Test `0-0`, `0-1`, maximum values and chained multiprecision subtraction.

### Detect subtraction overflow

Signed subtraction overflows when operand signs differ and the result sign differs from the minuend: `(sa XOR sb) AND (sa XOR sr)`.

Examples include maximum positive minus -1 and minimum negative minus 1. Carry behavior does not replace this test.

### Generate condition flags

Zero is true when every result bit is zero. Negative commonly copies the sign bit under two's-complement interpretation. Carry and overflow follow the declared operation.

Flags are architectural state in some ISAs and transient compare results in others. Pipeline them with the exact operation and suppress them for squashed instructions.

### Compare wrap, saturation and trap

Wrapping arithmetic returns the modulo result. Saturating arithmetic clamps to the greatest or least representable value. Trapping arithmetic signals an exception instead of committing an out-of-range result.

The same circuit can calculate raw result and flags, then select policy. Do not silently substitute one semantic because a language, ISA or DSP convention differs.

### Widen before operating

To retain an unsigned addition's full result, zero-extend each operand to `N+1` before adding. For signed addition, sign-extend before adding into the wider result.

Computing at `N` bits and extending afterward cannot recover discarded carry or overflow information. HDL expression sizing can accidentally do exactly that.

### Extend values correctly

Zero extension preserves an unsigned value. Sign extension repeats the most significant bit and preserves a two's-complement value.

Extending a negative signed value with zeros changes it to a large positive value. Extending an unsigned high-bit-set value by sign extension changes its meaning.

### Treat truncation as a policy

Keeping low bits implements modulo `2^N`. Keeping high multiply bits approximates scaling or supports full-product instructions. Dropping low bits usually implies rounding or fixed-point semantics beyond plain integer arithmetic.

Record whether discarded bits feed sticky, rounding, overflow or inexact status. Plain truncation is not neutral.

### Understand signed HDL expressions

Literal widths, unsized constants, concatenation, casts and mixed signedness can change expression size and extension. Two visually similar expressions can synthesize different circuits.

Size and cast at boundaries. Use lint and reference models. Verify elaborated widths rather than relying on reader intuition.

### Accelerate carry computation

Group generate says a block produces carry regardless of input carry; group propagate says it passes input carry through. These summaries compose associatively.

Carry-lookahead computes groups hierarchically. Parallel-prefix families arrange generate/propagate combinations in trees, trading depth, fanout, wiring and node count.

### Compare prefix topologies

Kogge-Stone-like structures minimize logic depth and fanout at high wiring cost. Brent-Kung-like structures reduce wiring and prefix nodes with more depth. Other hybrids target physical constraints.

The best schematic gate count may route poorly. Compare post-layout delay, congestion, energy and variation on the target process.

### Handle carry-select and carry-skip

Carry-select computes alternatives for carry-in 0 and 1, then selects when the real carry arrives. It spends area to shorten dependence.

Carry-skip lets a carry bypass a propagating group. Group size balances local ripple and skip delay. Both are points in the implementation design space.

### Define multiplier width

The full unsigned product of `N`-bit and `M`-bit operands needs up to `N+M` bits. The same width holds the exact two's-complement product when operands are extended and partial products are formed correctly.

Low-half multiplication can discard high bits only after proving they cannot affect the low result. High-half signed and unsigned operations require different extension.

### Build shift-add multiplication

For each set multiplier bit `j`, add the multiplicand shifted by `j`. An array multiplier forms partial products in parallel; an iterative multiplier adds conditionally over cycles.

The iterative design reuses an adder and registers, reducing area and issue rate. State how zero operands, early exit, stalls and constant latency are handled.

### Reduce partial products efficiently

Adding partial products serially creates excessive depth. Carry-save compressors reduce several rows to two without propagating carry across the full width at each layer.

A final carry-propagate adder produces the binary result. Wallace- and Dadda-style schedules differ in reduction organization and physical trade-offs.

### Use Booth recoding carefully

Radix-2 or higher-radix Booth recoding represents runs of multiplier bits with signed multiples such as 0, +A, -A or shifted variants. This can reduce partial-product rows.

Sign extension, correction bits and the most-negative operand are common failure points. Verify every recoding digit and full-width sum independently.

### Map to hardened DSP blocks

FPGAs and some SoCs provide multiplier, accumulator, pre-adder and pipeline resources. Inference depends on HDL shape, widths, signedness and registers.

Inspect the mapped block and latency. A fallback into logic can change timing and power dramatically. Vendor-specific instantiation gives control and reduces portability.

### Divide by repeated shift and subtract

Restoring division shifts a partial remainder, subtracts the divisor and restores when negative under its representation. Non-restoring variants avoid immediate restoration by alternating correction behavior.

The quotient emerges over iterations. Controller state, counter width and remainder precision are part of correctness.

### Specify signed division

A common rule truncates quotient toward zero and gives remainder the dividend's sign, satisfying `a = q*b + r` and `abs(r)<abs(b)`. Other systems can choose different rounding.

Convert magnitudes carefully, compute unsigned division, then restore signs, or use a directly signed algorithm. The most-negative magnitude is not representable in the same signed width.

### Handle division exceptions

Division by zero needs an architectural result or trap. For two's complement, minimum signed divided by -1 has a mathematical positive result outside the same width.

Do not let algorithm control wander on these inputs. Detect them at admission and align exception timing with the instruction or request.

### Choose combinational or iterative implementation

A combinational unit returns within one cycle but may create a long path and large switching activity. An iterative unit saves area and consumes several cycles while holding internal ownership.

Variable early-out improves some latency and complicates timing predictability and side-channel behavior. Choose from workload and security requirements.

### Pipeline for throughput

Registers between reduction or prefix stages shorten the cycle and permit multiple operations in flight. Latency rises while initiation interval can approach one cycle.

Carry operand tags, signedness, operation kind and exception status through every stall and flush. A result with the wrong flag is incorrect even when its bits match another request.

### Account for physical costs

Area includes cells and routing. Delay includes logic, wires, fanout and clock overhead. Energy includes internal switching, glitches, clocked pipeline state and operand activity.

Operand isolation can suppress unused multiplier switching. Clock gating can stop inactive pipeline stages. Both need functional, timing and test verification.

### Consider arithmetic side channels

Variable latency, early termination and operand-dependent switching can reveal information. Constant-time instruction semantics do not guarantee constant physical power.

Define attacker observations and secret operands. Select constant-latency control or masking only with evidence appropriate to the threat model.

### Add fault detection where required

Parity prediction, residue codes, duplicated computation and temporal recomputation can detect selected arithmetic faults. Coverage depends on fault location and common-cause assumptions.

Define response to detected error and protect flags and control as well as data. Fault detection can itself alter timing and introduce shared logic.

### Verify exhaustively at small widths

For small `N`, enumerate every operand, carry-in and operation. Compare result and flags with an independent mathematical model.

Use reduced widths to expose boundary logic, then formal bit-vector equivalence or proof for production width. Random large-width tests alone leave astronomical input spaces unexplored.

### Verify algebraic properties cautiously

Addition modulo `2^N` is commutative and associative. Saturating addition may be commutative but is not generally associative. Signed overflow flags depend on grouping.

Properties must match the declared semantics. A mathematically attractive property can be false for finite-width policy.

### Verify implementation layers

Check RTL widths, signed casts and four-state behavior; prove or test reference equivalence; inspect synthesis mapping and DSP inference; run static timing at all corners; and validate pipeline control.

Post-layout and silicon evidence cover wires, glitches, voltage, temperature and faults absent from the bit-vector model. Preserve tools, constraints, seeds, counterexamples and waivers.

## Definitions and Notation

- `N`: declared operand or result width in bits.
- `mod 2^N`: wrap into the low `N` result bits.
- `cin`, `cout`: carry into and out of a bit or word.
- `p_i`, `g_i`: propagate and generate for bit `i` under the declared definition.
- `sa`, `sb`, `sr`: sign bits of operands `a`, `b` and result `r`.
- `V`: signed-overflow indication.
- `C`: carry or no-borrow indication under a declared ISA convention.
- `Z`: zero-result indication.
- `Nflag`: negative-result indication, distinct from width `N`.
- **full precision:** width sufficient to represent every exact result in the operand domain.
- **partial product:** shifted signed or unsigned contribution to a product.
- **carry-save form:** two rows whose ordinary sum represents several reduced operands.
- **initiation interval:** cycles between accepted independent operations.
- **latency:** cycles or time from accepted operands to architecturally valid result.
- **exception:** declared condition preventing or modifying normal result commitment.

## Mechanisms, Invariants, or Proof Structure

1. **Semantic claim:** define width, signedness, operation and exceptional behavior.
2. **Bit invariant:** low result bits equal the mathematical operation modulo `2^N` when wrapping.
3. **Flag invariant:** carry, borrow, overflow, zero and negative follow independent declared predicates.
4. **Extension invariant:** widen operands according to interpretation before information loss.
5. **Addition invariant:** each sum bit and carry satisfy the full-adder equation.
6. **Prefix invariant:** group generate/propagate composition yields the same carries as ripple.
7. **Product invariant:** partial products sum to the full exact product before truncation.
8. **Division invariant:** accepted result satisfies quotient/remainder identity and range rule.
9. **Exception invariant:** divide-by-zero and unrepresentable signed cases take explicit paths.
10. **Iteration invariant:** internal accumulator, operands and count describe completed steps exactly.
11. **Pipeline invariant:** data, operation, tag, validity and flags advance atomically.
12. **Mapping claim:** synthesized cells or DSP primitives preserve the interface and latency.
13. **Timing claim:** worst paths meet setup, hold and clock constraints at required corners.
14. **Evidence invariant:** separate exhaustive, formal, RTL, mapped, physical and fault claims.
15. **Change invariant:** revalidate after width, policy, pipeline, target or tool change.

## Alternatives and Trade-Offs

- **Ripple versus prefix addition:** ripple is compact and regular; prefix reduces carry depth and increases wiring.
- **Carry-lookahead versus carry-select:** lookahead shares logical summaries; carry-select duplicates alternatives for speed.
- **Wrap versus saturation:** wrap composes with modular arithmetic; saturation bounds signal magnitude and adds selection.
- **Flags versus traps:** flags defer policy to software; traps enforce exceptional control flow and cost recovery.
- **Narrow versus widened result:** narrow results save storage; wide results preserve carry or full product.
- **Array versus iterative multiplier:** arrays provide parallel throughput; iterative units reuse area over cycles.
- **Booth versus simple partial products:** Booth reduces rows; correction and signed recoding grow complexity.
- **Serial versus tree reduction:** serial accumulation is simple; compressor trees shorten depth and complicate routing.
- **Combinational versus iterative division:** combinational logic lowers cycle count; iterative division reduces area and raises latency.
- **Fixed versus variable latency:** fixed latency simplifies scheduling and side channels; early-out improves common cases.
- **Unpipelined versus pipelined:** unpipelined units minimize cycle latency; pipelines improve frequency and throughput.
- **Inference versus DSP instantiation:** inference is portable; instantiation controls mapping and latency.
- **High frequency versus low energy:** deeper trees and pipelines improve clock rate; wiring and clock power can rise.
- **Residue check versus duplication:** residue costs less with bounded coverage; duplication covers more logic and shares common causes.
- **Random testing versus formal equivalence:** random tests scale operationally; formal methods cover modeled bit-vector domains.

## Failure Modes and Misconceptions

1. **“Bits know whether they are signed.”** interpretation comes from the operation and surrounding type contract.
2. **“Carry-out is signed overflow.”** they describe different ranges.
3. **“No carry means no overflow.”** positive signed addition can overflow without carry.
4. **“Carry after subtraction always means borrow.”** many complement adders expose no-borrow carry.
5. **“Extending the narrow result preserves precision.”** lost high information cannot be recovered.
6. **“The sign bit should always be copied when widening.”** unsigned values require zero extension.
7. **“Unsized HDL constants are harmless.”** width and signedness can change the expression.
8. **“Right shift has one signed behavior.”** logical and arithmetic shifts differ.
9. **“Negating any signed value stays in range.”** the minimum negative value has no positive peer.
10. **“Ripple delay is average carry length.”** timing closure covers the worst permitted path.
11. **“A prefix tree is always fastest.”** routing and fanout can dominate.
12. **“An N-bit product fits in N bits.”** full precision can require 2N bits.
13. **“Low-product truncation permits narrow partial products.”** discarded carries can affect retained bits if done incorrectly.
14. **“Booth recoding changes the mathematical product.”** correct recoding changes representation, not value.
15. **“A DSP inference is guaranteed by using `*`.”** widths, signedness and registers affect mapping.
16. **“Division remainder is universal.”** sign and rounding conventions vary.
17. **“Only divide by zero is exceptional.”** minimum signed divided by -1 can overflow.
18. **“Iterative means one operation can never overlap.”** replicated or interleaved state can overlap transactions.
19. **“Pipelining reduces operation latency.”** it usually raises cycles while improving clock and throughput.
20. **“Flags can be recomputed from a truncated result.”** carry and overflow can require discarded information.
21. **“A flushed result can still update flags.”** validity governs every architectural side effect.
22. **“Saturating addition remains associative.”** clamping order can change the result.
23. **“Random tests cover arithmetic well enough.”** rare boundaries and huge domains remain.
24. **“Formal equivalence proves timing.”** it proves a modeled relation, not physical closure.
25. **“Constant cycle count eliminates side channels.”** switching and contention can remain operand-dependent.
26. **“Correct result bits prove the ALU.”** flags, latency, exceptions, power and faults are part of the contract.

## Worked Examples

### Example 1

Four-bit unsigned `15+1` returns 0 with carry 1. Interpreted signed, `-1+1` returns 0 without signed overflow.

### Example 2

Eight-bit `120+20` returns 140 unsigned or -116 signed. Carry is 0; signed overflow is 1.

### Example 3

Eight-bit `200+100` returns 44 with carry 1. Interpreted signed, -56 plus 100 equals 44 without overflow.

### Example 4

Unsigned `3-5` returns 254 modulo 256 with borrow. The complement-adder carry-out is 0 under the no-borrow convention.

### Example 5

Sign-extending eight-bit `0xF0` gives `0xFFF0`, preserving -16. Zero-extending gives 240, a different intended value.

### Example 6

Two eight-bit operands need sixteen result bits for every full product. Keeping eight low bits deliberately implements multiplication modulo 256.

### Example 7

A memory-bound FPGA design writes `a*b` but fails to infer a DSP because registers and operand widths do not match the target template. The mapping report, not syntax alone, resolves it.

### Example 8

An iterative divider is canceled while its remainder register contains partial state. Clearing validity before accepting new operands prevents results from transactions mixing.

### Example 9

A five-stage multiplier stalls its data registers but not its overflow flag. The bits and flag emerge with different tags; atomic pipeline control is required.

### Example 10

A constant-cycle multiplier still shows operand-dependent power. Cycle-level timing is one observation boundary, not a complete side-channel argument.

## Cross-Program Connections

- **Digital logic:** full adders and compressor cells are Boolean networks.
- **Sequential control:** iterative multiply and divide use registers, counters and FSMs.
- **Instruction sets:** widths, flags, traps and high/low results define software-visible semantics.
- **Compilers:** signed overflow, shifts and widening determine legal transformations.
- **Algorithms:** prefix scans and reduction trees organize associative carry information.
- **Pipelines:** arithmetic latency, bypass and exceptions affect instruction scheduling.
- **Cryptography:** multiprecision, modular arithmetic and side channels depend on exact behavior.
- **DSP:** saturation, fixed-width products and hardened blocks prioritize signal workloads.
- **Verification:** bit-vector solvers and equivalence checking can cover all modeled inputs.
- **Physical design:** wires, fanout, clocking, voltage and temperature determine achievable arithmetic.

## References

1. IEEE, [IEEE 1800-2023 — SystemVerilog](https://standards.ieee.org/ieee/1800/7743/), expression width, signedness, shifts, procedural semantics and verification; retrieved 2026-09-04.
2. Sarah L. Harris and David Money Harris, [Digital Design and Computer Architecture: RISC-V Edition Resources](https://pages.hmc.edu/harris/ddca/ddcarv.html), binary arithmetic, adders, ALUs, multipliers and processor datapaths; retrieved 2026-09-04.
3. RISC-V International, [RV32I Base Integer Instruction Set](https://docs.riscv.org/reference/isa/unpriv/rv32.html), fixed-width integer arithmetic, comparisons, shifts and architectural results; retrieved 2026-09-04.
4. RISC-V International, [M Extension for Integer Multiplication and Division](https://docs.riscv.org/reference/isa/unpriv/m-st-ext.html), low/high multiplication, signedness, division and remainder corner cases; retrieved 2026-09-04.
5. AMD, [UltraScale Architecture DSP Slice](https://docs.amd.com/r/en-US/ug579-ultrascale-dsp), hardened multiply, pre-add, ALU, cascade and pipeline resources; retrieved 2026-09-04.
6. Intel, [Variable-Precision DSP Blocks](https://www.intel.com/content/www/us/en/docs/programmable/683852/22-3/variable-precision-dsp-blocks.html), multiplier precision, accumulation, modes and FPGA mapping; retrieved 2026-09-04.
7. Neil H. E. Weste and David Money Harris, [CMOS VLSI Design: A Circuits and Systems Perspective](https://www.pearson.com/en-us/subject-catalog/p/cmos-vlsi-design-a-circuits-and-systems-perspective/P200000003427/9780321547743), adders, multipliers, arithmetic timing, power and physical design; retrieved 2026-09-04.

## Exercises

### Exercise 1

Derive full-adder sum and carry equations from all eight inputs. Show equivalence between majority-form carry and generate/propagate form.

### Exercise 2

For eight-bit additions `120+20` and `200+100`, and subtraction `3-5`, compute result bits, unsigned values, signed interpretations, carry, borrow and signed overflow.

### Exercise 3

Compare a 64-bit ripple, parallel-prefix and pipelined adder for an FPGA and an ASIC. Define evidence needed beyond gate depth.

### Exercise 4

Specify a signed 32-bit iterative divide unit. Cover identity, remainder rule, divide by zero, minimum divided by -1, latency, stall, cancellation and precise exception.

### Exercise 5

Construct an assurance plan for arithmetic used in a radiation-exposed flight controller. Include semantics, faults, detection, timing, tools, physical tests and named review.

## Answers to the Exercises

### Answer 1

Sum is 1 when an odd number of `a,b,cin` is 1, so `sum=a XOR b XOR cin`. Carry is 1 when at least two inputs are 1, giving `(a AND b) OR (a AND cin) OR (b AND cin)`. With `g=a AND b` and `p=a XOR b`, `g OR (p AND cin)` expands to `(a AND b) OR ((a XOR b) AND cin)`, which selects carry for the two single-one operand cases plus generated carry when both operands are one. Exhaustive comparison across eight rows proves equivalence in the two-valued model.

### Answer 2

For `120+20`, result is 140 or `0x8C`, carry 0. Signed inputs are both positive but the result sign is negative, so signed overflow is true and the wrapped signed interpretation is -116. For `200+100`, exact unsigned sum is 300, result `0x2C` or 44, carry 1. Signed interpretations are -56 and 100; their sum 44 is representable, so overflow is false. For unsigned `3-5`, result is `0xFE` or 254 with borrow 1 and complement-adder carry-out 0; signed 3 minus 5 is -2 without overflow.

<!-- bijux-verify: {"id":"fixed-width-arithmetic-flags","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"add 120 20 result=140 carry=0 signed_result=-116 overflow=true\nadd 200 100 result=44 carry=1 signed_result=44 overflow=false\nsub 3 5 result=254 borrow=1 signed_result=-2 overflow=false\n"}} -->
```python
WIDTH = 8
MASK = (1 << WIDTH) - 1
SIGN = 1 << (WIDTH - 1)


def signed(value):
    return value - (1 << WIDTH) if value & SIGN else value


def add(a, b):
    exact = a + b
    result = exact & MASK
    overflow = ((a ^ result) & (b ^ result) & SIGN) != 0
    print(
        f"add {a} {b} result={result} carry={exact >> WIDTH} "
        f"signed_result={signed(result)} overflow={str(overflow).lower()}"
    )


def subtract(a, b):
    result = (a - b) & MASK
    overflow = ((a ^ b) & (a ^ result) & SIGN) != 0
    print(
        f"sub {a} {b} result={result} borrow={int(a < b)} "
        f"signed_result={signed(result)} overflow={str(overflow).lower()}"
    )


add(120, 20)
add(200, 100)
subtract(3, 5)
```

The model assumes eight-bit input patterns and conventional two's-complement interpretation. It establishes the printed arithmetic only, not an HDL implementation, architectural flag convention or physical circuit.

### Answer 3

The ripple adder offers regular low-area logic but a long carry chain; an FPGA may provide dedicated carry hardware that makes it competitive. A prefix adder reduces logical carry depth but can route poorly, especially in programmable fabric. A pipelined adder shortens the cycle and raises throughput while adding latency, clock power and stall/flush state.

Synthesize each against the same target, constraints, operand arrival, fanout and placement conditions. Inspect inferred cells, dedicated carry use, routing congestion, setup/hold, clock uncertainty, area, dynamic and leakage power, operand activity, latency and initiation interval. Verify bit results and flags, pipeline alignment, stalls and flushes formally or exhaustively where possible. Compare post-layout corners and representative silicon rather than gate levels alone.

### Answer 4

On acceptance, capture dividend, divisor, request tag and signedness. Define quotient truncated toward zero and remainder with dividend sign so `a=q*b+r` and `abs(r)<abs(b)`. Detect divisor zero and minimum signed value divided by -1 before iteration; produce the ISA-defined results or precise exceptions without entering ordinary control.

For normal inputs, retain magnitudes in widened internal registers, iterate a declared number of steps, restore signs and return result, remainder, tag and exception atomically. Either hold internal state on stall or decouple response through a queue. Cancellation clears ownership only under a contract that prevents partial state from committing. Reset invalidates in-flight work. Assertions cover the identity, range, count, no mixed requests, exceptional paths and stable response under backpressure.

### Answer 5

Freeze widths, signedness, rounding/wrap/saturation, flags, deadlines and safe response. Prove bit-vector equivalence for every operation and modeled input, including extrema. Trace compiler and ISA semantics to RTL and mapped implementation. Analyze single-event upset and transient faults in operands, arithmetic cells, state, flags and control; choose residue, parity, duplication or temporal recomputation from quantified coverage and common-cause assumptions.

Inject covered faults and verify detection, containment and safe-state transition. Close timing across radiation-relevant voltage, temperature, aging and process conditions; assess clock and reset faults and recovery. Inspect synthesis transformations, hardened blocks, placement, routes and diagnostic coverage. Perform environmental, radiation and hardware-in-loop tests with representative control loads. Preserve source, tools, constraints, netlists, device lots, results, counterexamples and waivers. Named architecture, RTL, physical, radiation-effects, safety, flight-control, verification, manufacturing, operations and independent assurance authorities review their scopes; accountable certification authorities decide use. This module claims no certification.
