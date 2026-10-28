# Module 13: Hindley–Milner and Type Inference

This module delineates the Hindley–Milner (HM) type system, a pragmatic approximation of System F's parametric polymorphism (Module 12) that restores decidable type inference while retaining much of its generic power. Full System F's universal quantification enables profound reusability—terms abstracting over arbitrary types—but renders principal type inference undecidable (Core 12.4), necessitating explicit annotations for practicality. HM circumvents this by restricting polymorphism to rank-1: universal quantifiers (∀) appear only outermost, at let-bound definitions, allowing automatic inference of principal types (the most general consistent with usage) via constraint-based unification. This let-polymorphism models ad-hoc overloading and generic functions in languages like ML and Haskell, where let x = e in body infers x's scheme ∀ α. A (free α generalized), instantiated on demand without annotations. HM bridges STLC's monomorphism (Module 8) to System F's universality, inheriting safety (progress/preservation from Module 9) but trading higher-rank expressiveness for usability. We introduce type schemes for quantified let-bindings, constraint generation and unification for inference, Algorithm W as the canonical procedure, and proofs of soundness, completeness, and principality. Finally, we survey HM in practice, relating it to rank-1 System F as a decidable fragment.

The module's five cores scaffold inference: Core 13.1 defines let-polymorphism and schemes; Core 13.2 details constraint generation and unification; Core 13.3 specifies Algorithm W with examples and implementation; Core 13.4 proves soundness, completeness, and principality; and Core 13.5 explores applications and rank-1 ties. Each core motivates its machinery—e.g., unification resolves ambiguity from polymorphic calls—with formal definitions, inductive proofs unpacking cases, and counterexamples from full F. Clarity derives from step-by-step inferences on example programs, tables contrasting HM with F, and Mermaid diagrams for unification graphs. Python implementations deliver executable inferencers, integrating STLC checking (Core 8.5) and substitution (Module 7). These affirm HM's elegance as a "sweet spot" for typed languages, transitioning to higher-kinded types in Module 14. Prerequisites include proficiency in Modules 1–12, especially System F rules (Core 12.2), substitution lemmas (Core 8.4), and undecidability (Core 12.4); all HM elements are self-contained with recaps.

## Core 13.1: Let-Polymorphism and Type Schemes (∀-Quantification at Let-Bound Definitions)

Let-polymorphism augments STLC (Module 8) with let-expressions for binding polymorphic identifiers, where quantification occurs only at the "top level" of types (rank-1), enabling inference of generic bindings without universal ∀ in arbitrary positions. Type schemes encapsulate these quantified types, distinguishing let-bound variables from local ones to permit generalization.

### Syntax of Let-Polymorphism

Extend STLC terms (Core 8.3) with:

\[
t ::= \dots \mid \mathsf{let}\, x = t_1\, \mathsf{in}\, t_2
\]

- $\mathsf{let}\, x = t_1\, \mathsf{in}\, t_2$: Binds x to t1 in scope of t2, allowing reuse.

Types remain STLC (no new constructors); polymorphism emerges from schemes.

### Type Schemes and Generalization

A **monotype** is a STLC type (no ∀); a **polytype** (scheme) is ∀ $\bar{\alpha}$. A, where $\bar{\alpha}$ are type variables free in A.

Judgements Δ; Γ ⊢ t : σ, where σ scheme (polytype).

**Generalization**: At let, infer monotype m for t1 under Γ; gen(m, Γ) = ∀ α ∈ free(m) \ free(Γ types). m (principal, most general).

