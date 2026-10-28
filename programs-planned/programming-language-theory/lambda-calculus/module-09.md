# Module 9 – STLC Metatheory and Data Types

In this module, we establish the basic **metatheory** of the Simply Typed $\lambda$-Calculus (STLC):

* **Canonical forms** for all type formers (functions, products, sums, unit, empty),
* **Progress**: well-typed closed terms do not get stuck,
* **Preservation**: types are invariant under reduction,
* **Strong normalization** for a precisely **bounded fragment** (presented as a proof sketch).

We extend the core STLC of Module 8 with standard **data types**:

* products $A \times B$,
* sums $A + B$,
* unit $1$,
* empty type $0$.

These correspond, via **Curry–Howard**, to $\land$, $\lor$, $\top$, and $\bot$ of intuitionistic propositional logic.

The **strong normalization** result in this module is restricted to:

> STLC with types built from **base types** and the connectives
> $\to,\ \times,\ +,\ 1,\ 0$;
> **no recursive types** and **no general recursion**.

Recursive types and general recursion are previewed only at the end; they are **not** covered by the SN theorem here.

We assume:

* Typing rules from **Module 8** (extended here to products/sums/unit/empty),
* A **small-step evaluation relation** $\to$ as in Module 6, specialized to this language,
* The **typed substitution lemma** (Lemma 8.6).

---

## 9.1 Language and Evaluation

### 9.1.1 Types

We extend the type grammar of Module 8 as follows.

**Definition 9.1 (Types).**

$$
A ::= B \mid A \to A \mid A \times A \mid A + A \mid 1 \mid 0
$$

where $B$ ranges over a fixed set of **base types** (e.g. Bool, Nat, …).

* $A \to B$ – function type.
* $A \times B$ – product type.
* $A + B$ – sum type.
* $1$ – unit type.
* $0$ – empty type.

Right-associativity convention for arrows: $A \to B \to C \equiv A \to (B \to C)$.

### 9.1.2 Terms

We extend the term syntax of Module 8.

**Definition 9.2 (Terms).**

$$
\begin{aligned}
t ::= &\ x \mid \lambda x.t \mid t\, t \\
&\mid \langle t, t \rangle \mid \mathsf{fst}\, t \mid \mathsf{snd}\, t \\
&\mid \mathsf{inl}\, t \mid \mathsf{inr}\, t \\
&\mid \mathsf{case}\ t\ \mathsf{of}\ \mathsf{inl}\, x \Rightarrow t \mid \mathsf{inr}\, y \Rightarrow t \\
&\mid * \mid \mathsf{absurd}\, t
\end{aligned}
$$

Informally:

* $\langle t_1,t_2\rangle$ – pair,
* $\mathsf{fst}\, t,\ \mathsf{snd}\, t$ – projections,
* $\mathsf{inl}\, t,\ \mathsf{inr}\, t$ – injections into sums,
* $\mathsf{case}$ – case analysis on sums,
* $*$ – the unique inhabitant of $1$,
* $\mathsf{absurd}\, t$ – elimination from $0$.

We always work **modulo $\alpha$-equivalence** (as fixed in Module 1).

### 9.1.3 Typing rules for data types

We extend the typing rules of Module 8.

Let $\Gamma$ be a context.

**Products.**

- **T-Pair** (premises: $\Gamma \vdash t_1 : A$, $\Gamma \vdash t_2 : B$): $\Gamma \vdash \langle t_1,t_2\rangle : A \times B$

- **T-Fst** (premise: $\Gamma \vdash t : A \times B$): $\Gamma \vdash \mathsf{fst}\, t : A$

- **T-Snd** (premise: $\Gamma \vdash t : A \times B$): $\Gamma \vdash \mathsf{snd}\, t : B$

**Sums.**

- **T-Inl** (premise: $\Gamma \vdash t : A$): $\Gamma \vdash \mathsf{inl}\, t : A + B$

- **T-Inr** (premise: $\Gamma \vdash t : B$): $\Gamma \vdash \mathsf{inr}\, t : A + B$

