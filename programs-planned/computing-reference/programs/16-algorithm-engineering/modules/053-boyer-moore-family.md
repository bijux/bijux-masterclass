---
module_id: ALGE-053
program: Algorithm Engineering
level: 2
module_number: 53
title: Boyer-Moore Family
status: complete
last_verified: 2026-09-05
---

# Boyer-Moore Family

## One-Page Review

### Governing question

How do right-to-left comparisons and proof-backed shifts let Boyer-Moore-family matchers skip text positions, and which guarantees survive in the full algorithm and its simplified variants?

### Essential definitions

- An **alignment** places pattern $P[0:m]$ over text window $T[s:s+m]$ at shift $s$.
- A **right-to-left scan** compares $P[m-1]$ first and decreases index $j$ while symbols agree.
- The **bad-character rule** uses mismatching text symbol $x=T[s+j]$ to align a viable occurrence of $x$ in the pattern or move it past the pattern.
- The **matched suffix** is $u=P[j+1:m]$, already equal to the aligned text suffix when mismatch occurs at $j$.
- The **good-suffix rule** realigns another compatible occurrence of $u$, or a prefix of $P$ matching a suffix of $u$.
- A **safe shift** eliminates only alignments that cannot be occurrences under facts already observed.
- **Horspool** uses one table indexed by the symbol under the pattern's last position.
- **Sunday/Quick Search** uses the symbol immediately after the current window.
- The **Galil rule** remembers a verified region so a suitable Boyer-Moore variant avoids re-comparing it and obtains a linear worst-case bound.

### Central model, mechanism, or theorem

After a mismatch at pattern position $j$, choose

$$
\Delta=\max(1,\Delta_{\mathrm{bad}}(j,x),
\Delta_{\mathrm{good}}(j))
$$

for correctly constructed tables. Each component proves that all smaller positive shifts it excludes are impossible. The algorithm moves alignment start to $s+\Delta$ without reading the skipped starts. Favorable data can therefore require fewer than $n$ text inspections, but family members have different preprocessing, worst-case, memory, and streaming properties.

### Critical invariants

- Text units, equality, empty-pattern policy, overlap policy, and coordinates match ALGE-051.
- At alignment $s$, positions $j+1$ through $m-1$ have matched before a mismatch at $j$.
- Every skipped shift contradicts the mismatch symbol, the matched suffix, or both.
- The shift is always at least one and arithmetic cannot overflow.
- Full-match shifting retains overlaps through a pattern border or variant-specific safe rule.
- A table is derived from the exact immutable pattern and alphabet/equality policy.
- Complexity claims name the precise variant; no simplified rule inherits another variant's theorem by resemblance.

### Common failures

Common failures include scanning left-to-right while applying right-to-left shifts; using the rightmost bad character even when it lies to the right of $j$ without clamping; shifting zero; omitting the good-suffix prefix fallback; losing overlaps after a full match; reading beyond the text for Sunday; treating Horspool as worst-case linear; claiming sublinear elapsed time rather than sublinear inspected positions; using a dense huge-alphabet table; applying random-access algorithms to streams without buffering; and reusing tables after pattern mutation.

### Compact example

Let $P=\texttt{NEEDLE}$ and suppose a mismatch at its last position observes `A`. Since `A` does not occur in $P$, the bad-character rule can move the pattern past that text symbol, shifting six positions. A left-to-right matcher could not justify the same jump before examining the window. If the observed symbol were `E`, its rightmost useful occurrence would limit the safe shift.

### Connections

