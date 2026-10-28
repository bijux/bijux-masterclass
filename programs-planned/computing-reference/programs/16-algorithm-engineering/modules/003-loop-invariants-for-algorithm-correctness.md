---
module_id: ALGE-003
program: Algorithm Engineering
level: 1
module_number: 3
title: Loop Invariants for Algorithm Correctness
status: complete
last_verified: 2026-09-04
---

# Loop Invariants for Algorithm Correctness

## One-Page Review

### Governing question

How can one finite argument prove that a loop with an unknown number of iterations establishes its postcondition for every admissible input?

### Essential definitions

- A **loop invariant** is a predicate that holds at a declared loop checkpoint before the first guard test and again after every completed iteration.
- **Initialization** proves the precondition and setup establish the invariant.
- **Preservation** proves one body execution re-establishes the invariant, assuming the invariant and guard held before that execution.
- **Exit reasoning** combines the invariant with the negated guard to derive the postcondition.
- A **variant** or **ranking function** maps continuing states into a well-founded order and strictly decreases, proving termination.
- A **frame condition** identifies state the loop may modify and state it must preserve.
- A **ghost value** is specification-only state, such as an immutable copy of an input, used to state a proof without affecting execution.

### Central model, mechanism, or theorem

For precondition $P$, invariant $I$, guard $B$, body $S$, and postcondition $Q$, partial correctness follows from:

$$
P\Rightarrow I,
\qquad
\{I\land B\}\ S\ \{I\},
\qquad
I\land\neg B\Rightarrow Q.
$$

Total correctness additionally needs a variant $V$ whose values lie in a well-founded set, remain in that set while $B$ holds, and strictly decrease after every body execution. The invariant explains what completed iterations mean; the variant explains why there cannot be infinitely many of them.

### Critical invariants

- State exactly where $I$ is asserted; “during the loop” is too vague.
- Make $I$ weak enough to hold initially and strong enough with $\neg B$ to imply $Q$.
- Preserve bounds, accumulated meaning, unprocessed-region meaning, frame conditions, and any representation invariant needed by the body.
- Prove preservation for an arbitrary state satisfying $I\land B$, not only for states seen in examples.
- Separate safety/partial correctness from progress/termination.
- Relate mutable state to an immutable initial value when permutation, conservation, or provenance matters.
- Match the proof model to actual indexing, arithmetic, mutation, aliasing, exceptions, and control flow.

### Common failures

Common failures are choosing only a bound such as $0\le i\le n$; restating the postcondition so strongly that initialization fails; checking the invariant after, rather than before, an unsafe access; assuming the guard while reasoning after exit; forgetting empty input; changing two variables without proving their relation; treating a decreasing integer as a variant without a lower bound; ignoring `break`, `continue`, return, exceptions, overflow, or mutation through aliases; and using tests or runtime assertions as a universal proof.

### Compact example

To sum $a[0:n)$, initialize $i=0$ and $s=0$, then repeatedly set $s:=s+a[i]$ and $i:=i+1$ while $i<n$. Use

$$
I\equiv 0\le i\le n\ \land\ s=\sum_{k=0}^{i-1}a_k.
$$

Initialization uses the empty-sum convention. Preservation expands the prefix by exactly $a_i$. At exit, $i\ge n$ from $\neg(i<n)$ and $i\le n$ from $I$, hence $i=n$ and $s$ is the full sum. Variant $n-i$ proves termination.

### Connections

[ALGE-001](./001-problem-statements-inputs-outputs-and-constraints.md) defines the problem relation, and [ALGE-002](./002-preconditions-postconditions-and-correctness.md) defines preconditions, postconditions, frames, and partial versus total correctness. [ALGE-004](../ROADMAP.md) generalizes the inductive structure used here. Theory of Programming owns general proof logics; Data Structures Engineering owns representation invariants of mutable structures.

## Governing Question

A loop may execute zero times, once, or a number of times determined by input and evolving state. We cannot prove it correct by listing all iteration counts. What finite proposition can summarize every reachable checkpoint, connect setup to completion, and expose enough structure to check one arbitrary iteration?

The answer is not merely “find something that stays true.” Many useless properties stay true. A useful loop invariant is an interface between the code already executed and the code still to execute. It records exactly enough accumulated meaning, bounds, preserved input, and remaining obligation for three local arguments—initialization, preservation, and exit—to establish a global partial-correctness claim. A separate well-founded progress argument establishes termination.

## Why This Matters

Loops concentrate algorithmic defects. One changed comparison can omit the last element, one index update can fail to progress, and one mutation can destroy information needed by the postcondition. Typical tests may miss the empty input, a one-element interval, duplicates at a boundary, arithmetic overflow, or a path through `continue`. An invariant forces those cases into a single quantified claim.

