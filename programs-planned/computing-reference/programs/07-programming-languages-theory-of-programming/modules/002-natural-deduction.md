---
module_id: TPROG-002
program: Programming Languages: Theory of Programming
level: 1
module_number: 2
title: Natural Deduction
status: complete
last_verified: 2026-08-29
---

# Natural Deduction

## One-Page Review

### Governing question

How can a small set of local introduction and elimination rules construct auditable proofs from explicit assumptions, and what prevents an apparent proof from using an assumption outside its scope?

### Essential definitions

- A **judgment** \(\Gamma\vdash A\) says proposition \(A\) is derivable from context \(\Gamma\).
- A **context** is the collection of currently available assumptions, normally tracked with labels or proof variables.
- An **introduction rule** explains how to construct evidence for a connective.
- An **elimination rule** explains how evidence for a connective may be used.
- A **derivation** is a finite tree whose leaves are assumptions and whose internal nodes are justified rule instances.
- **discharge** closes specified occurrences of a temporary assumption when a rule such as implication introduction completes a subderivation.
- An **open assumption** is still available at the conclusion; a **closed derivation** has none.
- **normalization** removes introduction-followed-immediately-by-elimination detours.
- **constructive logic** requires construction-relevant evidence; **classical logic** adds principles such as excluded middle or double-negation elimination.
- Under **Curry–Howard**, propositions correspond to types, proofs to terms, implication introduction to lambda abstraction, and implication elimination to function application.

### Central model, mechanism, or theorem

Natural deduction proves judgments by syntax-directed rules. For implication:

\[
\frac{\Gamma,A\vdash B}{\Gamma\vdash A\to B}\to I
\qquad
\frac{\Gamma\vdash A\to B\quad\Gamma\vdash A}{\Gamma\vdash B}\to E.
\]

The first rule discharges the indicated assumption \(A\). The second is modus ponens. A proof checker recursively verifies each node's premises, conclusion, context, and side conditions. Soundness is a metatheorem relating derivability to semantics; it is not established merely because a tree is well-shaped.

### Critical invariants

- Every leaf cites an assumption currently in scope.
- Every node exactly matches one rule schema after substitution.
- Discharge removes only the labeled assumptions owned by that subproof.
- Branches of disjunction elimination derive the same conclusion.
- Explosion uses an actual derivation of falsity, not mere disagreement.
- Quantifier rules obey freshness and substitution side conditions.
- Classical principles are explicit additions, never smuggled into constructive derivations.
- A theorem prover's acceptance is evidence relative to its kernel, definitions, and axioms.

### Common failures

Frequent errors are affirming the consequent, assuming the desired conclusion without discharge, reusing a branch-local hypothesis outside its branch, proving only one disjunction-elimination case, confusing \(A\to B\) with \(B\to A\), treating \(\neg A\) as an atom unrelated to \(A\to\bot\), choosing a non-fresh witness for universal introduction, invoking excluded middle silently, and mistaking a failed proof search for underivability.

### Compact example

To derive \((A\land B)\to A\), assume \(h:A\land B\). Conjunction elimination yields \(A\). Implication introduction then discharges \(h\), leaving a closed derivation. Under Curry–Howard the proof term is \(\lambda h.\mathrm{fst}(h)\).

### Connections

