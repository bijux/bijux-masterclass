---
module_id: ALGE-016
program: Algorithm Engineering
level: 1
module_number: 16
title: Counting, Radix, and Bucket Sorting
status: complete
last_verified: 2026-09-04
---

# Counting, Radix, and Bucket Sorting

## One-Page Review

### Governing question

When can explicit key structure replace general comparisons, and how should range size, stable distribution, digit encoding, bucket assumptions, memory, and hostile inputs be controlled so a near-linear sorting claim is actually valid?

### Essential definitions

- A **distribution sort** routes records to ordered positions or groups by information extracted directly from their keys.
- **Counting sort** uses one counter per key in a bounded discrete domain and prefix positions to scatter records.
- A **stable distribution pass** preserves input order among records assigned the same distribution key.
- A **radix** $b$ is the number of possible values of one processed digit.
- **LSD radix sort** processes digits from least significant to most significant using stable passes.
- **MSD radix sort** distributes by the most significant remaining digit and recursively sorts each resulting group.
- **Bucket sort** maps keys monotonically into ordered buckets, sorts within buckets, and concatenates them.
- A **key encoding** maps semantic order to a sequence of machine digits; signedness, width, exceptional values, and endianness are part of that mapping.
- A **distribution assumption** is a probabilistic claim about bucket occupancy, not a property guaranteed by the algorithm.

### Central model, mechanism, or theorem

For integer keys in $[L,U]$, define

$$
k=U-L+1,\qquad \operatorname{slot}(x)=x-L.
$$

A stable counting sort uses exclusive starts

$$
s_j=\sum_{q=0}^{j-1}c_q
$$

and runs in

$$
\Theta(n+k)
$$

time with $\Theta(n+k)$ auxiliary record-and-counter space in the standard stable implementation.

For $d$ digits of radix $b$, stable LSD radix sort runs in

$$
\Theta\bigl(d(n+b)\bigr).
$$

If a $W$-bit key is processed $r$ bits per digit, then $b=2^r$ and $d=\lceil W/r\rceil$. The choice trades passes against counter space and initialization/cache costs.

For bucket occupancies $n_0,\ldots,n_{B-1}$ and quadratic inner sorting,

$$
T=\Theta\left(n+B+\sum_{j=0}^{B-1}n_j^2\right).
$$

Under independent uniform assignment to $B$ buckets,

$$
\mathbb E\left[\sum_j n_j^2\right]
=n+\frac{n(n-1)}{B}.
$$

This is expected linear when $B=\Theta(n)$, but the worst case remains quadratic if a large fraction of records enters one bucket.

### Critical invariants

- The key domain and its encoded order must be explicit before indexing counters or extracting digits.
- Compute $k=U-L+1$ and $x-L$ without fixed-width overflow.
- Counts are nonnegative, fit their counter type, and sum to $n$.
- Exclusive prefix starts partition the output into disjoint, exhaustive key regions.
- Stable scatter scans input in original order and advances a private next position for each key.
- Every LSD digit pass must be stable; after $t$ passes, records are ordered by the $t$ processed least-significant digits.
- The complete digit sequence must preserve the intended semantic order, including signed values and exceptional cases.
- Bucket indices stay in $[0,B)$, and lower-index buckets contain no key greater than a key in a higher-index bucket.
- Each bucket is completely sorted before ordered concatenation.
- Expected bucket bounds state independence and distribution assumptions; deterministic fallback limits remain separate.
- Memory initialization, output buffers, key materialization, and counters belong in the cost model.

### Common failures

Common failures include allocating a counter array for a sparse 64-bit range; overflowing $U-L+1$ or $x-L$; confusing frequencies, inclusive ends, and exclusive starts; scanning backward with a forward-scatter formula; dropping record identities by reconstructing only keys; using an unstable digit pass in LSD radix; stopping before the highest distinguishing digit; sorting signed bit patterns as unsigned; mixing byte significance with storage endianness; treating variable-length strings as zero-padded without defining semantics; mapping the upper endpoint to bucket $B$; allowing NaN into a numeric bucket formula; assuming uniform occupancy from a convenient sample; and calling a conditional expected bound simply “linear time.”

### Compact example

Stable counting sort on records $((2,A),(0,B),(2,C),(1,D),(0,E))$ has counts $(2,1,2)$ and starts $(0,2,3)$. Forward scatter yields

$$
((0,B),(0,E),(1,D),(2,A),(2,C)).
$$

Both pairs of equal-key identities retain input order. The same stable mechanism can serve as one digit pass inside LSD radix sort.

### Connections

[ALGE-006](./006-best-worst-expected-and-amortized-cost.md) separates conditional expected claims from worst-case guarantees; [ALGE-008](./008-lower-bounds-and-adversary-arguments.md) states the comparison-model boundary; [ALGE-012](./012-insertion-selection-and-shell-sorting.md) defines order, identity, and stability; [ALGE-013](./013-merge-sort.md) supplies a stable comparison baseline; and ALGE-019 will combine workload evidence and safe fallbacks.

## Governing Question

How should counting, digit, and bucket mechanisms be derived from key semantics so their correctness, stability, resource use, and conditional performance remain valid from a classroom trace to a hostile production workload?

These algorithms are often summarized as “linear sorts.” That phrase hides the variables that make the result true. Counting sort is linear in records plus representable range, not merely records. Radix sort is linear in records per digit, not independently of key width and radix. Bucket sort is expected linear only under an occupancy model and a suitable inner sorter.

