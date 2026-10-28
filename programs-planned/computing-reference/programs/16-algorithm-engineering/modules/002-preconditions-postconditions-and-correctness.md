---
module_id: ALGE-002
program: Algorithm Engineering
level: 1
module_number: 2
title: Preconditions, Postconditions, and Correctness
status: complete
last_verified: 2026-08-29
---

# Preconditions, Postconditions, and Correctness

## One-Page Review

### Governing question

How can an algorithm contract state exactly what callers must establish, what every permitted execution must guarantee, and what proof is still needed to claim partial or total correctness?

### Essential definitions

- A **program state** assigns values to variables, memory locations, and abstract resources relevant to the algorithm.
- A **precondition** \(P\) is a predicate required of the initial state/input for the normal correctness claim.
- A **postcondition** \(Q\) is a predicate that must hold of initial state, final state, returned value, and observable effects after successful termination.
- A **frame/effect condition** says which state may change and which must remain unchanged.
- A **Hoare triple** \(\{P\}\ C\ \{Q\}\) expresses partial correctness: if \(P\) holds and command \(C\) terminates normally, then \(Q\) holds.
- **partial correctness** proves the result is correct if termination occurs; it does not prove termination.
- **total correctness** combines partial correctness with termination for every state satisfying \(P\).
- A **loop invariant** is preserved across iterations and connects the precondition to the postcondition; it is developed in the next module.
- A **variant/ranking function** decreases in a well-founded order and supports termination.
- **refinement** replaces a specification/algorithm with one that accepts at least the required inputs and provides at least the required guarantees.

### Central model, mechanism, or theorem

