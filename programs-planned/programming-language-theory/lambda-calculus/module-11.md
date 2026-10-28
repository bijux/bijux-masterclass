# Module 11: Recursive Types and General Recursion

This module incorporates recursive types into the Simply Typed λ-Calculus (STLC) framework established in Modules 8 and 9, thereby restoring the ability to define inductive data structures—such as natural numbers, lists, and trees—that support general-purpose recursion while retaining essential safety guarantees like progress and preservation. The untyped λ-calculus (Modules 1–3) permits arbitrary recursion via fixed-point combinators (Core 5.3), but at the cost of potential divergence and stuck states (Module 6.4). STLC's strong normalization (Core 9.4) precludes such risks, yet limits expressiveness to terminating computations, rendering it inadequate for practical data manipulation. Recursive types resolve this by permitting type-level fixed points, allowing types to refer to themselves, but introduce new challenges: explicit administrative reductions for unfolding and a loss of strong normalization, necessitating alternative metatheoretic tools like domain theory (previewed in Module 15.3) to interpret non-terminating behaviors soundly.

We distinguish two paradigms: iso-recursive types, which employ explicit roll and unroll operations to inject and project recursive structures, ensuring decidable equality through syntactic distinction; and equi-recursive types, which treat the recursive type as definitionally equivalent to its unfolding, enabling seamless recursion via coinductive equality but demanding careful handling of infinite type graphs. Operational semantics extend the small-step relations of Module 6 with fold/unfold redexes, while typing rules integrate these constructors into the STLC system of Core 8.3, preserving substitution invariance (Core 8.4) and leveraging explicit substitutions from Module 7 for efficient propagation. Metatheoretically, type safety endures—typed terms remain well-behaved under reduction—but strong normalization dissipates, as embedded fixed points (Module 10.1) permit loops; we delineate this failure and provide a domain-theoretic resolution, viewing recursive types as initial algebras in complete partial orders. Finally, we survey realizations in real languages, where algebraic datatypes and catamorphisms (folds) operationalize recursion safely, linking to polymorphic encodings in Module 12.3.

The module's five cores build recursively: Core 11.1 elucidates iso-recursive μ-types with roll/unroll, exemplified by lists and trees; Core 11.2 contrasts equi-recursive equality and cycle detection in type graphs; Core 11.3 formalizes operational and typing rules for μ-types; Core 11.4 proves safety, demonstrates SN loss, and introduces domain readings; and Core 11.5 examines practical implementations via algebraic datatypes and folds/unfolds. Each core motivates its innovations—e.g., iso's explicitness aids decidability—through formal statements, inductive proofs with unpacked cases, and counterexamples from untyped or non-recursive settings. Explanations interweave semantic intuitions (e.g., μX.A as least solution to X = A[X]) with syntactic details, ensuring accessibility. Depth accrues via exhaustive reduction traces on recursive examples, comparative tables of iso/equi trade-offs, and Mermaid diagrams for type unfoldings and computation graphs. Python prototypes simulate μ-typed evaluation and unfolding, incorporating typed substitution (Module 8.4) and reduction (Module 6) for verification. These elements collectively illuminate recursive types' elegance and subtleties, transitioning to System F's parametric recursion in Module 12. Prerequisites demand proficiency in Modules 1–10, including STLC metatheory (Module 9), PCF fixed points (Core 10.1), and explicit substitution propagation (Module 7.3); all recursive extensions are self-contained with recaps.

## Core 11.1: Iso-Recursive Types: μ-Types with Roll/Unroll, Examples (Lists, Trees)

Iso-recursive types explicitly encode recursion through the μ-constructor, binding a type variable X in A to the μ-type itself, with dedicated roll and unroll terms to embed and extract inhabitants. This approach, pioneered by Morris (1970) and refined in Fω (Module 14.1), ensures type equality is decidable via syntactic unfolding, avoiding the coinductive subtleties of equi-recursive variants (Core 11.2), but introduces administrative redexes—roll/unroll pairs that reduce to inner terms—mirroring the explicit substitutions of Module 7. Such types enable the definition of inductive structures like natural numbers (as least solutions to X = 1 + X) and lists (X = 1 + A × X), facilitating recursive processing without compromising decidable checking (Core 8.5).

### Syntax of Iso-Recursive Types and Terms

