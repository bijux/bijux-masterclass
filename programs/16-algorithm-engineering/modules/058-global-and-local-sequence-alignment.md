---
module_id: ALGE-058
program: Algorithm Engineering
level: 2
module_number: 58
title: Global and Local Sequence Alignment
status: complete
last_verified: 2026-09-05
---

# Global and Local Sequence Alignment

## One-Page Review

### Governing question

How can dynamic programming optimize full-sequence or best-subsequence alignments while preserving scoring semantics, gap conventions, traceback correctness, numerical safety, and the boundary between an algorithmic optimum and a scientific conclusion?

### Essential definitions

- An **alignment** inserts gap symbols so two expanded sequences have equal length and no column contains two gaps.
- A **substitution score** $s(a,b)$ rewards or penalizes aligning symbols $a$ and $b$.
- A **linear gap score** charges the same penalty for every gap symbol.
- An **affine gap score** charges $g_o+(k-1)g_e$ for a gap run of length $k$, separating opening from extension.
- **Global alignment** consumes both complete sequences; Needleman-Wunsch-style boundaries penalize unmatched prefixes.
- **Local alignment** chooses the best pair of subsequences; Smith-Waterman-style recurrence resets negative prefixes to zero.
- **Traceback** follows score-attaining predecessors to reconstruct one optimal alignment.
- A **score optimum** is conditional on the declared scoring model; it is not automatically evolutionary, functional, or statistical evidence.

### Central model, mechanism, or theorem

With linear gap score $g<0$ and substitution score $s$, global alignment uses

$$
G[i,j]=\max\{G[i-1,j-1]+s(A[i-1],B[j-1]),\ G[i-1,j]+g,\ G[i,j-1]+g\},
$$

with $G[i,0]=ig$ and $G[0,j]=jg$. Local alignment adds zero to the maximum and initializes all boundaries to zero. Global traceback begins at $(m,n)$ and ends at $(0,0)$; local traceback begins at a maximum-scoring cell and stops at zero. Both linear-gap scores take $O(mn)$ time; distance-only-style score evaluation can use linear space, while direct traceback needs retained decisions or recomputation.

### Critical invariants

- Sequence alphabet, encoding, and substitution-score table are versioned together.
- Each DP cell is the optimum for its declared global prefixes or local endpoint.
- Boundaries encode the alignment mode rather than incidental initialization.
- Gap sign and open/extension convention are used consistently in recurrence and reporting.
- Traceback follows a predecessor whose score exactly explains the current cell.
- Replayed columns consume each required source symbol exactly once and reproduce the reported score.
- Negative infinity cannot overflow into a viable score.
- Empty local alignment, ties, saturation, pruning, timeout, and heuristic results are explicitly represented.

### Common failures

Common failures include treating score as distance; mixing reward and penalty signs; using zero global boundaries; omitting the zero reset in local alignment; tracing local alignment from the bottom-right cell; charging a length-one affine gap both open and extension under the wrong convention; using one matrix for affine gaps; changing a substitution matrix without changing the model version; overflowing narrow SIMD lanes; returning one tie as uniquely meaningful; and calling a high raw score statistically or biologically significant without a calibrated model.

### Compact example

With match $+2$, mismatch $-1$, and gap $-1$, local alignment of `ACACACTA` and `AGCACACA` has optimum score 12. The zero reset discards harmful prefixes, and traceback starts at the best cell rather than the bottom-right corner. Global alignment must consume all symbols and answers a different question. Changing gap or substitution scores can change both the optimum score and the alignment.

### Connections

