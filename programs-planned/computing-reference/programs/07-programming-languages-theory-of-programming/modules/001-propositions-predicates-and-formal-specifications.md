---
module_id: TPROG-001
program: Programming Languages: Theory of Programming
level: 1
module_number: 1
title: Propositions, Predicates, and Formal Specifications
status: complete
last_verified: 2026-08-29
---

# Propositions, Predicates, and Formal Specifications

## One-Page Review

### Governing question

How can engineers turn informal claims about programs and states into formulas whose meaning, assumptions, counterexamples, and proof obligations are precise enough to check?

### Essential definitions

- A **proposition** is a declarative claim assigned a truth value under an interpretation; a **propositional variable** stands for such a claim.
- **syntax** determines well-formed formulas; **semantics** assigns meaning/truth under a valuation, structure, and variable assignment.
- The connectives **negation** $\neg$, **conjunction** $\land$, **disjunction** $\lor$, **implication** $\rightarrow$, and **biconditional** $\leftrightarrow$ construct formulas.
- A formula is **satisfiable** if true under at least one interpretation, **valid** if true under every permitted interpretation, and **unsatisfiable** if true under none.
- $\Gamma\models\varphi$ (**semantic entailment**) means every model satisfying all assumptions in $\Gamma$ also satisfies conclusion $\varphi$.
- Formulas $\varphi,\psi$ are **logically equivalent** when they have the same truth value under every permitted interpretation.
- A **predicate** $P(x_1,\ldots,x_n)$ denotes a truth-valued property/relation over a domain; an open formula becomes a proposition after variables are assigned or bound.
- $\forall x.P(x)$ asserts (P) for every domain element; $\exists x.P(x)$ asserts at least one witness.
- A variable occurrence is **bound** by a quantifier or **free** relative to a formula; substitution must avoid capture.
- A **formal specification** states permitted inputs/states/behaviors/results using a language with defined syntax and semantics.
- A **precondition** restricts admissible initial states; a **postcondition** relates initial state, result, and final state; an **invariant** holds at designated states throughout a computation/model.

### Central model, mechanism, or theorem

For propositional formula $\varphi$, valuation $v:Atoms\rightarrow\{\mathsf F,\mathsf T\}$ extends compositionally, for example

$$
\llbracket\varphi\rightarrow\psi\rrbracket_v=\neg\llbracket\varphi\rrbracket_v\lor\llbracket\psi\rrbracket_v.
$$

For first-order predicates, a structure $\mathcal M=(D,I)$ supplies a domain and interpretations for symbols, and assignment $\eta$ supplies free variables. Quantification changes the assignment:

$$
\mathcal M,\eta\models\forall x.\varphi
\iff
\text{for every }d\in D,\ \mathcal M,\eta[x\mapsto d]\models\varphi.
$$

A function contract can be a relation $Pre(s)\land Exec(s,s',r)\Rightarrow Post(s,s',r)$. It proves nothing until `Exec`, domain, arithmetic, failure/termination and observation semantics are connected to the implementation.

### Critical invariants

- Separate formula syntax from its interpretation/model; a symbol's spelling does not determine meaning.
- State the domain, types/sorts, arithmetic/overflow, equality, time and undefined/error behavior.
- Distinguish validity, satisfiability, entailment, equivalence, provability and empirical truth.
- Parenthesize or state precedence; do not rely on ambiguous natural-language “and/or/unless.”
- Treat $P\rightarrow Q$ as $\neg P\lor Q$, not as causality, chronology or its converse.
- Track free/bound variables and use capture-avoiding substitution/renaming.
- Negate quantifiers correctly: $\neg\forall x.P\equiv\exists x.\neg P$, $\neg\exists x.P\equiv\forall x.\neg P$.
- State preconditions without hiding desired conclusions; handle empty domains/collections and vacuity intentionally.
- Specifications include allowed failures, side effects, nondeterminism and termination when those are relevant.
- Testing/model enumeration provides counterexamples within a scope; proof soundly connects all modeled cases only under explicit assumptions.

### Common failures

Common failures include treating a predicate as true before assigning/binding variables; confusing implication with converse/causation; proving the consequent by assuming it as a precondition; using “or” without inclusive/exclusive intent; dropping parentheses; negating `forall` as `forall not`; quantifier-order reversal; variable capture; missing empty collection; using floating-point/int arithmetic as mathematical reals/integers; underspecifying errors/termination/side effects; checking a few cases and claiming validity; trusting an SMT `sat` result as program correctness; and formalizing the wrong requirement perfectly.