- **T-Case** (premises: $\Gamma \vdash t : A + B$, $\Gamma, x : A \vdash u : C$, $\Gamma, y : B \vdash v : C$): $\Gamma \vdash \mathsf{case}\ t\ \mathsf{of}\ \mathsf{inl}\, x \Rightarrow u \mid \mathsf{inr}\, y \Rightarrow v : C$

**Unit and empty.**

- **T-Unit**: $\Gamma \vdash * : 1$

- **T-Absurd** (premise: $\Gamma \vdash t : 0$): $\Gamma \vdash \mathsf{absurd}\, t : A$

The function rules T-Var, T-Abs, T-App remain as in Module 8.

### 9.1.4 Values and evaluation

We fix a standard **call-by-value** small-step semantics (one-step reduction $\to$) as in Module 6, specialized to this language.

**Definition 9.3 (Values).**

Values $v$ are:

* $\lambda x.t$ (abstractions),
* $\langle v_1,v_2\rangle$ where $v_1,v_2$ values,
* $\mathsf{inl}\, v$ and $\mathsf{inr}\, v$ where $v$ value,
* $*$.

We assume base constants (if any, e.g. `true`, `false`) are included as values with their usual types, but they do not affect the structure of the proofs. For simplicity in the metatheory below, we assume base types admit no eliminators (i.e., they are inert); canonical forms for base types are thus the base constants themselves.

**Definition 9.4 (Evaluation contexts).**

Evaluation contexts $E$ are defined by the following grammar (extending those from Module 6):

$$
\begin{aligned}
E ::= &\ [\cdot] \mid E\, t \mid v\, E \mid \mathsf{fst}\, E \mid \mathsf{snd}\, E \\
&\mid \mathsf{inl}\, E \mid \mathsf{inr}\, E \mid \mathsf{case}\, E\ \mathsf{of}\ \mathsf{inl}\, x \Rightarrow t \mid \mathsf{inr}\, y \Rightarrow t \\
&\mid \mathsf{absurd}\, E
\end{aligned}
$$

where $v$ ranges over values and $t$ over terms. A reduction step $t \to t'$ is obtained by selecting a redex $r \to r'$ and an evaluation context $E$ such that $t = E[r]$, yielding $t' = E[r']$. The semantics is deterministic.

Reduction rules include:

* $\beta$-reduction for application:
  $$
  (\lambda x.t)\, v \to t[v/x] \quad \text{if $v$ is a value},
  $$
* projections:
  $$
  \mathsf{fst}\, \langle v_1,v_2 \rangle \to v_1,\quad
  \mathsf{snd}\, \langle v_1,v_2 \rangle \to v_2,
  $$
* case on sums:
  $$
  \mathsf{case}\ (\mathsf{inl}\, v)\ \mathsf{of}\ \mathsf{inl}\, x \Rightarrow u
  \mid \mathsf{inr}\, y \Rightarrow w
  \to u[v/x],
  $$
  and similarly for $\mathsf{inr}$.

All rules are closed under the evaluation contexts defined above.

---

## 9.2 Canonical Forms

We now characterize the possible shapes of **closed values** at each type. These are used crucially in the **progress** proof.

We write $\emptyset \vdash v : A$ with $v$ a value.

### 9.2.1 Canonical forms for function types

**Lemma 9.1 (Canonical forms: functions).**
If $\emptyset \vdash v : A \to B$ and $v$ is a value, then $v = \lambda x.t$ for some $x,t$.

*Proof.* By inversion on the typing derivation.

Since $v$ is a value, the only possible syntactic forms are those in Def. 9.3. For $v$ to have type $A \to B$:

* It cannot be a pair, injection, or $*$, since T-Pair, T-Inl, T-Inr, T-Unit give types $A\times B$, $A+B$, and $1$ respectively.
* It cannot be a base constant, since base types are inert and do not match $A \to B$.

The only possibility is that the derivation ends with T-Abs, so $v = \lambda x.t$ and $\emptyset,x:A \vdash t : B$. ∎

