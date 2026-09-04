---
module_id: ALGE-011
program: Algorithm Engineering
level: 1
module_number: 11
title: Linear and Binary Search
status: complete
last_verified: 2026-09-04
---

# Linear and Binary Search

## One-Page Review

### Governing question

Given a sequence, a target, and a precise result contract, when should an implementation inspect items in order, and when may it discard an ordered region without inspecting every item?

### Essential definitions

- **Linear search** examines candidates in a defined order until it finds an acceptable result or exhausts the search domain.
- **Binary search** uses an ordered domain and a monotone decision predicate to eliminate part of the remaining interval at every iteration.
- A **search contract** specifies whether the result is membership, an arbitrary match, the first or last match, a count, an insertion boundary, or an error.
- The **lower bound** of target $x$ in sorted sequence $A[0:n]$ is the first index whose value is not less than $x$.
- The **upper bound** is the first index whose value is greater than $x$.
- A **half-open interval** $[lo,hi)$ contains indices $lo,lo+1,\ldots,hi-1$ and has length $hi-lo$.
- A predicate $P(i)$ is **monotone** over an ordered index domain when it changes at most once from false to true.
- A **partition point** is the smallest index $i$ for which a monotone predicate is true, with $n$ as the sentinel when it is never true.
- A **comparison contract** defines the ordering relation, key projection, treatment of exceptional values, and consistency assumptions.

### Central model, mechanism, or theorem

For sorted $A[0:n]$, define

$$
\operatorname{lower}(x)
=
\min\bigl(\{i\in\{0,\ldots,n-1\}:A[i]\ge x\}\cup\{n\}\bigr).
$$

Maintain a half-open candidate interval $[lo,hi)$ and the partition invariant

$$
\forall i<lo,\ A[i]<x,
\qquad
\forall i\ge hi,\ A[i]\ge x.
$$

At $mid=lo+\lfloor(hi-lo)/2\rfloor$, set $lo=mid+1$ if $A[mid]<x$; otherwise set $hi=mid$. The interval strictly shrinks. When $lo=hi$, the invariant identifies the unique partition point. The maximum number of loop iterations is

$$
\left\lceil \log_2(n+1)\right\rceil,
$$

whereas an unsuccessful linear search performs $n$ target comparisons.

### Critical invariants

- State the exact return meaning before selecting an algorithm.
- Binary search requires a stable ordered domain under the same comparison used by the search.
- The answer remains inside $[lo,hi]$ while indices in $[lo,hi)$ remain unresolved.
- Each iteration strictly decreases $hi-lo$; otherwise termination is not proved.
- Use $mid=lo+(hi-lo)//2$ in bounded-integer settings to avoid overflowing $lo+hi$.
- Duplicates make “a match,” “first match,” and “equal range” different contracts.
- Equality is tested only after a valid boundary index has been returned.
- Random access is an implementation premise, not a consequence of sortedness.
- Sorting or index construction must be charged to the lifecycle that benefits from it.
- Concurrent mutation can invalidate both the ordering premise and the interval proof.

### Common failures

Typical failures are searching unsorted data; returning an arbitrary duplicate when the contract requires the first; mixing inclusive and half-open endpoints; reading $A[n]$ before checking the sentinel; failing to advance past $mid$; overflowing midpoint arithmetic; using a comparator that is inconsistent or stateful; comparing keys under one normalization but sorting under another; assuming logarithmic comparisons imply logarithmic elapsed time on a linked structure; hiding preprocessing cost; using binary search for a predicate that can switch more than once; and treating library-specific duplicate behavior as portable.

### Compact example

For $A=(1,2,2,2,5,9)$ and $x=2$, lower bound returns $1$ and upper bound returns $4$. Therefore the equal range is $[1,4)$, membership is true, the first match is $1$, and the number of matches is $4-1=3$. One pair of boundary algorithms supports four explicit contracts without relying on an arbitrary-match result.

### Connections

[ALGE-003](./003-loop-invariants-for-algorithm-correctness.md) supplies loop-invariant proof structure; [ALGE-005](./005-asymptotic-time-and-space.md) supplies cost notation; [ALGE-008](./008-lower-bounds-and-adversary-arguments.md) supplies comparison lower bounds; [ALGE-010](./010-combining-proof-and-measurement-in-algorithm-evaluation.md) supplies evaluation discipline. [ALGE-012](../ROADMAP.md) begins the sorting sequence that constructs ordered search domains.

## Governing Question

Search is often introduced as “find a value,” but that sentence omits nearly every decision that makes an implementation correct. Is absence represented by a sentinel or an exception? If duplicates exist, may any matching index be returned, or must the earliest record win? Is the input already ordered under exactly the comparison used at query time? May the sequence change during the operation? Does the lifecycle contain one query or millions?

Linear and binary search answer different structural questions. Linear search needs only an enumerable domain and an acceptance predicate. Binary search needs a partition: after one observation, it must be sound to reject a whole region. The algorithmic gain comes from that proof obligation, not from the word “sorted” by itself.

This module develops both algorithms as contracts, invariants, and engineering choices. It treats lower and upper bounds as the canonical binary-search primitives because they handle absence and duplicates without special cases. It also charges construction, storage, comparison, and update costs so that logarithmic query complexity is not mistaken for a complete system decision.

## Why This Matters

Search sits inside parsers, routing tables, database operators, compilers, schedulers, symbol tables, storage indexes, and user interfaces. A boundary error can silently return the wrong policy, price tier, time interval, or version. A duplicate-handling mismatch can make results nondeterministic across library versions. A comparator mismatch can turn a formally correct loop into an invalid program.

