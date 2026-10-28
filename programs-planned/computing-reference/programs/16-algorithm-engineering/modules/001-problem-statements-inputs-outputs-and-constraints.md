---
module_id: ALGE-001
program: Algorithm Engineering
level: 1
module_number: 1
title: Problem Statements, Inputs, Outputs, and Constraints
status: complete
last_verified: 2026-08-28
---

# Problem Statements, Inputs, Outputs, and Constraints

## One-Page Review

### Governing question

What must a problem statement determine before an algorithm can be designed, proved correct, implemented, or measured?

### Essential definitions

- A **problem** is a relation between admissible inputs and acceptable outputs.
- An **instance** is one particular admissible input.
- A **solution** is an output related to that instance by the problem's acceptance relation.
- A **constraint** restricts admissible inputs, acceptable outputs, or available resources.
- A **precondition** is assumed at entry; a **postcondition** must hold at successful return.
- A **witness** is output that certifies a positive claim; a verifier checks it.

### Central model, mechanism, or theorem

Specify a problem as a triple `(I, O, R)`: input set `I`, output set `O`, and acceptance relation `R ⊆ I × O`. An implementation is correct when, for every admissible `x ∈ I`, it terminates with some `y ∈ O` satisfying `R(x,y)`. Optimization problems add an objective and a tie policy; partial or infeasible problems add an explicit outcome policy.

### Critical invariants

- Every quantified correctness claim names its input domain.
- Output validity and output optimality are separate obligations.
- Representation constraints are not silently confused with domain constraints.
- Boundary conventions—empty input, equality, indexing, overflow, duplicates, and ties—are explicit.
- Complexity is parameterized by a declared input-size measure.
- Examples illustrate a specification; they do not define it.

### Common failures

Common failures include solving a familiar but different problem, omitting infeasible cases, assuming uniqueness, leaving ties unspecified, using ambiguous indexing, hiding numeric overflow, stating “fast” without a cost model, and testing examples instead of defining a universal relation.

### Compact example

For two-sum, input is a finite integer sequence `a` and integer target `t`. A successful output is a pair `(i,j)` with `0 ≤ i < j < len(a)` and `a[i]+a[j]=t`; otherwise output `None`, permitted only when no such pair exists. This statement decides distinct indices, duplicates, indexing, and failure semantics without prescribing an algorithm.

### Connections

[ALGE-002](../ROADMAP.md) turns this relation into preconditions, postconditions, and correctness obligations. Formal encodings connect to [Theory of Computation & Complexity](../../15-theory-of-computation-and-complexity/ROADMAP.md); representation choices connect to [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md); stakeholder meaning connects to [Software Design & Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md).

## Governing Question

An algorithm is an answer, not the question. Before selecting a technique, we must know which inputs are legal, which outputs are acceptable for each input, whether a solution always exists, and which resources matter. Otherwise a proof can establish correctness for the wrong relation and a benchmark can optimize behavior users did not request.

