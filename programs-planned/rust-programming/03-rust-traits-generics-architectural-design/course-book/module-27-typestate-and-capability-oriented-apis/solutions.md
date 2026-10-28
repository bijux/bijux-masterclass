# Reasoned Solutions — Module 27: Typestate and Capability-Oriented APIs

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-07-typestate-publication/README.md) · [Review Engine guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 27: Typestate and Capability-Oriented APIs**. Compare the reasoning against this question: *Which illegal operations can be removed from the API by representing protocol state and authority in types?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Compiler specimen reasoning

### 1. `01-typestate-transition.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** A consuming transition may change the type parameter that represents protocol state.
- **Causal explanation:** `review` consumes `Doc<Draft>` and returns `Doc<Reviewed>`; the annotated result confirms that the old state cannot remain available after the transition.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Store a boolean alongside the marker.

### 2. `02-unavailable-state-method.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Methods implemented only for one typestate are absent from all other typestate instantiations.
- **Causal explanation:** `publish` exists for `Doc<Reviewed>` but the value is `Doc<Draft>`; method lookup correctly reports that the required transition has not occurred.
- **Principled repair:** Perform the validated transition first.
- **Weak repair to reject:** Add publish to every state and return unsupported errors.

### 3. `03-private-marker-construction.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Private marker fields prevent callers from forging privileged typestates directly.
- **Causal explanation:** `Reviewed(())` requires access to its private field, so external code cannot manufacture the state that unlocks `publish`; it must use an authorized transition.
- **Principled repair:** Use public constructors and transitions.
- **Weak repair to reject:** Expose marker fields.

### 4. `04-consumed-transition-value.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A transition taking `self` moves the old-state value and makes only the returned new-state value available.
- **Causal explanation:** `x.go()` consumes `x`; trying to bind `_z = x` afterward would preserve two protocol states for one resource, so ownership rejects it.
- **Principled repair:** Use the returned state or preserve ownership in an error type.
- **Weak repair to reject:** Clone the full object before every transition.

### 5. `05-single-use-capability.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** An owned capability token is linear unless it implements a duplication mechanism such as `Copy` or `Clone`.
- **Causal explanation:** The first `use_it(p)` consumes `p`; the second call attempts to reuse an authorization that has already been spent.
- **Principled repair:** Issue a new authorized permit if policy allows.
- **Weak repair to reject:** Make the permit Copy and destroy single-use semantics.

### 6. `06-incomplete-builder.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A typestate builder exposes `build` only for the instantiation in which all required components are present.
- **Causal explanation:** `B::new()` produces `B<M, M>`, while `build` exists only for `B<P<S>, P<u8>>`; the method set records the missing configuration at compile time.
- **Principled repair:** Supply the missing component.
- **Weak repair to reject:** Add a build method that panics at runtime.

### 7. `07-state-erasure-enum.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** A closed enum can erase several typestate instantiations into one run-time value when later code must handle all states explicitly.
- **Causal explanation:** `Any` stores either `X<D>` or `X<R>`, and the exhaustive match recovers the state distinction without pretending both variants share the same methods.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Erase all state into unvalidated strings.

### 8. `08-sealed-state-parameter.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** A public generic state parameter can remain extension-controlled when its trait is sealed by a private prerequisite.
- **Causal explanation:** Only the defining module can implement the private state trait, so external code cannot invent unsupported state types for `X<T>`.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Make arbitrary state parameters legal.

## Exercise reasoning

Typestate works by method availability on concrete state parameters and consuming transitions. Visibility and sealing prevent forgery. Failed transitions should return ownership when correction is expected. Capabilities represent possession-based permission and can be single-use through moves. Typestate builders are strongest for a few programmer-supplied mandatory components; external configuration and many independent options require runtime validation. Erasure must preserve or re-establish invariants.

## Transition graph first

Typestate should mirror a real protocol, not create one. A consuming transition ensures the old state value cannot be used after success. If failure permits retry, the error must return ownership of the original state or the transition must borrow and mutate only after validation. Cancellation should be explicit when it can fail or has domain meaning; `Drop` is reserved for infallible best-effort cleanup.

## Method availability

Implement methods on `Session<New>`, `Session<Authenticated>`, and so on. Marker types can be public if callers need to name states, but fields and constructors should remain controlled so states cannot be forged. A generic state setter bypasses every invariant and reduces typestate to decoration.

## Fallible ownership

`Result<Session<Authenticated>, AuthError>` consumes the `New` session even on failure. That is correct only if retry is not required. Returning `(Session<New>, AuthError)` or a named transition error preserves retry capability and makes the surviving state explicit. The right shape follows the product's failure semantics.

## Builder cost

Typestate builders are strong when a small number of stages form an ordered protocol. Independently required fields can create combinatorial state parameters and noisy types. Runtime validation may be clearer when configuration is data-driven, partially loaded, or reported with several missing-field diagnostics at once.

## Erasure after build

Construction state is no longer useful after the invariant has been established. Returning one concrete `Engine` avoids infecting collections and functions with builder-state parameters. Optional components should usually be runtime options or strategies unless their presence changes which operations are legal.

## Architecture clinic reasoning

The all-runtime design has the smallest type surface but allows `connect` to remain callable before mandatory configuration. That may be acceptable when values are assembled dynamically and a structured error list is the desired user experience. The all-typestate design is the opposite extreme: seven independent present/missing axes imply up to 128 combinations, produce signatures dominated by marker parameters, and still cannot prove that external credentials are semantically valid.

The hybrid design encodes only the two construction facts whose absence makes `build` meaningless. Optional values remain ordinary fields with defaults or runtime validation. Credential failure should return the builder state and error together when correction and retry are requirements; consuming and discarding the builder would make a recoverable validation failure unnecessarily destructive.

A `DeployPermit` is justified when authority must be non-duplicable and consumed by the operation. A role enum or Boolean records a claim but does not itself prevent reuse. Keep permit construction private to the authority-granting component. Do not serialize the permit: external bytes must not mint compile-time authority. After a fully configured builder produces a runtime client, erasing marker types is correct because the client constructor becomes the only path into the trusted representation; the invariant is now owned by the constructed value, not by downstream generic parameters.

## Reference implementation comparison

The complete laboratory implementation is in [`module-07-typestate-publication/solution`](../../labs/module-07-typestate-publication/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Typestate and Capability-Oriented APIs**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Encode a finite protocol with marker states and consuming transitions.
- Decide which invalid operations deserve compile-time prevention.
- Prevent construction of forbidden states through visibility and sealed state markers.
- Erase typestate at a dynamic boundary without corrupting invariants.
- Quantify typestate complexity and choose a runtime state machine when appropriate.

A complete explanation of **Typestate and Capability-Oriented APIs** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.

## Deep reasoning and transfer

### Decisive model

> Which illegal operations can be removed from the API by representing protocol state and authority in types?

Build a **typestate transition graph**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Encode a finite protocol with marker states and consuming transitions.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Decide which invalid operations deserve compile-time prevention.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Prevent construction of forbidden states through visibility and sealed state markers.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Erase typestate at a dynamic boundary without corrupting invariants.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Quantify typestate complexity and choose a runtime state machine when appropriate.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Encode a finite protocol with marker states and consuming transitions.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the typestate transition graph.

### Laboratory transfer review

For [Typestate Publication](../../labs/module-07-typestate-publication/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In Review Engine, Module 27 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Typestate and Capability-Oriented APIs**, which relationship decides this question: “Which illegal operations can be removed from the API by representing protocol state and authority in types?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to Review Engine?
