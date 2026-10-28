# Module 6 – Operational Semantics and Abstract Machines

In this module we refine the reduction theory of the $\lambda$-calculus (Module 3) into **operational semantics** suitable for reasoning about execution:

* **Small-step** semantics (one-step transitions),
* **Big-step** semantics (evaluation judgments),
* **Evaluation strategies** (call-by-name, call-by-value, weak vs strong),
* **Evaluation contexts**, **determinism**, and **stuck states**,
* **Abstract machines** (Krivine and CEK) and their correctness.

The goal is to connect the abstract, strategy-free $\beta$-reduction of Module 3 with concrete execution models that later support **type safety** (Module 9) and **implementation-oriented reasoning** (Module 7, explicit substitutions).

### Prerequisites and Dependencies

* **Required**: Modules 1–3 (syntax, substitution, $\beta/\eta$-reduction, multi-step, confluence).
* **Optional but helpful**:

  * Module 4 (head reduction, solvability) for understanding call-by-name vs head-normal forms.
  * Module 5 (Church encodings) for realistic examples (booleans, numerals, recursion).

Throughout we work modulo $\alpha$-equivalence and use the notation:

* $t \to t'$ for one-step reduction,
* $t \to^* t'$ for its reflexive-transitive closure,
* $t \equiv_{\beta\eta} u$ for $\beta\eta$-equivalence (Module 3).

---

## Core 6.1 – Small-Step Semantics via Evaluation Contexts

We first fix the syntax and a generic notion of **small-step semantics** based on **evaluation contexts**. Strategies (call-by-name, call-by-value, weak vs strong) will appear as *particular* choices of contexts in Core 6.3.

### 6.1.1 Syntax and values

We restrict attention to the standard untyped $\lambda$-calculus.

#### Definition 6.1 (Terms and values)

The set of $\lambda$-terms is given by:
$$
t ::= x \mid \lambda x.t \mid t\, t.
$$

For most of this module, we treat **values** as $\lambda$-abstractions:
$$
v ::= \lambda x.t.
$$

(Variables will be considered non-values in the operational semantics; they appear only in intermediate states or stuck terms.)

### 6.1.2 Primitive reduction

We fix the **primitive $\beta$-reduction** (and optionally $\eta$, though we mostly ignore $\eta$ in this module):

#### Definition 6.2 (Primitive $\beta$-reduction)

A **$\beta$-redex** is a term of the form $(\lambda x.t)\, s$. Primitive $\beta$-reduction is:
$$
(\lambda x.t)\, s \to_\beta t[s/x],
$$
where $t[s/x]$ is capture-avoiding substitution as defined in Module 2.

We will typically write $\to$ for a strategy-specific step relation built from $\beta$ and evaluation contexts. $\eta$-reduction is omitted from the main development (Module 3 covers $\beta\eta$-equivalence).

### 6.1.3 Evaluation contexts and small-step semantics

Evaluation contexts specify *where* reduction may occur.

#### Definition 6.3 (Evaluation contexts, informal)

An **evaluation context** is a term with a single distinguished hole $[\cdot]$ indicating the unique position where reduction may occur. For now we write $E$ for a context and $E[t]$ for the term obtained by replacing $[\cdot]$ with $t$.

Different **strategies** correspond to different grammars for $E$ (Core 6.3). For example:

* Weak call-by-name uses:
  $$
  E ::= [\cdot] \mid E\, t,
  $$
* Weak call-by-value uses:
  $$
  E ::= [\cdot] \mid E\, t \mid v\, E.
  $$

We keep the definition parametric in a strategy $S$.

#### Definition 6.4 (Small-step semantics via contexts)

Fix a strategy $S$ with its evaluation contexts $E_S$. The small-step relation $\to_S$ is the least relation such that:

$$
(\lambda x.t)\, s \to_S t[s/x]
\quad\text{($\beta$-step at the hole)}
$$
and
$$
\frac{t \to_S t'}{E_S[t] \to_S E_S[t']} \quad\text{(contextual closure)}.
$$

