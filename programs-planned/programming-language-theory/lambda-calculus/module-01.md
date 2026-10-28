# Module 1 – Syntax, Binding, and Substitution

This module establishes the **basic syntax** of the $\lambda$-calculus:
* what $\lambda$-terms are (as abstract trees),
* how **binding** and **free variables** work,
* what it means to be **equal up to renaming** ($\alpha$-equivalence),
* and how to define **capture-avoiding substitution** rigorously.

From **Module 2** onward, we will switch to nameless representations (De Bruijn, locally nameless) for mechanization. Here, we deliberately stay with a **named** syntax for clarity: we *define* everything on raw terms, but from **Module 3** onward we reason modulo $\alpha$ by default. This keeps Module 1 as the raw-syntax reference and aligns cleanly with Module 2’s move to $\alpha$-classes.

---

## 1.1 Abstract Syntax of $\lambda$-Terms

We first define $\lambda$-terms as inductively generated trees.

### Definition 1.1 (Variables and $\lambda$-terms)

Let $\mathcal{V} = \{x,y,z,x_1,x_2,\dots\}$ be a countably infinite set of **variables**.

The set $\Lambda$ of **$\lambda$-terms** is the smallest set such that:
* (Var) If $x \in \mathcal{V}$, then $x \in \Lambda$.
* (Abs) If $x \in \mathcal{V}$ and $t \in \Lambda$, then $\lambda x.t \in \Lambda$.
* (App) If $t_1,t_2 \in \Lambda$, then $t_1\, t_2 \in \Lambda$.

We write this also as the grammar:
$$
t ::= x \mid \lambda x.t \mid t\, t.
$$

Intuition:
* $x$ is a variable,
* $\lambda x.t$ is a **function** with parameter $x$ and body $t$,
* $t_1\, t_2$ is **application**.

### Concrete vs Abstract Syntax

The grammar above defines the **abstract syntax** (trees). For **concrete syntax** we use:
* Application associates to the **left**:
  $t_1\, t_2\, t_3 \equiv (t_1\, t_2)\, t_3$.
* Abstraction scopes to the **right**:
  $\lambda x.\, \lambda y.t \equiv \lambda x.(\lambda y.t)$.

To formalize unique parsing, consider the concrete grammar with precedence: application has higher precedence than abstraction (so $\lambda x.t\, u \equiv \lambda x.(t\, u)$), and left-associativity for applications. Every well-formed string under these rules parses to a unique abstract tree in $\Lambda$, as the precedence disambiguates nesting and associativity resolves chains.

> **Remark 1.1 (Unique parsing).**  
> Every concrete $\lambda$-term (with the above precedence and associativity rules) has a unique abstract syntax tree in $\Lambda$.  
> 
> *Proof sketch:* The concrete syntax corresponds to an unambiguous context-free grammar enforcing left-associative applications and right-scoping abstractions at the appropriate precedence levels. Unambiguity follows by induction on string length: base cases (variables, parenthesized terms, simple abstractions) are unique; inductive cases uniquely decompose into subterms via deterministic prefix matching and recursive parsing, yielding a single derivation and AST per valid string.

---

## 1.2 Free and Bound Variables, Scope, Capture

We now distinguish **bound** and **free** occurrences, and define scope formally.

### Definition 1.2 (Free variables)

The set of **free variables** of a term $t$, written $\mathrm{FV}(t)$, is defined inductively:
* $\mathrm{FV}(x) = \{x\}$.
* $\mathrm{FV}(\lambda x.t) = \mathrm{FV}(t) \setminus \{x\}$.
* $\mathrm{FV}(t_1\, t_2) = \mathrm{FV}(t_1) \cup \mathrm{FV}(t_2)$.

An occurrence of $x$ in $t$ is **bound** if it lies in the body of some enclosing $\lambda x.\, u$; otherwise it is **free**.

### Definition 1.2' (Bound variables)

The set of **bound variables** of a term $t$, written $\mathrm{BV}(t)$, is defined inductively:
* $\mathrm{BV}(x) = \emptyset$.
* $\mathrm{BV}(\lambda x.t) = \{x\} \cup \mathrm{BV}(t)$.
* $\mathrm{BV}(t_1\, t_2) = \mathrm{BV}(t_1) \cup \mathrm{BV}(t_2)$.

The set of all variables occurring in $t$ (free or bound) is $\mathrm{Vars}(t) = \mathrm{FV}(t) \cup \mathrm{BV}(t)$.