### 9.2.2 Canonical forms for products

**Lemma 9.2 (Canonical forms: products).**
If $\emptyset \vdash v : A \times B$ and $v$ is a value, then $v = \langle v_1,v_2\rangle$ with $\emptyset \vdash v_1 : A$ and $\emptyset \vdash v_2 : B$ and $v_1,v_2$ values.

*Proof.* By inversion on the typing derivation of $\emptyset \vdash v : A \times B$.

The only rule with conclusion $A \times B$ is T-Pair; hence $v = \langle t_1,t_2\rangle$ and $\emptyset \vdash t_1 : A$, $\emptyset \vdash t_2 : B$.
Since $v$ is a value, by the definition of values, $t_1,t_2$ must themselves be values, call them $v_1,v_2$. ∎

### 9.2.3 Canonical forms for sums

**Lemma 9.3 (Canonical forms: sums).**
If $\emptyset \vdash v : A + B$ and $v$ is a value, then either

* $v = \mathsf{inl}\, v_1$ with $\emptyset \vdash v_1 : A$ and $v_1$ a value, or
* $v = \mathsf{inr}\, v_2$ with $\emptyset \vdash v_2 : B$ and $v_2$ a value.

*Proof.* Again by inversion.

The only rules with conclusion $A + B$ are T-Inl and T-Inr, so $v$ must be of the form $\mathsf{inl}\, t$ or $\mathsf{inr}\, t$. Since $v$ is a value, $t$ must be a value. Typing gives the respective premises. ∎

### 9.2.4 Canonical forms for unit and empty

**Lemma 9.4 (Canonical forms: unit).**
If $\emptyset \vdash v : 1$ and $v$ is a value, then $v = *$.

*Proof.* By inversion on the typing derivation: the only rule with conclusion type $1$ is T-Unit, whose subject is $*$. ∎

**Lemma 9.5 (Canonical forms: empty).**
There is **no** closed value $v$ such that $\emptyset \vdash v : 0$.

*Proof.* There is no introduction rule for $0$, so no derivation of $\emptyset \vdash v : 0$ exists at all, value or not. ∎

---

## 9.3 Progress

We now formally state and prove that **well-typed closed terms do not get stuck**.

Recall: a term is **stuck** if it is not a value and there is **no** $t'$ with $t \to t'$.

**Theorem 9.6 (Progress).**
If $\emptyset \vdash t : A$, then either

1. $t$ is a value, or
2. there exists $t'$ such that $t \to t'$.

*Proof.* By induction on the typing derivation of $\emptyset \vdash t : A$.

We consider the last rule used.

* **Case T-Var.** Impossible, since the context is empty.

* **Case T-Abs.** $t = \lambda x.t_1$. Then $t$ is a value by definition.

* **Case T-App.** $t = t_1\, t_2$ with
  $$
  \emptyset \vdash t_1 : B \to A,\quad \emptyset \vdash t_2 : B.
  $$
  By IH applied to $t_1$:

  * Either $t_1$ is a value, or
  * $t_1 \to t_1'$ for some $t_1'$.

  Similarly for $t_2$.

  *Subcase 1:* $t_1 \to t_1'$. Then by the evaluation context rule for applications,
  $$
  t_1\, t_2 \to t_1'\, t_2,
  $$
  so we are done.

  *Subcase 2:* $t_1$ is a value. By canonical forms (Lemma 9.1), $t_1 = \lambda x.u$.

  Now apply IH to $t_2$:

  * If $t_2 \to t_2'$, then $t_1\, t_2 \to t_1\, t_2'$ by the context rule for the argument.
  * If $t_2$ is a value $v$, then $(\lambda x.u)\, v$ is a $\beta$-redex and
    $$
    (\lambda x.u)\, v \to u[v/x].
    $$

