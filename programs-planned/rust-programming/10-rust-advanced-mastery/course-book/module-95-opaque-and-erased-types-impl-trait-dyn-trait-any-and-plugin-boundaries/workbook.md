# Module 95 Workbook — Opaque and Erased Types: impl Trait, dyn Trait, Any, and Plugin Boundaries

[Chapter](index.md) · [AxiomStore guide](../capstone.md) · [Solutions](solutions.md)

This workbook turns the chapter’s **erasure ledger** into evidence. Write predictions before compiling or running anything. Preserve the stated product requirement during repair; a green build obtained by deleting the difficult relationship is not a solution.

## Part 1 — Predict

For each case, submit: expected category (`compile-pass`, `compile-fail`, `run-pass`, `run-fail`, or `manual-review`), first decisive phase or event, governing relationship, and the strongest conclusion the outcome would justify.

Your prediction sheet must make the erasure ledger visible. For one case, change exactly one assumption and explain why the decisive phase or outcome moves.

### Prediction 1 — Different opaque branches

A function returning `impl Iterator<Item = u8>` returns `slice.iter().copied()` in one branch and `once(0)` in another. Predict the result.

### Prediction 2 — Generic object method

A trait used as `dyn Codec` adds `fn decode<T>(&self, bytes: &[u8]) -> T`. Predict dyn compatibility.

### Prediction 3 — Ownership choice

A validator registry owns policies for its entire lifetime but never shares them across threads. Compare `Box<dyn Validator>` and `Arc<dyn Validator>`. 

### Prediction 4 — Any as protocol

A host stores plugins as `Box<dyn Any>` and downcasts every one before calling `validate`. Evaluate the design.

## Part 2 — Diagnose and repair

Each repair must leave a more precise erasure ledger. Reject fixes that merely erase the type, lifetime, state, compatibility, or artifact fact that the exercise is designed to expose.

### Repair 1 — Erasing the lending codec

A lifetime-indexed codec is forced behind one trait object solely for architectural uniformity.

Required direction: Keep the codec static/GAT-based and erase only runtime validator policy. Variation axes need not share one mechanism.

Submit the corrected boundary plus one causal negative case. In the explanation, show exactly how the erasure ledger changes.

### Repair 2 — Enum used for open plugins

An application must accept third-party validators but models them as a public exhaustive enum.

Required direction: Use a dyn-compatible trait registry or another open extension boundary; the enum gives extension authority to the defining crate.

Submit the corrected boundary plus one causal negative case. In the explanation, show exactly how the erasure ledger changes.

### Repair 3 — Arc selected by habit

Every dynamic component is stored in `Arc` even though ownership is unique.

Required direction: Choose ownership from liveness and sharing first. Dynamic dispatch works through borrowed or boxed values too.

Submit the corrected boundary plus one causal negative case. In the explanation, show exactly how the erasure ledger changes.

## Part 3 — Focused exercises

### Exercise 1 — Opaque unification

Repair two opaque iterator branches with an enum adapter, boxed iterator, and one common pipeline.

Completion standard: The comparison identifies retained information, allocation, and API cost.

### Exercise 2 — Dyn audit

Audit a trait containing associated types, generic methods, constructors, and consuming receivers.

Completion standard: Every object-usable and object-excluded method is justified.

### Exercise 3 — Closed/open pair

Implement the same semantic operations with an enum and a trait-object registry.

Completion standard: Tests share one oracle; extension authority differs explicitly.

### Exercise 4 — Typed context

Build a small `Any` context with duplicate and mismatch policy.

Completion standard: The result documents why it is not a behavioral plugin interface.

### Cross-course transfer

Choose one artifact from Courses 1–9 and reassess it through **Opaque and Erased Types: impl Trait, dyn Trait, Any, and Plugin Boundaries**. Reconstruct its current invariant owner, then decide whether the erasure ledger reveals a genuine defect. A justified no-change decision is valid when the advanced mechanism would add proof or compatibility cost without removing a real invalid state.


### Applied case study — preserving a stable plugin boundary

A validation engine has three built-in validators known at compile time and must also accept third-party validators loaded by the host. The built-ins are performance-sensitive; plugins need stable names, typed failures, deterministic order, and no downcasting in ordinary execution. A proposal stores everything as `Box<dyn Any>` and switches on `TypeId`. Another uses one giant enum. A third combines a generic built-in path with an erased `dyn Validator` registry.

Produce a variation map. Identify which variation is closed, which is open, who chooses each concrete type, and whether heterogeneous values coexist. Specify the smallest dyn-compatible trait. Explain why generic methods, associated constructors without `Self: Sized`, or returning `Self` would damage object use.

Define the one place where `Any` would be justified, if any, and require a typed method to remain the normal path. Finally, discuss public API evolution: what additions to the object-safe trait would break third-party implementors or dyn compatibility, and what adapter or versioning strategy preserves extension room.

## Part 4 — Independent laboratory

Build [Erased Validator Registry](../../labs/module-05-erased-validator-registry/README.md) from its `starter/` package.

Build an ordered validator registry with stable identity, duplicate rejection, typed failure context, and runtime heterogeneous policies over one owned record type.

Before implementation, freeze Erased Validator Registry’s public behavior and the erasure ledger. After implementation, complete its transfer task in a domain with different ownership, version, capacity, extension, or failure policy; renaming types does not demonstrate transfer.

## Part 5 — Capstone transfer

Complete AxiomStore’s variation map: static GAT codec, closed format authority, dynamic validators, and opaque query details. Record ownership separately from dispatch and reject unnecessary `Arc` or downcasting.

Update AxiomStore’s erasure ledger before code. Record the changed invariant owner, new failure paths, compatibility effect, and falsifying evidence. Then run the full capstone route because this module can invalidate guarantees outside its local file.

### Evidence quality review

Before leaving the module, revisit one boundary where you first chose erasure. State the concrete information lost, the runtime failure newly possible, and the caller who benefits from openness. Then revisit one boundary kept static or closed. Record the future requirement that would justify changing that decision rather than treating trait objects as the default form of extensibility.

## Part 6 — Reconstruct and defend

For an unseen extension request, choose generic, opaque, enum, trait object, or `Any` by stating what identity and operations survive, who may extend the set, and where mismatch occurs.

Finish without notes by reconstructing the erasure ledger. Name the requirement, the simpler design, the decisive rejected construction, the state after failure, and the evidence that could falsify your claim. End by stating one condition under which this mechanism should be removed.

The defense is complete only when another reader can reproduce the reasoning behind Erased Validator Registry and the AxiomStore increment without seeing your final implementation.
