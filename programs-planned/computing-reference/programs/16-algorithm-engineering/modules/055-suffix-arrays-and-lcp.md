---
module_id: ALGE-055
program: Algorithm Engineering
level: 2
module_number: 55
title: Suffix Arrays and LCP
status: complete
last_verified: 2026-09-05
---

# Suffix Arrays and LCP

## One-Page Review

### Governing question

How can one immutable text be transformed into compact ordered arrays that support exact substring search, repeated-substring analysis, and longest-common-extension queries with explicit construction, comparison, and memory guarantees?

### Essential definitions

- The **suffix** at position $i$ is the half-open sequence $T[i:n]$.
- A **suffix array** $SA[0:n]$ is a permutation of text positions such that $T[SA[k]:n]$ is in nondecreasing lexicographic order.
- The **rank array** is the inverse permutation: $rank[SA[k]]=k$.
- The **LCP array** stores adjacent longest-common-prefix lengths: $LCP[0]=0$ and $LCP[k]=\operatorname{lcp}(T[SA[k-1]:],T[SA[k]:])$ for $k>0$.
- A **pattern interval** $[\ell,r)$ contains exactly the suffixes beginning with a pattern.
- A **longest common extension**, $LCE(i,j)$, is the common-prefix length of suffixes beginning at $i$ and $j$.
- A **sentinel** is a unique symbol ordered outside the text alphabet and used only under an explicit construction convention.

### Central model, mechanism, or theorem

Suffixes that begin with the same pattern form one contiguous interval in lexicographic order. Two boundary searches find that interval. For suffix ranks $a<b$,

$$
LCE(SA[a],SA[b])=\min_{a<k\le b}LCP[k].
$$

Thus $SA$ supports reusable ordered search; $SA$, inverse ranks, $LCP$, and a range-minimum-query structure support repeated LCE queries. Construction cost depends on the named algorithm and alphabet model. A direct suffix-slicing implementation is an executable oracle, not a scalable construction.

### Critical invariants

- $SA$ contains every integer from $0$ through $n-1$ exactly once.
- Adjacent suffixes are ordered under one stable symbol order.
- $rank$ is the exact inverse of $SA$.
- $0\le LCP[k]\le n-\max(SA[k-1],SA[k])$ for $k>0$.
- Pattern lower and upper bounds use compatible total-order keys.
- Text representation, normalization, sentinel, and collection separators cannot change after index construction.
- Positions, units, and version identifiers are preserved through persistence and queries.

### Common failures

Common failures include sorting materialized suffix copies; claiming every construction is linear; confusing suffix order with starting-position order; shifting the LCP convention; using locale collation instead of stable symbol order; mishandling empty text or empty patterns; appending a sentinel that also occurs in the input; letting collection matches cross document separators; allocating 32-bit offsets for larger texts; returning an unordered result while promising position order; and treating benchmark throughput as a proof of asymptotic complexity.

### Compact example

For `banana`, $SA=(5,3,1,0,4,2)$, ordering `a`, `ana`, `anana`, `banana`, `na`, `nana`. The adjacent $LCP$ values are $(0,1,3,0,0,2)$. Pattern `ana` occupies suffix ranks $[1,3)$ and occurs at text positions 3 and 1; sort those positions separately if the API promises text order. The maximum LCP value 3 identifies a longest repeated substring, `ana`.

### Connections

