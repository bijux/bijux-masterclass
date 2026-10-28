---
module_id: ALGE-012
program: Algorithm Engineering
level: 1
module_number: 12
title: Insertion, Selection, and Shell Sorting
status: complete
last_verified: 2026-09-04
---

# Insertion, Selection, and Shell Sorting

## One-Page Review

### Governing question

How do three in-place comparison sorts organize the same array by exploiting different invariants, and when do adaptivity, stability, data movement, gap choice, or small-input constants make an elementary method the right engineering component?

### Essential definitions

- A sequence is **sorted** when its keys are nondecreasing under a declared ordering.
- A sort is **stable** when records equivalent under the sort key retain their original relative order.
- An **inversion** is a pair of positions $i<j$ whose keys satisfy $k(A[i])>k(A[j])$.
- **Insertion sort** grows a sorted prefix by shifting larger prefix elements and inserting the next record into its boundary.
- **Selection sort** grows a sorted prefix by selecting a minimum from the unsorted suffix and placing it at the boundary.
- A sequence is **$h$-sorted** when every subsequence of positions with one residue modulo $h$ is sorted.
- **Shellsort** performs insertion sorts at decreasing positive gaps, ending with gap $1$.
- A sort is **adaptive** when its work decreases for a quantifiable kind of existing order.
- An **in-place** array sort uses only constant auxiliary record storage, apart from representation and call-stack qualifications.

### Central model, mechanism, or theorem

For keys $k(A[i])$, define the inversion count

$$
I(A)=
\left|
\left\{
(i,j):0\le i<j<n,\ k(A[i])>k(A[j])
\right\}
\right|.
$$

A shift-based stable insertion sort performs exactly $I(A)$ right shifts of existing records: each shift removes one inversion involving the inserted record, and the final array has none. Consequently,

$$
0\le I(A)\le\binom n2=\frac{n(n-1)}2.
$$

Selection sort instead performs exactly

$$
\sum_{i=0}^{n-2}(n-i-1)=\frac{n(n-1)}2
$$

key comparisons in its conventional form, regardless of initial order, but needs at most $n-1$ swaps. Shellsort moves records farther during early $h$-sorts; its cost is inseparable from the chosen gap sequence.

### Critical invariants

- The comparator/key relation must be consistent and unchanged throughout the sort.
- In insertion sort, $A[0:i)$ is a stable sorted permutation of the original prefix before inserting $A[i]$.
- Shift only strictly greater keys to preserve the relative order of equals.
- In selection sort, the prefix contains the $i$ smallest remaining records in sorted order, and the suffix contains every unplaced record.
- Selection cannot stop scanning a suffix merely because its current minimum looks small.
- After an $h$-sort pass, each residue-class subsequence is sorted.
- A Shellsort gap schedule must contain a final $1$; otherwise ordinary sortedness is not guaranteed.
- Comparisons, swaps, record moves, key projections, and array writes are different costs.
- In-place does not imply stable, adaptive, cache-optimal, or low-write.
- Validate permutation preservation as well as order.

### Common failures

Common failures include overwriting the insertion key before saving it; shifting on equality and losing stability; using binary search to reduce comparisons while claiming it also removes shifts; skipping the final Shellsort gap $1$; silently inventing a gap extension; describing Shellsort as having one universal complexity; swapping a selected minimum across equal records and claiming stability; stopping selection early on nearly sorted input; counting a record swap as one machine write without defining the model; accepting a nontransitive comparator; checking only sortedness while losing or duplicating records; and applying elementary sorts to large arbitrary inputs without a measured reason.

### Compact example

For keys $(3,1,2)$, the inversions are $(3,1)$ and $(3,2)$, so $I=2$. Insertion sort shifts $3$ right once when inserting $1$ and once when inserting $2$, for exactly two shifts. Selection sort makes three comparisons regardless of the input order, then uses at most two swaps. The same $\Theta(n^2)$ worst-case class hides different dependence on disorder and different write behavior.

### Connections

[ALGE-003](./003-loop-invariants-for-algorithm-correctness.md) supplies invariant proofs; [ALGE-005](./005-asymptotic-time-and-space.md) supplies cost models; [ALGE-010](./010-combining-proof-and-measurement-in-algorithm-evaluation.md) supplies comparison discipline; [ALGE-011](./011-linear-and-binary-search.md) supplies insertion boundaries. [ALGE-013](../ROADMAP.md) introduces merge sort, while [ALGE-019](../ROADMAP.md) returns to adaptive and hybrid production sorting.

## Governing Question

Insertion, selection, and Shell sorting are sometimes dismissed as preliminary algorithms to memorize before “real” $O(n\log n)$ sorts. That misses their enduring value. They expose three distinct ways to make irreversible progress, three different cost profiles, and several components used inside sophisticated sort implementations.

Insertion sort pays for disorder and can be nearly linear on nearly sorted inputs. Selection sort pays a fixed quadratic comparison bill but writes few times. Shellsort tries to remove long-distance disorder before a final insertion pass, gaining practical speed at the price of gap-dependent analysis and stability. None is simply “better.” The decision depends on the contract, input structure, record size, comparator cost, memory behavior, and lifecycle.

The governing question is therefore not which name wins a Big-O table. It is which invariant produces the needed order, stability, permutation, movement, and finite performance guarantees under the actual cost model.