The durable approach is to start from the semantic ordering, design an order-preserving encoding or bucket map, state a stable distribution contract, and account for every counter, output position, pass, byte, and skewed group.

## Why This Matters

The $\Omega(n\log n)$ decision-tree lower bound applies when order is learned only through comparisons. Integer slots, digits, and monotone bucket maps expose more structure per operation, so distribution algorithms do not contradict that theorem. Their speed comes from stronger input and machine assumptions.

Those assumptions are powerful and dangerous. A four-billion-slot histogram is not practical merely because the input contains integers. A bytewise pass that ignores signed order can be consistently wrong. An apparently uniform production stream can become concentrated after a tenant, clock, prefix, or adversary changes. A stable counting kernel can preserve database tie order; a single unstable optimization can silently destroy it across radix passes.

These methods also reveal operational trade-offs that asymptotic notation compresses: zeroing large count arrays, allocating output buffers, moving wide records repeatedly, handling counters that exceed 32 bits, parallelizing histograms without contention, and recovering from allocation or key-extraction failure.

## Prerequisites and Retrieval

Retrieve:

- sorting order, identity permutation, stability, key projections, and total orders;
- integer intervals, modular arithmetic, floors, ceilings, and fixed-width overflow;
- prefix sums, histograms, cumulative counts, and disjoint array ranges;
- positional numeral systems, bit fields, signed representations, and endianness;
- expectation, indicator variables, independence, and balls-into-bins occupancy;
- insertion and merge sorting contracts and costs;
- memory allocation, cache capacity, counters, cancellation, and failure ownership.

You should be able to distinguish a semantic key from its machine representation, derive an exclusive prefix sum, and state which random experiment an expectation ranges over.

## Learning Objectives

After completing this module, you should be able to:

1. derive stable counting sort from frequency and exclusive-prefix invariants;
2. prove its ordered, permutation, and stability postconditions;
3. determine when range size makes counting sort practical or unsafe;
4. prove LSD radix sort by induction over stable digit passes;
5. choose radix width from pass, counter-memory, initialization, and cache costs;
6. encode unsigned, signed, fixed-width, and variable-length keys without changing semantic order;
7. prove bucket concatenation correct from a monotone range map and local sorting;
8. derive expected bucket work and separate it from quadratic worst-case skew;
9. design overflow, allocation, callback, cancellation, and fallback policies;
10. validate distribution algorithms with structural, finite, adversarial, and physical evidence.

## Core Exposition

### State the sorting and key-access contracts

Let $A[0:n)$ contain records with semantic keys under a declared total preorder or total order. Successful sorting requires:

$$
\forall i\in[0,n-1),\qquad \operatorname{key}(A[i])\le\operatorname{key}(A[i+1]),
$$

and identity permutation. If stability is promised, equal-key records retain their original relative order.

A distribution algorithm additionally needs an order-revealing operation: a bounded integer slot, a digit function, or a bucket map. That operation must be defined for every accepted key and agree with semantic order. Raw object hashes do not qualify; equal or ordered keys can hash to unrelated positions.

Key extraction may itself be costly, stateful, allocating, or fallible. Materialize immutable keys when the contract and memory allow, or require that repeated extraction returns the same result. Correct distribution over inconsistent keys is impossible.

### Derive stable counting sort

Assume every integer key lies in inclusive range $[L,U]$. Let

$$
k=U-L+1
$$

and map key $x$ to zero-based slot $j=x-L$.

The standard stable algorithm has three logical stages:

1. **Frequency:** initialize $c[0:k)$ to zero and increment $c[x-L]$ for every input record.
2. **Positions:** compute the exclusive start of each key block,

   $$
   s_0=0,\qquad s_j=\sum_{q=0}^{j-1}c_q.
   $$

   Copy starts into mutable next positions $p_j=s_j$.
3. **Scatter:** scan input left to right, write each record of slot $j$ to $B[p_j]$, then increment $p_j$.

The output block for slot $j$ is exactly

$$
B[s_j:s_j+c_j).
$$

The blocks are disjoint, adjacent, and cover $B[0:n)$ because counts are nonnegative and $\sum_jc_j=n$.

### Prove counting order, permutation, and stability

Every input record is written exactly once. Each next pointer begins at its block start and advances exactly $c_j$ times, so no output position is skipped or overwritten by another key. This establishes identity permutation.

If $j<q$, then every semantic key in slot $j$ is below every key in slot $q$, and the entire $j$ block precedes the $q$ block. Therefore concatenated blocks are ordered.

For equal-key records $a$ then $b$ in input order, the forward scatter processes $a$ first and assigns the earlier next position in their shared block. Thus $a$ precedes $b$ in output. Stability follows.

Another correct formulation stores inclusive cumulative ends and scans input right to left while decrementing positions. Mixing that scan direction with exclusive starts is a common bug. Name the position convention instead of copying isolated formulas.

### Account for counting-sort resources honestly

Frequency, prefix, and scatter work is

$$
\Theta(k)+\Theta(n)+\Theta(k)+\Theta(n)=\Theta(n+k).
$$

The conventional stable record sort uses an output array of $n$ records or references plus $\Theta(k)$ counters/positions. If only bare integer values are needed, counts can reconstruct keys without an $n$-record output, but that mechanism cannot preserve attached record identities.

