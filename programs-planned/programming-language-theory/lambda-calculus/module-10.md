# Module 10 – PCF and Observational Equivalence

In this module we introduce **PCF** (Programming Computable Functions), a simply-typed $\lambda$-calculus extended with:

* base types $\mathsf{Nat}$ and $\mathsf{Bool}$,
* constants and primitives on these types,
* a **fixed-point** operator $\mathsf{fix}$ providing general recursion.

PCF is a canonical core calculus for functional languages with recursion. We:

1. Define PCF’s **syntax**, **types**, and **typing rules**.
2. Give a **small-step operational semantics** (call-by-name with strict ground operations).
3. Define **typed contexts** and **observational (contextual) equivalence** rigorously.
4. Present a standard **denotational semantics** in domains with bottom.
5. State an **adequacy theorem** linking operational termination at ground types to semantic non-bottom (proved in Appendix 10.A).
6. Formulate the **full abstraction problem** and state the known failure of the standard domain model, with a pointer to game semantics.

We **do not** prove full abstraction here.

---

## 10.1 Types, Terms, and Typing Rules of PCF

### 10.1.1 Types

We extend the STLC types (Module 8) with two distinguished base types.

**Definition 10.1 (PCF types).**

$$
A ::= \mathsf{Nat} \mid \mathsf{Bool} \mid A \to A
$$

No products, sums, or recursive types are built in; they can be encoded or added later.

---

### 10.1.2 Terms

PCF terms extend STLC terms with numerals, booleans, arithmetic/boolean primitives, conditional, and $\mathsf{fix}$.

We write application by **juxtaposition**: $t\, u$.

**Definition 10.2 (PCF terms).**

$$
\begin{aligned}
t ::= &\, x \\
     &\, \mid \lambda x.t \\
     &\, \mid t\, t \\
     &\, \mid \overline{n} \quad (n \in \mathbb{N}) \\
     &\, \mid \mathsf{succ}\, t
       \mid \mathsf{pred}\, t
       \mid \mathsf{iszero}\, t \\
     &\, \mid \mathsf{true}
       \mid \mathsf{false}
       \mid \mathsf{if}\, t\, \mathsf{then}\, t\, \mathsf{else}\, t \\
     &\, \mid \mathsf{fix}\, t
\end{aligned}
$$

Numerals $\overline{n}$ are syntactic constants. $\mathsf{true}$ and $\mathsf{false}$ are the only boolean literals.

---

### 10.1.3 Typing rules

Typing contexts $\Gamma$ and the core rules T-Var, T-Abs, T-App are as in Module 8. We add rules for numerals, booleans, primitives, conditional, and $\mathsf{fix}$.

**Definition 10.3 (Typing rules for PCF primitives).**

- **T-Num**: $\Gamma \vdash \overline{n} : \mathsf{Nat}$
- **T-True**: $\Gamma \vdash \mathsf{true} : \mathsf{Bool}$
- **T-False**: $\Gamma \vdash \mathsf{false} : \mathsf{Bool}$

- **T-Succ** (premise: $\Gamma \vdash t : \mathsf{Nat}$): $\Gamma \vdash \mathsf{succ}\, t : \mathsf{Nat}$
- **T-Pred** (premise: $\Gamma \vdash t : \mathsf{Nat}$): $\Gamma \vdash \mathsf{pred}\, t : \mathsf{Nat}$

- **T-IsZero** (premise: $\Gamma \vdash t : \mathsf{Nat}$): $\Gamma \vdash \mathsf{iszero}\, t : \mathsf{Bool}$

- **T-If** (premises: $\Gamma \vdash t_1 : \mathsf{Bool}$, $\Gamma \vdash t_2 : A$, $\Gamma \vdash t_3 : A$): $\Gamma \vdash \mathsf{if}\, t_1\, \mathsf{then}\, t_2\, \mathsf{else}\, t_3 : A$

- **T-Fix** (premise: $\Gamma \vdash t : A \to A$): $\Gamma \vdash \mathsf{fix}\, t : A$