The ACM/IEEE-CS/AAAI CS2023 Algorithmic Foundations material asks learners to select algorithms for real problems and evaluate trade-offs. That competence begins with a specification whose domain, output obligations, and size parameters make alternatives comparable ([CS2023 final report](https://csed.acm.org/wp-content/uploads/2025/11/CS2023-Report.htm)).

## Why This Matters

Small wording choices change problems. “Find the nearest facility” is incomplete until distance, coordinate system, tie behavior, closed facilities, and unreachable clients are defined. “Sort these records” is incomplete if stability, key order, mutation, and invalid keys matter. Each omitted choice can alter admissible algorithms and correctness.

Production inputs add representation hazards: bounded integers overflow, text has encodings, graphs may contain parallel edges, and a stream cannot necessarily be reread. The mathematical problem should isolate enduring meaning while an implementation contract states machine limits. Mixing them makes the specification either unrealistically abstract or accidentally platform-specific.

## Prerequisites and Retrieval

You should be comfortable with sets, functions, relations, quantifiers, finite sequences, predicates, and basic programming. Recall that a function returns one output, while a relation may allow many; `∀` differs from testing selected examples; and a sequence differs from a set because order and multiplicity matter.

## Learning Objectives

After completing this module, you should be able to:

- express a computational problem as input, output, and acceptance sets;
- separate feasibility, validity, optimality, and tie-breaking;
- identify domain, representation, operational, and resource constraints;
- specify empty, malformed, infeasible, duplicate, and boundary cases;
- choose input-size parameters without assuming one scalar is sufficient;
- distinguish a problem from an algorithm, API, test suite, or data structure;
- critique ambiguous natural-language problem statements;
- design executable acceptance checks for finite examples without mistaking them for proofs.

## Core Exposition

Let `I` be admissible inputs and `O` possible outputs. A problem is an acceptance relation `R ⊆ I × O`. For input `x`, the acceptable set is `R(x)={y∈O | (x,y)∈R}`. A total problem has `R(x)≠∅` for every `x∈I`; a partial problem needs behavior for inputs with no solution. If exactly one output is acceptable for every input, the relation is a function.

This model separates the problem from the procedure. Sorting may require any nondecreasing permutation, while mergesort and heapsort are competing procedures. A graph path can be represented by vertex identifiers or edges without changing the abstract reachability relation, provided the representation preserves the required information.

Constraints have distinct ownership:

- **domain constraints** describe meaningful instances, such as nonnegative capacities;
- **representation constraints** describe encodings, such as 64-bit signed integers;
- **output constraints** define acceptable answers, such as distinct indices;
- **operational constraints** restrict access, such as one-pass streaming;
- **resource constraints** bound time, memory, communication, error, or energy.

Do not silently promote a convenience into a domain rule. Requiring an array to be sorted can enable binary search, but it changes the admissible input set. Conversely, a maximum length imposed by an API is not necessarily part of the abstract mathematical problem.

Optimization adds a feasible relation `F` and objective `c(x,y)`. A minimization answer must be feasible and attain `min{c(x,z) | (x,z)∈F}`. An approximation problem replaces equality to the optimum with a stated guarantee. A heuristic without a guarantee still needs output-validity rules and an empirical success criterion.

Input size must follow the representation and cost model. For a graph, both vertices `n` and edges `m` may matter. For an integer `N` encoded in binary, representation length is `Θ(log N)`. For a matrix, dimensions and sparsity can be more informative than a single byte count. State parameters before asymptotic analysis.

## Definitions and Notation

- `I`: admissible input instances.
- `O`: possible output values.
- `R(x,y)`: output `y` is acceptable for input `x`.
- `R(x)`: all acceptable outputs for `x`.
- `F(x,y)`: `y` is feasible for `x` in an optimization problem.
- `c(x,y)`: objective value of a feasible output.
- `|x|`: declared representation length, not automatically numeric magnitude.
- A **promise** restricts which encoded inputs an algorithm is required to handle.
- A **certificate** is evidence checkable against the input and claimed result.

## Mechanisms, Invariants, or Proof Structure

A disciplined formulation pass asks, in order:

1. What real question is being decided or constructed?
2. What mathematical objects are inputs, and which are admissible?
3. What output type is returned?
4. What predicate accepts an output for an input?
5. Can no solution, many solutions, or ties occur?
6. Which representation and numeric conventions affect implementation?
7. Which resource and quality measures matter?

Correctness later decomposes into termination and partial correctness: assuming an admissible input and termination, the returned output satisfies `R`; termination establishes that a total algorithm actually returns. Optimization adds feasibility and dominance over every feasible competitor. These obligations cannot be recovered from code after an ambiguous problem has been chosen.

An executable oracle can expose missing cases for bounded examples:

<!-- bijux-verify: {"id":"two-sum-output-relation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"pair: True\nnone-valid: True\nnone-invalid: False\nreused-index: False\n","stderr":""}} -->
```python
def acceptable(values, target, answer):
    if answer is None:
        return all(
            values[i] + values[j] != target
            for i in range(len(values))
            for j in range(i + 1, len(values))
        )
    i, j = answer
    return 0 <= i < j < len(values) and values[i] + values[j] == target

print("pair:", acceptable([4, 7, 4], 8, (0, 2)))
print("none-valid:", acceptable([1, 2], 8, None))
print("none-invalid:", acceptable([1, 7], 8, None))
print("reused-index:", acceptable([4], 8, (0, 0)))
```

The run checks four instances; the quantified relation, not the run, defines correctness for all instances.

## Alternatives and Trade-Offs

**Relational versus functional output.** Allowing any optimal answer gives implementations freedom; canonical output simplifies reproducibility but adds work and may exclude useful algorithms.

**Rejecting versus normalizing input.** Rejection keeps semantics explicit. Normalization improves usability but must preserve meaning and define how equivalent representations compare.

**Exact versus tolerance-based numeric output.** Exact equality is clean for discrete objects. Floating-point results often need absolute, relative, or problem-specific error bounds, with special handling near zero and for non-finite values.

**Abstract versus machine-bounded integers.** Unbounded integers simplify proofs. Fixed-width arithmetic reflects hardware but introduces overflow semantics. A durable specification states which layer owns the bound.

## Failure Modes and Misconceptions

1. Naming a technique defines a problem. False: “use dynamic programming” constrains a solution method, not acceptable outputs.
2. Examples are a specification. False: finitely many examples underdetermine general behavior.
3. Any optimum is automatically valid. False: feasibility is checked before optimality.
4. “Return a pair” implies distinct indices. False: state `i<j` or another rule.
5. A sorted-input assumption is harmless. False: it changes `I` unless preprocessing is part of the algorithm.
6. No-solution behavior is obvious. False: sentinel, exception, optional value, and proof of totality differ.
7. One input-size variable always suffices. False: graph and matrix costs commonly need multiple parameters.
8. Tests prove universal correctness. False: they supply finite evidence against a quantified claim.
9. Stability is merely an implementation detail. False when equal-key order is observable.
10. Resource limits do not affect correctness. False when exceeding them changes output, termination, or availability.

## Worked Examples

### Example 1

**Question:** Specify maximum of a nonempty integer sequence.

**Reasoning:** Input is sequence `a` with `len(a)>0`; output is an integer `m` appearing in `a` such that every element is at most `m`.

**Conclusion:** Nonemptiness makes the problem total and occurrence prevents an invented upper bound.

### Example 2

**Question:** What is missing from “sort the records by score”?

**Reasoning:** Ascending or descending order, stable treatment of equal scores, key validity, mutation, and output ownership are unspecified.

**Conclusion:** “Sorted” names only one part of the acceptance relation.

### Example 3

**Question:** Specify binary search without prescribing its loop.

**Reasoning:** Input is a nondecreasing sequence and target. Output is an index containing the target or `None` iff absent; duplicates require “any,” first, or last occurrence.

**Conclusion:** Sortedness is a precondition and duplicate policy is an output constraint.

### Example 4

**Question:** Distinguish shortest-path feasibility and optimality.

**Reasoning:** A path must join the named vertices and use graph edges. Only then is its weight compared with all feasible paths; unreachable targets need an explicit result.

**Conclusion:** A low-weight invalid walk is not an optimal path.

### Example 5

**Question:** Why can median be ambiguous?

**Reasoning:** Even-length inputs may use lower middle, upper middle, or the arithmetic mean. The mean may leave the element type or overflow.

**Conclusion:** Output type and even-cardinality policy belong in the problem.

### Example 6

**Question:** Formulate interval overlap.

**Reasoning:** For half-open intervals `[s,e)` with `s<e`, two intervals overlap iff `s1<e2` and `s2<e1`; touching endpoints do not overlap.

**Conclusion:** Endpoint convention determines boundary answers.

### Example 7

**Question:** Is “process a billion edges” a graph constraint?

**Reasoning:** It is an operational scale requirement, not a mathematical graph property. It affects representation, memory, and access strategy.

**Conclusion:** Domain and deployment constraints should be recorded separately.

### Example 8

**Question:** Specify top-k with ties.

**Reasoning:** Exactly `k` items may split equal scores arbitrarily, use a deterministic secondary key, or include all items tied at the boundary and return more than `k`.

**Conclusion:** Tie policy changes both output cardinality and reproducibility.

### Example 9

**Question:** What size describes a sparse graph?

**Reasoning:** `n` vertices and `m` edges expose costs that a single `n` hides; adjacency-matrix and adjacency-list representations have different lengths.

**Conclusion:** Complexity parameters follow relevant structure and representation.

### Example 10

**Question:** Specify approximate square root.

**Reasoning:** Input domain might be finite nonnegative numbers; output `y` can require `|y²-x|≤ε·max(1,x)`, plus policies for NaN, infinity, and negative values.

**Conclusion:** “Approximately equal” requires a metric, tolerance, and exceptional-value policy.

## Cross-Program Connections

- **Theory of Computation:** finite encodings turn decision predicates into languages.
- **Data Structures:** a representation determines supported operations and input length.
- **Software Design:** domain authority determines whether constraints reflect the problem or a chosen system.
- **Testing:** examples and generators probe the acceptance relation but do not replace it.
- **Security:** adversarial inputs exploit ambiguity, overflow, and inconsistent normalization.

## References

- Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. [*Introduction to Algorithms*, 4th ed.](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/) MIT Press, 2022. Publisher record checked 2026-08-28.
- Steven S. Skiena. [*The Algorithm Design Manual*, 3rd ed.](https://link.springer.com/book/10.1007/978-3-030-54256-6) Springer, 2020, DOI 10.1007/978-3-030-54256-6. Publisher record checked 2026-08-28.
- Jon Kleinberg and Éva Tardos. [*Algorithm Design*](https://www.pearson.com/en-ca/subject-catalog/p/algorithm-design/P200000003259/9780321349422). Pearson, 2006. Publisher record checked 2026-08-28.
- Amruth N. Kumar et al. [*Computer Science Curricula 2023*](https://csed.acm.org/wp-content/uploads/2025/11/CS2023-Report.htm). ACM, IEEE Computer Society, and AAAI, DOI 10.1145/3664191; endorsed 2024. Current report checked 2026-08-28.
- C. A. R. Hoare. [“An Axiomatic Basis for Computer Programming.”](https://doi.org/10.1145/363235.363259) *Communications of the ACM* 12(10), 1969, pp. 576–580. DOI record checked 2026-08-28.

## Exercises

### Exercise 1

Rewrite “find the cheapest flight” as inputs, admissibility constraints, outputs, and an acceptance relation. Identify at least three ambiguities.

### Exercise 2

Specify a function that returns the first minimum element of a nonempty sequence. State precondition, postcondition, tie rule, and size measure.

### Exercise 3

Design an acceptance oracle for a proposed result to the two-sum problem. Explain how it validates `None` and give four boundary cases.

### Exercise 4

Compare specifications for exact and approximate matrix multiplication. Discuss numeric type, dimensions, error metric, overflow, and reproducibility.

### Exercise 5

A service must assign jobs to eligible workers while respecting capacity and minimizing maximum load. Formulate inputs, feasibility, objective, infeasibility, ties, and scale parameters. Separate domain from operational constraints.

## Answers to the Exercises

### Answer 1

Input can be origin, destination, departure window, passenger count, and a finite set of flight legs with schedules and prices. Admissible itineraries connect endpoints, respect time order and minimum connections, and have enough capacity. Output is an admissible itinerary whose declared total cost is minimal, or `None` if none exists. Ambiguities include whether “cost” includes taxes and baggage, whether overnight or airport changes are allowed, how ties are broken, and whether prices can change during computation. A complete relation fixes the price snapshot and every feasibility convention.

### Answer 2

Precondition: `a` is a finite nonempty sequence over a totally ordered type. Output is index `i` satisfying `0≤i<len(a)`, `a[i]≤a[j]` for every valid `j`, and `i≤j` for every index whose value equals `a[i]`. The final clause selects the first minimum. A natural size measure is `n=len(a)`; representation cost may also include element width. Empty input is excluded rather than assigned an accidental sentinel.

### Answer 3

For pair `(i,j)`, check integer indices, `0≤i<j<n`, and `a[i]+a[j]=t`. For `None`, quantify over every distinct pair and accept only if none sums to `t`; merely failing to find one is insufficient unless the search is exhaustive or proved complete. Boundary cases include empty and singleton inputs, duplicate values at distinct indices, one value that would require reusing its index, multiple valid pairs, and arithmetic overflow under bounded integers. The executable oracle in this chapter implements the mathematical version with unbounded Python integers.

### Answer 4

Exact multiplication takes compatible matrices over a specified algebraic type and requires every output entry to equal the corresponding dot product. Approximate multiplication must declare floating-point format, accumulation model, and an error bound such as a normwise relative bound with an absolute term near zero. Fixed-width integer multiplication needs overflow semantics. Parallel floating-point reductions may be nondeterministic, so bitwise reproducibility and tolerance-based acceptance are different contracts. Dimensions `(m,k,n)`, sparsity, and representation length are relevant scale parameters.

### Answer 5

Inputs are jobs with demand and eligibility sets, workers with capacities, and a fixed snapshot of available workers. A feasible assignment maps every job to an eligible worker without exceeding capacity. Its load vector sums assigned demand per worker; the objective minimizes the maximum load among feasible assignments. Return `None` exactly when no feasible assignment exists. A secondary lexicographic assignment rule can make ties deterministic, or the relation can permit any optimum. Eligibility and capacity are domain constraints; latency, memory, update frequency, and distributed placement are operational constraints. Scale parameters include job count, worker count, eligibility-edge count, demand bit width, and update rate.
