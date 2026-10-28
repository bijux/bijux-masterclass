---
module_id: ALGE-017
program: Algorithm Engineering
level: 1
module_number: 17
title: Order Statistics and Quickselect
status: complete
last_verified: 2026-09-04
---

# Order Statistics and Quickselect

## One-Page Review

### Governing question

How can one rank be selected without fully sorting, and how should partition contracts, duplicates, randomized expectation, deterministic fallback, identity, mutation, and service-level resource limits be specified?

### Essential definitions

- The **order statistic of zero-based rank $k$** is the value that would occupy index $k$ after sorting, for $0\le k<n$.
- **Selection** finds an order statistic; it need not order either side internally.
- **Quickselect** partitions around a pivot, then continues into only the region containing the requested rank.
- A **three-way partition** returns less-than, equal-to, and greater-than regions and can finish any rank inside the equal region at once.
- A **randomized pivot** is sampled independently and uniformly from the current active records under the standard expected analysis.
- A **good pivot** leaves the continuing region no larger than a fixed fraction of the current range.
- **Median of medians** selects a pivot recursively from small-group medians to obtain deterministic linear worst-case selection.
- **Introselect** uses a fast ordinary selection policy and switches to a worst-case-safe method after a progress or depth budget is exhausted.
- A **quantile convention** maps a probability or percentile to one or more ranks; conventions differ and must be named.

### Central model, mechanism, or theorem

For sorted values

$$
x_{(0)}\le x_{(1)}\le\cdots\le x_{(n-1)},
$$

selection returns $x_{(k)}$. With duplicates, value $v$ is valid exactly when

$$
\#\{x:x<v\}\le k<\#\{x:x\le v\}.
$$

A partition taking $\Theta(n)$ work and leaving one continuing side of size $s$ gives

$$
T(n)=T(s)+\Theta(n).
$$

Repeated extreme pivots produce $\Theta(n^2)$ work. Independent uniform pivots produce expected $\Theta(n)$ work: a middle-half pivot occurs with probability at least $1/2$, costs expected at most two trials per shrink phase, and reduces the continuing size to at most $3/4$.

Classic groups-of-five median-of-medians satisfies the coarse recurrence

$$
T(n)
\le
T(\lceil n/5\rceil)
+
T(7n/10+6)
+
cn
=O(n).
$$

### Critical invariants

- Validate zero-based or one-based rank semantics before mutating input.
- The requested global rank remains inside the active half-open range.
- Regions discarded to the left cannot contain a value greater than the selected value; regions discarded right cannot contain a smaller value.
- Partition boundaries and equality policy belong to the specific partition routine.
- Every iteration excludes a nonempty pivot/equal region, so the active length strictly decreases.
- Partition and active-range updates preserve every record identity exactly once.
- If $k$ enters the equal region, the selected value is complete even though equal-record identity order is arbitrary.
- Randomized expected bounds require fresh unbiased choices independent of the fixed input and relevant adversary.
- Pivot sampling is not a deterministic worst-case guarantee.
- Deterministic fallback must preserve the same range, comparator, rank, identity, and failure contracts.
- A selected prefix contains small records but is not necessarily sorted.

### Common failures

Common failures include mixing zero- and one-based ranks; using a statistical median average when an input record is required; failing to validate empty input or $k=n$; copying quicksort recursion and processing both sides; mixing Hoare and Lomuto boundary meanings; recursing on the pivot/equal region; losing the global rank when rebasing a subarray; degrading quadratically on all-equal keys; saying randomization guarantees linear time; reusing a biased or attacker-visible random source; claiming sampling alone gives a worst-case bound; assuming the selected prefix is sorted; promising a stable equal-record identity without a tie rule; and hiding partial mutation after comparator failure.

### Compact example

Select rank $5$ from $(9,1,8,2,7,3,6,4,5,5,5)$. Partitioning around $3$ can produce less region $[0,2)$, equal region $[2,3)$, and a right active region $[3,11)$. Partitioning that right region around $5$ can produce equal region $[4,7)$, which contains rank $5$. The selected value is $5$; neither side needs full sorting.

### Connections

[ALGE-006](./006-best-worst-expected-and-amortized-cost.md) supplies expected-cost discipline; [ALGE-008](./008-lower-bounds-and-adversary-arguments.md) supplies lower-bound and adversary reasoning; [ALGE-014](./014-quicksort-and-partitioning.md) proves partition contracts; [ALGE-015](./015-heapsort.md) supplies one bounded fallback/tool for top-$k$ work; and ALGE-019 will integrate adaptive and introspective policies.

## Governing Question

How should an exact rank-selection algorithm be derived and reviewed so it saves work relative to sorting without weakening order semantics, worst-case controls, failure ownership, or reproducibility?

Selection is a partial-order problem. The result needs enough evidence to prove which value belongs at one rank; it does not need the complete pairwise order that a sort establishes. Quickselect exploits this by abandoning one partition side after every pivot.

That economy creates its own obligations. The caller and partition must agree on boundaries. Duplicate keys need interval rank semantics. Expected linearity needs an explicit probability space. A public service may require a deterministic fallback even when ordinary random pivots are fast. In-place selection can partially permute records before failure, and the chosen equal-key identity may be observable.