Thus at the meta-level, $\mathsf{fix}$ has type $(A \to A) \to A$: given $t : A \to A$, $\mathsf{fix}\, t : A$ is intended to satisfy

$$
\mathsf{fix}\, t \approx t\,(\mathsf{fix}\, t)
$$

operationally (see §10.2).

**Example 10.4.** A “constant-zero” functional:

$$
\mathsf{fix}\, (\lambda f.\lambda n.\overline{0}) : \mathsf{Nat} \to \mathsf{Nat}.
$$

Sketch:

* $f:\mathsf{Nat}\to\mathsf{Nat}, n:\mathsf{Nat} \vdash \overline{0} : \mathsf{Nat}$ (T-Num),
* $f:\mathsf{Nat}\to\mathsf{Nat} \vdash \lambda n.\overline{0} : \mathsf{Nat}\to\mathsf{Nat}$ (T-Abs),
* $\emptyset \vdash \lambda f.\lambda n.\overline{0} : (\mathsf{Nat}\to\mathsf{Nat})\to(\mathsf{Nat}\to\mathsf{Nat})$,
* T-Fix yields $\emptyset \vdash \mathsf{fix}(\lambda f.\lambda n.\overline{0}) : \mathsf{Nat}\to\mathsf{Nat}$.

Note: adding $\mathsf{fix}$ destroys **strong normalization**, but we retain **type safety** (progress + preservation).

---

## 10.2 Operational Semantics of PCF (Call-by-Name with Strict Ground Operations)

We define a **call-by-name** (CBN) small-step semantics. $\beta$-steps are allowed regardless of whether the argument is a value. Arguments are only evaluated when demanded by primitives or as branch conditions in conditionals.

### 10.2.1 Values

**Definition 10.5 (Values).**

$$
v ::= \lambda x.t \mid \overline{n} \mid \mathsf{true} \mid \mathsf{false}
$$

Only these terms are values.

### 10.2.2 Canonical Forms for Base Types

To support the type safety proof, we state the canonical forms for the base types.

**Lemma 10.6 (Canonical forms: $\mathsf{Nat}$).**
If $\emptyset \vdash v : \mathsf{Nat}$ and $v$ is a value, then $v = \overline{n}$ for some $n \in \mathbb{N}$.

*Proof.* By inversion on the typing derivation: the only rule yielding $\mathsf{Nat}$ for a value is T-Num. ∎

**Lemma 10.7 (Canonical forms: $\mathsf{Bool}$).**
If $\emptyset \vdash v : \mathsf{Bool}$ and $v$ is a value, then $v = \mathsf{true}$ or $v = \mathsf{false}$.

*Proof.* By inversion on the typing derivation: the only rules yielding $\mathsf{Bool}$ for a value are T-True and T-False. ∎

### 10.2.3 Primitive reduction rules

**Definition 10.8 (Primitive reduction rules).**

$\beta$ and fix:

$$
\begin{array}{ll}
(\lambda x.t)\, u \to t[u/x] & (\beta) \\
\mathsf{fix}\, t \to t\,(\mathsf{fix}\, t) & (\mathsf{fix})
\end{array}
$$

Arithmetic and boolean primitives:

$$
\begin{array}{ll}
\mathsf{succ}\,\overline{n} \to \overline{n+1} \\
\mathsf{pred}\,\overline{0} \to \overline{0}
\qquad
\mathsf{pred}\,\overline{n+1} \to \overline{n} \\
\mathsf{iszero}\,\overline{0} \to \mathsf{true}
\qquad
\mathsf{iszero}\,\overline{n+1} \to \mathsf{false}
\end{array}
$$

Conditional:

$$
\begin{array}{ll}
\mathsf{if}\, \mathsf{true}\, \mathsf{then}\, t_2\, \mathsf{else}\, t_3 \to t_2 \\
\mathsf{if}\, \mathsf{false}\, \mathsf{then}\, t_2\, \mathsf{else}\, t_3 \to t_3
\end{array}
$$