The types $\mathcal{T}_\mu$ extend STLC types (Core 8.1) with recursion:

\[
A ::= B \mid A \to A \mid \mu X. A
\]

Here, X ranges over type variables (fresh, not free in outer scope), and μX.A binds X in A, forming a finite tree with a self-reference at leaves. Terms $\Lambda_\mu$ extend STLC terms (Core 8.3) with:

- $\mathsf{roll}\, t$ provided $t : A[\mu X.A / X]$.
- $\mathsf{unroll}\, t$ provided $t : \mu X.A$, yielding type $A[\mu X.A / X]$.

Free type variables FT(A) exclude bound X; free term variables FV(t) as Module 1.2, treating roll/unroll as neutral (no binders).

Examples:
- Natural numbers: $\mathsf{Nat} \equiv \mu X. 1 + X$ (Core 9.5 unit 1, sum +).
  - zero $\equiv \mathsf{roll}\, \mathsf{inl}\, *$ : Nat (inl from sum intro, * unit).
  - succ n $\equiv \mathsf{roll}\, \mathsf{inr}\, n$ : Nat (inr right sum).
- Lists over A: $\mathsf{List}\, A \equiv \mu X. 1 + A \times X$ (product × from Core 9.5).
  - nil $\equiv \mathsf{roll}\, \mathsf{inl}\, *$ : List A.
  - cons a l $\equiv \mathsf{roll}\, \mathsf{inr}\, \langle a, l \rangle$ : List A (⟨,⟩ pair).

Trees: $\mathsf{Tree}\, A \equiv \mu X. 1 + A \times X \times X$ (binary, leaves 1, nodes value + children).

These unfold to infinite signatures: Nat = 1 + 1 + 1 + ..., List A = 1 + A × 1 + A × A × 1 + ...

| Type | μ-Form | Roll for Base | Roll for Rec | Unroll Yields | Unfolding |
|------|--------|---------------|--------------|---------------|-----------|
| Nat | μX. 1 + X | roll inl * = zero | roll inr n = succ n | 1 + Nat | Finite trees of + |
| List A | μX. 1 + A × X | roll inl * = nil | roll inr ⟨a, l⟩ = cons a l | 1 + A × List A | Infinite spine |
| Tree A | μX. 1 + A × X × X | roll inl * = leaf | roll inr ⟨a, l, r⟩ = node a l r | 1 + A × Tree A × Tree A | Branching infinite |

### Typing Rules for Roll and Unroll

The rules integrate seamlessly with STLC (Core 8.3), preserving uniqueness (Core 8.5):

- **T-Roll**: If $\Gamma \vdash t : A[\mu X.A / X]$, then $\Gamma \vdash \mathsf{roll}\, t : \mu X.A$.
  - Ensures injection matches the recursive unfolding; X substituted conservatively.

- **T-Unroll**: If $\Gamma \vdash t : \mu X.A$, then $\Gamma \vdash \mathsf{unroll}\, t : A[\mu X.A / X]$.
  - Projects to the body, enabling case analysis on constructors.

Freshness: X not free in $\Gamma$; substitution as Core 8.4, preserving types.

Derivation for succ zero : Nat.
- * : 1 (T-Unit, Core 9.5).
- inl * : 1 + Nat (T-Inl, assuming + rules extended).
- roll inl * : μX.1 + X = Nat (T-Roll, A=1 + X, t=inl * : 1 + μX.1 + X? Wait, 1 + X [μ/ X] = 1 + μ, yes).
- Inner n = roll inl * : Nat.
- inr n : Nat + Nat? No: inr n : 1 + Nat with Nat=μ (T-Inr).
- roll inr n : μX.1 + X = Nat (T-Roll).

Unroll Nat → 1 + Nat, case to zero/succ.

**Lemma 11.1 (Substitution for Recursive Types)**: If $\Gamma, X : \mu X.A \vdash t : B[\mu X.A / X]$, then $\Gamma \vdash t : B[\mu X.A / X]$.

*Proof*: Extend Core 8.4; ind derivation, X type var like term var, but types.

Ensures roll/unroll type-safe.

### Programming Representation

Python simulation of roll/unroll (tagged unions for μ):

