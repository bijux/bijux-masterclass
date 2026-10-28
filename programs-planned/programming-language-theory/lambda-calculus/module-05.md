# Module 5 – The $\lambda$-Calculus as a Programming Language

In this module, we treat the untyped $\lambda$-calculus as a **programming language**: we demonstrate how to encode data and programs *inside* the calculus using only $\lambda$-abstraction and application.

We cover:

* Church encodings of **booleans** and **pairs**,
* Church encodings of **natural numbers** and basic **arithmetic**,
* **Fixed-point combinators** and recursive definitions,
* Simple **higher-order programs** (factorial, lists, map/fold),
* The relation to **combinatory logic** (SKI), which eliminates variables.

All correctness claims are stated and proved as explicit lemmas/theorems in terms of **$\beta\eta$-equivalence** and **reduction** from Modules 1–3. A dedicated subsection (Core 5.3) isolates the informal discussion of **evaluation strategies** (call-by-name vs call-by-value); formal strategy definitions and machine models are postponed to Module 6.

### Prerequisites and Dependencies

* **Required**: Modules 1–3 (syntax, substitution, $\beta/\eta$-reduction, normal forms, confluence).
* **Optional but helpful**: Module 4 (solvability and Böhm trees) when reasoning about divergence of recursive definitions.
* No typed systems are needed here; typed refinements appear in Modules 8–12.

Throughout, we work **modulo $\alpha$-equivalence** and use the symmetric, transitive closure of $\beta\eta$-reduction, written $\equiv_{\beta\eta}$.

---

## Core 5.1 – Church Encodings of Booleans and Pairs

We first encode simple finite data types: **booleans** and **pairs**. The characteristic pattern is:

> Values are $\lambda$-terms that expect *eliminators* (what to do in each case) and apply one of them.

### 5.1.1 Church booleans and conditionals

#### Definition 5.1 (Church booleans and conditional)

Define:

* $\mathsf{true} \triangleq \lambda t.\lambda f.\, t$,
* $\mathsf{false} \triangleq \lambda t.\lambda f.\, f$,

and the **conditional** operator
$$
\mathsf{if} \triangleq \lambda b.\lambda u.\lambda v.\, b\, u\, v.
$$

Intended semantics: $\mathsf{true}$ chooses the first branch, $\mathsf{false}$ chooses the second, and $\mathsf{if}\, b\, u\, v$ behaves like “if $b$ then $u$ else $v$”. Formally, we regard two terms as representing the same boolean if they are $\beta\eta$-equivalent to either $\mathsf{true}$ or $\mathsf{false}$.

#### Lemma 5.1 (Correctness of booleans and conditional)

For all terms $u,v$:

1. $\mathsf{if}\, \mathsf{true}\, u\, v \to_\beta^* u$ and hence $\mathsf{if}\, \mathsf{true}\, u\, v \equiv_{\beta\eta} u$.
2. $\mathsf{if}\, \mathsf{false}\, u\, v \to_\beta^* v$ and hence $\mathsf{if}\, \mathsf{false}\, u\, v \equiv_{\beta\eta} v$.

*Proof.*

1.
$$
\begin{aligned}
\mathsf{if}\, \mathsf{true}\, u\, v
&\equiv (\lambda b.\lambda u.\lambda v.\, b\, u\, v)\, \mathsf{true}\, u\, v \\
&\to_\beta (\lambda u.\lambda v.\, \mathsf{true}\, u\, v)\, u\, v \\
&\to_\beta (\lambda v.\, \mathsf{true}\, u\, v)\, v \\
&\to_\beta \mathsf{true}\, u\, v \\
&\equiv (\lambda t.\lambda f.\, t)\, u\, v \\
&\to_\beta (\lambda f.\, u)\, v \\
&\to_\beta u.
\end{aligned}
$$

2. The calculation is symmetric with $\mathsf{false}$, which selects $v$ instead of $u$. ∎

We now encode logical connectives.

#### Definition 5.2 (Basic boolean connectives)

Define:

* $\mathsf{not} \triangleq \lambda b.\, b\, \mathsf{false}\, \mathsf{true}$,
* $\mathsf{and} \triangleq \lambda a.\lambda b.\, a\, b\, \mathsf{false}$,
* $\mathsf{or} \triangleq \lambda a.\lambda b.\, a\, \mathsf{true}\, b$.

#### Lemma 5.2 (Correctness of boolean connectives)

For all Church booleans $a,b \in \{\mathsf{true},\mathsf{false}\}$, the encodings realize the usual truth tables under $\equiv_{\beta\eta}$; e.g.:

* $\mathsf{not}\, \mathsf{true} \equiv_{\beta\eta} \mathsf{false}$ and $\mathsf{not}\, \mathsf{false} \equiv_{\beta\eta} \mathsf{true}$.
* $\mathsf{and}\, a\, b \equiv_{\beta\eta} \mathsf{true}$ iff both $a,b$ are $\mathsf{true}$; otherwise $\mathsf{false}$.
* $\mathsf{or}\, a\, b \equiv_{\beta\eta} \mathsf{false}$ iff both $a,b$ are $\mathsf{false}$; otherwise $\mathsf{true}$.

*Proof.* Straightforward case analysis on the four combinations $a,b \in \{\mathsf{true},\mathsf{false}\}$ using Lemma 5.1 and $\beta$-reduction. ∎

### 5.1.2 Church pairs and projections

Pairs are encoded as functions that consume a “continuation” choosing one of the components. This is the same pattern as booleans: a pair is a function that, given a selector, chooses a component. $\mathsf{fst}$ and $\mathsf{snd}$ are just two particular selectors.

#### Definition 5.3 (Pairs and projections)

Define:

* $\mathsf{pair} \triangleq \lambda a.\lambda b.\lambda p.\, p\, a\, b$,
* $\mathsf{fst} \triangleq \lambda r.\, r\, \mathsf{true}$,
* $\mathsf{snd} \triangleq \lambda r.\, r\, \mathsf{false}$.

Given $u,v$, we write
$$
\langle u , v \rangle \triangleq \mathsf{pair}\, u\, v.
$$

We expect:
$$
\mathsf{fst}\, \langle u,v\rangle \equiv_{\beta\eta} u,
\qquad
\mathsf{snd}\, \langle u,v\rangle \equiv_{\beta\eta} v.
$$

#### Lemma 5.3 (Correctness of pairs)

For all terms $u,v$:

1. $\mathsf{fst}\, \langle u,v\rangle \to_\beta^* u$ and hence $\mathsf{fst}\, \langle u,v\rangle \equiv_{\beta\eta} u$.
2. $\mathsf{snd}\, \langle u,v\rangle \to_\beta^* v$ and hence $\mathsf{snd}\, \langle u,v\rangle \equiv_{\beta\eta} v$.

*Proof.*

1.
$$
\begin{aligned}
\mathsf{fst}\, \langle u,v\rangle
&\equiv (\lambda r.\, r\, \mathsf{true})\, (\lambda p.\, p\, u\, v) \\
&\to_\beta (\lambda p.\, p\, u\, v)\, \mathsf{true} \\
&\to_\beta \mathsf{true}\, u\, v \\
&\equiv (\lambda t.\lambda f.\, t)\, u\, v \\
&\to_\beta u.
\end{aligned}
$$

2. The calculation is symmetric with $\mathsf{false}$, which selects $v$ instead of $u$. ∎

Pairs will reappear as **product types** in STLC (Module 9), where these encodings match the introduction–elimination rules for products.

---

## Core 5.2 – Church Numerals and Arithmetic

Natural numbers are encoded as *iterators*: $\overline{n}$ represents “apply $f$ exactly $n$ times”.

### 5.2.1 Church numerals

#### Definition 5.4 (Church numerals)

For each $n \in \mathbb{N}$, define the **Church numeral**:
$$
\overline{n} \triangleq \lambda f.\lambda x.\, f^n x,
$$
where:

* $f^0 x = x$,
* $f^{k+1} x = f (f^k x)$.

Explicitly:

* $\overline{0} \equiv \lambda f.\lambda x.\, x$,
* $\overline{1} \equiv \lambda f.\lambda x.\, f\, x$,
* $\overline{2} \equiv \lambda f.\lambda x.\, f (f\, x)$, etc.

#### Lemma 5.4 (Iterator property)

For all $n \in \mathbb{N}$, all terms $f,x$:
$$
\overline{n}\, f\, x \to_\beta^* f^n x.
$$

*Proof.* By induction on $n$.

* Base ($n=0$): $\overline{0}\, f\, x \equiv (\lambda f.\lambda x.\, x)\, f\, x \to_\beta x = f^0 x$.

* Step: Assume $\overline{n}\, f\, x \to_\beta^* f^n x$. Using the defining equation of Church numerals and the induction hypothesis, we may choose a $\beta\eta$-equivalent representative of $\overline{n+1}$ as $\lambda f.\lambda x.\, f\, (\overline{n}\, f\, x)$. Then
  $$
  \overline{n+1}\, f\, x \to_\beta f\, (\overline{n}\, f\, x) \to_\beta^* f\, (f^n x) = f^{n+1} x.
  $$

