# Module 7 – Explicit Substitution Calculi ($\lambda\sigma$)

This module makes **substitution explicit** in the syntax of the $\lambda$-calculus, following the classical **$\lambda\sigma$-calculus** of Abadi–Cardelli–Curien–Lévy. Instead of treating substitution $t[s/x]$ as a *meta-operation* (Module 2), we internalize substitution as a **term constructor** and give it reduction rules.

Motivations:

* **Implementation**: $\beta$-reduction in plain $\lambda$ does immediate, capture-avoiding substitution, which can be expensive and awkward to implement. Explicit substitution calculi make substitution *first-class* and allow it to be propagated lazily.
* **Mechanization**: In proof assistants (Module 2), explicit substitution rules make confluence proofs and simulation with abstract machines (Module 6) more structural.
* **Theoretical clarity**: Explicit substitution provides a middle layer between pure $\lambda$ and concrete machines (Krivine, CEK), clarifying how environments and delayed substitutions relate to $\beta$-reduction.

We work **with De Bruijn indices** throughout and follow a **standard $\lambda\sigma$** presentation. “Plain $\lambda$-calculus” in this module always means *untyped $\lambda$ with De Bruijn indices* and $\beta$-reduction.

### Prerequisites and Dependencies

* Required: Modules 1–3 (syntax, substitution, $\beta$-reduction, confluence), Module 2’s treatment of **De Bruijn indices** and shifting.
* Helpful: Module 6 (operational semantics and abstract machines) to appreciate the implementation angle.
* Typing is **not** used here; typed explicit substitutions appear later (Modules 8–9).

From now on in this module, **terms are nameless**; $\alpha$-equivalence has already been quotiented away via De Bruijn translation (Module 2).

---

## Core 7.1 – Design Choices and Relation to the Plain $\lambda$-Calculus

Before giving the $\lambda\sigma$ syntax, we fix the relationship to the underlying $\lambda$-calculus.

### 7.1.1 Plain $\lambda$ with De Bruijn indices

Recall (Module 2) the **nameless** $\lambda$-calculus with De Bruijn indices:

* Terms:
  $$
  t ::= n \mid \lambda t \mid t\, t,
  $$
  where $n \in \mathbb{N}_{>0}$ is a positive integer index: $1$ refers to the most recently bound variable, $2$ to the next, etc.

* $\beta$-reduction (plain $\lambda$):
  $$
  (\lambda t)\, u \to_\beta t[u/1],
  $$
  where $t[u/1]$ is capture-avoiding substitution at index 1, with appropriate shifting for free indices (Module 2).

There is a **bijective correspondence** between $\alpha$-equivalence classes of named terms and nameless terms; we write
$$
\lfloor - \rfloor : \Lambda / \alpha \to \Lambda_{db}
$$
for the De Bruijn translation.

All semantic claims in this module are intended **modulo this translation**: $\lambda\sigma$ is an explicit-substitution refinement of the De Bruijn $\lambda$-calculus.

### 7.1.2 Design decision: classical $\lambda\sigma$

We now **fix** the calculus used in this module:

> From this point on, “explicit substitution calculus” means **classical $\lambda\sigma$ with De Bruijn indices**, with:
>
> * a separate syntactic category of **substitutions**,
> * no $\alpha$-equivalence (indices only),
> * reduction rules that push substitutions inside terms.

We do *not* design a new named calculus; instead we adopt a standard system and clearly specify our variant.

---

## Core 7.2 – Syntax of $\lambda\sigma$: Terms and Substitutions

We extend the nameless $\lambda$-calculus with a category of substitutions.

### 7.2.1 Syntax

#### Definition 7.1 (Terms and substitutions in $\lambda\sigma$)

The set of **terms** $t,u$ and **substitutions** $\sigma,\tau$ in $\lambda\sigma$ is given by the grammars:

* Terms:
  $$
  t ::= n \mid \lambda t \mid t\, t \mid t[\sigma]
  $$