> **Definition 1.3 (Closed term).**  
> A term $t$ is **closed** if $\mathrm{FV}(t)=\emptyset$, otherwise **open**.

Examples:
* $t_1 = x$  
  $\mathrm{FV}(t_1) = \{x\}$, $\mathrm{BV}(t_1) = \emptyset$, $\mathrm{Vars}(t_1) = \{x\}$ (open)
* $t_2 = \lambda x.x$  
  $\mathrm{FV}(t_2) = \emptyset$, $\mathrm{BV}(t_2) = \{x\}$ (closed)
* $t_3 = (\lambda x.y\, x)\, z$  
  $y,z$ free, $x$ bound; $\mathrm{FV}(t_3)=\{y,z\}$, $\mathrm{BV}(t_3)=\{x\}$, $\mathrm{Vars}(t_3)=\{x,y,z\}$.

> **Remark.** This is **lexical scoping**: bindings are determined purely by the syntax, not by runtime state.

---

## 1.3 $\alpha$-Conversion and $\alpha$-Equivalence

Bound variable names are **syntactic noise**: renaming a bound variable does not change the computation.

### Definition 1.4 ($\alpha$-conversion step)

Let $x,y \in \mathcal{V}$ with $y \neq x$ and $y \notin \mathrm{Vars}(t)$. We write
$$
\lambda x.t \xrightarrow{\alpha} \lambda y.\, t[x \mapsto y]
$$
for an **$\alpha$-conversion step**, where $t[x \mapsto y]$ denotes the result of replacing all occurrences of $x$ in $t$ that are bound by the outer $\lambda x$ (equivalently, all free occurrences of $x$ in the body $t$) by $y$. This is defined by structural recursion on $t$:
* If $t = z$ (variable), then $z[x \mapsto y] = y$ if $z = x$, else $z$.
* If $t = \lambda z.u$, then $(\lambda z.u)[x \mapsto y] = \lambda z.u[x \mapsto y]$.
* If $t = u_1\, u_2$, then $(u_1\, u_2)[x \mapsto y] = u_1[x \mapsto y]\, u_2[x \mapsto y]$.

This replacement is capture-avoiding because $y$ is chosen fresh ($y \notin \mathrm{Vars}(t)$), ensuring no accidental binding of free or bound variables.

### Definition 1.5 ($\alpha$-equivalence)

The **$\alpha$-equivalence** relation $\equiv_\alpha$ is the smallest equivalence relation on $\Lambda$ that contains all $\alpha$-conversion steps and is closed under contexts:
* If $t \xrightarrow{\alpha} t'$, then $t \equiv_\alpha t'$.
* If $t \equiv_\alpha t'$, then:
  * $\lambda x.t \equiv_\alpha \lambda x.t'$,
  * $t\, u \equiv_\alpha t'\, u$,
  * $u\, t \equiv_\alpha u\, t'$.

Examples:
* $\lambda x.x \equiv_\alpha \lambda z.z$.
* $\lambda x.(\lambda y.x\, z) \equiv_\alpha \lambda a.(\lambda b.a\, z)$.
* $\lambda x.y \not\equiv_\alpha \lambda y.y$ (the second changes the free variable).

> **Theorem 1.2.**  
> $\equiv_\alpha$ is an **equivalence relation** (reflexive, symmetric, transitive).  
> *Proof:* Routine closure properties and symmetry/transitivity via reflexive–symmetric–transitive closure of the $\alpha$-step.

> 
> **Lemma 1.1 (Free variables invariant under $\alpha$).**  
If $t \equiv_\alpha u$ then $\mathrm{FV}(t) = \mathrm{FV}(u)$.  
>
> *Proof sketch:* Proceed by induction on the derivation of $t \equiv_\alpha u$. The only non-trivial case is the $\alpha$-step for an abstraction:  
>$$\mathrm{FV}(\lambda x.t) = \mathrm{FV}(t) \setminus \{x\}$$  
>and  
> $$\mathrm{FV}(\lambda y.t[x \mapsto y]) = \mathrm{FV}(t[x \mapsto y]) \setminus \{y\}.$$  
> Because $y$ is fresh with respect to $\mathrm{Vars}(t)$ and only occurrences of $x$ bound by the outer binder are changed (via capture-avoiding $\alpha$-renaming), the free-variable sets coincide.

---

## 1.4 Capture-Avoiding Substitution

Substitution instantiates a variable with a term. It must **avoid capture**: free variables of the substituted term must not become bound accidentally.