Before allocation, validate:

- $L\le U$;
- $U-L+1$ is representable;
- every $x-L$ is representable and in range;
- each count and the prefix total can represent $n$;
- $k$ counters plus output fit memory and policy limits.

For one million records whose keys may be any unsigned 32-bit value, an eight-byte counter per possible key requires

$$
2^{32}\cdot8=2^{35}\text{ bytes}=32\text{ GiB}
$$

before output storage. A sparse map avoids empty counters but introduces ordering and lookup costs; comparison or radix sorting may be the durable choice.

### Derive LSD radix correctness from stability

Represent each accepted key by exactly $d$ radix-$b$ digits:

$$
(a_{d-1},\ldots,a_1,a_0),
\qquad 0\le a_t<b,
$$

where $a_0$ is least significant and lexicographic digit order agrees with semantic key order.

Perform a stable distribution sort by $a_0$, then $a_1$, through $a_{d-1}$. Maintain:

> After completing pass $t$, records are ordered by the processed tuple $(a_t,a_{t-1},\ldots,a_0)$, and semantically equal complete keys remain stable.

The base case is one stable sort by $a_0$. For the inductive step, the stable pass orders different $a_t$ values. Among records with equal $a_t$, it preserves their previous order by lower processed digits. Therefore the longer tuple is ordered.

After pass $d-1$, the tuple is the complete key encoding, so semantic keys are ordered. If any pass is unstable, equal current digits can scramble the lower-digit order established earlier and the induction fails.

### Choose a radix from the complete resource equation

For a $W$-bit key and $r$-bit digits,

$$
b=2^r,\qquad d=\left\lceil\frac Wr\right\rceil,
$$

so a counting-based implementation has model

$$
T(r)=\Theta\left(
\left\lceil\frac Wr\right\rceil
(n+2^r)
\right).
$$

A larger digit reduces passes but enlarges counts, prefix work, and often cache pressure. For $W=32$ and $n=10^6$:

- $r=8$ gives four passes and work proxy $4(10^6+256)=4{,}001{,}024$;
- $r=16$ gives two passes and proxy $2(10^6+65{,}536)=2{,}131{,}072$.

The second proxy is smaller, but its counters occupy 256 times as many slots. Physical choice also depends on counter width, clearing technique, parallel shards, output traffic, cache, and digit extraction cost. Measure instead of treating the arithmetic proxy as elapsed time.

### Encode signed and exceptional keys deliberately

Applying unsigned radix order directly to a signed two's-complement bit pattern puts nonnegative values before negative ones. For a guaranteed $W$-bit two's-complement encoding, transform bits with

$$
u(x)=\operatorname{bits}(x)\mathbin{\operatorname{xor}}2^{W-1}.
$$

This flips the sign bit: the most negative value maps to $0$, $-1$ maps immediately below the transformed $0$, and the greatest positive value maps to $2^W-1$. Unsigned digit order of $u(x)$ then matches signed numeric order.

Biasing by the minimum key can also work mathematically, but $x-L$ may overflow in the source signed type before conversion. Use a widened or unsigned checked representation. Separating negative and nonnegative groups requires careful reversal and stability for negative magnitudes; it is not automatically simpler.

Floating-point keys require a declared total-order encoding for negative zero, infinities, and NaNs. Text requires a declared normalization, collation, code-unit or code-point model, and treatment of prefixes. Distribution on raw bytes is correct only if byte lexicographic order is the intended semantic order.

### Keep digit significance separate from storage endianness

Digit significance is mathematical: pass $0$ processes the least significant digit of the key encoding. Storage endianness tells where bytes reside in memory. An implementation may read byte positions differently on different machines while still process significance in the same order.

Define digit extraction numerically, for example

$$
a_t(x)=\left\lfloor\frac{x}{b^t}\right\rfloor\bmod b,
$$

or define a portable bit extraction from a normalized unsigned representation. Do not walk object memory and assume its first byte has a universal significance.

Fixed-width strings fit an LSD proof when every position has the same declared alphabet. Variable-length lexicographic strings need an explicit prefix/sentinel rule. MSD recursion commonly handles them naturally by treating end-of-string as a distinguished digit ordered before continuing characters.

### Contrast LSD and MSD distribution

LSD sorting makes full passes over all records and relies on stable lower-digit history. It is attractive for fixed-width integers and records when an auxiliary array is acceptable.

MSD sorting distributes first by the highest significant digit, then recursively processes each nontrivial bucket's next digit. Its correctness follows because distinct high-digit buckets are already globally ordered; recursion only refines equal-prefix groups. It can avoid inspecting long suffixes after early differences, especially for variable-length strings.

MSD implementations must control:

- recursion or explicit-worklist depth;
- empty and singleton buckets;
- end-of-key sentinel order;
- many tiny buckets and cutoff overhead;
- skewed prefixes;
- stable versus in-place distribution;
- repeated count-array initialization.

American-flag-style cycle distribution can reduce the $n$-record output buffer but is typically unstable and has more intricate permutation invariants. Space claims must not erase that semantic trade-off.

### Derive bucket-sort correctness

Choose $B>0$ and a total bucket function

$$
g:K\to\{0,\ldots,B-1\}
$$

that is monotone with semantic key order. Distribute every record to its bucket, completely sort each bucket, and concatenate buckets from $0$ through $B-1$.

