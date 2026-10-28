# Reasoned solutions — Module 25: Trait Objects and Dynamic Polymorphism

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the Review Engine engineering guide](../capstone.md)

Use these explanations to review your reasoning about **Trait Objects and Dynamic Polymorphism**, not to substitute for an attempt. The decisive question is: *When is run-time heterogeneity real, what information does a trait object erase, and what must remain dispatchable?* When your design differs, separate three possibilities: a Rust rule was applied incorrectly, the product contract changed, or two architectures satisfy the same contract with different trade-offs.

## Compiler specimen reasoning

### 1. `01-explicit-dyn.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Explicit dyn.
- **Causal explanation:** The specimen compiles because explicit dyn.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Make the function generic when runtime erasure is required.

### 2. `02-generic-method-dyn-incompatibility.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Generic method dyn incompatibility.
- **Causal explanation:** The compiler rejects the specimen because generic method dyn incompatibility.
- **Principled repair:** Move it to a Sized extension or erase the parameter.
- **Weak repair to reject:** Replace the result with String and ignore semantics.

### 3. `03-self-return-dyn-incompatibility.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Self return dyn incompatibility.
- **Causal explanation:** The compiler rejects the specimen because self return dyn incompatibility.
- **Principled repair:** Mark the method Self:Sized or define a boxed clone contract.
- **Weak repair to reject:** Return `Box<dyn Any>`.

### 4. `04-associated-constant-dyn-incompatibility.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Associated constant dyn incompatibility.
- **Causal explanation:** The compiler rejects the specimen because associated constant dyn incompatibility.
- **Principled repair:** Move dynamic metadata to a method or split a static metadata trait.
- **Weak repair to reject:** Hard-code the value in callers.

### 5. `05-associated-type-specification.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Associated type specification.
- **Causal explanation:** The compiler rejects the specimen because associated type specification.
- **Principled repair:** Use `dyn Source<Item=u8>` or a generic boundary.
- **Weak repair to reject:** Erase the item into String.

### 6. `06-self-sized-escape.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Self Sized escape.
- **Causal explanation:** The specimen compiles because self Sized escape.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Remove useful constructor convenience entirely.

### 7. `07-borrowed-object-lifetime.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Borrowed object lifetime.
- **Causal explanation:** The specimen compiles because borrowed object lifetime.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Require static data unnecessarily.

### 8. `08-heterogeneous-registry.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Heterogeneous registry.
- **Causal explanation:** The specimen compiles because heterogeneous registry.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Downcast each value for ordinary execution.

## Exercise reasoning

Dyn compatibility follows from whether one erased dispatch surface can represent each method. Generic methods, associated constants, GATs, opaque returns, and most uses of `Self` prevent dispatch. `Self: Sized` excludes concrete-only methods. Object lifetimes constrain hidden borrows; `'static` is a bound on contained references, not duration. Heterogeneous runtime collections justify trait objects only when their common contract is sufficient. Construction often remains typed and separate.

## Dyn compatibility

A generic method cannot be represented by one vtable entry for every possible caller-selected `T`; the erased concrete receiver does not provide a finite callable signature for that method. An associated function without a receiver also cannot be dispatched through an object unless excluded with `where Self: Sized`. Returning bare `Self` similarly requires knowledge of the erased type.

The principled redesign gives the boundary concrete domain types, for example `fn evaluate(&self, submission: &Submission) -> Vec<Finding>`. Generic parsing belongs before erasure or behind a separate static interface. Adding `Self: Sized` is appropriate only for operations intentionally unavailable through objects.

## Object ownership

`&dyn Rule` borrows an object owned elsewhere. `Box<dyn Rule>` gives the registry unique ownership and is the simplest fit for a single-threaded CLI. `Rc` supports shared single-thread ownership, while `Arc` supports atomic shared ownership across threads but does not itself make the underlying behavior thread-safe; the object contract generally needs `Send + Sync` for cross-thread use.

## Object lifetimes

`dyn Rule + 'a` says the erased object may contain references valid for `'a`. Omitting the object lifetime in owned pointer positions often defaults to `'static`, which rejects borrowed configuration. Owning parsed configuration inside each rule usually simplifies the registry unless borrowing has a measured reason.

## Enum comparison

Enums are strong for a closed set, exhaustive matching, direct serialization, and per-variant behavior. Trait objects are strong when the set is open at runtime or downstream implementations matter. The same system can parse an enum configuration and construct trait objects; mechanism boundaries may differ by phase.

## Registry defense

After boxing, callers know only the `Rule` contract and auto-trait/lifetime bounds. Concrete fields and inherent methods are erased. Downcasting should be added only for a real requirement because it weakens abstraction. Deterministic order follows from the chosen ordered collection and should be tested through observable finding order.

## Laboratory comparison

The complete laboratory implementation is in [`module-05-dynamic-command-bus/solution`](../../labs/module-05-dynamic-command-bus/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Trait Objects and Dynamic Polymorphism**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Derive whether a trait is dyn-compatible and repair it without erasing its meaning.
- Use borrowed and owned trait objects with correct object lifetimes.
- Build a heterogeneous runtime collection behind one behavioral interface.
- Compare enum, generic, and trait-object designs against explicit change scenarios.
- Identify the information and capabilities lost during type erasure.

A complete explanation of **Trait Objects and Dynamic Polymorphism** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.