* **Case T-Pair.** $t = \langle t_1,t_2 \rangle$ with $\emptyset \vdash t_1:A$ and $\emptyset \vdash t_2:B$.

  By IH on $t_1$:

  * If $t_1 \to t_1'$, then $\langle t_1,t_2 \rangle \to \langle t_1',t_2\rangle$.
  * If $t_1$ is a value, apply IH to $t_2$:

    * If $t_2 \to t_2'$, then $\langle t_1,t_2 \rangle \to \langle t_1,t_2'\rangle$.
    * If $t_2$ is also a value, then $\langle t_1,t_2 \rangle$ is a value.

* **Case T-Fst.** $t = \mathsf{fst}\, t_1$ with $\emptyset \vdash t_1 : A \times B$.

  By IH on $t_1$:

  * If $t_1 \to t_1'$, then $\mathsf{fst}\, t_1 \to \mathsf{fst}\, t_1'$.
  * If $t_1$ is a value, then by Lemma 9.2 $t_1 = \langle v_1,v_2\rangle$ and
    $$
    \mathsf{fst}\, \langle v_1,v_2\rangle \to v_1.
    $$

* **Case T-Snd.** Analogous to T-Fst using Lemma 9.2 and the rule for $\mathsf{snd}$.

* **Case T-Inl.** $t = \mathsf{inl}\, t_1$ with $\emptyset \vdash t_1 : A$.

  By IH on $t_1$:

  * If $t_1 \to t_1'$, then $\mathsf{inl}\, t_1 \to \mathsf{inl}\, t_1'$.
  * If $t_1$ is a value, then $\mathsf{inl}\, t_1$ is a value.

* **Case T-Inr.** Symmetric.

* **Case T-Case.**
  $t = \mathsf{case}\ t_0\ \mathsf{of}\ \mathsf{inl}\, x \Rightarrow u \mid \mathsf{inr}\, y \Rightarrow v$
  with
  $$
  \emptyset \vdash t_0 : A + B,\quad
  \emptyset,x:A \vdash u : C,\quad
  \emptyset,y:B \vdash v : C.
  $$

  By IH on $t_0$:

  * If $t_0 \to t_0'$, then
    $$
    \mathsf{case}\ t_0\ \dots \to \mathsf{case}\ t_0'\ \dots
    $$
    by the context rule.
  * If $t_0$ is a value, then by Lemma 9.3 either $t_0 = \mathsf{inl}\, v_1$ or $t_0 = \mathsf{inr}\, v_2$ with $v_i$ values. In the first case:
    $$
    \mathsf{case}\ (\mathsf{inl}\, v_1)\ \dots \to u[v_1/x],
    $$
    in the second:
    $$
    \mathsf{case}\ (\mathsf{inr}\, v_2)\ \dots \to v[v_2/y].
    $$

* **Case T-Unit.** $t = *$. No reduction possible; $t$ is a value.

* **Case T-Absurd.** $t = \mathsf{absurd}\, t_0$ with $\emptyset \vdash t_0 : 0$.

  Note that $\mathsf{absurd}\, t_0$ is not a value (by Def. 9.3). By the induction hypothesis applied to $\emptyset \vdash t_0 : 0$, either $t_0$ is a value or there exists $t_0'$ such that $t_0 \to t_0'$. But by Lemma 9.5, there are no closed values of type $0$, so the first possibility is impossible. Hence, there exists $t_0'$ such that $t_0 \to t_0'$. By the evaluation context rule for $\mathsf{absurd}\, E$ (Def. 9.4), it follows that $\mathsf{absurd}\, t_0 \to \mathsf{absurd}\, t_0'$.

All cases are covered. ∎

---

## 9.4 Preservation

We now prove that **types are invariant** under reduction.

**Theorem 9.7 (Preservation).**
If $\Gamma \vdash t : A$ and $t \to t'$, then $\Gamma \vdash t' : A$.

*Proof.* By induction on the typing derivation of $\Gamma \vdash t : A$, with a case analysis on the reduction step $t \to t'$.

We write out the non-trivial cases; steps in evaluation contexts follow by the induction hypothesis and reapplication of the same typing rule.

* **Case T-Var.** $t = x$. Variables do not reduce; contradiction with $t \to t'$.

