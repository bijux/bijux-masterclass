---
module_id: ALGE-013
program: Algorithm Engineering
level: 1
module_number: 13
title: Merge Sort
status: complete
last_verified: 2026-09-04
---

# Merge Sort

## One-Page Review

### Governing question

How can two independently sorted ranges be combined into one stable sorted permutation, and how does that linear merge support a predictable $O(n\log n)$ sort without hiding buffer, movement, recursion, or lifecycle costs?

### Essential definitions

- **Merge** consumes two sorted input ranges and emits their sorted multiset union.
- **Merge sort** divides a range, recursively sorts both halves, and merges them.
- A merge is **stable** when it chooses the left record first on equivalent keys, assuming the left run originally precedes the right run.
- A **run** is a contiguous range already ordered under the sort relation.
- **Top-down merge sort** recursively divides before merging; **bottom-up merge sort** iteratively merges runs of increasing width.
- An **auxiliary buffer** temporarily holds records or references so unread input is not overwritten.
- A **merge frontier** is the pair of current unconsumed heads of the left and right runs.
- A **ping-pong implementation** alternates source and destination buffers across levels to avoid copying merged data back after every merge.

### Central model, mechanism, or theorem

To merge sorted runs of lengths $p$ and $q$, compare their current heads. Emit the smaller, choosing the left head on equality. Maintain:

1. the output prefix is sorted and stable;
2. it contains exactly the consumed input records;
3. every emitted key is no greater than either remaining head.

At least one input head advances per emission. Once one run is exhausted, copy the other suffix. A merge performs at most $p+q-1$ key comparisons and $\Theta(p+q)$ record/reference movement.

Balanced merge sort satisfies

$$
T(n)
=
T(\lfloor n/2\rfloor)
+T(\lceil n/2\rceil)
+\Theta(n)
=
\Theta(n\log n).
$$

For the conventional balanced algorithm with a worst-case $p+q-1$ merge, the exact maximum key comparisons is

$$
W(n)
=
n\left\lceil\log_2 n\right\rceil
-2^{\left\lceil\log_2 n\right\rceil}
+1
\quad(n\ge1).
$$

### Critical invariants

- Both input runs must be sorted under the same stable comparison contract.
- The output cursor equals the number of records consumed from both runs.
- Never overwrite an unread input record unless a proved in-place merge handles that aliasing.
- Choose the left run on key equivalence to preserve cross-run stability.
- Exhaustion checks precede input reads; conceptual sentinels are not automatically representable values.
- Split intervals and merge intervals must use one endpoint convention.
- The recursive postcondition is sorted, permutation-preserving, and stable—not merely “looks ordered.”
- One reusable $O(n)$ buffer differs from allocating fresh subarrays at every recursive call.
- $O(n\log n)$ comparisons do not imply $O(1)$ auxiliary space or minimal writes.
- External, linked, parallel, and natural merging have distinct cost models and ownership.

### Common failures

Common failures include merging unsorted halves; choosing right on equality and silently losing stability; copying only keys and losing record identities; writing output over unread input; reading after one run is exhausted; using a sentinel key that can also occur in data; dropping the odd tail in bottom-up passes; overflowing midpoint or run-width arithmetic; allocating new arrays recursively while claiming one linear buffer; adding two independently sorted results without proving comparator consistency; claiming in-place because recursion uses no explicit list; ignoring exception/partial-mutation behavior; and timing an already allocated buffer against a competitor that pays allocation.

### Compact example

Merge left run $((1,a),(2,b),(2,c))$ with right run $((2,d),(4,e))$. Emit $(1,a)$, then compare equal key-$2$ heads and take $(2,b)$ from the left, then $(2,c)$ from the left, then $(2,d)$ and $(4,e)$. The result is sorted, contains every record once, and preserves $b,c,d$ order across the run boundary.

### Connections

[ALGE-004](./004-inductive-correctness-proofs.md) supplies recursive proof structure; [ALGE-007](./007-recurrences-and-the-master-method.md) solves the recurrence; [ALGE-012](./012-insertion-selection-and-shell-sorting.md) supplies sorting contracts and stability. [ALGE-014](../ROADMAP.md) contrasts partition-based quicksort, while [ALGE-018](../ROADMAP.md) deepens stable and indirect sorting.

## Governing Question

Dividing an array is easy. The essential work of merge sort lies in its composition law: if two adjacent ranges satisfy the complete sorting postcondition, can one linear procedure combine them while preserving order, identity multiplicity, and equal-key history?

Once that merge is correct, recursive sorting follows cleanly. Yet an engineering-quality account must go beyond the recurrence. It must say where records move, how stability is obtained, which buffer is owned, what happens for non-powers of two, whether the implementation is top-down or bottom-up, how comparator failures surface, and which representation makes merging attractive.

Merge sort is therefore both a canonical divide-and-conquer algorithm and a case study in turning a mathematical recurrence into a real memory/data-movement design.

## Why This Matters

