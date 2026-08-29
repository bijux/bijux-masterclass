---
module_id: SYSP-002
program: Programming Languages: Systems Programming
level: 1
module_number: 2
title: Integer Representation, Overflow, and Conversion
status: complete
last_verified: 2026-08-29
---

# Integer Representation, Overflow, and Conversion

## One-Page Review

### Governing question

How can a systems programmer determine which mathematical integer a finite bit pattern denotes, what happens when arithmetic leaves the destination range, and whether a conversion preserves the intended value?

### Essential definitions

- An **integer value** is a mathematical number; an **object representation** is the finite sequence of bits stored for a typed object.
- An unsigned \(w\)-bit interpretation maps bits \(b_{w-1}\ldots b_0\) to \(\sum_{i=0}^{w-1}b_i2^i\), with range \(0\) through \(2^w-1\).
- A two's-complement signed \(w\)-bit interpretation maps the same bits to \(-b_{w-1}2^{w-1}+\sum_{i=0}^{w-2}b_i2^i\), with range \(-2^{w-1}\) through \(2^{w-1}-1\).
- **Overflow** means that an exact mathematical result is outside the result type's representable range. A language may wrap, trap, saturate, diagnose, or leave behavior undefined.
- A **widening conversion** targets a type whose range contains every source value. A **narrowing conversion** lacks that guarantee.
- **Promotion** is a language-selected conversion before an operator. It can change the type in which overflow occurs.
- **Modulo reduction** maps \(x\) to the unique \(r\in[0,2^w)\) with \(r\equiv x\pmod{2^w}\).

### Central model, mechanism, or theorem

Reason in four explicit stages:

\[
\text{bits}\xrightarrow{I_T}\text{typed value}
\xrightarrow{\text{operation in }R}\text{mathematical result}
\xrightarrow{P_R}\text{language policy}
\xrightarrow{C_D}\text{destination value}.
\]

Never infer language semantics from hardware alone. For \(w\)-bit unsigned arithmetic, specified modular addition is \((x+y)\bmod 2^w\). For signed arithmetic, identical low bits do not imply identical language behavior. Conversion is value preservation only when the source value lies in the destination range or the specification defines another intended mapping.

### Critical invariants

- Width, signedness, language version, operator type, and conversion context must be known.
- A bit pattern has no unique numeric meaning without an interpretation.
- Intermediate expressions can overflow before assignment to a wider destination.
- Range checking must occur before a narrowing conversion, using a comparison that is itself type-safe.
- Modular arithmetic is not a substitute for checked size, count, offset, or allocation arithmetic.
- Binary formats require explicit width, signed interpretation, and byte order.
- Tests must cover both endpoints, one step beyond each endpoint, zero, and mixed-sign boundaries.

### Common failures

Common defects include assuming all languages copy C's rules, calling unsigned wrap “safe,” widening only after a narrow multiplication, comparing signed and unsigned values after an implicit conversion, using a cast as validation, negating the minimum signed value, shifting by the word width, decoding bytes in host order, and using a wrapped length for allocation.

### Compact example

In eight bits, the pattern `11111111` denotes \(255\) under unsigned interpretation and \(-1\) under two's complement. Adding one modulo \(2^8\) produces `00000000`. That explains unsigned wrap in a language that specifies it; it does not prove that signed addition is defined, checked, or desirable.

### Connections

Retrieve [SYSP-001's toolchain and ABI boundaries](001-from-source-text-to-process-image.md). This module prepares [SYSP-003's bitwise operations](../ROADMAP.md), binary parsing, memory sizing, and FFI work. It also connects to [Programming Languages & Semantics](../../01-programming-languages-and-semantics/ROADMAP.md), [Computer Architecture](../../23-computer-architecture/ROADMAP.md), and [Security Engineering](../../25-security-engineering/ROADMAP.md).

## Governing Question

What exactly happens between an intended integer calculation and the finite bits that a program stores or transmits?

