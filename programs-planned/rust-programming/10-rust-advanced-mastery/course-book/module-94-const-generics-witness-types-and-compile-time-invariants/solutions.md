# Module 94 Solutions — Const Generics, Witness Types, and Compile-Time Invariants

[Workbook](workbook.md) · [Chapter](index.md) · [AxiomStore guide](../capstone.md)

These are reasoned reference answers. Compare your predicted phase, invariant owner, and failure state before comparing syntax. A different implementation is stronger when it preserves the same contract with a smaller proof surface.

## Part 1 — Prediction

### Prediction 1 — Matrix multiplication

The composition is rejected at type checking because `3` and `4` are different type-level values.

### Prediction 2 — Capacity versus length

The type fixes capacity and storage shape. Initialization of exactly three slots is a runtime invariant; the other five must not be read as `T`.

### Prediction 3 — Forgeable witness

No. Callers can construct out-of-range values, so the witness no longer carries validated evidence.

### Prediction 4 — Zero capacity

It is always full, rejects every pushed value, yields an empty slice, and drops no elements. Zero must be designed, not treated as impossible.

## Part 2 — Diagnose and repair

Judge every repair against the static/dynamic invariant table: the decisive relationship must become clearer, not disappear behind cloning, erasure, broad bounds, visibility, unchecked construction, or deleted validation.

### Repair 1 — Every configuration becomes const

**Causal defect.** A service exposes user-selected batch sizes as public const parameters across its API.

**Principled repair.** Keep runtime policy dynamic unless callers need type-level composition or representation specialization. A small private specialization layer may bridge the two.

A strong answer updates the static/dynamic invariant table and includes a negative case that fails for the original cause.

### Repair 2 — Witness constructor unchecked

**Causal defect.** A private-field witness has a public `new_unchecked` safe constructor.

**Principled repair.** Make unchecked construction unsafe/private or remove it. Safe constructors must establish the carried predicate.

A strong answer updates the static/dynamic invariant table and includes a negative case that fails for the original cause.

### Repair 3 — Const arithmetic assumed infallible

**Causal defect.** A matrix constructor multiplies dimensions without checked arithmetic because dimensions are consts.

**Principled repair.** Validate overflow where stable const expressions cannot encode the required proof; const knowledge does not make `usize` multiplication mathematically unbounded.

A strong answer updates the static/dynamic invariant table and includes a negative case that fails for the original cause.

## Part 3 — Focused exercises

### Exercise 1 — Shape-checked multiplication

The construction should answer: Implement matrix multiplication with type-equal inner dimensions.

The decisive acceptance criterion is: Incompatible shapes fail before runtime and valid shapes match a dynamic oracle.

Evaluate the result through the static/dynamic invariant table; helper names may differ, but the invariant owner and adversarial case must be explicit.

### Exercise 2 — Witness API

The construction should answer: Build `BoundedIndex<N>` with private representation and boundary tests.

The decisive acceptance criterion is: The first invalid index is rejected for multiple `N`, including zero.

Evaluate the result through the static/dynamic invariant table; helper names may differ, but the invariant owner and adversarial case must be explicit.

### Exercise 3 — Hybrid capacity design

The construction should answer: Compare inline fixed capacity with a dynamic `Vec` implementation.

The decisive acceptance criterion is: The decision identifies a real storage/composition requirement rather than style.

Evaluate the result through the static/dynamic invariant table; helper names may differ, but the invariant owner and adversarial case must be explicit.

### Exercise 4 — Instantiation budget

The construction should answer: List all const values used by a sample application and inspect the compatibility implications.

The decisive acceptance criterion is: The report identifies unnecessary public instantiation freedom.

Evaluate the result through the static/dynamic invariant table; helper names may differ, but the invariant owner and adversarial case must be explicit.

### Cross-course transfer

Full credit may conclude that **Const Generics, Witness Types, and Compile-Time Invariants** should not be retrofitted into the earlier artifact. The comparison must identify the current owner, the proof benefit, maintenance cost, and a concrete failure that would change.


### Applied case study — static capacity versus runtime policy

The embedded inline capacity is a compile-time representation choice and can be expressed as `Batch<T, N>`. Array length, full-versus-not-full transitions, and a `BoundedIndex<N>` witness can exclude indexing beyond the initialized capacity. The configured server limit is external data; it should be validated once into a private `RuntimeLimit` and enforced at admission. Encoding it as a const generic would require a new type and usually a new monomorphization for every configured value, even though the value is not known at compilation.

A witness constructor `BoundedIndex::<N>::new(i)` can prove `i < N` before the unchecked-looking indexing operation. `N = 0` remains a valid type: construction of an index always fails and insertion immediately reports full. This is clearer than hiding a special nonzero assumption in unsafe code.

Public `N` becomes part of type identity. Changing a default or returning a different capacity can break inference and downstream signatures, and many capacities can increase code size. The server policy therefore should not leak into the public type unless callers genuinely need type-level distinction.

The combined component should define one explicit effective rule. For example, inline storage may be a staging optimization of size 32 while the runtime admission limit controls total accepted work. A test with limits 1, 32, and 33 must show that admission rejects at the runtime threshold and that staging flushes safely when its independent inline capacity is reached. Conflating the two numbers would make a performance representation accidentally own product policy.

## Part 4 — Independent laboratory

A complete [Bounded Matrix](../../labs/module-04-bounded-matrix/README.md) satisfies its public contract and makes the static/dynamic invariant table inspectable. The reference implementation is not canonical; compare accepted input, rejected input, state after failure, ownership/lifetime surface, deterministic behavior, and extension authority in that order.

Build a fixed-shape matrix and nonforgeable bounded indices, then redesign one API whose dimensions belong at runtime rather than in type identity.

The transfer variant for Bounded Matrix must alter at least two substantive dimensions and preserve an independent oracle; a domain-name substitution is not evidence of mastery.

## Part 5 — Capstone transfer

Defend `MAX_RECORD` and `TX_CAP` separately. Document what each const controls, what runtime state remains, zero/maximum behavior, expected instantiations, and the simpler dynamic alternative.

A strong capstone change keeps the responsibility described by the static/dynamic invariant table local. Reject any design that spreads the mechanism across unrelated AxiomStore modules without a named requirement.

## Part 6 — Reconstruct and defend

For every const parameter, answer: what downstream composition does it enable, what mutable state is still required, and what compatibility or code-generation cost does it create?

The defense passes when it reconstructs the static/dynamic invariant table from the requirement, shows a causal rejected construction, compares a simpler alternative, maps evidence, and names residual risk. Terminology without that chain is not mastery.