We first define a **naïve substitution** (without renaming), which fails on capture, then the **correct capture-avoiding** version. These follow Barendregt's convention: we assume variables are chosen fresh when needed, and define by structural recursion on the subject term.

### Naïve Substitution (Capture-Prone)

For $s,t \in \Lambda$ and $x \in \mathcal{V}$, the **naïve** substitution $t[s/x]_{\text{naïve}}$ replaces all free occurrences of $x$ in $t$ by $s$, *without* renaming binders:
1. Variables:
   * $x[s/x]_{\text{naïve}} = s$,
   * $y[s/x]_{\text{naïve}} = y$ for $y \neq x$.
2. Application:
   * $(t_1\, t_2)[s/x]_{\text{naïve}} = t_1[s/x]_{\text{naïve}}\, t_2[s/x]_{\text{naïve}}$.
3. Abstraction:
   * $(\lambda y.t)[s/x]_{\text{naïve}} = \lambda y.\, t[s/x]_{\text{naïve}}$ (even if $y \in \mathrm{FV}(s)$).

This captures free variables of $s$ under $\lambda y$ if $y \in \mathrm{FV}(s)$.

#### Failure Example

Consider $t = \lambda y.x$ and $s = y$, so $x[s/x]_{\text{naïve}} = y$. Naïve substitution gives:
$$
(\lambda y.x)[y/x]_{\text{naïve}} = \lambda y.\, x[y/x]_{\text{naïve}} = \lambda y.y.
$$
Intuitively, $\lambda y.x$ is a constant function returning free $x$, but the result $\lambda y.y$ is the identity—capture has changed the meaning.

### Correct Capture-Avoiding Substitution

To fix this, we rename binders explicitly when capture risks occur.

### Definition 1.6 (Capture-avoiding substitution)

For $s,t \in \Lambda$ and $x \in \mathcal{V}$, the substitution $t[s/x]$ is defined by recursion on $t$ (following the naïve cases, except for abstraction):
1. Variables: As in naïve.
2. Application: As in naïve.
3. Abstraction:
   * $(\lambda x.t)[s/x] = \lambda x.t$ (binder shadows $x$).
   * For $y \neq x$:
     $$
     (\lambda y.t)[s/x] =
     \begin{cases}
     \lambda y.(t[s/x]) & \text{if } y \notin \mathrm{FV}(s),\\
     \lambda z.(t[y \mapsto z])[s/x] & \text{if } y \in \mathrm{FV}(s),
     \end{cases}
     $$
     where $z$ is fresh ($z \notin \mathrm{Vars}(t) \cup \mathrm{Vars}(s) \cup \{x\}$) and $t[y \mapsto z]$ is the capture-avoiding $\alpha$-renaming of all occurrences of $y$ in $t$ that are bound by the outer $\lambda y$ (equivalently, all free occurrences of $y$ in the body $t$) to $z$ (as in Def. 1.4).

The side condition $y \notin \mathrm{FV}(s)$ ensures no capture; otherwise, $\alpha$-rename first.

#### Corrected Example

For the same $t = \lambda y.x$, $s = y$:
* $y \in \mathrm{FV}(s)$, so rename: choose $z$ fresh ($z \notin \mathrm{Vars}(t) \cup \mathrm{Vars}(s) \cup \{x\} = \{x,y\}$).
* $(\lambda y.x)[y/x] = \lambda z. (x[y \mapsto z])[y/x]$.
* First, $x[y \mapsto z] = x$ (no bound $y$ in $x$).
* Then, $x[y/x] = y$.
* Thus, $\lambda z.y$, the constant function returning free $y$, as intended (matching the original $\lambda y.x$ substituted to return free $y$).

This preserves meaning.

### Basic Properties

> **Theorem 1.3 (Free variables under substitution).**  
> For any terms $t,s$ and variable $x$,  
> $$\mathrm{FV}(t[s/x]) = \big(\mathrm{FV}(t) \setminus \{x\}\big) \cup
 \begin{cases}
 \mathrm{FV}(s) & \text{if } x \in \mathrm{FV}(t),\\
 \emptyset & \text{otherwise.}
 \end{cases}$$ 
> Equivalently: “We remove $x$ from $\mathrm{FV}(t)$ and add the free variables of $s$ precisely where $x$ occurred.”  
> *Proof sketch:* By structural induction on $t$. The abstraction case with renaming uses freshness of $z$ w.r.t. $\mathrm{Vars}(t) \cup \mathrm{Vars}(s) \cup \{x\}$ to preserve sets.