Retrieve [TPROG-001's propositions, predicates, and specifications](001-propositions-predicates-and-formal-specifications.md). [TPROG-003](../ROADMAP.md) develops induction. Natural deduction connects to [Programming Languages & Semantics](../../01-programming-languages-and-semantics/ROADMAP.md), [Theory of Computation & Complexity](../../15-theory-of-computation-and-complexity/ROADMAP.md), and proof-oriented software verification.

## Governing Question

What makes a line of logical reasoning a valid derivation rather than persuasive prose?

Natural deduction answers with local rules for building and consuming evidence. Instead of starting from a large catalog of axioms, it explains each connective by paired introduction and elimination rules. A proof becomes a tree of small checkable steps under scoped assumptions. This resembles structured programming: local interfaces compose, blocks delimit temporary resources, and a checker rejects an out-of-scope reference.

## Why This Matters

Program specifications are propositions about inputs, states, traces, and results. Verification requires more than writing those propositions: engineers must construct or check derivations while tracking assumptions. Implication introduction models conditional reasoning. Conjunction packages evidence for simultaneous invariants. Disjunction demands case analysis. Existential evidence carries a witness. Universal reasoning requires independence from an arbitrary choice.

Natural deduction also exposes the computational content of proofs. Under Curry–Howard, a proof of \(A\to B\) is a construction that transforms evidence of \(A\) into evidence of \(B\). Normalization corresponds to computation. This connection underlies typed functional languages and interactive theorem provers, while semantic soundness explains why syntactic proof checking can support claims about models.

## Prerequisites and Retrieval

You should understand propositional formulas, predicates, free and bound variables, functions, trees, lexical scope, and the specification distinction from [TPROG-001](001-propositions-predicates-and-formal-specifications.md). Retrieve:

1. A proposition is not the same object as evidence for it.
2. A variable occurrence is meaningful relative to a binding scope.
3. A rule schema stands for all capture-avoiding substitutions of its metavariables.
4. Validity in every model and derivability in a proof calculus require a metatheoretic connection.
5. A countermodel refutes semantic validity, whereas unfinished proof search proves little by itself.

## Learning Objectives

After completing this module, you should be able to:

- read and construct proof trees for \(\land,\lor,\to,\bot,\neg\);
- track contexts, assumption labels, subproofs, and discharge;
- distinguish introduction from elimination reasoning;
- translate simple derivations into proof terms;
- identify invalid scope, branch, and rule applications;
- normalize simple introduction–elimination detours;
- separate constructive rules from classical extensions;
- state freshness obligations for basic quantifier rules;
- implement a small trusted checker for a restricted calculus;
- explain the limits of syntactic acceptance and automated search.

## Core Exposition

Write \(\Gamma\vdash A\) when \(A\) has a derivation whose undischarged assumptions occur in \(\Gamma\). Contexts may be sets, multisets, sequences, or mappings from proof variables to propositions; the choice determines structural details. This module uses named assumptions and permits weakening, exchange, and contraction: unused assumptions may remain, order is irrelevant, and one assumption may be used repeatedly.

Those permissions are called **structural rules**. Weakening moves from \(\Gamma\vdash A\) to \(\Gamma,B\vdash A\); exchange reorders assumptions; contraction combines duplicate usable assumptions. Ordinary intuitionistic and classical natural deduction usually admit them, but substructural logics restrict one or more to model consumable, ordered, or unique resources. Thus the context representation is not bookkeeping trivia. It encodes which assumption uses the logic regards as legitimate.

The assumption rule is

\[
\frac{}{\,\Gamma,A\vdash A\,}hyp.
\]

It is not a global axiom asserting every \(A\). It says an assumption is usable inside its scope.

For conjunction:

\[
\frac{\Gamma\vdash A\quad\Gamma\vdash B}{\Gamma\vdash A\land B}\land I,
\quad
\frac{\Gamma\vdash A\land B}{\Gamma\vdash A}\land E_1,
\quad
\frac{\Gamma\vdash A\land B}{\Gamma\vdash B}\land E_2.
\]

Introduction packages two proofs; elimination projects either component. The proof terms are pairing and projections.

For implication, introduction opens a subderivation with a fresh assumption label \(x:A\), derives \(B\), then discharges occurrences owned by that label:

\[
\frac{\Gamma,x:A\vdash B}{\Gamma\vdash A\to B}\to I_x.
\]

Elimination applies a proof of \(A\to B\) to a proof of \(A\). Under Curry–Howard, the rules are lambda abstraction and application. Discharge is lexical: another assumption with the same formula but a different label is not silently removed.

For disjunction:

\[
\frac{\Gamma\vdash A}{\Gamma\vdash A\lor B}\lor I_1,
\qquad
\frac{\Gamma\vdash B}{\Gamma\vdash A\lor B}\lor I_2.
\]

Using a disjunction requires both cases:

\[
\frac{\Gamma\vdash A\lor B\quad
\Gamma,x:A\vdash C\quad
\Gamma,y:B\vdash C}
{\Gamma\vdash C}\lor E_{x,y}.
\]

Both branch assumptions are discharged, and both branches must reach the same \(C\). Knowing “one of these” never licenses choosing the convenient side.

Falsity \(\bot\) has no introduction rule in a consistent core. Its elimination rule

\[
\frac{\Gamma\vdash\bot}{\Gamma\vdash C}\bot E
\]

expresses explosion. Define \(\neg A\) as \(A\to\bot\). To prove \(\neg A\), assume \(A\) and derive falsity. From \(A\) and \(\neg A\), implication elimination derives \(\bot\).

These rules are constructive. Classical natural deduction explicitly adds, for example, \(A\lor\neg A\), double-negation elimination \(\neg\neg A\to A\), or a reductio rule with appropriate discharge. Classical reasoning is legitimate when the intended logic includes it; hidden use makes the proof's foundations unclear and can erase computational content.

Introduction rules specify canonical evidence. Elimination rules should not extract more than that evidence contains. Their harmony supports normalization. An implication introduced as \(\lambda x.t\) and immediately eliminated with argument \(u\) reduces to \(t[u/x]\). A conjunction formed as \(\langle s,t\rangle\) and immediately projected reduces to \(s\) or \(t\). These are proof detours: the introduced connective did no lasting logical work.

Normalization is not cosmetic. It can yield consistency results—no closed normal proof of \(\bot\) exists when no rule can end in it—and connects proof reduction to program evaluation. The full theorem requires induction over derivations and careful commuting conversions, beyond the examples here.

Quantifiers extend the same pattern. Universal elimination instantiates \(\forall x.A(x)\) with an admissible term \(t\). Universal introduction proves \(A(a)\) for a fresh arbitrary parameter \(a\) not free in undischarged assumptions on which the derivation depends, then concludes \(\forall x.A(x)\). Existential introduction provides witness \(t\) and proof of \(A(t)\). Existential elimination opens a branch with fresh witness parameter \(a\) and evidence \(A(a)\), derives a conclusion independent of \(a\), then discharges the branch. Freshness prevents proving a universal statement from a special case or leaking a hidden witness.

More formally, universal introduction has the shape

\[
\frac{\Gamma\vdash A(a)}{\Gamma\vdash\forall x.A(x)}\forall I,
\]

with \(a\notin\mathsf{fv}(\Gamma)\). Existential elimination has the shape

\[
\frac{\Gamma\vdash\exists x.A(x)\qquad
\Gamma,a,A(a)\vdash C}
{\Gamma\vdash C}\exists E,
\]

where \(a\) is fresh for \(\Gamma,C\) and the existential premise. The second condition prevents the conclusion from mentioning a private witness whose identity the existential never promised. Implementations often represent binders using locally nameless terms, de Bruijn indices, or globally fresh identifiers to make capture avoidance checkable.

Proof presentation varies. Tree notation makes dependencies explicit but grows wide. Fitch notation uses indented subproofs. Sequent-style terms expose contexts. Proof terms are compact and machine-checkable. Tactics construct proof terms through state transformations; the kernel, not the tactic, should validate the result in a small trusted base.

Backward proof construction starts at a goal and chooses a rule whose conclusion matches it. If the goal is \(A\land B\), \(\land I\) yields subgoals \(A\) and \(B\). If the goal is \(A\to B\), \(\to I\) adds a labeled \(A\) and leaves goal \(B\). Introduction rules are often invertible or goal-directed in this practical sense. Elimination rules require choosing useful assumptions or intermediate formulas and can expand search dramatically. Tactics manage metavariables, unification, backtracking, rewriting, and libraries, but a finished proof must contain enough information for deterministic rechecking.

Checking is not wholly context-free: definitions may unfold, implicit arguments may elaborate, type-class or coercion mechanisms may have run, and imported theorems may depend on axioms. A trustworthy record identifies the exact theorem statement after elaboration, imported environment, axiom set, kernel version, and proof-object digest. “The file compiled” is weaker than knowing which proposition and assumptions the kernel accepted.

Soundness states that if \(\Gamma\vdash A\), then every model satisfying \(\Gamma\) satisfies \(A\). Its proof proceeds by induction on the derivation, with one case per rule. Completeness states a converse for a chosen logic and semantics. Decidability of proof checking does not imply easy or even decidable proof discovery in richer logics. Keep checking, search, truth, and usability distinct.

For implication introduction, the soundness induction step is illustrative. Assume every model satisfying \(\Gamma,A\) satisfies \(B\). Take an arbitrary model satisfying \(\Gamma\). Under the semantics of implication, if that model satisfies \(A\), it satisfies the extended premises and hence \(B\); therefore it satisfies \(A\to B\). The argument depends on the intended semantics and the premise induction hypothesis. Merely drawing the rule cannot substitute for this metatheorem.

Natural deduction derivations can also expose dependency minimization. If a closed theorem was developed in context \(\Gamma\) but the proof term mentions only assumptions \(\Delta\subseteq\Gamma\), then weakening explains why the larger context was accepted while the proof term records the smaller operational dependency. Audits should distinguish assumptions merely available from axioms actually used, especially when classical choice, extensionality, or domain axioms change the strength or computational interpretation of a result.

The following checker handles only atoms, conjunction, and implication with named hypotheses. Each constructor recursively checks its premises. This executable evidence covers the shown finite calculus fragment; it does not establish soundness, completeness, normalization, quantifiers, disjunction, or the security of production proof assistants.

<!-- bijux-verify: {"id":"natural-deduction-fragment","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"projection: ((A & B) -> A)\ncomposition: ((A -> B) -> ((B -> C) -> (A -> C)))\ninvalid: unbound hypothesis x\n","stderr":""}} -->
```python
def check(term, context):
    tag = term[0]
    if tag == "hyp":
        name = term[1]
        if name not in context:
            raise ValueError(f"unbound hypothesis {name}")
        return context[name]
    if tag == "pair":
        return ("and", check(term[1], context), check(term[2], context))
    if tag == "left":
        proposition = check(term[1], context)
        if proposition[0] != "and":
            raise ValueError("left projection requires conjunction")
        return proposition[1]
    if tag == "lam":
        _, name, domain, body = term
        extended = dict(context)
        extended[name] = domain
        return ("implies", domain, check(body, extended))
    if tag == "app":
        function = check(term[1], context)
        argument = check(term[2], context)
        if function[0] != "implies" or function[1] != argument:
            raise ValueError("implication elimination mismatch")
        return function[2]
    raise ValueError(f"unknown rule {tag}")

def show(p):
    if isinstance(p, str):
        return p
    symbol = "&" if p[0] == "and" else "->"
    return f"({show(p[1])} {symbol} {show(p[2])})"

A, B, C = "A", "B", "C"
projection = ("lam", "p", ("and", A, B), ("left", ("hyp", "p")))
composition = (
    "lam", "f", ("implies", A, B),
    ("lam", "g", ("implies", B, C),
     ("lam", "x", A,
      ("app", ("hyp", "g"),
       ("app", ("hyp", "f"), ("hyp", "x"))))))
print("projection:", show(check(projection, {})))
print("composition:", show(check(composition, {})))
try:
    check(("hyp", "x"), {})
except ValueError as error:
    print("invalid:", error)
```

## Definitions and Notation

Propositions are \(A,B,C\). A context \(\Gamma=x_1:A_1,\ldots,x_n:A_n\) maps proof variables to assumptions. A derivation \(\mathcal D::\Gamma\vdash A\) is a tree concluding that judgment. Square brackets \([x:A]\) mark a temporary labeled assumption; a rule annotation such as \(\to I_x\) discharges it.

A substitution \(t[u/x]\) replaces free occurrences of proof variable \(x\) in \(t\) with \(u\), avoiding variable capture. Let \(\mathsf{fv}(A)\) be free variables of formula \(A\). Eigenvariable conditions constrain a parameter \(a\) not to occur freely in specified contexts or conclusions.

Semantic entailment \(\Gamma\models A\) is distinct from syntactic derivability \(\Gamma\vdash A\). Soundness is \(\Gamma\vdash A\Rightarrow\Gamma\models A\); completeness is the converse for a fixed calculus and semantics.

## Mechanisms, Invariants, or Proof Structure

**Local checking.** A rule instance is valid if its conclusion and premises unify with the rule schema and side conditions hold. Recursive checking terminates for a finite proof tree.

**Discharge invariant.** A rule may close only the assumption labels introduced for its subderivation. Formula equality alone does not determine ownership.

**Branch invariant.** In \(\lor E\), both hypothetical branches derive syntactically the same conclusion under their local assumptions; neither branch hypothesis escapes.

**Normalization step.** \((\lambda x.t)\,u\to t[u/x]\) eliminates an implication introduction/elimination detour. Capture-avoiding substitution preserves binding.

**Soundness proof structure.** Induct on the last derivation rule. For \(\land I\), the induction hypotheses make both conjuncts true. For \(\to I\), assume a model of \(\Gamma\) satisfying \(A\); the premise derivation yields \(B\). Each rule must preserve semantic consequence.

**Kernel boundary.** Parser, elaborator, automation, and tactics may be complex or untrusted relative to a small checker, but acceptance is trustworthy only if the final proof object is checked and the kernel/axioms/definitions match the claim.

## Alternatives and Trade-Offs

**Tree versus Fitch notation.** Trees expose rule dependencies; Fitch proofs scale vertically and make subproof scope visually intuitive. Both need explicit labels in mechanization.

**Proof terms versus tactics.** Terms show computational structure and are kernel inputs. Tactics improve construction ergonomics but can obscure the resulting proof unless inspectable.

**Constructive versus classical logic.** Classical principles prove more propositions and suit classical specifications. Constructive proofs retain witness/computational information and align directly with typed programs.

**Natural deduction versus sequent calculus.** Natural deduction centers introduction/elimination and assumptions. Sequent calculus makes structural proof search and duality more explicit. They support different metatheoretic workflows.

**Manual proof versus automation.** Manual steps teach invariants and yield control. Automation searches faster but needs limits, diagnostics, and a checked certificate; search failure is not generally a counterproof.

## Failure Modes and Misconceptions

1. **An assumption is a theorem.** It is available only in its scoped context.
2. **Deriving \(B\) after assuming \(A\) leaves \(B\) unconditional.** Only \(\to I\) closes the assumption and concludes \(A\to B\).
3. **A proof of \(A\lor B\) provides both sides.** It provides a tagged alternative; elimination requires both cases.
4. **Contradictory-looking prose is \(\bot\).** Falsity must be derived by rules.
5. **All natural deduction is classical.** Classical principles are optional explicit extensions.
6. **Proof checking and proof search are the same.** Checking a supplied finite tree is local; discovering one can be difficult.
7. **A theorem prover proves truth without assumptions.** Results depend on imported axioms, definitions, and kernel.
8. **Variable names alone manage scope.** Labels and capture-avoiding substitution are required.
9. **One successful example proves soundness.** Soundness quantifies over every derivation and model.
10. **Normalization preserves textual identity.** It preserves the relevant proof meaning while changing the term/tree.

## Worked Examples

### Example 1

**Question:** Derive \(A\to(B\to A)\).

**Reasoning:** Assume \(x:A\), then assume \(y:B\). Use \(x\) to derive \(A\). Discharge \(y\) to obtain \(B\to A\), then discharge \(x\).

**Conclusion:** The proof term is \(\lambda x.\lambda y.x\).

### Example 2

**Question:** Derive \((A\land B)\to(B\land A)\).

**Reasoning:** Assume \(p:A\land B\). Project \(B\) with \(\land E_2\) and \(A\) with \(\land E_1\); pair them using \(\land I\), then discharge \(p\).

**Conclusion:** Conjunction commutativity is derivable constructively.

### Example 3

**Question:** Compose \(A\to B\) and \(B\to C\).

**Reasoning:** Assume both implications and \(A\). Apply the first to get \(B\), the second to get \(C\), then discharge in reverse scope order.

**Conclusion:** Derive \((A\to B)\to((B\to C)\to(A\to C))\).

### Example 4

**Question:** Why is affirming the consequent invalid?

**Reasoning:** From \(A\to B\) and \(B\), no elimination rule yields \(A\). A valuation with \(A=false,B=true\) satisfies both premises but not \(A\).

**Conclusion:** The proposed inference is neither a rule instance nor semantically valid.

### Example 5

**Question:** Use \(A\lor B\), \(A\to C\), and \(B\to C\) to derive \(C\).

**Reasoning:** In the \(A\) branch, apply \(A\to C\). In the \(B\) branch, apply \(B\to C\). Both reach \(C\); \(\lor E\) discharges branch assumptions.

**Conclusion:** Disjunction elimination is exhaustive case analysis.

### Example 6

**Question:** Derive \(\neg(A\land\neg A)\).

**Reasoning:** Assume \(p:A\land\neg A\). Project \(A\) and \(A\to\bot\), apply them to derive \(\bot\), then discharge \(p\).

**Conclusion:** Non-contradiction is constructive for this encoding of negation.

### Example 7

**Question:** Normalize \((\lambda x.\langle x,x\rangle)\,u\).

**Reasoning:** Implication elimination immediately consumes an introduced implication. Substitute \(u\) for free \(x\), yielding \(\langle u,u\rangle\).

**Conclusion:** Normalization removes a logical detour and performs computation.

### Example 8

**Question:** Why can proving \(P(c)\) for a specific constant not establish \(\forall x.P(x)\)?

**Reasoning:** Universal introduction requires an arbitrary fresh parameter independent of special assumptions. A distinguished \(c\) may have unique properties.

**Conclusion:** The eigenvariable condition prevents special-case generalization.

### Example 9

**Question:** Does Lean's acceptance of a medication-dose theorem certify a clinical system?

**Reasoning:** Acceptance certifies a formal term relative to Lean's kernel, axioms, definitions, and encoded premises. It does not validate units, clinical requirements, sensors, code extraction, timing, or deployment. No external academic, clinical, regulatory, or practitioner review is claimed. Named qualified humans must review formalization fidelity, assumptions, implementation trace, tests, hazards, and applicable medical assurance.

**Conclusion:** Kernel checking is strong scoped evidence, not an end-to-end safety case.

### Example 10

**Question:** What does failed automated search for \(A\lor\neg A\) show in a constructive core?

**Reasoning:** It may reflect that excluded middle is not derivable constructively, or merely search limits. A semantic/metatheoretic argument is needed for non-derivability; adding excluded middle changes the calculus.

**Conclusion:** Search failure must not be overstated as a proof of impossibility.

## Cross-Program Connections

- [Programming Languages & Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) relates derivations to typing and operational meaning.
- [Functional Programming](../../03-programming-languages-functional-programming/ROADMAP.md) realizes implication and conjunction as functions and products.
- [Compilers & Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md) uses inference rules for typing and static semantics.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) benefits from distinguishing examples, countermodels, and universal proof.
- [Theory of Computation & Complexity](../../15-theory-of-computation-and-complexity/ROADMAP.md) studies decidability and proof-system limits.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) depends on explicit assumptions and trusted computing bases in formal assurance.