## Why This Matters

Elementary sorts appear in production as:

- base cases inside divide-and-conquer and hybrid sorts;
- small fixed-size sorting kernels;
- online insertion into already ordered buffers;
- nearly sorted cleanup passes;
- low-write rearrangement when comparisons are cheap;
- bounded-memory code on embedded or constrained systems;
- pedagogical and diagnostic reference implementations.

They also teach durable distinctions. A stable output is stronger than a sorted output. A low comparison count does not imply few data moves. An in-place algorithm can still write large records repeatedly. Adaptivity must name a disorder measure rather than rely on an impression that data is “almost sorted.” Shellsort demonstrates that an algorithm family may have no meaningful complexity claim until its parameter schedule is fixed.

These distinctions prepare the rest of the sorting block. Merge sort trades extra space for stable $O(n\log n)$ behavior. Quicksort trades worst-case risk against strong locality. Heapsort controls auxiliary space and worst-case comparison growth. Non-comparison sorts change the key model. Understanding the elementary methods makes those later trade-offs concrete.

## Prerequisites and Retrieval

Retrieve:

- arrays, records, key projections, permutations, and equivalence under a comparator;
- loop invariants, induction, termination variants, and frame conditions;
- arithmetic and geometric sums;
- best-, worst-, expected-, and input-sensitive analysis;
- comparison, swap, move, write, allocation, and cache cost models;
- lower and upper insertion boundaries;
- stability, indirect sorting, and mutation/ownership semantics.

You should be able to distinguish moving a record from comparing its key, prove that a sorted permutation is a correct sorting result, and explain why $n(n-1)/2$ is the number of unordered index pairs in an $n$-element sequence.

## Learning Objectives

After completing this module, you should be able to:

1. state sortedness, permutation, stability, and in-place contracts precisely;
2. derive insertion sort from a sorted-prefix invariant;
3. prove that insertion shifts equal the initial inversion count;
4. derive selection sort from a minimum-prefix invariant;
5. compute exact conventional selection comparison and swap bounds;
6. explain when selection sort's low write count matters;
7. define $h$-sortedness and derive Shellsort from gapped insertion passes;
8. reject gap-independent Shellsort complexity claims;
9. diagnose comparator, stability, movement, endpoint, and permutation defects;
10. select and validate an elementary sort or base-case kernel for an unfamiliar workload.

## Core Exposition

### Define the full sorting contract

Let the input be records $A[0:n]$ and let $k$ map records to comparison keys. A correct ascending sort must establish:

**Order**

$$
\forall i\in\{0,\ldots,n-2\},\quad
k(A[i])\le k(A[i+1]).
$$

**Permutation**

The output contains exactly the input records with the same multiplicities. For records with identities, checking only key counts is insufficient.

**Stability**, when required

If original positions $i<j$ have equivalent keys, their records appear in that same relative order in the output.

The contract may also constrain mutation, auxiliary storage, exceptions, determinism, comparator calls, and record movement. “Sort the values” does not say whether rearranging equal-key events, database rows, or messages is permitted.

The ordering relation must be suitable for sorting. At minimum, the algorithm needs comparisons that are consistent during execution and induce transitive ordered equivalence classes. Partial values such as floating NaN require a declared total-order policy when ordinary comparisons do not provide one. A key function that observes mutable external state can invalidate every proof below.

### Derive insertion sort from a sorted prefix

At outer-loop index $i$, maintain:

1. $A[0:i)$ is sorted;
2. $A[0:i)$ is a stable permutation of the original records from positions $0$ through $i-1$;
3. $A[i:n)$ contains the not-yet-inserted original suffix records.

Initially $i=1$ and a one-element prefix is sorted and stable. Save the record $key=A[i]$ before modifying its slot. Scan the prefix right-to-left. While the predecessor has a strictly greater key, copy it one slot right. When scanning stops, place the saved record in the hole.

Why does this preserve order? Every shifted record is greater than the saved key, so it belongs after the insertion position. Either the insertion position is zero or its predecessor is at most the saved key. The untouched earlier prefix remains ordered, and the untouched suffix has not lost a record because the key was saved.

Why is it stable? An existing record with a key equivalent to the saved record is not shifted, because the comparison is strictly greater rather than greater-or-equal. The newly inserted record therefore follows all equivalent records that appeared earlier in the input.

The outer index increases to $n$. At termination the sorted prefix is the whole array, while the permutation and stability clauses have been preserved.

### Prove shifts equal inversions

Consider inserting the record originally at position $i$. Each time a larger predecessor moves right across that record, one initial inversion involving the record is removed. No non-inversion is crossed, because scanning stops at the first key that is not greater. Each original inversion is encountered exactly once: when its later record is inserted into the prefix containing its earlier, larger partner.

Therefore

$$
\text{right shifts}=I(A).
$$

This gives an input-sensitive bound:

$$
T_{\mathrm{insert}}(A)\in\Theta(n+I(A))
$$

under a unit-cost model for loop overhead, comparisons, and record moves. The $\Theta(n)$ term accounts for visiting the $n-1$ outer positions and placing keys even when $I=0$.

For an already sorted nonempty input, $I=0$, there are $n-1$ failed greater-than comparisons, and no right shifts. For strictly reverse order,