* **Case T-Abs.** $t = \lambda x.t_1$ with $\Gamma, x : B \vdash t_1 : C$, $A = B \to C$.

  An abstraction reduces only by a step in its body:
  $$
  \lambda x.t_1 \to \lambda x.t_1' \quad\text{with } t_1 \to t_1'.
  $$
  By IH applied to $\Gamma, x : B \vdash t_1 : C$, we obtain $\Gamma, x : B \vdash t_1' : C$. Then T-Abs gives $\Gamma \vdash \lambda x.t_1' : B \to C = A$.

* **Case T-App.** $t = t_1\, t_2$ with
  $$
  \Gamma \vdash t_1 : B \to A,\quad \Gamma \vdash t_2 : B.
  $$

  Reduction $t \to t'$ can occur in three ways:

  1. **Left congruence:** $t_1 \to t_1'$, $t' = t_1'\, t_2$.

     By IH on $\Gamma \vdash t_1 : B \to A$, we get $\Gamma \vdash t_1' : B \to A$. T-App then gives $\Gamma \vdash t_1'\, t_2 : A$.

  2. **Right congruence:** $t_2 \to t_2'$, $t' = t_1\, t_2'$.

     By IH on $\Gamma \vdash t_2 : B$, we get $\Gamma \vdash t_2' : B$. T-App gives $\Gamma \vdash t_1\, t_2' : A$.

  3. **$\beta$-reduction:** $t_1 = \lambda x.u$, $t_2 = v$ value, and
     $$
     t' = u[v/x].
     $$
     From T-App and T-Abs, we know:
     $$
     \Gamma, x : B \vdash u : A,\quad \Gamma \vdash v : B.
     $$
     By the typed substitution lemma (Lemma 8.6), we get $\Gamma \vdash u[v/x] : A$.

* **Case T-Pair.** $t = \langle t_1,t_2\rangle$, $\Gamma \vdash t_1 : A$, $\Gamma \vdash t_2 : B$, $A_0 = A \times B$.

  Possible reductions:

  1. $t_1 \to t_1'$, $t' = \langle t_1',t_2\rangle$.

     IH: $\Gamma \vdash t_1' : A$. Then T-Pair: $\Gamma \vdash \langle t_1',t_2\rangle : A \times B$.

  2. $t_2 \to t_2'$, $t' = \langle t_1,t_2'\rangle$.

     Symmetric.

* **Case T-Fst.** $t = \mathsf{fst}\, t_0$, $\Gamma \vdash t_0 : A \times B$.

  Reductions:

  1. $t_0 \to t_0'$, $t' = \mathsf{fst}\, t_0'$.

     IH: $\Gamma \vdash t_0' : A \times B$, T-Fst then gives $\Gamma \vdash \mathsf{fst}\, t_0' : A$.

  2. $t_0 = \langle v_1,v_2\rangle$ values, $t' = v_1$.

     By inversion on T-Fst and T-Pair, $\Gamma \vdash v_1 : A$. Hence $\Gamma \vdash t' : A$.

* **Case T-Snd.** Analogous, using T-Snd.

* **Case T-Inl.** $t = \mathsf{inl}\, t_0$, $\Gamma \vdash t_0 : A$, $A_0 = A + B$.

  If $t_0 \to t_0'$, $t' = \mathsf{inl}\, t_0'$, IH gives $\Gamma \vdash t_0' : A$, then T-Inl gives $\Gamma \vdash t' : A_0$.

* **Case T-Inr.** Symmetric.

