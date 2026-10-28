# Workbook — Module 94: Const Generics, Witness Types, and Compile-Time Invariants

[Chapter](index.md) · [Laboratory](../../labs/module-04-bounded-matrix/README.md) · [AxiomStore guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Const Generics, Witness Types, and Compile-Time Invariants** has become a usable model rather than remembered vocabulary. Its governing question is: *Which numeric and state facts belong in types, which remain runtime data, and how do you avoid turning a library into an unusable type-level calculator?* Preserve your first prediction and record decisive facts in a **const witness proof**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 93 — GATs, Higher-Ranked Bounds, and Lending Interfaces that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **Which numeric and state facts belong in types, which remain runtime data, and how do you avoid turning a library into an unusable type-level calculator?**
3. Draw the smallest **const witness proof** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

For each case, submit: expected category (`compile-pass`, `compile-fail`, `run-pass`, `run-fail`, or `manual-review`), first decisive phase or event, governing relationship, and the strongest conclusion the outcome would justify.

Your prediction sheet must make the static/dynamic invariant table visible. For one case, change exactly one assumption and explain why the decisive phase or outcome moves.

### Prediction 1 — Matrix multiplication

Predict whether `Matrix<T, 2, 3>` may multiply `Matrix<T, 4, 2>` under a signature that requires equal inner const parameters.

### Prediction 2 — Capacity versus length

An `InlineBatch<T, 8>` has `len = 3`. Which facts are compile-time and which remain runtime?

### Prediction 3 — Forgeable witness

`BoundedIndex<N>` exposes its tuple field publicly. Predict whether indexing through the witness remains justified.

### Prediction 4 — Zero capacity

For `InlineBatch<T, 0>`, predict `is_full`, `push`, `as_slice`, and drop behavior.

## Part 2 — Diagnose and repair

Each repair must leave a more precise static/dynamic invariant table. Reject fixes that merely erase the type, lifetime, state, compatibility, or artifact fact that the exercise is designed to expose.

### Repair 1 — Every configuration becomes const

A service exposes user-selected batch sizes as public const parameters across its API.

Required direction: Keep runtime policy dynamic unless callers need type-level composition or representation specialization. A small private specialization layer may bridge the two.

Submit the corrected boundary plus one causal negative case. In the explanation, show exactly how the static/dynamic invariant table changes.

### Repair 2 — Witness constructor unchecked

A private-field witness has a public `new_unchecked` safe constructor.

Required direction: Make unchecked construction unsafe/private or remove it. Safe constructors must establish the carried predicate.

For **Repair 2 — Witness constructor unchecked**, submit the corrected boundary plus one causal negative case. In the explanation, show exactly how the static/dynamic invariant table changes.

### Repair 3 — Const arithmetic assumed infallible

A matrix constructor multiplies dimensions without checked arithmetic because dimensions are consts.

Required direction: Validate overflow where stable const expressions cannot encode the required proof; const knowledge does not make `usize` multiplication mathematically unbounded.

For **Repair 3 — Const arithmetic assumed infallible**, submit the corrected boundary plus one causal negative case. In the explanation, show exactly how the static/dynamic invariant table changes.

## Part 3 — Focused exercises

### Exercise 1 — Shape-checked multiplication

Implement matrix multiplication with type-equal inner dimensions.

Completion standard: Incompatible shapes fail before runtime and valid shapes match a dynamic oracle.

### Exercise 2 — Witness API

Build `BoundedIndex<N>` with private representation and boundary tests.

Completion standard: The first invalid index is rejected for multiple `N`, including zero.

### Exercise 3 — Hybrid capacity design

Compare inline fixed capacity with a dynamic `Vec` implementation.

Completion standard: The decision identifies a real storage/composition requirement rather than style.

### Exercise 4 — Instantiation budget

List all const values used by a sample application and inspect the compatibility implications.

Completion standard: The report identifies unnecessary public instantiation freedom.

### Cross-course transfer

Choose one artifact from Courses 1–10 and reassess it through **Const Generics, Witness Types, and Compile-Time Invariants**. Reconstruct its current invariant owner, then decide whether the static/dynamic invariant table reveals a genuine defect. A justified no-change decision is valid when the advanced mechanism would add proof or compatibility cost without removing a real invalid state.

### Applied case study — static capacity versus runtime policy

A telemetry component supports batches of at most 32 records in one embedded deployment and a user-configurable limit between 1 and 10,000 in a server deployment. A proposal makes both limits const generic parameters. Another stores both as `usize`. A third introduces `Batch<T, const N: usize>` for inline storage and a validated `RuntimeLimit` for admission policy.

Classify every invariant by phase and authority. Which invalid states can the type system exclude? Which must remain runtime decisions because they come from configuration? Show how a witness type can prevent indexing outside an `N`-element batch without pretending that arithmetic on arbitrary const expressions is universally available. Include the zero-capacity case in the design.

Then examine API stability. Explain how placing `N` in a public type affects downstream type identity, monomorphization, and migration. Decide whether the server's configured limit should appear in the public type. End with a construction that proves the selected inline capacity and runtime admission limit cannot silently disagree about which one controls rejection.

### Interleaved reasoning pass

1. For **Use const parameters when a numeric fact changes representation, layout, or legal composition**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the const witness proof.
2. For **Construct witness types only through checked functions and preserve their proof through private fields**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the const witness proof.
3. For **Distinguish compile-time capacity from runtime length and enforce both without off-by-one ambiguity**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the const witness proof.
4. For **Design APIs that compose equal dimensions while rejecting mismatched shapes before execution**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the const witness proof.

5. Identify one guarantee from an earlier course that a careless implementation of **Const Generics, Witness Types, and Compile-Time Invariants** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build [Bounded Matrix](../../labs/module-04-bounded-matrix/README.md) from its `starter/` package.

Build a fixed-shape matrix and nonforgeable bounded indices, then redesign one API whose dimensions belong at runtime rather than in type identity.

Before implementation, freeze Bounded Matrix’s public behavior and the static/dynamic invariant table. After implementation, complete its transfer task in a domain with different ownership, version, capacity, extension, or failure policy; renaming types does not demonstrate transfer.

### Laboratory acceptance trace

Before opening the reference implementation for **Bounded Matrix**, record:

- the public behavior that demonstrates **Use const parameters when a numeric fact changes representation, layout, or legal composition**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Defend `MAX_RECORD` and `TX_CAP` separately. Document what each const controls, what runtime state remains, zero/maximum behavior, expected instantiations, and the simpler dynamic alternative.

Update AxiomStore’s static/dynamic invariant table before code. Record the changed invariant owner, new failure paths, compatibility effect, and falsifying evidence. Then run the full capstone route because this module can invalidate guarantees outside its local file.

### Evidence quality review

Before leaving the module, list every numeric fact in the lab and classify it as representation-shaping const data, constructor-validated runtime data, or operating policy. Reconsider the fact you placed in the wrong category first. Record the compatibility and ergonomics cost of adding one more const parameter, even if that parameter would make a narrow illegal state unrepresentable.

### Capstone invariant trace

For the Module 94 AxiomStore increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

For every const parameter, answer: what downstream composition does it enable, what mutable state is still required, and what compatibility or code-generation cost does it create?

Finish without notes by reconstructing the static/dynamic invariant table. Name the requirement, the simpler design, the decisive rejected construction, the state after failure, and the evidence that could falsify your claim. End by stating one condition under which this mechanism should be removed.

The defense is complete only when another reader can reproduce the reasoning behind Bounded Matrix and the AxiomStore increment without seeing your final implementation.

### Closed-book defense

In five minutes, answer “Which numeric and state facts belong in types, which remain runtime data, and how do you avoid turning a library into an unusable type-level calculator?” using the **const witness proof**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside AxiomStore. A list of APIs without the deciding relationship is incomplete.