$$
I=\binom n2=\frac{n(n-1)}2,
$$

so shifts and successful comparisons are quadratic. For a uniformly random permutation of distinct keys, every index pair is inverted with probability $1/2$, hence

$$
\mathbb E[I]=\frac12\binom n2=\frac{n(n-1)}4.
$$

That expectation depends on the uniform-permutation model; duplicate-heavy or structured workloads need their own distribution.

### Count comparisons without confusing them with shifts

The number of key comparisons in insertion sort is close to, but not always equal to, the number of inversions. Each successful comparison produces a shift. For each outer iteration that stops because it finds a predecessor at most the key, there is one additional failed key comparison. An iteration that reaches index zero has no such final key comparison.

Thus a standard shift implementation satisfies

$$
I(A)\le C(A)\le I(A)+n-1.
$$

The exact placement within this range depends on how often insertion reaches the left boundary. This matters when comparisons are expensive but moves are cheap. Binary insertion can find the stable insertion boundary in $O(\log i)$ comparisons for prefix length $i$, reducing total comparisons to $O(n\log n)$, yet it still shifts $I(A)$ records. It changes one resource bound, not the whole algorithm into an $O(n\log n)$ mover.

Swapping adjacent records instead of shifting a block also performs one inversion-removing exchange per crossing, but an exchange typically writes both array slots and moves the saved record repeatedly. The hole-and-shift implementation usually has a better movement constant.

### Derive selection sort from a minimum suffix

At outer index $i$, conventional selection sort maintains:

1. $A[0:i)$ is sorted;
2. those $i$ positions contain the $i$ smallest records selected so far;
3. $A[i:n)$ contains exactly the remaining records.

Scan the entire suffix $A[i:n)$ to find an index $m$ holding a minimum key. Swap $A[i]$ with $A[m]$ if $m\ne i$. Now position $i$ contains a minimum of all remaining records, so it is at least the preceding prefix value and cannot need revision. Increment $i$.

The suffix scan must inspect every remaining candidate unless the key domain supplies a proven absolute minimum and the contract permits a corresponding early stop. Merely finding a small-looking value is not evidence that no smaller value occurs later.

At $i=n-1$, the final remaining record is necessarily in its correct position. The invariant then proves sortedness and permutation.

### Count selection comparisons and writes

At outer positions $i=0,\ldots,n-2$, selection scans $n-i-1$ later records. Therefore

$$
C(n)
=
\sum_{i=0}^{n-2}(n-i-1)
=
\sum_{r=1}^{n-1}r
=
\frac{n(n-1)}2.
$$

This count is identical for sorted, reverse, random, and nearly sorted inputs in the conventional algorithm. Selection sort is not adaptive to inversion count.

There is at most one swap for each of $n-1$ outer iterations. If self-swaps are skipped:

$$
0\le \text{swaps}\le n-1.
$$

Under an array-slot-write model, each ordinary swap writes two slots, so it uses at most $2(n-1)$ array writes, plus local temporary storage. Under a byte-movement or persistent-memory model, record width and write amplification must be included explicitly.

This profile can be rational when comparisons inspect cheap labels but moving records is exceptionally expensive. It is not rational to summarize that decision as “both are quadratic.”

### Understand why conventional selection is unstable

Consider identified records

$$
((2,a),(2,b),(1,c)).
$$

The first suffix minimum is $(1,c)$. Swapping it with position zero yields

$$
((1,c),(2,b),(2,a)).
$$

The two key-$2$ records have reversed relative order, even though the algorithm never directly swaps equal keys. A long-distance swap moved $(2,a)$ past $(2,b)$.

A stable selection variant can remove the selected minimum and shift the intervening block right, but then the low-write advantage changes. Stability is an algorithm-and-movement-policy property, not something inferred from the selection idea alone.

### Define $h$-sortedness

For a positive integer gap $h$, $A$ is $h$-sorted when, for every residue $r\in\{0,\ldots,h-1\}$, the subsequence

$$
A[r],A[r+h],A[r+2h],\ldots
$$

is sorted wherever those indices are below $n$. An $h$-sort is simply insertion sort applied to all these interleaved subsequences, conveniently implemented in one gapped loop.

With a large gap, a record can travel a long array distance in one shift. This attacks inversions that ordinary insertion sort would remove through many adjacent shifts. Later, smaller gaps refine the order. A final gap $h=1$ makes the one residue-class subsequence equal to the whole array; after that pass, the array is ordinarily sorted.

The proof of final correctness is deliberately modest:

1. each gapped insertion pass terminates and establishes its stated $h$-sorted postcondition;
2. the schedule contains $1$;
3. the final $1$-sort establishes ordinary sortedness and preserves permutation.

No claim that every later pass preserves every earlier gap property is needed.

### Treat the gap sequence as part of the algorithm

“Shellsort” names a family. The schedule may be based on repeated halving, $3h+1$, powers/products, an empirically selected finite table, or another construction. Gap count, ratios, common factors, order, and extension beyond a published table all affect behavior.

A valid schedule for length $n$ must:

- contain positive integers smaller than $n$ when used;
- avoid duplicate or increasing passes in the execution order unless justified;
- end with $1$;
- be generated without overflow or an infinite loop;
- declare how a finite published sequence is extended to larger $n$.