∎

### 5.2.2 Successor, addition, multiplication

We now define the standard arithmetic operators and state their correctness.

#### Definition 5.5 (Arithmetic operators)

Define:

* **Successor**:
  $$
  \mathsf{succ} \triangleq \lambda n.\lambda f.\lambda x.\, f\, (n\, f\, x).
  $$
* **Addition**:
  $$
  \mathsf{plus} \triangleq \lambda m.\lambda n.\lambda f.\lambda x.\, m\, f\, (n\, f\, x).
  $$
* **Multiplication**:
  $$
  \mathsf{mult} \triangleq \lambda m.\lambda n.\lambda f.\, m\, (n\, f).
  $$

#### Theorem 5.5 (Correctness of succ, plus, mult)

For all $m,n \in \mathbb{N}$:

1. $\mathsf{succ}\, \overline{n} \equiv_{\beta\eta} \overline{n+1}$.
2. $\mathsf{plus}\, \overline{m}\, \overline{n} \equiv_{\beta\eta} \overline{m+n}$.
3. $\mathsf{mult}\, \overline{m}\, \overline{n} \equiv_{\beta\eta} \overline{m \cdot n}$.

*Proof.*

1. For arbitrary $f,x$:
   $$
   \begin{aligned}
   \mathsf{succ}\, \overline{n}\, f\, x
   &\equiv (\lambda n.\lambda f.\lambda x.\, f\, (n\, f\, x))\, \overline{n}\, f\, x \\
   &\to_\beta (\lambda f.\lambda x.\, f\, (\overline{n}\, f\, x))\, f\, x \\
   &\to_\beta f\, (\overline{n}\, f\, x) \\
   &\to_\beta^* f\, (f^n x) = f^{n+1} x.
   \end{aligned}
   $$
   By Lemma 5.4, $\mathsf{succ}\, \overline{n}$ and $\overline{n+1}$ behave identically on all $f,x$, hence are $\equiv_{\beta\eta}$.

2. For arbitrary $f,x$:
   $$
   \begin{aligned}
   \mathsf{plus}\, \overline{m}\, \overline{n}\, f\, x
   &\equiv (\lambda m.\lambda n.\lambda f.\lambda x.\, m\, f\, (n\, f\, x))\, \overline{m}\, \overline{n}\, f\, x \\
   &\to_\beta (\lambda n.\lambda f.\lambda x.\, \overline{m}\, f\, (n\, f\, x))\, \overline{n}\, f\, x \\
   &\to_\beta (\lambda f.\lambda x.\, \overline{m}\, f\, (\overline{n}\, f\, x))\, f\, x \\
   &\to_\beta \overline{m}\, f\, (\overline{n}\, f\, x) \\
   &\to_\beta^* f^m (\overline{n}\, f\, x) \\
   &\to_\beta^* f^m (f^n x) = f^{m+n} x.
   \end{aligned}
   $$
   This is exactly the behavior of $\overline{m+n}$ by Lemma 5.4.

3. For arbitrary $f,x$:
   $$
   \begin{aligned}
   \mathsf{mult}\, \overline{m}\, \overline{n}\, f\, x
   &\equiv (\lambda m.\lambda n.\lambda f.\, m\, (n\, f))\, \overline{m}\, \overline{n}\, f\, x \\
   &\to_\beta (\lambda n.\lambda f.\, \overline{m}\, (n\, f))\, \overline{n}\, f\, x \\
   &\to_\beta (\lambda f.\, \overline{m}\, (\overline{n}\, f))\, f\, x \\
   &\to_\beta \overline{m}\, (\overline{n}\, f)\, x \\
   &\to_\beta^* (\overline{n}\, f)^m x.
   \end{aligned}
   $$
   By Lemma 5.4, $\overline{n}\, f$ is the function $y \mapsto f^n y$, so applying it $m$ times yields $f^{n \cdot m} x$. Thus the behavior coincides with $\overline{m \cdot n}$. ∎

### 5.2.3 Zero test and predecessor (statement only)

The zero test is easy; the predecessor is technically more delicate.

#### Definition 5.6 (Zero test and predecessor)

Define:

* **Zero test**:
  $$
  \mathsf{iszero} \triangleq \lambda n.\, n\, (\lambda x.\, \mathsf{false})\, \mathsf{true}.
  $$
* **Predecessor** (standard pair-encoding version):
  $$
  \mathsf{pred} \triangleq \lambda n.\lambda f.\lambda x.\,
  n\, (\lambda g.\lambda h.\, h\, (g\, f))\,
  (\lambda u.\, x)\,
  (\lambda u.\, u).
  $$

