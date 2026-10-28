---
module_id: ALGE-018
program: Algorithm Engineering
level: 1
module_number: 18
title: Stable Sorting and Indirect Sorting
status: complete
last_verified: 2026-09-04
---

# Stable Sorting and Indirect Sorting

## One-Page Review

### Governing question

How should a sorting implementation preserve the observable order of equivalent records, and when should it sort a permutation of indices instead of moving the records themselves?

### Essential definitions

- A strict ordering relation writes $a\prec b$ when $a$ must precede $b$.
- Records are **equivalent under the ordering** when neither precedes the other:

  $$
  a\sim b
  \iff
  \neg(a\prec b)\land\neg(b\prec a).
  $$

- A sort is **stable** when input identity $i$ remains before input identity $j$ whenever $i<j$ and their records are equivalent.
- A **direct sort** rearranges records, references, or record slots into output order.
- An **indirect sort** returns a permutation $p$ such that $p[j]$ names the old record viewed at new position $j$.
- The **gather map** is $p:\text{new}\to\text{old}$; its inverse $q:\text{old}\to\text{new}$ is the scatter or destination map.
- **Decorate-sort-undecorate** materializes a sortable key and an original-position tie breaker before sorting, then removes the decoration.
- A **stable merge** takes the left record first when left and right front records are equivalent.
- A **materialized permutation** physically rearranges records according to a validated index map, often by copying or following cycles.

### Central model, mechanism, or theorem

Let input identities be $r_0,\ldots,r_{n-1}$. An indirect result is a bijection

$$
p:\{0,\ldots,n-1\}\to\{0,\ldots,n-1\},
$$

with sorted view

$$
B[j]=A[p[j]].
$$

Let $q=p^{-1}$, so $q[p[j]]=j$. The complete stable-sort contract is:

$$
\neg\left(r_{p[j+1]}\prec r_{p[j]}\right)
\quad\text{for }0\le j<n-1,
$$

$$
i<j\land r_i\sim r_j
\Longrightarrow
q[i]<q[j].
$$

Stability composes lexicographic keys. Stable sorting first by the least significant component and proceeding toward the most significant component produces the intended priority order. Decorating record $r_i$ with $(K(r_i),i)$ also makes the desired order explicit because original positions uniquely break equal-key ties.

### Critical invariants

- Stability concerns equivalence under the declared comparator, not necessarily object equality.
- The result is an identity permutation: no record is omitted, duplicated, or synthesized.
- A stable merge chooses from the earlier input run on equivalence and preserves order within both runs.
- Stable multi-pass sorting processes key components from least to most significant.
- A decorated index is unique within the exact input snapshot and wide enough for every position.
- An indirect permutation has one in-range occurrence of every old index.
- The gather and inverse maps satisfy $q[p[j]]=j$ and $p[q[i]]=i$.
- A view and its cached keys refer to the same immutable snapshot or declared version.
- Applying a permutation publishes only a complete destination arrangement.
- Stability, determinism, reproducibility, and total-order semantics are related but distinct contracts.

### Common failures

Common failures include calling an algorithm stable by family name without checking its tie branch; confusing comparator equivalence with language equality; taking the right merge record on equality; swapping equal records in insertion or selection logic; sorting primary keys before secondary keys in a stable multi-pass pipeline; reversing a stable ascending output and thereby reversing equal groups; allowing the payload to participate after a decorate tie; confusing new-to-old and old-to-new permutations; accepting duplicate or out-of-range indices; applying a permutation twice; leaving keys stale while records mutate; claiming constant space while storing $n$ indices; and reporting fewer moved bytes without measuring indirection and locality.

### Compact example

For records

$$
((2,A),(1,B),(2,C),(1,D),(2,E)),
$$

a stable indirect result is

$$
p=(1,3,0,2,4).
$$

It denotes the view

$$
((1,B),(1,D),(2,A),(2,C),(2,E)).
$$

The inverse is $q=(2,0,3,1,4)$. The source records need not move; if materialization is later required, $q$ supplies each old record's destination.

### Connections

[ALGE-012](./012-insertion-selection-and-shell-sorting.md) introduced stability as a sorting postcondition; [ALGE-013](./013-merge-sort.md) supplies stable merge mechanics; [ALGE-016](./016-counting-radix-and-bucket-sorting.md) depends on stable distribution passes; and ALGE-019 will use stability inside adaptive and hybrid policies.

## Governing Question

How can stable and indirect sorting be specified, proved, implemented, and evaluated so that equal-key identity order and record-movement costs remain visible parts of the contract?

“Sorted” alone describes key order. It does not say what happens to two records that compare as equivalent. That missing order is observable in reports, pagination, event replay, user interfaces, multi-key queries, radix passes, tests, and distributed merges.

“Sort the records” is also incomplete. A system may instead sort small integers that identify records and expose a view through those integers. That choice can reduce movement of wide payloads, preserve the original arrangement, and support several simultaneous orders. It can also add memory, pointer chasing, snapshot-lifetime constraints, and a later materialization step.

This module treats stability and indirection as explicit mathematical and operational contracts rather than incidental properties of a library call.

## Why This Matters

Consider invoices ordered by customer while their arrival order already represents creation time. A stable customer sort preserves time order inside each customer. An unstable sort can silently scramble it. The keys are still nondecreasing, so a test that checks only adjacent keys misses the defect.

Stability also enables multi-key composition. If records are stably sorted by timestamp and then stably sorted by customer, the final order is customer first and timestamp second. This is useful when key fields are selected dynamically or have different ascending and descending policies.