We do **not** reduce under $\lambda$-abstractions.

### 10.2.4 Evaluation contexts and contextual closure

We now restrict where reductions can occur to obtain the CBN strategy with strict evaluation of arguments to ground primitives, conditionals, and $\mathsf{fix}$.

**Definition 10.9 (Evaluation contexts, call-by-name).**

$$
\begin{aligned}
E ::= &\, [\cdot] \\
      &\, \mid E\, t \\
      &\, \mid \mathsf{succ}\, E
        \mid \mathsf{pred}\, E
        \mid \mathsf{iszero}\, E \\
      &\, \mid \mathsf{if}\, E\, \mathsf{then}\, t\, \mathsf{else}\, t \\
      &\, \mid \mathsf{fix}\, E
\end{aligned}
$$

**Definition 10.10 (Contextual closure).**

We write $t \to_{PCF} t'$ iff there exist an evaluation context $E$, and primitive redex $r$ and contractum $r'$, such that:

$$
t = E[r],\quad r \to r' \text{ (primitive rule)},\quad t' = E[r'].
$$

We write $\to_{PCF}^*$ for the reflexive–transitive closure. We write $t \Downarrow v$ if $t \to_{PCF}^* v$ with $v$ a value.

**Theorem 10.11 (Type safety).**
For PCF:

* (**Progress**) If $\emptyset \vdash t : A$, then either $t$ is a value or there exists $t'$ with $t \to_{PCF} t'$.
* (**Preservation**) If $\Gamma \vdash t : A$ and $t \to_{PCF} t'$, then $\Gamma \vdash t' : A$.

*Proof.* By straightforward extension of Module 9. Canonical forms for function types are as in Lemma 9.1; for base types, see Lemmas 10.6 and 10.7.

For progress on T-Fix: given $\emptyset \vdash \mathsf{fix}\, t_0 : A$ (so $\emptyset \vdash t_0 : A \to A$), apply the induction hypothesis to $t_0$. If $t_0 \to t_0'$, then $\mathsf{fix}\, t_0 \to \mathsf{fix}\, t_0'$ by the evaluation context $\mathsf{fix}\, E$. If $t_0$ is a value, then by canonical forms for $A \to A$ ($t_0 = \lambda x.u$), we have $\mathsf{fix}\, (\lambda x.u) \to (\lambda x.u)\, (\mathsf{fix}\, (\lambda x.u))$ by the $\mathsf{fix}$ rule.

For preservation on T-Fix: given $\Gamma \vdash \mathsf{fix}\, t_0 : A$ and $\mathsf{fix}\, t_0 \to t_0\, (\mathsf{fix}\, t_0)$, we have $\Gamma \vdash t_0 : A \to A$ by inversion. Then $\Gamma \vdash \mathsf{fix}\, t_0 : A$ again by T-Fix, so $\Gamma \vdash t_0\, (\mathsf{fix}\, t_0) : A$ by T-App. All other cases are as in Module 9 or immediate for the new primitives. ∎

---

## 10.3 Typed Contexts and Observational (Contextual) Equivalence

We now define **observational equivalence** via typed contexts and ground-type observations.

### 10.3.1 Typed contexts

We work with one-hole contexts that are typable.

**Definition 10.12 (Typed contexts).**

A **context** $C[-]$ is a PCF term with a single distinguished hole $[-]$. We write

$$
\Gamma \vdash C[\{- \}] : A \Rightarrow B
$$

if, whenever $\Gamma \vdash t : A$, we have $\Gamma \vdash C[t] : B$. This judgement is defined inductively on $C$ using the typing rules of PCF.

Examples:

* Empty context: $[-]$ has type $A \Rightarrow A$.
* Left application: if $\Gamma \vdash D[-] : A \Rightarrow (B \to C)$ and $\Gamma \vdash u : B$, then $\Gamma \vdash D[-]\, u : A \Rightarrow C$.
* Conditional guard: if $\Gamma \vdash D[-] : A \Rightarrow \mathsf{Bool}$ and $\Gamma \vdash t_2 : B$, $\Gamma \vdash t_3 : B$, then
  $$
  \Gamma \vdash \mathsf{if}\, D[\{- \}]\, \mathsf{then}\, t_2\, \mathsf{else}\, t_3 : A \Rightarrow B.
  $$

We are interested in **closing contexts** with empty environment:

$$
\emptyset \vdash C[\{- \}] : A \Rightarrow G,
$$

where $G$ is a **ground type**.

**Definition 10.13 (Ground types).**

$$
G ::= \mathsf{Nat} \mid \mathsf{Bool}.
$$

### 10.3.2 Observations at ground types

For a closed term $\emptyset \vdash t : G$, with $G$ ground, we observe:

* whether $t$ **terminates** ($t \Downarrow v$),
* and, if so, which **value** $v$ it terminates to.

Concretely:

* For $G = \mathsf{Nat}$: either divergence, or convergence to some numeral $\overline{n}$.
* For $G = \mathsf{Bool}$: either divergence, or convergence to $\mathsf{true}$ or $\mathsf{false}$.

### 10.3.3 Observational / contextual equivalence

**Definition 10.14 (Observational equivalence).**

Let $\emptyset \vdash t : A$ and $\emptyset \vdash u : A$. We say $t$ and $u$ are **observationally equivalent** (or **contextually equivalent**),

$$
t \approx u,
$$

if for every **ground type** $G$ and every closing context

$$
\emptyset \vdash C[\{- \}] : A \Rightarrow G,
$$

we have:

1. $C[t]$ terminates iff $C[u]$ terminates;
2. if both terminate, they terminate to the same ground value.

We also write $t \equiv_{ctx} u$ for $t \approx u$.

**Lemma 10.15 (Congruence).**
If $t \approx u$ and $C[-]$ is any (well-typed) context, then

$$
C[t] \approx C[u].
$$

*Proof.* Immediate from the definition, since contextual equivalence quantifies over all closing contexts, including those obtained by composing with $C[-]$. ∎

**Example 10.16.**
Let $I := \lambda x.x$ and $I' := \lambda y.y$ of type $A \to A$. Then $I \approx I'$: these terms are $\alpha$-equivalent (modulo renaming of bound variables, as assumed since Module 1), and hence the same $\alpha$-equivalence class. Thus they have identical evaluation behavior in any closing context $\emptyset \vdash C[\{- \}] : A \to A \Rightarrow G$.

---

## 10.4 Denotational Semantics and Adequacy

We now give a standard **Scott-style domain model** and state the **adequacy theorem** that connects denotational non-bottom with operational termination at ground types.

### 10.4.1 Domains and type interpretation

We work in a category of **pointed cpos** (complete partial orders with least element $\bot$) and continuous functions.

**Definition 10.17 (Base domains).**

* $\mathbb{N}_\bot$: flat domain of naturals with bottom. Elements: $\{\bot\} \cup \mathbb{N}$, with order $\bot \sqsubseteq n$ for all $n$ and no other non-trivial order.
* $\mathbb{B}_\bot$: flat domain of booleans with bottom. Elements: $\{\bot, \mathsf{tt}, \mathsf{ff}\}$, with $\bot \sqsubseteq \mathsf{tt}$, $\bot \sqsubseteq \mathsf{ff}$, and no other non-trivial order.

We interpret PCF types as domains:

**Definition 10.18 (Type interpretation).**

$$
\begin{aligned}
\llbracket \mathsf{Nat} \rrbracket &:= \mathbb{N}_\bot, \\
\llbracket \mathsf{Bool} \rrbracket &:= \mathbb{B}_\bot, \\
\llbracket A \to B \rrbracket &:= [\llbracket A \rrbracket \to_{cont} \llbracket B \rrbracket],
\end{aligned}
$$

where the last is the cpo of **continuous** functions from $\llbracket A \rrbracket$ to $\llbracket B \rrbracket$.

We write $\mathsf{tt},\mathsf{ff}$ for the semantic booleans in $\mathbb{B}_\bot$, corresponding to syntactic $\mathsf{true},\mathsf{false}$.

An **environment** $\rho$ for a context $\Gamma$ maps each $x:A \in \Gamma$ to an element $\rho(x) \in \llbracket A \rrbracket$.

### 10.4.2 Interpretation of terms

**Definition 10.19 (Term interpretation).**

For each judgement $\Gamma \vdash t : A$ and environment $\rho$ for $\Gamma$, we define $\llbracket t \rrbracket_\rho \in \llbracket A \rrbracket$ by recursion on $t$:

* Variables:
  $$
  \llbracket x \rrbracket_\rho := \rho(x).
  $$
* Abstraction:
  $$
  \llbracket \lambda x.t \rrbracket_\rho := (d \mapsto \llbracket t \rrbracket_{\rho[x\mapsto d]}).
  $$
* Application:
  $$
  \llbracket t_1\, t_2 \rrbracket_\rho := \llbracket t_1 \rrbracket_\rho(\llbracket t_2 \rrbracket_\rho).
  $$
* Numerals and booleans:
  $$
  \llbracket \overline{n} \rrbracket_\rho = n \in \mathbb{N}_\bot,\quad
  \llbracket \mathsf{true} \rrbracket_\rho = \mathsf{tt},\quad
  \llbracket \mathsf{false} \rrbracket_\rho = \mathsf{ff}.
  $$
* Primitives (strict at $\bot$):
  $$
  \llbracket \mathsf{succ}\, t \rrbracket_\rho =
  \begin{cases}
  \bot & \text{if } \llbracket t \rrbracket_\rho = \bot, \\
  n+1 & \text{if } \llbracket t \rrbracket_\rho = n,
  \end{cases}
  $$
  and similarly for $\mathsf{pred}$ and $\mathsf{iszero}$ in the obvious way.
* Conditional:
  $$
  \llbracket \mathsf{if}\, t_1\, \mathsf{then}\, t_2\, \mathsf{else}\, t_3 \rrbracket_\rho =
  \begin{cases}
  \bot & \llbracket t_1 \rrbracket_\rho = \bot, \\
  \llbracket t_2 \rrbracket_\rho & \llbracket t_1 \rrbracket_\rho = \mathsf{tt}, \\
  \llbracket t_3 \rrbracket_\rho & \llbracket t_1 \rrbracket_\rho = \mathsf{ff}.
  \end{cases}
  $$
* Fixpoint:
  $$
  \llbracket \mathsf{fix}\, t \rrbracket_\rho := \mathsf{lfp}(\llbracket t \rrbracket_\rho),
  $$
  where $\mathsf{lfp}$ is the **least fixed point** of the continuous function
  $$
  F := \llbracket t \rrbracket_\rho : \llbracket A \rrbracket \to \llbracket A \rrbracket.
  $$

Standard domain theory ensures all clauses are well-defined and continuous.

For closed $\emptyset \vdash t : A$, we write simply $\llbracket t \rrbracket := \llbracket t \rrbracket_\emptyset$.

### 10.4.3 Soundness and adequacy

We first relate one-step reduction to semantics.

**Theorem 10.20 (Soundness of denotational semantics).**

If $\emptyset \vdash t : A$ and $t \to_{PCF} t'$, then

$$
\llbracket t \rrbracket = \llbracket t' \rrbracket.
$$

Consequently, if $t \to_{PCF}^* v$ with $v$ a value, then $\llbracket t \rrbracket = \llbracket v \rrbracket$.

*Proof (sketch).* Each primitive reduction ($\beta$, fix, primitives, conditionals) preserves denotation by unfolding the semantic clauses. Contextual closure is handled by induction on evaluation contexts, using compositionality of $\llbracket - \rrbracket$. ∎

We now state **adequacy** at ground types. The proof is given in **Appendix 10.A** via a logical-relations argument.

**Theorem 10.21 (Adequacy for PCF at ground types).**

Let $\emptyset \vdash t : G$ with $G \in \{\mathsf{Nat},\mathsf{Bool}\}$.

1. If $t \Downarrow v$ for some ground value $v$, then $\llbracket t \rrbracket = \llbracket v \rrbracket \neq \bot$.
2. If $\llbracket t \rrbracket \neq \bot$, then $t \Downarrow v$ for some ground value $v$ with $\llbracket v \rrbracket = \llbracket t \rrbracket$.

Thus, at ground types, **may-termination ⇔ denotation is non-bottom**.

### 10.4.4 Semantic equality implies contextual equivalence

We now relate the domain model to contextual equivalence.

First note that denotational semantics is **compositional over contexts**:

**Lemma 10.22 (Compositionality for typed contexts).**

Let $\emptyset \vdash t : A$ and $\emptyset \vdash C[\{- \}] : A \Rightarrow B$. Then there is a continuous function

$$
\llbracket C \rrbracket : \llbracket A \rrbracket \to \llbracket B \rrbracket
$$

such that:

$$
\llbracket C[t] \rrbracket = \llbracket C \rrbracket(\llbracket t \rrbracket).
$$

*Proof.* By induction on the structure/typing of $C[-]$, using the clauses of Definition 10.19. ∎

Using this, we obtain:

**Lemma 10.23 (Semantic equality ⇒ contextual equivalence).**

Let $\emptyset \vdash t : A$ and $\emptyset \vdash u : A$. If

$$
\llbracket t \rrbracket = \llbracket u \rrbracket,
$$

then $t \approx u$.

*Proof.* Fix any ground type $G$ and closing context $\emptyset \vdash C[\{- \}] : A \Rightarrow G$. By Lemma 10.22,

$$
\llbracket C[t] \rrbracket = \llbracket C \rrbracket(\llbracket t \rrbracket)
= \llbracket C \rrbracket(\llbracket u \rrbracket) = \llbracket C[u] \rrbracket.
$$

At ground types, by adequacy (Theorem 10.21):

* $C[t]$ terminates iff $\llbracket C[t] \rrbracket \neq \bot$,
* $C[u]$ terminates iff $\llbracket C[u] \rrbracket \neq \bot$,
* and when both terminate, they terminate to the same ground value denoting $\llbracket C[t] \rrbracket = \llbracket C[u] \rrbracket$.

Hence $C[t]$ and $C[u]$ have the same observation for every such context. Therefore $t \approx u$. ∎

So the standard model is **sound** w.r.t. contextual equivalence:

$$
\llbracket t \rrbracket = \llbracket u \rrbracket \Rightarrow t \approx u.
$$

What fails is the converse (full abstraction).

---

## 10.5 The Full Abstraction Problem for PCF

Adequacy plus soundness tell us:

* If two PCF terms are distinguishable by some context (at ground types), then they have **different denotations** in the standard domain model.
* If a ground term has denotation $\neq \bot$, it terminates.

However, the standard model is **too fine**: it sees distinctions that no PCF context can observe.

### 10.5.1 Full abstraction

**Definition 10.24 (Fully abstract model for PCF).**

A denotational semantics $\llbracket - \rrbracket$ for PCF is **fully abstract** if, for all closed terms $\emptyset \vdash t : A$ and $\emptyset \vdash u : A$,

$$
t \approx u \quad\Longleftrightarrow\quad \llbracket t \rrbracket = \llbracket u \rrbracket.
$$

Equivalently, denotational equality coincides exactly with operational indistinguishability in all typed contexts.

The standard Scott model of §10.4 is:

* adequate and sound (Theorems 10.20, 10.21, Lemma 10.23),
* but **not** fully abstract.

**Theorem 10.25 (Standard domain model is not fully abstract).**

In the Scott model of Definitions 10.17–10.19, there exist closed PCF terms $\emptyset \vdash t : A$, $\emptyset \vdash u : A$ such that:

* $t \approx u$, but
* $\llbracket t \rrbracket \neq \llbracket u \rrbracket$.

In other words, the model semantically distinguishes some terms that no PCF context can distinguish; semantic equality is a **strict refinement** of contextual equivalence.

We do not construct such a pair $(t,u)$ here; this is a standard and non-trivial result in the literature. The existence of such pairs motivates the search for **fully abstract** models.

**Problem 10.26 (Full abstraction for PCF).**

Construct a denotational model of PCF such that

$$
t \approx u \quad\Longleftrightarrow\quad \llbracket t \rrbracket = \llbracket u \rrbracket.
$$

### 10.5.2 Preview: game semantics

One successful answer to Problem 10.26 uses **game semantics**:

* Each type $A$ is interpreted as a **game** (an interaction protocol between program and environment).
* Each term $t : A$ is interpreted as a **strategy** for playing that game.
* Composition of programs corresponds to composition of strategies.

By imposing suitable constraints (e.g. innocence, well-bracketing), one obtains models where:

* contextually equivalent PCF terms have the **same strategy**,
* and distinct strategies give rise to separating contexts.

Such game models are known to be **fully abstract** for PCF. They will be treated later in the semantic part of the course (e.g., Module 18).

---

## 10.6 Summary and Exercises

In this module we:

* Defined **PCF**: STLC with base types $\mathsf{Nat}$, $\mathsf{Bool}$, constants, and a fixed-point operator $\mathsf{fix}$.
* Gave a **call-by-name small-step semantics** with $\beta$-, fix-unfold, and primitive rules and CBN evaluation contexts (strict at ground operations).
* Introduced **typed contexts** and **observational/contextual equivalence** $\approx$ at all types, using ground-type observations.
* Built a standard **Scott-style domain model** with $\llbracket \mathsf{Nat} \rrbracket = \mathbb{N}_\bot$, $\llbracket \mathsf{Bool} \rrbracket = \mathbb{B}_\bot$, and function spaces as continuous maps.
* Proved **soundness** of semantics w.r.t. reduction and stated **adequacy at ground types** (proved in Appendix 10.A).
* Showed that **semantic equality implies contextual equivalence**, but not conversely.
* Formulated the **full abstraction problem** and noted that the standard domain model is **not** fully abstract, with a pointer to **game semantics** as a fully abstract alternative.

---

### Appendix 10.A: Proof of Adequacy via Logical Relations

We sketch the proof of Theorem 10.21 using logical relations, restricted to closed terms for simplicity (the open-term version follows by extending to environments).

Define **reducibility relations** $R_A \subseteq \{ t \mid \emptyset \vdash t : A \}$ by induction on $A$:

* For ground $G \in \{\mathsf{Nat}, \mathsf{Bool}\}$: $R_G := \{ t \mid t \Downarrow v \text{ for some value } v \}$.
* For $A \to B$: $R_{A \to B} := \{ t \mid \emptyset \vdash t : A \to B \text{ and } \forall u \in R_A.\ t\, u \in R_B \}$.

**Lemma 10.A.1 (Fundamental lemma).** If $\emptyset \vdash t : A$ then $t \in R_A$.

*Proof (sketch).* By induction on the typing derivation.

* For base cases (T-Num, T-True, T-False): immediate, as constants terminate to themselves.
* For T-App: $t = t_1\, t_2$, $\emptyset \vdash t_1 : C \to A$, $\emptyset \vdash t_2 : C$. By IH, $t_1 \in R_{C \to A}$, $t_2 \in R_C$, so $t_1\, t_2 \in R_A$.
* For T-Abs: $t = \lambda x. u$, $\emptyset, x:C \vdash u : A$. For any $v \in R_C$, $(\lambda x. u)\, v \to u[v/x]$; by preservation, $\emptyset \vdash u[v/x] : A$. Lifting the relation to open terms (standard), $u[v/x] \in R_A$.
* For primitives (T-Succ, etc.): if argument in $R_{\mathsf{Nat}}$, the primitive terminates to a value.
* For T-If: if guard in $R_{\mathsf{Bool}}$ (terminates to $\mathsf{true}/\mathsf{false}$), selects the corresponding branch, which is in $R_A$ by IH.
* For T-Fix: $t = \mathsf{fix}\, f$, $\emptyset \vdash f : A \to A$. By IH, $f \in R_{A \to A}$. Unfolding shows $\mathsf{fix}\, f \in R_A$ (standard fixed-point argument in logical relations).

∎

**Theorem 10.21 (restated).** Follows from Lemma 10.A.1: for ground $G$, $t \in R_G$ iff $t \Downarrow v$ iff $\llbracket t \rrbracket \neq \bot$ (by soundness, since all ground values denote non-bottom).

Full details (including $\mathsf{fix}$ and open terms) are standard; see, e.g., Winskel (1993).

---

### Suggested Exercises

1. **Operational trace.**
   Define
   $$
   \mathsf{pred1} := \mathsf{pred}\,(\mathsf{succ}\,\overline{0}).
   $$
   (a) Show $\emptyset \vdash \mathsf{pred1} : \mathsf{Nat}$.
   (b) Compute the full reduction sequence $\mathsf{pred1} \to_{PCF}^* \overline{0}$ under the CBN semantics. (Note: The evaluation context $\mathsf{pred}\, E$ with $E = [\mathsf{succ}\,\overline{0}]$ first reduces the argument via $\mathsf{succ}\,\overline{0} \to \overline{1}$, yielding $\mathsf{pred}\,\overline{1}$; then $\mathsf{pred}\,\overline{1} \to \overline{0}$.)

2. **A simple PCF program.**
   Define
   $$
   \mathsf{idNat} := \mathsf{fix}\, (\lambda f.\lambda n.n) : \mathsf{Nat} \to \mathsf{Nat}.
   $$
   Show that for all numerals $\overline{n}$, we have $\mathsf{idNat}\,\overline{n} \Downarrow \overline{n}$.

3. **Contextual equivalence with fix.**
   Show that
   $$
   \lambda x.x \approx \mathsf{fix}\, (\lambda f.\lambda x.x)
   $$
   as terms of type $A \to A$. Hint: for any closing context $\emptyset \vdash C[\{- \}] : A\to A \Rightarrow G$, argue that $C[\lambda x.x]$ and $\mathsf{fix}(\lambda f.\lambda x.x)$ have the same denotation and thus the same observation.

4. **Soundness check for if.**
   Prove in detail that
   $$
   \mathsf{if}\, \mathsf{true}\, \mathsf{then}\, t_2\, \mathsf{else}\, t_3 \to t_2
   $$
   implies
   $$
   \llbracket \mathsf{if}\, \mathsf{true}\, \mathsf{then}\, t_2\, \mathsf{else}\, t_3 \rrbracket
   = \llbracket t_2 \rrbracket
   $$
   for all environments.

5. **Adequacy sketch via logical relations.**
   For type $\mathsf{Nat}$, define a predicate
   $$
   R_{\mathsf{Nat}}(t) :\equiv \exists n.\ t \Downarrow \overline{n}.
   $$
   Sketch how a logical-relations argument (as in Appendix 10.A) shows that for closed $\emptyset \vdash t : \mathsf{Nat}$, $\llbracket t \rrbracket \neq \bot$ implies $R_{\mathsf{Nat}}(t)$.

6. **Failure of full abstraction (conceptual).**
   Formulate precisely what it means for two closed PCF terms $t,u : A$ to satisfy:

   * $t \approx u$, but
   * $\llbracket t \rrbracket \neq \llbracket u \rrbracket$.

   Explain why the existence of such a pair shows that the Scott model is **not** fully abstract. (You do not need to construct an explicit pair.)
