# Reasoned Solutions — Module 24: Static Polymorphism and Opaque Types

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-04-static-pipeline/README.md) · [Review Engine guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 24: Static Polymorphism and Opaque Types**. Compare the reasoning against this question: *When should concrete types remain visible to the compiler, and how can an API hide implementation details without erasing static guarantees?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Compiler specimen reasoning

### 1. `01-method-specific-bound.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A method body may use formatting only when the method or enclosing implementation constrains the field type with the required formatting trait.
- **Causal explanation:** `format!("{}", self.0)` requires `T: Display`, but the unconstrained implementation promises `show` for every `T`; generic checking therefore rejects the body.
- **Principled repair:** Put the bound on the method or a separate impl block.
- **Weak repair to reject:** Put every possible bound on the struct.

### 2. `02-narrow-impl-bound.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Bounds can be placed on only the methods or implementation blocks that require them, leaving unrelated capabilities available to more types.
- **Causal explanation:** `first` is available for every `Pair<T>`, while `max` is available only when `T: PartialOrd`; the `i32` pair satisfies the narrower comparison contract.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Constrain the entire struct.

### 3. `03-independent-impl-trait-arguments.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Separate argument-position `impl Trait` occurrences denote independent hidden type parameters unless the signature explicitly ties them together.
- **Causal explanation:** `a` and `b` need only implement `Display`; one may be an integer and the other a string slice because no equality relation is declared between their concrete types.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Assume the types are equal in the body.

### 4. `04-named-generic-equality.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Reusing one named type parameter for two arguments requires both arguments to have exactly the same concrete type.
- **Causal explanation:** `show<T>(_: T, _: T)` cannot choose one `T` that is simultaneously `u8` and `u16`; independent parameters are needed when equality is not part of the contract.
- **Principled repair:** Use separate type parameters when equality is unnecessary.
- **Weak repair to reject:** Convert both values to String regardless of semantics.

### 5. `05-opaque-branch-mismatch.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Every return path of one return-position `impl Trait` function must produce the same hidden concrete type.
- **Causal explanation:** The `if` branches produce `u8` and `&str`. Both implement `Display`, but the opaque return denotes one concrete type, not a run-time union of all implementors.
- **Principled repair:** Use an enum, trait object, or one unified concrete adapter.
- **Weak repair to reject:** Return formatted strings solely to erase differences.

### 6. `06-opaque-static-dispatch.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** A return-position `impl Trait` hides a single concrete return type from callers while preserving its stated capabilities for static dispatch.
- **Causal explanation:** The function always returns the same array iterator type and promises `Iterator<Item = u8>`, so callers may use iterator methods without learning the concrete name.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Expose a long concrete iterator type publicly.

### 7. `07-opaque-capability-limit.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Callers of an opaque return may rely only on bounds named in the public return type.
- **Causal explanation:** Although the hidden value happens to be a `String`, the signature promises only `Display`; `clone` is therefore unavailable until `Clone` becomes an intentional part of the contract.
- **Principled repair:** Add a justified Clone bound or avoid requiring it.
- **Weak repair to reject:** Downcast the opaque value.

### 8. `08-generic-type-transition.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** A consuming generic method may return the same structure instantiated with a different type parameter.
- **Causal explanation:** `map` owns the original pair, preserves its first field, and returns `P<A, C>`; the annotated result exactly matches the new `C = &str` state.
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

## Reference implementation comparison

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

## Deep reasoning and transfer

### Decisive model

> When should concrete types remain visible to the compiler, and how can an API hide implementation details without erasing static guarantees?

Build a **static-dispatch map**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Design generic functions and types with the weakest sufficient bounds.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Distinguish argument-position and return-position `impl Trait`.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Explain monomorphization without promising optimization outcomes.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Choose static dispatch when concrete type identity carries useful guarantees.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Control generic API complexity through boundary placement.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Design generic functions and types with the weakest sufficient bounds.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the static-dispatch map.

### Laboratory transfer review

For [Static Pipeline](../../labs/module-04-static-pipeline/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In Review Engine, Module 24 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Static Polymorphism and Opaque Types**, which relationship decides this question: “When should concrete types remain visible to the compiler, and how can an API hide implementation details without erasing static guarantees?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to Review Engine?