### Compact example

Requirement: “Every admitted job has a known owner.” With domain `Job`, predicates `Admitted(j)` and `KnownOwner(j)`, write $\forall j:Job.\ Admitted(j)\rightarrow KnownOwner(j)$. A job with neither property does not violate the implication; an admitted ownerless job is a counterexample. If the intended requirement also demands some admitted job exists, add $\exists j.Admitted(j)$.

### Connections

[PLS-001](../../01-programming-languages-and-semantics/modules/001-programs-languages-and-observable-behavior.md) supplies programs, semantics and observations. The successor [TPROG-002](../ROADMAP.md) introduces natural-deduction proof rules. [TPROG-005 through TPROG-010](../ROADMAP.md) develop correctness/specification obligations; [Theory of Computation](../../15-theory-of-computation-and-complexity/ROADMAP.md) owns decision problems and computability, while this program owns logic about programs.

## Governing Question

How do syntax, models, quantification and state relations make a software requirement falsifiable and suitable for proof without erasing the real system assumptions?

Formal reasoning begins before a theorem prover. It begins when “the request is safe,” “every task eventually finishes,” or “the result is sorted” becomes a formula with an explicit universe and observable meaning. Formal notation does not create rigor by typography; rigor comes from defined semantics, correct translation, justified inference and honest scope.

This module establishes classical propositional and first-order reasoning as a foundation. Later modules distinguish proof calculi, induction, partial/total correctness, Hoare logic, temporal logic and mechanization. Here the aim is to read/write specifications, find countermodels and identify what a formula does—and does not—say.

## Why This Matters

Natural language compresses context. “All users have an account” may mean all authenticated users, all stored user rows, all people in a jurisdiction, or every request principal. “If payment succeeds, ship” may state permission, obligation, causal workflow or a mere invariant. Different formalizations produce different systems.

Logic exposes gaps. An implication can be vacuously true because its antecedent never holds. A maximum specification can accept a value not in the list unless membership is stated. A quantifier order can change “one server handles all tenants” into “each tenant has some server.” A precondition can exclude every difficult input and make a contract useless.

Logic also separates evidence. One counterexample refutes validity/entailment. Exhaustive truth tables decide finite propositional formulas. Finite-state enumeration covers only the bounded model. A proof assistant checks a derivation relative to its logic, definitions, axioms and trusted kernel; it cannot establish that a requirements translation matches human intent without review.

## Prerequisites and Retrieval

Learners should retrieve:

- sets, elements, subsets, functions, relations and Cartesian products;
- Boolean values and basic truth tables;
- program state, inputs, outputs, exceptions/errors and termination;
- mathematical integers versus fixed-width machine integers;
- variables, binding and substitution at an introductory level;
- examples versus counterexamples;
- specification versus implementation and model versus reality.

Before continuing, formalize “a successful withdrawal never makes the balance negative” with initial balance, requested amount, result status and final balance. State the arithmetic domain and what happens on failure.

## Learning Objectives

After this module, learners can:

1. distinguish formula syntax, valuation/structure, model and truth;
2. calculate truth tables and classify satisfiable, valid and unsatisfiable formulas;
3. distinguish implication, biconditional, converse, inverse and contrapositive;
4. test semantic entailment and logical equivalence using countermodels;
5. define predicates/domains and track free/bound variables;
6. negate and reorder quantifiers correctly, explaining changed meaning;
7. translate bounded natural-language requirements into formulas and back;
8. write preconditions, postconditions and invariants as state relations;
9. expose vacuity, missing cases, arithmetic and failure assumptions;
10. distinguish finite checking, automated solver evidence and general proof.

## Core Exposition

### Build formulas from syntax, then interpret them

Fix atoms $p,q,r$. Propositional formulas are built recursively: each atom is a formula; if $\varphi,\psi$ are formulas, then so are $\neg\varphi$, $\varphi\land\psi$, $\varphi\lor\psi$, $\varphi\rightarrow\psi$, $\varphi\leftrightarrow\psi$. This grammar is syntax.

A valuation assigns each atom true/false. Semantics extends recursively:

- $\neg\varphi$ reverses truth;
- $\varphi\land\psi$ is true only when both are true;
- $\varphi\lor\psi$ is inclusive true when at least one is true;
- $\varphi\rightarrow\psi$ is false only when antecedent true/consequent false;
- $\varphi\leftrightarrow\psi$ is true when their values agree.