For wide records, comparison count is only part of cost. Moving a 512-byte record is different from moving an eight-byte index. Indirect sorting can keep a canonical record store untouched while producing a compact order vector. Search results, column stores, graph layouts, scientific tables, and databases often exploit this separation.

The trade is not universally favorable. Every indirect lookup can add a dependent memory access. Repeated view traversal may be slower than one materialization. A permutation can become invalid if its source snapshot changes. The engineering question therefore includes record width, access pattern, number of views, mutation lifecycle, cache behavior, failure ownership, and publication semantics.

## Prerequisites and Retrieval

Retrieve:

- sorted-permutation and comparator contracts;
- strict weak order, equivalence classes, and lexicographic order;
- insertion, merge, counting, radix, quick, and heap sorting;
- arrays, indices, bijections, inverses, and cycle decompositions;
- loop invariants, induction, and identity preservation;
- key extraction, overflow, NaN, locale, null, and callback behavior;
- memory hierarchy, record width, references, snapshots, and versioning;
- exception safety, cancellation, concurrency, and atomic publication.

You should be able to distinguish a record's key, identity, physical position, and output rank, and to prove that an array rearrangement is a permutation.

## Learning Objectives

After completing this module, you should be able to:

1. define stability using comparator equivalence and original identities;
2. test order, permutation, and stability as separate postconditions;
3. prove stable merge and stable insertion tie behavior;
4. derive lexicographic multi-key order from least-to-most-significant stable passes;
5. derive stability from decorate-sort-undecorate with an original-position tie;
6. define indirect sorting with unambiguous gather and inverse maps;
7. validate and materialize a permutation using copying or cycles;
8. compare record movement, index movement, memory, and locality costs;
9. specify snapshots, cached keys, exceptions, cancellation, and parallel tie order;
10. design and evaluate a stable ordering pipeline for unfamiliar production constraints.

## Core Exposition

### Define equivalence before stability

Let $\prec$ be the relation supplied to a comparison sort. For a strict weak ordering, records $a$ and $b$ are equivalent when

$$
a\sim b
\iff
\neg(a\prec b)\land\neg(b\prec a).
$$

This is comparator equivalence, not necessarily object equality. Two distinct log events may compare equivalent by timestamp; two differently cased strings may compare equivalent under a case-folded key; two floating records may require a separately declared NaN policy before they form a valid ordering domain.

Let the input records carry stable identities $r_0,\ldots,r_{n-1}$. If output position $t$ contains input record $r_{p[t]}$, then $p$ maps a new position to an old identity. The output is ordered when

$$
\neg\left(r_{p[t+1]}\prec r_{p[t]}\right)
\quad
\text{for every }0\le t<n-1.
$$

It is stable when

$$
i<j\land r_i\sim r_j
\Longrightarrow
p^{-1}(i)<p^{-1}(j).
$$

It is an identity permutation when $p$ is a bijection. These are three separate obligations:

1. adjacent output keys are ordered;
2. every input identity occurs exactly once;
3. every comparator-equivalent pair keeps input order.

A correct stable-sort test records identities before sorting. Checking values alone cannot distinguish two equal-key records.

### Stability belongs to an implementation and comparator

Algorithm families suggest stability, but a concrete tie branch decides it. Conventional mergesort is stable only if its merge chooses from the left run when front records are equivalent. Conventional insertion sort is stable only if it moves a predecessor while the new record is strictly less, not while it is less than or equal.

Selection sort can exchange a later minimum across an equivalent record. Heapsort and ordinary in-place quicksort can exchange equivalent records across long distances. Stable variants exist, often with more metadata, movement, or algorithmic complexity. Therefore “mergesort is stable” is shorthand for a proven implementation under a declared relation, not permission to omit the tie proof.

Language-library contracts also differ. A stable-sort API promises relative order for equivalent elements; an ordinary sort API may not. The C standard specifies that the order of elements comparing equal after its ordinary array sort is unspecified. Do not infer stability from one platform, one observed run, or current input addresses.

### Prove the stable merge tie rule

Suppose left run $L$ and right run $R$ are individually sorted and stable relative to their source ranges, and every input identity in $L$ originally preceded every input identity in $R$. At each output position:

- take $R[j]$ if $R[j]\prec L[i]$;
- otherwise take $L[i]$.

The ordinary merge invariant says the output prefix is ordered and contains exactly the consumed run prefixes. The second branch includes both $L[i]\prec R[j]$ and equivalence. Thus an equivalent cross-run pair takes the left identity first. Within a run, consumption is left to right, so its identity order is unchanged.

Consequently the merge is sorted, a permutation, and stable. Replacing the decision with “take left only if $L[i]\prec R[j]$” sends the right record first on equivalence and reverses cross-run ties.

### Derive multi-key order by stable composition

Suppose the desired lexicographic priority is

$$
(K_1,K_2,\ldots,K_d),
$$

where $K_1$ is most significant. Perform stable sorts in reverse priority:

$$
K_d,\ K_{d-1},\ \ldots,\ K_1.
$$

After the $K_t$ pass, maintain:

> Records are ordered lexicographically by $(K_t,K_{t+1},\ldots,K_d)$.

The base case is the stable sort by $K_d$. For the inductive step, the next pass orders different $K_t$ values. Within an equal-$K_t$ class, stability preserves the previously established suffix order. After the final $K_1$ pass, the complete tuple is ordered.

Processing the primary component first generally fails because a later secondary pass is allowed to move records across primary groups. A direct tuple comparator can establish the same order in one sort. Multi-pass composition remains useful for dynamic specifications, legacy APIs, external passes, and distinct direction or collation policies.