* Substitutions:
  $$
  \sigma ::= \mathsf{id} \mid \uparrow \mid t \cdot \sigma \mid \sigma \circ \sigma.
  $$

Intuition:

* $n$ is a De Bruijn index.
* $\lambda t$ and $t\, u$ are as usual.
* $t[\sigma]$ is an **explicit application** of substitution $\sigma$ to term $t$.
* $\mathsf{id}$ is the **identity** substitution.
* $\uparrow$ is the **shift** substitution: it increases all free indices by 1.
* $t \cdot \sigma$ is “substitute $t$ for index 1, and apply $\sigma$ to indices $\ge 2$.”
* $\sigma \circ \tau$ is **composition** of substitutions.

We write $\mathsf{FV}(t)$ for free indices of $t$ exactly as in the De Bruijn setting from Module 2. Substitutions are **syntactic objects**, not meta-operations.

### 7.2.2 Informal reading of substitutions

Given an environment-style reading:

* $\mathsf{id}$ leaves all indices unchanged.
* $\uparrow$ corresponds to “going under a binder”: free indices shift by 1.
* $t \cdot \sigma$ describes a substitution $[1 \mapsto t]$ and “for $n+1$ apply $\sigma$ to $n$.”
* $\sigma \circ \tau$ means “first $\tau$, then $\sigma$.”

We will codify these intuitions via reduction rules; we do **not** define substitution as a meta-function.

---

## Core 7.3 – Reduction Rules of $\lambda\sigma$

The $\lambda\sigma$-calculus includes:

1. A $\beta$-like rule that **produces an explicit substitution**, and
2. Rules that **push substitutions inside terms** and normalize substitutions themselves.

We write $\to_{\sigma}$ for the $\lambda\sigma$ reduction relation; $\to_{\sigma}^*$ for its reflexive-transitive closure.

### 7.3.1 $\beta\sigma$: $\beta$-reduction with explicit substitution

#### Definition 7.2 ($\beta\sigma$-rule)

The $\beta$-rule in $\lambda\sigma$ is:
$$
(\lambda t)\, u \to_{\sigma} t[u \cdot \mathsf{id}],
$$

Instead of performing meta-level substitution $t[u/1]$, we attach an explicit substitution $u \cdot \mathsf{id}$ to $t$.

### 7.3.2 Propagation of substitutions inside terms

Substitutions are propagated structurally by rules that rewrite the *outermost* substitution occurrence.

#### Definition 7.3 (Propagation rules)

The propagation rules are:

1. **Variables** (indices):
   $$
   n[\mathsf{id}] \to_{\sigma} n \quad\text{(Id)},
   $$
   $$
   n[\uparrow] \to_{\sigma} n+1 \quad\text{(Shift)},
   $$
   $$
   1[t \cdot \sigma] \to_{\sigma} t \quad\text{(Cons-0)},
   $$
   $$
   (n+1)[t \cdot \sigma] \to_{\sigma} n[\sigma] \quad\text{(Cons-Succ)}.
   $$

2. **Application**:
   $$
   (t_1\, t_2)[\sigma] \to_{\sigma} t_1[\sigma]\, t_2[\sigma] \quad\text{(App-$\sigma$)}.
   $$

3. **Abstraction**:

   To go under a $\lambda$, we need to extend the substitution to account for the new binder. Here $1$ denotes the De Bruijn index term for the newly bound variable (i.e., the term consisting of the single index $1$), and $1 \cdot \rho$ denotes the substitution that maps index $1$ to $1$ (the bound variable) and indices $n+1$ to $\rho(n)$:
   $$
   (\lambda t)[\sigma] \to_{\sigma} \lambda\bigl(t[1 \cdot (\sigma \circ \uparrow)]\bigr)
   \quad\text{(Abs-$\sigma$)}.
   $$

   Intuition:

   * Index 1 becomes bound by the new $\lambda$ (so we map 1 to itself),
   * Free indices in $t$ are handled by $\sigma$, but we are one binder deeper, hence $\sigma \circ \uparrow$.