The topic is also a compact laboratory for algorithm engineering. It joins:

- contract design: membership, position, boundary, range, or predecessor;
- proof: initialization, preservation, termination, and postcondition;
- lower bounds: why ordered comparisons permit logarithmic decisions;
- representation: arrays, linked structures, remote pages, and compressed blocks;
- lifecycle economics: scan now, sort once, or maintain an index;
- measurement: comparisons, key projections, bytes touched, branches, and latency.

The central habit generalizes. Many “binary search” problems do not search stored values at all. They find the first feasible capacity, timestamp, version, or numerical threshold. The transferable skill is recognizing and proving a monotone predicate.

## Prerequisites and Retrieval

Retrieve:

- sequences, indices, half-open slices, sentinels, and total versus partial functions;
- preconditions, postconditions, loop invariants, variants, and boundary cases;
- logarithms, ceilings, floors, and geometric shrinkage;
- comparison models, adversary arguments, and decision trees;
- arrays, linked sequences, iterators, caches, and mutation semantics;
- stable sorting, key projections, and strict ordering relations;
- benchmark contracts, operation counters, and lifecycle cost accounting.

You should be able to explain why $[lo,hi)$ is empty exactly when $lo=hi$, why advancing from $mid$ sometimes requires $mid+1$, and why a sorted sequence under one key is not necessarily sorted under another.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish membership, arbitrary-match, first-match, last-match, boundary, predecessor, successor, and equal-range contracts;
2. derive and prove a linear-search invariant and cost bound;
3. express binary search as partition-point discovery for a monotone predicate;
4. prove lower-bound search by initialization, preservation, termination, and postcondition;
5. derive upper bound and an equal range without duplicate-specific loops;
6. calculate exact worst-case comparison and iteration bounds;
7. diagnose endpoint, midpoint, sentinel, comparator, and mutation defects;
8. evaluate binary search on arrays, iterators, memory hierarchies, and expensive keys;
9. account for sorting, indexing, updates, and repeated-query lifecycles;
10. select and validate a search strategy for an unfamiliar production workload.

## Core Exposition

### Start with the result contract

Let $A[0:n]$ be a finite sequence and let $x$ be a target. Plausible contracts include:

| Contract | Result |
|---|---|
| Membership | whether any $A[i]$ matches $x$ |
| Arbitrary match | some matching index, with no duplicate-position promise |
| First match | minimum matching index |
| Last match | maximum matching index |
| Lower bound | first index with $A[i]\ge x$ |
| Upper bound | first index with $A[i]>x$ |
| Equal range | half-open interval containing all values equal to $x$ |
| Predecessor | greatest admissible value below, or at most, $x$ |
| Successor | least admissible value above, or at least, $x$ |

These are not interchangeable. On $A=(2,2,2)$, every index satisfies arbitrary match, only $0$ satisfies first match, and the lower/upper boundaries are $0$ and $3$. If no item equals $x$, a boundary remains meaningful: it is an insertion position. An arbitrary-match API instead needs a distinct absence representation.

Specify equality and ordering too. Records may be compared by timestamp, normalized name, composite key, or application-defined rank. If sorting used key $k_s$ and searching uses key $k_q$, correctness requires that their induced ordering partitions agree for the query. Locale changes, case folding, floating exceptional values, mutable fields, and versioned normalization can break that premise.

### Linear search requires the weakest structure

For first-match linear search, inspect indices from left to right:

1. initialize $i=0$;
2. while $i<n$ and $A[i]$ does not match $x$, increment $i$;
3. return $i$ if $i<n$, otherwise return absence.

A useful invariant at the loop head is

$$
0\le i\le n
\quad\land\quad
\forall j\in[0,i),\ A[j]\not\sim x,
$$

where $\sim$ is the contract's match relation.

Initialization holds because $[0,0)$ is empty. If the loop continues, $A[i]$ is known not to match; incrementing $i$ extends the rejected prefix by one and preserves the invariant. The variant $n-i$ is a nonnegative integer that decreases, so the loop terminates. At exit, either $i<n$ and $A[i]\sim x$, making $i$ the first match, or $i=n$ and the invariant proves absence.

If the first match is at index $k$, the usual implementation performs $k+1$ match tests. An unsuccessful query performs $n$. The best case is one comparison for nonempty input; the worst case is $n$; expected cost depends on an explicit position/absence distribution.

Linear search remains attractive when the sequence is small, unsorted, streamed once, expensive to preprocess, frequently changing, or likely to match near the front. It supports arbitrary acceptance predicates and sequential storage. Its simplicity also reduces constant overhead and proof surface.

### Binary search needs a monotone partition

Suppose a Boolean predicate $P(i)$ over indices has the form

$$
\underbrace{\text{false},\ldots,\text{false}}_{\text{possibly empty}},
\underbrace{\text{true},\ldots,\text{true}}_{\text{possibly empty}}.
$$

The partition point is

$$
p=\min\bigl(\{i\in\{0,\ldots,n-1\}:P(i)\}\cup\{n\}\bigr).
$$

For lower bound, $P(i)$ is $A[i]\ge x$. Sortedness makes this predicate monotone. For upper bound, $P(i)$ is $A[i]>x$. The same loop can find the first feasible capacity, first timestamp at or after a cutoff, first software version satisfying a feature predicate, or smallest integer budget that meets a requirement—provided monotonicity is proved.

