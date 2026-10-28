# Reasoned Solutions — Module 25: Trait Objects and Dynamic Polymorphism

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-05-dynamic-command-bus/README.md) · [Review Engine guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 25: Trait Objects and Dynamic Polymorphism**. Compare the reasoning against this question: *When is run-time heterogeneity real, what information does a trait object erase, and what must remain dispatchable?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Compiler specimen reasoning

### 1. `01-explicit-dyn.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** A trait object type is written explicitly with `dyn` and may dispatch only methods represented by the object-safe trait surface.
- **Causal explanation:** `&dyn Name` erases the concrete `X` while retaining the callable `name(&self) -> &str` contract, so `show` can dispatch through the object.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Make the function generic when runtime erasure is required.

### 2. `02-generic-method-dyn-incompatibility.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A trait method with its own unconstrained type parameter cannot be represented by one finite vtable entry for a trait object.
- **Causal explanation:** `encode<T>` asks each call site to choose an arbitrary `T`; after erasing the concrete implementor, `dyn Encode` has no single monomorphic method signature to dispatch.
- **Principled repair:** Move it to a Sized extension or erase the parameter.
- **Weak repair to reject:** Replace the result with String and ignore semantics.

### 3. `03-self-return-dyn-incompatibility.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A trait-object method cannot return bare `Self` because the erased concrete return type and its size are unknown to the caller.
- **Causal explanation:** `copy_like` promises the implementing type itself, but `dyn CopyLike` deliberately hides that type; the object interface therefore cannot describe the returned value.
- **Principled repair:** Mark the method Self:Sized or define a boxed clone contract.
- **Weak repair to reject:** Return `Box<dyn Any>`.

### 4. `04-associated-constant-dyn-incompatibility.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** An associated constant has no receiver and is selected through a concrete implementation, so it is not a dispatchable trait-object member.
- **Causal explanation:** `dyn Meta` cannot choose `Meta::NAME` through a vtable receiver. Dynamic metadata must be exposed by an object-callable method or separated from the erased interface.
- **Principled repair:** Move dynamic metadata to a method or split a static metadata trait.
- **Weak repair to reject:** Hard-code the value in callers.

### 5. `05-associated-type-specification.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A trait object must specify associated types that occur in its callable method signatures.
- **Causal explanation:** `Box<dyn Source>` leaves the return type of `get` unknown; an equality such as `dyn Source<Item = u8>` is required to make the erased interface complete.
- **Principled repair:** Use `dyn Source<Item=u8>` or a generic boundary.
- **Weak repair to reject:** Erase the item into String.

### 6. `06-self-sized-escape.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** A concrete-only method guarded by `Self: Sized` may construct a trait object without making that method part of the object dispatch surface.
- **Causal explanation:** `X.boxed()` runs while `Self` is known and sized, returning `Box<dyn Name>`; subsequent calls use only the object-safe `name` method.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Remove useful constructor convenience entirely.

### 7. `07-borrowed-object-lifetime.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** A trait object may contain borrowed data when its object lifetime is tied explicitly to the source borrow.
- **Causal explanation:** `Box<dyn Name + 'a>` records that the erased `Borrowed<'a>` object cannot outlive `s`; no unnecessary `'static` requirement is introduced.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Require static data unnecessarily.

### 8. `08-heterogeneous-registry.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Owned trait objects allow values of different concrete types to coexist when they share one sufficient dyn-compatible contract.
- **Causal explanation:** `Box<A>` and `Box<B>` are coerced to `Box<dyn N>`; the vector stores one erased pointer representation and dispatches `n` through each value’s vtable.
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

## Reference implementation comparison

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

## Deep reasoning and transfer

### Decisive model

> When is run-time heterogeneity real, what information does a trait object erase, and what must remain dispatchable?

Build a **dynamic-dispatch map**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Derive whether a trait is dyn-compatible and repair it without erasing its meaning.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Use borrowed and owned trait objects with correct object lifetimes.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Build a heterogeneous runtime collection behind one behavioral interface.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Compare enum, generic, and trait-object designs against explicit change scenarios.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Identify the information and capabilities lost during type erasure.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Derive whether a trait is dyn-compatible and repair it without erasing its meaning.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the dynamic-dispatch map.

### Laboratory transfer review

For [Dynamic Command Bus](../../labs/module-05-dynamic-command-bus/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In Review Engine, Module 25 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Trait Objects and Dynamic Polymorphism**, which relationship decides this question: “When is run-time heterogeneity real, what information does a trait object erase, and what must remain dispatchable?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to Review Engine?
