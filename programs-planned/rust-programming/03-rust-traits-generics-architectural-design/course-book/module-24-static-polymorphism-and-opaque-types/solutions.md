# Reasoned solutions — Module 24: Static Polymorphism and Opaque Types

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the Review Engine engineering guide](../capstone.md)

Use these explanations to review your reasoning about **Static Polymorphism and Opaque Types**, not to substitute for an attempt. The decisive question is: *When should concrete types remain visible to the compiler, and how can an API hide implementation details without erasing static guarantees?* When your design differs, separate three possibilities: a Rust rule was applied incorrectly, the product contract changed, or two architectures satisfy the same contract with different trade-offs.

## Compiler specimen reasoning

### 1. `01-method-specific-bound.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Method-specific bound.
- **Causal explanation:** The compiler rejects the specimen because method-specific bound.
- **Principled repair:** Put the bound on the method or a separate impl block.
- **Weak repair to reject:** Put every possible bound on the struct.

### 2. `02-narrow-impl-bound.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Narrow impl bound.
- **Causal explanation:** The specimen compiles because narrow impl bound.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Constrain the entire struct.

### 3. `03-independent-impl-trait-arguments.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Independent impl Trait arguments.
- **Causal explanation:** The specimen compiles because independent impl Trait arguments.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Assume the types are equal in the body.

### 4. `04-named-generic-equality.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Named generic equality.
- **Causal explanation:** The compiler rejects the specimen because named generic equality.
- **Principled repair:** Use separate type parameters when equality is unnecessary.
- **Weak repair to reject:** Convert both values to String regardless of semantics.

### 5. `05-opaque-branch-mismatch.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Opaque branch mismatch.
- **Causal explanation:** The compiler rejects the specimen because opaque branch mismatch.
- **Principled repair:** Use an enum, trait object, or one unified concrete adapter.
- **Weak repair to reject:** Return formatted strings solely to erase differences.

### 6. `06-opaque-static-dispatch.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Opaque static dispatch.
- **Causal explanation:** The specimen compiles because opaque static dispatch.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Expose a long concrete iterator type publicly.

### 7. `07-opaque-capability-limit.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Opaque capability limit.
- **Causal explanation:** The compiler rejects the specimen because opaque capability limit.
- **Principled repair:** Add a justified Clone bound or avoid requiring it.
- **Weak repair to reject:** Downcast the opaque value.

### 8. `08-generic-type-transition.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Generic type transition.
- **Causal explanation:** The specimen compiles because generic type transition.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Hide all strategy changes behind dynamic dispatch.

## Exercise reasoning

Bounds should arise from operations in the body. Struct-wide bounds are unnecessary when only selected methods need them. Separate `impl Trait` arguments may differ; a named parameter enforces equality. Opaque return types preserve static dispatch but reveal only stated capabilities and require one hidden type. Enums preserve a closed set and pattern matching; trait objects support open runtime heterogeneity with erasure. Generic parameters should remain at boundaries where concrete identity affects construction or output, not spread solely for test substitution.

## Bound minimization

Bounds are capabilities the implementation demands from callers. Unused bounds exclude otherwise valid types, leak implementation choices, and can become semver constraints. `Send`, `Sync`, and `'static` are especially damaging when the current algorithm neither crosses threads nor stores data beyond a borrow.

Argument-position `impl Trait` is usually sugar for an anonymous generic parameter. A named `T` is required when multiple parameters must have the same type, when a where-clause relates types, or when the return type mentions the parameter.

## Opaque branches

Return-position `impl Trait` requires one hidden concrete type across all return paths. The range and vector iterator differ. Repairs include collecting both branches into the same owned collection and returning its iterator, defining a local enum that implements `Iterator`, or returning `Box<dyn Iterator<Item = u32>>`. Collection may allocate eagerly; an enum preserves static dispatch but adds implementation; boxing erases type and usually allocates. The product's runtime variation decides.

## RPITIT

A trait method returning `impl Iterator<Item = &str>` promises some implementation-specific iterator while hiding its concrete name. The returned borrows remain tied to `&self` through elision. Callers may use the iterator contract but cannot name or assume the hidden type. An associated type exposes a stable type family and supports equality constraints; a boxed trait object supports runtime erasure and heterogeneous choices.

## Monomorphization

The language-level design is statically typed for each concrete instantiation. Compilers commonly monomorphize generic code, which may enable inlining and may increase code size. Exact machine code, deduplication, and performance are implementation and measurement questions, not API guarantees.

## Static boundary

Sources and reporters are good generic outer boundaries when one engine execution uses one concrete source and reporter. The rule registry is not, because it must contain several concrete rule types together. A good signature map makes this asymmetry explicit rather than forcing one mechanism everywhere.

## Laboratory comparison

The complete laboratory implementation is in [`module-04-static-pipeline/solution`](../../labs/module-04-static-pipeline/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Static Polymorphism and Opaque Types**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Design generic functions and types with the weakest sufficient bounds.
- Distinguish argument-position and return-position `impl Trait`.
- Explain monomorphization without promising optimization outcomes.
- Choose static dispatch when concrete type identity carries useful guarantees.
- Control generic API complexity through boundary placement.

A complete explanation of **Static Polymorphism and Opaque Types** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.