* **Case T-Case.**
  $t = \mathsf{case}\ t_0\ \mathsf{of}\ \mathsf{inl}\, x \Rightarrow u \mid \mathsf{inr}\, y \Rightarrow v$,
  with
  $$
  \Gamma \vdash t_0 : A + B,\quad
  \Gamma, x : A \vdash u : C,\quad
  \Gamma, y : B \vdash v : C,
  $$
  and $A_0 = C$.

  Reductions:

  1. $t_0 \to t_0'$, $t' = \mathsf{case}\ t_0'\ \dots$.

     IH: $\Gamma \vdash t_0' : A + B$, and the rest of the typing derivation can be reused; T-Case gives $\Gamma \vdash t' : C$.

  2. $t_0 = \mathsf{inl}\, w$ value, $t' = u[w/x]$.

     We know $\Gamma, x : A \vdash u : C$ and (from T-Inl) $\Gamma \vdash w : A$. By Lemma 8.6, $\Gamma \vdash u[w/x] : C$.

  3. $t_0 = \mathsf{inr}\, w$ value, $t' = v[w/y]$.

     Analogous using $\Gamma, y : B \vdash v : C$ and $\Gamma \vdash w : B$.

* **Case T-Unit.** $t = *$. No reduction possible; case impossible.

* **Case T-Absurd.** $t = \mathsf{absurd}\, t_0$, $\Gamma \vdash t_0 : 0$.

  There is no reduction rule for $\mathsf{absurd}$; any $t \to t'$ must come from a step $t_0 \to t_0'$, with $t' = \mathsf{absurd}\, t_0'$. But this is a congruence case:

  * IH: $\Gamma \vdash t_0' : 0$,
  * T-Absurd: $\Gamma \vdash \mathsf{absurd}\, t_0' : A$.

All cases are covered. ∎

---

## 9.5 Strong Normalization

We now address **strong normalization (SN)**.

### 9.5.1 Scope

We **fix** the fragment:

* Types generated from base types by $\to,\ \times,\ +,\ 1,\ 0$.
* Terms generated as in Def. 9.2.
* **No recursive types** (no $\mu$), no general fixpoint combinators, no additional constants with looping semantics.

We consider $\beta$-reduction plus the data-type reduction rules, i.e. the same $\to$ as in Sections 9.3–9.4.

**Definition 9.5 (Strong normalization).**

A term $t$ is **strongly normalizing** if there is **no infinite sequence**
$$
t = t_0 \to t_1 \to t_2 \to \dots
$$
of reductions. We write $\mathsf{SN}(t)$ for this property.

### 9.5.2 Reducibility candidates (logical relations)

We define, for each type $A$, a set $\mathsf{RED}_A$ of “good terms” (reducible terms) such that:

* All terms in $\mathsf{RED}_A$ are strongly normalizing,
* $\mathsf{RED}_A$ is closed under the **intended introduction and elimination** forms for $A$,
* Typed terms inhabit the appropriate $\mathsf{RED}_A$.

We work with **closed** terms here for simplicity; the full treatment extends to open terms via environments (deferred to an appendix).

**Definition 9.6 (Reducibility sets, closed version).**

We define $\mathsf{RED}_A \subseteq \{ t \mid \emptyset \vdash t : A\}$ by induction on $A$:

* **Base type $B$**:
  $$
  \mathsf{RED}_B := \{ t \mid \emptyset \vdash t : B \text{ and } \mathsf{SN}(t)\}.
  $$

* **Function type $A \to B$**:
  $$
  \mathsf{RED}_{A \to B} := \{ t \mid \emptyset \vdash t : A \to B \text{ and }
  \forall u \in \mathsf{RED}_A.\ t\, u \in \mathsf{RED}_B \}.
  $$

* **Product type $A \times B$**:
  $$
  \mathsf{RED}_{A \times B} := \left\{ t \mid
  \emptyset \vdash t : A \times B,\ \mathsf{SN}(t),
  \mathsf{fst}\, t \in \mathsf{RED}_A,\ \mathsf{snd}\, t \in \mathsf{RED}_B \right\}.
  $$

* **Sum type $A + B$**:
  $$
  \mathsf{RED}_{A + B} := \left\{ t \mid
  \emptyset \vdash t : A + B,\ \mathsf{SN}(t),\
  \forall C, \forall u,v.\
  \begin{array}{l}
  \emptyset,x:A \vdash u : C,\ \emptyset,y:B \vdash v : C \
  \Rightarrow \mathsf{case}\ t\ \mathsf{of}\ \mathsf{inl}\, x \Rightarrow u
  \mid \mathsf{inr}\, y \Rightarrow v \in \mathsf{RED}_C
  \end{array}
  \right\}.
  $$