We do **not** re-derive the full proof here; we just record the standard result (see Barendregt [1984], §6.3 for details).

#### Theorem 5.6 (Correctness of iszero and pred – statement)

For all $n \in \mathbb{N}$:

1. $\mathsf{iszero}\, \overline{0} \equiv_{\beta\eta} \mathsf{true}$, and for $n>0$, $\mathsf{iszero}\, \overline{n} \equiv_{\beta\eta} \mathsf{false}$.
2. $\mathsf{pred}\, \overline{0} \equiv_{\beta\eta} \overline{0}$ and, for $n>0$, $\mathsf{pred}\, \overline{n} \equiv_{\beta\eta} \overline{n-1}$.

*Proof idea.* For $\mathsf{iszero}$ this is a one-line calculation using Lemma 5.4: $\overline{0}$ ignores the first argument and returns $\mathsf{true}$; any positive numeral applies the “make-false” function at least once and returns $\mathsf{false}$. For $\mathsf{pred}$, one iterates a state consisting of a pair of numerals, shifting them so that after $n$ iterations the first component holds $n-1$. ∎

---

## Core 5.3 – Strategy Sensitivity (Call-by-Name vs Call-by-Value)

All correctness statements above are formulated in terms of **$\beta\eta$-equivalence**, which abstracts from the **order** of reduction. However, when the $\lambda$-calculus is used as a *programming language* with a **fixed evaluation strategy**, Church encodings behave well under **call-by-name (CBN)**, but can misbehave under **call-by-value (CBV)**.

We do **not** define strategies formally here; that is the subject of Module 6. For now:

* Informally, CBN reduces the outermost redexes first and does not reduce under $\lambda$,
* CBV reduces arguments before passing them to a function.

In this module, “correctness” always means $\beta\eta$-equivalence. Under that notion, all encodings are extensionally correct. Under CBV, however, the operational semantics may diverge on terms that are $\beta\eta$-equivalent to a normal form. So Church encodings are extensionally correct but not always operationally correct under CBV in the presence of divergence.

#### Example 5.7 (Boolean encodings under CBV)

Consider:
$$
\mathsf{if}\, \mathsf{false}\, u\, v \equiv_{\beta\eta} v.
$$

* Under **CBN**, $u$ is never evaluated: the term reduces directly to $v$.
* Under **CBV**, both arguments $u$ and $v$ are evaluated *before* $\mathsf{false}$ is applied. So if $u$ diverges (e.g. $u = \Omega$), then $\mathsf{if}\, \mathsf{false}\, \Omega\, v$ diverges.

#### Example 5.8 (A concrete CBV anomaly)

Let $\Omega$ be a fixed divergent term. Consider:
$$
e \triangleq (\lambda n.\, \overline{0})\, (\mathsf{plus}\, \overline{1}\, \Omega).
$$

Under CBN, the argument $(\mathsf{plus}\, \overline{1}\, \Omega)$ is never evaluated; $e \to_\beta^* \overline{0}$. Under CBV, the argument must be evaluated first, but evaluating $(\mathsf{plus}\, \overline{1}\, \Omega)$ requires evaluating $\Omega$ and diverges.

Thus a $\beta\eta$-law like $(\lambda n.\, \overline{0})\, (\mathsf{plus}\, \overline{1}\, \Omega) \equiv_{\beta\eta} \overline{0}$ is not respected by CBV’s operational behavior.

We postpone **formal strategy theorems** to Module 6, where we define CBN/CBV semantics explicitly and can state, for example:

* Under CBN, Church encodings are **operationally correct** for the usual data and arithmetic,
* Under CBV, additional care (e.g. variants of fixed-point combinators, or different encodings) is needed.

---

## Core 5.4 – Fixed-Point Combinators and Recursion

The $\lambda$-calculus has no primitive recursion or self-reference. Fixed-point combinators allow us to define **recursive functions** purely within $\lambda$.

### 5.4.1 Fixed-point combinators

#### Definition 5.7 (Fixed-point combinator)

A term $Y$ is a **fixed-point combinator** (FPC) if for every term $f$:
$$
Y\, f \to_\beta^* f\, (Y\, f).
$$

Thus $Y\, f$ is a fixed point of $f$ with respect to $\beta$-reduction.

#### Definition 5.8 (Y and $\Theta$)

Define:

* **Curry’s Y**:
  $$
  Y \triangleq \lambda f.\, (\lambda x.\, f (x\, x))\, (\lambda x.\, f (x\, x)).
  $$
* **Turing’s $\Theta$**:
  $$
  \Theta \triangleq (\lambda x.\lambda y.\, y (x\, x\, y))\, (\lambda x.\lambda y.\, y (x\, x\, y)).
  $$

