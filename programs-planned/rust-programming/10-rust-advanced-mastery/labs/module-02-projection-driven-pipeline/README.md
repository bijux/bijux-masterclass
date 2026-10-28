# Laboratory 92 — Projection-Driven Pipeline

**Course 10 · Module 92: Advanced Trait Solving: Goals, Projections, and Type Equality**

[Chapter](../../course-book/module-92-advanced-trait-solving-goals-projections-and-type-equality/index.md) · [Workbook](../../course-book/module-92-advanced-trait-solving-goals-projections-and-type-equality/workbook.md) · [AxiomStore guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Advanced Trait Solving: Goals, Projections, and Type Equality**: How do you design and debug APIs when the compiler must prove nested trait goals and normalize associated types before ordinary operations become legal? The product must make **Rewrite a complex generic error as a small set of trait goals, projection goals, and equality constraints** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **trait-goal and projection graph** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Product

Build a three-stage pipeline in which every stage chooses its own input, output, and error family. Composition is legal only when adjacent associated types normalize to the same type. The laboratory exists to make projection equality concrete: the compiler should reject an impossible chain before any value flows through it, while valid stages remain reusable outside that chain.

The starter supplies a minimal `Stage` trait and an identity stage. Extend it with a `Chain<A, B>` adapter, a typed sum error, and at least three concrete stages. One useful route is text parsing, domain validation, and formatting. Another is decoding, normalization, and materialization. Choose a route where the intermediate types are genuinely different enough to make the equality constraint visible.

### Composition contract

The chain must satisfy all of the following:

- `A::Output` is exactly `B::Input`;
- the outer input is `A::Input`;
- the outer output is `B::Output`;
- first-stage and second-stage failures remain distinguishable;
- no stage acquires bounds required only by one particular composition;
- no `String` conversion erases error provenance.

Write the associated-type goal before implementing the adapter. Then create one negative compiler specimen using two stages that are individually valid but cannot compose. The failure must be caused by the projection mismatch, not by an unrelated missing import or typo.

### Ambiguity clinic

Add a second trait with an associated type named `Output`. Construct one small expression in which `T::Output` is ambiguous and repair it with a fully qualified projection. Explain why adding a random type annotation at the call site is weaker than naming the trait relationship directly.

### Runtime evidence

Test success, first-stage failure, second-stage failure, and a stage whose error type is `Infallible`. Verify that no later stage runs after an earlier failure. A counter or probe is acceptable, but it must remain outside the type relationship being tested.

### Transfer

Introduce a branch stage whose result is deliberately one of two types. Redesign the stage to return a domain enum and compose a common next stage over that enum. Explain why an explicit sum type represents the variation, whereas type erasure would hide it and a forced associated-type equality would make the branch impossible.

### Using the reference

After completing `starter/`, inspect `solution/`. Compare where each implementation places equality constraints, how it preserves errors, and whether it overconstrains standalone stages. Do not copy the reference’s syntax if your own design has a smaller public contract.

### Mechanism-specific completion standard

You can derive the required trait goals from a proposed pipeline, predict whether they normalize, and locate the narrowest boundary that owns each equality. A pipeline that merely converts everything to strings has avoided the lesson rather than completed it.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Projection-Driven Pipeline**.
2. Draw the smallest **trait-goal and projection graph** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to AxiomStore so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Whole-laboratory completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Rewrite a complex generic error as a small set of trait goals, projection goals, and equality constraints.
- Distinguish proving that a trait is implemented from normalizing an associated type selected by that implementation.
- Choose associated types, generic parameters, and helper traits according to who selects each type relationship.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 92 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **trait-goal and projection graph**. Defend why your design is simpler than one plausible alternative under the new requirements.