> **Lemma 1.2 (Substitution respects $\alpha$).**  
> If $t \equiv_\alpha u$, then for all $s,x$ we have $t[s/x] \equiv_\alpha u[s/x]$.  
> *Proof idea:* Induction on the derivation of $t \equiv_\alpha u$; both $\alpha$-steps and substitution use compatible freshness conditions.

---

## 1.5 Structural Induction and Recursion on Terms

Most properties of $\lambda$-terms are proved by **structural induction** on the syntax. We also introduce a **recursion principle** (fold) for defining functions on terms.

### Theorem 1.4 (Structural induction on $\lambda$-terms)

Let $P$ be a predicate on $\lambda$-terms such that:
1. (Var) $\forall x \in \mathcal{V}.\ P(x)$.
2. (Abs) $\forall x \in \mathcal{V}, \forall t \in \Lambda.\ (P(t) \implies P(\lambda x.t))$.
3. (App) $\forall t_1, t_2 \in \Lambda.\ (P(t_1) \land P(t_2) \implies P(t_1\, t_2))$.

Then $\forall t \in \Lambda.\ P(t)$.

*Proof:* By the standard induction principle on the inductive definition of $\Lambda$ (Def. 1.1); the cases match the constructors.

We will silently use this principle in later modules.

#### Worked Example: Finiteness of Free Variables

> **Theorem 1.5 (Finiteness of FV).**  
> For all $t \in \Lambda$, $\mathrm{FV}(t)$ is finite.  
> *Proof:* By induction on $t$ (Thm. 1.4). Let $P(t) \iff \mathrm{FV}(t)$ is finite.  
> - (Var) $\mathrm{FV}(x) = \{x\}$, singleton: finite.  
> - (Abs) Assume $P(t)$ (i.e., $\mathrm{FV}(t)$ finite). Then $\mathrm{FV}(\lambda x.t) = \mathrm{FV}(t) \setminus \{x\}$, a subset: finite.  
> - (App) Assume $P(t_1), P(t_2)$. Then $\mathrm{FV}(t_1\, t_2) = \mathrm{FV}(t_1) \cup \mathrm{FV}(t_2)$, finite union: finite.  
> Thus $P(t)$ for all $t$.

A similar argument shows $\mathrm{BV}(t)$ and $\mathrm{Vars}(t)$ are finite.

### Principle 1.2 (Recursion / Fold on $\lambda$-terms)

To define a function $f: \Lambda \to S$ (for some set $S$) by recursion on term structure, specify:
1. (Var) A function $v: \mathcal{V} \to S$ (how variables map).
2. (Abs) A function $a: \mathcal{V} \times S \to S$ (how to combine variable and body result).
3. (App) A function $p: S \times S \to S$ (how to combine function and argument results).

There exists a unique $f$ such that:
* $f(x) = v(x)$,
* $f(\lambda x.t) = a(x, f(t))$,
* $f(t_1\, t_2) = p(f(t_1), f(t_2))$.

This is the **fold** or **catamorphism** for $\lambda$-terms; $\mathrm{FV}$ is an example ($S = \mathcal{P}(\mathcal{V})$, $v(x) = \{x\}$, $a(x, T) = T \setminus \{x\}$, $p(T_1, T_2) = T_1 \cup T_2$). Similarly for $\mathrm{BV}$ ($v(x)=\emptyset$, $a(x,U)= \{x\} \cup U$, $p(U_1,U_2)=U_1 \cup U_2$).

#### Example: Term Size

Define $|t|$ recursively (as in Principle 1.2, with $S = \mathbb{N}$, $v(x) = 1$, $a(x, n) = 1 + n$, $p(n_1, n_2) = 1 + n_1 + n_2$). By the recursion principle, it is well-defined and total.

### Example: Closedness under Substitution

> **Lemma 1.3 (Closedness preserved under substitution).**  
> If $t$ and $s$ are closed and $x$ is any variable, then $t[s/x]$ is closed.  
> *Proof:* By Thm. 1.3, $\mathrm{FV}(t[s/x]) \subseteq (\mathrm{FV}(t)\setminus\{x\}) \cup \mathrm{FV}(s) = \emptyset$.

---

## 1.6 Implementations

This section provides Python implementations of the key functions defined in this module, including term representation, free/bound/all variables computation, pretty-printing, naïve and capture-avoiding substitution, freshness generation, and a dedicated renaming function. These are spec-level illustrations aligned with the definitions.

