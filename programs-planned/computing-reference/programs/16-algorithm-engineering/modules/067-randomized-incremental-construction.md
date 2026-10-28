---
module_id: ALGE-067
program: Algorithm Engineering
level: 2
module_number: 67
title: Randomized Incremental Construction
status: complete
last_verified: 2026-09-05
---

# Randomized Incremental Construction

## One-Page Review

### Governing question

How can a structure be built one object at a time in random order so that every update is correct for the objects already seen, while backward analysis turns local structural complexity into an expected total-work bound?

### Essential definitions

- A **randomized incremental construction** (RIC) chooses a uniformly random permutation of a fixed input set, then applies a deterministic insertion rule.
- The **prefix set** $R_i$ is the unordered set of the first $i$ objects; the **last object** $x_i$ is uniform in $R_i$ when conditioned on $R_i$.
- A **feature** is a primitive part of the maintained structure, such as a search-tree edge, hull edge, trapezoid, or Delaunay triangle.
- A feature's **defining set** is the smallest input subset that determines it; its **conflict set** contains uninserted objects that would invalidate it.
- A **conflict region** is the connected or otherwise enumerable set of current features destroyed by an insertion.
- A **history DAG** retains replacement relationships so a later object can be located without searching the current structure from scratch.
- **Backward analysis** studies the forward insertion of $x_i$ by deleting a uniformly random member from the completed prefix structure on $R_i$.
- **General position** excludes degeneracies such as collinearity or cocircularity; an implementation must replace that assumption with an explicit tie policy when real data can be degenerate.

### Central model, mechanism, or theorem

Condition on the event $R_i=S$ for a particular $i$-element subset. Every ordering of $S$ is equally likely, so each $x\in S$ has probability $1/i$ of being last. If $b(S,x)$ counts the primitive structural changes exposed by deleting $x$ from the structure on $S$, then the expected structural update cost is

$$
\mathbb E[c_i\mid R_i=S]=\frac1i\sum_{x\in S}b(S,x).
$$

Consequently, if the sum of deletion degrees is at most $g(i)$ for every $S$, then the expected update cost is at most $g(i)/i$. Summing these bounds controls structural work. Location cost, predicate cost, and memory must be accounted for separately.

For a random binary-search tree on distinct ranks $1,\ldots,n$, key $a$ is an ancestor of key $b$ exactly when it is the earliest inserted key in the interval between them. That probability is $1/(|a-b|+1)$. Hence the expected sum of node depths is

$$
2(n+1)H_n-4n=\Theta(n\log n),
$$

although a sorted insertion order produces a chain with $n(n-1)/2$ comparisons.

### Critical invariants

- After insertion $i$, the maintained object is exactly the specified structure for $R_i$.
- The permutation contains every canonical input identity exactly once.
- Every destroyed feature is in the located conflict region; every surviving feature remains valid.
- The boundary between destroyed and surviving features is complete and consistently oriented.
- Every new feature has valid defining objects and accurate conflict or history references.
- Random order is used only where the proof assumes it; retries, parallel batches, and filtering do not silently bias it.
- Exact or certified predicates determine topology; approximate coordinates may be used only behind a correctness-preserving filter.
- Expected structural work, search work, worst-case work, and observed runtime are reported as different claims.

### Common failures

Common failures include treating a shuffled stream as independent samples; analyzing an online adversarial arrival order as a random permutation; conditioning on the prefix order instead of only its set; charging location work to a structural bound; deleting conflict features before preserving their boundary; using floating signs without a degeneracy policy; assigning random priorities with collision-prone finite keys and no tie breaker; replaying a retry with a changed input snapshot; concurrently inserting conflicting objects as though operations commute; retaining a history DAG without bounding dead nodes; and promoting an expected bound into a request-level latency guarantee.

### Compact example

Insert distinct keys $1,2,3,4$ into an ordinary binary-search tree in random order. For keys 1 and 4, key 1 is an ancestor of key 4 exactly when 1 appears before 2, 3, and 4, which has probability $1/4$. The same interval-earliest argument gives every ancestor probability and, by linearity of expectation, the expected total depth $2(5)H_4-16=29/6$ comparisons.

### Connections

