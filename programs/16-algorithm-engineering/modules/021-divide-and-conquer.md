---
module_id: ALGE-021
program: Algorithm Engineering
level: 1
module_number: 21
title: Divide and Conquer
status: complete
last_verified: 2026-09-04
---

# Divide and Conquer

## One-Page Review

### Governing question

How can a problem be decomposed into strictly smaller, sufficiently independent subproblems whose returned summaries support a correct and efficient reconstruction of the whole answer?

### Essential definitions

- **Divide and conquer** divides one instance into smaller instances, solves them recursively, and combines their results.
- The **divide step** constructs subproblem inputs and any boundary metadata.
- The **conquer step** solves each smaller subproblem under the same or a compatible contract.
- The **combine step** reconstructs a solution or summary for the parent instance.
- A **well-founded measure** strictly decreases on every recursive edge and proves termination.
- A **separator** limits how solutions in different subproblems can interact.
- A **sufficient summary** retains exactly the child information required by every parent combine.
- **Balance** describes how subproblem sizes compare; it affects depth but does not alone prove efficiency.
- A **base-case cutoff** replaces recursion below a chosen size with a direct algorithm.
- **Work** counts all operations, while **span** counts the longest dependency path under an ideal parallel schedule.

### Central model, mechanism, or theorem

For instance $x$, let division produce children $x_1,\ldots,x_k$ and metadata $m$. A complete design specifies

$$
(x_1,\ldots,x_k,m)=D(x),
\qquad
y=C\bigl(x,m,S(x_1),\ldots,S(x_k)\bigr),
$$

where every child has smaller well-founded measure. Correctness follows when:

1. division preserves the information required by the specification;
2. the induction hypothesis makes each child result sound and complete for its child;
3. combine is sound—every returned parent result is valid;
4. combine is complete—no globally optimal or required result is omitted.

For size bounds $n_i<n$, work has the structural recurrence

$$
W(n)\le\sum_i W(n_i)+W_D(n)+W_C(n).
$$

If children can run in parallel, span follows the longest child rather than their sum:

$$
S_p(n)\le\max_i S_p(n_i)+S_{p,D}(n)+S_{p,C}(n).
$$

The recurrences must be derived from the actual interface, execution order, and resource being analyzed.

### Critical invariants

- Every recursive child satisfies the algorithm's input preconditions.
- Every recursive edge strictly decreases a declared well-founded measure.
- Child ranges or identities have explicit coverage, overlap, and ownership rules.
- Boundary interactions omitted from children are represented in metadata or combine logic.
- Child summaries retain all information required for a complete parent answer.
- Tie-breaking, stability, coordinate systems, and numeric semantics agree at every level.
- Work, span, peak space, I/O, and communication are analyzed separately.
- Midpoints and derived offsets use overflow-safe arithmetic and consistent half-open ranges.
- Parallel children do not race on mutable state, shared scratch space, or publication.
- Cutoffs preserve the same result contract and are justified by measurements rather than folklore.

### Common failures

Common failures include splitting without a complete combine; assuming child optima automatically form a parent optimum; overlooking cross-boundary candidates; recursing on an unchanged instance; confusing divide-and-conquer with overlapping dynamic programming; inserting a sort at every recursive level and creating an extra logarithmic factor; using balanced-looking syntax when data-dependent partitions are unbalanced; solving the wrong recurrence; summing child spans that run concurrently; summing sibling memory that is never simultaneously live; copying slices at every level; overflowing midpoint arithmetic; changing tie-breaking at the cutoff; spawning tasks below useful grain size; and reporting a cache or parallel theorem under unstated machine assumptions.

### Compact example

For values

$$
(4,-1,2,1,-7,5,2,-1,3,-10,4),
$$

return from each range its total plus its best prefix, suffix, and subarray, all with deterministic intervals. Two adjacent summaries combine in constant work. The root finds maximum subarray $[5,9)$ with sum $9$ and values $(5,2,-1,3)$. For a balanced tree,

$$
W(n)=2W(n/2)+\Theta(1)=\Theta(n),
$$

while parallel span with constant-time combine is $\Theta(\log n)$. The stronger summary avoids rescanning the crossing range at each level.

### Connections

[ALGE-004](./004-inductive-correctness-proofs.md) supplies strong induction and descent, [ALGE-007](./007-recurrences-and-the-master-method.md) supplies recurrence analysis, [ALGE-011](./011-linear-and-binary-search.md) supplies one-child localization, [ALGE-013](./013-merge-sort.md) supplies two-child merging, and [ALGE-014](./014-quicksort-and-partitioning.md) supplies data-dependent partitioning.

## Governing Question

What information must cross a recursive boundary so that independently solved pieces can be recombined into the exact global result, and when does that decomposition improve time, space, locality, or parallelism?

“Split it in half” is not a design proof. The important work is discovering a separator and a child interface. A useful separator makes most of the problem local. A sufficient summary captures the remaining interaction compactly. Correctness requires showing that every global answer is represented by local answers, cross-boundary candidates, or both.

Efficiency is equally structural. Reducing four half-size multiplications to three changes an exponent. Preserving a secondary ordering through recursive geometry avoids a sort at every level. Returning richer constant-size summaries can turn a linear combine into a constant combine. Conversely, perfect balance can still be slow if division or combination repeats expensive work.

## Why This Matters

Divide and conquer underlies binary search, merge sort, quicksort, selection, large-integer multiplication, matrix multiplication, Fourier transforms, geometric algorithms, parallel reductions, cache-oblivious layouts, and many tree algorithms. It is also a disciplined way to design interfaces: children own smaller regions, and parents reconcile precisely defined boundaries.

The paradigm exposes opportunities beyond sequential time. Independent children can execute concurrently. Recursive blocking can improve locality across unknown cache sizes. Subproblem ownership can limit failure and memory scope. These advantages appear only when the combine dependency, scratch-space liveness, grain size, and publication semantics are designed explicitly.

It also supplies diagnostic power. If subproblems overlap substantially, memoized dynamic programming may be the right paradigm. If only one child is followed, the design is decrease-and-conquer. If the hard part is replacing the representation before solving, transform-and-conquer may be clearer. Naming the structure accurately leads to better proofs and implementations.

## Prerequisites and Retrieval

Retrieve:

- mathematical functions, sequences, induction, invariants, and well-founded orderings;
- asymptotic notation, geometric sums, logarithms, and recurrence methods;
- half-open ranges, arrays, slices, views, buffers, pointers, and integer overflow;
- sorting, binary search, partitioning, stable merging, and selection;
- algebraic expansion, polynomial multiplication, and matrix blocks;
- Euclidean distance, planar coordinates, packing arguments, and lexicographic ties;
- tasks, dependency DAGs, work, span, synchronization, cancellation, and memory liveness;
- caches, blocks, locality, I/O, benchmarking, counters, and property testing.

You should be able to prove a recursive routine correct by strong induction and derive separate work and peak-space recurrences from code.

## Learning Objectives

After completing this module, you should be able to:

1. recognize when a separator makes divide and conquer appropriate;
2. specify divide, child, summary, combine, and base-case contracts;
3. prove termination, soundness, completeness, identity, and deterministic ties;
4. derive work, span, space, I/O, and communication recurrences from implementation structure;
5. explain how balance, branching, and combine cost interact;
6. redesign child summaries to eliminate repeated combine work;
7. derive Karatsuba and Strassen-style reductions in recursive suboperations;
8. preserve secondary order, ownership, and scratch-space invariants;
9. choose cutoffs and parallel grain sizes from reproducible evidence;
10. validate a divide-and-conquer implementation across boundaries, adversaries, and target machines.

## Core Exposition

### Recognize a useful separator

A promising instance has a separator with three properties:

1. it partitions most work into strictly smaller regions;
2. interactions across regions have limited, characterizable structure;
3. child answers or summaries can represent everything the parent needs.

For sorted search, comparing the middle key localizes any possible match to at most one half. For merge sort, the separator creates two independent ordering problems, and a linear merge reconciles their boundary. For planar closest pair, a vertical split localizes pairs except those close enough to the split line; a geometric packing argument limits the cross-strip candidates after secondary order is preserved.

Do not begin with recursion syntax. Begin with the global specification. Classify every possible valid or optimal answer by where its constituent identities lie. If a class crosses the separator, define exactly how combine enumerates or summarizes it.

### Distinguish neighboring paradigms

Divide and conquer usually creates multiple independent or nearly independent smaller instances. Related shapes deserve different names:

- **decrease and conquer:** solve one smaller instance and extend or localize, as in binary search;
- **dynamic programming:** solve overlapping subproblems and reuse their results;
- **transform and conquer:** change representation or preprocess, then solve an easier instance;
- **meet in the middle:** enumerate summaries of two large halves and match them, often trading exponential time for space;
- **backtracking:** explore a decision tree whose children represent choices, often with pruning;
- **branch and bound:** explore choices while bounding whether a subtree can improve the incumbent.

An algorithm may combine paradigms. Quicksort divides by a partition and recursively sorts both sides; its pivot selection can use randomized or selection techniques. A clear account names which proof and cost belong to each component.

### Write the recursive interface first

Specify a function over a domain such as

$$
S(x,lo,hi,\sigma)\to r,

$$

where $[lo,hi)$ is a half-open region, $\sigma$ is read-only context or scratch ownership, and $r$ is a declared summary. State:

- preconditions on representation, ordering, uniqueness, and numeric domain;
- the well-founded measure, often $hi-lo$;
- base cases and their exact results;
- child ranges and whether they cover, overlap, or omit boundary elements;
- metadata created by division;
- summary fields and coordinate system;
- combine's tie-breaking and mutation rules;
- errors, cancellation points, and publication behavior.

Half-open ranges make size $hi-lo$, empty ranges $lo=hi$, and adjacency $[lo,mid)$ followed by $[mid,hi)$ explicit. Compute the midpoint as

$$
mid=lo+\left\lfloor\frac{hi-lo}{2}\right\rfloor
$$

after verifying $0\le lo\le hi$ in a numeric type where the difference is representable. The familiar $(lo+hi)/2$ can overflow fixed-width arithmetic.

### Prove termination before optimality

Choose a measure $\mu(x)$ in a well-founded set. For every recursive child $x_i$, prove

$$
\mu(x_i)<\mu(x).
$$

For half-open array ranges, $\mu=hi-lo$ works when every non-base split satisfies $lo<mid<hi$. A partition routine that returns the original range on all-equal input can violate descent unless it removes an equal region or advances boundaries.

Termination also includes retry and failure paths. A recursive task that retries a failed child indefinitely has no finite descent argument merely because its data range is smaller. Bound retries or give a separate liveness premise.

### Prove combine soundness and completeness

Use strong induction on the measure. Assume every smaller legal instance returns a result satisfying its contract. Then prove four parent obligations:

1. **division validity:** every child meets preconditions and all metadata is correct;
2. **child coverage:** the set of global candidates is partitioned or covered by named child and boundary classes;
3. **combine soundness:** every candidate selected or constructed by combine is valid for the parent;
4. **combine completeness:** a globally required or optimal candidate appears in at least one examined class.

For an optimization problem with candidate classes $\mathcal C_1,\ldots,\mathcal C_t$, if children return each class optimum and combine returns their best under one deterministic order, then

$$
\operatorname{opt}\left(\bigcup_{j=1}^{t}\mathcal C_j\right)
=
\operatorname{best}\left(
\operatorname{opt}(\mathcal C_1),\ldots,
\operatorname{opt}(\mathcal C_t)
\right).
$$

This equation is useful only after proving the classes cover every parent candidate. “Take the better child” fails whenever an optimum can cross the separator.

### Derive recurrences from the interface

If division creates children of sizes $n_1,\ldots,n_k$, a worst-case work inequality is

$$
W(n)
\le
\max_{\text{legal splits}}
\left(
\sum_{i=1}^{k}W(n_i)+W_D(n)+W_C(n)
\right).
$$

Balanced fixed branching may simplify to

$$
W(n)=aW(n/b)+f(n).
$$

[ALGE-007](./007-recurrences-and-the-master-method.md) owns the Master theorem, substitution, recursion trees, Akra–Bazzi, rounding, and method selection. Here the essential lesson is correspondence: $a$, $b$, and $f$ come from executed children and real divide/combine work.

Balance controls depth and leaf distribution. Combine cost controls how much work repeats at each level. With two halves:

$$
2W(n/2)+\Theta(1)=\Theta(n),
$$

$$
2W(n/2)+\Theta(n)=\Theta(n\log n),
$$

and

$$
2W(n/2)+\Theta(n^2)=\Theta(n^2).
$$