The tempting answer—“the CPU does two's-complement arithmetic”—is incomplete. A processor executes finite-width instructions, but source-language semantics decide operand types, promotions, overflow consequences, and conversions. A compiler may prove that undefined behavior cannot occur and optimize accordingly. A managed language may specify low-bit wrap. A safety-oriented API may return an error. A file format may require an unsigned little-endian field even when the host variable is signed. Correct reasoning therefore crosses mathematics, representation, language rules, and application policy.

## Why This Matters

Integer mistakes are boundary mistakes with large consequences. A count multiplied by an element size can wrap to a small allocation, after which code writes the original number of elements. A negative value converted to an unsigned size can become enormous. A timestamp narrowed into an old protocol field can silently change identity. A sequence counter may intentionally wrap, yet naïve comparison fails around the rollover. These failures affect memory safety, authorization, financial totals, storage layout, and protocol interoperability.

The subject also disciplines performance reasoning. “The machine wraps anyway” does not license the programmer to depend on behavior the language does not guarantee. Conversely, inserting a branch after an overflowing operation is too late if the operation itself has undefined behavior or has already wrapped. Production code needs a chosen arithmetic policy—checked, wrapping, saturating, or proven in range—at every trust boundary.

## Prerequisites and Retrieval

You should know positional binary notation, powers of two, variables and static types, basic modular arithmetic, and the source-to-process pipeline from [SYSP-001](001-from-source-text-to-process-image.md). Retrieve these facts:

1. A mathematical value and its encoding are distinct.
2. A type supplies a domain of values and operations, not merely storage size.
3. An ABI and a serialized format are separate contracts.
4. A compiler may exploit language guarantees when transforming code.
5. Validation must precede any operation whose safety depends on the validated fact.

No assembly language is required. This module uses fixed-width abstract bit vectors and names language-specific behavior explicitly.

## Learning Objectives

After completing this module, you should be able to:

- derive unsigned and two's-complement values from a \(w\)-bit pattern;
- state the ranges of fixed-width signed and unsigned integer types;
- distinguish mathematical overflow, specified wrap, saturation, trapping, and undefined behavior;
- calculate modular results and identify when modular behavior is inappropriate;
- trace promotions, intermediate result types, and destination conversions;
- prove whether a conversion preserves a value by a range argument;
- design checked addition and multiplication guards without performing the dangerous operation first;
- specify integer fields at binary and foreign-function boundaries;
- construct endpoint and adversarial tests for integer code;
- explain why hardware observations alone do not establish source-language correctness.

## Core Exposition

A mathematical integer has unbounded magnitude. A machine representation has a fixed width. Let a bit vector have width \(w>0\), with \(b_0\) the least significant bit. Its unsigned value is

\[
U_w(b)=\sum_{i=0}^{w-1}b_i2^i.
\]

This is a bijection between all \(2^w\) bit patterns and the integers \([0,2^w-1]\). There is no negative unsigned value. The same patterns can instead be interpreted as two's-complement signed values:

\[
S_w(b)=-b_{w-1}2^{w-1}+\sum_{i=0}^{w-2}b_i2^i.
\]

The signed range is asymmetric: \([-2^{w-1},2^{w-1}-1]\). There is one more negative value than positive values, so \(-\min\) is not representable in the same type. For patterns whose top bit is zero, signed and unsigned values agree. When it is one, \(S_w(b)=U_w(b)-2^w\).

Representation is not byte order. Width and signed interpretation say what a bit vector means; endianness says how multi-byte units are ordered in memory or a byte stream. The 16-bit value `0x1234` can be serialized as bytes `12 34` in big-endian order or `34 12` in little-endian order while retaining the same mathematical value. A protocol must fix both field interpretation and byte order.

For exact mathematical addition, subtraction, or multiplication, compute in \(\mathbb Z\) first. Overflow occurs when the result lies outside the selected result type's range. This definition does not itself determine program behavior. Policy comes from the language, operator, build mode, library function, or application.