For initial state \(\sigma\), input \(x\), command \(C\), final state \(\sigma'\), and result \(r\), partial correctness is

\[
\forall \sigma,x,\sigma',r:
P(\sigma,x)\land
\langle C,\sigma,x\rangle\Downarrow(\sigma',r)
\Rightarrow Q(\sigma,x,\sigma',r).
\]

Total correctness adds:

\[
\forall \sigma,x:
P(\sigma,x)\Rightarrow
\exists \sigma',r:
\langle C,\sigma,x\rangle\Downarrow(\sigma',r).
\]

For nondeterministic execution, every permitted terminating outcome must satisfy \(Q\) under the usual demonic correctness reading. Testing supplies selected observations; it does not establish these universal implications.

### Critical invariants

- State the mathematical domain separately from representation, API validation, and environmental assumptions.
- Make the precondition neither an undocumented convenience nor a disguised description of the desired output.
- Define normal, exceptional, infeasible, malformed, timeout, and resource-exhaustion outcomes.
- Relate postconditions to the initial state; otherwise permutation, conservation, stability, and mutation claims can disappear.
- Specify frame/effects: correct return values do not excuse corrupted unrelated state.
- Prove soundness for every permitted result; prove completeness/optimality when the problem requires them.
- Partial correctness never implies termination; total correctness requires a separate well-founded argument.
- A weaker precondition accepts more states; a stronger postcondition promises more.
- Concrete integer, floating-point, memory, concurrency, and I/O semantics must match the proof model.
- A verified implementation can satisfy a wrong specification; validate the contract against stakeholder/domain intent.

### Common failures

Common failures include saying “assume the input is valid” without defining valid; using a precondition to exclude difficult but legitimate cases; writing a postcondition only for examples; omitting no-solution and exceptional behavior; confusing an assertion check with proof; proving output validity but not optimality; ignoring mutation and aliasing; assuming mathematical integers while code overflows; treating partial correctness as total; testing termination instead of proving it; accepting one nondeterministic outcome when another violates the postcondition; strengthening preconditions during optimization; weakening postconditions during replacement; and claiming system safety from algorithm correctness alone.

### Compact example

For first occurrence in a sorted integer sequence \(a\), precondition: \(a\) is finite and nondecreasing. Postcondition: return \(-1\) exactly if target \(t\) is absent; otherwise return \(i\) with \(0\le i<|a|\), \(a_i=t\), and \(\forall j<i:a_j\ne t\). Frame: \(a\) is unchanged. A binary-search implementation must prove the index property and termination; returning any matching duplicate satisfies a weaker, different contract.

### Connections

[ALGE-001](./001-problem-statements-inputs-outputs-and-constraints.md) supplies input/output relations. [TPROG-001](../../07-programming-languages-theory-of-programming/modules/001-propositions-predicates-and-formal-specifications.md) supplies predicates and specifications. [STQE-002](../../13-software-engineering-testing-and-quality-engineering/modules/002-specifications-expectations-and-test-oracles.md) turns contract fragments into scoped test oracles. [ALGE-003](../ROADMAP.md) develops loop invariants as the main iterative proof mechanism.

## Governing Question

Given a precise computational problem, how should we write and discharge a contract that separates caller obligations, algorithm guarantees, termination, effects, exceptional behavior, and implementation assumptions?

A correctness statement is conditional. “Binary search is correct” omits sortedness, index convention, duplicate policy, comparison semantics, mutation, and termination. A contract turns that slogan into a quantified proposition that can be proved, tested, implemented, reviewed, and refined.

## Why This Matters

Algorithms often appear correct because examples exercise their intended domain. In production, empty inputs, duplicate keys, overflow, NaN, aliasing, cancellation, stale state, or malformed encodings reveal that the real contract was never written. The code then chooses policy accidentally.

Contracts also control optimization. A faster replacement is valid only if it accepts the required initial states and preserves all observable guarantees, including stability, exactness, side effects, and errors. Without a contract, benchmark winners can silently solve an easier problem.

Formal proof does not eliminate validation. It establishes that a model/implementation satisfies stated predicates. If the postcondition omits a safety constraint or the precondition excludes realistic inputs, the proof can be flawless and the delivered behavior wrong. Correctness engineering therefore connects domain meaning, formal obligations, executable checks, and model correspondence.

## Prerequisites and Retrieval

Retrieve:

- predicate, implication, conjunction, universal/existential quantification, substitution, and logical equivalence;
- relation, function, partial function, set inclusion, and refinement;
- initial/final state, variable, assignment, expression, branch, loop, recursion, and termination;
- input/output relation, feasible result, optimal result, tie policy, and malformed input;
- mathematical versus bounded integer, floating-point semantics, alias, mutation, exception, and side effect;
- proof, counterexample, test oracle, invariant, and well-founded order.

You should be able to explain why \(P\Rightarrow Q\) differs from testing \(P,Q\) on examples, and why “returns a matching index” does not imply “returns the first matching index.”

## Learning Objectives

After completing this module, you should be able to:

1. write preconditions, postconditions, frame conditions, and exceptional outcomes over explicit states;
2. interpret a Hoare triple without smuggling in termination;
3. decompose total correctness into partial correctness and termination;
4. apply assignment, sequencing, conditional, and consequence rules to small algorithms;
5. compare contracts by precondition weakness and postcondition strength;
6. specify relational, optimization, nondeterministic, and approximate outputs;
7. identify hidden representation, aliasing, mutation, overflow, and environment assumptions;
8. design executable contract checks without mistaking them for universal proof;
9. review whether an optimized/replacement algorithm refines its required contract;
10. separate formally verified algorithm claims from high-consequence system validation and authority.

## Core Exposition

### Begin with states and observations

An algorithm transforms an initial abstract state into one or more possible outcomes. The state includes everything relevant to the claim: input sequence, mutable array, heap, graph, random source, external store, and sometimes initial copies used only in specifications.

Write \(a_0\) for the initial sequence and \(a\) for the final sequence. This “old” relation is essential. “Final \(a\) is sorted” does not prove sorting: an implementation that returns an empty sequence is sorted. A sorting postcondition also needs permutation/multiset preservation:

\[
sorted(a)\land multiset(a)=multiset(a_0).
\]

If stable sorting is required, relate equal-key records’ relative order. If in-place behavior matters, specify identity/space/effects separately. One word—“sort”—contains several contracts.

### Preconditions define the obligation boundary

A precondition states what the caller or surrounding proof must establish before the algorithm’s normal guarantee applies. Examples:

- a binary-search sequence is nondecreasing under comparator \(cmp\);
- graph edge weights are nonnegative for Dijkstra’s algorithm;
- divisor is nonzero;
- indices denote a valid half-open range;
- a buffer has enough writable capacity and does not overlap forbidden memory;
- arithmetic operations remain within the modeled domain.

Preconditions are not necessarily runtime checks. A proof rule treats \(P\) as an assumption; an API may validate and return an error, a type may make invalid states unrepresentable, or a trusted caller may establish it. Document which mechanism owns the obligation.

Avoid “precondition laundering”: excluding empty input, duplicates, disconnected graphs, negative values, or adversarial distributions merely because an implementation fails there when the problem includes them. Narrowing the domain changes the problem and must be authorized.

### Postconditions define every permitted successful result

A postcondition can depend on input, old state, final state, result, and effects. For a search returning \(i\):

\[
i=-1\iff \forall j\in[0,n):a_j\ne t,
\]

or

\[
0\le i<n\land a_i=t
\]

for a successful outcome. If duplicates exist, “any,” “first,” and “last” match are different relations.

For optimization, separate feasibility from optimality:

\[
F(x,y)\land
\forall z\,[F(x,z)\Rightarrow c(x,y)\le c(x,z)].
\]

A proof of feasibility alone does not establish an optimal solver. Approximation replaces the dominance clause with a stated ratio/additive/error guarantee and required domain conditions.

Postconditions should include conservation, provenance, stability, deterministic tie-breaking where required, and data-structure validity. What is not specified is not established by the correctness proof.

### Frame conditions control what may change

An algorithm can return the correct number while corrupting another array, consuming input, changing global state, leaking data, or mutating a shared comparator. A frame condition identifies modified locations/effects and preserves the rest.

Examples:

- pure search: input sequence and all external state unchanged;
- in-place partition: only segment \(a[lo:hi)\) may change; elements outside are unchanged;
- graph traversal: graph unchanged; caller-provided visitation map may change according to contract;
- randomized selection: random-source state advances, but input mutation follows an explicit rule.

Aliasing complicates frames. If two parameters refer to overlapping storage, modifying one changes the other. Either forbid overlap as a precondition or specify alias-aware effects. “Does not modify parameter \(b\)” is false if \(b\) aliases modified \(a\).

### Normal and exceptional outcomes form one contract

Real algorithms can return a value, report no solution, reject malformed input, overflow, exhaust resources, be cancelled, or encounter I/O failure. Model an outcome sum:

\[
Outcome=Success(y)\mid NoSolution\mid Invalid(e)\mid Failure(e).
\]

Give each branch pre/post/effect obligations. A successful result after partial mutation may be acceptable; an exception after partial mutation may violate atomicity. “Throws an exception” is incomplete without type, condition, state after failure, and resource cleanup.

Distinguish domain absence from invalid input. Two-sum returning `None` because no pair exists is a valid mathematical answer under its contract. Passing a malformed sequence may be invalid. Conflating them makes clients mis-handle recoverable outcomes.

### Partial correctness says “if it returns”

The Hoare triple

\[
\{P\}\ C\ \{Q\}
\]

means: for any initial state satisfying \(P\), every normal terminating execution of \(C\) ends in a state satisfying \(Q\). It can be true of `while true do skip` for any \(Q\), because there is no normal terminating execution to falsify the implication. This is not a paradox; it exposes that termination is a separate obligation.

Partial correctness needs soundness over all terminating outcomes. For nondeterministic algorithms under demonic semantics, one good execution is insufficient; every permitted terminating execution must meet \(Q\). Angelic/existential specifications use another convention and must say so.

### Total correctness adds termination

Total correctness requires:

1. \(P\) establishes the algorithm’s invariant/proof setup;
2. every step preserves correctness obligations;
3. on termination, \(Q\) follows;
4. every execution from \(P\) terminates.

For loops/recursion, termination often uses a variant \(V\) in a well-founded set such as nonnegative integers. Show \(V\ge0\) while continuing and \(V\) strictly decreases each iteration/recursive call. Bounded input consumption or finite unexplored-state count are common measures.

Termination is relative to semantics. Mathematical unit-cost arithmetic may terminate while a concrete operation traps; blocking I/O may not return; unfair scheduling can starve a thread. State whether correctness covers pure algorithm, sequential implementation, or concurrent/system execution.

### Basic Hoare rules expose proof structure

For assignment \(x:=E\), work backward from desired \(Q\):

\[
\{Q[x\leftarrow E]\}\ x:=E\ \{Q\}.
\]

The precondition substitutes expression \(E\) for occurrences of the final \(x\) in \(Q\). To prove final \(x=old(x)+1\), preserve an initial logical name \(x_0\); assignment alone cannot make `old` implicit.

For sequencing:

\[
\frac{\{P\}C_1\{R\}\quad\{R\}C_2\{Q\}}
{\{P\}C_1;C_2\{Q\}}.
\]

The intermediate assertion \(R\) connects commands.

For conditional:

\[
\frac{\{P\land B\}C_t\{Q\}\quad
\{P\land\neg B\}C_f\{Q\}}
{\{P\}\ if\ B\ then\ C_t\ else\ C_f\ \{Q\}}.
\]

Both branches must establish the same promised postcondition (or a postcondition implied by branch-specific results).

The consequence rule permits strengthening the proof entry and weakening the proof exit:

\[
\frac{P\Rightarrow P'\quad\{P'\}C\{Q'\}\quad Q'\Rightarrow Q}
{\{P\}C\{Q\}}.
\]

Direction matters. If code needs \(x>0\), proving caller has \(x>1\) suffices for that call, but it does not make the algorithm valid for every \(x>0\) if its public precondition became \(x>1\).

### Contract strength and refinement

A precondition \(P_1\) is weaker than \(P_2\) when \(P_2\Rightarrow P_1\): \(P_1\) accepts at least as many states. A postcondition \(Q_1\) is stronger than \(Q_2\) when \(Q_1\Rightarrow Q_2\): \(Q_1\) promises at least as much.

A replacement that must honor an existing contract should not require a stronger precondition or provide a weaker postcondition/effect guarantee. It may accept more inputs or guarantee more. This is the contract-level intuition behind substitutability.

Refinement also concerns nondeterminism. If a specification permits any minimum element’s index, an implementation returning the first minimum refines it. Returning an arbitrary local minimum does not. Deterministic tie-breaking narrows permitted results and may be useful for reproducibility but adds an obligation.

### Weakest preconditions support backward derivation

For command \(C\) and desired postcondition \(Q\), \(wp(C,Q)\) is the weakest predicate on initial states sufficient to guarantee termination in a \(Q\)-state under Dijkstra’s total-correctness interpretation. A liberal variant \(wlp\) captures partial correctness.

Backward calculation can derive code and proof together:

- assignment uses substitution;
- sequence composes predicate transformers backward;
- conditionals combine branch obligations;
- loops require invariants and termination arguments.

“Weakest” means least restrictive among sufficient predicates, not easiest to read. Real specifications often choose a stronger human meaningful precondition for modularity and validation.

### Mathematical and executable semantics must correspond

A proof over \(\mathbb Z\) does not cover 32-bit signed overflow. A comparator assumed to be a total order may return inconsistent results for NaN or mutable keys. A mathematical set loses duplicates; an array retains them. A unit-cost multiplication may have size-dependent cost.

Choose one:

- prove absence of overflow under preconditions;
- use arbitrary-precision arithmetic;
- model modular/wrapping arithmetic explicitly;
- treat overflow as an exceptional outcome;
- use checked operations and prove their result path.

For floating-point algorithms, exact postconditions may be impossible or wrong. State rounding mode, exceptional values, conditioning, error bound, stability, and units. Empirical tolerance is not a derived correctness theorem.

### Proof, testing, and validation have different roles

A deductive proof covers all states in its formal domain if axioms, semantics, proof, and toolchain are sound. Tests exercise selected concrete states and are excellent at exposing specification/implementation correspondence faults. Static analyzers and proof assistants automate subsets of obligations. None validates stakeholder intent automatically.

Use a layered assurance argument:

\[
intent\rightarrow problem\ relation\rightarrow contract
\rightarrow algorithm\ proof\rightarrow implementation\ correspondence
\rightarrow operational\ evidence.
\]

Each arrow can fail. A correct algorithm can be implemented incorrectly; a verified program can solve the wrong problem; operational configuration can violate a precondition.

## Definitions and Notation

Let \(\Sigma\) be program states. Predicates \(P,Q:\Sigma\to\{true,false\}\). For result-returning commands, model \(Q(\sigma_0,\sigma_1,r)\) so initial/final relation is explicit. Big-step judgment

\[
\langle C,\sigma_0\rangle\Downarrow(\sigma_1,r)
\]

means \(C\) terminates normally from \(\sigma_0\) with final state/result.

Partial correctness:

\[
\models\{P\}C\{Q\}
\iff
\forall\sigma_0,\sigma_1,r:
P(\sigma_0)\land
\langle C,\sigma_0\rangle\Downarrow(\sigma_1,r)
\Rightarrow Q(\sigma_0,\sigma_1,r).
\]

Total correctness additionally requires termination for every \(P\)-state. If semantics is nondeterministic, quantify over every possible terminating final outcome for partial correctness and require every maximal execution to terminate for demonic total correctness.

Define contract ordering \(K_1\sqsubseteq K_2\) (“\(K_2\) refines \(K_1\)”) when \(K_2\) accepts at least \(K_1\)’s required initial states and every behavior of \(K_2\) on those states satisfies \(K_1\)’s post/frame obligations. Exact relational definitions depend on exceptional outcomes and nondeterminism.

## Mechanisms, Invariants, or Proof Structure

Use this correctness workflow:

1. **Recover the problem relation:** admissible inputs and acceptable/optimal outputs.
2. **Choose the state model:** old/current values, representation, aliases, environment, and effects.
3. **Write preconditions:** domain, structure, numeric, ordering, capacity, and environmental assumptions.
4. **Write outcomes:** success, absence, invalidity, exceptions, cancellation, and resource failure.
5. **Write post/frame conditions:** value, relation to old state, conservation, optimality, mutation, and unchanged state.
6. **Prove partial correctness:** use assignments, branch cases, sequence assertions, invariants, induction, or other appropriate arguments.
7. **Prove termination:** supply decreasing well-founded variant or another totality argument.
8. **Check refinement:** no unauthorized stronger precondition or weaker post/effect behavior.
9. **Connect implementation:** overflow, comparator, memory, concurrency, I/O, compiler, and representation assumptions.
10. **Verify and validate:** run boundary/adversarial tests and independently review whether the contract is the right one.

The invariants are explicit domain, old/new-state relation, all-outcome coverage, no partial-as-total inference, proof-model correspondence, and contract strength preserved during replacement.

This executable implementation finds the first occurrence in a finite sorted integer list. The checker evaluates the concrete postcondition and frame for selected cases. It is not a universal proof; the mathematical proof uses the interval invariant and a decreasing interval length, developed fully in the next module.

<!-- bijux-verify: {"id":"first-occurrence-contract","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"values=[] target=4 result=-1 pre=True post=True frame=True\nvalues=[1, 2, 2, 5] target=2 result=1 pre=True post=True frame=True\nvalues=[1, 2, 2, 5] target=4 result=-1 pre=True post=True frame=True\nvalues=[2, 1] target=1 pre=False result=outside-contract\n","stderr":""}} -->
```python
def nondecreasing(values):
    return all(values[i] <= values[i + 1] for i in range(len(values) - 1))

def first_occurrence(values, target):
    low, high = 0, len(values)
    while low < high:
        middle = (low + high) // 2
        if values[middle] < target:
            low = middle + 1
        else:
            high = middle
    return low if low < len(values) and values[low] == target else -1

def postcondition(original, target, result):
    matches = [i for i, value in enumerate(original) if value == target]
    expected = matches[0] if matches else -1
    return result == expected

for values, target in (
    ([], 4),
    ([1, 2, 2, 5], 2),
    ([1, 2, 2, 5], 4),
    ([2, 1], 1),
):
    before = list(values)
    pre = nondecreasing(values)
    if not pre:
        print(f"values={values} target={target} pre=False result=outside-contract")
        continue
    result = first_occurrence(values, target)
    post = postcondition(before, target, result)
    frame = values == before
    print(
        f"values={values} target={target} result={result} "
        f"pre=True post={post} frame={frame}"
    )
```

For valid inputs, the checker’s expected result is computed by a simpler linear specification oracle, reducing common-mode risk. The code still assumes Python integer/comparison/list semantics and finite in-memory inputs.

## Alternatives and Trade-Offs

**Natural-language contracts** are accessible to domain experts but invite ambiguity. **Formal predicates** enable proof and automation but can omit intent behind precise symbols. Maintain both with traceability and examples that clarify rather than redefine.

**Runtime validation** catches violated preconditions at the boundary but adds cost and cannot always check global properties cheaply. **Static types/proofs** move evidence earlier but have modeling/tool costs. **Trusted callers** reduce repeated checks but enlarge the trusted base. Allocate by consequence and ownership.

**Strong postconditions** support reuse and safe optimization but cost more to prove/maintain. **Weak postconditions** admit more implementations but may not serve callers. Specify the weakest guarantee that fully meets the real problem—not a weaker convenient claim.

**Pure algorithms** simplify frame reasoning and parallel use but may allocate/copy. **In-place algorithms** reduce memory/movement but require alias/mutation proofs and can leave partial state on failure.

**Total APIs** encode invalid/no-solution outcomes and ease composition. **Partial APIs** can be mathematically clean when preconditions are statically guaranteed, but misuse may crash or corrupt. Make partiality visible in types/names/contracts.

**Exact arithmetic contracts** offer clear proofs. **Approximate/numerical contracts** reflect real computation but need error analysis, units, rounding, and stability. Do not replace derivation with a magic epsilon.

**Manual proofs** teach structure and expose assumptions. **Mechanized proofs** improve checking and scale certain obligations but rely on formalized semantics, specifications, tactics, kernels, and extraction/compilation correspondence. Both require human validation of what was specified.

## Failure Modes and Misconceptions

- **“Precondition means input validation.”** It is a logical assumption; validation is one enforcement mechanism.
- **“The caller violated the precondition, so any behavior is acceptable.”** Only if the public/system contract truly delegates that obligation; safety/security boundaries may still require containment.
- **“A successful assertion proves correctness.”** It proves one predicate at one execution point under that run.
- **“The function returned, so total correctness holds.”** Totality quantifies over every admissible state.
- **“Partial correctness is almost total.”** It can hold vacuously for a nonterminating command.
- **“The output is valid, so the optimizer is correct.”** Optimality/approximation is an additional quantified obligation.
- **“Sorted output proves sorting.”** Preservation/permutation and stability may be missing.
- **“Parameters not assigned are unchanged.”** Aliasing and external effects can invalidate that frame.
- **“Any matching duplicate is fine.”** Only if the postcondition permits any match.
- **“A stronger precondition is safer.”** It reduces supported inputs and may violate refinement/substitutability.
- **“A stronger postcondition is always free.”** It constrains implementations and can change cost/determinism.
- **“Mathematical proof covers machine arithmetic.”** Only with proven correspondence or explicit bounded/modular semantics.
- **“Randomized success on most runs is correctness.”** Probability/error and adversary model must be part of the contract.
- **“Verified means the system is safe.”** Verification is relative to specification/model; hazards and intended use need validation and authority.

## Worked Examples

### Example 1

**Question:** What contract describes integer division?

**Reasoning:** For Euclidean division with \(a\ge0,b>0\), return \(q,r\) such that \(a=bq+r\) and \(0\le r<b\). Without sign/rounding conventions, negative operands admit competing quotient/remainder policies. Division by zero needs invalid/exception behavior.

**Conclusion:** Preconditions and postconditions remove arithmetic-policy ambiguity.

### Example 2

**Question:** Does `{true} while true do skip {false}` satisfy partial correctness?

**Reasoning:** Yes under standard partial-correctness semantics: no normal terminating execution reaches a state violating `false`. It is not totally correct because it never terminates.

**Conclusion:** Partial correctness alone says nothing about termination.

### Example 3

**Question:** An algorithm returns a sorted empty list for every input. Which sorting obligation catches it?

**Reasoning:** Sortedness holds vacuously, but multiset equality with the initial list fails for every nonempty input. A stable-sort contract would additionally preserve order among equal-key records.

**Conclusion:** Relate the post-state to the pre-state, not only to itself.

### Example 4

**Question:** Apply the assignment rule to prove `{x=4} x:=x+3 {x=7}`.

**Reasoning:** Substitute \(x+3\) for final \(x\) in postcondition \(x=7\), giving precondition \(x+3=7\), equivalent to \(x=4\). The assignment axiom then yields the triple.

**Conclusion:** Assignment proof calculates the required precondition backward.

### Example 5

**Question:** A minimum finder returns index 3, whose value is smaller than its neighbors. Is it correct?

**Reasoning:** That proves a local property only. A global-minimum contract requires \(a_3\le a_j\) for every valid index \(j\), plus tie/index and empty-input policy. One counterexample elsewhere refutes correctness.

**Conclusion:** Match the proof’s quantifier to the required optimization claim.

### Example 6

**Question:** Can an optimized search require nonempty input when the original accepted empty input?

**Reasoning:** That strengthens the precondition and removes a previously supported state. Unless the public contract is deliberately changed, the optimization is not a refinement. It should preserve the empty-input no-result behavior.

**Conclusion:** Faster code cannot silently narrow the domain.

### Example 7

**Question:** A procedure returns the correct count but sorts its input as a side effect. Is it correct?

**Reasoning:** It meets the value predicate but violates a frame condition requiring the input unchanged. If mutation was unspecified, callers cannot reason safely; make the intended effect explicit.

**Conclusion:** Correctness includes observable effects, not only return values.

### Example 8

**Question:** A proof assumes unbounded integers, while code computes `middle=(low+high)//2` in fixed-width arithmetic. What is missing?

**Reasoning:** `low+high` can overflow even when both indices are valid. Prove a bound, use `low+(high-low)//2` under proven subtraction bounds, checked arithmetic, or model wrapping explicitly. Then verify language semantics.

**Conclusion:** Representation correspondence is a correctness obligation.

### Example 9

**Question:** Is a proved route-planning algorithm enough to authorize emergency medical transport?

**Reasoning:** A proof can establish path feasibility/optimality under a graph, weights, and constraints. It cannot validate live road data, clinical urgency, vehicle limits, dispatch policy, fairness, communications, or human override. No external academic, clinical, emergency-service, safety, regulatory, or practitioner review is claimed. Named qualified domain, clinical, operations, safety, human-factors, software/data, security/privacy, quality, and regulatory authorities must validate assumptions and authorize use.

**Conclusion:** Algorithm correctness is necessary evidence within, not a substitute for, system assurance.

### Example 10

**Question:** A randomized algorithm returns a valid answer with probability at least 0.99. Is `Q` simply “answer is valid”?

**Reasoning:** Not for every execution if invalid answers are possible. The contract must include random source/adversary/input conditions, probability space, error type, confidence/amplification, and whether failure is detectable. A Las Vegas algorithm instead always returns a valid answer but has randomized runtime.

**Conclusion:** Randomized correctness quantifies over an explicit probability model.

## Cross-Program Connections

- [Theory of Programming](../../07-programming-languages-theory-of-programming/ROADMAP.md) develops Hoare logic, operational semantics, refinement, and proof systems.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) derives boundary/property oracles from contracts and tests model correspondence.
- [Theory of Computation & Complexity](../../15-theory-of-computation-and-complexity/ROADMAP.md) separates partial recognition from total decision and formalizes resource-independent computability.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies representation invariants, aliasing, and mutation obligations.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) treats validation, bounds, authorization, and side effects adversarially.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) validates algorithm assumptions within physical, organizational, and lifecycle systems.

## References

1. C. A. R. Hoare. [“An Axiomatic Basis for Computer Programming”](https://doi.org/10.1145/363235.363259), *Communications of the ACM* 12(10), 1969, pp. 576–580. Foundational Hoare triples, assignment, composition, conditionals, loops, and machine-independent proof.
2. Robert W. Floyd. “Assigning Meanings to Programs.” In *Mathematical Aspects of Computer Science*, Proceedings of Symposia in Applied Mathematics 19, American Mathematical Society, 1967, pp. 19–32. Foundational assertion/invariant method for flowcharts.
3. Edsger W. Dijkstra. [“Guarded Commands, Nondeterminacy and Formal Derivation of Programs”](https://doi.org/10.1145/360933.360975), *Communications of the ACM* 18(8), 1975, pp. 453–457. Guarded commands and predicate-transformer derivation.
4. Edsger W. Dijkstra. *A Discipline of Programming*. Prentice-Hall, 1976. Weakest preconditions and correct-program derivation.
5. David Gries. *The Science of Programming*. Springer, 1981. Predicate logic, specifications, invariants, termination, and program derivation.
6. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. *Introduction to Algorithms*, fourth edition, MIT Press, 2022. Algorithm specifications, loop invariants, correctness, termination, and engineering analysis.
7. ACM, IEEE Computer Society, and AAAI. [*Computer Science Curricula 2023*](https://doi.org/10.1145/3664191), endorsed 2024, Algorithmic Foundations. Current curricular context for algorithm correctness, invariants, selection, and computational models; consulted 2026-08-29.

## Exercises

### Exercise 1

Write a complete contract for returning the maximum element’s first index from a finite integer sequence.

### Exercise 2

Use Hoare assignment and sequencing rules to prove `{x=2} y:=x+1; x:=2*y {x=6∧y=3}`.

### Exercise 3

Diagnose a sorting implementation proven to return a nondecreasing sequence but whose contract omits permutation, mutation, stability, overflow, and exceptional outcomes.

### Exercise 4

Compare two first-occurrence search implementations where the replacement is faster but requires nonempty input, mutates the sequence, and can return any matching duplicate.

### Exercise 5

Specify correctness and assurance for an unfamiliar insulin-dose calculation algorithm. Separate mathematical proof, executable correspondence, domain validation, and release authority.

## Answers to the Exercises

### Answer 1

Input \(a\) is a finite nonempty integer sequence; if empty input is legitimate, define a separate `NoSolution` outcome instead of hiding it. Successful result \(i\) satisfies \(0\le i<|a|\), \(\forall j\in[0,|a|):a_i\ge a_j\), and \(\forall j<i:a_j<a_i\) or, more directly, \(i=\min\{j\mid a_j=\max(a)\}\). The input sequence and all unrelated state remain unchanged.

For bounded implementation integers, comparisons must implement the mathematical order without overflow/conversion errors; values, indexing, aliasing, concurrency, cancellation, and malformed representation need policies. Total correctness requires termination for every admissible finite sequence, commonly by scanning a strictly advancing index.

### Answer 2

Work backward. Desired final postcondition is \(x=6\land y=3\). For assignment \(x:=2y\), substitute \(2y\) for final \(x\), yielding \(2y=6\land y=3\), equivalent to \(y=3\). Thus:

\[
\{y=3\}\ x:=2y\ \{x=6\land y=3\}.
\]

For \(y:=x+1\), substitute \(x+1\) for final \(y\) in intermediate assertion \(y=3\), giving \(x+1=3\), equivalent to \(x=2\):

\[
\{x=2\}\ y:=x+1\ \{y=3\}.
\]

The sequencing rule composes them. Both assignments terminate under the simple mathematical arithmetic semantics. A machine implementation additionally needs overflow/type semantics, though these constants are safe in ordinary signed representations.

### Answer 3

The proof allows deletion, duplication, fabrication, and replacement with the empty sequence because those can be nondecreasing. Add multiset equality between initial/final sequence; add stability relation if equal-key order matters. Specify whether sorting is in-place or returns a new sequence, exact modifiable range, aliasing, and unchanged external state. Define comparator requirements (total/preorder as appropriate), behavior for inconsistent comparison/NaN, empty/singleton input, malformed keys, allocation/resource failure, cancellation, and partial mutation.

If arithmetic computes keys/indices, connect mathematical and bounded semantics. Then prove partial correctness (sortedness plus preservation/stability/frame), prove termination, and test implementation correspondence including duplicates, boundaries, already/reverse-sorted data, exceptions, and aliases. A stronger contract may require different code; that is the point of discovering the real problem.

### Answer 4

The original contract accepts empty sorted sequences, preserves input, and returns the first match. The replacement strengthens the precondition (nonempty), weakens the frame (mutation), and weakens the postcondition (any duplicate). It is not a refinement even if faster and even if ordinary benchmarks exclude empty/duplicate cases.

Repair by handling empty input, preserving input or obtaining explicit permission for mutation, and retaining the lower-bound/first-match rule. Alternatively propose a versioned contract change with impact evidence and caller migration; do not label it a transparent optimization. Compare performance only after both implementations satisfy the same required relation/effects.

### Answer 5

Define units and representation; admissible patient/context inputs; missing/stale/conflicting measurement policy; drug/concentration, route, timing, and device constraints; mathematical formula; rounding/saturation; contraindications; dose bounds; output explanation/provenance; and invalid/no-recommendation/escalation outcomes. The postcondition states the dose and every boundary/constraint relative to initial inputs; frame conditions prevent unauthorized record/device mutation. Termination and numerical error/overflow are explicit.

Prove algebra, units, bounds, branch coverage, monotonicity where clinically justified, exceptional behavior, and termination under a formal model. Independently recompute reference cases, test boundaries/adversarial unit conversions, verify code/compiler/configuration correspondence, and validate data provenance. These activities do not establish clinical appropriateness by themselves.

No external academic, clinical, regulatory, safety, or practitioner review is claimed. Named qualified endocrinology/clinical, pharmacy, nursing/workflow, clinical-safety, human-factors, software/numerical, data, cybersecurity/privacy, quality/independent-assurance, device, and regulatory authorities must validate intended use, patient populations, evidence, hazards, overrides, monitoring, residual risk, and change/release authority. Unresolved critical specification, model-correspondence, or clinical evidence blocks deployment regardless of proof status.
