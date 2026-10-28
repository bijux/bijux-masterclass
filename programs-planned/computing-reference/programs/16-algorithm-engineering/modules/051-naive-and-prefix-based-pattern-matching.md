---
module_id: ALGE-051
program: Algorithm Engineering
level: 2
module_number: 51
title: Naive and Prefix-Based Pattern Matching
status: complete
last_verified: 2026-09-05
---

# Naive and Prefix-Based Pattern Matching

## One-Page Review

### Governing question

How can we specify exact pattern matching precisely, establish a trustworthy baseline, and use prefix information to find every occurrence in linear time without hiding text semantics or boundary policy?

### Essential definitions

- A **text** $T=T[0]T[1]\dots T[n-1]$ and **pattern** $P=P[0]P[1]\dots P[m-1]$ are finite sequences over a declared alphabet $\Sigma$.
- An **occurrence** starts at shift $s$ when $0\le s\le n-m$ and $T[s+j]=P[j]$ for every $0\le j<m$.
- Occurrences may **overlap**; reporting one does not consume its symbols.
- The **naive matcher** tests each legal shift directly. Its worst-case time is $\Theta((n-m+1)m)$ and its auxiliary space is $O(1)$, excluding output.
- A **border** of a string is a proper prefix that is also a suffix. Repeated borders explain why previous comparisons can be reused.
- The **Z-value** $Z[i]$ is the length of the longest prefix of a sequence $S$ that equals the substring beginning at $i$; by convention $Z[0]=0$ here.
- A **Z-box** $[\ell,r]$ is the rightmost interval already known to equal $S[0:r-\ell+1]$.
- A **typed separator** is a token outside $\Sigma$, used to prevent a match from crossing the boundary in $P\mathbin{\|}\bot\mathbin{\|}T$.

### Central model, mechanism, or theorem

Build $S=P\mathbin{\|}\bot\mathbin{\|}T$, compute its Z-array, and report text shift $s$ exactly when

$$
Z[m+1+s]\ge m.
$$

The Z-box invariant lets an implementation copy a proved lower bound from an earlier prefix comparison and perform new comparisons only when it can extend the right boundary. Since that boundary advances at most $|S|-1$ times, the entire computation is $O(|S|)=O(n+m)$.

### Critical invariants

- Equality, indexing unit, normalization, case policy, and empty-pattern policy are fixed before matching.
- Candidate shifts are exactly $0$ through $n-m$ when $m\le n$.
- A reported shift denotes a full match, including overlapping occurrences.
- Before processing $i$, every stored Z-value before $i$ is correct, and $S[\ell:r+1]=S[0:r-\ell+1]$ for the active rightmost Z-box.
- Reused Z-information is capped at the known box boundary; only explicit comparisons extend $r$.
- The separator cannot compare equal to any text or pattern symbol.
- Complexity claims include preprocessing, storage, and output, and identify whether the text is resident or streamed.

### Common failures

Common failures include confusing bytes, code points, and grapheme clusters; assuming canonically equivalent Unicode sequences compare equal; omitting overlaps; assigning accidental semantics to an empty pattern; accepting a separator that can occur in input; using an off-by-one Z-box formula; copying a Z-value beyond the known box; calling early-exit naive search linear; measuring only match-heavy or mismatch-heavy data; retaining an entire stream unnecessarily; and treating observed library speed as a theorem.

### Compact example

For $P=\texttt{aba}$ and $T=\texttt{ababa}$, naive search checks shifts $0,1,2$ and reports $0,2$. With $S=\texttt{aba}\bot\texttt{ababa}$, the Z-values at combined positions $4$ and $6$ are at least $3$, so the same shifts are reported. The overlap at text position $2$ is valid because exact matching reports positions rather than consuming substrings.

### Connections