Common policies include:

- **checked arithmetic**, which returns a value-or-failure or raises a defined exception;
- **trapping arithmetic**, which stops the current computation on overflow;
- **wrapping arithmetic**, which reduces modulo \(2^w\);
- **saturating arithmetic**, which clamps below-minimum to minimum and above-maximum to maximum;
- **undefined behavior**, which imposes a source-level precondition and gives no result semantics after violation;
- **proof-obligated arithmetic**, where a preceding argument establishes that overflow cannot occur.

These are not quality rankings. Wrapping is correct for hash mixing and some sequence-number protocols. Saturation is useful in signal processing and bounded counters. Checked arithmetic is appropriate for hostile lengths and financial limits. Undefined signed overflow in C enables optimizations but creates a strict obligation on the program. The error is leaving the policy accidental.

Conversion begins with ranges. A conversion from source type \(A\) to destination type \(B\) is universally value-preserving exactly when \(Range(A)\subseteq Range(B)\), assuming both describe integers with ordinary numeric meaning. A conversion can still be safe for a particular \(x\) when \(x\in Range(B)\). That fact must be established before conversion.

“Wider” is ambiguous. A signed 32-bit type does not contain every unsigned 32-bit value. An unsigned 64-bit type does not contain negative signed values. Bit width alone cannot prove containment. Use explicit minimum and maximum bounds.

Languages also insert conversions. Integer promotions may cause two small operands to be added as `int`. Usual arithmetic conversions may convert a negative signed operand to unsigned before comparison. Assignment conversion occurs after the right-hand expression is evaluated, so assigning to a wider destination does not widen earlier arithmetic. In C-like pseudocode, `wide = narrow_a * narrow_b` can overflow in the narrow promoted type before conversion to `wide`. Convert or otherwise select the wider operation before multiplying, and prove that the wider result fits.

Current languages deliberately differ. ISO C 2024 specifies two's-complement representations for standard signed integer types, unsigned arithmetic modulo \(2^N\), conversions with detailed rules, and undefined behavior for many signed overflows. Java SE 26 defines fixed integral ranges, numeric promotion, wrapping integer arithmetic, and low-bit behavior for integer narrowing. Rust defines fixed-width types and explicit families such as `checked_*`, `wrapping_*`, `saturating_*`, and `overflowing_*`; ordinary overflow checks depend partly on compilation settings, while casts have specified mappings. A portable chapter must preserve those distinctions.

C's integer promotions illustrate why source spelling is insufficient. Types narrower than `int` generally promote to `int` when `int` can represent their entire range; otherwise an unsigned alternative may be selected. The usual arithmetic conversions then seek a common real type for binary operands. Rank and representable range, rather than a simplistic “signed wins” rule, determine whether a mixed pair is evaluated as signed or unsigned. Therefore a careful trace lists each operand's declared type, promoted type, common operator type, exact result, overflow policy, and final conversion. The trace is a small proof certificate for the expression.

Java removes several C portability dimensions by fixing `byte`, `short`, `int`, `long`, and `char` ranges, but it still demands operator tracing. Arithmetic on `byte` and `short` operands is normally promoted to `int`. An explicit narrowing conversion discards high bits according to the specification; it is deterministic, but determinism does not make lost information acceptable. Libraries such as `Math.addExact` express checked intent for supported types. A reviewer must distinguish the language's ordinary operator from the checked library operation.

Rust makes policies lexically visible when code chooses methods such as `checked_add` or `wrapping_add`. An `as` conversion follows specified numeric-cast rules, which may truncate or reinterpret low bits for integer-to-integer cases; `TryFrom` is the clearer value-preserving request when failure must be represented. Ordinary arithmetic and compiler overflow-check settings are a separate question from explicit wrapping methods. The engineering lesson is not to crown one language safest, but to select an operation whose contract matches the domain and remains visible to reviewers.

