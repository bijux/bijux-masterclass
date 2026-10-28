---
module_id: ALGE-015
program: Algorithm Engineering
level: 1
module_number: 15
title: Heapsort
status: complete
last_verified: 2026-09-04
---

# Heapsort

## One-Page Review

### Governing question

How can a complete-tree order embedded in an array produce an in-place ascending sort with deterministic $O(n\log n)$ time, and which invariants, movement costs, comparator rules, and workload effects matter in a production implementation?

### Essential definitions

- A **binary max heap** is a complete binary tree in which every parent key is at least each child key.
- An **active heap** is the prefix still governed by heap order during sorting.
- A **sorted suffix** contains maxima already removed from the active heap and placed in final ascending positions.
- **Sift down** repairs a possible root violation when both child subtrees are already heaps.
- **Bottom-up heap construction** sifts internal nodes in reverse level order.
- **Sortdown** repeatedly exchanges the heap maximum with the final active position, shrinks the heap, and repairs the root.
- A **hole implementation** saves one record and promotes children into a vacant position instead of swapping at every level.
- **Binary heapsort** means the heap-based comparison sort, not every priority-queue workflow that happens to use a heap.

### Central model, mechanism, or theorem

For a zero-based active range $A[0:m)$,

$$
\operatorname{left}(i)=2i+1,\qquad
\operatorname{right}(i)=2i+2,\qquad
\operatorname{parent}(i)=\left\lfloor\frac{i-1}{2}\right\rfloor.
$$

A max heap satisfies

$$
A[\operatorname{parent}(i)]\ge A[i]
\quad\text{for every }1\le i<m.
$$

Bottom-up construction is linear because total possible descent over all starting nodes is bounded by the sum of their heights:

$$
\sum_v \operatorname{height}(v)
=
\sum_{h\ge1}N_{\ge h}
\le
\sum_{h\ge1}\left\lfloor\frac{n}{2^h}\right\rfloor
<n.
$$

Sortdown performs $n-1$ extractions, each followed by at most logarithmic repair. Thus classical binary heapsort uses $O(n\log n)$ comparisons in every execution, has $\Theta(n\log n)$ worst-case work, and can use $O(1)$ auxiliary array positions with iterative repair.

### Critical invariants

- Array indices represent one complete tree; heap size, not array capacity, decides which children exist.
- Before sifting a root, both child subtrees are heaps and only the saved/root record may violate order.
- Always compare both children that exist and descend through the larger child in a max heap.
- Bottom-up construction processes every internal root only after its child subtrees are heaps.
- During sortdown, the prefix is a max heap and the suffix is sorted ascending.
- Every active key is no greater than every key already in the suffix.
- The exchange at the boundary preserves identity permutation and fixes one maximum permanently.
- Shrink the active size before repair so the fixed suffix is never read or moved as heap storage.
- Heap order is partial order, not global sorted order.
- In-place space does not imply stability, adaptivity, locality, or failure atomicity.
- Comparator results and projected keys must remain consistent for the entire build and sortdown.

### Common failures

Common failures include mixing zero- and one-based child formulas; treating capacity as heap size; starting build at the wrong internal node; iterating internal roots upward; descending through the left child without checking the right; stopping after one exchange; repairing before shrinking; allowing sift down to touch the sorted suffix; assuming heap order means level-order sorting; counting bottom-up build as $n$ independent logarithmic operations; claiming repeated insertion is the same linear build; claiming $O(1)$ auxiliary positions makes the sort stable; ignoring large-record movement; and promising rollback after comparator failure even though the input was mutated in place.

### Compact example

For $(4,10,3,5,1)$, bottom-up repair starts at index $1$, then index $0$, and produces the max heap $(10,5,3,4,1)$. Exchanging $10$ with the final active record fixes $10$ in the suffix; repairing $(1,5,3,4)$ produces $(5,4,3,1)$. Repeating yields $(1,3,4,5,10)$. The heap prefix changes shape, but the sorted suffix only grows.

### Connections

[ALGE-006](./006-best-worst-expected-and-amortized-cost.md) supplies cost-claim discipline; [ALGE-008](./008-lower-bounds-and-adversary-arguments.md) explains why comparison sorting needs logarithmic-depth decisions; [ALGE-012](./012-insertion-selection-and-shell-sorting.md) defines sorting contracts; [ALGE-014](./014-quicksort-and-partitioning.md) motivates heapsort as a deterministic fallback; and ALGE-019 will engineer hybrid selection and tuning.

## Governing Question

How should heap construction, sift repair, and sortdown be specified and proved so an implementation provides ordered-permutation correctness, deterministic resource bounds, renderable mathematical evidence, and honest operational trade-offs?

The answer starts with two contracts, not with a memorized loop. A max heap exposes the greatest active key at its root while otherwise imposing only parent-child order. A sort must turn that partial order into a globally ordered permutation. Sift down establishes the local heap contract, bottom-up construction composes local repairs, and sortdown establishes one final array position per iteration.

## Why This Matters

Quicksort is often attractive because its scans have strong locality and small constants, but a poorly shaped partition sequence can consume quadratic work. Heapsort offers a different guarantee: the complete-tree shape fixes repair depth, so input order cannot create a taller heap. This makes heapsort useful as a standalone memory-bounded sort, a worst-case fallback in introspective sorting, and a case study in turning a structural invariant into a resource bound.