## Why This Matters

Medians, percentiles, thresholding, top-$k$ pipelines, robust statistics, scheduling, graphics, database operators, and monitoring systems frequently need ranks without a full order. Sorting first costs $O(n\log n)$ comparisons, while selection can use linear work.

The difference matters most when $n$ is large and only one or a few ranks are needed. It matters less when the caller immediately needs every result sorted, performs many rank queries, cannot mutate input, or consumes a stream that cannot be retained. Choosing quickselect merely because “it is linear” can be wrong when randomness is predictable, duplicates are mishandled, the comparator is hostile, or the API's quantile convention does not match the product definition.

This module therefore separates selected value, selected record identity, partial partition layout, probability model, deterministic ceiling, auxiliary storage, and physical runtime.

## Prerequisites and Retrieval

Retrieve:

- zero-based half-open arrays, sorted permutations, ranks, and duplicates;
- two-way and three-way partition postconditions;
- loop invariants, variants, induction, and recurrence trees;
- expectation, geometric waiting time, conditional probability, and random pivots;
- comparison lower bounds, adversaries, and deterministic fallback;
- medians, percentiles, quantile conventions, and top-$k$ outputs;
- comparator laws, mutation, identity, cancellation, and failure safety.

You should be able to prove a partition's regions, distinguish a value from a record identity, and state whether an asymptotic result is worst-case, expected, amortized, or empirical.

## Learning Objectives

After completing this module, you should be able to:

1. define zero-based order statistics and duplicate-aware rank intervals;
2. distinguish selection, partial partitioning, top-$k$, quantiles, and full sorting;
3. derive iterative three-way quickselect from a partition contract;
4. prove its active-range invariant, progress, permutation, and selected-rank postcondition;
5. derive quadratic behavior under repeated extreme pivots;
6. prove expected linear work for independent uniform pivots using good-pivot phases;
7. derive the groups-of-five median-of-medians recurrence and linear bound;
8. compare random, sampled, deterministic, heap, sorting, and introselect approaches;
9. specify duplicate identity, comparator, randomness, cancellation, and partial-mutation policies;
10. validate an exact selection service under unfamiliar rank and workload requirements.

## Core Exposition

### Define rank before choosing an algorithm

For nonempty input multiset sorted as

$$
x_{(0)}\le x_{(1)}\le\cdots\le x_{(n-1)},
$$

the zero-based order statistic of rank $k$ is $x_{(k)}$, where

$$
0\le k<n.
$$

One-based descriptions call the same value the $(k+1)$st smallest. An API must choose one convention and reject out-of-range ranks before mutation.

For distinct values, exactly $k$ inputs are smaller than $x_{(k)}$. With duplicates, a selected value $v$ may occupy an interval of sorted ranks. The robust condition is

$$
L(v)=\#\{x:x<v\},
\qquad
E(v)=\#\{x:x=v\},
$$

$$
L(v)\le k<L(v)+E(v).
$$

This defines the value, not a unique equal-key record. If identity matters, add a tie rule such as original position and select under that total key.

### Separate medians and quantile conventions

For odd $n$, the middle zero-based rank is $\lfloor n/2\rfloor$. For even $n$, applications may choose:

- lower median at rank $n/2-1$;
- upper median at rank $n/2$;
- arithmetic average of those two values;
- an interpolated quantile under another named convention.

The average may not be an input record, may be meaningless for ordinal keys, and may overflow or lose precision. Selection returns input order statistics; quantile interpolation is a separate semantic operation.

The same discipline applies to percentiles. A request for “p99” is incomplete until sample inclusion, endpoint, interpolation, and rank-rounding conventions are stated.

### State the selection postcondition

An in-place selector for rank $k$ may promise:

$$
\forall i<k,\qquad A[i]\le A[k],
$$

$$
\forall i>k,\qquad A[i]\ge A[k],
$$

plus identity permutation. It does not promise:

$$
A[0]\le A[1]\le\cdots\le A[n-1].
$$

The prefix $A[0:k)$ contains $k$ records no greater than the selected record, but their internal order is unspecified. If the caller wants the smallest $k$ records sorted, it must sort that prefix or use a different operation.

A nonmutating selector can copy records or indices and provide the same value result with additional space. Mutation behavior belongs in the API, not in an implementation footnote.

### Derive three-way quickselect

Maintain an active half-open range $A[lo:hi)$ containing the requested global rank $k$. Choose pivot value $v$ from that active range and partition into:

$$
A[lo:lt)<v,
$$

$$
A[lt:gt)=v,
$$

$$
A[gt:hi)>v.
$$

Then:

- if $k<lt$, set $hi=lt$;
- if $k\ge gt$, set $lo=gt$;
- otherwise $lt\le k<gt$, so return value $v$ or the record currently at $A[k]$.

No rank rebasing is required because $k$, $lo$, $lt$, $gt$, and $hi$ remain indices in the original array. An implementation using copied subarrays may instead use local ranks and must transform them explicitly.

