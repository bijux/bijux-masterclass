---
module_id: ALGE-028
program: Algorithm Engineering
level: 1
module_number: 28
title: Transform-and-Conquer
status: complete
last_verified: 2026-09-04
---

# Transform-and-Conquer

## One-Page Review

### Governing question

When is it better to pay once to transform an instance, representation, or problem into a form whose structure makes the remaining computation simpler, faster, or more reusable?

### Essential definitions

- A **transformation** $\tau$ maps a source instance to a target instance with a declared semantic relationship.
- A **target solver** operates on the transformed instance under its own preconditions.
- A **lift** $\lambda$ maps a target answer or witness back to the source problem.
- **Instance simplification** changes the particular instance, as with presorting or elimination.
- **Representation change** stores the same logical information in a structure better suited to later operations.
- **Problem reduction** maps one problem to another whose solver can be reused.
- **Preprocessing** performs work before one or more later queries.
- **Information preservation** means every fact needed by the promised answer remains recoverable or derivable.
- A **semantic version** identifies the source data, transformation rules, target representation, and query contract together.
- **Break-even volume** is the smallest workload for which transformation plus later operations costs less than the baseline.

### Central model, mechanism, or theorem

For source instance $x$, compute

$$
x'=\tau(x),\qquad y'=B(x'),\qquad y=\lambda(x,y').
$$