[ALGE-054](./054-rabin-karp-and-rolling-hashes.md) filters windows for one search; this module preprocesses a stable text for many ordered searches. [ALGE-056](../ROADMAP.md#block-06--string-sequence-and-compression-algorithms) studies suffix trees and automata. Data Structures Engineering supplies sorting, inverse permutations, and RMQ; Data Engineering owns stable text identity and collection framing.

## Governing Question

Given an immutable sequence and a workload of exact pattern, repeat, or suffix-comparison queries, how should we define, construct, validate, persist, and query a suffix array and its LCP array without hiding symbol-order assumptions, construction costs, or production failure modes?

A suffix array is small in definition—an ordered permutation of offsets—but not automatically cheap to build or use. Its engineering value comes from separating immutable text storage from integer index arrays and composing the order with LCP and range-minimum structures.

## Why This Matters

Scanning a text for every query repeats work. Sorting all suffixes once makes every occurrence of a pattern a contiguous range, supports repeat discovery through neighboring suffixes, and provides a foundation for compressed indexes and suffix-tree-like navigation.

The clean mathematical model can be compromised by implementation choices. Materialized suffixes can make an ostensibly simple sort quadratic in storage. Unicode normalization or collation changes can invalidate persisted order. Offset width, endianness, document boundaries, memory mapping, and output order affect whether an index remains correct when the corpus grows or moves.

Suffix arrays therefore teach a broader lesson: an index is a theorem plus a representation contract. The permutation and LCP identities prove query behavior only for the exact sequence and ordering that were indexed.

## Prerequisites and Retrieval

Retrieve lexicographic order, comparison sorting, stable integer encodings, binary-search loop invariants, inverse permutations, asymptotic analysis, range-minimum queries, and immutable snapshot identity. Complete [ALGE-051](./051-naive-and-prefix-based-pattern-matching.md) through [ALGE-054](./054-rabin-karp-and-rolling-hashes.md).

This chapter uses zero-based half-open slices. It defines a suffix array over the $n$ nonempty suffixes $T[i:n]$ for $0\le i<n$; some texts include the empty suffix at $n$. Either convention works, but arrays, proofs, and persisted formats must not mix them.

## Learning Objectives

After completing this module, you should be able to:

1. define suffix, suffix array, inverse rank, LCP, pattern interval, and LCE precisely;
2. construct and hand-check suffix and LCP arrays;
3. prove why pattern occurrences form one suffix-array interval;
4. derive Kasai's reuse rule and linear comparison bound;
5. distinguish naive, prefix-doubling, induced-sorting, and external-memory construction claims;
6. implement exact baseline construction, LCP computation, and pattern queries;
7. derive repeated-substring and distinct-substring results from LCP;
8. reduce LCE to range minimum over LCP;
9. design stable encodings, sentinels, separators, offset widths, and snapshot metadata; and
10. validate index invariants, query semantics, persistence, and performance independently.

## Core Exposition

### Fix the indexed sequence and its order

Let $T[0:n]$ be a finite sequence over a totally ordered alphabet $\Sigma$. Lexicographic comparison finds the first unequal symbols and compares them; if one sequence is a prefix of the other, the shorter sequence is smaller. The suffix at $i$ is $T[i:n]$.

The symbol order is part of the index format. Byte order is stable and simple. Unicode code-point order is stable after a named normalization policy, but it is not linguistic collation. Locale-sensitive collation can change across locale-data versions and may not give the prefix behavior expected by a code-point pattern query. Persist the encoding and normalization version with the text snapshot.

Some construction algorithms append a unique sentinel `$` smaller than every input symbol. This creates $T\$$ and makes every suffix distinct at a terminating symbol. The sentinel must be outside the admitted alphabet, occur exactly once, and be removed or translated consistently in the exported convention. It is not decorative punctuation.

### Define the suffix array as a permutation

A suffix array $SA[0:n]$ satisfies two properties:

1. it is a permutation of $0,1,\ldots,n-1$;
2. for every $0\le k<n-1$, $T[SA[k]:]\le_{lex}T[SA[k+1]:]$.

The inverse array $rank$ satisfies $rank[SA[k]]=k$. A permutation check catches missing and duplicate offsets; adjacent-order checks establish global sortedness because lexicographic order is transitive.

The array stores offsets, not suffix strings. If $n<2^{32}$, 32-bit offsets may suffice; larger snapshots require wider offsets or partitioning. The text remains necessary for comparisons unless a self-index or additional compressed representation owns reconstruction.

### Separate reference construction from scalable construction

The clearest oracle is `sorted(range(n), key=lambda i: text[i:])`. In Python this materializes or repeatedly handles suffix slices whose total length is $\Theta(n^2)$; comparison work can also be large. It is suitable for examples and differential tests, not a production complexity claim.

Prefix doubling begins with ranks for single symbols. At round $k$, sort suffixes by the pair

$$
(rank_k[i],rank_k[i+2^k]),
$$

using a distinguished rank for positions beyond $n$. Compress equal pairs into new integer ranks. Once all ranks differ, their order is the suffix order. There are $O(\log n)$ rounds. Comparison-sorting pairs yields $O(n\log^2 n)$ time; radix/counting sorting bounded integer ranks yields $O(n\log n)$ time with $O(n)$ auxiliary storage.

Linear-time constructions exist under explicit word-RAM or integer-alphabet assumptions, including difference-cover and induced-sorting families. “Suffix arrays build in linear time” is not a statement about an arbitrary library, comparison model, alphabet mapping, or external-memory workload. Name the algorithm, model, temporary space, and input transformation.

### Build LCP from inverse ranks

Define

$$
LCP[0]=0,\qquad LCP[k]=\operatorname{lcp}(T[SA[k-1]:],T[SA[k]:])\quad(k>0).
$$

Kasai's algorithm first constructs $rank$. It scans text positions $i$ in increasing order. If $rank[i]=0$, there is no lexicographic predecessor and the carried length is reset to zero. Otherwise let $j=SA[rank[i]-1]$. Starting from a carried lower bound $h$, compare $T[i+h]$ and $T[j+h]$, store the resulting $h$, then replace $h$ by $\max(h-1,0)$ before advancing $i$.

Why may one reuse $h-1$? If suffixes at $i$ and $j$ share $h$ symbols, suffixes at $i+1$ and $j+1$ share at least $h-1$. The lexicographic predecessor of suffix $i+1$ may be different, but its LCP with $i+1$ is at least that much: the suffix at $j+1$ is one witness on the appropriate side of the ordered suffixes. Each successful comparison increments $h$; each outer iteration decrements it at most once. Across the scan, total increments are $O(n)$, so LCP construction is $O(n)$ time after $SA$ is available.

### Search for a pattern interval

For pattern $P$, all suffixes beginning with $P$ are contiguous: if $P$ is a prefix of suffixes $A$ and $C$, then any suffix $B$ with $A\le B\le C$ cannot first differ from $P$ within its length without falling outside that order interval.

Find the first suffix whose length-$m$ prefix is not less than $P$, and the first whose prefix is greater than $P$. Their ranks form $[\ell,r)$. The baseline performs two binary searches and may inspect $O(m)$ symbols at each comparison, giving $O(m\log n)$ symbol comparisons plus $O(z)$ to enumerate $z=r-\ell$ results. LCP-aware search can reuse established prefix lengths and improve the comparison bound, but that improvement belongs only to the implemented variant.

Results emerge in suffix order, not numeric text-position order. Sorting the $z$ offsets adds $O(z\log z)$ comparison time; an API must state which order it promises.

### Reproduce the arrays and queries

This dependency-free Python uses the transparent suffix-slicing oracle for construction and Kasai's algorithm for LCP. Its construction is deliberately not scalable; it provides executable semantics and differential-test evidence.

<!-- bijux-verify: {"id":"suffix-array-lcp-reference","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"sa=(5, 3, 1, 0, 4, 2)\nlcp=(0, 1, 3, 0, 0, 2)\nana=(1, 3)\nlce_1_3=3\ndistinct=15\n","stderr":""}} -->
```python
def suffix_array(text):
    return tuple(sorted(range(len(text)), key=lambda i: text[i:]))


def lcp_array(text, sa):
    n = len(text)
    rank = [0] * n
    for k, start in enumerate(sa):
        rank[start] = k
    lcp = [0] * n
    h = 0
    for i in range(n):
        k = rank[i]
        if k == 0:
            h = 0
            continue
        j = sa[k - 1]
        while i + h < n and j + h < n and text[i + h] == text[j + h]:
            h += 1
        lcp[k] = h
        if h:
            h -= 1
    return tuple(lcp), tuple(rank)


def find_occurrences(text, sa, pattern):
    if not pattern:
        raise ValueError("empty-pattern policy is external")
    m = len(pattern)
    keys = [text[start : start + m] for start in sa]

    def lower_bound(target, upper):
        lo, hi = 0, len(sa)
        while lo < hi:
            mid = (lo + hi) // 2
            if keys[mid] < target or (upper and keys[mid] == target):
                lo = mid + 1
            else:
                hi = mid
        return lo

    left = lower_bound(pattern, False)
    right = lower_bound(pattern, True)
    return tuple(sorted(sa[left:right]))


def lce(i, j, rank, lcp):
    if i == j:
        return len(rank) - i
    a, b = sorted((rank[i], rank[j]))
    return min(lcp[a + 1 : b + 1])


text = "banana"
sa = suffix_array(text)
lcp, rank = lcp_array(text, sa)
print(f"sa={sa}")
print(f"lcp={lcp}")
print(f"ana={find_occurrences(text, sa, 'ana')}")
print(f"lce_1_3={lce(1, 3, rank, lcp)}")
print(f"distinct={len(text) * (len(text) + 1) // 2 - sum(lcp)}")
```

The code makes output ordering, empty-pattern policy, LCP indexing, and construction limitations visible. A production implementation should avoid the `keys` materialization and choose construction and query algorithms appropriate to its representation and workload.

### Derive repeated and distinct substrings

If a substring occurs at least twice, it is a prefix of at least two suffixes. Within the suffix-array interval sharing that prefix, some adjacent pair shares it. Therefore the maximum entry in $LCP$ is the length of a longest repeated substring; its neighboring suffix offsets locate witnesses.

There are $n(n+1)/2$ nonempty substring occurrences across all suffixes. In suffix order, suffix $SA[k]$ contributes $n-SA[k]$ prefixes, but its first $LCP[k]$ prefixes have already appeared as prefixes of earlier suffixes. Hence the number of distinct nonempty substrings is

$$
\sum_{k=0}^{n-1}(n-SA[k]-LCP[k])
=\frac{n(n+1)}2-\sum_{k=0}^{n-1}LCP[k].
$$

This counts symbol-sequence equality under the indexed representation, not linguistic words or normalization-equivalent strings unless the input policy made them identical first.

### Reduce LCE to range minimum

Let suffixes at ranks $a<b$ share $x$ symbols. Every adjacent pair between them must share at least those $x$ symbols; otherwise lexicographic order would separate the endpoints before position $x$. Conversely, if the minimum adjacent LCP in that rank interval is $x$, all suffixes in the interval share the first $x$ symbols, while the pair attaining the minimum prevents a longer common prefix. Therefore

$$
LCE(SA[a],SA[b])=\min LCP[a+1:b+1].
$$

A segment tree gives $O(\log n)$ RMQ after $O(n)$ construction. A sparse table gives $O(1)$ idempotent minimum queries with $O(n\log n)$ storage and preprocessing. Linear-space constant-query RMQ structures exist but are more complex. State the actual structure rather than saying “LCP makes LCE constant time.”

### Index collections without cross-document lies

Concatenating documents creates suffixes that cross boundaries. A pattern can then match the end of one document plus the beginning of another. Use unique ordered separators, boundary-aware verification, or a generalized suffix-array convention that preserves document identity and local offsets.

One unique separator per document may exhaust a small alphabet and complicate order. A shared separator plus a document-boundary table can work if comparisons stop at boundaries and the construction's equality/order rules are defined. Duplicate documents and empty documents require explicit IDs; offsets alone are not stable identities.

### Persist and validate the index

Persist a content digest or immutable generation ID, text length, alphabet/encoding version, normalization policy, sentinel/separator convention, offset width, byte order, array lengths, construction algorithm/version, and checksums. Load into a quarantined state, validate metadata and bounds, sample or fully check permutation and order according to risk, and expose queries only after acceptance.

Construction needs peak-space accounting for text, $SA$, ranks, temporary sort keys, $LCP$, RMQ, and serialization buffers. External-memory algorithms must count scans, random I/O, merge runs, and restart artifacts. A memory-mapped final array does not erase peak build memory.

## Definitions and Notation

Let $T\in\Sigma^n$ under a fixed total order and let positions be zero-based.

- $S_i=T[i:n]$ is the suffix starting at $i$.
- $SA[k]$ is the start position of the suffix at lexicographic rank $k$.
- $rank[i]$ is the rank of suffix $S_i$ and is the inverse of $SA$.
- $\operatorname{lcp}(X,Y)$ is the length of the longest sequence that is a prefix of both $X$ and $Y$.
- $LCP[0]=0$ and $LCP[k]=\operatorname{lcp}(S_{SA[k-1]},S_{SA[k]})$ for $k>0$.
- $[\ell,r)$ is a pattern interval in suffix-rank coordinates.
- $z=r-\ell$ is the number of reported occurrences before any deduplication or limit.
- $LCE(i,j)=\operatorname{lcp}(S_i,S_j)$.
- $RMQ(A,p,q)$ returns the minimum array value over a declared half-open or closed range; this chapter writes the exact slice instead of relying on an implicit convention.

Complexity statements distinguish symbol comparisons, word operations, bytes, I/O, preprocessing, query work, and output. The fixed-word model requires offsets and ranks to fit the selected word type.

## Mechanisms, Invariants, or Proof Structure

### Suffix-array validity theorem

**Theorem.** If $SA$ is a permutation of $0,\ldots,n-1$ and every adjacent suffix pair is nondecreasing, then $SA$ lists every suffix exactly once in lexicographic order.

**Proof.** The permutation condition establishes exact coverage. Lexicographic order is transitive, so adjacent nondecreasing relations imply $S_{SA[a]}\le S_{SA[b]}$ for all $a<b$. $\square$

### Pattern-interval theorem

**Theorem.** Suffixes beginning with a fixed nonempty pattern $P$ occupy a contiguous interval in $SA$.

**Proof.** Take matching suffixes $A<C$ and a suffix $B$ with $A\le B\le C$. If $B$ first differs from $P$ before $|P|$, a smaller symbol puts $B<A$ and a larger symbol puts $B>C$. If $B$ ends first, it is smaller than both matching suffixes. Each case contradicts its position, so $P$ prefixes $B$. $\square$

### Kasai reuse lemma

**Lemma.** If $LCE(i,j)=h>0$, then $LCE(i+1,j+1)\ge h-1$ whenever both shifted suffixes exist.

**Proof.** Equality $T[i:i+h]=T[j:j+h]$ remains equality after deleting the first symbol, leaving $h-1$ equal symbols. $\square$

In Kasai's scan, $j$ is the lexicographic predecessor of $i$. The shifted witness $j+1$ shows that the best adjacent predecessor/successor relation relevant to suffix $i+1$ preserves at least $h-1$. The algorithm compares only beyond that established prefix. Since the carried $h$ decreases at most once per outer iteration, its total successful increments are $O(n)$.

### LCE-RMQ theorem

**Theorem.** For suffix ranks $a<b$, $LCE(SA[a],SA[b])=\min_{a<k\le b}LCP[k]$.

**Proof.** Let the minimum be $x$. Every adjacent pair from rank $a$ through $b$ agrees on its first $x$ symbols, so by transitivity of equality the endpoints agree for $x$. An adjacent pair attaining the minimum disagrees or ends at the next symbol, and lexicographic contiguity prevents both endpoints from sharing a longer prefix across that boundary. Thus their LCE is exactly $x$. $\square$

### Validation invariants

For a trusted snapshot:

1. lengths of $SA$, $rank$, and $LCP$ are $n$;
2. $SA$ is a bounded permutation and $rank[SA[k]]=k$;
3. adjacent suffixes are ordered under the persisted representation;
4. every $LCP[k]$ equals the adjacent common-prefix length and lies within both suffix lengths;
5. binary-search boundaries partition suffixes into less-than, matching, and greater-than regions;
6. every reported occurrence passes direct pattern equality and document-boundary policy;
7. the text generation and encoding metadata match the index.

Full adjacent checks can be expensive because naive suffix comparisons repeat prefixes. Differential tests on small texts, construction-specific certificates, sampled production checks, checksums, and end-to-end query verification provide different evidence and must be labeled separately.

## Alternatives and Trade-Offs

| Design | Build | Query | Space character | Best fit | Main limitation |
|---|---:|---:|---|---|---|
| Direct scan | none | $O(n+m)$ | minimal | few queries, changing text | repeats work |
| Naive suffix sort | potentially quadratic or worse in processed symbols | baseline $O(m\log n+z)$ | may materialize $\Theta(n^2)$ symbols | oracle and tiny fixtures | not scalable |
| Prefix doubling | $O(n\log^2 n)$ comparison sort or $O(n\log n)$ radix rounds | same suffix-array query | $O(n)$ words plus temporaries | straightforward engineering | multiple full-array rounds |
| Linear suffix construction | $O(n)$ under named assumptions | same suffix-array query | algorithm-specific | very large stable text | complexity and constants |
| Suffix tree | algorithm-specific linear construction exists | $O(m+z)$ exact traversal | pointer/topology heavy | rich online navigation | complex representation |
| FM/compressed index | construction-specific | often near $O(m+z)$ with factors | compressed/self-indexing | large repetitive corpora | engineering and locate costs |
| Inverted index | tokenization dependent | efficient token queries | posting lists | word/document retrieval | not arbitrary substrings |

Suffix arrays are compelling when text is stable, arbitrary substring queries recur, integer arrays fit the storage hierarchy, and exact positions matter. Direct scanning wins for small or frequently changing data. Compressed indexes win when text and raw arrays exceed memory or reconstruction is required.

## Failure Modes and Misconceptions

1. **“The suffix array stores suffixes.”** It normally stores offsets into separately owned immutable text.
2. **“Sorting suffix slices is $O(n\log n)$.”** Slice creation and comparison can process quadratic total symbols.
3. **“Suffix-array construction is linear.”** Only named algorithms under stated machine and alphabet assumptions earn that bound.
4. **“LCP[k] belongs to text position $k$.”** It belongs to suffix rank $k$ and its predecessor.
5. **“Binary search returns positions in text order.”** It returns a suffix-order interval; numeric sorting is extra work.
6. **“LCP alone gives constant-time LCE.”** It also needs inverse ranks and a suitable RMQ structure.
7. **“A maximum LCP value identifies a unique repeat.”** Multiple pairs and substrings can tie.
8. **“A separator prevents cross-document matches automatically.”** Only if it is outside patterns and comparison/boundary semantics enforce it.
9. **“Unicode strings have one obvious order.”** Bytes, code points, normalization, graphemes, and collation are distinct policies.
10. **“A persisted index can follow mutable text.”** Any byte, symbol, or policy change invalidates offsets and order.
11. **“32-bit offsets are always smaller and sufficient.”** Overflow silently corrupts indexes beyond their range.
12. **“A successful sample proves the permutation.”** Sampling is evidence, not exhaustive certification.

## Worked Examples

### Example 1

**Situation.** Construct $SA$ for `banana`.

List suffixes with offsets: `banana` at 0, `anana` at 1, `nana` at 2, `ana` at 3, `na` at 4, and `a` at 5. Lexicographic order is `a`, `ana`, `anana`, `banana`, `na`, `nana`.

**Conclusion.** $SA=(5,3,1,0,4,2)$; these numbers are offsets in suffix order, not sorted positions.

### Example 2

**Situation.** Compute the adjacent LCP array for `banana`.

The first entry is 0 by convention. Adjacent common prefixes have lengths 1 for `a`/`ana`, 3 for `ana`/`anana`, 0 for `anana`/`banana`, 0 for `banana`/`na`, and 2 for `na`/`nana`.

**Conclusion.** $LCP=(0,1,3,0,0,2)$ under the predecessor-at-$k-1$ convention.

### Example 3

**Situation.** Search `ana` in the suffix array of `banana`.

Suffix prefixes less than `ana` end before rank 1. Ranks 1 and 2 begin with `ana`; rank 3 begins with `ban`, which is greater. The interval is $[1,3)$ and its offsets are $(3,1)$ in suffix order.

**Conclusion.** Occurrences are positions 1 and 3; returning $(1,3)$ requires separate numeric ordering.

### Example 4

**Situation.** Compute $LCE(1,3)$ in `banana` using RMQ.

$rank[1]=2$ and $rank[3]=1$. Take the minimum over $LCP[2:3]$, which is 3. Directly, `anana` and `ana` share `ana` before the shorter suffix ends.

**Conclusion.** $LCE(1,3)=3$, and the queried LCP range excludes the lower rank and includes the upper rank.

### Example 5

**Situation.** Count distinct nonempty substrings of `banana`.

There are $6\cdot7/2=21$ substring occurrences. Adjacent LCP values sum to $0+1+3+0+0+2=6$, representing prefixes already introduced by earlier suffixes. Thus $21-6=15$ distinct substrings remain.

**Conclusion.** `banana` has 15 distinct nonempty substrings under code-point equality.

### Example 6

**Situation.** Find a longest repeated substring.

The maximum LCP value is 3 between suffixes at offsets 3 and 1. Their first three symbols are `ana`. No adjacent suffix pair shares four symbols, so no substring of length four occurs twice.

**Conclusion.** `ana` is a longest repeated substring, with witnesses at positions 1 and 3.

### Example 7

**Situation.** Validate a purported suffix array $(5,3,1,0,2,2)$ for `banana`.

All values are in range, but offset 2 occurs twice and offset 4 is absent. It is not a permutation. Order checks alone could miss the lost suffix if only the listed pairs were inspected.

**Conclusion.** Bounds, uniqueness, coverage, and order are independent validation obligations.

### Example 8

**Situation.** Index two documents `ab` and `cd` by concatenating them as `abcd`.

Pattern `bc` appears at offset 1 in the concatenated sequence but in neither document. Insert an excluded separator or retain boundary metadata and reject any match whose half-open range crosses a document end.

**Conclusion.** Concatenation changes the language of valid substrings unless boundaries participate in index semantics.

### Example 9

**Situation.** Estimate storage for $n=10^9$ symbols using 64-bit $SA$ and LCP entries.

Each array needs $8\times10^9$ bytes, about 8 GB decimal or 7.45 GiB. Together they need about 16 GB decimal before inverse ranks, RMQ, text, temporary construction arrays, allocator overhead, or checksums.

**Conclusion.** Linear space is not small space; peak resident and external-memory costs must be budgeted in bytes.

### Example 10

**Situation.** A service rebuilds an index after changing Unicode normalization but reuses the old text digest and offsets.

Normalization can change symbol count and equality, so old offsets may identify different slices and old suffix order may be invalid. The build must create a new immutable text generation, record the policy version, validate the new arrays, and atomically switch readers.

**Conclusion.** Representation policy is part of indexed identity, not query-time decoration.

## Cross-Program Connections

- **Data Structures Engineering:** permutations, sorting, segment trees, sparse tables, and succinct structures determine construction and LCE trade-offs. See the [Data Structures Engineering roadmap](../../17-data-structures-engineering/ROADMAP.md).
- **Database Engineering:** suffix arrays are immutable secondary indexes; snapshot identity, build publication, corruption checks, and query ordering mirror database index concerns.
- **Data Engineering:** canonical encoding, document framing, corpus generations, lineage, and rebuilds determine whether offsets remain meaningful.
- **Operating Systems:** memory mapping, page locality, offset width, byte order, and external sorting dominate large-index behavior.
- **Security Engineering:** malformed index files, integer overflow, adversarial repeated prefixes, resource exhaustion, and untrusted query output require bounds and validation.
- **API and Service Engineering:** empty-pattern semantics, result ordering, pagination, snapshot version, units, and truncation must be explicit contracts.
- **Algorithms:** [ALGE-054](./054-rabin-karp-and-rolling-hashes.md) handles transient window filtering, while [ALGE-056](../ROADMAP.md#block-06--string-sequence-and-compression-algorithms) develops richer suffix representations.

## References

1. Udi Manber and Gene Myers, “Suffix Arrays: A New Method for On-Line String Searches,” *SIAM Journal on Computing* 22(5), October 1993, pp. 935–948. [Official publisher record and DOI 10.1137/0222058](https://doi.org/10.1137/0222058). Retrieved 2026-09-05.
2. Toru Kasai, Gunho Lee, Hiroki Arimura, Setsuo Arikawa, and Kunsoo Park, “Linear-Time Longest-Common-Prefix Computation in Suffix Arrays and Its Applications,” *CPM 2001*, LNCS 2089, pp. 181–192. [Official publisher record and DOI 10.1007/3-540-48194-X_17](https://doi.org/10.1007/3-540-48194-X_17). Retrieved 2026-09-05.
3. Juha Kärkkäinen and Peter Sanders, “Simple Linear Work Suffix Array Construction,” *ICALP 2003*, LNCS 2719, pp. 943–955. [Official publisher record and DOI 10.1007/3-540-45061-0_73](https://doi.org/10.1007/3-540-45061-0_73). Retrieved 2026-09-05.
4. Ge Nong, Sen Zhang, and Wai Hong Chan, “Linear Suffix Array Construction by Almost Pure Induced-Sorting,” *Data Compression Conference 2009*, pp. 193–202. [Official IEEE DOI 10.1109/DCC.2009.42](https://doi.org/10.1109/DCC.2009.42). Retrieved 2026-09-05.
5. Dan Gusfield, *Algorithms on Strings, Trees, and Sequences*, Cambridge University Press, 1997, Parts I–II. [Official publisher record and DOI 10.1017/CBO9780511574931](https://doi.org/10.1017/CBO9780511574931). Retrieved 2026-09-05.

## Exercises

### Exercise 1

Using the no-empty-suffix convention, construct $SA$ and $LCP$ for `abab`. State the exact LCP indexing convention.

### Exercise 2

Use inverse ranks and an LCP range minimum to compute $LCE(0,2)$ and $LCE(1,3)$ for `abab`. Show the rank interval used in each query.

### Exercise 3

A Python implementation builds `sorted(text[i:] for i in range(n))` and claims $O(n\log n)$ construction and $O(n)$ storage. Diagnose the claim and design a differential-test oracle that preserves offsets.

### Exercise 4

Design an immutable suffix-array service for a 12-billion-byte corpus. Specify representation, construction family, offset width, publication protocol, query semantics, validation, and resource limits.

### Exercise 5

Design a generalized suffix-array analysis that finds the longest substring occurring in at least three distinct documents without allowing cross-boundary matches. State the window/LCP condition and production evidence.

## Answers to the Exercises

### Answer 1

The suffixes are `abab` at 0, `bab` at 1, `ab` at 2, and `b` at 3. Ordered suffixes are `ab` (2), `abab` (0), `b` (3), and `bab` (1), so $SA=(2,0,3,1)$.

This chapter defines $LCP[0]=0$ and, for $k>0$, compares suffix ranks $k-1$ and $k$. The adjacent lengths are 2 for `ab`/`abab`, 0 for `abab`/`b`, and 1 for `b`/`bab`, so $LCP=(0,2,0,1)$.

### Answer 2

The inverse ranks are $rank[0]=1$, $rank[1]=3$, $rank[2]=0$, and $rank[3]=2$. For positions 0 and 2, the ordered ranks are 0 and 1, so take $\min LCP[1:2]=2$; indeed `abab` and `ab` share `ab`.

For positions 1 and 3, ranks are 3 and 2, so take $\min LCP[3:4]=1$; `bab` and `b` share `b`. Thus $LCE(0,2)=2$ and $LCE(1,3)=1$.

### Answer 3

The code materializes $n$ suffix strings whose lengths sum to $n+(n-1)+\cdots+1=\Theta(n^2)$ symbols. Sorting performs comparisons that may rescan long common prefixes, so neither the stated time nor storage follows from the $n$-item comparison-sort bound. It also loses original offsets when equal-looking objects or transformed representations are involved.

For a small oracle, retain the original immutable sequence and compute `sorted(range(n), key=lambda i: text[i:])`. Validate permutation and adjacent order. Generate exhaustive short sequences over a tiny alphabet and compare a production constructor's offsets with the oracle. Derive LCP by direct adjacent comparison and compare it with the production LCP. Include empty text, one symbol, all equal, all distinct, periodic strings, long common prefixes, sentinels, maximum symbols, and normalization fixtures. The oracle is intentionally quadratic-scale evidence and must be bounded to small inputs.

### Answer 4

Twelve billion offsets do not fit unsigned 32-bit values, so use validated 64-bit offsets and an immutable byte representation. Record corpus digest/generation, length, symbol order, construction algorithm/version, offset width, endianness, array checksums, and build parameters. Choose an external-memory or distributed construction whose I/O, temporary storage, restart, and alphabet assumptions match available resources; do not infer feasibility from asymptotic linear space.

Build beside the active generation, checkpoint merge/induction stages atomically, and never expose partial arrays. Validate file sizes and checksums, bounded permutation properties, construction certificates or full checks appropriate to the implementation, differential samples, direct verification of query results, and crash recovery. Publish metadata and files under one generation pointer, keep the prior generation for rollback, and reject mixed text/index generations.

Define byte-pattern input, reject or explicitly define empty patterns, return snapshot ID and either suffix or numeric position order, paginate with a stable rank cursor, bound pattern length, result count, CPU, I/O, and concurrent mappings, and distinguish truncated from complete results. Test repeated-prefix adversarial corpora, absent/present patterns, first/last suffix ranks, 64-bit boundary fixtures, corrupt files, partial publication, cancellation, and rollback.

### Answer 5

Concatenate canonical document sequences with excluded separators or retain boundary metadata that terminates suffix comparisons at document ends. Store a document ID and local offset for every suffix. In suffix order, consider windows that contain suffixes from at least three distinct document IDs. The common prefix of every suffix in ranks $[a,b]$ has length $\min LCP[a+1:b+1]$; maximize this minimum over qualifying windows, shrinking redundant endpoints to search efficiently. Cap the candidate length at every involved document boundary so separators or following documents cannot contribute.

Return the substring plus at least three document/offset witnesses, and directly verify each slice in its immutable source generation. Handle duplicate documents according to whether identity means document ID or distinct content. Evidence includes differential comparison with exhaustive substring enumeration on small document sets, repeated-document and empty-document cases, separator-like input, ties, normalization differences, long common prefixes, window-boundary cases, randomized corpora, corrupt metadata, restart, and result limits. A valid answer may use a suffix-tree or document-array formulation if it states the same distinct-document, boundary, and verification invariants.