Its asymptotic headline is not the whole engineering result. Heap accesses jump between levels, equal records can move across one another, large records can make every exchange expensive, a callback can dominate comparison cost, and an in-place failure may expose a partially permuted array. Bottom-up construction is linear only because most nodes are near the leaves; saying “there are $n$ calls and each is logarithmic” loses the decisive aggregate argument.

The module therefore treats ordered output, identity preservation, heap shape, comparison count, movement, auxiliary storage, stability, failure semantics, and physical locality as separate properties.

## Prerequisites and Retrieval

Retrieve:

- sorting order, identity permutation, stability, keys, and comparator laws;
- complete binary trees, levels, depths, heights, parents, and children;
- zero-based half-open arrays and overflow-aware index arithmetic;
- loop invariants, variants, induction, and aggregate summation;
- logarithms, geometric series, and worst-case upper bounds;
- swap cost, record width, indirect sorting, and cache locality;
- exception safety, cancellation, ownership, and operation instrumentation.

You should be able to distinguish a tree's logical shape from its pointer representation, prove that a loop variant decreases, and explain why $O(1)$ auxiliary positions says nothing about how many bytes are moved.

## Learning Objectives

After completing this module, you should be able to:

1. translate a complete binary tree between zero-based array indices and parent-child relations;
2. state the max-heap, sift-down, construction, and sortdown contracts independently;
3. prove sift down using child-subheap invariants and a decreasing height variant;
4. prove bottom-up heap construction by reverse induction over internal nodes;
5. derive the linear construction bound from the distribution of node heights;
6. prove sortdown preserves a heap prefix and sorted suffix;
7. bound comparisons, exchanges, stack space, and auxiliary array positions without conflating them;
8. explain instability, duplicate behavior, lack of ordinary adaptivity, and locality costs;
9. design comparator, key, overflow, cancellation, and partial-mutation policies;
10. evaluate binary, multiway, hole-based, indirect, and introspective uses of heapsort.

## Core Exposition

### Separate the sorting and heap contracts

Let the input be records $A[0:n)$ ordered by a declared key and comparator. Successful ascending sorting requires:

$$
\forall i\in[0,n-1),\qquad A[i]\le A[i+1],
$$

and identity permutation: every input record identity occurs exactly once in the output. Stability is an additional promise, not part of ordinary heapsort.

For an active prefix $A[0:m)$, max-heap order requires:

$$
\forall i\in[1,m),\qquad
A[\lfloor(i-1)/2\rfloor]\ge A[i].
$$

This implies the active maximum is at $A[0]$: repeatedly following parents from any node reaches the root through nondecreasing keys. It does not imply that siblings, cousins, levels, or the array representation are sorted.

Heapsort composes these contracts. Construction establishes heap order over $A[0:n)$. Sortdown converts one active maximum at a time into a final suffix while preserving the complete sorting contract.

### Map the complete tree without pointers

The first $m$ array positions represent a complete tree filled level by level from left to right. For a zero-based node $i$:

$$
\ell(i)=2i+1,\qquad r(i)=2i+2.
$$

The left child exists exactly when $\ell(i)<m$; the right child exists when $r(i)<m$. A nonroot node has parent

$$
p(i)=\left\lfloor\frac{i-1}{2}\right\rfloor.
$$

For $m\ge2$, the last internal node is

$$
\left\lfloor\frac{m}{2}\right\rfloor-1,
$$

and indices $\lfloor m/2\rfloor$ through $m-1$ are leaves. Empty and singleton heaps have no internal node, so code should let the construction loop be empty rather than manufacture a negative array access.

In a bounded integer type, evaluating $2i+1$ can overflow before the comparison with $m$. Guard by proving $i<(m-1)/2$, use checked arithmetic, or derive a loop form whose active internal-node range guarantees safe multiplication. Language and index-width assumptions belong in the contract.

### Derive sift down from one possible violation

Suppose both child subtrees rooted below index $root$ are max heaps, while the record at $root$ may be too small. Sift down restores the whole subtree.

At each iteration:

1. find the left child; if none exists, the saved/current record is at a leaf and repair is complete;
2. if a right child exists, compare the two children and choose the larger;
3. compare the current record with that larger child;
4. stop if the current record is at least the larger child;
5. otherwise exchange them and continue at the child's former position.

Why choose the larger child? Moving the smaller child above a larger sibling would immediately violate max-heap order at the old root. When the larger child moves up, it dominates both the other child and the demoted record. All untouched subtrees remain heaps; the only possible violation follows the demoted record downward.

The remaining height strictly decreases on every exchange. At a leaf it is zero, so repair terminates after at most the original subtree height. A binary level uses at most one child-selection comparison and one parent-child comparison.

### Prove sift down formally

Maintain these properties around the current position $i$:

- every subtree not on the traversed repair path is a heap;
- every node strictly above $i$ satisfies heap order;
- the subtree rooted at $i$ would be a heap except possibly for its root record;
- the array contains exactly the same record identities as at entry.

