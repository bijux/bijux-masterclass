---
module_id: ALGE-014
program: Algorithm Engineering
level: 1
module_number: 14
title: Quicksort and Partitioning
status: complete
last_verified: 2026-09-04
---

# Quicksort and Partitioning

## One-Page Review

### Governing question

How can an array be partitioned around a pivot so recursive subproblems become independent, and how should pivot choice, duplicates, recursion depth, comparator semantics, and adversarial inputs be controlled before quicksort is trusted?

### Essential definitions

- A **pivot** is a saved key or record used to classify the current range.
- A **partition** permutes a range into regions whose keys have declared relations to the pivot.
- A **two-way partition** commonly separates keys less than a pivot from keys at least as large, or produces two crossing-cursor regions under a scheme-specific contract.
- A **three-way partition** returns contiguous less-than, equal-to, and greater-than regions.
- A **partition boundary** is an index or index pair whose exact meaning belongs to the chosen scheme.
- **Randomized quicksort** makes pivot ranks independent of a fixed input by random choice or a prior random permutation under stated randomness assumptions.
- A **degenerate split** leaves a recursive side of size $n-1$ and another of size $0$.
- **Introspective sorting** monitors partition depth/progress and switches to a worst-case-safe fallback when a limit is crossed.
- A sort is **unstable** when equal-key records may change relative order; conventional in-place quicksort is unstable.

### Central model, mechanism, or theorem

For a two-way partition that places one pivot and leaves subproblem sizes $k$ and $n-k-1$,

$$
T(n)=T(k)+T(n-k-1)+\Theta(n).
$$

Balanced ranks yield $\Theta(n\log n)$; repeated extreme ranks yield

$$
T(n)=T(n-1)+\Theta(n)=\Theta(n^2),
$$

with $n(n-1)/2$ partition comparisons in a common distinct-key model.

If each pivot is uniformly random among the current $n$ distinct keys, the expected number of key comparisons is

$$
\mathbb E[C_n]
=
2(n+1)H_n-4n
=
\Theta(n\log n),
$$

where $H_n=\sum_{i=1}^{n}1/i$. A three-way partition improves duplicate-heavy recursion by excluding the entire equal region from subsequent calls.

### Critical invariants

- The partition contract must name every region, boundary, and equality policy.
- Save the pivot value/key before swaps can move its source record.
- Every loop step classifies at least one unknown record or strictly moves a scan boundary.
- Never recurse on the equal/pivot region already in final relation to both sides.
- A partitioned range is not necessarily sorted; only cross-region relations are known.
- Comparator results must be consistent throughout every partition and recursive call.
- Randomization improves an expected model; it does not erase quadratic possible executions.
- Median-of-sample heuristics improve pivot distributions empirically but do not alone prove a worst-case bound.
- Recurse on the smaller side and iterate on the larger to bound control-stack depth.
- Use three-way handling or an equally explicit duplicate strategy for low-cardinality inputs.
- Preserve permutation/identity and define partial-mutation behavior on comparison failure.

### Common failures

Common failures include mixing Hoare and Lomuto return conventions; losing the saved pivot during swaps; advancing both cursors after swapping an unclassified record; recursing on a range that still includes the same pivot boundary; treating partition output as sorted; using strict scans that run past sentinels; placing all equal keys on one side and recursing quadratically; choosing the first element on presorted hostile input; claiming random pivots guarantee $O(n\log n)$ worst case; allowing predictable randomness in an adversarial service; overflowing endpoints; retaining linear recursion depth; assuming in-place implies stable; and benchmarking only distinct random keys.

### Compact example

Partition $(3,1,2,3,3,0,2)$ around pivot $2$. A three-way pass may produce $(1,0\mid2,2\mid3,3,3)$ with boundaries $lt=2$ and $gt=4$. Only $[0,2)$ and $[4,7)$ require recursive sorting; the equal range $[2,4)$ is complete. Its internal record order is not promised unless the partition is specifically stable.

### Connections

[ALGE-006](./006-best-worst-expected-and-amortized-cost.md) separates worst and expected claims; [ALGE-008](./008-lower-bounds-and-adversary-arguments.md) supplies decision-tree and adversarial reasoning; [ALGE-012](./012-insertion-selection-and-shell-sorting.md) supplies sorting contracts; [ALGE-013](./013-merge-sort.md) provides a stable predictable contrast. [ALGE-015](../ROADMAP.md) supplies the heap fallback used by introspective designs.

## Governing Question

Quicksort is not one loop. It is a family formed by a partition scheme, pivot policy, equality policy, recursion schedule, small-range policy, and failure contract. Two implementations bearing the same name can have different boundary meanings, duplicate behavior, stack risk, comparison counts, and adversarial exposure.

Its appeal is powerful: rearrange in place with sequential scans, then solve two independent regions. Its danger is equally clear: partition quality controls recursion shape, and an apparently minor endpoint error can repeat a range forever or omit records. An engineering-quality quicksort must make the partition theorem explicit, then defend the pivot and recursion policy against real input distributions.