[ALGE-066](./066-randomized-selection-and-sampling.md) constructs and validates the random permutation. [ALGE-068](../ROADMAP.md#block-07--approximation-heuristics-and-randomized-algorithms) classifies error and runtime guarantees. [ALGE-074](../ROADMAP.md#block-08--online-streaming-and-dynamic-algorithms) contrasts offline random order with genuinely online arrivals.

## Governing Question

Given a set of constraints, points, segments, or keys, how do we build its target structure by random incremental insertion, prove correctness for every insertion order, derive expected efficiency from random order, and preserve those assumptions in robust software?

Randomization should simplify analysis or prevent consistently pathological insertion order; it must not repair an incorrect updater. A sound RIC therefore has two contracts. The deterministic contract says what structure exists after every prefix and how an insertion transforms it. The probabilistic contract says how the permutation is distributed and which adversary can observe it.

## Why This Matters

Incremental algorithms naturally expose locality. A new geometric site may invalidate one cavity; a constraint may matter only when it violates the current optimum; a key follows one search path. Random order makes the next object symmetric with every member of the completed prefix, often making deletion easier to analyze than insertion.

This pattern underlies practical algorithms for Delaunay and Voronoi diagrams, trapezoidal maps and point location, convex hulls, fixed-dimensional linear programming, and randomized search trees. It also provides an engineering architecture: canonicalize input, separate random ordering from deterministic updates, make conflicts explicit, retain replay evidence, and test the updater against an order-independent oracle on small instances.

Expected efficiency remains conditional. Degenerate predicates, hidden duplicate identities, adaptive arrivals, unbounded history, cache behavior, and tail latency can dominate a deployment even when the classical theorem is correct.

## Prerequisites and Retrieval

Retrieve conditional probability, random permutations, indicator variables, harmonic numbers, linearity of expectation, induction, binary-search trees, planar orientation, convex hulls, graph boundaries, exact integer arithmetic, and stable identifiers. Review [ALGE-006](./006-best-worst-expected-and-amortized-cost.md) for cost quantifiers, [ALGE-029](./029-randomization-as-a-design-tool.md) for fixed-input randomized analysis, and [ALGE-066](./066-randomized-selection-and-sampling.md) for unbiased permutation construction.

This chapter owns the reusable RIC method, backward analysis, conflict structures, history, degeneracy, and production evidence. It uses search trees and geometry as analysis vehicles without taking ownership of balanced-tree implementations or a full computational-geometry course. General Monte Carlo and Las Vegas taxonomy belongs to ALGE-068; dynamic deletion and adversarial online models belong to Block 08.

## Learning Objectives

After completing this module, you should be able to:

1. specify a randomized incremental algorithm as a random permutation plus a deterministic updater;
2. prove prefix correctness independently of random order;
3. derive the conditional uniform-last lemma used by backward analysis;
4. translate deletion degree into expected insertion work;
5. derive harmonic expected depth for a random binary-search tree;
6. distinguish structural update, conflict location, predicate, and memory costs;
7. design conflict graphs and history DAGs with auditable invariants;
8. handle duplicates and geometric degeneracies without relying on accidental floating behavior;
9. preserve the probability model across parallelism, retries, streaming, and adversarial exposure; and
10. validate both universal correctness and distribution-dependent performance claims at their proper strength.

## Core Exposition

### Separate the deterministic and probabilistic layers

Let $X$ be a finite set of $n$ objects with stable, unique identities. Choose a uniform permutation $\pi=(x_1,\ldots,x_n)$ and define $R_i=\{x_1,\ldots,x_i\}$. A deterministic updater transforms the canonical structure $C(R_{i-1})$ into $C(R_i)$. The fundamental correctness invariant is

$$
C_i=C(R_i)
$$

after every insertion. It must hold for every permutation, including the worst one. Randomness affects the distribution of work, not the definition of a valid result.

This separation is operationally useful. The permutation can be produced, versioned, and tested independently. The updater consumes an explicit sequence and can be replayed. A reference implementation can recompute $C(R_i)$ from scratch for small prefixes and compare canonical outputs after each incremental step.

Objects that compare equal still require distinct identities. Deduplicating before permutation changes the problem; assigning one random value per object can create collisions. Either shuffle unique identities directly or use a random priority paired with a unique deterministic tie breaker, and prove that the resulting total order has the required distribution.

### Prove the uniform-last lemma

Condition on $R_i=S$, where $S$ is a particular $i$-element subset. The first $i$ positions contain exactly the objects in $S$, and their relative order is uniform among $i!$ permutations. For a fixed $x\in S$, exactly $(i-1)!$ of those permutations put $x$ last. Therefore

$$
\Pr[x_i=x\mid R_i=S]=\frac{(i-1)!}{i!}=\frac1i.
$$

The conditioning is precise: retain the unordered set $S$ and forget its order. If one conditions on the complete prefix sequence, its last object is already known and no symmetry remains. If filtering or retry logic makes some orders more likely than others, the lemma no longer applies without a new argument.

Backward analysis fixes the completed prefix structure and asks what deleting its uniformly random last member would undo. This is often easier because a final planar structure has a global degree bound, while the forward insertion may discover a complicated conflict region.

### Convert deletion complexity into expected update work

For structure $C(S)$ and object $x\in S$, let $b(S,x)$ be the number of primitive changes that the reverse deletion of $x$ exposes, under a declared charging correspondence with forward insertion. Then

$$
\mathbb E[c_i\mid R_i=S]
=\sum_{x\in S}\frac1i b(S,x)
=\frac1i\sum_{x\in S}b(S,x).
$$

If $\sum_x b(S,x)\le g(i)$ for every size-$i$ set, the conditional expectation is at most $g(i)/i$, and so is the unconditional expectation by total expectation. When $g(i)=O(i)$, expected structural change per insertion is $O(1)$ and total structural change is $O(n)$.

The correspondence must be proved, not named. Forward insertion may create features that a naive reverse deletion does not uniquely recover. Some analyses charge a feature to its defining objects or count conflicts over a sample. Write the exact charged event, multiplicity, and premise.

Structural change is not total runtime. Locating the affected feature may cost $O(\log i)$ expected time through a history DAG even when the cavity has constant expected size. Exact predicates may use variable-precision arithmetic. Allocation, cache misses, and retained history add costs outside the combinatorial count.

### Use an incremental search tree as a finite model

Insert distinct ranked keys into an ordinary binary-search tree in permutation order. Its result is correct for every order: inorder traversal is sorted, and insertion preserves the search invariant. Its shape exposes the effect of order.

For distinct keys $a<b$, $a$ is an ancestor of $b$ exactly when $a$ is the earliest inserted key in interval $[a,b]$. If any interior key appears earlier, it separates them before $a$ arrives. Because each of the $b-a+1$ interval keys is equally likely to be earliest,

$$
\Pr[a\text{ is ancestor of }b]=\frac1{b-a+1}.
$$

For key $j$, summing indicators over smaller and larger possible ancestors gives

$$
\mathbb E[D_j]
=(H_j-1)+(H_{n-j+1}-1).
$$

Summing over $j$ and using $\sum_{j=1}^nH_j=(n+1)H_n-n$ yields expected internal path length

$$
\mathbb E\!\left[\sum_jD_j\right]=2(n+1)H_n-4n.
$$

The following executable model accepts an explicit order. It proves no distributional claim; it checks deterministic insertion behavior and demonstrates best-looking and pathological transcripts.

<!-- bijux-verify: {"id":"incremental-search-tree","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"balanced inorder=(1, 2, 3, 4, 5, 6, 7) height=3 comparisons=10\nsorted inorder=(1, 2, 3, 4, 5, 6, 7) height=7 comparisons=21\nduplicate=rejected\n","stderr":""}} -->
```python
class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


def build(order):
    root = None
    comparisons = 0
    seen = set()
    for key in order:
        if key in seen:
            raise ValueError("duplicate identity")
        seen.add(key)
        if root is None:
            root = Node(key)
            continue
        cursor = root
        while True:
            comparisons += 1
            if key < cursor.key:
                if cursor.left is None:
                    cursor.left = Node(key)
                    break
                cursor = cursor.left
            else:
                if cursor.right is None:
                    cursor.right = Node(key)
                    break
                cursor = cursor.right
    return root, comparisons


def inorder(node):
    return () if node is None else inorder(node.left) + (node.key,) + inorder(node.right)


def height(node):
    return 0 if node is None else 1 + max(height(node.left), height(node.right))


for label, order in (
    ("balanced", (4, 2, 6, 1, 3, 5, 7)),
    ("sorted", (1, 2, 3, 4, 5, 6, 7)),
):
    tree, comparisons = build(order)
    print(f"{label} inorder={inorder(tree)} height={height(tree)} comparisons={comparisons}")

try:
    build((2, 1, 2))
except ValueError:
    print("duplicate=rejected")
```

Expected output is the annotation's exact stdout. The balanced transcript is not uniformly sampled and the sorted transcript is deliberately bad. A distributional validation separately enumerates permutations and compares mean work with the formula.

### Represent features, conflicts, and history

Many geometric RIC algorithms maintain features determined by a constant-size subset. A Delaunay triangle is defined by three sites in general position; a fourth site conflicts with it if it lies inside its circumcircle. Inserting a site removes its conflict cavity and connects the new site to the cavity boundary. A trapezoidal map feature is determined by segment endpoints and neighboring segments; an inserted segment crosses and replaces a sequence of current trapezoids.

A **conflict graph** explicitly relates current features to uninserted objects. It can make the next conflict region easy to find, but eagerly storing every relation may be expensive. A **history DAG** instead retains replaced features and points each old feature to its replacements. A query starts at an initial feature and follows only children whose regions can contain the object. The history is acyclic because edges point from older to newer versions.

History and current topology have different lifecycles. A feature may be dead in the current structure yet essential for future location. Reference counting based only on current adjacency can therefore corrupt search. Conversely, retaining every auxiliary object without a proved expectation or compaction policy can exhaust memory.

Stable identifiers bind predicates, features, conflicts, and trace events. An insertion record should state the object identity, located starting feature, predicate outcomes or hashes, destroyed feature IDs, boundary feature IDs, created feature IDs, and implementation version. Sensitive coordinates or customer payloads need not be logged when a content-addressed snapshot and minimal replay fixture suffice.

### Preserve the conflict-boundary invariant

An update normally follows five stages:

1. locate one feature that conflicts with the new object;
2. enumerate the complete conflict region;
3. extract and orient the boundary between conflicting and surviving features;
4. construct replacement features attached to that boundary; and
5. update topology, conflicts, and history atomically.

Before mutation, validate that the region is connected when the theorem requires connectedness, every internal adjacency is paired, and every boundary incidence appears exactly once. After mutation, validate local orientation, reciprocal adjacency, defining-set cardinality, and the absence of references to removed current features. A transaction or copy-on-write update prevents an exception during predicate evaluation from publishing a half-rebuilt cavity.

In Delaunay insertion under general position, all triangles whose circumcircles contain the new point form the cavity, and the new triangles connect the point to each cavity-boundary edge. This local rule and the global empty-circumcircle characterization establish correctness. Point location and degeneracy resolution require additional machinery; merely finding one conflicting triangle is not the complete update.

### Handle degeneracy as semantics

Orientation and in-circle tests decide combinatorial topology. A rounded sign can flip an edge, split a connected cavity, or make two adjacent features disagree. A robust implementation commonly uses a filtered predicate: evaluate quickly in floating point with a certified error bound, then fall back to exact arithmetic when the sign is uncertain. The filter is an optimization; the exact sign or declared symbolic tie rule owns correctness.

General-position proofs exclude zero signs. Real inputs can contain duplicate points, collinear triples, cocircular quadruples, coincident segment endpoints, and coordinates whose integer products overflow a fixed-width accumulator. Choose a policy: reject invalid duplicates, canonicalize them while preserving multiplicity metadata, compute a canonical non-simplicial structure, or apply a consistent symbolic perturbation based on stable IDs. Per-call epsilon tests are not a global tie policy and may violate transitivity.

Input normalization also belongs to semantics. Scaling coordinates can reduce conditioning but must not change exact incidence. Coordinate-system conversion, unit normalization, and deduplication must happen before the snapshot digest and permutation are fixed.

### Account for location and recursive violation

Backward analysis often proves small expected change, but the new object must first reach its conflict. A history DAG can reduce expected point location to logarithmic depth for classical planar constructions. A randomized search tree obtains logarithmic expected search paths from its random shape. Conflict graphs can make location direct at the cost of maintaining more relations.

Seidel's fixed-dimensional linear-programming algorithm illustrates a different incremental mechanism. Process constraints in random order. If the current optimum satisfies the next constraint, do nothing. If it violates the constraint, the new optimum lies on that constraint's boundary, reducing the dimension in a recursive subproblem over earlier constraints. Backward analysis bounds the probability that the $i$th constraint is defining by at most $d/i$ for dimension $d$. The resulting expected time is linear in the number of constraints for fixed $d$, with dimension-dependent constants; it is not a dimension-independent linear-time LP solver.

The base cases, infeasibility representation, unboundedness representation, exact comparison, and repeated constraints are part of that algorithm's correctness. A floating solver called recursively does not inherit the combinatorial theorem automatically.

### Engineer randomness, concurrency, and tails

A uniform permutation assumes a fixed population. A live stream arriving from users is not random merely because arrival times look irregular. Snapshot first, bind the digest, and then shuffle. If the system must operate online, use an online analysis rather than importing an offline RIC theorem.

Expose the permutation seed only according to the threat model. A public seed is excellent for replay but lets an adaptive adversary construct or select a bad order if identities map predictably to priorities. Keep a secret keyed ordering for adversarial services, or add deterministic worst-case budgets and fallback. A retry must reuse the same snapshot and transcript when it claims replay; changing either creates a new trial.

Independent insertions do not necessarily commute. Two geometric sites may have overlapping conflict regions, while two search-tree keys contend on a shared path. Safe parallel variants identify a set of nonconflicting updates, apply a deterministic commit order, or use a separately analyzed divide-and-conquer algorithm. Scheduling the same random permutation concurrently without conflict control changes the algorithm.

Set budgets for predicates, conflict size, history depth, allocations, and wall time. On budget exhaustion, preserve the last coherent prefix and either resume from its transcript, switch to a proved deterministic construction, or return a declared resource failure. Expected $O(n\log n)$ is a population average over random choices for each fixed input; it is not a per-request deadline.

### Build evidence matched to claims

Correctness tests should exercise every insertion prefix, not only the final output. For small inputs, enumerate permutations and compare the incremental structure with a from-scratch oracle. Apply property tests to input relabeling, permutation replay, exact-predicate fallback, and canonical output equality. Inject individual failures between update stages to check atomicity.

Distributional tests can detect a broken shuffle but cannot prove uniformity. Prove the mapping as in ALGE-066, then test the concrete implementation. Performance experiments should retain instance family, original order, canonical snapshot digest, permutation version and seed, per-insertion structural changes, location depth, predicate counts, exact fallbacks, allocations, and elapsed time. Report mean, quantiles, maxima, and timeout policy; do not discard failed or slow trials.

Finite exhaustive checks support finite claims. Enumerating all permutations through $n=8$ can verify the random-tree depth formula for those sizes and expose updater errors. It does not establish the asymptotic theorem, generator uniformity for large states, geometric robustness, or production latency.

## Definitions and Notation

| Term | Precise use in this chapter |
|---|---|
| $X$ | Fixed input set of $n$ uniquely identified objects |
| $\pi$ | Uniform random permutation $(x_1,\ldots,x_n)$ of $X$ |
| $R_i$ | Unordered prefix set $\{x_1,\ldots,x_i\}$ |
| $C(S)$ | Canonical target structure defined by object set $S$ |
| $C_i$ | Incrementally maintained structure after insertion $i$ |
| feature | Primitive current structural object with stable identity |
| defining set | Minimal input identities determining a feature |
| conflict | Predicate saying an uninserted object invalidates a feature |
| $b(S,x)$ | Declared reverse-deletion charge for $x$ in $C(S)$ |
| history DAG | Acyclic replacement graph used to locate later conflicts |
| $H_n$ | Harmonic number $\sum_{k=1}^n1/k$ |
| general position | Input restriction eliminating declared zero-predicate cases |
| exact predicate | Decision procedure returning the mathematically correct combinatorial sign |

A **model** specifies $X$, $C$, predicates, random permutation, and adversary. A **mechanism** locates and replaces conflicts. A **guarantee** proves prefix correctness or a conditional expected bound. An **implementation** represents identities, topology, history, and arithmetic. A **policy** chooses duplicate handling, exposure, budgets, fallback, and retention. **Evidence** records tests and observations without silently strengthening those guarantees.

## Mechanisms, Invariants, or Proof Structure

### Prefix-correctness induction

**Base case.** Construct $C(\varnothing)$ or a documented sentinel structure and prove its representation invariants.

**Inductive hypothesis.** Assume $C_{i-1}=C(R_{i-1})$ and all topology, defining-set, conflict, and history invariants hold.

**Update lemma.** Prove the locator finds a seed conflict when one exists; region enumeration finds exactly all affected features; the extracted boundary separates affected from surviving features; and replacement constructs precisely the features of $C(R_i)$ incident to $x_i$.

**Preservation.** Surviving features remain valid, removed features leave no current references, new reciprocal adjacencies agree, and history edges point from older to newer features.

**Conclusion.** The committed state equals $C(R_i)$. By induction the final state is $C(X)$ for every permutation.

### Backward-analysis checklist

1. Fix a size-$i$ prefix set $S$; do not average over a vaguely random input.
2. Prove that the last object is uniform in $S$ under the actual permutation process.
3. Define the reverse-deletion charge $b(S,x)$ and prove it matches or upper-bounds forward work.
4. Bound $\sum_{x\in S}b(S,x)$ using structural combinatorics.
5. Divide by $i$, remove the conditioning by total expectation, and sum over $i$.
6. Add location, predicate, allocation, preprocessing, and output costs not included in $b$.
7. State worst-case work and the adversary/randomness visibility assumptions separately.

### History-DAG invariants

- graph edges follow strictly increasing creation epochs, so cycles are impossible;
- roots cover the initial search domain;
- every live feature is reachable for every object that can conflict with it;
- children collectively cover the searchable portion of their replaced parent's region;
- a query follows only predicate-compatible children and cannot terminate at a dead feature;
- deterministic ties select one valid path when regions share boundaries; and
- retention and compaction preserve reachability or rebuild it from a canonical snapshot.

## Alternatives and Trade-Offs

| Approach | Strength | Cost or risk | Appropriate use |
|---|---|---|---|
| Random incremental order | Simple local updater and backward analysis | Expected, not worst-case, work; replay metadata | Fixed snapshot with robust local conflicts |
| Deterministic incremental order | Natural for already ordered or online input | Can expose quadratic paths | Benign orders or proved order-sensitive bound |
| Divide and conquer | Often deterministic and parallelizable | Merge logic and storage can be complex | Batch construction with strong merge algorithms |
| Sweep line | Exploits coordinate order and event queue | Degeneracies and global ordering | Planar geometric arrangements and intersections |
| Conflict graph | Direct access to affected features | Potentially many stored relations | When conflict complexity is provably bounded |
| History DAG | Reuses replacement history for location | Dead-node retention and path tails | Static construction with many future queries |
| Rebuild-from-scratch oracle | Simple specification and strong small-case check | Usually too slow for production | Testing prefixes and recovery |
| Exact arithmetic everywhere | Simple correctness story | High constant factors and allocation | Small inputs or highly adversarial coordinates |
| Filtered exact predicates | Fast common case with exact decisions | More complicated implementation | Performance-sensitive robust geometry |
| Deterministic fallback | Caps bad randomized paths | Duplicate implementation and transition proof | Latency-sensitive or adversarial services |

Random priorities can replace an explicit permutation only when their induced total order is equivalent to the proved distribution. Divide-and-conquer may be a better parallel architecture than forcing concurrent mutation into a sequential RIC. A history DAG can accelerate construction and later queries, but it is not free evidence that its expected depth holds for a modified splitting or tie policy.

## Failure Modes and Misconceptions

- **“Incremental means online.”** Offline RIC permutes a fixed snapshot; an online algorithm must accept an arrival order it does not control.
- **“Every next object is independent of the prefix.”** It is uniform among remaining objects, not independent draws with replacement.
- **“Conditioning on $R_i$ fixes the order.”** $R_i$ is the unordered prefix set; retaining the sequence destroys the uniform-last symmetry.
- **“Constant expected structural change means linear runtime.”** Location, exact predicates, initialization, and output may contribute logarithmic or larger costs.
- **“A local cavity update is obviously correct.”** Region completeness, boundary orientation, replacement coverage, and surviving topology require proof.
- **“An epsilon handles degeneracy.”** Locally chosen tolerances can produce inconsistent signs and invalid combinatorial structures.
- **“Random priorities cannot tie.”** Finite priorities collide; a stable unique tie breaker is required and may affect the induced distribution.
- **“Retries are independent.”** Reusing a seed repeats the same path; changing snapshot or seed creates a different trial and must be disclosed.
- **“Parallel insertions preserve random order.”** Overlapping conflicts and nondeterministic commits define a different algorithm.
- **“Expected time is a latency SLO.”** Expectation permits rare expensive runs; budgets, tail measurement, and fallback are separate controls.
- **“The final output is enough evidence.”** Prefix bugs can cancel or remain latent in history; inspect every prefix against an oracle on small inputs.
- **“A history node can be freed when it dies.”** Dead current features may remain routing nodes for later location.

## Worked Examples

### Example 1

**Situation.** A random permutation of $\{a,b,c,d,e\}$ has unordered first-three set $S=\{a,c,e\}$. What is the probability that $c$ was inserted third?

**Reasoning.** Conditioning on $R_3=S$ leaves the $3!=6$ relative orders of $S$ equally likely. Exactly $2!=2$ end in $c$: the first two positions are either $a,e$ or $e,a$. Thus the probability is $2/6=1/3$. If we instead condition on the ordered prefix $(a,e,c)$, the probability is one; that conditioning is unusable for backward symmetry.

**Conclusion.** The last object is uniform only after conditioning on the unordered prefix set.

### Example 2

**Situation.** Scan a random permutation of distinct values and replace the current minimum whenever a smaller value appears. How many replacements occur in expectation, counting the first value?

**Reasoning.** Position $i$ is a new minimum exactly when the last element of its $i$-element prefix is the smallest member of that prefix. By uniform-last symmetry this has probability $1/i$. Let $I_i$ indicate this event. Then $\mathbb E[\sum_iI_i]=\sum_i\mathbb E[I_i]=H_n$. Independence of the indicators is unnecessary. For $n=4$, the expectation is $1+1/2+1/3+1/4=25/12$.

**Conclusion.** Backward analysis plus linearity gives $H_n$ expected records without assuming independent record events.

### Example 3

**Situation.** Find the expected total insertion comparisons for four distinct sorted ranks inserted in uniform random order.

**Reasoning.** Total comparisons equal the sum of final node depths. The formula gives

$$
2(n+1)H_n-4n=2(5)(25/12)-16=250/12-192/12=29/6.
$$

The result need not be an integer because it averages the 24 orders. The worst orders $(1,2,3,4)$ and $(4,3,2,1)$ cost $0+1+2+3=6$ comparisons.

**Conclusion.** Expected work is $29/6$, while a legal transcript costs six; expectation does not remove bad orders.

### Example 4

**Situation.** Compare orders $(4,2,6,1,3,5,7)$ and $(1,2,3,4,5,6,7)$ in the executable tree.

**Reasoning.** The first order creates depths $0,1,1,2,2,2,2$, totaling ten comparisons and height three. The sorted order creates depths $0,1,2,3,4,5,6$, totaling 21 and height seven. Both inorder traversals are $(1,2,3,4,5,6,7)$, so output correctness is order-independent even though work and representation shape are not.

**Conclusion.** Randomness supports an expected shape claim; the deterministic insertion invariant supports correctness.

### Example 5

**Situation.** A completed size-$i$ planar structure has $f_i$ features, each defined by at most three objects, and deletion charge counts defining incidences. Bound expected charge for the last object.

**Reasoning.** Summing charges over all objects counts each feature at most three times, so $\sum_{x\in S}b(S,x)\le3f_i$. Uniform-last symmetry gives expected charge at most $3f_i/i$. If a separate planar bound proves $f_i\le ci$, the expected charge is at most $3c$. Neither statement includes location or exact-predicate cost.

**Conclusion.** Constant expected structural change follows from a linear feature bound plus bounded defining-set size, not from “geometry is local.”

### Example 6

**Situation.** Inserting site $p$ conflicts with three current triangles forming a connected cavity whose boundary has five edges.

**Reasoning.** Preserve the five boundary edges before deleting the three triangles. Internal cavity edges occur twice with opposite orientation and cancel; boundary edges occur once. Create one triangle from $p$ and each oriented boundary edge, yielding five new triangles. Check positive orientation and reciprocal adjacency. Exact in-circle predicates establish that no surviving triangle conflicts with $p$; exact orientation or a declared symbolic policy handles zero cases.

**Conclusion.** The valid update is defined by complete conflict discovery and a checked boundary, not by deleting the first triangle found.

### Example 7

**Situation.** Trapezoid $T_0$ is split into $T_1,T_2$; later $T_2$ is split into $T_3,T_4$. A new query lies in $T_4$.

**Reasoning.** The current map contains $T_1,T_3,T_4$, but the history path is $T_0\to T_2\to T_4$. Freeing $T_0$ or $T_2$ when it leaves the current map breaks location. The epoch strictly increases along both edges, proving acyclicity. Child-region predicates route the query; boundary ties use the declared stable rule.

**Conclusion.** Current topology and search history are separate ownership graphs with different retention requirements.

### Example 8

**Situation.** A fixed-dimensional LP has $i$ constraints in its current prefix and at most $d$ constraints define its unique nondegenerate optimum. What is the probability that the $i$th constraint forces recursion?

**Reasoning.** Condition on the prefix set. The last constraint is uniform among its $i$ members. Removing it changes the optimum only if it belongs to the defining basis, whose size is at most $d$. Therefore the violation/defining probability is at most $d/i$. A recursive solve occurs on a $(d-1)$-dimensional boundary; its cost and base cases must still be included in the recurrence.

**Conclusion.** Random order makes expensive violations rare, but fixed dimension and a bounded basis are essential premises.

### Example 9

**Situation.** A 2D orientation implementation computes products of signed 64-bit coordinate differences. Inputs use coordinates up to $10^{12}$.

**Reasoning.** A difference can have magnitude $2\cdot10^{12}$, and a product can reach $4\cdot10^{24}$, far beyond the signed 64-bit maximum near $9.22\cdot10^{18}$. Overflow can change the sign and therefore topology. A floating epsilon does not repair integer overflow. Use widened or arbitrary-precision exact arithmetic, or a certified filter with exact fallback; define behavior when the exact determinant is zero.

**Conclusion.** Predicate range analysis and zero semantics are prerequisites for a trustworthy incremental geometry implementation.

### Example 10

**Situation.** Two workers insert sites whose cavities overlap. One loses a transaction race, takes a fresh seed, and retries against a newer snapshot while the run is reported as a replay.

**Reasoning.** The workers cannot both commit against the old boundary because their mutations do not commute. The loser also changed both prefix state and permutation transcript, so it is not replaying the original construction. A safe design serializes these commits in the declared order, schedules only proven-disjoint cavities, or records the newer snapshot and seed as a new trial. Metrics must retain the conflict and abandoned work.

**Conclusion.** Concurrency control and retry identity are part of the algorithm's semantics and evidence, not transparent infrastructure details.

## Cross-Program Connections

- **Data Structures Engineering:** randomized search trees and persistent/history structures supply representations; this chapter owns the randomized incremental analysis pattern.
- **Operating Systems:** transactional publication, concurrency, cancellation, and resource budgets determine whether a prefix remains coherent under failures.
- **Database Engineering:** snapshot identity, write conflicts, replay, and atomic commits provide direct analogies for incremental construction state.
- **Systems Engineering:** trace schemas, tail budgets, fallback, observability, and adversary models turn an expectation theorem into a deployable component.
- **Software Testing and Quality Engineering:** from-scratch oracles, exhaustive permutations, metamorphic relabeling, fault injection, and distributional tests provide different evidence strengths.
- **Theory of Computation and Complexity:** expectation is over algorithmic choices for each fixed input; it does not change worst-case correctness or imply deterministic polynomial latency.
- **Algorithm Engineering:** [ALGE-066](./066-randomized-selection-and-sampling.md) validates ordering machinery; [ALGE-068](../ROADMAP.md#block-07--approximation-heuristics-and-randomized-algorithms) classifies randomized guarantees; Block 08 treats online and dynamic settings.

## References

1. Kenneth L. Clarkson and Peter W. Shor, “Applications of Random Sampling in Computational Geometry, II,” *Discrete & Computational Geometry* 4 (1989), 387–421. DOI: [10.1007/BF02187740](https://doi.org/10.1007/BF02187740). Primary source for random-sampling and backward-analysis techniques in computational geometry; bibliographic record checked 2026-09-05.
2. Raimund Seidel, “Small-Dimensional Linear Programming and Convex Hulls Made Easy,” *Discrete & Computational Geometry* 6 (1991), 423–434. DOI: [10.1007/BF02574699](https://doi.org/10.1007/BF02574699). Primary source for simple randomized incremental fixed-dimensional LP and convex-hull algorithms; checked 2026-09-05.
3. Leonidas J. Guibas, Donald E. Knuth, and Micha Sharir, “Randomized Incremental Construction of Delaunay and Voronoi Diagrams,” *Algorithmica* 7 (1992), 381–413. DOI: [10.1007/BF01758770](https://doi.org/10.1007/BF01758770). Primary source for randomized incremental planar Delaunay/Voronoi construction and history; checked 2026-09-05.
4. Mark de Berg, Otfried Cheong, Marc van Kreveld, and Mark Overmars, *Computational Geometry: Algorithms and Applications*, 3rd ed., Springer, 2008. DOI: [10.1007/978-3-540-77974-2](https://doi.org/10.1007/978-3-540-77974-2). Textbook treatment of randomized incremental point location, Delaunay triangulation, predicates, and degeneracy; publisher record checked 2026-09-05.
5. Ketan Mulmuley, *Computational Geometry: An Introduction Through Randomized Algorithms*, Prentice Hall, 1994, ISBN 978-0-13-336363-0. Monograph on randomized geometric construction and analysis; bibliographic data checked 2026-09-05.
6. Raimund Seidel and Cecilia R. Aragon, “Randomized Search Trees,” *Algorithmica* 16 (1996), 464–497. DOI: [10.1007/BF01940876](https://doi.org/10.1007/BF01940876). Primary source for random-priority search trees and their analysis; bibliographic record checked 2026-09-05.
7. Donald E. Knuth, *The Art of Computer Programming, Volume 3: Sorting and Searching*, 2nd ed., Addison-Wesley, 1998, ISBN 978-0-201-89685-5. Reference for permutations, binary-tree searching, and quantitative analysis; publisher record checked 2026-09-05.

## Exercises

### Exercise 1

A service receives 100 uniquely identified constraints, snapshots them, applies a uniform Fisher–Yates permutation, and incrementally builds a structure. State the sample space, define $R_{20}$, and give the conditional probability that a fixed constraint $c\in R_{20}$ occupies position 20. Explain why the answer changes if you condition on the ordered first 20 positions.

### Exercise 2

For keys $1,\ldots,n$, derive the expected depth of key $j$ in a binary-search tree built from a uniform random permutation. Evaluate it for $n=7,j=4$.

### Exercise 3

A Delaunay inserter immediately deletes each conflicting triangle as depth-first search discovers it. Halfway through, an exact in-circle fallback raises an exception. The catch block retries from one surviving triangle. Diagnose the violated invariants and propose an atomic update design.

### Exercise 4

Compare a full conflict graph, a history DAG, and from-scratch location for a static randomized incremental geometric construction. State what each stores, the main benefit, main risk, and evidence needed before selecting it.

### Exercise 5

Consider an incremental structure where every final feature is defined by at most $k$ input objects and every size-$i$ structure has at most $ai+b$ features. Suppose forward structural work is at most the number of defining incidences exposed by deleting the last object. Derive an expected total structural-work bound over $n$ insertions. Then state three reasons actual runtime may exceed that bound.

## Answers to the Exercises

### Answer 1

The sample space is the $100!$ permutations of the fixed snapshot, each with probability $1/100!$. $R_{20}$ is the unordered set of identities in positions 1 through 20. Conditioned on a particular $R_{20}=S$ containing $c$, the relative order of $S$ is uniform over $20!$ orders, of which $19!$ put $c$ last. Thus the probability is $19!/20!=1/20$. Conditioning on the complete ordered prefix identifies its twentieth member, making the probability either zero or one; the symmetry needed for backward analysis has been conditioned away.

### Answer 2

For $a<j$, $a$ is an ancestor of $j$ when it is earliest in $[a,j]$, with probability $1/(j-a+1)$. Summing over $a=1,\ldots,j-1$ gives $H_j-1$. For $b>j$, the corresponding sum is $H_{n-j+1}-1$. Therefore

$$
\mathbb E[D_j]=H_j+H_{n-j+1}-2.
$$

For $n=7,j=4$, both terms are $H_4=25/12$, so the expectation is $50/12-2=13/6$. This is an expectation over order, not a bound for every tree.

### Answer 3

The implementation published a partial mutation before region discovery and replacement completed. Current topology can contain holes, boundary incidences were lost with deleted triangles, and the retry seed triangle may no longer lead to the original complete cavity. First discover the full conflict set without mutation; derive and validate its oriented boundary; compute all replacement triangles and exact predicate outcomes in private state; validate reciprocal adjacency and coverage; then atomically swap current references and append history. On failure, discard private state and leave the old coherent prefix unchanged. A write-ahead or immutable event record can support replay without treating half-mutated topology as valid.

### Answer 4

A full conflict graph stores relations from current features to all uninserted conflicting objects. It can locate the next conflict directly, but relation count and maintenance may dominate; require a proved expected conflict bound and measured memory. A history DAG stores old-to-new replacement edges and routes an object through predicate-compatible regions. It often uses less explicit conflict storage and supports point location, but depth tails, dead-node retention, and boundary ties need proofs and measurements. From-scratch location scans or reconstructs from the current structure. It is simplest and valuable as an oracle, but commonly costs linear or worse time per insertion. Select using proved total costs under the actual feature model plus traces of relation counts, path depths, predicate fallbacks, memory, and adversarial cases.

### Answer 5

For a size-$i$ prefix $S$, at most $k(ai+b)$ defining incidences exist. Uniform-last symmetry and the charging premise therefore give

$$
\mathbb E[c_i\mid R_i=S]\le\frac{k(ai+b)}i=ka+\frac{kb}{i}.
$$

Summing over $i=1,\ldots,n$ gives expected structural work at most

$$
kan+kbH_n=O(kan+kb\log n).
$$

Actual runtime can be larger because the bound omits conflict location, expensive or exact predicates, and allocation/history maintenance. Other acceptable additions include cache behavior, synchronization, retries, output construction, and rare tail paths. A complete answer must preserve the fixed-snapshot uniform-permutation premise and must not present the expectation as a per-run cap.