If there is no child, the possible root violation cannot exist. If the current record dominates the larger child, it dominates every existing child, so its already-heaped child subtrees compose into a heap. Otherwise, exchanging with the larger child repairs the old position: the promoted child dominates its sibling, and it was greater than the demoted record. Only the new position of the demoted record can violate order.

Each exchange is a bijection on positions. The remaining path height decreases, establishing termination. At exit, no possible violation remains, so the original subtree is a heap and identity permutation is preserved.

### Build a heap from the bottom up

Leaves are already one-node heaps. Process internal roots from

$$
\left\lfloor\frac{n}{2}\right\rfloor-1
$$

down through $0$, sifting each root over the full active size $n$.

Reverse induction supplies the precondition. When root $i$ is processed, each child has a larger index and was either a leaf or was processed earlier. Therefore both child subtrees are heaps, exactly what sift down requires. After repair, the subtree at $i$ is a heap. Processing a smaller index cannot destroy a completed descendant subtree except along a repair path whose own sift restores it.

After root $0$ is processed, its subtree is the entire complete tree, so $A[0:n)$ is a max heap. This method is not the same as inserting records one by one and swimming each new record. Repeated insertion is correct but can use $\Theta(n\log n)$ construction work.

### Derive the linear construction bound

A tempting loose bound multiplies $O(n)$ internal roots by $O(\log n)$ per sift. It is valid as an upper bound but hides the stronger result because it assigns root height to every node.

Charge each starting node only for its own possible descent. Let $N_{\ge h}$ be the number of heap nodes whose subtree height is at least $h$. In a complete binary heap,

$$
N_{\ge h}\le\left\lfloor\frac{n}{2^h}\right\rfloor.
$$

Summing heights by horizontal layers gives

$$
\begin{aligned}
\sum_v \operatorname{height}(v)
&=\sum_{h\ge1}N_{\ge h}\\
&\le\sum_{h\ge1}\left\lfloor\frac{n}{2^h}\right\rfloor\\
&<n\sum_{h\ge1}\frac1{2^h}\\
&=n.
\end{aligned}
$$

Thus a swap-based build performs fewer than $n$ downward exchanges under this charging model and fewer than $2n$ child-selection plus parent-child comparisons in the conventional binary routine. Exact counts depend on equality, missing right children, early stopping, and the chosen code, but the asymptotic build is $O(n)$.

For a perfect heap with $n=2^{H+1}-1$, the exact sum of node heights is

$$
\sum_{d=0}^{H}2^d(H-d)
=2^{H+1}-H-2
=n-H-1.
$$

The small number of high roots cannot outweigh the many leaves and near-leaf nodes.

### Prove sortdown with a two-region invariant

After construction, set active size $m=n$. Maintain:

1. $A[0:m)$ is a max heap;
2. $A[m:n)$ is sorted ascending;
3. every key in the active heap is at most every key in the suffix;
4. the whole array remains an identity permutation of the input.

Initially the suffix is empty, so its order and cross-boundary property hold vacuously.

While $m>1$, the root is the maximum active record. Exchange $A[0]$ with $A[m-1]$, then decrement $m$. The former maximum is now the first record of the suffix. It is at least every still-active key and no greater than maxima extracted earlier, so the suffix remains ascending.

The record moved to the root may violate heap order. Both child subtrees remain heaps, so sift down over $A[0:m)$ restores the prefix without touching the suffix. Exchange and repair preserve identities.

At termination, $m\le1$. A singleton or empty prefix is sorted, the suffix is sorted, and the cross-boundary property orders their concatenation. Therefore the complete array is an ordered identity permutation.

### Bound time, comparisons, movement, and storage separately

Construction is $O(n)$. After each extraction, a sift descends at most

$$
\left\lfloor\log_2 m\right\rfloor
$$

levels for the current active size $m$. A direct loose comparison bound for the reviewed binary routine is

$$
C(n)
<
2n
+
2\sum_{m=1}^{n-1}\left\lfloor\log_2 m\right\rfloor
=O(n\log n).
$$

The worst case is $\Theta(n\log n)$, and every input receives the deterministic $O(n\log n)$ upper bound. Do not silently strengthen that statement to the same exact count or even the same lower bound on every input: equal keys can make an early-stopping sift return near the root.

An iterative in-array implementation uses $O(1)$ auxiliary record positions beyond the array. It still performs $n-1$ boundary exchanges plus repair movement. If a record is wide, bytes moved can dominate comparisons. Sorting an index or pointer array reduces record movement but uses $O(n)$ auxiliary references and changes locality.

A recursive sift uses $O(\log n)$ call-stack space. Cached keys, decorated records, rollback copies, telemetry buffers, and comparator state must also be counted if present.

### Distinguish heap order, adaptivity, duplicates, and stability

A descending array is already a max heap, but sortdown still repeatedly extracts and repairs. Ordinary heapsort does not exploit long ascending runs or low inversion counts in the way insertion sort or an adaptive merge strategy can.

Duplicates do not violate the heap property because equality is allowed. In an early-stopping implementation, an all-equal heap can incur only constant comparisons per extraction. This is a finite behavior fact, not a stability result. Boundary exchanges can reverse equal record identities even when comparisons report equality.