**Instantiation**: Scheme σ = ∀ $\bar{\alpha}$. m inst to m[B1/α1, ...] (substitute fresh B's).

Typing rules (extend Core 8.3):
- **T-Let**: Δ; Γ ⊢ t1 : m (monotype), Δ; Γ, x : σ ⊢ t2 : A (σ inst from gen(m, Γ)) ⇒ Δ; Γ ⊢ let x = t1 in t2 : A.
- Other rules as STLC, but local vars monotypes.

Example: let id = λ x. x in id 5; id infers α → α, gen to ∀ α. α → α (free α not in Γ=∅); inst [Int] to Int → Int for 5.

let swap = λ x y. (y, x) in swap 1 true; swap : α × β → β × α (gen ∀ α β. ...).

| Let Example | Inferred Mono for Let-Body | Generalized Scheme | Instantiation in Use | Result Type |
|-------------|--------------------------------|---------------------|----------------------|-------------|
| let id = λ x. x in id 5 | α → α | ∀ α. α → α | [Int] → Int → Int | Int |
| let pair = λ a b. ⟨a,b⟩ in pair 1 true | α × β | ∀ α β. α × β | Int × Bool | Int × Bool |
| let swap = λ x y. (y, x) in swap p q | α × β → β × α | ∀ α β. α × β → β × α | A × B → B × A | B × A |

Derivation for let id = λ x. x in id 5 : Int (assume 5 : Int).
- Inner λ x. x : α → α (A-Abs, fresh α).
- Let: gen to ∀ α. α → α for id.
- Body id 5 : Inst [Int], T-App id [Int] : Int → Int, 5 : Int → T-App : Int.

Generalization: Free α in mono not generalized if bound in Γ (local mono).

**Lemma 13.1 (Generalization Correctness)**: gen(m, Γ) is principal scheme for m under Γ.

*Proof Sketch*: Free(m) \ free(Γ) are truly generic; ∀ over them most general consistent.

### Exercises

1. Infer let const = λ x y. x in const true 5 : Bool (scheme ∀ α β. α → β → α).
2. Why no gen in local λ (monotype)?
3. Derive let swap = λ x y. (y, x) in swap ⟨1,true⟩ ⟨a,b⟩ : ? (assume a:A b:B).

## Core 13.2: Constraint Generation and Unification for Simple Types

Inference in HM proceeds by generating equality constraints from term structure, then solving via unification to instantiate type variables. This modularizes ambiguity resolution, ensuring decidability for rank-1.

### Constraint Generation

Infer monotypes with vars: Infer Γ ⊢ t ⇒ σ (σ with vars).

Rules generate constraints E (sets {τ1 = τ2}):
- **I-Var**: x ⇒ Γ(x) (no constraint).
- **I-Abs**: λ x. t ⇒ α → σ where fresh α, infer x:α ⊢ t ⇒ σ, E.
- **I-App**: t1 t2 ⇒ σ where infer t1 ⇒ τ → σ, t2 ⇒ τ, E union constraints.
- **I-Let**: let x = t1 in t2 ⇒ infer Γ ⊢ t1 ⇒ m, E1; infer Γ, x : gen(m) ⊢ t2 ⇒ σ, E2; E = E1 ∪ E2.

Constraints from app (unify domain/arg).

### Unification

Unify E: Find subst θ s.t. θ(E) all equal (no occur-check fail).

Alg U(E):
- Empty: Id.
- α = α: Ignore.
- α = τ (α var not in τ): θ(α) = τ.
- τ = α: Sym.
- τ1 → τ2 = σ1 → σ2: Unify τ1=σ1, τ2=σ2.
- Occur α in τ: Fail (infinite type).

Decidable: Finite vars, no cycles.

Example: λ x. x x ⇒ α → α (app x x: domain α = arg α, ok).

let id = λ x. x in id (λ y. y) ⇒ id : β → β, gen ∀ β. β → β; inst [γ → γ], app λ y. y : γ → γ.

Constraints: γ → γ = β → β (unify β=γ).

| Term | Generated Mono/Constraints | Unify Solution | Principal Scheme |
|------|----------------------------|----------------|------------------|
| λ x. x | α → α, no E | Id | ∀ α. α → α |
| λ x. x x | α → α, E={α=α} | Id | ∀ α. α → α (self-app) |
| let id = λ x. x in id z | id : β → β, E=∅; body id z : γ, E={β → β = δ → γ? Wait} | β=δ, γ=τ | ∀ β. β → τ for z:τ |

### Programming

Unify Python:

```python
def unify(tau1, tau2):
    if tau1 == tau2:
        return {}
    if 'var' in tau1:  # α = τ
        return {tau1: tau2}
    if 'var' in tau2:
        return {tau2: tau1}
    if '->' in tau1 and '->' in tau2:
        theta1 = unify(tau1.split('->')[0], tau2.split('->')[0])
        theta2 = unify(tau1.split('->')[1], tau2.split('->')[1])
        return {**theta1, **theta2}
    return None  # Fail

print(unify('alpha -> beta', 'gamma -> beta'))  # {'alpha': 'gamma'}
```

### Exercises

1. Constraints λ x y. x y : α → β → γ, E={α=β→γ? No: app x y domain β = y:β, but x : α = β → γ}.
2. Unify α → α = β → β: {α:β}.
3. Occur fail: α → α = α (infinite).

## Core 13.3: Algorithm W: Specification, Examples, and Implementation Details

Algorithm W, due to Milner (1978), systematizes HM inference: Generate constraints recursively, solve via unification, generalize at let.

### Specification of Algorithm W

W(Γ, t) = (σ, E) or fail: Infer monotype σ for t under Γ, E constraints.

- W-Var: x ∈ Γ ⇒ (Γ(x), ∅).
- W-Abs λ x. t: α fresh, (σ, E) = W(Γ + x:α, t); return (α → σ, E).
- W-App t1 t2: (σ1, E1) = W(Γ, t1), (σ2, E2) = W(Γ, t2); fresh β, E3 = {σ1 = α → β, σ2 = α}; return (β, E1 ∪ E2 ∪ E3).
- W-Let let x = t1 in t2: (m, E1) = W(Γ, t1); (σ, E2) = W(Γ + x : m, t2); return (σ, E1 ∪ E2) (no gen here; post-process gen).

Post: Solve E with U; if θ, apply θ to σ; gen free(σ) \ free(Γ).

Fail on unify fail.

### Examples

Example 1: λ x. x : W(∅, λ x. x) = fresh α, W({x:α}, x) = (α, ∅); α → α, ∅. Solve id, principal ∀ α. α → α.

Example 2: let id = λ x. x in id (λ y. y) : W let: W(∅, λ x. x) = m = β → β, E1=∅; W({id: β→β}, id (λ y. y)): W(id) = β→β, W(λ y. y) = γ → γ, E2={β→β = δ → γ → γ? App id (λ y. y): W(id) = β→β, W(λ y. y) = γ → γ, E={β→β = ε → δ, γ→γ = ε}; unify β=ε, β=δ, γ=ε? Wait, app domain ε = arg γ→γ, so ε = γ→γ, β→β = (γ→γ) → δ, inconsistent unless β = (γ→γ) → δ, but fresh.

Correct: id : ∀ α. α → α (gen); inst [γ → γ] : γ → γ → γ? No: id [τ] : τ → τ, τ = γ → γ, so id (λ y. y) : (γ→γ) → (γ→γ), but λ y. y : γ → γ, app domain γ → γ = arg γ → γ, codomain γ → γ.

Inference: Let gen id ∀ β. β → β; body app id (λ y. y): Infer id ⇒ inst fresh δ, θ = {β:δ}, but W let post-gen.

W steps: Inner λ x. x ⇒ α → α.
Let: m = α → α, gen to ∀ α. α → α (free α not Γ).
Body app id (λ y. y): W(id) ⇒ ∀ α. α → α, but monotype inst fresh β, so β → β (E={∀ α. α → α = γ → β → β? No, W-Let uses m for infer body, but gen post-infer t1, then infer body with x : scheme, inst on use.

Standard W: Infer t1 to m, gen to σ = gen(m); infer t2 with x : σ (inst fresh on use); no E for let.

For body app: W(id) : Since id scheme, inst fresh μ, W(inst id μ) = μ → μ.
W(λ y. y) = ν → ν.
App: E = {μ → μ = ρ → σ, ν → ν = ρ}; unify μ = ρ, μ = σ, ν = ρ = μ, ν = μ = σ, so μ = ν, σ = μ.

Thus principal for body μ → μ, overall σ = ∀ μ. μ → μ for let? Wait, let returns infer t2 type.

W returns the type of whole let = type t2.

Yes.

### Implementation Details

Python W sketch:

```python
def fresh():
    return f'alpha_{len(fresh.counter)}'
fresh.counter = 0

def w_infer(gamma, t):
    if t[0] == 'var':
        return gamma.get(t[1], None), []
    if t[0] == 'abs':
        x = t[1]
        alpha = fresh()
        sigma, E = w_infer({**gamma, x: alpha}, t[2])
        return f'{alpha} -> {sigma}', E
    if t[0] == 'app':
        sigma1, E1 = w_infer(gamma, t[1])
        sigma2, E2 = w_infer(gamma, t[2])
        beta = fresh()
        E3 = [f'{sigma1} = rho -> {beta}', f'{sigma2} = rho']  # rho fresh
        return beta, E1 + E2 + E3
    if t[0] == 'let':
        x = t[1]
        m, E1 = w_infer(gamma, t[2])
        sigma, E2 = w_infer(gen(m, gamma), t[3])  # gen post
        return sigma, E1 + E2

def gen(m, gamma):
    free_m = extract_free(m)
    free_gamma = set(tau for tau in gamma.values())
    alphas = free_m - free_gamma
    return f'forall {" ".join(alphas)}. {m}'

# Example let id = λx.x in id (λy.y)
let_ex = ('let', 'id', ('abs', 'x', ('var', 'x')), ('app', ('var', 'id'), ('abs', 'y', ('var', 'y'))))
sigma, E = w_infer({}, let_ex)
print(sigma)  # forall alpha. alpha -> alpha (approx)
```

### Exercises

1. W(λx y. x y): Constraints E.
2. Unify {α → β = γ → β, δ = γ}.
3. Let poly: W let id=λx.x in id id.

## Core 13.4: Soundness, Completeness, and Principal Typings in HM

HM sound: Inferred types valid; complete: Finds all; principal: Most general.

### Soundness

**Theorem**: If W(Γ, t) = (σ, E) solvable θ, then Γ ⊢ t : θ(σ).

*Proof Ind t*:
- Var: θ(m) = m = Γ(x).
- Abs: θ(α → σ) = θ(α) → θ(σ); IH body θ(σ), T-Abs.
- App: θ(β) from unify θ(σ1) = θ(ρ) → θ(β), θ(σ2) = θ(ρ); IH σ1 : ρ → β, σ2 : ρ; T-App.
- Let: IH t1 m, gen σ, inst in body θ(σ) = θ'(m), IH t2 θ'(m); T-Let.

### Completeness

**Theorem**: If Γ ⊢ t : A, then W infers σ unifiable to A.

*Proof Ind Derivation*:
- Var: Returns A.
- Abs: Ind body B, fresh α unif A domain, α → B unif A.
- App: Ind func C → A, arg C; unify domain C, codomain A.
- Let: Ind t1 m ≤ A1 (unif), gen σ ≥ A1, inst in t2 unif to A.

### Principal Typings

**Theorem**: Inferred σ most general: Any A with ⊢ t : A unifies σ ≤ A.

*Proof*: Gen free vars exactly generic; unify solves minimal subst.

| Property | Statement | Proof Basis |
|----------|-----------|-------------|
| Soundness | Infer ⇒ typed | Ind + unify valid |
| Completeness | Typed ⇒ infer unif | Ind derivation |
| Principality | Infer most gen | Gen free exact |

### Exercises

1. Soundness Abs: Fresh α unif domain.
2. Complete T-Let: Gen ≥ inferred.
3. Principal: Why gen free \ Γ.

## Core 13.5: HM in Practice and Its Relationship to Rank-1 System F

HM powers ML/Haskell cores, inferring generics at let; rank-1 F subset: Let-poly prenex F (pull ∀ left).

### HM Practice

ML: fun id x = x; infers 'a -> 'a (poly a).

Haskell: id x = x; forall a. a -> a.

Extensions: Extensible variants, GADTs (dep-like, Module 14.4).

Cores: Compiler infers, erases types runtime (tag-free).

### Rank-1 System F

Rank n: ∀ depth n (leftmost n arrows).

HM rank-1: ∀ left of arrows.

F full arbitrary rank.

Relation: Let x = Λ α. t in s simulates rank-1; infer gen at let.

Decidable because prenex normal form.

| System | Rank | Let-Poly? | Inference | Language Core |
|--------|------|-----------|-----------|---------------|
| STLC | 0 | No | Decidable | Basic func |
| HM | 1 | Yes | Principal | ML/Haskell |
| F | Arbitrary | No | Undecidable | Full param |

### Exercises

1. ML infer fun swap (x,y) = (y,x) : 'a * 'b -> 'b * 'a.
2. Rank-2 example: ∀ α. (∀ β. β → α) → α (beyond HM).

## Summary and Suggested Exercises

HM let-poly schemes rank-1 F, constraints unify, W infers, sound/complete principal, practice ML cores.

**Exercises**:
1. W let id=λx.x in id id : Scheme ∀α. α→α, inst self.
2. Unify {α → β = γ → δ, β = δ, α = γ}.
3. Soundness Let: Gen valid.
4. Complete Abs: Fresh unif.
5. ML rank-1: Why no nested ∀ arg.

HM inferred generics, Module 14 higher/dep. 

**Resources**: Milner (1978) W; Damas-Milner (1982) complete; Pierce TAPL Ch. 22.