4. **Composition of substitutions**:

   Composition is normalized by:
   - **Comp-IdL**: $\mathsf{id} \circ \sigma \to_{\sigma} \sigma$
   - **Comp-IdR**: $\sigma \circ \mathsf{id} \to_{\sigma} \sigma$
   - **Comp-Shift**: $\uparrow \circ (t \cdot \sigma) \to_{\sigma} \sigma$
   - **Comp-Cons**: $(t \cdot \sigma) \circ \tau \to_{\sigma} t[\tau] \cdot (\sigma \circ \tau)$

5. **Substitution nesting**:

   Applying two substitutions in sequence is handled by composition:
   $$
   t[\sigma][\tau] \to_{\sigma} t[\sigma \circ \tau] \quad\text{(Subst-Comp)}.
   $$

The full $\lambda\sigma$ reduction relation $\to_{\sigma}$ is the **compatible closure** of $\beta\sigma$ and these rules: we may reduce inside any term or substitution position.

> *Remark.* There are slightly different presentations of $\lambda\sigma$ in the literature (e.g., some normalize composition differently, or treat $\uparrow$ via a family of shifts). The chosen rules here are a canonical, standard-style variant; all such presentations are equivalent up to straightforward encodings.

#### Lemma 7.3.1 (Local identity under binders)

For all terms $t$,
$$
t[1 \cdot \uparrow] \to_{\sigma}^* t.
$$