* **Unit type $1$**:
  $$
  \mathsf{RED}_1 := \{ t \mid \emptyset \vdash t : 1 \text{ and } \mathsf{SN}(t)\}.
  $$

* **Empty type $0$**:
  $$
  \mathsf{RED}_0 := \{ t \mid \emptyset \vdash t : 0 \}.
  $$
  (This set is in fact empty, as there are no closed inhabitants of $0$.)

### 9.5.3 Basic properties

We need two central properties.

**Lemma 9.8 (Reducibility implies SN).**
For every type $A$ and closed $t$, if $t \in \mathsf{RED}_A$ then $\mathsf{SN}(t)$.

*Proof.* By induction on the structure of $A$.

* If $A$ is base $B$, $\mathsf{SN}(t)$ is part of the definition.
* For $A = A_1 \to A_2$, suppose for contradiction that $t \notin \mathsf{SN}(t)$. Then there is an infinite reduction sequence starting from $t$. By repeatedly applying suitable reducible arguments from $\mathsf{RED}_{A_1}$ (which are strongly normalizing by the induction hypothesis), one derives an infinite reduction at type $A_2$, contradicting the induction hypothesis on $A_2$. (Full details are standard and follow the classical Tait argument.)
* For $A \times B$ and $A + B$, $\mathsf{SN}(t)$ is part of the definition.
* For $1$, same.
* For $0$, all terms are vacuously SN because there are no closed terms of type $0$.

∎

The heart of the method is the **fundamental lemma**. The following is a proof sketch in the closed setting; a full proof requires extending the relation to open terms via environment interpretations.

**Theorem 9.9 (Fundamental Theorem of Logical Relations, closed version; sketch).**
If $\emptyset \vdash t : A$ then $t \in \mathsf{RED}_A$.

*Proof (sketch).* By induction on the typing derivation of $\emptyset \vdash t : A$.

* **Case T-Var.** Impossible for empty context.

* **Case T-Abs.** $t = \lambda x.u$, $A = B \to C$, with $x : B \vdash u : C$.

  We must show:

  1. $\emptyset \vdash \lambda x.u : B \to C$ (given), and
  2. for every $v \in \mathsf{RED}_B$, $(\lambda x.u)\, v \in \mathsf{RED}_C$.

  Let $v \in \mathsf{RED}_B$; then $\emptyset \vdash v : B$ and $\mathsf{SN}(v)$ by Lemma 9.8.
  By T-App, $\emptyset \vdash (\lambda x.u)\, v : C$. The reduction
  $$
  (\lambda x.u)\, v \to u[v/x]
  $$
  plus Lemma 9.7 (preservation) ensures $\emptyset \vdash u[v/x] : C$.

  To show $u[v/x] \in \mathsf{RED}_C$, one extends the logical relation to open terms (e.g., via a relational environment $\rho$ such that $\rho(x) \in \mathsf{RED}_B$ implies the body $u$ is reducible at $C$), applying the induction hypothesis to the open derivation $x : B \vdash u : C$. (Full details are standard; see, e.g., Girard 1987 or an appendix.)

* **Case T-App.** $t = t_1\, t_2$, $A = C$, $\emptyset \vdash t_1 : B \to C$, $\emptyset \vdash t_2 : B$.

  By IH, $t_1 \in \mathsf{RED}_{B \to C}$ and $t_2 \in \mathsf{RED}_B$. By the definition of $\mathsf{RED}_{B \to C}$, we get $t_1\, t_2 \in \mathsf{RED}_C$.

* **Cases for products, sums, unit, empty.** These follow the same pattern:

  * For introductions (T-Pair, T-Inl, T-Inr, T-Unit), one uses IH on components plus the definition of $\mathsf{RED}$ for those types.
  * For eliminations (T-Fst, T-Snd, T-Case, T-Absurd), one exploits closure properties baked into the definition of the corresponding $\mathsf{RED}_A$.