Shell's original halving schedule is simple but has quadratic worst cases. Other schedules have different proven bounds, and empirically strong schedules do not automatically carry an optimal universal theorem. State the exact sequence and the exact sourced or derived claim.

The schedule also affects finite mechanisms: comparisons, shifts, locality, branch behavior, and the disorder presented to the final pass. Measure gap sequences on identical input instances, retain per-shape results, and avoid tuning on the same workload used for the final claim.

### Explain stability and movement in Shellsort

Gapped movement can carry one record past an equal-key record in another residue class. Therefore ordinary Shellsort is generally unstable even when each gapped insertion shifts only on strict greater-than comparisons. The instability arises across subsequences and passes, not necessarily inside one residue class.

Shellsort is normally in-place in the auxiliary-array sense: it keeps a saved record and a few indices. That does not mean it minimizes writes or has constant physical cost. It can move records many times across multiple passes. If records are large, sort an array of references/indices or separate keys from payloads, subject to ownership and locality trade-offs developed later in ALGE-018.

### Compare the three mechanisms

| Property | Insertion | Selection | Shell |
|---|---|---|---|
| Progress object | sorted prefix via insertion | fixed minimum prefix | decreasing-gap partial orders |
| Conventional worst comparisons | $\Theta(n^2)$ | exactly $n(n-1)/2$ | gap-dependent |
| Adaptive to inversions | yes, $\Theta(n+I)$ model | no | often input-sensitive, schedule-dependent |
| Conventional stability | yes with strict shifting | no | generally no |
| Auxiliary record storage | $O(1)$ | $O(1)$ | $O(1)$ |
| Data movement | exactly $I$ right shifts plus placements | at most $n-1$ swaps | gap/input-dependent |
| Natural use | small or nearly sorted ranges | expensive writes, simple reference | medium in-place ranges under a validated schedule |

This table describes conventional implementations under declared models. It does not predict a universal timing winner.

### Preserve executable mechanism evidence

The following deterministic run compares one shift-based insertion implementation, conventional selection, and Shellsort with the explicit gaps $(3,1)$.