Thus the same syntax can model different domain claims depending on atom interpretation. Truth tables enumerate (2^n) valuations for (n) atoms and decide classical propositional validity, but grow exponentially.

### Separate satisfiability, validity and entailment

`p ∨ q` is satisfiable but not valid. `p ∨ ¬p` is valid in classical two-valued logic. `p ∧ ¬p` is unsatisfiable. These classify one formula.

Entailment relates assumptions to conclusion. $\{p\rightarrow q,p\}\models q$ because no valuation makes both premises true and conclusion false. To refute $\Gamma\models\varphi$, find a countermodel satisfying $\Gamma\land\neg\varphi$. If none exists, entailment holds under the semantics.

Logical equivalence $\varphi\equiv\psi$ means $\models\varphi\leftrightarrow\psi$. `p → q` is equivalent to `¬p ∨ q` and to contrapositive `¬q → ¬p`; it is not equivalent to converse `q → p`.

Provability $\Gamma\vdash\varphi$ is syntactic derivability in a proof system. Soundness connects proof to entailment; completeness connects entailment to proof for a logic. Do not swap $\models$ and $\vdash$ before specifying calculus/metatheorem.

### Read implication materially, not causally

Classical material implication is truth-functional. `RequestValid → Accepted` does not say validation causes acceptance, occurs earlier, or that every accepted request was valid. The latter direction is `Accepted → RequestValid`; equivalence needs both.

Vacuity is often correct: if no request is accepted, `Accepted → RequestValid` holds. But an availability requirement may also need `ValidRequest → eventually AcceptedOrRejected`, which needs temporal logic, not a static implication. Keep descriptive invariants, permissions, obligations and temporal/causal claims separate.

Translate “only if”: “A only if B” means $A\rightarrow B$. “A if B” means $B\rightarrow A$. “A iff B” means both. “Unless” is context-sensitive; rewrite in explicit cases instead of trusting prose precedence.

### Move from propositions to predicates

A predicate is not a proposition until its arguments are supplied/bound. With domain users, `Active(u)` is an open formula in free variable (u); `Active(alice)` is closed if `alice` denotes an element; `∀u.Active(u)` binds it.

A first-order signature supplies predicate/function/constant symbols. A structure $\mathcal M$ supplies domain and interpretations; assignment $\eta$ maps free variables. Equality may be logical identity or domain-defined equivalence depending on formalism; state it.

Quantifier order matters:

$$
\forall tenant.\exists server.\ Handles(server,tenant)
$$

allows a different server per tenant, while

$$
\exists server.\forall tenant.\ Handles(server,tenant)
$$

requires one server for all. The second entails the first for nonempty relevant domains; converse does not.

### Negate and substitute with scope discipline

To negate a requirement, move negation through quantifiers/connectives:

$$
\neg\forall x.P(x)\equiv\exists x.\neg P(x),\qquad
\neg\exists x.P(x)\equiv\forall x.\neg P(x).
$$

The counterexample to “every completed order has payment” is “some completed order lacks payment,” not “every completed order lacks payment.”

Substituting term (t) for free (x) in $\varphi$ must avoid capture. In $\forall y.R(x,y)$, substituting (y) for (x) naively yields $\forall y.R(y,y)$, changing the formerly free (y). Rename binder first: $\forall z.R(x,z)$, then substitute to get $\forall z.R(y,z)$.

### Specify states and transitions

Let (State) map variables/heap abstractions to values. A precondition (Pre(s)) says which initial states are covered. An operation relation (Exec(s,input,s',result)) captures possible outcomes. A postcondition (Post(s,input,s',result)) constrains them.

For successful withdrawal over mathematical integers:

$$
Pre(s,a)\equiv a>0,
$$