Within a bucket, the local sorter establishes order. If a record $x$ is in a lower bucket than $y$, monotonic interval construction ensures $\operatorname{key}(x)\le\operatorname{key}(y)$. Thus every cross-bucket pair is ordered, and concatenation is globally ordered. Identity permutation follows if distribution, local sorting, and concatenation neither duplicate nor drop records.

Stability requires stable bucket insertion, a stable inner sort, and ordered concatenation. Bucket sorting is not stable merely because buckets themselves are ordered.

For real $x\in[0,1)$, a conventional map is

$$
g(x)=\lfloor Bx\rfloor.
$$

If $x=1$ is accepted, that formula yields invalid index $B$; either use a half-open domain or define and test a clamp/endpoint policy. General interpolation must address $a=b$, overflow in $x-a$, floating rounding, infinities, and NaN.

### Derive expected bucket work without hiding skew

Let $n_j$ be occupancy of bucket $j$ and use insertion sort inside each bucket. Distribution and concatenation cost $\Theta(n+B)$; inner work is bounded by $\Theta(\sum_j n_j^2)$.

Write

$$
\sum_j n_j^2
$$

as the number of ordered record pairs, including self-pairs, that land together. There are $n$ self-pairs. Under independent uniform assignment, each of the $n(n-1)$ distinct ordered pairs shares a bucket with probability $1/B$. Therefore

$$
\mathbb E\left[\sum_jn_j^2\right]
=n+\frac{n(n-1)}B.
$$

With $B=n$, this is $2n-1$, so expected total work is $\Theta(n)$. But if all records land in one bucket, $\sum_j n_j^2=n^2$. Uniformity, independence, correct interpolation, and a bounded-cost inner sorter are assumptions, not observations guaranteed to persist.

A deterministic $O(n\log n)$ inner sort caps the all-in-one-bucket case at $O(n\log n)$ while retaining distribution overhead. Occupancy thresholds can trigger such a fallback before quadratic insertion work develops.

### Preserve executable distribution evidence

The following stable counting kernel serves both a whole-key counting sort and each decimal LSD pass. It records frequencies, exclusive starts, digit snapshots, and equal-key identities.

