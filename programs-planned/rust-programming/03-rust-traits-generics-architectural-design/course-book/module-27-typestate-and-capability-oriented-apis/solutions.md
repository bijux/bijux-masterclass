# Reasoned solutions — Module 27: Typestate and Capability-Oriented APIs

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the Review Engine engineering guide](../capstone.md)

Use these explanations to review your reasoning about **Typestate and Capability-Oriented APIs**, not to substitute for an attempt. The decisive question is: *Which illegal operations can be removed from the API by representing protocol state and authority in types?* When your design differs, separate three possibilities: a Rust rule was applied incorrectly, the product contract changed, or two architectures satisfy the same contract with different trade-offs.

## Compiler specimen reasoning

### 1. `01-typestate-transition.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Typestate transition.
- **Causal explanation:** The specimen compiles because typestate transition.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Store a boolean alongside the marker.

### 2. `02-unavailable-state-method.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Unavailable state method.
- **Causal explanation:** The compiler rejects the specimen because unavailable state method.
- **Principled repair:** Perform the validated transition first.
- **Weak repair to reject:** Add publish to every state and return unsupported errors.

### 3. `03-private-marker-construction.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Private marker construction.
- **Causal explanation:** The compiler rejects the specimen because private marker construction.
- **Principled repair:** Use public constructors and transitions.
- **Weak repair to reject:** Expose marker fields.

### 4. `04-consumed-transition-value.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Consumed transition value.
- **Causal explanation:** The compiler rejects the specimen because consumed transition value.
- **Principled repair:** Use the returned state or preserve ownership in an error type.
- **Weak repair to reject:** Clone the full object before every transition.

### 5. `05-single-use-capability.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Single-use capability.
- **Causal explanation:** The compiler rejects the specimen because single-use capability.
- **Principled repair:** Issue a new authorized permit if policy allows.
- **Weak repair to reject:** Make the permit Copy and destroy single-use semantics.

### 6. `06-incomplete-builder.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** Incomplete builder.
- **Causal explanation:** The compiler rejects the specimen because incomplete builder.
- **Principled repair:** Supply the missing component.
- **Weak repair to reject:** Add a build method that panics at runtime.

### 7. `07-state-erasure-enum.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** State erasure enum.
- **Causal explanation:** The specimen compiles because state erasure enum.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Erase all state into unvalidated strings.

### 8. `08-sealed-state-parameter.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** Sealed state parameter.
- **Causal explanation:** The specimen compiles because sealed state parameter.
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

## Laboratory comparison

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