In words: a step under $S$ is a $\beta$-step at the designated redex position prescribed by $E_S$.

We write $\to_S^*$ for the reflexive-transitive closure.

---

## Core 6.2 – Unique Decomposition and Determinism

For a strategy defined by evaluation contexts, we want:

1. Each term to have a **unique decomposition** into context + redex (or be a value),
2. Hence the step relation $\to_S$ to be **deterministic**.

We prove this for two main strategies: **weak call-by-name** and **weak call-by-value** (their strong variants are analogous but slightly more involved).

### 6.2.1 Weak call-by-name and weak call-by-value

We now **fix** the two main strategies used later.

#### Definition 6.5 (Weak call-by-name and call-by-value)

1. **Weak call-by-name** (CBN):

   * Values: $v ::= \lambda x.t$.
   * Contexts:
     $$
     E_{\mathrm{cbn}} ::= [\cdot] \mid E_{\mathrm{cbn}}\, t.
     $$
   * Redexes:
     $$
     r ::= (\lambda x.t)\, s \quad\text{(no constraint on } s\text{)}.
     $$

2. **Weak call-by-value** (CBV):

   * Values: $v ::= \lambda x.t$.
   * Contexts:
     $$
     E_{\mathrm{cbv}} ::= [\cdot] \mid E_{\mathrm{cbv}}\, t \mid v\, E_{\mathrm{cbv}}.
     $$
   * Redexes:
     $$
     r ::= (\lambda x.t)\, v \quad\text{(right side must be a value)}.
     $$

The **small-step relations** $\to_{\mathrm{cbn}}$ and $\to_{\mathrm{cbv}}$ are defined from these contexts and $\beta$-steps as in Def. 6.4.

### 6.2.2 Unique decomposition

We first state the key structural lemma.

#### Theorem 6.1 (Unique decomposition)

Fix $S \in \{\text{weak CBN}, \text{weak CBV}\}$. For every term $t$ that is not a value and contains an $S$-redex, there exist a **unique** evaluation context $E_S$ and a **unique** redex $r$ such that
$$
t = E_S[r].
$$

*Proof.*

We treat weak CBV; weak CBN is similar (and slightly simpler).

**Existence** is by structural induction on $t$.

* If $t$ is a value $\lambda x.u$: excluded by hypothesis.
* If $t$ is a variable: it contains no $\beta$-redex; excluded by hypothesis.
* If $t = s_1\, s_2$:

  * If $s_1$ is not a value, by IH either $s_1$ is a redex in some context $E_s$, so we can write $s_1 = E_s[r]$ and thus
    $$
    t = s_1\, s_2 = E_s[r]\, s_2 = E_{\mathrm{cbv}}[r],
    $$
    where $E_{\mathrm{cbv}} ::= E_s\, s_2$.
  * If $s_1$ *is* a value and $s_2$ is not a value, IH on $s_2$ gives $s_2 = E_s[r]$ and
    $$
    t = s_1\, s_2 = s_1\, (E_s[r]) = E_{\mathrm{cbv}}[r],
    $$
    where $E_{\mathrm{cbv}} ::= s_1\, E_s$.
  * If $s_1$ is a value and $s_2$ is a value:

    * If $s_1 = \lambda x.u$, then $t$ itself is a redex: take $E_{\mathrm{cbv}} = [\cdot]$, $r = t$.
    * If $s_1$ is a non-$\lambda$ value (this cannot happen under our notion of values), we would be stuck.

Thus every non-value term containing a redex is decomposable as $E_{\mathrm{cbv}}[r]$.

**Uniqueness** of $E_S$ and $r$ follows from a straightforward structural induction and the **shape constraints** on the grammars of $E_{\mathrm{cbn}},E_{\mathrm{cbv}}$:

* In weak CBN, the hole is always the **left-most** position reachable by iterating the rule $E::=E\, t$.
* In weak CBV, the hole is always the **left-most** position, and any right-hand context must be under a value.