$$
Post(s,a,s',r)\equiv
(r=success\rightarrow balance(s)\ge a\land balance(s')=balance(s)-a)
\land
(r=failure\rightarrow balance(s')=balance(s)).
$$

If insufficient funds must fail, add `balance(s)<a → r=failure`; otherwise the contract permits failure even when funds exist and may permit success only through the first implication. If account identity, authorization, overdraft, fees, concurrency and machine overflow matter, add them/model them. Specification strength is inclusion/exclusion of behaviors.

### Write complete result specifications

For `max(xs)` over nonempty finite integer sequence, result (m) needs both:

$$
m\in xs\quad\land\quad\forall x\in xs.\ x\le m.
$$

Only upper-bound clause admits 1,000,000 for `[1,2]`; only membership admits 1. Empty sequence needs precondition `xs ≠ []` or explicit `None/error` result. Duplicate maxima do not alter value but matter if result includes index.

For sorting, state permutation/multiset preservation plus nondecreasing order. Sortedness alone permits returning empty list or zeros. Good specifications combine safety/functional relationship and frame/unchanged-state facts.

### Turn a contract into proof obligations

A contract is useful only after its quantifiers and execution meaning are exposed. For partial correctness, the central obligation is

$$
\forall s,i,s',r.\ Pre(s,i)\land Exec(s,i,s',r)\Rightarrow Post(s,i,s',r).
$$

This statement ranges over every terminating outcome admitted by `Exec`; it does not assert that an outcome exists. Total correctness adds termination for every covered initial state, usually through a well-founded variant, a liveness argument, or a termination-aware operational semantics. Conflating the two turns a diverging program into a vacuous “correct” implementation.

For a loop, select invariant (Inv) and decompose the argument. Initialization shows the precondition establishes (Inv). Preservation shows one enabled iteration maps an invariant state to another invariant state. Exit shows (Inv) together with the negated guard entails the desired postcondition. A termination argument separately shows that iterations cannot continue forever. For concurrent or reactive systems, a single loop variant is often inappropriate; rely/guarantee conditions, fairness assumptions, temporal properties, linearizability points, or refinement relations may be required.

The most revealing audit is to negate each obligation and search for a model. Initialization failure produces a legal input where the invariant never starts. Preservation failure produces one invariant state and transition that breaks it. Exit failure produces a reachable-looking terminal state that violates the result. These countermodels diagnose different defects and should not be merged into one generic “verification failed.” Reachability matters: an arbitrary countermodel can be impossible under initialization and transition history, so either prove reachability, add an inductive invariant that excludes it, or label the check as a local obligation.

Finally, distinguish implementation correctness from refinement. If an abstract specification admits behavior relation (A) and a concrete program admits (C), a refinement claim normally requires every observable concrete behavior to be represented by an allowed abstract behavior, under an abstraction relation and stated environment assumptions. Matching a few input/output examples is neither trace inclusion nor contextual equivalence. The abstraction function, observation boundary, divergence policy, nondeterminism, failures, and interference determine what the refinement theorem actually says.

### Detect underspecification and overspecification

**Underspecification** permits unwanted implementations: stack `pop` may return any element if LIFO relation omitted. **Overspecification** forbids acceptable implementations: requiring quicksort's exact intermediate swaps when only sorted permutation matters.

Ask for weakest useful precondition and strongest intended postcondition—without demanding implementation details. Specifications can intentionally allow nondeterminism, e.g., any shortest path, but must constrain all permitted results. Frame conditions state what cannot change.

Vacuity check: Is precondition satisfiable? Does antecedent ever occur? Is domain empty? Standard first-order semantics often assumes nonempty domain, while program collections may be empty. `∀x∈∅.P(x)` is true, `∃x∈∅.P(x)` false. Add existence/coverage when intended.

### Distinguish mathematical and machine models

Mathematical integers are unbounded; machine signed addition can overflow, wrap, trap or be undefined depending on language/configuration. Floating point has rounding, NaN and signed zero; real-number algebra may fail. Maps may be partial; division by zero/error needs modeling. Time can be wall/monotonic/logical, with precision and discontinuity.

Every formal tool has a logic/theory. SMT solvers reason over selected theories (bit-vectors, integers, arrays, floating point) with declared semantics; choose one matching implementation. An uninterpreted function has only congruence unless axiomatized; the solver does not know your domain name.

### Use checking and proof honestly

A truth table exhausts all valuations for a finite propositional formula. Finite model enumeration exhausts only chosen domain/state bounds. Property tests sample/generate implementation executions. SAT/SMT `sat` provides a model for encoded constraints; `unsat` shows none in encoded theory/assumptions if solver is sound/correctly used; `unknown` is not proof either way. Proof assistant checks a proof term relative to definitions/axioms/kernel.

In every case validate encoding and requirement. Preserve counterexamples with variable assignments/traces. Record tool/version/options/theory/bounds/timeouts and trusted base. Formal proof can establish the wrong formula; human/domain review connects formula to intended world.

### Exhaustive propositional evaluation

The executable model enumerates every Boolean valuation for two atoms and checks the equivalence $p\rightarrow q\equiv\neg p\lor q$.

<!-- bijux-verify: {"id":"tprog-001-material-implication","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"p q p->q !p|q\nF F T T\nF T T T\nT F F F\nT T T T\nequivalent=yes\ncountermodels=0\n","stderr":""}} -->
```python
def truth(value):
    return "T" if value else "F"

rows = []
countermodels = []
for p in (False, True):
    for q in (False, True):
        implication = not (p and not q)
        disjunction = (not p) or q
        rows.append((p, q, implication, disjunction))
        if implication != disjunction:
            countermodels.append((p, q))

print("p q p->q !p|q")
for row in rows:
    print(" ".join(truth(value) for value in row))
print("equivalent=" + ("yes" if not countermodels else "no"))
print("countermodels=" + str(len(countermodels)))
```

The run exhausts two-valued valuations for exactly this encoded formula and confirms no countermodel. It does not prove the Python encoding matches arbitrary source requirements, first-order quantifiers, nonclassical/three-valued logic, temporal behavior, program execution or solver correctness.

## Definitions and Notation

Let propositional atoms be (AP), formulas (Form(AP)), valuations $v:AP\to\mathbb B$, with $\mathbb B=\{\mathsf F,\mathsf T\}$. Satisfaction $v\models\varphi$ means formula evaluates true under (v). Validity $\models\varphi$; satisfiability $\exists v.v\models\varphi$; entailment $\Gamma\models\varphi$.

First-order signature $\Sigma=(Func,Pred,Const)$. Structure $\mathcal M=(D,I)$ interprets symbols over domain (D); assignment $\eta:Var\to D$. `FV(φ)` denotes free variables. A sentence has no free variables. Substitution $\varphi[t/x]$ replaces free (x) capture-avoidably where term is free-for (x).

For programs, initial state $s\in S$, input $i\in I$, final state $s'\in S$, result $r\in R$, and transition/execution relation $Exec\subseteq S\times I\times S\times R$. A contract is

$$
\forall s,i,s',r.\ Pre(s,i)\land Exec(s,i,s',r)\rightarrow Post(s,i,s',r).
$$

This resembles partial correctness because it constrains terminating outcomes represented by `Exec`; termination/liveness needs an additional obligation/model. Nondeterministic `Exec` requires every permitted outcome satisfy postcondition for demonic correctness interpretations.

## Mechanisms, Invariants, or Proof Structure

1. **Choose logic/semantics.** Classical/intuitionistic/temporal, domains/sorts, equality, arithmetic, state/termination/error model.
2. **Define vocabulary.** Each atom/predicate/function/constant and authoritative interpretation.
3. **Write syntax unambiguously.** Parentheses, types, variable scopes and quantifier domains.
4. **Check well-formedness.** Free variables, sorts, total/partial functions and capture-avoiding substitution.
5. **Test satisfiability/nonvacuity.** Premises/preconditions/domain and meaningful witness/counterexample existence.
6. **Strengthen complete behavior.** Success/failure, result relationship, frame conditions, nondeterminism and empty/boundary cases.
7. **Seek countermodels.** Premises true/conclusion false; property violated; quantify minimal causal state.
8. **Derive proof obligations.** Entailment/equivalence/invariant preservation/termination as separate claims.
9. **Match evidence.** Truth table, proof, solver/model checker, tests and human validation each to bounded claims.
10. **Record assumptions/trust.** Encoding, axioms, tool/kernel/version/bounds, arithmetic and residual risk.

Truth-table equivalence proof is exhaustive because a two-atom classical formula has exactly four valuations. Each row gives identical truth. This proof depends on Boolean domain and correct connective definitions. It cannot establish a domain requirement translation or an implementation's behavior.

## Alternatives and Trade-Offs

**Natural-language requirement** is accessible/context-rich but ambiguous. Keep it beside formalization and examples/counterexamples.

**Executable assertions/contracts** check observed executions and integrate with code; they may be disabled, incomplete, side-effecting or too late and do not quantify unexecuted states.

**Types/refinement types** make some predicates compositional/checkable at boundaries; expressiveness/decidability/annotation trade-offs apply.

**Property-based testing** searches many generated cases and shrinks counterexamples; passing remains sampling/bounded evidence.

**SAT/SMT solving** automates satisfiability/validity modulo theories; encoding/theory/solver result/trust must match claim.

**Model checking** exhaustively explores a finite/abstract transition model and produces traces; state explosion and abstraction limit scope.

**Interactive theorem proving** supports rich definitions/proofs with kernel checking; proof engineering and requirement validation remain human work.

**Runtime monitoring/temporal assertions** observe live traces and can enforce/detect; they cannot see counterfactual executions and may add overhead.

**Design by construction** represents invalid states as unconstructible where feasible; external/stateful/concurrent obligations still require specifications.

Combine rather than rank universally: prose for stakeholder intent, formal formula for precision, proof/checker for model, tests/monitoring for implementation/world correspondence.

## Failure Modes and Misconceptions

- **“A formula is true by itself.”** Truth is under interpretation; validity quantifies interpretations.
- **“Predicate equals proposition.”** Open predicates require arguments/assignments or binding.
- **“Implication is causality/time.”** Material implication is truth-functional.
- **“Converse is equivalent.”** $P\to Q$ does not imply $Q\to P$.
- **“False antecedent is a bug in logic.”** Vacuous truth is coherent; requirement may need existence/progress.
- **“Or means exclusive.”** Classical $\lor$ is inclusive; XOR must be stated.
- **“Negate words locally.”** Quantifiers/connectives transform under negation.
- **“Quantifier order does not matter.”** `∀∃` and `∃∀` usually express different dependency.
- **“Substitution is textual replacement.”** It must avoid variable capture.
- **“Precondition can exclude failures.”** It can, but then the contract intentionally covers less and may be useless.
- **“Postcondition gives algorithm.”** It specifies acceptable relation, often leaving implementation choices.
- **“Sorted output specifies sort.”** Also require permutation/multiset preservation.
- **“Integers/reals match machine arithmetic.”** Select bit-vector/overflow/floating semantics.
- **“No bounded counterexample proves theorem.”** It proves only explored bound/model.
- **“Mechanized means correct requirement.”** Formalization, axioms and model-world connection require review.

## Worked Examples

### Example 1

**Situation.** Classify $p\lor\neg p$, $p\land\neg p$, and $p\rightarrow q$.

**Reasoning.** First is true for p false/true: valid. Second false for both: unsatisfiable. Third true in three of four valuations: satisfiable but not valid; countermodel p=true,q=false.

**Conclusion.** Validity, unsatisfiability and mere satisfiability are different classifications.

### Example 2

**Situation.** Requirement says “a request is accepted only if authenticated.”

**Reasoning.** “A only if B” gives `Accepted → Authenticated`. `Authenticated → Accepted` is converse and would require accepting every authenticated request despite authorization/rate/business failures.

**Conclusion.** Direction of implication encodes necessary versus sufficient condition.

### Example 3

**Situation.** Does $p\lor q,\neg p\models q$?

**Reasoning.** A countermodel would require premises true and q false. Then `p∨q` forces p true, conflicting with `¬p`. No countermodel exists over four valuations.

**Conclusion.** The premises semantically entail q (disjunctive syllogism under classical semantics).

### Example 4

**Situation.** Formula `balance > 0` appears in a specification.

**Reasoning.** As written it is open unless balance denotes a state component/current constant. Define `Balance(account,state)` and bind account/state or declare context. Different states can yield different truth.

**Conclusion.** Predicate variables and interpretation must be explicit before truth/proof.

### Example 5

**Situation.** Negate “every completed job has an artifact.”

**Reasoning.** Original $\forall j.Completed(j)\to HasArtifact(j)$. Negation becomes $\exists j.Completed(j)\land\neg HasArtifact(j)$. It asks for one causal counterexample, not all jobs lacking artifacts.

**Conclusion.** Quantifier/connective negation constructs useful counterexample queries.

### Example 6

**Situation.** `∀x∈items. Valid(x)` passes when `items=[]`.

**Reasoning.** Universal restriction is vacuously true: no counterexample element. If requirement demands at least one item, conjoin `items ≠ []`; if empty is legitimate, passing is correct.

**Conclusion.** Nonvacuity is a domain requirement, not a change to logic.

### Example 7

**Situation.** Specify maximum of nonempty sequence.

**Reasoning.** `∀x∈xs.x≤m` only makes m an upper bound; require `m∈xs`. With `[1,2]`, 3 refutes incomplete spec because upper-bound true/membership false.

**Conclusion.** Complete result specs combine extremal property and provenance from input.

### Example 8

**Situation.** Withdrawal contract only states `success → final=initial-amount`.

**Reasoning.** It permits success with insufficient funds and arbitrary failed-state mutation. Add positive amount, funds/authorization condition, nonnegative invariant, failure unchanged/frame, integer/overflow and result-totality rules.

**Conclusion.** Implication-centered postconditions must cover guards, failure and frame conditions.

### Example 9

**Situation.** A checker verifies mutual exclusion for two processes and counter up to 3.

**Reasoning.** Exhaustive success proves the encoded bounded state model. It does not prove arbitrary process count/counter, implementation memory model or omitted transitions. Preserve bound and abstraction assumptions.

**Conclusion.** Exhaustiveness is always relative to the enumerated/model semantics.

### Example 10

**Situation.** A medical dose rule says “all eligible patients receive dose ≤ maximum.”

**Reasoning.** Define eligible population, units, weight/time/renal inputs, missing/stale data, inequality/rounding, contraindications and no-dose/error behavior. Check satisfiability/nonvacuity and counterexamples. Named clinicians/pharmacists, clinical-safety, privacy/security and regulatory reviewers validate meaning; theorem proving cannot establish clinical adequacy.

**Conclusion.** High-stakes formalization needs qualified human validation of vocabulary/model as well as mathematical checking.

## Cross-Program Connections

- **Programming Languages and Semantics:** interpretation and observations make formula/program claims meaningful.
- **Theory of Computation:** satisfiability/validity checking become decision problems with complexity/decidability boundaries.
- **Algorithms:** invariants, pre/postconditions and counterexamples support correctness reasoning.
- **Data Structures:** representation invariants specify valid concrete states for abstract values.
- **Concurrency/Distributed Systems:** static predicates are insufficient for order, temporal, safety/liveness and fairness claims.
- **Testing and Quality:** formal properties guide generated tests; tests find counterexamples without proving unbounded validity.
- **Security Engineering:** authorization/trust policies require exact quantifiers, negation, freshness and fail-closed cases.
- **Systems Engineering:** assumptions, environment/domain boundaries and stakeholder intent determine model validity.

## References

- Open Logic Project, [Open Logic Text](https://builds.openlogicproject.org/open-logic-complete.pdf), current build retrieved 2026-08-29. Open treatment of propositional/first-order syntax, semantics, proof and metatheory.
- Michael Huth and Mark Ryan, *Logic in Computer Science*, second edition, Cambridge University Press, 2004. Logic, program verification, temporal logic and model checking foundations.
- Herbert Enderton, *A Mathematical Introduction to Logic*, second edition, Academic Press, 2001. Rigorous first-order syntax, structures, satisfaction and proof foundations.
- C. A. R. Hoare, [An Axiomatic Basis for Computer Programming](https://doi.org/10.1145/363235.363259), *Communications of the ACM* 1969. Foundational precondition/postcondition reasoning about programs.
- Edsger W. Dijkstra, [Guarded Commands, Nondeterminacy and Formal Derivation of Programs](https://www.cs.utexas.edu/~EWD/transcriptions/EWD04xx/EWD472.html), EWD472, 1975, retrieved 2026-08-29. Predicate-transformer and program-derivation foundations.
- Leslie Lamport, [Specifying Systems](https://lamport.azurewebsites.net/tla/book.html), Addison-Wesley, 2002, retrieved 2026-08-29. State/behavior specification and temporal reasoning foundations.
- Lean Project, [Propositions and Proofs](https://lean-lang.org/theorem_proving_in_lean4/Propositions-and-Proofs/) and [Quantifiers and Equality](https://lean-lang.org/theorem_proving_in_lean4/Quantifiers-and-Equality/), *Theorem Proving in Lean 4*, retrieved 2026-08-29. Current mechanized formulations of propositions, connectives, quantifiers and equality.
- SMT-LIB Initiative, [The SMT-LIB Standard and Logics](https://smt-lib.org/language.shtml), retrieved 2026-08-29. Current authoritative language/theory reference for SMT encodings; solver results remain relative to selected logic.
- David Gries, *The Science of Programming*, Springer, 1981. Predicate logic and derivation of program correctness.
- Daniel Jackson, *Software Abstractions*, revised edition, MIT Press, 2012. Relational modeling, bounded analysis and counterexample-oriented specification.

## Exercises

### Exercise 1

For formulas $p\to q$, $q\to p$, $\neg q\to\neg p$, classify equivalences and give a countermodel for the non-equivalence.

### Exercise 2

Formalize and negate: “Every active tenant has some healthy server.” Compare with “Some healthy server serves every active tenant.”

### Exercise 3

Diagnose this stack `pop` contract: pre `true`; post `result ∈ old(stack)`. Repair empty input, LIFO result, final state, errors and unchanged external state.

### Exercise 4

Compare truth-table enumeration, property testing, SMT solving, finite model checking and interactive proof for verifying a bounded access-control rule and its implementation.

### Exercise 5

Write a preliminary formal specification/evidence plan for an unfamiliar autonomous train-door controller. Include state, environment, safety, progress, failures, arithmetic/time, assumptions and human review.

## Answers to the Exercises

### Answer 1

$p\to q\equiv\neg q\to\neg p$ (contrapositive). The converse $q\to p$ is not equivalent. Countermodel p=false,q=true: original `false→true` is true, converse `true→false` false. Conversely p=true,q=false makes original false and converse true. Do not confuse inverse `¬p→¬q`, which is equivalent to converse, with contrapositive. A four-row truth table proves these equivalences under classical two-valued semantics.

### Answer 2

Let predicates `Active(t)`, `Healthy(s)`, `Serves(s,t)` over Tenant/Server. First:

$$
\forall t:Tenant. Active(t)\rightarrow\exists s:Server. Healthy(s)\land Serves(s,t).
$$

Negation:

$$
\exists t. Active(t)\land\forall s.\neg(Healthy(s)\land Serves(s,t)).
$$

Second:

$$
\exists s.Healthy(s)\land\forall t.(Active(t)\rightarrow Serves(s,t)).
$$

It requires one healthy server for all active tenants, stronger than possibly different witnesses. If no active tenants, first is vacuously true; second still requires a healthy server due to its existential. Decide whether existence/load/capacity is intended.

### Answer 3

Original permits any historical element, leaves final stack unconstrained and cannot define membership for empty safely. Use result sum `Popped(value)|Empty`. For old stack sequence (xs): if (xs=[]), result `Empty` and new stack `[]`; if (xs=ys·[x]), result `Popped(x)` and new stack `ys`. State that only target stack changes (frame), and define atomicity/concurrency separately. If empty pop is excluded, precondition `xs≠[]` plus post top/removal is alternative, but caller obligations differ. Specify element equality and finite sequence; exceptions/resource failure policy may add outcomes without allowing partial mutation.

### Answer 4

Truth tables decide finite propositional abstraction and expose countervaluations but not quantified/stateful implementation. Property testing runs real implementation across generated principals/resources/actions and shrinks counterexamples, but samples. SMT encodes quantified/finite or theory-rich policy constraints and can find a model or prove unsatisfiability of violation formula relative to theory/encoding. Finite model checker exhausts bounded state/transition histories and returns traces, with state/bound limits. Interactive proof can establish a general theorem for formal policy/transition definitions relative to axioms/kernel, at proof-engineering cost. Combine: human-reviewed formal vocabulary; SMT/model counterexamples; proof for core invariant if risk justifies; property/integration tests for implementation correspondence; runtime audit for deployed identities/freshness. Record bounds/tool versions/unknowns.

### Answer 5

Model states `ClosedLocked`, `Opening`, `Open`, `Closing`, `Obstructed`, `Fault`, train motion/speed, platform alignment, command source, sensors, actuator and monotonic time. Environment includes passenger obstruction, sensor disagreement, power/network loss and manual emergency authority. Safety examples: moving above threshold implies doors closed/locked; unlock/open only when train stopped and aligned; closing with valid obstruction transitions to safe reopen/stop; conflicting/unknown sensors fail safe. Progress: under stable power, no obstruction and valid close command, door eventually closes/locks within deadline—requiring fairness/actuator assumptions. Specify permitted fault/manual states, debounce/time bounds, units/precision/clock discontinuity and no unsafe output on controller restart.

Use transition-system/temporal rather than static predicates alone. Check state-machine well-formedness, model-check bounded concurrency/fault traces, prove key invariant over transitions, run hardware-in-loop sensor/actuator faults and timing/resource tests, verify implementation/model trace refinement and independent hazard analysis. Counterexamples include stale speed zero, alignment loss during opening, obstruction during closing, restart with uncertain position and simultaneous commands. Named human railway safety, control, mechanical, human-factors/accessibility, cybersecurity, regulatory and operations reviewers validate hazards/assumptions/manual procedures; automated formal success cannot approve real-world safety alone.