<!-- bijux-verify: {"id":"stable-distribution-ledger","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"counting_input=((2, 'A'), (0, 'B'), (2, 'C'), (1, 'D'), (0, 'E'))\ncounts=(2, 1, 2) starts=(0, 2, 3)\ncounting_output=((0, 'B'), (0, 'E'), (1, 'D'), (2, 'A'), (2, 'C'))\nradix_input=((170, 'A'), (45, 'B'), (75, 'C'), (90, 'D'), (802, 'E'), (24, 'F'), (2, 'G'), (66, 'H'), (45, 'I'))\nones=(170, 90, 802, 2, 24, 45, 75, 45, 66)\ntens=(802, 2, 24, 45, 45, 66, 170, 75, 90)\nhundreds=(2, 24, 45, 45, 66, 75, 90, 170, 802)\nradix_output=((2, 'G'), (24, 'F'), (45, 'B'), (45, 'I'), (66, 'H'), (75, 'C'), (90, 'D'), (170, 'A'), (802, 'E'))\n","stderr":""}} -->
~~~python
def stable_counting(records, key_count, key):
    counts = [0] * key_count
    for record in records:
        counts[key(record)] += 1

    starts = [0] * key_count
    for value in range(1, key_count):
        starts[value] = starts[value - 1] + counts[value - 1]

    next_slot = starts.copy()
    output = [None] * len(records)
    for record in records:
        value = key(record)
        output[next_slot[value]] = record
        next_slot[value] += 1

    return tuple(output), tuple(counts), tuple(starts)


counting_input = ((2, "A"), (0, "B"), (2, "C"), (1, "D"), (0, "E"))
counted, counts, starts = stable_counting(
    counting_input,
    3,
    lambda record: record[0],
)
print(f"counting_input={counting_input}")
print(f"counts={counts} starts={starts}")
print(f"counting_output={counted}")

radix_input = (
    (170, "A"),
    (45, "B"),
    (75, "C"),
    (90, "D"),
    (802, "E"),
    (24, "F"),
    (2, "G"),
    (66, "H"),
    (45, "I"),
)
items = radix_input
snapshots = []
place = 1
for _ in range(3):
    items, _, _ = stable_counting(
        items,
        10,
        lambda record, current=place: (record[0] // current) % 10,
    )
    snapshots.append(tuple(record[0] for record in items))
    place *= 10

print(f"radix_input={radix_input}")
print(f"ones={snapshots[0]}")
print(f"tens={snapshots[1]}")
print(f"hundreds={snapshots[2]}")
print(f"radix_output={items}")
~~~

The run establishes one finite stable trace. It does not establish that decimal radix is optimal, that arbitrary signed values share this encoding, or that allocation and callbacks cannot fail.

### Engineer failure, parallelism, and evaluation

Validate the entire domain before mutating input when practical. Allocate counts and output under explicit memory limits. If allocation fails, return before publishing partial output or switch only to a fallback promised by the API. Checked prefix sums must end at exactly $n$.

Parallel counting can build one histogram per worker and reduce them, avoiding hot shared increments. Stable parallel scatter then needs per-worker offsets within each global key block so worker order and local input order compose correctly. Atomic counter increments alone do not define stable placement.

Cancellation checkpoints belong between bounded scans, prefix ranges, digit passes, or bucket groups. A double-buffered radix sort must define which buffer owns the latest complete pass; a failure mid-pass should not make an incomplete destination appear valid.

Evaluate:

- range $k$, digit width $r$, radix $b$, pass count $d$, and bucket count $B$;
- counter/output bytes, initialization bytes, key bytes, and peak resident memory;
- key extractions, digit operations, scatter writes, record bytes moved, and copy-back passes;
- occupancy maximum, variance, percentiles, and fallback counts;
- stable identity order, not only key order;
- cache misses, bandwidth, contention, allocation failures, cancellation latency, and tail time.

Use empty, singleton, all-equal, dense range, sparse extremes, signed boundaries, maximum key width, long common prefixes, variable lengths, NaN policy cases, uniform data, clustered data, one-bucket skew, and adversarial tenants. Preserve raw occupancy histograms and compare against stable merge, comparison hybrids, and relevant library baselines.

## Definitions and Notation

- $n$ is the number of input records.
- $[L,U]$ is an accepted inclusive integer-key range.
- $k=U-L+1$ is the number of integer slots.
- $c_j$ is the frequency in slot or digit $j$.
- $s_j=\sum_{q<j}c_q$ is an exclusive output-block start.
- $p_j$ is the next free output position in block $j$.
- $b$ is radix and $d$ is the number of processed digits.
- $W$ is key width in bits and $r$ is digit width in bits.
- $a_t(x)$ is digit $t$, with $t=0$ least significant for LSD sorting.
- $B$ is the number of buckets.
- $g(x)$ is the bucket index for key $x$.
- $n_j$ is occupancy of bucket $j$.
- Stability preserves relative identity order among records equal under the declared semantic key.
- A distribution assumption defines the probability space used for an expected occupancy result.
- Auxiliary space includes counters, positions, output buffers, materialized keys, worker histograms, and recursion/worklists.

## Mechanisms, Invariants, or Proof Structure

Use this sequence to review a distribution sort:

1. State semantic order, equality, identity, and stability requirements.
2. Define the accepted key domain and reject or normalize exceptional values.
3. Prove slot, digit sequence, or bucket map agrees with semantic order.
4. Check all range, offset, digit, and prefix arithmetic for overflow.
5. Account for counter width, initialization, output, keys, and peak memory.
6. For counting, prove counts sum to $n$ and exclusive blocks partition output.
7. Prove scatter writes every record once without collision or omission.
8. Prove equal-key input order maps to increasing positions.
9. For LSD, state the processed-suffix induction and require every pass to be stable.
10. For MSD, state prefix-bucket order, sentinel policy, and recursive progress.
11. For buckets, prove cross-bucket order and complete local order.
12. State the precise probability model before deriving expected occupancy work.
13. Bound worst-case skew or specify a deterministic threshold/fallback.
14. Define allocation, callback, cancellation, double-buffer, and partial-publication semantics.
15. Reproduce finite ledgers and test dense, sparse, signed, skewed, and hostile families.

The central correctness compositions are:

$$
\text{counts}
\Longrightarrow
\text{disjoint blocks}
\Longrightarrow
\text{stable ordered scatter},
$$

$$
\text{stable lower digits}
\Longrightarrow
\text{stable next digit}
\Longrightarrow
\text{complete encoded order},
$$

and

$$
\text{ordered bucket ranges}
\land
\text{locally sorted buckets}
\Longrightarrow
\text{globally sorted concatenation}.
$$

## Alternatives and Trade-Offs

| Approach | Time model | Typical extra storage | Stable by default | Principal condition |
|---|---:|---:|---:|---|
| Stable counting sort | $\Theta(n+k)$ | $\Theta(n+k)$ | Yes | Dense manageable integer domain |
| LSD radix with counting passes | $\Theta(d(n+b))$ | $\Theta(n+b)$ | Yes | Fixed order-preserving digits |
| MSD radix | Input/prefix dependent | Output plus recursion/counts | Policy dependent | Useful leading digits and sentinel |
| In-place cycle distribution | Near $\Theta(n+k)$ per level | $\Theta(k)$ | Usually no | Complex permutation acceptable |
| Bucket plus insertion | Expected $\Theta(n)$ under model | $\Theta(n+B)$ | Can be | Controlled occupancy distribution |
| Bucket plus $O(m\log m)$ inner sort | $O(n\log n+n+B)$ | Inner-sort dependent | Policy dependent | Worst-case skew must be capped |
| Stable merge sort | $O(n\log n)$ | Usually $\Theta(n)$ | Yes | General comparable keys |
| Introspective comparison sort | $O(n\log n)$ | Usually stack | No | General order and tight fallback |

Use counting when the range is dense enough that $k$ is an acceptable input parameter. Use LSD radix when a fixed, order-preserving encoding and repeated output scans fit memory bandwidth. Use MSD when high-order prefixes separate records early. Use buckets when a defensible range map controls occupancy, and retain a skew-safe inner strategy.

## Failure Modes and Misconceptions

1. **Comparison-bound contradiction:** the algorithm uses representation access outside the comparison model.
2. **Record-count-only complexity:** $\Theta(n+k)$ is shortened incorrectly to $\Theta(n)$.
3. **Sparse-domain allocation:** a few keys trigger an enormous dense histogram.
4. **Range overflow:** $U-L+1$ wraps to a small or negative allocation.
5. **Offset overflow:** $x-L$ overflows before it becomes a valid slot.
6. **Counter overflow:** frequencies or prefix totals wrap below $n$.
7. **Prefix convention mix:** inclusive ends are used as exclusive starts.
8. **Scatter-direction mix:** scan direction reverses equal identities.
9. **Key reconstruction:** attached records disappear while values appear sorted.
10. **Unstable LSD pass:** later equal digits destroy earlier lower-digit order.
11. **Missing top digit:** keys differing only above the processed width remain misordered.
12. **Signed-bit mistake:** raw unsigned representation places negatives after positives.
13. **Endianness mistake:** memory byte order is substituted for digit significance.
14. **Variable-length padding:** an undeclared sentinel changes prefix order.
15. **Upper-endpoint overflow:** $x=1$ maps to bucket $B$ under $\lfloor Bx\rfloor$.
16. **NaN interpolation:** unordered input creates an undefined or arbitrary bucket.
17. **Sample-to-guarantee leap:** observed uniformity is treated as a theorem.
18. **Quadratic skew:** one broad bucket receives a reverse-ordered cluster.
19. **Stability-by-buckets claim:** unstable insertion or local sorting reverses ties.
20. **Output-space omission:** repeated $n$-record buffers are called constant space.
21. **Atomic histogram assumption:** parallel counts do not define stable worker offsets.
22. **Partial buffer publication:** a failed digit pass exposes incomplete output as current.
23. **Free clearing assumption:** zeroing $2^r$ counters can dominate small inputs.
24. **Benchmark monoculture:** one random distribution hides sparse, skewed, and semantic cases.

## Worked Examples

### Example 1

**Question:** Count keys $(-2,1,-1,-2,0)$ over $[-2,1]$.

**Reasoning:** Slots are $x-(-2)=x+2$, so keys map to $(0,3,1,0,2)$. Counts are $(2,1,1,1)$ and exclusive starts are $(0,2,3,4)$.

**Conclusion:** Ordered values are $(-2,-2,-1,0,1)$, and negative keys require only a safe offset—not a negative array index.

### Example 2

**Question:** Stably count records $((2,A),(0,B),(2,C),(1,D),(0,E))$.

**Reasoning:** Counts $(2,1,2)$ produce starts $(0,2,3)$. Forward scatter assigns $B,E$ to positions $0,1$, $D$ to $2$, and $A,C$ to $3,4$.

**Conclusion:** Output is $((0,B),(0,E),(1,D),(2,A),(2,C))$; both equal-key pairs remain stable.

### Example 3

**Question:** Is dense counting practical for $10^6$ records with arbitrary 32-bit unsigned keys and eight-byte counters?

**Reasoning:** The domain has $2^{32}$ slots, so counters alone require $2^{32}\cdot8=32$ GiB. Input size does not shrink that allocation.

**Conclusion:** Use a narrower validated range, radix passes, or a comparison alternative rather than the full histogram.

### Example 4

**Question:** Give the decimal LSD snapshots for keys $(170,45,75,90,802,24,2,66,45)$.

**Reasoning:** Stable ones sorting yields $(170,90,802,2,24,45,75,45,66)$; tens yields $(802,2,24,45,45,66,170,75,90)$; hundreds yields $(2,24,45,45,66,75,90,170,802)$.

**Conclusion:** Each snapshot is ordered by the processed suffix of digits, and the two key-$45$ records retain identity order.

### Example 5

**Question:** Why can an unstable tens pass break a two-digit LSD sort of $(12,11)$?

**Reasoning:** The ones pass correctly produces $(11,12)$. Both tens digits equal $1$. An unstable tens pass may reverse that equal-digit pair to $(12,11)$, destroying the lower-digit order.

**Conclusion:** Stability is the inductive bridge between LSD passes, not an optional output decoration.

### Example 6

**Question:** Compare the simple work proxies for 8-bit and 16-bit digits on one million 32-bit keys.

**Reasoning:** Eight-bit digits use four passes: $4(10^6+256)=4{,}001{,}024$. Sixteen-bit digits use two: $2(10^6+65{,}536)=2{,}131{,}072$. The count arrays have 256 versus 65,536 entries.

**Conclusion:** The larger radix wins this arithmetic proxy but requires far more counter storage and may interact differently with cache and clearing.

### Example 7

**Question:** Show the sign-bit transform for 8-bit two's-complement values $(-128,-1,0,127)$.

**Reasoning:** Raw unsigned bit patterns are $(128,255,0,127)$, whose unsigned order is semantically wrong. XOR with $128$ produces transformed keys $(0,127,128,255)$.

**Conclusion:** Sorting transformed keys unsigned returns the correct signed order $(-128,-1,0,127)$.

### Example 8

**Question:** For $n=B=1000$ independent uniform bucket assignments, compute expected $\sum_jn_j^2$.

**Reasoning:**

$$
n+\frac{n(n-1)}B
=1000+\frac{1000\cdot999}{1000}
=1999.
$$

**Conclusion:** Quadratic per-bucket inner bounds sum to a linear expectation under this stated experiment.

### Example 9

**Question:** What if 1000 distinct descending keys all enter one broad bucket sorted by insertion sort?

**Reasoning:** That bucket has $n_0=1000$, and reverse insertion uses

$$
\frac{1000\cdot999}{2}=499{,}500
$$

key comparisons in the conventional model.

**Conclusion:** Distribution overhead remains linear, but skew exposes quadratic inner work.

### Example 10

**Question:** A floating bucket map accepts $x\in[0,1]$ and computes $\lfloor100x\rfloor$. What must change?

**Reasoning:** $x=1$ maps to invalid index $100$, while NaN has no ordered interval. Define domain $[0,1)$, or explicitly clamp the finite upper endpoint to bucket $99$; reject or separately order NaN.

**Conclusion:** Endpoint and exceptional-value semantics precede bounds-safe arithmetic.

## Cross-Program Connections

- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) owns arrays, counters, prefix structures, buckets, and container identity.
- [Programming Languages & Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) owns integer overflow, signed representation contracts, floating total order, text semantics, and callback behavior.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) owns cache, bandwidth, vectorization, endianness, atomics, and memory-layout mechanisms.
- [Concurrent & Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) owns worker histograms, prefix reductions, stable offsets, synchronization, and contention.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns allocation abuse, adversarial skew, untrusted keys/callbacks, and resource limits.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns property, differential, distribution, fault-injection, and performance validation.