Reducing branching can change the exponent. Improving combine can remove a logarithmic factor. Both are design achievements, not algebra afterthoughts.

### Localize to one child when the specification permits

Binary search compares a query with a middle key. Sorted order proves that at most one side can contain an equal key. Its work recurrence is

$$
W(n)=W(\lceil n/2\rceil)+\Theta(1)=\Theta(\log n).
$$

A one-dimensional peak finder can similarly follow a higher neighbor into one half, but its correctness argument is different: the chosen direction guarantees that a peak exists before the boundary, not that a fixed target lies there.

Calling both halves would preserve correctness for some specifications but waste the localization theorem. Returning after the first child without the theorem can lose answers.

### Merge independent child solutions

Merge sort divides an array into adjacent ranges. The induction hypothesis orders each range, while combine repeatedly selects the smaller front. The child identity sets are disjoint and cover the parent, so merge preserves permutation. Taking the left front on equivalence provides stability.

The work recurrence is

$$
W(n)=W(\lfloor n/2\rfloor)+W(\lceil n/2\rceil)+\Theta(n)
=\Theta(n\log n).
$$

The same structure can count inversions. Child calls count within-half inversions. During merge, whenever a right key precedes the current left key, every remaining left key forms a cross inversion. This combine both orders the range and accounts for the omitted candidate class in linear time.

Preserving the merged order in the return type is what lets every ancestor combine stay linear. Returning only an inversion count would be an insufficient summary.

### Strengthen summaries to reduce combine work

For maximum nonempty subarray, a textbook design can recursively find the best left and right subarrays, then scan outward from the midpoint for the best crossing interval. That gives

$$
W(n)=2W(n/2)+\Theta(n)=\Theta(n\log n).
$$

Instead return four fields for each range:

- total sum;
- best prefix with interval;
- best suffix with interval;
- best subarray with interval.

For adjacent summaries $L$ and $R$:

$$
total=L.total+R.total,
$$

$$
prefix=\operatorname{best}(L.prefix,L.total+R.prefix),
$$

$$
suffix=\operatorname{best}(R.suffix,L.suffix+R.total),
$$

and

$$
best=\operatorname{best}(L.best,R.best,L.suffix+R.prefix).
$$

With intervals and one deterministic tie rule, combine takes constant work. Thus

$$
W(n)=2W(n/2)+\Theta(1)=\Theta(n).
$$

The summary is also associative when its interval coordinates and tie order are defined consistently, enabling reductions and segment trees. This illustrates a general tactic: move reusable boundary information into the child contract.

### Reduce recursive algebraic suboperations

Let base-$B$ integers be split near half their digits:

$$
x=x_1B^m+x_0,
\qquad
y=y_1B^m+y_0.
$$

Schoolbook block multiplication needs four half-size products. Karatsuba computes

$$
z_2=x_1y_1,
\qquad
z_0=x_0y_0,
$$

$$
z_1=(x_1+x_0)(y_1+y_0)-z_2-z_0,
$$

then reconstructs

$$
xy=z_2B^{2m}+z_1B^m+z_0.
$$

The algebra proves exactness, while the recurrence

$$
W(n)=3W(n/2)+\Theta(n)
=\Theta\left(n^{\log_2 3}\right)
$$

improves on quadratic digit work asymptotically. Carries, signed intermediates, uneven lengths, allocation, and cutoff arithmetic remain implementation obligations.

Strassen's matrix method applies a related idea to $2\times2$ block matrices: seven recursive block multiplications plus additions replace eight multiplications, yielding

$$
W(n)=7W(n/2)+\Theta(n^2)
=\Theta\left(n^{\log_2 7}\right),
$$

where $\log_2 7\approx2.807$. Numerical stability, extra additions, workspace, padding, sparsity, and tuned kernels determine when the method is useful; the exponent is not a universal crossover claim.

### Preserve secondary order in geometric divide and conquer

For planar closest pair, presort points by $x$ and maintain a $y$-ordered view through recursion. Divide into left and right identity sets, solve each, and let

$$
d=\min(d_L,d_R).
$$

Only points within horizontal distance $d$ of the vertical separator can form a better cross pair. In $y$ order, a packing argument bounds how many subsequent strip points require comparison for each point. A stable linear partition of the $y$ order and a linear combine produce

$$
W(n)=2W(n/2)+\Theta(n)=\Theta(n\log n)
$$

after one initial sort.

Sorting the strip from scratch at every call can create $\Theta(n\log^2 n)$ work. Partitioning by coordinate alone can mishandle equal-$x$ points; child membership must follow identity assignments. Duplicate coordinates imply distance zero and need deterministic pair ties and safe squared-distance arithmetic.

### Separate work, span, and available parallelism

For independent child tasks,

$$
W(n)=\sum_i W(n_i)+W_D(n)+W_C(n),
$$

but ideal span is

$$
S_p(n)=\max_i S_p(n_i)+S_{p,D}(n)+S_{p,C}(n).
$$

Average parallelism is bounded by

$$
\frac{W(n)}{S(n)}.
$$

Two parallel merge-sort children do not by themselves create logarithmic span if combine is a sequential $\Theta(n)$ merge:

$$
S_p(n)=S_p(n/2)+\Theta(n)=\Theta(n).
$$

With a correct parallel merge of $\Theta(\log n)$ span, a simplified recurrence becomes

$$
S_p(n)=S_p(n/2)+\Theta(\log n)=\Theta(\log^2 n).
$$

These are algorithm-DAG bounds, not promises about wall time. Scheduler overhead, processors, bandwidth, contention, NUMA placement, and grain size matter. Spawn only when predicted useful work exceeds a measured threshold, and retain a sequential path.

### Model peak live space rather than allocations summed over time

Space depends on ownership and execution order. Sequential sibling calls can reuse workspace:

$$
M(n)=\max(M(n_1),M(n_2))+M_{local}(n).
$$

If $M_{local}(n)=\Theta(n)$ and child size halves, then

$$
M(n)=M(n/2)+\Theta(n)=\Theta(n).
$$

Parallel siblings may coexist, changing the recurrence. A parent that retains its full buffer while both children allocate separate buffers can require much more peak memory than a schedule that partitions one shared arena.

Track stack frames, descriptors, retained inputs, output buffers, temporary algebraic blocks, allocator metadata, and cancellation cleanup. “$O(\log n)$ recursion depth” does not imply $O(\log n)$ auxiliary bytes when each level retains data.