The right question is not “can I compare the middle?” It is “does the result of this comparison justify eliminating every index on one side?” If $P$ can revert from true to false, discarding a half is unsound.

### Derive lower bound with a half-open interval

Initialize $lo=0$ and $hi=n$. Define the conceptual sentinels:

$$
P(-1)=\text{false},
\qquad
P(n)=\text{true}.
$$

The implementation never reads those positions; they make the boundary statement uniform. Maintain

$$
0\le lo\le hi\le n,
$$

$$
\forall i<lo,\ \neg P(i),
\qquad
\forall i\ge hi,\ P(i).
$$

The unknown candidates are $[lo,hi)$. If it is nonempty, compute

$$
mid=lo+\left\lfloor\frac{hi-lo}{2}\right\rfloor.
$$

Then $lo\le mid<hi$. If $P(mid)$ is false, monotonicity proves $P(i)$ false for every $i\le mid$, so set $lo=mid+1$. If $P(mid)$ is true, every answer at or after $mid$ remains compatible but the first true might be $mid$, so set $hi=mid$.

Both updates preserve the partition facts. Both strictly reduce $hi-lo$: the false branch removes through $mid$, while the true branch removes after but retains $mid$. At termination $lo=hi$. Every earlier index is false and every index from $lo$ onward is true, so $lo=p$.

This derivation explains two famously error-prone details:

- the false branch uses $mid+1$ because $mid$ has been disproved;
- the true branch uses $mid$, not $mid-1$, because $mid$ may be the first true.

### Trace the boundary, not an equality branch

Let $A=(1,2,2,2,5,9)$ and seek the lower bound of $2$.

| Iteration | $lo$ | $hi$ | $mid$ | Test | Update |
|---:|---:|---:|---:|---|---|
| 1 | 0 | 6 | 3 | $A[3]=2\ge2$ | $hi=3$ |
| 2 | 0 | 3 | 1 | $A[1]=2\ge2$ | $hi=1$ |
| 3 | 0 | 1 | 0 | $A[0]=1<2$ | $lo=1$ |

The loop returns $1$. It never needs a special “found” branch. If the target is absent, the same postcondition gives the insertion boundary. For target $4$, lower bound is $4$: indices $0$ through $3$ are less than $4$, while index $4$ begins values at least $4$.

To obtain membership, compute $p=\operatorname{lower}(x)$ and then test

$$
p<n\ \land\ A[p]=x.
$$

The guard must precede the read because $p=n$ is a valid boundary result.

### Derive upper bound and duplicate ranges

Upper bound changes only the predicate:

$$
\operatorname{upper}(x)
=
\min\bigl(\{i:A[i]>x\}\cup\{n\}\bigr).
$$

Sortedness yields:

$$
\forall i<\operatorname{lower}(x),\ A[i]<x,
$$

$$
\forall i\in[\operatorname{lower}(x),\operatorname{upper}(x)),\ A[i]=x,
$$

$$
\forall i\ge\operatorname{upper}(x),\ A[i]>x.
$$

Therefore the equal range is

$$
[\operatorname{lower}(x),\operatorname{upper}(x)),
$$

and its cardinality is $\operatorname{upper}(x)-\operatorname{lower}(x)$. If the target is absent, both boundaries are the same insertion index and the range is empty. The first matching index is the lower bound when the range is nonempty; the last is upper bound minus one.

These definitions avoid fragile duplicate-specific equality loops. They also align with insertion policies: insert at lower bound to precede existing equals, or at upper bound to follow them. Physical insertion into an array-backed sequence still costs $\Theta(n)$ movements even though finding the position costs $\Theta(\log n)$ comparisons.

### Count iterations and comparisons

Let $L_t=hi-lo$ be the candidate length before iteration $t$. Each update leaves at most $\lfloor L_t/2\rfloor$ candidates in one branch or $\lceil L_t/2\rceil-1$ in the other; in either case,

$$
L_{t+1}\le\left\lfloor\frac{L_t}{2}\right\rfloor.
$$

After $t$ iterations,

$$
L_t\le\left\lfloor\frac{n}{2^t}\right\rfloor.
$$

The loop has terminated once this is zero. The exact maximum for this half-open implementation is

$$
t_{\max}=\left\lceil\log_2(n+1)\right\rceil
\quad(n\ge0).
$$

For $n=0,1,2,3,4$, the maxima are $0,1,2,2,3$. Each lower-bound iteration performs one ordering test, followed by at most one equality test if membership is requested. Thus the worst-case target-comparison count is logarithmic.

The comparison-model lower bound has the same shape. Locating an insertion position among $n+1$ possible gaps requires distinguishing $n+1$ outcomes. A binary decision tree of height $h$ has at most $2^h$ leaves, so

$$
2^h\ge n+1
\quad\Longrightarrow\quad
h\ge\left\lceil\log_2(n+1)\right\rceil.
$$

Lower-bound binary search meets this worst-case decision depth. The conclusion is model-relative: it counts binary comparison outcomes and assumes the ordered representation already exists.

### Preserve the comparison contract

Binary search correctness needs more than “the data looks sorted.” It needs a relation that partitions consistently. For ordinary ordered keys, require at least:

- comparisons are deterministic during the operation;
- the stored sequence is ordered by the same key projection and relation;
- equivalence classes are contiguous;
- no element or key mutates while it participates in the search;
- exceptional values have declared behavior.

In languages that express a strict ordering $<$, lower bound tests whether $A[mid]<x$ and upper bound tests whether $x<A[mid]$ is false or equivalently whether $A[mid]\le x$ under a total order. Equality used for membership should agree with ordering equivalence when the contract expects it.