## References

1. Gentzen, Gerhard. “Investigations into Logical Deduction.” 1935; English translation in *The Collected Papers of Gerhard Gentzen*, 1969.
2. Prawitz, Dag. *Natural Deduction: A Proof-Theoretical Study*. Almqvist & Wiksell, 1965.
3. Pfenning, Frank. [Lecture Notes on Natural Deduction](https://www.cs.cmu.edu/~fp/courses/15317-f17/lectures/02-natded.pdf), Constructive Logic 15-317, Carnegie Mellon University, 2017.
4. Avigad, Jeremy, Leonardo de Moura, Soonho Kong, Sebastian Ullrich, and contributors. [Theorem Proving in Lean 4: Propositions and Proofs](https://docs.lean-lang.org/theorem_proving_in_lean4/Propositions-and-Proofs/). Current online edition consulted 2026-08-29.
5. Stanford Encyclopedia of Philosophy. [Natural Deduction Systems in Logic](https://plato.stanford.edu/entries/natural-deduction/). Consulted 2026-08-29.
6. Sørensen, Morten Heine, and Paweł Urzyczyn. *Lectures on the Curry-Howard Isomorphism*. Elsevier, 2006.

## Exercises

### Exercise 1

Derive \(A\to(A\land A)\), naming every rule and discharge.

### Exercise 2

Construct a derivation of \((A\to C)\to((B\to C)\to((A\lor B)\to C))\).

### Exercise 3

Diagnose this proof: assume \(x:A\), derive \(A\), conclude \(A\), and then cite that conclusion outside the subproof without applying implication introduction.

### Exercise 4

Compare constructive proof of \(\neg\neg(A\lor\neg A)\) with a classical proof of \(A\lor\neg A\). What extra principle changes the result?

### Exercise 5

Specify review evidence for a proof assistant theorem claiming that an access-control decision never grants a permission absent from policy. Separate kernel-checkable claims from named human review.

## Answers to the Exercises

### Answer 1

Assume \(x:A\). By the assumption rule derive \(A\) twice; contraction permits reusing the evidence. Apply \(\land I\) to obtain \(A\land A\). Apply \(\to I_x\), discharging \(x\), to conclude \(A\to(A\land A)\). The proof term is \(\lambda x.\langle x,x\rangle\).

### Answer 2

Assume \(f:A\to C\), \(g:B\to C\), and \(s:A\lor B\). For the left branch assume \(x:A\); \(\to E\) on \(f,x\) yields \(C\). For the right branch assume \(y:B\); \(\to E\) on \(g,y\) yields \(C\). Apply \(\lor E\) to \(s\) and the two branches, discharging \(x,y\), to obtain \(C\). Discharge \(s\), then \(g\), then \(f\), yielding the target formula.

### Answer 3

The \(A\) derived from \(x:A\) depends on the open assumption. Closing a visual block does not remove the dependency, and the conclusion cannot escape. The valid closed conclusion is \(A\to A\), obtained by \(\to I_x\). Alternatively, \(A\) can be concluded only in a context that still contains \(x:A\). The defect is scope/discharge, not the assumption rule itself.

### Answer 4

Constructively, assume \(\neg(A\lor\neg A)\). From an assumed \(A\), introduce \(A\lor\neg A\), contradiction; hence derive \(\neg A\). Introduce the right disjunct to obtain \(A\lor\neg A\), contradiction, and discharge the outer assumption, proving \(\neg\neg(A\lor\neg A)\). Removing the double negation requires a classical principle such as double-negation elimination; equivalently, excluded middle may be admitted as an axiom/rule. Constructive and classical systems must label that boundary.

### Answer 5

The checker can verify a formally stated transition/policy model, definitions of permission and grant, explicit assumptions, and a derivation that every reachable grant has policy evidence. Reproducible builds can pin kernel, libraries, axioms, source digest, and extracted artifact. Counterexample search and executable tests strengthen but do not replace the proof.

Named humans must review whether the formal model matches the real policy language, identity lifecycle, deny/override rules, administrative APIs, caches, concurrency, external authorization data, deployment configuration, and code path. They must audit axioms and trusted base, theorem statement strength, implementation/extraction trace, threat model, tests, operational bypasses, and incident behavior. No external academic, security, or practitioner review is claimed without such a named record.