Merge-based ordering supports:

- predictable worst-case comparison growth;
- stable sorting of records with duplicate keys;
- sequential access patterns;
- natural operation on linked sequences and streams;
- external sorting when inputs exceed memory;
- parallel decomposition and merge;
- adaptive hybrids that discover existing runs.

Those applications share the merge abstraction but not one implementation. An array sort may use a reusable auxiliary buffer. A linked-list merge can relink nodes. An external merge pays block transfers and may combine many runs. A parallel merge partitions output work. This module owns the foundational two-way array mechanism and its proof; later modules develop the specialized regimes.

The algorithm also makes resource honesty unavoidable. Merge sort gives a strong worst-case time guarantee, but the conventional stable array version needs linear auxiliary storage and moves records at every merge level. When memory, payload width, write amplification, or allocation latency dominates, that trade can outweigh the comparison guarantee.

## Prerequisites and Retrieval

Retrieve:

- half-open ranges, arrays, iterators, records, keys, and permutations;
- stable sorting and identified duplicate records;
- recursive induction and loop invariants;
- floors, ceilings, logarithms, and recurrences;
- comparison-decision lower bounds;
- stack depth, heap allocation, aliasing, and buffer reuse;
- sequential versus random memory access and block transfer;
- benchmark lifecycle and resource-specific counters.

You should be able to prove a loop from an invariant and variant, solve $T(n)=2T(n/2)+\Theta(n)$ for powers of two, and distinguish auxiliary-space peak from cumulative allocation or total bytes moved.

## Learning Objectives

After completing this module, you should be able to:

1. state the sorted-run merge contract including permutation and stability;
2. derive a two-way merge from frontier and output-prefix invariants;
3. prove merge termination and its $p+q-1$ comparison upper bound;
4. prove top-down merge sort by strong induction;
5. solve its balanced recurrence for arbitrary $n$;
6. compute exact worst-case comparisons for conventional balanced merge sort;
7. translate the recursive algorithm into bottom-up run-width passes;
8. account for buffer peak, recursion stack, allocation, copies, and record width;
9. diagnose stability, aliasing, endpoint, tail, comparator, and failure defects;
10. select and validate a merge-based design for an unfamiliar workload.

## Core Exposition

### Establish the complete merge contract

Let adjacent half-open runs be

$$
L=A[lo:mid),
\qquad
R=A[mid:hi).
$$

Assume both are sorted under the same key relation. A correct stable merge writes $B[lo:hi)$ such that:

**Order**

$$
\forall t\in[lo,hi-1),\quad k(B[t])\le k(B[t+1]).
$$

**Permutation**

$B[lo:hi)$ contains exactly the identified records from $L$ and $R$, with the same multiplicities.

**Stability**

The relative order of equivalent records within each run is preserved, and equivalent records from $L$ precede equivalent records from $R$ because the left run represents the earlier original range.

**Frame**

Locations outside the declared destination are unchanged unless the interface explicitly owns them.

The stability premise about run origin matters. If two runs were formed by a prior transformation that already reordered equals, choosing left on equality preserves that transformed order, not magically the original one.

### Derive the two-way merge loop

Copy or otherwise expose both input runs without allowing destination writes to destroy unread records. Use indices $i$ and $j$ for the next left and right records and $o$ for the next destination slot.

At every loop head maintain:

1. $lo\le i\le mid$ and $mid\le j\le hi$;
2. $o-lo=(i-lo)+(j-mid)$;
3. $B[lo:o)$ is a sorted stable merge of $A[lo:i)$ and $A[mid:j)$;
4. if records remain, the last emitted key is no greater than either current head.

If both runs remain, compare $k(A[i])$ and $k(A[j])$. Emit $A[i]$ when its key is less than or equivalent to the right key; otherwise emit $A[j]$. Increment the chosen input cursor and $o$.

The count of unconsumed records,

$$
V=(mid-i)+(hi-j),
$$

is a nonnegative integer that decreases by one for every emission. When one run is exhausted, append the other suffix. Its order is already known, and the frontier invariant shows it can follow the output prefix.

At termination $V=0$ and $o=hi$. The invariant yields order, permutation, and stability for the whole destination.

### Prove the comparison bounds for one merge

Let the run lengths be $p$ and $q$. Every head comparison emits one record. Once either run is empty, no more key comparisons are needed; the other suffix is copied.

In the worst case, neither run becomes empty until $p+q-1$ records have been emitted. Then:

$$
C_{\max}(p,q)=p+q-1
\quad(p,q>0).
$$

This is attainable when keys interleave so that the last unconsumed record is not exposed until all other records have been selected.

In the best case, every key of the shorter-to-exhaust run comes before the other run's current head, so:

$$
C_{\min}(p,q)=\min(p,q)
\quad(p,q>0).
$$

Regardless of comparisons, producing a conventional materialized array merge touches or writes $\Theta(p+q)$ records/references. Comparison adaptivity does not erase output movement.

### Preserve stability at the equality branch