Floating-point NaN is a warning case: ordinary comparisons with NaN do not create a conventional total order. Locale-sensitive strings can reorder after configuration changes. A comparator reading time, random state, or mutable external data may return inconsistent answers within one loop. The algorithm cannot repair a broken relation.

### Midpoint and endpoint arithmetic are part of correctness

In mathematical integers, $\lfloor(lo+hi)/2\rfloor$ is harmless. In a fixed-width signed type, $lo+hi$ may overflow even when both endpoints are valid. Prefer

$$
mid=lo+\left\lfloor\frac{hi-lo}{2}\right\rfloor
$$

when $0\le lo\le hi$ makes the difference representable. A language library may provide an overflow-safe midpoint primitive.

Endpoint conventions must remain uniform. With $[lo,hi)$:

- initialize $hi=n$;
- loop while $lo<hi$;
- every array read uses an index strictly below $hi\le n$;
- return values range from $0$ through $n$.

An inclusive interval $[lo,hi]$ can also be correct, but it has different initialization, emptiness, and update rules. Combining $hi=n$ from a half-open design with an inclusive read is an out-of-bounds defect. Combining $hi=mid$ with a loop that expects removal of $mid$ can fail to terminate.

### Random access and physical cost

Binary search makes $O(\log n)$ probes, but it assumes the middle element can be reached efficiently. In an array, index access is constant in the usual RAM model. In a singly linked list, finding each middle node by traversal can cost linear time, erasing the expected elapsed-time advantage even though the number of key comparisons remains logarithmic.

On modern storage, probes can be far apart. A linear scan has more comparisons but predictable sequential access, vectorization opportunities, and prefetching. For small arrays or expensive branch mispredictions, it can beat a branchy binary search. For disk or network pages, a higher-fanout search structure can reduce transfers better than binary partitioning of individual records.

Separate at least:

$$
\text{key comparisons},\quad
\text{key projections},\quad
\text{bytes touched},\quad
\text{random transfers},\quad
\text{elapsed time}.
$$

They are related by a machine/workload model, not equal by definition.

### Charge construction and updates

Suppose an unsorted collection of size $n$ receives $q$ membership queries. Scanning has modeled comparison cost

$$
C_{\mathrm{scan}}(n,q)=q\,n
$$

in the unsuccessful worst case. Sorting once and then searching has

$$
C_{\mathrm{sort+search}}(n,q)
=
S(n)+q\left\lceil\log_2(n+1)\right\rceil,
$$

where $S(n)$ is the actual construction cost being compared. Sorting becomes attractive only when the saved query work repays construction, storage, and maintenance under the real lifecycle.

Updates alter the decision. Inserting into a sorted array requires locating a boundary and shifting elements. A write-heavy workload may prefer a different index, batching, periodic rebuilding, or scans over small partitions. If a maintained index is stale, binary search can be fast and wrong.

Precomputation must also follow ownership. If many components reuse one already-required sorted representation, charging the full sort to every query is wrong. If the search feature alone demands the order, hiding construction as “free” is equally wrong.

### Treat concurrency as a snapshot premise

The proof assumes every comparison observes one sequence ordered under one relation. Concurrent insertion, deletion, reordering, or key mutation can violate that assumption between iterations. The result may become meaningless even if each individual read is memory-safe.

Choose an explicit consistency mechanism:

- an immutable snapshot;
- a read lock spanning the operation;
- a versioned structure with validation/retry;
- an index implementation whose documented concurrency contract provides a suitable view.

A lock around only the final equality read does not restore the interval proof. Likewise, a concurrent library's memory safety does not automatically imply snapshot-consistent search semantics.

### Use boundary primitives in executable code

The following deterministic implementation exposes lower and upper boundaries. Its output checks absence, duplicates, an interior gap, and the end sentinel.