Several corner operations deserve their own review. Negating the signed minimum requests \(2^{w-1}\), which exceeds the signed maximum. Dividing that minimum by \(-1\) has the same exact result. A left shift can discard high bits or violate language-specific preconditions, and a shift distance equal to or greater than the width is not a portable route to zero. Absolute-value routines inherit the signed-minimum problem. Each language defines these cases separately, so a generic “ALU result” explanation is not enough.

Conversions across floating-point types introduce a different issue: precision. Even a destination with a larger maximum magnitude may be unable to represent every integer exactly because its significand is finite. This module focuses on integer-to-integer reasoning, but the general rule survives: range containment does not prove exactness when the destination's value set has gaps. At a mixed numeric boundary, document both range and precision obligations.

Counters that intentionally wrap require a protocol-level comparison rule. If an unsigned \(w\)-bit sequence number advances by less than half the space between observations, a design can compare modular distance rather than raw magnitude. That half-range premise is essential: without it, the same pair of bit patterns can describe either forward progress or an old value after multiple laps. Modular representation alone does not solve ordering.

Precondition checks should avoid the operation being guarded. For unsigned \(x+y\) with maximum \(M\), addition is safe iff \(x\le M-y\). For nonnegative \(x\cdot y\), handle zero, then require \(x\le\lfloor M/y\rfloor\). Signed multiplication needs sign-partitioned reasoning or a trusted checked primitive because dividing by \(-1\) near the signed minimum is itself exceptional in many systems.

Postcondition tests can be valid only where the language specifies wrapping and the relationship is proved. For example, for unsigned addition in C, `sum < x` detects wrap when adding nonnegative unsigned `y`. It is not a general signed-overflow detector. Prefer standard checked arithmetic APIs when available because they encode the policy and reduce proof surface.

At an external boundary, record five properties: width, signedness, byte order, admissible numeric range, and invalid-value policy. Decode raw bytes into a sufficiently capable intermediate, validate the domain range, then construct the domain type. Encoding reverses the proof. A field being physically 32 bits does not mean every one of its \(2^{32}\) patterns is a valid application value.

## Definitions and Notation

Let \(B_w=\{0,1\}^w\), \(M_u(w)=2^w-1\), \(m_s(w)=-2^{w-1}\), and \(M_s(w)=2^{w-1}-1\). Then:

\[
Range(U_w)=[0,M_u(w)],\qquad Range(S_w)=[m_s(w),M_s(w)].
\]

Define modulo normalization

\[
N_w(x)=x\bmod 2^w,
\]

where the result is chosen in \([0,2^w-1]\), including when \(x<0\). Define signed reinterpretation of low \(w\) bits:

\[
T_w(x)=
\begin{cases}
N_w(x),&N_w(x)<2^{w-1},\\
N_w(x)-2^w,&N_w(x)\ge2^{w-1}.
\end{cases}
\]

For destination range \([L,H]\), a checked conversion is the partial function

\[
C_{[L,H]}(x)=x\quad\text{iff}\quad L\le x\le H.
\]

Saturation is \(Sat_{[L,H]}(x)=\min(H,\max(L,x))\). It preserves order but not differences or invertibility outside the range.

Use \(E_T(e)\) for the exact mathematical result of expression \(e\) evaluated with result type \(T\), before its overflow policy. Use \(P_T\) for that policy. This notation keeps exact arithmetic separate from its representable program outcome.

## Mechanisms, Invariants, or Proof Structure

**Representation derivation.** For `11110110`, \(U_8=246\). Since the high bit is one, \(S_8=246-256=-10\). This equality follows from the definitions; it is not a rule that every untyped byte “really is” negative.

**Range proof.** Converting an unsigned 16-bit value to signed 32-bit preserves every value because \([0,65535]\subseteq[-2147483648,2147483647]\). Converting unsigned 32-bit to signed 32-bit lacks this proof because \(4294967295>2147483647\).