```python
class MuType:
    def __init__(self, body):
        self.body = body  # A with X

class Roll:
    def __init__(self, t):
        self.t = t

class Unroll:
    def __init__(self, t):
        self.t = t

def type_check_roll(t, mu_type):
    # Simulate A[μ/X] check
    return isinstance(t, (Roll,))  # Placeholder

def reduce_roll_unroll(term):
    if isinstance(term, Unroll) and isinstance(term.t, Roll):
        return term.t.t  # Unroll roll → inner
    return term

# Example Nat zero = Roll(Inl(Unit()))
zero = Roll('inl *')
unzero = Unroll(zero)
print(reduce_roll_unroll(unzero))  # 'inl *'
```

### Exercises

1. Full derivation roll inr ⟨a, nil⟩ : List A.
2. Type unroll cons a nil → A × List A.
3. Lemma sub for T-Roll: Why fresh X.

## Core 11.2: Equi-Recursive Types and Type Equality; Cycles in Type Graphs

Equi-recursive types dispense with explicit roll/unroll, treating μX.A definitionally equal to its unfolding A[μX.A / X], via coinductive equality that permits infinite approximations. This paradigm, favored in languages like Haskell for seamless recursion, contrasts iso-recursive's administrative burden but requires coinduction to handle cyclic definitions, modeled as graphs where types are nodes and recursive occurrences edges.

### Syntax and Coinductive Equality

Syntax identical to iso: A ::= ... | μX. A. Terms as STLC (no roll/unroll); recursion implicit via self-reference in bodies.

Equality ≅ is the largest relation closed under:
- μX.A ≅ A[μX.A / X] (unfold axiom).
- Congruence: If A ≅ A', B ≅ B', A → B ≅ A' → B'; base equal.
- Coinductive: If R relates A B, R coinductive (infinite unfold match).

Decidable via guardedness: X occurs under → (productive), finite approx check.

Example: Nat ≅ 1 + Nat (unfold); equality holds coinductively (infinite 1 + 1 + ... match).

List A ≅ 1 + A × List A.

Cycles: Type graph G(A) nodes sub-types, directed edges from A to occurrences of X in body. Recursive if self-cycle; equality if graph-isomorphic solutions.

| Paradigm | Explicit Constructors? | Equality | Decidable? | Infinite Unfold |
|----------|------------------------|----------|------------|-----------------|
| Iso | Yes (roll/unroll) | Syntactic + admin redex | Yes (finite) | Via repeated unroll |
| Equi | No | Coinductive unfold | Yes (guarded) | Direct ≅ chain |

Graph for Nat: Node Nat → 1 + Nat (edge Nat to Nat via + right).

Equality: Bisimilar graphs (match unfold trees).

**Lemma 11.2 (Coinductive Transitivity)**: ≅ transitive.

*Proof*: Coinduction principle: If R ⊆ ≅ and R coind (unfold preserves R), then R ⊆ ≅. For trans A ≅ B ≅ C, R = {(A,C)}; unfold A R B, B ≅ C ⇒ unfold B R C by cong, coind.

Guardedness ensures termination: Unfold depth bounded by productivity.

### Exercises

1. Unfold List A 3 times; show ≅ infinite.
2. Graph Tree A: Cycles? (Self left/right).
3. Why guarded (X under →) for decid (no immediate cycle).

## Core 11.3: Operational Semantics and Typing Rules for μ-Types and Recursive Data

Operational semantics for recursive types amalgamates βη (Module 3) with administrative reductions for iso (roll/unroll) or implicit unfolding for equi, while typing rules embed μ into STLC (Core 8.3), ensuring compatibility with substitution (Core 8.4) and explicit propagation (Module 7.3). These enable recursive data like lists, with operations (head, tail, fold) typed structurally.

### Operational Semantics: Admin Redexes and Unfolding

For iso-recursive:
- Extend small-step (Module 6.1): unroll (roll t) → t; roll (unroll t) → t (βμ admin).
- Contexts admit μ: C ::= ... | C roll | unroll C (congruence).

For equi: No admin; reduction as STLC, but equality permits unfold in typing/equivalence checks (coind).

Example Nat iso: unroll (succ zero) = unroll (roll inr (roll inl *)) → inr (roll inl *) (unroll roll) → inr inl * (unroll inner? No, inr neutral).

For list head: Assume match (unroll l) { inl _ → error | inr ⟨a, _⟩ → a } : A + 1 → A (error unit or empty).