### Engineer views, scratch space, and publication

Passing copied slices can add an $O(n)$ division cost at every balanced level. Even when the asymptotic class remains $O(n\log n)$, traffic and allocation may dominate. Prefer immutable views described by owner plus bounds, or intentionally partition ownership.

Scratch strategies include:

- one parent-owned buffer split into disjoint child regions;
- alternating source and destination roles by level;
- thread-local arenas with explicit peak budgets;
- staged child outputs combined into a parent buffer;
- recomputation when memory is more constrained than work.

State aliasing rules. Parallel children may read shared immutable input, but they must not write overlapping output or reuse the same mutable scratch region. Publication should occur only after required children and combine succeed. If in-place mutation precedes failure, document the valid partial state; do not imply rollback.

### Choose cutoffs and grain sizes from evidence

Recursion and generic combines have fixed overhead. A base cutoff may use insertion sort, schoolbook multiplication, a tuned matrix kernel, brute-force geometry, or a sequential reduction.

The cutoff must preserve:

- output and tie-breaking semantics;
- numeric overflow and precision policy;
- identity and stability requirements;
- ownership and mutation rules;
- error and cancellation behavior.

Measure sizes on both sides of every candidate cutoff across representative distributions, record widths, hardware, runtime/compiler versions, and cache states. Look for cliffs. Separate an algorithmic cutoff from a parallel spawn threshold: the best sequential leaf size need not equal the minimum profitable task size.

### Use recursive blocking without overclaiming locality

Recursive subdivision can create subproblems that eventually fit each cache level without hard-coding cache sizes. Cache-oblivious analyses use an idealized hierarchy with block size $B$, cache capacity $M$, and assumptions such as an optimal or simulable replacement policy.

The result applies only under its model and layout. Pointer-rich structures, conflict behavior, prefetchers, TLBs, NUMA, false sharing, and write allocation can change physical performance. Instrument block traffic or hardware counters and compare with a tuned iterative baseline.

A cache-oblivious theorem is an I/O-complexity result, not proof that a particular recursive implementation beats every cache-aware kernel.

### Preserve executable sufficient-summary evidence

The following teaching implementation returns the four-field maximum-subarray summary. It uses half-open intervals and breaks equal sums by earlier start, then earlier end.

