# Reasoned solutions — Module 28: Boundary Traits and Adapters

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the Review Engine engineering guide](../capstone.md)

Use these explanations to review your reasoning about **Boundary Traits and Adapters**, not to substitute for an attempt. The decisive question is: *How should a Rust program adapt external data, effects, closures, and foreign types without contaminating its core model?* When your design differs, separate three possibilities: a Rust rule was applied incorrectly, the product contract changed, or two architectures satisfy the same contract with different trade-offs.

## Compiler specimen reasoning

### 1. `01-blanket-extension.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Blanket extension.
- **Causal explanation:** The specimen compiles because blanket extension.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Put every convenience method in the core trait.

### 2. `02-extension-import.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Extension import.
- **Causal explanation:** The compiler rejects the specimen because extension import.
- **Principled repair:** Import the trait.
- **Weak repair to reject:** Copy the method as a free function at every call.

### 3. `03-fn-versus-fnmut.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Fn versus FnMut.
- **Causal explanation:** The compiler rejects the specimen because fn versus FnMut.
- **Principled repair:** Accept FnMut with mutable receiver or remove mutation.
- **Weak repair to reject:** Use RefCell solely to satisfy Fn.

### 4. `04-tryfrom-validation.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** TryFrom validation.
- **Causal explanation:** The specimen compiles because tryFrom validation.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Implement From and panic on invalid input.

### 5. `05-generic-port-associated-error.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Generic port associated error.
- **Causal explanation:** The specimen compiles because generic port associated error.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Convert every error to String at the trait boundary.

### 6. `06-trait-object-associated-error.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Trait object associated error.
- **Causal explanation:** The compiler rejects the specimen because trait object associated error.
- **Principled repair:** Fix the error type or keep the port generic.
- **Weak repair to reject:** Erase errors into strings without preserving sources.

### 7. `07-behavioral-fake.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Behavioral fake.
- **Causal explanation:** The specimen compiles because behavioral fake.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Add test-only controls to the production trait.

### 8. `08-bound-placement.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Bound placement.
- **Causal explanation:** The compiler rejects the specimen because bound placement.
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

## Laboratory comparison

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