## References

1. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. [*Introduction to Algorithms*, fourth edition](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), MIT Press, 2022. Counting sort, radix sort, bucket sort, correctness, and analysis.
2. Donald E. Knuth. [*The Art of Computer Programming, Volume 3: Sorting and Searching*, second edition](https://www.informit.com/store/art-of-computer-programming-volume-3-sorting-and-searching-9780321635785), Addison-Wesley Professional, 1998. Distribution sorting, key representations, and historical foundations.
3. National Institute of Standards and Technology. [“Counting sort”](https://xlinux.nist.gov/dads/HTML/countingsort.html), *Dictionary of Algorithms and Data Structures*, consulted 2026-09-04. Histogram, cumulative positions, and key-domain definition.
4. National Institute of Standards and Technology. [“Radix sort”](https://xlinux.nist.gov/dads/HTML/radixsort.html), *Dictionary of Algorithms and Data Structures*, entry modified 2022; consulted 2026-09-04. Stable least-significant distribution and collection.
5. National Institute of Standards and Technology. [“Bucket sort”](https://xlinux.nist.gov/dads/HTML/bucketsort.html), *Dictionary of Algorithms and Data Structures*, entry modified 2019; consulted 2026-09-04. Bucket mapping, local sorting, concatenation, and distribution conditions.
6. Robert Sedgewick and Kevin Wayne. [“String Sorts”](https://algs4.cs.princeton.edu/51radix/), companion to *Algorithms*, fourth edition, consulted 2026-09-04. Key-indexed counting, LSD/MSD implementations, integer bytes, and in-place variants.
7. ACM, IEEE Computer Society, and AAAI. [*Computer Science Curricula 2023: Algorithmic Foundations*](https://csed.acm.org/al-cs-core/), endorsed 2024; consulted 2026-09-04. Current curricular scope for bucket/radix sorting, invariants, complexity, and empirical evaluation.

## Exercises

### Exercise 1

Stably counting-sort records $((-1,A),(2,B),(-1,C),(0,D),(2,E))$ over declared range $[-1,2]$. Give slot mapping, counts, exclusive starts, every output block, and final identity order. State the arithmetic and memory checks required before allocation.

### Exercise 2

Prove LSD radix sort correct for fixed-width radix-$b$ encodings using induction on processed digits. Give a minimal counterexample showing that an unstable later pass can destroy correct lower-digit order, and explain why stable passes also preserve equal complete-key records.

### Exercise 3

For $n=10^6$ unsigned 64-bit keys and eight-byte counters, compare $r=8$, $r=11$, and $r=16$ using proxy $\lceil64/r\rceil(n+2^r)$. Compute pass counts, proxy totals, and counter bytes. Explain why the smallest proxy does not automatically minimize elapsed time.

### Exercise 4

Derive $\mathbb E[\sum_jn_j^2]=n+n(n-1)/B$ for $n$ independent records assigned uniformly to $B$ buckets. Evaluate it for $B=n/2$, $B=n$, and $B=2n$. Then give a deterministic inner-sort policy that prevents quadratic worst-case work under skew.

### Exercise 5

A service must stably sort fifty million event records by signed 64-bit timestamp, then preserve arrival order for equal timestamps. Records are wide, memory is bounded, inputs may be sparse or adversarial, cancellation and allocation failure are contractual, and parallel execution is desirable. Design the encoding, algorithm/fallback, buffers or indices, counter/radix choice, stability composition, parallel offsets, failure publication, validation, telemetry, and comparison baselines.

## Answers to the Exercises

### Answer 1

With $L=-1$, slot is $x-L=x+1$. The record slots are $(0,3,0,1,3)$. Frequencies over slots $0,1,2,3$ are

$$
c=(2,1,0,2).
$$

Exclusive starts are

$$
s=(0,2,3,3).
$$

Thus blocks are:

- slot $0$, key $-1$: output $[0,2)$;
- slot $1$, key $0$: output $[2,3)$;
- slot $2$, key $1$: output $[3,3)$;
- slot $3$, key $2$: output $[3,5)$.

Scanning input left to right yields

$$
((-1,A),(-1,C),(0,D),(2,B),(2,E)).
$$

The $A,C$ and $B,E$ pairs retain their input identity order.

Before allocation, verify $L\le U$, compute $k=U-L+1=4$ in a type that cannot overflow, validate every offset is in $[0,4)$, ensure counters and prefix totals can represent $n=5$, and ensure four counters/positions plus a five-record output fit the memory policy.

### Answer 2

Let a key have digits $(a_{d-1},\ldots,a_0)$. Claim that after pass $t$, records are sorted by tuple $(a_t,\ldots,a_0)$.

At $t=0$, the stable distribution pass orders $a_0$, establishing the claim. Assume it holds after $t-1$. Pass $t$ orders records with different $a_t$ values. When two records have the same $a_t$, stability preserves their prior relative order, which by induction is order by $(a_{t-1},\ldots,a_0)$. Therefore the longer tuple is ordered. At $t=d-1$, it is the complete order-preserving encoding, so semantic keys are sorted.

For a counterexample, decimal keys $(12,11)$ become $(11,12)$ after the ones pass. Their tens digits both equal $1$. An unstable tens pass is allowed to output $(12,11)$, destroying the already-correct ones order.

If two complete keys are equal, they have equal digit at every pass. Stability preserves their relative identity order at the first pass and again at every subsequent pass, so the complete radix sort is stable.

### Answer 3

The models are:

$$
\begin{array}{c|c|c|c}
r & d=\lceil64/r\rceil & d(n+2^r) & 8\cdot2^r\text{ counter bytes}\\
\hline
8 & 8 & 8(1{,}000{,}256)=8{,}002{,}048 & 2{,}048\\
11 & 6 & 6(1{,}002{,}048)=6{,}012{,}288 & 16{,}384\\
16 & 4 & 4(1{,}065{,}536)=4{,}262{,}144 & 524{,}288
\end{array}
$$

By this proxy, $r=16$ is smallest. Elapsed time also includes clearing and prefixing counters, cache/TLB behavior, digit extraction, output-buffer traffic, copy-back parity, worker-local histogram multiplication, scheduling, and record/reference width. The 512 KiB count array may behave differently from 2 KiB or 16 KiB arrays, so benchmark feasible choices on preserved workloads.

### Answer 4

Expand the square sum as ordered pairs:

$$
\sum_jn_j^2
=
\sum_{a=1}^{n}\sum_{c=1}^{n}
\mathbf 1[\text{records }a,c\text{ share a bucket}].
$$

There are $n$ self-pairs, each contributing $1$. For every one of the $n(n-1)$ ordered distinct pairs, independent uniform assignment gives probability $1/B$ of sharing a bucket. Linearity of expectation gives

$$
\mathbb E\left[\sum_jn_j^2\right]
=n+\frac{n(n-1)}B.
$$

Therefore:

$$
\begin{aligned}
B=n/2 &: &&3n-2,\\
B=n &: &&2n-1,\\
B=2n &: &&\frac{3n-1}{2}.
\end{aligned}
$$

All are $\Theta(n)$ for proportional $B$. A deterministic policy can use insertion sort only while occupancy is below a fixed threshold, then use stable merge sort within a large bucket. The total inner worst case becomes $O(n\log n)$ rather than $O(n^2)$, while small buckets retain simple low overhead.

### Answer 5

Normalize each timestamp to an order-preserving unsigned key. If the service contract guarantees 64-bit two's complement, reinterpret the bits and XOR the sign bit $2^{63}$. Define rejected or special timestamp sentinels before encoding. Keep arrival order out of the primary key if stable output is required; every digit scatter must preserve it.

Dense counting over the full 64-bit range is impossible. Use stable LSD radix on compact indices or references into the wide record store, avoiding repeated wide-record copies. A stable merge sort is the deterministic general fallback and baseline; it also works if key encoding or radix memory is rejected. If enough memory for one index output buffer is unavailable, use an external stable merge design rather than silently dropping stability.

Choose $r$ from measured feasible counter arrays, for example 8, 11, or 16 bits. Account for two index buffers if ping-pong is used, materialized transformed keys, worker-local counts, global prefix arrays, and peak memory. A four-pass 16-bit design saves scans but multiplies each worker's histogram; a smaller radix may fit caches and parallel memory better.

For parallel stable scatter, each worker counts its contiguous input shard. Reduce to global digit totals, compute global block starts, then prefix worker counts within each digit to assign disjoint worker subranges in input-shard order. Each worker scans its shard forward. Global digit order, worker order, and local order then compose into stability.

Allocate and validate all required buffers before publishing mutation. Treat the last fully completed pass's buffer as authoritative; a failed or cancelled pass never becomes visible. Check counter/prefix overflow and require the final total to equal $n$. Preserve ownership of every original record regardless of index-buffer failure.

Test signed extrema, zero, negative zero if the source type permits it, duplicates with arrival identities, sparse ranges, all equal, sorted/reverse, high-bit distinctions, maximum size, worker boundaries, every pass parity, allocation failure, cancellation at each scan, and adversarial concentrations. Differential-check against a stable trusted comparison sort.

Record pass count, radix, histogram sizes, maximum digit frequency, keys and bytes read, indices/records written, allocation peak, cache/bandwidth metrics, worker imbalance, cancellation latency, failures, and tail time. Compare radix choices, single-thread and parallel stable merge, relevant stable library sorting, and external sorting if memory pressure approaches the contract.