<!-- bijux-verify: {"id":"search-boundaries","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"target=0 lower=0 upper=0 count=0 first=None\ntarget=2 lower=1 upper=4 count=3 first=1\ntarget=4 lower=4 upper=4 count=0 first=None\ntarget=10 lower=6 upper=6 count=0 first=None\n","stderr":""}} -->
~~~python
def partition_point(values, predicate):
    lo = 0
    hi = len(values)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if predicate(values[mid]):
            hi = mid
        else:
            lo = mid + 1
    return lo


values = (1, 2, 2, 2, 5, 9)
for target in (0, 2, 4, 10):
    lower = partition_point(values, lambda value: value >= target)
    upper = partition_point(values, lambda value: value > target)
    first = lower if lower < upper else None
    print(
        f"target={target} lower={lower} upper={upper} "
        f"count={upper - lower} first={first}"
    )
~~~

Passing arbitrary callbacks may add overhead in some languages; specialized library routines can preserve the same logical contract more efficiently. The important reusable object is the predicate/invariant pair, not this particular interface.

## Definitions and Notation

- $A[0:n]$ denotes a sequence with valid indices $0,\ldots,n-1$.
- $x$ is the query target; $k(a)$ is an optional key projection.
- $a\sim x$ means that element $a$ satisfies the contract's match relation with $x$.
- $[lo,hi)$ is a half-open interval with cardinality $hi-lo$.
- $P(i)$ is the decision predicate at index $i$; it must be monotone for partition search.
- $p$ is a partition point: the least true index, or $n$ when no stored index is true.
- $\operatorname{lower}(x)$ is the first index $i$ with $A[i]\ge x$.
- $\operatorname{upper}(x)$ is the first index $i$ with $A[i]>x$.
- An **insertion point** is a boundary at which inserting a value preserves the declared order.
- A **sentinel result** is a valid out-of-domain value such as $n$ used to encode a boundary or absence; it must not be read as an element index.
- A **strict weak ordering** groups equivalent elements while ordering the equivalence classes consistently; some language APIs use this weaker contract rather than a total order.
- A **snapshot** is the logically stable collection version to which all observations in one search belong.
- $S(n)$ denotes construction or sorting cost; $q$ denotes the number of queries sharing it.

For predecessor and successor APIs, inequalities must be explicit. “Predecessor” sometimes means greatest value strictly below $x$ and sometimes greatest value at most $x$. Under the non-strict convention, a predecessor index is $\operatorname{upper}(x)-1$ when upper bound is positive. Under the strict convention, it is $\operatorname{lower}(x)-1$ when lower bound is positive.

## Mechanisms, Invariants, or Proof Structure

Use the following search-design worksheet:

1. **Domain:** identify the collection, valid indices, snapshot, and mutation rules.
2. **Result contract:** choose membership, boundary, exact position, range, predecessor, successor, or count.
3. **Match relation:** define equality, tolerance, normalization, and duplicate semantics.
4. **Order relation:** define comparator/key, exceptional values, and whether equivalence classes are contiguous.
5. **Structural evidence:** establish unsorted enumeration, sorted random access, or another monotone domain.
6. **Predicate:** state $P(i)$ and prove its false-then-true shape.
7. **Interval convention:** choose half-open or inclusive bounds and use it everywhere.
8. **Invariant:** state what is rejected on the left, accepted on the right, and unresolved in the middle.
9. **Progress:** prove every branch strictly reduces a nonnegative integer variant.
10. **Postcondition:** derive the exact returned boundary or match from the termination state.
11. **Arithmetic:** validate midpoint, endpoint, index type, and sentinel operations.
12. **Representation cost:** account for access, key projection, transfer, cache, and comparator costs.
13. **Lifecycle:** charge construction, reuse, insertion, deletion, rebuilding, and staleness.
14. **Executable checks:** cover empty, singleton, boundaries, absence gaps, duplicates, and exceptional keys.
15. **Measurement:** collect modeled counters and physical metrics without replacing proof.
16. **API translation:** verify the chosen library's duplicate, insertion, comparator, and concurrency semantics.

The proof skeleton for lower bound is:

**Precondition.** $A[0:n]$ is stable and sorted under the declared relation, which makes $P(i)\equiv A[i]\ge x$ monotone.

**Initialization.** With $lo=0$ and $hi=n$, there is no stored index left of $lo$ or at/after $hi$, so both excluded-region statements are vacuously true.

**Preservation.** If $P(mid)$ is false, monotonicity rejects every index at most $mid$; if true, it accepts every index at least $mid$. The corresponding update retains every possible partition point.

**Progress.** Since $lo\le mid<hi$, either $mid+1-lo>0$ candidates are removed or $hi-mid>0$ candidates are removed. Thus $hi-lo$ strictly decreases.

**Termination.** A decreasing nonnegative integer reaches zero, so $lo=hi$.

**Postcondition.** All indices below $lo$ are false and all stored indices from $lo$ onward are true. Therefore $lo$ is the least true index, with $n$ representing no true stored index.

For linear first-match search, replace the partition invariant with a rejected-prefix invariant. This contrast is the conceptual core: linear search earns progress by checking one candidate; binary search earns geometric progress only from a monotonicity proof.

## Alternatives and Trade-Offs

**Linear scan versus binary search.** A scan has weak preconditions, sequential locality, and no construction requirement. Binary search reduces comparisons on a stable ordered random-access domain. Small $n$, early matches, expensive setup, or cache effects can favor scanning.

**Arbitrary match versus boundary search.** An equality-exit loop can return sooner for a unique hit. Boundary search gives deterministic duplicate semantics, useful absence positions, and composable ranges. Choose from the API contract, not habit.

**Lower/upper bound versus two-sided expansion.** Finding one duplicate and scanning outward is simple but can take $\Theta(n)$ when many values are equal. Two boundary searches remain $O(\log n)$ comparisons.

**Sort once versus scan repeatedly.** Sorting adds $S(n)$ construction and may change record order. It pays only across sufficient reuse and compatible update rates. Preserve original order or identities when those are contract data.

**Sorted array versus search tree or hash index.** Arrays are compact and cache-friendly but costly to update. Balanced trees support ordered dynamic operations; hash indexes target expected membership rather than predecessor/range order. Data Structures Engineering owns their implementations.

**Branching versus branch-reduced implementations.** Conventional binary search is transparent and portable. Branchless, uniform, interpolation, exponential, or layout-specialized searches may improve a measured regime while increasing premises and maintenance. Preserve the boundary contract and validate on representative machines.

**Precomputed keys versus repeated projection.** Storing keys can avoid expensive normalization or extraction during comparisons, at the cost of memory and synchronization. A stale key array destroys correspondence with the records.

**One snapshot versus optimistic retry.** Locking or immutable snapshots simplify the proof but may affect concurrency. Version validation can reduce blocking, yet the search must retry if the compared view changes.

**Hand-written loop versus standard library.** A mature library reduces endpoint risk and may be optimized. It does not choose the right contract for you. Verify whether duplicates yield an arbitrary match, left/right insertion point, or an unspecified position.

## Failure Modes and Misconceptions

1. **“Binary search means look for equality at the midpoint.”** The durable primitive finds a monotone partition boundary.
2. **“Sorted somewhere is enough.”** The sequence must be sorted under the same current relation and key.
3. **“Any duplicate is as good as the first.”** Only if the result contract says so.
4. **“If the target is absent, binary search failed.”** A boundary result still identifies its ordered insertion gap.
5. **“Return $n$ and then read $A[n]$.”** The sentinel is not a stored index; guard it first.
6. **“Set $lo=mid$ after a false test.”** When $mid=lo$, this may make no progress and loop forever.
7. **“Set $hi=mid-1$ in a half-open lower-bound loop.”** This can discard the true boundary and mixes conventions.
8. **“$(lo+hi)//2$ is universally safe.”** Fixed-width addition can overflow.
9. **“$O(\log n)$ comparisons means $O(\log n)$ time everywhere.”** Accessing the middle or computing a key can dominate.
10. **“A linked list benefits from ordinary binary search.”** Repeated middle traversal can cost linear total time or worse in a naive implementation.
11. **“Sorting is free because the query is logarithmic.”** Construction and maintenance belong to lifecycle cost.
12. **“Insertion after binary search is logarithmic.”** Array movement is still linear in the worst case.
13. **“A comparator may change as long as individual calls work.”** Inconsistent decisions invalidate monotonicity.
14. **“NaN behaves like an ordinary ordered number.”** Standard floating comparisons do not supply the required total order.
15. **“One test on a present target validates the loop.”** Empty, absent, duplicates, endpoints, and sentinel results expose different defects.
16. **“A passing timing curve proves correctness.”** Measurement cannot prove the interval invariant for all admitted inputs.
17. **“A concurrent container makes a multi-read search coherent.”** Memory safety and snapshot consistency are different guarantees.
18. **“Library duplicate behavior is obvious.”** Some APIs return any match; others return a specific insertion boundary.
19. **“A predicate that is usually monotone is safe.”** One false-true-false pattern can make elimination unsound.
20. **“Binary search is always faster.”** Constants, locality, $n$, workload distribution, and setup determine the finite result.

## Worked Examples

### Example 1

**Question:** Find the first occurrence of $7$ in $A=(7,7,9)$ by linear search.

**Reasoning:** Start at $i=0$. The rejected prefix $[0,0)$ is empty. The first comparison already satisfies $A[0]=7$, so the loop exits without rejecting index $0$. Returning any later equal index would violate the first-match contract.

**Conclusion:** The result is index $0$ after one target comparison; first-match semantics depend on traversal order.

### Example 2

**Question:** What does lower bound return on an empty sequence?

**Reasoning:** Initialize $lo=hi=0$. The loop condition $lo<hi$ is false. The partition facts are vacuous, and $0=n$ is the sentinel for “no stored true position” as well as the only insertion gap.

**Conclusion:** Return $0$ without reading an element; emptiness needs no special algorithm branch.

### Example 3

**Question:** Trace lower bound for $x=6$ in $A=(1,3,5,7,9)$.

**Reasoning:** Start $[0,5)$. At $mid=2$, $A[2]=5<6$, so reject through index $2$ and set $lo=3$. Now $[3,5)$; $mid=4$ gives $9\ge6$, so $hi=4$. Now $[3,4)$; $mid=3$ gives $7\ge6$, so $hi=3$. Termination returns $3$.

**Conclusion:** Absence is represented by insertion boundary $3$, between values $5$ and $7$.

### Example 4

**Question:** Derive all duplicate results for $x=2$ in $A=(1,2,2,2,5,9)$.

**Reasoning:** Lower bound with predicate $A[i]\ge2$ returns $1$. Upper bound with predicate $A[i]>2$ returns $4$. The equal range is $[1,4)$, its size is $3$, its first index is $1$, and its last index is $4-1=3$.

**Conclusion:** Two partition boundaries answer membership, count, first, last, and range contracts deterministically.

### Example 5

**Question:** Why can the update $lo=mid$ fail in a half-open loop?

**Reasoning:** Let $lo=0$ and $hi=1$. Then $mid=0$. If the predicate is false and the loop assigns $lo=mid$, the state remains $[0,1)$. The variant $hi-lo$ stays $1$, so the same comparison repeats forever.

**Conclusion:** A disproved midpoint must be removed with $lo=mid+1$; strict progress is a correctness obligation.

### Example 6

**Question:** How many lower-bound iterations are needed in the worst case for $n=1000$?

**Reasoning:** The exact maximum is

$$
\left\lceil\log_2(1001)\right\rceil.
$$

Because $2^9=512<1001\le1024=2^{10}$, the ceiling is $10$. An unsuccessful linear scan would make $1000$ target comparisons.

**Conclusion:** Ordered partition search needs at most $10$ predicate tests, excluding construction and final equality.

### Example 7

**Question:** An array is sorted by lowercase username, but a query compares original case-sensitive strings. Is binary search valid?

**Reasoning:** The stored order may place “alice” and “Bob” according to normalized keys, while case-sensitive comparison orders their source strings differently. Thus the query predicate need not be false-then-true across the stored sequence. A locally correct loop cannot recover monotonicity.

**Conclusion:** Search with the same normalization/key used to establish order, or rebuild an index for the new relation.

### Example 8

**Question:** Should 20 keys be sorted before one membership query?

**Reasoning:** A worst-case scan uses $20$ comparisons. Sorting comparison cost is on the order of $20\log_2 20$ plus movement, followed by about $5$ search comparisons. Unless ordering is already required or reused, construction costs more than the single saved scan.

**Conclusion:** For one small unsorted query, linear search is normally the better lifecycle choice despite its larger asymptotic query bound.

### Example 9

**Question:** Can binary search find the smallest integer capacity $c$ that schedules a workload before a deadline?

**Reasoning:** Define $P(c)$ as “the scheduler succeeds by the deadline at capacity $c$.” Binary search is sound only if success at $c$ implies success at every larger admitted capacity. Resource contention, discrete policy changes, or a nonmonotone heuristic could violate this. Establish bounds with a false lower sentinel and true upper sentinel, then use partition search.

**Conclusion:** Binary search applies to the answer space only after feasibility monotonicity and sentinel bounds are proved.

### Example 10

**Question:** A sorted catalog is updated concurrently while a search reads it. Every read is memory-safe. Is the returned boundary valid?

**Reasoning:** One iteration may compare an old value at a high index and a later iteration a shifted new value at a low index. Those facts need not describe any single sorted snapshot, so the excluded regions cannot be combined into one proof. Memory safety prevents invalid access, not logical time travel.

**Conclusion:** Use an immutable/read-locked snapshot or a versioned validation-and-retry protocol whose semantics preserve the search premise.

## Cross-Program Connections

- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) owns dynamic ordered indexes, balanced trees, skip lists, hash tables, and their storage/update invariants.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) owns cache lines, prefetching, branches, SIMD, and memory-latency mechanisms that shape scan/search constants.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) owns virtual-memory, file-mapping, synchronization, and page-fault behavior beneath large searches.
- [Concurrent & Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) owns memory models, snapshots, locks, atomics, and data-race semantics.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) owns persistent indexes, query operators, collation, transactions, and range-query planning.
- [API & Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) owns pagination, versioning, error contracts, and externally visible duplicate/boundary semantics.
- [Programming Languages & Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) owns integer overflow, evaluation semantics, comparator interfaces, and partial/total result types.