Three-way partition is especially important for duplicates. It finishes every rank in the equal interval together and excludes all pivot-equivalent records from further work.

### Prove the active-range invariant

Maintain:

1. $0\le lo\le k<hi\le n$;
2. some record with global sorted rank $k$ lies in $A[lo:hi)$;
3. every record before $lo$ is no greater than every possible target in the active range;
4. every record from $hi$ onward is no less than every possible target;
5. the whole array is an identity permutation of the input.

Initially $[lo,hi)=[0,n)$, so outside regions are empty.

After partition, if $k<lt$, there are enough records in the less region to contain rank $k$. Equal and greater records cannot be smaller candidates, so discarding $[lt,hi)$ preserves the target. The symmetric argument applies when $k\ge gt$.

If $k$ lies in $[lt,gt)$, the number of strictly smaller records is at most $k$ and the number of records no greater than $v$ exceeds $k$. Therefore $v=x_{(k)}$.

The pivot came from the nonempty active range, so $lt<gt$. Either continuing branch excludes this equal range and strictly reduces $hi-lo$. Swaps preserve identity. Thus the loop terminates with the selection postcondition.

### Derive the one-sided recurrence

A partition scans the active range in $\Theta(n)$ work. Unlike quicksort, quickselect follows only one side:

$$
T(n)=T(s)+\Theta(n),
$$

where $s$ is the continuing region size.

If each pivot is extreme on distinct keys, $s=n-1$ repeatedly:

$$
T(n)=T(n-1)+\Theta(n)=\Theta(n^2).
$$

In a one-comparison-per-other-record model, the exact partition total is

$$
(n-1)+(n-2)+\cdots+1
=\frac{n(n-1)}2.
$$

If every continuing size is at most $\alpha n$ for fixed $\alpha<1$, then

$$
T(n)
\le
cn+c\alpha n+c\alpha^2n+\cdots
=\frac{cn}{1-\alpha}
=O(n).
$$

The algorithm's cost is controlled by eliminated volume, not by whether the discarded region is internally sorted.

### Prove randomized expected linear work

Fix the input and target rank. At every active range of size $m$, choose each active record independently with probability $1/m$. Call a pivot good when its rank lies in the middle half of the active order. At least half of the ranks are good, up to rounding, and a good pivot leaves a continuing side of size at most $3m/4$.

The expected number of independent trials until a good pivot is at most $2$. Charge every unsuccessful partition in that phase the phase's starting upper cost $cm$. The expected work before the active bound shrinks is at most $2cm$.

Summing phases:

$$
\mathbb E[T(n)]
\le
2c\left(
n+\frac34n+\left(\frac34\right)^2n+\cdots
\right)
=8cn
=O(n).
$$

Rounding changes constants, not the result. The proof requires uniform choices independent of the fixed input. A deterministic first pivot, biased generator, reused predictable seed, adaptive comparator, or adversary observing choices is a different model. Even under the model, quadratic executions remain possible; they simply have small probability.

### Handle duplicates as rank intervals

Two-way selection can repeatedly place equals on one side and make poor progress on low-cardinality data. A three-way partition returns an equal interval whose length is exactly the pivot multiplicity within the active range.

If $k$ enters that interval, no identity among the equal records is mathematically distinguished. Returning $A[k]$ is valid under a value-only contract, but repeated calls or different pivot policies may return another equal-key identity.

For stable tie selection, compare composite keys:

$$
(\operatorname{semantic\ key},\operatorname{original\ position}).
$$

This makes every record rank unique but adds key state and can reduce the duplicate shortcut because formerly equal semantic keys are now distinct under the composite order. Another API can return the whole equal range or only the value, making nondeterministic identity unobservable.

### Derive deterministic median of medians

The classic groups-of-five method:

1. divide the active records into groups of at most five;
2. sort each full group and move/extract its median;
3. recursively select the median of those medians as pivot $p$;
4. three-way partition the original active range around $p$;
5. continue only into the rank-containing side.

For full groups, at least half of the group medians are no less than $p$, and each such median has at least three group elements no less than it. Symmetrically, many elements are no greater than $p$. After accounting conservatively for the pivot group, an incomplete group, and rounding, at least

$$
\frac{3n}{10}-6
$$

elements lie on each protected side for sufficiently large $n$.

Therefore the continuing partition has size at most $7n/10+6$, while selecting the pivot among medians costs a subproblem of size at most $\lceil n/5\rceil$:

$$
T(n)
\le
T(\lceil n/5\rceil)
+
T(7n/10+6)
+
cn.
$$

The recursive fractions sum below $1$, so the recurrence is $O(n)$. For example, once $n\ge140$, the two size bounds sum to at most $.95n$; induction with a sufficiently large linear constant absorbs work and base cases.

The method proves a deterministic ceiling, not automatically the smallest finite constant on ordinary data. Group sorting, median movement, and recursive pivot selection can make it slower than randomized or sampled policies.

### Use introselect and sampling with explicit guarantees

Small fixed samples, median-of-three, ninthers, or Floyd–Rivest-style sampling can reduce expected partition imbalance. Their analysis and constants belong to their exact policies. A sample heuristic alone does not rule out constructed bad inputs.