[ALGE-052](./052-knuth-morris-pratt.md) uses failure links and never backs up a stream; this module instead exploits resident random access and skips alignments. [ALGE-054](../ROADMAP.md#block-06--string-sequence-and-compression-algorithms) uses rolling fingerprints to filter candidate windows. Data Structures Engineering owns table representation, Computer Architecture owns cache and vector behavior, and Security Engineering owns adversarial-work limits.

## Governing Question

For exact single-pattern search over resident text, how can information learned near the right edge of an alignment prove that multiple future alignments are impossible, and how should an engineer distinguish full Boyer-Moore, Galil-corrected bounds, Horspool, Sunday, and runtime-specific hybrids?

The name “Boyer-Moore” is often applied loosely to any matcher that scans a window backward and shifts by a table. That obscures correctness and complexity. A production decision must name the rules actually implemented, their preprocessing convention, their full-match behavior, and the theorem that applies to that exact variant.

## Why This Matters

KMP guarantees a linear sequential scan, but it examines the text in order. Boyer-Moore's distinctive advantage is the ability to inspect a symbol near a window's right edge and rule out several alignment starts. Over large alphabets and sufficiently long patterns, this can reduce inspected text positions dramatically.

That advantage depends on resident random access, useful mismatch distributions, table locality, and cheap symbol comparisons. Short patterns, tiny alphabets, repetitive data, transformation layers, or cache-unfriendly tables can erase it. Simplified variants are popular precisely because lower setup and simpler inner loops may outperform theoretically richer rules on selected workloads.

The family is an ideal case study in honest algorithm engineering: correctness derives from safe-shift proofs, while performance requires variant-specific worst-case analysis and measurement. “Usually fast” and “worst-case linear” are different claims.

## Prerequisites and Retrieval

Retrieve exact occurrence semantics, overlapping results, borders, KMP failure links, resident versus streaming ownership, amortized bounds, and adversarial families. Complete [ALGE-051](./051-naive-and-prefix-based-pattern-matching.md) and [ALGE-052](./052-knuth-morris-pratt.md).

This chapter assumes nonempty patterns for the search loops. An external API may use the finite all-boundaries empty policy from ALGE-051 or reject empty patterns, but preprocessing and result behavior must agree.

## Learning Objectives

After completing this module, you should be able to:

1. trace a right-to-left alignment and identify all observed facts;
2. derive a bad-character shift and prove it safe;
3. state the strong good-suffix alternatives;
4. combine independently safe shifts correctly;
5. distinguish full Boyer-Moore, Galil, Horspool, and Sunday variants;
6. construct quadratic cases for simplified variants;
7. implement and validate an overlap-preserving Horspool matcher;
8. choose dense, sparse, or hybrid shift tables;
9. assess resident, streaming, cache, and output constraints; and
10. benchmark variants without generalizing beyond the evidence.

## Core Exposition

### Reverse the comparison direction

At alignment $s$, compare $P[j]$ with $T[s+j]$ beginning at $j=m-1$. If they agree, decrement $j$. Reaching $j<0$ proves an occurrence at $s$. Otherwise the comparison has established two facts:

1. $x=T[s+j]\ne P[j]$;
2. $T[s+j+1:s+m]=P[j+1:m]$.

The second fact is a matched suffix. A safe shift can exploit either the mismatching symbol, the suffix, or both. The algorithm's power comes from proving that some nearby alignments cannot satisfy these facts simultaneously.

### Derive the bad-character rule

Suppose mismatch symbol $x$ occurs in $P[0:j]$. Let $k<j$ be its rightmost occurrence there. Shifting by $j-k$ aligns $P[k]=x$ with the observed text symbol. Any smaller shift would align $x$ with a pattern position between $k$ and $j$, where $x$ does not occur, so such an alignment cannot match.

If $x$ does not occur left of $j$, shift by $j+1$ to move the pattern start beyond the observed symbol. A common table stores only the last occurrence of each symbol anywhere in the pattern and computes

$$
\Delta_{\mathrm{bad}}=\max(1,j-\operatorname{last}(x)).
$$

When `last(x)` lies right of $j$, this table cannot justify a useful positive shift, so clamping to one preserves correctness. Position-specific tables can recover the strongest left-of-$j$ occurrence at greater preprocessing cost.

### Derive the strong good-suffix rule

Let $u=P[j+1:m]$ be the matched nonempty suffix. A candidate shifted occurrence must place some pattern substring over that observed text copy of $u$.

First seek a rightmost earlier occurrence $P[k:k+|u|]=u$ whose preceding pattern symbol, when present, differs from $P[j]$. The differing predecessor is the **strong** condition: aligning an occurrence preceded by the same mismatching pattern symbol would immediately recreate the known mismatch. Shift so this compatible copy covers the observed suffix.

If no compatible full copy exists, find the longest suffix of $u$ that is also a prefix of $P$ and align that prefix with the end of the observed suffix. If even that is empty, move the complete pattern past the suffix. Preprocessing compiles these choices into a good-suffix table indexed by mismatch position.

After a full match there is no mismatch position. To preserve overlaps, align the longest proper border of $P$ with its matched suffix, shifting by $m-b$ where $b$ is the longest border length. A non-overlap-only interface may choose a larger shift, but it implements a different result contract.

### Combine rules

If one proof says shifts $1$ through $a-1$ are impossible and another says shifts $1$ through $b-1$ are impossible, every shift below $\max(a,b)$ is impossible. Thus full Boyer-Moore chooses the maximum of one, the bad-character shift, and the good-suffix shift.

Adding safe lower bounds by summation is not justified: the rules may eliminate overlapping sets of shifts, not consecutive independent distances. Taking the minimum throws away a valid optimization but remains safe if it stays positive; taking an unsupported larger value can miss occurrences.

### Understand Horspool

Horspool simplifies the family to one shift table. Set the default shift to $m$. For each pattern position $i=0,\dots,m-2$, set

$$
H[P[i]]=m-1-i.
$$

Later assignments retain the rightmost occurrence before the pattern's final position. Compare the window right-to-left. Whether it matches or mismatches, shift by $H[T[s+m-1]]$, using $m$ when the window's final symbol is absent from the table.

Why is this safe? The observed final-window symbol must align with some occurrence before the pattern's last position in any intervening candidate alignment; the rightmost such occurrence gives the smallest possible positive displacement. If none exists, no start inside the next $m-1$ positions can match.

Horspool can shift far on diverse alphabets, but its worst case is quadratic. For $P=ba^{m-1}$ and $T=a^n$, each alignment matches $m-1$ symbols from the right, fails on `b`, and shifts only one because the final-window `a` has shift one. The comparison count is $m(n-m+1)$.

### Understand Sunday/Quick Search

Sunday's Quick Search examines the symbol $y=T[s+m]$ immediately after the current window when another alignment remains. A match beginning at any shift from $s+1$ through $s+m$ must align some pattern occurrence of $y$ with this known text position. If the rightmost occurrence is at pattern index $k$, shift $m-k$; if absent, shift $m+1$.

The rule is independent of comparison order within the current window. It requires a bounds check when $s+m=n$; there is no following symbol, so the search must terminate after classifying the last legal alignment. Like Horspool, simplified Quick Search does not automatically inherit a worst-case linear theorem.

### Separate the Galil guarantee

Repeated matches can cause a classical implementation to compare a region already proved equal. Galil's 1979 modification records a verified interval and avoids re-comparing it after certain shifts, establishing linear worst-case behavior for the modified Boyer-Moore strategy even when multiple occurrences exist.

This guarantee belongs to a precisely specified variant and proof. An implementation with only Horspool's table, only Sunday's table, or an informal “Galil optimization” cannot claim it. Record comparison counts under adversarial tests in addition to wall time.

### Reproduce an overlap-preserving Horspool variant

This dependency-free program implements Horspool over immutable Python tuples, records comparison counts, and exposes both its favorable skip and a quadratic family.

<!-- bijux-verify: {"id":"horspool-search-and-adversary","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"shifts={'a': 2, 'b': 1} default=3\nmatches=(0, 2) comparisons=6\nadversarial_matches=() comparisons=28\n","stderr":""}} -->
```python
def compile_horspool(pattern):
    pattern = tuple(pattern)
    if not pattern:
        raise ValueError("Horspool requires a nonempty pattern")
    shifts = {}
    m = len(pattern)
    for i in range(m - 1):
        shifts[pattern[i]] = m - 1 - i
    return pattern, shifts


def horspool_search(pattern, text):
    pattern, shifts = compile_horspool(pattern)
    text = tuple(text)
    m, n = len(pattern), len(text)
    starts = []
    comparisons = 0
    alignment = 0
    while alignment <= n - m:
        j = m - 1
        while j >= 0:
            comparisons += 1
            if pattern[j] != text[alignment + j]:
                break
            j -= 1
        if j < 0:
            starts.append(alignment)
        alignment += shifts.get(text[alignment + m - 1], m)
    return tuple(starts), comparisons


pattern, shifts = compile_horspool("aba")
print(f"shifts={shifts} default={len(pattern)}")
matches, comparisons = horspool_search("aba", "ababa")
print(f"matches={matches} comparisons={comparisons}")
bad_matches, bad_comparisons = horspool_search("baaa", "aaaaaaaaaa")
print(f"adversarial_matches={bad_matches} comparisons={bad_comparisons}")
```

The table gives `a` shift two and `b` shift one; `a` at the pattern's final position is intentionally excluded. The adversarial case has $m=4$ and seven alignments, each doing four comparisons, for 28 total. This execution demonstrates one implementation and input family, not universal relative performance.

### Choose table representation

For bytes, a fixed array of 256 integers is compact, predictable, and avoids hashing. For Unicode code points or arbitrary records, a dense alphabet table is wasteful; use a map containing only pattern symbols plus a default. A hybrid may use a small array for a common range and a map for others.

Table width must represent shifts through $m$ or $m+1$ for Sunday. Validate conversions and addition near maximum input size. Untrusted user-defined equality or hashing can violate constant-time assumptions or trigger application code; restrict symbol types at trust boundaries.

Pattern and tables form one immutable compiled object. Pattern mutation, normalization-policy changes, locale changes, or equality-version changes require recompilation. Per-search result and cancellation state should not live in a shared compiled table.

### Respect random-access ownership

Boyer-Moore-family algorithms jump among resident text positions. Applying them to a stream requires buffering at least a window and any lookahead the rule reads. Skipped alignments do not mean skipped I/O: bytes still must arrive or be read from storage. KMP is generally a cleaner streaming abstraction.

For memory-mapped files, far shifts may reduce comparisons yet interact with page faults and readahead. Packed or variable-width encodings complicate constant-time indexing. Benchmark the actual representation and include decoding, normalization, mapping, and output costs.

### Validate variants and claims

Use the naive matcher as an oracle over exhaustive short alphabets. Include empty and one-symbol patterns under policy, $m>n$, exact-length text, overlaps, repeated symbols, deep borders, symbols absent from the pattern, mismatch at every $j$, and the last legal window.

For each skip, a diagnostic build can enumerate the omitted starts and assert none matches. This does not replace the proof, but localizes table defects. Differentially compare full Boyer-Moore, Horspool, Sunday, KMP, and the host runtime on identical semantics.

Benchmark at least pattern length, alphabet size, symbol distribution, match density, repetition, corpus size, table build, one-shot versus reuse, cold/warm cache, result handling, and adversarial inputs. Report text positions inspected and symbol comparisons alongside elapsed time. A matcher can inspect sublinear positions on a favorable instance while end-to-end ingestion remains $\Omega(n)$.

## Definitions and Notation

Let $P\in\Sigma^m$ be a nonempty immutable pattern and $T\in\Sigma^n$ resident text.

- $s$ is a legal alignment start with $0\le s\le n-m$.
- $j$ is the current pattern comparison index, decreasing from $m-1$.
- $x=T[s+j]$ is the bad character at a mismatch.
- $u=P[j+1:m]$ is the already matched suffix.
- $\operatorname{last}(x)$ is the rightmost pattern index containing $x$, or $-1$ if absent.
- $\Delta_{\mathrm{bad}}$ and $\Delta_{\mathrm{good}}$ are safe lower bounds on the next viable displacement.
- $H[x]$ is Horspool's displacement for a last-window symbol, with default $m$.
- $Q[x]$ is Sunday's displacement for a post-window symbol, with default $m+1$.
- A **verified region** is a text interval proved equal to a pattern interval and retained across an alignment shift.
- $z$ is the number of reported matches.
- **Sublinear inspection** means fewer than $n$ text positions are examined on a particular input; it is not a claim that reading an external stream costs less than $n$.

The usual analysis assumes constant-time equality, indexing, and shift-table lookup. Sparse hash tables provide expected rather than automatically worst-case constant lookup unless stronger map guarantees apply.

## Mechanisms, Invariants, or Proof Structure

### Alignment invariant

Immediately before comparing position $j$ at alignment $s$:

1. $0\le s\le n-m$ and $-1\le j<m$;
2. $P[j+1:m]=T[s+j+1:s+m]$;
3. every alignment start below $s$ has been classified or safely eliminated;
4. pattern-derived tables correspond to the exact pattern and equality semantics.

Equality and decrement preserve the suffix clause. A mismatch supplies the bad-character and good-suffix facts. A proved safe positive shift preserves the eliminated-alignment clause.

### Bad-character safety lemma

**Lemma.** Let $k<j$ be the rightmost position with $P[k]=x=T[s+j]$, or $k=-1$ when none exists. No occurrence starts at $s+d$ for $0<d<j-k$.

**Proof.** Under shift $d$, the observed $x$ aligns with pattern index $j-d$. For the stated range, $k<j-d<j$. Rightmost choice of $k$ says no such position contains $x$, contradicting the equality required by an occurrence. $\square$

### Good-suffix safety argument

Any occurrence at a later alignment that overlaps the observed copy of $u$ must align that text substring with an equal pattern substring, or align an overlapping suffix of $u$ with a pattern prefix. The strong rule enumerates the former while excluding a predecessor that would repeat the known mismatch, then falls back to the longest latter border. A preprocessed table is correct only if it returns the smallest displacement surviving these cases; table construction requires its own proof and oracle tests.

### Horspool safety theorem

**Theorem.** The Horspool displacement $H[T[s+m-1]]$ cannot skip an occurrence.

**Proof.** Let $y=T[s+m-1]$. For a candidate start $s+d$ with $0<d<m$, this text position aligns to pattern index $m-1-d$. A match requires $P[m-1-d]=y$. The rightmost occurrence of $y$ before $m-1$ therefore gives the smallest possible $d$; if absent, no $d<m$ is possible. The table encodes exactly this distance, or default $m$. $\square$

### Guarantee matrix

| Claim | Full rules | With proven Galil rule | Horspool | Sunday Quick Search |
|---|---|---|---|---|
| Exact under correct tables | yes | yes | yes | yes |
| Can skip alignments | yes | yes | yes | yes |
| Natural unbounded streaming | no | no | no | no |
| Linear worst case | variant/proof dependent | yes | no | no |
| Simple single shift table | no | no | yes | yes |

“Full rules” is not enough to identify one implementation theorem: good-suffix definitions, full-match rule, and remembered regions matter. Cite and implement a precise variant before attaching a tight comparison bound.

### Evidence boundaries

- Safety proofs establish that table-directed skips retain exact occurrences.
- Worst-case results apply only to the specified family member and assumptions.
- Exhaustive oracles reveal implementation errors over tested domains.
- Comparison counts characterize one abstract cost; benchmarks characterize one environment.
- Text semantics, normalization, output policy, and security limits remain product decisions.

## Alternatives and Trade-Offs

| Variant | Pattern data | Inspected location | Main advantage | Main risk |
|---|---|---|---|---|
| Full Boyer-Moore | bad-character and good-suffix tables | right-to-left | combines two strong skip proofs | complex preprocessing and conventions |
| Boyer-Moore with Galil | full rules plus verified region | right-to-left | proven linear worst-case variant | more state and proof-sensitive code |
| Horspool | final-position shift table | right-to-left | compact, simple hot loop | quadratic repeated-suffix family |
| Sunday Quick Search | post-window shift table | any current-window order | often large shift; simple table | lookahead bound and quadratic cases |
| KMP | prefix/failure table | sequential | streaming and deterministic linear scan | no forward alignment skips |
| Runtime built-in | implementation-specific | opaque | tuned native code and representation | algorithm and guarantees can change |

Choose the full algorithm when comparison cost is high and strong skip behavior justifies preprocessing complexity. Choose a simplified variant when pattern setup and hot-loop simplicity dominate and admitted input bounds control worst cases. Choose KMP for streams or when deterministic linear comparison work is mandatory. Prefer a tested runtime primitive when it exactly matches semantics, but pin/version its behavior and retain independent correctness tests.

Hybrids can switch by pattern length or alphabet statistics, but every branch needs validation and operational observability. A selector trained on one corpus can be adversarially or accidentally misled; use conservative resource caps independent of its prediction.

## Failure Modes and Misconceptions

1. **“Boyer-Moore is one loop.”** It is a family with distinct rules and theorems.
2. **“Rightmost occurrence always gives the shift.”** At mismatch index $j$, occurrences to its right cannot justify a positive bad-character alignment; clamp or use a position-aware table.
3. **“Safe shifts can be added.”** Independent lower bounds combine by maximum, not sum.
4. **“Good suffix means find the same suffix anywhere.”** Predecessor compatibility and prefix fallback are required for the strong rule.
5. **“A full match permits shifting $m$.”** That loses overlapping matches when the pattern has a border.
6. **“Horspool is Boyer-Moore, so it is linear.”** The simplified variant has quadratic inputs.
7. **“Sublinear means the text need not be read.”** It describes inspected positions in a random-access model, not ingestion or I/O.
8. **“Sunday always has a next symbol.”** The last legal window ends at $n$ and must terminate without out-of-bounds lookahead.
9. **“A 256-entry table suits every string.”** Huge or structured alphabets need sparse or domain-specific representations.
10. **“Tables are reusable after normalization changes.”** They belong to an exact symbol and equality policy.
11. **“Fewer comparisons means lower latency.”** Branches, caches, hashing, allocation, and preprocessing may dominate.
12. **“Random text is enough validation.”** Repetition, borders, matches, absent symbols, and every mismatch position target the hard logic.

## Worked Examples

### Example 1

**Situation.** Apply the bad-character rule when $P=\texttt{ANPANMAN}$ mismatches at $j=7$ on text symbol `P`.

The rightmost `P` left of index 7 is at index 2. Aligning it with the observed symbol requires shift $7-2=5$. No shift 1 through 4 can match, because the observed `P` would align with pattern indices 6 through 3, none of which is `P`.

**Conclusion.** The bad-character shift is 5 and eliminates four candidate starts by a direct equality contradiction.

### Example 2

**Situation.** The mismatch symbol appears only to the right of $j$ in the pattern.

Let `last(x)=6` and $j=3$. The global-table formula gives $j-\operatorname{last}(x)=-3$. A negative shift is meaningless and zero would stall. The global table has no useful left-of-$j$ occurrence, so use $\max(1,-3)=1$, or consult a position-aware predecessor table.

**Conclusion.** A global last-occurrence table is correct with a positive clamp but can be weaker than a position-specific table.

### Example 3

**Situation.** Explain strong good-suffix predecessor compatibility.

Suppose mismatch pattern symbol is `A` and the matched suffix is `BC`. An earlier `BC` preceded by `A` would align the same text `BC` but place `A` over the same text symbol already known not to equal `A`; that alignment fails immediately. An earlier `BC` preceded by `D` does not reproduce this contradiction and remains viable.

**Conclusion.** The strong rule excludes copies with the same predecessor because the mismatch supplies information beyond suffix equality.

### Example 4

**Situation.** No earlier complete copy of matched suffix `ABAB` exists, but its suffix `AB` is a prefix of the pattern.

Any overlapping future occurrence covering the end of the observed suffix can align that `AB` with the pattern prefix. The good-suffix fallback shifts so the prefix `AB` covers the last two observed symbols. Moving farther could skip that viable border alignment.

**Conclusion.** Prefix fallback is the final good-suffix case and is also what preserves some overlaps.

### Example 5

**Situation.** Build Horspool's table for $P=\texttt{aba}$.

The default is $m=3$. Process indices 0 and 1 only. At index 0, set `a` to $3-1-0=2$. At index 1, set `b` to $3-1-1=1$. The final `a` at index 2 is excluded; including it would overwrite `a` with zero and prevent progress.

**Conclusion.** $H[\texttt{a}]=2$, $H[\texttt{b}]=1$, and every other symbol has shift 3.

### Example 6

**Situation.** Trace the overlapping Horspool search for `aba` in `ababa`.

At shift 0, right-to-left comparisons `a`, `b`, `a` all match, reporting 0. The last-window symbol is `a`, whose table shift is 2, so the next alignment is 2. Again all three comparisons match, reporting 2. Advancing by 2 ends the loop.

**Conclusion.** The result is $(0,2)$ with six comparisons; the full-match table shift preserves the overlap.

### Example 7

**Situation.** Exhibit Horspool's quadratic behavior for `baaa` in ten `a` symbols.

There are $10-4+1=7$ alignments. At each, the three trailing `a` symbols match right-to-left and `b` then mismatches `a`, for four comparisons. The last-window `a` has shift one, so all seven alignments are tried: $7\cdot4=28$ comparisons.

**Conclusion.** Favorable skips do not imply a linear worst-case bound for Horspool.

### Example 8

**Situation.** Apply Sunday's rule with pattern length 5 when the post-window symbol is absent from the pattern.

The observed symbol sits at text coordinate $s+5$. At candidate starts $s+1$ through $s+5$, it would align with pattern indices 4 through 0. Since none equals it, all five starts are impossible. Shift by $m+1=6$.

**Conclusion.** Post-window evidence can eliminate the entire pattern width plus one alignment, provided the lookahead position exists.

### Example 9

**Situation.** Choose between a dense and sparse table for 20-byte patterns over byte input and Unicode-scalar input.

For bytes, 256 integer entries are bounded and likely cache-resident; pattern reuse makes initialization cheap. For Unicode scalar values, a dense table near the full code space wastes memory for at most 19 stored Horspool positions. A map plus default represents only observed pattern symbols, though hashing adds overhead.

**Conclusion.** Table design follows actual alphabet cardinality and access costs, not the generic word “string.”

### Example 10

**Situation.** A benchmark shows Horspool fastest on English prose and declares it the production winner for user-controlled binary blobs.

The workload changed alphabet distribution, repetition, pattern length, and adversarial control. Add repeated-suffix cases, tiny alphabets, all-match output, maximum sizes, cold tables, and binary data. Enforce a processing budget or choose a worst-case-controlled algorithm if an attacker can select inputs. Record comparison counts and tail latency.

**Conclusion.** Corpus evidence transfers only when the relevant workload and threat assumptions transfer.

## Cross-Program Connections

- **Data Structures Engineering:** dense arrays, sparse maps, compact integers, and immutable compiled objects determine table cost. See the [Data Structures Engineering roadmap](../../17-data-structures-engineering/ROADMAP.md).
- **Computer Architecture:** branch prediction, cache locality, vectorized primitives, and memory bandwidth can reverse comparison-count expectations.
- **Operating Systems:** random access, memory mapping, page faults, and readahead affect large resident searches; skipped comparisons are not skipped storage reads automatically.
- **Concurrent and Parallel Programming:** tables may be shared immutably, but per-search alignment, results, cancellation, and metrics require isolation.
- **Security Engineering:** simplified quadratic variants, slow hashing/equality, large patterns, and result floods require resource limits.
- **API and Service Engineering:** algorithm selection must preserve normalization, overlap, empty-pattern, coordinate, pagination, and cancellation contracts.
- **Algorithms:** [ALGE-052](./052-knuth-morris-pratt.md) supplies the streaming linear alternative; [ALGE-054](../ROADMAP.md#block-06--string-sequence-and-compression-algorithms) replaces deterministic skip tables with rolling fingerprint filters and mandatory verification.

## References

1. Robert S. Boyer and J Strother Moore, “A Fast String Searching Algorithm,” *Communications of the ACM* 20(10), October 1977, pp. 762–772. [Primary paper and DOI 10.1145/359842.359859](https://doi.org/10.1145/359842.359859). Retrieved 2026-09-05.
2. Zvi Galil, “On Improving the Worst Case Running Time of the Boyer-Moore String Matching Algorithm,” *Communications of the ACM* 22(9), September 1979, pp. 505–508. [Primary paper and DOI 10.1145/359146.359148](https://doi.org/10.1145/359146.359148). Retrieved 2026-09-05.
3. R. Nigel Horspool, “Practical Fast Searching in Strings,” *Software: Practice and Experience* 10(6), June 1980, pp. 501–506. [Primary paper and DOI 10.1002/spe.4380100608](https://doi.org/10.1002/spe.4380100608). Retrieved 2026-09-05.
4. Daniel M. Sunday, “A Very Fast Substring Search Algorithm,” *Communications of the ACM* 33(8), August 1990, pp. 132–142. [Primary paper and DOI 10.1145/79173.79184](https://doi.org/10.1145/79173.79184). Retrieved 2026-09-05.
5. Gonzalo Navarro and Mathieu Raffinot, *Flexible Pattern Matching in Strings: Practical On-Line Search Algorithms for Texts and Biological Sequences*, Cambridge University Press, 2002, Chapter 2. [Publisher record and DOI 10.1017/CBO9781316135228](https://doi.org/10.1017/CBO9781316135228). Retrieved 2026-09-05.
6. Maxime Crochemore, Christophe Hancart, and Thierry Lecroq, *Algorithms on Strings*, Cambridge University Press, 2007, Chapter 3, “String Searching with a Sliding Window.” [Publisher record and DOI 10.1017/CBO9780511546853](https://doi.org/10.1017/CBO9780511546853). Retrieved 2026-09-05.

## Exercises

### Exercise 1

For pattern `CABABA`, construct the global last-occurrence table. If a mismatch at $j=4$ observes `C`, compute the clamped bad-character shift and explain why it is safe.

### Exercise 2

Build Horspool's shift table for `ABRACADABRA`. Trace the shift after a window whose final symbol is `C`, then after one whose final symbol is `X`.

### Exercise 3

A Horspool implementation includes the pattern's final position while building its table. Diagnose the failure, give a minimal pattern/input that does not terminate, and repair it.

### Exercise 4

Design a variant selector for resident byte strings that can choose KMP, Horspool, or a runtime built-in. State correctness constraints, measurable features, adversarial safeguards, and the evidence needed before deployment.

### Exercise 5

A malware scanner searches memory-mapped files for thousands of patterns and requires bounded worst-case work, stable byte offsets, and cancellation. Explain why independently running a Boyer-Moore variant per pattern may be unsuitable. Propose a bounded design and evaluation plan without claiming technology not established in this chapter.

## Answers to the Exercises

### Answer 1

For `CABABA`, zero-based last occurrences are `C:0`, `A:5`, and `B:4`. At mismatch index $j=4$ with observed `C`, the global formula is $\max(1,4-0)=4$. At any displacement $d=1,2,3$, the observed `C` would align with pattern index $4-d\in\{3,2,1\}$; none is `C`. Thus those starts cannot match, and shift 4 is safe. The `A` occurrence at index 5 illustrates why a symbol to the right of $j$ would require clamping rather than a negative shift.

### Answer 2

The pattern length is 11, and Horspool processes indices 0 through 9. Repeated assignments retain the rightmost such position: `A` last appears at 7, so its shift is $10-7=3$; `B` at 8 gives 2; `R` at 9 gives 1; `C` at 4 gives 6; and `D` at 6 gives 4. The default is 11. A window ending in `C` shifts 6. A window ending in absent `X` shifts 11. The final pattern `A` at index 10 is excluded.

### Answer 3

Including final index $m-1$ assigns its symbol shift $m-1-(m-1)=0$. For pattern `a` and text `a`, the table stores `a:0`. The alignment matches and then advances by zero forever. Exclude the final position by iterating only `range(m-1)` and use default $m$. More generally, assert every compiled shift is in $[1,m]$ and test one-symbol patterns and full matches.

### Answer 4

All branches must implement identical byte equality, empty-pattern behavior, overlaps, and zero-based byte offsets. Features may include $m$, text length, expected pattern reuse, byte diversity, border/repetition statistics, and whether the input is truly resident. Measure table-build cost, comparisons, positions inspected, allocations, throughput, and tail latency over representative and adversarial corpora.

Apply hard input, output, and time limits regardless of prediction. If worst-case bounded comparison work is mandatory, route untrusted or repetitive inputs to KMP or a built-in only when its bound is documented for the pinned runtime. Differentially compare every branch with a naive oracle, fuzz selector boundaries, and record the selected branch in diagnostics. Deploy with shadow comparison and rollback thresholds. A selector is acceptable only when optimization cannot alter semantics and the fallback remains safe.

### Answer 5

Running thousands of independent matchers multiplies preprocessing, file passes, page traffic, cancellation checks, and worst-case comparison budgets. Simplified Boyer-Moore variants can also encounter quadratic per-pattern inputs, while outputs across patterns may be enormous. The family studied here is single-pattern and does not itself solve shared multi-pattern scanning.

A bounded design first groups work by immutable pattern set and gives each scan a byte range, explicit overlap halo of at least maximum pattern length minus one, stable global coordinates, cancellation checks, and deduplication ownership for halo matches. Choose a documented multi-pattern algorithm only after its later specification and proof are reviewed, or batch bounded KMP states in one sequential pass as a conservative design while accounting for $O(number\ of\ patterns)$ work per byte. Cap pattern count/length, scan bytes, comparison or transition budget, output count, concurrency, mapped pages, and deadline; return explicit partial/cancelled status.

Validate each pattern against a naive oracle on small files, test matches crossing partition and page boundaries, duplicate and prefix-related patterns, all-match inputs, corrupted mappings, cancellation at every stage, and deterministic coordinate deduplication. Benchmark page faults, memory, aggregate transitions, tail latency, and output backpressure. The design should remain provisional until the chosen multi-pattern method receives its own proof and implementation review.