<!-- bijux-verify: {"id":"divide-conquer-subarray-summary","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"input=(4, -1, 2, 1, -7, 5, 2, -1, 3, -10, 4)\nbest_sum=9 range=[5,9) values=(5, 2, -1, 3)\ntotal=2 calls=21 combines=10 max_depth=4\nmatches_bruteforce=True\n","stderr":""}} -->
~~~python
from dataclasses import dataclass


@dataclass(frozen=True)
class Summary:
    lo: int
    hi: int
    total: int
    prefix: tuple[int, int, int]
    suffix: tuple[int, int, int]
    best: tuple[int, int, int]


def better(*candidates):
    return max(candidates, key=lambda item: (item[0], -item[1], -item[2]))


def combine(left, right):
    assert left.hi == right.lo
    total = left.total + right.total
    prefix = better(
        left.prefix,
        (left.total + right.prefix[0], left.lo, right.prefix[2]),
    )
    suffix = better(
        right.suffix,
        (left.suffix[0] + right.total, left.suffix[1], right.hi),
    )
    crossing = (
        left.suffix[0] + right.prefix[0],
        left.suffix[1],
        right.prefix[2],
    )
    return Summary(
        left.lo,
        right.hi,
        total,
        prefix,
        suffix,
        better(left.best, right.best, crossing),
    )


def summarize(values):
    ledger = {"calls": 0, "combines": 0, "max_depth": 0}

    def solve(lo, hi, depth):
        ledger["calls"] += 1
        ledger["max_depth"] = max(ledger["max_depth"], depth)
        if hi - lo == 1:
            candidate = (values[lo], lo, hi)
            return Summary(lo, hi, values[lo], candidate, candidate, candidate)
        mid = lo + (hi - lo) // 2
        left = solve(lo, mid, depth + 1)
        right = solve(mid, hi, depth + 1)
        ledger["combines"] += 1
        return combine(left, right)

    if not values:
        raise ValueError("the contract requires a nonempty sequence")
    return solve(0, len(values), 0), ledger


def brute_force(values):
    candidates = []
    for lo in range(len(values)):
        total = 0
        for hi in range(lo + 1, len(values) + 1):
            total += values[hi - 1]
            candidates.append((total, lo, hi))
    return better(*candidates)


values = (4, -1, 2, 1, -7, 5, 2, -1, 3, -10, 4)
summary, ledger = summarize(values)
best_sum, lo, hi = summary.best
print(f"input={values}")
print(f"best_sum={best_sum} range=[{lo},{hi}) values={values[lo:hi]}")
print(
    f"total={summary.total} calls={ledger['calls']} "
    f"combines={ledger['combines']} max_depth={ledger['max_depth']}"
)
print(f"matches_bruteforce={summary.best == brute_force(values)}")
~~~

The run verifies one finite input and summary tree. It does not prove associativity for every numeric domain, fixed-width overflow safety, exception behavior, parallel races, or a production cutoff.

### Validate structure, not only final answers

Use property and differential tests for:

- empty and minimum base sizes under the declared contract;
- child preconditions, strict measure decrease, and exact range boundaries;
- identity coverage, overlap rules, and ownership;
- combine soundness and completeness against brute force on small instances;
- summary equivalence under different parenthesizations when associativity is claimed;
- deterministic ties, duplicates, exceptional values, and numeric extremes;
- work counters by level, partition balance, recursion depth, and leaf sizes;
- peak live scratch under sequential and parallel schedules;
- cancellation and failure at division, child, join, combine, and publication;
- cutoff agreement on both sides of every boundary;
- parallel equivalence across task schedules and worker counts;
- cache/I/O counters across layouts and cold/warm conditions.

Generate exhaustive small instances where feasible. Metamorphic relations can translate values, permute identities that should not affect a result, concatenate neutral segments, or compare a parent summary with combining summaries of every legal split. Sanitizers and checked builds should target bounds, overflow, aliasing, use-after-free, and races.

## Definitions and Notation

- $x$: one admitted problem instance.
- $\mu(x)$: a well-founded size or progress measure.
- $D(x)$: divide operation producing children and metadata.
- $x_1,\ldots,x_k$: recursive child instances.
- $S(x)$: result or sufficient summary returned for $x$.
- $C$: combine operation.
- $n$: scalar input size used for a derived recurrence.
- $n_i$: size of child $i$, with $n_i<n$ on recursive edges.
- $a$: number of recursive children in a balanced recurrence.
- $b$: constant shrink factor in child size $n/b$.
- $f(n)$: non-recursive divide and combine work in a recurrence.
- $W(n)$: total work for the declared case and cost model.
- $S_p(n)$: span or critical-path cost; the subscript avoids collision with summary function $S$.
- $M(n)$: peak live auxiliary space.
- $Q(n)$: block transfers or I/O under a declared memory model.
- $[lo,hi)$: half-open range containing indices $lo$ through $hi-1$.
- $mid=lo+\lfloor(hi-lo)/2\rfloor$: overflow-aware midpoint after range validation.
- $\mathcal C_j$: a named class of valid parent candidates.
- $B$: positional number base in algebraic splitting, or cache block size when explicitly identified by context.
- $P=W/S_p$: average parallelism bound for an algorithm DAG.

Soundness means returned objects satisfy the parent specification. Completeness means every required possibility, especially an optimum, is represented in the examined child or boundary classes. Balance concerns child sizes; independence concerns whether children can be solved without unavailable sibling state.

## Mechanisms, Invariants, or Proof Structure

A reusable divide-and-conquer proof follows this order.

1. **Specification.** Define admitted inputs, output, identities, equivalence and tie order, numeric semantics, mutation, and failure behavior.
2. **Measure.** Choose $\mu$ and prove every recursive edge decreases it. Enumerate all base cases.
3. **Division.** Prove child preconditions, bounds, identity membership, coverage/overlap, and metadata correctness.
4. **Candidate classification.** Partition or cover every parent answer into child-local and cross-boundary classes.
5. **Summary sufficiency.** For each class, prove child outputs retain enough information for combine; remove fields only with a proof they are irrelevant.
6. **Induction.** Apply the child contract to strictly smaller instances.
7. **Combine soundness.** Prove constructed candidates are legal parent candidates and numeric/identity operations are safe.
8. **Combine completeness.** Prove a global optimum or required result cannot lie outside the examined classes.
9. **Determinism.** Prove one consistent tie, ordering, and coordinate policy across recursive and cutoff implementations.
10. **Resource correspondence.** Derive work, span, space, I/O, and communication from executed calls, local work, concurrency, and liveness.
11. **Boundary implementation.** Check half-open arithmetic, empty/singleton behavior, views, aliases, scratch partitions, exceptions, cancellation, and publication.
12. **Evidence.** Compare exhaustively with an independent solver on bounded inputs, instrument structural counters, benchmark cutoffs and grain sizes, and retain environment metadata.

For maximum-subarray summaries, prove the prefix invariant by classifying a parent prefix as either wholly inside the left child or the entire left range followed by a right prefix. The suffix proof is symmetric. Classify a parent subarray as wholly left, wholly right, or a left suffix followed by a right prefix. These classes are exhaustive and their constructed intervals are valid. The deterministic `better` relation then selects exactly the parent optimum.

For Karatsuba, expand the reconstruction algebra and check carries and digit bounds separately. For closest pair, prove identity-based partitioning, preservation of $y$ order, strip completeness, and the packing bound. For parallel execution, extend logical proofs with race-free ownership, join-before-combine, exception aggregation, cancellation, and deterministic publication.

## Alternatives and Trade-Offs

- **Balanced versus natural splits:** balanced halves bound depth; semantic separators may be unequal but make combine dramatically cheaper.
- **Narrow versus rich summaries:** narrow results save space and copying; richer sufficient summaries can eliminate ancestor rescans or enable reuse.
- **Recursive versus iterative control:** recursion mirrors the proof; explicit stacks give direct capacity control and can reduce call overhead.
- **Views versus copied slices:** views avoid repeated traffic; copies simplify ownership and can improve locality or failure isolation.
- **Sequential versus parallel children:** sequential execution is simple and reuses scratch; parallel execution reduces span but increases scheduling and peak-space pressure.
- **Sequential versus parallel combine:** a serial combine can dominate span; parallel combine adds algorithmic complexity and often more temporary storage.
- **Uniform versus adaptive split:** fixed halves are predictable; pivot-, geometry-, or data-driven splits can exploit structure but require imbalance analysis.
- **Small base versus tuned cutoff:** small bases make proofs clean; larger direct kernels reduce overhead but need semantic equivalence and measured thresholds.
- **Asymptotically faster algebra versus tuned classical kernels:** Karatsuba and Strassen reduce recursive multiplications; additions, padding, workspace, precision, and hardware determine crossover.
- **Presort once versus sort in every combine:** preserved secondary order saves a logarithmic factor; it enlarges child interfaces and identity bookkeeping.
- **Cache-aware versus cache-oblivious:** explicit blocking can exploit known hardware; recursive layouts can adapt across levels under stronger model assumptions.
- **Recomputation versus retention:** retaining boundary summaries reduces work; recomputation can reduce peak space or simplify ownership.
- **Divide and conquer versus dynamic programming:** independent children avoid memo tables; substantial overlap calls for reuse rather than exponential recomputation.
- **Divide and conquer versus a linear scan:** recursive summaries expose parallelism and reusable range composition; a sequential scan may have lower constants and simpler state.

## Failure Modes and Misconceptions

1. **Recursion as proof:** recursive syntax is mistaken for a correct decomposition.
2. **Missing candidate class:** cross-boundary optima are never examined.
3. **Unsound combine:** the parent constructs an object violating the original specification.
4. **Incomplete summary:** a child discards information needed by an ancestor.
5. **No descent:** a child can equal its parent size.
6. **Wrong base contract:** cutoff code uses different ties, stability, precision, or exceptions.
7. **Coverage ambiguity:** child ranges drop, duplicate, or overlap identities unintentionally.
8. **Coordinate drift:** child-local indices are published as parent/global indices.
9. **Midpoint overflow:** $lo+hi$ wraps before division.
10. **Slice-copy blindness:** division silently copies $\Theta(n)$ data per level.
11. **Repeated sorting:** a strip or secondary dimension is sorted anew at every node.
12. **Balance worship:** cheap balanced division is assumed sufficient despite an expensive combine.
13. **Average split as worst case:** data-dependent imbalance is replaced by equal halves.
14. **Master theorem forcing:** unequal, decrementing, variable, or overlapping recurrences are misclassified.
15. **Work/span confusion:** concurrent child work is summed on the critical path.
16. **Unlimited processors:** $W/S_p$ is quoted as achieved speedup without scheduler and machine bounds.
17. **Task confetti:** tiny children cost more to schedule than to solve.
18. **Sibling-space sum error:** sequential peaks are added, or parallel live buffers are ignored.
19. **Shared-scratch race:** concurrent children write overlapping workspace.
20. **Cancellation leak:** one failed child leaves siblings, buffers, or tasks live.
21. **Numerical reconstruction bug:** carries, padding, signed intermediates, or floating error invalidate algebraic splitting.
22. **Exponent as crossover:** asymptotic improvement is treated as universal physical speed.
23. **Cache-model leakage:** an ideal-cache bound is presented as a measured hardware result.
24. **Final-output testing only:** wrong summaries happen to cancel on a few examples.
25. **Timing-only validation:** finite speed measurements replace correctness, termination, and resource proofs.
26. **Nondeterministic ties:** parallel schedules choose different equivalent answers.

## Worked Examples

### Example 1

**Question:** What recurrence describes binary search over a sorted range of length $n$?

**Reasoning:** One comparison with the middle key eliminates at least one half, and only one child executes:

$$
W(n)=W(\lceil(n-1)/2\rceil)+\Theta(1).
$$

There are $\Theta(\log n)$ strict halvings.

**Conclusion:** Work and stack depth are $\Theta(\log n)$ recursively; an iterative implementation can use $\Theta(1)$ auxiliary space.

### Example 2

**Question:** In the ideal recurrence $W(1)=0$ and $W(n)=2W(n/2)+n$ for $n=16$, what is exact non-leaf work?

**Reasoning:** There are four non-leaf levels. Each level's local work sums to 16:

$$
W(16)=16+16+16+16=64.
$$

There are 16 leaves and 15 internal combine nodes.

**Conclusion:** Linear combine work repeated over logarithmically many balanced levels gives $n\log_2 n=64$ under this exact model.

### Example 3

**Question:** Why does the executable maximum-subarray combine need prefix and suffix summaries?

**Reasoning:** At the root, the best interval may lie left, lie right, or cross. Every crossing interval is a suffix of the left child followed by a prefix of the right child. Child `best` fields alone cannot recover that candidate.

**Conclusion:** Total, prefix, suffix, and best form a sufficient constant-size summary; the sample's root chooses right-local $[5,9)$ with sum 9 over its crossing alternative.

### Example 4

**Question:** Use Karatsuba's split to compute $1234\cdot5678$ with base $B=100$.

**Reasoning:** Split $(x_1,x_0)=(12,34)$ and $(y_1,y_0)=(56,78)$. Then

$$
z_2=12\cdot56=672,
\qquad
z_0=34\cdot78=2652,
$$

$$
z_1=46\cdot134-672-2652=6164-3324=2840.
$$

Therefore

$$
xy=672\cdot10000+2840\cdot100+2652=7{,}006{,}652.
$$

**Conclusion:** Three half-size products replace four; additions and reconstruction remain linear digit work.

### Example 5

**Question:** What exponent follows from seven half-size matrix multiplications?

**Reasoning:** With quadratic block additions,

$$
W(n)=7W(n/2)+\Theta(n^2).
$$

Because $\log_2 7\approx2.807>2$, recursive multiplications dominate.

**Conclusion:** Strassen's asymptotic work is $\Theta(n^{\log_2 7})$, subject to implementation crossover and numerical constraints.

### Example 6

**Question:** What happens if a partition repeatedly produces sizes $0$ and $n-1$ with linear partition work?

**Reasoning:** The recurrence becomes

$$
W(n)=W(n-1)+\Theta(n)
=\Theta\left(\sum_{j=1}^{n}j\right)
=\Theta(n^2).
$$

**Conclusion:** Two recursive branches in the source do not imply balanced $2W(n/2)$ behavior.

### Example 7

**Question:** Why preserve planar closest-pair points in $y$ order?

**Reasoning:** Each parent must examine a strip around its separator. If it sorts each strip independently, level-$i$ sorting can add $\Theta(n\log(n/2^i))$ work, totaling $\Theta(n\log^2 n)$. Linear partition and merge of inherited $y$ order keep each level linear.

**Conclusion:** A richer child interface preserves the intended $\Theta(n\log n)$ total work.

### Example 8

**Question:** Compare span for parallel children with serial versus logarithmic-span combine when $n=2^k$.

**Reasoning:** Serial linear combine gives

$$
S_p(n)=S_p(n/2)+\Theta(n)=\Theta(n).
$$

Logarithmic combine gives

$$
S_p(n)=S_p(n/2)+\Theta(\log n)=\Theta(\log^2 n).
$$

With $W(n)=\Theta(n\log n)$, average parallelism changes from $\Theta(\log n)$ to $\Theta(n/\log n)$.

**Conclusion:** Parallel child creation alone does not remove the combine bottleneck.

### Example 9

**Question:** Solve peak-space recurrence $M(1)=0$ and $M(n)=M(n/2)+n$ for powers of two.

**Reasoning:**

$$
M(n)=n+\frac n2+\frac n4+\cdots+2<2n.
$$

**Conclusion:** Peak space is $\Theta(n)$ when one child's peak coexists with geometrically shrinking parent-local storage; summing both sequential siblings would be wrong.

### Example 10

**Question:** A balanced size-1024 recursion uses a direct cutoff at size 32. What structural counts follow?

**Reasoning:** Five halvings take $1024$ to $32$. The recursion has $2^5=32$ leaf tasks and $31$ internal nodes.

**Conclusion:** The cutoff changes exact calls and overhead, while a fixed cutoff preserves the surrounding asymptotic class.

## Cross-Program Connections

- [Theory of Computation & Complexity](../../15-theory-of-computation-and-complexity/ROADMAP.md) owns induction, lower bounds, recurrence theorems, algebraic models, and problem-level complexity.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) owns range summaries, segment trees, recursive layouts, persistent structure sharing, and ownership-aware representations.
- [Concurrent & Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) owns task DAGs, work/span scheduling, joins, cancellation, races, and deterministic parallel reductions.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) owns cache/block models, memory bandwidth, vectors, tuned kernels, NUMA, and hardware counters.
- [Programming Languages & Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) owns recursion semantics, exceptions, generics, numeric types, ownership, aliasing, and stack behavior.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns exhaustive bounded checks, properties, metamorphic tests, race/sanitizer runs, benchmarks, and regression evidence.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) owns remote task partitioning, retries, stragglers, partial failure, communication, and idempotent publication.