<!-- bijux-verify: {"id":"elementary-sort-ledger","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"insertion sorted=(1, 2, 2, 4, 5) comparisons=10 shifts=8\nselection sorted=(1, 2, 2, 4, 5) comparisons=10 swaps=2\nshell gaps=(3, 1) sorted=(1, 2, 2, 4, 5) comparisons=8 shifts=5\n","stderr":""}} -->
~~~python
def insertion_sort(values, gap=1):
    items = list(values)
    comparisons = 0
    shifts = 0
    for index in range(gap, len(items)):
        saved = items[index]
        cursor = index
        while cursor >= gap:
            comparisons += 1
            if items[cursor - gap] <= saved:
                break
            items[cursor] = items[cursor - gap]
            shifts += 1
            cursor -= gap
        items[cursor] = saved
    return tuple(items), comparisons, shifts


def selection_sort(values):
    items = list(values)
    comparisons = 0
    swaps = 0
    for left in range(len(items) - 1):
        minimum = left
        for candidate in range(left + 1, len(items)):
            comparisons += 1
            if items[candidate] < items[minimum]:
                minimum = candidate
        if minimum != left:
            items[left], items[minimum] = items[minimum], items[left]
            swaps += 1
    return tuple(items), comparisons, swaps


def shell_sort(values, gaps):
    items = tuple(values)
    comparisons = 0
    shifts = 0
    for gap in gaps:
        items, pass_comparisons, pass_shifts = insertion_sort(items, gap)
        comparisons += pass_comparisons
        shifts += pass_shifts
    return items, comparisons, shifts


values = (5, 2, 4, 2, 1)
ordered, comparisons, shifts = insertion_sort(values)
print(f"insertion sorted={ordered} comparisons={comparisons} shifts={shifts}")
ordered, comparisons, swaps = selection_sort(values)
print(f"selection sorted={ordered} comparisons={comparisons} swaps={swaps}")
gaps = (3, 1)
ordered, comparisons, shifts = shell_sort(values, gaps)
print(
    f"shell gaps={gaps} sorted={ordered} "
    f"comparisons={comparisons} shifts={shifts}"
)
~~~

The figures are exact for this implementation and input only. They establish neither an average distribution nor a general timing ranking. A serious comparison also validates stability with identified equal-key records, permutation preservation, exceptional comparators, and representative sizes/shapes.

### Engineer the small-range decision

When selecting a base-case sort inside a larger algorithm, specify:

- the cutoff range and how it was chosen;
- whether subarrays arrive nearly sorted;
- record/key width and projection cost;
- required stability;
- comparison, movement, branch, and cache metrics;
- whether a sentinel or unguarded prefix premise is valid;
- whether the outer algorithm can defer small-range insertion until later;
- compiler, architecture, and workload scope.

Then compare complete implementations rather than isolated textbook loops. A lower cutoff can increase recursion/partition overhead; a higher cutoff can expose quadratic work. Tune on a training workload and confirm on held-out shapes so the cutoff is not merely fitted to one benchmark.

## Definitions and Notation

- $A[0:n]$ is an array of $n$ records; $k(A[i])$ is the key used for order.
- $A^{(0)}$ denotes the original input when a proof must relate output identities to input identities.
- $I(A)$ is the number of strict key inversions in $A$.
- $C(A)$ is a declared key-comparison count, not automatically elapsed time.
- A **right shift** copies a record from position $j-1$ to $j$ while a saved record occupies temporary storage.
- A **swap** exchanges two array positions; its move/write cost depends on record representation.
- A **sorted prefix** is an interval $A[0:i)$ already ordered under the comparator.
- A **minimum of a suffix** is any record whose key is no greater than every key in that suffix.
- $h$ is a positive Shellsort gap; indices in one $h$-chain have the same residue modulo $h$.
- A **gap schedule** is the exact ordered sequence of gaps executed by Shellsort.
- A sort is **comparison-based** when it learns key order only through comparisons.
- A **movement model** specifies whether the resource is assignments, array-slot writes, bytes copied, persistent writes, or another mechanism.

For duplicate keys, inversion count uses strict $>$ rather than $\ge$. Equal pairs are not out of order. This choice aligns the inversion measure with stable insertion sort's rule that equal predecessors do not move past the newly inserted record.

## Mechanisms, Invariants, or Proof Structure

Use this elementary-sort review:

1. **Records and identities:** define what must be preserved, including duplicate identity.
2. **Key and relation:** declare projection, order, equivalence, exceptional values, and mutability.
3. **Postconditions:** require order and permutation; add stability when the contract needs it.
4. **Cost resources:** separate comparisons, projections, shifts, swaps, writes, bytes, and allocation.
5. **Input structure:** measure size, inversions, runs, duplicate frequency, and displacement where relevant.
6. **Insertion invariant:** prove the prefix is a stable sorted permutation before and after insertion.
7. **Insertion progress:** show the inner cursor and outer boundary move toward termination.
8. **Selection invariant:** prove the fixed prefix consists of successive suffix minima.
9. **Selection certification:** account for every suffix candidate comparison.
10. **Gap invariant:** prove one pass $h$-sorts all residue classes.
11. **Schedule validity:** verify positivity, order, bounds, overflow safety, and final gap $1$.
12. **Movement semantics:** decide shift, adjacent exchange, long swap, reference movement, or block operation.
13. **Boundary cases:** cover $n=0$, $n=1$, all equal, sorted, reverse, duplicates, and invalid comparators.
14. **Executable evidence:** assert order, multiset/identity preservation, and stability separately.
15. **Finite evaluation:** compare representative inputs and modeled counters before wall time.
16. **Use boundary:** document why an elementary method or cutoff is selected and what would reverse it.

The shared sorting proof has two layers:

**Local mechanism.** Show that one insertion, selection, or $h$-sort step establishes its next invariant without losing a record.

**Global termination.** Show that the processed prefix grows or that a finite gap schedule reaches its final $1$-sort. Then derive order and permutation at the whole-array boundary.

Stability needs its own argument. Neither sortedness nor permutation implies it. Write the proof in terms of identified records with equivalent keys, and trace every movement that could cross them.

## Alternatives and Trade-Offs

**Insertion versus selection.** Insertion adapts to inversions and is conventionally stable, but may shift quadratic many records. Selection always performs quadratic comparisons but at most linear many swaps. Choose according to disorder, stability, and movement cost.

**Insertion versus Shellsort.** Insertion is easier to prove and performs well when displacement is already small. Shellsort can move distant records early and improve medium unsorted arrays, but gives up stability and requires a declared, validated gap schedule.

**Shifts versus adjacent swaps.** Shifts save the current record once and copy each larger predecessor once. Adjacent swaps repeatedly move both records. Swaps may fit an existing primitive, but their cost should not be hidden.

**Linear versus binary insertion position.** Linear backward search ties comparisons to inversions and has excellent local simplicity. Binary search bounds comparisons by $O(\log i)$ per insertion but does not reduce the required block shift in an array.

**Direct versus indirect movement.** Direct sorting keeps contiguous records but can copy large payloads repeatedly. Sorting indices or references reduces bytes moved while adding indirection, storage, and locality considerations.

**Stable selection versus low-write selection.** Shifting the interval after selecting a minimum can preserve equal-record order. It also turns one swap into potentially linear movements, surrendering selection's distinctive write profile.

**Fixed versus tuned gaps.** A cited fixed schedule is reproducible and analyzable within its stated domain. Workload-specific tuning can improve finite results but needs held-out validation, extension rules, and protection against overfitting.

**Textbook method versus library sort.** These algorithms are valuable components and reference implementations. A general application should normally use a well-specified library sort unless a measured constraint justifies owning comparator, stability, exception, and optimization risks.

## Failure Modes and Misconceptions

1. **“Sorted output proves a correct sort.”** Records may have been lost, duplicated, or replaced; permutation is separate.
2. **“Equal keys are interchangeable.”** Their identities and original order matter under a stable contract.
3. **“Use greater-or-equal in insertion.”** That moves earlier equal records behind later ones and breaks stability.
4. **“Write the insertion key after shifting begins.”** The first shift may overwrite the only copy.
5. **“Insertion always makes exactly $I$ comparisons.”** It makes exactly $I$ right shifts; failed stopping comparisons add cost.
6. **“Binary insertion makes the whole algorithm $O(n\log n)$.”** Array movements remain quadratic in the worst case.
7. **“Selection gets faster on sorted input.”** Conventional selection still scans every remaining suffix.
8. **“One swap means one write.”** A swap updates two array locations and moves data through temporary storage.
9. **“Selection is stable because it never swaps equal keys.”** A long swap can carry one equal record across another.
10. **“In-place means low movement.”** It constrains auxiliary storage, not total bytes written.
11. **“Shellsort is insertion sort, so it is stable.”** Cross-chain long movements can reverse equal records.
12. **“Any decreasing gaps work equally well.”** Correctness may survive, but finite and asymptotic costs can change radically.
13. **“A final gap near one is enough.”** Ordinary sortedness requires a $1$-sort.
14. **“Shellsort is $O(n^{3/2})$.”** Such a bound belongs to specified schedules, not the family name.
15. **“An empirical gap table extends itself.”** Values beyond the published domain require an explicit rule and new evidence.
16. **“Comparator exceptions cannot affect permutation.”** Partial mutation before failure may be observable unless the API guarantees otherwise.
17. **“NaN will settle into some harmless location.”** Without a total-order policy, the postcondition is undefined or false.
18. **“Wall time identifies why one sort wins.”** Counters and movement evidence are needed to connect a mechanism.
19. **“A cutoff measured on random integers generalizes.”** Record width, disorder, duplicates, keys, compiler, and hardware can move it.
20. **“Elementary means obsolete.”** Small-range and constrained-resource roles remain valid when explicitly justified.

## Worked Examples

### Example 1

**Question:** Trace insertion sort on $(4,1,3)$ and relate shifts to inversions.

**Reasoning:** The original inversions are $(4,1)$ and $(4,3)$, so $I=2$. Insert $1$: save it, shift $4$ right, and place $1$, giving $(1,4,3)$. Insert $3$: shift $4$ right and place $3$, giving $(1,3,4)$. Exactly two right shifts occurred.

**Conclusion:** Each shift removed one distinct inversion, and the shift total equals the original inversion count.

### Example 2

**Question:** What work does insertion sort perform on $(1,2,3,4,5)$?

**Reasoning:** Every new key compares once with its immediate predecessor and stops. There are $n-1=4$ key comparisons, zero right shifts, and four final placements in this implementation. The sorted-prefix invariant advances normally; there is no need for a special presorted detector.

**Conclusion:** Insertion sort is linear on already sorted input under the stated operation model.

### Example 3

**Question:** Why does strict shifting make insertion stable on $((2,a),(1,c),(2,b))$?

**Reasoning:** Inserting $(1,c)$ shifts $(2,a)$. Later, when inserting $(2,b)$, its predecessor $(2,a)$ is equal rather than greater, so scanning stops after $(2,a)$. The output is $((1,c),(2,a),(2,b))$.

**Conclusion:** The original order $a$ before $b$ is preserved because equal predecessors never cross the inserted record.

### Example 4

**Question:** How many key comparisons and swaps can selection sort use for $n=8$?

**Reasoning:** Comparisons are

$$
7+6+5+4+3+2+1=28.
$$

This count is input-independent. There are seven outer placements, so at most seven non-self swaps; a sorted input uses none if self-swaps are omitted.

**Conclusion:** Selection gives exactly $28$ comparisons and between $0$ and $7$ swaps under this implementation.

### Example 5

**Question:** Demonstrate selection sort instability without swapping equal keys directly.

**Reasoning:** On $((2,a),(2,b),(1,c))$, selecting $(1,c)$ and swapping positions $0$ and $2$ produces $((1,c),(2,b),(2,a))$. Records $a$ and $b$ had equal keys, but their order reversed because $a$ crossed $b$ during a swap with $c$.

**Conclusion:** Avoiding equal-key swaps is insufficient; conventional long-swap selection is unstable.

### Example 6

**Question:** Is $(1,4,2,5,3,6)$ sorted? Is it $2$-sorted?

**Reasoning:** It is not ordinarily sorted because $4>2$ at adjacent positions. Residue-zero positions contain $(1,2,3)$ and residue-one positions contain $(4,5,6)$; both subsequences are sorted.

**Conclusion:** The array is $2$-sorted but not $1$-sorted, showing why a Shellsort schedule must end at gap $1$.

### Example 7

**Question:** A Shellsort implementation executes gaps $(4,2)$ on eight records and stops. What can it claim?

**Reasoning:** If each pass is correct, the last pass establishes $2$-sortedness. The even and odd index chains may each be sorted while adjacent cross-chain pairs remain inverted, exactly as in Example 6. No $1$-sort establishes global order.

**Conclusion:** The implementation is incomplete as a general sort even if many test inputs happen to finish ordered.

### Example 8

**Question:** Does binary insertion remove quadratic movement on reverse input?

**Reasoning:** Binary search can locate each insertion boundary with logarithmic comparisons. But inserting the second record shifts one prefix record, the third shifts two, and so on. Total shifts remain

$$
1+2+\cdots+(n-1)=\frac{n(n-1)}2.
$$

**Conclusion:** Binary insertion improves the comparison resource, not the array-movement lower bound of this method.

### Example 9

**Question:** Comparisons cost one unit and a record swap costs 10,000 units. Which elementary profile deserves evaluation?

**Reasoning:** At size $n$, selection spends $n(n-1)/2$ cheap comparisons but at most $n-1$ expensive swaps. Reverse-order insertion shifts $n(n-1)/2$ records. If identities can be moved by reference the model changes, but under direct expensive records, selection's low-swap bound can dominate.

**Conclusion:** Evaluate selection when writes/moves dominate; a comparison-only Big-O table hides the relevant resource.

### Example 10

**Question:** A hybrid sort uses insertion for partitions of length at most $24$, based on one random-integer benchmark. Is the cutoff justified?

**Reasoning:** The benchmark does not cover nearly sorted partitions, duplicate keys, large records, expensive projections, alternate compilers, or target processors. It may also tune and evaluate on the same samples. Instrument comparisons and bytes moved, test representative partition states, select the cutoff on training data, and validate it on held-out cases.

**Conclusion:** Keep the elementary base case, but bind its cutoff to a reproducible workload and reversal criterion rather than treating $24$ as universal.

## Cross-Program Connections

- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) owns array representations, dynamic ordered collections, iterators, and movement/storage invariants.
- [Programming Languages & Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) owns comparator laws, exception behavior, numeric ordering, generics, and mutation semantics.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) owns cache, branch, SIMD, and write-path mechanisms beneath finite sorting performance.
- [Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) owns byte movement, aliasing, object layout, allocation, and low-level safety.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) owns collation, external records, persistent writes, and index/order requirements.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns property, differential, metamorphic, and performance-test design for sort implementations.