Assume left and right runs are individually stable relative to original order. When their head keys are equal, their original positions place the left head before the right head because the left range preceded the right range. Emitting left first therefore respects the global stable order.

If the merge uses

$$
k(L[i])<k(R[j])
$$

for its left branch and chooses right otherwise, equality selects the right record first and reverses cross-run equals. The output remains sorted and permutation-preserving but is not stable.

Stability tests must attach identities to equal-key records and arrange them across a split. Testing only integer values cannot reveal this defect.

### Prove merge sort by strong induction

Define merge sort on $A[lo:hi)$:

1. if $hi-lo<2$, return;
2. choose $mid=lo+\lfloor(hi-lo)/2\rfloor$;
3. recursively sort $A[lo:mid)$;
4. recursively sort $A[mid:hi)$;
5. stably merge the two sorted ranges.

**Base cases.** Empty and one-record ranges are already sorted, are permutations of themselves, and are stable.

**Inductive step.** Assume every smaller range is returned as a stable sorted permutation. Both halves have sizes smaller than $n=hi-lo$ when $n\ge2$. The induction hypothesis establishes the merge preconditions. The reviewed merge procedure combines them into a stable sorted permutation of their union, exactly the original range.

Thus the postcondition holds for every finite range. Termination follows because both recursive subproblem sizes are strictly smaller and reach zero or one.

### Solve the recurrence without assuming powers of two

For $n\ge2$, balanced splitting yields sizes $\lfloor n/2\rfloor$ and $\lceil n/2\rceil$. With linear merge and bookkeeping cost:

$$
T(n)
=
T(\lfloor n/2\rfloor)
+T(\lceil n/2\rceil)
+\Theta(n).
$$

The recursion tree has height $\lceil\log_2 n\rceil$. At every full level, subproblem sizes sum to $n$, so that level contributes $O(n)$. There are $O(\log n)$ levels, giving $O(n\log n)$. A comparison-sort lower bound supplies $\Omega(n\log n)$ worst-case comparisons for distinct arbitrary keys, while the algorithm itself has linear work at each necessary merge level. Hence conventional balanced merge sort is $\Theta(n\log n)$ in worst-case time under the model.

Floors and ceilings affect exact counts but not this asymptotic result. Never silently discard them in an endpoint proof.

### Derive exact worst-case comparisons

Let $W(0)=W(1)=0$. A worst-case merge of the balanced halves uses $n-1$ comparisons, so

$$
W(n)
=
W(\lfloor n/2\rfloor)
+W(\lceil n/2\rceil)
+n-1.
$$

The closed form is

$$
W(n)
=
\sum_{i=1}^{n}\left\lceil\log_2 i\right\rceil
=
n\left\lceil\log_2 n\right\rceil
-2^{\left\lceil\log_2 n\right\rceil}
+1
\quad(n\ge1).
$$

For $n=8$:

$$
W(8)=8\cdot3-8+1=17.
$$

For $n=10$:

$$
W(10)=10\cdot4-16+1=25.
$$

This is an implementation-specific exact maximum: balanced binary splitting, conventional two-way merge, and one key comparison per head decision. It is not the minimum possible comparisons among every sorting algorithm.

### Account for auxiliary memory honestly

A conventional stable array merge cannot generally write back into the same overlapping range with the simple frontier loop; output may overwrite unread input. Common designs include:

- one reusable auxiliary array of $n$ records or references;
- copying only one run into a buffer and merging with careful direction;
- alternating source and destination arrays between recursion levels;
- allocating fresh slices/results at recursive calls;
- specialized in-place stable merge algorithms with more complex movement/cost.

With one reusable full buffer, peak auxiliary array space is $\Theta(n)$ and recursive control depth is $\Theta(\log n)$. If the buffer holds references rather than payload records, byte space is proportional to reference width, but payload accesses remain indirect.

Fresh allocation at every call may still have bounded simultaneous live memory under a particular ownership schedule, but cumulative allocation and allocator traffic can be $\Theta(n\log n)$. State what is allocated, when it is live, and whether timing includes acquisition/initialization.

Calling a recursive implementation “in-place except for the merge arrays” is misleading: the merge arrays are the dominant auxiliary resource.

### Translate to bottom-up merging

Bottom-up merge sort begins with runs of width $1$ and repeatedly merges adjacent runs of width $w$:

$$
w=1,2,4,8,\ldots
$$

For each left boundary $lo$, compute

$$
mid=\min(lo+w,n),
\qquad
hi=\min(lo+2w,n).
$$

Merge only when $mid<hi$. The minimum operations preserve a short final run when $n$ is not a power of two. After the pass of width $w$, every processed block of at most $2w$ is sorted. Doubling continues until $w\ge n$.

Bottom-up form removes recursive stack frames and makes pass order explicit. Top-down form exposes divide-and-conquer proof structure and can localize subranges naturally. With equivalent merge schedules, both retain the same asymptotic comparison and buffer bounds.