**Checked-add proof.** Given \(0\le x,y\le M\), if \(x\le M-y\), then adding \(y\) yields \(x+y\le M\). Conversely, if \(x>M-y\), then \(x+y>M\). The guard is necessary and sufficient, and subtraction \(M-y\) is representable under the premises.

**Checked-product proof.** For \(x,y\ge0\) and \(y>0\), \(xy\le M\) iff \(x\le\lfloor M/y\rfloor\). Zero is separated to avoid division by zero. This supports allocation checks such as `count <= SIZE_MAX / element_size` before multiplication.

**Intermediate-type invariant.** Every operator must be assigned its actual language result type before reasoning about range. Parentheses change grouping, not necessarily type. A cast after an operator cannot retroactively change its semantics.

**Boundary invariant.** For each numeric boundary \(L,H\), test \(L\), \(L+1\), \(-1\) when meaningful, \(0\), \(H-1\), \(H\), and rejected mathematical neighbors \(L-1,H+1\) in an adequately wide test representation.

The following executable model makes width and policy explicit. It verifies unsigned interpretation, signed reinterpretation, checked addition, wrapping addition, and checked conversion. It is a mathematical model, not a claim about any source language's implicit conversions or runtime configuration.

<!-- bijux-verify: {"id":"fixed-width-integer-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"bits=11110110 unsigned=246 signed=-10\nchecked_add_8(250,10)=overflow\nwrapping_add_8(250,10)=4\nchecked_i8(127)=127\nchecked_i8(128)=out_of_range\n","stderr":""}} -->
```python
def unsigned(bits):
    return int(bits, 2)

def signed_twos_complement(bits):
    width = len(bits)
    value = unsigned(bits)
    return value if value < (1 << (width - 1)) else value - (1 << width)

def checked_unsigned_add(left, right, width):
    maximum = (1 << width) - 1
    return left + right if left <= maximum - right else None

def wrapping_unsigned_add(left, right, width):
    return (left + right) % (1 << width)

def checked_signed(value, width):
    minimum = -(1 << (width - 1))
    maximum = (1 << (width - 1)) - 1
    return value if minimum <= value <= maximum else None

bits = "11110110"
print(f"bits={bits} unsigned={unsigned(bits)} signed={signed_twos_complement(bits)}")
checked_sum = checked_unsigned_add(250, 10, 8)
print("checked_add_8(250,10)=" + ("overflow" if checked_sum is None else str(checked_sum)))
print(f"wrapping_add_8(250,10)={wrapping_unsigned_add(250, 10, 8)}")
print(f"checked_i8(127)={checked_signed(127, 8)}")
checked_value = checked_signed(128, 8)
print("checked_i8(128)=" + ("out_of_range" if checked_value is None else str(checked_value)))
```

## Alternatives and Trade-Offs

**Checked versus wrapping.** Checked arithmetic makes failure explicit and protects sizes, balances, and bounds. It adds a branch or alternative result path. Wrapping is algebraically useful when the domain is \(\mathbb Z/2^w\mathbb Z\), but a wrapped result can become a dangerous small size.

**Trapping versus result-returning.** A trap centralizes failure and prevents continuation, which can suit assertions and safety profiles. A value-or-error lets callers recover but requires disciplined propagation. Both are clearer than accidental behavior.

**Saturating versus checked.** Saturation preserves boundedness and monotonicity, useful for media samples and telemetry counters. It hides magnitude beyond the boundary and is unsuitable when exactness or rejection matters.

**Implicit versus explicit conversion.** Implicit widening reduces noise. Implicit signedness changes and narrowing reduce auditability. Strong APIs use domain types, checked constructors, and explicit conversion at boundaries.

**Native-width versus fixed-width types.** Native-width types fit indexing and platform APIs. Fixed-width types fit protocols and persisted layouts. Converting between them still requires a range proof, especially when a 64-bit field enters a 32-bit process.

**Precondition versus wider intermediate.** A precondition check can avoid overflow without a wider type. A wider intermediate simplifies reasoning when a truly wider exact type exists, but the final range must still be checked. Arbitrary precision is excellent for validation tools, not automatically appropriate for every hot path or ABI.

**Manual guards versus standard primitives.** Manual guards expose the proof for teaching and unusual policies. Standard checked primitives are usually preferable in production because they handle signed corners and benefit from compiler support. Their exact guarantees remain language- and version-specific.

## Failure Modes and Misconceptions

1. **Bits have an intrinsic signed value.** Signedness is an interpretation supplied by a type or format.
2. **Two's complement makes signed overflow wrap in every language.** Representation and operator semantics are different contracts.
3. **Unsigned arithmetic cannot go wrong.** It may be defined modulo \(2^w\) and still violate the application invariant.
4. **The destination type controls the expression.** Operators are evaluated before assignment conversion.
5. **A cast makes a value fit.** A cast applies a mapping; it does not establish value preservation.
6. **More bits always means a superset.** Signedness matters; signed and unsigned ranges are not ordered by width alone.
7. **A post-operation check always detects overflow.** The operation may already be undefined, trapped, or transformed.
8. **Checking only the maximum is sufficient.** Negative underflow, minimum negation, and mixed-sign conversion remain.
9. **Host byte order is the file format.** Durable formats state an order independent of the current machine.
10. **Passing unit tests proves safety.** Boundary coverage and a proof of the actual language semantics are both required.

## Worked Examples

### Example 1

**Question:** Interpret `10010110` as both unsigned and eight-bit two's complement.

**Reasoning:** Unsigned, \(128+16+4+2=150\). The high bit is one, so signed interpretation is \(150-256=-106\). The stored pattern is unchanged.

**Conclusion:** One representation can denote different integers under different types.

### Example 2

**Question:** What are the ranges of 12-bit unsigned and signed two's-complement integers?

**Reasoning:** Unsigned uses \([0,2^{12}-1]=[0,4095]\). Signed uses \([-2^{11},2^{11}-1]=[-2048,2047]\).

**Conclusion:** Two's complement trades the upper half of the unsigned range for negative values and has an asymmetric signed range.

### Example 3

**Question:** Compute eight-bit wrapping addition \(250+10\) and contrast it with checked addition.

**Reasoning:** The exact result is \(260\), outside \([0,255]\). Modulo \(256\), \(260\bmod256=4\). A wrapping operator returns 4; a checked operator reports overflow without returning an ordinary sum.

**Conclusion:** The same operands and bits can support distinct intentional policies.

### Example 4

**Question:** Why can storing a product in a 64-bit variable still be too late?

**Reasoning:** Suppose `a` and `b` are 32-bit integers and the language evaluates `a * b` in 32 bits. The product overflows before assignment converts it to 64 bits. Selecting a 64-bit operand before multiplication changes the operator type; checking after a narrow multiplication does not.

**Conclusion:** Trace intermediate types, not just destination declarations.

### Example 5

**Question:** Is every unsigned 16-bit value safely convertible to signed 32-bit?

**Reasoning:** Source range \([0,65535]\) is contained in destination range \([-2147483648,2147483647]\). The range inclusion proves universal preservation.

**Conclusion:** Safe conversion is a set-containment fact, not a naming convention.

### Example 6

**Question:** Diagnose a signed/unsigned comparison in which `signed_count = -1` is compared with unsigned `limit = 10`.

**Reasoning:** In languages with C-style usual arithmetic conversions, the negative operand may convert to a large unsigned value before comparison. The source-looking proposition \(-1<10\) is no longer the evaluated proposition. A robust design rejects negative counts first and then converts under a proved range.

**Conclusion:** Implicit conversion can change the values being compared.

### Example 7

**Question:** Prove a safe allocation-size calculation for `count` elements of `size` bytes with maximum `SIZE_MAX`.

**Reasoning:** If `size == 0`, the product is zero under the chosen API policy. Otherwise require `count <= SIZE_MAX / size` before multiplication. By integer division, that condition is equivalent to `count * size <= SIZE_MAX` for nonnegative operands, without computing the risky product.

**Conclusion:** Guard multiplication with division under explicit nonnegative premises.

### Example 8

**Question:** Decode bytes `FE FF` as a signed 16-bit little-endian field.

**Reasoning:** Little-endian assembly gives unsigned `0xFFFE = 65534`. Signed two's-complement reinterpretation subtracts \(2^{16}\), giving \(-2\). Reading the same byte order as big-endian would produce `0xFEFF` and a different value.

**Conclusion:** Byte order is resolved before signed interpretation.

### Example 9

**Question:** A medical infusion controller receives a 32-bit unsigned dose count and multiplies by a unit volume. Is checked multiplication enough to approve delivery?

**Reasoning:** Checked multiplication proves only that the machine result fits. Safety also requires authenticated message origin, protocol byte-order validation, clinical range constraints, unit consistency, freshness, device-state checks, independent alarm behavior, and an approved hazard analysis. The example is a reasoning model only. No external academic, clinical, regulatory, or practitioner review is claimed. A named qualified human reviewer must evaluate the implementation, requirements trace, tests, and applicable medical-device process before use.

**Conclusion:** Arithmetic evidence is necessary but radically insufficient for a safety-critical actuation claim.

### Example 10

**Question:** When is saturating addition preferable to wrapping addition for a dropped-event counter?

**Reasoning:** If the counter communicates “at least this many events were dropped,” saturation at the maximum preserves that warning. Wrap can return to zero and falsely suggest no loss. If exact totals are required, neither policy suffices; use a wider or arbitrary-precision counter with explicit exhaustion handling.

**Conclusion:** Choose arithmetic policy from the domain meaning of boundary behavior.

## Cross-Program Connections

- [Programming Languages & Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) explains why undefined, implementation-defined, and specified behavior affect valid transformations.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) and [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) depend on safe indices, sizes, costs, and sentinel values.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) must preserve numeric domains through storage encoding and query evaluation.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) supplies the instructions, flags, and representations beneath language contracts.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) encounters rollover in sequence numbers, clocks, and protocol fields.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) treats attacker-controlled sizes and conversions as trust-boundary operations.