This module develops two-way schemes as named contracts, gives a full proof for a half-open three-way partition, derives expected and worst-case cost, and connects those results to stack control and robust hybrid design.

## Why This Matters

Partitioning appears beyond full sorting:

- order-statistic and quickselect algorithms;
- database and analytics grouping;
- spatial and geometric algorithms;
- divide-and-conquer filtering;
- low-cardinality grouping;
- introspective and pattern-defeating library sorts;
- parallel and cache-aware rearrangement.

Quicksort also demonstrates why an average-case slogan is unsafe. A fixed pivot policy can be attacked by sorted, reverse, organ-pipe, equal, or deliberately constructed inputs. A randomized policy has a probability model, seed lifecycle, and adversary model. A depth fallback converts evidence about bad progress into a deterministic protection mechanism.

Finally, partitioning makes semantic details visible. Equal keys can be grouped or scattered; record stability is usually lost; comparator failure can leave an arbitrary permutation; and a generic callback can dominate or violate the algorithm. These are part of correctness and product behavior, not implementation trivia.

## Prerequisites and Retrieval

Retrieve:

- sorting order, identity permutation, stability, key projections, and comparator laws;
- half-open ranges, loop invariants, variants, and safe endpoints;
- recurrences, harmonic numbers, expectation, and indicator variables;
- random permutations, uniform pivot rank, seeds, and adversary knowledge;
- stack frames, tail iteration, integer overflow, and exception safety;
- insertion, merge, and heap sorting trade-offs;
- operation counters, input families, and controlled evaluation.

You should be able to prove a loop classifies a shrinking unknown region, distinguish expected from worst-case complexity, and explain why equal keys are distinct records even when their comparison result is zero.

## Learning Objectives

After completing this module, you should be able to:

1. specify Lomuto-, Hoare-, and three-way partition boundaries without mixing their contracts;
2. prove a half-open three-way partition using four-region invariants;
3. derive quicksort correctness from partition postconditions and recursive induction;
4. solve balanced and degenerate quicksort recurrences;
5. derive the expected distinct-key comparison formula from pair probabilities;
6. explain why two-way equality policies can fail on duplicate-heavy inputs;
7. evaluate pivot sampling, randomization, adversary knowledge, and introspective fallback;
8. bound stack depth by recursing on the smaller partition;
9. diagnose endpoint, progress, comparator, stability, and partial-mutation defects;
10. design and validate a robust partition-based sort for an unfamiliar workload.

## Core Exposition

### State sorting and partition contracts separately

For range $A[lo:hi)$, a completed sort must be an ordered permutation, with stability only if promised. A partition has a weaker postcondition: it establishes relations among regions but need not order records within any region.

A pivot-placement two-way contract may return $p$ such that:

$$
\forall i\in[lo,p),\quad A[i]<v,
$$

$$
A[p]=v,
$$

$$
\forall i\in[p+1,hi),\quad A[i]\ge v.
$$

A three-way contract returns $(lt,gt)$ such that:

$$
A[lo:lt)<v,\qquad
A[lt:gt)=v,\qquad
A[gt:hi)>v.
$$

These inequalities are policy choices. Other correct partitions may put equals on either two-way side or return a split point without placing the pivot. The caller must recurse according to the actual postcondition.

### Understand Lomuto's pivot-placement scheme

A conventional half-open Lomuto scheme saves pivot record $A[hi-1]$, sets boundary $b=lo$, and scans $i$ from $lo$ through $hi-2$. Whenever $A[i]<v$, swap $A[b]$ with $A[i]$ and increment $b$. After the scan, swap the pivot record into $A[b]$.

During scanning maintain:

$$
A[lo:b)<v,
$$

$$
A[b:i)\ge v,
$$

$$
A[i:hi-1)\text{ is unknown},
$$

with the saved/parked pivot at $hi-1$.

The scan classifies exactly one record per iteration. Final pivot placement yields the two-way contract above. Recursion must exclude $b$: sort $[lo,b)$ and $[b+1,hi)$.

This scheme is easy to specify but can perform many swaps and sends every equal-to-pivot non-pivot record to the right. On an all-equal array it repeatedly produces sizes $0$ and $n-1$, causing quadratic recursion unless equality is handled differently.

### Treat Hoare partition as a different interface

Hoare-style partition moves two cursors inward: the left cursor seeks a key not less than the pivot, the right seeks a key not greater, and out-of-side records are exchanged until cursors cross. It often performs fewer swaps than Lomuto.

Its return value commonly separates two nonempty ranges such that every left-region key is no greater than every right-region key. The pivot record need not occupy the returned boundary. A half-open caller might recurse on $[lo,s)$ and $[s,hi)$ for a scheme returning $s$, while an inclusive textbook version often returns $j$ and recurses on $[lo,j]$ and $[j+1,hi]$.

There is no safe universal translation from the name “Hoare partition.” Specify scan strictness, sentinel/access guards, equality behavior, returned index, and recursive ranges together. Using Lomuto's “exclude the pivot index” caller with a Hoare split is a classic omission or nontermination defect.

### Derive a half-open three-way partition

Choose and save pivot key $v$. Initialize