Introselect starts with a practical pivot/partition strategy and monitors a budget such as accumulated work, active-size progress, or partition depth. When the budget is exhausted, it invokes deterministic linear selection or another fallback that satisfies the required worst-case ceiling.

The handoff must preserve:

- the exact active range and global/local rank mapping;
- comparator and key semantics;
- three-way duplicate behavior or an equivalent progress rule;
- identity ownership and mutation state;
- cancellation, allocation, and error contracts;
- observability of fallback counts and reasons.

A heap-based fallback can be useful for extreme ranks or streaming top-$k$, but its $O(n\log k)$ behavior is not deterministic linear selection for arbitrary median ranks.

### Preserve executable selection evidence

The following iterative selector uses the reviewed half-open three-way contract and a deterministic middle-position pivot only to make the trace reproducible. Each classification counts one less-than Boolean test and a second greater-than test when needed.

<!-- bijux-verify: {"id":"three-way-quickselect-ledger","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"input=(9, 1, 8, 2, 7, 3, 6, 4, 5, 5, 5)\nrank=5 selected=5\ntrace=((0, 11, 3, 2, 3, 20), (3, 11, 5, 4, 7, 15))\npartitioned=(1, 2, 3, 4, 5, 5, 5, 6, 8, 9, 7)\nleft=(1, 2, 3, 4, 5) right=(5, 6, 8, 9, 7)\ncomparisons=35 contract=True\n","stderr":""}} -->
~~~python
from collections import Counter


def partition_three_way(items, lo, hi, pivot):
    lt = lo
    index = lo
    gt = hi
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

    return lt, gt, comparisons


def quickselect(values, rank):
    if not 0 <= rank < len(values):
        raise ValueError("rank outside input")

    items = list(values)
    lo = 0
    hi = len(items)
    trace = []
    comparisons = 0

    while True:
        pivot = items[lo + (hi - lo) // 2]
        lt, gt, used = partition_three_way(items, lo, hi, pivot)
        comparisons += used
        trace.append((lo, hi, pivot, lt, gt, used))

        if rank < lt:
            hi = lt
        elif rank >= gt:
            lo = gt
        else:
            return items, trace, comparisons


values = (9, 1, 8, 2, 7, 3, 6, 4, 5, 5, 5)
rank = 5
items, trace, comparisons = quickselect(values, rank)
selected = items[rank]
contract = (
    Counter(items) == Counter(values)
    and all(value <= selected for value in items[:rank])
    and all(value >= selected for value in items[rank + 1 :])
)

print(f"input={values}")
print(f"rank={rank} selected={selected}")
print(f"trace={tuple(trace)}")
print(f"partitioned={tuple(items)}")
print(f"left={tuple(items[:rank])} right={tuple(items[rank + 1:])}")
print(f"comparisons={comparisons} contract={contract}")
~~~

The final right side $(5,6,8,9,7)$ is not internally sorted and need not be. The deterministic pivot policy is deliberately not presented as an expected or worst-case protection mechanism.

### Choose selection, heaps, or sorting from the output contract

For one exact rank on retained mutable data:

- randomized three-way quickselect offers expected $O(n)$ work under its model;
- median of medians offers deterministic $O(n)$ work;
- introselect can combine ordinary constants with a deterministic ceiling.

For the smallest $k$ records:

- quickselect partitions in expected $O(n)$ and sorting the prefix costs $O(k\log k)$;
- a size-$k$ max heap uses $O(k)$ memory and $O(n\log k)$ time and supports streaming;
- full sorting costs $O(n\log n)$ but answers every later rank and ordered traversal.

For many rank queries, repeated independent selection may redo work. A full sort, multiselection algorithm, histogram, order-statistic tree, or approximate quantile sketch may better fit the lifecycle. Approximate streaming quantiles answer a different contract and require error/confidence semantics.

### Engineer failure, reproducibility, and evaluation

Validate $n>0$ and $0\le k<n$ before mutation. Define comparator totality for NaN, nulls, locale, and exceptional values. Cache immutable keys if repeated calls may be stateful or expensive.

An in-place partition can fail after arbitrary exchanges. Unless implemented on a private copy/index, promise identity ownership and a partially permuted state rather than rollback. Cancellation checkpoints belong between bounded partition blocks or active iterations, with maximum response latency measured.

For randomized selection, record the generator family, seed provenance, sampling method, rejection handling, and whether adversaries observe choices. Deterministic replay may require logging a seed, but exposing/reusing that seed can weaken adversarial protection. Service resource limits should not depend solely on expected behavior.

Validate empty/rank rejection, singleton, minimum, maximum, both even medians, all equal, low cardinality, sorted, reverse, organ-pipe, sawtooth, repeated extremes, wide records, expensive keys, inconsistent callbacks, cancellation, and fallback boundaries. Assert selected value against a trusted sorted copy on bounded tests, identity permutation, side inequalities, active-range progress, and equal-region termination.

Measure comparisons, key projections, swaps/bytes, active sizes, pivot ranks, equal-region sizes, iterations, maximum live storage, fallback count/reason, random retries, callback time, cancellation latency, and tail time. Preserve seeds and raw traces.

## Definitions and Notation

- $n$ is the number of records.
- $k\in[0,n)$ is a zero-based requested rank.
- $x_{(k)}$ is the value at index $k$ in nondecreasing order.
- $L(v)$ counts keys strictly less than value $v$.
- $E(v)$ counts keys equal to $v$.
- $A[lo:hi)$ is the active half-open range.
- $[lt,gt)$ is the pivot-equal region after three-way partition.
- $s$ is the one continuing subproblem size.
- A good pivot lies in a declared middle rank interval and guarantees a fractional shrink.
- Expected time averages over the named pivot randomness for a fixed accepted input.
- Median of medians refers here to the classic groups-of-five deterministic pivot construction.
- A partial selection layout satisfies side inequalities but not internal side order.
- Selected value and selected record identity are different contracts when keys repeat.

## Mechanisms, Invariants, or Proof Structure

Use this sequence to review an order-statistic implementation:

1. State zero-/one-based rank, duplicate semantics, median/quantile convention, and output shape.
2. Validate nonempty input and the complete rank domain before mutation.
3. State key/comparator totality and selected value versus identity policy.
4. State exact partition endpoints, equality regions, and permutation contract.
5. Maintain that the global target rank lies inside the active half-open range.
6. Prove left/right discarded regions cannot contain the target value.
7. Prove the equal interval satisfies the duplicate-aware rank inequality.
8. Prove every continuing branch strictly shortens the active range.
9. Derive one-sided work from the sequence of active sizes.
10. State worst-case pivot sequences independently of expected pivot models.
11. For random pivots, state uniformity, independence, fixed input, and adversary visibility.
12. For deterministic selection, derive protected-side counts and solve the recurrence.
13. Align introselect or heap fallback range, rank, comparator, identity, and failure semantics.
14. Define mutation, rollback, cancellation, reproducibility, and resource-limit behavior.
15. Reproduce a finite trace and test every rank across structured/adversarial families.

The core logical chain is:

$$
\text{partition contract}
\Longrightarrow
\text{rank-containing active region}
\Longrightarrow
\text{strict progress}
\Longrightarrow
\text{selected order statistic}.
$$

Cost then depends on the active-size sequence:

$$
T=\Theta(n_0+n_1+\cdots),
\qquad n_{t+1}<n_t.
$$

## Alternatives and Trade-Offs

| Approach | Time guarantee | Extra storage | Mutates input | Best fit |
|---|---:|---:|---:|---|
| Three-way randomized quickselect | Expected $O(n)$ under model; $O(n^2)$ possible | $O(1)$ iterative | Usually | One rank, ordinary data |
| Median of medians | Worst-case $O(n)$ | Implementation dependent | Usually | Deterministic selection ceiling |
| Introselect | Worst-case bound set by fallback | Usually small | Usually | Practical exact selection service |
| Full stable sort | $O(n\log n)$ | Often $O(n)$ | Policy dependent | Many ranks and ordered output |
| Size-$k$ heap | $O(n\log k)$ | $O(k)$ | No source mutation needed | Streaming/extreme top-$k$ |
| Counting/histogram selection | $O(n+K)$ | $O(K)$ | No | Dense bounded integer domain |
| Order-statistic tree | $O(\log n)$ per dynamic rank query | $O(n)$ | Separate structure | Repeated updates and queries |
| Quantile sketch | Model-specific approximate bounds | Sublinear possible | Streaming | Approximation explicitly allowed |

No row dominates without the lifecycle contract. Exactness, stability, streaming, updates, number of queries, mutation, memory, adversaries, and output order decide the method.

## Failure Modes and Misconceptions

1. **Rank-base mismatch:** “fifth” is passed as index $5$ instead of $4$.
2. **Empty-input selection:** a pivot is read before validating $n>0$.
3. **Even-median ambiguity:** lower, upper, and interpolated medians are conflated.
4. **Duplicate rank error:** exactly $k$ strictly smaller values is demanded when ties span $k$.
5. **Identity/value conflation:** an arbitrary equal record is presented as a stable choice.
6. **Full-sort postcondition:** internally unordered selected sides are reported as sorted.
7. **Quicksort copy:** both partition sides are processed, wasting the selection advantage.
8. **Boundary mix:** a Hoare split is treated as a placed pivot index.
9. **Equal-region recursion:** the same duplicate block is selected repeatedly.
10. **Rank rebasing error:** global $k$ is used as a local copied-subarray index or vice versa.
11. **No-progress pivot:** active endpoints retain the full prior range.
12. **Random-guarantee claim:** expected linear work is labeled deterministic linear time.
13. **Biased sampling:** modulo reduction or a weak generator distorts pivot ranks.
14. **Visible randomness:** an adaptive adversary constructs bad continuing ranges.
15. **Sampling-as-proof:** median-of-three is claimed to eliminate worst cases.
16. **BFPRT recurrence omission:** pivot-selection recursion is excluded from cost.
17. **Group guarantee overstatement:** rounding and incomplete groups are ignored.
18. **Heap/selection confusion:** an $O(n\log k)$ streaming method is called linear median selection.
19. **Mutation surprise:** callers expect original order after in-place selection.
20. **Rollback fiction:** comparator failure after swaps is described as atomic.
21. **NaN order gap:** side predicates are not exhaustive under a partial comparison.
22. **Repeated-query myopia:** many ranks repeatedly rescan data instead of sharing work.
23. **Seed-only reproducibility:** code, input identities, comparator, and policy version are omitted.
24. **Benchmark rank monoculture:** only medians or only random ranks are measured.

## Worked Examples

### Example 1

**Question:** Which ranks select value $2$ from sorted multiset $(1,2,2,2,4)$?

**Reasoning:** $L(2)=1$ and $E(2)=3$, so $1\le k<4$.

**Conclusion:** Zero-based ranks $1,2,3$ all select value $2$; no equal-record identity is unique without a tie rule.

### Example 2

**Question:** What are the medians of $(1,4,9,10)$?

**Reasoning:** Lower rank $1$ gives $4$; upper rank $2$ gives $9$; arithmetic interpolation gives $(4+9)/2=6.5$.

**Conclusion:** “Median” can mean two input order statistics or a non-input numeric value; the API must specify which.

### Example 3

**Question:** Select zero-based rank $5$ from $(9,1,8,2,7,3,6,4,5,5,5)$ using the executable trace.

**Reasoning:** Pivot $3$ returns equal range $[2,3)$, so continue in $[3,11)$. Pivot $5$ returns $[4,7)$, which contains $5$.

**Conclusion:** Value $5$ is selected after two partitions and 35 declared Boolean comparisons; full sorting is unnecessary.

### Example 4

**Question:** Does layout $(1,2,3,4,5,5,5,6,8,9,7)$ count as correct selection at rank $5$?

**Reasoning:** Every position before $5$ is at most $5$, and every later position is at least $5$. The suffix is not sorted because $9>7$, but selection never promised it.

**Conclusion:** The layout satisfies selection and permutation while failing full-sort order, exactly as allowed.

### Example 5

**Question:** How many pivot comparisons can repeated extreme quickselect use on eight distinct records?

**Reasoning:**

$$
7+6+5+4+3+2+1
=\frac{8\cdot7}{2}
=28.
$$

**Conclusion:** One-sided recursion does not prevent quadratic work when only one record is eliminated each time.

### Example 6

**Question:** Why does the middle-half pivot argument give an $8cn$ expected upper bound?

**Reasoning:** A good pivot appears with probability at least $1/2$, so expected trials per shrink phase are at most $2$. Each good pivot reduces size bound by $3/4$:

$$
2c n\sum_{t\ge0}(3/4)^t
=2cn\cdot4
=8cn.
$$

**Conclusion:** The constant belongs to a coarse proof; the durable result is expected linear work under the stated sampling model.

### Example 7

**Question:** What coarse protection does median of medians state at $n=100$?

**Reasoning:** The bound $3n/10-6$ protects at least $24$ elements on either side. The recurrence's coarse continuing-side ceiling is $7n/10+6=76$.

**Conclusion:** A constant fraction is eliminated deterministically; rounding makes this bound conservative.

### Example 8

**Question:** Compare two-way and three-way selection on one million equal keys.

**Reasoning:** A one-sided equality policy may fix one pivot and continue on $n-1$ equals repeatedly. Three-way partition scans once and returns an equal interval spanning the entire range.

**Conclusion:** Three-way equality changes this family from potential quadratic work to one linear partition.

### Example 9

**Question:** A stream has one million records but only the smallest 100 must be retained and sorted. Which method fits?

**Reasoning:** In-place quickselect requires retaining and mutating the million records. A size-100 max heap retains $O(100)$ records, processes each arrival in $O(\log100)$ worst-case update time, then sorts the retained set.

**Conclusion:** Heap selection's $O(n\log k)$ time can beat an expected-linear method on lifecycle and memory even when its asymptotic comparison count is larger.

### Example 10

**Question:** What protects a public exact-percentile endpoint from constructed pivot sequences?

**Reasoning:** Use three-way duplicates, unbiased hidden sampling where appropriate, checked active progress, an accumulated-work/depth budget, and a deterministic linear fallback. Bound comparator/key cost, validate ranks, and define cancellation and partial mutation.

**Conclusion:** Expected pivot quality is one layer; contractual protection needs deterministic resource and failure controls.

## Cross-Program Connections

- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) owns heaps, order-statistic trees, dynamic ranks, and streaming containers.
- [Programming Languages & Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) owns comparator laws, NaN, generic identity, callbacks, exceptions, and mutation contracts.
- [Theory of Computation & Complexity](../../15-theory-of-computation-and-complexity/ROADMAP.md) owns comparison lower bounds, adversaries, randomization models, and recurrence proof foundations.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) owns distributed quantiles, sketches, stream windows, and pipeline materialization.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns adversarial inputs, randomness exposure, denial-of-service limits, and hostile callbacks.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns property, differential, statistical, fault-injection, and performance testing.