For input $(2_A,1,2_B)$, the root-final exchange may place $2_A$ at the end and leave $2_B$ before it, yielding $(1,2_B,2_A)$. Keys are sorted, but original equal-key order is reversed. Making every record key include its original position can impose a total tie order, but it changes the comparison key and stores or retrieves extra information; it is not ordinary stable heapsort for free.

### Engineer movement and arity deliberately

Swap-based sift down is simple to prove and instrument. A hole-based variant saves the root record, repeatedly promotes the larger child upward, and writes the saved record once at its final position. It can reduce record writes, but its invariant must track the hole and prove that no identity is lost.

In a $d$-ary heap, children of zero-based node $i$ occupy

$$
di+1,\ldots,di+d
$$

when those indices are active. Increasing $d$ reduces height to $\Theta(\log_d n)$ but requires examining up to $d$ children to select the largest. It also changes cache lines, branches, and movement. Neither binary nor multiway arity wins universally; measure the actual key, record, and machine costs.

Bottom-up “bounce” techniques may promote larger children all the way to a leaf and then move the saved record upward to its final place, reducing comparisons during sortdown. They add implementation and proof complexity. Keep the baseline contract observable before adopting such tuning.

### Preserve comparator, ownership, and cancellation semantics

The comparator must define a consistent ordering for all records encountered. NaN, mutable keys, locale changes, time-dependent callbacks, or inconsistent user code can invalidate both the heap and sorted-suffix proofs. Prefer projecting immutable keys once when policy and memory permit, or explicitly require a pure comparator.

An exception during in-place build or sortdown usually leaves a valid owner for every record but an unspecified permutation that may be neither a heap nor sorted. Promise only the safety actually implemented. Strong rollback requires sorting a private copy/index or recording enough state to undo mutation, with corresponding space and latency.

Cancellation checkpoints can be placed between root repairs or at bounded intervals inside long repair sequences. The API must say whether cancellation leaves partial mutation, whether all identities remain owned, and whether the caller may retry. Arithmetic overflow, concurrent mutation, aliasing, and destructors/move operations can violate identity even when comparison logic is correct.

### Preserve executable operation evidence

The following implementation uses zero-based active sizes and swap-based sift down. Its counters separate construction from sortdown. A comparison means one evaluation between two keys; a swap means one pairwise position exchange, including every root-suffix exchange.