Both are classical fixed-point combinators; $\Theta$ is designed to behave better under CBV than $Y$.

#### Theorem 5.8 (Y and $\Theta$ are fixed-point combinators)

For all terms $f$:

1. $Y\, f \to_\beta^* f\, (Y\, f)$.
2. $\Theta\, f \to_\beta^* f\, (\Theta\, f)$.

*Proof.*

1.
$$
\begin{aligned}
Y\, f
&\equiv (\lambda f.\, (\lambda x.\, f (x\, x))\, (\lambda x.\, f (x\, x)))\, f \\
&\to_\beta (\lambda x.\, f (x\, x))\, (\lambda x.\, f (x\, x)) \\
&\to_\beta f\big( (\lambda x.\, f (x\, x))\, (\lambda x.\, f (x\, x)) \big) \\
&\equiv f (Y\, f).
\end{aligned}
$$

2. Let $G \equiv \lambda x.\lambda y.\, y (x\, x\, y)$. Then $\Theta \equiv G\, G$. For any $f$:
   $$
   \begin{aligned}
   \Theta\, f &= G\, G\, f \\
   &\to_\beta (\lambda y.\, y (G\, G\, y))\, f \\
   &\to_\beta f (G\, G\, f) \\
   &\equiv f (\Theta\, f).
   \end{aligned}
   $$
   ∎

Under **CBN**, both $Y$ and $\Theta$ behave as intended. Under **CBV**, $Y$ tends to diverge prematurely because it reduces $(x\, x)$ eagerly, whereas $\Theta$ delays self-application until after $f$ has been supplied; $\Theta$ is therefore better behaved in CBV.

#### Lemma 5.8.1 (Divergence of naive fixed points)

There exist functionals $F$ such that $Y\, F$ is unsolvable (i.e., has Böhm tree $\bot$ from Module 4). For example, take $F \triangleq \lambda r.\lambda x.\, r\, x$; then $Y\, F\, x \to_\beta^* (Y\, F)\, x$, yielding an infinite head reduction without exposing a variable head.

*Proof idea.* The unfolding $Y\, F \to_\beta^* F\, (Y\, F)$ loops forever under head reduction, as each step reintroduces a redex at the head without progress toward a neutral body. ∎

### 5.4.2 Recursive definitions via fixed points

Using an FPC $Y$, we can encode recursive functions in the usual “equation” style. This restriction ensures that recursive calls are always made in full arity, which matches the intended shape of the recursive definition and avoids ill-shaped uses like $r$ alone.

#### Definition 5.9 (Recursive definition pattern)

Given a “functional” $F$ of arity $k+1$:
$$
F \triangleq \lambda r.\lambda x_1.\dots.\lambda x_k.\, t[r,x_1,\dots,x_k],
$$
where $t$ may use $r$ **only in the form** $r\, u_1\dots u_k$, define:
$$
f \triangleq Y\, F.
$$

We intend $f$ to satisfy the recursive equation
$$
f\, x_1\dots x_k \approx t[f,x_1,\dots,x_k].
$$

#### Lemma 5.9 (Unfolding law for recursive definitions)

With $Y$ as in Def. 5.8 and $f \equiv Y\, F$ as above, we have:
$$
f\, x_1\dots x_k \equiv_{\beta\eta} F\, f\, x_1\dots x_k.
$$

*Proof.*
$$
\begin{aligned}
f &= Y\, F \to_\beta^* F (Y\, F) \equiv F\, f \\
\Rightarrow\quad
f\, x_1\dots x_k &\equiv F\, f\, x_1\dots x_k
\end{aligned}
$$
by $\beta$-reduction and congruence. ∎

This is exactly the usual unfolding equation used to reason about recursive definitions.

### 5.4.3 Example: factorial on Church numerals

We can define factorial using Church numerals and an FPC.

#### Definition 5.10 (Factorial functional and factorial)

Let $\mathsf{iszero}$, $\mathsf{pred}$, $\mathsf{mult}$, $\overline{1}$ be as in Defs. 5.5–5.6. Define:
$$
F_{\mathsf{fac}} \triangleq
\lambda r.\lambda n.\,
\mathsf{if}\, (\mathsf{iszero}\, n)\, \overline{1}\, (\mathsf{mult}\, n\, (r\, (\mathsf{pred}\, n))).
$$

Define the **factorial**:
$$
\mathsf{fac} \triangleq Y\, F_{\mathsf{fac}}.
$$

#### Theorem 5.10 (Factorial correctness – statement)

