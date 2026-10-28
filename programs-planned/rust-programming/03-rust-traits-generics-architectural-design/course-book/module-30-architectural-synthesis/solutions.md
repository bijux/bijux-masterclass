# Reasoned Solutions — Module 30: Architectural Synthesis

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-10-inspection-platform/README.md) · [Review Engine guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 30: Architectural Synthesis**. Compare the reasoning against this question: *Given a real source of variation, how do you choose among enums, generics, trait objects, closures, functions, and ordinary composition?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Compiler specimen reasoning

### 1. `01-hybrid-dispatch.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** A design may keep stable outer boundaries generic while storing runtime-variable behavior behind trait objects.
- **Causal explanation:** `run` monomorphizes the `Source` boundary for `M` and iterates a heterogeneous slice of `Box<dyn R>` for rules, using each dispatch mechanism where its variation is real.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Erase every boundary for uniform appearance.

### 2. `02-hybrid-associated-type-mismatch.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** An associated-type equality at an engine boundary is a real requirement that every source implementation must satisfy.
- **Causal explanation:** `run` requires `S<Item = u8>`, but `X::Item` is `String`; the mismatch is rejected before the engine can index or return an assumed byte.
- **Principled repair:** Constrain the associated type at the engine boundary.
- **Weak repair to reject:** Convert arbitrary items to strings.

### 3. `03-registry-dyn-compatibility.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A runtime registry requires a dyn-compatible execution trait whose methods have fixed erased signatures.
- **Causal explanation:** `Rule::run<T>` is generic over a caller-selected type, so `Box<dyn Rule>` cannot form a finite vtable entry for that method. Static construction and dynamic execution must be separated.
- **Principled repair:** Split static construction from dyn execution.
- **Weak repair to reject:** Make all input String.

### 4. `04-builder-state-gate.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A typestate builder may expose `build` only after every required component is represented in its type parameters.
- **Causal explanation:** `B::new()` is still `B<M, M>`; the only `build` implementation belongs to `B<P<S>, P<u8>>`, so the incomplete architecture cannot be constructed.
- **Principled repair:** Complete the typestate transition.
- **Weak repair to reject:** Add a runtime panic in build.

### 5. `05-coherence-adapter-need.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A foreign trait cannot be implemented directly for a foreign collection type; a local semantic adapter must own the relationship.
- **Causal explanation:** Both `Display` and `Vec<String>` are foreign, so this crate lacks coherence authority. A local newtype can provide formatting without claiming a global meaning for all vectors.
- **Principled repair:** Introduce a local adapter newtype.
- **Weak repair to reject:** Use a type alias.

### 6. `06-opaque-report-view.rs`

- **Outcome:** `compile-pass`
- **Governing rule:** An opaque iterator return can hide the concrete adapter chain while preserving a borrowed item type and static dispatch.
- **Causal explanation:** `errors` always returns one concrete filtering iterator over `&u8`; callers see only `Iterator<Item = &u8>` and cannot depend on the internal chain.
- **Principled repair:** No repair required.
- **Weak repair to reject:** Box the iterator without runtime need.

### 7. `07-object-lifetime-in-registry.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A storage boundary requiring `T: 'static` rejects values that contain references to shorter-lived local data.
- **Causal explanation:** `B(&s)` borrows the local `String`, so it cannot satisfy the registry’s `'static` requirement. The registry must carry a lifetime or own the referenced data.
- **Principled repair:** Give the registry an explicit lifetime or own the data.
- **Weak repair to reject:** Leak the borrowed string.

### 8. `08-sealed-integrated-extension.rs`

- **Outcome:** `compile-fail`
- **Governing rule:** A sealed built-in marker intentionally prevents downstream types from joining the privileged built-in set while a separate open trait may remain extensible.
- **Causal explanation:** `Mine` can implement the open `Rule` contract, but it cannot satisfy the private prerequisite behind `BuiltIn`; the attempted privileged extension is therefore rejected.
- **Principled repair:** Implement the open execution trait or use a supported factory.
- **Weak repair to reject:** Expose sealing internals publicly.

## Exercise reasoning

Final answers are requirement-dependent. A passing answer makes selection time, openness, caller knowledge, coherence ownership, and evolution consequences explicit. Static and dynamic paths must share domain semantics. ADRs name credible alternatives. An unseen rule should enter through construction/registry extension without modifying the executor. Reporter output changes should remain visible through `R::Output`. Removing an abstraction passes when no independent variation or contract is lost.

## Variation map

A strong map usually keeps source and reporter as generic outer boundaries because one execution selects one concrete implementation of each. Their associated types preserve item and error families. Rules form a runtime heterogeneous ordered collection, so trait objects are justified there. CLI commands are a closed enum. Pure helpers remain functions. Builder states are type parameters only until construction succeeds.

The map is not a feature inventory. It is a record of who chooses variation, when selection occurs, and whether several types must coexist.

## Failure repairs

Making every component dynamic erases useful relationships and spreads lifetime/object concerns. Making every rule generic produces an engine type proportional to the rule combination and cannot hold an open heterogeneous set. Public arbitrary state mutation destroys typestate. An overbroad closure blanket implementation consumes coherence space; a named adapter wrapper localizes it. Stringifying errors too early loses classification. Deterministic ordering requires an ordered registry and tests over observable output.

## Changed requirement

Warning-only behavior usually belongs in finding severity or rule outcome data, not a second rule trait. Explanation can be a required or default object-safe method when every rule has meaningful metadata, or stored registry metadata when behavior objects should remain minimal. Loading submissions is unrelated, so the command path should query the configured policy directly. The dynamic registry remains justified because configured concrete rule types still coexist at runtime.

## Independent build

The new domain proves transfer only when names, inputs, and failure modes differ. The static relationship should be one implementation-selected family, the dynamic collection should represent real runtime openness, and typestate should remove a concrete invalid call. A downstream-style test should construct only through public APIs.

## Final defense

Begin with the product's sources of variation. Rust mechanisms follow. A convincing defense includes rejected alternatives and explains what future change each chosen boundary makes easy or difficult.

## Reference implementation comparison

The complete laboratory implementation is in [`module-10-inspection-platform/solution`](../../labs/module-10-inspection-platform/solution). Before reading it, write down:

- your public API;
- the invariant each type owns;
- the failure behavior;
- the ownership or dispatch topology;
- the complexity claim you are prepared to defend.

For **Architectural Synthesis**, compare the contract, invariant, failure behavior, ownership or dispatch topology, and cost before comparing syntax. A different implementation is sound when it preserves those properties and makes the module’s central relationship at least as clear.

## What a strong answer demonstrates

- Map axes of variation before selecting polymorphism mechanisms.
- Combine static and dynamic dispatch without duplicating domain semantics.
- Review an architecture for coherence, dyn compatibility, state validity, and evolution.
- Implement an unseen cross-cutting feature while preserving public contracts.
- Defend the selected architecture and identify a credible alternative.

A complete explanation of **Architectural Synthesis** also states the boundary of the mechanism: which guarantee it does not provide, which cost it introduces, and which simpler design should be preferred when that guarantee is unnecessary.

## Deep reasoning and transfer

### Decisive model

> Given a real source of variation, how do you choose among enums, generics, trait objects, closures, functions, and ordinary composition?

Build a **architecture decision record**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Map axes of variation before selecting polymorphism mechanisms.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Combine static and dynamic dispatch without duplicating domain semantics.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Review an architecture for coherence, dyn compatibility, state validity, and evolution.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Implement an unseen cross-cutting feature while preserving public contracts.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Defend the selected architecture and identify a credible alternative.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Map axes of variation before selecting polymorphism mechanisms.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the architecture decision record.

### Laboratory transfer review

For [Inspection Platform](../../labs/module-10-inspection-platform/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In Review Engine, Module 30 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Architectural Synthesis**, which relationship decides this question: “Given a real source of variation, how do you choose among enums, generics, trait objects, closures, functions, and ordinary composition?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to Review Engine?