[ALGE-050](./050-turning-a-domain-problem-into-a-graph-optimization-problem.md) closes Level I with model discipline; this module applies the same discipline to sequence semantics. [ALGE-052](../ROADMAP.md#block-06--string-sequence-and-compression-algorithms) develops the failure-function and streaming KMP formulation. Data Structures Engineering owns compact sequence representations; Operating Systems owns memory mapping and page behavior; Security Engineering owns adversarial resource limits and canonicalization policy.

## Governing Question

Given a pattern and a text, how do we define what a symbol and an occurrence mean, implement a transparent reference matcher, derive a prefix-based linear-time matcher, prove both correct, and decide which evidence is sufficient for a production use?

Exact matching sounds elementary because its mathematical core is only equality. The engineering difficulty lies at the boundaries: which units are equal, whether normalization is allowed, how empty patterns behave, whether overlapping matches are required, how a stream is partitioned, and whether adversarial repetition can exhaust resources. This chapter makes those decisions explicit before optimizing comparisons.

## Why This Matters

Exact search is a primitive inside editors, protocol parsers, intrusion detection, genome pipelines, log processing, deduplication, and larger indexing systems. A reference implementation is valuable even when it is not deployed: it provides an independent oracle for optimized code, exposes semantic choices, and produces adversarial tests.

Prefix-based matching introduces a reusable algorithm-engineering pattern. Work performed at one position is summarized by an invariant and safely reused later. The asymptotic improvement is not caused by guessing where a match lies; it comes from proving which equalities are already known and charging each new comparison to monotone progress.

Production performance is broader than a comparison count. Representation conversions, normalization, decoding, allocation, cache locality, output size, and stream buffering may dominate. A linear matcher over the wrong sequence model is still wrong, and a theorem about abstract symbols does not predict the fastest implementation on every workload.

## Prerequisites and Retrieval

Retrieve arrays and half-open slices, loop invariants, asymptotic upper and lower bounds, amortized analysis, adversarial input construction, immutable input contracts, and differential testing. Review [ALGE-006](./006-best-worst-expected-and-amortized-cost.md) for cost bounds and charging arguments, [ALGE-011](./011-linear-and-binary-search.md) for search invariants, and [ALGE-015](./015-heapsort.md) for in-place array reasoning.

You should be comfortable distinguishing a mathematical sequence from its representation. No knowledge of KMP, suffix arrays, or compression is assumed.

## Learning Objectives

After completing this module, you should be able to:

1. specify exact matching over a declared sequence model;
2. state policies for empty patterns, overlaps, normalization, and malformed input;
3. implement and verify a naive reference matcher;
4. construct worst-case families for naive comparison counts;
5. define Z-values and maintain a Z-box invariant;
6. derive the Z algorithm rather than memorize its cases;
7. prove the pattern-to-Z reduction sound and complete;
8. prove linear time with a monotone-boundary argument;
9. design resident and streaming interfaces with explicit resource bounds; and
10. evaluate implementations with correctness oracles and representative workloads.

## Core Exposition

### Specify the sequence before the search

Let $T\in\Sigma^n$ and $P\in\Sigma^m$. The alphabet $\Sigma$ can be bytes, Unicode scalar values, grapheme clusters, integers, events, tokens, or domain records with a stable equality relation. The algorithm requires only equality, but the application must decide what equality means.

A UTF-8 byte sequence, a sequence of Unicode code points, and a sequence of user-perceived grapheme clusters are different texts. Byte offsets are useful for files and protocols; code-point offsets may suit language tooling; grapheme-cluster offsets may suit user interfaces. Converting among them changes indices and may require extra storage. Record both the unit and the coordinate system in the API.

Unicode canonical equivalence is not automatic equality. For example, a precomposed character and a base character followed by a combining mark can render alike but contain different code-point sequences. If canonical equivalence is part of the product contract, normalize both operands to a chosen form before matching and account for the effect on offsets. Unicode Standard Annex #15, Revision 57 for Unicode 17.0.0, defines NFC, NFD, NFKC, and NFKD; compatibility normalization is not a harmless substitute for canonical normalization because it can erase distinctions.

Case-insensitive, locale-aware, or collation-based search is not ordinary exact matching. Case folding can expand characters and can invalidate a simple one-input-index-to-one-output-index mapping. Treat such transformations as an explicit preprocessing and projection layer, not as an undocumented equality operator.

### Define the result contract

For a nonempty pattern, define the occurrence set

$$
\operatorname{Occ}(P,T)=\{s\mid 0\le s\le n-m\land
\forall j\in\{0,\dots,m-1\},\ P[j]=T[s+j]\}.
$$

If $m>n$, the set is empty. Occurrences overlap unless the caller asks for a separate non-overlap policy. A matcher that stops after the first result implements a different interface from one that reports all results.

The empty pattern needs a product decision. Mathematically, it matches at every boundary $0,\dots,n$ because its universal equality condition is vacuous. Some APIs instead reject it or return only position zero. Any policy can be coherent, but it must be stated identically in the specification, implementation, tests, and complexity bound. This chapter's executable example adopts the all-boundaries policy.

An output array can itself require $\Theta(n)$ space: the pattern `a` occurs $n$ times in `a` repeated $n$ times. Thus an all-occurrences matcher has time lower bound $\Omega(n+z)$, where $z$ is the number of reported positions. A callback or iterator can reduce retained output space, but it cannot erase the work of emitting $z$ results.

### Establish the naive oracle

The naive algorithm enumerates every legal shift $s$. At each shift it compares $P[0],P[1],\dots$ with the corresponding text symbols until either one differs or all $m$ symbols agree. It is correct almost directly from the occurrence definition: every reported shift satisfies every required equality, and every occurrence is examined and therefore reported.

When $0<m\le n$, there are $n-m+1$ candidates and at most $m$ comparisons per candidate, giving $O((n-m+1)m)$. This bound is tight. Set $P=a^{m-1}b$ and $T=a^n$. At every candidate shift the first $m-1$ comparisons succeed and the last fails, so the matcher performs exactly $(n-m+1)m$ symbol comparisons and reports nothing.

Early mismatch is still useful in practice. If independent symbols match with small probability, many alignments fail near their first character. That observation is workload evidence, not a worst-case guarantee. The naive matcher remains especially valuable as readable specification code and a differential oracle for small generated cases.

### Extract prefix information

For a sequence $S$ of length $N$, define

$$
Z[i]=\max\{k\mid 0\le k\le N-i\land S[0:k]=S[i:i+k]\}.
$$

We set $Z[0]=0$ because comparing the complete sequence with itself conveys no useful reuse here. Other texts use $Z[0]=N$; either convention works if stated consistently.

Suppose processing has established a rightmost interval $[\ell,r]$ such that

$$
S[\ell:r+1]=S[0:r-\ell+1].
$$

This is the Z-box. At a new position $i$:

1. If $i>r$, no equality at $i$ follows from the active box. Start with $k=0$ and compare explicitly.
2. If $i\le r$, let $q=i-\ell$. The box proves that the substring from $i$ through $r$ equals the prefix substring from $q$ through $r-\ell$. Therefore initialize

$$
k=\min(Z[q],r-i+1).
$$

3. Compare $S[k]$ with $S[i+k]$ while both positions exist and symbols are equal.
4. Store $Z[i]=k$. If $i+k-1>r$, replace the box with $[i,i+k-1]$.

The minimum in step 2 is essential. If $Z[q]$ extends beyond the corresponding part of the active box, the stored box proves nothing about those symbols; they must be compared explicitly. Copying the full value can manufacture a match.

### Prove the Z invariant

Assume all $Z[j]$ for $j<i$ are exact and the active box is the rightmost prefix-matching interval among those positions. If $i>r$, explicit comparison obviously finds the longest match at $i$.

If $i\le r$, the box equality maps $S[i:i+d]$ to $S[q:q+d]$ for any $d\le r-i+1$. Because $Z[q]$ is exact, the first $\min(Z[q],r-i+1)$ symbols match the prefix. If $Z[q]<r-i+1$, the next symbols differ inside the box, so $Z[i]=Z[q]$ and no explicit extension is needed. If $Z[q]\ge r-i+1$, equality is known only through $r$; comparisons starting at $r+1$ find the exact extension. In both cases the resulting $Z[i]$ is exact. Updating the box only with that exact prefix match preserves its equality and rightmost property.

This is an induction proof over $i$. The proof is stronger than an intuition about repeated text: it identifies exactly which comparisons may be skipped.

### Prove linear time

There are $N-1$ loop iterations and constant work per iteration outside the explicit comparison loop. Comparisons that remain inside an existing box are avoided by reuse. Every successful explicit comparison beyond the box increases $r$ by one. Since $r$ starts below the sequence and never decreases, at most $N-1$ such increases occur. Each iteration can also perform at most one failing comparison that stops extension. Therefore the total number of comparisons and total running time are $O(N)$; the Z-array uses $O(N)$ space.

This is amortized analysis. A single position can extend far, but all long extensions share one finite budget of right-boundary advances.

### Reduce pattern matching to Z-values

Create a token sequence

$$
S=P\mathbin{\|}\bot\mathbin{\|}T,
$$

where the separator $\bot$ is unequal to every element of $P$ and $T$. Text shift $s$ begins at combined index $i=m+1+s$.

If $P$ occurs at $s$, the first $m$ symbols at $S[i:]$ equal the prefix $P$, so $Z[i]\ge m$. Conversely, if $Z[i]\ge m$, those $m$ symbols equal $P$ and lie entirely in the text suffix, so $P=T[s:s+m]$. Thus reporting $s$ exactly when $Z[m+1+s]\ge m$ is sound and complete.

The separator is a proof obligation, not punctuation. Choosing `$` is unsafe unless input validation excludes it. A tagged token or a fresh object avoids collision in an in-memory implementation. A virtual concatenated view can avoid materializing the combined sequence.

### Reproduce both algorithms

The following dependency-free Python program specifies the empty-pattern policy, reports overlaps, uses a fresh object as a typed separator, and asserts agreement between the naive and Z-based algorithms.

<!-- bijux-verify: {"id":"naive-and-z-search","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"naive=(0, 5, 7)\nz_search=(0, 5, 7)\nagree=True\nempty=(0, 1, 2, 3)\n","stderr":""}} -->
```python
def naive_search(pattern, text):
    m, n = len(pattern), len(text)
    if m == 0:
        return tuple(range(n + 1))
    return tuple(
        shift
        for shift in range(n - m + 1)
        if all(pattern[j] == text[shift + j] for j in range(m))
    )


def z_values(sequence):
    z = [0] * len(sequence)
    left, right = 0, -1
    for i in range(1, len(sequence)):
        matched = 0 if i > right else min(z[i - left], right - i + 1)
        while (
            i + matched < len(sequence)
            and sequence[matched] == sequence[i + matched]
        ):
            matched += 1
        z[i] = matched
        if i + matched - 1 > right:
            left, right = i, i + matched - 1
    return z


def z_search(pattern, text):
    m, n = len(pattern), len(text)
    if m == 0:
        return tuple(range(n + 1))
    separator = object()
    combined = list(pattern) + [separator] + list(text)
    z = z_values(combined)
    return tuple(
        shift for shift in range(n - m + 1) if z[m + 1 + shift] >= m
    )


text = "ababaabababa"
pattern = "ababa"
naive = naive_search(pattern, text)
prefix_based = z_search(pattern, text)
assert naive == prefix_based
print(f"naive={naive}")
print(f"z_search={prefix_based}")
print(f"agree={naive == prefix_based}")
print(f"empty={z_search('', 'abc')}")
```

This run demonstrates the stated behavior on one CPython environment. The proof establishes the algorithms for finite sequences satisfying the equality and separator assumptions; neither the run nor the proof decides an application's text semantics.

### Engineer resident and streaming variants

The direct Z reduction stores $P$, $T$, the combined sequence, and a Z-array, so its straightforward auxiliary storage is $O(n+m)$. It suits resident inputs and batch search. A virtual combined sequence removes one copy but not the Z-array. If only match positions are needed, specialized online prefix methods can use $O(m)$ state; [ALGE-052](../ROADMAP.md#block-06--string-sequence-and-compression-algorithms) develops that route.

Naive search can process chunks with $m-1$ symbols of carry so a match spanning two chunks is not lost. The implementation must attach each retained symbol to its absolute input coordinate, suppress duplicate starts already emitted, and define what happens when decoding or normalization requires context across chunk boundaries. Normalization itself may need buffering; UAX #15 explicitly treats streaming concerns.

For untrusted inputs, bound pattern length, decoded size, retained carry, result count, and processing time. A naive implementation has an obvious repeated-prefix denial-of-service family. A linear algorithm prevents that comparison explosion but does not cap output volume or preprocessing expansion.

### Validate beyond one example

Use the naive matcher as a differential oracle for random short sequences. Enumerate small alphabets exhaustively when feasible. Include:

- empty pattern and empty text under the chosen policy;
- $m>n$, $m=n$, and $m=1$;
- no matches, one match, all positions, and overlapping matches;
- repeated symbols and long borders;
- a separator-like input symbol;
- transformed text with an index projection;
- chunk boundaries at every position;
- maximum allowed input and output sizes.

For performance evidence, record the implementation, runtime version, hardware, representation, $n$, $m$, alphabet distribution, match frequency, output mode, preprocessing inclusion, warm-up policy, and repeated trials. Compare resident and streaming modes separately. Do not infer universal superiority from one language's built-in search or one corpus.

## Definitions and Notation

Let $\Sigma$ be an alphabet with a deterministic equality relation. Let $P\in\Sigma^m$, $T\in\Sigma^n$, and $S\in(\Sigma\cup\{\bot\})^N$ with $N=n+m+1$ and $\bot\notin\Sigma$.

- $X[a:b]$ denotes the half-open subsequence $X[a],\dots,X[b-1]$.
- A **shift** is a candidate start coordinate in the text.
- $\operatorname{Occ}(P,T)$ is the ordered set of all occurrence shifts.
- A **prefix** of $X$ is $X[0:k]$; a **suffix** ends at $|X|$.
- A **proper** prefix or suffix is shorter than the complete sequence.
- A **border** is a sequence that is both a proper prefix and a suffix.
- $Z[i]$ is the longest common-prefix length of $S$ and $S[i:]$.
- A **candidate Z-box** for position $i$ is $[i,i+Z[i]-1]$ when $Z[i]>0$.
- The **active Z-box** $[\ell,r]$ is the processed candidate box with greatest right endpoint, with ties resolved arbitrarily.
- $z=|\operatorname{Occ}(P,T)|$ is output size.
- **Soundness** means every reported shift is an occurrence; **completeness** means every occurrence is reported.
- **Auxiliary space** excludes immutable inputs and emitted output unless stated otherwise.
- **Resident processing** assumes the complete text is addressable; **streaming processing** receives bounded chunks over time.

The abstract cost model counts symbol equality, indexing, and integer operations as $O(1)$. This assumption may fail for domain records with expensive equality, compressed storage, or transformed views. An implementation report must name its actual unit and representation.

## Mechanisms, Invariants, or Proof Structure

### Contract-to-implementation chain

The evidence chain is:

$$
\text{semantic policy}\to\text{sequence representation}\to\text{occurrence definition}
\to\text{algorithm invariant}\to\text{implementation}\to\text{reported coordinates}.
$$

Each arrow has separate failure modes. Algorithm correctness does not prove that normalization is appropriate or that transformed coordinates were projected correctly.

### Naive-loop invariant

Immediately before testing shift $s$, every legal shift smaller than $s$ has been classified correctly and no larger shift has been classified. The inner loop maintains that the first $j$ pattern symbols equal their aligned text symbols. A mismatch proves the current shift is not an occurrence; reaching $j=m$ proves that it is. Advancing $s$ preserves the outer invariant. Exhaustion proves completeness.

### Z-loop invariant

Immediately before iteration $i$:

1. every $Z[j]$ for $1\le j<i$ is exact;
2. if $r\ge\ell$, $S[\ell:r+1]=S[0:r-\ell+1]$;
3. $r$ is the maximum right endpoint of a Z-box beginning before $i$;
4. no unverified equality beyond $r$ is reused.

The inside-box initialization follows from items 1 and 2. The explicit loop establishes all new equality beyond the known region. A failed comparison or sequence end proves maximality. The update preserves all four clauses.

### Pattern-reduction theorem

**Theorem.** For nonempty $P$, collision-free $\bot$, and every $0\le s\le n-m$,

$$
s\in\operatorname{Occ}(P,T)\iff Z[m+1+s]\ge m.
$$

**Proof.** At combined index $m+1+s$, the next $m$ symbols are exactly $T[s:s+m]$. The first $m$ symbols of $S$ are exactly $P$. Therefore their equality is equivalent to the Z-value at that index being at least $m$. The separator lies before the indexed text suffix and cannot participate in these $m$ comparisons. This proves both directions. $\square$

### Complexity theorem

**Theorem.** The stated Z computation runs in $O(N)$ time and stores $O(N)$ integers.

**Proof.** The outer loop contributes $N-1$ constant-time iterations. Each successful explicit comparison that passes the current right boundary advances $r$, which can advance at most $N-1$ times. Each iteration contributes at most one comparison that fails or reaches the end after its extension. Reused equalities inside a box require no symbol comparisons. Hence total comparisons are linear. The array has $N$ entries. $\square$

The pattern reduction therefore runs in $O(n+m+z)$ time when emission is counted and uses $O(n+m)$ auxiliary space in its direct materialized form.

### Evidence boundaries

- The definitions determine intended results only for the declared sequence model.
- The proofs establish correctness and asymptotic bounds under their assumptions.
- Differential and exhaustive tests find implementation disagreements on tested inputs.
- Snippet execution records behavior in one environment.
- Benchmarks describe observed workloads and machines.
- Human product review is still needed for normalization, privacy, security, and user-facing coordinate policy.

## Alternatives and Trade-Offs

| Approach | Preprocessing | Search time | Extra state | Strength | Limitation |
|---|---:|---:|---:|---|---|
| Naive alignment | $O(1)$ | worst-case $O(nm)$ | $O(1)$ | transparent oracle; tiny implementation | repeated-prefix adversary |
| Z reduction | $O(n+m)$ over combined input | included in $O(n+m)$ | $O(n+m)$ direct | all prefix matches; simple linear proof | straightforward form is resident and allocates Z-array |
| KMP | $O(m)$ | $O(n+z)$ | $O(m)$ | natural online scan and reusable pattern | failure-function construction has its own invariant |
| Boyer-Moore family | pattern-dependent | sublinear inspections on favorable data; bounded variants vary | $O(m+|\Sigma|)$ typical | skips ahead in practice | guarantees and tables depend on variant |
| Rabin-Karp | $O(m)$ | expected/fingerprint-filter dependent; verification required | $O(1)$ or more | many patterns and rolling windows | collisions forbid hash-only exactness |
| Suffix index | text-index construction | fast repeated queries | large text-owned index | many queries over stable corpus | construction and maintenance cost |

Use naive search when inputs are small, a transparent oracle matters, or deployment evidence shows it sufficient under hard bounds. Use Z-values when all prefix-match lengths are useful or batch resident matching is acceptable. Use KMP when one pattern is reused or the text arrives online. Later modules develop the other families; their presence does not make the baseline obsolete.

Built-in string search can exploit vector instructions, specialized two-way algorithms, and runtime-specific representations. Prefer it for ordinary production search when its semantics match the contract and it has been tested on the target runtime. Keep independent tests because a fast opaque implementation is not a specification.

Normalization before matching gives canonical-equivalence semantics but adds work, may change length, and complicates offset projection. Normalizing stored data once can reduce repeated cost, but only if versioning and ingestion policy guarantee that every value conforms. Compatibility normalization and case folding broaden equality further and can be inappropriate for identifiers or security decisions.

## Failure Modes and Misconceptions

1. **“A character is a character.”** Bytes, code points, grapheme clusters, and display cells are different units with different offsets.
2. **“Visually identical text must match.”** Rendering does not imply identical encoded sequences; canonical equivalence requires an explicit normalization policy.
3. **“The empty pattern obviously has one answer.”** Multiple coherent conventions exist. Undeclared behavior is the defect.
4. **“Finding a match lets us skip its interior.”** That loses overlaps, such as shifts $0$ and $2$ for `aba` in `ababa`.
5. **“Early exit makes naive search linear.”** It often helps, but $a^{m-1}b$ against $a^n$ forces $m$ comparisons at each shift.
6. **“A separator character is surely absent.”** External input can contain it. Use a typed token or validate the alphabet.
7. **“Inside a Z-box, copy $Z[i-\ell]$.”** Only the portion capped by $r-i+1$ is proved.
8. **“Linear time means constant memory.”** The direct Z construction stores a linear array and materialized combined input.
9. **“Linear search bounds resource use.”** Output can still be $\Theta(n)$, and transformations can expand or buffer input.
10. **“Normalization preserves offsets.”** It can compose, decompose, or otherwise change sequence length; projection metadata is needed.
11. **“A benchmark proves the best algorithm.”** It supports only the measured implementation, representation, machine, and workload.
12. **“Passing differential tests proves correctness.”** Tests sample behavior; the invariant and reduction proof establish the general claim.

## Worked Examples

### Example 1

**Situation.** Find every occurrence of $P=\texttt{aba}$ in $T=\texttt{ababa}$.

There are $n-m+1=5-3+1=3$ legal shifts. At shift 0, `aba` equals `aba`, so report 0. At shift 1, the first comparison is `a` versus `b`, so reject 1. At shift 2, all three symbols agree, so report 2.

**Conclusion.** The result is $(0,2)$. Exact all-occurrences matching retains the overlapping second occurrence.

### Example 2

**Situation.** Define boundary behavior for $P=\epsilon$ and $T=\texttt{cat}$.

Under this chapter's all-boundaries policy, the empty sequence equals every zero-length slice. A length-three sequence has boundaries 0, 1, 2, and 3, so the result is $(0,1,2,3)$. Under a reject-empty API the operation would instead return an error; silently switching between these policies is invalid.

**Conclusion.** Empty-pattern behavior is a contract choice. Here it produces $n+1=4$ results and must be included in the output bound.

### Example 3

**Situation.** Show that early mismatch does not improve the naive worst case for $P=\texttt{aaaab}$ and $T=\texttt{aaaaaaaa}$.

Here $m=5$, $n=8$, and there are four candidate shifts. At every shift the first four `a` symbols match and the final comparison checks pattern `b` against text `a`, then fails. The comparison count is $4\cdot5=20$, equal to $(n-m+1)m$; there are no results.

**Conclusion.** The naive upper bound is attained even when the implementation stops at the first mismatch.

### Example 4

**Situation.** Compute Z-values for $S=\texttt{aabcaabxaaaz}$ at selected positions.

At $i=1$, `a` matches the prefix's first `a`, but `b` differs from the prefix's second `a`, so $Z[1]=1$. At $i=4$, `aab` matches the first three symbols and then `x` differs from prefix `c`, so $Z[4]=3$. At $i=8$, `aa` matches and the third compared symbol is `a` versus prefix `b`, so $Z[8]=2$. At $i=9$, the first two `a` symbols match: specifically, $S[9]=S[0]$ and $S[10]=S[1]$. The third comparison is $S[11]=\texttt{z}$ against $S[2]=\texttt{b}$ and fails, hence $Z[9]=2$.

**Conclusion.** Z-values are longest prefix matches, not counts of a repeated first symbol; each value ends at the first unequal aligned pair or sequence end.

### Example 5

**Situation.** Explain why copying an inside-box value without capping is unsound.

Suppose the active box is $[\ell,r]=[4,9]$ and $i=7$. Then only $r-i+1=3$ positions beginning at $i$ are known through the box equality. Let $q=i-\ell=3$ and suppose the already computed $Z[q]=5$. The earlier value says five symbols match at position 3, but the active box transfers only three of those equalities to position 7. Initializing to 5 would assert two unproved comparisons. Initializing to $\min(5,3)=3$ is justified, after which explicit comparison may extend it.

**Conclusion.** The Z-box is a bounded proof object. Reuse must stop at its right boundary.

### Example 6

**Situation.** Reduce $P=\texttt{aba}$ and $T=\texttt{ababa}$ to one Z computation.

Construct $S=\texttt{aba}\bot\texttt{ababa}$. The text starts at combined index 4. At index 4, the suffix begins `ababa`, whose first three symbols equal `aba`, so $Z[4]\ge3$ and shift $4-(3+1)=0$ is reported. At index 6, the suffix begins `aba`, so $Z[6]=3$ and shift $2$ is reported. The other legal text starts have Z-values below 3.

**Conclusion.** Testing $Z[m+1+s]\ge m$ reports exactly shifts 0 and 2.

### Example 7

**Situation.** A developer builds `pattern + "$" + text`, but both operands may contain `$`.

Take pattern `a$` and text `a$`. The delimiter is not outside the alphabet, so the structural claim that prefix matches cannot cross the separator is false. Even if a particular output happens to be correct, the reduction proof no longer applies. Replacing the dollar-sign token with a fresh tagged object makes it unequal to every string symbol.

**Conclusion.** Separator freshness is a required precondition, not a stylistic convention.

### Example 8

**Situation.** A user searches for precomposed `é` in text containing `e` followed by a combining acute accent.

At the code-point level the pattern has one code point while the text fragment has two, so exact code-point matching reports no occurrence. If the product contract requires canonical equivalence, normalize both to NFC or both to NFD first. The normalized search may find a match, but its coordinates refer to transformed text unless the preprocessing layer records a projection to original offsets.

**Conclusion.** The algorithm can be correct while a user-visible search is semantically wrong. Normalization and coordinate projection belong in the contract.

### Example 9

**Situation.** Search a chunked stream for $P=\texttt{needle}$ when one chunk ends with `nee` and the next begins with `dle`.

Searching each chunk independently misses the occurrence. A naive streaming adapter retains the last $m-1=5$ symbols from the preceding processed prefix, prepends them to the next chunk, and translates local starts to absolute positions. It emits only starts not already finalized in an earlier window. If chunks contain encoded bytes, decoding must also preserve partial code units before sequence matching begins.

**Conclusion.** Correct streaming requires boundary state and coordinate accounting; invoking a correct resident matcher on isolated chunks is incomplete.

### Example 10

**Situation.** A benchmark reports that naive search is faster than a Python Z implementation on 32-byte ASCII messages. Should the service standardize on naive search?

First verify that the benchmark includes construction and result materialization for both implementations and uses the production runtime. Then add repeated-prefix adversarial inputs, realistic pattern-length distributions, match-heavy inputs, and maximum output. If the service enforces a 32-byte limit and the measured built-in or naive routine meets latency under every admitted input, the simpler choice can be justified. Without the hard bound, average measurements do not control the $\Theta(nm)$ adversary.

**Conclusion.** Selection combines theorem-backed worst-case limits with bounded, reproducible workload evidence; neither replaces the other.

## Cross-Program Connections

- **Data Structures Engineering:** compact arrays, ropes, piece tables, and compressed representations determine random-access and equality costs. See the [Data Structures Engineering roadmap](../../17-data-structures-engineering/ROADMAP.md).
- **Operating Systems:** memory mapping, page faults, read-ahead, and chunked I/O can dominate scans over large files. See the [Operating Systems roadmap](../../22-operating-systems/ROADMAP.md).
- **Programming Languages and Semantics:** string representation, equality, slicing, and index types are language-level semantic choices, not merely implementation details.
- **Data Engineering:** ingestion normalization, schema versions, and offset provenance determine whether stored sequences remain comparable and auditable.
- **Security Engineering:** canonicalization, resource caps, adversarial repetition, and result-volume limits are part of the attack surface.
- **API and Service Engineering:** an external search API must specify units, normalization, pagination, empty patterns, and stable coordinates.
- **Algorithms:** [ALGE-052](../ROADMAP.md#block-06--string-sequence-and-compression-algorithms) converts prefix-border structure into an online failure transition; ALGE-053 and ALGE-054 explore skip heuristics and fingerprints, while ALGE-055 and ALGE-056 index a text for repeated queries.

## References

1. Dan Gusfield, *Algorithms on Strings, Trees, and Sequences: Computer Science and Computational Biology*, Cambridge University Press, 1997, especially Part I, “Exact String Matching.” [Publisher record and DOI 10.1017/CBO9780511574931](https://doi.org/10.1017/CBO9780511574931). Retrieved 2026-09-05.
2. Maxime Crochemore, Christophe Hancart, and Thierry Lecroq, *Algorithms on Strings*, Cambridge University Press, 2007. [Publisher record and DOI 10.1017/CBO9780511546853](https://doi.org/10.1017/CBO9780511546853). Retrieved 2026-09-05.
3. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein, *Introduction to Algorithms*, 4th ed., MIT Press, 2022, Chapter 32, “String Matching.” [Publisher record](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/). Retrieved 2026-09-05.
4. Donald E. Knuth, James H. Morris Jr., and Vaughan R. Pratt, “Fast Pattern Matching in Strings,” *SIAM Journal on Computing* 6(2), 1977, pp. 323–350. [Primary paper and DOI 10.1137/0206024](https://doi.org/10.1137/0206024). Retrieved 2026-09-05. This is primary background for the successor module's prefix-failure method.
5. The Unicode Consortium, *The Unicode Standard*, Version 17.0.0, 2025. [Official versioned standard](https://www.unicode.org/versions/Unicode17.0.0/). Retrieved 2026-09-05.
6. The Unicode Consortium, “Unicode Normalization Forms,” Unicode Standard Annex #15, Revision 57, Unicode 17.0.0, 2025-07-30. [Official annex](https://www.unicode.org/reports/tr15/tr15-57.html). Retrieved 2026-09-05.

## Exercises

### Exercise 1

For $P=\texttt{aa}$ and $T=\texttt{aaaa}$, list every occurrence under overlapping semantics. Then state the results for an empty pattern under this chapter's policy and under a reject-empty API.

### Exercise 2

Let $S=\texttt{aaaaa}$. Compute $Z[1]$ through $Z[4]$. Identify how far the active right boundary can advance in total and explain why the many equal symbols do not make the Z algorithm quadratic.

### Exercise 3

An implementation uses an inclusive Z-box $[\ell,r]$ but initializes an inside-box position with `min(z[i-left], right-i)`. Diagnose the error, give a minimum input on which the bound is too small, and state the correction.

### Exercise 4

Design a search interface for normalized Unicode text that must return byte offsets into the original UTF-8 input. Specify sequence semantics, preprocessing, projection metadata, empty-pattern policy, and evidence needed to test the interface.

### Exercise 5

A telemetry service scans an unbounded event stream for a pattern of structured event types and must report overlaps with bounded memory. Decide whether the direct Z reduction is appropriate. Propose a design, state its invariants and resource limits, and describe how you would validate cross-chunk correctness and adversarial behavior.

## Answers to the Exercises

### Answer 1

The legal shifts for `aa` in `aaaa` are 0, 1, and 2, and all three match. The result is $(0,1,2)$; shift 1 is retained even though it overlaps both neighbors. Under this chapter's all-boundaries policy, an empty pattern in a length-four text reports $(0,1,2,3,4)$. A reject-empty API returns a declared error and no occurrence sequence. A correct answer must distinguish the two contracts rather than call one universally correct.

### Answer 2

The suffix beginning at 1 shares four `a` symbols with the prefix, so $Z[1]=4$. Similarly, $Z[2]=3$, $Z[3]=2$, and $Z[4]=1$. Processing $i=1$ can advance $r$ from $-1$ to 4. Later positions lie inside the box and their values are bounded by already exact prefix values and the remaining box length; they require no extension beyond 4. Across the entire run, $r$ advances at most $N-1=4$ positions. Repetition makes one extension long but cannot replenish the monotone right-boundary budget.

### Answer 3

For an inclusive box, the number of known positions from $i$ through $r$ is $r-i+1$, not $r-i$. The implementation underestimates the reusable prefix by one. On `aaa`, after processing $i=1$ the box is $[1,2]$. At $i=2$, one symbol is known inside the box, but `right-i` is zero. The result may remain correct because explicit comparisons redo work, yet the stated reuse mechanism and performance accounting are wrong; variants that do not extend correctly can also produce a wrong value. The correction is `min(z[i-left], right-i+1)`, followed by explicit extension and a consistent inclusive-box update.

### Answer 4

A model interface accepts well-formed UTF-8 bytes, decodes them under a declared error policy, normalizes both pattern and text to NFC as defined by a pinned Unicode version, and performs exact matching over Unicode scalar values. During decoding and normalization it builds a monotone projection from each normalized span boundary to the corresponding original byte span; because composition and decomposition are not always one-to-one, the return type should be byte ranges rather than assuming a single offset transform. Choose and document either all-boundaries or reject-empty behavior; reject-empty often avoids ambiguous zero-length projected spans.

Tests should cover precomposed and decomposed equivalents, combining-mark order, supplementary characters, invalid UTF-8, normalization length changes, matches crossing transformation segments, empty input, overlaps, and round-trip validation of every returned byte range. Conformance cases should be drawn from the Unicode normalization test data for the pinned version. Differential tests can compare the matcher on normalized sequences with a naive oracle. The evaluation criteria are explicit semantics, a total projection policy, versioned authoritative evidence, and boundary tests; merely calling a normalization library is insufficient.

### Answer 5

The direct $P\mathbin{\|}\bot\mathbin{\|}T$ Z reduction is not appropriate for an unbounded stream because its materialized input and Z-array grow with all observed text. Use an online prefix matcher such as KMP with $O(m)$ pattern state, or a naive window adapter retaining $m-1$ events if hard bounds make $O(nm)$ processing acceptable. Assign every event a monotonically increasing absolute index. The state invariant says the retained prefix state is exactly the longest pattern prefix that is a suffix of all events processed so far; emission does not discard that state, so overlaps remain possible.

Set hard limits for pattern length, event decoding size, per-event equality cost, result rate, queue depth, and processing time. Test by partitioning the same finite event sequence at every possible chunk boundary and comparing all outputs with a resident naive oracle. Add repeated-prefix patterns, all-match streams, malformed events, slow equality cases, backpressure, restart/checkpoint boundaries, and maximum-length patterns. A good design records the pattern version and absolute coordinate at checkpoints. Alternative bounded-state online algorithms are acceptable if they prove the same suffix-state invariant and preserve overlapping results.