Let $\mathcal S_A(x)$ and $\mathcal S_B(x')$ be valid source and target answers. Sound lifting requires

$$
y'\in\mathcal S_B(\tau(x))
\Longrightarrow
\lambda(x,y')\in\mathcal S_A(x).
$$

For all-witness completeness, every $y\in\mathcal S_A(x)$ must be represented by some valid $y'$ whose lift is $y$. Decision problems need only preserve nonemptiness. Optimization additionally needs objective and tie-order preservation.

The total cost is

$$
C_{\mathrm{total}}
=C_\tau+C_B+C_\lambda.
$$

For $q$ repeated queries, preprocessing cost $P$, transformed-query cost $Q$, and baseline cost $C_0$, transformation wins in the simple static model when

$$
P+qQ<qC_0
\Longleftrightarrow
q>\frac{P}{C_0-Q},
$$

provided $C_0>Q$. Build bytes, updates, invalidation, numerical error, and failure recovery remain part of the real comparison.

### Critical invariants

- The transformed object belongs to the target solver's input domain.
- The transform preserves every source distinction observable under the output contract.
- Target answers lift to valid source answers; required source answers are not lost.
- Original identities, ties, units, coordinate systems, and provenance survive reconstruction.
- Any discarded state has an equivalence or dominance proof, not just a smaller representation.
- Preprocessed state is bound to the exact source and semantic version it represents.
- Updates either maintain the representation invariant or invalidate/rebuild atomically.
- Numeric transforms state conditioning, precision, padding, and error policy.
- Cost claims include transformation, materialization, memory, I/O, updates, and query volume.
- Failure during build or publication cannot expose a partial representation as current.

### Common failures

Common failures include sorting away original identities; assuming ranks preserve distances; using a lossy canonicalization for exact equality; reducing in the wrong direction; proving decision equivalence but claiming all witnesses; forgetting to lift target answers; changing secondary tie order; applying a solver whose target preconditions are false; calling bottom-up heap construction $O(n\log n)$ by multiplying a worst per-node height by every node; using Gaussian elimination without pivot and numeric policy; omitting convolution padding; rounding an FFT result without an error bound; serving a stale index after source updates; counting only transformed query time; letting build scratch exceed memory; and publishing a partially built distributed representation.

### Compact example

For two-sum on values $(7,-2,4,7,1)$ with target 5, transform records to sorted `(value, original_index)` order:

$$
((-2,1),(1,4),(4,2),(7,0),(7,3)).
$$

Two pointers meet immediately at $-2+7=5$. Because the scan begins at the final equal-7 record, lifting yields source indices $(1,3)$ and replay confirms $-2+7=5$. Sorting values without indices could prove existence but could not return the promised source witness.

### Connections

[ALGE-013](./013-merge-sort.md) and [ALGE-014](./014-quicksort-and-partitioning.md) supply sorting transforms, [ALGE-017](./017-order-statistics-and-quickselect.md) offers a no-full-sort alternative, [ALGE-021](./021-divide-and-conquer.md) distinguishes recursive decomposition, [ALGE-023](./023-dynamic-programming-state-design.md) transforms histories into reusable states, and [ALGE-030](../ROADMAP.md) compares paradigms from problem structure.

## Governing Question

How do we design a transform–solve–lift pipeline whose semantic proof, numeric behavior, lifetime, and end-to-end cost justify changing the problem before solving it?

Transform-and-conquer moves effort to a structural boundary. Instead of repeatedly fighting an awkward input order, representation, or formulation, it constructs a form where the governing operation is easier. The transformation can expose adjacency, balance a search structure, diagonalize an algebraic operation, eliminate variables, or reuse an existing solver.

The name does not grant correctness. A fast target solver is irrelevant if the transformation loses an observable distinction, violates a target precondition, or cannot reconstruct a source answer. Nor is a faster query enough: build work, memory, updates, invalidation, and numerical error can outweigh the saving.

## Why This Matters

Many important speedups come less from a clever inner loop than from changing what that loop sees. Sorting turns arbitrary pair relationships into local or monotone scans. A heap turns repeated maximum selection into root access and logarithmic repair. Balanced search trees replace history-dependent height with a maintained structural bound. Coordinate compression converts sparse ordered keys into dense ranks. Elimination converts a simultaneous linear system into triangular solves. Fourier transforms convert convolution into pointwise multiplication. Reductions make a mature flow, matching, or satisfiability engine available to a new domain.

These techniques are also systems decisions. An index must track source versions. A transformed cache needs publication and rollback. Packed ranks need overflow and unknown-key behavior. Numerical transforms need conditioning and error evidence. External builds need scratch and I/O budgets. Distributed transformations need ownership and global completion.

The durable practice is to treat transformation as a verified interface: define what it preserves, what it intentionally changes, how answers return, and when its total lifecycle cost is favorable.

## Prerequisites and Retrieval

Retrieve:

- functions, relations, implication, equivalence, injectivity, and surjectivity;
- preconditions, postconditions, loop invariants, and composition of correctness arguments;
- asymptotic time, auxiliary and peak space, amortization, and break-even algebra;
- sorting, binary search, two pointers, heaps, binary search trees, and graph basics;
- stable identities, duplicate keys, deterministic ties, and witness reconstruction;
- linear equations, matrices, elementary row operations, and finite-precision arithmetic;
- polynomials, convolution, roots of unity, and complex numbers at an introductory level;
- graph matching and flow terminology at a conceptual level;
- indexes, snapshots, cache invalidation, serialization, external sorting, and atomic publication;
- bounded exhaustive oracles, metamorphic testing, benchmarks, and failure injection.

You should be able to distinguish a source problem's logical answer from the bytes or nodes used to represent it.

## Learning Objectives

After completing this module, you should be able to:

1. classify instance simplification, representation change, and problem reduction;
2. state transform, target-solver, and lift contracts with explicit source and target domains;
3. prove soundness, completeness, objective preservation, and tie preservation separately;
4. derive end-to-end time, peak-space, I/O, update, and break-even costs;
5. use presorting, coordinate compression, heap construction, and balanced representations safely;
6. explain exact versus finite-precision behavior in elimination and transform-domain methods;
7. reduce a domain problem to a reusable solver without reversing the reduction or losing witnesses;
8. govern versioning, updates, publication, cancellation, and distributed ownership of transformed state;
9. distinguish transform-and-conquer from divide and conquer, dynamic programming, search, and direct algorithms;
10. validate transformation semantics, solver preconditions, lifted answers, numeric error, and lifecycle performance independently.

## Core Exposition

### Start with the obstruction

A useful transformation removes a named obstruction:

- arbitrary order prevents local scanning;
- an unbalanced shape makes operations history-dependent;
- sparse or wide keys make direct arrays impractical;
- coupled equations prevent independent substitution;
- convolution couples every output coefficient to many input pairs;
- a domain formulation lacks a mature exact solver;
- repeated queries redo the same discovery work.

Write down the expensive or error-prone operation before selecting a representation. “Build an index” is not a goal; “answer exact membership for an immutable snapshot under a 5 ms tail budget” is. The latter exposes equality semantics, snapshot lifetime, query volume, memory, and failure status.

### Distinguish three transformation families

**Instance simplification** changes the given instance into an easier instance of the same or closely related problem. Presorting records before duplicate detection and applying elementary row operations before back substitution are examples.

**Representation change** keeps the logical object but changes how operations access it. A heap, balanced search tree, bitset, dense rank map, adjacency structure, or search index supplies new locality or operation costs. The representation invariant becomes part of every update.

**Problem reduction** maps an instance of source problem $A$ to target problem $B$, invokes a solver for $B$, and maps its result back. Bipartite matching can be represented as a unit-capacity flow instance. A reduction used to establish hardness may point opposite the direction needed to solve today's instance; always draw the data flow.

One design can use all three. An offline scheduling system may normalize records, sort events, compress timestamps, construct a graph, reduce a selection condition to flow, and lift chosen edges to domain identities. Each boundary needs its own contract.

### Specify transform, solve, and lift

Declare types:

$$
\tau:\mathcal X_A\to\mathcal X_B,
\qquad
B:\mathcal X_B\to\mathcal Y_B,
\qquad
\lambda:\mathcal X_A\times\mathcal Y_B\to\mathcal Y_A.
$$

Then state:

- source preconditions and observable output;
- target preconditions established by $\tau$;
- semantic relation between source and target instances;
- whether $\lambda$ needs original $x$, provenance stored in $\tau(x)$, or both;
- behavior for no answer, many answers, errors, and partial computation;
- primary objective and all secondary tie rules;
- numeric types, units, precision, and overflow policy;
- transformed-state identity, schema, and lifetime.

For a decision problem, it may suffice to prove

$$
\mathcal S_A(x)\ne\varnothing
\Longleftrightarrow
\mathcal S_B(\tau(x))\ne\varnothing.
$$

For witness return, this is insufficient: a constructive lift is required. For all witnesses, the lift must cover the source answer set without unwanted duplication. For optimization, a feasible target optimum must lift to a feasible source optimum under an objective-preserving or order-preserving relation.

### Derive lifecycle cost, not only query cost

For one call, write

$$
T(n)=T_\tau(n)+T_B(m)+T_\lambda(n,m),
$$

where $m=|\tau(x)|$ may differ greatly from $n=|x|$. A reduction can expand the instance; a compression can shrink stored keys while retaining side metadata; a sparse-to-dense conversion can allocate by range.

For a workload with build cost $P$, $q$ queries of cost $Q$, $u$ updates of maintenance cost $U$, invalidation/rebuild cost $R$, and baseline query/update costs $C_0,V_0$, compare

$$
P+qQ+uU+R
\quad\text{with}\quad
qC_0+uV_0.
$$

Peak memory includes source, target, scratch, indexes, provenance, and concurrent old/new versions:

$$
M_{\mathrm{peak}}
\ge M_{\mathrm{source}}+M_{\mathrm{target}}+M_{\mathrm{scratch}}
$$

when all coexist. A zero-downtime rebuild can add the old target again. Measure startup latency, steady query latency, update amplification, bytes, I/O, and rebuild tails separately.

### Use presorting to expose adjacency and monotonicity

To detect whether records contain duplicate keys, decorate each record with stable identity and sort by `(key, tie)`. Equal keys form a contiguous run. Therefore a duplicate exists exactly when some adjacent sorted keys are equal. The transform costs $O(n\log n)$ comparisons with a comparison sort, and the scan costs $O(n)$.

For two-sum, sorting numeric values exposes a monotone search. With left and right values $a_i\le a_j$:

- if $a_i+a_j<T$, every pair using $a_i$ and an index at most $j$ is too small, so advance $i$;
- if $a_i+a_j>T$, every pair using $a_j$ and an index at least $i$ is too large, so decrease $j$;
- equality yields a candidate witness.

The scan is linear after sorting. Stable source identities are payload: sorting only values can decide existence but cannot necessarily reconstruct required indices or distinguish equal-valued records.

### Execute a transform–solve–lift pipeline

This implementation transforms values into sorted identity-bearing records, applies a two-pointer target solver, and lifts a match to ordered source indices. Its contract is one deterministic witness induced by `(value, index)` order, not the lexicographically smallest source pair.

<!-- bijux-verify: {"id":"transformed-two-sum","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"transformed=((-2, 1), (1, 4), (4, 2), (7, 0), (7, 3))\nwitness=(1, 3)\nvalues=(-2, 7)\nsum=5\nsource_unchanged=True\nmissing=None\n","stderr":""}} -->
```python
def transformed_two_sum(values, target):
    records = sorted((value, index) for index, value in enumerate(values))
    left = 0
    right = len(records) - 1
    while left < right:
        total = records[left][0] + records[right][0]
        if total < target:
            left += 1
        elif total > target:
            right -= 1
        else:
            first = records[left][1]
            second = records[right][1]
            witness = tuple(sorted((first, second)))
            assert sum(values[index] for index in witness) == target
            return records, witness
    return records, None


values = (7, -2, 4, 7, 1)
before = values
records, witness = transformed_two_sum(values, 5)
_, missing = transformed_two_sum(values, 100)
print(f"transformed={tuple(records)}")
print(f"witness={witness}")
print(f"values={tuple(values[index] for index in witness)}")
print(f"sum={sum(values[index] for index in witness)}")
print(f"source_unchanged={values == before}")
print(f"missing={missing}")
```

The assertion replays the source predicate rather than trusting pointer arithmetic. An API should separate `found(witness)`, `absent`, and `incomplete(reason)` if transformation, sorting, or scanning can be interrupted.

### Compress coordinates without inventing geometry

For a finite set of observed keys $V$, define dense rank

$$
c(x)=|\{v\in V:v<x\}|.
$$

For $x,y\in V$,

$$
x<y\Longleftrightarrow c(x)<c(y)
$$

and

$$
x=y\Longleftrightarrow c(x)=c(y).
$$

This supports array-indexed counts, Fenwick or segment structures, and offline sweeps. It does not preserve subtraction or physical gaps. Values $(10,20,100)$ map to ranks $(0,1,2)$; source gaps 10 and 80 both become rank gap 1. Interval algorithms may need original endpoints, elementary gap cells, or stored coordinate widths.

The observed-domain condition matters. A new unseen key needs a defined insertion, overflow area, dynamic ordered structure, or rebuild. Never silently map it to the nearest existing rank.

### Transform an array into a heap bottom-up

An unordered array can be interpreted as a complete binary tree. Starting at the last internal node and sifting each node downward produces a heap because its children are already heap roots when processed. The invariant is: after processing index $i$, every subtree rooted at an index at least $i$ satisfies heap order.

The build is linear, despite one root sift costing $O(\log n)$. At most about $n/2^{h+1}$ nodes have height $h$, so total downward levels are bounded by

$$
\sum_{h\ge0}\frac{n}{2^{h+1}}O(h)
=O(n)\sum_{h\ge0}\frac{h}{2^{h+1}}
=O(n).
$$

Building by $n$ repeated heap insertions gives $O(n\log n)$ as a simple upper bound and different intermediate behavior. Bottom-up construction is a representation transformation specialized to a complete array shape; it does not sort the array.

### Maintain balance when the transformed form is dynamic

A sorted array gives excellent scans and binary search but can require linear movement per arbitrary insertion. A balanced search tree maintains ordered representation through local rotations or splits, keeping height logarithmic under its invariant. AVL balance, B-tree occupancy, and red-black coloring are different target contracts with different update, cache, and storage behavior.

The logical set or map remains the source abstraction. Node shape, separator copies, parent links, page sizes, and balance metadata are representation. They become observable if serialized directly, exposed through iteration ties, or used in unstable hashes. A transformation is safely replaceable only across behavior the API did not promise.

Bulk building and incremental maintenance are different workloads. A static sorted array may dominate for millions of reads and no writes. A B-tree-like page structure may dominate on block storage with updates. An in-memory hash index may dominate exact equality but cannot answer order queries without another representation.

### Reduce to an existing solver in the solving direction

Suppose source problem $A$ can be mapped to target problem $B$. A solving reduction needs an efficient $\tau$, a suitable solver for $B$, and a lift. To solve $A$ using $B$, arrows flow

$$
A\ \xrightarrow{\tau}\ B\ \xrightarrow{\text{solve}}\ y'
\ \xrightarrow{\lambda}\ y.
$$

A proof that $B$ reduces to $A$ says something different and does not automatically provide this algorithm.

For bipartite graph $G=(L\cup R,E)$, create a source vertex $s$, sink $t$, capacity-1 arcs from $s$ to each $u\in L$, capacity-1 arcs for every $(u,v)\in E$, and capacity-1 arcs from each $v\in R$ to $t$. Each integral unit-flow path $s\to u\to v\to t$ selects edge $(u,v)$. Vertex capacities ensure selected edges share no endpoint. Conversely, every matching routes one unit along each selected edge. Integral-capacity max flow therefore yields a matching of the same cardinality, and selected middle arcs lift to source identities.

This is an algorithmic modeling result, not the complexity-theory claim that one problem is hard. Preserve graph direction, capacities, parallel-edge identities, and the target solver's integral-flow guarantee.

### Treat elimination as an exact and numerical transformation

For exact arithmetic, swapping two equations, multiplying one equation by a nonzero scalar, or adding a multiple of one equation to another preserves the solution set. Gaussian elimination composes these invertible row transformations until an upper-triangular system permits back substitution. Rank tests then distinguish unique, multiple, and inconsistent systems.

Machine arithmetic changes the claim. Dividing by a zero pivot fails; dividing by a tiny pivot can amplify rounding. Partial pivoting selects a larger-magnitude available pivot in the column, but no short slogan proves accuracy for every matrix. State input scaling, precision, pivot policy, singularity/rank threshold, condition evidence, residual checks, and whether the guarantee is forward error, backward error, or only observed residual.

Never use exact `== 0` and an arbitrary epsilon interchangeably. An exact rational or finite-field solver has different domains and costs from a floating-point linear algebra library.

### Move convolution into a transform domain

For coefficient sequences $a$ and $b$, linear convolution is

$$
c_k=\sum_i a_i b_{k-i}.
$$

After padding to transform length $N\ge |a|+|b|-1$, the discrete Fourier transform satisfies

$$
\operatorname{DFT}(a*b)
=\operatorname{DFT}(a)\odot\operatorname{DFT}(b),
$$

where $\odot$ is pointwise multiplication. Forward transforms, $N$ multiplications, and an inverse transform compute convolution in $O(N\log N)$ arithmetic operations with a suitable FFT, instead of the direct $O(|a||b|)$ pair sum.

Padding is semantic: too short a transform computes cyclic wraparound rather than the requested linear convolution. Floating FFT results are approximate. Rounding to integers is justified only by a bound showing total error stays below the decision margin. Number-theoretic transforms and Chinese-remainder reconstruction can provide exact modular/integer routes when modulus, roots, coefficient bounds, and reconstruction range are proved.

### Use canonicalization only under a declared equivalence

A canonical form maps equivalent source objects to one representation so equality and caching become easier. Soundness requires canonical equality to imply source equivalence; completeness requires source-equivalent objects to canonicalize equally. If both hold, canonical form represents equivalence classes.

Case folding, Unicode normalization, path normalization, algebraic simplification, graph labeling, and JSON field reordering each preserve some semantics and change others. Security and identity contracts often care about the changed distinctions. Version the equivalence relation and retain original material when display, audit, signature verification, or exact reconstruction requires it.

Cryptographic hashes are usually fingerprints, not canonical proofs. A collision-resistant digest can make comparison practical under a threat model, but exact acceptance may still require length/domain binding or source replay.

### Transform online work into an offline sweep

When all updates and queries are known in advance, sort them by coordinate or time and sweep once while maintaining active state. The transform turns arbitrary query order into monotone progression. Correctness depends on event ordering at equal coordinates: for closed intervals, starts, point queries, and ends may need a different tie order than for half-open intervals.

Offline sorting can remove a complex dynamic index and improve locality. It also delays answers, requires a finite batch, and may be incompatible with low-latency streaming. “Same events” is not enough; snapshot boundaries and equal-time semantics are part of the transformed instance.

### Version, publish, and retire transformed state

A derived representation should carry at least source snapshot ID, transform/schema version, semantic parameters, build status, and integrity digest. Build privately, validate, then atomically publish one immutable version. Readers pin a version for the duration of a query. Retire old versions only after readers and rollback policy release them.

For updates, choose deliberately among:

- synchronous invariant-preserving maintenance;
- append-only deltas merged with a base representation;
- invalidation followed by rebuild;
- multi-version publication with bounded staleness;
- rejecting queries whose required freshness is unavailable.

Never mutate a current index partly and then mark it failed. A stale but explicitly versioned result may satisfy a contract; an unversioned mixture usually cannot.

### Engineer memory, I/O, concurrency, and security

Account for transformed record width, pointers, allocator overhead, indexes, provenance, sort/build scratch, spill runs, checksums, old/new versions, and per-worker buffers. External transformations should use governed run locations, bounded fan-in, cancellation cleanup, and recoverable manifests. Sequential scans can beat asymptotically attractive pointer structures when memory locality dominates.

Parallel builds need disjoint source ranges and a deterministic merge or reconciliation rule. Distributed builds need durable shard ownership, input/schema version agreement, retry-safe output identities, validation of every partition, and a global publication barrier. Locally complete shards do not make a complete index if one range is absent.

Treat untrusted inputs as resource and semantic adversaries. Pathological keys can unbalance an unprotected tree or hash table. Huge expansion can turn decompression or normalization into denial of service. Malformed numeric data can create NaN comparisons. Crafted canonicalization collisions can cross authorization boundaries. Apply size, time, memory, recursion, expansion, and tenant budgets before publication.

### Validate each boundary independently

For bounded inputs, compute source answers directly and compare transformed answers after lifting. Do not test only target solver output. Check:

1. $\tau(x)$ satisfies every target precondition;
2. recomputed transformed fields match stored fields;
3. each lifted target witness satisfies the original source predicate;
4. every direct source witness or optimum is represented as promised;
5. identities, multiplicities, and tie order survive round trips;
6. numerical residual/error policy holds on conditioned and adversarial cases;
7. every update preserves invariants or blocks publication;
8. interrupted, corrupt, partial, or stale builds cannot report current success.

Metamorphic properties include permuting source storage while preserving stable identities, applying an idempotent canonicalization twice, comparing multiple transform strategies, rebuilding from a snapshot after incremental updates, and checking that adding irrelevant isolated data does not change existing answers.

Measure build and lift time, query latency distribution, update amplification, transformed cardinality, record width, peak resident and scratch bytes, I/O, cache behavior, stale-version age, validation failures, retry work, and answer correspondence. A query-only benchmark cannot justify a lifecycle transformation.

### Use a reusable design worksheet

Before implementation, record:

1. source input, output, identity, multiplicity, and tie contract;
2. the named obstruction the transformation removes;
3. transformation family and exact source/target types;
4. source preconditions and target preconditions;
5. semantic preservation relation and intentionally changed distinctions;
6. target solver guarantee and failure behavior;
7. lift, provenance, and source-witness replay;
8. decision, witness, all-answer, or optimization proof obligations;
9. numeric domains, units, precision, conditioning, and overflow;
10. build, solve, lift, output, and update time;
11. source, target, scratch, old/new, and peak bytes;
12. query/update volume and break-even model;
13. snapshot, schema, semantic version, and invalidation rules;
14. concurrency, shard ownership, retry, and publication barrier;
15. bounded oracle, metamorphic tests, numeric checks, and failure injection;
16. telemetry, workload evidence, rollout gates, and rollback conditions.

## Definitions and Notation

- $\mathcal X_A$ and $\mathcal Y_A$ are source-instance and source-answer domains.
- $\mathcal X_B$ and $\mathcal Y_B$ are target-instance and target-answer domains.
- $\tau$ is the transformation; $B$ is the target solver; $\lambda$ is the source-answer lift.
- $\mathcal S_A(x)$ and $\mathcal S_B(x')$ are valid-answer sets for specific instances.
- A transform is **lossless for a contract** when every source distinction observable by that contract remains recoverable.
- A transform may be **lossy but sufficient** when discarded information cannot change the requested answer.
- A **decorated record** carries a transformed key plus identity, tie, or reconstruction payload.
- A **canonical form** is one declared representative of an equivalence class.
- A **representation invariant** relates concrete transformed state to its logical source abstraction.
- **Materialization** stores transformed results; a streaming transform produces them on demand.
- $P,Q,U,R$ denote build, query, update-maintenance, and rebuild/invalidation costs in the workload model.
- $C_0,V_0$ denote baseline query and update costs without the transformation.
- A **source snapshot** is the immutable logical revision from which transformed state was built.
- **Atomic publication** makes either the old complete representation or the new complete representation visible, never an unvalidated mixture.
- A **residual** measures how well a computed numeric answer satisfies the original equation; it is not automatically a bound on answer error.
- `found`, `absent`, `incomplete`, and `error` are distinct outcomes. Only complete semantic coverage can justify `absent`.

Transformation is contract-relative. Sorting is lossless for a multiset if multiplicity remains, but not for original sequence order unless identities or positions are retained. Coordinate ranks are sufficient for comparisons within the observed domain, but lossy for metric distance. Floating transforms approximate real or complex arithmetic and need an error contract rather than the word “lossless.”

## Mechanisms, Invariants, or Proof Structure

### Composition theorem

Assume $\tau(x)$ satisfies every precondition of $B$. Assume $B$ returns only $y'\in\mathcal S_B(\tau(x))$, and assume

$$
y'\in\mathcal S_B(\tau(x))
\Longrightarrow
\lambda(x,y')\in\mathcal S_A(x).
$$

Then every successfully lifted answer is source-sound. The proof is direct function composition: solver validity supplies the antecedent, and lift soundness supplies the source postcondition.

For source completeness, also require

$$
\forall y\in\mathcal S_A(x)\quad
\exists y'\in\mathcal S_B(\tau(x)):
\lambda(x,y')=y
$$

under an all-witness contract. If only one representative is required, replace equality by the contract's equivalence. Termination requires terminating transform, target solver, and lift; semantic correctness does not by itself bound any of their work.

### Optimization preservation

Let source and target objectives be $f_A$ and $f_B$. One sufficient pattern is feasible-answer coverage plus a strictly increasing mapping $\phi$ such that

$$
f_A(\lambda(x,y'))=\phi(f_B(y'))
$$

for every target-feasible $y'$. If $y'^*$ minimizes $f_B$ but its lift were not source-optimal, completeness would provide a target answer for a better source answer. Strict monotonicity would make that target objective smaller than $f_B(y'^*)$, a contradiction.

This condition is stronger than necessary but exposes the obligation. Additive constants and positive scaling preserve order; negation reverses minimum and maximum; rounding can collapse or reverse close objectives. Secondary ties need their own order preservation or an explicit post-lift selection.

### Presorted-adjacency proof

Suppose two source records share key $k$. In nondecreasing key order, no different key can lie strictly between those two positions without violating the order on one side. Thus every equal-key class is contiguous, and any class of size at least two contains an adjacent equal pair. Conversely, adjacent equal keys are plainly duplicates. Decoration preserves the identities needed to lift that adjacency to source records.

For two pointers, the invariant is that every discarded row or column contains no target-sum pair. If $a_i+a_j<T$, then $a_i+a_k\le a_i+a_j<T$ for every $k\le j$. If $a_i+a_j>T$, then $a_k+a_j\ge a_i+a_j>T$ for every $k\ge i$. Each move is therefore complete for existence.

### Bottom-up heap work proof

Let a sift from a node of height $h$ cost at most $ch+d$. A complete binary-tree array has at most $\lceil n/2^{h+1}\rceil$ nodes of height $h$ up to a constant boundary term. The height-weighted part is bounded by

$$
cn\sum_{h\ge0}\frac{h}{2^{h+1}}.
$$

Using

$$
\sum_{h\ge0}hx^h=\frac{x}{(1-x)^2}
\qquad (|x|<1),
$$

the series at $x=1/2$, including the additional factor $1/2$, equals 1. The constant per-node work contributes $O(n)$. Therefore bottom-up construction is $O(n)$; applying the root's $O(\log n)$ bound to all nodes is a valid but loose upper bound.

### Coordinate-rank preservation proof

For observed distinct keys in sorted order $v_0<\cdots<v_{k-1}$, define $c(v_i)=i$. Then $i<j$ exactly when $v_i<v_j$, and equal source keys select the same unique rank. This proves order and equality preservation.

No analogous distance theorem holds. A strictly increasing map need not be affine. The counterexample $(10,20,100)\mapsto(0,1,2)$ maps unequal gaps 10 and 80 to equal gaps. Algorithms using lengths, interpolation, rates, or physical duration need the original values or separately transformed measures.

### Matching-to-flow proof

Given a matching $M$, route one unit on $s\to u\to v\to t$ for every $(u,v)\in M$. No capacity-1 endpoint arc is reused, so the flow is feasible and has value $|M|$.

Given an integral flow, decompose each unit leaving $s$ through some $u\to v$ to $t$. Capacity 1 on endpoint arcs prevents two selected middle arcs sharing $u$ or $v$, so they form a matching with cardinality equal to flow value. The two constructions preserve optimum cardinality. Fractional output would not directly lift to a matching; the target solver's integrality property is essential.

### Numerical evidence hierarchy

For a computed solution $\widehat x$ to $Ax=b$, the residual is

$$
r=b-A\widehat x.
$$

A scale-aware residual indicator can use

$$
\eta=
\frac{\lVert r\rVert}
{\lVert A\rVert\lVert\widehat x\rVert+\lVert b\rVert},
$$

with an explicit convention when the denominator is zero. Small $\eta$ supports a backward-error interpretation: the computed result nearly solves nearby data under additional analysis. It does not imply small forward error $\lVert\widehat x-x\rVert$ when $A$ is ill-conditioned.

For FFT-based integer convolution, testing that imaginary parts look small is empirical evidence, not a universal rounding proof. Exact recovery needs coefficient and accumulated-error bounds below one half, or an exact modular route with enough reconstruction range.

### Publication-state invariant

| State | May serve as current? | Required transition evidence |
|---|---:|---|
| allocated | no | source/schema identity recorded |
| building | no | assigned ranges and bounded resources |
| built | no | every range complete and checksummed |
| validating | no | semantic, structural, numeric, and oracle checks |
| published | yes | atomic pointer/version swap |
| superseded | pinned readers only | replacement is published |
| failed | no | error retained; partial state quarantined |
| retired | no | readers released; governed deletion |

Retries use stable build and shard identities. A worker's local completion advances only its range. Publication requires global source coverage, target invariants, and semantic validation under one version.

## Alternatives and Trade-Offs

| Choice | Strength | Cost or risk |
|---|---|---|
| direct one-shot algorithm | avoids build, provenance, and invalidation | repeats structural work and may have worse per-call cost |
| presort then scan | exposes adjacency and monotonicity; compact | $O(n\log n)$ build, identity/tie handling, mutation |
| selection or hashing | can avoid full order when query needs less | different worst-case, equality, memory, and adversarial contracts |
| sorted array representation | excellent locality, binary search, range scan | arbitrary insertion can move $O(n)$ elements |
| balanced tree | logarithmic governed search and updates | pointers/pages, invariant maintenance, lower locality |
| heap | efficient repeated extremum and repair | no full order or fast arbitrary search |
| coordinate compression | dense arrays and compact order keys | observed-domain rebuilds; distances not preserved |
| exact elimination/transform | algebraic equivalence | coefficient growth and high exact-arithmetic cost |
| floating transform | high performance and mature libraries | conditioning, rounding, reproducibility, and error contract |
| problem reduction | reuses a verified powerful solver | instance expansion, impedance mismatch, and lift complexity |
| materialized index | low repeated-query latency | build, bytes, freshness, update amplification |
| streaming transform | bounded storage and fresh computation | repeats work and may raise latency |

Presorting for one membership query is often inferior to a direct linear scan: both must read the input, and sorting adds work. Presorting for many binary searches can win, but hashing may better fit exact equality. Full order is valuable only when later operations consume it.

A representation can improve asymptotic operation bounds yet lose on realistic sizes through allocation and locality. Conversely, a linear scan over compact memory may beat a tree lookup for small collections. State the machine and workload, then measure after correctness correspondence is established.

Problem reduction should minimize more than target instance size. Consider solver startup, target expressiveness, witness mapping, numeric encoding, licensing or operational boundaries, incremental behavior, explainability, and failure isolation. A custom direct solver can be simpler even when a reduction exists.

For static transforms, the simple break-even equation is informative. For dynamic data, include updates and freshness. If $Q\ge C_0$, no positive query count repays a positive build cost in that model. If source revisions arrive faster than builds complete, an eventually rebuilt representation may never satisfy the required freshness.

## Failure Modes and Misconceptions

1. **Transformation by fashion:** no named obstruction or workload justifies the new form.
2. **Wrong source contract:** existence is implemented when indices, all witnesses, or ties were required.
3. **Target precondition gap:** transformed data violate ordering, uniqueness, capacity, or numeric assumptions.
4. **Soundness only:** target answers lift correctly, but some source answers disappear.
5. **Completeness only:** every source answer is represented, but false target answers are emitted.
6. **Missing lift:** a target objective is returned without a source witness.
7. **Identity loss:** sorting or deduplication drops original record identities.
8. **Multiplicity loss:** a set representation replaces a source multiset.
9. **Tie drift:** target ordering chooses a different promised secondary result.
10. **Wrong reduction direction:** a hardness arrow is mistaken for a solving pipeline.
11. **Objective reversal:** negation or sign changes minimum to maximum without updating the solver contract.
12. **Rank-as-distance:** dense coordinate differences are treated as physical differences.
13. **Unknown rank:** a new coordinate is silently forced into an old observed-domain map.
14. **Partial heap myth:** heap order is confused with total sorted order.
15. **Heap-build overcount:** worst root height is charged to every node as if tight.
16. **Unbalanced tree exposure:** input history destroys an unprotected search-tree bound.
17. **Invariant-free update:** a node/page change violates ordering, balance, or occupancy.
18. **Zero-pivot division:** elimination proceeds without row exchange or singularity handling.
19. **Residual confusion:** a small residual is called small forward error for an ill-conditioned system.
20. **Arbitrary epsilon:** exact singularity and approximate rank policy are mixed.
21. **Cyclic convolution:** insufficient padding aliases high coefficients to low positions.
22. **Blind FFT rounding:** approximate coefficients are rounded without a recovery bound.
23. **Insufficient modulus:** exact modular convolution wraps beyond reconstruction range.
24. **Lossy canonicalization:** distinct authorized identities collapse to one key.
25. **Digest as proof:** a fingerprint match replaces exact replay outside its threat model.
26. **Query-only accounting:** build, lift, update, invalidation, and bytes are omitted.
27. **Peak-space omission:** source, target, scratch, and old/new versions coexist unexpectedly.
28. **Stale representation:** source changes without maintenance, invalidation, or visible version.
29. **Partial publication:** readers observe mixed build ranges or schema revisions.
30. **Local completion:** a missing distributed shard is treated as a globally valid index.

## Worked Examples

### Example 1

**Question:** How does the executable transform two-sum instance $(7,-2,4,7,1)$ for target 5?

**Reasoning:** Decoration and sorting produce $((-2,1),(1,4),(4,2),(7,0),(7,3))$. The outer records $(-2,1)$ and $(7,3)$ sum to 5, so the implementation returns source indices $(1,3)$. Index 0 holds another 7 and gives valid pair $(0,1)$, but the endpoint policy does not promise lexicographic minimization.

**Conclusion:** A transformation proof must follow the exact implementation and tie policy, not only the mathematical value pair.

### Example 2

**Question:** Why does sorting make duplicate detection an adjacent scan?

**Reasoning:** In sorted keys $(2,4,4,9)$, the two 4s are adjacent. More generally, if equal keys had a different key between them, that middle key would need to be both at least and at most the equal key; it would belong to the same equal-key run.

**Conclusion:** Presorting turns a global “any equal pair” relation into a local adjacency predicate.

### Example 3

**Question:** Can compressed ranks replace timestamps in duration arithmetic?

**Reasoning:** Timestamps $(10,20,100)$ map to ranks $(0,1,2)$. The original durations are 10 and 80, while both rank differences are 1.

**Conclusion:** Coordinate compression preserves order and equality, not metric distance.

### Example 4

**Question:** Why can bottom-up heap construction be linear on a 15-node complete tree?

**Reasoning:** Eight leaves require no downward movement. At most four height-1 nodes contribute four levels, two height-2 nodes contribute four, and one height-3 root contributes three: at most 11 downward levels under this coarse accounting, plus constant work per node.

**Conclusion:** Most nodes are near the leaves; charging logarithmic height to every node is loose.

### Example 5

**Question:** A static index costs 120 ms to build, baseline lookup costs 8 ms, and indexed lookup costs 1.5 ms. When does it break even?

**Reasoning:** Require

$$
120+1.5q<8q
\Longleftrightarrow
q>\frac{120}{6.5}\approx18.46.
$$

Thus the first integer volume that strictly wins is 19 queries. At 18 queries, baseline is 144 ms while transformed cost is 147 ms; at 19, they are 152 ms and 148.5 ms.

**Conclusion:** Preprocessing pays only under a workload and lifetime model.

### Example 6

**Question:** Should a dynamic ordered collection always be transformed into a sorted array?

**Reasoning:** Binary search is logarithmic and scans are compact, but inserting near the front can shift linearly many elements. A balanced tree adds metadata and pointer/page costs while maintaining logarithmic search and updates.

**Conclusion:** Choose the representation from the operation mix, locality, and update contract.

### Example 7

**Question:** Solve $0x+y=1$ and $x+y=2$ by elimination.

**Reasoning:** Using the first row as a pivot would divide by zero. Swap the rows to obtain $x+y=2$ above $y=1$. Back substitution gives $y=1$ and $x=1$, which replay satisfies in both original equations.

**Conclusion:** Row swapping preserves the exact solution set and establishes a usable pivot; finite precision still needs a pivot and error policy.

### Example 8

**Question:** What is the linear convolution of $(1,2,1)$ and $(1,-1)$?

**Reasoning:** Coefficient expansion gives

$$
(1+2z+z^2)(1-z)=1+z-z^2-z^3,
$$

so the result is $(1,1,-1,-1)$. A transform length below $3+2-1=4$ would compute cyclic aliasing rather than these four coefficients.

**Conclusion:** Transform-domain multiplication needs semantic padding and source-domain replay.

### Example 9

**Question:** How does matching reduce to flow for edges $\{(a,1),(a,2),(b,2)\}$?

**Reasoning:** Unit endpoint capacities allow two disjoint paths, $s\to a\to1\to t$ and $s\to b\to2\to t$. The selected middle arcs lift to matching $\{(a,1),(b,2)\}$ of size 2. No matching can exceed two because the left side has two vertices.

**Conclusion:** Feasible integral flows and matchings correspond with equal cardinality.

### Example 10

**Question:** Why is an index built from snapshot 41 unsafe after source snapshot 42 changes one key?

**Reasoning:** The old representation may return a removed record or miss a new one while remaining structurally valid. Without visible source version and freshness rules, the caller cannot distinguish a permitted stale answer from corruption.

**Conclusion:** Representation invariants and source-version correspondence are separate obligations.

## Cross-Program Connections

- [Theory of Computation & Complexity](../../15-theory-of-computation-and-complexity/ROADMAP.md) owns formal reductions, encoded-size effects, completeness, and hardness direction.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) owns heap, balanced-tree, compressed-index, hash-table, bitset, and representation internals.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) owns indexes, query rewrites, materialization, external sorting, snapshots, and cost-based selection.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) owns locality, vectorization, memory bandwidth, layout, numeric hardware, and accelerator behavior.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns canonicalization boundaries, collision threats, decompression limits, authorization identity, and sensitive provenance.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) owns versioned publication, shard leases, retries, global completion, and replica freshness.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns source-oracle correspondence, metamorphic tests, numeric test matrices, failure injection, and rollout evidence.

## References

1. Anany Levitin. [*Introduction to the Design and Analysis of Algorithms*, third edition](https://www.pearson.com/en-gb/subject-catalog/p/introduction-to-the-design-and-analysis-of-algorithms/P200000003403/9780137541133), Pearson, current eText ISBN 9780137541133, published 2021. Authoritative classification and textbook treatment of transform-and-conquer.
2. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. [*Introduction to Algorithms*, fourth edition](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), MIT Press, 2022. Authoritative foundations for sorting, heaps, balanced trees, hashing, graphs, and reductions.
3. G. M. Adel'son-Vel'skii and E. M. Landis. [“An Algorithm for Organization of Information”](https://www.mathnet.ru/eng/dan26964), *Doklady Akademii Nauk SSSR* 146(2), 1962, pp. 263–266. Primary balanced-search-tree work; also translated in *Soviet Mathematics Doklady* 3.
4. Rudolf Bayer and Edward M. McCreight. [“Organization and Maintenance of Large Ordered Indexes”](https://doi.org/10.1007/BF00288683), *Acta Informatica* 1, 1972, pp. 173–189. Primary B-tree representation, maintenance, and external-storage analysis.
5. James W. Cooley and John W. Tukey. [“An Algorithm for the Machine Calculation of Complex Fourier Series”](https://doi.org/10.2307/2003354), *Mathematics of Computation* 19(90), 1965, pp. 297–301. Primary modern FFT algorithm paper.
6. Alan M. Turing. [“Rounding-Off Errors in Matrix Processes”](https://doi.org/10.1093/qjmam/1.1.287), *Quarterly Journal of Mechanics and Applied Mathematics* 1(1), 1948, pp. 287–308. Primary analysis of elimination and rounding error.
7. Nicholas J. Higham. [*Accuracy and Stability of Numerical Algorithms*, second edition](https://doi.org/10.1137/1.9780898718027), SIAM, 2002. Authoritative finite-precision, linear algebra, FFT, and software analysis.
8. Richard M. Karp. [“Reducibility Among Combinatorial Problems”](https://doi.org/10.1007/978-1-4684-2001-2_9), in Raymond E. Miller and James W. Thatcher, editors, *Complexity of Computer Computations*, Plenum Press, 1972, pp. 85–103. Primary reduction framework and directionality context.
9. Alok Aggarwal and Jeffrey Scott Vitter. [“The Input/Output Complexity of Sorting and Related Problems”](https://doi.org/10.1145/48529.48535), *Communications of the ACM* 31(9), 1988, pp. 1116–1127. Foundational external-memory sorting and I/O model.
10. ACM, IEEE Computer Society, and AAAI. [*Computer Science Curricula 2023: Algorithmic Foundations*](https://csed.acm.org/algorithms-and-complexity/), endorsed 2024; consulted 2026-09-04. Current curricular scope for design strategies, transformations, data structures, correctness, and evaluation.

## Exercises

### Exercise 1

Trace the executable two-sum transform on $(9,1,6,-2,4)$ with target 7. Give sorted identity-bearing records, every pointer comparison, the returned source indices, replay, and the output claim it does not make.

### Exercise 2

Prove a generic transform–solve–lift pipeline sound and complete for all witnesses. Then add sufficient conditions for minimum-objective preservation and explain why decision equivalence alone cannot justify source witness or tie claims.

### Exercise 3

Diagnose three defects: compressed coordinate differences are used as durations; an index remains published after an unmaintained source update; and integer convolution coefficients are rounded from a floating FFT without an error bound. Give a counterexample or failure chain, durable repair, and targeted evidence for each.

### Exercise 4

A derived representation costs $P=350$ ms to build, reduces each query from $C_0=12$ ms to $Q=2$ ms, and costs $U=5$ ms per update versus baseline $V_0=1$ ms. Ignore rebuild cost first: compute the static strict break-even query count, then compare transformed and baseline cost for (a) 50 queries and 5 updates and (b) 50 queries and 100 updates. State what additional evidence the arithmetic omits.

### Exercise 5

A service repeatedly answers exact anagram queries over a versioned dictionary. Define “anagram” as equality of NFC-normalized, case-sensitive Unicode code-point multisets. Design a transform-and-conquer solution. Specify transform, target representation, lift, duplicate and tie semantics, proof, costs, updates/publication, adversarial controls, telemetry, exhaustive bounded oracle, metamorphic tests, and conditions favoring a direct scan instead.

## Answers to the Exercises

### Answer 1

Decoration and sorting produce

$$
((-2,3),(1,1),(4,4),(6,2),(9,0)).
$$

Pointers begin at $-2$ and 9; their sum is 7, so the first comparison succeeds. Lifting indices 3 and 0 and sorting the pair returns $(0,3)$. Source replay gives $9+(-2)=7$.

The algorithm promises one deterministic witness induced by sorted `(value, index)` order and endpoint movement. It does not promise minimum cardinality beyond the inherent two items, lexicographically smallest source pair across every possible match, or all pairs. If any of those are required, the scan and duplicate/tie handling must implement that contract explicitly.

### Answer 2

Let $\tau$ map every source-valid instance into the target solver's domain. Require the target solver to emit exactly its promised valid target answers. Require lift soundness:

$$
y'\in\mathcal S_B(\tau(x))
\Longrightarrow
\lambda(x,y')\in\mathcal S_A(x).
$$

Then any emitted source answer is valid. For all-witness completeness require, for every $y\in\mathcal S_A(x)$, some target-valid $y'$ with $\lambda(x,y')=y$, and require the target enumeration to reach it. If duplicate-free output is promised, also require that target representations and lifting do not emit the same source identity twice, or apply a proved canonical deduplication. Termination composes only if transform, solver, lift, and finite output all terminate.

For minimization, one sufficient condition is complete feasible-answer coverage and a strictly increasing $\phi$ with

$$
f_A(\lambda(x,y'))=\phi(f_B(y')).
$$

A better source answer would then correspond to a target answer with a strictly better target objective, contradicting target optimality. Preserve the full secondary tie tuple similarly or select ties after lifting from all primary optima.

Decision equivalence states only that an answer exists on one side exactly when one exists on the other. It supplies neither a constructive target-to-source map nor coverage of every witness. It also says nothing about identity, multiplicity, objective value, or secondary order.

### Answer 3

For rank distance, map timestamps $(10,20,100)$ to $(0,1,2)$. Rank differences report both adjacent durations as 1 although source durations are 10 and 80. Use ranks only for order/index operations; retain original coordinates or transformed cell widths for metric calculations. Test every pair's comparison equivalence and include deliberately unequal gaps, duplicate endpoints, unseen coordinates, and open/closed interval boundaries.

For the stale index, suppose snapshot 42 removes key $k$ after an index for snapshot 41 is published. The structurally valid old index still returns a record forbidden by the current contract. Maintain updates synchronously, merge a versioned delta, or invalidate and privately rebuild. Bind queries to a visible source/index version and atomically publish only validated builds. Race updates through every build stage, pin old readers, lose notifications, retry shards, and assert freshness policy plus source-oracle correspondence.

For FFT rounding, large coefficients or an ill-scaled transform can accumulate error beyond one half, so nearest-integer rounding can change a coefficient. Establish an analytic and implementation-specific error envelope under bounded inputs, use higher precision with verified recovery margin, or choose an NTT/CRT route with proven roots, modulus products, and signed reconstruction range. Compare with arbitrary-precision direct convolution across extrema and adversarial cancellation; perturb transform results around half-integer thresholds and require refusal when the certificate is insufficient.

### Answer 4

Ignoring updates, require

$$
350+2q<12q
\Longleftrightarrow
q>35.
$$

The first integer query count that strictly wins is 36.

For 50 queries and 5 updates, transformed cost is

$$
350+50(2)+5(5)=475\text{ ms},
$$

while baseline cost is

$$
50(12)+5(1)=605\text{ ms}.
$$

The transformation wins by 130 ms in this model.

For 50 queries and 100 updates, transformed cost is

$$
350+100+500=950\text{ ms},
$$

while baseline cost is

$$
600+100=700\text{ ms}.
$$

The update-heavy baseline wins by 250 ms.

The model omits latency distributions, batchability, rebuild and invalidation, concurrent old/new bytes, cache behavior, write amplification, source arrival patterns, freshness, failures, contention, target cardinality, query skew, and whether update/query results remain semantically identical. Measure these under representative version lifetimes and resource limits.

### Answer 5

Assign each dictionary entry a stable word identity and immutable dictionary version. The source contract first NFC-normalizes each word, remains case-sensitive, and defines an anagram by equal multisets of normalized Unicode code points. Reject or explicitly handle invalid text before transformation.

Transform a normalized word to a canonical signature: sort its code points and encode the length plus an unambiguous sequence of scalar values, or store a canonical frequency vector/map. The target representation maps each signature to an identity-bearing run of dictionary entries ordered by the promised tie key. A query undergoes the identical normalization/signature transform, performs exact signature lookup, and lifts stored identities to original dictionary entries. Replay normalization and multiset equality before publication when corruption or representation mismatch is in scope.

Soundness follows because equal canonical code-point sequences have equal code-point multiplicities. Completeness follows because any two source anagrams normalize to the same multiset and sorting that multiset yields the same signature. Stable identity runs preserve duplicates. A find-one contract returns the first declared tie; all-results returns the full run; count-only returns its checked length. NFC and case sensitivity are semantic parameters, not incidental library defaults.

If a word has length $k$, comparison sorting costs $O(k\log k)$, while a frequency construction can be $O(k)$ expected or ordered-map dependent. Building costs total input transformation plus index construction and bytes; queries cost normalization, signature creation, and lookup plus output. Large result runs add unavoidable output cost.

Build against one source snapshot and Unicode/normalization implementation version, validate privately, and atomically publish. Updates either maintain one signature run transactionally or create a new immutable version; changing normalization semantics requires rebuild. Readers pin a version. Failed or partial shards cannot answer exhaustive absence.

Limit word length, normalized expansion, query rate, result size, hash work, and per-tenant memory. Use collision-resilient maps or sorted signatures, unambiguous encoding, and exact-key comparison after any fingerprint. Avoid logging sensitive source words; structural telemetry can record lengths and run sizes.

Record build time, normalized code points, distinct signatures, duplicate-run distribution, query and lift latency, output size, bytes, expansion rejects, collision probes, stale-version age, update lag, retries, and source-replay failures. For a bounded Unicode alphabet and short strings, enumerate every string, normalize with an independent oracle where available, compare every pair's direct multiset relation with signature equality, and compare query result identity sets. Metamorphic tests permute code points, apply NFC twice, permute dictionary storage while retaining identities, add a duplicate word, change case, and inject canonically equivalent composed/decomposed sequences.

A direct scan is preferable for a tiny dictionary, a one-off query, an update rate that prevents break-even, a freshness contract incompatible with rebuild lag, or a memory budget that cannot hold the index. The choice follows measured lifecycle cost after semantic correspondence passes.