Each pass must implement its requested direction stably. Reversing an entire stable ascending output is not a general stable descending transform: it reverses records inside each equal-key block. Use a stable descending comparator, a library contract that preserves equality under reverse order, or a proven double-reversal construction.

### Decorate with the original position

Decorate input identity $r_i$ as

$$
D_i=(K(r_i),i,r_i).
$$

Sort decorations lexicographically by the first two fields, then remove the key and index. When $K(r_i)<K(r_j)$, key order decides. When keys are equivalent and $i<j$, the index decides:

$$
(K(r_i),i)<(K(r_j),j).
$$

The composite keys are unique, so any correct sorter for that total composite order produces the desired stable order even if its native equal-key behavior is unstable. The payload must not be compared after the unique position field.

This transformation also caches an expensive key once. Its costs include $n$ keys, $n$ indices, decorations or references, allocation, and undecoration. The position must be unique in the exact accepted snapshot, wide enough for $n-1$, and compared without lossy subtraction. A persistent record identifier is not automatically an original-position tie breaker: identifiers may encode another order, repeat across shards, or be absent.

Decorating changes the comparator's formal equivalence classes by making each composite key unique. It implements stability with respect to the original key; it does not make the original records semantically unequal.

### Define indirect sorting with one direction

An indirect sort leaves source array $A$ in place and returns a permutation

$$
p[0:n).
$$

This module fixes the direction:

$$
p[\text{new position}]=\text{old position}.
$$

The sorted view is therefore

$$
B[j]=A[p[j]].
$$

For records

$$
A=((2,A),(1,B),(2,C),(1,D),(2,E)),
$$

the stable gather map is

$$
p=(1,3,0,2,4).
$$

The inverse map $q$ satisfies

$$
q[p[j]]=j,
$$

so

$$
q=(2,0,3,1,4).
$$

Here $q[\text{old position}]=\text{new position}$. Naming the direction at every interface prevents one of the most destructive permutation bugs: treating a gather vector as a destination vector.

An indirect sorter may stably merge indices by comparing $A[i]$, or sort indices by decorated key $(K(A[i]),i)$. The output must contain each integer from $0$ through $n-1$ exactly once. Key order and stability then refer through the indices.

### Prove the indirect postconditions

Validate four properties:

1. **Domain:** every $p[j]$ is an integer in $[0,n)$.
2. **Uniqueness:** no old index occurs twice.
3. **Order:** $A[p[j+1]]$ does not precede $A[p[j]]$.
4. **Stability:** if $i<j$ and $A[i]\sim A[j]$, then $q[i]<q[j]$.

There are $n$ output positions. Domain plus uniqueness implies that all $n$ old indices occur, so $p$ is a bijection. Constructing $q[p[j]]=j$ then yields both inverse laws:

$$
q[p[j]]=j,
\qquad
p[q[i]]=i.
$$

A Boolean seen array validates the permutation in $O(n)$ time and $O(n)$ bits or words. In-place marking schemes can reduce auxiliary storage but may mutate the vector, depend on a reserved numeric encoding, and complicate failure recovery.

### Materialize by copying or by cycles

The safest materialization allocates $B$ and gathers:

$$
B[j]\gets A[p[j]].
$$

After all writes succeed, publish or swap $B$. This costs $O(n)$ extra record storage but gives a simple strong-publication boundary: the original remains intact until success.

For in-place application, use the inverse destination map $q$. Every permutation decomposes into disjoint cycles. For cycle

$$
i_0\to i_1\to\cdots\to i_{\ell-1}\to i_0,
$$

hold the record from $i_0$, move it to destination $i_1=q[i_0]$, retain the displaced record, and continue. One temporary record and $\ell$ destination writes apply a nontrivial length-$\ell$ cycle. Mark each old position when its record has been sent.

If $f$ indices are fixed points and fixed points are skipped, this policy performs

$$
n-f
$$

record destination writes. The count excludes validation, index reads, the initial temporary load per nontrivial cycle, and move-constructor side effects. A swap-based implementation has a different ledger.

Cycles save a full record buffer but weaken failure simplicity. A throwing move can leave a partially rotated cycle. Aliases may observe intermediate states. Validate the entire permutation first, define whether record moves can fail, and do not apply the same map twice unless that is intentionally the mathematical operation.

### Preserve executable permutation evidence

The following ledger constructs a stable indirect order using key plus original index, computes both map directions, materializes by destination cycles, and checks independent postconditions.