## References

1. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. [*Introduction to Algorithms*, fourth edition](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), MIT Press, 2022. Sorting contracts, insertion-sort correctness, inversions, and comparison analysis.
2. Donald E. Knuth. [*The Art of Computer Programming, Volume 3: Sorting and Searching*, second edition](https://www.informit.com/store/art-of-computer-programming-volume-3-sorting-and-searching-9780321635785), Addison-Wesley Professional, 1998. Foundational classification and analysis of internal sorting methods.
3. Robert Sedgewick and Kevin Wayne. [“Elementary Sorts”](https://algs4.cs.princeton.edu/21elementary/), companion to *Algorithms*, fourth edition, checked 2026-09-04. Selection, insertion, inversion sensitivity, $h$-sortedness, Shellsort, and executable cost models.
4. Donald L. Shell. [“A High-Speed Sorting Procedure”](https://doi.org/10.1145/368370.368387), *Communications of the ACM* 2(7), 1959, pp. 30–32. Primary introduction of the diminishing-increment method.
5. Marcin Ciura. “Best Increments for the Average Case of Shellsort.” In [*Fundamentals of Computation Theory, FCT 2001*](https://link.springer.com/book/10.1007/3-540-44669-9), LNCS 2138, Springer, 2001, pp. 106–117. Primary empirical work on finite Shellsort increment sequences and their stated domain.
6. Jon Bentley. [*Programming Pearls*, second edition](https://www.informit.com/store/programming-pearls-9780201657883), Addison-Wesley Professional, 2000. Precise problem statements, invariants, implementation, testing, and cost reasoning.
7. ACM, IEEE Computer Society, and AAAI. [*Computer Science Curricula 2023: Algorithmic Foundations*](https://csed.acm.org/al-cs-core/), endorsed 2024; consulted 2026-09-04. Current curricular scope for elementary sorting, implementation, correctness, empirical analysis, and trade-offs.

## Exercises

### Exercise 1

For each conventional implementation, state whether it is stable, adaptive to inversions, in-place under the auxiliary-array model, and guaranteed to use $O(n^2)$ comparisons: (a) strict-shift insertion sort, (b) long-swap selection sort, and (c) Shellsort with one exact schedule ending in $1$. Qualify every answer that depends on the schedule or cost model.

### Exercise 2

For a uniformly random permutation of $n$ distinct keys, derive $\mathbb E[I(A)]$. Then use the shift/inversion correspondence to derive the expected right-shift count of insertion sort. Explain why the result does not apply unchanged to an arbitrary duplicate-heavy distribution.

### Exercise 3

Trace stable insertion sort and conventional selection sort on identified records

$$
((4,a),(3,b),(4,c),(1,d)).
$$

Give the final identity order, insertion right-shift count, selection comparison count, and selection swap trace. State which stability observation is and is not exercised by this particular selection trace.

### Exercise 4

For $A=(8,1,6,3,5,2,7,4)$, execute Shellsort gaps $(4,2,1)$ using stable-within-chain gapped insertion. Show the array after each complete pass. Verify the appropriate $h$-sorted property after each pass and give the final sorted array. Does this execution prove Shellsort stable on all inputs?

### Exercise 5

An embedded recorder periodically sorts at most 48 fixed-width event records. Flash-backed writes are expensive, RAM permits one saved record but no auxiliary array, timestamps can tie, batches are usually nearly sorted after clock correction, and a corrupted comparator configuration is possible. Design the contract, choose among insertion, selection, Shellsort, or a bounded combination, and specify proofs, failure handling, tests, counters, and measurements needed before deployment.

## Answers to the Exercises

### Answer 1

Strict-shift insertion is stable because it does not move an earlier equal key behind a later one. It is adaptive under the $\Theta(n+I)$ comparison/movement model, uses $O(1)$ auxiliary record storage, and has $O(n^2)$ worst-case comparisons.

Long-swap selection is generally unstable, is not adaptive to inversion count in its conventional full-suffix scan, and uses $O(1)$ auxiliary record storage. It makes exactly $n(n-1)/2=O(n^2)$ key comparisons but at most $n-1$ swaps.

Conventional in-place Shellsort uses $O(1)$ auxiliary record storage and is generally unstable. It is often input-sensitive in finite work, but “adaptive” needs a stated measure and schedule. Its comparison guarantee is gap-dependent: some schedules have quadratic worst cases and some have stronger sourced upper bounds. The family name alone does not justify one universal tight bound. Ending in $1$ guarantees final order, not a particular cost.

### Answer 2

For each unordered pair of distinct keys, define indicator $X_{ij}=1$ when their positions form an inversion and zero otherwise. Under a uniform random permutation, either relative order is equally likely, so

$$
\Pr(X_{ij}=1)=\frac12.
$$

There are $\binom n2$ pairs. By linearity of expectation,

$$
\mathbb E[I]
=
\mathbb E\left[\sum_{i<j}X_{ij}\right]
=
\sum_{i<j}\mathbb E[X_{ij}]
=
\binom n2\frac12
=
\frac{n(n-1)}4.
$$

Stable shift-based insertion performs one right shift for each strict inversion, so its expected shift count is also $n(n-1)/4$ in this model. Duplicate keys change pair probabilities: equal pairs are never strict inversions, and an arbitrary data distribution need not make either strict order equally likely. Its expected inversion count must be derived from that distribution.

### Answer 3

The original strict inversions are $(4a,3b)$, $(4a,1d)$, $(3b,1d)$, and $(4c,1d)$, for $I=4$. Stable insertion proceeds:

$$
(4a,3b,4c,1d)
\to
(3b,4a,4c,1d)
\to
(3b,4a,4c,1d)
\to
(1d,3b,4a,4c).
$$

It makes four right shifts. The two key-$4$ records finish in original order $a$ before $c$.

Selection on four records makes

$$
3+2+1=6
$$

comparisons. It first selects $(1,d)$ and swaps it with $(4,a)$:

$$
(4a,3b,4c,1d)\to(1d,3b,4c,4a).
$$

At position one, $(3,b)$ is already the suffix minimum, so no swap occurs. At position two, the implementation retains the first minimum $(4,c)$ and makes no swap. Final identity order is $(1d,3b,4c,4a)$.

This trace demonstrates actual instability: $4a$ originally preceded $4c$ but finishes after it. If a selection implementation had happened to preserve equals on this one input, that observation still would not prove stability; stability is universal over admitted inputs.

### Answer 4

Start with

$$
(8,1,6,3,5,2,7,4).
$$

For gap $4$, sort chains at residues $0,1,2,3$:

- $(8,5)\to(5,8)$,
- $(1,2)$ stays,
- $(6,7)$ stays,
- $(3,4)$ stays.

The array becomes

$$
(5,1,6,3,8,2,7,4),
$$

which is $4$-sorted.

For gap $2$, the even-index chain $(5,6,8,7)$ becomes $(5,6,7,8)$ and the odd-index chain $(1,3,2,4)$ becomes $(1,2,3,4)$. Interleaving them gives

$$
(5,1,6,2,7,3,8,4),
$$

which is $2$-sorted.

For gap $1$, ordinary insertion sorting yields

$$
(1,2,3,4,5,6,7,8).
$$

This execution proves the pass properties for this input and gives one sorted result. It does not prove stability for all inputs; ordinary Shellsort is generally unstable because records in different residue chains can cross.

### Answer 5

Require a nondecreasing timestamp order, exact preservation of every identified event, and stable original order among tied timestamps unless a documented sequence identifier supplies a stronger tie-break. Require one immutable comparator configuration for the entire batch and define rejection rather than partial output when it is invalid.

Because $n\le48$ and batches are usually nearly sorted, strict-shift insertion is the leading candidate: it is stable, uses one saved record, and movement follows inversion count. Selection is a useful alternative if measured flash-write cost dominates and stability can be preserved through an explicit composite key or a stable high-movement variant; ordinary long-swap selection cannot satisfy stability. Shellsort may reduce disorder on worse batches but is generally unstable, so it would need indirect identities or a total composite key and a fixed validated schedule ending in $1$. A bounded combination could use one or more gapped passes only if its semantics and write benefit survive those constraints, followed by strict insertion.

Prove order, identity permutation, stability/tie-break behavior, index bounds, and termination. Validate comparator reflexivity/antisymmetry/transitivity on the bounded batch or use a trusted fixed comparator; stage output or retain recovery metadata if failure cannot expose a partially rearranged persistent batch.

Exhaustively test sizes $0$ through $48$ where feasible over structured generators: sorted, reverse, one displaced event, all equal timestamps, duplicate runs, extremes, corrupted configuration, and power-loss/failure boundaries. Differentially compare with a trusted stable reference and assert identities, not only timestamps.

Count key comparisons, shifts, swaps, array-slot writes, and bytes written. Measure end-to-end batch latency, energy if relevant, flash-write amplification/endurance impact, and failure recovery on representative hardware. Use the observed inversion and duplicate distributions, preserve raw results, and choose the simplest candidate meeting the stable contract and predeclared latency/write thresholds.
