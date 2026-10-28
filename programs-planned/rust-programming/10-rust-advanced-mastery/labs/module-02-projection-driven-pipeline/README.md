# Laboratory 2 — Projection-Driven Pipeline

[Course 10](../../README.md) · [Common laboratory method](../../../START_HERE.md#laboratory-method)

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

### Completion standard

You can derive the required trait goals from a proposed pipeline, predict whether they normalize, and locate the narrowest boundary that owns each equality. A pipeline that merely converts everything to strings has avoided the lesson rather than completed it.
