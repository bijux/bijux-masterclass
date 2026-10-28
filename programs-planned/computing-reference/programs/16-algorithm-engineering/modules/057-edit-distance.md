---
module_id: ALGE-057
program: Algorithm Engineering
level: 2
module_number: 57
title: Edit Distance
status: complete
last_verified: 2026-09-05
---

# Edit Distance

## One-Page Review

### Governing question

How can we compute and operationalize minimum edit cost while keeping sequence units, allowed operations, cost semantics, exactness, resource bounds, and reconstructed scripts explicit?

### Essential definitions

- An **edit operation** inserts, deletes, or substitutes a symbol under the declared model.
- **Levenshtein distance** is the minimum number of unit-cost insertions, deletions, and substitutions transforming one sequence into another.
- An **edit script** is an ordered sequence of operations realizing a transformation.
- The **dynamic-programming state** $D[i,j]$ is the minimum cost to transform prefix $A[0:i]$ into $B[0:j]$.
- The **edit graph** has grid vertices $(i,j)$ and edges for deletion, insertion, match, or substitution.
- A **banded computation** evaluates only cells with $|i-j|\le k$ when deciding whether unit-cost distance is at most $k$.
- **Traceback** reconstructs one optimal script; distance alone does not identify a unique script.
- **Approximate matching** permits differences but can still compute an exact distance or threshold decision.

### Central model, mechanism, or theorem

With unit costs and indicator $[A[i-1]\ne B[j-1]]$,

$$
D[i,j]=\min\begin{cases}
D[i-1,j]+1 & \text{delete},\\
D[i,j-1]+1 & \text{insert},\\
D[i-1,j-1]+[A[i-1]\ne B[j-1]] & \text{match or substitute}.
\end{cases}
$$

Boundaries are $D[i,0]=i$ and $D[0,j]=j$. The recurrence is a shortest-path computation in an acyclic edit graph, giving $O(mn)$ time and $O(mn)$ storage for a full table. Distance-only evaluation uses two rows and $O(\min(m,n))$ storage. A threshold $k$ safely restricts computation to a diagonal band because any path reaching $|i-j|>k$ already used more than $k$ insertions or deletions.

### Critical invariants

- Sequence units and equality are fixed before computation.
- Every DP cell means an exact prefix-to-prefix optimum under one operation set and cost model.
- Each predecessor reduces at least one prefix length, so the dependency graph is acyclic.
- Boundary values match the cost of transforming to or from the empty sequence.
- Rolling rows are not overwritten before their dependencies are consumed.
- Banded cells outside the legal threshold region behave as infinity, not zero.
- A returned script replays to the target and its cost equals the reported optimum.
- Threshold, timeout, overflow, truncation, and unavailable results are not confused with an exact distance.

### Common failures

Common failures include comparing bytes when users expect graphemes; calling every edit metric “Levenshtein”; treating adjacent transposition as one unit without changing the recurrence; initializing boundaries incorrectly; taking a greedy local match; reading an overwritten rolling-row cell; returning a band boundary as the true distance; claiming linear-space traceback from a two-row distance routine; overflowing weighted costs; normalizing by a denominator without defining empty inputs; and exposing unbounded quadratic work to untrusted requests.

### Compact example

Transform `kitten` to `sitting`: substitute `k→s`, substitute `e→i`, and insert final `g`, for cost 3. Dynamic programming proves no cheaper script exists. With threshold 2, a banded exact decision returns “greater than 2,” not distance 3; with threshold 3 it returns the exact value 3. Different optimal scripts can exist for other inputs, so tie-breaking belongs to the script contract.

### Connections