*Proof.* By structural induction on $t$. For variables: $n[1 \cdot \uparrow] \to_{\sigma} n$ by (Cons-0) if $n=1$, or (Cons-Succ) + (Id) if $n>1$. For $\lambda t'$: apply (Abs-$\sigma$) with $\mathsf{id}$ to get $\lambda(t'[1 \cdot (\mathsf{id} \circ \uparrow)]) = \lambda(t'[1 \cdot \uparrow])$, then IH. For applications: (App-$\sigma$) + IH. ∎

This ensures that (Abs-$\sigma$) with $\sigma = \mathsf{id}$ behaves as expected: $(\lambda t)[\mathsf{id}] \to_{\sigma}^* \lambda t$.

### 7.3.3 Example reduction

Let
$$
t_0 \equiv (\lambda \lambda 2)\, u
$$
in De Bruijn notation. In the ordinary $\lambda$-calculus:

* $t_0 \to_\beta \lambda u$.

In $\lambda\sigma$:

1. $\beta\sigma$:
   $$
   (\lambda \lambda 2)\, u \to_{\sigma} (\lambda 2)[u \cdot \mathsf{id}].
   $$

2. Propagate under $\lambda$ (Abs-$\sigma$):
   $$
   (\lambda 2)[u \cdot \mathsf{id}] \to_{\sigma}
   \lambda\bigl(2[1 \cdot ((u \cdot \mathsf{id}) \circ \uparrow)]\bigr).
   $$

3. Let $\Sigma = (u \cdot \mathsf{id}) \circ \uparrow$. By (Comp-Cons):
   $$
   (u \cdot \mathsf{id}) \circ \uparrow \to_{\sigma} u[\uparrow] \cdot (\mathsf{id} \circ \uparrow) \to_{\sigma} u[\uparrow] \cdot \mathsf{id},
   $$
   since $\mathsf{id} \circ \uparrow \to_{\sigma} \uparrow$ is not needed (we propagate directly). Now propagate $2[1 \cdot \Sigma]$: by (Cons-Succ),
   $$
   2[1 \cdot \Sigma] \to_{\sigma} 1[\Sigma].
   $$
   Then $1[\Sigma] = 1[u[\uparrow] \cdot \mathsf{id}] \to_{\sigma} u[\uparrow]$ by (Cons-0).

4. Finally, $u[\uparrow] \to_{\sigma}^* u$ if $u$ has no free index $1$ (by Lemma 7.3.1 or direct propagation). The normal form is thus $\lambda u$, whose projection is the De Bruijn term for $\lambda u$.

This matches the plain $\lambda$ result exactly.

---

## Core 7.4 – Relationship to the Plain $\lambda$-Calculus and Metatheory

We now formalize the connection between $\lambda\sigma$ and the plain De Bruijn $\lambda$-calculus, and state the core metatheoretic properties: **simulation of $\beta$**, **conservativity**, and **confluence**. We also clarify the status of **strong normalization**.

### 7.4.1 Reading $\lambda\sigma$ terms back into $\lambda$

We define a **semantic projection** that “performs all explicit substitutions” and returns a plain $\lambda$-term.

#### Definition 7.4 (Semantic projection $\llbracket - \rrbracket$)

Define $\llbracket - \rrbracket : \Lambda_{\sigma} \to \Lambda_{db}$ by structural recursion:

* On terms:
  $$
  \begin{aligned}
  \llbracket n \rrbracket &= n,\\
  \llbracket \lambda t \rrbracket &= \lambda \llbracket t \rrbracket,\\
  \llbracket t_1\, t_2 \rrbracket &= \llbracket t_1 \rrbracket\, \llbracket t_2 \rrbracket,\\
  \llbracket t[\sigma] \rrbracket &= \sigma^\ast(\llbracket t \rrbracket),
  \end{aligned}
  $$
  where $\sigma^\ast : \Lambda_{db} \to \Lambda_{db}$ is the **meta-level** action of substitution $\sigma$ on plain $\lambda$-terms, defined by structural recursion as follows.

* On indices (extended homomorphically to terms):
  $$
  \begin{aligned}
  \mathsf{id}^\ast(n) &= n,\\
  \uparrow^\ast(n) &= n+1,\\
  (t \cdot \sigma)^\ast(1) &= \llbracket t \rrbracket,\\
  (t \cdot \sigma)^\ast(n+1) &= \sigma^\ast(n),\\
  (\sigma \circ \tau)^\ast(n) &= \sigma^\ast(\tau^\ast(n)).
  \end{aligned}
  $$
  For compound terms: $\sigma^\ast(\lambda t) = \lambda(\sigma^\ast(t))$ and $\sigma^\ast(t_1\, t_2) = \sigma^\ast(t_1)\, \sigma^\ast(t_2)$.

Thus $\llbracket t[\sigma] \rrbracket$ is just “interpret $t$ and then apply the semantic action of $\sigma$”.

> Note: $\sigma^\ast$ is only used to define $\llbracket - \rrbracket$; it is not part of the $\lambda\sigma$ syntax or reduction. All **operational** reasoning remains in $\lambda\sigma$.

### 7.4.2 Simulation of $\beta$-reduction and conservativity

We first show that $\lambda\sigma$ **simulates** $\beta$-reduction on plain $\lambda$, and conversely that $\lambda$ can simulate $\lambda\sigma$ up to $\beta$-equivalence.

#### Theorem 7.5 ($\beta$-simulation)

1. If $t \to_{\sigma} t'$ in $\lambda\sigma$, then
   $$
   \llbracket t \rrbracket \to_\beta^* \llbracket t' \rrbracket.
   $$
2. If $t \to_\beta t'$ in the plain $\lambda$-calculus (De Bruijn), then there exist $\lambda\sigma$ terms $u,u'$ such that
   $$
   \llbracket u \rrbracket = t,\quad \llbracket u' \rrbracket = t',\quad \text{and} \quad u \to_{\sigma}^* u'.
   $$

*Proof sketch.*

1. Inspect each $\lambda\sigma$ rule. For example:

   * $\beta\sigma$: $(\lambda t)\, u \to_{\sigma} t[u \cdot \mathsf{id}]$. Under projection:
     $$
     \llbracket (\lambda t)\, u \rrbracket = (\lambda \llbracket t \rrbracket)\, \llbracket u \rrbracket
     \to_\beta \llbracket t \rrbracket[\llbracket u \rrbracket/1] = \llbracket t[u \cdot \mathsf{id}] \rrbracket.
     $$
   * App-$\sigma$: $(t_1\, t_2)[\sigma] \to_{\sigma} t_1[\sigma]\, t_2[\sigma]$ projects to:
     $$
     \sigma^\ast(\llbracket t_1 \rrbracket\, \llbracket t_2 \rrbracket)
     = \sigma^\ast(\llbracket t_1 \rrbracket)\, \sigma^\ast(\llbracket t_2 \rrbracket)
     = \llbracket t_1[\sigma] \rrbracket\, \llbracket t_2[\sigma] \rrbracket,
     $$
     which is **syntactic congruence** in the plain $\lambda$-calculus (0 $\beta$-steps).
   * Abs-$\sigma$: $(\lambda t)[\sigma] \to_{\sigma} \lambda(t[1 \cdot (\sigma \circ \uparrow)])$. Under projection:
     $$
     \llbracket (\lambda t)[\sigma] \rrbracket = \sigma^\ast(\lambda \llbracket t \rrbracket) = \lambda(\sigma^\ast(\llbracket t \rrbracket)),
     $$
     and
     $$
     \llbracket \lambda(t[1 \cdot (\sigma \circ \uparrow)]) \rrbracket = \lambda\bigl( (1 \cdot (\sigma \circ \uparrow))^\ast(\llbracket t \rrbracket) \bigr).
     $$
     By definition of $(1 \cdot \rho)^\ast$, this matches $\lambda(\rho^\ast(\llbracket t \rrbracket))$ with $\rho = \sigma \circ \uparrow$, which is the correct shift+substitution under $\lambda$ (0 $\beta$-steps).
   * The remaining substitution rules are designed so that $\sigma^\ast$ is respected; each step corresponds to either 0 or 1 $\beta$-steps on $\llbracket t \rrbracket$.

   Thus every $\lambda\sigma$-step maps to a finite $\beta$-sequence.

2. For a $\beta$-step $(\lambda t)\, u \to_\beta t[u/1]$ in plain $\lambda$, take the $\lambda\sigma$ term $(\lambda t)\, u$. By one $\beta\sigma$ step:
   $$
   (\lambda t)\, u \to_\sigma t[u \cdot \mathsf{id}].
   $$
   By propagating $u \cdot \mathsf{id}$ fully inside $t$ using the $\lambda\sigma$ rules, we obtain some $u'$ with
   $$
   \llbracket u' \rrbracket = t[u/1].
   $$
   This gives the required simulation. ∎

The first part is **soundness** of $\lambda\sigma$ w.r.t. $\lambda$; the second is **relative completeness** ($\lambda\beta$ is embedded in $\lambda\sigma$’s reduction).

As a corollary:

#### Corollary 7.6 (Conservativity over $\lambda$)

For $\lambda$-terms $t,u$ (De Bruijn $\lambda$), we have:

* If $t \to_\beta^* u$, then there exist $\lambda\sigma$-terms $t',u'$ with $\llbracket t' \rrbracket = t$, $\llbracket u' \rrbracket = u$ and $t' \to_{\sigma}^* u'$.
* If $t' \to_{\sigma}^* u'$ and $\llbracket t' \rrbracket = t$, then $\llbracket u' \rrbracket$ is $\beta$-equivalent to $t$.

Thus $\lambda\sigma$ is a **conservative operational refinement** of $\beta$-reduction.

### 7.4.3 Confluence

One of the main technical advantages of $\lambda\sigma$ is that confluence can be proved *structurally*, without quotienting by $\alpha$-equivalence (we already eliminated $\alpha$ by using De Bruijn).

#### Theorem 7.7 (Confluence of $\lambda\sigma$)

The $\lambda\sigma$ reduction relation $\to_{\sigma}$ is confluent:
$$
t \to_{\sigma}^* u_1,\quad t \to_{\sigma}^* u_2
\quad\Rightarrow\quad
\exists w.\ u_1 \to_{\sigma}^* w \wedge u_2 \to_{\sigma}^* w.
$$

*Proof idea.*

One standard approach:

1. Define a **parallel reduction** relation $\Rightarrow$ for $\lambda\sigma$ that:

   * Reduces **all** redexes in a term simultaneously,
   * Is compatible with all constructors, including substitution and substitution composition.

2. Prove **diamond property** for $\Rightarrow$ by structural induction on terms and substitutions (local confluence).

3. Show that $\to_{\sigma}$ and $\Rightarrow$ have the same reflexive-transitive closure:
   $$
   \to_{\sigma}^* = \Rightarrow^*.
   $$

4. Conclude confluence of $\to_{\sigma}$ from the diamond property of $\Rightarrow$.

The key point: explicit substitutions make the analysis of overlaps between $\beta$ and substitution rules **purely syntactic**; there is no hidden $\alpha$-renaming step to reason about. ∎

### 7.4.4 Strong normalization and typed systems

For the **untyped** $\lambda\sigma$-calculus, strong normalization fails just as for untyped $\lambda$: the usual diverging terms (e.g. $\Omega$ translated to De Bruijn syntax) still diverge.

More interesting is the typed setting:

#### Theorem 7.8 (Non-preservation of strong normalization – statement)

There exist type systems (e.g., simply-typed $\lambda$-calculus) such that:

* The underlying $\lambda$-calculus is **strongly normalizing**,
* But the naive typed extension of $\lambda\sigma$ (obtained by just assigning types to the added constructs) does **not** preserve strong normalization.

We do not reproduce the construction here. The upshot is that **typed explicit substitution calculi require care**: there are refined variants (e.g. $\lambda$x, $\lambda$se, …) designed specifically to preserve strong normalization of typed $\lambda$. In these notes, we use $\lambda\sigma$ in the **untyped** setting as a tool to connect $\lambda$ and machines (Modules 6, 10), and only mention typed explicit substitution briefly when needed.

---

## Core 7.5 – Applications: Interpreters, Machines, and Mechanization

We close with a brief discussion of how $\lambda\sigma$ serves as a bridge between the $\lambda$-calculus and concrete implementations.

### 7.5.1 Interpreters with explicit substitution

A naïve $\lambda$-interpreter performs substitution directly at $\beta$-steps (Module 3):

* Evaluate $(\lambda x.t)\, u$ by computing $t[u/x]$.

An interpreter based on $\lambda\sigma$ instead:

1. Replaces $\beta$ by $\beta\sigma$:
   $$
   (\lambda t)\, u \leadsto t[u \cdot \mathsf{id}]
   $$
   – one cheap syntactic step.

2. Evaluates by repeatedly applying $\lambda\sigma$ rules, effectively *propagating* substitutions only as needed.

This allows **lazy substitution**, sharing of substituted terms, and a closer relationship to environment-based machines (next section).

### 7.5.2 $\lambda\sigma$ and abstract machines

The **Krivine** and **CEK** machines (Module 6) manipulate environments and stacks instead of performing explicit syntactic substitution. $\lambda\sigma$ sits between:

* Plain $\lambda$ with implicit substitution (high-level semantics),
* Machines with explicit environments (low-level semantics).

Conceptually, one can reformulate the correctness of Krivine/CEK via $\lambda\sigma$ and the projection $\llbracket - \rrbracket$: environments in Krivine/CEK correspond to **explicit substitutions** that have been factored out of the term into a separate structure. A $\lambda\sigma$ term $t[\sigma]$ is closely related to a *closure* $(t,\rho)$ where $\rho$ is an environment corresponding to $\sigma$. We do not formalize this here, but it is conceptually important: $\lambda\sigma$ gives a clean term-level view of what machines are doing with environments.

### 7.5.3 Mechanized metatheory

In proof assistants (Coq, Agda, Lean), explicit substitution calculi like $\lambda\sigma$ are attractive because:

* $\alpha$-equivalence has already been eliminated by De Bruijn indices (Module 2).
* Substitution is *not* a recursively defined meta-function; instead it is driven by syntax-directed rules, which are easier to reason about inductively.
* Confluence (Theorem 7.7) and simulation (Theorem 7.5) can be formalized with purely **syntactic** proofs, avoiding separate $\alpha$/renaming arguments.

In later modules, when we mechanize parts of STLC and PCF (Modules 8–10), we will occasionally use $\lambda\sigma$-style reasoning to keep substitution explicit and structural.

---

## Summary and Suggested Exercises

In this module we:

* Fixed a **specific calculus**: classical $\lambda\sigma$ with De Bruijn indices (Defs. 7.1–7.3).
* Gave explicit syntax for **terms vs substitutions**, including $\mathsf{id}$, $\uparrow$, $t \cdot \sigma$, and $\sigma \circ \sigma$.
* Defined the **$\beta\sigma$-rule** and **propagation rules** for variables, application, abstraction, and composition (Defs. 7.2–7.3).
* Defined a **semantic projection** $\llbracket - \rrbracket$ from $\lambda\sigma$ back to plain $\lambda$ (Def. 7.4).
* Proved (at the statement level) that $\lambda\sigma$ **simulates** and **refines** $\beta$-reduction (Theorem 7.5, Corollary 7.6).
* Stated confluence of $\lambda\sigma$ (Theorem 7.7), with a standard proof architecture via parallel reduction.
* Clarified that, in typed settings, naive $\lambda\sigma$ does **not** preserve strong normalization (Theorem 7.8 – statement).
* Explained how $\lambda\sigma$ bridges plain $\lambda$, abstract machines (Module 6), and mechanized proofs (Module 2).

This gives us a robust, standard explicit substitution calculus that we can refer to in later modules, without hand-wavy or underspecified syntax.

---

### Suggested Exercises

1. **Basic $\lambda\sigma$ steps**

   Work in De Bruijn syntax. For each term:

   1. $(\lambda 1)\, u$
   2. $(\lambda \lambda 2)\, u$

   Give a $\lambda\sigma$ reduction sequence from the initial term to one whose projection $\llbracket - \rrbracket$ is in $\beta$-normal form (no $\beta$-redex).

2. **Projection sanity check**

   Show that for any term $t$ (plain De Bruijn $\lambda$-term), if we view $t$ as a $\lambda\sigma$-term without substitutions, then:
   $$
   \llbracket t \rrbracket = t.
   $$
   Conclude that $\lambda\sigma$ is a genuine extension of $\lambda$.

3. **Substitution propagation**

   Compute explicitly, using the $\lambda\sigma$ rules, the normal form of:
   $$
   (\lambda . (1\, 2))[u \cdot \mathsf{id}].
   $$
   Then check that its projection matches the standard $\beta$-substitution result in the plain $\lambda$-calculus.

4. **Confluence local diamond**

   Pick one non-trivial overlap between rules (e.g., App-$\sigma$ and Subst-Comp) and show the **local diamond** property by hand:
   $$
   t \to_{\sigma} t_1,\quad t \to_{\sigma} t_2
   \quad\Rightarrow\quad
   \exists w.\ t_1 \to_{\sigma}^* w \wedge t_2 \to_{\sigma}^* w.
   $$

5. **Machine correspondence (informal)**

   For a simple closed term $t$, describe informally how a run of the CEK machine (Module 6) corresponds to a $\lambda\sigma$-reduction sequence on some $\lambda\sigma$-term $u$ with $\llbracket u \rrbracket = t$. Where do environments “live” in $\lambda\sigma$, and how do they compare to substitutions $t \cdot \sigma$?

6. **Typed $\lambda\sigma$ caveat**

   Explain why the possibility of **non-preservation of strong normalization** (Theorem 7.8) matters when designing a typed explicit substitution calculus. What goes wrong if we naively assign types to all $\lambda\sigma$ constructs without adjusting the rules?