For every $n \in \mathbb{N}$:
$$
\mathsf{fac}\, \overline{n} \equiv_{\beta\eta} \overline{n!}.
$$

*Proof idea.* Induction on $n$ using the unfolding law (Lemma 5.9) and the arithmetic correctness theorems (Theorems 5.5, 5.6).

For $n=0$, $\mathsf{iszero}\, \overline{0} \equiv \mathsf{true}$, so we obtain $\overline{1}$.

For $n>0$, the unfolding gives
$$
\mathsf{fac}\, \overline{n}
\equiv \mathsf{mult}\, \overline{n}\, (\mathsf{fac}\, \overline{n-1}),
$$
and the induction hypothesis gives the desired $n \cdot (n-1)! = n!$. ∎

We do not expand the full $\beta$-reduction; the pattern is standard and uses only results from this module and Module 3.

---

## Core 5.5 – Lists, Map, and Fold (via Church Encodings)

To illustrate higher-order programming, we encode **finite lists** of elements and define `map` and `foldr` using the encodings directly (no fixed points needed).

### 5.5.1 Church lists

Lists are encoded as higher-order folds: a list is a function that, given a “cons” handler and a “nil” value, performs a right fold. (In the untyped calculus, the element type is purely informal; the shape of the encoding does not enforce any type discipline yet.)

#### Definition 5.11 (Lists, nil, cons)

Define:

* **Nil**:
  $$
  \mathsf{nil} \triangleq \lambda c.\lambda n.\, n.
  $$
* **Cons**:
  $$
  \mathsf{cons} \triangleq \lambda h.\lambda t.\lambda c.\lambda n.\, c\, h\, (t\, c\, n).
  $$

Intuition: a list $l$ is a function such that $l\, c\, n$ behaves like `foldr c n` over the list.

We can define destructors:

* **IsNil**:
  $$
  \mathsf{isnil} \triangleq \lambda l.\, l\, (\lambda h.\lambda r.\, \mathsf{false})\, \mathsf{true}.
  $$
* **Head** (partial, erroring on nil):
  $$
  \mathsf{head} \triangleq \lambda l.\, l\, (\lambda h.\lambda r.\, h)\, \Omega,
  $$
  where $\Omega$ is any fixed divergent term (intentional partiality in an untyped setting).
* **Tail**:
  $$
  \mathsf{tail} \triangleq \lambda l.\, l\, (\lambda h.\lambda r.\, r)\, \mathsf{nil}.
  $$

We will not prove all destructor properties here; they are standard exercises.

### 5.5.2 Map and fold via encodings

We define `foldr` and `map` directly from the encodings (no recursion needed).

#### Definition 5.12 (Foldr and map)

Define:

* **Foldr**:
  $$
  \mathsf{foldr} \triangleq \lambda op.\lambda z.\lambda l.\, l\, op\, z.
  $$

* **Map**:
  $$
  \mathsf{map} \triangleq \lambda f.\lambda l.\lambda c.\lambda n.\, l\, (\lambda h.\lambda r.\, c\, (f\, h)\, r)\, n.
  $$

Intuitively:

* $\mathsf{foldr}\, op\, z\, [h_1,\dots,h_n] = op\, h_1\, (op\, h_2 (\dots (op\, h_n\, z)\dots))$,
* $\mathsf{map}\, f\, [h_1,\dots,h_n] = [f\, h_1,\dots,f\, h_n]$.

#### Lemma 5.11 (Foldr recursion law)

For all terms $op,z$ and lists $l$ encoded as above:

1. $\mathsf{foldr}\, op\, z\, \mathsf{nil} \equiv_{\beta\eta} z$.
2. $\mathsf{foldr}\, op\, z\, (\mathsf{cons}\, h\, t)
   \equiv_{\beta\eta} op\, h\, (\mathsf{foldr}\, op\, z\, t)$.

*Proof.*

1. $\mathsf{foldr}\, op\, z\, \mathsf{nil} \equiv (\lambda op.\lambda z.\lambda l.\, l\, op\, z)\, op\, z\, \mathsf{nil} \to_\beta \mathsf{nil}\, op\, z \equiv (\lambda c.\lambda n.\, n)\, op\, z \to_\beta z$.

2. $\mathsf{foldr}\, op\, z\, (\mathsf{cons}\, h\, t) \equiv (\mathsf{cons}\, h\, t)\, op\, z \equiv (\lambda h.\lambda t.\lambda c.\lambda n.\, c\, h\, (t\, c\, n))\, h\, t\, op\, z \to_\beta op\, h\, (t\, op\, z) \equiv op\, h\, (\mathsf{foldr}\, op\, z\, t)$. ∎