## References

1. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. [*Introduction to Algorithms*, fourth edition](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), MIT Press, 2022. Order statistics, randomized selection, deterministic selection, proofs, and recurrences.
2. Donald E. Knuth. [*The Art of Computer Programming, Volume 3: Sorting and Searching*, second edition](https://www.informit.com/store/art-of-computer-programming-volume-3-sorting-and-searching-9780321635785), Addison-Wesley Professional, 1998. Selection foundations and comparison analysis.
3. C. A. R. Hoare. [“Algorithm 65: Find”](https://doi.org/10.1145/366622.366647), *Communications of the ACM* 4(7), 1961, pp. 321–322. Primary partition-based selection algorithm.
4. Manuel Blum, Robert W. Floyd, Vaughan Pratt, Ronald L. Rivest, and Robert E. Tarjan. [“Time Bounds for Selection”](https://doi.org/10.1016/S0022-0000%2873%2980033-9), *Journal of Computer and System Sciences* 7(4), 1973, pp. 448–461. Primary deterministic linear-time selection result.
5. Robert W. Floyd and Ronald L. Rivest. [“Expected Time Bounds for Selection”](https://doi.org/10.1145/360680.360691), *Communications of the ACM* 18(3), 1975, pp. 165–172. Primary sampling-based expected selection analysis.
6. Robert Sedgewick and Kevin Wayne. [“Quicksort”](https://algs4.cs.princeton.edu/23quicksort/), companion to *Algorithms*, fourth edition, last modified 2022; consulted 2026-09-04. Partition contracts, quickselect, randomization, duplicates, and implementation context.
7. ACM, IEEE Computer Society, and AAAI. [*Computer Science Curricula 2023: Algorithmic Foundations*](https://csed.acm.org/al-cs-core/), endorsed 2024; consulted 2026-09-04. Current curricular scope for randomized algorithms, invariants, complexity, empirical analysis, and core data structures.

## Exercises

### Exercise 1

For input $(7,2,2,9,2,5,5)$, give every zero-based order statistic, the duplicate-validity intervals for values $2$ and $5$, the lower/upper median ranks and values, and the side postcondition required after selecting rank $4$. Explain what remains unspecified about equal-record identities.

### Exercise 2

Prove iterative three-way quickselect correct on $A[lo:hi)$ with global rank $k$. State initialization, preservation for both continuing branches, the equal-region return proof, a strict progress variant, identity permutation, and the final side inequalities. Cover empty, singleton, and all-equal boundaries.

### Exercise 3

Give the good-pivot phase proof that independent uniform-pivot quickselect has expected $O(n)$ work. State the probability space, derive the expected trials per phase and geometric work sum, and list at least four conditions under which the proof does not justify a production guarantee.

### Exercise 4

Derive the groups-of-five median-of-medians recurrence

$$
T(n)\le T(\lceil n/5\rceil)+T(7n/10+6)+cn
$$

and prove it is $O(n)$ by induction outside a sufficiently large base range. Explain why this deterministic theorem does not prove that the method is fastest on ordinary finite inputs.

### Exercise 5

A multitenant API computes one exact percentile from up to one hundred million mutable records. Keys may repeat, contain exceptional floating values, or be produced by slow/failing callbacks. Attackers choose inputs; p99 semantics, record identity, cancellation, tail latency, and failure ownership are contractual. Design rank mapping, comparator/key policy, partition/pivot/fallback, randomness, mutation, limits, validation, telemetry, and competing baselines.

## Answers to the Exercises

### Answer 1

Sorting the values gives

$$
(2,2,2,5,5,7,9).
$$

Thus:

$$
\begin{array}{c|ccccccc}
k&0&1&2&3&4&5&6\\
\hline
x_{(k)}&2&2&2&5&5&7&9
\end{array}
$$

For value $2$, $L(2)=0$ and $E(2)=3$, so valid ranks are $0\le k<3$. For value $5$, $L(5)=3$ and $E(5)=2$, so valid ranks are $3\le k<5$.

With $n=7$, both lower and upper median conventions choose rank $\lfloor7/2\rfloor=3$, value $5$. After selecting rank $4$, the selected value is also $5$, every position below $4$ must have key at most $5$, every position above $4$ must have key at least $5$, and the whole layout must be an identity permutation.

Unless records are compared by a composite tie key, either original key-$5$ identity may occupy index $4$, and the three key-$2$ identities may appear in any order. Value correctness does not imply stable identity selection.

### Answer 2

Reject empty input and any $k\notin[0,n)$ before entering the loop. Initially $lo=0$, $hi=n$, so $lo\le k<hi$, the target lies in the whole array, outside regions are empty, and identity permutation holds.

Partition the active range into less $[lo,lt)$, equal $[lt,gt)$, and greater $[gt,hi)$. If $k<lt$, the first $lt$ global positions can be filled from records strictly below the pivot plus previously discarded lower records, so the target cannot be in the equal/greater part; setting $hi=lt$ preserves the target and right-bound relation. If $k\ge gt$, enough less/equal records precede the target, so setting $lo=gt$ preserves it and the left-bound relation.

If $lt\le k<gt$, all active records before $lt$ are below pivot and all from $gt$ are above. Previously discarded left/right regions satisfy the same directional relation. Therefore the number below $v$ is at most $k$ and the number no greater than $v$ exceeds $k$, proving $v=x_{(k)}$. These relations also imply every physical position below $k$ is at most $A[k]$ and every later position is at least it.

Because the pivot is selected from the active nonempty range, $lt<gt$. Either continuing branch excludes $[lt,gt)$, so variant $hi-lo$ strictly decreases. Partition swaps are bijections, endpoint changes do not alter records, and therefore identity permutation persists. Termination follows.

Empty input is rejected. A singleton produces equal interval covering its only index and returns. An all-equal range produces $lt=lo$, $gt=hi$ and returns any valid rank after one partition.

### Answer 3

Fix an accepted input and target rank. At each active size $m$, sample every active record independently and uniformly. At least half of rank positions lie in the middle half, so a good pivot has probability at least $1/2$ up to harmless rounding. Its continuing side has size at most $3m/4$.

The number of independent trials until a good pivot is geometric with mean at most $2$. Charging every attempt at most $cm$, the expected cost of one shrink phase is at most $2cm$. After each completed phase, the active-size bound multiplies by $3/4$, so

$$
\mathbb E[T(n)]
\le
2cn\sum_{t\ge0}(3/4)^t
=8cn
=O(n).
$$

This does not by itself justify a deterministic latency guarantee; a nonuniform or modulo-biased sampler; dependent/reused choices; an adaptive adversary that observes pivots; a stateful/inconsistent comparator; unbounded key/callback cost; or a changed duplicate/partition policy. Finite constants, memory movement, and cancellation latency also require measurement.

### Answer 4

Create at most $\lceil n/5\rceil$ groups and recursively select pivot $p$ from their medians, costing $T(\lceil n/5\rceil)$. Among full groups whose medians are at least $p$, three records per group are at least $p$; the symmetric statement holds below. Discarding conservative allowances for the pivot group, an incomplete group, and rounding leaves at least $3n/10-6$ protected records on each side.

After linear partition work, the only continuing side therefore has size at most $7n/10+6$, giving

$$
T(n)\le T(\lceil n/5\rceil)+T(7n/10+6)+cn.
$$

For $n\ge140$,

$$
\lceil n/5\rceil+(7n/10+6)
\le .9n+7
\le .95n.
$$

Assume inductively $T(m)\le am$ for smaller $m$ outside a fixed base range. Then

$$
T(n)\le .95an+cn\le an
$$

when $a\ge20c$. Enlarge $a$ to cover all base cases. Hence $T(n)=O(n)$.

The theorem bounds asymptotic worst-case comparisons/work. It does not remove group sorting, median movement, recursion, cache effects, record width, or higher finite constants. Randomized or sampled quickselect can be faster on ordinary workloads while lacking this standalone deterministic ceiling.

### Answer 5

Define p99 first: specify zero-based rank mapping, such as a named nearest-rank or interpolation convention, for every $n$, including $n=0$. If the result must be one input record, avoid arithmetic interpolation. Define whether any equal-key identity is acceptable; otherwise add original position or a durable sequence as a tie key.

Materialize immutable keys before in-place mutation when memory permits, bounding callback calls and isolating callback failure. Define a total floating order for NaNs, infinities, and signed zero, or reject them before mutation. Validate rank and all keys under resource limits.

Use half-open three-way partition so repeated values form one finished interval. Start with an unbiased hidden random or reviewed sample pivot, iterate on only the target side, and track active sizes plus accumulated comparison/key work. When progress/work budget is crossed, switch to groups-of-five deterministic selection under the same range, rank, comparator, identity, and error contracts. Do not expose expected behavior as the latency ceiling.

If mutation is allowed, state that success leaves a partial partition and failure/cancellation leaves a valid owner for every record but unspecified order. For rollback, select on a private index array and publish only after success. Place bounded cancellation checks inside partition scans and between iterations.

Limit record count, retained/key bytes, callback calls/time/allocations, comparisons, swaps/bytes, total wall/CPU time, and concurrency. Randomness documentation must cover generator, unbiased range sampling, seed lifetime, adversary visibility, replay access, and policy version.

Test rank endpoints, the exact p99 mapping around small sizes, singleton, all equal, low-cardinality, sorted, reverse, organ-pipe, repeated extremes, exceptional floats, duplicate identities, slow/failing/stateful callbacks, biased/repeated seeds, budget boundary, deterministic fallback, cancellation at each region, and maximum size. Differential-check values against a trusted total-order sort and assert permutation and side predicates.

Record active sizes, pivot ranks, equal widths, comparisons, callback time/calls, swaps/bytes, iterations, fallback reason/count, seed identifier under access control, cancellation latency, failure state, peak memory, and end-to-end tail latency. Compare introselect, pure median of medians, stable full sort, histogram/radix when keys permit, and approximate quantile sketches only if the product contract is changed to allow error.