In fixed-width arithmetic, compute/double widths defensively. An overflowing $2w$ can wrap, repeat a pass, or produce invalid endpoints.

### Use ordered-boundary shortcuts carefully

After recursively sorting adjacent halves, if

$$
k(A[mid-1])\le k(A[mid]),
$$

their concatenation is already sorted and stable, so the merge movement can be skipped. This adds a boundary comparison but can reduce copying on ordered inputs.

In a top-down implementation that still visits the whole recursion tree, already sorted input can take $\Theta(n)$ boundary checks instead of materializing $\Theta(n\log n)$ merge movement. This does not make the worst case better, and the exact result depends on cutoff and comparison accounting.

Do not use the shortcut before both halves are known sorted. One boundary pair cannot certify arbitrary unsorted interiors.

Natural merge algorithms go further by detecting existing runs rather than recursively manufacturing them. Their run-stack policies and adaptivity belong to ALGE-019.

### Separate array, linked, and external mechanisms

For arrays, merging is sequential but normally needs auxiliary storage. For linked lists, a stable merge can relink nodes and use small auxiliary state, provided ownership and iterator validity are managed. Random access is unnecessary.

For data larger than memory, sorted runs can be written and merged through buffered sequential I/O. The relevant resource becomes block transfers, fan-in, memory buffers, temporary storage, and recovery, not merely comparison count. That is external sorting in ALGE-086.

The abstraction is shared—consume minimum frontiers from sorted runs—but a complexity claim must name representation and cost model.

### Preserve executable evidence

This implementation uses indices and one reusable auxiliary array. It chooses the left record on equality and counts only key comparisons between two live run heads.