Precisely: assume $t = E_1[r_1] = E_2[r_2]$ with $E_1,E_2$ evaluation contexts and $r_1,r_2$ redexes. Induction on the structure of $t$ shows that the contexts must agree on the top constructor: if $t = u\, v$, then both $E_1,E_2$ must be either of the form $E\, v$ or $u\, E$. The grammar ensures that there is only one legal place to put the hole given whether $u$ is a value or not (CBV) or given leftmost priority (CBN). Thus $E_1 = E_2$ and $r_1 = r_2$. ∎

### 6.2.3 Determinism

With unique decomposition, determinism is immediate.

#### Theorem 6.2 (Determinism of weak CBN and weak CBV)

For $S \in \{\text{weak CBN}, \text{weak CBV}\}$, if $t \to_S u$ and $t \to_S v$, then $u = v$.

*Proof.*

By Def. 6.4, any step $t \to_S u$ arises from a decomposition $t = E_S[r]$, a $\beta$-step $r \to_\beta r'$, and $u = E_S[r']$. By Theorem 6.1 (applied to $t$, which contains an $S$-redex), $E_S$ and $r$ are unique; the primitive $\beta$-step at $r$ is also deterministic. Thus the resulting $u$ is unique. ∎

Determinism is crucial for later: when we prove **progress + preservation** in STLC (Module 9), determinism ensures that evaluation is a total function on well-typed closed terms (modulo divergence).

---

## Core 6.3 – Big-Step (Natural) Semantics and Equivalence with Small-Step

Small-step semantics exposes every intermediate step; big-step semantics **directly** relates a term to its value. Here we define big-step only for **weak call-by-value** and prove equivalence with $\to_{\mathrm{cbv}}$ on terminating computations.

### 6.3.1 Big-step CBV semantics

#### Definition 6.6 (Big-step evaluation, CBV)

We write $t \Downarrow_{\mathrm{cbv}} v$ to mean that $t$ evaluates to value $v$ under weak call-by-value, and define it inductively:

1. **(B-Abs)**
   $$
   \lambda x.t \Downarrow_{\mathrm{cbv}} \lambda x.t
   $$

2. **(B-App)**
   $$
   \frac{
   t_1 \Downarrow_{\mathrm{cbv}} \lambda x.t_{12}
   \quad
   t_2 \Downarrow_{\mathrm{cbv}} v_2
   \quad
   t_{12}[v_2/x] \Downarrow_{\mathrm{cbv}} v
   }{
   t_1\, t_2 \Downarrow_{\mathrm{cbv}} v
   }.
   $$

There is no rule for variables; an unbound variable has **no** big-step derivation (it is stuck).

### 6.3.2 Soundness and completeness wrt small-step CBV

We now relate big-step to small-step.

#### Theorem 6.3 (Soundness of big-step CBV)

If $t \Downarrow_{\mathrm{cbv}} v$, then $t \to_{\mathrm{cbv}}^* v$ and $v$ is a value.

*Proof.*

By induction on the derivation of $t \Downarrow_{\mathrm{cbv}} v$.

* Case (B-Abs): $t = \lambda x.u$, $v = \lambda x.u$. Then $t \to_{\mathrm{cbv}}^* v$ by 0 steps; $v$ is a value by Def. 6.1.

* Case (B-App): premise:
  $$
  t_1 \Downarrow_{\mathrm{cbv}} \lambda x.t_{12},\quad
  t_2 \Downarrow_{\mathrm{cbv}} v_2,\quad
  t_{12}[v_2/x] \Downarrow_{\mathrm{cbv}} v.
  $$
  By IH:
  $$
  t_1 \to_{\mathrm{cbv}}^* \lambda x.t_{12},\quad
  t_2 \to_{\mathrm{cbv}}^* v_2,\quad
  t_{12}[v_2/x] \to_{\mathrm{cbv}}^* v,
  $$
  with $v_2,v$ values.

  Using Def. 6.5, $t_1\, t_2$ reduces in CBV as:
  $$
  t_1\, t_2 \to_{\mathrm{cbv}}^* (\lambda x.t_{12})\, t_2
  \to_{\mathrm{cbv}}^* (\lambda x.t_{12})\, v_2
  \to_{\mathrm{cbv}} t_{12}[v_2/x]
  \to_{\mathrm{cbv}}^* v.
  $$
  Concatenating these finite sequences yields $t \to_{\mathrm{cbv}}^* v$ with $v$ a value. ∎