$$
lt=lo,\qquad i=lo,\qquad gt=hi.
$$

Maintain four regions:

$$
A[lo:lt)<v,
$$

$$
A[lt:i)=v,
$$

$$
A[i:gt)\text{ is unknown},
$$

$$
A[gt:hi)>v.
$$

If $A[i]<v$, swap $A[lt]$ with $A[i]$, then increment both $lt$ and $i$. Before the swap, $A[lt:i)$ is equal and $A[lt]$ moves into position $i$; after incrementing $i$, that equal record belongs to the expanded equal region, while the small record expands the left region.

If $A[i]>v$, decrement $gt$ and swap $A[i]$ with $A[gt]$. Do not increment $i$: the record brought from the old unknown suffix has not been classified.

If $A[i]=v$, increment $i$, expanding the equal region.

The variant $gt-i$ is the unknown-region length. Every branch decreases it by one. At termination $i=gt$, so the unknown region is empty and $(lt,gt)$ satisfies the three-way contract.

### Prove recursive quicksort from partition

For a range of length zero or one, return. Otherwise partition into less, equal, and greater regions. The partition preserves every record exactly once and establishes:

$$
\text{less keys}<v=\text{equal keys}<\text{greater keys}.
$$

Recursively sort only the less and greater ranges. Both are strictly smaller when the equal range contains at least the chosen pivot. By induction they become sorted permutations of themselves. Their cross-region relations to $v$ mean their concatenation with the equal region is globally sorted.

Conventional in-place partition swaps can reorder equal-key identities, both within the equal region and by crossings elsewhere, so this proves an unstable sorted permutation. A stable quicksort needs a different stable partition/storage design and different movement analysis.

### Derive best and worst recursion shapes

For a two-way distinct-key partition with pivot final position $k$ relative to a length-$n$ range:

$$
T(n)=T(k)+T(n-k-1)+cn.
$$

If $k$ stays near $(n-1)/2$, recursion height is $\Theta(\log n)$ and each level processes total length $O(n)$, so:

$$
T(n)=\Theta(n\log n).
$$

If every pivot is the smallest or largest:

$$
T(n)=T(n-1)+cn=\Theta(n^2).
$$

With one comparison between the pivot and each of the other distinct records, the partition comparison total becomes:

$$
(n-1)+(n-2)+\cdots+1=\frac{n(n-1)}2.
$$

A pivot heuristic changes which inputs cause these shapes; it does not remove the recurrence's dependence on progress.

### Derive randomized expected comparisons

Assume $n$ distinct ranks and that the pivot is independently uniform within every current subarray, equivalently that a fixed input is randomly permuted before deterministic first-pivot quicksort under suitable independence.

Ranks $i<j$ are compared exactly when the first pivot chosen from ranks $i,i+1,\ldots,j$ is either endpoint. There are $j-i+1$ candidate ranks and two favorable endpoints, so:

$$
\Pr(i\text{ compared with }j)=\frac{2}{j-i+1}.
$$

Let $X_{ij}$ indicate that comparison. By linearity of expectation:

$$
\mathbb E[C_n]
=
\sum_{1\le i<j\le n}\mathbb E[X_{ij}]
=
\sum_{1\le i<j\le n}\frac{2}{j-i+1}
=
2(n+1)H_n-4n.
$$

Since $H_n=\ln n+\gamma+O(1/n)$,

$$
\mathbb E[C_n]=\Theta(n\log n).
$$

This theorem does not say every randomized execution is $O(n\log n)$, nor does it cover arbitrary duplicate policies, biased generators, reused predictable seeds, or an adaptive adversary that observes choices.

### Choose a pivot policy as a risk decision

Common policies include:

- first or last record: minimal overhead, obvious structured worst cases;
- middle position: avoids one sorted-input extreme but has constructed bad cases;
- uniformly random position: expected protection for a fixed input under sound randomness;
- median of three or a larger sample: often improves finite partition balance at extra comparisons;
- deterministic selection of an approximate or exact median: stronger balance at higher overhead;
- introspective depth/progress monitoring: retain ordinary pivots but fall back when recursion becomes dangerous.

Sampling values from fixed positions can be defeated by patterns tailored to the sample. Random sampling depends on generator quality, seed management, and adversary visibility. Exact median selection changes the cost model and is rarely justified for every partition of a general sort.

A robust general implementation often layers policies rather than betting on one pivot trick: sampling, three-way equality handling, small-range insertion, smaller-side recursion, and a worst-case fallback.

### Handle duplicates as a primary workload dimension

On an all-equal length-$n$ input, a three-way partition classifies the entire range once and returns an equal region of length $n$. No recursive work remains, so time is $\Theta(n)$ under constant-time comparisons.

A two-way policy that sends all equals to one side can instead recur on $n-1$ records and take $\Theta(n^2)$. A crossing-cursor two-way scheme may split equals more evenly but still performs work through multiple levels and has scheme-specific behavior.

Low-cardinality data is common: status codes, categories, Boolean flags, repeated timestamps, nulls, and bucketed scores. Benchmarking only distinct random keys omits a major determinant of partition performance.