<!-- bijux-verify: {"id":"stable-merge-ledger","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"input=((2, 'a'), (1, 'x'), (2, 'b'), (1, 'y'))\nsorted=((1, 'x'), (1, 'y'), (2, 'a'), (2, 'b'))\ncomparisons=5 stable_equal_order=('x', 'y', 'a', 'b')\n","stderr":""}} -->
~~~python
def stable_merge_sort(records):
    items = list(records)
    auxiliary = [None] * len(items)
    comparisons = 0

    def sort_range(lo, hi):
        nonlocal comparisons
        if hi - lo < 2:
            return
        mid = lo + (hi - lo) // 2
        sort_range(lo, mid)
        sort_range(mid, hi)

        auxiliary[lo:hi] = items[lo:hi]
        left = lo
        right = mid
        for output in range(lo, hi):
            if left == mid:
                items[output] = auxiliary[right]
                right += 1
            elif right == hi:
                items[output] = auxiliary[left]
                left += 1
            else:
                comparisons += 1
                if auxiliary[left][0] <= auxiliary[right][0]:
                    items[output] = auxiliary[left]
                    left += 1
                else:
                    items[output] = auxiliary[right]
                    right += 1

    sort_range(0, len(items))
    return tuple(items), comparisons


records = ((2, "a"), (1, "x"), (2, "b"), (1, "y"))
ordered, comparisons = stable_merge_sort(records)
print(f"input={records}")
print(f"sorted={ordered}")
print(
    f"comparisons={comparisons} "
    f"stable_equal_order={tuple(label for _, label in ordered)}"
)
~~~

The label sequence makes equal-key order visible: $x$ remains before $y$, and $a$ remains before $b$. The five comparisons also attain $W(4)=4\cdot2-4+1=5$ for this split schedule.

### Engineer failures and exceptions

A comparator or key projection can fail after recursive halves have already been rearranged. An in-place API may then expose a partially permuted range. Decide whether the language/library contract permits this, whether a copy-on-success strategy is required, and whether every original record remains recoverable.

Other hazards include:

- allocation failure for the auxiliary buffer;
- aliasing between source, auxiliary, and destination ranges;
- integer overflow in endpoints or bottom-up widths;
- cancellation during a long merge;
- mutation of keys while runs are being merged;
- inconsistent normalization between run production and merge;
- data corruption or duplicate/lost blocks in external variants.

Strong exception safety is not free. Sorting a private copy and committing atomically uses more memory. Journaling or restartable runs add I/O. State the failure postcondition rather than assuming success-only reasoning covers production.

### Evaluate the right resources

Useful analytical and empirical quantities include:

- key comparisons by merge level and input shape;
- key projection calls and whether keys are cached;
- records/references copied into and out of the buffer;
- bytes moved and peak live auxiliary bytes;
- allocation count and cumulative allocated bytes;
- recursion depth or bottom-up pass count;
- ordered-boundary skips;
- cache misses, memory bandwidth, and page transfers;
- elapsed time by size, record width, disorder, duplicates, and run structure.

Validate correctness before timing. Use identified duplicates, preserve failures, and compare the same stability contract. A stable merge sort should not be benchmarked against an unstable competitor without making that semantic difference part of the decision.

## Definitions and Notation

- $A[lo:hi)$ is the input/output range with length $n=hi-lo$.
- $mid$ divides the range into $A[lo:mid)$ and $A[mid:hi)$.
- $p=mid-lo$ and $q=hi-mid$ are the two run lengths.
- $i$ and $j$ are the next unconsumed positions in the left and right runs.
- $o$ is the next output position.
- $V=(mid-i)+(hi-j)$ is the merge termination variant.
- $T(n)$ is a cost recurrence whose resource must be named.
- $W(n)$ is the exact worst-case number of head key comparisons for the declared balanced implementation.
- A **stable permutation** preserves both multiplicity/identity and original relative order within every key-equivalence class.
- A **run boundary** separates adjacent sorted ranges.
- A **short tail** is the final bottom-up range whose length may be less than the current run width.
- **Peak auxiliary space** is maximum simultaneously live extra storage; **cumulative allocation** sums allocations over execution.

When $\log_2 n$ appears for $n=0$, handle the empty base case separately. The exact comparison formula is stated only for $n\ge1$.

## Mechanisms, Invariants, or Proof Structure

Use this merge-sort worksheet:

1. **Contract:** declare order, identity permutation, stability, mutation, and failure behavior.
2. **Relation:** define key projection, equivalence, exceptional values, and consistency duration.
3. **Ranges:** choose one endpoint convention and prove every split lies within it.
4. **Merge precondition:** prove both runs are sorted and refer to the intended snapshot.
5. **Frontiers:** identify the next unconsumed record of each run.
6. **Output invariant:** relate the output prefix exactly to consumed input prefixes.
7. **Tie rule:** choose left on equivalence when stable original-run order is required.
8. **Progress:** decrease the number of unconsumed records on every emission.
9. **Exhaustion:** guard before reading and append the known-sorted remaining suffix.
10. **Recursive proof:** apply the postcondition of smaller ranges as the merge precondition.
11. **Recurrence:** bind the merge resource and split sizes before solving.
12. **Buffer ownership:** define allocation, aliasing, initialization, reuse, and peak bytes.
13. **Iteration translation:** handle short tails and width arithmetic in bottom-up form.
14. **Optimization premises:** prove boundary skips, cutoffs, and buffer alternation preserve semantics.
15. **Validation:** assert order, identities, stability, boundaries, failures, and exact small counts.
16. **Evaluation:** measure comparisons, movement, memory, and time under one fair lifecycle.

The core composition theorem is:

> If the left and right ranges are each stable sorted permutations of their corresponding original subranges, and stable merge returns a stable sorted permutation of their concatenation, then merge sort returns a stable sorted permutation of the original range.

The induction proof depends on all three nouns—stable, sorted, permutation. Omitting one produces a weaker and often insufficient API.

## Alternatives and Trade-Offs

**Top-down versus bottom-up.** Top-down code mirrors recursive proof and naturally targets subranges. Bottom-up code removes recursion and exposes sequential passes, but must handle odd tails and width overflow.

**Full buffer versus half buffer.** A full reusable buffer simplifies symmetric merging. Copying one side can reduce peak storage but makes merge direction, overlap, and stability more delicate.

**Copy-back versus ping-pong buffers.** Copy-back keeps ownership simple but moves data twice per level. Alternating source/destination can remove a copy while complicating parity, base cases, and final-location guarantees.

**Always merge versus boundary skip.** Always merging gives uniform behavior and simple counts. A checked boundary can avoid work on ordered adjacent runs, at the price of one comparison and an extra correctness premise.

**Merge sort versus insertion sort.** Merge sort controls worst-case growth for large arbitrary ranges but allocates/moves more. Insertion sort is simpler and faster on sufficiently small or nearly sorted subranges; hybrids need measured cutoffs.

**Merge sort versus quicksort.** Merge sort is stable by a simple tie rule and has predictable worst-case comparisons, but conventional arrays need linear auxiliary space. Quicksort is typically in-place and locality-friendly but needs pivot/partition protection against bad cases.

**Array versus linked representation.** Arrays support compact traversal but need a merge destination. Linked structures can relink nodes with low auxiliary record space, while pointer chasing and ownership costs change physical performance.

**Binary versus multiway merge.** Two-way merge is foundational. Multiway merge can reduce external passes or combine many runs, but requires a frontier-selection structure and a different transfer/memory analysis.

**Direct versus indirect merge.** Moving references reduces payload bytes and supports stable identity order. It adds auxiliary references, indirection, and potentially scattered payload access.

## Failure Modes and Misconceptions

1. **“Recursion sorts the array.”** Correctness comes from the merge composition law and base cases.
2. **“Two sorted halves imply a sorted whole.”** Their boundary may be inverted; they must be merged or proved already ordered.
3. **“Choose either side on equality.”** Right-first choice breaks stability across the split.
4. **“Sorted values imply stable records.”** Equal-key identities must be inspected.
5. **“Copying keys is enough.”** Payload identities and multiplicities are part of the permutation.
6. **“Use the maximum key as a sentinel.”** Real data may contain it, and custom comparators may not treat it as maximal.
7. **“The output can safely overwrite the input.”** Unread records may be destroyed without an overlap proof.
8. **“Merge always uses $p+q$ comparisons.”** The maximum is $p+q-1$ for nonempty runs; exhaustion ends comparisons.
9. **“Merge sort always makes exactly $n\log n$ comparisons.”** Counts depend on $n$, input interleaving, and implementation.
10. **“The recurrence is $2T(n/2)+n$ for every integer $n$.”** Arbitrary sizes require floors, ceilings, and exact merge terms.
11. **“$O(n\log n)$ time means $O(\log n)$ space.”** Conventional stable array merging needs $\Theta(n)$ auxiliary storage.
12. **“Fresh arrays per recursion are the same as one buffer.”** Peak, cumulative allocation, initialization, and allocator traffic differ.
13. **“Bottom-up widths always pair evenly.”** Non-power-of-two lengths leave short tails.
14. **“Doubling width cannot fail.”** Fixed-width overflow can prevent termination or corrupt endpoints.
15. **“A boundary comparison can skip sorting.”** It can skip only the merge after both interiors are already sorted.
16. **“Linked-list merge sort has array locality.”** Its access and allocation mechanisms differ.
17. **“Sequential access makes memory free.”** Bandwidth and record movement may dominate.
18. **“A comparator exception leaves the original unchanged.”** Only a documented failure guarantee can promise that.
19. **“Stable library sort means it uses this merge implementation.”** Semantics do not identify internal algorithm choice.
20. **“One random timing validates a buffer optimization.”** Correctness, memory, shapes, records, and machines all need scoped evidence.

## Worked Examples

### Example 1

**Question:** Merge $L=(1,4,7)$ and $R=(2,3,9)$.

**Reasoning:** Compare heads: emit $1$ from $L$; emit $2$ then $3$ from $R$; emit $4$ and $7$ from $L$; $L$ is exhausted, so append $9$. The five comparisons equal $p+q-1=5$.

**Conclusion:** The merged result is $(1,2,3,4,7,9)$ with the worst-case comparison count for two length-three runs.

### Example 2

**Question:** What is the best comparison count when merging $L=(1,2,3)$ and $R=(7,8,9,10)$?

**Reasoning:** Compare $1,2,3$ in turn with right head $7$. All three left records are emitted, then the four-record right suffix is copied without key comparisons. The shorter run length is $3$.

**Conclusion:** The merge uses $\min(3,4)=3$ comparisons but still writes all seven output records.

### Example 3

**Question:** How does a one-character tie-rule defect break stability?

**Reasoning:** Merge left $((2,a))$ and right $((2,b))$. A test that chooses left only for strict less-than selects $(2,b)$ on equality, producing $((2,b),(2,a))$. Order by key and permutation still pass.

**Conclusion:** Stable merge must choose the earlier/left record on equality, and tests need record identities.

### Example 4

**Question:** Split a seven-record range without losing an element.

**Reasoning:** For $[lo,hi)=[0,7)$, choose $mid=0+\lfloor7/2\rfloor=3$. The halves are $[0,3)$ of length $3$ and $[3,7)$ of length $4$. They are disjoint and their lengths sum to $7$.

**Conclusion:** Half-open balanced splitting handles odd sizes through floor/ceiling halves without a special leftover element.

### Example 5

**Question:** Compute the exact worst-case comparisons for $n=10$.

**Reasoning:** $\lceil\log_2 10\rceil=4$, so

$$
W(10)=10(4)-2^4+1=25.
$$

Equivalently the recurrence combines worst cases for sizes $5$ and $5$ plus nine final-merge comparisons.

**Conclusion:** Conventional balanced merge sort needs at most $25$ head key comparisons on ten records.

### Example 6

**Question:** Trace bottom-up run widths for $n=7$.

**Reasoning:** Width $1$ merges pairs $[0,1)+[1,2)$, $[2,3)+[3,4)$, and $[4,5)+[5,6)$; index $6$ is a one-record tail. Width $2$ merges $[0,2)+[2,4)$ and $[4,6)+[6,7)$. Width $4$ merges $[0,4)+[4,7)$.

**Conclusion:** Minimum-capped endpoints preserve every short tail until it joins a later merge.

### Example 7

**Question:** May a merge be skipped for halves $(1,4,3)$ and $(5,2,6)$ because $3\le5$ at the boundary?

**Reasoning:** No. Neither half is sorted, so the boundary pair does not characterize their interiors; $4>3$ and $5>2$ remain. The shortcut is valid only after recursive postconditions establish sorted halves.

**Conclusion:** Boundary order composes two already sorted runs; it does not certify arbitrary ranges.

### Example 8

**Question:** A payload is 4 KiB and its sortable reference is 8 bytes. Why consider indirect merge?

**Reasoning:** Moving every payload through $\Theta(\log n)$ merge levels can transfer orders of magnitude more bytes than moving references. Indirect order adds an $8n$-byte reference array plus payload indirection and may require a later materialization.

**Conclusion:** Compare byte movement and downstream access, not just record-count movement; indirect sorting can be decisive for wide records.

### Example 9

**Question:** Does using one $n$-record auxiliary buffer mean the algorithm allocates $n\log n$ live records?

**Reasoning:** No. The same buffer can serve non-overlapping recursive merges sequentially. Its peak array capacity is $n$ records, plus $O(\log n)$ control frames. It may be read/written at every level, so total movement is still $\Theta(n\log n)$.

**Conclusion:** Peak space and cumulative data movement are different resources.

### Example 10

**Question:** A merge comparator fails after 60% of a range has been written. What must the API say?

**Reasoning:** The original range may now contain a mix of merged output and unread/auxiliary state. Unless the implementation sorts a private copy or maintains rollback metadata, it cannot promise the original order remains unchanged. It should at least preserve record ownership according to a documented basic guarantee.

**Conclusion:** Define and test failure-state semantics; the success proof alone is insufficient for a production sorting API.

## Cross-Program Connections

- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) owns array/list representations, iterators, node relinking, buffers, and identity/permutation invariants.
- [Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) owns aliasing, allocation, byte copying, overflow, exception cleanup, and object lifetime.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) owns bandwidth, caches, prefetching, write paths, and NUMA mechanisms behind merge costs.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) owns virtual memory, mapped files, paging, scheduling, and I/O mediation.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) owns durable run production, data provenance, partitioning, and large pipeline sorting.
- [Concurrent & Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) owns task decomposition, synchronization, span, and parallel merge coordination.