Equi: head l = match l with nil → error | cons a _ → a, where l : List A = 1 + A × List A definitionally.

Typing same for both: T-Fold/T-Unfold as T-Roll/Unroll (Core 11.1).

For data:
- Lists: nil : List A, cons a l : List A (a : A, l : List A).
- Ops: isNil l : Bool = iszero (length l) encoded, or match.

Full rec data: Trees node a left right : Tree A.

Semantics preserve via congruence (Lemma 11.1 sub).

### Typing Rules for Recursive Data

Rules uniform:
- T-Nil: Γ ⊢ nil : List A (for any A).
- T-Cons: Γ ⊢ a : A, Γ ⊢ l : List A ⇒ Γ ⊢ cons a l : List A.
- T-Head: Γ ⊢ l : List A ⇒ Γ ⊢ head l : A + 1 (error unit).
- T-CaseList: Γ ⊢ l : List A, Γ ⊢ n : C, Γ,a:A,l':List A ⊢ c : C ⇒ Γ ⊢ case l nil n (λa l'. c) : C.

Similar trees.

| Data Op | Typing Premise | Conclusion Type | Reduction |
|---------|----------------|-----------------|-----------|
| cons a l | a : A, l : List A | List A | Neutral |
| head l | l : List A | A + 1 | Case on unroll/fold |
| case l n c | l : List A, n : C, c : C | C | Match inl/inr |

Example derivation cons a nil : List A.
- nil : List A (T-Nil).
- a : A (assume).
- T-Cons: cons a nil : List A.

Semantics: head (cons a nil) = case (unroll cons...) inr ⟨a,nil⟩ → a (elim).

Equi: No unroll, case directly on cons (equality unfolds).

### Programming Representation

Iso rec sim Python (tagged):

```python
class MuRec:
    def __init__(self, body_type):
        self.body_type = body_type

class Roll:
    def __init__(self, inner):
        self.inner = inner

class Unroll:
    def __init__(self, rec):
        self.rec = rec

def reduce_rec(term):
    if isinstance(term, Unroll) and isinstance(term.rec, Roll):
        return term.rec.inner
    return term

# Nat
class NatMu(MuRec):
    pass

zero = Roll('inl *')
succ_zero = Roll('inr zero')
print(reduce_rec(Unroll(succ_zero)))  # 'inr zero'
```

### Exercises

1. Typing head cons a nil → a.
2. Reduce case unroll cons ... → a.
3. Equi head: How without unroll (match pattern).

## Core 11.4: Metatheory: Type Safety, Loss of Strong Normalization, Domain-Theoretic Reading

Recursive types inherit STLC safety (Module 9.2–9.3) but sacrifice strong normalization (SN), admitting divergence akin to untyped fix (Module 5.3); domain theory restores soundness by interpreting μ as least fixed points in CPOs (Module 15.1).

### Type Safety: Extended Progress and Preservation

Safety extends: Well-typed closed t : μX.A value or →.

**Theorem 11.2 (Progress for Recursive Types)**: If ∅ ⊢ t : A (A recursive), t value or ∃u t → u.

*Proof by Induction on Typing Derivation, Cases on Form*:
- T-Roll: t = roll s, s : B[μX.B/X]. IH s value or s → s'; roll value or roll s → roll s' (congruence).
- T-Unroll: t = unroll s, s : μX.B. If s value, canonical (extend 9.1): s = roll r ⇒ unroll roll r → r (admin β, progress). If s → s', unroll s → unroll s' (congruence).
- Other STLC rules as Module 9.2 (ind).

Preservation: t → u, ⊢ t : A ⇒ ⊢ u : A.

*Proof Ind Typing + Cases →*:
- Roll t → roll u: IH t → u preserves B[μ/X]; T-Roll u : μ.
- Unroll roll r → r: ⊢ roll r : μ, ⊢ r : B[μ/X] by T-Roll premise; matches.
- Congruence: As 9.3, contexts preserve.

No stuck: Typing ensures roll inner matches unfold, unroll on roll admin.

### Loss of Strong Normalization

**Theorem 11.3**: Recursive STLC not SN.

*Proof*: Embed PCF fix (Core 10.1): fix f = f (fix f), type (A→A) → A→A if f loops (e.g., f = λg. g g self). Infinite unfold.