The important point is that each typing rule corresponds to a clause in the $\mathsf{RED}_A$ definitions, and the induction follows that structure. A fully detailed proof (including open terms) is standard and can be found in the literature (e.g., Girard 1987). ∎

### 9.5.4 Strong normalization theorem

We can now state the main result.

**Theorem 9.10 (Strong normalization for STLC with $\to, \times, +, 1, 0$).**
Let $A$ be a type built from base types using only $\to,\ \times,\ +,\ 1,\ 0$.
If $\emptyset \vdash t : A$, then $\mathsf{SN}(t)$.

*Proof.* By Theorem 9.9, $\emptyset \vdash t : A$ implies $t \in \mathsf{RED}_A$. By Lemma 9.8, $t \in \mathsf{RED}_A$ implies $\mathsf{SN}(t)$. ∎

This is the exact scope of the SN claim in this module.

### 9.5.5 Recursive types and general recursion (preview, outside SN)

We briefly indicate the limits of the above result.

* If we extend the type language with **recursive types** $\mu X. F(X)$ and corresponding `roll`/`unroll` term formers, or
* If we add a **fixed-point combinator** (e.g. $\mathsf{fix} : (A \to A) \to A$ with $\mathsf{fix}\, f \to f\, (\mathsf{fix}\, f)$),

then strong normalization **fails**: one can encode non-terminating computations (e.g. analogues of the untyped $\Omega$ combinator) at well-typed types.

Consequently:

> Theorem 9.10 **does not extend** to STLC with recursive types or general recursion.

These extensions require different semantic tools (e.g. domain theory) and are treated in later modules (e.g. Modules 11 and 15). Here we restrict ourselves strictly to the non-recursive fragment specified above.

---

## 9.6 Summary

In this module we:

* Extended the STLC of Module 8 with **products, sums, unit, and empty types**.
* Proved **canonical forms** for all type formers (Lemmas 9.1–9.5).
* Proved **progress** (Theorem 9.6): well-typed closed terms are either values or can step.
* Proved **preservation** (Theorem 9.7): types are invariant under reduction.
* Defined **reducibility candidates** for each type (Definition 9.6).
* Proved the **fundamental theorem of logical relations** (Theorem 9.9, as a sketch).
* Derived **strong normalization** (Theorem 9.10) for STLC with
  $\to,\ \times,\ +,\ 1,\ 0$, **excluding** recursive types and general recursion.

Together, progress and preservation establish **type safety** in the sense that a well-typed closed term never reduces to a stuck term (i.e., if evaluation terminates, the result is a value). Combined with strong normalization, this yields **total correctness**: evaluation always terminates in a value.

---

### Suggested Exercises

1. **Canonical forms for all type formers.**
   Generalize Lemmas 9.1–9.5 to include any base constants you have added (e.g. booleans, numerals) and prove the extended statement.

2. **Progress with sums.**
   Write out in full the progress proof case for T-Case, including the use of Lemma 9.3 and the $\beta$-rule for case.

3. **Preservation for products.**
   Give the full derivation for the preservation case
   $$
   \mathsf{fst}\, \langle v_1,v_2\rangle \to v_1,
   $$
   showing all typing premises and the use of inversion for T-Pair.

4. **Strong normalization for functions only.**
   Restrict the language to the arrow fragment (no $\times, +, 1, 0$) and write out a complete, fully detailed logical-relations proof for that fragment.

5. **Non-normalizing extension.**
   Define a typed fixed-point operator $\mathsf{fix} : (A \to A) \to A$, add an appropriate reduction rule, and show that there exists a well-typed term $t$ such that $\emptyset \vdash t : A$ and $t$ is **not** strongly normalizing.

6. **Curry–Howard correspondence.**
   For each of the data types ($\times, +, 1, 0$), state the corresponding logical connective and write down the typing rules as natural deduction rules for intuitionistic propositional logic.