## References

1. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. [*Introduction to Algorithms*, fourth edition](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), MIT Press, 2022. Divide-and-conquer merge sort, correctness, recurrences, and comparison analysis.
2. Donald E. Knuth. [*The Art of Computer Programming, Volume 3: Sorting and Searching*, second edition](https://www.informit.com/store/art-of-computer-programming-volume-3-sorting-and-searching-9780321635785), Addison-Wesley Professional, 1998. Foundational merging methods and sorting analysis.
3. Robert Sedgewick and Kevin Wayne. [“Mergesort”](https://algs4.cs.princeton.edu/22mergesort/), companion to *Algorithms*, fourth edition, checked 2026-09-04. Top-down/bottom-up implementations, auxiliary arrays, cutoffs, boundary checks, and role reversal.
4. Marek A. Suchenek. [“Elementary Yet Precise Worst-Case Analysis of MergeSort”](https://arxiv.org/abs/1702.08443), 2017. Primary derivations of the exact conventional worst-case comparison formula.
5. Jon Bentley. [*Programming Pearls*, second edition](https://www.informit.com/store/programming-pearls-9780201657883), Addison-Wesley Professional, 2000. Invariant-driven implementation, testing, and resource reasoning.
6. ACM, IEEE Computer Society, and AAAI. [*Computer Science Curricula 2023: Algorithmic Foundations*](https://csed.acm.org/al-cs-core/), endorsed 2024; consulted 2026-09-04. Current curricular scope for divide-and-conquer sorting, correctness, complexity, implementation, and empirical trade-offs.

## Exercises

### Exercise 1

Merge identified runs $L=((1,a),(3,b),(3,c),(8,d))$ and $R=((2,e),(3,f),(7,g))$ stably. Show each chosen identity, count head comparisons, and state which invariant facts justify appending the final suffix.

### Exercise 2

Prove the two-way stable merge loop using the consumed-prefix/output invariant and variant $V=(mid-i)+(hi-j)$. Cover initialization, preservation for strict and equal keys, exhaustion, termination, order, permutation, and stability.

### Exercise 3

For conventional balanced merge sort, compute $W(n)$ for $n=1,2,3,4,8,10,16$ using the exact formula. Verify $W(10)$ once with the recurrence. Explain why these numbers are not a universal lower bound for all comparison sorts at each $n$.

### Exercise 4

Design a bottom-up stable merge sort for $n=13$ using half-open ranges and one reusable auxiliary buffer. List run widths and all merge triples $(lo,mid,hi)$ for each pass. State overflow-safe loop conditions and the invariant after a pass.

### Exercise 5

A service must stably order up to 50 million identified events by timestamp. Payloads average 2 KiB, equal timestamps are common, input is often composed of sorted producer runs, memory is bounded, comparator normalization can fail, and results must survive restart. Design the merge contract, representation, run/merge strategy, buffer and failure ownership, proof obligations, tests, resource model, and evaluation needed to choose an implementation.

## Answers to the Exercises

### Answer 1

Compare $1a$ with $2e$ and emit $1a$. Compare $3b$ with $2e$ and emit $2e$. Compare equal keys $3b$ and $3f$ and emit the left record $3b$; compare $3c$ and $3f$ and emit left $3c$; compare $8d$ and $3f$ and emit $3f$; compare $8d$ and $7g$ and emit $7g$. The right run is exhausted, so append $8d$.

The result is

$$
((1,a),(2,e),(3,b),(3,c),(3,f),(7,g),(8,d)).
$$

There are six comparisons, the maximum $4+3-1$. At exhaustion, the output prefix is sorted and contains exactly all consumed records; the remaining left suffix is internally sorted; and its head $8d$ is no less than the last emitted record $7g$. Therefore appending it preserves order, permutation, and stability.

### Answer 2

Initially $i=lo$, $j=mid$, and $o=lo$. No records are consumed, so the empty output prefix is exactly their stable merge and is sorted. The cursor equation holds, and $V=p+q$.

When both runs remain, their heads are the least remaining records within their runs. If the left key is smaller, emitting left is globally minimal; if the right key is smaller, emitting right is globally minimal. On equality, emitting left is still ordered and preserves original cross-run order. Incrementing the matching cursor and $o$ preserves the cursor equation, identity multiplicity, and sorted output-prefix invariant. Exactly one record is consumed, so $V$ decreases by one.

If one run is exhausted, every remaining record is in the other sorted suffix. The frontier invariant says its head can follow the output prefix; internal sortedness orders the rest. Copying it preserves identities and within-run stability without further head comparisons.

Because $V$ starts finite, never becomes negative, and decreases on every emission, the process terminates with $V=0$ and $o=hi$. All input records have then been consumed exactly once. The invariant yields a sorted stable permutation of the two original runs.

### Answer 3

Using

$$
W(n)=n\lceil\log_2 n\rceil-2^{\lceil\log_2 n\rceil}+1,
$$

gives:

| $n$ | $W(n)$ |
|---:|---:|
| 1 | 0 |
| 2 | 1 |
| 3 | 3 |
| 4 | 5 |
| 8 | 17 |
| 10 | 25 |
| 16 | 49 |

For $n=10$, the two halves have size $5$. Since $W(5)=5(3)-8+1=8$,

$$
W(10)=W(5)+W(5)+9=8+8+9=25.
$$

These are maxima for one balanced merge-sort scheme. A decision-tree lower bound applies asymptotically (and exact decision-tree minima depend on $n$); other comparison sorts can use fewer comparisons at particular sizes or inputs. An algorithm's upper bound is not automatically a problem lower bound.

### Answer 4

For $n=13$, use widths $1,2,4,8$. At width $1$, merge:

$$
(0,1,2),(2,3,4),(4,5,6),(6,7,8),(8,9,10),(10,11,12).
$$

Index range $[12,13)$ is an unpaired sorted tail.

At width $2$, merge:

$$
(0,2,4),(4,6,8),(8,10,12).
$$

Again $[12,13)$ remains a tail. At width $4$, merge:

$$
(0,4,8),(8,12,13).
$$

At width $8$, merge:

$$
(0,8,13).
$$

For each candidate $lo$, compute $mid=\min(lo+w,n)$ and $hi=\min(lo+2w,n)$ and merge only when $mid<hi$. Avoid evaluating overflowing $2w$ by using checked/saturating arithmetic or conditions such as doubling only while $w<n$ and replacing $w$ with $n$ when $w>n/2$. Advance $lo$ with checked bounds rather than wrapped addition.

After a width-$w$ pass, every completed block $A[b:\min(b+2w,n))$ is a stable sorted permutation of its pre-pass records, including a short final block. That invariant supports the next doubled width.

### Answer 5

Require nondecreasing normalized timestamps, exact preservation of event identities, and original input order among equivalent timestamps. Define whether producer order constitutes original order and how runs are sequenced. A normalization failure must have a declared atomic/basic failure result; it cannot silently compare under mixed versions.

Avoid moving 2 KiB payloads through every merge level. Store stable references or compact $(key,sequence,id)$ descriptors and retain payloads in durable immutable segments. Detect or accept producer-supplied runs only after validating their order/version. Use bounded-memory multi-pass merging with explicit fan-in and sequential buffers; write each output run to a new durable object, checksum it, then atomically publish a manifest. Keep inputs until publication so restart can resume or safely repeat.

For every merge, prove sorted-run preconditions, stable left/run-priority tie behavior, identity permutation, frontier invariant, termination, bounded buffer use, and atomic manifest transition. Prove run discovery does not skip inversions and version all normalization/comparator metadata.

Tests cover empty/singleton inputs, short tails, all equal timestamps, equal keys across every run boundary, malformed/corrupt runs, normalization failure at every comparison region, allocation/I/O exhaustion, cancellation, crash before/after flush and publication, restart idempotence, and lost/duplicate identities. Differentially compare bounded cases with a trusted stable in-memory reference.

Model and measure key comparisons, normalization calls, descriptor and payload bytes moved, block transfers, fan-in, temporary peak storage, memory peak, merge passes, checksums, recovery time, and end-to-end latency. Use real run-length/duplicate distributions plus adversarial interleaving. Compare direct versus indirect representation and alternative fan-in under the same durability lifecycle before choosing.