## References

1. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. [*Introduction to Algorithms*, fourth edition](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), MIT Press, 2022. Search correctness, loop invariants, comparison analysis, and algorithm engineering foundations.
2. Donald E. Knuth. [*The Art of Computer Programming, Volume 3: Sorting and Searching*, second edition](https://www.informit.com/store/art-of-computer-programming-volume-3-sorting-and-searching-9780321635785), Addison-Wesley Professional, 1998. Foundational treatment and analysis of sequential and binary searching.
3. Jon Bentley. [*Programming Pearls*, second edition](https://www.informit.com/store/programming-pearls-9780201657883), Addison-Wesley Professional, 2000. Search specification, invariants, boundary reasoning, and implementation discipline.
4. Robert Sedgewick and Kevin Wayne. [*Algorithms*, fourth edition and companion site](https://algs4.cs.princeton.edu/home/), Addison-Wesley, 2011. Search, sorting, cost models, executable examples, and empirical comparison.
5. Python Software Foundation. [“bisect — Array bisection algorithm”](https://docs.python.org/3/library/bisect.html), Python 3 standard-library documentation, checked 2026-09-04. Current insertion-point, key-projection, performance, and thread-safety semantics.
6. The Rust Project Developers. [“Primitive Type slice”](https://doc.rust-lang.org/stable/std/primitive.slice.html), stable standard-library documentation, checked 2026-09-04. Current binary-search, arbitrary-duplicate, insertion-index, and partition-point contracts.
7. Joshua Bloch. [“Extra, Extra—Read All About It: Nearly All Binary Searches and Mergesorts Are Broken”](https://research.google/blog/extra-extra-read-all-about-it-nearly-all-binary-searches-and-mergesorts-are-broken/), Google Research, 2006. Historical engineering account of fixed-width midpoint overflow.
8. ACM, IEEE Computer Society, and AAAI. [*Computer Science Curricula 2023: Algorithmic Foundations*](https://csed.acm.org/al-cs-core/), endorsed 2024; consulted 2026-09-04. Current curricular scope for sequential/binary search, correctness, empirical analysis, and implementation trade-offs.

## Exercises

### Exercise 1

For $A=(1,1,3,3,3,8)$, give lower bound, upper bound, equal range, first match, last match, and count for targets $3$ and $4$. Identify every sentinel that must be guarded before indexing.

### Exercise 2

Prove the lower-bound loop correct using the invariant

$$
\forall i<lo,\ A[i]<x,
\qquad
\forall i\ge hi,\ A[i]\ge x.
$$

Show initialization, preservation for both branches, strict progress, termination, and the returned postcondition.

### Exercise 3

Diagnose this half-open implementation:

<!-- bijux-verify: {"id":"defective-search-exercise","mode":"schematic","language":"python","toolchain":"none","reason":"the intentionally defective pseudocode is analyzed rather than executed"} -->
~~~python
lo = 0
hi = len(values)
while lo <= hi:
    mid = (lo + hi) // 2
    if values[mid] < target:
        lo = mid
    else:
        hi = mid - 1
return lo
~~~

List the endpoint, access, progress, overflow, and postcondition defects, then state corrected lower-bound updates.

### Exercise 4

An unsorted immutable array of $n=1{,}000{,}000$ records will receive $q$ unsuccessful membership queries. Model one scan as $n$ comparisons, sorting as $25n\log_2 n$ primitive-cost units, and each binary search as $8\lceil\log_2(n+1)\rceil$ units. Ignoring storage and movement beyond the supplied coefficients, find the smallest integer $q$ for which sort-plus-search has lower modeled cost than repeated scanning. Explain why this calculation is not yet a deployment decision.

### Exercise 5

A service stores versioned price rules sorted by $(product,\ valid\_from)$. Queries ask for the rule active at timestamp $t$, duplicate timestamps are possible, updates arrive concurrently, key normalization can change between releases, and most product partitions contain fewer than 16 rules. Design the result contract, boundary search, snapshot rule, duplicate policy, testing strategy, lifecycle comparison, and measurements needed to choose between scanning each partition and binary search.

## Answers to the Exercises

### Answer 1

For target $3$, lower bound is $2$ and upper bound is $5$. The equal range is $[2,5)$, first match is $2$, last match is $4$, and count is $5-2=3$.

For target $4$, both lower and upper bounds are $5$, so the equal range is $[5,5)$ and count is zero. There is no first or last match. Index $5$ itself is valid to read here but contains $8$, not $4$.

In general, either boundary may equal $n=6$, especially for a target greater than $8$. Guard a lower-bound result with $p<n$ before reading $A[p]$. Guard upper-bound minus one with $upper>0$ before reading it. A nonempty equal range is established by $lower<upper$.

### Answer 2

Initially $lo=0$ and $hi=n$. There is no valid index below $0$ and no valid stored index at least $n$, so both quantified statements hold vacuously; also $0\le lo\le hi\le n$.

With $lo<hi$, choose $mid=lo+\lfloor(hi-lo)/2\rfloor$, giving $lo\le mid<hi$. If $A[mid]<x$, sortedness implies $A[i]<x$ for every $i\le mid$. Setting $lo=mid+1$ therefore preserves the rejected-left statement and does not change the accepted-right statement. Otherwise $A[mid]\ge x$, and sortedness implies $A[i]\ge x$ for every $i\ge mid$. Setting $hi=mid$ preserves the accepted-right statement and does not change the rejected-left statement.

In the false branch the new interval length is $hi-(mid+1)<hi-lo$. In the true branch it is $mid-lo<hi-lo$. Thus the nonnegative integer $hi-lo$ strictly decreases, proving termination.

At termination $lo=hi$. The invariant says every earlier index contains a value less than $x$ and every stored index at or after $lo$ contains a value at least $x$. Hence $lo$ is exactly the least qualifying index, or $n$ if none exists.

### Answer 3

The code initializes a half-open interval but loops with the inclusive condition $lo\le hi$. When $lo=hi=n$, it reads $values[n]$ out of bounds. The false branch uses $lo=mid$; when $mid=lo$, no progress occurs. The true branch uses $hi=mid-1$, discarding $mid$ even though it may be the first qualifying index and potentially making $hi<lo$. The midpoint addition can overflow in a fixed-width type. No coherent invariant supports the returned $lo$ after these mixed updates.

For half-open lower bound, use:

- loop condition $lo<hi$;
- midpoint $lo+(hi-lo)//2$;
- if $values[mid]<target$, set $lo=mid+1$;
- otherwise set $hi=mid$;
- return $lo$ in $0,\ldots,n$ and guard the sentinel before indexing.

### Answer 4

Here

$$
\log_2(1{,}000{,}000)\approx19.9316
$$

and

$$
\left\lceil\log_2(1{,}000{,}001)\right\rceil=20.
$$

Repeated scanning costs

$$
C_{\mathrm{scan}}=1{,}000{,}000q.
$$

Sort-plus-search costs

$$
C_{\mathrm{sorted}}
=25(1{,}000{,}000)(19.9316)+8q(20)
\approx498{,}289{,}214+160q.
$$

Require $C_{\mathrm{sorted}}<C_{\mathrm{scan}}$:

$$
498{,}289{,}214+160q<1{,}000{,}000q,
$$

so

$$
q>\frac{498{,}289{,}214}{999{,}840}\approx498.369.
$$

The smallest integer is $q=499$. This is only a supplied cost-model result. A deployment decision still needs construction/movement time, memory, updates, successful-query positions, key cost, locality, latency, concurrency, reuse ownership, and measured workload evidence.

### Answer 5

Define the result as the rule with the greatest $valid\_from\le t$ within exactly one normalized product partition, plus an explicit absence result. Specify whether duplicate timestamps are invalid, use a deterministic sequence/version priority, or require the last rule under a stable composite key. Do not let an arbitrary duplicate decide price.

For a partition sorted by $(normalized\_product,valid\_from,tiebreaker)$, first isolate the product's half-open range. Within it, compute upper bound of $t$ under the timestamp/tiebreak contract, then use the preceding element if one exists. A strict-predecessor policy would use lower bound instead. Validate effective-end times or next-rule boundaries separately.

Each query must observe an immutable version, a read lock, or a version token checked after the search with retry on change. The index and query must share the same normalization version; a release that changes normalization requires rebuilding/versioning the index before it serves matching queries.

Tests cover empty products, one rule, before-first/at-first/between/at-last/after-last times, duplicate timestamps, normalization collisions, invalid intervals, concurrent update schedules, stale versions, and retry exhaustion. Differentially compare scan and boundary implementations against an independent specification on generated histories.

For partitions below 16 elements, benchmark both implementations on representative key costs and cache states after correctness is established. Count comparisons and projections; measure cold/warm latency, tail latency, update/rebuild cost, snapshot/retry overhead, and memory. Include the cost of maintaining sorted partitions and the distribution of partition sizes and query timestamps. Choose scanning if its simpler sequential path wins the bounded workload; choose binary search only where its reduced comparisons repay added invariants and maintenance.