Three-way partitioning does not itself promise stability. It only makes the equal block explicit and removes it from recursion.

### Bound stack independently of running time

Naive recursive quicksort can use $\Theta(n)$ stack frames on degenerate partitions, causing stack exhaustion before quadratic time completes. The following schedule bounds control depth:

1. partition the current range;
2. recursively sort the smaller non-equal side;
3. replace the current range with the larger side and continue iteratively.

Whenever recursion occurs, its range has size at most half of the current non-equal work. Therefore recursive depth is $O(\log n)$ even if time remains $\Theta(n^2)$ from repeatedly iterating over large degenerate sides.

Stack safety is not a time guarantee. An introspective fallback addresses time by switching once a depth/progress budget signals too many bad partitions.

### Understand introspective protection

An introspective sort begins with quicksort and tracks a limit commonly proportional to $\lfloor\log_2 n\rfloor$. If partition depth exceeds the limit, it switches the remaining range to a sorter with $O(n\log n)$ worst-case time, classically heapsort.

The depth limit and fallback must be included in the proof:

- work before the limit spans only $O(\log n)$ partition levels;
- each such level processes at most $O(n)$ total records;
- fallback ranges are disjoint at the point they are converted;
- the fallback satisfies the same ordering/permutation contract.

This yields an $O(n\log n)$ worst-case hybrid without claiming that pivot sampling alone eliminated bad inputs. Detailed hybrid tuning returns in ALGE-019.

### Preserve endpoint and comparator safety

Use one interval convention throughout. For half-open $[lo,hi)$, an empty range has $lo=hi$, the last record is $hi-1$, and returned three-way boundaries satisfy:

$$
lo\le lt\le gt\le hi.
$$

Save the pivot key or an immutable copy before exchanges can move its record. If key extraction refers to mutable record storage, swaps must not change the comparison value being used as $v$.

Comparators must remain consistent. NaN, locale/configuration changes, mutation, or a stateful comparator can make a record compare less at one moment and greater later, destroying the region proof. Comparator/key exceptions can leave a partial permutation; the API must define ownership and recovery rather than implying rollback.

### Preserve executable partition evidence

The following run implements the reviewed half-open three-way invariant. It counts one less-than test for every classification and a second greater-than test when the first is false.