Invariants are also a design tool. If no plausible invariant is preserved, the code may be maintaining the wrong state. Deriving an invariant before the body often reveals which counters, accumulators, partitions, or ghost values the algorithm actually needs. This is why loop invariants appear both in foundational algorithm texts and in verification tools. The current [Dafny reference manual](https://dafny.org/dafny/DafnyRef/DafnyRef) describes loop specifications in terms of invariants, decreases clauses, and modified state; a tool discharges generated obligations, but the author remains responsible for the specification and model.

The ACM/IEEE-CS/AAAI CS2023 Algorithmic Foundations guidance explicitly includes explaining how loop invariants prove algorithm correctness ([CS2023 final report](https://csed.acm.org/wp-content/uploads/2025/11/CS2023-Report.htm)). The enduring skill is broader than any notation or verifier: partition a changing computation into facts already established, obligations still outstanding, and progress toward a boundary.

## Prerequisites and Retrieval

Retrieve the following before proceeding:

- predicates, implication, conjunction, negation, universal quantification, and mathematical induction;
- finite sequences, half-open intervals $[l,r)$, sums, products, sets, and multisets;
- program states, assignment, sequential composition, conditionals, and `while` loops;
- preconditions, postconditions, frame conditions, Hoare triples, partial correctness, and total correctness;
- bounded versus mathematical integers, array bounds, aliasing, mutation, and exceptional control flow;
- well-founded orders and why a strictly decreasing natural number cannot decrease forever.

From [ALGE-002](./002-preconditions-postconditions-and-correctness.md), recall that $\{P\}\ C\ \{Q\}$ is a partial-correctness claim: if $P$ holds and $C$ terminates normally, then $Q$ holds. It does not by itself say that $C$ terminates.

## Learning Objectives

After completing this module, you should be able to:

1. state a loop checkpoint precisely and write an invariant over the complete relevant state;
2. prove initialization, preservation, and exit implication for a `while` loop;
3. distinguish an invariant from the guard, postcondition, assertion, representation invariant, and variant;
4. derive useful invariants by weakening a postcondition and separating processed from unprocessed regions;
5. include bounds, conservation, provenance, frames, and ghost state when the result requires them;
6. prove termination with an appropriate well-founded variant;
7. analyze zero-iteration, boundary, duplicate, and adversarial cases;
8. handle `break`, `continue`, early return, mutation, and exceptional paths without assuming structured-loop rules still apply unchanged;
9. connect mathematical reasoning to concrete integer, indexing, memory, and language semantics;
10. use runtime checks and automated verification as scoped evidence without confusing them with specification validity or universal proof.

## Core Exposition

### A loop is a repeated state transition

Let $\Sigma$ be the set of states relevant to a loop. A guard $B:\Sigma\to\{true,false\}$ decides whether another iteration begins. The body $S$ transforms a state into a successor state, possibly with several outcomes if the language or algorithm is nondeterministic.

Choose the **loop-head checkpoint** immediately before evaluating $B$. An invariant $I$ must hold at that checkpoint:

1. after the initialization code and before the first guard test;
2. after any completed body execution returns control to the loop head;
3. therefore, when a normal guard-false exit occurs.

This placement matters. An array access inside the body may rely on $I\land B$, not on $I$ alone. After a `break`, the invariant may not have been re-established unless the language-specific proof rule or code establishes it. “The invariant is always true” is misleading shorthand; its truth is required at named checkpoints.

### The while rule compresses arbitrarily many iterations

For a structured loop `while B do S`, prove:

**Initialization**

$$
P\Rightarrow I.
$$

The precondition together with loop setup establishes the invariant. This obligation includes the zero-iteration case: if $B$ is false initially, the program exits using the initial invariant.

**Preservation**

$$
\{I\land B\}\ S\ \{I\}.
$$

Assume an arbitrary loop-head state satisfying both the invariant and guard. Execute one body iteration symbolically and prove the successor state again satisfies $I$. This is a conditional claim; an invariant need not survive arbitrary execution from a state that violates its premises.

**Exit implication**

$$
I\land\neg B\Rightarrow Q.
$$

On normal exit, the invariant still holds and the guard is false. Those facts—not the invariant alone—must imply the postcondition.

These obligations yield the partial-correctness rule

$$
\frac{
P\Rightarrow I
\qquad
\{I\land B\}\ S\ \{I\}
\qquad
I\land\neg B\Rightarrow Q
}{
\{P\}\ \mathbf{while}\ B\ \mathbf{do}\ S\ \{Q\}
}.
$$

The reasoning is inductive: initialization is the base case, and preservation is the step. [Floyd's 1967 assertion method](https://bookstore.ams.org/PSAPM/19) and [Hoare's 1969 axiomatic treatment](https://doi.org/10.1145/363235.363259) provide the historical foundations. ALGE-004 develops the broader use of induction; here the focus is the loop-specific proof interface.

### Useful invariants balance weakness and strength

The postcondition is often too strong to hold before work begins. For summation, $s=\sum_{k=0}^{n-1}a_k$ normally fails initially. The bound $0\le i\le n$ is easy to preserve but too weak to say what $s$ means. Combine a progress boundary with a generalized result:

$$
0\le i\le n
\quad\land\quad
s=\sum_{k=0}^{i-1}a_k.
$$

At $i=0$, the accumulated result describes an empty prefix. As $i$ advances, the same formula describes more of the final result. At $i=n$, it becomes the postcondition. This “replace the final boundary by the current boundary” pattern is one reliable derivation technique.

An invariant can also be too strong in an irrelevant way. Demanding that the unprocessed suffix remain byte-for-byte unchanged may block an in-place partition algorithm that is allowed to rearrange it. Strength must serve the postcondition, safe execution, preservation, or a later proof obligation.

### Partition the state into processed, frontier, and unprocessed regions

Array and sequence invariants often describe three regions:

- a processed prefix or suffix whose required property is established;
- one or more frontier indices with explicit bounds;
- an unprocessed region that still contains all unresolved candidates.

For linear search over $a[0:n)$, before testing $a_i$ a suitable invariant is

$$
0\le i\le n
\quad\land\quad
\forall k\in[0,i):a_k\ne t.
$$

The prefix contains no target. If $a_i=t$, returning $i$ proves it is the first occurrence. Otherwise advancing $i$ extends the known target-free prefix by one element. If the loop exits at $i=n$, the whole sequence is target-free.

Binary search uses a complementary idea: all still-possible answers remain inside a shrinking interval. The invariant must say both that the interval bounds are valid and that discarded regions cannot contain an admissible answer. Bounds alone prevent some memory errors but do not prove search correctness.

### Preserve initial meaning with ghost state

Mutation can erase the evidence needed to state a postcondition. Let $a_0$ denote an immutable mathematical copy of the initial sequence. An in-place sorting invariant may state that a prefix is sorted while also requiring

$$
multiset(a)=multiset(a_0).
$$

This conservation property rules out losing, duplicating, or inventing elements. The ghost value $a_0$ is not copied at runtime merely because the proof names it; it belongs to the specification model. A concrete verification system decides how such state is represented and erased.

Frame conditions matter inside loops too. If the method promises not to change memory outside $a[l:r)$, the loop proof must preserve that frame on every iteration. A correct final value does not excuse transient or permanent corruption elsewhere.

### Termination requires a different argument

Initialization, preservation, and exit establish partial correctness. To prove total correctness, choose a variant $V$ into a well-founded set. For a natural-number variant, prove:

$$
I\land B\Rightarrow V\in\mathbb{N},
$$

and for every body transition from state $\sigma$ to $\sigma'$,

$$
V(\sigma')<V(\sigma).
$$

For a prefix scan, $V=n-i$. For interval search, $V=r-l$. Nonnegativity without strict decrease permits stuttering; strict decrease without a lower bound permits an infinite descent over mathematical integers. Both obligations are necessary.

Lexicographic tuples handle nested or multi-stage progress. A pair $(u,v)\in\mathbb{N}^2$ decreases lexicographically if either $u$ decreases or $u$ stays equal and $v$ decreases. The order, reset conditions, and bounds must be explicit.

Termination remains relative to the execution model. A body containing blocking I/O, an unfairly scheduled concurrent operation, or an unbounded retry may not terminate merely because a local counter changes. Do not hide environmental liveness assumptions inside an algorithmic variant.

### Derive an invariant systematically

There is no complete mechanical recipe for discovering the right invariant, but a disciplined derivation is better than guessing:

1. Write the exact postcondition $Q$, including initial/final relations.
2. Normalize the loop head and identify every variable or location changed by the body.
3. Choose a boundary variable that measures how much input is processed.
4. Replace the postcondition's final boundary with the current boundary.
5. Describe what is known about the unprocessed region or remaining candidates.
6. Add bounds required for every access and update.
7. Add conservation, ordering, uniqueness, frame, and representation properties used later.
8. Test initialization, including empty and already-finished inputs.
9. Execute one arbitrary symbolic iteration and repair missing relations.
10. Combine $I$ with $\neg B$; if $Q$ does not follow, strengthen $I$ with the missing fact.
11. Remove clauses that serve no safety, preservation, exit, or modular reasoning purpose.
12. Choose and prove a separate variant for termination.

This workflow is bidirectional. Exit reasoning reveals missing strength; preservation reveals excessive or false strength; initialization reveals whether the generalized claim actually includes the starting state.

### Control flow changes the proof graph

A `continue` transfers control to the next loop-head checkpoint. Every path to it must establish the invariant and any progress needed for the variant. A `break` exits without necessarily providing $\neg B$; its path needs a separate exit assertion sufficient for the postcondition. An early return must establish the method postcondition directly. An exception needs the exceptional postcondition and frame promised by the contract.

Desugaring a `for` loop can clarify the checkpoint, bound evaluation, and update order. However, language semantics differ: bounds may be evaluated once or repeatedly; iterators may detect mutation; arithmetic may wrap or trap; and `finally` blocks may run on exits. Apply a proof rule matching the actual construct rather than an imagined `while` translation.

### Assertions, tests, and verifiers provide different evidence

A runtime `assert I` checks one reached state in one run. Property-based or exhaustive bounded tests check many finite states. A verifier attempts to prove generated obligations over a formal model. None automatically proves that $I$ expresses the intended problem, that the model matches the deployed language/runtime, or that environmental assumptions hold.

The following Python program makes the prefix-sum invariant executable and checks every sequence of length at most four over five values. It is deliberately bounded evidence, not a universal proof. Python's integers are unbounded for these purposes; a fixed-width implementation needs an overflow policy and proof.

<!-- bijux-verify: {"id":"prefix-sum-invariant-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"[] -> 0\n[5] -> 5\n[3, -2, 7] -> 8\n[0, 0, 0] -> 0\nexhaustive-small: 781\n","stderr":""}} -->
```python
from itertools import product


def prefix_total(values):
    index = 0
    total = 0
    while index < len(values):
        assert 0 <= index <= len(values)
        assert total == sum(values[:index])
        total += values[index]
        index += 1
    assert index == len(values)
    assert total == sum(values)
    return total


for sample in ([], [5], [3, -2, 7], [0, 0, 0]):
    print(f"{sample} -> {prefix_total(sample)}")

checked = 0
for length in range(5):
    for candidate in product(range(-2, 3), repeat=length):
        values = list(candidate)
        assert prefix_total(values) == sum(values)
        checked += 1
print(f"exhaustive-small: {checked}")
```

The count is $\sum_{j=0}^{4}5^j=(5^5-1)/(5-1)=781$. The run checks invariant assertions and results for those cases. The mathematical preservation proof covers arbitrary finite sequences under the stated arithmetic and indexing model.

### Model correspondence completes the engineering argument

A paper proof may use mathematical integers, immutable sequences, atomic assignments, and normal termination only. An implementation may use bounded integers, shared mutable buffers, callbacks, exceptions, and compiler transformations. Record the bridge:

- whether index arithmetic can overflow;
- whether the guard guarantees every array access is in bounds;
- whether aliases or concurrent writers can invalidate $I$ between checkpoints;
- whether comparisons form the assumed relation;
- whether body operations can fail after partial mutation;
- whether the loop reads a stable length or a changing stream;
- whether floating-point algebra preserves the identities used in the proof.

The invariant proof is conditional on those semantics. It is rigorous precisely when its scope and assumptions are explicit.

## Definitions and Notation

- $\Sigma$: set of program states in the proof model.
- $P(\sigma)$: precondition on initial state $\sigma$.
- $Q(\sigma_0,\sigma_f)$: postcondition relating initial and final states.
- $B(\sigma)$: loop guard.
- $S$: loop body transition or command.
- $I(\sigma)$: loop invariant at the declared checkpoint.
- $V(\sigma)$: variant or ranking value used for termination.
- $\{P\}\ C\ \{Q\}$: partial-correctness Hoare triple.
- $a_0$: immutable logical value of sequence $a$ at method entry.
- $a[l:r)$: half-open sequence region containing indices $l$ through $r-1$.
- $\sum_{k=l}^{r-1}a_k=0$ when $l=r$: empty-sum convention.
- $multiset(a)$: elements of $a$ with multiplicity but without order.
- A predicate $I$ is **inductive for the loop** when it holds initially and is preserved by every enabled body transition.
- An invariant is **sufficient for $Q$** when $I\land\neg B\Rightarrow Q$ for normal exit.
- A relation $\prec$ is **well founded** when it admits no infinite descending chain.

For deterministic body semantics, preservation can be written

$$
\forall\sigma,\sigma':
I(\sigma)\land B(\sigma)\land S(\sigma,\sigma')
\Rightarrow I(\sigma').
$$

For nondeterministic semantics, the universal quantifier over $\sigma'$ is essential: every permitted successor must preserve the invariant under demonic correctness.

## Mechanisms, Invariants, or Proof Structure

Use this proof worksheet for a structured loop:

1. **Contract:** state $P$, $Q$, normal and exceptional outcomes, and the frame.
2. **State:** name initial values and every mutable variable/location relevant to $Q$.
3. **Checkpoint:** place $I$ immediately before the guard, or declare another precise checkpoint and use matching rules.
4. **Candidate:** combine frontier bounds, processed-region meaning, unresolved-region meaning, conservation, and representation facts.
5. **Initialization:** substitute initial values and simplify every conjunct, including empty ranges.
6. **Safety:** derive that $I\land B$ makes each body access and operation defined.
7. **Preservation:** introduce old logical names, execute one arbitrary iteration, and prove every conjunct in the successor state.
8. **Exit:** negate the guard exactly and derive $Q$ from it together with $I$.
9. **Alternative exits:** prove separate obligations for `break`, return, exception, cancellation, and resource failure.
10. **Termination:** give $V$, its well-founded domain, lower-bound argument, and strict-decrease calculation.
11. **Correspondence:** check arithmetic, indexing, aliases, mutation, comparator, concurrency, and language control-flow semantics.
12. **Evidence:** recompute examples, exercise boundaries, run executable checks, and label what remains unproved.

For the prefix-sum loop, let the body old state be $(i,s)$ and successor be $(i',s')$ with

$$
s'=s+a_i,
\qquad
i'=i+1.
$$

Assume $I\land i<n$. Bounds give $0\le i<n$, so $a_i$ is defined. From the sum invariant,

$$
s'=\left(\sum_{k=0}^{i-1}a_k\right)+a_i
=\sum_{k=0}^{i}a_k
=\sum_{k=0}^{i'-1}a_k.
$$

Also $0\le i'<n+1$, hence $0\le i'\le n$. Both conjuncts are restored. For the variant,

$$
V'=n-i'=n-(i+1)=(n-i)-1=V-1<V,
$$

and $i<n$ with $i\ge0$ implies $V=n-i\ge1$. This is a proof, under the finite-sequence and mathematical-integer model, not merely an execution trace.

## Alternatives and Trade-Offs

**Backward derivation versus forward discovery.** Working backward from $Q$ exposes the generalized result needed at exit. Working forward from the initialized state exposes facts the body naturally preserves. Strong practice alternates them until the assertions meet.

**One compound invariant versus named clauses.** A single formula is concise for proof rules. Named clauses—bounds, processed meaning, remaining candidates, conservation, frame—are easier to review and diagnose. Their conjunction is the actual invariant; prove every clause.

**Functional versus in-place algorithms.** Immutable transformations reduce frame and alias obligations but may allocate or copy. In-place loops can reduce memory traffic but need region, conservation, and representation invariants strong enough to exclude corruption.

**Sentinel versus explicit bound.** A sentinel may remove a repeated bounds test, but establishing and restoring it changes state and proof obligations. An explicit bound is often easier to specify. Compare measured benefit only after both versions satisfy the same contract.

**Early exit versus single exit.** Early return can make the successful case direct and efficient. A single exit can simplify one post-loop argument. The proof cost depends on whether each early path naturally establishes $Q$ or requires duplicated reasoning.

**Runtime assertions versus static verification.** Assertions reveal violations on executed paths and can protect internal assumptions in testing. Static verification can quantify over a formal state space. Assertions have runtime/build-mode effects; verification has modeling and annotation costs. Neither validates the stakeholder contract automatically.

**Strong versus minimal invariants.** Strong invariants support later reasoning and safe maintenance, but unnecessary clauses increase proof burden and coupling. Minimal invariants are elegant but may omit a fact future code depends on. Prefer the smallest invariant that supports safety, preservation, exit, framing, and intended modular use.

## Failure Modes and Misconceptions

1. **“The guard is the invariant.”** A guard says whether to continue; it usually says nothing about accumulated correctness.
2. **“Any unchanged fact is useful.”** `n=n` is invariant but contributes no proof value.
3. **“The postcondition is always the best invariant.”** It may fail before the first iteration; generalize it to the processed region.
4. **“Initialization can ignore zero iterations.”** If the guard starts false, initialization plus exit must already establish $Q$.
5. **“Preservation can use what happened in previous examples.”** It must start from an arbitrary state satisfying $I\land B$.
6. **“Bounds prove correctness.”** Bounds may prove safe access but not result meaning.
7. **“Result meaning proves safe access.”** A semantic accumulator equation may omit index bounds required by the next body step.
8. **“The invariant holds at every instruction.”** Its guaranteed checkpoints depend on the proof rule; body statements may temporarily break it.
9. **“A decreasing expression proves termination.”** Its domain must be well founded and decrease on every continuing path.
10. **“Partial correctness includes progress.”** A nonterminating loop can satisfy a partial-correctness triple vacuously.
11. **“The negated guard is obvious.”** Off-by-one errors often come from negating `<` as `>` instead of $\ge$.
12. **“`break` exits because the guard is false.”** It may exit while the guard is true, so a separate exit fact is required.
13. **“`continue` is harmless.”** It can bypass progress or invariant-restoring statements.
14. **“A final sorted array proves sorting.”** Conservation, stability, range, and frame properties may be missing.
15. **“Runtime assertions prove the loop.”** They check reached states under selected executions.
16. **“A verifier discovers the intended invariant.”** Automation proves supplied or inferred formulas relative to a model; it does not choose stakeholder meaning.
17. **“Mathematical arithmetic automatically matches code.”** Overflow, rounding, NaN, and conversion can invalidate algebra.
18. **“No alias is modified because its variable name is absent.”** Aliases can reach the same storage.

## Worked Examples

### Example 1

**Question:** Prove a counter loop executes exactly $n$ iterations for $n\ge0$.

**Reasoning:** Initialize $i=0$; guard $i<n$; body $i:=i+1$. Choose $I\equiv0\le i\le n$. Initialization follows from $n\ge0$. Under $I\land i<n$, $i+1\le n$, so preservation holds. At exit, $i\ge n$ and $i\le n$, hence $i=n$. Variant $n-i$ is a natural number and decreases by one.

**Conclusion:** Bounds plus the negated guard establish the exact final counter, and the variant establishes termination.

### Example 2

**Question:** Why does the prefix-sum invariant use $a[0:i)$ rather than $a[0:i]$?

**Reasoning:** At the loop head, $i$ denotes the next unread index. Initially $i=0$, so the processed region must be empty. After adding $a_i$ and incrementing $i$, the processed region becomes the old prefix plus that element. Using an inclusive prefix would claim $a_0$ had already been added at initialization and would make $i=n$ refer beyond the final valid index.

**Conclusion:** Half-open regions align the frontier with zero work, one-step extension, and the $i=n$ exit boundary.

### Example 3

**Question:** Derive an invariant for returning the first index of target $t$ by linear search.

**Reasoning:** Let $i$ be the next index. Use $0\le i\le n$ and $\forall k\in[0,i):a_k\ne t$. Initially the prefix is empty. If $i<n$ and $a_i\ne t$, incrementing $i$ extends the target-free prefix. If $a_i=t$, return $i$; the invariant proves no earlier match. If $i=n$, the invariant proves absence. Variant $n-i$ handles the non-returning path.

**Conclusion:** The invariant captures both discarded evidence and the minimality needed for “first,” not merely “some” match.

### Example 4

**Question:** What invariant proves a lower-bound binary search returns the first position whose value is at least $t$?

**Reasoning:** For sorted $a[0:n)$ maintain $0\le l\le r\le n$, every index below $l$ has value $<t$, and every index at or above $r$ has value $\ge t$. The unresolved interval is $[l,r)$. If $a_m<t$, set $l=m+1$; otherwise set $r=m$. Each update discards only positions whose relation is known. At $l=r$, the boundary clauses characterize the lower bound. Variant $r-l$ strictly shrinks when $m=l+\lfloor(r-l)/2\rfloor$.

**Conclusion:** Search correctness comes from the semantic partition around the interval, while interval length proves progress.

### Example 5

**Question:** What does the outer-loop invariant of insertion sort need beyond “the prefix is sorted”?

**Reasoning:** Before iteration $i$, state $1\le i\le n$, prefix $a[0:i)$ is sorted, and $multiset(a)=multiset(a_0)$. Sorting alone permits replacing the prefix with invented small values. The inner shift loop needs its own hole/region invariant to show which element is being inserted and that shifts preserve the multiset and bounds. At $i=n$, sortedness covers the full array and conservation proves it is a sorting of the input.

**Conclusion:** Order plus conservation and bounds establish sorting; nested loops require compatible invariants at both levels.

### Example 6

**Question:** Prove Euclid's loop preserves the greatest common divisor for nonnegative $x,y$.

**Reasoning:** Save $x_0,y_0$ and maintain $x\ge0$, $y\ge0$, and $\gcd(x,y)=\gcd(x_0,y_0)$. With guard $y\ne0$, update $(x,y):=(y,x\bmod y)$. For $y>0$, the division property gives $\gcd(x,y)=\gcd(y,x\bmod y)$, so the invariant is preserved. The new $y$ satisfies $0\le x\bmod y<y$, making old $y$ a decreasing natural-number variant. At exit $y=0$, so $x=\gcd(x,0)=\gcd(x_0,y_0)$.

**Conclusion:** An algebraic conservation invariant proves the result, and the remainder bound proves termination.

### Example 7

**Question:** How does a three-way partition invariant handle values less than, equal to, and greater than a pivot?

**Reasoning:** Maintain indices $0\le l\le i\le r\le n$ with $a[0:l)<p$, $a[l:i)=p$, $a[r:n)>p$, and $[i,r)$ unclassified, plus multiset conservation. Classifying $a_i$ either swaps it into the low region and advances $l,i$, advances $i$ for equality, or swaps it into the high region and decreases $r$ without advancing $i$ because the incoming value is unclassified. Variant $r-i$ decreases in every case.

**Conclusion:** Region meanings determine the asymmetric updates that a bare index-bound invariant cannot justify.

### Example 8

**Question:** Diagnose two candidates for the summation loop: $I_1\equiv s$ equals the final total and $I_2\equiv0\le i\le n$.

**Reasoning:** $I_1$ is strong enough at exit but normally false at initialization; it assumes the work already done. $I_2$ initializes and preserves but says nothing about $s$, so it cannot imply the result. Their failure directions suggest the repair: generalize the final total to the current prefix and conjoin the bounds.

**Conclusion:** Failed proof obligations are diagnostic: initialization exposes excessive strength, while exit exposes insufficient strength.

### Example 9

**Question:** A loop increments $i$ at the bottom, but one branch executes `continue` first. What fails?

**Reasoning:** If that branch leaves the semantic clauses unchanged, the invariant might still hold at the next head, but variant $n-i$ does not decrease. The loop can repeat forever on the same element. If the branch partially mutates an accumulator before continuing, preservation may fail too. Move the progress update before all `continue` paths or prove a different well-founded measure and restored invariant per path.

**Conclusion:** Every back edge—not merely the textual bottom of the body—must re-establish safety and progress obligations.

### Example 10

**Question:** How should a chunked message parser reason about an incomplete final record?

**Reasoning:** Maintain cursor bounds, that bytes before the cursor decode to exactly the emitted records, that emitted records satisfy the format, that the remaining suffix equals the unconsumed input, and that output/error state obeys the frame. A complete record advances the cursor by a positive encoded length. If the suffix lacks enough bytes, policy decides whether to return `NeedMoreData` with the suffix untouched or `Malformed`; it must not read past the buffer or silently drop bytes. The variant is remaining bytes only on paths guaranteed to consume; streaming waits require a separate environmental liveness contract.

**Conclusion:** The same processed/frontier/unprocessed pattern transfers to production parsing, but termination and partial-input policy depend on the surrounding system.

## Cross-Program Connections

- [Theory of Programming](../../07-programming-languages-theory-of-programming/ROADMAP.md) owns general Hoare logic, axiomatic semantics, predicate transformers, and mechanized program proof.
- [Theory of Computation & Complexity](../../15-theory-of-computation-and-complexity/ROADMAP.md) supplies formal machine models and separates termination from recognition behavior.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) uses representation invariants for heaps, trees, hash tables, and mutable graph structures; a loop must preserve both its local invariant and the structure's representation invariant.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) turns invariant boundaries into tests and property oracles while retaining the distinction between finite evidence and proof.
- [Concurrent & Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) extends invariants to interference, atomicity, ownership, and rely/guarantee reasoning; a sequential loop proof does not survive arbitrary concurrent mutation.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) treats bounds, conservation, parser progress, and exceptional frames as adversarial safety obligations.

## References

1. Robert W. Floyd. [“Assigning Meanings to Programs,” in *Mathematical Aspects of Computer Science*](https://bookstore.ams.org/PSAPM/19), Proceedings of Symposia in Applied Mathematics 19, American Mathematical Society, 1967, pp. 19–32. Foundational assertion and invariant method.
2. C. A. R. Hoare. [“An Axiomatic Basis for Computer Programming”](https://doi.org/10.1145/363235.363259), *Communications of the ACM* 12(10), 1969, pp. 576–580. Axiomatic rules for assignments, composition, conditionals, and iteration.
3. Edsger W. Dijkstra. [“Guarded Commands, Nondeterminacy and Formal Derivation of Programs”](https://doi.org/10.1145/360933.360975), *Communications of the ACM* 18(8), 1975, pp. 453–457. Program derivation and guarded iteration.
4. David Gries. *The Science of Programming*. Springer, 1981. Systematic invariant discovery, predicate logic, and loop development.
5. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. [*Introduction to Algorithms*, fourth edition](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), MIT Press, 2022. Loop invariants in algorithm correctness and analysis.
6. Cornell University CS 2110. [“Loop Invariants”](https://www.cs.cornell.edu/courses/cs2110/2026fa/lectures/lec04/), Fall 2026. Checkpoint, array-region, initialization, preservation, and progress pedagogy; consulted 2026-09-04.
7. Dafny contributors. [*Dafny Reference Manual*](https://dafny.org/dafny/DafnyRef/DafnyRef), sections on loop specifications, invariants, framing, and termination; consulted 2026-09-04. This is tool documentation, not authority for language-independent correctness.
8. ACM, IEEE Computer Society, and AAAI. [*Computer Science Curricula 2023*](https://doi.org/10.1145/3664191), endorsed 2024, Algorithmic Foundations. Curricular context for algorithm correctness and loop invariants; consulted 2026-09-04.

## Exercises

### Exercise 1

For a loop that initializes $i=0$ and repeatedly writes `a[i] = 0; i += 1` while $i<n$, state the loop-head checkpoint, a sufficient invariant, the normal-exit argument, and a variant. Include the empty-array case and a frame condition.

### Exercise 2

Derive and prove an invariant for computing $x^n$ by repeated multiplication when $n\in\mathbb{N}$: initialize $i=0,r=1$ and repeat $r:=r\cdot x; i:=i+1$ while $i<n$. Show initialization, preservation, exit, and termination, and state the arithmetic assumption.

### Exercise 3

Diagnose this binary-search design over sorted $a[0:n)$: `l=0; r=n-1; while l<r: m=(l+r)//2; if a[m]<t: l=m; else: r=m`. Give a concrete nonterminating input, identify the failed proof obligation, and repair the interval convention and updates for lower-bound search.

### Exercise 4

Compare an early-return linear search with a version that uses a `found` flag and one normal loop exit. Give suitable invariants for both, explain their exit obligations, and decide when either structure is preferable without changing the first-occurrence contract.

### Exercise 5

Design correctness obligations for an unfamiliar reconciliation loop that processes a finite snapshot of account adjustments in chunks. It must apply each accepted adjustment exactly once, reject invalid adjustments without changing balances, support cancellation between chunks, and resume safely from a durable cursor. State the invariant, variant or liveness limitation, frame, failure boundaries, and evidence needed beyond the mathematical proof.

## Answers to the Exercises

### Answer 1

Place the checkpoint immediately before the guard. With $a_0$ the initial array and $n=|a|$ fixed at entry, use

$$
0\le i\le n
\land
\forall k\in[0,i):a_k=0
\land
\forall k\in[i,n):a_k=(a_0)_k.
$$

The last clause is stronger than needed if later unprocessed cells may be modified, but it expresses this loop's exact frame. Also state that memory outside $a[0:n)$ and unrelated state are unchanged. At initialization, $i=0$ makes the processed prefix empty and the full suffix equal to $a_0$; this includes $n=0$. Under $I\land i<n$, access $a_i$ is in bounds. Writing zero establishes the next processed element, and incrementing produces the new split at $i+1$. At exit, $i\ge n$ and $i\le n$, so $i=n$ and every array element is zero. Variant $n-i$ is a natural number under the guard and decreases by one.

If aliases or concurrent writers can change the array, forbid them in the precondition or extend the model; the sequential invariant otherwise does not hold.

### Answer 2

Use the invariant

$$
0\le i\le n
\land
r=x^i.
$$

Initialization gives $i=0$ and $r=1=x^0$. Assume the invariant and guard $i<n$. With old values $i,r$, the body gives $r'=rx$ and $i'=i+1$. Therefore

$$
r'=x^i x=x^{i+1}=x^{i'},
$$

and $i<n$ implies $0\le i'\le n$. Thus the invariant is preserved. At exit, $i\ge n$ combines with $i\le n$ to give $i=n$, so $r=x^n$. Variant $n-i$ starts nonnegative and decreases by one per iteration.

This proof assumes exact exponent and multiplication laws, such as mathematical integers/reals or an algebraic structure where the stated exponentiation law holds. Fixed-width code needs an explicit checked, wrapping, saturating, or preconditioned overflow policy; floating-point multiplication does not inherit arbitrary real-algebra equalities exactly.

### Answer 3

Take $a=[1,3]$ and $t=2$. Initially $l=0,r=1$, so $m=0$. Since $a_0<t$, the update sets $l=m=0$; the state does not change and the loop repeats forever. The candidate variant $r-l$ fails strict decrease. The update also makes the intended discarded-prefix invariant awkward because index $m$ was classified but remains in the unresolved interval.

Use the half-open interval $[l,r)$ with initialization $l=0,r=n$. Maintain $0\le l\le r\le n$, all indices below $l$ have value $<t$, and all indices at or above $r$ have value $\ge t$. While $l<r$, choose

$$
m=l+\left\lfloor\frac{r-l}{2}\right\rfloor.
$$

If $a_m<t$, set $l=m+1$; otherwise set $r=m$. Since $l\le m<r$, either update strictly reduces $r-l$. At exit $l=r$, and the partition clauses characterize the first position whose value is at least $t$, including the answer $n$ when no such element exists. In bounded arithmetic, the midpoint expression also avoids adding two potentially large nonnegative indices, subject to proven subtraction bounds.

### Answer 4

For early return, maintain $0\le i\le n$ and $\forall k<i:a_k\ne t$. At each iteration, if $a_i=t$, the return path directly proves valid index, equality, and absence of earlier matches. The normal guard-false exit proves absence from the whole sequence. This form mirrors the two result cases and uses no flag.

For one exit, a loop may maintain $0\le i\le n$, a Boolean `found`, and a relation such as: if `found` then $i<n$, $a_i=t$, and no earlier index matches; if not `found`, no index below $i$ matches. The guard can be $i<n\land\neg found$. On exit, either `found` supplies the first index or $i=n$ supplies absence. Updates must avoid advancing $i$ after discovering the match, or the invariant must name a separate result index.

Early return is usually clearer when discovery immediately establishes the method postcondition and cleanup is automatic. A single exit can centralize cleanup, tracing, or result construction, but the flag increases state and proof clauses. Either is acceptable only if it preserves the same first-occurrence, frame, and termination contract; style alone is not a correctness argument.

### Answer 5

Let the finite snapshot contain adjustments $A[0:n)$ with immutable snapshot identifier $s$, and let durable cursor $i$ identify the next undecided adjustment. A suitable invariant includes:

- $0\le i\le n$ and cursor/snapshot identity agree;
- every valid adjustment in $A[0:i)$ has one committed idempotency record and its effect appears exactly once in balances;
- every invalid adjustment in $A[0:i)$ has one durable rejection record and no balance effect;
- no adjustment in $A[i:n)$ has an effect attributed to this run;
- the sum and provenance of applied balance deltas equal exactly the accepted processed records;
- unrelated accounts, currencies, ledgers, and metadata satisfy the frame;
- chunk transaction state is either wholly committed with its new cursor or wholly absent.

For an in-memory loop with guaranteed successful local steps, $n-i$ is a variant. In a real system, transient storage failure and retry mean wall-clock termination additionally depends on bounded retry, cancellation, or environmental recovery assumptions. Cancellation is accepted only between atomic chunks: committed effects and cursor remain aligned, and resume loads the same snapshot plus cursor. Invalid records are rejected atomically without balance mutation. A crash between balance writes and cursor advancement is prevented by one transaction or recovered through an idempotency protocol whose invariant covers the intermediate state.

The proof model needs unique adjustment identities, snapshot immutability, transaction and isolation semantics, numeric range and currency-unit rules, authorization, and duplicate-delivery policy. Evidence beyond the invariant proof includes transaction-fault injection, crash/restart and duplicate replay tests, boundary and overflow cases, concurrency/isolation tests, durable-log reconciliation, access-control review, observability checks, and operational recovery exercises. No external financial, accounting, regulatory, security, distributed-systems, or practitioner review is claimed; qualified owners must validate policy and authorize production use.