## References

1. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. [*Introduction to Algorithms*, fourth edition](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), MIT Press, 2022. Divide-and-conquer design, maximum subarray, recurrences, sorting, matrix multiplication, and parallel foundations.
2. MIT OpenCourseWare 6.006. [“Lecture 1: Introduction and Peak Finding”](https://www.ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/c32185c7158955425455159a8455298b_MIT6_006F11_lec01.pdf), Fall 2011. Instructional divide-and-conquer localization, correctness question, and logarithmic recurrence.
3. Mohamad Akra and Louay Bazzi. [“On the Solution of Linear Recurrence Equations”](https://doi.org/10.1023/A:1018373005182), *Computational Optimization and Applications* 10(2), 1998, pp. 195–210. Primary generalization for eligible unequal divide-and-conquer recurrences.
4. Anatolii Karatsuba and Yuri Ofman. [“Multiplication of Many-Digital Numbers by Automatic Computers”](https://m.mathnet.ru/php/archive.phtml?jrnid=dan&option_lang=eng&paperid=26729&wshow=paper), *Doklady Akademii Nauk SSSR* 145(2), 1962, pp. 293–294. Primary fast multiplication result.
5. Volker Strassen. [“Gaussian Elimination Is Not Optimal”](https://doi.org/10.1007/BF02165411), *Numerische Mathematik* 13, 1969, pp. 354–356. Primary subcubic matrix multiplication result.
6. Jon Louis Bentley and Michael Ian Shamos. [“Divide-and-Conquer in Multidimensional Space”](https://doi.org/10.1145/800113.803652), *Proceedings of the Eighth Annual ACM Symposium on Theory of Computing*, 1976, pp. 220–230. Primary multidimensional and closest-pair divide-and-conquer work.
7. Matteo Frigo, Charles E. Leiserson, Harald Prokop, and Sridhar Ramachandran. [“Cache-Oblivious Algorithms”](https://doi.org/10.1145/2071379.2071383), *ACM Transactions on Algorithms* 8(1), 2012, article 4. Primary ideal-cache model and recursive cache-oblivious algorithms.
8. ACM, IEEE Computer Society, and AAAI. [*Computer Science Curricula 2023: Algorithmic Foundations*](https://csed.acm.org/al-cs-core/), endorsed 2024; consulted 2026-09-04. Current curricular scope for design strategies, recursive analysis, parallelism, and empirical evaluation.

## Exercises

### Exercise 1

Design and prove a one-dimensional peak finder for a nonempty array: an index $i$ is a peak when its existing neighbors do not exceed it. Follow at most one half after inspecting a midpoint and adjacent value. State boundary rules, termination, correctness, work, recursive stack space, and an iterative alternative.

### Exercise 2

Prove the four-field maximum-subarray summary and combine used in the executable correct for nonempty integer sequences with tie order “larger sum, then earlier start, then earlier end.” Derive sequential work, ideal parallel span, and peak stack/summary space. Explain why returning only each child's best subarray is insufficient.

### Exercise 3

Apply Karatsuba splitting with $B=100$ to $1234\cdot5678$. Compute all three recursive products and reconstruction. Prove the algebraic identity, derive the asymptotic recurrence for $n$ digits, and list implementation conditions hidden by the recurrence.

### Exercise 4

For powers of two, solve

$$
W(n)=2W(n/2)+n,
\qquad
S_p(n)=S_p(n/2)+\log_2 n,
\qquad
M(n)=M(n/2)+n,
$$

with constant base values. Derive average parallelism $W/S_p$, and explain the execution and liveness assumptions behind all three recurrences.

### Exercise 5

Engineer a parallel library operation that returns total, best prefix, best suffix, and best subarray for a massive immutable numeric array. Specify numeric and tie contracts, range/scratch ownership, cutoffs, task grain, cancellation, overflow, deterministic results, work/span/space models, exhaustive and property tests, benchmarks, telemetry, and rollout safeguards.

## Answers to the Exercises

### Answer 1

Use half-open range $[lo,hi)$ and require $lo<hi$. Let

$$
mid=lo+\left\lfloor\frac{hi-lo}{2}\right\rfloor.
$$

Treat a missing neighbor as negative infinity for comparison only. If $mid>lo$ and $A[mid-1]>A[mid]$, continue with $[lo,mid)$. Otherwise, if $mid+1<hi$ and $A[mid+1]>A[mid]$, continue with $[mid+1,hi)$. Otherwise return $mid$.

Every recursive range is nonempty and strictly shorter. If the left neighbor is larger, move left from $mid-1$ while values strictly rise in that direction; either a boundary is reached or the rise stops at an index no smaller than both existing neighbors. That peak lies in the selected left range. The right case is symmetric. If neither neighbor is larger, $mid$ satisfies the peak definition. Thus the invariant “the current range contains a peak of the original array under its boundary directions” is preserved, and strict size descent proves termination.

At most one child of size no more than $\lceil n/2\rceil$ executes with constant local work:

$$
W(n)=W(\lceil n/2\rceil)+\Theta(1)=\Theta(\log n).
$$

Recursive stack space is $\Theta(\log n)$. An iterative loop that updates `lo` or `hi` preserves the same invariant and uses $\Theta(1)$ auxiliary space. Equal neighbors cause the current midpoint to qualify; deterministic selection among multiple peaks is not promised unless an additional tie contract is designed.

### Answer 2

For a range $R=[lo,hi)$, define `total` as the sum of all values. `prefix` is the best nonempty interval $[lo,j)$, `suffix` the best nonempty interval $[i,hi)$, and `best` the best nonempty subinterval, all under the declared total tie order. A singleton summary is immediate.

Assume adjacent child summaries $L=[lo,mid)$ and $R=[mid,hi)$ are correct. A parent prefix either ends at or before $mid$ and is represented by $L.prefix$, or contains all of $L$ followed by a prefix of $R$. These classes are exhaustive, so selecting the better of $L.prefix$ and $L.total+R.prefix$ is correct. The suffix proof is symmetric.

Every nonempty parent subarray is wholly in $L$, wholly in $R$, or crosses $mid$. A crossing interval is exactly a suffix of $L$ followed by a prefix of $R$. The best representatives are therefore $L.best$, $R.best$, and $L.suffix+R.prefix$. The same deterministic total order selects the correct sum and interval. Strong induction proves every summary field correct.

Returning only child `best` fields omits the information needed to construct the crossing class. Rescanning can recover it in linear combine work; prefix and suffix summaries recover it in constant work.

For balanced halves,

$$
W(n)=2W(n/2)+\Theta(1)=\Theta(n).
$$

If children execute in parallel and combine is constant span,

$$
S_p(n)=S_p(n/2)+\Theta(1)=\Theta(\log n).
$$

Sequential recursion retains $O(\log n)$ frames and constant-size summaries per live level, so peak auxiliary space is $O(\log n)$ excluding input and output. Parallel execution can retain summaries and task metadata across a frontier, reaching $O(n)$ total live task/summary storage without throttling. Fixed-width integer addition must be checked, widened, wrapped, or saturated according to the contract.

### Answer 3

Write

$$
1234=12\cdot100+34,
\qquad
5678=56\cdot100+78.
$$

The three products are

$$
z_2=12\cdot56=672,
$$

$$
z_0=34\cdot78=2652,
$$

and

$$
p=(12+34)(56+78)=46\cdot134=6164.
$$

Therefore

$$
z_1=p-z_2-z_0=6164-672-2652=2840,
$$

and

$$
672\cdot100^2+2840\cdot100+2652=7{,}006{,}652.
$$

In general,

$$
(x_1B^m+x_0)(y_1B^m+y_0)
=x_1y_1B^{2m}+(x_1y_0+x_0y_1)B^m+x_0y_0.
$$

Also,

$$
(x_1+x_0)(y_1+y_0)-x_1y_1-x_0y_0
=x_1y_0+x_0y_1,
$$

which proves reconstruction.

For $n$ digits and linear splitting, addition, subtraction, carry, and reconstruction,

$$
W(n)=3W(\lceil n/2\rceil)+\Theta(n)
=\Theta(n^{\log_2 3}).
$$

The recurrence hides signed intermediates, carry normalization, unequal lengths, leading zeros, representation base, allocation and aliasing, recursion stack, multiplication/addition constants, cutoff to a classical kernel, failures, and target hardware. It also assumes linear-time digit additions and that child sizes remain near half.

### Answer 4

Let $n=2^k$. Each non-leaf work level totals $n$, and there are $k$ levels, so

$$
W(n)=\Theta(n\log n).
$$

For span, unroll the logarithmic combine along one child path:

$$
S_p(n)
=\Theta\left(
k+(k-1)+\cdots+1
\right)
=\Theta(k^2)
=\Theta(\log^2 n).
$$

For peak space,

$$
M(n)
=n+\frac n2+\frac n4+\cdots+O(1)
=\Theta(n).
$$

Thus average parallelism is

$$
\frac{W(n)}{S_p(n)}
=
\Theta\left(\frac{n\log n}{\log^2 n}\right)
=
\Theta\left(\frac n{\log n}\right).
$$

The work recurrence assumes both children execute and their total non-recursive work is exactly linear by level. The span recurrence assumes children are independent and concurrent, division is covered by the stated term, and combine has $\Theta(\log n)$ critical path. The space recurrence assumes only one child peak is added to geometrically shrinking parent-local storage, as with sequential children or a carefully shared/throttled schedule. Fully concurrent siblings with private retained buffers require a different liveness recurrence. None of the formulas includes finite processor count, scheduler overhead, bandwidth, or allocator contention.

### Answer 5

Accept an immutable nonempty random-access range and return one summary with global half-open indices. Declare numeric input types, whether accumulation widens, checks, wraps, saturates, or uses arbitrary precision, and the total tie rule “larger sum, earlier start, earlier end.” Reject invalid ranges before task creation. Empty input either has a separately defined identity summary or returns a declared error; do not improvise a sentinel that conflicts with valid values.

Represent each child by owner plus $[lo,hi)$; children only read input and write disjoint task-local summary slots. Compute midpoints from validated differences. Singleton and sequential-cutoff kernels return the identical four-field contract. Combine only adjacent summaries, verifies `left.hi == right.lo` in checked builds, uses checked numeric operations, and publishes the root only after all joins succeed.

Use a sequential direct kernel below a benchmarked algorithm cutoff. Spawn the larger recursive tree only while size exceeds a separate grain threshold and a bounded executor has capacity. On child error or cancellation, signal siblings, join them, release slots/arenas, and return no published result. Define deterministic error precedence when both children fail. Bound task count, recursion depth, retained summaries, total CPU, wall time, and cancellation latency.

The ideal model is $W(n)=2W(n/2)+O(1)=O(n)$ and, above the sequential cutoff with parallel children, $S_p(n)=S_p(n/2)+O(1)=O(\log n)$. A sequential recursion uses $O(\log n)$ live frames; an unthrottled parallel frontier can use $O(n)$ task/summary metadata, so the executor and arena need an explicit cap. Model numeric width and input traffic separately.

Exhaust every short sequence over a small signed alphabet and compare total, prefix, suffix, best, and ties with independent brute force. For every legal split, compare the direct parent summary with `combine(summarize(left), summarize(right))`; test multiple parenthesizations. Add singleton, all negative, zeros, ties, extreme values, overflow, cutoff neighbors, cancellation at each lifecycle point, allocation failure, injected child errors, worker counts, randomized schedules, and race/sanitizer runs.

Benchmark full calls across size, sign/run distributions, numeric widths, cutoff/grain grids, cold/warm caches, worker counts, NUMA placement, and contention. Retain raw repetitions, environment/build versions, wall and CPU distributions, bandwidth/counters, tasks, steals, depth, peak bytes, cancellation, and errors. Compare with a trusted sequential scan and a simple parallel reduction. Reject parallel dispatch when overhead or memory exceeds the agreed objective.

Version cutoffs and executor policy. Canary the parallel path, compare sampled results with the sequential baseline, expose bounded non-sensitive telemetry, and define rollback on any result mismatch, overflow-policy deviation, task/space spike, or tail-latency regression. Keep the sequential implementation as the known-safe fallback until the observation criteria pass.