<!-- bijux-verify: {"id":"three-way-partition-ledger","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"input=(3, 1, 2, 3, 3, 0, 2) pivot=2\npartitioned=(1, 0, 2, 2, 3, 3, 3) lt=2 gt=4 comparisons=12\nless=(1, 0) equal=(2, 2) greater=(3, 3, 3)\n","stderr":""}} -->
~~~python
def partition_three_way(values, pivot):
    items = list(values)
    lt = 0
    index = 0
    gt = len(items)
    comparisons = 0

    while index < gt:
        comparisons += 1
        if items[index] < pivot:
            items[lt], items[index] = items[index], items[lt]
            lt += 1
            index += 1
        else:
            comparisons += 1
            if items[index] > pivot:
                gt -= 1
                items[index], items[gt] = items[gt], items[index]
            else:
                index += 1

    return tuple(items), lt, gt, comparisons


values = (3, 1, 2, 3, 3, 0, 2)
pivot = 2
partitioned, lt, gt, comparisons = partition_three_way(values, pivot)
print(f"input={values} pivot={pivot}")
print(
    f"partitioned={partitioned} lt={lt} gt={gt} "
    f"comparisons={comparisons}"
)
print(
    f"less={partitioned[:lt]} equal={partitioned[lt:gt]} "
    f"greater={partitioned[gt:]}"
)
~~~

The internal order of the less and greater regions is incidental. Tests should assert region predicates and identity permutation rather than freeze a swap order unless the API promises it.

### Evaluate partitions before whole-sort timing

Instrument:

- pivot rank and equal-region size;
- less/equal/greater sizes by depth;
- comparisons and key projections;
- swaps, bytes moved, and self-swaps;
- recursion and iteration depth;
- fallback and small-range counts;
- branch and cache behavior;
- failures and comparator inconsistencies.

Use input families including sorted, reverse, rotated, organ-pipe, sawtooth, all equal, low-cardinality, duplicate clusters, nearly sorted, random, and adversarial constructions relevant to the pivot policy. Validate order and identity permutation first. Report randomness procedures and realized seeds; a single favorable shuffle is not an expected-case study.

## Definitions and Notation

- $A[lo:hi)$ is the half-open range being partitioned or sorted; $n=hi-lo$.
- $v$ is a saved pivot key under the declared projection.
- $k$ is the number of records placed on one side of a two-way pivot in the recurrence.
- $(lt,gt)$ are three-way boundaries, with equal region $[lt,gt)$.
- $i$ is the next unclassified index and $gt-i$ is the unknown-region variant.
- $H_n=\sum_{r=1}^{n}1/r$ is the $n$th harmonic number.
- $C_n$ is the random variable counting key comparisons under the declared randomized model.
- A **pivot rank** is the pivot's order-statistic position within the current distinct-key subarray.
- A **bad partition** is defined relative to a progress threshold; it is not merely one that looks visually uneven.
- An **adaptive adversary** may choose or alter inputs using observations of the algorithm's choices.
- A **fallback** is a sorter invoked to preserve a stronger bound after a monitored limit.
- A **small-range cutoff** changes the terminal mechanism from partition recursion to a base-case sorter.

Two-way and three-way comparison counts are not interchangeable. Three-way classification may use a three-outcome comparator once or two Boolean comparisons, as the executable ledger does. Name the primitive before reporting totals.

## Mechanisms, Invariants, or Proof Structure

Use this partitioned-sort worksheet:

1. **Sort contract:** declare order, identity permutation, stability, mutation, and failure semantics.
2. **Comparator:** define key, equivalence, exceptional values, and consistency duration.
3. **Partition scheme:** name Lomuto, Hoare, three-way, block, or another exact contract.
4. **Endpoints:** state half-open/inclusive ranges and every returned boundary meaning.
5. **Pivot ownership:** save a stable key/record before swaps and define selection cost.
6. **Regions:** label classified left/equal/right and the unknown interval.
7. **Preservation:** prove every swap/update restores all region predicates.
8. **Progress:** prove unknown length or cursor distance decreases.
9. **Partition postcondition:** assert region relations and identity permutation, not full order.
10. **Recursive ranges:** exclude every already classified pivot/equal record and prove strict size decrease.
11. **Recursive proof:** compose sorted subranges with cross-region relations.
12. **Cost model:** distinguish worst, expected, sampled, duplicate, and adversarial cases.
13. **Risk controls:** define randomization, seed/adversary model, depth limit, and fallback.
14. **Stack control:** recurse on the smaller side and iterate the larger where required.
15. **Validation:** cover region predicates, permutation, duplicates, patterns, failures, and small exhaustive domains.
16. **Evaluation:** retain pivot/split telemetry, counters, seeds, environment, and bounded conclusions.

For the three-way loop, the key invariant is a complete partition of the active range:

$$
[lo,lt)\ \cup\ [lt,i)\ \cup\ [i,gt)\ \cup\ [gt,hi)
=
[lo,hi),
$$

with disjoint half-open regions, respectively less, equal, unknown, and greater. Preservation must show both the key predicate and exact identity membership; a swap cannot create or destroy a record.

## Alternatives and Trade-Offs

**Lomuto versus Hoare partition.** Lomuto offers a simple pivot-placement contract but often swaps more and handles equals poorly without modification. Hoare uses inward scans and often fewer swaps, but its split/pivot semantics are easier to call incorrectly.

**Two-way versus three-way.** Two-way code can be compact and effective for mostly distinct keys. Three-way classification prevents repeated work on large equal classes and exposes a useful equal range, at some branch/comparison overhead.

**Fixed versus randomized pivots.** Fixed positions are reproducible and cheap but admit simple hostile patterns. Random pivots give expected guarantees for fixed inputs under sound independence, while adding randomness lifecycle and adversary questions.

**Random pivot versus sampling.** One uniform pivot makes analysis clean. Median-of-three or larger samples often improve finite balance but cost comparisons and remain susceptible to constructed patterns unless combined with other controls.

**Sampling versus deterministic median selection.** Strong median selection can guarantee balanced progress, but its overhead and implementation complexity may overwhelm typical sort partitions. It is more central to worst-case selection than ordinary library quicksort.

**Naive recursion versus smaller-side recursion.** Naive recursion mirrors the mathematical recurrence but can exhaust the stack. Recursing only on the smaller side preserves sorting behavior while bounding control depth independently of time.

**Pure quicksort versus introspective fallback.** Pure quicksort has a simple expected model and quadratic worst case. Introspection adds state and a fallback but produces a deterministic $O(n\log n)$ worst-case hybrid when implemented and proved correctly.

**In-place unstable versus stable partition.** Swap-based partitioning uses small auxiliary storage and strong locality but reorders equals. Stable partitioning usually requires extra storage, extra movement, or more sophisticated algorithms.

**Direct records versus indices.** Direct swaps are simple for narrow values. Indirect sorting reduces payload movement but adds memory, indirection, and a later application/materialization question.

## Failure Modes and Misconceptions

1. **“Partition means both sides are sorted.”** It establishes only relations to a pivot or split.
2. **“All partition functions return the pivot index.”** Hoare-style schemes often return a split boundary instead.
3. **“Exclude the returned Hoare index as if it were Lomuto's pivot.”** This can omit a record or repeat a range.
4. **“The pivot remains at its original slot.”** Swaps move records; save a stable key/value.
5. **“Increment $i$ after every three-way swap.”** A record arriving from the right unknown region still needs classification.
6. **“Equal keys can go anywhere without cost consequences.”** One-sided equals can create quadratic recursion.
7. **“Three-way partition is stable.”** Grouping equals does not preserve their identity order.
8. **“First-element pivot is fine because sorted input is easy.”** It is a canonical degenerate case for several schemes.
9. **“Middle-position pivot guarantees balance.”** Position and rank are different; constructed values can make it extreme.
10. **“Median of three guarantees $O(n\log n)$.”** Sampling improves a distribution but has deterministic bad inputs.
11. **“Randomized means worst-case $O(n\log n)$.”** The quadratic execution remains possible.
12. **“One fixed seed proves expected performance.”** It provides one deterministic replay, not a randomness sample.
13. **“Secret randomness solves every denial-of-service risk.”** Leakage, bias, reuse, cost, and fallback policy still matter.
14. **“$O(\log n)$ expected recursion means the stack is safe.”** One bad execution can be linear without smaller-side scheduling.
15. **“Smaller-side recursion fixes quadratic time.”** It fixes control depth, not partition work.
16. **“In-place means no extra state.”** Stack, pivot copies, cutoffs, and fallback state still consume resources.
17. **“Comparator equality is object identity.”** Key equivalence and record identity are distinct.
18. **“A sort failure rolls back.”** Swap-based partial mutation remains unless stronger semantics are implemented.
19. **“Random distinct integers represent real data.”** Duplicates and structured patterns may dominate.
20. **“Fast average timing justifies a public comparator callback.”** Correctness, adversarial cost, and failure isolation remain.

## Worked Examples

### Example 1

**Question:** Apply Lomuto partition to $(4,1,3,2)$ using final value $2$ as pivot and strict less-than classification.

**Reasoning:** Boundary starts at $0$. Record $4$ is not less; $1$ is less, so swap it into boundary position, producing $(1,4,3,2)$ and advance boundary to $1$; $3$ is not less. Swap the pivot with position $1$, producing $(1,2,3,4)$.

**Conclusion:** Pivot index is $1$, left keys are below $2$, and right keys are at least $2$; only this scheme's caller may exclude index $1$.

### Example 2

**Question:** A Hoare partition returns split $s=3$ for $[0,8)$. Why is recursing on $[0,3)$ and $[4,8)$ suspicious?

**Reasoning:** A Hoare split commonly promises two ranges $[0,3)$ and $[3,8)$ or, under an inclusive version returning $j=2$, $[0,2]$ and $[3,7]$. It may not place a pivot at index $3$. Excluding $3$ without the exact contract can leave its record unsorted.

**Conclusion:** Derive recursive endpoints from the implementation's postcondition; the algorithm name does not define them.

### Example 3

**Question:** In three-way partition, why is $i$ unchanged after swapping a greater key with $A[gt-1]$?

**Reasoning:** The greater key is correctly moved into the new $[gt,hi)$ region. But the incoming record came from $[i,gt)$, which was unknown before decrement. It could be less, equal, or greater, so advancing $i$ would classify it without comparison.

**Conclusion:** Decrement $gt$, swap, and re-examine index $i$; the unknown length still decreases by one.

### Example 4

**Question:** Compare two-way one-sided equality and three-way behavior on 1000 equal keys.

**Reasoning:** A Lomuto strict-less partition fixes one pivot and sends 999 equals right, then 998, producing roughly $1000\cdot999/2$ classifications. A three-way partition scans once, returns an equal region of size 1000, and makes no recursive calls.

**Conclusion:** Duplicate policy changes the recursion from quadratic to linear on this input family.

### Example 5

**Question:** What is the common worst-case partition-comparison total for eight distinct keys under repeated extreme pivots?

**Reasoning:** Each partition compares the pivot with every other remaining key:

$$
7+6+5+4+3+2+1=\frac{8\cdot7}{2}=28.
$$

**Conclusion:** The degenerate distinct-key execution uses 28 pivot comparisons and has linear recursion height before stack control.

### Example 6

**Question:** Compute randomized quicksort's expected comparisons for five distinct ranks.

**Reasoning:** $H_5=1+1/2+1/3+1/4+1/5=137/60$. Therefore

$$
\mathbb E[C_5]
=2(6)\frac{137}{60}-20
=\frac{37}{5}
=7.4.
$$

An expectation need not be an integer because it averages integer counts across pivot executions.

**Conclusion:** The standard uniform-pivot distinct-key model yields 7.4 expected key comparisons at $n=5$.

### Example 7

**Question:** What is the probability that ranks $2$ and $5$ are compared in randomized quicksort?

**Reasoning:** They are compared only if the first pivot among ranks $2,3,4,5$ is rank $2$ or rank $5$. Two of four uniform candidates qualify:

$$
\Pr(X_{2,5}=1)=\frac{2}{4}=\frac12.
$$

**Conclusion:** Pairwise comparison probability depends on rank distance, not on their absolute values.

### Example 8

**Question:** A partition repeatedly produces sizes $0$ and $n-1$. What does smaller-side recursion change?

**Reasoning:** The empty side is the smaller side, so its recursive call returns immediately. The implementation iterates on the $n-1$ side in the same frame. It still scans $n,n-1,\ldots$ records, but no linear chain of live stack frames accumulates.

**Conclusion:** Stack depth becomes $O(\log n)$—in this trace effectively constant—while time remains $\Theta(n^2)$.

### Example 9

**Question:** Can ordinary comparisons quicksort a list containing NaN under an undeclared floating order?

**Reasoning:** NaN may be neither less than, equal to, nor greater than an ordinary number under language comparisons. A three-way classifier expecting exactly one of those outcomes may misclassify it as equal or violate partition exhaustiveness.

**Conclusion:** Define a total-order/key policy for exceptional values before invoking the sort.

### Example 10

**Question:** A public API sorts attacker-controlled keys with deterministic median-of-three and no fallback. What is missing?

**Reasoning:** Fixed sampling can have constructed bad patterns; comparator calls may also be expensive or malicious. Add a defined input/comparator resource policy, three-way duplicates, stack control, depth/progress monitoring, a worst-case-safe fallback, and bounded cancellation/failure semantics. Randomness can supplement but not replace deterministic limits.

**Conclusion:** Robustness comes from layered progress and resource controls, not from assuming typical inputs.

## Cross-Program Connections

- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) owns arrays, iterators, record identity, swap semantics, and dynamic partitioned structures.
- [Programming Languages & Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) owns comparator laws, NaN/total order, callbacks, exceptions, and mutation semantics.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns adversary models, denial-of-service exposure, seed secrecy, and untrusted callback/input policy.
- [Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) owns stack limits, integer overflow, byte movement, aliasing, and cancellation cleanup.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) owns cache, branch prediction, SIMD/block partition, and memory-bandwidth mechanisms.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns property, differential, fuzz, adversarial, and statistical performance testing.