## References

1. ISO. [ISO/IEC 9899:2024, Information technology — Programming languages — C](https://www.iso.org/standard/82075.html), edition 5, published October 2024. Current C language authority consulted 2026-08-29; clauses 6.2.5, 6.3.1, and 6.5 govern integer types, conversions, and expressions.
2. Oracle. [The Java Language Specification, Java SE 26, Chapter 4: Types, Values, and Variables](https://docs.oracle.com/javase/specs/jls/se26/html/jls-4.html) and [Chapter 5: Conversions and Contexts](https://docs.oracle.com/javase/specs/jls/se26/html/jls-5.html). Consulted 2026-08-29.
3. The Rust Project. [The Rust Reference: Operator Expressions](https://doc.rust-lang.org/reference/expressions/operator-expr.html) and [Primitive integer types](https://doc.rust-lang.org/std/primitive.u32.html). Consulted 2026-08-29.
4. Software Engineering Institute. [CERT C INT30-C: Ensure that unsigned integer operations do not wrap](https://wiki.sei.cmu.edu/confluence/display/c/INT30-C.+Ensure+that+unsigned+integer+operations+do+not+wrap), updated for ISO/IEC 9899:2024 material; consulted 2026-08-29.
5. Software Engineering Institute. [CERT C INT31-C: Ensure that integer conversions do not result in lost or misinterpreted data](https://wiki.sei.cmu.edu/confluence/display/c/INT31-C.+Ensure+that+integer+conversions+do+not+result+in+lost+or+misinterpreted+data). Consulted 2026-08-29.
6. Bryant, Randal E., and David R. O'Hallaron. *Computer Systems: A Programmer's Perspective*, 3rd ed. Pearson, 2016. Chapters 2 and 7.
7. Warren, Henry S. *Hacker's Delight*, 2nd ed. Addison-Wesley, 2013. Chapters 2 and 4.

## Exercises

### Exercise 1

For width 10, state unsigned and two's-complement ranges. Interpret `1111111111` in both systems.

### Exercise 2

Derive the eight-bit results of exact, wrapping, saturating, and checked addition for \(200+100\).

### Exercise 3

A parser reads an untrusted unsigned 64-bit element count and needs a native allocation of `count * 24` bytes. Give a safe validation sequence for a platform whose allocation-size maximum is \(M\).

### Exercise 4

Compare wrapping and saturating policies for (a) a cryptographic mixing primitive and (b) a user-visible “failed login attempts” counter. State what neither policy proves.

### Exercise 5

Design the integer-boundary review for a railway braking message containing a signed 16-bit acceleration in millimetres per second squared and an unsigned 32-bit validity duration in milliseconds. Identify arithmetic checks and the evidence still requiring named human review.

## Answers to the Exercises

### Answer 1

Unsigned 10-bit range is \([0,2^{10}-1]=[0,1023]\). Signed two's-complement range is \([-2^9,2^9-1]=[-512,511]\). Pattern `1111111111` has unsigned value 1023. Its high bit is one, so its signed value is \(1023-1024=-1\).

### Answer 2

The exact mathematical result is 300, which is outside unsigned eight-bit range \([0,255]\). Wrapping returns \(300\bmod256=44\). Saturating addition returns 255. Checked addition reports overflow and supplies no ordinary sum. If signed eight-bit operands were intended, even the inputs 200 and 100 would already be unrepresentable; width and signedness are premises, not afterthoughts.

### Answer 3

First decode the field according to the protocol's fixed width and byte order into a representation that can hold all unsigned 64-bit values. Apply any protocol/domain maximum. Prove that the count fits the platform index type without narrowing it first. If 24 is nonzero, require `count <= M / 24`. Only then compute `bytes = count * 24` in the checked destination type. Also validate that the input contains the claimed elements and enforce process-level resource budgets. A cast, wrapped product, or post-allocation length check is insufficient.

### Answer 4

Cryptographic mixing commonly specifies arithmetic over fixed-width words, so wrapping may be part of the algorithm; saturation would destroy the intended algebra and test vectors. For a failed-login counter, saturation prevents rollover from making a very high count appear small, whereas wrapping is normally unsafe. Saturation still loses the exact count after the maximum, and neither policy proves concurrency correctness, persistence, authentication, resistance to reset, or that thresholds implement a sound security policy.

### Answer 5

The review fixes byte order, field widths, two's-complement interpretation for acceleration, and admissible protocol versions. It tests acceleration at \(-32768,-32767,-1,0,32766,32767\) plus rejected wider-domain neighbors, and duration at \(0,1,2^{32}-2,2^{32}-1\) plus policy limits. Every conversion to physical units uses checked or proven-wide arithmetic; duration-to-tick conversion checks multiplication before use. Semantic validation rejects clinically or mechanically impossible acceleration, stale/excessive duration, unit mismatch, replay, and inconsistent vehicle state.

This arithmetic review does not validate braking physics, timing guarantees, sensor integrity, network authenticity, fail-safe behavior, or applicable railway safety obligations. No external academic, railway, regulatory, or practitioner review is claimed. Before deployment, named qualified humans must review requirements, hazard analysis, formal and test evidence, implementation, integration behavior, and the applicable assurance process. A satisfactory answer separates numeric correctness from the broader safety case.