#### Lemma 5.12 (Map recursion law)

For all $f$ and lists $l$:

1. $\mathsf{map}\, f\, \mathsf{nil} \equiv_{\beta\eta} \mathsf{nil}$.
2. $\mathsf{map}\, f\, (\mathsf{cons}\, h\, t)
   \equiv_{\beta\eta} \mathsf{cons}\, (f\, h)\, (\mathsf{map}\, f\, t)$.

*Proof.* Because lists are Church-encoded as $\lambda c.\lambda n.\, \dots$, to show two lists $L$ and $M$ are equal up to $\equiv_{\beta\eta}$, it suffices to show that for arbitrary $c,n$,
$$
L\, c\, n \to_\beta^* M\, c\, n.
$$

1. For $\mathsf{nil}$:
   $$
   \begin{aligned}
   \mathsf{map}\, f\, \mathsf{nil}
   &\equiv \lambda c.\lambda n.\, \mathsf{nil}\, (\lambda h.\lambda r.\, c\, (f\, h)\, r)\, n \\
   &\equiv \lambda c.\lambda n.\, (\lambda c.\lambda n.\, n)\, (\lambda h.\lambda r.\, c\, (f\, h)\, r)\, n \\
   &\to_\beta \lambda c.\lambda n.\, n \\
   &\equiv \mathsf{nil}.
   \end{aligned}
   $$

2. For $\mathsf{cons}\, h\, t$:
   $$
   \begin{aligned}
   \mathsf{map}\, f\, (\mathsf{cons}\, h\, t)
   &\equiv \lambda c.\lambda n.\, (\mathsf{cons}\, h\, t)\, (\lambda h'.\lambda r.\, c\, (f\, h')\, r)\, n \\
   &\equiv \lambda c.\lambda n.\, (\lambda h.\lambda t.\lambda c.\lambda n.\, c\, h\, (t\, c\, n))\, h\, t\, (\lambda h'.\lambda r.\, c\, (f\, h')\, r)\, n \\
   &\to_\beta \lambda c.\lambda n.\, (\lambda t.\lambda c.\lambda n.\, c\, h\, (t\, c\, n))\, t\, (\lambda h'.\lambda r.\, c\, (f\, h')\, r)\, n \\
   &\to_\beta \lambda c.\lambda n.\, (\lambda c.\lambda n.\, c\, h\, (t\, c\, n))\, (\lambda h'.\lambda r.\, c\, (f\, h')\, r)\, n \\
   &\to_\beta \lambda c.\lambda n.\, (\lambda n.\, (\lambda h'.\lambda r.\, c\, (f\, h')\, r)\, h\, (t\, (\lambda h'.\lambda r.\, c\, (f\, h')\, r)\, n))\, n \\
   &\to_\beta \lambda c.\lambda n.\, (\lambda h'.\lambda r.\, c\, (f\, h')\, r)\, h\, (t\, (\lambda h'.\lambda r.\, c\, (f\, h')\, r)\, n) \\
   &\to_\beta \lambda c.\lambda n.\, c\, (f\, h)\, (t\, (\lambda h'.\lambda r.\, c\, (f\, h')\, r)\, n) \\
   &\equiv \lambda c.\lambda n.\, c\, (f\, h)\, (\mathsf{map}\, f\, t\, c\, n) \\
   &\equiv \mathsf{cons}\, (f\, h)\, (\mathsf{map}\, f\, t).
   \end{aligned}
   $$
   ∎

These laws match precisely the familiar recursion equations for `foldr` and `map` in functional programming languages.

---

## Core 5.6 – Combinatory Logic and SKI Translation

Finally, we briefly link the $\lambda$-calculus to **combinatory logic (CL)**, which eliminates $\lambda$-abstractions entirely by expressing programs in terms of a small basis of combinators.

### 5.6.1 SKI combinators

#### Definition 5.13 (S, K, I)

Define:

* $K \equiv \lambda x.\lambda y.\, x$   (constant function),
* $I \equiv \lambda x.\, x$              (identity),
* $S \equiv \lambda x.\lambda y.\lambda z.\, x\, z\, (y\, z)$.

In pure combinatory logic, terms are built from variables and $S,K$ (and optionally $I$) using application only; reduction is governed by the rewrite rules
$$
\begin{aligned}
K\, x\, y &\to x, \\
S\, x\, y\, z &\to x\, z\, (y\, z).
\end{aligned}
$$

### 5.6.2 Bracket abstraction and translation

Every $\lambda$-term can be translated to an equivalent **SKI** term by eliminating $\lambda$’s via *bracket abstraction*.