## References

1. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. [*Introduction to Algorithms*, fourth edition](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), MIT Press, 2022. Quicksort correctness, randomized analysis, partitioning, and recurrences.
2. Donald E. Knuth. [*The Art of Computer Programming, Volume 3: Sorting and Searching*, second edition](https://www.informit.com/store/art-of-computer-programming-volume-3-sorting-and-searching-9780321635785), Addison-Wesley Professional, 1998. Foundational sorting and quicksort analysis.
3. C. A. R. Hoare. [“Quicksort”](https://doi.org/10.1093/comjnl/5.1.10), *The Computer Journal* 5(1), 1962, pp. 10–16. Primary algorithm and implementation analysis.
4. Robert Sedgewick and Kevin Wayne. [“Quicksort”](https://algs4.cs.princeton.edu/23quicksort/), companion to *Algorithms*, fourth edition, checked 2026-09-04. Two-way/three-way partitioning, shuffling, duplicates, implementation, and empirical study.
5. Jon L. Bentley and M. Douglas McIlroy. [“Engineering a Sort Function”](https://doi.org/10.1002/spe.4380231105), *Software: Practice and Experience* 23(11), 1993, pp. 1249–1265. Primary engineering evidence on sampling, three-way partitioning, robustness, and testbeds.
6. David R. Musser. [“Introspective Sorting and Selection Algorithms”](https://doi.org/10.1002/%28SICI%291097-024X%28199708%2927%3A8%3C983%3A%3AAID-SPE117%3E3.0.CO%3B2-%23), *Software: Practice and Experience* 27(8), 1997, pp. 983–993. Primary depth-limited fallback construction and worst-case protection.
7. ACM, IEEE Computer Society, and AAAI. [*Computer Science Curricula 2023: Algorithmic Foundations*](https://csed.acm.org/al-cs-core/), endorsed 2024; consulted 2026-09-04. Current curricular scope for partition sorting, randomized algorithms, correctness, analysis, and implementation trade-offs.

## Exercises

### Exercise 1

For each postcondition, identify whether it describes a Lomuto-style pivot placement, a Hoare-style split, or a three-way partition, and give the recursive half-open ranges: (a) $A[lo:p)<v$, $A[p]=v$, $A[p+1:hi)\ge v$; (b) every key in $A[lo:s)$ is at most every key in $A[s:hi)$ but the pivot position is unspecified; (c) $A[lo:lt)<v$, $A[lt:gt)=v$, $A[gt:hi)>v$.

### Exercise 2

Prove the half-open three-way partition correct from its four-region invariant and variant $gt-i$. Explain every cursor update, including why the greater-than branch does not increment $i$, and prove identity permutation.

### Exercise 3

Compute $\mathbb E[C_6]$ exactly for uniform-pivot quicksort on six distinct ranks. Separately compute the degenerate worst-case comparison count. State the assumptions that prevent either number from being a universal production prediction.

### Exercise 4

Apply recursive three-way quicksort with the first value as pivot to $(2,3,2,1,3,2,0)$. You may choose any swap order satisfying the reviewed partition contract. Show the first partition's region multisets/boundaries, the recursive subproblems, and the final sorted sequence. Explain why internal partition order is irrelevant to the proof.

### Exercise 5

A multitenant service accepts up to ten million records and a user-defined key callback. Inputs may be sorted, low-cardinality, or adversarial; callbacks can be slow, stateful, or fail; stack and latency are bounded; stability is not required, but every record must remain owned after failure. Design the partition, pivot, equality, stack, fallback, callback, cancellation, testing, telemetry, and evaluation policies.

## Answers to the Exercises

### Answer 1

(a) is a Lomuto-style or other pivot-placement contract. The pivot is complete at $p$, so recursively sort $[lo,p)$ and $[p+1,hi)$.

(b) is a Hoare-style split contract. Recursively sort $[lo,s)$ and $[s,hi)$, assuming the specific implementation proves both are strict subranges. Do not exclude $s$ as a pivot position.

(c) is a three-way contract. The equal range is complete, so recursively sort $[lo,lt)$ and $[gt,hi)$. Empty less, equal beyond the required pivot, or greater regions are handled naturally by half-open endpoints.

The exact caller remains conditional on the exact partition routine. Inclusive variants require a deliberate translation rather than copying these endpoints.

### Answer 2

Initially $lt=i=lo$ and $gt=hi$. The less, equal, and greater regions are empty; the unknown region is the whole range. Their disjoint union is $[lo,hi)$, and all predicates hold vacuously outside the unknown region.

If $A[i]<v$, swapping $A[lt]$ and $A[i]$ places the small record at the end of the less region. When $lt<i$, the equal record formerly at $lt$ moves to $i$; advancing both cursors includes it in the equal region. When $lt=i$, the self-swap is harmless. Unknown length falls by one.

If $A[i]=v$, advancing $i$ adds that record to the equal region and decreases unknown length by one.

If $A[i]>v$, decrement $gt$ first and swap positions $i$ and $gt$. The greater record enters the expanded greater region. The incoming record was unknown, so $i$ stays fixed for classification on the next iteration. Although $i$ does not advance, $gt-i$ decreases by one.

Swaps are bijections on array positions and cursor changes neither create nor destroy records, so identity permutation is preserved. The nonnegative integer $gt-i$ strictly decreases and reaches zero. Then the unknown region is empty, leaving exactly the less, equal, and greater postcondition regions.

### Answer 3

First,

$$
H_6=1+\frac12+\frac13+\frac14+\frac15+\frac16
=\frac{49}{20}.
$$

Therefore

$$
\mathbb E[C_6]
=2(7)\frac{49}{20}-24
=\frac{343}{10}-\frac{240}{10}
=\frac{103}{10}
=10.3.
$$

Repeated extreme pivots use

$$
\frac{6\cdot5}{2}=15
$$

comparisons in the one-per-other-record model.

The expectation assumes distinct ranks and independent uniform pivots (or an equivalent independent random permutation) with a specified partition comparison model. The worst number assumes repeated extremes and the same model. Duplicates, three-outcome comparisons, key cost, pivot sampling, cutoffs, input/adversary knowledge, and physical machine costs change production behavior.

### Answer 4

The first pivot is $2$. A correct three-way partition returns the multisets:

$$
\{1,0\}\mid\{2,2,2\}\mid\{3,3\}
$$

with lengths $2,3,2$ and relative boundaries $lt=2$, $gt=5$. One valid physical arrangement is

$$
(1,0,2,2,2,3,3).
$$

Recursively sort the less subrange $(1,0)$. With first pivot $1$, its three regions are $(0)\mid(1)\mid()$, yielding $(0,1)$. The greater subrange $(3,3)$ becomes one equal region and needs no further recursion. The middle key-$2$ region was already excluded.

The final sequence is

$$
(0,1,2,2,2,3,3).
$$

Another valid first partition could permute records within each region. The recursive proof needs only identity preservation and the cross-region predicates; recursive sorting establishes internal order where needed, while all equal middle keys are already ordered by equivalence.

### Answer 5

Use a half-open three-way partition with explicit less/equal/greater boundaries so repeated keys leave recursion in one pass. Cache or materialize validated keys when policy and memory permit; never let a stateful callback be invoked unpredictably without a contract. Reject comparators that demonstrably violate required ordering, set call/time budgets, and define callback failure/cancellation as leaving all record identities owned though order may be partially permuted.

Choose a pivot by bounded sampling or sound random selection, record the policy, and assume hostile patterns. Recurse on the smaller side and iterate the larger for $O(\log n)$ stack. Track a depth/progress budget and fall back to heapsort or another in-place $O(n\log n)$ worst-case algorithm. Use insertion only for bounded small ranges. Stability is not required, so swap-based partition is acceptable.

Place hard limits on records, key bytes, callback duration/calls, cancellation checkpoints, and total work. Isolate untrusted callback execution as the platform permits; snapshot keys if repeated calls could change. On failure, retain a valid owner/container for every record and report that order is unspecified unless sorting was done in a private index/copy.

Test empty/singleton, sorted, reverse, rotations, organ-pipe, sawtooth, all equal, low-cardinality, duplicate clusters, maximum size, adversarial sampler patterns, biased/repeated seeds, callback exceptions, inconsistent results, timeouts, cancellation at each loop region, and fallback boundaries. Assert identity multisets and partition predicates after instrumented steps, then differential-sort successful small cases against a trusted reference.

Record pivot ranks, three region sizes, depth, fallback/cutoff counts, comparisons, callback calls/time, swaps/bytes, cancellation latency, failures, memory, and end-to-end latency. Evaluate identical inputs across policies with preserved seeds and raw results. Ship only a configuration meeting deterministic resource limits and bounded workload evidence; do not rely on expected timing alone for hostile tenants.
