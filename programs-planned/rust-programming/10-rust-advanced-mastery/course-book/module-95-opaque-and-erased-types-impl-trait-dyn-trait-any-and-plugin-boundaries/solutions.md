# Module 95 Solutions — Opaque and Erased Types: impl Trait, dyn Trait, Any, and Plugin Boundaries

[Workbook](workbook.md) · [Chapter](index.md) · [AxiomStore guide](../capstone.md)

These are reasoned reference answers. Compare your predicted phase, invariant owner, and failure state before comparing syntax. A different implementation is stronger when it preserves the same contract with a smaller proof surface.

## Part 1 — Prediction

### Prediction 1 — Different opaque branches

The branches have different concrete iterator types. Return-position `impl Trait` hides one concrete type, not an arbitrary union.

### Prediction 2 — Generic object method

The generic method cannot be represented by one finite vtable entry for all future `T`; it must be excluded from object use, moved outside, or redesigned.

### Prediction 3 — Ownership choice

`Box` expresses unique ownership and is sufficient. `Arc` adds shared atomic liveness without a requirement.

### Prediction 4 — Any as protocol

The repeated conceptual operation indicates a missing behavioral trait. `Any` supplies identity and mismatch, not the validation protocol.

## Part 2 — Diagnose and repair

Judge every repair against the erasure ledger: the decisive relationship must become clearer, not disappear behind cloning, erasure, broad bounds, visibility, unchecked construction, or deleted validation.

### Repair 1 — Erasing the lending codec

**Causal defect.** A lifetime-indexed codec is forced behind one trait object solely for architectural uniformity.

**Principled repair.** Keep the codec static/GAT-based and erase only runtime validator policy. Variation axes need not share one mechanism.

A strong answer updates the erasure ledger and includes a negative case that fails for the original cause.

### Repair 2 — Enum used for open plugins

**Causal defect.** An application must accept third-party validators but models them as a public exhaustive enum.

**Principled repair.** Use a dyn-compatible trait registry or another open extension boundary; the enum gives extension authority to the defining crate.

A strong answer updates the erasure ledger and includes a negative case that fails for the original cause.

### Repair 3 — Arc selected by habit

**Causal defect.** Every dynamic component is stored in `Arc` even though ownership is unique.

**Principled repair.** Choose ownership from liveness and sharing first. Dynamic dispatch works through borrowed or boxed values too.

A strong answer updates the erasure ledger and includes a negative case that fails for the original cause.

## Part 3 — Focused exercises

### Exercise 1 — Opaque unification

The construction should answer: Repair two opaque iterator branches with an enum adapter, boxed iterator, and one common pipeline.

The decisive acceptance criterion is: The comparison identifies retained information, allocation, and API cost.

Evaluate the result through the erasure ledger; helper names may differ, but the invariant owner and adversarial case must be explicit.

### Exercise 2 — Dyn audit

The construction should answer: Audit a trait containing associated types, generic methods, constructors, and consuming receivers.

The decisive acceptance criterion is: Every object-usable and object-excluded method is justified.

Evaluate the result through the erasure ledger; helper names may differ, but the invariant owner and adversarial case must be explicit.

### Exercise 3 — Closed/open pair

The construction should answer: Implement the same semantic operations with an enum and a trait-object registry.

The decisive acceptance criterion is: Tests share one oracle; extension authority differs explicitly.

Evaluate the result through the erasure ledger; helper names may differ, but the invariant owner and adversarial case must be explicit.

### Exercise 4 — Typed context

The construction should answer: Build a small `Any` context with duplicate and mismatch policy.

The decisive acceptance criterion is: The result documents why it is not a behavioral plugin interface.

Evaluate the result through the erasure ledger; helper names may differ, but the invariant owner and adversarial case must be explicit.

### Cross-course transfer

Full credit may conclude that **Opaque and Erased Types: impl Trait, dyn Trait, Any, and Plugin Boundaries** should not be retrofitted into the earlier artifact. The comparison must identify the current owner, the proof benefit, maintenance cost, and a concrete failure that would change.


### Applied case study — preserving a stable plugin boundary

The built-in set is closed and selected by the library, so a generic or enum representation is appropriate. The plugin set is open, selected by the host at runtime, and heterogeneous in one registry, so erasure is justified there. The minimal erased contract needs a stable `name(&self) -> &'static str` and a method such as `validate(&self, &Record) -> Result<(), ValidationFailure>`. It should not expose generic methods, return `Self`, or require associated constructors through the trait object.

`Box<dyn Any>` discards the behavioral contract and replaces it with a type switch maintained by the host. `TypeId` can be justified at a narrow diagnostic or optional capability boundary—for example, a separate `as_any` hook used only by tooling—but ordinary validation should call the typed trait method. A giant enum preserves static exhaustiveness but makes every new external plugin a source change and release of the core crate.

Adding a required method to the public trait breaks all downstream implementors. Adding a method that makes the trait no longer dyn compatible breaks object users even if a default body exists. Safer evolution options include an extension trait, a new `ValidatorV2` trait with an adapter from V1, or a separate capability trait queried explicitly.

Deterministic order belongs to the registry, not to erasure. The registry should reject duplicate stable names and iterate in insertion or documented sorted order. Errors should retain the validator identity so a caller can distinguish policy failure from registry or host failure.

## Part 4 — Independent laboratory

A complete [Erased Validator Registry](../../labs/module-05-erased-validator-registry/README.md) satisfies its public contract and makes the erasure ledger inspectable. The reference implementation is not canonical; compare accepted input, rejected input, state after failure, ownership/lifetime surface, deterministic behavior, and extension authority in that order.

Build an ordered validator registry with stable identity, duplicate rejection, typed failure context, and runtime heterogeneous policies over one owned record type.

The transfer variant for Erased Validator Registry must alter at least two substantive dimensions and preserve an independent oracle; a domain-name substitution is not evidence of mastery.

## Part 5 — Capstone transfer

Complete AxiomStore’s variation map: static GAT codec, closed format authority, dynamic validators, and opaque query details. Record ownership separately from dispatch and reject unnecessary `Arc` or downcasting.

A strong capstone change keeps the responsibility described by the erasure ledger local. Reject any design that spreads the mechanism across unrelated AxiomStore modules without a named requirement.

## Part 6 — Reconstruct and defend

For an unseen extension request, choose generic, opaque, enum, trait object, or `Any` by stating what identity and operations survive, who may extend the set, and where mismatch occurs.

The defense passes when it reconstructs the erasure ledger from the requirement, shows a causal rejected construction, compares a simpler alternative, maps evidence, and names residual risk. Terminology without that chain is not mastery.