#### Theorem 6.4 (Completeness of big-step CBV)

If $t \to_{\mathrm{cbv}}^* v$ and $v$ is a value, then $t \Downarrow_{\mathrm{cbv}} v$.

*Proof.*

By structural induction on $t$, using Theorem 6.2 (determinism) to ensure uniqueness of normal forms.

* Case $t = \lambda x.u$: The sequence must be empty ($t \to_{\mathrm{cbv}}^* v$ implies $v = t$), so (B-Abs) gives $t \Downarrow_{\mathrm{cbv}} v$.

* Case $t = t_1\, t_2$: By the CBV evaluation order (Theorem 6.1), the sequence segments as
  $$
  t_1\, t_2 \to_{\mathrm{cbv}}^* (\lambda x.t_{12})\, t_2 \to_{\mathrm{cbv}}^* (\lambda x.t_{12})\, v_2 \to_{\mathrm{cbv}} t_{12}[v_2/x] \to_{\mathrm{cbv}}^* v,
  $$
  where $v_2$ is a value. By IH on the sub-sequences, $t_1 \Downarrow_{\mathrm{cbv}} \lambda x.t_{12}$, $t_2 \Downarrow_{\mathrm{cbv}} v_2$, and $t_{12}[v_2/x] \Downarrow_{\mathrm{cbv}} v$. Thus (B-App) gives $t \Downarrow_{\mathrm{cbv}} v$.

Variables are excluded, as they have no reduction sequence to a value. ∎

Result: for terminating computations, **small-step CBV and big-step CBV coincide** on values. Big-step, however, says nothing about divergent or stuck terms (they simply have no derivation).

---

## Core 6.4 – Evaluation Strategies, Weak vs Strong, and Stuck States

We now systematically present the main evaluation strategies and isolate the notion of a **stuck state** in the untyped calculus. This is the interface to the type-safety results of Module 9.

### 6.4.1 Strategy summary

We consider:

* Call-by-name (CBN),
* Call-by-value (CBV),
* Weak vs strong variants (whether or not we reduce under $\lambda$).

#### Definition 6.7 (Strategy-specific values and contexts)

1. **Weak call-by-name (CBN)**:

   * Values: $v ::= \lambda x.t$.
   * Contexts:
     $$
     E^{w}_{\mathrm{cbn}} ::= [\cdot] \mid E^{w}_{\mathrm{cbn}}\, t.
     $$
   * Redexes: $(\lambda x.t)\, s$ (no restriction on $s$).
   * No reduction under $\lambda$: the body of a $\lambda$-abstraction is never reduced.

2. **Strong call-by-name**:

   * Same redexes and values.
   * Contexts:
     $$
     E^{s}_{\mathrm{cbn}} ::= [\cdot] \mid E^{s}_{\mathrm{cbn}}\, t \mid \lambda x.E^{s}_{\mathrm{cbn}}.
     $$
   * Reduces under $\lambda$ as well.

3. **Weak call-by-value (CBV)** (Def. 6.5).

4. **Strong call-by-value**:

   * Values: $v ::= \lambda x.t$.
   * Contexts:
     $$
     E^{s}_{\mathrm{cbv}} ::= [\cdot] \mid E^{s}_{\mathrm{cbv}}\, t \mid v\, E^{s}_{\mathrm{cbv}} \mid \lambda x.E^{s}_{\mathrm{cbv}}.
     $$
   * Reduces under $\lambda$, but $\beta$-steps only when the argument is a value.

A simple comparison:

| Strategy     | Contexts (weak)                              | Redex form        | Reduces under $\lambda$? | Typical language          |
| ------------ | -------------------------------------------- | ----------------- | ------------------------ | ------------------------- |
| CBN (weak)   | $[\cdot] \mid E\, t$                         | $(\lambda x.t)\, s$ | No                       | Haskell-style core        |
| CBN (strong) | $[\cdot] \mid E\, t \mid \lambda x.E$        | $(\lambda x.t)\, s$ | Yes                      | Normalization proofs      |
| CBV (weak)   | $[\cdot] \mid E\, t \mid v\, E$              | $(\lambda x.t)\, v$ | No                       | ML, OCaml, Scheme         |
| CBV (strong) | $[\cdot] \mid E\, t \mid v\, E \mid \lambda x.E$ | $(\lambda x.t)\, v$ | Yes                      | Full normalization (rare) |

We will mostly use **weak** variants: strong strategies are useful for normalization arguments but less realistic operationally.

### 6.4.2 Stuck states and untyped progress

In the untyped calculus, **stuck** terms are unavoidable: nothing prevents us from forming nonsense like $x\, (\lambda y.y)$ with $x$ free.

#### Definition 6.8 (Stuck terms under $S$)

Fix a strategy $S$. A term $t$ is **stuck** under $S$ if:

* $t$ is not a value, and
* there is **no** $u$ such that $t \to_S u$.

Equivalently, $t$ is neither a value nor of the form $E_S[r]$ with $r$ a redex.

Examples under weak CBV:

* $x$ is stuck (not a value, no redex).
* $x\, (\lambda y.y)$ is stuck (function is not a value, but has no redex; CBV never steps into argument first when function is not a value).

#### Theorem 6.5 (Untyped “progress decomposition” under $S$)

Let $S$ be any of the four strategies above. For every **closed** term $t$ (no free variables), exactly one of the following holds:

1. $t$ is a value, or
2. there exists $u$ such that $t \to_S u$, or
3. $t$ is stuck.

*Proof.*

By structural induction on $t$. The cases are mechanical:

* $t = \lambda x.u$: value.
* $t = x$: cannot happen if $t$ is closed (no free variables).
* $t = t_1\, t_2$:

  * If $t_1$ is a value and (in CBV) $t_2$ is a value and $t_1 = \lambda x.u$, then $t$ is a redex and hence takes a step.
  * Else if $t_1$ is not a value and has a redex (by IH), then $t$ has a decomposition $E[r]$ and steps.
  * Else, if $t_1$ is a value and $t_2$ is not a value and strategy permits stepping in the argument (CBV, not CBN), then $t$ steps.
  * Otherwise no context applies and $t$ is not a value; hence $t$ is stuck.

Exhaustiveness follows from Theorem 6.1; in each case we either find a step or conclude non-value and non-step. ∎

In the pure $\lambda$-calculus, closed terms are never stuck; case (3) only arises once we enrich the language with constants or partial primitives. We keep the definition general because we will need it in typed and extended settings.

In **typed** settings (Module 9), we will show that *well-typed closed terms are never stuck*: they either are values or can reduce. That is the usual **progress** theorem.

---

## Core 6.5 – Abstract Machines: Krivine (CBN) and CEK (CBV)

Small-step semantics is still expressed in terms of **substitution on syntactic trees**. Realistic implementations use **environments**, **closures**, and **stacks/continuations**. Abstract machines formalize this, while remaining mathematically precise.

We present two classical machines:

* the **Krivine machine** for weak call-by-name, and
* the **CEK machine** for weak call-by-value.

For each, we state a correctness theorem relating machine executions to the corresponding small-step semantics.

### 6.5.1 The Krivine machine (weak call-by-name)

The Krivine machine evaluates a term under weak CBN by manipulating:

* a **control** term,
* an **environment** mapping variables to closures,
* a **stack** of argument closures.

#### Definition 6.9 (Closures and Krivine states)

A **closure** is a pair $(t,\rho)$ of a term $t$ and an environment $\rho$ (finite mapping from variables to closures).