<!-- bijux-verify: {"id":"binary-heapsort-ledger","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"input=(4, 10, 3, 5, 1)\nheap=(10, 5, 3, 4, 1) build_comparisons=6 build_swaps=2\nsorted=(1, 3, 4, 5, 10) sortdown_comparisons=6 sortdown_swaps=7\ntotal_comparisons=12 total_swaps=9\n","stderr":""}} -->
~~~python
def sift_down(items, root, size):
    comparisons = 0
    swaps = 0

    while True:
        left = 2 * root + 1
        if left >= size:
            return comparisons, swaps

        largest = left
        right = left + 1
        if right < size:
            comparisons += 1
            if items[right] > items[left]:
                largest = right

        comparisons += 1
        if items[root] >= items[largest]:
            return comparisons, swaps

        items[root], items[largest] = items[largest], items[root]
        swaps += 1
        root = largest


def heapsort(values):
    items = list(values)
    build_comparisons = 0
    build_swaps = 0

    for root in range(len(items) // 2 - 1, -1, -1):
        comparisons, swaps = sift_down(items, root, len(items))
        build_comparisons += comparisons
        build_swaps += swaps

    heap = tuple(items)
    sortdown_comparisons = 0
    sortdown_swaps = 0

    for end in range(len(items) - 1, 0, -1):
        items[0], items[end] = items[end], items[0]
        sortdown_swaps += 1
        comparisons, swaps = sift_down(items, 0, end)
        sortdown_comparisons += comparisons
        sortdown_swaps += swaps

    return (
        heap,
        tuple(items),
        build_comparisons,
        build_swaps,
        sortdown_comparisons,
        sortdown_swaps,
    )


values = (4, 10, 3, 5, 1)
heap, ordered, build_c, build_s, sort_c, sort_s = heapsort(values)
print(f"input={values}")
print(
    f"heap={heap} build_comparisons={build_c} "
    f"build_swaps={build_s}"
)
print(
    f"sorted={ordered} sortdown_comparisons={sort_c} "
    f"sortdown_swaps={sort_s}"
)
print(f"total_comparisons={build_c + sort_c} total_swaps={build_s + sort_s}")
~~~

The heap layout is one valid deterministic consequence of this routine. The mathematical contract should assert heap order and identity permutation rather than require the same layout from every valid construction algorithm.

### Evaluate the algorithm before choosing it

Validate:

- ascending order under the declared comparator;
- identity permutation, including equal-key record identities;
- heap order after every construction root;
- prefix heap, suffix order, and cross-boundary order after every extraction;
- child-index safety at empty, singleton, odd, even, and maximum sizes;
- comparator and key-extraction failure at every call position;
- cancellation and ownership at every mutation boundary.

Measure comparisons, child-selection comparisons, root-child comparisons, exchanges, bytes moved, key projections, depth, cache misses, branch behavior, and end-to-end latency. Use empty, singleton, sorted, reverse, heap-ordered, nearly sorted, all-equal, low-cardinality, wide-record, expensive-key, random, and adversarial inputs.

Compare against merge, quick, insertion, radix-eligible, and hybrid alternatives under identical data and contracts. A deterministic asymptotic bound can be decisive for one service and still lose on locality or stability in another.

## Definitions and Notation

- $A[0:n)$ is the zero-based array to sort.
- $m$ is the active heap size; positions $m$ through $n-1$ form the suffix.
- $\ell(i)=2i+1$ and $r(i)=2i+2$ are child indices.
- $p(i)=\lfloor(i-1)/2\rfloor$ is the parent for $i>0$.
- $\operatorname{depth}(v)$ counts edges from the root to node $v$.
- $\operatorname{height}(v)$ is the greatest edge count from $v$ to a descendant leaf.
- A max heap has each parent key at least its children.
- Sift down repairs a root whose child subtrees already satisfy heap order.
- Heapify here means bottom-up construction unless another method is named.
- Sortdown means repeated maximum placement and active-prefix repair.
- $C(n)$ counts key-comparator evaluations under a stated implementation.
- $M(n)$ counts record exchanges or bytes moved; it is not inferred from $C(n)$.
- Auxiliary space excludes the input array but includes explicit buffers, indices, keys, and call frames.
- Identity permutation preserves record instances and multiplicities, not merely key values.

## Mechanisms, Invariants, or Proof Structure

Use this review sequence for any heap-based sort:

1. State ascending/descending direction, key projection, equality, and identity contract.
2. State zero- or one-based indexing and the active half-open range.
3. Derive parent and child formulas under that convention.
4. Prove which indices are leaves and identify the last internal root.
5. State sift down's precondition: child subtrees are heaps; only the root may violate.
6. State the path invariant and the remaining-height termination variant.
7. Prove larger-child selection restores the old root before descent.
8. Prove swaps or hole moves preserve every record identity.
9. Apply reverse induction to bottom-up construction.
10. Sum actual node heights rather than multiplying all nodes by root height.
11. State the sortdown prefix, suffix, cross-boundary, and permutation invariant.
12. Shrink before repair and prove the suffix is untouched.
13. Derive separate comparison, movement, stack, and auxiliary-space bounds.
14. Audit stability, duplicates, comparator consistency, overflow, failure, and cancellation.
15. Reproduce executable counters, then test invariant checkpoints and competing algorithms.

The proof chain is compositional:

$$
\text{child heaps}
\Longrightarrow
\text{sifted subtree}
\Longrightarrow
\text{whole heap}
\Longrightarrow
\text{one fixed maximum}
\Longrightarrow
\text{sorted permutation}.
$$

If a tuned implementation cannot expose an equivalent chain, its speed result is not enough to establish correctness.

## Alternatives and Trade-Offs

| Approach | Time guarantee | Extra positions | Stable by default | Characteristic trade-off |
|---|---:|---:|---:|---|
| Binary heapsort | $O(n\log n)$ | $O(1)$ | No | Deterministic bound, irregular level access |
| Merge sort | $O(n\log n)$ | Often $O(n)$ for arrays | Yes when ties choose left | Predictable scans and movement, buffer cost |
| Randomized quicksort | Expected $O(n\log n)$ under its model | Stack dependent | No | Strong locality, possible quadratic executions |
| Introspective sort | $O(n\log n)$ with safe fallback | Usually $O(\log n)$ stack | No | Fast partitioning plus heap fallback complexity |
| Insertion sort | $O(n^2)$ worst case | $O(1)$ | Yes conventionally | Adaptive and efficient for small/nearly sorted ranges |
| Indirect heapsort | $O(n\log n)$ | $O(n)$ references | Tie policy dependent | Less wide-record movement, extra indirection |
| $d$-ary heapsort | $O(n\log_d n)$ levels | $O(1)$ | No | Lower height, more child selection per level |

Use heapsort when deterministic comparison bounds and tight auxiliary storage dominate stability and scan locality. Use merge-based sorting when stable ordering, sequential access, or external-memory behavior dominates. Use introspection when quick partitioning is desirable but a deterministic worst-case ceiling is required.

## Failure Modes and Misconceptions

1. **Mixed index convention:** using $2i$ with a zero-based array makes the root its own child.
2. **Capacity as size:** repair crosses into unused storage or the fixed suffix.
3. **Wrong build start:** skipping the last internal node can leave a violation.
4. **Forward construction order:** a parent is sifted before its child subtrees satisfy the precondition.
5. **Arbitrary child descent:** choosing the left child can leave a larger right child above it.
6. **Single-level repair:** one exchange does not prove the demoted record dominates grandchildren.
7. **Late shrink:** the just-fixed maximum reenters the heap and can move again.
8. **Heap-equals-sorted belief:** parent-child order leaves many incomparable array positions.
9. **Linear-build proof error:** $n$ logarithmic upper bounds do not establish the tighter aggregate.
10. **Repeated insertion substitution:** swimming $n$ arrivals can require $\Theta(n\log n)$.
11. **Unqualified exact counts:** equality, missing children, early exit, and implementation variants change constants.
12. **Stable-in-place inference:** distant exchanges can reverse equal identities.
13. **Free movement assumption:** exchanging two wide records may cost far more than comparing their keys.
14. **Free comparator assumption:** projections, locale rules, callbacks, and remote data can dominate.
15. **Universal locality claim:** tree-level jumps interact with cache and arity differently by machine.
16. **Overflow-blind children:** $2i+2$ can wrap before a bounds check.
17. **Rollback fiction:** in-place callback failure generally leaves a partial permutation.
18. **Concurrent mutation:** changing keys while sorting invalidates prior comparisons and heap order.
19. **Recursive-space omission:** a recursive repair is not $O(1)$ call-stack space.
20. **Benchmark monoculture:** random narrow integers do not represent equal keys, wide records, or hostile callbacks.

## Worked Examples

### Example 1

**Question:** For a zero-based heap of size $10$, give the children of index $3$, the parent of index $8$, the last internal node, and the leaf range.

**Reasoning:** $\ell(3)=7$ and $r(3)=8$, both below $10$. Also $p(8)=\lfloor7/2\rfloor=3$. The last internal index is $\lfloor10/2\rfloor-1=4$.

**Conclusion:** Index $3$ has children $7,8$; index $8$ has parent $3$; internal nodes are $0$ through $4$; leaves are $5$ through $9$.

### Example 2

**Question:** Sift the root of $(4,9,7,3,2,6,5)$ when both child subtrees are heaps.

**Reasoning:** Compare children $9$ and $7$, choose $9$, and exchange it with $4$. The array becomes $(9,4,7,3,2,6,5)$. At index $1$, compare children $3$ and $2$; $4$ already dominates $3$, so stop.

**Conclusion:** Repair uses four key comparisons and one exchange, yielding a max heap.

### Example 3

**Question:** Build a heap from $(4,10,3,5,1)$ bottom up.

**Reasoning:** The last internal root is index $1$. Its key $10$ dominates $5,1$. At root $0$, choose child $10$ over $3$ and exchange with $4$; then choose $5$ over $1$ and exchange with $4$.

**Conclusion:** The resulting heap is $(10,5,3,4,1)$, with six comparisons and two exchanges in the reviewed routine.

### Example 4

**Question:** What is the maximum total descent charged by bottom-up construction in a perfect heap of $31$ nodes?

**Reasoning:** Here $31=2^{5}-1$, so tree height $H=4$. There are $8$ nodes of height $1$, $4$ of height $2$, $2$ of height $3$, and $1$ of height $4$:

$$
8(1)+4(2)+2(3)+1(4)=26.
$$

Equivalently, $n-H-1=31-4-1=26$.

**Conclusion:** At most 26 downward exchanges are chargeable, demonstrating why construction is linear rather than $31\log_2 31$.

### Example 5

**Question:** Perform the first sortdown iteration from $(10,5,3,4,1)$.

**Reasoning:** Exchange root and final active record to get $(1,5,3,4\mid10)$, then shrink to $m=4$. Choose $5$, exchange, then choose $4$ below it and exchange:

$$
(1,5,3,4\mid10)
\to
(5,1,3,4\mid10)
\to
(5,4,3,1\mid10).
$$

**Conclusion:** The prefix is again a heap and $10$ is fixed in the sorted suffix.

### Example 6

**Question:** Give a direct loose comparison bound for the reviewed routine at $n=8$.

**Reasoning:** Construction uses fewer than $2n=16$ comparisons. Post-extraction active sizes are $7$ through $1$, so repair uses at most

$$
2\sum_{m=1}^{7}\lfloor\log_2m\rfloor
=2(0+1+1+2+2+2+2)
=20.
$$

**Conclusion:** Fewer than 36 comparisons follows from this deliberately loose proof; a tighter implementation-specific result may be smaller.

### Example 7

**Question:** Show that ordinary heapsort can reverse equal records.

**Reasoning:** Label equal keys in input order: $(2_A,1,2_B)$. A valid max heap can retain this layout. The first root-suffix exchange fixes $2_A$ at the end and leaves $2_B$ active. Completing sortdown yields $(1,2_B,2_A)$.

**Conclusion:** Keys are ordered, but $B$ precedes $A$; heapsort is not stable.

### Example 8

**Question:** What happens to the reviewed early-stopping code on seven equal keys?

**Reasoning:** Build checks child equality but performs no repair exchange. Each sortdown boundary exchange swaps equal keys, and sift down stops at the root after checking its existing children. The number of comparisons is linear for this special family even though identities may move.

**Conclusion:** Duplicate behavior can improve the finite comparison count without providing adaptivity in general or stability.

### Example 9

**Question:** Does an eight-ary heap automatically use fewer comparisons than a binary heap on one million records?

**Reasoning:** Its height is about $\log_8 n$, roughly one third of $\log_2 n$, but choosing a maximum among up to eight children needs seven child comparisons before the parent comparison. Cache-line placement and record movement also change.

**Conclusion:** Lower height is not a proof of lower total cost; compare complete operation and machine ledgers.

### Example 10

**Question:** A quicksort service switches to heapsort after a depth limit. Which contract must cross the boundary?

**Reasoning:** The fallback must sort exactly the current half-open subrange under the same key/comparator, preserve every record identity, respect the same failure ownership policy, and avoid touching completed regions. It must receive a local length and translate children relative to the subrange base.

**Conclusion:** “Call heapsort” is insufficient until range, ordering, identity, and failure contracts align.

## Cross-Program Connections

- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) owns heap priority-queue APIs, indexed heaps, updates, and reusable container invariants.
- [Programming Languages & Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) owns comparator laws, exceptional values, callbacks, generics, moves, and exception guarantees.
- [Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) owns index overflow, aliasing, stack use, ownership, cancellation, and byte movement.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) owns cache-line, branch, prefetch, and memory-bandwidth mechanisms behind heap access.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns hostile input/callback models, resource limits, and denial-of-service controls.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns property, differential, fault-injection, invariant, and performance testing.