[ALGE-056](./056-suffix-trees-and-automata.md) recognizes exact factors; edit distance introduces controlled disagreement. [ALGE-058](../ROADMAP.md#block-06--string-sequence-and-compression-algorithms) generalizes to global and local sequence-alignment scoring. Data Engineering owns representation and normalization; API Engineering owns thresholds, resource statuses, and result semantics.

## Governing Question

Given two sequences and an application-specific meaning of change, how can we find the minimum transformation cost, prove the recurrence, reduce time or memory when the workload permits, reconstruct trustworthy operations, and prevent representation or resource policy from silently changing the answer?

“The edit distance” is incomplete without units, equality, operations, costs, and output. Unit-cost Levenshtein distance over bytes, normalized token distance with weighted substitutions, and a human-readable diff solve different problems even when all use a grid.

## Why This Matters

Edit distance appears in spelling support, record linkage, deduplication, OCR evaluation, biosequence comparison, test diagnostics, version differences, and fuzzy search. The quadratic baseline is simple enough to trust and expensive enough to abuse accidentally.

Optimization is workload-specific. A small threshold justifies banding. Small machine-word patterns may justify bit-parallelism. Similar files under insertion/deletion cost can favor distance-sensitive edit-graph algorithms. Reconstructing an alignment changes memory requirements. Hardware acceleration changes layout but not dependencies.

The enduring engineering task is to match the exact mathematical problem to the representation, performance regime, and consequence of errors.

## Prerequisites and Retrieval

Retrieve dynamic programming, shortest paths in directed acyclic graphs, induction on prefix length, asymptotic time and storage, Unicode and byte encodings, integer overflow, and result-type design. Complete [ALGE-051](./051-naive-and-prefix-based-pattern-matching.md) through [ALGE-056](./056-suffix-trees-and-automata.md).

This chapter focuses on global unit-cost Levenshtein distance, then explains bounded and weighted variants. ALGE-058 owns biological scoring matrices, local alignment, and affine gaps. Myers's insertion/deletion shortest-edit-script problem is identified separately because a substitution then costs two operations unless modeled otherwise.

## Learning Objectives

After completing this module, you should be able to:

1. define the sequence units, operations, costs, and result contract;
2. derive the Levenshtein recurrence and boundary conditions;
3. prove correctness through edit-graph paths or prefix optimality;
4. compute and trace small tables by hand;
5. implement full, rolling-row, and threshold-banded evaluation correctly;
6. distinguish distance computation from optimal-script reconstruction;
7. compare quadratic, banded, bit-parallel, and distance-sensitive methods;
8. identify when transposition, weighting, normalization, or local matching changes the problem;
9. design resource-bounded, versioned, deterministic service behavior; and
10. validate mathematical, implementation, representation, and performance claims independently.

## Core Exposition

### Define sequences before defining edits

Let $A[0:m]$ and $B[0:n]$ be sequences. Their symbols may be bytes, Unicode scalar values, grapheme clusters under a named segmentation version, tokens, lines, records, or domain objects under a stable equality relation. The choice can change both lengths and distance.

UTF-8 bytes are appropriate for byte-level corruption but not necessarily user-perceived text. Code points keep Unicode scalar identity but separate combining sequences. Normalization can make canonically equivalent spellings equal before distance, while grapheme segmentation groups user-visible clusters. Tokenization can discard punctuation or case. Persist the transformation policy when results must be reproducible.

Under unit-cost Levenshtein distance, allowed operations are:

- delete one symbol from the source;
- insert one target symbol;
- substitute one source symbol for one target symbol, at zero cost when they are equal and one otherwise.

Adjacent transposition is not one Levenshtein edit. Adding it yields a Damerau-style model whose variants differ in whether substrings may be edited repeatedly. Name the exact recurrence.

### Derive optimal prefix structure

Let $D[i,j]$ be the minimum cost to transform $A[0:i]$ into $B[0:j]$. Transforming $i$ symbols to empty requires $i$ deletions, and transforming empty to $j$ symbols requires $j$ insertions:

$$
D[i,0]=i,\qquad D[0,j]=j.
$$

For $i,j>0$, consider the last operation of an optimal script:

- delete $A[i-1]$, after optimally producing $B[0:j]$ from $A[0:i-1]$;
- insert $B[j-1]$, after optimally producing $B[0:j-1]$ from $A[0:i]$;
- align the last symbols, paying zero if equal or one substitution otherwise, after optimally transforming the preceding prefixes.

Taking the least candidate yields the recurrence in the review. Any nonoptimal predecessor could be replaced with a cheaper prefix script, contradicting optimality. Conversely, appending the named last operation to each optimal predecessor creates a valid script at exactly that candidate cost.

### View the table as an edit graph

Grid vertex $(i,j)$ represents consumed prefixes. A vertical edge $(i-1,j)\to(i,j)$ deletes, a horizontal edge inserts, and a diagonal edge matches or substitutes. All edges move forward, so the graph is acyclic. $D[i,j]$ is the shortest-path distance from $(0,0)$.

This view separates correctness from evaluation order. Row-major, column-major, anti-diagonal parallel, tiled, recursive-cache-oblivious, and GPU wavefront schedules are valid only if predecessors are available before a cell. It also makes script reconstruction a shortest-path predecessor problem.

For unit costs,

$$
|m-n|\le d(A,B)\le\max(m,n).
$$

The lower bound follows because only insertions and deletions change length by one. The upper bound substitutes the first $\min(m,n)$ symbols and inserts or deletes the remainder.

### Compute distance with rolling rows

Each row depends only on the previous row and the current row's left neighbor. Preserve the shorter sequence as the column dimension to use $O(\min(m,n))$ integers. The time remains $\Theta(mn)$ cell evaluations.

The update needs three logically old values: `previous[j]`, `current[j-1]`, and `previous[j-1]`. A one-array implementation can work if it saves the old diagonal before overwriting; casual in-place mutation often reads a value from the wrong row.

Two rows provide the optimum value but discard most predecessor choices. Full traceback normally retains the matrix or compact predecessor decisions. Hirschberg-style divide and conquer recomputes forward and reverse score rows to recover an optimal alignment in linear space with quadratic time. “The distance uses linear space” does not imply “the script is already available.”

### Reproduce exact and bounded evaluation

The following dependency-free Python computes the exact unit-cost distance with two rows and a threshold decision inside a diagonal band. `None` means the exact distance is greater than the supplied threshold, not unknown and not equal to the threshold.

<!-- bijux-verify: {"id":"levenshtein-exact-and-banded","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"kitten_sitting=3\nempty_abc=3\nsunday_saturday=3\nbounded_kitten_2=None\nbounded_kitten_3=3\n","stderr":""}} -->
```python
def levenshtein(left, right):
    if len(left) < len(right):
        left, right = right, left
    previous = list(range(len(right) + 1))
    for i, left_symbol in enumerate(left, 1):
        current = [i]
        for j, right_symbol in enumerate(right, 1):
            current.append(
                min(
                    previous[j] + 1,
                    current[j - 1] + 1,
                    previous[j - 1] + (left_symbol != right_symbol),
                )
            )
        previous = current
    return previous[-1]


def bounded_levenshtein(left, right, threshold):
    if threshold < 0:
        raise ValueError("threshold must be nonnegative")
    m, n = len(left), len(right)
    if abs(m - n) > threshold:
        return None
    infinity = threshold + 1
    previous = {j: j for j in range(min(n, threshold) + 1)}
    for i in range(1, m + 1):
        low, high = max(0, i - threshold), min(n, i + threshold)
        current = {0: i} if low == 0 else {}
        for j in range(max(1, low), high + 1):
            current[j] = min(
                previous.get(j, infinity) + 1,
                current.get(j - 1, infinity) + 1,
                previous.get(j - 1, infinity) + (left[i - 1] != right[j - 1]),
            )
        previous = current
    result = previous.get(n, infinity)
    return result if result <= threshold else None


print(f"kitten_sitting={levenshtein('kitten', 'sitting')}")
print(f"empty_abc={levenshtein('', 'abc')}")
print(f"sunday_saturday={levenshtein('sunday', 'saturday')}")
print(f"bounded_kitten_2={bounded_levenshtein('kitten', 'sitting', 2)}")
print(f"bounded_kitten_3={bounded_levenshtein('kitten', 'sitting', 3)}")
```

The dictionary rows store only live band cells for clarity. A production implementation can use compact arrays with validated diagonal indexing. The local run proves these fixtures in the recorded environment; exhaustive comparison against the full DP is stronger finite-domain evidence.

### Prove the diagonal band safe

At vertex $(i,j)$, the consumed-length difference is $i-j$. Diagonal match/substitution edges preserve it; deletion or insertion changes it by one. Reaching a cell with $|i-j|>k$ therefore requires more than $k$ length-changing operations, so no path of total unit cost at most $k$ can enter that cell.

Evaluate only $|i-j|\le k$, treating absent predecessors as infinity. With $m$ row iterations, at most $2k+1$ cells per row are live, so the simple bound is $O(mk)$ time and $O(k)$ live distance storage after an immediate $|m-n|>k$ rejection. When $k$ approaches the sequence lengths, the full DP may have lower overhead.

A banded algorithm answers a threshold problem. If the target cell is absent or exceeds $k$, report `greater_than_threshold`; do not publish its clipped sentinel as an exact distance.

### Generalize costs cautiously

Let deletion cost $c_d(a)$, insertion cost $c_i(b)$, and substitution cost $c_s(a,b)$. Replace the three unit increments in the recurrence with these costs. Nonnegative costs preserve the shortest-path interpretation, but symmetry, identity of indiscernibles, and application meaning need separate checks. Zero-cost changes can make unequal sequences distance zero. Direction-dependent costs make $d(A,B)\ne d(B,A)$.

Weighted arithmetic needs a safe numeric type and an infinity value that cannot overflow when an edge cost is added. Floating costs introduce rounding and tie questions. Fixed-point integers or exact rationals may be preferable when reproducibility matters.

Normalizing by $\max(m,n)$, $m+n$, or another denominator produces different scores. Define the empty/empty case and do not assume a normalized formula remains a metric.

### Distinguish neighboring algorithm families

Myers's $O(ND)$ difference algorithm considers insertions and deletions, with $N=m+n$ and $D$ the shortest edit-script length in that model. Matching diagonals are extended greedily after each edit. A Levenshtein substitution of cost one is not the same objective because replacement is a deletion plus insertion there.

Bit-parallel algorithms pack a DP frontier into machine words and can process many cells per word operation. Their bounds depend on pattern length, word width, alphabet masks, and multiword handling. SIMD and GPU implementations exploit lane or anti-diagonal parallelism but must include transfer, packing, padding, and saturation semantics.

Four-Russians, wavefront, and distance-sensitive methods serve other regimes. Select from measured length distribution, expected distance, thresholds, alphabet, required script, batch size, memory hierarchy, and worst-case exposure—not from one headline bound.

### Reconstruct scripts and define tie-breaking

A full table can trace backward from $(m,n)$ through a predecessor attaining the cell minimum. Multiple predecessors may tie, so multiple optimal scripts may exist. A deterministic API can prefer match, then substitution, deletion, and insertion—or another documented order—but that policy changes the returned script without changing distance.

Validate a script by replaying it against the original source, checking every consumed symbol and produced symbol, arriving exactly at the target, summing operation costs independently, and comparing with $D[m,n]$. Never trust traceback structure merely because the final numeric cell is correct.

Human-readable diffs often optimize stability, locality, or unique anchors rather than only minimum edit count. That is a product objective layered above mathematical distance.

### Engineer safe services and benchmarks

Record unit type, encoding/normalization/tokenizer version, operation set, cost model, threshold, algorithm, exactness, script tie-break, input digests, runtime, and resource status. Return a tagged result such as exact distance, greater than threshold, resource limit, invalid input, or unavailable—not one overloaded integer.

Bound both dimensions, product $mn$, band width, output script, memory, wall time, and concurrency. Check multiplication before allocating a matrix. Stream cancellation through long row loops. Avoid logging sensitive raw sequences; store digests and approved aggregates when evidence permits.

Benchmark by length pair, distance ratio, common-prefix structure, alphabet, representation, algorithm path, threshold, script requirement, CPU/vector features, peak bytes, cells or word operations, and latency distribution. Include adversarial long equal prefixes, all mismatch, repeated symbols, and threshold just below and above the answer.

## Definitions and Notation

Let $A\in\Sigma^m$ and $B\in\Sigma^n$ under a stable equality relation.

- $A[0:i]$ and $B[0:j]$ are prefixes under half-open indexing.
- $D[i,j]$ is the minimum declared edit cost between those prefixes.
- $d(A,B)=D[m,n]$ is the resulting global distance.
- $[x\ne y]$ is 1 when $x$ and $y$ differ and 0 otherwise.
- An **optimal script** has total cost $d(A,B)$.
- $k$ is a nonnegative threshold for an exact within-distance decision.
- An out-of-band or unavailable cell has value $\infty$, which cannot win a minimum.
- $N=m+n$ and $D$ in an insertion/deletion shortest-script discussion follow that algorithm's model, not automatically Levenshtein's substitution model.
- $z$ may denote returned script operations or approximate occurrences and must be included in output cost.

All complexity bounds assume symbol equality and numeric cost operations have the stated constant or measured cost. Tokenization, normalization, decoding, allocation, and output are separate work.

## Mechanisms, Invariants, or Proof Structure

### Optimal-prefix theorem

**Theorem.** The boundary conditions and three-way recurrence compute unit-cost Levenshtein distance for every prefix pair.

**Proof.** Induct on $i+j$. Boundaries have only insertions or deletions. For positive $i,j$, any final operation is a deletion, insertion, match, or substitution and leaves one of the three smaller predecessor pairs. By induction its cheapest prefix transformation has the stored cost, so every complete script costs at least the recurrence minimum. Appending the associated last operation to a minimizing predecessor constructs a script at that cost. $\square$

### Metric properties under unit costs

Nonnegativity is immediate. Distance zero permits only zero-cost equal-symbol diagonals, hence identical sequences. Reversing a script exchanges insertions and deletions and reverses substitutions, proving symmetry. Concatenating an optimal $A\to B$ script with an optimal $B\to C$ script gives an $A\to C$ script, so $d(A,C)\le d(A,B)+d(B,C)$.

These statements apply to the symmetric unit-cost model. Weighted, normalized, token-filtered, or directed policies need fresh analysis.

### Rolling-row invariant

Before computing column $j$ of row $i$, `previous[j]` is $D[i-1,j]$, `previous[j-1]` is $D[i-1,j-1]$, and `current[j-1]` is $D[i,j-1]$. After the minimum is appended, `current[j]` is exact. Row completion therefore preserves the recurrence while discarding rows no longer needed for distance.

### Band-safety lemma

**Lemma.** No unit-cost edit path of cost at most $k$ visits a cell with $|i-j|>k$.

**Proof.** Starting from zero coordinate difference, only insertion and deletion edges change $i-j$, each by one and each costing one. Achieving absolute difference greater than $k$ requires more than $k$ such edges. $\square$

### Script-verification invariant

After replaying the first $r$ operations, consumed source and target prefixes equal the script's recorded coordinates, emitted symbols equal the target prefix, and accumulated cost equals the sum of independently validated operations. At completion, both coordinates must reach $(m,n)$ and cost must equal the numeric optimum.

### Evidence boundaries

- Induction and shortest-path equivalence prove the recurrence under the model.
- Exhaustive tests cover finite alphabets and lengths, not arbitrary inputs.
- A run establishes one implementation's observed behavior.
- Benchmarks compare named implementations, hardware, and workloads.
- Linguistic or biological usefulness requires domain validation beyond algorithmic exactness.

## Alternatives and Trade-Offs

| Method | Time character | Live distance space | Script | Best regime | Main limitation |
|---|---:|---:|---|---|---|
| Full DP | $\Theta(mn)$ | $\Theta(mn)$ | direct traceback | trusted baseline, scripts | quadratic memory |
| Two-row DP | $\Theta(mn)$ | $O(\min(m,n))$ | not directly | exact distance only | still quadratic cells |
| Banded DP | $O(mk)$ after length check | $O(k)$ | possible with added state | small threshold | only decides/returns distances within $k$ |
| Hirschberg divide/conquer | $\Theta(mn)$ | linear | one optimum | memory-bounded alignment | recomputation and complexity |
| Bit-parallel DP | word-dependent | compact bit vectors | variant-dependent | short/moderate patterns, batches | width and implementation assumptions |
| Myers insertion/deletion diff | $O(ND)$ family | variant-dependent | shortest insert/delete script | similar files | different substitution cost model |

The baseline is often the best oracle. Production selection can dispatch by length, threshold, expected similarity, and output requirement, but every path must return the same declared semantics or a distinct tagged result.

## Failure Modes and Misconceptions

1. **“Distance compares strings.”** It compares declared symbol sequences; encoding and tokenization come first.
2. **“A swap is one edit.”** Not under ordinary Levenshtein operations.
3. **“Greedy matching finds an optimum.”** A locally attractive diagonal can force more later edits.
4. **“Two rows reconstruct the script.”** They retain the value, not all predecessor choices.
5. **“Banded failure means distance equals $k+1$.”** It establishes only that distance exceeds $k$.
6. **“Approximate matching returns approximate answers.”** It may exactly decide matches within an allowed distance.
7. **“Myers diff is unit-substitution Levenshtein.”** Its classic shortest script counts insertions and deletions.
8. **“Normalization is presentation.”** It changes symbols, lengths, equality, and answers.
9. **“Weighted costs remain a metric.”** Zero, asymmetric, or policy-dependent costs can break metric properties.
10. **“Linear space means cheap.”** Quadratic time can still exhaust CPU.
11. **“Parallel cells are independent.”** Each cell waits on three predecessors; legal wavefronts expose parallelism.
12. **“One benchmark picks the algorithm.”** Performance depends on length, distance, alphabet, thresholds, script needs, and hardware.

## Worked Examples

### Example 1

**Situation.** Compute the distance from `cat` to `cut`.

The prefixes `c` and `cu` match through the first symbol. Substituting `a` with `u` costs one, and `t` matches. A zero-cost script would require identical symbols, which they are not.

**Conclusion.** The unit-cost Levenshtein distance is 1.

### Example 2

**Situation.** Transform the empty sequence to `abc`.

No deletion or substitution can emit a target symbol without a source symbol. Three insertions construct `a`, then `ab`, then `abc`, matching boundary value $D[0,3]=3$.

**Conclusion.** Empty-prefix initialization is part of the proof, not boilerplate.

### Example 3

**Situation.** Compare `ab` with `ba` under two operation models.

Unit-cost Levenshtein can substitute both symbols for cost 2; one deletion and one insertion also cost 2. A model allowing adjacent transposition at unit cost returns 1.

**Conclusion.** The numeric answer identifies the operation model only when that model is named.

### Example 4

**Situation.** Trace the final row for `cat` versus `cut`.

Starting row is $(0,1,2,3)$. After `c`: $(1,0,1,2)$. After `a`: $(2,1,1,2)$. After `t`: $(3,2,2,1)$. The final cell is 1.

**Conclusion.** Each value uses north, west, and northwest predecessors from the correct logical rows.

### Example 5

**Situation.** Reject `abc` versus `abcdefgh` under threshold 3.

Their length difference is 5. Any transformation must insert at least five symbols, already exceeding the threshold, so no DP cells need evaluation.

**Conclusion.** $|m-n|$ is a cheap exact lower bound for unit costs.

### Example 6

**Situation.** Interpret bounded results for `kitten` and `sitting`.

The exact distance is 3. Threshold 2 returns `greater_than_threshold`; it does not reveal whether the answer is 3 or 300. Threshold 3 reaches the target with value 3 and may return that exact value.

**Conclusion.** A tagged threshold result prevents a sentinel from becoming false data.

### Example 7

**Situation.** Compare composed and precomposed visible text.

`é` may be one code point, while `e` plus a combining acute mark is two. Raw code-point Levenshtein sees different sequences; normalization to a declared canonical form can make them equal. UTF-8 byte distance differs again.

**Conclusion.** Reproducible user-facing distance requires versioned normalization and segmentation policy.

### Example 8

**Situation.** Use deletion cost 3 and insertion cost 1.

Transforming `a` to empty costs 3, while empty to `a` costs 1. The shortest-path recurrence remains meaningful with nonnegative directed edges, but symmetry fails.

**Conclusion.** A weighted edit optimum need not be a metric.

### Example 9

**Situation.** Allocate a full table for two sequences of length 100,000 using 32-bit cells.

There are $(100{,}001)^2=10{,}000{,}200{,}001$ cells. At four bytes each, raw cells alone require about 40.0 GB decimal before row objects, predecessors, inputs, or allocator overhead.

**Conclusion.** Validate dimensions and choose rolling, banded, divide-and-conquer, or external strategies before allocation.

### Example 10

**Situation.** Two optimal scripts yield different human diffs for repeated lines.

The numeric DP can tie between deleting an earlier repeated line and a later identical line. Both scripts have minimum cost, but one may preserve more stable anchors. A documented tie-break or higher-level diff heuristic chooses presentation.

**Conclusion.** Minimum cost proves optimal quantity, not unique or most comprehensible explanation.

## Cross-Program Connections

- **Programming Languages and Semantics:** equality, token streams, and operational replay determine what a script means.
- **Data Structures Engineering:** compact rows, predecessor encodings, deques, bitsets, and cache-aware tiles determine memory and locality. See the [Data Structures Engineering roadmap](../../17-data-structures-engineering/ROADMAP.md).
- **Data Engineering:** normalization, entity resolution, deduplication thresholds, lineage, and feature versions determine reproducibility.
- **Security Engineering:** quadratic denial of service, integer overflow, sensitive input logging, malformed encodings, and output amplification require explicit controls.
- **API and Service Engineering:** tagged threshold/resource results, cost-model versions, timeouts, pagination, and deterministic tie-breaks define compatibility.
- **Concurrent and Parallel Programming:** anti-diagonal dependencies, tiling barriers, vector lanes, cancellation, and deterministic traceback shape parallel execution.
- **Algorithms:** [ALGE-056](./056-suffix-trees-and-automata.md) provides exact membership; [ALGE-058](../ROADMAP.md#block-06--string-sequence-and-compression-algorithms) develops global/local scoring and gap models.

## References

1. Robert A. Wagner and Michael J. Fischer, “The String-to-String Correction Problem,” *Journal of the ACM* 21(1), January 1974, pp. 168–173. [Official ACM DOI 10.1145/321796.321811](https://doi.org/10.1145/321796.321811). Retrieved 2026-09-05.
2. Daniel S. Hirschberg, “A Linear Space Algorithm for Computing Maximal Common Subsequences,” *Communications of the ACM* 18(6), June 1975, pp. 341–343. [Official ACM DOI 10.1145/360825.360861](https://doi.org/10.1145/360825.360861). Retrieved 2026-09-05.
3. Esko Ukkonen, “Algorithms for Approximate String Matching,” *Information and Control* 64(1–3), 1985, pp. 100–118. [Official publisher DOI 10.1016/S0019-9958(85)80046-2](https://doi.org/10.1016/S0019-9958(85)80046-2). Retrieved 2026-09-05.
4. Eugene W. Myers, “An O(ND) Difference Algorithm and Its Variations,” *Algorithmica* 1, 1986, pp. 251–266. [Official publisher DOI 10.1007/BF01840446](https://doi.org/10.1007/BF01840446). Retrieved 2026-09-05.
5. Eugene W. Myers, “A Fast Bit-Vector Algorithm for Approximate String Matching Based on Dynamic Programming,” *Journal of the ACM* 46(3), May 1999, pp. 395–415. [Official ACM DOI 10.1145/316542.316550](https://doi.org/10.1145/316542.316550). Retrieved 2026-09-05.
6. Gonzalo Navarro, “A Guided Tour to Approximate String Matching,” *ACM Computing Surveys* 33(1), March 2001, pp. 31–88. [Official ACM DOI 10.1145/375360.375365](https://doi.org/10.1145/375360.375365). Retrieved 2026-09-05.

## Exercises

### Exercise 1

State the unit-cost Levenshtein meaning of $D[i,j]$, its boundaries, and all three recurrence candidates. Explain why adjacent transposition is absent.

### Exercise 2

Compute the complete rows for `book` versus `back`, give the distance, and exhibit one optimal edit script.

### Exercise 3

Diagnose an API that returns `min(distance, 4)` after banding with threshold 3. Replace it with a result type that preserves exactness and resource outcomes.

### Exercise 4

Design a dispatcher among two-row, banded, full-table, and bit-parallel methods. Specify semantic compatibility, workload inputs, fallbacks, resource controls, and differential evidence.

### Exercise 5

Design a multilingual record-linkage distance for personal names. Define units, normalization, weights, thresholds, fairness and privacy limits, versioning, review evidence, and what the score must not claim.

## Answers to the Exercises

### Answer 1

$D[i,j]$ is the minimum number of unit insertions, deletions, and substitutions transforming source prefix $A[0:i]$ into target prefix $B[0:j]$. Boundaries are $D[i,0]=i$ and $D[0,j]=j$. For positive indices, take the minimum of $D[i-1,j]+1$, $D[i,j-1]+1$, and $D[i-1,j-1]+[A[i-1]\ne B[j-1]]$.

The three predecessors correspond to the only allowed final operations. Adjacent transposition consumes two symbols from both sides and is not in the declared operation set; adding it requires a named Damerau-style state and recurrence rather than silently assigning a different answer.

### Answer 2

For columns empty, `b`, `a`, `c`, `k`, the rows are:

- empty: $(0,1,2,3,4)$;
- `b`: $(1,0,1,2,3)$;
- `bo`: $(2,1,1,2,3)$;
- `boo`: $(3,2,2,2,3)$;
- `book`: $(4,3,3,3,2)$.

Thus the distance is 2. One optimal script keeps `b`, substitutes the first `o` with `a`, substitutes the second `o` with `c`, and keeps `k`, producing `back`. Replaying consumes and emits all four symbols and costs two. Other tie-equivalent scripts are acceptable only if replay and cost checks pass.

### Answer 3

Clipping maps every exact distance 4 or greater to the same integer and falsely suggests that 4 was computed. Use a tagged union such as `Exact(value)`, `GreaterThan(threshold)`, `ResourceLimit(kind, progress)`, `InvalidInput(reason)`, and `Unavailable(reason)`. Banded threshold 3 returns `Exact(d)` only when $d\le3$; otherwise it returns `GreaterThan(3)`.

The contract records units, operation/cost model version, threshold, algorithm, and whether a script was requested. It never substitutes a timeout or memory rejection for `GreaterThan`, because failure to compute is not a mathematical lower bound.

### Answer 4

All paths must implement the same sequence preprocessing, equality, unit-cost Levenshtein objective, threshold semantics, and empty-input rules. Use immediate length-difference rejection for threshold calls. Choose banded DP when $k$ is small relative to lengths, bit-parallel only within validated pattern-width and multiword limits, two-row DP for unthresholded distance, and a full table only when a script is required and its checked allocation fits. Use linear-space reconstruction or reject explicitly when a full script exceeds memory policy.

Dispatch inputs include lengths, threshold, script requirement, available vector features, memory budget, and configured algorithm versions—not the sequence contents if that leaks sensitive classification. Every optimized result is differentially checked against full DP on exhaustive short sequences and randomized/adversarial larger fixtures. Include empty, unequal lengths, all equal, all mismatch, repetitions, Unicode transformations, thresholds around the answer, maximum costs, cancellation, and overflow. On unsupported features or unsafe allocation, fall back to a semantically identical path or return a tagged resource/unavailable result.

### Answer 5

Normalize with a versioned, locale-reviewed Unicode policy; segment into a declared unit such as code points or grapheme clusters; preserve original text separately; and define case, spacing, punctuation, diacritic, abbreviation, and token-order behavior. Derive weights from a documented domain objective with nonnegative bounded integers, and state whether the directed score is a metric. Thresholds should be calibrated per use rather than treated as universal identity cutoffs.

Return the model/version, transformed-length metadata, score, threshold decision, and explanation limits. Do not claim that a small distance proves two people are identical, that a large distance proves they differ, or that one global threshold is fair across languages and naming traditions. Require secondary identifiers and human review for consequential merges.

Evaluate exact implementation behavior with replayed scripts and oracle comparison, then measure false merges and misses across consented, representative language groups, including short names, transliteration, combining marks, reordered family names, aliases, and adversarial inputs. Audit disparate error rates and allow policy overrides with governance. Minimize retention, restrict raw-name logs, protect test data, record transformations without exposing identities, support deletion, and version/revalidate every normalization, weight, or threshold change. Acceptable alternatives must provide an equally precise representation, metric, privacy, fairness, and decision boundary.