```python
from dataclasses import dataclass

class Term: ...
@dataclass
class Var(Term):
    name: str

@dataclass
class Abs(Term):
    var: str
    body: Term

@dataclass
class App(Term):
    func: Term
    arg: Term

def free_vars(t: Term) -> set[str]:
    if isinstance(t, Var):
        return {t.name}
    if isinstance(t, Abs):
        return free_vars(t.body) - {t.var}
    if isinstance(t, App):
        return free_vars(t.func) | free_vars(t.arg)
    raise TypeError("unknown term")

def bound_vars(t: Term) -> set[str]:
    if isinstance(t, Var):
        return set()
    if isinstance(t, Abs):
        return {t.var} | bound_vars(t.body)
    if isinstance(t, App):
        return bound_vars(t.func) | bound_vars(t.arg)
    raise TypeError("unknown term")

def all_vars(t: Term) -> set[str]:
    return free_vars(t) | bound_vars(t)

def pretty(t: Term) -> str:
    if isinstance(t, Var):
        return t.name
    elif isinstance(t, Abs):
        return f"λ{t.var}.{pretty(t.body)}"
    elif isinstance(t, App):
        return f"({pretty(t.func)} {pretty(t.arg)})"
    raise TypeError("unknown term")

def fresh_name(avoid: set[str]) -> str:
    if "z" not in avoid:
        return "z"
    i = 0
    while True:
        candidate = f"z_{i}"
        if candidate not in avoid:
            return candidate
        i += 1

def rename(t: Term, old: str, new: str) -> Term:
    """Dedicated α-renaming: replace free occurrences of old in t with new (bound by outer binder)."""
    if isinstance(t, Var):
        return Var(new) if t.name == old else t
    if isinstance(t, App):
        return App(rename(t.func, old, new), rename(t.arg, old, new))
    if isinstance(t, Abs):
        return Abs(t.var, rename(t.body, old, new))
    raise TypeError("unknown term")

def subst_naive(t: Term, x: str, s: Term) -> Term:
    if isinstance(t, Var):
        return s if t.name == x else t
    if isinstance(t, App):
        return App(subst_naive(t.func, x, s), subst_naive(t.arg, x, s))
    if isinstance(t, Abs):
        # No renaming: always recurse
        return Abs(t.var, subst_naive(t.body, x, s))
    raise TypeError("unknown term")

def subst(t: Term, x: str, s: Term) -> Term:
    if isinstance(t, Var):
        return s if t.name == x else t
    if isinstance(t, App):
        return App(subst(t.func, x, s), subst(t.arg, x, s))
    if isinstance(t, Abs):
        if t.var == x:
            return t # Shadowed
        fv_s = free_vars(s)
        if t.var not in fv_s:
            return Abs(t.var, subst(t.body, x, s))
        # Rename to avoid capture
        avoid = all_vars(t.body) | all_vars(s) | {x}
        new_var = fresh_name(avoid)
        renamed_body = rename(t.body, t.var, new_var) # α-rename bound occurrences
        return Abs(new_var, subst(renamed_body, x, s))
    raise TypeError("unknown term")

# Example tests
t = Abs("y", Var("x")) # λy.x
s = Var("y") # y

# Naïve substitution failure
result_naive = subst_naive(t, "x", s)
print(f"Naïve: {pretty(result_naive)}")  # λy.y (captured)
print("Naive capture demonstrated!")

# Correct substitution
result_correct = subst(t, "x", s)
print(f"Correct: {pretty(result_correct)}")  # λz.y (no capture)
print("Capture avoided!")
```

These functions correspond to Definitions 1.2, 1.2', 1.4, and 1.6 (naïve vs. correct substitution), and support the recursion principle (Principle 1.2).

---

## Summary

This module established:
* **Syntax** of $\lambda$-terms as inductively generated trees (Def. 1.1).
* **Free and bound variables**, scope visualization, and **closed** terms (Defs. 1.2–1.3), with $\mathrm{BV}$ and $\mathrm{Vars}$.
* **$\alpha$-equivalence** (Defs. 1.4–1.5, Thm. 1.2, Lem. 1.1).
* **Naïve vs. capture-avoiding substitution** (Def. 1.6 and example), with properties (Thm. 1.3, Lem. 1.2).
* **Structural induction** (Thm. 1.4, with worked finiteness proof) and **recursion principle** (Principle 1.2).

These are the syntactic foundations. In **Module 2**, we re-express the same notions with De Bruijn indices and locally nameless encodings, and prove reusable substitution/renaming lemmas in a form suitable for mechanized proofs.