<!-- bijux-verify: {"id":"stable-indirect-cycle-ledger","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"records=((2, 'A'), (1, 'B'), (2, 'C'), (1, 'D'), (2, 'E'))\ngather=(1, 3, 0, 2, 4)\ninverse=(2, 0, 3, 1, 4)\nview=((1, 'B'), (1, 'D'), (2, 'A'), (2, 'C'), (2, 'E'))\nmaterialized=((1, 'B'), (1, 'D'), (2, 'A'), (2, 'C'), (2, 'E'))\ncycle_writes=4 fixed_points=1\nordered=True stable=True permutation=True\n","stderr":""}} -->
~~~python
from collections import Counter


records = ((2, "A"), (1, "B"), (2, "C"), (1, "D"), (2, "E"))
n = len(records)

gather = tuple(sorted(range(n), key=lambda index: (records[index][0], index)))
inverse_list = [0] * n
for new_position, old_position in enumerate(gather):
    inverse_list[old_position] = new_position
inverse = tuple(inverse_list)

view = tuple(records[old_position] for old_position in gather)

materialized = list(records)
visited = [False] * n
writes = 0
for start in range(n):
    if inverse[start] == start:
        visited[start] = True
        continue
    if visited[start]:
        continue

    current = start
    held = materialized[current]
    while True:
        destination = inverse[current]
        held, materialized[destination] = materialized[destination], held
        writes += 1
        visited[current] = True
        current = destination
        if current == start:
            break

ordered = all(view[index][0] <= view[index + 1][0] for index in range(n - 1))
stable = all(
    inverse[left] < inverse[right]
    for left in range(n)
    for right in range(left + 1, n)
    if records[left][0] == records[right][0]
)
permutation = (
    Counter(materialized) == Counter(records)
    and all(inverse[gather[new]] == new for new in range(n))
    and all(gather[inverse[old]] == old for old in range(n))
)

print(f"records={records}")
print(f"gather={gather}")
print(f"inverse={inverse}")
print(f"view={view}")
print(f"materialized={tuple(materialized)}")
print(f"cycle_writes={writes} fixed_points={sum(inverse[i] == i for i in range(n))}")
print(f"ordered={ordered} stable={stable} permutation={permutation}")
~~~

This execution establishes one finite map and cycle trace. It does not prove that every comparator is valid, that every record move is nonthrowing, or that indirection improves physical performance.

### Account for movement and storage

Let record width be $w$, index width $s$, and cached-key width $h$. One sequential pass that rewrites all records transfers at least a model quantity

$$
nw
$$

of destination payload bytes, before reads, write allocation, metadata, or amplification. One index-vector pass writes

$$
ns.
$$

For $n=10{,}000{,}000$, $w=512$ bytes, and $s=8$ bytes:

$$
nw=5{,}120{,}000{,}000\text{ bytes}=5.12\text{ GB},
$$

$$
ns=80{,}000{,}000\text{ bytes}=80\text{ MB}.
$$

The modeled destination-byte ratio is $w/s=64$. A sort performs multiple passes or swaps, so measure actual reads and writes rather than multiplying this example into an undocumented claim.

Indirect storage is not constant space. One permutation costs $ns$ bytes. Stable mergesort of indices may require another $ns$-byte buffer. Cached keys cost $nh$. With a 16-byte key in the example, one index vector, one auxiliary index vector, and cached keys total

$$
n(8+8+16)=320{,}000{,}000\text{ bytes}=320\text{ MB}
$$

before allocator and container overhead.

### Evaluate locality, reuse, and materialization

Indirect comparison can improve sorting locality because the permutation and keys are compact, but traversing the resulting view accesses records in permutation order. If records are scattered, the dependent gathers can cause cache and translation misses.

The lifecycle decides:

- If only a small projection is consumed once, keep the indirect view.
- If several orders over one immutable store are needed, keep several permutations.
- If the entire wide payload is scanned repeatedly in final order, one materialization may amortize its cost.
- If downstream code needs stable addresses, move indices or references rather than objects.
- If the source changes frequently, maintain versioned views or rebuild them.

Benchmark sort construction and downstream consumption separately and together. A faster index sort can lose end to end if every later operator becomes a random gather.

### Cache keys against a declared snapshot

A key function may normalize text, parse a timestamp, consult a table, or allocate. Calling it during every comparison can multiply cost and expose inconsistent results if external state changes.

Materializing one key per accepted record gives an explicit snapshot:

$$
\widehat K_i=K(r_i)\quad\text{once}.
$$

The sort then compares $\widehat K_i$. This can improve consistency and failure isolation, but it consumes memory and freezes the key at extraction time. Define whether mutation after extraction is prohibited, version checked, copied, or intentionally ignored.

Validate key domains before publication: total order for NaNs and nulls, normalization and collation version for text, time zone and precision for timestamps, and overflow-safe comparisons. Comparing integers by subtraction can overflow. Comparator callbacks must be transitive, repeatable for cached state, and free of prohibited reentrancy.

### Separate stability from determinism

Stability says only that equivalent records retain their input order. If input arrival order varies across executions, a stable result can vary too. A deterministic result may instead require a durable total tie key such as

$$
(\text{business key},\text{event sequence},\text{record identifier}).
$$

That produces a repeatable order only if every component and its encoding are themselves repeatable and unique where required. Conversely, a deterministic but unstable algorithm could use an implementation-specific identity order that repeats on one machine while violating the API's intended input-order semantics.

Document separately:

- semantic primary and secondary keys;
- equivalence;
- whether original input order is meaningful;
- stable behavior;
- deterministic tie resolution across snapshots;
- collation/version provenance.

Stable sort is not a substitute for an explicit total order in pagination or distributed reconciliation.

### Compose stable parallel and external sorting

Parallel local stable sorts are insufficient if equal-key runs are concatenated in worker-completion order. Preserve each record's global input position or preserve source-range order during stable merges.

For adjacent source ranges, a stable merge takes the earlier range first on equivalence. A merge tree remains globally stable by induction when every leaf corresponds to an ordered source interval and every internal merge observes that rule.

External sorting has the same obligation. Run generation must define order within equal keys, and the multiway merge must break equal keys by original run/source position. If runs are produced from contiguous source intervals, run ordinal plus within-run position can encode original order. If ingestion is concurrent, “original” must be a declared sequence, not worker finish time.

Partitioning by key across machines makes cross-partition order easy for unequal keys but leaves boundary/equal-key ownership, retries, duplicates, and shard sequence to specify. A globally unique stable sequence can be expensive; require it only when the product contract needs it.

### Engineer failure, cancellation, and publication

A direct in-place stable sort may permute records before comparator failure, allocation failure, or cancellation. An indirect pipeline can isolate risk:

1. acquire or identify an immutable source version;
2. extract and validate keys into private storage;
3. build and validate a private permutation;
4. verify order, stability, and inverse maps;
5. publish the permutation atomically;
6. optionally materialize into a private destination and publish after completion.

This pattern does not make callbacks safe by itself. Bound key time, allocations, output size, and cancellation latency. Do not expose a half-filled permutation. If cycle application is used in place, state basic rather than strong failure safety unless record movement cannot fail or a recovery journal exists.

Cancellation checkpoints belong between bounded key blocks, merge blocks, index partitions, validation blocks, and permutation cycles. A single enormous record move or comparator call can still dominate response latency.

### Validate and measure the whole contract

Use empty, singleton, two equivalent identities, all equal, already sorted, reverse, alternating duplicate groups, large equivalence classes, inconsistent comparator, NaN/null policy, maximum index, wide payload, throwing move, stale snapshot, and corrupted permutation cases.

Property checks should assert:

- output length and identity multiset;
- adjacent comparator order;
- stable pair order for every bounded equivalent pair;
- exact agreement with a trusted decoration $(K_i,i)$;
- gather/inverse laws;
- cycle materialization agreement with copying;
- source immutability for indirect mode;
- publication only after complete validation.

Measure comparisons, key calls/time, key bytes, index bytes, auxiliary bytes, record moves/bytes, cycles, fixed points, cache and translation misses, gather throughput, allocation failure, cancellation latency, merge skew, and end-to-end consumer time. Compare stable direct sort, decorated unstable sort, stable index sort, unstable index sort when allowed, and materialized versus retained views.

## Definitions and Notation

- $n$ is the number of records in one accepted snapshot.
- $r_i$ is the identity of the record originally at position $i$.
- $\prec$ is the declared strict ordering relation.
- $a\sim b$ means neither $a\prec b$ nor $b\prec a$.
- $K_t$ is key component $t$, ordered from most to least significant.
- $p[j]$ is the old position viewed at new position $j$.
- $q[i]$ is the new destination of old position $i$.
- $q=p^{-1}$, so $q[p[j]]=j$ and $p[q[i]]=i$.
- A direct sort changes physical record order.
- An indirect sort returns a permutation while retaining source order.
- A fixed point is an index $i$ with $q[i]=i$.
- A cycle is an orbit under repeated application of a permutation.
- $w$, $s$, and $h$ are record, index, and cached-key widths.
- Stability preserves original order inside every comparator-equivalence class.
- Deterministic tie order is a separate cross-execution policy.
- Materialization converts an indirect view into a physical record arrangement.

## Mechanisms, Invariants, or Proof Structure

Use this sequence to review a stable or indirect sort:

1. State record identity, snapshot boundary, semantic keys, directions, and equivalence.
2. Verify the comparator or key encoding defines the required order domain.
3. State whether the API promises stability, deterministic total ties, or both.
4. Prove adjacent order and identity permutation independently.
5. For direct stability, trace every operation that can move one equal record across another.
6. For merge, choose the earlier source run on equivalence.
7. For multi-pass keys, process components from least to most significant.
8. For decoration, prove original position is unique, in range, and compared before payload.
9. State the permutation direction as new-to-old or old-to-new at every boundary.
10. Validate the permutation domain and uniqueness before indexing or mutation.
11. Construct the inverse and check both inverse laws.
12. Prove indirect order and stable equivalent-pair ranks through the source snapshot.
13. Choose private gather copying or checked cycle application and state failure safety.
14. Account for keys, indices, auxiliary vectors, record bytes, and downstream gathers.
15. Define versioning, publication, cancellation, parallel merge order, telemetry, and tests.

The stable composition chain is:

$$
\text{stable suffix order}
\land
\text{stable next-key sort}
\Longrightarrow
\text{longer lexicographic order}.
$$

The indirect correctness chain is:

$$
\text{valid bijection}
\land
\text{ordered gathered keys}
\land
\text{increasing ranks for equivalent identities}
\Longrightarrow
\text{stable indirect order}.
$$

Materialization then requires:

$$
q=p^{-1}
\land
\text{each cycle applied once}
\Longrightarrow
A_{\mathrm{new}}[j]=A_{\mathrm{old}}[p[j]].
$$

## Alternatives and Trade-Offs

| Approach | Stable behavior | Extra storage | Record movement | Best fit |
|---|---|---:|---:|---|
| Stable direct merge sort | Native when ties take left | $O(n)$ records or references conventionally | Multiple record passes | General stable materialized output |
| Stable in-place insertion sort | Native with strict shifts | $O(1)$ records | Can be quadratic | Small or nearly ordered ranges |
| Decorate plus arbitrary correct sort | Enforced by original-index tie | $O(n)$ keys and indices | Depends on payload/reference choice | Expensive keys or unstable library primitive |
| Stable indirect merge sort | Native on indices | $O(n)$ indices plus buffer | Source records unchanged | Wide records and reusable views |
| Index sort by $(K_i,i)$ | Enforced by unique composite key | $O(n)$ indices and optional keys | Source records unchanged | Explicit deterministic snapshot order |
| Gather-copy materialization | Inherits validated permutation | $O(n)$ records | One complete gather/write | Strong publish boundary |
| In-place cycle materialization | Inherits validated permutation | Marks plus one record | $n-f$ modeled destination writes | Memory-constrained, nonthrowing moves |
| Unstable direct sort | Not promised | Often $O(\log n)$ stack or less | Algorithm dependent | Equality order genuinely irrelevant |

No row dominates. Stability semantics, record width, key cost, number of views, mutation, locality, memory, failure guarantees, and downstream traversal choose the implementation.

## Failure Modes and Misconceptions

1. **Equality mismatch:** object equality is tested instead of comparator equivalence.
2. **Family-name proof:** mergesort is called stable while its equality branch takes right.
3. **Non-strict insertion:** an equal predecessor is shifted past the inserted identity.
4. **Long-distance swap:** selection, heap, or partition movement crosses equal records unnoticed.
5. **Value-only testing:** duplicate identities are erased before stability is checked.
6. **Primary-first passes:** a later secondary sort destroys primary grouping.
7. **Whole-output reversal:** equal groups reverse during a descending conversion.
8. **Payload comparison:** decoration falls through to an unorderable or unintended record field.
9. **Nonunique decoration:** shard-local positions collide in a combined snapshot.
10. **Index overflow:** an original position is truncated or compared by overflowing subtraction.
11. **Map-direction confusion:** a gather vector is treated as a destination vector.
12. **Range omission:** a negative or $n$ index is dereferenced before validation.
13. **Duplicate index:** one record is emitted twice and another silently disappears.
14. **Missing inverse check:** only $q[p[j]]=j$ is sampled and corruption escapes.
15. **Double application:** a correct permutation is accidentally materialized twice.
16. **Fixed-point overcount:** skipped records are included in a claimed movement saving.
17. **Constant-space fiction:** the $n$-entry permutation or visited marks are ignored.
18. **Stale view:** source records mutate after keys and order were captured.
19. **Address instability:** moved objects invalidate pointers held by another subsystem.
20. **Stable-means-deterministic:** varying input arrival order yields varying equal groups.
21. **Deterministic-means-semantic:** an address or hash tie produces repeatable but unintended order.
22. **Parallel completion order:** worker finish time replaces original source order.
23. **Retry duplication:** external runs contain repeated identities after partial retry.
24. **Partial publication:** consumers observe an incomplete index vector or destination.
25. **Comparison-only benchmark:** record bytes and gather misses are omitted.
26. **One-view assumption:** repeated downstream traversal cost is excluded from the decision.

## Worked Examples

### Example 1

**Question:** Is output $(B,D,A,C,E)$ stable for input identities $(A,B,C,D,E)$ with keys $(2,1,2,1,2)$?

**Reasoning:** The key-1 input order is $B$ before $D$, and the output retains it. The key-2 input order is $A$ before $C$ before $E$, and the output retains it. Output keys are $(1,1,2,2,2)$ and every identity occurs once.

**Conclusion:** The output is ordered, a permutation, and stable.

### Example 2

**Question:** Left run is $((1,A),(2,B))$ and right run is $((1,C),(2,D))$. What does a stable merge produce?

**Reasoning:** At key $1$, $C$ is not strictly less than $A$, so the left tie wins. At key $2$, the same rule places $B$ before $D$.

**Conclusion:** The merge is $((1,A),(1,C),(2,B),(2,D))$; choosing right on equality would violate source order across the runs.

### Example 3

**Question:** Records $(A,2)$, $(B,1)$, $(A,1)$, $(B,2)$ must be ordered by letter first and number second. Which stable passes work?

**Reasoning:** Stable sort by number first gives $(B,1),(A,1),(A,2),(B,2)$. Stable sort by letter then groups the $A$ records and the $B$ records while preserving number order inside each group.

**Conclusion:** Least-significant number first, then most-significant letter, yields $(A,1),(A,2),(B,1),(B,2)$.

### Example 4

**Question:** Can an unstable sorter implement stability for keys $(4,2,4,2)$?

**Reasoning:** Decorate identities as $(4,0)$, $(2,1)$, $(4,2)$, $(2,3)$. These composite keys are unique. Sorting them produces index order $(1,3,0,2)$ regardless of native behavior on equal composite keys.

**Conclusion:** Yes, provided the sorter correctly orders the composite key and never falls through to payload comparison.

### Example 5

**Question:** For gather map $p=(1,3,0,2,4)$, what is the inverse and how many cycle destination writes are needed?

**Reasoning:** Set $q[p[j]]=j$, giving $q=(2,0,3,1,4)$. Its nontrivial cycle is $0\to2\to3\to1\to0$; index $4$ is fixed.

**Conclusion:** The in-place ledger uses four destination writes when fixed points are skipped, matching $n-f=5-1=4$.

### Example 6

**Question:** Compare one destination pass over ten million 512-byte records with one pass over eight-byte indices.

**Reasoning:**

$$
10^7\cdot512=5.12\text{ GB},
\qquad
10^7\cdot8=80\text{ MB}.
$$

The modeled ratio is $64$, before reads, cache effects, or later gathers.

**Conclusion:** Indirect sorting can greatly reduce sort-phase payload writes, but the complete workload still needs measurement.

### Example 7

**Question:** Why is reversing stable ascending output $(1,A),(1,B),(2,C),(2,D)$ not stable descending sorting?

**Reasoning:** Whole-array reversal produces $(2,D),(2,C),(1,B),(1,A)$. Each equal-key block has reversed input identity order.

**Conclusion:** Descending order must preserve equality with a stable descending policy; naive final reversal fails.

### Example 8

**Question:** Two workers stably sort adjacent source ranges containing equal key $7$. Which run wins a merge tie?

**Reasoning:** Every identity in the earlier source range originally preceded every identity in the later range. A stable merge therefore consumes the earlier range on equivalence, regardless of which worker finished first.

**Conclusion:** Source-range order, not scheduling order, composes global stability.

### Example 9

**Question:** Under a case-folded key, are records “Ada”, “ADA”, and “ada” equivalent even though their strings differ?

**Reasoning:** Their materialized case-folded keys are equal. Neither record precedes another under that comparator, so they share one equivalence class.

**Conclusion:** A stable sort retains their input identity order; language-level string inequality does not change the stability obligation.

### Example 10

**Question:** A service paginates records by score, and arrivals with equal scores can be ingested in different orders after replay. Is stable score sorting enough for repeatable pages?

**Reasoning:** Stability preserves whichever arrival order the replay produced. It does not establish the same tie order across different accepted input sequences.

**Conclusion:** Use an explicit durable tie key such as $(\text{score},\text{event sequence},\text{record ID})$ and version its semantics; stability alone is insufficient.

## Cross-Program Connections

- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) owns permutations, arrays, linked representations, iterators, and order-maintenance structures.
- [Programming Languages & Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) owns comparator laws, object identity, moves, aliases, exceptions, and generic library contracts.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) owns ORDER BY ties, sort operators, index scans, stable pagination, and external merge execution.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) owns distributed shuffles, partitioned order, deterministic replay, and immutable dataset versions.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) owns cache, translation, bandwidth, pointer chasing, and record-layout cost.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns property, differential, fault-injection, concurrency, and performance tests.