[ALGE-057](./057-edit-distance.md) minimizes unit edit cost; alignment usually maximizes a domain score. [ALGE-059](../ROADMAP.md#block-06--string-sequence-and-compression-algorithms) turns repeated phrases into compression references. Data Engineering owns sequence provenance; Software Testing owns oracle, replay, tie, and numerical validation.

## Governing Question

Given two biological or general symbol sequences, a scoring system, and either full-length or best-region intent, how can we compute an optimal alignment, reconstruct and verify it, select gap and numerical models honestly, and avoid interpreting an algorithmic optimum beyond its evidence?

An alignment algorithm does not discover a context-free truth. It optimizes a declared objective over a declared representation. Global versus local boundaries, substitution scores, gap-run penalties, end-gap policy, and tie-breaking can all change the returned columns.

## Why This Matters

Alignment is a core example of dynamic programming whose boundary conditions define the problem. The same interior recurrence can produce semiglobal, overlap, global, or local behavior when boundaries and traceback endpoints change.

In production, scoring and representation matter as much as loops. Protein and nucleotide scores have domain interpretations. Text or event-sequence alignment may need different equality and gap models. Large matrices motivate linear-space traceback, banding, wavefronts, SIMD, GPUs, heuristics, or distributed tiling—each with a different evidence boundary.

An exact optimum demonstrates only optimality under the configured score. Homology, causation, identity, plagiarism, or fraud require additional statistical and domain evidence.

## Prerequisites and Retrieval

Retrieve [ALGE-057](./057-edit-distance.md), dynamic programming, edit graphs, induction, numeric bounds, traceback, matrix tiling, and sequence representation. Understand that minimizing nonnegative costs and maximizing signed scores are transformable only when the objective and constants preserve ordering.

This chapter covers pairwise global and local alignment with linear and affine gap scores. Multiple alignment, profile models, structural alignment, database-search heuristics, and statistical calibration are adjacent topics, not implied guarantees.

## Learning Objectives

After completing this module, you should be able to:

1. define alignment columns, substitution scores, and gap-run conventions;
2. derive global and local recurrences from endpoint intent;
3. trace score tables and reconstruct one optimum;
4. prove why local zero reset discards harmful prefixes safely;
5. formulate affine-gap state recurrences without double-charging;
6. distinguish score-only storage from traceback requirements;
7. design safe integer, SIMD, tiled, and parallel evaluation;
8. compare exact, banded, sparse, heuristic, and seed-and-extend methods;
9. validate scores, paths, ties, provenance, and resource outcomes; and
10. limit scientific and operational claims to evidence actually obtained.

## Core Exposition

### Define an alignment and its score

An alignment expands $A$ and $B$ by inserting gap markers so the expanded sequences have equal length and never align gap with gap. Removing gaps recovers the originals. A column aligns two symbols, a symbol with a gap, or a gap with a symbol.

Let $s(a,b)$ score a symbol pair. With linear gap score $g<0$, every symbol-gap column contributes $g$. The total alignment score is the sum over columns. Higher is better. Unlike unit Levenshtein distance, matches can earn positive values, different substitutions can have different values, and gap runs can have nonlinear scores.

The alphabet and score table must agree. An unknown symbol needs a documented row, rejection, or preprocessing rule. Silently mapping it to another symbol changes the objective. Matrix name, edition, scale, alphabet order, and gap convention belong in result provenance when scores have domain meaning.

### Derive global alignment

Let $G[i,j]$ be the maximum score of an alignment consuming all symbols of prefixes $A[0:i]$ and $B[0:j]$. Its final column is one of:

- $A[i-1]$ aligned with $B[j-1]$;
- $A[i-1]$ aligned with a gap;
- a gap aligned with $B[j-1]$.

Removing that final column yields the three predecessors in the review recurrence. Empty versus a length-$i$ prefix is forced to contain $i$ gaps, so $G[i,0]=ig$ and symmetrically $G[0,j]=jg$.

This is a longest-path computation in an acyclic grid with possibly negative edge weights. Global traceback begins at $(m,n)$ because both sequences must be consumed. A score-attaining path defines an alignment, and every alignment defines such a path.

### Turn global into local with boundaries

Let $L[i,j]$ be the best score of any aligned subsequences ending at $A[i-1]$ and/or $B[j-1]$ in the current cell's transition. Define zero boundaries and

$$
L[i,j]=\max\{0,\ L[i-1,j-1]+s(A[i-1],B[j-1]),\ L[i-1,j]+g,\ L[i,j-1]+g\}.
$$

Zero means abandon any negative-scoring prefix and start after it. Appending the same future columns to a negative prefix is always worse than starting from zero, so no optimal positive local alignment needs that prefix.

The optimum local score is the maximum over all cells, not necessarily $L[m,n]$. Traceback begins at a maximum cell and stops when it reaches zero. If every nonempty alignment has nonpositive score, the empty local alignment has score zero unless policy requires a nonempty result.

The scoring scheme must permit positive evidence for meaningful local results. If all substitution and gap scores are nonpositive, empty alignment always wins.

### Reproduce global and local scores

This dependency-free implementation computes scores with two rows. It intentionally does not return traceback; the distinction is part of the interface.

<!-- bijux-verify: {"id":"global-local-linear-gap-scores","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"global_gattaca=0\nlocal_classic=12\nlocal_no_positive=0\nglobal_empty=-6\n","stderr":""}} -->
```python
def alignment_score(left, right, *, local, match, mismatch, gap):
    if match <= 0:
        raise ValueError("match score must be positive for this local-score contract")
    previous = [0] * (len(right) + 1) if local else [j * gap for j in range(len(right) + 1)]
    best = 0
    for i, left_symbol in enumerate(left, 1):
        current = [0 if local else i * gap]
        for j, right_symbol in enumerate(right, 1):
            diagonal = previous[j - 1] + (
                match if left_symbol == right_symbol else mismatch
            )
            value = max(diagonal, previous[j] + gap, current[j - 1] + gap)
            if local:
                value = max(0, value)
                best = max(best, value)
            current.append(value)
        previous = current
    return best if local else previous[-1]


print(
    "global_gattaca="
    f"{alignment_score('GATTACA', 'GCATGCU', local=False, match=1, mismatch=-1, gap=-1)}"
)
print(
    "local_classic="
    f"{alignment_score('ACACACTA', 'AGCACACA', local=True, match=2, mismatch=-1, gap=-1)}"
)
print(
    "local_no_positive="
    f"{alignment_score('AAAA', 'TTTT', local=True, match=2, mismatch=-1, gap=-1)}"
)
print(
    "global_empty="
    f"{alignment_score('', 'ABC', local=False, match=2, mismatch=-1, gap=-2)}"
)
```

The validation environment records exact output and toolchain. Independent full-table oracles and exhaustive small sequences can check the two-row schedule. Neither run demonstrates biological appropriateness of these toy scores.

### Reconstruct and verify traceback

For global alignment, start at $(m,n)$. At cell $(i,j)$, choose a predecessor whose score plus its column contribution equals $G[i,j]$. Append the corresponding column in reverse and continue to $(0,0)$. For local alignment, start at a maximum cell and stop at zero.

Ties are common. A deterministic preference—diagonal before deletion before insertion, for example—returns one stable optimum but does not make it uniquely correct. If all optimal alignments matter, their number can be exponential and the output contract needs enumeration limits or a compact predecessor DAG.

Validate a returned alignment independently:

1. both expanded sequences have equal length;
2. no column has two gaps;
3. removing gaps recovers exactly the selected source ranges;
4. column scores under the recorded model sum to the reported optimum;
5. global ranges cover both inputs, while local coordinates match its endpoints;
6. every traceback step satisfies the recorded recurrence.

Score-only rolling rows do not preserve the necessary predecessor path. Retain full scores or predecessor bits, use divide-and-conquer reconstruction, checkpoint rows and recompute blocks, or return score-only explicitly.

### Model affine gap runs with states

A linear gap score treats one run of length ten like ten independent openings. Many domains distinguish opening a gap from extending it. This chapter uses positive penalties subtracted from score:

$$
gap(k)=g_o+(k-1)g_e,\qquad k\ge1.
$$

Maintain $M[i,j]$ for alignments ending with a symbol pair, $X[i,j]$ for a gap in $B$, and $Y[i,j]$ for a gap in $A$:

$$
\begin{aligned}
M[i,j]&=\max(M[i-1,j-1],X[i-1,j-1],Y[i-1,j-1])+s(A[i-1],B[j-1]),\\
X[i,j]&=\max(M[i-1,j]-g_o,X[i-1,j]-g_e,Y[i-1,j]-g_o),\\
Y[i,j]&=\max(M[i,j-1]-g_o,Y[i,j-1]-g_e,X[i,j-1]-g_o).
\end{aligned}
$$

The direct $X\leftrightarrow Y$ terms allow an immediately switched gap direction and charge a new open; a canonical model may forbid them when such adjacent opposing gaps are redundant under its score constraints. State that choice. Some literature defines length-$k$ penalty as $g_o+kg_e$, charging extension even for the first symbol. These conventions differ by $g_e$ per run.

Global initialization makes impossible states negative infinity and initializes the one legal boundary gap run with exactly the declared formula. Local affine alignment adds appropriate zero resets and begins traceback at the best state/cell. One matrix cannot remember whether a new gap continues a run.

### Choose numerical representation deliberately

For integer scores, bound the worst magnitude from maximum sequence length and per-column absolute score before choosing 8-, 16-, 32-, or 64-bit lanes. Saturating SIMD arithmetic can silently turn different true values into one maximum. Detect saturation and rerun in a wider path, or prove it impossible for admitted inputs.

Negative infinity must remain impossible after addition. Use a guarded sentinel far enough from the numeric minimum, or branch before adding. Floating substitution scores introduce rounding-dependent ties and cross-platform reproducibility concerns; fixed-point integers can be easier to audit.

Traceback pointers also need a format: bit-packed ties, one deterministic predecessor, or a predecessor mask. Ensure dimensions and products are checked before allocation.

### Optimize the dependency graph, not the semantics

Cells on an anti-diagonal are independent once the preceding anti-diagonals complete. Tiling improves cache reuse; tile $(p,q)$ waits for its north, west, and northwest neighbors. SIMD lanes can process striped or wavefront layouts. GPUs require transfer and traceback strategies. Distributed execution must checkpoint tile ownership and avoid publishing partial score surfaces.

Banding is exact only when a valid bound ties optimal paths to the band. X-drop and seed-and-extend pruning can be heuristic depending on configuration. BLAST-style database search identifies promising regions and extends them; it is not a full Smith-Waterman oracle over every database cell. Mark exact and heuristic paths separately.

Linear-space divide and conquer can reconstruct global alignments by finding a midpoint from forward and reverse score vectors. Local and affine variants need more state and careful endpoints. State the implemented variant rather than transferring a familiar bound by analogy.

### Interpret scores within evidence

Raw scores depend on matrix scale, gap penalties, sequence lengths, alphabet composition, and mode. Scores from different configurations are not directly comparable. Percent identity depends on which alignment and denominator were chosen. Multiple testing matters in database search.

In biosequence work, an optimal score may support a similarity analysis but does not alone establish homology, function, structure, clinical significance, or ancestry. Those claims need calibrated statistics, controls, databases, domain review, and often independent evidence. In text or event streams, the corresponding risks are identity, plagiarism, fraud, or causation claims.

### Engineer reproducible alignment services

Record input digests and immutable versions, sequence type and units, normalization, substitution matrix identifier/digest, gap formula and values, global/local/semiglobal mode, end-gap policy, algorithm/version, numeric width, exact/heuristic status, tie-break, coordinates, score, and resource outcome.

Bound dimensions, cell or band count, traceback bytes, output length, tie enumeration, runtime, and concurrency. Reject invalid symbols and score tables. Make cancellation safe at row or tile boundaries. Keep raw sensitive sequences out of routine logs.

Test full tables against rolling scores, affine implementations against exhaustive alignment enumeration on tiny inputs, traceback by replay, local endpoints by direct substring enumeration, SIMD widths against wide scalar arithmetic, tiles against row-major results, and optimized or heuristic paths against labeled exact baselines.

## Definitions and Notation

Let $A\in\Sigma^m$ and $B\in\Sigma^n$ under a declared symbol representation.

- An alignment column is $(a,b)$, $(a,-)$, or $(-,b)$, never $(-,-)$.
- $s(a,b)$ is the substitution score.
- $g<0$ is a linear per-gap-symbol score.
- $g_o,g_e\ge0$ are affine opening and extension penalties under $g_o+(k-1)g_e$.
- $G[i,j]$ is the optimum global prefix score.
- $L[i,j]$ is the optimum local score ending at the current region, with zero as restart.
- $M,X,Y$ are affine states ending in a pair, gap in $B$, and gap in $A$.
- $-\infty$ marks an impossible state and must be numerically safe.
- A traceback endpoint is $(i,j,state)$ together with a mode-specific stopping rule.
- $z$ is output alignment length or number of returned ties and contributes to cost.

Complexity claims count symbol-score lookup, numeric operations, storage, preprocessing, transfer, traceback, and output separately when they are not constant in the implementation.

## Mechanisms, Invariants, or Proof Structure

### Global optimality theorem

**Theorem.** The global recurrence and gap-initialized boundaries compute the maximum score over all alignments of complete prefixes.

**Proof.** Induct on $i+j$. Each nonempty alignment has exactly one legal final column, yielding one of the three smaller predecessors. By induction, replacing its prefix by the stored optimum cannot lower score, so no alignment exceeds the recurrence. Appending the associated final column to a maximizing predecessor constructs an alignment at the stored value. Boundaries contain only forced gap columns. $\square$

### Local reset theorem

**Theorem.** With additive column scores, discarding a negative-scoring prefix cannot remove an optimal positive local alignment.

**Proof.** If a candidate local alignment has a proper prefix with negative total $x<0$, remove that prefix. The remaining aligned subsequences are still legal and their score increases by $-x$. Therefore an optimum positive local alignment begins after every negative prefix; zero represents that restart. $\square$

### Traceback invariant

At traceback state $(i,j)$, the reversed columns already emitted explain the score difference from the chosen endpoint to the current cell and consume exactly the corresponding suffix ranges. Selecting an equality-attaining predecessor extends this property by one column. The mode-specific terminal condition establishes complete global or selected local ranges.

### Affine-state invariant

$M$ ends in a symbol pair, $X$ in a nonempty gap run in $B$, and $Y$ in a nonempty gap run in $A$. Entering $X$ or $Y$ subtracts $g_o$; remaining in the same gap state subtracts $g_e$. Thus a run of length $k$ is charged once for opening and $k-1$ times for extension.

### Numerical invariant

Every reachable score lies within a precomputed numeric bound, and impossible-state sentinels remain below any reachable score after guarded arithmetic. A narrow optimized kernel either proves this bound or reports saturation and falls back before publishing a result.

### Evidence boundaries

- Dynamic-programming induction proves optimality under the score model.
- Replay proves a returned alignment realizes its score and endpoints.
- Exhaustive enumeration proves finite small cases only.
- SIMD/GPU execution proves one kernel/environment, not numeric universality.
- Statistical, biological, or social meaning requires evidence beyond optimal score.

## Alternatives and Trade-Offs

| Design | Objective | Time/space character | Best fit | Main limitation |
|---|---|---|---|---|
| Global linear gap | consume both sequences | $O(mn)$; rolling score space possible | full-length peers | end differences penalized |
| Local linear gap | best subsequences | $O(mn)$; maximum endpoint | embedded similar regions | raw score needs calibration |
| Affine gap | contiguous gap runs | three-state $O(mn)$ | domain gap events | convention and initialization complexity |
| Semiglobal/overlap | selected free ends | boundary/endpoints vary | containment or overlaps | easily mislabeled as global/local |
| Banded exact | constrained path with proof | work near diagonal | known small displacement | unsafe without a path bound |
| Seed-and-extend heuristic | candidate regions | workload-dependent | huge databases | may miss the exact optimum |

Select mode from the scientific or product question, then select an implementation from scale and hardware. Do not choose a fast kernel first and retrofit semantics afterward.

## Failure Modes and Misconceptions

1. **“Alignment score is edit distance.”** One is usually maximized with rewards; the other is minimized under costs.
2. **“Global and local differ only at traceback.”** Boundary initialization and zero reset change the DP values.
3. **“Local traceback starts bottom-right.”** It starts at a maximum cell and stops at zero.
4. **“One matrix handles affine gaps.”** Gap-open versus extension requires state.
5. **“Open plus extend has one standard meaning.”** Length-one charging conventions differ.
6. **“All optimal alignments tell the same story.”** Ties can place gaps or mismatches differently.
7. **“Two rows can return an alignment.”** They return a score unless reconstruction recomputes or stores decisions.
8. **“SIMD integer output is exact by default.”** Narrow lanes may saturate or wrap.
9. **“Banding and X-drop are automatically exact.”** Each pruning rule needs a proof for the configured objective.
10. **“A high raw score is significant.”** Length, composition, matrix, gap, search space, and calibration matter.
11. **“Percent identity is configuration-free.”** Alignment and denominator choices change it.
12. **“An optimum establishes domain truth.”** It establishes only optimality under the recorded model.

## Worked Examples

### Example 1

**Situation.** Globally align `GATTACA` and `GCATGCU` with match $+1$, mismatch $-1$, and gap $-1$.

One optimum is `G-ATTACA` over `GCA-TGCU`. Its columns score $1-1+1-1+1-1+1-1=0$. Full DP confirms no complete-sequence alignment scores higher.

**Conclusion.** The global optimum is 0 under this toy scoring model; the chosen tie is not unique evidence of history.

### Example 2

**Situation.** Locally align `ACACACTA` and `AGCACACA` with match $+2$, mismatch $-1$, and gap $-1$.

The Smith-Waterman recurrence reaches maximum 12 after resetting harmful prefixes to zero. A traceback from that maximum extracts one best pair of subsequences rather than consuming both complete strings.

**Conclusion.** The local optimum is 12; its meaning depends on the exact score configuration.

### Example 3

**Situation.** Locally align `AAAA` with `TTTT` when match is $+2$, mismatch $-1$, and gap $-1$.

Every nonempty path begins with a negative mismatch or gap. Each cell resets to zero, so the empty local alignment wins.

**Conclusion.** Score zero can mean “no positive-scoring local region,” not four matching or aligned symbols.

### Example 4

**Situation.** Compare global and local intent for `XXXXABC` and `ABCYYYY`.

Local alignment can select `ABC`/`ABC` and ignore flanks. Global alignment must consume all seven symbols from each sequence, so mismatch or gap penalties for the flanks can dominate.

**Conclusion.** Endpoint policy answers whether unmatched flanks are evidence to score or context to ignore.

### Example 5

**Situation.** Charge $g_o=5$ and $g_e=1$ under $g_o+(k-1)g_e$.

One gap run of length four costs $5+3=8$. Four separate length-one runs cost $4\cdot5=20$. A linear penalty of 2 per symbol would charge both patterns 8 and cannot express the preference for one event.

**Conclusion.** Affine state preserves gap-run structure that a single linear column score loses.

### Example 6

**Situation.** Two traceback predecessors tie.

If diagonal and gap-based predecessors both explain a cell's optimum, choosing diagonal first yields a stable single output. Choosing the gap path may produce a different but equal-score alignment. Both must replay and rescore exactly.

**Conclusion.** Tie-breaking is deterministic policy, not a proof that alternatives are wrong.

### Example 7

**Situation.** A substitution matrix lacks symbol `X` present in input.

Indexing a nonexistent row can fail; mapping `X` to `A` silently creates false matches; assigning zero without documentation changes scale. Reject it or use a versioned explicit unknown-symbol row whose behavior was calibrated.

**Conclusion.** Alphabet validation precedes optimization.

### Example 8

**Situation.** A 16-bit SIMD kernel saturates at 32,767 on long matching sequences.

Several true scores collapse to the same saturated value, corrupting ranking and traceback. Bound score by length and maximum reward before dispatch, or detect saturation and rerun with 32- or 64-bit lanes.

**Conclusion.** Faster arithmetic is exact only inside a proved or checked numeric range.

### Example 9

**Situation.** Schedule a $4\times4$ tile grid in parallel.

Tile $(p,q)$ reads boundary data from $(p-1,q)$, $(p,q-1)$, and $(p-1,q-1)$. Tiles with equal $p+q$ can run after the prior wavefront completes. Running all tiles at once races on incomplete boundaries.

**Conclusion.** Parallelism follows the DP dependency DAG, not the visual independence of cells.

### Example 10

**Situation.** A database search returns a high local alignment score and labels two proteins homologous.

The DP proves that no alignment scores higher under the chosen matrix and gaps. It does not calibrate chance occurrence across the searched database, verify the input sequences, establish evolutionary history, or infer function. Statistical significance and domain review are separate evidence.

**Conclusion.** Algorithmic optimality must not be promoted into an unsupported scientific conclusion.

## Cross-Program Connections

- **Data Structures Engineering:** packed predecessor masks, rolling rows, band frontiers, and tiled matrices determine space and locality. See the [Data Structures Engineering roadmap](../../17-data-structures-engineering/ROADMAP.md).
- **Concurrent and Parallel Programming:** wavefront dependencies, barriers, SIMD lanes, GPU transfer, and deterministic reductions govern acceleration.
- **Data Engineering:** sequence provenance, alphabet validation, score-matrix versions, coordinate systems, and reproducible transformations govern data meaning.
- **Security Engineering:** matrix allocation, numeric overflow, malformed symbols, heuristic abuse, sensitive sequence logs, and output expansion require controls.
- **API and Service Engineering:** alignment mode, score model, coordinates, ties, exact/heuristic status, pagination, timeout, and saturation fallback are public contracts.
- **Software Testing and Quality Engineering:** exhaustive tiny alignments, independent rescoring, replay, mutation tests, and scalar-versus-vector differential checks provide layered evidence.
- **Algorithms:** [ALGE-057](./057-edit-distance.md) supplies cost-minimizing DP; [ALGE-059](../ROADMAP.md#block-06--string-sequence-and-compression-algorithms) studies dictionary-based compression of repeated sequence structure.

## References

1. Saul B. Needleman and Christian D. Wunsch, “A General Method Applicable to the Search for Similarities in the Amino Acid Sequence of Two Proteins,” *Journal of Molecular Biology* 48(3), March 1970, pp. 443–453. [Official publisher DOI 10.1016/0022-2836(70)90057-4](https://doi.org/10.1016/0022-2836(70)90057-4). Retrieved 2026-09-05.
2. Temple F. Smith and Michael S. Waterman, “Identification of Common Molecular Subsequences,” *Journal of Molecular Biology* 147(1), March 1981, pp. 195–197. [PubMed record and DOI 10.1016/0022-2836(81)90087-5](https://pubmed.ncbi.nlm.nih.gov/7265238/). Retrieved 2026-09-05.
3. Osamu Gotoh, “An Improved Algorithm for Matching Biological Sequences,” *Journal of Molecular Biology* 162(3), December 1982, pp. 705–708. [PubMed record and DOI 10.1016/0022-2836(82)90398-9](https://pubmed.ncbi.nlm.nih.gov/7166760/). Retrieved 2026-09-05.
4. Stephen F. Altschul and Mihai Pop, “Sequence Alignment,” in *Handbook of Discrete and Combinatorial Mathematics*, 2nd ed., CRC Press, 2017, Section 20.1. [NCBI Bookshelf edition](https://www.ncbi.nlm.nih.gov/books/NBK464187/). Retrieved 2026-09-05.
5. Richard Durbin, Sean R. Eddy, Anders Krogh, and Graeme Mitchison, *Biological Sequence Analysis*, Cambridge University Press, 1998. [Official publisher DOI 10.1017/CBO9780511790492](https://doi.org/10.1017/CBO9780511790492). Retrieved 2026-09-05.
6. Stephen F. Altschul, Warren Gish, Webb Miller, Eugene W. Myers, and David J. Lipman, “Basic Local Alignment Search Tool,” *Journal of Molecular Biology* 215(3), October 1990, pp. 403–410. [PubMed Central record](https://pmc.ncbi.nlm.nih.gov/articles/PMC116826/). Retrieved 2026-09-05.

## Exercises

### Exercise 1

With match $+2$, mismatch $-1$, and linear gap $-2$, compute all global DP rows for `AC` versus `AGC` and give the optimum score.

### Exercise 2

Explain why Smith-Waterman uses zero boundaries, a zero recurrence candidate, a maximum-cell endpoint, and a zero traceback stop. Give a counterexample to bottom-right traceback.

### Exercise 3

An affine implementation charges $g_o+kg_e$ but its API documents $g_o+(k-1)g_e$. Diagnose the numerical effect for three gap runs and define a compatibility repair.

### Exercise 4

Design a CPU dispatcher among scalar full-table, rolling-row, banded, and narrow-lane SIMD alignment. Specify semantic gates, score bounds, traceback behavior, fallbacks, and validation.

### Exercise 5

Design a reproducible local-alignment search service for a regulated biological workflow. Include provenance, significance boundaries, exact versus heuristic search, data protection, human review, and release evidence.

## Answers to the Exercises

### Answer 1

For columns empty, `A`, `G`, `C`, the empty row is $(0,-2,-4,-6)$. The row for `A` is $(-2,2,0,-2)$. The row for `AC` is $(-4,0,1,2)$: the final diagonal adds the `C`/`C` match reward to the prior score zero.

Thus the global optimum is 2. One alignment is `A-C` over `AGC`, scoring $2-2+2=2$. It consumes both complete sequences and independently rescoring its columns matches the final DP cell.

### Answer 2

Zero boundaries allow a local region to begin after either sequence's prefix. The zero candidate discards any negative-scoring aligned prefix because removing it improves every continuation. The best region can end anywhere, so traceback begins at a maximum over all cells and stops at zero, where the selected region began.

For `ABCxxxx` versus `yyyyABC` with positive matches and sufficiently negative mismatch/gap scores, the best local alignment is `ABC`/`ABC` and ends before the first sequence's bottom-right coordinate or begins after the second's origin. Bottom-right traceback would force irrelevant flanks or return a lower score. A complete answer must distinguish local source coordinates from global consumption.

### Answer 3

Under the documented convention, a length-$k$ run costs $g_o+(k-1)g_e$; the implementation charges exactly one extra $g_e$ per run. With three runs, every alignment containing them is over-penalized by $3g_e$, which can change ranking, not merely reported scale.

Do not silently reinterpret stored scores. Introduce a new score-model version naming the actual formula, or fix the recurrence and rebuild every result under the documented version. Persist formula identifier, values, and matrix digest; reject mixed versions. Create fixtures for length-one and longer gaps, multiple runs, global boundaries, local reset, and ties, and compare with exhaustive enumeration. Migration must recompute rather than algebraically subtract a count unless the exact gap-run structure is durably known and verified.

### Answer 4

All kernels must share alphabet mapping, substitution table, gap convention, alignment mode, end-gap policy, exactness, and tie contract. Use rolling scalar rows for score-only requests, full scores or predecessor bits for direct traceback, banded evaluation only with a proved path constraint and explicit outside-band result, and SIMD only when the maximum and minimum reachable scores fit its lanes.

Compute numeric bounds from lengths and score extrema before dispatch. Detect saturation and rerun in a wider scalar or SIMD path. Reject matrix-size overflow before allocation. A request needing unrestricted traceback cannot silently take a score-only path; use an approved reconstruction method or return a resource result.

Differentially compare every kernel with a wide scalar full-table oracle over exhaustive short alphabets and randomized/adversarial longer inputs. Include empty inputs, unknown symbols, global/local boundaries, long gaps, all mismatch, all match, ties, band edges, lengths at lane thresholds, saturation fixtures, cancellation, and replay/rescoring. Benchmark only after exact agreement, recording hardware features and chosen path.

### Answer 5

Create immutable input records with sequence digest, source accession/version, alphabet, preprocessing, consent/access classification, and coordinate system. Version the substitution matrix by name and digest, affine formula and values, local endpoint/tie policy, software and database generation, and numeric kernel. Return aligned source ranges, score, exact/heuristic status, resource status, and reproducible parameters.

For database scale, a reviewed seed-and-extend heuristic may generate candidates, but label it heuristic and define sensitivity evidence. Recompute high-consequence candidates with an exact local-alignment kernel over the declared region or full comparison when required. Statistical calibration must cover length, composition, searched database size, and multiple testing. State that optimal alignment and statistical significance do not alone prove homology, function, pathogenicity, or clinical action.

Encrypt data in transit and at rest, minimize sequence logs, enforce access and retention, audit exports, and use approved deidentified fixtures where possible. Require qualified human review and independent evidence for regulated conclusions. Release evidence includes source checks, full model documentation, exhaustive small oracles, scalar/SIMD differential tests, traceback replay, saturation and corruption tests, benchmark strata, heuristic sensitivity evaluation, security/privacy review, and rollback of versioned models. Any unavailable domain validation blocks the corresponding scientific claim, not merely a technical checklist item.