We omit the full algorithm and state the standard result. If we embed SKI back into $\lambda$-calculus by interpreting $S,K,I$ as the $\lambda$-terms above, then $t^*$ is $\beta\eta$-equivalent to $t$.

#### Theorem 5.13 ($\lambda \to$ SKI translation – statement)

There exists an effective translation $(\cdot)^*$ from $\lambda$-terms to SKI-terms such that:

1. If $t \to_\beta u$ in the $\lambda$-calculus, then $t^* \to^* u^*$ in the SKI system (where $\to$ is generated by the $K$ and $S$ reduction rules).
2. For every $\lambda$-term $t$, $t^* \equiv_{\beta\eta} t$ when read back into the $\lambda$-calculus.

In particular, combinatory logic is **equivalent** to the $\lambda$-calculus in expressive power.

*Proof idea.* Define bracket abstraction $[x]t$ by recursion on $t$:

* If $x$ not free in $t$, set $[x]t \equiv K\, t$,
* $[x]x \equiv I$,
* $[x](u\, v) \equiv S\, ([x]u)\, ([x]v)$.

Then $(\lambda x.t)^* \equiv [x](t^*)$, and $(u\, v)^* \equiv u^*\, v^*$. Induction on the structure of $t$ gives the required simulation of $\beta$-reduction by SKI-reduction. ∎

**Example.** $[x] (x\, y) = S\, I\, (K\, y)$. Check: $(S\, I\, (K\, y))\, z \to_\beta z\, y$, matching $\lambda x.\, x\, y$.

This shows that all of the programming power we have developed in this module can also be realized in a language **without variables at all**.

---

## Summary and Exercises

In this module we:

* Encoded **booleans** and **pairs** (Defs. 5.1–5.3) and proved their correctness (Lemmas 5.1–5.3).
* Encoded **natural numbers** and basic **arithmetic** (Defs. 5.4–5.6) and proved correctness for successor, addition, and multiplication (Thm. 5.5), with standard statements for zero and predecessor (Thm. 5.6).
* Isolated **strategy sensitivity** (Core 5.3), noting that Church encodings rely on non-strict evaluation (CBN).
* Introduced **fixed-point combinators** $Y$ and $\Theta$ (Defs. 5.7–5.8), proved they satisfy the fixed-point property (Thm. 5.8), and used them for **recursive definitions** (Lemmas 5.9, 5.10).
* Encoded **lists**, **map**, and **foldr** (Defs. 5.11–5.12) and stated their recursion laws (Lemmas 5.11–5.12).
* Linked the $\lambda$-calculus to **combinatory logic** via SKI and the $\lambda\to$SKI translation (Thm. 5.13).

These constructions prepare the ground for:

* **Operational strategies and machines** (Module 6),
* **Typed encodings** of booleans, products, and sums in STLC (Modules 8–9),
* **Inductive and recursive types** for naturals and lists (Module 11),
* **Polymorphic encodings** (System F, Module 12).

### Suggested Exercises

1. **Boolean exercises**

   * Reduce $\mathsf{not}\, \mathsf{true}$ and $\mathsf{not}\, \mathsf{false}$ to normal form.
   * Show $\mathsf{and}\, \mathsf{false}\, \Omega$ diverges under CBV but not under CBN.

2. **Arithmetic exercises**

   * Give a full $\beta$-reduction trace showing $\mathsf{plus}\, \overline{2}\, \overline{3} \equiv_{\beta\eta} \overline{5}$.
   * Do the same for $\mathsf{mult}\, \overline{2}\, \overline{3} \equiv_{\beta\eta} \overline{6}$.

3. **Fixed-point exercises**

   * Fully expand the reduction $Y\, f \to_\beta^* f\, (Y\, f)$ in 2–3 steps.
   * Define a “sum-to-$n$” function $\mathsf{sum}$ via $Y$ and prove $\mathsf{sum}\, \overline{n} \equiv_{\beta\eta} \overline{1+2+\dots+n}$.

4. **List exercises**

   * Encode the list $[\overline{0},\overline{1}]$ using $\mathsf{nil}$ and $\mathsf{cons}$ and compute $\mathsf{foldr}\, \mathsf{plus}\, \overline{0}\, [\overline{0},\overline{1}]$.
   * Show that $\mathsf{map}\, \mathsf{succ}\, [\overline{0},\overline{1}] \equiv_{\beta\eta} [\overline{1},\overline{2}]$.

5. **SKI exercises**

   * Apply the bracket abstraction algorithm to translate $\lambda x.\lambda y.\, x\, y$ to SKI.
   * Reduce $S\, K\, K\, t$ and show that it behaves like the identity on $t$.