## References

1. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. [*Introduction to Algorithms*, fourth edition](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), MIT Press, 2022. Sorting correctness, stability, merge mechanics, counting/radix composition, and permutation foundations.
2. Donald E. Knuth. [*The Art of Computer Programming, Volume 3: Sorting and Searching*, second edition](https://www.informit.com/store/art-of-computer-programming-volume-3-sorting-and-searching-9780321635785), Addison-Wesley Professional, 1998. Sorting records, keys, stability, permutations, and movement analysis.
3. Paul E. Black, editor. [“stable”](https://www.nist.gov/dads/HTML/stable.html), NIST Dictionary of Algorithms and Data Structures, modified 2004; page formatted 2024; consulted 2026-09-04. Definition of preserving relative order among equal-key items and original-position tie construction.
4. Python Software Foundation. [“Sorting Techniques”](https://docs.python.org/3/howto/sorting.html), Python 3 documentation; consulted 2026-09-04. Current stable-sort guarantee, multi-pass ordering, key caching, reverse behavior, and decorate-sort-undecorate guidance.
5. Robert Sedgewick and Kevin Wayne. [“Merge”](https://algs4.cs.princeton.edu/code/javadoc/edu/princeton/cs/algs4/Merge.html), *Algorithms*, fourth-edition companion; consulted 2026-09-04. Stable mergesort and a documented index-sort permutation contract.
6. ISO C++ working draft. [“Requirements for stable algorithms”](https://eel.is/c++draft/algorithm.stable) and [“stable_sort”](https://eel.is/c++draft/stable.sort), current working draft; consulted 2026-09-04. Relative order of equivalent elements and a contemporary stable-sort library contract.
7. ISO/IEC JTC 1/SC 22/WG 14. [*ISO/IEC 9899:2024 working draft N3220*](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n3220.pdf), 2024. Current C language-library draft specifying that order among equal-comparing elements after qsort is unspecified.
8. ACM, IEEE Computer Society, and AAAI. [*Computer Science Curricula 2023: Algorithmic Foundations*](https://csed.acm.org/al-cs-core/), endorsed 2024; consulted 2026-09-04. Current curricular scope for sorting, correctness, efficiency, and empirical evaluation.

## Exercises

### Exercise 1

Input identities $A,B,C,D,E,F$ have keys $2,1,2,1,2,1$. Candidate output identities are $B,F,D,A,C,E$. Determine separately whether it is ordered, an identity permutation, and stable. Construct the stable gather map and inverse map for the correct output. State the comparator-equivalence classes.

### Exercise 2

Prove the standard two-run merge stable. State preconditions, output-prefix invariant, permutation preservation, cross-run tie rule, within-run identity preservation, progress, and termination. Give the smallest counterexample when the right run is chosen on equivalence.

### Exercise 3

A report must order records by department ascending, priority descending, and timestamp ascending. Derive the sequence of stable single-key passes and prove the final lexicographic order. Explain why reversing an ascending priority result is unsafe and give a one-sort decorated alternative.

### Exercise 4

Let the new-to-old gather map be

$$
p=(3,0,4,1,2).
$$

Compute its old-to-new inverse, decompose that inverse into cycles, materialize the arrangement symbolically from $(A,B,C,D,E)$, and count destination writes when fixed points are skipped. Specify validation and failure conditions required before in-place application.

### Exercise 5

Design a stable ordering subsystem for fifty million immutable 768-byte records. Users can request several reusable views with expensive 24-byte normalized keys; equal-key pagination must replay deterministically across machines. Memory is bounded, key extraction can fail, source versions change, and some consumers repeatedly scan every payload. Specify key/tie semantics, direct versus indirect representation, algorithm, memory model, publication, external/parallel stability, materialization policy, cancellation, validation, telemetry, and baselines.

## Answers to the Exercises

### Answer 1

The candidate's keys are

$$
(1,1,1,2,2,2),
$$

so it is ordered. It contains every identity exactly once, so it is a permutation. It is not stable: key-1 identities originally occur as $B,D,F$, but the candidate contains $B,F,D$. The key-2 order $A,C,E$ happens to remain stable.

The equivalence classes are

$$
\{B,D,F\}
\quad\text{and}\quad
\{A,C,E\}.
$$

The correct stable output is

$$
(B,D,F,A,C,E).
$$

Using old positions $A=0,\ldots,F=5$, its gather map is

$$
p=(1,3,5,0,2,4).
$$

Set $q[p[j]]=j$:

$$
q=(3,0,4,1,5,2).
$$

Both inverse laws hold, adjacent keys are nondecreasing, and ranks inside each equivalence class increase with original position.

### Answer 2

Assume $L$ and $R$ are individually ordered and stable, and all identities in $L$ precede all identities in $R$ in the original source. Maintain that the output prefix is ordered, contains exactly the consumed prefixes of $L$ and $R$, and is stable relative to those consumed identities.

If one run is empty, append from the other in its current order. Otherwise, take $R[j]$ only when

$$
R[j]\prec L[i].
$$

In every other case take $L[i]$. The chosen record is no greater than either remaining front, so appending preserves order. Exactly one front is consumed, so identity permutation of the consumed prefixes is preserved and the remaining-count variant decreases.

Within each run, front-only consumption preserves identity order. Across runs, if fronts are equivalent, the rule takes the left identity; because the left source interval preceded the right interval, cross-run stability holds. Exhaustion terminates after $|L|+|R|$ emissions. The final prefix is the complete stable permutation.

For the smallest counterexample, take left $((1,A))$ and right $((1,B))$, with $A$ originally before $B$. A rule that takes left only under strict less sends $B$ first on equivalence, producing $(B,A)$ and violating stability.

### Answer 3

The most-significant-to-least-significant specification is

$$
(\text{department ascending},
\text{priority descending},
\text{timestamp ascending}).
$$

Stable passes must run in reverse significance:

1. timestamp ascending;
2. priority descending with equality preserved;
3. department ascending.

After the first pass, records are ordered by timestamp. The stable priority pass orders distinct priorities descending and retains timestamp order inside each equal-priority class. The stable department pass orders distinct departments ascending and retains the established $(\text{priority descending},\text{timestamp ascending})$ suffix inside each equal-department class. Thus the final tuple order is correct.

Sorting priority ascending and reversing the entire result reverses the arrival order of equal-priority records, so it cannot serve as the stable descending pass. Use a stable descending comparator or a library reverse mode whose stability contract is explicit.

A one-sort alternative decorates record $r_i$ with

$$
(\text{department key},
\text{descending-priority encoding},
\text{timestamp key},
i),
$$

where every component encoding has the declared total order. The final $i$ implements original-order ties, and the payload is not compared.

### Answer 4

The gather relation is

$$
B[j]=A[p[j]],
$$

so the desired materialized order is

$$
(D,A,E,B,C).
$$

Compute the inverse with $q[p[j]]=j$:

$$
q=(1,3,4,0,2).
$$

As an old-to-new destination function, its cycles are

$$
(0\ 1\ 3)
\quad\text{and}\quad
(2\ 4).
$$

The first cycle sends $A$ to position $1$, $B$ to position $3$, and $D$ to position $0$. The second sends $C$ to position $4$ and $E$ to position $2$. There are no fixed points, so a one-temporary-per-cycle policy performs

$$
3+2=5
$$

destination writes, plus two initial temporary loads under the stated ledger.

Before mutation, validate that every entry is an integer in $[0,5)$ and appears once, construct and check both inverse laws, and ensure the map belongs to the current source snapshot. Define alias behavior and prohibit double application. If moves can throw or cancellation can occur inside a cycle, either accept a documented partially permuted state, journal recovery, or gather into private storage and publish only on success.

### Answer 5

Define the normalized semantic key and its normalization/collation version first. For cross-machine deterministic pagination, append a durable globally unique sequence or record identifier:

$$
(\text{normalized user key},
\text{durable sequence},
\text{record ID}).
$$

If user-key equivalence must retain source order, the durable sequence must encode that accepted source order. Do not use worker completion, addresses, or shard-local positions.

Keep records in an immutable versioned store. Extract each 24-byte key once into private storage under time, allocation, and cancellation limits. Record the source version and reject or restart publication if it changes. Store a new-to-old index vector with explicit width sufficient for fifty million positions. A stable external/index mergesort or a sort of composite $(K_i,i)$ entries can build each view; contiguous input-run ordinals and stable earlier-run-first multiway merges preserve source order.

For one index vector with eight-byte indices and cached keys, the modeled storage is

$$
50{,}000{,}000(8+24)
=1.6\text{ GB}.
$$

A second merge buffer raises it to

$$
50{,}000{,}000(8+8+24)
=2.0\text{ GB},
$$

before metadata, run files, and allocator overhead. Plan bounded external runs if that does not fit resident memory. Account for temporary disk, checksums, retry identity, and cleanup.

Validate every completed permutation's domain, uniqueness, inverse laws, adjacent composite order, and stable equal-user-key ranks. Differential-check bounded samples against trusted $(K_i,i)$ sorting. Publish the source-version identifier, key-policy version, and complete permutation atomically; never expose partial runs as a finished view.

Consumers that read a small projection or alternate among several orders should retain indirect views. A consumer that repeatedly scans every 768-byte payload should benchmark a private gather materialization against repeated random access. Materialize only after permutation validation, then atomically publish the complete destination. Preserve the canonical immutable source if several views remain necessary.

Place cancellation checks between bounded key batches, run-sort blocks, merge output blocks, validation blocks, and materialization chunks. Specify behavior for key failure, storage exhaustion, corrupt runs, retry, source-version mismatch, and cancelled publication.

Measure key calls/time/failures, key and index bytes, run/disk bytes, comparisons, merge fan-in, record bytes, cycles, cache and translation misses, indirect scan throughput, materialization time, source-version retries, cancellation latency, and p50/p99 end-to-end consumer time. Compare stable direct external sorting, stable indirect sorting, decorated unstable primitives, retained versus materialized views, and a database/index implementation under the same semantic and durability contract.