Contrast STLC SN (Core 9.4): No rec, no loops.

### Domain-Theoretic Reading

Interpret μX.A as initial F-algebra, where F(X) = A[X] endofunctor on CPO category (Module 15.1).

Denotation [[μX.A]] = colim {D0 = 1 (terminal), D_{i+1} = [[A[D_i / X]]] }, least fixed point lfp F.

[[roll t]] = η : [[A[μ]]] → μ (unit of colim).

[[unroll t]] = ε : μ → [[A[μ]]] (counit).

Cat eqs: ε η = id, natural. Sound: unroll roll = id.

For divergence: ⊥ in CPO, lfp includes non-strict funcs (apply ⊥ = ⊥).

SN loss: lfp has ⊥-loops, but safety: Typed ops continuous, preserve ⊥.

| Property | Recursive | STLC (M9) | Domain Fix |
|----------|-----------|-----------|------------|
| Progress | Yes | Yes | Colim inj/pro |
| Preservation | Yes | Yes | Natural trans |
| SN | No | Yes | lfp ⊥-infinite |

### Programming

Domain approx Python (iterate F):

```python
def domain_iter(F, init=0, steps=5):
    D = init
    for _ in range(steps):
        D = F(D)
    return D  # Approx lfp

def F_list_A(D):
    return 1 + A * D  # Symbolic

# Nat approx: F(X) = 1 + X, iter 1, 1+1=2, 1+2=3, ... approx ℕ
print(domain_iter(lambda d: 1 + d, 0, 3))  # 3 (approx)
```

### Exercises

1. Progress unroll non-roll: Congruence.
2. Preservation roll inner step.
3. Embed fix: Type (A→A)→A, infinite.
4. Domain chain Nat step 3: 1 + (1 + (1 + 1)).

## Core 11.5: Recursive Types in Real Languages and Typed IRs (Algebraic Datatypes, Folds/Unfolds)

Recursive types underpin algebraic datatypes (ADTs) in functional languages, with folds (catamorphisms) for consumption and unfolds for generation, typed to ensure totality where possible.

### Algebraic Datatypes in Languages

Haskell: data Nat = Zero | Succ Nat; deriving Eq (auto ops).

ML: datatype Nat = Zero | Succ of Nat.

Typing: Zero : Nat, Succ n : Nat.

IR: Typed assembly with constructors/tags, jumps for cases.

### Folds and Unfolds

Fold (catamorphism): Rec deconstruct to base.
- fold_Nat : (1 → B) → (Nat → B) → Nat → B.
- fold zero z s = z; fold (succ n) z s = s (fold n z s).

Unfold (anamorphism): Rec build from seed.
- unfold_Nat : (B → 1 + B) → B → Nat.
- Builds tree from co-rec seed.

Real: Haskell foldr :: (a → b → b) → b → [a] → b; total if strict.

Typed IR: FOLD instr with visitor func, UNROLL with generator.

| Lang/IR | ADT Decl | Fold Syntax | Unfold | Safety |
|---------|----------|-------------|--------|--------|
| Haskell | data Nat = Z | foldr s z n | unfoldr g seed | Totality optional |
| ML | datatype Nat = Z | rec fold ... | — | Pattern match exhaust |
| Typed IR | tag Zero | FOLD visitor | UNROLL gen | Stack-safe rec |

Example Haskell foldr (+) 0 [1,2,3] = 6; typed (Num a) ⇒ a.

IR: PUSH seed; UNROLL gen → Nat on stack.

### Exercises

1. Haskell fold_Nat z s (Succ (Succ Zero)) = s (s z).
2. Typed IR FOLD for sum list.
3. Why folds total if visitor strict.

## Summary and Suggested Exercises

Recursive types restore data/rec: Iso explicit roll/unroll, equi coind graphs, ops/typing fold/unfold, safety yes SN no domains, real ADTs folds.

**Exercises**:
1. Type fold_List : ... → List A → B.
2. Reduce unroll succ zero → inr inl *.
3. Equi unfold implicit: How in typing.
4. Preservation T-Unroll.
5. Domain lfp F(X) = 1 + X approx 4 steps.

Rec foundation, Module 12 F param. 

**Resources**: Rehof/Thiemann (2000) rec types; Sheard/Moore (1998) folds; Jones (1990) ADTs.