A **Krivine state** is a triple
$$
\langle t, \rho, \pi \rangle,
$$
where:

* $t$ is a term (the current control),
* $\rho$ is an environment,
* $\pi$ is a stack: a finite list of closures.

The initial state for a closed term $t$ is $\langle t, \emptyset, \epsilon \rangle$, where $\epsilon$ is the empty stack.

#### Definition 6.10 (Krivine transition relation)

The Krivine machine for **weak CBN** has the following transitions:

1. **Application (push argument)**
   $$
   \langle t_1\, t_2, \rho, \pi \rangle
   \to_K
   \langle t_1, \rho, (t_2,\rho) :: \pi \rangle.
   $$

2. **Abstraction (pop argument)**
   $$
   \langle \lambda x.t, \rho, (u,\rho') :: \pi \rangle
   \to_K
   \langle t, \rho[x \mapsto (u,\rho')], \pi \rangle.
   $$

3. **Variable lookup**
   If $\rho(x) = (u,\rho')$, then
   $$
   \langle x, \rho, \pi \rangle
   \to_K
   \langle u, \rho', \pi \rangle.
   $$

A state of the form $\langle \lambda x.t, \rho, \epsilon \rangle$ (abstraction and empty stack) is **final**; we read its result as the closure $(\lambda x.t, \rho)$, which corresponds to the $\lambda$-value $\lambda x.t$ in the original semantics (the environment is irrelevant for a closed result).

This machine never reduces under $\lambda$: it is a **weak** call-by-name evaluator.

### 6.5.2 Correctness of the Krivine machine

We relate Krivine runs to weak CBN small-step reduction on closed terms.

#### Theorem 6.6 (Krivine soundness)

If
$$
\langle t, \emptyset, \epsilon \rangle \to_K^* \langle \lambda x.u, \rho, \epsilon \rangle
$$
for a **closed** term $t$, then
$$
t \to_{\mathrm{cbn}}^* \lambda x.u.
$$

*Proof sketch.*

Each Krivine step corresponds to either:

* a CBN **context step** (application rule pushes arguments left-associatively), or
* a single **$\beta$-step** (abstraction rule), or
* a **variable dereference** (which, for closed $t$, corresponds to inlining a substitution already represented by the environment).

By induction on the length of the machine run, we show that:

* the control term in the state is always of the form $E_{\mathrm{cbn}}[t']$ for some $t'$,
* a Krivine step either leaves the small-step term unchanged or performs one $\beta$-step at the leftmost-outermost redex.

Thus the final abstraction reached by the machine is reachable via $\to_{\mathrm{cbn}}^*$ from the initial term. ∎

#### Theorem 6.7 (Krivine completeness)

Conversely, if $t$ is closed and $t \to_{\mathrm{cbn}}^* v$ with $v$ a value, then there exists an environment $\rho$ and stack $\pi$ such that
$$
\langle t, \emptyset, \epsilon \rangle \to_K^* \langle v, \rho, \epsilon \rangle.
$$

*Proof sketch.*

Induction on the length of the CBN reduction sequence. The crucial lemma is that each CBN $\beta$-step
$$
E_{\mathrm{cbn}}[(\lambda x.t_1)\, s] \to_{\mathrm{cbn}} E_{\mathrm{cbn}}[t_1[s/x]]
$$
is simulated by a finite number of Krivine steps that:

* push $s$ as a closure onto the stack,
* enter the body $t_1$ with an environment updated with $x \mapsto (s,\rho)$.

By composing these simulations along the reduction sequence, we obtain a full machine run from $t$ to $v$. ∎

Together, Theorems 6.6–6.7 say: **on closed terms, the Krivine machine implements weak CBN exactly** (up to environments, which are implementation detail).

---

### 6.5.3 The CEK machine (weak call-by-value)

The CEK machine evaluates terms under weak CBV using:

* **C**ontrol (a term),
* **E**nvironment (variable bindings),
* **K**ontinuation (stack of frames).

#### Definition 6.11 (CEK states, environments, continuations)

* A **value** in the CEK machine is still a $\lambda$-abstraction $\lambda x.t$.
* An **environment** $\rho$ maps variables to values. For closed programs we can maintain the invariant that all bound variables map to closed values, so we do not distinguish values from closures here.
* A **continuation** is a stack built from frames:
  $$
  \kappa ::= \bullet \mid \mathbf{ARG}(t,\rho,\kappa) \mid \mathbf{FUN}(v,\kappa),
  $$
  where:

  * $\bullet$ is the empty continuation,
  * $\mathbf{ARG}(t,\rho,\kappa)$ records that we still need to evaluate argument $t$ under environment $\rho$ then continue with $\kappa$,
  * $\mathbf{FUN}(v,\kappa)$ records that we have evaluated the function to value $v$ and must apply it to the already evaluated argument.

A **CEK state** is a triple $\langle c, \rho, \kappa \rangle$.

The initial state for a closed term $t$ is $\langle t, \emptyset, \bullet \rangle$.

#### Definition 6.12 (CEK transition relation, weak CBV)

The CEK machine for weak CBV has the following transitions:

1. **Application (start)**
   $$
   \langle t_1\, t_2, \rho, \kappa \rangle
   \to_{\mathrm{CEK}}
   \langle t_1, \rho, \mathbf{ARG}(t_2,\rho,\kappa) \rangle.
   $$

2. **Function evaluated**
   $$
   \langle v_1, \rho, \mathbf{ARG}(t_2,\rho',\kappa) \rangle
   \to_{\mathrm{CEK}}
   \langle t_2, \rho', \mathbf{FUN}(v_1,\kappa) \rangle,
   $$
   where $v_1$ is a value.

3. **Argument evaluated and function is $\lambda$**
   $$
   \langle v_2, \rho, \mathbf{FUN}(\lambda x.t_0,\kappa) \rangle
   \to_{\mathrm{CEK}}
   \langle t_0, \rho[x \mapsto v_2], \kappa \rangle.
   $$

4. **Variable lookup**
   If $\rho(x) = v$, then
   $$
   \langle x, \rho, \kappa \rangle
   \to_{\mathrm{CEK}}
   \langle v, \rho, \kappa \rangle.
   $$

A state of the form $\langle v, \rho, \bullet \rangle$ with $v$ a value is **final**; we read the result as $v$ (for closed programs, the environment on exit is irrelevant).

This machine never reduces under $\lambda$ (weak CBV).

### 6.5.4 Correctness of the CEK machine

We relate the CEK machine to weak CBV small-step and to the big-step semantics of Core 6.3.

Let $t \Downarrow_{\mathrm{cbv}} v$ be as in Def. 6.6.

#### Theorem 6.8 (CEK soundness: from machine to small-step CBV)

If
$$
\langle t, \emptyset, \bullet \rangle \to_{\mathrm{CEK}}^* \langle v, \rho, \bullet \rangle
$$
for a closed $t$ and some value $v$, then
$$
t \to_{\mathrm{cbv}}^* v.
$$

*Proof idea.*

Proof by induction on the length of the CEK run. Each machine step corresponds either to:

* a decomposition of $t$ into a CBV context plus a redex (steps (1) and (2)), or
* a $\beta$-step at a redex $(\lambda x.t_0)\, v_2$ (step (3)), or
* a value-preserving environment lookup (step (4)), which is observationally inert with respect to the source language (it simulates the application of a substitution).

One shows that:

* the control component of the state always matches the current CBV small-step term,
* every step (or bounded cluster of steps) in the machine corresponds to 0 or 1 CBV small-steps.

Thus the final value reached by the machine is reachable by $\to_{\mathrm{cbv}}^*$ from $t$. ∎

#### Theorem 6.9 (CEK completeness: from small-step / big-step CBV to machine)

If $t$ is closed and $t \Downarrow_{\mathrm{cbv}} v$, then
$$
\langle t, \emptyset, \bullet \rangle \to_{\mathrm{CEK}}^* \langle v, \rho, \bullet \rangle
$$
for some environment $\rho$.

*Proof idea.*

We use Theorem 6.4 (big-step $\Leftrightarrow$ small-step) and then prove, by induction on the big-step derivation $t \Downarrow_{\mathrm{cbv}} v$, that each big-step rule is simulated by a finite CEK run:

* For $t = \lambda x.u$, the machine performs zero or more harmless lookup steps and halts with $v = \lambda x.u$.
* For $t = t_1\, t_2$, the (B-App) rule decomposes evaluation into:

  * evaluating $t_1$ to $\lambda x.t_{12}$,
  * evaluating $t_2$ to a value $v_2$,
  * evaluating $t_{12}[v_2/x]$ to $v$.

  The CEK transitions mirror this exactly: (1) moves into $t_1$ with a pending $\mathbf{ARG}$ frame, (2) moves into $t_2$ with a pending $\mathbf{FUN}$ frame, (3) performs the $\beta$-step by switching control to $t_{12}$ with $x$ bound to $v_2$.

Induction on the structure of the big-step derivation yields a complete machine run. ∎

Thus, **on closed, terminating programs**, the CEK machine, small-step CBV, and big-step CBV all agree.

---

## Summary and Exercises

In this module we:

* Defined **small-step semantics** via evaluation contexts (Defs. 6.3–6.5) and proved **unique decomposition** and **determinism** for weak CBN/CBV (Thms. 6.1–6.2).
* Introduced **big-step CBV semantics** (Def. 6.6) and proved **soundness and completeness** with respect to small-step CBV (Thms. 6.3–6.4).
* Systematically distinguished **evaluation strategies** (weak/strong CBN/CBV) via their contexts and redex conditions (Def. 6.7).
* Defined **stuck states** and gave an untyped “progress decomposition” for closed terms (Thm. 6.5), which will be refined into full **progress** once types are added (Module 9).
* Presented the **Krivine machine** for weak call-by-name (Defs. 6.9–6.10) and proved its correctness (Thms. 6.6–6.7).
* Presented the **CEK machine** for weak call-by-value (Defs. 6.11–6.12) and proved its correctness (Thms. 6.8–6.9).

This sets the stage for:

* **Explicit substitutions** (Module 7), which internalize environments at the term level.
* **Typing and type safety** (Modules 8–9), where we prove that well-typed programs do not get stuck under these operational semantics.

---

### Suggested Exercises

1. **Decomposition under CBV**

   For each of the following terms, give the unique CBV context $E_{\mathrm{cbv}}$ and redex $r$ such that $t = E_{\mathrm{cbv}}[r]$, or explain why $t$ is a value or stuck:

   1. $(\lambda x.x)\, ((\lambda y.y)\, z)$
   2. $(\lambda x.y)\, \Omega$
   3. $x\, (\lambda y.y)$ (with $x$ free).

2. **Small-step vs big-step CBV**

   Show directly (by constructing derivations) that
   $$
   (\lambda x.x)\, ((\lambda y.y)\, z) \Downarrow_{\mathrm{cbv}} z
   $$
   and verify that this matches the small-step CBV evaluation sequence.

3. **Strategy comparison**

   For each term below, describe the behavior under weak CBN and weak CBV:

   1. $(\lambda x.y)\, \Omega$,
   2. $(\lambda x.x)\, \Omega$.

   Does evaluation terminate? If so, to what value?

4. **Krivine trace**

   Give a complete Krivine machine trace for the closed term
   $$
   t = (\lambda x.x)\, (\lambda y.y).
   $$
   Show how each step corresponds to a CBN small-step.

5. **CEK trace**

   Give a complete CEK machine trace for the same term $t$ under weak CBV. Check that the final value matches both the small-step and big-step CBV semantics.

6. **Strong strategies**

   Extend the definition of evaluation contexts to **strong CBV** (Def. 6.7). Prove a version of Theorem 6.1 (unique decomposition) for strong CBV and explain why strong CBV is rarely used as an implementation strategy in practical languages.
