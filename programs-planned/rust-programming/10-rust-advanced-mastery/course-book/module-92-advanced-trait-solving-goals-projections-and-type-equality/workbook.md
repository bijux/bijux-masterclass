# Workbook — Module 92: Advanced Trait Solving: Goals, Projections, and Type Equality

[Chapter](index.md) · [Laboratory](../../labs/module-02-projection-driven-pipeline/README.md) · [AxiomStore guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Advanced Trait Solving: Goals, Projections, and Type Equality** has become a usable model rather than remembered vocabulary. Its governing question is: *How do you design and debug APIs when the compiler must prove nested trait goals and normalize associated types before ordinary operations become legal?* Preserve your first prediction and record decisive facts in a **trait-goal and projection graph**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 91 — Reading Rust Through the Compiler: HIR, MIR, Borrow Checking, and Codegen that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **How do you design and debug APIs when the compiler must prove nested trait goals and normalize associated types before ordinary operations become legal?**
3. Draw the smallest **trait-goal and projection graph** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

For each case, submit: expected category (`compile-pass`, `compile-fail`, `run-pass`, `run-fail`, or `manual-review`), first decisive phase or event, governing relationship, and the strongest conclusion the outcome would justify.

Your prediction sheet must make the trait-goal graph visible. For one case, change exactly one assumption and explain why the decisive phase or outcome moves.

### Prediction 1 — Pipeline composition

For `Chain<A, B>` with `A: Stage` and `B: Stage<Input = A::Output>`, list the goals needed to call `run` and predict the first failure after removing the associated-type equality.

### Prediction 2 — Ambiguous conversion

A function calls `value.into()` where two target types are legal and the return type is otherwise unconstrained. Predict the result and identify three principled ways to supply selection information.

### Prediction 3 — Implied bound myth

An impl block has `T: Display`, and a free helper extracted from a method formats `T` without repeating the bound. Predict whether the helper is well formed.

### Prediction 4 — Recursive trait goal

A blanket implementation requires the same trait for an associated output without a decreasing type structure. Predict the likely solver behavior and the design question that must be answered first.

## Part 2 — Diagnose and repair

Each repair must leave a more precise trait-goal graph. Reject fixes that merely erase the type, lifetime, state, compatibility, or artifact fact that the exercise is designed to expose.

### Repair 1 — Global equality constraint

Two independently useful stages are defined with a global equality that couples all implementations.

Required direction: Move the equality to the `Chain` impl or constructor where the components meet. Standalone stages keep their own associated families.

Submit the corrected boundary plus one causal negative case. In the explanation, show exactly how the trait-goal graph changes.

### Repair 2 — String-erased stage errors

A reusable pipeline converts every stage error to `String` to make composition easy.

Required direction: Preserve a typed sum such as `ChainError<A::Error, B::Error>` and translate once at the application boundary that owns recovery policy.

For **Repair 2 — String-erased stage errors**, submit the corrected boundary plus one causal negative case. In the explanation, show exactly how the trait-goal graph changes.

### Repair 3 — Bound accumulation

A generic helper has ten bounds added one by one until it compiles.

Required direction: Remove all bounds, inspect each operation, and restore only the goals actually introduced by the body. Split the helper if one signature is carrying unrelated proof domains.

For **Repair 3 — Bound accumulation**, submit the corrected boundary plus one causal negative case. In the explanation, show exactly how the trait-goal graph changes.

## Part 3 — Focused exercises

### Exercise 1 — Goal expansion

Expand a nested `Iterator<Item = Result<T, E>>` consumer into implementation, projection, equality, and well-formedness goals.

Completion standard: Every operation is connected to the goal that authorizes it.

### Exercise 2 — Three-stage error family

Compose parse, validate, and encode stages without text erasure.

Completion standard: The final error identifies the failing stage and retains its source type.

### Exercise 3 — Ambiguity redesign

Produce three APIs that resolve one ambiguous target by caller input, implementation ownership, and explicit constructor.

Completion standard: The comparison names who chooses the type in each design.

### Exercise 4 — Coherence boundary

Create an overlapping blanket-impl proposal and repair it with a local newtype or narrower trait domain.

Completion standard: The final implementation ownership is legal and architecturally justified.

### Cross-course transfer

Choose one artifact from Courses 1–10 and reassess it through **Advanced Trait Solving: Goals, Projections, and Type Equality**. Reconstruct its current invariant owner, then decide whether the trait-goal graph reveals a genuine defect. A justified no-change decision is valid when the advanced mechanism would add proof or compatibility cost without removing a real invalid state.

### Applied case study — projected errors in a storage pipeline

Design a three-stage archival pipeline: a decoder produces a borrowed record view, a validator accepts that exact view family, and a materializer produces an owned record. Each stage selects its own error type. A proposed API adds a single generic `E` and converts every failure into `E: From<String>`. Another proposal places every associated-type equality on the `Stage` trait itself.

Write the trait goals required to compose the three stages. Separate normalization goals such as `<D as Decode>::View<'a> = <V as Validate>::Input<'a>` from capability goals such as `V: Validate`. Identify which equalities belong at the composition boundary and which would overconstrain standalone implementations. Show how ambiguity can arise when a projected type has no uniquely determined implementor, and specify where a fully qualified projection is needed.

Your answer must preserve error provenance. Explain how the outer pipeline can expose a sum error without forcing unrelated stages to share one error family. Finally, construct one negative example in which the decoder and validator are both individually valid but cannot compose, and state what compiler evidence would prove the mismatch.

### Interleaved reasoning pass

1. For **Rewrite a complex generic error as a small set of trait goals, projection goals, and equality constraints**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the trait-goal and projection graph.
2. For **Distinguish proving that a trait is implemented from normalizing an associated type selected by that implementation**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the trait-goal and projection graph.
3. For **Choose associated types, generic parameters, and helper traits according to who selects each type relationship**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the trait-goal and projection graph.
4. For **Express equality between associated outputs without forcing unrelated callers to name implementation details**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the trait-goal and projection graph.

5. Identify one guarantee from an earlier course that a careless implementation of **Advanced Trait Solving: Goals, Projections, and Type Equality** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build [Projection-Driven Pipeline](../../labs/module-02-projection-driven-pipeline/README.md) from its `starter/` package.

Build a three-stage pipeline whose associated input, output, and error families connect only at the assembly boundary. Mismatched composition must be rejected before execution.

Before implementation, freeze Projection-Driven Pipeline’s public behavior and the trait-goal graph. After implementation, complete its transfer task in a domain with different ownership, version, capacity, extension, or failure policy; renaming types does not demonstrate transfer.

### Laboratory acceptance trace

Before opening the reference implementation for **Projection-Driven Pipeline**, record:

- the public behavior that demonstrates **Rewrite a complex generic error as a small set of trait goals, projection goals, and equality constraints**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Write the goal graph for AxiomStore’s codec, borrowed view, owned record conversion, and validator boundary. Keep codec errors precise until translation into `StoreError`; do not make runtime validators generic over the codec’s lending family.

Update AxiomStore’s trait-goal graph before code. Record the changed invariant owner, new failure paths, compatibility effect, and falsifying evidence. Then run the full capstone route because this module can invalidate guarantees outside its local file.

### Evidence quality review

Before leaving the module, revisit the trait goal you initially expected the compiler to infer. Write the projection or equality that was actually missing, identify the downstream operation that required it, and remove one bound that turned out to be unrelated. Record one case that remains intentionally unsupported so the resulting trait surface does not imply a broader family of compositions than you proved.

### Capstone invariant trace

For the Module 92 AxiomStore increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Normalize one nested projection aloud, identify the owner of every type choice, and explain why a more generic signature can admit nonsense rather than improve reuse.

Finish without notes by reconstructing the trait-goal graph. Name the requirement, the simpler design, the decisive rejected construction, the state after failure, and the evidence that could falsify your claim. End by stating one condition under which this mechanism should be removed.

The defense is complete only when another reader can reproduce the reasoning behind Projection-Driven Pipeline and the AxiomStore increment without seeing your final implementation.

### Closed-book defense

In five minutes, answer “How do you design and debug APIs when the compiler must prove nested trait goals and normalize associated types before ordinary operations become legal?” using the **trait-goal and projection graph**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside AxiomStore. A list of APIs without the deciding relationship is incomplete.