## References

1. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. [*Introduction to Algorithms*, fourth edition](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), MIT Press, 2022. Heap properties, heap construction, heapsort correctness, and analysis.
2. Donald E. Knuth. [*The Art of Computer Programming, Volume 3: Sorting and Searching*, second edition](https://www.informit.com/store/art-of-computer-programming-volume-3-sorting-and-searching-9780321635785), Addison-Wesley Professional, 1998. Foundational comparison-sorting and heap analysis.
3. J. W. J. Williams. [“Algorithm 232: Heapsort”](https://doi.org/10.1145/512274.512284), *Communications of the ACM* 7(6), 1964, pp. 347–348. Primary heapsort publication.
4. Robert W. Floyd. [“Algorithm 245: Treesort 3”](https://doi.org/10.1145/355588.365103), *Communications of the ACM* 7(12), 1964, p. 701. Primary bottom-up in-place heap-sorting refinement.
5. Robert Sedgewick and Kevin Wayne. [“Priority Queues”](https://algs4.cs.princeton.edu/24pq/), companion to *Algorithms*, fourth edition, last modified 2022; consulted 2026-09-04. Binary heap operations, linear bottom-up construction, heapsort, variants, and implementation evidence.
6. David R. Musser. [“Introspective Sorting and Selection Algorithms”](https://doi.org/10.1002/%28SICI%291097-024X%28199708%2927%3A8%3C983%3A%3AAID-SPE117%3E3.0.CO%3B2-%23), *Software: Practice and Experience* 27(8), 1997, pp. 983–993. Primary worst-case fallback construction using heapsort.
7. ACM, IEEE Computer Society, and AAAI. [*Computer Science Curricula 2023: Algorithmic Foundations*](https://csed.acm.org/al-cs-core/), endorsed 2024; consulted 2026-09-04. Current curricular scope for sorting, heaps, correctness, complexity, implementation, and empirical evaluation.

## Exercises

### Exercise 1

For a zero-based active heap of size $m$, prove that indices $\lfloor m/2\rfloor$ through $m-1$ are exactly the leaves. Cover $m=0$, $m=1$, odd $m$, and even $m$, and explain one overflow-safe way to decide whether an index has a child.

### Exercise 2

Prove swap-based sift down correct when both child subtrees are max heaps and only their parent may violate order. State initialization, preservation for both stop and exchange branches, a termination variant, identity preservation, and the maximum comparisons per descended binary level.

### Exercise 3

Apply the reviewed bottom-up routine to $(2,9,7,6,5,4,3,1)$. Show the array after each internal root is processed, give the final heap, and count build comparisons and exchanges. Then explain why repeated insertion is not entitled to the same linear proof.

### Exercise 4

Prove the four-part sortdown invariant and trace the complete sort of $(10,5,3,4,1)$ from its already-built heap. Include each active boundary and explain where stability can fail if the two key-$3$ records in a larger example are distinguishable.

### Exercise 5

A memory-constrained service sorts fifty million wide records by a user-defined key. Inputs and callbacks may be hostile; stability is not required; latency, cancellation, and record ownership after failure are contractual. Design whether and how heapsort should be used, including representation, comparator/key policy, range arithmetic, movement, fallback role, validation, telemetry, and competing baselines.

## Answers to the Exercises

### Answer 1

A node $i$ has a left child exactly when

$$
2i+1<m.
$$

For $i\ge\lfloor m/2\rfloor$, $2i+1\ge2\lfloor m/2\rfloor+1\ge m$, for both odd and even $m$, so no left child exists. These indices are leaves.

For $0\le i<\lfloor m/2\rfloor$, $2i+1<m$, so a left child exists and the node is internal. Therefore the leaf set is exactly

$$
\{\lfloor m/2\rfloor,\ldots,m-1\}.
$$

When $m=0$, that index interval is empty. When $m=1$, it is $\{0\}$, the singleton root/leaf. For even $m=2q$, internal indices are $0$ through $q-1$ and leaves $q$ through $2q-1$; the last internal node has only a left child. For odd $m=2q+1$, internal indices are $0$ through $q-1$ and leaves $q$ through $2q$; the last internal node has two children.

Instead of computing $2i+1$ before checking overflow, code can establish $i<m/2$ using a division-based internal-node test, then use checked multiplication/addition for the child indices. The exact safe form depends on the integer model.

### Answer 2

Initially both child subtrees are heaps, all subtrees away from the root are valid, and only the root record can be smaller than a child. The array begins as an identity permutation of itself.

At current index $i$, if no child exists, its subtree is a one-node heap. If children exist, choose the larger. If the current key is at least that child, it is at least every child; composing the root with the already-heaped child subtrees proves the whole current subtree is a heap, so stopping is correct.

Otherwise exchange the current record with the larger child. The promoted key dominates both its sibling and the demoted key, so the old position becomes heap ordered. Untouched subtrees remain heaps. Only the demoted record at the chosen child can violate its new children, reproducing the invariant one level lower.

The remaining height is a nonnegative integer and drops by one with each exchange. Therefore the process terminates at a leaf or a dominating position. Exchanges are bijections, so record identities and multiplicities are preserved. Each descended binary level uses at most one comparison to choose between two children and one to compare parent with the larger child; a node with only a left child uses only the latter.

### Answer 3

The active size is $8$, and internal roots are $3,2,1,0$.

- Root $3$ has child $1$ at index $7$; $6$ dominates it, so the array remains $(2,9,7,6,5,4,3,1)$.
- Root $2$ has children $4,3$; $7$ dominates them, so the array remains unchanged.
- Root $1$ has children $6,5$; $9$ dominates them, so the array remains unchanged.
- Root $0$ has children $9,7$; exchange $2$ with $9$, producing $(9,2,7,6,5,4,3,1)$. At index $1$, choose $6$ over $5$ and exchange, producing $(9,6,7,2,5,4,3,1)$. At index $3$, $2$ dominates its child $1$, so repair stops.

The final heap is

$$
(9,6,7,2,5,4,3,1).
$$

In the reviewed counter model, roots $3,2,1$ use $1,2,2$ comparisons; root $0$ uses $2+2+1=5$. The total is $10$ comparisons and $2$ exchanges.

Bottom-up construction starts many repairs near leaves, so total possible descent is the sum of node heights, less than $n$. Repeated insertion instead swims the $k$th arrival through as many as $\lfloor\log_2 k\rfloor$ levels. Summing those independent arrival heights can be $\Theta(n\log n)$, so the bottom-up aggregate proof does not transfer.

### Answer 4

Initially $m=5$, the whole prefix $(10,5,3,4,1)$ is a max heap, and the suffix is empty.

1. Exchange $10$ with $1$, shrink, and repair:

   $$
   (10,5,3,4,1)
   \to
   (1,5,3,4\mid10)
   \to
   (5,4,3,1\mid10).
   $$

2. Exchange $5$ with $1$, shrink, and repair:

   $$
   (1,4,3\mid5,10)
   \to
   (4,1,3\mid5,10).
   $$

3. Exchange $4$ with $3$, shrink; $3$ dominates child $1$:

   $$
   (3,1\mid4,5,10).
   $$

4. Exchange the final active pair:

   $$
   (1\mid3,4,5,10).
   $$

At each boundary, the prefix is a max heap; the suffix is ascending; every prefix key is at most every suffix key; and exchanges preserve identity permutation. The extracted root is the active maximum, so placing it immediately before previously extracted, larger-or-equal maxima preserves suffix order. Repair is bounded by the shrunken size and cannot touch the suffix. With one active record left, concatenation is globally sorted.

If equal key-$3$ records are distinguishable, either can become the root or be exchanged across the active boundary first. The invariant compares keys only and permits equality, so it cannot preserve their original identity order. Stability would need a different algorithm or an explicit original-position tie key.

### Answer 5

Represent the sort as an array of compact indices or pointers into the wide-record store rather than repeatedly exchanging full records. This uses $O(n)$ references, so first verify that the memory budget can hold them; if it cannot, in-place record movement must be measured explicitly and may make heapsort unsuitable. Sort exactly one checked half-open range, use an index width large enough for fifty million positions, and use overflow-safe child arithmetic relative to the range base.

Materialize immutable keys once when key size and memory permit. Otherwise require a pure, deterministic comparator/key callback and impose call, time, allocation, and cancellation budgets. Define exceptional values such as NaN. On callback failure or cancellation, keep every record owned and report that index order may be partially permuted. If strong rollback is required, sort a private index array and publish it only after success.

Heapsort is a candidate when a deterministic $O(n\log n)$ comparison ceiling and bounded in-place workspace matter. It can also be the depth fallback behind three-way introspective partitioning, limiting worst-case work while using quicker local scans normally. The fallback must accept the same subrange, comparator, identity, cancellation, and error contracts. If stable output or sequential external I/O is required later, use a stable merge/external sort instead.

Validate order and identity, instrument heap invariants after construction roots and sortdown steps on small cases, and fault-inject every callback/cancellation boundary. Cover empty/singleton, maximum size, sorted, reverse, heap-ordered, all equal, low-cardinality, wide records, expensive keys, and hostile callbacks.

Record comparisons, callback calls/time, exchanges, bytes moved, cache misses, branch behavior, cancellation latency, failures, maximum repair depth, and end-to-end tail latency. Compare direct heapsort, indirect heapsort, three-way introsort with heap fallback, and merge/external approaches on identical preserved inputs. Choose from contractual resource limits and measured workload evidence, not the $O(n\log n)$ label alone.
