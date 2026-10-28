# Reasoned Solutions — Module 28: Boundary Traits and Adapters

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-08-boundary-ports/README.md) · [Review Engine guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 28: Boundary Traits and Adapters**. Compare the reasoning against this question: *How should a Rust program adapt external data, effects, closures, and foreign types without contaminating its core model?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Compiler specimen reasoning

### 1. `01-blanket-extension.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** A blanket extension implementation can add a method to every type satisfying the extension trait’s prerequisite bounds.
- **Causal explanation:** `impl<T: Display + ?Sized> Ext for T` includes `str`, so the borrowed string receives `bracket` while the method remains derived from `Display`.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Put every convenience method in the core trait.

### 2. `02-extension-import.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** An extension trait must be in scope before its methods participate in receiver-style lookup.
- **Causal explanation:** `u8` implements `x::Ext`, but the trait is not imported in `main`; the method therefore remains invisible despite the existing implementation.
- **Principled repair:** Import the trait.
- **Weak repair to reject:** Copy the method as a free function at every call.

### 3. `03-fn-versus-fnmut.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A closure that mutates captured state implements `FnMut`, not the stronger repeatable shared-call contract `Fn`.
- **Causal explanation:** The closure increments `n`, requiring mutable access to its capture. `twice` promises to call through an immutable callable interface, so its bound is too strong for this closure.
- **Principled repair:** Accept FnMut with mutable receiver or remove mutation.
- **Weak repair to reject:** Use RefCell solely to satisfy Fn.

### 4. `04-tryfrom-validation.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** `TryFrom` expresses a fallible conversion that may establish a stronger validated target invariant.
- **Causal explanation:** `P::try_from` rejects values above 100 and constructs the private wrapper only for admitted bytes, so both the failure and success paths preserve the percentage contract.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Implement From and panic on invalid input.

### 5. `05-generic-port-associated-error.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** A generic port may bind each implementation to its own associated error type while propagating that type through callers.
- **Causal explanation:** `run<T: S>` returns `Result<u8, T::E>`; for `M`, the projection is `Infallible`, so the generic boundary preserves the implementation-specific error family without erasure.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Convert every error to String at the trait boundary.

### 6. `06-trait-object-associated-error.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A trait object must fix associated types that appear in object-callable method signatures.
- **Causal explanation:** `Box<dyn S>` leaves `S::E` unspecified, so the erased return type `Result<u8, Self::E>` is incomplete. The object must constrain `E` or the boundary must remain generic.
- **Principled repair:** Fix the error type or keep the port generic.
- **Weak repair to reject:** Erase errors into strings without preserving sources.

### 7. `07-behavioral-fake.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** A fake is useful when it implements the same behavioral port and can deliberately exercise success and failure semantics.
- **Causal explanation:** `Fake(true)` returns the port’s declared error rather than bypassing the contract, so the test observes a real boundary behavior through the same interface.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Add test-only controls to the production trait.

### 8. `08-bound-placement.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A generic function must declare every trait capability used by its body.
- **Causal explanation:** `run` calls `load` on unconstrained `T`; because the signature does not promise `T: S`, the method is unavailable while the generic body is checked.
- **Principled repair:** Add the precise Source bound.
- **Weak repair to reject:** Make the function accept only the fake.

## Exercise reasoning

Extension traits derive convenience from a stable core. Closure adapters should carry domain identity and use the weakest callable contract. Standard conversion traits imply semantics, especially `Borrow` equivalence. Ports belong to consumers and may remain concrete, generic, or dynamic according to selection and error needs. Fakes should preserve behavior and laws rather than encode internal call order. Patterns pass only when they localize a real change.

## Port extraction

Do not wrap the standard library wholesale. A clock seam is justified when decisions depend on time; a function parameter may be enough for one timestamp. A source trait is justified when file and in-memory sources share a meaningful load contract. Printing can often be replaced by returning report data to a thin CLI shell rather than by introducing a `Console` interface.

## Closure adapter

If a rule may evaluate many submissions without mutating its callback environment, `Fn` is sufficient and strongest for callers. Mutable counters require `FnMut`, which in turn affects the `Rule` receiver and registry access. `FnOnce` would permit only one evaluation and is wrong for a reusable rule. Derive the callable bound from invocation count and mutation, not from the closure's current implementation.

## Conversion matrix

Validation can fail, so `TryFrom<String> for Email` is appropriate. A path wrapper can implement `AsRef<Path>` for a cheap borrowed view. `Borrow` has stronger equality/hash expectations and is suitable for lookup only when owned and borrowed forms compare identically. Lossy status translation should be an explicit named method or fallible conversion; `From` promises total, unsurprising conversion. Extracting a raw integer from an owning ID can be `From<DomainId>` when no invariant information is lost.

## Fakes

A credible fake preserves ordering, duplicates, and error timing defined by the port. A vector stub that can never fail does not test error propagation. Contract tests should exercise the same observable rules for every implementation without asserting private representation.

## Boundary budget

The result should be small. Traits belong where independent implementations and caller substitution are real. Configuration values, pure helper functions, and one-off operations often remain concrete or use closures.

## Boundary review reasoning

The core port should describe fetching a policy document, not operating an object-store SDK. A validated logical policy name prevents repeated syntax checks. The result may be an owned byte or text value when the core must retain it after the adapter call; a borrowed streaming handle would import the external lifecycle into every caller.

The application error should keep only distinctions that change core behavior: not found, transient unavailability, invalid policy content, and permanent external failure. Vendor request IDs or raw status structures may be retained as diagnostic sources inside the adapter without becoming domain variants. Request builders, pagination, authentication refresh, streaming handles, and vendor retry configuration remain adapter concerns.

A closure implementation usually requires `FnMut` when the fake records calls or consumes a scripted response queue; `Fn` is sufficient for a pure shared lookup. Add `'static`, `Send`, or `Sync` only if the port value is actually stored without borrowed context or moved/shared across threads. Contract tests must assert the application semantics, not the fake’s storage layout. The fake is credible only when the same not-found and invalid-content rules hold as for the production adapter.

## Reference implementation comparison

The complete laboratory implementation is in [`module-08-boundary-ports/solution`](../../labs/module-08-boundary-ports/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Boundary Traits and Adapters**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Design extension traits, closure adapters, and conversion boundaries with precise contracts.
- Use generic or dynamic ports according to ownership and deployment needs.
- Build test doubles that preserve the production contract rather than mirror internals.
- Recognize visitor, repository, and service abstractions that add more ceremony than leverage.
- Refactor a boundary while preserving the domain core.

A complete explanation of **Boundary Traits and Adapters** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.

## Deep reasoning and transfer

### Decisive model

> How should a Rust program adapt external data, effects, closures, and foreign types without contaminating its core model?

Build a **adapter boundary map**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Design extension traits, closure adapters, and conversion boundaries with precise contracts.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Use generic or dynamic ports according to ownership and deployment needs.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Build test doubles that preserve the production contract rather than mirror internals.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Recognize visitor, repository, and service abstractions that add more ceremony than leverage.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Refactor a boundary while preserving the domain core.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Design extension traits, closure adapters, and conversion boundaries with precise contracts.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the adapter boundary map.

### Laboratory transfer review

For [Boundary Ports](../../labs/module-08-boundary-ports/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In Review Engine, Module 28 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Boundary Traits and Adapters**, which relationship decides this question: “How should a Rust program adapt external data, effects, closures, and foreign types without contaminating its core model?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to Review Engine?
